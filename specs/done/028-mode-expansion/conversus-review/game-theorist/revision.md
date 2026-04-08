# Game Theorist — Round 1 Revision

## Changes Based on Cross-Review

### Concession 1: GT-R1-06 (Missing voting/social choice mode) — WITHDRAWN

The template engineer's cross-review correctly argues this is out of scope for spec 028. The current expansion is from 4 to 8 modes, and the 8 modes cover the vast majority of real-world multi-agent decision scenarios. Winner-take-all with multiple agents approximates committee voting sufficiently for the current scope. Adding a 9th mode would require a new game form (social choice functions) not currently in `schema/game-forms/`.

**Revision**: GT-R1-06 is withdrawn as a spec 028 concern. It may be relevant for a future spec but does not represent a gap in the current implementation.

### Modification 1: GT-R1-01 (Negotiation bayesian mapping) — REFRAMED

The spec compliance auditor's cross-review argues this is a violation of FR-002 because the spec says "Bayesian + Stackelberg" but the implementation maps only to bayesian. The auditor recommends: either fix the code or fix the spec.

The game theorist's original assessment was "PARTIALLY CORRECT" — the bayesian mapping is correct as the primary form, and the Stackelberg aspect is captured procedurally.

**Revision**: Reframed from "partially correct mapping" to "spec-implementation deviation requiring resolution." The game theorist recommends **updating the spec** (option a) rather than the code (option b), because:

1. The engine's mode-mapping supports a single `form` field per mode. Adding `secondary_form` would require schema changes beyond spec 028's scope.
2. The Stackelberg dynamics ARE implemented through the phase structure — this is not a missing feature, it is a different design choice.
3. The spec should document this design choice: "Negotiation mode maps to Bayesian game form. Sequential offer dynamics (Stackelberg) are captured by the engine's phase structure rather than the game form schema."

**Revised status**: The mapping is CORRECT as implemented. The SPEC should be updated to match the implementation.

### Modification 2: GT-R1-03 (keyword "settle" overlap) — ADOPTED as LOW PRIORITY

The template engineer's cross-review agrees this is low-risk due to match-count tiebreaking. The spec compliance auditor did not challenge it.

**Revision**: Retained as a valid finding but downgraded to P3 recommendation. The match-count mechanism provides sufficient protection. If a future false positive is observed, the fix is: `settle(?:\s+(?:on\s+terms|the\s+dispute|a\s+deal|this))`.

### Maintained: GT-R1-04 ("ration" keyword bug)

All agents who reviewed this finding agree it is a real bug. The template engineer adopted it as a P1 recommendation. The spec compliance auditor notes it affects FR-007.

**No change**: This remains a P1 finding.

### Maintained: GT-R1-05 (Resource-allocation vs. fair-division user confusion)

The spec compliance auditor notes this does not affect FR-005 compliance but is a usability gap. The template engineer agrees disambiguation guidance would help.

**Revision**: Maintained as P3 recommendation. Add disambiguation guidance to `/conversus mode` output.

---

## Revised Summary

| Finding | Original | Revised |
|---------|----------|---------|
| negotiation -> bayesian | PARTIALLY CORRECT | CORRECT (spec should update) |
| resource-allocation -> coalitional | CORRECT | CORRECT (no change) |
| fair-division -> coalitional | CORRECT | CORRECT (no change) |
| mechanism-design -> mechanism-design | CORRECT | CORRECT (no change) |
| Keyword classifier | MOSTLY CORRECT | MOSTLY CORRECT (no change) |
| Redundancy check | PASS | PASS (no change) |
| Completeness check | PASS (one gap) | PASS (gap withdrawn) |

## Revised Recommendations

1. **P1 — Must**: Fix "ration" regex to avoid matching "rational." (Unchanged)
2. **P1 — Must**: Update spec Section 2.1 to document that Stackelberg dynamics are captured by the phase structure, removing the "Bayesian + Stackelberg" claim from the game form mapping. (Revised from "document why" to "update spec")
3. **P3 — Consider**: Add disambiguation guidance for resource-allocation vs. fair-division. (Unchanged)
4. **P3 — Consider**: Harden "settle" keyword if false positives observed. (Downgraded from P2)
