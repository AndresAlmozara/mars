# scripts/

This folder contains executable workflow scripts.

These scripts are entry points for specific tasks.  
They are not the reusable core of MARS.

The reusable logic lives in `src/`.  
Scripts in this folder call that logic when a full runnable workflow is useful.

---

## `run_baseline_preprocessing.py`

Baseline orchestration script for a simple, declarative preprocessing workflow.

### What it is for
Use this script when the project has **one clear preprocessing recipe** and you want to generate a reproducible baseline output saved to disk.

This script is useful for:
- simple tabular projects
- stable preprocessing workflows
- quick project initialization
- reproducible baseline handoff artifacts

### What it does
- load and validate the config file
- load the raw dataset
- apply safe table cleaning
- read target and feature roles
- split the data
- build the preprocessing object
- fit on training data
- transform the corresponding splits
- save processed outputs

### Typical outputs
Examples of saved outputs:
- `data/processed/X_train_processed.csv`
- `data/processed/X_test_processed.csv`
- `data/processed/y_train.csv`
- `data/processed/y_test.csv`

Optional output:
- `data/processed/cleaned_data.csv`

### When to use it
Use this script when:
- there is one main preprocessing path
- the workflow is mostly declarative
- saving processed datasets is helpful
- you want a simple reproducible baseline

### When not to use it as the main workflow
Do not treat this script as the default workflow for every project.

In more flexible or model-dependent setups, it is often better to:
- import functions directly from `src/`
- build preprocessors inside notebooks or project-specific scripts
- keep preprocessing inside model-specific sklearn pipelines

This is especially relevant for:
- multi-model benchmarking
- model-aware preprocessing recipes
- experiments with different preprocessing strategies
- workflows where preprocessing should stay attached to each model pipeline

### Typical usage
```bash
python scripts/run_baseline_preprocessing.py
```

### Custom config path
```bash
python scripts/run_baseline_preprocessing.py configs/config.yaml
```

### Summary
This script is a baseline convenience workflow, not the core of MARS.

MARS is centered on reusable modules in `src/`.  
This script is one optional way to orchestrate them in simple cases.