# Phase 4 Disputes: optimization-engineer

**Spec**: 026-optimization-template-library

---

## Remaining Disputes

### DISPUTE 1: Cross-reference validation for game_form and mode_compatibility (Low)

**Status**: Surviving -- all three agents agree on both the gap and the severity (Low).

Template `game_form` and `mode_compatibility` values are not validated against their respective source-of-truth files (`schema/game-forms/*.yml` and `mode-mapping.yml`). This allows silently invalid references. All current values are valid, but the invariant is unenforced.

**Recommended resolution**: Add two parametric tests:
1. For each template, verify `game_form` value matches a filename in `schema/game-forms/`
2. For each template, verify each `mode_compatibility` value is a key in `mode-mapping.yml` or matches a filename in the modes directory

**Agent consensus**: Unanimous (optimization-engineer OE-3/OE-4, schema-engineer SE-2/SE-3, spec-compliance SC-C4).

### DISPUTE 2: Constraint template gap_question test coverage (Low)

**Status**: Surviving -- all three agents agree.

The `TestGapQuestions` class only tests objective templates. Constraint template parameters with `gap_question` fields are not verified by any test. All current constraint templates have correct gap_questions, but the invariant is unenforced.

**Recommended resolution**: Add a `TestConstraintGapQuestions` class that mirrors `TestGapQuestions` but operates on constraint YAML files.

**Agent consensus**: Unanimous (identified by spec-compliance, adopted by optimization-engineer and schema-engineer in Phase 3).

---

## Withdrawn Disputes

- **PSD validation (OE-1)**: Downgraded to Info in Phase 1, confirmed as Info by all agents. Not a dispute -- it's an inherent limitation.
- **Supply-demand sum-to-zero (OE-2)**: Same as OE-1. Info observation, not actionable.
- **String-encoded matrices (original OE-3 numbering)**: Info architectural observation. No disagreement.
- **form field semantic validation (OE-6)**: Info. Depends on manual review. No disagreement.

---

## Convergence

- **All 15 templates are mathematically correct and schema-compliant**: Unanimous across all three agents from Phase 1 through Phase 4. No agent challenged any formulation or schema compliance finding.
- **SC-004 is PASS**: Unanimous after Phase 3. The initial PARTIAL assessment by spec-compliance was revised to PASS with cross-review input.
- **FR-004 and SC-005 are correctly deferred to other specs**: Unanimous. Both are cross-spec integration concerns.
- **Overall verdict is PASS**: Unanimous. No blocking concerns.
