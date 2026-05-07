"""Run the main Quantum Zeno Effect sweep."""
from src.zeno_circuit import zeno_sweep
from src.visualization import plot_zeno_sweep


def main() -> None:
    """Execute the Zeno sweep and save a plot."""
    print("Running Quantum Zeno Effect sweep...")
    print("Sweeping 0 to 50 intermediate measurements: 100 rotation steps, π total")
    measurement_counts, probabilities = zeno_sweep(n_steps=100, max_measurements=50, shots=4096)
    print("
Results:")
    for measurements, probability in zip(measurement_counts, probabilities):
        bar = "█" * int(probability * 40)
        print(f"  {measurements:3d} measurements → P(|1⟩) = {probability:.3f} {bar}")
    plot_zeno_sweep(measurement_counts, probabilities, save_path="zeno_sweep.png")
    print("
Plot saved to zeno_sweep.png")


if __name__ == "__main__":
    main()
