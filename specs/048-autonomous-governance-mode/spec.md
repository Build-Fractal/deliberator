# Feature Specification: Autonomous Governance Mode — Conversus as Background Quality Gate

**Feature ID**: `048-autonomous-governance-mode`
**Created**: 2026-04-04
**Status**: Active 2026-04-29 (promoted from draft) — drift-analyzed + 3-agent deliberation resolved dependencies; specs 042/050/057 closed; governance config settled; implementation blockers documented.
**Depends On**: `001-subject-arbitration` (arbiter foundation), `011-phase-consensus-gates` (done — existing gate mechanism), `042-execution-providers` (headless execution — CRITICAL dependency, **Accepted 2026-04-05** — see [`../042-execution-providers/conversus-output/arbitration/resolution.md`](../042-execution-providers/conversus-output/arbitration/resolution.md)), `046-commentator-agents` (PR comment output format), `050-cascading-settings` (governance config schema and 4-level cascade — CRITICAL dependency, governs §3 config format and merge semantics)
**042 Integration Note**: Spec 042's Phase 6 binding arbitration resolved key 048 dependencies: (a) `settings.governance.default_agents` schema accepts URL entries from v1 with "not yet supported" error (enables future A2A activation as config change, not schema migration — see §3.1 below and spec 042 binding condition #3); (b) `claude-code` executor is direct `claude` CLI subprocess via spec 042's `SubprocessProvider`, no `claude-agent-sdk` dependency; (c) the `ExecutionTask`/`ExecutionResult` protocol shape is A2A-Task-Request-compatible from Week 1 so governance-as-remote-agent deployments work additively (binding condition #1). Spec 042 shipped 12 execution providers (not the original 4-provider v1 plan).
**Docs Update**: New docs/user-guide/autonomous-mode.md; new docs/developer-guide/governance-arbitration.md; update docs/user-guide/cli.md with `conversus governance` subcommand
**Origin**: User vision statement (2026-04-04): "I would like to gear conversus toward being a tool that runs outside of user interaction. It can be the CLI that runs outside of your CLI." Conversus should enforce project governance documents (constitution, AGENTS.md, CLAUDE.md) automatically via arbiter-backed deliberation, invoked from CI/cron/hooks without human present.

---

## 0. Decision Record — Drift Deliberation (2026-04-05)

A 3-agent drift deliberation (implementer, settings-advocate, governance-purist) was run against the codebase after spec 042 shipped. The full output is in `.conversus/output-048-drift/`. Key resolutions:

1. **Config format settled**: `.conversusrc` (YAML) is superseded. Governance config lives in `.conversus/settings.json` under the `"governance"` key, per spec 050. See revised §3.
2. **Provider count updated**: Spec 042 shipped 12 execution providers, not 4. References updated throughout. See §9 (Constraints) and §14 (Relationship to Other Specs).
3. **Executor name corrected**: The registered provider name is `claude-code`, not `claude-code-headless`. The `SubprocessProvider` wraps the `claude` CLI directly.
4. **Exit code 4 (WARNING) confirmed**: All three agents agreed `4=WARNING` was missing from the exit code scheme docstring in `context.py` but was already specified in FR-014/FR-015. Now explicit in §5 and §7.
5. **Merge semantics for grounding docs**: FR-007's additive-only rule for grounding documents is preserved. Spec 050's replace semantics apply to other config namespaces (e.g., `providers.*`). The `SettingsResolver` must implement per-namespace merge strategies: governance grounding keys use additive (union) merge, not replace. This is the key distinction between specs 048 and 050.
6. **Phase 1 blockers added**: Four implementation prerequisites surfaced by the deliberation are now tracked in §12 Phase 1. See below.
7. **Spec 050 dependency added**: Spec 050 (Cascading Settings) is now a hard dependency. See §9 and §14.

---

## 1. The Vision

Conversus today is an **interactive** tool. You open Claude Code, invoke `/conversus run`, watch the deliberation unfold, and read the synthesis. That's valuable, but it means conversus only runs when a human is present AND motivated AND has capacity to interpret results.

The autonomous governance vision flips this: conversus becomes a **background quality gate** — like `pytest`, `mypy`, `ruff`, or `shellcheck`. It runs on every PR, every push to main, every deployment. It reads the project's governance documents (constitution, agents, policies) and uses an arbiter to judge whether the proposed change complies. Violations block the merge. Compliance is silent.

**The "CLI that runs outside your CLI" reframe**: today conversus runs inside Claude Code. In the new vision, conversus runs in GitHub Actions, pre-commit hooks, cron jobs, webhook handlers, and any headless context — producing machine-readable rulings that gate merges, populate dashboards, or log to audit trails. Claude Code is one execution surface; it's not the only one.

**Why arbiters are the right mechanism**: governance documents are the LAW. The arbiter is the JUDGE. Reviewers argue cases; the arbiter applies the law. This is the pattern conversus was built for (spec 001), but it's been used interactively where humans configure the arbiter per-run. Autonomous mode makes the arbiter **always configured** — from persistent project-level config — so every deliberation inherits the governance framework automatically.

---

## 2. The Three-Layer Model

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Execution Surfaces                                │
│  ─────────────────────────                                  │
│  • GitHub Actions (PR gate)                                 │
│  • Git pre-commit / pre-push hooks                          │
│  • Cron / scheduled audits                                  │
│  • Webhook handlers (external events)                       │
│  • Claude Code (interactive — unchanged)                    │
│  • CLI: `conversus governance <target>`                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  Layer 2: Autonomous Mode Engine                            │
│  ─────────────────────────────                              │
│  • Reads .conversus/settings.json "governance" key          │
│  • Auto-configures arbiter from configured grounding docs   │
│  • Resolves target from git diff / changed files            │
│  • Runs deliberation headlessly (via 12 execution providers)│
│  • Returns structured verdict (PASS/BLOCK/ERROR/META_DISPUTE│
│    /WARNING)                                                │
│  • Optionally posts commentary as PR comment                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  Layer 1: Existing Conversus Engine                         │
│  ──────────────────────────────                             │
│  • Phases 1-6 (unchanged)                                   │
│  • Arbitration (spec 001, with auto-grounding extension)    │
│  • Execution providers (spec 042)                           │
│  • Gates (spec 011-phase-consensus-gates)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Governance Configuration

**Updated 2026-04-05** per drift deliberation (§0) and spec 050 (Cascading Settings).

Governance config lives in `.conversus/settings.json` under the `"governance"` key. This replaces the original `.conversusrc` YAML design. The governance key participates in spec 050's 4-level cascade (default -> global -> project -> local) but grounding documents use **additive (union) merge**, not replace — this is the critical merge semantics distinction from spec 050's default replace behavior.

### 3.1 Schema (settings.json)

```json
{
  "default_provider": "claude-code",
  "default_model": "claude-sonnet-4-20250514",
  "output_dir": ".conversus/output",
  "runtimes": {},
  "governance": {
    "version": 1,
    "grounding": {
      "documents": [
        { "path": "CONSTITUTION.md", "weight": "highest" },
        { "path": "AGENTS.md", "weight": "high" },
        { "path": "CLAUDE.md", "weight": "high" },
        { "path": "docs/principles.md", "weight": "medium" },
        { "path": ".github/CODE_OF_CONDUCT.md", "weight": "medium" }
      ],
      "globs": [
        "docs/adr/*.md",
        "docs/policies/*.md"
      ]
    },
    "default_agents": [
      { "preset": "security-reviewer" },
      { "preset": "architecture-reviewer" },
      { "preset": "maintainability-reviewer" }
    ],
    "arbiter": {
      "name": "project-constitution-arbiter",
      "prompt": "You are the project's governance arbiter. Your rulings enforce the documents listed in `grounding`. You do not have independent opinions — you apply the law as written. When documents conflict, higher weight wins. When weight ties, the more specific document wins.",
      "trigger": "always",
      "timing": "final",
      "influence": "binding"
    },
    "gates": {
      "pr": {
        "target": "{changed_files}",
        "mode": "cooperative",
        "rounds": 1,
        "pass": "max_disputes 0",
        "commentary": "enabled",
        "post_to_pr": true
      },
      "push_main": {
        "target": "{changed_files}",
        "mode": "cooperative",
        "rounds": 1,
        "pass": "max_disputes 0",
        "commentary": "enabled",
        "post_to_issue": "compliance-log"
      },
      "pre_commit": {
        "target": "{staged_files}",
        "mode": "cooperative",
        "rounds": 1,
        "pass": "max_disputes 0",
        "commentary": "disabled"
      },
      "scheduled_audit": {
        "target": "specs/*/spec.md",
        "mode": "cooperative",
        "rounds": 2,
        "pass": "always",
        "commentary": "enabled"
      }
    },
    "executor": {
      "provider": "claude-code"
    },
    "output": {
      "base_dir": ".conversus/runs/",
      "retention_days": 90,
      "archive_on": [
        { "pass": false },
        { "gate": "scheduled_audit" }
      ]
    }
  }
}
```

The `default_agents` array accepts three entry forms from v1 (per spec 042 binding condition #3):
- `{ "preset": "<name>" }` — inline preset reference (v1, supported)
- `{ "url": "<a2a-server-url>", "name": "..." }` — remote A2A agent (schema valid in v1, runtime returns "not yet supported" until the A2A ecosystem has counterparties — see spec 042 §0)
- `{ "name": "...", "prompt": "...", "docs": [...] }` — inline definition (v1, supported)

### 3.2 Backward compatibility (.conversusrc fallback)

Per spec 050 §5: if `settings.json` exists but has **no `"governance"` key**, the engine falls back to reading `.conversus/.conversusrc` (the original YAML format). This supports projects that adopted the YAML config before the settings.json migration.

**Deprecation path**: When `.conversusrc` fallback is triggered, the engine MUST emit a deprecation warning and recommend running `conversus config migrate` to move governance config into `settings.json`. The `.conversusrc` format will be removed in a future major version.

**Original YAML format** (deprecated, shown for migration reference):

```yaml
# .conversus/.conversusrc — DEPRECATED, migrate to settings.json governance key
version: 1
grounding:
  documents:
    - path: CONSTITUTION.md
      weight: highest
    # ...
default_agents:
  - preset: security-reviewer
  # ...
arbiter:
  name: project-constitution-arbiter
  # ...
gates:
  pr:
    target: "{changed_files}"
    # ...
executor:
  provider: claude-code
output:
  base_dir: .conversus/runs/
  retention_days: 90
```

### 3.3 Why settings.json

- **Unified config surface**: all conversus configuration in one file, per spec 050's cascading settings design. No proliferation of dotfiles.
- **`.conversus/` directory**: scoped namespace. Future files (credentials, run cache, scenario snapshots) live here.
- **JSON over YAML**: consistency with the codebase's `settings.json` format already in use by `engine/project.py`.
- **Cascade participation**: governance config inherits from global/org-level settings via spec 050's 4-level cascade, enabling org-wide governance baselines that projects extend.

### 3.4 Config discovery

On invocation, conversus walks upward from the target file/cwd until it finds `.conversus/settings.json` (via the existing `find_conversus_dir()` in `engine/project.py`). If found, it reads the `governance` key. If the key is absent, it falls back to `.conversus/.conversusrc` (§3.2). If neither is found, autonomous mode is **not available** — the user must either create the config or use the interactive `conversus run` path.

### 3.5 Merge semantics for governance keys

When multiple cascade levels define governance config (e.g., org-level `settings.json` and project-level `settings.json`), the merge strategy depends on the key namespace:

- **`governance.grounding.documents`** and **`governance.grounding.globs`**: **additive (union) merge**. A project-level grounding list extends the org-level list — it cannot narrow or remove entries. This preserves FR-007 (per-run configs may extend but must not narrow the grounding set).
- **`governance.executor`**, **`governance.arbiter`**, **`governance.output`**: **replace merge** (spec 050 default). Project-level values override org-level values.
- **`governance.gates`**: **deep merge by gate name**. A project-level gate definition overrides the same-named org-level gate; org-level gates not redefined at project level are inherited.
- **`governance.default_agents`**: **replace merge**. Project-level agent list replaces org-level (agent selection is project-specific).

The `SettingsResolver` must implement these per-namespace merge strategies. This is the architectural distinction from spec 050's default replace-all behavior.

---

## 4. Auto-Grounding Rule

This is the central behavioral change from existing arbiter semantics.

### 4.1 Current arbiter behavior

In `conversus run config.yml`, the arbiter's grounding document is declared per-run:

```yaml
arbiter:
  grounding: docs/constitution.md
```

The arbiter reads ONLY that document when ruling.

### 4.2 Autonomous-mode arbiter behavior

When conversus runs in autonomous mode (via `conversus governance` or a configured gate), the arbiter automatically loads **all** documents in the project's `settings.governance.grounding` section, regardless of what the per-run config says.

**The rule**: if an arbiter fires in autonomous mode, it MUST read every grounding document before issuing rulings. The per-run config cannot narrow the grounding set — only extend it.

This means:
- A constitution change affects every future deliberation without editing per-run configs
- An agents.md update propagates automatically
- New ADRs in `docs/adr/` are picked up by the next scheduled audit
- Users cannot accidentally or intentionally skip grounding documents

### 4.3 Conflict resolution

When grounding documents disagree, the `weight` field determines precedence:
- `highest` > `high` > `medium` > `low`
- Within a weight tier, file modification time is the tiebreaker (newer wins)

When documents are ambiguous or mutually contradictory with no weight difference, the arbiter MUST:
1. Surface the conflict explicitly in the ruling
2. Set `verdict: META_DISPUTE` (new verdict type)
3. NOT issue a binding ruling — the dispute is escalated to a human

This prevents the arbiter from silently choosing a side when the governance documents themselves are unclear.

---

## 5. The `conversus governance` Subcommand

New CLI entry point for autonomous runs:

```bash
# Run governance check on a target
conversus governance <target-path>

# Run the PR gate (auto-detects changed files)
conversus governance --gate pr

# Run scheduled audit
conversus governance --gate scheduled_audit

# Post results to a PR
conversus governance --gate pr --post-to pr-42

# Dry run (no side effects, shows what would happen)
conversus governance --gate pr --dry-run

# Override grounding (adds, doesn't replace — additive only)
conversus governance --gate pr --add-grounding docs/new-policy.md

# Exit codes matter for CI:
#   0 — PASS (all rules satisfied)
#   1 — BLOCK (violations detected, merge should fail)
#   2 — ERROR (config invalid, target missing, arbiter failed)
#   3 — META_DISPUTE (grounding docs contradict each other)
#   4 — WARNING (advisory verdict, not blocking)
```

### 5.1 Output format (machine-readable)

```json
{
  "schema_version": 1,
  "verdict": "BLOCK",
  "gate": "pr",
  "target": ["src/auth.py", "tests/test_auth.py"],
  "grounding_documents": [
    {"path": "CONSTITUTION.md", "weight": "highest", "sha": "abc123"},
    {"path": "AGENTS.md", "weight": "high", "sha": "def456"}
  ],
  "agents": ["security-reviewer", "architecture-reviewer", "maintainability-reviewer"],
  "rulings": [
    {
      "rule": "CONSTITUTION.md §3.2 — All auth changes require threat model",
      "verdict": "VIOLATED",
      "evidence": "src/auth.py introduces new auth method without threat model doc",
      "severity": "blocking"
    }
  ],
  "summary": "1 blocking violation found. See rulings.",
  "run_id": "gov-2026-04-04-abc123",
  "duration_ms": 12400,
  "output_dir": ".conversus/runs/gov-2026-04-04-abc123/",
  "commentary_url": ".conversus/runs/gov-2026-04-04-abc123/commentary/color-commentary.md"
}
```

This structured output is the interface for GitHub Actions, dashboards, and downstream tooling.

### 5.2 Human-readable output

In addition to JSON, conversus governance produces a concise human summary for terminal use:

```
governance PR gate — BLOCK

Target: src/auth.py, tests/test_auth.py (2 files)
Grounding: CONSTITUTION.md (highest), AGENTS.md (high), CLAUDE.md (high)

1 violation found:

  ❌ CONSTITUTION.md §3.2 — All auth changes require threat model
     src/auth.py introduces new auth method without threat model doc
     Severity: blocking

Run ID: gov-2026-04-04-abc123
Full output: .conversus/runs/gov-2026-04-04-abc123/
Commentary: .conversus/runs/gov-2026-04-04-abc123/commentary/color-commentary.md

Exit code: 1 (BLOCK)
```

---

## 6. GitHub Actions Integration

### 6.1 Workflow template

```yaml
# .github/workflows/conversus-governance.yml
name: Conversus Governance

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Nightly audit

jobs:
  pr-gate:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run governance gate
        run: |
          conversus governance --gate pr \
            --post-to pr-${{ github.event.pull_request.number }}

  scheduled-audit:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run audit
        run: conversus governance --gate scheduled_audit
      - name: Post results to issue
        run: |
          gh issue comment compliance-log \
            --body-file .conversus/runs/latest/report.md
```

### 6.2 PR comment format

When `post_to_pr: true`, conversus posts a comment using the commentator output (spec 046):

```markdown
## Conversus Governance: BLOCK

**Gate**: `pr` · **Agents**: security-reviewer, architecture-reviewer, maintainability-reviewer · **Duration**: 12.4s

### Rulings

| Document | Rule | Verdict | Severity |
|----------|------|---------|----------|
| CONSTITUTION.md §3.2 | All auth changes require threat model | ❌ VIOLATED | blocking |

### What Happened

The security-reviewer flagged that `src/auth.py` introduces a new JWT signing algorithm (HS512) without a corresponding threat model document. The architecture-reviewer agreed. The maintainability-reviewer argued the change was well-factored and tested. The arbiter ruled that CONSTITUTION.md §3.2's requirement is unambiguous and binding — no exception for well-factored code.

### How to Fix

1. Add `docs/threat-models/auth-hs512.md` describing the change's threat model
2. Re-request review — the governance check will re-run automatically

---
[Full run output](.conversus/runs/gov-2026-04-04-abc123/) · [Commentary](.conversus/runs/gov-2026-04-04-abc123/commentary/color-commentary.md) · Gate: pr · Exit code: 1
```

The narrative ("What Happened") comes from the commentator agents (spec 046). The tabular rulings come from the arbiter's structured output. The "How to Fix" section is generated by the arbiter based on the violated rules.

---

## 7. Functional Requirements

### Config discovery and parsing
- **FR-001**: `conversus governance` MUST walk upward from target/cwd to find `.conversus/settings.json` (via `find_conversus_dir()`), then read the `"governance"` key. If `"governance"` is absent, fall back to `.conversus/.conversusrc` per §3.2.
- **FR-002**: If neither `settings.json` governance key nor `.conversusrc` is found, `conversus governance` MUST exit with code 2 (ERROR) and a clear message.
- **FR-003**: Config MUST be validated against a JSON Schema — invalid configs (malformed JSON, missing required fields, unknown keys) exit with code 2 and detailed errors. `read_settings()` MUST raise `ConfigError` on corrupt JSON, not silently fall back to defaults.
- **FR-004**: Grounding document paths in config MUST be resolved relative to the `.conversus/` directory.
- **FR-005**: Missing grounding documents MUST NOT silently fail — the run exits with code 2 listing missing files.

### Auto-grounding
- **FR-006**: When autonomous mode fires an arbiter, it MUST load every grounding document from `settings.governance.grounding`.
- **FR-007**: Per-run configs MAY extend but MUST NOT narrow the autonomous grounding set.
- **FR-008**: Weight-based conflict resolution MUST be deterministic (highest > high > medium > low; mtime tiebreak).
- **FR-009**: When grounding documents contradict each other with no weight difference, the verdict MUST be `META_DISPUTE` (exit code 3).

### Gate invocation
- **FR-010**: Each named gate in `settings.governance.gates` MUST be invokable via `--gate <name>`.
- **FR-011**: Target resolution MUST support `{changed_files}` (git diff against main), `{staged_files}` (git diff --staged), glob patterns, and explicit paths.
- **FR-012**: The `pass` criterion MUST support `converged`, `max_disputes N`, and `always` (same as spec 011 gates).
- **FR-013**: The `commentary` flag MUST control whether commentator agents (spec 046) run after the deliberation.

### Exit codes
- **FR-014**: Exit codes MUST be: 0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE, 4=WARNING.
- **FR-015**: Exit codes MUST be stable — they are CI interface.

### Output
- **FR-016**: Structured JSON output MUST be written to `{output}/report.json`.
- **FR-017**: Human-readable markdown output MUST be written to `{output}/report.md`.
- **FR-018**: When `commentary: enabled`, commentator agents MUST produce narrative files.
- **FR-019**: When `post_to_pr: true`, the report MUST be posted as a PR comment via `gh` CLI.
- **FR-020**: Output retention MUST be enforced by `retention_days` — runs older than the retention window are deleted unless archived.

### Integration
- **FR-021**: `conversus governance` MUST be invokable without Claude Code running (requires spec 042 execution providers).
- **FR-022**: Git hook integration MUST support pre-commit and pre-push via a shim script.
- **FR-023**: GitHub Actions integration MUST work via a documented workflow template.
- **FR-024**: The subcommand MUST support `--dry-run` mode that shows what would run without executing.

### Phase 1 blockers (from drift deliberation)
- **FR-025**: `read_settings()` MUST raise `ConfigError` on corrupt JSON (e.g., `JSONDecodeError`). Silent fallback to defaults when the file exists but is malformed is a critical vulnerability — governance could silently deactivate on a parse error.
- **FR-026**: The `governance` key in `settings.json` MUST be validated against a JSON Schema before any governance operation. Schema validation covers required fields (`version`, `grounding`, `arbiter`), allowed types, and enum constraints (e.g., weight values). Invalid governance config exits with code 2 and line-level error detail.
- **FR-027**: `conversus init` MUST accept a `--governance` flag that writes a governance config stub into `settings.json`. If governance grounding documents are detected in the project (e.g., `CONSTITUTION.md`, `AGENTS.md`), `init` SHOULD suggest the flag. Without `--governance`, `init` writes `settings.json` with no `governance` key (current behavior).
- **FR-028**: `config set` MUST enforce write protection for governance keys. Mutations to `governance.grounding`, `governance.arbiter`, and `governance.gates` via `config set` MUST require an explicit `--governance` flag or `--force` flag. This prevents accidental narrowing of grounding documents or weakening of gate pass criteria via casual `config set` commands.

---

## 8. Success Criteria

- **SC-001**: `conversus governance --gate pr` runs to completion against a PR with governance documents and exits with the correct code.
- **SC-002**: Modifying `CONSTITUTION.md` immediately affects the next run's arbiter — no per-run config changes required.
- **SC-003**: A scheduled audit runs nightly via GitHub Actions cron and posts a daily compliance report.
- **SC-004**: A contradictory governance document produces a `META_DISPUTE` verdict with exit code 3 and a clear explanation.
- **SC-005**: Missing grounding documents produce exit code 2 with a clear error — never a silent fallback.
- **SC-006**: PR comments generated by the governance gate are readable by a non-conversus-user and clearly explain the verdict.
- **SC-007**: Running `conversus governance --dry-run --gate pr` shows the targets, agents, arbiter, and grounding docs without side effects.
- **SC-008**: A misconfigured `settings.json` governance key (invalid JSON, missing required fields, impossible gate) produces exit code 2 and a detailed validation error.

---

## 9. Constraints

- **Spec 042 dependency**: Autonomous mode REQUIRES execution providers (headless execution via 12 registered providers). Cannot ship before 042. The registered executor name is `claude-code` (not `claude-code-headless`).
- **Spec 046 dependency**: Commentary in PR comments requires commentator agents. Can ship without 046 by disabling commentary; commentary becomes available once 046 lands.
- **Spec 050 dependency**: Governance config lives in `settings.json` under the `"governance"` key per spec 050's cascading settings design. The `SettingsResolver` must implement per-namespace merge strategies — governance grounding uses additive (union) merge, not replace. Cannot ship before 050's `SettingsResolver` supports custom merge strategies.
- **Spec 047 soft dependency**: SLA rules in constitutions ("reviews must complete within 24 hours") require structured duration parsing. Without 047, SLA rules are text-only and the arbiter reasons about them qualitatively.
- **No silent fallbacks**: if anything is missing (config, grounding doc, execution provider), the run exits with code 2. Never silently skip. This includes corrupt JSON in `settings.json` — `read_settings()` must fail loud (FR-025).
- **Deterministic output**: exit codes, JSON schema, and report format are stable contracts. Breaking changes require a major version bump.
- **Backward compat**: interactive `conversus run` is unchanged. Autonomous mode is additive.
- **No human required at runtime**: by design, autonomous mode runs without a person present. All decisions are made by the arbiter against the governance documents.
- **Security**: `conversus governance` MUST NOT accept arbitrary code execution from governance config. Grounding documents are read-only; gate definitions are declarative only. Governance keys in `config set` are write-protected (FR-028).

---

## 10. Open Questions (from user)

The user explicitly asked these questions — they remain open and need resolution before implementation.

### Q1: Opt-in granularity
Should autonomous mode be **opt-in per repo** (user writes governance config) or **opt-in per run** (CI step explicitly invokes `conversus governance`)?

**Possible answers:**
- **A**: Per-repo — presence of `settings.json` governance key auto-enables governance for any `conversus` invocation in that tree. Pro: zero-config discovery. Con: surprise runs.
- **B**: Per-run — users must invoke `conversus governance` explicitly; plain `conversus run` never loads governance. Pro: explicit opt-in. Con: users forget.
- **C**: Both — governance config declares the framework; explicit invocation triggers it. `conversus run` doesn't auto-enforce, but CI workflows call `conversus governance`.

**Lean (pending user decision)**: **C**. Explicit invocation for the enforcement step, declarative config for the framework.

### Q2: Blocking vs advisory
Should the arbiter's governance check be **blocking** (merge fails on violation) or **advisory** (PR comment only, no block)?

**Possible answers:**
- **A**: Always blocking — BLOCK verdict → exit 1 → merge fails
- **B**: Always advisory — exit 0 regardless of verdict; only post comment
- **C**: Per-gate configurable — `gates.pr.blocking: true` vs `gates.pr.blocking: false`
- **D**: Per-rule configurable — each governance rule declares its severity (blocking/advisory/info)

**Lean (pending user decision)**: **D**. Governance rules are not uniform — a code style violation is different from a security violation. Let the rules themselves declare severity in the grounding documents, with a default of `blocking`.

### Q3: Self-contradictory governance
What's the failure mode when a constitution is ambiguous or self-contradictory?

**Possible answers:**
- **A**: Arbiter picks a side (weight + mtime tiebreak)
- **B**: Arbiter raises a META_DISPUTE verdict and escalates to human
- **C**: Arbiter runs a sub-deliberation with the contradiction as the target
- **D**: User pre-resolves all contradictions before enabling governance (tooling doesn't handle them)

**Lean (pending user decision)**: **B** for v1 (META_DISPUTE), with **C** as a v2 enhancement (sub-deliberation) for when the META_DISPUTE is itself escalated.

### Q4: Relationship to gate spec
Does this replace the existing gate spec (`specs/done/011-phase-consensus-gates/`) or extend it?

**Possible answers:**
- **A**: Replaces — gates become a sub-case of autonomous governance
- **B**: Extends — autonomous governance uses gates as the underlying mechanism
- **C**: Orthogonal — gates are for ad-hoc phase checkpoints, governance is for enforcement

**Lean (pending user decision)**: **B**. Autonomous governance USES gates. A `conversus governance --gate pr` invocation is literally running the `pr` gate with auto-grounding enabled. The gate spec provides the mechanism; this spec adds the declarative framework on top.

### Q5 (additional from the FP-guru's discussion style): Should autonomous mode support **dry-run with diff output**?
When users modify the governance config, can they preview the impact? e.g., "this change would have produced 3 additional violations on the last 10 PRs."

**Lean**: Yes. `conversus governance --replay --last 10` replays the autonomous mode over recent PRs and shows what would have changed. This is valuable for refining the constitution without breaking CI.

### Q6: Should commentary be tiered free/paid (ref spec 033)?
Governance itself is a quality-gate use case — core to the free tier. But commentary (spec 046) is more value-added. Should free tier get verdict-only, paid tier get commentary?

**Lean**: Governance core (verdict + rulings + exit codes) is free. Commentary (narrative PR comments, play-by-play) is paid. This matches spec 033's "deliberation is free, scoring is paid" principle — commentary is scoring-adjacent.

### Q7: Retention and archival
How long should `.conversus/runs/` retain autonomous run output? Should everything be archived to a persistent store?

**Lean**: `retention_days: 90` default. Failures (BLOCK verdicts) are auto-archived regardless of retention. Scheduled audits are auto-archived. Integration with scenario storage (spec 020) for long-term queries is a v2 feature.

### Q8: Multi-repo governance
Can a single governance config govern multiple repos (monorepo case)? Or does every repo need its own?

**Lean**: Each repo has its own `settings.json` governance key. Monorepos use directory-scoped configs (`apps/frontend/.conversus/settings.json` overrides the root via spec 050's cascade). Cross-repo governance is out of scope for v1.

### Q9: Governance for the governance
Who arbitrates changes to `CONSTITUTION.md` itself? The same arbiter that enforces it? That seems recursive.

**Lean**: Changes to grounding documents themselves go through a **meta-gate** with a different arbiter (e.g., `meta-arbiter` that reads the project's `META_CONSTITUTION.md` — a document about how to change the constitution). This is optional — if no meta-gate is configured, constitution changes are treated as normal edits. Note: `config set` write protection (FR-028) provides a weaker form of this for the config itself.

### Q10: Escape hatch
What if the arbiter is wrong? Can humans override?

**Lean**: Yes. `conversus governance --override --reason "..."` on the command line, or a signed comment on the PR (`/conversus override: reason`) — but every override is logged to an audit trail. Overrides are rate-limited and visible in compliance dashboards.

---

## 11. The "CLI that runs outside your CLI" Implication

This spec is about turning conversus into infrastructure, not a tool. The difference:

**Tool (current state):**
- User opens Claude Code
- User invokes `/conversus run`
- User reads output
- User decides action

**Infrastructure (this spec):**
- Developer pushes code
- CI auto-invokes `conversus governance`
- Arbiter rules against governance docs
- Merge blocked or proceeds automatically
- Humans see only exceptions (blocks or meta-disputes)

The core conversus engine is unchanged. What changes is the **surface** it runs on:

| Surface | Today | With Spec 048 |
|---------|-------|---------------|
| Claude Code | Primary | Secondary |
| CLI (interactive) | Primary | Secondary |
| CI (GitHub Actions) | Not supported | Primary |
| Git hooks | Not supported | Supported |
| Cron / scheduled | Not supported | Supported |
| Webhooks | Not supported | Supported (via execution providers) |
| IDE plugins | Not supported | Future (via spec 049 "Conversus as Universal Skill/MCP Server" — VSCode extension, Cursor rules, Zed extension; the Zed/JetBrains Agent Client Protocol is tracked separately as `zed-acp` in spec 042 §11 and is NOT the same as Google/IBM A2A) |

**Why this matters**: most quality-gate tools (mypy, pytest, ruff) live in CI because they're fast and objective. Conversus is slower (multi-agent deliberation takes minutes) but catches things mypy/pytest can't — architecture violations, security posture drift, governance breaches. The right place for it is as a **slow, thoughtful** CI check that runs asynchronously and produces narrative output humans can learn from.

---

## 12. Phasing

### Phase 1: Config format, parser, and deliberation blockers (~5 days)
- `settings.json` governance key schema definition (JSON Schema)
- Config loader with JSON Schema validation (FR-026)
- `read_settings()` fail-loud on corrupt JSON — raise `ConfigError`, not silent fallback (FR-025)
- `conversus init --governance` flag with auto-detection of grounding documents (FR-027)
- `config set` write protection for governance keys (FR-028)
- Backward-compat `.conversusrc` fallback with deprecation warning (§3.2)
- Schema documentation

### Phase 2: Auto-grounding arbiter extension (~2 days)
- Modify arbiter to auto-load grounding when in autonomous mode
- Weight-based conflict resolution
- META_DISPUTE verdict type

### Phase 3: `conversus governance` CLI subcommand (~3 days)
- Command dispatch, exit codes, structured output
- Target resolution (`{changed_files}`, globs, paths)
- Gate invocation
- Dry-run mode

### Phase 4: GitHub Actions integration (~2 days)
- Workflow template
- PR comment posting via `gh`
- Scheduled audit support

### Phase 5: Git hooks integration (~1 day)
- Pre-commit shim script
- Pre-push shim script
- Documentation

### Phase 6: Human-readable output + commentary integration (~2 days, requires spec 046)
- Markdown report format
- PR comment format with commentator output
- Compliance dashboard integration

### Phase 7: Advanced features (~ongoing)
- Override mechanism (Q10)
- Replay/preview (`--replay --last 10`)
- Multi-repo / directory-scoped configs
- Meta-gate for constitution changes

---

## 13. Non-Goals

- **Not a static analyzer**: conversus doesn't replace mypy, ruff, bandit. It runs alongside them for things they can't catch.
- **Not a replacement for human review**: governance mode is one signal. Humans still approve PRs.
- **Not a rubber stamp**: the arbiter must justify rulings with evidence from grounding documents. Unjustified rulings are bugs.
- **Not magic**: the quality of governance enforcement is bounded by the quality of the grounding documents. Vague constitutions produce vague rulings.
- **Not free for premium features**: commentary, advanced patterns, and compliance dashboards are paid tier per spec 033.

---

## 14. Relationship to Other Specs

- **Spec 001 (subject arbitration)**: This spec extends the arbiter from per-run configuration to persistent project-level configuration.
- **Spec 011 (phase consensus gates)**: This spec USES gates as the underlying enforcement mechanism; it adds the declarative framework (`settings.governance`) on top.
- **Spec 020 (scenario storage)**: Autonomous run output is a prime candidate for scenario storage. Cross-run governance queries ("how many times has rule X been violated?") require scenario queries.
- **Spec 033 (monetization partitioning)**: Governance core is free-tier; commentary and compliance dashboards are paid.
- **Spec 042 (execution providers)**: HARD DEPENDENCY. Autonomous mode cannot ship without headless execution support. Spec 042 shipped 12 execution providers organized by tier: **Tier 1 (native)**: `claude-code`, `anthropic`; **Tier 2 (subprocess)**: `aider`, `opencode`, `codex`, `copilot`; **Tier 3 (API-compat)**: `openai-compat`, `gemini`, `ollama`, `llama-cpp`, `vllm`; **Tier 4 (internal)**: `mock`, `pi`. The registered executor name for Claude Code is `claude-code` (direct `claude` CLI subprocess via `SubprocessProvider`).
- **Spec 043 (AMPL game solvers)**: Governance mode benefits from formal models when constitution rules can be expressed as optimization constraints (e.g., resource allocation governance).
- **Spec 050 (cascading settings)**: HARD DEPENDENCY. Governance config lives in `settings.json["governance"]` per spec 050's unified settings design. The 4-level cascade (default -> global -> project -> local) applies, but governance grounding documents use additive (union) merge — not replace — to prevent narrowing at lower cascade levels. This is the key merge semantics distinction. Cannot ship before 050's `SettingsResolver` supports per-namespace merge strategies.
- **Spec 046 (commentator agents)**: Commentary output is the natural format for PR comments on autonomous runs. Without commentary, PR comments are verdict-only; with commentary, they're narrative.
- **Spec 047 (duration parser)**: SLA rules in constitutions ("reviews within 24 hours") require structured duration parsing for arbiter arithmetic.

---

## 15. Vision Statement (from user)

> "I would like to gear conversus toward being a tool that runs outside of user interaction. It can be the CLI that runs outside of your CLI."

This spec is the concrete path to that vision. After shipping, conversus will run in:

- Every PR (pr gate)
- Every push to main (post-merge audit)
- Every night (scheduled audit)
- Every commit (pre-commit hook, optional)
- Every dependency update (webhook trigger)
- Every deployment (CI/CD pipeline)

And humans will interact with it only when:

- They're writing the constitution
- They're reviewing a BLOCK verdict
- They're resolving a META_DISPUTE
- They're using interactive `/conversus run` for ad-hoc deliberations

The overwhelming majority of conversus invocations will be autonomous. The CLI becomes infrastructure, not a tool.
