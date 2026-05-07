from src.decoherence import create_noise_model, run_noisy_zeno


def test_noise_model_has_quantum_errors():
    noise_model = create_noise_model()
    assert len(noise_model._local_quantum_errors) > 0


def test_noisy_zeno_probability_bounds():
    p = run_noisy_zeno(30, 5, shots=512)
    assert 0.0 <= p <= 1.0
