# Review: Devil's Advocate — 007-subcommand-dispatch-define (Round 2)

**Reviewer**: devils-advocate
**Round**: 2 of 2
**Basis**: spec.md, SKILL.md, Round 1 synthesis (final.md), Round 1 arbitration (resolution.md)
**Date**: 2026-03-22

---

## Executive Summary

The Round 1 deliberation produced strong consensus on functional requirements (all 12 FRs implemented correctly), backward compatibility, and several P1 improvements (post-write schema validation, `--context` path validation, explicit dispatch matching). I do not contest any convergence points from Round 1 (C-1 through C-13). Those concessions stand.

Round 1 also surfaced five disputes, three of which I consider architecturally load-bearing. The arbiter's resolution provides useful perspective on all five, and I engage with each opinion below. I accept the arbiter's framing on three of the five disputes (RD-1, RD-3, RD-4) while maintaining refined positions on two (RD-2 and RD-5). I also identify two missed opportunities that Round 1 did not adequately address.

The core tension this review presses is the same one I pressed in Round 1, now sharpened by the arbiter's own acknowledgment of it: spec 007 simultaneously declares itself foundational and scoped. The synthesis named this as systemic contradiction SC-1. The arbiter called it "real but manageable" and proposed the `## Status` section and validation contract as the "minimal bridge" between these two identities. I agree with the arbiter that the bridge is necessary. My remaining disputes concern whether the proposed bridge is load-bearing enough for the weight it will carry.

---

## Alignment

### Convergence Honored — No Reversals

I affirm all Round 1 convergence points without reversal. Specifically:

- **C-1 (Post-write schema validation, P1)**: The define handler validates all 7 headings after writing. If any heading is missing, it adds a `[CLARIFY:]` placeholder and re-writes. This is the single most important structural addition to spec 007. No dispute.

- **C-2 (`--context` path validation, P1)**: Fail with clear error on non-existent path, warn on directory with no `.md` files. Mirrors the `run` handler's validation at SKILL.md L195-196. No dispute.

- **C-3 (Dispatch matching exact and case-sensitive, P1)**: Fallback-to-`run` is dead. Exact matching with exhaustive dispatch table. The error message enhancement ("Did you mean: `/conversus run {cmd}`?") is a good UX addition. No dispute.

- **C-4 through C-13**: All consensus items at P2 and P3 are accepted. Particular note: I continue to accept the version-scoped wording for single-agent execution (C-4), the four-rule refine contract as the structural minimum (C-6), the taxonomy closure language (C-8), and the single-sentence pipeline overview (C-9).

### Concessions from Round 1 That Stand

1. I withdrew consumer-side gate enforcement in favor of producer-side `## Status` field. This concession stands.
2. I adopted content hash over modification timestamp for staleness tracking. This concession stands.
3. I fixed the taxonomy closure self-contradiction. This concession stands.
4. I accepted integration-architect's four-rule refine contract as the structural minimum. This concession stands.
5. I accepted the `--type` override flag withdrawal. This concession stands.

### Disputes Where I Accept the Arbiter's Position

**RD-3 (Multi-path `--context`)**: I accept deferral. The arbiter's grounding is persuasive: SKILL.md L797's directory support is the designed multi-source mechanism, not a workaround. The arbiter also correctly identifies ordering, deduplication, and conflict resolution as non-trivial interaction semantics that multi-path introduces without FR guidance. My Round 1 position that the implementation cost is "trivial" understated the specification cost. I still want the limitation documented as a scoping decision rather than the permanent design (Change 11 in the synthesis), and I accept that this documentation is sufficient for spec 007.

**RD-4 (`--force` and `--dry-run`)**: I accept deferral. The arbiter's analysis of the non-expert user principle (spec.md L87) is convincing: every flag is a decision the user must understand or ignore, and for the target audience, fewer flags is better. The documentation note acknowledging future need (Change 13 in the synthesis) is the appropriate compromise. I withdraw my P2 priority for these flags within spec 007.

---

## Missed Opportunities

### MO-1: The Report Section (SKILL.md L856-875) Has No Failure Mode

The define handler's Report section (SKILL.md L856-875) describes what to print after *successfully* writing `problem.md`. It does not specify what happens when writing fails. Consider: the output directory is on a read-only filesystem, or disk is full, or permissions are insufficient. The handler has no defined error behavior for write failure.

This is not a theoretical concern. The `run` handler has implicit write failure handling because it uses the Agent tool (which surfaces errors to the orchestrator). The `define` handler writes directly. If the write fails silently (e.g., the agent calls Write and gets an error it does not check), the Report section runs against a non-existent artifact, printing a path to a file that does not exist.

**Recommendation**: Add a write-failure error specification to the Output section: "If writing `problem.md` fails, report the error to the user and do not print the success report. Do not attempt to recover silently." This is a one-sentence addition that closes an unguarded path.

**Priority**: P2. Not as critical as the P1 changes (post-write validation, path validation, dispatch matching), but a real gap that no Round 1 reviewer identified.

### MO-2: Interactive Mode (FR-012) Has No Termination Contract

FR-012 specifies that the define handler asks three clarifying questions when invoked with no description and no `--context`. SKILL.md L779-782 implements this. But there is no specification for what happens if the user provides no answers, provides empty answers, or explicitly declines to answer ("I don't know yet").

For the non-expert audience spec 007 targets, this matters. A user who types `/conversus define` and responds to "What decision are you facing?" with "I'm not sure" should not get a `problem.md` full of hallucinated content. The handler should produce a `problem.md` where every section contains a `[CLARIFY:]` tag -- which is arguably the correct behavior given the post-write validation convergence (C-1), but neither the spec nor SKILL.md states this explicitly.

**Recommendation**: Add to the Interactive input section (SKILL.md L779-782): "If the user provides vague or empty responses, the resulting `problem.md` should contain `[CLARIFY:]` tags for all sections that cannot be confidently determined. The ambiguity handling rule (SKILL.md L852) applies to interactive input equally." This is consistent with the existing design but makes the behavior explicit for an edge case the non-expert user will hit.

**Priority**: P2. The existing ambiguity handling rule (SKILL.md L852) arguably covers this implicitly, but explicit coverage for the interactive path prevents an agent from interpreting "no input" as license to generate speculative content.

---

## Off-Base Assumptions

### OBA-1: The Arbiter's "Factual Annotation" Framing for `## Status` Is Correct but Incomplete

The arbiter reframes the `## Status` dispute (RD-1) by arguing the field is neither advisory nor binding -- it is *descriptive*. The field states a measurable property (count of `[CLARIFY:]` tags) and the define handler already computes this count (SKILL.md L865). The arbiter's argument: writing it into the artifact costs nothing, helps the non-expert user, and leaves enforcement to spec 008.

I accept this framing for the `## Status` section itself. The arbiter is right that the deliberation spent energy debating advisory-vs-binding when the field is simply a fact about the artifact. I withdraw my Round 1 demand for RFC 2119 SHOULD language prescribing consumer behavior. The arbiter's reasoning -- "spec 007 need not have an opinion on" what consumers do with the status -- is consistent with the boundary principle functional-typing defended, and I accept it.

However, this framing only resolves the *field* dispute. It does not resolve the *user experience* dispute I raised in Round 1. The concern was never really about whether the field exists. It was about whether the guided workflow has any quality checkpoint between `define` and `interests`. If `## Status: draft` is a fact that nothing acts on, the non-expert user still runs `/conversus interests` on an incomplete `problem.md` and gets low-quality output. The arbiter punts this to spec 008: "Whether spec 008 treats `draft` status as blocking is spec 008's decision."

I accept the punt. But I note for the record that spec 008 now inherits a design obligation that spec 007 chose not to address. If spec 008's review does not mandate checking the status field, the entire `[CLARIFY:]` system -- tags, warnings, status section -- is structural decoration with no operational effect. The arbiter acknowledges this implicitly in Point 5 of the "Considerations for Next Round" section: the `## Status` section is described as the "minimal bridge" between spec 007's dual identities. A bridge that nothing walks across is not a bridge.

**This is not a reversal of my concession.** I accept the `## Status` section as a factual annotation in spec 007. I accept that spec 007 does not prescribe consumer behavior. I flag, as a design risk, that the quality checkpoint this system was designed to provide does not exist until spec 008 explicitly implements it -- and that "spec 008 will handle it" is an assumption, not a guarantee.

### OBA-2: The "Prose Validation Contract" Is Weaker Than It Appears

The arbiter's position on RD-2 proposes a one-sentence prose validation contract alongside the `problem.md` schema: "After writing `problem.md`, validate that all required headings exist. Any command that reads `problem.md` as input should apply the same heading check before processing."

The arbiter argues this is "strictly better than silence" and "strictly less than a mandated shared function." Both claims are true. But the arbiter also claims this "acknowledges devils-advocate's post-mutation threat model with a forward-looking contract." This overstates the contract's strength.

A prose statement that says "should apply the same heading check" is a comment, not a contract. It has no enforcement mechanism. It is not referenced by any consumer. It does not define the validation operation precisely enough that two independent spec authors would implement the same check. "All required headings exist" -- does that mean the heading text must match exactly? Does `## constraints` (lowercase) satisfy `## Constraints`? Does a heading with no content beneath it count as present?

I am not re-litigating whether a shared validation function should be mandated in spec 007. The Round 1 consensus (and the arbiter's position) is that a function is premature for one producer and zero consumers. I accept that.

What I am arguing is that the prose contract must be precise enough to be implementable. The current formulation ("validate that all required headings exist") is ambiguous in at least three ways: case sensitivity of heading text, content-beneath-heading requirements, and heading-level flexibility (is `### Decision` acceptable where `## Decision` is specified?).

**Recommendation**: Tighten the validation contract prose to: "Validate that `problem.md` contains all 7 required headings (`## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`) at heading level 2 beneath a `# Problem Definition` level-1 heading. Headings are matched case-sensitively. A heading with no content beneath it (only whitespace before the next heading) is present but empty -- apply `[CLARIFY:]` handling per the ambiguity rule." This is still prose, not code. But it is precise enough that two independent implementations would produce the same result.

**Priority**: P1 amendment to the existing post-write validation convergence (C-1). This is not a new recommendation -- it is a precision refinement of the consensus change.

### OBA-3: Per-Handler Validation Is Accepted -- the Architecture Note Should Be Concrete

The arbiter sides with integration-architect on RD-2: define the validation contract at the schema layer, not the dispatch layer. Functional-typing is correct that routing and validation are separate concerns. I accept all of this. My Round 1 proposal for a "Common Handler Utilities" subsection in the dispatch section was architecturally misplaced, and I withdraw it.

But the synthesis proposes Change 14 (P3) as the architectural note: "Future commands that consume this artifact should apply the same heading validation at read time. See this validation as a shared contract, not a handler-specific check." This is the right sentiment at the wrong priority. If the validation contract is important enough to define (everyone agrees it is), the note pointing future spec authors to it should be at the same priority as the contract itself -- P1, not P3.

I am not arguing for a higher implementation burden. The change is still one sentence of prose. I am arguing that the sentence matters enough to not be tagged P3-optional. When the spec 008 author reads spec 007 looking for integration contracts, a P3 note is easy to skip. A P1 note adjacent to the schema is not.

**Recommendation**: Elevate Change 14 from P3 to P2 and place it directly after the post-write validation text (Change 1), not in a separate location. The two form a single contract: "The define handler validates headings after writing. Any command that reads `problem.md` should apply the same check."

**Priority**: P2 (elevated from P3).

---

## Actionable Recommendations

### Rec-1: Accept `## Status` as factual annotation, no consumer prescriptions (revised from Round 1 Rec #1)

Accept the arbiter's framing. The `## Status` section is a factual declaration of completeness. The define handler sets `draft` when `[CLARIFY:]` tags exist, `ready` when none exist. No RFC 2119 language about downstream behavior. Spec 008 decides how to use the field.

**Priority**: P1 (unchanged).
**Change from Round 1**: Withdrew SHOULD language. Accepted arbiter's descriptive framing.
**Traced to**: Arbiter opinion on RD-1, synthesis Change 10, integration-architect revision New Rec #1.

### Rec-2: Tighten the validation contract prose to specify case-sensitive heading-level-2 matching (new precision)

The post-write validation convergence (C-1) should specify: headings are `##`-level, case-sensitive, matched by exact text. A heading with no content is present but triggers `[CLARIFY:]` handling. This eliminates three ambiguities in the current formulation.

**Priority**: P1 (precision amendment to existing C-1 consensus).
**Traced to**: Synthesis Change 1, arbiter opinion on RD-2.

### Rec-3: Add write-failure error specification to the define handler (new)

The Output section should specify: "If writing `problem.md` fails, report the error to the user and do not print the success report." One sentence. Closes an unguarded path.

**Priority**: P2.
**Traced to**: MO-1 above.

### Rec-4: Specify interactive-mode behavior for vague or empty input (new)

The Interactive input section should specify: vague or empty responses produce `[CLARIFY:]` tags, not hallucinated content. Consistent with SKILL.md L852 ambiguity handling but needs explicit statement for the interactive path.

**Priority**: P2.
**Traced to**: MO-2 above.

### Rec-5: Elevate the architectural validation note from P3 to P2 and co-locate with the schema contract (revised from Round 1 New Rec #1)

The note that future consumers should apply the same heading validation is the second half of a single contract. It should be at P2, placed adjacent to the post-write validation text, not in a separate P3 section.

**Priority**: P2 (elevated from Round 1 position of P2 for a different mechanism).
**Change from Round 1**: Withdrew "Common Handler Utilities" dispatch-layer proposal. Accepted schema-layer placement. Argument now is about priority of the cross-reference note, not about where validation lives.
**Traced to**: Synthesis Change 14, arbiter opinion on RD-2.

### Rec-6: Accept deferral of multi-path `--context` (revised from Round 1 Rec #5)

Accept the 2-1 majority and arbiter opinion. Single-path is a scoping decision, documented as such. Multi-path deferred to a follow-up spec.

**Priority**: Withdrawn from spec 007 scope. Documentation of limitation at P3 (Change 11 in synthesis).
**Change from Round 1**: Reversed position. Accepted deferral.
**Traced to**: Arbiter opinion on RD-3, synthesis RD-3 assessment.

### Rec-7: Accept deferral of `--force` and `--dry-run` flags (revised from Round 1 Rec #6)

Accept the 2-1 majority and arbiter opinion. Documentation note acknowledging future need is sufficient.

**Priority**: Withdrawn from spec 007 scope. Documentation note at P3 (Change 13 in synthesis).
**Change from Round 1**: Reversed position. Accepted deferral.
**Traced to**: Arbiter opinion on RD-4, synthesis RD-4 assessment.

### Rec-8: Adopt the four-rule refine contract; diff summary as recommended practice (revised from Round 1 Dispute #5)

Accept integration-architect's four rules as normative: (a) all headings preserved, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated. The diff summary is recommended practice ("should" lowercase), not a structural requirement. The arbiter's reasoning is sound: the post-conditions define what the output must satisfy; the summary describes how the operation is reported. These are different concerns.

**Priority**: P2 (unchanged).
**Change from Round 1**: Accepted arbiter's distinction between normative post-conditions and UX guidance. Diff summary downgraded from structural requirement to recommended practice.
**Traced to**: Arbiter opinion on RD-5, synthesis Change 7.

---

## Referenced Documentation

| Document | Location | Relevance |
|----------|----------|-----------|
| Spec 007 | `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/spec.md` | Target specification. All FRs, success criteria, and constraints. |
| SKILL.md | `<HOME>/code/payer-index-mono/conversus/SKILL.md` | Implementation. Dispatch table (L18-34), define handler (L769-876), schema (L822-850), run handler path validation (L195-196), engine validation patterns (L286-295, L659-676). |
| Round 1 synthesis | `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/summary/final.md` | Neutral synthesis of all Round 1 positions. Convergence C-1 through C-13, disputes RD-1 through RD-5, systemic contradictions SC-1 and SC-2. |
| Round 1 arbitration | `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/arbitration/resolution.md` | Arbiter advisory opinions on all 5 disputes. Decision framework, grounding citations, confidence assessments. |
| Round 1 devils-advocate disputes | `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/devils-advocate/disputes.md` | My Round 1 final positions on all 5 disputes and 10 convergence points. |
| Round 1 devils-advocate revision | `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/devils-advocate/revision.md` | My Round 1 recommendation dispositions, including all concessions and maintained positions. |
