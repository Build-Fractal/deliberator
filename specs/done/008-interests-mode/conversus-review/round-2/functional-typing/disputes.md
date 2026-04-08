# Functional-Typing Disputes — Round 2 (Final)

**Reviewer**: functional-typing
**Phase**: Cooperative Disputes (Phase 4, Round 2 of 2)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: K-2 third exit state — double-declination stop vs. user-confirmed degraded mode

**With**: devils-advocate (revision NR-1), integration-architect (implicit via their acceptance of synthesis K-2 without addressing the third exit state)
**Regarding**: SKILL.md ~line 955, interests handler behavior when the user declines both choosing a calibration style and running `/conversus define`

**What is agreed by all three reviewers**: K-2's synthesized text does not specify what happens after the user declines the recommendation to run `/conversus define`. All three of us identified this gap independently. All agree it must be closed. All agree the interests handler cannot generate calibrated prompts without a type. All agree the define handler's deferred-resolution design (SKILL.md line 889) should be respected to the extent possible.

**Where we diverge**:

My revision (NR-1, revised K-2) prescribes a two-attempt flow: the first declination produces a recommendation to run `/conversus define`; a second declination produces a hard stop. This narrows the deferred-resolution window to one attempt but does not eliminate it entirely. The user gets two clear decision points before the handler stops.

Devils-advocate's revision (NR-1) prescribes a user-confirmed degraded mode: if the user declines both choosing a calibration style and returning to `/conversus define`, the handler explains that prompts will use "generic calibration rather than type-specific calibration," asks the user to confirm, and if confirmed, generates interests with generic prompts.

**Why I dispute devils-advocate's approach**: The concept of "generic calibration" is not defined anywhere in the spec or SKILL.md. The Interest Generation table (SKILL.md lines 957-962) has exactly four rows, each corresponding to a problem type. There is no fifth row for "generic." Devils-advocate's proposal requires either: (a) inventing a fifth calibration style that does not exist in the current schema, which is a design change that has not been deliberated, or (b) silently choosing one of the four existing styles as the "generic" stand-in, which is exactly the silent default that the arbiter's Domain Agnosticism reasoning eliminates (resolution.md lines 56-58). Either path introduces new complexity that the proposal does not specify.

My approach is more constrained but architecturally honest: the interests handler cannot generate calibrated prompts without knowing the type, so after two opportunities for the user to provide one, it stops. This is a hard boundary that follows from the Interest Generation table's structure, not an arbitrary restriction. The table has four rows; the handler needs one of them; the user must provide the selection.

I acknowledge that this makes CLARIFY-tag resolution effectively mandatory for the interests handler after two attempts, which narrows the define handler's deferred-resolution contract. I accepted this trade-off explicitly in my revision (lines 56-58) because the interests handler's calibration table structurally requires a type -- there is no uncalibrated path through the table.

**Devils-advocate's approach would be preferable IF** the spec and SKILL.md defined what "generic calibration" means in concrete prompt-generation terms. Without that definition, the proposal is an unspecified design extension presented as a resolution to a control-flow gap.

**Status**: Genuine dispute. Both approaches close the gap. The disagreement is whether the interests handler should support a degraded mode that does not currently exist in its schema, or enforce the schema's structural requirement that a type be selected.

---

### Dispute 2: K-5 cost estimate — priority of computed count refinement

**With**: devils-advocate (revision AR-2, priority downgraded to P3)
**Regarding**: SKILL.md ~line 1203, mode confirmation cost display

**What is agreed**: All three reviewers now agree the mode confirmation should display a computed agent launch count rather than the raw formula `N^2 + N + 1`. The mode handler knows N at confirmation time and can compute the exact number. The formula remains valuable in the Important Notes section as implementer documentation.

**Where we diverge**: I classified this as P2 in my revision (K-5 revised). Devils-advocate downgraded to P3 in their revision (AR-2), arguing it is a "presentation refinement" because "the user has already expressed intent to proceed." Integration-architect consolidated this as NR-1 at P2.

**My position**: P2 is correct because the cost estimate's purpose is to inform a go/no-go decision, and the spec's No Game Theory Knowledge constraint (spec.md line 103) applies. Displaying `N^2 + N + 1` requires the user to perform mental arithmetic with a polynomial -- this is not "game theory knowledge" per se, but it violates the spirit of the constraint, which is to insulate users from the system's internal abstractions. A user with 4 interests must compute `16 + 4 + 1 = 21` to understand the cost. A user with 6 interests must compute `36 + 6 + 1 = 43`. The formula is not difficult for the system to evaluate; requiring the user to evaluate it is an unnecessary cognitive transfer. P3 treats this as polish; P2 treats it as a usability gap in a cost-awareness mechanism. The mechanism exists to inform user decisions; if the mechanism requires mental arithmetic to parse, it is not fully serving its purpose.

This is a minor disagreement. I will not block on priority classification. But the 2-to-1 alignment (my P2, integration-architect's P2, devils-advocate's P3) supports P2.

---

## Convergence

The following items have reached full convergence across all three reviewers in Round 2. These are settled and require no further deliberation.

### All Round 1 convergence points (C-1 through C-10) remain stable

No reviewer proposed reopening any of the eight convergence items or the three dispute resolutions from Round 1. All prior concessions stand across all three reviewers. The converged recommendation set from Round 1 is the foundation on which Round 2 refinements build.

### S-1 through S-4 and K-1, K-3, K-4, K-7, K-8: Confirmed without modification

All three Round 2 revisions confirm these items exactly as specified in the synthesis. No reviewer proposed changes to the spec updates (ambiguous row replacement, Preset field addition, workspace-override documentation, Confidence column footnote) or to the uncontested SKILL.md changes (preset validation, draft status behavior, heuristic-is-advisory sentence, zero-signal handling, extension-points note).

### K-6: Interest-vs-type cross-validation — "interest structure (names, perspectives, and prompts)"

All three reviewers converge on replacing "naming pattern" with "interest structure (names, perspectives, and prompts)" in the K-6 cross-validation description. Integration-architect withdrew the standalone four-row mapping table (AR-1 revised). Devils-advocate maintained AR-3 with this wording. My revision adopted the same language. The cross-validation should examine the full interest structure -- names, Perspective sentences, and Prompt content -- not names alone. If interest names are semantically opaque, perspective and prompt content provide the signals. The parenthetical example categories (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles) remain as illustrative guidance, not as the sole input.

**Traced agreement**: functional-typing revision K-6; integration-architect revision NR-2; devils-advocate revision AR-3.

### NR-2 / AR-2 / D-1: `(none)` sentinel standardization — standardize to `(none)` in the define handler

All three reviewers agree the sentinel text mismatch between the define handler's `(none -- no context documents provided)` (SKILL.md line 891) and the mode handler's `(none)` check (SKILL.md line 1254) is a real gap that should be fixed in spec 008's scope rather than fully deferred to D-1. Integration-architect changed from option (a) prefix matching to option (b) canonical form standardization. My revision specified the same resolution. Devils-advocate did not contest this in their Round 2 revision.

The resolution: change the define handler's sentinel output from `(none -- no context documents provided)` to `(none)`. The mode handler's check remains unchanged. The descriptive text adds no information the user does not already know. D-1 remains as a broader deferred item for sentinel conventions across future handlers.

**Traced agreement**: functional-typing revision NR-2; integration-architect revision AR-2 (direction changed to option b); devils-advocate Round 2 review (no contest).

### K-5 substance: Computed count with explicit assumptions

All three reviewers agree the K-5 mode confirmation display should show a computed agent launch count rather than the raw formula. All agree the parenthetical should make assumptions explicit. The converged display text:

> "This configuration will launch {computed_count} agents (all {count} agents cross-review all others, single iteration)."

Where `computed_count` = N^2 + N + 1, computed by the handler. The formula is retained in the Important Notes section (SKILL.md lines 1304-1308) as implementer documentation with both qualifications: uniform cross-review and iterations=1.

Priority is disputed (P2 vs. P3; see Dispute 2 above), but the substance and display format are converged.

**Traced agreement**: functional-typing revision K-5; integration-architect revision NR-1; devils-advocate revision AR-2 (substance accepted, priority differs).

### NR-1 / S-5: Interest count upper-bound validation in SKILL.md

All three reviewers now agree that the SKILL.md post-write validation should enforce the spec's "2-5" upper bound. Integration-architect's DC-1 and devils-advocate's DC-1 both identified that relaxing to "2 or more" creates an unacknowledged dependency on the cost estimate as a throttle -- a role C-6 did not converge it to play. I reversed my preference in my revision. The resolution: add a warning gate at 5 interests with user confirmation override. This reconciles the spec's stated range with the SKILL.md's current "2+" validation without promoting the cost estimate from informational display to enforcement mechanism.

If 5 is later found too restrictive, the threshold can be raised in both documents together. The principle -- that a hard ceiling must exist somewhere -- is settled.

**Traced agreement**: functional-typing revision NR-1 (reversed from "relax" to "enforce"); integration-architect revision DC-1 reasoning; devils-advocate revision DC-1 reasoning.

### K-2 substance (excluding third exit state): Inline user choice with four calibration styles

All three reviewers agree on the core K-2 mechanism: when the interests handler encounters a CLARIFY-tagged Type field, present the four calibration styles as explicit choices to the user. If the user chooses one, proceed. If the user declines, recommend `/conversus define`. No silent extraction of the best-guess type. No silent default. The disagreement is solely on the third exit state (what happens after the user declines both choosing and running define), which is Dispute 1 above.

### AR-4 calibration style descriptions: No parenthetical type labels

Integration-architect revised AR-4 to remove parenthetical type names from the calibration style prompt (revision AR-4 revised). Both my cross-review DC-2 and devils-advocate's DC-1 of integration-architect independently identified the contradiction with the No Game Theory Knowledge constraint. Integration-architect conceded. The four calibration style descriptions should be presented as plain-language behavioral choices without internal taxonomy labels.

**Traced agreement**: integration-architect revision AR-4 (revised, labels removed); functional-typing cross-review DC-2; devils-advocate cross-review DC-1 of integration-architect.

### OBA-1 correction: Equal-probability assumption is consequential, not inconsequential

Integration-architect's DC-2 of my cross-review correctly demonstrated that the unequal prior probability of modes under heuristic detection is the architectural justification for K-6 (cross-validation warning) and K-7 (zero-signal presentation). I withdrew "inconsequential" in my revision (OBA-1 revised). The corrected characterization: "Off-base and consequential for the design rationale of K-6 and K-7, but not requiring a new recommendation because K-6 and K-7 already handle the consequences correctly."

### D-3 withdrawn: `--output` flag rename is not a formal deferred item

I withdrew D-3 as a formal deferred item in my revision. The P3 naming observation stands as an editorial note. Integration-architect's T-4 and devils-advocate's T-4 both correctly noted that a formal deferred item for a flag rename in a pre-shipped system is overengineered.

### Devils-advocate concessions: AR-1 hard stop, AR-4, OBA-1

Devils-advocate conceded three positions in their revision: the AR-1 hard stop for the CLARIFY-tag third exit state (replaced with user-confirmed degraded mode), AR-4 and MO-2 withdrawal (internal inconsistency with AR-2 and relitigation of Round 1 cost-placement concession), and OBA-1 (arbiter engaged with architecture in full, critique was misplaced). These concessions narrow the remaining dispute surface and are well-reasoned.

### Integration-architect concessions: AR-1, AR-2, AR-3, AR-4, AR-5

Integration-architect revised all five of their Round 2 recommendations in response to cross-review feedback. AR-1 withdrew the standalone mapping table, AR-2 changed sentinel resolution direction from prefix matching to canonical form, AR-3 was superseded by the computed count, AR-4 removed parenthetical type labels, and AR-5 separated the timestamp concern from the state-model advisory. All five revisions are well-reasoned and strengthen the converged position.

---

## Final Position Statement

### Assessment of the deliberation

This deliberation achieved strong closure. Two rounds of review, cross-review, revision, and dispute resolution across three reviewers produced a converged recommendation set of 4 spec changes, 10 SKILL.md changes, and 2 deferred items. Eight convergence points from Round 1 survived Round 2 without challenge. Three disputes from Round 1 were resolved. Two new recommendations emerged from Round 2 (interest count upper-bound validation and sentinel standardization) with unanimous support. The cross-review mechanism worked as designed: it surfaced genuine errors in each reviewer's reasoning (my MO-1 resolution direction, my OBA-1 "inconsequential" dismissal, my D-1 priority classification, integration-architect's mapping table, integration-architect's prefix matching, devils-advocate's hard stop, devils-advocate's arbiter critique) and produced corrections that all reviewers accepted.

### What I defend

1. **The double-declination stop is architecturally honest.** The interests handler's calibration table has four rows. It needs one of them. "Generic calibration" is not a defined concept in the system, and introducing it as a resolution to a control-flow gap creates more specification surface than it closes. My revised K-2 (two-attempt flow, stop after second declination) respects the table's structure while giving the user two clear opportunities to choose. If a future spec defines an uncalibrated prompt generation path, the double-declination stop can be relaxed to a degraded-mode option at that time.

2. **K-5 computed count is P2, not P3.** The cost estimate exists to inform decisions. A mechanism that requires mental polynomial evaluation to parse is not fully serving its informational purpose. The 2-to-1 alignment supports P2.

3. **All prior positions are stable.** I have not reversed any concession from Round 1 or Round 2. Every correction I accepted was warranted and I do not seek to relitigate any of them.

### What I concede

1. **Devils-advocate's identification of the third exit state is correct.** K-2 as synthesized does not specify this case. The gap must be closed regardless of which resolution is adopted. I acknowledged this in my revision and proposed the double-declination stop as the resolution.

2. **My original MO-1 resolution preference (relax to "2 or more") was wrong.** Both cross-reviewers demonstrated the dependency on the cost estimate as a throttle. I reversed the preference in my revision without reservation.

3. **My D-1 P3 classification was internally inconsistent.** Claiming the SKILL.md "handles this correctly" while noting a text mismatch is contradictory. The sentinel mismatch is P2 and should be fixed in spec 008's scope. I accepted this correction fully in my revision.

4. **My OBA-1 "inconsequential" dismissal was wrong.** The unequal prior probability of modes is consequential for K-6 and K-7's design rationale. I corrected this in my revision.

### Non-negotiables

1. **The spec's `ambiguous` row must be replaced.** (C-1, S-1, P1.) Unchanged from Round 1.

2. **The `Preset` field must be added to the spec schema.** (C-2, S-2, P1.) Unchanged from Round 1.

3. **Preset existence validation must be added to post-write checks.** (C-3, K-1, P1.) Unchanged from Round 1.

4. **The CLARIFY-tag gap must be closed with an explicit control flow.** (K-2, P1.) The specific third-exit-state resolution is disputed, but leaving the gap open is not acceptable.

5. **The `--output` workspace-override behavior must be documented.** (S-3, P1.) Unchanged from Round 1.

6. **The `(none)` sentinel must be standardized.** (NR-2, P2.) Elevated from D-1 deferred based on Round 2 cross-review corrections.

7. **The interest count upper bound must be enforced in SKILL.md.** (NR-1, P2.) Added in Round 2 based on cross-review corrections to my original resolution preference.

### Final recommendation table

#### Spec changes

| ID | Item | Priority | Action | Status |
|---|---|---|---|---|
| S-1 | Replace `ambiguous` row | P1 | As synthesis C-1 | Converged |
| S-2 | Add `Preset` field to interests.md schema | P1 | As synthesis C-2 | Converged |
| S-3 | Document `--output` as workspace override | P1 | As synthesis, integration-architect framing | Converged |
| S-4 | Rename or footnote Confidence column | P2 | As synthesis C-11 | Converged |

#### SKILL.md changes

| ID | Item | Priority | Action | Status |
|---|---|---|---|---|
| K-1 | Preset existence validation | P1 | As synthesis C-3 | Converged |
| K-2 | CLARIFY-tag handling with two-attempt flow | P1 | Present four calibration styles, recommend define on first decline, stop on second decline | Disputed (third exit state only) |
| K-3 | Draft status behavior | P1 | As synthesis C-5 | Converged |
| K-4 | Heuristic-is-advisory sentence | P2 | As synthesis C-4 | Converged |
| K-5 | Cost estimate: computed count with assumptions | P2 | Display computed number, not formula; note cross-review and iteration assumptions | Converged on substance; priority disputed (P2 vs. P3) |
| K-6 | Cross-validation on interest structure | P2 | "Interest structure (names, perspectives, and prompts)" replaces "naming pattern" | Converged |
| K-7 | Zero-signal: present all four modes | P2 | As synthesis C-8 | Converged |
| K-8 | Extension-points note | P2 | Use "extend"/"add" language, not "complete"/"fill in" | Converged |
| NR-1 | Interest count upper-bound validation | P2 | Warning gate at 5 with user confirmation override | Converged |
| NR-2 | Standardize `(none)` sentinel | P2 | Change define handler sentinel to `(none)` | Converged |

#### Deferred items

| ID | Item | Priority | Status |
|---|---|---|---|
| D-1 | Sentinel formalization (broader, future handlers) | P2 | Confirmed |
| D-2 | Interest deduplication/overlap detection | P3 | Confirmed |

### Closing note

One genuine dispute remains: the third exit state for K-2's CLARIFY-tag handling. The disagreement is narrow and well-defined -- whether the interests handler should stop after two declinations (my position) or offer a "generic calibration" degraded mode that does not currently exist in the schema (devils-advocate's position). Both approaches close the gap. The choice depends on whether the system should introduce a new concept ("generic calibration") to avoid a hard stop, or enforce the existing schema's structural requirement that a type be selected. I advocate for the latter because it is faithful to the current specification without introducing undeliberated design surface.

All other items are converged. The spec and SKILL.md are substantively sound and ready for implementation with the agreed changes.
