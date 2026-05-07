import numpy as np

from src.rabi_oscillation import build_rabi_circuit, run_rabi, rabi_sweep


def test_rabi_circuit_structure():
    qc = build_rabi_circuit(10, np.pi)
    ops = [inst.operation.name for inst in qc.data]
    assert ops.count("ry") == 10
    assert ops.count("measure") == 1


def test_pi_rotation_reaches_one():
    p = run_rabi(100, np.pi, shots=2048)
    assert p > 0.9


def test_zero_rotation_stays_zero():
    p = run_rabi(100, 0.0, shots=1024)
    assert p < 0.05


def test_rabi_sweep_lengths():
    angles, probs = rabi_sweep(n_steps=20, n_angles=5, shots=256)
    assert len(angles) == 6
    assert len(probs) == 6
    assert all(0.0 <= p <= 1.0 for p in probs)
