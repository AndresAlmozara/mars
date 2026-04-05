# Modeling / Experimentation Ownership

## Purpose
Clarify how the DS system should treat modeling / experimentation as a real lane even though clean ownership is not yet fully closed.

## Current state
Modeling / experimentation is:
- architecturally required
- operationally real
- not yet fully closed as a clean owner lane

This must remain explicit.

## What this lane includes
- baseline model selection
- experiment framing
- comparison logic
- bounded tuning
- iteration on candidate models
- experiment result interpretation (pre-review)

## What this lane does NOT own
- final validation authority
- final methodological signoff
- generic feature/preparation ownership
- AI-meta evaluation
- final portfolio readiness judgment

## Current operational ownership model
Until stronger closure exists:

- `ds-build-executor` is the primary execution path for modeling work
- `ds-modeling-experimentation-specialist` is the main lane specialist
- `ds-evaluation-validation-reviewer` reviews evaluation quality and anti-overclaim discipline
- `ds-review-governor` gives final readiness judgment when needed

## Rule
The existence of the modeling specialist does NOT mean the lane is fully solved architecturally.

## Practical implication
Modeling work is allowed, but the system must remain honest that:
- execution exists
- lane closure is partial
- validation remains separate
