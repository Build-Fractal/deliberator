# Feature Specification: Conversus Adoption Harness

**Feature Branch**: `011-adoption-harness`
**Created**: 2026-03-22
**Status**: Draft
**Input**: Derived from 5-agent cooperative deliberation — see `conversus/summary/final.md`

## User Scenarios & Testing *(mandatory)*

### User Story 1 — "Just Ask" Zero-Config Decision (Priority: P1)

A user with no technical knowledge asks a natural-language question and receives a structured, multi-perspective recommendation within 30 seconds, without installing anything or configuring any settings.

**Why this priority**: This is the atomic unit of value. Every distribution format depends on the "Just Ask" pipeline. If this experience is indistinguishable from asking a single LLM, the entire product premise fails.

**Independent Test**: Enter a question like "Should I lease or buy a car?" and receive a recommendation that includes visible agent disagreement, supporting arguments, and a quality indicator — structurally different from a single-model response.

**Acceptance Scenarios**:

1. **Given** a user enters "Should I use Redis or Postgres for caching?", **When** the system processes the question, **Then** the output contains: a headline recommendation, a summary with trade-offs, at least one substantive disagreement between agents with attributions, and quality indicators.
2. **Given** a user enters a vague question like "help me decide", **When** the system processes the question, **Then** the system responds with one focused clarification question (interactive mode) or a structured error listing what's missing (non-interactive mode).
3. **Given** a user enters "What stocks should I buy?", **When** the system runs a lightweight deliberation, **Then** the output passes the quality floor: (a) the synthesis contains at least one substantive disagreement, and (b) agent attributions are present. If the base 2-agent configuration fails these checks, a mini-cross-review (4 launches total) is used instead.

---

### User Story 2 — Developer MCP Integration (Priority: P1)

An AI-native engineer using Claude Code, Cursor, or VS Code adds conversus as an MCP server and invokes deliberations from within their editor without context-switching.

**Why this priority**: MCP reaches developers at the point of decision-making inside their tools. This is the primary developer distribution path and validates the engine before broader distribution.

**Independent Test**: Install the MCP server, invoke `conversus_run` with a YAML config from within Claude Code, and receive a complete deliberation output. Then invoke `conversus_decide` with a natural-language question and receive a quality-validated recommendation.

**Acceptance Scenarios**:

1. **Given** a developer has the MCP server configured, **When** they invoke `conversus_run` with a valid YAML config, **Then** a complete deliberation executes and returns structured output.
2. **Given** a developer invokes `conversus_decide` with a question, **When** the quality floor has been validated, **Then** the tool returns a structured recommendation with quality indicators, debate transcript, and headline.
3. **Given** the quality floor has NOT been validated for `conversus_decide`, **When** a developer tries to invoke it, **Then** the tool is unavailable with a clear message explaining the prerequisite.
4. **Given** a developer invokes `conversus_validate` with a YAML config, **Then** the system parses, resolves presets, validates templates, and returns cost/token estimates without executing.

---

### User Story 3 — Claude Code Skill Prototype (Priority: P1)

A Claude Code user invokes "Just Ask" as a skill within their current session, receiving a multi-perspective recommendation without leaving their workflow.

**Why this priority**: This is the fastest path to real users and validates the "Just Ask" pipeline before engine extraction. The prototype generates configuration and formats output on top of existing SKILL.md orchestration — no new orchestration logic.

**Independent Test**: Invoke the skill with a natural-language question and receive a formatted recommendation that passes the quality floor.

**Acceptance Scenarios**:

1. **Given** a user invokes the Just Ask skill with "Should I use a monorepo or polyrepo?", **When** the skill processes the request, **Then** it generates a conversus config, runs the deliberation via existing SKILL.md, and returns a formatted recommendation.
2. **Given** the prototype has been used for 50+ runs, **When** the adoption gates are evaluated, **Then** the system reports trust rate, return rate, and sharing metrics to inform the next distribution phase.

---

### User Story 4 — Consumer Web Validation (Priority: P2)

A non-technical user visits a hosted web page, enters their AI provider API key, types a decision question, and receives a multi-perspective recommendation without creating an account or installing software.

**Why this priority**: Consumers are the largest addressable market. Without a consumer-accessible channel, consumer demand cannot be measured — developer-only channels structurally exclude non-technical users from demonstrating interest.

**Independent Test**: Visit the hosted form, enter a valid API key, type "Should I take the job offer or stay at my current company?", and receive a clear recommendation with visible disagreement, supporting arguments, and a shareable link.

**Acceptance Scenarios**:

1. **Given** a non-technical user visits the hosted form and provides a valid API key, **When** they enter a decision question and submit, **Then** they receive a recommendation within 30 seconds, presented with progressive disclosure (headline first, expandable details).
2. **Given** a user receives a recommendation, **When** they click "Share", **Then** a self-contained link is generated that renders the full recommendation without requiring the recipient to log in.
3. **Given** 50+ developer runs have passed the quality floor, **When** the minimal web form is launched, **Then** consumer-specific adoption metrics (task completion rate, perceived value) are tracked separately from developer metrics.

---

### User Story 5 — Programmatic SDK Access (Priority: P2)

A developer uses the Python SDK to compose and execute deliberations programmatically in their application, CI/CD pipeline, or automation workflow.

**Why this priority**: Enables programmatic integration, CI/CD pipelines, and custom tooling. The SDK's type system and output contract inform all other distribution formats.

**Independent Test**: Import the SDK, create a Deliberation with a config object, execute it, and receive a typed Result with all expected fields.

**Acceptance Scenarios**:

1. **Given** a developer creates a Deliberation object, **When** they call execute(), **Then** they receive a typed Result containing headline, summary, full_analysis, quality_indicators, and debate_transcript.
2. **Given** a developer calls validate(), **When** the config is invalid, **Then** a structured error identifies the specific validation failure.
3. **Given** a developer uses the SDK in CI/CD, **When** the deliberation runs in non-interactive mode, **Then** vague questions return structured errors (not conversational clarification), and the process exits with appropriate codes.

---

### User Story 6 — CLI Execution (Priority: P3)

A developer runs deliberations from the command line without requiring an MCP-compatible editor.

**Why this priority**: Convenience wrapper for developers who prefer terminal workflows. Ships after MCP since MCP reaches more developers at the decision point.

**Independent Test**: Run `conversus run config.yml` and receive a complete deliberation. Run `conversus decide "question"` and receive a recommendation.

**Acceptance Scenarios**:

1. **Given** a developer runs `conversus run config.yml`, **When** the config is valid, **Then** a complete deliberation executes with streaming progress output.
2. **Given** a developer runs `conversus validate config.yml`, **When** the command completes, **Then** it reports validation results and cost estimates without executing.

---

### Edge Cases

- What happens when all agents agree on everything? The quality floor structurally checks whether agents recommend different options or reach opposing conclusions on at least one dimension. If the 2-agent configuration produces no such disagreement, the system escalates to a mini-cross-review (4 launches).
- What happens when a single agent fails during parallel dispatch? The system continues with N-1 agents (default behavior). The failure is reported in quality indicators. Abort-phase is available as a configurable alternative.
- What happens when the user's question is adversarial or instruction-like? The question classifier distinguishes adversarial prompt injection from naive instruction-like phrasing and handles each appropriately.
- What happens when the chosen model lacks required capabilities? The capability validation layer checks model output after generation and fails with a structured error identifying the specific gap.
- What happens when a consumer asks a question requiring domain expertise? For v1, all questions use general-purpose presets. After 200-500 real queries, top categories are identified and domain-specific presets are created.

## Requirements *(mandatory)*

### Functional Requirements

**Quality Model**

- **FR-001**: System MUST define two binary pre-ship quality gates for "Just Ask" output: (a) the synthesis contains at least one substantive disagreement between agents — defined as agents recommending different options or reaching opposing conclusions on at least one dimension (structural check, no LLM judge required), (b) the output includes agent attributions.
- **FR-002**: System MUST implement a mini-cross-review pipeline (2 agents + 1 combined cross-review + 1 synthesis = 4 launches) as the fallback when the base 2-agent configuration fails quality gates.
- **FR-003**: System MUST include at least one worked side-by-side example comparing single-model vs. conversus output for the same question, demonstrating structural differentiation.
- **FR-004**: Quality gates MUST block shipping — if checks fail, the "Just Ask" feature does not ship until the pipeline is adjusted.

**Engine Architecture**

- **FR-005**: Engine extraction MUST be decomposed into 5 independently testable sub-phases: (a) config parser + validator, (b) template engine + linter integration, (c) async dispatch engine with phase barriers, (d) dispute parsing subsystem, (e) output manager with round-directory lifecycle.
- **FR-006**: The target architecture MUST be Python extraction. A time-boxed SKILL.md prototype validates the product concept before extraction begins.
- **FR-007**: The engine MUST produce template-conformant markdown as the canonical output artifact with machine-extractable fields: headline, summary, full_analysis, quality_indicators, debate_transcript.
- **FR-008**: The quality_indicators object MUST replace the confidence float, containing structural facts: agent_count, mode, phases_completed, cross_reviews_performed, genuine_disagreements_surfaced, genuine_disagreements_surviving. Consumer-facing labels MUST be derived from documented rules on these indicators.
- **FR-009**: The engine MUST include a question classifier capability: interactive mode triggers one clarification question; non-interactive mode returns a structured error listing missing fields.
- **FR-010**: The engine MUST emit streaming phase-lifecycle events: PHASE_STARTED, AGENT_DISPATCHED, AGENT_COMPLETED, PHASE_COMPLETED.
- **FR-011**: The engine MUST NOT assume filesystem-only storage — output and events must be consumable by web, CLI, MCP, and SDK channels.

**Distribution**

- **FR-012**: The Claude Code skill prototype MUST be implemented as config-generation-plus-output-formatting over existing SKILL.md execution, with no new orchestration logic. The prototype sunsets after 50+ runs and adoption metrics (trust rate, return rate, sharing behavior) are collected per FR-024 — at which point the skill transitions to the extracted Python engine.
- **FR-013**: The MCP server MUST ship before the standalone CLI in the build order.
- **FR-014**: `conversus_run` MUST ship with or before quality model validation. `conversus_decide` MUST ship only after the quality floor is validated.
- **FR-015**: Each MCP tool MUST have defined input schema, output schema, error types, and execution model.
- **FR-016**: A minimal hosted web form (single page, text input, BYOK API key entry, no history) MUST ship after developer validation (50+ Just Ask runs). Users MUST provide their own AI provider API key (OpenAI, Anthropic, or compatible provider) to submit questions. The form includes share page rendering.
- **FR-017**: The full web app MUST be removed from this spec's scope and addressed in a separate spec, gated behind consumer validation data from the minimal form.
- **FR-018**: The spec MUST use dual-primary integration path labels: "Primary Developer Integration Path" (MCP Server) and "Primary Consumer Integration Path" (Web App / Hosted Form).

**Model Abstraction**

- **FR-019**: The model abstraction MUST use two layers: a ModelProvider (with tool use, structured output, and schema support) and a capability validation layer that checks output structural requirements after generation.
- **FR-020**: The ModelProvider interface MUST include per-phase model routing from day one (initial implementation uses a single model as default; the interface permits routing).
- **FR-021**: The async dispatch engine MUST specify failure semantics: default continue-with-N-1 behavior (configurable to abort-phase), per-agent error isolation, and failure mode taxonomy. The v1 concurrency model is single-threaded per request — one deliberation at a time per user/session, with queuing for concurrent requests.

**Output & Rendering**

- **FR-022**: Each distribution channel MUST render the canonical output for its audience: progressive disclosure for web, concise + expandable for CLI, typed Result dataclass for SDK, structured JSON for MCP.
- **FR-023**: The output MUST include visible deliberation transparency — agent attributions, disagreement summaries, and trade-off analysis — as the primary differentiator from single-model responses.

**Adoption & Validation**

- **FR-024**: Developer adoption gates MUST be measured after 50 Just Ask runs: trust rate, return rate, sharing behavior.
- **FR-025**: Consumer adoption gates MUST use the minimal web form with consumer-specific metrics: task completion rate, perceived value. Neither population's data evaluates the other's demand.
- **FR-026**: The system MUST ship with 20 seed presets: 12-13 developer/professional scenarios plus 7-8 consumer scenarios, all first-party and curated.

**Backward Compatibility**

- **FR-027**: Existing `/conversus run` behavior MUST NOT be broken by any changes.
- **FR-028**: Power-user workflows (hand-crafted YAML, full control) MUST remain fully functional.

### Key Entities

- **Deliberation**: A complete multi-agent decision-making session, from question input through synthesis output.
- **Agent**: A perspective-bearing participant defined by an identity prompt and optional documentation. May be auto-generated or user-specified.
- **Preset**: A reusable agent identity template with prompt, documentation references, and composability rules.
- **Quality Indicators**: A structured object describing what the deliberation did — the basis for consumer-facing confidence labels.
- **Output Contract**: The canonical output format that all distribution channels render from.
- **Question Classifier**: An engine component that evaluates input sufficiency and triggers clarification or structured errors.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can go from zero to first recommendation in under 60 seconds with zero configuration via any channel.
- **SC-002**: 100% of Just Ask outputs pass the quality floor: at least one substantive disagreement and agent attributions present.
- **SC-003**: The worked side-by-side example demonstrates at least 3 structural differences between single-model and conversus output.
- **SC-004**: 50+ developer runs of the Claude Code skill prototype completed, with adoption gate metrics (trust, return, sharing) collected.
- **SC-005**: Consumer validation via minimal web form reaches 25+ non-technical users with task completion and perceived value metrics collected.
- **SC-006**: All 5 engine sub-phases pass independent testing before integration.
- **SC-007**: MCP server ships with complete input/output schemas for all tools, validated against at least 2 MCP-compatible editors.
- **SC-008**: Existing `/conversus run` behavior passes all current tests with zero regressions.
- **SC-009**: The system supports at least 2 model providers with capability validation preventing silent degradation.
- **SC-010**: 20 seed presets produce quality-passing deliberations on representative questions.

## Clarifications

### Session 2026-03-22

- Q: What is the data handling / privacy posture for v1? → A: No special handling — questions sent to LLM providers per their default policies.
- Q: What abuse prevention strategy for the public web form? → A: BYOK — users must provide their own AI provider API key (or OpenAI/Claude subscription). No operator-funded LLM calls.
- Q: How is "substantive disagreement" operationally defined for quality gates? → A: Agents must recommend different options or reach opposing conclusions on at least one dimension.
- Q: What triggers the SKILL.md prototype sunset? → A: Adoption-gated — sunsets after 50+ runs and adoption metrics (trust, return, sharing) collected per FR-024.
- Q: What is the concurrency model for v1? → A: Single-threaded per request — one deliberation at a time per user/session; requests queue if concurrent.

## Assumptions

- MCP is mature enough for production distribution (deployed across Claude Code, Cursor, Windsurf, Zed, VS Code).
- The existing SKILL.md orchestration supports a config-generation-only Just Ask prototype without new orchestration logic.
- A 2-agent configuration with mini-cross-review (4 launches) produces output meaningfully different from a single-model response — validated by the worked example before shipping.
- LiteLLM provides adequate model routing for the initial implementation, supplemented by a custom capability validation layer.
- The minimal web form is days of work, not weeks — a single page with API key entry, text input, and API call.
- All distribution channels use a BYOK (Bring Your Own Key) model — users provide their own AI provider API key. No operator-funded LLM calls. This eliminates abuse/cost concerns and means API keys are handled client-side (never stored server-side).
- V1 concurrency is single-threaded per request — one deliberation per user/session at a time. Concurrent requests queue. This is sufficient given BYOK (LLM API calls are the bottleneck, not engine throughput).
- Community preset contributions are deferred to a later phase; v1 uses curated first-party presets only.
- Data handling for v1 follows LLM provider default policies — no additional privacy layer, server-side storage, or consent flow. User questions are passed directly to model providers without intermediary logging or retention.

## Deliberation Source

This specification was derived from a 5-agent cooperative conversus deliberation:
- **50 recommendations proposed** across 5 agents
- **1 withdrawn**, **33 modified**, **16 surviving**, **10 new** recommendations after cross-review
- **5 unanimous convergence points** drove P1 requirements
- **8 disputes resolved** by the neutral synthesizer
- Full deliberation record: `specs/011-adoption-harness/conversus/`
- Synthesis: `specs/011-adoption-harness/conversus/summary/final.md`
