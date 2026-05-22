# Config Reference

Every conversus deliberation is driven by a YAML config file (`conversus.yml`).

!!! example "Minimal starter config"
    ```yaml
    mode: cooperative
    target: docs/my-proposal.md
    output: docs/my-proposal-review/
    agents:
      - name: pragmatist
        preset: pragmatist
      - name: devils-advocate
        preset: devils-advocate
    ```

!!! warning "Provider defaults differ by surface"
    The provider default depends on how you run conversus:

    - **Config file** (`provider:` field): defaults to `anthropic`
    - **CLI** (`--provider` flag): defaults to `mock`
    - **SDK** (`provider=` parameter): defaults to `mock`

    The CLI `--provider` flag does **not** read the config file's `provider` field -- it always applies its own default. Set `--provider` explicitly if your config specifies a different provider.

## Full schema

```yaml
# --- Required fields ---

mode: cooperative
# One of: cooperative, winner-take-all, prisoners-dilemma, red-blue,
#         negotiation, resource-allocation, fair-division, mechanism-design

target: specs/my-feature/spec.md
# File, file list, or directory (trailing /) to review.
# Directories are expanded to all .md files (non-recursive).
# target:
#   - specs/my-feature/spec.md
#   - specs/my-feature/plan.md
# target: specs/my-feature/

output: specs/my-feature/conversus/
# Where deliberation output files are written.

agents:
  - name: pragmatist              # lowercase alphanumeric, hyphens, underscores
    preset: pragmatist            # Use a built-in preset (see presets/)
    # OR inline prompt:
    # prompt: "You are a pragmatic engineer..."
    docs:                         # Optional grounding documents
      - docs/architecture.md
      - docs/requirements.md
  - name: devils-advocate
    preset: devils-advocate

# --- Optional fields ---

iterations: 1
# Cross-review/revision cycles per round (1-3). Default: 1.
# 1 = standard, 2 = deep, 3 = exhaustive.

rounds: 1
# Outer deliberation rounds (1-5). Default: 1.
# Multi-round adds stagnation detection and cross-round synthesis.

stagnation: detect
# 'detect' (default) or 'ignore'. When 'detect', pipeline stops early
# if dispute count doesn't decrease between rounds.

prior:
  - specs/my-feature/conversus/summary/final.md
# Optional prior iteration context. When this run builds on a previous
# conversus iteration, list the prior outputs so agents have history.

validate_templates: true
# Set false to skip template schema validation. Default: true.

provider: anthropic
# Default provider for the config. Accepts any registered provider
# (mock, demo, anthropic, openai, claude-code, claude-desktop, aider,
# opencode, codex, copilot, gemini, pi, ollama, llama-cpp, vllm).
# See README.md providers table for install + auth per provider.
# CLI --provider flag overrides this.

# --- Arbiter (optional Phase 6) ---

arbiter:
  name: my-arbiter
  prompt: |
    You ARE the system being reviewed. Evaluate disputes from the
    perspective of operational reliability.
  docs:
    - docs/constitution.md
  grounding: docs/constitution.md   # Required: citation source for rulings
  trigger: disputes_remain          # 'disputes_remain' or 'always'
```

## Agent configuration

Agents can be configured three ways:

**Preset only:**
```yaml
- name: pragmatist
  preset: pragmatist
```

**Inline prompt:**
```yaml
- name: backend-lead
  prompt: "You represent the backend team's perspective on this design."
  docs: [docs/backend-architecture.md]
```

**Preset + override:** Inline `prompt` replaces the preset prompt. Inline `docs` replaces preset docs entirely.
```yaml
- name: custom-pragmatist
  preset: pragmatist
  docs: [docs/my-specific-context.md]   # Replaces preset docs
```

**Composed presets:** Combine up to 3 presets. First is identity, rest are modifiers.
```yaml
- name: security-pragmatist
  preset:
    - pragmatist         # Primary identity
    - security           # Domain modifier
```

### Preset categories

| Category | Presets |
|----------|---------|
| `philosophy/` | pragmatist, purist, mechanist |
| `role/` | balanced-arbiter, blue-team, devils-advocate, red-team |
| `domain/` | accessibility, cost, performance, security, ux |
| `tool/` | apm, gh-aw, spec-kit |
| `consumer/` | career-advisor, educator, financial-analyst, health-advocate, housing-advisor, lifestyle-optimizer, relationship-counselor |
| `standard/` | agents-md, agentskills, apm-auditor |

**Qualified names:** When two presets share a name across categories, use qualified names:
```yaml
preset: domain/security     # Explicit category
```

## Plugins

The `plugins:` key declares an ordered list of plugin entries. Each entry has a `name`, a `package` (dotted import path to the module containing the `Plugin` subclass), and an optional `config` dict passed to the plugin at instantiation.

```yaml
plugins:
  - name: equilibrium-scorer
    package: conversus.plugins.nashopt
    config:
      threshold: 0.85
      gamma: 1.0
      solver_timeout: 30.0

  - name: deliberation-logger
    package: my_org.plugins.logger
    # No config needed

  - name: scenario-runner
    package: conversus.plugins.scenarios
    config:
      max_scenarios: 5
```

**Fields per entry:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Human-readable identifier. Used in log messages and output filenames. |
| `package` | Yes | Dotted Python import path to the module containing the `Plugin` subclass. The engine calls `importlib.import_module()` on this value. |
| `config` | No | Dict of plugin-specific configuration. Accessible in the plugin via `self.plugin_config`. |

If a `package` cannot be imported (not installed), a warning is logged and that plugin is skipped. The deliberation proceeds without it.

## Red-blue role enforcement

In `red-blue` mode, every agent must have `role: red` or `role: blue`. At least one of each is required.

```yaml
mode: red-blue
agents:
  - name: attacker
    role: red
    prompt: "Find vulnerabilities."
  - name: defender
    role: blue
    prompt: "Defend with evidence."
```

## Target resolution

| Syntax | Resolves to |
|--------|-------------|
| `target: spec.md` | Single file |
| `target: [a.md, b.md]` | File list |
| `target: specs/` | All `.md` files in directory (non-recursive) |

All paths are relative to the config file's directory.

## Cost formula

For N agents, I iterations, and optional arbiter:

| Phase | Launches |
|-------|----------|
| Review | N |
| Cross-review | N x (N-1) |
| Revision | N x I |
| Disputes | N |
| Synthesis | 1 |
| Arbitration | 1 (if configured) |

**Example:** 3 agents, 1 iteration, no arbiter = 3 + 6 + 3 + 3 + 1 = **16 launches**.

## Common configs

**Quick 2-agent review:**
```yaml
mode: cooperative
target: docs/my-proposal.md
output: docs/my-proposal-review/
agents:
  - name: pragmatist
    preset: pragmatist
  - name: devils-advocate
    preset: devils-advocate
```

**Security red-team with arbiter:**
```yaml
mode: red-blue
target: docs/api-design.md
output: docs/api-design-review/
rounds: 2
agents:
  - name: attacker
    role: red
    preset: red-team
  - name: defender
    role: blue
    preset: blue-team
    docs: [docs/api-design.md]
arbiter:
  name: security-lead
  prompt: "You are the security lead. Evaluate disputed risks."
  grounding: docs/security-policy.md
  trigger: disputes_remain
```
