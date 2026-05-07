"""Zeno effect with thermal-relaxation noise (T1/T2 decoherence)."""
from __future__ import annotations

import numpy as np
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

from .zeno_circuit import build_zeno_circuit, run_zeno


def create_noise_model(
    t1: float = 50e-6,
    t2: float = 30e-6,
    gate_time: float = 50e-9,
) -> NoiseModel:
    """Create a one-qubit thermal-relaxation noise model.

    Args:
        t1: Energy relaxation time in seconds.
        t2: Dephasing time in seconds. Must be <= 2*T1 for the Aer model.
        gate_time: Approximate duration of each Ry/reset operation in seconds.
    """
    if t1 <= 0 or t2 <= 0 or gate_time <= 0:
        raise ValueError("t1, t2, and gate_time must be positive")
    noise_model = NoiseModel()
    error = thermal_relaxation_error(t1, t2, gate_time)
    noise_model.add_all_qubit_quantum_error(error, ["ry", "reset"])
    return noise_model


def run_noisy_zeno(
    n_steps: int,
    n_measurements: int,
    rotation_angle: float = np.pi,
    shots: int = 4096,
    t1: float = 50e-6,
    t2: float = 30e-6,
    gate_time: float = 50e-9,
    seed_simulator: int | None = 12345,
) -> float:
    """Run the Zeno circuit with T1/T2 noise and return P(|1>)."""
    circuit = build_zeno_circuit(n_steps, n_measurements, rotation_angle)
    noise_model = create_noise_model(t1=t1, t2=t2, gate_time=gate_time)
    simulator = AerSimulator(noise_model=noise_model, seed_simulator=seed_simulator)
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts()
    return counts.get("1", 0) / shots


def noisy_vs_ideal_sweep(
    n_steps: int = 100,
    max_measurements: int = 50,
    shots: int = 4096,
) -> dict[str, list[int] | list[float]]:
    """Compare ideal and noisy Zeno sweeps."""
    measurement_counts = list(range(0, max_measurements + 1, 5))
    ideal = [run_zeno(n_steps, m, shots=shots) for m in measurement_counts]
    noisy = [run_noisy_zeno(n_steps, m, shots=shots) for m in measurement_counts]
    return {"measurement_counts": measurement_counts, "ideal": ideal, "noisy": noisy}
