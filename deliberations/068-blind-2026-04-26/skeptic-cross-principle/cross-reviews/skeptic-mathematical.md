# Cross-Review: skeptic-cross-principle audits skeptic-mathematical

**Reviewer**: skeptic-cross-principle (Devil's Advocate)
**Target**: skeptic-mathematical's Phase 1 review of Principle XVI
**Posture**: Audit the mathematical critique for conflicts with the rest of the
constitution and with the cross-principle audit produced in parallel.

---

### Dangerous Contradictions

1. **"Move determinism claims to Principle VII" collides with VII's own
   non-negotiable framing.** skeptic-mathematical's Recommendation 2 proposes
   replacing XVI's determinism block with "Once parameters are pinned,
   Principle VII applies unchanged." But VII as written says "Deterministic
   orchestration is non-negotiable" — it has no concept of LLM-mediated
   stochasticity in its body. Dumping the determinism content into VII without
   *also* amending VII to acknowledge LLM-mediated parameter resolution
   produces a worse contradiction than the one being solved: VII's
   "non-negotiable" claim now silently absorbs an exception it never
   articulates. The cross-principle review reaches the opposite conclusion —
   VII needs an *added* back-reference to XVI, not VII *taking over* XVI's
   territory. skeptic-mathematical's recommendation propagates the conflict
   into VII rather than resolving it.

2. **Recommendation 10 ("consider whether XVI earns its keep") would create
   dead infrastructure under Principle XII.** Folding XVI's transparency
   content into IV (Documentation Is the Product), determinism into VII, and
   plugin-explanation into XV would leave specs 012-019 (the cited origin)
   without a single constitutional anchor. Every spec referencing "Principle
   XVI" would become a dangling pointer. Principle XII says "every
   provisioned capability MUST have at least one consumer" and "unattributed
   future-proofing becomes dead code" — a constitution that deletes a
   principle while leaving its consumers wired to it is the inverse of XII:
   stranded consumers with no provisioned capability. This is the textbook
   anti-pattern the constitution forbids.

3. **Recommendation 3 ("replace MUST/MUST NOT with a test contract
   reference") imports a Principle-XXIV pattern that does not generalize.**
   skeptic-mathematical cites XXIII/XXIV's "schema + parser + reproducing
   test" as the model XVI should follow. But XXIV explicitly scopes itself to
   **"synthesis verdict generation" and "provider protocol implementation"**
   — not to optimization parameter pinning. Re-purposing XXIV's pattern for
   XVI either (a) silently expands XXIV's safety-critical scope to include
   optimization (which XXIV does not authorize), or (b) creates a parallel
   "schema + parser + test" doctrine that duplicates XXIV without saying so.
   Both outcomes violate Principle XI (Single Source of Truth): the
   defense-in-depth pattern is owned by XXIV; XVI cannot quietly replicate it.

4. **The "audience for transparency" recommendation contradicts Principle IV.**
   Recommendation 6 proposes replacing the user-facing transparency claim
   with "A spec author who reads the template can explain what is being
   optimized in user-facing documentation." But Principle IV declares
   "specification text IS the implementation" and "SKILL.md MUST be the
   single source of truth for agent behavior." A constitution that says spec
   text *is* the product cannot then say spec text is for spec authors only,
   with end-user transparency outsourced to "the documentation surface."
   That move re-introduces the very gap between artifact and user that IV
   was created to close. skeptic-mathematical's recommendation reads as
   sensible engineering hygiene but is structurally incompatible with IV's
   prose-is-product axiom.

---

### Tensions

1. **Recommendation 1 (split XVI into XVI-A and XVI-B) doubles the
   surface area the cross-principle audit already flagged as
   under-coordinated.** The cross-principle review identified seven
   uncoordinated interactions between XVI and other principles (V, VII, XI,
   XII, XV, XXIV, plus the VIII vocabulary issue). Splitting XVI into two
   principles turns those seven gaps into fourteen. skeptic-mathematical
   notes "a principle that fails should fail cleanly" — but a principle that
   *interacts* needs fewer cleavage planes, not more. The splitting
   recommendation optimizes for post-mortem attribution at the cost of
   forward coordination.

2. **"Specify cache key as `(template_id, template_version, gap_identifier,
   user_answer_hash)`" is a constitutional overreach.** Recommendation 4
   imports an implementation contract into the constitutional layer. This
   collides with III ("constitutions describe contracts, implementations
   evolve") and with VI (Scripts Over Markdown — config belongs in YAML, not
   constitutional prose). The cross-principle review's recommendation #5
   takes the opposite tack: define "pinning" as a *term-of-art* and let the
   cache contract live in spec 013 or a references file. skeptic-mathematical
   wants the constitution to legislate cache schemas; the cross-principle
   review wants the constitution to legislate vocabulary and delegate
   schemas downward. The latter is more consistent with the rest of the
   constitution's level of abstraction.

3. **The "address LLM temperature/seed" recommendation conflicts with VIII.**
   Recommendation 5 asks XVI to document whether parameter resolution sets
   `temperature=0` or `seed=N`. But Principle VIII (Templating Engines Over
   Inference) treats LLM inference as the *last resort*, not as a tunable
   knob to expose in the constitution. Encoding temperature/seed choices in
   constitutional prose elevates an LLM API artifact to first-class
   constitutional vocabulary — which is precisely the inversion VIII
   resists. The cleaner move is the cross-principle review's
   recommendation #4: pick "mechanical" or "deterministic" as the canonical
   term and align with VIII's vocabulary, leaving temperature/seed as
   spec-level details.

4. **Recommendation 7 (acknowledge the pinning trade-off) and
   Recommendation 8 (template versioning) point in different directions.**
   Both are reasonable in isolation. Together they expand XVI from a
   transparency principle into a parameter-lifecycle principle with cache
   policy, version policy, and trade-off policy. The cross-principle review
   reached the parallel observation that XVI is currently doing too much;
   skeptic-mathematical's response is to add *more* policy clauses to XVI
   while also recommending it be split (Recommendation 1) and possibly
   removed (Recommendation 10). This is internally inconsistent: if XVI is
   too crowded to fail cleanly, the answer cannot be "add four more
   sub-clauses about cache, version, freshness, and audience" before
   splitting it.

5. **"Cross-run reproducibility once parameters are pinned is a tautology"
   undersells the principle.** skeptic-mathematical correctly notes that
   mechanical assembly of pinned parameters is trivially deterministic. But
   the constitutional value of stating the tautology is that it forecloses
   a *different* tautology — the implementation drift where re-runs
   silently re-resolve parameters because the cache was never wired in. VII
   does not say this; XVI does. Treating the claim as "trivially true" and
   recommending its removal (implicit in Recommendations 2 and 10) loses the
   forecloser. The cross-principle review's framing — VII and XVI bracket
   the same territory at different abstraction levels — preserves the
   forecloser by demanding mutual cross-references rather than collapse.

---

### Safe Agreements

1. **XVI is doing more than one job.** Both reviews independently reach
   this conclusion. skeptic-mathematical frames it as "two principles
   wearing one hat" (transparency vs determinism); the cross-principle
   review frames it as "vocabulary drift + uncoordinated interactions."
   These are different diagnoses of the same underlying overcrowding. Any
   resolution that reduces XVI's scope is welcome; the disagreement is
   about *which* sub-claims survive and *where* the survivors live.

2. **The plain-language requirement for plugin recommendations is a
   keeper.** Both reviews flag the "Equilibrium quality: 0.87" / "87% of
   agents are at their best possible position" example as the strongest,
   most testable, most uniquely-XVI content in the principle. Whatever
   restructuring happens, this clause should survive — it has no clean
   home elsewhere (IV is about spec-as-product; X is about output
   aesthetics; XV is about isolation, not output content).

3. **The solver/objective separation is a clean architectural invariant.**
   Both reviews note that "changing solvers MUST NOT change what is being
   optimized" maps onto III's backward-compatibility contract and is
   testable via swap-and-assert. The cross-principle review's
   Recommendation 8 ("soften the solver-substitution claim") and
   skeptic-mathematical's silence on this point (it appears in the
   Alignment section) together suggest the *direction* of the claim is
   correct — only the bit-for-bit numerical wording needs softening. This
   is the rare clause both reviews approve of in spirit.

4. **"Pinning" needs to be defined.** Both reviews flag pinning as
   under-specified. The cross-principle review pushes for a glossary entry
   or II-vocabulary integration; skeptic-mathematical pushes for a cache
   contract. Neither review tolerates the current state where "pinned"
   appears in constitutional prose without a definition. A minimum viable
   resolution: define pinning as "a parameter value committed to a
   run-scoped store, immutable for the duration of the run, with
   invalidation policy specified in spec 013." Both reviews would accept
   this; both would reject leaving "pinning" undefined.

---

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/skeptic-mathematical/review.md`
  — the audited review.
- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/skeptic-cross-principle/review.md`
  — the parallel cross-principle review used as the comparison anchor.
- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/CONSTITUTION-v2.3.2-blind.md`
  — Principles IV (lines 96-110), VII (lines 139-152), VIII (lines 154-172),
  XI (lines 277-320), XII (lines 322-344), XV (lines 393-424), XVI
  (lines 426-481), XXIV (lines 681-706) load-bearing for this cross-review.
