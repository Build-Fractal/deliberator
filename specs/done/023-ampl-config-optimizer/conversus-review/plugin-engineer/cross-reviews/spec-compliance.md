# Cross-Review of spec-compliance's Review

**Cross-reviewer**: plugin-engineer
**Reviewing**: spec-compliance's review of spec 023
**Date**: 2026-04-01

---

### Dangerous Contradictions

- **FR-001: amplpy-only check vs. spec's "amplpy AND highspy"**
  - **spec-compliance claims**: FR-001 is PASS, noting that "The spec says 'amplpy AND highspy are importable,' but the implementation only checks for amplpy. This is acceptable because highspy is a solver backend that AMPL discovers at solve time."
  - **plugin-engineer claims**: This is a compliance gap, not an acceptable deviation. The spec explicitly requires both packages to be importable. If `amplpy` is installed but `highspy` is not, the solver will fail at solve time with an opaque AMPL error rather than falling back to grid search. The `HAS_AMPL` flag should check for both: `try: import amplpy; import highspy; HAS_AMPL = True`. Alternatively, the solve path should catch solver-not-found errors and fall back.
  - **Why this is dangerous**: A user who installs `amplpy` without `highspy` gets a runtime error instead of a graceful fallback. The current `_solve_with_ampl_fallback` exception handler catches this, but the user sees a warning log about "AMPL solver failed" when the real problem is a missing dependency. The fallback works, but the diagnostic is poor.
  - **Suggested resolution**: Either check for both imports in the `HAS_AMPL` guard, or add a try/except in `solve_with_ampl` that catches solver-not-found errors and returns a descriptive `None` (or the proposed `SolveOutcome` with `status="solver_not_found"`). I prefer the import check: `try: from amplpy import AMPL; import highspy; HAS_AMPL = True`.

### Tensions

- **FR-004 PARTIAL PASS rating**
  - spec-compliance rates FR-004 as PARTIAL PASS. plugin-engineer's review did not evaluate FR-004 (it is a solver formulation concern, not a plugin concern). However, spec-compliance's analysis is thorough and the partial rating is appropriate from a compliance perspective. The tolerance is met; the technique differs. I have no objection to the rating.

- **Integration test recommendation scope**
  - spec-compliance recommends `@pytest.mark.skipunless(HAS_AMPL)` integration tests (Rec 5, P3). plugin-engineer agrees this is valuable but notes it introduces a CI dependency. The integration tests would only run on developer machines with amplpy installed, creating a testing gap in CI pipelines. A better approach: run integration tests in a separate CI job that installs amplpy/highspy, similar to how database-dependent tests use a separate service container.
  - Regardless of CI strategy, the recommendation is sound. The mock tests cannot catch AMPL model syntax errors.

- **Compliance table completeness**
  - spec-compliance's table is well-structured but does not cover Section 6 constraints as line items. The Section 6 constraints ("Must NOT add to core requirements," "Must NOT change Plugin interface," "Must NOT break grid search," "AMPL model as .mod file," "HiGHS as default") are separate from FRs. The `.mod` file constraint is flagged under FR-009, and the others are covered implicitly, but a dedicated Section 6 compliance check would be more rigorous.

### Safe Agreements

- **FR-002, FR-003, FR-005, FR-006, FR-007, FR-010, FR-011 are fully compliant**: plugin-engineer's review implicitly validates these through the dispatch and API analysis. spec-compliance's explicit per-requirement verification confirms them.

- **SC-001 is the strongest success criterion**: Both reviews agree the enumeration approach guarantees SC-001 by construction. plugin-engineer notes the quality/cost consistency tests; spec-compliance notes the same tests under SC-001 analysis.

- **SC-004 is fully satisfied**: Both reviews confirm grid search behavior is unchanged when AMPL is unavailable. plugin-engineer's backward compatibility analysis and spec-compliance's SC-004 assessment converge.

- **Gap hardcode is a real issue**: spec-compliance notes it as a "caveat" under FR-012. plugin-engineer did not flag it but accepts solver-engineer's P2 finding on this point. The three reviews converge: the gap should be extracted from the solver, not hardcoded.

- **Config model `.mod` file**: spec-compliance flags the Section 6 violation under FR-009. plugin-engineer did not independently flag this but accepts it. Three-way convergence on this recommendation.

- **Test coverage is appropriate for the optional dependency**: spec-compliance notes that all AMPL tests use mocks and rates this as acceptable given the optional dependency. plugin-engineer agrees. The test design correctly isolates the testable logic (dispatch, data generation, result extraction) from the untestable dependency (actual AMPL solver).
