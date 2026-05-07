"""Run ideal-vs-noisy Zeno comparison."""
from src.decoherence import noisy_vs_ideal_sweep
from src.visualization import plot_noisy_comparison


def main() -> None:
    """Execute ideal/noisy comparison and save a plot."""
    print("Running Zeno sweep with and without T1/T2 decoherence...")
    data = noisy_vs_ideal_sweep(n_steps=100, max_measurements=50, shots=4096)
    print("
Results:")
    for m, ideal, noisy in zip(data["measurement_counts"], data["ideal"], data["noisy"]):
        print(f"  {m:3d} measurements → ideal={ideal:.3f}, noisy={noisy:.3f}")
    plot_noisy_comparison(data["measurement_counts"], data["ideal"], data["noisy"], "noisy_comparison.png")
    print("
Plot saved to noisy_comparison.png")


if __name__ == "__main__":
    main()
