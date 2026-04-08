# Contract: Antipattern Catalog Format

**Feature**: 010-antipattern-steering | **Date**: 2026-03-20

## Purpose

Defines the exact structure of `antipatterns/catalog.md` — the file agents and humans read. This contract ensures entries are consistent, self-contained, and machine-scannable.

## Catalog File Structure

```markdown
# Antipattern Catalog

> Agents: Read the summary index below. If your current work matches any
> entry's symptoms, read the full entry and adjust your approach.

## Summary Index

| Name | Summary | Keywords |
|------|---------|----------|
| redundant-cache | Do not create tracking documents that duplicate computable state | tracking, cache, artifact-creation, status |
| ... | ... | ... |

---

## redundant-cache

**Status**: Active
**Observed**: 2026-03-20
**Summary**: Do not create tracking documents that duplicate computable state

### Symptoms

- [bullet list of observable indicators]

### Root Cause

[paragraph explaining why agents exhibit this behavior]

### Example

[paragraph referencing specific observed incident with file/spec paths]

### Correction

[paragraph explaining what to do instead]

### When This Does NOT Apply

[paragraph bounding the antipattern's scope]

### Keywords

`tracking`, `cache`, `artifact-creation`, `status`

---

## [next-entry-name]
...
```

## Field Contracts

### Summary Index Row

- **Name**: kebab-case identifier, unique across all entries (active + deprecated), matches H2 heading in entry
- **Summary**: Single line, <100 characters, no markdown formatting
- **Keywords**: Comma-separated, lowercase, hyphenated tags

### Entry Section

- Begins with H2 heading matching the Name from Summary Index
- Fields appear in fixed order: Status, Observed, Summary, Symptoms, Root Cause, Example, Correction, When This Does NOT Apply, Keywords
- **Status** field: `Active` or `Deprecated`. Omit for Active (default)
- **Observed** field: `YYYY-MM-DD` format
- **Symptoms**: Bulleted list, minimum 2 items
- **Example**: Must reference real files/specs (not hypothetical)
- **Correction**: Actionable — tells the agent what to do instead
- **When This Does NOT Apply**: Minimum 1 exclusion
- **Keywords**: Backtick-formatted, comma-separated, matching Summary Index

### Deprecated Entry

- **Status** line reads `**Status**: Deprecated`
- A `### Deprecation Note` section is appended after Keywords
- Entry is removed from the Summary Index table
- Entry remains in the file in its original position

## SKILL.md Integration Contract

The following instruction block is added to SKILL.md. Location: before agent phase execution, after config parsing. Exact wording:

```markdown
### Antipattern Check

Before proposing new artifacts, tracking documents, or process changes, agents
MUST check the antipattern catalog at `antipatterns/catalog.md`:

1. Read the Summary Index table
2. If any entry's keywords or summary matches your current work, read the full entry
3. If your proposed approach matches an entry's Symptoms, follow the Correction instead
4. If no entries match, proceed normally — do not raise false positives
```

## Versioning

- New entries: append to end of file, add row to Summary Index table. No existing entries modified (FR-010).
- Deprecation: remove from Summary Index, add Status + Deprecation Note to entry.
- Format changes to this contract require updating all existing entries for consistency.