# Game Engine Advocate Review: Spec 005 (Generalized Template Schema, Variables, and Linter)

**Reviewer role**: game-engine-advocate (spec 007)
**Target**: spec 005 — schema/variables.yml, schema/modes/*.yml, linter/models.py, linter/validate.py
**Date**: 2026-03-21

---

## Executive Summary

Spec 005 introduces the foundational schema and linter architecture that spec 007's pluggable game engine will build on. The variable schema (`variables.yml`), mode schemas (`modes/*.yml`), and Pydantic models (`models.py`) establish a machine-readable contract for template variables. This is a prerequisite for spec 007's plugin system, which needs to inject new variables at lifecycle hooks (PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, POST_ARBITRATION) and introduce objective function templates that define custom variables per scenario.

The current implementation is solid for its stated scope but architecturally closed. The `VALID_VARIABLE_TYPES`, `VALID_PHASES`, and `VALID_MODES` are frozen sets in `models.py` (L23-35). The `TemplateContext` base model uses `extra = "forbid"` (L140), which means a plugin cannot inject a new variable without modifying the core. The mode schema structure has no extension point for plugin-contributed sections. These are not bugs in spec 005 -- they are correct for a closed system -- but they create real friction for spec 007's plugin architecture unless addressed now. Every one of these constraints will need to be relaxed or wrapped in an extension mechanism before a single plugin can function.

The single most important recommendation: add a documented extension mechanism (a `custom_variables` namespace or `extra = "allow"` model variant) so that plugins can register new template variables without modifying `models.py` or `variables.yml` core definitions.

---

## Alignment

- **[Variable registry as structured data]** (spec 005 `variables.yml`, L25-416): The YAML registry of all template variables with types, phases, and mode assignments directly supports spec 007's feature extraction pipeline (spec 007 `spec.md`, L164-177), which maps deliberation artifacts to numerical vectors. Having structured metadata about what each variable contains (type: `path-list` vs `extracted-content` vs `string`) lets the feature extractor know what to parse without inspecting templates. This is foundational.

- **[Mode schema separation]** (spec 005 `schema/modes/*.yml`): Each mode defining its own dispute headings, structural markers, and arbitration headings maps cleanly to spec 007's per-mode payoff function definitions (spec 007 `spec.md`, L180-187). The mode schema is the natural place to attach objective function template references when spec 007 ships.

- **[Pydantic model hierarchy]** (`models.py`, L129-270): The `TemplateContext` base class with per-phase subclasses (`ReviewContext`, `SynthesisContext`, etc.) establishes a typed contract that spec 007's `DeliberationState` (spec 007 `spec.md`, L138-146) can consume. The phase context models already capture exactly the data the feature extraction pipeline needs -- agent names, paths to review artifacts, dispute content.

- **[Linter as development-time validation]** (`validate.py`, L281-305): The composable validation architecture (pure functions that return error lists) is compatible with spec 007's need for plugin-aware validation. A plugin that introduces new template variables could provide its own validation function composed alongside the existing ones.

- **[`PHASE_CONTEXT_MODELS` registry]** (`models.py`, L262-270): The dict mapping phase names to context model classes is the exact pattern spec 007 needs for registering plugin-contributed context models. A plugin could extend this registry at load time.

- **[Conditional variable support via `modes` field]** (`variables.yml`, L389-416): The `modes` field on variable definitions (e.g., `AGENT_ROLE` scoped to `red-blue`) demonstrates that the schema already handles conditional presence. Spec 007's plugin-injected variables need the same mechanism -- a variable present only when a specific plugin is active.

---

## Missed Opportunities

- **[No plugin namespace in variable schema]**: `variables.yml` has no mechanism for a plugin to register its own variables. Spec 007's objective function templates (spec 007 `spec.md`, L412-448) define custom parameters (`w_i`, `score_i`, `penalty`, `overlap`) that need to flow into templates as variables. Today, adding a variable requires editing `variables.yml` and `models.py` -- core files that plugins should not modify. A `plugins` or `custom_variables` namespace in the schema would let plugins declare variables without touching core. **Impact: high.**

- **[`extra = "forbid"` blocks plugin injection]**: `TemplateContext` and all subclasses use `model_config = {"extra": "forbid"}` (`models.py`, L140). This is correct for preventing typos in core variables but prevents plugins from adding fields to the context. Spec 007's `DeliberationState` (spec 007 `spec.md`, L138-146) needs to carry plugin-specific data (equilibrium scores, convergence predictions) alongside core variables. Either a parallel context model or `extra = "allow"` on a plugin-aware variant is needed. **Impact: high.**

- **[No variable type for numerical/float]**: `VALID_VARIABLE_TYPES` (`models.py`, L23-26) includes `string`, `integer`, `path`, `path-list`, `conditional-block`, `extracted-content`. Spec 007's feature extraction produces numerical vectors (spec 007 `spec.md`, L164-177) -- concession rates (float), severity scores (float), equilibrium quality (float 0.0-1.0). There is no `float` or `number` type. Plugin-contributed variables carrying numerical data would need to abuse `string` type. **Impact: medium.**

- **[No hook point metadata in phase definitions]**: Spec 007 defines lifecycle hooks at specific points in the deliberation flow: `PRE_EXECUTION`, `POST_PHASE_5`, `POST_DELIBERATION`, `POST_ARBITRATION` (spec 007 `spec.md`, L97-112). The phase list in `VALID_PHASES` (`models.py`, L28-31) does not encode where hooks fire relative to phases. Adding hook point metadata to the schema would let plugins declare which phases they operate on and let the linter validate plugin-template compatibility. **Impact: medium.**

- **[Mode schema has no extension section]**: `ModeSchema` (`models.py`, L105-123) defines `mode`, `variables`, `templates`, `disputes`, `arbitration`, `cross_round_synthesis`. There is no `plugins` or `extensions` section where a mode could declare plugin-specific configuration. Spec 007's scenario storage (spec 007 `spec.md`, L519-563) needs mode schemas to reference objective function templates and plugin configs. Today, adding this requires modifying `ModeSchema` itself. **Impact: medium.**

- **[No schema versioning]**: Neither `variables.yml` nor `modes/*.yml` carry a version field. Spec 007's scenario replay system (spec 007 `spec.md`, L509-608) stores scenarios that reference specific variable schemas. If the schema changes between runs, replayed scenarios may use variables that no longer exist or miss new required variables. A schema version would let the replay system detect incompatibilities. **Impact: medium.**

- **[`VALID_MODES` is a frozen set, not a registry]**: `VALID_MODES` (`models.py`, L33-35) is hardcoded to four modes. Spec 005's own SC-003 (spec 005 `spec.md`, L353) envisions adding a new mode ("auction") by creating a schema file. But the Pydantic validator on `ModeSchema.mode` (`models.py`, L115-122) would reject any mode name not in the frozen set. A plugin that introduces a custom game mode (a plausible spec 007 extension) would fail validation. **Impact: low** (easily fixable, but worth noting as a contradiction between spec 005's stated goals and implementation).

- **[No support for objective function template schemas]**: Spec 007 describes a library of objective function templates stored in `schema/objectives/` (spec 007 `spec.md`, L449). The current schema directory structure (`schema/variables.yml`, `schema/modes/`) has no provision for this. The linter does not know about objective function templates. Adding linter support for validating objective function parameter completeness would be a natural extension of spec 005's validation architecture. **Impact: low** (spec 007 Phase 2+ concern, but the directory layout matters now).

- **[MODE_PRESENCE hardcoded lookup table]**: `validate.py` (L108-144) uses a manually maintained dict of 28 `(phase, mode) -> bool` entries to decide whether `{MODE}` is expected. This does not scale to plugin-introduced modes or plugin-modified phase behavior. The information should be derivable from the schema rather than hardcoded. **Impact: low.**

---

## Off-Base Assumptions

1. **The variable set is static and known at development time.** The entire spec 005 architecture assumes all variables are enumerable in `variables.yml` before any templates are written. Spec 007's plugin system fundamentally breaks this assumption: plugins can introduce variables at runtime (a convergence predictor might inject `{CONVERGENCE_SCORE}` into a synthesis template). The linter needs a concept of "this template may contain variables not in variables.yml if the corresponding plugin is declared." Without this, plugin-contributed variables will always fail linting.

2. **Modes are a closed enum.** `VALID_MODES` (`models.py`, L33-35) and the `ModeSchema.validate_mode` validator (`models.py`, L115-122) treat the four current modes as the complete set. Spec 007's long-term vision (spec 007 `spec.md`, L245-260) sees the game engine recommending modes mathematically, and spec 005's own user story US-3 AC-2 (spec 005 `spec.md`, L71) describes creating a new "auction" mode. The implementation contradicts the spec's own extensibility story.

3. **Phases are a fixed 7-element set.** `VALID_PHASES` (`models.py`, L28-31) is frozen. Spec 007 introduces lifecycle hooks that occur BETWEEN phases (POST_PHASE_5 fires between synthesis and arbitration). If a plugin needs to contribute variables to a hook-injected phase (e.g., a "plugin-analysis" phase that runs after synthesis), the current phase validator would reject it.

---

## Actionable Recommendations

1. **Add a plugin variable namespace to the schema** (Priority: P1)
   - **Current state**: `variables.yml` contains only core variables. No mechanism for external contributions (L25-416).
   - **Proposed change**: Add a top-level `plugin_variables` section (or a `namespace: core | plugin` field per variable) that the linter treats as optional. Plugin-contributed variables are validated against plugin-provided schemas, not the core schema.
   - **Rationale**: Spec 007 `spec.md` L412-448 defines objective function templates with custom parameters that need to flow as template variables. Without a plugin namespace, every plugin must fork `variables.yml`. Constitution Principle III (Backward-Compatible Extension, `constitution.md` L49-61) requires that extensions not restructure existing behavior.
   - **Risk if ignored**: Every spec 007 plugin will need to modify core schema files, creating merge conflicts and violating the plugin isolation constraint (spec 007 `spec.md`, L335-336: "Must NOT make the core depend on...").

2. **Create an extensible TemplateContext variant** (Priority: P1)
   - **Current state**: `TemplateContext` uses `extra = "forbid"` (`models.py`, L140), rejecting any field not explicitly declared.
   - **Proposed change**: Add a `PluginTemplateContext` base class (or a factory function) that inherits from `TemplateContext` but uses `extra = "allow"`. Plugins construct contexts from this variant. Alternatively, add a `plugin_data: dict[str, Any] = Field(default_factory=dict)` field to `TemplateContext` itself.
   - **Rationale**: Spec 007's `DeliberationState` (`spec.md`, L138-146) carries plugin-specific data alongside core data. The plugin API (`spec.md`, L131-157) passes state objects to plugin `execute()` methods. If the state model forbids extra fields, plugins cannot attach their data. Constitution Principle IX (Explicit Typing, `constitution.md`, L171-185) prefers Pydantic models, but a `dict[str, Any]` plugin data field is the standard escape hatch for extensibility.
   - **Risk if ignored**: Plugin authors will bypass Pydantic entirely, using raw dicts, violating Constitution Principle IX and losing type safety at the plugin boundary.

3. **Make VALID_MODES a registry, not a frozen set** (Priority: P1)
   - **Current state**: `VALID_MODES = frozenset({"cooperative", "red-blue", "winner-take-all", "prisoners-dilemma"})` (`models.py`, L33-35). `ModeSchema.validate_mode` rejects unknown modes (L115-122).
   - **Proposed change**: Replace the frozen set with a function `get_valid_modes()` that scans `schema/modes/*.yml` file names. Or accept any mode string in the Pydantic model and let the linter's file-existence check handle unknown modes.
   - **Rationale**: Spec 005's own user story US-3 AC-2 (`spec.md`, L71) says "the maintainer creates `schema/modes/auction.yml`" and expects the linter to validate it. The current implementation would reject the `auction` mode at Pydantic validation before the linter ever sees the templates. Spec 007's pluggable architecture may introduce engine-recommended modes.
   - **Risk if ignored**: Adding any new mode requires modifying `models.py`, a core source file. This contradicts spec 005's stated design goal of adding modes via YAML files alone.

4. **Add a `float`/`number` variable type** (Priority: P2)
   - **Current state**: `VALID_VARIABLE_TYPES` includes `string`, `integer`, `path`, `path-list`, `conditional-block`, `extracted-content` (`models.py`, L23-26).
   - **Proposed change**: Add `float` (or `number` to cover both int and float) to `VALID_VARIABLE_TYPES`.
   - **Rationale**: Spec 007's feature extraction (`spec.md`, L164-177) produces continuous values: concession rates, equilibrium scores (0.0-1.0), severity vectors. Plugin-contributed template variables carrying these values need an appropriate type. The `equilibrium-score` type mentioned in spec 007 `spec.md`, L298 is a float.
   - **Risk if ignored**: Plugin developers will use `string` type for numerical data, losing type validation and making the schema misleading.

5. **Add schema version field** (Priority: P2)
   - **Current state**: Neither `variables.yml` nor mode schema files carry version information.
   - **Proposed change**: Add a `schema_version: "1.0"` top-level field to `variables.yml` and each mode schema file. Bump on any structural change.
   - **Rationale**: Spec 007's scenario replay system (`spec.md`, L509-608) stores scenarios referencing specific variable sets. A replayed scenario from 3 months ago may reference variables that have been renamed or removed. Schema versioning lets the replay system detect this. Constitution Principle VII (Reproducibility, `constitution.md`, L107-120) requires deterministic behavior from the same inputs -- version mismatch detection supports this.
   - **Risk if ignored**: Scenario replay may silently produce incorrect results when the schema has drifted since the scenario was stored.

6. **Derive MODE_PRESENCE from schema rather than hardcoding** (Priority: P2)
   - **Current state**: `MODE_PRESENCE` in `validate.py` (L108-144) is a manually maintained 28-entry lookup table.
   - **Proposed change**: Compute MODE presence by scanning existing templates at linter initialization, or encode the information in the mode schema files (e.g., `mode_uses_in_phase: {review: true, revision: false}`).
   - **Rationale**: When spec 007 introduces new modes or plugins modify phase behavior, this table must be manually updated for every new `(phase, mode)` combination. Spec 007's long-term vision (`spec.md`, L245-260) sees engine-recommended modes, which would need entries in this table. Derivation from schema data eliminates manual maintenance and scales to arbitrary mode counts.
   - **Risk if ignored**: Every new mode requires editing Python source code in addition to creating YAML schema files, undermining the "YAML-only mode addition" story.

7. **Add an `extensions` section to ModeSchema** (Priority: P2)
   - **Current state**: `ModeSchema` (`models.py`, L105-123) has fixed fields: `mode`, `variables`, `templates`, `disputes`, `arbitration`, `cross_round_synthesis`.
   - **Proposed change**: Add `extensions: dict[str, Any] = Field(default_factory=dict)` to `ModeSchema`. Alternatively, add `objective_template: Optional[str] = None` as a forward-looking field.
   - **Rationale**: Spec 007's objective function templates (`spec.md`, L412-448) are mode-specific. Each mode maps to a canonical objective template (`competitive-selection` for WTA, `cooperative-integration` for cooperative). The mode schema is the natural place to declare this mapping. Without an extension point, spec 007 must create a parallel configuration structure that duplicates mode identity.
   - **Risk if ignored**: Spec 007 creates a shadow mode configuration system, violating the single-source-of-truth property that spec 005 establishes.

8. **Make VALID_PHASES extensible** (Priority: P3)
   - **Current state**: `VALID_PHASES = frozenset({"review", "cross-review", "revision", "disputes", "synthesis", "arbitration", "cross-round-synthesis"})` (`models.py`, L28-31).
   - **Proposed change**: Same approach as VALID_MODES: derive from schema or use a registry function. At minimum, allow `VALID_PHASES` to be augmented at import time by plugins.
   - **Rationale**: Spec 007's lifecycle hooks (`spec.md`, L96-112) introduce execution points between existing phases. If a future spec introduces a "plugin-analysis" phase (between synthesis and arbitration), the current validator would reject it. Constitution Principle III (`constitution.md`, L59-60) says "New orchestration capabilities are added as... new named phases after Phase 6."
   - **Risk if ignored**: Any post-Phase-7 phase (e.g., a "quality-audit" phase from a plugin) requires modifying the frozen set in core code.

9. **Document the extension contract in spec 005** (Priority: P3)
   - **Current state**: Spec 005 (`spec.md`) does not mention extensibility or plugin compatibility anywhere in its functional requirements or implementation notes.
   - **Proposed change**: Add a section to spec 005's implementation notes (after L376) titled "Extension Points for Future Specs" documenting: (a) how new variable types can be added, (b) how new modes integrate, (c) how plugins will interact with the schema and linter. This does not require implementation -- just documenting the intended extension surface.
   - **Rationale**: Spec 007 explicitly depends on spec 005 (`spec.md`, L6: `Depends On: 005-generalized-templates`). Without documented extension contracts, spec 007 implementers will make assumptions about what's safe to extend and what's not. Constitution Principle II (Stable Interfaces, `constitution.md`, L36-47) requires that interfaces be documented.
   - **Risk if ignored**: Spec 007 implementation makes breaking changes to spec 005 artifacts that were intended to be stable, or avoids extending them and builds parallel infrastructure.

10. **Reserve `schema/objectives/` directory in project structure** (Priority: P3)
    - **Current state**: The schema directory contains `variables.yml` and `modes/`. No provision for objective function templates.
    - **Proposed change**: Create an empty `schema/objectives/` directory (or document it as a planned location in spec 005's data model section, L91-322).
    - **Rationale**: Spec 007 `spec.md` L449 states "These templates are stored in `schema/objectives/` alongside the variable schema from spec 005." Reserving the directory now prevents naming conflicts and signals that the schema directory is intended to grow. The linter can be extended later to validate objective function template parameter completeness against `variables.yml`.
    - **Risk if ignored**: Spec 007 may choose a different location, fragmenting the schema directory structure. Minor, but consistency matters.

---

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-game-engine/spec.md` -- Sections: L6 (dependency declaration), L96-112 (lifecycle hooks), L131-157 (plugin API), L138-146 (DeliberationState), L164-177 (feature extraction), L180-187 (per-mode payoff functions), L245-260 (evolution path), L298 (equilibrium score output), L335-336 (plugin isolation constraint), L412-448 (objective function templates), L449 (schema/objectives location), L509-608 (scenario storage and replay)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-game-engine/ideation-context.md` -- Sections: L86-115 (objective function construction pipeline), L117-126 (objective function template library), L129-152 (scenario storage and replay ideation)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/spec.md` -- Sections: L6-7 (dependencies), L71 (US-3 AC-2 auction mode), L91-322 (data model), L353 (SC-003 new mode), L376 (implementation notes end)
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/models.py` -- Sections: L23-26 (VALID_VARIABLE_TYPES), L28-31 (VALID_PHASES), L33-35 (VALID_MODES), L105-123 (ModeSchema), L115-122 (mode validator), L129-140 (TemplateContext with extra=forbid), L262-270 (PHASE_CONTEXT_MODELS)
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/validate.py` -- Sections: L108-144 (MODE_PRESENCE lookup table), L281-305 (validate_template composition)
- `/Users/business-daddy/code/payer-index-mono/conversus/schema/variables.yml` -- Full file (L1-416)
- `/Users/business-daddy/code/payer-index-mono/conversus/.specify/memory/constitution.md` -- Sections: L36-47 (Principle II, Stable Interfaces), L49-61 (Principle III, Backward-Compatible Extension), L59-60 (new phases after Phase 6), L107-120 (Principle VII, Reproducibility), L171-185 (Principle IX, Explicit Typing)
