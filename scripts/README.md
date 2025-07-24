This is the main launcher script for running modular machine learning experiments.
Each experiment lives in its own folder under `experiments/`, with its own `config.yaml`,
custom `main.py`, and optionally a set of overrides under `configs/`.

This script handles:
- Loading a base shared config from `modules/configs/default.yaml`
- Merging the experiment's config from `experiments/<exp_name>/config.yaml`
- Optionally applying a second override config from `experiments/<exp_name>/configs/*.yaml`
- Accepting further parameter overrides via command-line
- Automatically saving a copy of the full merged config
- Running the experiment's `main.py`

Usage:
    python scripts/run_experiment.py experiment=<experiment_folder_name>
    python scripts/run_experiment.py experiment=baseline override=configs/lr_1e-4.yaml
    python scripts/run_experiment.py experiment=baseline training.epochs=300 model.embed_dim=128

Required:
- Each experiment folder (e.g., `experiments/baseline/`) must contain:
    - config.yaml (must include `name: baseline`)
    - main.py

Hydra handles command-line overrides and manages config merging.