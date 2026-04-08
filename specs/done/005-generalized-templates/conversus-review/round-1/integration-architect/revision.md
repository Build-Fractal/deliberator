# Integration Architect Revision — Spec 005: Generalized Template Schema, Variables, and Linter

**Reviewer**: integration-architect
**Revision iteration**: 1
**Date**: 2026-03-21

---

## Recommendation Dispositions

### Recommendation 1: Add config-condition field to VariableDefinition (was P1)

**Disposition**: MODIFIED — retain P1 priority, refine the typing and acknowledge a broader conditionality design.

My original recommendation proposed `config_conditions: Optional[dict[str, str]]` on `VariableDefinition`. functional-typing's cross-review correctly identifies this as weakly typed — `dict[str, str]` is a stringly-typed interface that violates the spirit of Constitution Principle IX. Their proposed resolution — a `ConfigCondition` Pydantic model with `field: str` and `value: str`, validated against known config fields at schema-load time — is a better design. I accept this refinement.

game-engine-advocate's cross-review raises a legitimate broader concern: spec 007 needs a second conditional axis (`provided_by` for plugin-contributed variables) that `config_conditions` alone does not address. However, I maintain that spec 006's needs are concrete and immediate while spec 007's plugin conditionality is speculative. The right approach is to design `config_conditions` cleanly now (using a typed model, not `dict[str, str]`), and leave the plugin conditionality axis to spec 007's implementation phase. Designing all three axes (`modes`, `config_conditions`, `provided_by`) simultaneously before any concrete spec 007 code exists risks over-engineering. The `ConfigCondition` model is extensible — a `PluginCondition` model can compose with it later without modification.

**Revised recommendation**: Add `config_conditions: Optional[list[ConfigCondition]]` where `ConfigCondition` is a Pydantic model with `field: str` and `value: str`. Validate `field` values against a known set at schema-load time. Defer plugin-conditionality to spec 007.

---

### Recommendation 2: Extract a programmatic validation API from the CLI (was P1)

**Disposition**: MODIFIED — retain P1, expand scope to include purification of schema loaders as a prerequisite.

functional-typing's cross-review identifies a genuine gap I missed: my recommendation proposes `validate_all()` returning structured results, but the underlying `load_variables_schema()` and `load_mode_schema()` functions call `sys.exit(2)` and `click.echo()` on failure paths (`validate.py`, L43-45, L52-53, L63-64). Building a programmatic API on top of functions that terminate the process is incoherent. functional-typing is correct that purifying the loaders is a prerequisite for this recommendation, and I should have identified this in my original review. The schema-loading functions are labeled "pure functions" in their comment header (`validate.py`, L31-33), but they are impure. I failed to catch this contradiction.

game-engine-advocate's cross-review raises a valid point about the API needing to accept plugin-contributed variables. However, a `plugin_variables: frozenset[str]` parameter on `validate_all()` is a spec 007 concern. The API should be designed to be extensible (accepting `**kwargs` or a `ValidationConfig` model), but the initial implementation need not include plugin awareness. Spec 007 can extend the API when it ships.

**Revised recommendation**: (a) Purify `load_variables_schema` and `load_mode_schema` by replacing `sys.exit()`/`click.echo()` with exceptions (a `SchemaLoadError` exception class). (b) Then extract `validate_all(root: Path, mode: Optional[str] = None) -> ValidationResult`. The Click CLI becomes a thin wrapper that catches `SchemaLoadError` and calls `sys.exit(2)`. These are two steps of a single unit of work.

---

### Recommendation 3: Add `PRIOR_ARBITRATION_PATH` to Phase 1-5 context models and `ARBITRATION_PATHS` to CrossRoundSynthesisContext (was P1)

**Disposition**: MODIFIED — retain P1, refine field types.

functional-typing's cross-review raises a valid ordering concern: my recommendation adds new `Optional[str]` fields for path-list variables, perpetuating the same raw-string encoding that functional-typing's review identifies as a Principle IX violation. The right approach is to use typed representations from the start.

However, I disagree with functional-typing's proposal to use `list[Path]` for these fields in the context models. The template substitution system uses `{VARIABLE}` string replacement — a `list[Path]` cannot be directly substituted into a template. A serialization step is needed. In my cross-review of functional-typing, I proposed a `PathList` type alias with a custom Pydantic serializer that stores `list[Path]` internally but renders as newline-separated strings for template substitution. I still think this is the right compromise, but I acknowledge it is an implementation detail that should not block the addition of the fields themselves.

For `PRIOR_ARBITRATION_PATH` specifically, this is a single path, not a path list. Using `Optional[Path]` (not `Optional[str]`) is unambiguously correct and has no serialization complexity.

**Revised recommendation**: Add `PRIOR_ARBITRATION_PATH: Optional[Path] = None` (not `str`) to all Phase 1-5 context models. Add `ARBITRATION_PATHS: Optional[str] = None` to `CrossRoundSynthesisContext` (keeping `str` for now, with a comment noting it should be upgraded to `PathList` when the type alias is implemented). Add corresponding entries in `schema/variables.yml` with `config_conditions` (Recommendation 1).

---

### Recommendation 4: Add `ARBITRATION_RULINGS` variable for cross-round synthesis (was P1)

**Disposition**: RETAINED — keep at P1.

game-engine-advocate's cross-review raises a valid conceptual concern about precedent: if `ARBITRATION_RULINGS` establishes that "extracted content from core outputs is a core variable," plugins may expect the same treatment. However, game-engine-advocate also identifies the correct resolution: core variables carry data produced by the core orchestrator; plugin variables carry data produced by plugins. `ARBITRATION_RULINGS` is produced by the orchestrator extracting content from Phase 6 outputs — it is unambiguously a core variable. The precedent is correct, and the distinction should be documented.

Neither cross-reviewer disputed the substance of this recommendation. The rationale stands: Constitution Principle VIII mandates that the orchestrator extracts and injects content rather than delegating parsing to agents. The cross-round synthesizer needs arbitration ruling content, not just file paths.

**Revised recommendation**: Unchanged. Add `ARBITRATION_RULINGS: Optional[str] = None` to `CrossRoundSynthesisContext` and `schema/variables.yml`. Document the rule: core variables carry orchestrator-produced data; plugin variables carry plugin-produced data.

---

### Recommendation 5: Add `[project.scripts]` entry point to pyproject.toml (was P2)

**Disposition**: MODIFIED — retain P2, expand scope to include import path fixes.

functional-typing's cross-review correctly identifies that the bare imports in `validate.py` (`from models import ...`, L24-28) are a latent bug that will surface during packaging. game-engine-advocate's cross-review extends this: spec 007 needs the package to be importable by plugins (`from conversus.linter.models import TemplateContext`), which bare imports prevent.

Both cross-reviewers converge on the same conclusion: the entry point fix must include converting bare imports to package-relative imports. This is a prerequisite for both spec 008 (programmatic linter invocation) and spec 007 (plugin model extension).

**Revised recommendation**: (a) Convert bare imports in `validate.py` to package-relative imports (`from .models import ...` or `from conversus.linter.models import ...`). (b) Add `[tool.setuptools.packages.find]` or equivalent package discovery. (c) Add `[project.scripts]` with `conversus-lint = "conversus.linter.validate:main"`. These three changes are a single unit of work.

---

### Recommendation 6: Add schema evolution regression tests (was P2)

**Disposition**: RETAINED — keep at P2.

Neither cross-reviewer disputed this recommendation. game-engine-advocate's recommendations for extensible `VALID_MODES` and `VALID_PHASES` implicitly require evolution tests (if the sets become dynamic, tests must verify dynamic extension works). functional-typing's test suite praise ("textbook functional testing") applies to existing tests but does not address the coverage gap for schema changes.

The recommendation stands as written. When spec 006 adds `PRIOR_ARBITRATION_PATH` and `ARBITRATION_PATHS`, these tests will be the regression safety net.

---

### Recommendation 7: Document MODE_PRESENCE table maintenance in the schema (was P2)

**Disposition**: MODIFIED — retain P2, retract the contradictory Alignment endorsement, and reject template-scanning alternatives.

functional-typing's cross-review correctly identifies that my review contradicts itself: the Alignment section calls the hardcoded table "the right approach," while Recommendation 7 calls it "brittle coupling." I retract the Alignment endorsement. The hardcoded table is not the right approach — it is a correct-for-now implementation that creates maintenance risk. Recommendation 7 (move to mode schema YAML) is my actual position.

functional-typing proposes deriving MODE_PRESENCE via a pure function `compute_mode_presence(schema, modes)`. game-engine-advocate proposes either scanning templates or encoding in mode schemas. In my cross-review of game-engine-advocate, I explained why template scanning is actively harmful: it makes the linter's behavior dependent on template content, creating a circularity where the validation tool's rules are derived from the artifacts it validates. A template bug (accidentally omitting `{MODE}`) would silently change the validation rules.

The schema-first approach is correct: encode `mode_presence` declarations in mode schema YAML files. The linter reads this declaration rather than inferring it. functional-typing's pure-function derivation would work if the source data is the schema YAML declarations (not templates), but the function is trivial at that point — it is just reading a YAML field.

**Revised recommendation**: Add a `mode_presence` field to each mode schema YAML file listing which phases use `{MODE}` in that mode's templates. The linter reads this field instead of the hardcoded `MODE_PRESENCE` table. Retract the Alignment section's endorsement of the hardcoded table.

---

### Recommendation 8: Use structured error objects instead of string lists (was P2)

**Disposition**: MODIFIED — retain P2, adjust the error type representation.

functional-typing's cross-review treats `list[str]` as acceptable and proposes `itertools.chain.from_iterable` for aggregation. I maintain my original position: `list[str]` is the wrong abstraction. Spec 008's orchestrator needs to programmatically distinguish error types, and string parsing for this is fragile. Constitution Principle IX mandates Pydantic models for data structures. functional-typing's `itertools.chain` suggestion optimizes concatenation of the wrong type — once errors are Pydantic models, aggregation is trivial.

game-engine-advocate's cross-review raises a valid point about the error type taxonomy: a `Literal` with 5 hardcoded values cannot represent plugin-contributed error types. However, spec 007's plugin validation is speculative. For the current scope, a `Literal` enum is appropriate — it provides type safety and autocompletion. When spec 007 adds plugin validation rules, the `Literal` can be expanded or a `PluginValidationError` subclass can be added. Using `str` for `error_type` now to preemptively support plugins would sacrifice the type safety that is the entire point of the recommendation.

**Revised recommendation**: Define `ValidationError` with `error_type: Literal["missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"]`. Acknowledge in a docstring that this enum may be expanded when plugin validation is introduced. Do not preemptively weaken the type to `str`.

---

### Recommendation 9: Add a schema version field (was P3)

**Disposition**: MODIFIED — upgrade to P2.

game-engine-advocate's cross-review provides a stronger urgency argument than my original rationale: scenario replay (spec 007) requires version-aware deserialization. But the most immediate argument, which neither my original review nor game-engine-advocate's review emphasized strongly enough, is that spec 006 will be the first schema evolution event. Adding versioning before that event means the first schema change is already versioned. Adding it after means retroactive version assignment.

In my cross-review of game-engine-advocate, I concluded P2 is appropriate. I now agree with that assessment and upgrade from P3.

functional-typing's cross-review defers versioning until spec 008 demonstrates concrete need. I disagree — spec 006 is the concrete need. It adds `PRIOR_ARBITRATION_PATH` and `ARBITRATION_PATHS` to the schema. A version bump from `1.0.0` to `1.1.0` signals this contract change to all consumers.

**Revised recommendation**: Add `schema_version: "1.0.0"` to `variables.yml` before spec 006 adds its variables. Upgrade priority from P3 to P2.

---

### Recommendation 10: Fix `AGENT_DOCS` type discrepancy between spec and implementation (was P3)

**Disposition**: RETAINED — keep at P3.

All reviewers agree the implementation (`extracted-content`) is correct and the spec (`path-list`) is stale. game-engine-advocate's cross-review reinforces the urgency: their feature extraction pipeline would build different extractors depending on which document they read. The fix is editorial — update the spec's data model section to match the implementation.

No modification needed.

---

## New Recommendations

### N1: Retract Alignment endorsement of hardcoded MODE_PRESENCE table (Priority: editorial)

My original Alignment section, bullet 6, states: "The `MODE_PRESENCE` lookup table handles conditional MODE usage correctly... This is the right approach." This contradicts Recommendation 7, which calls the same table "brittle coupling." functional-typing's cross-review correctly identifies this as a dangerous contradiction — a future implementor reading the Alignment section could take it as endorsement and stop before reaching Recommendation 7.

The Alignment bullet should be rewritten to: "The `MODE_PRESENCE` lookup table correctly captures the conditional MODE usage pattern. However, the hardcoded implementation creates maintenance risk (see Recommendation 7 for the proposed schema-first alternative)."

---

### N2: Retract Alignment characterization of schema-loading functions as "pure" (Priority: editorial)

My original review describes the linter as having "pure validation functions" without flagging that the schema-loading layer (`load_variables_schema`, `load_mode_schema`, `find_project_root`) calls `sys.exit()` and `click.echo()`. functional-typing's cross-review correctly identifies this as a dangerous omission — my Recommendation 2 depends on these functions being composable, but I did not identify that they are currently not composable. The Alignment section should not describe these functions as pure without qualification.

---

### N3: Define core-variable vs. plugin-variable namespace rule (Priority: P3)

game-engine-advocate's cross-review on Recommendation 4 (`ARBITRATION_RULINGS`) raises a valid precedent concern. Adding `ARBITRATION_RULINGS` as a core variable is correct because the orchestrator produces it. But the distinction between "core variable produced by the orchestrator" and "plugin variable produced by a plugin" should be documented in the schema, not left implicit. This prevents spec 007 plugin authors from expecting their derived data to be added to the core schema.

**Proposed rule**: Variables in `schema/variables.yml` carry data produced by the core orchestrator or provided by the user config. Variables produced by plugins are namespaced separately (mechanism to be defined by spec 007). Add a comment to `variables.yml` header documenting this boundary.

---

### N4: Preserve `extra = "forbid"` on core models; scope plugin extensibility separately (Priority: P2)

game-engine-advocate's review proposes `extra = "allow"` on `TemplateContext` for plugin-injected variables. My original review defends `extra = "forbid"` as a safety net but does not propose a resolution for the plugin extensibility tension. After reading both cross-reviews, the resolution is clear:

- For spec 006 variables: add explicit `Optional` fields to the context models. These are known variables with known types.
- For spec 007 plugin variables: add a scoped `plugin_data: dict[str, Any]` field on `TemplateContext` (with a default of empty dict). This preserves `extra = "forbid"` for all core fields while providing a typed escape hatch for plugins.
- Do not use `extra = "allow"` on any core model.

This resolution serves both downstream specs without compromising the typo-catching safety that `extra = "forbid"` provides.

---

## Position Summary

After processing both cross-reviews, my overall assessment of spec 005 is strengthened, not weakened. The foundation is solid — the Pydantic model hierarchy, phase coverage, mode schema separation, and composable validation functions are correct and serve downstream specs well. The gaps I identified remain real, and the cross-reviews have improved the precision of my recommendations rather than invalidating them.

**What I got wrong**:

1. I failed to identify that schema-loading functions are impure (`sys.exit()`, `click.echo()`) while simultaneously recommending a programmatic API that depends on them being composable. functional-typing correctly caught this blind spot. Purifying the loaders is a prerequisite for Recommendation 2, and I should have identified it as part of the same unit of work.

2. I contradicted myself on the `MODE_PRESENCE` hardcoded table — endorsing it in the Alignment section and then calling it brittle in Recommendation 7. The Alignment endorsement is retracted. Recommendation 7 (schema-first declaration) is my actual position.

3. I proposed `config_conditions: Optional[dict[str, str]]` — a weakly typed interface that violates the very Principle IX I cite throughout my review. functional-typing's proposal for a typed `ConfigCondition` model is better.

**What survives scrutiny**:

1. The priority ordering of spec 006 concrete variables before spec 007 speculative extensibility. game-engine-advocate's plugin concerns are valid but forward-looking. Spec 006's `PRIOR_ARBITRATION_PATH` and `ARBITRATION_PATHS` are defined today with known types, phases, and conditions. They should be implemented first.

2. `extra = "forbid"` must be preserved on core models. game-engine-advocate's `extra = "allow"` proposal would sacrifice typo-catching safety. A scoped `plugin_data` field is the correct compromise.

3. Structured error objects over `list[str]`. functional-typing's `itertools.chain` proposal optimizes the wrong abstraction. Spec 008 needs machine-readable errors.

4. Schema versioning should be implemented before spec 006's schema changes, not after. Upgraded from P3 to P2.

5. The linter is a runtime dependency, not a development-time tool. Both cross-reviewers converge on this conclusion from different angles. The spec's framing must be corrected.

**Priority ordering (revised)**:

| Priority | Recommendation | Status |
|----------|---------------|--------|
| P1 | Purify schema loaders (new prerequisite for Rec 2) + Extract programmatic API | Modified |
| P1 | Add `config_conditions` with typed `ConfigCondition` model | Modified |
| P1 | Add spec 006 variables to context models (`PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, `ARBITRATION_RULINGS`) | Modified |
| P2 | Schema versioning (`schema_version: "1.0.0"`) | Upgraded from P3 |
| P2 | Move `MODE_PRESENCE` to mode schema YAML | Retained |
| P2 | Structured `ValidationError` objects | Retained |
| P2 | `pyproject.toml` packaging + import path fixes | Modified |
| P2 | Schema evolution regression tests | Retained |
| P2 | Preserve `extra = "forbid"`, design `plugin_data` escape hatch (N4) | New |
| P3 | Document core-variable vs. plugin-variable namespace rule (N3) | New |
| P3 | Fix `AGENT_DOCS` type discrepancy in spec | Retained |

---

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/integration-architect/review.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/functional-typing/cross-reviews/integration-architect.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/game-engine-advocate/cross-reviews/integration-architect.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/integration-architect/cross-reviews/functional-typing.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/integration-architect/cross-reviews/game-engine-advocate.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/models.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/validate.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/006-inter-round-arbitration/spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/008-executable-conversus/001-executable-conversus.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md`
