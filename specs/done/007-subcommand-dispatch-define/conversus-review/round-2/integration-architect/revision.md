# Integration Architect — Round 2 Revision

**Reviewer**: integration-architect
**Revision**: Iteration 1, Round 2
**Date**: 2026-03-22
**Basis**: Own Round 2 review, cross-reviews from functional-typing and devils-advocate, spec.md, SKILL.md

---

## Recommendation Dispositions

### R1: Post-write schema validation (P1 unanimous) — MAINTAINED with heading count update

**Original**: The define handler validates all required headings after writing `problem.md`. Missing headings are added with `[CLARIFY:]` placeholders.

**Cross-review input**: Functional-typing's DC-1 correctly identifies that my R1 and R10 create a mechanical inconsistency: R1 references 7 headings while R10 adds an 8th (`## Status`). Functional-typing's Rec #1 (FT review L129-131) requires the heading count to be reconciled. This is not a new requirement — it is a mechanical consequence of adopting both changes, and I should have stated it explicitly.

**Disposition**: Maintained with amendment. If `## Status` is adopted (R10), the heading count in the post-write validation becomes 8, not 7. The heading list must include `## Status` alongside the existing 7. I adopt functional-typing's reconciliation as a mandatory mechanical fix. My use of "all required headings" without hardcoding a count (review L183) remains correct as a formulation, but the normative heading list that defines "required" must be updated.

**Grounding**: SKILL.md L822-850 (current 7-heading schema), functional-typing MO-1 at L101-105, Rec #1 at L129-131.

---

### R2: `--context` path validation (P1 unanimous) — MAINTAINED, no change

No cross-reviewer contested this recommendation. Fail on non-existent paths, warn on empty directories. Mirrors SKILL.md L195-196.

---

### R3: Dispatch matching (P1 consensus) — MAINTAINED, no change

Exact, case-sensitive, exhaustive. No cross-reviewer contested this. The "Did you mean: `/conversus run {cmd}`?" error message enhancement is accepted.

---

### R4: Single-agent execution model statement (P2 consensus) — MAINTAINED, no change

No cross-review engagement on this item. Confirmed at P2 without modification.

---

### R5: Empty-section `[CLARIFY:]` coverage (P2 consensus) — MAINTAINED, no change

No cross-review engagement on this item. Confirmed at P2 without modification.

---

### R6: `--output` directory creation semantics (P2 uncontested) — MAINTAINED, no change

No cross-review engagement on this item. Confirmed at P2 without modification.

---

### R7: Refine semantics — four-rule contract (P2 majority) — MAINTAINED with fifth invariant accepted

**Original**: Four normative post-conditions: (a) all headings preserved, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated. Diff summary as recommended practice.

**Cross-review input**: Functional-typing's DC-2 identifies that my four-rule contract leaves a write path (refine) that can produce a stale `## Status` field. The argument is precise: I advocate `## Status` as a "factual annotation" (review L57: "It is a fact: 'this artifact has N unresolved items'"), but a fact that is not re-evaluated after a refine becomes a falsehood. If a refine resolves all `[CLARIFY:]` tags, the status must flip from `draft` to `ready`. If a refine introduces new ambiguity, it must flip back. Functional-typing's Rec #3 (FT review L139-141) proposes invariant (e): Status re-evaluated based on `[CLARIFY:]` tag count in the refined output.

Devils-advocate's T-3 raises a secondary tension: rule (d) ("Type re-evaluated") is a process obligation, not a structural check observable from the output alone. This is a valid methodological observation but does not change the rule's value — the obligation is that the handler must consider type re-evaluation, not that the type must change. I acknowledge the distinction between structural checks (a-c) and process obligations (d, and now e) without changing the contract's normative status.

**Disposition**: Maintained with amendment. I accept functional-typing's fifth invariant. The refine contract becomes five rules: (a) all required headings preserved, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated, (e) Status re-evaluated based on `[CLARIFY:]` tag count. This is a mechanical consequence of adopting both `## Status` (R10) and the refine contract. The factual-annotation framing I advocate requires the fact to be maintained on every write path. Functional-typing identified a gap in my own argument that I should have caught.

I also note, per my cross-review T-1 of functional-typing (cross-reviews/functional-typing.md L33-39), that my formulation of rule (a) as "all headings preserved" (without hardcoding a count) remains correct regardless of whether the heading count is 7 or 8. The count is defined by the schema; the rule references the schema. This avoids the coupling risk functional-typing's explicit-count formulation creates.

**Grounding**: SKILL.md L791 (refine behavior), SKILL.md L865 (count computed from final output), functional-typing Rec #3 at L139-141, devils-advocate T-3 at L57-63.

---

### R8: Taxonomy closure design note (P2 consensus) — MAINTAINED, no change

No cross-review engagement on this item. Confirmed at P2 without modification.

---

### R9: Pipeline overview scaled to single sentence (P2 consensus) — MAINTAINED, no change

No cross-review engagement on this item. Confirmed at P2 without modification.

---

### R10: `## Status` section as factual annotation — MAINTAINED at P2, placement clarified

**Original**: Add a `## Status` section to `problem.md` as a factual annotation reporting the artifact's completeness state. Maintained at P1 from my position; synthesis rated it disputed.

**Cross-review input — placement**: Functional-typing's concession condition 3 (FT review L63) specifies placement between `# Problem Definition` and `## Decision`. My cross-review DC-2 of functional-typing (cross-reviews/functional-typing.md L19-28) identifies this as problematic: inserting metadata between the document title and the anchoring decision statement breaks reading flow for the non-expert user (spec.md L87). The user opening `problem.md` should see the decision first, not a metadata field. The arbiter's framing of status as a "factual annotation" supports placement at the end (after `## Source Documents`) or as document-level metadata before `# Problem Definition`, not between the title and content.

**Cross-review input — priority**: Devils-advocate's T-4 (DA cross-review L65-69) correctly notes that my R10 formulation ("Maintained P1 from my position; synthesis rates disputed. I accept the synthesis priority assignment while maintaining that the factual-annotation framing should resolve functional-typing's objection") is a diplomatic hedge that creates ambiguity. I should pick one. Functional-typing's concession (FT review L56-63) removes the sole objection that made the item disputed, but neither cross-reviewer explicitly re-rates the priority upward. Given that both other reviewers now accept the substance, this is no longer disputed, but I do not have consensus for P1. I register my position as P2 — elevated from "disputed" by virtue of the concession, but not P1 in the absence of explicit agreement from both other reviewers.

**Cross-review input — sufficiency**: Devils-advocate's DC-1 (DA cross-review L11-23) argues the factual-annotation framing "creates the appearance of having addressed the quality-checkpoint concern without actually addressing it." Devils-advocate's position is that a descriptive field with no consumer obligation is "metadata, not user experience improvement." I engaged with this in my cross-review DC-2 of devils-advocate (cross-reviews/devils-advocate.md L23-33): the concession is either real or it is not. If `## Status` is a fact about the artifact, the fact is useful regardless of what consumers do with it — just as a file's word count is useful even if no consumer gates on it. The user sees the status. That is the UX improvement. Whether the system enforces it is a different question for a different spec.

However, I take devils-advocate's synthesis guidance seriously: the synthesis should label `## Status` as "an explicit, accepted gap in the quality-checkpoint chain — the field is defined here; enforcement is deferred to spec 008." This is factually accurate and prevents spec 008's author from assuming the checkpoint is already operational.

**Disposition**: Maintained at P2. Placement should be at the end of the schema (after `## Source Documents`) or as frontmatter metadata, not between `# Problem Definition` and `## Decision`. The synthesis should note that this is a producer-side annotation with enforcement deferred to spec 008.

**Grounding**: Functional-typing RD-1 concession at L56-63 (substance conceded), devils-advocate DC-1 at L11-23 (sufficiency concern), spec.md L87 (non-expert user principle), SKILL.md L865 (count already computed).

---

### R11: Document single `--context` path constraint (P3 majority) — MAINTAINED with framing adjustment

**Cross-review input**: Devils-advocate's T-1 (DA cross-review L41-49) correctly notes the tension in calling directory-based aggregation a "deliberate design" while acknowledging it lacks specification for ordering, scoping, and conflict resolution. Devils-advocate proposes more honest framing: "Single-path is a scoping decision for spec 007. Directory support provides a pragmatic multi-source mechanism. A follow-up spec may introduce multi-path syntax with explicit ordering and conflict semantics."

**Disposition**: Maintained at P3. I accept devils-advocate's proposed documentation language. It is factually accurate without overclaiming. My Round 2 review's "deliberate design" characterization overstated the intent behind SKILL.md L797's file-or-directory convention — this is a file-resolution convention that happens to enable multi-source, not an architecturally deliberate multi-source pattern.

**Grounding**: SKILL.md L797, spec.md L35 (FR-006), devils-advocate T-1 at L41-49.

---

### R12: Acknowledge frontmatter change in spec (P3 single advocate) — MAINTAINED, no change

No cross-review engagement on this item. Confirmed at P3 without modification.

---

### R13: Note `--force`/`--dry-run` as future consideration (P3 majority) — MAINTAINED, no change

All reviewers agree on deferral. Documentation note is the appropriate compromise. No cross-review engagement beyond confirmation.

---

### R14: Note shared validation as architectural direction (P3 compromise) — MAINTAINED at P3

**Cross-review input**: Devils-advocate's Rec-5 (DA review L149-155) argues for elevation from P3 to P2 and co-location with the schema contract. My cross-review T-3 of devils-advocate (cross-reviews/devils-advocate.md L63-71) responded: priority tiers signal implementation urgency, not importance to future readers. Discoverability is a placement concern, not a priority concern. I accept co-location with the schema section but maintain P3 priority.

**Disposition**: Maintained at P3 with co-location accepted. The note should be placed adjacent to the schema/validation text for discoverability. The priority remains P3 because it is a forward-looking architectural note, not a spec 007 implementation requirement.

**Grounding**: SKILL.md L822-850 (schema location), devils-advocate Rec-5 at L149-155.

---

### R15: Document `problem.md` and `conversus.yml` artifact independence (P3 new) — MAINTAINED, acknowledged as single-round material

**Cross-review input**: Functional-typing's T-2 (FT cross-review L51-58) correctly notes that R15 is new Round 2 material that has not been subjected to adversarial scrutiny, and recommends the synthesizer weight it accordingly (analogous to Change 12, which was also single-advocate). Devils-advocate's SA-6 (DA cross-review L95-97) agrees it is a valid documentation gap.

**Disposition**: Maintained at P3. I accept functional-typing's procedural observation: this is single-advocate, single-round material and should be weighted accordingly by the synthesizer. The substance is straightforward — a single sentence noting that `problem.md` (guided workflow) and `conversus.yml` (direct execution) are independent artifacts for different workflow paths — and both cross-reviewers agree the observation is valid.

**Grounding**: SKILL.md L36-42 (run handler looks for `conversus.yml`), SKILL.md L769-876 (define handler produces `problem.md`).

---

## New Recommendations (Revision)

### NR-1: Accept devils-advocate's validation precision as P2 (not P1 amendment to C-1)

Devils-advocate's Rec-2 (DA review L128-133) proposes tightening the validation contract prose to specify case-sensitive heading-level-2 matching. My cross-review DC-1 of devils-advocate (cross-reviews/devils-advocate.md L11-19) rejected the "P1 amendment to C-1" framing as procedurally problematic — it attempts to reopen a closed consensus item by calling new requirements a "refinement." However, the substance is valid: the prose contract should specify that headings are `##`-level, case-sensitive, and matched by exact text.

The SKILL.md schema block at L822-850 already demonstrates the headings at `##` level with exact text, making the schema itself the normative reference. But an explicit prose statement eliminates the three ambiguities devils-advocate identifies (case sensitivity, heading level, content-presence). The specification cost is one sentence. The benefit is that two independent implementers produce the same check.

**Recommendation**: Add to the validation contract prose (adjacent to the schema at SKILL.md L822-850): "Headings are matched at `##` level with case-sensitive exact text. A heading present with no content beneath it (only whitespace before the next heading) is treated as present but empty — apply `[CLARIFY:]` handling per the ambiguity rule." Priority: P2, as a new clarification, not a P1 amendment to C-1.

**Grounding**: SKILL.md L822-850 (schema block is the normative reference), devils-advocate Rec-2 at L128-133, integration-architect cross-review DC-1 of devils-advocate at L11-19.

---

### NR-2: Gate the Report section on write success (one-word fix)

Devils-advocate's MO-1 (DA review L52-60) identifies that the Report section (SKILL.md L856-875) has no failure mode for write operations. My cross-review T-1 of devils-advocate (cross-reviews/devils-advocate.md L39-48) responded: the real concern is whether the Report section should be gated on write success, and the fix is a one-word qualifier — changing "After writing `problem.md`, print:" (SKILL.md L858) to "After successfully writing `problem.md`, print:". This closes the unguarded path without introducing a separate error-handling specification that competes with the agent runtime's own error contract.

**Recommendation**: Change SKILL.md L858 from "After writing `problem.md`, print:" to "After successfully writing `problem.md`, print:". Priority: P2. One-word edit, closes a real gap.

**Grounding**: SKILL.md L858 (current Report section preamble), devils-advocate MO-1 at L52-60, integration-architect cross-review T-1 at L39-48.

---

## Position Summary

### What changed from my Round 2 review

1. **Refine contract expanded from four to five rules** (R7). Functional-typing's fifth invariant (Status re-evaluated on refine) is a mechanical consequence of my own `## Status` advocacy. I should have identified this. The factual-annotation framing I championed requires the fact to be maintained on every write path, including refine.

2. **`## Status` placement clarified** (R10). I now explicitly oppose functional-typing's proposed placement between `# Problem Definition` and `## Decision`. The status section should go at the end of the schema (after `## Source Documents`) or as frontmatter, preserving the reading flow where the decision statement is the first substantive content.

3. **`## Status` priority settled at P2** (R10). I drop the P1 aspiration and accept P2. Functional-typing's concession removes the "disputed" label; explicit P1 consensus does not exist.

4. **Single-path `--context` framing adjusted** (R11). I accept devils-advocate's more honest documentation language. "Deliberate design" overstated; "scoping decision with pragmatic multi-source mechanism" is accurate.

5. **Validation precision accepted as new P2** (NR-1). Devils-advocate's case-sensitive heading-level-2 matching specification is substantively correct. I reject the "P1 amendment to C-1" framing but accept the content at P2.

6. **Report section write-success gate accepted as P2** (NR-2). A one-word fix that closes a real gap devils-advocate identified.

### What did not change

- All 13 Round 1 convergence points (C-1 through C-13) remain confirmed without modification.
- All 6 Round 1 concessions remain in effect without reversal.
- The three P1 changes (R1-R3) remain unanimous and unchanged in substance.
- The schema-layer validation contract (R14) remains at P3 with co-location accepted.
- The `problem.md`/`conversus.yml` independence note (R15) remains at P3 as single-round material.

### Final priority summary

| Priority | Recommendations |
|----------|----------------|
| P1 | R1 (post-write validation, heading count updated if R10 adopted), R2 (path validation), R3 (dispatch matching) |
| P2 | R4 (single-agent model), R5 (empty-section CLARIFY), R6 (output dir creation), R7 (five-rule refine contract), R8 (taxonomy closure note), R9 (pipeline overview), R10 (Status section, placement at end or frontmatter), NR-1 (validation precision), NR-2 (report write-success gate) |
| P3 | R11 (single-path documentation, adjusted framing), R12 (frontmatter change), R13 (force/dry-run future note), R14 (shared validation architectural note, co-located), R15 (artifact independence note, single-round) |

### Remaining disagreements

1. **`## Status` placement**: I oppose functional-typing's placement between `# Problem Definition` and `## Decision`. I advocate end-of-schema or frontmatter. This is a new disagreement that the synthesizer must resolve.

2. **Validation precision priority**: I rate NR-1 at P2. Devils-advocate rates equivalent content at P1 (as amendment to C-1). The substance is agreed; the priority and framing differ.

3. **`## Status` sufficiency**: Devils-advocate flags the factual annotation as an "accepted gap" in the quality-checkpoint chain. I agree it should be labeled as such in the synthesis. The field is defined here; enforcement is deferred to spec 008. This is not a disagreement on substance but on how the synthesis should characterize the outcome.
