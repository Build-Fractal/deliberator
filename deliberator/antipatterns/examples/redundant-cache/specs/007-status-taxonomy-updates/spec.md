# Feature Specification: Status Taxonomy Updates

**Feature Branch**: `007-status-taxonomy-updates`
**Created**: 2026-03-20
**Status**: Draft
**Input**: Phase 2 gate deliberation summary (`deliberator/specs/005-p2p3-backlog-hardening/gates/phase-2/summary/final.md`)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Acceptance Tier Coverage (Priority: P1)

A process maintainer reviewing STATUS.md discovers that spec 003 uses the acceptance label "Not started," which is not defined in the taxonomy section. The taxonomy defines only two acceptance-tier labels ("Feature-complete" and "Spec-complete"), but a third state exists in practice: specs whose acceptance criteria have not yet been evaluated. The maintainer needs the taxonomy to define all labels actually in use so that the Phase 2 checkpoint claim — "STATUS.md taxonomy is authoritative" — is true.

**Why this priority**: Without a defined third acceptance label, the taxonomy is incomplete and the Phase 2 checkpoint fails. Every downstream phase depends on the taxonomy being authoritative.

**Independent Test**: Read STATUS.md's taxonomy section and verify every acceptance label used in any spec entry is defined there. Then read spec 003's entry and confirm its acceptance label matches a defined taxonomy value.

**Acceptance Scenarios**:

1. **Given** the acceptance tier taxonomy defines only "Feature-complete" and "Spec-complete," **When** a third label "Not assessed" is added with the definition "No acceptance criteria have been evaluated," **Then** the taxonomy covers all three observable acceptance states.
2. **Given** spec 003's acceptance field currently reads "Not started," **When** the label is updated to "Not assessed," **Then** spec 003 uses a label that is defined in the taxonomy.
3. **Given** a contributor reads the acceptance tier section, **When** they look for guidance on labeling a spec that has no implementation and no acceptance evaluation, **Then** the "Not assessed" label unambiguously applies without requiring inference about implementation state.

---

### User Story 2 - Spec 004 Acceptance Gap Transparency (Priority: P1)

An implementor planning work on spec 004 (Preset Agents) needs to see at a glance which acceptance criteria are unmet, just as spec 001 enumerates its gaps. Currently spec 004 is labeled "Feature-complete" but does not list its specific gaps, forcing the implementor to cross-reference the original spec to understand what remains. The implementor needs gap documentation consistent with spec 001's format.

**Why this priority**: The Phase 2 checkpoint requires the acceptance convention to be "applied to all 4 specs." Spec 001 has explicit gaps; spec 004 does not. This inconsistency violates FR-009 (uniform label application) and FR-013 (gap documentation).

**Independent Test**: Read spec 004's entry in STATUS.md and verify it contains a Gaps line identifying the specific FRs and acceptance scenarios that are unmet.

**Acceptance Scenarios**:

1. **Given** spec 004's STATUS.md entry has no Gaps line, **When** gap documentation is added listing FR-022, FR-023, and FR-024 as unstarted discovery features with affected acceptance scenarios, **Then** the entry matches the documentation standard set by spec 001.
2. **Given** an implementor reads spec 004's entry, **When** they look for what remains to be done for acceptance, **Then** they can identify the specific FRs and scenarios without consulting the original spec document.

---

### User Story 3 - Compound Label Convention (Priority: P1)

A contributor updating STATUS.md for a spec with independently-implementable subsystems (like spec 004's core engine vs. discovery CLI) needs to express per-subsystem status without losing information. The current taxonomy defines three implementation labels but has no rule for specs where different subsystems are at different implementation stages. Spec 004 already uses a compound format ("Implementation-complete (core) / Not started (discovery)"), but this format is not sanctioned by the taxonomy, creating ambiguity about whether it is valid.

**Why this priority**: Spec 004's current label uses an undocumented format. Without a formal rule, Phase 3 contributors labeling spec 005 (which may also have subsystem variance) will make ad-hoc formatting choices. The taxonomy must define all formats it permits.

**Independent Test**: Read the Implementation Tier section and verify it includes a rule for compound labels. Then confirm spec 004's existing label complies with that rule.

**Acceptance Scenarios**:

1. **Given** the Implementation Tier section defines three labels but no compound format, **When** a compound-label permission rule is added constraining components to existing tier values, **Then** the taxonomy formally sanctions the format spec 004 already uses.
2. **Given** spec 004 uses "Implementation-complete (core) / Not started (discovery)," **When** the compound-label rule is in place, **Then** spec 004's label is valid without modification.
3. **Given** a future contributor needs to label a spec with two independent subsystems at different stages, **When** they consult the taxonomy, **Then** they find an explicit rule for how to compose a compound label using defined tier values.

---

### User Story 4 - Phase 3 Labeling Readiness (Priority: P2)

A Phase 3 contributor implementing T012a (adding spec 005 to STATUS.md) needs clear guidance on how to label spec 005's implementation and acceptance status. Without guidance, the contributor must infer labeling conventions from existing entries, risking inconsistency. The contributor also needs to know that spec 005 was intentionally excluded from Phase 2's T007 scope.

**Why this priority**: Phase 3 immediately follows Phase 2. If labeling guidance is missing, T012a either stalls waiting for clarification or produces labels inconsistent with the convention.

**Independent Test**: Read the task descriptions for T007 and T012a and verify T007 documents the spec 005 exclusion and T012a contains explicit labeling instructions.

**Acceptance Scenarios**:

1. **Given** T007 applies acceptance labels to specs 001–004 but does not mention spec 005, **When** a parenthetical annotation is added to T007 noting that spec 005 is deferred to T012a, **Then** the exclusion is explicit rather than implicit.
2. **Given** T012a instructs the contributor to add a spec 005 entry, **When** labeling guidance is added explaining how to choose implementation and acceptance labels based on FR completion state, **Then** the contributor can label spec 005 without guesswork.

---

### User Story 5 - Transition Criteria Commitment (Priority: P2)

A Phase 3 implementor working on T008 (maintenance obligation) needs to know the agreed formulation for when a spec transitions from "Feature-complete" to "Spec-complete." The Phase 2 deliberation reached bilateral agreement on a dual-condition formulation, but this agreement is not recorded anywhere that Phase 3 can consume as an input.

**Why this priority**: Without the transition criteria recorded as a binding Phase 3 input, the bilateral agreement from Phase 2 may be lost or reinterpreted, undermining the deliberation's value.

**Independent Test**: Read the Phase 2 gate summary or a designated post-conditions document and verify it contains the dual-condition formulation as a binding commitment for T008.

**Acceptance Scenarios**:

1. **Given** the Phase 2 deliberation reached bilateral agreement on the dual-condition transition formulation, **When** this is recorded as a Phase 3 T008 input, **Then** the Phase 3 implementor has an unambiguous specification to work from.
2. **Given** the recorded formulation states both conditions — (a) all documented gaps resolved and (b) all acceptance scenarios verified — **When** an implementor reads it, **Then** they understand that both conditions must be met simultaneously to transition a spec to "Spec-complete."

---

### User Story 6 - Gap Documentation Convention (Priority: P3)

A Phase 3 contributor documenting gaps for multiple specs needs a clear convention for whether to reference FRs, acceptance scenarios, or both. The current entries use FR identifiers (consistent with FR-013's precedent), but this convention is not explicitly stated, risking inconsistency as more specs are documented.

**Why this priority**: Low cost to add; prevents ad-hoc formatting choices in Phase 3 and beyond.

**Independent Test**: Read the taxonomy section and verify it contains a one-sentence convention note about gap documentation format.

**Acceptance Scenarios**:

1. **Given** gap documentation in spec 001 uses FR identifiers, **When** a convention note is added stating FR identifiers are the primary reference with optional acceptance-scenario annotations, **Then** the format is codified rather than implicit.

---

### User Story 7 - Phase 4 Post-Conditions (Priority: P3)

A Phase 4 implementor needs to know that certain Phase 2 observations require action after T013 completes. Specifically, the FR-023 gap characterization in STATUS.md is accurate for Phase 2 but will be incomplete once T013 adds heading match semantics. Similarly, spec 002's "Spec-complete" label should be re-evaluated after T019 modifies dispute-parsing cross-references.

**Why this priority**: These are forward-facing risk notes. The information is accurate now but will become stale. Recording them prevents knowledge loss between phases.

**Independent Test**: Read the post-conditions record and verify it contains both the FR-023 update trigger and the spec 002 re-evaluation trigger.

**Acceptance Scenarios**:

1. **Given** STATUS.md L32's FR-023 characterization is accurate for Phase 2, **When** a post-condition is recorded stating it must be updated after T013, **Then** Phase 4 implementors know to revisit FR-023's gap text.
2. **Given** spec 002's "Spec-complete" label is valid for Phase 2's current-state assessment, **When** a post-condition is recorded noting T019's potential impact, **Then** Phase 4 implementors know to re-evaluate the label.

---

### Edge Cases

- What happens when a spec has more than two independently-implementable subsystems? The compound-label rule must work for any number of components, not just two.
- What happens when a spec's acceptance tier could be either "Not assessed" or "Feature-complete" based on partial evaluation? The label definitions must make the boundary unambiguous — "Not assessed" means zero evaluation; "Feature-complete" means evaluation has occurred with remaining gaps.
- What happens when the gap documentation convention note conflicts with a future spec's gap format? The convention note should be descriptive of the current precedent, not prescriptive in a way that prevents future evolution.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The acceptance tier taxonomy MUST include a third label "Not assessed" defined as "No acceptance criteria have been evaluated"
- **FR-002**: The "Not assessed" label definition MUST NOT reference implementation state, keeping the acceptance tier orthogonal to the implementation tier
- **FR-003**: Spec 003's acceptance label in STATUS.md MUST be updated from "Not started" to "Not assessed"
- **FR-004**: Spec 004's STATUS.md entry MUST include a Gaps line listing FR-022, FR-023, and FR-024 as unstarted discovery features with affected acceptance scenarios (US-3 through US-6)
- **FR-005**: The gap documentation format for spec 004 MUST be consistent with spec 001's existing format (FR identifiers as primary references)
- **FR-006**: The implementation tier taxonomy MUST include a compound-label permission rule stating that specs with independently-implementable subsystems may use compound labels composed of existing tier values
- **FR-007**: Each component of a compound label MUST use a defined implementation-tier label value
- **FR-008**: Spec 004's existing compound label format MUST comply with the compound-label rule without requiring modification
- **FR-009**: T007's task description MUST be annotated to document that spec 005 is excluded and deferred to T012a in Phase 3
- **FR-010**: T012a's task description MUST include explicit labeling guidance for spec 005 covering both implementation and acceptance tier label selection
- **FR-011**: The dual-condition transition criteria formulation MUST be recorded as a binding input for Phase 3's T008 implementation
- **FR-012**: The taxonomy section MUST include a one-sentence convention note specifying that gap documentation uses FR identifiers as primary references with optional acceptance-scenario annotations
- **FR-013**: A Phase 4 post-condition MUST be recorded stating that FR-023's gap characterization in STATUS.md should be updated after T013 implements heading match semantics
- **FR-014**: A Phase 4 post-condition MUST be recorded stating that spec 002's "Spec-complete" label should be re-evaluated after T019 modifies dispute-parsing cross-references
- **FR-015**: After all changes, every acceptance label used in any spec entry in STATUS.md MUST be defined in the taxonomy section
- **FR-016**: After all changes, every spec entry in STATUS.md MUST have both an implementation-tier and an acceptance-tier label

### Key Entities

- **Acceptance Tier Label**: A defined vocabulary value describing the state of a spec's acceptance criteria evaluation. Three values: "Spec-complete," "Feature-complete," "Not assessed."
- **Implementation Tier Label**: A defined vocabulary value describing the state of a spec's functional requirements in SKILL.md. Three values plus compound format: "Implementation-complete," "Partially-complete," "Not started," and structured compound labels for multi-subsystem specs.
- **Gap Documentation**: A structured annotation on a spec entry listing unmet FRs and affected acceptance scenarios, using FR identifiers as primary references.
- **Compound Label**: A structured composition of existing tier values used when a spec has independently-implementable subsystems at different implementation stages.
- **Post-Condition**: A recorded commitment that a specific action must be taken in a future phase when a triggering event occurs.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every acceptance label used in STATUS.md spec entries is defined in the taxonomy section — zero undefined labels remain
- **SC-002**: Every spec entry in STATUS.md contains both an implementation-tier and an acceptance-tier label — zero entries are missing either tier
- **SC-003**: Spec 004's gap documentation lists the same level of detail as spec 001's — an implementor can identify remaining work from either entry without consulting the original spec
- **SC-004**: A contributor labeling a new multi-subsystem spec can find an explicit compound-label rule in the taxonomy within 30 seconds of opening STATUS.md
- **SC-005**: Phase 3's T012a contains labeling guidance specific enough that two independent contributors would produce the same label choices for spec 005 given identical input
- **SC-006**: The dual-condition transition criteria are recorded in a location that Phase 3's T008 implementor will encounter during normal task execution
- **SC-007**: All post-conditions reference specific task IDs and triggering events, making them actionable without additional context

## Assumptions

- The Phase 2 gate deliberation's recommendations are authoritative for this feature. Disputed items are resolved per the synthesizer's recommended resolutions.
- STATUS.md's current structure and format conventions are preserved. Changes are additive (new labels, new rules, new annotations) rather than restructuring.
- The compound-label rule from the dispute resolution favoring taxonomy-reviewer and consistency-checker's position is adopted, as the synthesizer assessment found the evidence favored this approach and scope-boundary's flexibility conditions were met.
- Post-conditions are recorded in the Phase 2 gate summary document itself, as this is the natural location Phase 4 implementors will consult.
- Task description annotations (T007, T012a) are made directly in the existing tasks.md file.
