"""Plotting helpers for Quantum Zeno simulations."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib.pyplot as plt


def _save(fig: plt.Figure, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    return path


def plot_zeno_sweep(
    measurement_counts: Sequence[int],
    probabilities: Sequence[float],
    output_path: str | Path = "zeno_sweep.png",
) -> Path:
    """Plot P(|1>) as a function of intermediate measurement count."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(measurement_counts, probabilities, "o-", label="Zeno sweep")
    ax.set_xlabel("Number of intermediate measurements")
    ax.set_ylabel("$P(|1\\rangle)$")
    ax.set_title("Quantum Zeno suppression of transition")
    ax.grid(alpha=0.25)
    ax.legend()
    path = _save(fig, output_path)
    plt.close(fig)
    return path


def plot_rabi_vs_zeno(
    rabi_data: Mapping[str, Sequence[float]],
    zeno_data: Mapping[str, Sequence[float]],
    output_path: str | Path = "rabi_vs_zeno.png",
) -> Path:
    """Plot free Rabi evolution versus Zeno-suppressed evolution."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(rabi_data["x"], rabi_data["y"], "-", label="Rabi (no measurements)")
    ax.plot(zeno_data["x"], zeno_data["y"], "o-", label="Zeno")
    ax.set_xlabel("Control parameter")
    ax.set_ylabel("$P(|1\\rangle)$")
    ax.set_title("Rabi vs Quantum Zeno")
    ax.grid(alpha=0.25)
    ax.legend()
    path = _save(fig, output_path)
    plt.close(fig)
    return path


def plot_anti_zeno(
    data: Mapping[str, float],
    output_path: str | Path = "anti_zeno.png",
) -> Path:
    """Plot anti-Zeno demonstration data."""
    labels = list(data.keys())
    values = [float(v) for v in data.values()]
    cmap = plt.get_cmap("tab10")
    colors = [cmap(i % cmap.N) for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(labels, values, color=colors)
    ax.set_ylim(0, 1)
    ax.set_ylabel("$P(|1\\rangle)$")
    ax.set_title("Anti-Zeno effect demonstration")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.3f}", ha="center")
    path = _save(fig, output_path)
    plt.close(fig)
    return path
