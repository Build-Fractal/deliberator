# Disputes -- game-engine-advocate

## Remaining Disputes

### D1: Plugin Hook Comments -- Withdrawn vs. Deferred

**Parties**: game-engine-advocate (withdrawn) vs. integration-architect (defer to separate section if desired)
**Status**: Resolved. game-engine-advocate withdrew R3 based on integration-architect's valid concerns about SKILL.md being an executable spec. If plugin hooks are ever needed, they should be in an active spec, not as comments in spec 006's implementation. No remaining dispute.

### D2: Influence Dispatch Externalization -- Withdrawn vs. YAGNI

**Parties**: game-engine-advocate (withdrawn) vs. integration-architect (premature abstraction)
**Status**: Resolved. game-engine-advocate withdrew R5. The game-engine-advocate's own OBA-1 undermined the primary use case for externalization. The proposed `influence_headings` field on ArbitrationConfig already provides sufficient data-driven mapping. No remaining dispute.

### D3: Option A vs. Option B for Heading Validation

**Parties**: game-engine-advocate (originally Option B, revised to Option A) vs. functional-typing (Option A) vs. integration-architect (Option A)
**Status**: Resolved. game-engine-advocate revised to Option A (structured data) based on cross-review arguments. No remaining dispute.

## Convergence

The following recommendations have full three-agent consensus:

1. **P1: Influence-aware heading data in ArbitrationConfig + cooperative.yml** -- Universal P1. All agents endorse the same YAML structure and Pydantic field design.

2. **P1: Wire {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} into cross-round synthesis** -- game-engine-advocate adopted this from integration-architect and acknowledged it as the review's most significant miss.

3. **P2: Fix conversus.yml doc paths** -- Trivial, factual error.

4. **P2: Structural markers for provisionally resolved disputes** -- game-engine-advocate and integration-architect endorse this. Necessary for accurate convergence prediction in the game engine context and for correct dispute counting in the current system.

5. **P3: Normalize ConfigCondition operators** -- Cosmetic consistency, no disagreement.

## Final Position Statement

The game-engine-advocate's position after the full deliberation:

Spec 006 is well-designed from the game engine perspective. The core finding stands: **the spec makes no decisions that would require rework when the game engine ships**. The StrEnum extensibility, influence model taxonomy, and inter-round execution ordering are all structurally compatible with the archived game engine vision.

Two recommendations were withdrawn (plugin hook comments, influence dispatch externalization) as premature for an archived spec. This is the correct application of YAGNI -- build the abstraction when the concrete need arrives, not before.

The game-engine-advocate review's most significant gap was missing the dead template variables ({ARBITRATION_PATHS}, {ARBITRATION_RULINGS}). This reveals a blind spot in extensibility-focused reviews: verifying that the architecture supports extension is necessary but not sufficient. The integration pipeline must also be connected end-to-end. Future game-engine reviews should include a template-level completeness audit.

The game-engine-advocate contributed unique value in three areas:
1. Validating that the three-tier influence model maps to game-theoretic mechanism design roles (dictator/mediator/observer)
2. Confirming that the inter-round execution ordering (Phase 5 -> Phase 6 -> termination) is correct for convergence prediction
3. Self-correcting the assumption that plugins need to extend InfluenceLevel (OBA-1), which prevented premature abstraction in the spec
