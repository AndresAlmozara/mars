# MARS OpenCode Instructions

You are working inside a project built on MARS (Mechanical Automation for Reusable Science).

## Core philosophy
- automate the mechanical, repeatable, and configurable parts
- do not automate human analytical judgment
- preserve reusable architecture, clarity, robustness, maintainability, modularity, and low mental overhead
- evolve the system organically and avoid overengineering

## Repository structure
- `notebooks/` for EDA, reasoning, interpretation, and project-specific thinking
- `configs/` for declarative decisions
- `src/` for reusable modular execution logic
- `scripts/` for complete workflow orchestration when useful

Do not treat notebooks, config, `src/`, and scripts as interchangeable.

## MARS workflow rules
- Keep the baseline declarative preprocessing workflow centered on:
  - `configs/config.yaml`
  - `configs/preprocessing_recipes.yaml`
  - `scripts/run_baseline_preprocessing.py`
- For flexible or benchmark workflows, reuse modules directly from `src/` and use notebooks or project-specific scripts when needed.
- Do not mix the baseline declarative workflow and flexible benchmarking workflow without a clear reason.

## Reuse before addition
- Before making edits, inspect the relevant files and current structure instead of assuming missing functionality or missing conventions.
- Reuse existing MARS functions before proposing new helpers, wrappers, or parallel APIs.
- Important existing reusable APIs include:
  - `src/data/io.py`: `load_dataset(...)`, `save_dataframe(...)`
  - `src/data/split.py`: `split_features_target(...)`, `make_dataset_splits(...)`
  - `src/preprocessing/cleaning.py`: `run_basic_cleaning(...)`
  - `src/preprocessing/typing.py`: `get_target_column(...)`, `get_feature_groups(...)`
  - `src/preprocessing/pipeline_builder.py`: recipe selection, imputer/scaler/encoder builders, and preprocessor construction helpers
  - `src/utils/config.py`: config loading and validation helpers
  - `src/utils/paths.py`: common path helpers

## Data and preprocessing conventions
- Semantic typing is explicit, not inferred silently at runtime.
- Split is declarative and supports:
  - `train_test`
  - `train_valid_test`
- Recipes are preprocessing strategies, not model-specific recipes.
- Preserve train/test discipline and avoid leakage.

## Change policy
- Prefer minimal structural change.
- Avoid unnecessary abstractions, classes, or wrappers.
- Do not opportunistically refactor unrelated parts of the project while solving the current task.
- Distinguish between:
  - a real reusable MARS improvement
  - a local project-specific patch
  - a postponed observation
- Do not promote a project-specific workaround into reusable MARS core logic unless the reuse case is clear and structural.
- Governance rule: propose at most 3 meaningful MARS improvements per real project unless a further change is clearly structural and high impact.

## Working style
- Be direct, analytical, and architecture-aware.
- Prioritize planning, tradeoffs, and risks before implementation when the user is exploring design choices.
- Keep code changes pragmatic and scoped.
- When updating docs, keep them aligned with the actual current workflow and avoid leaving stale references to replaced tooling or outdated standards.
- Preserve the neutral core of MARS; AI integration is optional and tool-specific conventions should not leak into the default template unless explicitly requested.
