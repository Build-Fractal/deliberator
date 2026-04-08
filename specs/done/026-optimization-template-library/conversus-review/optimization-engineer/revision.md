# Phase 3 Revision: optimization-engineer

**Spec**: 026-optimization-template-library

---

## Position Changes After Cross-Review

### Modified: OE-1 (PSD validation) -- MAINTAINED as Info

- **Original position**: Info. PSD constraint not enforceable at template level.
- **Cross-review input**: spec-compliance confirms Info is correct. schema-engineer agrees it's a solver-time concern.
- **Disposition**: Surviving. All three agents agree this is an inherent limitation of the template abstraction layer. No change needed.

### Modified: OE-2 (supply_demand sum-to-zero) -- MAINTAINED as Info

- **Original position**: Info. Feasibility constraint belongs in solver/assembler layer.
- **Cross-review input**: spec-compliance uses the same reasoning as OE-1. Template descriptions correctly document the requirement.
- **Disposition**: Surviving. Unanimous agreement across agents.

### Surviving: OE-3 (game_form cross-validation) -- MAINTAINED as Low

- **Original position**: Low. game_form values not validated against game-forms/*.yml.
- **Cross-review input**: schema-engineer independently flagged the same gap (SE-2, also Low). spec-compliance agrees with Low. All three agents converge on both the gap and the severity.
- **Disposition**: Surviving. Unanimous. The fix is clear: one parametric test.

### Surviving: OE-4 (mode_compatibility cross-validation) -- MAINTAINED as Low

- **Original position**: Low. mode_compatibility values not validated against mode-mapping.yml.
- **Cross-review input**: schema-engineer flagged this as Info (SE-3), one notch lower. spec-compliance argues for Low to maintain consistency with the parallel game_form gap. I side with spec-compliance: both gaps have the same structure (unchecked cross-reference) and the same fix pattern (parametric test). Consistent severity is clearer for prioritization.
- **Disposition**: Surviving at Low. Minor severity disagreement with schema-engineer on SE-3.

### New: Constraint template gap_question test coverage (Low)

- **Source**: spec-compliance cross-review (addition A2).
- **Observation**: The `TestGapQuestions` class only tests objective templates, not constraint templates. Constraint template parameters with gap_question fields are not verified by any test. All current constraint templates have correct gap_questions, but the invariant is unenforced.
- **Assessment**: Low. Same fix pattern as OE-3/OE-4 -- add a `TestConstraintGapQuestions` class.
- **Disposition**: Adopted. The spec-compliance agent identified a genuine test coverage gap.

### New: form field mathematical validity is unautomated (Info)

- **Source**: spec-compliance cross-review (addition A2 in optimization-engineer review).
- **Observation**: No test validates that `form` expressions are mathematically valid. A template with `form: "J = ???"` passes all tests. Mathematical correctness depends entirely on expert review.
- **Assessment**: Info. Mathematical expression parsing is complex and probably not worth automating in the template test suite. The optimization-engineer's manual review covers the current template set. For future templates, the review process should include mathematical review.
- **Disposition**: Adopted as Info. Document the dependency on manual review in the test suite comments.

---

## Revised Concern Table

| # | Severity | Item | Status |
|---|----------|------|--------|
| OE-1 | Info | Portfolio covariance PSD not enforceable at template level | Surviving |
| OE-2 | Info | Network flow supply_demand sum-to-zero not enforceable at template level | Surviving |
| OE-3 | Low | game_form values not cross-validated against game-forms/*.yml | Surviving (unanimous) |
| OE-4 | Low | mode_compatibility values not cross-validated against mode-mapping.yml | Surviving (majority: Low; schema-engineer says Info) |
| OE-5 | Low | Constraint template gap_question enforcement missing from tests | New (from spec-compliance) |
| OE-6 | Info | form field mathematical validity depends on manual review | New (from spec-compliance) |

---

## Recommendation

**Accept.** Revised from 4 concerns to 6, but no concern exceeds Low severity. All formulations remain mathematically correct. The new concerns (OE-5, OE-6) are test coverage improvements, not template defects. The overall verdict is unchanged: the template library is mathematically sound and ready for use.
