"""
run_experiment.py

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
"""

import hydra
from omegaconf import OmegaConf
from pathlib import Path
from datetime import datetime
import runpy
import sys

@hydra.main(config_path="../conf", config_name="config", version_base="1.3")
def main(cfg):
    # Step 1: Determine experiment name
    exp_name = cfg.experiment if isinstance(cfg.experiment, str) else "unnamed"

    # Step 2: Load base config for the experiment (e.g., experiments/baseline/config.yaml)
    exp_config_path = Path(f"../experiments/{exp_name}/config.yaml")
    if not exp_config_path.exists():
        print(f"[ERROR] config.yaml not found in {exp_config_path}")
        sys.exit(1)

    exp_cfg = OmegaConf.load(exp_config_path)
    cfg = OmegaConf.merge(cfg, exp_cfg)

    # Step 3: Validate consistency between folder name and config name
    if "name" not in cfg or cfg.name != exp_name:
        print(f"[ERROR] Mismatch between experiment folder and config name.")
        print(f"  Folder: {exp_name}")
        print(f"  Config name: {cfg.name if 'name' in cfg else 'MISSING'}")
        sys.exit(1)

    # Step 4: Optionally merge a second override config file (if specified)
    if "override" in cfg:
        override_path = Path(f"../experiments/{exp_name}/{cfg.override}")
        if override_path.exists():
            override_cfg = OmegaConf.load(override_path)
            cfg = OmegaConf.merge(cfg, override_cfg)
        else:
            print(f"[WARNING] Override file not found: {override_path}")

    # Step 5: Create timestamped run folder under the experiment directory
    run_time = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
    run_dir = Path(f"../experiments/{exp_name}/runs/{run_time}")
    run_dir.mkdir(parents=True, exist_ok=True)

    # Step 6: Save final merged config for reproducibility
    with open(run_dir / "config.yaml", "w") as f:
        f.write(OmegaConf.to_yaml(cfg))

    # Step 7: Add output path to config
    cfg.output_dir = str(run_dir)

    # Step 8: Run the experiment's custom main.py script
    exp_main = Path(f"../experiments/{exp_name}/main.py")
    if exp_main.exists():
        runpy.run_path(str(exp_main), init_globals={"cfg": cfg})
    else:
        print(f"[ERROR] main.py not found in: experiments/{exp_name}/")

if __name__ == "__main__":
    main()


