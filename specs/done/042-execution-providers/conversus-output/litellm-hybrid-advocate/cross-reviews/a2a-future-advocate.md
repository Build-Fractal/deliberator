# Cross-Review: LiteLLM-Hybrid on A2A-Future

**Reviewer**: litellm-hybrid-advocate
**Target**: a2a-future-advocate
**Round**: 1 Phase 2 — Cross-Review
**Date**: 2026-04-03

---

## 0. Framing

The a2a-future-advocate and I have a common enemy — "build our own model-API layer from scratch." We both think that's strategically incoherent. Where we disagree is on **what the seam should be** and, more importantly, **when the seam's counterparty is allowed to be vapor.**

The advocate bets on a future ecosystem. I bet on today's reality. Both bets can be right — and in fact my position explicitly preserves their bet as a Phase 3 outcome. The question this cross-review has to answer is whether their argument, *as written*, holds up against the backbone-researcher's ground-truth findings. I will argue it does not, but I will also identify the one place where they have a genuine point that belongs in the final synthesis.

---

## 1. The "Cross-Tool Interop Dividend" Collapses Against an Empty Ecosystem

The load-bearing paragraph of the a2a-future-advocate's case is §2.3, "One provider, every tool — the cross-tool interop dividend." The argument is that under A2A, "each tool that speaks A2A is free — zero lines of conversus code." The ecosystem flywheel kicks in, someone else wraps Claude Code, conversus inherits the work for free.

**The backbone-researcher's §9 is dispositive on this**: *"As of 2026-04, there is no off-the-shelf A2A server that wraps any of the coding agents conversus would actually dispatch to. If conversus ships an A2A provider today, it will have nothing on the other end of the wire that speaks A2A natively — someone (probably conversus maintainers) has to build the wrapper."* (§9 and reinforced in §0 point 8 and §10's mapping table, which shows "A2A server?" = "No" for Claude Code, OpenCode, Aider, Copilot, Codex, Gemini, Continue, Cline, Cursor, Windsurf, and gh-aw.)

Let me translate this into the advocate's own dividend math. Under the advocate's model, the benefit of A2A is N wrappers × M clients = free reuse. But *N today is zero*. Zero coding agents have been wrapped as A2A servers by their maintainers or by anyone else. The flywheel has no counterparty. The "reusable artifact" argument only works once at least one counterparty exists; otherwise conversus is **both the protocol client and the wrapper author for every provider**, which is *strictly more work* than writing direct adapters because conversus now has to write the adapter AND the A2A server that wraps the adapter.

The advocate anticipates this objection in §3.3 and waves it off: *"And that is why the `claude-code` direct provider exists in spec 042 §4 as a reference implementation. I am not arguing we delete it. I am arguing it should be built as an A2A server wrapper from day one."* But that concession guts the "zero lines of conversus code" claim. If conversus is building the wrapper, it is not zero lines — it is ~500 lines per tool (the advocate's own number, cited back at the hybrid in §3.2) *plus* an HTTP server layer *plus* process lifecycle management *plus* a discovery registry *plus* operational babysitting of N long-running server processes in every environment conversus runs in.

The dividend only arrives when other people start shipping A2A servers. The advocate assumes they will. The researcher documents that they have not. **That gap is the entire argument.**

---

## 2. "A2A and Zed/JetBrains ACP" — The Conflation the Researcher Flagged

The backbone-researcher spends §6 of their report untangling a specific confusion in the current landscape: there are **two different protocols** that both get called "ACP":

- **A2A** (formerly IBM ACP, merged into Google A2A, Linux Foundation): JSON-RPC over HTTP, agent-to-agent dispatch. 1.0.0 released 2026-03-12. Python SDK `a2a-sdk` at 0.3.25 stable / 1.0.0a0 alpha.
- **Agent Client Protocol** (Zed/JetBrains): JSON-RPC over stdio (HTTP experimental), IDE-to-coding-agent. v0.11.4, not yet 1.0.

The researcher is explicit (§6.3): *"It is NOT a general-purpose agent dispatch protocol for headless pipelines. Its threat model and UX assume a live IDE with a human in the loop approving tool calls. Spec 042's 'autonomous governance' use case (spec 048) does not fit Zed/JetBrains ACP cleanly — it fits A2A."* And in §11 point 9: *"The spec-042 'ACP provider' name is ambiguous given the two-ACP problem in the current landscape."*

Now re-read the a2a-future-advocate's review in light of that distinction:

- §2.3: *"JetBrains ACP is literally a protocol for this exact use case."* — referring to IDE dispatch surfaces for autonomous governance in CI. That is **exactly the category error** the researcher warned about. Zed/JetBrains ACP is not for CI dispatch; it's for IDE integration with a human approver in the loop.
- §1: The ACP Mapping table is lifted from spec 042, which the researcher flags as *"partially correct but the naming has moved on"* (§6.4). The spec conflates the two protocols, and the advocate's argument inherits that conflation wholesale.
- §4: The Zed/JetBrains ACP row in the spec-048 surface table is presented as evidence that *"every one of those surfaces is an A2A client in disguise."* It isn't. IDE plugins are Zed/JetBrains ACP clients. CI runners and webhooks would be A2A clients. Those are two separate implementations with two separate SDKs and two separate wire formats.

This is not a small nitpick. The advocate's strongest argumentative move — *"every execution surface in the 'CLI that runs outside your CLI' vision is an A2A client in disguise"* — depends on treating two different protocols as one. Once you separate them, the unification story fractures. A2A covers CI, cron, webhooks. Zed/JetBrains ACP covers IDE plugins. That is already **two adapters**, not one. The "every future tool is A2A-native" prediction becomes "every future tool is either A2A-native or Zed/JetBrains-ACP-native, and conversus has to figure out which."

My hybrid approach treats this cleanly: the `ExecutionProvider` protocol absorbs any wire format. LiteLLM for Tier 3. Direct SDK adapters for Tier 1 agents today. A2A provider when the A2A server ecosystem actually exists. Zed/JetBrains ACP provider if and when the "conversus inside an IDE" story becomes load-bearing (spec 042 §12 Q8). **Each adapter is additive, not exclusive.** The advocate's architecture forces a choice where no choice is needed.

---

## 3. The "Splitting the Abstraction in Three" Attack — A Strength, Not a Weakness

In §3.2 the advocate attacks the hybrid approach with:

> "It splits the abstraction in half. Tier 3 goes through LiteLLM; Tier 1–2 goes through bespoke adapters; A2A is deferred. Conversus now has to maintain THREE mental models..."

Let me respond on architectural grounds, not rhetorical ones.

**There is already only one mental model**: the `ExecutionProvider` protocol. That protocol defines `execute()`, `execute_batch()`, `ExecutionTask`, `ExecutionResult`, and `supports_tool_use`. LiteLLM, Claude Code subprocess, future A2A — **each of these is an implementation of that single protocol**. The engine, the deliberation loop, the phase sequencer, the arbiter, the dispute parser all see exactly one type: `ExecutionProvider`. That is not three mental models. That is one abstraction with three implementations, which is the entire point of polymorphism and the entire point of spec 042 §3.

What the advocate is calling "three mental models" is actually "three implementation files." Each file is narrow (the LiteLLM adapter is literally ~14 lines per the research sketch; the Claude Code subprocess adapter is ~100–300 lines; a future A2A adapter is another ~200 lines) and independently testable. The engine touches none of their internals. The "splitting" the advocate attacks is exactly what a protocol is *for*.

Compare that to the advocate's proposal in §5. They propose:
- `conversus-acp-claude` (A2A server wrapping Claude Code)
- `claude-code` direct provider (as a fast-path optimization, "convenience, not pillar")
- LiteLLM used "inside A2A server wrappers if we want" but not as a conversus-level abstraction
- A2A server wrappers for copilot, gemini-cli, opencode, aider, gh-aw, langgraph, temporal, gsd

**That is at least two conversus-level abstractions** (A2A client + direct Claude Code fast path) *plus* ~8 separate A2A server projects that conversus has to author. It is strictly more pieces than the hybrid. The advocate's attack on "three mental models" applies with more force to their own architecture, not less.

The advocate's architecture is also harder to test locally. Every A2A server the advocate proposes is a long-running process that has to be started, health-checked, and torn down for every test run. The hybrid approach tests LiteLLM in-process (one line — `litellm.completion_async(mock=True)`) and subprocess adapters with stdlib mocks. In a CI runner that fires `conversus governance --gate pr` once per PR and exits, the cold-start cost of an A2A server fleet is net negative compared to in-process LiteLLM + one-shot `claude -p --bare`.

**Splitting at the natural seam — commodity vs unique, in-process vs out-of-process — is a strength of the hybrid approach. Collapsing it into a universal A2A layer assumes a uniformity the ecosystem has not yet delivered.**

---

## 4. "Every Future Provider Is A2A-Native" — The Prediction Question

The advocate's position has an implicit forecast: within some relevant horizon, every coding agent and model provider the conversus team cares about will ship an A2A server. How confident am I that this will be true?

**Moderately confident on a 2–4 year horizon. Not confident at all on a 6-month horizon.** The researcher's §9 documents the current state:

- A2A protocol v1.0.0 released 2026-03-12 (less than a month old at review time)
- Python SDK `a2a-sdk` at 0.3.25 stable / 1.0.0a0 alpha
- Reference implementations: Google ADK, IBM BeeAI, LangGraph integration
- Zero shipping coding agents have been wrapped as A2A servers by their maintainers

Compare the adoption curve of similar protocols the advocate cites as analogies:

- **Kubernetes**: Released 2014. Took ~3 years to become industry consensus and ~5 years before every major platform shipped native integrations. The analogy only works if you're willing to wait that long.
- **OpenTelemetry**: Merged from OpenTracing + OpenCensus in 2019. GA for Traces in 2021, Metrics in 2022, Logs in 2023. Four years from merger to full feature parity.
- **gRPC**: Announced 2015. Broad SDK coverage by 2017. But it still has not displaced REST for most public APIs a decade later.
- **OCI**: Announced 2015. Broad runtime support by 2017, but Docker Hub still dominates image distribution in 2026.

The advocate says *"this coalition wins standards wars"* and I don't dispute that. What I dispute is the timeline. Even in the advocate's best analogies, standards take **years** to propagate from "1.0 release" to "every tool ships a native implementation." A2A hit 1.0 last month. Spec 042 needs to ship in ~3 weeks to unblock spec 048. Spec 048 needs to ship to unblock the autonomous governance vision that is currently conversus's north star. **The timelines do not overlap.**

A more honest version of the advocate's forecast would be: "By 2028, A2A will likely be a standard that conversus should target. Betting on it in 2026 is speculative." That forecast is compatible with my hybrid position. The position that is *not* compatible with the researcher's ground truth is "build the `acp` provider first in 2026 and treat every direct SDK adapter as technical debt." That treats a 2028 outcome as a 2026 design constraint, and that is how projects miss their ship dates.

---

## 5. What the Hybrid Offers TODAY That A2A Does Not

Let me be concrete about the delta, because this is where the debate is actually won or lost.

**Today, with the hybrid approach, conversus can ship:**

1. **LiteLLM provider covering OpenAI, Anthropic, Google, Bedrock, Groq, Together, Fireworks, DeepSeek, Mistral, Cohere, xAI, Ollama, VLLM, LMStudio, Hugging Face** — 14 lines of adapter code, ~2 hours of work. Immediate Tier 3 support for every requested provider in spec 042 §11 and most providers the community is going to ask for in the next 18 months. All of these have stable SDKs that LiteLLM already normalizes.

2. **Claude Code provider via `claude -p --bare --output-format json` subprocess** — ~200 lines per the research sketch. Works today. Covers the default conversus configuration out of the box. The backbone-researcher's §1.4 point 3 and §11 point 2 specifically recommend this path as "the most portable, lowest-risk backbone today."

3. **OpenCode provider via `httpx` against `opencode serve` and the published OpenAPI 3.1 spec** — ~100 lines (researcher §2.4). OpenCode is the one coding agent with a first-class HTTP server today; we get it as an architectural outlier, not a standard.

4. **Aider provider via subprocess (`aider --message` with `--yes`)** — ~150 lines. The researcher's §3 documents the exact invocation pattern.

5. **Cost tracking, retry, rate limiting, error taxonomy** — inherited from LiteLLM for Tier 3, wrapped manually for Tier 1. Total per-tier code: ~14 lines for the LiteLLM tier, ~100 lines of shared retry/cost wrapping for subprocess tiers.

6. **Spec 048 unblocked on its original timeline.** Governance mode lands in Q2 2026 instead of Q4 2026 or later.

**With A2A-first, conversus can ship today:**

1. **An A2A client that posts to... nothing.** No shipping coding agent is an A2A server as of 2026-04. The advocate's counter is "we'll wrap them ourselves," which means the 500-lines-per-SDK wrapper work the advocate criticized in §3.2 is now on the A2A approach's balance sheet, *plus* the A2A server transport layer, *plus* running those servers as sidecars in every environment conversus runs in.

2. **A bet that A2A wrappers of Claude Code / Copilot / Aider / OpenCode will exist within the conversus ship horizon.** The researcher's §9 rates this as speculative and explicitly says *"no counterparties exist yet."*

3. **A delayed ship date** because every "free" wrapper is actually a conversus-authored wrapper, and we have to build the A2A server fleet before we can ship the A2A client.

This is the TODAY vs FUTURE asymmetry the framing called out. The hybrid ships real code against real counterparties right now. The A2A-first approach ships a client against a hypothetical server fleet that conversus would have to author.

---

## 6. Where the A2A Advocate Has a Legitimate Point

I want to be explicit: **the advocate is right about one thing that my position should absorb, not reject.**

They are right that **A2A is the correct long-term shape of this layer**. The mapping between conversus phase dispatch and A2A Task Requests in spec 042 §2 is not wrong; it is prescient. In 2–4 years, when the A2A server ecosystem has filled in, conversus absolutely should ship an `a2a` provider as a first-class citizen of the `ExecutionProvider` protocol. When that day comes:

- Tier 3 providers that are behind A2A fronts (e.g., some future "A2A endpoint for OpenAI" offered by Microsoft or a Linux Foundation reference server) can migrate from LiteLLM to the A2A provider.
- Tier 1 agent runtimes that ship their own A2A servers (when Anthropic ships "Claude Code as an A2A server" or when community wraps `opencode` behind `a2a-sdk` on PyPI) can migrate from the direct subprocess adapter to the A2A provider.
- The migration is incremental and non-breaking because the engine only sees `ExecutionProvider`. One file changes at a time. Users don't notice.

**My position explicitly accommodates this.** Spec 042 §4 in the hybrid research recommendation already names A2A as Phase 3 (~6 months out, conditional on ecosystem maturity). The hybrid approach is not "A2A never"; it is "A2A when the counterparty exists."

The disagreement is about **sequencing**, not about **destination**. The advocate wants to sequence A2A first and let the ecosystem catch up. I want to sequence LiteLLM + direct adapters first and adopt A2A when the ecosystem has actually caught up. The hybrid position is strictly dominant in the "what ships in the next 3 weeks" window and strictly *equivalent* to the advocate's position in the "what do we run in 2028" window — because both arrive at the same place.

**The advocate's position is my position with a sequencing bug.** Fix the sequencing, and we agree.

---

## 7. Specific Factual Corrections to the A2A Review

Noted in passing for the synthesis phase:

- **§2.6**: *"BeeAI Framework — official Python/TypeScript SDK for building A2A agents... Full asyncio-native."* — The canonical Python SDK is `a2a-sdk` (Google LLC, Apache 2.0, 0.3.25 stable / 1.0.0a0 alpha per researcher §6.2). BeeAI is *one of several* framework integrations, not "the" official SDK. The advocate is representing BeeAI as canonical when it is one of multiple reference implementations (Google ADK, BeeAI, LangGraph).

- **§1 citation**: *"Python SDK available via the BeeAI framework."* — Same issue. The primary Python SDK is `a2a-sdk`, not BeeAI.

- **§2.6 dependency footprint claim**: *"No new dependencies; standard `httpx` for HTTP client."* — If conversus ships an A2A provider that actually speaks the protocol correctly, it will pull in `a2a-sdk`, which itself depends on FastAPI/Starlette (optional server), `opentelemetry` (optional tracing), and a JSON-RPC framework. The "just httpx" claim is only true if conversus hand-rolls the JSON-RPC wire format, which is a maintenance liability of its own and defeats the "use the standard" argument.

- **§3.2 attack**: *"Spec 042's problem is agent dispatch (the engine already has a `ModelProvider` for raw completions — the hybrid advocate's 'new' LiteLLM wrapper is a rename of what exists)."* — This mischaracterizes the hybrid. The hybrid does not rename `ModelProvider`. It defines `ExecutionProvider` as a *new* abstraction above `ModelProvider`, exactly as spec 042 §3 specifies. LiteLLM wraps the lower model-API layer inside one `ExecutionProvider` implementation; that is not "a rename of what exists."

- **§3.3**: *"A2A is a Linux Foundation standard, not a single vendor's package... A standards change takes years and happens in the open. A supply chain incident happens on a Tuesday."* — This is rhetorically effective but empirically wrong on the timelines involved. The Python SDK `a2a-sdk` IS a single vendor's package (Google LLC maintainer per researcher §6.2) at version 0.3.25 stable / 1.0.0a0 alpha. That is the same vendor risk surface as LiteLLM, except LiteLLM is at 41,900 stars with multi-release-per-month cadence and `a2a-sdk` is pre-1.0. The "Linux Foundation standard" governs the *protocol*, not the Python client the advocate wants conversus to depend on.

- **§4 "IDE plugins (via JetBrains ACP from spec 042)"** — As noted in §2 of this cross-review, JetBrains ACP is a different protocol from A2A. Citing it as evidence of A2A's reach confuses two separate standards that happen to share a partial name.

---

## 8. Summary

The a2a-future-advocate and I agree on more than we disagree on:

- Build-our-own is strategically incoherent.
- The `ExecutionProvider` protocol (spec 042 §3) is the right seam.
- A2A has the right *shape* for the long-term agent-to-agent dispatch problem.
- Conversus should not spend engineering time on commodity model-API glue.

We disagree on one thing: **timing.**

The advocate argues "target A2A now, treat everything else as legacy." The backbone-researcher's §9 is the fatal blow to this sequencing: no shipping coding agent has been wrapped as an A2A server, the Python SDK is pre-1.0 alpha, and the 1.0 protocol release is less than a month old. Building the A2A provider first means conversus is simultaneously the client, the wrapper author for every tool, and the operator of the server fleet — strictly more work than the hybrid, with a later ship date.

The hybrid approach ships against today's ground truth (LiteLLM is production-proven, `claude -p --bare` works, `opencode serve` has a published OpenAPI 3.1 spec, `aider --message` works) while leaving the A2A door open for the day — probably 2027 or 2028, per historical standards-adoption curves — when the ecosystem catches up. When that day arrives, conversus adds one more `ExecutionProvider` implementation and the engine doesn't notice.

**The advocate's vision is correct. Their sequencing is wrong. The hybrid honors the vision while shipping the spec.**

On the concrete questions the framing asked:

1. **Does "cross-tool interop" hold given the empty ecosystem?** No. The dividend requires at least one counterparty other than conversus; today there are zero.
2. **Is "splitting the abstraction in three" a fair attack?** No. There is one protocol (`ExecutionProvider`) with three implementations. That's polymorphism, not fragmentation. The advocate's own architecture has more pieces.
3. **How confident am I that "every future provider is A2A-native"?** Moderately confident on a 2–4 year horizon; not at all confident on a 6-month horizon. Spec 042 has to ship in 3 weeks.
4. **What does the hybrid offer today that A2A doesn't?** Working code against real counterparties: LiteLLM for 15+ model providers, `claude -p --bare` for Claude Code, `opencode serve` HTTP client for OpenCode, `aider --message` for Aider. Spec 048 unblocked on schedule.
5. **Where does the advocate have a point?** A2A is the right long-term destination. My position already plans for it as Phase 3. The disagreement is sequencing, not direction. Fix the sequencing and we agree.

**The hybrid wins today. A2A wins eventually. Shipping the hybrid is how we get to "eventually" without missing "today."**

---

**End of cross-review.**
