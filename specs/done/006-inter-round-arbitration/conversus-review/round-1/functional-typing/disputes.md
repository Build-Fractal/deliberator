# Disputes -- functional-typing

## Remaining Disputes

### D1: Phase Enum Priority -- P1 vs. P2

**Parties**: functional-typing (P2, downgraded from P1) vs. integration-architect (P2, adopted)
**Status**: Resolved. Both agents now agree on P2. No remaining dispute.

### D2: ErrorType Reclassification Priority -- P2 vs. P3

**Parties**: functional-typing (P3, downgraded from P2) vs. integration-architect (P3 assessment in cross-review)
**Status**: Resolved. functional-typing accepted the downgrade to P3. No remaining dispute.

### D3: config_conditions Evaluation Sequencing

**Parties**: functional-typing (evaluate or document now, P2) vs. integration-architect (fix required status first, evaluate later)
**Status**: Minor tension remains. functional-typing believes the minimum variant (document that config_conditions are metadata-only) should be part of spec 006 changes. integration-architect's Rec 9 (mark ARBITRATION_RULINGS as required:true) implicitly depends on evaluation existing. The sequencing matters: documenting the gap first prevents false expectations, which is a prerequisite for either approach.

**functional-typing position**: Document the metadata-only nature of config_conditions in this spec cycle. Defer full evaluation to a future spec. This is not a high-stakes dispute -- both agents agree the gap exists and should be addressed. The disagreement is only about timing.

### D4: ConversusConfig Model extra Policy

**Parties**: functional-typing (create model, P3) vs. game-engine-advocate (needs extra:"allow" for plugins)
**Status**: Resolved. functional-typing accepted the extensibility note. The model should use `extra: "allow"` at the top level or include a `plugins: dict[str, Any]` field. No remaining dispute on the recommendation itself; only on whether P3 is the right priority (all agree P3).

## Convergence

The following recommendations have full three-agent consensus:

1. **P1: Add influence-aware heading data to ArbitrationConfig + cooperative.yml** -- All three agents endorse this as the top priority. The YAML structure and Pydantic field type are agreed.

2. **P1: Wire {ARBITRATION_PATHS} into cross-round synthesis template** -- All three agents adopted this after integration-architect identified it. functional-typing and game-engine-advocate both acknowledged missing this in their original reviews.

3. **P1: Wire {ARBITRATION_RULINGS} into cross-round synthesis template** -- Same as above. Dead infrastructure must be connected.

4. **P2: Use Phase enum in validate.py** -- All three agents agree on P2. functional-typing downgraded from P1; integration-architect adopted at P2.

5. **P2: Fix conversus.yml doc paths** -- Trivial, no disagreement.

6. **P2: Document linter static-vs-runtime heading validation boundary** -- All three agents agree the boundary is intentional and should be documented.

7. **P2: Add structural markers for provisionally resolved disputes** -- integration-architect and game-engine-advocate endorse this. functional-typing supports it as consistent with typed behavioral categories.

## Final Position Statement

The functional-typing agent's position after the full deliberation:

The spec 006 implementation is type-safe and well-structured. The StrEnum conversions, Pydantic model immutability, and pure function composition in the linter are correct and aligned with Constitution Principle IX. The three most important findings across all agents are:

1. The influence-aware heading data gap (shared P1 across all agents)
2. The dead template variable infrastructure for ARBITRATION_PATHS and ARBITRATION_RULINGS (integration-architect P1, adopted by all)
3. The config_conditions evaluation gap (functional-typing P2, with sequencing nuance)

The functional-typing review's unique contribution is identifying the type-system layer gaps: Phase enum non-usage in validate.py, VariableDefinition.phases as list[str], and ErrorType semantic misuse. These are code quality improvements (P2-P3) that strengthen the codebase's long-term maintainability without affecting current correctness.

The functional-typing review's blind spot was the template layer: a perfectly typed pipeline with no template consumer is dead infrastructure. Future functional-typing reviews should include a "last-mile audit" that verifies typed variables are actually consumed by their intended templates.
