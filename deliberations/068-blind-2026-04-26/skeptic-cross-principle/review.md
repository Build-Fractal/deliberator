# skeptic-cross-principle: Audit of Principle XVI for Cross-Principle Conflicts

## Executive Summary

Principle XVI (Mathematical Transparency) is well-intentioned but has been
amended in a defensive crouch: the long "Clarification: determinism scope"
section reads as if it was bolted on after a previous reviewer pointed out
an inconsistency with Principle VII (Reproducibility Over Inconsistency).
The amendment papers over the conflict rather than resolving it. As written,
XVI grants itself two privileges that no other principle in the constitution
enjoys: (a) explicit permission to harbor a stochastic step inside an otherwise
"deterministic" pipeline, and (b) a bespoke vocabulary ("pinning",
"within-run vs cross-run", "mechanical assembly") that is not used anywhere
else and that quietly redefines what "reproducibility" means for one
subsystem. That is a textbook constitutional drift: a principle so important
it gets to break the rules the other principles establish.

The strongest argument for redefining or merging XVI: VII already states
that "Given the same inputs, conversus MUST produce structurally identical
output. Deterministic orchestration is non-negotiable." XVI's stage 2
("LLM gap-filling: stochastic at the LLM call") is a direct, named
exception to that non-negotiable rule. If the rule has an exception, the
rule was never non-negotiable; either VII must be amended to recognize
LLM-mediated steps as a category VII does not cover, or XVI must be
demoted to a clarification of VII rather than a co-equal principle.
Leaving both in place as written produces interpretive ambiguity in
exactly the place — optimization-driven decisions — where ambiguity is
most damaging.

A secondary, narrower concern: XVI uses "mechanical" for stage 3 while
VII uses "mechanical" for template variable substitution AND "deterministic"
for orchestration. Stage 3 is described as "mechanical" and "deterministic"
in the same paragraph as if the words are interchangeable. They are not
interchangeable elsewhere in the constitution (VIII contrasts "mechanical
template-driven behavior" against "LLM inference"; VII uses "deterministic"
as the higher-order claim and "mechanical" as the implementation
technique). XVI is sloppy with the vocabulary the rest of the constitution
has carefully separated.

## Alignment

- **XVI ↔ VIII (Templating Engines Over Inference)**: Strong, intentional
  alignment. XVI's claim that "the LLM does not generate the objective
  function — it translates gap identifiers into natural-language questions"
  is exactly VIII's "Agents fill variables; they do not invent structure."
  XVI is, in part, VIII applied to mathematical optimization. This
  alignment is so strong it raises the merge question (see Recommendations).

- **XVI ↔ XV (Plugin Isolation)**: Aligned via Origin pointer to specs
  012-019 ("game engine vision"). XVI is the contract for the optimization
  layer that XV protects from leaking into core deliberation. The two
  principles share the same risk model (paid optimization vs free core)
  but address different surfaces.

- **XVI ↔ III (Backward-Compatible Extension)**: XVI's "solver choice is
  an implementation detail … Changing solvers MUST NOT change what is
  being optimized" is exactly the contract III demands of optional fields.
  Solver swap is a backward-compatible substitution because the objective
  function — the contract — is preserved.

- **XVI ↔ II (Stable Interfaces)**: The objective function template
  (spec 013) is implicitly a stable interface under II. XVI does not
  cross-reference II, but its "contract between user intent and
  mathematical optimization" framing is II's stable-interface concept
  applied to the optimization surface. This is an alignment that XVI
  fails to make explicit (see Missed Opportunities #1).

- **XVI ↔ IV (Documentation Is the Product)**: XVI's "Every objective
  function template documents its mathematical form, its parameters, and
  what each parameter means in plain language" is IV applied to math
  artifacts. The plain-language requirement for plugin recommendations
  ("Equilibrium quality: 0.87" insufficient) is Documentation-Is-Product
  enforced at the user-facing layer.

## Missed Opportunities

1. **XVI never cites VII.** This is the most damaging omission. XVI's
   own clarification block contains the phrase "Once parameters are
   pinned, the optimization is reproducible (Principle VII applies)" —
   but in the body, not the headline. A reader who skips the
   clarification block (which reads as a footnote) will see XVI's
   stochastic-LLM-step admission and conclude conversus tolerates
   non-determinism in optimization. XVI MUST open with "Subject to
   Principle VII, …" or the relationship has to be inverted (XVI as
   an extension of VII rather than a parallel principle).

2. **No reference from VII back to XVI.** VII says "Deterministic
   orchestration is non-negotiable." If LLM gap-filling is a sanctioned
   exception, VII should acknowledge it: "Deterministic orchestration
   is non-negotiable; Principle XVI defines the bounded exception for
   LLM-mediated parameter resolution." Without this back-reference, VII
   reads as absolute and XVI reads as a violation.

3. **"Pinning" is XVI-only vocabulary.** No other principle uses the
   verb "pin" for a parameter or value. The same concept exists
   elsewhere (XI's "single authoritative source", III's "omitting
   optional fields preserves behavior") but with different words.
   Either XVI should define "pinning" as a term-of-art (perhaps in
   II's stable-interface vocabulary) or it should adopt the existing
   vocabulary. As written, "pinning" sounds like a new requirement
   that exists only in this principle.

4. **"Within-run determinism" is undefined elsewhere.** What is a
   "run"? VII talks about re-running with the same config. XVI talks
   about a single deliberation run. Are those the same unit? If so,
   one of them should adopt the other's term. If not, the constitution
   has two implicit time-units and only XVI names one of them.

5. **No interaction clause with V (Observable Deliberation).** If
   parameters are LLM-resolved and pinned, the pinned values are
   observable artifacts that V's "every phase MUST report progress"
   should arguably require logging. XVI is silent on whether the
   pinned parameter set must appear in deliberation output. This is
   a real gap: a user troubleshooting an unexpected optimization
   result would need to see the pinned values, and V is the principle
   that should require their emission.

6. **No cross-reference to XII (No Dead Infrastructure).** XVI
   describes a 3-stage pipeline. XII demands that every provisioned
   capability have a consumer. If a template parameter is defined but
   the LLM gap-filler never produces a value for it, is that XII-dead
   or is it XVI-stochastic-acceptable? The constitution does not say.

7. **No interaction clause with XXIV (Safety-Critical Defense-in-Depth).**
   XVI describes optimization that "drives decisions". XXIV defines
   safety-critical paths to include "synthesis verdict generation".
   Optimization-driven decisions in arbitration mode could plausibly
   be synthesis verdicts. If so, XVI's tolerance for stochastic
   LLM-mediated parameters interacts directly with XXIV's three-layer
   defense requirement. Neither principle acknowledges the other.

8. **No cross-reference to XI (Single Source of Truth) for the
   parameter cache.** XVI says "cached values from the first resolution
   are reused." That cache IS a single source of truth for run-scoped
   parameters. XI is the relevant principle. Without the cross-reference,
   the cache lifecycle (when is it invalidated? where is it stored?) is
   underspecified.

9. **"Mechanical" used inconsistently with VIII.** VIII establishes
   "mechanical" as the antonym of "LLM inference". XVI uses "mechanical
   assembly" for the stage that follows LLM gap-filling. Within XVI,
   stage 1 is "deterministic" and stage 3 is "mechanical" — implying
   they are different things — but the body of XVI describes both as
   "deterministic" in the next sentence. Either pick one term
   consistently or define why they differ.

## Off-Base Assumptions

1. **XVI assumes "stochastic at the LLM call" is acceptable as long as
   values are pinned.** This is plausible but unargued. A user who
   re-runs a deliberation expecting reproducibility would be surprised
   to learn the first run's LLM output is now permanent. The principle
   should justify why first-run pinning is the right policy (versus,
   e.g., requiring the user to confirm pinned values, or persisting
   them outside the run).

2. **XVI assumes solver substitution preserves the objective function
   bit-for-bit.** "Changing solvers MUST NOT change what is being
   optimized" is a strong claim. In practice, two solvers will produce
   different floating-point results on the same objective function
   even with identical inputs (different numerical methods, different
   tolerances). The principle conflates "what is being optimized" (the
   contract) with "the optimization result" (the output). Without
   distinguishing them, the principle promises something solvers
   cannot deliver.

3. **XVI assumes plain-language explanations are sufficient mathematical
   transparency.** "87% of agents are at their best possible position
   given others' positions" sounds transparent but is itself a
   compressed gloss of equilibrium theory. A user who does not
   understand Nash equilibria still does not understand what "best
   possible position" means. Principle XVI's "users do not need to
   understand the math" is a comforting framing that may not survive
   contact with adversarial users.

4. **XVI assumes the 3-stage pipeline is the only architecture worth
   constitutionalizing.** Specs 012-019 are cited as the origin, but
   the principle constitutionalizes the implementation pattern, not
   the underlying property. If a future spec replaces the 3-stage
   pipeline with a 2-stage or 4-stage one, XVI as written becomes
   stale. The principle should describe the property (transparency
   of optimization intent) not the mechanism (3 stages).

## Actionable Recommendations

1. **Merge XVI into VII as an extension** ("Extension (vN.N): LLM-mediated
   parameter resolution"). VII already establishes the reproducibility
   contract. XVI's distinct content — the 3-stage pipeline and the
   pinning discipline — is a refinement of VII for the optimization
   surface, not a separate principle. Precedent: IX has a behavior-over-
   shape extension; XI has a Registry-First Declaration extension.
   XVI fits the same pattern.

2. **Alternatively, narrow XVI to "Mathematical Transparency" only**
   (parameter meaning, plain-language explanations, solver substitution)
   and move the 3-stage / pinning discipline content into a VII
   extension. This preserves XVI as a distinct principle about user
   comprehension while removing its problematic determinism claims.

3. **Add a back-reference from VII** acknowledging the LLM-mediated
   exception. Without this, VII's "non-negotiable" framing is misleading.
   Suggested: append "Principle XVI defines the sole sanctioned
   exception, scoped to LLM-mediated parameter resolution with
   within-run pinning."

4. **Replace "mechanical" in XVI stage 3 with "deterministic"** (or
   replace "deterministic" in stage 1 with "mechanical"). Pick one. The
   current usage suggests they mean different things in adjacent
   sentences. VIII already establishes "mechanical" as the antonym of
   "LLM inference"; XVI should adopt that convention or explicitly
   redefine the term.

5. **Define "pinning" as a constitutional term**, either in II (as a
   stable-interface concept) or as a glossary entry. As a one-off
   vocabulary item used only in XVI, it reads like jargon imported
   from one spec rather than a cross-cutting concept.

6. **Add an interaction clause between XVI and V (Observable
   Deliberation)**: pinned parameter values MUST be emitted as
   deliberation output so users can audit what was optimized. Without
   this, XVI's transparency claim is hollow — the user can read the
   template but cannot see the values plugged into it.

7. **Add an interaction clause between XVI and XXIV (Safety-Critical
   Defense-in-Depth)**: when optimization drives a synthesis verdict
   (red-blue, arbitration), XXIV's three-layer defense MUST validate
   the pinned parameters. Without this, XVI's stochastic stage is a
   defense-in-depth gap.

8. **Soften the solver-substitution claim**: "Changing solvers MUST
   NOT change what is being optimized" should be qualified to
   "MUST NOT change the objective function or its parameter
   semantics." Current wording promises numerical-result equivalence
   that no two solvers can deliver.

9. **Generalize the principle away from the 3-stage pipeline**: the
   constitutional property is "user understands what is being
   optimized." The 3-stage pipeline is one implementation of that
   property. XVI as written constitutionalizes the implementation,
   which violates III's spirit (constitutions describe contracts,
   implementations evolve). Move the 3-stage description to spec 013
   where it belongs and keep XVI focused on the user-facing
   contract.

10. **Consider removing XVI entirely** if (1) its transparency content
    can fold into IV (Documentation Is the Product) and (2) its
    determinism content can fold into VII. The remaining content —
    the 3-stage pipeline — belongs in spec 013, not in the
    constitution. This is the most aggressive recommendation and
    should be considered as a backstop if recommendations 1-9 do not
    achieve consensus.

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/CONSTITUTION-v2.3.2-blind.md`
  — full constitution text under audit; Principles VII, VIII, XVI,
  and the determinism-scope clarification block were the load-bearing
  passages for this review.
- Principle VII (Reproducibility Over Inconsistency), lines 139-153 —
  primary conflict surface.
- Principle VIII (Templating Engines Over Inference), lines 154-172 —
  vocabulary alignment ("mechanical" usage).
- Principle XVI (Mathematical Transparency), lines 426-481 — subject
  of audit, including the post-hoc Clarification block at lines
  469-476.
- Principle XV (Plugin Isolation), lines 393-424 — shared origin
  story (game engine vision specs 012-019); relevant to merge
  question because XVI's content overlaps XV's "paid optimization
  layer must not compromise free deliberation core" framing.
- Principle XXIV (Safety-Critical Defense-in-Depth), lines 681-706 —
  unacknowledged interaction with XVI's stochastic stage.
- Principle V (Observable Deliberation), lines 113-122 — unacknowledged
  interaction with XVI's pinned-parameter emission requirement.
- Constitution Sync Impact Report header, lines 1-38 — establishes
  that XVI is NOT in the v2.3.0 amendment list, indicating XVI
  predates the recent amendments and the determinism-scope
  clarification was added separately. This dating supports the
  hypothesis that XVI was patched defensively rather than
  re-derived.
