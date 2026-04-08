# Phase 1 Review: plugin-engineer

**Spec**: 018-convergence-predictor
**Reviewer**: plugin-engineer
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Evaluate Plugin ABC conformance, hook execution, coexistence with EquilibriumScorer, and output format compliance.

---

## Plugin ABC Conformance

### Class Attributes

`ConvergencePredictor` correctly subclasses `Plugin`:
- `name = "convergence-predictor"` -- matches FR-001.
- `hooks = [HookPoint.POST_PHASE_5]` -- matches FR-001 (single hook).

### `execute()` Method

Signature matches ABC: `def execute(self, state: DeliberationState, config: dict[str, Any]) -> PluginResult`.
Returns `PluginResult` in all paths: unknown mode, no agents, feature history failure, prediction failure, and success.

### Instantiation

Default and config-based construction work. Tests verify `plugin_config` storage.

**Verdict**: Full ABC conformance.

---

## Hook Execution

### POST_PHASE_5

Tests confirm firing via `execute_hooks()`. Output file: `convergence-predictor-post_phase_5-round-{N}.json`. Correct.

### Negative Cases

Tests confirm the plugin does NOT fire at POST_DELIBERATION or PRE_EXECUTION. This is correct per FR-001 (only POST_PHASE_5).

### Output File Persistence

The output JSON is written by `execute_hooks()` in base.py with the standard structure: plugin name, hook, round, recommendation, data, advisory flag.

**Verdict**: Hook execution is correct. Single hook, fires at the right point, output persisted.

---

## Coexistence with EquilibriumScorer

Both plugins subscribe to POST_PHASE_5. Test `test_coexists_with_equilibrium_scorer` runs both plugins at the same hook and verifies:
1. Both return results (len == 2).
2. Both output files exist with distinct names.

The naming convention `{plugin-name}-{hook}-round-{N}.json` ensures no collision.

**Issue**: The ConvergencePredictor passes `equilibrium_scores=None` to `predict_convergence()`. It does not read the EquilibriumScorer's output from the plugins directory, even when both run at the same hook. This means the equilibrium trend bonus in confidence calibration is always 0. The code has a TODO: `# TODO: read from scorer output`.

**Verdict**: Coexistence works at the infrastructure level (no crashes, no collisions). But the intended data flow (predictor reads scorer output) is not implemented.

---

## Output Format (FR-010)

Required fields in `plugins/convergence-prediction-round-{N}.json`:
- `prediction`: string (converge/stagnate/uncertain) -- present
- `confidence`: float 0.0-1.0 -- present
- `estimated_rounds_remaining`: integer or null -- present
- `current_round`: integer -- present
- `dispute_trajectory`: list of ints -- present
- `position_drift`: float -- present
- `fixed_point_exists`: boolean -- present
- `reasoning`: string -- present

All FR-010 fields are present. Types are correct.

### Filename

The output filename is `convergence-predictor-post_phase_5-round-{N}.json`. The spec says `plugins/convergence-prediction-round-{N}.json`. Same pattern deviation as spec 017 (base infrastructure naming).

**Verdict**: Output format fully compliant. Filename has the same pattern deviation as the scorer.

---

## Recommendation Strings (FR-007, FR-008)

### Converge (FR-008)

`"Convergence predicted in ~{N} round(s) (confidence: {C}). Estimated additional agent launches: {L}."`

Matches FR-008's required format. Cost estimation (`rounds * (num_agents + 1)`) provides the "estimated additional agent launches" field.

### Stagnate (FR-007)

`"Stagnation predicted (confidence: {C}). Consider: (1) triggering arbitration, (2) adjusting agent configuration, (3) stopping and using current synthesis."`

Matches FR-007 exactly.

### Uncertain

`"Prediction uncertain (confidence: {C}). {reasoning}"`

No specific FR for uncertain format; the implementation is reasonable.

**Verdict**: Recommendation strings match FR-007 and FR-008 closely.

---

## Error Handling

1. **Unknown mode**: Returns advisory error result. No crash.
2. **No agents**: Returns "uncertain" with empty trajectory. FR-012 compliant.
3. **Feature history construction failure**: Catches exception, returns advisory.
4. **Prediction computation failure**: Catches exception, returns advisory.

All error paths tested. Defense-in-depth with multiple try/except layers.

**Verdict**: Robust error handling. FR-012 and FR-013 are MET.

---

## Additional Observations

1. **advisory=True always**: Correct per FR-009 (advisory only).
2. **auto_stop config**: Accepted but not used. FR-011 says `auto_stop` defaults to false and is "reserved for future autonomous mode." The code reads it: `config.get("auto_stop", False)` is NOT present in the execute() method -- the config key is documented but not read. This is fine since it's reserved for the future.
3. **History construction**: `_build_feature_history()` converts `state.history` (list of `RoundState`) to `RoundFeatures` and appends current round. This is the bridge between the plugin state model and the prediction function's feature model.

---

## Summary

| Area | Verdict |
|------|---------|
| Plugin ABC conformance | Full |
| Hook execution | Correct (POST_PHASE_5 only) |
| Coexistence with scorer | Works; data flow incomplete (TODO) |
| Output format (FR-010) | Fully compliant |
| Recommendations (FR-007, FR-008) | Match spec format |
| Error handling | Robust |
| advisory flag | Correct |

### Key Issues

1. **Equilibrium score integration TODO**: Predictor never reads scorer output. Equilibrium trend is always 0.
2. **auto_stop config not read**: Documented but not consumed. Minor.
