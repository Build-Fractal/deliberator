# Cross-Review: Backbone Researcher's Ground-Truth Report

**Reviewer**: a2a-future-advocate
**Reviewing**: `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/backbone-researcher/review.md`
**Round**: 1, Cross-Review Phase
**Verdict on researcher's report**: Factually solid. Largely refutes my original review. I concede the core naming error and narrow my position significantly.

---

## 1. What I got wrong — direct concessions

The researcher's findings force three concessions. I'll name each explicitly.

### 1.1 I conflated A2A with Zed/JetBrains Agent Client Protocol

**The researcher is right.** Re-reading my own review against §6 of the researcher's report (the "three-protocol tangle"), I see the error clearly.

My original review treated "ACP" as a single protocol, leaning on spec 042's language:

> "ACP (Agent Communication Protocol) — IBM/Linux Foundation standard for agent-to-agent dispatch, merged with Google's A2A protocol (2025). ACP Task Requests map to conversus phase dispatch."

But spec 042 itself also says in §12 Q8 that "JetBrains ACP [is] different from IBM ACP." I noticed the footnote and then ignored it — I plowed ahead arguing for "the `acp` provider" as if it were one thing. The researcher's §6 separates them cleanly:

- **A2A** (Google + IBM, merged Aug 2025, LF AI & Data governance) — JSON-RPC 2.0 over HTTP(S), agent-to-agent task dispatch, Python SDK `a2a-sdk` 0.3.25 stable / 1.0.0a0 alpha.
- **Agent Client Protocol** (Zed/JetBrains, `agentclientprotocol.com`) — JSON-RPC over stdio, IDE ↔ coding-agent integration, "LSP for agents," v0.11.4 as of March 2026.

These are **two completely different protocols** with different wire formats, different scopes (headless server-to-server vs. IDE-to-subprocess), and different threat models (A2A assumes autonomous dispatch; Zed/JetBrains ACP assumes a human-in-the-loop IDE approving each tool call).

My review used "A2A/ACP" as a single term and cited Zed-context ACP facts (JetBrains Agent Registry includes Claude Code, Codex CLI, Copilot CLI, OpenCode, Gemini CLI) implicitly as evidence of A2A ecosystem presence. **That is wrong.** The fact that those agents are in the Zed/JetBrains ACP registry does NOT mean they have A2A server wrappers. Per the researcher's §9:

> "No Anthropic/Claude Code reference. No GitHub/Copilot reference. No Aider reference. No OpenCode reference."

I cannot use the Zed ACP ecosystem as A2A ecosystem evidence. They are separate markets.

### 1.2 My "every future tool is A2A-native" claim is empirically false as of 2026-04

I wrote in §2.3:

> "Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships."

The researcher's §9 directly refutes this:

> "**Ecosystem fact**: As of 2026-04, there is no off-the-shelf A2A server that wraps any of the coding agents conversus would actually dispatch to. If conversus ships an A2A provider today, it will have nothing on the other end of the wire that speaks A2A natively — someone (probably conversus maintainers) has to build the wrapper."

And §6.2:

> "No major agent SDK has shipped an A2A server wrapper for itself yet. No canonical reference implementation of 'wrap Claude Code as an A2A server' exists."

This destroys my "one provider, every tool" argument as a **present-tense** claim. In 2026-04, a conversus A2A client provider would dispatch to exactly zero shipping A2A servers. My review implied the opposite — that the ecosystem flywheel was already turning and we just needed to plug in. It isn't and we can't.

### 1.3 My "pay nothing extra" and "ecosystem flywheel" claims assumed a market that doesn't exist

I wrote:

> "Every SDK that ships an A2A endpoint... becomes conversus-compatible the day it ships. The wrapper is NOT conversus's problem... because wrapping Claude Code as an A2A server is valuable to every A2A client in the world."

The researcher's §9 and §10 mapping table make it clear: **no shipping coding agent exposes an A2A server today**. The researcher even flags in §13 that "if conversus ships an A2A provider, it will initially have no counterparties unless conversus maintainers build the wrappers themselves." So the "wrapper is someone else's problem" framing is wrong. If conversus wants A2A dispatch to work, conversus has to write the Claude-Code-as-A2A-server wrapper itself. There is no community to free-ride on — yet.

---

## 2. Where the researcher does NOT refute me — preserved points

Not everything in my review is dead. Let me separate what survives from what doesn't.

### 2.1 A2A is still the correct long-term protocol (researcher agrees)

The researcher's §6.2, §8, and §11 explicitly validate this:

- §8: "Conversus phase dispatch is agent-to-agent, not model-to-tool. That puts it in A2A's scope, not MCP's."
- §11, point 4: "**A2A exists and is technically the right abstraction** for agent-to-agent dispatch (which conversus phase dispatch is)."
- §13: "Google+IBM's A2A protocol... is the right long-term abstraction for agent-to-agent dispatch."

So my claim "A2A is the right protocol for conversus dispatch" is **endorsed** by the researcher. What gets refuted is "bet everything on it now and skip the bespoke layer" — because the bespoke layer is the only thing on the wire today.

### 2.2 Spec 042's terminology needs cleanup (researcher agrees)

The researcher's §6.4 calls for exactly the same cleanup I should have called for:

> "Rename the 'ACP provider' to 'A2A provider' (or more explicitly, `a2a` using `a2a-sdk`). Explicitly distinguish from the Agent Client Protocol (Zed/JetBrains) — which is a different integration vector."

My review argued "build the `acp` provider first" using spec 042's ambiguous term. The researcher is saying: first, fix the name, because the name is hiding a protocol confusion. I agree.

### 2.3 Subprocess cold-start cost is real (researcher agrees)

Researcher's §11, point 10:

> "subprocess-spawning Claude Code has a cold-start cost (typically ~1–3 seconds for the CLI to boot, load plugins/hooks/MCP servers)... For a conversus run with 10–30 parallel agent phases, this adds up. An HTTP-server-based backbone (OpenCode or A2A) avoids the cold start entirely by reusing a long-lived process."

This is an independently-grounded argument for *some* HTTP-based dispatch path in the eventual provider matrix. It does not validate "A2A first" — OpenCode's HTTP server satisfies the same cold-start avoidance, and is shipping today — but it does validate "we should not be all-subprocess forever."

---

## 3. The corrected position — "PIVOT"

Given the facts, I pivot rather than defend. My new position:

### 3.1 What I no longer claim

- ❌ "Build the A2A provider FIRST." (No counterparties exist today.)
- ❌ "Don't build bespoke providers for copilot, gemini-cli, opencode, aider, gh-aw, langgraph, temporal, gsd." (Researcher's §7 shows subprocess CLI is the **only** de facto interop layer across all of them. Removing bespoke providers removes every provider that works today.)
- ❌ "The ecosystem flywheel already exists." (It doesn't. Researcher §9, §10.)
- ❌ "One provider, every tool, today." (Not today. Maybe 2027.)
- ❌ "A2A" and Zed/JetBrains ACP are the same protocol. (They are not.)

### 3.2 What I still claim

- A2A is the correct long-term protocol for conversus phase dispatch (researcher concurs, §8, §11, §13).
- Spec 042's current "ACP" language is ambiguous and conflates two protocols; it must be split into an `a2a` provider (HTTP, headless, `a2a-sdk`) and a separately-scoped future "Agent Client Protocol" story for IDE integration (researcher concurs, §6.4).
- Cold-start subprocess dispatch does not scale to 10–30 parallel phases; the provider matrix must include **at least one** long-lived-process path (researcher concurs, §11.10). Whether that's OpenCode HTTP, A2A, or something else is an architectural choice, not a given.
- Conversus authoring `conversus-a2a-claude` (an A2A-server wrapper around Claude Code's headless CLI) is a legitimate artifact *independent of whether we ship it as a conversus provider*. It would be the first A2A wrapper for Claude Code in the ecosystem (researcher §6.2, §9: "No canonical reference implementation of 'wrap Claude Code as an A2A server' exists").

### 3.3 What I now propose instead

The researcher's §11 gives us the honest option set. Restating in my own words, with the A2A advocacy narrowed to what the facts support:

1. **Spec 042 provider v1 ships CLI-subprocess providers** for Claude Code, Aider, Copilot CLI, Codex CLI, Gemini CLI, Continue `cn`. The researcher's §7 confirms this is the one interop layer that uniformly exists. This is the "baseline that works today." It is the opposite of what my original review argued.

2. **Spec 042 provider v1 also ships an OpenCode HTTP provider.** OpenCode is the only coding agent with a first-class HTTP server and OpenAPI 3.1 spec today (researcher §2). A ~100-line httpx client gives us the cold-start-free path. This is a **real** long-lived-process dispatch option conversus can have in 2026-04 without waiting for A2A.

3. **Spec 042 provider v1 ships an `a2a` provider** (renamed from `acp` to disambiguate — researcher §6.4) as a **forward bet, not a primary path**. It is client-only initially: conversus can POST Task Requests to any A2A server that a user or team stands up. At ship time, this provider will have zero counterparties on the open ecosystem. That is fine — it is positioned as "opt-in, experimental, for teams running their own A2A agents." It gates on the user providing an A2A endpoint; it does not assume one exists.

4. **Conversus commits to authoring ONE A2A server wrapper** — `conversus-a2a-claude` — as a **standalone artifact**, versioned and released independently of the conversus package. This is the piece of my original argument that actually survives: writing this wrapper **is** valuable even if no other A2A ecosystem exists, because (a) it lets conversus itself dispatch long-lived Claude Code processes over HTTP instead of subprocess-per-phase, (b) it satisfies the cold-start issue the researcher flagged in §11.10, and (c) it establishes the first A2A wrapper for Claude Code, which the researcher explicitly notes does not exist today (§6.2, §9). If the ecosystem grows, we were first. If it doesn't, we still got long-lived-process dispatch for our most-used agent.

5. **Zed/JetBrains Agent Client Protocol is explicitly out of scope for spec 042.** It is the wrong protocol for headless CI dispatch (researcher §6.3: "threat model and UX assume a live IDE with a human in the loop approving tool calls. Spec 042's 'autonomous governance' use case (spec 048) does not fit Zed/JetBrains ACP cleanly"). Spec 042 should mention it only to **rule it out** for the headless dispatch layer and defer it to a possible future "run conversus inside an IDE" track.

6. **A2A-as-the-future is preserved as a documented direction, not a v1 commitment.** The spec 042 provider matrix lists `a2a` as "experimental / forward" with a note that the primary dispatch paths are CLI subprocess (portable baseline) and OpenCode HTTP (one known long-lived server). A2A becomes the primary path **when and if** counterparty wrappers exist — which is a measurable external condition, not a deadline.

---

## 4. Rebutting my own specific errors in the original review

Going through my review section by section and flagging what the researcher's facts invalidate.

### §2.1 "Standards convergence is already decided"

**Still partially valid.** Google + IBM + Linux Foundation backing is real (researcher §6.2 confirms "Google + IBM + Microsoft + AWS + Cisco + Salesforce + ServiceNow + SAP on the TSC"). But "decided" overstates it. Protocol v1.0.0 shipped 2026-03-12 — less than a month before my review. Python SDK is 0.3.25 stable / 1.0.0a0 alpha. "Decided" among framework authors is not the same as "adopted" by coding-agent authors. None of Claude Code, Aider, Copilot, Codex, Gemini, or OpenCode has shipped an A2A server yet (researcher §6.2, §9, §10).

Corrected claim: "A2A has strong standards-level backing that suggests long-term convergence, but adoption by individual coding agents has not happened yet."

### §2.2 "Runtime discovery kills the hardcoded provider list"

**Still technically valid, but moot in 2026-04.** A2A Agent Detail does give runtime discovery. But if no agents are registered, discovery returns an empty set. This argument matures as the ecosystem matures. It is not a reason to ship A2A as the primary dispatch path in 2026-04.

Corrected claim: "Once A2A agents exist, runtime discovery replaces hardcoded registries. Until they exist, runtime discovery is a forward capability, not a current one."

### §2.3 "One provider, every tool — the cross-tool interop dividend"

**Empirically wrong in 2026-04.** I claimed the math changes under A2A: one provider, every tool free. That is only true once tools speak A2A. Today, zero of the researcher's 10 coding tools speak A2A. The math is actually: one A2A provider + N A2A wrappers we or the community write = one provider + N things that look suspiciously like bespoke adapters, just with a different wire format.

The researcher makes this concrete in §11.8: the spec-042 `claude-code` provider "via 'Node bridge' is misleading — the `@anthropic-ai/claude-agent-sdk` is itself a subprocess wrapper around the `claude` CLI binary. From Python you are not avoiding subprocess by calling the TS SDK — you are adding a Node layer between your Python and a CLI subprocess."

By extension, an A2A wrapper around Claude Code is a long-lived server wrapping a subprocess wrapping a CLI. It's still a wrapper. The "wrapper is reusable" part is real — but only if other A2A clients exist to reuse it, which currently means: conversus, and nobody else.

Corrected claim: "A2A server wrappers are reusable artifacts *in principle*. Today, the only guaranteed consumer is conversus itself. The cross-tool dividend is a bet on future A2A client proliferation."

### §2.4 "Composability — recursive deliberation is free"

**Preserved in theory, deferred in practice.** A2A does allow recursive agent-to-agent dispatch (researcher §6.2). But recursive dispatch requires agents on both ends of every hop to speak A2A. With no coding-agent A2A servers shipping, composability is a capability of the protocol, not a capability conversus can use until it writes those servers itself.

### §2.5 "Every bespoke adapter is technical debt that A2A retires"

**Half right, half wrong.** The technical-debt framing assumes A2A arrives. If A2A arrives for coding agents in, say, 2027, then subprocess providers written in 2026 are indeed debt. If A2A arrives in 2028 or 2029, the subprocess providers did their job for 2-3 years of production use and were not debt — they were runway. The researcher's §9 is explicit: A2A is "a bet on a future that will probably arrive, but it has not arrived yet."

My original review treated the bet as certain. It isn't. And the cost of being wrong about the timeline is that conversus ships zero working providers in 2026-04 and waits for a counterparty ecosystem that may take a year or more to exist. That cost is unacceptable; the researcher's subprocess baseline is the only honest hedge.

Corrected claim: "Bespoke subprocess providers become technical debt *when and if* A2A adoption makes them redundant. Until then, they are production infrastructure. We should design them to be replaceable, not avoid writing them."

### §2.6 "The Python SDK already exists"

**Partially wrong.** I cited BeeAI as if it were the primary Python A2A SDK. The researcher's §6.2 clarifies: the primary Python A2A SDK is `a2a-sdk` on PyPI, maintained by Google LLC. Version 0.3.25 stable, 1.0.0a0 alpha. BeeAI is an IBM framework that uses A2A; it is not the A2A SDK itself. More importantly, the researcher flags: the stable version is **pre-1.0**. Betting architecture on a 0.3.x Python package with a 1.0.0a0 alpha is higher risk than my original review acknowledged.

Corrected claim: "A Python A2A SDK exists (`a2a-sdk`), but it is 0.3.25 stable. Production adoption in 2026-04 accepts the risk of a pre-1.0 dependency."

### §3.1 Attack on "Build Our Own"

**The attack survives in part.** The N×M argument is still real in a world where you actually have N SDKs to wrap — which the researcher's subprocess-CLI baseline reduces to N CLIs with a common shape ("subprocess + flags + JSON output"). That is not quite N bespoke adapters; the researcher's §7 explicitly names subprocess-CLI as a **de facto standard**. So the "10 adapters at 500 lines each" number I quoted was inflated — a well-designed subprocess provider base class handles 80% of the variance and each specific tool is more like 100 lines of argv construction and JSON parsing. The researcher's baseline is closer to "one subprocess provider base + thin per-tool configurations" than "ten bespoke adapters." I overstated the pain.

### §3.2 Attack on "LiteLLM-Hybrid"

**Mostly survives**, because the hybrid approach is orthogonal to the A2A-vs-subprocess question. LiteLLM addresses Tier 3 (model APIs), which the researcher's §7 confirms is already unified by LiteLLM and OpenAI-compatible endpoints. That part of the hybrid pitch is fine. The Tier 1–2 part of the hybrid pitch (direct SDK providers) is what my review attacked, and it should have been attacking "we write ten bespoke SDK wrappers" when the researcher shows the answer is actually "we write one subprocess provider base class." The hybrid advocate is not wrong about needing bespoke-ish providers for Tier 1–2; they just might be wrong about the shape (bespoke per-SDK) vs. the shape the researcher documents (shared subprocess base).

### §4 "Spec 048 as the Proof Case"

**Still valid in direction, wrong in specifics.** Spec 048 does require execution providers for headless CI dispatch (FR-021: "`conversus governance` MUST be invokable without Claude Code running"). My review argued A2A makes this deployable and bespoke adapters make it a dependency nightmare. The researcher's counter: the dependency nightmare is not a given if the subprocess providers are designed as thin argv builders, and A2A cannot satisfy spec 048 today because there are no A2A coding-agent servers to dispatch to.

Corrected claim: "Spec 048 will eventually benefit from A2A dispatch, but spec 048 in 2026-04 must ship against subprocess CLI providers because those are the only working backbone. A2A support should be added when counterparties exist."

### §5 "Proposed Commitment"

**Every numbered point except possibly #2 is wrong or needs rewording.** Restating:

1. ~~Prioritize the `acp` provider.~~ **Corrected**: Rename to `a2a` and position as experimental/forward. Prioritize subprocess CLI providers.
2. Ship `conversus-a2a-claude` as a reference A2A server wrapper. **Preserved** — this is the piece that actually survives as immediately useful.
3. ~~Implement `claude-code` direct provider ONLY as fast-path optimization.~~ **Corrected**: Implement it as the primary path. It is what works today.
4. ~~Do NOT build bespoke providers for other tools.~~ **Corrected**: DO build subprocess CLI providers for the other tools. They share a common shape (researcher §7) and are the de facto interop layer.
5. Use LiteLLM inside A2A server wrappers. **Soft preserved** — can still be an implementation detail.
6. Align spec 048's `agent_registry` config with A2A Agent Detail discovery. **Preserved as forward design**, deferred as current implementation.

---

## 5. What I still think the deliberation should care about

Even with my core position narrowed, a few things from my original review deserve to survive as forward-looking constraints on the spec:

1. **Name the protocols correctly.** Spec 042 must stop saying "ACP" as if it were one thing. A2A (HTTP, headless, `a2a-sdk`) and Zed/JetBrains Agent Client Protocol (stdio, IDE) are different protocols. The researcher's §6.4 is correct; spec 042 needs this cleanup.

2. **Design the subprocess provider base class with A2A in mind.** If we know A2A is the long-term dispatch protocol, the provider interface should be shaped so that a future A2A provider is a drop-in replacement — same task shape, same result shape, same streaming model. The researcher's §11.2 argues for subprocess-CLI as the portable baseline; I argue the base class should be designed so that replacing a subprocess call with an A2A Task Request is a code path swap, not a refactor.

3. **Ship `conversus-a2a-claude` as a standalone artifact.** This is the piece of A2A advocacy that survives scrutiny. Writing an A2A-server wrapper around `claude -p --bare` is ~100-200 lines, solves the cold-start problem the researcher flagged in §11.10, and establishes the first A2A wrapper for Claude Code. It is worth doing *even if* no other A2A ecosystem exists — because conversus itself is the first consumer.

4. **Spec 048 governance mode should declare A2A as the target dispatch protocol for multi-repo and cross-organization deployment**, even while its 2026-04 implementation uses subprocess providers. This keeps the long-term architecture coherent and avoids retrofitting governance to a subprocess model it outgrows.

5. **Zed/JetBrains Agent Client Protocol deserves a separate, later spec** for "run conversus inside an IDE." It is not in scope for spec 042 headless dispatch. The researcher's §6.3 is correct to separate these.

---

## 6. Honest summary

My original review made a protocol-naming error and overcommitted to a future that has not arrived. The researcher's report is factually sound and forces me to narrow from "bet everything on A2A now" to "ship subprocess + OpenCode + experimental A2A now, author the first A2A Claude Code wrapper ourselves, design the provider base class so A2A is a drop-in replacement later."

The strong version of my advocacy — "A2A first, bespoke is dead, one provider rules them all" — does not survive contact with the ecosystem data. The researcher's §9 is definitive: **zero shipping coding agents expose A2A servers as of 2026-04**. Any "A2A provider" conversus ships today has nothing to talk to on the other end unless conversus writes that other end itself.

The weak version of my advocacy — "A2A is the right long-term protocol, spec 042's naming needs to be fixed, and conversus should author the first A2A Claude Code wrapper as a standalone artifact" — survives and is actually *endorsed* by the researcher's §6, §8, §11, §13.

I'll take the weak version. It is the honest one.

---

## 7. Points of agreement with the researcher (for synthesis)

For the arbitration phase, these are claims I and the researcher both agree on and that the synthesizer can treat as joint-ratified:

1. A2A and Zed/JetBrains Agent Client Protocol are **different protocols** and spec 042 conflates them. Fix required.
2. A2A is the correct **long-term** abstraction for conversus phase dispatch (agent-to-agent).
3. MCP is the **wrong** layer for conversus execution providers (it is for model-to-tool, not agent-to-agent). MCP stays as a tool-access concern inside agents.
4. No shipping coding agent exposes an A2A server in 2026-04. The ecosystem is empty of counterparties.
5. Subprocess CLI is the **only** interop layer that uniformly works across Claude Code, Aider, Copilot, Codex, Gemini, and Continue in 2026-04.
6. OpenCode is the **one exception** — it ships a first-class HTTP/OpenAPI 3.1 server and is uniquely positioned for a native long-lived-process provider today.
7. Cold-start subprocess dispatch does not scale to 10–30 parallel agent phases; the provider matrix needs at least one long-lived-process option.
8. Zed/JetBrains Agent Client Protocol is **not** the right layer for spec 048 autonomous governance (it assumes IDE + human-in-the-loop).
9. Spec 042's "Node bridge" framing of the `claude-code` provider is misleading; the Claude Agent SDK is itself a subprocess wrapper, so going Python → Node SDK → CLI subprocess is strictly worse than Python → CLI subprocess directly.

These are nine points the other advocates cannot relitigate without bringing new evidence.

---

**Files referenced**:
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/backbone-researcher/review.md` (§0 TL;DR, §6 three-protocol tangle, §7 common patterns table, §8 MCP scope, §9 A2A maturity, §10 mapping table, §11 spec-042 implications, §13 one-paragraph summary)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/review.md` (my own original review — §2.1–2.6 arguments, §3.1–3.2 attacks, §4 spec 048, §5 proposed commitment)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/spec.md` (§2 Protocol Alignment, §4 ACP-Native Provider, §12 Q8 JetBrains ACP footnote)
