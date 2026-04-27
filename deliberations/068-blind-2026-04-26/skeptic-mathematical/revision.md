# Skeptic-Mathematical Revision — Phase 3, Iteration 1

**Persona**: skeptic-mathematical (Devil's Advocate)
**Target**: Constitution v2.3.2-blind, Principle XVI
**Phase**: 3 (revision of Phase 1 review in light of cross-reviews)

---

### Recommendation Dispositions

#### Recommendation 1: [P1] Split XVI into XVI-A and XVI-B

- **Original position**: Decompose XVI into XVI-A (Mathematical Transparency) and XVI-B (Parameter Resolution Discipline) as standalone numbered principles, so each fails cleanly.
- **Disposition**: Modified.
- **Explanation**: Skeptic-cross-principle's first Tension landed: "splitting XVI into two principles turns those seven uncoordinated interactions into fourteen." Practitioner reached the same point from the developer-ergonomics side ("more principles" = cross-reference debt, principle-numbering churn). Both reviewers, including my own cross-review of skeptic-cross-principle, converged on a sequenced operation rather than a binary fork: *first* decompose XVI's content along the transparency / determinism / pinning axis, *then* evaluate each fragment for absorption. The modified recommendation: keep the decomposition as an analytic move, but the output is not necessarily two new numbered principles. Most likely outcome — transparency stays inline as the surviving kernel of XVI; determinism content cross-references VII (per Recommendation 2); pinning discipline collapses to one operational sentence backed by a test contract. No new principle numbers issued. This costs me the clean-failure attribution argument in my original framing, but the cross-reference-debt cost is real and I underestimated it.

#### Recommendation 2: [P1] Move determinism claims to Principle VII or explicitly defer to it

- **Original position**: Replace XVI's determinism block with a single sentence pointing at VII and a `references/parameter-resolution.md` file.
- **Disposition**: Modified.
- **Explanation**: Two cross-review hits, both correct. Skeptic-cross-principle: VII as written says "Deterministic orchestration is non-negotiable" — dumping LLM-mediated stochasticity into VII without amending VII propagates the conflict rather than resolving it. Practitioner: pointing at a `references/` doc that does not exist degrades the constitutional weight of the prohibition. Both critiques converge on the same fix: the move must be *bilateral* (VII gains an explicit acknowledgment of LLM-mediated parameter resolution as the documented exception; XVI gains an explicit cross-reference back to VII), and the prose must remain inline rather than redirected to a non-existent reference doc. The modified recommendation: amend VII to add a single sentence — "VII applies under the parameter-pinning discipline of XVI; LLM-mediated stages are scoped via XVI's pinning contract" — and amend XVI to defer to VII for what reproducibility *means*, while keeping XVI's pinning sentence inline. No `references/` redirect.

#### Recommendation 3: [P1] Replace MUST/MUST NOT claims with a test contract reference

- **Original position**: "Parameter resolution discipline is enforced by `tests/test_parameter_pinning.py::test_no_within_run_drift`."
- **Disposition**: Modified.
- **Explanation**: Skeptic-cross-principle's Dangerous Contradiction #3 is sharp: XXIV's "schema + parser + reproducing test" pattern is *scoped* to synthesis verdicts and provider protocols. Re-purposing it for optimization parameter pinning silently expands XXIV's safety-critical scope or creates a parallel doctrine — both bad. Practitioner's Tension #4 adds: don't reference tests that don't exist yet. The modified recommendation: keep the *intent* (replace prose-only prohibition with a verification anchor) but drop the XXIV pattern citation. Replace with a generic clause: "Parameter resolution discipline MUST be enforced by a test that demonstrably fails if a future PR re-resolves parameters mid-deliberation. Until that test exists, this principle is aspirational; first PR adding the test removes the aspirational caveat." This is an honest framing — it acknowledges the current unenforceability without falsely citing patterns from elsewhere or pointing at fictional test files.

#### Recommendation 4: [P2] Specify cache key and invalidation policy

- **Original position**: Define cache key as `(template_id, template_version, gap_identifier, user_answer_hash)` with documented invalidation triggers in the constitution.
- **Disposition**: Withdrawn.
- **Explanation**: Skeptic-cross-principle's Tension #2 is a clean win for them and a clean withdrawal for me. The cache-key tuple is implementation contract, not constitutional content; embedding it in constitutional prose violates III ("constitutions describe contracts, implementations evolve") and VI ("config belongs in YAML, not constitutional prose"). Their counterproposal — define "pinning" as a term-of-art and let the cache contract live in spec 013 — is consistent with the constitution's level of abstraction and resolves the same underlying defect (non-falsifiability of "pinning" as a bare term). Practitioner's parallel concern about operational simplicity reinforces this: a PR author cannot verify a four-tuple cache key in five minutes of code review, but they can verify "called at most once per parameter per run." The constitutional prose should hold the operational rule; the cache contract belongs downstream. I withdraw the four-tuple specification entirely.

#### Recommendation 5: [P2] Address LLM temperature/seed instead of relying solely on pinning

- **Original position**: Constitution should document whether parameter resolution sets `temperature=0` or passes a seed.
- **Disposition**: Withdrawn.
- **Explanation**: Skeptic-cross-principle's Tension #3 caught a real category error in my recommendation: encoding LLM API artifacts (temperature, seed) in constitutional prose elevates implementation knobs to first-class constitutional vocabulary, which is precisely the inversion VIII (Templating Engines Over Inference) resists. VIII treats LLM inference as last resort; my recommendation would have re-promoted LLM API parameters to constitutional concepts. The correct move is to align XVI's vocabulary with VIII (their Recommendation #4) and let temperature/seed live in spec-level provider configuration. Withdrawn without modification — the original recommendation was an unforced error.

#### Recommendation 6: [P2] Define the audience for "mathematical transparency"

- **Original position**: Replace "user understands what they are optimizing" with "spec author can explain it; end-user transparency is IV's responsibility."
- **Disposition**: Modified.
- **Explanation**: Both cross-reviewers landed strikes here, in different directions. Skeptic-cross-principle's Dangerous Contradiction #4: outsourcing end-user transparency to IV contradicts IV's "specification text IS the implementation" axiom — IV is about prose-as-product, not about runtime output legibility. Practitioner's Dangerous Contradiction #3: redefining the audience as "spec author" silently revokes a user-facing promise; nothing else in the constitution then requires user-facing optimization output to be intelligible, and a developer could legitimately ship "Equilibrium quality: 0.87" with no gloss and point at my redefinition for cover. Both critiques converge: the original recommendation severed the user-facing promise that the plain-language clause depends on. The modified recommendation: keep the audience as the end user (do not narrow to spec author), but distinguish *template legibility* (spec-author concern, addressed by template documentation per the existing XVI clause) from *runtime output legibility* (end-user concern, addressed by the plain-language requirement which both cross-reviewers and I agreed is XVI's strongest clause). Two audiences, two surfaces, both retained. The original "narrow to spec author" framing is withdrawn.

#### Recommendation 7: [P2] Add a clause acknowledging the pinning trade-off

- **Original position**: Add a paragraph stating that pinning trades freshness for reproducibility, with cache-clearing as escape hatch.
- **Disposition**: Withdrawn.
- **Explanation**: Practitioner's Tension #3 names this correctly: trade-off discussion is feature-spec content, not constitutional content. Constitutions encode invariants; the rationale for *which* invariant was chosen belongs in the spec that motivated the principle (spec 013 here). Skeptic-cross-principle's overall framing — XVI is overcrowded — also argues against adding more clauses. My own cross-review of skeptic-cross-principle flagged that Recommendations 7 and 8 together expand XVI from a transparency principle into a parameter-lifecycle principle, which is internally inconsistent with my own Recommendation 1 (split/decrowd). Withdrawing Recommendation 7 resolves that internal inconsistency. The trade-off discussion belongs in spec 013's design notes, not in XVI's prose.

#### Recommendation 8: [P2] Add template-versioning to the cross-run reproducibility claim

- **Original position**: "Template version MUST be part of the parameter pin; cross-run reproducibility is scoped to (config, template_version)."
- **Disposition**: Surviving (with scope expansion).
- **Explanation**: Both cross-reviewers acknowledged this as a real gap I caught. Practitioner explicitly: "skeptic identifies that cross-run reproducibility silently breaks when templates are edited. This is real and my review missed it." Practitioner also raised a sharpening: the template-versioning fix is broader than XVI — VII has the same problem ("same config produces same output *only if templates are unchanged*"). Skeptic-cross-principle did not contest the template-versioning content. The recommendation survives with scope expansion: template versioning belongs in VII as a clarification of what "same inputs" means (templates are inputs to the deterministic substitution), with XVI cross-referencing VII's expanded clause. This stacks with the modified Recommendation 2 (bilateral cross-reference between VII and XVI) — VII gains both the LLM-mediated-pinning exception *and* the template-version clarification in the same edit.

#### Recommendation 9: [P3] Reconcile the plugin-explanation clause with Principle XV

- **Original position**: Add a one-line cross-reference distinguishing XVI's clause (plugin output content) from XV's (plugin isolation from core state).
- **Disposition**: Surviving.
- **Explanation**: No cross-reviewer challenged this. Both cross-reviewers agreed the plain-language plugin clause is XVI's strongest content (Safe Agreement). XXVII already established the pattern of explicit cross-principle coordination between XV-territory clauses ("Coordination with Principle XV"); the same hygiene should apply to XVI's plugin-output clause. Low-risk, low-cost edit; survives unchanged.

#### Recommendation 10: [P3] Consider whether XVI earns its keep at all

- **Original position**: Migrate durable claims into IV/X/VII; remove XVI as standalone if nothing remains uniquely its own.
- **Disposition**: Withdrawn.
- **Explanation**: Two converging Dangerous Contradictions kill this. Practitioner's #1: "remove XVI entirely" discards the *one* operationally crisp gate in the constitution — the clarification block sentence catches "developer adds a second LLM call to the gap-fill code path," which VII/IV/X do not catch. Skeptic-cross-principle's #2: removing XVI while specs 012-019 still reference "Principle XVI" creates the textbook XII anti-pattern (consumers stranded with no provisioned capability). Both critiques are correct and decisive. The plain-language clause has no clean home (Safe Agreement across all three reviewers); the parameter-pinning clause has no clean home (my own Phase 2 cross-review of practitioner conceded this); and removing XVI breaks downstream specs. Withdrawn entirely. XVI stays as a numbered principle.

---

### New Recommendations

#### New Recommendation A: Define "pinning" as a term-of-art in II's stable-interface vocabulary

- **Trigger**: Skeptic-cross-principle's Recommendation #5 (terminological fix in II) and my own Phase 2 cross-review acknowledgement that glossary-without-test and test-without-glossary are both incomplete; both moves together produce an enforceable definition.
- **Content**: Add to II: "Pinning — a parameter value committed to a run-scoped store, immutable for the duration of the run, with invalidation policy defined in spec 013." This gives "pinning" a constitutional home so XVI can reference it without re-defining it.
- **Rationale**: Resolves the non-falsifiability of bare "pinning" without importing the cache-contract overreach I withdrew in Recommendation 4.

#### New Recommendation B: Soften the solver-substitution claim from numerical to semantic

- **Trigger**: My own Phase 2 cross-review of skeptic-cross-principle conceded that their conservative reading is right ("MUST NOT change the objective function or its parameter semantics" beats "MUST NOT change what is being optimized"). Worth surfacing here as a New Recommendation since it did not exist in my Phase 1 Alignment-only treatment.
- **Content**: Replace XVI's "Changing solvers MUST NOT change what is being optimized" with "Changing solvers MUST NOT change the objective function expression or its parameter semantics. Numerical results may differ across solvers; the objective function is the contract, not the solver's output."
- **Rationale**: Closes the ambiguity at zero semantic cost. A reader currently could interpret the existing wording as a promise of numerical-result equivalence across solvers, which is technically false (floating-point differences are inevitable). The semantic-vs-numerical distinction makes the contract testable (swap solvers, assert identical objective expression) without overpromising.

---

### Position Summary

Of ten original recommendations: four withdrawn (4, 5, 7, 10), four modified (1, 2, 3, 6), and two surviving (8, 9). Two new recommendations added (A: pinning glossary entry; B: solver-substitution wording softening). The withdrawal rate is high because my Phase 1 review made two systematic errors that both cross-reviewers caught: (a) over-reaching by importing implementation contracts into constitutional prose (cache key tuple, LLM temperature/seed), and (b) under-weighting the cost of the proposed cures relative to the disease (removing XVI strands downstream specs; narrowing transparency audience revokes a user-facing promise).

The most significant change is the disposition of Recommendation 10. My Phase 1 framing treated XVI as potentially redundant constitutional bloat. The two Dangerous Contradictions identified in cross-review — practitioner's "removing XVI loses the one enforceable gate against the most likely real-world regression" and skeptic-cross-principle's "removing XVI strands specs 012-019 with dangling Principle-XVI pointers" — converge on the same point: even a flawed XVI is doing more constitutional work than I credited. The withdrawal of Recommendation 10 forces the rest of my recommendations to operate in a *repair* mode rather than a *replace* mode, which is also why Recommendation 1's "split into XVI-A/XVI-B" had to be modified to "decompose analytically, but no new principle numbers."

The highest-priority remaining recommendation is the modified Recommendation 2 (bilateral cross-reference between VII and XVI), now strengthened by the surviving Recommendation 8 (template versioning) which lands inside VII as part of the same edit. This is the highest-leverage move because it resolves the single-source-of-truth violation against XI that all three reviewers flagged independently, while also closing the silent-failure hole that practitioner correctly noted I had under-scoped — VII as written silently breaks the moment any spec author edits a template, regardless of XVI's pinning discipline. One bilateral edit fixes both defects; everything else is downstream cleanup.
