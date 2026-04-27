# Practitioner Revision — Constitutional Inclusion Criteria Gate

Iteration 1, Phase 3. Reconciles original recommendations against cross-reviews from skeptic-mathematical and skeptic-cross-principle, and against my own cross-reviews of those reviewers.

The dominant signal across all four cross-review documents: **the gate has no enforcer, and that is the largest single defect**. Every other dispute is downstream of that. I retain that priority. I also retreat from two original recommendations (#3 "delete Criterion 1" and #6 "footnote demoting grandfathered principles") that both skeptics independently flagged as worse than the disease.

---

### Recommendation Dispositions

**Recommendation 1 — Mechanize the gate via PR template + CI lint.**
Status: **KEEP, strengthened.**
Both skeptics independently arrived at the same fix (skeptic-mathematical's Rec 10, skeptic-cross-principle's Rec 6). This is the strongest convergent finding across all three reviewers and is the single highest-leverage change. Skeptic-cross-principle raised one valid concern (Tension 1): mandating a CI lint for the gate creates an asymmetry with grandfathered principles XII / XIII / XXVI that say "the linter SHOULD eventually check." I accept the asymmetry — it is the correct direction of drift. The gate enforcing the gate is the floor; principles can be brought up to that floor over time. The asymmetry is not a reason to weaken the gate's enforcement; it is a reason to upgrade other principles' enforcement later.

**Recommendation 2 — Replace "concrete enough to sketch in one paragraph" with named-artifact requirement.**
Status: **KEEP, refined.**
Strong agreement from both skeptics (skeptic-mathematical's Rec 1; skeptic-cross-principle's Rec 2 with the structured `Verification:` block). My original wording ("name the artifact: file path, test pattern, or schema constraint") is a strict subset of skeptic-cross-principle's `Verification:` block proposal (check type + artifact + failure signal). I adopt the structured-block framing — it's a more rigorous version of the same fix and resolves my own ambiguity about what counts as "naming the artifact."

**Recommendation 3 — Remove Criterion 1 entirely and rely on Criteria 2 and 3 (aggressive simplification).**
Status: **WITHDRAW.**
Skeptic-cross-principle's Dangerous Contradiction #1 is correct: Criterion 1 is the only criterion that adds something the constitution does not already encode. Criterion 3 is largely a restatement of Principle XI applied to the principle corpus. Deleting Criterion 1 inverts the gate's value proposition — keeping the redundant criteria and removing the novel one. My own cross-review of skeptic-mathematical reached the same conclusion against their merge proposal: "the right move is to keep Criterion 1 and strengthen it" (named artifact) rather than collapse it. Withdrawing this recommendation aligns my position internally and removes a fork in the road for downstream readers.

**Recommendation 4 — Add a worked Criterion 3 example.**
Status: **KEEP, expanded.**
Both skeptics support worked examples (skeptic-mathematical's Rec 3, skeptic-cross-principle's recognition of the unsolved boundary problem). Skeptic-cross-principle's Tension 4 raised a sharp point I missed: my proposed example ("Principle XXVIII: lowercase template variables → composes from IX + XI") handles the easy refinement-vs-novel case, but does not handle the harder scope-extension case (e.g., XXVII operator-subtraction extending XV plugin-isolation, which a strict Criterion 3 read could have rejected). Expand Recommendation 4: the gate should carry **two** worked examples — one clean rejection (refinement composes from existing principles) and one accepted scope-extension (XXVII as the precedent that scope expansion can warrant a new principle). Without the second example, Criterion 3 over-rejects in practice.

**Recommendation 5 — Specify the enforcer (mandate non-author maintainer review).**
Status: **KEEP, conditional on resolving the maintainer-role gap.**
Skeptic-cross-principle's Dangerous Contradiction #4 raised a real procedural defect: the constitution does not currently define "project maintainer" — no roster, no role designation, no acceptance criteria. A bare "MUST be reviewed by a maintainer" rule creates an enforcement loophole worse than the current self-assessment. Refinement: the recommendation must specify the artifact resolving the ambiguity. CODEOWNERS file or a named GitHub team is the right pattern. If neither exists, the gate's enforcer clause MUST be paired with a separate amendment establishing the maintainer role. Skeptic-mathematical's framing of "PR template + maintainer review must ship together" (their Tension 3 with my Rec 1) is also load-bearing: a template without a human reviewer is bot rubber-stamping; a reviewer without a template is human rubber-stamping. Both ship together or neither does.

**Recommendation 6 — Footnote disclaiming grandfathered principles X, XVI, prose-of-IX as precedent.**
Status: **WITHDRAW.**
Both skeptics flagged this as worse than the disease. Skeptic-mathematical's Dangerous Contradiction #2: a footnote demoting specific principles from precedential force without going through the constitution's mandated migration path violates the prospective-only carve-out's purpose ("a separate, intentional act"). Skeptic-cross-principle's Dangerous Contradiction #2: the footnote codifies a permanent two-tier constitution and contradicts Principle XI's own anti-duplication logic. Both reviewers correctly identified that this recommendation optimizes for amendment-author UX at the cost of constitutional coherence. The right move is either skeptic-mathematical's tiered audit (which I criticized as too aggressive) or skeptic-cross-principle's time-boxed audit-by-v3.0.0 (which I criticized as too costly), but **not** my softer footnote which inherits the worst properties of both. Withdraw. The grandfathered-precedent problem is real but the remedy needs more thought than a footnote — and probably belongs in a separate amendment, not in this gate.

**Recommendation 7 — Migration spec must identify receiving file's current owner, not just the file.**
Status: **KEEP.**
No reviewer pushed back on this. Skeptic-cross-principle's Tension 1 (re: the antipattern catalog as migration destination) is complementary: if migration sends content to the antipattern catalog, *its* maintainer becomes the named owner. Standard pattern works regardless of destination.

**Recommendation 8 — Sunset clause for "linter SHOULD eventually" hedges (require tracking spec citation).**
Status: **KEEP.**
Both skeptics agreed the indefinite "eventually" carve-out is a debt sink (skeptic-mathematical's Safe Agreement 3; skeptic-cross-principle's convergence on the same). Skeptic-cross-principle's Tension 3 raised the retroactivity question (XII / XIII / XXVI use this hedge without tracking specs — should the rule apply to them?). My answer: prospective only, matching the gate itself. The grandfathering pattern is consistent within this amendment; retroactive cleanup of existing principles is a separate intentional act. This deflects the criticism that I "didn't pick a side" — the side is "match the gate's own grandfathering discipline."

**Recommendation 9 — Document body-vs-new-principle trade-off; permit new principles when extension > one paragraph.**
Status: **WITHDRAW.**
Skeptic-cross-principle's Dangerous Contradiction #3 is sharper than I credited in my own cross-review of them: my "more than one paragraph" threshold is itself unfalsifiable (the trap Criterion 2 was meant to prevent), and the rule re-opens the door Criterion 3 was designed to close. Skeptic-mathematical's vocabulary-novelty test (which I criticized in my cross-review) at least introduces a structural test; my paragraph-length threshold introduces only a quantitative one with no falsifiable scope. The body-bloat problem is real (Principle IX's v2.3.0 Extension is large) but my proposed remedy is worse than the status quo. Withdraw without replacement — let the gate use Criterion 3 strictly, accept that some extensions will land as in-body subsections, and revisit if body-bloat becomes a measurable problem (an issue-tracking observation, not a gate provision).

**Recommendation 10 — Reorder section to lead with enforcement, not criteria; rename "Amendment Inclusion Gate."**
Status: **KEEP.**
Both skeptics independently arrive at the same reordering (skeptic-mathematical's Rec 10, skeptic-cross-principle implicit in their template-replacement framing). High-confidence cosmetic-but-load-bearing fix.

---

### New Recommendations

**Recommendation 11 — Establish maintainer role (CODEOWNERS or named GitHub team) as a separate amendment, prerequisite for Recommendation 5's enforcer clause.**

Skeptic-cross-principle's Dangerous Contradiction #4 surfaced a real governance gap: my Recommendation 5 depends on a role the constitution does not establish. Rather than hand-wave the dependency, the gate should either (a) cite an existing CODEOWNERS file or GitHub team that resolves the ambiguity, or (b) note that the enforcer clause is conditional on a follow-up amendment establishing the role. Sequencing matters: shipping the gate with an undefined "maintainer" creates enforcement-by-self-designation. This recommendation closes that loop without expanding the gate's scope.

**Recommendation 12 — Ship Recommendations 1 (PR template + CI lint) and 5 (maintainer review) as a paired bundle, not independently.**

Skeptic-mathematical's Tension 3 and the cross-review convergence on this point: a PR template without a human reviewer degenerates into "did the bot pass" rubber-stamping; a maintainer-review requirement without a template degenerates into "did someone approve" rubber-stamping. Each one alone produces the *appearance* of governance without the substance — which is worse than either the status quo or the full pairing because it consumes political capital for no net gain. The amendment introducing this gate should land both at once or land neither, and the constitution text should explicitly note the pairing as a requirement (not a recommendation) for the gate to be considered enforced.

---

### Position Summary

The gate's structural problem (under-enforced) and its content problem (Criterion 1 over-promises, grandfathered principles complicate precedent) are both real, but the structural problem is dominant. Two cross-reviewers and my own cross-reviews independently converged on the same priority: **fix enforcement first, simplify content second**.

I retain seven of my original ten recommendations (1, 2, 4, 5, 7, 8, 10), withdraw three (3, 6, 9) that the cross-reviews demonstrated were worse than the status quo, and add two new ones (11, 12) addressing dependencies my original review missed. The withdrawals matter as much as the additions — Recommendations 3 and 9 were aggressive simplifications that would have weakened the gate's only load-bearing element, and Recommendation 6 institutionalized a two-tier constitution by footnote rather than through the constitution's own mandated migration discipline.

The remaining disagreement with skeptic-mathematical (their merge of Criteria 1 and 2 vs my keep-and-strengthen) and with skeptic-cross-principle (their collapse of the gate into Principle XI vs my mechanize-the-three-criteria) is structural, not procedural. Both skeptics are arguing the gate is internally redundant and should shrink; I argue the gate's redundancy is less costly than its under-enforcement and the right fix is procedural mechanization. A maintainer reading all three positions should treat this as a binary fork: collapse-and-simplify OR mechanize-and-retain, but not both. My position is the latter. The PR-template + CI-lint + maintainer-review bundle (Recommendations 1, 5, 11, 12) is the operational machinery that makes any three-criterion gate usable; without that machinery, the skeptics' simplification arguments win by default because there is nothing for the redundancy to support.

Net: **mechanize the gate as a three-criterion structure, retain Criterion 1 as the load-bearing artifact-producing requirement, ship enforcement and template together as a non-separable bundle, and resolve the maintainer-role definition as a prerequisite amendment.** Withdraw the recommendations that would have created two-tier constitutional status by footnote or quantitative-but-unfalsifiable thresholds.
