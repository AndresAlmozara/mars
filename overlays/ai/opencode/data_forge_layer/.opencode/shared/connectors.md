# CONNECTORS

## Purpose

Define how DATA_FORGE should access, interpret, and reason about data inputs across the DS runtime.

This document is not about external integration breadth.
It is about disciplined handling of available data access conditions inside MARS-based project work.

Its goals are to:

- standardize how agents identify and validate data sources
- avoid false assumptions about availability
- distinguish access limitations from structural system gaps
- support explicit, scoped, and honest runtime behavior

## Accepted data source types

DATA_FORGE may work with:

- local files inside the project structure
  - CSV
  - Parquet
  - similar tabular files
- in-memory dataframes
- user-provided paths or file references
- user-described datasets when direct access is not available

These should be treated as different access conditions, not as interchangeable states.

## Default access model

When data access is needed, agents should follow this sequence:

1. identify the current data source type
2. verify whether the data is actually accessible
3. determine whether the schema is known, partially known, or unknown
4. decide whether useful progress can be made safely
5. proceed, request clarification, or surface the access constraint explicitly

Do not jump directly from “the user mentioned data” to “full data access exists”.

## Access states

At runtime, treat data access as one of the following states:

### 1. Directly available
The data is accessible through:
- local files
- already loaded dataframe objects
- clearly available project paths

This is the easiest case.
Proceed with normal inspection and analysis discipline.

### 2. Partially available
The data is only partly accessible, for example:
- path known but file not yet confirmed
- schema partly described
- sample shown but full dataset unavailable
- target mentioned but not verified

Proceed cautiously.
State assumptions explicitly.
Avoid pretending full access exists.

### 3. Described but not accessible
The user describes the dataset, but the system does not have direct access to it.

This is still a workable state for:
- planning
- reasoning
- workflow design
- preparation or modeling strategy discussion
- checklist-driven guidance

But it is not enough for pretending that inspection or execution already happened.

### 4. Blocked or missing
The data is expected but currently unavailable.

Examples:
- missing file
- invalid path
- inaccessible mount
- unclear source
- required sample/schema absent

In this case:
- identify the constraint clearly
- say what cannot be confirmed
- request the smallest useful clarification or artifact when needed

## Standard runtime behavior

Agents should:

- inspect availability before acting
- prefer explicit confirmation over silent guessing
- state assumptions when access is partial
- stay scoped to what the current access state supports
- avoid inventing connectors or ingestion infrastructure that does not exist

If useful work can continue without full access, continue honestly.
If not, surface the blocker clearly.

## Fallback behavior

### If data is missing
- ask for the path, file, sample, or minimal description needed
- do not pretend inspection has already occurred

### If data is ambiguous
- ask for schema, sample, or target clarification
- state what remains uncertain

### If data is partially described
- proceed cautiously where planning or reasoning is still possible
- make assumptions visible
- avoid claiming dataset-level conclusions

### If only a conceptual dataset description exists
- support framing, workflow design, and methodological planning
- do not present unverified implementation as completed analysis

## Connector and access realism

This document does not define broad external connector support.

Do not assume:

- database access
- API access
- cloud mount access
- internet-backed retrieval
- enterprise connector availability

If such access is required, treat it as a runtime condition that must be confirmed explicitly.

Lack of external access is not automatically a structural failure of DATA_FORGE or MARS.

## Diagnostic rule

Before interpreting a data-access problem as a major system gap, check whether it is better explained by:

- missing file availability
- unclear project path
- absent sample/schema
- runtime environment limitation
- partial local setup
- blocked external access

Do not confuse access conditionality with architectural absence.

## Relationship to other shared docs

This document works together with:

- `data_access_patterns.md` for inspection and transformation discipline
- `tooling_assumptions.md` for environment assumptions
- preparation and modeling workflow docs when downstream work depends on confirmed inputs

## Non-goals

This document does not define:

- heavy ingestion logic
- database connector implementations
- API client behavior
- full ETL architecture
- automatic schema inference as a substitute for explicit validation

## Final rule

DATA_FORGE should treat data access as a runtime condition to be identified and made explicit.

If access is real, proceed with discipline.
If access is partial, proceed with caution.
If access is blocked, say so clearly.

Do not invent availability.
Do not fake inspection.
Do not escalate ordinary access limitations into fake architectural drama.
