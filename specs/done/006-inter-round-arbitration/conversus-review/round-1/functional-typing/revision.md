# Revision -- functional-typing

## Recommendation Dispositions

### Rec 1: Use Phase enum in validate.py (originally P1)
**Disposition: Maintain, downgrade to P2.**
Cross-reviews from integration-architect correctly note this is a code quality improvement with no behavioral impact. The linter works correctly with string comparisons -- the risk is future maintenance, not current correctness. The constitution mandates StrEnum for closed behavioral choices, but the mandate is about design purity, not about a broken system. Downgrading to P2 acknowledges the integration-architect's point that P1 should be reserved for correctness gaps.

### Rec 2: Add influence-aware heading map to ArbitrationConfig (originally P1)
**Disposition: Maintain at P1. Adopt integration-architect's YAML structure.**
All three agents converge on this as the top gap. integration-architect's proposed YAML structure (explicit heading lists per influence level) is directly compatible with the proposed `dict[InfluenceLevel, list[str]]` field. game-engine-advocate's Option B (skip validation entirely) is rejected in favor of the structured data approach, because abandoning static validation for arbitration headings removes a safety net. The structured approach enables future linter evolution while providing an immediate single source of truth.

game-engine-advocate raises a tension about whether the source of truth should be in YAML (plugin-extensible) or Pydantic (type-safe). The answer is both: YAML as the declarative source, Pydantic model as the validated runtime form. This is exactly how the existing mode schema works -- `cooperative.yml` is loaded into `ModeSchema` Pydantic model.

### Rec 3: Reclassify semantic misuses of ErrorType (originally P2)
**Disposition: Maintain, downgrade to P3.**
integration-architect's cross-review correctly notes this is a linter-internal issue with no downstream behavioral impact. The error type misclassification does not affect template generation, agent behavior, or output correctness. Downgrading to P3 reflects that this is cleanup, not correctness.

### Rec 4: Type VariableDefinition.phases as list[Phase] (originally P2)
**Disposition: Maintain at P2.**
No cross-review disagreement. game-engine-advocate raises a general concern about Phase enum strictness vs. plugin-contributed phases, but this applies to `validate.py` function signatures, not to `VariableDefinition.phases`. The `phases` field describes which phases a variable appears in -- this is schema metadata, not runtime dispatch. Even with plugin phases, the core schema variables would still use core phases.

### Rec 5: Implement config_conditions evaluation in the linter (originally P2)
**Disposition: Maintain at P2, adopt minimum variant.**
integration-architect's Rec 9 (mark ARBITRATION_RULINGS as required:true with config_conditions) implicitly depends on config_conditions being evaluated -- otherwise the "required:true" is enforced unconditionally, which is wrong. The minimum variant (document that config_conditions are metadata-only, not linter-enforced) should be the first step. Full evaluation can follow in a future spec.

### Rec 6: Use match/case for phase-specific validation (originally P2)
**Disposition: Maintain at P2.**
game-engine-advocate correctly notes that match/case exhaustiveness only applies to core phases; plugin phases hit the default branch. This is not a problem -- it is the correct behavior. The value of match/case is making the default case explicit, not preventing it.

### Rec 7: Create a ConversusConfig Pydantic model (originally P3)
**Disposition: Maintain at P3, add extensibility note.**
game-engine-advocate's concern about a frozen ConversusConfig rejecting plugin config fields is valid. The model should use `extra: "allow"` for the top-level config or include a `plugins: dict[str, Any]` field. Adding this note to the recommendation.

### Rec 8: Add PRIOR_ARBITRATION_PATH model_validator (originally P3)
**Disposition: Maintain at P3.**
integration-architect's complementary recommendation (inline documentation) is additive. Both documentation and enforcement are warranted.

## New Recommendations

### NEW-1: Wire {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} into cross-round synthesis template (Priority: P1)
**Source: integration-architect Recs 2 and 3, endorsed during cross-review.**
integration-architect identified dead infrastructure: variables defined in schema, wired in Pydantic models, documented in SKILL.md, but never referenced in the cross-round synthesis template. This is a correctness gap -- the cross-round synthesizer cannot produce accurate Resolution Attribution without reading arbitration files. functional-typing did not catch this because the review focused on the type system layer, not the template layer. Adopting this as P1.

### NEW-2: Fix conversus.yml doc paths for game-engine-advocate (Priority: P2)
**Source: game-engine-advocate R4.**
The broken doc paths are a factual config error. Trivial fix.

## Position Summary

After cross-reviews, the functional-typing position has adjusted in two ways:

1. **Priority recalibration**: Rec 1 (Phase enum in validate.py) and Rec 3 (ErrorType reclassification) are downgraded from P1/P2 to P2/P3 respectively. The integration-architect's framework -- P1 for correctness gaps, P2 for code quality, P3 for cleanup -- is more pragmatic than the constitution-compliance-first framework used in the original review.

2. **Template-level gaps adopted**: The integration-architect identified a critical gap (dead template variables) that the functional-typing review missed entirely. The type system was correct end-to-end, but the last-mile template reference was missing. This is a blind spot of type-system-focused reviews: a perfectly typed variable that no template references is still dead infrastructure.

The core position remains: type safety and enum coverage are essential for maintainability, but they rank below correctness gaps in the integration pipeline. The top P1 items are now (1) influence-aware heading data in ArbitrationConfig and (2) wiring ARBITRATION_PATHS/RULINGS into the cross-round synthesis template.
