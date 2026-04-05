# PREPARATION GUIDELINES

## Purpose
Define how data preparation and transformation should be approached across the DS runtime.

## Core principle
Preparation is not a single step.
It is a staged, explicit, and reversible process.

## Standard phases

### 1. Raw inspection
- understand structure
- identify missing values
- identify data types
- detect obvious anomalies

### 2. Cleaning
- handle missing values
- fix incorrect types
- remove or flag anomalies
- do not mix with feature engineering

### 3. Feature engineering
- create derived variables
- encode categories
- scale or normalize if needed
- document transformations

### 4. Dataset finalization
- define final feature set
- define target variable
- ensure reproducibility

## Separation rules
- do not mix cleaning and feature engineering blindly
- do not jump directly to modeling-ready dataset
- keep transformations traceable

## Output expectation
Preparation should produce:
- a clean dataset
- a transformation description
- optionally: reusable code blocks

## Anti-patterns
- monolithic preprocessing
- silent transformations
- irreversible steps without documentation
