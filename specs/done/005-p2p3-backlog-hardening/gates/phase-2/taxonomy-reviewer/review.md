# Taxonomy Reviewer — Phase 2 Review

**Reviewer**: taxonomy-reviewer
**Date**: 2026-03-20
**Gate**: Phase 2 (Two-Tier Status Convention)
**Spec**: 005-p2p3-backlog-hardening
**Target files**: `specs/STATUS.md`, `specs/005-p2p3-backlog-hardening/spec.md`, `specs/005-p2p3-backlog-hardening/tasks.md`

---

### Executive Summary

Spec 005 Phase 2 defines a two-tier acceptance convention ("feature-complete" / "spec-complete") to sit alongside the existing implementation tier in `specs/STATUS.md`, then applies acceptance labels to all four existing specs. The purpose is foundational: Phase 3 enrichment (shared subsystems, risk-of-gap, effort, structure plan) depends on the taxonomy being unambiguous, and the convention itself was born from a labeling disagreement during the self-audit cross-review. The taxonomy exists to prevent exactly the kind of ambiguity that stalled the self-audit.

The implementation in STATUS.md is solid. The taxonomy section (L3-24) defines both tiers clearly, the definitions match FR-012 exactly, and the "Interpreting the Two Tiers" paragraph (L22-24) correctly establishes orthogonality. Spec 001 is labeled "feature-complete" with gaps FR-023, FR-025, FR-026 per FR-013. Specs 002, 003, and 004 all carry acceptance labels per FR-009. The convention is well-structured and will support Phase 3 without ambiguity for the common cases.

However, there are three areas where the taxonomy falls short of being fully authoritative: (1) the acceptance tier has only two labels but STATUS.md uses "Not started" for spec 003, creating a three-state system that is not defined in the taxonomy, (2) the gap list for spec 001 has a subtle discrepancy between the spec's US5 AS3 and FR-013, and (3) spec 004's split-label format for the implementation tier is a deviation from the taxonomy's three-label system that is not explained. My most important recommendation: formalize "Not started" as a valid acceptance-tier label, or explain why spec 003's acceptance status falls outside the two-tier convention.

### Alignment

- **Two-tier taxonomy structure** (STATUS.md L3-20): The taxonomy section cleanly separates implementation tier (L7-13) and acceptance tier (L15-20) under distinct headings, each with a brief purpose statement ("Tracks whether...") followed by enumerated labels. This matches FR-012's requirement for a two-tier status convention exactly: "feature-complete" (all major capabilities present, acceptance criteria gaps remain) and "spec-complete" (all acceptance criteria met). [`spec.md`, L225]

- **FR-012 definition fidelity** (STATUS.md L19-20): The "feature-complete" definition ("All major capabilities are present, but acceptance criteria gaps remain") and "spec-complete" definition ("All acceptance criteria are met. The spec is fully satisfied.") are faithful to the spec wording at `spec.md` L225. The parenthetical example in "feature-complete" ("e.g., missing template instructions, incomplete edge case documentation") is a useful, non-distorting addition that grounds the abstraction in a concrete case.

- **Spec 001 gap list** (STATUS.md L31-33): Spec 001 is labeled "feature-complete" with three documented gaps: FR-023, FR-025, FR-026. This matches FR-013 (`spec.md` L226) exactly. The FR-023 parenthetical ("SKILL.md validation logic exists but template-level heading instructions pending") adds useful context that aligns with spec 001's own FR-023 definition at `001-subject-arbitration/spec.md` L173.

- **Orthogonality explanation** (STATUS.md L22-24): The "Interpreting the Two Tiers" paragraph explicitly states the tiers are orthogonal and gives two concrete examples (implementation-complete but only feature-complete; partially-complete but spec-complete for its subset). This is the right level of explanation to prevent the labeling disagreements the convention was designed to resolve, per US5 (`spec.md` L77-90).

- **All four specs carry acceptance labels** (STATUS.md L30-49): Spec 001 has "Feature-complete", spec 002 has "Spec-complete", spec 003 has "Not started", spec 004 has "Feature-complete". This satisfies FR-009 (`spec.md` L216): "Status labels MUST use the two-tier convention defined in FR-012/FR-013."

### Missed Opportunities

- **"Not started" is not a defined acceptance-tier label**: The acceptance tier taxonomy (STATUS.md L17-20) defines exactly two labels: "feature-complete" and "spec-complete." Yet spec 003 (STATUS.md L41) uses "Not started" as its acceptance label. This is not a label in the acceptance tier. FR-012 (`spec.md` L225) only establishes two labels. If "Not started" is valid for acceptance, it must be defined in the taxonomy alongside the other two. If it is borrowed from the implementation tier, the taxonomy must say so. Currently, a reader must infer this on their own, which is exactly the ambiguity the convention was supposed to eliminate. Impact: **high** — undermines the taxonomy's claim to be authoritative for all acceptance labels.

- **No guidance for edge-case label combinations**: The orthogonality paragraph (STATUS.md L22-24) gives two examples (implementation-complete + feature-complete; partially-complete + spec-complete) but does not address the most confusing combinations: "Not started" + "Not started" (spec 003), or "Implementation-complete (core) / Not started (discovery)" (spec 004). An implementor trying to parse spec 004's compound implementation label against the taxonomy's three clean labels would find no guidance. Impact: **medium** — Phase 3 will add content to STATUS.md and may need to assign labels to spec 005 (per T012a in `tasks.md` L68); without guidance on compound labels, the Phase 3 implementor may invent their own format.

- **No explicit transition rules**: The taxonomy defines static labels but says nothing about when or how a spec transitions between them. When does "feature-complete" become "spec-complete"? When the gap list is empty? When someone manually changes the label? When all acceptance scenarios pass? FR-008 (`spec.md` L215) says STATUS.md "MUST be updated when any spec's implementation or acceptance status changes," but the taxonomy does not define the threshold for change. Impact: **medium** — without transition criteria, two reviewers could disagree about whether closing one of three gaps warrants relabeling.

- **FR-023 gap description inconsistency across documents**: Spec 005's US5 AS3 (`spec.md` L89) lists spec 001's gaps as "FR-025 (citation instructions), FR-026 (file attribution)" and notes "FR-023 is implemented in SKILL.md; template instructions pending." This framing treats FR-023 as a partial gap (implemented in SKILL.md, pending in templates). But FR-013 (`spec.md` L226) and STATUS.md (L32) both list FR-023 as a full gap alongside FR-025 and FR-026. The two framings are not contradictory, but they are not consistent either: US5 AS3 suggests two gaps plus a partial, while FR-013 and STATUS.md show three gaps. Impact: **medium** — a reviewer checking Phase 2 completion against US5 AS3 vs. FR-013 could reach different conclusions about whether the gap list is correctly applied.

- **Spec 004's acceptance label lacks gap documentation**: Spec 004 is labeled "Feature-complete" (STATUS.md L46) but has no explicit **Gaps** field listing which acceptance criteria are unmet. The taxonomy definition says feature-complete means "acceptance criteria gaps remain." If gaps remain, they should be listed, as they are for spec 001. The discovery section (FR-022-024) is listed under implementation, but it is unclear whether those same FRs represent the acceptance gaps or whether there are separate acceptance criteria that are unmet. Impact: **medium** — inconsistency with spec 001's treatment, where gaps are explicitly enumerated.

- **No label for "partially feature-complete"**: Spec 004's implementation tier uses a compound label: "Implementation-complete (core) / Not started (discovery)" (STATUS.md L46). This is a pragmatic representation of a partially-implemented spec with distinct subsystems. But the taxonomy (L11-13) does not account for this. "Partially-complete" is the closest match, yet that label does not convey that one entire subsystem is complete while another is untouched. The same pattern could apply to acceptance: a spec could be spec-complete for its core acceptance criteria but not-started for discovery acceptance criteria. Impact: **low** — this is a presentation/naming issue, not a functional one, and the compound format is readable even if not formally defined.

### Off-Base Assumptions

- **Spec 005 assumes two labels suffice for the acceptance tier**: FR-012 (`spec.md` L225) defines only "feature-complete" and "spec-complete." The implementation tier (STATUS.md L9-13) has three labels: implementation-complete, partially-complete, not started. The acceptance tier has only two. Yet STATUS.md itself immediately needs a third value ("Not started" for spec 003 at L41). The assumption that two labels are sufficient is contradicted by the first application of the convention. The correct understanding is that the acceptance tier needs at least three labels to cover specs that have no implementation and therefore have not had their acceptance criteria evaluated at all.

- **The spec assumes "feature-complete" and "spec-complete" are the only meaningful distinction**: US5 (`spec.md` L87-88) frames the convention as resolving a binary disagreement: "all major capabilities present but gaps remain" vs. "all acceptance criteria met." But the actual STATUS.md reveals at least four states: not started (003), feature-complete with enumerated gaps (001), feature-complete without enumerated gaps (004), and spec-complete (002). The two-tier convention collapses four observed states into two labels plus an undocumented third. The correct understanding is that the taxonomy should account for all states actually used, not just the two that motivated the convention.

### Actionable Recommendations

1. **Add "Not started" to acceptance tier** (Priority: P1)
   - **Current state**: Acceptance tier (STATUS.md L17-20) defines only "feature-complete" and "spec-complete." Spec 003 uses "Not started" (STATUS.md L41) without this being a defined acceptance label.
   - **Proposed change**: Add to the Acceptance Tier section: `- **Not started**: No acceptance criteria have been evaluated. The spec has no implementation to assess.`
   - **Rationale**: FR-009 (`spec.md` L216) requires status labels to "use the two-tier convention defined in FR-012/FR-013." If "Not started" is used but not defined, it violates FR-009's requirement that labels use the defined convention. The acceptance tier taxonomy must be exhaustive for all labels actually applied. [`spec.md`, L216, L225]
   - **Risk if ignored**: Phase 3 will add spec 005 to STATUS.md (T012a, `tasks.md` L68). The implementor must assign an acceptance label. Without "Not started" in the taxonomy, they face the same ambiguity for spec 005 (which is in-progress, not feature-complete, not spec-complete, and not really "not started" either). The taxonomy becomes incomplete on its first extension.

2. **Add explicit acceptance gaps to spec 004** (Priority: P1)
   - **Current state**: Spec 004 is labeled "Feature-complete" (STATUS.md L46) but has no **Gaps** field. Spec 001 (STATUS.md L32) lists gaps explicitly. The inconsistency is unforced.
   - **Proposed change**: Add a **Gaps** field to spec 004's entry identifying which acceptance criteria remain unmet (likely the discovery CLI commands FR-022-024, which are unimplemented and therefore their acceptance scenarios are untested).
   - **Rationale**: The taxonomy defines feature-complete as having "acceptance criteria gaps remain." If gaps remain, they must be documented for the label to be meaningful. Spec 001 sets the precedent. FR-009 (`spec.md` L216) requires labels to use the convention, and the convention implies gap documentation for feature-complete specs. [`STATUS.md`, L19, L32]
   - **Risk if ignored**: An implementor looking at spec 004's feature-complete label will not know which acceptance criteria are unmet, defeating the purpose of the label. The inconsistency with spec 001 creates a precedent conflict for Phase 3.

3. **Reconcile US5 AS3 gap list with FR-013 gap list** (Priority: P2)
   - **Current state**: FR-013 (`spec.md` L226) lists three gaps: FR-023, FR-025, FR-026. US5 AS3 (`spec.md` L89) lists two gaps (FR-025, FR-026) and treats FR-023 as a partially-implemented item ("implemented in SKILL.md; template instructions pending"). STATUS.md (L32) follows FR-013's three-gap formulation.
   - **Proposed change**: Either (a) align US5 AS3 to list all three gaps consistently with FR-013, or (b) add a parenthetical to FR-013 noting that FR-023 is a partial gap (SKILL.md logic exists, template instructions pending) to match US5 AS3's framing. Option (b) is more precise and already reflected in STATUS.md L32.
   - **Rationale**: US5 AS3 is the acceptance scenario against which Phase 2 completion is verified. If it says two gaps and FR-013 says three, a Phase 2 verification check will produce ambiguous results depending on which reference is consulted. [`spec.md`, L89, L226]
   - **Risk if ignored**: A future reviewer checking Phase 2 against US5 AS3 may flag STATUS.md as non-compliant because it lists three gaps where US5 AS3 implies two. Low functional risk, but this is exactly the kind of labeling ambiguity the convention was designed to prevent.

4. **Add transition criteria to taxonomy section** (Priority: P2)
   - **Current state**: The taxonomy (STATUS.md L7-24) defines static labels but has no guidance on when a spec moves between labels (e.g., from feature-complete to spec-complete).
   - **Proposed change**: Add a brief paragraph after "Interpreting the Two Tiers": "A spec transitions from feature-complete to spec-complete when all documented gaps are resolved and all acceptance scenarios in the spec pass. Transition updates must be recorded in STATUS.md per the maintenance obligation (FR-008)."
   - **Rationale**: FR-008 (`spec.md` L215) requires STATUS.md updates when status changes, but the taxonomy does not define what constitutes a status change. Without transition criteria, two reviewers could disagree on whether partial gap closure warrants relabeling. [`spec.md`, L215]
   - **Risk if ignored**: Phase 3 adds risk-of-gap and effort fields (T010, T011 in `tasks.md` L65-66). As implementation proceeds post-Phase 3, spec labels will need to be updated. Without transition criteria, the updates will be ad hoc and potentially inconsistent.

5. **Document compound-label conventions for multi-subsystem specs** (Priority: P2)
   - **Current state**: Spec 004 uses "Implementation-complete (core) / Not started (discovery)" (STATUS.md L46), which is a compound label not explained by the taxonomy's three-label system (L9-13).
   - **Proposed change**: Add a note to the Implementation Tier section: "Specs with independently-implementable subsystems may use compound labels (e.g., 'Implementation-complete (core) / Not started (discovery)') to distinguish subsystem status. Subsystem boundaries should be identified by FR ranges."
   - **Rationale**: The taxonomy must describe every label format used in the Status section. Compound labels are currently used but not defined, making them a convention-by-example rather than a taxonomy-defined format. [`STATUS.md`, L9-13, L46]
   - **Risk if ignored**: Phase 3 adds spec 005 (T012a, `tasks.md` L68), which may also have subsystem-level variance. Without documented compound-label conventions, the format will drift.

6. **Verify spec 002's "Spec-complete" label is justified** (Priority: P2)
   - **Current state**: Spec 002 is labeled "Spec-complete" (STATUS.md L36), meaning all acceptance criteria are met. The notes state "All 36 FRs represented in SKILL.md" and add that "Runtime correctness of stagnation detection depends on spec 001's parsing subsystem."
   - **Proposed change**: Verify that spec 002's acceptance scenarios (not just FRs) are fully satisfied. If the dependency on spec 001's parsing subsystem means some acceptance scenarios cannot be fully validated until spec 001's gaps are resolved, note this qualification. "Spec-complete" should mean "all acceptance criteria met," not "all FRs present in SKILL.md."
   - **Rationale**: The Phase 1 final summary (`gates/phase-1/summary/final.md`, L107-108) documents that T019 introduces behavioral expansion to stagnation detection and that STATUS.md will become stale after T019. If spec 002's acceptance depends on parsing behavior that T019 will change, the "spec-complete" label may be premature. [`gates/phase-1/summary/final.md`, L107-109]
   - **Risk if ignored**: If T019 (Phase 4) changes parsing behavior and this invalidates one of spec 002's acceptance criteria, the "spec-complete" label becomes false. The taxonomy's credibility depends on labels being accurate.

7. **Add a "Partially feature-complete" or "In progress" acceptance label** (Priority: P3)
   - **Current state**: The acceptance tier has two labels (plus the undocumented "Not started"). When Phase 3 adds spec 005 to STATUS.md, its acceptance status will be "in progress" — some acceptance criteria met, others not yet, and gaps not yet fully enumerated. Neither "feature-complete" nor "not started" accurately describes this.
   - **Proposed change**: Either (a) add "In progress" as an acceptance-tier label: "Some acceptance criteria are met, implementation is ongoing. Specific gap list may evolve." Or (b) document that "feature-complete" can apply to specs in active development once their gap list is stable.
   - **Rationale**: Spec 005 is the first spec to self-track in STATUS.md (per SC-003, `spec.md` L265; and T012a, `tasks.md` L68). It will need a label that is not "not started" (it has implementation) and not "feature-complete" (its gap list is not stable yet). [`spec.md`, L265, L279]
   - **Risk if ignored**: Phase 3 implementor invents a label or misapplies "feature-complete" to a spec that does not yet have all major capabilities present. Low impact but avoidable.

8. **Scope-check the "Interpreting the Two Tiers" paragraph** (Priority: P3)
   - **Current state**: The paragraph (STATUS.md L22-24) includes three sentences covering orthogonality, two illustrative examples, and a note about dependencies. The dependency note ("Dependencies are also orthogonal — a spec can be implementation-complete while depending on another spec's correctness for composed behavior") is useful but may be considered Phase 3 scope (dependency tracking is T009, `tasks.md` L64).
   - **Proposed change**: Either (a) retain as-is, since it is a single sentence that aids taxonomy interpretation, or (b) remove the dependency sentence and let Phase 3's cross-spec dependency section handle it. Recommend (a) — it is a natural part of explaining orthogonality and does not encroach on Phase 3's structural content.
   - **Rationale**: The Phase 2 scope is taxonomy + labels (`tasks.md` L34-47). The dependency sentence is borderline but does not add structural content (no dependency graph, no implementation order). It explains a taxonomy concept. [`tasks.md`, L34-47]
   - **Risk if ignored**: None. This is a scope-purity observation, not a functional concern. The scope-boundary agent may flag it; this recommendation preempts that discussion.

### Referenced Documentation

- `conversus/specs/STATUS.md` — sections/lines cited: L3-24 (taxonomy), L30-49 (per-spec status entries), L22-24 (interpreting two tiers), L31-33 (spec 001 entry), L36-38 (spec 002 entry), L40-43 (spec 003 entry), L46-49 (spec 004 entry)
- `conversus/specs/005-p2p3-backlog-hardening/spec.md` — sections/lines cited: L77-90 (US5), L87-89 (US5 AS1-AS3), L215-216 (FR-008, FR-009), L225-226 (FR-012, FR-013), L265 (SC-003), L275-279 (Assumptions)
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` — sections/lines cited: L34-47 (Phase 2), L64 (T009), L65-66 (T010, T011), L68 (T012a)
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-1/summary/final.md` — sections/lines cited: L107-109 (T019 behavioral expansion convergence), L262 (gate verdict)
- `conversus/specs/001-subject-arbitration/spec.md` — sections/lines cited: L158-160 (FR-025, FR-026), L173 (FR-023)
