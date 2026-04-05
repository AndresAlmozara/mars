# DATA ACCESS PATTERNS

## Purpose

Standardize how DATA_FORGE should interact with data during analysis and execution.

This document focuses on inspection and handling discipline once some form of data access exists or has been reasonably described.

It is intended to help agents:

- inspect before acting
- make assumptions explicit
- work incrementally
- preserve reproducibility
- avoid sloppy transitions from data access to transformation or modeling

## Core patterns

### 1. Inspect before acting

Before applying transformations, analysis steps, or pipeline logic, inspect what is actually available.

When possible, check:

- shape
- columns
- missingness
- target presence or absence
- obvious type issues
- obvious anomalies or inconsistencies

Do not move directly from “data exists” to “processing should start”.

### 2. Explicit assumptions

If something is unclear:

- state the assumption explicitly
- distinguish known facts from inferred guesses
- keep conclusions bounded by what is actually known

Do not silently guess schema, target definition, or preparation state.

### 3. Incremental work

Prefer staged progress over premature full-pipeline behavior.

Do not:

- jump immediately to end-to-end preprocessing
- jump immediately to full modeling loops
- compress inspection, cleaning, feature engineering, and evaluation into one opaque step

Prefer:

- stepwise exploration
- progressive transformation
- bounded analytical loops
- explicit handoff points between stages

### 4. Reproducibility mindset

Prefer:

- deterministic steps where possible
- explicit transformations
- visible assumptions
- minimal hidden logic
- traceable preparation decisions

When transformations are applied, they should be understandable and reviewable.

### 5. Boundary awareness

Respect the difference between:

- data inspection
- cleaning
- feature engineering
- modeling
- validation/review

Do not let one stage silently absorb another without making that shift explicit.

This matters especially when preparation is still incomplete or when modeling is being discussed before the data state is clear.

### 6. Access-aware reasoning

The quality of the current reasoning should match the quality of the current data access.

If access is:

- direct → inspect and proceed normally
- partial → proceed cautiously and make assumptions visible
- descriptive only → support planning and methodological reasoning, but do not fake completed inspection or execution

Do not present dataset-level conclusions when the available evidence is only partial or described abstractly.

## Anti-patterns

Avoid:

- blind transformations
- implicit schema inference without stating it
- skipping validation steps
- jumping from partial access to overconfident conclusions
- mixing cleaning, feature engineering, and modeling in one opaque step
- pretending that unverified inputs are already modeling-ready

## Final rule

Good data interaction is not just “touching the dataset.”

Good data interaction should leave the work:

- clearer
- more explicit
- easier to review
- easier to reproduce
- better prepared for the next stage without hiding uncertainty
