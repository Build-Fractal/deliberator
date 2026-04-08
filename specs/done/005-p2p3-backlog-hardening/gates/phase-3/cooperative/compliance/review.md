# Phase 3 Cooperative Review — Compliance

**Agent**: compliance
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening
**Target**: `conversus/specs/STATUS.md`

---

### Executive Summary

Phase 3 is tasked with completing STATUS.md as the single-document cross-spec reference. The six tasks (T008, T009, T010, T011, T012, T012a) collectively deliver the "Shared Subsystems" section, "Cross-Spec Dependencies" section, Risk-of-Gap and Effort fields for all five specs, a "SKILL.md Structure Plan" section, and spec 005's own entry. These additions directly service FR-008, FR-016, FR-017, FR-019, and SC-003 from the spec.

My audit finds that the current STATUS.md (L86-138) satisfies the structural requirements of all six Phase 3 tasks. Each section exists, contains the FR-specified content, and the maintenance obligation note is present at L138. The document is substantively compliant with the Phase 3 checkpoint: "STATUS.md is the complete cross-spec reference with status for all 5 specs, subsystems, dependencies, risk, effort, and structure plan." However, there are material compliance gaps in the detail level of several fields, most critically the Effort fields which omit the "new files, logic complexity, testing surface" breakdown that FR-017 explicitly requires.

My most important recommendation: the Effort fields for specs 001, 003, and 004 must be enriched to cover the four dimensions specified in FR-017 (new files, logic complexity, testing surface, relative effort), not just the relative effort label and a summary sentence.

### Alignment

- **Shared Subsystems — three entries with correct structure** (STATUS.md L86-104): The section contains exactly three entries (Dispute-Parsing Subsystem, Structural Markers, Template Conventions), each with stability status and consumer lists. This directly satisfies T008's requirement for "three entries" and FR-008's requirement for "shared subsystem status (component, stability, consumers)." The Dispute-Parsing Subsystem entry includes the stagnation-detection limitation note per T008's specification. [`spec.md`, L215; `tasks.md`, L63]

- **Cross-Spec Dependencies — graph and ordering** (STATUS.md L106-129): The dependency graph at L110-118 shows the required chain: 001 is foundational, 002 depends on 001, 003 depends on 001/002/004, 004 is self-contained, and 005 documents 001/002/004. The recommended implementation order at L122 shows "001 -> 004 -> 002 -> 003" with per-step rationale. This satisfies FR-008's "cross-spec dependency map and recommended implementation order" and T009's requirements. [`spec.md`, L215; `tasks.md`, L64]

- **Risk-of-Gap present for all five specs** (STATUS.md L34, L41, L48, L55, L63): Every spec entry includes a "Risk-of-Gap" field answering what happens without implementation. Spec 001: disputes unresolved. Spec 002: single-pass only. Spec 003: manual configuration. Spec 004: copy-paste agents. Spec 005: documentation gaps persist. This satisfies FR-016 and T010. [`spec.md`, L238; `tasks.md`, L65]

- **Effort present for all five specs** (STATUS.md L35, L42, L49, L56, L64): Every spec entry includes an "Effort" field with a relative-effort label (Small/None/Large/Small/Small). This partially satisfies FR-017 and T011. [`spec.md`, L242; `tasks.md`, L66]

- **SKILL.md Structure Plan covers specs 002, 003, 004** (STATUS.md L66-84): Entries for all three specs exist. Spec 002 is "Already integrated" with section list. Spec 003 is "Needs new sections" with specific change descriptions. Spec 004 is "Already integrated" with section list. This satisfies FR-019 and T012. [`spec.md`, L250; `tasks.md`, L67]

- **Spec 005 has its own entry** (STATUS.md L58-64): Spec 005 is present with implementation status ("Partially-complete"), acceptance status ("Feature-complete"), gaps, depends-on, notes, risk-of-gap, and effort. This satisfies SC-003's "any spec" requirement and T012a. [`spec.md`, L265; `tasks.md`, L68]

### Missed Opportunities

- **Effort fields lack FR-017's four-dimension breakdown**: FR-017 (spec.md L242) requires effort estimates "covering: new files, logic complexity, testing surface, and relative effort (small/medium/large)." The current Effort fields provide only the relative effort label and a summary description. For example, spec 003 (STATUS.md L49) says "Large — 5 new subcommands..." but does not separately address logic complexity or testing surface. Spec 001 (L35) says "Small — 2 FRs remain" without mentioning new files (none), logic complexity (low — template edits), or testing surface (minimal — behavioral verification only). FR-017 uses "covering" which indicates all four dimensions should be addressed. Impact: **high**. [`spec.md`, L242]

- **Structural Markers subsystem lacks Location field**: The Dispute-Parsing Subsystem entry (STATUS.md L88-93) has a "Location" field pointing to SKILL.md. The Template Conventions entry (L101-104) has no Location field but its location is implicit. The Structural Markers entry (L95-99) has no Location or Interface field, making it the only subsystem entry without either. FR-008 requires "shared subsystem status (component, stability, consumers)" — Location is not strictly required, but the inconsistency within the section undermines the "single-document reference" goal of SC-003. Impact: **medium**. [`spec.md`, L215]

- **No "Depends On" field for spec 001**: Specs 002 (L39), 003 (L46), 004 (implicit — no dependencies), and 005 (L61) have dependency information. Spec 001 (L30-35) has no "Depends On" field and no note indicating it is foundational with no upstream dependencies. The Cross-Spec Dependencies section (L111) shows "001 Subject Arbitration -> (none — foundational)" but the per-spec entry does not mirror this. The Note at L129 states "per-spec entries are authoritative" — but spec 001's per-spec entry is silent on dependencies, creating ambiguity about whether the dependency was assessed. Impact: **low**. [`STATUS.md`, L129]

- **Maintenance note lacks spec-005 FR identifier**: The maintenance obligation note (STATUS.md L138) says "(FR-008a)" but this identifier does not appear in spec.md's FR list. FR-008 (spec.md L215) contains the maintenance requirement as part of its text: "STATUS.md MUST be updated when any spec's implementation or acceptance status changes." The "(FR-008a)" sub-identifier is an informal convention not defined in the spec. This is not a compliance failure, but it introduces a reference that a reader cannot trace back to the authoritative FR list. Impact: **low**. [`spec.md`, L215]

- **Spec 003 acceptance tier uses "Not started" rather than "Not assessed"**: STATUS.md L45 shows `**Acceptance**: Not started` for spec 003. The Phase 2 deliberation (final.md, Convergence point 1, L122-126) unanimously agreed to add "Not assessed" as a third acceptance label and apply it to spec 003. The Acceptance Tier taxonomy (STATUS.md L15-20) does not include "Not assessed" as a defined label. This means spec 003 uses a label that is defined in the Implementation Tier (L13) but not in the Acceptance Tier — a cross-tier label reuse that the Phase 2 deliberation identified as an orthogonality violation. This is a Phase 2 residual, not a Phase 3 task failure, but it remains a compliance issue against FR-009 (spec.md L216: "Status labels MUST use the two-tier convention defined in FR-012/FR-013"). Impact: **high**. [`spec.md`, L216; `gates/phase-2/summary/final.md`, L122-126]

- **Transition criteria absent from taxonomy**: The Phase 2 deliberation's Convergence point 6 (final.md L152-156) established a bilateral agreement on dual-condition transition criteria. The Actionable Spec Changes P2-3 (final.md L202-203) recorded this as a binding commitment for T008: "T008 must add transition criteria to the taxonomy section." The current STATUS.md taxonomy section (L3-24) contains no transition criteria. This was intended as a Phase 3 delivery per the Phase 2 synthesis, making it a Phase 3 compliance gap. Impact: **medium**. [`gates/phase-2/summary/final.md`, L202-203]

- **Compound-label permission rule absent from Implementation Tier**: The Phase 2 synthesis recommended (Actionable Spec Changes P1-4, final.md L192) adding a compound-label permission rule to the Implementation Tier section. The current taxonomy (STATUS.md L7-13) has no such rule, yet spec 004 (L52) uses compound format: "Implementation-complete (core) / Not started (discovery)." The label format is in use without being formally defined. Impact: **medium**. [`gates/phase-2/summary/final.md`, L192]

### Off-Base Assumptions

- **FR-017's "covering" dimension list is treated as optional guidance**: The spec (L242) says effort estimates must cover "new files, logic complexity, testing surface, and relative effort (small/medium/large)." The tasks.md T011 description (L66) paraphrases this as a single summary line per spec. The STATUS.md implementation follows the T011 paraphrase rather than the FR-017 source. This is a task-decomposition fidelity issue: T011 simplified the FR and the implementation followed T011, not FR-017. The correct understanding is that FR-017 uses "covering" to require all four dimensions be addressed, even if briefly (e.g., "New files: none. Logic complexity: low. Testing surface: behavioral verification. Relative effort: Small.").

- **Phase 2 "binding commitments" are treated as advisory**: The Phase 2 synthesis (final.md L171) explicitly states regarding transition criteria: "The synthesis records this as a binding commitment, not an optional suggestion." The Phase 2 Actionable Spec Changes (final.md L192, L198-203) list five P1 changes and four P2 changes. Several of these (compound-label rule, transition criteria, "Not assessed" label) were not implemented in Phase 2 and are not addressed in Phase 3's task list. If Phase 2's synthesis is authoritative, these are outstanding obligations that Phase 3 inherited. If the synthesis is advisory, its framing as "binding" is misleading.

### Actionable Recommendations

1. **Enrich Effort fields to four dimensions** (Priority: P1)
   - **Current state**: STATUS.md L35, L42, L49, L56, L64 contain relative-effort labels with summary descriptions but omit the "new files, logic complexity, testing surface" breakdown.
   - **Proposed change**: For each spec, add the three missing dimensions. Example for spec 001 (L35): "**Effort**: Small — New files: none. Logic complexity: low (template-level instructions only). Testing surface: behavioral verification of template output. 2 FRs remain (FR-025 per-FR citation, FR-026 per-file attribution)."
   - **Rationale**: FR-017 (spec.md L242) uses "covering" to enumerate four required dimensions. SC-006(d) (spec.md L268) requires effort estimates to be present. Present but incomplete estimates only partially satisfy these requirements.
   - **Risk if ignored**: An implementor using STATUS.md for prioritization has relative effort labels but cannot assess the nature of the work (is it new files? is it complex logic? does it need tests?) — which is the stated purpose of FR-017.

2. **Add "Not assessed" to Acceptance Tier taxonomy** (Priority: P1)
   - **Current state**: STATUS.md L15-20 defines two acceptance labels (Feature-complete, Spec-complete). Spec 003 (L45) uses "Not started" which is an Implementation Tier label (L13), not an Acceptance Tier label.
   - **Proposed change**: Add to L20: `- **Not assessed**: No acceptance criteria have been evaluated.` Change spec 003 L45 from `**Acceptance**: Not started` to `**Acceptance**: Not assessed`.
   - **Rationale**: Phase 2 deliberation unanimously converged on this (final.md L122-126). FR-009 (spec.md L216) requires labels to use the defined convention. Using an undefined label violates FR-009.
   - **Risk if ignored**: The taxonomy section claims to be the authoritative label definition, but a label in active use ("Not started" on spec 003) is not defined there. This directly contradicts SC-005's "zero labeling disagreements" criterion.

3. **Add compound-label permission rule to Implementation Tier** (Priority: P1)
   - **Current state**: STATUS.md L7-13 defines three implementation labels with no compound-label convention. Spec 004 (L52) uses a compound format.
   - **Proposed change**: Add after L13: "Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label."
   - **Rationale**: Phase 2 synthesis P1-4 (final.md L192) recommended this as a P1 change. Spec 004's label format is currently in use without formal definition, which means the taxonomy is incomplete as a reference.
   - **Risk if ignored**: Future spec entries (and spec 005's own T012a labeling) have no guidance on whether compound labels are permitted, leading to ad-hoc formatting decisions.

4. **Add transition criteria to taxonomy section** (Priority: P2)
   - **Current state**: STATUS.md L3-24 defines labels and their interpretation but contains no criteria for when a spec transitions between labels.
   - **Proposed change**: Add after the "Interpreting the Two Tiers" paragraph (L24): "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied."
   - **Rationale**: Phase 2 synthesis P2-3 (final.md L202-203) recorded this as a "binding commitment" for T008. The dual-condition formulation was a bilateral convergence point (final.md L152-156).
   - **Risk if ignored**: The boundary between Feature-complete and Spec-complete remains implicit. A reviewer could argue a spec with resolved gaps but unverified scenarios is Spec-complete, or vice versa.

5. **Add "Depends On" line to spec 001 entry** (Priority: P2)
   - **Current state**: Spec 001 (STATUS.md L30-35) has no "Depends On" field. All other specs with dependencies have one. The cross-spec dependency graph (L111) shows 001 has no dependencies.
   - **Proposed change**: Add after L31: `**Depends On**: None (foundational)`
   - **Rationale**: FR-008 requires per-spec status with dependency information. The Note at L129 says "per-spec entries are authoritative." If per-spec entries are authoritative but spec 001's entry is silent on dependencies, a reader cannot determine whether the dependency was assessed or simply omitted.
   - **Risk if ignored**: Minor ambiguity — the cross-spec section provides coverage, but the authoritative source (per-spec entry) is incomplete.

6. **Add Location field to Structural Markers subsystem entry** (Priority: P3)
   - **Current state**: STATUS.md L95-99 has Stability and sub-entries but no Location or Interface field. The other two subsystem entries have Location (L89) or Interface (L92, L104) fields.
   - **Proposed change**: Add after L96: `**Location**: SKILL.md Step 3 (TEMPLATE_STATUS check), Phase 5 synthesis templates (DISPUTES markers)`
   - **Rationale**: SC-003 requires zero ambiguity about shared subsystems. A reader checking the Structural Markers subsystem cannot determine where the markers are defined without searching SKILL.md.
   - **Risk if ignored**: Inconsistency within the Shared Subsystems section. An implementor looking for where TEMPLATE_STATUS is checked must search SKILL.md rather than finding a pointer in STATUS.md.

7. **Normalize FR-008a reference in maintenance note** (Priority: P3)
   - **Current state**: STATUS.md L138 references "(FR-008a)" — a sub-identifier not in the spec's FR list.
   - **Proposed change**: Change to "(FR-008)" to match the authoritative identifier in spec.md L215. The maintenance obligation is part of FR-008's text, not a separate requirement.
   - **Rationale**: Traceability. A reader seeing "FR-008a" and searching spec.md will find no match, which undermines the trust relationship between STATUS.md and the spec.
   - **Risk if ignored**: Minor confusion for readers cross-referencing the maintenance note with the spec.

8. **Add gap documentation convention note** (Priority: P3)
   - **Current state**: STATUS.md gap fields use FR identifiers (e.g., "FR-023 (output validation...)") but no convention is documented specifying that FR identifiers are the primary reference format.
   - **Proposed change**: Add to the taxonomy section: "Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability."
   - **Rationale**: Phase 2 synthesis P3-1 (final.md L208) recommended this. Without it, Phase 4 contributors updating gap fields may use inconsistent formats (some FR-based, some scenario-based).
   - **Risk if ignored**: Minor inconsistency risk in future gap field updates.

9. **Verify spec 005 gap list completeness** (Priority: P3)
   - **Current state**: Spec 005 entry (STATUS.md L60) lists four gaps: FR-007, FR-011, FR-014, FR-015. But tasks.md shows 8 remaining FRs at Phase 3 entry (FR-007, FR-011a, FR-011b, FR-013 heading semantics via T013, FR-014, FR-015, and the Phase 4 tasks). The gap list appears to represent only the SKILL.md-targeted FRs, omitting any STATUS.md-targeted FRs that may still be incomplete.
   - **Proposed change**: Verify that the four listed gaps accurately represent all unimplemented FRs at the time of writing. If additional FRs were incomplete when T012a was written, add them. The T012a labeling guidance from Phase 2 (final.md L147) instructs: "Label spec 005 implementation status based on FRs completed at time of writing."
   - **Rationale**: Accuracy of the gap field is the mechanism by which a reviewer distinguishes Feature-complete from Spec-complete.
   - **Risk if ignored**: A reviewer relying on the gap field may underestimate remaining work for spec 005.

### Referenced Documentation

- `conversus/specs/005-p2p3-backlog-hardening/spec.md` — sections/lines cited: L215-216 (FR-008, FR-009), L238 (FR-016), L242 (FR-017), L250 (FR-019), L265 (SC-003), L268 (SC-006)
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` — sections/lines cited: L63 (T008), L64 (T009), L65 (T010), L66 (T011), L67 (T012), L68 (T012a)
- `conversus/specs/STATUS.md` — sections/lines cited: L7-13 (Implementation Tier), L15-20 (Acceptance Tier), L22-24 (Interpreting), L30-35 (spec 001), L37-42 (spec 002), L44-49 (spec 003), L51-56 (spec 004), L58-64 (spec 005), L86-104 (Shared Subsystems), L106-129 (Cross-Spec Dependencies), L134 (timestamp), L138 (maintenance note)
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-2/summary/final.md` — sections/lines cited: L122-126 (Convergence point 1: "Not assessed"), L152-156 (Convergence point 6: transition criteria), L192 (P1-4: compound-label rule), L198-203 (P2-1 through P2-3: T007 annotation, T012a guidance, transition criteria), L202-203 (binding commitment for T008), L208 (P3-1: gap convention note)
