# Feature Specification: STATUS.md Enrichment Hardening

**Feature Branch**: `008-status-enrichment-hardening`
**Created**: 2026-03-20
**Status**: Draft
**Input**: Phase 3 gate deliberation summary (`conversus/specs/005-p2p3-backlog-hardening/gates/phase-3/cooperative/summary/final.md`)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Taxonomy Completeness (Priority: P1)

A process maintainer reviewing STATUS.md needs the taxonomy to be fully authoritative: every label in use must be defined, every label transition must have explicit criteria, and every format variation must be sanctioned by a rule. Currently three gaps exist: (1) spec 003 uses an acceptance label ("Not started") not defined in the Acceptance Tier, (2) the boundary between "Feature-complete" and "Spec-complete" has no explicit transition criteria, and (3) spec 004 uses a compound implementation label format the taxonomy does not formally permit.

**Why this priority**: These are Phase 2 binding commitments that were not executed during Phase 2. The Phase 3 checkpoint cannot pass without them. All three were unanimously agreed during deliberation.

**Independent Test**: Read the taxonomy section and verify: (a) three acceptance-tier labels are defined, (b) transition criteria are stated, (c) a compound-label rule exists. Then verify spec 003 uses a defined acceptance label and spec 004's compound label complies with the rule.

**Acceptance Scenarios**:

1. **Given** the Acceptance Tier defines only "Feature-complete" and "Spec-complete," **When** "Not assessed" is added with the definition "No acceptance criteria have been evaluated," **Then** every acceptance label used in STATUS.md is defined in the taxonomy.
2. **Given** spec 003's acceptance field reads "Not started," **When** it is updated to "Not assessed," **Then** spec 003 uses a defined taxonomy label.
3. **Given** no transition criteria exist, **When** the dual-condition formulation is added ("transitions when (a) all gaps resolved and (b) all acceptance scenarios verified"), **Then** the boundary between Feature-complete and Spec-complete is explicit.
4. **Given** no compound-label rule exists, **When** the permission rule is added constraining components to existing tier values, **Then** spec 004's existing label format is formally sanctioned.

---

### User Story 2 - Effort Field Dimensional Completeness (Priority: P1)

A project maintainer comparing specs for priority decisions needs each Effort field to address all four dimensions required by FR-017: new files, logic complexity, testing surface, and relative effort. The current Effort fields provide only a relative-effort tier and free-text description, omitting one or more dimensions and making cross-spec comparison inconsistent.

**Why this priority**: FR-017 uses an enumerative construction ("covering: X, Y, Z, and W") that mandates all four dimensions. Incomplete fields prevent systematic cross-spec comparison for prioritization.

**Independent Test**: Read each spec's Effort field and verify all four dimensions are explicitly addressed for every spec with remaining work. Verify a global scale definition exists for interpreting effort tiers.

**Acceptance Scenarios**:

1. **Given** spec 001's Effort field mentions only relative effort and FR count, **When** it is enriched with new-files, logic-complexity, and testing-surface dimensions, **Then** all four FR-017 dimensions are covered.
2. **Given** spec 003's Effort field lacks explicit dimensional breakdown, **When** all four dimensions are added in compact inline format, **Then** cross-spec comparison is possible on each dimension.
3. **Given** no global scale definition exists, **When** a scale definition is added (Small/Medium/Large with criteria), **Then** readers can interpret effort tiers consistently across specs.
4. **Given** spec 002 is marked "None -- complete," **When** no dimensional expansion is applied, **Then** complete specs are exempt from four-dimension expansion.

---

### User Story 3 - Dispute-Parsing Gap Visibility (Priority: P1)

An implementor reading the Dispute-Parsing Subsystem entry in the Shared Subsystems section encounters a note about unspecified heading-match semantics but has no visibility into whether or when this will be fixed. Adding a cross-reference to the scheduled Phase 4 task (T013) tells the reader that the gap has a planned resolution.

**Why this priority**: Without the cross-reference, an implementor might attempt to independently specify heading-match semantics, duplicating or conflicting with T013's upcoming work. Unanimously agreed.

**Independent Test**: Read the Dispute-Parsing Subsystem notes and verify a cross-reference to T013 (FR-007) is present.

**Acceptance Scenarios**:

1. **Given** the heading-match note states semantics are "not explicitly specified," **When** a T013 cross-reference is appended, **Then** readers know when and how the gap will be closed.

---

### User Story 4 - Risk-of-Gap Accuracy (Priority: P2)

A project maintainer using risk-of-gap statements for prioritization reads spec 005's statement and finds it describes deliverables already completed by Phase 3 ("STATUS.md lacks complete cross-spec reference information"). The statement needs to be rewritten to reflect the actual remaining risk: undocumented SKILL.md Phase 6 edge cases and unconsolidated dispute-parsing inline references.

**Why this priority**: A stale risk-of-gap statement degrades the comparative value of all risk assessments. Unanimously agreed on the need to rewrite.

**Independent Test**: Read spec 005's risk-of-gap statement and verify it describes consequences of remaining unimplemented FRs, not already-completed work.

**Acceptance Scenarios**:

1. **Given** spec 005's risk-of-gap references "STATUS.md lacks complete cross-spec reference information," **When** it is rewritten to reference remaining SKILL.md FRs, **Then** the statement accurately reflects current risk.

---

### User Story 5 - Dependency Field Uniformity (Priority: P2)

An implementor scanning STATUS.md entries to understand dependency relationships notices that specs 001 and 004 omit the "Depends On" field entirely, while specs 002, 003, and 005 include it. The omission creates ambiguity: was the dependency assessed and found to be none, or was it not assessed? Adding explicit "none" fields eliminates the ambiguity.

**Why this priority**: The Cross-Spec Dependencies section (L129) declares per-spec entries authoritative. Omitted fields undermine this authority. Bilateral agreement.

**Independent Test**: Read every spec entry and verify each has a "Depends On" field.

**Acceptance Scenarios**:

1. **Given** spec 001 has no "Depends On" field, **When** `**Depends On**: None (foundational)` is added, **Then** the dependency assessment is explicit.
2. **Given** spec 004 has no "Depends On" field, **When** `**Depends On**: None (self-contained engine)` is added, **Then** readers know the omission was intentional.

---

### User Story 6 - SKILL.md Structure Plan Completeness (Priority: P3)

A contributor preparing to implement spec 005's SKILL.md changes consults the Structure Plan but finds no entry for spec 005. The plan covers specs 002, 003, and 004 but omits 005, creating a gap between the plan's coverage and the full spec set.

**Why this priority**: Low cost to add; closes a gap between T012's implementation (three specs) and FR-019's intent (all future spec implementations).

**Independent Test**: Read the SKILL.md Structure Plan section and verify it contains entries for all specs that require SKILL.md changes.

**Acceptance Scenarios**:

1. **Given** the Structure Plan covers specs 002, 003, 004, **When** a spec 005 entry is added listing FR-007, FR-011, FR-014, and FR-015 as documentation edits, **Then** the plan covers all specs with pending SKILL.md work.

---

### User Story 7 - Maintenance Note Completeness (Priority: P3)

A process maintainer relies on the maintenance note at the bottom of STATUS.md to know when the document must be updated. The current note covers only implementation/acceptance status changes but not the Phase 3 living-content sections (Shared Subsystems, SKILL.md Structure Plan). If a subsystem's stability changes or a new spec implementation invalidates the Structure Plan, the note does not trigger an update obligation.

**Why this priority**: Low cost. Without broadening, Phase 3 sections could silently go stale. Bilateral agreement.

**Independent Test**: Read the maintenance note and verify it covers subsystem stability/consumer changes and Structure Plan updates in addition to status changes.

**Acceptance Scenarios**:

1. **Given** the maintenance note only covers implementation/acceptance changes, **When** it is broadened to include subsystem and Structure Plan triggers, **Then** all living-content sections are covered by the update obligation.
2. **Given** the maintenance note references "(FR-008a)," **When** the note is updated, **Then** the FR-008a identifier is retained (not normalized to FR-008).

---

### Edge Cases

- What happens when a spec has no remaining work but other specs' Effort fields reference it comparatively? The global scale definition provides the anchor; per-spec fields stand alone.
- What happens when the compound-label rule is applied to a spec with three or more independent subsystems? The rule permits "existing tier values" as components with no limit on count — it scales naturally.
- What happens when the T013 cross-reference in the Dispute-Parsing note becomes stale after T013 is implemented? The cross-reference should be updated or removed as part of T013's implementation, per the maintenance note obligation.
- What happens when a "Depends On: None" spec later acquires a dependency? The maintenance note obligation applies — the field must be updated when dependency state changes.

## Requirements *(mandatory)*

### Functional Requirements

#### Taxonomy Completeness (P1)

- **FR-001**: The Acceptance Tier taxonomy MUST include "Not assessed" defined as "No acceptance criteria have been evaluated"
- **FR-002**: Spec 003's acceptance label MUST be changed from "Not started" to "Not assessed"
- **FR-003**: Transition criteria MUST be added to the taxonomy section stating: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied"
- **FR-004**: The Implementation Tier taxonomy MUST include a compound-label permission rule constraining components to existing tier values
- **FR-005**: The compound-label rule MUST be implemented after FR-001/FR-002 and FR-003 within the P1 block (ordered by urgency: undefined labels first, undefined transitions second, undefined formats third)

#### Effort Field Enrichment (P1)

- **FR-006**: Every spec with remaining work (001, 003, 004, 005) MUST have its Effort field expanded to address all four FR-017 dimensions: new files, logic complexity, testing surface, and relative effort
- **FR-007**: Spec 002's Effort field ("None -- complete") MAY remain as-is without four-dimension expansion
- **FR-008**: A global scale definition MUST be added to the taxonomy or enrichment section defining Small, Medium, and Large effort tiers with criteria
- **FR-009**: The compact inline format MUST be used for per-spec dimensional coverage to preserve scanability

#### Dispute-Parsing Cross-Reference (P1)

- **FR-010**: The Dispute-Parsing Subsystem's heading-match note MUST include a cross-reference to T013 (FR-007) as the scheduled fix

#### Risk-of-Gap Accuracy (P2)

- **FR-011**: Spec 005's risk-of-gap statement MUST be rewritten to describe consequences of remaining unimplemented FRs (FR-007, FR-011, FR-014, FR-015), not already-completed Phase 3 work

#### Dependency Field Uniformity (P2)

- **FR-012**: Spec 001 MUST include `**Depends On**: None (foundational)`
- **FR-013**: Spec 004 MUST include `**Depends On**: None (self-contained engine)`

#### Structure Plan Completeness (P3)

- **FR-014**: The SKILL.md Structure Plan MUST include a spec 005 entry listing FR-007, FR-011, FR-014, and FR-015 as documentation edits to existing sections

#### Maintenance Note Scope (P3)

- **FR-015**: The maintenance note MUST be broadened to cover shared subsystem stability/consumer changes and SKILL.md Structure Plan updates
- **FR-016**: The maintenance note MUST retain the "(FR-008a)" identifier — normalization to "(FR-008)" is prohibited per deliberation withdrawal

#### Additional Improvements (P3)

- **FR-017**: A gap documentation convention note MUST be added to the taxonomy section: "Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability"
- **FR-018**: The Structural Markers subsystem entry MUST include a Location field identifying where markers are checked and used
- **FR-019**: Spec 003's dependency on spec 004 MUST be expanded to note that discovery features (FR-022-024) must be implemented before spec 003 Phase A
- **FR-020**: Spec 005's gap list MUST be verified complete for SKILL.md-targeted FRs, with a parenthetical clarifying that STATUS.md-targeted FRs are tracked by the maintenance obligation
- **FR-021**: The SKILL.md Structure Plan entry for spec 003 MUST specify existing sections modified (Step 1, Step 4, Step 5) in addition to new sections needed

### Key Entities

- **Transition Criteria**: A dual-condition rule defining when a spec moves from "Feature-complete" to "Spec-complete." Both conditions must be met simultaneously.
- **Effort Dimension**: One of four attributes required by FR-017: new files, logic complexity, testing surface, and relative effort. Each spec's Effort field must address all four.
- **Scale Definition**: A global mapping of effort tiers (Small/Medium/Large) to criteria, enabling consistent interpretation across spec entries.
- **Phase 2 Binding Commitment**: An obligation from a prior phase gate synthesis that must be executed in the current phase. Carries forward at its original priority level.
- **Post-Condition**: A recorded obligation for a future phase, stored in gate summaries rather than STATUS.md per-spec entries. STATUS.md entries may reference current deficiencies with scheduled fixes but should not contain temporal predicates about future label re-evaluations.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every acceptance label used in STATUS.md spec entries is defined in the taxonomy — zero undefined labels remain
- **SC-002**: The taxonomy section contains explicit transition criteria — a reader can determine exactly when a spec transitions between acceptance labels without inference
- **SC-003**: Every spec with remaining work has an Effort field covering all four FR-017 dimensions — zero partially-addressed dimensions across specs 001, 003, 004, 005
- **SC-004**: Every spec entry in STATUS.md has a "Depends On" field — zero entries with ambiguous dependency status
- **SC-005**: Spec 005's risk-of-gap statement references only remaining unimplemented FRs — zero references to completed Phase 3 work
- **SC-006**: The Dispute-Parsing heading-match note includes a cross-reference to its scheduled fix — an implementor can find the resolution plan within 10 seconds
- **SC-007**: The maintenance note covers all living-content sections — zero Phase 3 sections are excluded from the update obligation

## Assumptions

- The Phase 3 gate deliberation's recommendations are authoritative. Disputed items are resolved per the synthesizer's recommended resolutions.
- STATUS.md's current structure from Phase 3 tasks (T008-T012a) is preserved. Changes are targeted edits to existing entries and sections, not restructuring.
- The "Phase 2 remediation executed during Phase 3" framing is adopted: taxonomy changes (Not assessed, transition criteria, compound-label rule) are Phase 2 obligations whose execution occurs now because Phase 3 cannot pass without them.
- Effort field enrichment uses the compact inline format proposed by the compliance agent, as it has majority support and addresses the integration agent's scanability concern.
- The spec 002 Phase 4 re-evaluation note is recorded in the gate summary (this synthesis document) rather than STATUS.md, per the synthesizer's recommended resolution and the principle that STATUS.md entries describe current deficiencies, not future events.
- The FR-008a identifier is retained in the maintenance note per the compliance agent's evidence-based withdrawal of the normalization proposal.
