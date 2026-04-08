# Devil's Advocate Review — Spec 011: Adoption Harness

## Executive Summary

Spec 011 proposes transforming conversus from a power-user deliberation framework into a multi-tier product spanning CLI, SDK, MCP server, and web application, with model agnosticism via LiteLLM and a "just ask" zero-config entry point. The ambition is clear: make structured multi-agent deliberation accessible to everyone from retirees picking stocks to AI-native engineers wiring up CI pipelines. The proposal identifies real barriers to adoption (YAML config, game theory jargon, Claude Code lock-in) and proposes real solutions.

The problem is that this proposal converges too quickly on a sprawling architecture without adequately stress-testing its own assumptions. It reads as a vision document that has already decided its answers before asking its questions. The eight open questions at the end (L129-138) are more dangerous than they appear — several of them, if answered differently than the proposal implicitly assumes, would invalidate entire sections of the architecture. The build order (L118-128) is presented as a sequential plan but contains hidden parallelism assumptions and scope risks that are not acknowledged. Most critically, the proposal never confronts the central tension: the features that make conversus genuinely valuable (adversarial multi-agent pressure, context isolation, phase barriers, game-theoretic incentive structures) are exactly the features most likely to be gutted or diluted by the "just ask" simplification that is supposed to drive adoption.

The most important recommendation: before building anything, the spec must define what "good enough" deliberation quality means for "just ask" mode, with concrete criteria that distinguish it from simply asking a single LLM the same question — because if that distinction is not measurable, the entire adoption thesis collapses.

## Alignment

- **Three-tier user model** (L25-31): The proposal correctly identifies that a single interface cannot serve all user types. Separating zero-config, guided, and power modes is sound architecture. The tier boundaries are drawn at the right fault lines (technical knowledge, configuration willingness, control needs).

- **Open questions are explicitly stated** (L129-138): The proposal does not hide its uncertainties. Eight open questions are listed, covering engine extraction strategy, abstraction layer choice, deployment model, community governance, MCP maturity, parallelism design, quality risk, and control balance. This intellectual honesty is a strength — the problem is not that the questions exist but that the rest of the proposal proceeds as if they have already been answered.

- **Constraint list** (L140-146): The constraints are well-chosen and mutually reinforcing. "Must not break existing `/conversus run` behavior" prevents regression. "Must not require any specific model or provider" enforces genuine agnosticism. "Must work for both trivial decisions and high-stakes decisions" prevents premature simplification. These constraints, if enforced, would catch many of the problems I identify below.

- **Performance optimizations acknowledge cost** (L109-116): The proposal recognizes that multi-agent deliberation is expensive (in time and API cost) and proposes concrete mitigations: parallel dispatch, smart defaults, streaming, caching, and model tiering. This shows awareness that adoption is not just about UX — it is also about economics.

## Missed Opportunities

- **No quality metric for "just ask" mode**: The proposal describes what "just ask" mode does (L33-45) but never defines how to tell if it worked. What distinguishes a good 2-agent, 1-round lightweight deliberation from asking ChatGPT the same question? Without a concrete quality bar — even a heuristic one like "the synthesis must contain at least one substantive disagreement that was resolved through evidence" — there is no way to know if the simplified mode is delivering conversus's value or just adding latency to a single-model response. Impact: high.

- **No degradation model across providers**: The proposal assumes LiteLLM makes model agnosticism straightforward (L57-72), but different models have wildly different capabilities for the kind of structured argumentation conversus requires. A Llama-7B agent cannot produce the same quality adversarial cross-review as Claude Opus. The spec needs a capability matrix or minimum model requirements per mode/tier, and a graceful degradation strategy when the selected model cannot support the requested deliberation depth. Impact: high.

- **No cost estimation or budget controls**: Multi-agent deliberation with 5 agents across 5 phases on GPT-4o or Claude could cost $5-20 per run. For the "just ask" mode targeting non-technical users, there is no discussion of cost visibility, budget caps, or how pricing works in a web app context. A retiree who asks "what stocks should I buy?" and gets a $15 API bill is not going to become a repeat user. Impact: high.

- **No failure mode analysis**: What happens when one agent in a parallel dispatch fails? When the model returns malformed output that does not match the template? When the LiteLLM abstraction silently changes behavior between providers? The current SKILL.md (L286-298) has strict rules about phase barriers and context isolation. The proposal does not discuss how these invariants survive extraction to a Python engine running across arbitrary providers. Impact: high.

- **No competitive differentiation articulation**: Open question 7 (L137) asks "Does 'just ask' mode risk oversimplifying?" but the proposal never answers the prior question: what is the user-visible evidence that multi-agent deliberation produces better outcomes than single-agent reasoning? The examples (L43-45) show multi-agent output formats, but a user comparing "ask ChatGPT" vs "ask conversus just-ask" needs to see a measurable difference. Without this, the adoption story is "it is like ChatGPT but slower and more expensive." Impact: high.

- **Community presets without quality control**: The proposal mentions a "community preset library" (L116) and open question 4 (L134) asks about curation vs. community contribution. But the existing preset system (SKILL.md L93-169) has strict validation requirements (name matching, category matching, composability flags). Scaling this to a community registry without defining quality gates, versioning, or deprecation policies creates a npm-left-pad risk for deliberation quality. Impact: medium.

- **No discussion of prompt injection risk**: When "just ask" mode auto-generates agent prompts from user natural language input (L36-41), the system is constructing agent identities from untrusted input. In a web app context (L89-98), this is a prompt injection surface. A user could craft input that causes agents to bypass their adversarial roles or produce biased outputs. Impact: medium.

- **MCP as "primary integration path" without fallback**: The proposal labels MCP as the primary integration path (L74) but open question 5 (L135) acknowledges MCP may not be mature enough. The build order (L125) places MCP at step 5, but no fallback integration strategy is defined if MCP adoption stalls. Impact: medium.

## Off-Base Assumptions

- **"LiteLLM as the model abstraction layer" implies uniform capability** (L59): The proposal treats model agnosticism as a routing problem — swap the provider, keep the behavior. This is incorrect. Conversus's value comes from structured adversarial pressure: agents must follow specific output formats (review sections per SKILL.md L59-72), respect phase boundaries, and produce genuinely independent positions. These behaviors are highly model-dependent. A model that cannot reliably follow the cooperative cross-review template (5 required sections per SKILL.md L106-111) will produce garbage that corrupts downstream phases. Model agnosticism is not "use any model" — it is "use any model that meets minimum capability thresholds for the requested mode."

- **"2-3 agents, 1 round — fast and cheap" implies adequate deliberation** (L40, L112): The proposal assumes a lightweight configuration is sufficient for "just ask" mode. But the entire conversus architecture is designed around multi-phase adversarial pressure: Phase 1 reviews are challenged by Phase 2 cross-reviews, which force Phase 3 revisions, which surface Phase 4 disputes. With only 1 round and no iterations, you get reviews and a synthesis — but you skip the cross-review/revision cycle that is the mechanism by which bad arguments get eliminated. A 2-agent, 1-round deliberation is structurally identical to asking two models the same question and having a third summarize — which is not what makes conversus valuable.

- **"Streaming output for real-time progress" is straightforward** (L113): The proposal lists streaming as a performance optimization, but the current architecture (SKILL.md L286-298) requires phase barriers — all agents in a phase must complete before the next phase begins. Streaming individual agent outputs is possible, but streaming the deliberation as a coherent narrative requires significant design work around partial-phase rendering, progress indicators that reflect the actual dependency graph, and handling the case where one agent in a parallel batch takes 10x longer than the others. This is not an optimization; it is a feature with its own spec.

## Actionable Recommendations

1. **Define deliberation quality criteria** (Priority: P1)
   - **Current state**: "Just ask" mode is described by its mechanics (L33-45) — classify, generate agents, pick mode, run, synthesize — but not by its quality bar.
   - **Proposed change**: Add a "Quality Model" section defining minimum criteria for a valid deliberation output. At minimum: (a) the synthesis must surface at least one substantive disagreement between agents, (b) each agent must reference specific evidence from its docs or the target, (c) the recommendation must acknowledge trade-offs, not just declare a winner. Define how to detect when a "just ask" run has degenerated to single-model-equivalent output.
   - **Rationale**: Without quality criteria, there is no way to iterate on "just ask" mode or to detect when model substitution degrades output below the threshold where conversus adds value over direct prompting.
   - **Risk if ignored**: "Just ask" ships as a slow, expensive wrapper around single-model Q&A, users see no benefit over ChatGPT, and the adoption thesis fails.

2. **Add model capability requirements per mode** (Priority: P1)
   - **Current state**: LiteLLM integration is described as a provider routing layer (L57-72) with no mention of minimum model capabilities.
   - **Proposed change**: Define a capability matrix: which modes require which model features (structured output, long context, instruction following fidelity). Add runtime validation that warns or blocks when the selected model is unlikely to produce valid deliberation output for the requested mode. For example: "prisoners-dilemma mode requires models scoring above X on structured instruction following benchmarks."
   - **Rationale**: The existing template system (SKILL.md L243-269) has strict structural requirements (headings, dispute markers, variable formats). Models that cannot reliably follow these templates will produce output that breaks downstream phases.
   - **Risk if ignored**: Users run conversus with a weak model, get garbage output, blame conversus instead of the model choice, and churn.

3. **Design the cross-review bypass for lightweight mode** (Priority: P1)
   - **Current state**: "Just ask" runs "2-3 agents, 1 round" (L40) but does not specify whether cross-reviews are included or skipped.
   - **Proposed change**: Explicitly design the phase subset for "just ask" mode. If cross-reviews are skipped, document what adversarial pressure mechanism replaces them. If cross-reviews are included, the "fast and cheap" claim needs revision (2 agents with cross-reviews = 2 + 2 + 2 + 2 + 1 = 9 agent launches, not "lightweight"). Consider a "mini-cross-review" phase where agents respond to each other in a single combined prompt rather than isolated context.
   - **Rationale**: The cross-review/revision cycle is the core mechanism that makes conversus outputs better than "ask N models and summarize" (SKILL.md L286-298, context isolation rationale). Skipping it without replacement removes the value; including it without modification contradicts the "lightweight" promise.
   - **Risk if ignored**: "Just ask" either produces shallow output (no cross-review pressure) or is slow and expensive (full cross-review cycle), and neither outcome serves the adoption goal.

4. **Add cost estimation and budget controls** (Priority: P1)
   - **Current state**: No mention of cost visibility, estimation, or limits anywhere in the proposal.
   - **Proposed change**: Add a "Cost Model" section. For each tier, estimate API cost ranges. For "just ask" and the web app, define a cost estimation step before execution ("This deliberation will use approximately X tokens across Y API calls, estimated cost: $Z. Proceed?"). For programmatic use (SDK, CI/CD), support budget caps that abort if estimated cost exceeds threshold.
   - **Rationale**: Multi-agent deliberation is inherently expensive. The proposal targets non-technical users (L12) who have no mental model for API costs. Surprise bills will kill adoption faster than any UX issue.
   - **Risk if ignored**: First-time web app users trigger expensive deliberations unknowingly, generate negative word-of-mouth, and the web app becomes a liability rather than an adoption driver.

5. **Resolve the engine extraction question before proceeding** (Priority: P1)
   - **Current state**: Open question 1 (L131) asks whether to extract to Python or keep SKILL.md with adapters. The build order (L120) assumes Python extraction is step 1, but the question is still open.
   - **Proposed change**: This is not an open question — it is a blocking architectural decision that determines the shape of everything downstream. The proposal should either commit to Python extraction with a concrete migration plan (including how SKILL.md's orchestration logic maps to Python constructs, how the Agent tool's parallel dispatch is replicated with asyncio, and how template resolution works without filesystem-relative paths) or commit to the adapter approach with a concrete interface definition. Present both as evaluated options with trade-offs, then decide.
   - **Rationale**: Every subsequent build step (CLI, MCP server, SDK, web app) depends on this decision. Leaving it open means the build order is not a plan — it is a wish list.
   - **Risk if ignored**: The team starts building and discovers halfway through that the extraction approach has fundamental problems (e.g., the parallel dispatch model does not translate, template resolution breaks), requiring a rearchitecture that invalidates work already done.

6. **Add failure mode analysis for multi-provider execution** (Priority: P2)
   - **Current state**: The proposal assumes multi-provider execution works if the routing layer works (L57-72). No failure modes are discussed.
   - **Proposed change**: Add a "Failure Modes" section addressing: (a) what happens when one agent in a parallel batch fails (retry? abort phase? continue with N-1 agents?), (b) how to handle provider-specific rate limits and throttling during parallel dispatch, (c) how to validate that agent output conforms to template structure before proceeding to the next phase, (d) how to handle provider API outages mid-deliberation.
   - **Rationale**: The current system runs on a single provider (Claude via Agent tool) where failure modes are well-understood. Moving to arbitrary providers multiplies the failure surface by the number of providers times the number of agents.
   - **Risk if ignored**: Production deliberations fail in unpredictable ways, partial outputs corrupt downstream phases, and debugging requires understanding both conversus internals and provider-specific failure modes.

7. **Separate the web app into its own spec** (Priority: P2)
   - **Current state**: The web app is described in 9 lines (L89-99) covering landing page, live view, mode picker, results, history, and sharing. Tech stack is specified (Next.js, FastAPI, WebSocket, PostgreSQL).
   - **Proposed change**: Remove the web app from this spec's build order. Create a separate spec (012 or later) for the web app after the core engine, CLI, and MCP server are stable. The web app introduces authentication, hosting, state management, real-time streaming, and database design — each of which is a significant design surface that is not addressed here.
   - **Rationale**: The web app is the highest-complexity, lowest-certainty item in the proposal. Including it in the same spec as the engine extraction creates scope that is impossible to estimate or validate. The architect agent in the conversus.yml (L57-77) explicitly calls this out: "The web app adds massive complexity. Is it worth it in v1?"
   - **Risk if ignored**: The web app scope creep delays delivery of the CLI, SDK, and MCP server — the distribution formats that serve the users most likely to adopt conversus first (developers and AI-native engineers).

8. **Define what "auto-generates 2-4 appropriate agents" means concretely** (Priority: P2)
   - **Current state**: "Just ask" mode "auto-generates 2-4 appropriate agents with relevant perspectives" (L38) with no specification of how this generation works.
   - **Proposed change**: Define the agent generation algorithm. Options include: (a) a classification model that maps question types to preset agent configurations, (b) a prompt that asks the model to generate agent identities and then instantiates them, (c) a rule-based system with heuristic matching. Each has different quality, cost, and latency characteristics. The spec should evaluate at least two approaches and select one with rationale.
   - **Rationale**: Auto-generation is the critical UX differentiator of "just ask" mode. If agents are poorly generated (e.g., two agents with nearly identical perspectives, or agents whose expertise does not match the question domain), the deliberation produces no adversarial pressure and no value. This is not a detail to defer — it is the mechanism that makes or breaks the feature.
   - **Risk if ignored**: Auto-generated agents produce low-quality deliberations, users do not understand why the output is unhelpful, and the "just ask" mode earns a reputation as unreliable.

9. **Address the "just another ChatGPT wrapper" risk head-on** (Priority: P2)
   - **Current state**: The adoption strategist agent (conversus.yml L93-95) flags this risk, but the proposal itself does not address it.
   - **Proposed change**: Add a "Differentiation" section that concretely demonstrates — with a side-by-side example — how a conversus "just ask" response differs from asking the same question to a single model. Show the structural differences: explicit disagreement, evidence-grounded positions, transparent reasoning chains, surviving dissent in the synthesis. If the differences are not visible in a side-by-side comparison, the product has a positioning problem that no amount of engineering will fix.
   - **Rationale**: The proposal's entire adoption thesis is that structured multi-agent deliberation produces better decisions. If users cannot see the difference, the thesis is untestable and the product is indefensible against "just use ChatGPT."
   - **Risk if ignored**: Conversus launches and is immediately dismissed as "ChatGPT with extra steps" because the value difference is not visible to users who do not understand the underlying mechanism.

10. **Define the MCP tool contract more precisely** (Priority: P3)
    - **Current state**: Six MCP tools are listed (L79-86) with one-line descriptions.
    - **Proposed change**: For each tool, define: input schema (what parameters it accepts), output schema (what it returns), error contract (what errors it raises and when), and execution model (synchronous vs. streaming vs. background). The `conversus_decide` tool in particular needs specification: does it block until the full deliberation completes? Does it stream intermediate results? What is the timeout behavior?
    - **Rationale**: MCP tool contracts are the API surface that third-party integrations depend on. Underspecifying them leads to integration breakage when implementation details change. The current SKILL.md (L17-19) is invoked via a single entry point (`/conversus run`); six separate tools need six separate contracts.
    - **Risk if ignored**: MCP integrations break across versions because the tool contracts were never specified, leading to distrust of the MCP distribution channel.

## Referenced Documentation

- `specs/011-adoption-harness/proposal.md` — sections/lines cited: L5-12, L14-21, L25-31, L33-45, L47-55, L57-72, L74-86, L89-99, L101-107, L109-116, L118-128, L129-138, L140-146
- `specs/011-adoption-harness/conversus.yml` — sections/lines cited: L57-77, L93-95
- `SKILL.md` — sections/lines cited: L17-19, L59-72, L93-169, L106-111, L243-269, L286-298
- `README.md` — sections/lines cited: L1-17 (architectural invariant), L59-72 (cross-review sections), L109-116 (scoring)
