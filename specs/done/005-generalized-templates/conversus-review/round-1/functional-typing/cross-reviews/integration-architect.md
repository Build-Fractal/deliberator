# Cross-Review: integration-architect's Review of Spec 005

**Cross-reviewer**: functional-typing
**Reviewing**: integration-architect's Phase 1 review
**Date**: 2026-03-21

---

## Dangerous Contradictions

### 1. "Pure functions" label on impure schema loaders

integration-architect's review labels the schema-loading section of `validate.py` as "pure functions returning typed models" (review, Alignment section: "Pydantic models enforce Constitution Principle IX rigorously"). The review praises `load_variables_schema` and `load_mode_schema` as part of the well-structured pipeline but never flags that these functions call `click.echo()` and `sys.exit(2)` on failure paths (`validate.py`, L43-45, L52-53, L63-64). My review identified this as the single most important issue: these side effects make the functions impure, untestable without monkeypatching, and non-composable (functional-typing review, Missed Opportunity #1, Priority P1).

This is a dangerous contradiction because integration-architect's Recommendation #2 (extract a programmatic validation API) depends on these functions being importable and callable from an orchestrator without risk of process termination. The recommendation asks for a `validate_all()` function that returns structured results -- but the underlying `load_variables_schema` and `load_mode_schema` functions it would compose will `sys.exit(2)` before `validate_all` can catch or report the error. integration-architect correctly identifies the need for the programmatic API but does not identify that the existing schema-loading functions are the first thing that must be purified to make that API possible.

**Resolution**: integration-architect's Recommendation #2 is incomplete without my Recommendation #1 (purify schema-loading functions). These must be treated as a single unit of work: purify the loaders first, then extract the programmatic API. Implementing #2 without #1 produces a `validate_all()` that still calls `sys.exit()` on missing schema files.

### 2. `MODE_PRESENCE` -- contradictory assessments of the hardcoded table

integration-architect's review states: "The hardcoded table is the correct implementation" and "This is the right approach -- it avoids the complexity of conditional expressions in the schema" (review, Alignment section, bullet 6). But then Recommendation #7 proposes moving `MODE_PRESENCE` into the mode schema YAML files, explicitly calling the hardcoded table "a brittle coupling between the linter and template content."

My review takes a consistent position: the hardcoded table violates single-source-of-truth principles and should be derived from schema data via a pure function (functional-typing review, Missed Opportunity #3, Recommendation #5). The `condition` field on `VariableDefinition` already exists (`models.py`, L50) but is unused by the linter -- it is the natural home for this information.

integration-architect contradicts itself within a single review. More dangerously, the Alignment section's approval of the hardcoded table could be read as endorsement by a future implementor who stops reading before reaching Recommendation #7. If the table is "the right approach," there is no motivation to implement Recommendation #7. If it is "brittle coupling," the Alignment section should not endorse it.

**Resolution**: The table is not the right approach. It duplicates information that should be derivable from schema data. integration-architect's Recommendation #7 is correct; the Alignment bullet contradicts it and should be retracted. My Recommendation #5 and integration-architect's Recommendation #7 converge on the same fix -- move mode presence declarations into schema YAML and compute the lookup from it.

### 3. Structured errors requested, but `list[str]` praised as "well-structured"

integration-architect's Alignment section states the linter is "well-structured with pure validation functions composed into a single `validate_template` entrypoint." But Recommendation #8 identifies that returning `list[str]` from all `check_*` functions is inadequate for programmatic consumption and proposes a `ValidationError` Pydantic model. My review agrees that `list[str]` is a typed return (functional-typing review, Alignment section, bullet 2), but I never describe it as a well-structured data contract -- it is a list of formatted human-readable messages, not a typed data structure.

The contradiction: if the linter is well-structured, its error output should already be suitable for downstream consumers. But Recommendation #8 says it is not. The Alignment assessment overstates the maturity of the current design, which could lead to deprioritizing Recommendation #8. Meanwhile, Constitution Principle IX mandates Pydantic models for "ALL data structures" (`constitution.md`, L175-176) -- and validation error results are unambiguously a data structure. integration-architect correctly cites this in Recommendation #8 but does not flag it as a Principle IX violation in the Missed Opportunities section.

**Resolution**: Both reviews agree structured errors are needed. integration-architect's Alignment language should be qualified: the validation functions are pure and composable (good), but their return type (`list[str]`) violates the Explicit Typing mandate for data structures. My review and integration-architect's Recommendation #8 are aligned on the fix.

---

## Tensions

### 1. Scope of Pydantic model changes: forward-looking vs. present-spec

integration-architect recommends adding `PRIOR_ARBITRATION_PATH` to Phase 1-5 context models (Recommendation #3) and `ARBITRATION_PATHS` plus `ARBITRATION_RULINGS` to `CrossRoundSynthesisContext` (Recommendations #3 and #4), citing spec 006 requirements. These are P1 recommendations -- highest priority.

My review focuses on the type quality of existing fields rather than adding new ones: replacing `str` path-list fields with `list[Path]` (Recommendation #2, P1), making context models frozen (Recommendation #4, P2), and using `Literal` types for constrained enumerations (Recommendation #3, P2).

The tension: integration-architect's recommendations add new `Optional[str]` fields to context models, perpetuating the raw-string path-list pattern my review identifies as a Principle IX violation. If Recommendations #3 and #4 from integration-architect are implemented before my Recommendation #2, the new fields (`PRIOR_ARBITRATION_PATH: Optional[str]`, `ARBITRATION_PATHS: Optional[str]`) will use the same untyped `str` encoding that my review flags as the second most important issue. The models grow wider without getting type-safer.

**Resolution**: Neither review is wrong -- both priorities are real. But the ordering matters. My Recommendation #2 (replace `str` path-list fields with `list[Path]`) should be applied first or simultaneously with integration-architect's Recommendation #3. New fields should use the typed pattern from the start: `PRIOR_ARBITRATION_PATH: Optional[Path] = None` and `ARBITRATION_PATHS: Optional[list[Path]] = None`. This prevents introducing new instances of the very pattern being corrected.

### 2. `config_condition` field: type safety vs. integration extensibility

integration-architect's highest-priority recommendation (#1) proposes adding `config_conditions: Optional[dict[str, str]]` to `VariableDefinition` -- a mapping from config field names to expected values. This is a pragmatic integration concern: spec 006 needs conditional variables, and the current schema has no axis for config-dependent conditionality.

From a type safety perspective, `dict[str, str]` is weakly typed. It encodes arbitrary config field names as string keys and expected values as string values, with no validation that the config field names are real or that the values are valid for those fields. This is the kind of stringly-typed interface that Constitution Principle IX's Explicit Typing mandate warns against. A more type-safe approach would be a discriminated union of known condition types: `Literal["arbiter.timing"]` with associated value constraints, or a dedicated `ConfigCondition` Pydantic model with validated fields.

The tension is genuine: integration-architect optimizes for extensibility (any future config field can be a condition axis without schema changes), while my paradigm optimizes for type safety (every condition axis is explicitly modeled and validated). Extensibility via `dict[str, str]` means the linter cannot validate whether a `config_condition` references a real config field. Type safety via `Literal` or a Pydantic model means adding a new condition axis requires a model change.

**Resolution**: The right compromise is a `ConfigCondition` Pydantic model with a `field: str` and `value: str`, where the `field` values are validated against a known set at schema-load time (not at the type level, since config fields may evolve). This gives Pydantic validation without hardcoding every possible field into a `Literal`. integration-architect's direction is correct; the implementation should use a typed model rather than raw `dict[str, str]`.

### 3. Schema versioning: necessity vs. premature abstraction

integration-architect recommends adding a `schema_version` field to `variables.yml` (Recommendation #9, P3). My review does not mention schema versioning at all.

From a functional-typing perspective, schema versioning introduces a coupling between the schema and its consumers that must be maintained. Every schema change requires a version bump, every consumer must check the version, and version comparison logic must be implemented. For a system with exactly one consumer (the linter) and one producer (the template author), this is overhead without benefit -- the linter reads the schema directly and either validates or does not. Versioning matters when producers and consumers are decoupled across systems or deployment boundaries.

integration-architect's rationale cites spec 008's executable conversus potentially supporting "multiple schema versions during migration periods." This is speculative -- spec 008 is not yet implemented, and there is no evidence that rolling schema migration will be needed. Constitution Principle III (Backward-Compatible Extension) already governs schema evolution without requiring version numbers.

**Resolution**: Not a dangerous contradiction -- a genuine philosophical tension. integration-architect's P3 priority is appropriate. I would defer this until spec 008 demonstrates a concrete need for version-aware schema consumers. Adding a version field is trivial; adding version comparison logic and migration support is not.

### 4. `pyproject.toml` entry points: packaging concern vs. type system concern

integration-architect identifies the missing `[project.scripts]` entry point as P2 (Recommendation #5). My review does not address packaging at all, focusing instead on the type quality of the code that will be packaged.

The tension: integration-architect's packaging recommendation is outside my domain expertise, but it has a type safety implication I should acknowledge. The current import style (`from models import ...` in `validate.py`, L24-28) uses bare module imports that work only when running from the `linter/` directory. These will break when the code is packaged as `conversus.linter.validate` -- the import must become `from conversus.linter.models import ...` or a relative import (`from .models import ...`). This is a structural type system concern: the import paths encode assumptions about the package layout that are not validated by any type checker today.

**Resolution**: integration-architect's packaging recommendation is correct and has downstream implications for my type system concerns. The bare imports are a latent bug that will surface during packaging. This reinforces integration-architect's point about establishing package structure early.

---

## Safe Agreements

### 1. Pydantic model enforcement is correctly implemented

Both reviews agree that the Pydantic model layer in `models.py` is strong and correctly aligned with Constitution Principle IX. integration-architect praises `model_config = {"extra": "forbid"}` as "exactly the safety net that spec 006 and 008 need" (review, Alignment bullet 3). My review confirms that all YAML structures are parsed through Pydantic `model_validate` before use, satisfying the Explicit Typing mandate (functional-typing review, Alignment bullet 1). No contradiction.

### 2. The five `check_*` validation functions are pure and composable

Both reviews agree that `check_unknown_variables`, `check_missing_required_variables`, `check_mode_specific_variables`, `check_required_headings`, and `check_structural_markers` are pure functions. integration-architect notes the composition in `validate_template` (review, Alignment section). My review confirms they take typed inputs and return `list[str]` without side effects, aligned with Constitution Principle IX's composability requirement (functional-typing review, Alignment bullet 2). The disagreement about `list[str]` as a return type (see Dangerous Contradiction #3) is about whether the type is sufficiently structured, not about whether the functions are pure.

### 3. The spec incorrectly allows shell implementation

integration-architect does not explicitly flag the "Python or shell" language in spec Section 6 (L362). My review calls this out as an off-base assumption (functional-typing review, Off-Base Assumptions #1). However, integration-architect's entire review implicitly assumes Python throughout (recommending Pydantic models, Python type annotations, Click CLI refactoring). There is no tension here -- both reviews operate in a Python-only world. My review makes the mandate explicit; integration-architect's review assumes it without stating it.

### 4. Full type annotations are present and correct

Both reviews acknowledge that function signatures have explicit type annotations throughout `validate.py`, `models.py`, and `test_validate.py`. integration-architect does not call this out as a separate alignment point, but all recommendations assume typed code. My review identifies this as a clear Principle IX compliance point (functional-typing review, Alignment bullet 3). Agreement is implicit.

### 5. Data-driven parametrized tests are well-structured

integration-architect does not comment on the test suite's functional structure in detail, focusing instead on what the tests do not cover (schema evolution, Recommendation #6). My review praises the test suite's data-driven, parametrized design as "textbook functional testing" (functional-typing review, Alignment bullet 4). No contradiction -- integration-architect's Recommendation #6 extends coverage rather than critiquing the existing pattern.

### 6. The `AGENT_DOCS` type discrepancy must be fixed in the spec

integration-architect identifies that the spec says `type: path-list` for `AGENT_DOCS` while the implementation correctly uses `extracted-content` (review, Off-Base Assumption #3, Recommendation #10). My review does not mention this specific discrepancy. I agree with integration-architect's assessment: the implementation is correct, the spec is stale, and the fix should update the spec to match. This is not a type system concern (the implementation already uses the right type) but a documentation accuracy concern.

### 7. The linter is a runtime dependency, not a development-time tool

integration-architect flags the spec's framing of the linter as development-time-only as an off-base assumption (review, Off-Base Assumption #1), noting that SKILL.md Step 3 already integrates validation as a mandatory pre-execution step. My review does not directly address the runtime/development-time distinction, but my Recommendation #1 (purify schema-loading functions) and my critique of `sys.exit()` side effects are motivated by the same concern: if the linter is used programmatically at runtime, its functions must be pure and composable. Both reviews converge on the conclusion that the linter's API must be designed for runtime invocation, not just CLI usage.

---

## Summary

The most dangerous gap between our reviews is integration-architect's failure to flag `sys.exit()` in schema loaders as an impurity violation, while simultaneously recommending a programmatic API that depends on those functions being composable. This is the single highest-priority reconciliation: purify the loaders before building the API.

The most productive tension is around the ordering of new field additions (integration-architect Rec #3) vs. type quality improvements to existing fields (functional-typing Rec #2). Both are P1. The resolution is to do them simultaneously, ensuring new fields use typed patterns from the start.

The reviews are strongly aligned on the core assessment: the Pydantic model layer and pure validation functions are solid, the `MODE_PRESENCE` table should be derived from schema data, and structured error types are needed for programmatic consumption.
