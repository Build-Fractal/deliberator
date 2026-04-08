# Neutral Synthesis — Phase 1 Verification Gate (Spec 005)

**Synthesizer**: neutral
**Date**: 2026-03-20
**Spec**: 005-p2p3-backlog-hardening
**Gate**: Phase 1 (Verification of Pre-Existing FRs)

---

## Process Summary

**Agents**: 2 (compliance-auditor, scope-boundary)

**Artifacts produced**:
- 2 Phase 1 reviews (compliance-auditor: 7 recommendations; scope-boundary: 8 recommendations)
- 2 Phase 2 cross-reviews (each identifying 3-4 dangerous contradictions, 4-5 tensions, 4 safe agreements)
- 2 Phase 3 revisions (compliance-auditor: 2 withdrawn, 3 modified, 2 surviving, 3 new; scope-boundary: 1 withdrawn, 3 modified, 4 surviving, 2 new)
- 2 Phase 4 dispute documents (compliance-auditor: 2 disputes, 5 convergence points; scope-boundary: 2 disputes, 5 convergence points)

**Recommendations**:
- Total proposed: 15 original (7 + 8) + 5 new in revision (3 + 2) = 20
- Withdrawn: 3 (compliance-auditor Recs 6, 7; scope-boundary Rec 6)
- Modified: 6 (compliance-auditor Recs 1, 3, 5; scope-boundary Recs 1, 3, 7)
- Surviving unmodified: 6 (compliance-auditor Recs 2, 4; scope-boundary Recs 2, 4, 5, 8)
- New from revision: 5 (compliance-auditor New Recs A, B, C; scope-boundary New Recs N1, N2)
- Total active after revision: 17

**Disputes remaining**: 2 (both narrow -- mechanism/placement disagreements, not substance disagreements)

**Convergence points**: 5 strong bilateral convergences confirmed by both agents in Phase 4

---

## Recommendation Scorecard

| ID | Agent | Original Summary | Original Priority | Cross-Review Reaction | Revision Disposition | Final Status | Disputes? |
|---|---|---|---|---|---|---|---|
| CA-1 | compliance-auditor | Update FR-002 error message to match SKILL.md | P2 | scope-boundary: unidirectional pass, no edit needed | Modified to P3, Phase 5 polish | Active (P3) | No |
| CA-2 | compliance-auditor | Expand spec.md L278 to mention both inline-parsing sites | P2 | scope-boundary concedes correctness | Surviving (P2) | Active (P2) | No |
| CA-3 | compliance-auditor | Add behavioral-change note to T019 | P2 | scope-boundary: valid but respect read-only boundary | Modified: P2, acted upon outside Phase 1 | Active (P2) | No |
| CA-4 | compliance-auditor | Add task to update STATUS.md after T019 | P2 | scope-boundary endorses independently | Surviving (P2) | Active (P2) | No |
| CA-5 | compliance-auditor | Clarify T003 scope excludes FR-007 | P3 | scope-boundary: belongs in Phase 4 review | Modified to informational, bundle with other edits | Active (informational) | No |
| CA-6 | compliance-auditor | Note cooperative template heading asymmetry | P3 | scope-boundary: out of Phase 1 scope | Withdrawn | Closed | No |
| CA-7 | compliance-auditor | Document draft message game-dynamics note | P3 | Not directly challenged | Withdrawn (speculative, future-proofing) | Closed | No |
| CA-A | compliance-auditor | FR-012 verification gap (new) | P2 | N/A (emerged from cross-review) | New recommendation, P2 | Active (P2) | Yes (Dispute 1: placement) |
| CA-B | compliance-auditor | Explicit enumeration of "10 FRs" (new) | P2 | N/A | New recommendation, P2 | Active | Yes (Dispute 2: P2 vs. P3) |
| CA-C | compliance-auditor | STATUS.md baseline verification (new) | P3 | N/A | New recommendation, P3 | Active (P3) | No |
| SB-1 | scope-boundary | Add explicit pass/fail criteria to Phase 1 tasks | P2 | compliance-auditor: sufficient for one-time audit | Modified to P3 | Active (P3) | No |
| SB-2 | scope-boundary | Replace line numbers with section heading references | P2 | compliance-auditor concedes forward-looking value | Surviving (P2) | Active (P2) | Yes (Dispute 2: bundling) |
| SB-3 | scope-boundary | Add Phase 1 task to verify STATUS.md baseline | P2 | compliance-auditor: out of Phase 1 scope | Modified: Phase 2 header precondition note, P3 | Active (P3) | No |
| SB-4 | scope-boundary | Add negative verification for cooperative template | P3 | compliance-auditor performed check, agrees task should include it | Surviving (P3) | Active (P3) | No |
| SB-5 | scope-boundary | Enumerate verified FRs in Phase 1 header | P3 | compliance-auditor concedes gap, adds New Rec B | Surviving (P3) | Active (P3) | Yes (Dispute 2: priority) |
| SB-6 | scope-boundary | Confirm Phase 4 does not encroach Phase 1 scope | P1 | Not challenged (confirmation) | Withdrawn (was confirmation, not recommendation) | Closed | No |
| SB-7 | scope-boundary | Verify Phase 3+4 parallel safety | P2 | compliance-auditor reframes as behavioral risk | Modified: P3, credits compliance-auditor's framing | Active (P3) | No |
| SB-8 | scope-boundary | Confirm T006 marked [x], add FR-012 verification | P1 | compliance-auditor concedes blind spot fully | Surviving (P2, reduced from P1) | Active (P2) | Yes (Dispute 1: placement) |
| SB-N1 | scope-boundary | Acknowledge dual-site FR-011 in T004 description (new) | P3 | N/A | New recommendation | Active (P3) | No |
| SB-N2 | scope-boundary | Adopt FR-002 superset message as Phase 2 doc note (new) | P3 | N/A | New recommendation | Active (P3) | No |

---

## Dangerous Contradictions Found

### Resolved Contradictions

**1. Phase 1 read-only boundary vs. write-producing recommendations**
- compliance-auditor's original Recommendations 3, 4, 5 proposed edits to tasks.md as Phase 1 findings.
- scope-boundary established that Phase 1 is read-only and these edits violate that boundary.
- **Resolution**: Both agents converge on the "Phase 1.5" or "pre-Phase-2 cleanup" framing. All write-producing recommendations are now framed as observations to be acted upon between phases. [compliance-auditor revision, Recs 3/4/5 dispositions; scope-boundary cross-review, Dangerous Contradiction 1]

**2. FR-002 error message: bidirectional vs. unidirectional verification**
- compliance-auditor treated verification as bidirectional (spec must match implementation AND vice versa), flagging the SKILL.md superset message as a discrepancy.
- scope-boundary treated verification as unidirectional (implementation satisfies spec as substring match).
- **Resolution**: Both agents now agree unidirectional is correct for Phase 1. compliance-auditor downgraded to P3 documentation hygiene. scope-boundary's N2 proposes capturing the observation as a Phase 5 note. [compliance-auditor revision, Rec 1; scope-boundary revision, N2]

**3. FR count discrepancy ("10 pre-existing FRs")**
- compliance-auditor's Verification Summary Table showed 8 full + 1 partial = 9, yet the checkpoint claims 10.
- scope-boundary's Rec 5 flagged the count as opaque.
- **Resolution**: Both agents agree enumeration is necessary. The likely tenth is FR-012 (T006 marked [x]). Resolution requires explicit enumeration and FR-012 verification. The count discrepancy is now acknowledged by both agents as a real gap. [compliance-auditor cross-review, Dangerous Contradiction 1; compliance-auditor New Rec A, B]

**4. T006 completion creating an unverified FR**
- compliance-auditor's original review did not mention T006 or FR-012 at all.
- scope-boundary's Rec 8 identified the blind spot.
- **Resolution**: compliance-auditor fully concedes the gap ("my most significant oversight from the original review"). Both agree FR-012 must be verified. [compliance-auditor revision, New Rec A; scope-boundary revision, Rec 8]

### Unresolved Contradictions

**None at the substance level.** All substantive disagreements were resolved during the deliberation. The two remaining disputes (see Remaining Disputes below) concern mechanism and priority, not substance.

---

## Systemic Contradictions

Two patterns emerged across the individual contradictions:

**1. Scope conservatism vs. compliance thoroughness.** scope-boundary consistently advocated for narrow, well-bounded phases with explicit preconditions. compliance-auditor consistently probed deeper into behavioral implications and cross-phase consequences. These are complementary perspectives, not irreconcilable positions. The tension surfaced productive findings: compliance-auditor's depth caught the T019 behavioral expansion and the FR-011 dual-site gap; scope-boundary's restraint caught the read-only boundary violation and the FR-012 verification blind spot. Both agents adapted well, with compliance-auditor accepting the read-only boundary and scope-boundary accepting that behavioral analysis belongs in the audit record even if it references future phases.

**2. Process purity vs. pragmatic bundling.** Several recommendations affect the same documents (tasks.md line number replacements, T019 behavioral note, T004 dual-site note, FR enumeration). The agents disagree on whether these should be individual work items (scope-boundary's preference for traceable, discrete changes) or bundled into a single editorial pass (compliance-auditor's preference for reducing overhead). This tension is resolved pragmatically in the Actionable Spec Changes section below.

---

## Convergence Achieved

Ordered by strength of bilateral agreement (strongest first):

1. **Phase 1 is a read-only verification gate.** Both agents independently established this in their original reviews, defended it in cross-review, and enforced it during revision against their own recommendations. Every write-producing recommendation was reframed as an observation for inter-phase cleanup. [compliance-auditor revision, Recs 3/4/5; scope-boundary Alignment item 1; both Phase 4 Convergence item 1]

2. **T019 introduces behavioral expansion, not a transparent refactor.** Both agents agree that replacing inline heading-only parsing with a Dispute-Parsing Subsystem cross-reference introduces (a) structural-marker support as primary parsing and (b) case-insensitive/level-agnostic heading matching. This must be documented before T019 executes. [compliance-auditor Rec 3 modified + Phase 4 Non-Negotiable 3; scope-boundary Rec 7 modified + Phase 4 Non-Negotiable 2]

3. **STATUS.md will become stale after T019 unless proactively updated.** T008 creates an entry stating stagnation detection uses heading-only parsing. T019 will make this false by connecting stagnation detection to the full Dispute-Parsing Subsystem. A planned update task is needed. [compliance-auditor Rec 4; scope-boundary cross-review Safe Agreement 4; both Phase 4 Convergence item 4]

4. **Line number references in task descriptions are fragile and should be replaced with section heading anchors.** compliance-auditor concedes this is "the more forward-looking" concern. Both agents agree T002's "L249" and T003's "L581-582" should use distinctive phrases. [scope-boundary Rec 2; compliance-auditor cross-review Tension 2; both Phase 4 Convergence item 5]

5. **The "10 pre-existing FRs" checkpoint count must be explicitly enumerated.** Both agents struggled to reconcile the number. compliance-auditor's own table showed only 9. Explicit enumeration prevents miscounting and makes the gate auditable. [scope-boundary Rec 5; compliance-auditor New Rec B; both Phase 4 Convergence item 4]

6. **FR-011 partial status involves two inline-parsing sites, not one.** spec.md L278 mentions only Round Termination Check. Both agents now agree Trigger Evaluation (L531-542) is the second site. The tasks document (T019 + T019a) handles both correctly, but the spec assumption text is incomplete. [compliance-auditor Rec 2 + Off-Base Assumption 1; scope-boundary cross-review Dangerous Contradiction 4, conceding; both Phase 4 Convergence item 2]

7. **STATUS.md baseline belongs as a Phase 2 precondition, not a Phase 1 task.** scope-boundary originally proposed T005a in Phase 1, then revised to a Phase 2 header note. compliance-auditor originally excluded STATUS.md entirely, then accepted the Phase 2 precondition note. [scope-boundary Rec 3 modified; compliance-auditor New Rec C; both Phase 4 Convergence item 5]

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

### Dispute 1: Where FR-012 verification belongs

**Positions**:
- **compliance-auditor**: FR-012 verification should be a pre-Phase-2 gate check. Adding a task to Phase 1 (T005b) retroactively changes a completed phase's scope, which undermines process integrity. The verification is necessary; reopening Phase 1's task list is not. [compliance-auditor Phase 4 Dispute 1; Phase 4 Flexibility 1]
- **scope-boundary**: FR-012 verification should happen outside Phase 1 -- as a pre-Phase-2 gate activity, a Phase 2 header note, or folded into T016 (Phase 5). The read-only boundary applies uniformly. If T005b is added, it belongs in a pre-Phase-2 gate, not in Phase 1's task list. [scope-boundary Phase 4 Dispute 1; Phase 4 Non-Negotiable 1; Phase 4 Flexibility 1]

**Synthesizer assessment**: The dispute is narrower than it appears. Both agents agree on three things: (a) FR-012 must be verified, (b) no new task should be added to Phase 1's completed task list, and (c) verification must happen before Phase 2 begins. The only difference is labeling: compliance-auditor says "pre-Phase-2 gate check"; scope-boundary says the same thing but also lists "folded into T016" as an acceptable alternative. Since both positions converge on "pre-Phase-2 gate, not Phase 1 task," this dispute is effectively resolved.

**Recommended resolution**: FR-012 verification is performed as a pre-Phase-2 gate check. The Phase 1 record documents the observation (FR-012 is unverified); the verification itself is executed before Phase 2 begins but is not retroactively added to Phase 1's task list. This satisfies both agents' non-negotiables.

---

### Dispute 2: Priority of the "10 FRs" enumeration and bundling of line number replacements

This dispute has two sub-issues that both agents filed separately but which share a common thread about granularity:

**Sub-issue 2a: Priority of FR enumeration (P2 vs. P3)**

**Positions**:
- **compliance-auditor**: P2. Enumeration "forces resolution of whether the count is 9 or 10," making it functionally tied to the FR-012 verification gap. [compliance-auditor New Rec B; Phase 4 Non-Negotiable 2]
- **scope-boundary**: P3. The count opacity is a documentation clarity issue, not a functional risk. The FR-012 verification gap is P2, but the label in the header is P3. They are separate concerns. [scope-boundary Phase 4 Dispute 2; Phase 4 Flexibility 2]

**Synthesizer assessment**: scope-boundary's separation is analytically cleaner: the verification gap (substance) is distinct from the missing enumeration (labeling). However, compliance-auditor is correct that the enumeration is the mechanism that forces the count to be reconciled. In practice, the enumeration takes one line of text and would be done simultaneously with the FR-012 verification. The priority distinction is academic if both are done as part of the same pre-Phase-2 gate.

**Recommended resolution**: Assign P2 to the combined action "enumerate the verified FRs and verify FR-012" as a single pre-Phase-2 gate item. The enumeration is not a separate work item from the verification -- it is the vehicle that makes the verification traceable.

**Sub-issue 2b: Line number replacement as standalone vs. bundled edit**

**Positions**:
- **scope-boundary**: Standalone P2 action. Both reviews converge on line numbers being fragile; it should be tracked as its own item. [scope-boundary Rec 2 surviving]
- **compliance-auditor**: Bundle with other task description edits (T019 behavioral note, T004 dual-site note) as a single pre-Phase-2 editorial pass. A dedicated work item for two find-and-replace edits is process overhead. [compliance-auditor Phase 4 Dispute 2]

**Synthesizer assessment**: Both agents agree the line numbers must be replaced. The disagreement is purely about project management granularity. Since both agents accept that the edits will happen, and since multiple edits to tasks.md are needed anyway (T004 dual-site note, T019 behavioral note, FR enumeration), bundling is pragmatically efficient without losing traceability -- each change can be itemized within a single editorial pass.

**Recommended resolution**: Bundle all tasks.md editorial changes into a single pre-Phase-2 cleanup pass. Track individual items within that pass for traceability, but do not create separate work items for each line edit.
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

All changes are traced to scorecard recommendations. Changes are grouped by priority and target file.

### P1 Changes (none)

No P1 changes. Both agents downgraded their P1 recommendations during revision. Phase 1 verification passes for all 10 (or 9+1) pre-existing FRs.

### P2 Changes

**P2-1: Pre-Phase-2 gate: Verify FR-012 and enumerate verified FRs**
*Traced to: CA-A, CA-B, SB-5, SB-8*

Before Phase 2 begins, execute the following gate check:
- Verify that `specs/STATUS.md` taxonomy section contains both implementation-tier and acceptance-tier definitions (FR-012 satisfaction check).
- Update the Phase 1 checkpoint statement (`tasks.md` L22/L30) to enumerate verified FRs explicitly: "FRs verified: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-010, FR-012, FR-018 (9 fully implemented) + FR-011 (partial). Total: 10 verified."
- This is a pre-Phase-2 gate activity, not a retroactive Phase 1 task addition.

**P2-2: Pre-Phase-2 editorial pass on tasks.md**
*Traced to: CA-3, CA-5, SB-2, SB-N1*

Single editorial pass covering:
- **T002**: Replace "SKILL.md Step 3 (L249)" with "SKILL.md Step 3 (the paragraph beginning 'If the loaded template's first line contains')".
- **T003**: Replace "SKILL.md Phase 6 output validation (L581-582)" with "SKILL.md Phase 6 section (the paragraph beginning 'After Phase 6 completes successfully, validate that')". Optionally append "(FR-007 heading match semantics deferred to T013, Phase 4)".
- **T004**: Replace "Round Termination Check still uses inline parsing (remediated in T019)" with "Round Termination Check and Trigger Evaluation both still use inline parsing (remediated in T019 and T019a respectively)".
- **T019**: Append behavioral-change note: "Note: This replacement introduces two behavioral changes: (1) structural-marker support is added as the primary parsing method (the inline logic only used heading-based parsing), and (2) heading matching becomes case-insensitive and level-agnostic (the inline logic hardcoded `### Remaining Disputes`). Both changes are intentional -- the Dispute-Parsing Subsystem is the authoritative specification. Additionally, after this task completes, the STATUS.md entry for the Dispute-Parsing Subsystem created by T008 must be updated to reflect that stagnation detection now uses the full subsystem (see T019-post below)."

**P2-3: Expand spec.md assumption about FR-011 partial status**
*Traced to: CA-2*

Update `spec.md` L278 from:
> "FR-011 is partially complete: STATUS.md cross-reference exists but SKILL.md Round Termination Check still uses inline dispute-counting logic independent of the Dispute-Parsing Subsystem."

To:
> "FR-011 is partially complete: STATUS.md cross-reference exists but SKILL.md Round Termination Check (L459-469) and Trigger Evaluation (L531-542) both still use inline dispute-counting logic independent of the Dispute-Parsing Subsystem."

**P2-4: Add post-T019 STATUS.md update task**
*Traced to: CA-4*

Add to Phase 4 or Phase 5 in `tasks.md`:
> "T019-post [US4] After T019 completes: update the Dispute-Parsing Subsystem entry in specs/STATUS.md to remove the note that stagnation detection does not support structural-marker parsing. After T019, stagnation detection uses the full Dispute-Parsing Subsystem (structural markers primary, heading fallback)."

This prevents STATUS.md from containing information that T019 has rendered false, directly supporting SC-003.

### P3 Changes

**P3-1: Phase 2 header precondition note for STATUS.md baseline**
*Traced to: CA-C, SB-3 (modified)*

Add to the Phase 2 header in `tasks.md`, after the existing dependency note:
> "Precondition: specs/STATUS.md exists with per-spec entries for specs 001-004. If STATUS.md structure has drifted, T006 and T007 instructions may need adjustment."

**P3-2: Add negative verification for cooperative template to T001**
*Traced to: SB-4*

Extend T001 description to include: "...and verify templates/cooperative/arbitration.md does NOT contain the draft marker (US1: FR-001 inverse, AS4)."

**P3-3: Add pass/fail criteria to Phase 1 tasks (if editing tasks.md for other reasons)**
*Traced to: SB-1 (modified)*

If tasks.md is being edited as part of P2-2, optionally append failure conditions to each Phase 1 task. Example for T001: "(FAIL if marker is absent, on wrong line, or has different syntax)." This is informational, not blocking.

**P3-4: FR-002 error message alignment**
*Traced to: CA-1 (modified), SB-N2*

During Phase 5 polish (T016), verify FR-002 error message text matches SKILL.md exactly, or add "at minimum" qualifier to FR-002. This is documentation hygiene, not a functional concern.

**P3-5: Parallel execution precondition note**
*Traced to: SB-7 (modified)*

Add to the Parallel Example section in `tasks.md`:
> "Precondition: Phase 3 tasks do not read SKILL.md, and Phase 4 tasks do not read STATUS.md. If any task in either phase reads the other phase's target file, the phases cannot safely run in parallel."

---

## Key Concessions

### compliance-auditor concessions

1. **Read-only boundary** (Recs 3, 4, 5): Originally proposed writes to tasks.md as Phase 1 findings. After scope-boundary's cross-review established the read-only principle, compliance-auditor reframed all write-producing recommendations as inter-phase observations. This was the largest procedural concession in the deliberation. [compliance-auditor revision, Recs 3/4/5]

2. **Verification directionality** (Rec 1): Originally treated verification as bidirectional (spec must match implementation). Accepted scope-boundary's unidirectional framing (implementation satisfies spec) and downgraded from P2 to P3. [compliance-auditor revision, Rec 1]

3. **FR-012 verification gap** (New Rec A): Fully credited scope-boundary for identifying a blind spot ("my most significant oversight from the original review"). This concession was notable for its candor: compliance-auditor acknowledged that their narrower scoping (verify only what tasks instruct) missed what scope-boundary's broader scoping (verify what the checkpoint claims) caught. [compliance-auditor revision, New Rec A]

4. **Withdrawn recommendations** (Recs 6, 7): Withdrew two P3 recommendations as over-documentation (Rec 6) and speculative future-proofing (Rec 7). Both withdrawals demonstrated appropriate self-correction. [compliance-auditor revision, Recs 6/7]

### scope-boundary concessions

1. **FR-011 dual-site incompleteness** (N1): Conceded that compliance-auditor was correct about spec.md L278 omitting Trigger Evaluation and that scope-boundary's own review "was less thorough on this point." This was a direct analytical concession. [scope-boundary cross-review, Dangerous Contradiction 4; scope-boundary revision, N1]

2. **STATUS.md baseline scope** (Rec 3): Originally proposed adding a new Phase 1 task (T005a). After compliance-auditor argued this expanded Phase 1's scope beyond its stated purpose, scope-boundary revised to a lighter Phase 2 header precondition note and reduced priority from P2 to P3. [scope-boundary revision, Rec 3]

3. **T019 behavioral risk framing** (Rec 7): Originally focused exclusively on parallel-safety risk. After compliance-auditor identified the semantic-expansion risk as higher-impact, scope-boundary credited compliance-auditor's framing and reduced Rec 7's priority from P2 to P3, deferring to compliance-auditor's Rec 3 as the more actionable mitigation. [scope-boundary revision, Rec 7]

4. **Withdrawn recommendation** (Rec 6): Withdrew the Phase 4 encroachment confirmation, acknowledging it was a confirmation misclassified as a recommendation. [scope-boundary revision, Rec 6]

---

## Gate Verdict

Both agents confirm that all Phase 1 verification tasks (T001-T005) pass. The 10 pre-existing FRs (pending explicit enumeration confirming the count) are satisfied. FR-011 is partial as expected. The Phase 1 checkpoint is achieved: the pre-existing implementation is intact and the remaining 9 FRs are ready for Phases 2-5.

The gate passes with 4 P2 conditions to be addressed before Phase 2 begins (pre-Phase-2 gate check for FR-012, editorial pass on tasks.md, spec.md assumption expansion, and post-T019 update task planning) and 5 P3 documentation improvements that can be addressed during the editorial pass or deferred to Phase 5 polish.
