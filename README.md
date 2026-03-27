# MARS

**Mechanical Automation for Reusable Science**

MARS is a reusable template and bootstrap system for tabular Machine Learning and Data Science projects.

Its goal is to automate the mechanical, repeatable parts of project setup and reusable infrastructure without automating analytical judgment.

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
│           └── AGENTS.md
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

## Core template vs overlays

MARS separates:

- `template/` -> the neutral base project structure
- `overlays/` -> optional layers that can be added on top of the base project

This keeps the default template portable and editor-agnostic while still allowing workflow-specific extensions when needed.

For example, the current AI overlay can add support files for:

- GitHub Copilot
- OpenCode

## What MARS does not try to automate

MARS does not try to automate:

- full EDA
- business or domain interpretation
- storytelling
- deep analytical decisions
- final conclusions

The goal is not to replace thinking.
The goal is to remove repetitive setup and infrastructure work.

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
- OpenCode `AGENTS.md` guidance

The bootstrap script creates a new project folder from the MARS template, applies the selected overlays if requested, and replaces the relevant placeholders automatically.

## Current scope

MARS currently focuses on:

- reusable initialization
- baseline project structure
- modular preprocessing support
- configuration-driven workflows
- clean separation between reusable code and orchestration scripts
- optional overlays for workflow-specific extensions

It is intentionally kept simple and practical.
More advanced improvements are expected to emerge through real project use.

## Status

MARS is an evolving infrastructure project for building cleaner, more reusable, and more maintainable tabular ML/Data Science projects.
