# Phase 1 Review: plugin-engineer

**Spec**: 019-config-optimizer
**Reviewer**: plugin-engineer
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Evaluate Plugin ABC conformance, PRE_EXECUTION hook behavior, auto_optimize flag, and advisory vs actionable distinction.

---

## Plugin ABC Conformance

### Class Attributes

`ConfigOptimizer` subclasses `Plugin`:
- `name = "config-optimizer"` -- matches FR-001.
- `hooks = [HookPoint.PRE_EXECUTION]` -- matches FR-001.

### `execute()` Method

Signature: `def execute(self, state: DeliberationState, config: dict[str, Any]) -> PluginResult`.
Returns `PluginResult` in all paths: missing budget, invalid budget, infeasible, and optimal.

### Instantiation

Default and config-based construction work. Tests verify `plugin_config` storage.

**Verdict**: Full ABC conformance.

---

## PRE_EXECUTION Hook Behavior

The optimizer runs at PRE_EXECUTION -- before deliberation starts. This is the correct hook for recommending configuration changes.

### State at PRE_EXECUTION

At PRE_EXECUTION, `state.round` is 0, `state.agents` is typically empty (agents haven't been created yet), and `state.config` contains the user's initial config. The optimizer reads `state.config.get("has_arbiter", False)` for cost calculation. This is appropriate -- the optimizer uses the declared config, not runtime state.

### Output File

The output file is `config-optimizer-pre_execution-round-0.json`. Tests verify existence and content structure. The round-0 naming is correct for PRE_EXECUTION.

**Verdict**: Correct hook placement and execution.

---

## auto_optimize Flag Behavior (FR-012)

The spec defines two modes:
1. **Advisory (default)**: `auto_optimize: false` -- recommendations require user confirmation.
2. **Auto mode**: `auto_optimize: true` -- recommendations "MAY be silently applied."

Implementation:
```python
auto_optimize = bool(config.get("auto_optimize", False))
is_advisory = not auto_optimize
```

When `auto_optimize=True`, `PluginResult.advisory = False`. When `auto_optimize=False` (default), `advisory = True`.

**Assessment**: The flag correctly controls the advisory field. However, the actual application of recommendations is not implemented in the plugin -- it only sets the advisory flag. The spec says "the calling code (mode handler or converge handler) applies it if the user confirms." The plugin's job is to signal intent via the advisory flag; the calling code acts on it. This separation is correct.

### FR-013 Compliance

"The optimizer MUST NOT modify `conversus.yml` directly." The plugin returns a PluginResult; it never writes to conversus.yml. MET.

---

## Output Format (FR-009)

Required fields:
- `recommended_rounds`: present
- `recommended_agent_count`: present
- `recommended_mode`: **MISSING**
- `recommended_iterations`: present
- `estimated_total_launches`: present
- `estimated_quality`: present
- `solver_status`: present (optimal/feasible/infeasible)
- `objective_value`: **MISSING**
- `budget_used`: present (percentage)

**Issues**:
1. `recommended_mode` is missing because the optimizer does not search over modes.
2. `objective_value` is missing. The grid search does not have a separate objective value (it maximizes quality). The `estimated_quality` serves a similar role but is not labeled `objective_value`.

**Verdict**: FR-009 PARTIALLY MET due to missing fields.

---

## Error Handling

1. **Missing budget**: Returns advisory result with `error: "missing_budget"`. Clear message.
2. **Invalid budget**: Returns advisory result with `error: "invalid_budget"`. Handles non-numeric values.
3. **Infeasible optimization**: Returns result with `solver_status: "infeasible"` and reasoning that explains minimum budget needed (FR-008).

### FR-017: AMPL/Solver Unavailable

The code never attempts AMPL. The grid search is always used. FR-017 says "emit a warning and return a heuristic recommendation." Since the heuristic is always the primary path, this is technically satisfied -- the warning is absent because the heuristic never fails.

### FR-018: Solver Timeout

Not applicable -- grid search completes in microseconds. No timeout mechanism exists, but none is needed.

**Verdict**: Error handling is robust for the implemented scope. Missing AMPL means FR-017/FR-018 are moot.

---

## Additional Observations

1. **Budget validation**: Accepts both int and float budgets via `float(budget)`. Robust type coercion.
2. **max_agents clamping**: `max(2, min(max_agents, 10))` ensures valid range. Test verifies.
3. **cost_per_launch multiplier**: Allows budget in units other than raw launches (e.g., dollars). Well-designed abstraction.
4. **No mode recommendation**: The optimizer does not suggest a mode, which is a significant gap per the spec.
5. **Logging on infeasible**: `logger.warning()` is called for infeasible results. Good practice.

---

## Summary

| Area | Verdict |
|------|---------|
| Plugin ABC conformance | Full |
| PRE_EXECUTION hook | Correct |
| auto_optimize flag | Correctly controls advisory field |
| FR-013 (no direct config modification) | MET |
| Output format (FR-009) | PARTIALLY MET (missing fields) |
| Error handling | Robust for implemented scope |
| FR-017/FR-018 | Moot (no AMPL) |

### Key Issues

1. **FR-009 missing `recommended_mode` and `objective_value`**: Two required output fields absent.
2. **No mode search**: Spec envisions mode as a decision variable.
3. **AMPL not implemented**: Grid search is the only backend.
