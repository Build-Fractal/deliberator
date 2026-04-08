# Cross-Review: schema-engineer reviewing spec-compliance

**Spec**: 025-game-form-expansion
**Reviewer**: schema-engineer
**Subject**: spec-compliance Phase 1 review

---

## Verified Claims

### 1. FR compliance matrix is well-structured and accurate

The tabular format with FR ID, requirement text, verdict, and evidence is clear and auditable. I verify:

- FR-001 through FR-003: PASS verdicts are correct. Evidence references specific test classes and YAML files.
- FR-004: PASS verdict is correct (the diagnostic is implemented as check functions, the PotentialGame model is a result container).
- FR-005 through FR-007: PASS verdicts are correct. The note about FR-005 being exceeded (pure Python, no scipy) is accurate.
- FR-011 through FR-013: PASS verdicts with test counts are correct.

### 2. SC-003 and SC-004 deferral is appropriate

The spec-compliance agent correctly identifies these as Tier 2 dependencies. The spec's phased approach means schema-only definitions without solver implementations are expected for Tier 2 forms.

### 3. FR-010 upgrade from NOT ASSESSED to PASS

The spec-compliance agent correctly identifies that integrality.yml and cardinality.yml exist in `schema/objective-functions/constraints/`. This is an improvement over the earlier conversus-output which did not assess FR-010.

---

## Disagreements

### 1. FR-008 / FR-009 should not be "NOT ASSESSED"

The spec-compliance agent defers FR-008 and FR-009 entirely to spec 026. However, FR-008 is a requirement *of this spec* (025):

> FR-008: Each game form MUST have at least one objective template in `schema/objective-functions/`.

The `schema/objective-functions/` directory contains 20+ templates. Some are applicable to new game forms:

- `cooperative-consensus.yml`, `cooperative-fairness.yml`, `cooperative-integration.yml` -- applicable to coalitional games
- `territory-claiming.yml`, `territory-cooperative.yml` -- applicable to congestion games
- `competitive-selection.yml`, `competitive-threshold.yml` -- applicable to mechanism design
- `general-linear.yml`, `general-quadratic.yml` -- applicable broadly

Whether these constitute "dedicated" templates for each new form is debatable, but "NOT ASSESSED" understates the situation. A more accurate verdict would be:

- **FR-008**: PARTIAL -- existing general-purpose templates cover some new forms, but no dedicated per-form templates exist (e.g., no `shapley-attribution.yml` for coalitional games, no `folk-theorem-cooperation.yml` for repeated games).

### 2. SC-005 verdict should be more decisive

I agree with the game-theorist's cross-review position: the spec describes exactly 9 forms + 1 diagnostic. The threshold `>= 10` in the spec text appears to count the potential diagnostic as a form, contradicting FR-004. The implementation correctly has 9 form schemas and a test threshold of `>= 9`.

This should be **PASS with spec amendment** rather than "PARTIAL." The implementation covers every form the spec describes.

---

## Additions

### Structural validation of mode-mapping.yml

The spec-compliance review credits mode mapping via functional tests (lookup returns expected form). It does not assess the structural integrity of mode-mapping.yml itself:

- Each entry should have a `form` key and an optional `note` key
- The `form` value should reference an existing YAML schema in `game-forms/`
- No two entries should map to conflicting forms

The ModeMapping Pydantic model (`ModeFormMapping` with `form: str` and `note: Optional[str]`) provides structural validation. The test `test_total_mappings_count` verifies count but not referential integrity (form values pointing to existing schemas). This is a minor testing gap.

### Test suite organization quality

The spec-compliance review assesses test existence (FR-011) but could credit the organizational quality:

- Each game form has its own test class (easy to locate and extend)
- Parametric tests (`@pytest.mark.parametrize`) avoid repetitive boilerplate for YAML schema validation
- YAML round-trip tests (yaml.safe_load -> model_validate) are included alongside unit tests
- Edge cases (empty resources, invalid cost_type, wrong form literal) are systematically tested

This exceeds the FR-011 requirement of "MUST have Pydantic validation tests."
