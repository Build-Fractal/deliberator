# Phase 4 Disputes — skeptic-mathematical

The revision phase resolved most of the surface friction across the three positions. Two genuine disputes remain that the synthesis must resolve before this gate can land coherently. They are not re-litigation of withdrawn recommendations — they are forks the revisions did not close.

---

### Remaining Disputes

**Dispute: Grandfathering disposition — non-precedential footnote vs. tiered classification with v3.0.0 audit**

- *My claim*: The grandfathering text needs a single non-precedential footnote (my R-N2, aligned with practitioner's withdrawn-but-residual concern) that warns future authors which existing principles to model on, and explicitly disclaims any procedural force against pre-gate principles. No tiering, no audit deadline, no migration-candidate list.
- *Opposing position(s)*: Skeptic-cross-principle's revised Recommendation 4 retains a three-tier classification (exemplar / tolerated / migration-candidate) and binds "migration-candidate" principles to a v3.0.0 disposition deadline. Their revised Recommendation 8 additionally pulls Extension blocks of grandfathered principles into the gate, which retroactively narrows pre-gate principles' modification surface.
- *Why I will not concede*: The tier-plus-deadline approach reproduces, in a softer form, exactly the contradiction practitioner's contradiction #2 identified and that I withdrew my own original Recommendation 4 over: it pre-litigates migration without the migration spec the prospective-only clause itself requires. Skeptic-cross-principle's "permanent exception listing the failing criteria" for tolerated principles is the procedural cudgel I withdrew my own tiering to avoid handing future authors. The Extension-block gating goes further — it converts grandfathering from "existing principles retain ratified status" to "existing principles retain ratified status only until the next time they are touched," which is a different and stricter rule than the constitution currently states.
- *Counter-argument*: Skeptic-cross-principle would argue that without a deadline, "tolerated" status is permanent and the two-tier constitution never collapses. That is correct as a description. My response is that intentional permanence is the right design for a constitution: pre-gate principles were ratified under the rules in force at ratification time, and changing the rules retroactively is exactly what the prospective-only clause exists to prevent. A two-tier constitution that collapses when authors choose to migrate (via the standard amendment process) is honest; one that collapses on a deadline pressures migration regardless of readiness.
- *Proposed resolution path*: The synthesis should adopt the footnote (my R-N2 wording or equivalent) as the grandfathering disposition. It should NOT adopt tiered classification, "permanent exception" listings, the v3.0.0 audit deadline, or Extension-block gating of grandfathered principles. If the synthesizer judges that calibration requires a stronger signal than a footnote, the next-strongest acceptable form is naming the well-modeled principles (XI, XII, XIII, XXII, XXIV, XXVI) without naming the poorly-modeled ones — positive guidance only, no demotion lever. The migration-candidate list (VI, X, XVI, XX, XXI per skeptic-cross-principle) should live in a separate follow-up issue or spec, not in the gate amendment itself.

**Dispute: Criterion 3 operational test — distinctness block (skeptic-cross-principle N1) vs. worked-example calibration (my modified Recommendation 3 + R-N1)**

- *My claim*: Criterion 3's calibration is best served by two worked rejection examples — one for mechanical-falsifiability failure, one for distinctness-or-composition failure (my modified Recommendation 3) — plus a worked interaction-conflict example in the PR template's compatibility section (my R-N1). Examples calibrate reviewers; structured blocks add procedural surface that does not reliably catch the error mode they target.
- *Opposing position(s)*: Skeptic-cross-principle's new Recommendation N1 requires amendments to include a structured `Existing-Principle-Distinctness:` block citing (a) the 2-3 closest principles, (b) the novel predicate, (c) why an Extension block is insufficient. Practitioner's modified Recommendation 4 sits between us, expanding worked examples to two (one rejection, one accepted scope-extension on the XXVII precedent).
- *Why I will not concede*: The distinctness block is structurally similar to the vocabulary-novelty test I withdrew, and inherits the same failure mode in a different costume. Amendment authors will satisfy the block by listing the three nearest principles, asserting a predicate they call novel, and asserting an Extension block insufficient. The block is mechanically tractable but its outputs are author self-certifications, not falsifiable claims — exactly the rhetorical-rather-than-operational failure mode my own original review flagged the gate for. By contrast, worked examples in the gate text constrain *reviewer* interpretation: a reviewer reading two worked rejections has calibration anchors when reading a real amendment. Examples bind reviewers; blocks do not bind authors.
- *Counter-argument*: Skeptic-cross-principle would argue worked examples are educational but not enforceable — a reviewer can ignore them where a missing block fails the template check. That is correct in form. My response is that the PR template (modified Recommendation 10, promoted to P1) already provides the enforcement vehicle: the template requires a Distinctness section. What that section should *contain* is the open question. A free-form distinctness statement plus worked examples gives the reviewer calibration without manufacturing a procedural surface that authors will satisfy mechanically. The structured block adds the appearance of rigor without the substance.
- *Proposed resolution path*: The synthesis should adopt practitioner's two-example expansion (one rejection, one accepted scope-extension citing XXVII as precedent) for the gate text proper, and require the PR template's Distinctness section to contain a free-form statement referencing the gate's worked examples. The structured `Existing-Principle-Distinctness:` block from skeptic-cross-principle's N1 should NOT be required as a separate template section. If the synthesizer judges that a structured block adds enforcement value, the lighter form is acceptable: require the Distinctness section to *name* the closest existing principle and state in one sentence why it is insufficient — without the three-part (a)/(b)/(c) sub-structure, which is where the mechanical-satisfaction failure mode lives.

---

### Convergence

**Converged: Enforcement is the dominant defect, PR template paired with named human reviewer is the fix**

- *Shared position*: All three Phase 3 revisions converge on this as the highest-leverage single change, and on the pairing requirement.
- *Agreeing agents*: skeptic-mathematical (modified Recommendation 10 promoted to P1, plus R-N3 named human reviewer), skeptic-cross-principle (kept Recommendation 6 plus N3 CODEOWNERS-defined maintainer), practitioner (kept Recommendation 1 plus new Recommendation 12 paired-bundle requirement).
- *Strength*: Strong. Independent derivation of both the mechanism and the pairing constraint from three different review lenses.
- *Path*: Synthesis adopts: (1) PR template with required sections, (2) maintainer review by at least one CODEOWNER who is not the amendment author, (3) explicit constitutional text stating the pairing — neither alone counts as gate enforcement.

**Converged: Replace "concrete enough to sketch in one paragraph" with named-artifact-or-pseudocode requirement**

- *Shared position*: The "one paragraph sketch" sub-clause is the gate's weakest sentence and must be replaced with a structured artifact requirement.
- *Agreeing agents*: skeptic-mathematical (modified Recommendation 1, artifact-or-named-pointer-or-5-10-line-pseudocode), skeptic-cross-principle (kept Recommendation 2, structured `Verification:` block with deferrable implementation but required tracking artifact), practitioner (kept Recommendation 2 refined, adopted skeptic-cross-principle's `Verification:` block framing).
- *Strength*: Strong. All three reviewers independently reached compatible formulations; the residual differences are wording, not substance.
- *Path*: Synthesis adopts the structured-block framing from skeptic-cross-principle, with the deferred-but-tracked discipline from skeptic-mathematical. The block requires: check type, artifact (file path / lint rule / CI job / 5-10 line pseudo-code), failure signal. If the working artifact does not exist at amendment time, the block cites the tracking issue or spec.

**Converged: CODEOWNERS-grounded maintainer role, not phantom designation**

- *Shared position*: A maintainer-review enforcer requires the maintainer role to be defined in an existing artifact, not introduced by the gate amendment itself.
- *Agreeing agents*: skeptic-cross-principle (new Recommendation N3 explicitly grounds the role in CODEOWNERS), practitioner (new Recommendation 11 makes the maintainer-role definition a prerequisite amendment), skeptic-mathematical (R-N3 implies but does not name the artifact; consistent with the explicit framings).
- *Strength*: Moderate-to-strong. The framings differ in sequencing (skeptic-cross-principle: cite existing CODEOWNERS; practitioner: separate prerequisite amendment if missing) but agree on the structural requirement.
- *Path*: Synthesis verifies whether `conversus-oss` has a CODEOWNERS file or named GitHub team for `constitution.md`. If yes, cite it directly in the gate's enforcer clause. If no, the gate amendment is conditional on a paired amendment establishing the role; ship them together or block the gate.

**Converged: Withdraw periodic-audit and auto-reclassification mechanisms; governance auto-anything is contradictory**

- *Shared position*: Auto-reclassification deadlines, every-MAJOR audits, and auto-demotion timers are bad governance design — they bypass the migration-spec discipline the constitution itself mandates.
- *Agreeing agents*: skeptic-mathematical (withdrew Recommendation 6 deadline and Recommendation 9 periodic audit), practitioner (withdrew Recommendation 9, accepted no replacement). Skeptic-cross-principle's revised Recommendation 4 is the holdout via tiering+deadline.
- *Strength*: Moderate. Two of three converged; one (skeptic-cross-principle) softened but did not withdraw.
- *Path*: Synthesis treats this as an established convergence and resolves the residual disagreement via the first remaining dispute above (footnote, not tiering).

**Converged: Withdraw vocabulary-novelty test and "delete Criterion 1" simplification**

- *Shared position*: Both the vocabulary-novelty test (my original Recommendation 7) and the delete-Criterion-1 simplification (practitioner's original Recommendation 3) are worse than the disease.
- *Agreeing agents*: All three reviewers agreed on both withdrawals via cross-review pressure.
- *Strength*: Strong. Symmetric withdrawal with no holdout.
- *Path*: Synthesis treats Criterion 1 as load-bearing (with the artifact-block fix from convergence #2) and rejects the vocabulary-novelty mechanism in favor of worked examples (subject to the second remaining dispute above).

---

### Final Position Statement

**Non-Negotiables**

1. **The PR template and named maintainer reviewer ship as a paired bundle, with explicit constitutional text stating the pairing.** A template without a maintainer is bot rubber-stamping; a maintainer without a template is human rubber-stamping. The constitutional text MUST state that gate enforcement is the conjunction of both, not either alone. This is the single load-bearing change without which every other recommendation is rhetorical.

2. **Grandfathering is preserved as ratified status, not demoted by tiering, deadline, or Extension-block gating.** The synthesis adopts a non-precedential footnote (positive modeling guidance) at most. Pre-gate principles I-XXVII retain full ratification. Any migration of pre-gate principles to operational guidance happens via the standard amendment process with a migration spec — not via the gate amendment, not via auto-reclassification, not via Extension-block retroactivity.

3. **Criterion 1's artifact requirement is structured and enforced; Criterion 2 and Criterion 3 retain their wording responsibilities.** The "one paragraph sketch" sub-clause is replaced by a structured Verification block. Criterion 1 is not collapsed into Criterion 2; Criterion 3 is not absorbed into Principle XI. The three-criterion structure is retained because mechanization (the PR template) is what makes it operational.

**Flexibility**

1. **Worked-example count and form**. Two worked rejection examples are my position; one is acceptable if the synthesizer judges constitutional length a real constraint. The accepted scope-extension example (practitioner's XXVII precedent) is preferred but not strictly required if the rejection examples are well-chosen.

2. **Distinctness section structure**. Free-form statement plus worked examples is my position. A lighter structured form (name closest principle + one sentence on insufficiency) is acceptable. Skeptic-cross-principle's three-part (a)/(b)/(c) block is the form I will not concede to, but anything between free-form and that level of structure is negotiable.

3. **Asymmetry acknowledgment in Governance**. Whether the gate-vs-grandfathered enforcement asymmetry is acknowledged in one sentence (my modified Recommendation 8), in skeptic-cross-principle's N2 framing, or implicitly through the grandfathering footnote is a wording question. The asymmetry is real and should be visible somewhere; the exact location is flexible.
