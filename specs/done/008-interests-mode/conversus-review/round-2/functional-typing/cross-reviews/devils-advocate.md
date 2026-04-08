# Cross-Review of devils-advocate Round 2

**Reviewer**: functional-typing
**Reviewing**: devils-advocate Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: AR-1's "hard stop" contradicts the define handler's deferred-resolution design

Devils-advocate's AR-1 proposes that when the user declines both choosing a calibration style and running `/conversus define`, the interests handler should stop processing with the message: "Cannot generate interests without a calibration style." This is framed as closing an unspecified exit state in K-2.

The problem is that this converts the interests handler into a hard gate on CLARIFY-tag resolution, which is exactly what the arbiter warned against (resolution.md lines 60-62): "If the interests handler always bounces the user back to define, it effectively makes deferred resolution impossible -- every CLARIFY tag becomes mandatory, which contradicts the define handler's design intent." The arbiter's reasoning was specifically about preserving the define handler's deferred-resolution design (SKILL.md line 889: "downstream commands decide how to handle this").

Devils-advocate acknowledges the arbiter's reasoning on the "recommend, do not require" distinction in the Alignment section, writing that the word "recommend" is the right verb, not "require." But then AR-1 prescribes a hard stop -- "Do not generate interests with uncalibrated prompts" -- which is functionally a requirement, not a recommendation. The user is given exactly two paths: choose a calibration style or leave. There is no "proceed with acknowledged uncertainty" path.

My Round 2 review accepted the synthesis recommendation as-is, which says: "If the user declines to choose, recommend running `/conversus define` to resolve the CLARIFY tag before proceeding. Do not silently extract the best-guess type or default to any calibration style." The synthesis does not specify a hard stop. Devils-advocate is adding a hard stop that the synthesis deliberately omitted.

The contradiction is between devils-advocate's stated acceptance of the synthesis ("the word 'recommend' is the right verb, not 'require'") and the actual behavior prescribed by AR-1 (a hard stop that requires resolution before the workflow can proceed).

**Resolution path**: The K-2 gap devils-advocate identifies is real -- the third exit state (user declines both choosing and returning to define) is underspecified. But the resolution should be consistent with the arbiter's deferred-resolution reasoning. Two options: (a) offer the choices one more time as devils-advocate suggests, but if the user still declines, generate interests with a warning that prompts are uncalibrated rather than hard-stopping, or (b) accept the hard stop but acknowledge explicitly that this makes CLARIFY-tag resolution mandatory for the interests handler, which narrows the define handler's deferred-resolution contract. Either is defensible, but presenting a hard stop while claiming alignment with "recommend, do not require" is not.

### DC-2: OBA-1 claims Dispute 1 has an "architectural dimension" while accepting a resolution that already accounts for it

Devils-advocate's OBA-1 argues the arbiter underweights the architectural significance of Dispute 1 by calling it "about language." The specific architectural concern is: "If a future spec (say, a batch mode or CI integration) needs to run the interests handler non-interactively, this architectural choice means CLARIFY-tagged problems cannot flow through the pipeline without manual intervention."

This is a valid forward-looking concern. But it contradicts devils-advocate's own acceptance of the synthesis resolution, which prescribes interactive user confirmation as the primary mechanism. The synthesis recommendation that devils-advocate accepts in the Alignment section -- "inline user confirmation with four calibration style choices" -- is inherently interactive. If the concern is that the interests handler must support non-interactive execution for future batch/CI specs, then the accepted resolution is already architecturally constrained in the way OBA-1 warns about. Devils-advocate cannot simultaneously accept the interactive resolution and flag non-interactive support as an unacknowledged architectural consequence of that resolution.

The deeper issue: if non-interactive execution is a real concern, the fix is not to call the arbiter's framing wrong. The fix is to propose a non-interactive fallback path (e.g., a `--calibration <style>` flag for CI contexts) as a deferred item. OBA-1 identifies a real design constraint but presents it as a critique of the arbiter's framing rather than as a constructive recommendation. That misplacement makes it a contradiction rather than an extension.

---

## Tensions

### T-1: MO-1 (cost formula display) is correct but the priority may be too high

Devils-advocate correctly identifies that displaying the formula `N^2 + N + 1` to users at mode confirmation is implementer-facing language in a user-facing context. The recommendation to compute the exact count and display it as a plain number (option b) is sound -- the mode handler knows N, knows rounds=1, and knows arbiter=absent for generated configs, so the computation is deterministic.

However, rating this P2 overweights the user impact. The formula is shown at mode confirmation time, where the user has already expressed intent to proceed. A formula vs. a computed number is a presentation refinement, not a correctness or usability issue. The C-6 convergence text already specifies "based on {count} agents in {mode} mode," which contextualizes the formula. This is P3 at most -- a polish item, not a gap.

My position: accept the substance (compute the count, display the number), adjust priority to P3.

### T-2: MO-2 (cost trade-off at interests confirmation) creates a premature optimization pressure

Devils-advocate proposes surfacing the agent-launch cost at interests confirmation time (SKILL.md ~line 1008), noting that the quadratic scaling is "mode-independent" because every mode runs N^2 cross-reviews. This is factually correct -- the cross-review matrix is always N*(N-1) regardless of mode.

The tension is with the User Confirmation Gate and the deliberation's own convergence on C-6. The Round 1 deliberation explicitly converged on placing the cost estimate at mode confirmation, not interests confirmation, because "mode is not yet selected at that point; the cost formula depends on mode" (devils-advocate's own Round 1 concession, synthesis Key Concessions, devils-advocate #3). Devils-advocate is now proposing a separate, earlier cost display at interests confirmation. While this does not contradict C-6 (it is additive), it creates a user experience problem: the user sees a cost warning before they know the mode, sees it again after they choose the mode, and must evaluate the same information twice. The first display is necessarily less accurate (it cannot account for arbiter, rounds, or mode-specific variations), which risks anchoring the user on an approximate number before they see the real one.

I agree that quadratic scaling is worth knowing, but the right place for this information is the mode confirmation (C-6), not the interests confirmation. Users can still add or remove interests after seeing the cost at mode confirmation.

My position: defer MO-2. The C-6 cost estimate at mode confirmation is sufficient.

### T-3: OBA-2 (interest-vs-type cross-validation) identifies a real implementation risk but understates the synthesis's intent

Devils-advocate correctly notes that interest names like `alpha` or `beta` cannot be reliably classified as "products/tools" vs. "teams/roles" from the name alone. The recommendation to replace "naming pattern" with "interest structure (names, perspectives, and prompts)" in C-7 is a good refinement.

The tension: devils-advocate frames this as the synthesis text "risking a naive implementation that pattern-matches on names." But the C-7 text in the synthesis says "interest structure's naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles)" -- it uses "interest structure" as the subject, with the parenthetical as example categories, not as the sole input. A reasonable implementation would read the full interest structure to infer which category applies. The synthesis text is imprecise but not misleading.

That said, tightening the wording is low-cost and reduces implementation ambiguity. I accept AR-3's substance: replace "naming pattern" with "interest structure (names, perspectives, and prompts)" in C-7. The priority (P2) is appropriate.

### T-4: AR-4 duplicates C-6 at a different confirmation step

AR-4 proposes adding a cost note at interests confirmation using the formula `N^2 + N + 1`. This is the same formula that AR-2 argues should NOT be shown to users (replacing it with a computed count). AR-4 and AR-2 are internally inconsistent: AR-2 says users should not see the formula; AR-4 says users should see the formula at an earlier step. If the formula is too implementer-facing for mode confirmation (AR-2), it is also too implementer-facing for interests confirmation (AR-4).

This is a minor tension -- the intent (early cost awareness) is reasonable -- but the specific text of AR-4 contradicts the specific reasoning of AR-2.

### T-5: The "missed opportunities" framing risks scope creep in Round 2

Devils-advocate's Round 2 review introduces two missed opportunities (MO-1, MO-2) and two off-base assumptions (OBA-1, OBA-2), all of which are new items not surfaced in Round 1. Round 2 is described in the executive summary as "the last opportunity to tighten the remediation language before these changes are applied." Introducing new findings in Round 2 is legitimate, but four new items alongside four recommendations risks expanding the scope of the deliberation at a point where convergence is the goal.

This is not a blocking concern. MO-1 and OBA-2 (AR-3) are genuinely useful refinements. MO-2 and OBA-1 are less actionable. The tension is methodological, not substantive: Round 2 should prioritize closing gaps, not opening new ones.

---

## Safe Agreements

### SA-1: AR-1's identification of the third exit state is correct

Devils-advocate correctly identifies that K-2 does not specify what happens when the user declines both choosing a calibration style and running `/conversus define`. The synthesis text says "If the user declines to choose, recommend running `/conversus define`" but does not address the next step after the recommendation is also declined. This is a genuine gap in the K-2 fix text that should be closed. I disagree with the hard-stop resolution (see DC-1 above) but agree the gap exists.

### SA-2: AR-2's computed count over formula display is correct

The mode handler knows the exact values of N, rounds (always 1 for generated configs), and arbiter status (always absent for generated configs). Displaying a computed count like "Estimated agent launches: 13" is more user-friendly than "Estimated agent launches per round: N^2 + N + 1." I accept this refinement. The formula belongs in the SKILL.md's Important Notes section (implementer-facing), not in the user-facing mode confirmation. The priority should be P3 rather than P2.

### SA-3: AR-3's wording adjustment to C-7 is well-grounded

Replacing "naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles)" with "interest structure (names, perspectives, and prompts)" in C-7 reduces implementation ambiguity without changing the validation's purpose. Interest names alone are insufficient for reliable type inference. The Perspective and Prompt fields contain the semantic content needed for meaningful cross-validation. Accepted at P2.

### SA-4: All prior concessions are respected

Devils-advocate explicitly affirms all five Round 1 concessions and does not attempt to reopen any settled item. The review builds on the converged positions rather than relitigating them. This is consistent with my own approach in Round 2. The deliberation's convergence surface is preserved.

### SA-5: The executive summary's framing is productive

Devils-advocate's observation that "the deliberation converged on what to fix but was less rigorous about how to fix it" is a fair characterization of the Round 1 synthesis. Several of the K-items specify outcomes without specifying control flow (K-2 being the clearest example). Round 2 is the right time to tighten remediation language, and devils-advocate's contributions on AR-2 and AR-3 do exactly that.

### SA-6: MO-1 (cost formula accuracy) correctly distinguishes implementer-facing vs. user-facing information

The observation that the Important Notes section's formula (SKILL.md lines 1304-1308) serves implementers while the mode confirmation display serves users is architecturally sound. These are different audiences with different needs. Implementers need the formula to understand scaling behavior; users need a number to make a go/no-go decision. This distinction should inform how C-6 is applied.

### SA-7: All three disputes are correctly marked as resolved

Devils-advocate accepts all three dispute resolutions from the synthesis and arbiter without reopening any of them. Dispute 1 (CLARIFY-tag handling) is accepted with a qualification (the K-2 gap), Dispute 2 (--output framing) is accepted without reservation, and Dispute 3 (generated config completeness) is accepted without reservation. This matches my own Round 2 position on all three disputes.

---

## Summary

Devils-advocate's Round 2 review is focused and productive. The strongest contributions are AR-2 (computed count over formula), AR-3 (C-7 wording tightening), and the identification of the K-2 third exit state. The most significant concern is DC-1: AR-1 prescribes a hard stop that contradicts the define handler's deferred-resolution design and devils-advocate's own stated acceptance of the "recommend, do not require" principle. This should be resolved by either softening the hard stop to a warning-and-proceed path or by explicitly acknowledging that CLARIFY-tag resolution is mandatory for the interests handler.

The four new items (MO-1, MO-2, OBA-1, OBA-2) are mixed in value. AR-3 (from OBA-2) is a clear improvement. MO-1/AR-2 is correct in substance but overrated in priority. MO-2/AR-4 has an internal consistency issue with AR-2 and duplicates C-6's coverage. OBA-1 raises a valid forward-looking concern but misplaces it as a critique of the arbiter's framing rather than as a constructive deferred item.
