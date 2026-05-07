"""Plotting utilities for Quantum Zeno experiments."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def _prepare_path(save_path: str) -> Path:
    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def plot_zeno_sweep(
    measurement_counts: list[int],
    probabilities: list[float],
    save_path: str = "zeno_sweep.png",
) -> None:
    """Plot transition probability P(|1>) vs intermediate measurement count."""
    path = _prepare_path(save_path)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(measurement_counts, probabilities, "o-", linewidth=2, label="Measured evolution")
    ax.set_xlabel("Number of Intermediate Measurements")
    ax.set_ylabel("P(|1⟩) — Transition Probability")
    ax.set_title("Quantum Zeno Effect")
    ax.axhline(y=1.0, linestyle="--", alpha=0.5, label="Free π rotation")
    ax.axhline(y=0.0, linestyle=":", alpha=0.5, label="Complete suppression")
    ax.set_ylim(-0.05, 1.1)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)


def plot_rabi_vs_zeno(
    rabi_angles: list[float],
    rabi_probs: list[float],
    zeno_measurements: list[int],
    zeno_probs: list[float],
    save_path: str = "rabi_vs_zeno.png",
) -> None:
    """Create a side-by-side plot of free Rabi oscillation and Zeno suppression."""
    path = _prepare_path(save_path)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(rabi_angles, rabi_probs, "-", linewidth=2)
    ax1.set_xlabel("Rotation Angle (rad)")
    ax1.set_ylabel("P(|1⟩)")
    ax1.set_title("Free Rabi Oscillation")
    ax1.grid(True, alpha=0.3)

    ax2.plot(zeno_measurements, zeno_probs, "o-", linewidth=2)
    ax2.set_xlabel("Number of Measurements")
    ax2.set_ylabel("P(|1⟩)")
    ax2.set_title("Zeno Suppression for π Rotation")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)


def plot_anti_zeno(
    data: dict[str, list[float] | list[str]],
    save_path: str = "anti_zeno.png",
) -> None:
    """Plot the anti-Zeno-style measurement-placement comparison."""
    path = _prepare_path(save_path)
    labels = data["labels"]
    probabilities = data["probabilities"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, probabilities)
    ax.set_xlabel("Measurement Strategy")
    ax.set_ylabel("P(|1⟩)")
    ax.set_title("Anti-Zeno-Style Measurement Placement")
    ax.set_ylim(0, 1.05)
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)


def plot_noisy_comparison(
    measurement_counts: list[int],
    ideal: list[float],
    noisy: list[float],
    save_path: str = "noisy_comparison.png",
) -> None:
    """Plot ideal vs noisy Zeno transition probabilities."""
    path = _prepare_path(save_path)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(measurement_counts, ideal, "o-", label="Ideal")
    ax.plot(measurement_counts, noisy, "s--", label="Noisy (T1/T2)")
    ax.set_xlabel("Number of Measurements")
    ax.set_ylabel("P(|1⟩)")
    ax.set_title("Zeno Effect: Ideal vs Decoherence")
    ax.set_ylim(-0.05, 1.1)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)
