# Quickstart: Agent Antipattern Steering

**Feature**: 010-antipattern-steering | **Date**: 2026-03-20

## What This Feature Does

Provides a catalog of observed agent behavioral mistakes so that agents can check it before repeating the same errors. The catalog lives at `antipatterns/catalog.md` and agents are instructed via SKILL.md to consult it before proposing new artifacts.

## Implementation Checklist

### P1: Catalog + Agent Integration

1. **Create catalog file** at `antipatterns/catalog.md`
   - Add the summary index table
   - Seed with the `redundant-cache` entry (content from `antipatterns/examples/redundant-cache/README.md`)

2. **Add SKILL.md instruction** — insert the Antipattern Check block after config parsing, before phase execution. See [catalog-format contract](contracts/catalog-format.md) for exact wording.

3. **Update constitution** — verify the "Known Antipatterns" section in `.specify/memory/constitution.md` references the catalog location (`antipatterns/catalog.md`).

### P2: Keyword Retrieval + Maintenance

4. **Keyword retrieval** — agents use keyword matching against the Summary Index Keywords column to filter relevant entries. No tooling needed — agents read the file and match text.

5. **Deprecation workflow** — mark entries as Deprecated, remove from index, add deprecation note.

## How to Add a New Antipattern

1. Observe a recurring agent behavioral mistake with a concrete example
2. Append a new entry section to `antipatterns/catalog.md` following the entry format
3. Add a row to the Summary Index table
4. Do NOT modify any existing entries

## How to Verify It Works

- Run a conversus deliberation where an agent's natural approach would match a cataloged antipattern
- Verify the agent reads the catalog, identifies the match, and adjusts its approach
- Verify no false positives when the agent's work doesn't match any entries

## Key Files

| File | Purpose |
|------|---------|
| `antipatterns/catalog.md` | The antipattern catalog (new) |
| `SKILL.md` | Agent orchestration spec (edit: add check instruction) |
| `.specify/memory/constitution.md` | Project constitution (verify reference) |
| `antipatterns/examples/` | Seed data for first entry |