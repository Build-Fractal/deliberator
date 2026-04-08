# Phase 1 Review: spec-compliance

**Spec**: 020-scenario-storage
**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Check every FR and SC for compliance status.

---

## Functional Requirements

### FR-001: YAML files at `scenarios/{id}.yml`

**MET**

`FileScenarioStore._path_for(name)` returns `{root}/scenarios/{name}.yml`. Tests verify save creates the path.

### FR-002: Pydantic Scenario model validates scenario files

**MET**

`Scenario` is a frozen Pydantic BaseModel with typed fields. `_dict_to_scenario()` uses `Scenario.model_validate()`. `ScenarioValidationError` wraps Pydantic `ValidationError`.

### FR-003: Clean separation of game structure, data bindings, run history

**MET**

Three distinct models: `GameStructure`, `DataBindings`, `RunRecord`. Composed in `Scenario`. Tests verify all three sections.

### FR-004: `/conversus save <name>` extracts game structure

**NOT VERIFIED**

No CLI command implementation reviewed. The plugin extracts game structure from `DeliberationState` in its `execute()` method. The actual `/conversus save` command is not implemented at the plugin level -- it would be in the CLI layer.

### FR-005: Overwrite prompt on duplicate name

**NOT VERIFIED**

No CLI overwrite-prompt implementation. `FileScenarioStore.save()` silently overwrites. The prompt would be in the CLI layer.

### FR-006: Data bindings set to null in saved scenario

**MET**

Plugin creates `DataBindings()` (all defaults: target=None, agent_docs={}, grounding_doc=None). Tests verify null bindings.

### FR-007: Current run appended to run history

**MET**

Plugin constructs a `RunRecord` and calls `store.append_run()` when `scenarios_dir` is configured. The record includes rounds_completed, dispute_count, and termination_reason.

### FR-008: Replay command loads game structure and binds target

**NOT VERIFIED**

No CLI replay command implementation reviewed.

### FR-009: Replay presents summary and asks confirmation

**NOT VERIFIED**

CLI-layer concern.

### FR-010: Replay with parameter adjustment

**NOT VERIFIED**

CLI-layer concern.

### FR-011: Replayed run appended to history

**MET (by design)**

The same `append_run()` mechanism applies to replayed runs. The plugin would be triggered at POST_DELIBERATION regardless of whether the run was original or replayed.

### FR-012: List scenarios command

**NOT VERIFIED**

CLI command not implemented. `FileScenarioStore.list_scenarios()` provides the data layer.

### FR-013: Scenario detail display

**NOT VERIFIED**

CLI-layer concern.

### FR-014: Human-readable YAML

**MET**

`yaml.dump(data, default_flow_style=False, sort_keys=False)` produces block-style YAML. Test `test_yaml_file_is_human_readable` verifies `name: caching-decision` and `mode: cooperative` appear in plain text.

### FR-015: Self-contained files

**MET**

Scenario files contain all game structure data inline. Objective template is referenced by name (string), not path. No external file references.

### FR-016: Run history append-only

**MET**

`append_run()` creates a new Scenario with `[*old_history, new_record]`. Frozen models prevent in-place modification. Manual YAML editing is the only way to modify history.

### FR-017: Cross-run analysis with 3+ runs

**NOT IMPLEMENTED**

No analysis computation exists. No `--analysis` flag or method.

### FR-018: Analysis computed at display time

**NOT APPLICABLE** (FR-017 not implemented)

### FR-019: ScenarioStore protocol

**MET**

`ScenarioStore` is a `Protocol` with `runtime_checkable`. Methods: `save`, `load`, `list_scenarios`, `append_run`, `delete`. `FileScenarioStore` implements all methods. Test verifies protocol compliance.

---

## Success Criteria

### SC-001: Save WTA scenario with null bindings

**MET**

Test `test_execute_writes_scenario_yaml` saves a cooperative scenario. While not WTA specifically, the mechanism is mode-agnostic. `DataBindings()` defaults to null. The save + null-bindings behavior is verified.

### SC-002: Replay generates valid conversus.yml

**NOT VERIFIED**

No replay command implementation.

### SC-003: Analysis after 3 replays

**NOT IMPLEMENTED**

FR-017 not implemented.

### SC-004: Human-readable YAML passes validation

**MET**

`test_yaml_file_is_human_readable` + `test_save_and_load_round_trip` verify YAML is readable and validates via Pydantic.

### SC-005: Equilibrium score in history

**MET**

`RunRecord.equilibrium_score: float | None`. Test `test_scenario_with_equilibrium_score_in_history` verifies: score present when provided (0.92), None when omitted.

---

## Constraints Compliance

| Constraint | Status |
|-----------|--------|
| Must NOT require database | MET -- file-based only |
| Must NOT build sharing infrastructure | MET -- git handles distribution |
| Must NOT couple to plugins | MET -- equilibrium_score is optional |
| Must NOT modify historical entries | MET -- frozen models, append-only |

---

## Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-001 | MET | |
| FR-002 | MET | |
| FR-003 | MET | |
| FR-004 | NOT VERIFIED | CLI layer |
| FR-005 | NOT VERIFIED | CLI layer |
| FR-006 | MET | |
| FR-007 | MET | |
| FR-008 | NOT VERIFIED | CLI layer |
| FR-009 | NOT VERIFIED | CLI layer |
| FR-010 | NOT VERIFIED | CLI layer |
| FR-011 | MET (by design) | |
| FR-012 | NOT VERIFIED | CLI layer |
| FR-013 | NOT VERIFIED | CLI layer |
| FR-014 | MET | |
| FR-015 | MET | |
| FR-016 | MET | |
| FR-017 | **NOT IMPLEMENTED** | No analysis |
| FR-018 | N/A | |
| FR-019 | MET | |
| SC-001 | MET | |
| SC-002 | NOT VERIFIED | |
| SC-003 | NOT IMPLEMENTED | |
| SC-004 | MET | |
| SC-005 | MET | |

Note: Many FRs are NOT VERIFIED because they pertain to CLI commands (save, replay, scenarios) which are not part of the plugin implementation under review. The data layer (models, storage, plugin) is well-implemented.
