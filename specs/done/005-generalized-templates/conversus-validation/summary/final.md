# Validation Synthesis: Spec 005 -- Generalized Template Schema, Variables, and Linter

**Synthesizer**: neutral (validation)
**Spec**: `005-generalized-templates`
**Validation mode**: Independent triplicate review
**Agents**: functional-typing, game-engine-advocate, integration-architect
**Date**: 2026-03-21
**Prior iteration**: `conversus-review/summary/final.md` (2-round cooperative deliberation, 3 agents, converged with 20 convergence items)

---

## Process Summary

Three agents independently reviewed the implementation of 22 recommendations (P1-1 through P3-8) from a prior 2-round cooperative deliberation on spec 005. The prior deliberation produced a convergence record with 5 P1 items, 9 P2 items, and 8 P3 items, plus 7 deferred items (D1-D7, explicitly out of scope).

Each validation agent:
- Ran the test suite (360 tests, all passing in ~0.70s)
- Verified the linter against all 28 templates
- Traced each convergence record item to its implementation in the codebase
- Assessed Constitution Principle IX (Functional Programming, Explicit Typing) and Principle II (Stable Interfaces) compliance
- Identified missed opportunities and actionable recommendations

All three agents independently concluded that the implementation satisfies the prior review's recommendations.

**Artifacts validated**:
- `linter/models.py` -- Pydantic models (TemplateContext hierarchy, ConfigCondition, LintError, ModeSchema, PathList, VariablesSchema, get_valid_modes)
- `linter/validate.py` -- Validation pipeline (validate_all, ValidationConfig, ValidationResult, SchemaLoadError, check_* functions, CLI main)
- `linter/test_validate.py` -- Test suite (360 tests including schema evolution regression tests)
- `schema/variables.yml` -- Variable schema with schema_version, config_conditions, spec 006 variables
- `schema/modes/*.yml` -- Four mode schemas with mode_in_phases declarations
- `specs/005-generalized-templates/spec.md` -- Spec with Section 8 extension contracts
- `pyproject.toml` -- Package configuration with conversus-lint entry point

---

## Validation Scorecard

### P1 -- Must be addressed before spec 005 can be considered complete

| ID | Recommendation | Status | Verified by | Notes |
|----|---------------|--------|-------------|-------|
| P1-1 | Purify schema-loading functions (SchemaLoadError replaces sys.exit) | **Implemented** | functional-typing, game-engine-advocate, integration-architect | All three loaders raise SchemaLoadError. sys.exit() confined to CLI main(). Unanimous, no caveats. |
| P1-2 | Extract programmatic validation API (validate_all + ValidationConfig) | **Implemented** | functional-typing, game-engine-advocate, integration-architect | ValidationConfig and ValidationResult are Pydantic models. validate_all() is a pure function. CLI main() is a thin wrapper. Docstring matches convergence record verbatim. Bare imports handled via try/except dual-path pattern. |
| P1-3 | Define PathList custom type | **Implemented** | functional-typing, game-engine-advocate, integration-architect | BeforeValidator + PlainSerializer composed into Annotated type. Applied to all path-list fields. ROUND_SYNTHESES correctly excluded (typed as str). |
| P1-4 | Add config_conditions field with typed ConfigCondition model | **Implemented** | functional-typing, game-engine-advocate, integration-architect | ConfigCondition(BaseModel) with field, operator (default "=="), value. Applied to VariableDefinition. Used in variables.yml for round-aware and arbitration-aware conditions. |
| P1-5 | Add spec 006 variables to context models and schema | **Implemented** | functional-typing, game-engine-advocate, integration-architect | PRIOR_ARBITRATION_PATH on 5 context models. ARBITRATION_PATHS (PathList) and ARBITRATION_RULINGS (str) on CrossRoundSynthesisContext. Corresponding schema entries with config_conditions. |

### P2 -- Should be addressed in spec 005's scope

| ID | Recommendation | Status | Verified by | Notes |
|----|---------------|--------|-------------|-------|
| P2-1 | Move MODE_PRESENCE to mode schema YAML with bidirectional template validation | **Implemented** | functional-typing, game-engine-advocate, integration-architect | mode_in_phases declared in all 4 mode schemas. Hardcoded MODE_PRESENCE dict deleted. Reverse template existence check implemented. ModeSchema model includes mode_in_phases field. |
| P2-2 | Make VALID_MODES a dynamic registry | **Implemented** | functional-typing, game-engine-advocate, integration-architect | get_valid_modes(schema_dir) scans schema/modes/*.yml. No hardcoded VALID_MODES frozenset. Test confirms dynamic discovery of new modes. |
| P2-3 | Structured LintError model with strict error type validation | **Partially Implemented** | functional-typing, game-engine-advocate, integration-architect | LintError model exists with correct fields and @field_validator against KNOWN_ERROR_TYPES. However, check_* functions still return list[str], not list[LintError]. ValidationResult.errors typed as bare list. All three agents independently flagged this as the same known gap. See Remaining Work. |
| P2-4 | Schema versioning | **Implemented** | functional-typing, game-engine-advocate, integration-architect | schema_version: "1.0.0" in variables.yml. VariablesSchema model includes schema_version field with matching default. Compatibility validation correctly deferred. |
| P2-5 | Apply frozen=True to TemplateContext hierarchy | **Implemented** | functional-typing, game-engine-advocate, integration-architect | model_config = {"extra": "forbid", "frozen": True} on TemplateContext. |
| P2-6 | Document extension contracts in spec 005 | **Implemented** | functional-typing, game-engine-advocate, integration-architect | Section 8 in spec.md with all three subsections: extension points, non-extension points, observations. Content matches convergence record. Placed as Section 8 rather than Section 6 -- functionally equivalent. |
| P2-7 | Mandate Python in spec Implementation Notes | **Implemented** | game-engine-advocate, integration-architect | Python mandate present in spec implementation notes. |
| P2-8 | pyproject.toml packaging and entry point | **Implemented** | functional-typing, game-engine-advocate, integration-architect | conversus-lint = "conversus.linter.validate:main" in [project.scripts]. Dependencies declared. |
| P2-9 | Schema evolution regression tests | **Implemented** | functional-typing, game-engine-advocate, integration-architect | Three test methods in TestSchemaEvolution: new optional variable accepted, new required variable produces errors, new mode schema discovered. All parametrized across modes. |

### P3 -- Should be addressed, low urgency

| ID | Recommendation | Status | Verified by | Notes |
|----|---------------|--------|-------------|-------|
| P3-1 | Document required: True default in spec | **Implemented** | game-engine-advocate | Documented in spec. |
| P3-2 | Fix AGENT_DOCS type discrepancy in spec | **Implemented** | game-engine-advocate | Spec Section 3 corrected. |
| P3-3 | Document core-variable vs. plugin-variable namespace rule | **Implemented** | game-engine-advocate | Comment in variables.yml header establishes namespace convention. |
| P3-4 | Make VALID_PHASES extensible | **Implemented** | game-engine-advocate | Derivable from schema data / PHASE_CONTEXT_MODELS keys. |
| P3-5 | Extend ConfigCondition with operator field | **Implemented** | functional-typing, game-engine-advocate, integration-architect | operator: str = "==" on ConfigCondition. Delivered together with P1-4. |
| P3-6 | Fix ROUND_SYNTHESES comment in models.py | **Implemented** | functional-typing, game-engine-advocate, integration-architect | Comment reads "pre-formatted synthesis content per round." Correctly excluded from PathList conversion. |
| P3-7 | Validate mode schema templates entries against phase names | **Implemented** | functional-typing, game-engine-advocate, integration-architect | validate_all() validates that template names correspond to known phases. Bridges P2-1 and P2-6 into three-part validation chain. |
| P3-8 | Use itertools.product in test case generators | **Implemented** | functional-typing | Minor readability improvement applied where applicable. |

---

## Unanimous Findings

All three validation agents agreed on the following:

### Passes

1. **All five P1 items are fully implemented.** SchemaLoadError exceptions (P1-1), programmatic API with ValidationConfig/ValidationResult (P1-2), PathList custom type with ROUND_SYNTHESES exclusion (P1-3), ConfigCondition model with operator field (P1-4), and spec 006 variables in context models and schema (P1-5). No agent raised any concern about any P1 item.

2. **The "freeze first, compose later" principle held throughout.** The implementation freezes the foundation (extra = "forbid", frozen = True, strict LintError validation) while leaving documented extension surfaces for spec 007. This was the governing principle from the deliberation and it was faithfully applied.

3. **Constitution Principle IX compliance is strong.** All functions have explicit type annotations. All data structures use Pydantic models. Functions are pure (schema loading raises exceptions rather than calling sys.exit()). No mutable global state.

4. **The test suite is comprehensive.** 360 tests covering positive validation, negative detection, fuzzy suggestions, structural markers, mode-specific enforcement, and schema evolution scenarios. All pass.

5. **Dynamic mode discovery works correctly.** get_valid_modes() scans the filesystem. Adding a fifth mode requires only creating a new YAML file -- no code changes to the validation pipeline or models.

6. **Extension contracts are properly documented.** Spec Section 8 covers extension points, non-extension points, and observations, matching the convergence record.

### Gaps

1. **LintError model defined but not wired into the validation pipeline (P2-3 partial).** All three agents independently identified the same gap: the LintError Pydantic model exists with correct structure and strict @field_validator, but the check_* functions still return list[str] rather than list[LintError], and ValidationResult.errors is typed as bare list. The model is ready infrastructure awaiting mechanical wiring. All three agents classified this as a known P2 follow-up item, not a blocking defect.

2. **ValidationResult.errors uses unparameterized list type.** A consequence of the P2-3 gap. The field is typed as `list` rather than `list[LintError]` or even `list[str]`. functional-typing noted this as the only Principle IX violation in the entire implementation.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

No remaining disputed positions -- all agents independently confirm the implementations pass validation.

The three agents' assessments are fully concordant on all 22 convergence items. There are no cases where one agent marked an item as implemented while another marked it as not implemented. The only item with any nuance (P2-3) was independently assessed by all three agents using the same framing: the model is correctly defined, the wiring is incomplete, and this is a known follow-up rather than a missed requirement.
<!-- CONVERSUS:DISPUTES_END -->

---

## Remaining Work

### Priority P2

**1. Wire LintError into check_* return types (P2-3 completion)**
- **Flagged by**: functional-typing (AR-1), game-engine-advocate (Observation 2), integration-architect (R1)
- **Scope**: Convert each check_* function to return list[LintError] instead of list[str]. Update ValidationResult.errors type annotation from list to list[LintError]. Update CLI main() to format LintError instances for human display.
- **Rationale**: The model exists with correct structure and strict validation. Wiring it in completes the programmatic API contract for downstream consumers (spec 007 plugins, spec 008 executable conversus). Currently, KNOWN_ERROR_TYPES validation only runs if someone manually constructs a LintError.
- **Effort**: Mechanical refactor. No architectural decisions required.

### Priority P3

**2. Populate linter/__init__.py with public API exports**
- **Flagged by**: integration-architect (R2)
- **Scope**: Export validate_all, ValidationConfig, ValidationResult, and SchemaLoadError from __init__.py.
- **Rationale**: Makes the programmatic API discoverable via standard Python import conventions. Currently __init__.py is empty.

**3. Tighten ValidationResult.errors type annotation**
- **Flagged by**: functional-typing (AR-2)
- **Scope**: Change errors: list to errors: list[str] (if LintError wiring is deferred) or errors: list[LintError] (if completed). Resolves the only Principle IX explicit-typing violation.
- **Note**: Subsumed by item 1 above if LintError wiring is completed.

### Cosmetic

**4. CLI --mode option uses hardcoded click.Choice**
- **Flagged by**: game-engine-advocate (Observation 1)
- **Scope**: Derive click.Choice list from get_valid_modes() at CLI definition time.
- **Rationale**: The programmatic API dynamically discovers modes, but the CLI convenience wrapper hardcodes the four mode names. Adding a fifth mode would require a code change in the CLI even though validate_all() would discover it automatically.
- **Priority**: Cosmetic. The programmatic API is the contract surface; the CLI is a developer convenience.

**5. AGENT_NAME phase list discrepancy in spec Section 3**
- **Flagged by**: functional-typing (MO-2)
- **Scope**: The spec's Section 3 data model example lists AGENT_NAME with phases [review, cross-review, revision, disputes], but the schema correctly omits cross-review (which uses REVIEWER_NAME/REVIEWED_NAME instead).
- **Priority**: Negligible. The spec example is illustrative, not normative. The schema is the source of truth.

---

## Validation Verdict

**The implementation satisfies the prior review's recommendations.**

All five P1 items are fully and correctly implemented. All nine P2 items are implemented, with one (P2-3: LintError wiring) partially complete -- the model is defined with correct structure but not yet used as the return type of the validation pipeline. All eight P3 items are implemented. The implementation is well-aligned with Constitution Principle IX (Functional Programming, Explicit Typing) and Principle II (Stable Interfaces with documented extension points).

The single incomplete item (P2-3 wiring) is a mechanical refactor with no architectural decisions remaining. The LintError model, KNOWN_ERROR_TYPES set, and @field_validator are all in place -- only the plumbing from check_* functions to LintError instances is missing. All three agents independently classified this as a known follow-up, not a blocking defect.

The "freeze first, compose later" principle that emerged from the deliberation is faithfully reflected in the implementation: core models use extra = "forbid" and frozen = True, while extension surfaces (new variables, new modes, new config conditions, PHASE_CONTEXT_MODELS registry, KNOWN_ERROR_TYPES registry) are documented and structurally available for spec 007. The foundation is correct, well-structured, and ready for downstream extension.

**Spec 005 is validated for completion**, with P2-3 LintError wiring as the sole remaining follow-up item.
