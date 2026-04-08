# Phase 1 Review: spec-compliance

**Spec**: 023-ampl-config-optimizer
**Reviewer**: spec-compliance
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: Verification of FR-001 through FR-012 and SC-001 through SC-004

---

## Executive Summary

Of 12 functional requirements, 10 are MET, 1 is PARTIALLY MET, and 1 requires runtime verification. Of 4 success criteria, 2 are MET, 1 is PARTIALLY MET, and 1 requires runtime verification. The implementation faithfully encodes the spec's MIP formulation and cost/quality models. The grid search fallback is preserved. The primary gap is FR-012: the optimality gap is hardcoded to 0.0 rather than extracted from HiGHS.

---

## Functional Requirements

### FR-001: Use AMPL/HiGHS when importable -- MET

HAS_AMPL flag gates the dispatch. When True, `solve_config()` routes to `_solve_with_ampl_fallback()`. Tests verify both dispatch paths.

### FR-002: Fall back to grid search -- MET

When HAS_AMPL is False, or when AMPL raises any exception, grid search runs. Tests `test_dispatch_to_grid_search_when_no_ampl`, `test_timeout_falls_back_to_grid_search`, and `test_runtime_error_falls_back` verify all fallback scenarios.

### FR-003: AMPL model encodes D007 cost formula exactly -- MET

The `_total_cost()` function in ampl_model.py implements the D007 formula. The test `test_cost_values_match_grid_search` verifies exact match at all grid points. The test `test_cost_values_with_arbiter` verifies the arbiter adds exactly `rounds` launches per config.

### FR-004: Quality model within 5% of heuristic -- MET (exceeds requirement)

The quality model uses the identical formula as grid search. The test `test_quality_scores_match_grid_search` verifies 0% error at all grid points. The requirement is "within 5%"; the implementation achieves 0%.

### FR-005: Handle infeasibility gracefully -- MET

AMPL returns None on infeasibility. The dispatch layer delegates to grid search for the detailed report. The test `test_ampl_infeasible_delegates_to_grid_search_report` verifies this. The grid search produces an infeasibility report with minimum-budget information.

### FR-006: Configurable timeout (default 10s) -- MET

The timeout is passed to HiGHS via `time_limit={timeout}`. The default is 10 seconds. The `solver_timeout` parameter on `solve_config()` is configurable.

### FR-007: Expose solve_ampl() for arbitrary problems -- MET

The `solve_ampl()` function in ampl_model.py provides the general-purpose API. It accepts model strings or file paths, arbitrary data parameters, and configurable solver selection.

### FR-008: Support MIP, LP, NLP, MINLP -- MET

The API does not restrict problem type. AMPL + solver handle type selection. HiGHS supports MIP and LP natively. NLP and MINLP require solver switching (e.g., to Ipopt), which the `solver` parameter enables.

### FR-009: Model files loadable from disk -- MET

The `solve_ampl()` function detects `.mod` file paths and uses `ampl.read()`. The test `test_solve_ampl_with_file_path` verifies this.

### FR-010: No AMPL license required -- MET

HiGHS is free (Apache 2.0). amplpy's Community Edition is free for models within size limits. The conversus config model (up to 135 variables) fits within the free tier.

### FR-011: solver field in PluginResult.data -- MET

`solver: "ampl-highs"` when AMPL solves, `solver: "grid-search"` for fallback. Tests verify both.

### FR-012: solve_time_ms and gap in result -- PARTIALLY MET

`solve_time_ms` is correctly measured via `time.monotonic()`. The `gap` is hardcoded to `0.0` in the dispatch layer:

```python
metadata = {"solver": "ampl-highs", "solve_time_ms": ..., "gap": 0.0}
```

FR-012 says the result "MUST include solve_time_ms and gap (optimality gap for MIP)." The gap should be extracted from HiGHS's actual solver output, not hardcoded. For the binary selection problem, 0.0 is always correct (HiGHS proves optimality trivially). But the hardcoding violates the letter of FR-012 and would be incorrect for the general-purpose API with non-trivial MIPs.

---

## Success Criteria

### SC-001: AMPL produces same optimal config as grid search -- NOT VERIFIED (runtime)

This requires running AMPL with amplpy/highspy installed. The tests use mocks. The mathematical equivalence is established (same quality and cost functions, same grid points), so the criterion should be met at runtime. But it cannot be verified from the test suite alone.

### SC-002: AMPL finds infeasibility faster than grid search -- NOT VERIFIED (runtime)

This is a performance criterion that requires timing both solvers on the same input. The test suite does not measure performance.

### SC-003: solve_ampl() solves a simple LP -- PARTIALLY MET

The mock test `test_solve_ampl_with_string_model` tests the API flow but does not actually solve an LP (the solver is mocked). A real integration test would require amplpy. The API design supports LP problems, but runtime verification is needed.

### SC-004: Without amplpy/highspy, identical to grid search -- MET

When HAS_AMPL is False, `solve_config()` calls grid search directly. Tests `test_dispatch_to_grid_search_when_no_ampl` and `test_grid_search_result_matches_direct_call` verify identical behavior and results.

---

## Compliance Matrix

| Requirement | Status | Evidence |
|------------|--------|----------|
| FR-001 | MET | HAS_AMPL flag, dispatch tests |
| FR-002 | MET | Fallback tests for missing dep, timeout, error |
| FR-003 | MET | Cost formula match at all grid points |
| FR-004 | MET | Quality formula exact match (0% error) |
| FR-005 | MET | Infeasibility delegation to grid search |
| FR-006 | MET | time_limit passed to HiGHS, configurable |
| FR-007 | MET | solve_ampl() function |
| FR-008 | MET | No problem type restriction |
| FR-009 | MET | .mod file detection and read |
| FR-010 | MET | HiGHS free, amplpy community edition |
| FR-011 | MET | solver field in metadata |
| FR-012 | PARTIALLY MET | gap hardcoded to 0.0 |
| SC-001 | NOT VERIFIED | Requires runtime with amplpy |
| SC-002 | NOT VERIFIED | Performance criterion, needs timing |
| SC-003 | PARTIALLY MET | Mock test only |
| SC-004 | MET | Grid search identity verified |

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Extract the actual optimality gap from HiGHS for FR-012 compliance. For the config optimizer this is 0.0, but the code should read it from the solver rather than hardcode it.

### P2 (Should Fix)

2. **P2-1**: Add `@pytest.mark.skipif(not HAS_AMPL)` runtime tests for SC-001 and SC-003 that run when amplpy is available.

3. **P2-2**: Verify the 4 constraints from spec Section 6:
   - No amplpy/highspy in core requirements.
   - No Plugin interface change.
   - No grid search breakage.
   - AMPL model readable/editable.

### P3 (Consider)

4. **P3-1**: Document the practical performance trade-off between MIP and grid search for the current search space.
