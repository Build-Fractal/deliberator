# Skeptic-Mathematical Review — Principle XVI (Mathematical Transparency)

**Persona**: skeptic-mathematical (Devil's Advocate)
**Target**: Constitution v2.3.2-blind, Principle XVI
**Posture**: Argue the strongest case that XVI is logically incoherent or unenforceable as written.

---

### Executive Summary

Principle XVI tries to do three jobs in one body of text: (a) ground a moral
claim ("users must understand what is being optimized"), (b) describe a
3-stage pipeline whose deterministic properties differ across stages, and
(c) bind the architecture to a discipline of *parameter pinning*. The
moral claim is uncontroversial. The 3-stage description is plausible.
What does not survive scrutiny is the third job: the principle's
clarification block uses the language of guarantees ("MUST NOT," "is
prohibited") to constrain behavior that the principle text itself cannot
enforce — and that, by the principle's own admission, depends on a
caching layer in code that is not part of the principle. The principle
is conflating an architectural promise with an implementation discipline,
and labeling the result a "principle."

The within-run / cross-run distinction is the cleverest move in the text,
but it is also where the incoherence concentrates. "Within-run
determinism for the assembled objective function" is trivially true once
parameters are pinned — that is just the definition of mechanical
assembly. "Cross-run reproducibility once parameters are pinned"
depends entirely on whether parameters are *re-pinned* on each run,
which the principle leaves to "discipline." A principle whose
enforceability reduces to "don't re-call the LLM" is not an architectural
guarantee; it is a code review checklist masquerading as constitutional
text.

The strongest version of the skeptical case: XVI as written is two
principles wearing one hat. The defensible kernel — "objective functions
must be parameterized by user-provided values, not opaque model
internals, and every template must document its mathematical form in
plain language" — is a clean transparency claim. The determinism
clarification block is a separate (and weaker) reproducibility claim
that should either be moved to Principle VII (Reproducibility Over
Inconsistency, which already governs this territory) or honestly labeled
as aspirational discipline. Bundling them under one heading hides
accountability: when reproducibility fails, the principle as written
gives no clean way to say which sub-claim was violated.

---

### Alignment

- The plain-language requirement for plugin recommendations
  ("Equilibrium quality: 0.87" insufficient; "87% of agents are at their
  best possible position…" required) is a clean, testable contract. A
  reviewer can grep plugin output and check for an explanation alongside
  every numeric score. This part of XVI earns its keep.
- The solver-vs-objective separation ("Changing solvers MUST NOT change
  what is being optimized") is a coherent architectural invariant — the
  objective function is the contract; the solver is the implementation.
  This is enforceable via tests that swap solvers and assert identical
  objective values.
- The claim that "the LLM does not generate the objective function — it
  translates gap identifiers into natural-language questions and the
  user's answers into parameter values" is a clean role boundary. If
  upheld in code, it bounds the LLM's blast radius to parameter values,
  not mathematical structure.
- The 3-stage pipeline description correctly identifies which stages can
  be deterministic (stages 1 and 3 are mechanical) and which cannot
  (stage 2 is an LLM call). This structural honesty is a strength —
  many "deterministic pipeline" claims hand-wave past LLM stages.
- The requirement that every objective-function template documents its
  mathematical form, parameters, and parameter meanings in plain language
  is a concrete, auditable artifact. A spec reviewer can demand this
  documentation per template.
- The cross-reference to Principle VII ("Once parameters are pinned, the
  optimization is reproducible (Principle VII applies)") at least
  acknowledges that XVI is borrowing reproducibility semantics from
  elsewhere rather than redefining them.

---

### Missed Opportunities

- **The clarification block hides which sub-claim is the principle.**
  The body of XVI mixes (a) a transparency claim ("users must understand
  what is being optimized"), (b) a determinism claim about pipeline
  stages, and (c) a discipline claim about parameter pinning. A
  principle with three independent claims under one heading cannot fail
  cleanly — when something breaks, the post-mortem cannot point to
  "Principle XVI was violated" without ambiguity. Split or label.
- **"Pinned per deliberation run" is asserted but not bounded.**
  Where is the pin stored? When is it invalidated? The principle says
  "cached values from the first resolution are reused" but does not
  define cache lifetime, key, or invalidation policy. A test that
  passes on Monday because the cache is warm may fail on Tuesday because
  the cache was evicted, with no constitutional violation having
  occurred. This is the canonical pattern of a principle whose claims
  rely on unspecified infrastructure.
- **"Within-run variance is prohibited" is unenforceable as written.**
  The principle text alone cannot prohibit within-run variance; only
  the parameter-resolution code can. If a future PR re-resolves
  parameters mid-deliberation (the very scenario the clarification block
  warns against), what mechanism in the constitution catches it? A
  reviewer who hasn't read this principle would not know to look. The
  prohibition needs a corresponding test contract or it is hortatory.
- **Cross-run reproducibility "once parameters are pinned" is a
  tautology.** Mechanical assembly of the same parameters always
  produces the same output — that is what "mechanical" means. The
  non-trivial claim would be that *running the deliberation again*
  produces the same parameters, but the principle explicitly disclaims
  this ("Cross-run variance is acceptable"). So the cross-run
  reproducibility claim collapses to "if you reuse the parameter file,
  you get the same answer," which is true of any function on any input.
- **The principle uses `MUST` and `MUST NOT` for behavior the principle
  cannot itself enforce.** "A future PR that re-resolves parameters
  mid-deliberation… violates this principle" — but the constitution does
  not run; it does not have a test harness; it does not block PRs. The
  prohibition lives in code review discipline. Per Principle XI's own
  spirit (single source of truth), the enforcement should be in a test
  or linter, not restated in constitutional prose.
- **"Stochastic at the LLM call" handwaves over temperature and
  seeding.** Stage 2 is described as stochastic, but modern LLM APIs
  expose temperature and seed parameters that can make a call
  near-deterministic for fixed inputs. The principle does not say
  whether parameter resolution should set temperature=0 or pass a seed.
  If the answer is "we accept stochasticity and pin the result," that
  is a defensible choice — but the principle does not articulate why
  pinning is preferable to just calling with temperature=0 every time.
- **The principle does not address what happens when the user changes
  the natural-language question between runs.** If stage 2 turns gap
  identifiers into "natural-language questions" and the user's answers
  fill parameters, then the same gap could yield different parameters
  if the question wording drifts, even with cached values. The
  principle is silent on whether the cache key includes the prompt
  template version, the LLM version, or just the gap identifier.
- **"Mathematical Transparency" promises understanding without defining
  the audience.** A user who reads the template "understands what they
  are optimizing" — but which user? The end user invoking conversus,
  or the spec author who wrote the template? If it is the latter, the
  principle is a documentation rule for spec authors, not a transparency
  guarantee for users. If the former, the principle owes us evidence
  that templates are written in language an end user can parse.
- **No interaction clause with Principle VII or XV.** Principle VII
  governs reproducibility; XVI restates a piece of it for the math
  pipeline. Principle XV governs plugin isolation; XVI's last clause
  ("Plugin recommendations… MUST include plain-language explanations")
  sits inside the same territory. A constitution where multiple
  principles regulate overlapping behavior without explicit coordination
  invites contradictory rulings.

---

### Off-Base Assumptions

- **Assumption: pinning is the right primitive for handling LLM
  stochasticity.** The principle treats parameter pinning as the
  obvious solution. But pinning has its own failure mode: a *bad* first
  resolution gets locked in, and the system becomes reproducibly wrong
  rather than stochastically right-on-average. The principle does not
  acknowledge this trade-off. A user who runs the deliberation once,
  gets a confused gap-fill, and then re-runs expecting "pinned"
  reproducibility is now permanently anchored to bad parameters until
  the cache is cleared. Whether this is the right default is a design
  question the principle quietly closes by fiat.
- **Assumption: "the math template is pre-defined at design time" is
  invariant.** The principle leans on this to bound what the LLM does.
  But specs evolve; templates get edited; new templates are added. If
  a template is edited between two runs, the "mechanical assembly"
  guarantee no longer applies across those runs. The principle does
  not address template versioning at all, despite making cross-run
  claims that depend on template stability.
- **Assumption: users want reproducibility more than they want
  freshness.** The whole pinning architecture trades freshness (re-ask
  the LLM, possibly get a better answer) for reproducibility (always
  get the same answer). Some users may prefer the opposite — and the
  principle does not expose this as a configuration choice or even
  acknowledge that it is a choice.
- **Assumption: "the user understands what is being optimized" is
  achievable through documentation alone.** Mathematical optimization
  involves emergent behavior — local minima, sensitivity to
  initialization, parameter interactions. A user who reads the template
  may understand the *shape* of what is being optimized but not what
  the optimizer will actually return on their specific inputs. The
  principle conflates "transparency of objective" with "predictability
  of outcome." These are not the same thing.

---

### Actionable Recommendations

1. **[P1] Split XVI into two principles.**
   - **Current state**: One principle bundles transparency, pipeline
     determinism, and parameter-pinning discipline.
   - **Proposed change**: Create XVI-A "Mathematical Transparency"
     (objective functions parameterized by user values; plain-language
     explanations; solver/objective separation) and XVI-B "Parameter
     Resolution Discipline" (pinning, within-run prohibition,
     cross-run semantics).
   - **Rationale**: A principle that fails should fail cleanly. Two
     claims under one heading prevent precise post-mortem attribution.
   - **Risk if ignored**: Future violations cannot be cited
     unambiguously; "Principle XVI was violated" remains debatable
     forever.

2. **[P1] Move determinism claims to Principle VII or explicitly
   defer to it.**
   - **Current state**: XVI restates reproducibility semantics that
     Principle VII already owns ("Reproducibility Over Inconsistency").
   - **Proposed change**: Replace XVI's determinism block with a single
     sentence: "Once parameters are pinned, Principle VII applies
     unchanged. Pinning policy is defined in
     `references/parameter-resolution.md`."
   - **Rationale**: Single-source-of-truth (Principle XI) applies to
     constitutional prose itself. Restating reproducibility in two
     places creates the exact drift Principle XI prohibits.
   - **Risk if ignored**: VII and XVI can drift; future amendments to
     one will not propagate.

3. **[P1] Replace `MUST`/`MUST NOT` claims about pinning with a test
   contract reference.**
   - **Current state**: "Within-run variance is prohibited" / "A
     future PR that re-resolves parameters mid-deliberation… violates
     this principle."
   - **Proposed change**: "Parameter resolution discipline is enforced
     by `tests/test_parameter_pinning.py::test_no_within_run_drift`
     (see Principle XXIV for safety-critical test requirements)."
   - **Rationale**: Principles XXIII and XXIV already model the pattern
     of "schema + parser + reproducing test" for enforceable contracts.
     XVI should follow the same pattern instead of using prose
     prohibitions.
   - **Risk if ignored**: The prohibition remains aspirational; the
     first PR that violates it has no automated tripwire.

4. **[P2] Specify cache key and invalidation policy for pinned
   parameters.**
   - **Current state**: "Cached values from the first resolution are
     reused." No cache key, lifetime, or invalidation policy.
   - **Proposed change**: Define cache key as
     `(template_id, template_version, gap_identifier, user_answer_hash)`
     and document invalidation triggers (template edit, schema change,
     user override).
   - **Rationale**: Without a cache contract, "pinning" is a
     non-falsifiable claim — the same code can be pinning or not
     depending on cache state at run time.
   - **Risk if ignored**: Users will report non-reproducibility bugs
     that no one can adjudicate because the contract is undefined.

5. **[P2] Address LLM temperature/seed instead of relying solely on
   pinning.**
   - **Current state**: Stage 2 is described as "stochastic at the LLM
     call" with no discussion of whether stochasticity is necessary.
   - **Proposed change**: Document the choice — either "we set
     temperature=0 and seed=N to minimize stage-2 variance, *and* we
     pin the result for cross-run determinism," or "we accept
     stochasticity because [reason]; pinning is the chosen mitigation."
   - **Rationale**: A principle that does not acknowledge alternatives
     it considered and rejected is hiding its design space.
   - **Risk if ignored**: Future maintainers re-derive the temperature
     question and may make incompatible choices.

6. **[P2] Define the audience for "mathematical transparency."**
   - **Current state**: "A user who reads the template understands what
     they are optimizing." The "user" is unspecified.
   - **Proposed change**: Replace with "A spec author who reads the
     template can explain what is being optimized in user-facing
     documentation. End-user transparency is the responsibility of
     the documentation surface (Principle IV)."
   - **Rationale**: Mathematical templates are not end-user-readable
     by default. Pretending otherwise is the kind of conflation that
     erodes the constitution's credibility.
   - **Risk if ignored**: The principle's transparency claim cannot
     be tested because the audience is undefined.

7. **[P2] Add a clause acknowledging the pinning trade-off.**
   - **Current state**: Principle treats pinning as obviously correct.
   - **Proposed change**: Add a paragraph: "Pinning trades freshness
     for reproducibility. A bad first resolution becomes reproducibly
     wrong rather than stochastically right. Cache invalidation
     (recommendation 4) is the escape hatch; users encountering
     persistent bad parameters MUST be able to clear the pin."
   - **Rationale**: A constitutional principle that ignores its own
     trade-off space is brittle; the next time the trade-off bites,
     someone will propose removing the principle entirely.
   - **Risk if ignored**: First production incident around bad pinned
     parameters will become a referendum on the principle.

8. **[P2] Add template-versioning to the cross-run reproducibility
   claim.**
   - **Current state**: "Mechanical assembly: deterministic — given a
     template and a fully-pinned parameter set, the resulting
     objective function is identical bit-for-bit on every assembly."
     But what if the template was edited between assemblies?
   - **Proposed change**: "...given a template at version V and a
     fully-pinned parameter set, the resulting objective function is
     identical bit-for-bit on every assembly. Template version MUST
     be part of the parameter pin; cross-run reproducibility is
     scoped to (config, template_version)."
   - **Rationale**: Without versioning, the cross-run claim fails
     silently the moment any spec author edits a template.
   - **Risk if ignored**: Reproducibility breaks invisibly during
     ordinary spec evolution.

9. **[P3] Reconcile the plugin-explanation clause with Principle XV.**
   - **Current state**: XVI's plugin-recommendation clause overlaps
     with XV's plugin-isolation clause without explicit coordination.
   - **Proposed change**: Add a one-line cross-reference: "This clause
     constrains plugin *output content*; Principle XV constrains
     plugin *isolation from core state*. The two are independent."
   - **Rationale**: Principle XXVII added similar coordination
     language with XV. The same hygiene should apply here.
   - **Risk if ignored**: Future plugin authors will see overlapping
     constraints and ask which governs.

10. **[P3] Consider whether XVI earns its keep at all.**
    - **Current state**: XVI's strongest claims (transparency,
      solver/objective separation, plain-language explanations) could
      live as extensions to Principles IV (Documentation Is the
      Product) and X (Zen of Python Output). Its determinism claims
      duplicate Principle VII.
    - **Proposed change**: Migrate the durable claims into IV/X/VII
      with cross-references; remove XVI as a standalone principle if
      nothing remains that is uniquely its own.
    - **Rationale**: A constitution accumulates principles over time;
      occasional pruning is healthy. The bar for keeping a principle
      is "this content has nowhere else to live and stands on its
      own." XVI may not clear that bar.
    - **Risk if ignored**: Constitutional bloat; future readers spend
      cognitive cycles on a principle that mostly restates others.

---

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/CONSTITUTION-v2.3.2-blind.md` (the audited constitution; Principle XVI specifically lines 426-481)
- Principle VII: Reproducibility Over Inconsistency (lines 140-152) — overlapping reproducibility territory
- Principle XI: Single Source of Truth (lines 277-320) — the test XVI's clarification block fails when it restates VII's claims
- Principle XV: Plugin Isolation (lines 393-424) — overlapping plugin-output territory
- Principle XXIII / XXIV: Provider Robustness Contract / Safety-Critical Defense-in-Depth (lines 654-706) — the model XVI should follow for enforceable contracts (schema + parser + test)
- Principle IV: Documentation Is the Product (lines 96-110) — natural home for XVI's transparency claim if XVI is folded
