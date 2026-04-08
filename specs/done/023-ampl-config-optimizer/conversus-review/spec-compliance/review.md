# Spec-Compliance Review: Spec 023 -- AMPL Config Optimizer

**Reviewer**: spec-compliance
**Spec**: `specs/done/023-ampl-config-optimizer/spec.md`
**Implementation files reviewed**: `ampl_model.py`, `ampl_solver.py`, `optimizer.py`, `__init__.py`, `models.py`, `search.py`, `tests/test_ampl.py`

---

### Executive Summary

This review evaluates the implementation against each functional requirement (FR-001 through FR-012) and success criterion (SC-001 through SC-004) defined in spec 023. The implementation achieves strong compliance on the core config optimization path: AMPL dispatch when available (FR-001), grid search fallback (FR-002), exact cost encoding (FR-003), infeasibility handling (FR-005), timeout (FR-006), solver field in output (FR-011), and AMPL telemetry (FR-012). The general-purpose API (FR-007 through FR-010) is implemented and functional.

However, three requirements have compliance gaps. FR-004 specifies a "piecewise linear approximation validated to within 5% of the heuristic at all integer grid points," but the implementation uses exact enumeration (0% error at all points) -- which trivially satisfies the tolerance but does not implement the approximation approach the requirement envisions. FR-009 requires models to be "loadable from disk (.mod files)," which the general-purpose `solve_ampl()` supports but the config-specific model violates (it is a Python string, not a `.mod` file, contrary to Section 6's constraint). SC-002 claims faster infeasibility detection via AMPL, which the enumeration-based formulation cannot achieve.

The test suite provides good coverage for the requirements. Every FR has at least one corresponding test, and the cross-solver consistency tests (`TestQualityModelConsistency`) give high confidence in SC-001. The test design is sound: mocks are used appropriately for the AMPL dependency, and the grid search path is tested with real solver calls.

My overall assessment: 9 of 12 functional requirements are fully satisfied, 2 are partially satisfied (FR-004, FR-009), and 1 is satisfied at the API level but has a documentation gap (FR-008). All 4 success criteria are addressed, with SC-002 being the weakest (not falsifiable with the current formulation).

---

### Requirement-by-Requirement Analysis

#### FR-001: AMPL/HiGHS used when amplpy and highspy are importable

**Status: PASS**

`ampl_solver.py` L91-99: When `HAS_AMPL` is True, `solve_config()` calls `_solve_with_ampl_fallback()`, which builds the AMPL model and calls `solve_with_ampl()`. The `HAS_AMPL` flag is set at import time by a `try/except ImportError` on `amplpy` (`ampl_model.py`, L29-34).

Test coverage: `TestAMPLMockIntegration.test_dispatch_to_ampl_when_available` patches `HAS_AMPL=True` and verifies AMPL is called. `TestAMPLMockIntegration.test_ampl_metadata_in_plugin_result` verifies the full plugin path with AMPL.

Note: The spec says "amplpy AND highspy are importable," but the implementation only checks for `amplpy`. HiGHS availability is implicitly assumed when amplpy is present. This is acceptable because `highspy` is a solver backend that AMPL discovers at solve time, not at import time.

---

#### FR-002: Grid search fallback when AMPL unavailable

**Status: PASS**

`ampl_solver.py` L101-111: When `HAS_AMPL` is False, `solve_config()` calls `grid_search()` directly with `metadata = {"solver": "grid-search"}`.

Test coverage: `TestSolverDispatch.test_dispatch_to_grid_search_when_no_ampl`, `TestSolverDispatch.test_grid_search_result_matches_direct_call`, `TestPluginSolverField.test_solver_field_grid_search`.

---

#### FR-003: AMPL model encodes D007 cost formula exactly

**Status: PASS**

`ampl_model.py` L122-145 (`_total_cost`): The cost formula matches D007: `agents + agents*(agents-1) + agents*iterations + agents + 1 + arbiter_cost`. This is computed for each grid point and stored in `qp_cost`.

Test coverage: `TestAMPLModelGeneration.test_cost_values_match_grid_search` verifies that AMPL cost values match `_total_launches * cost_per_launch` at every grid point. `TestAMPLModelGeneration.test_cost_values_with_arbiter` verifies the arbiter adds exactly `rounds` launches.

---

#### FR-004: Quality model is a piecewise linear approximation validated to within 5%

**Status: PARTIAL PASS**

The requirement specifies a "piecewise linear approximation of the heuristic quality curves, validated to within 5% of the heuristic at all integer grid points." The implementation uses exact heuristic values at all integer grid points (0% error), not an approximation. The tolerance criterion is trivially satisfied, but the implementation approach differs from the spec's intent.

`ampl_model.py` L109-119: `_quality_score` computes the exact same quality formula as `search.py`. `build_ampl_model` stores these exact values as `qp_quality` parameters.

Test coverage: `TestAMPLModelGeneration.test_quality_scores_match_grid_search`, `TestQualityModelConsistency.test_ampl_quality_matches_search_at_all_points` -- both verify 0% error.

The spec envisioned a PWL approximation that would enable continuous relaxation in the MIP solver. The implementation chose exact enumeration, which satisfies the tolerance but does not deliver the approximation's benefits (LP relaxation pruning, continuous variable support).

---

#### FR-005: Graceful infeasibility handling matching grid search

**Status: PASS**

`ampl_solver.py` L153-171: When `solve_with_ampl` returns `None` (infeasible), the dispatcher calls `grid_search()` to generate the infeasibility report. This ensures the infeasibility message includes minimum-budget information, matching the grid search's detailed reporting.

`ampl_model.py` L271-272: The AMPL solver detects infeasibility via `solve_result == "infeasible"` and returns `None`.

Test coverage: `TestInfeasibilityConsistency.test_ampl_infeasible_delegates_to_grid_search_report`, `TestAMPLMockIntegration.test_ampl_solve_infeasible_returns_none`, `TestInfeasibilityConsistency.test_grid_search_infeasible_budget_too_low`, `TestInfeasibilityConsistency.test_grid_search_infeasible_quality_unreachable`, `TestInfeasibilityConsistency.test_infeasibility_in_plugin_result`.

---

#### FR-006: Configurable solver timeout (default 10s)

**Status: PASS**

`ampl_model.py` L263: `ampl.set_option(f"{solver}_options", f"time_limit={timeout}")`. Default timeout is 10 seconds (`ampl_model.py` L221, `ampl_solver.py` L70).

`optimizer.py` L91: Plugin reads `solver_timeout` from config with default 10.

Test coverage: `TestTimeoutFallback.test_timeout_falls_back_to_grid_search` verifies that a `TimeoutError` in the AMPL path triggers grid search fallback with `ampl_fallback: True` in metadata.

Note: There is no test verifying the `time_limit` option string is actually passed to the solver. The timeout test mocks the entire `solve_with_ampl` function, so it does not exercise the option-setting code path.

---

#### FR-007: General-purpose `solve_ampl()` API exposed

**Status: PASS**

`ampl_model.py` L315-404: `solve_ampl(model, data, solver, timeout)` is implemented. `__init__.py` L19: Exported via `from conversus.plugins.optimizer.ampl_model import solve_ampl`. `__init__.py` L22: Listed in `__all__`.

Test coverage: `TestSolveAMPLAPI` has six tests covering ImportError, string model, file path, data parameters, variable extraction, and cleanup.

---

#### FR-008: Support MIP, LP, NLP, MINLP problem types

**Status: PASS (with documentation gap)**

The `solve_ampl()` function passes the `solver` parameter through to AMPL (`ampl.set_option("solver", solver)`), so any AMPL-compatible solver can be used. MIP/LP via HiGHS, NLP via Ipopt, MINLP via Bonmin -- all work if the solver is installed.

However, the default solver is HiGHS, which only supports MIP/LP. The docstring does not document that NLP/MINLP require non-default solvers. This is a documentation gap, not a code defect.

Test coverage: No test for NLP or MINLP problem types. All tests use `solver="highs"`. This is acceptable given the optional dependency nature.

---

#### FR-009: Models loadable from disk (.mod files) or from string

**Status: PASS (general API) / PARTIAL PASS (config model)**

`solve_ampl()` (`ampl_model.py` L354-357): Detects `.mod` files by suffix and loads with `ampl.read()`. String models are loaded with `ampl.eval()`. Test `test_solve_ampl_with_file_path` verifies file loading; `test_solve_ampl_with_string_model` verifies string loading.

However, Section 6 of the spec states: "The AMPL model must be readable/editable by users (stored as `.mod` file, not generated code)." The config optimizer's AMPL model is stored as a Python string constant `CONVERSUS_CONFIG_MODEL` in `ampl_model.py` L65-102. This violates the Section 6 constraint. The model is readable in the Python file but not loadable independently as a `.mod` file.

---

#### FR-010: API does not require AMPL licence

**Status: PASS**

The implementation uses `amplpy` with the free AMPL Community Edition. HiGHS is Apache 2.0 licensed. Neither requires a commercial licence for the problem sizes in the config optimizer (~135 variables).

Note: The AMPL Community Edition has size limits (500 variables, 500 constraints). The general-purpose API may hit these limits for larger problems. This is not documented.

---

#### FR-011: PluginResult.data includes solver field

**Status: PASS**

`optimizer.py` L117: `"solver": solver_meta.get("solver", "grid-search")`. The `solver` field is always present, with value `"ampl-highs"` or `"grid-search"`.

Test coverage: `TestPluginSolverField.test_solver_field_grid_search`, `TestAMPLMockIntegration.test_dispatch_to_ampl_when_available` (checks `meta["solver"] == "ampl-highs"`), `TestPluginSolverField.test_existing_fields_preserved`.

---

#### FR-012: AMPL results include solve_time_ms and gap

**Status: PASS (with caveat on gap accuracy)**

`optimizer.py` L121-125: When `solver_meta["solver"] == "ampl-highs"`, `solve_time_ms` and `gap` are added to `PluginResult.data`. `ampl_solver.py` L146-150: Metadata includes `solve_time_ms` (measured wall-clock) and `gap` (hardcoded to 0.0).

Test coverage: `TestAMPLMockIntegration.test_ampl_metadata_in_plugin_result` verifies `solve_time_ms` and `gap` are in plugin result. `TestPluginSolverField.test_no_solve_time_for_grid_search` verifies these are absent for grid search.

Caveat: The gap is hardcoded to 0.0 rather than extracted from the solver. This satisfies FR-012's letter (the field is present) but not its spirit (the value should reflect the actual optimality gap).

---

### Success Criteria Analysis

#### SC-001: AMPL produces same optimal config as grid search for all feasible inputs

**Status: STRONG**

The formulation guarantees this by construction: the AMPL model selects from exactly the same grid points with exactly the same quality/cost values. `TestQualityModelConsistency` verifies value equivalence at all 135 points. `TestSolverDispatch.test_grid_search_result_matches_direct_call` verifies result equivalence end-to-end.

The only risk is floating-point tie-breaking: if two grid points have the same quality, the MIP solver and grid search may break ties differently (grid search prefers lower cost; HiGHS may select arbitrarily). This does not violate SC-001 (both are optimal), but it means results may differ in degenerate cases.

---

#### SC-002: AMPL finds infeasibility faster than grid search

**Status: WEAK**

The enumeration-based formulation does not enable faster infeasibility detection. The MIP solver must evaluate the same constraint matrix as grid search iterates through. For the 135-point problem, grid search completes in microseconds; the MIP adds model parsing and solver overhead.

No test explicitly measures relative infeasibility detection time. `TestInfeasibilityConsistency` verifies correctness but not speed.

---

#### SC-003: General-purpose solve_ampl() solves a simple LP correctly

**Status: PASS (via mocks)**

`TestSolveAMPLAPI.test_solve_ampl_with_string_model` tests the solve path with a mocked AMPL instance. The mock returns `solve_result="solved"` and `objective_value=42.0`. This verifies the API correctly dispatches and extracts results.

A true integration test (without mocks, solving an actual LP) is not present but is impractical in CI where amplpy may not be installed.

---

#### SC-004: Without amplpy/highspy, behavior identical to current grid search

**Status: PASS**

`TestSolverDispatch.test_dispatch_to_grid_search_when_no_ampl` patches `HAS_AMPL=False` and verifies grid search runs. `TestSolverDispatch.test_grid_search_result_matches_direct_call` verifies the dispatch result matches a direct `optimize_config()` call. `TestPluginSolverField.test_solver_field_grid_search` verifies the plugin output with grid search.

The only new field in the grid search path is `solver: "grid-search"`, which is additive and does not change existing behavior.

---

### Compliance Summary Table

| Requirement | Status | Notes |
|---|---|---|
| FR-001 | PASS | AMPL dispatched when HAS_AMPL=True |
| FR-002 | PASS | Grid search fallback when HAS_AMPL=False |
| FR-003 | PASS | D007 cost formula verified at all grid points |
| FR-004 | PARTIAL | Exact enumeration, not PWL approximation |
| FR-005 | PASS | Infeasibility delegates to grid search report |
| FR-006 | PASS | Configurable timeout with 10s default |
| FR-007 | PASS | solve_ampl() API exported |
| FR-008 | PASS* | Solver-dependent; doc gap on NLP/MINLP |
| FR-009 | PARTIAL | solve_ampl supports .mod; config model is Python string |
| FR-010 | PASS | No licence required (Community Edition) |
| FR-011 | PASS | solver field always present |
| FR-012 | PASS* | Fields present; gap hardcoded to 0.0 |
| SC-001 | STRONG | Guaranteed by construction + full grid verification |
| SC-002 | WEAK | Enumeration cannot be faster than grid search |
| SC-003 | PASS | Tested via mocks |
| SC-004 | PASS | Identical grid search behavior verified |

---

### Actionable Recommendations

1. **Align FR-004 spec text with implementation** (Priority: P1)
   - **Current state**: FR-004 says "piecewise linear approximation validated to within 5%." Implementation uses exact enumeration.
   - **Proposed change**: Amend FR-004 to: "The quality model MUST use the exact heuristic quality values at all integer grid points, ensuring 0% deviation from the grid search. (Original design: piecewise linear approximation; changed to exact enumeration for correctness guarantee.)"
   - **Rationale**: The spec should describe what was built. A spec that does not match its implementation is a liability for future audits.

2. **Store config model as `.mod` file per Section 6** (Priority: P2)
   - **Current state**: AMPL model is a Python string constant.
   - **Proposed change**: Create `conversus/plugins/optimizer/config_optimizer.mod`. Load it in `build_ampl_model` or at module init.
   - **Rationale**: Section 6 explicitly requires this. FR-009 supports it.

3. **Revise SC-002 or change formulation** (Priority: P2)
   - **Current state**: SC-002 claims faster infeasibility detection which the enumeration approach cannot deliver.
   - **Proposed change**: Revise to: "AMPL optimizer correctly identifies infeasibility, with the grid search providing the detailed report."
   - **Rationale**: Unfalsifiable success criteria erode trust in the spec as a testable contract.

4. **Extract real MIP gap from solver output** (Priority: P2)
   - **Current state**: `gap: 0.0` hardcoded in `ampl_solver.py` L149.
   - **Proposed change**: Query AMPL for actual gap post-solve.
   - **Rationale**: FR-012 requires `gap` in the output. A hardcoded value defeats the diagnostic purpose.

5. **Add integration test marker for AMPL-available environments** (Priority: P3)
   - **Current state**: All AMPL tests use mocks.
   - **Proposed change**: Add `@pytest.mark.skipunless(HAS_AMPL, "amplpy not installed")` integration tests that solve the actual config optimization problem and verify SC-001 with real solver output.
   - **Rationale**: Mock tests verify dispatch logic but not solver correctness. An integration test would catch AMPL model syntax errors, solver option format changes, and data loading issues.

---

### Referenced Documentation

- `specs/done/023-ampl-config-optimizer/spec.md` -- FR-001 through FR-012, SC-001 through SC-004, Section 6 (constraints)
- `conversus/plugins/optimizer/ampl_model.py` -- L29-34, L65-102, L109-145, L218-312, L315-404
- `conversus/plugins/optimizer/ampl_solver.py` -- L64-186
- `conversus/plugins/optimizer/optimizer.py` -- L30-136
- `conversus/plugins/optimizer/__init__.py` -- L19-22
- `tests/test_ampl.py` -- full file
