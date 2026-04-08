# Schema Engineer Revision: 015 Feature Extraction Pipeline

**Reviewer**: schema-engineer
**Revision iteration**: 1
**Date**: 2026-03-24

---

## Recommendation Dispositions

#### Recommendation 1: Refactor AgentFeatures into per-mode discriminated union

- **Original position**: Create separate per-mode models with a discriminator.
- **Disposition**: Modified
- **Explanation**: Extraction-engineer DC-1 correctly identifies the operational cost: all four mode extractors must be rewritten, RoundFeatures type annotation changes, and every test that constructs AgentFeatures needs updating. Spec-compliance DC-1 notes FR-007 is technically met with the flat model. Modified recommendation: stage the refactoring. Phase 1: add a `mode: str | None = None` field to AgentFeatures now (non-breaking, backward-compatible). Phase 2: create per-mode subclasses in a future spec. The `mode` field immediately enables consumers to filter relevant fields, and the subclasses can be introduced without breaking existing code that constructs the base AgentFeatures.

#### Recommendation 2: Add per-mode field validation to FeatureSet

- **Original position**: Model_validator checks agents carry mode-appropriate types.
- **Disposition**: Modified
- **Explanation**: Without per-mode discriminated unions (R-1 deferred), a strict per-mode validator would need to check that mode-specific fields are zero for non-matching modes. This is fragile: it requires the validator to know which fields belong to which mode, duplicating the knowledge that should live in per-mode models. Modified recommendation: add a soft validator that checks `agent_features` is non-empty and that all agents have the same set of non-zero fields (consistency check within a round). This catches bugs where one agent has cooperative features and another has PD features without hardcoding mode-field mappings.

#### Recommendation 3: Deduplicate VALID_MODES into a single canonical location

- **Original position**: Move VALID_MODES to a shared module.
- **Disposition**: Surviving
- **Explanation**: Spec-compliance DC-2 agrees deduplication is correct but low-priority. Extraction-engineer T-1 agrees. No cross-review challenges the recommendation. Priority remains P2 -- the risk is real but not urgent.

#### Recommendation 4: Add AgreementMatrix type alias or model

- **Original position**: Create a semantic type alias or validated model.
- **Disposition**: Surviving
- **Explanation**: Extraction-engineer T-2 agrees this is complementary to their parsing fix. A type alias `AgreementMatrix = dict[str, dict[str, int]]` with a docstring is the minimum change. A validated model with square-matrix invariant is the stretch goal.

#### Recommendation 5: Remove or implement territory_claim_vector and confirmed_count

- **Original position**: Implement or remove declared-but-unpopulated fields.
- **Disposition**: Surviving
- **Explanation**: All three reviews independently flag these fields. Extraction-engineer DC-2 agrees the fields should be implemented since the spec defines them. Spec-compliance R-4/R-5 concur. Implement extraction logic for both fields.

#### Recommendation 6: Create typed FeatureSetMetadata model

- **Original position**: Replace metadata dict with a typed model.
- **Disposition**: Modified
- **Explanation**: Spec-compliance T-2 proposes a compromise: create the model with `extra="allow"` so known fields are typed but unknown fields pass through. This is the right trade-off: discoverability for common fields without blocking extension. Modified recommendation: `FeatureSetMetadata` with `output_dir: str`, `agent_count: int`, `round_count: int`, and `model_config = {"extra": "allow", "frozen": True}`.

#### Recommendation 7: Add `__all__` to features.py

- **Original position**: Define the public API surface explicitly.
- **Disposition**: Surviving
- **Explanation**: Spec-compliance SA-6 agrees. No challenges.

#### Recommendation 8: Generate features.schema.json at build time

- **Original position**: Export JSON Schema for non-Python consumers.
- **Disposition**: Modified
- **Explanation**: Extraction-engineer T-3 correctly notes no non-Python consumer currently exists. Spec-compliance T-1 proposes that JSON Schema could satisfy FR-005's requirement for per-mode schema files. Modified recommendation: generate JSON Schema and use it as the FR-005 artifact. This replaces the YAML schema files spec-compliance identifies as missing, using a machine-generated format that is always in sync with the Pydantic models. Generate per-mode sub-schemas if the discriminated union (R-1 phase 2) is later adopted.

---

## New Recommendations

- **Add `mode` field to AgentFeatures as interim extensibility measure** (Priority: P2)
  - Triggered by: Extraction-engineer DC-1 noting the operational cost of full discriminated-union refactoring.
  - Proposed change: Add `mode: str | None = None` to AgentFeatures. Extraction code sets this field at construction time. Consumers can filter relevant fields by mode.
  - Rationale: Non-breaking, backward-compatible stepping stone toward per-mode subclasses.

---

## Position Summary

Withdrew 0, modified 4, maintained 4. Added 1 new recommendation.

The most significant change is R-1 (discriminated union refactoring), which was staged into two phases based on extraction-engineer's feedback about operational cost. The immediate step (add `mode` field) provides the consumer-facing benefit without the producer-side rewrite. The R-8 modification (JSON Schema as FR-005 artifact) resolves the cross-review tension between spec-compliance's "YAML files are required" and my "Pydantic is sufficient" positions.

My highest-priority surviving recommendation is R-5 (implement unpopulated fields). Declared but empty fields are worse than absent fields because they create a false API surface that consumers code against.
