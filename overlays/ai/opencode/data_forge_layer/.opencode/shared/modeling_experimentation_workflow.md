# modeling_experimentation_workflow.md

## Purpose

Define the standard internal workflow for modeling / experimentation work inside the Data Science runtime.

This document exists to make the modeling lane more disciplined and reproducible **without pretending that architectural ownership is already fully solved**.

It should help the system:
- structure modeling work consistently
- avoid ad hoc experiment loops
- separate modeling execution from validation authority
- keep experiment work bounded and reviewable

This is **not** a public command.
It is an internal workflow reference.

---

## Current architectural status

Modeling / experimentation is:

- a real and necessary DS lane
- operationally active
- not yet fully closed as a clean architecture owner

Therefore, this workflow should be used to improve discipline and consistency, **not** to hide the unresolved ownership gap.

---

## What this workflow covers

This workflow covers:

- baseline model definition
- model-family selection
- model-specific preparation considerations
- bounded experiment design
- experiment comparison
- recording modeling decisions
- preparing outputs for downstream validation/review

It does **not** cover:

- final validation authority
- final methodological signoff
- generic preparation ownership
- AI-meta evaluation or system governance
- final portfolio-readiness judgment

---

## Core operating principle

Modeling work should be treated as a **bounded analytical loop**, not as open-ended trial-and-error.

Every modeling task should aim to answer a concrete question such as:

- what is the baseline?
- does this candidate improve over baseline?
- what trade-off changed?
- what assumptions or risks appeared?
- is this worth carrying forward for validation/review?

If a modeling task cannot answer a bounded question, the workflow should stop and request clarification.

---

## Standard modeling workflow

### 1. Confirm modeling objective

Before modeling starts, make explicit:

- task type
  - classification
  - regression
  - ranking
  - clustering
  - anomaly detection
  - other
- target variable (if applicable)
- unit of analysis
- success criteria
- minimum acceptable baseline
- known constraints
  - interpretability
  - latency
  - class imbalance
  - data size
  - missing values
  - deployment realism
  - business realism

If these are unclear, modeling should not proceed as if they were settled.

---

### 2. Confirm modeling-ready inputs

Before comparing models, explicitly confirm:

- what data version is being used
- whether preparation steps are already defined
- what transformations are already fixed
- what remains uncertain in preparation
- what leakage risks are already known
- what must remain outside the modeling loop

Important rule:

Modeling should not silently absorb unresolved preparation work and pretend the lane boundary does not exist.

If preparation is materially unclear, surface the dependency explicitly.

---

### 3. Define the baseline

Every modeling sequence should begin with an explicit baseline.

A baseline should be:

- simple
- understandable
- justifiable
- reproducible
- clearly named

Examples of baseline logic:

- simple linear/logistic baseline
- simple tree baseline
- majority / naive predictor where appropriate
- rule-based benchmark where appropriate

The point of the baseline is not to impress.
The point is to anchor comparison honestly.

---

### 4. Choose candidate model families deliberately

Candidate models should be selected for reasons, not because they are popular.

Good selection criteria include:

- fit to data size and feature structure
- robustness under class imbalance
- interpretability needs
- expected nonlinear behavior
- tolerance to missingness
- compatibility with current preparation choices
- realism for the intended project

Avoid:

- uncontrolled model hopping
- choosing five model families “just in case”
- treating framework availability as the same thing as modeling rationale

---

### 5. Record model-specific preparation dependencies

Some preparation decisions are model-sensitive.

Examples:

- scaling may matter for some models and not others
- encoding strategy may affect some models more strongly
- missing-value handling may vary by family
- text/vector features may require separate treatment

This should be recorded explicitly as:

- fixed preparation already shared across candidates
- model-specific preparation assumptions
- unresolved prep/model coupling risks

Do not silently bury these dependencies inside code.

---

### 6. Run bounded experiment cycles

Each experiment cycle should be bounded.

A good bounded cycle includes:

- baseline or candidate name
- preparation assumptions in force
- metrics used
- validation scheme in force
- result summary
- notable failure or caveat
- next decision

A bounded cycle should end with one of:

- keep as baseline
- keep as candidate
- reject
- needs clarification
- escalate to validation/review

Avoid open-ended tuning loops with no stopping condition.

---

### 7. Compare candidates explicitly

Comparison should not be “this one felt better.”

Comparison should explicitly state:

- what changed
- what improved
- what degraded
- whether improvement is meaningful
- whether trade-offs are acceptable
- whether evidence is strong enough to continue

Where possible, compare candidates against the baseline first, not just against each other.

---

### 8. Record experiment decisions

Every meaningful modeling pass should leave a short decision trace.

At minimum, record:

- baseline used
- candidates tested
- comparison result
- accepted / rejected candidates
- important assumptions
- unresolved risks
- what should happen next

This can be brief.
But it should exist.

---

### 9. Hand off to validation/review cleanly

Modeling does not own final judgment.

When work reaches a meaningful checkpoint, hand off with:

- the baseline definition
- the candidate summary
- the comparison summary
- important assumptions
- known risks
- known leakage concerns
- unresolved preparation/model coupling concerns

The goal is to make downstream validation easier, not to make it guess what happened.

---

## Standard output expectation

Modeling work should ideally produce:

- a named baseline
- a list of candidate models tested
- a brief comparison summary
- model-specific preparation notes when relevant
- explicit assumptions
- explicit unresolved risks
- a clear next-step recommendation

---

## Strong anti-patterns

Avoid these patterns:

- modeling without an explicit baseline
- model selection by fashion
- open-ended tuning without a bounded question
- hidden preparation/model coupling
- silent leakage risk
- presenting experimentation as final validation
- overstating weak improvements
- treating one library or workflow helper as lane ownership

---

## Relationship to other DS roles

### Preparation / transformation
Preparation may feed modeling, but modeling should not silently absorb preparation ownership.

### Evaluation / validation
Validation reviews modeling outputs; it is not replaced by modeling success.

### Review-governor
Final readiness remains outside the modeling loop.

### Reporting / packaging
Reporting should package conclusions honestly, not inflate modeling outcomes.

---

## Final rule

Use this workflow to make modeling more disciplined and reusable.

Do **not** use it to pretend that the modeling / experimentation ownership gap is already fully solved.



# modeling_experimentation_checklist.md

## Purpose

Provide a lightweight checklist for modeling / experimentation work inside the DS runtime.

This checklist is meant to reduce sloppy experimentation and make modeling outputs easier to validate and review.

It is intentionally short.

---

## Modeling / experimentation checklist

Before treating a modeling task as adequately handled, confirm:

### Objective and framing
- [ ] Task type is explicit
- [ ] Target variable is explicit (if applicable)
- [ ] Unit of analysis is explicit
- [ ] Success criteria or comparison goal is explicit

### Data and preparation awareness
- [ ] Current dataset/preparation state is known
- [ ] Important preparation assumptions are stated
- [ ] Model-specific preprocessing needs are stated where relevant
- [ ] Known leakage risks are surfaced

### Baseline discipline
- [ ] A baseline model is explicitly defined
- [ ] Baseline rationale is clear
- [ ] Candidate models are selected for reasons, not habit

### Experiment discipline
- [ ] Experiment scope is bounded
- [ ] Metrics are explicit
- [ ] Validation scheme in force is explicit
- [ ] Comparison logic is explicit
- [ ] Tuning, if any, is bounded rather than open-ended

### Result honesty
- [ ] Improvements are described relative to baseline
- [ ] Trade-offs are stated
- [ ] Weak or ambiguous gains are not overstated
- [ ] Unresolved risks are explicitly noted

### Handoff quality
- [ ] There is a short experiment summary
- [ ] The next step is clear
- [ ] The work is ready for validation/review, or the blocker is explicit

---

## Failure signals

If several of these are missing, the modeling work is probably not ready:

- no explicit baseline
- no clear comparison logic
- hidden preparation assumptions
- unclear validation context
- no written experiment summary
- claims stronger than evidence

---

## Final rule

A completed modeling task is not just “a model was trained.”

A completed modeling task should leave enough structure that another DS role can understand:

- what was tried
- why it was tried
- what happened
- what should happen next
