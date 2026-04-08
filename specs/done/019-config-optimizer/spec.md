# Feature Specification: Config Optimizer Plugin (AMPL)

**Feature ID**: `019-config-optimizer`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `014-guided-objective-construction` (objective function as input), `016-plugin-system` (Plugin base class, PRE_EXECUTION hook)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 4: Config Optimization, FR-015, decision Q3: mode-dependent advisory/auto behavior).

---

## 1. Feature Summary

Given a problem description, an objective function, and a budget, the config optimizer computes the optimal conversus configuration: how many rounds, how many agents, which mode, and how many iterations. It answers: "What config should I use to get the best outcome within my budget?"

The optimizer models config selection as a mixed-integer programming (MIP) problem. Decision variables are the config parameters. The objective is to minimize total agent launches subject to a quality threshold. AMPL is the modeling language, making the formulation solver-agnostic -- HiGHS (free, bundled) for most users, Gurobi for enterprise scale.

Beyond conversus config optimization, the AMPL plugin provides general-purpose optimization capability. Users can define arbitrary MIP, NLP, or MINLP problems using AMPL's modeling language. The conversus config optimizer is the flagship use case, but the infrastructure supports any optimization problem.

**What changes**: New `conversus-ampl` package with `ConfigOptimizer` plugin class. New `plugins/config-recommendation.json` output.

**What does not change**: Core deliberation. Config parsing. Template system.

---

## 2. Optimization Model

### Decision Variables

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| `rounds` | integer | [1, 5] | Number of deliberation rounds |
| `agent_count` | integer | [2, 10] | Number of agents |
| `mode` | categorical | {cooperative, wta, pd, rb} | Deliberation mode |
| `iterations` | integer | [1, 3] | Iterations per agent per phase |

### Objective Function

Minimize total agent launches:

```
minimize: agent_count * phases_per_mode(mode) * rounds * iterations
```

Where `phases_per_mode` maps mode to phase count (cooperative=5, wta=5, pd=5, rb=5 base; +1 for arbitration if configured).

### Constraints

- Budget: `total_launches <= max_budget`
- Quality: `estimated_quality(rounds, agent_count, mode) >= quality_threshold`
- Mode compatibility: mode must be compatible with the objective function's `mode_compatibility` field (spec 013)

### Quality Estimation

Quality is estimated from the objective function parameters and known relationships:
- More agents improve coverage but have diminishing returns
- More rounds improve convergence but have diminishing returns
- Mode affects dispute structure (cooperative produces fewer disputes than adversarial modes)

The quality model is a parameterized function fit from prior deliberation data. For v1, it uses conservative heuristic estimates. Future versions improve the quality model as more deliberation data accumulates (per decision Q5: local-only learning).

---

## 3. Functional Requirements

### Plugin Registration

- **FR-001**: The plugin MUST register as `config-optimizer` with hook `[PRE_EXECUTION]`.
- **FR-002**: The plugin MUST ship as the `conversus-ampl` package, installable via `pip install conversus-ampl`.

### Input

- **FR-003**: The optimizer MUST accept an objective function (`objective.yml` from spec 014) as input. If no objective function is available, the optimizer uses mode-default heuristics.
- **FR-004**: The optimizer MUST accept a budget constraint (maximum total agent launches) from plugin config.
- **FR-005**: The optimizer MUST accept a quality threshold (minimum acceptable quality score, default 0.7) from plugin config.

### Optimization

- **FR-006**: The optimizer MUST formulate the config selection problem as a mixed-integer program using AMPL's modeling language.
- **FR-007**: The optimizer MUST solve using HiGHS (bundled, free) by default. Users MAY configure an alternative solver (Gurobi, CPLEX) via plugin config.
- **FR-008**: The optimizer MUST report if the problem is infeasible (budget too low for quality threshold) with a plain-language explanation and the minimum budget needed.

### Output

- **FR-009**: The plugin MUST produce `plugins/config-recommendation.json` containing:
  - `recommended_rounds`: integer
  - `recommended_agent_count`: integer
  - `recommended_mode`: string
  - `recommended_iterations`: integer
  - `estimated_total_launches`: integer
  - `estimated_quality`: float
  - `solver_status`: string (optimal, feasible, infeasible)
  - `objective_value`: float
  - `budget_used`: float (percentage of budget consumed)
- **FR-010**: The `recommendation` field MUST include a plain-language summary: "Recommended: 3 agents, 2 rounds, cooperative mode, 1 iteration. Estimated 30 agent launches (60% of budget). Estimated quality: 0.82."

### Mode-Dependent Behavior (Decision Q3)

- **FR-011**: In interactive mode (invoked via `/conversus mode` or `/conversus converge`), the optimizer MUST present recommendations with reasoning and wait for user confirmation before applying.
- **FR-012**: In auto mode (`auto_optimize: true` in plugin config), recommendations MAY be silently applied to the config. Default is advisory-only; auto-apply requires explicit opt-in.
- **FR-013**: The optimizer MUST NOT modify `conversus.yml` directly. It produces a recommendation; the calling code (mode handler or converge handler) applies it if the user confirms.

### General-Purpose Optimization

- **FR-014**: The `conversus-ampl` package MUST expose a general-purpose optimization API: `solve(model: str, data: dict, solver: str = "highs") -> Solution`. This enables users to define custom AMPL models beyond conversus config optimization.
- **FR-015**: Custom models MUST be specifiable in plugin config via a `model_file` field pointing to a `.mod` file.

### Configuration

- **FR-016**: Plugin config MUST support:
  - `budget`: integer (maximum total agent launches)
  - `quality_threshold`: float (default 0.7)
  - `solver`: string (default "highs")
  - `auto_optimize`: boolean (default false)
  - `model_file`: string (optional, path to custom AMPL model)

### Error Handling

- **FR-017**: If AMPL or the solver is not available, the plugin MUST emit a warning and return a heuristic recommendation (e.g., "3 agents, 2 rounds" as safe defaults). No crash.
- **FR-018**: Solver timeout MUST be configurable (default: 30 seconds). If the solver times out, report the best feasible solution found so far.

---

## 4. Success Criteria

- **SC-001**: Given budget=50 and quality_threshold=0.7, the optimizer recommends a config whose estimated launches are <= 50 and estimated quality >= 0.7.
- **SC-002**: Given budget=5 and quality_threshold=0.9, the optimizer reports infeasible and suggests the minimum budget needed.
- **SC-003**: The optimizer's recommended config is a valid `conversus.yml` config (correct types, valid mode, valid ranges).
- **SC-004**: `pip install conversus-ampl` installs amplpy and HiGHS without requiring a commercial license.
- **SC-005**: In interactive mode, the optimizer presents the recommendation and waits for confirmation before any config is changed.

---

## 5. Constraints

- **Must NOT modify `conversus.yml` directly.** The optimizer recommends; the user or calling code applies. Plugin isolation (FR-015 from spec 016) is absolute.
- **Must NOT require a commercial solver.** HiGHS (Apache 2.0) is bundled. Commercial solvers (Gurobi, CPLEX) are optional for users who have licenses.
- **Must NOT make the core engine depend on AMPL.** `conversus-ampl` is a paid plugin package. The core engine works without it.
- **Must NOT auto-apply by default.** Auto-optimization is opt-in (`auto_optimize: true`). Default behavior is advisory with user confirmation (decision Q3).
