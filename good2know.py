

# Never hardcode values in main scripts (except paths to configs!)

_______________________________________________________


from utils.config_loader import load_config, update_config

base_config = load_config("config/default.yaml")
exp_config = load_config("experiments/experiment_dfr/config.yaml")
cfg = update_config(base_config, exp_config)

# Access like cfg["training"]["epochs"]


_______________________________________________________

import hydra
from omegaconf import DictConfig, OmegaConf
from modules.train.trainer import Trainer

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    trainer = Trainer(cfg)
    trainer.train()

if __name__ == "__main__":
    main()

_______________________________________________________


# rewrite with proper naming convetion and documentation 

_______________________________________________________


simple_key: value

nested_block:
  key1: val1
  key2: val2

list_example:
  - item1
  - item2

boolean: true
float_val: 0.001
null_val: null


Indentation matters (always 2 spaces)
No tabs allowed
Comments use #

_______________________________________________________


# modules/train/trainer.py

class Trainer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.device = "cuda"  # or dynamic check

        self.model = self.build_model(cfg.model)
        self.optimizer = self.build_optimizer()
        # etc...

    def build_model(self, model_cfg):
        if model_cfg.type == "EEGEmbedNet":
            return EEGEmbedNet(
                embed_dim=model_cfg.embed_dim,
                dropout=model_cfg.dropout_rate,
                # ...
            )
        # Add more types here

    def build_optimizer(self):
        import torch.optim as optim
        return optim.AdamW(
            self.model.parameters(),
            lr=self.cfg.training.learning_rate,
            weight_decay=self.cfg.training.weight_decay
        )

    def train(self):
        print(f"Training {self.cfg.model.type} for {self.cfg.training.epochs} epochs")
        # loop through data, etc...


_______________________________________________________


your-repo/
├── modules/                    # All reusable code
│   ├── model/
│   ├── train/
│   ├── data/
│   └── configs/
│       └── default.yaml        # Default config
│
├── experiments/                # All experiments here
│   ├── baseline/
│       ├── config.yaml
│       └── main.py
│   ├── group_dro/
│   │   ├── config.yaml         # Custom config for this experiment
│   │   ├── main.py             # Custom pipeline
│   │   └── runs/               # Automatically created folders per run
│   │       ├── run_2025-07-23_09-15-12/
│   │       │   ├── config.yaml
│   │       │   ├── logs/
│   │       │   ├── checkpoints/
│   │       │   └── plots/
│   │       └── ...
│   └── mixup/
│       ├── config.yaml
│       ├── main.py
│       └── runs/
│           └── run_2025-07-23_10-03-01/
│
├── scripts/
│   └── run_experiment.py       # Master launcher
│
├── conf/
│   └── config.yaml             # Hydra entrypoint

_______________________________________________________


scripts/run_experiment.py — Master runner
import hydra
from omegaconf import OmegaConf
from pathlib import Path
from datetime import datetime
import runpy
import shutil

@hydra.main(config_path="../conf", config_name="config", version_base="1.3")
def main(cfg):
    exp_name = cfg.experiment.name if "name" in cfg.experiment else "unnamed"
    run_time = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
    
    # Create output dir under the experiment folder
    run_dir = Path(f"../experiments/{exp_name}/runs/{run_time}")
    run_dir.mkdir(parents=True, exist_ok=True)

    # Save merged config
    with open(run_dir / "config.yaml", "w") as f:
        f.write(OmegaConf.to_yaml(cfg))

    # Save checkpoint/log dir path to config
    cfg.output_dir = str(run_dir)

    # If custom main exists, run it
    exp_main = Path(f"../experiments/{exp_name}/main.py")
    if exp_main.exists():
        runpy.run_path(str(exp_main), init_globals={"cfg": cfg})
    else:
        print("No custom main.py for this experiment")

if __name__ == "__main__":
    main()

_______________________________________________________

Example experiments/new_idea/main.py
from modules.train.trainer import Trainer

def run(cfg):
    print("Running:", cfg.name)
    trainer = Trainer(cfg)
    trainer.train()

run(cfg)

_______________________________________________________

# put entry point scripts like plot_results.py in scripts/ if they are CLI-style executables (e.g., called from terminal)

_______________________________________________________

# custom override YAML file (not just CLI flags)

python scripts/run_experiment.py experiment=new_idea override=configs/hyperparam_sweep_1.yaml


_______________________________________________________

Usage Scenarios

Basic run (uses experiments/group_dro/config.yaml)
python scripts/run_experiment.py experiment=group_dro

Use additional override YAML
python scripts/run_experiment.py experiment=group_dro override=configs/lr_1e-4.yaml

Override hyperparameters on the fly
python scripts/run_experiment.py experiment=group_dro training.epochs=200 model.embed_dim=256

_______________________________________________________

experiments/**/runs/
# ignore all runs/ folders inside any subdirectory of experiments/.

_______________________________________________________


_______________________________________________________



_______________________________________________________


_______________________________________________________



_______________________________________________________


_______________________________________________________



_______________________________________________________