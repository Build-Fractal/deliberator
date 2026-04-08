# Plugin Framework Review — Phase 1

**Agent**: framework-architect
**Spec**: 035-plugin-framework-fixes
**Date**: 2026-04-01
**Files reviewed**: base.py, test_cross_plugin.py, test_plugins.py

---

## Executive Summary

The plugin framework is well-designed with clear separation between base class, loading, and execution. The spec's 5 items target real gaps in producer/consumer safety. 3 of 5 items are addressed in code; 2 are deferred by design.

---

## Findings

### F-1: DuplicateProducerError [HIGH — H-3]

**Location**: base.py:307-308 (class), base.py:341-346 (enforcement)
**Status**: IMPLEMENTED

`DuplicateProducerError` is raised in `_topological_sort_plugins` when two plugins declare the same `produces` key. The error message includes both plugin names.

**Assessment**: Clean implementation. The error is raised at sort time (before any plugin executes), which is correct — fail fast at wiring time, not at execution time.

**Verdict**: H-3 is resolved. SC-001 is achievable.

### F-2: Producer key validation / missing produces warning [HIGH — D-2, MEDIUM — NEW-5]

**Location**: base.py:491-499
**Status**: IMPLEMENTED (as warning)

After each plugin executes, `execute_hooks` iterates the plugin's `produces` list and checks whether each key is present in `result.data`. If missing, a warning is logged:
```python
logger.warning("Plugin '%s' declares produces=['%s'] but did not emit it", ...)
```

This implements NEW-5 (warn, not error). D-2 (error) is not implemented — the framework logs a warning but does not raise. This is the correct design choice: erroring on a missing key would make the framework brittle. A producer might legitimately not emit a key in certain conditions (e.g., scorer returns error data without eq_score).

**Verdict**: NEW-5 MET. D-2 partially met (warn instead of error, by design). SC-002 is achievable.

### F-3: Cross-hook plugin_results scoping [MEDIUM — M-2]

**Location**: base.py:429-432 (docstring), base.py:477-478 (implementation)
**Status**: DOCUMENTED + IMPLEMENTED

The `execute_hooks` docstring explicitly states:
> "plugin_results is accumulated per invocation of this function (i.e., per hook point). Results from one hook invocation are not carried over to the next."

The implementation starts with `plugin_results = dict(state.plugin_results)` — a shallow copy. Results from previous hooks survive only if the engine passes them in the state.

**Missing**: The test in test_cross_plugin.py should verify that plugin_results from hook A are NOT visible in hook B when called separately. This is the M-2 test.

**Verdict**: M-2 is documented but under-tested. SC-003 needs a dedicated test.

### F-4: Deferred items — typed contracts (D-3) and immutability (NEW-4) [DEFERRED]

**Status**: Correctly deferred.

D-3 (typed contracts for produced values) is tracked for spec 032 (package splitting). NEW-4 (immutable types enforcement) has no current bug — all current values are immutable floats/strings.

**Verdict**: Deferrals are correct and well-documented.

### F-5: API design concern — `produces`/`consumes` are class attributes, not instance [OBSERVATION]

**Location**: base.py:159-160
**Status**: By design

`produces` and `consumes` are class-level attributes (`list[str] = []`). This means they are shared across all instances of a plugin class. If a plugin dynamically changes its produces list (e.g., based on config), the mutation would affect all instances. Currently no plugin does this, but the design invites the error.

**Priority**: P3 — document that `produces`/`consumes` must be class-level constants, not instance-modifiable.

### F-6: `_find_plugin_class` returns first match, not best match [OBSERVATION]

**Location**: base.py:216-226
**Status**: By design

`_find_plugin_class` iterates `dir(module)` and returns the first `Plugin` subclass found. If a module contains multiple Plugin subclasses (e.g., a base class and a concrete class), the alphabetically-first one is returned, which may not be the intended one.

**Priority**: P3 — document that each plugin module should contain exactly one non-abstract Plugin subclass.

---

## Spec Compliance Summary

| Item | Status | Priority |
|---|---|---|
| H-3 (DuplicateProducerError) | IMPLEMENTED | -- |
| D-2 (producer key validation) | IMPLEMENTED (as warning) | -- |
| M-2 (cross-hook scoping test) | DOCUMENTED, needs test | P2 |
| NEW-5 (log warning for missing produces) | IMPLEMENTED | -- |
| D-3 (typed contracts) | DEFERRED to spec 032 | -- |
| NEW-4 (immutable types) | DEFERRED (no bug) | -- |
