# Cross-Review: game-engine-advocate reviewing integration-architect (Round 2)

## Overall Assessment

integration-architect's Round 2 review is the most implementation-ready of the three. The concrete template wording proposals for P1 items 2 and 3 are directly insertable. The P2 sub-ordering (Rec 4) is a pragmatic contribution that makes the P2 tier actionable. The review correctly engages with the arbiter's observations and provides precise, deterministic specifications.

## Recommendation-by-Recommendation Assessment

### Rec 1: Wire {ARBITRATION_PATHS} into cross-round synthesis template (P1)

**Strong agreement.** The proposed template text is exact and correct. The conditional framing handles the empty-string case gracefully. No design questions remain.

### Rec 2: Wire {ARBITRATION_RULINGS} into cross-round synthesis template (P1)

**Strong agreement.** The instruction "cite the specific round and ruling rather than summarizing from the round synthesis" is a direct application of Principle VIII. The proposed placement in the Resolution Attribution section is correct.

From a game engine perspective, both {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} are exactly the data the post-deliberation hooks would consume. Wiring them into the template ensures the data flows through the existing pipeline, which the game engine can later tap into without restructuring.

### Rec 3: Add influence_headings to cooperative.yml and ArbitrationConfig (P1)

**Agreement with one clarification needed.** The proposed field type `dict[str, list[str]]` converges with all three agents. The fallback logic ("use influence_headings[level] when non-binding, fall back to required_headings for binding") is correct for runtime validation.

However, functional-typing's cross-review raises a valid point: this fallback logic applies to runtime orchestrator validation (SKILL.md L640-655), not to the linter. The linter validates templates statically and does not know the influence level. The integration-architect should clarify this boundary to avoid conflating static and runtime validation.

game-engine-advocate endorses the string-keyed design for plugin extensibility. The Pydantic model field `dict[str, list[str]]` accommodates plugin-defined influence levels without requiring enum changes.

### Rec 4: Establish P2 implementation sub-ordering (P2-meta)

**Strong agreement.** The P2-easy / P2-structural distinction is valuable for implementation planning. The categorization is correct:
- P2-easy: items 8, 10, 9, 11, 6 (documentation and path fixes)
- P2-structural: items 4, 5, 7, 12 (type system and markers)

This allows P2-easy items to be implemented immediately without blocking on the more complex structural changes.

### Rec 5: Specify PRIOR_ARBITRATION_PATH formula explicitly (P2)

**Agreement.** The explicit formula is deterministic and reproducible. This matters for the game engine because plugin developers need to compute these paths programmatically. An explicit formula is better than "infer from context."

### Rec 6: Address provisional-resolution marker lifecycle (P2)

**Strong agreement.** The integration-architect's proposal aligns with game-engine-advocate's Round 2 Rec 1 and functional-typing's Round 2 Rec 6. Three-agent convergence on the lifecycle design:
- Markers are round-scoped
- Re-opened disputes move back to DISPUTES_BEGIN/DISPUTES_END
- PROVISIONALLY_RESOLVED markers exist only for disputes that remain provisionally resolved in the current round

The stability recommendation (mark as unstable until validated) is correct per Principle II.

### Rec 7: Verify template last-mile coverage (P2)

**Agreement.** The dual-track approach (manual audit now, linter --audit mode later) is correct. game-engine-advocate's Round 2 Rec 3 proposes the same dual-track. The scope distinction (spec 006 action vs. future linter enhancement) should be made explicit.

## Gaps or Missed Points

- **No mention of stagnation-influence feedback loop**: The integration-architect does not address the arbiter's Consideration 4 (feedback loop where recommended influence prevents stagnation detection). This is a P3 item and may be outside the Round 2 scope, but it is worth noting for completeness.

## Tensions or Contradictions

- **Minor: SC1 boundary in Rec 3.** The integration-architect's Rec 3 says "the linter's heading validation should use influence_headings[level]." This conflates static and runtime validation. The linter cannot know the influence level at validation time. This should be clarified as a runtime validation change, not a linter change. This is a precision issue, not a substantive disagreement -- the integration-architect likely means the runtime heading validation in SKILL.md, not the static linter.
