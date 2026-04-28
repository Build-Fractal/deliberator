# Cross-Review: Backbone Researcher's Report

**Reviewer**: build-our-own-advocate
**Target**: backbone-researcher's factual ground-truth report
**Round**: 1 / Phase 2 (cross-review)
**Stance**: The research substantially validates the build-our-own position, but also surfaces genuine weaknesses in my v1 plan that I need to fix.

---

## 0. Verdict up front

The researcher's report is the strongest possible piece of evidence for build-our-own — not because the researcher was trying to help me (they explicitly avoided advocacy), but because the ground truth is unusually clean: **no library exists that can be the `ExecutionProvider`, and the only universal backbone is "spawn a CLI, pass a prompt, read JSON output."**

That fact transforms my argument from "our abstraction is better" to "our abstraction is the only one that can exist at this point in the ecosystem." It also forces me to fix two mistakes in my original review:

1. I underestimated how much shared machinery every adapter needs. "100–200 lines per adapter" is right for the business logic, but the researcher's report reveals a common substrate (subprocess lifecycle, stdin marshalling, JSON stream parsing, stderr capture, timeout handling, cold-start amortization) that should NOT be duplicated N times. The protocol design needs a `SubprocessProvider` base class, not just a bare `Protocol`.
2. I referenced `claude-code` as a v1 provider without being specific about *how* it dispatches. The researcher proves the "Node bridge" framing is wrong and the in-session `Agent` tool is not externally addressable. The v1 `ClaudeCodeProvider` has to be `claude -p --bare` subprocess from day one — no SDK wrapping, no Node layer.

With those corrections, the build-our-own plan gets *more* defensible, not less. But it also gets more opinionated about what ships in v1.

---

## 1. Where the research validates the build-our-own position

I will cite specific findings, with section/line references from the researcher's report.

### 1.1 Every alternative requires the same adapter work — validated

The researcher's §7 (Is there a common pattern?) and §10 (Verified mapping table) are devastating to the "adopt a framework" counter-arguments:

- **LiteLLM**: confirmed to cover only the model-API layer, not agent runtimes. Researcher §7 table: "Model API — Yes (LiteLLM). … Agent ↔ agent — Emerging (A2A) — Framework integrations only; no major SDK ships an A2A server wrapper of itself yet."
- **MCP**: researcher §8, verbatim: *"MCP is not the right layer, and this is unambiguous."* It is model→tool, not agent→agent. The researcher explicitly rules it out as a candidate for the execution provider layer.
- **A2A**: researcher §9: protocol v1.0.0 is less than a month old (2026-03-12), Python SDK is 0.3.25 stable / 1.0.0a0 alpha, and **no shipping coding agent has been wrapped as an A2A server yet**. The wire exists; the counterparties do not.
- **Zed/JetBrains Agent Client Protocol**: researcher §6.3 — a *different* protocol, designed for IDE-to-agent with human-in-the-loop approval, explicitly not for headless CI.

This directly validates my §2.6 argument ("nobody else does both"). The researcher, working from first principles with no advocacy goal, independently arrived at the same conclusion I argued for: there is no unifying abstraction available to adopt. My original claim was "the wheel doesn't exist" — the researcher's report is the x-ray.

### 1.2 The Claude Code "Node bridge" framing is wrong — validated (and I need to fix my v1 plan)

Researcher §1.2 and §11 observation 8 are precise:

> *"The `@anthropic-ai/claude-agent-sdk` is itself a subprocess wrapper around the `claude` CLI binary. From Python you are not avoiding subprocess by calling the TS SDK — you are adding a Node layer between your Python and a CLI subprocess. Go straight to `claude -p --bare` from Python."*

And the Python SDK (§1.2):

> *"The SDK spawns a subprocess running the bundled `claude` CLI binary. It does not call the Anthropic /v1/messages API directly."*

**This validates my core claim that the execution-provider layer is inherently adapter shaped** — but it also corrects me: `claude-agent-sdk` Python is not a "library integration," it is a subprocess wrapper we would be re-wrapping. Using it from Python buys us nothing over `subprocess.run(["claude", "-p", prompt, "--bare", ...])`. It adds a dependency (and the SDK is still marked "Alpha") for no architectural gain.

My v1 plan said "`claude-code` (`claude-agent-sdk` OR subprocess — zero new deps)". The researcher proves these are the same thing with extra steps. I need to pick one: **direct subprocess**.

### 1.3 The in-session `Agent` tool is not a protocol — validated, and this is the spec's entire motivation

Researcher §1.4, responding to "is the `Agent` tool exposed externally?":

> *"This tool is only usable from within a Claude session — it is invoked by the model via tool_use blocks. It is not a standalone API endpoint."*

And §11 observation 1:

> *"The SKILL.md's current dispatch primitive (Claude's `Agent` tool with `run_in_background`) is not portable. It only exists inside a live Claude Code session. Any execution-provider abstraction that claims to support 'running headless' must replace it with one of: (a) `claude -p --bare` subprocess, (b) `claude-agent-sdk.query()` (which itself subprocesses), or (c) something else entirely."*

This is the factual basis for spec 042 existing at all. Conversus today runs inside Claude Code and relies on a tool that only exists in that specific process context. Every time spec 048 (autonomous governance) is mentioned, this is the concrete coupling it has to break. The researcher doesn't argue for or against any position — they simply state that **the current dispatch is not reusable outside its host**. That is the entire problem the ExecutionProvider protocol solves.

### 1.4 The de facto backbone IS "subprocess + CLI + JSON" — validated

Researcher §7, table row "Headless CLI invocation":

> *"**De facto** (subprocess + flags + JSON output). Every shipping agentic coding tool supports this: `claude -p --output-format json`, `aider --message`, `opencode` CLI, `copilot` CLI, `codex` CLI, `gemini` CLI, `cn` for Continue."*

And §11 observation 2:

> *"The most portable, lowest-risk backbone today is 'spawn a CLI and read JSON output.' Every shipping agentic coding tool supports this. It's ugly, it's per-task process overhead, but it is the one thing that actually works across Claude Code, Aider, OpenCode, Copilot, Codex, Gemini, and Continue today."*

This is the single most important finding in the whole report for my position, and it changes how I should write the v1 plan (see §3 below). If every shipping agent supports the exact same "subprocess + `-p` / `--message` + JSON output" pattern, then that pattern is the right thing to factor out of the protocol and into a shared base class. It is the actual common substrate of the execution provider layer, and it already exists — not as a library, but as a convergent convention across unrelated vendors.

### 1.5 OpenCode is the lone HTTP exception — validated, and it's a strategic asset

Researcher §2.2:

> *"OpenCode is a proper HTTP server by design. … `opencode serve [--port <number>]` … Default port 4096. Exposes OpenAPI 3.1 spec at `http://<host>:<port>/doc`."*

And the clincher, §2.4:

> *"'Can conversus just HTTP POST to a locally-running OpenCode server?' Yes, literally."*

This means my spec 042 §11 provider matrix has **two fundamentally different provider shapes**, not one:

1. **Subprocess providers** (claude-code, aider, copilot, codex, gemini, continue) — share a substrate.
2. **HTTP providers** (opencode today, a2a tomorrow) — share a different substrate.

I did not make this distinction clearly enough in my original review. The protocol still collapses both under one `ExecutionProvider` interface (that's the whole point), but the *implementation* has two base classes. I'll enumerate them in §3.

### 1.6 A2A terminology is a spec bug, and the research fixes it

Researcher §6 is a clean correction to spec 042's language. The spec uses "ACP" for both IBM→A2A (agent-to-agent) and Zed/JetBrains Agent Client Protocol (IDE-to-agent). These are different protocols with different threat models and different use cases. The researcher explicitly recommends renaming the `acp` provider in spec 042 §11 to `a2a` and treating Zed/JetBrains ACP as a separate, future, IDE-facing integration.

I didn't flag this in my original review; I should have. The terminology fix strengthens my position because it clarifies that the A2A-future counter-argument is actually a bet on one specific protocol (A2A/LF-governance), not on "the ACP standard," and that protocol is still early. My §3.4 "wait for A2A" rebuttal was right in substance but imprecise in naming; the researcher's fix sharpens it.

---

## 2. Did I underestimate adapter complexity?

**Yes, partially.** My original review cited the research doc's "100–200 lines per adapter" figure and used it to argue that total v1 code is ~500–700 lines. That number is right for each adapter's *unique* code. It is wrong if the adapters duplicate substrate work.

The researcher's §11 table and §7 expose exactly what the subprocess substrate has to do, because it's the same across every tool:

1. Locate the CLI binary (env var, PATH search, override).
2. Spawn it with the correct flags for headless mode (`-p` / `--message` / etc.), JSON output (`--output-format json` / `--bare` / etc.), allowed tools, working directory, timeouts.
3. Marshal the prompt to stdin or argv (tool-specific).
4. Stream stdout JSON, parse per-tool schema, capture stderr for errors.
5. Handle the tool-specific failure modes the researcher enumerates (`CLINotFoundError`, `CLIConnectionError`, `ProcessError`, `CLIJSONDecodeError` for claude; unsupported-version warnings for aider; etc.).
6. Handle the cold-start cost the researcher calls out in §11 observation 10: *"subprocess-spawning Claude Code has a cold-start cost (typically ~1–3 seconds for the CLI to boot, load plugins/hooks/MCP servers). `--bare` exists specifically to cut this. For a conversus run with 10–30 parallel agent phases, this adds up."*
7. Enforce the engine's tool-use adaptation (spec 042 §4 lines 268–290) for providers that don't natively have tool use.
8. Attribute the output to the engine-chosen `output_path` (either via tool use or by post-writing the content dict).

If every adapter reimplements this, we have the same problem the `BaseIntegrator` architecture already warned about in the monorepo's apm skill guidance (@apm/src/apm_cli/integration/ design philosophy: "One base, many file types"). Duplicating infrastructure across adapters produces drift, bugs, and performance regressions.

**Corrected estimate for v1**: protocol + data classes + registry (~80 lines) + `SubprocessProvider` base (~250–400 lines, because it has to be *good*) + `HTTPProvider` base (~150–250 lines, stub for v2 OpenCode) + `mock` provider (~80 lines) + `anthropic` provider (~120 lines) + `ClaudeCodeProvider` concrete subclass on top of `SubprocessProvider` (~150 lines). **Total: ~800–1100 lines.**

That's still small. It's still less than one Django admin class in this monorepo. But it's ~60% larger than the number I quoted, and I should own the correction publicly rather than let it be a "gotcha" the other advocates can spring.

The tradeoff is good: 400 lines of shared substrate that every future provider inherits is a far better investment than 400 lines of substrate duplicated across five providers. This is the same calculus as `BaseIntegrator` — infrastructure belongs in one place.

---

## 3. `SubprocessProvider` as the default implementation

Yes. The researcher's finding directly implies this, and it is the single most valuable change to my v1 plan.

### 3.1 Why it has to exist

The researcher's §7 and §11 together make the case: *every production coding agent is a subprocess with flags*. That is not a failure of the ecosystem — it is a stable convention that has emerged because it's the simplest thing that works. If we don't factor it out, every adapter author has to rediscover:

- How to find the binary (check env var `CLAUDE_CLI_PATH`, then `$PATH`, then platform-specific install locations)
- How to marshal a prompt safely (argv vs stdin; handling prompts > ARG_MAX)
- How to stream JSON output without blocking (asyncio streams, line-buffered vs chunked)
- How to enforce timeouts and kill runaway processes cleanly (process groups on POSIX, `taskkill /T` on Windows)
- How to distinguish CLI-missing errors from CLI-errored errors from output-parse errors
- How to translate the tool's output format into the engine's `ExecutionResult` fields
- How to write the engine-required `output_path` when the tool only streams to stdout

All of this is invariant across Claude Code, Aider, Copilot CLI, Codex CLI, Gemini CLI, Continue's `cn`, and even `opencode` (as a CLI fallback to its HTTP server).

### 3.2 Proposed base class shape

```python
# conversus/execution/subprocess_provider.py
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class SubprocessInvocation:
    argv: list[str]
    stdin: str | None
    cwd: Path | None
    env_overrides: dict[str, str]
    output_format: Literal["json", "stream-json", "text"]

class SubprocessProvider(ExecutionProvider):
    """Base class for the 'spawn a CLI, read JSON output' backbone pattern.

    Subclasses implement the three tool-specific pieces:
    - build_invocation(task) -> SubprocessInvocation
    - parse_output(stdout, stderr, returncode) -> dict
    - locate_binary() -> Path

    Everything else (process lifecycle, timeouts, error classification,
    output_path writing, tool-use adaptation, cold-start amortization hooks,
    cancellation) is handled by the base class.
    """

    @abstractmethod
    def build_invocation(self, task: ExecutionTask) -> SubprocessInvocation: ...

    @abstractmethod
    def parse_output(self, stdout: str, stderr: str, returncode: int) -> dict: ...

    @abstractmethod
    def locate_binary(self) -> Path: ...

    async def execute(self, prompt, output_path, read_paths=None, metadata=None):
        # Shared: build ExecutionTask, resolve binary, spawn subprocess with
        # timeout from metadata, stream stdout, capture stderr, parse output,
        # write content to output_path if tool didn't write it, classify errors,
        # return ExecutionResult. ~250-400 lines of carefully tested code.
        ...

    async def execute_batch(self, tasks):
        # Shared: asyncio.gather with bounded concurrency from metadata.
        # Subclasses can override to implement process pooling / cold-start
        # amortization if their tool supports it.
        ...
```

### 3.3 What each concrete provider contributes

| Provider | LoC for subclass | Unique work |
|---|---|---|
| `ClaudeCodeProvider(SubprocessProvider)` | ~120 | `claude -p --bare --output-format json --allowedTools ... --agents ...` invocation building, claude CLI JSON output schema parsing, plugin/MCP config passthrough |
| `AiderProvider(SubprocessProvider)` | ~100 | `aider --message ... --yes --no-pretty` invocation, stdout parsing (aider doesn't produce JSON by default; subclass may need `--stream` off and regex-extraction or subprocess a tiny Python shim) |
| `CopilotCLIProvider(SubprocessProvider)` | ~100 | `copilot ...` invocation (researcher §12 flags headless flag surface as underdocumented — may require more investigation) |
| `GeminiCLIProvider(SubprocessProvider)` | ~80 | `gemini ...` invocation |
| `ContinueCLIProvider(SubprocessProvider)` | ~80 | `cn` invocation — but note researcher §5.2: "the abstraction is 'check files' not 'dispatch arbitrary tasks'" — may not fit the task model cleanly |

Each concrete provider becomes a **narrow, tool-specific transform** from conversus's `ExecutionTask` to that tool's argv/stdin/output schema. All error handling, process management, timeout logic, output-path writing, and ExecutionResult construction stays in `SubprocessProvider`. That is the "one base, many file types" principle from the monorepo's apm integrator guidance, applied to execution providers.

### 3.4 Complementary base class: `HTTPProvider`

For OpenCode (researcher §2.2) and future A2A (researcher §9), there's a second shared substrate: long-lived HTTP connections, session management, SSE or JSON streaming, auth, retries, connection pooling. This is also ~150–250 lines once, and used by `OpenCodeProvider` and `A2AProvider`. It does not belong in `SubprocessProvider`.

The protocol sits above both:

```
ExecutionProvider (Protocol)
├── SubprocessProvider (base class)
│   ├── ClaudeCodeProvider
│   ├── AiderProvider
│   ├── CopilotCLIProvider
│   ├── GeminiCLIProvider
│   └── ContinueCLIProvider
├── HTTPProvider (base class)
│   ├── OpenCodeProvider
│   └── A2AProvider  (future)
└── NativeProvider (mock, anthropic-direct-api, openai-direct-api)
```

`NativeProvider` isn't really a base class — it's the residual category for providers that don't share a substrate (e.g., calling `anthropic.AsyncAnthropic().messages.create()` directly in ~80 lines doesn't benefit from inheritance; it just implements `ExecutionProvider` directly).

---

## 4. Changes to the v1 plan

My original v1 was "`mock` + `anthropic` + `claude-code`". The research forces three specific updates:

### 4.1 Drop the `claude-agent-sdk` option for `claude-code`

Original v1 language: *"`claude-code` — `claude-agent-sdk` OR subprocess (zero new deps)"* (my review §2.2 table).

**Corrected**: `ClaudeCodeProvider` is a direct subclass of `SubprocessProvider`. It invokes `claude -p --bare --output-format json --allowedTools ... --agents ...`. It does NOT depend on `claude-agent-sdk` Python. Rationale (researcher §11 obs. 8): the SDK is itself a subprocess wrapper, marked Alpha, and adds a dependency for zero architectural benefit. Skipping it removes a dependency AND a failure mode (the bundled CLI binary issue at researcher §1.2: *"platform-specific wheels ship prebuilt CLI binaries"*).

### 4.2 v1 needs `SubprocessProvider` + `HTTPProvider` base classes, not just the protocol

Original v1 implied we ship the `ExecutionProvider` Protocol and providers inherit directly. **Corrected**: v1 ships the Protocol AND `SubprocessProvider` AND a stub `HTTPProvider` (the stub is important because it locks in the shape before OpenCode/A2A providers land, preventing future drift).

### 4.3 Add `opencode` as a v1 or v1.1 provider — reconsider the cut list

Researcher §2.4 establishes that OpenCode has a real HTTP API today, with an OpenAPI 3.1 spec, and that a Python client is ~100 lines via `httpx` against the spec. This is the one provider in the matrix that is *architecturally superior* to the subprocess baseline (no cold start, native streaming, long-lived session — see researcher §11 obs. 10).

I did not include OpenCode in v1 originally because I was optimizing for "tools we know we use today." The research suggests OpenCode should be v1.1 at latest, and possibly v1, because:

- It validates the `HTTPProvider` base class early (before A2A, which is still alpha).
- It proves the protocol works across both substrates before we commit to 5+ subprocess providers.
- It gives us a cold-start-free benchmark to compare against the subprocess-based `ClaudeCodeProvider`.

**Revised v1 set**: `mock`, `anthropic` (direct API), `claude-code` (via `SubprocessProvider`), `opencode` (via `HTTPProvider`). Four providers, two substrate base classes, one protocol. Still small; better coverage of the design space.

### 4.4 Rename the future `acp` provider to `a2a`

Researcher §6 fixes the spec's ambiguity. The §11 matrix row currently labeled `acp` should be renamed `a2a` and documented as "JSON-RPC 2.0 over HTTP via `a2a-sdk`, Python ≥3.10." Zed/JetBrains ACP becomes a separate, future row labeled `zed-acp` or similar, with a different use case (IDE integration).

### 4.5 Document the cold-start tradeoff in the spec

Researcher §11 obs. 10 is important and not currently in spec 042: subprocess providers pay 1–3 seconds of cold start per invocation, and `--bare` exists specifically to cut this. For a conversus deliberation with 20–30 parallel phases, that's 20–90 seconds of cumulative startup overhead on subprocess providers. HTTPProvider-based providers avoid it entirely.

This should appear in spec 042 §11 as a column ("Cold start per call") and be part of the provider selection guidance. It does not change the build-our-own conclusion, but it makes the `opencode`/`a2a` providers more clearly attractive for high-fanout deliberation workloads.

---

## 5. Weaknesses the research reveals in my position

Honest accounting.

### 5.1 The "mock provider stabilizes 3,428 tests" claim is under-specified

My §2.5 argument asserted that a `mock` provider makes the test suite provider-independent. The research doesn't contradict this, but it also doesn't validate it — because the research doesn't look at conversus's test suite at all. I stated this as a benefit, but I haven't done the work to verify:

- How many of the 3,428 tests actually dispatch an agent vs. test template rendering / phase logic / markdown parsing?
- How many will need to be rewritten to hit `mock` vs. just swapped by config?
- What does `mock` need to return to satisfy existing test assertions about phase output shape?

This is a real gap. The mock provider is still a good idea, but I should tone down "stabilizes 3,428 tests" to "provides a clean substitute for the current ad-hoc agent mocking patterns, with an enumerable migration of test files."

### 5.2 I handwaved "tool-use adaptation" in §4

Spec 042 §4 lines 268–290 describe how the engine inlines file contents for providers that don't support tool use (`supports_tool_use=False`). I cited this as "the engine handles it" — which is true, but the research reveals the engine-side complexity I glossed over:

- For `AnthropicProvider` (direct API, no tool use), the engine has to read all `read_paths`, inline them into the prompt with format markers, then parse the model's response for the intended output file, then write it to `output_path`. That's a non-trivial transform.
- For `ClaudeCodeProvider` (via `SubprocessProvider`, CLI has tool use), the engine passes `read_paths` as allowed-files flags and the CLI does the reading. Different path entirely.

The protocol hides this dichotomy well, but the *engine* has to know which mode each provider is in, and the inline-and-parse path is its own implementation surface that needs tests. I didn't price that into my 500–700 LoC estimate. (It's roughly another 150–250 LoC on the engine side, not the provider side — so it doesn't inflate the provider layer, but it does inflate "total code to ship spec 042".)

### 5.3 The "100–200 lines per adapter" number came from the previous research doc, not from this report

The researcher's §10 table gives tool-by-tool dispatch strategies but doesn't estimate LoC. The "100–200 lines" figure I cited was from the earlier tool-landscape.md doc, not this new ground-truth report. With the `SubprocessProvider` factoring in §3 above, the per-concrete-provider LoC drops to ~80–150 — but the shared substrate pulls the overall total up. Net total is still small, but I should stop quoting the "100–200 per adapter" number as if it came from the research the other agents are reading; they'll check.

### 5.4 I was too dismissive of A2A adoption risk as an *opportunity*

My §3.4 framed A2A as "we can add it later when the ecosystem matures." That's correct, but I didn't acknowledge the flip side: if conversus ships an A2A provider early and contributes Claude Code / Aider / OpenCode A2A server wrappers to the ecosystem, conversus becomes a non-trivial player in establishing the counterparties the researcher §9 notes don't yet exist. That's a strategic opening, not just a risk. It doesn't change the v1 decision, but my argument should acknowledge it as a v2+ opportunity rather than framing A2A purely defensively.

### 5.5 Copilot CLI is underdocumented — my provider matrix overstates certainty

Researcher §12 gap: *"GitHub Copilot CLI's actual headless/JSON-output surface is less well-documented publicly than `claude -p`; my understanding of its capabilities is limited to 'it exists, gh-aw uses it as an engine'."*

My provider matrix in the original review treated `copilot` as a first-class subprocess-provider target. The researcher's flag means I should downgrade it to "exploratory — verify headless surface before committing." This doesn't affect v1 (Copilot isn't in v1 anyway), but it affects the spec 042 §11 matrix confidence level.

### 5.6 The `gh-aw` provider is a different animal and I didn't distinguish it

Researcher §4.5: *"gh-aw is a legitimate execution surface — a `gh-aw` provider for conversus would emit lock.yml files and dispatch workflow runs. But it is not an agent runtime conversus can embed."*

This means a `GhAwProvider` in spec 042 §11 does not fit either `SubprocessProvider` or `HTTPProvider` — it's a third shape: "emit YAML, trigger GitHub Actions, poll for results." I treated it as just another row in the matrix. It actually requires a third (small) substrate: `WorkflowProvider` or `DispatchProvider`. For v1 this is irrelevant, but for the full §11 matrix, there are **three** base classes, not two.

---

## 6. Net effect on the deliberation

The research strengthens the core build-our-own thesis and kills both counter-positions harder than I originally argued:

- **LiteLLM-hybrid** is now provably a subset: it covers only direct-model-API providers (which, in my revised taxonomy, don't even inherit from either base class — they're `NativeProvider`s), and the research confirms LiteLLM cannot dispatch to any of the subprocess-backed coding agents. "Use LiteLLM for Tier 3" is still fine — it becomes a ~100-line `LiteLLMProvider: NativeProvider` adapter at our discretion. It is not a substitute for the protocol.
- **A2A-future** is now provably early: v1.0.0 one month old, SDK 0.3.25 stable, zero coding-agent counterparties. Waiting means shipping nothing. Adopting means writing the counterparties ourselves, which is identical to the subprocess adapters we're writing either way.
- **Build-our-own** gains two new concrete artifacts from the research: `SubprocessProvider` base class (fills the ecosystem's de facto backbone pattern) and the A2A terminology fix. Both make the protocol proposal more concrete and more implementable.

The weaknesses in my argument are mostly about scope honesty (total LoC, engine-side complexity, mock test migration) and not about the fundamental structure. The structure is right. The v1 plan needed sharpening.

---

## 7. Revised bottom-line recommendation

Unchanged in direction, sharpened in detail:

**Adopt spec 042's `ExecutionProvider` Protocol as specified. Ship v1 as:**

1. **Protocol + data classes + registry** (`~80 LoC`)
2. **`SubprocessProvider` base class** — new, factored from the researcher's §7 finding that subprocess-CLI-JSON is the de facto backbone across all coding agents (`~300–400 LoC`)
3. **`HTTPProvider` base class (stub)** — new, to lock in the shape before OpenCode/A2A land (`~150 LoC`)
4. **`mock` provider** (`~80 LoC`)
5. **`AnthropicProvider`** (direct API, NativeProvider-style, `~120 LoC`)
6. **`ClaudeCodeProvider(SubprocessProvider)`** via `claude -p --bare --output-format json`, NOT via `claude-agent-sdk` Python (`~150 LoC`)
7. **`OpenCodeProvider(HTTPProvider)`** via `httpx` + the OpenAPI 3.1 spec against `opencode serve` (`~200 LoC`)

**Total v1**: ~1,000–1,200 LoC. Four concrete providers, two substrate base classes, one protocol. Zero mandatory dependencies in core conversus beyond `httpx` (already widely used). Every provider in spec 042 §11 is an incremental subclass from here.

**Terminology fix**: rename the spec-042 §11 `acp` row to `a2a`; add a separate `zed-acp` row for IDE integration.

**Spec text additions**:
- A "cold start per call" column in the §11 matrix (researcher §11 obs. 10).
- A note that `ClaudeCodeProvider` MUST go direct-to-CLI, not through `claude-agent-sdk` (researcher §11 obs. 8).
- An explicit statement that the "Agent tool with `run_in_background`" pattern in SKILL.md is not portable and must be replaced (researcher §11 obs. 1).

**Recommendation stands**: build our own. The research didn't just fail to find a library we should adopt — it proved one cannot exist in the current ecosystem, because the thing we need (a unifying adapter layer across two substrates and three dispatch shapes) is exactly what nobody else has built. We build the axle. The wheels are already there, vendor by vendor.
