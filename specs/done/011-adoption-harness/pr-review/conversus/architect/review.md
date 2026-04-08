# Architect Review — 011-adoption-harness Global Synthesis

**Reviewer**: Systems Architect
**Date**: 2026-03-24
**Target**: `global-synthesis.md` + all 5 milestone reviews (M001-M005)
**Scope**: Engineering quality, dependency structure, extension point adequacy, production readiness

---

## Executive Summary

The 011-adoption-harness PR delivers a substantial body of work: 277 files, ~39,000 lines, 1,318 tests across 5 milestones, taking conversus from a SKILL.md prototype to a packaged engine with CLI, SDK, MCP server, and web interface. The architecture is fundamentally sound -- pure function extraction, frozen Pydantic models, protocol-based typing, and event-driven dispatch are all correct choices that will compound in value as the game engine specs (012-020) land. The test culture is exceptional, running 3x spec requirements in M002 alone.

The critical architectural issue is the linter-to-engine dependency inversion. The engine package imports context models, quality gates, and output parsing from the linter package in three separate locations (`engine/templates.py`, `engine/phases.py`, `engine/sdk.py`). This is not merely a packaging concern -- it is a layering violation that will become a hard blocker when specs 015 (feature extraction) and 016 (plugin system) need to import from the engine without dragging in the linter. The models in `linter/models.py` are not linter models; they are domain models that the linter, engine, and future plugins all consume. They belong in a shared location.

The second systemic concern is the missing extension point surface for the game engine vision. The EventEmitter is observe-only (no interception), there are no lifecycle hooks for plugin execution, ModelProvider is text-only with no capability negotiation, and per-phase model routing is advertised but not wired. Individually these are P2s. Collectively they represent the entire integration surface that specs 016-019 need to build on. Deferring all of them makes the game engine specs write against an API that does not exist yet, guaranteeing a breaking refactor later. **My most important recommendation: resolve the linter/engine dependency inversion and add the three missing extension protocols (PluginHook, StorageWriter, per-phase model map) before merge, because every game engine spec will import from engine/ and the current dependency graph makes that unsafe.**

---

## Alignment

- **Pure function extraction** (`global-synthesis.md`, L72): Every milestone extracts testable pure functions behind thin wrappers (MCP tools, CLI commands, SDK methods). This is the correct architecture for a system that will be extended by plugins. Pure functions are composable, testable, and importable without side effects -- exactly what spec 016's plugin `execute()` needs to call. [`m002-engine.md`, L46-50]

- **Frozen Pydantic models throughout** (`global-synthesis.md`, L73): Constitution Principle IX enforcement is thorough and tested. The 12+ frozen models across 4 files form a reliable contract surface. This is critical for spec 015 (feature extraction), which needs to import `StructuredDeliberation`, `QualityIndicators`, and phase context models without worrying about mutation. [`m001-foundation.md`, L28; `linter/models.py`, L248]

- **Protocol-based ModelProvider** (`m002-engine.md`, L24): Using `@runtime_checkable Protocol` instead of ABCs is the right choice for a plugin ecosystem. Any class with `complete()` and `stream()` is a valid provider -- no inheritance required. This structural subtyping aligns with spec 016's design principle "Plugins are swappable." [`engine/providers/__init__.py`, L16-30]

- **EventEmitter as protocol with multiple implementations** (`m002-engine.md`, L37): `CallbackEmitter`, `NullEmitter`, and `AsyncQueueEmitter` demonstrate clean separation of event production from consumption. The SSE streaming in M005 validates this architecture under real async load. [`engine/events.py`, L79-113]

- **EngineConfig as validated Pydantic with estimate_cost()** (`global-synthesis.md`, L91): This is the exact interface that spec 019 (config optimizer) needs. The optimizer's `PRE_EXECUTION` hook can call `validate()` and `estimate_cost()` to evaluate candidate configurations before execution. [`engine/config.py`, L34-60]

- **JSON-serializable pipeline results** (`global-synthesis.md`, L89): `PipelineResult` and `ConversusOutput` both support `model_dump_json()`, which is the serialization path for spec 020 (scenario storage). The `--format json` output in M004 proves this works end-to-end. [`m004-cli-polish.md`, L28-30]

---

## Missed Opportunities

- **Shared domain model package**: The `linter/models.py` file contains 387 lines of domain models (Phase, TemplateContext subclasses, ModeSchema, VariablesSchema) that the engine, linter, SDK, and future plugins all need. Neither "linter" nor "engine" is the correct home. A `conversus.models` or `conversus.schema` package would eliminate the inverted dependency (G1) and provide a clean import target for specs 015-020. The engine already has its own config models in `engine/config.py`; the template context models should sit alongside them or in a shared namespace. Impact: **high**. [`m002-engine.md`, L30-32; `engine/templates.py`, L23-33]

- **Lifecycle hook protocol for plugin system**: The EventEmitter protocol is observe-only (`emit()` receives events; nothing intercepts or modifies them). Spec 016 requires four hook points (`PRE_EXECUTION`, `POST_PHASE_5`, `POST_DELIBERATION`, `POST_ARBITRATION`) where plugins execute logic and return results. This requires a different protocol -- `execute(state: DeliberationState) -> PluginResult` -- with the orchestrator calling registered hooks at the right points in `run_pipeline()`. Adding hook call sites now (even with no registered hooks) is trivial; retrofitting them after M005 merges means touching the core pipeline. Impact: **high**. [`016-plugin-system/spec.md`, L50-54; `m002-engine.md`, L72; `global-synthesis.md`, L94]

- **StorageWriter abstraction for OutputManager**: `OutputManager` writes directly to the filesystem via `Path.write_text()` and `shutil.move()`. Spec 020 (scenario storage) needs to write to `scenarios/` YAML files. The web backend stores results in Supabase JSONB. These are three different storage backends all writing pipeline artifacts. A `StorageWriter` protocol (with `write(path, content)`, `read(path)`, `exists(path)`) injected into `OutputManager` would unify them. Impact: **medium**. [`m002-engine.md`, L41, L89; `engine/output.py`, L53-60]

- **Per-phase model routing in EngineConfig**: `dispatch_phase()` accepts a single `model` string applied to all agents in all phases. Spec 019 (config optimizer) needs to assign different models per phase (e.g., cheaper model for review, expensive for synthesis). `EngineConfig` already has the structure to support `phase_models: dict[str, str]` -- the config parser just needs to read it and `dispatch_phase` needs to look it up. This was flagged as FR-020 PARTIAL in M002 and M003. Impact: **medium**. [`m002-engine.md`, L16; `m003-provider-cli-sdk.md`, L15; `engine/dispatch.py`, L29-38]

- **Provider capability negotiation**: `ModelProvider.complete()` is text-in, text-out. Spec 019 needs to know whether a model supports structured output or tool use before assigning it to a phase. A `capabilities()` method returning a frozen set of capability tokens (`"text"`, `"tool_use"`, `"structured_output"`, `"vision"`) would let the optimizer make informed assignments. This does not require changing existing providers -- they just return `{"text"}`. Impact: **medium**. [`m002-engine.md`, L74; `engine/providers/__init__.py`, L24-28]

- **Separate debate_transcript from full_analysis**: Both M001 and the global synthesis note that `debate_transcript == full_analysis` (G32). Spec 015 (feature extraction) needs per-phase artifacts separately -- Phase 3 revisions for disposition extraction, Phase 4 disputes for count extraction, Phase 5 synthesis for convergence assessment. If these are all concatenated into `full_analysis` with no structured separation, the feature extraction pipeline has to re-parse markdown to find phase boundaries. Emitting a `StructuredDeliberation` with per-phase sections would make feature extraction deterministic and fast. Impact: **medium**. [`m001-foundation.md`, L58; `global-synthesis.md`, L95]

- **Per-agent outputs in SDK Result**: The SDK `Result` model exposes `written_files` and `output_dir` but not `per_agent_outputs: dict[str, dict[str, str]]` mapping agent names to their phase outputs. Spec 015 needs per-agent position vectors. Currently this requires reading files from disk, which breaks for non-filesystem backends (web, future Supabase storage). Impact: **low**. [`m003-provider-cli-sdk.md`, L90; `engine/sdk.py`, L64-83]

---

## Off-Base Assumptions

- **"Linter/engine coupling" framed as packaging concern** (`global-synthesis.md`, L26, L79): The synthesis frames G1 as "Blocks clean packaging; confuses module ownership." This understates the problem. The dependency inversion is an architectural layering violation, not a packaging inconvenience. The engine is the core domain layer; the linter is a validation layer that operates on engine outputs. When the engine imports from the linter, the dependency arrow points from core to peripheral, which means any change to linter models (adding a new error type, changing a validation rule) can break the engine. More critically, specs 015-016 need to import from the engine to access `PipelineResult`, `EngineConfig`, and `EngineEvent` -- if engine transitively imports from linter, those specs also depend on linter, creating a diamond dependency. The correct understanding: the models in `linter/models.py` are **shared domain models** that must be extracted to a package that both linter and engine depend on, with neither depending on the other.

- **"EventEmitter is observe-only" as a P2** (`global-synthesis.md`, L94): The synthesis flags missing plugin hooks as "Needs Work for Game Engine" but rates G8 as P2. For an adoption harness that is the foundation for specs 016-019, having no hook mechanism is closer to P1. The EventEmitter cannot be repurposed as a hook system because hooks must return results (plugin output) while events are fire-and-forget. This is a different protocol, not an extension of the existing one. If lifecycle hooks are not added before merge, every game engine spec will need to modify `run_pipeline()` to inject its hook calls, creating merge conflicts and coupling between spec PRs.

- **"FR-020 per-phase routing not implemented" as acceptable debt** (`global-synthesis.md`, L112, question 4): The synthesis asks whether FR-020 is a "hard merge blocker or acceptable technical debt for v1." The answer depends on what "v1" means. If v1 is the adoption harness alone, single-model routing is fine. If v1 is the foundation for the game engine (which the synthesis implies on L87-98), then per-phase routing is structural -- the config optimizer (spec 019) cannot recommend per-phase model assignments if the engine cannot execute them. The `EngineConfig` model is the right place for `phase_models: dict[Phase, str]`, and `dispatch_phase()` already receives the phase name. The wiring is small; the debt is in the interface contract, not the implementation.

---

## Actionable Recommendations

1. **Extract shared domain models to `conversus.models`** (Priority: P1)
   - **Current state**: `linter/models.py` (L1-396) contains `Phase`, `TemplateContext` and all 7 subclasses, `ModeSchema`, `VariablesSchema`, `LintError`, and supporting types. `engine/templates.py` (L23-33), `engine/phases.py` (L49), and `engine/sdk.py` (L52-53) import from it. This creates engine -> linter dependencies in 3 locations.
   - **Proposed change**: Create `conversus/models/` package. Move `Phase`, all `TemplateContext` subclasses, `InfluenceLevel`, `ArbiterTiming`, `PathList`, `ModeSchema`, `VariablesSchema`, and `VariableDefinition` there. Leave `LintError` and `ErrorType` in `linter/models.py` (they are genuinely linter-specific). Update all imports.
   - **Rationale**: The dependency graph must be: shared models <- engine <- linter. Currently it is: linter <- engine (inverted). Every future spec (015, 016, 017, 018, 019, 020) will import from engine/; if engine transitively pulls linter, the entire package graph becomes a hairball. [`m002-engine.md`, L30-32, L87; `global-synthesis.md`, L26]
   - **Risk if ignored**: Every game engine spec PR will carry the transitive linter dependency. Any linter refactoring (e.g., adding new error types for mode-specific validation) risks breaking engine tests. Package extraction becomes exponentially harder as more code depends on the current import paths.

2. **Add lifecycle hook call sites to run_pipeline()** (Priority: P1)
   - **Current state**: `engine/phases.py` runs the 5-phase pipeline with event emission but no plugin hook points (`m002-engine.md`, L41, L72). The global synthesis rates this G8 (P2).
   - **Proposed change**: Define a `PluginHook` protocol with `execute(state, config) -> PluginResult` (matching spec 016's interface). Add 4 hook call sites in `run_pipeline()`: before Phase 1, after Phase 5 per round, after Phase 6, after all rounds. Accept an optional `hooks: dict[HookPoint, list[PluginHook]]` parameter (default empty dict). When empty, behavior is identical to current code.
   - **Rationale**: Spec 016 (`016-plugin-system/spec.md`, L50-54) requires `PRE_EXECUTION`, `POST_PHASE_5`, `POST_DELIBERATION`, and `POST_ARBITRATION` hooks. If the hook call sites are not in the pipeline when M005 merges to main, the spec 016 PR must modify the core orchestrator, which is the riskiest part of the codebase to change. Adding empty hook calls now is zero-cost and high-value.
   - **Risk if ignored**: Spec 016 becomes a large, risky PR that touches the pipeline orchestrator. Multiple spec PRs (017, 018, 019) that depend on 016 are sequentially blocked.

3. **Wire per-phase model routing in EngineConfig and dispatch** (Priority: P1)
   - **Current state**: `EngineConfig` has a single `model` field (`engine/config.py`, L60+). `dispatch_phase()` accepts a single `model: str` parameter (`engine/dispatch.py`, L29-38). FR-020 is PARTIAL in both M002 and M003 reviews.
   - **Proposed change**: Add `phase_models: dict[str, str] = {}` to `EngineConfig`. In `run_pipeline()`, resolve the model for each phase: `model = config.phase_models.get(phase_name, config.model)`. Pass the resolved model to `dispatch_phase()`. No changes to dispatch_phase's signature needed.
   - **Rationale**: Spec 019 (`019-config-optimizer/spec.md`, L30-35) defines `mode` as a decision variable but the optimizer also needs to recommend per-phase model assignments. If the engine cannot route models per phase, the optimizer's recommendations are artificially constrained to single-model configurations.
   - **Risk if ignored**: The config optimizer (spec 019) launches with single-model-only support, limiting its optimization space and the value it delivers.

4. **Introduce StorageWriter protocol for OutputManager** (Priority: P2)
   - **Current state**: `OutputManager` (`engine/output.py`, L53+) writes directly to filesystem via `Path.write_text()` and `shutil.move()`. The web backend stores to Supabase JSONB. These are two separate write paths for the same data.
   - **Proposed change**: Define `StorageWriter` protocol with `write(rel_path: str, content: str) -> None` and `read(rel_path: str) -> str`. `OutputManager` accepts an optional `writer: StorageWriter` (default: `FilesystemWriter`). Web backend provides `SupabaseWriter`. Future scenario storage (spec 020) provides `ScenarioWriter`.
   - **Rationale**: Three current or planned backends all write pipeline artifacts. Without abstraction, each new backend duplicates path logic and the OutputManager's `retroactive_move_to_round_1()` mutation cannot work for non-filesystem storage. [`m002-engine.md`, L89; `m005-web-interface.md`, L101]
   - **Risk if ignored**: Spec 020 (scenario storage) and web backend evolution require ad-hoc workarounds around OutputManager's filesystem assumptions.

5. **Fix BYOK key injection via constructor instead of os.environ** (Priority: P1)
   - **Current state**: The web backend temporarily sets the API key as a process-level environment variable during request handling (`m005-web-interface.md`, L48-51). This is a race condition under concurrent requests and briefly exposes the key in the process environment.
   - **Proposed change**: Pass the API key directly to the provider constructor. `AnthropicProvider.__init__` and `OpenAIProvider.__init__` should accept an optional `api_key: str` parameter that takes precedence over environment variables. `resolve_provider()` in `engine/auth.py` should accept and forward this parameter.
   - **Rationale**: The `ModelProvider` protocol already abstracts provider construction. Provider instances are per-request in the web backend; constructing with the key is natural and thread-safe. [`m005-web-interface.md`, L113; `global-synthesis.md`, L28]
   - **Risk if ignored**: Key leakage between concurrent requests. A user's API key is used for another user's deliberation. This is a security and trust violation that undermines BYOK's entire value proposition.

6. **Fix OAuth state validation** (Priority: P1)
   - **Current state**: Anthropic code-paste flow generates a `state` parameter but never compares the returned state to the locally generated value (`m004-cli-polish.md`, L46-48). The code sends `state_returned` to the server but skips local comparison.
   - **Proposed change**: After parsing the code-paste input, assert `state_returned == state_local`. If they differ, abort with an error message explaining the CSRF risk.
   - **Rationale**: This is a one-line fix for a real security vulnerability. OAuth 2.0 state validation prevents CSRF attacks where an attacker tricks the user into authorizing with the attacker's code. [`m004-cli-polish.md`, L92; `global-synthesis.md`, L27]
   - **Risk if ignored**: CSRF vector in the authentication flow. While exploitation requires social engineering, the fix is trivial and the vulnerability is well-understood.

7. **Fix RLS / user_id mismatch in Supabase migration** (Priority: P1)
   - **Current state**: Migration 002 creates RLS policies requiring `auth.uid() = user_id`, but the backend never populates `user_id` when inserting deliberations (`m005-web-interface.md`, L30-32, L55-56`).
   - **Proposed change**: Either (a) use a service role key for backend operations (bypasses RLS), or (b) populate `user_id` from the anonymous session, or (c) replace the user-scoped policy with a backend-specific policy. Option (a) is simplest for the current anonymous-user model.
   - **Rationale**: This is a functional bug. If migration 002 is applied, all backend inserts and reads fail. The web interface is non-functional in production. [`m005-web-interface.md`, L114; `global-synthesis.md`, L30]
   - **Risk if ignored**: Web interface does not work in production.

8. **Extend ModelProvider with optional capabilities() method** (Priority: P2)
   - **Current state**: `ModelProvider` protocol defines `complete()` and `stream()` only (`engine/providers/__init__.py`, L17-28). No mechanism to query what a model supports.
   - **Proposed change**: Add `def capabilities(self) -> frozenset[str]` to the protocol with a default implementation returning `frozenset({"text"})`. Future providers return additional capabilities: `{"text", "tool_use"}`, `{"text", "structured_output"}`. Make it optional via `hasattr` check for backward compatibility.
   - **Rationale**: Spec 019 (config optimizer) needs to know model capabilities to make per-phase assignments. Spec 015 (feature extraction) could benefit from structured output mode. Without capability negotiation, the optimizer has no information to differentiate models. [`m002-engine.md`, L74, L91; `019-config-optimizer/spec.md`, L30-35]
   - **Risk if ignored**: Config optimizer treats all models as equivalent, producing suboptimal recommendations.

9. **Remove unsupported phase choices from CLI --phase** (Priority: P2)
   - **Current state**: `run --phase` offers `click.Choice` values including cross-review, revision, disputes, synthesis, but only "all" and "review" are implemented (`m003-provider-cli-sdk.md`, L66-67). Users selecting advertised options get a `ValueError`.
   - **Proposed change**: Remove unimplemented values from the `click.Choice` list. Add them back when the corresponding phase execution paths are implemented.
   - **Rationale**: Advertising features that crash is worse than not advertising them. This is a small fix that prevents user confusion and support burden. [`m003-provider-cli-sdk.md`, L96; `global-synthesis.md`, L29]
   - **Risk if ignored**: Users discover the feature, try it, get an error, and lose trust in the tool.

10. **Replace OutputManager.retroactive_move_to_round_1() with immutable pattern** (Priority: P2)
    - **Current state**: When a second round starts, `OutputManager` mutates `self.output_dir` by moving all Round 1 files into a `round-1/` subdirectory (`m002-engine.md`, L26, L56`). Any reference to the original `output_dir` becomes stale.
    - **Proposed change**: Construct multi-round directory structure upfront when `config.rounds > 1`. The first round writes to `{output}/round-1/` from the start. No retroactive move needed. For single-round runs, flat layout is preserved.
    - **Rationale**: Mutable state in the output manager is a footgun that becomes more dangerous as more consumers hold references to output paths (plugins, feature extraction, scenario storage). The retroactive move also cannot work for non-filesystem backends. [`m002-engine.md`, L56, L92; `engine/output.py`, L22-34]
    - **Risk if ignored**: Stale path references cause intermittent bugs that are hard to diagnose. Non-filesystem storage backends cannot implement retroactive moves.

---

## Referenced Documentation

- `global-synthesis.md` -- sections/lines cited: L26, L27, L28, L29, L30, L72, L73, L79, L87-98, L89, L91, L94, L95, L112
- `reviews/m001-foundation.md` -- sections/lines cited: L28, L58
- `reviews/m002-engine.md` -- sections/lines cited: L16, L24, L26, L30-32, L37, L41, L46-50, L56, L72, L74, L87, L89, L91, L92
- `reviews/m003-provider-cli-sdk.md` -- sections/lines cited: L15, L66-67, L90, L96
- `reviews/m004-cli-polish.md` -- sections/lines cited: L28-30, L46-48, L92
- `reviews/m005-web-interface.md` -- sections/lines cited: L30-32, L48-51, L55-56, L101, L113, L114
- `engine/templates.py` -- lines cited: L23-33
- `engine/phases.py` -- lines cited: L49
- `engine/sdk.py` -- lines cited: L52-53, L64-83
- `engine/providers/__init__.py` -- lines cited: L16-30, L24-28
- `engine/config.py` -- lines cited: L34-60
- `engine/events.py` -- lines cited: L79-113
- `engine/output.py` -- lines cited: L22-34, L53-60
- `engine/dispatch.py` -- lines cited: L29-38
- `linter/models.py` -- lines cited: L1-396, L248
- `specs/016-plugin-system/spec.md` -- lines cited: L50-54
- `specs/019-config-optimizer/spec.md` -- lines cited: L30-35
- `specs/015-feature-extraction/spec.md` -- lines cited: FR-001, FR-002
