# Cross-Principle Coherence Review — Constitution v2.3.2 Candidate

## Executive Summary

The amended Principle XVI (lines 448-503) introduces a structurally honest three-stage determinism taxonomy that broadly fits the constitution's existing reproducibility commitments, but it does so by importing a new term ("mechanical assembly") and a new admission ("stochastic at the LLM call," line 463) that interact non-trivially with Principles VII and VIII. The single explicit cross-reference XVI makes — "(Principle VII applies)" on line 476 — is correctly placed but underspecified: it does not address whether "structurally identical output" (line 164) survives the stochastic gap-filling step on a *first* run, where parameters have not yet been pinned.

The amendment's terminology shift from a presumed earlier umbrella of "deterministic assembly" to "mechanical assembly" (line 458) is *locally* coherent (the new word survives Principle VIII's preference for "mechanical template-driven behavior," line 178) but the constitution still uses "deterministic" as the unqualified, top-level commitment in VII (lines 161-175) and VIII (lines 188-190). XVI now carves out a documented exception inside that commitment without VII or VIII being updated to acknowledge the carve-out. This is the largest coherence risk in the amendment.

The clarification block at lines 491-498 is the strongest part of the amendment from a cross-principle perspective: it scopes the determinism claim, names the prohibited future change ("re-resolves parameters mid-deliberation"), and inverts the discipline from "make the LLM deterministic" to "pin and cache its output." That inversion would benefit from a single explicit cross-reference to Principle XI (Single Source of Truth, lines 298-322) — pinned parameters become the authoritative source for the assembled objective, and re-resolution would create the exact "two places that disagree" failure mode XI exists to prohibit.

## Alignment

- **XVI line 476 ("Principle VII applies") correctly invokes VII (lines 161-175) for the post-pinning regime.** Once parameters are pinned, the assembly is deterministic from config alone, which is the predicate VII actually requires ("An implementor can predict the output tree from `conversus.yml` alone," lines 169-170). The invocation is well-targeted to the cross-run reproducibility claim, not to the within-run claim.
- **"Mechanical assembly" (line 458, line 470) is consistent with Principle VIII's chosen umbrella term "mechanical" (line 178: "Prefer mechanical template-driven behavior").** The new vocabulary in XVI plugs into VIII's existing taxonomy without coining a new word — "mechanical" already meant "rule-based, not inferred" in the constitution.
- **The "LLM does not generate the objective function" claim (lines 472-473) reinforces VIII's "Unconstrained inference is a last resort" (lines 193-194).** XVI is using the LLM only to translate identifiers and answers, exactly the constrained role VIII sanctions.
- **The cached-pinned-values discipline (lines 463-467) is consistent with XII (No Dead Infrastructure, lines 344-366) by implication:** pinned parameters are provisioned-and-consumed within the same run; nothing is provisioned for hypothetical re-resolution.
- **XVI's "objective function template … pre-defined at design time" (lines 471-472) lines up with Principle I's spec-driven mandate (lines 66-77)** — spec 013 is named as the design-time artifact, which matches "New features require a spec in `specs/{NNN}-{name}/spec.md` before any SKILL.md edits" (lines 73-74).
- **The clarification block (lines 491-498) follows the same "Clarification (vN.N.N)" cosmetic pattern XV used in v2.3.1 (lines 434-442) and XI used in v2.3.0 (lines 324-342),** giving readers a consistent visual anchor for amendment scope.

## Missed Opportunities

- **Line 164 ("structurally identical output") is not reconciled with line 463 ("stochastic at the LLM call").** A first-run deliberation with no cached parameters will have non-identical structural output across two cold runs (different LLM-generated parameter values produce different assembled objective bodies). XVI should explicitly note that VII's "structurally identical" claim applies *to the assembly stage* and *across post-pinning runs*, not to the first-run gap-filling stage. Currently, a careful reader will notice VII and XVI appear to contradict each other on cold-run behavior.
- **Line 167 ("No ambient state or hidden context") interacts with the cache (line 466).** A pinned-parameter cache *is* persisted state that conditions later behavior. XVI should cross-reference VII line 167 and clarify that the cache is sanctioned persistence, distinguishing it from the "ambient state" VII prohibits (the cache is keyed and explicit; ambient state would not be).
- **Lines 463-467 do not reference Principle XI (Single Source of Truth, lines 298-322), but should.** Pinned parameters become *the* authoritative source for the assembled objective for the remainder of that run. Re-resolution would be exactly the "same fact in two places" failure XI line 316 prohibits ("If you find yourself writing the same fact in two places, stop"). The "future PR that re-resolves parameters mid-deliberation" risk on lines 496-497 is materially the XI failure mode.
- **The "cached values from the first resolution are reused" discipline (lines 466-467) does not say where the cache lives.** Principle X (Zen of Python Output, lines 277-296) calls for "one obvious way to find the result" (line 283) and predictable file structure. XVI should at minimum note that pinned parameters land in a deterministic location in the output tree (e.g., next to `summary/final.md`) so the persistence is observable, not hidden.
- **Principle V (Observable Deliberation, lines 134-144) is not invoked by XVI, but the LLM gap-filling step is exactly the kind of operation that should emit a phase report line.** "Phase {N} complete: {summary}" (line 140) extends naturally to "parameters resolved: 7 pinned (3 from cache, 4 newly resolved)," and XVI not mentioning observability of the stochastic step is a gap given V's coverage requirements.
- **Principle II (Stable Interfaces, lines 79-102) is not referenced even though pinned parameters are now effectively a contract surface.** If a future change alters how parameter caches are keyed or persisted, that is a stable-interface change. XVI should classify the pinned-parameter contract under II's stability regime, or explicitly mark it as not-yet-stable.
- **Principle III (Backward-Compatible Extension, lines 104-117) is silent on what happens if a deliberation is re-run after the pipeline implementation changes.** XVI's "Repeating a deliberation … does NOT re-call the LLM" (lines 463-465) assumes the cache is interpretable across versions. III's "Omitting optional fields MUST preserve existing behavior exactly" (lines 108-109) is the closest analogue and could anchor a re-run-across-versions guarantee.
- **The Clarification block (lines 491-498) names the prohibition ("future PR that re-resolves parameters mid-deliberation") but does not designate which test layer enforces it.** Principle XXIV (Safety-Critical Defense-in-Depth, lines 712-741) is the natural home for that enforcement — re-resolution mid-run is exactly the silent-drift failure mode XXIV exists to catch with "Contract test reproducing the failure scenario" (lines 730-733). XVI should cross-reference XXIV for the test obligation.
- **Line 489 ("Changing solvers MUST NOT change what is being optimized") is a reproducibility-class claim that should explicitly cite VII.** The current wording stands alone, but it is the same property VII calls "structurally identical output" applied at a different layer (solver substitution rather than re-run). A `(Principle VII applies)` parenthetical mirroring line 476 would strengthen coherence.

## Off-Base Assumptions

- **XVI lines 463-465 assume that "Repeating a deliberation with the same input does NOT re-call the LLM for parameters" is enforced by the system.** No other principle currently mandates this caching behavior. Principle VII (lines 161-175) talks about deterministic *outputs given inputs*, not about caching strategy. If the cache is invalidated (e.g., user clears it, version bump, hash mismatch) the LLM *will* be re-called. XVI's wording presents "cached values are reused" as a property when it is actually a policy that has no enforcement principle backing it elsewhere in the document.
- **XVI line 476's parenthetical "(Principle VII applies)" assumes VII's claim is conditionally scoped to "once parameters are pinned."** VII as written (lines 161-175) makes no such conditional claim — it says "Given the same inputs, conversus MUST produce structurally identical output" unconditionally. XVI is *narrowing* VII without VII being amended to acknowledge the narrowing. The parenthetical reads like a reference but is functionally a unilateral redefinition.
- **The Clarification block (lines 491-498) assumes a reader will understand that "within-run determinism" applies to the assembled objective function but *not* to the LLM call that produced its parameters.** This is correct but is not stated anywhere else in the constitution. Principle VIII (lines 176-194) treats "mechanical" and "deterministic" as roughly co-extensive; XVI assumes a finer distinction that VIII does not articulate.
- **Lines 488-489 ("Solver choice … is an implementation detail") assume that solver substitution preserves the objective function bit-for-bit.** This is a strong claim that depends on numerical stability of the solver, which is not a property the constitution discusses anywhere. XVI presents it as definitional ("Changing solvers MUST NOT change what is being optimized") but the *result* of optimization may differ across solvers even when the objective is identical.

## Actionable Recommendations

1. **[P1] Explicitly scope Principle VII's "structurally identical output" claim.**
2. **[P1] Add a Principle XI (Single Source of Truth) cross-reference inside XVI's pinning discipline.**
3. **[P1] Cross-reference Principle XXIV for the re-resolution prohibition.**
4. **[P2] Reconcile XVI's caching discipline with Principle VII's "no ambient state" prohibition.**
5. **[P2] Anchor the pinned-parameter contract in Principle II (Stable Interfaces).**
6. **[P2] Add observability obligation tied to Principle V.**
7. **[P2] Cross-reference Principle VII at line 489 for solver substitution.**
8. **[P3] Acknowledge the "mechanical" vs "deterministic" terminology shift in Principle VIII.**
9. **[P3] Add the cache location to Principle X's "one obvious way to find the result."**
10. **[P3] Tighten the solver-equivalence claim on lines 488-489.**

(See full bodies in original review — abbreviated here for the orchestrator's record.)

## Referenced Documentation

- `CONSTITUTION-v2.3.2-candidate.md` — Principles I, II, III, V, VII, VIII, X, XI, XII, XV, XVI, XXIV across lines 66-503; v2.3.2 clarification 491-498; version footer 900.
