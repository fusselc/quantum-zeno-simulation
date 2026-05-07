import numpy as np

from src.anti_zeno import run_anti_zeno
from src.zeno_circuit import run_zeno


def test_anti_zeno_probability_bounds():
    p = run_anti_zeno(n_steps=40, measurement_positions=[30, 34, 37], rotation_angle=np.pi, shots=3000)
    assert 0.0 <= p <= 1.0


def test_strategic_measurements_exceed_frequent_zeno():
    strategic = run_anti_zeno(n_steps=40, measurement_positions=[30, 34, 37], rotation_angle=np.pi, shots=4000)
    frequent = run_zeno(n_steps=40, n_measurements=20, rotation_angle=np.pi, shots=4000)
    assert strategic > frequent
