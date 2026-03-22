# {{PROJECT_NAME}}

Brief description of the project.

## Project objective

Describe the main analytical objective of the project here.

Examples:
- predict a target outcome from tabular data
- compare candidate models for a classification task
- build a reproducible baseline workflow for a portfolio project
- study the impact of selected features on model performance

## Repository structure

```text
{{PROJECT_SLUG}}/
├── configs/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
├── scripts/
├── src/
├── .gitignore
├── pyproject.toml
└── README.md
```

## Project philosophy

This project follows a structure that separates analytical reasoning from reusable execution logic:

- `notebooks/` for exploration, EDA, reasoning, interpretation, and experimentation
- `configs/` for declared project decisions
- `src/` for reusable and modular project logic
- `scripts/` for executable workflow entry points
- `docs/` for complementary technical documentation

The goal is to keep the project clear, reproducible, and easy to evolve.

## Main components

### `configs/`
Configuration files used to declare project settings and workflow decisions.

### `data/`
Project datasets.

- `data/raw/` stores original input data
- `data/processed/` stores generated processed outputs when needed

### `docs/`
Complementary technical documentation, such as:
- methodology notes
- feature engineering rationale
- preprocessing decisions
- references
- project handoff notes

### `notebooks/`
Notebooks for:
- exploratory data analysis
- reasoning and interpretation
- model experimentation
- result review

### `scripts/`
Executable scripts for specific workflow tasks.

These scripts are optional entry points.
They are not the reusable core of the project.

### `src/`
Reusable core code for:
- data loading and saving
- config handling
- path management
- safe table cleaning
- semantic feature typing
- split logic
- preprocessing object construction

## Typical workflow

A common project flow is:

`EDA -> feature decisions -> config -> preprocessing -> modeling -> evaluation`

Depending on the project, preprocessing may be handled:
- through a baseline script in `scripts/`
- directly in notebooks
- inside model-specific sklearn pipelines

## Getting started

Typical setup steps:

1. place the dataset inside `data/raw/`
2. update `configs/config.yaml`
3. start with the EDA notebook
4. define feature roles and preprocessing decisions
5. move to modeling and evaluation
6. use scripts only when they fit the workflow

## Notes

This README is a starting template.

It should be updated as the project becomes more specific, especially:
- project description
- dataset description
- methodology
- modeling approach
- evaluation strategy
- results and conclusions
