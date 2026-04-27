# Cross-Review: a2a-future-advocate

**Reviewer**: backbone-researcher
**Target**: a2a-future-advocate (Round 1, Phase 1)
**Date**: 2026-04-03
**Tone**: Factual, blunt. I am not here to adjudicate advocacy style — I am here to report where their claims diverge from what I was able to verify.

---

## 0. Summary

The advocate's position is built on three factual load-bearing claims, and **two of them do not survive my research**:

1. "A2A is the standard that has merged IBM ACP and Google A2A under the Linux Foundation" — **TRUE**, verified (my §6.2).
2. "The coding-agent ecosystem is A2A-native (or about to be), so conversus can plug into a living A2A mesh by shipping one `acp` provider" — **FALSE as of 2026-04**. No shipping coding agent has been wrapped as an A2A server by its vendor or by a third party I could locate (my §6.2, §9, §10).
3. "The advocate's use of 'ACP' unambiguously refers to A2A-the-merged-protocol" — **AMBIGUOUS and in places INCORRECT**. The advocate quotes spec 042 text that itself uses "ACP" and then references "JetBrains ACP" in the same argument as if they were the same ecosystem. They are two different protocols (my §6).

The advocate's **direction of travel** (A2A is the right long-term dispatch layer for agent-to-agent work) is defensible. Their **claim of imminent ecosystem arrival** is not. Their concrete plan (ship `conversus-acp-claude` as a reference A2A wrapper) is still technically viable, but only if they are honest that conversus will be doing the pioneer wrapping work itself with no counterparties on day one.

---

## 1. Did they conflate A2A with Zed/JetBrains Agent Client Protocol?

**Yes, in at least two places, and in a third they use the ambiguity of "ACP" to smuggle in evidence from the wrong protocol.**

### 1.1 Direct conflation — Section 4, "The CLI that runs outside your CLI" table

Advocate review line 210:

> "IDE plugins | Not supported | **Future (via JetBrains ACP from spec 042)**"

Advocate review line 211:

> "Every one of those surfaces is an A2A client in disguise. A GitHub Action wants to dispatch to an agent — that is a Task Request. A webhook wants to dispatch to an agent — that is a Task Request. An IDE plugin wants to dispatch to a coding agent — **JetBrains ACP is literally a protocol for this exact use case** (spec 042 §12 Q8 tracks it)."

This paragraph is where the conflation is most obvious. The advocate lists "JetBrains ACP" as one of the execution surfaces and then in the very next sentence calls **all of them** "A2A clients in disguise." That is incorrect. Per my §6.3:

- **JetBrains/Zed Agent Client Protocol** is a completely separate protocol from A2A.
- It lives at `agentclientprotocol.com` / `github.com/zed-industries/agent-client-protocol`.
- It is "LSP for AI agents" — IDE-to-local-agent JSON-RPC over stdio. Its threat model assumes a human-in-the-loop editor approving tool calls.
- It is **not** a member of the A2A family, not governed by Linux Foundation LF AI & Data, not using the A2A wire format, and has a separate TSC, separate SDKs (Rust/TS/Python/Kotlin/Java under the `@agentclientprotocol/*` namespace, not `a2a-sdk`).
- v0.11.4 as of March 2026, **not 1.0**.

So the advocate's argument "every execution surface is an A2A client in disguise" is factually wrong at the IDE row of the table. The IDE surface is an Agent-Client-Protocol surface, governed by a different organization, using a different wire format, with a different maturity status.

### 1.2 Thesis-level ambiguity — Section 1 and Section 2.3

Advocate review lines 13–14 (quoting spec 042):

> "ACP (Agent Communication Protocol) — IBM/Linux Foundation standard for agent-to-agent dispatch, merged with Google's A2A protocol (2025). ACP Task Requests map to conversus phase dispatch."

The advocate takes this spec-042 paragraph at face value and builds the entire thesis on the label "ACP" throughout the document — "the `acp` provider," "ship `conversus-acp-claude`," "the ACP ecosystem for free" — while simultaneously reaching for evidence from the Zed/JetBrains Agent Client Protocol ecosystem (see §1.1 above).

This is not a pedantic naming complaint. It is a real technical error with real consequences:

- If "ACP" in the advocate's document means **A2A-the-merged-protocol**, then their §2.3 ecosystem flywheel claim ("every SDK that ships an A2A endpoint becomes conversus-compatible") is currently empty — no shipping coding agent has an A2A endpoint.
- If "ACP" means **Zed/JetBrains Agent Client Protocol**, then there IS an ecosystem (Claude Code, Codex CLI, Copilot CLI, OpenCode, Gemini CLI are all in the Zed registry) — but that protocol is IDE-to-agent, not agent-to-agent, and does not satisfy spec 048's "autonomous governance" use case, which the advocate names as the load-bearing proof in their §4.

The advocate cannot have it both ways. The ecosystem they point at in their rhetoric lives under the **wrong protocol** for the use case they are arguing for.

Spec 042 itself is also guilty of this conflation — see my §6.4, which explicitly flags the naming as a correctness issue in the spec. The advocate inherited the bug from the spec and amplified it.

### 1.3 Section 5 — "Proposed Commitment"

Advocate review line 227:

> "Prioritize the `acp` provider.'"

Line 228:

> "Ship `conversus-acp-claude` as the reference A2A server wrapper for Claude Code (spec 042 §12 Q7)."

Line 229 (new):

> "`claude-code` direct provider ONLY as a fast-path optimization"

The advocate switches between "acp" and "A2A" within three adjacent bullets as if the two names were interchangeable. Given the real-world ambiguity of "ACP" in 2026-04, a reader acting on this plan has no way to tell whether the deliverable is an A2A server (HTTP JSON-RPC 2.0, `a2a-sdk`, Linux Foundation LF AI & Data) or an Agent Client Protocol server (stdio JSON-RPC, `@agentclientprotocol/sdk`, Zed Industries). These produce different binaries that talk to different clients.

**Cite for the file**: advocate's own review, lines 227–232, are unimplementable as written until the naming is disambiguated.

---

## 2. Did they claim the coding-agent ecosystem has A2A support when it doesn't?

**Yes. This is the single most damaging factual error in the advocate's position.**

### 2.1 The direct claim — Section 2.3

Advocate review lines 100–102:

> "- `conversus-provider-a2a` (single HTTP client, ~200 lines)
> - Each tool that speaks A2A is free — zero lines of conversus code
>
> Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships."

The empirical status of "Each tool that speaks A2A" and "every SDK that ships an A2A endpoint" as of 2026-04 is: **none of the tools conversus would dispatch to speaks A2A**, and **zero SDKs ship an A2A endpoint**.

From my §6.2:

> "Adoption: Framework integrations in Google ADK, LangGraph, BeeAI. No major agent SDK has shipped an A2A server wrapper for itself yet. No canonical reference implementation of 'wrap Claude Code as an A2A server' exists."

From my §9:

> "Ecosystem fact: As of 2026-04, there is no off-the-shelf A2A server that wraps any of the coding agents conversus would actually dispatch to. If conversus ships an A2A provider today, it will have nothing on the other end of the wire that speaks A2A natively — someone (probably conversus maintainers) has to build the wrapper."

My §10 provider table documents this row by row. The "A2A server?" column is "No" for Claude Code, OpenCode, Aider, GitHub Copilot CLI, OpenAI Codex CLI, Gemini CLI, Continue.dev, Cline, Cursor, Windsurf, and gh-aw.

The advocate's "zero lines of conversus code per tool" is true **only once conversus maintainers or someone else writes the A2A wrapper for each tool**. Until that work happens, the actual cost per tool is "the full wrapper, plus the A2A client." That is strictly more code than writing a subprocess adapter against the tool's CLI, which already exists and works today.

### 2.2 The rhetorical flourish — Section 2.3 flywheel

Advocate review line 102:

> "Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships. The wrapper is NOT conversus's problem — it is the SDK's problem, or it is a **reusable artifact** because wrapping Claude Code as an A2A server is valuable to every A2A client in the world, not just conversus. **We write it once, and Cursor, Zed, OpenCode, LangGraph, CrewAI, Haystack, Microsoft Agent Framework, and everyone else benefits.** That is the ecosystem flywheel."

This is the cleanest statement of the empty-ecosystem problem in the advocate's own words. Parse the sentence carefully:

- "Every SDK that ships an A2A endpoint" — zero such SDKs exist for coding agents.
- "The wrapper is NOT conversus's problem — it is the SDK's problem" — no SDK has treated it as their problem.
- "Cursor, Zed, OpenCode, LangGraph, CrewAI, Haystack, Microsoft Agent Framework, and everyone else benefits" — none of these projects has shipped an A2A server or an A2A client that would consume a conversus-authored wrapper.

The flywheel described here has no flywheel. The advocate is pointing at an A2A ecosystem diagram and describing the steady state ("we write it once, everyone benefits"), but the ecosystem is at step zero. Someone has to push the wheel first. The advocate does not name who. They imply it is already spinning.

### 2.3 The "already has adoption" argument — Section 2.1

Advocate review line 38:

> "Per `research/tool-landscape.md` §14 (A2A Protocol):
> - Launched by Google April 2025
> - IBM ACP **merged** in September 2025
> - Now governed by the **Linux Foundation**
> - Unified under the 'A2A' name
> - Python SDK available via the BeeAI framework"

The advocate's source here is the conversus team's own `tool-landscape.md`. I was unable to find any listed production adoptions in coding-agent tools beyond framework integrations (Google ADK, LangGraph, BeeAI). None of those framework integrations produces an A2A server wrapping Claude Code, Aider, Copilot CLI, Codex CLI, Gemini CLI, OpenCode, or Continue. The advocate's bullet list stops at "Python SDK available via the BeeAI framework" — notice it does not include "Claude Code wrapped as an A2A server" or "Copilot CLI wrapped as an A2A server" because those do not exist.

Note also: `a2a-sdk` on PyPI is 0.3.25 stable, 1.0.0a0 alpha. The advocate does not mention the version status in Section 2.6 where they assert "The Python SDK already exists." A 0.3.x stable release of a protocol SDK is a meaningful caveat that the advocate elides.

### 2.4 The "12 months of stabilization" claim — Section 2.3 rebuttals

Advocate review line 191:

> "'A2A is too new.' Launched April 2025, merged September 2025. We are in April 2026. That is **twelve months** of stabilization"

Verified facts from my §6.2 and §9:

- A2A **protocol v1.0.0** released 2026-03-12. **Less than a month old.**
- `a2a-sdk` Python **stable** is 0.3.25 (2026-03-10). **Also less than a month old at stable.**
- The merger happened August 2025 (not September) per the Linux Foundation announcement. Minor date error.

"Twelve months of stabilization" is the gap between first launch and today's calendar date, not the age of the shippable v1.0.0 artifact. The v1.0.0 artifact is three weeks old. That is the number that matters for a production bet. The advocate chose the longer number and called it stabilization time.

---

## 3. Does "one provider for all tools" survive the empty-ecosystem finding?

**Not as an immediate-term argument. It survives as a five-year bet.**

The advocate's pitch in §2.3 ("one provider, every tool") is the strongest *theoretical* case in their document. If A2A reaches the adoption it aspires to, then yes, a single `a2a` provider in conversus replaces the N×M adapter explosion. That is what standards convergence looks like when it works, and the comparison to Kubernetes/OCI/OpenTelemetry/gRPC in their §2.1 is a reasonable pattern to cite.

But "one provider, every tool" is an equilibrium statement. The advocate pitches it as a day-one deliverable:

> (line 102) "Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships."

In 2026-04 the conditional clause ("SDK that ships an A2A endpoint") is empty. So the day-one state of `conversus-provider-a2a` is: one provider, **zero** tools. Shipping it immediately makes conversus compatible with nothing that conversus users currently use.

This survives as an argument only if:

1. Conversus commits to writing the A2A wrappers for Claude Code, OpenCode, Aider, and Copilot themselves as reusable artifacts — which is real work (hundreds of lines per tool plus ops) and which the advocate's own plan names as "30 lines" (my response: their 30-line number is from a sketch in `tool-landscape.md` §Candidate B that is not a production server), or
2. Conversus bets that someone else will do the wrapping work in the next 12 months. This bet is currently unsupported by evidence — no vendor roadmap I could verify announces A2A support for a shipping coding agent.

**The "one provider, every tool" argument is good strategic direction but bad 2026-04 execution.** It becomes correct only after an A2A server ecosystem exists for coding agents. The advocate's error is treating the direction as if it were already the state.

---

## 4. Is their concrete plan (ship `acp` provider first, ship `conversus-acp-claude` wrapper) viable?

**Technically yes. Empirically it requires conversus to do pioneer work the advocate's own framing denies is needed.**

The advocate's §5 plan:

> (line 227) "Prioritize the `acp` provider. Build it first per spec 042 §11..."
> (line 228) "Ship `conversus-acp-claude` as the reference A2A server wrapper for Claude Code..."
> (line 229) "Implement the `claude-code` direct provider ONLY as a fast-path optimization..."
> (line 230) "Do NOT build bespoke providers for `copilot`, `gemini-cli`, `opencode`, `aider`, `gh-aw`, `langgraph`, `temporal`, `gsd`. Instead, write A2A server wrappers for each..."

This plan IS technically viable. Nothing in my findings says conversus cannot write A2A server wrappers for these tools. Three blunt observations:

### 4.1 The plan requires writing, not consuming

The advocate frames the A2A path as "we plug into the ecosystem." In reality the plan is **"we create the ecosystem for coding agents."** Those are very different projects:

- Plugging in = implement a client, connect to existing servers. Low risk, low cost.
- Creating = implement a client AND the first servers AND the reference implementations AND evangelize other vendors to adopt. High risk, high cost, high leverage if it works.

The conversus team should go in eyes open: this plan is the creation plan, not the consumption plan. The advocate's own document does not acknowledge this anywhere.

### 4.2 The 30-line wrapper claim is incorrect

Advocate review line 193 (rebuttal):

> "The research report's §Candidate B (lines ~698–724) gives us the exact wrapper pattern. Thirty lines of Python. Writing it as an A2A server is no harder than writing it as a bespoke adapter"

I did not verify that sketch directly, but from my §1 Claude Agent SDK findings, a production A2A server wrapping Claude Code has to do all of:

- Translate A2A Task Request → `ClaudeAgentOptions` + `query()` call, including mapping Task Request reference parts to `cwd`/allowed paths, metadata to options, and custom fields to tools.
- Stream Claude's `AssistantMessage`/`ToolUseBlock`/`ToolResultBlock` events back as A2A `session/update` equivalents over SSE.
- Handle subprocess lifecycle of the bundled `claude` binary (crashes, hangs, timeouts).
- Map `CLINotFoundError`/`CLIConnectionError`/`ProcessError`/`CLIJSONDecodeError` to A2A error responses.
- Handle auth (Anthropic API key passthrough, permission_mode).
- Handle cancellation (A2A cancel → terminate subprocess).
- Handle partial results on timeout.
- Handle multi-turn (sessions, resume via `agentId`).

That is not 30 lines. Thirty lines is a demo sketch. A production A2A server wrapping Claude Code is several hundred lines, and doing it RIGHT so it can be the reference implementation the rest of the ecosystem copies is more like a thousand lines plus tests and docs. The advocate's "no harder than a bespoke adapter" is true in order-of-magnitude terms (both are multi-hundred lines), but their "30 lines" quote undersells the cost of their own plan by ~10×.

### 4.3 The "direct provider as fast-path optimization" is backwards

Advocate review line 229:

> "Implement the `claude-code` direct provider ONLY as a fast-path optimization for users who do not want to run a local A2A server. It is a convenience, not an architectural pillar."

Given the empty ecosystem finding, the correct sentence is the inverse: the direct `claude-code` provider (via `claude -p --bare` or `claude-agent-sdk.query()`) is the **architectural pillar** for 2026, because it is the only path that works on a laptop today without requiring the user to run a local A2A server they do not have. The A2A server wrapper is the convenience for the day the ecosystem catches up.

The advocate has the priority inverted because their model assumes the A2A ecosystem exists and the direct adapter is a compatibility shim. In actual 2026-04, the direct adapter is the primary execution path and the A2A wrapper is the forward bet.

**Net assessment of the plan**: Viable but significantly more expensive than the advocate says, and with an inverted priority. If the conversus team wants to do pioneer work on the A2A-for-coding-agents ecosystem, this is a reasonable roadmap. If they want to ship execution providers for existing users in the spec-042 horizon, they need direct CLI-subprocess providers first and A2A wrappers second.

---

## 5. What parts of the position SURVIVE?

Several, and the advocate should regroup around them rather than defending the empty-ecosystem claim:

### 5.1 SURVIVES: A2A is the right long-term agent-dispatch protocol

The advocate is correct that MCP is the wrong layer (my §8), that the conversus phase-dispatch semantics match A2A Task Request semantics line for line (spec 042 §2, which I verified is a real isomorphism), and that Linux-Foundation-backed standards with Google + IBM + Microsoft + AWS + Cisco + Salesforce + ServiceNow + SAP on the TSC (my §9) historically win in the long run. This part of the argument is sound.

The correction to make: frame A2A as **where the industry is going** and position conversus to ride the wave, rather than framing it as **where the industry has arrived** and claiming conversus can plug in today.

### 5.2 SURVIVES: Writing an A2A server for Claude Code IS valuable as an ecosystem contribution

This is the strongest version of the advocate's position and I want to elevate it deliberately because they nearly state it correctly. **Given that no one has yet wrapped a major coding agent as an A2A server, conversus being the first to do so is a genuine ecosystem contribution that benefits every future A2A client, not just conversus.** The flywheel metaphor works if conversus is willing to push the wheel.

This reframe turns the weakness (no counterparties exist) into a strength (first mover with a reusable artifact). It just requires the advocate to admit that:

1. Conversus is the pioneer, not a late adopter.
2. The work is real (hundreds to low thousands of lines per tool wrapper) — not "30 lines."
3. The ROI accrues over 12–24 months as other A2A clients adopt the wrapper, not on day one.

That is a respectable bet. The advocate should make it plainly instead of claiming the ecosystem is already there.

### 5.3 SURVIVES: Runtime agent discovery via Agent Detail IS a real differentiator for spec 048

Advocate §2.2 on discoverability. This argument survives because it does not depend on any existing A2A servers for coding agents — it depends on A2A Agent Detail being the right abstraction for spec 048's `agent_registry` concept. Whether the advocate's `agent_registry` config becomes useful depends on whether conversus builds the wrappers (same dependency as §5.2), but the architectural claim — "discoverable URLs beat hardcoded Python class names" — is correct and not refuted by anything in my findings.

### 5.4 SURVIVES with caveats: Recursive composability

Advocate §2.4. The claim that "agents calling agents" is native to A2A and hard under bespoke adapters is accurate. The caveat is the same one as §5.2: it only becomes load-bearing after the A2A server ecosystem exists. For spec 048's 2026 timeline, the advocate would need to either (a) wait, or (b) build the first few A2A servers themselves to make the composability real.

### 5.5 DOES NOT SURVIVE: "Every future provider is A2A-native"

Advocate implicit and explicit throughout §2.3 and §5. This is the core aspirational claim that fails on empirical grounds. It is not that it is wrong in the limit — it is wrong **as a 2026-04 factual description** of the shipping ecosystem. The advocate should either drop this framing entirely or qualify it with a date: "We believe every future provider will be A2A-native by 2027–2028; in the interim conversus must ship the reference wrappers."

### 5.6 DOES NOT SURVIVE: Conflation of A2A and Agent Client Protocol

Already treated in §1 above. The advocate cannot use Zed/JetBrains ACP ecosystem facts as evidence for A2A ecosystem adoption. Fix the naming and the conflated evidence drops out.

### 5.7 DOES NOT SURVIVE: Specific attacks on the "hybrid" position

Advocate §3.2. Their attacks on the LiteLLM-hybrid approach are mostly rhetorical. In particular their claim that "the hybrid splits the abstraction in half" ignores that in 2026-04 the hybrid's Tier 1–2 bespoke adapters are the only way to dispatch to the actual shipping tools, because no A2A counterparty exists. The hybrid is not splitting the abstraction — it is choosing the only path that has endpoints on the other end. The advocate needs to either (a) prove the A2A counterparties exist (they cannot — see §2 above), or (b) accept that the hybrid is the correct 2026 answer and reframe their position as "A2A roadmap starting Q3 2026, hybrid for Q2."

---

## 6. Specific citations and corrections table

| Advocate claim | Location | My finding | Verdict |
|---|---|---|---|
| "ACP Task Requests map to conversus phase dispatch" | line 14 (quoting spec) | The mapping is real, but "ACP" here means A2A-the-merged-protocol, and the advocate uses "ACP" ambiguously throughout | Correct in isolation, misleading in context |
| "Python SDK available via the BeeAI framework" | line 44 | `a2a-sdk` on PyPI is the primary SDK (0.3.25 stable / 1.0.0a0 alpha, maintained by Google LLC). BeeAI is one framework that builds on it. Calling BeeAI "the Python SDK" overstates BeeAI's centrality. | Partially incorrect |
| "Each tool that speaks A2A is free — zero lines of conversus code" | line 101 | Zero tools currently speak A2A | Hypothetical framed as present tense |
| "Every SDK that ships an A2A endpoint... becomes conversus-compatible the day it ships" | line 102 | True in principle, but no SDK ships an A2A endpoint in 2026-04 | Hypothetical framed as present tense |
| "We write it once, and Cursor, Zed, OpenCode, LangGraph, CrewAI, Haystack, Microsoft Agent Framework, and everyone else benefits" | line 102 | None of the listed projects has a shipping A2A client that would consume a conversus-authored wrapper. Zed's editor integration uses Agent Client Protocol, not A2A. | Mixes A2A and ACP ecosystems |
| "trivially yes, from day one" (multi-provider routing via A2A) | line 116 | True AFTER A2A servers for each tool exist. Day one = zero tools speak A2A = no routing. | Hypothetical framed as present tense |
| "Under A2A, the arbiter says 'dispatch Task Request to `agent://cve-lookup`'" | line 124 | Requires an existing `agent://cve-lookup` A2A server. None currently exists for CVE lookup. | Hypothetical framed as present tense |
| "IBM ACP merged in September 2025" | line 40 | Merger was announced August 2025 (LFAI blog, 2025-08-29) | Minor factual error |
| "twelve months of stabilization" | line 191 | Protocol v1.0.0 released 2026-03-12. Three weeks old at stable. | Misleading framing — counts from first launch, not from stable |
| "Thirty lines of Python" for A2A server wrapper | line 193 | A production A2A server wrapping Claude Code is several hundred lines. Thirty is a demo sketch. | Undersells cost of own plan ~10× |
| "JetBrains ACP is literally a protocol for this exact use case" (IDE dispatch as A2A client) | line 211 | JetBrains ACP is not an A2A protocol. Different org, different wire format, different maturity, different use case. | Direct factual conflation |
| "ecosystem still immature (2026, early adoption)" is "dated" | line 191 | Still accurate in 2026-04. | Incorrect — advocate dismisses a caveat that still holds |

---

## 7. Recommended position for the advocate to defend in revision

If I were in their chair and wanted to salvage the position without overclaiming, I would rewrite to:

1. **Drop all present-tense claims about an A2A coding-agent ecosystem.** Replace with explicit future-tense claims and dates.
2. **Explicitly disambiguate A2A from Agent Client Protocol** everywhere. Rename the provider from `acp` to `a2a`. If JetBrains/Zed ACP is in scope, treat it as a second, separate provider (`agent-client-protocol`) with a different use case.
3. **Own the pioneer framing.** "Conversus will write the first A2A server wrappers for Claude Code and OpenCode as reusable open-source artifacts. This is pioneer work that benefits the broader ecosystem starting in 2027."
4. **Correct the cost estimates.** Per-tool A2A wrapper is several hundred lines, not thirty. Budget accordingly.
5. **Accept the hybrid for 2026.** Direct CLI-subprocess providers for Claude Code / Aider / Copilot / Codex / Gemini CLI as the 2026-Q2 baseline. A2A wrapper work begins in 2026-Q3 as a parallel initiative. Full A2A-primary architecture targets 2027.
6. **Keep the long-term architectural argument.** A2A as the right dispatch protocol for agent-to-agent work is correct. MCP as the wrong layer is correct. Runtime discovery via Agent Detail for spec 048 is a real benefit. These parts do not need to be defended against my findings.

That is a revised position I would find credible. The current position is not.

---

## 8. One-paragraph cross-review summary

The advocate's architectural direction — A2A as the correct long-term agent-dispatch protocol, MCP as the wrong layer, discoverable agents beating hardcoded registries — is sound and survives my findings. Their factual framing does not. They conflate Google/IBM/Linux-Foundation A2A with the Zed/JetBrains Agent Client Protocol at least twice (most clearly at lines 210–211), they claim a coding-agent A2A ecosystem that does not exist in 2026-04 (lines 101–102), they undersell the cost of their own wrapper plan by an order of magnitude (line 193: "thirty lines"), and they dismiss an ecosystem-maturity caveat ("ecosystem still immature") that remains accurate given a2a-sdk is 0.3.25 stable and protocol v1.0.0 is three weeks old. The plan to ship `conversus-acp-claude` is technically viable but requires conversus to act as the pioneer building the first A2A server wrappers for shipping coding agents — a role the advocate's own framing implies is unnecessary because "the community" will do it, when in fact no community effort to do it exists. Revise to: keep the long-term architectural claim, drop the present-tense ecosystem claims, disambiguate A2A from Agent Client Protocol everywhere, accept a 2026 hybrid baseline with A2A wrapper work starting Q3, and own the pioneer framing honestly.
