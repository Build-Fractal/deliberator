# Solver-Engineer Review: Spec 023 -- AMPL Config Optimizer

**Reviewer**: solver-engineer
**Spec**: `specs/done/023-ampl-config-optimizer/spec.md`
**Implementation files reviewed**: `ampl_model.py`, `ampl_solver.py`, `optimizer.py`, `search.py`, `models.py`, `tests/test_ampl.py`

---

### Executive Summary

Spec 023 introduces AMPL/HiGHS mixed-integer programming as an exact solver for the conversus config optimization problem, with the existing grid search retained as a zero-dependency fallback. The implementation takes a sound approach: rather than encoding the non-linear quality model directly (which would require MINLP), it enumerates all integer grid points and encodes them as a binary selection MIP. This is correct for the small search space (max 5x3x9 = 135 points) and guarantees that the MIP solution matches the grid search optimum exactly.

However, the MIP formulation has a structural issue that undermines the claimed advantage over grid search. Because the model enumerates the entire grid and selects one point via binary variables, it is mathematically equivalent to evaluating all points and picking the best -- which is exactly what grid search does. The MIP adds AMPL/HiGHS overhead without any algorithmic advantage. The spec's FR-004 anticipated a "piecewise linear approximation" that would allow the solver to explore continuous relaxations and use branch-and-bound, but the implementation chose full enumeration instead. This is not wrong (it is provably correct), but it means the AMPL solver will always be slower than grid search, not faster, contradicting SC-002.

The quality and cost model consistency is excellent. Tests explicitly verify that `_quality_score` and `_total_cost` in `ampl_model.py` match the grid search equivalents at every integer point (`TestQualityModelConsistency`). The `HAS_AMPL` pattern is clean, the fallback logic is robust, and the general-purpose `solve_ampl()` API is well-designed.

My most critical finding: the MIP formulation should be documented as "exact enumeration via MIP" rather than "mixed-integer programming that outperforms grid search," because the current formulation cannot outperform grid search -- it performs the same enumeration with additional solver overhead.

---

### Alignment

- **[Quality model consistency]** (`ampl_model.py`, L109-119; `search.py`, L33-68): The `_quality_score` function in `ampl_model.py` is an exact copy of the function in `search.py`. Both use the same diminishing-returns formula: `round_factor^0.40 * agent_factor^0.35 * iter_factor^0.25` with identical exponential parameters. The test suite verifies this at every grid point (`TestQualityModelConsistency.test_ampl_quality_matches_search_at_all_points`). This satisfies FR-003's requirement that the AMPL model encode the cost formula exactly.

- **[Cost model consistency]** (`ampl_model.py`, L122-145; `search.py`, L75-98): The `_total_cost` function correctly implements the D007 formula: `agents + agents*(agents-1) + agents*iterations + agents + 1 + arbiter`. The arbiter test (`TestAMPLModelGeneration.test_cost_values_with_arbiter`) verifies that the arbiter flag adds exactly `rounds` launches to the total. The cost computation delegates to `engine.cost.estimate_cost` in the grid search path, and reimplements the formula in `ampl_model.py` for AMPL data generation -- this duplication is acceptable because the test suite verifies equivalence.

- **[HAS_AMPL pattern]** (`ampl_model.py`, L29-34; `ampl_solver.py`, L17-21): The module-level `try/except ImportError` for `amplpy` is the standard pattern for optional dependencies. The flag propagates correctly through `ampl_solver.py`'s import of `HAS_AMPL` from `ampl_model.py`. The test suite patches this flag at the correct module paths (`conversus.plugins.optimizer.ampl_solver.HAS_AMPL` and `conversus.plugins.optimizer.ampl_model.HAS_AMPL`).

- **[Binary selection MIP formulation]** (`ampl_model.py`, L65-102): The AMPL model uses binary `choose[p]` variables over a set of pre-enumerated grid points, constrained to `sum choose[p] = 1`. The objective maximizes quality and the constraints enforce budget and quality thresholds. This is a well-formed 0-1 knapsack variant. The formulation is provably correct: it selects the feasible point with maximum quality, which is exactly what grid search does.

- **[Grid point enumeration]** (`ampl_model.py`, L177-211): The `build_ampl_model` function enumerates all (rounds, iterations, agents) triples, computes quality and cost for each, and stores them as indexed AMPL parameters. The test `test_build_ampl_model_grid_point_count` verifies the count: `5 * 3 * (max_agents - 2 + 1)`. The 1-indexed dict keys match AMPL's 1-based indexing convention. This is correct.

- **[Timeout and fallback]** (`ampl_solver.py`, L114-186): The `_solve_with_ampl_fallback` function wraps the AMPL call in a broad `except Exception` that falls back to grid search. This handles timeout, licence errors, and solver crashes. The test suite verifies `TimeoutError`, `RuntimeError`, and generic `Exception` fallbacks. The metadata correctly reports `ampl_fallback: True` in the fallback case.

---

### Missed Opportunities

- **[MIP adds no algorithmic value over grid search]**: The current formulation enumerates all grid points (up to 135) and uses binary selection variables to pick one. This is mathematically equivalent to iterating over the points and picking the best feasible one -- which is exactly what `optimize_config` in `search.py` does. A HiGHS MIP solver adds overhead (model parsing, presolve, LP relaxation, branch-and-bound) to solve a problem that can be answered by a single pass over 135 points. The spec's FR-004 envisioned a "piecewise linear approximation" that would allow the solver to use LP relaxation to prune the search space, but the implementation chose full enumeration instead. For the current search space size, grid search completes in microseconds while the MIP requires milliseconds -- there is no scenario where the MIP is faster. Impact: **high** (architectural claim of the spec is not realized).

- **[Duplicated quality/cost functions]**: `_quality_score` and `_total_cost` exist in both `ampl_model.py` and `search.py` (as `_quality_score` and `_total_launches`). The test suite verifies equivalence, but the duplication means a change to the quality model requires updating two files. A shared module (e.g., `conversus/plugins/optimizer/formulas.py`) would eliminate this risk. Impact: **medium**.

- **[Hardcoded `gap: 0.0` in solver metadata]** (`ampl_solver.py`, L149): The solver metadata reports `"gap": 0.0` unconditionally when AMPL solves to optimality. However, the gap should be extracted from the HiGHS solver's actual output, not hardcoded. If the solver terminates at the timeout with a feasible (but not proven optimal) solution, the gap would be non-zero, and the hardcoded value would be incorrect. The AMPL API provides `solve_result_num` or solver-specific output to obtain the actual gap. Impact: **medium**.

- **[No test for AMPL timeout path]**: The test `test_timeout_falls_back_to_grid_search` mocks `solve_with_ampl` to raise `TimeoutError`, but there is no test that verifies the `time_limit` option is actually passed to HiGHS. If the option string format changes (e.g., `timelimit` vs `time_limit`), the timeout would silently not apply. A mock test that verifies `ampl.set_option(f"{solver}_options", f"time_limit={timeout}")` was called with the correct value would catch this. Impact: **low**.

- **[`solve_with_ampl` returns `None` for both infeasible and missing-amplpy]** (`ampl_model.py`, L239-240, L271-272, L282-283): Three distinct conditions return `None`: amplpy not installed, AMPL reports infeasible, and no binary variable selected. The caller (`_solve_with_ampl_fallback`) cannot distinguish between "infeasible" and "solver bug where no variable was selected." A richer return type (e.g., returning the solve_result string alongside `None`) would allow the caller to log more precisely. Impact: **low**.

- **[AMPL model stored as Python string, not `.mod` file]**: Spec Section 6 states "The AMPL model must be readable/editable by users (stored as `.mod` file, not generated code)." The implementation stores the model as a Python string constant `CONVERSUS_CONFIG_MODEL` in `ampl_model.py` (L65-102). While technically readable, this violates the spec's explicit constraint. A `.mod` file alongside the Python module would satisfy both the spec requirement and the general-purpose API's file-loading feature (FR-009). Impact: **medium**.

---

### Off-Base Assumptions

- **[SC-002: "AMPL optimizer finds infeasibility faster than grid search"]**: For the current formulation, this is false. The MIP formulation enumerates the same grid points as the grid search. HiGHS must parse the model, build the constraint matrix, solve the LP relaxation, and run branch-and-bound -- all to conclude that no feasible binary assignment exists. The grid search reaches the same conclusion after a single O(n) pass with `n <= 135`. The MIP overhead makes infeasibility detection strictly slower, not faster. This success criterion should be revised or the formulation should be changed to exploit LP relaxation for early infeasibility detection.

- **[Spec FR-004: "piecewise linear approximation validated to within 5% of heuristic"]**: The implementation does not use a piecewise linear approximation. It uses exact quality values at every grid point. This means FR-004's tolerance criterion (within 5%) is trivially satisfied (0% error), but the spirit of the requirement -- that the AMPL model would use an approximation enabling continuous optimization -- is not realized. The spec and implementation should be aligned: either the spec should say "exact enumeration" or the implementation should use an actual PWL approximation.

---

### Actionable Recommendations

1. **Document the enumeration-based MIP as equivalent to grid search** (Priority: P1)
   - **Current state**: The spec and module docstrings claim the MIP "solves the mixed-integer program exactly rather than enumerating the entire grid" (`ampl_model.py`, L8). The implementation enumerates the entire grid.
   - **Proposed change**: Update docstrings and spec Section 2 to accurately describe the formulation: "The MIP encodes all integer grid points as binary selection variables, providing a provably correct solution. For the current search space size (~135 points), this is mathematically equivalent to exhaustive enumeration. The MIP framework enables future extension to larger or continuous search spaces."
   - **Rationale**: Accuracy. The current documentation implies an algorithmic advantage that does not exist. This creates false expectations and makes it harder for future maintainers to understand why the AMPL solver is not faster than grid search.
   - **Risk if ignored**: Developers may waste time debugging performance issues when the AMPL path is slower than grid search, not understanding that this is expected.

2. **Extract quality/cost formulas into a shared module** (Priority: P2)
   - **Current state**: `_quality_score` exists in both `ampl_model.py` and `search.py`. `_total_cost` in `ampl_model.py` reimplements the formula from `engine.cost.estimate_cost`.
   - **Proposed change**: Create `conversus/plugins/optimizer/formulas.py` with canonical `quality_score()` and `total_cost()` functions. Both `ampl_model.py` and `search.py` import from it.
   - **Rationale**: Single source of truth. The test suite currently compensates for duplication by verifying equivalence at every point, but this is a test-as-documentation pattern that hides the real problem: two copies of the same formula.
   - **Risk if ignored**: A quality model change (e.g., adjusting weights) requires coordinated updates to two files. If one is missed, the AMPL and grid search solvers silently diverge.

3. **Extract the actual MIP gap from HiGHS** (Priority: P2)
   - **Current state**: `ampl_solver.py` L149 hardcodes `"gap": 0.0`.
   - **Proposed change**: After `ampl.solve()`, query the solver for the actual gap: `gap = ampl.get_value("solve_result_num")` or use HiGHS-specific output parsing. If the solver status is "solved" (proven optimal), gap is 0.0. If "feasible" (timeout with incumbent), extract the actual gap.
   - **Rationale**: The gap is a key MIP diagnostic. Hardcoding it defeats the purpose of FR-012's requirement to include the gap in solver output.
   - **Risk if ignored**: Users see `gap: 0.0` even when the solver timed out with a suboptimal incumbent, creating false confidence in optimality.

4. **Store the AMPL model as a `.mod` file** (Priority: P2)
   - **Current state**: `CONVERSUS_CONFIG_MODEL` is a Python string constant in `ampl_model.py` L65-102.
   - **Proposed change**: Create `conversus/plugins/optimizer/config_optimizer.mod` and load it at module level or in `build_ampl_model`. The `solve_ampl()` API already supports file loading.
   - **Rationale**: Spec Section 6 constraint: "The AMPL model must be readable/editable by users (stored as `.mod` file, not generated code)."
   - **Risk if ignored**: Spec non-compliance. Users who want to inspect or modify the AMPL formulation must navigate Python string escaping.

5. **Return a richer type from `solve_with_ampl`** (Priority: P3)
   - **Current state**: Returns `OptimalConfig | None` where `None` means either "amplpy not installed," "infeasible," or "no variable selected."
   - **Proposed change**: Return a `SolveOutcome` dataclass with fields `config: OptimalConfig | None`, `status: Literal["optimal", "infeasible", "no_amplpy", "no_selection"]`, and `solve_time_ms: float | None`. This lets the caller distinguish failure modes and log accurately.
   - **Rationale**: Three distinct failure conditions collapsed into a single `None` is a loss of information at the API boundary.
   - **Risk if ignored**: The caller in `_solve_with_ampl_fallback` cannot distinguish "AMPL correctly determined infeasible" from "AMPL silently failed to select a variable."

6. **Revise SC-002 in the spec** (Priority: P3)
   - **Current state**: SC-002 claims "AMPL optimizer finds infeasibility faster than grid search for tight constraints."
   - **Proposed change**: "AMPL optimizer produces the same infeasibility determination as grid search. For larger search spaces (future extensions beyond the current 135-point grid), the MIP formulation enables LP-relaxation-based pruning that grid search cannot."
   - **Rationale**: The current formulation cannot satisfy SC-002 as written. Being honest about the tradeoff (correctness and extensibility vs. performance) is better than claiming a performance advantage that does not exist.
   - **Risk if ignored**: SC-002 is unfalsifiable with the current implementation, which undermines the spec's credibility as a testable contract.

---

### Referenced Documentation

- `conversus/plugins/optimizer/ampl_model.py` -- L8 (docstring claim), L29-34 (HAS_AMPL), L65-102 (CONVERSUS_CONFIG_MODEL), L109-145 (quality/cost helpers), L152-211 (build_ampl_model), L218-312 (solve_with_ampl), L315-404 (solve_ampl)
- `conversus/plugins/optimizer/ampl_solver.py` -- L17-21 (HAS_AMPL import), L64-111 (solve_config dispatch), L114-186 (_solve_with_ampl_fallback), L149 (hardcoded gap)
- `conversus/plugins/optimizer/search.py` -- L33-68 (_quality_score), L75-98 (_total_launches), L105-252 (optimize_config)
- `conversus/plugins/optimizer/models.py` -- L38-59 (OptimalConfig)
- `tests/test_ampl.py` -- L83-226 (TestAMPLModelGeneration), L233-253 (TestHasAMPLFlag), L261-296 (TestSolverDispatch), L340-476 (TestAMPLMockIntegration), L484-591 (TestSolveAMPLAPI), L598-649 (TestTimeoutFallback), L657-704 (TestInfeasibilityConsistency), L740-763 (TestQualityModelConsistency)
- `specs/done/023-ampl-config-optimizer/spec.md` -- FR-003 (cost formula), FR-004 (quality approximation), FR-009 (.mod file), FR-012 (solve_time_ms, gap), SC-002 (infeasibility speed), Section 6 (.mod file constraint)
