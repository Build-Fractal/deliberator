# Template Engineer — Round 1 Revision

## Changes Based on Cross-Review

### Concession 1: TE-R1-03 (Negotiation review structure) — WITHDRAWN

The game theorist's cross-review provides a compelling counter-argument. The negotiation review's structured format (Interests Declaration with priority classification, Opening Offer with measurable terms, ZOPA Assessment, Risk Factors) is not overly constraining — it is a **necessary information revelation mechanism** for Bayesian games with private information.

The game theorist correctly argues that without structured interest revelation, the mediator cannot perform ZOPA analysis. The cooperative mode's free-form review works because cooperative agents share goals; negotiation agents have conflicting interests and must be induced to reveal controlled amounts of private information.

**Revision**: Concern TE-R1-03 is withdrawn. The negotiation review template's structured format is the correct design choice.

### Concession 2: TE-R1-01 (TARGET_PATH vs. TARGET_FILES) — DOWNGRADED

The spec compliance auditor's cross-review argues this is a non-issue because the variable injection system is mode-agnostic. If it works for cooperative, it works for negotiation. The game theorist similarly notes this is an implementation detail.

**Revision**: TE-R1-01 is downgraded from "observation requiring verification" to "noted, no action needed." The engine's variable injection is tested elsewhere and is not a mode-expansion concern.

### Maintained: Empty test file (FAIL)

All three agents independently identified this as the primary gap. No cross-review challenged this finding. The test file must be populated.

### Maintained: TE-R1-02 (Cross-round-synthesis DISPUTES markers)

The spec compliance auditor notes that FR-008 specifically says "synthesis template" not "cross-round-synthesis template," so this is not a spec violation. However, from a template engineering perspective, the `schema/modes/*.yml` files require `cross_round_synthesis.structural_markers: true` for all new modes. If the cross-round-synthesis templates lack DISPUTES markers, multi-round deliberations will have broken dispute tracking.

**Revised framing**: This is not a spec 028 compliance issue but IS a functional correctness issue that should be verified as part of the mode expansion work. Downgraded from P2 to P3 recommendation.

### New Finding from Cross-Reviews

**TE-R1-04 (Game theorist's "ration" keyword bug)**: Adopted from game theorist's GT-R1-04. The template engineer agrees this is a real bug. The regex `ration` in the RESOURCE_ALLOCATION pattern matches "rational" which appears frequently in analytical texts. The fix is straightforward: `\bration(?:ing|ed)?\b` or `\bration\b`.

---

## Revised Summary

| Check | Original | Revised |
|-------|----------|---------|
| Structural validity | PASS | PASS (no change) |
| Dispute headings | PASS | PASS (no change) |
| DISPUTES markers | PASS | PASS (no change) |
| Quality parity | PASS (with concern TE-R1-03) | PASS (concern withdrawn) |
| Test coverage | FAIL | FAIL (no change) |

## Revised Recommendations

1. **P1 — Must**: `tests/test_mode_expansion.py` must contain tests. (Unchanged)
2. **P1 — Must**: Fix "ration" keyword regex to avoid matching "rational." (New, adopted from game theorist)
3. **P3 — Consider**: Verify cross-round-synthesis DISPUTES markers for new modes. (Downgraded from P2)
