# Cross-Review: functional-typing reviewing integration-architect

## Dangerous Contradictions

None identified. The integration-architect's recommendations are architecturally compatible with functional-typing's type-system-oriented positions. No recommendation from either agent would invalidate or break the other's proposals.

## Tensions

### T1: Template Wiring Gaps vs. Type-System Gaps -- Priority Ordering

**functional-typing** prioritizes type-system completeness: Phase enum usage in validate.py (Rec 1), influence-aware heading model (Rec 2), ErrorType reclassification (Rec 3), and VariableDefinition.phases typing (Rec 4) are all P1 or P2.

**integration-architect** prioritizes template wiring completeness: `{ARBITRATION_PATHS}` in cross-round synthesis (Rec 2, P1), `{ARBITRATION_RULINGS}` in cross-round synthesis (Rec 3, P1), and PRIOR_ARBITRATION_PATH path computation documentation (Rec 6, P2).

The tension is not about correctness but about urgency. integration-architect identifies dead infrastructure: variables are defined in the schema, wired in Pydantic models, documented in SKILL.md, but never referenced in the template that consumes them. This means the entire pipeline is built but the last-mile connection (template reference) is missing. functional-typing's type-system improvements would not fix this gap -- a perfectly typed variable that no template references is still dead infrastructure.

From the functional-typing perspective, the integration-architect's P1 items (Recs 2 and 3) are legitimate P1 issues that should rank alongside or above type-system cleanup. Dead infrastructure is worse than imperfect typing because it creates a false sense of completeness.

### T2: Structural Markers for Provisionally Resolved Disputes

**integration-architect** identifies that the dispute-parsing subsystem has no structural markers for "Provisionally Resolved" disputes (Missed Opportunity 6). With `recommended` influence, disputes should be excluded from the remaining count, but the synthesis template lacks a separate marker block. The orchestrator relies on agent reasoning to categorize disputes correctly.

**functional-typing** does not address this directly but the concern maps to functional-typing's broader principle: if the system distinguishes "provisionally resolved" as a behavioral category, it should be modeled in the type system (e.g., a `DisputeStatus` enum with `REMAINING`, `PROVISIONALLY_RESOLVED`, `RESOLVED`). The current reliance on agent prose to categorize disputes is exactly the kind of ambiguity that typed structural markers would eliminate.

This is a tension because functional-typing would want to model it in the type system first, while integration-architect focuses on the template-level structural marker. Both are needed: the type defines the category, the template marker makes it parseable.

### T3: Linter Documentation vs. Linter Implementation

**integration-architect** recommends documenting the linter's static-vs-runtime heading validation gap with a code comment (Rec 4, P2). This is a "document the gap, don't fix it" approach.

**functional-typing** recommends building the infrastructure to eventually close the gap: influence-aware heading map in ArbitrationConfig (Rec 2, P1) and config_conditions evaluation in the linter (Rec 5, P2). This is a "fix the gap incrementally" approach.

The tension: documentation-only approaches prevent wasted effort but also prevent progress. If the comment says "don't try to make the linter influence-aware," it may discourage the very improvement that functional-typing's Rec 2 would enable. The resolution is to document the current gap AND build the data model that makes the gap closable -- then a future iteration can connect the two.

## Safe Agreements

### SA1: Influence-Aware Heading Validation Is the Top Shared P1
Both agents rank influence-aware heading validation as P1. integration-architect's Rec 1 and functional-typing's Rec 2 propose the same structural change to `ArbitrationConfig` with `influence_headings` data. The proposed YAML structure in integration-architect's Rec 1 is directly compatible with functional-typing's proposed `dict[InfluenceLevel, list[str]]` field.

### SA2: PRIOR_ARBITRATION_SECTION vs. PRIOR_ARBITRATION_PATH Distinction Is Load-Bearing
integration-architect's Rec 5 (add documentation distinguishing SECTION from PATH on ReviewContext) aligns with functional-typing's Rec 8 (add model_validator enforcing PRIOR_ARBITRATION_PATH when PRIOR_ARBITRATION_SECTION is non-empty). Both recognize the distinction is subtle, important, and under-documented.

### SA3: StrEnum Implementation Is Correct
Both agents validate the StrEnum implementation for InfluenceLevel and ArbiterTiming. integration-architect specifically confirms Constitution Principle IX compliance.

### SA4: Stagnation Detection Needs Influence-Adjusted Counts
integration-architect's Rec 8 (add stagnation interaction documentation for influence levels) addresses a gap that functional-typing's config_conditions evaluation (Rec 5) would partially surface. Both agree the influence-adjusted dispute count must flow through to stagnation detection.

### SA5: Schema Variables Are Correctly Provisioned
Both agents agree the schema variables in variables.yml are correctly defined with appropriate phases, types, and config_conditions. The gap is in consumption (template references) and enforcement (linter evaluation), not definition.
