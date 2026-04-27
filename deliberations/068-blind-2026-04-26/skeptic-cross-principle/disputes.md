# skeptic-cross-principle: Disputes (Phase 4)

This phase audits the three Phase 3 revisions (skeptic-mathematical, skeptic-cross-principle, practitioner) for residual cross-principle conflicts. My remit is to test whether the convergence claimed in the revisions actually resolves the inter-principle tensions, or merely re-distributes them. Where convergence is real, I name it. Where the revisions still leave a coordination gap, I file it as a remaining dispute.

---

### Remaining Disputes

#### Dispute 1 — Structural fork (collapse vs. decompose-and-redistribute) is not actually closed

The three revisions claim agreement on a sequenced operation (split → relocate → cross-reference → absorb), but the practitioner explicitly preserved the "tight standalone XVI" preference and stated they would defer to the room rather than retract. Skeptic-mathematical's modified Recommendation 1 says "decompose analytically, but no new principle numbers — most likely outcome, transparency stays inline as the surviving kernel." My own Phase 3 sequenced four operations whose last step ("absorb the transparency fragment into IV; fold pinning into VII as named extension OR keep freestanding") is itself a fork.

The cross-principle hazard: each of the three terminal states (tight-standalone, transparency-only-fragment-folded-into-IV, freestanding-pinning-principle-plus-IV-absorption) interacts differently with V (Observable Deliberation), XV (Plugin Isolation), and XXIV (Safety-Critical Defense-in-Depth). A V-emission requirement landing in a tight-standalone XVI is a different cross-reference graph than the same requirement landing in IV or VII. The synthesizer cannot defer the structural choice to "the room" without choosing which principle the V-emission, XV-coordination, and XXIV-narrowing clauses bind to. Three reviewers converged on "fix the cross-references" without converging on which node owns the edges.

**Disputed against**: practitioner's revised Rec 1 ("not retracting the collapse direction") and skeptic-mathematical's modified Rec 1 ("most likely outcome, transparency stays inline"). Both reviewers privately predict the structural disposition; neither commits to one. The synthesizer must.

#### Dispute 2 — Cross-reference graph is asymmetric across the three revisions

All three revisions endorse a VII↔XVI bidirectional cross-reference. Practitioner's New Rec 13 widens the VII pre-condition list to include capability registry and template registry (citing XI and XXII drift hazards). Skeptic-mathematical's modified Rec 2 plus surviving Rec 8 lands template versioning *inside* VII as a clarification of "same inputs." My own strengthened Rec 6 lands V-emission inside XVI ("pinned values MUST be emitted under V's contract"). My narrowed Rec 7 lands XXIV interaction at the XVI/XXIV boundary, narrowed to synthesis-verdict scope.

This is a star graph centred on VII for some edges (template version, capability registry) and centred on XVI for others (V-emission, XXIV-synthesis). The three revisions never reconcile the centring choice. If template versioning lands in VII and V-emission lands in XVI, then XVI's V-emission clause depends on VII's reproducibility pre-conditions being satisfied — but neither revision states the dependency. A future spec author editing a template breaks VII's reproducibility, which silently invalidates XVI's V-emission as an audit artifact (the emitted pinned values no longer correspond to the run that produced them, because the template changed mid-stream).

**Disputed against**: practitioner New Rec 13 and skeptic-mathematical Rec 8 (both VII-centred), versus my Rec 6 and Rec 7 (both XVI-centred). The revisions agreed each edge should exist; they did not agree which node owns each edge or how the edges compose under template/registry drift.

#### Dispute 3 — Pinning glossary entry in II does not bind to V's emission contract

Skeptic-mathematical's New Rec A and my Rec 5 converge on a glossary entry for "pinning" in Principle II's stable-interface vocabulary. The proposed wording: "a parameter value committed to a run-scoped store, immutable for the duration of the run, with invalidation policy specified in spec 013." This is correct as far as it goes. But II is the stable-interface principle — its glossary defines *what counts as a stable contract*. Without a binding clause stating that pinned parameter values are observable as deliberation output, the glossary entry creates a stable-interface concept that is not itself observable, which is internally inconsistent with V (Observable Deliberation): every phase MUST report progress; an unobservable stable contract violates the spirit of V.

My own strengthened Rec 6 fixes half of this (pinned values MUST be emitted), but the glossary entry in II does not cross-reference Rec 6's emission contract. Practitioner's New Rec 11 (V-emission clause) similarly does not bind to the II glossary entry. Three reviewers added the same artifact (V-emission) and the same concept (pinning glossary) without wiring them together. A reader of v2.3.3 will find "pinning" defined in II without an emission requirement attached, and an emission requirement in XVI (or wherever it lands) without a definition attached.

**Disputed against**: skeptic-mathematical New Rec A, my Rec 5, practitioner New Rec 11 — three independently-correct moves that do not compose unless the synthesizer adds the cross-reference explicitly.

#### Dispute 4 — XXIV scope is conservatively narrowed without confirming the residual coverage

My narrowed Rec 7 restricts the XVI/XXIV interaction to "optimization-driven outputs consumed by synthesis-verdict generation." Skeptic-mathematical's modified Rec 3 dropped the XXIV citation entirely in favour of a generic test-contract clause. Practitioner did not address XXIV at all in the revision (their revision deliberately stayed at the V/VII surface).

The cross-principle hazard: optimization that does NOT feed synthesis verdicts is now under XVI/VII alone, with no defense-in-depth requirement. This is correct under XXIV's literal scope, but it leaves a coverage question unanswered: what happens when an optimization output later becomes a synthesis-verdict input via a downstream spec? XXIV's three-layer defense (schema field, parser validation, contract test) does not retroactively apply to optimization outputs that were authored before they became synthesis-bearing. The narrowing is constitutionally clean but operationally fragile — it relies on spec authors knowing in advance whether their optimization output will eventually feed a synthesis verdict.

**Disputed against**: my own narrowed Rec 7. Skeptic-mathematical and practitioner did not surface this; the dispute is mine to file because the narrowing was my move and the residual gap is my responsibility to name.

---

### Convergence

#### Convergence 1 — VII↔XVI bidirectional cross-reference is non-negotiable

All three revisions independently rate this the highest-leverage edit. Skeptic-mathematical: "the highest-priority remaining recommendation." Practitioner: "adopting their wording: VII gets a back-reference acknowledging XVI as the sole sanctioned exception." Mine: "this cross-reference is mandatory regardless of which structural disposition is chosen." The convergence holds across all three structural forks (tight-standalone, decompose, fold-into-VII). The wording is settled: VII appends "Principle XVI defines the sole sanctioned exception, scoped to LLM-mediated parameter resolution under within-run pinning discipline" and XVI opens with "Subject to Principle VII, …".

#### Convergence 2 — Solver-substitution wording softens to objective-function-as-contract

Practitioner's New Rec 12 and skeptic-mathematical's New Rec B both adopt my Phase 1 framing. Final wording converges on: "Changing solvers MUST NOT change the objective function expression or its parameter semantics. Numerical results may differ across solvers within solver-tolerance bounds; the objective function is the contract, not the solver's output." Three reviewers, identical disposition. No further dispute.

#### Convergence 3 — Removing XVI entirely is off the table

Skeptic-mathematical withdrew Rec 10. Practitioner withdrew Rec 7 (their removal recommendation). I withdrew Rec 10 as a standalone (folded into the decomposition path). The convergence: removing XVI strands specs 012-019 with dangling Principle-XVI pointers (a textbook XII violation), and discards the one operationally crisp gate against re-resolving parameters mid-run. Even a flawed XVI is doing more constitutional work than any of the three Phase 1 reviews credited. XVI stays as a numbered principle in some form.

#### Convergence 4 — Template versioning belongs in VII, not just XVI

Practitioner's New Rec 13 and skeptic-mathematical's surviving Rec 8 both land template versioning inside VII as a clarification of "same inputs." My own Phase 3 noted the practitioner's framing was sharper than the alternatives. Three-way convergence: VII MUST acknowledge that cross-run reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs. This stacks with Convergence 1 (the same VII edit carries both the LLM-mediated-pinning exception and the template-version pre-condition).

#### Convergence 5 — V-emission for pinned parameter values is required

Practitioner's New Rec 11 ("V-emission clause"), my strengthened Rec 6 ("pinned values MUST be emitted under V's contract"), and skeptic-mathematical's Phase 3 implicit endorsement (no objection raised, and their cross-review of me noted the V-emission point was correctly caught) all converge: pinned parameter values must appear in deliberation output (e.g., `optimization/pinned_parameters.yml`) so the user can audit which parameter values their objective function was assembled from. Without observable pinned values, XVI's transparency claim is hollow regardless of how the principle is named or located.

---

### Final Position Statement

#### Non-Negotiables

**Non-Negotiable 1 — VII gets the bilateral cross-reference and the template/registry pre-condition list in the same edit.**

VII MUST be amended to (a) acknowledge XVI as the sole sanctioned exception to deterministic orchestration, scoped to LLM-mediated parameter resolution under within-run pinning, AND (b) enumerate that cross-run reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs. These two amendments are conceptually distinct but operationally inseparable — VII's "non-negotiable" framing stands or falls on both being explicit. Splitting them across two PRs leaves an intermediate state in which VII is internally inconsistent. This is the highest-leverage edit in the entire deliberation; all three reviewers converge on it; the synthesizer must execute it as one atomic amendment.

**Non-Negotiable 2 — V-emission for pinned parameter values, wired to the II glossary entry.**

Pinned parameter values MUST be emitted as deliberation output under V's "every phase MUST report progress" contract. The II glossary entry defining "pinning" MUST cross-reference the V-emission requirement, regardless of which principle hosts the requirement (XVI, VII, or IV under the decomposition path). An unobservable stable contract violates V; a glossary entry without an emission requirement is unfalsifiable; an emission requirement without a definition is uninterpretable. The three artifacts compose into a single coordinated rule, or none of them works.

**Non-Negotiable 3 — XVI stays as a numbered principle in some surviving form.**

Removal is off the table. Specs 012-019 reference Principle XVI by number; removing it without redirecting those references creates the dead-infrastructure pattern XII was written to prevent. Whichever structural disposition the synthesizer chooses, the constitution v2.3.3 MUST contain a Principle XVI (or a clearly-renamed successor reachable by the same constitutional pointer mechanism) that hosts at minimum the within-run pinning discipline and the user-facing transparency claim.

#### Flexibility

**Flexibility 1 — Structural disposition (collapse vs. decompose vs. fold-into-VII) is open.**

I previously argued for decompose-and-redistribute. The practitioner argued for tight-standalone. Skeptic-mathematical argued for analytic decomposition without new principle numbers. All three of us conceded the others' framings have merit. I now treat this as a synthesizer decision rather than a Devil's-Advocate hill — the cross-references in Non-Negotiables 1 and 2 land regardless of which structural form survives, and all three forms preserve XVI's constitutional pointer (Non-Negotiable 3). Pick the form that minimizes downstream churn. My only residual constraint: whichever form is chosen, the V-emission and II-glossary clauses must compose without forward references.

**Flexibility 2 — XXIV scope (synthesis-only vs. broader optimization coverage) is open within bounds.**

My narrowed Rec 7 restricted XXIV to optimization outputs consumed by synthesis-verdict generation. Skeptic-mathematical's modified Rec 3 dropped XXIV entirely in favour of a generic test-contract clause. Either disposition is constitutionally defensible; I prefer the narrowing because it preserves XXIV's scoped authority, but I will not block a synthesizer decision to drop the XXIV citation entirely if the test-contract clause stands on its own. The bound: optimization outputs consumed by synthesis verdicts MUST land under some defense-in-depth requirement, whether explicitly via XXIV or implicitly via a generic test-contract clause that covers the same surface.

**Flexibility 3 — Pinning glossary placement (II vs. inline in XVI/VII) is open.**

I argued for placing the "pinning" definition in II's stable-interface vocabulary. Skeptic-mathematical agreed. Practitioner did not address this directly. The alternative — defining pinning inline at first use inside XVI or VII — is operationally equivalent provided the cross-reference chain to V-emission is preserved (Non-Negotiable 2). I prefer II because it elevates "pinning" to a constitution-wide vocabulary item rather than a XVI-local term, but I will not dispute a synthesizer decision to define inline if the V-emission cross-reference is wired correctly.

---

### Summary

Phase 4 disputes are residuals of the structural fork left open by Phase 3. The convergence is real on five fronts (VII↔XVI cross-reference, solver-substitution softening, no-removal, template versioning in VII, V-emission), but the synthesizer must close the structural choice that all three Phase 3 revisions deliberately left open. My non-negotiables bind on the cross-reference graph and the V/II/XVI tripartite composition; my flexibilities yield on the structural form, XXIV scoping, and glossary placement. The single highest-priority synthesizer move remains the bilateral VII edit identified in Convergence 1 and Non-Negotiable 1 — every other cleanup follows from that one amendment landing correctly.
