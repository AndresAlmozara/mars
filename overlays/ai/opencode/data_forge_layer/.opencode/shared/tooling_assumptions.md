# TOOLING ASSUMPTIONS

## Purpose

Define what tools, environment conditions, and execution capabilities DATA_FORGE can reasonably assume during runtime.

This document exists to keep runtime behavior realistic, scoped, and explicit.

Its role is not to guarantee full execution conditions.
Its role is to provide a practical default baseline for reasoning and action.

## Default environment assumptions

Unless the project context clearly indicates otherwise, DATA_FORGE may reasonably assume:

- a Python environment is available
- common tabular Data Science libraries may be available
  - `pandas`
  - `numpy`
  - `scikit-learn`
- the Python standard library is available
  - `pathlib`
  - `json`
  - `os`
  - `typing`
  - `collections`
- a notebook-based workflow may be available
  - Jupyter
  - or equivalent notebook environment
- the project file structure is accessible
- relative-path project work is preferred

These are runtime defaults, not hard guarantees.

## Common but not guaranteed tools

Some projects may also have access to tools such as:

- `matplotlib`
- `seaborn`
- `scipy`
- `statsmodels`
- `pyarrow`
- `xgboost`
- `lightgbm`
- `catboost`

These may be common in DS projects, but they should not be silently assumed unless the project context, environment, or user confirms them.

## Execution assumptions

DATA_FORGE may assume that:

- code can be proposed
- scripts can be drafted
- notebooks can be structured
- reusable project logic can be referenced
- execution may be possible, but should not be silently assumed complete

If execution is materially relevant, the system should be explicit about whether it is:

- proposing code
- reasoning about code
- expecting the user to run code
- or working from already observed outputs

## File-system assumptions

DATA_FORGE may assume:

- the project structure exists
- paths inside the project should be preferred over ad hoc locations
- relative paths are usually better than hardcoded absolute paths
- files may exist in expected MARS locations, but should still be checked when relevant

Do not treat “expected project structure” as proof that the needed file is actually present.

## Non-assumptions

Do not assume by default:

- database access
- API access
- external connectors
- internet availability
- external mounts
- cloud storage access
- enterprise workspace integration
- unrestricted compute
- guaranteed package/version parity across environments

Do not behave as if these capabilities exist unless the user or the runtime context makes them explicit.

## Runtime realism rule

Treat tooling assumptions as a working baseline, not as a license to fake operational certainty.

If a request depends on tooling or environment capabilities that are not confirmed:

- say so explicitly
- proceed with the part that is still safely supportable
- distinguish between “can be designed” and “can be executed now”
- avoid silently upgrading assumptions into facts

## Large-computation rule

If the proposed work may involve large computation, heavy tuning, expensive processing, or long-running notebook/script execution:

- keep scope bounded
- warn about the likely computational weight when relevant
- prefer narrower or staged suggestions when possible
- avoid acting as if heavyweight execution is trivial

The goal is to stay practical, not timid.

## Version and dependency caution

When suggesting code that depends on tooling details:

- prefer conservative assumptions
- avoid relying on fragile or niche behavior unless justified
- be explicit when a component may depend on package version or environment state
- do not hide compatibility risk behind confident wording

If a specific workflow depends on a version-sensitive component, surface that dependency honestly.

## Relationship to other shared docs

This document works together with:

- `connectors.md` for data-access conditions
- `data_access_patterns.md` for inspection and handling discipline
- `mars_api_reference.md` for reusable project surfaces
- lane-specific workflow/checklist docs when downstream work depends on confirmed environment capabilities

## Final rule

Assume enough to be useful.
Do not assume so much that the system becomes misleading.

A good runtime assumption should help DATA_FORGE move work forward while staying honest about what is available, what is uncertain, and what still depends on real execution conditions.
