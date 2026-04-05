# MARS

**Mechanical Automation for Reusable Science**

MARS is a reusable template and bootstrap system for tabular Machine Learning and Data Science projects.

Its purpose is to automate the mechanical, repeatable parts of project setup and reusable infrastructure without automating analytical judgment.

MARS is designed as a practical working system first:
- for building projects faster,
- with more consistency,
- and with a reusable technical substrate that can improve through real use.

## Philosophy

MARS is built around a simple idea:

- automate the mechanical
- do not automate human reasoning
- separate exploration from execution
- keep the system reusable, modular, and evolvable
- let the infrastructure grow through real use, not overengineering

In practice, this means:

- `notebooks/` for EDA, reasoning, interpretation, and experimentation
- `configs/` for declared decisions
- `src/` for reusable logic
- `scripts/` for executable workflows
- `template/` for the neutral project base
- `overlays/` for optional extensions
- `tools/` for MARS infrastructure utilities

## Repository structure

```text
mars/
├── template/
│   ├── configs/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── docs/
│   ├── notebooks/
│   ├── scripts/
│   ├── src/
│   ├── .gitignore
│   ├── README.md
│   └── pyproject.toml
├── overlays/
│   └── ai/
│       ├── copilot/
│       │   └── .github/
│       │       └── copilot-instructions.md
│       └── opencode/
│           ├── README.md
│           └── data_forge_layer/
│               ├── README.md
│               ├── AGENTS.md
│               └── .opencode/
│                   ├── shared/
│                   ├── agents/
│                   └── commands/
└── tools/
    └── create_mars_project.py
```

## What MARS provides

MARS helps initialize and structure new tabular ML/Data Science projects by providing:

- a reusable neutral project template
- modular reusable core code
- baseline preprocessing structure
- consistent project layout
- optional overlays for workflow-specific extensions
- a bootstrap script to create new projects from the template

MARS is not only a folder scaffold.
It is intended to become a reusable working substrate for real projects.

## Core template vs overlays

MARS separates:

- `template/` -> the neutral base project structure
- `overlays/` -> optional layers that can be added on top of the base project

This keeps the default template portable and editor-agnostic while still allowing workflow-specific extensions when needed.

For example, the current AI overlays can add support for:

- GitHub Copilot
- OpenCode

## OpenCode and DATA_FORGE

The OpenCode overlay is not just a generic assistant setup.

It installs a MARS-aware agentic workspace configuration centered on **DATA_FORGE**, the native Data Science agent layer for MARS.

DATA_FORGE is designed to work specifically with:

- the MARS project structure
- reusable code under `src/`
- executable workflows under `scripts/`
- declarative project configuration under `configs/`
- shared conventions and support surfaces defined inside the overlay

This means the current OpenCode integration is intentionally **MARS-native**, not tool-agnostic.

That is a deliberate design choice.

The goal is not to build a standalone generic Data Science agent framework first.
The goal is to make MARS more powerful, faster, and more consistent for real project work.

If this agent layer becomes mature enough over time, parts of it may later be generalized or adapted to other agentic systems.
That is a possible future direction, not a current design requirement.

## What MARS does not try to automate

MARS does not try to automate:

- full EDA
- business or domain interpretation
- storytelling
- deep analytical decisions
- final conclusions

The goal is not to replace thinking.
The goal is to remove repetitive setup and infrastructure work while supporting faster and more disciplined execution.

## Creating a new project

From the root of `mars/`, run one of the following commands.

### Base project only

```bash
python tools/create_mars_project.py --name "My New Project" --destination "PATH/TO/PORTFOLIO"
```

### Base project + Copilot overlay

```bash
python tools/create_mars_project.py --name "My New Project" --destination "PATH/TO/PORTFOLIO" --with-copilot
```

### Base project + OpenCode overlay

```bash
python tools/create_mars_project.py --name "My New Project" --destination "PATH/TO/PORTFOLIO" --with-opencode
```

### Base project + both AI overlays

```bash
python tools/create_mars_project.py --name "My New Project" --destination "PATH/TO/PORTFOLIO" --with-ai
```

`--with-ai` includes the current recommended optional AI workspace setup:

- GitHub Copilot instructions
- OpenCode overlay with the DATA_FORGE layer

The bootstrap script creates a new project folder from the MARS template, applies the selected overlays if requested, and replaces the relevant placeholders automatically.

## Current scope

MARS currently focuses on:

- reusable initialization
- baseline project structure
- modular preprocessing support
- configuration-driven workflows
- clean separation between reusable code and orchestration scripts
- optional overlays for workflow-specific extensions
- MARS-native agentic support for Data Science work through DATA_FORGE

It is intentionally kept practical and use-oriented.
More advanced improvements are expected to emerge through real project use, not speculative framework design.

## Status

MARS is an evolving infrastructure system for building cleaner, more reusable, and more maintainable tabular ML/Data Science projects.

Its current direction is:

- keep the reusable substrate strong
- improve project execution speed and consistency
- let the agent layer and the infrastructure co-evolve through real use
- preserve human analytical control while reducing mechanical friction
