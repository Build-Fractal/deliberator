# Round 2 Review: functional-typing

**Agent**: functional-typing
**Round**: 2 of 2
**Date**: 2026-03-22
**Target**: spec.md (007-subcommand-dispatch-define) + SKILL.md
**Prior round**: round-1/summary/final.md, round-1/arbitration/resolution.md

---

## Executive Summary

Round 1 produced 13 convergence points and 5 remaining disputes. This review engages the arbiter's advisory opinions and the synthesizer's assessments to resolve my positions on the five disputes. I concede on two (RD-1 and RD-2), hold on two (RD-3 and RD-4), and refine my position on one (RD-5). The spec and SKILL.md implementation remain structurally sound: all 12 FRs are correctly implemented, dispatch routing is correct, backward compatibility is preserved, and the `problem.md` schema matches spec.md character-for-character. What remains is tightening the schema and handler to close gaps the first round identified.

---

## Alignment

### Convergence points I reaffirm without modification

**C-1 (post-write schema validation, P1)**: Remains the single most important structural addition. The define handler at SKILL.md L822-850 defines a 7-heading schema but provides no runtime enforcement. The engine has validation at L195-196 (path existence), L286-295 (template validation), and L659-676 (Phase 6 output validation). The define handler needs the same discipline. Unanimous P1.

**C-2 (--context path validation, P1)**: The define handler's Context Ingestion section (SKILL.md L795-802) resolves the path and reads files but never checks existence. The `run` handler validates at L195-196 ("All resolved `TARGET_FILES` exist") and L196 ("All agent `docs` paths exist"). The define handler must mirror this. Unanimous P1.

**C-3 (dispatch matching, P1)**: SKILL.md L31-32 handles the unknown-subcommand case but does not state that matching is exact and case-sensitive. The dispatch table at L22-26 is exhaustive but does not say so. Both omissions should be fixed. I withdrew the fallback-to-`run` proposal in Round 1 and do not revisit it. Consensus P1.

**C-4 through C-13**: I reaffirm all remaining convergence points at their established priority levels without modification. None require further analysis from my perspective.

### FR coverage verification (unchanged from Round 1)

All 12 functional requirements (FR-001 through FR-012, spec.md L27-41) are implemented in SKILL.md:

- FR-001 (dispatch by first argument): SKILL.md L18-28.
- FR-002 (run routes to existing flow): SKILL.md L24 routes to `[Run: Input](#run-input)`.
- FR-003 (no-argument defaults to run): SKILL.md L26.
- FR-004 (unknown subcommand error): SKILL.md L31-32.
- FR-005 (natural-language input): SKILL.md L775-779.
- FR-006 (--context): SKILL.md L778, L795-802.
- FR-007 (output path): SKILL.md L784, L822.
- FR-008 (type classification): SKILL.md L806-818.
- FR-009 (problem.md sections): SKILL.md L822-850, matching spec.md L45-71.
- FR-010 (CLARIFY tags): SKILL.md L852.
- FR-011 (existing file check): SKILL.md L786-793.
- FR-012 (interactive questions): SKILL.md L779-782.

No FR is unimplemented or incorrectly implemented.

---

## Engagement with Disputes

### RD-1: `[CLARIFY:]` tags -- advisory vs. `## Status` section

**Round 1 position**: I opposed the `## Status` section as unnecessary schema expansion for an unwritten consumer.

**Arbiter's reframing**: The arbiter (resolution.md, RD-1 opinion) reframes the `## Status` field as neither advisory nor binding but **factual**: "it states a measurable property of the artifact." The arbiter grounds this in three observations: (1) SKILL.md L865 already computes the clarification count, (2) the Report section at L872-875 already warns the user, and (3) the non-expert user principle (spec.md L87) is served by making the file self-documenting.

**Revised position**: I concede. The arbiter's factual-annotation framing resolves my boundary concern. Spec 007 is not prescribing consumer behavior -- it is embedding a computed property in the artifact. The define handler already computes `count of [CLARIFY:] tags` at SKILL.md L865. Writing that count into the artifact is a zero-cost producer-side action that makes `problem.md` self-documenting. The non-expert user who opens `problem.md` in their editor sees `## Status: draft -- 3 items need clarification` without needing to scan for tags.

**Conditions on concession**:
1. The `## Status` section must use the synthesis's recommended language (final.md, Change 10): the define handler sets the status, spec 007 does not state what consumers do with it.
2. No RFC 2119 SHOULD language prescribing downstream behavior. Devils-advocate's original "Downstream commands SHOULD check the Status section before proceeding" remains outside spec 007's jurisdiction. The arbiter agrees (resolution.md, RD-1: "spec 007 does not define `/conversus interests`. It cannot prescribe that command's behavior, even with SHOULD").
3. The `## Status` section goes between `# Problem Definition` and `## Decision` in the schema, making the total required heading count 8 (not 7). Post-write schema validation (C-1) must be updated to check for 8 headings.

### RD-2: Shared validation function

**Round 1 position**: Validation belongs in each handler. The dispatch layer is a routing table.

**Arbiter's reframing**: The arbiter proposes a prose validation contract alongside the schema (resolution.md, RD-2): "After writing `problem.md`, validate that all required headings exist. Any command that reads `problem.md` as input should apply the same heading check before processing." One sentence, no code, no dispatch-layer utilities section.

**Revised position**: I concede to integration-architect's schema-layer approach as articulated by the arbiter. My Round 1 position was correct that validation does not belong in the dispatch section (SKILL.md L18-34 is six lines of routing -- it should stay minimal). The arbiter confirms this (resolution.md, RD-2: "Do not add a 'Common Handler Utilities' subsection to the dispatch section"). But I was too restrictive in insisting validation is purely handler-local. A one-sentence prose contract at the schema level (SKILL.md, after the schema block near L850) names the obligation for future consumers without mandating a shared function. This is the right balance: per-handler implementation now, shared contract as prose.

### RD-3: Multi-path `--context`

**Round 1 position**: Defer.

**Arbiter's confirmation**: The arbiter confirms deferral and grounds it in design intent: "SKILL.md L797 explicitly supports directories: 'path may be a file or directory.' The directory mechanism is the intended multi-source pattern -- not a workaround, but the design" (resolution.md, RD-3).

**Position held**: I maintain deferral. The arbiter's grounding in SKILL.md L797 is structurally significant. The directory mechanism is not a limitation -- it is the designed multi-source pattern. FR-006 (spec.md L35) uses the singular: `--context <path>`. Multi-path introduces ordering, deduplication, and conflict resolution semantics that no FR addresses. Spec 007 should document the single-path constraint explicitly (Change 11) and note that multi-path is a candidate for future extension.

### RD-4: `--force` and `--dry-run` flags

**Round 1 position**: Defer.

**Arbiter's confirmation**: The arbiter confirms deferral: "spec 007 does not define an automation context" (resolution.md, RD-4). The non-expert user principle (spec.md L87) argues against expanding the flag surface.

**Position held**: I maintain deferral. The arbiter adds a structural argument I did not make in Round 1: `--dry-run` is unnecessary in an interactive context where the agent already presents the result to the user (resolution.md, RD-4). The agent writes `problem.md` and prints the Report (SKILL.md L856-875). The user sees what happened. Preview mechanisms add value only in scripted contexts, which do not exist in spec 007's scope. Change 13 (documentation note acknowledging future need) is the appropriate compromise.

### RD-5: Refine semantics -- minimal contract depth

**Round 1 position**: Defer to integration-architect's four-rule formulation.

**Arbiter's refinement**: The arbiter endorses the four rules as normative and the diff summary as recommended practice (resolution.md, RD-5): "After refining, the define handler should summarize what changed... to make the operation auditable." Lowercase "should" -- recommendation, not requirement.

**Refined position**: I adopt the arbiter's formulation. The four post-conditions (headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated) are structural invariants the agent can enforce. The diff summary is UX guidance. This distinction matters: structural invariants are testable against output; UX guidance varies by context. Change 7 in the synthesis captures this correctly.

---

## Missed Opportunities

### MO-1: Post-write validation must account for `## Status` heading (P1)

If the `## Status` section is adopted (per my concession on RD-1), the post-write schema validation (C-1, Change 1) must check for 8 required headings, not 7. The synthesis's Change 1 text references "all required headings" and lists them, but does not include `## Status`. This is a mechanical inconsistency between Change 1 and Change 10 that must be reconciled. If both changes are adopted, the heading list in Change 1 must include `## Status`.

**Structural evidence**: The schema at SKILL.md L822-850 currently has 7 headings. Adding `## Status` (Change 10) makes it 8. Refine semantics (Change 7, rule (a)) references "All 7 required headings" -- this must become "All 8 required headings."

### MO-2: `## Status` must be updated on refine, not just initial write (P2)

Change 10 specifies that the define handler sets `status: draft` or `status: ready` based on `[CLARIFY:]` tag presence. But the refine path (SKILL.md L791, "incorporate the user's new input while preserving existing structure") may change the number of `[CLARIFY:]` tags. If a user resolves all clarification items during a refine operation, the status must flip from `draft` to `ready`. If a refine introduces new ambiguity, the status must flip the other direction. The refine semantics (Change 7) should include a fifth invariant: (e) Status must be re-evaluated based on `[CLARIFY:]` tag count in the refined output.

**Structural evidence**: The Report section (SKILL.md L865) computes `count of [CLARIFY:] tags` from the final output. The status field must be consistent with this count after every write, including refines.

### MO-3: Schema block in spec.md does not include `## Status` (P3)

Spec.md L45-71 contains the canonical `problem.md` schema. If `## Status` is adopted, the spec's schema block should be updated to match. Otherwise spec.md and SKILL.md diverge on the artifact structure.

---

## Off-Base Assumptions

None identified. The Round 1 deliberation was rigorous. The synthesis accurately characterized all positions. The arbiter's advisory opinions are well-grounded in specific SKILL.md lines and spec.md constraints.

---

## Actionable Recommendations

### P1 Recommendations

**Rec #1: Reconcile heading count between Change 1 and Change 10.**
If both post-write schema validation (Change 1) and `## Status` (Change 10) are adopted, the validation must check for 8 headings: `# Problem Definition`, `## Status`, `## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`. Refine semantics (Change 7, rule (a)) must reference 8, not 7.
*Traced to*: C-1, Change 1, Change 10 interaction. Structural consistency requirement.

**Rec #2: Reaffirm all P1 changes from the synthesis.**
Changes 1, 2, and 3 from the Round 1 synthesis are correct, well-grounded, and should be adopted without modification (aside from the heading count fix in Rec #1).
*Traced to*: C-1, C-2, C-3.

### P2 Recommendations

**Rec #3: Add `## Status` re-evaluation to refine invariants.**
Change 7's four refine invariants should become five: (a) all required headings present, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated, (e) Status re-evaluated based on `[CLARIFY:]` tag count. This is a mechanical consequence of adopting both Change 7 and Change 10.
*Traced to*: MO-2, Change 7, Change 10 interaction.

**Rec #4: Reaffirm all P2 changes from the synthesis.**
Changes 4-9 from the Round 1 synthesis are correct and should be adopted. Change 10 should be adopted with the conditions stated in my RD-1 concession (factual annotation, no SHOULD language, heading count updated).
*Traced to*: C-4 through C-9.

### P3 Recommendations

**Rec #5: Update spec.md schema block if `## Status` is adopted.**
Spec.md L45-71 should include `## Status` between `# Problem Definition` and `## Decision` to stay consistent with the SKILL.md schema.
*Traced to*: MO-3.

**Rec #6: Reaffirm all P3 changes from the synthesis.**
Changes 11-14 from the Round 1 synthesis are appropriate low-risk additions.
*Traced to*: C-10 through C-13, Changes 11-14.

---

## Referenced Documentation

| Document | Lines/Sections | Purpose |
|----------|---------------|---------|
| spec.md | L6 (foundational declaration) | Spec jurisdiction |
| spec.md | L13 (feature summary) | Scope of changes |
| spec.md | L17 (what changes) | Change surface |
| spec.md | L27-41 (FR-001 through FR-012) | Functional requirements |
| spec.md | L35 (FR-006, singular `--context <path>`) | Multi-path deferral grounding |
| spec.md | L40 (FR-011, existing file check) | Interactive safeguard |
| spec.md | L45-71 (problem.md schema) | Canonical schema definition |
| spec.md | L87 (non-expert user principle) | Design constraint |
| spec.md | L88-89 (must not break run, must not couple) | Additive constraint |
| SKILL.md | L18-34 (Subcommand Dispatch) | Dispatch implementation |
| SKILL.md | L22-26 (dispatch table) | Routing table |
| SKILL.md | L31-32 (unknown subcommand error) | Error handling |
| SKILL.md | L192-196 (run handler validation) | Validation precedent |
| SKILL.md | L286-295 (template validation) | Validation precedent |
| SKILL.md | L659-676 (Phase 6 output validation) | Validation precedent |
| SKILL.md | L769-876 (Define: Problem Definition) | Define handler implementation |
| SKILL.md | L775-782 (input forms) | FR-005, FR-012 coverage |
| SKILL.md | L786-793 (existing file check) | FR-011 coverage |
| SKILL.md | L795-802 (context ingestion) | FR-006 coverage, path validation gap |
| SKILL.md | L797 (directory support) | Multi-source design pattern |
| SKILL.md | L806-818 (type classification table) | FR-008 coverage |
| SKILL.md | L822-850 (problem.md schema) | Schema definition |
| SKILL.md | L852 (CLARIFY tag rule) | FR-010 coverage |
| SKILL.md | L854 (empty sections rule) | Empty section handling |
| SKILL.md | L856-875 (Report section) | Output format |
| SKILL.md | L865 (clarification count) | Status field grounding |
| SKILL.md | L872-875 (clarification warning) | Warning mechanism |
| final.md (Round 1 synthesis) | C-1 through C-13 | Convergence points |
| final.md (Round 1 synthesis) | RD-1 through RD-5 | Remaining disputes |
| final.md (Round 1 synthesis) | Changes 1-14 | Actionable spec changes |
| resolution.md (arbitration) | RD-1 opinion | Status-as-fact framing |
| resolution.md (arbitration) | RD-2 opinion | Schema-layer validation contract |
| resolution.md (arbitration) | RD-3 opinion | Directory-as-design grounding |
| resolution.md (arbitration) | RD-4 opinion | Interactive-context argument |
| resolution.md (arbitration) | RD-5 opinion | Four rules normative, diff summary recommended |
