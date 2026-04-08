# Cross-Review of functional-typing's Review — Spec 005

**Cross-reviewer**: integration-architect
**Reviewing**: functional-typing's Phase 1 review of `005-generalized-templates`
**Date**: 2026-03-21

---

## Dangerous Contradictions

### 1. MODE_PRESENCE: "Derive from schema" vs. "Hardcoded table is correct"

functional-typing recommends deriving `MODE_PRESENCE` from the schema via a pure function `compute_mode_presence(schema, modes)` (Missed Opportunities, bullet 3; Recommendation 5, P2), calling the hardcoded table a "maintenance burden and drift risk." My review states the opposite: "The `MODE_PRESENCE` lookup table handles conditional MODE usage correctly... This is the right approach — it avoids the complexity of conditional expressions in the schema while capturing the actual template reality" (Alignment, bullet 6). My Off-Base Assumptions section further notes that MODE's conditional presence "cannot be derived from `variables.yml` or the mode schemas" because the schema's `condition` field is insufficient to encode per-mode per-phase template reality.

**Resolution**: functional-typing is correct that the hardcoded table is a maintenance risk. I am correct that it cannot currently be derived from the schema. These are not incompatible positions — they imply the schema needs a new field to make derivation possible. My Recommendation 7 (move `mode_presence` into mode schema YAML files) resolves this: the data becomes declarative and schema-owned without requiring a computation function that would need heuristics. functional-typing's proposed `compute_mode_presence` function would need to scan actual templates to produce correct results, which defeats the purpose of a schema-first validation tool. The mode schema approach keeps the data authoritative rather than inferred.

**Risk if unresolved**: A future contributor reads functional-typing's review, implements `compute_mode_presence` by scanning templates, and creates a circular dependency: the linter needs to read templates to know what to validate in templates. Alternatively, they read my review, keep the hardcoded table, and it silently drifts when spec 006 modifies templates.

### 2. `list[str]` error returns: "Use `itertools.chain`" vs. "Use structured `ValidationError` models"

functional-typing's Recommendation 5 (P2, itertools.chain) and Missed Opportunity bullet 5 treat `list[str]` as an acceptable return type that can be made more idiomatically functional via `itertools.chain.from_iterable`. My Recommendation 8 (P2, structured error objects) argues that `list[str]` itself is the problem — errors should be Pydantic `ValidationError` models with typed fields (`error_type`, `variable_name`, `phase`, `mode`, `suggestion`). These are contradictory directions: optimizing the concatenation of string lists assumes strings are the right representation, while replacing strings with models makes concatenation strategy irrelevant.

**Resolution**: My position takes priority from an integration perspective. Spec 008's orchestrator needs to programmatically distinguish error types (missing marker is blocking; unknown variable may be a warning). String parsing is fragile and ironic for a linter. Constitution Principle IX mandates Pydantic models for all data structures — error results are data structures. functional-typing's `itertools.chain` suggestion is a local optimization on the wrong abstraction. Once errors are Pydantic models, the aggregation question becomes trivial (`list` concatenation, `itertools.chain`, or even a `ValidationResult` container — all equivalent for typed objects).

**Risk if unresolved**: A developer implements `itertools.chain.from_iterable` on string lists, making the code more "functional" but cementing the untyped error representation. Spec 008 then has to parse error strings with regex to make programmatic decisions — the exact fragility the linter was built to prevent.

### 3. Scope of review: code purity vs. downstream integration

functional-typing's highest-priority recommendation (P1, Recommendation 1) is purifying schema-loading functions by replacing `sys.exit()` with exceptions or Result types. My highest-priority recommendation (P1, Recommendation 1) is adding `config_condition` to `VariableDefinition` for spec 006 compatibility. These are not contradictory in principle, but they compete for P1 priority and represent fundamentally different risk assessments.

functional-typing sees impure functions as the most dangerous defect because they prevent composition and library use. I see the missing `config_condition` field as the most dangerous defect because it will force spec 006 to bypass the schema entirely, fragmenting the "single source of truth" that spec 005 exists to establish.

**Resolution**: Both are P1, but they are sequentially independent — fixing one does not block fixing the other. However, if forced to choose, the integration risk is more severe. A function that calls `sys.exit()` can be wrapped in a try/except at the call site as a temporary measure. A schema that cannot represent config-dependent variables forces spec 006 into a parallel validation path with no temporary workaround — the architectural damage is structural, not cosmetic. functional-typing's recommendation becomes more urgent once the programmatic API (my Recommendation 2) is built, since at that point `sys.exit()` in library code becomes a runtime crash rather than merely a testing inconvenience.

**Risk if unresolved**: Resources are spent purifying schema-loading functions while the schema itself cannot represent the variables that spec 006 needs. Spec 006 implementation begins, discovers the schema gap, and builds a second validation path — the exact fragmentation spec 005 was designed to prevent.

---

## Tensions

### 1. Literal types vs. extensibility

functional-typing recommends `Literal["cooperative", "red-blue", "winner-take-all", "prisoners-dilemma"]` for `ModeSchema.mode` and `Literal[...]` for `VariableDefinition.type` (Recommendation 3, P2). This provides static type checking at the cost of extensibility: adding a fifth mode or a seventh variable type requires modifying the `Literal` union in source code, not just adding a YAML file.

My review does not recommend Literal types. My Missed Opportunities section emphasizes that the schema must support extensibility for new modes (US-3 AC-2 of the spec) and new variables (spec 006 adds `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, `ARBITRATION_RULINGS`). A `Literal` type for modes would require a code change every time a mode schema YAML file is added, creating a coupling between the type system and the file system that the schema-first design is meant to avoid.

**Tension**: functional-typing optimizes for compile-time safety within the current mode set. I optimize for runtime extensibility across the evolving mode set. The right balance depends on how frequently modes are added. With 4 modes today and no concrete fifth mode planned, the Literal approach is safe for modes. For variable types, the tension is sharper: spec 006 does not add new types, but the `extracted-content` type was itself a late addition (see the `AGENT_DOCS` type discrepancy in the spec), suggesting the type vocabulary is still evolving.

**Suggested resolution**: Use `Literal` for `ModeSchema.mode` (modes change rarely and require a full mode schema file anyway). Keep runtime validation for `VariableDefinition.type` (types may evolve and are purely a schema concern, not a mode-file concern).

### 2. `frozen=True` on TemplateContext vs. runtime context building

functional-typing recommends `model_config = {"extra": "forbid", "frozen": True}` for `TemplateContext` models (Recommendation 4, P2), arguing that context objects should be constructed once and never mutated. This is sound in principle, but creates a practical tension with how the orchestrator builds context incrementally.

SKILL.md Step 4 shows that template variables are populated from multiple sources: config values, computed paths, extracted content, round-aware state. The orchestrator currently (or will, under spec 008) build context dictionaries incrementally and then pass them to the Pydantic model. If the model is frozen, the orchestrator cannot use builder-pattern construction (create model, then set fields). It must construct all fields upfront in a single `dict` and pass that to `model_validate`.

**Tension**: This is not a blocker — constructing a complete dict before model creation is the correct Pydantic pattern anyway. But it constrains spec 008's orchestrator design: no `context.PRIOR_ARBITRATION_PATH = arb_path` after initial construction. Given that spec 006 adds `PRIOR_ARBITRATION_PATH` conditionally (only when `arbiter.timing: inter-round` and prior arbitration exists), the orchestrator must determine all conditional fields before constructing the context. With `frozen=True`, there is no "set it later if applicable" escape hatch.

**Suggested resolution**: Accept `frozen=True`. It enforces the discipline that context construction is complete before template substitution begins, which is architecturally correct. Spec 008's orchestrator should use a builder function that returns a complete dict, then calls `ContextModel.model_validate(complete_dict)`. This is cleaner than post-construction mutation anyway.

### 3. `__all__` exports (functional-typing Rec 7) vs. schema evolution tests (integration-architect Rec 6)

Both are P3/P2 respectively and do not contradict, but they compete for attention. functional-typing's `__all__` recommendation is about API hygiene. My schema evolution tests recommendation is about ensuring spec 006's additions do not regress existing validation.

**Tension**: Pure priority competition. Schema evolution tests have higher integration value because they catch regressions when spec 006 adds `PRIOR_ARBITRATION_PATH` to the schema — a concrete near-term event. `__all__` exports prevent hypothetical import accidents in a module with ~15 public symbols — a real but lower-probability risk.

### 4. Path-list typing: `list[Path]` with validator vs. `str` with comments

functional-typing calls out `str` fields for newline-separated path lists as a P1 violation of the Explicit Typing mandate (Recommendation 2). My review notes the same fields in the context of missing `ARBITRATION_PATHS` (Recommendation 3) but does not elevate the typing issue to P1.

**Tension**: functional-typing is right that `str` for path lists violates Constitution Principle IX. But changing these to `list[Path]` has a cascading effect: the template substitution system uses `{VARIABLE}` string replacement, and a `list[Path]` cannot be directly substituted into a template string. A serialization step is needed (join paths with newlines before substitution). This is tractable but touches every template variable population site in the orchestrator — a change that bleeds into spec 008's implementation scope.

**Suggested resolution**: Define a `PathList` type alias with a custom Pydantic serializer that renders as newline-separated strings. The model stores `list[Path]` internally, but `model.ARBITRATION_PATHS` returns a formatted string when used in template substitution via a `__str__` method or a dedicated `render()` method. This satisfies both functional-typing's type safety requirement and the template engine's string substitution need.

---

## Safe Agreements

### 1. Schema-loading functions must not call `sys.exit()`

functional-typing's Recommendation 1 (P1) and my Recommendation 2 (P1, programmatic API) converge on the same conclusion from different angles. functional-typing argues from purity: functions that call `sys.exit()` are impure and uncomposable (`validate.py` L48-56, L59-67, L35-45). I argue from integration: spec 008 needs to call the linter as a library, and `sys.exit()` in library code is a crash, not an error (`specs/008-executable-conversus/001-executable-conversus.md`, Phase 5). Both reviews agree the CLI layer (`main()`) should be the sole site of `sys.exit()` and user-facing output.

**Confidence**: High. Both the functional programming mandate and the integration requirement point to the same fix. The only question is whether to use exceptions (my position: `SchemaLoadError`) or a Result type (functional-typing's position: `Result[T, str]`). In practice, exceptions are more Pythonic and the FP HOWTO acknowledges this; a Result type is elegant but non-standard in the Python ecosystem. Either works; exceptions are lower friction.

### 2. The linter is a runtime dependency, not a development-time tool

My Off-Base Assumptions section flags the spec's framing of the linter as development-time-only, noting that SKILL.md Step 3 already treats validation as a mandatory pre-execution step (lines 260-271). functional-typing does not flag this directly but implicitly agrees through Recommendation 1 (purifying functions for library use) and the observation that the linter must be importable and composable. A development-time-only tool does not need to be importable — a runtime dependency does.

**Confidence**: High. Both reviews treat the linter as infrastructure that other specs depend on, not as an optional developer convenience.

### 3. The spec should mandate Python, not "Python or shell"

functional-typing's Off-Base Assumptions section and Recommendation 6 (P2) flag spec Section 6's "Python or shell" language as incompatible with Constitution Principle IX. My review does not call this out explicitly, but my entire review presumes a Python implementation (referencing Pydantic models, type annotations, Click CLI). The agreement is implicit: both reviews assume and require Python.

**Confidence**: High. The linter is already implemented in Python with Pydantic models. The spec language is outdated relative to the implementation. Updating it is editorial, not architectural.

### 4. The `AGENT_DOCS` type discrepancy must be fixed

My Recommendation 10 (P3) and functional-typing's implicit reliance on the schema's `extracted-content` typing for `AGENT_DOCS` agree that the spec's data model showing `type: path-list` is wrong. The implementation correctly types it as `extracted-content`. The spec should be updated to match.

**Confidence**: High. Both reviews reference the same discrepancy. The implementation is correct; the spec is stale.

### 5. `PHASE_CONTEXT_MODELS` should be immutable

functional-typing recommends `Final` typing for the module-level dict (Recommendation 8, P3). My review does not address this directly but my emphasis on `extra: "forbid"` as a safety net (Alignment, bullet 3) implies agreement that the phase-to-model mapping should not be mutable at runtime. If a runtime mutation changed `PHASE_CONTEXT_MODELS["review"]` to point at the wrong model, the `extra: "forbid"` safety net would produce confusing errors rather than catching the root cause.

**Confidence**: Medium. Both reviews value immutability of the mapping; we differ only on whether `Final` annotation is worth the effort at P3 priority.

### 6. Spec should document `required: True` as the default

functional-typing's Recommendation 9 (P3) calls out the spec's inconsistent use of the `required` field, noting that the implementation defaults to `True` (`models.py` L48) but the spec never states this. My review does not flag this, but my emphasis on schema extensibility implicitly requires that defaults be documented — when spec 006 adds `PRIOR_ARBITRATION_PATH` as `Optional`, the distinction between "omitted required (defaults true)" and "explicitly required: false" must be clear.

**Confidence**: High. This is an editorial fix with no implementation cost and direct documentation value.

---

## Summary of Positions

| Issue | functional-typing | integration-architect | Resolution |
|---|---|---|---|
| Top P1 priority | Purify `sys.exit()` from loaders | Add `config_condition` for spec 006 | Both P1; `config_condition` first if sequencing is needed |
| MODE_PRESENCE | Derive via pure function | Keep hardcoded (correct impl) | Move to mode schema YAML (my Rec 7) |
| Error return type | Optimize `list[str]` with `itertools.chain` | Replace `list[str]` with Pydantic models | Pydantic models; chain becomes irrelevant |
| Literal types | Use `Literal` for modes + types | No recommendation | Literal for modes only; runtime validation for types |
| `frozen=True` | Recommend for all contexts | Not addressed | Accept; enforces correct construction discipline |
| Path-list fields | `list[Path]` with Pydantic validator (P1) | Not elevated to P1 | `PathList` type alias with custom serializer |
| Spec "Python or shell" | Flag as off-base (P2) | Implicit agreement | Update spec; editorial fix |
| `AGENT_DOCS` type | Not flagged | Flag as P3 | Update spec to match implementation |

---

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/functional-typing/review.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/integration-architect/review.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/models.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/validate.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/006-inter-round-arbitration/spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/008-executable-conversus/001-executable-conversus.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md`
