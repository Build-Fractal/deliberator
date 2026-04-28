# Cross-Review: LiteLLM-Hybrid Advocate

**Reviewer**: a2a-future-advocate
**Target**: litellm-hybrid-advocate
**Round**: 1, Phase 2 (cross-review)
**Date**: 2026-04-03

---

## 0. Framing — this is a sequencing debate, not a religious war

I want to start by conceding something my Round 1 review was too combative to say clearly: **the LiteLLM-hybrid advocate is mostly right about April 2026.** Their review is well-argued, well-cited, and matches the backbone researcher's ground truth on several load-bearing points. If you forced me to ship spec 042 next Monday, I would not ship pure A2A — I would ship something that looks a lot like what they are proposing.

The real disagreement is not "which approach is correct" but "what time horizon are we optimizing for, and what does the path between horizons look like?" My Round 1 position read as *A2A instead of hybrid*. On reflection, the stronger position is *hybrid today, A2A tomorrow, and the shape of today's code determines whether tomorrow is cheap or expensive*.

Below I work through the five questions in order and try to be honest about where the hybrid advocate is correct, where my critique stands, and where I need to update.

---

## 1. Can both be true? The pragmatic/strategic split

**Yes. Both can be true, and the hybrid advocate's case for "today" is stronger than my Round 1 review admitted.** The backbone researcher establishes three facts that are fatal to a "pure A2A now" position:

1. **No counterparties exist.** §10 of the backbone report: *"no off-the-shelf A2A server that wraps any of the coding agents conversus would actually dispatch to."* Claude Code, Aider, Copilot, Codex, Gemini CLI, OpenCode — zero A2A servers among them. If conversus ships a `acp`/`a2a` provider in April 2026, the wire is there but there is nothing on the other end until conversus maintainers write the wrappers themselves.
2. **The Python SDK is still pre-1.0.** `a2a-sdk` is 0.3.25 stable with 1.0.0a0 alpha. The protocol spec v1.0.0 dropped less than a month ago (2026-03-12). My Round 1 review waved this away as "twelve months of stabilization" — I was double-counting. The protocol merger happened in August 2025, but the Python SDK being usable for production headless dispatch is much more recent than that.
3. **Spec 048 is blocked on 042 as a HARD dependency.** Every week 042 slips, governance mode slips. Burning 2–3 extra weeks on an A2A-only path that then needs wrapper code conversus has to write anyway is, in fact, shipping slower for no near-term gain.

The hybrid advocate reads those three facts and concludes "don't bet on A2A now." That conclusion is correct for the **implementation** of spec 042. Where I want to push back is on the **architecture** of spec 042 — specifically on whether the `ExecutionProvider` protocol that lands in Week 1 is *shaped like A2A* or *shaped like the lowest-common-denominator of bespoke SDKs*. That is the load-bearing question, and the hybrid advocate's review does not answer it.

So: LiteLLM-hybrid today AND A2A tomorrow is not just possible, it is probably the right plan. The remaining question is whether the hybrid's Week 1 design choices make the A2A migration in ~12–18 months cheap or expensive.

---

## 2. Does LiteLLM-hybrid permanently lock conversus into the Tier 3 / Tier 1-2 split?

**No, but only if the `ExecutionProvider` protocol is designed with A2A's semantics as the target shape from day 1.** This is where I disagree with the hybrid advocate's review most sharply, and I think the disagreement is substantive rather than rhetorical.

The hybrid advocate says (§4): *"The `ExecutionProvider` protocol itself... is conversus's intellectual property — the shape of `execute()`, `execute_batch()`, `supports_tool_use`, `ExecutionTask`, `ExecutionResult`. LiteLLM does not and should not own this. We own the abstraction; we rent the implementation for one tier."*

I agree with this exactly. But the review stops there. It does not ask **what shape** that protocol should take. And the shape matters enormously for whether the eventual A2A addition is a `LiteLLMProvider`-parallel 14-line adapter or a retrofit that breaks every existing provider.

Concretely: spec 042 §2 already maps conversus concepts 1:1 to A2A Task Requests. The fields a Task Request has (text parts, reference parts, metadata, streaming updates, async push notifications, agent detail) are a superset of what LiteLLM's `completion_async()` exposes. If conversus designs `ExecutionTask` and `ExecutionResult` around LiteLLM's shape (messages list, response, cost) because "LiteLLM covers 70%," the protocol will quietly ossify around model-API semantics and will need breaking changes when A2A arrives. If conversus designs `ExecutionTask` around A2A Task Request semantics (structured parts, references, metadata, streaming) and implements `LiteLLMProvider` as a *narrower adapter* that maps the A2A shape onto LiteLLM's shape, then:

- Week 1 still ships LiteLLM-over-Tier-3 on the hybrid advocate's timeline.
- The `acp` provider in Phase 3 is ~30–50 lines because the engine already speaks A2A-shaped envelopes.
- Every Tier 1–2 bespoke adapter (Claude Code, OpenCode, Aider) is a *downward* translation from A2A shape to the underlying CLI/HTTP, which is the same direction as the eventual A2A-server wrapper would go.

The hybrid review does not take a position on this. In the absence of a position, the default will be to shape the protocol around what LiteLLM returns — because that is what Week 1 ships. **That is the lock-in risk.** Not "we depend on LiteLLM," but "we depend on LiteLLM's shape leaking into the abstraction."

**My revised position**: I am no longer asking to skip the hybrid. I am asking to adopt the hybrid's implementation plan with one architectural constraint — design `ExecutionTask`/`ExecutionResult` around A2A Task Request semantics, not around LiteLLM's `completion_async` shape. That makes the hybrid's "Phase 3 (Future)" a matter of adding one more implementation of an existing protocol, not a rewrite.

---

## 3. Is the "splits the abstraction in three" critique fair?

**Partially fair, but my Round 1 phrasing was too strong.** Let me rework it honestly.

My Round 1 review said the hybrid "splits the abstraction in half" / "in three mental models: LiteLLM's `completion_async`, the ExecutionProvider protocol for direct SDKs, and A2A eventually." Reading the hybrid advocate's actual proposal, that critique misses: the hybrid is *one* abstraction (`ExecutionProvider`) with *multiple implementations* (LiteLLM, Claude Code subprocess, OpenCode HTTP, eventually A2A). That is not three abstractions. That is one abstraction with a healthy plugin architecture, which is exactly what spec 042 §3 already specifies.

The better framing is the one the caller suggested: **"LiteLLM is good for direct APIs, agent runtimes need different treatment, and A2A unifies both eventually."** I accept this framing. It is more accurate than mine and more useful for planning. Three observations follow:

1. **LiteLLM is genuinely the right tool for Tier 3 *today*.** I undersold this in Round 1. 100+ providers, automatic format conversion, built-in retry/rate-limit/cost tracking, 14-line adapter. The hybrid advocate is not wrong to call rewriting this "malpractice." I withdraw the implied claim that LiteLLM is optional scaffolding — it isn't, for the 12-month horizon.
2. **Agent runtimes (Tier 1-2) genuinely need different treatment *today*.** The backbone researcher confirms this: every shipping agent runtime has a bespoke dispatch mechanism (subprocess + CLI flags, or HTTP in OpenCode's case). There is no shared layer. The hybrid advocate is correct that conversus has to write Claude Code / OpenCode / Aider adapters regardless of approach.
3. **A2A is the unification layer the industry is heading toward but has not arrived at.** The backbone researcher is explicit: Python SDK 0.3.x stable, protocol v1.0.0 one month old, zero coding-agent wrappers exist. My Round 1 characterization of A2A as "mature enough to bet on" overstated the case. It is mature enough to design toward, not mature enough to depend on.

So the accurate three-part statement is:

- **Tier 3**: LiteLLM today, A2A-server-fronted LiteLLM tomorrow (an implementation detail).
- **Tier 1-2**: bespoke adapters today, A2A-server wrappers tomorrow (the same SDK code with an HTTP server around it).
- **The `ExecutionProvider` protocol**: shaped like A2A Task Request semantics from day 1 so tomorrow's migration is mechanical.

---

## 4. Is LiteLLM-hybrid STRICTLY BETTER TODAY given the empty A2A ecosystem?

**Yes. I concede this.** The empty ecosystem finding is load-bearing. My Round 1 review had the backbone researcher's facts but did not reckon with them honestly.

Specifically, the hybrid advocate is correct on every "today" claim:

- Time-to-ship: hybrid is ~3 weeks, pure-A2A-first is longer because conversus has to build the wrappers nobody else has built.
- Operational simplicity: LiteLLM is a library call, not a sidecar fleet. CI runners do not want to spin up long-running A2A servers for a one-shot `conversus governance --gate pr`.
- Risk profile: LiteLLM's supply chain risk is Low-with-mitigation per the research report's own risk matrix; A2A's ecosystem-maturity risk is Medium-with-no-mitigation for coding agents specifically, because the mitigation (wrappers exist) is precisely what is missing.
- Spec 048 unblock: every week matters.

The only place I will not concede "strictly better" is the architectural-shape question from §2 above. The hybrid advocate's review does not take a position on the shape of `ExecutionTask`/`ExecutionResult`, which means "the hybrid proposal as written" is *not quite* strictly better — it is strictly better on implementation but silent on protocol shape. A version of the hybrid that explicitly designs the protocol around A2A Task Request semantics is strictly better. A version that designs the protocol around LiteLLM's `completion_async` shape is strictly better today but accumulates migration debt.

In the language of the question: yes, LiteLLM-hybrid is strictly better today. The path from today to tomorrow is where the care needs to go.

---

## 5. What should a revised A2A position incorporate from LiteLLM's strengths?

Five concrete things. I think each of these is a Pareto improvement over my Round 1 review.

### 5.1 Use LiteLLM inside the engine as the Tier 3 implementation

The hybrid advocate is right that rewriting 144 cells of provider-specific glue (auth, envelopes, parsing, streaming, rate limits, cost tables) is malpractice. A revised A2A position accepts LiteLLM as the *default implementation* of any direct model-API provider. The question is whether the engine exposes it as `LiteLLMProvider` (a named provider in `PROVIDER_REGISTRY`) or as an internal detail of a generic "direct model API" provider. Either is fine; I have no strong preference. The strong form of my original objection — "don't use LiteLLM" — was wrong. I withdraw it.

### 5.2 Treat A2A as "the protocol the abstraction is shaped like," not "the provider we ship first"

My Round 1 review conflated two things: (a) the design of `ExecutionProvider` as a protocol, and (b) the existence of an `acp`/`a2a` provider implementation. These are separable. You can design the protocol around A2A semantics and not ship an `acp` provider on day 1. You can ship an `acp` provider later as just one more implementation. This is exactly the "Phase 3" the hybrid advocate's review lays out — I was attacking it for being too late, but what matters is that the protocol shape in Week 1 makes Phase 3 cheap. The implementation timing is not the disagreement; the protocol shape is.

### 5.3 Ship LiteLLM fronted by an A2A server as the reference Tier 3 A2A implementation

This is the synthesis move I missed in Round 1. When the A2A ecosystem matures (estimate: 12–18 months based on SDK version trajectory and protocol v1.0.0 age), conversus does not need to write a separate "A2A for models" path. It takes the existing `LiteLLMProvider` implementation and wraps it as an A2A server. The `a2a-sdk`'s FastAPI/Starlette backend does the HTTP layer; LiteLLM does the model call; one reference artifact fronts every Tier 3 provider at once. **Reusable outside conversus.** Any A2A client in the world can now dispatch to any LiteLLM-supported model via a single server. That is the kind of thing that gets upstreamed to the `a2a-project` org as a reference implementation and earns conversus ecosystem credibility.

### 5.4 Ship the Claude Code direct provider with an A2A-shaped public surface

The hybrid advocate proposes Week 2 builds `conversus-provider-claude-code` as a subprocess wrapper over `claude -p --bare`. Good — this matches the backbone researcher's recommendation (§11 item 8). My revision: design the provider's `ExecutionTask`/`ExecutionResult` conversion to mirror A2A Task Request / streaming update shapes, so that `conversus-acp-claude` (the future A2A-server wrapper of Claude Code) is a thin HTTP shell around the same internal functions. Zero rewrite. The A2A-server artifact becomes a by-product of the direct provider, not a parallel codebase. This is the "write it once, reuse it" dividend I argued for in Round 1 — but I was wrong to argue it has to happen on day 1. It has to be *possible* on day 1, via protocol shape.

### 5.5 Leave the `acp`/`a2a` provider for Phase 3 as the hybrid advocate proposes

I concede the timing. My Round 1 "ship A2A first" demand was wrong given the empty ecosystem. The correct order is:

- **Week 1**: `ExecutionProvider` protocol shaped around A2A Task Request semantics + LiteLLM implementation for Tier 3.
- **Week 2**: Claude Code subprocess provider with A2A-shaped internal structure.
- **Week 3**: tests, docs, OpenCode HTTP provider if time permits.
- **Phase 2 (post-042)**: OpenCode HTTP, Aider subprocess, Copilot subprocess as bespoke providers.
- **Phase 3 (~12 months, when A2A ecosystem has wrappers)**: `a2a` client provider + LiteLLM-fronted A2A server as reusable artifacts.
- **Phase 4 (~18–24 months)**: migrate Tier 1-2 bespoke providers behind A2A-server wrappers, retire direct subprocess paths as the ecosystem shifts.

This is essentially the hybrid advocate's plan with three additions: (1) explicit protocol shape constraint, (2) explicit A2A-server-wrapping strategy for each Tier 1-2 provider as a by-product, (3) explicit migration plan for retiring direct paths once A2A wrappers exist. None of these slow down Week 1.

---

## 6. Where I still disagree with the hybrid advocate

Three residual disagreements, ranked by importance.

**6.1 The hybrid advocate's silence on protocol shape is the biggest risk.** Their review treats `ExecutionProvider` as "conversus's IP" and moves on. But the shape of that IP determines whether Phase 3 is a bolt-on or a rewrite. A conversus maintainer reading the hybrid advocate's review might reasonably design `ExecutionTask` as `{messages: list, model: str, tools: list}` — the LiteLLM shape — because that is what Week 1 ships. The right shape is closer to `{parts: list[Part], references: list[Reference], metadata: dict, agent_capabilities: list}` — the A2A Task Request shape — with LiteLLM adapting down from that. **The review should take a position on this and does not.**

**6.2 "Hybrid doesn't close the door on A2A" is weaker than "hybrid keeps the door open cheaply."** The hybrid advocate says (§5.2): *"The hybrid approach doesn't close the door on A2A. It explicitly leaves it open as Phase 3."* Technically true. But "door open" is not the same as "door cheap to walk through." If the abstraction ossifies around LiteLLM's shape in the first three weeks, the door is open but walking through it means a protocol migration. If the abstraction is A2A-shaped from day 1, walking through is adding one more provider file. This is a concrete engineering difference the review does not engage with.

**6.3 I still think the Agent Detail / runtime discovery story is load-bearing for spec 048 and the hybrid review ignores it.** The hybrid advocate's spec-048 argument is "every hour spent on LiteLLM glue is an hour not spent on governance features" — which is fair as a budget argument. But spec 048's `.conversusrc` has a `default_agents:` field that lists hardcoded preset names. That works for v1. It does not scale to "teams add custom governance agents without a conversus release," which is the long-term governance vision in spec 048 §10 Q4 (multi-repo governance) and §11 (IDE plugins via JetBrains ACP). A2A Agent Detail discovery is how that scales. The hybrid advocate's plan does not forbid this future — but it also does not design for it, and the longer the hardcoded `default_agents:` list lives, the more it becomes the default mental model for governance configuration. This is a soft concern, not a blocker for spec 042 shipping, but it is the part of my Round 1 review I still think is unanswered.

---

## 7. Proposed synthesis — what I will push for in the deliberation

Take the hybrid advocate's implementation plan verbatim, but add three amendments:

1. **Protocol shape amendment**: `ExecutionTask` and `ExecutionResult` are designed around A2A Task Request / streaming update semantics. `LiteLLMProvider` adapts down from this shape to `completion_async`. Document this choice in spec 042 §3 with a note that the shape is chosen to make the eventual A2A provider a trivial addition. Cost: ~4 hours of extra design in Week 1.
2. **By-product artifact amendment**: Each Tier 1-2 provider is written such that its core dispatch function (prompt → result) can be trivially wrapped as an A2A server later. No extra code in Week 1-3; just a structural constraint on how the functions are organized. When Phase 3 arrives, `conversus-acp-claude`, `conversus-acp-opencode`, `conversus-acp-aider` are 30–50 line HTTP shells over existing internal functions. Cost: ~2 hours of extra design per provider.
3. **Phase 3 commitment amendment**: Spec 042 explicitly schedules the `a2a` client provider and the A2A-server reference wrappers for ~12 months post-042 ship, not "someday." Tie this to a concrete trigger: when `a2a-sdk` reaches 1.0 stable and when the first third-party A2A wrapper of a coding agent ships. Cost: zero today; prevents the "Phase 3 (Future)" from becoming "Phase 3 (Never)."

These amendments cost maybe ~2 days of engineering thought across all of Week 1-3. They preserve every hybrid advocate timeline commitment. They close my biggest concern from Round 1. **If the hybrid advocate accepts these three amendments, I think we have a position both of us can sign.**

---

## 8. Summary

- The hybrid advocate is right about April 2026. I was too strong in Round 1.
- The empty A2A coding-agent ecosystem is a decisive fact. Shipping A2A-first in April 2026 means building wrappers nobody else has, which defeats the point of targeting a standard.
- LiteLLM is genuinely the right tool for Tier 3 today. I withdraw the implied "don't use LiteLLM" position.
- The sequencing is: hybrid implementation today, A2A protocol shape today, A2A provider in Phase 3 (~12 months), A2A-server wrappers as by-products of existing providers rather than parallel code.
- My biggest remaining concern is protocol shape, not implementation timing. The hybrid advocate's review does not take a position on protocol shape; if the default ends up being "shaped like LiteLLM's response," the Phase 3 migration gets expensive.
- Three concrete amendments to the hybrid plan cost ~2 days total and resolve the shape-ossification risk.

**The path from LiteLLM-hybrid to A2A is: same implementation plan, A2A-shaped protocol in Week 1, A2A-friendly structure in the Tier 1-2 adapters, scheduled migration when the ecosystem has counterparties.** That is the synthesis I should have proposed in Round 1 and did not.

---

**Files referenced**:
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/litellm-hybrid-advocate/review.md` (full review)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/backbone-researcher/review.md` (§9 A2A maturity, §10 tool mapping, §11 neutral observations)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/review.md` (my Round 1 position being revised)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/spec.md` (§2 Protocol Alignment, §3 ExecutionProvider protocol, §11 Provider Matrix, §12 Open Questions)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/048-autonomous-governance-mode/spec.md` (§3 .conversusrc, §10 Q4 multi-repo governance, §11 execution surfaces)
