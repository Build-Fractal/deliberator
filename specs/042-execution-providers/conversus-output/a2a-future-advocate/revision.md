# a2a-future-advocate — Phase 3 Revision

**Advocate**: a2a-future-advocate
**Round**: 1, Phase 3 (Defense / Revision)
**Iteration**: 1
**Date**: 2026-04-05

---

## Position Summary

My Round 1 thesis — "build the `acp` provider first, bet everything on A2A now" — is dead. The backbone-researcher's §9/§10 findings were decisive: in 2026-04, **zero** shipping coding agents expose A2A servers, the `a2a-sdk` is 0.3.25 stable / 1.0.0a0 alpha, and protocol v1.0.0 is three weeks old. Every advocate now agrees subprocess providers are the v1 baseline. I yielded that axis in Phase 2 and I do not reopen it here.

What survives — and what this revision sharpens — is a **much narrower and more defensible claim** in three parts:

1. **Protocol shape is load-bearing and time-sensitive.** `ExecutionTask` and `ExecutionResult` must be designed around A2A Task Request semantics in Week 1. If they ossify around LiteLLM's `completion_async` shape, the Phase 3 A2A migration becomes a rewrite, not an additive provider. This is the one architectural decision where "do it now" is strictly cheaper than "do it later."

2. **Conversus should author `conversus-a2a-claude` as the first A2A server wrapper for a shipping coding agent.** The empty-ecosystem finding cuts two ways. The backbone-researcher framed it as damaging (no counterparties → the flywheel has no wheel). I now frame it as opportunity (no counterparties → first mover gets disproportionate ecosystem influence). Conversus is building a `ClaudeCodeProvider` anyway. The delta from "internal Python adapter" to "standalone A2A server artifact wrapping the same `claude -p --bare` invocation" is ~300–600 lines. If conversus ships this as a separately-versioned package, it is the first A2A wrapper of any shipping coding agent in the world.

3. **Spec 048's agent discovery story remains unanswered by every other advocate.** Spec 048 §10 Q4 (multi-repo governance) and the §11 execution surfaces table point to a future where `.conversusrc::default_agents` cannot stay a hardcoded list of Python provider strings — it has to become URLs/endpoints. A2A Agent Detail is the only protocol in the landscape that solves this. The hybrid and build-our-own positions are silent on it. Silence is not an answer.

**Revised thesis**: Ship subprocess providers as the v1 baseline (conceded). Shape the protocol A2A-friendly from Week 1. Author `conversus-a2a-claude` as a standalone pioneer artifact. Design spec 048's registry with URL-based dispatch in mind so the eventual A2A migration is a config change, not a breaking change.

This is not "A2A first." It is "A2A-shaped protocol, A2A-compatible provider code, pioneer wrapper as a by-product, forward-compatible discovery." Everything I hold is cheap to do on the hybrid/build-our-own timeline.

---

## Rebuttals

The attacks against me in Phase 2 fall into two categories: attacks on claims I have already **conceded** (Round 1 ecosystem overreach, ACP/A2A conflation, "zero lines per tool" math, 30-line wrapper claim) and attacks on claims I am **still holding** (protocol shape, pioneer wrapper value, discovery gap). I address both — conceding the first category cleanly, rebutting or partially rebutting the second.

### Conceded: Zed/JetBrains ACP vs Google/IBM A2A conflation

- **Their claim** (backbone-researcher §1, build-our-own §1, litellm-hybrid §2): My Round 1 review treated "ACP" as a single protocol and cited Zed/JetBrains Agent Client Protocol ecosystem facts (OpenCode in the Zed registry, JetBrains IDE integration) as evidence for A2A adoption. These are two different protocols — A2A is JSON-RPC over HTTP for headless agent-to-agent dispatch (LF AI & Data, `a2a-sdk`); Agent Client Protocol is JSON-RPC over stdio for IDE-to-agent integration (Zed Industries, `@agentclientprotocol/*`). Different wire formats, different scopes, different threat models.
- **Concession**: Correct. I conflated them in at least two places (§2.3 flywheel list including "Zed," §4 "IDE plugins are A2A clients in disguise"). The conflation is inherited from spec 042 §2 which itself ambiguously says "ACP," but that does not excuse me propagating it.
- **Impact**: The terminology fix is now **universally agreed** by all three advocates. Spec 042 §11's `acp` row must split into (a) `a2a` for headless HTTP dispatch and (b) `zed-acp` (out of scope for v1) for IDE integration. This is a clean win that I take gratefully — every advocate's revision will carry this correction forward, which means the synthesizer has a joint-ratified spec edit to apply. The advocate who first insisted on the distinction (implicitly the backbone-researcher, explicitly adopted by all of us) deserves the credit. I am happy to share it.
- **Status**: Conceded with context — the concession is a joint ratification, not a unilateral retreat.

### Conceded: "One provider, every tool — zero lines of conversus code" was present-tense when it should have been future-tense

- **Their claim** (all three Phase 2 attacks): In 2026-04, zero shipping coding agents expose A2A servers. My "every SDK that ships an A2A endpoint becomes conversus-compatible the day it ships" is empty because the conditional clause is empty. The actual 2026-04 math is: one A2A client + N A2A wrappers conversus must author = strictly more code than N direct subprocess adapters.
- **Concession**: Correct. The flywheel description was a steady-state equation treated as a day-one state. I also undersold the cost of the wrapper work — my Round 1 cited "thirty lines" from a sketch; the backbone-researcher's §4.2 is correct that a production A2A server wrapping Claude Code is several hundred lines (stream translation, subprocess lifecycle, cancellation, auth, error mapping, multi-turn sessions).
- **Impact**: This concession does not touch the three arguments I am still holding. Protocol shape does not require a populated ecosystem — it is a Week 1 design choice inside conversus's own codebase. The pioneer wrapper argument explicitly *embraces* the empty-ecosystem finding as the reason the first mover matters. The discovery-gap argument is about 2027+ design headroom, not 2026-04 implementation.
- **Status**: Conceded with context — the concession sits inside the claims I am dropping, not inside the claims I am defending.

### Conceded: "Twelve months of stabilization" was counting from the wrong point

- **Their claim** (backbone-researcher §2.4, litellm-hybrid §1): I claimed "twelve months of stabilization" measuring from A2A's April 2025 launch. The v1.0.0 protocol artifact released 2026-03-12 is three weeks old. The Python SDK stable release `a2a-sdk` 0.3.25 is also ~three weeks old. Counting from protocol-announcement, not from shippable-v1.0.0, inflates maturity.
- **Concession**: Correct. The number that matters for a production bet is the stable-artifact age, not the protocol-announcement age.
- **Impact**: This is an argument against "bet everything on A2A now," which I have already conceded. It is not an argument against the three claims I am holding. A Week 1 protocol-shape decision does not require `a2a-sdk` to be 1.0 — it requires the A2A Task Request semantics to be stable (which they are — the wire format is what v1.0.0 stabilized). Authoring `conversus-a2a-claude` does not require `a2a-sdk` maturity because the wrapper can be built against the wire spec directly, or against `a2a-sdk` as a pinned dependency with a known upgrade path.
- **Status**: Conceded with context.

### Rebutted: "The 6-month deletion timeline you attacked in the hybrid is exactly what your plan does"

- **Their claim** (build-our-own §4): "The A2A advocate plan = 1 direct Claude Code provider + 1 A2A server wrapper for Claude Code + 1 A2A client provider = 3 artifacts, all maintained in parallel, all needing to stay API-compatible. The advocate's 'commit now, don't hedge' rhetoric is unreconciled with their own implementation plan."
- **My response**: This attack lands against my **Round 1** plan, where I asked conversus to build both a direct provider and a reference A2A wrapper simultaneously as v1 deliverables. That plan is gone. The revised plan has exactly **two** artifacts at v1 ship:
  1. `claude-code` direct subprocess provider (v1 of spec 042, ships with the hybrid baseline).
  2. `conversus-a2a-claude` standalone package (post-v1 pioneer artifact, ships when the team has bandwidth — not a spec 042 blocker).
  The third artifact (`a2a` client provider inside conversus) is deferred to Phase 3 exactly as the hybrid advocate proposes. That is not more artifacts than the hybrid plan — it is the same count (direct providers + eventual A2A provider), with one additional standalone ecosystem contribution that the hybrid plan does not produce.
- **Status**: Rebutted — the "3 artifacts in parallel" critique applied to my Round 1, not to this revision. The revised plan has the same artifact count as the hybrid plan with one standalone ecosystem deliverable added.

### Partially Rebutted: "The wrapper is NOT conversus's problem" was empty (backbone-researcher §2.2, build-our-own §2, litellm-hybrid §1)

- **Their claim**: My Round 1 said "the wrapper is NOT conversus's problem — it is the SDK's problem, or it is a reusable artifact because wrapping Claude Code as an A2A server is valuable to every A2A client in the world." Reality: no SDK has treated wrapping itself as their problem, no community effort exists, "valuable to every A2A client" is speculative when zero A2A clients consume coding-agent wrappers today.
- **What is true**: "It is the SDK's problem" was wishful thinking in 2026-04. No vendor roadmap announces A2A-server support for a shipping coding agent. If the wrapper exists, conversus writes it.
- **What is false or misleading**: "Valuable to every A2A client in the world" is not speculative *if we frame it as future value accruing over 12–24 months*. The backbone-researcher's own §5.2 explicitly lists this as a **surviving** claim: *"Given that no one has yet wrapped a major coding agent as an A2A server, conversus being the first to do so is a genuine ecosystem contribution that benefits every future A2A client, not just conversus. The flywheel metaphor works if conversus is willing to push the wheel."* The researcher endorsed the reframe — pioneer, not late adopter. The attack was on my Round 1 **framing** (present tense, community free-rider), not on the **underlying claim** (writing the wrapper is valuable).
- **Net assessment**: The correct sentence is: "The wrapper IS conversus's problem in 2026, and conversus doing it first is the single highest-leverage ecosystem contribution conversus can make to the A2A story." The researcher wrote this nearly verbatim in their §5.2. The build-our-own and litellm-hybrid cross-reviews attack the Round 1 wording without engaging with this reframe — and the reframe is what my revision holds.
- **Status**: Partially rebutted — Round 1 framing was wrong, reframed claim is endorsed by the researcher and unanswered by the other advocates.

### Rebutted: "Your architecture forces a choice where no choice is needed" (litellm-hybrid §2)

- **Their claim**: "My hybrid approach treats this cleanly: the `ExecutionProvider` protocol absorbs any wire format. LiteLLM for Tier 3. Direct SDK adapters for Tier 1 agents today. A2A provider when the A2A server ecosystem actually exists. Zed/JetBrains ACP provider if and when… Each adapter is additive, not exclusive. The advocate's architecture forces a choice where no choice is needed."
- **My response**: My revised position is **not** a choice between hybrid and A2A. It is a design constraint **on** the hybrid: that the `ExecutionProvider` protocol's `ExecutionTask`/`ExecutionResult` be shaped around A2A Task Request semantics from Week 1. The litellm-hybrid advocate's review is **silent on protocol shape** — they treat `ExecutionProvider` as conversus IP and move on, without naming what shape that IP should take. I agree with their §2 ("LiteLLM absorbs any wire format") **at the implementation level**. At the abstraction level, a Protocol with `execute(prompt: str, output_path: str, read_paths: list[str], metadata: dict) → ExecutionResult` is a shape choice. The question is whether that shape mirrors A2A's structured parts/references/metadata/streaming or collapses toward LiteLLM's flat `messages: list, model: str, tools: list`. The hybrid review does not take a position. In the absence of a position, the default will be the Week 1 implementation's shape, which is LiteLLM-first. That is how abstractions ossify.
- **Status**: Rebutted — "adapters absorb wire formats" is true at the implementation layer but silent on the abstraction layer. Shape choice in Week 1 is not a choice between architectures; it is a refinement the hybrid architecture needs to specify.

### Rebutted: "Build-our-own already contains everything the A2A advocate wants" (build-our-own §6, §8)

- **Their claim**: "Build the protocol. Ship the direct providers. Add `a2a` to the matrix. Let A2A win as a provider when its ecosystem is real… Their position becomes my §11 matrix row when A2A grows up. They are not proposing a different architecture; they are proposing a different ordering. The researcher's facts make that ordering wrong."
- **My response**: The "superset framing" works if and only if the protocol shape is designed A2A-friendly. Build-our-own's review is silent on `ExecutionTask` field structure. If the build-our-own protocol ships with `ExecutionTask(prompt: str, ...)` — a flat string prompt with no structured parts, no reference list, no agent capability metadata — then adding an `ACPProvider` later means one of two things: (a) the `ACPProvider` flattens A2A's richer envelope into conversus's poorer envelope, discarding composability and metadata; or (b) `ExecutionTask` grows new fields in a breaking change and every other provider adapts. Both outcomes are worse than designing the richer shape in Week 1. My revised position asks build-our-own to **own** this shape choice explicitly — not as a concession, but as a small Week 1 design note that costs ~4 hours and prevents a Phase 3 rewrite. The build-our-own review does not engage with this.
- **Status**: Rebutted — "superset" is architectural cover for a question build-our-own has not answered. The shape needs to be specified, and A2A Task Request semantics is the right specification.

### Partially Rebutted: "Discovery becomes a provider-internal detail instead of a conversus-level feature" (my own cross-review of build-our-own §4.1, echoed by build-our-own §6 reply)

- **Their claim** (build-our-own's implicit reply): Runtime discovery can live inside the `ACPProvider` adapter when that provider ships. Spec 048's `default_agents:` config can stay as a list of provider strings in 2026; URL-based discovery is a forward capability.
- **What is true**: Discovery **can** live inside a future provider adapter. Spec 048 can ship with hardcoded presets in v1.
- **What is false or misleading**: "Provider-internal discovery" is not equivalent to "conversus-level discovery." If the `.conversusrc::default_agents` schema is shaped around Python provider strings, teams cannot add custom governance agents without a conversus release. If it is shaped around URLs/endpoints (with provider strings as a legacy path), teams stand up an A2A server and register it — no release required. This is exactly the scaling story in spec 048 §10 Q4 (multi-repo governance) and the §11 execution-surfaces table. Neither the build-our-own nor litellm-hybrid reviews engage with Q4 or the surfaces table. They are unanswered.
- **Net assessment**: Build-our-own's response to this concern is "leave room in `PROVIDER_REGISTRY` for runtime registration." That is the minimum viable accommodation. I want stronger: the `.conversusrc::agent_registry` field should accept URL entries in addition to provider-string entries from day 1, with URL entries dispatched via a future `a2a` provider. Spec 042 v1 ships without A2A clients; spec 048 v1 ships with `.conversusrc` accepting both forms and erroring on URL entries ("A2A provider not yet available"). This costs near-zero in v1 and prevents a `.conversusrc` schema migration in 2027.
- **Status**: Partially rebutted — build-our-own concedes the registry extension point but does not propagate it into spec 048. I am asking for the propagation.

### Rebutted: "Python SDK is pre-1.0, betting architecture on it is risky" (backbone-researcher §2.4, litellm-hybrid §7 factual corrections)

- **Their claim**: `a2a-sdk` is 0.3.25 stable / 1.0.0a0 alpha. Single vendor (Google LLC). Depends on FastAPI/Starlette, opentelemetry, JSON-RPC framework. Claiming "no new dependencies, just httpx" is incorrect.
- **My response**: My revised position **does not require** conversus to depend on `a2a-sdk` for spec 042 v1. The protocol-shape amendment is an internal-codebase decision with zero external dependencies — `ExecutionTask` field names and types are conversus code. The `conversus-a2a-claude` standalone artifact is a separate package, separately versioned, with its own dependency graph — if it pins `a2a-sdk` 0.3.25 as an early-access dependency, that risk is contained inside an optional standalone package and does not touch spec 042's core dependency surface. My Round 1 claim "no new dependencies, just httpx" was misleading; my revised claim is "protocol shape requires zero external dependencies, and the pioneer wrapper pins its own dependencies in its own package boundary."
- **Status**: Rebutted — the dependency concern applies to my Round 1 "ship A2A in core v1" plan and does not apply to the revised "A2A-shaped protocol + standalone wrapper package" plan.

### Rebutted: "Reference LiteLLM as the Tier 3 implementation is already the right answer" (litellm-hybrid §5)

- **Their claim**: LiteLLM covers Tier 3 today with 14 lines and stable cost tracking / retry / rate limiting. My Round 1 attack on LiteLLM ("rename of ModelProvider") was wrong.
- **My response**: Conceded in my own cross-review (litellm-hybrid §5.1). I am not re-litigating. **What I am adding**: the correct architecture is `LiteLLMProvider` as an implementation of the A2A-shaped `ExecutionProvider`, where `LiteLLMProvider` adapts down from the A2A-shaped `ExecutionTask` to `litellm.completion_async`'s flat messages shape. This is strictly better than the inverse (shape `ExecutionTask` around LiteLLM and force the future `ACPProvider` to adapt up). Round 1 me was wrong to attack LiteLLM; Round 1 me was right to want protocol shape to come from A2A. These are separable, and the revised position holds both.
- **Status**: Rebutted as a blanket attack on my position — LiteLLM concession is orthogonal to the protocol shape claim, which is what I am holding.

---

## Reinforced Strengths

Three strengths from my opening argument survive Phase 2 either **unchallenged** or **challenged and confirmed** by competitor reviews. Each is sharpened below.

### 1. Protocol shape in Week 1 is load-bearing and unanswered by competitors

**Unchallenged.** Neither the build-our-own nor the litellm-hybrid review takes a position on the shape of `ExecutionTask` and `ExecutionResult`. Build-our-own §2 defines the 4-method interface in ~40 lines and calls it "conversus's IP." The litellm-hybrid review says the protocol "absorbs any wire format" and moves on. Neither review answers: does `ExecutionTask` have structured parts (text, references, binary) or a flat `prompt: str`? Does `ExecutionResult` have streaming updates or only a final payload? Does `metadata` include A2A-style agent capabilities, or only conversus-phase fields?

These field-shape questions determine whether the Phase 3 A2A provider is a ~30–50 line adapter or a rewrite with breaking changes across every other provider. Phase 3 slip risk is exactly proportional to how tightly the Week 1 shape constrains A2A's richer envelope.

**The exact Week 1 amendment** (cost: ~4 hours of design):

```python
@dataclass(frozen=True)
class ExecutionTask:
    # A2A-Task-Request-shaped fields, not LiteLLM-completion-shaped fields:
    parts: list[Part]              # text, reference, binary — superset of "prompt: str"
    metadata: dict[str, Any]       # phase, agent, capabilities, auth hints
    references: list[Reference]    # read_paths become structured references
    stream: bool = False           # streaming semantics from day 1
    output_path: str | None = None # conversus-specific, orthogonal to A2A

    @classmethod
    def from_prompt(cls, prompt: str, output_path: str, read_paths: list[str] | None = None):
        """Compatibility constructor — flat prompt + read_paths still works."""
        ...
```

The `from_prompt` compatibility constructor means subprocess/LiteLLM providers can keep accepting flat prompts in Week 1. The structured shape is there for future providers. Adapting `LiteLLMProvider` to flatten `parts` down to `messages=[{"role": "user", "content": text_of(parts)}]` is three lines. Adapting a flat-`prompt` protocol upward into A2A's structured shape is a breaking change.

This is a **one-way door** decision. Do it right on day one, or pay a migration tax later. The hybrid advocate has not taken a position; I am asking them to take one.

### 2. Authoring `conversus-a2a-claude` as a standalone pioneer artifact is a positive-expected-value ecosystem contribution

**Challenged by build-our-own and litellm-hybrid as premature; confirmed by backbone-researcher §5.2 as valid reframe.** The researcher's §5.2 explicitly elevated this claim:

> "Given that no one has yet wrapped a major coding agent as an A2A server, conversus being the first to do so is a genuine ecosystem contribution that benefits every future A2A client, not just conversus. The flywheel metaphor works if conversus is willing to push the wheel. … That is a respectable bet."

The build-our-own and litellm-hybrid cross-reviews attack this claim by treating it as a Round 1 "v1 deliverable" that blocks spec 042. It is not — **in the revised position, it is a post-v1 standalone package on a separate timeline**. Spec 042 ships the subprocess `claude-code` provider on the hybrid schedule. `conversus-a2a-claude` ships as a separately-versioned package when the team has bandwidth (estimated post-042, parallel to spec 048 development).

The economics the Phase 2 attacks missed:

- **Cost**: 300–600 lines (the researcher's honest number, not my Round 1 "30 lines"), built on top of the existing `ClaudeCodeProvider`'s `claude -p --bare` invocation. The internal dispatch function is already written; the A2A server is an HTTP shell around it.
- **Benefit if A2A ecosystem arrives by 2027**: Conversus is the reference implementation for wrapping coding agents. Every A2A client in the world (Google ADK, IBM BeeAI, LangGraph, future vendors) benefits. Conversus gets ecosystem influence disproportionate to its size.
- **Benefit if A2A ecosystem does not arrive**: Conversus has a long-lived-process Claude Code dispatch path that avoids the 1–3 second cold-start per phase that the researcher flags in §11.10 as a scaling problem for 10–30 parallel phases. This is valuable **independent of the A2A ecosystem question**.
- **Risk if wrong**: ~300–600 lines of optional standalone code. Not a dependency of spec 042 core. Deletable.

This is a positive-EV bet on both branches of the future. Round 1 me argued it had to ship in v1; revised me argues it ships as a separate artifact on a separate timeline. Neither the build-our-own nor litellm-hybrid review engages with the post-v1 framing — they attack the v1 framing that I already dropped.

### 3. Spec 048's discovery gap is unanswered by every other advocate

**Unchallenged.** Spec 048 §10 Q4 asks:

> "**Q4: Relationship to gate spec**: Does this replace the existing gate spec or extend it?"

and §10 Q8:

> "**Q8: Multi-repo governance**: Can a single `.conversusrc` govern multiple repos (monorepo case)? Or does every repo need its own?"

and §11 "The CLI that runs outside your CLI" lists seven execution surfaces (GitHub Actions, git hooks, cron, webhooks, Claude Code, CLI, IDE plugins) that all need to resolve "which agents to dispatch to."

The build-our-own review is silent on spec 048 beyond naming it as a hard dependency consumer. The litellm-hybrid review mentions spec 048 only to note the timeline pressure. Neither engages with the discovery model that spec 048 needs once it moves beyond a single-repo hardcoded-preset v1.

**The concrete gap**: Spec 048's `.conversusrc::default_agents` is a list of Python provider strings:

```yaml
default_agents:
  - preset: security-reviewer
  - preset: architecture-reviewer
```

For spec 048 v1, this works. For multi-repo governance (Q8), cross-team agent sharing, or any team adding a custom reviewer without a conversus release, it does not. The only protocol in the 2026-04 landscape that addresses this is A2A Agent Detail — agents self-describe via a JSON endpoint, clients discover capabilities at runtime, the registry is an HTTP concern instead of a Python import concern.

**The revised amendment** (cost: near-zero in v1): Spec 048's `.conversusrc` schema should accept both forms from day 1:

```yaml
default_agents:
  - preset: security-reviewer           # v1: hardcoded Python provider
  - url: https://agents.internal/cve    # v2: A2A endpoint (errors with
                                         #     "A2A provider not available"
                                         #     in spec 042 v1, works when
                                         #     ACPProvider lands)
```

Spec 042 v1 ships with a forward-compatible `.conversusrc` schema that knows about URL entries but cannot dispatch them yet. When the `a2a` provider lands in Phase 3, every existing `.conversusrc` with URL entries starts working without a schema migration. The cost today is the YAML schema definition and a "not yet supported" error — maybe 20 lines.

Neither the build-our-own nor litellm-hybrid review engages with spec 048's discovery model. I am not claiming they have to solve it; I am claiming the amendment I am proposing costs near-zero and forecloses a future schema migration. That is a free win.

---

## New Arguments

The Phase 2 cross-reviews exposed one new line of argument I did not make in Round 1 and that I want to elevate in Phase 3.

### New: Protocol shape is the only A2A decision with a one-way door

- **The argument**: Every other A2A decision is reversible or deferrable. The `a2a` client provider is additive — add it when counterparties exist. The standalone `conversus-a2a-claude` wrapper is a separate package — ship it post-v1 or not at all. The `.conversusrc` URL entries are a schema extension — add them in a minor version bump. **But the shape of `ExecutionTask` and `ExecutionResult` in the engine's Python code is a one-way door.** Every provider adapter is written against that shape. Every test is written against that shape. Every downstream spec (048, 046, 020) consumes that shape. Changing it after Week 1 is a migration, not an addition.

  This is the distinction the litellm-hybrid review's "each adapter is additive" framing misses. Implementation layers are additive; **abstraction layers are not**. The `ExecutionProvider` Protocol is the abstraction. Its field shape is the schema all implementations share. You don't get to add structured parts to a flat-string prompt abstraction without touching every implementation.

- **Source**: Triggered by litellm-hybrid's §3 "one abstraction with three implementations" framing. That framing is correct for implementations and wrong for the abstraction's field shape. The gap between those two observations is where the one-way-door argument lives.

- **Evidence**:
  - Spec 042 §3 defines `ExecutionTask` with `prompt: str, output_path: str, read_paths: list[str], metadata: dict`. This is the flat LiteLLM-ish shape. A2A Task Request has structured `parts` (text, reference, data, file) and optional `push_notification_config`, `metadata`, and streaming `task_status` updates.
  - Spec 042 §4 "Tool-use adaptation" shows the engine falling back to pre-reading files and inlining them into `augmented_prompt = task.prompt + "\n\n---\n\n# File Contents\n\n" + ...`. This is a string-concatenation adaptation that works because `prompt` is flat. A structured `parts` shape eliminates this branch entirely — references are first-class — but retrofitting `parts` into a v1-shipped string shape means every provider's `execute()` grows new branches.
  - Spec 048 §6 PR comment format and §3.1 `.conversusrc` schema consume `ExecutionResult`'s fields. If `ExecutionResult.content: str | None` is a flat string in v1, governance rulings and commentary get a string to parse. If it is a structured list of ruling-parts (verdict, citation, evidence, severity), spec 048's JSON output (§5.1) lines up 1:1 with the A2A streaming update events. Adding structure in v2 means spec 048's JSON schema also has a breaking change.
  - Backbone-researcher §11.3 (not quoted in Round 1): "Design the Python protocol to be shape-compatible with A2A Task Request semantics even if the v1 provider matrix is subprocess-only. Otherwise the Phase 3 A2A provider becomes a retrofit." The researcher already said this; I did not foreground it in Round 1 because I was arguing for A2A-first. In the revised position it is the centerpiece.

---

## Updated Risk Profile

Round 1 risk profile was a single axis: "bet on A2A now, hedge against bespoke N×M." The revision replaces it with a four-axis profile that matches the narrower claim.

### Risks confirmed by competitors (strengthens my credibility)

- **Standards-adoption timeline is uncertain.** The litellm-hybrid advocate's §4 historical analysis (Kubernetes 3 years, OpenTelemetry 4 years, gRPC still not displacing REST in 2026) is well-taken. My Round 1 compressed "probably arrives" into "has arrived." Revised position treats A2A adoption as a **2027–2028 event** with 2026-04 being the design-constraint year, not the ship year. This is closer to the litellm-hybrid Phase 3 timeline and to the backbone-researcher's §13 "bet on a future that will probably arrive but has not arrived yet."

- **`a2a-sdk` is pre-1.0 and single-vendor (Google LLC).** Confirmed by backbone-researcher §6.2. The revision addresses this by **not depending on `a2a-sdk` in spec 042 v1 core**. The protocol-shape amendment is internal conversus code with zero external deps. The standalone `conversus-a2a-claude` package can pin `a2a-sdk` with its own upgrade path and absorb the SDK's pre-1.0 churn in an optional artifact, not in the core spec 042 dependency graph.

- **Production A2A wrappers are several hundred lines, not thirty.** Confirmed by backbone-researcher §4.2. I cited "30 lines" from the tool-landscape sketch; the researcher is correct that a production A2A server wrapping Claude Code must handle streaming, subprocess lifecycle, cancellation, auth, error mapping, multi-turn sessions — all told, 300–600 lines. The revised pioneer-wrapper argument budgets for this honestly.

### New risks raised that I must address

- **"Protocol shape amendment" is a design-by-committee trap.** A critique the hybrid advocate could reasonably make but did not: forcing the Week 1 protocol to match A2A semantics is a coupling that locks the engine to an external spec maintained by Google LLC and the LF TSC. If A2A's v2 breaks the v1 wire format, does conversus follow? My response: the amendment I propose is not "match A2A's wire format exactly." It is "shape the Python field layout around A2A's **semantic** structure (parts, references, metadata, streaming) while keeping the Python types conversus-owned." LiteLLM's `completion_async` is a strict subset of this semantic structure. A2A's wire format is a concrete serialization. Conversus adopts the semantics, not the bytes-on-the-wire. A2A v2 affecting the wire format does not affect the Python types.

- **Authoring `conversus-a2a-claude` diverts engineering bandwidth from spec 048.** Real concern. Mitigation: the standalone wrapper is **post-v1, optional, unscheduled**. It does not block spec 042, does not block spec 048, does not even require conversus to ship it — a community contributor could take it on. The claim is only that conversus is the best-positioned team to ship it and should not let it drop from the roadmap. The proposed commitment is "on the roadmap, unscheduled"; the risk of diverted bandwidth is zero if the team never has bandwidth.

- **Spec 048 URL-entry schema addition could create confusion in v1.** If `.conversusrc` accepts URL entries but spec 042 v1 cannot dispatch them, users could be confused by "A2A provider not available" errors. Mitigation: the error message must be explicit ("URL-based agent entries require the `a2a` provider, which is scheduled for Phase 3 of spec 042. Use `preset: <name>` for v1.") and the spec 048 documentation must mark URL entries as forward-compatible / future-only. This is a ~20 line documentation and error-message deliverable.

### Risks mitigated by Phase 2 cross-reviews

- **"Conversus is the pioneer, which means more work" is mitigated by separating artifacts.** Round 1 me bundled the pioneer work into v1. Revised me separates it into a standalone package with its own timeline. The pioneer cost is now optional and bounded, not load-bearing on v1 ship.

- **"Abstraction ossification around LiteLLM's shape" is mitigated by an explicit Week 1 design note.** The litellm-hybrid advocate's own cross-review acknowledges this risk in their §5.2 (door-open vs door-cheap-to-walk-through, though they frame it as residual disagreement). The mitigation is a ~4-hour design activity in Week 1 — add the `from_prompt` compatibility constructor and structured `parts` field. This is not a blocker; it is a refinement I expect the synthesis phase to absorb.

- **"Empty ecosystem" is mitigated by reframing as first-mover opportunity.** The backbone-researcher's §5.2 explicitly endorses this reframe. The Phase 2 attacks against "zero lines per tool" Round 1 framing do not touch the Phase 3 reframe. The empty ecosystem is now an argument **for** the pioneer wrapper, not an argument against the whole position.

### What I am no longer claiming as a risk

- "A2A is certain to win." Downgraded to "A2A is the most credible long-term bet, 2027–2028 arrival probable but not certain."
- "Bespoke adapters are technical debt." Downgraded to "bespoke subprocess adapters are production infrastructure for 2026; their replaceability depends on Week 1 protocol shape."
- "We should skip the hybrid." Dropped entirely. The hybrid is the correct 2026 implementation; the revision is a set of amendments to the hybrid's design.

---

## Bottom Line

I yielded 70% of my Round 1 position in Phase 2. The remaining 30% — protocol shape in Week 1, standalone pioneer wrapper as post-v1 artifact, spec 048 forward-compatible discovery schema — is cheap, unanswered by competitors, and preserves the long-term A2A migration path without touching the hybrid baseline everyone now agrees on.

If the synthesizer takes **only** these three amendments, the final architecture is the hybrid plan that every advocate endorses, with three small refinements that keep A2A as a zero-friction Phase 3 addition instead of a future rewrite. None of the three amendments slow Week 1. All three pay off in 2027–2028 when the A2A ecosystem arrives — or pay off independently (long-lived-process Claude Code dispatch via the standalone wrapper) even if it does not.

The revised claim is not "A2A now." It is: **"Ship the hybrid. Shape the protocol right. Author the pioneer wrapper. Leave room in spec 048's registry for URLs. Let A2A win later without a rewrite."**

That is the honest version of the position, and it is the one I am defending in Phase 3.

---

**Files referenced**:
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/spec.md` (§2, §3, §4, §11, §12)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/research/tool-landscape.md` (§14, §Candidate B, §Candidate C)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/048-autonomous-governance-mode/spec.md` (§3.1, §5.1, §6, §10 Q4/Q8, §11, FR-021)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/review.md` (Round 1 original)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/backbone-researcher/cross-reviews/a2a-future-advocate.md` (§1, §2, §4.2, §5.2, §5.3)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/build-our-own-advocate/cross-reviews/a2a-future-advocate.md` (§1, §2, §4, §5.4, §6, §8)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/litellm-hybrid-advocate/cross-reviews/a2a-future-advocate.md` (§1, §2, §3, §6, §7)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/cross-reviews/backbone-researcher.md` (Phase 2 concessions, §3.3, §5)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/cross-reviews/build-our-own-advocate.md` (Phase 2 concessions, §4.1, §7)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/cross-reviews/litellm-hybrid-advocate.md` (Phase 2 concessions, §2, §5, §6, §7)
