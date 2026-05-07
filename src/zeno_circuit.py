"""Quantum Zeno Effect circuit builder.

The Quantum Zeno Effect (QZE) is the inhibition of quantum evolution by
frequent observation. In this educational model, a single qubit is rotated
from |0> toward |1> using small Ry rotations. Intermediate measurements are
followed by reset operations to model post-selection / re-preparation into
|0>, making the suppression visually clear and reproducible on a simulator.
"""
from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def _validate_inputs(n_steps: int, n_measurements: int, shots: int | None = None) -> None:
    """Validate shared experiment inputs."""
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    if n_measurements < 0:
        raise ValueError("n_measurements must be non-negative")
    if n_measurements >= n_steps:
        raise ValueError("n_measurements must be less than n_steps")
    if shots is not None and shots <= 0:
        raise ValueError("shots must be positive")


def build_zeno_circuit(
    n_steps: int,
    n_measurements: int,
    rotation_angle: float = np.pi,
) -> QuantumCircuit:
    """Build a single-qubit Zeno-effect circuit.

    Args:
        n_steps: Total number of small rotation steps.
        n_measurements: Number of intermediate measurements. Zero means free
            evolution with only the final measurement.
        rotation_angle: Total intended rotation angle. ``pi`` maps |0> to |1>
            under free Ry evolution.

    Returns:
        A Qiskit ``QuantumCircuit`` with one qubit and one classical bit.
    """
    _validate_inputs(n_steps, n_measurements)
    angle_per_step = rotation_angle / n_steps
    qc = QuantumCircuit(1, 1, name=f"zeno_m{n_measurements}")

    if n_measurements == 0:
        for _ in range(n_steps):
            qc.ry(angle_per_step, 0)
    else:
        # Split n_steps into n_measurements + 1 near-equal coherent segments.
        segment_count = n_measurements + 1
        base_steps = n_steps // segment_count
        remainder = n_steps % segment_count

        for segment in range(segment_count):
            segment_steps = base_steps + (1 if segment < remainder else 0)
            for _ in range(segment_steps):
                qc.ry(angle_per_step, 0)
            if segment < n_measurements:
                qc.barrier()
                qc.measure(0, 0)
                qc.reset(0)

    qc.barrier()
    qc.measure(0, 0)
    return qc


def run_zeno(
    n_steps: int,
    n_measurements: int,
    rotation_angle: float = np.pi,
    shots: int = 4096,
    seed_simulator: int | None = 12345,
) -> float:
    """Execute the Zeno experiment and return the transition probability P(|1>)."""
    _validate_inputs(n_steps, n_measurements, shots)
    circuit = build_zeno_circuit(n_steps, n_measurements, rotation_angle)
    simulator = AerSimulator(seed_simulator=seed_simulator)
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts()
    return counts.get("1", 0) / shots


def zeno_sweep(
    n_steps: int = 100,
    max_measurements: int = 50,
    rotation_angle: float = np.pi,
    shots: int = 4096,
) -> tuple[list[int], list[float]]:
    """Sweep intermediate-measurement count and return P(|1>) values."""
    if max_measurements < 0:
        raise ValueError("max_measurements must be non-negative")
    measurement_counts = list(range(0, max_measurements + 1, 2))
    probabilities = [
        run_zeno(n_steps, n_meas, rotation_angle=rotation_angle, shots=shots)
        for n_meas in measurement_counts
    ]
    return measurement_counts, probabilities
