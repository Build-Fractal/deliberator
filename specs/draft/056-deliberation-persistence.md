# Feature Specification: Deliberation Persistence & Content Browsing

**Feature ID**: `056-deliberation-persistence`
**Created**: 2026-04-12
**Status**: Draft (revised after spec 056 deliberation)
**Depends On**: `055-capability-registry`, `057-settings-architecture`
**Motivated by**: Desktop Extension gap (ephemeral output) + developer workflow needs

> **Revision 2026-04-12** — Rewritten based on deliberation results.
> Both agents unanimously concluded the original framing was backwards:
> these are **developer-first** tools that Desktop inherits via the
> registry's per-surface projection, not Desktop-first features with
> developer use bolted on. Storage is **workspace-scoped** (project
> directory), not global (`~/.conversus/`). The global directory is
> for settings and credentials only (see spec 057).

---

## 1. Problem

Conversus deliberations produce a rich multi-file record: each agent's review, cross-reviews between every pair, revised positions, extracted disputes, and a final synthesis. This adversarial record is the core value — it's the evidence chain that makes the synthesis trustworthy.

**Today, all of it is ephemeral.** `conversus_decide` creates a temp directory, runs the pipeline, parses the synthesis, and deletes the output. Users on every surface — CLI developers, Claude Code users, Cursor users, Desktop Extension users — lose the full record after every run.

CLI users can work around this with `--output /path/`. But `conversus decide` (the primary entry point) has no persistence by default, and no way to browse or reference past deliberations.

---

## 2. Design principles (from the deliberation)

1. **Developer-first.** Developers using CLI, Claude Code, and Cursor are the primary creators and consumers of deliberation content. Desktop Extension users get the same tools via the registry's per-surface projection — no separate "Desktop-friendly" system.

2. **Workspace-scoped.** Deliberation output belongs with the project, not in a user-global directory. A developer running `conversus decide "Postgres or MongoDB?"` inside `~/code/my-app/` finds the output at `~/code/my-app/.conversus/deliberations/`. This makes output git-trackable, shareable with colleagues, and contextual to the project.

3. **Enhance existing workflows.** The `--output` flag already works. Persistence means making it the default (write to `.conversus/deliberations/`), not inventing a parallel mechanism.

4. **File-level access first, semantic API later.** The `show` tool starts as raw file access (read any markdown from a past deliberation). A semantic layer (`show disputes`, `show agent X review`) is a follow-up after the file-level foundation proves itself.

---

## 3. Capabilities

### 3.1 Persist by default (P1)

All `conversus decide` and `conversus run` invocations persist their full output to the workspace:

```
<project>/.conversus/deliberations/<timestamp>-<slug>/
  question.md              # the original question (decide) or target doc reference
  conversus.yml            # the generated or provided config
  output/
    pragmatist/
      review.md
      cross-reviews/devils-advocate.md
    devils-advocate/
      review.md
      cross-reviews/pragmatist.md
    pragmatist/revision.md
    devils-advocate/revision.md
    pragmatist/disputes.md
    devils-advocate/disputes.md
    summary/final.md
```

- `<timestamp>`: ISO 8601 compact (`20260412T173000`)
- `<slug>`: sanitized first ~40 chars of the question
- Controlled by `persistence.enabled` in `.conversus/settings.yml` (default: `true`, see spec 057)
- Auto-cleanup via `persistence.retention_days` (default: 90 days)
- The `DecideResult` / `RunResult` response includes `output_path` pointing to the persisted directory
- CLI prints the path after the synthesis: `Output saved to: .conversus/deliberations/20260412T173000-postgres-vs-mongodb/`

### 3.2 List deliberations (P2)

New capability: `list_deliberations`

Scans `<project>/.conversus/deliberations/` and returns a summary of each:

```json
[
  {
    "timestamp": "2026-04-12T17:30:00",
    "question": "Should I build a timber framed home or...",
    "mode": "cooperative",
    "agents": ["pragmatist", "devils-advocate"],
    "path": ".conversus/deliberations/20260412T173000-timber-vs-conventional/",
    "has_synthesis": true
  }
]
```

**Surfaces**: CLI + MCP + Plugin + MCPB

**CLI**: `conversus list` — prints a table of past deliberations with timestamps, questions, modes. `--json` flag for piping to `jq`.

**MCP**: `conversus_list_deliberations` — returns the JSON array. Claude/Cursor can use it to reference past decisions in conversation.

### 3.3 Show deliberation content (P2)

New capability: `show_deliberation`

Reads a specific file from a past deliberation and returns it:

```
User: "Show me the devil's advocate review from my timber framing deliberation"
Claude: [calls conversus_show_deliberation]
→ Returns the full text of devils-advocate/review.md
```

**Surfaces**: CLI + MCP + Plugin + MCPB

**CLI**: `conversus show <deliberation-path> <file>` — prints the file content. Examples:
```bash
conversus show .conversus/deliberations/20260412T173000-timber/ summary/final.md
conversus show .conversus/deliberations/20260412T173000-timber/ pragmatist/review.md
conversus show .conversus/deliberations/20260412T173000-timber/ devils-advocate/disputes.md
```

**MCP**: `conversus_show_deliberation(deliberation_path, file_path)` — returns the file text as a string. Security: validates both paths are inside `.conversus/deliberations/` (no path traversal).

### 3.4 Semantic API (P3 — future phase)

Higher-level queries that don't require knowing file paths:

```
"What were the disputes from my last deliberation?"
"Show me where the pragmatist changed their mind"
"Compare the synthesis from my cooperative vs red-blue run on the same question"
```

These map to:
- `show_disputes(deliberation)` → reads `*/disputes.md`, extracts structured disputes
- `show_revisions(deliberation, agent)` → reads `*/revision.md`, extracts withdrawn/modified/surviving
- `compare_deliberations(path_a, path_b)` → diff two syntheses

**Deferred** — build after file-level access (3.3) proves the pattern. The file-level tool is the foundation; semantic tools are views over it.

---

## 4. Implementation plan

### Phase 1: Persistence (depends on spec 057 for `.conversus/` directory)

1. Update `run_decide_mcp` and `run_decide_cli` in `engine/handlers.py`:
   - After pipeline completion, copy the output tree to `<project>/.conversus/deliberations/<timestamp>-<slug>/`
   - Add `output_path` field to `DecideResult`
   - CLI prints the persistence path
2. Same for `run_mcp` and `run_cli` (the `conversus run` handlers)
3. Add `persistence.retention_days` cleanup: on each run, delete deliberation directories older than the retention limit
4. Add to `capabilities.py`, project, test

### Phase 2: List + Show

1. Add `list_deliberations_cli` + `list_deliberations_mcp` to `engine/handlers.py`
2. Add `show_deliberation_cli` + `show_deliberation_mcp` to `engine/handlers.py`
3. Register both as capabilities in `capabilities.py`
4. Project via `make build-surfaces`
5. Day 5-style validation: generate, exec, verify signatures, principle XI compliance

### Phase 3: Semantic API (separate spec)

Not in scope for this spec. Write a follow-up spec after Phase 2 is validated.

---

## 5. `conversus init` integration

`conversus init` (spec 057) creates the `.conversus/` directory. This spec adds:

```bash
conversus init
# → creates .conversus/settings.yml (with persistence.enabled: true)
# → creates .conversus/deliberations/ (empty, ready for output)
# → creates .conversus/runtimes/ (per-runtime permission configs)
```

For Desktop Extension users who don't have the CLI:
- The `.mcpb` bundle's MCP server creates `.conversus/deliberations/` on first deliberation run (lazy init)
- No explicit `init` step needed — persistence "just works"

---

## 6. Success criteria

- SC-001: `conversus decide` persists the full output tree to `<project>/.conversus/deliberations/` without the user requesting it
- SC-002: `DecideResult` and `RunResult` include a non-null `output_path` after a successful deliberation
- SC-003: `conversus list` prints a table of past deliberations from the project's `.conversus/deliberations/`
- SC-004: `conversus show <path> <file>` returns the full markdown text of any file within a past deliberation
- SC-005: Path traversal outside `.conversus/deliberations/` is rejected with a clear error
- SC-006: Deliberation directories older than `persistence.retention_days` are cleaned up automatically
- SC-007: `--json` flag on `list` produces `jq`-friendly output

---

## 7. Out of scope

- **Semantic API** (show disputes, compare deliberations) — Phase 3, separate spec after file-level access is validated
- **Full-text search** across deliberations — needs an index, separate concern
- **Cloud sync** — not needed for single-user workflows
- **Deliberation deletion via tool** — users can `rm -rf`; no in-tool deletion for v1
- **Settings cascade** — defined in spec 057, not here

## 8. Future consideration: in-memory deliberation representations

> **Note for future spec**: The current persistence model is file-system
> based — the engine writes markdown files to disk, and the persistence
> layer copies those files to `.conversus/deliberations/`. This works but
> creates a tight coupling between the pipeline and the filesystem.
>
> A future spec should explore **in-memory deliberation representations**
> where the pipeline produces structured objects (agent reviews as typed
> models, cross-reviews as relationship objects, disputes as first-class
> entities) that can be:
>
> - Serialized to disk as the current markdown files (backward compat)
> - Queried in memory without file I/O (for the semantic API in Phase 3)
> - Rendered to different formats (markdown, JSON, HTML) by surface-specific adapters
> - Streamed to MCP clients as structured progress events during execution
> - Diffed programmatically (compare two deliberation runs without parsing markdown)
>
> This would make the `show_deliberation` semantic API trivial —
> instead of parsing markdown files to extract disputes/revisions, the
> engine would produce typed objects that the show handler can filter
> and project directly. It would also enable real-time deliberation
> streaming to Desktop Extension users (show each phase as it completes
> rather than waiting for the full pipeline to finish).
>
> The key design question: should the in-memory representation be the
> pipeline's native output format (with files as a serialization), or
> should files remain primary with in-memory as a parsed projection?
> The former is cleaner but requires refactoring the engine; the latter
> is more incremental but creates a parse-at-read-time cost.

---

## 8. Sources

| Source | Use |
|---|---|
| `specs/055-capability-registry.md` | Capability framework for `list_deliberations` and `show_deliberation` |
| Spec 056 deliberation results | Unanimous: developer-first, workspace-scoped, file-level access first |
| `specs/057-settings-architecture.md` | `.conversus/` directory structure and settings cascade |
| `.claude/` directory convention | The pattern `.conversus/` follows |
