# Cross-Review: integration-architect reviewing game-engine-advocate

## Dangerous Contradictions

None identified. The game-engine-advocate's recommendations are forward-looking and non-destructive. No recommendation would break current integration correctness or template wiring.

## Tensions

### T1: Plugin Hook Comments in SKILL.md -- Useful Signal vs. Spec Noise

**game-engine-advocate** recommends (R3, P3) adding comments at three execution points in SKILL.md to signal game engine plugin hook opportunities (PRE_EXECUTION, POST_SYNTHESIS, POST_ARBITRATION).

**integration-architect** is cautious about adding comments that reference an archived spec. SKILL.md is the executable orchestration specification -- every line is load-bearing for implementers. Comments referencing a non-existent plugin system could:
1. Confuse implementers into thinking hooks are part of the current contract
2. Create maintenance burden when hook point locations shift during future spec changes
3. Introduce terminology ("POST_SYNTHESIS", "POST_ARBITRATION") that is not defined in any active spec

The integration-architect's preference: if plugin hooks are desired, they should be specified in an active spec, not as comments in an existing spec's implementation artifact. A comment like "Plugin hook point: POST_ARBITRATION (spec 007)" when spec 007 does not exist is misleading.

Resolution: defer the comments until the game engine spec is unarchived. If a placeholder is desired, it should be in a separate "Future Integration Points" section at the bottom of SKILL.md, clearly marked as non-normative.

### T2: Influence Dispatch Externalization -- Premature Abstraction Risk

**game-engine-advocate** recommends (R5, P3) externalizing per-influence behavioral parameters into a data structure (e.g., `schema/influence-levels.yml`). The motivation is that plugins adding new influence levels would need to modify SKILL.md text if the dispatch remains embedded.

**integration-architect** recognizes the value but flags the premature abstraction risk. The current three-level influence model has exactly three consumers: heading validation, dispute counting, and template language. Externalizing three known values into a schema file adds a layer of indirection with no current consumer. The YAGNI principle applies: build the abstraction when the fourth influence level arrives, not before.

Additionally, game-engine-advocate's own OBA-1 self-corrects the assumption that plugins need new influence levels -- game engine plugins are analytical observers, not arbiters. If the primary motivating use case does not actually need the extensibility, the externalization is purely speculative.

Resolution: defer to when a concrete need for a fourth influence level arises. The current ArbitrationConfig model (with the proposed `influence_headings` field) already provides a data-driven mapping that could be extended without introducing a new schema file.

### T3: ConfigCondition Normalization Scope

**game-engine-advocate** recommends (R1, P3) normalizing all `config_conditions` entries to include the explicit `operator: "=="`. Lists specific lines in `variables.yml` (L95-96, L109-110, etc.).

**integration-architect** agrees on normalization but notes a broader concern: the game-engine-advocate identified 7 lines needing normalization, which implies many variables use config_conditions without explicit operators. Since config_conditions are not evaluated by the linter (as functional-typing identified), normalizing the syntax without implementing the evaluation creates more precise-looking metadata that is still not enforced. The normalization is fine as a consistency pass, but it should not be mistaken for fixing the evaluation gap.

## Safe Agreements

### SA1: Influence-Aware Heading Validation Is P1
Both agents agree this is the highest-priority gap. game-engine-advocate's R2 Option A aligns with integration-architect's Rec 1. Both propose structured heading data in the mode schema.

### SA2: Spec 006 Does Not Block Game Engine Integration
game-engine-advocate's core finding ("no decisions that would require rework") is independently confirmed by integration-architect's assessment that all 23 FRs have implementation artifacts and the architecture is extensible.

### SA3: The conversum.yml Doc Paths Are Broken
game-engine-advocate's R4 (fix doc paths from `specs/007-game-engine/` to `specs/archive/game-engine-vision/`) is a factual config error that integration-architect confirms needs fixing. Straightforward P2.

### SA4: Runtime vs. Static Heading Validation Architecture Is Correct
game-engine-advocate's R2 Option B (skip linter heading validation for dynamic templates) and integration-architect's Off-Base Assumption (influence-adjusted heading validation belongs at runtime) agree on the architectural boundary. The linter validates static templates; the orchestrator validates runtime output.

### SA5: Inter-Round Execution Ordering Is Correct
game-engine-advocate validates that the Phase 5 -> Phase 6 -> termination check sequence is the correct ordering for game engine integration (convergence predictor should see post-arbitration state). integration-architect validates that this sequence correctly implements the spec's inter-round execution model. Both agree the ordering is sound.
