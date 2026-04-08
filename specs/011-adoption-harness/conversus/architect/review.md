# Architect Review: Conversus Adoption Harness (011)

---

### Executive Summary

The Adoption Harness proposal aims to transform conversus from a power-user Claude Code skill into a general-purpose decision-making tool with five distribution formats (MCP server, Python CLI, web app, Claude Code skill, Python SDK), three user tiers (Just Ask, Guided, Power), and model agnosticism via LiteLLM. The ambition is correct: conversus's current SKILL.md + Agent tool architecture locks it to a single runtime, a single model provider, and users who can hand-write YAML. Opening it up is the right strategic move.

However, the proposal underestimates the engineering difficulty of the extraction step and overestimates how many distribution formats can share a single engine in v1. The SKILL.md orchestration logic at `SKILL.md, L286-298` encodes five non-negotiable multi-agent rules (one agent per output file, parallel dispatch within phases, context isolation, no meta-agents, hard phase boundaries) that are trivial to enforce when Claude Code's Agent tool does the dispatching but require substantial infrastructure to replicate in a standalone Python runtime. The proposal lists 8 build phases but does not address the hardest engineering problem: how asyncio + concurrent API calls replicate the Agent tool's parallel dispatch semantics, error handling, and output isolation. Meanwhile, the web app (phase 7) adds auth, hosting, streaming, and state management complexity that dwarfs the core engine work. The spec 007 plugin system (phase 8) is listed last but is architecturally foundational -- it defines the Python plugin API and `DeliberationState` model that the engine extraction in phase 1 needs to target.

The most important recommendation: invert the build order so that spec 007's plugin interface and `DeliberationState` model are defined first, then extract the engine to target those interfaces, deferring the web app to v2 or later.

---

### Alignment

- **Three-tier user model** (`L25-31`): The Just Ask / Guided / Power tiering correctly maps to three distinct user populations with different config effort tolerances. This aligns with the SKILL.md architecture, which already separates the concerns of config parsing (`SKILL.md, L28-78`) from orchestration (`SKILL.md, L273-327`), making it feasible to wrap different front-ends around the same execution core.

- **Maintaining Claude Code Skill** (`L54`): Keeping the current SKILL.md as a distribution format alongside the new engine is the right call. The SKILL.md is battle-tested orchestration logic, and the proposal correctly identifies it should be "maintained as-is" rather than replaced. This preserves the working system while the Python engine matures.

- **Parallel agent dispatch acknowledged** (`L111`): The proposal notes that parallel agent dispatch is "already built," which is accurate for the Claude Code runtime (`SKILL.md, L290-291`, `SKILL.md, L397`). Recognizing this as existing capability rather than something to invent is correct.

- **Plugin system as final phase** (`L128`): While I argue below that spec 007's interfaces should be defined earlier, the proposal does correctly identify that the plugin system (spec 007) is part of the adoption harness scope. The connection between distribution formats and the plugin architecture from `007-game-engine/spec.md, L62-70` (design principles: core works alone, plugins optional, data flows one direction) is implicitly maintained.

- **MCP tool surface** (`L79-86`): The six MCP tools (`conversus_decide`, `conversus_define`, `conversus_interests`, `conversus_mode`, `conversus_converge`, `conversus_run`) are a well-chosen surface area. They map cleanly to the existing execution model: `conversus_run` maps to the full SKILL.md execution (`SKILL.md, L19`), while the others decompose the guided workflow into discrete steps.

---

### Missed Opportunities

- **DeliberationState as the extraction target**: The proposal describes engine extraction (phase 1) as "SKILL.md logic to Python package" (`L120`) but does not reference the `DeliberationState` model already designed in spec 007 (`007-game-engine/spec.md, L138-146`). That model defines `mode`, `round`, `agents` (positions/concessions), `synthesis`, and `history` -- exactly the runtime state that the Python engine needs to maintain. Building the engine without this model means retrofitting it later when plugins need it. Impact: high.

- **Plugin lifecycle hooks as engine architecture**: The proposal's build order puts the plugin system last (`L128`), but spec 007's lifecycle hooks (`007-game-engine/spec.md, L96-112`) -- `PRE_EXECUTION`, `POST_PHASE_5`, `POST_DELIBERATION`, `POST_ARBITRATION` -- are not just plugin attachment points. They are the natural phase boundaries of the engine itself. Designing the engine around these hooks from the start means the plugin system is just exposing what already exists, rather than a separate integration project. The SKILL.md already has these implicit boundaries (`SKILL.md, L296-297`: "Phase boundaries are hard barriers"). Impact: high.

- **Feature extraction pipeline for "Just Ask" mode**: The proposal's "Just Ask" mode (`L34-45`) needs to classify question types and auto-generate agents. Spec 007 defines a feature extraction pipeline (`007-game-engine/spec.md, L166-177`) that converts deliberation artifacts to numerical vectors. A subset of this -- specifically the structured extraction approach (`007-game-engine/spec.md, L392-406`) -- could be adapted for input classification rather than output analysis, using the same template-structure-is-schema principle to parse natural language questions into config parameters. Impact: medium.

- **Scenario replay as a distribution feature**: Spec 007 defines scenario storage and replay (`007-game-engine/spec.md, L509-597`), which is a powerful adoption feature for teams who want to reuse decision frameworks. The proposal's distribution formats do not mention scenario replay at all. For the MCP server and CLI, exposing `conversus_replay` as a tool/command would significantly increase adoption for recurring decisions. Impact: medium.

- **Config optimizer for "Just Ask" defaults**: The proposal mentions "smart defaults" (`L112`) for Just Ask mode (2-3 agents, 1 round) but does not connect this to spec 007's config optimizer plugin (`007-game-engine/spec.md, L47, L206-211`), which can compute optimal rounds/agents/mode for a given problem structure. Even without the full nashopt integration, the config optimizer's interface (`PRE_EXECUTION` hook) is the right place to house the "Just Ask" auto-configuration logic. Impact: medium.

- **Stagnation detection portability**: The SKILL.md's stagnation detection (`SKILL.md, L488-495`) relies on the Dispute-Parsing Subsystem (`SKILL.md, L670-697`), which parses synthesis markdown for structural markers and mode-specific headings. The proposal does not address how this parsing logic transfers to the Python engine. This is non-trivial: the parsing rules are currently specified as prose instructions for Claude Code's agent, not as executable code. They need to become deterministic Python functions. Impact: medium.

- **Model tiering requires provider abstraction design**: The proposal mentions "cheap model for cross-reviews, expensive for synthesis" (`L115`) but the current SKILL.md explicitly states "All subagents use the orchestrator's model. Per-agent model selection is not supported" (`SKILL.md, L716`). Model tiering is a new capability that requires the provider abstraction to support per-phase or per-agent model selection -- this is a design requirement for the LiteLLM integration (phase 2), not just an optimization. Impact: medium.

- **Template validation in non-Claude-Code runtimes**: The SKILL.md's template validation (`SKILL.md, L260-271`) currently invokes `uv run python linter/validate.py`. In the Python engine, this should be a direct function call, not a subprocess invocation. The proposal does not address how the existing linter infrastructure integrates with the new engine. Impact: low.

---

### Off-Base Assumptions

- **"Parallel agent dispatch (already built)" (`L111`)**: This is misleading. Parallel dispatch is built *for Claude Code's Agent tool* (`SKILL.md, L290-291`: "All agents within a phase launch in a single message"). The Agent tool handles background execution, output collection, and error propagation natively. In a standalone Python runtime, "parallel dispatch" means implementing an async task manager that: (a) makes concurrent LLM API calls, (b) enforces context isolation between concurrent agents, (c) collects and validates outputs, (d) handles partial failures without corrupting other agents' results, and (e) enforces hard phase barriers (`SKILL.md, L296-297`). This is a substantial piece of infrastructure that does not exist and must be built from scratch. The proposal's open question #6 (`L136`) acknowledges this but framing it as "already built" in the performance section creates a false sense of readiness.

- **"Python engine extraction (SKILL.md logic to Python package)" as a single build phase (`L120`)**: This undersells the scope. SKILL.md is not a script to be transliterated; it is an agent orchestration specification that relies on the host runtime (Claude Code) for execution. The extraction requires: (1) a config parser (rewriting `SKILL.md, L28-196` as Python), (2) a template engine (rewriting `SKILL.md, L243-271`), (3) a parallel dispatch engine (rewriting `SKILL.md, L273-327` with an async runtime), (4) a dispute parsing subsystem (rewriting `SKILL.md, L670-697`), (5) an output manager (directory creation, file writes, round-directory restructuring from `SKILL.md, L210-241`), and (6) an agent prompt construction system (all of `SKILL.md, L358-598`). Each of these is a module-scale piece of work. Treating it as one phase risks underestimating the effort by 3-5x.

- **LiteLLM as a simple swap (`L59`)**: The proposal presents LiteLLM as a drop-in model abstraction layer. LiteLLM does handle multi-provider routing, but conversus's agent model is unusual: agents are not simple prompt-response pairs. Each agent needs to read files, write files, and follow structured output formats. In Claude Code, the Agent tool provides this capability natively. With LiteLLM, the engine must implement tool-use patterns (function calling) or structured output enforcement per provider, and these APIs differ significantly across OpenAI, Anthropic, and Google. LiteLLM normalizes the chat completion API but does not normalize tool use, structured output, or long-context handling -- all of which conversus agents depend on.

---

### Actionable Recommendations

1. **Define-engine-interfaces-first** (Priority: P1)
   - **Current state**: Build order starts with "Python engine extraction" (`L120`) and puts the plugin system last (`L128`).
   - **Proposed change**: Add a "Phase 0: Interface Definition" step before engine extraction. Define `DeliberationState`, `AgentState`, `RoundState`, `PluginResult`, and the lifecycle hook enum from spec 007 (`007-game-engine/spec.md, L131-157`) as Python dataclasses/protocols. The engine extraction then targets these interfaces. The plugin system becomes "expose what already exists" rather than "retrofit hooks into a finished engine."
   - **Rationale**: Spec 007 has already designed these interfaces (`007-game-engine/spec.md, L96-158`). They encode the phase-boundary and state-passing architecture that the engine needs regardless of plugins. Building without them means a second rewrite when plugins ship.
   - **Risk if ignored**: The engine will be built with ad-hoc internal state, requiring a disruptive refactor to support plugins. Phase 8 becomes a rewrite, not an integration.

2. **Decompose-engine-extraction** (Priority: P1)
   - **Current state**: "Python engine extraction (SKILL.md logic to Python package)" is a single build phase (`L120`).
   - **Proposed change**: Break into 5 sub-phases: (a) config parser + validator, (b) template engine + linter integration, (c) async dispatch engine with phase barriers, (d) dispute parsing subsystem, (e) output manager with round-directory lifecycle. Each is independently testable against the SKILL.md specification.
   - **Rationale**: SKILL.md contains 734 lines of orchestration logic across 6 distinct subsystems (`SKILL.md, L28-734`). A monolithic extraction will produce an untestable blob. Each subsystem has clear input/output contracts that map to module boundaries.
   - **Risk if ignored**: Monolithic extraction produces a single large module with interleaved concerns, making debugging and iterative development impractical.

3. **Design-async-dispatch-engine** (Priority: P1)
   - **Current state**: Open question #6 (`L136`) asks "How do we handle multi-agent parallelism outside of Claude Code's Agent tool?" with no proposed answer.
   - **Proposed change**: Add a dedicated architecture section specifying: (a) `asyncio.TaskGroup` for parallel agent dispatch within phases, (b) a `PhaseBarrier` abstraction that collects all agent results before allowing the next phase, (c) per-agent error isolation (one agent's failure does not crash others), (d) configurable concurrency limits (rate limiting for API providers). Reference the non-negotiable rules at `SKILL.md, L286-298` as the contract the dispatch engine must satisfy.
   - **Rationale**: The five non-negotiable multi-agent rules (`SKILL.md, L286-298`) are the architectural invariants of conversus. The dispatch engine is the component that enforces them. Without explicit design, these rules will be violated.
   - **Risk if ignored**: Subtle concurrency bugs (e.g., agents seeing each other's in-progress outputs, phase barriers not enforcing, partial failures corrupting state) that are invisible in testing and catastrophic in production.

4. **Defer-web-app-to-v2** (Priority: P1)
   - **Current state**: Web app is build phase 7 (`L127`), listed before plugins.
   - **Proposed change**: Move the web app out of the v1 scope entirely. The web app requires: Next.js frontend, FastAPI backend, WebSocket streaming, PostgreSQL, authentication, session management, deployment infrastructure, and a real-time deliberation viewer (`L89-99`). This is a full product engineering effort that is orthogonal to the core engine work. Replace with: "v1 ships CLI + MCP server + Python SDK. Web app is a separate proposal."
   - **Rationale**: The web app shares the Python engine with CLI/MCP but adds 5+ new technology layers (Next.js, WebSocket, PostgreSQL, auth, hosting). Including it in the same proposal creates scope pressure that will force shortcuts in the engine layer. The SKILL.md orchestration logic (`SKILL.md, L273-327`) is complex enough to extract correctly without also building a real-time streaming UI.
   - **Risk if ignored**: The engine extraction will be rushed to make room for web app work, producing a fragile foundation that all five distribution formats depend on.

5. **Address-LiteLLM-tool-use-gap** (Priority: P2)
   - **Current state**: LiteLLM is presented as a straightforward abstraction layer (`L59-72`).
   - **Proposed change**: Add a section acknowledging that conversus agents are not simple chat completions. They require: (a) reading files (tool use or context injection), (b) writing structured output to specific paths, (c) following template-dictated output formats. Evaluate whether LiteLLM's tool-use normalization is sufficient or whether a custom agent abstraction is needed on top of LiteLLM. Consider a thin `ConversusAgent` abstraction that uses LiteLLM for the API call but handles tool registration and output validation.
   - **Rationale**: The SKILL.md agents use Read and Write tools (`SKILL.md, L13`). In standalone Python, file I/O is direct, but prompt construction and output parsing still need to handle the structured format that templates produce. LiteLLM does not solve this.
   - **Risk if ignored**: The engine works with Anthropic's API (which has native tool use) but breaks with OpenAI or Ollama due to different tool-use semantics. "Model agnostic" becomes "model agnostic for simple cases."

6. **Add-scenario-replay-to-MCP-tools** (Priority: P2)
   - **Current state**: MCP tools are `conversus_decide`, `conversus_define`, `conversus_interests`, `conversus_mode`, `conversus_converge`, `conversus_run` (`L79-86`).
   - **Proposed change**: Add `conversus_replay` as a seventh MCP tool, exposing spec 007's scenario replay workflow (`007-game-engine/spec.md, L566-587`). Input: scenario ID + new target path. Output: deliberation results using stored config.
   - **Rationale**: Scenario replay (`007-game-engine/spec.md, L509-597`) is one of the most adoption-friendly features in the conversus ecosystem. Teams that run a good deliberation want to reuse the framework. Making replay a first-class MCP tool means it is discoverable in every MCP-compatible editor.
   - **Risk if ignored**: Users manually reconfigure YAML for recurring decisions, reducing adoption and increasing error rates.

7. **Resolve-SKILL.md-vs-engine-coexistence** (Priority: P2)
   - **Current state**: Open question #1 (`L131`) asks whether the engine should be extracted to Python or kept as SKILL.md with adapters. The proposal lists both as distribution formats (`L54`).
   - **Proposed change**: Commit to a clear answer: the Python engine is the canonical implementation. SKILL.md becomes a thin adapter that invokes the Python engine via subprocess or MCP, OR SKILL.md is frozen as a legacy distribution format that receives no new features. Do not maintain two independent implementations of the same orchestration logic -- they will diverge.
   - **Rationale**: SKILL.md contains 734 lines of orchestration spec (`SKILL.md, L1-734`). A Python engine will also encode this logic. Maintaining both in sync is a coordination burden that scales with every new feature. The spec 007 plugin system (`007-game-engine/spec.md, L62-70`) is designed for the Python engine; it cannot run in SKILL.md.
   - **Risk if ignored**: Feature drift between SKILL.md and Python engine produces two subtly different deliberation behaviors, making bug reports unresolvable ("works in Claude Code, fails in CLI").

8. **Specify-output-contract-for-Just-Ask** (Priority: P2)
   - **Current state**: "Just Ask" mode returns "a plain-English synthesis with the recommendation, supporting arguments, and dissenting views" (`L41`).
   - **Proposed change**: Define the output format explicitly. "Just Ask" should produce a subset of the standard conversus output: at minimum, a synthesis file following the same mode-specific template structure. This ensures "Just Ask" results can be fed back into the system as `prior:` context (`SKILL.md, L51-56`) for deeper follow-up deliberation, and that the dispute parsing subsystem (`SKILL.md, L670-697`) works on Just Ask output.
   - **Rationale**: The SKILL.md's `prior:` mechanism (`SKILL.md, L87-91`) and dispute parsing subsystem (`SKILL.md, L670-697`) depend on structured output. If "Just Ask" produces unstructured prose, it cannot participate in the conversus ecosystem (no follow-up rounds, no arbitration, no plugin analysis).
   - **Risk if ignored**: "Just Ask" becomes an island -- its outputs cannot feed into guided or power-user workflows, forcing users to start over when they want to go deeper.

9. **Define-minimum-viable-extraction** (Priority: P3)
   - **Current state**: The proposal presents a linear 8-phase plan (`L118-128`) without identifying a minimum viable product.
   - **Proposed change**: Add a "Minimum Viable Extraction" section. The MVE is: Python CLI that reads `conversus.yml`, makes concurrent API calls to one provider (Anthropic), writes output files, and supports cooperative mode only. This is shippable, testable, and validates the core extraction without requiring LiteLLM, MCP, Just Ask, or multi-provider support. Each subsequent phase extends the MVE.
   - **Rationale**: An 8-phase plan with no identified MVP creates "phase 1 paralysis" -- the team tries to build the entire engine before shipping anything. A cooperative-only, single-provider CLI can validate the extraction in days, not months. The SKILL.md's cooperative mode is the simplest orchestration path (no role assignments, straightforward dispute parsing at `SKILL.md, L688`).
   - **Risk if ignored**: The extraction effort takes months before producing anything runnable, losing momentum and making course correction impossible.

10. **Align-model-tiering-with-provider-abstraction** (Priority: P3)
    - **Current state**: Model tiering is listed as a performance optimization (`L115`): "cheap model for cross-reviews, expensive for synthesis."
    - **Proposed change**: Move model tiering from the "Performance Optimizations" section into the LiteLLM architecture section. Define it as a per-phase model configuration in `conversus.yml`, overriding the SKILL.md constraint that "All subagents use the orchestrator's model" (`SKILL.md, L716`). Example config: `models: { default: claude-sonnet-4-6, synthesis: claude-opus-4, cross-review: gpt-4o-mini }`.
    - **Rationale**: Model tiering is an architectural decision, not an optimization. It requires the provider abstraction to support per-invocation model selection, which must be designed into the engine from the start, not bolted on later.
    - **Risk if ignored**: The engine is built with a single-model assumption baked into the dispatch loop, requiring a refactor to support per-phase model selection.

---

### Referenced Documentation

- `/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/proposal.md` -- sections/lines cited: L25-31, L34-45, L54, L59-72, L79-86, L89-99, L111-116, L118-128, L120, L127, L128, L131, L136, L141
- `/Users/brettkellgren/Sites/conversus/SKILL.md` -- sections/lines cited: L13, L19, L28-78, L28-196, L51-56, L87-91, L210-241, L243-271, L260-271, L273-327, L286-298, L290-291, L296-297, L358-598, L397, L488-495, L670-697, L688, L704-719, L716, L1-734
- `/Users/brettkellgren/Sites/conversus/specs/007-game-engine/spec.md` -- sections/lines cited: L47, L62-70, L96-112, L131-157, L138-146, L166-177, L206-211, L392-406, L509-597, L566-587
