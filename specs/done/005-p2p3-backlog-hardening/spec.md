# Feature Specification: P2/P3 Backlog Hardening

**Feature Branch**: `005-p2p3-backlog-hardening`
**Created**: 2026-03-20
**Status**: Draft
**Input**: User description: "P2/P3 backlog items from self-audit deliberation: draft template markers, post-Phase-6 output validation, cross-spec status tracking, shared dispute-parsing documentation, two-tier status convention, edge case documentation, overwrite semantics, risk/effort assessments, baseline documentation, and SKILL.md structural preparation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Draft Template Safety Gate (Priority: P1)

As a developer running a conversus, I want non-cooperative arbitration templates to be marked as draft and rejected at load time, so that untested game-dynamics templates cannot accidentally run in production.

**Why this priority**: Defense-in-depth for the cooperative-only v1 constraint (Spec 001 L212). Without this, a misconfigured `mode` combined with an `arbiter` field could silently load an unvalidated template.

**Independent Test**: Can be fully tested by adding the draft marker to three template files and adding a single check to SKILL.md Step 3. Delivers safety enforcement independently of all other items.

**Acceptance Scenarios**:

1. **Given** `templates/winner-take-all/arbitration.md` contains `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` as its first line, **When** the engine loads this template during Step 3, **Then** execution fails with: "Template templates/winner-take-all/arbitration.md is marked as draft and cannot be used in production runs."
2. **Given** `templates/red-blue/arbitration.md` contains the draft marker, **When** the engine loads this template, **Then** the same failure occurs with the correct path.
3. **Given** `templates/prisoners-dilemma/arbitration.md` contains the draft marker, **When** the engine loads this template, **Then** the same failure occurs with the correct path.
4. **Given** `templates/cooperative/arbitration.md` does NOT contain a draft marker, **When** the engine loads this template, **Then** loading succeeds normally.

---

### User Story 2 — Post-Phase-6 Output Validation (Priority: P1)

As a developer running a cooperative-mode conversus with arbitration, I want the engine to validate that the arbiter's output contains the required section headings, so that malformed output is flagged before I rely on it.

**Why this priority**: Implements Spec 001 FR-023. Without this, a malformed `resolution.md` (missing required sections) would be silently accepted, undermining the structured output guarantee.

**Independent Test**: Can be tested by running Phase 6 and checking that the engine emits warnings for missing headings while still writing the file. Delivers output quality assurance independently.

**Acceptance Scenarios**:

1. **Given** Phase 6 completes and writes `resolution.md`, **When** the engine validates the output, **Then** it checks for these required section headings: "Process Note", "Decision Framework", "Binding Decisions", "Summary of Changes Required".
2. **Given** `resolution.md` is missing one or more required headings, **When** validation runs, **Then** the engine emits a warning listing the missing headings (e.g., "Warning: resolution.md missing required sections: Decision Framework, Summary of Changes Required").
3. **Given** `resolution.md` is missing required headings, **When** validation runs, **Then** the file is still written to disk — the warning is informational, not blocking.
4. **Given** `resolution.md` contains all four required headings, **When** validation runs, **Then** no warning is emitted.

---

### User Story 3 — Cross-Spec Implementation Status Tracking (Priority: P1)

As an implementor working across conversus specs, I want a single status document that tracks which specs, shared subsystems, and cross-spec integrations are complete, so that I can determine what is safe to build on.

**Why this priority**: All four specs share subsystems (dispute parsing), template conventions (structural markers), and schema fields. Without a status tracker, implementors risk building on incomplete foundations or duplicating work.

**Independent Test**: Can be tested by creating `specs/STATUS.md` and verifying it contains status entries for all four specs plus shared subsystems. Delivers implementor orientation independently.

**Acceptance Scenarios**:

1. **Given** the conversus specs directory, **When** an implementor looks for status, **Then** `specs/STATUS.md` exists with per-spec status (spec number, name, status label, key gaps).
2. **Given** `specs/STATUS.md`, **When** an implementor checks shared subsystems, **Then** it lists shared components (dispute parsing, structural markers, template conventions) with their stability status.
3. **Given** `specs/STATUS.md`, **When** an implementor checks cross-spec dependencies, **Then** it shows which specs depend on which shared subsystems and the recommended implementation order (001 -> 004 -> 002 -> 003).

---

### User Story 4 — Shared Dispute-Parsing Specification (Priority: P2)

As a developer implementing either spec 001 (trigger evaluation) or spec 002 (stagnation detection), I want the dispute-parsing subsystem documented as a single shared component, so that both consumers implement the same parsing logic.

**Why this priority**: Dispute parsing is consumed by two independent specs. Without a single specification, divergent implementations could parse the same synthesis file differently — one detecting disputes where the other does not.

**Independent Test**: Can be tested by verifying the shared specification exists in SKILL.md (or a shared conventions document), defines input/output/parsing rules, and is referenced by both spec 001 and spec 002.

**Acceptance Scenarios**:

1. **Given** the dispute-parsing subsystem, **When** documented as a shared component, **Then** it specifies: input (synthesis file path), output (boolean for trigger, integer count for stagnation), parsing rules (structural markers first, heading fallback second).
2. **Given** the shared specification, **When** spec 001 references trigger evaluation, **Then** it delegates to the shared dispute-parsing interface rather than defining its own parsing rules.
3. **Given** the shared specification, **When** spec 002 references stagnation detection, **Then** it consumes the integer dispute count from the same parsing interface.
4. **Given** the shared specification, **When** a future consumer needs dispute data, **Then** the interface contract (input type, output type, marker format) is stable and documented.

---

### User Story 5 — Two-Tier Status Convention (Priority: P2)

As a project maintainer reviewing spec completion, I want a clear convention distinguishing "feature-complete" from "spec-complete", so that status labels are unambiguous and consistent.

**Why this priority**: Resolves a labeling disagreement from the self-audit cross-review. Without this, reviewers may classify the same spec differently depending on whether they assess at the feature level or acceptance-criteria level.

**Independent Test**: Can be tested by verifying the convention is documented and applied to spec 001 (feature-complete, not spec-complete). Delivers labeling clarity independently.

**Acceptance Scenarios**:

1. **Given** the status convention, **When** a spec has all major capabilities present but acceptance criteria gaps remain, **Then** it is labeled "feature-complete".
2. **Given** the status convention, **When** a spec has all acceptance criteria met, **Then** it is labeled "spec-complete".
3. **Given** spec 001, **When** the convention is applied, **Then** it is labeled "feature-complete" (all major capabilities present) with noted gaps: FR-025 (citation instructions), FR-026 (file attribution). (FR-023 is implemented in SKILL.md; template instructions pending.)

---

### User Story 6 — Phase 4 Missing Document Edge Case (Priority: P3)

As a developer running a conversus where an agent produces no disputes, I want the engine to handle missing or empty Phase 4 documents gracefully, so that Phase 6 proceeds with available documents.

**Why this priority**: Minor documentation polish (Spec 001 Edge Cases L97). The behavior is likely already correct, but explicit documentation prevents confusion.

**Independent Test**: Verified by checking SKILL.md Phase 6 notes document this edge case.

**Acceptance Scenarios**:

1. **Given** a Phase 4 dispute document is missing or empty for one agent, **When** Phase 6 runs, **Then** it proceeds with the available dispute documents from other agents.

**Verification**: SKILL.md Phase 6 section contains a note about missing/empty dispute documents.

---

### User Story 7 — Phase 6 Overwrite Semantics (Priority: P3)

As a developer re-running Phase 6, I want explicit documentation that re-running overwrites any existing `resolution.md`, so that the overwrite behavior is not ambiguous.

**Why this priority**: SKILL.md's general overwrite note (L359) likely covers this, but explicit Phase 6 documentation is cleaner (Spec 001 FR-027).

**Independent Test**: Verified by checking SKILL.md Phase 6 notes include overwrite semantics.

**Acceptance Scenarios**:

1. **Given** an existing `resolution.md`, **When** Phase 6 is re-run, **Then** the existing file is overwritten with the new output.

**Verification**: SKILL.md Phase 6 section contains an explicit overwrite semantics note.

---

### User Story 8 — Risk-of-Gap Assessment Per Spec (Priority: P3)

As a project maintainer prioritizing implementation work, I want each spec to answer "What happens if this spec is never implemented?", so that priority decisions consider the cost of delay.

**Why this priority**: Risk-of-gap directly informs priority beyond value alone. Not blocking any implementation.

**Independent Test**: Verified by checking each spec (or STATUS.md) includes a risk-of-gap statement.

**Acceptance Scenarios**:

1. **Given** each spec, **When** a maintainer checks risk, **Then** a brief statement describes what capability is lost or degraded without that spec.

**Verification**: STATUS.md contains a "Risk-of-Gap" field for each of the 5 specs (001-005).

---

### User Story 9 — Estimated Implementation Effort Per Spec (Priority: P3)

As a project maintainer prioritizing implementation work, I want order-of-magnitude effort estimates per spec, so that priority considers effort alongside value.

**Why this priority**: Priority = value / effort. Without effort estimates, ordering considers only value. Not blocking.

**Independent Test**: Verified by checking each spec (or STATUS.md) includes relative effort comparison.

**Acceptance Scenarios**:

1. **Given** each spec, **When** a maintainer checks effort, **Then** an estimate covers: new files, logic complexity, testing surface, and relative effort (e.g., small/medium/large).

**Verification**: STATUS.md contains an "Effort" field for each of the 5 specs (001-005).

---

### User Story 10 — Baseline Feature Documentation (Priority: P3)

As an implementor extending conversus, I want pre-spec organic features (context mechanism, iterations field, path-list formatting, multi-file target resolution) documented as the stable baseline, so that I know what is established versus what specs add.

**Why this priority**: Documentation completeness. These features work and are relied upon but lack formal spec backing.

**Independent Test**: Verified by checking documentation acknowledges the baseline features and their stability.

**Acceptance Scenarios**:

1. **Given** the baseline features, **When** documented, **Then** each is listed with: what it does, where it's specified (SKILL.md section), and that it is a stable interface.

**Verification**: SKILL.md contains a "Baseline Features" section listing: `iterations`, `prior:`, path-list formatting, multi-file target resolution.

---

### User Story 11 — SKILL.md Structure Preparation (Priority: P3)

As an implementor planning future spec work, I want a documented plan for how SKILL.md will accommodate specs 002 (rounds, stagnation), 003 (subcommand dispatch), and 004 (preset resolution), so that future changes can be made incrementally without structural rework.

**Why this priority**: Advance planning reduces error during implementation. Not blocking any current work.

**Independent Test**: Verified by checking a structure plan exists (in STATUS.md or a planning document) that maps future spec sections to SKILL.md locations.

**Acceptance Scenarios**:

1. **Given** the structure plan, **When** an implementor prepares to add spec 002 features, **Then** the plan identifies which SKILL.md sections will be modified and what new sections are needed.

**Verification**: STATUS.md contains a "SKILL.md Structure Plan" section with entries for specs 002, 003, and 004.

---

### Edge Cases

- What happens when a template file is empty but has the draft marker? The engine checks for the draft marker before any other template processing. An empty-after-marker template still triggers the draft rejection.
- What happens when `resolution.md` is completely empty after Phase 6? All four required headings are missing. The engine emits a warning listing all four and writes the empty file anyway.
- What happens when STATUS.md becomes outdated? It is a living document. Each spec implementation should update it. Staleness is a process risk, not a system failure.
- What happens when dispute-parsing markers are present but malformed (e.g., only BEGIN without END)? Fallback to heading-based parsing per existing spec 001 FR-011 behavior.

## Requirements *(mandatory)*

### Functional Requirements

#### Draft Template Markers (P2-1)

- **FR-001**: Templates `templates/winner-take-all/arbitration.md`, `templates/red-blue/arbitration.md`, and `templates/prisoners-dilemma/arbitration.md` MUST contain `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` as their first line.
- **FR-002**: SKILL.md Step 3 MUST check loaded templates for the draft marker. If present, execution MUST fail with: "Template {path} is marked as draft and cannot be used in production runs."
- **FR-003**: The draft marker check MUST occur before any variable substitution or other template processing.

#### Post-Phase-6 Output Validation (P2-2)

- **FR-004**: After Phase 6 writes `resolution.md`, the engine MUST validate that the file contains these section headings: "Process Note", "Decision Framework", "Binding Decisions", "Summary of Changes Required".
- **FR-005**: If any required heading is missing, the engine MUST emit a warning listing the missing headings.
- **FR-006**: Validation failure MUST NOT prevent the file from being written. The warning is informational only.
- **FR-007**: Heading validation MUST be case-insensitive and match as substring within heading lines (e.g., `## Process Note` and `### Process Note` both satisfy the "Process Note" requirement).

#### Cross-Spec Status Tracking (P2-3)

- **FR-008**: A `specs/STATUS.md` file MUST be created containing: per-spec status (number, name, status label, key gaps), shared subsystem status (component, stability, consumers), cross-spec dependency map, and recommended implementation order. STATUS.md MUST be updated when any spec's implementation or acceptance status changes.
- **FR-009**: Status labels MUST use the two-tier convention defined in FR-012/FR-013.

#### Shared Dispute-Parsing Specification (P2-4)

- **FR-010**: The dispute-parsing subsystem MUST be documented as a shared component (in SKILL.md or a dedicated shared conventions section) with: input specification (synthesis file path), output specification (boolean for trigger, integer count for stagnation), parsing rules (structural markers primary, heading-based fallback), and a stable-interface contract.
- **FR-011**: Spec 001 (trigger evaluation) and spec 002 (stagnation detection) MUST reference the shared dispute-parsing specification rather than defining independent parsing logic.

#### Two-Tier Status Convention (P2-5)

- **FR-012**: The project MUST establish and document a two-tier status convention: "feature-complete" (all major capabilities present, acceptance criteria gaps remain) and "spec-complete" (all acceptance criteria met).
- **FR-013**: Spec 001 MUST be classified as "feature-complete" with documented gaps: FR-023 (output validation — SKILL.md validation logic exists but template-level heading instructions are pending), FR-025 (per-FR citation instructions), FR-026 (per-file attribution instructions).

#### Phase 4 Edge Case Documentation (P3-1)

- **FR-014**: SKILL.md Phase 6 notes MUST state: "If a Phase 4 dispute document is missing or empty, Phase 6 proceeds with available documents."

#### Phase 6 Overwrite Semantics (P3-2)

- **FR-015**: SKILL.md Phase 6 notes MUST explicitly state: "Phase 6 arbitration follows the same overwrite semantics: re-running overwrites any existing resolution.md."

#### Risk-of-Gap Assessment (P3-3)

- **FR-016**: Each spec in `specs/STATUS.md` MUST include a brief risk-of-gap statement answering: "What happens if this spec is never implemented?"

#### Effort Estimates (P3-4)

- **FR-017**: Each spec in `specs/STATUS.md` MUST include an order-of-magnitude effort estimate covering: new files, logic complexity, testing surface, and relative effort (small/medium/large).

#### Baseline Documentation (P3-5)

- **FR-018**: Organic SKILL.md features (context mechanism, iterations field, path-list formatting rules, multi-file target resolution) MUST be documented as the stable baseline that specs extend, with references to their SKILL.md locations.

#### SKILL.md Structure Preparation (P3-6)

- **FR-019**: A structural plan MUST document how SKILL.md will accommodate future spec implementations (002: rounds/stagnation sections, 003: subcommand dispatch entry points, 004: preset resolution steps), identifying which existing sections change and what new sections are needed.

### Key Entities

- **Draft Marker**: An HTML comment (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`) placed as the first line of templates that are not ready for production use. Checked by the engine at template load time.
- **Status Document** (`specs/STATUS.md`): A living tracking document for cross-spec implementation progress, shared subsystem stability, and dependency mapping.
- **Dispute-Parsing Subsystem**: A shared component consumed by spec 001 (trigger evaluation) and spec 002 (stagnation detection). Takes a synthesis file path as input and produces a boolean (disputes exist) and an integer (dispute count).
- **Status Tier**: A classification label — either "feature-complete" (major capabilities present, AC gaps remain) or "spec-complete" (all acceptance criteria met).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All three non-cooperative arbitration templates contain the draft marker as their first line, and attempting to load any of them causes a clear failure message — zero silent draft-template activations.
- **SC-002**: After every Phase 6 execution, the engine reports whether `resolution.md` contains all four required section headings — zero silently malformed outputs.
- **SC-003**: An implementor can determine the status of any spec, shared subsystem, or cross-spec dependency by reading a single document (`specs/STATUS.md`) — zero ambiguity about what is safe to build on.
- **SC-004**: The dispute-parsing subsystem has a single specification consumed by both spec 001 and spec 002 — zero divergent parsing implementations.
- **SC-005**: Every spec has a consistent, unambiguous status label using the two-tier convention — zero labeling disagreements between reviewers.
- **SC-006**: All P3 documentation items are present in their designated locations — documentation coverage for all identified gaps. Checklist: (a) edge cases (FR-014), (b) overwrite semantics (FR-015), (c) risk assessments (FR-016), (d) effort estimates (FR-017), (e) baseline docs (FR-018), (f) structure plan (FR-019).

## Assumptions

- Spec 001 is the authoritative source for Phase 6 behavior. This spec adds hardening and documentation on top of spec 001's functional specification.
- The three non-cooperative arbitration templates already exist in the templates directory (they do — the exploration confirmed this).
- SKILL.md is the primary specification document and the natural location for shared subsystem documentation (dispute parsing, draft marker checking).
- `specs/STATUS.md` exists with basic per-spec status but lacks subsystem tracking, risk/effort assessments, and structure plan.
- The two-tier status convention applies to all four existing specs. Future specs also adopt it.
- P3 items are documentation-only and carry minor behavioral impact in a prompt-orchestrated system. They can be implemented in any order.
- FR-011 is partially complete: STATUS.md cross-reference exists but SKILL.md Round Termination Check still uses inline dispute-counting logic independent of the Dispute-Parsing Subsystem.
- Spec 005 must track itself in STATUS.md to satisfy SC-003.

## Constraints

- P2 items (Stories 1-5) should be implemented before P3 items (Stories 6-11), following the priority ordering from the self-audit.
- Draft marker checking (FR-002) adds a new behavioral rule to SKILL.md Step 3. It must be compatible with the existing template loading flow.
- Output validation (FR-004) is non-blocking by design. It MUST NOT prevent `resolution.md` from being written, even if validation fails completely.
- STATUS.md is a living document that must be maintained as specs are implemented. It is not a one-time artifact.
- The shared dispute-parsing specification must not break existing SKILL.md behavior — it documents and consolidates what is already specified across specs 001 and 002.
