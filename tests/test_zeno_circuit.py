import numpy as np
import pytest

from src.zeno_circuit import build_zeno_circuit, run_zeno


def test_build_zeno_circuit_classical_bits():
    circuit = build_zeno_circuit(n_steps=20, n_measurements=5, rotation_angle=np.pi)
    assert circuit.num_qubits == 1
    assert circuit.num_clbits == 6


def test_zeno_measurements_suppress_transition():
    free = run_zeno(n_steps=40, n_measurements=0, rotation_angle=np.pi, shots=4000)
    suppressed = run_zeno(n_steps=40, n_measurements=20, rotation_angle=np.pi, shots=4000)
    assert free > 0.95
    assert suppressed < 0.05
    assert 0.0 <= suppressed <= 1.0


@pytest.mark.parametrize("shots", [0, -1, 1.5, True])
def test_run_zeno_rejects_invalid_shots(shots):
    with pytest.raises(ValueError, match="shots must be a positive integer"):
        run_zeno(n_steps=10, n_measurements=2, shots=shots)
