# EEG-modules-n-more
all sorts of code needed for EEG experimentation


10. Why This Workflow Works
Feature	Benefit
Self-contained experiments	Easy to track, share, and reproduce
Central shared defaults	Keeps your core configs DRY and consistent
Optional overrides	Easy to test multiple variants without rewriting files
Full config snapshots	Every run is reproducible from its saved config
CLI param overrides	Instant testing for small changes
Auto logging paths	Every run is timestamped and neatly organized
Hydra-powered flexibility	Supports complex nesting, inheritance, and CLI control
🛠 Example Full Command Flow
# Basic experiment
python scripts/run_experiment.py experiment=my_new_idea

# With override file
python scripts/run_experiment.py experiment=my_new_idea override=configs/lr_1e-4.yaml

# With CLI flags
python scripts/run_experiment.py experiment=my_new_idea training.epochs=500 model.embed_dim=256

# Combined: override file + CLI flags
python scripts/run_experiment.py experiment=my_new_idea override=configs/lr_1e-4.yaml training.epochs=600