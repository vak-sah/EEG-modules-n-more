# EEG-modules-n-more
all sorts of code needed for EEG experimentation

<pre><code># EEG-modules-n-more All sorts of modular code needed for EEG experimentation. This repository is designed to help you: - Create, configure, and run EEG model experiments quickly - Maintain a clean, reproducible folder structure - Support multiple experimental variants and override configs - Avoid cluttering Git history with output artifacts --- ## Repository Layout &gt; See the [Repository Layout](#repository-layout) section for a general overview of how folders and modules are organized. --- ## Step-by-Step Experiment Workflow ### 1. Create a New Experiment Folder Copy from an existing experiment or the default template: <pre><code>cp -r experiments/template/ experiments/my_new_idea/</code></pre>
This will create a new experiment directory with the recommended structure.

2. Define a Base Configuration
Each experiment must include a base config file at config.yaml, and the value of the name: field must match the experiment folder name.

<pre><code># experiments/my_new_idea/config.yaml name: my_new_idea model: embed_dim: 128 training: epochs: 200 </code></pre>
3. (Optional) Add Override Configs for Variants
You can define alternate configs for quick testing of different settings (e.g. learning rate, model size, etc.).

<pre><code># experiments/my_new_idea/configs/lr_1e-4.yaml training: learning_rate: 0.0001 </code></pre>
This allows clean experimentation without modifying the base config.

4. Run the Experiment with the Base Config
<pre><code>python scripts/run_experiment.py experiment=my_new_idea</code></pre>
What this does:

Loads experiments/my_new_idea/config.yaml
Merges it with the global defaults in modules/configs/default.yaml
Creates a timestamped folder in experiments/my_new_idea/runs/ for outputs
5. Run the Experiment with a Variant (Override) Config
<pre><code>python scripts/run_experiment.py experiment=my_new_idea override=configs/lr_1e-4.yaml</code></pre>
This merges config files in the following order:

modules/configs/default.yaml
experiments/my_new_idea/config.yaml
experiments/my_new_idea/configs/lr_1e-4.yaml
6. Override Parameters Directly via Command Line
You can also override config values without creating new YAML files:

<pre><code>python scripts/run_experiment.py experiment=my_new_idea training.epochs=300 model.embed_dim=256</code></pre>
This is useful for quick experiments or sweeps.

7. Output Directory & Results
Each run creates a timestamped directory like:

<pre><code>experiments/my_new_idea/runs/run_2025-07-24_12-45-03/</code></pre>
Inside each run directory:

config.yaml — the fully merged config used for that run
output_dir/ — a directory (defined inside config) for saving checkpoints, logs, plots, etc.
You can access this programmatically via cfg.output_dir inside your modules.

8. .gitignore Recommendation
To avoid cluttering Git history with logs and run results, add the following to your .gitignore file:

<pre><code>experiments/**/runs/</code></pre>