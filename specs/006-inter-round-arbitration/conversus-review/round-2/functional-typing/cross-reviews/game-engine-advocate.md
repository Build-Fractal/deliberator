# Cross-Review: functional-typing reviewing game-engine-advocate (Round 2)

## Overall Assessment

game-engine-advocate's Round 2 review is well-focused and constructive. The core contribution -- specifying the provisional-resolution marker lifecycle -- is the right question to answer in Round 2. The review correctly engages with the arbiter's observations (AO-5, Consideration 1, Consideration 4) and does not reverse any Round 1 concessions. The recommendation for string keys in influence_headings is a design question where the game-engine-advocate brings a unique perspective that merits engagement.

## Recommendation-by-Recommendation Assessment

### Rec 1: Specify provisional-resolution marker lifecycle (P2)

**Agreement: Strong.** The lifecycle question raised by the arbiter (AO-5) is real and needs resolution before the markers are declared. game-engine-advocate's proposed answer -- re-opened disputes move back to DISPUTES_BEGIN/DISPUTES_END, PROVISIONALLY_RESOLVED markers are round-scoped -- is correct and aligns with functional-typing's position (Round 2 Rec 6). This is the right design: each round's synthesis is a fresh categorization, and the structural markers reflect the current round's state. The convergence predictor use case strengthens the argument for structural markers over prose annotations.

### Rec 2: Ensure influence_headings YAML is plugin-extensible (P1-design)

**Partial agreement with nuance.** game-engine-advocate argues that `influence_headings` should use `dict[str, list[str]]` (string keys) rather than `dict[InfluenceLevel, list[str]]` (enum keys) to allow plugin-defined influence levels. This is consistent with Constitution Principle IX's distinction between closed behavioral choices (StrEnum for runtime dispatch) and open registries (str for schema data).

However, the functional-typing review (Round 2 Rec 1) also proposes `dict[str, list[str]]` -- the same conclusion, reached independently through different reasoning. functional-typing's rationale is practical: YAML deserialization produces strings, and mode schema files should not require enum awareness. game-engine-advocate's rationale is extensibility: plugin influence levels need to add entries.

Both rationales converge on the same type. This is a genuine convergence point, not a dispute.

### Rec 3: Formalize template last-mile audit (P2)

**Agreement with scope clarification.** The arbiter's Consideration 1 correctly identifies a systemic blind spot. game-engine-advocate proposes a linter check that verifies variables with `required: false` are consumed by at least one template. This is a good long-term goal, but the scope should be clear: this is a future linter enhancement, not a spec 006 change. The immediate action is documenting the manual audit practice. The linter enhancement belongs in a future spec.

### Rec 4: Document stagnation-influence interaction (P3)

**Agreement.** This was P3 item 16 in Round 1 and remains correctly prioritized. The arbiter's Consideration 4 raises the feedback loop concern, which is worth documenting. No priority change needed.

### Rec 5: Maintain game engine structural compatibility (confirmation)

**Acknowledged.** This is a confirmation, not a new recommendation. The game-engine-advocate is correct that the P1 implementation should preserve extensibility. No action needed beyond confirming that `dict[str, list[str]]` (not `dict[InfluenceLevel, list[str]]`) is the agreed field type.

## Gaps or Missed Points

- **No engagement with Phase enum adoption**: The game-engine-advocate review does not address P2 items 4, 5, or 12 (Phase enum in validate.py, VariableDefinition.phases typing, match/case). These items have functional-typing + integration-architect consensus from Round 1. game-engine-advocate should confirm or note any extensibility concerns.

- **Template last-mile audit scope**: The recommendation conflates a spec 006 action (documenting the manual practice) with a future linter enhancement (automated check). These should be separated: the manual practice is a P2 for this spec cycle; the automated check is a future spec.

## Tensions or Contradictions

None. game-engine-advocate's Round 2 recommendations complement rather than contradict functional-typing's positions. The influence_headings field type is a convergence point, not a tension.
