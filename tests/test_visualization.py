from src.visualization import plot_anti_zeno, plot_rabi_vs_zeno, plot_zeno_sweep


def test_plot_zeno_sweep(tmp_path):
    out = plot_zeno_sweep([0, 1, 2], [0.9, 0.5, 0.2], output_path=tmp_path / "zeno.png")
    assert out.exists()


def test_plot_rabi_vs_zeno(tmp_path):
    out = plot_rabi_vs_zeno(
        {"x": [0, 1, 2], "y": [0.1, 0.5, 0.9]},
        {"x": [0, 1, 2], "y": [0.1, 0.3, 0.4]},
        output_path=tmp_path / "compare.png",
    )
    assert out.exists()


def test_plot_anti_zeno(tmp_path):
    out = plot_anti_zeno({"free": 1.0, "frequent": 0.2, "strategic": 0.6}, output_path=tmp_path / "anti.png")
    assert out.exists()


def test_plot_anti_zeno_supports_more_than_three_categories(tmp_path):
    out = plot_anti_zeno(
        {
            "free": 1.0,
            "frequent": 0.2,
            "strategic": 0.6,
            "variant_a": 0.4,
            "variant_b": 0.3,
        },
        output_path=tmp_path / "anti_many.png",
    )
    assert out.exists()
