# Phase 3 Review — scope-boundary

**Agent**: scope-boundary
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening

---

### Executive Summary

Phase 3 adds five categories of content to `specs/STATUS.md`: shared subsystems (T008), cross-spec dependencies (T009), risk-of-gap statements (T010), effort estimates (T011), a SKILL.md structure plan (T012), and a spec 005 self-entry (T012a). All six tasks have been marked complete in `tasks.md` (L63-68). The scope of this phase is constrained to STATUS.md enrichment only — no taxonomy modifications, no acceptance-label changes, no SKILL.md edits.

From a scope-boundary perspective, the current STATUS.md (L66-138) is mostly well-bounded. The additions stay within their designated file, do not redefine Phase 2's taxonomy, and do not touch SKILL.md. However, there are several areas where Phase 3 content either encroaches on Phase 2 territory, introduces forward references to Phase 4 work, or creates structural ambiguities that could cause problems when the document is maintained over time. The spec 005 self-entry (T012a) is handled cleanly and avoids circular self-reference, though the risk-of-gap statement for spec 005 contains a forward reference to STATUS.md itself that warrants scrutiny.

The most important recommendation is to add the dual-condition transition criteria that Phase 2's synthesis recorded as a binding commitment for T008 (Phase 2 final.md, L202), which is absent from the current STATUS.md.

### Alignment

- **Shared Subsystems section stays in STATUS.md** (STATUS.md L86-104): All three subsystem entries (Dispute-Parsing, Structural Markers, Template Conventions) are documented within STATUS.md, not in SKILL.md or a new file. This respects Phase 3's single-file scope. `[tasks.md, L63]` specifies STATUS.md as the target.

- **No taxonomy modifications** (STATUS.md L3-24): The Taxonomy section, including the Implementation Tier (L7-13), Acceptance Tier (L15-20), and Interpreting the Two Tiers (L22-24), is unchanged from Phase 2. Phase 3 correctly left these definitions untouched. `[conversus.yml, L77-78]` — my mandate is to flag taxonomy changes, and none exist.

- **No acceptance label changes on specs 001-004** (STATUS.md L30-56): The per-spec acceptance labels ("Feature-complete", "Spec-complete", "Not started") are identical to Phase 2's output. Phase 3 added Risk-of-Gap and Effort fields without altering the labels Phase 2 established. `[conversus.yml, L78]` — flagging acceptance label changes is part of my job.

- **No SKILL.md changes** (Phase 3 scope): The SKILL.md Structure Plan section (STATUS.md L66-84) documents future SKILL.md changes without making them. This correctly defers execution to Phase 4. `[tasks.md, L74-93]` places SKILL.md edits in Phase 4.

- **Spec 005 self-entry avoids circularity** (STATUS.md L58-64): The entry describes spec 005's own state without creating a recursive dependency. It references its gaps (FR-007, FR-011, FR-014, FR-015) and its dependencies (specs 001, 002, 004) without making spec 005's status contingent on its own STATUS.md entry. `[spec.md, L279]` acknowledges the self-tracking requirement.

- **Dependency graph includes spec 005** (STATUS.md L117): The cross-spec dependency graph at L110-118 includes spec 005, which is correct since T012a added spec 005 to the status section and T009 should reflect all tracked specs. `[tasks.md, L64]` specifies the dependency graph should show the recommended implementation order.

### Missed Opportunities

- **Transition criteria omitted from T008**: Phase 2's synthesis explicitly recorded a binding commitment (Phase 2 final.md, L202): "T008 must add transition criteria to the taxonomy section." The agreed formulation is: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." This is absent from STATUS.md. T008's task description (tasks.md, L63) mentions "maintenance note" but the transition criteria were recorded as an explicit T008 input. This is a Phase 2 binding output that Phase 3 was obligated to implement. Impact: **high**.

- **No "Depends On" field for spec 001**: STATUS.md L30-35 (spec 001) has no "Depends On" field. Specs 002 (L39), 003 (L46), 004 (implied by subsystem entries), and 005 (L61) all have dependency information. Spec 001 is foundational with no dependencies, but the field should be present with a value like "(none — foundational)" for consistency with the dependency graph at L111. This was specified in T009's task (tasks.md, L64) which requires the dependency information to be cross-referenced. Impact: **medium**.

- **No "Depends On" field for spec 004**: STATUS.md L51-56 (spec 004) lacks an explicit "Depends On" field. The dependency graph at L116 shows "(none — self-contained engine)" but this is not reflected in the per-spec entry. For the same consistency reason as spec 001. Impact: **low**.

- **Spec 003 acceptance label "Not started" not updated to "Not assessed"**: STATUS.md L45 shows `**Acceptance**: Not started`. Phase 2's synthesis (final.md, L188) recorded as P1 item 2: "Apply 'Not assessed' label to spec 003: Update STATUS.md L41 from `**Acceptance**: Not started` to `**Acceptance**: Not assessed`." The current STATUS.md still shows "Not started." This is a Phase 2 deliverable that was not completed, but since my Phase 3 scope is to flag rather than fix Phase 2 items, I note this as a pre-existing gap that Phase 3 inherited. The acceptance tier taxonomy (L15-20) defines "Feature-complete" and "Spec-complete" but does not define "Not started" or "Not assessed" — meaning L45 uses a label not in the taxonomy, violating FR-009. Impact: **high** (but Phase 2 scope).

- **Compound-label permission rule missing from taxonomy**: Phase 2's synthesis (final.md, L192) recorded as P1 item 4: add compound-label permission rule to Implementation Tier section. STATUS.md L7-13 does not contain this rule, yet L52 uses a compound label. Again, this is a Phase 2 deliverable — I flag it but do not recommend Phase 3 fix it, as that would be a taxonomy modification. Impact: **medium** (but Phase 2 scope).

- **Maintenance note lacks specificity about what triggers updates**: The maintenance note at L138 states: "This document MUST be updated when any spec's implementation or acceptance status changes (FR-008a)." This covers label changes but does not cover updates to Risk-of-Gap, Effort, Shared Subsystems stability, or the Structure Plan. These sections could become stale without triggering the maintenance obligation. Impact: **low**.

- **SKILL.md Structure Plan lacks spec 005 entry**: STATUS.md L66-84 documents structure plans for specs 002, 003, and 004. Spec 005's SKILL.md changes (FR-007, FR-011, FR-014, FR-015 — all Phase 4 tasks) are not represented in the structure plan. T012 (tasks.md, L67) specifies "specs 002, 003, 004" but spec 005 also has pending SKILL.md work. The structure plan is incomplete as a forward-looking reference. Impact: **low**.

### Off-Base Assumptions

- **Spec 003 "Not started" label is consistent with the taxonomy**: STATUS.md L45 uses `**Acceptance**: Not started` but the Acceptance Tier taxonomy (L15-20) defines only "Feature-complete" and "Spec-complete." Phase 2's synthesis unanimously agreed to add "Not assessed" as a third label (final.md, L186-188) and to apply it to spec 003. The current STATUS.md assumes "Not started" is a valid acceptance label — it is not defined in the taxonomy. This is not a Phase 3 assumption error (Phase 3 did not change this label), but it is a pre-existing inaccuracy that Phase 3's content builds upon. The dependency graph and implementation ordering at L120-129 assume the status entries are accurate.

- **The maintenance note covers all living-document obligations**: STATUS.md L138 scopes the maintenance trigger to "implementation or acceptance status changes." However, Phase 3 added sections (Shared Subsystems, Structure Plan) that are also living content. A subsystem's stability could change, a consumer could be added, or the structure plan could become outdated — none of these would trigger the maintenance obligation as currently worded. The assumption that L138 fully captures FR-008's intent is incorrect; FR-008 (spec.md, L215) says "STATUS.md MUST be updated when any spec's implementation or acceptance status changes," which is narrower than the full scope of content now in the document.

### Actionable Recommendations

1. **Add transition criteria to STATUS.md** (Priority: P1)
   - **Current state**: STATUS.md has no transition criteria. The Taxonomy section (L3-24) defines labels but not when they change.
   - **Proposed change**: Add after L24 (after "Interpreting the Two Tiers" paragraph), a new subsection or paragraph: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied."
   - **Rationale**: Phase 2's synthesis recorded this as a binding commitment for T008 implementation `[Phase 2 final.md, L202]`. The dual-condition formulation was a bilateral convergence point `[Phase 2 final.md, L152-156]`. T008 is marked complete but this obligation is unmet.
   - **Risk if ignored**: The boundary between "Feature-complete" and "Spec-complete" is implicit. Future label transitions could be applied inconsistently, undermining the taxonomy's purpose.

2. **Resolve spec 003 acceptance label** (Priority: P1)
   - **Current state**: STATUS.md L45 uses `**Acceptance**: Not started`. The taxonomy (L15-20) does not define "Not started" as an acceptance label.
   - **Proposed change**: This is a Phase 2 deliverable (final.md, L188). Two options: (a) add "Not assessed" to the Acceptance Tier taxonomy at L20 and update L45, or (b) flag as a Phase 2 incomplete that blocks Phase 3's checkpoint claim. I recommend option (a) since Phase 2's synthesis unanimously agreed on this change.
   - **Rationale**: FR-009 (spec.md, L216) requires status labels to use the defined convention. An undefined label violates this requirement. `[Phase 2 final.md, L186-188]` — unanimous P1 convergence.
   - **Risk if ignored**: STATUS.md uses a label the taxonomy does not define. The Phase 2 checkpoint claim that "STATUS.md taxonomy is authoritative" (tasks.md, L47) is falsified. Phase 3's content inherits this inconsistency.

3. **Add "Depends On" field to spec 001 entry** (Priority: P2)
   - **Current state**: STATUS.md L30-35 (spec 001) has no "Depends On" field. The dependency graph at L111 shows "(none — foundational)" but this is not in the per-spec entry.
   - **Proposed change**: Add `**Depends On**: (none — foundational)` to spec 001's entry, after the Notes field.
   - **Rationale**: L129 states "Per-spec entries are authoritative; this section provides the cross-cutting view." If per-spec entries are authoritative for dependencies, spec 001 should have a "Depends On" field even if the value is "none." `[tasks.md, L64]` requires the dependency information in STATUS.md.
   - **Risk if ignored**: An implementor reading spec 001's entry cannot confirm it has no dependencies without checking the separate dependency graph. Minor inconsistency.

4. **Add "Depends On" field to spec 004 entry** (Priority: P2)
   - **Current state**: STATUS.md L51-56 (spec 004) has no "Depends On" field. L116 shows "(none — self-contained engine)."
   - **Proposed change**: Add `**Depends On**: (none — self-contained engine)` to spec 004's entry.
   - **Rationale**: Same as recommendation 3. Per-spec entries should be authoritative and self-contained. `[STATUS.md, L129]`.
   - **Risk if ignored**: Same as recommendation 3. Minor inconsistency.

5. **Verify compound-label rule was implemented** (Priority: P2)
   - **Current state**: STATUS.md L52 uses a compound implementation label ("Implementation-complete (core) / Not started (discovery)") but the Implementation Tier taxonomy (L7-13) does not define compound-label rules.
   - **Proposed change**: Verify whether the compound-label permission rule from Phase 2's synthesis (final.md, L192) was intentionally deferred or accidentally omitted. If omitted, add it to L13: "Specs with independently-implementable subsystems may use compound labels composed of existing tier values. Each component must use a defined implementation-tier label."
   - **Rationale**: Using a format the taxonomy does not define is the same category of issue as using an undefined label. `[Phase 2 final.md, L192]` — recorded as P1 actionable change.
   - **Risk if ignored**: The compound label at L52 has no formal backing, creating precedent for ad-hoc label formats.

6. **Broaden maintenance note scope** (Priority: P3)
   - **Current state**: L138 limits the maintenance trigger to "implementation or acceptance status changes."
   - **Proposed change**: Amend to: "This document MUST be updated when any spec's implementation or acceptance status changes, when shared subsystem stability or consumers change, or when the SKILL.md Structure Plan is affected by implementation progress (FR-008a)."
   - **Rationale**: Phase 3 added three new section types (Shared Subsystems, Structure Plan, Risk/Effort) that are living content but not covered by the maintenance trigger. FR-008 (spec.md, L215) mentions status changes specifically, but the spirit of a "living document" (spec.md, L286) extends to all sections. `[spec.md, L286]`.
   - **Risk if ignored**: Shared Subsystems or Structure Plan could become stale without anyone feeling obligated to update them.

7. **Add spec 005 to SKILL.md Structure Plan** (Priority: P3)
   - **Current state**: STATUS.md L66-84 covers specs 002, 003, 004 only. Spec 005 has pending SKILL.md changes (FR-007, FR-011, FR-014, FR-015 per tasks.md L86-90).
   - **Proposed change**: Add a `### 005 — P2/P3 Backlog Hardening` entry to the Structure Plan section: "**Status**: Needs additions. **Changes required**: Phase 6 heading match semantics (FR-007), dispute-parsing cross-references in Round Termination Check and Trigger Evaluation (FR-011), Phase 4 missing document edge case (FR-014), Phase 6 overwrite semantics (FR-015)."
   - **Rationale**: T012 (tasks.md, L67) only names specs 002, 003, 004, but FR-019 (spec.md, L250) says "future spec implementations" without limiting to those three. Spec 005 has more pending SKILL.md work than any other spec. `[tasks.md, L86-90]`.
   - **Risk if ignored**: An implementor consulting the Structure Plan for guidance before Phase 4 would not see spec 005's SKILL.md changes listed, despite those being the next items to implement.

8. **Add "Not assessed" acceptance label to taxonomy** (Priority: P1)
   - **Current state**: The Acceptance Tier (L15-20) defines only "Feature-complete" and "Spec-complete." Spec 003 (L45) uses "Not started" which is not in the taxonomy.
   - **Proposed change**: Add to L20: `- **Not assessed**: No acceptance criteria have been evaluated.`
   - **Rationale**: Phase 2 unanimously agreed on this `[Phase 2 final.md, L186-187]`. FR-012 (spec.md, L225) requires the convention to be documented. FR-009 (spec.md, L216) requires labels to use the convention. This appears to be a Phase 2 implementation gap that Phase 3 inherited. Adding it now is a prerequisite for Phase 3's checkpoint claim (SC-003, spec.md L265) since an implementor reading STATUS.md alone would find an undefined label.
   - **Risk if ignored**: STATUS.md's taxonomy is incomplete. Any agent or implementor validating labels against the taxonomy will find an inconsistency.

### Referenced Documentation

- `conversus/specs/STATUS.md` — sections/lines cited: L3-24, L30-35, L39, L45, L46, L51-56, L58-64, L66-84, L86-104, L106-129, L134, L138
- `conversus/specs/005-p2p3-backlog-hardening/spec.md` — sections/lines cited: L215-216, L225-226, L250, L265, L279, L286
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` — sections/lines cited: L44-45, L47, L63-68, L64, L67, L74-93, L86-90
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-2/summary/final.md` — sections/lines cited: L152-156, L186-188, L192, L202
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-3/cooperative/conversus.yml` — sections/lines cited: L72, L77-78, L84-86
