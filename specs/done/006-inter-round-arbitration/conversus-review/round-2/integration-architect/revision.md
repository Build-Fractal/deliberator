# Revision -- integration-architect (Round 2)

## Recommendation Dispositions

### Rec 1: Wire {ARBITRATION_PATHS} into cross-round synthesis template (P1)
**Disposition: Maintain at P1.**
Both co-reviewers endorse the proposed template text. No design questions remain. The implementation is specified.

### Rec 2: Wire {ARBITRATION_RULINGS} into cross-round synthesis template (P1)
**Disposition: Maintain at P1.**
Both co-reviewers endorse the proposed template text and placement. No design questions remain.

### Rec 3: Add influence_headings to cooperative.yml and ArbitrationConfig (P1)
**Disposition: Maintain at P1, with static-vs-runtime clarification.**
All three agents converge on `dict[str, list[str]]` field type. functional-typing's cross-review raises a valid precision issue: the statement "the linter's heading validation should use influence_headings[level]" is incorrect. The linter validates templates statically and does not know the influence level at validation time. Correcting:
- **Linter (static)**: validates that the mode schema has an `influence_headings` section and that the template has `{INFLUENCE_LEVEL}`. Continues to validate headings against `required_headings` (binding default).
- **Orchestrator (runtime)**: uses `influence_headings[level]` for heading validation after Phase 6 output is produced (SKILL.md L640-655).

This is the SC1 boundary, correctly re-applied. Accepting functional-typing's correction.

### Rec 4: Establish P2 implementation sub-ordering (P2-meta)
**Disposition: Maintain.**
game-engine-advocate endorses the categorization (Round 2 NEW-2). No disagreement from functional-typing. The sub-ordering stands.

### Rec 5: Specify PRIOR_ARBITRATION_PATH formula explicitly (P2)
**Disposition: Maintain at P2.**
No disagreement. The explicit formula is deterministic and reproducible.

### Rec 6: Address provisional-resolution marker lifecycle (P2)
**Disposition: Maintain at P2. Lifecycle design is settled.**
Three-agent convergence: markers are round-scoped, re-opened disputes return to DISPUTES_BEGIN/DISPUTES_END. Mark as unstable per Principle II until validated by one spec. No remaining design questions.

### Rec 7: Verify template last-mile coverage (P2)
**Disposition: Maintain at P2, scope clarified.**
All three agents agree on the dual-track approach: document the manual audit practice now, build the linter --audit mode later. game-engine-advocate adds a valid constraint: the automated check should be advisory (not blocking) to handle variables provisioned for future specs. Accepted.

## New Recommendations

### NEW-1: Accept SC1 boundary correction from functional-typing (Priority: P1-clarification)
**Source: functional-typing cross-review of integration-architect Rec 3.**
The original Rec 3 conflated static and runtime validation for influence_headings. The correction is: influence_headings enables runtime heading validation in the orchestrator, not static validation in the linter. The linter validates against the binding default (`required_headings`). This is not a new recommendation but a correction to the P1 implementation specification. Documenting the boundary in validate.py (as a comment extending Round 1 P2 item 6) prevents future confusion.

### NEW-2: Confirm Phase enum items have three-agent consensus (Priority: P2)
**Source: game-engine-advocate Round 2 NEW-1 confirmation.**
game-engine-advocate explicitly confirms no objection to P2 items 4 (Phase enum in validate.py), 5 (VariableDefinition.phases typing), and 12 (match/case). These now have three-agent consensus, upgraded from functional-typing + integration-architect bilateral to unanimous.

## Position Summary

After cross-reviews, the integration-architect position has refined in one substantive way:

1. **SC1 boundary correction accepted**: The influence_headings Pydantic field and YAML data serve runtime validation, not static linting. The linter validates templates against binding-default headings. The orchestrator validates Phase 6 output against influence-specific headings at runtime. This correction from functional-typing is precise and correct.

2. **All P1 items are implementation-ready**: The three P1 items have exact template text (Recs 1, 2), exact YAML structure (functional-typing Rec 2), exact Pydantic field type (all three agents), and clear static-vs-runtime validation boundaries. No further design deliberation is needed.

3. **P2 sub-ordering accepted**: The P2-easy / P2-structural categorization enables incremental implementation. game-engine-advocate endorsement makes this three-agent consensus.

4. **Phase enum items upgraded to unanimous**: With game-engine-advocate's explicit confirmation, P2 items 4, 5, and 12 now have three-agent consensus.

The integration-architect's core position is unchanged: the template wiring gaps ({ARBITRATION_PATHS}, {ARBITRATION_RULINGS}) are the most consequential findings because they represent dead infrastructure. Round 2 has produced implementation-ready specifications for all P1 items and resolved the remaining P2 design questions.
