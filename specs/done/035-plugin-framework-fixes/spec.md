# Feature Specification: Plugin Framework Fixes

**Feature ID**: `035-plugin-framework-fixes`
**Created**: 2026-04-01
**Status**: Draft
**Files**: `conversus/plugins/base.py`, `tests/test_cross_plugin.py`, `tests/test_plugins.py`

---

## Items (5)

### HIGH
- **H-3**: DuplicateProducerError. Two plugins declaring same `produces` key silently shadow. base.py:333-336 overwrites without warning. Raise dedicated error.
- **D-2**: Producer key validation. Plugin declares `produces=["foo"]` but execute() never puts "foo" in result.data. Consumer gets None silently. Fix: warn after execute() if declared produces keys are missing.

### MEDIUM
- **M-2**: Cross-hook plugin_results scoping test. `plugin_results` resets per hook invocation. Undocumented, untested. Add test + docstring.
- **NEW-5**: Log warning when plugin declares produces but omits key from result.data (lighter version of D-2 — warn not error).

### DEFERRED
- **D-3**: Typed contracts for produced values. `plugin_results` is `dict[str, Any]`. Track for spec 032 (package splitting) when plugin boundaries harden.
- **NEW-4**: Immutable types enforcement. `model_copy` is shallow; mutable values can leak. No bug today — all current values are immutable floats/strings.

## Success Criteria
- SC-001: Two plugins with same produces key raise DuplicateProducerError.
- SC-002: Plugin declaring produces=["foo"] but not emitting it triggers logged warning.
- SC-003: plugin_results from hook A not visible in hook B (scoping test passes).
