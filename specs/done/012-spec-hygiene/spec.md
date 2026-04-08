# Feature Specification: Spec Hygiene — Pruning and Deprecation

**Feature ID**: `012-spec-hygiene`
**Created**: 2026-03-20
**Status**: Draft
**Depends On**: `009-antipattern-steering` (captures lessons from pruned specs in the antipattern catalog), `005-p2p3-backlog-hardening` (STATUS.md as the source of truth for spec status)
**Input**: Establish a formal process for identifying, deprecating, and removing specs that duplicate existing infrastructure or were created as agent artifacts of the redundant-cache antipattern.

---

## 1. Feature Summary

Specs 007 (preset-discovery) and 008 (status-enrichment-hardening) exist because agents observed a gap — "we need to track detailed status information" — and filled it by creating a manually-maintained cache in STATUS.md with rich taxonomy, effort estimates, and cross-spec dependency tracking. This is useful information, but it duplicates what speckit's task checkboxes, git branch status, and spec frontmatter already track. The agents then spent deliberation cycles maintaining the cache (updating STATUS.md whenever a spec changed), which is the textbook redundant-cache antipattern: agents inventing tracking artifacts that duplicate existing infrastructure, then paying ongoing maintenance costs.

The specific issue with specs 007 and 008: they specified features (preset discovery commands, status enrichment) that were shaped by the need to maintain the cache rather than by user needs. Spec 008's STATUS.md taxonomy with two-tier implementation/acceptance tracking is sophisticated, but it exists to serve agent context needs, not user workflows. Users query spec status through speckit, not by reading STATUS.md.

This spec does three things:

1. **Deprecates** specs 007 and 008 with documented rationale, preserving them in an archive for reference.
2. **Establishes a formal deprecation/removal process** for future specs, so that pruning is a defined operation rather than an ad-hoc deletion.
3. **Simplifies STATUS.md** to contain only information not tracked elsewhere, eliminating the redundant-cache properties.

**What changes**: Specs 007 and 008 are moved to a `specs/deprecated/` directory. STATUS.md is simplified to cross-spec dependency and implementation-order information (which IS unique to STATUS.md and not tracked elsewhere). A deprecation process is documented.

**What does not change**: All other specs remain as-is. The conversus engine is unaffected. Implemented features from specs 007/008 that are independently valuable (if any) remain in SKILL.md.

---

## 2. User Stories

### US-1: Deprecate Specs 007 and 008

As a conversus maintainer, I want to formally deprecate specs 007 and 008 so that they stop consuming deliberation attention and their removal rationale is documented for future reference.

**Acceptance Criteria**:

1. **Given** specs 007 (preset-discovery) and 008 (status-enrichment-hardening), **When** the deprecation process runs, **Then** both specs are moved to `specs/deprecated/` with a `DEPRECATED.md` file explaining the rationale: "These specs were products of the redundant-cache antipattern — they specified features to maintain a tracking artifact (STATUS.md) that duplicated information tracked by speckit's task checkboxes and spec frontmatter."

2. **Given** the deprecated specs, **When** an agent encounters a reference to spec 007 or 008 (e.g., in STATUS.md or other specs' "Depends On"), **Then** the reference points to the deprecated location and includes a note: "Deprecated — see `009-antipattern-steering` for the antipattern this spec exemplified."

3. **Given** spec 004 (preset-agents) currently references spec 007 for discovery commands (FR-022-024 extracted to spec 007), **When** spec 007 is deprecated, **Then** spec 004's STATUS.md entry is updated to note: "Discovery commands (formerly spec 007) — deprecated, see spec 012 rationale."

4. **Given** the deprecation is complete, **When** the antipattern catalog (spec 009) exists, **Then** a `redundant-cache.md` antipattern entry is created referencing specs 007/008 as the canonical example.

### US-2: Formal Deprecation Process

As a conversus maintainer, I want a defined process for deprecating specs so that future pruning is systematic rather than ad-hoc.

**Acceptance Criteria**:

1. **Given** a spec is identified as a deprecation candidate, **When** the maintainer initiates deprecation, **Then** the process requires: (a) documented rationale (why the spec should be removed), (b) impact assessment (what depends on this spec, what breaks), (c) migration path (where does the useful content go), (d) antipattern extraction (what lesson should be captured in the antipattern catalog).

2. **Given** a spec with dependencies (other specs reference it), **When** deprecation proceeds, **Then** all references must be updated: "Depends On" fields in dependent specs, STATUS.md entries, and any cross-references in other specs' bodies.

3. **Given** a deprecated spec, **When** it is archived, **Then** the original directory is replaced with a symlink or redirect file pointing to `specs/deprecated/{spec-id}/`, so that existing file paths don't silently 404.

### US-3: STATUS.md Simplification

As a developer reading STATUS.md, I want it to contain only information not available elsewhere so that it is a useful cross-cutting view rather than a redundant cache.

**Acceptance Criteria**:

1. **Given** the current STATUS.md with two-tier taxonomy (implementation/acceptance), effort estimates, risk-of-gap, and SKILL.md structure plans, **When** simplification is applied, **Then** STATUS.md retains: (a) cross-spec dependency graph (unique to STATUS.md — not tracked per-spec), (b) recommended implementation order (unique synthesis), (c) shared subsystem documentation (cross-cutting, not per-spec), (d) one-line status per spec (pointing to the authoritative source for details).

2. **Given** the simplified STATUS.md, **When** detailed spec status is needed, **Then** the one-line entry points to the authoritative source: "See speckit task checkboxes for implementation status" or "See spec frontmatter for acceptance status."

3. **Given** the simplified STATUS.md, **Then** it MUST NOT contain: per-FR implementation tracking (tracked by speckit tasks), effort estimates (subjective, stale quickly), risk-of-gap narratives (belong in spec bodies), or SKILL.md structure plans (belong in implementation plans, not status tracking).

---

## 3. Functional Requirements

### Deprecation Process

- **FR-001**: The project MUST maintain a `specs/deprecated/` directory for archived specs.
- **FR-002**: Each deprecated spec directory MUST contain a `DEPRECATED.md` file with: deprecation date, rationale (1-2 paragraphs), impact assessment (what depended on it), migration path (where useful content moved), and antipattern reference (if applicable).
- **FR-003**: When a spec is deprecated, its original directory MUST be replaced with a `MOVED.md` file containing: the new location (`specs/deprecated/{spec-id}/`) and a one-line rationale. This prevents silent broken references.
- **FR-004**: All cross-references to a deprecated spec (STATUS.md, other specs' "Depends On" fields, SKILL.md comments) MUST be updated to note the deprecation.
- **FR-005**: The deprecation process MUST be documented in `specs/PROCESS.md` (or equivalent) as a repeatable procedure with a checklist.

### Specs 007/008 Specific Actions

- **FR-006**: Spec 007 (preset-discovery) MUST be moved to `specs/deprecated/007-preset-discovery/` with a `DEPRECATED.md` explaining: "Discovery commands for presets are a convenience feature, not a core engine capability. The preset directory structure and README are sufficient for discovery. This spec was extracted from spec 004 to justify maintaining a separate feature area; the extraction itself was shaped by the redundant-cache antipattern — creating work to maintain a tracking system."
- **FR-007**: Spec 008 (status-enrichment-hardening) MUST be moved to `specs/deprecated/008-status-enrichment-hardening/` with a `DEPRECATED.md` explaining: "This spec formalized a two-tier STATUS.md taxonomy with per-FR tracking, effort estimates, and risk-of-gap analysis. While individually useful, this information duplicates speckit's task tracking and encourages agents to maintain a secondary tracking artifact. The taxonomy itself is preserved in STATUS.md history (git) for reference."
- **FR-008**: Any features from specs 007/008 that are already implemented in SKILL.md and independently valuable (not dependent on the redundant cache pattern) MUST be identified and preserved. Features that exist solely to maintain the cache MUST be marked for removal.

### STATUS.md Simplification

- **FR-009**: STATUS.md MUST be restructured to contain only cross-cutting information not tracked elsewhere: dependency graph, implementation order, shared subsystem documentation, and one-line spec status summaries.
- **FR-010**: Per-spec entries in the simplified STATUS.md MUST follow this format:
  ```
  ### NNN — Spec Title
  **Status**: {one word: draft | in-progress | complete | deprecated}
  **Depends On**: `NNN-name` (reason)
  **Notes**: One sentence of cross-cutting context (if any).
  ```
- **FR-011**: The detailed implementation tracking (per-FR status, gap lists, effort estimates) MUST be removed from STATUS.md. If this information is needed, it belongs in speckit task descriptions or spec-local tracking.
- **FR-012**: The "SKILL.md Structure Plan" section MUST be removed from STATUS.md. Implementation planning belongs in the spec body or in a separate plan document, not in a cross-spec status tracker.

### Antipattern Extraction

- **FR-013**: When spec 009 (antipattern-steering) is implemented, a `redundant-cache.md` antipattern MUST be created with: tags `[tracking, duplication, status, cache, taxonomy]`, severity `high`, and an example section documenting the STATUS.md/specs-007-008 incident specifically.
- **FR-014**: The antipattern entry MUST describe the general pattern (not just the specific incident): "Agents observe a gap in their immediate context, create a tracking artifact to fill it, and never verify whether existing infrastructure already covers the need. The artifact then requires ongoing maintenance that consumes deliberation cycles."

---

## 4. Success Criteria

- **SC-001**: Specs 007 and 008 are in `specs/deprecated/` with complete `DEPRECATED.md` files documenting rationale, impact, and migration.
- **SC-002**: All references to specs 007 and 008 in STATUS.md, other specs, and SKILL.md are updated to note the deprecation.
- **SC-003**: STATUS.md is reduced to cross-cutting information only: dependency graph, implementation order, shared subsystems, one-line status summaries. No per-FR tracking, no effort estimates, no risk-of-gap narratives.
- **SC-004**: The `redundant-cache` antipattern entry exists in the catalog (when spec 009 is implemented) with the specs 007/008 incident as its canonical example.
- **SC-005**: `specs/PROCESS.md` documents the deprecation checklist as a repeatable procedure.
- **SC-006**: Original spec directories (007, 008) contain `MOVED.md` redirect files, preventing silent broken references.
- **SC-007**: No independently valuable implemented features are lost during deprecation — any useful SKILL.md additions from 007/008 are preserved with updated attribution.

---

## 5. Implementation Notes

### Why Deprecate Rather Than Delete

Git preserves history, so deletion is recoverable. But deprecation with explicit rationale serves a different purpose: it communicates to future agents and developers WHY the specs were removed. A `DEPRECATED.md` file with the redundant-cache rationale is a persistent warning. A deleted directory with no trace (except git log) teaches nothing.

This is the same principle behind spec 009's antipattern catalog: capturing lessons at the point where they'll be encountered (in the file system, in STATUS.md references) rather than burying them in commit history.

### Phased Execution

This spec has two phases:

**Phase A** (immediate, no dependencies): Deprecate specs 007/008, create DEPRECATED.md files, update cross-references, simplify STATUS.md. This can be done today with no engine changes.

**Phase B** (after spec 009): Create the `redundant-cache.md` antipattern entry referencing the deprecation. This requires the antipattern catalog directory structure from spec 009.

Phase A is independently valuable. The STATUS.md simplification alone reduces agent context waste — agents currently read the full STATUS.md and then spend time maintaining it.

### What Stays in STATUS.md

The dependency graph and implementation order are genuinely cross-cutting and not tracked elsewhere. No single spec's frontmatter captures the full dependency web. The shared subsystem documentation (Dispute-Parsing Subsystem, Structural Markers, Template Conventions) is cross-cutting infrastructure that no single spec owns. These are the legitimate contents of a cross-spec status document.

The test for any STATUS.md content: "Is this information derivable from the individual spec files and speckit task state?" If yes, it's a cache and should be removed. If no, it's unique cross-cutting information and should stay.

### The Meta-Irony

This spec is itself an example of the system working correctly. Specs 007/008 were created by agents. The deliberation process (including cross-review and synthesis) eventually identified them as antipatterns. This spec formalizes the cleanup. The full arc — creation, identification, deprecation, antipattern extraction — is the system's self-correction mechanism operating at spec-lifecycle timescale rather than within a single deliberation.
