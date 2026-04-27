# Advocacy Review: The LiteLLM Hybrid Approach

**Position**: Build spec 042's `ExecutionProvider` protocol ourselves, but delegate the model-API layer to LiteLLM. Build native adapters only for agent runtimes (Claude Code, OpenCode, Aider).

**Phase**: Round 1 Phase 1 — Advocacy
**Advocate**: LiteLLM-hybrid
**Date**: 2026-04-03

---

## 1. The Core Argument in One Sentence

Spec 042 is ~30% an agent-runtime problem and ~70% a model-API problem, and LiteLLM has already solved the 70% — for free, in production, at 41,900-star scale — so spending engineering weeks rewriting what LiteLLM already does would be malpractice.

The research report (`tool-landscape.md`, Part 4, line 822) arrived at exactly this conclusion after evaluating 14 frameworks: **"Implement the hybrid approach."** That recommendation didn't come from vibes — it came from a matrix (Part 3, lines 804–814) where Hybrid scored 95% fit, Build-Our-Own scored 100% "by definition" but with the highest maintenance burden, and A2A scored 85% with the highest operational complexity. The research is the prior; the other advocates have to overturn it.

---

## 2. What LiteLLM Actually Gives Us (Cited from the Report)

From `tool-landscape.md` §1 (lines 27–77):

- **100+ model providers on day 1**: OpenAI, Anthropic, Azure, Google, Mistral, Ollama, Bedrock, Groq, Together, Fireworks, xAI, DeepSeek, Cohere, Hugging Face, VLLM, LMStudio. Every one of those is a direct hit on Tier 3 of spec 042's provider matrix (§11). Every one of those is a user we win without writing a line of SDK glue.
- **41,900 GitHub stars, active multi-release-per-month cadence, used by Stripe, OpenAI, FastAPI maintainers** (line 36). This is not a toy or a bet. This is infrastructure the industry is already standing on.
- **MIT license** (line 32). Zero license risk, zero commercial entanglement, zero reason to fork.
- **Automatic format conversion per provider** (line 46). Every provider has a different function-calling syntax; LiteLLM normalizes them. Conversus would otherwise have to write — and *maintain forever* — a matrix of N providers × M format quirks.
- **Built-in exponential backoff, per-provider rate limit handling, circuit breakers** (lines 60–63). These are not one-afternoon features. They are months of production-hardening that LiteLLM already ate the cost of.
- **Full async-native `AsyncLiteLLM`** (line 51). Drops straight into conversus's `async def execute()` signature in spec 042 §3 with zero impedance mismatch.
- **Cost tracking built into response metadata, per-call granularity, real-time budget enforcement** (lines 54–58). Spec 042 Open Question #3 asks whether `ExecutionResult` should include cost. LiteLLM answers "yes, and here it is."
- **Security advisories patched promptly (PYSEC-2026-2 fixed in March 2026)** (line 38). Mature CVE-response discipline. That's a *positive* signal, not a red flag — it means the maintainers take security seriously and have a working disclosure pipeline.

The research-authored integration sketch (lines 613–633) is **fourteen lines of Python** to wrap LiteLLM as an `ExecutionProvider`. Fourteen. That's the entire Tier 3 story. Compare that to the surface area of rolling our own.

---

## 3. The Surface Area We Avoid Rewriting

Let me enumerate exactly what the "build our own" position has to write and maintain, provider by provider, that the hybrid approach does not:

| Concern | Providers affected | What we'd have to build |
|---|---|---|
| Client construction + auth | 12+ | Env var conventions, keyring, org-ID handling per provider |
| Request envelope | 12+ | Each provider has a different `messages` format (OpenAI vs Anthropic vs Gemini vs Bedrock) |
| Response parsing | 12+ | Each provider returns different `choices`/`content`/`candidates` shapes |
| Streaming | 12+ | SSE for OpenAI, chunked JSON for Anthropic, gRPC for Vertex |
| Function-calling format | 12+ | OpenAI tools, Anthropic tool_use blocks, Gemini functionDeclarations, Mistral's variant |
| Rate limit handling | 12+ | Per-provider header parsing (`x-ratelimit-*`), backoff curves |
| Retry semantics | 12+ | Which errors retry, which don't, idempotency keys |
| Cost calculation | 12+ | Price tables per model × per token type × per region, updated as providers change pricing |
| Error taxonomy | 12+ | Mapping provider error codes to a unified exception hierarchy |
| Context window limits | 12+ | Per-model max tokens, reserved output tokens |
| SDK version drift | 12+ | Every provider ships SDK updates monthly; we'd be on a treadmill |

That is **roughly 144 cells of bespoke code**, plus perpetual maintenance, plus a bug tail that shows up every time a provider ships a breaking change. LiteLLM's existence means those 144 cells are someone else's problem. Every hour we spend rewriting them is an hour not spent on the parts of conversus that are actually unique — phase sequencing, dispute parsing, arbitration, governance.

The research report puts this plainly in Part 4 (line 843): **"Don't build our own model provider abstraction: LiteLLM solves this; reinventing wastes time."**

---

## 4. Where We Still Build Ourselves — And Why That Matters

This is not a "use LiteLLM for everything" position. The hybrid explicitly builds our own:

1. **The `ExecutionProvider` protocol itself** (spec 042 §3). This is conversus's intellectual property — the shape of `execute()`, `execute_batch()`, `supports_tool_use`, `ExecutionTask`, `ExecutionResult`. LiteLLM does not and should not own this. We own the abstraction; we rent the implementation for one tier.
2. **Tier 1 agent-runtime providers**: `claude-code`, `opencode`, `aider` (and later `copilot`, `gemini-cli`). LiteLLM does not cover these (report line 72: *"No agent runtimes: Cannot dispatch to Claude Code, Aider, OpenCode, Copilot"*). These are our job. And they're **the same job** under any of the three approaches — build-our-own, hybrid, or A2A-future all have to write these adapters eventually.
3. **Tool-use adaptation** — the `supports_tool_use=False` path that pre-reads files into the prompt and post-writes output (spec 042 §4). This is engine logic, not provider logic. We own it.
4. **Phase-aware metadata routing, cost aggregation across phases, dispute parsing, gate evaluation** — none of which LiteLLM touches.

So the hybrid splits the work at the natural seam: **LiteLLM owns "how do I talk to model X"; conversus owns "how do I run a deliberation."** Those are two different problems. Conflating them (as build-our-own does) is a category error.

---

## 5. Attack Surface: Why the Other Two Positions Are Weaker

### 5.1 Against "Build Our Own"

**Claim**: "External dependency is dangerous. Write it ourselves."

**Rebuttals**:

- **The research report literally scores this at the worst maintenance burden** (Part 3, line 808): *"Build Our Own → Maintenance Burden: High (reinvent wheels)."* Not my opinion. The backbone research.
- **Time-to-ship is 4–6 weeks** vs 2–3 weeks for hybrid (Part 3, line 807). That's 2–3 extra weeks of runway burned on a problem that has been solved in public for years. Conversus has spec 048 (autonomous governance) blocked on 042 as a HARD dependency (spec 048 §9: *"Spec 042 dependency: Autonomous mode REQUIRES execution providers (headless execution). Cannot ship before 042."*). Every week 042 slips, 048 slips. Every week 048 slips, we don't have CI gates, PR comments, scheduled audits, or the "CLI that runs outside your CLI" vision (048 §1). The cost of delay is not theoretical.
- **"Zero dependencies" is a myth.** Build-our-own still depends on the underlying `anthropic`, `openai`, `google-generativeai`, `mistralai`, `cohere`, `boto3`, `ollama` SDKs. You don't *eliminate* dependencies, you just move them from one well-tested aggregator to twelve individually-pinned, individually-drifting SDKs. The math is worse, not better.
- **Provider coverage day 1: "Limited initially (1-3)"** (Part 3 line 810). Three providers on day 1 versus LiteLLM's hundred-plus. Users asking "does conversus support Groq?" get told "no, maybe in Q3" — that's a losing pitch against Aider, OpenCode, and anything else that just uses LiteLLM and ships.
- **The build-our-own advocate will say "we pin versions."** So do we. The difference is we pin *one* version of LiteLLM (which abstracts 12 SDKs) versus pinning *twelve* versions of *twelve* SDKs and handling twelve independent upgrade cycles. That's a qualitative difference in operational load, not a rounding error.

### 5.2 Against "A2A-Future"

**Claim**: "A2A is the standard; build for that future now."

**Rebuttals**:

- **The report is blunt**: Part 4 line 842, *"Don't implement A2A now: Ecosystem too new; operational overhead too high; LiteLLM + direct SDKs are faster."* That's the research conclusion, not mine.
- **A2A requires running agents as HTTP services** (report line 564: *"Operational overhead: Each agent needs to be running and reachable"*). Conversus today runs inside Claude Code as a skill, inside Python as a library, and soon inside GitHub Actions as a CI step (spec 048 §6). Demanding that users spin up long-running A2A server processes for Claude Code, Aider, and OpenCode — just so conversus can dispatch — is a **massive regression in operational simplicity** for the 99% case. CI runners want a one-shot `conversus governance --gate pr`, not a sidecar fleet.
- **A2A wrapper effort is ~500 lines per SDK** (report line 654: *"A2A server wrappers for each SDK: Medium effort (~500 lines per SDK)"*). For Claude Code, Aider, and OpenCode that's 1,500 lines of server code we'd write **in addition to** the ExecutionProvider work. The hybrid approach writes the same SDK adapter code but skips the HTTP server layer entirely — because the engine can just call the SDK in-process.
- **A2A ecosystem is early-2026 early.** Report line 571: *"A2A is still early (2025-2026); SDK maturity is improving but not yet as battle-tested as LiteLLM or LangChain."* Conversus is not in a position to bet spec 042 — and through it spec 048's entire governance vision — on an ecosystem whose SDK maturity was flagged as a risk in the ground-truth research three days ago.
- **The hybrid approach doesn't close the door on A2A.** It explicitly leaves it open as Phase 3 (report lines 750–754, 826). When A2A matures, we add an `acp` provider alongside the others. The `ExecutionProvider` protocol is the abstraction boundary. A2A slots in as one more implementation. The A2A advocate's "future" is something the hybrid approach *already plans for* — we just don't hold shipping hostage to it.

In other words: build-our-own pays too much today, A2A-future pays too much today for a speculative tomorrow, hybrid pays the minimum today and keeps both doors open.

---

## 6. Addressing the Counter-Arguments Head-On

**"External dependency creates supply-chain risk."**
LiteLLM is MIT-licensed, actively maintained with multi-release-per-month cadence (report line 35), security-disciplined (PYSEC-2026-2 patched, line 38), and pinned to a stable version in our lockfile. The research flags this risk explicitly (Part 7, line 1005) and rates it **Low likelihood, mitigated by version pinning and fallback direct SDKs**. That's a residual risk of roughly the same order as depending on `requests` or `httpx` — which conversus already does. We don't refuse to use `httpx` because it's "external." Same principle.

**"Version lock-in to LiteLLM's API."**
LiteLLM's API is stable (report line 38, *"Stability: Stable"*) and the surface we consume is narrow: `litellm.completion_async()` plus response shape. If LiteLLM ever breaks us, the adapter is **14 lines of code** (research integration sketch, lines 613–633). We can rewrite those 14 lines in a weekend. That's not lock-in; that's a thin Facade pattern around a commodity. Lock-in would be if we coupled our *orchestration* to LiteLLM's internals. We don't. We couple one provider implementation to it.

**"It's only a partial solution — 70% of the problem."**
Yes. And that 70% is free. The remaining 30% (agent runtimes) is **the same work under any approach**. Build-our-own has to write Claude Code, Aider, and OpenCode adapters. A2A has to write ACP servers around those same SDKs. Hybrid writes the adapters directly. The agent-runtime work is constant; the only variable is whether we also rewrite the model-API layer. Rewriting it is the expensive, no-value option.

**"What if LiteLLM disappears?"**
It won't — 41,900 stars, Stripe and OpenAI-maintainer production usage, multi-release cadence (report lines 34–37). But even under the worst case, the `ExecutionProvider` protocol is ours. Swapping LiteLLM for Mirascope, pydantic-ai, or hand-rolled SDKs is a bounded project — one adapter file. The research's risk table (Part 7) rates this a **Low-likelihood, High-impact risk with clean mitigation** (line 1005: *"Monitor releases; pin to stable version; fallback direct SDKs"*). Contrast with build-our-own, where there is no mitigation for "we fell behind on twelve SDK upgrade cycles simultaneously" — that's not a risk, that's a guaranteed outcome.

---

## 7. The Strategic Argument: This Is the Only Path That Respects Conversus's Core Work

Look at what conversus is actually trying to be. Spec 048 (`autonomous-governance-mode`) is the north star: conversus as infrastructure, running in CI, cron, hooks, webhooks, scheduled audits, PR gates. Spec 048 §1 says it outright: *"conversus becomes a background quality gate — like pytest, mypy, ruff, or shellcheck."* Spec 048 §11 lists seven execution surfaces conversus needs to land on.

Every hour spent reinventing what LiteLLM already does is an hour not spent on:
- The `conversus governance` CLI subcommand (spec 048 §5)
- Auto-grounding arbiter (spec 048 §4)
- `.conversusrc` schema and config discovery (spec 048 §3)
- GitHub Actions workflow templates (spec 048 §6)
- PR comment formatting with commentator integration (spec 048 §6.2)
- META_DISPUTE handling (spec 048 FR-009)
- Exit-code stability guarantees (spec 048 FR-014)
- Override mechanisms (spec 048 Q10)
- Replay/preview (`--replay --last 10`, spec 048 Q5)

**That** is the conversus-unique surface area. That's where the defensible work lives. The model-API layer is a commodity. Treating it as a commodity — by outsourcing it to LiteLLM — is how we concentrate our engineering budget on the differentiated work.

Build-our-own inverts that allocation: it spends the most expensive engineering hours on the least differentiated work. That is strategically incoherent.

---

## 8. Concrete Proposal

Adopt the implementation checklist from the research report (Part 6, lines 962–998) verbatim. Specifically:

### Week 1 (Core + Tier 3)
- Implement `ExecutionProvider`, `ExecutionTask`, `ExecutionResult` per spec 042 §3 — **conversus code, not LiteLLM**.
- Implement `PROVIDER_REGISTRY` and `get_provider()` — **conversus code**.
- Create `conversus-provider-litellm` package with `LiteLLMProvider` wrapping `litellm.completion_async()` — **14 lines of adapter code** over LiteLLM.
- Validate against Anthropic, OpenAI, Google, Ollama via LiteLLM — free, covers 90% of requested providers.
- Cost tracking inherits from LiteLLM's built-in metadata.

### Week 2 (Tier 1 — Claude Code)
- Create `conversus-provider-claude-code` package. Subprocess wrapper is the recommended option (report line 975). No LiteLLM involvement — this is a native adapter, as it must be.

### Week 3 (Tests, Docs, Backward Compat)
- End-to-end: `claude-code` provider runs a full deliberation.
- End-to-end: `anthropic` via LiteLLM runs a full deliberation with file inlining per spec 042 §4.
- Blog pipeline PoC per spec 042 §6.
- Verify SKILL.md, Python SDK, and CLI all retain current behavior with no `executor:` configured (spec 042 FR-009, FR-010, FR-011).

### Post-042 (Phase 2)
- Add `conversus-provider-opencode` and `conversus-provider-aider` — again, native adapters, no LiteLLM.
- Future: `copilot`, `gemini-cli` as they stabilize.

### Future (Phase 3, ~6 months out)
- Add `acp` provider when A2A ecosystem matures. `ExecutionProvider` protocol absorbs it without engine changes.

**Shipping date**: ~3 weeks from start. Spec 048 unblocked by end of week 3. Governance mode lands on the original timeline.

Compare that to build-our-own's 4–6 weeks (per research matrix) and the cascading slip into 048, 046, 047.

---

## 9. Closing Argument

The research report evaluated 14 tools and concluded in plain language (Part 4, line 822):

> **"Implement the hybrid approach."**

And the reasons it gave (lines 830–836):

> "Fastest to ship... Lowest risk... Simplest architecture... Zero vendor lock-in... Solves the blog pipeline problem... Future-proof."

Every one of those is a property conversus needs to honor spec 048's vision, ship on time, and not burn engineering weeks on commodity SDK glue. The other two positions each fail at least one of those properties:

- **Build-our-own** fails "fastest to ship," "lowest risk," and "provider coverage on day 1." It is the position of someone who prefers owning problems to solving them.
- **A2A-future** fails "fastest to ship" and "operational simplicity" today in exchange for a speculative ecosystem bet. It is the position of someone who would rather build the perfect tomorrow than ship a working today.

The hybrid approach is the only one that ships the spec, honors the abstraction, keeps the future open, and respects conversus's core engineering budget. It is backed by the backbone research, it matches the natural seam between "commodity" and "unique" work, and it leaves every future door — including A2A — open.

**The hybrid wins.**

---

## 10. Key Citations from the Research Report

- **Executive recommendation** — `tool-landscape.md` line 21: *"Implement conversus's own lightweight ExecutionProvider protocol... then use LiteLLM for Tier 3 (direct API) and A2A/MCP wrappers for Tier 1-2 (agentic SDKs)."*
- **LiteLLM maturity** — lines 34–38 (41,900 stars, Stripe/OpenAI production use, security-disciplined).
- **LiteLLM provider coverage** — lines 40–43 (100+ providers, full Ollama, VLLM, LMStudio, Together, Bedrock).
- **LiteLLM built-in retry/rate-limit/cost** — lines 54–63.
- **LiteLLM integration sketch (14 lines)** — lines 613–633.
- **Tradeoff matrix scoring Hybrid at 95%** — Part 3, lines 804–814.
- **Explicit recommendation against build-our-own** — line 843: *"Don't build our own model provider abstraction: LiteLLM solves this; reinventing wastes time."*
- **Explicit recommendation against A2A-now** — line 842: *"Don't implement A2A now: Ecosystem too new; operational overhead too high."*
- **Risk assessment** — Part 7, lines 1004–1011 (LiteLLM risks rated Low with clean mitigations).
- **Implementation checklist (3-week plan)** — Part 6, lines 962–998.

---

**End of advocacy review.**
