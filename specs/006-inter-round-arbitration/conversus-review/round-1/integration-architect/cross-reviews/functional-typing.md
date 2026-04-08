# Cross-Review: integration-architect reviewing functional-typing

## Dangerous Contradictions

None identified. The functional-typing recommendations target the type system and linter internals, which are compatible with integration-architect's template wiring and schema completeness concerns. No recommendation from either agent would break the other's proposals.

## Tensions

### T1: Phase Enum in validate.py -- Correctness vs. Practical Impact

**functional-typing** ranks using `Phase` enum in `validate.py` as P1 (Rec 1), citing Constitution Principle IX's mandate for StrEnum in closed behavioral choices.

**integration-architect** did not identify this as a gap. From an integration perspective, the phase string comparisons in `validate.py` are internal to the linter and do not affect template wiring, runtime behavior, or schema correctness. The risk of a string typo in a well-tested linter function is low. A P1 ranking seems high for what is effectively a code quality improvement with no behavioral impact.

The tension is about P1 scope: functional-typing treats constitution compliance as inherently P1; integration-architect reserves P1 for gaps that affect correctness of the orchestrated output. Both are valid prioritization frameworks. For spec 006 specifically, the integration-architect would suggest P2 for this item since the linter is not broken -- it just uses strings where it could use enums.

### T2: config_conditions Evaluation in the Linter

**functional-typing** recommends (Rec 5, P2) implementing config_conditions evaluation in the linter, or at minimum documenting that they are metadata-only.

**integration-architect** identifies a related but distinct concern: `ARBITRATION_RULINGS` should be `required: true` with a config_conditions gate (Rec 9, P3). This recommendation implicitly assumes config_conditions WILL be evaluated eventually -- otherwise making a variable `required: true` with a condition is no different from `required: false`.

The tension: functional-typing wants the evaluation mechanism now (or documented as absent); integration-architect wants the data correct (required status) and implicitly assumes the mechanism will follow. Both are right -- the data should be correct AND the mechanism should either exist or be documented as missing. The practical resolution is: fix the required status (integration-architect Rec 9), document that config_conditions are not yet evaluated (functional-typing Rec 5 minimum variant), and plan the evaluation mechanism for a future spec.

### T3: ErrorType Reclassification Priority

**functional-typing** identifies semantic misuse of ErrorType members for non-variable errors (Rec 3, P2) and proposes new enum members.

**integration-architect** did not identify this gap. From an integration perspective, the error type misclassification is internal to the linter's error reporting and does not affect template generation, agent behavior, or output correctness. It would matter if consumers filtered errors by type, but the current system presents all errors in a flat list.

No disagreement that the reclassification is correct -- only that P2 may be high for a linter-internal issue with no downstream behavioral impact. integration-architect would rank this P3.

## Safe Agreements

### SA1: Influence-Aware Heading Data in ArbitrationConfig
Both agents propose adding influence-aware heading data to the `ArbitrationConfig` model. functional-typing's `dict[InfluenceLevel, list[str]]` field matches integration-architect's `influence_headings` YAML structure. Both rank this P1.

### SA2: PRIOR_ARBITRATION_SECTION / PATH Distinction Needs Documentation
functional-typing's Rec 8 (model_validator on ReviewContext) and integration-architect's Rec 5 (inline comment on ReviewContext) both address the subtle SECTION-vs-PATH distinction. functional-typing proposes enforcement; integration-architect proposes documentation. Both are complementary -- document the distinction AND enforce the constraint.

### SA3: Pydantic Immutability and Frozen Models Are Correct
Both agents validate the `frozen=True` and `extra: "forbid"` configuration on Pydantic models. functional-typing cites FP immutability principles; integration-architect cites the practical benefit that `extra: "forbid"` prevents silent field drops when schemas evolve.

### SA4: Backward Compatibility Is Preserved
Both agents confirm that default values (`timing: final`, `influence: binding`) produce pre-spec-006 behavior. The implementation correctly handles the omitted-config case.

### SA5: The Linter Cannot Statically Validate Influence-Dependent Headings
functional-typing's Off-Base Assumption 2 and integration-architect's Off-Base Assumption 1 reach the same conclusion: the linter validates templates before runtime config is known, so influence-adjusted headings must be validated at the orchestrator level. Both agree this is an intentional architectural boundary, not a bug.
