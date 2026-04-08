# Conversus Spec Status

## Taxonomy

Status uses two tiers measuring different dimensions.

### Implementation Tier

Tracks whether a spec's functional requirements (FRs) are represented in SKILL.md.

- **Implementation-complete**: All FRs from this spec are represented in SKILL.md.
- **Partially-complete**: Some FRs are implemented, others remain. Specific gaps listed.
- **Not started**: No SKILL.md representation exists for this spec's features.

Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., "Implementation-complete (core) / Not started (discovery)"). Each component must use a defined implementation-tier label.

### Acceptance Tier

Tracks whether a spec's own acceptance criteria are met.

- **Feature-complete**: All major capabilities are present, but acceptance criteria gaps remain (e.g., missing template instructions, incomplete edge case documentation).
- **Spec-complete**: All acceptance criteria are met. The spec is fully satisfied.
- **Not assessed**: No acceptance criteria have been evaluated.

Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability.

### Interpreting the Two Tiers

The tiers are orthogonal. A spec can be implementation-complete (all FRs in SKILL.md) but only feature-complete (some acceptance criteria gaps remain). Conversely, a spec can be partially-complete in implementation but spec-complete for the subset it covers. Dependencies are also orthogonal — a spec can be implementation-complete while depending on another spec's correctness for composed behavior.

---

## Status

### 001 — Subject Arbitration
**Implementation**: Partially-complete | **Acceptance**: Feature-complete
**Gaps**: FR-023 (output validation — SKILL.md validation logic exists but template-level heading instructions pending), FR-025 (per-FR citation instructions), FR-026 (per-file attribution instructions)
**Notes**: Core Phase 6 execution, config validation, trigger evaluation, failure handling, and structural markers are all implemented. Remaining gaps are template-level behavioral instructions.
**Risk-of-Gap**: Disputes remain unresolved after deliberation; manual post-processing needed to extract actionable decisions from raw synthesis output.
**Effort**: Small — 2 FRs remain (template-level instructions for FR-025 per-FR citation and FR-026 per-file attribution). FR-023 engine logic exists; template instructions pending.

### 002 — Recursive Rounds
**Implementation**: Implementation-complete | **Acceptance**: Spec-complete
**Depends On**: `001-subject-arbitration` (shared dispute-parsing subsystem — stagnation detection FR-021 reuses spec 001's structural markers and heading-based parsing per FR-011)
**Notes**: All 36 FRs represented in SKILL.md. Cross-round synthesis template exists. Runtime correctness of stagnation detection depends on spec 001's parsing subsystem.
**Risk-of-Gap**: Single-pass deliberation only; no iterative convergence improvement. Complex multi-perspective topics may not reach consensus in one round.
**Effort**: None — complete. All 36 FRs implemented. No remaining work.

### 004 — Preset Agents
**Implementation**: Implementation-complete | **Acceptance**: Spec-complete
**Core (FR-001–021)**: Engine-level preset resolution, composition, validation, caching, arbiter support — all implemented. 18 preset files across 6 categories.
**Gaps**: None — all 21 core FRs satisfied. Discovery commands (former FR-022–024) tracked in ideas.md.
**Notes**: US-6 (arbiter preset interaction) is implemented. US-5 (preset-aware guided workflow) belongs to spec 008.
**Risk-of-Gap**: None — core engine complete.
**Effort**: None — complete.

### 005 — P2/P3 Backlog Hardening
**Implementation**: Implementation-complete | **Acceptance**: Spec-complete
**Gaps**: None — all 19 FRs satisfied.
**Depends On**: `001-subject-arbitration` (documents spec 001 implementation state), `002-recursive-rounds` (documents spec 002 implementation state), `004-preset-agents` (documents spec 004 implementation state)
**Notes**: All 19 FRs implemented. STATUS.md enriched with two-tier taxonomy, shared subsystems, dependencies, risk-of-gap, effort estimates, and SKILL.md structure plan.
**Risk-of-Gap**: None — all documentation and validation gaps are closed.
**Effort**: None — complete.

### 006 — Inter-Round Arbitration
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `001-subject-arbitration` (Phase 6 engine), `004-universal-rounds` (multi-round execution), `005-generalized-templates` (schema variables pre-provisioned)
**Scope**: Two new arbiter config fields: `timing` (final | inter-round) and `influence` (binding | recommended | advisory). Phase 6 fires between rounds when `timing: inter-round`. Influence level controls arbiter authority — from dictator (binding) to observer (advisory).
**Risk-of-Gap**: Multi-round deliberations waste rounds on intractable disputes that an inter-round arbiter could clear early. Binary authority model (binding only) reduces agent incentive to self-resolve.
**Effort**: Medium — 23 FRs across schema extension, execution model changes, influence-aware dispute counting, cross-round context injection, and template adaptations.

### 007 — Subcommand Dispatch & Problem Definition
**Implementation**: Implementation-complete | **Acceptance**: Feature-complete
**Gaps**: None — all 12 FRs satisfied.
**Depends On**: None (foundational)
**Notes**: Subcommand dispatch routing added to SKILL.md. `/conversus define` handler implemented with problem type classification, context ingestion, and structured problem.md output.
**Risk-of-Gap**: None — foundational infrastructure complete.
**Effort**: None — complete.

### 008 — Interest Discovery & Mode Selection
**Implementation**: Implementation-complete | **Acceptance**: Feature-complete
**Depends On**: `007-subcommand-dispatch-define` (dispatch, problem.md), `004-preset-agents` (soft — preset suggestions)
**Gaps**: None — all 13 FRs satisfied (FR-001 through FR-013).
**Notes**: `/conversus interests` handler reads `problem.md`, generates calibrated interests with preset matching (spec 004), produces `interests.md`. `/conversus mode` handler reads both artifacts, applies decision matrix with heuristic fallback, generates valid `conversus.yml` using the same schema as hand-crafted configs. Both handlers include missing prerequisite routing, existing file checks, user confirmation, and post-write validation.
**Risk-of-Gap**: None — both commands are fully implemented with all constraint handling.
**Effort**: None — complete.

### 009 — Guided Execution
**Implementation**: Implementation-complete | **Acceptance**: Feature-complete
**Depends On**: `008-interests-mode` (generates conversus.yml)
**Gaps**: None — all 10 FRs satisfied (FR-001 through FR-010).
**Notes**: `/conversus converge` handler implemented as thin UX wrapper around `/conversus run`. Pre-execution summary with plain-language mode explanation, agent summaries, and launch estimate. User confirmation gate. Missing prerequisite routing to define/interests/mode. Staleness warning for interests.md vs conversus.yml. Post-execution report with mode-specific interpretation guidance, dispute status, and suggested next steps.
**Risk-of-Gap**: None — pure UX wrapper with no engine logic.
**Effort**: None — complete.

### 010 — Guided Arbitration
**Implementation**: Implementation-complete | **Acceptance**: Feature-complete
**Depends On**: `001-subject-arbitration` (hard gate — spec-complete required), `006-inter-round-arbitration` (influence levels), `009-guided-execution`
**Gaps**: None — all FRs satisfied.
**Notes**: `/conversus arbitrate` handler implemented with dispute detection, guided arbiter configuration (identity, prompt generation, grounding document, influence level), config generation and append to `conversus.yml`, Phase 6 execution delegation, and post-arbitration plain-language ruling summaries. Supports `--force` flag for no-dispute arbitration and existing arbiter config detection with reuse/reconfigure/cancel flow. Grounding document generation from `problem.md` constraints and success criteria.
**Review findings applied**: Conversus review P1s (YAML-aware serialization, template validation in Step 5, grounding document quality validation) and high-impact P2s (--force + existing arbiter, first-time guidance, config backup, name collision check, grounding overwrite protection, influence mapping table, timing field, structural ruling extraction, prerequisite check scope, Phase 6 failure handling in post-arbitration report, all arbiter fields in existing-config display) applied to SKILL.md.
**Risk-of-Gap**: None — thin UX wrapper over Phase 6 engine with no new arbitration logic.
**Effort**: None — complete.

### 011 — Phase Consensus Gates
**Implementation**: Implementation-complete | **Acceptance**: Feature-complete
**Depends On**: `007-subcommand-dispatch-define` (dispatch), `004-preset-agents` (preset resolution)
**Gaps**: None — all 12 FRs satisfied (FR-001 through FR-012).
**Notes**: `/conversus gate` handler implemented with config-based and inline (ad-hoc) invocation, gate configuration parsing (`gates.yml` or `gates:` section in `conversus.yml`), three pass criteria (converged, max_disputes N, always), machine-readable `gate-result.md` output, exit codes (0/1/2) for CI/CD, re-run attempt history preservation, and engine-independent orchestration that generates standard `conversus.yml` configs.
**Review findings applied**: Conversus review P1s (two-tier error handling for Dispute-Parsing failures, max_disputes non-negative integer validation, gate config example clarified for 2-agent minimum) and high-impact P2s (CLI flag override precedence, stagnation in gate config schema, --force-pass bypass with scope boundary, validate_templates pass-through) applied to SKILL.md.
**Risk-of-Gap**: None — thin orchestration layer with no engine modifications.
**Effort**: None — complete.

### 012 — Game Form Schema Library
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `005-generalized-templates` (schema foundation)
**Scope**: YAML schemas for standard game theory forms (normal-form, GNEP, parametric, Stackelberg) plus Pydantic validation models. Mode-to-form mapping. Ships in `conversus-schemas` package. Pure schema — no solver dependency.
**Risk-of-Gap**: Without formal game form definitions, the plugin system has no shared vocabulary for game structure. Each plugin would define its own ad-hoc representations.
**Effort**: Small — 4 YAML schema files, 4 Pydantic models, 1 mode-mapping file.

### 013 — Objective Function Template Library
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `012-game-form-schemas` (game form Pydantic models, YAML conventions)
**Scope**: ~20-30 curated objective function templates as YAML files with Pydantic validation. Per-mode templates (cooperative, WTA, PD, red-blue) plus cross-mode templates (budget-constrained, general quadratic/linear). Standard constraint templates (budget, capacity, mutual exclusivity). Ships in `conversus-schemas` package.
**Risk-of-Gap**: Without templates, objective function construction (spec 014) would need to generate functions from scratch — unreliable and non-reproducible.
**Effort**: Medium — ~25 YAML template files, constraint templates, Pydantic models, mathematical validation of each template.

### 014 — Guided Objective Function Construction
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `013-objective-function-templates` (template library), `008-interests-mode` (mode selection)
**Scope**: 3-stage pipeline: symbolic logic parsing (deterministic) -> LLM gap-filling (interactive) -> objective function assembly (deterministic). Produces `objective.yml`. Optional integration with `/conversus mode`. Ships in `conversus-schemas` package.
**Risk-of-Gap**: Without guided construction, users must manually parameterize objective functions — requiring mathematical expertise that the guided workflow (007-010) was designed to eliminate.
**Effort**: Medium — parsing rules, gap-filling pipeline, assembly logic, integration point with mode handler.

### 015 — Feature Extraction Pipeline
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `012-game-form-schemas` (game form definitions), `013-objective-function-templates` (parameter types)
**Scope**: Deterministic text-to-vector extraction from deliberation artifacts. Per-mode feature schemas (cooperative, WTA, PD, red-blue). Parses Phase 3 revisions, Phase 4 disputes, Phase 5 synthesis. Produces `features.json`. Ships as `conversus-features` package. Dependencies: pyyaml, pydantic only.
**Risk-of-Gap**: Without feature extraction, the equilibrium scorer and convergence predictor cannot operate — they need numerical vectors, not markdown text.
**Effort**: Medium — per-mode extraction rules, structured parsing, Pydantic schemas, CLI interface.

### 016 — Plugin System Infrastructure
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: None (infrastructure foundation)
**Scope**: Plugin base class, lifecycle hooks (PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, POST_ARBITRATION), DeliberationState interface, PluginResult type, plugin loading via importlib, `plugins:` config section, `{output}/plugins/` output namespace. Constitution Principle XV grounding. Ships as `conversus-plugins` package.
**Risk-of-Gap**: Without the plugin framework, specs 017-019 cannot exist. The game engine evolution has no extension point.
**Effort**: Medium — base class, hook system, state interface, loading mechanism, config parsing, output namespacing.

### 017 — Equilibrium Scorer Plugin (nashopt)
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `015-feature-extraction` (feature vectors), `016-plugin-system` (Plugin base class, hooks)
**Scope**: First paid plugin. Computes Nash equilibrium quality score (0.0-1.0) using nashopt's `check_equilibrium()`. Per-mode payoff functions. Hooks: POST_PHASE_5, POST_DELIBERATION. Ships as `conversus-nashopt` package. Dependencies: nashopt, jax, scipy, conversus-features.
**Risk-of-Gap**: Without equilibrium scoring, deliberation quality is subjective — users read synthesis and guess whether the outcome is stable.
**Effort**: Medium — payoff function definitions per mode, nashopt integration, plugin wiring, output formatting.

### 018 — Convergence Predictor Plugin (nashopt)
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `015-feature-extraction` (feature vectors), `016-plugin-system` (Plugin base class), `017-equilibrium-scorer` (same package, shared payoff functions)
**Scope**: Predicts whether next round will reduce disputes. Uses gnep-learn Kalman-filtered surrogate models. Outputs: prediction (converge/stagnate/uncertain), confidence, estimated rounds remaining. Hook: POST_PHASE_5. Ships in `conversus-nashopt` package. Advisory only — recommend-then-confirm (decision Q2).
**Risk-of-Gap**: Without convergence prediction, users guess whether additional rounds are worth the token cost. Wasted rounds on stagnated deliberations.
**Effort**: Medium — surrogate model construction, fixed-point detection, confidence calibration, heuristic fallback.

### 019 — Config Optimizer Plugin (AMPL)
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `014-guided-objective-construction` (objective function input), `016-plugin-system` (Plugin base class, PRE_EXECUTION hook)
**Scope**: Mixed-integer programming via AMPL to compute optimal conversus config (rounds, agents, mode, iterations) given budget and quality threshold. HiGHS solver bundled (free). Also supports general-purpose MIP/NLP/MINLP problems. Hook: PRE_EXECUTION. Ships as `conversus-ampl` package.
**Risk-of-Gap**: Without config optimization, users manually guess config parameters. Suboptimal configs waste tokens or produce poor outcomes.
**Effort**: Large — AMPL model formulation, quality estimation model, solver integration, general-purpose optimization API.

### 020 — Scenario Storage & Replay
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `016-plugin-system` (plugin hooks for save/load)
**Scope**: Store game configurations (mode, objective, parameters, agent roles) as reusable YAML scenarios. Swap data bindings for replay. Run history for audit. Commands: `/conversus save`, `/conversus replay`, `/conversus scenarios`. Cross-run analysis. ScenarioStore protocol for future database backends. File-based storage (decision Q7).
**Risk-of-Gap**: Without scenario storage, recurring decision types require full reconfiguration each time. No institutional memory of how decisions are made.
**Effort**: Medium — scenario schema, save/replay/list commands, run history append, cross-run analysis, ScenarioStore protocol.

## SKILL.md Structure Plan

Documents how SKILL.md accommodates future spec implementations.

### 002 — Recursive Rounds
**Status**: Already integrated
**Sections**: Rounds configuration (Step 1 config parsing), round termination check, cross-round synthesis template, stagnation detection, multi-round completion report. Dispute-parsing subsystem section handles round-level dispute counting.

### 006 — Inter-Round Arbitration
**Status**: Needs new sections
**Changes required**:
- `timing` and `influence` fields in Step 1 config parsing
- Phase 6 insertion in round loop (between Phase 5 synthesis and termination check)
- Influence-aware dispute counting in termination check
- `{PRIOR_ARBITRATION_SECTION}` and `{INFLUENCE_LEVEL}` template variables
- Per-round arbitration output paths

### 007 — Subcommand Dispatch & Define
**Status**: Already integrated
**Sections**: Subcommand dispatch routing before Step 1, entry point routing logic distinguishing subcommand invocations from `/conversus run`, `/conversus define` handler producing `problem.md` with problem type classification and context ingestion.

### 008 — Interests & Mode
**Status**: Already integrated
**Sections**: `/conversus interests` handler with interest generation calibrated by problem type, preset matching (spec 004), ungrounded agent warnings, and `interests.md` output. `/conversus mode` handler with decision matrix, heuristic mode detection, mixed-signal handling, user override with trade-off explanation, and `conversus.yml` generation using the run engine's schema. Both handlers include missing prerequisite routing, existing file checks, user confirmation, and post-write validation.

### 009 — Guided Execution
**Status**: Already integrated
**Sections**: `/conversus converge` handler with missing prerequisite routing, staleness warning, plain-language pre-execution summary with confirmation gate, delegation to `/conversus run`, and post-execution report with mode-specific interpretation guidance, dispute status assessment, and suggested next steps.

### 010 — Guided Arbitration
**Status**: Already integrated
**Sections**: `/conversus arbitrate` handler with dispute detection via Dispute-Parsing Subsystem, guided arbiter configuration (identity prompt generation, grounding document setup with `problem.md` fallback, influence level selection), config generation and append to `conversus.yml`, Phase 6 execution delegation, and post-arbitration plain-language ruling summaries. Dispatch table updated with `arbitrate` routing.

### 011 — Phase Consensus Gates
**Status**: Already integrated
**Sections**: `/conversus gate` handler with config-based and inline invocation, gate configuration parsing (`gates.yml` / `gates:` section), pass criteria evaluation via Dispute-Parsing Subsystem, `gate-result.md` structured output, exit codes, re-run attempt preservation, and post-execution reporting. Dispatch table updated with `gate` routing.

### 004 — Preset Agents
**Status**: Already integrated
**Sections**: Preset resolution in Step 1 config parsing (single preset, composition, qualified/unqualified names), preset validation, caching, arbiter preset support. 18 preset files across 6 categories in `presets/` directory.

## Shared Subsystems

### Dispute-Parsing Subsystem
**Location**: SKILL.md section "Dispute-Parsing Subsystem"
**Stability**: Stable
**Consumers**: spec 001 (trigger evaluation), spec 002 (stagnation detection), spec 010 (arbitrate dispute detection), spec 011 (gate pass/fail)
**Interface**: Input — synthesis file path; Output — boolean (has disputes) for trigger evaluation, integer (dispute count) for stagnation detection and gate evaluation. Parsing rules: structural markers primary (`DISPUTES_BEGIN`/`DISPUTES_END`), heading-based fallback per mode.
**Notes**: Stagnation detection (spec 002) does not support structural-marker parsing — it uses only heading-based parsing. Heading-match semantics for the dispute-parsing fallback are not explicitly specified in the subsystem documentation.

### Structural Markers
**Stability**: Stable

- `DISPUTES_BEGIN` / `DISPUTES_END`: Delimit dispute sections in synthesis output. Consumers: spec 001, spec 002, synthesis templates.
- `TEMPLATE_STATUS`: Marks non-production templates as draft. Consumers: spec 005, all arbitration templates.

### Template Conventions
**Stability**: Stable
**Consumers**: All specs
**Interface**: `{VARIABLE}` substitution syntax, mode-specific template selection (`templates/{mode}/`), standardized output sections per mode.

## Cross-Spec Dependencies

### Dependency Graph

```
Engine Layer (done/in-progress):
001 Subject Arbitration ──→ (none — foundational)
002 Recursive Rounds ────→ 001 (shared dispute-parsing subsystem)
004 Preset Agents ───────→ (none — self-contained engine) ✓ complete
005 P2/P3 Hardening ────→ 001, 002, 004 (documents existing implementations) ✓ complete
006 Inter-Round Arb ─────→ 001, 004-universal-rounds, 005-generalized-templates

Guided Workflow Layer (007-010):
007 Dispatch & Define ───→ (none — foundational for workflow layer) ✓ complete
008 Interests & Mode ────→ 007, 004 (soft: preset suggestions) ✓ complete
009 Guided Execution ────→ 008 ✓ complete
010 Guided Arbitration ──→ 001 (hard gate: spec-complete), 006, 009 ✓ complete

Automation Layer:
011 Phase Gates ─────────→ 007 (dispatch), 004 (presets) ✓ complete

Game Engine Layer (012-020):
012 Game Form Schemas ───→ 005 (schema foundation)
013 Objective Templates ─→ 012
014 Guided Objective ────→ 013, 008
015 Feature Extraction ──→ 012, 013
016 Plugin System ───────→ (none — infrastructure foundation)
017 Equilibrium Scorer ──→ 015, 016
018 Convergence Pred. ───→ 015, 016, 017
019 Config Optimizer ────→ 014, 016
020 Scenario Storage ────→ 016
```

### Recommended Implementation Order

**Engine/Workflow/Automation (006-011):**

**006 → 007 → 008 → 009 → 010 → 011**

- **006 current**: Inter-round arbitration — establishes lifecycle hook pattern and influence levels.
- **007 done**: Subcommand dispatch and `/conversus define` implemented.
- **008 done**: Interest discovery and mode selection implemented. `/conversus interests` and `/conversus mode` transform problem.md into a runnable config.
- **009 done**: Guided execution implemented. `/conversus converge` wraps the run engine with pre/post UX.
- **010 done**: Guided arbitration implemented. `/conversus arbitrate` provides guided arbiter configuration and Phase 6 invocation.
- **011 done**: Phase consensus gates implemented. `/conversus gate` provides config-based and inline gate execution with CI/CD exit codes.

**Note**: All guided workflow specs (007-011) are implementation-complete. The only remaining spec in the implementation order is 006 (inter-round arbitration).

**Game Engine (012-020):**

**Phase 1 (schemas): 012 → 013 → 014**
**Phase 2 (infrastructure): 016 (parallel with Phase 1)**
**Phase 3 (extraction): 015 (after 012, 013)**
**Phase 4 (plugins): 017 → 018, 019, 020 (after 015, 016)**

- **012**: Game form schemas — mathematical vocabulary for all subsequent specs. Start here.
- **013**: Objective function templates — curated library of ~25 parameterized forms. Builds on 012.
- **014**: Guided objective construction — 3-stage pipeline from natural language to parameterized objectives. Builds on 013 and 008.
- **016**: Plugin system infrastructure — can be built in parallel with 012-013. No dependencies.
- **015**: Feature extraction — bridge between text and numbers. Needs 012 and 013 for schemas.
- **017**: Equilibrium scorer — first paid plugin. Needs 015 and 016.
- **018**: Convergence predictor — same package as 017. Needs 015, 016, 017.
- **019**: Config optimizer — AMPL-based. Needs 014 and 016. Parallel with 017-018.
- **020**: Scenario storage — file-based replay. Needs 016. Parallel with 017-019.

**Note**: Game engine specs are code specs (Python packages, pip installable), not SKILL.md edits. They represent a future evolution of conversus from template orchestrator to pluggable game engine. See `specs/archive/game-engine-vision/` for the original monolithic vision that these specs decompose.

---

*Updated: 2026-03-22 (specs 010, 011 conversus review findings applied to SKILL.md)*

---

*Maintenance obligation: This document MUST be updated when any spec's implementation or acceptance status changes (FR-008a).*
