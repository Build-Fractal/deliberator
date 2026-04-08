# Cross-Review: schema-engineer reviewing spec-compliance

**Spec**: 026-optimization-template-library

---

## Dangerous Contradictions

None. The spec-compliance agent's FR/SC assessments are accurate and consistent with schema-level findings.

---

## Tensions

### T1: SC-004 initial PARTIAL rating

- **spec-compliance's position**: Initially rated SC-004 as PARTIAL because "the full AssembledObjective assembly is not tested." Later revised to PASS within the same review.
- **schema-engineer's position**: I agree with the revised PASS rating. The ObjectiveTemplate model validates the template including its example section. The AssembledObjective is a downstream construct from spec 014 that takes a validated template and combines it with resolved parameter values and assembled constraints. At spec 026's layer, the template provides valid example data that passes schema validation. The assembly step is spec 014's contract to fulfill.
- **Nature**: Resolved within the spec-compliance review itself. The initial PARTIAL was overly conservative; the revision to PASS is correct.

### T2: FR-004 NOT ASSESSED framing

- **spec-compliance's position**: FR-004 is NOT ASSESSED because it "crosses spec boundaries." Recommends tracking as a cross-spec dependency.
- **schema-engineer's position**: I agree this is not assessable from spec 026 artifacts. However, I note that FR-004 is also a *testability gap* -- there is no test in `test_templates_expanded.py` that exercises the classifier routing. The spec says "MUST be updated," implying an implementation task, but no test verifies the outcome. If a test existed (even a placeholder assertion), it would make the dependency visible in CI.
- **Nature**: Agreement on the assessment, mild tension on whether a placeholder test should exist in spec 026's test suite to surface the dependency.

---

## Safe Agreements

1. **FR-001 through FR-003, FR-005, FR-006 all PASS**: Unanimous across all three agents. Evidence is strong (Pydantic model_validate, parametric tests, manual audits).

2. **SC-001 PASS (count >= 35)**: Verified by test and directory listing. 36 templates exceed the threshold.

3. **SC-002 PASS (count >= 10)**: Verified by test and directory listing. Exactly 10 constraints meet the threshold.

4. **SC-003 and SC-005 correctly deferred**: Both require integration with other specs (014, 023) that are outside spec 026's scope.

5. **Test suite is comprehensive at the schema validation level**: The spec-compliance agent correctly identifies the test structure as thorough for spec 026's requirements.

---

## Additions from schema-engineer perspective

### A1: Test organization quality

The spec-compliance agent cites specific test classes and methods as evidence. I want to highlight that the test organization itself is noteworthy:

- `TestSC001TemplateCount` and `TestSC002ConstraintCount` directly map to success criteria
- `TestSC003NewTemplatesValidate` parametrizes over the exact 15 new templates from the spec
- `TestSC004NewConstraintsValidate` parametrizes over the exact 4 new constraints
- `TestGapQuestions` enforces FR-002 with correct exclusion logic
- `TestTemplateConstraintReferences` enforces constraint reference validity
- `TestAllTemplatesValidate` and `TestAllConstraintsValidate` provide regression coverage for existing templates

This 1:1 mapping between spec requirements and test classes makes compliance auditing straightforward. It is a best practice for spec-driven development.

### A2: mode_compatibility validation gap (reinforcing SC-C2)

The spec-compliance agent flags game_form cross-validation as a concern (via reference to other agents). I want to add that the same gap exists for `mode_compatibility`. The test `test_new_template_has_mode_compatibility` only checks `len >= 1` -- it does not verify that the mode names are valid. A template declaring `mode_compatibility: ["cooperative", "typo-mode"]` would pass all tests.

Two additional parametric tests would close both gaps:
1. `test_game_form_references_valid_game_form_file`
2. `test_mode_compatibility_values_are_valid_modes`
