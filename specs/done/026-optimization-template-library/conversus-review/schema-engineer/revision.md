# Phase 3 Revision: schema-engineer

**Spec**: 026-optimization-template-library

---

## Position Changes After Cross-Review

### Modified: SE-2 (game_form cross-validation) -- MAINTAINED as Low

- **Original position**: Low. game_form values not cross-validated against game-forms/*.yml.
- **Cross-review input**: optimization-engineer independently flagged the same gap (OE-3, also Low). spec-compliance agrees with Low. All three agents converge.
- **Disposition**: Surviving. Unanimous on both the gap and the severity. Fix: one parametric test.

### Modified: SE-3 (mode_compatibility validation) -- UPGRADED from Info to Low

- **Original position**: Info. mode_compatibility values not validated against known mode set.
- **Cross-review input**: spec-compliance argues for Low, reasoning that this is the same class of gap as game_form cross-validation (SE-2/OE-3) and should carry consistent severity. optimization-engineer agrees with Low (OE-4). Two agents at Low, one (me) at Info.
- **Disposition**: Upgraded to Low. The consistency argument is persuasive: both gaps have identical structure (unchecked cross-reference against a source-of-truth file), identical fix pattern (parametric test), and identical risk profile (silent acceptance of invalid values). Assigning different severities to structurally identical gaps creates confusion.

### Surviving: SE-1 (constraint count fragility) -- MAINTAINED as Info

- **Original position**: Info. Constraint count at exact threshold (10/10).
- **Cross-review input**: spec-compliance notes that the reference test (`TestTemplateConstraintReferences`) provides a stronger signal than the count test if a constraint is deleted. optimization-engineer notes the threshold is from the spec, not the test.
- **Disposition**: Surviving at Info. Both cross-review inputs reinforce that the count test serves its purpose (SC-002 compliance checking) even at exact threshold. The reference test provides defense-in-depth.

### New: Constraint template gap_question test coverage (Low)

- **Source**: spec-compliance cross-review of schema-engineer (addition A2).
- **Observation**: `TestGapQuestions` only tests objective templates. Constraint template parameters with gap_questions are not tested.
- **Assessment**: Low. Constraint templates are simpler (fewer parameters) but the invariant should still be enforced.
- **Disposition**: Adopted. Add a `TestConstraintGapQuestions` class mirroring the existing pattern.

### New: Template-to-constraint semantic alignment is verified by expert review (Info)

- **Source**: optimization-engineer cross-review (addition A1).
- **Observation**: The test suite verifies that constraint references resolve to files (structural), but does not verify that the referenced constraints are *mathematically appropriate* for the problem class (semantic). The optimization-engineer's manual review confirms semantic correctness for all 15 templates.
- **Assessment**: Info. Semantic validation of constraint-template alignment requires domain knowledge that cannot be practically automated. The manual review provides sufficient coverage.
- **Disposition**: Adopted as Info. Document the dependency on mathematical review.

---

## Revised Concern Table

| # | Severity | Item | Status |
|---|----------|------|--------|
| SE-1 | Info | Constraint count at exact threshold (10/10) | Surviving |
| SE-2 | Low | game_form values not cross-validated against game-forms/*.yml | Surviving (unanimous) |
| SE-3 | Low | mode_compatibility values not cross-validated against mode-mapping.yml | Upgraded from Info (spec-compliance consistency argument) |
| SE-4 | Low | Constraint template gap_question enforcement missing from tests | New (from spec-compliance) |
| SE-5 | Info | Constraint-template semantic alignment depends on manual review | New (from optimization-engineer) |

---

## Recommendation

**Accept.** Revised from 3 concerns to 5, with SE-3 upgraded from Info to Low. All concerns are test coverage improvements, not schema defects. The template library is structurally sound with complete gap_questions, valid constraint references, and proper schema compliance.
