# Cross-Review: integration-architect reviewing functional-typing (Round 2)

## Overall Assessment

functional-typing's Round 2 review is precise and well-grounded. The review correctly focuses on the P1 implementation details and the P2 items where the type-system perspective is strongest. The concrete YAML structure for influence_headings (Rec 2) is the definitive format proposal. The provisional-resolution marker lifecycle answer (Rec 6) converges with the integration-architect's position.

## Recommendation-by-Recommendation Assessment

### Rec 1: Finalize influence_headings field type (P1)

**Strong agreement.** The proposed field type `dict[str, list[str]]` with `Field(default_factory=dict)` is correct. The design that `required_headings` serves as the `binding` headings eliminates duplication. The rationale (YAML deserialization produces strings; mode schema files should not require enum awareness) is pragmatic and aligns with the integration-architect's implementation perspective.

One observation: the field default (`default_factory=dict`) means existing mode schemas (cooperative.yml, red-blue.yml, etc.) that lack `influence_headings` will load with an empty dict, which is correct backward-compatible behavior. When the dict is empty and the influence level is non-binding, the runtime validation falls back to `required_headings`. This is the right default.

### Rec 2: Add influence_headings to cooperative.yml (P1)

**Strong agreement.** The proposed YAML is the exact format that should be implemented. The structure is clean, declarative, and lintable. No further design discussion needed.

### Rec 3: Use Phase enum in validate.py (P2)

**Agreement, maintained from Round 1.** This was adopted by the integration-architect as NEW-1 in Round 1 revision. No change. The arbiter (AO-4) confirmed the constitutional grounding. The downgrade from P1 to P2 was the right call.

### Rec 4: Type VariableDefinition.phases as list[Phase] (P2)

**Agreement, maintained from Round 1.** This was adopted by the integration-architect as NEW-2 in Round 1 revision. Clean type-system improvement.

### Rec 5: Document config_conditions as metadata-only (P2)

**Agreement.** The integration-architect conceded on this sequencing in Round 1, and the arbiter (AO-3) confirmed the concession was sound. Document first, implement evaluation later. No change.

### Rec 6: Address provisional-resolution marker lifecycle (P2)

**Strong agreement.** The proposed lifecycle -- markers are round-scoped, re-opened disputes return to DISPUTES_BEGIN/DISPUTES_END -- converges with the integration-architect's Round 2 Rec 6. Three-agent convergence.

functional-typing adds a valuable Principle II observation: the markers should be specified before they are declared stable. This is correct. The integration-architect's Round 2 Rec 6 suggests marking them as unstable until validated, which is the same conclusion.

### Rec 7: Use PHASE_CONTEXT_MODELS with Phase keys (P3)

**Weak agreement.** This is a consistency improvement but very low impact. The runtime assertion (models.py L390-394) already catches drift. The Phase-keyed dict would make the structural guarantee rather than asserted, which is marginally better. Correctly prioritized at P3.

## Gaps or Missed Points

- **No engagement with template last-mile audit**: functional-typing does not address the systemic blind spot identified by the arbiter (Consideration 1). The integration-architect and game-engine-advocate both propose formalizing this. functional-typing's silence on this topic is a minor gap.

- **No P2 sub-ordering engagement**: The integration-architect proposed P2-easy vs. P2-structural sub-ordering (Round 2 Rec 4). functional-typing does not comment on this. Agreement or disagreement would be useful.

## Tensions or Contradictions

None. functional-typing's Round 2 positions are fully compatible with the integration-architect's positions. The influence_headings field type is a three-agent convergence point.
