# Cross-Review: functional-typing reviewing integration-architect (Round 2)

**Reviewer**: functional-typing
**Reviewing**: integration-architect's Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: `## Status` heading count -- both reviews acknowledge 8 headings but integration-architect's recommendation table does not update Change 7

Integration-architect's RD-1 section states the `## Status` section should go into `problem.md` and invokes the "factual annotation" framing (IA review L57-59). My review explicitly flags that adopting `## Status` changes the heading count from 7 to 8 and that Change 7 rule (a) must be updated (FT review L102-105, Rec #1 at L129-131). Integration-architect's R7 entry in the recommendation table (IA review L183) says "Confirmed P2 majority, with diff summary as recommended practice" but does not mention the heading count update. Meanwhile, R10 (IA review L186) advocates `## Status` at P1.

The danger: if the synthesizer reads integration-architect's table literally, R7 (four refine invariants referencing "7 headings") and R10 (`## Status` adding an 8th heading) are mechanically inconsistent. Integration-architect acknowledges both changes individually but does not reconcile them. My review's Rec #1 (FT review L129-131) and Rec #3 (FT review L139-141) explicitly close this gap. The synthesizer must treat the heading count reconciliation as a mandatory mechanical fix, not an optional addition.

**IA evidence**: R7 at L183 ("four-rule minimal contract"), R10 at L186 ("`## Status` section").
**FT evidence**: MO-1 at L101-105, Rec #1 at L129-131, Rec #3 at L139-141.

### DC-2: Refine invariants -- integration-architect holds at four rules; I require five

Integration-architect's RD-5 position (IA review L113-128) maintains the four-rule contract: (a) headings preserved, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated. The review explicitly says "I adopt the arbiter's formulation in full" (IA review L119) and makes no mention of Status re-evaluation during refine operations.

My review adds a fifth invariant: (e) Status re-evaluated based on `[CLARIFY:]` tag count in the refined output (FT review L107-111, Rec #3 at L139-141). This is a mechanical consequence of adopting both `## Status` (RD-1) and the refine contract (RD-5). If a refine resolves all `[CLARIFY:]` tags, the status must flip from `draft` to `ready`. If a refine introduces new ambiguity, it must flip back. Without rule (e), the `## Status` field can become stale after a refine -- a factual annotation that states a falsehood.

The contradiction: integration-architect strongly advocates `## Status` as a factual annotation (IA review L57: "It is a fact: 'this artifact has N unresolved items'"), but does not ensure the fact remains accurate after refine operations. The factual-annotation framing requires the fact to be maintained on every write path. Integration-architect's four-rule contract leaves a write path (refine) that can produce a stale fact.

**IA evidence**: RD-5 at L113-128 (four rules only), RD-1 at L57 ("It is a fact").
**FT evidence**: MO-2 at L107-111, Rec #3 at L139-141 (fifth invariant).
**Spec evidence**: SKILL.md L865 (count computed from final output), SKILL.md L791 (refine path).

---

## Tensions

### T-1: `## Status` placement in the schema -- agreement on inclusion, tension on specification depth

Integration-architect advocates the `## Status` section and states it should satisfy my "boundary concern" (IA review L59). My review concedes and accepts the factual-annotation framing (FT review L56-58). However, I impose three explicit conditions on the concession (FT review L61-63):
1. The define handler sets the status; spec 007 does not state what consumers do with it.
2. No RFC 2119 SHOULD language prescribing downstream behavior.
3. The `## Status` section goes between `# Problem Definition` and `## Decision`, making the total heading count 8.

Integration-architect's review does not address condition 3 (schema ordering). The review mentions the non-expert user seeing "## Status: draft -- 3 items need clarification" (IA review L61) but does not specify where in the schema the section sits. My review pins it between `# Problem Definition` and `## Decision` (FT review L63) and further notes that spec.md L45-71 must be updated to include it (FT review MO-3, L113-115).

This is a tension, not a contradiction: both reviews agree on inclusion, but the integration point in the schema is specified only by my review. The synthesizer must resolve the placement.

**IA evidence**: RD-1 at L51-63 (advocates `## Status`, no placement specified).
**FT evidence**: RD-1 concession conditions at L61-63 (placement specified), MO-3 at L113-115.
**Spec evidence**: spec.md L45-71 (current schema, no `## Status`), SKILL.md L822-850 (current schema, no `## Status`).

### T-2: Scope of "missed opportunities" -- integration-architect introduces new material (MO-2: problem.md vs. conversus.yml) not in functional-typing's analysis

Integration-architect's MO-2 (IA review L142-147) proposes a documentation sentence clarifying that `problem.md` and `conversus.yml` are independent artifacts for different workflow paths. This is grounded in SKILL.md L36-42 (run handler looks for `conversus.yml`) and L769-876 (define handler produces `problem.md`). Integration-architect adds this as new recommendation R15 at P3 (IA review L201).

My review does not identify this gap. I do not contest the observation -- the two artifacts do coexist with no stated interaction, and a clarifying sentence is reasonable. However, the R15 recommendation introduces a new spec change in the final round of review. Per the deliberation protocol, new material in Round 2 has not been subjected to adversarial scrutiny. The synthesizer should note that R15 is single-advocate, single-round material and weight it accordingly (analogous to Change 12 in the Round 1 synthesis, which was also single-advocate).

**IA evidence**: MO-2 at L142-147, R15 at L201.
**FT evidence**: No corresponding analysis.

### T-3: Idempotency on `ready` problem.md -- integration-architect raises, functional-typing does not

Integration-architect's MO-1 (IA review L134-140) asks what happens when a user runs `/conversus define` against a `problem.md` that is already `status: ready` with zero `[CLARIFY:]` tags. The concern is that refine rule (d) ("Type re-evaluated") implies re-evaluation even when no new information is provided, and the scope of that re-evaluation is undefined.

My review does not address this case. I agree the observation is valid at P3 -- it is a real edge case that will surface in practice. But integration-architect's own assessment is correct: "The define handler's judgment is adequate" (IA review L138). FR-011 (spec.md L40) already governs this interaction: the agent presents the existing file and asks refine/replace. The scope of re-evaluation during a no-op refine is appropriately left to handler judgment at the spec 007 level.

**IA evidence**: MO-1 at L134-140.
**FT evidence**: Not addressed.
**Spec evidence**: spec.md L40 (FR-011), SKILL.md L786-793 (existing file check).

### T-4: Priority assignment for `## Status` -- integration-architect maintains P1, synthesis rated it disputed

Integration-architect's R10 (IA review L186) states: "Maintained P1 from my position; synthesis rates disputed." This is transparent about the disagreement with the synthesis priority assignment, but the review accepts the synthesis assignment while maintaining its own view. My review concedes on the substance of `## Status` (FT review L56-58) but does not explicitly re-rate its priority. My Rec #1 (FT review L129-131) treats heading count reconciliation as P1, which implicitly treats `## Status` adoption as settled but does not assign the `## Status` change itself a priority tier.

The tension: integration-architect wants `## Status` at P1. The Round 1 synthesis rated it disputed. My concession removes the dispute but does not explicitly upgrade the priority. The synthesizer must determine whether my concession (removing the sole objection) elevates `## Status` to P1 or whether it remains at the synthesis's assigned level.

**IA evidence**: R10 at L186 (P1 maintained).
**FT evidence**: RD-1 concession at L56-63 (substance conceded, no priority re-assignment).

---

## Safe Agreements

### SA-1: All 13 Round 1 convergence points are reaffirmed without modification

Integration-architect explicitly reaffirms C-1 through C-13 (IA review L20-32). My review reaffirms C-1 through C-13 (FT review L19-27). Neither review reverses or modifies any prior convergence point. The three P1 changes (post-write schema validation, `--context` path validation, dispatch matching) are unanimously confirmed in both reviews.

**IA evidence**: L20-32 (convergence reaffirmation).
**FT evidence**: L19-27 (convergence reaffirmation).

### SA-2: All Round 1 concessions are maintained -- no reversals in either review

Integration-architect confirms all six concessions from Round 1 without reversal (IA review L36-45). My review does not reverse any prior concession and adds two new concessions (RD-1 and RD-2). Both reviews demonstrate deliberative stability: positions move toward convergence, not away from it.

**IA evidence**: L36-45 (concessions maintained).
**FT evidence**: RD-1 concession at L56-63, RD-2 concession at L65-71.

### SA-3: `## Status` as factual annotation -- both reviews adopt the arbiter's framing

Integration-architect adopts the arbiter's "factual annotation" framing "without reservation" (IA review L57). My review concedes and states: "The arbiter's factual-annotation framing resolves my boundary concern" (FT review L58). Both reviews reject devils-advocate's RFC 2119 SHOULD language for downstream consumers. Both ground the field in the already-computed clarification count at SKILL.md L865.

**IA evidence**: RD-1 at L51-63.
**FT evidence**: RD-1 concession at L56-63.

### SA-4: Shared validation -- schema-layer prose contract, not dispatch-section infrastructure

Integration-architect maintains the schema-layer approach and adopts the arbiter's one-sentence prose formulation (IA review L67-83). My review concedes to the schema-layer approach "as articulated by the arbiter" (FT review L70-71). Both reviews agree that: (a) validation does not belong in the dispatch section at SKILL.md L18-34, (b) a shared function is premature abstraction for one producer and zero consumers, and (c) a prose contract at the schema level names the obligation without mandating infrastructure.

**IA evidence**: RD-2 at L67-83.
**FT evidence**: RD-2 concession at L65-71.

### SA-5: Multi-path `--context` deferred -- directory mechanism is the designed multi-source pattern

Both reviews maintain deferral on multi-path `--context`. Integration-architect states: "The single-path constraint is a scoping decision, not a design flaw" (IA review L95). My review states: "The directory mechanism is not a limitation -- it is the designed multi-source pattern" (FT review L78). Both ground this in SKILL.md L797 and FR-006 (spec.md L35). Both endorse Change 11 (document the constraint).

**IA evidence**: RD-3 at L87-97.
**FT evidence**: RD-3 at L73-79.

### SA-6: `--force` and `--dry-run` deferred -- automation context does not exist in spec 007

Both reviews maintain deferral. Integration-architect grounds this in FR-011's interactive safeguard (IA review L101-109). My review adds the arbiter's structural argument: `--dry-run` is unnecessary in an interactive context where the agent already presents the result (FT review L87). Both endorse Change 13 (documentation note).

**IA evidence**: RD-4 at L101-109.
**FT evidence**: RD-4 at L81-87.

### SA-7: Refine semantics -- four normative post-conditions, diff summary as recommended practice

Both reviews adopt the arbiter's distinction between structural invariants (normative) and diff summary (recommended practice). Integration-architect states: "The four-rule contract is normative. The diff summary is recommended practice" (IA review L119). My review states: "The four post-conditions... are structural invariants the agent can enforce. The diff summary is UX guidance" (FT review L95). Both endorse Change 7 from the synthesis.

Note: this agreement is on the four existing rules. The tension on whether a fifth rule (Status re-evaluation) should be added is documented in DC-2 above.

**IA evidence**: RD-5 at L113-128.
**FT evidence**: RD-5 at L89-95.

### SA-8: All 12 functional requirements are implemented -- no gaps

My review verifies all 12 FRs (FR-001 through FR-012) with specific SKILL.md line citations (FT review L31-46). Integration-architect does not repeat this verification in Round 2 but reaffirms "all convergence items C-1 through C-13" which include the FR coverage confirmation from Round 1. Neither review identifies an unimplemented or incorrectly implemented FR.

**IA evidence**: L20-23 (reaffirmation of Round 1 convergence).
**FT evidence**: L29-46 (FR coverage table).

### SA-9: No off-base assumptions identified in the other review's analysis

My review states: "None identified. The Round 1 deliberation was rigorous" (FT review L121). Integration-architect's OBA-1 (IA review L152-160) observes that composite decisions may map to multiple types, but explicitly states this is "not a spec change recommendation" and that the taxonomy closure consensus is correct. Neither review identifies foundational analytical errors in any agent's work.

**IA evidence**: OBA-1 at L152-160 (observation, not objection).
**FT evidence**: L119-121 (no off-base assumptions found).

---

## Summary for Synthesizer

**Convergence is strong.** Both reviews reaffirm all 13 Round 1 convergence points, maintain all prior concessions, and resolve RD-1 and RD-2 through concession to the arbiter's framing. RD-3, RD-4, and RD-5 are held at their majority positions by both reviews.

**Two items require synthesizer attention:**

1. **Heading count reconciliation** (DC-1): Both reviews adopt `## Status` but only my review explicitly reconciles the 7-to-8 heading count change across Changes 1, 7, and 10. The synthesizer must ensure this mechanical fix is applied.

2. **Fifth refine invariant** (DC-2): Integration-architect holds at four refine rules. I require a fifth (Status re-evaluation on refine). This is an unresolved disagreement with structural implications -- a `## Status` field that is not re-evaluated on refine violates the factual-annotation framing both reviews endorse.
