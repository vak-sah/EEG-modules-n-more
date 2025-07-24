

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



_______________________________________________________




_______________________________________________________



_______________________________________________________



_______________________________________________________