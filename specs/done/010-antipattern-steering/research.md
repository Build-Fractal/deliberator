# Research: Agent Antipattern Steering

**Feature**: 010-antipattern-steering | **Date**: 2026-03-20

## R1: Catalog Format — Single File vs Directory of Files

**Decision**: Single markdown file (`antipatterns/catalog.md`) with summary index + sequential entries.

**Rationale**: At the target scale (50 entries), a single file remains well within agent context limits (~500 lines for 50 entries at ~10 lines each). A single file is simpler to maintain, simpler for agents to load, and avoids the overhead of directory traversal or file aggregation. The summary index at the top provides the "quick scan" capability without needing a separate index file.

**Alternatives considered**:
- **Directory of individual files** (`antipatterns/001-redundant-cache.md`, etc.): Adds file management overhead, requires an index file that must stay in sync, and makes the "read summary first" workflow harder — agents would need to read the index file, then selectively read individual files. Rejected for P1 complexity.
- **YAML catalog**: Structured and machine-parseable, but agents consume the catalog as reading context, not via programmatic parsing. YAML is less natural for agents to read and less natural for humans to author. Rejected per Constitution Principle VI justification.
- **Frontmatter-per-entry in markdown**: Each entry could use YAML frontmatter blocks within the single file. Adds parsing complexity for no retrieval benefit at P1 scale. Keyword tags work as plain-text headers.

## R2: Catalog Location in Project Tree

**Decision**: `antipatterns/catalog.md` at the conversus project root.

**Rationale**: Follows the existing flat layout convention — `presets/`, `templates/`, `specs/`, and now `antipatterns/`. The directory allows future expansion (e.g., `antipatterns/archive/` for deprecated entries) without restructuring. Placing it at project root ensures agents spawned for any conversus task can reference it with a stable, predictable path.

**Alternatives considered**:
- **`specs/antipatterns/catalog.md`**: Conflates specs (features being built) with operational artifacts (the catalog IS infrastructure). Rejected — specs are work products, the catalog is a permanent reference.
- **`.specify/memory/antipatterns.md`**: Would co-locate with the constitution, but `.specify/` is speckit infrastructure, not conversus-specific content. The catalog is a conversus project artifact, not a speckit memory.
- **Inline in `SKILL.md`**: Would bloat SKILL.md and make the catalog harder to maintain independently. SKILL.md should reference the catalog, not contain it.

## R3: Agent Integration Mechanism

**Decision**: Add a pre-task check instruction to SKILL.md that agents encounter during deliberation setup.

**Rationale**: SKILL.md is the single source of truth for agent behavior (Constitution Principle IV). Adding a brief instruction there ensures all agents — deliberation agents, review agents, arbiters — see the antipattern check as part of their standard workflow. The instruction directs agents to read the catalog summary index and match against current work before proposing new artifacts.

**Alternatives considered**:
- **Template-level injection**: Add antipattern check instructions to each phase template (review.md, revision.md, etc.). Would duplicate the instruction across 24+ template files and create a maintenance burden. Rejected — a single SKILL.md instruction is DRYer.
- **Constitution-only reference**: The constitution already mentions antipatterns but is not consumed by deliberation agents during task execution. Agents read SKILL.md, not the constitution. Rejected — insufficient integration point.
- **Preset-based injection**: Create an `antipattern-aware` preset that adds the check instruction. Would require every agent config to include the preset, which is opt-in rather than default-on. Rejected — the check should be universal, not opt-in.

## R4: Summary Index Design

**Decision**: Markdown table at the top of catalog.md with columns: Name, Summary, Keywords.

**Rationale**: A table is scannable by both agents and humans. Agents read the table first and only proceed to full entries for matches. The Keywords column enables P2 retrieval by making tags visible in the index. At 50 entries, the table is ~55 lines — well within a single-screen scan.

**Alternatives considered**:
- **Bulleted list**: Less structured, harder to scan at scale. Tables provide better visual alignment.
- **Separate index file**: Adds sync burden (index must be updated when entries change). Single-file approach keeps index and entries co-located.

## R5: Keyword Retrieval Mechanism (P2)

**Decision**: Plain-text grep against keyword tags in the catalog file. No semantic search, no database, no indexing infrastructure.

**Rationale**: The spec explicitly states "For P1, keyword retrieval is a simple text match (grep-equivalent)." At 50 entries, grep over a single file completes in milliseconds. Agent-side implementation: read the file, scan for keyword matches in the index table, read matched full entries. This is mechanically achievable with existing agent tools (Read + text matching).

**Alternatives considered**:
- **Structured YAML with jq queries**: Over-engineered for the scale. Agents don't have jq; they'd need bash calls for something achievable by reading text.
- **Separate keyword index file**: Adds sync burden. Keywords in the summary table serve double duty as both index and retrieval target.
- **Semantic/vector search**: Spec identifies this as a future enhancement beyond P2. Current scale doesn't warrant it.

## R6: Deprecation Mechanism (P2)

**Decision**: Deprecated entries are marked with a `**Status**: Deprecated` line and a deprecation note explaining why. Deprecated entries remain in the full catalog but are excluded from the summary index table.

**Rationale**: FR-009 requires deprecated entries to remain in the catalog (for historical reference) but be excluded from the summary index (so agents don't match against outdated patterns). Removing from the index table while preserving the full entry achieves both goals with zero tooling.

**Alternatives considered**:
- **Move to separate archive file**: Loses the "single file" simplicity and requires agents to know about two files. Rejected.
- **Strikethrough in index**: Visually marks deprecation but agents might still match on the text. Removing from the index is cleaner.

## R7: Seed Entry Source

**Decision**: Seed the catalog with the "redundant-cache" antipattern using content from `antipatterns/examples/redundant-cache/README.md`.

**Rationale**: SC-004 requires every entry to reference a real observed incident. The redundant-cache example is fully documented with the original STATUS.md artifact, the fix-it specs it spawned, and the deliberation transcripts. This is the motivating incident for the entire feature.

**Alternatives considered**: No alternatives — this is the only observed antipattern documented so far. The catalog structure is validated by whether this entry is complete and useful.