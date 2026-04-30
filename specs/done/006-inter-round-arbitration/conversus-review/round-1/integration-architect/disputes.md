# Disputes -- integration-architect

## Remaining Disputes

### D1: config_conditions -- Document Now vs. Fix Required Status Now

**Parties**: functional-typing (document metadata-only nature now, P2) vs. integration-architect (fix required status, then evaluate later)
**Status**: Minor tension remains. functional-typing wants the documentation to come first to prevent false expectations. integration-architect wants the data to be correct first (mark ARBITRATION_RULINGS as required:true with conditions) so that when evaluation is implemented, it works correctly. Both agree the gap exists; the sequencing is the disagreement.

**integration-architect position**: Both should happen, but in different spec cycles. For spec 006: document that config_conditions are metadata-only (functional-typing's minimum variant). For a future spec: implement evaluation and then adjust required statuses. The risk of setting `required: true` without evaluation is that the linter will enforce it unconditionally, which is wrong. So documentation-first is actually the safer sequencing. Conceding to functional-typing on this point.

### D2: Structural Marker Design for Provisionally Resolved Disputes

**Parties**: integration-architect (P2) vs. game-engine-advocate (P2, with specific marker names)
**Status**: Agreed on need, minor design question on marker naming. game-engine-advocate proposes `PROVISIONALLY_RESOLVED_BEGIN`/`PROVISIONALLY_RESOLVED_END`. integration-architect suggests aligning with the existing `DISPUTES_BEGIN`/`DISPUTES_END` naming pattern. Both names work; the design choice is cosmetic.

**integration-architect position**: Use `PROVISIONALLY_RESOLVED_BEGIN`/`PROVISIONALLY_RESOLVED_END` to parallel `DISPUTES_BEGIN`/`DISPUTES_END`. The naming is descriptive and self-documenting. No real dispute here.

## Convergence

The following recommendations have full three-agent consensus after the revision cycle:

**P1 (3 items, unanimous):**
1. Add influence-aware heading data to ArbitrationConfig model + cooperative.yml schema
2. Wire `{ARBITRATION_PATHS}` into cross-round synthesis template "What to Read" section
3. Wire `{ARBITRATION_RULINGS}` into cross-round synthesis template Resolution Attribution section

**P2 (6 items, majority or unanimous):**
4. Use Phase enum in validate.py (functional-typing + integration-architect)
5. Type VariableDefinition.phases as list[Phase] (functional-typing + integration-architect)
6. Document linter static-vs-runtime heading validation boundary (all three)
7. Add structural markers for provisionally resolved disputes (integration-architect + game-engine-advocate)
8. Fix conversus.yml doc paths (game-engine-advocate + integration-architect)
9. Document that config_conditions are metadata-only, not linter-enforced (functional-typing + integration-architect)

**P3 (5 items):**
10. Normalize ConfigCondition operators in variables.yml (game-engine-advocate)
11. Reclassify semantic misuses of ErrorType (functional-typing)
12. Create ConversusConfig Pydantic model with extensible extra policy (functional-typing)
13. Add stagnation-influence interaction documentation in SKILL.md (integration-architect)
14. Add PRIOR_ARBITRATION_PATH model_validator on ReviewContext (functional-typing)

**Withdrawn (2 items):**
- Plugin hook comments in SKILL.md (game-engine-advocate, withdrawn)
- Influence dispatch externalization into schema/influence-levels.yml (game-engine-advocate, withdrawn)

## Final Position Statement

The integration-architect's position after the full deliberation:

Spec 006 is a comprehensive and well-structured extension to the arbiter subsystem. All 23 functional requirements have corresponding implementation artifacts. The backward compatibility story is clean: omitting both `timing` and `influence` produces pre-spec-006 behavior.

The integration-architect's unique contribution is identifying the template wiring gaps that other agents missed. The {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} variables are fully provisioned in the schema, Pydantic models, and SKILL.md documentation -- but the cross-round synthesis template, which is the sole consumer, does not reference them. This is the most consequential finding because it means the cross-round synthesizer will produce Resolution Attribution without reading the actual arbitration files, relying on inference from round syntheses instead of explicit data.

The integration-architect adopted two functional-typing recommendations (Phase enum usage, VariableDefinition.phases typing) that strengthen the codebase without conflicting with integration concerns. The integration-architect also conceded to functional-typing on the config_conditions documentation sequencing -- documenting metadata-only status first is safer than changing required statuses before the evaluation mechanism exists.

The deliberation process worked effectively: each agent identified gaps the others missed (functional-typing: type-system layer; game-engine-advocate: extensibility architecture; integration-architect: template wiring). The cross-review cycle produced genuine priority adjustments and two withdrawn recommendations, indicating the agents engaged substantively rather than defensively.
