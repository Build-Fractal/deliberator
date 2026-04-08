# Devils-Advocate Revision — Round 2

**Role**: devils-advocate
**Round**: 2 of 2 (Phase 3 — Cooperative Revision)
**Date**: 2026-03-22

---

## Recommendation Dispositions

### AR-1: Tighten K-2 (CLARIFY-tag handling) control flow [was P1] — REVISED, concede hard stop

Both cross-reviewers identified the same dangerous contradiction (functional-typing DC-1, integration-architect DC-1): my proposed hard stop contradicts the arbiter's "recommend, do not require" resolution and the define handler's deferred-resolution design (SKILL.md line 889). They are right.

I stated in my own Alignment section that "the word 'recommend' is the right verb, not 'require,'" and then prescribed a hard stop that functionally requires type resolution. That is an internal contradiction. I concede it.

**The gap is real; the resolution was wrong.** The third exit state (user declines both choosing a calibration style and returning to `/conversus define`) remains unspecified in K-2. Both cross-reviewers agree on this (functional-typing SA-1, integration-architect DC-1 paragraph 3). The disagreement is about what happens in that state.

**Revised position**: Adopt integration-architect's "user-confirmed degraded mode" approach. If the user declines to choose a calibration style and declines to run `/conversus define`, the handler should:

1. Explain that interest prompts will use generic calibration (not type-specific).
2. State this explicitly: "Without a problem type, interest prompts will use generic framing rather than type-calibrated prompts (e.g., adversarial for selection, cooperative for integration)."
3. Ask the user to confirm: "Proceed with generic calibration?"
4. If the user confirms, generate interests with generic prompts. This is not a silent default -- it is a user-confirmed degraded mode.
5. If the user declines, stop processing with the existing recommendation to run `/conversus define`.

This preserves deferred resolution, avoids silent defaults, and gives the user an explicit path forward. The hard stop I originally proposed was architecturally inconsistent with the design I had already accepted. Conceded.

**Revised priority**: P1 (the gap still needs closing; only the resolution changed).

### AR-2: Adjust C-6 cost estimate to use computed count, not formula [was P2] — MAINTAINED, accept priority downgrade to P3

Both cross-reviewers accept the substance of this recommendation. Functional-typing (SA-2) agrees with the computed count but argues P3 is more appropriate. Integration-architect (T-1) explicitly concedes in my favor for the mode confirmation display, accepting Option (b).

I accept the priority downgrade. Functional-typing's reasoning is sound: the formula is shown at mode confirmation time where the user has already expressed intent to proceed. A formula vs. a computed number is a presentation refinement. The C-6 convergence text already contextualizes the formula. P3 is appropriate.

**Revised priority**: P3.

### AR-3: Adjust C-7 cross-validation to reference full interest structure [was P2] — MAINTAINED

Both cross-reviewers accept this recommendation (functional-typing SA-3, integration-architect T-2). Integration-architect proposes combining my wording change with a simplified version of their mapping table as implementation guidance, noting the table covers naming signals while acknowledging that names alone are insufficient. This is a reasonable synthesis.

I accept the combined approach: replace "naming pattern" with "interest structure (names, perspectives, and prompts)" in C-7, and retain integration-architect's mapping table as one input signal among several, with a note that naming signals alone are insufficient for reliable type inference.

**Priority**: P2 (unchanged).

### AR-4: Add interest-count cost note at interests confirmation [was P3] — WITHDRAWN

Functional-typing identifies two problems: (1) T-2 argues this creates premature optimization pressure before the mode is known, and the Round 1 deliberation converged on placing the cost estimate at mode confirmation for exactly this reason; (2) T-4 identifies an internal inconsistency with AR-2 -- AR-2 says users should not see the formula, but AR-4 proposes showing the formula at an earlier step.

Both points are correct. The T-4 inconsistency is particularly damning: I cannot argue that `N^2 + N + 1` is too implementer-facing for mode confirmation while simultaneously proposing it at interests confirmation. And functional-typing's point about my own Round 1 concession (that mode is not yet selected at interests confirmation, so the cost formula depends on mode) applies directly here. I conceded this in Round 1 and am now relitigating it. That is inconsistent.

**Withdrawn.** The C-6 cost estimate at mode confirmation is the right placement. Users can still add or remove interests after seeing the cost at mode confirmation.

### MO-1: Cost estimate formula appears wrong — SUBSUMED by AR-2

The underlying observation (that the formula assumes no arbiter and single round, and that the user should see a computed count rather than a formula) is accepted by both cross-reviewers. AR-2 is the actionable form of this observation. MO-1 is not a separate recommendation; it is the motivation for AR-2.

### MO-2: No guidance on interest count vs. agent launch cost trade-off — WITHDRAWN (same as AR-4)

This is the missed-opportunity form of AR-4. Withdrawn for the same reasons.

### OBA-1: The arbiter treats all three disputes as purely about language — CONCEDE

Integration-architect's DC-2 makes the decisive point: the arbiter's general observation 7 is a summary characterization, not a claim that no architectural implications exist. The arbiter's Dispute 1 opinion spends six paragraphs analyzing architectural implications -- the User Confirmation Gate, Domain Agnosticism, deferred resolution, the difference between the interests handler's and mode handler's input spaces. The arbiter clearly engaged with the architecture. I conflated a headline with the analysis beneath it.

Functional-typing's DC-2 adds that I cannot simultaneously accept the interactive resolution and flag non-interactive support as an unacknowledged architectural consequence. If batch/CI mode is a real concern, the fix is to propose a deferred `--calibration <style>` flag for non-interactive contexts, not to critique the arbiter's framing.

Both are right. The arbiter did not underweight the architecture; my critique was misplaced. The forward-looking concern about non-interactive execution is valid but belongs as a deferred item, not as a challenge to the arbiter's characterization.

**Conceded.** The non-interactive execution concern is noted but deferred. It is not a spec 008 issue.

### OBA-2: The synthesis assumes interest-vs-type cross-validation is implementable as described — MAINTAINED as AR-3

This observation is accepted by both cross-reviewers and produces the accepted AR-3 recommendation. The observation stands; it is now fully captured by AR-3.

---

## New Recommendations

### NR-1: Specify the third exit state for CLARIFY-tag handling as user-confirmed degraded mode [P1]

This replaces the withdrawn hard-stop portion of AR-1 with the revised resolution described above. The K-2 fix text should add:

> "If the user declines to choose a calibration style and also declines to return to `/conversus define`, explain that interest prompts will use generic calibration rather than type-specific calibration. Ask the user to confirm proceeding with generic calibration. If confirmed, generate interests with generic prompts. If declined, stop processing with the recommendation to run `/conversus define`."

This is the only new recommendation. The remaining active items (AR-2, AR-3) are maintained from my original Round 2 review.

---

## Position Summary

**Active recommendations (3):**

| ID | Description | Priority | Status |
|---|---|---|---|
| NR-1 | Specify CLARIFY-tag third exit state as user-confirmed degraded mode | P1 | New (replaces AR-1 hard stop) |
| AR-2 | Display computed agent count, not formula, at mode confirmation | P3 | Maintained (priority downgraded from P2) |
| AR-3 | C-7 cross-validation should reference full interest structure, not naming patterns alone | P2 | Maintained |

**Withdrawn (2):**

| ID | Reason |
|---|---|
| AR-4 | Internal inconsistency with AR-2; relitigates Round 1 concession on cost estimate placement |
| MO-2 | Same as AR-4 |

**Conceded (2):**

| ID | Reason |
|---|---|
| AR-1 (hard stop) | Contradicts "recommend, do not require" principle and deferred-resolution design I had already accepted |
| OBA-1 | Conflated arbiter's summary headline with the detailed analysis; the arbiter engaged with architecture in full |

**Assessment**: The cross-reviews correctly identified two contradictions in my Round 2 review. My proposed hard stop for the CLARIFY-tag third exit state was inconsistent with positions I had accepted. My critique of the arbiter's "about language" observation ignored the detailed architectural analysis in the arbiter's opinion. Both concessions strengthen the deliberation's coherence. The remaining three recommendations are accepted by both cross-reviewers in substance and are ready for synthesis.
