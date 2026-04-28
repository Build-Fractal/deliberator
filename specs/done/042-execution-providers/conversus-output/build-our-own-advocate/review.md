# Build Our Own ExecutionProvider Protocol — Advocate Review

**Position**: Conversus should define and ship its own minimal `ExecutionProvider` protocol (as already specified in spec 042 §3) and implement the providers we care about as thin adapters on top of it. External SDKs — `anthropic`, `claude-agent-sdk`, `litellm`, future ACP/A2A clients — live at the adapter layer, never at the protocol layer.

**Round**: 1 / Phase 1 (winner-take-all)

---

## 1. The core claim

Spec 042 already defines the right shape. It is ~40 lines of Protocol, two dataclasses, and a registry:

```python
@runtime_checkable
class ExecutionProvider(Protocol):
    async def execute(self, prompt: str, output_path: str,
                      read_paths: list[str] | None = None,
                      metadata: dict | None = None) -> ExecutionResult: ...
    async def execute_batch(self, tasks: list[ExecutionTask]) -> list[ExecutionResult]: ...
    @property
    def name(self) -> str: ...
    @property
    def supports_tool_use(self) -> bool: ...
```

(Spec 042 §3, lines 108–176.)

That protocol — `prompt`, `read_paths`, `output_path`, `metadata` → `ExecutionResult` — is **exactly** the surface conversus needs and **nothing more**. It is the distilled API of the phase dispatch that already exists in SKILL.md today. The engine already doesn't care about the runtime (spec 042 §2: *"The engine already doesn't care"*, lines 98–104). All we have to do is name the interface it is already using.

The alternative approaches — "just adopt LiteLLM" and "wait for A2A/ACP to mature" — both force conversus to take on either someone else's abstraction or someone else's timeline. Neither of those is a good trade when the thing we actually need is a 4-field dataclass.

---

## 2. Why this is the right call (six direct arguments)

### 2.1 Control: the protocol is exactly what conversus needs

Conversus phases have a very specific shape:

1. A fully-rendered template prompt (variables substituted by the engine).
2. A list of files the agent should read (targets + docs + per-phase inputs).
3. An absolute output path (the engine decides where outputs go — it must, because phases depend on deterministic paths).
4. Phase metadata (`phase`, `agent_name`, `mode`, `round`, `timeout`) — spec 042 §3 lines 136–145.

This is **not** the shape of a chat completion. It is not the shape of an Agent-with-roles (CrewAI). It is not the shape of a LangGraph StateGraph node. It is not the shape of a LiteLLM `completion_async` call. It is *our* shape, and the engine is already built around it.

When you adopt someone else's abstraction, you inherit an impedance mismatch at every call site — you're constantly translating between their concepts and yours. Spec 042's protocol is the minimum viable contract between the phase engine and whatever runs the agent. It does not include irrelevant concepts like "role", "goal", "graph node", "chat history", or "tool schema". It includes exactly the four things the engine gives a provider and the two things the engine needs back.

### 2.2 Zero runtime dependencies beyond what each provider needs

The protocol itself has **zero runtime dependencies**. It is pure stdlib: `typing.Protocol`, `dataclass`, `asyncio`. Spec 042 §10 makes this explicit (line 487): *"Provider implementations are optional packages — only `mock` ships with core `conversus`."*

Dependency footprint per provider:

| Provider | Adds to conversus core |
|---|---|
| `mock` | Nothing (ships with core, pure Python) |
| `anthropic` | `anthropic` — one well-maintained SDK |
| `openai` | `openai` — one well-maintained SDK |
| `claude-code` | `claude-agent-sdk` OR subprocess (zero new deps) |
| `acp` (future) | `httpx` (standard HTTP) |

Compare to the LiteLLM-hybrid path: every user installs LiteLLM, a 41k-star framework with its own plugin system, its own proxy server, its own budget enforcement, its own cost tracking, its own security advisory surface (the research doc itself cites PYSEC-2026-2, line 38). All of that is "free" in the sense that it's optional — but if we bake it into the recommended provider for "Tier 3", every user is on the LiteLLM upgrade treadmill forever.

Our protocol lets a user who only wants `mock` + `anthropic` install literally two packages. That is a different category of leanness than any framework-based approach can offer.

### 2.3 Forward compatibility: the protocol is stable even as the ecosystem churns

The research doc (tool-landscape.md §1055 and throughout) describes an ecosystem mid-churn:

- AutoGen is now in maintenance mode, replaced by "Microsoft Agent Framework" v1.0 in 2026
- Google A2A merged with IBM ACP only in September 2025
- MCP Python SDK hit 1.0 on April 2, 2026 — one day before this research was written
- BeeAI framework is the "official" A2A Python SDK, but itself is early
- Astral was acquired by OpenAI in 2026

This is not a settled ecosystem. **Any bet we make on a specific framework is a bet on which of these will still be maintained in two years.**

Our protocol sidesteps the question entirely. When A2A/ACP matures, we add an `acp` provider — spec 042 §4 already sketches `ACPProvider` at lines 211–229. When a new agent runtime ships, we add an adapter. When LiteLLM's API changes, our `LiteLLMProvider` adapter absorbs the change and the engine sees nothing. When MCP semantics evolve, our Claude Code provider adapts and the engine sees nothing.

**The protocol never needs to change.** That is the definition of forward compatibility, and we get it because we own the protocol.

### 2.4 Backward compatibility: a single call site, already abstracted

The counter-narrative against "build our own" is usually "refactoring is expensive". It isn't, because conversus today has **one** dispatch call site: `Agent(prompt=..., run_in_background=True)` inside SKILL.md. That's it. The engine's phase templates and variable contracts are already provider-agnostic — they're just markdown with `{VARIABLE}` placeholders (spec 042 §1, lines 20–23). The coupling is in one place.

Spec 042's FR-009/FR-010/FR-011 (lines 463–466) spell this out:
- FR-009: Omitting `executor:` inside Claude Code MUST behave identically to current SKILL.md.
- FR-010: Omitting `executor:` in Python SDK MUST use existing ModelProvider path.
- FR-011: SKILL.md MUST continue to work as-is.

This is trivially achievable because we control the protocol: we define the default behavior, we define the resolution rules, we wrap the existing `Agent(...)` call as the reference `ClaudeCodeProvider`, and everything else is additive. Today's user sees **zero** change. Tomorrow's CI user gets headless execution. The blog pipeline unblocks. Spec 048 (autonomous governance) unblocks.

Notably, spec 048 §9 declares spec 042 a **HARD DEPENDENCY** (line 425) — it cannot ship without 042. The LiteLLM-hybrid path doesn't actually deliver 042 any faster; it just adds a framework in front of the same adapter layer we'd build anyway. The A2A-future path blocks 042 on a protocol that isn't ready. Build-our-own is the path that unblocks 048 soonest *with the fewest assumptions*.

### 2.5 Testing: 3,428 tests already exist, and a `mock` provider makes them provider-independent forever

Conversus has an enormous test suite. Today many of those tests either (a) mock out the agent call in ad-hoc ways or (b) run against a specific Claude Code harness. Spec 042 §11 (line 497) lists `mock` as shipping with core, and SC-003 (line 475) requires that a full deliberation can run under `mock`.

A `mock` provider that implements the same 4-method Protocol the real providers implement gives us a strictly better testing story than either alternative:

- **Versus LiteLLM-hybrid**: LiteLLM does not replace conversus's agent-runtime path, so we'd still need our own mock for Tier 1/2 providers. We'd also need to mock LiteLLM itself for Tier 3 tests, which means maintaining two mock layers instead of one.
- **Versus A2A-future**: A2A's model is "stand up an HTTP server for each agent". Mocking that in 3,428 tests means either spinning up HTTP servers (slow, flaky) or writing a client-side mock that re-implements the A2A wire protocol. Either way, you still end up writing a protocol-level mock — at which point, why not just have the protocol be yours?

Our protocol gives us one mock, one interface, one source of truth. Every provider the project grows into is tested against the same fixture harness.

### 2.6 The "agent runtimes vs model APIs" split: nobody else does both

This is the decisive technical argument. The research doc makes it bluntly (tool-landscape.md §9–21, in the executive summary):

> *"No single tool solves 100% of the problem because conversus's unique requirement—supporting both model APIs (Anthropic, OpenAI) AND agent runtimes (Claude Code, OpenCode, Aider) in the same abstraction layer—is rare. Most frameworks optimize for one or the other."*

Let's be concrete about what the three "best" candidates *actually* cover:

| Tool | Model APIs | Agent runtimes | Notes |
|---|---|---|---|
| **LiteLLM** | 100+ | **0** | Research line 71: "No agent runtimes: Cannot dispatch to Claude Code, Aider, OpenCode, Copilot" |
| **A2A / ACP** | 0 direct | Depends on wrappers we write | Research line 573: "Requires building/maintaining ACP wrappers for each SDK" |
| **pydantic-ai / LangGraph / CrewAI / Haystack** | N | Framework itself IS a runtime | Semantic mismatch with conversus's "task in → output out" model |

**None** of these give us both halves of what we need. Every single path to a working conversus runs through an adapter layer that we build. The only question is whether that adapter layer is framed around **our abstraction** (we keep control) or **someone else's abstraction** (we pay translation tax forever).

When the shape of the problem is "we need a unifying abstraction that nobody else has built", the right answer is to build it. This isn't a wheel-reinvention case. **There is no wheel.**

---

## 3. Attacking the counter-arguments directly

### 3.1 "You're reinventing the wheel"

**Which wheel?** Point at it. Name the library whose public API looks like:

```python
async def execute(prompt: str, output_path: str,
                  read_paths: list[str] | None,
                  metadata: dict | None) -> ExecutionResult
```

and covers **both** `anthropic` API calls and `claude-agent-sdk` subprocess dispatch under one interface. It does not exist. LiteLLM explicitly does not (research line 71). A2A/ACP is a wire protocol, not a Python Protocol — and its Python implementation is still early-stage (research lines 539–571). pydantic-ai is an agent framework, not an adapter.

"Reinventing the wheel" is a valid critique when a mature wheel exists. Here, the thing that exists is a collection of half-wheels from different vehicles. Our job is to build an axle, not another wheel.

### 3.2 "Maintenance burden"

**The protocol is ~40 lines.** The data classes are ~20. The registry is ~15. Each provider adapter is 100–200 lines per the research doc's own estimate (tool-landscape.md line 757):

> *"Each provider is a thin adapter (100-200 lines of code)"*

So the initial deliverable — protocol + data classes + registry + `mock` + `anthropic` + `claude-code` — is ~500–700 lines of code. That is less than a single Django admin class in this monorepo. Calling that a "framework maintenance burden" is a category error.

Compare to the LiteLLM-hybrid path: we still write every adapter (research's own Implementation Checklist, lines 960–998, lists the exact same providers we'd write), AND we take on LiteLLM as a transitive dependency in core config, AND we inherit its release cadence ("releases multiple times per month", research line 36), AND we inherit its security surface. The "lower burden" claim is an illusion — LiteLLM-hybrid is just our plan plus LiteLLM.

### 3.3 "LiteLLM already does this"

LiteLLM **does not do this**. It does model APIs. Research line 71, verbatim:

> *"No agent runtimes: Cannot dispatch to Claude Code, Aider, OpenCode, Copilot"*

And line 73:

> *"Orchestration: No multi-phase or multi-task coordination; single-completion only"*

LiteLLM solves one of the three tiers in spec 042 §4 (the Tier 3 direct-model-API case). That is 3 of our 12 targeted providers in the matrix at §11 (lines 497–512): `anthropic`, `openai`, and arguably future `gemini`. It does not solve Tier 1 (agentic SDKs: `claude-code`, `copilot`, `gemini-cli`, `opencode`). It does not solve Tier 2 (workflow orchestrators: `gh-aw`, `langgraph`, `temporal`, `gsd`). It does not solve the motivating use case — the blog pipeline (spec 042 §6) — because the blog pipeline needs agents that can read files and produce structured markdown output, which is a Tier 1 concern.

A partial solution to a 3/12 slice of the problem is not a solution. It's a library we might optionally call from *inside* one of our adapters. Which is exactly what this proposal allows — build-our-own does not prohibit using LiteLLM inside a `LiteLLMProvider` adapter. It just refuses to let LiteLLM define the shape of the conversus engine's dispatch layer.

### 3.4 "A2A/ACP is the future, just wait"

Spec 042 already aligns with ACP at the architectural level (see the protocol-stack diagram §2, lines 33–67, and the ACP-mapping table at lines 86–97). The protocol we're proposing is *deliberately* ACP-compatible at the concept level: `prompt` maps to the Task Request text part, `read_paths` maps to reference parts, `output_path` maps to metadata, our `metadata` dict maps to Task Request custom fields. This is not an accident — the spec author explicitly designed it to be a superset that collapses to ACP when an `ACPProvider` is added.

But **waiting for A2A** has three problems:

1. **It doesn't ship**: spec 048 depends on 042, the blog pipeline depends on 042, the entire "CLI that runs outside your CLI" vision (spec 048 §11) depends on 042. A2A ecosystem maturity is measured in "early 2026 adoption"; we cannot block our roadmap on it.
2. **It still requires wrappers we write**: research line 573, "Requires building/maintaining ACP wrappers for each SDK (Claude Code, Aider, OpenCode)". A2A does not magic agent runtimes into existence — somebody has to write the server-side adapter for each SDK. Currently that somebody is us. This is the same adapter work as the build-our-own path, plus an HTTP server lifecycle on top.
3. **It couples us to a protocol that may still change**: A2A merged with ACP in September 2025 (research line 537). Linux Foundation governance is young. Committing our public Python Protocol to match an external wire protocol's current shape is a durability risk. Better: own the Python Protocol, and let the `acp` provider translate in one place when the wire protocol shifts.

The correct A2A strategy is: **ship our own protocol now, add an `acp` provider when the ecosystem is ready**. Spec 042 §11 explicitly lists `acp` as a first-class provider (line 498). We are not betting against A2A. We are refusing to block on A2A.

---

## 4. Concrete protocol citations from spec 042

For the deliberation record, the specific protocol elements this advocacy endorses:

- **Protocol definition**: spec 042 §3, lines 114–176. Four-method Protocol (`execute`, `execute_batch`, `name`, `supports_tool_use`), `runtime_checkable` so duck typing works, async-native.
- **Data classes**: spec 042 §3, lines 180–201. `ExecutionTask` (frozen dataclass, four fields) and `ExecutionResult` (mutable, six fields including `success`, `output_path`, `content`, `error`, `duration_ms`, `provider`, `metadata`).
- **Tool-use adaptation**: spec 042 §4, lines 268–290. The engine itself handles the `supports_tool_use = False` case by inlining file contents and post-writing output — this keeps direct-API providers dead-simple and puts the complexity in one well-tested engine path.
- **Registry and resolution**: spec 042 §5, lines 335–359. `PROVIDER_REGISTRY` dict, `get_provider()` with clear error messages, direct import registration (no entry points required pre-032, but compatible with them post-032).
- **Provider matrix**: spec 042 §11, lines 497–512. Twelve providers listed with type, tool-use flag, parallel strategy, ACP-wrappability. This is the roadmap, and it's achievable only if we own the protocol.
- **FRs that lock in backward compat**: FR-006 through FR-011 (spec 042 §8, lines 459–466). These prove the refactor is a single call site.
- **SCs that define done**: SC-001 through SC-005 (spec 042 §9, lines 475–480). Each one is a provider substitution test — exactly what a protocol-first design enables.

---

## 5. Why this is the winner in winner-take-all

Let me state the positions as cleanly as possible:

- **LiteLLM-hybrid**: use LiteLLM for Tier 3, build everything else ourselves. Net result: same adapter work as build-our-own, plus a framework dependency, plus partial coverage.
- **A2A-future**: wait for A2A/ACP ecosystem to mature, then adopt. Net result: spec 042 blocked indefinitely, spec 048 blocked, blog pipeline blocked, still have to write wrappers when we do adopt.
- **Build-our-own**: define our Protocol, ship `mock` + `anthropic` + `claude-code` in v1, add providers as needed, add `acp` provider when A2A matures. Net result: 500–700 lines of code, zero core dependencies, every future provider is additive, every existing test becomes provider-independent, backward compat is trivial, spec 048 unblocks.

The other two options are **strict subsets** of build-our-own:

- Build-our-own can include a `LiteLLMProvider` adapter whenever we decide LiteLLM is worth the dep (it's a 100-line wrapper). Nothing in this proposal prohibits that.
- Build-our-own can include an `ACPProvider` the moment A2A's Python SDK matures. Spec 042 §11 already lists it as the top row.

So the two counter-positions are not actually alternatives — they are **features** that the build-our-own path can ship when it wants to. The only thing the other positions buy that we don't already have is the **constraint** that our engine must bend to someone else's shape. That's a constraint without a benefit.

---

## 6. Conclusion

The protocol in spec 042 §3 is correct, minimal, and already matches the engine's current dispatch behavior. Owning it gives us:

- Zero core dependencies
- Forward compatibility through adapters, not protocol changes
- A `mock` provider that stabilizes 3,428 tests
- A single-call-site refactor for backward compat
- A clear path to every provider in spec 042 §11, *including* `acp` and `litellm` when we want them
- Unblocked delivery of spec 048 (autonomous governance), the blog pipeline, and every future headless use case

The other two positions either solve 3/12 of the problem (LiteLLM) or block on an ecosystem timeline we do not control (A2A). Both force us to write the same adapter code we'd write anyway, just with extra constraints.

Build the protocol. Ship spec 042. Add providers as we need them.

**Recommendation: adopt the protocol as specified in spec 042 §3 unchanged. Ship `mock`, `anthropic`, and `claude-code` as the v1 provider set. Treat every other provider in the §11 matrix as an additive downstream package.**
