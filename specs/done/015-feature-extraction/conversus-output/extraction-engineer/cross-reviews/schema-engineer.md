# Extraction Engineer Cross-Review of Schema Engineer
# Spec: 015-feature-extraction

**Cross-reviewer**: extraction-engineer
**Reviewing**: schema-engineer's review at `conversus-output/schema-engineer/review.md`
**My review**: `conversus-output/extraction-engineer/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: AgentFeatures refactoring — discriminated union vs. backward-compatible flat model

Schema-engineer R-1 recommends refactoring AgentFeatures into per-mode discriminated unions (CooperativeAgentFeatures, WTAAgentFeatures, etc.). My review does not address the model structure at all, implicitly accepting the flat model. The contradiction is not in the assessment but in the impact on extraction code: the extraction module constructs AgentFeatures directly in four separate mode extractors. Adopting discriminated unions would require rewriting all four mode extractors to produce their specific subtypes, changing the `agent_features: dict[str, AgentFeatures]` type on RoundFeatures to `dict[str, AgentFeaturesUnion]`, and updating every test that constructs AgentFeatures. The extraction code is the primary producer of these models; the schema-engineer's recommendation is architecturally correct but operationally expensive for a pipeline that currently works correctly.

**Resolution needed**: The refactoring is sound for long-term extensibility (FR-007), but it should be staged: first stabilize the extraction pipeline (fix the parsing bugs I identify), then refactor the models. Doing both simultaneously risks compounding defects.

### DC-2: territory_claim_vector — declared-but-unpopulated field

Schema-engineer O-1 flags `territory_claim_vector` as declared but never populated and recommends removing or implementing it. My review M-6 identifies a related but distinct gap: position vector lengths are not normalized across agents. These are different fields, but they expose the same underlying pattern -- the model declares more than the extraction pipeline populates. I agree with schema-engineer's diagnosis. The field should be implemented, not removed: the spec explicitly defines territory claims as a PD feature, and the extraction logic should parse them from the "Core Competencies" / "Unique Capabilities" / "Shared Territory" sections into a binary vector.

---

## Tensions

### T-1: VALID_MODES deduplication priority

Schema-engineer M-3 recommends deduplicating VALID_MODES between features.py and objectives.py. This is correct but low-urgency: the two frozensets are identical and unlikely to diverge since adding a new mode is a spec-level change that would touch many files. My review does not address this because the extraction module imports VALID_MODES from features.py and has no dependency on objectives.py.

### T-2: AgreementMatrix type alias vs. my tighter pattern matching

Schema-engineer M-4 recommends a semantic AgreementMatrix type. My review M-3 recommends tightening the regex that counts agreements. These are complementary: schema-engineer addresses the type representation, I address the parsing accuracy. Both should be done, with parsing fixes preceding type changes (no point typing an incorrectly-parsed matrix).

### T-3: JSON Schema export priority

Schema-engineer R-8 recommends generating features.schema.json for non-Python consumers. This is a valid improvement but has no current consumers: all plugins (specs 017-019) are Python packages that import the Pydantic model directly. The JSON Schema export should wait until a non-Python consumer exists.

---

## Safe Agreements

- **SA-1: Frozen models are correct** — Both reviews agree that frozen Pydantic models are the right choice for extraction output consumed by plugins.

- **SA-2: FeatureSet mode validation works** — Both reviews confirm the model_validator catches invalid modes.

- **SA-3: Default values enable FR-003 compliance** — Both reviews agree that zero defaults on all feature fields enable graceful degradation.

- **SA-4: confirmed_count is declared but unpopulated** — Schema-engineer O-2 and the extraction code confirm this. The field should be implemented.

- **SA-5: metadata extensibility is pragmatic** — Schema-engineer A-5 notes `dict[str, Any]` metadata as a useful extension point. I agree this is the right trade-off for now, though schema-engineer's R-6 (typed FeatureSetMetadata) would improve discoverability.
