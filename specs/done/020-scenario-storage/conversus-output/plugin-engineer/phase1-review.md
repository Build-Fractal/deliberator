# Phase 1 Review: plugin-engineer

**Spec**: 020-scenario-storage
**Reviewer**: plugin-engineer
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Evaluate Plugin ABC conformance, POST_DELIBERATION hook behavior, auto_save config, and output namespace.

---

## Plugin ABC Conformance

### Class Attributes

`ScenarioPlugin` subclasses `Plugin`:
- `name = "scenario"` -- the spec does not specify a plugin name explicitly. The name "scenario" is reasonable.
- `hooks = [HookPoint.POST_DELIBERATION]` -- correct for scenario capture after deliberation completes.

### `execute()` Method

Signature matches ABC. Returns `PluginResult` in all paths.

### Instantiation

Default and config-based construction work.

**Verdict**: Full ABC conformance.

---

## POST_DELIBERATION Hook

### Timing

POST_DELIBERATION is the correct hook for scenario saving: the deliberation is complete, the outcome is known, and the game structure can be captured.

### Output

The plugin writes `scenario.yml` to `{output_dir}/plugins/`. This is direct file I/O within the execute() method, unlike the equilibrium scorer and convergence predictor which delegate file writing to `execute_hooks()`.

**Concern**: The plugin writes to `{output_dir}/plugins/scenario.yml` directly, in addition to `execute_hooks()` writing `scenario-post_deliberation-round-{N}.json`. This creates two output files: one YAML (from the plugin) and one JSON (from the base infrastructure). The JSON contains the PluginResult data (scenario name, mode, agent count); the YAML contains the full scenario object. This dual-output is intentional but could be confusing.

### Hook Integration

Test `test_plugin_attributes` verifies hook registration. No test for firing via `execute_hooks()` exists -- the tests call `execute()` directly. This is a gap in integration testing.

**Verdict**: Hook placement is correct. Dual-output (YAML + JSON) is intentional but worth noting.

---

## auto_save Config

```python
auto_save = config.get("auto_save", True)
```

Default is True -- the plugin writes scenario.yml by default. Setting `auto_save: false` disables the YAML write. Even with auto_save disabled, the base `execute_hooks()` still writes the JSON output.

Test `test_execute_auto_save_disabled` verifies no YAML file when auto_save=False. Test `test_execute_default_auto_save` verifies default True behavior.

**Assessment**: Clean config behavior. The default True is sensible -- auto-save is the expected behavior for a scenario plugin.

---

## Output Namespace

### YAML Output

Written to `{output_dir}/plugins/scenario.yml`. This is within the plugins namespace, consistent with Principle XV (plugin isolation).

### Scenarios Directory

When `scenarios_dir` is configured, the plugin also writes to `{scenarios_dir}/scenarios/{name}.yml` via `FileScenarioStore.save()`. This creates persistent scenario files outside the output directory.

**Concern**: The plugin has two write paths: (1) output-dir YAML (ephemeral, per-run) and (2) scenarios-dir YAML (persistent, cross-run). This dual-path is appropriate for different use cases but increases complexity.

### PluginResult Structure

```python
PluginResult(
    recommendation=f"Scenario '{scenario_name}' saved.",
    data={
        "scenario_name": scenario_name,
        "mode": state.mode,
        "agent_count": len(agent_roles),
        "scenario_path": str(scenario_path),  # only if auto_save
        "run_count": len(updated.run_history),  # only if scenarios_dir
    },
)
```

The `advisory` field defaults to True (from PluginResult default). This is correct -- scenario saving is informational.

**Concern**: The `advisory` field is not explicitly set in the PluginResult constructor. It relies on the Pydantic default (True). While correct, explicit is better than implicit for such an important field.

---

## Error Handling

1. **No output_dir**: If `state.output_dir` doesn't exist, `plugins_dir.mkdir(parents=True, exist_ok=True)` handles it.
2. **No scenarios_dir**: If `config.get("scenarios_dir")` is None, the persistent store path is skipped.
3. **Store operations**: If `store.save()` or `store.append_run()` fail, the exception propagates. There is no try/except around the store operations.

**Concern**: Unhandled exceptions in store operations could crash the plugin. If the scenarios directory is read-only or the YAML file is malformed, the plugin would fail. This violates the principle that plugins should not crash.

**Assessment**: Missing error handling for store operations. Should wrap in try/except and return advisory error result.

---

## Additional Observations

1. **RunRecord construction**: The plugin computes `dispute_count` as `sum(r.dispute_count for r in state.history)`. This sums across all rounds, giving total disputes. Individual round disputes are lost. This is acceptable for the summary record.

2. **No outcome field in RunRecord**: The spec's Section 2.3 mentions "outcome: brief description of the result" in run history. The RunRecord model has `termination_reason` instead of `outcome`, and no `agents_launched` field. The spec and model diverge on field names.

3. **ScenarioPlugin name is "scenario"**: Different from the spec's "scenario-storage" naming. Not a compliance issue per se, but the naming convention differs from other plugins (e.g., "equilibrium-scorer", "convergence-predictor", "config-optimizer").

---

## Summary

| Area | Verdict |
|------|---------|
| Plugin ABC conformance | Full |
| POST_DELIBERATION hook | Correct placement |
| auto_save config | Clean, default True |
| Output namespace | Within plugins/, correct |
| Dual output (YAML + JSON) | Intentional but notable |
| Error handling | Missing try/except for store ops |
| advisory field | Correct (default True) |

### Key Issues

1. **Missing error handling for store operations**: Exception propagation could crash plugin.
2. **RunRecord field divergence**: `termination_reason` vs spec's `outcome`, missing `agents_launched`.
3. **advisory not explicitly set**: Relies on default.
