# Phase 3 Revision: plugin-engineer

**Agent**: plugin-engineer
**Spec**: 023-ampl-config-optimizer
**Date**: 2026-04-01
**Inputs**: optimization-engineer cross-review, spec-compliance cross-review

---

## Disposition of Original Recommendations

### P1-1. Check highspy in HAS_AMPL flag -- MAINTAINED

**Original**: Import both amplpy and highspy in the HAS_AMPL check.

**Cross-review support**: optimization-engineer agrees and adopts as N-1. spec-compliance agrees this is the most impactful finding.

**Priority**: Remains P1.

---

### P1-2. Extract actual optimality gap -- MAINTAINED

**Original**: Read gap from HiGHS rather than hardcoding 0.0.

**Cross-review response**: optimization-engineer provides a nuanced analysis: P1 for general-purpose API, P2 for dispatch layer. I accept the split but maintain overall P1 because FR-012 applies to the dispatch layer.

**Priority**: Remains P1.

---

### P2-1. Clarify infeasibility metadata -- MAINTAINED

**Original**: Add `report_generated_by: "grid-search"` to infeasibility metadata.

**Cross-review support**: optimization-engineer supports as P2. spec-compliance supports.

**Priority**: Remains P2.

---

### P2-2. Python-level timeout wrapper -- MODIFIED

**Original**: Add a threading-based timeout around the AMPL solve call.

**Cross-review response (spec-compliance T-1)**: FR-006 says "solver execution" which is bounded by HiGHS time_limit. Model parsing is not "solver execution."

**Revised position**: I accept that FR-006 is met by HiGHS time_limit. The Python-level timeout is a defense-in-depth improvement for the general-purpose API, not a compliance requirement.

**Priority**: Downgraded to P3 (general-purpose API improvement).

---

### P3-1. Document AMPL Community Edition limits -- WITHDRAWN

**Cross-review response (optimization-engineer T-2)**: FR-010 explicitly addresses licensing. The amplpy Community Edition is free for all supported model sizes.

**Revised position**: I withdraw this recommendation. The spec already addresses it.

---

## New Recommendations from Cross-Reviews

### N-1. Wrap AMPL parse errors in user-friendly exceptions (from optimization-engineer cross-review discussion)

Add error wrapping to `solve_ampl()`:

```python
try:
    ampl.eval(model)
except Exception as e:
    raise ValueError(f"AMPL model parse error: {e}") from e
```

**Priority**: P2 (usability improvement for general-purpose API).

---

### N-2. Add write_config_model() helper (from plugin-engineer cross-review of optimization-engineer)

Provide a function to export the built-in AMPL model to a .mod file for user inspection and modification.

**Priority**: P2 (satisfies the .mod file constraint and improves usability).

---

### N-3. Note AMPLSolverResult is unused (from spec-compliance MO-1)

The `AMPLSolverResult` dataclass in ampl_solver.py is defined but never instantiated. It is either dead code or a forward declaration. If it is a forward declaration, add a docstring noting this. If it is dead code, remove it.

**Priority**: P3 (code hygiene).
