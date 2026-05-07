"""Noise-model utilities for decoherence studies."""

from __future__ import annotations

import numpy as np
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

from ._validation import validate_positive_integer
from .zeno_circuit import build_zeno_circuit

def create_noise_model(t1: float, t2: float, gate_time: float) -> NoiseModel:
    """Create a thermal relaxation noise model for single-qubit operations."""
    if t1 <= 0 or t2 <= 0 or gate_time <= 0:
        raise ValueError("t1, t2, and gate_time must all be positive")

    t2_eff = min(t2, 2 * t1)
    error = thermal_relaxation_error(t1=t1, t2=t2_eff, time=gate_time)

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ["ry", "id", "reset"])
    return noise_model


def run_zeno_with_noise(
    n_steps: int,
    n_measurements: int,
    shots: int = 4096,
    rotation_angle: float = np.pi,
    t1: float = 120e-6,
    t2: float = 80e-6,
    gate_time: float = 50e-9,
) -> dict[str, float]:
    """Compare ideal and noisy Zeno probabilities and return both."""
    validate_positive_integer(shots, "shots")
    circuit = build_zeno_circuit(n_steps, n_measurements, rotation_angle)
    ideal_result = AerSimulator().run(circuit, shots=shots).result().get_counts(circuit)

    noise_model = create_noise_model(t1=t1, t2=t2, gate_time=gate_time)
    noisy_result = (
        AerSimulator(noise_model=noise_model)
        .run(circuit, shots=shots)
        .result()
        .get_counts(circuit)
    )

    def p1(counts: dict[str, int]) -> float:
        return sum(v for k, v in counts.items() if k[0] == "1") / float(shots)

    return {"ideal": p1(ideal_result), "noisy": p1(noisy_result)}
