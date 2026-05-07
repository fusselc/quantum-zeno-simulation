"""Anti-Zeno-style demonstration with strategically placed measurements.

This module is educational rather than a full open-quantum-system derivation of
the Anti-Zeno Effect. It contrasts reset-based Zeno suppression with mid-circuit
measurements that do not reset the qubit, allowing projections into |1> to be
preserved for the final readout.
"""
from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def build_anti_zeno_circuit(
    n_steps: int,
    measurement_positions: list[int],
    rotation_angle: float = np.pi,
) -> QuantumCircuit:
    """Build a circuit with non-resetting measurements at selected step indices."""
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    invalid = [pos for pos in measurement_positions if pos < 0 or pos >= n_steps]
    if invalid:
        raise ValueError(f"measurement positions out of range: {invalid}")

    measurement_set = set(measurement_positions)
    angle_per_step = rotation_angle / n_steps
    qc = QuantumCircuit(1, 1, name="anti_zeno")

    for step in range(n_steps):
        qc.ry(angle_per_step, 0)
        if step in measurement_set:
            qc.barrier()
            qc.measure(0, 0)

    qc.barrier()
    qc.measure(0, 0)
    return qc


def run_anti_zeno(
    n_steps: int = 100,
    measurement_positions: list[int] | None = None,
    rotation_angle: float = np.pi,
    shots: int = 4096,
    seed_simulator: int | None = 12345,
) -> float:
    """Run the anti-Zeno-style experiment and return P(|1>)."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    if measurement_positions is None:
        measurement_positions = [n_steps // 2]
    circuit = build_anti_zeno_circuit(n_steps, measurement_positions, rotation_angle)
    simulator = AerSimulator(seed_simulator=seed_simulator)
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts()
    return counts.get("1", 0) / shots


def anti_zeno_sweep(
    n_steps: int = 100,
    shots: int = 4096,
) -> dict[str, list[float] | list[str]]:
    """Compare several measurement-placement strategies."""
    strategies: dict[str, list[int]] = {
        "none": [],
        "early": [n_steps // 4],
        "midpoint": [n_steps // 2],
        "late": [3 * n_steps // 4],
        "quarter+mid": [n_steps // 4, n_steps // 2],
    }
    labels = list(strategies.keys())
    probabilities = [
        run_anti_zeno(n_steps, positions, shots=shots)
        for positions in strategies.values()
    ]
    return {"labels": labels, "probabilities": probabilities}
