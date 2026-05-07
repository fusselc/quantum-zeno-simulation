from src.anti_zeno import build_anti_zeno_circuit, run_anti_zeno, anti_zeno_sweep


def test_anti_zeno_circuit_contains_measurement():
    qc = build_anti_zeno_circuit(20, [10])
    ops = [inst.operation.name for inst in qc.data]
    assert "measure" in ops
    assert "reset" not in ops


def test_anti_zeno_probability_bounds():
    p = run_anti_zeno(n_steps=50, measurement_positions=[25], shots=1024)
    assert 0.0 <= p <= 1.0


def test_anti_zeno_sweep_shape():
    data = anti_zeno_sweep(n_steps=40, shots=256)
    assert "labels" in data
    assert "probabilities" in data
    assert len(data["labels"]) == len(data["probabilities"])
