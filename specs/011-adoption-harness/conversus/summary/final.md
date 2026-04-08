# Neutral Synthesis: Conversus Adoption Harness (Spec 011)

---

### Process Summary

- **Agents**: 5 -- consumer-advocate, devex-advocate, architect, adoption-strategist, devils-advocate
- **Total artifacts**: 35
- **Phase 1 reviews**: 5
- **Phase 2 cross-reviews**: 20
- **Phase 3 revisions**: 5
- **Phase 4 disputes**: 5
- **Recommendations proposed** (Phase 1 total): 50 (10 per agent)
- **Recommendations withdrawn** (Phase 3): 1 (architect withdrew scenario replay MCP tool)
- **Recommendations modified** (Phase 3): 33
- **Recommendations surviving** (Phase 3): 16
- **New recommendations added** (Phase 3): 10 (consumer-advocate: 2, devex-advocate: 2, architect: 2, adoption-strategist: 2, devils-advocate: 2)
- **Disputes remaining** (Phase 4): 12 (consumer-advocate: 3, devex-advocate: 3, architect: 3, adoption-strategist: 3, devils-advocate: 3)
- **Convergence points** (Phase 4): 27 (consumer-advocate: 5, devex-advocate: 5, architect: 5, adoption-strategist: 6, devils-advocate: 6)

---

### Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| 1 | consumer-advocate | Elevate web-app priority | P1 | Modified | architect, adoption-strategist, devils-advocate, devex-advocate | Majority | Accepted-Modified |
| 2 | consumer-advocate | Specify vague-question handling | P1 | Surviving | None (universally endorsed) | Unanimous | Accepted |
| 3 | consumer-advocate | Add example questions to landing page | P1 | Modified | devils-advocate, adoption-strategist | Bilateral | Accepted-Modified |
| 4 | consumer-advocate | Design progressive result disclosure | P1 | Modified | devex-advocate, architect, devils-advocate | Unanimous | Accepted-Modified |
| 5 | consumer-advocate | Add confidence indicator | P2 | Modified | devex-advocate | Majority | Disputed |
| 6 | consumer-advocate | Declare dual-primary integration paths | P2 | Surviving | devils-advocate, architect (silence), adoption-strategist | Bilateral | Disputed |
| 7 | consumer-advocate | Add mobile-first requirement | P2 | Modified | adoption-strategist | Bilateral | Accepted-Modified |
| 8 | consumer-advocate | Self-contained share page experience | P2 | Modified | adoption-strategist | Majority | Accepted-Modified |
| 9 | consumer-advocate | Consumer domain routing | P3 | Modified | adoption-strategist, devils-advocate, devex-advocate | Majority | Accepted-Modified |
| 10 | consumer-advocate | Result quality feedback mechanism | P3 | Surviving | None | Bilateral | Accepted |
| 11 | devex-advocate | Define SDK public API | P1 | Modified | architect, devils-advocate, adoption-strategist | Majority | Disputed |
| 12 | devex-advocate | Add structured output mode | P1 | Modified | devils-advocate, consumer-advocate, adoption-strategist, architect | Unanimous | Accepted-Modified |
| 13 | devex-advocate | Move MCP server to build step 3 | P1 | Modified | architect, devils-advocate, adoption-strategist, consumer-advocate | Majority | Disputed |
| 14 | devex-advocate | Design CI/CD non-interactive mode | P1 | Modified | architect, adoption-strategist | Majority | Accepted-Modified |
| 15 | devex-advocate | Specify MCP tool input/output schemas | P2 | Surviving | None (universally endorsed) | Unanimous | Accepted |
| 16 | devex-advocate | Add dry-run/validate command | P2 | Surviving | None | Bilateral | Accepted |
| 17 | devex-advocate | Expose preset system programmatically | P2 | Modified | devils-advocate, adoption-strategist, architect | Majority | Accepted-Modified |
| 18 | devex-advocate | Resolve LiteLLM vs custom provider | P2 | Modified | architect, devils-advocate | Majority | Accepted-Modified |
| 19 | devex-advocate | Add config builder pattern to SDK | P3 | Surviving | adoption-strategist (timing) | Bilateral | Accepted |
| 20 | devex-advocate | Specify plugin/extension hook | P3 | Surviving | None | None | Accepted |
| 21 | architect | Define engine interfaces first (Phase 0) | P1 | Modified | devex-advocate, adoption-strategist, devils-advocate | Majority | Disputed |
| 22 | architect | Decompose engine extraction | P1 | Surviving | None (zero challenges) | Unanimous | Accepted |
| 23 | architect | Design async dispatch engine | P1 | Modified | devils-advocate, devex-advocate | Majority | Accepted-Modified |
| 24 | architect | Defer web app to v2 | P1 | Modified | consumer-advocate, adoption-strategist, devils-advocate | Unanimous | Accepted-Modified |
| 25 | architect | Address LiteLLM tool-use gap | P2 | Modified | devils-advocate, devex-advocate | Majority | Accepted-Modified |
| 26 | architect | Add scenario replay to MCP tools | P2 | Withdrawn | adoption-strategist | N/A | Rejected |
| 27 | architect | Resolve SKILL.md vs engine coexistence | P2 | Modified | adoption-strategist, devils-advocate | Majority | Accepted-Modified |
| 28 | architect | Specify output contract for Just Ask | P2 | Modified | consumer-advocate, devex-advocate, devils-advocate, adoption-strategist | Unanimous | Accepted-Modified |
| 29 | architect | Define minimum viable extraction | P3 | Modified | adoption-strategist | Majority | Accepted-Modified |
| 30 | architect | Align model tiering with provider abstraction | P3 | Modified | devils-advocate, consumer-advocate | Bilateral | Disputed |
| 31 | adoption-strategist | Ship Just Ask as Claude Code skill first | P1 | Modified | architect, devils-advocate, devex-advocate | Majority | Disputed |
| 32 | adoption-strategist | Define adoption gates | P1 | Modified | consumer-advocate, devex-advocate | Majority | Accepted-Modified |
| 33 | adoption-strategist | Add "see the debate" to output | P1 | Modified | devils-advocate, consumer-advocate | Majority | Accepted-Modified |
| 34 | adoption-strategist | Reorder MCP before CLI | P2 | Surviving | None | Majority | Accepted |
| 35 | adoption-strategist | Seed 20 community presets | P2 | Modified | consumer-advocate, devils-advocate | Majority | Accepted-Modified |
| 36 | adoption-strategist | Resolve open-source strategy | P2 | Surviving | None | None | Accepted |
| 37 | adoption-strategist | Build sharing mechanism | P2 | Modified | consumer-advocate | Majority | Accepted-Modified |
| 38 | adoption-strategist | Cut web app from roadmap | P2 | Modified | consumer-advocate, devils-advocate | Unanimous | Accepted-Modified |
| 39 | adoption-strategist | Answer "Why not ChatGPT?" in output | P3 | Modified | devils-advocate, consumer-advocate | Majority | Accepted-Modified |
| 40 | adoption-strategist | Address MCP maturity with fallback | P3 | Modified | devex-advocate | Majority | Accepted-Modified |
| 41 | devils-advocate | Define deliberation quality criteria | P1 | Surviving | None (universally endorsed) | Unanimous | Accepted |
| 42 | devils-advocate | Add model capability requirements | P1 | Modified | architect, devex-advocate, consumer-advocate | Majority | Accepted-Modified |
| 43 | devils-advocate | Design cross-review bypass for lightweight mode | P1 | Surviving | None (reinforced by all) | Majority | Accepted |
| 44 | devils-advocate | Add cost estimation and budget controls | P1 | Modified | consumer-advocate, adoption-strategist, architect | Majority | Accepted-Modified |
| 45 | devils-advocate | Resolve engine extraction question | P1 | Modified | adoption-strategist, architect | Majority | Disputed |
| 46 | devils-advocate | Add failure mode analysis | P2 | Modified | architect | Majority | Accepted-Modified |
| 47 | devils-advocate | Separate web app into own spec | P2 | Modified | consumer-advocate, adoption-strategist, architect | Unanimous | Accepted-Modified |
| 48 | devils-advocate | Define agent auto-generation concretely | P2 | Modified | adoption-strategist, devex-advocate | Majority | Accepted-Modified |
| 49 | devils-advocate | Address "ChatGPT wrapper" risk | P2 | Surviving | None (endorsed by all) | Majority | Disputed |
| 50 | devils-advocate | Define MCP tool contract precisely | P3 | Modified | adoption-strategist | Majority | Accepted-Modified |
| N1 | consumer-advocate | Adopt deliberation quality criteria for Just Ask | P1 | New | N/A | Unanimous | Accepted |
| N2 | consumer-advocate | Design engine API with web consumption as first-class input | P1 | New | N/A | Unanimous | Accepted |
| N3 | devex-advocate | Define Just Ask quality model before output schema | P1 | New | N/A | Unanimous | Accepted |
| N4 | devex-advocate | Gate web app behind adoption metric | P2 | New | N/A | Majority | Accepted |
| N5 | architect | Add question classifier protocol | P2 | New | N/A | Unanimous | Accepted |
| N6 | architect | Add engine event model | P2 | New | N/A | Majority | Accepted |
| N7 | adoption-strategist | Define Just Ask quality floor | P1 | New | N/A | Unanimous | Accepted |
| N8 | adoption-strategist | Design output format for dual audiences | P1 | New | N/A | Unanimous | Accepted |
| N9 | devils-advocate | Gate Just Ask prototype on minimum quality bar | P1 | New | N/A | Unanimous | Accepted |
| N10 | devils-advocate | Design engine API with streaming phase-lifecycle events | P2 | New | N/A | Majority | Accepted |

---

### Dangerous Contradictions Found

**Resolved Contradictions:**

1. **Web app priority: elevate vs. cut vs. defer**
   - Consumer-advocate wanted web app at step 4-5; architect and adoption-strategist wanted it removed; devils-advocate wanted separate spec.
   - Resolution: Consumer-advocate conceded full web app is too large for this spec (revision, Modified Recommendation 1). Adoption-strategist conceded "cut entirely" was wrong because it creates a self-fulfilling prophecy for consumer demand (revision, Modified Recommendation 8). All agents converged on: full web app removed from scope, engine designed with web-compatible constraints from day one. Remaining dispute is narrower -- whether a minimal web form is in-scope (see Remaining Disputes).

2. **Structured JSON vs. plain-English output as default**
   - Devex-advocate wanted JSON as primary; consumer-advocate wanted prose as primary; architect wanted template-conformant markdown.
   - Resolution: All three agents conceded their format was not "primary" but a rendering. The canonical output is template-conformant markdown (architect's position). Structured JSON (devex-advocate) and progressive disclosure prose (consumer-advocate) are both first-class renderings. Adoption-strategist formulated the unifying principle: "same data, different renderings" (revision, New Recommendation 2).

3. **"Just Ask" as CLI-first vs. web-native**
   - Consumer-advocate wanted web-native design first; devex-advocate wanted headless engine; adoption-strategist wanted Claude Code skill.
   - Resolution: Consumer-advocate conceded the engine should be headless (revision, New Recommendation 2). Devex-advocate conceded the engine API must be shaped by consumer UX requirements, not just SDK ergonomics (revision, Recommendation 3 cross-review response). Both accepted: engine is headless, but its API contract includes streaming events, clarification flow, and progressive-disclosure-compatible fields as first-class design inputs.

4. **Lightweight deliberation: adequate vs. degraded**
   - Consumer-advocate endorsed 2-agent, 1-round as "correct for consumer use cases." Devils-advocate argued it is "structurally identical to asking two models and having a third summarize."
   - Resolution: Consumer-advocate conceded the blind spot (revision, New Recommendation 1): "I was optimizing for consumer UX without ensuring the underlying output is worth presenting." All agents converged on the mini-cross-review (2 agents + 1 combined cross-review prompt + 1 synthesis = 4 launches) as the compromise that preserves adversarial pressure while keeping costs within consumer tolerance.

5. **SKILL.md: living distribution format vs. frozen legacy**
   - Adoption-strategist wanted to build new features into SKILL.md. Architect wanted it frozen or converted to thin adapter.
   - Resolution: Architect proposed (cross-review of adoption-strategist, Dangerous Contradictions item 2) and adoption-strategist accepted: Just Ask is built as config-generation-plus-output-formatting on top of existing SKILL.md orchestration, not as new orchestration logic within SKILL.md. This preserves portability and prevents divergence.

**Unresolved Contradictions:**

1. **Confidence representation: float vs. quality indicators**
   - Consumer-advocate and adoption-strategist want a numeric float (0-1) mapped to qualitative labels via bucket boundaries. Devex-advocate wants the float removed entirely, replaced by a `quality_indicators` object (structural facts about what the deliberation did), with labels derived from rules rather than numeric mapping.
   - Assessment: The devex-advocate's position is stronger. The float requires calibration that no mechanism in the proposal supports. A `confidence: 0.72` value from an uncalibrated system is misleading, and developers will build CI/CD gates on it. The consumer-advocate's need for qualitative labels is fully satisfied by rule-based derivation from structural indicators. The adoption-strategist's "quantitative metadata" requirement is satisfied by the indicators object. No functionality is lost by removing the float; risk is reduced.

2. **Phase 0 timing relative to Just Ask prototype**
   - Architect insists Phase 0 (1 week) must precede any shipping. Adoption-strategist insists Just Ask must ship before Phase 0 completes, with only a lightweight output contract (2-3 days) as prerequisite.
   - Assessment: Neither position is clearly stronger. Both agents' underlying concerns are legitimate -- the architect is right that interfaces designed without the full context will need costly retrofitting, and the adoption-strategist is right that designing in a vacuum produces wrong interfaces. The compromise both agents gesture toward -- Phase 0 runs in parallel with Just Ask design work, with the output contract as a Phase 0 deliverable -- is the viable resolution.

3. **Engine extraction: commit now vs. evaluate in Phase 0**
   - Devils-advocate wants the spec to commit to Python extraction as the target architecture immediately, citing spec 007's Python-only plugin system as decisive evidence. Architect wants the commitment deferred to after Phase 0 demonstrates the requirement.
   - Assessment: The devils-advocate's position is stronger. The architect's own evidence (spec 007's lifecycle hooks, `DeliberationState`, and feature extraction are Python constructs) already answers the evaluation question. Deferring a decided question to Phase 0 creates ambiguity without producing new information. The architect's Phase 0 should proceed with the extraction commitment as context, not as a conclusion to be re-derived.

---

### Systemic Contradictions

- **Speed-to-Users vs. Foundation-First**
  - **Manifests in**: Phase 0 timing dispute (architect vs. adoption-strategist), SDK design before shipping dispute (devex-advocate vs. adoption-strategist), quality criteria as gate vs. iteration target (devils-advocate vs. adoption-strategist), MCP prerequisites dispute (devex-advocate vs. adoption-strategist).
  - **Root cause**: The proposal attempts to serve two masters simultaneously -- building a robust, extensible platform and validating product-market fit quickly. The adoption-strategist optimizes for learning velocity; the architect and devex-advocate optimize for cost-of-rework. The spec does not distinguish between "prototype-quality work that will be replaced" and "foundation-quality work that must endure," so every deliverable is debated as both.
  - **Implication for spec**: Explicitly designate each deliverable as either "prototype" (expected to be replaced; optimized for speed; ships with minimal design prerequisites) or "foundation" (expected to endure; optimized for correctness; requires interface design before implementation). The Just Ask Claude Code skill is a prototype. The Python engine, SDK types, and MCP tool contracts are foundations.

- **Consumer Invisibility in Developer Channels**
  - **Manifests in**: Minimal web form dispute (consumer-advocate/adoption-strategist vs. architect/devils-advocate), dual-primary label dispute (consumer-advocate vs. silence from architect/devils-advocate), adoption gate design (adoption-strategist's revised consumer-specific gates).
  - **Root cause**: The proposal declares a vision serving "everyone" but proposes a build order and validation methodology that can only reach developers. Non-technical users -- the largest addressable market per the proposal's own framing -- have no channel to try the product, no channel to demonstrate demand, and no label in the architecture declaring them a first-class audience. The spec's feedback loops are structurally incapable of detecting consumer demand.
  - **Implication for spec**: Either narrow the vision to "developer tool" (in which case consumer-facing language should be removed from the proposal) or commit to at least one consumer-accessible validation artifact with consumer-specific adoption metrics. The latter is the stronger choice, given the proposal's explicit naming of consumer use cases.

- **Quality Assurance Without Quality Infrastructure**
  - **Manifests in**: Confidence float calibration gap (devex-advocate dispute), quality criteria as pre-ship gate vs. post-ship target (devils-advocate dispute), model capability validation mechanisms (architect vs. devils-advocate approaches), the uncalibrated side-by-side differentiation question.
  - **Root cause**: The proposal assumes conversus output is better than single-model output but provides no mechanism to measure, validate, or enforce this assumption. Every agent built recommendations on this assumption. The devils-advocate is the only agent who challenged it directly, and the result was unanimous convergence on quality criteria -- but the criteria themselves are heuristic, not calibrated. The spec has no path from heuristic quality checks to validated quality measurement.
  - **Implication for spec**: Define quality as a first-class architectural concern, not just a checklist. Include: (1) the heuristic pre-ship gate (unanimously agreed), (2) a plan for collecting quality feedback data to enable future calibration, and (3) the side-by-side differentiation example as a spec-level validation artifact. Quality infrastructure is a distinct workstream that should appear in the build order.

- **Interface Contract Proliferation**
  - **Manifests in**: SDK API vs. engine interfaces (devex-advocate vs. architect), output contract vs. SDK Result type (adoption-strategist vs. devex-advocate), MCP tool contracts vs. SDK methods, template-conformant markdown vs. structured JSON vs. progressive disclosure layers.
  - **Root cause**: Five distribution formats (Claude Code skill, CLI, MCP, SDK, web app) each need their own interface contract, but all depend on the same engine. The proposal does not distinguish between the engine's internal state model, its canonical output format, and the per-channel rendering contracts. Each agent proposed interface specifications from their domain without acknowledging the layered architecture that must connect them.
  - **Implication for spec**: Define three explicit contract layers: (1) internal engine state (`DeliberationState`, `AgentState`, lifecycle hooks -- from spec 007), (2) canonical output format (template-conformant markdown with machine-parseable sections), (3) per-channel rendering contracts (SDK `Result` dataclass, MCP JSON schema, CLI text, web progressive disclosure). Each layer has its own design authority and change velocity.

- **Scope Ambition vs. Specification Depth**
  - **Manifests in**: The proposal covers 5 distribution formats, 3 user tiers, 8 build phases, and 8 open questions in 147 lines. Every agent identified underspecification in their domain. The web app is 9 lines covering 6 features. The MCP server is 6 tool names with no schemas. The SDK is one import statement.
  - **Root cause**: The document is a vision proposal operating as a technical specification. It has the breadth of a product brief but is being reviewed as an engineering plan. The mismatch means every agent found gaps, but the gaps are a feature of the document type, not a flaw in any specific section.
  - **Implication for spec**: Explicitly declare this as a "proposal" that produces child specs for each major component: engine extraction spec, MCP server spec, SDK spec, Just Ask mode spec, and (conditionally) web app spec. The proposal defines scope, sequencing, and constraints; the child specs define interfaces, schemas, and implementation details.

---

### Convergence Achieved

- **Deliberation quality criteria must be defined before shipping Just Ask** -- Strength: Unanimous
  - **Agreed recommendation**: Before the Just Ask prototype ships in any form, validate that its output passes two minimum quality checks: (1) the synthesis contains at least one substantive disagreement between agents, and (2) the output structurally differs from a single-model response (agent attributions present). If the 2-agent, 1-round configuration cannot meet these criteria, implement a mini-cross-review (agents respond to each other in a single combined prompt). Target launch configuration: 2 agents + 1 mini-cross-review + 1 synthesis = 4 launches.
  - **Supporting agents**: devils-advocate (revision, Recommendation 1; new recommendation "Gate Just Ask prototype on minimum quality bar"), consumer-advocate (revision, New Recommendation 1), devex-advocate (revision, New Recommendation 1), adoption-strategist (revision, New Recommendation 1), architect (revision, Recommendation 8 -- quality gate as priority 1 constraint).
  - **Evidence basis**: The devils-advocate demonstrated that a 2-agent, 1-round deliberation without cross-reviews is structurally identical to asking two models and having a third summarize (Off-Base Assumptions, item 2). The adoption-strategist conceded that "if the first 100 users' experience is indistinguishable from ChatGPT, the validation data does not say 'the product needs iteration' -- it says 'users tried it once and left'" (revision, New Recommendation rationale).
  - **Pre-existing or earned**: Earned. Only the devils-advocate raised this in Phase 1. Every other agent's Phase 1 review either endorsed the lightweight default without examining quality (consumer-advocate) or focused on output format rather than output quality (devex-advocate, architect). Convergence emerged through Phase 2 cross-reviews and was formalized in Phase 3 revisions.

- **Engine extraction must be decomposed into independently testable sub-phases** -- Strength: Unanimous
  - **Agreed recommendation**: Break engine extraction into 5 sub-phases: (a) config parser + validator, (b) template engine + linter integration, (c) async dispatch engine with phase barriers, (d) dispute parsing subsystem, (e) output manager with round-directory lifecycle. Each sub-phase has distinct inputs, outputs, and testability criteria.
  - **Supporting agents**: architect (revision, Recommendation 2 -- zero challenges received), all other agents endorsed in cross-reviews and revisions.
  - **Evidence basis**: SKILL.md contains 734 lines across 6 distinct subsystems. The architect mapped each sub-phase to specific SKILL.md line ranges. The adoption-strategist confirmed from the timeline perspective that a monolithic phase is unplannable.
  - **Pre-existing or earned**: Pre-existing. Agreed from Phase 1. The only recommendation in the entire deliberation that received zero challenges from any agent.

- **Full web app removed from scope; engine designed with web-compatible constraints** -- Strength: Unanimous
  - **Agreed recommendation**: Remove the full-featured web app (Next.js, FastAPI, WebSocket, PostgreSQL, auth, history) from this spec's build order. Address it in a separate spec (012 or later) gated behind adoption metrics. The engine must include web-app-compatible design requirements from day one: streaming phase-lifecycle events, structured output suitable for progressive rendering, and no assumption of filesystem-only storage.
  - **Supporting agents**: architect (revision, Recommendation 4), devils-advocate (revision, Recommendation 7), adoption-strategist (revision, Recommendation 8), devex-advocate (revision, New Recommendation 2), consumer-advocate (revision, Recommendation 1 -- accepts full web app removal, advocates minimal form).
  - **Evidence basis**: The web app adds 5+ orthogonal technology layers (architect), is the highest-cost highest-risk item (adoption-strategist), and has unvalidated demand from its target audience (adoption-strategist, consumer-advocate).
  - **Pre-existing or earned**: Earned. The consumer-advocate initially wanted the web app at step 4-5. Through cross-reviews, the consumer-advocate accepted scope reduction while extracting the crucial constraint that engine design must not calcify around CLI-only patterns.

- **Structured output with per-channel rendering** -- Strength: Unanimous
  - **Agreed recommendation**: The engine produces template-conformant markdown as the canonical artifact. This includes machine-extractable fields: headline/recommendation, summary/trade-offs, full analysis/debate transcript, quality indicators. Each distribution channel renders these fields for its audience: progressive disclosure for web, concise + expandable for CLI, typed `Result` dataclass for SDK, structured JSON for MCP. Neither structured data nor prose is derived from the other; both are renderings of the canonical output.
  - **Supporting agents**: consumer-advocate (revision, Recommendation 4), devex-advocate (revision, Recommendation 2), architect (revision, Recommendation 8), adoption-strategist (revision, New Recommendation 2). Devils-advocate does not contest the structure but prioritizes quality criteria over format.
  - **Evidence basis**: The adoption-strategist formulated the unifying principle: "same data, different renderings." The architect provided the canonical format (template-conformant markdown for ecosystem compatibility). The consumer-advocate provided the consumer rendering (progressive disclosure). The devex-advocate provided the developer rendering (typed dataclass).
  - **Pre-existing or earned**: Earned. In Phase 1, structured output, plain-English prose, and template-conformant markdown appeared as competing requirements. Cross-reviews revealed they are complementary layers.

- **Vague question handling as a shared engine capability** -- Strength: Unanimous
  - **Agreed recommendation**: The Just Ask pipeline must handle vague, ambiguous, or insufficient input. The engine includes a `QuestionClassifier` protocol or `NEEDS_CLARIFICATION` state: interactive mode triggers conversational clarification (one focused question), non-interactive mode returns a structured error with missing fields. The clarification step uses a cheap model and a single lightweight call.
  - **Supporting agents**: consumer-advocate (revision, Recommendation 2), architect (revision, New Recommendation 1 -- `QuestionClassifier` protocol), devex-advocate (revision, Recommendation 4 -- mode-dependent responses), devils-advocate (revision -- cost-control constraint).
  - **Evidence basis**: The decision framework already has `[CLARIFY: ...]` tags for vague input (spec 003, US-1, AC-5). Consumer users are the most likely to provide unclear input and the least equipped to fix it.
  - **Pre-existing or earned**: Pre-existing. The consumer-advocate proposed this in Phase 1, and it received zero challenges across all cross-reviews. Other agents added design constraints (mode-dependent responses, cost control, protocol-level definition) that refined without contesting it.

- **Claude Code skill prototype ships first, Python extraction follows** -- Strength: Majority (4 agents)
  - **Agreed recommendation**: Ship Just Ask as a Claude Code skill within the existing SKILL.md runtime for initial user validation. Implement as config-generation-plus-output-formatting (not new orchestration logic). Python extraction is committed as the target architecture but informed by prototype usage data. The prototype has a defined sunset.
  - **Supporting agents**: adoption-strategist (revision, Recommendation 1), architect (revision, Recommendations 7 and 9), devils-advocate (revision, Recommendation 5), devex-advocate (revision, Recommendation 1 -- accepts prototype as validation mechanism). Consumer-advocate focused on web channel rather than skill prototype sequencing.
  - **Evidence basis**: The adoption-strategist demonstrated that the existing runtime supports everything needed for Just Ask. The architect confirmed that config-generation-plus-formatting adds no new orchestration logic to SKILL.md.
  - **Pre-existing or earned**: Earned. In Phase 1, the adoption-strategist proposed this against resistance from the architect (who wanted interfaces first) and the devils-advocate (who wanted the extraction question resolved first). Cross-reviews produced the compromise: prototype in SKILL.md with config-generation constraint.

- **MCP before CLI in build order** -- Strength: Majority (4 agents)
  - **Agreed recommendation**: Reverse the proposal's build order (CLI at step 3, MCP at step 5). MCP reaches developers at the point of decision-making inside their editors. CLI is a convenience wrapper that ships after MCP.
  - **Supporting agents**: adoption-strategist (revision, Recommendation 4), devex-advocate (revision, Recommendation 3), devils-advocate (revision, Recommendation 10), architect (implicit -- did not contest).
  - **Evidence basis**: MCP is deployed across Claude Code, Cursor, Windsurf, Zed, and VS Code. CLI requires context-switching; MCP does not. The decision framework's commands map 1:1 to MCP tool signatures.
  - **Pre-existing or earned**: Pre-existing. Agreed from Phase 1 between adoption-strategist and devex-advocate. No agent produced a counter-argument for CLI-before-MCP.

- **Two-layer model abstraction (ModelProvider + capability validation)** -- Strength: Majority (3 agents)
  - **Agreed recommendation**: Two abstraction layers: (a) `ModelProvider` with signature `async def execute(messages, tools, output_schema, **kwargs) -> AgentOutput`, with LiteLLM as default implementation; (b) a capability validation layer that checks model output meets structural requirements. The original `async def complete(messages, **kwargs) -> str` signature was wrong.
  - **Supporting agents**: devex-advocate (revision, Recommendation 8 -- accepted architect's correction), architect (revision, Recommendation 5), devils-advocate (revision, Recommendation 2 -- converged on runtime validation over static catalog).
  - **Evidence basis**: The architect demonstrated that conversus agents require tool use, structured output, and template enforcement -- none of which a bare `-> str` return supports.
  - **Pre-existing or earned**: Earned. The devex-advocate's original interface was challenged by the architect in Phase 2. The devex-advocate explicitly conceded: "I was wrong about the method signature. The architect is right" (revision, Recommendation 8).

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

- **Dispute: Minimal web form in-scope for this spec**
  - **Positions**: Consumer-advocate and adoption-strategist argue a minimal hosted web form (single page, no auth, no history, no PostgreSQL) must be in this spec's scope as a consumer validation artifact. Architect and devils-advocate argue the consumer surface should remain an open question or be gated behind demand signals from developer channels.
    - Consumer-advocate (disputes, Dispute 1): "If the spec does not commit to at least a minimal consumer-accessible surface, it contradicts its own vision."
    - Adoption-strategist (disputes, Dispute 2): "Validating only through developer channels and concluding 'no consumer demand' is a methodological error."
    - Architect (revision, Recommendation 4): "evaluate lightweight alternatives (Slack bot, simple hosted form) alongside the engine work, rather than committing to a full web app prematurely."
    - Devils-advocate (revision, Recommendation 7): "define a quantitative adoption gate that triggers a dedicated web app spec."
  - **Arguments**: Consumer-advocate/adoption-strategist: A retiree or parent will never install a CLI or configure MCP. Measuring "demand from non-technical users via CLI/MCP channels" is structurally incoherent -- it asks non-technical users to demonstrate demand through channels they cannot access. A single-page web form is "days of work, not weeks." Architect/devils-advocate: The consumer surface adds scope risk. The engine should be designed with web consumption in mind, but committing to any specific consumer surface is premature before the engine exists.
  - **Synthesizer assessment**: The consumer-advocate and adoption-strategist have the stronger position. The adoption-strategist's self-fulfilling-prophecy argument is logically sound: if the only channels available are developer channels, the data will show only developer demand regardless of actual consumer interest. The architect's scope concern is valid for the full web app but does not apply to a single-page form. The devils-advocate's adoption gate ("measurable demand from non-technical users via CLI/MCP channels") is internally contradictory, as both the consumer-advocate and the adoption-strategist identified. The minimal web form is the cheapest possible resolution to a methodological flaw in the validation strategy.
  - **Recommended resolution**: Include a minimal hosted web form (single page, text input, API call, no auth, no history) as a committed deliverable in this spec, shipping after developer validation (Just Ask skill, 50+ runs). The form is the consumer validation artifact. The full web app is addressed in a separate spec (012) triggered by consumer validation data from the minimal form. The share page is included in the minimal form scope.

- **Dispute: Confidence representation -- float vs. quality indicators**
  - **Positions**: Consumer-advocate and adoption-strategist want a numeric float (0.0-1.0) derived from deliberation dynamics, with documented bucket boundaries mapping to qualitative labels. Devex-advocate wants the float removed entirely, replaced by a `quality_indicators` object containing structural facts.
    - Devex-advocate (disputes, Dispute 1): "A confidence float requires calibration... Without calibration, a float is a fiction that looks authoritative."
    - Consumer-advocate (revision, Recommendation 5): "Confidence is a float (0.0-1.0) in the engine output... Documented, configurable bucket boundaries map the float to consumer labels."
    - Adoption-strategist (disputes, Convergence item 6): "the output must include both a machine-readable confidence signal and a human-readable confidence label."
  - **Arguments**: Devex-advocate: Calibrating a confidence score requires thousands of validated decisions with ground-truth outcomes. No such process exists. Developers will build CI/CD gates on uncalibrated numbers. Quality indicators (booleans and structural facts) are honest and verifiable. Consumer-advocate/adoption-strategist: Consumers need a plain-language signal; documented bucket boundaries ensure consistency.
  - **Synthesizer assessment**: The devex-advocate's position is stronger on the calibration point. A `confidence: 0.72` value from an uncalibrated system is misleading, and the devils-advocate's quality criteria convergence reinforces this -- confidence from a shallow deliberation is meaningless. However, the consumer-advocate's need for qualitative labels is legitimate and can be met without a numeric float.
  - **Recommended resolution**: Replace the confidence float with a `quality_indicators` object: `{ agent_count, mode, phases_completed, cross_reviews_performed, genuine_disagreements_surfaced, genuine_disagreements_surviving }`. Derive consumer-facing labels from documented rules on these indicators (e.g., cross-reviews performed AND disagreements surviving > 0 = "Strong recommendation"). If calibration data later supports a true confidence score, add it as an optional field. This satisfies all parties' functional requirements while eliminating the calibration problem.

- **Dispute: Phase 0 timing relative to Just Ask prototype**
  - **Positions**: Architect wants Phase 0 (internal + external interface definition, 1 week) to precede any shipping. Adoption-strategist wants Just Ask to ship before Phase 0 completes, with only a lightweight output contract (2-3 days) as prerequisite. Devex-advocate wants SDK types designed before prototype ships.
    - Architect (disputes, Dispute 1): "The difference between '2-3 days of output contract' and '1 week of Phase 0' is 2-4 days. The cost of getting the interfaces wrong and retrofitting is months."
    - Adoption-strategist (disputes, Dispute 1): "Requiring the full SDK type system before shipping a thin SKILL.md wrapper conflates two different deliverables."
    - Devex-advocate (disputes, Dispute 2): "The adoption-strategist's 'output contract' and my 'SDK Result type' should be the same document."
  - **Arguments**: Architect: Phase 0 costs 1 week and prevents months of rework. The adoption-strategist's output contract is a subset of Phase 0 work. Adoption-strategist: The Just Ask skill is config-generation-plus-formatting -- a thin wrapper that does not need the full type system. Usage data should inform the SDK design. Devex-advocate: The output contract IS the SDK Result type -- the disagreement is naming, not substance.
  - **Synthesizer assessment**: Neither position is clearly stronger, but the devex-advocate's framing provides the resolution. The adoption-strategist's output contract and the devex-advocate's SDK Result type define the same fields. The architect's Phase 0 can run in parallel with Just Ask design work, with the output contract as a Phase 0 deliverable. The core question is whether shipping is blocked on Phase 0 completion.
  - **Recommended resolution**: Adopt a three-step sequence: (1) Define the Just Ask output contract / SDK Result type and quality floor (days of work -- this is a Phase 0 deliverable). (2) Ship the Just Ask Claude Code skill using this output contract. (3) Complete remaining Phase 0 work (engine internal interfaces, lifecycle hooks, mapping layer) in parallel, informed by early usage data. The output contract must be defined before shipping; the full internal interface definition need not be.

- **Dispute: MCP server prerequisites -- quality model required before `conversus_decide` ships**
  - **Positions**: Devex-advocate wants `conversus_decide` gated behind quality model validation. Adoption-strategist wants MCP development in parallel with skill validation, not sequentially gated.
    - Devex-advocate (disputes, Dispute 3): "If conversus_decide produces output indistinguishable from a single-model response, the MCP tool actively degrades the developer's workflow."
    - Adoption-strategist (disputes, Dispute 3): "MCP users and Claude Code skill users are the same developer population. Gating MCP behind skill validation creates unnecessary delay."
  - **Arguments**: Devex-advocate: MCP tools may be invoked programmatically by AI agents without human review, making quality more critical than for the interactive Claude Code skill. Adoption-strategist: Sequential gating delays MCP by months when both channels serve the same users.
  - **Synthesizer assessment**: The devex-advocate's distinction between `conversus_run` (user-specified configuration) and `conversus_decide` (system-level quality decisions) is sound. The risk profile genuinely differs. The adoption-strategist's parallel development concern is also valid.
  - **Recommended resolution**: Adopt the devils-advocate's two-tier approach (endorsed by the devex-advocate): `conversus_run` ships with or before quality model validation. `conversus_decide` ships only after the quality floor is validated. MCP server development begins in parallel with skill validation, starting with `conversus_run`. This preserves parallel development while ensuring the highest-risk tool has quality backing.

- **Dispute: Dual-primary integration path labels**
  - **Positions**: Consumer-advocate wants the spec to replace "Primary Integration Path" (currently labeling only MCP) with "Primary Developer Integration Path" and "Primary Consumer Integration Path." Architect and devils-advocate are silent on the label; adoption-strategist is compatible but does not explicitly endorse.
    - Consumer-advocate (disputes, Dispute 2): "Labels shape internal prioritization... If MCP is 'primary' and the web app is unlabeled, every scope cut will deprioritize the consumer path."
  - **Arguments**: Consumer-advocate: The label is zero-cost and high-signal. It prevents the consumer path from being permanently deprioritized. The proposal declares conversus for "everyone" but architecturally privileges developers. Opposing agents: Silence, not explicit disagreement.
  - **Synthesizer assessment**: The consumer-advocate's argument is straightforward and uncontested. No agent explicitly argued against dual-primary labeling. The silence from architect and devils-advocate appears to reflect indifference, not opposition.
  - **Recommended resolution**: Adopt the dual-primary labeling. Change "MCP Server (Primary Integration Path)" to "MCP Server (Primary Developer Integration Path)" and add "Web App / Hosted Form (Primary Consumer Integration Path)" with a note that the consumer path ships after initial developer validation but is architecturally primary. This is a wording change with zero engineering cost.

- **Dispute: Side-by-side differentiation example as spec-level gate**
  - **Positions**: Devils-advocate wants the spec to include a worked example comparing single-model vs. conversus output for the same question, as a gate on spec completion. Adoption-strategist frames it as a "marketing asset" rather than a design gate. Other agents do not explicitly address it.
    - Devils-advocate (disputes, Dispute 1): "If the assumption is false -- if a 2-agent, 1-round deliberation produces output that is functionally equivalent to asking Claude directly -- then every other recommendation in this deliberation is building on sand."
    - Adoption-strategist (revision, Recommendation 9): Includes a side-by-side example as a secondary addition, calling it "a design target and a marketing asset."
  - **Arguments**: Devils-advocate: The entire deliberation rests on an unvalidated assumption. An afternoon of work proves or disproves it. Adoption-strategist: The example is useful but should not gate engineering work.
  - **Synthesizer assessment**: The devils-advocate's argument is compelling. The assumption that conversus output is meaningfully better than single-model output is foundational and untested. The cost of testing is trivially small (an afternoon). The risk of not testing is building an entire product on an unvalidated premise.
  - **Recommended resolution**: Require the spec to include at least one worked example: a specific question answered by both a single LLM call and a conversus Just Ask deliberation, with structural annotations. This is a spec-completion requirement (P1), not an engineering gate -- it validates the design before implementation begins. If the example fails to show meaningful differentiation, the spec must document what pipeline changes (mini-cross-review, additional agents) are required.

- **Dispute: Engine extraction commitment -- now vs. Phase 0**
  - **Positions**: Devils-advocate wants the spec to commit to Python extraction as the target architecture immediately. Architect wants the commitment deferred to after Phase 0 evaluation.
    - Devils-advocate (disputes, Dispute 3): "Spec 007's plugin system is Python-only... The directional question is already answered."
    - Architect (revision, Recommendation 7): "The commitment to Python-as-canonical is made *after* the Phase 0 interface definition demonstrates that spec 007's plugin system requires a Python runtime."
  - **Arguments**: Devils-advocate: The architect's own evidence (spec 007 lifecycle hooks, `DeliberationState`, feature extraction are Python constructs) answers the question. Leaving it open creates ambiguity that slows dependent decisions. Architect: The interface definitions are approach-agnostic and Phase 0 should demonstrate the requirement rather than assume it.
  - **Synthesizer assessment**: The devils-advocate's position is stronger. The architect's evidence for Python extraction is already in the record and was not challenged by any agent. Phase 0 will not produce new information that changes this conclusion. The architect's "approach-agnostic" claim is technically true for type definitions but false for design decisions that depend on in-process vs. subprocess communication patterns.
  - **Recommended resolution**: The spec should commit: "The target architecture is Python extraction. Evidence: spec 007's Python-only plugin system. A time-boxed SKILL.md prototype validates the product concept before extraction begins. The prototype informs the extraction but does not replace it." Phase 0 proceeds with this commitment as context.

- **Dispute: Model tiering as architectural requirement vs. optimization**
  - **Positions**: Architect wants per-phase model configuration designed into the engine's provider abstraction from Phase 0. Devex-advocate places capability validation in the `AgentRuntime` layer as post-generation checking. Adoption-strategist does not address model tiering directly.
    - Architect (disputes, Dispute 3): "If the engine ships with single-model-only and model tiering is added later, the ModelProvider interface must change... which is a breaking API change."
  - **Arguments**: Architect: Model tiering determines quality ceiling per phase and must be in the interface from day one. Devex-advocate: Post-generation validation is the safety net; the interface can evolve. Adoption-strategist: Implicit deferral.
  - **Synthesizer assessment**: The architect's argument about preventing a breaking API change is sound. The cost of including per-phase model routing in the interface definition is negligible (the initial implementation uses a single model; the interface merely permits routing). The cost of excluding it and retrofitting is high.
  - **Recommended resolution**: Include per-phase model configuration in the `ModelProvider` interface definition during Phase 0. The initial implementation uses a single model for all phases (the `default` key), making tiering opt-in with zero implementation complexity. The interface supports it from day one.

- **Dispute: Quality floor as pre-ship gate vs. post-ship iteration target**
  - **Positions**: Devils-advocate insists the two quality checks must be hard gates -- shipping is blocked if they fail. Adoption-strategist and consumer-advocate frame them as "checks to define before shipping" without explicitly stating they gate shipping.
    - Devils-advocate (disputes, Dispute 2): "Defining checks without gating on them means the checks can be documented, acknowledged, and then shipped past."
    - Adoption-strategist (revision, New Recommendation 1): "These two checks are testable in 30 minutes against a handful of sample questions."
  - **Arguments**: Devils-advocate: First impressions are irreversible. The adoption-strategist's own argument about irreversible negative first impressions validates the gate framing. Adoption-strategist: The checks are fast enough to not meaningfully delay shipping.
  - **Synthesizer assessment**: This is largely a semantic dispute. Both agents agree on the same two checks and both agree they should be completed before shipping. The adoption-strategist already frames them as "before shipping." The devils-advocate wants explicit gate language. Given that both agents acknowledge first-impression damage is irreversible, the gate framing adds precision without adding cost.
  - **Recommended resolution**: Adopt the quality checks as explicit pre-ship gates. If the checks fail, shipping is blocked until the issue is resolved (e.g., by implementing the mini-cross-review). Given the checks are testable in 30 minutes, the gate adds at most a day of delay.
<!-- CONVERSUS:DISPUTES_END -->

---

### Actionable Spec Changes

**P1 -- Must implement** (blocking issues or unanimous convergence):

1. **Add deliberation quality criteria section with pre-ship gate**: Add a "Quality Model" section defining minimum quality criteria for Just Ask output. Two binary pre-ship gates: (a) the synthesis must contain at least one substantive disagreement between agents, (b) the output must include agent attributions. If the base 2-agent configuration fails these checks, implement a mini-cross-review (4 launches total). Include a worked side-by-side example comparing single-model vs. conversus output for the same question. Source: Recommendations #41, #43, #49, N1, N3, N7, N9; convergence point "Deliberation quality criteria."

2. **Decompose engine extraction into 5 sub-phases**: Replace the single "Python engine extraction" build phase with 5 independently testable sub-phases: (a) config parser + validator, (b) template engine + linter integration, (c) async dispatch engine with phase barriers, (d) dispute parsing subsystem, (e) output manager with round-directory lifecycle. Source: Recommendation #22; convergence point "Engine extraction decomposition."

3. **Define structured output format with per-channel rendering**: Add an output architecture section. The engine produces template-conformant markdown as the canonical artifact with machine-extractable fields: headline, summary, full_analysis, quality_indicators, debate_transcript. Replace the confidence float with a `quality_indicators` object. Define per-channel rendering: progressive disclosure for web, concise + expandable for CLI, typed `Result` dataclass for SDK, structured JSON for MCP. Source: Recommendations #4, #12, #28, #33, N8; convergence point "Structured output with per-channel rendering."

4. **Specify vague-question handling as engine capability**: Add a `QuestionClassifier` protocol or `NEEDS_CLARIFICATION` state to the engine's execution flow. Interactive mode triggers one clarification question; non-interactive mode returns a structured error. Clarification uses a cheap model. Source: Recommendation #2, N5; convergence point "Vague question handling."

5. **Commit to Python extraction as target architecture**: State in the spec: "The target architecture is Python extraction. A time-boxed SKILL.md prototype validates the product concept before extraction begins." Source: Recommendations #27, #45; convergence point "Python extraction as target."

6. **Remove full web app from scope; add engine web-compatibility constraints**: Remove the full web app (Next.js, FastAPI, WebSocket, PostgreSQL) from the build order. Add engine design constraints: streaming phase-lifecycle events (`DispatchEvent` type with `PHASE_STARTED`, `AGENT_DISPATCHED`, `AGENT_COMPLETED`, `PHASE_COMPLETED` events), structured output suitable for progressive rendering, no filesystem-only storage assumption. Source: Recommendations #24, #47, N2, N6, N10; convergence point "Full web app removed."

7. **Adopt dual-primary integration path labels**: Change "MCP Server (Primary Integration Path)" to "MCP Server (Primary Developer Integration Path)." Add "Web App / Hosted Form (Primary Consumer Integration Path)" with a note that it ships after developer validation. Source: Recommendation #6.

**P2 -- Should implement** (majority convergence or strong single-agent case):

1. **Reorder build sequence: MCP before CLI**: Reverse the proposal's build order. MCP server ships before the standalone CLI. `conversus_run` ships first (known behavior); `conversus_decide` ships after quality floor validation. Source: Recommendations #13, #34; convergence point "MCP before CLI."

2. **Design async dispatch engine with failure contract**: Add an architecture section specifying: `asyncio.TaskGroup` for parallel dispatch, `PhaseBarrier` abstraction, per-agent error isolation with default continue-with-N-1 behavior (configurable to abort), phase-lifecycle event emission, and failure mode taxonomy for single-provider case. Source: Recommendations #23, #46; convergence point on dispatch engine across multiple agents.

3. **Define two-layer model abstraction**: Replace LiteLLM-as-drop-in with two layers: `ModelProvider` (`async def execute(messages, tools, output_schema, **kwargs) -> AgentOutput`) with LiteLLM as default, plus capability validation layer that checks output structural requirements after generation. Include per-phase model routing in the interface (single model as default). Source: Recommendations #18, #25, #42, #30; convergence point "Two-layer model abstraction."

4. **Include minimal hosted web form as consumer validation artifact**: A single-page web form (text input, API call, no auth, no history) ships after developer validation (50+ runs). Includes share page rendering. Full web app addressed in separate spec (012) triggered by consumer validation data. Source: Recommendations #1, #38; dispute resolution.

5. **Specify MCP tool input/output schemas**: For each MCP tool, define input schema, output schema, error types, and execution model (blocking vs. streaming). Start with `conversus_run` and `conversus_decide`; add guided workflow tools as they mature. Source: Recommendations #15, #50; convergence point "MCP tool contracts."

6. **Ship Just Ask as Claude Code skill prototype**: Implement as config-generation-plus-output-formatting over existing SKILL.md execution. Define output contract before shipping. Prototype has a defined sunset. Source: Recommendation #31; convergence point "Claude Code skill prototype."

7. **Add adoption gates with channel-appropriate populations**: Developer gates: after 50 Just Ask runs, measure trust, return rate, sharing. Consumer gates: separate test via minimal web form with task completion rate and perceived value. Neither population's data evaluates the other's demand. Source: Recommendation #32.

8. **Seed community presets**: Create 20 seed presets: 12-13 developer/professional (framework selection, database choice, architecture patterns, cloud provider, build-vs-buy, etc.) plus 7-8 consumer (lease vs. buy, major selection, career change, vacation planning, etc.). All first-party, curated to quality standard. Community contributions launch as separate phase with quality gates. Source: Recommendations #35.

9. **Add dry-run/validate command**: `conversus validate [path-to-yml]` CLI command and `Deliberation.validate()` SDK method. Parses YAML, resolves presets, validates templates, estimates cost/tokens without executing. Source: Recommendation #16.

10. **Resolve open-source strategy**: Commit to: engine and CLI are open source (MIT/Apache 2.0). Community presets are open. Web app (if built) is a hosted service with free tier. Source: Recommendation #36.

**P3 -- Consider implementing** (bilateral agreement or strong but disputed):

1. **Expose preset system programmatically (tiered)**: Tier 1 with SDK launch: `presets.list()`, `presets.get(name)`, `presets.compose([names])`. Tier 2 after community validation: `presets.install(source)` with quality governance. Source: Recommendation #17. Note: Implementation timing depends on SDK maturity.

2. **Add config builder pattern to SDK**: Fluent builder API as a Tier 2 SDK feature. Interface designed in Phase 0; implementation ships after core SDK validation. Source: Recommendation #19. Note: Deferred to post-launch by adoption-strategist's tiering.

3. **Design consumer domain routing via presets**: Do not build for v1. Track question categories from usage data. After 200-500 real questions, build domain-specific presets for top 3-5 observed categories. Domain awareness implemented as preset layer, not engine logic. Source: Recommendation #9. Note: Contingent on usage data.

4. **Specify plugin/extension hook for custom modes**: Document how to register custom competition modes (template directory + mode config), how custom modes appear in mode selection, and how distribution surfaces discover them. Source: Recommendation #20. Note: Low-cost documentation that prevents forking.

5. **Add result quality feedback mechanism**: Thumbs-up/thumbs-down on results with optional free-text. Lightweight backend for initial artifact (not dependent on PostgreSQL). Source: Recommendation #10. Note: Required for future quality calibration.

6. **Add mobile-responsive requirement for minimal web artifact**: The minimal web form must be responsive and usable on mobile browsers. Full mobile-first design (custom mobile UX) is a constraint for the eventual full web app, not the validation artifact. Source: Recommendation #7. Note: Modern CSS frameworks provide this by default.

---

### Key Concessions

**consumer-advocate**:
- Conceded that the full web app cannot be at step 4-5, accepting it is too large for this spec's scope (revision, Modified Recommendation 1). Conceded from "web-native from the start" to "engine is headless, but its API contract is shaped by consumer UX requirements" (revision, New Recommendation 2). Most significantly, conceded that the 2-agent, 1-round lightweight default may not preserve conversus's value proposition: "I was optimizing for consumer UX without ensuring the underlying output is worth presenting" (revision, New Recommendation 1). This was triggered by the devils-advocate's challenge in cross-review.

**devex-advocate**:
- Conceded the LiteLLM provider interface signature was wrong: "I was wrong about the method signature. The architect is right" (revision, Recommendation 8). The original `async def complete(messages, **kwargs) -> str` was replaced with a two-layer model incorporating tool use and structured output. Also conceded that the confidence float should be replaced with quality indicators until calibration is possible (revision, Recommendation 2), and that the Claude Code skill prototype can ship before the SDK design is finalized (revision, Recommendation 1).

**architect**:
- Withdrew the scenario replay MCP tool recommendation after the adoption-strategist reframed it as a retention feature that depends on spec 007 infrastructure not available in v1 (revision, Recommendation 6). Conceded that the web app should not be "out of v1 scope entirely" but rather gated, accepting that some consumer surface is necessary to prevent CLI-shaped abstractions from calcifying (revision, Recommendation 4). Also conceded that the quality gate should be the first constraint on Just Ask output, above structural format compatibility: "I was focused on format compatibility when I should have been focused first on whether the output is worth feeding into anything" (revision, Recommendation 8).

**adoption-strategist**:
- Most significant concession: reversed position on "cut the web app entirely," acknowledging: "I was wrong to propose 'cut entirely' because it eliminated the possibility of consumer validation, not just the full-stack investment" (revision, Recommendation 8). This was triggered by the consumer-advocate's self-fulfilling-prophecy argument. Also conceded that MCP is mature enough as a protocol, withdrawing the "MCP is premature" characterization after the devex-advocate's evidence about deployment across multiple IDEs (revision, Recommendation 10). Added two new P1 recommendations (quality floor, structured output schema) that were absent from the original review, acknowledging blind spots exposed by the devils-advocate and devex-advocate.

**devils-advocate**:
- Conceded on engine extraction timing: originally demanded the question be resolved before any work begins, then accepted a time-boxed SKILL.md prototype that validates the product concept before extraction (revision, Recommendation 5). This was the most significant change, triggered by the adoption-strategist's argument that waiting for full extraction before any user validation is wasteful. Also withdrew the MCP maturity risk characterization as "medium impact," accepting the devex-advocate's evidence that MCP is sufficiently deployed (revision, Recommendation 10). Modified the model capability matrix from a static lookup to dynamic output validation, accepting the architect's and devex-advocate's argument that runtime checking is more robust (revision, Recommendation 2).
