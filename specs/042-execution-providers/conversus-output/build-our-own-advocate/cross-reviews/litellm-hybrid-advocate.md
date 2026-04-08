# Cross-Review: LiteLLM-Hybrid Advocate

**Reviewer**: build-our-own-advocate
**Target**: litellm-hybrid-advocate/review.md
**Round**: 1, Phase 2 (Cross-review)
**Date**: 2026-04-03

---

## 0. Posture

The hybrid advocate makes a genuinely strong case and I want to concede the parts that are right before attacking the parts that are wrong. The concessions are not rhetorical — they change my own Phase-3 revision. Specifically:

- **LiteLLM is the right implementation for Tier 3 direct-model-API calls.** I agree. I said so in my own review (§3.3, line 165): *"build-our-own does not prohibit using LiteLLM inside a `LiteLLMProvider` adapter."*
- **A `LiteLLMProvider` adapter should be in the v1 provider set**, not deferred. I'll expand on this in §5 below.
- **The model-API tier genuinely is commodity work**, and paying twelve SDK upgrade cycles instead of one LiteLLM upgrade cycle is real operational cost that my review underweighted.

Where the hybrid advocate is wrong is in the framing — specifically the 70/30 split, the 144-cell surface area, and the "you're spending expensive hours on undifferentiated work" opportunity-cost argument. The backbone researcher's facts, which neither of us had during Phase 1, decisively tilt the framing toward build-our-own. I'll walk through each objection with the new evidence.

---

## 1. The 70/30 split collapses under the researcher's findings

The hybrid advocate's core framing (review §1): *"Spec 042 is ~30% an agent-runtime problem and ~70% a model-API problem."*

This is the load-bearing claim. Everything else — the opportunity cost, the "commodity glue" framing, the 3-week vs 4–6 week timeline — derives from it. **It does not survive the backbone researcher's findings.**

The researcher establishes (§0 TL;DR, §1.2, §10, §11.2) that **every production agentic coding tool conversus wants to dispatch to is, at the wire level, a subprocess-spawn-a-CLI dispatch model**. Specifically:

- **Claude Code**: `claude-agent-sdk` is itself a thin wrapper that spawns the `claude` CLI binary as a subprocess and speaks JSON-RPC over stdio (researcher §1.2). There is **no direct-to-API mode**. The SDK IS a subprocess wrapper. Even the TS SDK exposes a `spawnClaudeCodeProcess` hook.
- **Aider**: CLI is the primary interface; Python API is explicitly unsupported (researcher §3.2).
- **OpenCode**: HTTP is real, but there's no Python SDK (researcher §2.1).
- **Copilot CLI, Codex CLI, Gemini CLI, Continue's `cn`**: CLI subprocess, no public Python SDK (researcher §10).
- **Cursor, Windsurf, Cline**: no programmatic surface at all (researcher §5).

Now look at spec 042's provider matrix (§11, lines 497–512): 12 providers. Of those, **how many are pure model APIs that LiteLLM covers?** Let me enumerate from spec 042 itself and the researcher's findings:

| Provider | Type | LiteLLM covers? | Notes |
|---|---|---|---|
| `mock` | Testing | No | We own this |
| `anthropic` | Direct API | **Yes** | Tier 3 model API |
| `openai` | Direct API | **Yes** | Tier 3 model API |
| `gemini` | Direct API | **Yes** | Tier 3 model API |
| `claude-code` | Agent runtime | **No** | Subprocess CLI (researcher §1) |
| `opencode` | Agent runtime | **No** | HTTP server (researcher §2) |
| `aider` | Agent runtime | **No** | Subprocess CLI (researcher §3) |
| `copilot` | Agent runtime | **No** | Subprocess CLI (researcher §10) |
| `gemini-cli` | Agent runtime | **No** | Subprocess CLI (researcher §10) |
| `gh-aw` | Workflow compiler | **No** | Emits Actions YAML (researcher §4) |
| `langgraph` | Framework | **No** | In-process framework |
| `a2a` / `acp` | Wire protocol | **No** | HTTP JSON-RPC (researcher §6.2) |

**That's 3 of 12 providers LiteLLM helps with, and 9 of 12 where conversus writes the adapter regardless.**

The hybrid advocate's 70/30 split does not describe spec 042's provider matrix. It describes a different spec — one where the goal is "talk to every model API in existence." Spec 042's actual goal, stated in §1 and §6, is **headless execution of conversus phases**, and the blog pipeline, and spec 048 governance. Those use cases live almost entirely in the agent-runtime half of the matrix. Tier 3 direct-model-API is a *supporting* tier for cases where a full agent runtime is overkill — not the main event.

So the correct framing is not "70% model API, 30% agent runtime." The correct framing is: **25% model API (3 providers LiteLLM helps with), 75% agent runtime or other (9 providers we write either way).** LiteLLM is helpful for a quarter of the matrix, not two-thirds.

The hybrid advocate's entire strategic argument hinges on getting this ratio wrong in their favor. With the researcher's findings, the ratio flips, and with it the "we're outsourcing the bulk of the work" framing. We are not outsourcing the bulk of the work. We are outsourcing a helpful but bounded slice.

---

## 2. The 144-cell surface area is overcounted

The hybrid advocate's most visually persuasive argument is the table in §3: **12 concerns × 12 providers = 144 cells of bespoke code we supposedly avoid**. The table lists things like "request envelope", "response parsing", "streaming", "function-calling format", "rate limit handling", "retry semantics", "cost calculation", "error taxonomy", "context window limits", "SDK version drift".

This argument is doing a lot of rhetorical work with an illusion. Let me decompose it:

### 2.1 LiteLLM only touches the model-API column, not the agent-runtime column

Look at what "response parsing" means for each provider type:

- For `anthropic` (Tier 3 model API): parsing `{"content": [{"type": "text", "text": "..."}]}`. LiteLLM normalizes this. Real concern, real solution.
- For `claude-code` (Tier 1 agent runtime): parsing the stream-json output of `claude -p --output-format stream-json`. LiteLLM has **literally nothing to say about this**. It's a completely different wire format (JSON-RPC lines over stdio from a subprocess), and LiteLLM does not handle subprocess dispatch at all.
- For `opencode` (Tier 1 agent runtime): parsing the SessionPromptParamsPartUnion response shape from OpenCode's OpenAPI. LiteLLM does not cover this.

The hybrid advocate's table silently assumes every cell in the "response parsing" row is the same shape of work. It isn't. The Tier-3 cells are format-normalization work (LiteLLM's domain). The Tier-1 cells are subprocess / HTTP-server / IPC work (nobody's domain but ours). Conflating them inflates the count.

Let me redraw the table honestly. For each row in the hybrid advocate's §3 table, how many of the 12 providers does LiteLLM *actually* help with?

| Concern | Hybrid claim | LiteLLM actually helps | Real reduction |
|---|---|---|---|
| Client construction + auth | 12 | 3 (Tier 3 only) | 9/12 unchanged |
| Request envelope | 12 | 3 | 9/12 unchanged |
| Response parsing | 12 | 3 | 9/12 unchanged |
| Streaming | 12 | 3 | 9/12 unchanged |
| Function-calling format | 12 | 3 | 9/12 unchanged |
| Rate limit handling | 12 | 3 | 9/12 unchanged |
| Retry semantics | 12 | 3 | 9/12 unchanged |
| Cost calculation | 12 | 3 | 9/12 unchanged |
| Error taxonomy | 12 | 3 | 9/12 unchanged |
| Context window limits | 12 | 3 | 9/12 unchanged |
| SDK version drift | 12 | 3 | 9/12 unchanged |

**True reduction: 33 cells of 144, or 23%.** Not 100%, not 70%, not "most of the work." Roughly a quarter.

And even that 23% overstates it, because several of those "concerns" don't exist for agent runtimes at all:

- **Function-calling format** is meaningless for a subprocess CLI — the agent runtime has its own tool loop; conversus doesn't define the tool schema.
- **Context window limits** are the agent's problem, not conversus's — we hand it a prompt and files, it manages its own window.
- **Retry semantics** for a subprocess are "did it exit 0?" — no provider-specific header parsing.
- **Cost calculation** for `claude-code` comes from the CLI's own `--output-format json` metadata, not from LiteLLM.

So the real number of cells where LiteLLM genuinely eliminates bespoke work is closer to **20–25 cells out of 144, or ~15%**. That is useful. It is not "we don't have to write 144 cells." The hybrid's most striking visual argument is 6x overcounted.

### 2.2 The agent-runtime adapters are the same under all three positions

The hybrid advocate concedes this in their own §4: *"Tier 1 agent-runtime providers: claude-code, opencode, aider (and later copilot, gemini-cli). LiteLLM does not cover these... these are our job. And they're the same job under any of the three approaches."*

This is a critical concession. It means the 9/12 providers LiteLLM does not help with are a constant cost across all three positions. The only delta between hybrid and build-our-own is **how we implement the Tier 3 adapter** — either we wrap LiteLLM (14 lines) or we wrap the direct SDKs (14 lines × 3 SDKs = ~42 lines).

The delta between "build our own provider for anthropic + openai + gemini" and "build a LiteLLMProvider that covers all three" is maybe 50–100 lines of adapter code and one dependency. That is the real scope of the disagreement. Not 144 cells. Not 70% of the work. **About 50 lines and one transitive dependency.**

I'll concede in §5 that LiteLLM wins that 50-line trade. But let's be honest about the scope.

---

## 3. "Your 'superset' framing is academic" — not fair, here's why

The hybrid advocate doesn't explicitly attack my superset framing, but the implicit attack is in their §9 closing: *"Build-our-own... is the position of someone who prefers owning problems to solving them."* The charge is that build-our-own is academic purism dressed up as architecture — "own the abstraction" is a nice slogan but ships nothing.

That charge would be fair if owning the abstraction were *additional* work. **It isn't.** Here's the key fact the hybrid advocate glosses over: **the hybrid approach builds the exact same protocol I'm proposing.**

Read the hybrid's own §8 implementation checklist, Week 1:

> "Implement `ExecutionProvider`, `ExecutionTask`, `ExecutionResult` per spec 042 §3 — **conversus code, not LiteLLM**."
> "Implement `PROVIDER_REGISTRY` and `get_provider()` — **conversus code**."

That is **my proposal**. Verbatim. Spec 042 §3 is build-our-own. The hybrid advocate is proposing build-our-own **plus** a specific first implementation that wraps LiteLLM. Which is fine — that is the thing they're actually adding on top. But the **abstraction layer** is identical. We're both building spec 042 §3. The disagreement is purely about which provider ships in the first week.

So when the hybrid advocate writes (§9): *"Build-our-own fails 'fastest to ship,' 'lowest risk,' and 'provider coverage on day 1.' It is the position of someone who prefers owning problems to solving them"* — they are describing a straw man. Build-our-own *is* the protocol. The hybrid approach *is* the protocol + LiteLLM as one of the first concrete providers. Those are not opposing positions; they are nested positions.

The "superset" framing in my §5 was pointing at exactly this: *"The other two options are **strict subsets** of build-our-own."* The hybrid advocate never rebuts this. They can't, because it's true — their Week 1 deliverable is "our protocol" + "our registry" + "an adapter we wrote" (which happens to wrap LiteLLM). Every line of that except the LiteLLM call itself is build-our-own code.

The genuinely contested question is **not** "build the protocol vs. outsource it to LiteLLM." The genuinely contested question is "in the v1 provider set, should we ship `LiteLLMProvider` or three native SDK providers (`anthropic`, `openai`, `gemini`)?" That's a 50-line decision, and it's tactical, not architectural.

The superset framing is not academic. It is the literal, line-for-line truth of what the hybrid advocate proposes. Their own §8 proves it.

---

## 4. The opportunity-cost argument is backwards

The hybrid advocate's §7 is the most strategically aggressive part of their review: *"Every hour spent reinventing what LiteLLM already does is an hour not spent on..."* followed by a list of spec 048 deliverables.

This framing has two problems.

### 4.1 The hours being traded are tiny and non-substitutable

Per the hybrid's own §8, the LiteLLM integration is **14 lines of Python**. Writing three native provider adapters (`anthropic`, `openai`, `gemini`) using their official SDKs — which are all well-documented and async-native in 2026 — is plausibly 100–150 lines each, so 300–450 lines total.

The delta is **~300 lines of adapter code**. At conversus's current pace, that is one to two days of focused work, not "engineering weeks" (hybrid §1). The hybrid advocate's rhetoric ("spending engineering weeks rewriting what LiteLLM already does would be malpractice") is overheated for a 300-line delta.

And even granting the time delta: are those specific 1–2 days substitutable for work on spec 048's auto-grounding arbiter? No. Writing a provider adapter and writing META_DISPUTE handling are different people's work, different parts of the codebase, and different skill gradients. The opportunity-cost accounting only holds if engineer-hours are a fungible pool. In practice they aren't; the person best-suited to write an anthropic SDK wrapper is probably not the person best-suited to design override semantics.

### 4.2 The protocol IS the foundation; everything else builds on it

More importantly: the opportunity-cost frame mischaracterizes what build-our-own is doing. The hybrid advocate writes (§7): *"build-our-own... spends the most expensive engineering hours on the least differentiated work."*

**The most expensive engineering hours in spec 042 are the protocol design hours, not the adapter hours.** The `ExecutionProvider` protocol, the `ExecutionTask` / `ExecutionResult` data classes, the registry, the tool-use adaptation logic (pre-read files, post-write output), the backward-compat guarantees (FR-009/FR-010/FR-011), the deterministic path rules — **all of that is build-our-own work**, and **all of that is also hybrid work**, because the hybrid ships the same protocol.

The provider adapters — Tier 1, Tier 2, Tier 3 — are the *cheap* part of the work. They're 100–200 lines each. They come after the hard thinking is done. Framing the cheap part as "the expensive engineering hours" and the hard part as "already solved" inverts the actual cost structure.

The protocol is the foundation everything else builds on. Spec 048 (autonomous governance), the blog pipeline, the `conversus governance` CLI, the exit-code stability contracts — every one of those depends on the protocol being right. If we get the protocol wrong because we shaped it to fit LiteLLM's `completion_async()` signature, every downstream spec inherits that mismatch. The expensive work is the protocol, and **we do that work under both positions**. The only thing LiteLLM offers is a slight shortcut on the cheapest layer.

So the opportunity cost, correctly framed, is: **"Do we spend 1–2 days writing native Anthropic/OpenAI/Gemini adapters and own three fewer transitive dependencies, or do we save those 1–2 days and inherit LiteLLM's upgrade cadence and security surface forever?"** That is a legitimate trade. It is not "hours of commodity glue vs. hours on spec 048."

---

## 5. Concession: `LiteLLMProvider` should be in the v1 provider set

Here is where the hybrid advocate's case is genuinely strong and I'm updating my position.

My Phase 1 review recommended shipping `mock` + `anthropic` + `claude-code` as v1. On reflection, driven by the researcher's findings and the hybrid advocate's arguments, **I think `litellm` should join `anthropic` in the v1 provider set**. Specifically:

- **v1 providers**: `mock`, `claude-code`, `anthropic`, `litellm`
- **v2 providers**: `opencode`, `openai` (direct, as a second Tier-3 option), `aider`
- **v3 providers**: `a2a`, `gh-aw`, `copilot`, `gemini-cli`

Why add `litellm` to v1:

1. **Breadth without commitment.** A single `LiteLLMProvider` adapter gives conversus users access to 100+ models on day 1 without conversus having to write or maintain any of them. The researcher confirms LiteLLM's maturity (41.9k stars, Stripe/OpenAI production use, MIT license, stable API). That breadth is a genuine user-facing win my Phase 1 position underweighted.

2. **The adapter is genuinely small and isolated.** Per the research sketch cited by the hybrid advocate (§2), the adapter is ~14 lines. The blast radius of LiteLLM going sideways is contained to that one file — the protocol, the registry, the engine, the tests, and every other provider are completely insulated. This is the correct use of an external dependency: gated behind our own abstraction, in one place, easily replaceable.

3. **It does not commit us to the hybrid split.** Shipping `LiteLLMProvider` alongside a direct `anthropic` provider means users can choose. Those who want a lean dependency footprint install `conversus-provider-anthropic` and nothing else. Those who want the 100-provider buffet install `conversus-provider-litellm`. Both coexist because the protocol accepts either. This is the **build-our-own** outcome, with LiteLLM as **one of** the concrete first implementations, not **the** first implementation to the exclusion of others.

4. **The researcher didn't give me enough to reject this.** My Phase 1 review leaned on "LiteLLM doesn't cover agent runtimes" (true) to argue LiteLLM shouldn't define the shape of the dispatch layer (still true, and both positions agree on that now). But the researcher's confirmation that LiteLLM is stable, actively maintained, security-disciplined, and covers exactly the Tier-3 slice cleanly means there's no principled reason to *refuse* to ship a `LiteLLMProvider` adapter alongside `anthropic`. Refusing would be dogmatic, not pragmatic.

What I still refuse to concede:

- **LiteLLM should not be a required dependency of `conversus` core.** It must remain an optional provider package (`conversus-provider-litellm`), per spec 042 §10 (line 487). Users who want `mock` + `anthropic` + `claude-code` get zero LiteLLM footprint. The hybrid advocate's Week 1 plan is ambiguous on this — I want it explicit.
- **The `anthropic` native adapter should also ship in v1.** Not as a purist gesture, but because it's the reference implementation that proves direct-SDK providers work under the protocol, it's needed for the `supports_tool_use=False` tool-use adaptation path to be exercised (spec 042 §4 lines 268–290), and it gives users a LiteLLM-free option on day 1. The hybrid advocate would apparently skip it in favor of "anthropic via LiteLLM" — that's one provider too few.
- **The protocol, registry, data classes, tool-use adaptation, and backward-compat guarantees are all conversus-owned code that has to be written regardless.** On this the hybrid and build-our-own agree in substance but the hybrid's framing obscures it. My final position will make this explicit.

---

## 6. Summary of conceded ground

In the Phase 3 revision I will:

1. **Add `litellm` to the v1 provider set.** Alongside `mock`, `anthropic`, and `claude-code`. Ship it as `conversus-provider-litellm`, optional install.
2. **Explicitly call out LiteLLM's operational-cost advantage for Tier 3.** One upgrade cycle for 100+ models beats twelve upgrade cycles for twelve SDKs. This is a real win and I should have named it in Phase 1.
3. **Recharacterize the provider matrix** to make clear that Tier 3 (direct model APIs) is ~25% of spec 042's target providers, not 70%, and that `LiteLLMProvider` is the recommended default for that tier.
4. **Keep the 9/12 agent-runtime adapters as native build-our-own code** because LiteLLM does not help there (both reviews agree, researcher confirms).
5. **Keep the protocol, registry, and backward-compat guarantees as conversus-owned** — both positions already agree.

---

## 7. Summary of ground not conceded

1. **The 70/30 split is wrong.** The real ratio is ~25/75 in favor of agent-runtime work that conversus writes under any approach. The researcher's findings on Claude Code, Aider, OpenCode, Copilot CLI, Codex CLI, Gemini CLI, and Continue settle this.
2. **The 144-cell surface area is ~6x overcounted.** LiteLLM genuinely eliminates ~20–25 cells of bespoke code, not 144. The hybrid advocate's table conflates "model-API row × 12 providers" with "model-API row × 3 providers that are actually model APIs".
3. **The superset framing is not academic.** Both positions ship spec 042 §3 verbatim. The only disagreement is which concrete adapter is in the first week's deliverable, and even there both approaches are mutually compatible.
4. **The opportunity-cost argument is backwards.** The expensive engineering work is the protocol design and tool-use adaptation, which both positions must do. The cheap part is the 300 lines of direct-SDK adapters we'd skip. Framing those 300 lines as "the hours that delay spec 048" is not credible.
5. **"Build-our-own is the position of someone who prefers owning problems to solving them"** — this is rhetoric, not argument. The thing being "owned" is a ~40-line Protocol that the hybrid advocate also proposes to write. Owning the abstraction is not the same as owning the implementation of 144 cells, and the hybrid advocate equivocates between the two.

---

## 8. The revised position in one sentence

**Build our own `ExecutionProvider` protocol (spec 042 §3), ship `mock` + `claude-code` + `anthropic` + `litellm` as the v1 provider set, and treat `LiteLLMProvider` as the recommended default for Tier 3 direct-model-API use cases — while keeping native adapters for the 9/12 providers where LiteLLM offers nothing.**

This absorbs the hybrid advocate's strongest argument (LiteLLM is mature, the Tier-3 slice is commodity work, 14-line adapters are cheap leverage) without accepting their weakest (that the protocol should bend to LiteLLM's shape, that agent-runtime work is a minority of spec 042, or that build-our-own and hybrid are opposing rather than nested positions).

---

**End of cross-review.**
