# Quantum Zeno Effect Simulation

Educational simulations of the **Quantum Zeno Effect** using Qiskit: frequent measurement inhibits quantum state evolution.

## What this repository demonstrates

- **Free Rabi oscillation:** a qubit rotates from `|0⟩` toward `|1⟩` with no intermediate measurement.
- **Quantum Zeno suppression:** frequent measurement plus reset/post-selection suppresses the transition.
- **Anti-Zeno-style contrast:** selected mid-circuit measurements without reset can preserve projected transitions.
- **Decoherence comparison:** ideal circuits compared against T1/T2 thermal-relaxation noise using `qiskit-aer`.

## Repository layout

```text
quantum-zeno-simulation/
├── src/
│   ├── zeno_circuit.py
│   ├── rabi_oscillation.py
│   ├── anti_zeno.py
│   ├── decoherence.py
│   └── visualization.py
├── experiments/
│   ├── run_zeno_sweep.py
│   ├── run_anti_zeno.py
│   └── run_decoherence.py
├── notebooks/
│   ├── zeno_tutorial.ipynb
│   └── results_analysis.ipynb
├── tests/
├── .github/workflows/ci.yml
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/FusselChris/quantum-zeno-simulation.git
cd quantum-zeno-simulation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate with:

```powershell
.\venv\Scripts\Activate.ps1
```

## Run tests

```bash
python -m pytest tests/ -v
```

## Run experiments

```bash
python experiments/run_zeno_sweep.py
python experiments/run_anti_zeno.py
python experiments/run_decoherence.py
```

Expected qualitative result: for a total `π` rotation, `P(|1⟩)` starts near `1.0` with no intermediate measurements and drops toward `0.0` as the number of measurements increases.

## Scientific note

The main Zeno model uses intermediate measurement followed by `reset(0)`. This makes the suppression mechanism clear in a circuit simulator: each short segment has small transition probability, and repeated observation/re-preparation inhibits accumulation of amplitude in `|1⟩`. The anti-Zeno module is an educational contrast rather than a complete open-system derivation.

## License

MIT