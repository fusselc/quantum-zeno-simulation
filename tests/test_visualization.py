from pathlib import Path

from src.visualization import plot_anti_zeno, plot_noisy_comparison, plot_rabi_vs_zeno, plot_zeno_sweep


def test_plot_zeno_sweep_creates_file(tmp_path):
    out = tmp_path / "zeno.png"
    plot_zeno_sweep([0, 2, 4], [1.0, 0.5, 0.2], str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_rabi_vs_zeno_creates_file(tmp_path):
    out = tmp_path / "compare.png"
    plot_rabi_vs_zeno([0, 1, 2], [0, 0.5, 1], [0, 5], [1, 0.2], str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_anti_zeno_creates_file(tmp_path):
    out = tmp_path / "anti.png"
    plot_anti_zeno({"labels": ["none", "mid"], "probabilities": [1.0, 0.8]}, str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_noisy_comparison_creates_file(tmp_path):
    out = tmp_path / "noisy.png"
    plot_noisy_comparison([0, 5], [1.0, 0.2], [0.9, 0.3], str(out))
    assert out.exists()
    assert out.stat().st_size > 0
