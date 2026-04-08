# Validation Flow Review — Phase 1

**Agent**: solver-engineer
**Spec**: 037-validation-flow-fixes
**Date**: 2026-04-01
**Files reviewed**: validation.py, test_validation.py

---

## Executive Summary

The validation models are well-structured for solver integration. The ConstraintAddition model enables programmatic constraint passing to solvers. The SolverSolution model captures the standard solver output fields. One gap: the SolverSolution model lacks integration with actual solver output formats (AMPL, HiGHS).

---

## Findings

### F-1: ConstraintAddition for solver consumption [HIGH — H-4]

**Location**: validation.py:45-58
**Status**: IMPLEMENTED

The model is well-designed for downstream solver consumption:
- `constraint_type` enables dispatching to the correct solver constraint handler
- `expression` is the standard mathematical form
- `target_solver = "any"` allows generic or solver-specific constraints
- `parameters` dict handles solver-specific options

**AMPL integration concern**: AMPL constraints need specific syntax. The `expression` field allows free-form text, which works but is not validated. A future AMPL integration would need to parse `expression` into AMPL syntax. This is acceptable for now — the model is solver-agnostic.

**Verdict**: H-4 MET.

### F-2: SolverSolution model [HIGH — D-1]

**Location**: validation.py:65-79
**Status**: IMPLEMENTED

Fields cover the standard solver output:
- `objective_value`: The optimal value found
- `variable_assignments`: Decision variable values
- `solver_status`: Solver termination status (optimal, infeasible, timeout, etc.)
- `constraints_satisfied`: Which constraints the solution respects
- `solve_time_ms`: Performance metric

**Gap**: `solver_status` is a free-form `str`, not a constrained Literal. Standard statuses include "optimal", "infeasible", "unbounded", "timeout", "error". Making this a Literal would improve type safety.

**Priority**: P3 — works as-is, Literal would be better.

### F-3: Sensitivity framing [MEDIUM — D-4]

**Location**: validation.py:114-119
**Status**: CORRECT

The instructions say "reason about" not "compute." This is correct — the agent receives text, not numerical data. It can reason about which parameters are sensitive but cannot perform actual sensitivity analysis.

**Verdict**: D-4 MET.

### F-4: SolverSolution embedding in config [MEDIUM]

**Location**: validation.py:417-418
**Status**: IMPLEMENTED

```python
if solution is not None:
    config["solution"] = solution.model_dump()
```

When a SolverSolution is provided, its serialized form is embedded in the conversus config. Agents can reference concrete numbers instead of parsing files. Good UX.

### F-5: Phase 2/3 tracking [MEDIUM — NEW-10, NEW-11]

Phase 2 (CLI command `conversus validate`) and Phase 3 (AMPL/HiGHS integrations) are documented in docstrings but not as separate specs or tracking issues. For spec compliance, docstring tracking is sufficient. For project management, these should be separate specs.

**Verdict**: Tracked, not implemented (by design — these are future phases).

---

## Solver Integration Readiness

| Solver | Model Support | Gap |
|---|---|---|
| Generic | Full — SolverSolution model works for any solver | -- |
| AMPL | Partial — expression field needs syntax validation | Phase 3 |
| HiGHS | Partial — solver_status needs Literal mapping | Phase 3 |
