import numpy as np

from src.zeno_circuit import build_zeno_circuit, run_zeno


def test_build_zeno_circuit_classical_bits():
    circuit = build_zeno_circuit(n_steps=20, n_measurements=5, rotation_angle=np.pi)
    assert circuit.num_qubits == 1
    assert circuit.num_clbits == 6


def test_zeno_measurements_suppress_transition():
    free = run_zeno(n_steps=40, n_measurements=0, rotation_angle=np.pi, shots=4000)
    suppressed = run_zeno(n_steps=40, n_measurements=20, rotation_angle=np.pi, shots=4000)
    assert free > suppressed
    assert 0.0 <= suppressed <= 1.0
