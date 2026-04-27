# Phase 4 Disputes — skeptic-cross-principle

I have read all three Phase 3 revisions (skeptic-mathematical, practitioner, my own) and the v2.4.0-blind target. Below I record what I still dispute, what has converged, and the position I am willing to ratify.

---

### Remaining Disputes

**Dispute 1 — Grandfathering treatment: tiered classification with v3.0.0 audit (mine) vs. non-precedential footnote (skeptic-mathematical R-N2, practitioner withdrawal of #6).**

This is the deepest unresolved disagreement. Both other reviewers converged in Phase 3 on a *softer* grandfathering treatment than mine. Skeptic-mathematical adopted practitioner's footnote framing in their R-N2 ("future amendments SHOULD be modeled on principles with named verification artifacts (XI, XII, XIII, XXII, XXIV, XXVI), not on principles whose verification path is implicit (X, XVI, prose subsections of IX)"). Practitioner withdrew their own softer footnote (#6) on grounds that it institutionalized a permanent two-tier constitution. The result is that skeptic-mathematical now holds the position practitioner explicitly abandoned, while I hold the only position that actually forces resolution.

I still maintain that the footnote-only approach is structurally wrong. Practitioner's *original* objection to their own footnote was correct: it codifies a permanent two-tier constitution by listing X, XVI, and prose subsections of IX as "do not model on me" without ever providing a path to remediation. Skeptic-mathematical's R-N2 inherits this defect. My tiered classification (exemplar / tolerated / migration-candidate) with v3.0.0 audit for migration-candidates only is the only proposal that pairs the calibration warning with a forcing mechanism. Without the deadline, the footnote becomes the constitutional equivalent of a `# TODO` comment that compounds across releases.

I concede the practitioner's contradiction-#3 against my Phase 2 proposal: combining a time-boxed audit with a permanent footnote creates contradictory posture. My Phase 3 revision already addressed this by collapsing the footnote into the tiering itself — "tolerated" principles persist with documented exception listing the failing criteria, "migration-candidates" must be dispositioned by v3.0.0. I do not claim victory on this dispute; I claim the footnote-only path is incomplete and the synthesis should adopt my tiering at minimum as a starting structure.

**Dispute 2 — Extension blocks subject to the gate (mine, retained) vs. silent on Extension blocks (both other reviewers).**

Neither skeptic-mathematical nor practitioner addressed Extension blocks in their Phase 3 revisions. My Phase 2 recommendation #8 (Extension blocks ARE amendments and MUST satisfy the gate) survived without challenge, but it also survived without endorsement. This is consequential: Principle IX has a v2.3.0 Extension (behavior-over-shape testing), Principle XI has a v2.3.0 Extension (registry-first declaration), Principle XV has a v2.3.1 Clarification. Under the current grandfathering text, these are pre-gate principles — but the *Extensions* postdate the gate as currently written.

The grandfathering clause says "Existing principles I-XXVII are grandfathered" but does not specify whether *future Extensions to grandfathered principles* must satisfy the gate. I argue they must; absent that rule, every grandfathered principle becomes a backdoor admission channel for prose-only additions. Skeptic-mathematical's withdrawn Recommendation 9 (periodic re-evaluation) gestured at this concern; practitioner did not engage with it.

I maintain this dispute and request the synthesis explicitly address Extension-block treatment. The minimum acceptable resolution: Extension blocks landing after the gate's ratification date MUST satisfy criteria 1, 2, 3 even when extending a grandfathered principle.

**Dispute 3 — Whether Criterion 2 should be demoted (mine) or retained as a co-equal criterion (both other reviewers).**

My Phase 3 disposition kept Recommendation 3 (demote criterion 2 to a one-sentence Governance note). Skeptic-mathematical's Phase 3 withdrew their own collapse-criteria-1-and-2 recommendation, but their reasoning leaves criterion 2 in place as a structural co-equal. Practitioner's Phase 3 keeps all three criteria.

I still hold criterion 2 (falsifiable scope) is partially encoded by Principle II's exemplar discipline and the constitution's MUST/SHOULD language. Keeping it as a co-equal criterion implies three distinct verification artifacts when only two structural questions exist: "is there a check?" (criterion 1) and "is the scope distinct?" (criterion 3). Criterion 2 is a wording-quality property, not a verification property — it belongs in the amendment process description, not as a criterion. This is a smaller dispute than the first two; I flag it but will defer to either reviewer's position in synthesis if the PR-template machinery (now P1 across all three reviewers) lands.

---

### Convergence

**Convergence 1 — The "concrete enough to sketch in one paragraph" sub-clause must be replaced with a structured artifact requirement.**

All three reviewers independently arrived at this fix in Phase 1, defended it in Phase 2 cross-review, and refined it in Phase 3. My structured `Verification:` block (check type + named artifact + failure signal + tracking-spec citation if deferred) is the synthesis target. Skeptic-mathematical's modified Recommendation 1 ("named artifact location or 5-10 line pseudo-code") is a strict subset. Practitioner's refined Recommendation 2 explicitly adopts my structured-block framing.

**Convergence 2 — The gate has no enforcer, and that is the largest single defect.**

All three reviewers' Phase 3 revisions agree on this as the highest-priority finding. Skeptic-mathematical promoted their structured-PR-template recommendation from P3 to P1. Practitioner ranked their PR-template + CI-lint as the strongest convergent finding. I retained my enforcement-path recommendation as a P1. The synthesis vehicle is: PR template with required sections + CI lint + maintainer review tied to CODEOWNERS.

**Convergence 3 — Maintainer role must be defined before requiring maintainer review.**

Skeptic-mathematical's R-N3, practitioner's #11, and my N3 all converge on the same procedural prerequisite: cite CODEOWNERS or a named GitHub team as the source of authoritative reviewer identity. Without this, the enforcer clause is enforcement-by-self-designation. The synthesis text should establish CODEOWNERS as the source of truth and pair the enforcer requirement with the role definition.

**Convergence 4 — Worked examples are required, and at least two of them.**

Skeptic-mathematical's modified Recommendation 3 (two worked rejections — falsifiability failure and distinctness failure) plus their R-N1 (worked interaction-conflict example) converges with practitioner's expanded Recommendation 4 (clean rejection + accepted scope-extension exemplar) and my N1 (`Existing-Principle-Distinctness:` block with cited closest principles). The synthesis should ship at least two worked examples in the gate text plus a structured distinctness block in the PR template.

**Convergence 5 — Recommendations 1 (PR template + CI lint) and 5/N3 (maintainer review) MUST ship as a paired bundle, not independently.**

Practitioner's new Recommendation 12, skeptic-mathematical's R-N3 ("template is the artifact; maintainer is the enforcer; both required"), and my N3 (maintainer review tied to CODEOWNERS) all encode this pairing. A template without a human reviewer is bot rubber-stamping; a reviewer without a template is human rubber-stamping. The synthesis text MUST state the pairing as a non-separable requirement.

---

### Final Position Statement

**Non-Negotiables:**

1. **Replace the "sketch in one paragraph" sub-clause with a structured `Verification:` block** that names the check type, the verification artifact (file path, lint rule, parity test, schema constraint, or named CI job), and the failure signal. If the artifact does not exist at amendment time, a tracking spec or issue MUST be cited within the block. This is the gate's only load-bearing artifact requirement; without it, criterion 1 is rhetorical.

2. **The enforcement path is non-optional.** The gate MUST be enforced by (a) a PR template with required sections corresponding to each criterion, (b) a CI lint that fails the PR if any required section is empty or missing, AND (c) review sign-off from at least one CODEOWNER of `constitution.md` who is not the amendment author. All three ship together or none ship — a partial implementation produces enforcement theater worse than the status quo.

3. **Extension blocks landing after the gate's ratification date MUST satisfy criteria 1, 2, and 3 even when extending a grandfathered principle.** Without this rule, every grandfathered principle becomes a backdoor admission channel for prose-only additions, and the gate's prospective applicability becomes a loophole rather than a discipline.

**Flexibility:**

1. **Grandfathering remediation mechanism.** I prefer my tiered classification (exemplar / tolerated / migration-candidate) with v3.0.0 audit for migration-candidates only, but I will accept skeptic-mathematical's R-N2 footnote as a starting point IF the synthesis adds a forcing mechanism (e.g., the v3.0.0 audit applies to the explicitly-named "implicit verification path" principles X, XVI, prose subsections of IX). The non-negotiable property is that grandfathering must have a path to remediation, not a permanent footnote.

2. **Criterion 2 status.** I prefer demoting criterion 2 to a Governance prose note, but I will accept retention as a co-equal criterion if the PR-template machinery lands. The structural redundancy with II's exemplar discipline and the MUST/SHOULD language is a secondary defect — fixing enforcement matters more than fixing redundancy.

3. **Distinctness test mechanism.** I prefer my `Existing-Principle-Distinctness:` block (cite 2-3 closest principles + name the novel predicate + explain why an Extension would be insufficient). I will accept practitioner's worked-example approach as a complement, but the structured block is the structural test that catches restatement; worked examples calibrate but do not enforce. The synthesis should ship both — block as enforcement, examples as calibration.

The synthesis target I am willing to ratify: structured `Verification:` block + structured `Existing-Principle-Distinctness:` block + PR template with required sections + CI lint + CODEOWNERS-defined maintainer review + at least two worked examples + Extension-block gating after ratification + grandfathering remediation mechanism (tiering OR footnote-with-forcing-deadline). Anything weaker leaves the gate rhetorical; anything stronger pre-litigates content decisions that belong in subsequent amendments.
