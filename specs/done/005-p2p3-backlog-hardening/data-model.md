# Data Model: P2/P3 Backlog Hardening

**Branch**: `005-p2p3-backlog-hardening` | **Date**: 2026-03-20

This feature is documentation-focused. No new data entities, database schemas, or persistent state are introduced. All changes modify existing Markdown specification files.

## Document Entities

### STATUS.md (enriched)

Existing document at `specs/STATUS.md`. Enriched with:

| Field | Type | Description |
|-------|------|-------------|
| Spec Number | string | e.g., "001" |
| Spec Name | string | e.g., "Subject Arbitration" |
| Status (implementation) | enum | implementation-complete, partially-complete, not-started |
| Status (acceptance) | enum | feature-complete, spec-complete, not-started |
| Key Gaps | list | Outstanding FR numbers with brief descriptions |
| Dependencies | list | Spec numbers this spec depends on |
| Risk-of-Gap | string | What happens if this spec is never implemented |
| Effort Estimate | enum + description | small/medium/large with detail |

### Shared Subsystems (new section in STATUS.md)

| Field | Type | Description |
|-------|------|-------------|
| Subsystem Name | string | e.g., "Dispute-Parsing" |
| SKILL.md Location | string | Section heading reference (not line numbers — use stable anchors) |
| Stability | enum | stable, evolving, draft |
| Consumers | list | Spec numbers that depend on this subsystem |

### SKILL.md Structure Plan (new section in STATUS.md)

| Field | Type | Description |
|-------|------|-------------|
| Spec Number | string | e.g., "002" |
| Affected SKILL.md Sections | list | Section heading names |
| New Sections Required | list | Section names to add |
| Estimated Scope | string | Brief description of changes |

## Validation Rules

- Status labels must use one of the defined enum values
- Risk-of-gap must be a single sentence answering "What happens if never implemented?"
- Effort estimates must include relative size (S/M/L) plus at least one dimension (files, complexity, testing)

## Taxonomy Note

The implementation tier ("implementation-complete", "partially-complete", "not-started") and acceptance tier ("feature-complete", "spec-complete") measure different dimensions. The implementation tier tracks whether FRs are represented in SKILL.md. The acceptance tier tracks whether the spec's own acceptance criteria are met. A spec can be implementation-complete but only feature-complete (all FRs in SKILL.md but some acceptance criteria gaps remain).

## Rendered Example

```markdown
### 001 — Subject Arbitration
**Implementation**: Partially-complete | **Acceptance**: feature-complete
**Gaps**: FR-025 (per-FR citation instructions), FR-026 (per-file attribution instructions)
**Risk-of-Gap**: Disputes remain unresolved; manual post-processing needed
**Effort**: Small — 2 FRs remain, template-level instructions
```

## State Transitions

No state machines. STATUS.md is a living document updated when any spec's implementation or acceptance status changes.
