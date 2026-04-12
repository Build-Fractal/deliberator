# Feature Specification: Settings Architecture (`.conversus/` Directory)

**Feature ID**: `057-settings-architecture`
**Created**: 2026-04-12
**Status**: Draft
**Depends On**: `056-deliberation-persistence`, existing `conversus init` command
**Motivated by**: spec 056 deliberation finding ("workspace-scoped persistence, not global") + analogy with `.claude/` directory convention

---

## 1. Problem

Conversus currently has no coherent settings architecture. Configuration state is scattered:

- **Runtime permissions** — `conversus init` writes `.claude/settings.json`, `.opencode/config.toml`, etc. into the PROJECT directory, but each goes to the runtime's own dot-folder, not a unified `.conversus/` directory
- **Provider credentials** — stored in `~/.conversus-credentials/` (a flat credential store)
- **Deliberation output** — temp dir, deleted after each run (spec 056 addresses this)
- **Default provider/model** — passed as CLI flags every time, no persistent default
- **Project settings** — none. Every invocation is stateless.

The `.claude/` directory provides a proven pattern for how AI tool settings should work:

| Layer | `.claude/` | `.conversus/` (proposed) |
|---|---|---|
| **Global (user-level)** | `~/.claude/` — API keys, memory, global preferences | `~/.conversus/` — provider credentials, default provider/model, global preferences |
| **Project-level** | `<project>/.claude/` — CLAUDE.md, agents, skills, settings.json | `<project>/.conversus/` — project settings, runtime configs, deliberation history |
| **Cascade** | Project overrides global | Project overrides global |

Conversus needs the same two-layer architecture.

---

## 2. Proposed directory structure

### 2.1 Global: `~/.conversus/`

User-level settings that apply to all projects unless overridden.

```
~/.conversus/
  settings.yml              # global defaults (provider, model, mode, max_launches)
  credentials/              # provider OAuth tokens + API keys
    anthropic.json
    openai.json
  memory/                   # (future) cross-project memory, like ~/.claude/memory/
```

**`settings.yml`** example:

```yaml
# Global defaults — overridden by project .conversus/settings.yml
default_provider: anthropic
default_model: claude-sonnet-4-20250514
default_mode: cooperative
max_launches: 20
persistence:
  enabled: true             # persist deliberation output by default (spec 056)
  retention_days: 90        # auto-cleanup after 90 days
```

### 2.2 Project: `<project>/.conversus/`

Project-level settings + deliberation output. Lives inside the project directory (git-trackable if desired).

```
<project>/.conversus/
  settings.yml              # project overrides (provider, model, mode, agents)
  runtimes/                 # per-runtime permission files (from conversus init)
    claude-code.json        # → currently written to .claude/settings.json
    opencode.toml           # → currently written to .opencode/config.toml
    copilot.json            # → currently written to .github/copilot-settings.json
  deliberations/            # output from conversus decide/run (spec 056)
    20260412T173000-timber-vs-conventional/
      question.md
      conversus.yml
      output/
        pragmatist/review.md
        ...
        summary/final.md
```

**`settings.yml`** example:

```yaml
# Project-level overrides — takes precedence over ~/.conversus/settings.yml
default_provider: claude-code    # this project uses Claude Code
default_mode: winner-take-all    # this project prefers decisive outcomes
agents:                          # project-specific agent presets
  - name: security-reviewer
    preset: role/security-auditor
  - name: cost-optimizer
    preset: philosophy/pragmatist
```

### 2.3 Resolution order

Settings cascade from most-specific to least-specific, identical to `.claude/`:

```
CLI flag (--provider anthropic)
  ↓ overrides
conversus.yml (in the config file itself)
  ↓ overrides
<project>/.conversus/settings.yml
  ↓ overrides
~/.conversus/settings.yml
  ↓ overrides
Built-in defaults (provider=mock, mode=cooperative, etc.)
```

---

## 3. Per-runtime settings

Different AI runtimes have different configuration needs. `conversus init --runtime <name>` currently writes each runtime's config to that runtime's native location. This spec proposes also writing a canonical copy inside `.conversus/runtimes/`:

| Runtime | Native location (current) | `.conversus/runtimes/` (proposed) |
|---|---|---|
| claude-code | `.claude/settings.json` | `.conversus/runtimes/claude-code.json` |
| claude-desktop | `~/Library/.../claude_desktop_config.json` | `.conversus/runtimes/claude-desktop.json` |
| opencode | `.opencode/config.toml` | `.conversus/runtimes/opencode.toml` |
| copilot | `.github/copilot-settings.json` | `.conversus/runtimes/copilot.json` |
| gemini | `.gemini/settings.json` | `.conversus/runtimes/gemini.json` |
| codex | `.codex/settings.json` | `.conversus/runtimes/codex.json` |
| aider | `.aider.conf.yml` | `.conversus/runtimes/aider.yml` |

**Why both?** The native location is what the runtime reads. The `.conversus/runtimes/` copy is what `conversus status` reads to show which runtimes are configured, and what a future `conversus init --sync` would use to re-generate native configs after a settings change.

---

## 4. How this changes existing commands

### `conversus init`

**Before**: writes runtime permission files to native locations only.

**After**:
1. Creates `<project>/.conversus/` directory
2. Writes `settings.yml` with the chosen provider/model/mode defaults
3. Writes `runtimes/<name>.json` for each selected runtime
4. ALSO writes the native location files (backward compatible)
5. If `~/.conversus/` doesn't exist, creates it with empty `settings.yml` and `credentials/`

### `conversus decide` / `conversus run`

**Before**: provider/model/mode must be specified as flags every time.

**After**: reads defaults from the cascade (`project settings.yml → global settings.yml → built-in`). Flags still override.

### `conversus status`

**Before**: reads from credential store only.

**After**: also reports which project-level settings are active, which runtimes are configured, and the effective cascade for each setting.

### `conversus login` / `conversus logout`

**Before**: writes to `~/.conversus-credentials/`.

**After**: writes to `~/.conversus/credentials/`. Migration: if the old credential store exists, read from it but write to the new location. Eventually remove the old path.

---

## 5. Relation to spec 056

Spec 056 (deliberation persistence) proposed `~/.conversus/deliberations/` as the persistence directory. The deliberation on spec 056 unanimously concluded that **workspace-scoped persistence is correct** — deliberation output belongs with the project, not in a global directory.

This spec confirms that design:
- Deliberation output goes to `<project>/.conversus/deliberations/` (workspace-scoped)
- `~/.conversus/` is for user-level settings and credentials only
- The `persistence.enabled` and `persistence.retention_days` settings control the behavior

---

## 6. Success criteria

- SC-001: `conversus init` creates `<project>/.conversus/settings.yml` and `<project>/.conversus/runtimes/`
- SC-002: `conversus decide` reads `default_provider` from the settings cascade without requiring `--provider` flag
- SC-003: `conversus status` shows the effective settings cascade (which setting came from which layer)
- SC-004: `conversus login anthropic` writes credentials to `~/.conversus/credentials/anthropic.json`
- SC-005: A project with `.conversus/settings.yml` setting `default_provider: claude-code` does not need `--provider claude-code` on every invocation
- SC-006: CLI flags override project settings which override global settings which override built-in defaults

---

## 7. Out of scope

- **Settings UI** — no web interface or TUI for editing settings. YAML files are the interface.
- **Settings sync** — no cloud sync of `~/.conversus/` across machines.
- **Settings encryption** — credentials are stored as plain JSON (same as current). Keychain integration is a separate concern.
- **Settings schema validation** — the settings.yml format should be validated, but the schema definition + validation tooling is a follow-up.

---

## 8. Sources

| Source | Use |
|---|---|
| `specs/056-deliberation-persistence.md` | Deliberation persistence that depends on this settings architecture |
| Spec 056 deliberation results | Unanimous: workspace-scoped persistence, developer-first, enhance existing `--output` |
| `.claude/` directory convention | The proven pattern this spec follows for two-layer cascade |
| `engine/project.py::init_project` | Current `init` implementation that needs extension |
| `engine/auth.py::CredentialStore` | Current credential storage that moves to `~/.conversus/credentials/` |
