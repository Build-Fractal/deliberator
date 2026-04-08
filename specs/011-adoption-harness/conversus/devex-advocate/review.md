# Developer Experience Advocate — Initial Utilization Review

**Spec under review:** `specs/011-adoption-harness/proposal.md`
**Reviewer role:** devex-advocate
**Grounding document:** `specs/999-decision-framework/spec.md`

---

## Executive Summary

The Adoption Harness proposal (spec 011) sets out to transform conversus from a power-user-only deliberation engine into a multi-tier tool accessible to everyone from non-technical consumers to AI-native engineers. From a developer experience standpoint, the proposal correctly identifies the five distribution formats that matter — MCP server, Python CLI, Python SDK, Claude Code Skill, and web app — and it correctly sequences CLI and MCP ahead of the web app in the build order. The three-tier user model (Just Ask, Guided, Power) is a sound abstraction that maps cleanly to how developers actually adopt tools: try it in one command, use the guided workflow when they need more control, then drop to raw YAML when they own the domain.

However, the proposal has significant gaps in the developer experience layer. The Python SDK surface area is undefined — there is no API sketch, no type contract, no async story. The MCP server tool signatures are listed but not designed: there are no input schemas, no streaming semantics, and no error contract. The "Just Ask" mode is overspecified for consumers and underspecified for programmatic use — developers will want `conversus_decide` to return structured data (JSON), not prose. Model agnosticism via LiteLLM is stated as a goal but open question 2 (L134) immediately hedges it, and the spec provides no fallback design if LiteLLM proves inadequate. The build order (L120-128) is driven by technical dependencies rather than developer adoption milestones, which means the MCP server — the single highest-value integration for AI-native engineers — does not ship until step 5.

**Most important recommendation:** Define the Python SDK's public API surface (classes, methods, types, async support) before any implementation begins — it is the contract that CLI, MCP server, and web app all depend on, and designing it after the fact will produce a leaky abstraction.

---

## Alignment

- **MCP-first integration** (L50-51, L74-86): The proposal explicitly names MCP as the primary integration path for Claude Code, Cursor, Windsurf, VS Code, and Codex users, and lists six well-scoped tool names. This aligns directly with how the decision framework's guided workflow (spec 003) is structured as discrete commands that map 1:1 to MCP tools. `[specs/999-decision-framework/spec.md, L448-458]` — the command registry already defines the exact subcommands these MCP tools would wrap.

- **CLI as pip-installable package** (L52): `pip install conversus` with a Click CLI is the correct distribution choice. It makes conversus instantly scriptable in CI/CD and composable with other tools. The decision framework's artifact-per-step model `[specs/999-decision-framework/spec.md, L259-300]` — where each command produces a durable file on disk — is inherently CLI-friendly: commands are stateless, inputs are file paths, outputs are file paths.

- **Power-user YAML preserved** (L31, L54, L142-146): The proposal explicitly preserves `/conversus run` for hand-crafted YAML, which means existing power-user workflows are not broken. This aligns with the backward compatibility constraint in the decision framework `[specs/999-decision-framework/spec.md, L439-446]` and ensures the adoption harness is additive, not disruptive.

- **Model agnosticism as a goal** (L57-72): Decoupling from Claude-only execution is essential for developer adoption. Engineers locked into a single provider will not adopt a tool for production CI/CD pipelines. The LiteLLM proposal supports the existing model-agnostic YAML config schema where `provider` and `name` are configurable fields.

- **Build order: CLI before web app** (L120-127): The proposal correctly sequences Python engine extraction, CLI, and MCP server before the web app. This matches developer adoption patterns — CLI and SDK adoption always precedes web app usage for developer tools. The decision framework's phased delivery model `[specs/999-decision-framework/spec.md, L547-566]` already demonstrates that independent phases with clear gates produce better outcomes than waterfall.

- **Preset and template extensibility** (L116, L134): The proposal mentions community presets and user customizations. The existing SKILL.md preset system `[SKILL.md, L93-168]` — with single-preset resolution, multi-preset composition, composability flags, and inline overrides — is already well-designed for extensibility. The adoption harness should expose this system programmatically, not just through YAML.

---

## Missed Opportunities

- **No SDK API design**: The proposal lists "Python SDK" as a distribution format (L55) with the example `from conversus import Deliberation` but provides zero design for it — no classes, no methods, no type hints, no async interface, no return types. The decision framework `[specs/999-decision-framework/spec.md, L259-271]` defines a clear artifact chain (problem.md -> interests.md -> conversus.yml -> output/) that maps naturally to a Python dataclass pipeline: `Problem -> Interests -> Config -> Result`. Without this API sketch, the SDK will be an afterthought bolted onto the CLI rather than the foundational layer everything else depends on. **Impact: high.**

- **No structured output format**: The "Just Ask" mode (L33-45) returns "plain-English synthesis." Developers need structured output — JSON with fields like `recommendation`, `confidence`, `arguments_for`, `arguments_against`, `dissent`. The decision framework's synthesis output `[specs/999-decision-framework/spec.md, L455-457]` already produces structured markdown with defined sections (from the templates). The SDK and MCP tools should parse this into structured data rather than passing raw markdown through. **Impact: high.**

- **No CI/CD integration design**: The proposal mentions CI/CD (L52) but provides no design for headless, non-interactive execution. The decision framework's guided commands `[specs/999-decision-framework/spec.md, L26-43]` are explicitly interactive ("asks clarifying questions"), which will fail in CI. The CLI needs a `--non-interactive` flag that accepts all defaults or fails fast on missing inputs rather than prompting. **Impact: high.**

- **No error contract for MCP tools**: Six MCP tools are listed (L79-86) but there are no input schemas, error codes, or failure semantics. When `conversus_decide` fails — bad model API key, rate limit, invalid question — what does the MCP client receive? The decision framework defines validation rules `[specs/999-decision-framework/spec.md, L517-531]` and guided recovery `[specs/999-decision-framework/spec.md, L500-503]` for the interactive case, but MCP tools need machine-readable errors, not conversational guidance. **Impact: high.**

- **No streaming design for MCP/SDK**: The proposal mentions "streaming output for real-time progress" (L113) but does not specify how. MCP supports streaming via progress notifications and partial results. The SKILL.md execution model `[SKILL.md, L273-298]` already has phase-by-phase reporting ("Phase 1 complete: N reviews produced"). These natural phase boundaries should be exposed as progress events in the MCP and SDK interfaces. **Impact: medium.**

- **No programmatic preset management**: The proposal mentions "community preset library" (L116) and the existing preset system `[SKILL.md, L93-168]` is robust, but there is no API for listing, searching, installing, or composing presets programmatically. A developer building a CI pipeline needs `conversus.presets.list()`, `conversus.presets.get("devils-advocate")`, and `conversus.presets.compose(["mechanist", "security"])` — not filesystem-level knowledge of `presets/{category}/{name}.yml`. **Impact: medium.**

- **No config-as-code pattern**: The decision framework produces `conversus.yml` as the configuration artifact `[specs/999-decision-framework/spec.md, L135-154]`. Developers will want to generate this programmatically — `Config.from_problem(problem).with_agents(agents).with_mode("cooperative").save("conversus.yml")`. The builder pattern is a standard SDK expectation that the proposal does not address. **Impact: medium.**

- **No testing/dry-run mode**: The proposal provides no mechanism for developers to validate a deliberation configuration without executing it. The decision framework's `converge` command `[specs/999-decision-framework/spec.md, L167-188]` shows the config and asks for confirmation, but in CI or SDK usage, developers need `conversus validate conversus.yml` or `Deliberation.dry_run()` that checks the config, resolves presets, validates templates, and estimates cost/tokens — without launching any agents. **Impact: medium.**

---

## Off-Base Assumptions

- **"Running inside Claude Code (locked to one model, one runtime)" (L9)**: The proposal frames the current state as being locked to Claude Code, but the SKILL.md `[SKILL.md, L10-13]` already specifies the abstraction correctly: "Requires an agent runtime that supports background Agent tool dispatch." The lock-in is to the Agent tool pattern, not to Claude Code specifically. Any runtime that implements `Agent`, `Read`, `Write`, and `Bash(ls:*)` could run conversus today. The correct framing is: the current distribution requires an MCP-compatible agent runtime, and the extraction to Python removes even that requirement. This matters because the proposal's architecture treats "extract to Python" as step 1, when the real step 1 is "define the Python API that the Agent-tool runtime was implicitly providing."

- **MCP maturity concern is overstated (L135)**: Open question 5 asks "Is MCP mature enough to be the primary integration strategy?" MCP is already supported by Claude Code, Cursor, Windsurf, Zed, and VS Code (via extensions). For a developer tool targeting AI-native engineers, MCP coverage is sufficient. The question implies MCP might not be ready, which could delay the MCP server unnecessarily. The correct concern is not MCP's maturity but conversus's MCP server design quality — a bad MCP server on a mature protocol is still a bad experience.

---

## Actionable Recommendations

1. **Define SDK public API** (Priority: P1)
   - **Current state**: The SDK is mentioned at L55 with one import example (`from conversus import Deliberation`) and no further design.
   - **Proposed change**: Add a section to the proposal specifying the SDK's public surface: core classes (`Problem`, `Interests`, `Config`, `Deliberation`, `Result`), key methods (`Deliberation.run()`, `Deliberation.run_async()`, `Config.from_yaml()`, `Config.from_problem()`), return types (dataclasses with typed fields), and async support (`asyncio`-native with sync wrappers). The artifact chain from the decision framework `[specs/999-decision-framework/spec.md, L259-271]` should be the SDK's data model.
   - **Rationale**: The SDK is the foundational layer. CLI is `click` wrapping SDK methods. MCP server is MCP handlers wrapping SDK methods. Web app is FastAPI wrapping SDK methods. If the SDK is not designed first, every surface will implement its own version of config parsing, execution, and result handling. `[specs/999-decision-framework/spec.md, L439-446]` shows the two paths (guided and manual) converge at the same engine — the SDK is that engine's programmatic interface.
   - **Risk if ignored**: Three separate implementations of core logic (CLI, MCP, web) that diverge in behavior, making bugs surface differently per distribution format and tripling maintenance cost.

2. **Add structured output mode** (Priority: P1)
   - **Current state**: "Just Ask" mode (L41) returns "plain-English synthesis." MCP tools (L79-86) have no output schema.
   - **Proposed change**: All SDK methods and MCP tools should return structured data by default — a Python dataclass / JSON object with fields: `recommendation` (string), `confidence` (float 0-1), `mode_used` (string), `agents` (list of agent summaries), `arguments` (list), `dissent` (list), `raw_synthesis` (string, full markdown). Plain-English is a rendering of this structure, not the primary output.
   - **Rationale**: Developers composing conversus in CI/CD or as a step in a larger agent workflow need machine-readable output. The decision framework's synthesis `[specs/999-decision-framework/spec.md, L455-457]` already has structured sections that can be parsed. Structured output is the difference between a developer tool and a demo.
   - **Risk if ignored**: Developers will parse markdown with regex to extract recommendations, leading to brittle integrations that break when template wording changes.

3. **Move MCP server to build step 3** (Priority: P1)
   - **Current state**: Build order (L120-127) puts MCP server at step 5, after CLI (step 3) and "Just Ask" mode (step 4).
   - **Proposed change**: Reorder to: (1) Python engine extraction, (2) SDK with types, (3) MCP server wrapping SDK, (4) CLI wrapping SDK, (5) "Just Ask" mode. The MCP server should ship alongside or immediately after the CLI because it reaches the largest developer audience (every Claude Code, Cursor, and Windsurf user) with zero behavior change — they stay in their editor.
   - **Rationale**: The decision framework's commands `[specs/999-decision-framework/spec.md, L448-458]` map directly to MCP tool signatures. The MCP server is a thin wrapper, not a large engineering effort. Delaying it to step 5 means the highest-value developer integration ships last. The proposal itself calls MCP the "Primary Integration Path" (L74) — the build order should reflect that priority.
   - **Risk if ignored**: Developer adoption is delayed by months while consumer-facing features (Just Ask, web app) are built first, missing the window where AI-native engineers are actively looking for MCP tools to add to their workflows.

4. **Design CI/CD non-interactive mode** (Priority: P1)
   - **Current state**: The guided workflow commands are interactive (L29-30: "Step-by-step wizard"). No non-interactive execution path is specified.
   - **Proposed change**: Add `--non-interactive` / `--ci` flag to all CLI commands that: (a) accepts all auto-generated defaults without prompting, (b) fails with a non-zero exit code and structured error on missing required inputs instead of prompting, (c) outputs JSON instead of pretty-printed text. SDK methods should be non-interactive by default (they are programmatic).
   - **Rationale**: The decision framework `[specs/999-decision-framework/spec.md, L535-536]` requires incremental artifacts on disk, which is CI-friendly. But the interactive confirmation gates `[specs/999-decision-framework/spec.md, L177-178]` will block headless execution. CI/CD is a primary use case for developer tools — it must be designed in, not bolted on.
   - **Risk if ignored**: Developers cannot use conversus in GitHub Actions, GitLab CI, or automated review pipelines — the highest-value integration point for engineering teams.

5. **Specify MCP tool input/output schemas** (Priority: P2)
   - **Current state**: Six MCP tool names are listed (L79-86) with no input parameters, output types, or error handling.
   - **Proposed change**: For each MCP tool, define: input schema (required and optional parameters with types), output schema (structured JSON), error types (invalid input, model failure, rate limit, missing dependencies), and progress/streaming behavior. Example for `conversus_decide`: input `{question: string, model?: string, agents?: int, mode?: string}`, output `{recommendation: string, confidence: float, agents: [{name, position, key_argument}], dissent: [string]}`.
   - **Rationale**: MCP clients need schemas to render tool descriptions, validate inputs, and parse outputs. The decision framework's artifact specifications `[specs/999-decision-framework/spec.md, L46-75, L105-126]` already define structured formats — the MCP schemas should mirror these.
   - **Risk if ignored**: MCP clients will show generic "call conversus" tools with no parameter guidance, producing a poor developer experience that undermines adoption.

6. **Add dry-run/validate command** (Priority: P2)
   - **Current state**: No mechanism to validate a configuration without executing a deliberation.
   - **Proposed change**: Add `conversus validate [path-to-yml]` CLI command and `Deliberation.validate()` / `Deliberation.dry_run()` SDK methods that: parse and validate the YAML, resolve presets, validate templates (using the existing linter at `linter/validate.py`), estimate agent launches and token cost, and report any issues — without launching any agents.
   - **Rationale**: The SKILL.md validation logic `[SKILL.md, L170-196]` already performs extensive checks. The decision framework's `converge` command `[specs/999-decision-framework/spec.md, L177]` presents a pre-execution summary. A standalone validate command makes this available to CI/CD and SDK users without requiring the full execution flow.
   - **Risk if ignored**: Developers discover configuration errors only after launching (and paying for) agents. In CI, this means failed pipeline runs with no fast-fail path.

7. **Expose preset system programmatically** (Priority: P2)
   - **Current state**: Presets are filesystem-based (`presets/{category}/{name}.yml`) with resolution logic in SKILL.md (L93-168). The proposal mentions "community preset library" (L116) but no programmatic interface.
   - **Proposed change**: Add SDK methods: `conversus.presets.list() -> List[PresetInfo]`, `conversus.presets.get(name) -> Preset`, `conversus.presets.compose([names]) -> ComposedPrompt`, `conversus.presets.install(source) -> None`. Add corresponding MCP tools: `conversus_presets_list`, `conversus_presets_search`. Add CLI commands: `conversus presets list`, `conversus presets show <name>`.
   - **Rationale**: The preset composition system `[SKILL.md, L113-157]` is one of conversus's most differentiating features. Making it programmatically accessible turns it from a YAML convention into a composable API that developers can use to build custom deliberation workflows.
   - **Risk if ignored**: Presets remain a hidden power-user feature that most developers never discover, reducing the viral potential of the community preset library.

8. **Resolve LiteLLM vs custom provider decisively** (Priority: P2)
   - **Current state**: Open question 2 (L134) asks "Is LiteLLM the right abstraction or should we build a custom provider interface?" and leaves it unresolved.
   - **Proposed change**: Commit to a thin provider interface (`class ModelProvider: async def complete(messages, **kwargs) -> str`) with LiteLLM as the default implementation. This gives model agnosticism immediately via LiteLLM while allowing custom providers (e.g., for Ollama edge cases or corporate proxies) without forking. The interface should be documented in the SDK's public API.
   - **Rationale**: Indecision on the model layer blocks the entire extraction (build step 1-2). A thin interface with a default implementation is the standard pattern (see: LangChain's BaseModel, LlamaIndex's LLM class). `[specs/999-decision-framework/spec.md, L531]` requires "Must not require any specific model" — a provider interface satisfies this while LiteLLM alone does not (it adds a hard dependency).
   - **Risk if ignored**: The model abstraction is designed reactively during implementation, producing a leaky abstraction that makes non-Claude models second-class citizens — exactly the failure mode the proposal warns against at L9.

9. **Add config builder pattern to SDK** (Priority: P3)
   - **Current state**: Configuration is via YAML files only. The decision framework generates YAML through a guided workflow `[specs/999-decision-framework/spec.md, L135-154]`.
   - **Proposed change**: Add a fluent builder API: `Config.builder().problem("Should we use Redis?").agent("redis-fan", prompt="...").agent("pg-fan", prompt="...").mode("winner-take-all").build()`. This is the programmatic equivalent of the guided workflow — same artifact, different interface.
   - **Rationale**: Developers composing deliberations in code should not have to generate YAML strings. The decision framework's step-by-step artifact production `[specs/999-decision-framework/spec.md, L219-256]` maps cleanly to a builder pattern where each method call corresponds to a workflow step.
   - **Risk if ignored**: Developers resort to YAML string templates with f-string interpolation, which is error-prone and defeats the purpose of having a typed SDK.

10. **Specify plugin/extension hook for custom modes** (Priority: P3)
    - **Current state**: Build step 8 (L127) mentions "Plugin system (spec 007 — game engine, scoring)" but the adoption harness proposal does not describe how developers would create or register custom competition modes.
    - **Proposed change**: Add a section describing the extension model: how to register a custom mode (template directory + mode config), how custom modes appear in the mode selection logic, and how the MCP/CLI/SDK surfaces discover them. Reference the existing template system `[SKILL.md, L243-269]` which already resolves templates by mode name — custom modes need only add a new directory.
    - **Rationale**: The decision framework's mode selection matrix `[specs/999-decision-framework/spec.md, L309-319]` is closed — it only supports four modes. Developers working in domains with different competitive dynamics (e.g., auction-based, consensus-building, parliamentary) need an extension point. The template system already supports this structurally; it just needs to be documented and surfaced.
    - **Risk if ignored**: Developers fork conversus to add modes instead of extending it, fragmenting the ecosystem and reducing the value of the community preset library.

---

## Referenced Documentation

- `specs/011-adoption-harness/proposal.md` — lines cited: L9, L29-31, L33-45, L41, L50-55, L57-72, L74-86, L79-86, L113, L116, L120-128, L127, L134, L135, L142-146
- `specs/999-decision-framework/spec.md` — sections/lines cited: L26-43, L46-75, L105-126, L135-154, L167-188, L177-178, L219-256, L259-271, L259-300, L309-319, L439-446, L448-458, L455-457, L500-503, L517-531, L535-536, L547-566
- `SKILL.md` — sections/lines cited: L10-13, L93-168, L113-157, L170-196, L243-269, L273-298
