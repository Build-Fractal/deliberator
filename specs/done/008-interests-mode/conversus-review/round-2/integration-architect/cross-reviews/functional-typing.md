# Cross-Review of functional-typing — Round 2

**Cross-reviewer**: integration-architect
**Reviewing**: functional-typing's Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: MO-1 proposes relaxing the spec's interest count upper bound, but the cost estimate convergence (C-6, K-5) already relies on N being manageable

Functional-typing's MO-1 identifies a genuine gap: the spec says "2-5 competing interests" (spec.md line 31) while SKILL.md post-write validation enforces only "at least 2" (SKILL.md line 1059). The gap is real and I missed it in both rounds. However, functional-typing's preferred resolution — relaxing the spec to "2 or more" and relying on the cost estimate as the user's throttle — contradicts the design implications of the converged cost estimate recommendation (C-6, K-5).

The cost formula is N^2 + N + 1. At N=5, that is 31 agent launches per round. At N=8, it is 73. At N=12, it is 157. The cost estimate was converged as an informational display at mode confirmation (final.md, lines 327-329), not as a validation gate. There is no mechanism in the converged recommendations that would *prevent* a user from confirming 12 agents after seeing "Estimated agent launches per round: 157" — the estimate is advisory, the user clicks yes, and the system launches 157 agents.

If functional-typing's resolution 2 is adopted, the cost estimate must be promoted from informational display to a confirmation gate with explicit acknowledgment above some threshold — otherwise the "let the cost estimate serve as the user's throttle" claim has no enforcement mechanism. This is a meaningful change to the C-6/K-5 convergence that functional-typing does not acknowledge. The cost estimate was converged as a display element, not as a validation gate, and changing it to a gate reopens a settled item.

The cleaner resolution is functional-typing's own resolution 1: add the upper-bound validation to SKILL.md (line 1059) to match the spec. If the bound of 5 is too restrictive, the threshold can be raised (to 7 or 8) while still providing a hard ceiling that prevents runaway agent costs without requiring the cost estimate to become a gate. This preserves the C-6/K-5 convergence as-is.

### DC-2: OBA-1 claims the equal-probability assumption for heuristic detection is "inconsequential," but this undercuts the rationale for the cross-validation warning (K-6)

Functional-typing's OBA-1 observes that the heuristic detection section and the C-1 convergence assume all four modes are equally plausible candidates when heuristic detection fires. Functional-typing then dismisses this as "off-base but inconsequential" because the user makes the final decision regardless.

This contradicts the rationale for the cross-validation warning (K-6, final.md lines 333-337), which my own MO-2 also addresses. K-6 exists precisely because the mode recommendation is *not* equally valid for all type/interest combinations — when interest naming patterns diverge from the stated problem type, the recommendation may be misleading. If all four modes were equally valid starting positions regardless of signals (as OBA-1 implies by calling the equal-probability assumption inconsequential), K-6 would be unnecessary — there would be nothing to cross-validate.

The equal-probability assumption matters for exactly the reason functional-typing identifies (the problem genuinely does not map cleanly to one type) and then dismisses. When heuristic detection fires on a genuinely ambiguous problem, the interest naming patterns become the strongest available signal for mode selection. The K-6 cross-validation warning depends on this signal being meaningful. Calling the equal-probability assumption inconsequential weakens the justification for K-6, which is a P2 converged recommendation that both functional-typing and I endorsed.

The fix is straightforward: OBA-1 should not dismiss the observation. The unequal prior probability of modes under heuristic detection is precisely why K-6 (cross-validation) and K-7 (zero-signal presentation of all four modes) exist as separate mechanisms — K-6 handles the case where signals exist but conflict with stated type, K-7 handles the case where no signals exist at all. Both mechanisms are necessary because the modes are *not* equally likely, which is consequential, not inconsequential.

---

## Tensions

### T-1: MO-2 correctly identifies the `(none)` sentinel mismatch but assigns it P3 on the wrong grounds

Functional-typing's MO-2 identifies the same sentinel mismatch that my MO-3 identifies: the define handler writes `(none — no context documents provided)` (SKILL.md line 891) while the mode handler checks for `(none)` (SKILL.md line 1254). Our observations are factually aligned. But functional-typing assigns P3 because "the SKILL.md already handles this correctly" and defers to D-1.

The SKILL.md does not handle this correctly — that is the point. The mode handler checks for `(none)` (a short string) while the define handler produces `(none — no context documents provided)` (a longer string). Whether this "works" depends entirely on whether the implementer uses substring matching or exact matching, which the SKILL.md does not specify. Functional-typing acknowledges this ("This is likely handled by substring matching in practice") but treats implementation-dependent behavior as equivalent to correct specification.

My MO-3 assigns P2 and recommends an explicit fix within spec 008 rather than deferring. The tension between our positions is about whether unspecified-but-probably-fine behavior should be formalized now (my position) or deferred (functional-typing's position). Given that this is a current code path — the mode handler already consumes this sentinel — I maintain P2 is the correct priority. Deferring to D-1 means the mismatch ships without explicit resolution, relying on implementer judgment about matching strategy.

### T-2: Dispute 1 resolution accepts the arbiter's "recommend, do not require" language without addressing the ambiguity in "recommend"

Functional-typing's alignment on Dispute 1 is thorough and well-grounded. The analysis of why `integration` as a neutral default fails (two independent grounds: domain agnosticism violation and calibration/mode conflation) is sharper than my own Round 1 reasoning. The acceptance of the arbiter's observation about the define handler's deferred resolution design (resolution.md, lines 60-62) is correct.

However, functional-typing's position statement ("Present the four calibration styles inline with the CLARIFY tag's context. Let the user choose. If they decline, recommend `/conversus define` to resolve the tag. Do not default. Do not block.") uses "recommend" without specifying the form of the recommendation. Is "recommend" a displayed message ("We suggest running /conversus define")? A prompt with options ("Would you like to: (a) run /conversus define, (b) skip and proceed without calibration")? A blocking prompt that requires explicit dismissal?

My AR-4 addresses a related concern — that the four calibration styles should use plain-language descriptions, not type names — but neither of us specifies the UX of the "recommend" fallback path. This is a minor implementation gap in the otherwise well-resolved dispute, not a disagreement.

### T-3: S-5 (interest count reconciliation) is listed as a spec change but may require a SKILL.md change instead

Functional-typing lists S-5 as a spec change at P2: "Reconcile interest count range: spec says '2-5', SKILL.md enforces '2+.'" But the two possible resolutions point in opposite directions:

- Resolution 1 (add upper bound to SKILL.md) is a SKILL.md change, not a spec change.
- Resolution 2 (relax spec to "2 or more") is a spec change.

Listing this as a spec change before the resolution direction is decided is premature. The recommendation should be listed as a reconciliation action on both documents, with the resolution direction noted as open. This is a minor organizational issue, not a substantive disagreement.

### T-4: D-3 (`--output` flag rename) may be premature as a deferred item

Functional-typing adds D-3 — renaming `--output` to `--dir` or `--workspace` — as a P3 deferred item sourced from the arbiter's suggestion (resolution.md, line 87). I agree the naming mismatch exists and is worth noting. However, creating a deferred item for a flag rename in a system with no shipped CLI and no backward-compatibility constraints may be overengineering the deferral process. If the flag should be renamed, it can be renamed in the SKILL.md directly as a P3 editorial change in spec 008 rather than creating a deferred item that implies future spec work.

This is a process tension, not a substantive disagreement. The observation is valid either way.

---

## Safe Agreements

### SA-1: All three Round 1 disputes are correctly resolved

Functional-typing's alignment on all three disputes matches mine exactly. The reasoning is independently derived and mutually reinforcing:

- **Dispute 1**: Both accept the synthesis + arbiter position. Functional-typing's two-grounds analysis (domain agnosticism violation and calibration/mode conflation) is more structured than my single-ground alignment. The conclusion is identical: present four calibration styles, let user choose, recommend define if they decline, no default.

- **Dispute 2**: Both withdraw competing framings and adopt the workspace-override characterization. Functional-typing's explicit statement that the `cd` analogy is "decisive" confirms convergence.

- **Dispute 3**: Both affirm the "complete config with extensions" framing. Functional-typing's forward-looking argument (from the arbiter) about future guided commands making "starter template" language retractable is a useful addition I had not incorporated.

### SA-2: No prior concessions should be reversed

Both reviews explicitly confirm that all prior concessions stand. Functional-typing lists four concessions (P0 severity demotion, CLARIFY-tag extract-and-warn withdrawal, staleness warning withdrawal, "specification drift" reframing); I list four concessions (FR-007 downgrade, Preset field as spec omission, preset validation escalation, extract-and-warn withdrawal). Neither review identifies any reason to reopen any concession from either reviewer. This bilateral confirmation closes the concession set definitively.

### SA-3: Convergence items C-1 through C-10 and actionable changes S-1 through S-4, K-1 through K-8 are settled

Both reviews confirm all convergence items and the full set of actionable changes without modification to any item's substance or priority. The converged recommendations are ready for implementation.

### SA-4: The interest count upper-bound gap is a genuine finding

Functional-typing's MO-1 identifies a real divergence between spec and SKILL.md that all three Round 1 reviewers missed. The spec says "2-5" (spec.md line 31); the SKILL.md enforces only "2+" (SKILL.md line 1059). The gap exists. I disagree with the preferred resolution (see DC-1 above) but agree the gap must be closed in one direction or the other.

### SA-5: The `(none)` sentinel mismatch is a genuine finding that extends D-1

Both reviews independently identify the same string-mismatch between the define handler's long-form sentinel (`(none — no context documents provided)`) and the mode handler's short-form check (`(none)`). We agree the mismatch is real and should be resolved. We disagree on priority (P3 vs P2) and timing (defer vs fix now), as noted in T-1 above, but the factual observation is fully aligned.

### SA-6: The spec and SKILL.md remain substantively sound with no blocking defects

Both reviews explicitly confirm that no blocking defects exist. Both frame Round 2 contributions as precision improvements to converged recommendations and identification of gaps within the agreed framework, not as challenges to the framework itself. The deliberation is mature and the remaining work is editorial and implementational.

### SA-7: Functional-typing's acceptance of the arbiter's reasoning is thorough and well-grounded

Functional-typing's Dispute 1 analysis deserves specific recognition. The two-grounds argument (domain agnosticism as independent from the confirmation gate, and the calibration/mode conflation as a separate architectural error) is cleaner than the synthesis's single-narrative presentation. The explicit acknowledgment that the CLARIFY tag's deferred resolution design means `define` routing should be recommended but not required (per the arbiter's "recommend is load-bearing" observation) demonstrates genuine engagement with the arbiter's reasoning rather than pro forma acceptance.

---

## Summary

Functional-typing's Round 2 review is well-structured and demonstrates genuine alignment with the synthesis and arbiter positions. The dispute resolutions are correctly adopted with independent reasoning. The two missed opportunities (MO-1 interest count gap, MO-2 sentinel mismatch) are both legitimate findings that extend the deliberation's coverage.

Two dangerous contradictions exist. First, the preferred resolution for MO-1 (relax to "2 or more") implicitly requires promoting the cost estimate from display to gate, which reopens the C-6/K-5 convergence without acknowledging the dependency. Second, OBA-1's dismissal of the equal-probability assumption as inconsequential contradicts the rationale for the K-6 cross-validation warning that both reviewers endorsed.

Four tensions exist, all concerning priority, timing, or organizational precision rather than substantive disagreement. The sentinel mismatch priority (P2 vs P3) is the most consequential of these.

Seven safe agreements confirm that the deliberation has reached stable convergence on all previously settled items, all dispute resolutions, and all concessions. The remaining work is implementation-level precision within the agreed framework.
