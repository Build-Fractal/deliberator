# Cross-Review: devils-advocate reviewing integration-architect (Round 2)

**Cross-reviewer**: devils-advocate
**Reviewing**: integration-architect Round 2
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: The "Factual Annotation" Framing Neutralizes the Very Problem It Claims to Solve

Integration-architect adopts the arbiter's "factual annotation" framing for `## Status` with enthusiasm, calling it a resolution that "sidesteps" the advisory-vs-gate debate. The review states: "The field is not advisory (it does not suggest; it states). It is not a gate (it does not block; it describes). It is a fact."

This is a semantic maneuver, not a resolution. Integration-architect simultaneously argues (a) the `## Status` field helps non-expert users because they can see "Status: draft -- 3 items need clarification" in their editor, and (b) the field prescribes nothing about what anyone should do with that information. These claims are in tension.

If the field is purely descriptive and no consumer is obligated to check it, what exactly does it help the non-expert user *do*? The user sees "draft" and then... what? The spec says nothing. The user cannot be expected to know that "draft" means "you should resolve the CLARIFY tags before running /conversus interests" because *nobody has said that anywhere*. Integration-architect explicitly states: "Whether spec 008 treats `draft` as blocking is spec 008's decision."

So the non-expert user -- the person integration-architect invokes as the primary beneficiary (spec.md L87) -- sees a status label with no documented meaning, no documented action to take, and no guarantee that any downstream command will ever care about it. The arbiter called this a "minimal bridge." I called it a bridge that nothing walks across. Integration-architect's enthusiastic adoption of the framing does not change the structural problem: factual annotations that trigger no behavior are metadata, not user experience improvements.

This is dangerous because it creates the appearance of having addressed the quality-checkpoint concern without actually addressing it. If the synthesis adopts this language, spec 008's author may reasonably conclude the checkpoint problem is solved -- after all, the `## Status` field exists, the non-expert user can see it, the define handler reports it. But nothing in spec 007 or spec 008's inheritance chain actually tells anyone what to do about a `draft` status.

**My position is not a reversal.** I accepted the `## Status` field as a factual annotation. I accepted that spec 007 does not prescribe consumer behavior. But integration-architect's review presents this as a clean resolution when it is actually a conscious deferral of the quality checkpoint to spec 008 with no binding obligation on spec 008 to implement it. The synthesis should label it as such: an explicit, accepted gap, not a solved problem.

### DC-2: The Prose Validation Contract Is Declared Sufficient While Its Precision Is Left Undefined

Integration-architect's position on RD-2 adopts the arbiter's one-sentence prose contract: "After writing `problem.md`, validate that all required headings exist. Any command that reads `problem.md` as input should apply the same heading check before processing."

Integration-architect then claims this formulation "resolves the dispute" by satisfying three concerns: my post-edit threat model (forward-looking contract), functional-typing's routing/validation separation (no validation in dispatch), and integration-architect's own centralization concern (contract defined once at the schema level).

But integration-architect does not engage with the ambiguity I raised in my own Round 2 review (OBA-2). "All required headings exist" is ambiguous in at least three ways: case sensitivity of heading text, content-beneath-heading requirements, and heading-level flexibility. Integration-architect declares the prose formulation sufficient without specifying what "the same heading check" means precisely enough that two independent implementers would produce the same check.

This is not an abstract concern. When spec 008's author reads "apply the same heading check," they must decide: does `## constraints` (lowercase) pass? Does an empty heading with no content pass? Does `### Decision` (wrong level) pass? The prose contract does not answer these questions. Integration-architect's review does not acknowledge they need answering.

I raised a concrete precision amendment in my own review (Rec-2): specify heading level 2, case-sensitive exact text matching, and clarify that content-free headings are "present but empty" triggering CLARIFY handling. Integration-architect's review does not address this. The contradiction is claiming the prose contract satisfies the centralization concern while leaving the contract too imprecise for centralized reuse.

---

## Tensions

### T-1: "Deliberate Design" vs. "Scoping Decision" for Single-Path `--context`

Integration-architect's Round 2 position on RD-3 reframes the single-path `--context` constraint from "limitation with workaround" to "deliberate design with a directory-based multi-source mechanism," adopting the arbiter's language. The review recommends documentation that frames this "as a deliberate design choice with a defined multi-source mechanism (directories), not as a limitation to apologize for."

I accepted the deferral and no longer contest it. But the framing matters for downstream spec authors. Calling directory-based aggregation a "deliberate design" implies it was a considered architectural decision with rationale. In reality, SKILL.md L797 says "path may be a file or directory" -- this is a file-resolution convention, not a multi-source architecture. The directory mechanism does not address ordering (alphabetical? user-specified?), does not address conflicts between documents, and does not address deduplication. Integration-architect's own review acknowledges these gaps (inherited from the arbiter's analysis) while simultaneously calling the current behavior a "deliberate design."

The tension is: if the directory mechanism is a deliberate design, it should be specified well enough to be predictable (ordering, scoping rules). If it is a pragmatic convenience pending proper multi-path support, it should be documented as such. Calling it "deliberate design" while acknowledging it lacks the specification that deliberate designs require creates ambiguity about whether a follow-up spec needs to redesign multi-source or merely add syntactic sugar on top of a sound foundation.

I would prefer the documentation say: "Single-path is a scoping decision for spec 007. Directory support provides a pragmatic multi-source mechanism. A follow-up spec may introduce multi-path syntax with explicit ordering and conflict semantics." This is factually accurate without either apologizing or overclaiming.

### T-2: MO-1 (Idempotency on Ready problem.md) Overlaps With, But Does Not Acknowledge, My MO-2

Integration-architect's MO-1 asks what happens when a user runs `/conversus define` against a `problem.md` that is already `status: ready` with zero CLARIFY tags. This is a real gap. But it overlaps substantially with my MO-2 (interactive mode termination contract for vague/empty input) -- both concern the define handler's behavior at the boundaries of meaningful input. Integration-architect's MO-1 is the "too complete" boundary; my MO-2 is the "too vague" boundary.

The tension is not that these are contradictory -- they are complementary. The tension is that integration-architect raises one boundary condition without acknowledging the other, and vice versa in my review. The synthesis should treat both as facets of a single gap: the define handler's behavior when input does not clearly motivate a write operation (either because the artifact is already complete or because the input is too vague to produce meaningful content). Both should be at the same priority.

### T-3: The Four-Rule Refine Contract and the Diff Summary Occupy an Uncomfortable Middle Ground

Integration-architect maintains the four-rule refine contract as normative and the diff summary as recommended practice, adopting the arbiter's distinction. The review argues: "The four rules define what the output must satisfy -- they are testable post-conditions a downstream consumer can depend on. The diff summary describes how the operation is reported -- it is a UX concern that varies by context."

I accepted this distinction in my own review (Rec-8). But integration-architect's "testable post-conditions" claim deserves scrutiny. Rule (d), "Type re-evaluated," is not testable in the same way as rules (a), (b), and (c). Rules (a) through (c) are structural checks: headings are present, content was not silently deleted, Source Documents are unioned. These can be verified by diffing the before and after artifacts. Rule (d) is a process obligation: the handler must *consider* whether the type should change. This is not observable from the output alone -- if the type does not change, there is no way to verify whether the handler re-evaluated or simply copied. A post-condition that cannot be falsified from the artifact is not a testable post-condition; it is a guideline.

This does not change my acceptance of the four-rule contract. But integration-architect should acknowledge that rules (a)-(c) and rule (d) are different kinds of obligations, and the "testable post-conditions" framing applies cleanly only to the first three.

### T-4: R10 Priority Tension -- Accepting Synthesis Priority While Maintaining a Different One

Integration-architect's recommendation table lists R10 (`## Status` section) as: "Maintained P1 from my position; synthesis rates disputed. I accept the synthesis priority assignment while maintaining that the factual-annotation framing should resolve functional-typing's objection."

This is a diplomatic hedge that creates ambiguity. Integration-architect simultaneously accepts the synthesis priority (which rates `## Status` as disputed, not P1 consensus) and maintains a P1 position. For the Round 2 synthesis author, this is difficult to adjudicate: is integration-architect's vote P1 or "whatever the synthesis says"? The review should pick one. Either the `## Status` section is P1 from integration-architect's perspective and they are registering a minority position, or they accept the synthesis priority and their personal conviction is immaterial to the priority assignment. The current formulation tries to have both.

---

## Safe Agreements

### SA-1: All Round 1 Convergence Items (C-1 Through C-13) Survive Round 2

Integration-architect reaffirms all 13 convergence items. I reaffirm all 13 convergence items. The three P1 changes (post-write schema validation, context path validation, dispatch matching semantics) are settled. No reviewer has contested any of these in Round 2. This is the strongest signal in the entire deliberation: the core structural improvements are unambiguous.

### SA-2: All Round 1 Concessions Hold Without Reversal

Integration-architect lists six concessions from Round 1 and confirms none are reversed. I listed five concessions from Round 1 and confirmed none are reversed. Neither reviewer reverses any position conceded in Round 1. The deliberation has been monotonically convergent -- positions only narrow, never widen. This is a healthy process signal.

### SA-3: Multi-Path `--context` and `--force`/`--dry-run` Are Properly Deferred

Integration-architect and I now agree on deferral for both RD-3 and RD-4. The arbiter concurred. This is a 3-0 position (excluding functional-typing, who held the majority position originally). The deferral is grounded in concrete reasoning: multi-path requires interaction semantics (ordering, deduplication, conflict) that no FR addresses; `--force`/`--dry-run` serve automation contexts that spec 007 does not define. Documentation notes (Changes 11 and 13) acknowledge the future need without expanding spec 007's interface. No disagreement remains.

### SA-4: Per-Handler Validation at the Schema Layer, Not the Dispatch Layer

Integration-architect and I agree that validation logic belongs at the schema layer, not in the dispatch section. I withdrew my "Common Handler Utilities" proposal from Round 1. Integration-architect correctly notes that SKILL.md L18-34 (dispatch) should stay minimal. The dispute is resolved: validation is defined alongside the `problem.md` schema. The only remaining tension is the precision of the prose contract (see DC-2 above) and the priority of the forward-looking note (my Rec-5 proposes P2; integration-architect's R14 keeps P3).

### SA-5: Refine Semantics -- Four Rules Normative, Diff Summary Recommended Practice

Integration-architect and I agree on the four-rule contract and the arbiter's distinction between normative post-conditions and UX guidance. The four rules (headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated) are structural requirements. The diff summary is recommended practice. I accepted this in my Rec-8; integration-architect maintains it in RD-5. The only nuance I raise is the testability difference between rules (a)-(c) and rule (d) (see T-3 above), which does not affect the agreement itself.

### SA-6: MO-2 (problem.md vs. conversus.yml Artifact Independence) Is a Valid Documentation Gap

Integration-architect's MO-2 identifies that `problem.md` (guided workflow) and `conversus.yml` (direct execution) coexist in the same directory with no documented interaction. This is a real user-confusion risk, and a single sentence noting their independence is appropriate. I did not raise this in my own review, and I agree it belongs in the spec as a P3 note (integration-architect's R15).

---

## Summary

Integration-architect's Round 2 review is well-structured and makes no reversals. The convergence is real. The two dangerous contradictions I identify are not about wrong positions but about insufficient precision: the `## Status` field is presented as solving a user-experience problem it does not actually solve (DC-1), and the prose validation contract is declared sufficient without engaging with the ambiguity questions that make it insufficient for cross-spec reuse (DC-2). The tensions are secondary -- framing choices that affect downstream interpretation but do not block consensus. The safe agreements cover the vast majority of the deliberation's output.
