# Cross-Review: functional-typing reviewing game-engine-advocate

## Dangerous Contradictions

None identified. The game-engine-advocate's recommendations do not contradict functional-typing's positions. Both agents converge on the same core gap (influence-aware heading validation) and propose compatible solutions.

## Tensions

### T1: Influence Dispatch Externalization vs. Type-System-First

**functional-typing** recommends extending `ArbitrationConfig` with an `influence_headings: dict[InfluenceLevel, list[str]]` field and a `get_headings()` method on the Pydantic model (Recommendation 2). This keeps the dispatch in typed Python data structures where the type system enforces completeness.

**game-engine-advocate** recommends externalizing influence dispatch into a dedicated `schema/influence-levels.yml` file or a mode schema section (MO-1, R5). This prioritizes plugin extensibility -- plugins add YAML entries rather than modifying Python code.

These approaches are not mutually exclusive but create a tension about where the source of truth lives. functional-typing wants it in Pydantic models (type-safe, import-time validated); game-engine-advocate wants it in YAML schema (plugin-extensible, no code changes). The resolution is likely both: YAML schema as the declarative source, Pydantic model as the validated runtime form. But the game-engine-advocate's approach risks re-introducing the "raw dict" problem that Constitution Principle IX warns against unless the YAML is loaded through a Pydantic model.

### T2: Heading Validation Strategy -- Option A vs. Option B

**game-engine-advocate** explicitly presents two options for FR-023 heading validation (R2): Option A (add all heading variants to mode schema) vs. Option B (skip heading validation for arbitration templates with `{INFLUENCE_LEVEL}`). The game-engine-advocate favors Option B as simpler.

**functional-typing** implicitly favors Option A by recommending a structured `influence_headings` field on `ArbitrationConfig` with a `get_headings()` method. This assumes the linter should eventually validate influence-adjusted headings, which requires the heading data to exist in the schema.

The tension: Option B (skip validation) is pragmatic now but abandons static validation for arbitration headings entirely. Option A (structured data) is more work but preserves the linter's ability to validate headings as the system evolves. For a type-safety-oriented perspective, Option A is preferable because it keeps the type system engaged rather than carving out an exception.

### T3: Plugin Hook Comments -- Scope Creep Risk

**game-engine-advocate** recommends adding plugin hook point comments to SKILL.md (R3) referencing the archived game engine spec. **functional-typing** has no position on this but notes a general concern: adding comments that reference archived/unimplemented specs can mislead maintainers into thinking the hook points are load-bearing design constraints rather than aspirational notes. The comments should be clearly marked as forward-looking and non-normative.

## Safe Agreements

### SA1: Influence-Aware Heading Validation Is a P1 Gap
Both agents identify the static `required_headings` in `cooperative.yml` as the most important gap. functional-typing's Recommendation 2 and game-engine-advocate's R2 target the same problem. Both agree this is P1 priority.

### SA2: ConfigCondition Operator Inconsistency Should Be Normalized
game-engine-advocate identifies the inconsistent `operator` usage in `variables.yml` (MO-4, R1). functional-typing does not explicitly flag this but notes that `config_conditions` are not evaluated by the linter (Off-Base Assumption 1), which implicitly supports normalizing the schema for consistency even if the conditions are metadata-only.

### SA3: StrEnum Implementation Is Correct
Both agents agree that the `InfluenceLevel` and `ArbiterTiming` StrEnums are correctly implemented per Constitution Principle IX. game-engine-advocate specifically validates the factory extension docstrings. functional-typing validates the closed behavioral enum pattern.

### SA4: Spec 006 Does Not Block Future Extensibility
game-engine-advocate's core finding ("The spec makes no decisions that would require rework when the game engine ships") aligns with functional-typing's assessment that the StrEnum and Pydantic model architecture is correctly extensible.

### SA5: The Game Engine May Not Need Additional Influence Levels
game-engine-advocate's OBA-1 self-corrects the assumption that plugins need to extend `InfluenceLevel`, noting that game engine plugins are analytical observers, not arbiters. functional-typing does not challenge the factory extension pattern itself but would agree that the three-level model is complete for the current design.
