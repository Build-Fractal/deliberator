# Spec Compliance — Round 1 Review

## Assessment Scope

Auditing all functional requirements (FR-001 through FR-012) and success criteria (SC-001 through SC-005) from `specs/028-mode-expansion/spec.md` against the current implementation.

---

## Functional Requirements

### FR-001: Each new mode MUST have a complete template set (review, cross-review, revision, disputes, synthesis, arbitration).

**MET.**

All 4 new modes have 7 templates each in their respective `templates/` directories:

| Mode | review | cross-review | revision | disputes | synthesis | arbitration | cross-round-synthesis |
|------|--------|-------------|----------|----------|-----------|------------|----------------------|
| negotiation | YES | YES | YES | YES | YES | YES | YES |
| resource-allocation | YES | YES | YES | YES | YES | YES | YES |
| fair-division | YES | YES | YES | YES | YES | YES | YES |
| mechanism-design | YES | YES | YES | YES | YES | YES | YES |

Note: The spec lists 6 required templates. The implementation includes a 7th (`cross-round-synthesis`) which is part of the multi-round infrastructure. This exceeds the requirement.

### FR-002: The mode-mapping (schema/game-forms/mode-mapping.yml) MUST be updated.

**MET.**

`schema/game-forms/mode-mapping.yml` contains entries for all 4 new modes:
- `negotiation: form: bayesian`
- `resource-allocation: form: coalitional`
- `fair-division: form: coalitional`
- `mechanism-design: form: mechanism-design`

Each entry includes a `solver` field (all `nashopt`) and a `note` field explaining the mapping rationale.

### FR-003: VALID_MODES in engine/config.py and conversus/schemas/objectives.py MUST be updated.

**MET.**

`engine/config.py` line 82-91:
```python
VALID_MODES = (
    "cooperative", "winner-take-all", "prisoners-dilemma", "red-blue",
    "negotiation", "resource-allocation", "fair-division", "mechanism-design",
)
```

`conversus/schemas/objectives.py` line 30-39:
```python
VALID_MODES: frozenset[str] = frozenset({
    "cooperative", "winner-take-all", "prisoners-dilemma", "red-blue",
    "negotiation", "resource-allocation", "fair-division", "mechanism-design",
})
```

Both contain all 8 modes. The `engine/config.py` uses a tuple (ordered), while `objectives.py` uses a frozenset (unordered). Both are valid representations. The `AssembledObjective.validate_assembled()` method in `construction.py` validates against the `objectives.py` `VALID_MODES`, so the chain is complete.

### FR-004: The decision type classifier (spec 014) MUST route new problem types to new modes.

**MET.**

`conversus/schemas/construction.py` contains:
- `DecisionType` enum with all 8 types including `NEGOTIATION`, `RESOURCE_ALLOCATION`, `FAIR_DIVISION`, `MECHANISM_DESIGN` (lines 60-74).
- `_DECISION_TYPE_PATTERNS` with regex patterns for all 8 types (lines 78-120).
- `_DECISION_TYPE_MODE` mapping all 8 decision types to their modes (lines 123-132).

### FR-005: /conversus mode MUST include new modes in its recommendation matrix.

**PARTIALLY MET.**

The `engine/config.py` `VALID_MODES` tuple includes all 8 modes, which means any mode validation will accept them. However, I cannot verify the `/conversus mode` CLI command implementation directly from the target files provided. The `_DECISION_TYPE_MODE` mapping in `construction.py` routes new types to new modes, which the CLI command presumably uses. Marking as PARTIALLY MET pending verification of the CLI command itself.

### FR-006: New decision types MUST be added: negotiation, resource_allocation, fair_division, mechanism_design.

**MET.**

The `DecisionType` enum in `construction.py` contains:
- `NEGOTIATION = "NEGOTIATION"`
- `RESOURCE_ALLOCATION = "RESOURCE_ALLOCATION"`
- `FAIR_DIVISION = "FAIR_DIVISION"`
- `MECHANISM_DESIGN = "MECHANISM_DESIGN"`

### FR-007: Heuristic mode detection MUST recognize keywords for each new type.

**MET.**

`_DECISION_TYPE_PATTERNS` in `construction.py` includes regex patterns for all 4 new types:
- `DecisionType.NEGOTIATION`: negotiat, bargain, deal, contract with, ZOPA, BATNA, counter-offer, mutual accept, terms of, settle
- `DecisionType.RESOURCE_ALLOCATION`: allocat, distribut, budget, resource pool, capacity, headcount, assign resource, fair share, ration
- `DecisionType.FAIR_DIVISION`: fair divis, envy free, valuat, split fairly, cake cut, proportional share, subjective value, divide among
- `DecisionType.MECHANISM_DESIGN`: mechanism design, incentive compat, truthful, auction design, VCG, game the system, rule design, strategyproof

### FR-008: Each mode's synthesis template MUST define mode-specific dispute headings for the Dispute-Parsing Subsystem.

**MET.**

Each synthesis template uses a distinct dispute heading within DISPUTES markers:
- Negotiation: `### Unresolved Terms` with `**Term:` entry pattern
- Resource-allocation: `### Contested Allocations` with `**Contested:` entry pattern
- Fair-division: `### Disputed Valuations` with `**Disputed:` entry pattern
- Mechanism-design: `### Mechanism Vulnerabilities` with `**Vulnerability:` entry pattern

These match the `schema/modes/*.yml` definitions exactly.

### FR-009: Each mode's arbitration template MUST define mode-specific required headings.

**MET.**

Each `schema/modes/*.yml` defines `arbitration.required_headings`:
- Negotiation: Process Note, Decision Framework, Binding Decisions, Summary of Required Terms
- Resource-allocation: Process Note, Decision Framework, Binding Decisions, Final Allocation Table
- Fair-division: Process Note, Decision Framework, Binding Decisions, Final Allocation
- Mechanism-design: Process Note, Decision Framework, Binding Decisions, Summary of Mechanism Changes Required

Each also defines `influence_headings` for `recommended` and `advisory` influence levels.

### FR-010: The linter (linter/validate.py) MUST validate templates for new modes.

**PARTIALLY MET.**

The `schema/modes/*.yml` files define the validation rules (expected templates, dispute headings, structural markers, arbitration headings) for all 4 new modes. However, I have not directly examined `linter/validate.py` to confirm it loads and applies these schemas. The infrastructure is in place via the schema files, but linter implementation verification requires examining `linter/validate.py`, which is not among the target files.

### FR-011: Existing 4 modes MUST work identically.

**NOT VERIFIABLE FROM TARGETS.**

No changes were made to existing mode templates (cooperative, winner-take-all, prisoners-dilemma, red-blue) based on the target files. The `VALID_MODES` additions in `config.py` and `objectives.py` are additive (new entries appended/added to set). The `_DECISION_TYPE_PATTERNS` additions are also additive (new entries in the dict). No existing pattern was modified.

**Risk SC-R1-01**: The keyword classifier in `classify_decision_type()` uses match count to break ties. Adding 4 new decision types increases the chance that a problem text with general language matches multiple types. If a previously unambiguous SELECTION classification now ties with NEGOTIATION due to shared keywords like "deal," the classifier's behavior changes. This is testable but no tests exist (`test_mode_expansion.py` is empty).

### FR-012: Existing configs with the original 4 modes MUST NOT be affected.

**MET by code inspection.**

The `parse_config()` function in `engine/config.py` validates mode against `VALID_MODES`, which is a superset of the original 4. No validation logic was changed — only the set was expanded. Existing configs specifying `mode: cooperative` (etc.) will parse identically.

---

## Success Criteria

### SC-001: /conversus mode recommends negotiation for "We need to negotiate a contract with our vendor."

**MET by code inspection.**

`classify_decision_type("We need to negotiate a contract with our vendor.")` will match:
- NEGOTIATION: "negotiat" matches "negotiate" (1 match), "contract\s+with" matches "contract with" (1 match) = 2 matches
- No other type's keywords are present in this text

The function returns `DecisionType.NEGOTIATION`, which maps to mode `"negotiation"` via `_DECISION_TYPE_MODE`.

### SC-002: A resource allocation deliberation produces an allocation table with Shapley fairness scores.

**MET by template design.**

The `templates/resource-allocation/synthesis.md` template requires:
- "### Allocation Table" section with a resource-by-agent table
- "### Fairness Analysis" section with "**Shapley Value Assessment**" and a Shapley value table
- "**Envy Analysis**" and "**Efficiency Score**"

The template structurally enforces this output.

### SC-003: A mechanism design deliberation produces a rule set with an incentive compatibility analysis.

**MET by template design.**

The `templates/mechanism-design/synthesis.md` template requires:
- "### Mechanism Specification" section with "**Mechanism Rules**"
- "**Incentive Compatibility Guarantee**"
- "### Property Assessment Matrix" including incentive compatibility row
- "**Gaming Vulnerability Report**"

### SC-004: len(VALID_MODES) >= 8 after implementation.

**MET.**

`engine/config.py` `VALID_MODES` contains exactly 8 entries. `conversus/schemas/objectives.py` `VALID_MODES` contains exactly 8 entries. `len(VALID_MODES) == 8 >= 8`.

### SC-005: All existing tests pass unchanged (backward compatibility).

**NOT VERIFIABLE.**

`tests/test_mode_expansion.py` is empty. No test run was performed. This criterion requires executing the test suite, not just inspecting code.

---

## Compliance Summary

| Requirement | Status |
|------------|--------|
| FR-001 | MET |
| FR-002 | MET |
| FR-003 | MET |
| FR-004 | MET |
| FR-005 | PARTIALLY MET (CLI not in target files) |
| FR-006 | MET |
| FR-007 | MET |
| FR-008 | MET |
| FR-009 | MET |
| FR-010 | PARTIALLY MET (linter not in target files) |
| FR-011 | NOT VERIFIABLE (no tests) |
| FR-012 | MET |
| SC-001 | MET |
| SC-002 | MET |
| SC-003 | MET |
| SC-004 | MET |
| SC-005 | NOT VERIFIABLE (no tests) |

**Overall**: 12/17 MET, 2/17 PARTIALLY MET, 3/17 NOT VERIFIABLE.

### Recommendations

1. **P1 — Must**: Populate `tests/test_mode_expansion.py` with tests covering FR-011, FR-012, SC-004, and SC-005. Without tests, 3 requirements remain unverifiable.

2. **P1 — Must**: Verify FR-005 and FR-010 by examining the CLI mode command and linter implementation respectively.

3. **P2 — Should**: Add regression tests that the keyword classifier still correctly classifies the original 4 decision types after the 4 new patterns are added (addresses risk SC-R1-01).
