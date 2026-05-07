"""Rabi oscillation control experiment with no intermediate measurements."""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from ._validation import validate_positive_integer


def build_rabi_circuit(n_steps: int, total_angle: float = np.pi) -> QuantumCircuit:
    """Build a free-evolution circuit using n_steps Ry rotations."""
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")

    circuit = QuantumCircuit(1, 1)
    step_angle = total_angle / float(n_steps)
    for _ in range(n_steps):
        circuit.ry(step_angle, 0)
    circuit.measure(0, 0)
    return circuit


def run_rabi(n_steps: int, total_angle: float = np.pi, shots: int = 4096) -> float:
    """Run Rabi control experiment and return P(|1>)."""
    validate_positive_integer(shots, "shots")
    circuit = build_rabi_circuit(n_steps, total_angle)
    result = AerSimulator().run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)
    return counts.get("1", 0) / float(shots)
