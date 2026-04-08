# Architect Revision: Conversus Adoption Harness (011)

**Revision iteration**: 1
**Date**: 2026-03-21

---

### Recommendation Dispositions

#### Recommendation 1: Define-engine-interfaces-first

- **Original position**: Add a "Phase 0: Interface Definition" step before engine extraction, defining `DeliberationState`, `AgentState`, `RoundState`, `PluginResult`, and lifecycle hooks from spec 007 as Python dataclasses/protocols.
- **Disposition**: Modified
- **Explanation**:

Three cross-reviews challenged this recommendation, each from a different angle:

1. **devex-advocate** (Dangerous Contradictions, "SDK API design vs. engine-interfaces-first") correctly identified that my Phase 0 defines *internal* engine interfaces but ignores the *external* SDK API. The devex-advocate's `Problem`, `Config`, `Deliberation`, `Result` types are a different interface set from my `DeliberationState` and lifecycle hooks, and designing either in isolation produces impedance mismatch. The devex-advocate's suggested resolution -- design both interface sets together in Phase 0, with an explicit `to_result()` mapping layer -- is the right approach.

2. **adoption-strategist** (Dangerous Contradictions, "Build order: infrastructure-first vs. validation-first") argued that interface design should be informed by real usage data, not done in a vacuum. The specific claim: "The architect's Phase 0 interfaces will be better if they are designed after observing how users actually interact with 'Just Ask' mode." This is partially right. The core `DeliberationState` model is stable -- it tracks mode, round, agents, and synthesis, which are structural invariants of the deliberation protocol. But the external SDK types (what does `Result` look like? what fields matter to developers?) would genuinely benefit from usage data.

3. **devils-advocate** (Dangerous Contradictions, "Engine extraction scope") argued that Phase 0 commits design effort to Python extraction before resolving whether Python extraction is the correct approach at all. However, as I argued in my cross-review of the devil's advocate (Tensions, "Build order philosophy"), the spec 007 interfaces are approach-agnostic -- `DeliberationState` and lifecycle hooks define the *contract*, not the *implementation*. Whether the engine is a Python package or a SKILL.md adapter, it needs to communicate state in the same shape.

**Modified recommendation**: Phase 0 defines *both* internal engine interfaces (my original `DeliberationState`, `AgentState`, lifecycle hooks from spec 007) *and* external SDK types (devex-advocate's `Problem`, `Config`, `Deliberation`, `Result`), plus the mapping between them. Phase 0 is time-boxed to one week, not open-ended. The internal interfaces are defined from spec 007's existing design; the external SDK types are defined as an initial draft that may evolve after early usage data (adoption-strategist's concern). The devil's advocate's blocking-decision concern is addressed by noting that these interfaces are valid regardless of whether the implementation is Python extraction or SKILL.md adapters.

#### Recommendation 2: Decompose-engine-extraction

- **Original position**: Break engine extraction into 5 sub-phases: config parser, template engine, async dispatch, dispute parsing, and output manager.
- **Disposition**: Surviving
- **Explanation**:

No cross-review challenged the decomposition itself. All four cross-reviews either endorsed it or built upon it:

- **devex-advocate** (Safe Agreements, "Decomposition of the engine extraction") independently arrived at a complementary decomposition from the API perspective, confirming the internal decomposition maps to distinct external capabilities.
- **adoption-strategist** (Safe Agreements, "The proposal underestimates engine extraction complexity") endorsed the diagnosis from the adoption-timeline perspective.
- **devils-advocate** (Safe Agreements, "Engine extraction is undersized as a single phase") endorsed the decomposition and added the observation that the extraction *approach* is also undecided.
- **consumer-advocate** (Safe Agreements, "The proposal underestimates the complexity of engine extraction") agreed from the product perspective.

The 5-sub-phase decomposition is the most universally endorsed recommendation across all cross-reviews. It should survive into the synthesis as-is.

#### Recommendation 3: Design-async-dispatch-engine

- **Original position**: Add a dedicated architecture section specifying `asyncio.TaskGroup` for parallel dispatch, `PhaseBarrier` abstraction, per-agent error isolation, and configurable concurrency limits.
- **Disposition**: Modified
- **Explanation**:

Two cross-reviews strengthened this recommendation by adding requirements I missed:

1. **devils-advocate** (Safe Agreements, "Parallel dispatch outside Claude Code is a substantial unsolved engineering problem") added a failure-mode dimension I did not address. The devil's advocate's Recommendation #6 specifies: what happens when one agent fails? Provider rate limits? Malformed output? Mid-deliberation outages? My original recommendation specified the positive requirements (what the dispatch engine must do) but not the negative requirements (what failure modes it must handle). The devil's advocate's failure taxonomy is a necessary complement.

2. **devex-advocate** (Tensions, "Parallel dispatch complexity framing") added the observability dimension. The devex-advocate's streaming/progress design requires the dispatch engine to emit phase-lifecycle events. My `PhaseBarrier` abstraction naturally emits these events, but I did not make this explicit.

**Modified recommendation**: The async dispatch engine design must include three layers: (a) the positive contract (my original `asyncio.TaskGroup`, `PhaseBarrier`, context isolation, concurrency limits), (b) the failure-mode contract (devil's advocate's taxonomy: single-agent failure strategy, rate limit handling, output validation gates, mid-execution recovery), and (c) the observability contract (devex-advocate's phase-lifecycle events emitted by `PhaseBarrier` for streaming consumers). The single-agent failure question -- abort phase or continue with N-1 agents -- must be resolved as a design decision, not left as an open question.

#### Recommendation 4: Defer-web-app-to-v2

- **Original position**: Move the web app out of v1 scope entirely. Ship CLI + MCP server + Python SDK. Web app is a separate proposal.
- **Disposition**: Modified
- **Explanation**:

This was the most contested recommendation across all cross-reviews:

1. **consumer-advocate** (Dangerous Contradictions, "Web app priority: defer vs. elevate") made the strongest counter-argument: if v1 has no consumer path, the product establishes its identity as a developer tool, and the web app (whenever it ships) inherits developer-shaped abstractions. The suggested resolution -- a "v1.1" minimal web app (landing page + Just Ask + results, no auth, no history, no PostgreSQL) within weeks of v1 -- is a compromise I can accept.

2. **adoption-strategist** (Dangerous Contradictions, "Web app: defer to v2 vs. cut entirely") went further than I did, arguing the web app may not be the right vehicle at all for non-technical users, and proposing Slack bots, ChatGPT plugins, or simple hosted forms as alternatives. This is a perspective I had not considered. The cheapest path to non-technical users may not be a custom web app.

3. **devils-advocate** (Tensions, "Web app: defer to v2 vs. separate spec") proposed creating a separate spec (012 or later) for the web app, which is more rigorous than my "separate proposal" framing. The devil's advocate correctly notes this ensures the web app receives proper specification treatment.

4. **devex-advocate** (Tensions, "Scope of v1: web app inclusion") did not object to the web app's presence in the proposal, creating ambiguity about whether it stays in scope by default.

I was too absolute. Removing the web app "entirely" from v1 scope is correct for the *full-featured* web app (Next.js, PostgreSQL, auth, WebSocket streaming, decision history). But the consumer-advocate's point about product identity is real. If the engine is designed without any consumer surface in mind, its abstractions will be CLI-shaped.

**Modified recommendation**: Remove the full-featured web app from v1 scope. Create a separate spec (012) for it, as the devil's advocate recommends. However, add one engine-design constraint: the dispatch engine must emit phase-lifecycle events (as specified in modified Recommendation 3) that a future streaming consumer could subscribe to. This prevents painting the engine into a CLI-only corner. For reaching non-technical users in v1, evaluate lightweight alternatives (adoption-strategist's Slack bot, simple hosted form) alongside the engine work, rather than committing to a full web app prematurely. The decision of *which* consumer surface to build should be informed by demand data, not assumed to be a web app.

#### Recommendation 5: Address-LiteLLM-tool-use-gap

- **Original position**: Evaluate whether LiteLLM's tool-use normalization is sufficient; consider a thin `ConversusAgent` abstraction on top of LiteLLM that handles tool registration and output validation.
- **Disposition**: Modified
- **Explanation**:

Two cross-reviews deepened this recommendation in complementary ways:

1. **devils-advocate** (Dangerous Contradictions, "LiteLLM assessment: solvable engineering vs. fundamental capability gap") exposed a gap in my analysis. I focused on the API normalization problem (tool use, structured output, long-context handling), but the devil's advocate identified a deeper problem: model *capability* variance. A Llama-7B cannot produce the same quality cross-review as Claude Opus, and no amount of API wrapping fixes that. The devil's advocate's recommendation for a capability matrix -- minimum model requirements per mode/tier -- addresses a problem my `ConversusAgent` abstraction does not solve.

2. **devex-advocate** (Tensions, "LiteLLM adequacy assessment") proposed a thin `ModelProvider` interface (`async def complete(messages, **kwargs) -> str`) with LiteLLM as default. I challenged this in my cross-review (Dangerous Contradictions, "LiteLLM sufficiency assessment") because the `-> str` return type hides the fact that conversus agents need structured output, not bare strings. The devex-advocate's interface is the right *pattern* but the wrong *signature*.

The devil's advocate's cross-review resolution is correct: both positions are needed and non-overlapping. My `ConversusAgent` abstraction handles the *how* (API normalization); the devil's advocate's capability matrix handles the *whether* (model qualification).

**Modified recommendation**: The model abstraction requires two layers: (a) a `ModelProvider` interface following the devex-advocate's pattern but with a richer signature -- `async def execute(messages, tools, output_schema, **kwargs) -> AgentOutput` -- that accounts for structured output and tool use; and (b) a capability validation gate following the devil's advocate's pattern -- a per-mode capability matrix that checks whether the selected model meets minimum requirements before dispatching. LiteLLM is the default `ModelProvider` implementation. The capability gate runs before invocation; the `ConversusAgent` wrapper handles output validation after invocation. Both are needed.

#### Recommendation 6: Add-scenario-replay-to-MCP-tools

- **Original position**: Add `conversus_replay` as a seventh MCP tool exposing spec 007's scenario replay workflow.
- **Disposition**: Withdrawn
- **Explanation**:

The adoption-strategist's cross-review (Tensions, "Scenario replay: engine feature vs. adoption feature") correctly reframed the priority. The strategist distinguishes between *presets* (reusable configurations for starting new deliberations) and *replays* (re-running specific past deliberations). Presets serve the adoption use case; replays serve the retention use case. The strategist argues presets should come first because they have lower technical dependency and immediate adoption value, while replay depends on spec 007 infrastructure that all reviews agree should come after initial adoption validation.

I was wrong to prioritize replay over presets. Replay requires the spec 007 scenario storage system, which is not part of the v1 engine extraction. Adding `conversus_replay` to the MCP tool surface before the storage system exists is premature -- it would be a tool signature with no implementation. The adoption-strategist is right that presets are the on-ramp and replay is the retention mechanism, and the on-ramp must come first.

#### Recommendation 7: Resolve-SKILL.md-vs-engine-coexistence

- **Original position**: Commit to the Python engine as canonical. SKILL.md becomes either a thin adapter or a frozen legacy format. Do not maintain two independent implementations.
- **Disposition**: Modified
- **Explanation**:

Two cross-reviews challenged the *timing* of this commitment, though not the principle:

1. **adoption-strategist** (Dangerous Contradictions, "SKILL.md coexistence: thin adapter vs. frozen legacy") argued that SKILL.md should be the initial shipping vehicle for Just Ask, with new features built into it for fast validation. The strategist explicitly wants to invest new features in the SKILL.md path, which contradicts my recommendation to freeze it.

2. **devils-advocate** (Dangerous Contradictions, "Engine extraction scope: monolithic phase vs. blocking architectural question") argued that the Python extraction decision itself is not yet validated and should be formally evaluated before committing.

In my cross-review of the adoption-strategist (Dangerous Contradictions, "SKILL.md as living distribution format vs frozen legacy"), I proposed a resolution that I still believe is correct: build Just Ask as a thin config-generation layer that delegates to existing SKILL.md execution (`auto-generate conversus.yml, call /conversus run`), rather than adding new orchestration logic to SKILL.md. If Just Ask is purely config-generation plus output formatting, it is portable to any runtime. The orchestration logic remains in one place.

The principle survives: do not maintain two independent implementations of orchestration logic. But the timing must change.

**Modified recommendation**: SKILL.md remains the primary execution runtime for initial user validation (adoption-strategist's concern). New features (Just Ask) are built as config-generation layers *on top of* existing SKILL.md orchestration, not as new orchestration logic *within* SKILL.md. This preserves the portability of the new features -- when the Python engine ships, the config-generation layer ports trivially. The commitment to Python-as-canonical is made *after* the Phase 0 interface definition demonstrates that spec 007's plugin system requires a Python runtime (which it does -- lifecycle hooks, `DeliberationState`, and feature extraction are all Python constructs). The devil's advocate's formal evaluation is satisfied; the adoption-strategist's speed-to-users is preserved; and the principle of single-implementation is maintained by not adding new orchestration logic to SKILL.md.

#### Recommendation 8: Specify-output-contract-for-Just-Ask

- **Original position**: Just Ask output must produce a subset of the standard conversus output following mode-specific template structure, ensuring ecosystem compatibility (prior context, dispute parsing, plugins).
- **Disposition**: Modified
- **Explanation**:

This recommendation received the most diverse set of challenges:

1. **consumer-advocate** (Dangerous Contradictions, "Just Ask output format: structured vs. plain-English") argued for progressive disclosure with three layers: headline, summary, and expandable full arguments. The consumer-advocate's resolution -- generate output using my template structure, then render through progressive disclosure layers -- correctly separates data model from presentation.

2. **devex-advocate** (Tensions, "Just Ask output format") argued the output should be a Python dataclass / JSON object with `recommendation`, `confidence`, `mode_used`, `agents`, `arguments`, `dissent`, `raw_synthesis`. Plain English is "a rendering of this structure, not the primary output."

3. **devils-advocate** (Dangerous Contradictions, "Just Ask output format: structured subset vs. quality-defined") argued the primary constraint should be output *quality*, not output *format*. A well-formatted document that is no better than ChatGPT output is worthless. The devil's advocate wants quality criteria: "the synthesis must contain at least one substantive disagreement that was resolved through evidence."

4. **adoption-strategist** (Tensions, "Just Ask output format: structured vs. accessible") argued for two layers: concise recommendation (2-3 sentences) plus full debate transcript showing agent positions and cross-review attacks.

The devil's advocate's challenge is the one that changed my thinking most. I was focused on format compatibility (can the output feed into `prior:` context?) when I should have been focused first on *whether the output is worth feeding into anything*. The devil's advocate is right: quality is the acceptance criterion; format is the implementation constraint.

**Modified recommendation**: Just Ask output has three constraints, in priority order: (1) **Quality gate** (devil's advocate): the output must demonstrate genuine multi-perspective deliberation -- at minimum, one substantive disagreement that was resolved through evidence, not just summarized away. Define measurable quality criteria that distinguish Just Ask output from a single-model response. (2) **Structural contract** (original position): the underlying artifact follows the mode-specific template structure for ecosystem compatibility (prior context, dispute parsing, plugins). (3) **Presentation layer** (consumer-advocate + adoption-strategist + devex-advocate): the structured artifact is rendered differently per distribution channel -- progressive disclosure for web, concise + expandable for CLI, typed `Result` dataclass for SDK. The template-structured markdown is the canonical artifact; all other views are renderings.

#### Recommendation 9: Define-minimum-viable-extraction

- **Original position**: Define an MVE as a Python CLI that reads conversus.yml, makes concurrent API calls to one provider (Anthropic), writes output files, and supports cooperative mode only.
- **Disposition**: Modified
- **Explanation**:

The adoption-strategist's cross-review (Tensions, "Minimum viable product scope: engine MVE vs. feature MVP") drew a critical distinction I had blurred. My MVE tests "can we extract the orchestration logic into standalone Python?" The strategist's MVP tests "do users trust multi-agent deliberation for real decisions?" These are different hypotheses, and the strategist is right that the existential question (is there demand?) should be answered before the engineering question (can we extract?).

However, the strategist's cross-review also acknowledged (Coordination needed) that my MVE scope -- cooperative-only, single-provider -- "is actually a good match for what early 'Just Ask' usage will likely show." This suggests the two can be sequenced without conflict.

**Modified recommendation**: Define two minimum viable milestones. **MV1** (feature validation): Just Ask mode running within the existing SKILL.md runtime (adoption-strategist's recommendation), validating that users trust multi-agent deliberation for real decisions. Target: 50+ real deliberations within 2-4 weeks. **MV2** (engine validation): Python CLI that reads conversus.yml, makes concurrent API calls to one provider (Anthropic), writes output files, supports cooperative mode only. MV2 is informed by MV1's usage data -- which modes were selected, what output formats users needed, how often multi-round was triggered. MV1 does not require Python extraction; MV2 does not require multi-provider support. Each validates a different hypothesis. The devex-advocate's SDK type definitions (from modified Recommendation 1) are designed for all modes but MV2 only implements cooperative, with `mode_used` always set to `"cooperative"` in the initial release.

#### Recommendation 10: Align-model-tiering-with-provider-abstraction

- **Original position**: Move model tiering from "Performance Optimizations" to the LiteLLM architecture section. Define per-phase model configuration in conversus.yml, overriding the SKILL.md constraint that all subagents use the orchestrator's model.
- **Disposition**: Modified
- **Explanation**:

The devils-advocate's cross-review (Tensions, "Scope of 'model agnosticism' ambition") identified a compounding problem I had not considered. My per-phase model tiering (`gpt-4o-mini` for cross-reviews, `claude-opus-4` for synthesis) actually *increases* the capability validation problem. If the system mixes providers within a single deliberation, the capability matrix (from modified Recommendation 5) must validate each model against the requirements of its *assigned phase*, not just check that a model is supported by LiteLLM. A cheap model assigned to cross-reviews might not meet the minimum threshold for producing structurally valid cross-review output.

The consumer-advocate's cross-review (Tensions, "Model tiering scope: optimization vs. architecture") also noted that the consumer-advocate's "fast and cheap" goal for Just Ask implicitly depends on model tiering, but neither review had made this dependency explicit.

**Modified recommendation**: Model tiering is an architectural decision that must be designed into the engine's provider abstraction from Phase 0. The per-phase model configuration is the right design (`models: { default: ..., synthesis: ..., cross-review: ... }`). However, each per-phase model assignment must pass the capability validation gate (from modified Recommendation 5) for that specific phase's requirements -- not just a general "is this model supported?" check. For Just Ask mode, model tiering is automatic (the system selects appropriate models per phase based on the capability matrix), not user-configured. For Power mode, model tiering is explicit user configuration with validation warnings when a selected model does not meet the phase's capability threshold.

---

### New Recommendations

- **Add-question-classifier-protocol** (Priority: P2)
  - **Triggered by**: consumer-advocate's cross-review (Tensions, "Vague question handling: system concern vs. consumer concern"). The consumer-advocate identified that I did not address vague input handling anywhere in my review, and that for the consumer path, input quality is the architectural concern. My cross-review of the consumer-advocate (Tensions, "Vague question handling vs. single-shot Just Ask") proposed a `NEEDS_CLARIFICATION` state in the execution flow but did not elevate this to a recommendation.
  - **Proposed change**: Define a `QuestionClassifier` protocol in Phase 0 alongside `DeliberationState`. The classifier takes natural-language input and produces either a valid config (sufficient-input mode) or a clarification request (clarification mode). The engine's execution flow has an explicit `NEEDS_CLARIFICATION` state between question intake and agent dispatch. This is the hook point for handling vague questions without requiring each distribution channel to invent its own classification logic.
  - **Rationale**: Every distribution channel (MCP, CLI, web, SDK) will face the vague-question problem. If classification logic is not part of the engine, it will be reimplemented inconsistently across channels. Defining the protocol in Phase 0 costs almost nothing (it is a type definition) but ensures all channels share the same classification contract.

- **Add-engine-event-model** (Priority: P2)
  - **Triggered by**: The convergence of three cross-reviews on the need for the dispatch engine to emit observable events. The devex-advocate (Tensions, "Parallel dispatch complexity framing") wants progress events for streaming. The consumer-advocate (Safe Agreements, "Parallel dispatch is harder") implicitly requires streaming for real-time deliberation viewing. My own modified Recommendation 4 (web app deferral) adds the constraint that the engine must emit phase-lifecycle events for future streaming consumers. Rather than treating this as a footnote on other recommendations, it deserves its own recommendation.
  - **Proposed change**: Define a `DispatchEvent` type in Phase 0 that the `PhaseBarrier` abstraction emits at each phase boundary. Events include: `PHASE_STARTED`, `AGENT_DISPATCHED`, `AGENT_COMPLETED`, `AGENT_FAILED`, `PHASE_COMPLETED`, `DELIBERATION_COMPLETED`. Each event carries the relevant `DeliberationState` snapshot. Distribution channels subscribe to these events for their presentation needs (streaming in web, progress bars in CLI, progress notifications in MCP).
  - **Rationale**: Without an explicit event model, the dispatch engine becomes a black box that only emits final output. This makes streaming, progress reporting, and real-time viewing impossible without retrofitting. Defining the event types in Phase 0 is a small investment that prevents a large retrofit later.

---

### Position Summary

Of my original 10 recommendations, I have withdrawn 1 (scenario replay to MCP tools), modified 8, and maintained 1 (decompose engine extraction). I added 2 new recommendations (question classifier protocol, engine event model). The high modification rate reflects genuine engagement with the cross-reviews rather than stubbornness -- most modifications *strengthened* the original recommendation by adding dimensions I had missed, rather than retreating from the core position.

The most significant change in my thinking was caused by the devil's advocate's challenge to my Just Ask output recommendation. I had framed the output contract as primarily a format compatibility problem -- can the output feed into `prior:` context and dispute parsing? The devil's advocate reframed it as a quality problem -- is the output worth feeding into anything? This shifted my priority ordering: quality gate first, structural contract second, presentation layer third. The consumer-advocate, devex-advocate, and adoption-strategist each added a presentation-layer requirement, but the devil's advocate's quality challenge was the one that changed the fundamental priority. A well-formatted document that is no better than ChatGPT is worse than useless -- it is actively misleading because the multi-agent framing implies rigor that does not exist.

My highest-priority surviving recommendation is the decomposition of engine extraction into independently testable sub-phases (Recommendation 2). This is the only recommendation that received zero challenges across all four cross-reviews. Every reviewer independently confirmed that treating engine extraction as a single build phase is a planning failure. The 5-sub-phase decomposition (config parser, template engine, async dispatch, dispute parsing, output manager) maps to distinct SKILL.md subsystems with clear input/output contracts, and it is the structural foundation on which all other recommendations depend. If the synthesis adopts only one thing from my review, it should be this decomposition -- it makes the extraction estimable, testable, and parallelizable, which are prerequisites for every other recommendation's success.
