# Cross-Review: backbone-researcher

**From**: litellm-hybrid-advocate
**Target**: backbone-researcher / `review.md`
**Phase**: Round 1 Phase 2 — Cross-Review
**Date**: 2026-04-03

---

## 0. Verdict up front

The researcher's findings are **mostly supportive of my core claim and genuinely damaging to my framing**. LiteLLM remains the right answer for direct model APIs — that part of my position survives intact and is arguably strengthened. But the researcher has exposed a real category error in how I described the non-LiteLLM half of the architecture. I was calling it "agent runtimes" and implying it was a qualitatively different tier with its own abstractions. The evidence says it's almost entirely **CLI subprocess wrangling with JSON output**, and that means my 70/30 framing was the wrong shape of the problem.

I need to concede the framing, keep the core recommendation, and reframe the proposal. The revised position is stronger than the original. Details below.

---

## 1. What the research validates

### 1.1 LiteLLM is the right tool for direct model APIs — confirmed.

The researcher doesn't contest this and in fact reinforces it. From §7's "common pattern" table (lines 299–305):

> Model API — Yes (LiteLLM, OpenAI-compatible endpoints) — 100+ providers via a single OpenAI-shaped interface

And §10's verified mapping confirms LiteLLM's coverage is real — Anthropic, OpenAI, Google/Gemini, Ollama, Azure, Bedrock, Mistral, Groq, Together, Fireworks, VLLM, LMStudio, etc. are all first-party LiteLLM providers. The earlier `tool-landscape.md` claim of "100+ providers" is not inflated.

**My core claim holds**: for the direct-model-API tier (spec 042's Tier 3), rewriting LiteLLM would be a category mistake. Nothing in the researcher's report suggests otherwise. The 14-line adapter sketch from `tool-landscape.md` lines 613–633 is still the right shape of code.

### 1.2 The "don't reinvent provider SDK glue" argument gets stronger, not weaker.

The researcher's mapping table (§10) actually strengthens the case. Look at what it shows for the non-LiteLLM column:

- Claude Code: subprocess only
- Aider: subprocess (unofficial Python API is "could change without backwards compatibility")
- Copilot CLI: subprocess (docs sparse)
- Codex CLI: subprocess
- Gemini CLI: subprocess
- Continue: subprocess (`cn`)

None of these have shipped Python SDKs worth depending on. Meanwhile the researcher confirms (§7) that **for model APIs**, LiteLLM and OpenAI-compatible endpoints are the *one layer where a shared standard actually exists*. That is exactly the seam where outsourcing to a third party is most justified — it is the layer where the market has converged, the surface area is huge, and the work is commodity. The research didn't refute this; it drew a clearer map of where the commodity layer ends and the bespoke layer begins.

---

## 2. What the research refutes — and I have to concede

### 2.1 "Agent runtimes" was the wrong name for the non-LiteLLM tier.

My original review talked about "Tier 1 agent-runtime providers" and implied they were a qualitatively different kind of thing — a richer, in-process, SDK-driven dispatch layer distinct from raw model calls. The researcher demolishes that framing. From §1.2:

> The SDK spawns a subprocess running the bundled `claude` CLI binary. It does not call the Anthropic `/v1/messages` API directly.

And §11, observation 8:

> Spec 042's `claude-code` provider via "Node bridge" is misleading: the `@anthropic-ai/claude-agent-sdk` is itself a subprocess wrapper around the `claude` CLI binary. From Python you are not avoiding subprocess by calling the TS SDK — you are adding a Node layer between your Python and a CLI subprocess. Go straight to `claude -p --bare` from Python.

This is a concrete factual correction to my mental model. I had been treating `claude-agent-sdk` as if it were in the same architectural family as `anthropic` or `openai` — a library that talks to a service. It is not. It is a subprocess wrapper around a CLI binary. The "Agent tool" that conversus's current SKILL.md relies on is not even an API; it's an in-session tool that only exists inside a live Claude Code conversation (§1.4).

So when I said "agent runtimes need native adapters because LiteLLM can't reach them," I was technically right for the wrong reason. The real reason LiteLLM can't reach them is not that they're a higher-level abstraction — it's that **they're not network APIs at all**. They're CLIs you shell out to.

### 2.2 The 70/30 split was describing the wrong axis.

I framed the split as:
- **70% model API work** → LiteLLM
- **30% agent runtime work** → native adapters

The researcher's §7 shows the actual axis is:
- **One layer**: direct network APIs (model providers, OpenCode's HTTP server)
- **Another layer**: subprocess + CLI + JSON (Claude Code, Aider, Copilot, Codex, Gemini, Continue)

These are not "70/30" — they are **two fundamentally different transport mechanisms**, not two points on a complexity spectrum. My framing implied conversus would have two adapter families distinguished by richness. The truth is the two families are distinguished by **whether bytes travel over TCP or over stdin/stdout of a child process**. That's a much sharper and more useful cleavage.

### 2.3 "Hybrid" sounds like a blend; the reality is "two transports."

"Hybrid" implies a compromise or a 70/30 mix-and-match. But once you see the transport-level distinction, the right framing isn't "hybrid at all" — it's **"pick the right transport per target, and use the best-in-class library for each transport."** That's not a hybrid, that's just competent layering.

I concede the framing. The word "hybrid" was my contribution and it was doing rhetorical work that the evidence doesn't support.

---

## 3. The reframed position

Dropping the hybrid language and adopting the transport-level framing, here is what I now argue:

### 3.1 The `ExecutionProvider` protocol is still ours (unchanged)

Spec 042 §3's `ExecutionProvider`, `ExecutionTask`, `ExecutionResult` remain conversus-owned. This is the abstraction boundary and it doesn't change based on what sits behind it. Everything below is "how do you implement a provider"; the protocol is "what does a provider look like to the engine."

### 3.2 Two concrete base implementations, not one "native" pile

Instead of "LiteLLM for model APIs + hand-written adapters for agent runtimes," the revised proposal is:

1. **`LiteLLMProvider`** — wraps `litellm.acompletion()`. Handles every direct-API model (Anthropic, OpenAI, Gemini, Bedrock, Ollama, Groq, Together, Fireworks, Mistral, VLLM, LMStudio, ~100 more). This is Tier 3 in spec 042's sense. The 14-line adapter sketch stands.

2. **`SubprocessProvider`** (new base class) — a single generic adapter that spawns a CLI with a configured argv template, pipes the prompt to stdin or `-p`, collects stdout (parsing JSON if the CLI supports `--output-format json`), surfaces exit codes and stderr as errors. Concrete providers are thin configurations of this base:
   - `ClaudeCodeProvider` = `SubprocessProvider(cmd=["claude", "-p", "--bare", "--output-format", "json", ...])`
   - `AiderProvider` = `SubprocessProvider(cmd=["aider", "--message", ..., "--yes"])`
   - `CopilotCliProvider`, `CodexProvider`, `GeminiCliProvider`, `ContinueProvider` — same shape, different argv.

3. **`OpenCodeProvider`** — special case because OpenCode is the one tool with a real HTTP server (researcher §2). Use `httpx` against the published OpenAPI 3.1 spec. Not a subprocess, not LiteLLM — its own small adapter.

4. **Optional future `A2AProvider`** — when A2A matures and counterparty wrappers exist (researcher §9 flags this is speculative today).

This is **stronger than my original "hybrid"** in two concrete ways:

- It eliminates the N bespoke "agent runtime" adapters I was pricing in. Instead of "Claude Code adapter + Aider adapter + OpenCode adapter + Copilot adapter" as four separate engineering tasks, it's **one `SubprocessProvider` base + N small config objects**. The researcher's §7 observation that subprocess-with-JSON is "the de facto backbone across all agentic coding tools today" means one base class genuinely covers them all. This is a meaningful reduction in surface area compared to my original framing.
- It makes the architecture honest about what each provider actually does. A reader looking at `ClaudeCodeProvider` should not be misled into thinking it's a rich SDK integration — it's a subprocess. Say so in the class name and the docstring. Intellectual honesty is an engineering virtue.

### 3.3 So the real split is:

| Transport | Library | Targets | Code we write |
|---|---|---|---|
| Direct network API (model provider) | LiteLLM | ~100+ model providers | `LiteLLMProvider` (14 lines) |
| Subprocess + CLI + JSON | stdlib `asyncio.subprocess` | Claude Code, Aider, Copilot, Codex, Gemini, Continue | `SubprocessProvider` base (~150 lines) + N small configs |
| HTTP (non-OpenAI-shape) | `httpx` | OpenCode | `OpenCodeProvider` (~100 lines per researcher §2.4) |
| Future: A2A | `a2a-sdk` | Anything wrapped as A2A (none today) | `A2AProvider` (deferred) |

That is the actual shape. Three transports, ~300 lines of provider code total (excluding the base class and protocol definitions), covering every realistic 2026 target.

---

## 4. Where LiteLLM is *more* useful than my original framing suggested

The researcher's findings surface two LiteLLM advantages I underweighted:

### 4.1 LiteLLM covers the local/self-hosted case that subprocess providers can't

Researcher §1 didn't call this out specifically, but LiteLLM ships first-class Ollama, VLLM, LMStudio, and LocalAI providers. That's meaningful because:

- CLI-subprocess providers only help for tools that have a CLI. Ollama has a CLI but most users want to hit its HTTP API.
- Users who want "run conversus against a local 70B model" can do it through LiteLLM with zero conversus code changes. That is a legitimate differentiator.
- Offline / air-gapped / on-prem users are a non-trivial segment for a tool positioning itself as governance infrastructure (spec 048). LiteLLM lets us serve them for free.

This actually *strengthens* the LiteLLM case relative to my original review, which mostly emphasized cloud providers.

### 4.2 LiteLLM's OpenAI-compatible proxy mode is a force multiplier

LiteLLM can run as a proxy server exposing an OpenAI-compatible endpoint that routes to any of its 100+ backends. This means:

- Any tool that already speaks OpenAI's wire format (which includes Aider, Continue, Cursor, Codex, and more) can be pointed at a LiteLLM proxy and will automatically gain access to every model LiteLLM supports.
- Conversus users running the `SubprocessProvider` flavor for Aider or Codex can plug a LiteLLM proxy in front and get the same 100-provider reach through those subprocess-based tools.

This is a composition story my original review didn't surface. LiteLLM isn't just "the Tier 3 implementation" — it can also act as a **universal translator layer in front of the Tier 1 subprocess tools**, giving conversus users a way to hit exotic providers through any CLI. That's a bigger footprint than "70% of the work," and it's a real argument for LiteLLM showing up in more than one place in the stack.

Neither of these were in my original review. The researcher's more careful taxonomy is what made them visible. Credit where due.

---

## 5. Where the researcher's findings create new risks for my position

Being honest about the downsides:

### 5.1 If subprocess is the common pattern, a LiteLLM-only story isn't enough on its own

My original review leaned heavily on "LiteLLM solves 70% of the problem." The researcher's reframing makes clear that **the non-LiteLLM 30% is actually the *primary* use case** for many conversus users. Spec 048's governance mode presumes Claude Code / Copilot / Codex running in CI. None of those are LiteLLM targets. So a proposal that says "LiteLLM is the main event" is underselling the subprocess tier.

Concession: the subprocess provider is not a footnote. It is co-equal. A fair presentation of the revised position gives `SubprocessProvider` and `LiteLLMProvider` equal billing. The argument for LiteLLM is not "it solves most of the problem" (it doesn't, for conversus's target use case) — it is "**it solves the layer it's responsible for completely and for free**, so we get to spend our engineering budget on the subprocess base class and the conversus-unique work."

### 5.2 The "hybrid" rhetoric was doing work my revised framing can't

My original review used "hybrid" as rhetorical ammunition against both build-our-own and A2A-future: "we pick the best of both worlds." The researcher's framing destroys that rhetoric by showing the two worlds aren't worlds at all — they're just different transports. I can no longer argue "hybrid is a clever middle path." I have to argue something less catchy but more honest: "there are three transports, and for each transport we pick the right tool, and one of those tools happens to be LiteLLM."

That's a weaker narrative, even though it's a stronger technical position. I should be honest about this in the synthesis phase.

### 5.3 The researcher's "subprocess cold start" observation is a real concern LiteLLM cannot help with

Researcher §11 observation 10:

> Subprocess-spawning Claude Code has a cold-start cost (typically ~1–3 seconds for the CLI to boot, load plugins/hooks/MCP servers). `--bare` exists specifically to cut this. For a conversus run with 10–30 parallel agent phases, this adds up.

This is a real performance concern for the subprocess transport that LiteLLM (which uses persistent HTTP) does not have. For the model-API tier LiteLLM is strictly faster because there's no per-call process spawn. But for the Tier 1 subprocess targets, conversus is going to eat 1–3s × N phases of cold start unless we pool, batch, or use a long-lived process (which the tools don't support).

This argues for a **third** provider variant I didn't originally propose: a **process-pooled subprocess provider** that keeps warm CLI workers around. That's future work, but it should be in the protocol from day 1 — `ExecutionProvider.supports_pooling: bool` or similar. Researcher's observation forced me to think about this; I should include it in the revised proposal.

---

## 6. What I'm keeping from my original review

Even with the framing concession, these points from my original review are unchanged and still load-bearing:

1. **LiteLLM is the right tool for direct model APIs** — still the single highest-leverage decision in spec 042.
2. **The `ExecutionProvider` protocol is ours** — LiteLLM does not and should not own this abstraction.
3. **The maintenance-burden argument against build-our-own** — writing 12 SDK wrappers from scratch when LiteLLM exists is still strategically incoherent. The researcher's findings don't change this; they just clarify that the "12 SDK wrappers" are specifically for the direct-API tier, which is what I always meant.
4. **The A2A-future position is premature** — researcher §9 confirms A2A protocol is 1.0.0 as of one month ago, Python SDK is 0.3.25 stable / 1.0.0a0 alpha, and **no shipping coding agent has been wrapped as an A2A server yet**. Betting spec 042 on A2A today means conversus maintainers building every counterparty wrapper themselves. That risk is real and the researcher documented it.
5. **Spec 048 is blocked on 042** and the timeline pressure is real.
6. **The 3-week shipping target** per the `tool-landscape.md` implementation checklist still holds, with the modification that "hand-written agent runtime adapters" should be replaced with "one `SubprocessProvider` base class + thin per-tool configs," which is probably *faster*, not slower.

---

## 7. Answers to the specific prompt questions

**Q1: Does the research VALIDATE your core claim (LiteLLM for model APIs)?**
Yes, unambiguously. Researcher §7 explicitly identifies model APIs as the one layer where a shared standard exists and names LiteLLM as that standard. The 100+ provider count is confirmed. My core claim stands.

**Q2: Does the research REFUTE your split (70% model APIs / 30% agent runtimes)?**
Yes. The split isn't 70/30 of one problem — it's two different transports (network vs subprocess). My framing was wrong. I concede it.

**Q3: Should you CONCEDE that the "agent runtime" tier isn't really different from the model API tier — it's just "direct API" vs "CLI subprocess" — and reframe your position accordingly?**
Yes, and I have, above. The revised framing is "two transports, pick the right library for each." LiteLLM covers the network transport; a new `SubprocessProvider` base covers the subprocess transport; OpenCode gets its own small HTTP adapter; A2A is deferred.

**Q4: Given that the researcher says CLI subprocess is the actual common pattern, should your proposal be "LiteLLM for direct APIs + a generic SubprocessProvider for CLI-based tools"? Is that stronger than your original "hybrid" framing?**
Yes on both counts. It is meaningfully stronger. Instead of four bespoke "agent runtime" adapters, it's one base class with thin per-tool configs. That reduces code, centralizes error handling (`CLINotFoundError`, timeouts, exit codes, stderr parsing), and makes the architecture honest about what the non-LiteLLM providers actually are. The word "hybrid" should be retired from my vocabulary on this spec.

**Q5: Is there ANYTHING in the researcher's findings that makes LiteLLM MORE useful than your original framing suggested?**
Yes, two things:
- LiteLLM's local/self-hosted coverage (Ollama, VLLM, LMStudio, LocalAI) unlocks the on-prem / air-gapped / offline segments for free. My original review undersold this.
- LiteLLM's OpenAI-compatible proxy mode lets users point *subprocess-based tools* (Aider, Codex, Continue) at a LiteLLM proxy to reach 100+ backends. That's a composition pattern I hadn't articulated. LiteLLM isn't just "the Tier 3 implementation"; it can sit in front of Tier 1 tools as a universal translator. That is a bigger footprint than my original review described.

---

## 8. Net effect on the deliberation

- **Core recommendation**: unchanged. Use LiteLLM for direct model APIs. This is still the right answer.
- **Framing**: changed materially. "Hybrid" is the wrong word. The real framing is "pick the right library per transport," and the transports are network (LiteLLM), subprocess (new `SubprocessProvider` base), HTTP-not-OpenAI-shape (OpenCode adapter), and future A2A (deferred).
- **Provider count**: my original review was implicitly planning N bespoke adapters for the non-LiteLLM tier. The researcher's findings say it should be 1 base class + N configs. That is a code reduction and I should take the win.
- **Concessions I owe the other advocates**:
  - To build-our-own: you were right that I was underweighting the bespoke-adapter work. I was — but the researcher's findings show the bespoke work is smaller than either of us thought (one base class, not N adapters). The conclusion still points toward LiteLLM-plus-subprocess-base, not full build-our-own, but I acknowledge the research shrank the LiteLLM-exclusive portion of the stack.
  - To A2A-future: the researcher confirms A2A is a plausible long-term target and the `ExecutionProvider` protocol leaves the door open. I still oppose betting spec 042 on it today, but I should acknowledge the researcher treated it with more nuance than my original review did — especially the "no counterparty wrappers exist yet" finding, which is the single most important fact for the A2A-now position to grapple with.

---

## 9. One-sentence synthesis of the revised position

**Use LiteLLM to own the model-API transport completely, introduce a generic `SubprocessProvider` base class to own the CLI-subprocess transport uniformly, add a small `OpenCodeProvider` HTTP adapter for the one tool with a real server, and defer A2A until counterparties exist — all behind conversus's own `ExecutionProvider` protocol.**

That is a more accurate, more honest, and technically stronger position than my original "hybrid" framing. The research forced the correction. It is a correction, not a refutation.

---

**End of cross-review.**
