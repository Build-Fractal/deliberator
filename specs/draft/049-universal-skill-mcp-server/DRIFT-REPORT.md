# Drift Report — Spec 049: Universal Skill MCP Server

**Report date**: 2026-04-05
**Against commit**: current HEAD (main)
**Spec status**: Draft — not yet implemented in main branch

---

## Summary

Spec 049 was written 2026-04-05 against a provider landscape that has since grown significantly. The spec also predicts a spec 050 that doesn't match what spec 050 turned out to be. An experimental MCP server implementation exists in a Claude worktree (`agent-ab42d1e4/mcp_server.py`) that diverges substantially from the tool surface this spec defines. No MCP server code exists yet in the main codebase.

---

## Drift Vector 1: Provider count (HIGH)

### What the spec says

Two explicit claims in the spec:

- §2 architecture diagram (line 67): `ExecutionProvider protocol + 4 v1 providers + optional litellm`
- §13 (line 409): `mock + claude-code + anthropic + opencode + optional litellm providers`

### What exists in the codebase

`engine/execution/providers/__init__.py` registers **10 providers** at import time:

| Provider name | File | Type |
|---|---|---|
| `mock` | `mock.py` | Test/stub |
| `anthropic` | `anthropic.py` | Direct API |
| `claude-code` | `claude_code.py` | Subprocess runtime |
| `aider` | `aider.py` | Subprocess runtime |
| `opencode` | `opencode.py` | Subprocess runtime |
| `ollama` | `openai_compat.py` | Local inference (OpenAI-compat) |
| `llama-cpp` | `openai_compat.py` | Local inference (OpenAI-compat) |
| `vllm` | `openai_compat.py` | Local inference (OpenAI-compat) |
| `codex` | `codex.py` | Subprocess runtime |
| `copilot` | `copilot.py` | Subprocess runtime |
| `gemini` | `gemini.py` | Subprocess runtime |
| `pi` | `pi.py` | Subprocess runtime |

**12 total registrations** (10 files, `openai_compat.py` registers 3). No `litellm` provider exists — the `__init__.py` docstring mentions it as an "optional companion package" but nothing is shipped.

The CLI `--provider` choice list (both `run` and `decide` commands in `engine/cli/__init__.py`) already reflects the full 13-item list: `mock`, `anthropic`, `openai`, `claude-code`, `aider`, `opencode`, `ollama`, `llama-cpp`, `vllm`, `codex`, `copilot`, `gemini`, `pi`.

Note: `openai` appears in the CLI choice list but is NOT registered in `PROVIDER_REGISTRY` — it resolves via `resolve_provider()` separately. There is no `openai.py` provider file.

### Impact on spec 049

The spec's Layer 1 description is stale. The "4 v1 providers + optional litellm" framing no longer describes reality and should not drive MCP server implementation decisions. Specifically:

- §4.3 auth passthrough section mentions only `claude-code` and implicit API-key providers. The 6 subprocess providers (`aider`, `opencode`, `codex`, `copilot`, `gemini`, `pi`) and 3 local inference providers (`ollama`, `llama-cpp`, `vllm`) each have different auth/credential requirements that the MCP server needs to handle.
- §4.3's "API-key-less user story" would be correct for `mock`, `claude-code`, `ollama`, `llama-cpp`, and `vllm` — but incorrect for `anthropic`, `copilot`, `gemini`, `codex`, and `pi` which require credentials.
- The free-tier story in §13 (60-second zero-API-key install) remains valid for `mock` + `claude-code` path, but the provider diversity needs to be acknowledged.

---

## Drift Vector 2: Spec 050 subject mismatch (HIGH)

### What spec 049 says

Spec 049 references `spec 050` three times, always as "JetBrains plugin + Zed/JetBrains Agent Client Protocol":

- §2 diagram: `JetBrains plugin — future (tracked as 050)`
- §10 open question 8: "Lean: Separate spec (tracked as **spec 050** — JetBrains plugin + Zed/JetBrains Agent Client Protocol)"
- §12: "Spec 050 (JetBrains plugin + Zed/JetBrains ACP)"
- §11: "Not a JetBrains solution. JetBrains users are served by spec 050"

### What spec 050 actually is

`specs/050-cascading-settings/spec.md` — **Cascading Settings System** (2026-04-06). It defines a three-level settings cascade (`~/.conversus/settings.json` → `.conversus/settings.json` → `conversus.yml` → CLI flags), a `conversus config show/set` CLI, and migration of `.conversusrc` from spec 048.

There is no JetBrains plugin spec in existence. The dependency from spec 049 §12 ("Spec 050 (JetBrains plugin + Zed/JetBrains ACP)") is referencing a spec that doesn't exist under that number.

### Impact

- Cross-reference from §12 ("Relationship to Other Specs") is incorrect
- The JetBrains/Zed work has no assigned spec number yet
- Spec 050 (Cascading Settings) is actually a **direct dependency** of spec 049's MCP server: the MCP server needs to discover `default_provider` and project config from `.conversus/settings.json`. This relationship is entirely missing from the spec.

---

## Drift Vector 3: MCP tool surface vs. worktree implementation (HIGH)

### What spec 049 defines (§4.1)

12 tools total: 8 free-tier (`conversus_run`, `conversus_define`, `conversus_interests`, `conversus_mode`, `conversus_converge`, `conversus_arbitrate`, `conversus_gate`, `conversus_governance`) and 4 paid-tier (`conversus_score`, `conversus_solve`, `conversus_scenario_query`, `conversus_predict_convergence`).

### What the worktree implementation ships

The worktree `mcp_server.py` (in `.claude/worktrees/agent-ab42d1e4/`) implements **3 tools** with different names and semantics:

| Worktree tool | Spec 049 equivalent | Notes |
|---|---|---|
| `conversus_validate` | None — not in spec | New tool: validates YAML + classifies question + cost estimate |
| `conversus_run` | `conversus_run` | Different semantics: operates in 3 modes (validate-only, parse-results, in-process) |
| `conversus_decide` | None — not in spec | New tool: ad-hoc deliberation on natural language question |

The spec's `conversus_run` takes `config_path` (filesystem path). The worktree's `conversus_run` takes `config_yaml` (inline YAML string) — a fundamentally different input contract.

Spec tools with no worktree equivalent: `conversus_define`, `conversus_interests`, `conversus_mode`, `conversus_converge`, `conversus_arbitrate`, `conversus_gate`, `conversus_governance`, and all 4 paid-tier tools.

The worktree implementation also documents only `mock`, `anthropic`, `openai` as supported providers for in-process execution (line 508, 573) — contradicting the 12-provider registry.

### Impact

If the worktree is the implementation prototype, spec 049's tool taxonomy needs a complete revision before implementation begins. The "hybrid execution model" approach (validate-only / parse-results / in-process modes) in the worktree is a more practical design than the spec's one-tool-per-operation approach.

---

## Drift Vector 4: `conversus init` and project config discovery (MEDIUM)

### What the spec says

Spec 049 §4.3 says: "When the user installs `conversus-mcp-server`, they configure `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / etc. in their environment." The MCP server discovers project config implicitly.

### What now exists

`engine/project.py` (fully implemented) provides:
- `init_project()` — creates `.conversus/` directory + `settings.json` + per-runtime permission configs
- `find_conversus_dir()` — walks up the directory tree to find `.conversus/`
- `read_settings()` — reads `.conversus/settings.json`
- `AVAILABLE_RUNTIMES` — `["aider", "claude-code", "codex", "copilot", "gemini", "opencode"]`

`engine/cli/__init__.py` implements `conversus init` with `--runtime` choices restricted to those 6 runtimes (not the full 12 execution providers). The separation between "runtimes" (subprocess agents needing permission configs) and "providers" (all 12 registered execution providers) is not reflected in spec 049 at all.

The MCP server spec §4.3 says "no additional configuration" needed, but with the cascading settings system from spec 050 now defined, the MCP server should read `default_provider` from `.conversus/settings.json` to avoid requiring the provider to be specified per-tool-call. This is a new dependency that doesn't exist in the spec.

### Impact

The `conversus init` command now exists and shapes user workflow. Spec 049's APM promotion flow (§5) and standalone install path (§5.3) need to acknowledge that `conversus init` is the mechanism for setting up the project directory, and the MCP server should use `find_conversus_dir()` + `read_settings()` to resolve the default provider.

---

## Drift Vector 5: Spec 050 as unacknowledged dependency (MEDIUM)

### What the spec says

Spec 049 lists its dependencies as spec 042 (hard), spec 033 (free/paid boundary), and spec 048 (autonomous governance). Spec 050 is only referenced as a future "JetBrains plugin" — something spec 049 explicitly excludes.

### What actually needs to happen

Spec 050 (Cascading Settings) defines how `default_provider` and provider-specific model configs resolve across global, project, and per-invocation scopes. The MCP server:

1. Needs to discover the project's `default_provider` from `.conversus/settings.json` (spec 050 Level 2)
2. Should respect user-global defaults from `~/.conversus/settings.json` (spec 050 Level 1)
3. The `conversus_run` tool's `provider` parameter becomes optional when a project default is configured

Without spec 050 integration, every MCP tool call requires explicit provider specification, degrading UX. The spec's §4.3 "no additional configuration" promise only holds if the MCP server reads from the settings cascade.

Spec 050 §4 also updates `conversus init` as "a convenience wrapper" for creating the settings file — which affects how spec 049's §5 APM promotion flow generates the `.conversus/` directory.

---

## Drift Vector 6: `.conversusrc` governance config reference (LOW)

### What the spec says

Spec 049 §3.1 references "the current `.conversusrc` config (read-only)" in the VSCode extension Governance sub-view.

### What spec 050 says

Spec 050 §5 subsumes `.conversusrc` into `.conversus/settings.json` under a `"governance"` key, making `.conversusrc` a deprecated backward-compat format. The VSCode extension's Governance sub-view should read from `settings.json["governance"]`, not `.conversusrc`.

---

## Summary table

| # | Vector | Severity | Action needed |
|---|---|---|---|
| 1 | Provider count: "4 v1 providers" → actually 12 | HIGH | Update §2 diagram, §13 free-tier story; audit auth passthrough for all 12 providers |
| 2 | Spec 050 is Cascading Settings, not JetBrains plugin | HIGH | Fix all 4 references to spec 050; JetBrains needs a new spec number; add spec 050 as a dependency |
| 3 | Worktree `mcp_server.py` implements 3 tools with different names/contracts vs. spec's 12 | HIGH | Reconcile tool taxonomy before implementation; decide whether worktree approach supersedes spec §4.1 |
| 4 | `conversus init` + `engine/project.py` now exist; spec doesn't account for them | MEDIUM | Update §4.3 to reference `find_conversus_dir()` + `read_settings()`; update §5 APM flow |
| 5 | Spec 050 (Cascading Settings) is an undeclared dependency | MEDIUM | Add spec 050 as soft dependency; MCP server should read `default_provider` from settings cascade |
| 6 | `.conversusrc` referenced in VSCode extension; spec 050 deprecates it | LOW | Update §3.1 to reference `settings.json["governance"]` instead |
