# Cross-Review: a2a-future-advocate

**Reviewer**: build-our-own-advocate
**Round**: 1, Phase 1 (cross-review)
**Target**: `../../a2a-future-advocate/review.md`

---

## Executive verdict

The a2a-future-advocate's position is built on a factual error the backbone-researcher explicitly flagged: **it conflates two different protocols that happen to share the letters "ACP"**. Once that conflation is corrected, the "one provider, every tool" dividend collapses, the "every future provider is A2A-native" claim becomes false, and the "6-month deletion timeline for bespoke adapters" becomes exactly the kind of aspirational-future pragmatism the advocate themselves spends §2.5 attacking.

What remains after the correction is a genuinely valid forward-looking observation: A2A is the right long-term target for *agent-to-agent* dispatch in a post-2026 ecosystem, and our own protocol should have `a2a` as a first-class provider the moment wrappers exist. I already believe this — spec 042 §11 already lists it, and §4 of my review endorses it — so most of what the A2A advocate wants is **already inside my plan as a downstream provider**, not as the protocol layer.

The disagreement is not "A2A yes vs. A2A no". The disagreement is "A2A as the *foundation* we build on vs. A2A as *one provider among many* behind our own Protocol". The researcher's facts decisively favor the latter.

---

## 1. The ACP conflation — the load-bearing factual error

The backbone-researcher dedicates §6 of their report to this exact issue. Quoting directly:

> **"'ACP' is an ambiguous term in the current (2026-04) landscape. Two different protocols share the name":**
> - **IBM ACP → merged into Google A2A** (Aug 2025, Linux Foundation): agent-to-agent dispatch, JSON-RPC over HTTP.
> - **Zed/JetBrains Agent Client Protocol** (agentclientprotocol.com): IDE-to-coding-agent, "LSP for agents", JSON-RPC over stdio.
>
> **"Spec 042 currently conflates these two. [...] this is a correctness issue in the spec and other deliberation agents must not assume either protocol alone covers both layers."** (researcher §0, item 6)

The researcher then separates them in §6.3:

> "[Zed/JetBrains ACP] is NOT a general-purpose agent dispatch protocol for headless pipelines. Its threat model and UX assume a live IDE with a human in the loop approving tool calls. **Spec 042's 'autonomous governance' use case (spec 048) does not fit Zed/JetBrains ACP cleanly — it fits A2A.**" (researcher §6.3)

And conversely for A2A:

> "No major agent SDK has shipped an A2A server wrapper for itself yet. No canonical reference implementation of 'wrap Claude Code as an A2A server' exists." (researcher §6.2)

Now look at how the a2a-future-advocate moves between these two protocols as if they were one:

**Passage A (advocate §2.3, the "one provider, every tool" argument)**:
> "Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships. [...] **We write it once, and Cursor, Zed, OpenCode, LangGraph, CrewAI, Haystack, Microsoft Agent Framework, and everyone else benefits.**"

This passage lists **Zed** as an "A2A" beneficiary. Zed does not speak A2A. Zed speaks the Zed/JetBrains **Agent Client Protocol** — a completely separate protocol the researcher catalogues at §6.3. The advocate has silently merged the two ecosystems to inflate A2A's coverage. OpenCode in the same list speaks `opencode acp` (Zed/JetBrains ACP) per researcher §2.3, not A2A. Cursor, Windsurf, Cline speak *neither* per researcher §5.1 and §5.3.

**Passage B (advocate §4, the "CLI that runs outside your CLI" argument)**:
> "IDE plugins | Not supported | **Future (via JetBrains ACP from spec 042)**
> [...] Every one of those surfaces is an A2A client in disguise. [...] An IDE plugin wants to dispatch to a coding agent — **JetBrains ACP is literally a protocol for this exact use case**."

This passage does the opposite move: it introduces "JetBrains ACP" (the IDE protocol) and then claims "every one of those surfaces is an A2A client in disguise". That is the conflation in its purest form: A2A is doing the work in the sentence, but the example is a different protocol. Per researcher §6.3, the JetBrains Agent Client Protocol is specifically *not* designed for headless dispatch, which is exactly what spec 048 needs.

**Passage C (advocate §5, the commitment list)**:
> "Ship `conversus-acp-claude` as the reference A2A server wrapper for Claude Code."

The name mixes the two. Is it an "acp" wrapper (Zed/JetBrains stdio protocol, which Claude Code already supports through Anthropic's existing CLI) or an "A2A server" (Google/IBM HTTP protocol, which no one has wrapped Claude Code as yet)? These are different integrations with different transports, different audiences, and different maturity levels. The advocate is treating them as interchangeable.

**Why this matters**: The entire "A2A coalition already won the standards war" argument in advocate §2.1 rests on counting Zed/JetBrains adoption as A2A adoption. It is not. Zed/JetBrains ACP is a young (v0.11.4, not 1.0) IDE protocol. A2A is a young (1.0.0 released 2026-03-12) dispatch protocol. Both exist, neither dominates, and neither has wrapped the coding agents conversus needs to dispatch to. **The advocate's "mature standard" is actually two separate immature standards stapled together.**

---

## 2. "One provider for all tools" vs. the empty-ecosystem finding

Advocate §2.3 is the economic heart of their argument:

> "Under A2A, the math changes:
> - `conversus-provider-a2a` (single HTTP client, ~200 lines)
> - **Each tool that speaks A2A is free — zero lines of conversus code**
>
> Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships."

The researcher's §9 destroys this with a single observation:

> "**There is no off-the-shelf A2A server that wraps any of the coding agents conversus would actually dispatch to.** If conversus ships an A2A provider today, it will have nothing on the other end of the wire that speaks A2A natively — someone (probably conversus maintainers) has to build the wrapper." (researcher §9)

And §10's mapping table lists every mainstream coding agent with "A2A server? → **No**" in every row. Every single one.

So the actual math under the advocate's proposal is:

- `conversus-provider-a2a` (~200 lines)
- **Plus** a `conversus-a2a-server-for-claude` wrapper we ship ourselves
- **Plus** a `conversus-a2a-server-for-aider` wrapper we ship ourselves
- **Plus** a `conversus-a2a-server-for-opencode` wrapper we ship ourselves
- **Plus** a `conversus-a2a-server-for-copilot` wrapper we ship ourselves
- **Plus** lifecycle management for N long-lived A2A server subprocesses
- **Plus** auth, health-checking, restart, port allocation, discovery config for each

This is not "zero lines of conversus code per tool". It is "more lines per tool than a direct provider, plus an HTTP server, plus a subprocess lifecycle manager, plus a registry". The "community wraps once" hand-wave is precisely the empty ecosystem the researcher documents. **There is no community wrapping anything yet.** The advocate is proposing that *we* become that community — which means writing every wrapper we would have written as a direct provider, plus an HTTP layer on top.

The build-our-own path writes a 100–200 line direct adapter once. The A2A-first path writes a 100–200 line server wrapper plus an HTTP client plus orchestration scaffolding. The advocate's claim that A2A reduces total code is only true in a future where someone else has already paid the wrapping cost. **In 2026-04, no one has.**

---

## 3. "Every future provider is A2A-native" — false per the research

Advocate §2.3 asserts a near-term future where the A2A ecosystem auto-populates:

> "Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships."

This is framed as if we can expect coding agents to ship A2A endpoints. The researcher addressed this directly:

> "**Reference implementations**: Google ADK, IBM BeeAI, LangGraph integration. **No Anthropic/Claude Code reference. No GitHub/Copilot reference. No Aider reference. No OpenCode reference.**" (researcher §9)

> "Framework integrations in Google ADK, LangGraph, BeeAI. **No major agent SDK has shipped an A2A server wrapper for itself yet.**" (researcher §6.2)

The three A2A reference implementations (Google ADK, IBM BeeAI, LangGraph) are *agent frameworks*, not coding agents. They are competitors to CrewAI and AutoGen. They are not the tools conversus needs to dispatch to. Conversus dispatches to Claude Code, Aider, OpenCode, Copilot CLI, Codex CLI, Gemini CLI, Continue — and **zero** of those ship or have announced an A2A server.

The advocate also lists the Linux Foundation coalition (§2.1) as evidence A2A will win:

> "Google + IBM + Linux Foundation is the exact pattern that produced every standard we currently rely on — Kubernetes, OpenTelemetry, gRPC, OCI."

The pattern is real, but the timescale is wrong. Kubernetes took years to reach the "every vendor ships a compatible implementation" state. gRPC took years. OpenTelemetry took years. A2A merged with IBM ACP in August 2025 (~8 months ago) and shipped 1.0.0 a month ago. The researcher characterizes the Python SDK as "0.3.25 stable, 1.0.0a0 alpha" and warns "This is early." (researcher §6.2). **The standards-coalition argument is an argument for investing in A2A in three years, not betting on A2A being the substrate we build on today.**

The advocate tries to pre-empt this with "we are in April 2026, A2A has had 12 months of stabilization". That is true about the *wire protocol*. It is not true about the coding-agent ecosystem that would consume that protocol — which researcher §10 documents as "no A2A servers exist". The wire protocol being stable is necessary but not sufficient; the peers have to exist.

---

## 4. The 6-month deletion timeline — aspirational future, their own words

Advocate §2.5 attacks the hybrid path for deferring A2A:

> "The research report's §Candidate C explicitly says 'Phase 3 (Future, ~6 months): Implement A2A protocol support.' **Six months of writing code that is scheduled to be replaced is not pragmatism — it is hedging that costs more than committing.**"

The advocate's own commitment list in §5 contains the same six-month problem *dressed differently*:

> "Implement the `claude-code` direct provider ONLY as a fast-path optimization for users who do not want to run a local A2A server. It is a convenience, not an architectural pillar. **Its public surface matches the A2A server wrapper so users can migrate.**"

Read that carefully. The advocate is proposing:

1. Build a `claude-code` direct provider (yes, they concede this)
2. Build a separate A2A server wrapper for Claude Code
3. Make them API-compatible so users "migrate"
4. Eventually deprecate the direct one

That is **exactly** the ~6-month deletion timeline the advocate just called "hedging that costs more than committing". They are doing the same hedge, just in a more expensive form:

- **Hybrid advocate plan**: 1 direct Claude Code provider + 1 future A2A provider = 2 artifacts
- **A2A advocate plan**: 1 direct Claude Code provider + 1 A2A server wrapper for Claude Code + 1 A2A client provider = **3 artifacts**, all maintained in parallel, all needing to stay API-compatible

And the build-our-own plan I'm defending? 1 direct Claude Code provider today, plus 1 A2A client provider when the ecosystem has peers. Total artifacts over the lifetime: 2, same as hybrid, 33% fewer than the A2A-first proposal.

The advocate's "commit now, don't hedge" rhetoric is unreconciled with their own implementation plan, which hedges harder than either alternative. Either their rhetoric is right and they should delete the direct `claude-code` provider from their §5 commitment list (which would break spec 042 on day one, because no A2A server for Claude Code exists), or their implementation plan is right and the rhetoric about "no hedging" is empty. They cannot have both.

**This is the same aspirational-future critique I make in §3.4 of my own review**, applied back to them. Waiting for A2A peers is not different in kind from waiting for LiteLLM's missing agent-runtime features. Both are bets on ecosystem work someone else has to do.

---

## 5. What I want to INCORPORATE from their position

Credit where it is due: the A2A advocate makes several forward-looking observations that are genuinely correct and that strengthen my own plan when I absorb them. I want to be explicit about what I am taking.

### 5.1 A2A is the right long-term target for agent-to-agent dispatch

The advocate's §2.4 composability argument — "agents calling agents" — is real. For spec 048's autonomous governance mode, the ability for an arbiter agent to recursively dispatch to specialized agents (CVE lookup, OWASP reference, etc.) via a standard protocol is genuinely valuable. A2A is the correct substrate for that, in the limit. My own review already acknowledges this at §3.4: *"when A2A/ACP matures, we add an `acp` provider"*. I want to go further and commit: **when a critical mass of A2A-wrapped coding agents exists (defined as: at least 3 of {Claude Code, Aider, OpenCode, Copilot, Codex, Gemini} ship A2A endpoints), the `a2a` provider becomes our recommended path for agent-to-agent composition.**

That is not the same as making A2A the foundation today. It is a commitment to make A2A a first-class provider on a triggered condition. Spec 042 §11 already lists `a2a` (corrected name) as the first row of the provider matrix; I endorse elevating it to "recommended" once the precondition holds.

### 5.2 The Agent Detail / runtime-discovery pattern is worth borrowing

The advocate's §2.2 point about discovery — that hardcoded provider lists age poorly, and A2A's Agent Detail metadata enables extensible agent registries — is a good architectural observation. **Our own protocol should accommodate this pattern.** Concretely, the `PROVIDER_REGISTRY` dict in spec 042 §5 should be extensible at runtime (not just at compile time) so that a future `a2a` provider can register discovered agents dynamically. That is a small protocol refinement: add a `register_provider(name, instance)` hook to the registry module. It costs nothing today and makes the A2A transition trivial tomorrow.

This is the build-our-own-contains-everything framing in action: the A2A advocate is right that *some* workloads will want URL-based agents. Our protocol does not prevent that. It just does not *mandate* it for workloads that don't need it.

### 5.3 A2A server wrappers are valuable community artifacts

Advocate §2.3's observation that "wrapping Claude Code as an A2A server is valuable to every A2A client in the world, not just conversus" is correct. If and when we write one, it *should* be packaged as a standalone artifact reusable outside conversus. But — critically — this is a **deployment decision**, not a **protocol decision**. We can ship `conversus-a2a-server-for-claude` as a separate PyPI package whose implementation happens to be "spawn claude CLI, translate A2A Task Request to `claude -p` flags". The build-our-own protocol does not prevent this; in fact, it's how an A2A server wrapper would be implemented *anyway* (someone has to call the `claude` CLI; that someone has to use something like our `ClaudeCodeProvider` under the hood).

**The A2A server wrapper and the `ClaudeCodeProvider` are not competing artifacts — the first is built on top of the second.** I am happy to ship both when the demand exists. The build-our-own path is the layer the A2A wrapper sits on.

### 5.4 Spec 042 §2 rename — ACP → A2A

The advocate (perhaps inadvertently) raises a genuine spec-hygiene issue: spec 042 currently says "ACP" in places where it means "A2A" and in other places where it means "Zed/JetBrains Agent Client Protocol". Per the researcher's §6.4:

> "Rename the 'ACP provider' to 'A2A provider' (or more explicitly, `a2a` using `a2a-sdk`). Explicitly distinguish from the Agent Client Protocol (Zed/JetBrains) — which is a *different* integration vector."

**I accept this correction and propose we rename the §11 row from `acp` to `a2a` in the provider matrix**, and add a separate (lower-priority) row for `zed-acp` as an IDE integration vector. This is a small spec edit that clarifies the roadmap without changing the architecture. Both advocates' positions improve with this rename.

---

## 6. The correct role for A2A in the architecture

Putting it all together, here is how A2A fits into the build-our-own plan — not as an opponent of it, but as a first-class citizen of it:

| Layer | Owned by | Stable? | When |
|---|---|---|---|
| Conversus engine (phase dispatch, templates, variables) | Us | Yes, today | Shipped |
| `ExecutionProvider` Protocol (our 4-method interface) | Us | Yes, ~40 lines | Spec 042 v1 |
| `mock`, `anthropic`, `claude-code` providers | Us | Yes, ~500 lines total | Spec 042 v1 |
| `litellm`, `openai`, `gemini` providers (direct API) | Adapters | Additive | Spec 042 v1 or soon after |
| `opencode` provider (HTTP client, OpenAPI-generated) | Adapters | Additive | When demand arrives |
| `a2a` provider (calls a2a-sdk) | Adapters | **Additive** | **When A2A peers exist** |
| A2A server wrappers (`conversus-a2a-server-for-claude`, etc.) | Separate artifacts, built on our providers | **Additive** | **When community demand arrives** |
| `zed-acp` IDE integration | Separate track | Future | Spec 042 §12 Q8 |

**A2A is a provider. A2A server wrappers are downstream artifacts. Neither is the foundation.** The foundation is a 40-line `Protocol` that has no runtime dependencies and to which every runtime — direct SDK, LiteLLM, OpenCode HTTP, A2A HTTP — attaches as an adapter.

The A2A advocate's mistake is treating the wire protocol as the abstraction layer the engine should commit to. But the engine does not speak HTTP, does not speak JSON-RPC, and does not need to. The engine speaks "give me a string prompt and a list of read paths, write the result to this output path". That is an in-process Python Protocol, not a wire format. Committing the in-process Python Protocol to match an external wire protocol's current shape would couple us to a 1.0.0-released-last-month standard *inside our own codebase*, which is exactly the kind of coupling the advocate themselves warns against in §2.5 ("code written against a deprecating abstraction is technical debt").

Our Protocol is stable because it is minimal, internal, and owned. A2A is a provider inside that Protocol. When A2A matures, A2A wins — **inside our plan**.

---

## 7. Where the advocate is gracious-points right

To be fair and not strawman:

- **A2A as a future dispatch standard**: Correct. I agree and list `a2a` as a first-class provider row.
- **Composability / recursive dispatch for spec 048**: Correct and valuable. Our protocol does not prevent it; when A2A matures, the `a2a` provider unlocks it.
- **Runtime discovery via Agent Detail**: A good pattern. I want to accommodate it via a registry-extension hook.
- **Wrapping coding agents as A2A servers is a community good**: Correct, and those wrappers can be built *on top of* our direct providers. They are not opposed to the build-our-own plan.
- **Spec 042's "ACP" naming is ambiguous and should be tightened**: Correct, per the researcher. We should rename to `a2a` and separately track Zed/JetBrains ACP.

The advocate is an accurate read of the direction of travel. They are wrong about the timescale, wrong about conflating two protocols, and wrong about treating a wire protocol as an internal abstraction. Those are the disagreements.

---

## 8. Conclusion

The A2A advocate's position survives as a **future-facing provider roadmap commitment**, not as a foundation. The researcher's finding that no coding agent ships an A2A server today is fatal to the "one provider, every tool" economics *in the present tense*. The advocate's own commitment list (§5, "ship both a direct Claude Code provider and an A2A server wrapper for Claude Code") hedges in the same way they accuse the hybrid advocate of hedging — and more expensively.

What we should take from them:
1. Name the provider `a2a`, not `acp`, and separate it from Zed/JetBrains ACP in the spec.
2. Make the `PROVIDER_REGISTRY` extensible at runtime so A2A-style discovery is natural.
3. Pre-commit that when A2A reaches critical peer mass, `a2a` becomes the recommended provider for agent-to-agent composability.
4. Package any future A2A server wrappers as standalone community artifacts built on top of our direct providers.

What we should reject:
1. Making A2A the foundation today.
2. Pretending Zed/JetBrains adoption is A2A adoption.
3. Accepting the "zero lines of conversus code per tool" math before any A2A peers exist.
4. Treating our internal Python Protocol as something that should match an external wire format's shape.

**The build-our-own plan already contains everything the A2A advocate wants — as an additive downstream provider. Their position becomes my §11 matrix row when A2A grows up. They are not proposing a different architecture; they are proposing a different ordering. The researcher's facts make that ordering wrong.**

Build the protocol. Ship the direct providers. Add `a2a` to the matrix. Let A2A win as a provider when its ecosystem is real.

---

**Files referenced**:
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/review.md`
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/backbone-researcher/review.md` (§0, §6, §6.2, §6.3, §6.4, §9, §10)
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/build-our-own-advocate/review.md` (§3.4, §4, §11)
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/spec.md` (§2, §3, §5, §11, §12)
