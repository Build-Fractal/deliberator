# Phase 1 Review: spec-compliance

**Spec**: 019-config-optimizer
**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Check every FR and SC for compliance status.

---

## Functional Requirements

### FR-001: Register as `config-optimizer` with hook `[PRE_EXECUTION]`

**MET**

`ConfigOptimizer.name = "config-optimizer"`, `hooks = [HookPoint.PRE_EXECUTION]`. Tests verify.

### FR-002: Ship as `conversus-ampl` package

**PARTIALLY MET**

The plugin lives at `conversus/plugins/optimizer/`. The `__init__.py` exports `ConfigOptimizer`. However, the spec says "installable via `pip install conversus-ampl`." No AMPL integration exists, and the package is named `optimizer`, not `ampl`. The packaging infrastructure (separate pip package) is not present.

### FR-003: Accept objective function input

**NOT MET**

The optimizer does not read `objective.yml` or use objective function data. It operates purely from plugin config (budget, quality_threshold, max_agents). The spec says "If no objective function is available, the optimizer uses mode-default heuristics." The implementation always uses mode-default heuristics without attempting to read an objective.

### FR-004: Accept budget constraint from config

**MET**

`budget = config.get("budget")`. Required field, handled with error message if missing.

### FR-005: Accept quality threshold from config

**MET**

`quality_threshold = float(config.get("quality_threshold", 0.7))`. Default 0.7 matches spec.

### FR-006: Formulate as MIP using AMPL

**NOT MET**

No AMPL code exists. The implementation uses a Python grid search. The spec says "MUST formulate the config selection problem as a mixed-integer program using AMPL's modeling language." The grid search is an alternative approach, not a MIP formulation.

### FR-007: Solve using HiGHS by default

**NOT MET**

No HiGHS integration. No solver infrastructure. The grid search replaces the solver.

### FR-008: Report infeasible with minimum budget

**MET**

Infeasible cases report the minimum budget needed and the cheapest qualifying config. Reasoning string is clear and actionable.

### FR-009: Output format with required fields

**PARTIALLY MET**

Present: `recommended_rounds`, `recommended_agent_count`, `recommended_iterations`, `estimated_total_launches`, `estimated_quality`, `solver_status`, `budget_used`.
Missing: `recommended_mode`, `objective_value`.

### FR-010: Plain-language recommendation

**MET**

"Recommended: {agents} agents, {rounds} rounds, {iterations} iteration(s). Estimated {cost} agent launches ({pct}% of budget). Expected quality: {quality}." Matches spec format closely. Missing mode recommendation (because mode is not searched).

### FR-011: Interactive mode -- present recommendations with reasoning

**NOT VERIFIED**

No interactive mode implementation. The plugin returns a PluginResult; the interactive confirmation ("wait for user confirmation") is the responsibility of the calling code (mode handler). The plugin correctly sets `advisory=True` for interactive mode, but the actual user interaction is not testable at the plugin level.

### FR-012: Auto mode with `auto_optimize: true`

**MET**

`auto_optimize = bool(config.get("auto_optimize", False))`. When True, `advisory=False`. When False, `advisory=True`. Default is advisory-only.

### FR-013: Must NOT modify conversus.yml directly

**MET**

The plugin returns a PluginResult. No file writes to conversus.yml.

### FR-014: General-purpose solve() API

**NOT MET**

No `solve(model, data, solver)` API exists. The implementation is config-specific.

### FR-015: Custom AMPL model via model_file config

**NOT MET**

No model_file support. The config key is documented in the class docstring ("reserved for future use") but not consumed.

### FR-016: Config fields

**PARTIALLY MET**

Present: `budget`, `quality_threshold`, `auto_optimize`.
Present but unused: `solver`, `model_file`.
Extra: `max_agents`, `cost_per_agent_launch` (not in spec).

### FR-017: Heuristic fallback when AMPL unavailable

**MET (by design)**

The heuristic (grid search) is always used. No AMPL to fail. Same pattern as spec 018's FR-013.

### FR-018: Solver timeout

**NOT APPLICABLE**

Grid search completes in microseconds. No timeout needed.

---

## Success Criteria

### SC-001: Budget=50, quality=0.7 produces valid config

**MET**

Test `test_sc001_budget_50_quality_07` verifies: optimal status, cost <= 50, quality >= 0.7, valid ranges.

### SC-002: Budget=5, quality=0.9 reports infeasible

**MET**

Test `test_sc002_budget_5_quality_09` verifies: infeasible status, reasoning contains "infeasible."

### SC-003: Recommended config is valid conversus.yml config

**PARTIALLY MET**

Types are valid (int rounds, int agents, int iterations). Ranges are valid (rounds 1-5, agents 2-10, iterations 1-3). However, the output does not include `recommended_mode`, which would be required for a complete conversus.yml config.

### SC-004: pip install conversus-ampl installs amplpy and HiGHS

**NOT VERIFIED**

No packaging config. No AMPL dependencies.

### SC-005: Interactive mode presents and waits for confirmation

**NOT VERIFIED**

No interactive mode implementation at the plugin level. This is a calling-code responsibility.

---

## Constraints Compliance

| Constraint | Status |
|-----------|--------|
| Must NOT modify conversus.yml | MET |
| Must NOT require commercial solver | MET (no solver at all) |
| Must NOT make core depend on AMPL | MET |
| Must NOT auto-apply by default | MET -- advisory=True default |

---

## Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-001 | MET | |
| FR-002 | PARTIALLY MET | No AMPL, wrong package name |
| FR-003 | **NOT MET** | No objective function input |
| FR-004 | MET | |
| FR-005 | MET | |
| FR-006 | **NOT MET** | No AMPL MIP formulation |
| FR-007 | **NOT MET** | No HiGHS solver |
| FR-008 | MET | |
| FR-009 | PARTIALLY MET | Missing recommended_mode, objective_value |
| FR-010 | MET | |
| FR-011 | NOT VERIFIED | Calling-code responsibility |
| FR-012 | MET | |
| FR-013 | MET | |
| FR-014 | **NOT MET** | No general-purpose API |
| FR-015 | **NOT MET** | No custom model support |
| FR-016 | PARTIALLY MET | Some fields unused |
| FR-017 | MET (by design) | |
| FR-018 | N/A | |
| SC-001 | MET | |
| SC-002 | MET | |
| SC-003 | PARTIALLY MET | Missing mode |
| SC-004 | NOT VERIFIED | |
| SC-005 | NOT VERIFIED | |
