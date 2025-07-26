_______________________________________________________

# gitignore

wandb/
runs/

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


eeg-modules-n-more/
│
├── README.md
├── Dockerfile
├── .gitignore
├── requirements.txt               # core runtime deps
├── requirements-dev.txt           # lint / test / docs
├── .pre-commit-config.yaml        # auto‑format / lint / type‑check
│
├── datasets/                      # data‑source recipes
│   ├── local_paths.yaml           # absolute paths on your box / Colab
│   ├── download_tdb.yaml          # URL + SHA256 spec (optional)
│   └── fetch_tdb.py               # downloads + verifies → data_root/
│
├── experiments/                   # **Hydra configs** (nothing else)
│   ├── baseline.yaml              # defaults → ERM on laptop
│   ├── dataset/
│   │   ├── local_paths.yaml
│   │   └── download_tdb.yaml
│   ├── model/
│   │   ├── eeg_small.yaml         # embed_dim 64, 5 layers
│   │   └── eeg_big.yaml           # embed_dim 128, 8 layers
│   ├── algo/
│   │   ├── erm.yaml               # _target_: algorithms.erm.ERM
│   │   ├── group_dro.yaml         # step_size etc.
│   │   └── dfr.yaml               # teacher_temp, alpha, student_epochs
│   └── runtime/
│       ├── laptop.yaml            # CPU/GPU auto, batch_size 64
│       ├── colab.yaml             # auto‑install on start
│       └── server.yaml            # multi‑GPU flags placeholder
│
├── scripts/
│   ├── train.py                   # single entry‑point (Hydra main)
│   └── eval.py                    # test‑set evaluation / pooling
│
├── src/                           # importable Python package
│   ├── __init__.py                # exposes maybe_skip etc.
│   │
│   ├── data/
│   │   ├── base_datamodule.py     # abstract class with split helpers
│   │   └── tdb_datamodule.py      # • TDBrainDataModule
│   │   │                            - setup(), train/val/test_dataloader()
│   │   │                            - SubjectsDataset inner class
│   │
│   ├── models/
│   │   └── eeg_embed_net.py       # • PositionalEncoding
│   │                               • AddClsToken
│   │                               • CustomTransformerEncoderBlock
│   │                               • EEGEmbedNetModel (nn.Module)
│   │
│   ├── algorithms/                # plug‑and‑play losses
│   │   ├── base_algorithm.py      # • BaseAlgo (ABC)
│   │   ├── erm.py                 # • ERM  (CrossEntropyLoss)
│   │   ├── group_dro.py           # • GroupDRO (adv_probs update, worst‑group)
│   │   └── dfr.py                 # • DFR
│   │                                 attach_teacher(), KD + CE loss
│   │
│   ├── training/
│   │   ├── loop.py                # train_one_run() (epochs, early stop)
│   │   ├── callbacks.py           # EarlyStopper, EMAMetric (future hooks)
│   │   └── resume.py              # maybe_skip()  + epoch‑level stubs
│   │
│   ├── evaluation/
│   │   └── pooling.py             # pool_predictions( logits, pooling )
│   │
│   └── utils/
│       ├── repro.py               # seed_everything()
│       ├── logging.py             # build_logger() → W&B offline/online
│       ├── metrics.py             # accuracy, per‑group helpers
│       ├── paths.py               # get_data_root(), resolve save dirs
│       ├── auto_install.py        # ensure_packages([...]) for Colab
│       └── sweep.py               # hydra_to_wandb( search_space → YAML )
│
├── docs/
│   ├── source/
│   │   ├── conf.py                # Sphinx config (napoleon, autodoc)
│   │   ├── index.rst              # high‑level guide
│   │   └── api.rst                # **autogenerated API reference**
│   └── _build/                    # HTML published to GitHub Pages
│
└── .github/
    └── workflows/
        ├── ci.yml                 # lint + 1‑batch smoke tests + coverage
        └── docs.yml               # auto‑build & deploy Sphinx site


_______________________________________________________



_______________________________________________________


_______________________________________________________



_______________________________________________________


_______________________________________________________



_______________________________________________________