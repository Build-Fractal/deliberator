# Feature Specification: Deliberation Persistence & Desktop Content Viewing

**Feature ID**: `056-deliberation-persistence`
**Created**: 2026-04-12
**Status**: Draft
**Depends On**: `055-capability-registry` (capability framework), existing Desktop Extension (`.mcpb`)
**Motivated by**: spec 055 deliberation feedback (P1: "the registry creates genuine single points of failure") + user feedback on Desktop Extension experience

---

## 1. Problem

Conversus deliberations produce rich, multi-file output: each agent's review, cross-reviews between every pair, revised positions, extracted disputes, and a final synthesis. This pipeline record is the core value — it's the evidence chain that makes the synthesis trustworthy.

**Today, Desktop Extension users lose all of it.** The `conversus_decide` tool:

1. Creates a temp directory
2. Runs the full 5-phase pipeline, writing ~10-20 files
3. Parses the synthesis into a structured `DecideResult`
4. Returns the result to Claude Desktop
5. **Deletes the temp directory** in the `finally` block

The user sees the synthesis in the chat. But the agent reviews, cross-reviews, revisions, and disputes — the adversarial record that *justifies* the synthesis — are gone. There's no way to:

- Revisit a past deliberation ("what did the devil's advocate say about my database choice last week?")
- Compare deliberations ("how did the cooperative mode differ from red-blue for the same question?")
- Share the full record with a colleague
- Audit the reasoning chain behind a decision

CLI users can work around this with `--output /path/to/keep`. MCP users on `conversus_run` can pass `output_path`. But `conversus_decide` — the primary tool for Desktop Extension users — offers no persistence.

---

## 2. Proposed solution

Three capabilities, in order of implementation priority:

### 2.1 Persist by default (P1)

All `conversus_decide` invocations (on every surface) persist their full output to a known directory:

```
~/.conversus/deliberations/<timestamp>-<slug>/
  question.md
  conversus.yml          # the generated config
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

The `<slug>` is a sanitized version of the question (first ~40 chars). The `<timestamp>` is ISO 8601 compact (`20260412T173000`).

**What changes**: `run_decide_mcp` and `run_decide_cli` copy the output tree to `~/.conversus/deliberations/` before deleting the temp dir. The `DecideResult` response includes a new `output_path` field pointing to the persisted directory.

**Backward compatible**: the temp dir is still created and cleaned up. The persistent copy is additional, not a replacement.

### 2.2 List past deliberations (P2)

A new `conversus_list_deliberations` MCP tool (and CLI command) that scans `~/.conversus/deliberations/` and returns a summary of each:

```json
[
  {
    "timestamp": "2026-04-12T17:30:00",
    "question": "Should I build a timber framed home or...",
    "mode": "cooperative",
    "agents": ["pragmatist", "devils-advocate"],
    "path": "~/.conversus/deliberations/20260412T173000-timber-vs-conventional/"
  }
]
```

### 2.3 View deliberation content (P3)

A new `conversus_show_deliberation` MCP tool that reads a specific file from a past deliberation and returns it as markdown:

```
User: "Show me the devil's advocate review from my timber framing deliberation"
Claude: [calls conversus_show_deliberation with path and file]
→ Returns the full text of devils-advocate/review.md
```

This lets Desktop Extension users browse the full adversarial record from within their chat — no file browser, no terminal, no leaving Claude Desktop.

---

## 3. Surface projection

| Capability | CLI | MCP | Plugin | MCPB |
|---|---|---|---|---|
| Persist by default | ✅ (already has `--output`) | ✅ (new behavior) | n/a | ✅ (via MCP) |
| `list_deliberations` | ✅ | ✅ | ✅ | ✅ |
| `show_deliberation` | ✅ | ✅ | ✅ | ✅ |

These are the "discovery capabilities" that spec 055 Day 7 deferred: `list_deliberations` and `show_deliberation` replace the originally-planned `list_modes`/`list_providers`/`list_presets`/`list_examples`/`show_docs` with something users actually need — access to their own deliberation history, not static metadata they can find in the docs.

---

## 4. Implementation plan

### Phase 1: Persist by default

- Add `~/.conversus/deliberations/` as the default persistence root
- After pipeline completion in `run_decide_mcp`, copy the output tree to the persistence directory
- Add `output_path: str | None` field to `DecideResult` pointing to the persisted copy
- Update `run_decide_cli` to print the persistence path after the synthesis
- Add the persistence path to the structured MCP result so Claude Desktop can reference it

### Phase 2: List deliberations

- Add `list_deliberations` handler to `engine/handlers.py`
- Scan `~/.conversus/deliberations/`, read each directory's `conversus.yml` for metadata
- Add `list_deliberations` capability to `capabilities.py` with CLI + MCP + Plugin + MCPB surfaces
- Project via `make build-surfaces`

### Phase 3: View deliberation content

- Add `show_deliberation` handler that takes a deliberation path + relative file path
- Returns the file content as a string (markdown rendered in Claude Desktop chat)
- Security: validate the path is inside `~/.conversus/deliberations/` (no path traversal)
- Add capability to `capabilities.py`, project

---

## 5. Success criteria

- SC-001: `conversus_decide` in Desktop Extension persists the full output tree to `~/.conversus/deliberations/` without the user requesting it
- SC-002: The `DecideResult` response includes a non-null `output_path` after a successful deliberation
- SC-003: `conversus_list_deliberations` returns a JSON array of past deliberations with timestamps, questions, and modes
- SC-004: `conversus_show_deliberation` returns the full markdown text of any file within a past deliberation
- SC-005: Path traversal outside `~/.conversus/deliberations/` is rejected with a clear error

---

## 6. `conversus init` integration

`conversus init` currently creates per-runtime permission files. This spec extends it to also handle Desktop Extension setup:

```bash
conversus init --runtime claude-desktop
```

What it creates:

- `~/.conversus/deliberations/` — the persistence directory for all deliberation output
- Claude Desktop MCP server registration — adds conversus to Claude Desktop's MCP config (typically `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS) so the extension works without manually installing a `.mcpb` bundle
- Permission grants for the conversus MCP tools

This means Desktop Extension users have **two install paths**:

1. **Double-click the `.mcpb`** — self-contained, no terminal, no CLI. The bundle ships its own Python + dependencies. Deliberation persistence directory is created on first run.
2. **`conversus init --runtime claude-desktop`** — for users who already have conversus installed via pip. Registers the local `mcp_server.py` as a Claude Desktop MCP server and creates the persistence directory. No bundle needed.

Path 1 is for non-technical users. Path 2 is for developers who want the CLI + Desktop Extension from the same install.

---

## 7. Out of scope

- **Search across deliberations** — full-text search of past deliberation content. Useful but complex (index maintenance, relevance ranking). Separate spec.
- **Deliberation diff** — comparing two deliberations on the same question with different modes/agents. Useful but needs a diff rendering strategy. Separate spec.
- **Cloud sync** — syncing `~/.conversus/deliberations/` to a remote backend. Not needed for single-user Desktop Extension.
- **Deliberation deletion** — users can `rm -rf` the directory. No in-tool deletion needed for v1.

---

## 7. Sources

| Source | Use |
|---|---|
| `specs/055-capability-registry.md` | Capability framework that `list_deliberations` and `show_deliberation` register into |
| Spec 055 deliberation (Day 7 deferred items) | Discovery capabilities were deferred from Day 7 — this spec replaces them with user-facing discovery of their own content |
| `CONSTITUTION.md` principles IX, XI | Persistence path is configuration passed as a parameter (not module-level state); deliberation metadata is single-source-of-truth from the persisted `conversus.yml` |
