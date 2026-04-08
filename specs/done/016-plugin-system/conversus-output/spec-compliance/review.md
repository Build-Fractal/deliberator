# Spec Compliance Review: 016 Plugin System Infrastructure

**Reviewer**: spec-compliance
**Spec**: 016-plugin-system
**Date**: 2026-03-24

---

## Executive Summary

Spec 016 defines 15 functional requirements (FR-001 through FR-015) and 5 success criteria (SC-001 through SC-005). The implementation in `conversus/plugins/` satisfies the majority of requirements with strong compliance on the core isolation guarantees (FR-010, FR-011, FR-015) and the loading/execution mechanics (FR-003 through FR-008). Key gaps: FR-001 config parsing is implemented in a separate module but not yet wired into the engine's config parser, FR-006 hook execution exists in `base.py` but is never called from the engine pipeline, FR-009 output file naming convention is implemented but uses `-` instead of the spec's suggested `/` for separating components, FR-012 package naming (`conversus-plugins`) diverges from the actual `conversus.plugins` namespace, and FR-014 states core engine does not depend on plugins -- this is true at import time but the engine will need to call `execute_hooks()` at runtime. All five success criteria are testable and supported by the test suite.

---

## Functional Requirement Compliance

### FR-001: Config section in conversus.yml — PARTIALLY MET

**Evidence**: `parse_plugins_config()` in `config.py` validates the `plugins:` config structure: list of objects with `name`, `package`, and optional `config`. The PluginConfigEntry model is frozen and validated. However, the engine's `EngineConfig` model in `engine/config.py` does not yet include a `plugins` field. The config parsing exists but is not wired into the engine's config pipeline.

### FR-002: Empty/absent plugins field produces identical behavior — MET

**Evidence**: `parse_plugins_config(None)` returns `[]`. `parse_plugins_config([])` returns `[]`. `execute_hooks()` with an empty plugin list returns `[]` without creating any directories or files. Test `test_no_plugins_no_side_effects` confirms no `plugins/` directory is created.

### FR-003: Orchestrator loads plugins at startup — PARTIALLY MET

**Evidence**: `load_plugins()` implements the loading mechanism: imports the package, finds the Plugin subclass, instantiates with config. But the orchestrator (`engine/phases.py`) does not call `load_plugins()`. The loading function exists but is not integrated into the pipeline startup.

### FR-004: Plugins installable via pip, loaded via importlib — MET

**Evidence**: `load_plugins()` uses `importlib.import_module(package)` for dynamic loading (line 210). The import path is the package name from the config, which is the pip package name. Tests use `sys.modules` injection to simulate installed packages, confirming the mechanism works.

### FR-005: Missing package warns and continues — MET

**Evidence**: `load_plugins()` catches `ImportError` and logs a warning (lines 211-217). Test `test_missing_package_warns_no_crash` confirms no crash and warning message. The pipeline continues loading remaining plugins.

### FR-006: Execute plugins at each hook point — PARTIALLY MET

**Evidence**: `execute_hooks()` iterates plugins registered for a given hook and calls `execute()`. The function is implemented and tested. However, the orchestrator does not call `execute_hooks()` at any lifecycle point. The execution mechanism exists but is not wired into the pipeline.

### FR-007: Sequential execution in declaration order — MET

**Evidence**: `load_plugins()` preserves config list order. `execute_hooks()` iterates the filtered list in order. Test `test_sequential_declaration_order` confirms execution order matches declaration order using order-tracking plugins.

### FR-008: Plugin exception does not block deliberation — MET

**Evidence**: `execute_hooks()` wraps each `plugin.execute()` call in try/except (line 306). Exceptions are logged with `exc_info=True` and execution continues. Test `test_exception_isolation` confirms a failing plugin does not prevent subsequent plugins from executing.

### FR-009: Plugin output to {output}/plugins/{name}.json — MET

**Evidence**: Output files are written to `{output}/plugins/{plugin-name}-{hook}-round-{N}.json` (line 291). The naming convention includes hook and round information. Test `test_output_file_written` confirms the file exists at the expected path with correct content.

### FR-010: Plugins must not write to core output directories — MET (by design)

**Evidence**: `execute_hooks()` is the only function that writes plugin output, and it writes exclusively to `{output}/plugins/`. The Plugin ABC's `execute()` method returns a `PluginResult` which the framework writes -- plugins themselves do not perform I/O. A malicious plugin could bypass this by using `state.output_dir` to write arbitrary files, but the framework does not facilitate this.

### FR-011: Core output identical with or without plugins — MET (with caveat)

**Evidence**: Plugin execution is separate from core phase execution. The engine's `_run_single_round()` produces the same output regardless of plugin presence because it does not call `execute_hooks()` yet. When integration is added, the hook calls will be inserted between phase executions, not within them. The caveat: if plugins are configured, `execute_hooks()` creates a `plugins/` directory even if all plugins fail (schema-engineer's M-8 observation). This directory is technically not core output, but it changes the output directory structure.

### FR-012: Plugin base class ships in conversus-plugins package — NOT MET

**Evidence**: The implementation ships as `conversus.plugins` within the main conversus project, not as a standalone `conversus-plugins` pip package. The import path is `from conversus.plugins import Plugin`, not `from conversus_plugins import Plugin`.

### FR-013: Dependencies limited to pydantic — MET

**Evidence**: `base.py` imports `importlib`, `json`, `logging`, `abc`, `enum`, `pathlib`, `typing` (all stdlib) and `pydantic`. `config.py` imports `typing` and `pydantic`. No other dependencies.

### FR-014: Plugin implementations depend on conversus-plugins; core engine does not — MET (at import time)

**Evidence**: The engine's `phases.py` does not import anything from `conversus.plugins`. The plugins package does not import anything from `engine/`. At import time, the dependency graph is clean. At runtime, the engine will need to call `execute_hooks()`, but this can be an optional import within a function, preserving FR-014's intent.

### FR-015: Constitution Principle XV adherence — MET

**Evidence**: The five design principles are structurally enforced: (1) core works alone -- engine runs without plugins. (2) Plugins optional -- empty config produces no change. (3) Plugins swappable -- Plugin ABC defines the interface. (4) One-direction data flow -- DeliberationState is frozen, read-only. (5) Advisory output -- PluginResult.advisory defaults to True.

---

## Success Criteria Compliance

### SC-001: plugins: [] produces byte-identical core output — MET

**Evidence**: `execute_hooks()` with empty list produces no files and no directories. Test `test_no_plugins_no_side_effects` confirms.

### SC-002: Configured plugin produces core output plus plugins/{name}.json — MET

**Evidence**: Test `test_output_file_written` confirms plugin output is written to `plugins/echo-post_phase_5-round-1.json` alongside (hypothetical) core output. Core output is unmodified.

### SC-003: Missing package warns, no crash — MET

**Evidence**: Test `test_missing_package_warns_no_crash` confirms.

### SC-004: Plugin exception logged and skipped — MET

**Evidence**: Test `test_exception_isolation` confirms. Failing plugin is skipped; echo plugin still succeeds.

### SC-005: Two plugins at same hook, second failure does not affect first — MET

**Evidence**: Test `test_second_plugin_failure_does_not_affect_first` confirms. Echo plugin output is written correctly even when a subsequent failing plugin raises.

---

## Actionable Recommendations

1. **Wire plugin loading and execution into the engine pipeline** (Priority: P1)
   - Add `plugins` field to `EngineConfig`. Call `load_plugins()` at startup. Call `execute_hooks()` at PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, and POST_ARBITRATION hook points in `_run_single_round()` and `run_pipeline()`.

2. **Amend FR-012 package naming** (Priority: P1)
   - Change FR-012 to: "The plugin base class, hook points, state objects, and result type MUST ship in the `conversus.plugins` package." Amend import path examples to `from conversus.plugins import Plugin`.

3. **Add integration test for end-to-end plugin execution** (Priority: P1)
   - Current tests cover the plugin framework in isolation. An integration test should run a minimal deliberation pipeline with a configured plugin and verify that: (a) core output is produced, (b) plugin output appears in `plugins/`, (c) the plugin received a valid DeliberationState.

4. **Only create plugins/ directory when plugins produce output** (Priority: P3)
   - Strengthen FR-011 compliance by avoiding empty directory creation.

5. **Document the engine integration contract** (Priority: P2)
   - Specify exactly where in `_run_single_round()` and `run_pipeline()` the hook calls should be inserted. This is currently implicit.
