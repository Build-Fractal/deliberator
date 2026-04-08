# Disputes: Devil's Advocate — Round 2 Final (Phase 4)

**Reviewer**: devils-advocate
**Round**: 2 of 2
**Phase**: 4 (Final disputes before synthesis)
**Date**: 2026-03-22

---

## Remaining Disputes

### RD-1: `## Status` Priority — P1 vs P2

**My position**: P1.
**Functional-typing**: Has not assigned an explicit priority to `## Status` since conceding on RD-1. The revised conditions in Rec #4 govern the field's behavior but do not state a priority for the field itself as a standalone change. The implicit position is P2 by deference to the synthesis.
**Integration-architect**: P2 explicitly (revision L88: "I register my position as P2 -- elevated from 'disputed' by virtue of the concession, but not P1 in the absence of explicit agreement from both other reviewers").

**Status**: I am the sole P1 advocate. Integration-architect's P2 is a principled position -- without explicit P1 agreement from functional-typing, P1 consensus does not exist. I acknowledge this.

**Why I hold P1**: The `## Status` field is not an additive enhancement like Changes 4-9. It is the only element in the schema that makes the artifact's completeness state machine-readable. The Report section (SKILL.md L860-875) already computes and displays the `[CLARIFY:]` tag count to the terminal. Writing the same information into the file costs one line. Without it, the artifact's completeness state is only visible during the terminal session where `define` ran. Any subsequent reader -- human or agent -- must scan the entire file and count tags manually.

**Concession**: I accept that this will be synthesized at P2 given the vote distribution. I register the P1 position for the record but do not contest the P2 outcome.

---

### RD-2: Validation Matching Semantics — Phase 6 Precedent vs Handler-Controlled Precision

**My position**: The define handler's post-write validation should follow the existing Phase 6 precedent (case-insensitive, level-agnostic) for consistency across SKILL.md, unless a future spec explicitly establishes a separate validation model.
**Functional-typing**: References "all headings in the schema" without specifying matching semantics. Defers to the schema block as the single source of truth.
**Integration-architect**: Accepts the substance of case-sensitive heading-level-2 matching at P2 (NR-1 in revision L144-153) but rejects the "P1 amendment to C-1" framing. Proposes the SKILL.md schema block itself as the normative reference.

**Status**: This dispute has narrowed to a question of internal consistency. All three reviewers agree that (a) the define handler must validate headings after writing, and (b) the validation contract should be precise enough for independent implementation.

The remaining disagreement is whether define-handler validation should mirror Phase 6's permissive model (case-insensitive, level-agnostic -- SKILL.md L659) or adopt a stricter model justified by the handler controlling its own output. In my revision, I conceded toward Phase 6 consistency after functional-typing's DC-1 identified the incoherence of having two incompatible validation semantics in the same file. Integration-architect's NR-1 leans toward stricter matching but positions the schema block as the normative reference, which partially sidesteps the question.

**Resolution path**: The synthesizer should pick one model and state it. My revised recommendation is: follow Phase 6 precedent for consistency, note the divergence rationale if stricter matching is desired later, and let a future spec establish the separate validation model if the use case warrants it. This is the conservative choice -- it avoids creating an internal inconsistency in SKILL.md without a spec that explicitly justifies the divergence.

---

### RD-3: Synthesis Framing of `## Status` — "Solved" vs "Explicitly Deferred Gap"

**My position**: The synthesis must label `## Status` as a producer-side annotation with enforcement explicitly deferred to spec 008. It must not present the field as having resolved the quality-checkpoint concern.
**Functional-typing**: Agrees that FR-009 is unchanged and `## Status` is a "non-FR enhancement" (revision L97). Does not explicitly address the "solved vs deferred" framing question.
**Integration-architect**: Agrees explicitly (revision L92-93): "The synthesis should note that this is a producer-side annotation with enforcement deferred to spec 008."

**Status**: This is a framing dispute, not a substance dispute. All three reviewers agree on the mechanism (factual annotation, no consumer prescriptions). Integration-architect and I agree on the framing language. Functional-typing's position is compatible but does not explicitly state it.

**Why this matters**: If the synthesis presents `## Status` as a completed quality-checkpoint solution, spec 008's author may skip the enforcement question. If the synthesis labels it as a deliberate deferral, spec 008's author knows the checkpoint chain is incomplete and must be closed. The difference is one sentence in the synthesis, but it determines whether a design obligation is inherited or dropped.

**Concession**: This dispute is effectively settled. Integration-architect's explicit agreement (2 of 3 reviewers) gives the synthesizer sufficient basis to include the deferral language.

---

## Convergence

The following items are settled across all three reviewers with no remaining disagreement. This is a comprehensive inventory of the consensus surface.

### Unanimous P1 — No Dispute

1. **Post-write schema validation (C-1 / R1)**: The define handler validates all required headings after writing `problem.md`. Missing headings are added with `[CLARIFY:]` placeholders. The heading list is defined by the schema; the count updates if the schema changes. All three reviewers agree without reservation across both rounds.

2. **`--context` path validation (C-2 / R2)**: Fail on non-existent paths, warn on empty directories. Mirrors SKILL.md L195-196. Unanimous across both rounds.

3. **Dispatch matching semantics (C-3 / R3)**: Exact, case-sensitive, exhaustive dispatch table. "Did you mean: `/conversus run {cmd}`?" error message for unknown subcommands. Unanimous across both rounds.

### Unanimous P2 — No Dispute

4. **Single-agent execution model statement (C-4 / R4)**: Version-scoped wording. Uncontested.

5. **Empty-section `[CLARIFY:]` coverage (C-5 / R5)**: Uncontested.

6. **`--output` directory creation semantics (C-6 / R6)**: Uncontested.

7. **Five-rule refine contract (C-6 / R7)**: All three reviewers now accept five normative post-conditions: (a) all required headings preserved, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated, (e) Status re-evaluated based on `[CLARIFY:]` tag count. The expansion from four to five rules was initially proposed by functional-typing, accepted by integration-architect, and accepted by me. Diff summary remains recommended practice (lowercase "should").

8. **Taxonomy closure design note (C-8 / R8)**: Uncontested.

9. **Pipeline overview scaled to single sentence (C-9 / R9)**: Uncontested.

10. **`## Status` section as factual annotation (C-10 / R10)**: All three reviewers accept the field. All three accept the arbiter's "factual annotation" framing. All three withdraw RFC 2119 consumer prescriptions. Priority is P2 by majority (integration-architect and functional-typing) with my minority P1 position registered. **Placement**: All three reviewers now agree on end-of-schema placement (after `## Source Documents`). Functional-typing withdrew the between-title-and-decision placement after integration-architect's DC-2.

11. **Report section gated on write success (NR-2)**: Integration-architect's one-word fix ("After *successfully* writing `problem.md`, print:") is accepted by all three reviewers. P2.

12. **Single-path `--context` documented as scoping decision (C-11 / R11)**: All three accept deferral. Integration-architect accepts my proposed documentation language: "Single-path is a scoping decision for spec 007. Directory support provides a pragmatic multi-source mechanism." P3.

13. **Frontmatter change acknowledged (C-12 / R12)**: P3. Uncontested.

14. **`--force`/`--dry-run` as future consideration (C-13 / R13)**: All three accept deferral with documentation note. P3.

15. **Shared validation as architectural direction (C-14 / R14)**: All three agree on P3 priority, co-located with the schema section for discoverability. I withdrew the P2 elevation after both cross-reviewers correctly identified the priority/discoverability conflation.

16. **Interactive-mode vague input handling (Rec-4)**: Downgraded to P3 as a cross-reference to the existing ambiguity rule (SKILL.md L852), not a restated obligation. Accepted by all three reviewers at this priority and form.

17. **`problem.md` / `conversus.yml` artifact independence (R15 / New Rec-1)**: All three reviewers accept as a valid documentation gap. P3, single-round material, weighted accordingly by synthesizer.

18. **Validation precision (NR-1 / Rec-2)**: All three reviewers agree on the substance (validation should be precise enough for independent implementation). Priority: P2 as a new recommendation, not a P1 amendment to C-1. The "P1 amendment to C-1" framing is withdrawn by me. The matching-semantics question (Phase 6 consistency vs stricter model) is the only remaining nuance (see RD-2 above).

### FR Coverage

All 12 functional requirements (FR-001 through FR-012) are correctly implemented in SKILL.md. No reviewer in either round has disputed any FR implementation. This is the strongest consensus position in the entire deliberation. Adding `## Status` does not change FR-009; it is a non-FR schema enhancement.

---

## Final Position Statement

This deliberation has been monotonically convergent. No position conceded in Round 1 was reversed in Round 2. No position conceded in the Round 2 cross-reviews was reversed in the revisions. The disagreement surface has narrowed from five active disputes in Round 1 to three narrow disputes in Round 2 -- and of those three, one is effectively settled (RD-3: framing language), one is a priority vote I acknowledge losing (RD-1: P1 vs P2 for `## Status`), and one is a technical nuance the synthesizer can resolve with a single sentence (RD-2: validation matching semantics).

The structural integrity of spec 007 is sound. The 12 FRs are correctly implemented. The three P1 changes (post-write validation, path validation, dispatch matching) are the most robust consensus items I have seen in a multi-round deliberation -- not a single challenge in two rounds from any reviewer. The P2 changes are substantive and well-grounded. The P3 items are correctly scoped as documentation and forward-looking notes.

I close with three observations for the synthesizer:

1. **The `## Status` deferral language is load-bearing.** The synthesis must state that `## Status` is a producer-side annotation with enforcement deferred to spec 008. This is not editorial preference -- it determines whether spec 008's author inherits a binding design obligation or assumes the checkpoint is already operational. Integration-architect agrees on this framing.

2. **The five-rule refine contract is the most significant consensus achievement of Round 2.** Round 1 could not settle on refine semantics. Round 2 produced unanimous agreement on five testable (or at minimum, statable) post-conditions. The synthesizer should treat this as a settled contract, not a recommendation.

3. **The validation matching semantics question (RD-2) should default to Phase 6 consistency.** Creating two validation models in the same SKILL.md is an internal inconsistency that costs more than the precision it buys. The conservative choice is: follow the established precedent, note the possibility of a stricter model for handler-controlled output, and let a future spec make the change explicitly if warranted.

The deliberation is ready for synthesis.
