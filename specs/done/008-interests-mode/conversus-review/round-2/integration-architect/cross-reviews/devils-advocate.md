# Cross-Review of devils-advocate Round 2
**Reviewer**: integration-architect
**Target**: devils-advocate Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: AR-1 proposes a hard stop that contradicts the arbiter's "recommend, do not require" resolution

Devils-advocate's AR-1 prescribes that if the user declines both choosing a calibration style and running `/conversus define`, the interests handler should "stop processing" with a hard message: "Cannot generate calibrated interest prompts without a problem type." This is framed as closing an unspecified exit state in K-2, but it actually contradicts the arbiter's resolution of Dispute 1.

The arbiter's opinion (resolution.md, lines 56-62) explicitly warned against making every CLARIFY tag mandatory: "If the interests handler always bounces the user back to define, it effectively makes deferred resolution impossible — every CLARIFY tag becomes mandatory, which contradicts the define handler's design intent." The arbiter chose the word "recommend" as load-bearing (resolution.md, line 62) precisely to preserve the define handler's deferred-resolution semantics (SKILL.md line 889).

AR-1's hard stop in the third exit state reintroduces the problem the arbiter identified. If the user declines to choose a type *and* declines to go back to define, then the only outcome is the handler refuses to proceed. The user has no path forward except running `/conversus define` — which means the interests handler does in fact *require* define, just with an extra interaction step. The "recommend, do not require" semantics collapse into "recommend, and if they ignore the recommendation, require."

I accept that the third exit state needs specification. But the resolution should honor deferred resolution: if the user declines both options on a second presentation, the handler should warn that interest prompts will use generic calibration (not type-specific), state this explicitly, and proceed with user confirmation. This is not a silent default — it is a user-confirmed degraded mode. The alternative (hard stop) turns the CLARIFY tag from "deferred resolution" into "deferred requirement," which is architecturally different from what the define handler promises.

### DC-2: OBA-1 mischaracterizes the arbiter's general observation 7

Devils-advocate claims the arbiter "underweights" the architectural dimension of Dispute 1 by calling all three disputes "about language, not architecture" (OBA-1). But the arbiter's observation 7 is a summary characterization of the dispute *surface area*, not a claim that no architectural implications exist anywhere in the deliberation. The arbiter's own Dispute 1 opinion (resolution.md, lines 56-68) spends six paragraphs analyzing the architectural implications — the User Confirmation Gate, Domain Agnosticism, deferred resolution design, the difference between the interests handler's input space and the mode handler's input space. The arbiter clearly engaged with the architecture.

The observation that "all three disputes are about language, not architecture" is accurate *at the dispute level*: no reviewer proposed changing the handler's control flow, adding new commands, or restructuring the prerequisite chain. The disputes concern what words to use in user-facing prompts, how to describe a flag, and how to frame a config. These are language decisions — they happen to have architectural consequences (as devils-advocate correctly notes about the hard-stop vs. proceed-with-degradation choice), but the disputes themselves are expressed as framing disagreements.

More importantly, devils-advocate's challenge in OBA-1 is rendered moot by the fact that the arbiter's opinion on Dispute 1 *already addresses* the architectural dimension. The arbiter explicitly warns against making CLARIFY tags mandatory (resolution.md, line 60) and distinguishes between the interests handler and mode handler input spaces (resolution.md, lines 64-65). Claiming the arbiter "underweights" the architecture in a summary sentence, when the detailed opinion demonstrably engages with it, conflates a headline with the analysis beneath it.

---

## Tensions

### T-1: MO-1 cost estimate improvement is sound, but Option (b) overstates the case against the formula

Devils-advocate's MO-1 correctly identifies that displaying `N^2 + N + 1` at mode confirmation is implementer-facing information in a user-facing context. The point about the formula assuming no arbiter is well-taken — the generated config always has rounds=1 and no arbiter, so the handler can compute an exact number.

However, Option (b) ("Omit the formula and use a plain count") and my own AR-3 from Round 2 ("Qualify the formula with its cross-review assumption") are in tension. Both identify the same problem — the formula's assumptions are unexplained — but propose different solutions. Devils-advocate wants to hide the formula entirely; I proposed making its assumptions explicit.

The tension resolves in devils-advocate's favor for the specific case of the mode confirmation display. At confirmation time, the handler knows N, knows rounds=1, and knows arbiter=absent. There is no reason to display a formula the user must mentally evaluate when the handler can display the result. My AR-3 is better suited for documentation (the Important Notes section) where the formula serves an explanatory purpose. For the user-facing confirmation, a computed count is the right choice.

I accept devils-advocate's Option (b) for the mode confirmation display. My AR-3 should be redirected to qualify the formula in the Important Notes section (SKILL.md lines 1304-1308), not in the user-facing K-5 text.

### T-2: AR-3 (naming pattern to interest structure) and my AR-1 (naming pattern mapping table) target the same gap differently

Devils-advocate's AR-3 proposes replacing "naming pattern" with "interest structure (names, perspectives, and prompts)" in C-7's cross-validation description. My Round 2 AR-1 proposes adding an explicit naming-pattern-to-type mapping table to K-6. These are complementary, not contradictory, but they address the same underlying concern from different angles.

Devils-advocate's fix is more fundamental. If the cross-validation is supposed to examine the full interest structure (names, perspectives, and prompts), then my mapping table — which maps *naming patterns* to problem types — is insufficient. The mapping table would need to be expanded to describe how perspective language and prompt content also signal problem types, which makes it substantially more complex than the four-row table I proposed.

The resolution: adopt devils-advocate's wording change (replace "naming pattern" with "interest structure") *and* keep a simplified version of my mapping table as implementation guidance, but note that the table covers naming signals only and that implementers should also examine perspective and prompt content for type-consistent language. This gives implementers a concrete starting point (my table) while being honest that naming patterns alone are insufficient (devils-advocate's point).

### T-3: MO-2 (interest count cost note at confirmation) has merit but risks information overload

Devils-advocate's MO-2 proposes surfacing the agent-launch cost at the interests confirmation step (SKILL.md ~line 1008), not just at mode confirmation (C-6). The rationale is sound: by mode confirmation, interests are locked, so the user cannot remove an interest to reduce cost. Surfacing cost earlier gives users a decision point.

The tension is with information density at the interests confirmation step. The user is already being asked to confirm interest names, perspectives, and potentially ungrounded-agent warnings. Adding a cost estimate — which is approximate at this point because the mode is unknown — risks making the confirmation prompt feel like a wall of disclaimers rather than a clear decision point. The spec's constraint against requiring game theory knowledge (spec.md line 103) suggests keeping user-facing interactions clean.

Devils-advocate correctly grades this P3 and notes it is a UX improvement, not a correctness issue. I would refine the proposal: rather than embedding the cost scaling note directly in the confirmation prompt, surface it only when the interest count exceeds 3 (the point where quadratic scaling becomes materially expensive — 21 vs. 13 agent launches). For 2-3 interests the cost is modest enough that the note adds noise without decision value.

### T-4: The batch-mode / CI integration concern in OBA-1 is forward-looking but premature for spec 008

Devils-advocate's OBA-1 raises a valid future concern: if the interests handler treats type resolution as a hard prerequisite (via the K-2 user confirmation flow), then CLARIFY-tagged problems cannot flow through a non-interactive pipeline. This is a real architectural constraint.

However, spec 008 does not define batch mode or CI integration. The interests handler explicitly "executes entirely in the main conversation" (SKILL.md line 930) — it is inherently interactive. Designing the handler's CLARIFY-tag behavior around a non-interactive use case that does not yet exist would be speculative. My MO-1 from Round 2 (prerequisite chain state-machine formalization) already flags this category of concern for future specs. The right action is to acknowledge the constraint in a deferred-items note, not to change spec 008's interactive handler design to accommodate a hypothetical batch mode.

---

## Safe Agreements

### SA-1: All prior concessions are correctly respected

Devils-advocate explicitly affirms all Round 1 concessions (interests.md-as-optional, integration fallback default, fabricated confidence framing) and does not revisit any of them. This matches my position. The deliberation's settled items remain settled.

### SA-2: Convergence points C-1, C-2, C-3, C-5, C-9, C-10 are affirmed without reservation

Devils-advocate and I agree on all six convergence points that devils-advocate explicitly lists. No further deliberation is needed on these items.

### SA-3: Dispute 2 (`--output` framing) and Dispute 3 (config completeness) are settled

Devils-advocate accepts both the workspace-override framing for `--output` and the "complete config with extensions" framing. The arbiter's reasoning is endorsed. These disputes required no further Round 2 discussion, and neither review reopens them.

### SA-4: The cost estimate formula assumptions need qualification

Both reviews identify that the C-6/K-5 cost formula has unexplained assumptions. Devils-advocate (MO-1) focuses on the arbiter vs. no-arbiter distinction and the user-facing vs. implementer-facing framing. My review (OBA-1) focuses on the uniform cross-review assumption. Both concerns are valid and complementary. The combined fix — computed count for user-facing display, qualified formula for implementer-facing documentation — addresses both.

### SA-5: C-7 cross-validation needs more concrete implementation guidance

Both reviews identify that C-7's cross-validation description is too abstract for reliable implementation. Devils-advocate (OBA-2, AR-3) proposes broadening the signal source from naming patterns to full interest structures. My review (MO-2, AR-1) proposes adding an explicit mapping table. As noted in T-2, these are complementary improvements that should both be adopted.

### SA-6: The K-2 calibration style choices should use plain-language descriptions

Devils-advocate's alignment section on Dispute 1 notes that K-2 should present calibration styles in plain language, not using mode names. My AR-4 from Round 2 makes the same point and provides specific suggested text. We agree both on the principle and the rationale — the no-game-theory constraint (spec.md line 103) applies to calibration style selection, not just mode selection.

### SA-7: The executive-summary framing is accurate — Round 1 converged on *what* to fix but was less precise about *how*

Devils-advocate's executive summary observes that the synthesis prescribed fixes that introduce new ambiguities. My review's focus on implementation precision within converged recommendations reflects the same assessment. Both reviews treat Round 2 as the opportunity to tighten remediation language, not to reopen settled questions. This alignment on the purpose of Round 2 is productive.

### SA-8: The `(none)` sentinel mismatch is a real implementation hazard

Devils-advocate does not address the `(none)` sentinel mismatch (my MO-3/AR-2), but the issue is upstream of their concerns. The define handler writes `(none -- no context documents provided)` while the mode handler checks for `(none)`. Devils-advocate's focus on the cost formula and calibration style presentation does not conflict with my recommendation on sentinel matching. This is an independent P2 fix that both reviews implicitly support by neither contesting the deferred D-1 item from Round 1 nor proposing an alternative.
