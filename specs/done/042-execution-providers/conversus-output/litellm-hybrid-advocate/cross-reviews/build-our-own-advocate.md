# Cross-Review: LiteLLM-Hybrid Advocate vs. Build-Our-Own Advocate

**Reviewer**: LiteLLM-Hybrid Advocate
**Target**: Build-Our-Own Advocate's review
**Phase**: Round 1 Phase 2 — Cross-review
**Date**: 2026-04-03

---

## 0. Headline finding

I went into this cross-review expecting a fight. After reading the build-our-own position carefully against the backbone-researcher's ground truth, I have to concede something important: **the build-our-own advocate and I are, in substance, proposing the same architecture**. We disagree about framing, emphasis, and one factual claim about LiteLLM's coverage. We do not actually disagree about what code gets written in week 1.

Both positions agree:

1. The `ExecutionProvider` protocol in spec 042 §3 should be conversus-owned code, not imported from a framework. (My review §4.1; their §2.1.)
2. The engine should not bend to LiteLLM's — or anyone else's — shape. (My review §4; their §2.1.)
3. A `mock` + `anthropic` + `claude-code` set is the v1 target. (My week-1 plan §8 essentially maps to their v1 proposal §6.)
4. `claude-code`, `aider`, `opencode` are written as native adapters because LiteLLM does not cover them. (My §4.2; their §3.3.)
5. A2A is a future phase, not a blocker. (My §5.2; their §3.4.)

The one place we differ is whether a `LiteLLMProvider` appears in **v1** (my position) or in **v2+, if at all** (their position). That is an emphasis argument, not an architectural argument. I will make the case below that v1 is the right answer, but I am going to stop pretending we're in a different paradigm.

---

## 1. Is the "superset" framing correct?

**Yes, it is correct, and this is the most important finding in this cross-review.**

From their §5 (verbatim, lines 203–208):

> "The other two options are **strict subsets** of build-our-own:
> - Build-our-own can include a `LiteLLMProvider` adapter whenever we decide LiteLLM is worth the dep (it's a 100-line wrapper). Nothing in this proposal prohibits that.
> - Build-our-own can include an `ACPProvider` the moment A2A's Python SDK matures."

That is true. And it exposes something I should acknowledge about my own review. When I titled my position "LiteLLM-hybrid," I implied the protocol came from LiteLLM or was shaped around LiteLLM. It is not. My week-1 proposal (my §8) says explicitly: *"Implement `ExecutionProvider`, `ExecutionTask`, `ExecutionResult` per spec 042 §3 — **conversus code, not LiteLLM**."* That is word-for-word the build-our-own position.

What I actually advocate is: **build-our-own protocol + LiteLLMProvider as one of the first concrete implementations**. The build-our-own advocate advocates: **build-our-own protocol + `anthropic`/`openai` SDK providers as the first concrete implementations, with a `LiteLLMProvider` available if we later decide we want it**.

Both are "build our own protocol." The only disagreement is which concrete provider ships first under the protocol for Tier 3 workloads. That is a week-1-vs-week-2 argument, not a paradigm war.

**I concede the superset framing.** My position can be more honestly restated as: *"Build our own protocol, and make `LiteLLMProvider` the default Tier-3 implementation in v1 so we get 100+ providers on day 1 instead of 2."* That's a narrower, more defensible claim, and it doesn't pretend to be a different architecture.

---

## 2. Is "100–200 lines per adapter" realistic?

The build-our-own advocate cites the research report's own estimate of 100–200 lines per adapter (their §3.2, citing tool-landscape.md line 757). Let me check that against the backbone-researcher's findings.

The backbone-researcher documents what an adapter actually has to do:

**For subprocess-based agent runtimes (§1.2, §3.3, §10)**: `subprocess.run(["claude", "-p", prompt, "--bare", "--output-format", "json", ...])`, then parse JSON output. That's genuinely short — probably 80–150 lines once you handle:
- Prompt construction
- Flag assembly (`--allowedTools`, `--settings`, `--mcp-config`, `--agents`, `--append-system-prompt`, `--resume`)
- JSON output parsing (both `json` and `stream-json` formats)
- Error class mapping (`CLINotFoundError`, `CLIConnectionError`, `ProcessError`, `CLIJSONDecodeError`)
- Async subprocess via `asyncio.create_subprocess_exec`
- Timeout handling
- Working directory (`cwd`) and env var passthrough
- Exit-code → `ExecutionResult.success` mapping
- Cost tracking (which for CLI-subprocess providers is a separate call or post-hoc estimation since the CLI doesn't uniformly return cost metadata)

**For direct-API Tier-3 providers (the contested surface)**: The research-authored LiteLLM adapter sketch is ~14 lines (`tool-landscape.md` lines 613–633). Writing the same coverage without LiteLLM means, per provider:
- Auth + client construction
- Message envelope construction (OpenAI format vs Anthropic `messages` vs Gemini `contents` vs Bedrock `InvokeModel`)
- Response parsing (`choices[0].message.content` vs `content[0].text` vs `candidates[0].content.parts[0].text`)
- Tool-use path (if `supports_tool_use=True` — see spec 042 §4 lines 268–290)
- Token-usage → cost calculation (requires a price table per model, maintained by us)
- Rate-limit parsing (per-provider headers)
- Retry + backoff (async, with jitter, per-error-class decisions)
- Streaming path (SSE for OpenAI/Anthropic, differently for Bedrock/Vertex)
- Error taxonomy (mapping provider errors to a shared exception hierarchy)

I think **200 lines per Tier-3 adapter is optimistic** once you handle retries, cost tracking, streaming, and a unified error surface. Realistic range: 250–400 lines each, plus a shared base class to factor common logic. For 3 providers (anthropic, openai, gemini) that's 750–1,200 lines, plus a price table we have to keep current as providers change prices.

For subprocess-based providers (`claude-code`, `aider`, `opencode` via CLI), the 100–200 estimate is realistic — maybe 150–250 each with the full flag surface and async subprocess plumbing.

**Where I land**: The build-our-own advocate's estimate is reasonable for the subprocess adapters (which we both write identically) but optimistic for the direct-API Tier-3 adapters (which my position outsources to LiteLLM). This is not a decisive objection to their position — 1,200 lines is not a lot of code by absolute measure — but it is directionally wrong to collapse "thin subprocess wrapper" and "full SDK client" into the same 100–200 line estimate. The former is true; the latter is not.

That said, the numbers here are not the point. Even 1,200 lines for three direct-API providers is a tractable engineering effort. The real question is **ongoing maintenance cost**: cost-table drift, SDK version drift, new-model onboarding, streaming format changes, rate-limit header changes. Those are what make LiteLLM valuable — not the initial 1,200 lines, but the ongoing treadmill it absorbs.

---

## 3. Is the "3 of 12 providers" attack on LiteLLM fair?

**No. This is the weakest move in the build-our-own review and it deserves a direct correction.**

They write (their §3.3):

> "LiteLLM solves one of the three tiers in spec 042 §4 (the Tier 3 direct-model-API case). That is 3 of our 12 targeted providers in the matrix at §11 (lines 497–512): `anthropic`, `openai`, and arguably future `gemini`."

Let me check this against spec 042 §11 and the backbone-researcher's findings.

The backbone-researcher's ground truth (§7 and §10) and the tool-landscape research both confirm LiteLLM covers **100+ providers** including: OpenAI, Anthropic, Azure OpenAI, Google (Gemini/Vertex AI), Mistral, Ollama, Bedrock, Groq, Together, Fireworks, xAI, DeepSeek, Cohere, Hugging Face, VLLM, LMStudio, Perplexity, Replicate, and more.

Spec 042 §11's 12-provider matrix includes the Tier-3 direct-API providers (`anthropic`, `openai`, `gemini`, plus local runtimes like `ollama`, `vllm`) and the Tier-1 agent runtimes (`claude-code`, `aider`, `opencode`, `copilot`, `gemini-cli`) and the workflow orchestrators (`gh-aw`, `langgraph`, `temporal`). LiteLLM covers **every Tier-3 entry in that matrix**, not "3 of 12."

The build-our-own advocate's framing counts 12 matrix rows and says LiteLLM hits 3. But:

1. **Ollama and VLLM are in the matrix and LiteLLM covers both.** That's 5, not 3.
2. **The matrix is not a list of equal-weighted providers.** Tier-3 providers are things users configure by name (`anthropic`, `openai`, `gemini`). Each Tier-3 entry in the matrix represents "the direct-API path to that model family." LiteLLM covers all of them plus a long tail the matrix doesn't enumerate. When a user asks "does conversus support Groq?" or "does conversus support DeepSeek?", the answer under the hybrid path is *yes, today, via the LiteLLM provider*. Under build-our-own it is *not until we write another adapter and maintain its price table*.
3. **More importantly**, LiteLLM's value proposition isn't "N providers in the matrix" — it's "a unified interface that absorbs the long tail so conversus never has to write a Groq adapter, a DeepSeek adapter, a Fireworks adapter, etc." The matrix undercounts by design: it only lists the providers conversus has thought to enumerate. The real set of providers conversus users will ask for is unbounded. LiteLLM's job is to absorb that unbounded set. Build-our-own's job under that framing is to absorb it one adapter at a time.

**The "3 of 12" framing is factually wrong** (undercounts what's actually in the matrix) **and strategically wrong** (misses the point that LiteLLM's value is long-tail absorption, not matrix cell count). This is the one place I think the build-our-own review overstates its case.

That said, I want to be fair: even correcting this, LiteLLM does not cover agent runtimes, and the build-our-own advocate's underlying point — that conversus still has to write every Tier-1 adapter itself — is correct. LiteLLM is not a complete solution. It is a solution for a distinct sub-problem (direct-API model calls) that happens to be a large sub-problem with a huge long tail.

---

## 4. Does the attack on my 70/30 split hold up?

My review's opening claim was: "Spec 042 is ~30% an agent-runtime problem and ~70% a model-API problem, and LiteLLM has already solved the 70%."

The build-our-own advocate doesn't attack this as a percentage, but their §3.3 implicitly challenges it by arguing that the blog pipeline (spec 042 §6) — the motivating use case — *needs* agents that can read files and produce structured markdown, which is a Tier-1 concern. If the motivating use case is 100% Tier-1, then my 70/30 split is wrong about where the value lives even if it's right about where the lines-of-code live.

The backbone-researcher's findings are relevant here. §1 (Claude Code) makes clear that the blog-pipeline use case requires agent-runtime dispatch (subprocess `claude -p --bare` or equivalent) because the agent needs to read files, run tools, and write output. That is **not** a LiteLLM workload. LiteLLM cannot run the blog pipeline. A `LiteLLMProvider` in conversus serves a different purpose: it powers phase dispatch for Tier-3-compatible workloads (summarization, classification, extraction, small verification checks) where the phase doesn't need tools.

**Honest assessment of my 70/30 split**:

- If you count **lines of code LiteLLM saves us**, the 70% figure is plausible — LiteLLM absorbs a lot of SDK glue.
- If you count **lines of code in conversus's critical path for the motivating use case (blog pipeline)**, the figure is closer to 0% — LiteLLM doesn't run agents, and the blog pipeline is an agent workload.
- If you count **conversus's eventual user base**, the split probably lands somewhere in between. Some users want conversus as a phase-dispatch engine for Tier-3 LLM calls (fast, cheap, no tools). Other users want conversus as a deliberation orchestrator over agent runtimes. LiteLLM helps the first population, not the second.

The build-our-own advocate is **right to challenge the 70/30 framing** to the extent it implies "LiteLLM is 70% of the work." It isn't. LiteLLM is 70% of the *provider implementation effort for the Tier-3 sub-problem*, which is itself a fraction of the total problem. I was imprecise.

**Revised framing**: LiteLLM is the best available implementation for the Tier-3 sub-problem, which is one of three sub-problems spec 042 addresses. The other two (Tier-1 agent runtimes and Tier-2 orchestrators) are ours to build. The build-our-own advocate is correct that the Tier-1 work is the load-bearing work for the blog pipeline and spec 048. My argument is still that outsourcing the Tier-3 sub-problem to LiteLLM is correct — but it is a narrower argument than "LiteLLM solves 70% of spec 042."

---

## 5. Can I reframe my position to absorb their critique?

Yes, and I think I should.

**Original framing**: "LiteLLM Hybrid — delegate the model-API layer to LiteLLM, build native adapters only for agent runtimes."

**Revised framing**: "Build our own `ExecutionProvider` protocol (as spec 042 §3 specifies), and make `LiteLLMProvider` the first concrete implementation for direct-API Tier-3 workloads. Write subprocess-based adapters for Tier-1 agent runtimes (`claude-code`, `opencode`, `aider`) natively. A2A is a future phase-3 provider."

Under the revised framing, my position is **identical** to the build-our-own position in every respect except one: **which concrete Tier-3 provider ships in v1**. Build-our-own says: start with `AnthropicProvider` and `OpenAIProvider` as native SDK adapters, add `LiteLLMProvider` later if we decide it's worth the dependency. I say: start with `LiteLLMProvider` as the Tier-3 default because it gives us 100+ providers on day 1 for ~14 lines of code, and we can always add native `AnthropicProvider` later if we want to drop the dependency.

Both paths converge. The protocol is identical. The Tier-1 adapters are identical. The architecture is identical. The only difference is a single adapter file: `litellm_provider.py` (my path, ~14 lines, pulls in LiteLLM) vs. `anthropic_provider.py` + `openai_provider.py` (their path, ~500–800 lines combined, no framework dependency, per-provider price tables).

### Why I still prefer v1-with-LiteLLM

1. **Day-1 provider coverage**: 100+ providers vs. 2. That's a qualitative leap in what conversus can pitch to users on ship day.
2. **Cost tracking for free**: LiteLLM returns cost metadata per call (spec 042 open question #3 answered by the adapter for free).
3. **Long-tail absorption**: We never get asked "does conversus support X?" and have to write another adapter. The answer is "if LiteLLM supports X, yes, today."
4. **Optional dependency**: Per spec 042 §10 (line 487), provider implementations ship as optional packages — `conversus-provider-litellm` is opt-in, not core. So the "every user pays the LiteLLM dependency" concern (build-our-own §2.2) is not quite accurate: only users who install the LiteLLM provider pay it. Users who only want `mock` + `claude-code` don't touch LiteLLM.

### Why their v1-without-LiteLLM is also defensible

1. **Zero framework dependency**: Clean, auditable, no transitive surface.
2. **No bet on LiteLLM's release cadence or security posture**: Though LiteLLM's posture is actually fine per the research (41k stars, PYSEC-2026-2 patched, Stripe/OpenAI production usage).
3. **Control over cost-table accuracy**: We own the price table and can correct LiteLLM's known pricing lag.
4. **Forces us to build the shared adapter base class** that makes future providers faster to add.

### The honest conclusion

**Both paths are correct and the disagreement is small.** We could literally ship the build-our-own v1 (mock + anthropic-native + claude-code) in week 2, add `LiteLLMProvider` as a `conversus-provider-litellm` package in week 3, and have the union of both positions. That is, in fact, what I would propose if I were synthesizing these two reviews.

---

## 6. Is my position actually in conflict with theirs?

**No. After careful reading, there is no architectural conflict.** There is a packaging/ordering disagreement about one provider file.

The conflicts are:

| Claim | My position | Their position | Resolvable? |
|---|---|---|---|
| Protocol shape | Build our own per spec 042 §3 | Build our own per spec 042 §3 | **Agreement** |
| Tier-1 adapters (`claude-code`, `aider`, `opencode`) | Native subprocess adapters | Native subprocess adapters | **Agreement** |
| A2A | Phase 3, future | Phase 3, future | **Agreement** |
| Tier-3 v1 default | `LiteLLMProvider` (~14 lines, 100+ providers) | `AnthropicProvider` + `OpenAIProvider` (native, 2 providers) | **Minor disagreement** |
| `LiteLLMProvider` existence | In v1 | Allowed but not v1 | **Minor disagreement** |
| `mock` provider | Ships in core | Ships in core | **Agreement** |
| Ownership of `ExecutionResult` shape | Conversus | Conversus | **Agreement** |
| Lines-per-adapter estimate | 250–400 for direct-API, 150–250 for subprocess | 100–200 across the board | **Minor factual disagreement** |
| LiteLLM provider coverage | 100+ | "3 of 12" | **Factual error on their side; correcting** |

**The only substantive disagreement is: should `LiteLLMProvider` exist in v1?** My answer is yes because it's ~14 lines for 100+ providers. Their answer is not-necessary because we can write native adapters instead. Both answers are defensible. Neither disqualifies the other's architecture.

---

## 7. What the build-our-own advocate got right that I should credit

Several things in their review are stronger than I gave them credit for in my own write-up:

1. **The protocol-ownership argument (their §2.1) is correct.** Conversus phases have a specific shape (`prompt`, `read_paths`, `output_path`, `metadata`) that does not map cleanly to any existing framework's abstraction. Owning this shape is the right call, and my review agrees with this in §4.1 — I just buried it.

2. **The "single call site" refactor argument (their §2.4) is correct.** Conversus today dispatches through one place in SKILL.md. Refactoring to a protocol is cheap because the coupling is minimal. This is a point in favor of the build-our-own path being fast, which I underweighted.

3. **The `mock` provider for 3,428 tests argument (their §2.5) is strong.** A protocol-owned mock is strictly better than any framework-delegated alternative for testing, and this is a real conversus-specific benefit that LiteLLM cannot provide. I did not emphasize this enough.

4. **The "no wheel exists" argument (their §3.1) is correct.** There is no library whose API matches spec 042 §3. LiteLLM is not a wheel for this — it's a wheel for a different (sub-)problem. Calling the protocol "wheel reinvention" would be wrong, and I would never make that claim; neither would any honest hybrid advocate.

5. **The forward-compatibility argument (their §2.3) is correct.** Owning the protocol means the ecosystem can churn (AutoGen → Microsoft Agent Framework, A2A/ACP merge, etc.) without breaking conversus. This is genuinely valuable and applies under both positions.

---

## 8. What I'd want them to concede in return

If this were a true cross-review rather than a winner-take-all, I'd ask them to concede:

1. **The "3 of 12 providers" claim is wrong.** LiteLLM covers 100+ providers including every Tier-3 entry in the spec 042 §11 matrix plus a long tail. The correct critique is "LiteLLM covers zero Tier-1 providers," which is true and sufficient — they don't need the matrix undercount to make their point.

2. **The "100–200 lines per adapter" estimate is optimistic for direct-API providers.** Realistic is 250–400 lines each once you handle retries, cost tracking, streaming, and unified error taxonomy. This matters because ongoing maintenance cost (cost-table drift, SDK drift, new-model onboarding) is where LiteLLM's value actually lives — not in the initial line count.

3. **`LiteLLMProvider` as an optional adapter is not a framework commitment.** Per spec 042 §10 line 487, provider implementations are optional packages. Users who don't install `conversus-provider-litellm` never touch LiteLLM. The concern about "every user on the LiteLLM treadmill" (their §2.2) is not quite right — it's every user *of that optional package*.

4. **The day-1 provider coverage argument matters strategically.** Users compare conversus against tools that already use LiteLLM (Aider, OpenCode, etc.). Shipping with 2 providers instead of 100+ is a losing pitch, even if both paths have the same architecture.

---

## 9. Proposed synthesis for the arbiter

If the arbiter in phase 5 is looking for a unified recommendation that both positions can sign onto, I would propose:

**Week 1**: Ship `ExecutionProvider` protocol, `ExecutionTask`, `ExecutionResult`, `PROVIDER_REGISTRY`, and `mock` provider per spec 042 §3. Both positions agree on this verbatim.

**Week 2**: Ship `claude-code` provider as a subprocess adapter over `claude -p --bare --output-format json` per backbone-researcher §1.2 (83). Both positions agree.

**Week 3**: Ship **two** Tier-3 providers as optional packages:
- `conversus-provider-litellm` (~14 lines, pulls in LiteLLM, covers 100+ providers including anthropic, openai, gemini, ollama, etc.)
- `conversus-provider-anthropic` (~300 lines, native `anthropic` SDK, no framework dependency, for users who want zero transitive surface)

Users pick whichever fits their constraints. The protocol accepts both. Conversus's core has zero framework dependency. The Tier-3 sub-problem is solved by both paths simultaneously, and neither camp has to lose.

**Phase 2 (post-042)**: `opencode` (HTTP via httpx against OpenAPI 3.1 per backbone-researcher §2), `aider` (subprocess), `copilot` (subprocess), `gemini-cli` (subprocess).

**Phase 3 (~6 months)**: `a2a` provider when A2A Python SDK goes 1.0 stable and at least one of Claude Code / Aider / OpenCode ships an A2A server wrapper (currently none do per backbone-researcher §9).

This synthesis takes both positions seriously. The architecture is 100% build-our-own. The v1 provider set is a superset of both proposals. The maintenance question (who owns Tier-3 price tables and SDK drift?) is answered by letting users choose.

---

## 10. Summary

**The build-our-own advocate is right about the architecture**: build the protocol ourselves, own the shape, write native adapters, keep the core framework-free. I agree and I should have framed my position that way from the start.

**I am right about LiteLLM's coverage**: it is 100+ providers, not 3 of 12, and that long-tail absorption has real value even if it is not a complete solution to spec 042.

**The disagreement is narrow**: one provider file, week 1 vs. week 3, optional package vs. never. Not an architectural war.

**The honest conclusion**: my position is better named **"build our own protocol + LiteLLMProvider as a v1 optional package"** than "LiteLLM hybrid." Under that naming, the build-our-own advocate's "superset" framing is correct and the two positions collapse into nearly the same plan. The remaining disagreement is about ordering and packaging, which can be resolved by shipping both in v1 as optional packages and letting users choose.

If this is a winner-take-all vote, I'd vote for the build-our-own position as stated — with the explicit understanding that it does not preclude a `LiteLLMProvider` adapter landing in the same week. If the game allows nuance, I'd vote for the synthesis in §9.

**The build-our-own advocate wrote a better review than I did** on the protocol-ownership question, and I'm willing to say so on the record.

---

**End of cross-review.**
