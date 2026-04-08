# Cross-Review: devils-advocate on functional-typing (Round 2)

**Reviewer**: devils-advocate
**Reviewing**: functional-typing's Round 2 review
**Round**: 2 of 2
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: Conceding on RD-1 (`## Status`) While Listing Cascading Obligations That Cannot Be Enforced Within Spec 007

Functional-typing concedes on RD-1 and accepts the arbiter's "factual annotation" framing for `## Status`. Then, in MO-1, MO-2, and MO-3, functional-typing identifies three separate downstream obligations created by that concession: the heading count must change from 7 to 8 in all validation references (MO-1), the Status field must be re-evaluated on refine operations (MO-2), and spec.md's schema block must be updated to include `## Status` (MO-3). In Rec #1, functional-typing explicitly states that Change 1 and Change 10 are inconsistent if both are adopted without reconciliation.

This is a concession that generates more work than the original dispute. Functional-typing is simultaneously saying "I concede, the field is simple and zero-cost" (RD-1 revised position) and "but adopting the field breaks the heading count in Change 1, breaks the refine invariants in Change 7, and diverges spec.md from SKILL.md" (MO-1, MO-2, MO-3). The field is not zero-cost. It propagates through every validation and invariant reference in the spec.

The danger: functional-typing's concession on RD-1 is treated as settled, but three MO items are created to patch the consequences. If the synthesizer treats the concession as final and the MO items as optional suggestions, the spec acquires a `## Status` field that is inconsistent with its own validation rules. The concession and its MO items are a single atomic unit -- adopting one without the others produces a spec with internal contradictions (7-heading validation checking an 8-heading schema, refine operations that preserve status from input but never re-evaluate it).

Functional-typing should have conditioned the concession more explicitly: "I concede on `## Status` if and only if Changes 1, 7, and the spec.md schema are simultaneously updated." The current framing -- concede first, then note three MO items at P1/P2/P3 -- risks the concession being accepted while the MO items are deprioritized.

### DC-2: FR Coverage Claimed as "Unchanged from Round 1" Despite Accepting a New Schema Element

Functional-typing's FR coverage verification section states "unchanged from Round 1" and maps all 12 FRs to SKILL.md lines. But functional-typing has just conceded on adding `## Status` to the schema (RD-1). FR-009 (spec.md L38) specifies the required sections of `problem.md`: "Decision (one sentence), Type, Context (2-4 sentences), Constraints (bulleted), Success Criteria, Open Questions, Source Documents." The `## Status` section is not in this FR. It is not in the spec.md schema block (L45-71).

If `## Status` is added to the SKILL.md schema, there are two possible readings: (a) it is a non-FR enhancement, or (b) it extends what FR-009 requires. Functional-typing treats it as (a) implicitly -- the FR coverage section does not mention it. But MO-3 simultaneously argues that spec.md's schema block (which is the normative expression of FR-009) must be updated to include `## Status`. You cannot claim FR coverage is unchanged and also argue the FR's normative schema must be expanded. One of these positions is wrong.

The spec.md schema block at L45-71 is the canonical definition of `problem.md` structure. If `## Status` is added there, FR-009 now implicitly requires it. If `## Status` is not added there, SKILL.md and spec.md disagree on the artifact schema. Functional-typing identified this in MO-3 but did not follow the implication back to the FR coverage claim.

---

## Tensions

### T-1: Condition 3 of the RD-1 Concession Places `## Status` Between `# Problem Definition` and `## Decision`

Functional-typing's concession on RD-1 includes three conditions. Condition 3 states: "The `## Status` section goes between `# Problem Definition` and `## Decision` in the schema." This is a structural choice with UX consequences that functional-typing does not analyze.

The `## Status` field is a meta-property (is the artifact complete?). Placing it before `## Decision` means the first thing a human reader sees after the title is a machine status indicator, not the substance of the problem. For the non-expert user principle (spec.md L87), the decision statement is arguably the most important content in the file -- it is what the user wrote or confirmed. Pushing it below a status indicator inverts the priority: machine metadata before human content.

My own review (OBA-1) pressed the point that `## Status` is structural decoration without an operational consumer. If it is also placed before the substantive content, it becomes the most prominent element in an artifact that supposedly serves non-experts. This is a tension with the user-facing design philosophy, not a fatal flaw, but functional-typing should have justified the placement or deferred it as a formatting decision.

### T-2: Functional-Typing's MO-2 (Status Re-evaluation on Refine) Conflicts with the Arbiter's Boundary Principle

Functional-typing recommends adding a fifth refine invariant: "(e) Status must be re-evaluated based on `[CLARIFY:]` tag count in the refined output." This is presented as a "mechanical consequence" of adopting both Change 7 and Change 10. The logic is sound: if `## Status` reflects `[CLARIFY:]` tag count, and refine can change that count, then refine must re-evaluate status.

But this is in tension with a principle both functional-typing and the arbiter established in RD-1: the `## Status` field is a factual annotation that spec 007 does not prescribe consumer behavior for. The refine invariants (Change 7) define what the define handler must guarantee when modifying an existing `problem.md`. Adding status re-evaluation as an invariant -- a structural requirement the handler MUST satisfy -- elevates `## Status` from "factual annotation" to "actively managed state." A factual annotation is computed once at write time and reflects reality. Actively managed state must be maintained across mutations and creates coupling between the mutation logic and the status field.

I do not argue this is wrong -- it is logically necessary if `## Status` is adopted. But it creates a tension with the framing that justified the concession. The field was sold as "zero-cost producer-side action." A refine invariant is not zero-cost. It adds a post-condition that every refine path must satisfy, which means test coverage, edge case analysis (what if the user resolves some but not all `[CLARIFY:]` tags?), and correctness obligations that did not exist before the concession.

### T-3: Rec #1 Heading Count Fix Is Correct but Reveals a Deeper Problem

Functional-typing's Rec #1 lists 9 headings (including `# Problem Definition` and `## Status`) when reconciling Change 1 and Change 10. My own review (Rec-2) argues the validation contract should specify heading level, case sensitivity, and content requirements. These two recommendations are compatible but reveal a deeper tension: the validation specification is becoming complex enough that prose may be insufficient.

Functional-typing's heading list in Rec #1 (`# Problem Definition`, `## Status`, `## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`) is a 9-element enumeration. My Rec-2 adds case sensitivity, heading-level matching, and content-beneath-heading rules. Together, these constitute a non-trivial validation specification embedded in prose. At what point does "one-sentence prose contract" become a multi-paragraph validation spec that would be more clearly expressed as a structured rule set?

Neither review proposes crossing that line in spec 007, and I am not proposing it now. But the tension is real: every addition to the validation contract (heading count, case rules, content requirements) makes the "prose not code" framing harder to sustain.

### T-4: No Off-Base Assumptions Identified -- Excessive Deference?

Functional-typing's Off-Base Assumptions section states: "None identified. The Round 1 deliberation was rigorous. The synthesis accurately characterized all positions. The arbiter's advisory opinions are well-grounded in specific SKILL.md lines and spec.md constraints."

For a multi-agent deliberation system designed around adversarial review, this is unusually deferential. By Round 2, three reviewers, a synthesizer, and an arbiter have produced positions. The probability that zero assumptions are off-base across all participants is low. This section reads as an endorsement of the process rather than a critical evaluation of the positions.

I note this as a tension, not a contradiction. It is possible that all positions are genuinely well-grounded. But the purpose of the Off-Base Assumptions section is to identify positions that rest on flawed premises -- and Round 2 introduced new premises (the arbiter's "factual annotation" framing, the "prose validation contract" concept, the "directory is the designed multi-source mechanism" grounding). Functional-typing accepted all three without identifying any weakness in their premises. My own review challenged two of them (OBA-1, OBA-2). The absence of any OBA finding from functional-typing suggests either genuine agreement or insufficient scrutiny of the new inputs.

---

## Safe Agreements

### SA-1: All 12 FRs Are Correctly Implemented

Both reviews confirm that all 12 functional requirements (FR-001 through FR-012) are implemented in SKILL.md and that the implementation is correct. Functional-typing provides a complete line-by-line mapping. My review does not contest any FR coverage. This is the strongest consensus position in the entire review -- no reviewer across either round has disputed it.

### SA-2: C-1 (Post-Write Schema Validation) Remains the Highest Priority Change

Both reviews reaffirm C-1 at P1 without modification. The define handler must validate all required headings after writing `problem.md`. Functional-typing grounds this in validation precedents elsewhere in SKILL.md (L195-196, L286-295, L659-676). My review agrees and adds precision requirements (case sensitivity, heading level). The core recommendation is identical.

### SA-3: C-2 (`--context` Path Validation) Remains P1

Both reviews reaffirm C-2 without modification. The define handler must validate that the `--context` path exists and warn when a directory contains no `.md` files. No dispute.

### SA-4: C-3 (Dispatch Matching) Remains P1

Both reviews confirm that dispatch matching must be documented as exact and case-sensitive. The fallback-to-`run` proposal is dead in both reviews. Both accept the error message enhancement for unknown subcommands.

### SA-5: Deferral of Multi-Path `--context` (RD-3)

Both reviews accept deferral. Functional-typing grounds the acceptance in the arbiter's observation that SKILL.md L797's directory support is the designed multi-source mechanism. My review accepts the same grounding. Both agree that the single-path constraint should be documented as a scoping decision (Change 11).

### SA-6: Deferral of `--force` and `--dry-run` (RD-4)

Both reviews accept deferral. Functional-typing cites the arbiter's non-expert user principle argument and the observation that `--dry-run` adds value only in scripted contexts. My review agrees. Both accept the documentation note (Change 13) as the appropriate compromise.

### SA-7: Four-Rule Refine Contract with Diff Summary as Recommended Practice (RD-5)

Both reviews adopt the arbiter's formulation: four post-conditions as normative, diff summary as recommended ("should" lowercase). Functional-typing traces the distinction to testability: structural invariants can be verified against output, UX guidance varies by context. My review agrees with this framing.

### SA-8: `## Status` as Factual Annotation Without Consumer Prescriptions (RD-1)

Both reviews accept the `## Status` section using the arbiter's "factual annotation" framing. Both withdraw RFC 2119 SHOULD language prescribing downstream behavior. Both agree that spec 008 decides how to use the field, not spec 007. This agreement is genuine despite the tensions I identify above -- the disagreement is about consequences and precision, not about whether the field should exist.

### SA-9: Validation Belongs at the Schema Layer, Not the Dispatch Layer (RD-2)

Both reviews accept the arbiter's position that validation is a schema-level concern, not a dispatch-layer concern. Both withdraw proposals for shared functions or dispatch-layer utilities. Functional-typing frames it as "per-handler implementation now, shared contract as prose." My review agrees with this placement but argues the prose must be more precise. The architectural decision is settled.

### SA-10: Changes 4-9 and 11-14 from the Round 1 Synthesis Are Accepted

Both reviews reaffirm the full set of P2 and P3 changes from the Round 1 synthesis without modification. No reviewer in either round has contested Changes 4 through 9 or Changes 11 through 14. These are consensus items.
