# Mode & Template Review — Phase 1

**Agent**: classification-engineer
**Spec**: 036-mode-template-fixes
**Date**: 2026-04-01
**Files reviewed**: construction.py, modes.py, config.py, test_mode_expansion.py

---

## Executive Summary

The keyword classification system for 8 decision types is well-implemented with clear regex patterns and comprehensive tests. The ration regex fix is correct. One edge case in the classification tie-breaking logic deserves attention.

---

## Findings

### F-1: Regex patterns cover all 8 decision types [HIGH]

**Location**: construction.py:78-120
**Status**: CORRECT

Each DecisionType has a compiled regex pattern in `_DECISION_TYPE_PATTERNS`. Patterns use:
- Word boundaries (`\b`) where needed to prevent substring matches
- `re.IGNORECASE` for case-insensitive matching
- Alternation (`|`) for multiple keyword variants

All 8 types have non-trivial patterns with 3+ keyword variants.

### F-2: ration regex fix is correct [HIGH — H-1]

**Location**: construction.py:105-109
**Status**: CORRECT

The RESOURCE_ALLOCATION pattern starts with `\bresource.?allocat` instead of the old `ration`. This prevents "rational" and "irrational" from matching. The test suite (TestRationRegexFix) explicitly verifies this with 5 tests.

**Edge case verified**: "resource-allocation" matches (the `.?` handles the hyphen). "resource allocation" matches (the `.?` handles the space). "resourceallocation" matches (the `.?` allows zero characters). All correct.

### F-3: Classification tie-breaking [OBSERVATION]

**Location**: construction.py:424-425
**Status**: CORRECT but fragile

```python
return max(scores, key=lambda dt: (scores[dt], -list(DecisionType).index(dt)))
```

Ties are broken by enum definition order (earlier = higher priority). This means SELECTION wins ties against INTEGRATION, etc. The ordering is:
1. SELECTION
2. INTEGRATION
3. SCOPING
4. STRESS_TEST
5. NEGOTIATION
6. RESOURCE_ALLOCATION
7. FAIR_DIVISION
8. MECHANISM_DESIGN

This creates a bias toward the original 4 modes over the new 4 modes. If a problem description contains keywords for both SELECTION and NEGOTIATION with equal frequency, SELECTION wins. This is probably intentional (backward compatibility) but undocumented.

**Priority**: P3 — document the tie-breaking bias.

### F-4: Decision type to mode mapping is complete [HIGH]

**Location**: construction.py:123-132
**Status**: CORRECT

`_DECISION_TYPE_MODE` maps all 8 DecisionTypes to their correct modes. TestDecisionTypeModeMapping verifies this with per-type tests.

### F-5: VALID_MODES sources all import from modes.py [HIGH — H-2/M-4]

**Location**: modes.py, features.py:16, config.py:19
**Status**: CORRECT

Single canonical source. TestValidModesConsistency has 10 tests verifying this, including the three-way equality assertion.

---

## Classification Quality Assessment

| Decision Type | Pattern Quality | Test Coverage |
|---|---|---|
| SELECTION | Good — 7 variants | 2 tests |
| INTEGRATION | Good — 7 variants | 1 test |
| SCOPING | Good — 6 variants | 1 test |
| STRESS_TEST | Good — 7 variants | 1 test |
| NEGOTIATION | Good — 6 variants | 3 tests |
| RESOURCE_ALLOCATION | Good — 5 variants (ration removed) | 5 tests |
| FAIR_DIVISION | Good — 6 variants | 2 tests |
| MECHANISM_DESIGN | Good — 6 variants | 3 tests |

All patterns have adequate keyword coverage.
