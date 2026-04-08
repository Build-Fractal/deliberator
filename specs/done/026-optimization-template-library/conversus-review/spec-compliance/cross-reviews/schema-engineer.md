# Cross-Review: spec-compliance reviewing schema-engineer

**Spec**: 026-optimization-template-library

---

## Dangerous Contradictions

None. The schema-engineer's structural findings are accurate and consistent with the compliance assessment.

---

## Tensions

### T1: SE-2 (game_form cross-validation) severity -- Low is correct

- **schema-engineer's position**: Rates game_form cross-validation gap as Low (SE-2). A template with `game_form: nonexistent` would pass all tests.
- **spec-compliance's position**: I agree with Low. The fix is a single parametric test. The current risk is zero (all values are valid today). The future risk is real but bounded (a contributor adding a template would likely copy an existing one, preserving a valid game_form value). Low captures the right urgency: fix it before the library grows significantly, but it is not blocking.
- **Nature**: Agreement.

### T2: SE-1 (constraint count fragility) -- Info is correct but worth monitoring

- **schema-engineer's position**: Flags constraint count at exact threshold (10/10) as Info.
- **spec-compliance's position**: I agree with Info. The test correctly implements SC-002 as written (`>= 10`). The threshold is a spec-level decision. If the library grows and constraints are added, the threshold will be exceeded naturally. If a constraint is accidentally removed, the test will catch it -- which is the *purpose* of the threshold test.

  However, I note a subtle risk: the "new constraints" in this spec (integrality, cardinality, precedence, flow-conservation) are *referenced* by the new templates. If one of these constraint files is deleted, two tests would fail simultaneously: SC-002 (count < 10) and `TestTemplateConstraintReferences` (broken reference). The reference test provides a stronger signal than the count test in this scenario.
- **Nature**: Minor framing difference. Both tests serve distinct purposes: count threshold tests SC-002 compliance, reference tests catch broken links.

### T3: SE-3 (mode_compatibility validation) -- align with my observation

- **schema-engineer's position**: Flags mode_compatibility values not validated against known mode set as Info (SE-3).
- **spec-compliance's position**: I independently identified the same gap in my review. I rate it the same as game_form cross-validation (Low) because the fix is identical in pattern: a parametric test that cross-references values against a source-of-truth file. The schema-engineer rates it Info, one notch lower. The difference is minor and depends on how much weight you give to the "consistent severity for parallel gaps" argument vs. the "mode_compatibility has fewer valid values so typos are less likely" argument.
- **Nature**: Minor severity disagreement. Low vs. Info for mode_compatibility validation.

---

## Safe Agreements

1. **All 15 templates follow the YAML schema**: Both agents verify structural compliance. The schema-engineer's field-by-field audit table is a strong evidence artifact.

2. **gap_question completeness is verified**: The schema-engineer's parameter-by-parameter audit of 5 sample templates confirms the test's findings. All 15 non-derived parameters across the samples have gap_question fields.

3. **Constraint references are all valid**: The schema-engineer's reference map shows every constraint reference resolves. This is critical for template correctness.

4. **New constraint templates follow the ConstraintTemplate schema**: Both agents agree the 4 new constraints are well-formed.

5. **Test suite provides comprehensive parametric validation**: Both agents agree the test organization maps cleanly to spec requirements.

---

## Additions from spec-compliance perspective

### A1: game_form and mode_compatibility should be validated together

The schema-engineer flags game_form (Low) and mode_compatibility (Info) as separate concerns. I argue they should be addressed together because:

1. Both are cross-reference validation gaps against source-of-truth YAML files
2. Both can be fixed with the same test pattern (parametric test over templates, check value against glob of valid files/keys)
3. Addressing one without the other leaves an asymmetric validation surface

Recommendation: Bundle both into a single "cross-reference validation" work item with two test additions.

### A2: Constraint template gap_question coverage

The schema-engineer notes that constraint templates have parameters with gap_question fields (e.g., flow-conservation has `supply_demand` with a gap_question). However, the `TestGapQuestions` class only tests *objective* templates, not constraint templates. If a constraint template's parameter is missing a gap_question, no test would catch it.

This is a coverage gap in the test suite. The constraint templates currently all have gap_questions where applicable, but the invariant is unenforced for constraints. The fix: add a `TestConstraintGapQuestions` class that mirrors `TestGapQuestions` but operates on constraint YAML files.

### A3: Template count margin

The schema-engineer notes 36 templates vs. the 35 threshold (1 margin). I count from the directory listing: there are 36 files in `schema/objective-functions/` matching `*.yml`. The spec expected ~20 existing + 15 new = 35. The extra file suggests either the spec underestimated existing templates or one template was added outside this spec. Either way, the margin is thin. Future template additions will naturally increase the margin, so this is not actionable.
