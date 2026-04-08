# Neutral Synthesis: 005 P2/P3 Backlog Hardening

**Synthesizer**: neutral
**Date**: 2026-03-20
**Deliberation type**: Cooperative
**Target specification**: `/conversus/specs/005-p2p3-backlog-hardening/spec.md`

---

### Process Summary

- **Agents**: 3 -- spec-quality, skill-engine, implementor
- **Total artifacts**: 15
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 27 (spec-quality: 9, skill-engine: 9, implementor: 9)
- **Recommendations withdrawn** (Phase 3): 0
- **Recommendations modified** (Phase 3): 13 (spec-quality: 4, skill-engine: 4, implementor: 5)
- **Recommendations surviving** (Phase 3): 14 (spec-quality: 5, skill-engine: 5, implementor: 4)
- **New recommendations added** (Phase 3): 5 (spec-quality: 2, skill-engine: 1, implementor: 2)
- **Disputes remaining** (Phase 4): 4
- **Convergence points** (Phase 4): 6

---

### Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| 1 | spec-quality | Fix FR-009 cross-reference error | P1 | Surviving | None | Unanimous | Accepted |
| 2 | spec-quality | Resolve effort estimate contradiction (plan vs. tasks) | P1 | Surviving | None | Unanimous | Accepted |
| 3 | spec-quality | Add binary acceptance criteria to P3 user stories | P2 | Modified | implementor | Bilateral (spec-quality + implementor) | Accepted-Modified |
| 4 | spec-quality | Define STATUS.md maintenance trigger | P2 | Modified | implementor | Bilateral (spec-quality + implementor) | Accepted-Modified |
| 5 | spec-quality | Consolidate two-tier convention normative definition | P2 | Modified | implementor, skill-engine | Majority | Accepted-Modified |
| 6 | spec-quality | Disambiguate "implementation-complete" from "spec-complete" | P2 | Modified (priority lowered to P3) | skill-engine | Bilateral (spec-quality + skill-engine) | Disputed |
| 7 | spec-quality | Split SC-006 into per-category success criteria | P2 | Modified | implementor | Bilateral (spec-quality + implementor) | Accepted-Modified |
| 8 | spec-quality | Acknowledge FR-007 as behavioral specification change | P3 | Surviving | None | Unanimous | Accepted |
| 9 | spec-quality | Add FR traceability header to research.md | P3 | Surviving | None | Unanimous | Accepted |
| 10 | skill-engine | Unify Round Termination dispute counting with shared subsystem | P1 | Modified (deferred to STATUS.md tracking) | implementor | Bilateral (skill-engine + implementor) | Accepted-Modified |
| 11 | skill-engine | Add structural-marker support to stagnation detection | P1 | Modified (deferred to STATUS.md tracking) | implementor | Bilateral (skill-engine + implementor) | Accepted-Modified |
| 12 | skill-engine | Reclassify FR-011 as "Partial" | P1 | Surviving | None | Unanimous | Accepted |
| 13 | skill-engine | Use section headings instead of line numbers in STATUS.md | P2 | Surviving | None | Unanimous | Accepted |
| 14 | skill-engine | Harmonize heading-match semantics across subsystems | P2 | Modified (deferred to STATUS.md tracking) | implementor | Bilateral (skill-engine + implementor) | Accepted-Modified |
| 15 | skill-engine | Cross-reference template headings against FR-004 validation list | P2 | Modified (note in task description) | implementor | Bilateral (skill-engine + implementor) | Accepted-Modified |
| 16 | skill-engine | Refine FR-007 gap description for accuracy | P2 | Surviving | None | Unanimous | Accepted |
| 17 | skill-engine | Add Phase 6 overwrite note as cross-reference | P3 | Surviving | None | Bilateral (skill-engine + implementor) | Accepted |
| 18 | skill-engine | Document TEMPLATE_STATUS marker as shared convention | P3 | Surviving | None (but format disputed) | None | Disputed |
| 19 | implementor | Add content-anchor references to tasks T013-T015 | P1 | Surviving | None | Unanimous | Accepted |
| 20 | implementor | Add spec 005 to STATUS.md tracking | P1 | Surviving | None (priority disputed by skill-engine) | Unanimous (on inclusion) | Accepted |
| 21 | implementor | Define rendered format for two-tier convention | P1 | Modified | spec-quality | Bilateral (spec-quality + implementor) | Disputed |
| 22 | implementor | Downgrade FR-007 from P1 to P3 | P2 | Modified (keep current priority) | spec-quality, skill-engine | Unanimous (on keeping priority) | Accepted-Modified |
| 23 | implementor | Add acceptance verification to implementation tasks | P2 | Modified | spec-quality | Bilateral (spec-quality + implementor) | Accepted-Modified |
| 24 | implementor | Specify insertion format for SKILL.md additions | P2 | Modified | skill-engine | Bilateral (skill-engine + implementor) | Accepted-Modified |
| 25 | implementor | Add risk-of-gap and effort rendering examples | P2 | Modified | spec-quality | Bilateral (spec-quality + implementor) | Accepted-Modified |
| 26 | implementor | Add "done" state convention to tasks file | P3 | Surviving | None | None | Accepted |
| 27 | implementor | Clarify FR-008 dependency map format | P3 | Surviving | None | None | Accepted |
| N1 | spec-quality | Add spec 005 to STATUS.md tracking | P1 (new in Phase 3) | New | N/A | Unanimous | Accepted |
| N2 | spec-quality | Reclassify FR-011 as "Partial" | P1 (new in Phase 3) | New | N/A | Unanimous | Accepted |
| N3 | skill-engine | Add spec 005 self-tracking to STATUS.md | P2 (new in Phase 3) | New | N/A | Unanimous | Accepted |
| N4 | implementor | Reclassify FR-011 as Partial and add remaining work | P1 (new in Phase 3) | New | N/A | Unanimous | Accepted |
| N5 | implementor | Fix FR-009 cross-reference error | P1 (new in Phase 3) | New | N/A | Unanimous | Accepted |

Note: Recommendations N1/N3/20 converge on the same fix (spec 005 self-tracking). N2/N4/12 converge on the same fix (FR-011 reclassification). N5/1 converge on the same fix (FR-009 cross-reference). These are counted as single convergence points below.

---

### Dangerous Contradictions Found

**Resolved Contradictions**

1. **FR-011 "Done" assessment -- all three agents initially diverged, then converged.**
   - **What it was**: skill-engine identified in Phase 1 that research.md marks FR-011 as "Done" based on a STATUS.md cross-reference, but SKILL.md L459-469 (Round Termination Check) still contains inline dispute-counting logic independent of the Dispute-Parsing Subsystem (L641-666). spec-quality and implementor both accepted the "Done" assessment at face value in their Phase 1 reviews.
   - **Who conceded**: spec-quality conceded in their cross-review of skill-engine: "skill-engine's position is correct here... spec-quality should yield" (spec-quality cross-review of skill-engine, Dangerous Contradictions, first item). implementor conceded in their cross-review of skill-engine: "If skill-engine is correct that FR-011 is only partially done, the spec's '11 of 19 done, 8 remaining' framing is wrong" (implementor cross-review of skill-engine, Dangerous Contradictions, first item).
   - **Resolution**: All three agents agreed by Phase 3 to reclassify FR-011 as "Partial" and update the remaining work count from 8 to 9. This became a unanimous convergence point.

2. **FR-007 priority classification -- P3 downgrade vs. behavioral acknowledgment.**
   - **What it was**: implementor proposed downgrading FR-007 to P3 as "documentation polish" (implementor review, Actionable Recommendation 4). spec-quality argued FR-007 is a behavioral specification change requiring risk-table acknowledgment (spec-quality review, Off-Base Assumptions, second item; Actionable Recommendation 8). skill-engine argued FR-007 should stay at current priority with a more precise gap description (skill-engine review, Actionable Recommendation 7).
   - **Who conceded**: implementor conceded in their Phase 3 revision: "I was wrong to treat this as pure documentation polish. In a prompt-orchestrated system, the distinction between 'documentation' and 'behavioral specification' is thinner than in code-based systems" (implementor revision, Recommendation 4, Modified). The implementor adopted both spec-quality's risk-table edit and skill-engine's three-clarification scope.
   - **Resolution**: All three agents agreed to keep FR-007 at its current priority, update the plan risk table from "None" to "Minor," and refine the gap description to three specific clarifications.

3. **Scope boundary -- whether spec 005 should add new FRs (FR-020 for Round Termination, structural markers, heading harmonization, template cross-referencing).**
   - **What it was**: skill-engine proposed four new FRs or FR-extensions expanding spec 005's scope into behavioral specification changes (skill-engine review, Actionable Recommendations 1, 2, 5, 6). implementor maintained that the spec's scope should remain "documentation hardening" (implementor cross-review of skill-engine, Dangerous Contradictions, third item).
   - **Who conceded**: skill-engine conceded in their Phase 3 revision: "I accept the implementor's scope argument for the same reason I modified Recommendation 1 -- stagnation detection belongs to spec 002" (skill-engine revision, Recommendation 2, Modified). skill-engine modified all four recommendations to defer the actual fixes to STATUS.md tracking entries or notes rather than in-spec FRs.
   - **Resolution**: Diagnoses preserved via STATUS.md gap entries; fixes deferred to spec 002 or future work. However, a residual dispute remains about whether the Round Termination cross-reference specifically belongs in spec 005 (see Remaining Disputes).

**Unresolved Contradictions**

1. **FR-011 remediation scope -- in-spec cross-reference vs. deferred follow-up.**
   All three agents agree FR-011 is "Partial." The disagreement is about where the fix lives. spec-quality and implementor argue the cross-reference update belongs in spec 005 as a documentation edit. skill-engine initially deferred it to spec 002 but softened in Phase 4, stating the implementor's reframing is "persuasive." This contradiction is narrowing toward resolution (see Remaining Disputes, Dispute 1).

2. **Two-tier convention semantic resolution -- redefinition vs. clarifying note.**
   implementor proposes redefining "implementation-complete" to exclude acceptance criteria. spec-quality initially proposed this but withdrew after skill-engine raised the retroactive semantic shift concern. spec-quality now proposes a clarifying note instead. The implementor's revision adopted the redefinition approach that spec-quality had already withdrawn (see Remaining Disputes, Dispute 2).

---

### Systemic Contradictions

- **Specification-as-program tension**
  - **Manifests in**: FR-007 priority dispute (documentation vs. behavioral change), scope boundary dispute (documentation hardening vs. specification refactoring), plan risk table "None" vs. "Minor" disagreement.
  - **Root cause**: In a prompt-orchestrated system, the distinction between "documenting" existing behavior and "specifying" new behavior is ambiguous. SKILL.md is simultaneously documentation and program code. Any textual addition to SKILL.md potentially changes engine behavior because the LLM reads and acts on the text. The spec treats itself as "documentation-only" (plan.md L129) while adding specification-level matching rules (FR-007), creating a category mismatch.
  - **Implication for spec**: The spec should explicitly acknowledge that SKILL.md changes are specification changes, not pure documentation. The "documentation-only" framing should be replaced with "specification hardening" or the risk table should consistently reflect that SKILL.md edits carry minor behavioral impact. This is a framing change, not a structural one.

- **Shared subsystem ownership gap**
  - **Manifests in**: FR-011 remediation scope dispute, structural-marker gap in stagnation detection (skill-engine Recommendation 2), Round Termination inline parsing (skill-engine Recommendation 1), heading-match harmonization (skill-engine Recommendation 5).
  - **Root cause**: The Dispute-Parsing Subsystem is a shared component consumed by specs 001 and 002, but no single spec owns its maintenance. Spec 005 created FR-010/FR-011 to consolidate it, but the consolidation is incomplete -- one major consumer (Round Termination Check) still operates independently. The spec cannot fix this without expanding scope into another spec's domain.
  - **Implication for spec**: Shared subsystems need explicit ownership assignments in STATUS.md. The spec should designate which spec is responsible for maintaining the Dispute-Parsing Subsystem's consumer consistency and define what "stable interface" means for change management.

- **Living-document sustainability**
  - **Manifests in**: STATUS.md maintenance trigger debate, line-number fragility across documents, effort-estimate contradiction between plan.md and tasks.md, FR-traceability staleness risk.
  - **Root cause**: The spec creates STATUS.md as a "living document" with cross-references to other living documents (SKILL.md, research.md), but living documents decay at different rates and have no synchronization mechanism. Line numbers shift, effort counts diverge, and status labels become stale without defined triggers.
  - **Implication for spec**: STATUS.md should use stable references (section headings, not line numbers) and define explicit update triggers. More fundamentally, the spec should establish a convention that all cross-document references use anchors that survive content edits, not positional references.

- **Taxonomy layering complexity**
  - **Manifests in**: Two-tier convention semantic overlap dispute, rendering format ambiguity, retroactive semantic shift concern for spec 002's existing label.
  - **Root cause**: The spec introduces a new acceptance tier alongside an existing implementation tier without fully resolving how the two tiers interact semantically. "Implementation-complete" already implies acceptance criteria are met (per STATUS.md L5), creating overlap with "spec-complete." The spec attempts to make them complementary but the definitions are not orthogonal.
  - **Implication for spec**: Either redefine the existing implementation tier (accepting the retroactive shift risk) or add a clarifying note that explicitly maps the relationship. The rendering format should follow from the semantic resolution, not precede it. The spec should settle on one approach and apply it consistently across all four existing spec entries.

---

### Convergence Achieved

- **FR-011 reclassification from "Done" to "Partial"** -- Strength: Unanimous
  - **Agreed recommendation**: Reclassify FR-011 in research.md from "Done" to "Partial." Update the remaining work count from "11 done, 8 remaining" to "10 done, 9 remaining" across research.md, quickstart.md, plan.md, and tasks.md. The STATUS.md cross-reference is genuine partial progress, but SKILL.md L459-469 (Round Termination Check) still contains inline dispute-counting logic independent of the Dispute-Parsing Subsystem at L641-666, violating spec.md L209's delegation requirement.
  - **Supporting agents**: skill-engine (revision Recommendation 3, Surviving), spec-quality (revision New Recommendations, "Reclassify FR-011 as Partial"), implementor (revision New Recommendations, "Reclassify FR-011 as Partial and add remaining work").
  - **Evidence basis**: spec.md L209 requires "Spec 001 and spec 002 MUST reference the shared dispute-parsing specification rather than defining independent parsing logic." SKILL.md L459-460 specifies its own parsing rules ("Find the `### Remaining Disputes` heading and count `**Dispute:` entries under it") rather than referencing the Dispute-Parsing Subsystem at L641-666. This is a textual comparison against the spec's own requirement.
  - **Pre-existing or earned**: Earned. skill-engine identified this in Phase 1. spec-quality and implementor both initially accepted the "Done" assessment and conceded during cross-review after auditing the SKILL.md text. This was the single most significant position change in the deliberation.

- **FR-009 cross-reference error is a P1 spec bug** -- Strength: Unanimous
  - **Agreed recommendation**: Fix spec.md L204 to reference "FR-012/FR-013" instead of "FR-014/FR-015." FR-009 currently points implementors to Phase 4 edge case documentation and Phase 6 overwrite semantics instead of the two-tier status convention.
  - **Supporting agents**: spec-quality (revision Recommendation 1, Surviving), skill-engine (cross-review Safe Agreements, first item), implementor (revision New Recommendations, "Fix FR-009 cross-reference error").
  - **Evidence basis**: FR-014 is "Phase 4 Edge Case Documentation" and FR-015 is "Phase 6 Overwrite Semantics" (spec.md L216-220). The two-tier convention is defined in FR-012/FR-013 (spec.md L211-214). The cross-reference at L204 is demonstrably wrong.
  - **Pre-existing or earned**: Pre-existing. spec-quality identified this in Phase 1. No agent at any phase disputed the finding.

- **Content-anchor references must replace line numbers in Phase 4 tasks** -- Strength: Unanimous
  - **Agreed recommendation**: Replace absolute line-number references in tasks T013-T015 with content-anchor references identifying insertion points by unique text patterns (e.g., "after the output validation paragraph that begins 'After Phase 6 completes successfully, validate that...'"). Additionally, STATUS.md should use section headings rather than line numbers for SKILL.md cross-references.
  - **Supporting agents**: implementor (revision Recommendation 1, Surviving), spec-quality (cross-review of implementor, Tensions, endorsing as P1), skill-engine (revision Recommendation 4, Surviving, complementary STATUS.md references).
  - **Evidence basis**: Phase 4 tasks edit SKILL.md sequentially. After T013 inserts content, the line numbers referenced by T014 and T015 shift. With the addition of a potential T019 for FR-011 remediation, four sequential edits to the same file make line-number references untenable.
  - **Pre-existing or earned**: Pre-existing. implementor identified this in Phase 1. All agents agreed without challenge.

- **Spec 005 must track itself in STATUS.md** -- Strength: Unanimous
  - **Agreed recommendation**: Add a STATUS.md entry for spec 005 during Phase 3 implementation. Without this, SC-003 ("an implementor can determine the status of any spec... by reading a single document") is not satisfied by the spec's own delivery.
  - **Supporting agents**: implementor (revision Recommendation 2, Surviving, P1), spec-quality (revision New Recommendations, P1), skill-engine (revision New Recommendations, P2).
  - **Evidence basis**: STATUS.md currently tracks specs 001-004 (STATUS.md L15-34). Spec 005 creates and enriches STATUS.md but does not add itself. SC-003 requires coverage of "any spec."
  - **Pre-existing or earned**: Earned. implementor identified this in Phase 1. spec-quality and skill-engine both missed it in their initial reviews and added it as new recommendations in Phase 3 after the implementor's cross-review surfaced it.

- **Plan.md effort estimate must be corrected** -- Strength: Unanimous
  - **Agreed recommendation**: Update plan.md L92 from "3 FRs remain" to "2 FRs remain" for spec 001. Research.md L24 confirms FR-023 is implemented, making tasks.md L64 ("2 FRs remain") the correct figure.
  - **Supporting agents**: spec-quality (revision Recommendation 2, Surviving), skill-engine (cross-review Safe Agreements, fourth item), implementor (revision Recommendation 7, Modified).
  - **Evidence basis**: Research.md L24 marks FR-023 as "Done" with evidence at SKILL.md L581-582. plan.md L92 says "3 FRs remain," which contradicts the research evidence.
  - **Pre-existing or earned**: Pre-existing. spec-quality identified this in Phase 1. No agent disputed it.

- **Plan risk table must change from "None" to "Minor" for behavioral impact** -- Strength: Unanimous
  - **Agreed recommendation**: Update plan.md L129 from "SKILL.md additions change engine behavior: None" to "Minor -- FR-007 adds explicit matching semantics that refine existing behavior."
  - **Supporting agents**: spec-quality (revision Recommendation 8, Surviving), skill-engine (revision Recommendation 7, complementary), implementor (revision Recommendation 4, Modified).
  - **Evidence basis**: FR-007 (spec.md L199) adds case-insensitive, heading-line-scoped matching semantics to output validation. In a prompt-orchestrated system, SKILL.md text changes are specification changes that can affect engine behavior. The current "None" characterization is inaccurate.
  - **Pre-existing or earned**: Earned. spec-quality identified the inaccuracy in Phase 1. implementor initially disagreed, proposing to downgrade FR-007 to P3, but conceded in Phase 3 that the risk-table edit is warranted.

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

- **Dispute: FR-011 remediation scope -- in-spec cross-reference vs. deferred follow-up**
  - **Positions**: implementor and spec-quality argue the Round Termination Check (SKILL.md L459-469) should receive a cross-reference sentence within spec 005, framing it as a "reference update, not a specification redesign" (implementor revision, New Recommendation 1; spec-quality disputes, Dispute 1). skill-engine initially argued for deferral to spec 002 (skill-engine revision, Recommendation 1, Modified) but softened in Phase 4, stating the implementor's reframing is "persuasive" and proposing acceptance with explicit task ordering (skill-engine disputes, Dispute 1, Proposed resolution path).
  - **Arguments**: implementor argues that reclassifying FR-011 as "Partial" without adding a remediation task creates a gap between stated scope (9 FRs) and actionable work (8 tasks), which is "exactly the kind of ambiguity this spec is designed to eliminate." spec-quality argues that deferring to a follow-up "lacks any mechanism to ensure the follow-up actually happens -- there is no spec 002 revision in flight." skill-engine initially argued the fix belongs to spec 002's domain but in Phase 4 acknowledged the cross-reference framing is "documentation, not a behavioral rewrite" and proposed accepting it with a content-anchored task definition executed before T013-T015.
  - **Synthesizer assessment**: The evidence strongly favors including the cross-reference update in spec 005. All three agents agree FR-011 is "Partial." The dispute is narrowing: skill-engine's Phase 4 position is "I am willing to accept inclusion in spec 005" (skill-engine disputes, Flexibility, item 1). The implementor's framing -- that a one-sentence cross-reference is a documentation edit, analogous to FR-007's matching semantics addition -- is architecturally consistent with spec 005's scope. The stronger concern, raised by skill-engine, is about task ordering and content anchoring, which is a legitimate execution detail, not a scope objection.
  - **Recommended resolution**: Adopt the implementor's position. Add a new task (T019) to spec 005's Phase 4 that inserts a cross-reference sentence at L459-469 delegating to the Dispute-Parsing Subsystem. Use content-anchor references per skill-engine's Phase 4 proposal: "In the Round Termination Check section (the paragraph beginning 'Read the current round's synthesis'), replace the inline dispute-counting specification with a cross-reference to the Dispute-Parsing Subsystem." Execute T019 before T013-T015 per skill-engine's ordering rationale (edits flow downward in the file). The broader behavioral concerns (structural-marker support, heading-match harmonization) remain deferred to STATUS.md entries for spec 002.

- **Dispute: Two-tier convention semantic resolution -- redefinition vs. clarifying note**
  - **Positions**: implementor proposes redefining "implementation-complete" to mean only "all FRs represented in SKILL.md" without implying acceptance criteria coverage (implementor revision, Recommendation 3, Modified). spec-quality initially proposed this same approach but withdrew it after skill-engine raised the retroactive semantic shift concern, and now proposes a clarifying note instead (spec-quality revision, Recommendation 6, Modified; spec-quality disputes, Dispute 2). skill-engine does not directly address the semantic resolution but warned against retroactive redefinition (skill-engine cross-review of spec-quality, Tensions, third item).
  - **Arguments**: implementor argues redefinition makes the taxonomies cleanly orthogonal. spec-quality argues that changing the definition of "implementation-complete" after spec 002 has been labeled with it creates a retroactive semantic shift -- "even if spec 002 would still satisfy the narrower definition, the definitional change affects any future reader who consults the taxonomy section." spec-quality proposes a clarifying note that achieves conceptual orthogonality without rewriting the existing definition.
  - **Synthesizer assessment**: spec-quality's clarifying-note approach is better supported. The retroactive semantic shift concern is substantive: STATUS.md L5 currently defines "Implementation-complete" as including "The spec's own acceptance criteria are met," and spec 002 is labeled under that definition. Changing the definition after application creates a version-control problem for the taxonomy itself. The clarifying-note approach achieves the same conceptual clarity (explaining that the implementation tier and acceptance tier measure different things) without invalidating existing labels. The implementor may not have fully processed the retroactive-shift argument when formulating their revision, given that spec-quality had already withdrawn the same proposal for the same reason.
  - **Recommended resolution**: Adopt spec-quality's clarifying-note approach. Add a note to the STATUS.md taxonomy section that explains the relationship between the implementation tier and the acceptance tier without redefining either term. Then produce the rendering example the implementor requests, using the clarified (not redefined) semantics. The implementor's rendering example (`**Implementation**: Partially-complete / **Acceptance**: feature-complete`) remains a reasonable format, but the underlying label definitions should not change.

- **Dispute: TEMPLATE_STATUS marker -- separate subsystem entry vs. bundled under Structural Markers**
  - **Positions**: skill-engine argues `TEMPLATE_STATUS` deserves its own entry in the STATUS.md shared subsystem section, parallel to the Dispute-Parsing Subsystem, because it has different consumers and a different breaking-change surface than `DISPUTES_BEGIN/END` markers (skill-engine revision, Recommendation 9, Surviving; skill-engine disputes, Dispute 2). Neither spec-quality nor implementor explicitly addressed the separation question -- the existing T008 task bundles both marker types under a single "Structural Markers" entry.
  - **Arguments**: skill-engine argues the two marker types serve different purposes (`DISPUTES_BEGIN/END` for synthesis parsing, `TEMPLATE_STATUS` for template loading), have different consumers (specs 001/002 vs. spec 005), and have independent breaking-change surfaces. A bundled entry obscures which interfaces break when either changes. Neither opposing agent argued for bundling on principled grounds; their silence reflects an oversight rather than a deliberate architectural choice.
  - **Synthesizer assessment**: skill-engine's argument is technically sound. The two marker types are genuinely independent stable interfaces. However, the practical impact of bundling vs. separating is minimal for a document with five spec entries and a few shared subsystems. The cost of separation (one additional row) is near zero, and the benefit (precise change-impact tracking) is real if modest.
  - **Recommended resolution**: Adopt a compromise from skill-engine's own flexibility statement: keep a single "Structural Markers" entry in STATUS.md but add explicit sub-entries distinguishing the two marker types with their separate consumer lists and breaking-change surfaces. This provides the tracking precision skill-engine requires without inflating the subsystem section. If the document grows large enough that sub-entries become unwieldy, promote them to separate entries at that point.

- **Dispute: Spec 005 self-tracking priority -- P1 vs. P2**
  - **Positions**: implementor and spec-quality classify adding spec 005 to STATUS.md as P1 (implementor revision, Recommendation 2; spec-quality revision, New Recommendations). skill-engine classifies it as P2 (skill-engine revision, New Recommendations).
  - **Arguments**: implementor argues SC-003 requires "the status of any spec" and a success criterion violation is P1 by definition. skill-engine treats it as an enrichment task rather than a success criterion fix.
  - **Synthesizer assessment**: The implementor's argument is dispositive. SC-003 (spec.md L253) is explicit: "An implementor can determine the status of any spec... by reading a single document." If STATUS.md omits spec 005, this criterion is not met at delivery. The task is trivially small, so the priority classification is about mandatory-vs-optional signaling, not effort. skill-engine's own Phase 4 flexibility statement concedes: "I am willing to accept P1" (skill-engine disputes, Flexibility, item 3).
  - **Recommended resolution**: Classify as P1. All three agents agree on inclusion; the only disagreement is priority, and skill-engine has explicitly indicated willingness to accept P1.
<!-- CONVERSUS:DISPUTES_END -->

---

### Actionable Spec Changes

**P1 -- Must implement** (blocking issues or unanimous convergence):

1. **Fix FR-009 cross-reference error**: In spec.md L204, replace "FR-014/FR-015" with "FR-012/FR-013." Source: spec-quality Recommendation 1 (unanimous convergence). This is a factual error that misdirects implementors.

2. **Reclassify FR-011 as "Partial"**: In research.md, change FR-011 from "Done" to "Partial" with remaining work: "Round Termination Check (SKILL.md L459-469) must reference the Dispute-Parsing Subsystem rather than specifying inline parsing rules." Update remaining work count from "11 done, 8 remaining" to "10 done, 9 remaining" across research.md, quickstart.md, plan.md, and tasks.md. Source: skill-engine Recommendation 12, spec-quality New Recommendation N2, implementor New Recommendation N4 (unanimous convergence).

3. **Add FR-011 remediation task (T019) to spec 005**: Create a new task in Phase 4 to insert a cross-reference sentence at SKILL.md L459-469 delegating dispute counting to the Dispute-Parsing Subsystem. Use content-anchor reference: "In the Round Termination Check section (paragraph beginning 'Read the current round's synthesis')." Execute before T013-T015. Source: implementor New Recommendation N4, spec-quality Dispute 1, skill-engine Dispute 1 (converging, with synthesizer resolution).

4. **Replace line numbers with content anchors in tasks T013-T015**: Replace absolute SKILL.md line numbers with content-anchor references identifying insertion points by unique text patterns. Source: implementor Recommendation 19 (unanimous convergence).

5. **Correct plan.md effort estimate**: Update plan.md L92 from "3 FRs remain" to "2 FRs remain" for spec 001. Source: spec-quality Recommendation 2 (unanimous convergence).

6. **Add spec 005 to STATUS.md**: Add a STATUS.md entry for spec 005 during Phase 3 with implementation status, acceptance status, and standard fields. Source: implementor Recommendation 20, spec-quality N1, skill-engine N3 (unanimous convergence, P1 per synthesizer resolution).

7. **Update plan risk table**: Change plan.md L129 from "None" to "Minor -- FR-007 adds explicit matching semantics that refine existing behavior." Source: spec-quality Recommendation 8, skill-engine Recommendation 16, implementor Recommendation 22 (unanimous convergence).

**P2 -- Should implement** (majority convergence or strong single-agent case):

1. **Use section headings in STATUS.md cross-references**: Replace SKILL.md line-number references in STATUS.md (e.g., "L641-666") with section heading references (e.g., "section `### Dispute-Parsing Subsystem`"). Source: skill-engine Recommendation 13 (unanimous, unchallenged).

2. **Refine FR-007 gap description**: In research.md L27, replace the broad "doesn't specify case-insensitive or substring matching" with three specific missing items: (a) matching scoped to heading lines (lines starting with `#`), (b) case-insensitivity, (c) heading-level prefix irrelevance. Note that "contains" (SKILL.md L581) already implies substring matching. Source: skill-engine Recommendation 16 (unanimous, unchallenged).

3. **Add binary acceptance criteria to P3 user stories**: Add one concrete, enumerated criterion per P3 user story (US6-US11) naming specific items to verify -- not full Given/When/Then scenarios. Examples: US6 should name the specific Phase 6 note. US10 should list the four baseline features by name. US11 should name specs 002, 003, 004 as required entries. Source: spec-quality Recommendation 3, implementor Recommendation 23 (bilateral convergence, modified).

4. **Define STATUS.md maintenance trigger**: Amend FR-008 to include: "STATUS.md MUST be updated when any spec's implementation or acceptance status changes." Source: spec-quality Recommendation 4 (bilateral convergence with implementor).

5. **Consolidate two-tier convention normative definition with rendering example**: Designate FR-012 (spec.md L213) as the normative definition of "feature-complete" and "spec-complete." Add a clarifying note to the STATUS.md taxonomy section explaining the relationship between the implementation tier and the acceptance tier without redefining existing terms. Produce a rendering example in data-model.md showing the STATUS.md entry format. Source: spec-quality Recommendation 5, implementor Recommendation 21/25, synthesizer resolution of Dispute 2.

6. **Modify SC-006 to include an inline checklist**: Keep SC-006 as a single success criterion but add an inline checklist naming the six P3 categories: edge cases (FR-014), overwrite semantics (FR-015), risk assessments (FR-016), effort estimates (FR-017), baseline docs (FR-018), structure plan (FR-019). Source: spec-quality Recommendation 7, implementor agreement (bilateral convergence).

7. **Add acceptance verification to implementation tasks**: For P1/P2 tasks (T006-T013), add verification lines referencing corresponding spec.md acceptance scenarios. For P3 tasks, add verification lines after tightening P3 acceptance criteria per P2-3 above. Source: implementor Recommendation 23 (bilateral convergence with spec-quality).

8. **Specify insertion format for SKILL.md additions**: T013 = append as new sentence within existing output validation paragraph. T014 = add as new paragraph before failure handling list. T015 = add as new paragraph after output validation, formatted as cross-reference to Important Notes section: "Phase 6 follows the general overwrite semantics described in Important Notes: re-running overwrites any existing resolution.md." Source: implementor Recommendation 24, skill-engine Recommendation 17 (bilateral convergence).

9. **Add template heading note to output validation**: Add a brief note to the output validation section of SKILL.md or to task T013: "The headings validated here correspond to those instructed by `templates/cooperative/arbitration.md`. If the template's heading instructions change, update this list." Source: skill-engine Recommendation 15 (modified, bilateral convergence).

10. **Document Round Termination and stagnation gaps in STATUS.md under spec 002**: Add notes to spec 002's STATUS.md entry documenting: (1) stagnation detection does not support structural-marker parsing, only heading-based parsing; (2) heading-match semantics for the dispute-parsing heading fallback are not explicitly specified. Source: skill-engine Recommendations 10, 11, 14 (modified, bilateral convergence with implementor).

11. **Clarify FR-008 dependency map format**: Add a note to the Cross-Spec Dependencies section in STATUS.md: "This section summarizes the per-spec Depends On fields above. The per-spec entries are authoritative." Source: implementor Recommendation 27 (unchallenged).

**P3 -- Consider implementing** (bilateral agreement or strong but disputed):

1. **Add FR traceability header to research.md**: Add a traceability note: "FR numbers below correspond to spec.md as of [date]. If FRs are renumbered, this mapping must be updated." Source: spec-quality Recommendation 9 (unchallenged). Note: Low risk materializes only if FRs are renumbered.

2. **Add clarifying note for implementation-complete vs. spec-complete overlap**: Add a note to the taxonomy section explaining the relationship between the implementation tier and acceptance tier. Source: spec-quality Recommendation 6 (modified, synthesizer resolution of Dispute 2). Note: This is the conservative approach that avoids retroactive redefinition.

3. **Add TEMPLATE_STATUS sub-entry to Structural Markers**: In STATUS.md shared subsystem section, add explicit sub-entries under "Structural Markers" distinguishing `TEMPLATE_STATUS` (consumers: spec 005, all arbitration templates) from `DISPUTES_BEGIN/END` (consumers: specs 001/002, synthesis templates). Source: skill-engine Recommendation 18 (synthesizer resolution of Dispute 3).

4. **Add rendering examples for risk-of-gap and effort estimates**: Add a "Rendered Example" subsection to data-model.md showing a sample STATUS.md entry with all enriched fields, using corrected data (2 FRs for spec 001). Source: implementor Recommendation 25 (modified, bilateral convergence).

5. **Add "done" state convention to tasks file**: State that tasks should be marked `- [x]` as completed. Source: implementor Recommendation 26 (unchallenged, minor process improvement).

6. **Add heading-match harmonization note to STATUS.md**: Under the Dispute-Parsing Subsystem shared entry, note that heading-match semantics (case sensitivity, substring scope) are not explicitly specified for the heading fallback, and future work should harmonize with spec 005 FR-007's output validation rules. Source: skill-engine Recommendation 14 (modified).

---

### Key Concessions

**spec-quality**:
- Conceded that FR-011 should be reclassified as "Partial" after initially accepting research.md's "Done" assessment. spec-quality stated in their cross-review of skill-engine: "skill-engine's position is correct here. The spec text (FR-011, spec.md L209) requires specification-level delegation, and a STATUS.md cross-reference is metadata, not delegation. spec-quality should yield" (spec-quality cross-review of skill-engine, Dangerous Contradictions, first item). This was the most significant concession in the deliberation, changing the remaining work count from 8 to 9.
- Conceded that SC-006 splitting into six separate criteria was disproportionate, accepting the implementor's compromise of a checklist within a single criterion (spec-quality revision, Recommendation 7, Modified).
- Withdrew the orthogonal-redefinition approach for "implementation-complete" after skill-engine raised the retroactive semantic shift concern, adopting a clarifying-note approach instead (spec-quality revision, Recommendation 6, Modified).

**skill-engine**:
- Conceded that behavioral specification changes to the Round Termination Check (Recommendations 1 and 2) belong outside spec 005's scope. skill-engine stated: "I accept the implementor's scope argument for the same reason I modified Recommendation 1 -- stagnation detection belongs to spec 002" (skill-engine revision, Recommendation 2, Modified). This was the largest scope concession, removing two P1 recommendations from in-spec work.
- Conceded that heading-match harmonization across subsystems (Recommendation 5) and template heading cross-referencing (Recommendation 6) should be tracked as STATUS.md notes rather than in-spec FRs, accepting the implementor's scope constraint (skill-engine revision, Recommendations 5 and 6, Modified).
- Softened position on FR-011 remediation in Phase 4, acknowledging the implementor's cross-reference framing as "persuasive" and expressing willingness to accept inclusion in spec 005 (skill-engine disputes, Dispute 1 and Flexibility, item 1).

**implementor**:
- Conceded that FR-007 should not be downgraded to P3, acknowledging that "in a prompt-orchestrated system, the distinction between 'documentation' and 'behavioral specification' is thinner than in code-based systems" (implementor revision, Recommendation 4, Modified). This reversed the implementor's Phase 1 position.
- Conceded that the plan risk table's "None" characterization was inaccurate, adopting spec-quality's "Minor" edit (implementor revision, Recommendation 4, Modified).
- Conceded that FR-011 was incorrectly assessed as "Done," crediting skill-engine: "I credit skill-engine for catching what is genuinely 'the most significant assessment error in research.md'" (implementor revision, New Recommendation 1).
- Conceded that the rendering format for the two-tier convention depends on resolving the semantic overlap first, adopting spec-quality's sequencing: "semantics first, rendering second" (implementor revision, Recommendation 3, Modified).
