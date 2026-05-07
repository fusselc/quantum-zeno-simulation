"""Run the anti-Zeno-style measurement-placement experiment."""
from src.anti_zeno import anti_zeno_sweep
from src.visualization import plot_anti_zeno


def main() -> None:
    """Execute anti-Zeno-style sweep and save a plot."""
    print("Running Anti-Zeno-style measurement-placement comparison...")
    data = anti_zeno_sweep(n_steps=100, shots=4096)
    for label, probability in zip(data["labels"], data["probabilities"]):
        print(f"  {label:>11s} → P(|1⟩) = {probability:.3f}")
    plot_anti_zeno(data, save_path="anti_zeno.png")
    print("
Plot saved to anti_zeno.png")


if __name__ == "__main__":
    main()
