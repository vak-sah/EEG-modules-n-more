# EEG-modules-n-more
all sorts of code needed for EEG experimentation

see "repository layout" for a general overview

Step-by-Step Experiment Workflow
1. Create a new experiment folder
Copy from a template (or an existing experiment):

<pre><code>cp -r experiments/template/ experiments/my_new_idea/</code></pre>


2. Define base configuration
Every experiment must include a config.yaml with a name: field matching the folder name:

<pre><code># experiments/my_new_idea/config.yaml name: my_new_idea model: embed_dim: 128 training: epochs: 200 </code></pre>


3. (Optional) Add override config for variants
You can define alternate configs (e.g. for learning rates, model sizes, etc.):

<pre><code># experiments/my_new_idea/configs/lr_1e-4.yaml training: learning_rate: 0.0001 </code></pre>


4. Run experiment with base config
<pre><code>python scripts/run_experiment.py experiment=my_new_idea</code></pre>

This:
Loads experiments/my_new_idea/config.yaml
Merges it with modules/configs/default.yaml
Creates a timestamped folder in experiments/my_new_idea/runs/

5. Run with a variant override config
<pre><code>python scripts/run_experiment.py experiment=my_new_idea override=configs/lr_1e-4.yaml</code></pre>

This merges:
Global defaults
config.yaml from the experiment folder
Then the specific override config


6. Override individual parameters directly from CLI
<pre><code>python scripts/run_experiment.py experiment=my_new_idea training.epochs=300 model.embed_dim=256</code></pre>

This lets you test quick ideas without creating new YAMLs.


7. Where do results go?
All logs, configs, plots, and checkpoints for each run are saved to:

<pre><code>experiments/my_new_idea/runs/run_YYYY-MM-DD_HH-MM-SS/</code></pre>
📌 Inside that folder you’ll find:

config.yaml — snapshot of the full merged config
output_dir — available inside cfg for saving models, logs, etc.

8. .gitignore recommendation
To avoid cluttering Git with logs and run outputs, add this to your .gitignore:

<pre><code>experiments/**/runs/</code></pre>