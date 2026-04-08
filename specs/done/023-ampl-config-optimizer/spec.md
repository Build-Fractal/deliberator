# Feature Specification: AMPL/HiGHS Config Optimization

**Feature ID**: `023-ampl-config-optimizer`
**Created**: 2026-03-25
**Status**: Draft
**Depends On**: `019-config-optimizer` (heuristic optimizer to upgrade), `014-guided-objective-construction` (objective function as optimization input), `016-plugin-system` (plugin framework)
**Origin**: Review finding — spec 019 implements heuristic grid search only. This spec delivers mixed-integer programming via AMPL.

---

## 1. Feature Summary

Replace the heuristic grid search in the config optimizer with a proper mixed-integer programming (MIP) formulation using AMPL modeling language and the HiGHS solver (free, bundled). The grid search remains as the zero-dependency fallback.

The AMPL optimizer also enables a general-purpose optimization API: users can define custom optimization problems beyond conversus config tuning.

**What changes**: `conversus/plugins/optimizer/` gains `ampl_model.py` (AMPL formulation) and `ampl_solver.py` (solver interface). The optimizer plugin dispatches to AMPL when available, grid search otherwise.

**What does not change**: Plugin interface. Hook point (PRE_EXECUTION). Output format (OptimalConfig). Budget/quality constraints.

---

## 2. Technical Approach

### AMPL Model: Conversus Config Optimization

```ampl
# Decision variables
var rounds integer >= 1, <= 5;
var iterations integer >= 1, <= 3;
var agent_count integer >= 2, <= max_agents;

# Derived
var total_launches = agent_count^2 + 2*agent_count + 1;
var cost = rounds * total_launches * cost_per_launch;

# Quality model (piecewise linear approximation of heuristic curves)
var quality;

# Objective: maximize quality
maximize expected_quality: quality;

# Constraints
subject to budget_limit: cost <= max_budget;
subject to quality_floor: quality >= quality_threshold;
subject to quality_model: quality = f(rounds, iterations, agent_count);
```

### HiGHS Solver

HiGHS is a free, open-source MIP solver (Apache 2.0 licensed) that ships as a Python wheel (`pip install highspy`). It handles the integer constraints on rounds/iterations/agent_count natively.

### General-Purpose API

Beyond conversus config, the AMPL integration enables users to define custom optimization problems:

```python
from conversus.plugins.optimizer import solve_ampl

result = solve_ampl(
    model_file="my_problem.mod",
    data={"budget": 1000, "agents": 5},
    solver="highs",
)
```

---

## 3. Functional Requirements

### Config Optimization
- **FR-001**: When `amplpy` and `highspy` are importable, the optimizer MUST use the AMPL/HiGHS formulation instead of grid search.
- **FR-002**: When neither is available, the optimizer MUST fall back to the existing grid search.
- **FR-003**: The AMPL model MUST encode the D007 cost formula exactly (not an approximation).
- **FR-004**: The quality model MUST be a piecewise linear approximation of the heuristic quality curves, validated to within 5% of the heuristic at all integer grid points.
- **FR-005**: The solver MUST handle infeasibility gracefully (budget too low or quality too high), returning the same infeasibility report as the grid search.
- **FR-006**: Solver execution MUST be capped at a configurable timeout (default 10s).

### General-Purpose API
- **FR-007**: The optimizer package MUST expose a `solve_ampl(model, data, solver)` function for arbitrary AMPL problems.
- **FR-008**: The general-purpose API MUST support MIP, LP, NLP, and MINLP problem types (solver permitting).
- **FR-009**: Model files MUST be loadable from disk (`.mod` files) or from string.
- **FR-010**: The API MUST NOT require AMPL license — HiGHS is free and sufficient for MIP/LP.

### Output
- **FR-011**: The `PluginResult.data` dict MUST include `solver: "ampl-highs"` (or `solver: "grid-search"`).
- **FR-012**: When AMPL solves, the result MUST include `solve_time_ms` and `gap` (optimality gap for MIP).

---

## 4. Success Criteria

- **SC-001**: AMPL optimizer produces the same optimal config as grid search for all feasible inputs (they should agree on the optimum since the search space is small).
- **SC-002**: AMPL optimizer finds infeasibility faster than grid search for tight constraints.
- **SC-003**: General-purpose `solve_ampl()` solves a simple LP problem correctly.
- **SC-004**: With amplpy/highspy uninstalled, behavior is identical to the current grid search.

---

## 5. Dependencies

- `amplpy` — AMPL Python API
- `highspy` — HiGHS solver Python bindings (free, Apache 2.0)
- Both are optional runtime dependencies, not package requirements.

---

## 6. Constraints

- Must NOT add amplpy/highspy to core package requirements.
- Must NOT change the Plugin interface or output format.
- Must NOT break the grid search fallback path.
- The AMPL model must be readable/editable by users (stored as `.mod` file, not generated code).
- HiGHS is the default solver. Commercial solvers (Gurobi, CPLEX) may be supported via AMPL's solver switching but are not required.
