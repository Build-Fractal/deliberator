# Devils-Advocate Review — Round 2
## Spec 008: Interest Discovery & Mode Selection

**Role**: devils-advocate
**Round**: 2 of 2
**Target**: `conversus/specs/008-interests-mode/spec.md` and `conversus/SKILL.md` (lines 926-1296)
**Prior**: Round 1 synthesis (`round-1/summary/final.md`) and arbiter opinions (`round-1/arbitration/resolution.md`)
**Date**: 2026-03-22

---

## Executive Summary

Round 1 was productive. Eight convergence points were established, three disputes were narrowed to language precision, and the arbiter's advisory opinions aligned with the synthesis recommendations on all three. I conceded five positions in Round 1 -- all correctly. I do not revisit any of them here.

That said, the Round 1 synthesis and arbiter opinions exhibit a pattern I want to challenge: premature closure on items where the agreed-upon fix is less precise than the problem it addresses. The convergence points are real, but several of the "Actionable Spec Changes" prescribe fixes that introduce new ambiguities or leave edge cases unspecified. The deliberation converged on *what* to fix but was less rigorous about *how* to fix it. Round 2 is the last opportunity to tighten the remediation language before these changes are applied.

I also identify two missed opportunities that were not surfaced in Round 1, and one assumption in the arbiter's reasoning that deserves scrutiny.

I respect all prior concessions. I am not reopening `interests.md`-as-optional, the `integration` fallback default, or the "fabricated" confidence framing. Those positions were wrong and were correctly abandoned.

---

## Alignment

### Convergence points I affirm without reservation

**C-1 (Ambiguous row)**: The SKILL.md's heuristic-detection-plus-user-choice is superior to the spec's static `cooperative` default. The spec should catch up. No further comment.

**C-2 (Preset field in schema)**: Correct. The spec schema should include the Preset field. The data flow from FR-006 makes this necessary, not optional.

**C-3 (Preset existence validation)**: Correct. A config that passes post-write validation but deterministically fails at run time is a validation gap. The proposed fix (resolve preset path, warn on failure) follows the existing pattern for docs paths (SKILL.md line 1271) and target paths (line 1266).

**C-5 (Draft status behavior)**: Correct. Warn and proceed. The define handler's deferred resolution design (SKILL.md line 889) means downstream handlers must tolerate draft status, not block on it.

**C-9 (interests.md is necessary)**: I conceded this in Round 1 for three concrete architectural reasons. It remains correct.

**C-10 (Staleness warning text)**: The SKILL.md wording is more precise than the spec's. No alignment needed.

### Dispute resolutions I accept from the synthesis

**Dispute 2 (--output framing)**: Integration-architect's workspace-override framing is correct. I originally suggested considering a flag split in Round 1 cross-review but did not reiterate it. The arbiter's analogy to `cd` is apt -- no one calls `cd` "dual semantics." The spec should document `--output` as a workspace directory override. Settled.

**Dispute 3 (Generated config completeness)**: I accept the "complete config with extensions" framing. The arbiter's observation that Schema Completeness via Defaults (SKILL.md lines 57-60) makes the config functionally identical to one with all optional fields set to their defaults is structurally decisive. My "starter template" framing was factually inaccurate -- a config that passes validation and runs successfully is not a starter template. The extension-points note in the mode handler's report (K-8) addresses my underlying concern about discoverability. Settled.

### Dispute resolution I accept with a qualification

**Dispute 1 (CLARIFY-tag handling)**: I accept the synthesis recommendation: inline user confirmation with four calibration style choices, "recommend `/conversus define`" as fallback, no silent default. The arbiter's reasoning is tight -- the User Confirmation Gate and Domain Agnosticism constraints together eliminate the `integration` fallback, and the define handler's deferred-resolution design means "recommend" is the right verb, not "require."

However, the K-2 fix text in the synthesis has a gap. It says: "If the user declines to choose, recommend running `/conversus define` to resolve the CLARIFY tag before proceeding." The word "before proceeding" is ambiguous. Does the interests handler stop processing after making the recommendation? Or does it wait for the user to respond, and if the user says "proceed anyway," generate interests without a calibration style? The fix text needs to specify the control flow:

- If the user chooses a calibration style: use it, proceed.
- If the user declines to choose and accepts the recommendation to run `/conversus define`: stop processing (same as the missing prerequisite behavior).
- If the user declines to choose but also declines to run `/conversus define`: what happens?

The third case is the one K-2 does not address. The user has declined to pick a type and declined to go back to define. The interests handler cannot generate calibrated prompts without a type. My position: the handler should explain that prompt calibration requires a type, offer the four choices one more time, and if the user still declines, stop processing with a clear message: "Cannot generate interests without a calibration style. Run `/conversus define` to set the problem type, or choose a calibration style above." This is not a silent default -- it is an explicit hard stop when the system genuinely cannot proceed without user input.

---

## Missed Opportunities

### MO-1: The cost estimate formula in C-6 appears wrong

Convergence C-6 prescribes adding to the mode confirmation: "Estimated agent launches per round: {N^2 + N + 1}." But the Important Notes section (SKILL.md lines 1304-1308) shows the formula depends on whether an arbiter is configured:

- Without arbiter: N^2 + N + 1
- With arbiter: N^2 + N + 2

The mode handler does not configure an arbiter -- the `arbiter` field is optional and is added manually (or by a future guided command). So at mode confirmation time, the arbiter status is unknown. Displaying `N^2 + N + 1` as the estimate is technically correct only for the no-arbiter case, but it creates a false sense of precision. Worse, for multi-round deliberation (rounds > 1), the per-round formula is different (SKILL.md line 1310), and the total includes a cross-round synthesis agent.

The fix should either:
- (a) State the formula explicitly as the single-round, no-arbiter case: "Estimated agent launches: {N^2 + N + 1} (single round, no arbiter)." This sets honest expectations.
- (b) Omit the formula and use a plain count: "This configuration will launch approximately {computed number} agents per round."

Option (b) is better because the mode handler knows the exact values of N, the round count (always 1 for generated configs), and the arbiter status (always absent for generated configs), so it can compute the exact number rather than displaying a formula that users must mentally evaluate. The formula is for the Important Notes section of the SKILL.md (implementer-facing), not for the user-facing mode confirmation.

**Priority**: P2. The current C-6 text is not wrong, but it displays implementer-facing information in a user-facing context.

### MO-2: No guidance on interest count vs. agent launch cost trade-off

The spec allows 2-5 interests (FR-001). The agent launch cost is quadratic in the number of interests (N^2 + N + 1). This means:

- 2 interests: 7 agent launches
- 3 interests: 13 agent launches
- 4 interests: 21 agent launches
- 5 interests: 31 agent launches

Going from 3 to 5 interests more than doubles the agent launches. Neither the spec nor the SKILL.md surfaces this trade-off to the user at interest confirmation time. The user has no information to make an informed decision about whether their 5th interest is worth 10 additional agent launches.

This is distinct from C-6 (which places the cost estimate at mode confirmation, after interests are already locked). The missed opportunity is at the interests confirmation step (SKILL.md line 1008), where the user is asked "Proceed with these interests?" At this point, the exact mode is unknown, but the quadratic scaling is mode-independent -- every mode runs N^2 cross-reviews. A sentence like "Note: Each additional interest significantly increases deliberation cost. 3 interests require ~13 agent launches; 5 interests require ~31." would help users make informed trade-offs.

**Priority**: P3. This is a user experience improvement, not a correctness issue. Users can always remove interests later.

---

## Off-Base Assumptions

### OBA-1: The arbiter treats all three disputes as purely about language

The arbiter's general observation 7 states: "All three disputes are about language, not architecture. No reviewer at any phase identified a blocking defect." This is true for Disputes 2 and 3, but Dispute 1 (CLARIFY-tag handling) has an architectural dimension that the arbiter underweights.

The CLARIFY-tag dispute is not just about what words to show the user. It is about control flow: what happens after the user interacts with the CLARIFY-tag prompt? The interests handler has four possible exit states from the CLARIFY interaction (choose a type, go back to define, decline both, or the case K-2 does not specify). The define handler's deferred-resolution design creates a genuine architectural question: should the interests handler support "proceed with acknowledged uncertainty" (generating interests without a calibrated type), or should it treat type resolution as a hard prerequisite?

The synthesis chose the hard prerequisite path (no silent default, recommend define, do not proceed without a choice). This is an architectural decision, not a language choice. It means the interests handler has a stricter prerequisite contract than `problem.md` existence alone -- it requires either an explicit type or a user-confirmed type. This is a valid design decision, but calling it "about language" understates its significance. If a future spec (say, a batch mode or CI integration) needs to run the interests handler non-interactively, this architectural choice means CLARIFY-tagged problems cannot flow through the pipeline without manual intervention. That is a design constraint worth acknowledging explicitly.

### OBA-2: The synthesis assumes interest-vs-type cross-validation (C-7) is implementable as described

Convergence C-7 prescribes checking "whether the interest structure's naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles) is consistent with the stated problem type." This assumes the mode handler can reliably classify interest names into these four categories. But interest names are user-defined strings matching `[a-z0-9][a-z0-9-_]*` -- they could be `alpha`, `beta`, `gamma`, or `team-backend`, `team-frontend`, or `hammer`, `screwdriver`.

The classification of `alpha` as a "product/tool" vs. a "team/role" is not determinable from the name alone. The handler would need to inspect the Perspective and Prompt fields to infer the interest's nature, which is a substantially more complex operation than "check the naming pattern."

I am not recommending removing C-7 -- the cross-validation concept is sound. But the implementation description should acknowledge that this validation operates on the full interest structure (name + perspective + prompt), not on naming patterns alone. The current text risks producing a naive implementation that pattern-matches on names and generates false warnings (e.g., warning that `alpha` and `beta` "suggest a selection problem" when they are team identifiers).

**Priority**: P2. The fix is a wording adjustment to C-7: replace "naming pattern" with "interest structure (names, perspectives, and prompts)."

---

## Actionable Recommendations

All recommendations below respect prior concessions and build on the converged positions from Round 1. None reverse settled items.

### AR-1: Tighten K-2 (CLARIFY-tag handling) control flow [P1]

Add explicit control flow for the case where the user declines both choosing a calibration style and running `/conversus define`:

> "If the user declines to choose a calibration style and also declines to return to `/conversus define`, explain that interest prompt calibration requires a problem type and stop processing: 'Cannot generate calibrated interest prompts without a problem type. Please either choose a calibration style or run `/conversus define` to set the type.' Do not generate interests with uncalibrated prompts."

This closes the unspecified third exit state identified in the Alignment section above.

### AR-2: Adjust C-6 cost estimate to use computed count, not formula [P2]

Replace the formula display with a computed count:

> "Estimated agent launches: {computed count} (based on {count} agents, single round, no arbiter)."

Since the mode handler knows N at confirmation time and the generated config always has rounds=1 and no arbiter, the exact count is deterministic. Display the result, not the formula. Users do not need to mentally evaluate N^2 + N + 1.

### AR-3: Adjust C-7 cross-validation description to reference full interest structure [P2]

Replace "naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles)" with "interest structure (names, perspectives, and prompts)." Interest names alone are insufficient for reliable type inference. The Perspective and Prompt fields contain the semantic content needed to assess whether interests align with the stated problem type.

### AR-4: Add interest-count cost note at interests confirmation [P3]

Add to the interests confirmation display (SKILL.md ~line 1008): "Note: Deliberation cost scales with interest count. {count} interests will require approximately {N^2 + N + 1} agent launches per round."

This gives users the information needed to make informed trade-offs about interest count before they commit. Distinct from C-6 (mode confirmation), which comes after interests are locked.

---

## Referenced Documentation

| Document | Lines | Relevance |
|----------|-------|-----------|
| `specs/008-interests-mode/spec.md` | 1-106 | Full spec under review |
| `conversus/SKILL.md` | 926-1296 | Interests and Mode handler implementations |
| `conversus/SKILL.md` | 57-60 | Schema Completeness via Defaults (arbiter opinion grounding) |
| `conversus/SKILL.md` | 889 | Define handler deferred resolution design |
| `conversus/SKILL.md` | 1304-1318 | Agent launch cost formulas (MO-1 reference) |
| `round-1/summary/final.md` | Full | Round 1 synthesis -- convergence points, disputes, concessions |
| `round-1/arbitration/resolution.md` | Full | Arbiter advisory opinions on three remaining disputes |
| `round-1/summary/final.md` | C-6 (lines 153-159) | Cost estimate convergence point (challenged in MO-1) |
| `round-1/summary/final.md` | C-7 (lines 161-167) | Cross-validation convergence point (challenged in OBA-2) |
| `round-1/summary/final.md` | K-2 (lines 307-313) | CLARIFY-tag fix text (gap identified in AR-1) |
| `round-1/arbitration/resolution.md` | Dispute 1 (lines 47-68) | Arbiter opinion on CLARIFY-tag handling |
| `round-1/arbitration/resolution.md` | General observation 7 (line 142) | "All disputes are about language" claim (challenged in OBA-1) |
