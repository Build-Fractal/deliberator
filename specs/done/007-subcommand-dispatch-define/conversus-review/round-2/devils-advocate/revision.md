# Revision: Devil's Advocate — 007-subcommand-dispatch-define (Round 2)

**Reviewer**: devils-advocate
**Round**: 2 of 2
**Revision iteration**: 1
**Basis**: Round 2 review + cross-reviews from functional-typing and integration-architect
**Date**: 2026-03-22

---

## Recommendation Dispositions

### Rec-1: `## Status` as factual annotation — MAINTAINED, concession sharpened

**Round 2 position**: Accept the arbiter's factual-annotation framing. The define handler sets `draft` when `[CLARIFY:]` tags exist, `ready` when none. No RFC 2119 language prescribing consumer behavior.

**Cross-review feedback**: Both functional-typing (DC-2) and integration-architect (DC-2) independently flagged my "bridge that nothing walks across" language as contradicting the concession. Functional-typing's analogy is precise: "You do not say 'a SHA-256 hash is not a hash if nothing verifies it.'" Integration-architect frames it more sharply: "The concession is either real or it is not."

**Revised position**: I concede the point fully. The "bridge" rhetoric was a qualified concession functioning as a reversal, and both cross-reviewers correctly identified it. The `## Status` field is valuable as a descriptive annotation regardless of whether spec 008 acts on it. A factual record of completeness in the artifact is useful to the human reader examining the file, independent of any programmatic consumer. I withdraw the "design risk" flag. Spec 008 will make its own decisions about gates, and loading those decisions with implied pressure from spec 007's review record is not this spec's responsibility.

**Priority**: P1 (unchanged).

---

### Rec-2: Tighten validation contract prose — MODIFIED, downgraded from P1 to P2

**Round 2 position**: Specify case-sensitive, heading-level-2-only matching for all 7 required headings. Framed as a "P1 amendment to existing C-1 consensus."

**Cross-review feedback**: Functional-typing (DC-1) identifies a dangerous contradiction: SKILL.md L659 uses case-insensitive, level-agnostic validation for Phase 6 output. My proposal would create two incompatible validation models in the same file. Integration-architect (DC-1) rejects the "P1 amendment to C-1" framing as procedurally improper -- calling new requirements "precision refinements" of closed consensus items would let any reviewer reopen any consensus item.

**Revised position**: Both critiques land.

On the procedural point: integration-architect is right. C-1 established the obligation (validate headings after writing). My Rec-2 adds implementation semantics (case sensitivity, heading level, content rules). These are new requirements, not refinements. I withdraw the "P1 amendment" framing. This is a new P2 recommendation.

On the substance: functional-typing's DC-1 is the stronger challenge. I was proposing stricter validation for `problem.md` than the engine applies to its own arbitration output -- without acknowledging or justifying the divergence. Two validation models with opposite semantics in the same SKILL.md is an incoherent outcome.

However, I do not fully concede on the substance. There is a legitimate reason for the divergence: Phase 6 validates output from an agent that writes freely (the arbiter may use any heading level or casing), while the define handler validates output it controls (it writes the schema itself). The define handler can and should validate precisely against the schema it just wrote. The Phase 6 validator must be permissive because the arbiter's output format is less constrained.

Revised recommendation: The define handler's post-write validation should check that all 7 required headings from the schema (SKILL.md L822-850) are present. The matching semantics should follow the existing Phase 6 precedent (case-insensitive, level-agnostic) for consistency across SKILL.md, unless a future spec explicitly establishes a separate validation model for handler-controlled output. This preserves the validation obligation without creating an internal inconsistency.

**Priority**: P2 (downgraded from P1). **Framing**: new recommendation, not an amendment to C-1.

---

### Rec-3: Write-failure error specification — MODIFIED to one-word qualifier

**Round 2 position**: Add a write-failure error specification: "If writing `problem.md` fails, report the error to the user and do not print the success report."

**Cross-review feedback**: Functional-typing (T-1) accepts the gap but notes the define handler uses the same Write tool as every other handler -- it does not write via a lower-level mechanism that could fail silently. The claimed define-vs-run asymmetry is weaker than presented. Integration-architect (T-1) proposes a simpler fix: change "After writing `problem.md`, print:" (SKILL.md L858) to "After *successfully* writing `problem.md`, print:" -- a one-word edit that gates the Report section on write success without introducing a redundant error-handling specification.

**Revised position**: Integration-architect's one-word fix is better than my multi-sentence specification. It closes the same gap with less text and without duplicating the runtime's own error-handling contract. Functional-typing is correct that the Write tool surfaces errors in both the define and run handlers -- my justification based on a define-specific silent-failure risk was overstated.

I adopt integration-architect's formulation: add "successfully" to SKILL.md L858.

**Priority**: P2 (unchanged). **Mechanism**: reduced from a new error-handling section to a one-word qualifier on the existing Report section.

---

### Rec-4: Interactive-mode behavior for vague/empty input — MAINTAINED, downgraded to P3

**Round 2 position**: Add explicit behavior for vague or empty responses in interactive mode: produce `[CLARIFY:]` tags, not hallucinated content. Priority P2.

**Cross-review feedback**: Functional-typing (T-2) agrees with the concern but argues the universal ambiguity rule at SKILL.md L852 ("Any field where the agent cannot confidently determine the content MUST include a `[CLARIFY: ...]` tag") already covers this. Adding a restatement for one input path sets a precedent of restating the rule for each new input mechanism. Recommends P3. Integration-architect (T-2) argues similarly: the MUST at L852 is unconditional, and an agent violating it on interactive input violates it everywhere. Recommends P3 at most, framed as a cross-reference rather than a restated obligation.

**Revised position**: Both cross-reviewers make a fair point about the precedent of per-path restatement. The MUST at L852 is indeed unconditional -- its second sentence ("Vague descriptions should produce more `[CLARIFY:]` tags, not hallucinated specifics") is precisely the behavior I am requesting for interactive mode.

I maintain the recommendation because the interactive path is uniquely exposed to this risk (a user typing "I'm not sure" is a qualitatively different input than a vague inline description), but I accept the downgrade to P3. The form should be a cross-reference as integration-architect suggests: "The ambiguity handling rule applies equally to interactive input -- vague or empty responses produce `[CLARIFY:]` tags, not speculative content."

**Priority**: P3 (downgraded from P2).

---

### Rec-5: Elevate architectural validation note from P3 to P2 — WITHDRAWN, placement accepted

**Round 2 position**: The note that future consumers should apply the same heading validation should be P2, placed adjacent to the post-write validation text.

**Cross-review feedback**: Functional-typing (T-3) argues I am conflating discoverability (a formatting decision) with priority (an implementation urgency signal). Co-location is a formatting fix that costs nothing; priority elevation is unwarranted for a forward-looking note with no current consumer. Integration-architect (T-3) makes the same distinction: priority tiers signal implementation urgency to spec 007 implementers, not reading order for future spec authors.

**Revised position**: I concede. Both cross-reviewers correctly identify the conflation. Priority indicates "when to implement," not "how important to find." A forward-looking note with no current consumer is correctly P3 regardless of where it is placed. The fix I actually wanted -- co-location with the schema section for discoverability -- is a formatting decision, not a priority decision.

I withdraw the P2 elevation. Accept Change 14 at P3, co-located with the post-write validation text (Change 1) for discoverability.

**Priority**: P3 (reverted from my proposed P2). **Placement**: adjacent to the validation contract, as both reviews agree.

---

### Rec-6: Deferral of multi-path `--context` — MAINTAINED (deferred)

**Round 2 position**: Accept deferral. Single-path is a scoping decision, documented as such.

**Cross-review feedback**: No challenge.

**Revised position**: Unchanged. One framing note from my cross-review of integration-architect stands: the documentation should describe directory support as a "pragmatic multi-source mechanism" rather than "deliberate design," since the directory mechanism lacks specification of ordering, conflicts, and deduplication that a deliberate design would require. But this is a wording preference, not a dispute.

**Priority**: Withdrawn from spec 007 scope. Documentation at P3 (Change 11).

---

### Rec-7: Deferral of `--force` and `--dry-run` — MAINTAINED (deferred)

**Round 2 position**: Accept deferral. Documentation note acknowledging future need is sufficient.

**Cross-review feedback**: No challenge.

**Revised position**: Unchanged.

**Priority**: Withdrawn from spec 007 scope. Documentation at P3 (Change 13).

---

### Rec-8: Four-rule refine contract, diff summary as recommended practice — MAINTAINED, with status re-evaluation gap acknowledged

**Round 2 position**: Accept four normative post-conditions (headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated). Diff summary as lowercase "should" recommended practice.

**Cross-review feedback**: Functional-typing (T-4) identifies a gap I missed: if both Change 7 (refine rules) and Change 10 (`## Status`) are adopted, the refine invariants are incomplete without status re-evaluation. A refine operation can change the `[CLARIFY:]` tag count, which changes the status. This is a fifth invariant: "(e) Status must be re-evaluated based on `[CLARIFY:]` tag count in the refined output."

**Revised position**: Functional-typing is correct. This is a mechanical consequence that I failed to account for despite accepting both changes. If `## Status` reflects `[CLARIFY:]` tag count and refine can change that count, then refine must re-evaluate status. I adopt the fifth invariant.

I note the tension functional-typing's own cross-review of my review (T-4) surfaces: this elevates `## Status` from "factual annotation computed once at write time" to "actively managed state maintained across mutations." This is logically unavoidable if both Change 7 and Change 10 are adopted, but it adds a post-condition that every refine path must satisfy. The cost is not zero, but it is proportionate -- re-counting `[CLARIFY:]` tags after a refine is a trivial operation.

Additionally, my cross-review of integration-architect raised a valid nuance (T-3): rule (d) ("Type re-evaluated") is not testable in the same way as rules (a)-(c). Rules (a)-(c) are structural checks verifiable by diffing artifacts. Rule (d) is a process obligation -- if the type does not change, there is no way to verify whether the handler re-evaluated or copied. This does not change my acceptance of the four-rule contract, but the distinction between testable structural invariants (a-c, e) and process obligations (d) should be noted in the spec prose.

**Priority**: P2 (unchanged). **Scope**: expanded from four to five invariants.

---

## New Recommendations

### New Rec-1: Specify `problem.md` / `conversus.yml` artifact independence (Priority: P3)

**Source**: Integration-architect's MO-2 from their Round 2 review, which I endorsed in SA-6 of my cross-review. Both `problem.md` (guided workflow output) and `conversus.yml` (direct execution input) coexist in the same directory with no documented interaction. A user who runs `/conversus define` in a directory that already contains `conversus.yml` may reasonably wonder whether the two artifacts are linked.

**Proposed change**: Add a single sentence to the Define: Problem Definition section: "`problem.md` and `conversus.yml` are independent artifacts. The guided workflow produces `problem.md` first; subsequent commands transform it into `conversus.yml`. The define handler does not read, modify, or depend on an existing `conversus.yml`."

**Priority**: P3. This is a documentation clarification, not a behavioral change.

---

## Position Summary

This revision makes three substantive concessions in response to cross-review challenges.

First, I fully withdraw the "bridge that nothing walks across" rhetoric about `## Status`. Both cross-reviewers correctly identified it as a qualified concession functioning as a reversal. The factual-annotation framing is accepted without reservation. The field is valuable as a descriptive record of artifact completeness, independent of downstream enforcement.

Second, I accept that my validation-precision proposal (Rec-2) was internally inconsistent with the existing Phase 6 validation model at SKILL.md L659. Creating two incompatible validation semantics in the same file is an incoherent outcome. The revised recommendation aligns with the established precedent (case-insensitive, level-agnostic) while maintaining the post-write validation obligation. The priority drops from P1 to P2, and the "amendment to C-1" framing is withdrawn as procedurally improper.

Third, I accept the downgrade of the architectural note priority (Rec-5) from P2 to P3. Both cross-reviewers correctly identified that I was conflating discoverability (a placement concern) with implementation priority. The co-location fix I wanted is a formatting decision, not a priority decision.

The remaining positions are refined rather than reversed. Rec-3 adopts integration-architect's elegant one-word fix over my verbose error specification. Rec-4 is downgraded to P3 with the form changed to a cross-reference. Rec-8 expands to include status re-evaluation as a fifth refine invariant -- a gap functional-typing identified that I should have caught.

The deliberation has converged substantially. The three P1 items from Round 1 (post-write validation, path validation, dispatch matching) are uncontested across all reviewers. The `## Status` field, the validation contract, the refine semantics, and the deferred items (multi-path `--context`, `--force`/`--dry-run`) are all settled at the mechanism level. The remaining differences are matters of priority assignment and prose precision -- exactly the kind of residual disagreement that a final synthesis can resolve without further rounds.
