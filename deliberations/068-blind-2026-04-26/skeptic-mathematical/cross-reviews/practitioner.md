# Cross-Review of Practitioner — by skeptic-mathematical

**My review**: `<HOME>/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/skeptic-mathematical/review.md`
**Their review**: `<HOME>/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/practitioner/review.md`
**Target**: Constitution v2.3.2-blind, Principle XVI (Mathematical Transparency)

The two reviews converge on the diagnosis — XVI bundles too many concerns
under one heading and the determinism block is the weakest part — but
they diverge on the prescription in ways worth surfacing. Practitioner
treats XVI's content as mostly redistributable into VII, IX, and X.
I treat XVI as bifurcated, with a defensible kernel that earns its keep
once split. The disagreement matters because "fold into existing
principles" and "split into XVI-A / XVI-B" produce different constitutions
even though both reviews agree the current text is incoherent.

### Dangerous Contradictions

1. **Fold-into-others vs split-and-keep is not a stylistic difference.**
   Practitioner's recommendations 5–7 propose migrating the plain-language
   rule into X, the template-documentation rule into spec 013, and the
   pinning rule under VII as a sub-bullet — concluding that "XVI has
   nothing left that doesn't fit better elsewhere" (practitioner review
   §Recommendations, item 7). My recommendation 1 proposes splitting XVI
   into XVI-A (transparency) and XVI-B (parameter-resolution discipline),
   keeping both as standalone principles (skeptic-mathematical review
   §Recommendations, item 1). If the deliberation accepts practitioner's
   path, my split is moot; if it accepts mine, practitioner's "remove
   XVI entirely" option is foreclosed. Both paths cannot coexist — the
   arbiter (or the next round) will have to pick one. Cooperative
   resolution: agree on a *test* — does the parameter-pinning rule have
   substantive content beyond what VII already says? Practitioner argues
   yes implicitly (recommendation 1 keeps a 4–6 line principle around
   it), I argue yes explicitly (XVI-B). That's actually agreement
   masked as disagreement: neither of us thinks pinning collapses fully
   into VII without losing something. The real divergence is whether
   that residue deserves a numbered principle or a sub-bullet.

2. **Practitioner's recommendation 3 and my recommendation 4 disagree
   on whether the VII–XVI tension is resolvable in prose alone.**
   Practitioner frames the tension as a choice: either (a) require
   pinned parameters to be persisted and replayable across runs, or
   (b) explicitly carve optimization runs out of VII's promise
   (practitioner review §Recommendations, item 3). My recommendation 4
   instead defines a cache key
   `(template_id, template_version, gap_identifier, user_answer_hash)`
   and treats reproducibility as a derived property of the cache
   contract. These prescriptions could conflict: practitioner's path
   (b) — carving optimization out of VII — would render my cache-key
   spec partially redundant (cross-run reproducibility is no longer
   promised, so the cache-key just bounds within-run stability). If
   the constitution adopts (b), my P2 work on cache semantics shrinks.
   This needs explicit reconciliation — we should not let both
   recommendations land independently and discover the conflict
   downstream.

3. **"Aspirational without verification path" framing differs in what
   counts as a fix.** Practitioner's missed-opportunity #5 says XVI
   "demands... vibes" and points to XXIV, XXVI, and XXII as models for
   verifiable principles (practitioner review §Missed Opportunities,
   item 5). My recommendation 3 proposes a specific test contract
   reference (`tests/test_parameter_pinning.py::test_no_within_run_drift`).
   These look compatible but aren't quite — practitioner's framing
   suggests *removing* the prose prohibitions, mine suggests *keeping*
   them but anchoring them to a concrete test file. If practitioner's
   recommendation 1 (rewrite XVI as 4–6 lines focused on pinning) is
   adopted, the resulting principle still contains MUST/MUST NOT prose;
   if my recommendation 3 is adopted on top, that prose now points at
   a test file. Compatible — but only if the order is "split first,
   anchor second." The wrong sequencing produces a tightened-but-still-
   unverifiable rump principle.

### Tensions

1. **Audience question.** My missed-opportunity #8 and recommendation 6
   demand we define *which* user "understands what they are optimizing"
   — end user vs spec author. Practitioner's off-base assumption #2
   independently flags that "within-run determinism" is implementation
   language leaking into a user-promise framing. We're hitting the same
   nerve from two angles: practitioner says XVI mixes implementation
   into user-facing promises; I say XVI fails to specify which user
   the promise is for. A unified fix would be useful — the principle
   needs both a clean audience definition *and* a separation of
   user-facing claims from implementation invariants.

2. **The 3-stage pipeline as content category.** Practitioner says
   it "reads like spec excerpt, not constitution" and should move to
   spec 013 (practitioner review §Missed Opportunities, item 1). I
   give the 3-stage description partial credit ("structural honesty
   is a strength — many 'deterministic pipeline' claims hand-wave
   past LLM stages"; my Alignment §4). Both can be true: the
   acknowledgment of stage-2 stochasticity is genuinely valuable, but
   numbering the stages and describing them in detail is doc-page
   content. A compromise: keep one sentence — "stage 2 is stochastic;
   stages 1 and 3 are mechanical" — and offload the rest. This isn't
   a contradiction so much as a calibration question.

3. **Recommendation priority for cache-versioning vs template-
   versioning.** My recommendation 8 says template version MUST be
   part of the parameter pin; practitioner's off-base assumption #1
   notes the principle stops matching code if specs evolve. We agree
   the template-versioning gap is real, but practitioner does not
   carry it into a recommendation, while I do. If practitioner's
   "remove XVI entirely" path wins, my recommendation 8 has no home
   to land in. If practitioner's "rewrite as 4–6 lines" path wins,
   mine becomes a one-sentence addition. Compatible if we agree the
   versioning concern survives any restructuring.

4. **Solver-vs-objective separation: principle vs sub-bullet.**
   Practitioner's recommendation 7 sketches moving the solver-swap
   invariant under Principle II ("Stable Interfaces"). My alignment
   §2 treats it as a coherent architectural invariant on its own.
   Both are defensible. The tension is whether II's "stable
   interfaces" framing — currently focused on structural markers,
   template variables, dispatch table — naturally accommodates
   "the objective function is the contract surface." Worth deciding
   in round 2: II's text would need a sub-bullet, and the question
   is whether that bullet reads naturally there or feels grafted on.

5. **Plain-language rule: rule vs CI hook.** Practitioner's
   recommendation 9 proposes a linter check scanning
   `templates/optimization/*.yml` for `description:` and
   `plain_language:` fields; my recommendation 6 reframes the
   transparency claim around audience but does not propose a linter.
   Compatible and complementary — practitioner's CI hook would
   operationalize whatever audience definition I land on. We should
   bundle them.

### Safe Agreements

1. **The clarification block is a tell.** Practitioner's
   missed-opportunity #3 ("a principle that needs a clarification
   block titled 'determinism scope' is a principle that did not land
   cleanly the first time") and my executive summary ("the within-run /
   cross-run distinction is the cleverest move in the text, but it is
   also where the incoherence concentrates") agree the clarification
   block is a symptom, not a feature. Whatever the deliberation
   chooses, the next version of XVI should not need a footnote to
   explain itself.

2. **The plain-language requirement is the strongest part.**
   Practitioner's alignment §3 calls it "a concrete, testable UX
   requirement"; my alignment §1 says "this part of XVI earns its
   keep." Both reviews independently identified the same kernel of
   value. If anything is preserved unchanged from current XVI, this
   should be it — and both reviews are open to relocating it (under
   X for practitioner, kept anywhere for me) as long as the rule
   itself survives.

3. **VII-XVI overlap is real and unresolved.** Practitioner's
   missed-opportunity #6 ("overlap with Principle VII is real, not
   just feared") and my recommendation 2 ("move determinism claims
   to Principle VII or explicitly defer to it") agree the current
   text creates a single-source-of-truth violation against XI. The
   review-level disagreement is over the fix (fold vs cross-reference),
   but the diagnosis is shared. Whatever solution lands, it must
   resolve the overlap rather than paper over it.

4. **No enforcement mechanism is a constitutional weakness, not just
   an ergonomic one.** Practitioner's missed-opportunity #5 and my
   recommendation 3 converge on the same point: principles that
   demand behavior without test contracts (XXIV, XXVI, XXII as
   counterexamples) become aspirational. XVI in its current form
   joins that anti-pattern. Both reviews want a verification anchor;
   the disagreement is only about exact wording.

---

**Resolution path I'd propose for round 2**: agree the clarification
block must go and the VII overlap must resolve. Defer the
"fold-into-others vs split-and-keep" question to a single explicit
binary choice put to the deliberation, framed as: *does the parameter-
pinning rule contain enough novel content to deserve its own principle
number?* If yes, my XVI-A/XVI-B split. If no, practitioner's fold-into-
VII path. Either path absorbs most of the safe agreements; the
disagreement is genuinely about constitutional density, not about
whether the current XVI is broken.
