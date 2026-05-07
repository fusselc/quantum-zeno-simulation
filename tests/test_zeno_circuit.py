import numpy as np
import pytest

from src.zeno_circuit import build_zeno_circuit, run_zeno


def test_circuit_has_one_qubit():
    qc = build_zeno_circuit(10, 0)
    assert qc.num_qubits == 1


def test_free_evolution_reaches_one():
    p = run_zeno(100, 0, rotation_angle=np.pi, shots=2048)
    assert p > 0.9


def test_many_measurements_suppresses():
    p = run_zeno(100, 30, rotation_angle=np.pi, shots=2048)
    assert p < 0.3


def test_zeno_monotonic_suppression():
    p_few = run_zeno(100, 2, shots=4096)
    p_many = run_zeno(100, 20, shots=4096)
    assert p_many < p_few


def test_zero_angle_stays_zero():
    p = run_zeno(100, 5, rotation_angle=0.0, shots=1024)
    assert p < 0.05


def test_circuit_structure_with_measurements():
    qc = build_zeno_circuit(10, 3)
    ops = [inst.operation.name for inst in qc.data]
    assert "measure" in ops
    assert "ry" in ops
    assert "reset" in ops


def test_invalid_measurement_count_raises():
    with pytest.raises(ValueError):
        build_zeno_circuit(10, 10)
