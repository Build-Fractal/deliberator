# Cross-Review: game-engine-advocate on functional-typing's Review of Spec 005

**Cross-reviewer**: game-engine-advocate (spec 007)
**Reviewing**: functional-typing's Phase 1 review of spec 005
**Date**: 2026-03-21

---

## Dangerous Contradictions

### 1. `frozen=True` on TemplateContext directly conflicts with plugin extensibility

functional-typing recommends making `TemplateContext` models frozen (`model_config = {"extra": "forbid", "frozen": True}`) [functional-typing review, Recommendation #4]. My review identifies `extra = "forbid"` as already blocking plugin injection [game-engine review, Missed Opportunities #2] and recommends either `extra = "allow"` on a plugin-aware variant or a `plugin_data: dict[str, Any]` field.

Adding `frozen=True` on top of `extra = "forbid"` doubles down on the closure. A frozen, extra-forbidding model is the maximally hostile surface for plugin extensibility. Spec 007's `DeliberationState` (`spec.md`, L138-146) needs to carry plugin-specific data (equilibrium scores, convergence predictions) alongside core variables. If the context models are frozen AND forbid extras, plugins have no path to attach their data without constructing entirely parallel objects -- which means the plugin layer cannot reuse the typed models that spec 005 establishes.

**The contradiction**: functional-typing's recommendation optimizes for immutability correctness in a closed system, but spec 005 is not a closed system -- it is an explicitly declared dependency of spec 007 (`spec.md`, L6). Making the foundation maximally rigid before the extension layer is designed creates rework. The correct sequence is: design the extension points (spec 007 Phase 1), then apply immutability to the parts that are genuinely closed.

**Resolution**: Apply `frozen=True` only after defining which fields are core (frozen, forbid-extra) and which are extension points (mutable or extra-allowing). A `CoreTemplateContext(frozen=True, extra="forbid")` and a `PluginTemplateContext(frozen=True, extra="allow")` split would satisfy both reviewers. Alternatively, add a `plugin_data: dict[str, Any] = Field(default_factory=dict)` to the base before freezing -- the dict itself is mutable even if the model is frozen, since Pydantic's `frozen` only prevents field reassignment, not mutation of mutable field values.

### 2. `Literal` types for modes would hardcode the closed-enum assumption into the type system

functional-typing recommends replacing `str` + `@field_validator` with `Literal["cooperative", "red-blue", "winner-take-all", "prisoners-dilemma"]` for `ModeSchema.mode` [functional-typing review, Recommendation #3]. My review identifies `VALID_MODES` as a frozen set that should become a registry [game-engine review, Recommendation #3] and flags the contradiction between spec 005's own SC-003 (adding an "auction" mode via YAML alone) and the implementation's hard-reject of unknown modes.

Replacing a runtime validator with a `Literal` type makes the problem strictly worse. A `@field_validator` can be loosened to read from a dynamic registry. A `Literal` type is baked into the type definition itself -- changing the set of valid modes requires modifying the source code, regenerating type stubs, and updating every downstream type annotation. Spec 005's own user story US-3 AC-2 (`spec.md`, L71) envisions adding "auction" by creating a YAML file. A `Literal` type makes that impossible without a code change.

For `VariableDefinition.type`, the same concern applies at lower severity: spec 007 needs a `float`/`number` type for plugin-contributed numerical variables [game-engine review, Recommendation #4]. A `Literal` type for variable types means adding `float` requires editing the type annotation in `models.py` -- acceptable but unnecessarily rigid.

**The contradiction**: functional-typing optimizes for static type checking (mypy/Pyright enforcement), but the spec's own stated extensibility story requires runtime flexibility. These goals are in direct tension. Static types that enumerate a closed set prevent the dynamic extension that both spec 005 and spec 007 require.

**Resolution**: Keep the `@field_validator` pattern but make it read from a dynamically constructed set. For mode validation, scan `schema/modes/*.yml` filenames at schema-load time. This preserves runtime validation without baking the enum into the type system. If static type narrowing is desired, use `str` with `Annotated[str, AfterValidator(...)]` -- this gives Pydantic runtime validation while keeping the type open.

---

## Tensions

### 3. Purifying schema-loading functions: agreed on direction, different urgency models

functional-typing's top recommendation (P1) is purifying `load_variables_schema`, `load_mode_schema`, and `find_project_root` by removing `sys.exit()` calls [functional-typing review, Recommendation #1]. My review does not address this directly -- my focus is on extensibility rather than functional purity.

However, I agree this matters for spec 007 and would reprioritize it. functional-typing's rationale -- "these functions cannot be imported and used in other contexts (e.g., an orchestrator calling the linter as a library) without risking process termination" -- is directly relevant. Spec 007's plugin validation system will need to call `load_variables_schema` as a library function (to validate plugin-contributed variables against the core schema). If it calls `sys.exit(2)` on a missing file, the entire plugin loading process dies. This is a real integration hazard.

**The tension**: functional-typing frames this as a functional purity concern (Constitution Principle IX). From the game-engine perspective, it is a library reusability concern. Same fix, different motivations, different priority framing. functional-typing rates it P1 for purity; I would rate it P1 for integration safety. We agree on the fix and priority but for different reasons.

### 4. Deriving MODE_PRESENCE from schema: agreed on need, tension on approach

Both reviews flag `MODE_PRESENCE` as a hardcoded table that should be derived [functional-typing review, Recommendation #5; game-engine review, Recommendation #6]. functional-typing proposes adding a `mode_presence` field to `variables.yml`'s `MODE` entry or computing it from the `condition` field. My review proposes scanning existing templates at linter initialization or encoding the information in mode schema files.

**The tension**: functional-typing's approach (derive from `condition` field or add to variable schema) keeps the derivation close to the variable definition. My approach (scan templates or add to mode schemas) keeps it close to the mode definition. These are different locations in the data model for the same information. For spec 007, the mode schema is the more natural home -- when a plugin introduces a new mode, it provides a mode schema file, and that file should declare whether MODE is expected in each phase. Asking plugin authors to modify the core `variables.yml` to add mode-presence data defeats the plugin isolation constraint.

**Resolution**: Encode in mode schema files. Each mode schema already declares its variables; adding `mode_in_phases: [synthesis, arbitration, cross-round-synthesis]` is a natural extension. The linter derives the lookup table from mode schemas at load time. This scales to plugin-contributed modes without touching core schema files.

### 5. `list[Path]` for path-list fields: correct but insufficient for plugins

functional-typing recommends replacing raw `str` path-list fields with `list[Path]` using a custom Pydantic validator [functional-typing review, Recommendation #2]. This is correct for core variables. From the game-engine perspective, there is a secondary concern: plugin-contributed variables may also carry path lists (e.g., a list of prior scenario files for replay). If the `list[Path]` pattern is established only on core context models, plugins constructing their own context objects must reimplement the same validator.

**The tension is minor**: functional-typing's recommendation is right for spec 005's scope. The game-engine concern is that the `PathList` custom type should be exported as a reusable type from `models.py` so that plugin developers can use it in their own Pydantic models. This is an additive extension of functional-typing's recommendation, not a contradiction.

### 6. `__all__` exports and `Final` typing: premature if the public API is about to expand

functional-typing recommends adding `__all__` to `models.py` [functional-typing review, Recommendation #7] and marking `PHASE_CONTEXT_MODELS` as `Final` [functional-typing review, Recommendation #8]. From the game-engine perspective, `PHASE_CONTEXT_MODELS` is specifically the registry that plugins need to extend [game-engine review, Alignment #5: "A plugin could extend this registry at load time"]. Marking it `Final` tells type checkers and developers that it must not be modified -- which is exactly what plugins need to do.

Similarly, `__all__` restricts the public API surface. If spec 007 needs to import internal types (the `TemplateContext` hierarchy, `VariableDefinition`, the frozenset constants) for plugin validation, a restrictive `__all__` could hide symbols that plugins need.

**The tension**: These are good practices for stable, closed modules. `models.py` is about to become a shared foundation for a plugin ecosystem. Locking down the API surface before knowing what the plugin interface needs is premature. The `__all__` and `Final` decisions should be made after spec 007 Phase 1 defines which symbols are core-stable vs plugin-extensible.

---

## Safe Agreements

### 7. Pydantic models for all YAML data

Both reviews affirm that the Pydantic model hierarchy in `models.py` is well-structured and correct for its scope [functional-typing review, Alignment #1; game-engine review, Alignment #3]. functional-typing notes satisfaction of Constitution Principle IX's Explicit Typing mandate. My review notes that the `TemplateContext` hierarchy establishes the typed contract that `DeliberationState` can consume. No disagreement.

### 8. Pure validation functions in validate.py are composable and extensible

functional-typing praises the five `check_*` functions as pure and composable [functional-typing review, Alignment #2]. My review identifies this composable architecture as compatible with spec 007's plugin-aware validation [game-engine review, Alignment #4: "A plugin that introduces new template variables could provide its own validation function composed alongside the existing ones"]. Both reviews see the same strength from different angles.

### 9. Data-driven parametrized tests are the right pattern

functional-typing praises the test suite's functional testing pattern [functional-typing review, Alignment #5]. My review does not address testing directly, but the test architecture's use of pure mutation helpers and parametrized generation would extend naturally to plugin-contributed variable testing. No disagreement.

### 10. Spec should mandate Python, not "Python or shell"

functional-typing flags the spec's "Python or shell" language as off-base [functional-typing review, Off-Base Assumptions #1]. From the game-engine perspective, I did not flag this -- but I implicitly agree. The plugin API is Python (`from conversus.plugins import Plugin`). The linter must be Python to serve as a library function for plugin validation. Shell is not viable. functional-typing's recommendation to mandate Python in the spec is correct and compatible with spec 007's requirements.

### 11. Documenting the `required: True` default in the spec

functional-typing identifies that the spec omits the `required` default [functional-typing review, Off-Base Assumptions #2, Recommendation #9]. This is a spec-quality concern unrelated to game-engine extensibility. No contradiction; it should be addressed.

### 12. Frozenset usage for immutable collections

functional-typing praises `frozenset` usage for `VALID_VARIABLE_TYPES`, `VALID_PHASES`, and `extract_variables` returns [functional-typing review, Alignment #6]. My review flags `VALID_MODES` and `VALID_PHASES` as problematic because they are frozen sets rather than registries [game-engine review, Missed Opportunities #7, Recommendation #3 and #8]. These are not contradictions -- we agree that the frozenset pattern is correct for genuinely immutable data (like `extract_variables` returns) but disagree on whether the mode/phase sets are genuinely immutable. The underlying agreement is that immutability should be applied to data that is actually closed, not to data that the system's own spec says is extensible.

---

## Summary

The two reviews converge on the quality of the existing implementation (Pydantic models, pure validation functions, data-driven tests) and on the need to derive `MODE_PRESENCE` from schema data. They diverge on how much to close down the system. functional-typing's recommendations -- `frozen=True`, `Literal` types, `Final`, `__all__` -- are individually correct for a closed module but collectively create a foundation that is hostile to spec 007's plugin architecture. The most dangerous contradictions are `Literal` types for modes (which conflicts with spec 005's own extensibility story) and `frozen=True` on context models (which blocks plugin data injection). These should be resolved before either review's recommendations are implemented, ideally by defining the extension contract first and then applying immutability and type narrowing to the genuinely closed portions.
