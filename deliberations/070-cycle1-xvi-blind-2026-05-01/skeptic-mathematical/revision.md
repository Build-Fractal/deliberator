Reading through all the provided documents to produce my revision for skeptic-mathematical.

### Recommendation Dispositions

#### Recommendation 1: Unbundle plain-language requirement from Principle XVI

- **Original position**: Remove requirement 3 (plain-language output pairing) from Principle XVI entirely and relocate it to AGENTS.md as a plugin authoring guideline, on the grounds that it fails the Governance Criterion 2 (falsifiable scope) gate.
- **Disposition**: Modified
- **Explanation**:

The cross-review of my work (skeptic-cross-principle's cross-reviews, "Dangerous Contradictions — Plain-language requirement — Remove vs. Fix-in-Place") correctly identifies that my removal recommendation and skeptic-cross-principle's in-place patch are mutually exclusive execution paths: if both are applied, the constitution simultaneously treats non-conforming plain-language output as an invalid-plugin signal under XV while AGENTS.md treats the same requirement as non-normative authoring guidance.

The cross-review's suggested resolution is: "the in-place patch is an acceptable interim state IF AND ONLY IF a minimum-sufficiency test is written that makes the requirement falsifiable; absent that test, the excision proceeds." I find this framing correct. The upstream question — can a minimum-sufficiency test be written that makes "plain-language explanation" mechanically evaluable without reviewer interpretation? — is logically prior to the location question.

My cross-review of skeptic-cross-principle ("Dangerous Contradictions — Plain-language requirement: excise vs. patch-in-place") already concluded: "Until that test exists, skeptic-mathematical's excision is the safer constitutional move." I maintain this conclusion but convert it from a categorical recommendation to a conditional one.

**Modified version**: Remove requirement 3 from Principle XVI's headline and body UNLESS skeptic-cross-principle or the synthesis can produce a concrete minimum-sufficiency test — stated in one or two falsifiable sentences — that makes "adequate plain-language explanation" mechanically evaluable without interpretation. The test must resolve ambiguities like: is "Equilibrium quality: 0.87" a violation? Is "above average convergence" sufficient? If the test cannot be written, excision proceeds as originally recommended. If the test can be written and is adopted, the in-place patch survives contingent on also resolving the XVI/XV composition gap explicitly (as Recommendation 1 in my cross-review of skeptic-cross-principle specifies). In either case, the receiving context (whether AGENTS.md or a revised XVI bullet) must explicitly state what runtime behavior follows when a plugin emits non-conforming output: XV's warning-and-continue semantics apply, core deliberation is not blocked, and non-conforming output is preserved with a warning.

The modification preserves the core value — the Criterion 2 failure is real and must be addressed — while acknowledging the cross-review's legitimate point that the patch path is viable if and only if falsifiability can be achieved.

---

#### Recommendation 2: Scope headline "byte-identical" claim explicitly

- **Original position**: Amend the headline to add scoping conditions: "within a deliberation run, given a fully-pinned parameter set."
- **Disposition**: Surviving
- **Explanation**:

The cross-review of my work identifies this as a safe agreement under "Headline 'byte-identical on every assembly' overpromises": "While cross-principle does not make this a standalone recommendation (mathematical does, as rec 2), both reviews are structured around the same structural observation." The cross-review explicitly endorses the proposed fix: "the synthesis should adopt mathematical's rec 2 as the action item."

No challenge was raised. The cross-review's analysis of the carve-out corroborates the diagnosis: the Clarification v2.3.2 is doing scoping work the headline should have done. A misleading headline in a specification consumed as execution truth by agents is a functional bug, not a presentational issue. The fix is minimal and uncontroversial.

---

#### Recommendation 3: Add atomicity requirement for GapFiller.fill() partial failures

- **Original position**: Add an explicit clause requiring that if `GapFiller.fill()` fails before returning, any partial results MUST NOT be persisted to `objective.yml`, and the run orchestrator MUST treat the failure as requiring a fresh invocation of `fill()`.
- **Disposition**: Surviving
- **Explanation**:

The cross-review of my work ("Tensions — GapFiller.fill() partial failure: unaddressed by both but framed differently") explicitly distinguishes this from skeptic-cross-principle's XVI/XV resolution: "Skeptic-cross-principle's proposed XVI text...applies XV semantics to plugin output. Skeptic-mathematical's atomicity requirement applies to the gap-filling stage (stage 2), which is not a plugin. The two fixes target different system components, but skeptic-cross-principle's XV-import framing could mislead a reader into thinking the XV resolution covers gap-filling failures as well. It does not — gap-filling is core execution, not plugin execution."

The cross-review's suggested coordination: "The synthesis should explicitly scope the XV resolution to plugin output and add skeptic-mathematical's atomicity requirement for stage-2 as a separate, independent fix." This is agreement on both the substance and the scope distinction.

The gap is structurally real: the current text requires all parameter values to be "pinned together once `fill()` returns" but is silent on what a partial return means. Without the atomicity clause, implementors must either violate the no-re-invocation rule (correct behavior, letter violation) or honor the rule and ship a broken retry path. Both outcomes are worse than explicit text.

---

#### Recommendation 4: Reconcile two organizational frameworks

- **Original position**: Restructure the headline to explicitly reference the pipeline, making the stage-to-requirement mapping explicit, with "two invariants across its three stages" as the headline framing.
- **Disposition**: Modified
- **Explanation**:

The cross-review of my work ("Dangerous Contradictions — Stage-3 in restructured XVI — Keep as headline invariant vs. Collapse into VII+VIII cross-reference") correctly identifies that my restructured headline is mutually exclusive with skeptic-cross-principle's option (b) for stage-3: if stage-3 is dissolved into a cross-reference to VII+VIII, the restructured headline's reference to a stage-3 invariant becomes incoherent — it references a stage whose normative content no longer lives in XVI.

In my own cross-review of skeptic-cross-principle ("Dangerous Contradictions — Stage-3 determinism: keep in XVI vs. dissolve into VII+VIII"), I concluded: "The Criterion 3 question is logically prior; both reviewers should defer the structural reorganization until it is answered." That conclusion applies with equal force to my own Recommendation 4.

The cross-review's suggested resolution: "the synthesis should adopt option (a) — which both adds the Criterion 1 verification artifact cross-principle requires and preserves the stage-3 structural claim mathematical's headline restructuring needs." Both reviews identify as a safe agreement that "stage-3 deterministic assembly is a composition of VII and VIII, not an independent normative requirement" — the question is whether the headline names it anyway for pipeline completeness or omits it as non-independent.

**Modified version**: Restructure the headline conditionally on the Criterion 3 analysis outcome. If stage-3 survives the analysis as contributing an independently verifiable claim (e.g., a named contract test that tests something VII+VIII do not independently require), restructure the headline to: "conversus's optimization pipeline MUST satisfy two invariants across its three stages: (1) **parameter pinning** — the LLM gap-filling stage (stage 2) produces values that are persisted and not re-resolved within a deliberation run; (2) **shape determinism** — the deterministic assembly stage (stage 3) produces byte-identical output given a fully-pinned parameter set within a deliberation run." If stage-3 is instead reduced to a VII+VIII cross-reference, reduce the headline to enumerate one invariant (parameter pinning) with a note that stage-3 applies Principles VII and VIII and introduces no independent normative requirement. In either case, make the stage-to-requirement mapping explicit in the headline framing to eliminate the dual-taxonomy confusion. Stage-1 (symbolic parsing) should be acknowledged as deterministic-by-construction in the body without being elevated to a separate headline invariant.

---

#### Recommendation 5: Distinguish shipped enforcement from planned enforcement

- **Original position**: Replace "is required" with "is pending (tracked in spec 014 follow-up)" and add explicit notice that enforcement depends on code review and manual verification until the contract test ships.
- **Disposition**: Modified
- **Explanation**:

The cross-review of my work ("Dangerous Contradictions — Enforcement language: soften the MUST vs. add a verification artifact") correctly identifies that my softening recommendation and skeptic-cross-principle's artifact-addition recommendation are not alternatives — they are sequential: "skeptic-mathematical's softening is the correct interim state (before the artifact ships); skeptic-cross-principle's artifact addition is the correct final state (after the artifact ships)."

The cross-review's suggested resolution: "Implement skeptic-mathematical's language change now with a clear 'WHEN this lint exists, remove the pending qualifier' note. Skeptic-cross-principle's verification artifact recommendation becomes the trigger condition for reverting the softened language — not an alternative to it."

This is correct. My original recommendation addressed the interim state (acknowledge the gap) without specifying the exit condition. The cross-review makes the sequencing explicit in a way my original recommendation did not.

**Modified version**: Apply two changes simultaneously. First (interim state): Replace "is required" with "is pending (tracked in spec 014 follow-up)" and add: "Until the contract test ships, enforcement of the pinning discipline depends on code review and manual verification; do not assume the test exists." Second (exit condition): Add a conditional marker: "When the stage-2 contract test reproducing the re-resolution failure pattern ships, restore 'is required' and remove this notice." The safe agreement that "enforcement is aspirational, not operational" confirms both changes are warranted; the cross-review's sequencing framing improves my original recommendation without contradicting it.

---

#### Recommendation 6: Add explicit template registry stability requirement

- **Original position**: Add a MUST clause requiring the template registry to be treated as immutable for the duration of a deliberation run, with plugin reloads or registry updates prohibited from taking effect mid-run.
- **Disposition**: Surviving
- **Explanation**:

The cross-review of my work ("Tensions — Template registry stability: silent dependency vs. unacknowledged gap") confirms the diagnosis: "skeptic-cross-principle's scoping fix for the headline...narrows the byte-identical claim but does not close the silent dependency gap. A plugin hot-reload during a run would still violate byte-identity under the scoped claim without violating any stated prohibition, which is exactly the gap skeptic-mathematical identifies."

The cross-review's coordination guidance: "The headline scoping fix (skeptic-cross-principle) and the registry stability requirement (skeptic-mathematical) are complementary, not competing. Both should be adopted. The synthesis should present them as two components of one fix: scope the headline correctly AND make the implied registry stability requirement explicit."

This is agreement on the substance. The cross-review further notes: "Mathematical's rec 6 (template registry stability) is a precondition for the behavioral guarantees cross-principle's contract test recommendations are designed to verify." This strengthens the case — without explicit registry stability, the contract tests cross-principle recommends for stage-3 become unreliable, since a correctly-pinned parameter could produce different output if the template changed between assemblies within a run.

---

#### Recommendation 7: Address version-boundary edge case for deliberation run definition

- **Original position**: Add a clause specifying what happens when `conversus` is upgraded mid-run: either complete using the pre-upgrade binary, abort and require fresh invocation, or prohibit resuming a pre-upgrade `objective.yml` with a post-upgrade binary.
- **Disposition**: Surviving
- **Explanation**:

No cross-review challenged this recommendation. Both the cross-review of my work and my cross-review of skeptic-cross-principle are silent on the version-boundary edge case. The recommendation remains a P3 item — low probability, but the failure mode (mid-run upgrade creating an ambiguous version context) is difficult to debug, and the principle's "deliberation run" definition explicitly places cross-version replay out of scope without addressing the in-progress case.

The gap is genuinely an unstated-dependency problem of the kind Principle X warns against ("errors should never pass silently"). The recommendation is narrow and specific enough to flag a hypothetical violating PR — an implementation that resumes a pre-upgrade `objective.yml` with a post-upgrade binary — without requiring interpretation. It satisfies the Governance Criterion 2 standard that motivated the principle's more significant gaps, which means it belongs in the constitution's text rather than in operational guidance.

---

### New Recommendations

- **Specify receiving-document semantics for plain-language migration** (Priority: P1)
  - **Triggered by**: The cross-review of my work ("Dangerous Contradictions — Plain-language requirement — Remove vs. Fix-in-Place") identifies that the XVI/XV composition gap — what happens at runtime when a plugin emits non-conforming plain-language output — does not disappear when the requirement moves to AGENTS.md. My original removal recommendation was silent on this. The cross-review's safe agreement section ("XVI/XV composition creates an unresolved and dangerous behavioral ambiguity") further confirms the composition gap is independent of the location question.
  - **Proposed change**: Whether plain-language pairing ends up removed from XVI (my modified Rec 1 default path) or retained in XVI with an in-place patch (the conditional path), the following clause must appear somewhere in the authoritative specification: "A plugin that emits numerical output without a conforming plain-language explanation is treated as non-conforming plugin output under Principle XV: the output is preserved with a warning and core deliberation continues. Non-conforming plain-language output DOES NOT block core execution." If plain-language moves to AGENTS.md, this clause belongs in the AGENTS.md plugin authoring section as a runtime behavior declaration. If it stays in XVI, it resolves the composition gap in-place. The clause itself is not new — it was proposed by skeptic-cross-principle — but it needs to be anchored regardless of the location decision.
  - **Rationale**: The safe agreement in both reviews is that XVI's MUST language and XV's warning-and-continue model produce contradictory behavioral contracts for the same triggering event. That contradiction does not resolve itself by moving the requirement to AGENTS.md — it only changes which document contains the contradiction. The runtime behavior must be specified explicitly wherever the requirement lives. My original Rec 1 focused on the constitutional location question and neglected the runtime-semantics question; this new recommendation closes that gap.

- **Conditional stage-3 Criterion 3 analysis as prerequisite** (Priority: P2)
  - **Triggered by**: The cross-review of my work ("Dangerous Contradictions — Stage-3 in restructured XVI") and my own cross-review of skeptic-cross-principle ("Dangerous Contradictions — Stage-3 determinism: keep in XVI vs. dissolve into VII+VIII"). Both identify that the structural reorganization in my Rec 4 and the stage-3 dissolution option in skeptic-cross-principle's Rec 2 are mutually exclusive paths whose correct resolution depends on the Criterion 3 analysis outcome — a prerequisite question neither review answered definitively.
  - **Proposed change**: The synthesis should commission or perform the Criterion 3 analysis for stage-3 deterministic assembly before applying Rec 4's structural reorganization. The analysis should answer: does stage-3's bit-identical assembly claim produce a verifiable assertion that is not already implied by composing Principle VII (same inputs → structurally identical output) with Principle VIII (mechanical template-driven behavior)? If the analysis finds no independent contribution, record stage-3 in the SIR as a VII+VIII composition (per the safe agreement in both reviews) and reduce Rec 4's restructuring accordingly. If the analysis finds an independent verifiable contribution — such as a contract test covering assembly behavior that VII+VIII leave underspecified — retain stage-3 as a named invariant in the headline.
  - **Rationale**: Both reviews independently reached the safe agreement that stage-3 "is a composition of VII and VIII, not an independent normative requirement" — but both also acknowledge that if a stage-3-specific verification artifact can be named, the argument changes. The synthesis cannot consistently apply both Rec 4 (keep stage-3) and skeptic-cross-principle's option (b) (dissolve stage-3); the Criterion 3 analysis is the only path through the contradiction that doesn't require one review to yield entirely on the merits.

---

### Position Summary

I withdrew no recommendations outright. I modified four (Recs 1, 4, 5, and implicitly the framing of Rec 3's scope relative to the XV resolution). Three recommendations survive unchanged (Recs 2, 6, 7). I added two new recommendations: one specifying runtime-semantics for plain-language output wherever the requirement lands (closing a gap my original Rec 1 neglected), and one framing the stage-3 Criterion 3 analysis as a prerequisite for the structural reorganization in Rec 4.

The most significant change in my thinking was prompted by the cross-review's handling of the plain-language contradiction. My original Rec 1 was categorical — excise the requirement — and did not acknowledge that the XVI/XV composition gap persists regardless of location. The cross-review correctly identified that removing the requirement from XVI without specifying runtime behavior in the receiving document leaves the behavioral ambiguity unresolved. The modification converts my categorical excision into a conditional: the excision proceeds unless a falsifiable minimum-sufficiency test can be written, and in either case the runtime semantics must be explicitly specified. This is a more honest position because it acknowledges the location question and the semantics question are separable problems.

My remaining highest-priority recommendation is the modified Rec 1 combined with the new receiving-document semantics recommendation. The plain-language requirement fails the constitution's own Criterion 2 gate — this is a safe agreement confirmed by both reviews independently — and the XVI/XV composition gap means the failure has runtime consequences, not just editorial ones. These two changes together (resolve the location question via the falsifiability test, specify runtime semantics wherever the requirement lands) address the most structurally dangerous gap in Principle XVI: an unenforceable MUST with contradictory failure semantics that agents consuming the constitution as execution truth cannot resolve without interpretation.