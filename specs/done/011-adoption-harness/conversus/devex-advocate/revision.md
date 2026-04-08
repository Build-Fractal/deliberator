# Developer Experience Advocate — Revised Position

**Spec under review:** `specs/011-adoption-harness/proposal.md`
**Reviewer role:** devex-advocate
**Revision iteration:** 1
**Grounding document:** `specs/999-decision-framework/spec.md`

---

### Recommendation Dispositions

#### Recommendation 1: Define SDK public API

- **Original position**: Define the Python SDK's public API surface (classes, methods, types, async support) before any implementation begins — it is the contract that CLI, MCP server, and web app all depend on.
- **Disposition**: Modified
- **Explanation**:

  The architect's cross-review (Dangerous Contradictions, "SDK as foundation vs engine interfaces as foundation") correctly identifies that I proposed the SDK public API as the foundational contract without acknowledging that the engine's internal interfaces — `DeliberationState`, `AgentState`, `RoundState`, and the spec 007 lifecycle hooks — are a separate, equally necessary contract layer. My original recommendation treated the SDK types as the sole foundation; the architect demonstrates that there are two contract layers (internal engine state and external SDK surface) that must be designed together or they produce impedance mismatch.

  The devil's-advocate cross-review (Dangerous Contradictions, "SDK-first design vs. unresolved engine extraction") adds a second valid challenge: my recommendation implicitly assumes the answer to open question 1 (Python extraction vs. SKILL.md adapters) is "extract to Python." Designing a Python SDK with `Deliberation.run_async()` is incoherent if the decision goes the other way. The extraction question is a blocking prerequisite to SDK design.

  The adoption-strategist cross-review (Dangerous Contradictions, "Build order: infrastructure-first vs. validation-first") challenges the timing — designing a full SDK API before any user validation means the API is designed in a vacuum. Their point that usage data from a quick Claude Code skill prototype should inform the API is well-taken.

  **Modified recommendation**: (1) Resolve the engine extraction question first — commit to Python extraction as a blocking decision. (2) Define the SDK's public API types and the engine's internal interfaces together in a single Phase 0, with an explicit mapping layer between them. The SDK surface (`Problem`, `Config`, `Deliberation`, `Result`) is the external contract; the engine interfaces (`DeliberationState`, `AgentState`, lifecycle hooks) are the internal contract. Both are designed concurrently, with a `to_result()` bridge defined between them. (3) Treat the SDK API as a "draft sketch" that is refined after the first 50 validated uses via the Claude Code skill prototype. The types and method signatures are designed up front; the behavioral details evolve.

#### Recommendation 2: Add structured output mode

- **Original position**: All SDK methods and MCP tools should return structured data by default — a Python dataclass / JSON object with fields like `recommendation`, `confidence`, `arguments_for`, `arguments_against`, `dissent`. Plain-English is a rendering of this structure, not the primary output.
- **Disposition**: Modified
- **Explanation**:

  Three cross-reviews challenged aspects of this recommendation, and all three have merit.

  The devil's-advocate cross-review (Dangerous Contradictions, "Structured output as default vs. quality verification gap") makes the strongest challenge: a `confidence: 0.82` value from a 2-agent, 1-round deliberation without cross-reviews is meaningless — it creates an illusion of rigor. Developers will branch CI pipelines on `confidence > 0.7` when the underlying deliberation may not have produced genuinely adversarial pressure. The devil's advocate is right that the quality model must be defined before the output schema, not after.

  The consumer-advocate cross-review (Dangerous Contradictions, "Structured output vs. plain-English output as the default") argues that both structured and prose outputs need to be first-class — not one derived from the other. Their point is that a synthesis "written for human comprehension" is qualitatively different from rendering structured field labels into prose.

  The adoption-strategist cross-review (Dangerous Contradictions, "Structured output as default vs. 'show the debate' as differentiator") argues the debate transcript — the visible multi-agent process — is what differentiates conversus from ChatGPT. My structured JSON distills this away.

  The architect cross-review (Tensions, "Structured output: SDK concern vs architectural concern") adds that the output must follow template-structured markdown for internal ecosystem compatibility (prior rounds, dispute parsing).

  **Modified recommendation**: The engine produces template-conformant markdown as its canonical output (architect's requirement for ecosystem compatibility). A parser converts this to a typed `Result` dataclass with fields: `recommendation`, `mode_used`, `agents` (list of agent summaries), `arguments`, `dissent`, `debate_transcript` (the full multi-agent exchange — adoption-strategist's differentiator), `quality_indicators` (object reporting phases run, agent count, whether cross-reviews occurred, whether genuine disagreement surfaced — devil's advocate's quality model), and `raw_synthesis` (the template-conformant markdown). The `confidence` field is either removed or replaced with `quality_indicators` until a calibrated quality model exists. Plain-English rendering and structured JSON are both projections of the canonical output — neither is derived from the other. Both are first-class.

#### Recommendation 3: Move MCP server to build step 3

- **Original position**: Reorder the build so the MCP server ships at step 3, immediately after the SDK, because it reaches the largest developer audience and is a thin wrapper.
- **Disposition**: Modified
- **Explanation**:

  This was the most contested recommendation. Four cross-reviews challenged it, each from a different angle.

  The architect cross-review (Dangerous Contradictions, "Build order priority: MCP server vs engine interfaces") argues that moving MCP to step 3 assumes the SDK is stable by step 2, but the engine extraction alone requires 5 sub-phases. If MCP wraps an SDK whose underlying engine is still being decomposed, the tool signatures will either expose unstable internals or be a superficial shell that needs rebuilding.

  The devil's-advocate cross-review (Dangerous Contradictions, "Build order priority: MCP server vs. quality foundations") argues that shipping MCP before quality criteria are defined means early adopters hit undesigned failure modes, forming negative first impressions that are "extremely difficult to reverse in developer communities."

  The adoption-strategist cross-review (Dangerous Contradictions, "MCP as primary channel vs. MCP as premature bet") argues MCP should not be primary until validated by user demand, and the Claude Code skill should come first.

  The consumer-advocate cross-review (Dangerous Contradictions, "Build order: web app vs. MCP server priority") argues the web app should occupy the same step 4-5 position I claimed for MCP.

  I yield on the timing but not the principle. The architect's point about unstable SDK surfaces is the most technically compelling — an MCP server that wraps a moving SDK target will produce breaking changes that destroy developer trust. The devil's advocate's quality concern is also valid — `conversus_decide` should not ship before we know what a good output looks like.

  **Modified recommendation**: The MCP server ships after the SDK public API is designed and the "Just Ask" quality criteria are defined — but before the web app. The specific step number matters less than the prerequisites: (1) engine extraction committed, (2) SDK API designed (even as a draft), (3) "Just Ask" quality model defined, (4) MCP server ships with `conversus_run` and `conversus_decide` using full tool contracts. The devil's advocate's suggestion to ship `conversus_run` first (known behavior) and add `conversus_decide` only after quality criteria are met is a sound incremental approach. Additionally, I accept the adoption-strategist's recommendation that a Claude Code skill prototype can ship immediately as a validation mechanism — this does not compete with MCP, it informs it.

#### Recommendation 4: Design CI/CD non-interactive mode

- **Original position**: Add `--non-interactive` / `--ci` flag to all CLI commands that accepts defaults, fails fast on missing inputs with structured errors, and outputs JSON.
- **Disposition**: Modified
- **Explanation**:

  The architect cross-review (Tensions, "CI/CD non-interactive mode: depth of design") makes a subtle but important framing correction: if the minimum viable extraction is a CLI that reads `conversus.yml` and writes output files, the CLI starts non-interactive by design. The interactive guided wizard is the addition, not the default. This inverts my framing: instead of "add a flag to disable interactivity," the CLI starts non-interactive and adds a flag to enable it (`--interactive` / `--guided`).

  The adoption-strategist cross-review (Tensions, "CI/CD as first-class concern vs. CI/CD as premature optimization") implicitly challenges the P1 priority — their entire review focuses on interactive, human-facing use cases, suggesting CI/CD adoption follows human adoption.

  I accept the architect's framing inversion — it is cleaner and produces less design overhead. I maintain the P1 priority but acknowledge that the interactive Claude Code skill may ship first per the adoption-strategist's sequencing.

  **Modified recommendation**: The CLI is non-interactive by default (config-file-in, output-files-out). Interactive features from the guided workflow (spec 003) are added as a separate `--interactive` or `--guided` flag. The SDK is non-interactive by design (it is programmatic). This framing eliminates the need for a `--ci` flag because CI behavior is the default. The key deliverable remains: structured error output (JSON with error type, description, and missing fields) when configuration is invalid or inputs are insufficient.

#### Recommendation 5: Specify MCP tool input/output schemas

- **Original position**: For each MCP tool, define input schema, output schema, error types, and streaming behavior.
- **Disposition**: Surviving
- **Explanation**:

  This recommendation received broad agreement rather than challenge. The devil's-advocate cross-review (Safe Agreements, "MCP tool contracts must be specified before implementation") independently flagged the same gap and recommended essentially the same fix. The architect cross-review did not challenge it. The consumer-advocate cross-review did not challenge it (their concerns are about the web app, not MCP schemas).

  The devil's-advocate cross-review (Tensions, "MCP tool granularity") adds a valid nuance: start with fewer, well-specified tools rather than more underspecified ones. Ship `conversus_run` and `conversus_decide` with full contracts first, then add guided workflow tools as they mature. I accept this incremental approach — it aligns with my modified MCP timeline recommendation.

  This recommendation survives because it was the strongest convergence point across multiple reviews. The spec should include full tool schemas as part of the MCP server design, not defer them to implementation.

#### Recommendation 6: Add dry-run/validate command

- **Original position**: Add `conversus validate` CLI command and `Deliberation.validate()` / `Deliberation.dry_run()` SDK methods that parse YAML, resolve presets, validate templates, and estimate cost/tokens without executing.
- **Disposition**: Surviving
- **Explanation**:

  The devil's-advocate cross-review (Tensions, "Cost controls: who pays vs. how much") validates the need from a complementary angle — they want runtime budget caps for consumers, while I want pre-execution validation for developers. The consumer-advocate cross-review (Tensions, "Dry-run/validate vs. consumer trust signals") distinguishes between pre-execution validation (my concern) and post-execution confidence (their concern) and correctly notes that neither substitutes for the other.

  No cross-review challenged the recommendation itself — the challenges were about priority relative to other work. The adoption-strategist cross-review (Tensions, "Breadth of SDK surface vs. minimal viable distribution") implies this could be deferred to a Tier 2 SDK surface, which I accept as reasonable. The recommendation survives at P2 priority.

  The cost estimation component of this recommendation is reinforced by the devil's advocate's concern about API bill shock for non-technical users. A shared cost estimation engine, exposed differently per surface (consent dialog for web, structured estimate for CLI/SDK, metadata for MCP), serves both audiences.

#### Recommendation 7: Expose preset system programmatically

- **Original position**: Add SDK methods (`conversus.presets.list()`, `.get()`, `.compose()`, `.install()`) and corresponding MCP tools and CLI commands for preset management.
- **Disposition**: Modified
- **Explanation**:

  The devil's-advocate cross-review (Tensions, "Preset system: programmatic API vs. quality governance") challenges the `install()` method specifically: pulling from an unvetted community registry combined with arbitrary `compose()` could produce agent configurations that violate template structural requirements. The existing preset validation was designed for a curated, filesystem-local set — not a package manager.

  The adoption-strategist cross-review (Safe Agreements, "Community presets need a seeding strategy") provides the complementary content concern: an empty preset library has no network effects, so the first 20 presets need to be built by the team.

  The architect cross-review (Tensions, "Preset system: programmatic API priority") does not treat presets as a priority API surface, focusing instead on extraction correctness.

  **Modified recommendation**: The programmatic preset API ships in two tiers. Tier 1 (with SDK launch): `presets.list()`, `presets.get(name)`, `presets.compose([names])` — read-only operations against the local preset library. These enforce the same validation constraints the SKILL.md preset system enforces (name matching, category matching, composability flags). Tier 2 (after community validation): `presets.install(source)` with quality governance — validation on install, not just on use, and a defined vetting process. The `install()` method is deferred until the quality governance model is designed. Additionally, 20 seed presets covering high-value decision types should be created before launch (adoption-strategist's recommendation).

#### Recommendation 8: Resolve LiteLLM vs custom provider decisively

- **Original position**: Commit to a thin provider interface (`class ModelProvider: async def complete(messages, **kwargs) -> str`) with LiteLLM as the default implementation.
- **Disposition**: Modified
- **Explanation**:

  The architect cross-review (Dangerous Contradictions, "LiteLLM sufficiency assessment") delivers the most substantive technical challenge to any of my recommendations. The architect correctly identifies that conversus agents are not simple chat completions — they use tool calls, structured output, and template-format enforcement. My proposed interface (`async def complete(messages, **kwargs) -> str`) hides this complexity and would produce a provider interface that works for trivial cases and breaks for real deliberations. Fixing it later is a breaking API change.

  The devil's-advocate cross-review (Tensions, "Model agnosticism: capability matrix vs. provider interface") adds that a thin interface should also include capability validation — preventing developers from plugging in models that cannot support the requested deliberation depth.

  I was wrong about the method signature. The architect is right.

  **Modified recommendation**: Two abstraction layers, not one. Layer 1: `ModelProvider` — handles model routing and credentials. Method signature: `async def execute(messages, tools, output_schema, **kwargs) -> AgentOutput` (architect's correction — reflects what conversus agents actually need, including tool use and structured output). LiteLLM is the default implementation. Layer 2: `AgentRuntime` — sits above ModelProvider, handles tool registration, output validation, template enforcement, and the agent behavioral contract. This separates "which model to call" from "what an agent can do." The capability validation (devil's advocate's concern) belongs in the `AgentRuntime` layer — it checks whether the model's output meets structural requirements after generation, rather than maintaining a static capability catalog.

#### Recommendation 9: Add config builder pattern to SDK

- **Original position**: Add a fluent builder API: `Config.builder().problem("...").agent("name", prompt="...").mode("cooperative").build()`.
- **Disposition**: Surviving
- **Explanation**:

  The adoption-strategist cross-review (Tensions, "Breadth of SDK surface vs. minimal viable distribution") implicitly challenges this as a Tier 2 or Tier 3 SDK feature — part of a mature product's API, not a launch product's API. No cross-review challenged the recommendation on substance.

  I accept the tiering. The builder pattern is a Tier 2 SDK feature: the interface is designed in Phase 0 alongside the core types, but implementation ships after the core `Deliberation.run()` and `Config.from_yaml()` are validated. This maintains the "design before implementation" principle while respecting the "validate before expanding" principle.

  The recommendation survives at P3 priority with the understanding that it ships after core SDK validation.

#### Recommendation 10: Specify plugin/extension hook for custom modes

- **Original position**: Add a section describing how developers create, register, and discover custom competition modes through the template system.
- **Disposition**: Surviving
- **Explanation**:

  No cross-review directly challenged this recommendation. The architect cross-review reinforces it by pulling spec 007's plugin system forward to Phase 0 as an interface definition concern (Actionable Recommendations, item 1). The devil's-advocate cross-review does not mention custom modes. The adoption-strategist and consumer-advocate cross-reviews focus on other priorities.

  The recommendation survives at P3 priority. The template system already supports custom modes structurally — a new mode needs only a new template directory. What is missing is documentation and discovery: how the MCP/CLI/SDK surfaces find and present custom modes. This is low-cost design work that prevents forking and can be specified without being implemented immediately.

---

### New Recommendations

- **Define "Just Ask" quality model before output schema** (Priority: P1)
  - **Triggered by**: Devil's-advocate cross-review of my review (Dangerous Contradictions, "Structured output as default vs. quality verification gap") and their original review's identification that a 2-agent, 1-round deliberation without cross-reviews is "structurally identical to asking two models the same question and having a third summarize."
  - **Proposed change**: Before designing the structured output schema or MCP tool contracts, define the minimum quality criteria for "Just Ask" mode: what distinguishes a conversus deliberation from a single-model call? The spec should define measurable quality indicators — whether genuine disagreement surfaced, whether agents cited different evidence, whether the synthesis acknowledged trade-offs rather than averaging positions. These indicators become fields in the output schema and inform whether a "mini-cross-review" (devil's advocate's proposal) is required for the lightweight mode.
  - **Rationale**: I focused entirely on the output format and ignored the output quality question. The devil's advocate correctly identified that well-typed, CI-friendly structured output from a shallow deliberation is worse than no structure at all — it makes low-quality output look authoritative. Quality criteria must come before schema design because the schema should reflect what the system actually guarantees, not what it aspires to.

- **Gate web app behind adoption metric, do not cut entirely** (Priority: P2)
  - **Triggered by**: The tension between architect (cut web app from v1 entirely — Actionable Recommendations, item 4), adoption-strategist (cut web app from this proposal — Actionable Recommendations, item 8), consumer-advocate (move web app earlier — Actionable Recommendations, item 1), and my own silence on the question. My cross-review of the architect (Dangerous Contradictions, "Web app deferral") and my cross-review of the adoption-strategist (Dangerous Contradictions, "'Cut the web app' vs. implicit acceptance") both surfaced this as an unresolved gap in my original review.
  - **Proposed change**: Keep the web app in the proposal as a vision item with explicit scope boundaries: the engine must not assume filesystem-only storage (forward compatibility), but detailed web app design is deferred to a separate spec. The web app is gated behind a specific adoption metric (e.g., 200 active CLI/MCP/SDK users) rather than unconditionally cut or unconditionally included. This ensures developer-facing surfaces ship without scope pressure from the web app, while preserving the non-technical user story.
  - **Rationale**: My original review was silent on the web app's scope status, which created ambiguity that multiple cross-reviews exploited. Taking an explicit position — gated, not cut — addresses the architect's scope-pressure concern, the adoption-strategist's unvalidated-demand concern, and the consumer-advocate's non-technical-user-story concern simultaneously.

---

### Position Summary

Of my 10 original recommendations, I modified 5 (recommendations 1, 2, 3, 4, 7, and 8 — six modifications total when including the LiteLLM interface correction), maintained 3 without substantive change (recommendations 5, 9, and 10), and withdrew none. I added 2 new recommendations. No recommendation was fully withdrawn because even the most heavily challenged positions (MCP build order, structured output, SDK-first design) contained core insights that survived scrutiny — they needed refinement in scope, sequencing, or technical detail, not abandonment.

The most significant change in my thinking was caused by the architect's challenge to my LiteLLM provider interface (recommendation 8). My original `async def complete(messages, **kwargs) -> str` was a clean-looking API that fundamentally misrepresented what conversus agents do. The architect's observation that agents require tool use, structured output, and template enforcement — none of which a bare string return supports — exposed a gap between my API aesthetics and the system's actual requirements. This correction cascades: a richer provider interface means the SDK's model layer is more complex than I originally scoped, which validates the architect's broader point that the engine extraction is a multi-module effort, not a quick extraction. I was optimizing for API surface elegance while underestimating implementation complexity. The corrected two-layer model (`ModelProvider` for routing + `AgentRuntime` for behavioral contract) is architecturally sound in a way my original was not.

My remaining highest-priority recommendation is the modified version of recommendation 1 (Define SDK public API) combined with the new recommendation on quality model definition. The SDK public API — designed together with the engine's internal interfaces in a shared Phase 0, informed by early Claude Code skill validation — remains the single most important deliverable for the adoption harness. Without it, CLI, MCP, and web app each implement their own version of config parsing, execution, and result handling, producing the three-divergent-implementations failure mode that every cross-reviewer acknowledged as a real risk. The quality model must be defined alongside the API so that the output schema reflects genuine deliberation guarantees rather than aspirational fields. These two concerns — API contract and quality contract — are the foundation everything else depends on, and they should survive into the final synthesis as the first deliverables after the engine extraction decision is committed.
