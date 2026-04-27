# Backbone Researcher — Revised Position (Phase 3)

**Role**: Tooling archaeologist. I do not advocate for an architecture. My "position" is the set of factual findings about how production agent tools actually dispatch work today.
**Date**: 2026-04-05
**Iteration**: 1 (post–cross-review)

---

## Position Summary

My Phase 1 report established ground truth about what production agent tools use under the hood. Nothing in the cross-reviews surfaced evidence that contradicted the core findings. All three advocates *used my findings as primary evidence*, two of them explicitly restructured their own positions around them, and the only disputes about my report were cost-estimation details that I will tighten in §3 below.

The refined factual position for Phase 3:

1. **No single library wraps both model APIs and agent runtimes under a unified dispatch interface.** LiteLLM covers model APIs (100+). MCP is for model→tool, not agent→agent. A2A is the right long-term shape but has no shipping coding-agent counterparties in 2026-04. No candidate for the execution-provider layer is off the shelf.
2. **The de facto backbone across shipping coding agents is "subprocess + CLI + JSON output."** Every one of Claude Code, Aider, Copilot CLI, Codex CLI, Gemini CLI, and Continue's `cn` supports this. It is the only pattern that uniformly exists.
3. **OpenCode is the lone exception** with a first-class HTTP server (`opencode serve`, OpenAPI 3.1). No Python SDK, but ~100 lines of `httpx` against the OpenAPI spec is sufficient.
4. **"ACP" is ambiguous**: A2A (Google+IBM, merged Aug 2025, LF AI & Data) and the Zed/JetBrains Agent Client Protocol are different protocols with different wire formats, different threat models, and different use cases. Spec 042 currently conflates them. This is a correctness issue in the spec that the deliberation has now consensus-ratified (all three advocates agreed).
5. **`claude-agent-sdk` is itself a subprocess wrapper around the bundled `claude` CLI binary.** Going Python → Node SDK → CLI is strictly worse than Python → CLI directly.
6. **Subprocess providers pay a 1–3 second cold-start cost per invocation** without `--bare`. For 10–30 parallel conversus phases, this is a measurable latency floor that long-lived-process transports (OpenCode HTTP, future A2A) avoid.

These are not claims I need to defend with new evidence — they are the evidence the other advocates argued *from*. The Phase 3 task is to clean up the cost estimates where I was imprecise, incorporate a correction that build-our-own-advocate surfaced about my subprocess-cost framing, and sharpen the one place where I was genuinely wrong (date arithmetic on A2A merger — August vs September 2025; I had the right fact but the original report should cite August per the LF AI blog).

I hold my stance: factual, non-advocacy. I do not recommend an architecture. I report what shipping tools actually do and flag the claims deliberation agents should not make without evidence.

---

## Rebuttals

### Partially Rebutted: "Researcher's `claude-code` cost estimate (~400–800 LoC) is higher than advocates quoted"

- **Their claim** (implicit across build-our-own §1.5–§2.4 and litellm-hybrid §7): My own cross-review of build-our-own said the production `claude-code` subprocess adapter is ~400–800 lines, not the 100–200 the advocate cited. Build-our-own took this correction and ran with it, proposing a `SubprocessProvider` base class (~300–400 LoC) + thin per-tool subclasses (~100–150 LoC) to absorb the common substrate once. They argued — correctly — that my estimate lumped substrate work into each adapter instead of factoring it out.
- **What is true**: Build-our-own is right that when you factor the substrate out, each concrete provider drops back toward 100–150 LoC. My cross-review's ~400–800 estimate was for a standalone `ClaudeCodeProvider` that reimplemented subprocess lifecycle, error classification, binary discovery, timeout handling, output_path writing, and JSON stream parsing from scratch. Their factoring is better engineering and reduces the per-provider cost.
- **What is unchanged**: The *total* cost at v1 is roughly the same — the substrate has to exist somewhere. Build-our-own's revised estimate (protocol + SubprocessProvider base + HTTPProvider stub + mock + anthropic + ClaudeCodeProvider + OpenCodeProvider ≈ 800–1,200 LoC) is within 10–20% of where a naive "one adapter per tool" accounting ends up, because the work is the same — it just lives in a base class instead of being duplicated. My original number was right in aggregate; build-our-own's refactoring spreads it across a base class + subclasses more cleanly.
- **Net assessment**: The correction is to *architecture*, not to *total cost*. My factual claim stands: a production `claude-code` subprocess dispatch path has non-trivial lifecycle, flag marshalling, error mapping, and JSON-stream parsing work that no advocate should pretend is 30 lines or 100 lines. Whether that code lives in `ClaudeCodeProvider` or in `SubprocessProvider` is a refactoring choice that does not change the empirical effort.
- **Status**: Partially rebutted. Build-our-own surfaced a valid factoring I didn't enumerate. I adopt the SubprocessProvider refactoring as correct. The aggregate cost and the underlying work items are unchanged.

### Rebutted: "Researcher treats subprocess cold-start as disqualifying" (strawman raised by no one but worth addressing)

- **Their claim**: None of the advocates actually raised this as an attack on me; I flag it because my §11 obs. 10 could be read as advocating *against* subprocess providers. Litellm-hybrid cited cold-start as a reason to add process pooling; a2a-future cited it as motivation for an HTTP path. Build-our-own cited it as a reason `opencode` should move into v1.
- **My response**: I never claimed cold-start disqualifies subprocess providers. I reported the ~1–3 second figure as an operational fact the deliberation should price in. Every advocate accepted it. The fact is not adversarial to any position — it is a constraint every proposal has to design around. Subprocess providers are unambiguously the only path that works for Claude Code / Aider / Copilot / Codex / Gemini in 2026-04; cold-start is the cost of that path.
- **Status**: Rebutted (preemptively). The cold-start observation is neutral ground, adopted by all three advocates as input to their proposals. It is not a critique of subprocess providers; it is a budget line item.

### Conceded: "Minor factual error — A2A merger date (August vs September 2025)"

- **Their claim** (a2a-future-advocate §2.4, §6 citations table): My original report said "IBM ACP → merged into Google A2A (Aug 2025, Linux Foundation governance)" in my §0 TL;DR, but in §6.2 I correctly cited "August 2025" per the LF AI blog (`lfaidata.foundation/communityblog/2025/08/29/...`). A2A-future's review at their line 40 quoted the `tool-landscape.md` as saying "IBM ACP merged in September 2025," and my cross-review of a2a-future pointed out the merger was August, not September.
- **Concession**: I had the right fact (August) but I should flag explicitly for the deliberation record that the canonical date is 2025-08-29 per the LF AI blog. The earlier `tool-landscape.md` document uses "September 2025" which is wrong. Other agents should use August.
- **Impact**: Zero on the substantive claims. It is a minor date-arithmetic correction that tightens the record but does not affect any position.
- **Status**: Conceded, with the correction entered for the deliberation record.

### Rebutted: "Researcher conflated two protocols himself / the 'two ACP' finding is overblown"

- **Their claim**: Not raised directly, but I flag this because it is the one area where my report was load-bearing for ratification. All three advocates agreed with my §6 two-protocol finding; none disputed it. The risk is a synthesis reader assuming the finding was controversial.
- **My response**: The finding is ratified by adversarial cross-review — three advocates with different architectural goals independently adopted the A2A-vs-Agent-Client-Protocol distinction, and a2a-future explicitly conceded they had conflated the two in their own original review. The claim is as validated as anything in a deliberation can be.
- **Evidence**: Build-our-own's cross-review §1.6 ("Researcher §6 is a clean correction to spec 042's language… I didn't flag this in my original review; I should have"). Litellm-hybrid's §8 ("Use LiteLLM to own the model-API transport… defer A2A until counterparties exist — all behind conversus's own `ExecutionProvider` protocol"). A2a-future's §1.1 ("The researcher is right. Re-reading my own review against §6 of the researcher's report, I see the error clearly."). Three advocates, three architectural positions, one ratified correction.
- **Status**: Rebutted as a hypothetical; reinforced as ratified fact.

### Conceded: "Researcher did not audit conversus test suite, codebase call sites, or LiteLLM release cadence"

- **Their claim**: My own cross-review of build-our-own explicitly flagged in §7 that I did not verify several of their claims: "Conversus has 3,428 tests," "the engine's phase templates are already provider-agnostic," "LiteLLM releases multiple times per month," etc. These are ratified by advocates but unverified by me.
- **Concession**: I am a tool-landscape archaeologist, not a conversus codebase auditor. My factual scope is "what shipping agent tools expose as dispatch primitives." Claims about conversus's internal state, test counts, and downstream vendor release cadences are outside what I verified.
- **Impact**: Low. Those claims belong to their respective advocates; my report does not rise or fall on them. The synthesis phase should attribute each claim to the source that verified it (the advocate), not treat my Phase 1 report as endorsing conversus-internal numbers I did not measure.
- **Status**: Conceded with context. My scope is external tools. Conversus-internal claims need advocate-level sourcing, not researcher-level sourcing.

### Rebutted: "Researcher's 'no off-the-shelf A2A server wraps any coding agent' finding might be out of date"

- **Their claim**: Not directly raised, but a steelman a future reader might attempt: "The researcher surveyed as of 2026-04-03; by the time synthesis ships, someone may have published an A2A Claude Code wrapper."
- **My response**: As of the date this revision is written (2026-04-05, two days after my Phase 1), the finding still holds. I cite §9 of my Phase 1 report:
  - A2A protocol v1.0.0 released 2026-03-12 (three weeks old at Phase 1).
  - `a2a-sdk` Python: 0.3.25 stable, 1.0.0a0 alpha.
  - No Anthropic/Claude Code reference. No GitHub/Copilot reference. No Aider. No OpenCode. No Codex CLI. No Gemini CLI.
  - Framework integrations exist only in Google ADK, LangGraph, BeeAI — none of which are the coding agents conversus would dispatch to.
  A2a-future's concession in their cross-review §1.2–§1.3 independently confirms this finding via their own inability to cite counterparty servers. The deliberation has ratified the empty-ecosystem finding. Rebutted.
- **Status**: Rebutted. The "empty A2A coding-agent ecosystem as of 2026-04" finding is the single most important factual result in the whole deliberation and is not in dispute by any advocate.

### Partially Rebutted: "The 'de facto subprocess-CLI backbone' finding glosses over tools that DON'T fit"

- **Their claim** (implicit in build-our-own's §5.6 note about `gh-aw` as a third shape, and in my own cross-review of litellm-hybrid where I noted OpenCode is a genuine exception): The "subprocess + CLI + JSON" pattern is NOT universal — OpenCode has HTTP, gh-aw is a compiler not a runtime, and Continue's `cn` has a different task model ("check files" not "arbitrary task dispatch").
- **What is true**: The finding is "de facto across coding-agent CLIs with headless modes," not "universal across all agentic tools." I should tighten the framing. The subprocess-CLI-JSON pattern covers Claude Code, Aider, Copilot CLI, Codex CLI, Gemini CLI, and Continue's `cn` headless mode. It does NOT describe: (a) OpenCode (HTTP-first), (b) gh-aw (Actions YAML compiler, not runtime), (c) Cline/Cursor/Windsurf (IDE-only, no headless surface at all).
- **What is unchanged**: For the set of tools conversus actually intends to dispatch to in its spec 042 §11 matrix, subprocess-CLI-JSON is the baseline that uniformly works. The exceptions are (a) OpenCode, which gets its own HTTP provider — build-our-own has now moved it into v1 in response to my finding, and (b) IDE-only tools, which are out of scope for spec 042's headless dispatch use case.
- **Net assessment**: The finding is "de facto for the in-scope tools." Build-our-own's revised v1 (SubprocessProvider + HTTPProvider) correctly recognizes this by shipping two base classes, not one. A finding of "one pattern covers all in-scope tools" was never accurate; a finding of "one pattern covers the headless CLI in-scope tools, with OpenCode as the HTTP-shaped exception" is accurate and matches what the deliberation converged on.
- **Status**: Partially rebutted; framing tightened.

---

## Convergence with Other Advocates

Per Phase 3 instructions, I flag where the adversarial process produced ratified consensus so I don't redefend it:

- **Spec 042 terminology fix (A2A vs Agent Client Protocol)**: All three advocates + me agree. Spec 042 must rename the `acp` provider to `a2a`, split the Zed/JetBrains Agent Client Protocol into a separate row (or drop it from 042 entirely), and stop using "ACP" as an umbrella term. This is no longer contested — it is the single most unanimous finding in the deliberation.
- **MCP is the wrong layer**: All three advocates + me agree. No one is proposing MCP as the execution-provider abstraction. It stays as tool access inside individual agents.
- **Subprocess CLI is the portable baseline**: All three advocates + me agree (even a2a-future concedes in their §3.3 that "Spec 042 provider v1 ships CLI-subprocess providers for Claude Code, Aider, Copilot CLI, Codex CLI, Gemini CLI, Continue `cn`"). The baseline is not in dispute.
- **OpenCode is architecturally distinct and should get an HTTP provider**: Build-our-own moved OpenCode into v1 in direct response to my finding. Litellm-hybrid acknowledged it as a third transport. A2a-future cited it as a near-term alternative to A2A for long-lived-process dispatch. Consensus.
- **A2A is the right long-term protocol**: All three advocates + me agree. Where they disagree is on *when* to commit — build-our-own says "add it when we need it, the protocol is a superset," litellm-hybrid says "defer until counterparties exist," a2a-future says "be the pioneer now." My role is not to adjudicate; all three positions are consistent with my factual findings.
- **A2A coding-agent ecosystem is empty in 2026-04**: All three advocates agree, including a2a-future, who explicitly conceded it in their §1.2. No shipping coding agent has an A2A server; any conversus A2A provider would have nothing to talk to on day one unless conversus writes the counterparties itself.
- **The `claude-agent-sdk` / Node-bridge framing is misleading**: Build-our-own adopted this correction (their §4.1). Litellm-hybrid adopted it (their §2.1). A2a-future did not contest it. Consensus: a `ClaudeCodeProvider` must go direct to `claude -p --bare` subprocess, not through any SDK layer.

These are the seven points the synthesis phase can treat as joint-ratified and will not need re-litigation.

---

## Reinforced Strengths

Four findings from my Phase 1 report that either went unchallenged or were explicitly ratified by adversarial cross-review:

### 1. The `Agent` tool in SKILL.md is not a protocol and is not portable (Phase 1 §1.4, §11 obs. 1) — UNCHALLENGED

This is the entire motivation for spec 042 existing, and every advocate built on it without dispute. Build-our-own §1.3 explicitly cited it as "the factual basis for spec 042 existing at all." Litellm-hybrid §2.1 restated it as "LiteLLM does not help with the Claude Code agent loop — only with direct Anthropic API calls." A2a-future treated it as a given. The conversus SKILL.md's current dispatch is an in-session Claude tool; it cannot run outside a live Claude session; it must be replaced with `claude -p --bare` (or equivalent) for headless dispatch. Not contested by anyone.

### 2. The two-ACP problem in spec 042 (Phase 1 §6) — BATTLE-TESTED, RATIFIED

A2a-future originally built their whole position on the ambiguity and conceded the error explicitly in Phase 2. Build-our-own said they should have flagged it in their own original review. Litellm-hybrid accepted the correction without dispute. This is the finding that transformed from "researcher's minor nit" to "deliberation-wide mandatory spec fix" in the course of one round of cross-review.

### 3. `claude-agent-sdk` is a CLI subprocess wrapper, not a library API (Phase 1 §1.2, §11 obs. 8) — RATIFIED

Every advocate adopted this correction. Build-our-own dropped the SDK option from v1 (their §4.1). Litellm-hybrid added it to their "what the research refutes" section (their §2.1). A2a-future cited it in explaining why their "A2A wraps around Claude Code" plan was more work than they admitted (their §4.2). Nobody tried to defend the "library integration" framing.

### 4. No shipping coding agent exposes an A2A server in 2026-04 (Phase 1 §9) — BATTLE-TESTED, DEVASTATING TO A2A-FUTURE

This is the factual finding that forced a2a-future to pivot from "bet everything on A2A now" to "ship subprocess providers for 2026 and commit to authoring the first Claude Code A2A wrapper ourselves." The cross-review acknowledged the finding as "the single most damaging factual error" in their original position. The finding was never in question — they could not cite a single counterparty server, and neither could I.

---

## New Arguments

The adversarial process surfaced three factual insights that were not in my Phase 1 report but deserve to be added to the deliberation record. Each is grounded in cross-review evidence, not speculation.

### 1. The deliberation now has consensus on a three-transport taxonomy — and my Phase 1 report almost had it

- **The argument**: The spec 042 §11 provider matrix implicitly assumes one common shape ("ExecutionProvider"). The adversarial process revealed three distinct transports: (a) **Direct network API** (Anthropic, OpenAI, Google, Ollama — what LiteLLM covers), (b) **Subprocess + CLI + JSON** (Claude Code, Aider, Copilot CLI, Codex CLI, Gemini CLI, Continue `cn`), and (c) **HTTP with per-tool schema** (OpenCode today, A2A tomorrow once counterparties exist). Build-our-own's revised v1 has explicit `SubprocessProvider` and `HTTPProvider` base classes; litellm-hybrid's §3.3 table enumerates the same three transports; a2a-future's revised §3.3 accepts the same structure. All three advocates independently arrived at the three-transport taxonomy.
- **Source**: Build-our-own cross-review §3, litellm-hybrid cross-review §3.3 table, a2a-future cross-review §3.3.
- **Evidence**: My Phase 1 §7 and §10 tables enumerated the transports row by row; the advocates collapsed them into a taxonomy I did not explicitly draw. This is a tightening of my own report's structure that I endorse. The Phase 1 finding "subprocess + CLI + JSON is the de facto backbone" is accurate for one of the three transports, not for the whole landscape; the fuller factual picture is "three transports, each with a dominant pattern."

### 2. Build-our-own's `SubprocessProvider` base-class factoring is the correct response to my Phase 1 §7 finding

- **The argument**: My Phase 1 §7 table said subprocess-CLI-JSON is the de facto pattern across six shipping tools. The correct architectural response to "six tools share a pattern" is a shared base class, not six independent adapters. Build-our-own's revised v1 (§3 of their cross-review of me) proposes a `SubprocessProvider` base handling process lifecycle / timeout / error classification / JSON-stream parsing / output_path writing, with each concrete provider as a ~100–150 LoC argv+parse subclass. This is the architecturally correct factoring of my finding.
- **Source**: Build-our-own's cross-review §3 — "Yes. The researcher's finding directly implies this, and it is the single most valuable change to my v1 plan."
- **Evidence**: The common substrate across six tools is enumerated in my Phase 1 §1 (Claude Code), §3 (Aider), §5.2 (Continue), §10 (mapping table), and my cross-review of build-our-own §2.3 (the seven items a production subprocess adapter has to do). If the finding is "these six tools converge on the same dispatch pattern," the finding implies "factor the pattern into a base class." I did not make this architectural implication explicit in Phase 1; build-our-own did, and it is a correct reading of the factual evidence.

### 3. Cold-start amortization is a second-order design constraint that none of the three v1 plans fully addressed

- **The argument**: Subprocess-CLI providers pay 1–3 seconds of cold-start per invocation without `--bare` (Phase 1 §11 obs. 10). For conversus deliberations with 10–30 parallel phases × 3–5 rounds = 30–150 subprocess spawns per run, that is 30–450 seconds of cumulative cold-start overhead. Litellm-hybrid's cross-review §5.3 flags the need for a "process-pooled subprocess provider" that keeps warm CLI workers. Build-our-own's cross-review §4.3 moves `OpenCodeProvider` into v1 partly to validate the long-lived-process transport. A2a-future's cross-review §3.3 proposes authoring `conversus-a2a-claude` as a long-lived HTTP server for exactly this reason. **Three different advocates independently identified a design constraint that none of their v1 plans fully solves.** The synthesis phase should recognize that *any* v1 built purely on subprocess providers will have a latency ceiling that spec 048's autonomous governance scenarios will hit within months.
- **Source**: Litellm-hybrid cross-review §5.3, build-our-own cross-review §4.3, a2a-future cross-review §3.3.
- **Evidence**: My Phase 1 §11 obs. 10 was the original report; the advocates independently treated it as load-bearing. The factual basis: `--bare` exists specifically to cut cold start and does not eliminate it; CLI startup time is dominated by plugin/hook/MCP/CLAUDE.md discovery, which persists even with `--bare` for any provider that wants those features available. Long-lived-process transports (OpenCode HTTP, future A2A server wrapping `claude -p --bare`) amortize the cost across a whole deliberation. The cost matters for spec 048's CI gate use case, where every PR triggers a multi-phase conversus run.

---

## Updated Risk Profile

My Phase 1 report did not include a risk profile per se (I don't advocate for an architecture, so I don't underwrite risks), but I did flag factual gaps and areas where my research was incomplete. The cross-reviews confirmed some of those gaps and introduced new ones. Updated for Phase 3:

### Risks I flagged in Phase 1 that were confirmed by adversarial cross-review

- **A2A Python SDK maturity**: Phase 1 §9 flagged "`a2a-sdk` Python 0.3.25 stable / 1.0.0a0 alpha, protocol v1.0.0 three weeks old." All three advocates independently confirmed this as a blocker for A2A-as-primary-path in 2026-04. The maturity risk is ratified.
- **Missing A2A counterparties**: Phase 1 §9 flagged "no shipping coding agent wraps as an A2A server." A2a-future's concession in cross-review §1.2 explicitly confirmed this as the single most damaging fact against their original position. Ratified.
- **Spec 042 terminology ambiguity**: Phase 1 §6.4 flagged. All three advocates agreed in cross-review that spec 042 must rename `acp` → `a2a` and split Zed/JetBrains ACP into a separate row. Ratified mandatory spec fix.
- **Copilot CLI headless surface is under-documented**: Phase 1 §12 flagged this as a gap in my research. No advocate surfaced additional documentation to close it, and build-our-own's cross-review §5.5 downgraded `copilot` to "exploratory — verify headless surface before committing." The risk is unchanged: a `CopilotCLIProvider` in any v1+ plan is partially unknown surface until someone measures `copilot`'s actual flag and output-format support.

### New risks raised during cross-review

- **Process-pooling is not in any v1 protocol shape**: The `ExecutionProvider.execute()` signature is a single async call per task. None of the advocates' revised v1 plans include a pooled / warm-worker mode for subprocess providers, yet all three cite cold-start as a real concern. This is a latent architectural risk: if v1 ships and the subprocess latency becomes a spec 048 blocker, adding pooling later may require protocol changes. The deliberation should decide now whether to bake `supports_pooling: bool` or similar into the protocol, or accept the refactor cost later.
- **LiteLLM as a proxy in front of subprocess tools is an unverified composition pattern**: Litellm-hybrid's cross-review §4.2 claims LiteLLM's OpenAI-compatible proxy mode can sit in front of subprocess-based tools (Aider, Codex, Continue) to extend their model reach. This is theoretically sound — if those tools accept OpenAI-compatible endpoints via their own config — but I did not verify the composition end-to-end, and none of the advocates' v1 plans exercise it. Flag as "interesting theoretical lever, not validated in practice."
- **Test-suite migration scope for `mock` provider is unmeasured**: Build-our-own cross-review §5.1 conceded their "stabilizes 3,428 tests" claim is under-specified. I did not audit the conversus test suite. The deliberation record should reflect that *how many of conversus's 3,428 tests actually exercise a dispatch call* is unknown; any v1 plan that treats `mock` as a test-infrastructure foundation is making an implicit claim the advocates have not measured.

### Risks mitigated during cross-review

- **Adapter code cost feared as "too high to build"**: Build-our-own's `SubprocessProvider` base class factoring mitigates this. The common substrate lives in one place; concrete providers become thin argv+parse subclasses. The total v1 cost stays in the 800–1,200 LoC range that all three advocates now accept as realistic.
- **Protocol-lock-in risk for conversus**: Build-our-own and litellm-hybrid both establish that `ExecutionProvider` is conversus-owned; A2A, LiteLLM, and future protocols are all implementation details behind the protocol. The risk of locking in to any single external dependency is mitigated by the Protocol-owns-the-boundary architecture all three advocates agree on.
- **A2A-adoption timing uncertainty**: A2a-future's revised §3.3 ("A2A as experimental/forward, subprocess as primary") and build-our-own's "add A2A when counterparties exist" mitigate the risk of betting v1 on an empty ecosystem. All three advocates now agree v1 should not depend on A2A counterparty maturity.

---

## Closing — factual posture for synthesis

My role through this deliberation has been to establish ground truth, not to pick a winner. The three advocates have arrived at positions that are more similar to each other than any of them would likely admit: all three now propose a `SubprocessProvider` base class (or equivalent), all three preserve conversus's own `ExecutionProvider` protocol, all three treat A2A as forward work rather than v1, and all three accept subprocess-CLI-JSON as the 2026-04 baseline. What distinguishes them is *emphasis* (LiteLLM-first vs conversus-first vs A2A-first) and *v1 scope* (how many providers ship in the first release).

The synthesis phase has substantially more convergence to work with than the cross-review rhetoric suggests. My factual findings are shared input to all three proposals; none of them survived contact with the evidence without modification. If the judge treats the ratified seven-point consensus in my "Convergence" section as joint-ratified input, the remaining debate is about v1 scope and emphasis — which is a legitimate engineering tradeoff discussion, not a disagreement about ground truth.

I do not recommend a winner. I report that all three revised positions are consistent with the factual landscape, and the decision is a matter of engineering priority, not correctness.
