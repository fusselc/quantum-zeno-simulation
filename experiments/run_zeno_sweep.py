"""Run a measurement-frequency sweep for the Quantum Zeno effect."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.visualization import plot_zeno_sweep
from src.zeno_circuit import run_zeno


if __name__ == "__main__":
    n_steps = 50
    measurement_counts = list(range(0, 51))
    probabilities = [run_zeno(n_steps=n_steps, n_measurements=m, shots=4096, rotation_angle=np.pi) for m in measurement_counts]
    output = plot_zeno_sweep(measurement_counts, probabilities, output_path="experiments/zeno_sweep.png")
    print(f"Saved {output}")
