# Feature Specification: Conversus as Universal Skill & MCP Server

**Feature ID**: `049-universal-skill-mcp-server`
**Created**: 2026-04-05
**Status**: Draft

**Partial-close note (2026-04-27 audit)**: MCP server core (FastMCP stdio,
3 of 5 v1 tools, env auth, no host-cred handling) shipped via PRs #11/#14/#18/#22
plus desktop-extension/.mcpb pipeline. Tier enforcement (FR-002/016-019)
superseded by spec 064 capability discovery. Cascading-settings dependency
fulfilled by spec 057 (closed). Residual vision in this spec: VSCode extension
(FR-007 through FR-012) and Cursor/APM compile targets (FR-013-015) — unstarted,
moved to draft until prioritized.

**Depends On**: `042-execution-providers` (Accepted — provider protocol must be stable before MCP server can expose `conversus_run` as a tool), `033-monetization-partitioning` (free/paid tier boundary), `050-cascading-settings` (MCP server needs `find_conversus_dir()` + `read_settings()` from spec 050 for project config discovery and `default_provider` resolution)
**Soft depends on**: `048-autonomous-governance-mode` (shares the "headless execution" use case; 048 is CI-first, 049 is IDE-first)

---

## 0. Decision Record

**Drift deliberation date**: 2026-04-07
**Deliberation agents**: mcp-architect, free-tier-analyst, vscode-implementer
**Drift report**: `DRIFT-REPORT.md` (6 drift vectors identified, 3 HIGH / 2 MEDIUM / 1 LOW)

**Key resolutions**:

1. **Provider count**: Updated from "4 v1 providers" to 12 v1 providers across three tiers (Direct SDK, Subprocess, HTTP/OpenAI-compat). The `litellm` optional companion is removed from the spec language — it was never shipped.
2. **Spec 050 cross-reference**: All references to "spec 050 — JetBrains plugin" corrected to "spec 050 — Cascading Settings". JetBrains/Zed ACP work assigned to spec 052 (unassigned). Spec 050 added as a hard dependency (MCP server reads `default_provider` from settings cascade).
3. **Tool taxonomy**: Reduced from 12 speculative tools to a phased rollout — 5 v1 tools (`conversus_run`, `conversus_decide`, `conversus_validate`, `conversus_init`, `conversus_status`), remaining tools documented as "Planned, demand-gated". Aligns spec with the worktree prototype's bottom-up approach.
4. **Free tier**: `mock` + `ollama` are both free-tier defaults. The "60-second zero-API-key install" story works with mock provider AND local ollama inference.
5. **Auth passthrough**: Expanded to cover all 12 providers' auth requirements by tier (no-auth local, session-auth subprocess, API-key providers).
6. **`conversus_decide` and `conversus_validate`**: Promoted to P1 MCP tools (unanimous across all three deliberation agents). `conversus_decide` is the strongest free-tier acquisition tool; `conversus_validate` subsumes the standalone cost-estimation use case.

**Docs Update**: New docs/user-guide/install-in-your-ide.md; new docs/developer-guide/mcp-server.md; new docs/developer-guide/vscode-extension.md
**Origin**: User directive (2026-04-05): "We are sleeping on VSCode." The post-042 roadmap initially treated VSCode as one of four equal hosts (Claude Code, Cursor, VSCode, Copilot). VSCode is actually the primary target after Claude Code — largest IDE user base, Microsoft-owned (same owner as GitHub which runs spec 048's CI gate), rich extension API, native MCP support in Copilot. Cursor, Windsurf, and other VSCode forks inherit anything we ship for VSCode.

---

## 1. Problem

Conversus today is available in two places:

1. **Claude Code**, via an APM-deployed skill (`.claude/skills/conversus/`). Works because Claude Code loads skills automatically from the workspace.
2. **The command line**, via `pip install conversus` + `conversus run`. Works for headless users.

That's the entire coverage matrix today. Users in VSCode, Cursor, Windsurf, JetBrains, Zed, Continue.dev, Copilot Chat, Cline, Roo Code, Augment, or any other IDE/agent tool cannot invoke conversus from inside their working environment. They have to:

1. Switch to a terminal, or
2. Install Claude Code just to get conversus, or
3. Not use conversus.

This is a **distribution problem**, not an architecture problem. Conversus the engine is already portable (spec 042 made the execution provider layer pluggable). What's missing is the packaging layer that installs conversus *as an invokable tool* into every host that matters.

The cost of the gap is enormous because the audiences that matter most for conversus — developers writing code, reviewing PRs, enforcing governance, running CI — live overwhelmingly in VSCode and its forks. Every hour conversus is not available in VSCode is an hour the "CLI that runs outside your CLI" vision (spec 048) doesn't reach its actual audience.

---

## 2. Solution: MCP Server + VSCode Extension + APM Promotion

Ship three coordinated artifacts that together give conversus universal reach:

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: Host-specific packaging (APM-compiled)                │
│  ─────────────────────────────────────                          │
│  • .claude/skills/conversus/         — already shipped          │
│  • .cursor/rules/conversus.md        — inherited from VSCode    │
│  • .vscode/extensions/conversus/     — NEW, primary UX          │
│  • .zed/extensions/conversus/        — future                   │
│  • JetBrains plugin                  — future (spec 052, unassigned) │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│  Layer 2: Conversus MCP Server (the universal substrate)        │
│  ───────────────────────────────────────────────                │
│  Exposes conversus as MCP tools (5 v1, others planned):         │
│  • conversus_run          — execute a deliberation      (v1)    │
│  • conversus_decide       — ad-hoc deliberation         (v1)    │
│  • conversus_validate     — config validation + cost    (v1)    │
│  • conversus_init         — project setup               (v1)    │
│  • conversus_status       — state + provider check      (v1)    │
│  • + 11 planned tools (demand-gated, see §4.1)                  │
│                                                                  │
│  Any MCP client can invoke: Copilot, Cline, Continue, Cursor,   │
│  Zed, Roo Code, Augment, custom clients.                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│  Layer 1: Conversus engine (spec 042 provider abstraction)      │
│  ──────────────────────────────────────────────────             │
│  ExecutionProvider protocol + 12 v1 providers:                  │
│  • Direct SDK: mock, anthropic                                  │
│  • Subprocess: claude-code, aider, opencode, codex, copilot,   │
│    gemini, pi                                                   │
│  • HTTP/OpenAI-compat: ollama, llama-cpp, vllm                  │
└─────────────────────────────────────────────────────────────────┘
```

**Why MCP is the correct substrate**:
- Every major VSCode-resident agent speaks MCP in 2026 (Copilot since late 2025, Cline, Continue, Roo Code, Augment, Cursor)
- MCP is a protocol, not a wrapper — one server implementation reaches every MCP-speaking client simultaneously
- MCP tool-use is unidirectional (host → conversus), which matches the "host invokes conversus" direction and avoids the bidirectional complexity that killed A2A in spec 042 (no counterparty ecosystem needed)
- Spec 042's ground-truth constraint "MCP is tools, not dispatch" applies inversely: here, conversus is the *tool*, and hosts dispatch TO it. This is the correct use of MCP.

**Why VSCode extension is NOT replaced by MCP**:
- MCP gives you *tool invocation* — Copilot can call `conversus_run` from inside a Copilot chat
- MCP does NOT give you *UI surface* — there's no MCP primitive for "render a sidebar view of phase progress" or "show arbitration resolution with clickable references"
- A VSCode extension is the right vehicle for the rich UX (sidebar panels, command palette, status bar, inline diagnostics)
- The two layers compose: Copilot users invoke `conversus_run` via MCP and watch the output in the VSCode extension sidebar

---

## 3. VSCode Extension Scope

The extension ships in v1 with four surfaces. Anything beyond these is out of scope and tracked as v2.

### 3.1 Sidebar view: "Conversus"

A persistent sidebar panel (activity bar icon) with three sub-views:

**Deliberations** — list of recent conversus runs with status (running, completed, failed, governance-blocked). Click a run to open the `summary/final.md` in the editor. Expanded view shows phase progress tree (Phase 1 → 2 → 3 → 4 → 5 → 6) with per-agent status indicators.

**Arbitration** — rendered view of `arbitration/resolution.md` with clickable grounding citations. When the arbiter cites "spec 042 §5", clicking jumps to that section in the editor. Makes arbiter rulings first-class navigable artifacts.

**Governance** — autonomous mode status. Shows the current governance config from `.conversus/settings.json["governance"]` (read-only; `.conversusrc` supported as deprecated fallback per spec 050 §5), pending PR gates, last governance ruling, and a "Run governance now" button that shells out to `conversus governance --gate pr` via the MCP server.

### 3.2 Command palette

Commands (all prefixed `Conversus:`):

- `Conversus: Run Deliberation` — opens a config picker (existing `conversus.yml` files in the workspace), runs the deliberation via MCP server, shows progress in sidebar
- `Conversus: Define Problem` — problem definition mode
- `Conversus: Run Governance Gate` — invokes `conversus governance` for the current changeset
- `Conversus: Show Last Arbitration` — jumps to the most recent `resolution.md` in the workspace
- `Conversus: Install as Skill` — invokes APM to install the conversus skill into the workspace's agent configs (so users in Claude Code inside VSCode inherit conversus automatically)

### 3.3 Status bar

Single status bar item showing:
- Autonomous mode state (`Governance: on` | `off` | `blocked` — the "blocked" state when a governance gate failed)
- Click to open the sidebar Governance view

### 3.4 Inline diagnostics

When a governance gate produces violations, file-scoped violations render as VSCode diagnostics (problems panel). Users see "spec 042 §5.1 violation: subprocess secrets in argv" as a red squiggle on the offending code line, with the arbiter's grounding citation in the hover popup. This is the "conversus in the feedback loop" moment — violations surface where the user is already looking.

### Out of v1 scope (tracked for v2)

- Multi-user collaboration / shared deliberation views
- Visual graph rendering of dispute DAGs
- Inline "start a deliberation about this selection" code actions
- Mermaid / sequence diagrams for deliberation flow
- Integration with VSCode's AI view (Copilot Chat panel) — covered by the MCP server path instead

---

## 4. MCP Server Interface

The MCP server is a Python package (`conversus-mcp-server`) that runs as a stdio or HTTP-based MCP server. It exposes conversus operations as MCP tools.

### 4.1 Tool surface

**v1 tools** (ship in Phase 1-2):

| Tool | Input schema | Output | Tier | Spec |
|---|---|---|---|---|
| `conversus_run` | `config_path` or `config_yaml` (inline YAML), `target`, `agents`, `provider` (optional — falls back to spec 050 settings cascade) | Path to output directory | **Free** | 033 (deliberation is free) |
| `conversus_decide` | `question` (natural language), `agents` (optional), `provider` (optional) | Deliberation output + `summary/final.md` | **Free** | — (ad-hoc deliberation on any question without a pre-authored config) |
| `conversus_validate` | `config_yaml` (inline YAML) | Structured validation result: YAML validity, question classification, `cost_estimate` with `paid_tier_additions` field | **Free** | — (subsumes standalone cost-estimation use case) |
| `conversus_init` | `runtime` (optional), `provider` (optional) | Creates `.conversus/` directory + `settings.json` | **Free** | 050 (cascading settings) |
| `conversus_status` | `output_path` (optional) | Current deliberation state, recent runs, provider availability | **Free** | — |

**Planned tools** (demand-gated — promoted to v1 when usage data justifies):

| Tool | Input schema | Output | Tier | Spec | Gate |
|---|---|---|---|---|---|
| `conversus_define` | `description` (free text) | Problem definition markdown | **Free** | 006 (problem definition) | Low demand signal — `conversus_decide` covers most ad-hoc use cases |
| `conversus_interests` | `options` | Interest discovery markdown | **Free** | — | Evaluate after v1 adoption metrics |
| `conversus_mode` | `target`, `options` | Mode recommendation | **Free** | — | Evaluate after v1 adoption metrics |
| `conversus_converge` | `config_path` | Run status + output path | **Free** | — | Evaluate after v1 adoption metrics |
| `conversus_arbitrate` | `path` to output dir | Arbitration resolution | **Free** | 001 (subject arbitration) | Evaluate after v1 adoption metrics |
| `conversus_gate` | `phase`, `artifact` | Gate decision | **Free** | 011 (phase consensus gates) | Evaluate after v1 adoption metrics |
| `conversus_governance` | `gate_name`, `target` | Verdict (PASS/BLOCK/ERROR) + resolution | **Free** | 048 | Promote when spec 048 adoption warrants |
| `conversus_score` | `deliberation_output_path` | Equilibrium scores, convergence metrics | **Paid** | 033 (scoring is paid) | Promote with `conversus-solvers` package |
| `conversus_solve` | `scenario`, `model` | AMPL solver output | **Paid** | 043 (AMPL solvers) | Promote with `conversus-solvers` package |
| `conversus_scenario_query` | `query`, `filters` | Scenario storage query results | **Paid** | 020 (scenarios) | Promote with `conversus-solvers` package |
| `conversus_predict_convergence` | `deliberation_config` | Convergence prediction | **Paid** | 034 (Kalman) | Promote with `conversus-solvers` package |

### 4.2 Free vs paid gating

Per user directive (2026-04-05) and spec 033:
- **All 5 v1 tools are free**: `conversus_run`, `conversus_decide`, `conversus_validate`, `conversus_init`, `conversus_status` — running a deliberation, deciding, validating configs, initializing projects, and checking status are all in the "free tier" of spec 033
- **Planned free-tier tools** (demand-gated): `conversus_define`, `conversus_interests`, `conversus_mode`, `conversus_converge`, `conversus_arbitrate`, `conversus_gate`, `conversus_governance` — these are free but not shipped in v1; promoted when usage data justifies
- **Planned paid-tier tools**: `conversus_score`, `conversus_solve`, `conversus_scenario_query`, `conversus_predict_convergence` — anything that invokes heuristic payoffs, equilibrium scoring, AMPL solvers, convergence prediction, scenario storage queries, config optimization, nashopt

The MCP server enforces tier gating at tool-call time:
- v1 tools succeed with any install
- Planned free-tier tools return a structured info response: `{"code": "TOOL_PLANNED", "message": "This tool is planned for a future release. Use conversus_run or conversus_decide instead.", "alternatives": [...]}`
- Planned paid-tier tools check for `conversus-solvers` (or equivalent paid package) in the Python environment
- Paid tool call without paid package returns a structured MCP error: `{"code": "PAID_TIER_REQUIRED", "message": "This tool requires conversus-solvers. Install via: pip install conversus-solvers", "tier": "paid", "paid_tier_additions": "equilibrium scoring, AMPL solvers, convergence prediction, scenario queries"}`

Hosts display these responses naturally in their UI (Copilot shows it in chat, the VSCode extension shows it as a notification with a "Learn more" link to the docs).

### 4.3 Authentication passthrough

The MCP server itself is unauthenticated — it runs in the user's local environment and inherits their credentials. It does NOT manage auth for upstream LLM providers. Instead, each provider tier has different auth requirements:

**No auth required (local/free)**:
| Provider | Auth mechanism | Notes |
|---|---|---|
| `mock` | None | Test/stub provider — no LLM calls |
| `ollama` | None | Local inference server, no API key |
| `llama-cpp` | None | Local inference server, no API key |
| `vllm` | None | Local inference server, no API key |

**Session/binary auth (no explicit API key)**:
| Provider | Auth mechanism | Notes |
|---|---|---|
| `claude-code` | Local `claude` binary session | Inherits the user's existing Claude Code login; the free-tier "API-key-less user story" from spec 042 §2.3 |
| `copilot` | `gh auth` session | Requires GitHub CLI authentication (`gh auth login`); inherits existing session |

**API key required (environment variables)**:
| Provider | Required env var(s) | Notes |
|---|---|---|
| `anthropic` | `ANTHROPIC_API_KEY` | Direct Anthropic API access |
| `codex` | `OPENAI_API_KEY` | OpenAI Codex subprocess |
| `gemini` | `GOOGLE_API_KEY` | Google Gemini subprocess |
| `pi` | `INFLECTION_API_KEY` | Inflection Pi subprocess |
| `aider` | Varies — `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or other provider key depending on aider's configured backend | Aider supports multiple LLM backends; the user configures which key aider uses |
| `opencode` | Varies — same multi-provider pattern as aider | OpenCode inherits the user's configured LLM backend |

When a host calls `conversus_run`, the server spawns a conversus process that inherits those env vars. The MCP server resolves the active provider via the spec 050 settings cascade (`~/.conversus/settings.json` → `.conversus/settings.json` → `conversus.yml` → explicit `provider` parameter), so users who have configured a `default_provider` in their project settings do not need to specify it per-tool-call.

The MCP server never sees host-side credentials (Copilot's API key, VSCode's GitHub token). Host-side auth is the host's concern.

### 4.4 Transport

v1 ships stdio-based MCP (the default for most hosts). HTTP-based MCP transport is v2 work.

The server is installable via pip: `pip install conversus-mcp-server`. After install, users configure their host to launch it:

```json
// Claude Code, Cursor, Copilot, Cline, etc. all use similar MCP config formats
{
  "mcpServers": {
    "conversus": {
      "command": "conversus-mcp-server",
      "args": [],
      "env": {}
    }
  }
}
```

---

## 5. APM Promotion Flow

APM is already set up for cross-host artifact distribution (Claude/Copilot/Cursor per the APM setup memory). Spec 049 extends this to the new targets.

### 5.1 Single source, multiple targets

The canonical conversus artifacts live in the conversus repo's `.apm/` subtree:

```
conversus/
├── .apm/
│   ├── skills/conversus/          # Base skill (Claude Code native format)
│   ├── prompts/                   # Shared prompts
│   ├── instructions/              # Shared instructions
│   └── mcp/conversus-server.yml   # MCP server manifest
```

APM's `compile` step generates host-specific output from this single source:

| Source | Target | Format |
|---|---|---|
| `.apm/skills/conversus/` | `.claude/skills/conversus/` | Claude Code skill (already works) |
| `.apm/skills/conversus/` | `.cursor/rules/conversus.md` | Cursor rule (APM cross-compile) |
| `.apm/skills/conversus/` + `.apm/mcp/conversus-server.yml` | `.vscode/extensions/conversus-vscode/` | VSCode extension scaffold + MCP bridge config |
| `.apm/mcp/conversus-server.yml` | All MCP-speaking hosts | MCP server registration |

### 5.2 The monorepo inheritance path

The payer-index-mono repo uses APM with the monorepo as an org package — submodules inherit from the root. Conversus lives as a submodule. When a user clones the monorepo and runs `apm install`:

1. APM reads the monorepo's `apm.yml`
2. Resolves the conversus submodule's `.apm/` artifacts
3. Compiles them for the host(s) installed in that workspace (detected by presence of `.claude/`, `.cursor/`, `.vscode/`, etc.)
4. Deploys to each host's expected path

The user's IDE instantly has conversus available in whatever form the host supports. This is the "zero config, any IDE" UX.

### 5.3 Standalone install path (no monorepo)

For users who don't work in the monorepo:

```bash
pip install conversus conversus-mcp-server
apm install conversus  # registers conversus artifacts globally, host auto-detected
```

APM handles the host-specific install (VSCode extension from marketplace, MCP server config file, Claude Code skill directory, etc.).

---

## 6. Functional Requirements

### MCP Server

- **FR-001**: `conversus-mcp-server` MUST expose the 5 v1 tools listed in §4.1 (`conversus_run`, `conversus_decide`, `conversus_validate`, `conversus_init`, `conversus_status`) without requiring any paid package. Planned tools are promoted to v1 when usage data justifies.
- **FR-002**: Paid-tier planned tools MUST return a structured `PAID_TIER_REQUIRED` error when invoked without the paid package installed.
- **FR-003**: The server MUST be installable via `pip install conversus-mcp-server` and run as a standalone stdio MCP server.
- **FR-004**: The server MUST inherit user environment variables for LLM provider auth (ANTHROPIC_API_KEY, etc.) without additional configuration.
- **FR-005**: The server MUST NOT request or store host-side credentials (Copilot tokens, GitHub tokens, etc.).
- **FR-006**: Tool outputs MUST include a stable output path that the host can render in its UI (sidebar, chat, etc.).

### VSCode Extension

- **FR-007**: The extension MUST install from the VSCode Marketplace as `conversus.conversus-vscode`.
- **FR-008**: The extension MUST provide a sidebar view with Deliberations, Arbitration, and Governance sub-views (§3.1).
- **FR-009**: The extension MUST register the command palette entries listed in §3.2.
- **FR-010**: The extension MUST render governance violations as VSCode diagnostics (Problems panel) with clickable grounding citations.
- **FR-011**: The extension MUST communicate with conversus via the MCP server (not a custom protocol).
- **FR-012**: The extension MUST work in VSCode, Cursor, Windsurf, and any VSCode fork that supports extensions.

### APM Integration

- **FR-013**: APM's `compile` step MUST generate host-specific artifacts from the single conversus `.apm/` source tree.
- **FR-014**: APM MUST auto-detect the host(s) in the workspace and install only the relevant artifacts.
- **FR-015**: APM's monorepo inheritance flow MUST work unchanged — submodule conversus artifacts propagate to the root.

### Tier Enforcement

- **FR-016**: Free-tier tools MUST succeed without any paid package installed.
- **FR-017**: Paid-tier tools MUST detect paid package presence at invocation time, not at server startup.
- **FR-018**: Paid-tier errors MUST be structured and machine-readable (MCP error codes), not string-parsed.
- **FR-019**: Users MUST be able to upgrade from free to paid without reinstalling or reconfiguring the MCP server — the server picks up the paid package on its next invocation.

### Documentation

- **FR-020**: `docs/user-guide/install-in-your-ide.md` MUST provide host-specific install instructions for VSCode, Cursor, Copilot, Cline, Claude Code, and Zed.
- **FR-021**: Each host section MUST include a screenshot (or equivalent visual) of conversus successfully invoked from that host.

---

## 7. Success Criteria

- **SC-001**: A VSCode user installs the conversus extension from the marketplace and successfully runs a deliberation without leaving VSCode.
- **SC-002**: A Copilot user (in VSCode) configures the conversus MCP server and asks Copilot to "run a conversus deliberation on this spec" — Copilot invokes `conversus_run` and the deliberation completes.
- **SC-003**: A Cursor user installs the same VSCode extension (Cursor inherits it) and gets the same experience.
- **SC-004**: A Cline user configures the conversus MCP server and Cline can invoke all 5 v1 tools.
- **SC-005**: A free-tier user invokes `conversus_score` and receives a clear `PAID_TIER_REQUIRED` error with upgrade instructions.
- **SC-006**: A paid-tier user (with `conversus-solvers` installed) invokes `conversus_score` and receives structured scoring output.
- **SC-007**: A user clones the monorepo, runs `apm install`, and has conversus available in whichever IDE they open the workspace with — zero additional config.
- **SC-008**: An autonomous governance gate (spec 048) running in GitHub Actions can invoke the MCP server's `conversus_governance` tool headlessly (no interactive host needed).
- **SC-009**: A governance violation surfaces in the VSCode extension's Problems panel with a clickable link to the grounding document.

---

## 8. Constraints

- **Spec 042 is the hard dependency**: the MCP server cannot stabilize until the execution provider protocol is stable. Spec 042 Phase 1 (protocol shape) must land before MCP server Phase 1 starts.
- **Spec 033 boundary is non-negotiable**: deliberation is free, scoring/solvers/scenarios are paid. The MCP server enforces this per-tool, not per-install. Users with only the free tier see all 5 v1 tools; paid planned tools appear (succeed) only when the paid package is present. Additional free-tier tools are promoted from "Planned" status based on demand signals.
- **VSCode extension must use MCP, not a custom protocol**: if the extension shipped a custom IPC layer to conversus, every other host would need one too. Using MCP is the "one implementation reaches every host" guarantee.
- **APM is the canonical distribution mechanism**: we do NOT ship per-host wrappers by hand. Every host artifact is generated by APM from the single `.apm/` source tree. This avoids drift.
- **Host credentials are the host's problem**: conversus never requests, stores, or forwards host-side credentials. If Copilot calls `conversus_run`, Copilot's auth to its own backend is Copilot's concern.
- **No bundled LLM credentials**: the MCP server ships with zero bundled API keys. Users provide their own. Four providers require no API key at all (`mock`, `ollama`, `llama-cpp`, `vllm`), two use session auth (`claude-code`, `copilot`), and six require explicit API keys (see §4.3).
- **Backward compatibility**: existing Claude Code skill install path (the APM `.claude/skills/conversus/` deployment) MUST continue to work unchanged. Spec 049 is additive.

---

## 9. Phasing

Phasing is coordinated with spec 042 so the MCP server and VSCode extension ship in the same sprint window as 042.

### Phase 1: MCP server skeleton (concurrent with 042 Phase 1-2, ~1 week)
- `conversus-mcp-server` package scaffold
- Stdio MCP transport
- 3 v1 tools as smoke tests: `conversus_run`, `conversus_decide`, `conversus_validate`
- Tested against Claude Code as the first MCP client

### Phase 2: Full v1 tool surface (concurrent with 042 Phase 3, ~1 week)
- All 5 v1 tools implemented (`conversus_run`, `conversus_decide`, `conversus_validate`, `conversus_init`, `conversus_status`)
- Auth passthrough via environment for all 12 providers (§4.3)
- Spec 050 settings cascade integration (`find_conversus_dir()` + `read_settings()`)
- Planned tools documented as stubs returning tool descriptions + promotion criteria
- Paid planned tools return `PAID_TIER_REQUIRED` with structured error
- Tier-detection logic (import `conversus_solvers`, catch ImportError)

### Phase 3: VSCode extension v0.1 (concurrent with 042 Phase 4, ~1.5 weeks)
- Extension scaffold + MCP client wiring
- Sidebar view with Deliberations sub-view only
- Command palette: `Conversus: Run Deliberation`
- Basic status bar item

### Phase 4: VSCode extension v1.0 (concurrent with 042 Phase 5, ~1 week)
- Arbitration sub-view with clickable grounding citations
- Governance sub-view + diagnostics integration
- Full command palette
- VSCode Marketplace submission

### Phase 5: APM cross-compile (~3 days)
- APM targets: `.cursor/rules/`, `.vscode/extensions/`, existing `.claude/skills/` unchanged
- Monorepo inheritance validation
- Standalone install path via `apm install conversus`

### Phase 6: Paid-tier integration (~1 week)
- Paid tools wired through to `conversus-solvers` package
- Error surfaces tested in all hosts (Copilot, Cline, VSCode extension, Cursor)
- Documentation of upgrade path

**Total timeline**: Phases 1-5 ship in the same sprint as spec 042 (6 weeks). Phase 6 ships within 1-2 weeks after.

---

## 10. Open Questions

1. **Should the VSCode extension bundle the MCP server binary?** Pro: one-install experience. Con: tight coupling, harder to update independently.
   - **Lean**: No. Extension declares `conversus-mcp-server` as a Python dependency in the extension's docs; installs via `pip` or auto-prompt. Extension talks to the server via MCP stdio.

2. **Should the VSCode extension work without the MCP server?** I.e., can users install just the extension and get a "browse past deliberations" read-only view?
   - **Lean**: Yes, read-only mode. The Arbitration and Deliberations sub-views can render any `resolution.md` / `final.md` found in the workspace without needing an active MCP server. "Run deliberation" and "Run governance" commands are disabled when the MCP server is not running.

3. **Should the MCP server expose conversus templates as MCP resources?** MCP has a `resources` primitive separate from `tools`. Exposing the conversus templates as resources would let hosts browse them.
   - **Lean**: Yes, v1. Templates are static files, zero cost to expose, lets host UIs render available modes.

4. **Which MCP version do we target?** MCP has multiple spec versions in 2026.
   - **Lean**: Target the current stable MCP spec version at spec 049 implementation time (check at Phase 1 start). Pin to that version for v1.

5. **Should conversus-mcp-server live in the main conversus repo or a separate repo?**
   - **Lean**: Same repo, separate package (`conversus-mcp-server`). Shared release cycle with conversus core. Same monorepo benefits as spec 032's package split.

6. **VSCode extension: TypeScript or Rust (extension API supports both now)?**
   - **Lean**: TypeScript. Standard VSCode extension language, faster iteration, better ecosystem for UI work. Rust is over-engineering for a UI extension.

7. **Should the extension submit deliberation output to a cloud backend for shared team views?**
   - **Lean**: Out of v1 scope. This is a future paid-tier feature (team collaboration). Local-only in v1.

8. **JetBrains plugin: separate spec or bundled here?**
   - **Lean**: Separate spec (tracked as **spec 052 — JetBrains/Zed Agent Client Protocol**, unassigned). Spec 049 is VSCode-first; JetBrains is a different protocol stack (JetBrains uses the Agent Client Protocol for IDE-to-agent integration, which is different from MCP) and deserves its own spec and timeline. Note: spec 050 turned out to be Cascading Settings, not JetBrains — see §0 Decision Record.

---

## 11. Non-Goals

- **Not a replacement for the standalone CLI.** `conversus run` on the command line continues to work and remains the primary path for CI/scripting.
- **Not a cloud service.** The MCP server runs locally. No hosted endpoint in v1.
- **Not a collaboration tool.** Single-user, local deliberation only. Team views are out of scope.
- **Not a model marketplace.** The MCP server uses whatever providers spec 042 ships. No provider selection UI in v1.
- **Not a replacement for spec 040 Command Center.** Spec 040 remains a separate workstream. The VSCode extension and the Command Center overlap in features but serve different audiences (developers-in-IDE vs non-technical stakeholders-in-dashboard). They may converge in v2, tracked separately.
- **Not a JetBrains solution.** JetBrains users are served by spec 052 — JetBrains/Zed Agent Client Protocol (unassigned), not spec 049.

---

## 12. Relationship to Other Specs

- **Spec 042 (execution providers)**: HARD DEPENDENCY. MCP server exposes conversus operations that all flow through the ExecutionProvider protocol. Spec 042 Phase 1 must ship before 049 Phase 1 starts.
- **Spec 033 (monetization partitioning)**: Spec 049's MCP tool taxonomy IS the free/paid boundary at the tool-call level. Each tool is tagged free or paid, and the server enforces gating per-invocation.
- **Spec 048 (autonomous governance)**: Spec 049 provides the IDE-side rendering for spec 048's governance rulings. A governance violation detected by spec 048 becomes a VSCode diagnostic via spec 049.
- **Spec 040 (Command Center)**: Adjacent, not overlapping. Command Center is the non-technical stakeholder dashboard. Spec 049 is the developer-in-IDE surface. Both may converge in v2.
- **Spec 046 (commentator agents)**: Commentary output from spec 046 is a natural fit for the VSCode extension's Arbitration sub-view. The extension can render commentary alongside the arbiter's ruling.
- **Spec 050 (Cascading Settings)**: HARD DEPENDENCY. The MCP server uses `find_conversus_dir()` + `read_settings()` from spec 050 to resolve `default_provider` and project config from the three-level settings cascade (`~/.conversus/settings.json` → `.conversus/settings.json` → `conversus.yml` → CLI flags). Without spec 050, every MCP tool call requires explicit `provider` specification, degrading UX. The `conversus_init` tool is a thin wrapper around spec 050's project initialization.
- **Spec 052 (JetBrains/Zed Agent Client Protocol)**: Separate future spec (unassigned). Tracks the JetBrains-specific protocol stack (Agent Client Protocol, not MCP). Out of 049 scope.

---

## 13. Impact on the Free Tier

Spec 049 changes the free-tier value proposition materially:

**Before spec 049**: "Install conversus if you use Claude Code, or run it from the command line."
**After spec 049**: "Install conversus in any IDE — VSCode, Cursor, Windsurf, Copilot, Cline, Continue, Roo Code, Augment, Claude Code — and invoke deliberations without leaving your editor."

This is a user-acquisition step-change. The free tier becomes genuinely universal, not "universal for people who use the right tools." Combined with spec 042's free-tier architecture (12 v1 providers across three tiers), two providers serve as **free-tier defaults**:

- **`mock`** — zero-cost test/stub provider, always available, no external dependencies. Lets users validate configs, explore the tool surface, and run dry-run deliberations without any LLM.
- **`ollama`** — local inference via Ollama. Users with `ollama` installed get real LLM-powered deliberations with zero API keys and zero cost. This is the strongest free-tier acquisition path for users who want substantive output without signing up for anything.

The "60-second zero-API-key install" story works with both paths: **`pip install conversus conversus-mcp-server` + configure MCP in your IDE = deliberation working in 60 seconds.** With `mock`, users get immediate structural validation. With `ollama` running locally, users get full LLM-powered deliberations. With `claude-code` (existing Claude Code session), users get Anthropic-quality output through their existing login. No API key configuration required for any of these three paths.

That user story is the missing piece of the spec 033 free-tier promise.
