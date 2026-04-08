# Feature Specification: Execution Provider Abstraction

**Feature ID**: `042-execution-providers`
**Created**: 2026-04-02
**Status**: Accepted (2026-04-05, winner-take-all conversus deliberation, binding arbitration)
**Depends On**: `032-package-splitting` (soft — the abstraction works pre-split, but pip-installable packages make provider plugins practical)
**Docs Update**: New docs/developer-guide/execution-providers.md; update docs/developer-guide/architecture.md with provider layer diagram; update docs/user-guide/config-reference.md with `executor:` field
**Origin**: Blog generation use case revealed that conversus is hard-coded to Claude Code's Agent tool. Every phase prompt is the same regardless of executor — only the dispatch mechanism differs.
**Protocol Alignment**: Conversus owns the `ExecutionProvider` protocol. A2A (Google/IBM, Linux Foundation, JSON-RPC over HTTP) is tracked as a forward-compatible dispatch protocol but not a v1 deliverable — the A2A coding-agent ecosystem is empty as of 2026-04. See Decision Record (§0) for the ruling. **Do not conflate A2A with the Zed/JetBrains Agent Client Protocol** (stdio, IDE-to-agent) — these are different protocols with different scopes.

---

## 0. Decision Record

**Deliberation**: 4-agent winner-take-all conversus run, 2026-04-03 to 2026-04-05
**Winner**: `build-our-own-advocate` (conversus-owned protocol + 8 v1 providers + optional companion package)
**Runner-up**: `litellm-hybrid-advocate`
**Arbiter ruling**: Affirm with 14 binding conditions (see §13)
**Validation battery**: [`validation.md`](validation.md) — 28 acceptance tests
**Artifacts**: [`conversus-output/summary/final.md`](conversus-output/summary/final.md) (judge verdict), [`conversus-output/arbitration/resolution.md`](conversus-output/arbitration/resolution.md) (binding arbitration)

### Ruling Summary

1. **Protocol ownership**: `ExecutionProvider` is conversus-owned. No external library covers both agent runtimes and model APIs under one abstraction.
2. **v1 provider set** (8 providers across 3 tiers): Direct SDK — `mock`, `anthropic` (native); Subprocess — `claude-code` (direct `claude` CLI, **no** `claude-agent-sdk` dependency), `aider`, `opencode`; HTTP/OpenAI-compatible — `ollama`, `llama-cpp`, `vllm`.
3. **Base classes**: `SubprocessProvider` and `HTTPProvider` factored from research findings — shared lifecycle for subprocess-based and HTTP-based providers.
4. **Optional companion**: `LiteLLMProvider` ships as opt-in Tier-3 package alongside native `AnthropicProvider` (the 300-line redundancy is enterprise resilience, not waste — see resolution.md §5).
5. **`acp` row renamed to `a2a`** throughout the matrix. Separate `zed-acp` row for the Zed/JetBrains IDE protocol (different scope, explicitly out of v1).
6. **A2A is deferred**, not cancelled. A `conversus-a2a-claude` standalone wrapper ships as a **post-v1 pioneer artifact** when the A2A coding-agent ecosystem develops counterparties.
7. **Protocol shape is A2A-friendly from Week 1**: `ExecutionTask` and `ExecutionResult` designed with structured `parts`/`references`/`metadata`/streaming-compatible fields, but with a `from_prompt()` compatibility constructor so subprocess/direct-API providers remain flat. ~4 hours of design cost, avoids a rewrite in Phase 3.
8. **Spec 048 discovery gap addressed**: `.conversusrc::default_agents` schema accepts URL entries from day 1, with a "not yet supported" error in v1. Future A2A activation becomes a config change, not a schema migration.

### Ground-Truth Constraints (from backbone-researcher, ratified by all advocates)

These findings are binding on all implementation decisions below. Any code that contradicts them is wrong on the merits:

- **Claude Agent SDK is itself a CLI subprocess wrapper.** The `claude-code` provider MUST use subprocess of the `claude` CLI binary directly.
- **No shipping coding agent has been wrapped as an A2A server as of 2026-04.** If v1 promises an `a2a` provider, it must name the specific counterparty. "A2A provider" without a named counterparty is a false promise.
- **MCP is tools, not dispatch.** Agents USE MCP tools during execution; the provider layer DOES NOT USE MCP to dispatch to other agents.
- **No unifying library exists** that handles both agent runtimes and model APIs under one abstraction. Protocol must be conversus-owned.
- **Subprocess cold start (1-3s per invocation) × N phases is real.** The protocol MUST expose a pooling hook or document the cost explicitly.

### 14 Binding Conditions

Full list in §13. These are non-negotiable for Phase 1-6 implementation.

---

## 1. Problem

Conversus orchestration is currently coupled to a single execution environment: the Claude Code SKILL.md running inside an interactive Claude Code session. This means:

- **No CI/CD**: You can't run a conversus deliberation in a GitHub Action without a human in the loop
- **No SDK choice**: Users locked into Claude Code even if they prefer Copilot, Gemini CLI, or OpenCode
- **No programmatic API**: The Python SDK (`engine/sdk.py`) uses `ModelProvider` for raw completions but has no way to dispatch agentic tasks with tool use (file read/write, search, etc.)
- **No workflow integration**: LangGraph, GitHub Agentic Workflows (gh-aw), and other orchestrators can't plug into conversus phases
- **Blog generation pipeline**: Can't build automated content pipelines that read conversus output and generate blog posts without manual SKILL.md invocation

The engine's phase templates and variable contracts are already provider-agnostic — they're just markdown with `{VARIABLE}` placeholders. The coupling is in the dispatch layer, not the protocol.

---

## 2. Architecture

### Protocol Stack

Three complementary protocols serve different layers of the agentic stack. Conversus uses all three:

```
┌──────────────────────────────────────────────────────────────┐
│  Conversus Engine (orchestration protocol)                   │
│  - Phase sequencing (1-6), templates, dispute parsing        │
│  - Round management, stagnation detection                    │
│  - Output path management                                    │
└──────────────────┬───────────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │  ACP / A2A Layer  │  Agent Communication Protocol
         │  (task dispatch)  │  - Task Request envelope
         │                   │  - Agent discovery (Agent Detail)
         │                   │  - Async streaming results
         └────────┬──────────┘
                  │
    ┌─────────────┼─────────────────────────────────┐
    │             │                                  │
    ▼             ▼                                  ▼
┌─────────┐ ┌──────────┐ ┌───────────┐ ┌──────────────────┐
│ Agentic │ │ Workflow  │ │ Model API │ │ IDE Agent        │
│ SDKs    │ │ Engines   │ │ (direct)  │ │ (JetBrains ACP)  │
├─────────┤ ├──────────┤ ├───────────┤ ├──────────────────┤
│ Claude  │ │ gh-aw    │ │ Anthropic │ │ JetBrains Junie  │
│ Copilot │ │ LangGraph│ │ OpenAI    │ │ Zed              │
│ Gemini  │ │ GSD      │ │ Gemini    │ │                  │
│ OpenCode│ │ Temporal │ │ Mock      │ │                  │
└────┬────┘ └────┬─────┘ └─────┬─────┘ └───────┬──────────┘
     │           │              │                │
     └───────────┴──────┬───────┘                │
                        │                        │
                   ┌────┴────┐              ┌────┴────┐
                   │  MCP    │              │  MCP    │
                   │ (tools) │              │ (tools) │
                   └─────────┘              └─────────┘
```

**ACP (Agent Communication Protocol)** — IBM/Linux Foundation, merged with Google A2A (2025):
- Standardizes how agents discover each other and dispatch work
- REST-based, MIME multipart messages, async with streaming
- Agents expose ACP server endpoints; clients (like conversus) send Task Requests
- No specialized libraries required — standard HTTP

**MCP (Model Context Protocol)** — Anthropic:
- Standardizes how models invoke tools (read files, search, etc.)
- Already in use — Claude Code tools are MCP
- Agents use MCP internally to interact with their environment

**JetBrains ACP (Agent Client Protocol)** — different from IBM ACP:
- Standardizes IDE-to-coding-agent integration (like LSP for agents)
- Relevant for conversus agents that modify code

### ACP Mapping to Conversus Phases

A conversus phase dispatch maps directly to an ACP Task Request:

| Conversus Concept | ACP Concept |
|-------------------|-------------|
| Phase agent prompt (filled template) | Task Request message (text/markdown part) |
| `read_paths` (files agent must read) | Task Request message (reference parts) |
| `output_path` (where agent writes) | Task Request metadata (output expectation) |
| Phase metadata (phase, mode, round) | Task Request metadata (custom fields) |
| Background agent execution | Async task with streaming |
| Agent completion notification | Task status update / completion event |
| `execute_batch()` (parallel agents) | Multiple concurrent Task Requests |

### The Engine Already Doesn't Care

Today the SKILL.md builds a prompt string and calls `Agent(prompt=..., run_in_background=True)`. The agent receives:
1. A natural-language prompt (the filled template)
2. Implicit file system access (read targets, write output)

This is already a clean interface. ACP formalizes the wire protocol; the `ExecutionProvider` is a Python adapter between the conversus engine and ACP (or non-ACP providers that don't speak the protocol yet).

---

## 3. ExecutionProvider Protocol

```python
from __future__ import annotations
from typing import Protocol, runtime_checkable

@runtime_checkable
class ExecutionProvider(Protocol):
    """Interface for executing a single conversus agent task.

    A task is: read these files, follow this prompt, write output to this path.
    The provider handles HOW (SDK, subprocess, API call, workflow dispatch).
    The engine handles WHAT (which phase, which template, which variables).
    """

    async def execute(
        self,
        prompt: str,
        output_path: str,
        read_paths: list[str] | None = None,
        metadata: dict | None = None,
    ) -> ExecutionResult:
        """Execute a single agent task.

        Args:
            prompt: The fully-rendered phase template (all variables substituted).
            output_path: Absolute path where the agent must write its output.
            read_paths: Files the agent should read as input context.
                       Provider may enforce these as the only readable files
                       (sandboxed) or treat them as hints (permissive).
            metadata: Optional execution metadata:
                - phase: str (e.g., "review", "cross-review", "synthesis")
                - agent_name: str
                - mode: str
                - round: int
                - timeout: int (seconds)

        Returns:
            ExecutionResult with output content and execution metadata.
        """
        ...

    async def execute_batch(
        self,
        tasks: list[ExecutionTask],
    ) -> list[ExecutionResult]:
        """Execute multiple tasks in parallel.

        Default implementation: asyncio.gather over execute().
        Providers may override for native batch support
        (e.g., GitHub Actions matrix, LangGraph parallel nodes).
        """
        ...

    @property
    def name(self) -> str:
        """Provider identifier (e.g., 'claude-code', 'copilot', 'langgraph')."""
        ...

    @property
    def supports_tool_use(self) -> bool:
        """Whether this provider gives agents file read/write/search tools.

        True: Agents can autonomously read files and write output (agentic SDKs).
        False: Engine must pre-read files into the prompt and post-write the
               output from the result (direct model API providers).
        """
        ...
```

### ExecutionTask and ExecutionResult

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class ExecutionTask:
    """A single agent task to execute."""
    prompt: str
    output_path: str
    read_paths: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

@dataclass
class ExecutionResult:
    """Result from a single agent execution."""
    success: bool
    output_path: str
    content: str | None = None  # Output content (if provider captured it)
    error: str | None = None
    duration_ms: int = 0
    provider: str = ""
    metadata: dict = field(default_factory=dict)
```

---

## 4. Provider Implementations

> **Post-ruling note (2026-04-05)**: The original "ACP-native preferred path" framing below is **superseded** by the Decision Record (§0). The v1 preferred path is direct SDK (`mock`, `anthropic`) + subprocess (`claude-code`, `aider`, `opencode`) + HTTP/OpenAI-compatible (`ollama`, `llama-cpp`, `vllm`) + optional `LiteLLMProvider` companion. The `A2AProvider` (renamed from `acp`) is deferred pending ecosystem development. The historical subsection is preserved for context and is referenced by the `conversus-a2a-claude` post-v1 pioneer artifact.

### v1 Provider Set (binding)

Per the arbiter's ruling (updated to reflect implemented scope), v1 ships eight providers across three tiers plus one optional companion:

**Direct SDK (supports_tool_use=False):**

| Provider | Base class | Substrate validation | LoC estimate | Status |
|---|---|---|---|---|
| `mock` | — | Test substrate, deterministic responses | ~100 | Ships with core |
| `anthropic` | — | Anthropic Messages API with real cost telemetry | ~250-400 | v1 |

**Subprocess (supports_tool_use=True for agent runtimes):**

| Provider | Base class | Substrate validation | LoC estimate | Status |
|---|---|---|---|---|
| `claude-code` | `SubprocessProvider` | `claude -p` with JSON output, cost/duration from modelUsage | ~400-500 | v1, direct `claude` CLI subprocess |
| `aider` | `SubprocessProvider` | `aider --message --exit --yes-always` | ~200-300 | v1 |
| `opencode` | `SubprocessProvider` | `opencode run` | ~200-300 | v1 |

**HTTP/OpenAI-compatible (supports_tool_use=False, local inference):**

| Provider | Base class | Substrate validation | LoC estimate | Status |
|---|---|---|---|---|
| `ollama` | `HTTPProvider` | http://localhost:11434/v1 | ~150-250 | v1 |
| `llama-cpp` | `HTTPProvider` | http://localhost:8080/v1 (llama-server) | ~150-250 | v1 |
| `vllm` | `HTTPProvider` | http://localhost:8000/v1 | ~150-250 | v1 |

**Optional companion:**

| Provider | Base class | Substrate validation | LoC estimate | Status |
|---|---|---|---|---|
| `litellm` | — | 100+ model API coverage | ~14 core + docs | v1 optional companion package |

Total v1 budget: ~1,500-2,200 LoC core + ~150-250 LoC engine-side tool-use adaptation = ~1,700-2,450 LoC.

### Base classes

Two base classes factored from shared lifecycle code:

- **`SubprocessProvider`**: owns subprocess spawn, argv construction (secrets go via env, never argv), stdout/stderr capture, timeout handling, SIGTERM cleanup, cold-start amortization hooks. Used by `claude-code`, `aider`, and `opencode` in v1; future `copilot`, `codex`, `gemini-cli`, `continue` adapters.
- **`HTTPProvider`**: owns HTTP session lifecycle, OpenAI-compatible API dispatch, error taxonomy mapping, streaming passthrough. Used by `ollama`, `llama-cpp`, and `vllm` in v1; future `a2a` adapter.

### Historical ACP-native path (deferred)

The original spec 042 draft proposed `ACPProvider` as the preferred v1 path. Phase 1 research established that no shipping coding agent has been wrapped as an A2A server as of 2026-04, so "ACP ecosystem for free" is empirically false today. The path is preserved here as the future shape for `A2AProvider`:

```python
# POST-v1 — ships only when A2A coding-agent counterparties exist
class A2AProvider(HTTPProvider):
    """Dispatch tasks to A2A-compliant agent servers (Google/IBM protocol)."""

    name = "a2a"
    supports_tool_use = True

    def __init__(self, agent_url: str, **options):
        self.agent_url = agent_url  # A2A server endpoint

    async def execute(self, prompt, output_path, read_paths=None, metadata=None):
        task = build_a2a_task_request(prompt, output_path, read_paths, metadata)
        result = await self.client.submit_task(task, stream=True)
        return adapt_a2a_result(result)
```

A2A agents self-describe via **Agent Detail** metadata (capabilities, supported input types, etc.). When the ecosystem develops, the conversus engine can discover available agents at runtime rather than hard-coding provider lists. `.conversusrc::default_agents` schema accepts URL entries from v1 (with a "not yet supported" error) so future activation is config-level, not schema-level.

### Tier 1: Full agentic (tool use = True)

These providers give agents autonomous file access. The prompt says "read X, write to Y" and the agent handles it. Each can be wrapped as an ACP server or used directly via SDK.

| Provider | SDK/Interface | Parallel Strategy | ACP Wrappable? | Notes |
|----------|--------------|-------------------|----------------|-------|
| `acp` | ACP client (HTTP REST) | Concurrent Task Requests | Native | Preferred. Any ACP server. |
| `claude-code` | `@anthropic-ai/claude-agent-sdk` (subprocess or Node bridge) | `execute_batch` → parallel subprocess | Yes — wrap as ACP server | Default for interactive use. |
| `copilot` | `@github/copilot-sdk` (JSON-RPC to CLI server) | Session-per-task | Yes | Copilot CLI in server mode |
| `gemini-cli` | `@google/gemini-cli-sdk` (subprocess or Node bridge) | Subagent spawning | Yes | Gemini CLI headless mode |
| `opencode` | `@opencode-ai/sdk` (HTTP REST API) | Session-per-task | Yes — already HTTP | OpenCode in server mode |

### Tier 2: Workflow orchestrators (tool use = True, different dispatch)

These dispatch tasks to external workflow systems that manage their own agent lifecycles. Each could also be wrapped as an ACP server for uniform dispatch.

| Provider | Interface | Parallel Strategy | ACP Wrappable? | Notes |
|----------|----------|-------------------|----------------|-------|
| `gh-aw` | GitHub Actions workflow dispatch | Matrix strategy (N jobs) | Yes — action as ACP endpoint | Each phase is a workflow job. Cross-review = N*(N-1) matrix. |
| `langgraph` | LangGraph StateGraph | Parallel nodes per phase | Yes — graph as ACP server | Each phase is a node. Batch = fan-out/fan-in. |
| `gsd` | GSD executor agent | Sequential (GSD manages) | Internal only | Maps phases to GSD tasks. |
| `temporal` | Temporal workflows | Activity-per-task | Yes — workflow as ACP server | Enterprise workflow engine. Durable execution. |

### Tier 3: Direct model API (tool use = False)

These call model APIs directly. The engine must pre-read files into the prompt context and extract output from the response.

| Provider | Interface | Notes |
|----------|----------|-------|
| `anthropic` | `anthropic.AsyncAnthropic` | Existing `ModelProvider`. Engine inlines file contents. |
| `openai` | `openai.AsyncOpenAI` | Same pattern as anthropic. |
| `mock` | Canned responses | Testing. Already exists in `engine/providers/`. |

### Tool-use adaptation

When `supports_tool_use` is False, the engine wraps the prompt:

```python
if not provider.supports_tool_use:
    # Pre-read all files into prompt context
    file_contents = []
    for path in task.read_paths:
        content = Path(path).read_text()
        file_contents.append(f"## File: {path}\n\n{content}")

    augmented_prompt = (
        task.prompt
        + "\n\n---\n\n# File Contents\n\n"
        + "\n\n".join(file_contents)
        + f"\n\n---\n\nWrite your output below. It will be saved to {task.output_path}.\n"
    )

    result = await provider.execute(augmented_prompt, task.output_path)

    # Post-write: engine writes the content to output_path
    if result.content and result.success:
        Path(task.output_path).write_text(result.content)
```

---

## 5. Configuration

### conversus.yml

```yaml
mode: cooperative
target: specs/039-new-mode-payoffs/spec.md
output: conversus-output/

# NEW: execution provider configuration
executor:
  provider: claude-code          # required: provider name
  # Provider-specific options:
  model: claude-sonnet-4-6       # model override (provider-dependent)
  timeout: 120                   # per-task timeout in seconds
  max_parallel: 10               # max concurrent tasks
  # Provider-specific extras (passed as metadata):
  options:
    working_directory: .         # claude-code specific
    allowed_tools:               # claude-code specific
      - Read
      - Write
      - Grep
      - Glob

agents:
  - name: reviewer-a
    prompt: |
      ...
```

### Defaults

- If `executor:` is omitted, behavior depends on execution context:
  - Inside Claude Code session (SKILL.md): uses `claude-code` provider via Agent tool (current behavior, backward compatible)
  - Via Python SDK (`Deliberation.run()`): uses `anthropic` provider (current ModelProvider behavior)
  - Via CLI (`conversus run`): uses `claude-code` provider via subprocess

### Provider resolution

```python
PROVIDER_REGISTRY: dict[str, type[ExecutionProvider]] = {}

def get_provider(name: str, options: dict) -> ExecutionProvider:
    """Resolve provider by name. Raises if not installed."""
    if name not in PROVIDER_REGISTRY:
        available = sorted(PROVIDER_REGISTRY.keys())
        raise ValueError(
            f"Unknown executor provider '{name}'. "
            f"Available: {available}. "
            f"Install the provider package or check spelling."
        )
    return PROVIDER_REGISTRY[name](**options)
```

Providers register via entry points (post-032 pip packaging) or direct import:

```python
# conversus/providers/claude_code.py
from conversus.engine.execution import ExecutionProvider, PROVIDER_REGISTRY

class ClaudeCodeProvider(ExecutionProvider):
    ...

PROVIDER_REGISTRY["claude-code"] = ClaudeCodeProvider
```

---

## 6. Blog Generation Pipeline (motivating use case)

The blog pipeline is the first consumer of the execution provider abstraction. It reads conversus output (reviews, synthesis, disputes) and generates blog posts.

### Pipeline definition

```yaml
# blog-pipeline.yml
mode: cooperative
target:
  - conversus-output/summary/final.md
  - specs/EXECUTION-ORDER.md
  - conversus/plugins/nashopt/payoffs.py
output: blog-output/

executor:
  provider: claude-code
  options:
    allowed_tools: [Read, Write, Grep, Glob]

agents:
  - name: technical-writer
    prompt: |
      You are a technical writer for the conversus engineering blog.
      Read the deliberation output and source code changes.
      Write a blog post explaining what was built, why, and how.
      Use the mkdocs-material blog frontmatter format.
      Target audience: developers evaluating conversus.
    docs:
      - docs/blog/posts/01-docs-review-setup.md  # style reference

  - name: storyteller
    prompt: |
      You are a narrative writer. Read the deliberation output.
      Write a blog post that tells the STORY — the problem,
      the approach, the surprises, the result.
      Make it engaging for non-technical readers.
    docs:
      - docs/blog/posts/02-three-rounds-to-convergence.md  # style reference
```

### Post-processing

After the deliberation, the synthesis identifies the best elements from both drafts. A final agent (or manual review) combines them into the published post.

This is just a standard conversus run — the "target" is the work output, the "agents" are writers with different perspectives. The execution provider doesn't know or care that the output is a blog post.

---

## 7. GitHub Agentic Workflows Integration

The `gh-aw` provider maps conversus phases to GitHub Actions jobs:

```yaml
# .github/workflows/conversus-review.yml
name: Conversus Review
on:
  pull_request:
    paths: ['specs/**']

jobs:
  review:
    strategy:
      matrix:
        agent: [code-verifier, user-advocate, developer-advocate]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run conversus agent
        uses: Build-Fractal/gh-aw-conversus@v1
        with:
          phase: review
          agent: ${{ matrix.agent }}
          config: conversus.yml
```

Each phase becomes a workflow job. Cross-review is an N*(N-1) matrix. The `gh-aw` provider handles:
- Dispatching workflow runs via `gh workflow run`
- Polling for completion
- Collecting output artifacts
- Passing output paths between phases

This turns conversus into a **CI/CD-native review tool** — every PR gets a multi-agent deliberation as part of the check suite.

---

## 8. Functional Requirements

### Provider Interface
- **FR-001**: All providers MUST implement the `ExecutionProvider` protocol.
- **FR-002**: `execute()` MUST be async and return `ExecutionResult`.
- **FR-003**: `execute_batch()` MUST execute tasks in parallel where possible.
- **FR-004**: Providers MUST report `supports_tool_use` accurately.
- **FR-005**: When `supports_tool_use` is False, the engine MUST inline file contents and post-write output.

### Configuration
- **FR-006**: `executor:` field in conversus.yml MUST be optional (backward compatible).
- **FR-007**: Provider resolution MUST fail with a clear error if the provider is not installed.
- **FR-008**: Provider-specific options MUST pass through without engine validation (providers validate their own options).

### Backward Compatibility
- **FR-009**: Omitting `executor:` inside a Claude Code session MUST behave identically to current SKILL.md behavior.
- **FR-010**: Omitting `executor:` in the Python SDK MUST use the existing ModelProvider path.
- **FR-011**: The SKILL.md MUST continue to work as-is for users who don't configure an executor.

### Provider Lifecycle
- **FR-012**: Providers MAY implement `async def setup()` and `async def teardown()` for session management.
- **FR-013**: The engine MUST call `setup()` before first `execute()` and `teardown()` after last `execute()` in a run.

---

## 9. Success Criteria

- **SC-001**: A conversus deliberation runs end-to-end using the `claude-code` provider (subprocess, not SKILL.md) and produces identical output structure.
- **SC-002**: A conversus deliberation runs using the `anthropic` provider (direct API, no tool use) with file contents inlined.
- **SC-003**: A conversus deliberation runs using the `mock` provider in tests.
- **SC-004**: The blog generation pipeline produces a blog post from Wave 1 output using any provider.
- **SC-005**: Adding a new provider requires only implementing `ExecutionProvider` — no engine changes.

---

## 10. Constraints

- The engine orchestration logic (phase sequencing, template rendering, dispute parsing) MUST NOT change.
- Provider implementations are optional packages — only `mock` ships with core `conversus`.
- The `claude-code` provider is the reference implementation but NOT a core dependency.
- No provider may modify the template variable contract — templates are provider-agnostic.
- The SKILL.md remains the primary UX for interactive use. The provider abstraction enables headless/programmatic/CI use cases.

---

## 11. Supported Provider Matrix (living document)

Updated 2026-04-05 per arbiter ruling (§0). `acp` row split into `a2a` (HTTP, agent-to-agent) and `zed-acp` (stdio, IDE-to-agent). Cold-start column added per ground-truth constraint.

| Provider | Type | Tool Use | Parallel | Base class | Cold Start | Status |
|----------|------|----------|----------|------------|------------|--------|
| `mock` | Test (Direct SDK) | No | asyncio.gather | — | 0ms | **v1** — ships with core, deterministic responses |
| `anthropic` | Model API (Direct SDK) | No | asyncio.gather | — | ~0ms | **v1** — Anthropic Messages API with real cost telemetry |
| `claude-code` | Agentic CLI subprocess | Yes | Subprocess pool | `SubprocessProvider` | 1-3s/invocation | **v1** — `claude -p` with JSON output, cost/duration from modelUsage |
| `aider` | Agentic CLI subprocess | Yes | Subprocess pool | `SubprocessProvider` | 1-3s/invocation | **v1** — `aider --message --exit --yes-always` |
| `opencode` | Agentic CLI subprocess | Yes | Subprocess pool | `SubprocessProvider` | 1-3s/invocation | **v1** — `opencode run` |
| `ollama` | HTTP/OpenAI-compatible | No | asyncio.gather | `HTTPProvider` | ~0ms (local server) | **v1** — http://localhost:11434/v1 |
| `llama-cpp` | HTTP/OpenAI-compatible | No | asyncio.gather | `HTTPProvider` | ~0ms (local server) | **v1** — http://localhost:8080/v1 (llama-server) |
| `vllm` | HTTP/OpenAI-compatible | No | asyncio.gather | `HTTPProvider` | ~0ms (local server) | **v1** — http://localhost:8000/v1 |
| `litellm` | Model API multiplexer | No | asyncio.gather | — | ~0ms | **v1 optional** — companion package, covers 100+ model APIs |
| `openai` | Model API | No | asyncio.gather | — | ~0ms | v2 — subsumed by `litellm` unless user opts for native |
| `copilot` | Agentic CLI subprocess | Yes | Session pool | `SubprocessProvider` | 1-3s/invocation | v2 — shares `SubprocessProvider` base |
| `gemini-cli` | Agentic CLI subprocess | Yes | Subprocess pool | `SubprocessProvider` | 1-3s/invocation | v2 — shares `SubprocessProvider` base |
| `codex` | Agentic CLI subprocess | Yes | Subprocess pool | `SubprocessProvider` | 1-3s/invocation | v2 — shares `SubprocessProvider` base |
| `continue` | Agentic CLI subprocess | Yes | Subprocess pool | `SubprocessProvider` | 1-3s/invocation | v2 — shares `SubprocessProvider` base |
| `a2a` | A2A HTTP (Google/IBM LF) | Yes | Concurrent HTTP | `HTTPProvider` | ~100ms | **Deferred** — empty counterparty ecosystem as of 2026-04; ships when ≥3 shipping coding agents expose A2A servers |
| `zed-acp` | Zed/JetBrains Agent Client Protocol | Yes | stdio sessions | separate scope | — | **Out of v1 scope** — different protocol, IDE-to-agent stdio, not agent dispatch |
| `gh-aw` | Workflow | Yes | GitHub Actions matrix | separate scope | — | v2+ |
| `langgraph` | Workflow | Yes | StateGraph fan-out | separate scope | — | v2+ |
| `temporal` | Workflow | Yes | Activity pool | separate scope | — | v2+ |
| `gsd` | Workflow | Yes | GSD executor | separate scope | — | Internal |

**Implementation strategy** (post-ruling, updated): Ship 8 v1 providers across three tiers + `LiteLLMProvider` companion. The `SubprocessProvider` base class validates via `claude-code`, `aider`, and `opencode`, then serves every future CLI tool. The `HTTPProvider` base class validates via `ollama`, `llama-cpp`, and `vllm` (all OpenAI-compatible local inference servers), and serves the future `a2a` provider. The `a2a` row is a triggered commitment — it ships when ≥3 coding agents expose A2A servers, at which point `conversus-a2a-claude` (authored post-v1 as a standalone pioneer artifact) becomes the reference implementation for wrapping subprocess tools as A2A servers.

---

## 12. Open Questions (resolved and remaining)

Most open questions are resolved by the arbiter ruling (§0). See [`conversus-output/arbitration/resolution.md`](conversus-output/arbitration/resolution.md) for the full ruling.

1. **Credential management**: ~~Should the engine manage auth or delegate?~~ **Resolved**: Delegate to providers via env vars. `SubprocessProvider` guarantees secrets never appear in argv (validation.md §3.4).

2. **Output format enforcement**: **Unchanged**: Post-execution validation is engine responsibility, applies regardless of provider.

3. **Cost tracking**: ~~Optional field?~~ **Resolved**: `ExecutionResult.cost` is a first-class structured field. Per-agent, per-phase, per-run aggregation required (validation.md §3.2, binding condition #5).

4. **Streaming**: **Deferred to v2**: Batch execution with completion notification sufficient for v1. Protocol shape accommodates streaming without future migration (binding condition #1).

5. **Provider composition**: **Unchanged**: Single provider per run in v1. `metadata.phase` field enables per-phase routing when needed.

6. **`a2a` vs direct SDK**: ~~When to use which?~~ **Resolved**: Direct SDK (subprocess/HTTP) for v1. `a2a` deferred until ecosystem counterparties exist.

7. **A2A agent wrapping**: ~~Ship reference wrapper?~~ **Resolved**: Yes, `conversus-a2a-claude` as a **post-v1 standalone pioneer artifact** (not a v1 deliverable). Enables long-lived-process Claude Code dispatch solving cold-start amortization.

8. **Zed/JetBrains Agent Client Protocol**: ~~Track?~~ **Resolved**: Out of spec 042 scope entirely. Separate protocol, separate use case (IDE-to-agent stdio), tracked as `zed-acp` row in §11 for terminological clarity only.

### Remaining open questions (post-ruling)

9. **Subprocess pooling trigger**: When does `SubprocessProvider` graduate from "spawn-per-task" to "pool-based"? Ground-truth constraint says cold start × N phases is real. Expose `supports_pooling` flag day 1, implement pool in v1.1 or v2?
   - **Lean**: Flag in v1, pool implementation deferred to v1.1 after real-world cold-start measurements.

10. **LiteLLM proxy-mode composition**: Litellm advocate flagged "LiteLLM proxy fronting subprocess tools" as unchallenged through all 6 cross-reviews — no one has validated the composition works end-to-end. Does it?
    - **Lean**: Smoke-test in Phase 5 integration tests. If it works, documented as an enterprise-gateway pattern. If it doesn't, not a blocker.

11. **Conversus-as-universal-skill**: Should conversus be packaged via APM for Cursor, VSCode, Copilot, Zed in parallel with 042? See sibling **spec 049** (Conversus as Universal Skill/MCP Server) — new spec, runs in parallel with 042 implementation.

---

## 13. Binding Conditions (arbiter ruling — implementation requirements)

Per Phase 6 arbitration (2026-04-05), the winning architecture must satisfy these 14 conditions during Phase 1-6 implementation. See [`conversus-output/arbitration/resolution.md`](conversus-output/arbitration/resolution.md) for full rationale.

### Protocol shape conditions (partial incorporation from a2a-future-advocate)

1. **A2A-Task-Request-compatible shape**: `ExecutionTask`/`ExecutionResult` designed with structured `parts`, `references`, `metadata`, and streaming-compatible fields in Week 1. Provide `from_prompt()` compatibility constructor so subprocess/direct-API providers remain flat. ~4 hours design cost. Zero `a2a-sdk` dependency in core v1.

2. **`conversus-a2a-claude` as post-v1 pioneer artifact**: Separate standalone package, not a v1 deliverable. Ships when ecosystem triggers activate.

3. **`.conversusrc::default_agents` URL schema**: Schema accepts URL entries with "not yet supported" error in v1. ~20 lines of schema code. Enables future A2A activation as config change.

### Validation battery conditions (from validation.md)

4. **`ProviderError.category` expanded Literal**: `auth`, `rate_limit`, `server`, `timeout`, `subprocess`, `network`, `malformed`, `unknown`. Each failure mode mapped to a distinct category. (validation.md §3.3)

5. **Per-agent cost telemetry**: `ExecutionResult.cost` is a structured field, not free-form. Per-agent, per-phase, per-run aggregation. (validation.md §3.2)

6. **Duration as structured type**: `ExecutionResult.duration` is a `Duration` (compatible with spec 047's `TemporalMatch`) or convertible with zero precision loss. (validation.md §1.7)

7. **SIGTERM handling**: All in-flight subprocesses cleanly cancel on SIGTERM. Partial output preserved. No orphan processes. (validation.md §3.6)

8. **Replay harness**: Spec 042, 045, 031 deliberations replayable through the new architecture as integration tests. (validation.md §4)

9. **MCP tool-use preserved**: Agents can USE MCP tools during execution (filesystem, fetch, etc.). Provider layer does NOT conflate MCP with dispatch. (validation.md §3.5, ground-truth constraint)

10. **Secrets never in argv**: `SubprocessProvider` enforces env-only secret passing. Audited per provider. (validation.md §3.4)

11. **12-agent parallel phase test**: Concurrency test launching 12 agents in a single phase. Wall-clock ≈ max(agents), not sum. (validation.md §3.1)

12. **Free-tier clean-venv install test**: `pip install conversus` (no paid extras) + run deliberation with `mock` + `claude-code` providers. (validation.md §2.1)

13. **Paid-tier layered install test**: Install `conversus-solvers` on top of free tier. Verify free-tier deliberation still works identically. (validation.md §2.2)

14. **API-key-less free-tier user story**: User with only local `claude` binary (no API keys) can run a deliberation. `claude-code` provider must not require env vars or API keys. (validation.md §2.3)

### Reconsideration triggers (from arbitration resolution §Required changes)

The ruling should be reconsidered if any of the following occur:

- **LiteLLM health decline**: Maintenance stalls, CVE response slows, or upstream LLM providers break the LiteLLM adapter layer → reconsider native-only posture
- **A2A ecosystem acceleration**: ≥3 shipping coding agents expose A2A servers → activate `a2a` provider and `conversus-a2a-claude` pioneer artifact
- **URL schema real usage**: Users begin registering URL-addressable agents in `.conversusrc` → prioritize `a2a` implementation
- **LiteLLM proxy-mode end-to-end validation failure**: If the proxy-mode-fronts-subprocess composition fails real-world testing, drop it from documentation
- **Budget compression to 2 weeks**: If 042 must ship in half the planned time → drop `opencode` from v1 (validates HTTP substrate later, not in v1)
