# Cross-Review of devils-advocate Round 2

**Reviewer**: functional-typing
**Reviewing**: devils-advocate Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: Rec-2's heading-level precision conflicts with existing Phase 6 validation precedent

Devils-advocate's Rec-2 (OBA-2, lines 88-102) demands case-sensitive, heading-level-2-only matching for `problem.md` validation: "Headings are matched case-sensitively. A heading with no content beneath it (only whitespace before the next heading) is present but empty."

This directly contradicts the validation precedent already established in SKILL.md for the engine's own Phase 6 output validation. SKILL.md L659 explicitly states: "Heading validation is case-insensitive, scoped to heading lines (lines starting with `#`), and heading-level prefix is irrelevant (e.g., `## Process Note` and `### Process Note` both satisfy the 'Process Note' check)."

Devils-advocate is proposing that spec 007 introduce a validation contract for `problem.md` that is *stricter* than what the engine uses for its own arbitration output -- the most structurally important artifact in the system. This creates two incompatible validation models within the same SKILL.md file: case-insensitive, level-agnostic validation for `resolution.md` (L659), and case-sensitive, level-2-only validation for `problem.md` (Rec-2). Any future spec author implementing the "shared contract" that both reviews agree on would face an immediate design conflict about which model to follow.

The contradiction is not just aesthetic. If spec 008's `interests` handler consumes `problem.md` and also emits an artifact validated by Phase 6's existing model, the same codebase would need two validation functions with opposite semantics. Devils-advocate's own argument in OBA-2 (line 96) that "two independent spec authors would implement the same check" is undermined by the fact that one spec author could reasonably look at L659 and implement case-insensitive matching -- which is exactly what "two independent implementations" means when the existing system already chose a convention.

If stricter validation is warranted for `problem.md` (which may be reasonable given it is a user-facing artifact), the review must acknowledge the divergence from L659 and justify it. As written, Rec-2 presents its precision requirements as obvious refinements when they are actually architectural choices that break consistency with the only other heading validation in the system.

### DC-2: "Factual annotation" framing accepted, then immediately undermined

In OBA-1 (lines 76-86), devils-advocate accepts the arbiter's reframing of `## Status` as a factual annotation and explicitly withdraws RFC 2119 SHOULD language. Line 81: "I withdraw my Round 1 demand for RFC 2119 SHOULD language prescribing consumer behavior."

But the very next paragraph (lines 82-84) reintroduces the same concern in different clothing: "If `## Status: draft` is a fact that nothing acts on, the non-expert user still runs `/conversus interests` on an incomplete `problem.md` and gets low-quality output." Devils-advocate then flags this as a "design risk" (line 86) and states: "A bridge that nothing walks across is not a bridge."

This is a rhetorical contradiction. If the `## Status` field is accepted as a factual annotation -- a computed property embedded in the artifact, like a file checksum -- then whether a downstream consumer checks it is, by definition, outside the annotation's concern. You do not say "a SHA-256 hash is not a hash if nothing verifies it." The hash exists as a fact. Devils-advocate says they accept this framing, then immediately argues the fact is pointless without consumer enforcement -- which is precisely the advisory/binding framing they claim to have withdrawn.

The "design risk" framing is technically not a reversal (devils-advocate is careful to say so at line 86), but it functions as one. It re-opens the dispute by embedding in the Round 2 record a warning that the arbiter's resolution is inadequate -- after accepting that resolution. If the goal is to influence spec 008's review, the proper mechanism is a forward-looking note, not a qualified concession that undercuts the arbiter in the same breath.

---

## Tensions

### T-1: Write-failure error specification (MO-1) has merit but overstates the gap

Devils-advocate's MO-1 (lines 52-58) identifies that the define handler has no specified behavior for write failure. The observation is accurate: the Report section (SKILL.md L856-875) assumes `problem.md` was successfully written. The recommendation -- "If writing `problem.md` fails, report the error to the user and do not print the success report" -- is a reasonable one-sentence addition.

However, the claimed distinction between the define handler and the run handler is overstated. Line 55: "The `run` handler has implicit write failure handling because it uses the Agent tool (which surfaces errors to the orchestrator). The `define` handler writes directly." The define handler also runs within an agent context (SKILL.md frontmatter L14: `allowed-tools: Agent Read Write Bash(ls:*)`). The Write tool surfaces errors to the agent in both cases. The define handler does not use a lower-level write mechanism that could fail silently -- it uses the same Write tool available to all handlers.

That said, specifying the error behavior explicitly is still defensible on the principle that agent behavior on tool failure is not guaranteed to be consistent. The recommendation is sound at P2, but the justification based on a define-vs-run asymmetry is weaker than presented. The real argument is: the Report section assumes success, and assumptions about prior steps should be stated.

### T-2: Interactive-mode termination (MO-2) is already covered by the ambiguity rule

Devils-advocate's MO-2 (lines 62-70) argues that FR-012's interactive mode needs an explicit specification for vague or empty responses. The recommendation is that such responses produce `[CLARIFY:]` tags rather than hallucinated content.

I agree with the concern but note that devils-advocate acknowledges the existing coverage at line 70: "The existing ambiguity handling rule (SKILL.md L852) arguably covers this implicitly." SKILL.md L852 reads: "Any field where the agent cannot confidently determine the content MUST include a `[CLARIFY: ...]` tag. Vague descriptions should produce more `[CLARIFY:]` tags, not hallucinated specifics." The second sentence is precisely the behavior MO-2 requests for interactive mode.

The tension is about whether "implicitly covered" is sufficient or whether the interactive path needs its own explicit statement. Devils-advocate argues the latter prevents "an agent from interpreting 'no input' as license to generate speculative content" (line 70). This is a judgment call about implementation discipline. I lean toward agreement that explicitness helps, given the non-expert user principle (spec.md L87), but I would place this at P3 rather than P2. The ambiguity rule at L852 is unconditional ("Any field") and applies regardless of input source. Adding a restatement for one input path sets a precedent of restating the rule for each new input mechanism.

### T-3: Elevating Change 14 from P3 to P2 (OBA-3) conflates discoverability with priority

Devils-advocate's OBA-3 (lines 104-114) argues that the architectural validation note (Change 14) should be elevated from P3 to P2 because "When the spec 008 author reads spec 007 looking for integration contracts, a P3 note is easy to skip. A P1 note adjacent to the schema is not" (line 110).

This conflates two things: the importance of the note's *placement* (co-location with the schema) and its *implementation priority*. Co-location is a formatting decision that costs nothing and should simply be done. Priority indicates when the change is needed relative to other changes. Change 14 is a forward-looking note about future consumers that do not yet exist. It has no implementation effect on spec 007. P3 is the correct priority for prose that has no current consumer -- regardless of where that prose is placed within the document.

The recommendation to co-locate the note with the schema (lines 112) is correct and unobjectionable. The recommendation to elevate its priority is not justified by the argument given. Place it adjacent to the validation text at P3.

### T-4: Rec-8's "normative vs. recommended" distinction for refine rules is well-drawn but incomplete

Devils-advocate's Rec-8 (lines 173-179) adopts the arbiter's distinction between the four normative post-conditions and the diff summary as recommended practice. This is the same position I hold (my review, lines 90-96). The distinction is correct: structural invariants are testable, UX guidance is contextual.

The tension is that neither review addresses how the refine path interacts with the `## Status` field. My review's MO-2 (lines 107-111) identifies that refine operations must re-evaluate `## Status` based on `[CLARIFY:]` tag count, adding a fifth invariant. Devils-advocate does not address this interaction despite accepting both Change 7 (refine rules) and Change 10 (`## Status`). This is a mechanical gap: if both changes are adopted, the refine invariants are incomplete without status re-evaluation. Devils-advocate's Rec-8 should account for it.

---

## Safe Agreements

### SA-1: All Round 1 convergence points (C-1 through C-13) are correctly reaffirmed

Both reviews reaffirm all 13 convergence points without reversal. Devils-advocate lines 24-32 and my review lines 19-27 align exactly. No disagreement on C-1 (post-write validation, P1), C-2 (path validation, P1), or C-3 (dispatch matching, P1). This is the structural backbone of the spec's improvements, and both reviews treat it as settled.

### SA-2: Deferral of multi-path `--context` (RD-3) and `--force`/`--dry-run` (RD-4)

Devils-advocate accepts deferral on both RD-3 (lines 43-44) and RD-4 (lines 46-47). My review holds the same deferral positions (lines 74-80 and lines 82-87). Both reviews ground deferral in the arbiter's reasoning: SKILL.md L797's directory support is the designed multi-source mechanism (not a workaround), and `--dry-run` adds no value in an interactive agent context. Complete agreement. The documentation notes (Changes 11 and 13) are the appropriate compromise.

### SA-3: `## Status` as factual annotation without consumer prescriptions (RD-1)

Both reviews concede to the arbiter's factual-annotation framing. Devils-advocate Rec-1 (lines 120-126): "The define handler sets `draft` when `[CLARIFY:]` tags exist, `ready` when none exist. No RFC 2119 language about downstream behavior." My review (lines 52-63): "The arbiter's factual-annotation framing resolves my boundary concern. Spec 007 is not prescribing consumer behavior -- it is embedding a computed property in the artifact." Full alignment on the mechanism and its boundary.

### SA-4: Validation belongs at the schema layer, not the dispatch layer (RD-2)

Devils-advocate withdraws the "Common Handler Utilities" dispatch-layer proposal (OBA-3, line 106). My review concedes to the schema-layer approach (lines 66-71). Both reviews accept the arbiter's position that validation is a per-handler responsibility with a prose contract at the schema level. The dispatch section (SKILL.md L18-34) should remain a minimal routing table. Both reviews agree the prose contract exists alongside the schema, not in a shared utilities section.

### SA-5: Four normative refine post-conditions with diff summary as recommended practice (RD-5)

Devils-advocate Rec-8 (lines 173-179) and my review (lines 90-96) adopt the same formulation: (a) headings preserved, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated as normative invariants; diff summary as lowercase "should" recommended practice. Both trace this to the arbiter's opinion on RD-5 and synthesis Change 7. No daylight between the two positions.

### SA-6: FR coverage is complete and correctly implemented

Devils-advocate (lines 24-39) and my review (lines 29-46) independently verify all 12 FRs are implemented with correct SKILL.md line references. No FR is missing, incorrectly implemented, or under-specified at the implementation level. This was uncontested in Round 1 and remains uncontested.

---

## Summary

Devils-advocate's Round 2 review is substantially improved from Round 1 -- the concessions are genuine, the remaining positions are better grounded, and the new missed opportunities (MO-1, MO-2) identify real gaps. The two dangerous contradictions I identify are not peripheral: DC-1 (heading validation semantics conflicting with the Phase 6 precedent at SKILL.md L659) would create an incoherent validation model across SKILL.md, and DC-2 (accepting the factual-annotation framing while immediately arguing the annotation is useless without enforcement) undercuts the stated concession. The tensions are resolvable -- T-1 and T-2 are matters of emphasis and priority, T-3 is a conflation of placement and priority that has a simple fix, and T-4 is a gap in devils-advocate's own analysis that my review already addresses. The five safe agreements cover the large majority of the review's surface area, confirming that Round 2 has produced strong convergence on all structural questions.
