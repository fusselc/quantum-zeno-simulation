"""Run a simple anti-Zeno comparison experiment."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.anti_zeno import run_anti_zeno
from src.visualization import plot_anti_zeno
from src.zeno_circuit import run_zeno


if __name__ == "__main__":
    n_steps = 40
    shots = 4096

    free = run_anti_zeno(n_steps=n_steps, measurement_positions=[], rotation_angle=np.pi, shots=shots)
    frequent_reset = run_zeno(n_steps=n_steps, n_measurements=20, rotation_angle=np.pi, shots=shots)
    strategic = run_anti_zeno(
        n_steps=n_steps,
        measurement_positions=[30, 34, 37],
        rotation_angle=np.pi,
        shots=shots,
    )

    output = plot_anti_zeno(
        {
            "Free": free,
            "Frequent Zeno": frequent_reset,
            "Strategic (Anti-Zeno)": strategic,
        },
        output_path="experiments/anti_zeno.png",
    )
    print(f"Saved {output}")
