# spec-compliance Cross-Review of optimization-engineer

**Cross-reviewer**: spec-compliance
**Reviewing**: optimization-engineer Phase 1 review of spec 023
**Date**: 2026-04-01

---

## Agreements

### 1. MIP formulation is correct

optimization-engineer's analysis of the binary selection model, the equivalence to grid search, and the cost/quality formula verification is thorough. The mathematical proof that the formulation is correct is convincing.

### 2. Infeasibility handling is correct

The two-stage approach (AMPL presolve detects, grid search reports) is correctly analyzed. optimization-engineer's assessment that AMPL detects infeasibility quickly (presolve) while grid search provides the human-readable report is accurate.

### 3. General-purpose API is well-designed

The file/string model detection, parameter passing, and AMPL lifecycle management are correctly reviewed.

---

## Tensions

### 1. MIP-vs-grid-search performance documentation priority

optimization-engineer marks this as P1. From a compliance perspective, the spec does not require the AMPL solver to be faster than grid search. The spec requires that AMPL be used when available (FR-001) and that grid search be the fallback (FR-002). Whether AMPL is faster is a quality-of-implementation concern, not a compliance concern.

I would classify performance documentation as P3. Users do not choose between AMPL and grid search (the dispatch layer chooses automatically), so the performance trade-off is an internal implementation detail.

### 2. Model readability constraint

optimization-engineer does not address the constraint "The AMPL model must be readable/editable by users (stored as .mod file, not generated code)." The model IS generated code (a Python string constant). It is not stored as a .mod file. optimization-engineer's cross-review of me raises this, but the original review does not.

From a compliance perspective, this is a constraint violation. The model is readable (well-formatted AMPL syntax) but is not stored as a .mod file. The fix is straightforward: add a function to write the model to disk, or store it as a .mod file and read it at runtime.

---

## Missed Opportunities

### 1. No assessment of the piecewise-linear claim

The spec says the quality model is "a piecewise linear approximation of the heuristic quality curves." optimization-engineer correctly notes that the implementation uses grid-point lookup (not a piecewise-linear approximation), achieving exact match. But the spec's claim that the model uses "piecewise linear approximation" is technically inaccurate for the implemented approach. The AMPL model uses binary selection over grid points, which is a different mathematical structure than piecewise-linear interpolation.

This is a spec-implementation mismatch: the spec describes one approach, the implementation uses a better one. Like FR-001 in spec 022 (scipy vs. pure Python), the implementation exceeds the spec. The spec should be amended.

### 2. No analysis of the AMPL model's extensibility

optimization-engineer mentions that the MIP formulation enables extensibility (new constraints, continuous variables) but does not provide concrete examples. This is relevant because the spec says the "AMPL optimizer also enables a general-purpose optimization API." The extensibility argument is the main justification for the MIP approach over grid search. Concrete examples would strengthen this argument.
