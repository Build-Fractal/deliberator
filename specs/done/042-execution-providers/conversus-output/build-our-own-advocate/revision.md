# Build-Our-Own-Advocate — Phase 3 Revision

**Round**: 1, Phase 3 (defense)
**Iteration**: 1
**Stance**: Build a conversus-owned `ExecutionProvider` Protocol. Ship 4 providers in v1. Every other proposal — LiteLLM, A2A, workflow orchestrators — is an **additive downstream adapter** inside this plan, not a competitor to it.

---

## Position Summary

**Thesis, refined**: conversus defines its own minimal `ExecutionProvider` Protocol (`prompt`, `read_paths`, `output_path`, `metadata` → `ExecutionResult`), factors a `SubprocessProvider` base class around the subprocess-CLI-JSON backbone that the ecosystem has already converged on, and ships four concrete providers in v1: `mock`, `anthropic`, `claude-code` (via direct `claude -p --bare` subprocess — not via `claude-agent-sdk`), and `opencode` (via `HTTPProvider` against the `opencode serve` OpenAPI 3.1 spec). Every other provider the roadmap wants — LiteLLM, A2A, OpenAI, Gemini, gh-aw, aider, copilot, langgraph — is an incremental subclass against the same Protocol, landing on its own schedule.

**What did not change from my opening argument**: the core structural claim. No library exists whose public API is `execute(prompt, read_paths, output_path, metadata) -> ExecutionResult` covering both model APIs and agent runtimes. That was verified by the backbone researcher (§7, §10) and conceded outright by both other advocates. Build-our-own is the only architecture that can exist in this ecosystem in 2026-04.

**What changed**: the v1 provider count (3 → 4), the implementation factoring (bare Protocol → Protocol + two base classes), the realistic LoC estimate (~500–700 → ~1000–1200), and the explicit disambiguation of A2A vs. Zed/JetBrains ACP in spec 042 §11.

**Convergence note — the LiteLLM position has collapsed into mine.** The litellm-hybrid advocate conceded in their cross-review §1 (verbatim): *"The build-our-own advocate and I are, in substance, proposing the same architecture… The build-our-own advocate wrote a better review than I did on the protocol-ownership question."* Their Week 1 deliverable (§8) explicitly says "Implement `ExecutionProvider`, `ExecutionTask`, `ExecutionResult` per spec 042 §3 — **conversus code, not LiteLLM**." That is my proposal verbatim. The remaining disagreement is a single ~14-line adapter file. I accept the superset framing and fold it in: **`litellm` becomes one of the Tier-3 providers inside my Protocol**, alongside native `anthropic`. This document is the unified position.

---

## Rebuttals

### Partially Rebutted: "100–200 LoC per adapter is ~2x low for `claude-code`" (backbone-researcher §2.3)

- **Their claim**: My cost estimate cited tool-landscape.md's "100–200 lines per adapter" figure and concluded v1 is ~500–700 LoC. The researcher documented that a production `claude-code` subprocess adapter must handle process lifecycle, JSON stream parsing, flag construction, binary discovery, cold-start economics, `read_paths` semantics, and `output_path` enforcement — realistically 400–800 LoC, not 100–200. Adjusted v1 total ~800–1,200 LoC.
- **What is true**: I cited a planning number from an internal research doc as if it were empirical ground truth. For `mock` and `anthropic` the 100–200 figure holds. For `claude-code` as a subprocess lifecycle manager, it understates by ~2x. I concede the cost adjustment.
- **What is false or misleading**: The conclusion "~500–700 LoC" was wrong; the conclusion "still small in absolute terms" is unchanged. The researcher themselves writes that even the adjusted number is "still small — less than a single Django admin class framing survives — but the estimate they quote is off by roughly 2x." My **architectural** argument does not depend on the exact number; it depends on the relative scale being tractable. ~1,000–1,200 LoC is tractable. It is also still strictly smaller than the code LiteLLM-hybrid would ship, because LiteLLM-hybrid writes the same subprocess adapters AND pulls in LiteLLM.
- **Net assessment**: The estimate is corrected in this revision. The architectural conclusion is unchanged. The "Django admin class" framing survives for the thin providers and gets retired for the load-bearing one.
- **Status**: Partially rebutted. Cost correction absorbed; architectural conclusion intact.

### Conceded: "`claude-code` is not zero-dep and the `claude-agent-sdk` path adds failure modes" (backbone-researcher §4.1, §4.2)

- **Their claim**: My dependency table labeled `claude-code` as "`claude-agent-sdk` OR subprocess (zero new deps)." This elides (a) that `claude-agent-sdk` is itself a PyPI package marked Alpha at 0.1.56, (b) that it is a subprocess wrapper underneath — choosing it adds a dep for zero architectural benefit, and (c) that the "OR subprocess" path still requires the `claude` CLI binary on PATH as a deployment dep. The "zero new deps" framing is misleading.
- **Concession**: All three points are correct. I am dropping the `claude-agent-sdk` option entirely from my v1 plan. The v1 `ClaudeCodeProvider` invokes `claude -p --bare --output-format json` directly via `asyncio.create_subprocess_exec`, and the v1 deployment prerequisites explicitly include "the `claude` CLI binary must be on PATH at a compatible version." The Python SDK is a layer with no architectural value once we're already a subprocess-manager.
- **Impact**: This actually **strengthens** the build-our-own position. Going through `claude-agent-sdk` would have been an alpha-package dependency with bundled-binary distribution complexity; going direct-to-CLI is fewer moving parts and fewer failure modes. The concession removes a weakness from my plan rather than introducing one. It also eliminates the "Node bridge" phantom option that the spec text previously referenced — Python → Node → CLI is strictly worse than Python → CLI.
- **Status**: Conceded with context. The correction improves the plan.

### Conceded: "The single `acp` row conflates two different protocols and must be split" (backbone-researcher §3.2)

- **Their claim**: Spec 042 §11's `acp` row mixes A2A (Linux Foundation, JSON-RPC over HTTP, zero coding-agent wrappers shipped) with Zed/JetBrains Agent Client Protocol (stdio JSON-RPC, IDE-to-agent, designed for human-in-the-loop approval). These are different wires, different transports, different threat models, different timelines. My "one acp provider" framing obscures this.
- **Concession**: Fully correct. I am renaming the spec 042 §11 row from `acp` to `a2a` and adding a separate, lower-priority `zed-acp` row tracked as an IDE-integration vector (appropriate for a future spec, not spec 042 v1). My original review's "ACP-compatible superset" argument should be read as "A2A-compatible superset" — the prompt/read_paths/output_path/metadata mapping was to A2A's Task Request model, not to the IDE-facing stdio protocol.
- **Impact**: The researcher's own observation is that owning the Protocol is **exactly what lets you have two provider rows for two wire protocols**. This correction makes my position stronger, not weaker. When the eventually-distinct `a2a` and `zed-acp` providers ship, they will ship as independent adapters behind the same internal Protocol. A LiteLLM-hybrid or A2A-first architecture could not cleanly express that split.
- **Status**: Conceded with context. The correction is a spec-hygiene fix; the architecture survives unchanged.

### Rebutted: "You did not discuss subprocess cold-start economics, which matter for spec 048" (backbone-researcher §4.3)

- **Their claim**: CLI cold-start is ~1–3s per invocation. A conversus deliberation with 10 parallel phases × 5 rounds is 50 subprocess spawns ≈ 50–150s of process overhead. An HTTP-server backbone (OpenCode, future A2A) amortizes this to near-zero. My review did not acknowledge this.
- **My response**: Correct that I did not discuss it. The response is not to concede but to **act on it** in the v1 plan: add `opencode` as a v1 provider via an `HTTPProvider` base class. That is now the fourth v1 provider. It validates the HTTP substrate before A2A matures, provides an architecturally-superior benchmark against subprocess providers, and gives spec 048 a cold-start-free option for autonomous-governance runs that fan out widely. The researcher's observation is actionable, not fatal.
- **Concrete plan**: v1 ships with two substrate base classes (`SubprocessProvider`, `HTTPProvider`), not one. Users with high-fanout workloads pick `opencode`; users who need Claude Code compatibility pick `claude-code`. The protocol is indifferent; the engine is indifferent; the user chooses based on their cost profile.
- **Status**: Rebutted via plan amendment. The v1 provider set expands from 3 to 4, with `opencode` specifically included to address the cold-start concern.

### Rebutted: "The `mock` provider stabilizes 3,428 tests" claim is under-specified (backbone-researcher §2 implicit; self-noted in my own cross-review §5.1)

- **Their claim** (self-raised in my own cross-review of the researcher): The benefit is real but I haven't actually enumerated how many of the 3,428 tests dispatch agents vs. test template rendering vs. phase logic. The "stabilizes 3,428 tests" rhetoric over-claims.
- **My response**: Downgraded. The revised claim is narrower and still defensible: **the `mock` provider replaces the ad-hoc agent mocking patterns currently scattered across the test suite with a single, protocol-typed test double.** The exact count of affected tests is an implementation detail that will be surfaced during migration. The structural benefit — one mock, one protocol, one source of truth — holds regardless of the specific number.
- **Why this matters for the deliberation**: Even under the downgraded framing, no alternative architecture provides this benefit. LiteLLM cannot provide it for Tier 1 (LiteLLM does not dispatch agents). A2A cannot provide it in 2026-04 (no counterparties; a mock would have to re-implement the wire protocol). Only a conversus-owned Protocol gives us a conversus-owned mock. The claim was rhetorically oversized; the underlying advantage is real and unique to this architecture.
- **Status**: Rebutted in its rhetorical form; underlying advantage preserved.

### Rebutted: "3 of 12 providers" undercounts LiteLLM's coverage (litellm-hybrid §3)

- **Their claim**: My original review said LiteLLM covers "3 of 12 targeted providers" (`anthropic`, `openai`, `gemini`). The hybrid advocate corrected this: LiteLLM covers 100+ providers, including every Tier-3 entry in spec 042 §11 plus a long tail (Groq, DeepSeek, Fireworks, Ollama, VLLM, Bedrock, Vertex, etc.). The correct critique is "LiteLLM covers zero Tier-1 providers," which is sufficient to make my point.
- **My response**: The hybrid advocate is right on the factual correction and I am adopting their framing. The accurate statement is: **LiteLLM covers ~25% of spec 042 §11's target provider rows (the Tier-3 direct-model-API slice) and absorbs an unbounded long tail of additional model APIs not enumerated in the matrix. It covers zero Tier-1 agent runtimes and zero Tier-2 workflow orchestrators.** That is a cleaner critique and a more honest recognition of LiteLLM's actual value.
- **What this means for the v1 set**: Because the hybrid advocate has conceded the protocol-ownership question and the superset framing, and because LiteLLM's long-tail absorption is genuine value, **I am folding `LiteLLMProvider` into the Tier-3 adapter slot as a recommended optional package** (`conversus-provider-litellm`). Users who want the 100+ model buffet install it; users who want minimum dependency footprint install the native `anthropic` provider instead. Both coexist under the same Protocol. This is exactly the synthesis the hybrid advocate proposed in their §9.
- **Net assessment**: The "3 of 12" framing was wrong. The underlying point — that LiteLLM does not cover the Tier-1 half of spec 042 — is preserved and is sufficient. The hybrid advocate has already conceded that their position is a proper subset of mine, so the disagreement collapses to "which concrete Tier-3 implementation ships first." My answer is now "both, as optional packages, in v1."
- **Status**: Rebutted in the factual framing (I adopt their correction); the architectural conclusion is unchanged and the hybrid position is absorbed into mine.

### Rebutted: "The `PROVIDER_REGISTRY` is too static for A2A-style discovery" (a2a-future §4.1, §6)

- **Their claim**: The module-level dict in spec 042 §5 does not accommodate runtime-discovered agents (A2A's Agent Detail model, URL-dispatched providers, etc.). For the 2027+ A2A future, conversus should leave room for dynamic discovery.
- **My response**: Accepted as a small, forward-looking protocol refinement that costs nothing today. The `PROVIDER_REGISTRY` gains a `register_provider(name, instance)` hook so a future `a2a` provider can register discovered agents dynamically, and `.conversusrc::agent_registry` (spec 048) can evolve to accept URLs alongside provider-name strings when the ecosystem is ready. This is a three-line API addition, not an architectural change.
- **Why this strengthens my position**: The a2a-future advocate conceded in their §5 (verbatim): *"Build-our-own's `ExecutionProvider` protocol is the correct v1 foundation for spec 042. A2A is the most important future provider within that protocol, not a replacement for it."* My plan already treats A2A as an additive provider. Adding a dynamic registration hook is the exact design affordance they wanted. I accept it.
- **Status**: Rebutted via plan amendment. The registry gains a `register_provider()` hook; the architecture is unchanged.

### Rebutted: "The A2A commitment in your plan is too weak — it should be in the spec, not deferred" (a2a-future §6)

- **Their claim**: My §3.4 "A2A/ACP is the future, just wait" is too dismissive. The actual answer should be "ship build-our-own now AND commit to A2A as the destination." The superset framing should come with an explicit A2A commitment in the spec.
- **My response**: Accepted, with the caveat that commitments must be triggered by ecosystem reality, not calendar dates. The revised commitment is: **when at least 3 of {Claude Code, Aider, OpenCode, Copilot, Codex, Gemini} ship A2A server wrappers (whether from the vendors, the community, or conversus itself as a post-042 ecosystem contribution), the `a2a` provider becomes the recommended path for agent-to-agent composition and cross-vendor dispatch.** Until then, `a2a` stays in the spec 042 §11 matrix as a first-class row with "Status: awaiting counterparties." This is a firmer commitment than my original review's "we'll see," and it is tied to a concrete, measurable precondition.
- **Status**: Rebutted via strengthened commitment. The A2A advocate's forward-looking argument is absorbed as a triggered roadmap commitment inside my plan.

### Rebutted: "Conversus should contribute A2A server wrappers as an ecosystem investment" (a2a-future §4.3)

- **Their claim**: If no one has wrapped Claude Code as an A2A server yet, the first team that does owns disproportionate ecosystem influence. Conversus is already building a `ClaudeCodeProvider`; the delta to exposing it as an A2A server is modest (~300–600 lines).
- **My response**: Accepted as a post-042 opportunity, explicitly not part of v1. Critically, **the A2A server wrapper is built on top of `ClaudeCodeProvider`, not as a replacement for it.** An A2A server exposing Claude Code has to shell out to `claude -p --bare` underneath — it has to use exactly the subprocess machinery my plan ships in v1. So the v1 plan is a **prerequisite** for the A2A ecosystem contribution, not an alternative to it. The A2A advocate's own §4.3 says so: "the researcher's §10 shows Claude Code's CLI surface is exactly what an A2A server would shell out to anyway."
- **This is the cleanest "superset" case in the deliberation**: the A2A advocate's single most strategically valuable idea (wrap Claude Code as an A2A server for ecosystem leverage) is literally built on top of my v1 `ClaudeCodeProvider`. Their Phase 1 framing treated these as alternatives; they now explicitly recognize them as layered.
- **Status**: Rebutted by absorption. The A2A server wrapper is a post-042 artifact that the v1 plan enables.

---

## Reinforced Strengths

### 1. No wheel exists — verified by the researcher, conceded by both other advocates

My §3.1 argument ("name the library whose public API is `execute(prompt, read_paths, output_path, metadata)` covering both model APIs and agent runtimes — it does not exist") was the load-bearing claim of my Phase 1 review. It survived cross-review with **explicit verification** from the backbone researcher (§1 of their cross-review: *"This claim is verified"*) and **explicit concession** from both advocates:

- LiteLLM-hybrid §7, verbatim: *"The 'no wheel exists' argument (their §3.1) is correct. There is no library whose API matches spec 042 §3. LiteLLM is not a wheel for this — it's a wheel for a different (sub-)problem. Calling the protocol 'wheel reinvention' would be wrong."*
- A2A-future §1, verbatim: *"The superset framing is valid at the architectural level (A2A is an adapter, not a competitor)."*

When the load-bearing claim is verified by the neutral researcher AND conceded by both adversarial advocates, the architectural question is settled. The remaining disagreements are tactical.

### 2. The engine has one dispatch call site — unchallenged

My §2.4 argument that the refactor is a single call site (`Agent(prompt=..., run_in_background=True)` in SKILL.md) was not challenged by any cross-review. The researcher's §1.4 independently confirmed that Claude Code's `Agent` tool is only addressable from inside a live Claude session, which **is** the coupling the refactor removes. FR-009/010/011 backward compat guarantees are trivially achievable because there is one place to change.

This is an unchallenged advantage. It means the refactor cost is bounded, the backward-compat story is credible, and spec 048's hard dependency on spec 042 unblocks on a realistic timeline.

### 3. Owning the Protocol is exactly what lets us have two provider rows for two wire protocols — battle-tested

The backbone researcher's §3.2 on the ACP/A2A conflation is framed as a critique of my Phase 1 review, but the researcher's own conclusion (verbatim) is: *"The build-our-own position actually **strengthens** when you acknowledge the split — because owning the Protocol is exactly what lets you have two providers where the wire-level standard has two protocols."*

This is a strength my Phase 1 review did not claim explicitly. The cross-review process surfaced it. Under a LiteLLM-framed architecture or an A2A-framed architecture, splitting `acp` into `a2a` and `zed-acp` would be awkward because the external framework would have opinions about what "ACP" means. Under a conversus-owned Protocol, the split is trivial: two rows, two adapters, done.

### 4. The v1 plan unblocks spec 048 on the only calendar that exists — strengthened by the A2A concession

The a2a-future advocate's §2 concession is the sharpest version of this argument:

> *"Spec 042 cannot wait for the A2A ecosystem to catch up because spec 048 cannot wait for spec 042. And even if spec 042 did wait, waiting produces no A2A counterparties on its own — someone still has to write the wrappers."*

They go on to conclude that "build-our-own wins this axis outright." I did not have this level of commitment from them in my Phase 1 review. The hard-dependency argument has moved from "my claim" to "stipulated by all parties." Spec 048 cannot ship without spec 042 shipping first, and the only architecture that ships spec 042 in 2026-04 is build-our-own.

---

## New Arguments

### New Argument 1: The v1 provider set is the **minimum set that validates both substrates and both tool-use modes**

- **The argument**: The four v1 providers (`mock`, `anthropic`, `claude-code`, `opencode`) are not arbitrary — they are the minimum set that exercises every important axis of the protocol:
  - **`mock`**: validates the Protocol shape, validates the test-substitution story, pure Python.
  - **`anthropic`**: validates `NativeProvider`-style direct-SDK adapters, validates `supports_tool_use=False` with engine-side file inlining and post-writing (spec 042 §4 lines 268–290). This exercises the engine's tool-use adaptation path.
  - **`claude-code`**: validates `SubprocessProvider` base class, validates `supports_tool_use=True` path (agent reads files itself via Read tool, agent writes output via Write tool), validates subprocess lifecycle and cold-start economics, provides backward compat with SKILL.md workflows.
  - **`opencode`**: validates `HTTPProvider` base class, validates long-lived connections and session management, provides the cold-start-free option for high-fanout workloads.
  - Every future provider is a subclass of one of these three shapes.
- **Source**: This insight emerged from the backbone researcher's §2.2 (OpenCode is a proper HTTP server by design) and §4.3 (cold-start economics for subprocess providers). I did not frame it this way in my Phase 1 review.
- **Evidence**: Backbone researcher §1 (Claude Code subprocess architecture), §2 (OpenCode HTTP architecture), §4.3 (cold-start tradeoffs). Spec 042 §4 lines 268–290 (tool-use adaptation). The four v1 providers collectively cover 100% of the Protocol's surface; adding any fifth provider in v1 adds zero new validation coverage.

### New Argument 2: `SubprocessProvider` and `HTTPProvider` base classes are the `BaseIntegrator` pattern applied to execution providers

- **The argument**: The monorepo's apm integrator architecture has a well-known principle from `/Users/business-daddy/code/payer-index-mono/apm/src/apm_cli/integration/` (cited in the project instructions): *"One base, many file types. All file-level integrators share a single `BaseIntegrator` infrastructure… New integrators add what to deploy, never how to deploy."* The execution-provider layer has the exact same shape: many providers, shared substrate, the substrate belongs in one place. `SubprocessProvider` factors out the "spawn a CLI, read JSON output" backbone; `HTTPProvider` factors out the "long-lived HTTP session with streaming" backbone. Concrete providers then only define *what* to dispatch (flag construction, output schema parsing) — never *how*.
- **Source**: The backbone researcher's §7 finding that "the de facto backbone across all agentic coding tools today is: subprocess-spawn a CLI, pass a prompt via `-p`/`--message`/stdin, collect JSON output" made the substrate unavoidable. My original review proposed bare providers inheriting from the Protocol directly; that would have duplicated the substrate N times.
- **Evidence**: Backbone researcher §7 (common pattern table), §10 (tool-by-tool CLI surface), §11.2 (de facto backbone). Monorepo integrator architecture at `/Users/business-daddy/code/payer-index-mono/apm/src/apm_cli/integration/base_integrator.py`.

### New Argument 3: The deliberation has produced a **unified provider plan** — this is the only architecture all three positions can sign onto

- **The argument**: After Phase 2 cross-reviews, both competing advocates have conceded the protocol-ownership question. The LiteLLM-hybrid advocate's §9 synthesis and the a2a-future advocate's §6 concession independently arrive at the same architecture as my Phase 1 review, differing only in which concrete providers land in which week. By absorbing their concrete additions (`litellm` as a v1 Tier-3 option, `opencode` as a v1 HTTP substrate validator, the A2A triggered-commitment, the `PROVIDER_REGISTRY` runtime-extension hook), my v1 plan becomes the union of all three positions' credible deliverables. There is no competing architecture left standing; there is only one plan, and every advocate's best ideas are inside it.
- **Source**: LiteLLM-hybrid §9 synthesis (*"the synthesis takes both positions seriously… the architecture is 100% build-our-own"*). A2A-future §5 (*"Build-our-own's ExecutionProvider protocol is the correct v1 foundation for spec 042. A2A is the most important future provider within that protocol, not a replacement for it."*).
- **Evidence**: Direct quotes from both competing advocates' cross-reviews, linked above. This is not a rhetorical claim — it is a literal description of what the cross-reviews concluded.

---

## The Final v1 Implementation Plan

### The Protocol

```python
# conversus/execution/protocol.py
from __future__ import annotations
from typing import Protocol, runtime_checkable
from dataclasses import dataclass, field

@runtime_checkable
class ExecutionProvider(Protocol):
    async def execute(
        self,
        prompt: str,
        output_path: str,
        read_paths: list[str] | None = None,
        metadata: dict | None = None,
    ) -> ExecutionResult: ...

    async def execute_batch(
        self,
        tasks: list[ExecutionTask],
    ) -> list[ExecutionResult]: ...

    @property
    def name(self) -> str: ...

    @property
    def supports_tool_use(self) -> bool: ...

@dataclass(frozen=True)
class ExecutionTask:
    prompt: str
    output_path: str
    read_paths: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

@dataclass
class ExecutionResult:
    success: bool
    output_path: str
    content: str | None = None
    error: str | None = None
    duration_ms: int = 0
    provider: str = ""
    metadata: dict = field(default_factory=dict)
```

Unchanged from spec 042 §3. Pure stdlib. Zero runtime dependencies.

### The Registry (with runtime-extension hook absorbed from A2A-future)

```python
# conversus/execution/registry.py
PROVIDER_REGISTRY: dict[str, type[ExecutionProvider] | ExecutionProvider] = {}

def register_provider_class(name: str, cls: type[ExecutionProvider]) -> None:
    """Register a provider class at module import time (static registration)."""
    PROVIDER_REGISTRY[name] = cls

def register_provider_instance(name: str, instance: ExecutionProvider) -> None:
    """Register a pre-constructed provider instance at runtime.

    This hook enables A2A-style dynamic discovery: a future ACPProvider may
    discover remote agents via Agent Detail and register each as a named
    provider without requiring a new module import.
    """
    PROVIDER_REGISTRY[name] = instance

def get_provider(name: str, options: dict | None = None) -> ExecutionProvider:
    if name not in PROVIDER_REGISTRY:
        available = sorted(k for k in PROVIDER_REGISTRY.keys())
        raise ValueError(
            f"Unknown executor provider '{name}'. "
            f"Available: {available}. "
            f"Install the provider package or check spelling."
        )
    entry = PROVIDER_REGISTRY[name]
    if isinstance(entry, type):
        return entry(**(options or {}))
    return entry  # pre-constructed instance
```

### The SubprocessProvider base class

```python
# conversus/execution/subprocess_provider.py
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

@dataclass(frozen=True)
class SubprocessInvocation:
    argv: list[str]
    stdin: str | None
    cwd: Path | None
    env_overrides: dict[str, str]
    output_format: Literal["json", "stream-json", "text"]

class SubprocessProvider:
    """Base class for the subprocess-CLI-JSON backbone pattern.

    Subclasses implement three tool-specific pieces:
      - build_invocation(task) -> SubprocessInvocation
      - parse_output(stdout, stderr, returncode) -> dict
      - locate_binary() -> Path

    Shared substrate handled by the base class:
      - Binary discovery (env var, PATH, platform-specific locations)
      - Prompt marshalling (argv vs stdin, ARG_MAX handling)
      - Async subprocess lifecycle (asyncio.create_subprocess_exec)
      - Concurrent stdout/stderr streaming
      - Timeout enforcement and clean process-group kill (POSIX/Windows)
      - Error classification (binary-missing vs process-errored vs parse-failed)
      - ExecutionResult construction
      - Engine-required output_path writing when the tool only streams to stdout
      - Bounded-concurrency execute_batch with optional provider-specific pooling
    """

    @abstractmethod
    def build_invocation(self, task: ExecutionTask) -> SubprocessInvocation: ...

    @abstractmethod
    def parse_output(self, stdout: str, stderr: str, returncode: int) -> dict: ...

    @abstractmethod
    def locate_binary(self) -> Path: ...

    # ... ~350 LoC of shared lifecycle, timeout, error, and batch machinery ...
```

### The HTTPProvider base class

```python
# conversus/execution/http_provider.py
import httpx

class HTTPProvider:
    """Base class for HTTP-server-backed providers.

    Subclasses implement:
      - base_url: str | property
      - submit_task(client, task) -> task_id
      - poll_or_stream_task(client, task_id) -> result_dict

    Shared substrate:
      - Long-lived httpx.AsyncClient with connection pooling
      - Auth header construction (Bearer, API key, mTLS)
      - Retry with jittered backoff on transient errors
      - SSE / JSON-stream parsing
      - Session setup/teardown hooks
    """

    # ... ~200 LoC of shared HTTP, retry, and streaming machinery ...
```

### The v1 provider set (4 providers, ~1000–1200 LoC total)

| # | Provider | Base class | LoC (concrete subclass) | Dependency | Substrate role |
|---|---|---|---|---|---|
| 1 | `MockProvider` | Direct Protocol | ~80 | None (stdlib) | Testing, CI-fast path |
| 2 | `AnthropicProvider` | Direct Protocol (Native) | ~150 | `anthropic` | Validates `supports_tool_use=False` + engine-side file inlining |
| 3 | `ClaudeCodeProvider` | `SubprocessProvider` | ~150 | `claude` CLI on PATH | Validates subprocess substrate, backward compat with SKILL.md |
| 4 | `OpenCodeProvider` | `HTTPProvider` | ~200 | `httpx` (already widely used) | Validates HTTP substrate, cold-start-free option |

**Total v1 LoC budget**:

| Component | LoC |
|---|---|
| Protocol + data classes + registry | ~100 |
| `SubprocessProvider` base class | ~350 |
| `HTTPProvider` base class | ~200 |
| `MockProvider` | ~80 |
| `AnthropicProvider` | ~150 |
| `ClaudeCodeProvider` | ~150 |
| `OpenCodeProvider` | ~200 |
| **v1 core total** | **~1,230 LoC** |

Plus the engine-side tool-use adaptation path (pre-read files for `supports_tool_use=False`, post-write output from result content) at ~150–250 LoC.

**Grand total**: ~1,400–1,500 LoC to ship spec 042 v1. Still small in absolute terms. Still the smallest tractable path that satisfies spec 048's hard dependency and unblocks the blog pipeline.

### Optional v1 companion packages (shipped alongside, not in core)

- `conversus-provider-litellm` (~60–100 LoC, pulls in LiteLLM): recommended default for Tier-3 direct-model-API workloads when users want 100+ provider coverage without maintaining SDK glue. Absorbs the LiteLLM-hybrid advocate's strongest argument. **Optional; users who want minimum dependency footprint install `conversus-provider-anthropic` instead.**
- `conversus-provider-openai` (~150 LoC, pulls in `openai`): native direct-SDK Tier-3 option, alternative to going through LiteLLM.

### Phase 1–6 implementation plan

| Phase | Deliverable | LoC | Duration (wall time, single engineer) | Blocks |
|---|---|---|---|---|
| **Phase 1** | Protocol, data classes, registry, `MockProvider`, tool-use adaptation engine path | ~380 | 2–3 days | Unblocks all later phases and spec 048 Phase 1 |
| **Phase 2** | `AnthropicProvider` (native SDK, `supports_tool_use=False` path validated) | ~150 | 1–2 days | Proves Tier-3 native path, unblocks blog pipeline for non-tool workloads |
| **Phase 3** | `SubprocessProvider` base class | ~350 | 3–4 days | Blocks all subprocess providers (claude-code, aider, copilot, gemini-cli, etc.) |
| **Phase 4** | `ClaudeCodeProvider` (on `SubprocessProvider`, direct `claude -p --bare`, no claude-agent-sdk) | ~150 | 2–3 days | Backward compat with SKILL.md flows, unblocks spec 048 governance runs against Claude Code |
| **Phase 5** | `HTTPProvider` base class + `OpenCodeProvider` (against OpenAPI 3.1) | ~400 | 3–4 days | Cold-start-free option for high-fanout workloads, validates HTTP substrate before A2A |
| **Phase 6** | Migration of SKILL.md to use `ClaudeCodeProvider` through the Protocol, FR-009/010/011 backward-compat tests, spec 042 §11 rename (`acp` → `a2a`, add `zed-acp` row) | ~50 + docs | 2–3 days | Closes spec 042. Spec 048 unblocks immediately after. |
| **Total** | v1 shipping | ~1,480 | **~13–19 working days** | |

Post-v1 phases (not in scope for spec 042 v1, but additive under the same Protocol):

- **v1.1**: `conversus-provider-litellm` optional package (~80 LoC). Ships the same week as Phase 6 or right after.
- **v1.2**: `AiderProvider`, `CopilotCLIProvider`, `GeminiCLIProvider` as `SubprocessProvider` subclasses (~80–120 LoC each).
- **v2**: `A2AProvider` (`HTTPProvider` subclass wrapping `a2a-sdk`) when the triggered precondition is met — at least 3 of {Claude Code, Aider, OpenCode, Copilot, Codex, Gemini} ship A2A endpoints.
- **v2+**: Post-042 ecosystem contribution — `conversus-a2a-server-for-claude`, a standalone PyPI package that exposes `ClaudeCodeProvider` behind an A2A server, reusable by any A2A client in the world. High-leverage community investment; explicitly not v1.
- **Future**: `zed-acp` integration (separate, IDE-facing track, appropriate for a future spec).
- **Workflow orchestrators** (`gh-aw`, `langgraph`, `temporal`, `gsd`): each gets a `WorkflowProvider` or equivalent substrate when demand arrives. Not v1.

### What happens to A2A and LiteLLM in this architecture

The one-sentence answer: **both become providers inside this plan.**

- **LiteLLM** is a Tier-3 `NativeProvider`-style adapter at ~14–60 lines of code, shipped as the optional `conversus-provider-litellm` package. It is the recommended Tier-3 default for users who want 100+ model coverage without writing SDK glue per vendor. It coexists with the native `AnthropicProvider` in v1; users pick based on their dependency preferences. The LiteLLM-hybrid advocate's §9 synthesis **is** this arrangement.

- **A2A** is a `HTTPProvider` subclass that will ship when the ecosystem produces counterparties — at least 3 of {Claude Code, Aider, OpenCode, Copilot, Codex, Gemini} must have A2A server wrappers (from vendors, community, or conversus itself). Until that trigger, `a2a` stays in spec 042 §11 as a first-class row with "Status: awaiting counterparties." When the trigger fires, `a2a` becomes the recommended path for agent-to-agent composition. The a2a-future advocate's §5 revised position **is** this arrangement.

Neither is a competitor to build-our-own. Both are providers. That is the whole point of owning the Protocol: every interesting thing that happens in the agentic ecosystem maps to an additive adapter inside this architecture, and the engine is insulated from ecosystem churn forever.

---

## Updated Risk Profile

### Risks confirmed by competitors (strengthens credibility)

- **Subprocess cold-start is real and load-bearing for high-fanout workloads** (backbone-researcher §4.3). Confirmed as a real performance tax on the `claude-code` path. **Mitigation in v1 plan**: `opencode` via `HTTPProvider` ships in v1 as the cold-start-free alternative, giving users a choice based on their workload profile. This mitigation was added in direct response to the researcher's observation.

- **`claude-agent-sdk` is alpha and adds dependencies for zero architectural benefit** (backbone-researcher §4.1). Confirmed. **Mitigation in v1 plan**: dropped from the plan entirely. `ClaudeCodeProvider` goes direct-to-CLI via `claude -p --bare`. This removes a risk my original review carried.

- **The ACP/A2A terminology conflation is a spec-hygiene bug** (backbone-researcher §3.2). Confirmed. **Mitigation in v1 plan**: spec 042 §11 row rename from `acp` to `a2a`, with a separate `zed-acp` row added. This correction is absorbed into the final v1 plan.

- **No coding agent ships an A2A server wrapper in 2026-04** (backbone-researcher §9, a2a-future §2 concession). Confirmed, and confirmed to be fatal for A2A-first. **Mitigation in v1 plan**: A2A is a triggered roadmap commitment, not a v1 dependency. The v1 path is insulated from A2A ecosystem timing.

### New risks raised by competitors (addressed in v1 plan)

- **Mock test-suite migration is not enumerated** (self-raised in my cross-review §5.1). The claim that `mock` stabilizes 3,428 tests was under-specified. **Mitigation**: downgraded claim to "replaces ad-hoc agent mocking with a protocol-typed test double." Full migration enumeration is an implementation detail surfaced during Phase 1, not a pre-v1 blocker.

- **The LoC estimate was ~2x low for `claude-code`** (backbone-researcher §2.3). **Mitigation**: corrected in this revision. New total ~1,230 LoC core + ~150–250 engine-side tool-use adaptation. Still tractable; still the smallest path to a shipping spec 042.

- **Engine-side tool-use adaptation is non-trivial** (self-raised in my cross-review §5.2). Spec 042 §4 lines 268–290's inline-and-post-write logic is ~150–250 LoC on the engine side, not the provider side. **Mitigation**: priced into the Phase 1 LoC budget above. Validated end-to-end by `AnthropicProvider` in Phase 2 before any subprocess provider lands.

### Risks mitigated during cross-review

- **"Are we reinventing the wheel?"** — verified dead by the backbone researcher and conceded by both advocates. There is no wheel. There are only half-wheels from different vehicles. Our job is to build an axle.

- **"Is A2A a better foundation than build-our-own?"** — conceded by the a2a-future advocate, who now agrees A2A is the most important future provider inside build-our-own's Protocol, not a replacement for it.

- **"Is LiteLLM a better foundation than build-our-own?"** — conceded by the LiteLLM-hybrid advocate, whose Week 1 plan explicitly builds spec 042 §3 "conversus code, not LiteLLM" and whose §10 says "the build-our-own advocate wrote a better review than I did on the protocol-ownership question."

- **"Will the protocol need to change when the ecosystem evolves?"** — no. The protocol is a minimal in-process Python interface. Every ecosystem shift (A2A maturing, new coding agents shipping, LiteLLM API changes, MCP evolving) is absorbed at the adapter layer. This is the core of the forward-compatibility argument and it was not challenged in any cross-review.

### Residual risks (acknowledged, not eliminated)

- **Copilot CLI's headless surface is underdocumented** (backbone-researcher §12). Not a v1 risk (Copilot isn't in v1), but a confidence downgrade on the future §11 matrix row. Documented; revisit before committing to a `CopilotCLIProvider`.

- **The `gh-aw` provider requires a third base class shape** ("emit workflow YAML, trigger Actions, poll results"). Not `SubprocessProvider`, not `HTTPProvider`. A future `WorkflowProvider` base class (~150–250 LoC) is needed when that provider lands. Acknowledged; explicitly not v1.

- **Spec 048's autonomous-governance workloads may expose subprocess cold-start costs at scale** once real users fan out to 30+ parallel phases. Acknowledged. `opencode` in v1 gives those users an escape hatch; `a2a` will give them another when counterparties exist; future process-pooling optimizations in `SubprocessProvider` are available if needed.

---

## Bottom line for Phase 4+

Build the protocol. Ship the four v1 providers (`mock`, `anthropic`, `claude-code` via direct CLI, `opencode` via HTTP). Factor out `SubprocessProvider` and `HTTPProvider` as the two substrate base classes the ecosystem has already converged on. Add `LiteLLMProvider` as an optional companion package the same week or immediately after. Keep `a2a` as a first-class row in spec 042 §11 with a triggered commitment to elevate it when counterparties exist. Rename the spec's `acp` references to disambiguate A2A from Zed/JetBrains ACP.

All three Phase-1 positions agree on the architecture. The LiteLLM-hybrid advocate conceded protocol ownership and renamed their position to "build our own + LiteLLM as one Tier-3 provider." The a2a-future advocate conceded their central position and renamed theirs to "A2A as the most important future provider within build-our-own's protocol." The backbone researcher verified the core structural claim and corrected the cost estimate without touching the architectural conclusion.

**Total v1 cost**: ~1,400–1,500 LoC, ~13–19 working days, zero mandatory runtime dependencies beyond `httpx` (already widely used).

**What unblocks**: spec 048 (autonomous governance), the blog pipeline, every headless-execution use case, every future provider in spec 042 §11, and the ecosystem contribution opportunity (conversus as the first team to wrap Claude Code as an A2A server).

**What we refuse**: bending the internal Python Protocol to match any external wire format, any framework abstraction, or any ecosystem timeline we do not control.

Recommendation: **adopt the revised v1 plan as the winning architecture**. It is the only plan all three advocates can sign onto, and it is the only plan that ships in the calendar spec 048 requires.
