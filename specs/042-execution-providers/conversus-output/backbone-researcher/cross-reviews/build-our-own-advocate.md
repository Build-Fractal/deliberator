# Cross-Review: Build-Our-Own-Advocate

**Reviewer**: backbone-researcher
**Target**: build-our-own-advocate/review.md
**Date**: 2026-04-03
**Mode**: Fact-check the advocacy against Round 1 ground truth. Not advocacy.

---

## 0. Summary of verdict

The advocate's core structural argument — *"there is no library whose public API is `execute(prompt, read_paths, output_path, metadata) -> ExecutionResult` covering both model APIs and agent runtimes"* — is **factually correct** and matches my Round 1 finding (§7, §10). No such library exists. Their framing of the problem shape is right.

However, several of their secondary claims either (a) misrepresent cost, (b) understate implementation complexity created by the subprocess-wrapper reality, or (c) make a "superset" claim about ACP/A2A that does not hold up under the two-protocol distinction I established in §6.

Itemized below.

---

## 1. Does their position assume a library exists where none does?

**No — this claim checks out.** This is the strongest part of their argument and it aligns with my findings.

The advocate writes (§3.1): *"Name the library whose public API looks like [their four-arg execute signature] and covers both `anthropic` API calls and `claude-agent-sdk` subprocess dispatch under one interface. It does not exist."*

My Round 1 §7 table confirmed this:
- LiteLLM: model APIs only, zero agent runtimes (my §10 row + §7).
- A2A: wire protocol with Python SDK still at 0.3.25 stable / 1.0.0a0 alpha, and as of 2026-04 there is no shipping A2A server wrapping Claude Code, Aider, Copilot, Codex, Gemini, or OpenCode (my §9).
- pydantic-ai / LangGraph / CrewAI: agent frameworks that *are* runtimes, not adapters over runtimes.
- MCP: wrong layer entirely (my §8).

So the advocate's "there is no wheel, only half-wheels from different vehicles" metaphor is consistent with the evidence I gathered. **This claim is verified.**

What I would add for the record: the absence of such a library is not purely because nobody tried. It is partly because the tools themselves do not expose compatible primitives. Claude Code's only public primitive is a CLI subprocess (my §1.2). Aider's only stable interface is a CLI subprocess (my §3). OpenCode has HTTP, but no Python SDK (my §2.1). Any "unifying library" has to be a subprocess-wrapper + HTTP-client hybrid — which is exactly what the advocate is proposing to build. So the argument "nobody has built this" is downstream of the fact that "the tools this would unify do not present unifiable surfaces". That makes their proposal viable, but it also makes the implementation cost higher than they claim — see §2 of this cross-review.

---

## 2. Does their cost estimate ("100–200 lines per adapter") hold up?

**Partially, and with important caveats.** The advocate cites tool-landscape.md line 757 (*"Each provider is a thin adapter (100-200 lines of code)"*) and concludes (§3.2) that *"the initial deliverable — protocol + data classes + registry + mock + anthropic + claude-code — is ~500–700 lines of code."*

Against my Round 1 findings:

### 2.1 `mock` — likely correct
A pure-Python mock implementing the Protocol is straightforwardly ~50–100 lines. No issue.

### 2.2 `anthropic` — likely correct
The `anthropic` SDK is a first-party Python package with a clean async interface. An adapter that (a) receives `prompt` + inlined `read_paths`, (b) calls `client.messages.create(...)`, (c) writes the returned text to `output_path`, (d) returns an `ExecutionResult` is plausibly 100–200 lines including error handling and retry. **Estimate holds.**

### 2.3 `claude-code` — the cost is load-bearing and the estimate understates it

This is where my Round 1 findings put pressure on the advocate's number. Specifically (my §1.2, §1.3, §1.4):

- There is no "direct API" path to Claude Code. The `claude-agent-sdk` Python package is itself a subprocess wrapper around the bundled `claude` CLI binary. It spawns the binary and speaks JSON-RPC over stdio. This is not an implementation detail — it is the only architecture available.
- The alternative (bypassing the SDK) is spawning `claude -p --bare --output-format json ...` directly from Python. Also a subprocess.
- Either way, a `claude-code` provider is a subprocess-lifecycle manager, not a thin API adapter.

What 100–200 lines does *not* cover realistically for a production `claude-code` provider:

1. **Process lifecycle**: spawn, track PID, stream stdout/stderr concurrently, detect exit, handle kill on timeout, handle zombie processes, reap, handle signal propagation on cancellation.
2. **JSON stream parsing**: `--output-format stream-json` emits one JSON object per line; partial lines across buffer boundaries must be handled; the advocate's `execute` returns a single `ExecutionResult`, but the CLI emits a stream of events (assistant messages, tool_use blocks, tool_results, final result) — the adapter must reduce a stream to a result.
3. **Flag construction**: `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--mcp-config`, `--agents`, `--append-system-prompt`, `--settings`, `--resume`, `--session-id` — mapping `ExecutionTask.metadata` to this flag surface is real translation work.
4. **Binary discovery**: handling missing CLI, wrong version, `cli_path` override, PATH lookup. My §1.2 documents `CLINotFoundError`, `CLIConnectionError`, `ProcessError`, `CLIJSONDecodeError` as the SDK's own error classes — a from-scratch adapter has to reproduce all four.
5. **Cold-start cost and `--bare`**: my §11 point 10 — CLI cold-start is 1–3s without `--bare`, must be explicitly opted into, interacts with hooks/skills/plugins discovery.
6. **`read_paths` semantics**: Claude Code reads files via its own `Read` tool when the model decides to; it does not accept "here is a list of files, preload them" as a flag. The adapter must either (a) inline file contents into the prompt (which is what spec 042 §4 lines 268–290 proposes for non-tool-use providers, but Claude Code *does* support tool use so inlining is wrong), or (b) rely on the model to `Read` them (but then you must communicate the list in the prompt text), or (c) use `--add-dir` and document path semantics. None of these are zero-line choices.
7. **`output_path` semantics**: Claude Code's Write tool writes wherever the model decides. Enforcing "you MUST write to exactly this path" is a prompt-engineering + verification problem, not a flag. The adapter has to post-validate the file exists at the expected path and error loudly if the model wrote somewhere else.

A reasonable lower bound for a production `claude-code` subprocess adapter that handles all of the above is **~400–800 lines**, not 100–200. The advocate's cited range probably assumes "call the SDK's `query()` function and await the async iterator" which is ~50 lines of happy-path glue — but that elides items 4, 5, 6, 7 above and still takes a subprocess hit per call.

**Adjusted v1 total**: ~800–1,200 lines (mock 100 + anthropic 200 + claude-code 400–800 + protocol/dataclasses/registry 100). Still small in absolute terms — the advocate's "less than a single Django admin class" framing survives — but the estimate they quote is off by roughly 2x on the load-bearing provider.

### 2.4 The research-doc cited number is not an independent data point

The advocate quotes `tool-landscape.md` line 757 as the source. That document is internal to the spec-042 deliberation, not an empirical study of shipping adapters. I have no evidence the 100–200 number was derived from measuring an actual working Claude Code subprocess adapter against the concerns enumerated in §2.3 above. It reads to me as an unverified planning estimate, not ground truth. The advocate is entitled to use it, but it should not be treated as a load-bearing fact.

---

## 3. Does their "superset" argument (we CONTAIN LiteLLM / ACP as providers) survive?

**Partially for LiteLLM. Not in the way they claim for A2A/ACP, because the advocate conflates two protocols.**

### 3.1 LiteLLM superset — yes, this works

The advocate's §5 argument is: *"Build-our-own can include a `LiteLLMProvider` adapter whenever we decide LiteLLM is worth the dep (it's a 100-line wrapper). Nothing in this proposal prohibits that."*

This is factually sound. LiteLLM's API shape (`litellm.completion_async(model=..., messages=...)`) maps cleanly to a Protocol adapter: take `prompt`, inline `read_paths`, call LiteLLM, write output, return `ExecutionResult`. This is in fact the exact pattern that solves the direct-model-API tier. The superset claim holds for LiteLLM because LiteLLM itself is a pure model-API layer with no agent-runtime ambitions.

### 3.2 ACP / A2A superset — claim does not survive unchanged

The advocate's §3.4 and §4 repeatedly treat "ACP provider" as a single thing that will drop in later. They cite spec 042 §11's `acp` provider entry and the "protocol-stack diagram". They write (§3.4):

> *"The protocol we're proposing is deliberately ACP-compatible at the concept level: prompt maps to the Task Request text part, read_paths maps to reference parts, output_path maps to metadata, our metadata dict maps to Task Request custom fields. This is not an accident — the spec author explicitly designed it to be a superset that collapses to ACP when an ACPProvider is added."*

My Round 1 §6 establishes that "ACP" in the current (2026-04) landscape refers to **two entirely different protocols**:

1. **A2A / IBM ACP (merged)** — JSON-RPC 2.0 over HTTP(S), agent-to-agent dispatch, Linux Foundation LF AI & Data, `a2a-sdk` Python 0.3.25 stable / 1.0.0a0 alpha. This *could* be the target of a future adapter, but per my §9 there are no A2A-wrapped coding agents to dispatch to yet.

2. **Zed/JetBrains Agent Client Protocol** — JSON-RPC over stdio (primary) or HTTP/WebSocket (experimental), IDE ↔ coding agent, v0.11.4 (pre-1.0), "LSP for agents". Claude Code, Codex CLI, Copilot CLI, OpenCode, Gemini CLI are all in its agent registry — but the protocol's threat model assumes a live human in the IDE approving tool calls. It is not designed for headless CI dispatch.

The advocate's "superset" argument about the four-field `execute()` shape mapping to "Task Request text part + reference parts + metadata" describes the **A2A** task model (per my §6.2). But the actual shipping ecosystem of coding agents reachable via "ACP" today is the **Zed/JetBrains ACP** one (per my §6.3). Those are not the same wire, not the same transport, not the same semantic model.

Concrete implications the advocate did not address:

- A `JetBrainsACPProvider` would be viable *today* as a subprocess provider (e.g. `opencode acp`, or spawning `claude` in its ACP mode if that exists). But it speaks stdio JSON-RPC and assumes a session lifecycle with human-approval gates — it is not a drop-in for headless dispatch.
- An `A2AProvider` would be viable *when wrappers exist*, but per my §9 no such wrappers exist for Claude Code / Copilot / Codex / Gemini / Aider / OpenCode as of 2026-04, which means shipping an `A2AProvider` in spec 042 would be a provider with no server on the other end.
- The advocate's "one acp provider" does not distinguish these. Either:
  - The advocate means A2A — in which case it is a real protocol with no counterparties yet (my §9), and the "add it when A2A matures" plan is correct but the adapter is not a drop-in: it ships nothing usable until the counterparty ecosystem exists.
  - The advocate means Zed/JetBrains ACP — in which case it is a live protocol with counterparties, but the transport model (stdio JSON-RPC subprocess with interactive tool-approval) is a poor fit for spec 048's "autonomous governance" headless use case (my §11 point 6).
  - The advocate means "both" — in which case spec 042 §11 needs two entries, not one, and the "it's the same adapter" framing is wrong.

**The "superset" claim survives for LiteLLM. It does not survive unchanged for ACP/A2A** — the advocate's own proposal needs to split the single `acp` provider row into at least two distinct provider types with different semantics, timelines, and use cases. This is not fatal to the build-our-own position — it actually strengthens it, because *owning* the Protocol is exactly what lets you have two providers where the wire-level standard has two protocols. But the advocate's rhetoric that it's "one provider we add later" is imprecise enough to mislead the deliberation.

My §6.4 recommendation stands: spec 042 should rename, split, and disambiguate.

---

## 4. Did they miss implications of Claude Agent SDK being a CLI subprocess wrapper?

**Yes, in two places.** The advocate nowhere acknowledges that `claude-agent-sdk` is itself a subprocess wrapper. This is not a niche detail — it is the single most important fact about the advocate's v1 provider set.

### 4.1 The "zero new deps" table in §2.2 is misleading

The advocate writes:

| Provider | Adds to conversus core |
|---|---|
| `claude-code` | `claude-agent-sdk` OR subprocess (zero new deps) |

The "zero new deps" label is wrong two ways:

1. **`claude-agent-sdk` is a dep**. It is a PyPI package (`claude-agent-sdk`, Python ≥3.10, marked Alpha, currently 0.1.56 per my §1.1). Choosing it adds a runtime dependency on an alpha-status package that ships a platform-specific prebuilt CLI binary in its wheels. That is not zero — it is a dependency with an unusually large attack/compat surface (bundled binary, alpha status, tight coupling to Claude Code CLI version).
2. **"OR subprocess" still has a dep**: the system-installed `claude` CLI binary, which must be present and on PATH, at a compatible version. This is a hard runtime prerequisite that every CI environment / container / developer laptop must satisfy. It is not a Python package dep, but it is absolutely a deployment dep and should be represented in the table.

The advocate's framing makes `claude-code` look like free lunch. It is not. It is the single heaviest-dependency provider in the v1 set, regardless of which path (SDK vs raw subprocess) you take, because in both cases you are depending on a prebuilt CLI binary that Anthropic ships and updates out-of-band.

### 4.2 "A Node bridge" is a phantom option the spec also gets wrong

The advocate does not bring this up, but it matters for completeness. Spec 042 elsewhere references a "claude-code provider via Node bridge". My Round 1 §11 point 8 established that the TypeScript SDK `@anthropic-ai/claude-agent-sdk` is *also* a subprocess wrapper around the `claude` CLI binary. From Python, going through a Node layer to reach the TS SDK means: Python → Node → CLI subprocess. That is strictly worse than Python → CLI subprocess directly. The advocate's proposal to "ship `claude-code` as v1" should explicitly say "via direct CLI subprocess, not via Node bridge or TS SDK" — otherwise a future implementer may take the wrong path.

### 4.3 Cold-start economics are unmentioned

The advocate's §2.5 argues the `mock` provider stabilizes 3,428 tests. True. But nowhere in the review does the advocate discuss what happens when those 3,428 tests are exercised against the **real** `claude-code` provider during integration testing, or what happens in a production conversus run with 10–30 parallel agent phases:

- My §11 point 10: subprocess-spawning Claude Code has ~1–3s cold-start per invocation, cut (but not eliminated) by `--bare`.
- For 10 parallel phases × 5 rounds = 50 subprocess spawns per deliberation, that is ~50–150 seconds of pure process overhead under optimistic assumptions.
- An HTTP-server-based backbone (OpenCode, or a future A2A server that reuses a long-lived process) avoids this entirely by amortizing startup across the whole run.

This is not a disqualifying point for build-our-own — the advocate's protocol allows both subprocess and HTTP providers. But the v1 plan (`mock` + `anthropic` + `claude-code`) consists of two "fast" providers and one "subprocess cold-start per call" provider, and the implications for conversus's performance profile under spec 048's autonomous governance scenarios should be acknowledged in any "ship this in v1" pitch. The advocate does not acknowledge it.

---

## 5. Is the "v1: mock + anthropic + claude-code" plan realistic?

**Realistic, yes. Trivial, no. The advocate's framing oversells the ease of the `claude-code` provider specifically.**

Breakdown:

- **`mock`**: realistic and trivial. Pure Python. No disagreement.
- **`anthropic`**: realistic and moderate effort. Real SDK, clean async interface. Actual cost probably ~200–300 lines including retries, tool-use-free mode per spec 042 §4 lines 268–290, and `ExecutionResult` conversion.
- **`claude-code`**: realistic, but **this is where the project lives or dies**, and the advocate treats it as interchangeable with `anthropic` in effort. It is not. Per §2.3 of this cross-review, the realistic effort is ~400–800 lines and the dependency surface is larger than the table in their §2.2 admits.

A more honest v1 scope would be one of:

**Option A** (what the advocate is actually proposing, restated honestly):
> v1 = mock (100 LOC) + anthropic (200–300 LOC) + claude-code CLI subprocess adapter (400–800 LOC). Total ~700–1,200 LOC. Requires `claude` CLI binary on PATH at deployment. Per-call subprocess cold-start. `claude-agent-sdk` optional, does not reduce cost.

**Option B** (smaller, safer v1):
> v1 = mock + anthropic. Ship spec 042's protocol and two providers that are genuinely thin. Add `claude-code` as v1.1 once the subprocess concerns are designed through. This would unblock the blog pipeline and spec 048's Anthropic-API-based agents without taking on the subprocess-lifecycle complexity in the first release.

The advocate chose Option A. That is defensible — `claude-code` is the provider that preserves backward compatibility with the current SKILL.md flow, and my §11 point 1 notes that the current SKILL.md dispatch (`Agent` tool with `run_in_background`) is not portable and must be replaced by one of: (a) `claude -p --bare` subprocess, (b) `claude-agent-sdk.query()` subprocess, or (c) something else. If the v1 goal is "today's users see zero change" (advocate §2.4, FR-009/010/011), then `claude-code` has to be in v1.

But the advocate should concede that "today's users see zero change" is load-bearing on successfully building a full subprocess-lifecycle adapter in v1, not on a 100-line wrapper. The rhetorical ease of "it's just a thin adapter" papers over the one provider that has to actually work for the refactor to be invisible.

---

## 6. Claims the advocate made that I can independently verify

For the deliberation record, here are the claims in the advocate's review that my Round 1 research directly supports:

| Advocate claim | My finding | Verdict |
|---|---|---|
| "No library covers both model APIs AND agent runtimes" (§2.6, §3.1) | §7 table + §10 table | Verified |
| "LiteLLM has zero agent runtimes" (§3.3) | §7, §10 (LiteLLM is model-API only) | Verified |
| "A2A requires wrappers we'd have to write ourselves" (§3.4) | §9 (no A2A-wrapped coding agents exist as of 2026-04) | Verified |
| "MCP is the wrong layer for agent dispatch" (implicit throughout) | §8 | Verified |
| "Claude Code's dispatch primitive lives inside a Claude session" (implicit in §2.4's FR-011) | §1.4 | Verified — stronger than they stated |
| "The engine already doesn't care about the runtime" (§1) | I did not audit conversus engine code; cannot verify directly | Not independently verified by me |
| "100–200 lines per adapter" (§3.2) | §2.3 of this cross-review | **Partially incorrect** — holds for mock/anthropic, ~2x low for `claude-code` |
| "Spec 042's protocol is ACP-compatible as a superset" (§3.4) | §6 of Round 1, §3.2 of this cross-review | **Ambiguous** — depends on which ACP, and the two-protocol split must be acknowledged |
| "OpenCode has no agent runtimes or ACP provider path" (implied absence) | Not a claim the advocate made, but worth flagging: OpenCode has both `opencode serve` HTTP AND `opencode acp` stdio. My §2.2–2.3. | Advocate did not discuss OpenCode; not addressed in their v1. |

---

## 7. Claims the advocate made that I cannot verify from Round 1 (gaps)

These are not disputed, just not things I researched:

- "Conversus has 3,428 tests." I did not count them.
- "The engine's phase templates are already provider-agnostic markdown with {VARIABLE} placeholders." I did not audit conversus template code.
- "Conversus today has one dispatch call site: Agent(prompt=..., run_in_background=True) inside SKILL.md." This matches my reading of the SKILL.md-based dispatch model in Round 1, but I did not grep the conversus codebase to confirm it is literally one call site.
- "Spec 048 declares spec 042 a HARD DEPENDENCY." I did not read spec 048.
- "LiteLLM releases multiple times per month." I did not verify release cadence.
- "MCP Python SDK hit 1.0 on April 2, 2026, one day before this research was written." I did not verify this specific date.

I flag these as "advocate-provided, not researcher-verified" so other agents can rely on them at their own risk.

---

## 8. Overall evaluation

The advocate's **core structural argument is sound** and my Round 1 findings support it: there is no existing library with the right shape, every path requires writing adapters, and owning the Protocol avoids translation tax on a problem shape conversus already has. On the big question — "should conversus define its own `ExecutionProvider` Protocol?" — the advocate's answer is consistent with the facts I established.

The advocate's **secondary claims are uneven**:

- Cost estimate: ~2x low on the load-bearing provider (`claude-code`). Still small in absolute terms, but the framing "less than a Django admin class" is true only of the mock + anthropic slice, not the full v1 set.
- Dependency table: misleading on `claude-code` — "zero new deps" elides both the `claude-agent-sdk` alpha package dep and the system-binary dep.
- ACP/A2A superset: conflates two distinct protocols into one `acp` provider row, which my Round 1 §6 showed must be split. The build-our-own position actually *strengthens* when you acknowledge the split (because owning the Protocol is what lets you have two provider rows for two wire protocols), but the advocate's current framing obscures that and should be corrected.
- Performance implications of CLI-subprocess backbone: not mentioned. Should be mentioned because spec 048's autonomous-governance scenarios amplify the cold-start cost the advocate does not discuss.

**None of these corrections invalidate the build-our-own recommendation**. They adjust its cost, scope its claims more honestly, and force a clearer split in the provider matrix. A revised version of the advocate's review that (a) corrects the `claude-code` effort estimate, (b) fixes the dependency table, (c) splits `acp` into `a2a` and `jetbrains-acp` (or drops one and states which), and (d) acknowledges subprocess cold-start economics would be, in my judgment, factually correct and still arrive at the same recommendation.

As a researcher, I neither endorse nor oppose the build-our-own position. I verify that:
- The empirical claim it rests on (no library exists) is true.
- The cost model it uses is roughly right on two providers and roughly 2x low on the third.
- The "we contain them as providers" claim works for LiteLLM, works for A2A-with-caveats, and needs disambiguation for ACP.
- The v1 plan is realistic but carries more complexity in `claude-code` than the advocate acknowledges.

Other deliberation agents should argue against this position on dimensions other than "the library they're ignoring" — because that library does not exist — but may legitimately push on cost realism, dependency honesty, and the ACP/A2A disambiguation.

---

## 9. Relevant Round 1 sections

For anyone cross-referencing this cross-review to source facts:

- Round 1 §1 (Claude Code / Agent SDK subprocess architecture): `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/backbone-researcher/review.md` lines 27–95
- Round 1 §2 (OpenCode HTTP + ACP bridge): same file, lines 97–157
- Round 1 §6 (MCP vs A2A vs Zed/JetBrains ACP — the three-protocol tangle): same file, lines 252–293
- Round 1 §7 (shared primitive table): lines 295–307
- Round 1 §8 (MCP not the right layer): lines 311–320
- Round 1 §9 (A2A maturity): lines 324–334
- Round 1 §10 (per-tool mapping table): lines 338–354
- Round 1 §11 (neutral observations for deliberation): lines 358–380
