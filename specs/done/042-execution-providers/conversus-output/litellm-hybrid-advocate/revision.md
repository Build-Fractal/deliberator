# litellm-hybrid-advocate — Phase 3 Revision

**Phase**: Round 1 Phase 3 — Defense
**Date**: 2026-04-05
**Iteration**: 1

---

## Position Summary

I no longer defend "hybrid." That word was retired in Phase 2. My refined thesis is:

**Build our own `ExecutionProvider` protocol (spec 042 §3, conversus-owned). Ship `LiteLLMProvider` in the v1 provider set as a first-class Tier-3 implementation, alongside `mock` and `claude-code`. Use a shared `SubprocessProvider` base class for CLI-based agent runtimes. Defer A2A to Phase 3 when counterparty wrappers exist. Do not ship a second hand-rolled Tier-3 SDK adapter in v1 — `LiteLLMProvider` *is* the Tier-3 adapter.**

This is substantively what build-our-own now proposes, with one narrow disagreement: **when does `LiteLLMProvider` ship, and what does it replace?**

Build-our-own Phase 2 conceded `LiteLLMProvider` should land in v1 alongside a native `anthropic` adapter. I contend that is one adapter too many for v1. Ship `LiteLLMProvider` *instead of* a hand-rolled `anthropic` adapter in v1, because (a) LiteLLM covers Anthropic better than we can, (b) the second adapter is redundant, and (c) v1 engineering budget belongs on Claude Code parity and `SubprocessProvider`, not on a parallel direct-SDK wrapper we are shipping only to have a framework-free fallback we do not need.

The remaining unchallenged claims from Phase 1 — LiteLLM's operational maturity, cost tracking, retry/fallback discipline, 100+ provider coverage, proxy mode in front of subprocess tools, security posture — still stand and decide the v1-inclusion question.

---

## Rebuttals

### Conceded: The 70/30 split framing

- **Their claim** (backbone, build-our-own): "Spec 042 is ~30% agent-runtime / ~70% model-API" is wrong. The ratio inverts once you count workloads conversus actually runs. Backbone: five of six agent runtimes are subprocess-spawn-a-CLI, not a distinct category. Build-our-own: the matrix is ~25% Tier-3 / ~75% agent-runtime-or-other.
- **Concession**: Granted, without hedging. The 70/30 split was a framing choice, not a measurement, and the researcher's §1 / §10 / §11 collapse the "agent runtime" tier into "subprocess + stdio + JSON." I retired "hybrid" in Phase 2 for precisely this reason.
- **Impact**: The concession does not change the v1 provider question. The work of shipping `claude-code` + `SubprocessProvider` is the same under all three positions. The unchallenged claim is that LiteLLM still completely owns the Tier-3 layer it covers, whether Tier-3 is 25% or 70% of the matrix. A 25% slice is still a slice conversus would otherwise write by hand, and the operational advantages (see Reinforced Strengths) do not scale down with the slice size.
- **Status**: Conceded with context.

### Conceded: The 144-cell surface area was overcounted

- **Their claim** (build-our-own §2): LiteLLM only helps on the ~3 Tier-3 rows in spec 042 §11, so the real reduction is ~23 cells, not 144.
- **Concession**: The 144 number was rhetorical. Correct number is closer to 30–40 cells where LiteLLM genuinely eliminates bespoke work — every cell Tier-3 providers need, times the realistic Tier-3 provider set including the long tail (Ollama, VLLM, LMStudio, Bedrock, Groq, Together, Fireworks, DeepSeek, xAI) that LiteLLM normalizes for free.
- **Impact**: The operational argument is cell-count-invariant. Even 30 cells of bespoke code — auth, envelopes, response parsing, streaming, function-calling format, cost calculation, error taxonomy, SDK version drift — are cells conversus would either write and maintain forever or rent via `LiteLLMProvider`. The ongoing cost is the point, not the initial line count. Build-our-own conceded this explicitly in their Phase 2 review (§5 point 2): "one upgrade cycle for 100+ models beats twelve upgrade cycles for twelve SDKs."
- **Status**: Conceded with context.

### Conceded: "Build-our-own is academic purism"

- **Their claim** (build-our-own §3): The superset framing is correct. Both positions ship spec 042 §3 verbatim. My rhetoric ("prefers owning problems to solving them") was a straw man against a position whose Week 1 code I explicitly copy.
- **Concession**: Fully conceded. My Phase 1 §9 closing line was unfair. Build-our-own's protocol is my protocol. The positions are nested, not opposing. I said so in my own cross-review of build-our-own (§1, §6, §10) and I say it again here: the `ExecutionProvider` protocol is conversus IP, not LiteLLM-shaped, and both positions agree on this.
- **Impact**: This is the concession that narrows the debate to its actual shape — not "which architecture," but "which v1 provider set." See New Arguments §1.
- **Status**: Conceded with context.

### Rebutted: LiteLLM does not cover Claude Code workloads

- **Their claim** (backbone §2): Counting "Anthropic" as a LiteLLM win is misleading because conversus's current SKILL.md workload is Claude Code agent-loop, not direct Anthropic API. LiteLLM cannot invoke `claude -p`, load CLAUDE.md, spawn subagents, or run the Read/Write/Edit/Bash tool loop.
- **My response**: Technically correct, strategically irrelevant to the v1 question. I never claimed LiteLLM replaces Claude Code. My v1 plan ships `LiteLLMProvider` **and** `claude-code` — they cover different workloads. The Claude Code provider runs agent-loop workloads (current SKILL.md, blog pipeline, spec 048 governance). The LiteLLM provider runs Tier-3 workloads where the phase does not need tools (summarization, classification, judge calls, cross-review synthesis, arbitration). Those are two separate surfaces. Spec 042 §4 explicitly defines the `supports_tool_use=False` path for exactly this case. Pre-read files into prompt, post-write output — that is the LiteLLM workload.
- **Evidence**: Spec 042 §4 lines 268–290 (the tool-use adaptation path); spec 042 §11 (the provider matrix lists `anthropic`/`openai`/`gemini` as Tier-3 direct-API *and* `claude-code` as Tier-1 agentic SDK — they are separate rows for a reason).
- **Status**: Rebutted. The backbone critique dissolves once you stop conflating "LiteLLM serves Claude Code workloads" (I never claimed this) with "LiteLLM serves direct-API workloads that are part of conversus's surface area" (I do claim this, and nothing in the cross-reviews disputes it).

### Partially Rebutted: The 3-week timeline is optimistic for SKILL.md parity

- **Their claim** (backbone §4): 3 weeks is plausible for an MVP but not for SKILL.md semantic parity (subagents, skills, hooks, MCP config, CLAUDE.md context).
- **What is true**: Full SKILL.md parity — including subagent dispatch via Claude Code's internal Agent tool, skill auto-discovery, MCP server config passthrough, streaming output parsing — probably takes 4–5 weeks, not 3. Backbone is right to call that out.
- **What is false or misleading**: The build-our-own 4–6 week estimate does not buy back SKILL.md parity either. Both positions ship a subprocess wrapper in the same timeframe. The "extra" time in build-our-own's 4–6 week estimate is not spent on subagent dispatch; it is spent on the hand-rolled `anthropic`/`openai`/`gemini` adapters that LiteLLM obviates. Subagent parity is orthogonal to the LiteLLM decision. It is a Claude Code provider problem, not a Tier-3 problem.
- **Net assessment**: Accept the schedule correction: v1 minimal ships in 3 weeks; full SKILL.md parity is 4–5 weeks. This is still faster than build-our-own's 4–6 weeks *for the same scope* because the Tier-3 layer is free. The timeline delta is conserved, just shifted to a more honest absolute value.
- **Status**: Partially rebutted.

### Rebutted: "v1-without-LiteLLM is also defensible"

- **Their claim** (build-our-own §5, conceded portion): Build-our-own conceded `LiteLLMProvider` should join v1, but still insists on shipping a native `anthropic` adapter alongside it "as the reference implementation that proves direct-SDK providers work under the protocol" and "to give users a LiteLLM-free option on day 1."
- **My response**: This is the one place I am not conceding. Both justifications fail.
  - **"Reference implementation that proves direct-SDK providers work"** — `LiteLLMProvider` *is* a direct-SDK provider. It is a concrete implementation of `ExecutionProvider` that exercises the protocol, the `supports_tool_use=False` path, the `tool_use` adaptation, the file-inlining logic, the cost metadata plumbing, and the error taxonomy. The protocol is proven the same way by wrapping LiteLLM as by wrapping `anthropic` directly. The claim that a hand-rolled `anthropic` adapter is needed to "prove" the abstraction is circular — the abstraction is proven by any adapter, and LiteLLM gives us one for 14 lines.
  - **"LiteLLM-free option on day 1"** — a `conversus-provider-anthropic` package that users who want zero LiteLLM footprint can install. But per spec 042 §10 (line 487), all providers are optional packages. Users who don't want LiteLLM don't install `conversus-provider-litellm` — they get `conversus-provider-mock` + `conversus-provider-claude-code` and nothing else. The core has no LiteLLM dependency already. What build-our-own is actually asking for is a *second* Tier-3 provider implemented via the `anthropic` SDK directly, for users who want Tier-3 coverage *and* a zero-LiteLLM footprint *and* are willing to lose OpenAI, Gemini, Bedrock, Ollama, Groq, Together, and the long tail. That is an unusually narrow intersection.
  - **The cost of the second adapter is non-zero**: 250–400 lines (build-our-own Phase 2 §5 conceded 300–450 for three native adapters; the single-provider version is ~300 lines). Plus a price table we have to keep current. Plus retry/cost/error logic that LiteLLM already provides for free. For a user population of "we want Tier-3 but refuse LiteLLM," that engineering cost is not justified.
- **Evidence**:
  - Spec 042 §10 line 487: *"Provider implementations are optional packages — only `mock` ships with core `conversus`."* No user installs LiteLLM unless they install `conversus-provider-litellm`.
  - Build-our-own Phase 2 §5 point 3: *"Shipping `LiteLLMProvider` alongside a direct `anthropic` provider means users can choose."* This is the only place build-our-own defends the second adapter, and the defense is "optionality" — but optionality is already provided by the package split. The second adapter adds no optionality; it adds 300 lines of code for a user segment that does not meaningfully exist in v1.
  - My own cross-review of build-our-own (§2): "1,200 lines is not a lot of code by absolute measure — but [the] real question is ongoing maintenance cost: cost-table drift, SDK version drift, new-model onboarding, streaming format changes, rate-limit header changes." Those costs apply to even a single hand-rolled `anthropic` adapter. LiteLLM absorbs them. Writing the adapter ourselves puts them back on our balance sheet for no corresponding user-facing benefit.
- **Status**: Rebutted. Ship `LiteLLMProvider` in v1. Do not ship a parallel hand-rolled `anthropic` adapter in v1. If a user segment materializes later that genuinely needs a LiteLLM-free Tier-3 path, add `conversus-provider-anthropic` in v2 on-demand.

### Rebutted: "LiteLLM is a single-vendor dependency"

- **Their claim** (a2a-future-advocate §3, preserved from Phase 1): Depending on LiteLLM is a supply-chain risk, contrasted against "Linux Foundation standards."
- **My response**: The backbone researcher independently verified LiteLLM's posture (§10 table, §7 "common pattern" table) — 41,900 stars, MIT license, Stripe/OpenAI production usage, multi-release-per-month cadence, security-disciplined (PYSEC-2026-2 patched March 2026). The a2a-advocate's own Phase 2 revision §5.1 concedes this: *"LiteLLM is genuinely the right tool for Tier 3 today. I withdraw the implied 'don't use LiteLLM' position."* The supply-chain attack is dead.
  - Meanwhile, `a2a-sdk` itself is Google-LLC-maintained, 0.3.25 stable / 1.0.0a0 alpha (backbone §9). If single-vendor concentration is the worry, `a2a-sdk` is strictly worse than LiteLLM on every dimension — younger, less adopted, pre-1.0, one vendor, fewer users. This is addressed in my own cross-review of a2a-future-advocate §7.
- **Evidence**: Backbone §9, §10, §11; a2a-future-advocate Phase 2 cross-review §5.1 withdrawal; my cross-review of a2a §7 single-vendor-risk comparison.
- **Status**: Rebutted. Both attacking advocates concede LiteLLM's operational posture in Phase 2. This attack is no longer live.

### Rebutted: A2A protocol-shape amendment should constrain Week 1

- **Their claim** (a2a-future-advocate Phase 2 §2, §6.1): The hybrid is silent on `ExecutionTask`/`ExecutionResult` shape, and the default will be to shape the protocol around LiteLLM's `completion_async` signature, which ossifies migration cost when A2A matures.
- **My response**: This is a legitimate concern and I accept the constraint *as an architectural footnote*, not as a v1 deliverable. Spec 042 §3 already defines `ExecutionTask` and `ExecutionResult` with `prompt`, `output_path`, `read_paths`, and `metadata` fields — a superset of LiteLLM's `completion_async` shape, already closer to A2A Task Request shape than LiteLLM's. The protocol as specified does not need to bend to LiteLLM. `LiteLLMProvider` adapts *down* from the protocol to `completion_async`, which is the correct direction. I will explicitly document in the Week 1 PR that the protocol shape is chosen to make future A2A adoption mechanical, as the a2a-advocate's §7.1 amendment proposes. Cost: ~4 hours of extra docstring and design notes. Zero impact on v1 scope.
- **Status**: Rebutted on the "hybrid is silent" charge (spec 042 §3 already has the right shape) and absorbed on the "document the intent" charge (I will add the docstring).

### Rebutted: Agent Detail / runtime discovery is unaddressed

- **Their claim** (a2a-future-advocate Phase 2 §6.3): Spec 048's long-term governance vision (multi-repo, IDE plugins) needs dynamic agent discovery, and hardcoded `default_agents:` in `.conversusrc` does not scale.
- **My response**: True but not in v1 scope. Spec 042 is an execution-provider abstraction, not an agent-discovery service. When multi-repo governance becomes load-bearing (spec 048 §10 Q4, which is not in the v1 cut), the `ExecutionProvider` protocol accepts an A2A client as one more implementation, and A2A's Agent Detail discovery slots in through that provider. The fact that v1 uses static provider registration does not preclude v2 adding runtime discovery. This is explicitly what the "A2A as Phase 3" plan buys.
- **Status**: Rebutted. Out of scope for v1 by spec definition; in scope for Phase 3 via A2A provider addition.

---

## Reinforced Strengths

These are the claims from Phase 1 that survived cross-review either unchallenged or challenged and successfully rebutted. They decide the v1-inclusion question and the agent-runtime-front-end question.

### 1. LiteLLM operational maturity is unchallenged

- **Strength**: 41,900 stars, MIT license, multi-release-per-month cadence, Stripe and OpenAI maintainers in production use, security-disciplined (PYSEC-2026-2 patched promptly), stable API surface, full async via `AsyncLiteLLM`.
- **Status**: Unchallenged. Backbone §10 independently confirmed the posture. Build-our-own Phase 2 §5 explicitly conceded: *"the model-API tier genuinely is commodity work, and paying twelve SDK upgrade cycles instead of one LiteLLM upgrade cycle is real operational cost that my review underweighted."* A2A-future Phase 2 §5.1 withdrew the supply-chain attack. **Every advocate in the deliberation now agrees LiteLLM is stable enough to ship against.**

### 2. Built-in retry, exponential backoff, rate-limit handling, circuit breakers

- **Strength**: These are production-hardening features that took LiteLLM months of real traffic to get right. They are not afternoon features. Conversus would otherwise need to write per-provider header parsing (`x-ratelimit-*`), per-provider backoff curves, per-error-class retry decisions, and idempotency-key handling.
- **Status**: Unchallenged. No cross-review contests that this work is real, worth having, or better than hand-rolling. Build-our-own's concession (Phase 2 §5 point 2) implicitly validates it by naming "upgrade cycles" as the operational cost — retries and rate-limit logic are exactly what ships in those upgrade cycles.

### 3. Cost tracking per call, built into response metadata

- **Strength**: Spec 042 Open Question #3 asks whether `ExecutionResult` should include cost data. LiteLLM answers "yes, already in the response." Writing this ourselves means maintaining a per-model, per-token-type, per-region price table that drifts every time a provider changes pricing.
- **Status**: Unchallenged. No cross-review proposes a better answer to Open Question #3 than "inherit from LiteLLM." Build-our-own concedes the maintenance treadmill. Critically: cost tracking is not optional for spec 048's governance use case — every CI run needs to surface cost for budget enforcement, and the arbiter needs to reason about phase-level cost for META_DISPUTE. LiteLLM's built-in metadata answers this cleanly.

### 4. 100+ provider long-tail coverage

- **Strength**: LiteLLM covers OpenAI, Anthropic, Google, Mistral, Bedrock, Ollama, Groq, Together, Fireworks, xAI, DeepSeek, Cohere, Hugging Face, VLLM, LMStudio, Perplexity, Replicate, and roughly 85 more. Every one is a direct hit on Tier-3, and the set expands as LiteLLM adds providers — not as conversus writes adapters.
- **Status**: Challenged on framing ("3 of 12 rows in spec 042 §11") and successfully rebutted in my cross-review of build-our-own §3. The matrix undercounts by design; it enumerates only the providers conversus has thought to list. Real user asks include Groq, DeepSeek, Together, Fireworks — all free under LiteLLM, all bespoke work under the hand-rolled alternative. The researcher's §10 independently confirms the 100+ count. Build-our-own Phase 2 §5 point 1 concedes: *"A single `LiteLLMProvider` adapter gives conversus users access to 100+ models on day 1... That breadth is a genuine user-facing win my Phase 1 position underweighted."*

### 5. LiteLLM covers local/self-hosted runtimes (Ollama, VLLM, LMStudio, LocalAI) that no other path covers cleanly

- **Strength**: This is new relative to Phase 1, surfaced by my own cross-review of the backbone researcher (§4.1). LiteLLM is first-class for offline / air-gapped / on-prem deployments. No subprocess-CLI adapter helps here (Ollama has a CLI, but most users want the HTTP endpoint). Spec 048's governance vision explicitly targets CI, cron, and webhook surfaces, some of which will be inside enterprise VPCs with no egress. LiteLLM serves those environments for free.
- **Status**: Unchallenged. No cross-review addresses the local/self-hosted angle. This is a net positive discovery from Phase 2 that strengthens v1 inclusion.

### 6. LiteLLM proxy mode in front of subprocess tools

- **Strength**: LiteLLM can run as an OpenAI-compatible proxy server exposing a single endpoint that routes to any of its 100+ backends. Tools that already speak OpenAI wire format — which includes Aider, Continue, Cursor, Codex, and anything honoring `OPENAI_BASE_URL` — can be pointed at a LiteLLM proxy and automatically gain access to every model LiteLLM supports. Users running the `SubprocessProvider` flavor for Aider / Codex / Continue get the 100-provider buffet through those CLI tools without any conversus code changes.
- **Status**: Unchallenged. This is the single most important claim in my Phase 1 review that **no cross-review engaged with at all**. Backbone did not address it. Build-our-own did not address it. A2A-future did not address it. It is a load-bearing argument for LiteLLM appearing in more than one place in the stack, and by the rules of the deliberation (silence is concession), it stands uncontested. See New Arguments §2 for the operational implication.

### 7. 14-line adapter surface for LiteLLM integration

- **Strength**: `LiteLLMProvider` wrapping `litellm.acompletion()` is a ~14-line adapter (research `tool-landscape.md` lines 613–633). The blast radius of LiteLLM going sideways is contained to that one file. If LiteLLM ever breaks us, we rewrite 14 lines over a weekend. This is the opposite of lock-in; it is a thin Facade pattern over a commodity.
- **Status**: Challenged on the "only 14 lines" claim by backbone §4 (realistic: 2–4 days for production-ready version once you factor in tool-use mapping, error taxonomy, streaming, multi-provider testing) and partially conceded. Revised estimate: the happy path is 14 lines; production-ready with full error handling and cost extraction is ~80–120 lines. Still trivial compared to the 300-line hand-rolled alternative per provider, times N providers, for a smaller coverage surface.

---

## New Arguments

### 1. The disagreement with build-our-own is now one adapter file, and we disagree on which one

- **The argument**: Phase 2 converged the architecture. Both positions ship spec 042 §3's protocol verbatim, `mock`, `claude-code` (subprocess), and `LiteLLMProvider`. The only unresolved v1 question is whether a hand-rolled `anthropic` adapter ships *alongside* `LiteLLMProvider` in v1. I say no; build-our-own says yes. This is a 300-line, ~3-engineer-day decision, not an architectural split.
- **Source**: Build-our-own Phase 2 cross-review §5 ("Concession: `LiteLLMProvider` should be in the v1 provider set") and §6 ("Summary of conceded ground"), combined with their §7 point 5 ("The `anthropic` native adapter should also ship in v1. Not as a purist gesture, but...").
- **Evidence**: My case for shipping `LiteLLMProvider` *without* a parallel hand-rolled `anthropic` adapter:
  1. **Spec 042 §10 already delivers the "zero framework footprint" option.** Users who do not install `conversus-provider-litellm` have zero LiteLLM transitive dependency. They still have `mock` + `claude-code`. Build-our-own's "LiteLLM-free Tier-3 option" requires a *third* package — `conversus-provider-anthropic` — which serves the intersection of (wants Tier-3) ∩ (refuses LiteLLM) ∩ (doesn't want OpenAI/Gemini/Bedrock/Ollama/Groq/etc). That intersection is unmeasurably small in v1.
  2. **The `supports_tool_use=False` path is exercised by `LiteLLMProvider` alone.** Build-our-own's Phase 2 §5 justification for the native adapter is "it's needed for the `supports_tool_use=False` tool-use adaptation path to be exercised." This is wrong. `LiteLLMProvider.supports_tool_use = False` — the LiteLLM adapter exercises the exact same engine code path as a hand-rolled anthropic adapter would. The protocol is proven identically by either.
  3. **v1 engineering budget is the binding constraint, and the expensive week is Claude Code subagent parity.** Backbone §4 established the realistic v1 timeline at 4–5 weeks for full SKILL.md parity. Every engineer-day spent on a redundant hand-rolled `anthropic` adapter is a day not spent on `SubprocessProvider` hardening, subagent dispatch via `parent_tool_use_id`, `--agents` JSON marshalling, `stream-json` parsing, or cold-start mitigation. The opportunity cost still exists — it just lands on agent-runtime work instead of governance features.
  4. **Ship-first, diversify-later is the right default for v1.** If, post-v1, a user segment materializes that genuinely needs a LiteLLM-free Tier-3 path (for compliance, audit, or policy reasons), adding `conversus-provider-anthropic` as a v2 on-demand package is ~300 lines of additive code. It does not block v1, and it does not compromise the abstraction. The reverse move — shipping two adapters in v1 and retiring one later — is more expensive because deprecating a v1 provider is a user-visible break.

### 2. LiteLLM proxy mode is a force multiplier for the `SubprocessProvider` base class

- **The argument**: Once we have `SubprocessProvider` as a base class for `claude-code`, `aider`, `codex`, `copilot`, `gemini-cli`, and `continue`, putting a LiteLLM proxy in front of the entire subprocess tier is a one-configuration step. Users set `OPENAI_BASE_URL=http://localhost:4000` and every OpenAI-wire-format-compatible subprocess tool automatically gains access to Groq, DeepSeek, Bedrock, Ollama, and every other LiteLLM backend. This is composition, not replication — and no cross-review engaged with it.
- **Source**: My own cross-review of backbone-researcher §4.2, unchallenged by any Phase 2 response.
- **Evidence**:
  1. **Aider reads `OPENAI_API_KEY` and `OPENAI_API_BASE`** (backbone §3.3 documents Aider's OpenAI compatibility). Point Aider at a LiteLLM proxy and it transparently gains Bedrock/Groq/Together/Fireworks/DeepSeek backend routing.
  2. **Continue's `cn` CLI has the same story** — it speaks OpenAI wire format and honors `OPENAI_BASE_URL`.
  3. **Codex CLI and Gemini CLI are less uniform**, but the pattern generalizes as those tools mature — LiteLLM is the de facto gateway layer for OpenAI-wire compatibility.
  4. **Operational implication**: A conversus user in an enterprise with "all LLM traffic goes through our LiteLLM proxy for audit/cost/policy" can use *every* conversus provider — `claude-code`, `aider`, `opencode`, `codex`, `continue` — against their centralized gateway without writing glue code. This is the kind of enterprise integration story spec 048 governance mode needs, and LiteLLM delivers it for free.
  5. **This is not available under the "hand-rolled `anthropic`" alternative**. If build-our-own wants to match this capability, they have to build a gateway layer themselves, or concede that enterprise customers deploy LiteLLM proxy regardless — at which point they have already taken the dependency and might as well ship `LiteLLMProvider`.

### 3. `SubprocessProvider` base class absorbs the backbone researcher's finding and removes the "N bespoke adapters" attack from build-our-own's quiver

- **The argument**: Backbone's §1 / §10 collapse of "five of six agent runtimes = subprocess + CLI + JSON" is not a concession — it is a gift. Because the transport is uniform, one generic `SubprocessProvider` base class plus thin per-tool argv configs replaces the N-bespoke-adapters work both positions were previously pricing in. This is a *code reduction* relative to both Phase 1 proposals, and it means my Phase 1 "N adapters to write" estimate was high.
- **Source**: My own cross-review of backbone §3, unchallenged by any Phase 2 response.
- **Evidence**:
  1. **`SubprocessProvider` base** handles: async subprocess lifecycle (`asyncio.create_subprocess_exec`), argv template substitution, stdin prompt piping, stdout capture, JSON output parsing, stderr → error mapping, exit-code → `ExecutionResult.success`, timeout handling, cwd + env passthrough, `--output-format json` vs `--output-format stream-json` demux. Estimated: ~200 lines once, covering all CLI tools.
  2. **Per-tool configs** are ~50–80 lines each: `ClaudeCodeProvider(cmd=..., parse=..., error_map=...)`, `AiderProvider(...)`, etc. This is strictly less code than six bespoke adapters.
  3. **Error centralization**: `CLINotFoundError`, `CLIConnectionError`, `ProcessError`, `CLIJSONDecodeError` live in the base class once, not once per adapter.
  4. **Testing centralization**: stdlib-mocked subprocess behavior lives in one test module.
- **Impact on the v1 decision**: With `SubprocessProvider` handling agent runtimes and `LiteLLMProvider` handling Tier-3, v1 is **two adapter layers + one base class + one registry + one protocol**, not "12 bespoke providers." That is the actual size of spec 042 v1 and it is smaller than any Phase 1 estimate.

### 4. Build-our-own's v1 proposal contains a redundancy it has not justified

- **The argument**: Build-our-own Phase 2 §5 proposes v1 = `mock` + `claude-code` + `anthropic` + `litellm`. Note the implicit claim: both `anthropic` (hand-rolled direct SDK) and `litellm` (which covers Anthropic) ship in v1. **There is no user segment that benefits from both simultaneously.** If a user wants Tier-3 for Anthropic, they install one of the two providers and ignore the other. Shipping both in v1 means paying the engineering cost for a provider every user will ignore in favor of the other.
- **Source**: Build-our-own Phase 2 §5 ("v1 providers: `mock`, `claude-code`, `anthropic`, `litellm`"), which is the summary of their conceded ground.
- **Evidence**:
  - **For users who want LiteLLM**: `conversus-provider-litellm` covers Anthropic plus 99 others. They do not install `conversus-provider-anthropic`.
  - **For users who want zero LiteLLM**: `conversus-provider-anthropic` is Anthropic-only. They do not install `conversus-provider-litellm`, and they also cannot reach OpenAI, Gemini, Bedrock, Ollama, etc. without additional hand-rolled adapters conversus has not written.
  - **For users who want both installed simultaneously**: this is a configuration redundancy with no behavioral benefit. The user picks one via the `executor:` field. The other is dead weight.
  - **Therefore**: build-our-own's v1 set contains one adapter that serves zero distinct user populations beyond what `LiteLLMProvider` alone serves. The only justification is "reference implementation for the abstraction," which is rebutted above (every provider is a reference implementation; `LiteLLMProvider` proves the protocol identically).
- **Conclusion**: The correct v1 provider set is `mock` + `claude-code` + `litellm`. Add `anthropic` in v2 if a user segment emerges that justifies it. This is the residual disagreement between my position and build-our-own's Phase 2 revision.

---

## Updated Risk Profile

### Risks confirmed by competitors (strengthens credibility)

- **Subprocess cold-start cost** for CLI-based agent runtimes (~1–3 seconds per `claude -p` without `--bare`, per backbone §11 item 10). I flagged this in my cross-review of backbone §5.3. Mitigation: `--bare` mode, process pooling (future `supports_pooling` protocol extension), parallelism via `asyncio.gather`. This applies to `claude-code` regardless of Tier-3 choice and is orthogonal to the LiteLLM decision.
- **Claude Code subagent dispatch complexity** (backbone §4). Week 2–3 is tight for full SKILL.md parity. Accepted: v1 minimal ships in 3 weeks; full parity is 4–5 weeks. Timeline amended in Rebuttals.
- **Protocol shape ossification risk** (a2a-future §2). Mitigated by explicit documentation in the Week 1 PR that `ExecutionTask`/`ExecutionResult` shape is chosen for A2A compatibility, not LiteLLM compatibility. Cost: ~4 hours of design notes.

### New risks raised

- **Hand-rolled Tier-3 adapter treadmill** (my own surfacing, strengthened by build-our-own's Phase 2 concession §5 point 2): "twelve SDK upgrade cycles beats one LiteLLM upgrade cycle." This risk applies *against* build-our-own's "also ship `anthropic` native" proposal. Shipping `LiteLLMProvider` alone in v1 avoids this risk entirely for the v1 scope; shipping a parallel `anthropic` adapter reintroduces it for one provider immediately, with no corresponding benefit.
- **Dead-weight provider risk**: Build-our-own's v1 set contains a provider (`anthropic` hand-rolled) that duplicates coverage of another v1 provider (`litellm`). Ongoing maintenance cost on a feature no user uniquely benefits from. New Arguments §4.
- **Two-ACP confusion risk** (my cross-review of a2a-future §2): Spec 042 currently uses "ACP" ambiguously between A2A (IBM/Linux Foundation, HTTP) and Agent Client Protocol (Zed/JetBrains, stdio). This is a documentation risk, not an implementation risk, and should be cleaned up in the Week 1 spec 042 amendment.

### Risks mitigated by Phase 2 cross-reviews

- **"LiteLLM supply-chain risk"** — dead. Both attacking advocates conceded LiteLLM's operational posture in Phase 2. Backbone independently verified. No longer a live risk.
- **"LiteLLM-shaped protocol lock-in"** — mitigated. Spec 042 §3's `ExecutionTask`/`ExecutionResult` is already a superset of LiteLLM's shape and closer to A2A Task Request. Documenting the intent addresses a2a-future's legitimate concern at ~4 hours of cost.
- **"Hybrid splits the abstraction in three"** — dead. Retired the word "hybrid." One protocol, N implementations, polymorphism. A2A-future withdrew this attack in Phase 2 §3.
- **"70/30 split is wrong"** — conceded, and the concession is free. The ratio does not determine the v1 provider question; the operational-cost argument does, and it is cell-count-invariant.
- **"Build-our-own is strategically incoherent"** — retracted (my Phase 1 §9 closing was unfair). Build-our-own's architecture is my architecture. The remaining disagreement is one adapter file.

### Residual risks I still own

1. **`LiteLLMProvider` production-ready adapter is not 14 lines** — it's 80–120 lines once error handling, cost extraction, streaming, and multi-provider testing are included. Realistic effort: 2–4 engineer-days, not "a weekend." This is still trivially cheaper than any alternative and does not change the v1 decision.
2. **LiteLLM occasional pricing lag** in the `model_cost` table. Mitigation: conversus-level price override hooks if accuracy becomes critical for spec 048 budget enforcement. Deferred to v2 unless a user complaint surfaces.
3. **A2A sequencing commitment**: Phase 3 must schedule the `a2a` provider with a concrete trigger (a2a-sdk ≥ 1.0 stable AND at least one third-party A2A wrapper of a coding agent exists), per a2a-future Phase 2 §7.3. Cost: zero today. Prevents "Phase 3" from becoming "Phase Never."

---

## Closing (narrow the fight)

Phase 2 converged everything except one 300-line adapter file. The architecture, the protocol, the Tier-1 story, the A2A deferral, the `mock` + `claude-code` + `litellm` core of v1 — all agreed. The residual disagreement is:

**Ship `LiteLLMProvider` in v1 (my position). Do not ship a parallel hand-rolled `anthropic` adapter in v1 (my position; build-our-own disagrees).**

Build-our-own's justification for the redundant adapter rests on three claims, all of which are rebuttable:
1. "Reference implementation for the protocol" — `LiteLLMProvider` is a reference implementation.
2. "LiteLLM-free Tier-3 option" — already provided by the optional-package split; the additional adapter only serves an empty user intersection.
3. "Proves `supports_tool_use=False` path" — `LiteLLMProvider.supports_tool_use = False` already exercises this path identically.

The unchallenged claims that decide the fight are:
- **LiteLLM operational maturity** (every advocate now agrees).
- **Built-in retry, rate-limit, cost tracking, streaming** (unchallenged; answers spec 042 Open Question #3).
- **100+ provider long-tail absorption** including local/self-hosted (Ollama, VLLM, LMStudio) — critical for spec 048's enterprise governance surfaces.
- **Proxy mode in front of subprocess tools** — unchallenged, not addressed by any Phase 2 review, directly enables enterprise LLM-gateway integration through every `SubprocessProvider` target.
- **14-line (production: ~100-line) adapter surface** — trivial compared to any alternative.

`LiteLLMProvider` belongs in v1. A hand-rolled `anthropic` adapter does not. That is the argument.

---

**End of revision.**
