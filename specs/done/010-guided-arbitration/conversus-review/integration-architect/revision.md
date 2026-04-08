# Cooperative Revision — Phase 3

**Agent**: integration-architect
**Round**: 1 of 2
**Mode**: cooperative
**Iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Scope Step 5 validation to arbiter block only
- **Original position**: Validate only the `arbiter:` block in Step 5, not the full config.
- **Disposition**: Modified
- **Explanation**: Devils-advocate's cross-review (cross-reviews/integration-architect.md, Dangerous Contradictions, "Step 5 validation scope") correctly identifies that purely arbiter-scoped validation could miss cross-reference issues like arbiter name collisions with agent names. The modified recommendation adopts a middle ground.
- **Modified recommendation**: In Step 5, validate the `arbiter:` block using the arbiter-specific validation from Step 1 (SKILL.md L212-222) PLUS cross-references: (1) arbiter name does not collide with any agent name, (2) grounding path exists on disk. Skip re-validation of agents, targets, and mode — these were validated when the deliberation originally ran.

#### Recommendation 2: Specify template validation in Step 5
- **Original position**: Add template existence validation before launching Phase 6.
- **Disposition**: Surviving
- **Explanation**: Functional-typing acknowledged this gap in their cross-review (Tensions, "Template validation in the arbitrate handler") and added it as a new recommendation in revision. Devils-advocate's cross-review (Tensions, "Template validation") suggested wrapping the error in plain language. I accept the plain-language wrapping while maintaining the core recommendation.
- **Surviving with note**: The error message should be user-friendly: "The arbitration system is not properly configured. Check that the templates/ directory exists alongside conversus.yml."

#### Recommendation 3: Specify arbiter block removal method for reconfigure
- **Original position**: Read, parse as YAML, remove the `arbiter` key, and write back.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. Functional-typing's cross-review (Safe Agreements, "YAML modification needs proper specification") reinforces the need for YAML-aware operations. This recommendation is part of the broader consensus on YAML serialization.

#### Recommendation 4: Add timing field to generated config
- **Original position**: Add `timing: final` to the generated arbiter config block.
- **Disposition**: Surviving
- **Explanation**: Devils-advocate's cross-review (Tensions, "Adding fields to generated config") calls this a "no-brainer addition." No cross-review challenged it. The self-documenting value is clear.

#### Recommendation 5: Define structural ruling extraction for post-arbitration report
- **Original position**: Extract rulings by parsing `#### Dispute:` headings, `**Ruling:**` lines, and `**Rationale:**` first sentences.
- **Disposition**: Modified
- **Explanation**: Devils-advocate's cross-review (Dangerous Contradictions, "Post-arbitration report") notes that structural extraction should produce plain-language summaries, not mechanical extractions. I agree — the extraction method is about reliability, but the output should be reformatted for users.
- **Modified recommendation**: Extract rulings by parsing `#### Dispute:` headings and `**Ruling:**` lines from `resolution.md`. Reformat each extracted ruling into a plain-language one-liner: "{dispute topic} -> {decision} ({first sentence of rationale})". If no `#### Dispute:` headings are found, use the generic fallback at SKILL.md L1852-1854.

#### Recommendation 6: Use Step 1 trigger determination instead of re-evaluating in Step 5
- **Original position**: Use the trigger determination from Step 1 rather than re-reading the synthesis.
- **Disposition**: Withdrawn
- **Explanation**: Devils-advocate's cross-review (Tensions, "Trigger re-evaluation") argues the re-evaluation is a safety check with negligible overhead. On reflection, the re-evaluation serves as a guard against an edge case where the synthesis changes between Steps 1 and 5 (unlikely but possible). The original recommendation optimized for logical purity at the expense of a minor safety net. The current spec behavior (re-evaluate) is defensible.

#### Recommendation 7: Add explicit multi-round output documentation
- **Original position**: Add a note clarifying that `summary/final.md` works for both single-round and multi-round outputs.
- **Disposition**: Surviving
- **Explanation**: Functional-typing independently made the same recommendation (Recommendation 5, P2). Cross-review confirmed unanimous convergence (Safe Agreements, "Multi-round output directory needs documentation"). This is a straightforward documentation addition.

#### Recommendation 8: Include docs field in generated arbiter config
- **Original position**: Add an optional step 3e asking about additional arbiter documentation.
- **Disposition**: Modified
- **Explanation**: Devils-advocate's cross-review (Tensions, "Adding fields to generated config") notes that adding a `docs:` step adds another decision point to an already multi-step flow. On reflection, this should be optional and positioned as advanced configuration.
- **Modified recommendation**: After Step 3d (influence level), add: "Any additional documents the arbiter should reference? (Enter paths separated by commas, or press Enter to skip)". This step is explicitly labeled as optional. If paths are provided, include `docs:` in the generated config. If skipped, omit `docs:` entirely.

### New Recommendations

- **Add arbiter name collision check** (Priority: P2)
  - **Triggered by**: Devils-advocate's cross-review (cross-reviews/integration-architect.md, Dangerous Contradictions, "Step 5 validation scope") identified that arbiter names could collide with agent names.
  - **Proposed change**: When generating the arbiter name (SKILL.md L1772), check it against agent names from `conversus.yml`. If a collision is found, append `-arbiter` to the name and report: "Arbiter name adjusted to '{name}-arbiter' to avoid collision with agent name '{name}'."
  - **Rationale**: Name collisions could cause directory conflicts in the output structure and confusing cross-references in the resolution document.

### Position Summary

I withdrew 1 recommendation (Recommendation 6 — trigger re-evaluation, yielding to the safety-check argument), modified 3 (Recommendations 1, 5, and 8), and maintained 4 (Recommendations 2, 3, 4, and 7). I added 1 new recommendation (arbiter name collision check).

The most significant change was on Step 5 validation scope (Recommendation 1). My original position was "arbiter-only." Devils-advocate's cross-review correctly identified that purely scoped validation misses cross-reference issues. The modified recommendation adds cross-reference checks (name collision, grounding path) while still avoiding full config re-validation. This is a better design — narrower than full re-validation but broader than pure arbiter-scoping.

My highest-priority recommendation remains template validation in Step 5 (Recommendation 2, P1). This is a genuine gap: the arbitrate handler delegates to Phase 6 but skips the Run engine's template loading step, meaning a missing template produces an opaque error instead of clear guidance.
