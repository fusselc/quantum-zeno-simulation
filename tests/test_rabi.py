import numpy as np

from src.rabi_oscillation import run_rabi


def test_rabi_probability_bounds():
    p = run_rabi(n_steps=40, total_angle=np.pi / 2, shots=3000)
    assert 0.0 <= p <= 1.0


def test_rabi_full_rotation_reaches_one():
    p = run_rabi(n_steps=40, total_angle=np.pi, shots=3000)
    assert p > 0.9
