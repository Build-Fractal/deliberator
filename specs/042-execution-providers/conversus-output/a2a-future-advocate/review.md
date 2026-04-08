# A2A/ACP as the Dispatch Protocol — Advocacy Review

**Advocate**: a2a-future-advocate
**Round**: 1, Phase 1
**Position**: Conversus should bet on A2A (Agent-to-Agent Protocol, merged with IBM ACP under Linux Foundation, Aug 2025) as the canonical dispatch layer. Build the `acp` provider first. Every other adapter is technical debt.
**Target**: spec 042 (execution-providers), with spec 048 (autonomous-governance-mode) as the load-bearing use case

---

## 1. The Thesis

Spec 042 already names the right protocol. Read §2 of the spec. The Protocol Alignment header is not incidental decoration:

> "ACP (Agent Communication Protocol) — IBM/Linux Foundation standard for agent-to-agent dispatch, merged with Google's A2A protocol (2025). ACP Task Requests map to conversus phase dispatch."

The spec author looked at the dispatch problem and saw that it is already solved by a standard. The ACP Mapping table in spec 042 §2 is a line-by-line isomorphism:

| Conversus Concept | A2A/ACP Concept |
|---|---|
| Filled phase template | Task Request message (text/markdown part) |
| `read_paths` | Task Request reference parts |
| `output_path` | Task Request metadata |
| Phase metadata | Task Request custom fields |
| Background execution | Async task with streaming |
| `execute_batch()` | Concurrent Task Requests |

This is not a near miss. It is the protocol we would have designed if Google, IBM, and the Linux Foundation had not already designed it for us. **The only question is whether we build our own bespoke adapter zoo and eventually throw it away, or we target the standard now and save ourselves the migration.**

I argue: target the standard now. Build the `acp` provider FIRST and treat every direct SDK adapter as either (a) a temporary bridge for SDKs that do not yet speak A2A, or (b) an A2A-server wrapper that we also ship.

---

## 2. Six Arguments for Betting on A2A

### 2.1 Standards convergence is already decided

Per `research/tool-landscape.md` §14 (A2A Protocol):

- Launched by Google April 2025
- IBM ACP **merged** in September 2025
- Now governed by the **Linux Foundation**
- Unified under the "A2A" name
- Python SDK available via the BeeAI framework

Let me name what that means in platform-strategy terms. Google + IBM + Linux Foundation is the exact pattern that produced every standard we currently rely on — Kubernetes (Google/CNCF), OpenTelemetry (Google/CNCF), gRPC (Google), OCI (Docker/Linux Foundation). This is the coalition that wins standards wars. When this set of backers agrees, the standard wins. Betting against A2A at this point is betting against the platform trend. We do not have a better protocol. We do not have a larger coalition. We do not have a differentiated reason to fork.

Spec 042 already acknowledges this in §11: "Priority — universal provider." The author gave A2A the top row of the provider matrix for a reason.

### 2.2 Runtime discovery kills the hardcoded provider list

The research report describes Agent Detail metadata:

> "Agents self-describe via **Agent Detail** metadata (capabilities, supported input types, etc.). The conversus engine can discover available agents at runtime rather than hard-coding provider lists."

Consider what this enables for spec 048 (autonomous-governance-mode). Today's `.conversusrc` hardcodes an `executor:` field and a `default_agents:` list. Read spec 048 §3.1:

```yaml
executor:
  provider: claude-code-headless
default_agents:
  - preset: security-reviewer
  - preset: architecture-reviewer
  - preset: maintainability-reviewer
```

That is a list of strings the user has to know about. **With A2A, the config becomes**:

```yaml
agent_registry:
  - https://agents.internal/security-reviewer
  - https://agents.internal/architecture-reviewer
  - https://marketplace.a2a.org/owasp-reviewer/v2
```

Or even just a registry URL that the engine queries for agents advertising `capability: security-review`. The governance gate becomes **extensible without a conversus release**. Teams add a custom agent, stand it up behind an A2A endpoint, register it, and the next nightly audit picks it up automatically. The build-our-own camp cannot offer that without reinventing service discovery.

This is not a hypothetical. Spec 048 FR-011 requires target resolution via `{changed_files}`, globs, and explicit paths. Spec 048 §10 Q4 asks about multi-repo governance. Spec 048 §14 names spec 020 (scenario storage) as a downstream consumer. **Every one of those features is easier when agents are discoverable objects with a URL instead of hardcoded Python classes in a `PROVIDER_REGISTRY` dict.**

### 2.3 One provider, every tool — the cross-tool interop dividend

Consider the N×M problem the other advocates are about to hand us. Here is N (conversus) × M (agent runtimes) under the build-our-own and LiteLLM-hybrid approaches:

- `conversus-provider-claude-code` (subprocess)
- `conversus-provider-aider` (subprocess)
- `conversus-provider-opencode` (REST)
- `conversus-provider-copilot` (JSON-RPC CLI)
- `conversus-provider-gemini-cli` (subprocess)
- `conversus-provider-cursor` (???)
- `conversus-provider-gh-aw` (workflow dispatch)
- `conversus-provider-langgraph` (StateGraph)
- `conversus-provider-temporal` (workflow activity)
- `conversus-provider-gsd` (GSD executor)
- (future new tools — repeat forever)

That is ten adapters that each need: auth handling, error mapping, cost tracking, cancellation, timeout, subprocess lifecycle, dependency pinning, CI coverage, version-skew handling, and maintenance across SDK upgrades. **We are talking 300–800 lines each plus ongoing maintenance.** The research report estimates ~500 lines per SDK wrapper (§Candidate B). Times ten, plus bit rot.

Under A2A, the math changes:

- `conversus-provider-a2a` (single HTTP client, ~200 lines)
- Each tool that speaks A2A is free — zero lines of conversus code

Every SDK that ships an A2A endpoint (or that the community wraps once as an A2A server) becomes conversus-compatible the day it ships. The wrapper is NOT conversus's problem — it is the SDK's problem, or it is a **reusable artifact** because wrapping Claude Code as an A2A server is valuable to every A2A client in the world, not just conversus. **We write it once, and Cursor, Zed, OpenCode, LangGraph, CrewAI, Haystack, Microsoft Agent Framework, and everyone else benefits.** That is the ecosystem flywheel.

Spec 042 §11 says this explicitly in the Implementation strategy note:

> "Build the `acp` provider first as the universal adapter. Then wrap individual SDKs as ACP servers — one wrapper per SDK, reusable across any ACP client (not just conversus)."

That is the correct order of operations. The spec already knows it.

### 2.4 Composability — recursive deliberation is free

Spec 042 §12 Open Question 5 asks:

> "Can a single run use multiple providers (e.g., `claude-code` for Phase 1-4, `anthropic` for Phase 5)?"

The bespoke answer: "Not in v1." Because per-phase routing means the engine has to know about heterogeneous dispatch, maintain per-phase provider state, handle per-phase auth, and serialize per-phase cost. It is genuinely hard under a bespoke abstraction.

The A2A answer: **trivially yes, from day one**. Every agent is a URL. Different phases route to different URLs. The engine does not care. More importantly, **agents can invoke other agents**. A conversus synthesis agent can call an OWASP-security-research agent which calls a CVE-lookup agent — without conversus knowing those sub-invocations happened. The call graph is recursive because A2A is compositional by construction.

For spec 048 (autonomous governance), this is load-bearing. Imagine a constitution rule:

> "Any change to authentication code must cite a current CVE search."

Under bespoke adapters, the arbiter either has no way to trigger a CVE search or has to be hardcoded with a CVE-search tool. Under A2A, the arbiter says "dispatch Task Request to `agent://cve-lookup`" as part of its ruling workflow, and the governance deliberation can reach out to the broader agent ecosystem without conversus being a middleman. **Composability is not a nice-to-have for governance-mode conversus — it is how the mode becomes useful beyond a single repo.**

### 2.5 Future-proofing — every bespoke adapter is technical debt that A2A retires

Let me be blunt about what the LiteLLM-hybrid advocate is about to propose. The research report has already scripted it in §Candidate C (Hybrid, 95% fit). The proposal will be:

1. LiteLLM for Tier 3 (direct model APIs)
2. Direct SDK providers for Tier 1–2 (Claude Code, Aider, OpenCode)
3. A2A "later, when it matures"

That reads as pragmatic. It IS pragmatic — for 2025. But here is what it hides:

- **Every direct SDK provider we build in 2026 is a line item we will rip out in 2027.** The research report admits this: it calls A2A the "long-term ideal" and "the future path." Code written against a deprecating abstraction is technical debt the day it ships.
- **LiteLLM is a Tier 3-only solution.** It does not touch the agent-runtime dispatch problem. So the hybrid approach is really "build our own for the hard part, use LiteLLM for the easy part." The hard part is the part A2A actually solves.
- **We will do the migration anyway.** The research report's §Candidate C explicitly says "Phase 3 (Future, ~6 months): Implement A2A protocol support." Six months of writing code that is scheduled to be replaced is not pragmatism — it is hedging that costs more than committing.

The research report's own risk matrix rates "A2A standard changes" as **Low likelihood / Medium impact**. That is the same risk profile as "LiteLLM supply chain incident" (Low/High) — except A2A is a Linux Foundation standard, not a single vendor's package. A standards change takes years and happens in the open. A supply chain incident happens on a Tuesday.

### 2.6 The Python SDK already exists

Research §14: **BeeAI Framework** — official Python/TypeScript SDK for building A2A agents:

- `@agent` decorator to mark functions as A2A-compliant
- Custom tools as A2A agent capabilities
- Full asyncio-native

The research report also gives us the A2A provider integration sketch (§Candidate B, lines ~660–720 of `tool-landscape.md`). It is about 30 lines of Python using stdlib + `httpx`. No new framework. No vendor lock-in. Just HTTP with a defined envelope.

Let me quote the dependency footprint from the research:

> "Dependency Footprint: No new dependencies; standard `httpx` for HTTP client"

Compare that to the LiteLLM-hybrid dependency footprint:

> "`pip install litellm`" + each bespoke SDK provider's own dependency tree

LiteLLM alone has security advisories (PYSEC-2026-2, patched March 2026 per the research). Every direct SDK provider has its own version skew and auth handling. **The A2A path has the smallest blast radius and the smallest surface area for supply chain risk.**

---

## 3. Attacks on the Competing Positions

### 3.1 Against "Build Our Own"

The build-our-own advocate will argue for maximum control: "We define the ExecutionProvider protocol, we ship one or two reference providers, we own every abstraction."

This is the 100%-fit illusion from the tradeoff matrix (research §Part 3). The 100% is computed against today's requirements. The moment a new requirement lands — a new SDK, a new orchestrator, a new governance-mode agent registry — the fit drops and the build-our-own camp has to ship code. **A2A fit is 85% today and climbing; build-our-own fit is 100% today and dropping.** Over any time horizon longer than six months, the lines cross.

Specific attacks:

- **The N×M explosion**: Every new SDK = a new conversus release, a new pip package, new tests, new CI, new docs. Ten adapters at 500 lines each is the baseline. The research report names this number and it is not cheap.
- **No discovery story**: Build-our-own has a `PROVIDER_REGISTRY` dict. That dict lives inside the conversus package. Third parties cannot extend it without forking or entry-point shenanigans (which spec 042 §5 punts to post-032 packaging). A2A makes discovery an HTTP concern that lives outside the conversus process entirely.
- **Reinvents wheels we already see rolling**: The build-our-own advocate will have to reinvent: async task envelopes (A2A has them), streaming (A2A has it), agent metadata (A2A has Agent Detail), capability negotiation (A2A has it), and eventually service discovery (A2A has it via Agent Detail). Every one of those is a standard we are choosing to abandon.
- **"Control" is a euphemism for "our problem forever"**: Owning the abstraction means owning every bug in every adapter. Shared standards mean shared bug surfaces with shared fixes.

### 3.2 Against "LiteLLM-Hybrid"

The hybrid advocate will argue: "LiteLLM for model APIs, direct SDK providers for agents, A2A as future work." This is the research report's own recommendation (§Part 4). It sounds safe. Here is why it is actually the worst of both worlds:

- **It splits the abstraction in half.** Tier 3 goes through LiteLLM; Tier 1–2 goes through bespoke adapters; A2A is deferred. Conversus now has to maintain THREE mental models: LiteLLM's `completion_async`, the ExecutionProvider protocol for direct SDKs, and (eventually) A2A. That is more surface area than just committing to A2A.
- **Tier 3 vs Tier 1–2 is a false partition.** The research report itself says (§Candidate C) that A2A can wrap Tier 3 providers too — any model API can be fronted by an A2A server. So the LiteLLM piece is optional scaffolding that A2A subsumes. We are building scaffolding we will remove.
- **The "future work" is never done.** Every software project has deferred work that never ships. "Phase 3 (Future, ~6 months)" is how spec 042 becomes spec 042 + spec 065 + spec 092. By the time we actually implement A2A, we will have accumulated three layers of hybrid debt and the migration will be harder, not easier.
- **"LiteLLM is proven" is an argument from authority, not architecture.** LiteLLM is proven for what it does (unified model API). It is not proven for agent dispatch because it does not do agent dispatch. Spec 042's problem is agent dispatch (the engine already has a `ModelProvider` for raw completions — the hybrid advocate's "new" LiteLLM wrapper is a rename of what exists). **The hybrid approach contributes nothing we do not already have on the Tier 3 side, and it ducks the hard problem on the Tier 1–2 side.**
- **The 95% fit number is a mirage.** It is computed by adding three approaches together. You cannot just sum fit scores — you pay integration overhead for each layer. Real fit of the hybrid is "95% features, 150% maintenance."

### 3.3 Rebuttals to the standard A2A counter-arguments

**"A2A is too new."** Launched April 2025, merged September 2025. We are in April 2026. That is **twelve months** of stabilization, including the IBM/Linux Foundation merger. Spec 048 (autonomous-governance-mode) is drafted on 2026-04-04 and depends on spec 042 which is drafted on 2026-04-02. Spec 042 will not ship "instantly" — by the time it lands, A2A will be 14–18 months old. The research report's §14 limitation ("ecosystem still immature (2026, early adoption)") is dated. By the time we are feature-complete, it is out of date.

**"Claude Code doesn't speak A2A yet."** Correct. And that is why the `claude-code` direct provider exists in spec 042 §4 as a **reference implementation**. I am not arguing we delete it. I am arguing it should be built as an A2A server wrapper from day one — `conversus-acp-claude` in spec 042 §12 Q7 — so that the same code serves (a) the direct-SDK bridge for local interactive use, and (b) the A2A-server mode for every other A2A client in the world. The research report's §Candidate B (lines ~698–724) gives us the exact wrapper pattern. Thirty lines of Python. **Writing it as an A2A server is no harder than writing it as a bespoke adapter**, and the output is reusable beyond conversus.

**"Ecosystem immaturity."** The research report itself rates A2A at **85% fit** versus LiteLLM at 70%. That is 15 points of pure ecosystem value the hybrid approach is throwing away. Ecosystem maturity grows monotonically; we are arguing about whether to enter on day 400 of A2A's existence or day 600. There is no version of this where entering later is cheaper than entering now.

---

## 4. Spec 048 as the Proof Case

Spec 048 is not a hypothetical. It is drafted. It exists. It declares spec 042 a HARD DEPENDENCY (§9 Constraints). Read spec 048 §11, "The CLI that runs outside your CLI":

| Surface | Today | With Spec 048 |
|---|---|---|
| CI (GitHub Actions) | Not supported | **Primary** |
| Git hooks | Not supported | Supported |
| Cron / scheduled | Not supported | Supported |
| Webhooks | Not supported | **Supported (via execution providers)** |
| IDE plugins | Not supported | **Future (via JetBrains ACP from spec 042)** |

Every one of those surfaces is an A2A client in disguise. A GitHub Action wants to dispatch to an agent — that is a Task Request. A webhook wants to dispatch to an agent — that is a Task Request. An IDE plugin wants to dispatch to a coding agent — **JetBrains ACP is literally a protocol for this exact use case** (spec 042 §12 Q8 tracks it).

Under A2A, spec 048's execution surfaces ARE A2A clients. Under bespoke, every surface re-learns dispatch.

And spec 048 §6.1 shows the GitHub Actions workflow template. Each step calls `conversus governance --gate pr`. Where does that invocation dispatch to? If conversus is an A2A client, the governance binary POSTs to a registry of agent URLs declared in `.conversusrc`. If it is not, every CI runner has to have every SDK installed, every auth config, every subprocess dependency. **A2A makes governance mode deployable. Bespoke adapters make it a dependency nightmare.**

Spec 048 FR-021 is worth quoting:

> "`conversus governance` MUST be invokable without Claude Code running (requires spec 042 execution providers)."

This is the core autonomous-mode requirement. The easiest, most future-proof way to satisfy it is to make conversus an A2A client that dispatches to remote A2A agents. Bespoke providers make it a subprocess-spawning binary with a directory full of SDKs to babysit.

---

## 5. Proposed Commitment

1. **Prioritize the `acp` provider.** Build it first per spec 042 §11 ("Priority — universal provider") and §4 ("The `acp` provider ... is the preferred path because it gives us the entire ACP ecosystem for free").
2. **Ship `conversus-acp-claude` as the reference A2A server wrapper** for Claude Code (spec 042 §12 Q7). This doubles as our "direct" Claude Code bridge for users running conversus locally — but the same code serves every other A2A client.
3. **Implement the `claude-code` direct provider ONLY as a fast-path optimization** for users who do not want to run a local A2A server. It is a convenience, not an architectural pillar. Its public surface matches the A2A server wrapper so users can migrate.
4. **Do NOT build bespoke providers for `copilot`, `gemini-cli`, `opencode`, `aider`, `gh-aw`, `langgraph`, `temporal`, `gsd`.** Instead, write A2A server wrappers for each as they become relevant. Each wrapper is a standalone artifact usable by any A2A client, not just conversus. Community can contribute.
5. **Use LiteLLM inside A2A server wrappers if we want**, but do not expose it as a conversus-level provider abstraction. LiteLLM becomes an implementation detail of the Tier 3 A2A server, not a public dispatch path.
6. **Align spec 048's `agent_registry` config with A2A Agent Detail discovery** so governance-mode agents are URLs, not hardcoded strings.

---

## 6. Summary

- A2A is backed by Google + IBM + Linux Foundation. This coalition wins standards wars. (tool-landscape.md §14)
- Spec 042 already maps conversus dispatch 1:1 to A2A Task Requests. (spec.md §2)
- Spec 042 already names the `acp` provider "Priority — universal provider." (spec.md §11)
- A2A gives us runtime agent discovery via Agent Detail. (tool-landscape.md §14)
- A2A gives us recursive composability — agents calling agents — which is load-bearing for spec 048 governance mode.
- The BeeAI Python SDK exists today. The research report provides a ~30-line integration sketch. (tool-landscape.md §Candidate B)
- The hybrid approach defers A2A by ~6 months at a cost of writing adapter code that will be deleted. (tool-landscape.md §Part 4, Phase 3)
- The build-our-own approach creates a 10+ adapter N×M explosion we own forever.
- Every counter-argument (newness, Claude Code gap, immaturity) is either (a) already stale or (b) already answered by spec 042's own wrapping strategy.
- Spec 048 makes A2A alignment load-bearing: every execution surface in the "CLI that runs outside your CLI" vision is an A2A client in disguise.

**We stop building bespoke adapters. We target A2A as the dispatch protocol. We ship one `acp` provider. We wrap Claude Code as our reference A2A server. Every future tool integration is an A2A server we write once and share with the entire agent ecosystem. Spec 042 already told us to do this — we should listen to it.**

---

**Files referenced**:
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/spec.md` (§2 Protocol Alignment, §4 ACP-Native Provider, §11 Provider Matrix, §12 Open Questions)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/042-execution-providers/research/tool-landscape.md` (§14 A2A Protocol, §Candidate B A2A Fit Assessment, §Candidate C Hybrid, §Part 3 Tradeoff Matrix, §Part 4 Recommendation)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/048-autonomous-governance-mode/spec.md` (§3 .conversusrc, §6 GitHub Actions, §9 Constraints, §11 "CLI that runs outside your CLI")
