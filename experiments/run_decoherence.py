"""Run noisy-vs-ideal Zeno comparison."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.decoherence import run_zeno_with_noise
from src.visualization import plot_rabi_vs_zeno


if __name__ == "__main__":
    n_steps = 40
    measurement_counts = [0, 2, 5, 10, 20, 30]

    ideal = []
    noisy = []
    for m in measurement_counts:
        result = run_zeno_with_noise(n_steps=n_steps, n_measurements=m, rotation_angle=np.pi, shots=4096)
        ideal.append(result["ideal"])
        noisy.append(result["noisy"])

    output = plot_rabi_vs_zeno(
        {"x": measurement_counts, "y": ideal},
        {"x": measurement_counts, "y": noisy},
        output_path="experiments/decoherence_comparison.png",
    )
    print(f"Saved {output}")
