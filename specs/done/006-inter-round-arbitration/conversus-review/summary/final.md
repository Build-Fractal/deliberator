# Cross-Round Synthesis -- Spec 006: Inter-Round Arbitration

**Spec**: 006-inter-round-arbitration
**Agents**: functional-typing, game-engine-advocate, integration-architect
**Arbiter**: conversus-constitution (grounding: constitution.md v1.5.0)
**Arbiter Influence**: advisory
**Arbiter Timing**: inter-round
**Rounds**: 2 of 2
**Termination**: converged (0 disputes after Round 2)
**Date**: 2026-03-22

---

## Process Summary

Three agents conducted a 2-round cooperative deliberation on spec 006 (Inter-Round Arbitration with Influence Control). The deliberation was itself a live exercise of the spec's subject matter: an advisory arbiter (conversus-constitution) operated inter-round, reviewing the Round 1 synthesis and issuing advisory opinions before Round 2 began.

**Round 1** produced 22 original recommendations across the three agents, which were reduced to 18 through cross-review (2 withdrawn by game-engine-advocate, 2 priority downgrades by functional-typing). One dispute surfaced (config_conditions documentation sequencing) and was resolved through integration-architect's concession within Round 1. The three agents converged on 7 unanimous positions and identified 3 systemic contradictions (all architectural boundaries, not bugs).

**Inter-round arbitration** issued 7 advisory opinions (AO-1 through AO-7) and 4 considerations for Round 2. The advisory opinions affirmed the P1 items, confirmed the static-vs-runtime boundary, validated the dispute resolution and withdrawals, and raised design questions about provisional-resolution marker lifecycle and P2 sub-ordering.

**Round 2** consumed the advisory arbitration and produced implementation-ready specifications for all 3 P1 items, resolved remaining P2 design questions, upgraded 3 items from bilateral to unanimous consensus, added 4 new items (3 P2, 1 P3), and closed with zero disputes.

---

## Dispute Trajectory

| Metric | After Round 1 | Advisory Opinion | After Round 2 |
|--------|--------------|------------------|---------------|
| Active disputes | 0 (1 surfaced and resolved within Round 1) | Confirmed resolution was sound (AO-3) | 0 |
| Unresolved design questions | 4 (influence_headings type, provisional marker lifecycle, SC1 boundary for influence_headings, P2 ordering) | Raised 2 additional considerations (marker lifecycle, stagnation-influence) | 0 |
| Items at unanimous consensus | 7 of 18 | N/A | 10 of 18 (original) + 3 of 4 (new) |

The single dispute (config_conditions documentation sequencing, RD1) was raised and resolved entirely within Round 1. integration-architect conceded to functional-typing's documentation-first approach. The arbiter's advisory opinion (AO-3) confirmed the resolution was sound under Principle IV but did not influence it -- the concession predated the arbitration.

No new disputes appeared in Round 2. The deliberation achieved monotonic convergence: each round strictly increased agreement without re-opening settled positions.

---

## Resolution Attribution

### Resolved by Agent Convergence (No Arbiter Influence)

These resolutions occurred in Round 1, before the advisory arbitration was available. The arbiter subsequently confirmed them but did not cause them.

| Resolution | Mechanism | Round |
|-----------|-----------|-------|
| config_conditions sequencing (RD1) | integration-architect conceded to documentation-first | Round 1 |
| Phase enum priority downgrade (P1 to P2) | functional-typing accepted integration-architect's pragmatism argument | Round 1 |
| ErrorType reclassification downgrade (P2 to P3) | functional-typing accepted integration-architect's no-downstream-impact argument | Round 1 |
| Plugin hook comments withdrawal | game-engine-advocate accepted SKILL.md executable spec argument | Round 1 |
| Influence dispatch externalization withdrawal | game-engine-advocate self-corrected via OBA-1 | Round 1 |
| Heading validation Option A over Option B | game-engine-advocate revised based on safety-net argument | Round 1 |

### Resolved by Agent Convergence (Arbiter Advisory May Have Contributed)

These resolutions occurred in Round 2 after agents received the advisory arbitration. Attribution is assessed below.

| Resolution | Mechanism | Round | Arbiter Advisory Relevance |
|-----------|-----------|-------|---------------------------|
| influence_headings field type (`dict[str, list[str]]`) | Three-agent independent convergence | Round 2 | AO-1 affirmed the approach but did not specify the type. Agents converged on the type independently. **Low influence.** |
| Phase enum items upgraded to unanimous | game-engine-advocate confirmed no objection | Round 2 | AO-4 noted the Principle IX grounding and validated the P2 downgrade. game-engine-advocate's confirmation may have been nudged by the arbiter's explicit endorsement. **Possible low influence.** |
| SC1 boundary applied to influence_headings | functional-typing identified that integration-architect's P1 Rec 3 conflated static/runtime validation | Round 2 | AO-2 confirmed SC1 was intentional architecture. This may have primed functional-typing to re-apply the boundary to the P1 implementation details. **Possible moderate influence.** |
| Provisional-resolution marker lifecycle | Three-agent convergence on round-scoped markers, unstable per Principle II | Round 2 | AO-5 explicitly raised the lifecycle question (re-opening semantics) and the stability classification. Agents directly addressed both points. **Likely moderate influence.** |
| Template last-mile audit practice | All three agents adopted | Round 2 | Consideration 1 proposed this practice. All three agents acknowledged the systemic blind spot and adopted the recommendation. **High influence** -- this item originated from the arbiter. |
| P2 sub-ordering (easy vs. structural) | Three-agent convergence | Round 2 | Consideration 3 proposed the distinction. integration-architect formalized it. **High influence** -- this organizational structure originated from the arbiter. |
| Stagnation-influence interaction endorsement | game-engine-advocate endorsed integration-architect's P3 item | Round 2 | Consideration 4 highlighted the subtle feedback loop. game-engine-advocate's endorsement may have been influenced by the arbiter's analysis. **Possible moderate influence.** |

### Influence Assessment Summary

The advisory arbiter's influence was **measurable but non-coercive**. Of 13 total resolutions across both rounds:

- **6 resolutions** (46%) occurred in Round 1 with zero arbiter involvement. These demonstrate that agents can self-resolve effectively through direct cross-review engagement.
- **5 resolutions** (38%) occurred in Round 2 with possible-to-moderate arbiter influence. The arbiter's opinions provided constitutional grounding and raised design questions that agents then addressed, but the agents arrived at their own positions rather than adopting the arbiter's positions wholesale.
- **2 items** (15%) originated directly from the arbiter's considerations (template last-mile audit, P2 sub-ordering). These were process improvements rather than substantive design positions -- the arbiter contributed organizational clarity, not design direction.

No agent cited the arbiter's advisory opinions as a reason to change a substantive position. The arbiter's primary contribution was framing (constitutional grounding, lifecycle questions, organizational suggestions) rather than position advocacy.

---

## Final Convergence Record

### P1 -- Must Address (3 items, all unanimous, implementation-ready)

**1. Add influence_headings to ArbitrationConfig and cooperative.yml**
- Field: `influence_headings: dict[str, list[str]] = Field(default_factory=dict)` on `ArbitrationConfig`
- YAML: `influence_headings` section in `schema/modes/cooperative.yml` with heading lists for `recommended` and `advisory`
- Default `required_headings` serves as `binding` headings (no duplication)
- Runtime heading validation in SKILL.md uses `influence_headings[level]` when non-binding; linter (static) continues to validate against `required_headings` only
- Files: `linter/models.py`, `schema/modes/cooperative.yml`, `SKILL.md`

**2. Wire {ARBITRATION_PATHS} into cross-round synthesis template**
- Add conditional reading instruction in "What to Read" section referencing `{ARBITRATION_PATHS}` for inter-round arbitration scenarios
- Files: `templates/cooperative/cross-round-synthesis.md`

**3. Wire {ARBITRATION_RULINGS} into cross-round synthesis template**
- Add `{ARBITRATION_RULINGS}` in Resolution Attribution section as pre-formatted arbiter ruling content
- Files: `templates/cooperative/cross-round-synthesis.md`

### P2 -- Should Address (13 items; sub-ordered as P2-easy then P2-structural)

**P2-easy (documentation and path fixes):**

| # | Recommendation | Consensus | Files |
|---|---------------|-----------|-------|
| 4 | Fix conversus.yml doc paths (game-engine-advocate) | Unanimous | `conversus.yml` |
| 5 | Add PRIOR_ARBITRATION_SECTION field documentation | Bilateral (IA+FT) | `linter/models.py` |
| 6 | Specify PRIOR_ARBITRATION_PATH formula explicitly | Bilateral (IA+GEA) | `SKILL.md` |
| 7 | Document config_conditions as metadata-only | Bilateral (FT+IA) | `schema/variables.yml`, `linter/validate.py` |
| 8 | Document linter static-vs-runtime heading validation boundary (extended with influence_headings context) | Unanimous | `linter/validate.py` |
| 9 | Document template last-mile audit practice | Unanimous | `linter/validate.py` or separate documentation |

**P2-structural (type system and marker changes):**

| # | Recommendation | Consensus | Files |
|---|---------------|-----------|-------|
| 10 | Use Phase enum in validate.py | Unanimous | `linter/validate.py` |
| 11 | Type VariableDefinition.phases as list[Phase] | Unanimous | `linter/models.py` |
| 12 | Use match/case for phase-specific validation | Unanimous | `linter/validate.py` |
| 13 | Add structural markers for provisionally resolved disputes (round-scoped, unstable per Principle II) | Unanimous | `templates/cooperative/synthesis.md`, `SKILL.md` |
| 19 | Clarify static-vs-runtime boundary for influence_headings validation | Unanimous | `linter/validate.py` |
| 20 | Template last-mile audit practice (manual) | Unanimous | Documentation |
| 21 | P2 sub-ordering: P2-easy vs. P2-structural (meta) | Unanimous | N/A (process) |

### P3 -- Nice to Have (7 items)

| # | Recommendation | Consensus |
|---|---------------|-----------|
| 14 | Normalize ConfigCondition operators | Solo (GEA) |
| 15 | Reclassify ErrorType semantic misuses | Solo (FT) |
| 16 | Create ConversusConfig Pydantic model | Bilateral (FT+GEA) |
| 17 | Add stagnation-influence interaction documentation | Bilateral (IA+GEA) |
| 18 | Add PRIOR_ARBITRATION_PATH model_validator | Bilateral (FT+IA) |
| 19-P3 | Mark ARBITRATION_RULINGS as conditionally required (deferred until config_conditions evaluation exists) | Solo (IA) |
| 22 | PHASE_CONTEXT_MODELS with Phase keys | Solo (FT) |

### Withdrawn (2 items, sustained across both rounds)

- Plugin hook comments in SKILL.md (game-engine-advocate) -- SKILL.md is executable spec; archived references mislead
- Influence dispatch externalization (game-engine-advocate) -- premature abstraction; own OBA-1 undermined the case

---

<!-- CONVERSUS:DISPUTES_BEGIN -->

No remaining disputes.

All design questions have been resolved through agent convergence across two rounds of deliberation. The single dispute from Round 1 (config_conditions documentation sequencing) was resolved within Round 1 through concession and sustained without challenge in Round 2.

<!-- CONVERSUS:DISPUTES_END -->

---

## Termination Assessment

### Was termination appropriate?

Yes. Round 2 produced zero new disputes, resolved all remaining design questions, and upgraded 3 items from bilateral to unanimous consensus. All P1 items are implementation-ready with exact field types, YAML structures, and template text specified. Further rounds would not produce additional value.

### Was advisory influence effective?

**Yes, within its intended scope.** The advisory arbiter contributed in two distinct ways:

1. **Validation and constitutional grounding.** The arbiter confirmed that the agents' P1 priorities, dispute resolution, and withdrawals were well-grounded in constitutional principles. This is not mere rubber-stamping -- it provides confidence that the convergence is principled rather than coincidental. Agents in Round 2 could build on Round 1 positions knowing they had external validation.

2. **Design question elevation.** The arbiter's considerations (provisional marker lifecycle, template last-mile audit, P2 sub-ordering, stagnation-influence interaction) raised issues that agents had not surfaced on their own. Two of these (template last-mile audit, P2 sub-ordering) were adopted unanimously. This demonstrates the advisory arbiter's value as an "observer" per the spec's own game theory framework (Section 5): informational value without short-circuiting the deliberation.

### Did agents converge on their own or did the advisory nudge help?

**Both, on different items.** The deliberation naturally partitions into:

- **Self-resolved** (Round 1): All substantive design disputes, priority downgrades, and withdrawals. The agents demonstrated effective self-governance through cross-review engagement.
- **Arbiter-influenced** (Round 2): Process improvements and architectural precision. The arbiter raised questions (marker lifecycle, last-mile audit) that agents then resolved independently. The arbiter did not dictate answers; it identified gaps.

This pattern matches the spec's intended design for advisory influence: "The arbiter's value is informational -- providing a perspective agents may not have considered. Does not short-circuit the deliberation process."

### How would recommended or binding influence have changed the outcome?

- **Recommended influence** would likely have produced the same final positions but with a different process. The arbiter's lifecycle question (AO-5) would have carried "comply or explain" weight, potentially accelerating convergence on provisional marker design. However, the agents converged on their own within Round 2, so the acceleration would have been marginal.

- **Binding influence** would have been unnecessary and potentially counterproductive. The Round 1 dispute (config_conditions sequencing) was resolved through concession before arbitration fired. Binding rulings would have had nothing to bind. The design questions resolved in Round 2 were implementation details (field types, marker lifecycle) where binding authority would have been heavy-handed -- these are exactly the questions where agent expertise should prevail over arbiter diktat.

**Conclusion**: Advisory was the correct influence level for this deliberation. The agents self-resolved substantive disputes. The arbiter added value through framing and gap identification. A stronger influence level would have added overhead without improving outcomes.

---

## Systemic Contradictions (Final Status)

| ID | Contradiction | Status |
|----|--------------|--------|
| SC1 | Static linting vs. runtime configuration | Refined in Round 2: influence_headings serves runtime validation only. Boundary documented for implementation. |
| SC2 | config_conditions schema precision vs. enforcement gap | Unchanged. Document as metadata-only (P2). Defer evaluation to future spec. |
| SC3 | Typed pipeline vs. template last-mile | Addressed: manual audit practice adopted (P2). Automated linter --audit mode deferred as future enhancement. |

---

## Concessions (Complete Record)

**Round 1:**
1. functional-typing: Phase enum P1 to P2, ErrorType reclassification P2 to P3.
2. game-engine-advocate: Withdrew plugin hook comments and influence dispatch externalization; revised heading validation from Option B to Option A.
3. integration-architect: Conceded config_conditions sequencing (documentation-first).

**Round 2:**
4. integration-architect: Accepted SC1 boundary correction on influence_headings validation (runtime, not static).
5. game-engine-advocate: Reclassified "P1-design" to design constraint within P1 item 1.
6. functional-typing: Adopted template last-mile audit practice.

All concessions were sustained across rounds. No reversed positions.
