import numpy as np

from src.decoherence import create_noise_model, run_zeno_with_noise


def test_noise_model_creation():
    model = create_noise_model(t1=120e-6, t2=80e-6, gate_time=50e-9)
    assert model is not None


def test_noisy_and_ideal_outputs_are_probabilities():
    result = run_zeno_with_noise(n_steps=30, n_measurements=10, rotation_angle=np.pi, shots=2000)
    assert set(result.keys()) == {"ideal", "noisy"}
    assert 0.0 <= result["ideal"] <= 1.0
    assert 0.0 <= result["noisy"] <= 1.0
