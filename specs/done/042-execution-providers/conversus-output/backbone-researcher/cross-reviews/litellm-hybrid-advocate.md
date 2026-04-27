# Cross-Review: litellm-hybrid-advocate

**Reviewer**: backbone-researcher
**Target**: litellm-hybrid-advocate/review.md
**Date**: 2026-04-03
**Mode**: Factual evaluation against the ground-truth findings in my own review. Not advocacy.

---

## 0. Summary of the finding

The litellm-hybrid position has a solid core (LiteLLM is real, mature, and genuinely solves the direct-model-API problem) but it is built on a tier taxonomy that does not survive contact with the architectural facts I established. Specifically, the "Tier 1-2 agent runtimes / Tier 3 model APIs" split assumes the two tiers are different kinds of work, and my ground-truth section §1 and §10 show they are largely the same kind of work — subprocess-spawn a CLI. Once that collapse happens, the "70% of the problem is solved for free" framing becomes "X% of a differently-shaped problem is solved for free, where X depends on how you count workloads conversus actually runs."

Where the advocacy is accurate, I say so. Where it rests on assumptions I verified to be wrong, I say that too.

---

## 1. Does the "Tier 3 APIs (LiteLLM) / Tier 1-2 runtimes (native)" split hold up?

**Partially. The seam the advocacy draws is not where the advocacy thinks it is.**

The advocate's mental model is:

- Tier 3 = "direct API" = OpenAI/Anthropic/Google/Ollama HTTP endpoints. LiteLLM covers this.
- Tier 1-2 = "agent runtimes" = Claude Code, OpenCode, Aider, Copilot CLI, Codex CLI, Gemini CLI. Native adapters.

Two of the assumptions inside that split are incorrect against my findings:

**a) Claude Code is not an "agent runtime" in the sense of "a thing with its own dispatch protocol that is categorically different from a model API."** Per §1.2 of my review, `claude-agent-sdk` (Python) and `@anthropic-ai/claude-agent-sdk` (TS) are thin wrappers that spawn the bundled `claude` CLI binary as a subprocess and speak JSON-RPC over stdio. The "agent runtime" is literally `subprocess.run(["claude", "-p", prompt, "--bare", "--output-format", "json", ...])` plus flag marshalling. There is no network API, no HTTP server, no daemon. It is a fork-exec.

This matters for the advocacy because it means a "native `claude-code` provider" is not a materially harder object than a "LiteLLM provider for `anthropic/claude-3-5-sonnet`." It is a `subprocess.run(...)` with argv construction and stdout JSON parsing. Whether the advocate counts that as "Tier 1 work" or "Tier 3 work," the actual labor is closer to the latter than the advocacy implies.

**b) The same collapse applies to every other "agent runtime" in the list.** Aider: `aider --message "..." --yes` (§3). Copilot CLI, Codex CLI, Gemini CLI, Continue's `cn`: subprocess + flags (§5, §10 table). OpenCode is the **only** exception in my §10 table that ships a real HTTP server (`opencode serve`, OpenAPI 3.1) — and even OpenCode has no Python SDK, so the conversus-side work is still either "httpx against the OpenAPI spec" or "generate a client from the spec." OpenCode is the one place where the "agent runtime" category genuinely has a different shape than "subprocess a CLI."

**What the "agent runtime" tier actually reduces to, concretely:**

| Tool | The "runtime adapter" is | Fundamentally different from a LiteLLM wrapper? |
|---|---|---|
| Claude Code | `subprocess.run(["claude", "-p", ...])` + JSON parse | No — it's subprocess plumbing vs HTTP plumbing |
| Aider | `subprocess.run(["aider", "--message", ...])` + output scrape | No |
| OpenCode | `httpx` against `opencode serve` OpenAPI 3.1 | **Yes** — this is real HTTP, closest analog to LiteLLM |
| Copilot CLI | `subprocess.run(["copilot", ...])` + JSON parse | No |
| Codex CLI | `subprocess.run(["codex", ...])` + JSON parse | No |
| Gemini CLI | `subprocess.run(["gemini", ...])` + JSON parse | No |
| Continue `cn` | `subprocess.run(["cn", ...])` + output scrape | No |

**Verdict on the split**: The taxonomy is coherent as a conceptual organization ("direct-API vs agent-that-does-its-own-tool-loop"), and the advocate is correct that LiteLLM's scope maps cleanly onto the direct-API half. But the claim that the other half is an intrinsically harder category of work is not supported by my findings. Five of the six "Tier 1-2" agent runtimes are subprocess wrappers that each require roughly the same kind of adapter code (argv construction, stdout/JSON parsing, error code mapping) — not fundamentally more complex than LiteLLM's own wrapper code, just not the same wrapper. OpenCode is a genuine exception and is the one place where a "separate category" framing is defensible.

---

## 2. Is LiteLLM useful for Claude CLI invocation, or only for direct Anthropic API?

**Only for direct Anthropic API. LiteLLM cannot invoke the `claude` CLI or the `claude-agent-sdk` agent loop.**

This is a distinction my review established but the advocacy elides. LiteLLM's `litellm.completion(model="anthropic/claude-3-5-sonnet-20241022", ...)` routes to Anthropic's `/v1/messages` HTTPS endpoint. It is a stateless, single-turn, model-API call. It does not:

- Load the Claude Code agent loop (the thing that does Read/Write/Edit/Bash/Glob/Grep/Agent tool dispatch).
- Spawn subagents via the in-session `Agent` tool (§1.4 of my review).
- Honor CLAUDE.md / skills / plugins / hooks / MCP server config.
- Produce the same output as `claude -p "..."` — because `claude -p` is running the entire Claude Code agent loop, with tool use, file I/O, and plan mode, while `litellm.completion(...)` is doing a raw model call with whatever tools you hand-construct in the request.

Put plainly: **using LiteLLM to talk to Anthropic is not using Claude Code. It is using the Anthropic API, the same way you would use it before Claude Code existed.**

This has two consequences for the advocacy:

1. **When the advocate says "LiteLLM covers Anthropic," that is true only for the direct-API case.** Any conversus workload that needs the Claude Code agent loop (skill auto-discovery, CLAUDE.md context, the bundled Read/Write/Edit/Bash tools, subagent dispatch, MCP servers already configured in the user's Claude setup) is NOT served by LiteLLM. It requires a `claude-code` provider that either subprocesses `claude -p --bare` or uses `claude-agent-sdk.query()` (which itself subprocesses).

2. **Conversus's current SKILL.md workload is the agent-loop case, not the direct-API case.** The SKILL.md dispatches agents that read files, write review artifacts, spawn subagents, use skills, and operate with CLAUDE.md context. LiteLLM's Anthropic support does not replace any of that. It replaces a different, thinner kind of call.

The advocacy does not explicitly claim LiteLLM replaces Claude Code. But by counting "Anthropic" as a LiteLLM-covered provider in the "70% solved" framing, it creates the impression that the hybrid approach gets Anthropic for free. It gets *direct Anthropic API* for free. It still has to write the `claude-code` adapter to serve the conversus workloads that the SKILL.md actually runs today. Those are different things and the advocacy blurs them.

---

## 3. Is the "30% agent runtime work remains" figure accurate?

**The 70/30 split is a framing choice, not a measurement, and the underlying framing does not match the actual workloads.**

The advocacy presents "~30% agent-runtime, ~70% model-API" as the shape of spec 042's problem. Two issues:

**a) The percentages come from the research report's framing, not from a measurement of conversus's workloads.** They reflect "how much of the provider matrix in spec 042 §11 does LiteLLM cover" — which is a count of boxes, not a count of calls, workloads, or engineering days. If you weight by the workloads conversus actually ships today (SKILL.md dispatch inside Claude Code sessions, which uses the Claude Code agent loop, not direct Anthropic API), the model-API tier is closer to 0% of current production usage. If you weight by the workloads spec 048 envisions (CI gates, cron audits, governance checks — which in the advocacy's own plan run via the `claude-code` provider, not LiteLLM), the model-API tier is still a minority of first-cohort usage.

**b) "30% agent-runtime work" understates the actual engineering cost because the agent-runtime work is the work that will be exercised first and hardest.** From my §1 and §10: the `claude-code` adapter has to handle subprocess lifecycle, CLI flag marshalling, `--bare` mode semantics, `--output-format stream-json` parsing, `--allowedTools` / `--permission-mode` / `--agents` / `--append-system-prompt` / `--mcp-config` / `--resume`, process cold-start cost (~1-3 seconds per invocation without `--bare`, per my §11 item 10), parent_tool_use_id tagging for subagents, and error mapping from `CLINotFoundError`/`CLIConnectionError`/`ProcessError`/`CLIJSONDecodeError`. None of this is covered by LiteLLM. All of it is exercised on day 1 because the `claude-code` provider is what runs conversus's current workloads.

Meanwhile, the "70%" saved by LiteLLM is real savings — I am not disputing that LiteLLM genuinely covers 100+ direct-model endpoints, does cost tracking, retries, rate limits, and format normalization. Those savings are worth having. But they are savings on workloads that are not the current SKILL.md workload and are not the first thing spec 048 ships.

**Verdict**: The 30% figure is directionally defensible if you count provider matrix boxes. It is misleading if you count engineering hours spent on what actually runs first. The agent-runtime work is not 30% of the total — it is closer to 100% of the work needed to unblock spec 048's first release, plus whatever additional LiteLLM-covered workloads conversus chooses to enable later.

---

## 4. Is the 3-week estimate realistic?

**Week 1 is plausible. Week 2 is the hard week and the advocacy underestimates it. Week 3 is reasonable.**

Let me walk through the advocacy's week-by-week plan against my findings:

**Week 1 (Core + Tier 3 via LiteLLM)**
- Implement `ExecutionProvider` / `ExecutionTask` / `ExecutionResult` — this is pure spec work, maybe 2-3 days.
- Implement `PROVIDER_REGISTRY` and `get_provider()` — 1 day.
- Wrap `litellm.completion_async()` as a `LiteLLMProvider` — the advocacy cites "14 lines of code." That is plausible for the happy path. It is not plausible for production use once you factor in: mapping `ExecutionTask.tools` to LiteLLM's tool-calling format, mapping `ExecutionResult.cost` from LiteLLM's response metadata, handling LiteLLM's error taxonomy, streaming support if desired, and testing against at least Anthropic + OpenAI + Google + Ollama. Realistic: 2-4 days, not "a weekend."
- File-inlining adapter for `supports_tool_use=False` path (spec 042 §4) — this is non-trivial and the advocacy treats it as a one-liner. Realistic: 2-3 days.

Week 1 total: 7-11 engineer-days of work compressed into 5. Possible with a focused engineer but tight.

**Week 2 (Claude Code provider)**
The advocacy says "Subprocess wrapper is the recommended option (report line 975). No LiteLLM involvement." This is the week the advocacy hand-waves. From my §1:

- `claude -p --bare --output-format json` flag surface: `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--settings`, `--mcp-config`, `--agents`, `--append-system-prompt`, `--json-schema`, `--continue`, `--resume`. Each one that conversus wants to expose through `ExecutionTask` has to be marshalled.
- Subprocess lifecycle: timeouts, graceful vs forced termination, stdout/stderr capture, streaming output parsing if `--output-format stream-json`.
- Error mapping: `CLINotFoundError`, `CLIConnectionError`, `ProcessError`, `CLIJSONDecodeError`.
- `ClaudeAgentOptions` vs CLI flags — decide whether to use the SDK or raw subprocess. If SDK, deal with async generator semantics; if raw, deal with flag drift as Anthropic ships new flags.
- Cold-start cost (~1-3 seconds per call without `--bare`, per my §11 item 10). For a conversus run with 10-30 parallel agent phases, this is a measurable latency floor that the design has to accommodate (e.g., via parallelism, via persistent sessions with `--resume`, or by accepting the cost).
- Subagent dispatch: if conversus wants to use the Agent tool to spawn subagents (which is what the current SKILL.md does), the provider has to construct `--agents` JSON and parse `parent_tool_use_id` tagging in messages.
- Testing: at minimum, smoke tests against a real `claude` binary, plus the file-inlining adapter path for the no-tool-use case.

Realistic week 2: 5-10 engineer-days. The advocacy's "one week" is achievable for a minimal subprocess wrapper that supports prompt-in / JSON-out and nothing else. It is not achievable for a wrapper that preserves the full SKILL.md dispatch semantics (subagents, skills, hooks, MCP config, CLAUDE.md context, streaming).

**Week 3 (Tests, docs, backward compat)**
Reasonable if weeks 1 and 2 came in on time. Optimistic if they didn't.

**Overall verdict on 3 weeks**: Plausible for a minimum-viable implementation that ships a LiteLLM provider (narrow scope, happy-path testing) and a Claude Code subprocess provider (minimal flag support, no subagents). **Not plausible** for an implementation that preserves current SKILL.md dispatch semantics, because preserving those requires the Claude Code provider to handle subagent dispatch, which the advocacy does not scope. If the MVP ships in 3 weeks and subagent parity slips to week 4-5, that is a reasonable tradeoff — but the advocacy should say so explicitly instead of presenting "3 weeks" as covering the full SKILL.md-equivalent scope.

The build-our-own 4-6 week estimate the advocacy attacks is not obviously wrong given this accounting. Much of the "extra" time in 4-6 weeks is exactly the Claude Code subagent / streaming / flag-coverage work that also needs to happen under the hybrid approach — it is delta against LiteLLM coverage, not delta against total work.

---

## 5. Does the position depend on any false assumptions about A2A or agent runtimes?

**Two assumptions are shaky; one is effectively correct.**

**Shaky assumption 1: "A2A wrapper effort is ~500 lines per SDK" treats A2A as a real option today.**

The advocacy cites report line 654 and argues that hybrid avoids the 500-lines-per-SDK A2A cost. This rebuttal is valid *if* you believe the "A2A-future" position is actually proposing A2A today. My §9 establishes that A2A 1.0.0 shipped 2026-03-12 (less than a month ago), the Python SDK is `a2a-sdk` 0.3.25 stable / 1.0.0a0 alpha, and **no shipping agentic coding tool has been wrapped as an A2A server yet** — not Claude Code, not Aider, not Copilot, not Codex, not Gemini, not OpenCode. If conversus wanted to ship an A2A provider today it would have nothing on the other end of the wire and would have to build the wrappers itself.

So the advocacy's attack on A2A ("operational overhead," "ecosystem too new," "500 lines per SDK") is directionally correct on the facts. But the framing "we'd have to write 1,500 lines of A2A server code in addition to the ExecutionProvider work" overstates the contrast: the hybrid approach **also** has to write adapter code for Claude Code / Aider / OpenCode, and those adapters are non-trivial. The hybrid saves the A2A-server layer but not the underlying SDK-adapter work. The advocacy counts the A2A server cost against A2A but does not count the equivalent subprocess-adapter cost against hybrid.

**Shaky assumption 2: "The ExecutionProvider protocol absorbs A2A without engine changes" assumes the protocol is well-shaped for multi-turn / async / streaming A2A semantics.**

A2A supports sync request/response, SSE streaming, and async push notifications (my §6.2). The `ExecutionProvider.execute()` signature in spec 042 §3 is a single async call with a single `ExecutionResult` return. That fits sync A2A fine; it is a less-clean fit for A2A's async push-notification mode (long-running tasks where the agent calls back when done). If conversus adopts A2A later, the protocol abstraction may need to grow to accommodate it — the advocacy's "A2A just slots in" claim is plausible but not guaranteed. This is a minor caveat, not a fatal flaw.

**Effectively correct: LiteLLM is real, mature, and a commodity.**

The advocacy's claims about LiteLLM — 100+ providers, MIT license, active maintenance, Stripe/OpenAI production usage, stable API surface, built-in cost tracking and retries — are consistent with what I would expect given the project's public footprint. I did not independently re-verify the 41,900 stars figure or the specific security advisory (PYSEC-2026-2) but the ambient facts about LiteLLM match. **If conversus needs direct-model-API coverage, LiteLLM is the right answer and the advocacy is correct on that narrow point.** The question is whether "direct-model-API coverage" is what spec 042 actually needs to ship first, and my finding is that it is not the primary blocker for current SKILL.md workloads or for the spec 048 critical path.

**Assumption about "agent runtimes" that is wrong but load-bearing: that "agent runtime" is a distinct category of work.**

Per question 1 above, the advocacy's taxonomy treats Tier 1-2 ("agent runtimes") as a fundamentally different kind of work from Tier 3 ("model APIs"). My findings show that for five of the six agent runtimes, the work is subprocess + CLI flags + stdout parsing — the same shape as any other CLI wrapper, and not the same shape as an HTTP/SDK wrapper. This does not invalidate the hybrid approach (LiteLLM still saves real work on the direct-API side), but it means the "70/30 split" and "hybrid = pay only for what's unique" framings collapse once you look inside. The unique conversus work is in the orchestration layer (phase sequencing, dispute parsing, gate evaluation) — which is not a provider concern at all, and which every one of the three positions preserves identically. Whether the provider layer uses LiteLLM, hand-rolled SDKs, or A2A does not change how much orchestration work conversus has to do.

---

## 6. What the advocacy gets right

To be clear, the litellm-hybrid position has real strengths that my findings confirm:

1. **LiteLLM is the right tool for direct-model-API coverage.** If conversus needs to support OpenAI, Google Gemini (API), Mistral, Bedrock, Ollama, Together, Groq, Fireworks, or any of the other 100+ providers LiteLLM covers, writing that from scratch would be wasteful. The 144-cell bespoke-code table in §3 of the advocacy is a fair accounting of what build-our-own has to maintain per direct-API provider, and LiteLLM does cover that surface.

2. **The `ExecutionProvider` protocol is conversus's IP and should be conversus-owned.** The advocacy is right that LiteLLM should not own the abstraction boundary; it should be rented as an implementation for one tier. This is architecturally clean.

3. **MCP is not the right layer for agent dispatch.** The advocacy does not make this claim directly, but it implicitly agrees by not proposing MCP as a provider. My §8 confirms this.

4. **Shipping risk matters and spec 048 is blocked on 042.** The advocacy's point that engineering time spent on commodity SDK glue is time not spent on spec 048's governance-specific work is valid. The question is how much of the hybrid plan is actually commodity SDK glue savings vs. how much is savings the advocacy claims but doesn't fully deliver against the agent-runtime workloads.

5. **The advocacy is correct that A2A is not ready today.** My §9 independently arrives at the same conclusion via different evidence (protocol version, SDK maturity, absence of counterpart wrappers). The "A2A-future" position faces genuine maturity headwinds in 2026-04.

---

## 7. What the advocacy gets wrong or underweights

1. **The tier split mislabels the work.** "Tier 1-2 agent runtimes" is not a separate category of engineering effort from "Tier 3 model APIs" for five of the six tools in scope. Both reduce to adapter code. The adapter shape differs (subprocess vs HTTP vs library call), but the engineering cost per adapter is in the same order of magnitude.

2. **LiteLLM does not cover Claude Code.** It covers direct Anthropic API. These are not the same thing for conversus's current SKILL.md workloads. The advocacy counts "Anthropic" as a LiteLLM win without noting that the Anthropic workloads conversus actually runs today are Claude Code agent-loop workloads, which require a separate `claude-code` provider regardless.

3. **The 3-week estimate is optimistic for SKILL.md parity.** It is plausible for an MVP that ships a LiteLLM provider + a minimal Claude Code subprocess wrapper. It is not plausible for a Claude Code provider that preserves subagent dispatch, skills, hooks, MCP config, and CLAUDE.md context — which is what current conversus workloads use.

4. **The attack on build-our-own's 4-6 week estimate is partially self-defeating.** The "extra" 1-3 weeks in the build-our-own estimate is largely the same Claude Code / Aider / OpenCode adapter work that hybrid also has to do. The hybrid saves the direct-API adapter work (~1-2 weeks of it), not the agent-runtime adapter work.

5. **"Three providers on day 1" straw-mans build-our-own.** The advocacy argues build-our-own only covers 1-3 providers day 1 vs LiteLLM's 100+. This is true if you count the provider matrix. It is less meaningful if you count the providers conversus users actually ask for in the first cohort — Claude Code and OpenAI are the common asks and both are covered by either approach.

---

## 8. Bottom line (non-advocacy)

The litellm-hybrid position is a coherent engineering proposal with a real strength (LiteLLM genuinely covers the direct-model-API tier) and a real weakness (the "tier split" framing conflates different kinds of work and undercounts the effort needed to ship a Claude Code provider that matches current SKILL.md semantics).

- The advocacy's "70% of the problem is already solved" claim is directionally true if you count provider matrix boxes, and directionally misleading if you count current conversus workloads.
- LiteLLM does not help with the Claude Code agent loop — only with direct Anthropic API calls. These are different things and the advocacy does not distinguish them.
- The "Tier 1-2 agent runtimes" category is mostly subprocess wrappers, not a separate engineering species. OpenCode is the lone exception with a real HTTP server.
- The 3-week timeline is achievable for an MVP and tight for SKILL.md parity.
- The attacks on A2A-future are factually well-supported by my findings.
- The attacks on build-our-own overstate the savings LiteLLM provides against the work that actually needs to happen.

The litellm-hybrid approach is not wrong. It is a reasonable engineering choice for the direct-API tier. But the advocacy oversells the magnitude of the savings by conflating "LiteLLM covers the Anthropic API" with "LiteLLM covers what conversus currently does with Anthropic" — and those are different claims.

---

**End of cross-review.**
