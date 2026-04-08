# Spec 050: Cascading Settings System

**Status**: Draft
**Author**: Brian Slater + Claude Opus 4.6
**Date**: 2026-04-06
**Depends on**: 042 (execution providers), 048 (governance mode)
**Replaces**: `.conversusrc` from spec 048 §3

---

## 1. Problem

Conversus currently has no unified settings system. Configuration is scattered:

- Provider selection: CLI `--provider` flag only, no defaults
- Model selection: CLI `--model` flag only
- Permissions: `conversus init` generates per-runtime configs, but nothing reads them back
- Governance config: `.conversusrc` from spec 048 is a standalone format
- No user-level defaults (every project starts from scratch)

Claude Code solved this with a cascading settings system: `~/.claude/settings.json` → `<project>/.claude/settings.json` → CLI flags. Conversus should mirror that pattern.

## 2. Design: Three-Level Cascade

Settings resolve **most-specific wins**, identical to Claude Code:

```
~/.conversus/settings.json          # Level 1: Global user defaults
<project>/.conversus/settings.json  # Level 2: Project overrides
conversus.yml agent-level fields    # Level 3: Per-agent overrides
CLI --provider / --model            # Level 4: Per-invocation (highest priority)
```

### 2.1 Level 1: Global (`~/.conversus/settings.json`)

User-wide defaults. Created by `conversus config set` or manual edit.

```json
{
  "default_provider": "claude-code",
  "default_model": "sonnet",
  "providers": {
    "anthropic": {
      "model": "claude-sonnet-4-20250514"
    },
    "ollama": {
      "base_url": "http://localhost:11434/v1",
      "model": "qwen3:0.6b"
    },
    "claude-code": {
      "model": "sonnet",
      "skip_permissions": false,
      "max_budget_usd": 5.00
    }
  },
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Glob", "Grep"],
    "deny": []
  },
  "telemetry": {
    "cost_tracking": true,
    "usage_file": "~/.conversus/usage.jsonl"
  }
}
```

### 2.2 Level 2: Project (`.conversus/settings.json`)

Project-specific overrides. Created by `conversus init`. Checked into the repo.

```json
{
  "default_provider": "claude-code",
  "default_model": "opus",
  "runtimes": ["claude-code", "opencode", "aider"],
  "output_dir": "output",
  "providers": {
    "claude-code": {
      "model": "opus",
      "system_prompt": "You are reviewing healthcare specifications.",
      "max_budget_usd": 2.00
    },
    "ollama": {
      "model": "llama3:70b"
    }
  },
  "governance": {
    "grounding": ["CLAUDE.md", "AGENTS.md", "constitution.md"],
    "default_mode": "red-blue",
    "arbiter_trigger": "disputes_remain",
    "default_agents": [
      {"name": "architect", "provider": "claude-code"},
      {"name": "reviewer", "provider": "ollama"}
    ]
  }
}
```

### 2.3 Level 3: Agent Config (`conversus.yml`)

Per-agent overrides within a deliberation config. Already implemented.

```yaml
agents:
  - name: skeptic
    provider: ollama
    model: qwen3:0.6b
    prompt: ...
```

### 2.4 Level 4: CLI Flags

Per-invocation overrides. Highest priority.

```bash
conversus run config.yml --provider claude-code --model opus
```

## 3. Resolution Algorithm

```python
def resolve_setting(key: str) -> Any:
    """Resolve a setting through the cascade."""
    # Level 4: CLI flag (if provided)
    if cli_flags.get(key) is not None:
        return cli_flags[key]
    
    # Level 3: Agent config (if in agent context)
    if agent_config and getattr(agent_config, key, None) is not None:
        return getattr(agent_config, key)
    
    # Level 2: Project settings
    project = read_settings(find_conversus_dir(cwd))
    if project.get(key) is not None:
        return project[key]
    
    # Level 1: Global settings
    global_settings = read_settings(Path.home() / ".conversus")
    if global_settings.get(key) is not None:
        return global_settings[key]
    
    # Default
    return DEFAULTS[key]
```

For nested keys (e.g., `providers.claude-code.model`), project-level
values **replace** (not merge with) global-level values for that
provider. This prevents surprising cross-level interactions.

## 4. CLI Commands

### `conversus config`

```bash
# View effective settings (all levels merged)
conversus config show

# View a specific level
conversus config show --level global
conversus config show --level project

# Set a global default
conversus config set default_provider claude-code
conversus config set default_model opus

# Set a project default (writes to .conversus/settings.json)
conversus config set --project default_model opus
conversus config set --project providers.ollama.model llama3:70b
```

### `conversus init` (updated)

The existing `conversus init` command becomes a convenience wrapper:
1. Creates `.conversus/settings.json` (Level 2)
2. Generates runtime-specific permission configs (`.claude/`, `.opencode/`, etc.)
3. Creates `.conversus/output/` and `.gitignore`

## 5. Relationship to `.conversusrc` (Spec 048)

Spec 048 §3 defined `.conversus/.conversusrc` as a YAML governance config.
This spec **subsumes** `.conversusrc` by moving governance settings into
the `"governance"` key of `.conversus/settings.json`.

Migration path:
- `.conversusrc` is still read for backward compat (if `settings.json` has no `governance` key)
- New projects use `settings.json` exclusively
- Spec 048 implementation should read from `settings.governance`, not `.conversusrc`

## 6. File Layout

After `conversus init --runtime claude-code --runtime ollama`:

```
~/.conversus/
├── settings.json              # Global defaults
└── usage.jsonl                # Cost tracking log

project/
├── .conversus/
│   ├── settings.json          # Project settings + governance
│   ├── output/                # Deliberation output (gitignored)
│   └── .gitignore
├── .claude/
│   └── settings.json          # Claude Code permission grants
├── conversus.yml              # Deliberation config (per-run)
└── ...
```

## 7. Implementation Phases

| Phase | What | LoC |
|---|---|---|
| 1 | `SettingsResolver` class with 4-level cascade | ~150 |
| 2 | Wire into `run_engine()` and `resolve_execution_provider()` | ~50 |
| 3 | `conversus config show/set` CLI commands | ~100 |
| 4 | Migrate spec 048 governance to `settings.governance` | ~50 |
| 5 | Global `~/.conversus/` init on first run | ~30 |

**Total**: ~380 lines. The `SettingsResolver` is the only new module;
everything else is wiring existing code to read from it.

## 8. Open Questions

1. **Should `.conversus/settings.json` be gitignored or committed?** Recommendation: committed (like `.claude/settings.json`). Project teams share provider and governance defaults.
2. **Should we support `.conversus/settings.local.json` for local overrides?** Same pattern as `.env.local` — not committed, overrides the committed settings.
3. **TOML vs JSON?** Claude Code uses JSON. Python ecosystem prefers TOML. Recommendation: JSON for consistency with Claude Code; TOML as optional alternative later.
