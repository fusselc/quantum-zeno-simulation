"""Free Rabi oscillation: the control experiment without intermediate measurement."""
from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def build_rabi_circuit(n_steps: int, total_angle: float = np.pi) -> QuantumCircuit:
    """Build a free-rotation circuit with one final measurement."""
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    angle_per_step = total_angle / n_steps
    qc = QuantumCircuit(1, 1, name="rabi")
    for _ in range(n_steps):
        qc.ry(angle_per_step, 0)
    qc.measure(0, 0)
    return qc


def run_rabi(
    n_steps: int,
    total_angle: float = np.pi,
    shots: int = 4096,
    seed_simulator: int | None = 12345,
) -> float:
    """Run free Rabi evolution and return P(|1>)."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    circuit = build_rabi_circuit(n_steps, total_angle)
    simulator = AerSimulator(seed_simulator=seed_simulator)
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts()
    return counts.get("1", 0) / shots


def rabi_sweep(
    n_steps: int = 100,
    n_angles: int = 50,
    shots: int = 4096,
) -> tuple[list[float], list[float]]:
    """Sweep the total Ry angle from 0 to 2π and return P(|1>)."""
    if n_angles <= 0:
        raise ValueError("n_angles must be positive")
    angles = [2 * np.pi * i / n_angles for i in range(n_angles + 1)]
    probabilities = [run_rabi(n_steps, angle, shots=shots) for angle in angles]
    return angles, probabilities
