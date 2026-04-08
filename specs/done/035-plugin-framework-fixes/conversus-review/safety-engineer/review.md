# Plugin Framework Review — Phase 1

**Agent**: safety-engineer
**Spec**: 035-plugin-framework-fixes
**Date**: 2026-04-01
**Files reviewed**: base.py, test_cross_plugin.py, test_plugins.py

---

## Executive Summary

The plugin framework has good error isolation: plugin exceptions are caught and logged, not propagated. The DuplicateProducerError and missing-produces warning add important safety rails. Two error-handling gaps remain.

---

## Findings

### F-1: DuplicateProducerError is correctly fail-fast [HIGH — H-3]

**Location**: base.py:341-346
**Status**: CORRECT

The error is raised during topological sort (before execution), not during plugin loading. This is the correct ordering — catching collisions at wire-time prevents ambiguous runtime behavior.

**Edge case**: If two plugins produce the same key but are registered for DIFFERENT hooks, they will never collide in `_topological_sort_plugins` because the function filters by hook first (line 467). This is correct behavior — producing the same key at different lifecycle points is valid.

**Verdict**: H-3 MET.

### F-2: Missing-produces warning is non-fatal [MEDIUM — NEW-5 / D-2]

**Location**: base.py:491-499
**Status**: CORRECT

Warning-only is the right safety level. A hard error would make the framework brittle. Producers may legitimately skip emitting a key (e.g., error paths, conditional data).

**Concern**: The warning goes to the logger only. If the consumer plugin reads the missing key from `plugin_results`, it gets `None` silently. The consumer has no way to distinguish "producer ran but chose not to emit" from "producer was not registered at all."

**Recommendation**: Add a sentinel value (e.g., `PLUGIN_KEY_NOT_EMITTED`) to distinguish these cases. P3 — no current bug, but would improve debuggability.

### F-3: Exception isolation in execute_hooks [HIGH — existing]

**Location**: base.py:519-525
**Status**: CORRECT

The `except Exception` in `execute_hooks` catches all plugin failures and continues with the next plugin. This is correct for fault isolation. However:

1. The exception is logged with `exc_info=True` (good — full traceback).
2. The failed plugin's `produces` keys are NOT populated in `plugin_results`. This means consumers of a failed producer will get `None` — same as if the producer was never registered.
3. No mechanism exists to signal to consumers that their dependency failed (vs. was absent).

**Recommendation**: After a plugin fails, add a `_plugin_errors` entry to `plugin_results` so consumers can detect the failure. P3 — no current bug, defense in depth.

### F-4: Shallow copy in model_copy [MEDIUM — related to NEW-4]

**Location**: base.py:482-484
**Status**: KNOWN LIMITATION

```python
current_state = state.model_copy(update={"plugin_results": plugin_results})
```

`model_copy` with `update` performs a shallow copy. If `plugin_results` contains mutable values (lists, dicts), mutations by a later plugin could affect earlier plugins' views. Currently all values are immutable (floats, strings, booleans), so no bug exists.

**Verdict**: NEW-4 is correctly deferred. No current risk.

### F-5: Cross-hook scoping test gap [MEDIUM — M-2]

**Location**: test_cross_plugin.py
**Status**: NEEDS TEST

The test file covers topological sort and single-hook execution. Missing: a test where:
1. Hook A executes plugins, producing results
2. Hook B executes with fresh state
3. Assert results from A are NOT in B's plugin_results

This is the explicit M-2 test required by the spec.

**Priority**: P2.

### F-6: Plugin loading silently skips broken packages [OBSERVATION]

**Location**: base.py:262-294
**Status**: By design

If a plugin package fails to import, `load_plugins` logs a warning and continues. This is correct for optional plugins but means a required plugin that fails to install will be silently missing. There is no concept of "required" vs. "optional" plugins.

**Priority**: P3 — suggest adding a `required: bool` flag to plugin config entries.

---

## Safety Assessment

| Category | Rating |
|---|---|
| Fail-fast on wiring errors | GOOD (DuplicateProducerError) |
| Fault isolation during execution | GOOD (exception caught + logged) |
| Consumer safety (missing data) | FAIR (None silently, no sentinel) |
| Type safety (produced values) | FAIR (Any, no typed contracts) |
| Test coverage for safety invariants | NEEDS IMPROVEMENT (M-2 test missing) |
