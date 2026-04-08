# Feature Specification: Mode & Template Fixes

**Feature ID**: `036-mode-template-fixes`
**Created**: 2026-04-01
**Status**: Draft
**Files**: `conversus/schemas/construction.py`, `engine/config.py`, `conversus/schemas/features.py`, `conversus/schemas/objectives.py`, `templates/`, `tests/test_mode_expansion.py`

---

## Items (6)

### CRITICAL
- **C-1**: Populate test_mode_expansion.py. File is EMPTY. Write tests for: all 8 modes in VALID_MODES, mode mapping entries, template completeness (7 files × 8 modes), DISPUTES markers, DecisionType enum, keyword classification, parse_config acceptance, backward compat. Target: 40+ tests.

### HIGH
- **H-1**: Fix `ration` regex in construction.py. Pattern `ration` matches "rational", "irrational". Fix: use `\bresource.?allocat` or `\bration(?:ing|ed)?\b`.
- **H-2**: VALID_MODES consistency test. Three files define VALID_MODES independently. Add assertion: `set(engine_config.VALID_MODES) == features.VALID_MODES == objectives.VALID_MODES`.

### MEDIUM
- **M-4**: Consolidate VALID_MODES to single canonical source imported by all three files.
- **D-5**: Amend spec 028 Section 2.1 text: "Bayesian + Stackelberg" → "Bayesian" for negotiation mode.
- **RE-5**: Empirical template quality — run at least one deliberation using each new mode template on a real problem.

## Success Criteria
- SC-001: test_mode_expansion.py has 40+ tests.
- SC-002: "rational" is NOT classified as resource_allocation.
- SC-003: VALID_MODES sync test catches a simulated drift.
- SC-004: One deliberation per new mode completes without template errors.
