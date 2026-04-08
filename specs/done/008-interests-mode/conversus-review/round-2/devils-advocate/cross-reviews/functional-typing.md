# Cross-Review of functional-typing — Round 2

**Reviewer**: devils-advocate
**Reviewing**: functional-typing's Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: MO-1 (interest count upper bound) contradicts the stated preference for relaxing it

Functional-typing identifies a real gap: the spec says "2-5 competing interests" (FR-001, spec.md line 31) but the SKILL.md post-write validation (line 1059) only enforces "at least 2." This is a genuine spec/SKILL.md divergence that all three reviewers missed in Round 1. Good catch.

But functional-typing's proposed resolution 2 -- relax the spec to "2 or more" and let the cost estimate serve as the user's throttle -- contradicts the converged position on C-6 (agent-launch cost estimate). My own Round 2 review (MO-1) identifies that the C-6 cost estimate as currently specified displays a formula (`N^2 + N + 1`) rather than a computed count, and that this formula covers only the single-round no-arbiter case. If the cost estimate is the user's primary throttle against unbounded interest counts, that throttle must be accurate and legible. Under functional-typing's resolution 2, a user could add 8 interests and see "Estimated agent launches per round: N^2 + N + 1" without understanding that this means 73 agent launches. The cost estimate is not yet in a state to serve as a reliable throttle for interest count.

The contradiction: functional-typing delegates the upper-bound enforcement to a mechanism (the cost estimate) that functional-typing's own review does not examine for adequacy as a throttle. Functional-typing does not reference the cost formula's limitations that my review surfaces (MO-1, AR-2). If resolution 2 is adopted, the cost estimate must first be upgraded from a formula display to a computed count with explicit qualification -- otherwise the "throttle" is a formula that users must mentally evaluate under quadratic scaling they may not anticipate.

Functional-typing's resolution 1 (add the upper bound to SKILL.md validation) is the safer path precisely because it does not depend on a downstream mechanism being fit for purpose. But if the deliberation prefers resolution 2, it must pair that relaxation with AR-2 from my review.

### DC-2: MO-2 (sentinel text mismatch) is noted as P3 but contradicts the claim that "the SKILL.md handles this correctly"

Functional-typing observes that the define handler writes `(none -- no context documents provided)` (SKILL.md line 891) while the mode handler checks for `(none)` (SKILL.md line 1254). Functional-typing then says "This is likely handled by substring matching in practice" and classifies it as P3.

The phrase "likely handled by substring matching" is an assumption about implementation behavior in a system that has no code -- it is a SKILL.md, not a codebase. The SKILL.md is the implementation specification. The mode handler says to check for `(none)`, not "check whether the sentinel contains the substring `(none)`." In a strict reading, the mode handler would fail to match the define handler's sentinel because `(none -- no context documents provided)` is not `(none)`.

Functional-typing correctly connects this to D-1 (sentinel formalization) from the Round 1 synthesis. But classifying it as P3 while simultaneously saying "the SKILL.md handles this correctly" is internally inconsistent. Either the SKILL.md handles it correctly (in which case there is no finding) or the sentinel text divergence is a real gap (in which case it should be at least P2, consistent with D-1's priority). It cannot both "handle this correctly" and have a sentinel text mismatch that requires deferred formalization.

My position: this is a P2 finding that belongs under D-1, not a P3 afterthought. The SKILL.md does not handle this correctly in a strict reading -- it handles it correctly only under an assumption of substring matching that the SKILL.md text does not specify.

---

## Tensions

### T-1: Dispute 1 resolution accepts the synthesis fully but does not address the control flow gap I identify

Functional-typing's Dispute 1 resolution is thorough and well-grounded. The reasoning on why `integration` is wrong on two independent grounds (Domain Agnosticism violation and conflation of calibration style with mode selection) is structurally sound and adds precision beyond what the arbiter provided.

However, functional-typing's resolution says: "If they decline, recommend `/conversus define` to resolve the tag. Do not default. Do not block." My review (AR-1) identifies a specific gap in this formulation: what happens when the user declines to choose a calibration style AND declines to run `/conversus define`? The synthesis text says "recommend running `/conversus define` to resolve the CLARIFY tag before proceeding" but does not specify the control flow for the double-decline case.

Functional-typing does not address this third exit state at all. The "Do not block" instruction in functional-typing's position is ambiguous: does "do not block" mean the handler should proceed without calibration (which contradicts "do not default"), or does it mean the handler should not force the user to run `/conversus define` (which leaves the double-decline case unresolved)? My review resolves this by specifying an explicit hard stop: the handler explains that it cannot generate calibrated prompts without a type, offers the choices once more, and if the user still declines, stops processing with a clear message.

This is a tension, not a contradiction, because functional-typing's position is compatible with adding the control flow specification -- it just does not include it. The gap is real but closable.

### T-2: OBA-1 (equal probability assumption) is correctly identified but the "inconsequential" dismissal may be premature

Functional-typing identifies that the synthesis and convergence on C-1 assume all four modes are equally plausible candidates for heuristic detection, and correctly notes that this assumption is not grounded in actual usage patterns. The analysis of the two cases (skipped define, or define produced CLARIFY tag) is sound.

But the conclusion -- "off-base but inconsequential" -- depends on the assumption that presenting all four modes with plain-language descriptions is always the correct behavior. This is true for the current interactive workflow. It would not be true if a future spec introduces batch mode, CI integration, or non-interactive execution, where an unattended pipeline needs a reasonable default or must fail explicitly rather than presenting four choices to a non-existent user. My OBA-1 in my own review (the arbiter's "all disputes are about language" claim) makes a related point: the CLARIFY-tag handling dispute has architectural implications for non-interactive execution paths that the current interactive framing obscures.

The tension: functional-typing and I agree that the equal-probability assumption is off-base, but we differ on whether its consequences are bounded to the current interactive design or extend to future non-interactive designs. If the deliberation's output (the actionable changes) will constrain future specs, the "inconsequential" dismissal should be softened to "inconsequential for the current interactive workflow; future non-interactive workflows may need a different approach."

### T-3: Convergence confirmation is blanket rather than item-by-item

Functional-typing confirms all convergence items C-1 through C-10 with the statement: "All eight convergence points from Round 1 remain settled. I have no corrections, extensions, or reversals for any of them."

My review challenges two specific convergence items: C-6 (the cost estimate formula should be a computed count, not a raw formula) and C-7 (the cross-validation description references "naming patterns" but should reference the full interest structure). These are not reversals -- they are precision improvements to the implementation language of converged items. Functional-typing's blanket confirmation forecloses the possibility of refining converged items without reversing them.

The tension is methodological: can Round 2 tighten the implementation language of a converged item without "reopening" it? I believe yes -- the convergence is on the substance (display a cost estimate, perform cross-validation), not on the specific wording of how to implement it. Functional-typing's blanket confirmation treats the convergence as covering both substance and wording, which constrains Round 2's ability to improve the remediation text.

### T-4: D-3 (--output flag rename) is a new deferred item without Round 1 grounding

Functional-typing introduces D-3: rename `--output` to `--dir` or `--workspace` as a P3 deferred item, citing the arbiter's observation at resolution.md line 87. This is a reasonable forward-looking suggestion. However, the arbiter's observation was made in an advisory capacity and was not part of any convergence or dispute resolution. Adding it to the deferred items list gives it more standing than the arbiter intended -- the arbiter said "consider renaming" as a passing note, not as a deferred recommendation.

This is a minor tension. The item is correctly prioritized at P3 and correctly marked as "new." But the deferred items list from Round 1 (D-1 and D-2) had convergence support from multiple reviewers. D-3 has support from one reviewer and an advisory arbiter note. If D-3 is included, it should acknowledge that it is a single-reviewer recommendation endorsed by an advisory comment, not a convergence-backed deferral.

---

## Safe Agreements

### SA-1: All three disputes are correctly resolved

Functional-typing's resolution of all three disputes (CLARIFY-tag handling, --output framing, generated config completeness) aligns with my own positions. The reasoning is well-grounded and adds substantive depth beyond restating the synthesis:

- On Dispute 1: The two independent grounds for rejecting `integration` as a default (Domain Agnosticism violation and conflation of calibration style with mode selection) are architecturally precise. The second ground -- that calibration style and mode selection have different input spaces -- is a point the arbiter made (resolution.md lines 124-125) that functional-typing correctly integrates into the reasoning.

- On Dispute 2: The acceptance of workspace-override framing is correct and the acknowledgment of the naming mismatch as a P3 concern (rather than a P1 documentation concern) is appropriately scoped.

- On Dispute 3: The forward-looking argument from the arbiter (if future specs add guided commands, "starter template" language needs retraction) is correctly identified as a consideration I had not surfaced.

### SA-2: Prior concessions are correctly upheld

Functional-typing's statement that all four prior concessions stand is correct. Each concession was well-grounded in Round 1 and the Round 2 context reinforces rather than undermines them. The explicit enumeration (P0 severity demotion, CLARIFY-tag extract-and-warn withdrawal, staleness warning withdrawal, specification drift reframing) provides clear traceability.

### SA-3: MO-1 (interest count validation boundary) is a genuine gap

Regardless of the preferred resolution, the observation that the spec says "2-5" and the SKILL.md enforces only "2+" is a real divergence that all three reviewers missed in Round 1. This is a valid new finding at P2 priority. The two proposed resolutions (add upper bound to SKILL.md, or relax spec to "2 or more") are both reasonable -- the choice is a design decision about whether the quadratic scaling is sufficiently dangerous to warrant a hard cap.

### SA-4: The review's overall structure and rigor are strong

Functional-typing's Round 2 review is well-organized: it explicitly addresses each dispute, confirms or corrects each convergence point, identifies genuine missed opportunities, and provides a complete actionable recommendations table with source tracing. The review correctly scopes itself to Round 2's purpose (closing disputes, surfacing missed items) rather than relitigating settled positions. The referenced documentation section is comprehensive and enables independent verification of every claim.

### SA-5: S-5 (reconcile interest count range) is correctly added to the actionable recommendations

The addition of S-5 to the spec changes table, with either-or resolution options and P2 priority, is appropriate. The item is real, the priority is proportionate, and both resolution paths are clearly stated. This should be carried forward into the final synthesis.
