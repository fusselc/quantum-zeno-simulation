"""Quantum Zeno effect circuit builders and runners."""

from __future__ import annotations

from typing import Set

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def _measurement_steps(n_steps: int, n_measurements: int) -> Set[int]:
    """Return evenly spaced intermediate measurement steps in 1..n_steps-1."""
    if n_measurements <= 0 or n_steps <= 1:
        return set()
    capped = min(n_measurements, n_steps - 1)
    positions = np.linspace(1, n_steps - 1, capped, dtype=int)
    return set(int(pos) for pos in positions)


def build_zeno_circuit(
    n_steps: int,
    n_measurements: int,
    rotation_angle: float = np.pi,
) -> QuantumCircuit:
    """Build a Zeno circuit using small Ry rotations and intermediate measurements.

    Intermediate measurements include a reset so the state is projected back to |0>.
    """
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    if n_measurements < 0:
        raise ValueError("n_measurements must be non-negative")

    measurement_steps = _measurement_steps(n_steps, n_measurements)
    circuit = QuantumCircuit(1, len(measurement_steps) + 1)
    step_angle = rotation_angle / float(n_steps)

    c_idx = 0
    for step in range(1, n_steps + 1):
        circuit.ry(step_angle, 0)
        if step in measurement_steps:
            circuit.measure(0, c_idx)
            circuit.reset(0)
            c_idx += 1

    circuit.measure(0, c_idx)
    return circuit


def run_zeno(
    n_steps: int,
    n_measurements: int,
    shots: int = 4096,
    rotation_angle: float = np.pi,
) -> float:
    """Execute the Zeno circuit and return final P(|1>)."""
    circuit = build_zeno_circuit(n_steps, n_measurements, rotation_angle)
    result = AerSimulator().run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    p1 = 0.0
    for bitstring, count in counts.items():
        if bitstring[0] == "1":
            p1 += count
    return p1 / float(shots)
