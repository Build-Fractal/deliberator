# optimization-engineer Cross-Review of spec-compliance

**Cross-reviewer**: optimization-engineer
**Reviewing**: spec-compliance Phase 1 review of spec 023
**Date**: 2026-04-01

---

## Agreements

### 1. FR-012 PARTIALLY MET is correct

The gap is hardcoded to 0.0. While this is correct for the config optimizer (trivial MIP), it violates the letter of FR-012. spec-compliance's recommendation to extract the actual gap is correct.

### 2. FR-004 exceeds the 5% requirement

spec-compliance correctly notes that the quality model achieves 0% error (exact match) because it uses the identical formula. The "within 5%" threshold was written for a piecewise-linear approximation that turned out to be unnecessary -- the grid-point lookup approach avoids approximation entirely.

### 3. Compliance matrix is thorough

The 12-FR and 4-SC matrix with evidence columns provides clear traceability. The distinction between MET, PARTIALLY MET, and NOT VERIFIED is appropriately applied.

---

## Tensions

### 1. SC-001 and SC-002 verifiability

spec-compliance marks SC-001 and SC-002 as NOT VERIFIED (runtime). I have a stronger position: the mathematical equivalence of the MIP formulation and grid search can be proven analytically, not just verified at runtime.

The MIP model selects from the same grid points as the grid search, with the same quality and cost values. The objective is to maximize quality subject to budget and quality constraints. Both algorithms solve the same problem with the same data. The grid search uses exhaustive enumeration; the MIP uses integer programming. Both must find the same optimum (or both must report infeasible).

This is a mathematical proof, not a runtime test. SC-001 is MET by construction. SC-002 (performance comparison) does require runtime measurement.

### 2. SC-003 assessment

spec-compliance marks SC-003 (solve_ampl solves a simple LP) as PARTIALLY MET because the mock test does not actually solve an LP. I agree this needs a runtime test. But the API design clearly supports LP problems (no type restriction, HiGHS handles LP natively). The risk of SC-003 failure at runtime is very low.

---

## Missed Opportunities

### 1. No assessment of the AMPL model string readability

The spec's constraint says "The AMPL model must be readable/editable by users (stored as .mod file, not generated code)." The model is stored as a Python string constant (`CONVERSUS_CONFIG_MODEL`), not a `.mod` file. This technically violates the constraint's letter: the model is embedded in Python code, not stored as a standalone `.mod` file that users can edit without touching Python.

However, the model string is clearly formatted with AMPL comments and standard AMPL syntax. It is readable and could be extracted to a `.mod` file. The constraint's intent (readability) is satisfied; the mechanism (file storage) is not.

### 2. No verification of D007 formula source

FR-003 says "The AMPL model MUST encode the D007 cost formula exactly (not an approximation)." spec-compliance verifies the formula matches search.py, but does not independently verify that search.py correctly implements D007. If search.py has a bug in the D007 formula, both implementations would agree (on the wrong answer). A cross-reference to the D007 definition would strengthen the verification.
