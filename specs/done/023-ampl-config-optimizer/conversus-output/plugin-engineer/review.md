# Phase 1 Review: plugin-engineer

**Spec**: 023-ampl-config-optimizer
**Reviewer**: plugin-engineer
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: AMPL dispatch, HAS_AMPL flag, general-purpose solve_ampl() API, timeout/fallback

---

## Executive Summary

The AMPL optimizer integration follows the established optional-dependency pattern (HAS_AMPL flag, dispatch to grid search fallback). The solver dispatch layer (ampl_solver.py) provides clean separation between the MIP backend and the grid search fallback. The general-purpose `solve_ampl()` API is well-designed with file/string model support and proper AMPL instance lifecycle management. The `solver` field in PluginResult.data correctly identifies the backend. However, there are three concerns: (1) the timeout mechanism uses HiGHS's `time_limit` option rather than a Python-level timeout, which means solver startup/teardown time is not bounded, (2) the HAS_AMPL flag checks only `amplpy` import, not `highspy`, even though the spec lists both as dependencies, and (3) the infeasibility delegation from AMPL to grid search preserves the `solver: "ampl-highs"` metadata even though the result came from grid search.

---

## HAS_AMPL Flag

### Design

```python
try:
    from amplpy import AMPL
    HAS_AMPL = True
except ImportError:
    HAS_AMPL = False
```

This checks only `amplpy`, not `highspy`. The spec lists both `amplpy` and `highspy` as dependencies. If `amplpy` is installed but `highspy` is not, HAS_AMPL is True but the solver will fail at runtime when it tries to use HiGHS.

### Concern

Unlike the nashopt flag (which couples nashopt + numpy), the AMPL flag does not check the solver backend. The `solve_with_ampl()` function sets `solver="highs"`, which requires `highspy`. If highspy is missing, AMPL will report a solver error, which the dispatch layer catches and falls back to grid search. This is correct behavior (the fallback catches the error), but the HAS_AMPL flag is misleading -- it reports True when the solver is not actually available.

A more accurate check would be:

```python
try:
    from amplpy import AMPL
    import highspy  # noqa: F401
    HAS_AMPL = True
except ImportError:
    HAS_AMPL = False
```

---

## Dispatch Layer (ampl_solver.py)

### Architecture

The `solve_config()` function dispatches based on HAS_AMPL:
1. If True: `_solve_with_ampl_fallback()` -- try AMPL, fall back to grid search on any error.
2. If False: direct grid search.

The AMPL fallback has three outcomes:
- AMPL solves optimally: return OptimalConfig with `solver: "ampl-highs"`.
- AMPL reports infeasible: delegate to grid search for detailed report, keep `solver: "ampl-highs"`.
- AMPL raises exception: fall back to grid search with `ampl_fallback: True`.

### Concern: Infeasibility Metadata

When AMPL reports infeasible and the result is delegated to grid search, the metadata says `solver: "ampl-highs"`. This is misleading -- the OptimalConfig came from grid search, not AMPL. The metadata should indicate that AMPL detected infeasibility but the report came from grid search. Something like:

```python
metadata = {
    "solver": "ampl-highs",
    "infeasibility_detected_by": "ampl-highs",
    "report_generated_by": "grid-search",
}
```

---

## Timeout (FR-006)

The timeout is implemented via HiGHS's `time_limit` option:

```python
ampl.set_option(f"{solver}_options", f"time_limit={timeout}")
```

This bounds the solver's computation time but not:
- AMPL model parsing time.
- AMPL-to-HiGHS translation time.
- Python object construction time.

For the current model size (up to 135 binary variables), parsing and translation are fast. But for the general-purpose API with large user-supplied models, parsing could be slow. A Python-level timeout (e.g., `signal.alarm` or `threading.Timer`) would provide a hard bound on total execution time.

The default timeout is 10 seconds (spec says "default 10s"). The test verifies that timeout falls back to grid search.

---

## General-Purpose API (FR-007 through FR-010)

### solve_ampl() Function

The API supports:
- **String models**: `ampl.eval(model)` -- correct.
- **File models**: `ampl.read(model.strip())` -- correct (FR-009).
- **Scalar parameters**: `param.set(value)` -- correct.
- **Indexed parameters**: `param.set_values(value)` -- correct.
- **Multiple problem types**: FR-008 says MIP, LP, NLP, MINLP. The API does not restrict problem type -- it passes the model to AMPL, which delegates to the solver. HiGHS handles MIP and LP. NLP and MINLP require different solvers (e.g., Ipopt, Bonmin). The API supports solver switching via the `solver` parameter.

### FR-010: No AMPL License Required

HiGHS is free (Apache 2.0). The AMPL Community Edition (amplpy) is also free for small models. For the conversus config model (up to 135 variables), the free tier is sufficient. The general-purpose API does not enforce model size limits, so users with large models would need a commercial AMPL license. This should be documented.

---

## FR-011, FR-012: Output Fields

FR-011 requires `solver: "ampl-highs"` or `solver: "grid-search"` in PluginResult.data. FR-012 requires `solve_time_ms` and `gap` when AMPL solves.

The dispatch layer sets these in the metadata dict:
- `solver: "ampl-highs"` with `solve_time_ms` and `gap: 0.0` for optimal solutions.
- `solver: "grid-search"` for fallback.
- `solver: "ampl-highs"` with `gap: None` for infeasible (delegated to grid search).

The `gap: 0.0` for optimal solutions assumes HiGHS proves optimality. For the binary selection problem (trivial MIP), this is always the case. For general-purpose models, the gap should be extracted from HiGHS's actual gap report, not hardcoded.

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Check both amplpy and highspy in the HAS_AMPL flag. If highspy is missing, HAS_AMPL should be False (or the flag should be renamed to indicate partial availability).

2. **P1-2**: Extract the actual optimality gap from HiGHS for the metadata, rather than hardcoding 0.0. For the config optimizer this is always 0.0, but for the general-purpose API it may not be.

### P2 (Should Fix)

3. **P2-1**: Clarify infeasibility metadata to indicate that the report came from grid search, not AMPL.

4. **P2-2**: Add a Python-level timeout wrapper around the AMPL solve call (in addition to the HiGHS time_limit) to bound total execution time including model parsing.

### P3 (Consider)

5. **P3-1**: Document AMPL Community Edition model size limits and the need for a commercial license for large models.
