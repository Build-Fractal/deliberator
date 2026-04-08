# Phase 1 Review: optimization-engineer

**Spec**: 023-ampl-config-optimizer
**Reviewer**: optimization-engineer
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: MIP formulation correctness, grid point enumeration, quality/cost model consistency

---

## Executive Summary

The AMPL config optimizer is well-designed. The MIP formulation correctly encodes the config optimization problem as a binary selection over pre-computed grid points, which is mathematically equivalent to the grid search but can be solved by HiGHS in O(1) decision variables rather than O(n) enumeration. The quality and cost functions match the grid search exactly (verified at all integer grid points in the test suite). The piecewise-linear approximation via grid-point lookup with binary selection variables is a clever approach that avoids non-linear quality models while preserving optimality. However, there are two concerns: (1) the MIP formulation reduces to a simple binary selection problem (choose one grid point) which HiGHS will solve via enumeration anyway -- the theoretical advantage of MIP over grid search is minimal for the current search space, and (2) the general-purpose `solve_ampl()` API is well-designed but its error handling for malformed models is delegated entirely to amplpy, with no wrapper-level validation.

---

## MIP Formulation (FR-003, FR-004)

### Model Structure

The AMPL model uses binary selection variables over pre-computed grid points:

```ampl
var choose {QUALITY_POINTS} binary;
maximize expected_quality: sum {p} qp_quality[p] * choose[p];
subject to one_choice: sum {p} choose[p] = 1;
subject to budget_limit: sum {p} qp_cost[p] * choose[p] <= max_budget;
subject to quality_floor: sum {p} qp_quality[p] * choose[p] >= quality_threshold;
```

This is a correct MIP formulation. The binary selection with the `one_choice` constraint ensures exactly one grid point is chosen. The budget and quality constraints are linear in the binary variables.

### Equivalence to Grid Search

The formulation is mathematically equivalent to: "choose the grid point with the highest quality that satisfies the budget and quality constraints." This is exactly what the grid search does by enumeration. The MIP formulation does not add mathematical insight -- it translates the enumeration into a form that a MIP solver can process.

For the current search space (5 rounds x 3 iterations x up to 9 agents = up to 135 grid points), the grid search enumeration is O(135) comparisons -- effectively instant. The MIP solver adds overhead (model parsing, presolve, branching setup) that likely exceeds the grid search time for this problem size.

**Assessment**: The MIP formulation is correct and mathematically sound, but its practical advantage emerges only if the search space grows (more dimensions, continuous relaxations, or additional constraints that make enumeration infeasible).

### Cost Formula Correctness (FR-003)

The `_total_cost()` function in ampl_model.py matches the D007 formula:

```python
per_round = (
    agent_count                           # review
    + agent_count * (agent_count - 1)     # cross_review
    + agent_count * iterations            # revision
    + agent_count                         # disputes
    + 1                                   # synthesis
    + (1 if has_arbiter else 0)           # arbitration
)
total_cost = rounds * per_round * cost_per_launch
```

The test `test_cost_values_match_grid_search` verifies this matches `search.py`'s `_total_launches()` at every grid point. The arbiter test (`test_cost_values_with_arbiter`) verifies the arbiter adds exactly `rounds` launches (one per round).

### Quality Model Correctness (FR-004)

The `_quality_score()` function uses the same weighted geometric mean of diminishing-returns curves as the grid search:

```python
quality = round_factor^0.40 * agent_factor^0.35 * iter_factor^0.25
```

Where each factor is `1 - exp(-k * x)`. The test `test_quality_scores_match_grid_search` verifies exact match at all grid points. The test `test_ampl_quality_matches_search_at_all_points` extends this to the full 5x3x9 grid (135 points per config). FR-004 requires the approximation to be "within 5% of the heuristic at all integer grid points" -- the implementation achieves 0% error (exact match) because it uses the same formula.

---

## Grid Point Enumeration

The `build_ampl_model()` function enumerates all integer grid points:

```python
for r in range(1, 6):        # rounds: 1-5
    for it in range(1, 4):    # iterations: 1-3
        for a in range(2, max_agents + 1):  # agents: 2-max_agents
```

The grid size is `5 * 3 * (max_agents - 1)`. With max_agents = 5, this is 60 points. With max_agents = 10, this is 135 points. The max_agents clamping to [2, 10] is correct (you need at least 2 agents; more than 10 is impractical).

Each grid point stores rounds, iterations, agents, quality, and cost. These are passed to AMPL as indexed parameters. The index starts at 1 (AMPL convention) -- this is correctly handled.

---

## Infeasibility Handling (FR-005)

When the budget is too low or quality threshold too high, no grid point satisfies both constraints. The AMPL solver reports "infeasible." The `solve_with_ampl()` function returns None, and the dispatch layer delegates to grid search for the infeasibility report.

This two-stage approach is correct: AMPL detects infeasibility quickly (presolve), then grid search provides the human-readable report (minimum budget needed, available quality range). The test `test_ampl_infeasible_delegates_to_grid_search_report` verifies this flow.

---

## General-Purpose API (FR-007 through FR-010)

The `solve_ampl()` function is a clean general-purpose interface:
- Accepts model strings or `.mod` file paths (FR-009).
- Supports arbitrary AMPL parameters (scalar and indexed) via a data dict.
- Extracts solve result, objective value, solve time, and variable values.
- Always closes the AMPL instance (try/finally).

The file-vs-string detection uses a simple heuristic: if the model ends with `.mod` and contains no newlines, it is a file path. This is pragmatic but could misclassify a model string that ends with ".mod" (unlikely but possible).

### Concern: No Model Validation

`solve_ampl()` passes the model string directly to `ampl.eval()` without validation. A malformed model (syntax errors, undefined parameters) will produce an amplpy exception. The function does not wrap this in a user-friendly error. For the general-purpose API (which external users may call), a validation layer would improve usability.

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Document the MIP-vs-grid-search performance trade-off. For the current search space (up to 135 points), the grid search is likely faster. The MIP formulation's value is extensibility (additional constraints, continuous relaxations, larger search spaces).

### P2 (Should Fix)

2. **P2-1**: Add basic model validation to `solve_ampl()` -- at minimum, check that the model string is non-empty and catch AMPL parse errors with a descriptive message.

3. **P2-2**: The file-vs-string heuristic for `.mod` detection should be more robust. Consider requiring an explicit `model_file` parameter instead of overloading the `model` parameter.

### P3 (Consider)

4. **P3-1**: For future extensibility, consider parameterizing the quality model (allow users to provide custom quality curves via the plugin config). Currently, the exponential diminishing-returns model is hardcoded.
