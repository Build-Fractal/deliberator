# Revision -- functional-typing (Round 2)

## Recommendation Dispositions

### Rec 1: Finalize influence_headings field type (P1)
**Disposition: Maintain at P1.**
Three-agent convergence on `dict[str, list[str]]` with string keys. functional-typing's rationale (YAML deserialization produces strings) and game-engine-advocate's rationale (plugin extensibility) both support the same type. integration-architect endorses the design. The field type is settled: `influence_headings: dict[str, list[str]] = Field(default_factory=dict)` on ArbitrationConfig. The existing `required_headings` serves as the binding headings -- no duplication.

### Rec 2: Add influence_headings to cooperative.yml (P1)
**Disposition: Maintain at P1.**
The proposed YAML structure is endorsed by all three agents. No cross-review disagreement. The structure is implementation-ready.

### Rec 3: Use Phase enum in validate.py (P2)
**Disposition: Maintain at P2.**
No new disagreement. game-engine-advocate confirms "no objection" via cross-review. The consensus from Round 1 (functional-typing + integration-architect, arbiter AO-4) holds.

### Rec 4: Type VariableDefinition.phases as list[Phase] (P2)
**Disposition: Maintain at P2.**
No new disagreement. Clean type improvement.

### Rec 5: Document config_conditions as metadata-only (P2)
**Disposition: Maintain at P2.**
Arbiter (AO-3) grounded this in Principle IV. All agents agree. No change.

### Rec 6: Address provisional-resolution marker lifecycle (P2)
**Disposition: Maintain at P2. Lifecycle design is settled.**
Three-agent convergence: markers are round-scoped, re-opened disputes return to DISPUTES_BEGIN/DISPUTES_END, PROVISIONALLY_RESOLVED markers exist only for disputes that remain provisionally resolved in the current round. Integration-architect adds: mark the markers as unstable per Principle II until one spec has consumed them successfully. Accepted.

### Rec 7: Use PHASE_CONTEXT_MODELS with Phase keys (P3)
**Disposition: Maintain at P3.**
Minor consistency improvement. No disagreement.

## New Recommendations

### NEW-1: Clarify static-vs-runtime boundary for influence_headings validation (Priority: P2)
**Source: Cross-review of integration-architect Rec 3.**
integration-architect's Rec 3 states "the linter's heading validation should use influence_headings[level]." This conflates static and runtime validation. The linter validates templates statically and does not know the influence level at validation time. The correct boundary:
- **Linter (static)**: validates that the template has `{INFLUENCE_LEVEL}` variable and that the mode schema has an `influence_headings` section. Continues to validate headings against `required_headings` (binding default).
- **Orchestrator (runtime)**: uses `influence_headings[level]` for the actual heading validation after Phase 6 produces output (SKILL.md L640-655).

This should be documented as a comment in validate.py (extending Round 1 P2 item 6) to prevent future contributors from attempting to push runtime logic into the linter.

### NEW-2: Acknowledge template last-mile audit practice (Priority: P2)
**Source: Cross-reviews from game-engine-advocate and integration-architect; arbiter Consideration 1.**
functional-typing's original review did not address the template last-mile audit. Both co-reviewers flag this gap. The immediate action is documenting the manual audit practice: "After adding a variable to variables.yml, verify at least one template in the corresponding phase references it." The linter enhancement (automated check) is a future spec. Adopting as P2 documentation item.

## Position Summary

After cross-reviews, the functional-typing position has refined in two ways:

1. **influence_headings field type settled**: Three-agent convergence on `dict[str, list[str]]` with string keys. The design is implementation-ready: Pydantic field on ArbitrationConfig, YAML data in cooperative.yml, runtime validation in SKILL.md orchestrator, static validation in the linter against the binding default.

2. **Static-vs-runtime validation boundary clarified**: Cross-reviewing integration-architect's Rec 3 revealed a precision issue. The influence_headings data enables runtime heading validation, not linter-time validation. This is the SC1 boundary from Round 1, re-applied to the P1 implementation. Documenting this boundary (NEW-1) extends Round 1 P2 item 6.

3. **Template last-mile audit adopted**: Both co-reviewers raised this gap. The arbiter flagged it as a systemic observation. functional-typing acknowledges the blind spot and adopts the documentation practice (NEW-2).

The core functional-typing position is unchanged: type safety and enum coverage are essential for maintainability. The Round 2 refinement is about implementation precision -- ensuring the P1 implementation correctly respects the static-vs-runtime validation boundary and that the type system design is unambiguous.
