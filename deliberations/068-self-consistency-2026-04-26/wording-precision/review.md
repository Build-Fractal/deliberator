### Executive Summary

The candidate v2.3.2 amendment to Principle XVI restructures the first bullet of "Mathematical Transparency" into a 3-stage pipeline (symbolic parsing → LLM gap-filling → mechanical assembly), each with an explicit determinism property, and appends a "Clarification (v2.3.2): determinism scope" paragraph that names within-run determinism, cross-run reproducibility, and the explicit non-claim about LLM determinism. The intent is clearly to resolve the prior tension between Principle VII ("structurally identical output") and the obvious fact that LLMs are stochastic, by localizing determinism to assembly while moving stochasticity to a pinning step.

From a wording-precision standpoint the amendment is largely successful at the conceptual level — it names three stages, assigns determinism properties to each, and ends with a falsification rule ("A future PR that re-resolves parameters mid-deliberation … violates this principle"). However, several normative verbs are missing or weak in exactly the places a future reviewer would need them. The 3-stage breakdown is descriptive prose, not requirement language: there is no MUST/SHOULD anywhere in lines 458-476 except inside reused sub-clauses, and the central pinning rule is buried in a parenthetical ("cached values from the first resolution are reused") rather than stated as an obligation. The clarification paragraph at L491-498 then asserts what the principle "claims" rather than what implementations MUST do, which makes it weaker than a normative rule and creates an asymmetry: the falsification clause is sharp, but the obligation it falsifies against is vague.

**Most important recommendation**: Convert the pinning rule in stage 2 from descriptive prose ("the resulting parameter values are pinned per deliberation run") into an explicit normative requirement ("Resolved parameter values MUST be pinned for the duration of the deliberation run; the LLM MUST NOT be re-invoked for parameter resolution within the same run") so a reviewer can mechanically test a PR against it.

### Alignment

- **Falsification clause is concrete** (L496-498): "A future PR that re-resolves parameters mid-deliberation, or that lets parameter values drift during a single optimization run, violates this principle." This sentence is unusually precise for a constitution — it names two specific code behaviors that constitute violation, which a reviewer can mechanically check against.

- **Stage labels carry their determinism property in-line** (L460, L462, L468): Each stage in the numbered list is tagged "deterministic", "stochastic at the LLM call", or "deterministic" before the explanation. This puts the load-bearing claim adjacent to its label and avoids forcing the reader to extract it from prose.

- **"Bit-for-bit" is unambiguous** (L470): "the resulting objective function is identical bit-for-bit on every assembly" leaves no interpretive wiggle room — there is no softer reading of bit-for-bit. This is the right level of precision for a determinism claim about mechanical assembly.

- **Within-run vs cross-run distinction is named explicitly** (L491-493, L466-467): The principle separates "within-run variance is prohibited" from "cross-run variance is acceptable" and the clarification re-states this as "within-run determinism" vs "cross-run reproducibility once parameters are pinned." The vocabulary is consistent across both halves, which is a precision win.

- **Explicit non-claim about LLM determinism** (L493-495): "It does NOT claim the LLM gap-filling step itself is deterministic" pre-empts the most likely future misreading. Negative scoping ("we do not claim X") is rare in this constitution and is exactly the right tool here given that VII still says "structurally identical output."

### Missed Opportunities

- **Pinning is descriptive, not normative** (L463-466): "the resulting parameter values are **pinned per deliberation run**. Repeating a deliberation with the same input does NOT re-call the LLM for parameters; cached values from the first resolution are reused." This describes what happens, not what MUST happen. Tightening: "Resolved parameter values MUST be pinned for the duration of the deliberation run. The LLM MUST NOT be re-invoked for parameter resolution within the same run; cached values from the first resolution MUST be reused." Impact: high. Without MUST, a future PR that re-resolves on retry has no rule to violate — only a description it disagrees with.

- **"Per deliberation run" is undefined** (L463-464): Concept 3 of the prompt asks whether a reviewer can tell if a specific code change violates this. "Run" is not defined here or elsewhere in Principle XVI. Does a retry constitute a new run? Does a Phase 6 re-execution? Does a `--continue` invocation? Tightening: define "deliberation run" inline or cross-reference Principle VII's "Re-running a conversus with the same config" language. Impact: high — this is the operational hinge of the whole pinning claim.

- **"Cached values from the first resolution"** does not say where the cache lives or how long it persists (L465-466): A reviewer auditing a PR cannot tell whether an in-memory dict, a file on disk, or a Redis entry satisfies this. Tightening: say "cached in [output_dir]/parameters.json" or at least "persisted for the lifetime of the run's output directory." Impact: medium.

- **"Cross-run variance is acceptable"** lacks bounds (L467): Acceptable to whom, and to what magnitude? A 1% drift is different from a 50% drift. Principle VII says "Given the same inputs, conversus MUST produce structurally identical output" — XVI now permits cross-run variance, which conflicts with VII unless XVI scopes the variance. Tightening: "Cross-run variance in resolved parameter values is acceptable; cross-run variance in the assembled objective function shape, parameter names, or template selection is NOT." Impact: high (this is also the cleanest fix for the XVI ↔ VII tension noted in the Off-Base section).

- **"Symbolic parsing"** is defined only by example (L460-462): "given a template ID, the parser yields the same gap identifiers every time." A reviewer needs to know what counts as a gap identifier and what counts as a template ID. Tightening: cite the spec 013 artifact that defines these (or at minimum the type — "string identifiers for unfilled parameters in the math template"). Impact: medium.

- **"LLM gap-filling" mixes two activities** (L473-475): The prose says the LLM "translates gap identifiers into natural-language questions and the user's answers into parameter values." That is two distinct LLM calls (question generation + answer extraction), each with its own determinism profile. The 3-stage breakdown collapses them into one stochastic step. Tightening: either split stage 2 into 2a (question generation) and 2b (answer→value extraction), or state explicitly "stage 2 encompasses both question generation and answer extraction; both are stochastic and both pinned together." Impact: medium.

- **"Fully-pinned parameter set"** (L469) is not defined: when is a parameter set "fully pinned"? Tightening: "all gap identifiers from stage 1 have an associated pinned value." Impact: low.

- **The clarification uses "claims" instead of normative language** (L491-493): "Principle XVI claims **within-run** determinism for the assembled objective function and **cross-run** reproducibility once parameters are pinned." A constitution does not "claim" — it requires. Tightening: "Principle XVI requires within-run determinism for the assembled objective function, and cross-run reproducibility of that function once parameters are pinned." Impact: medium. Compounds with the missing MUST in stage 2.

- **"Parameters are pinned"** uses passive voice without an agent** (L491-493, L463): Who pins them? The orchestrator? The provider? A `pin_parameters()` function call? Without an agent, the rule cannot be checked against a specific code path. Tightening: name the responsible component. Impact: low-medium.

### Off-Base Assumptions

- **The text alone does not guarantee parameter pinning is implemented.** The candidate's stage 2 says values "are **pinned per deliberation run**" as if reporting a fact about the codebase. The principle is a normative document, not a status report. If the underlying code does not actually cache resolutions (or does so inconsistently — e.g., on-disk for some providers, in-memory for others), the principle's descriptive prose is silently false. The Origin block (L500-503) names specs 012-019 as the source but does not cite a spec FR or test that locks in the pinning behavior. A reviewer reading only the constitution cannot verify the claim is enforceable.

- **"Cross-run variance is acceptable"** (L467) appears to contradict Principle VII directly. VII at L162-163 says "Given the same inputs, conversus MUST produce structurally identical output. Deterministic orchestration is non-negotiable." XVI now says cross-run variance in parameter values is acceptable. The clarification at L491-493 attempts to reconcile by scoping XVI's claim to the assembled objective function "once parameters are pinned" — but VII's "same inputs → structurally identical output" includes the parameter resolution step within "same inputs." If the user's natural-language answers are inputs, and the LLM's translation of those answers into parameter values is stochastic, then VII is violated by stage 2. The candidate does not explicitly say "Principle VII's determinism claim does NOT extend to LLM gap-filling output" or carve out the exception. This is a real internal contradiction that the v2.3.2 amendment was meant to resolve and only partly does.

- **The Origin claims this was the source of "past wording confusion"** (L457-458) but does not cite what the prior wording actually said. Without that anchor, a future editor cannot tell whether v2.3.2's wording avoids the same confusion or merely renames it.

### Actionable Recommendations

1. **Promote pinning from description to obligation** (Priority: P1)
   - **Current state** (L463-466): "the resulting parameter values are **pinned per deliberation run**. Repeating a deliberation with the same input does NOT re-call the LLM for parameters; cached values from the first resolution are reused."
   - **Proposed change**: "the resulting parameter values **MUST be pinned for the duration of the deliberation run**. The LLM **MUST NOT** be re-invoked for parameter resolution after the first successful resolution within a run. Cached values from the first resolution **MUST** be reused for any subsequent reference within the same run."
   - **Rationale**: Constitutions are normative. Descriptive prose cannot be violated, only contradicted.
   - **Risk if ignored**: A PR that re-resolves on retry passes review because there is no MUST to violate.

2. **Define "deliberation run"** (Priority: P1)
   - **Current state** (L463-464): "pinned per deliberation run" — undefined.
   - **Proposed change**: Add a parenthetical at first use: "pinned per deliberation run (a single invocation of the run engine producing one output directory; retries within an invocation are part of the same run, separate `/conversus run` invocations are different runs)."
   - **Rationale**: Without this, a reviewer cannot mechanically check whether a retry violates pinning.
   - **Risk if ignored**: Ambiguity about retry semantics produces silent drift between implementations.

3. **Resolve the VII ↔ XVI cross-run determinism tension explicitly** (Priority: P1)
   - **Current state** (L467, L491-493): XVI permits cross-run variance in parameter values; VII (L162-163) says "Given the same inputs, conversus MUST produce structurally identical output."
   - **Proposed change**: In the v2.3.2 clarification (after L495), add: "This carves an explicit exception to Principle VII: the assembled objective function is the determinism boundary, not the LLM-resolved parameter values that feed into it. Two runs with identical user inputs MAY produce different parameter values; both runs MUST produce structurally identical objective function shapes, parameter names, and template selections."
   - **Rationale**: The contradiction is real and the candidate only half-resolves it. Naming the exception explicitly closes the loop.
   - **Risk if ignored**: The constitution remains internally contradictory, defeating the point of the v2.3.2 amendment.

4. **Convert "claims" to normative verbs** (Priority: P2)
   - **Current state** (L491-493): "Principle XVI claims **within-run** determinism for the assembled objective function and **cross-run** reproducibility once parameters are pinned."
   - **Proposed change**: "Principle XVI **requires** within-run determinism for the assembled objective function and **requires** cross-run reproducibility of that function once parameters are pinned."
   - **Rationale**: A constitution requires; it does not claim.
   - **Risk if ignored**: Soft language invites soft enforcement.

5. **Bound "cross-run variance is acceptable"** (Priority: P2)
   - **Current state** (L467): "Cross-run variance is acceptable; within-run variance is prohibited."
   - **Proposed change**: "Cross-run variance in resolved parameter *values* is acceptable; cross-run variance in the assembled objective function's *shape* (parameter names, template selection, gap-identifier set) is prohibited. Within-run variance of any kind is prohibited."
   - **Rationale**: "Acceptable" without a scope is unbounded; pairs with #3.
   - **Risk if ignored**: A PR that swaps the template based on LLM whim could claim XVI compliance.

6. **Specify pinning storage and lifetime** (Priority: P2)
   - **Current state** (L465-466): "cached values from the first resolution are reused" — no location, no lifetime.
   - **Proposed change**: "cached values from the first resolution are persisted to the run's output directory and reused for the lifetime of that directory."
   - **Rationale**: Reviewers need to know where to look.
   - **Risk if ignored**: An in-memory-only implementation passes review but loses pinning across the orchestrator restart that retry typically implies.

7. **Disambiguate the two LLM activities in stage 2** (Priority: P2)
   - **Current state** (L473-475): Stage 2 is described as one stochastic step but the prose names two LLM activities (question generation + answer→value extraction).
   - **Proposed change**: "**LLM gap-filling**: stochastic at the LLM call. This stage encompasses both (a) translating gap identifiers into natural-language questions for the user, and (b) extracting parameter values from the user's natural-language answers. Both substeps are stochastic; both are pinned together once stage 2 completes."
   - **Rationale**: Without disambiguation, a reviewer cannot tell whether re-generating a question (without re-extracting a value) violates the principle.
   - **Risk if ignored**: Silent disagreement about which LLM calls count as "parameter resolution."

8. **Cite a spec FR for the pinning behavior** (Priority: P2)
   - **Current state** (L500-503): Origin names specs 012-019 generically.
   - **Proposed change**: Add a specific FR or contract test reference, e.g., "Pinning behavior is specified in spec 013 FR-{N} and verified by test {path}."
   - **Rationale**: Anchors the descriptive claim to a verifiable artifact.
   - **Risk if ignored**: The principle cannot be audited against the codebase without a search expedition.

9. **Define "fully-pinned parameter set"** (Priority: P3)
   - **Current state** (L469): "given a template and a fully-pinned parameter set"
   - **Proposed change**: "given a template and a *fully-pinned parameter set* (every gap identifier produced by stage 1 has an associated pinned value from stage 2)"
   - **Rationale**: Defines the precondition for stage 3's determinism guarantee.
   - **Risk if ignored**: Stage 3's bit-for-bit guarantee can be evaded by claiming the parameter set wasn't "fully" pinned.

10. **Name the agent that pins parameters** (Priority: P3)
    - **Current state** (L463, L491-493): Passive voice — "are pinned" without naming who pins.
    - **Proposed change**: Identify the orchestrator (or the specific subsystem) as the responsible component, e.g., "The run orchestrator MUST pin resolved parameter values…"
    - **Rationale**: Removes ambiguity about responsibility.
    - **Risk if ignored**: Multiple components could each disclaim responsibility.

### Scope Creep Check (item 3 of the brief)

Spec 068's amendment scope per the prompt was: (a) replace XVI's first bullet with a 3-stage breakdown, and (b) append a "Clarification (v2.3.2): determinism scope" paragraph. The candidate at L457-476 and L491-498 implements exactly that — no new bullets were added, the second/third/fourth bullets of XVI (L477-489) appear unchanged from prior versions, and no other principles were touched in v2.3.2 (the Sync Impact Report at L1-21 only describes v2.3.1's XV change; v2.3.2 has no Sync Impact Report at all — see internal-contradiction note below). **No scope creep detected.** However, the absence of a v2.3.2 Sync Impact Report is itself a documentation gap: the version footer at L900 says "Last Amended: 2026-04-26" and the version is 2.3.2, but the top-of-file Sync Impact Report still describes only v2.3.1. This is not scope creep but it is a precision problem in the amendment's metadata.

### Internal Contradiction Check (item 4 of the brief)

Within Principle XVI itself, after the v2.3.2 fix:

- **L466 vs L491-493**: stage 2 says "Cross-run variance is acceptable; within-run variance is prohibited." The clarification re-states this as "within-run determinism for the assembled objective function and cross-run reproducibility once parameters are pinned." These are *almost* the same claim, but stage 2 is about parameter values and the clarification is about the assembled function. The candidate does not explicitly say that cross-run reproducibility of the function does NOT require cross-run reproducibility of the parameters — a careful reader can derive it from stage 3's "given a fully-pinned parameter set" precondition, but the principle could state it directly.

- **L463 ("pinned per deliberation run") vs L466 ("Repeating a deliberation … does NOT re-call the LLM")**: these are consistent with each other but jointly imply that "deliberation" and "deliberation run" are the same thing. If a "deliberation" is multi-run (e.g., a deliberation comprises many runs), the second sentence becomes false. Recommend tightening to use one term consistently.

- **No hard contradiction within XVI** in the strict sense — the post-fix text is internally consistent if "deliberation run" is defined and the descriptive prose is read charitably. The harder contradiction is between XVI and VII (covered in Off-Base #2 and Recommendation #3).

### Referenced Documentation

- `CONSTITUTION-v2.3.2-candidate.md` — sections/lines cited:
  - Sync Impact Report header: L1-21 (v2.3.1 metadata; no v2.3.2 metadata present)
  - Principle VII: L162-174 (cross-reference for the determinism contradiction)
  - Principle XVI title and intro: L448-454
  - 3-stage pipeline (the amendment): L456-476
  - Stage 1 Symbolic parsing: L460-462
  - Stage 2 LLM gap-filling: L462-467
  - Stage 3 Mechanical assembly: L468-470
  - Surrounding XVI bullets (unchanged): L472-489
  - v2.3.2 Clarification paragraph (the appended amendment): L491-498
  - Origin block: L500-503
  - Version footer: L900
