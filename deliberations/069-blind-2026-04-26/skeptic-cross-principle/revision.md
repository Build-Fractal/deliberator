# Phase 3 Revision — skeptic-cross-principle (iteration 1)

I read both cross-reviews against my original review and the v2.4.0 target. The cross-reviews surfaced two genuine errors in my original (the XI-extension drift, the maintainer-role gap) and validated three core findings (the "one paragraph" sub-clause is broken, grandfathering is under-specified, the gate has no enforcer). I revise accordingly. Below I dispose of every recommendation in my original review, add one new recommendation prompted by the cross-reviews, and restate my position.

---

### Recommendation Dispositions

**Original Recommendation 1 — Merge gate criterion 3 into Principle XI.**
**Disposition: WITHDRAWN.** Practitioner Dangerous Contradiction §2 caught a genuine error: my proposed XI extension ("a new principle that restates an existing principle in different words is a duplication") would convert XI from a *data-duplication* principle (its origin: MODE_PRESENCE / INFLUENCE_LEVEL / FR-018, all detectable by parity tests) into a *prose-duplication* principle, which is exactly the unverifiable kind of rule the gate is meant to exclude. XI's mechanical-verification posture would weaken if amended this way. Skeptic-mathematical Dangerous Contradiction §1 also flagged the incompatibility with their vocabulary-novelty test. **Replacement**: keep criterion 3 in the gate, but tighten its operational test (see new recommendation below) rather than absorb it into XI.

**Original Recommendation 2 — Tighten criterion 1 to a structured `Verification:` block.**
**Disposition: KEPT, strengthened.** Both cross-reviews converged on this fix as the strongest finding (skeptic-mathematical Safe Agreement §1, practitioner Safe Agreement §2). Skeptic-mathematical wanted a stricter bar (working artifact or 5-10 line pseudo-code at amendment time); my proposal kept the artifact deferrable. The cross-review correctly flagged that the stricter bar creates an even sharper two-tier system because grandfathered XII/XIII say "the linter SHOULD eventually check." I now adopt a hybrid: the `Verification:` block is required at amendment time, the implementation is deferrable BUT only with a tracking artifact (issue/spec) cited in the block. This closes the "SHOULD eventually" loophole without demanding a working artifact at amendment time.

**Original Recommendation 3 — Demote criterion 2 (falsifiable scope) to one sentence in the amendment-process description.**
**Disposition: KEPT.** Practitioner Dangerous Contradiction §4 noted that I keep criterion 1 while the practitioner had proposed dropping it; this is a real contradiction between our reviews, but on reflection my position holds. Criterion 1 (mechanical verification) is the gate's only genuinely novel contribution; criterion 2 (falsifiable scope) is partially encoded by II's exemplar and the constitution's MUST/SHOULD discipline. Demoting 2 to one sentence in Governance ("Amendments MUST use MUST/SHOULD/MAY language and MUST be specific enough that a hypothetical PR can be flagged as violating without interpretation") preserves the precision requirement without redundancy.

**Original Recommendation 4 — Time-box the grandfather clause (v3.0.0 audit).**
**Disposition: REVISED.** Practitioner Dangerous Contradiction §3 noted that combining a time-boxed audit with a permanent footnote disclaiming grandfathered principles creates a contradictory posture (retained-as-valid AND pre-flagged-for-removal). Skeptic-mathematical Tension §2 noted that a static "exemplar/tolerated" tier and a time-boxed audit push different incentives but can compose. **Revised**: replace open-ended audit with a tiered classification *now* (exemplar / tolerated / migration-candidate), and require a v3.0.0 disposition for "migration-candidate" only. "Tolerated" principles persist with a documented permanent exception listing the failing criteria. This avoids the contradiction the practitioner flagged while still forcing resolution for the worst offenders.

**Original Recommendation 5 — Identify migration candidates explicitly (VI, X, XVI, XX, XXI).**
**Disposition: KEPT.** Both cross-reviews converged on this candidate list (skeptic-mathematical Safe Agreement §3, practitioner Safe Agreement §3). The practitioner's list (X, XVI, IX-prose) is a strict subset of mine; no contradiction. Under the revised tiering (Disposition 4), these become migration-candidates with a v3.0.0 deadline.

**Original Recommendation 6 — Specify the gate's enforcement path.**
**Disposition: KEPT.** Strongest convergent finding across all three reviews (mine Off-Base Assumption §4, skeptic-mathematical Safe Agreement §3, practitioner Safe Agreement §1). The gate is rhetorical without a `/speckit.constitution` checklist or PR-template enforcement hook. Practitioner Tension §1 raised the asymmetry concern — if the gate gets a CI lint while XII/XIII/XXII §1 still say "SHOULD eventually," the gate has stricter enforcement than the principles it gates. I accept this as a legitimate cost: the gate IS being held to a higher standard, by design (it governs the standard for everything else). The asymmetry should be acknowledged in Governance, not eliminated.

**Original Recommendation 7 — Clarify versioning for migrations.**
**Disposition: KEPT.** Skeptic-mathematical Tension §3 noted that under MAJOR-bump migration, false-admission becomes even stickier than they assumed — strengthening rather than weakening this recommendation. Practitioner Tension §2 noted my framing leaves "what version bump for adopting the gate itself" unaddressed; I now specify: adopting the gate is MINOR (new principle / material expansion of Governance).

**Original Recommendation 8 — Address Extension blocks explicitly (Extension blocks ARE amendments and MUST satisfy the gate).**
**Disposition: KEPT.** Practitioner Tension §3 acknowledged my position is more rigorous and theirs more permissive. Skeptic-mathematical Tension §5 noted Extension-block gating retroactively pulls grandfathered principles into the gate, creating instability — I treat this as a feature, not a bug. The two-tier system collapsing over time IS the path to a single-tier coherent constitution. Without Extension-block gating, the two-tier system is permanent.

**Original Recommendation 9 — Cross-reference the antipatterns catalog.**
**Disposition: KEPT.** Skeptic-mathematical Tension §4 acknowledged this as a genuine gap in their review and recommended folding it in. Practitioner Tension §1 noted that if the antipatterns catalog becomes the migration destination, its maintainer becomes the owner. I extend this recommendation: name the antipatterns catalog AND CONTRIBUTING.md as the two primary destinations, with the catalog being the natural fit for "rules of thumb learned from recurring failures" (VI, X, XX, XXI fit this profile; XVI's plain-language explanation requirement fits CONTRIBUTING.md).

**Original Recommendation 10 — Alternative: remove the gate entirely, fold criterion 1 into Principle XII.**
**Disposition: WITHDRAWN.** Skeptic-mathematical Dangerous Contradiction §2 and practitioner Dangerous Contradiction §1 both flagged this as the most consequential disagreement: collapse-into-existing-principles vs. mechanize-the-gate point in opposite architectural directions. Combined with my withdrawn Recommendation 1, the "remove the gate" path loses its load-bearing piece. Folding criterion 1 into XII would also weaken XII: XII's origin is dead variables and dead Pydantic fields, not constitutional rules. The conceptual stretch is too far. **Replacement**: keep the gate as a discrete construct in Governance, mechanized via Recommendation 6's enforcement path. The gate earns its existence by being the venue where amendment-process discipline is checked.

---

### New Recommendations

**N1. Replace gate criterion 3's operational test with a structured `Existing-Principle-Distinctness:` block.**

Skeptic-mathematical's vocabulary-novelty test (their Recommendation 7) would over-reject — XII and XI legitimately share vocabulary like "schema" and "variable." Practitioner's worked-example proposal (their Recommendation 4) would educate but not enforce. The right structural test: amendments must include a block citing (a) the 2-3 existing principles closest in scope, (b) the *predicate* (the thing the new principle requires) that none of those principles requires, (c) why an Extension block on one of the cited principles would be insufficient. This catches restatement (no novel predicate) and forces the body-vs-new-principle question to be answered explicitly, without devolving into thesaurus puzzles.

**N2. Acknowledge the gate-vs-grandfathered enforcement asymmetry in Governance.**

Practitioner Tension §1 (cross-review of me) raised this: if the gate gets a CI lint while XII/XIII/XXII §1 say "SHOULD eventually check," the gate has stricter enforcement than the principles it gates. Rather than eliminate the asymmetry (which would require shipping working artifacts for every grandfathered principle), Governance should state: "The Constitutional Inclusion Criteria are enforced strictly because they govern the standard for every other principle. Existing principles that defer their verification mechanism ('the linter SHOULD eventually check') retain their grandfathered status; the gate does not retroactively require them to ship."

**N3. Define the maintainer role before requiring non-author maintainer review.**

Practitioner Dangerous Contradiction §4 (cross-review of me) caught a procedural gap: my Recommendation 6 implies a reviewer role, but the constitution does not establish "project maintainer" anywhere. Add to Governance: "Amendment review requires sign-off from at least one CODEOWNER of `constitution.md` who is not the amendment author. The CODEOWNERS file is the single authoritative source for the maintainer role." This grounds the procedural requirement in an existing artifact rather than introducing a phantom role.

---

### Position Summary

The Constitutional Inclusion Criteria gate is **structurally sound but operationally incomplete**. My original position — that the gate would itself fail the gate's own tests — survives Phase 2 cross-review. What changed: (1) my "merge criterion 3 into XI" fix is withdrawn because it weakens XI, replaced with a structured `Existing-Principle-Distinctness:` block; (2) my "remove the gate entirely" alternative is withdrawn because folding criterion 1 into XII overstretches XII's scope; (3) my time-boxed audit is revised into a tiered classification (exemplar / tolerated / migration-candidate) to avoid the contradictory posture the practitioner flagged.

The three convergent findings across all three reviews are robust: the "one paragraph" sub-clause must be replaced with a structured `Verification:` block; grandfathering needs an explicit disposition (now: tiered classification with v3.0.0 audit for migration-candidates only); the gate needs an enforcement path tied to CODEOWNERS-defined maintainer review. Adopting these three plus my N1 (distinctness block) yields a gate that is internally coherent, operationally enforceable, and honest about the two-tier transition period it imposes on the existing corpus.

The key asymmetry I now accept (per practitioner Tension §1): the gate is held to a stricter standard than the principles it gates. This is correct by design — the gate is the venue where amendment-process discipline is checked, so its own discipline must be exemplary. Governance should state this asymmetry rather than try to resolve it by either weakening the gate (skeptic-mathematical's risk) or retroactively upgrading every grandfathered principle's enforcement (impractical).
