# DATA_FORGE for MARS

DATA_FORGE is the native Data Science agent layer for MARS-generated projects.

It is not designed as a generic standalone agent framework.
It exists to provide a **MARS-aware agentic workspace layer** for Data Science execution, review, and iterative system improvement.

## Purpose

DATA_FORGE makes MARS projects more operational by adding:

- workspace-level agent guidance
- shared project context for agentic execution
- a minimal Data Science command surface
- role-specialized agents for planning, building, and reviewing DS work

The goal is not to replace the reusable MARS substrate.
The goal is to make that substrate easier to use, extend, and pressure-test through real project work.

## Relationship with MARS

MARS is the primary system.

DATA_FORGE is intentionally built to operate on top of MARS and with direct awareness of:

- the MARS project structure
- reusable logic under `src/`
- workflow scripts under `scripts/`
- declarative configuration under `configs/`
- project conventions inherited from the MARS template

This means DATA_FORGE is intentionally **MARS-native**, not tool-agnostic.

Its purpose is to strengthen real work inside MARS projects, not to behave like a blank-slate assistant layer detached from project infrastructure.

## Design principles

DATA_FORGE is designed for practical use first.

That means:

- optimize for real project execution
- reuse existing MARS infrastructure before inventing new abstractions
- keep the public command surface small and memorable
- preserve human analytical judgment
- improve the system through runtime evidence, not speculative framework design

## Scope

DATA_FORGE is currently focused on:

- MARS-based Data Science projects
- MARS-aware agentic support
- practical project execution
- iterative refinement through real use

Standalone portability of the layer is not a current design goal.

If the layer becomes mature enough over time, parts of it may later be generalized or adapted elsewhere.
For now, it is intentionally built to strengthen MARS itself.

## Structure

A typical structure for this layer is:

```text
data_forge_layer/
├── README.md
├── AGENTS.md
└── .opencode/
    ├── shared/
    ├── agents/
    └── commands/
```

## Main components

### `AGENTS.md`
Defines the core behavioral rules of the DATA_FORGE layer.

### `.opencode/shared/`
Contains shared references and operational context used by the layer.

Typical contents may include:

- MARS context
- MARS API references
- runtime rules
- improvement guidance

### `.opencode/agents/`
Contains the specialized agent definitions used internally by the layer.

### `.opencode/commands/`
Contains the minimal public command surface for Data Science work.

## Working model

DATA_FORGE is designed to support a clear working model:

- MARS provides the reusable project substrate
- DATA_FORGE provides the Data Science agent layer
- the user remains the final analytical authority
- the system improves through repeated project use and real friction

This keeps the agent layer useful, grounded, and aligned with the actual way projects are built and refined.

## Notes

DATA_FORGE should be understood as an optional working layer on top of MARS.

- `template/` remains the reusable project base
- MARS remains the primary reusable system
- DATA_FORGE provides the Data Science-specific agent layer

The reusable substrate still lives in the generated project itself.
DATA_FORGE adds guidance, coordination, and agent-facing support around it.
