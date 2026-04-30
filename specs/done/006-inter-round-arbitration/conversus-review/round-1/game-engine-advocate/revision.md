# Revision -- game-engine-advocate

## Recommendation Dispositions

### R1: Normalize ConfigCondition operators in variables.yml (originally P3)
**Disposition: Maintain at P3.**
No cross-review disagreement. integration-architect notes the normalization is fine but should not be mistaken for fixing the evaluation gap. Agreed -- this is a consistency pass, not a semantic fix.

### R2: Address influence-aware heading validation (originally P1)
**Disposition: Maintain at P1. Adopt Option A (structured data), not Option B (skip validation).**
Cross-reviews from both functional-typing and integration-architect favor Option A. functional-typing provides the Pydantic model design (`dict[InfluenceLevel, list[str]]`); integration-architect provides the YAML schema structure. Option B (skip validation) was proposed as simpler, but the cross-reviews correctly argue that abandoning static validation for arbitration headings removes a safety net. The structured data approach enables future linter evolution without blocking current functionality.

Revising the recommendation to explicitly endorse the integration-architect's YAML structure loaded into functional-typing's Pydantic field.

### R3: Add plugin hook comments to SKILL.md (originally P3)
**Disposition: Withdraw.**
integration-architect's cross-review raises valid concerns: SKILL.md is an executable spec where every line is load-bearing. Comments referencing an archived spec with undefined terminology ("POST_SYNTHESIS", "POST_ARBITRATION") would confuse implementers. The integration-architect's counter-proposal (defer until the game engine spec is unarchived, or add a non-normative section at the bottom) is more appropriate. Withdrawing this recommendation.

### R4: Update conversus.yml doc paths (originally P2)
**Disposition: Maintain at P2.**
No disagreement. Factual config error.

### R5: Consider influence dispatch externalization (originally P3)
**Disposition: Withdraw.**
integration-architect's cross-review correctly identifies premature abstraction risk. The game-engine-advocate's own OBA-1 self-corrected the assumption that plugins need new influence levels. If the primary use case (game engine plugins as analytical observers) does not need influence extensibility, externalizing the dispatch is YAGNI. The proposed `influence_headings` field on `ArbitrationConfig` already provides a data-driven mapping that could be extended when needed.

## New Recommendations

### NEW-1: Wire {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} into cross-round synthesis template (Priority: P1)
**Source: integration-architect Recs 2 and 3.**
This is the game-engine-advocate's most significant miss. The cross-round synthesis template is the natural predecessor to game engine post-deliberation hooks, and it does not reference the arbitration data variables that are fully provisioned in the pipeline. integration-architect correctly identifies this as dead infrastructure. The game-engine-advocate's review was too focused on structural compatibility and missed template-level completeness. Adopting as P1.

### NEW-2: Add structural markers for provisionally resolved disputes (Priority: P2)
**Source: integration-architect Missed Opportunity 6, cross-reviewed by game-engine-advocate.**
The dispute-parsing subsystem needs structural markers to distinguish provisionally-resolved disputes from remaining disputes. This matters for game engine integration because the convergence predictor needs accurate dispute counts. Without markers, the predictor would need to parse agent prose, violating "templating over inference." Adding a `PROVISIONALLY_RESOLVED_BEGIN`/`PROVISIONALLY_RESOLVED_END` marker pair in the synthesis template would close this gap.

## Position Summary

After cross-reviews, the game-engine-advocate position has narrowed significantly:

1. **Two recommendations withdrawn**: Plugin hook comments (R3) and influence dispatch externalization (R5) were both premature for an archived spec. The integration-architect's "build when needed" discipline is correct.

2. **Critical miss acknowledged**: The dead template variables ({ARBITRATION_PATHS}, {ARBITRATION_RULINGS}) were not caught by the game-engine-advocate review. This reveals a blind spot: the review validated structural compatibility and extensibility architecture but did not verify that the integration pipeline was actually connected end-to-end. Future game-engine reviews should include a "last-mile template audit."

3. **Option A over Option B for heading validation**: The game-engine-advocate originally favored the simpler Option B (skip validation). Both co-reviewers made convincing arguments for Option A (structured data). The revised position endorses structured heading data in both YAML and Pydantic model.

The core game-engine finding stands: spec 006 makes no decisions that would require rework when the game engine ships. The structural compatibility is sound. The gaps are in template completeness (adopted from integration-architect) and heading validation data (shared with all three agents).
