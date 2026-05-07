"""Anti-Zeno experiment utilities."""

from __future__ import annotations

from numbers import Integral
from typing import Iterable, List

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def _validate_shots(shots: int) -> None:
    """Validate shot count used for simulator execution."""
    if isinstance(shots, bool) or not isinstance(shots, Integral) or shots <= 0:
        raise ValueError("shots must be a positive integer")


def build_anti_zeno_circuit(
    n_steps: int,
    measurement_positions: Iterable[int],
    rotation_angle: float = np.pi,
) -> QuantumCircuit:
    """Build circuit with strategically placed projective measurements.

    Measurements are placed only at selected steps and do not reset to |0>,
    which can increase transition probability compared with frequent resets.
    """
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")

    positions: List[int] = sorted({int(p) for p in measurement_positions if 1 <= int(p) < n_steps})
    circuit = QuantumCircuit(1, len(positions) + 1)
    step_angle = rotation_angle / float(n_steps)

    c_idx = 0
    for step in range(1, n_steps + 1):
        circuit.ry(step_angle, 0)
        if c_idx < len(positions) and step == positions[c_idx]:
            circuit.measure(0, c_idx)
            c_idx += 1

    circuit.measure(0, c_idx)
    return circuit


def run_anti_zeno(
    n_steps: int,
    measurement_positions: Iterable[int],
    rotation_angle: float = np.pi,
    shots: int = 4096,
) -> float:
    """Run anti-Zeno circuit and return final P(|1>)."""
    _validate_shots(shots)
    circuit = build_anti_zeno_circuit(n_steps, measurement_positions, rotation_angle)
    result = AerSimulator().run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    p1 = 0.0
    for bitstring, count in counts.items():
        if bitstring[0] == "1":
            p1 += count
    return p1 / float(shots)
