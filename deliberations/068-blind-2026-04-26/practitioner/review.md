# Practitioner Review — Constitution v2.3.2 (blind)

**Reviewer perspective**: I'm a developer about to ship a PR that touches the parameter-pinning code path. I'm reading this constitution for the first time as a guide to whether my change passes review. I do not know which principles are recent or contested.

## Executive Summary

Principle XVI (Mathematical Transparency) is the principle most likely to confuse a developer trying to use the constitution as a real gate. It mixes three different things — a user-facing UX promise (plain-language explanations), an architectural invariant (parameters pinned per run), and an internal pipeline description (3 stages with different determinism properties). Each of those, individually, has merit. Stitched together under one heading, the principle reads like an architecture-doc excerpt that wandered into a constitution.

A practitioner shipping changes to the optimization layer needs the constitution to answer one question: **"is what I'm about to do compliant?"** XVI partially answers that for the narrow case of "do not re-resolve parameters mid-run" — the clarification block at the bottom is the one operationally crisp sentence in the whole principle. The rest is either covered by Principle VII (reproducibility), Principle X (Zen of Python output / readability), and Principle IX (functional, explicit), or it's documentation that belongs in the spec for the 3-stage pipeline itself, not in the constitution.

My recommendation, with full willingness to be overruled by people who know the recent history: **collapse XVI into a 4–6 line principle that states the user-facing transparency invariant and the parameter-pinning rule, and move the 3-stage pipeline description into the spec it came from**. If the deliberation prefers to keep XVI intact, at minimum the within-run / cross-run distinction needs to be reframed in terms a developer can mechanically verify in a code review.

## Alignment — where XVI is operationally useful

These are the places XVI does something a PR author can act on.

1. **Parameter pinning rule (the clarification block, lines 469–476)**. "A future PR that re-resolves parameters mid-deliberation, or that lets parameter values drift during a single optimization run, violates this principle." This is the one sentence in XVI that I, as a developer, can hold against my diff. If my PR introduces a code path that would re-call the LLM gap-filler after the first resolution, I know I'm violating the principle. This is real, enforceable, and not duplicated elsewhere — Principle VII says "same inputs produce same output" but does not specifically forbid mid-run re-resolution of stochastic inputs.

2. **Solver-swap invariant (line 466–467)**. "Changing solvers MUST NOT change what is being optimized." This is a useful architectural rule that constrains future PRs to keep the objective function as the contract surface, not the solver implementation. A practitioner adding AMPL alongside nashopt has a clear gate: if the optimization result differs in *what* is being computed (not just *how*), the PR is non-compliant.

3. **Plain-language explanation requirement (lines 459–463)**. The "Equilibrium quality: 0.87" → "87% of agents are at their best possible position given others' positions" rule is a concrete, testable UX requirement. A PR that adds a new optimization output without a plain-language gloss can be flagged in review against this clause.

4. **Template-documents-its-form requirement (lines 455–458)**. "Every objective function template documents its mathematical form, its parameters, and what each parameter means in plain language." This is a good documentation gate for spec 013 templates and is mechanically checkable (does the template have the documentation block? yes/no).

5. **Coordination with Principle VII**. The line "Once parameters are pinned, the optimization is reproducible (Principle VII applies)" is genuinely useful — it tells a reviewer where the determinism story handoff happens between XVI and VII. Without this bridge sentence, VII's "same inputs produce same output" would be ambiguous in the presence of stochastic LLM calls.

## Missed Opportunities — where XVI is overengineered or aspirational

These are the places XVI burns ink without giving a practitioner anything actionable.

1. **The 3-stage pipeline breakdown (lines 437–449) reads like spec excerpt, not constitution**. The numbered stages are descriptive — they explain *how* the implementation works today. A constitution should encode invariants that constrain future implementations, not document the current pipeline architecture. If spec 013 is rewritten in 6 months to fold parsing and assembly together, this principle text becomes wrong even if the underlying invariants (user intent → math, no opaque internals) still hold. **The right home for this content is the spec or an architecture doc, with a one-line reference from XVI**.

2. **"Within-run determinism" vs. "cross-run reproducibility" terminology is academic**. As a practitioner reviewing a PR, I do not naturally think in those terms. I think: "does this PR cache the LLM call across phases? does it re-call within a single run?" The constitution should phrase the invariant operationally: "the LLM gap-filler MUST be called at most once per parameter per deliberation run; subsequent uses MUST read from the pinned cache." That's what the principle actually means; the determinism-scope language obscures it.

3. **The clarification block (lines 469–476) is a tell**. A principle that needs a clarification block titled "determinism scope" is a principle that did not land cleanly the first time. The fact that the author had to add a separate paragraph saying "Principle XVI claims X and does NOT claim Y" suggests the original wording was confusing to readers. The fix is to rewrite the principle so the clarification is unnecessary, not to bolt the clarification on as a footnote.

4. **"Mathematical Transparency" as a name oversells the scope**. The principle is really three loosely related rules: (a) user-parameterizable objectives, (b) parameter pinning, (c) plain-language output. None of those is "mathematical transparency" in any rigorous sense — they are UX rules for an optimization layer. The name invites scope creep (any future math-related concern will get appended to XVI because the name is broad enough to absorb it).

5. **No enforcement mechanism**. Principle XXIV ("Safety-Critical Defense-in-Depth") explicitly demands a contract test reproducing the failure scenario. Principle XXVI ("Meta-Testing for Parametrized Capabilities") demands a meta-test. Principle XXII demands force-include in `pyproject.toml`. Principle XVI demands... vibes? There is no test, no linter check, no CI gate that catches a PR violating "within-run determinism." The principle is aspirational without a verification path.

6. **Overlap with Principle VII is real, not just feared**. Principle VII says: "Re-running a conversus with the same config overwrites cleanly. No accumulated state, no merge conflicts with prior runs." Principle VII says: "Template variable substitution is mechanical — same config produces same prompts. No ambient state or hidden context." A practitioner reading both XVI and VII has to mentally diff them to find the delta. The honest delta is "XVI extends VII to handle stochastic LLM gap-filling by mandating pinning" — and that one sentence could be a sub-bullet under VII.

7. **Overlap with Principle IX (explicit typing, Pydantic models)**. The "every parameter has a meaning in plain language" requirement maps closely to IX's "self-documenting through clear naming and structure" plus "comments explain WHY, not WHAT." The plain-language gloss requirement could be expressed as a Pydantic field description convention, lifting it from XVI prose into IX's typing discipline.

8. **Overlap with Principle X (Zen of Python output)**. "Equilibrium quality: 0.87" → "87% of agents are at their best possible position" is exactly the Zen-of-Python "explicit is better than implicit, readability counts" rule applied to optimization output. X already covers this; XVI duplicating it is redundant.

9. **Aspirational tone in lines 432–434**. "The user MUST understand what is being optimized, even without understanding the math." That is an aspiration, not a verifiable contract. How does a reviewer mechanically test "the user understood"? The principle would be stronger if it said: "every objective function template includes a `description:` field in plain language that does not contain Greek symbols or LaTeX," which is something a linter can check.

## Off-Base Assumptions

1. **XVI assumes the 3-stage pipeline is the canonical architecture forever**. The principle text is structured around stages 1/2/3. If a future spec collapses stage 1 and 3 (parsing and assembly become a single deterministic function), or interposes a stage 1.5 (constraint validation), the principle's numbering stops matching the code. A constitution should not enumerate implementation stages; it should enumerate invariants.

2. **XVI assumes "determinism" is the user concern**. It isn't. The user concern is "I get the same answer when I re-run with the same config." That's a behavioral promise. "Within-run determinism" is an implementation property, not a user-facing guarantee. The principle leaks implementation concepts into a user-promise framing.

3. **XVI assumes "pinned parameters" are persisted and reproducible across runs**. The clarification says "Cross-run variance is acceptable; within-run variance is prohibited." But Principle VII says re-running with the same config produces structurally identical output. If parameters are pinned per-run and cross-run variance is acceptable, then re-running with the same config can produce *different optimization results* (because the LLM gap-filler is stochastic and runs fresh on each invocation). This contradicts VII's promise unless the pinned parameters are themselves persisted to the run output and replayable. **The principles do not resolve this tension**, and a practitioner reading both will be confused about which guarantee to honor.

4. **XVI assumes the LLM gap-filling step is a single discrete call**. Real implementations may batch, retry, or stream. The principle's discussion of "the LLM call" as a singular event is too crisp for what production LLM integration actually looks like.

## Actionable Recommendations

In rough priority order. I'm flagging the "remove or simplify" options as legitimate even though I don't know which principles are new — if XVI was added recently to fix a concrete bug, removal is wrong; if it was added speculatively, removal is right.

1. **Rewrite XVI as 4–6 lines focused on the parameter-pinning invariant.** Drop the 3-stage pipeline breakdown. Drop the within-run / cross-run terminology. Keep the user-parameterizable promise, the pinning rule, and the solver-swap invariant. Move the pipeline description to spec 013 or a new architecture doc with a `*Origin*` link from the principle.

2. **Replace "within-run determinism" / "cross-run reproducibility" with operational language.** Suggested phrasing: "Each LLM-resolved parameter MUST be cached at first resolution and reused for the remainder of the deliberation run. Re-resolving a parameter mid-run is a violation of this principle."

3. **Resolve the VII-vs-XVI tension on cross-run reproducibility.** Either (a) require pinned parameters to be persisted to run output and replayable on re-run (making cross-run determinism real), or (b) explicitly carve out optimization runs from VII's "same config produces same output" promise. The current text leaves this ambiguous and a practitioner cannot tell which way to lean.

4. **Add a verification mechanism.** Mirror XXIV's contract-test requirement: "Every objective function template MUST have a test that pins parameters at known values and asserts the assembled function is byte-identical across two assemblies." Without a test gate, the principle cannot be enforced in CI.

5. **Move the plain-language output rule into Principle X (Zen of Python Output) as a sub-bullet.** "Plugin recommendations and optimization outputs MUST include a plain-language gloss alongside numerical values" fits naturally under X's "explicit is better than implicit." This eliminates duplication.

6. **Move the template-documentation rule into a spec 013 acceptance criterion**, not a constitutional principle. "Every template documents its parameters in plain language" is a code-review checklist item, not an invariant.

7. **Consider removing XVI entirely**. If recommendations 1–6 are taken, what remains is: (a) parameter-pinning rule (could be a sub-bullet of VII), (b) solver-swap invariant (could be a sub-bullet of II "Stable Interfaces" — the objective function is the stable interface, the solver is implementation). With those moves, XVI has nothing left that doesn't fit better elsewhere. The constitution would be tighter without it.

8. **If XVI is retained, rename it.** "Mathematical Transparency" is too broad. Suggested alternatives: "Pinned Parameter Discipline", "Optimization Reproducibility Contract", "User-Parameterized Objectives". The narrower name discourages future scope creep.

9. **If XVI is retained, add the missing CI hook.** A linter check that scans `templates/optimization/*.yml` (or wherever spec 013 templates live) for missing `description:` and `plain_language:` fields would operationalize the documentation requirements.

10. **Add an explicit cross-reference from VII to XVI.** Right now VII does not mention that stochastic LLM steps are a special case requiring pinning. A practitioner reading VII alone would conclude "everything is deterministic" and miss XVI. A one-line "See Principle XVI for stochastic-input handling" inside VII would close the gap.

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/068-blind-2026-04-26/CONSTITUTION-v2.3.2-blind.md` — entire constitution, with focus on Principle XVI (lines 426–481) and adjacent principles VII (lines 140–152), IX (lines 174–253), X (lines 256–274), II (lines 58–80), XXIV (lines 681–706), and XXVI (lines 749–771)
- Principle XVI internal references: spec 013 (objective function templates), specs 012–019 (game engine vision)
- Principle VII as the determinism baseline that XVI extends or duplicates
- Principle X as the readability baseline that XVI's plain-language rule duplicates
- Principle IX as the typing/explicitness baseline that XVI's parameter-meaning rule overlaps with

---

**Bottom line for the developer about to ship**: if my PR touches parameter-pinning code, XVI tells me one useful thing — don't re-resolve mid-run — buried under three paragraphs of pipeline description and a clarification footnote. I would prefer a 4-line principle that says exactly that. The rest belongs in the spec.
