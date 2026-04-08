# Data Model: Agent Antipattern Steering

**Feature**: 010-antipattern-steering | **Date**: 2026-03-20

## Entities

### 1. Antipattern Catalog

The top-level container. A single markdown file (`antipatterns/catalog.md`) containing the summary index and all antipattern entries.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | heading | yes | `# Antipattern Catalog` |
| summary_index | table | yes | Scannable table of all active (non-deprecated) entries |
| entries | section[] | yes | Ordered list of Antipattern Entry sections |

**Validation rules**:
- Summary index must list every active entry (FR-003)
- Summary index must NOT list deprecated entries (FR-009)
- Entries are ordered chronologically by observation date (append-only, FR-010)

### 2. Summary Index

A markdown table at the top of the catalog providing quick scanning capability.

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| Name | string | yes | Antipattern identifier (kebab-case, e.g., `redundant-cache`) |
| Summary | string | yes | One-line description (<100 chars) |
| Keywords | string | yes | Comma-separated keyword tags for retrieval |

**Validation rules**:
- Every active Antipattern Entry must have a corresponding row (bidirectional sync)
- Name must be unique across all entries (active and deprecated)
- Summary must be a single line, no markdown formatting

### 3. Antipattern Entry

A self-contained section describing one observed agent behavioral mistake.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | heading (H2) | yes | Entry identifier matching Summary Index name |
| status | string | no | `Active` (default if omitted) or `Deprecated` |
| observed | date | yes | When the antipattern was first observed (YYYY-MM-DD) |
| summary | string | yes | One-line description, same as Summary Index |
| symptoms | list | yes | Observable indicators an agent can match against current work |
| root_cause | paragraph | yes | Why agents exhibit this behavior |
| example | paragraph + refs | yes | Specific observed incident with file/spec references (SC-004) |
| correction | paragraph | yes | What to do instead |
| scope | paragraph | yes | When this antipattern does NOT apply (boundary conditions) |
| keywords | list | yes | Terms for retrieval: topic tags like `tracking`, `cache`, `artifact-creation` |
| deprecation_note | paragraph | no | Only present when status=Deprecated. Explains why guidance changed |

**Validation rules**:
- `example` must reference a real observed incident, not a hypothetical (SC-004)
- `symptoms` must contain at least 2 items (enough for pattern matching)
- `scope` must contain at least 1 exclusion (prevents over-application)
- `keywords` must contain at least 2 tags
- Adding a new entry must NOT require modifying any existing entry (FR-010)
- Entry is self-contained — reading it provides full context (FR-004)

### 4. Keyword Tag

A retrieval term associated with an antipattern entry.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| value | string | yes | Lowercase, hyphenated tag (e.g., `deliberation-drift`) |

**Validation rules**:
- Tags are lowercase with hyphens for multi-word terms
- Tags appear in both the entry's Keywords field and the Summary Index Keywords column
- No controlled vocabulary — tags are free-form but should be consistent across entries

## Relationships

```
Catalog 1──* Antipattern Entry
Catalog 1──1 Summary Index
Summary Index 1──* Index Row
Index Row 1──1 Antipattern Entry (by name)
Antipattern Entry *──* Keyword Tag
```

## State Transitions

### Antipattern Entry Lifecycle

```
[New Observation] → Active → Deprecated
                              ↓
                        (remains in file,
                         removed from index)
```

- **Active → Deprecated**: When the antipattern guidance is determined to be wrong or no longer applicable. Requires a `deprecation_note` explaining why. Entry remains in the catalog file but is removed from the Summary Index table.
- No deletion state — entries are never removed from the catalog file (historical record).
- No "draft" state — entries are added when fully documented with a real example. Incomplete observations stay out of the catalog until they have all required fields.