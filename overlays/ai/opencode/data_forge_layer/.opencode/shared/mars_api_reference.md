# MARS API Reference

## Purpose

This document provides the shared operational reference for the current reusable MARS API.

Its role is to help DATA_FORGE and other MARS-aware project workflows understand:

- which reusable modules already exist
- what each module is responsible for
- when to reuse the baseline declarative workflow
- when to use `src/` directly for more flexible work
- what should not be assumed or reinvented

Use this document to reduce duplicate implementation, avoid parallel APIs, and keep project work aligned with the current MARS substrate.

## Operating principles

When proposing or writing code inside a MARS-generated project:

- use real module and function names
- respect current responsibilities and boundaries
- reuse existing infrastructure before proposing new helpers or wrappers
- do not assume functionality exists unless it is explicitly described here
- if a need is not well covered by the current API, say so explicitly

Do not mix notebook-only logic with reusable project logic if a clear utility already exists under `src/`.

## Current reusable project structure

The reusable project architecture generated from MARS is currently organized as:

```text
project/
├── configs/
│   ├── config.yaml
│   └── preprocessing_recipes.yaml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_modeling.ipynb
├── scripts/
│   └── run_baseline_preprocessing.py
├── src/
│   ├── data/
│   │   ├── io.py
│   │   └── split.py
│   ├── preprocessing/
│   │   ├── cleaning.py
│   │   ├── typing.py
│   │   └── pipeline_builder.py
│   └── utils/
│       ├── config.py
│       └── paths.py
├── README.md
└── pyproject.toml
```

## Official workflow model

MARS currently supports two main workflow patterns.

### Workflow A — declarative baseline workflow

Use this workflow when the case is stable, declarative, and well described through config.

Typical fit:

- one selected preprocessing recipe
- one declared split strategy
- outputs persisted under `data/processed/`
- a reusable preprocessing path is desired

Primary surfaces:

- `configs/config.yaml`
- `configs/preprocessing_recipes.yaml`
- `scripts/run_baseline_preprocessing.py`

### Workflow B — modular experimental workflow

Use this workflow when the case is more flexible, comparative, or project-specific.

Typical fit:

- comparing multiple models
- comparing multiple preprocessing recipes
- building project-specific experiments
- working more directly from notebook or custom scripts
- avoiding unnecessary persistence of intermediate artifacts

Primary surfaces:

- `src/data/*.py`
- `src/preprocessing/*.py`
- notebooks
- project-specific scripts

Do not mix Workflow A and Workflow B carelessly.
Use the baseline path when it fits clearly.
Use the modular path when flexibility is genuinely needed.

## Core conventions

### 1. Semantic typing is explicit

MARS does not silently infer analytical feature roles from dtype at runtime.

The intended pattern is:

1. use heuristics during EDA if helpful
2. declare semantic roles explicitly in `config.yaml`
3. execute using that declared structure

Important config surfaces:

- `features.numeric`
- `features.categorical`

### 2. Split is declarative

MARS currently supports:

- `train_test`
- `train_valid_test`

The split configuration lives in `config.yaml`.

The system returns structured splits plus basic split metadata.

### 3. Recipes are preprocessing strategies

The active recipe is declared in:

- `config.yaml`
  - `preprocessing.recipe: ...`

The recipe catalog lives in:

- `configs/preprocessing_recipes.yaml`

Recipes are not model-specific identities.
They are reusable preprocessing strategies.

## Current recipe catalog

The current baseline recipe catalog includes:

- `scaled_ohe_simple`
- `robust_ohe`
- `native_cat_boosted`
- `numeric_scaled`
- `target_encoded_tree`

Do not assume a recipe belongs naturally to only one model family.
Different models may share a recipe.
One model may also be evaluated under different recipes.

## Module reference

## `src/data/io.py`

### `load_dataset(path, file_type="csv", sep=",", encoding="utf-8")`

**Responsibility**
- load datasets from disk

**Typical use**
- reading from `data/raw/...`
- baseline CSV ingestion

**Should not**
- clean data
- split data
- transform data

### `save_dataframe(df, path, file_type="csv", index=False)`

**Responsibility**
- save DataFrames to disk

**Typical use**
- persist processed outputs
- save intermediate datasets when appropriate

---

## `src/data/split.py`

### `split_features_target(df, target_col)`

**Responsibility**
- separate a DataFrame into `X` and `y`

**Arguments**
- `df`: DataFrame containing features and target
- `target_col`: target column name

**Returns**
- `X`
- `y`

### `make_dataset_splits(X, y, split_config, target_col=None)`

**Responsibility**
- create declarative dataset splits from config

**Arguments**
- `X`: feature DataFrame
- `y`: target Series
- `split_config`: split configuration dictionary
- `target_col`: optional, used for metadata

**Supported strategies**
- `train_test`
- `train_valid_test`

**Returns**
A structured dictionary of the form:

```python
{
  "splits": {
    "train": {"X": ..., "y": ...},
    "valid": {"X": ..., "y": ...},   # only if applicable
    "test": {"X": ..., "y": ...}
  },
  "metadata": {
    "strategy": ...,
    "target_column": ...,
    "stratify": ...,
    "random_state": ...,
    "requested_proportions": ...,
    "actual_sizes": ...
  }
}
```

Do not assume an older tuple-style return such as `X_train, X_test, ...`.

---

## `src/preprocessing/cleaning.py`

### `run_basic_cleaning(df, config)`

**Responsibility**
- apply safe tabular cleaning before the split

**Typical behavior may include**
- column name normalization
- string stripping
- replacing empty strings with missing values
- duplicate removal
- dropping declared columns
- explicit row filtering

**Should not**
- scale features
- encode features
- fit transforms
- contain model logic

---

## `src/preprocessing/typing.py`

### `get_target_column(config)`

**Responsibility**
- read the target from:
  - `target.column`

### `get_feature_groups(df, config)`

**Responsibility**
- read and validate:
  - `features.numeric`
  - `features.categorical`

**Validation includes**
- columns must exist
- target must not be included in features
- feature groups must not overlap
- `cleaning.drop_columns` must not conflict with declared features

**Important doctrine**
- respect explicit semantic typing
- do not perform silent dtype-based inference

**Returns**
```python
{
  "target": "...",
  "numeric_features": [...],
  "categorical_features": [...]
}
```

---

## `src/preprocessing/pipeline_builder.py`

This module no longer reads the full preprocessing configuration inline from `config.yaml`.
It resolves preprocessing through the selected recipe and the recipe catalog.

### `load_preprocessing_recipes(recipes_path=None)`

**Responsibility**
- load the recipe catalog from YAML

**Default path**
- `configs/preprocessing_recipes.yaml`

### `get_selected_recipe_name(config)`

**Responsibility**
- read the selected recipe from:
  - `config["preprocessing"]["recipe"]`

### `get_recipe_config(config, recipes_path=None)`

**Responsibility**
- resolve the full configuration of the selected recipe from the catalog

### `make_numeric_imputer(strategy="median")`

**Responsibility**
- build a numeric imputer

**Supported strategies**
- `mean`
- `median`
- `most_frequent`
- `constant`

### `make_categorical_imputer(strategy="most_frequent", fill_value="missing")`

**Responsibility**
- build a categorical imputer

**Supported strategies**
- `most_frequent`
- `constant`

### `make_scaler(name="standard")`

**Responsibility**
- build a scaler

**Supported scalers**
- `standard`
- `minmax`
- `robust`
- `none`

### `make_encoder(name="onehot")`

**Responsibility**
- build a categorical encoder

**Supported encoders**
- `onehot`
- `target`

**Important**
`TargetEncoder` may depend on the scikit-learn version available in the environment.
If it fails in a real project, do not invent a parallel workaround silently.
Propose the concrete adjustment explicitly.

### `build_numeric_pipeline(imputer_strategy="median", scaler_name="standard")`

**Responsibility**
- build the numeric pipeline
- typically `imputer -> scaler`

### `build_categorical_encoded_pipeline(imputer_strategy="most_frequent", encoder_name="onehot", fill_value="missing")`

**Responsibility**
- build the categorical encoded pipeline
- typically `imputer -> encoder`

### `build_preprocessor(numeric_features, categorical_features, config)`

**Responsibility**
- build the final `ColumnTransformer` based on the selected recipe

**Arguments**
- `numeric_features`
- `categorical_features`
- `config`

**Important behavior**
- `native_cat_boosted` may leave categorical features as passthrough
- `numeric_scaled` may ignore categorical features
- other recipes may use explicit encoding

Do not assume every recipe produces a purely numeric matrix.

---

## `src/utils/config.py`

### `load_config(path)`

**Responsibility**
- load the main YAML configuration as a dictionary

### `validate_config(config)`

**Responsibility**
- validate the minimum required structure of `config.yaml`

**Validates**
- `dataset`
- `target`
- `features`
- `cleaning`
- `split`
- `preprocessing.recipe`
- `outputs`

It does not fully validate internal recipe logic from the recipe catalog.
That resolution happens closer to the builder layer.

### `load_and_validate_config(path)`

**Responsibility**
- load and validate the main config

**Typical use**
- standard entry point for declarative scripts and workflows

---

## `src/utils/paths.py`

### `get_config_path(filename="config.yaml")`

**Responsibility**
- resolve the main config path by convention

**Typical use**
- `configs/config.yaml`

### `get_processed_data_path(filename)`

**Responsibility**
- resolve output paths under `data/processed/`

**Typical use**
- baseline script outputs

**Important**
There is already partial support for `outputs.processed_dir`.
Do not redesign path handling unless there is real friction strong enough to justify it.

---

## `scripts/run_baseline_preprocessing.py`

### `run_preprocessing(config_path=None)`

**Responsibility**
- execute the full declarative baseline preprocessing workflow

**Flow**
1. load config
2. load dataset
3. clean data
4. resolve typing
5. create declared split
6. resolve recipe
7. build preprocessor
8. fit on train
9. transform available splits
10. save outputs and metadata

**Important**
- fitting happens on train only
- `y_train` is passed to `fit`, which matters for recipes such as `target_encoded_tree`
- supports `train_test`
- supports `train_valid_test`
- saves `split_metadata.json`

### `to_dataframe(transformed_data, feature_names=None)`

**Responsibility**
- convert transformed output into a DataFrame

### `get_split_config(config)`

**Responsibility**
- read `config["split"]`

### `get_outputs_config(config)`

**Responsibility**
- read `config["outputs"]`

### `save_split_metadata(metadata, output_path)`

**Responsibility**
- save split metadata to JSON

### `save_processed_split_outputs(splits, feature_names, target_col, outputs_cfg)`

**Responsibility**
- save `X_*_processed.csv` and `y_*.csv` for all available splits

## Practical usage rules

### If the case is declarative and simple

Think first in terms of:

- `config.yaml`
- `preprocessing_recipes.yaml`
- `run_baseline_preprocessing.py`

### If the case is flexible, experimental, or multi-model

Think first in terms of:

- `split_features_target(...)`
- `make_dataset_splits(...)`
- `get_feature_groups(...)`
- `build_preprocessor(...)`

Then build experiments more modularly from notebook or project-specific scripts.

### If the need does not fit the current API

Do not pretend it already exists.

State clearly:

- what part does exist
- what part is missing
- whether the gap may deserve a MARS improvement
- or whether it is better solved locally inside the project

## Final rule

This document exists to help MARS-aware work stay precise and grounded.

If there is doubt between:

- improvising a new abstraction
- or reusing an existing MARS module

evaluate the second option first.

MARS should be reused whenever it already covers the need reasonably well.
Parallel APIs should not be invented casually.
