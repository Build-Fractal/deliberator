# a2a-future-advocate — Phase 4 Closing Argument

**Advocate**: a2a-future-advocate
**Phase**: 4 (Closing Arguments / Disputes)
**Round**: 1
**Date**: 2026-04-05

---

## Preamble — what this closing is and is not

This is not a bid to win winner-take-all. "Ship A2A first" died in Phase 2, and "wrap Claude Code as an A2A server in v1" died in Phase 3. What I am defending in this closing is narrower and harder to dismiss: **three future-proofing commitments that neither build-our-own nor litellm-hybrid currently makes in their v1 plans**, and that cost the winner almost nothing to adopt.

The arbiter's Phase 6 template explicitly permits incorporating elements from losing positions into the winner's ruling. This document is engineered for that. I am asking the arbiter to bind the winner — whoever that is — to the three claims below. If the winner's implementation plan already contains them implicitly, the arbiter loses nothing by making them explicit. If it does not, the cost of adding them is measured in hours and one schema field.

---

## Head-to-Head Scorecard

Seven criteria, weighted for long-term architectural soundness and downstream-spec compatibility. I score myself honestly — I lose on v1 velocity and current ecosystem coverage, and I will not pretend otherwise. I score myself Strong on the three criteria where my Phase 3 revision held.

| Criterion | Weight | a2a-future-advocate (me) | build-our-own-advocate | litellm-hybrid-advocate | backbone-researcher |
|---|---|---|---|---|---|
| **v1 shipping velocity** (Can we ship spec 042 in 2026-04, unblocking spec 048?) | High | **Weak** — my Round 1 "ship A2A first" was indefensible; even my Phase 3 revision has nothing unique on the v1 critical path | **Strong** — 4 providers (`mock`, `anthropic`, `claude-code`, `opencode`) shipping on a 4–6 week plan, realistic LoC | **Strong** — 3 providers (`mock`, `claude-code`, `litellm`) on a 3 week plan, smaller v1 surface | N/A — non-advocacy |
| **Current ecosystem coverage** (Does the plan serve 2026-04 users with production-ready providers?) | High | **Weak** — A2A coding-agent ecosystem is empty; I cannot name a single counterparty | **Strong** — subprocess CLI is the de facto backbone across 6 shipping agents | **Strong** — LiteLLM alone covers 100+ model APIs, Tier-3 is free | N/A |
| **Long-term protocol durability** (Will the `ExecutionTask`/`ExecutionResult` shape still fit 2027–2028 workloads without breaking changes?) | High | **Strong** — my Phase 3 revision is the only position that asks the question; A2A Task Request semantics (structured parts, references, metadata, streaming) is the only shape in the 2026-04 landscape that accommodates every known future provider | **Adequate** — defines the protocol in ~40 lines but takes no position on field shape; "conversus owns the protocol" is true but silent on *what shape* | **Adequate** — explicitly accepts my ~4-hour amendment in their revision §Rebuttals but does not bind it | N/A |
| **Spec 048 discovery enablement** (Does the plan keep `.conversusrc::default_agents` forward-compatible with URL-addressable agents?) | High | **Strong** — only position proposing the `default_agents` URL-entry schema change, with "not yet supported" error in v1 | **Adequate** — accepted the `register_provider_instance()` runtime-extension hook in §Registry but did not propagate to spec 048's `.conversusrc` schema | **Weak** — revision explicitly defers runtime discovery to Phase 3 "out of scope for v1 by spec definition" | N/A |
| **Protocol-shape one-way door awareness** (Does the plan recognize that `ExecutionTask`/`ExecutionResult` is a non-reversible decision?) | High | **Strong** — this is my surviving Phase 3 thesis; I am the only advocate who named the one-way door explicitly | **Weak** — silent on field-shape choices; treats the protocol as a 40-line interface and moves on | **Adequate** — their Phase 3 §Rebuttals accepted the protocol-shape amendment as "4 hours of design notes" but did not make it a binding deliverable | N/A |
| **Ground-truth factual grounding** (Does the plan respect the backbone-researcher's §5 non-negotiables?) | High | **Adequate** — I violated §5.2 (empty A2A ecosystem) in Round 1, conceded fully in Phase 2, and my Phase 3 revision respects every §5 constraint | **Strong** — revision cites researcher findings as load-bearing; `claude-agent-sdk` dropped, `acp` row split, subprocess baseline accepted | **Strong** — same; LiteLLM operational posture independently verified by researcher | **Strong** — the source of the constraints |
| **Simplicity of v1 plan** (How much code ships, how many moving parts?) | Medium | **Weak** — my Phase 3 plan adds ~4 hours of protocol-shape design + ~20 lines of `.conversusrc` schema, but the main build is still someone else's plan | **Adequate** — 4 providers, 2 base classes (SubprocessProvider, HTTPProvider), ~1000–1200 LoC | **Strong** — 3 providers, 1 base class, smallest v1 surface of any plan | N/A |

### Weighting rationale

The top four criteria (v1 velocity, current coverage, long-term durability, spec 048 enablement) are all weighted High because spec 042 is a **load-bearing dependency** for specs 040, 043, 044, 046, and 048. A plan that ships fast but forecloses downstream work is a Pyrrhic victory. A plan that defers everything is no plan. The decision space is bounded by "ship something that works in 2026-04 AND survives until 2028."

I lose on shipping velocity and current coverage. I acknowledge this cleanly. I win on three forward-looking criteria that the other advocates have not prioritized because they are architecturally correct but not flashy. That is the honest picture.

Protocol-shape one-way door awareness is weighted High because **it is the one decision the winner cannot undo**. Every other deliberation outcome is additive or deletable. `ExecutionTask.parts` vs `ExecutionTask.prompt: str` is not.

---

## Conceded Weaknesses

I concede every weakness raised in Phase 2 and Phase 3 against my Round 1 position. These concessions are extensive. They also do not touch my three Phase 3 held claims.

### Round 1 overreach — SIGNIFICANT severity, bounded to Phase 1

1. **"The A2A coding-agent ecosystem exists"** — raised by backbone-researcher §9, build-our-own §2, litellm-hybrid §1. I claimed an ecosystem that did not exist. Conceded in Phase 2. Severity: significant, decisive against "ship A2A first." Bounded to Round 1; does not touch my Phase 3 held claims.

2. **"ACP is one protocol" — conflation of Google/IBM A2A with Zed/JetBrains Agent Client Protocol** — raised by backbone-researcher §6, universally ratified. I propagated spec 042's ambiguous "ACP" language. Conceded cleanly in Phase 2. The correction is now a joint-ratified spec edit. Severity: significant in framing, zero impact on the three held claims (which are all A2A-specific, not ACP-ambiguous).

3. **"Every future coding tool will be A2A-native"** — speculation presented as forecast. Raised by all three Phase 2 attacks. I had no evidence. Conceded. Severity: significant as a reason to delay v1; zero impact on the held claims.

4. **"30-line wrapper for Claude Code A2A server"** — factual error. The backbone-researcher's §4.2 established 300–600 lines as the realistic number. Conceded in Phase 3. Severity: moderate — corrects the *cost* of the pioneer wrapper but does not change the *positive-EV* argument for authoring it.

5. **"Twelve months of stabilization" counted from the wrong date** — raised by backbone-researcher §2.4 and litellm-hybrid §1. I measured from A2A's April 2025 protocol announcement, not from the `v1.0.0` wire-spec release three weeks before Phase 1. Conceded. Severity: moderate, argues against "bet on A2A now" which I already conceded.

6. **"The wrapper is not conversus's problem"** — raised by all three Phase 2 attacks. I argued the SDK vendors would ship A2A servers themselves. No vendor has announced this. Conceded that in 2026-04, if the wrapper exists, conversus writes it. Severity: moderate; reframed in Phase 3 as "conversus should write it as a post-v1 pioneer contribution."

7. **"Python SDK maturity supports production use"** — `a2a-sdk` is 0.3.25 stable / 1.0.0a0 alpha. I elided this in Round 1. Conceded in Phase 2. Severity: moderate; my Phase 3 revision explicitly isolates any `a2a-sdk` dependency inside the optional standalone `conversus-a2a-claude` package, not in spec 042 core.

8. **"Single-vendor LiteLLM dependency is risky"** — my Round 1 supply-chain attack on LiteLLM. Raised by backbone §10, litellm-hybrid §3, and I conceded in my own Phase 2 cross-review. Severity: moderate; LiteLLM's operational posture is now universally endorsed in the deliberation.

### Aggregate assessment

These eight concessions sink "ship A2A first" and "wrap Claude Code as an A2A server in v1." They do not touch my three Phase 3 held claims. Every conceded weakness belongs to a Round 1 position I no longer defend. The three claims I am defending were either not attacked (spec 048 discovery gap) or attacked and defended successfully (protocol shape, pioneer wrapper as post-v1 standalone).

---

## Surviving Advantages

### 1. Protocol shape is a one-way door — neither winner's plan binds it (established Phase 1, sharpened Phase 3)

Every Phase 3 revision agrees the `ExecutionProvider` protocol is conversus-owned. None of them take a position on field shape. Specifically:

- **Build-our-own §Protocol** defines `ExecutionTask(prompt: str, output_path: str, read_paths: list[str], metadata: dict)` — a flat string prompt, no structured parts, no references, no streaming envelope, no A2A Task Request compatibility.
- **Litellm-hybrid Phase 3 §Rebuttals** explicitly accepted my protocol-shape amendment as "~4 hours of extra docstring and design notes. Zero impact on v1 scope" — but framed it as an architectural footnote, not a binding deliverable. Their own v1 plan ships the same flat-prompt shape.
- **Backbone-researcher** is non-advocacy and takes no architectural position.

The gap is real. Neither winner's plan has specified what `ExecutionTask` looks like beyond the four fields spec 042 §3 enumerates. The default, absent a Week 1 design note, will be whatever the first adapter needs — which is `LiteLLMProvider`'s `completion_async(messages, model, tools)` or `ClaudeCodeProvider`'s `claude -p <prompt>`. Both are flatter than A2A Task Request semantics.

The argument (Phase 3 §Reinforced Strengths §1): this is a one-way door. Every provider adapter, every test, every downstream spec (048, 046, 020) consumes the shape. Changing it after Week 1 is a migration, not an addition. Adapting `LiteLLMProvider` to flatten structured `parts` down to `messages=[{"role": "user", "content": text}]` is three lines. Adapting a flat-prompt protocol upward into A2A's structured shape later is a breaking change across every provider.

**Cost to adopt**: ~4 hours of design notes in the Week 1 PR, plus a `from_prompt(prompt, output_path, read_paths)` compatibility constructor so existing subprocess and LiteLLM providers keep working unchanged. This is smaller than a lunch break.

### 2. `conversus-a2a-claude` as post-v1 standalone pioneer artifact (Phase 3 §Reinforced Strengths §2, endorsed by backbone-researcher §5.2)

The backbone-researcher's own §5.2 endorsed this as a valid reframe: *"Given that no one has yet wrapped a major coding agent as an A2A server, conversus being the first to do so is a genuine ecosystem contribution that benefits every future A2A client, not just conversus. The flywheel metaphor works if conversus is willing to push the wheel."*

Phase 2 attacks on this claim targeted my Round 1 framing (v1 deliverable blocking spec 042). Phase 3 reframed it as a separate-package, post-v1, standalone artifact on an independent timeline. Neither winner's Phase 3 revision engages with the reframed version — they attack the Round 1 version I already dropped.

Positive-EV on both futures:
- **If A2A arrives 2027–2028**: conversus is the reference implementation for wrapping coding agents. Disproportionate ecosystem influence.
- **If A2A does not arrive**: conversus gains a long-lived-process Claude Code dispatch path that amortizes the 1–3 second cold-start cost flagged in backbone §11.10 as a scaling problem for spec 048's 10–30 parallel phases.
- **Risk**: ~300–600 lines of optional code in an optional standalone package. Deletable. Not a dependency of spec 042 core.

Build-our-own's revision §Rebuttals actually accepted this: *"the A2A server wrapper is built on top of `ClaudeCodeProvider`, not as a replacement for it… The A2A advocate's single most strategically valuable idea (wrap Claude Code as an A2A server for ecosystem leverage) is literally built on top of my v1 `ClaudeCodeProvider`."* That is the concession I am carrying forward — build-our-own agrees the v1 plan *enables* the pioneer artifact. I am asking the arbiter to record this as an explicit commitment in the winner's plan, not a verbal concession in a revision document.

### 3. Spec 048 discovery gap — `.conversusrc::default_agents` must accept URL entries from day 1 (Phase 3 §Reinforced Strengths §3, unchallenged)

This is my most defensible claim and the one no advocate engaged with. Spec 048 §10 Q4 (multi-repo governance), §10 Q8 (monorepo scoping), and §11 (seven execution surfaces) all require a discovery model beyond hardcoded Python provider strings.

- **Build-our-own** conceded the `register_provider_instance()` runtime hook in their Phase 3 §Registry code but did not propagate it to spec 048's `.conversusrc` schema.
- **Litellm-hybrid** Phase 3 explicitly deferred this: *"Spec 042 is an execution-provider abstraction, not an agent-discovery service… Out of scope for v1 by spec definition; in scope for Phase 3 via A2A provider addition."*
- **Backbone-researcher** is non-advocacy.

The gap: if `.conversusrc::default_agents` ships in spec 048 v1 accepting only `{preset: string}` entries, adding URL entries in 2027 requires a schema migration. The validation battery §1.2 explicitly flags this: *"The config schema must not forbid URL entries. An error saying 'URL-addressable agents not yet supported in v1' is acceptable; a schema that rejects the field outright is not, because it would require a migration to add later."*

**Cost to adopt**: ~20 lines of YAML schema definition and a "URL-addressable agents not yet supported" error in spec 042 v1 / spec 048 v1. Zero runtime impact. The schema accepts both forms:

```yaml
default_agents:
  - preset: security-reviewer           # v1: hardcoded Python provider
  - url: https://agents.internal/cve    # v2: A2A endpoint, errors in v1
```

When `ACPProvider` lands in Phase 3, every existing `.conversusrc` with URL entries starts working without a schema migration. This is a free forward-compatibility win, and the validation battery explicitly asks for it.

---

## Why Pick Me — Partial Ruling Ask

I am not asking the arbiter to pick me to win winner-take-all. That argument is dead. Three rounds of adversarial testing have shown that my v1 critical path is indefensible — the A2A ecosystem is empty, my Round 1 "ship A2A first" was a mistake, and neither of my Phase 3 amendments (protocol shape, pioneer wrapper, discovery gap) constitutes a standalone v1 architecture. Build-our-own and litellm-hybrid are both better v1 architectures than anything I can offer.

**What I am asking**: that the arbiter incorporate my three Phase 3 held claims into the winner's implementation plan as **binding elements**, under the Phase 6 rule that allows incorporating specific elements from losing positions into the winner. This is not rhetorical dressing — it is a concrete ask with three concrete deliverables:

1. **If the arbiter picks build-our-own**, bind them to: (a) a Week 1 protocol-shape design note specifying `ExecutionTask.parts` / `references` / `metadata` / streaming-ready fields with a `from_prompt()` compatibility constructor (cost: ~4 hours); (b) explicit commitment to `conversus-a2a-claude` as a post-v1 standalone package on an independent timeline (cost: ~300–600 LoC when built, deferrable); (c) `.conversusrc::default_agents` schema accepting URL entries with a "not yet supported" error in v1 (cost: ~20 lines). Build-our-own has already conceded all three verbally in their Phase 3 revision §Rebuttals. Making them binding costs nothing and forecloses three future migrations.

2. **If the arbiter picks litellm-hybrid**, bind them to the same three commitments. Litellm-hybrid's Phase 3 §Rebuttals explicitly accepted the protocol-shape amendment as "~4 hours of design notes. Zero impact on v1 scope." They did not bind it. Binding it prevents the `LiteLLMProvider`-shaped default from ossifying into the protocol. The pioneer-wrapper commitment is harder for litellm-hybrid to absorb because their v1 set is smaller, but it can ship as a spec 042 footnote: "if/when authored, `conversus-a2a-claude` is built on top of the v1 `ClaudeCodeProvider` subprocess machinery." The discovery-gap commitment is the hardest for litellm-hybrid to absorb — they explicitly deferred it in Phase 3 — and I am asking the arbiter to override that deferral. The cost is ~20 lines; the value is preventing a 2027 schema migration the validation battery §1.2 explicitly flags as unacceptable.

3. **If the arbiter picks a synthesis of build-our-own + litellm-hybrid** (which is what the Phase 2 convergence actually supports), bind the synthesis plan to all three commitments. The three claims do not conflict with any element of either winner's architecture. They add constraints on *how* the winner's plan ships, not on *what* it ships.

**The risk calculus for the arbiter**: picking a winner and ignoring my three claims exposes the deliberation to three foreseeable failure modes. First, a 2027 `ExecutionTask` migration that breaks every downstream spec when A2A counterparties emerge and the flat-prompt shape cannot accommodate structured parts. Second, a missed ecosystem-leadership opportunity when someone else writes the first Claude Code A2A wrapper and gets the reference-implementation status that conversus's v1 work already enables. Third, a `.conversusrc` schema migration in spec 048 v2 that breaks every existing governance config because v1 forbade URL entries outright. Each failure is preventable today at a combined cost of ~4 hours plus ~20 lines of schema plus one paragraph of post-v1 commitment. The cost of not preventing them is measured in weeks of migration work and foregone ecosystem position.

**The single most important takeaway**: if the arbiter binds only one of my three claims, bind the protocol shape. **`ExecutionTask` and `ExecutionResult` are a one-way door.** Every other decision in this deliberation is additive or deletable — new providers can be added, old providers can be retired, A2A can arrive or not, LiteLLM can be swapped out. But the `ExecutionTask` field shape is consumed by every provider, every test, and every downstream spec from the moment v1 ships. Changing it later is not a refactor; it is a breaking migration across the entire execution-provider surface. The winner's Week 1 PR should include a 4-hour design note specifying A2A Task Request semantics (`parts`, `references`, `metadata`, streaming-ready fields) with a `from_prompt()` compatibility constructor. This is the cheapest architectural insurance in the entire deliberation, and neither winner's current plan specifies it. I am asking the arbiter to make them.
