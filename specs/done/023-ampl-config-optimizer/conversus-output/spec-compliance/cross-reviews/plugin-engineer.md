# spec-compliance Cross-Review of plugin-engineer

**Cross-reviewer**: spec-compliance
**Reviewing**: plugin-engineer Phase 1 review of spec 023
**Date**: 2026-04-01

---

## Agreements

### 1. HAS_AMPL should check highspy

plugin-engineer's P1-1 is the most impactful finding. All three reviewers should converge on this. The HAS_AMPL flag reports True when only amplpy is installed, but the solver requires highspy. This creates a false-positive dispatch that will fail at runtime and fall back to grid search (correct but unnecessary overhead and misleading logging).

### 2. Infeasibility metadata is misleading

The `solver: "ampl-highs"` metadata on grid-search-generated results is confusing. plugin-engineer's suggestion to differentiate `infeasibility_detected_by` and `report_generated_by` is clean. I support this as P2.

### 3. FR-011 and FR-012 assessment is correct

The solver field and solve_time_ms are correctly classified. The gap hardcoding is the top finding.

---

## Tensions

### 1. Timeout mechanism adequacy

plugin-engineer recommends a Python-level timeout wrapper (P2-2) in addition to HiGHS's time_limit. From a compliance perspective, FR-006 says "Solver execution MUST be capped at a configurable timeout." The HiGHS time_limit caps solver execution. Model parsing and Python object construction are not "solver execution" under a strict reading of FR-006.

plugin-engineer's concern is valid for the general-purpose API (large models could have long parse times), but for FR-006 compliance, the HiGHS time_limit is sufficient.

### 2. AMPL Community Edition licensing

plugin-engineer raises licensing as P3-1. I agree with optimization-engineer's counterargument: FR-010 explicitly says "The API MUST NOT require AMPL license -- HiGHS is free." The amplpy Community Edition is free. Documenting this is informational, not a compliance requirement.

---

## Missed Opportunities

### 1. No assessment of ampl_solver.py's AMPLSolverResult

plugin-engineer reviews the dispatch layer but does not note that `AMPLSolverResult` is defined but never instantiated. The dataclass exists in ampl_solver.py with fields for solve_time_ms, gap, and solver_status, but the `solve_config()` function returns `(OptimalConfig, dict)` instead. This is either dead code or a forward declaration for future use. From a compliance perspective, it is harmless but should be noted.

### 2. No discussion of the solver name convention

FR-011 requires `solver: "ampl-highs"` or `solver: "grid-search"`. The implementation uses these exact strings. But if a user changes the solver (e.g., `solver="gurobi"` in the general-purpose API), the dispatch layer still reports `"ampl-highs"`. The convention should be `"ampl-{solver_name}"` to accurately reflect the backend.

This is a minor extensibility concern that does not affect current compliance.
