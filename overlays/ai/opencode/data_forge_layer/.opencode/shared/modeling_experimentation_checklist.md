# modeling_experimentation_checklist.md

## Purpose

Provide a lightweight but disciplined checklist for modeling / experimentation work inside the DS runtime.

This checklist exists to reduce sloppy experimentation, keep modeling bounded, and make downstream validation/review easier.

It is intentionally short, but it should still force explicit thinking.

---

## Modeling / experimentation checklist

Before treating a modeling task as adequately handled, confirm:

### 1. Objective and framing
- [ ] Task type is explicit
  - classification
  - regression
  - ranking
  - clustering
  - anomaly detection
  - other
- [ ] Target variable is explicit (if applicable)
- [ ] Unit of analysis is explicit
- [ ] Success criteria or comparison goal is explicit
- [ ] Important constraints are stated where relevant
  - interpretability
  - latency
  - class imbalance
  - deployment realism
  - project realism

### 2. Data and preparation awareness
- [ ] Current dataset version / preparation state is known
- [ ] Important preparation assumptions are explicit
- [ ] Model-specific preprocessing needs are stated where relevant
- [ ] Known leakage risks are surfaced
- [ ] It is clear what belongs to preparation vs modeling

### 3. Baseline discipline
- [ ] A baseline model is explicitly defined
- [ ] Baseline rationale is clear
- [ ] Baseline is simple enough to anchor comparison honestly
- [ ] Candidate models were selected for reasons, not habit or popularity

### 4. Experiment discipline
- [ ] Experiment scope is bounded
- [ ] Metrics are explicit
- [ ] Validation scheme in force is explicit
- [ ] Comparison logic is explicit
- [ ] Tuning, if any, is bounded rather than open-ended
- [ ] Each experiment cycle leaves a short decision trace

### 5. Result honesty
- [ ] Improvements are described relative to baseline
- [ ] Trade-offs are stated
- [ ] Weak, noisy, or ambiguous gains are not overstated
- [ ] Important risks or caveats are explicit
- [ ] Modeling output is not being presented as final validation

### 6. Handoff quality
- [ ] There is a short experiment summary
- [ ] Accepted / rejected candidates are explicit
- [ ] The next step is explicit
- [ ] The work is ready for validation/review, or the blocker is explicit

---

## Failure signals

If several of these are missing, the modeling work is probably not ready:

- no explicit task framing
- no explicit baseline
- no clear comparison logic
- hidden preparation assumptions
- unclear validation context
- open-ended tuning with no stopping logic
- no written experiment summary
- claims stronger than the evidence

---

## Review rule

If the checklist cannot be satisfied because:
- the task is underspecified
- preparation is still unclear
- the validation context is missing
- the modeling question itself is vague

then the correct behavior is:

- stop pretending the modeling task is complete
- surface the blocker explicitly
- request clarification or hand off appropriately

---

## Final rule

A completed modeling task is not just “a model was trained.”

A completed modeling task should leave enough structure that another DS role can understand:

- what was tried
- why it was tried
- what changed
- what remains uncertain
- what should happen next
