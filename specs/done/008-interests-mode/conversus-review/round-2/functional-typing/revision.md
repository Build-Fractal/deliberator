# Round 2 Revision — functional-typing

**Reviewer**: functional-typing
**Round**: 2 of 2 (Phase 3 — Cooperative Revision)
**Date**: 2026-03-22

---

## Recommendation Dispositions

### S-1: Replace `ambiguous` row with heuristic detection reference — CONFIRMED
Priority: P1. No changes. All three reviewers and both cross-reviews affirm this. Ready for implementation as specified in synthesis C-1.

### S-2: Add `Preset` field to interests.md schema — CONFIRMED
Priority: P1. No changes. Unanimously settled.

### S-3: Document `--output` as workspace override — CONFIRMED
Priority: P1. No changes. Workspace-override framing adopted per synthesis and arbiter. No cross-review challenged this.

### S-4: Rename or footnote Confidence column — CONFIRMED
Priority: P2. No changes. Editorial choice on label; substance settled.

### S-5: Reconcile interest count range — MODIFIED

**Original position**: Either add upper bound to SKILL.md or relax spec to "2 or more," with a stated preference for resolution 2 (relax). Both cross-reviewers identified dangerous contradictions in the relaxation path.

**Integration-architect DC-1**: Correctly identifies that relaxing the upper bound to "2 or more" while relying on the cost estimate as a throttle has no enforcement mechanism. The cost estimate was converged as an informational display (C-6, K-5), not as a validation gate. Promoting it to a gate reopens a settled convergence item. This is a real dependency I failed to trace.

**Devils-advocate DC-1**: Independently arrives at the same conclusion via a different path -- the cost formula as currently specified displays `N^2 + N + 1` as a formula, not a computed count. A user adding 8 interests would need to mentally compute 73. The throttle is not legible enough to serve as the primary enforcement mechanism.

**Revised position**: I withdraw the preference for resolution 2. Both cross-reviewers' reasoning is sound. The correct resolution is resolution 1: add the upper-bound validation to SKILL.md (line 1059) to match the spec's "2-5" range. If 5 is too restrictive, the threshold can be raised (to 7 or 8) as integration-architect suggests, but a hard ceiling must exist to prevent runaway agent costs without requiring the cost estimate to become a validation gate. The gap between spec and SKILL.md remains a genuine P2 finding; only the resolution direction changes.

**Reclassified**: S-5 becomes a reconciliation action on both documents. If the upper bound is retained at 5, the SKILL.md needs the validation change. If the upper bound is raised, both the spec and SKILL.md need updating. In either case, the SKILL.md post-write validation (line 1059) must enforce whatever ceiling is chosen. I list it as a SKILL.md change (K-9 below) with a corresponding spec confirmation.

### K-1: Preset existence validation in post-write check — CONFIRMED
Priority: P1. No changes.

### K-2: CLARIFY-tag handling: inline user choice, recommend define, no default — MODIFIED

**Original position**: Present four calibration styles, let user choose, recommend `/conversus define` if user declines, do not default, do not block.

**Devils-advocate T-1 (via cross-review)**: Correctly identifies that my position leaves the third exit state underspecified -- what happens when the user declines both choosing a calibration style AND running `/conversus define`? My "do not block" instruction is ambiguous: it could mean the handler proceeds without calibration (contradicting "do not default") or that it does not force the user to run define (leaving the exit state unresolved).

**Devils-advocate AR-1 (via their review)**: Proposes a hard stop for the double-decline case. However, as I identified in my cross-review of devils-advocate (DC-1), a hard stop functionally converts K-2 from "recommend" to "require," which contradicts the arbiter's reasoning about preserving the define handler's deferred-resolution design (SKILL.md line 889, resolution.md lines 60-62).

**Integration-architect T-2 (via cross-review)**: Notes that my position uses "recommend" without specifying the form of the recommendation. This is a valid implementation-level gap.

**Revised position**: The third exit state must be specified, but the resolution must be consistent with the deferred-resolution design. Revised K-2 control flow:

1. Present the CLARIFY tag's context and the four calibration styles as explicit choices.
2. If the user chooses a calibration style, proceed with it.
3. If the user declines to choose, display: "We recommend running `/conversus define` to resolve the type before generating interests. Would you like to: (a) choose a calibration style from the list above, (b) stop and run `/conversus define` first?"
4. If the user chooses (a), return to step 1. If the user chooses (b), stop processing with a clear message: "Run `/conversus define` to resolve the problem type, then re-run `/conversus interests`."
5. If the user declines both options a second time, stop processing: "Cannot proceed without a calibration style. Run `/conversus define` to resolve the problem type."

This is functionally a hard stop after two declinations, which narrows the deferred-resolution window but does not eliminate it. The user gets two clear opportunities to choose before the handler stops. This is more constrained than my original "do not block" position but less rigid than devils-advocate's immediate hard stop. The key distinction: the first declination results in a recommendation (preserving deferred resolution); only a second declination results in a stop (acknowledging that the handler genuinely cannot generate calibrated prompts without a type).

I accept that this makes CLARIFY-tag resolution effectively mandatory for the interests handler after two attempts, which narrows the define handler's deferred-resolution contract for this specific downstream consumer. This is an acceptable narrowing because the interests handler's calibration table (SKILL.md lines 957-962) has no "uncalibrated" row -- it structurally requires a type.

**Integration-architect T-2 on "recommend" form**: The revised control flow above specifies the UX: a binary choice prompt (a/b), not a free-text suggestion. This closes the implementation gap.

### K-3: Draft status behavior: warn and proceed — CONFIRMED
Priority: P1. No changes.

### K-4: Heuristic-is-advisory sentence — CONFIRMED
Priority: P2. No changes.

### K-5: Agent-launch cost estimate at mode confirmation — MODIFIED

**Original position**: Confirmed as specified in synthesis C-6 without modification.

**Devils-advocate MO-1 and AR-2 (via their review)**: Correctly distinguishes implementer-facing information (the formula `N^2 + N + 1`) from user-facing information (a computed count like "13 agent launches"). The mode handler knows N at confirmation time and can compute the exact number.

**Integration-architect OBA-1 (via their review)**: Proposes qualifying the parenthetical from "(based on {count} agents in {mode} mode)" to "(all {count} agents cross-review all others)." This makes the cost estimate's assumptions explicit.

**My cross-review of integration-architect (T-3)**: I noted that the formula also assumes `iterations: 1`, which is the default for generated configs. The qualification should note this assumption too if we are making assumptions explicit.

**Devils-advocate T-3 (via cross-review of me)**: Argues this is a refinement to the implementation language of a converged item, not a reopening. I agree -- the convergence is on the substance (display a cost estimate at mode confirmation), not on the specific display format.

**Revised position**: K-5 should display a computed count, not a raw formula. Change the synthesis text from:

> "Estimated agent launches per round: {N^2 + N + 1} (based on {count} agents in {mode} mode)."

To:

> "Estimated agent launches per round: {computed_count} (all {count} agents cross-review all others, single iteration)."

Where `computed_count` = N^2 + N + 1, computed by the handler. This is a P2 refinement to the implementation language that does not reopen the C-6 convergence on substance or placement. Priority remains P2. I accept devils-advocate's substance on the computed count and integration-architect's substance on the parenthetical, and I add the iteration assumption for consistency with my own T-3 observation.

### K-6: Interest-vs-type cross-validation warning — MODIFIED

**Original position**: Confirmed as specified in synthesis C-7.

**Integration-architect DC-1 (via their review) and DC-1 of my cross-review of integration-architect**: I identified that integration-architect's proposed naming-pattern-to-type mapping table would collapse multi-signal heuristic inference into a single-dimension lookup, producing false positives. I stand by that analysis.

**Devils-advocate OBA-2 and AR-3 (via their review)**: Proposes replacing "naming pattern" with "interest structure (names, perspectives, and prompts)" in C-7. This is the correct refinement. Interest names alone are insufficient for reliable type inference; the Perspective and Prompt fields contain the semantic content needed for meaningful cross-validation.

**My cross-review of devils-advocate (T-3, SA-3)**: I accepted AR-3's substance and noted the synthesis text is imprecise but not misleading.

**Revised position**: K-6 wording should be tightened. Replace "interest structure's naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles)" with "interest structure (names, perspectives, and prompts)." The parenthetical example categories can remain as illustrative guidance but should not be presented as the sole input to the cross-validation. Priority remains P2.

### K-7: Zero-signal edge case: present all four modes — CONFIRMED
Priority: P2. No changes.

### K-8: Advanced fields extension-points note — CONFIRMED
Priority: P2. No changes. "Extend"/"add" language, not "complete"/"fill in."

### OBA-1: Equal-probability assumption for heuristic detection — MODIFIED

**Original position**: Identified the assumption as "off-base but inconsequential."

**Integration-architect DC-2 (via cross-review of me)**: Argues that dismissing the equal-probability assumption as inconsequential contradicts the rationale for K-6 (cross-validation warning). K-6 exists precisely because the mode recommendation is not equally valid for all type/interest combinations. If all four modes were equally valid starting positions regardless of signals, K-6 would be unnecessary. The unequal prior probability of modes under heuristic detection is why K-6 and K-7 exist as separate mechanisms.

**Devils-advocate T-2 (via cross-review of me)**: Argues the "inconsequential" dismissal is premature because it is bounded to the current interactive workflow and does not account for future non-interactive workflows.

**Revised position**: Integration-architect's reasoning is correct. I withdraw "inconsequential." The unequal prior probability of modes under heuristic detection is consequential -- it is the architectural justification for K-6 (cross-validation when signals exist but conflict with stated type) and K-7 (zero-signal presentation when no signals exist). These are distinct mechanisms because the modes are not equally likely, and both mechanisms depend on this being the case. My original observation was correct in identifying the off-base assumption; my dismissal of its consequences was wrong because I failed to trace the dependency to K-6 and K-7.

I soften the characterization to: "Off-base and consequential for the design of K-6 and K-7, but not requiring a new recommendation because K-6 and K-7 already handle the consequences correctly." The observation informs the rationale for existing recommendations rather than generating a new one.

Devils-advocate's point about future non-interactive workflows is valid as a forward-looking note but does not change any spec 008 recommendation.

### D-1: `(none)` sentinel formalization — MODIFIED, PRIORITY ELEVATED

**Original position**: P3, deferred to D-1. Stated "the SKILL.md handles this correctly."

**Integration-architect T-1 (via cross-review of me)**: Correctly challenges my claim that the SKILL.md handles the sentinel correctly. The define handler writes `(none -- no context documents provided)` (SKILL.md line 891); the mode handler checks for `(none)` (SKILL.md line 1254). Whether these match depends on substring vs. exact matching, which the SKILL.md does not specify. My statement "likely handled by substring matching in practice" assumes implementation behavior in a system that has no code -- the SKILL.md is the implementation specification.

**Devils-advocate DC-2 (via cross-review of me)**: Makes the same point more sharply: classifying as P3 while saying "handles this correctly" is internally inconsistent. Either the SKILL.md handles it correctly (no finding) or the sentinel text diverges (P2 finding). Both cannot be true.

**Revised position**: I withdraw the claim that the SKILL.md handles this correctly. Integration-architect and devils-advocate are both right: unspecified-but-probably-fine is not the same as correctly specified. The sentinel mismatch is a P2 finding.

On the resolution approach, I maintain my cross-review position from T-2 of integration-architect's review: standardize to `- (none)` in the define handler's output (integration-architect's option b). This eliminates the matching problem entirely rather than introducing a prefix-matching rule (`(none`...) that creates its own fragility. Changing one line of sentinel text in the define handler is lower risk than codifying an ambiguous matching strategy.

This should be resolved within spec 008 rather than deferred to D-1. D-1 can still address the broader sentinel formalization question for future handlers, but the specific mismatch between the define handler's output and the mode handler's check is a current code path that should be fixed now.

### D-2: Interest deduplication/overlap detection — CONFIRMED
Priority: P3. Deferred. No changes.

### D-3: `--output` flag rename — MODIFIED

**Original position**: P3, deferred item for future spec.

**Integration-architect T-4 (via cross-review of me)**: Notes that creating a deferred item for a flag rename in a system with no shipped CLI and no backward-compatibility constraints may be overengineering the deferral process. If the flag should be renamed, it can be renamed directly as a P3 editorial change.

**Devils-advocate T-4 (via cross-review of me)**: Notes that D-3 has support from one reviewer and an advisory arbiter note, unlike D-1 and D-2 which had convergence support from multiple reviewers.

**Revised position**: Both points are fair. I withdraw D-3 as a formal deferred item. The observation about the naming mismatch (`--output` behaving as `--workspace`) stands as a P3 editorial note. If a future spec touches the flag's interface, the rename can be considered at that time without needing a standing deferred item. This simplifies the deferred items list to D-1 and D-2, both of which have multi-reviewer convergence support.

---

## New Recommendations

### NR-1: Add upper-bound validation to SKILL.md post-write check for interest count

**Priority**: P2
**Target**: SKILL.md, post-write validation (~line 1059)
**Action**: Change "At least 2 interests are defined" to "At least 2 and at most 5 interests are defined. If more than 5 are present, warn: 'You have {count} interests. The agent-launch cost scales quadratically (estimated {count^2 + count + 1} launches per round). Reduce to 5 or fewer, or confirm to proceed.' If the user confirms, proceed."

This resolves the spec/SKILL.md divergence identified in MO-1 by enforcing the spec's upper bound in the SKILL.md while preserving user agency through a confirmation gate. The ceiling is a warning gate, not a hard block -- users can override with explicit confirmation. This avoids promoting the C-6 cost estimate from display to validation gate (which would reopen a settled convergence item) while still providing an enforcement mechanism above the threshold.

**Source**: MO-1 revised per integration-architect DC-1 and devils-advocate DC-1.

### NR-2: Standardize `(none)` sentinel in define handler output

**Priority**: P2
**Target**: SKILL.md, define handler Source Documents sentinel (~line 891)
**Action**: Change the define handler's sentinel from `(none -- no context documents provided)` to `(none)`. This makes the define handler's output match the mode handler's check (SKILL.md line 1254) exactly, eliminating the substring-vs-exact-matching ambiguity.

The mode handler's check for `(none)` remains unchanged. The define handler's longer form `(none -- no context documents provided)` is the source of the mismatch and should be shortened. The explanatory text ("no context documents provided") adds no information that the user does not already know -- they explicitly declined to provide documents.

This is a fix within spec 008's scope because both the define handler's output and the mode handler's consumption are current code paths in the SKILL.md. D-1 remains as a broader deferred item for sentinel formalization across future handlers.

**Source**: MO-2 revised per integration-architect T-1, devils-advocate DC-2, and my cross-review of integration-architect T-2.

---

## Position Summary

Round 2 produced genuine improvements to my positions. The two most significant corrections came from the cross-reviews:

1. **MO-1 resolution direction reversed**. Both cross-reviewers independently identified that my preferred resolution (relax the spec to "2 or more") created an unacknowledged dependency on the cost estimate serving as a throttle -- a role it was not converged to play. The correct resolution is to enforce the upper bound in the SKILL.md, preserving C-6 as an informational display.

2. **D-1 sentinel mismatch elevated from P3 to P2**. Both cross-reviewers correctly challenged my internal inconsistency: claiming the SKILL.md "handles this correctly" while simultaneously noting a text mismatch is contradictory. The SKILL.md does not handle it correctly in a strict reading. The fix is to standardize the sentinel text now rather than defer it.

Three smaller adjustments: K-2 now specifies the third exit state (double-declination results in a stop after two opportunities to choose, preserving one round of deferred resolution); K-5 now specifies a computed count with explicit assumptions rather than a raw formula; K-6 now references "interest structure (names, perspectives, and prompts)" rather than "naming pattern" alone.

OBA-1 is corrected from "inconsequential" to "consequential for K-6 and K-7 design rationale but not requiring a new recommendation." D-3 is withdrawn as a formal deferred item.

All prior concessions from Round 1 stand without reversal. All eight convergence points (C-1 through C-10) remain confirmed. All three dispute resolutions from Round 1 remain adopted. The spec and SKILL.md are substantively sound with no blocking defects. The remaining work is implementation-level precision within the agreed framework.

### Final Recommendation Table

#### Spec changes

| ID | Item | Priority | Action |
|---|---|---|---|
| S-1 | Replace `ambiguous` row | P1 | As synthesis C-1 |
| S-2 | Add `Preset` field to interests.md schema | P1 | As synthesis C-2 |
| S-3 | Document `--output` as workspace override | P1 | As synthesis, integration-architect framing |
| S-4 | Rename or footnote Confidence column | P2 | As synthesis C-11 |

#### SKILL.md changes

| ID | Item | Priority | Action |
|---|---|---|---|
| K-1 | Preset existence validation | P1 | As synthesis C-3 |
| K-2 | CLARIFY-tag handling with double-declination stop | P1 | Revised: two-attempt flow, stop after second declination |
| K-3 | Draft status behavior | P1 | As synthesis C-5 |
| K-4 | Heuristic-is-advisory sentence | P2 | As synthesis C-4 |
| K-5 | Cost estimate: computed count with assumptions | P2 | Revised: display computed number, not formula; note cross-review and iteration assumptions |
| K-6 | Cross-validation on interest structure | P2 | Revised: "interest structure (names, perspectives, and prompts)" replaces "naming pattern" |
| K-7 | Zero-signal: present all four modes | P2 | As synthesis C-8 |
| K-8 | Extension-points note | P2 | As synthesis Dispute 3 resolution |
| NR-1 | Interest count upper-bound validation | P2 | Warning gate at 5 with user override; reconciles spec "2-5" with SKILL.md "2+" |
| NR-2 | Standardize `(none)` sentinel | P2 | Change define handler sentinel to `(none)` to match mode handler check |

#### Deferred items

| ID | Item | Priority |
|---|---|---|
| D-1 | Sentinel formalization (broader, future handlers) | P2 |
| D-2 | Interest deduplication/overlap detection | P3 |
