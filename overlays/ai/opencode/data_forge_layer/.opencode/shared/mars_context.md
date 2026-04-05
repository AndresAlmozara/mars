# MARS Context

## What MARS is

MARS stands for **Mechanical Automation for Reusable Science**.

It is a reusable template and bootstrap system for tabular Machine Learning and Data Science projects.

Its purpose is to automate the mechanical, repeatable, and configurable parts of project setup and reusable infrastructure without automating analytical judgment.

MARS is the primary system.
DATA_FORGE operates on top of it as the native Data Science agent layer.

## Core philosophy

MARS is built around a simple idea:

- automate the mechanical
- do not automate human reasoning
- separate exploration from execution
- keep the system reusable, modular, and evolvable
- let the infrastructure grow through real use, not overengineering

MARS is intended to reduce setup friction, improve consistency, and provide a reusable substrate for real project work.

It is not intended to replace analytical thinking.

## What MARS automates

MARS is designed to support and automate parts of the project that are mechanical, repeatable, or infrastructure-oriented, such as:

- project initialization
- consistent repository structure
- reusable workflow scaffolding
- config-driven decisions
- data loading and saving
- safe cleaning utilities
- split logic
- preprocessing construction
- reusable scripts and path conventions

## What MARS does not try to automate

MARS does not try to automate:

- full EDA
- business or domain interpretation
- storytelling
- deep analytical decisions
- final conclusions

These remain under human control.

## Repository model

MARS projects are built around a clear separation of responsibilities.

### `notebooks/`
Used for:

- EDA
- reasoning
- interpretation
- experimentation
- project-specific analytical thinking

### `configs/`
Used for:

- declared project decisions
- configuration-driven workflow choices
- explicit feature and preprocessing choices

### `src/`
Used for:

- reusable project logic
- modular implementation
- infrastructure that should not live as ad hoc notebook code

### `scripts/`
Used for:

- executable workflow entry points
- orchestration of complete reusable flows when appropriate

### `docs/`
Used for:

- complementary technical documentation
- rationale
- methodology notes
- decisions that should not be buried in notebooks or code

Do not treat notebooks, config, `src/`, and scripts as interchangeable.

## Template and overlays

MARS separates the neutral reusable base from optional workspace-specific layers.

### `template/`
The neutral reusable project base.

It provides the default project structure and reusable starting point.

### `overlays/`
Optional extensions layered on top of the template.

These may add workflow-specific or tool-specific support without contaminating the neutral core unnecessarily.

This separation exists to keep the default MARS base clear, portable, and maintainable.

## OpenCode and DATA_FORGE

When the OpenCode overlay is used, the project may include DATA_FORGE.

DATA_FORGE is the native Data Science agent layer for MARS.

It is intentionally MARS-aware and designed to work with:

- the project structure created by MARS
- reusable logic already present in the project
- workflow scripts and configuration surfaces
- shared runtime guidance provided in the layer

DATA_FORGE should therefore assume a MARS-based environment, not a blank-slate repository.

## Workflow model

MARS may support more than one valid working style.

Two important patterns are:

### 1. Declarative baseline workflow
Typically:

- config-driven
- script-oriented
- useful when a reusable and stable path already exists

### 2. Modular experimental workflow
Typically:

- more flexible
- notebook- or script-assisted
- useful for experimentation, comparison, and project-specific iteration

Both are valid.
They should not be mixed carelessly.

## Design stance

MARS favors:

- practical reuse
- clarity
- robustness
- maintainability
- low mental overhead
- incremental improvement through real use

MARS does not favor:

- speculative abstraction
- unnecessary framework complexity
- overengineering
- replacing judgment with automation theater

## Final principle

MARS is the reusable working substrate.

It should remain clear, strong, and practical.

Agentic support layers such as DATA_FORGE should strengthen project execution on top of MARS, not replace it, duplicate it, or detach from it.
