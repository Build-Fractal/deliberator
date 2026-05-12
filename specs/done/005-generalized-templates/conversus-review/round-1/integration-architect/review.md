# Integration Architect Review — Spec 005: Generalized Template Schema, Variables, and Linter

**Reviewer**: integration-architect
**Spec Under Review**: `005-generalized-templates`
**Date**: 2026-03-21

---

### Executive Summary

Spec 005 establishes the machine-readable schema (`schema/variables.yml`, `schema/modes/{mode}.yml`) and development-time linter that will become the foundational contract for all template variables in conversus. This is a critical piece of infrastructure: specs 006 (Inter-Round Arbitration), 008 (Executable Conversus), and any future mode or phase extension will depend on this schema being correct, complete, and extensible. The implementation delivered against spec 005 is solid — the schema captures all 7 phases, all 4 modes, and correctly separates universal variables from mode-specific ones. The Pydantic model layer (`linter/models.py`) enforces type safety at both schema-load and runtime-context levels, aligned with Constitution Principle IX. The linter itself is well-structured with pure validation functions composed into a single `validate_template` entrypoint.

However, the schema and linter have significant gaps when viewed through the lens of downstream specs. The variable schema has no provision for the `PRIOR_ARBITRATION_PATH` or `ARBITRATION_PATHS` variables required by spec 006, and the schema's extensibility model does not account for variables that are conditionally present based on config fields (like `arbiter.timing: inter-round`) rather than mode or phase. The linter is tightly coupled to the Click CLI, which conflicts with spec 008's vision of conversus as a standalone executable that invokes the linter programmatically. The `pyproject.toml` lacks entry points, package discovery configuration, and the `[project.scripts]` section needed for distributable packaging. The test suite, while comprehensive for current templates, does not test schema evolution scenarios — adding a new variable or a new phase produces no regression signal.

The single most important recommendation is: add a `config_condition` field to `VariableDefinition` and corresponding Pydantic context models so that spec 006's `PRIOR_ARBITRATION_PATH` and `ARBITRATION_PATHS` variables can be declared in the schema without breaking existing templates that do not use them.

### Alignment

- **Phase coverage is complete.** The schema declares all 7 phases in execution order (review through cross-round-synthesis), matching the SKILL.md phase model exactly. This supports spec 006's requirement that Phase 6 can run between rounds, since the arbitration phase is already a first-class schema citizen. (`schema/variables.yml`, lines 17-18; `linter/models.py`, lines 28-31)

- **Mode schemas capture the dispute-parsing subsystem interface.** Each mode's YAML file declares `disputes.synthesis_heading`, `disputes.entry_pattern`, and `disputes.structural_markers` — the exact stable interfaces that spec 006 FR-005 needs for post-arbitration dispute counting. (`schema/modes/cooperative.yml`, lines 20-25; `specs/006-inter-round-arbitration/spec.md`, FR-015)

- **Pydantic models enforce Constitution Principle IX rigorously.** The `VariableDefinition`, `ModeSchema`, and per-phase `TemplateContext` subclasses ensure that raw YAML is never used directly. The `model_config = {"extra": "forbid"}` on `TemplateContext` prevents undeclared variables from sneaking through at runtime, which is exactly the safety net that spec 006 and 008 need. (`linter/models.py`, lines 8-10, 140)

- **The linter validates both structural markers and required headings.** This two-layer validation (variable presence + output structure) directly serves the dispute-parsing subsystem that spec 006 depends on — if a synthesis template loses its `DISPUTES_BEGIN`/`DISPUTES_END` markers, the linter catches it before the inter-round arbitration loop runs. (`linter/validate.py`, lines 259-278)

- **`validate_templates` config flag exists in SKILL.md.** The opt-out mechanism (`validate_templates: false`) gives spec 008's executable conversus the ability to skip validation when running in a CI environment where templates are pre-validated, reducing startup latency. (`SKILL.md`, line 36; `specs/005-generalized-templates/spec.md`, US-4 AC-3)

- **The `MODE_PRESENCE` lookup table handles conditional MODE usage correctly.** The hardcoded truth table for which (phase, mode) pairs require `{MODE}` prevents false positives in modes where MODE is not referenced in early phases. This is the right approach — it avoids the complexity of conditional expressions in the schema while capturing the actual template reality. (`linter/validate.py`, lines 108-144)

### Missed Opportunities

- **No `config_condition` field for config-dependent variables.** Spec 006 introduces `PRIOR_ARBITRATION_PATH` (FR-012) and `ARBITRATION_PATHS` (FR-013), which are only present when `arbiter.timing: inter-round`. The current schema supports only `modes` as a conditional axis (e.g., `AGENT_ROLE` is red-blue only). There is no way to declare "this variable exists only when config field X has value Y." Without this, spec 006 cannot add its variables to the schema without either: (a) making them universally optional (losing validation value), or (b) creating a parallel validation path outside the linter. (`schema/variables.yml`, lines 8-16; `specs/006-inter-round-arbitration/spec.md`, FR-012, FR-013)

- **No programmatic API for the linter.** `validate.py` is structured as a Click CLI script with `main()` decorated by `@click.command()`. Spec 008 envisions conversus as an executable package where validation is invoked programmatically during the orchestration loop (SKILL.md Step 3). The current design requires either subprocess invocation or importing and calling internal functions that bypass the CLI layer. A `validate_all(root, mode=None)` function returning a structured result (not printing to stdout and calling `sys.exit`) is missing. (`linter/validate.py`, lines 312-371; `specs/008-executable-conversus/001-executable-conversus.md`, Phase 5)

- **No `ArbitrationContext` support for inter-round context variables.** The `ArbitrationContext` Pydantic model in `models.py` has no `PRIOR_ARBITRATION_PATH` field. When spec 006 is implemented, the Phase 6 template for Round 2+ inter-round arbitration needs the path to the prior round's arbitration output so the arbiter knows what it already ruled on. This field must be `Optional[str]` on `ArbitrationContext`. (`linter/models.py`, lines 234-246; `specs/006-inter-round-arbitration/spec.md`, Template Reuse section)

- **`CrossRoundSynthesisContext` missing `ARBITRATION_PATHS` field.** Spec 006 FR-013 requires `{ARBITRATION_PATHS}` in the cross-round synthesis template — a newline-separated list of per-round arbitration resolution paths. The current `CrossRoundSynthesisContext` model does not include this variable. (`linter/models.py`, lines 249-258; `specs/006-inter-round-arbitration/spec.md`, FR-013)

- **`ReviewContext` missing `PRIOR_ARBITRATION_PATH` field.** Spec 006 FR-009 and FR-012 state that all Phase 1-5 templates must support `{PRIOR_ARBITRATION_PATH}` for inter-round arbitration context injection. None of the Phase 1-5 context models include this field. (`linter/models.py`, lines 146-160; `specs/006-inter-round-arbitration/spec.md`, FR-009, FR-012)

- **No schema versioning.** The schema files have no version field. When spec 006 adds new variables, there is no way to determine which schema version a template was validated against. This matters for spec 008's executable conversus, which may need to support multiple schema versions during migration periods. (`schema/variables.yml`; `specs/008-executable-conversus/001-executable-conversus.md`)

- **Linter error output is string-based, not structured.** All validation functions return `list[str]` — human-readable error strings. Spec 008's executable conversus needs machine-readable errors (with fields for file path, error type, variable name, phase, mode) so the orchestration engine can make programmatic decisions (e.g., "skip this template and use fallback" vs. "abort the run"). (`linter/validate.py`, all `check_*` functions)

- **`pyproject.toml` has no entry points or package structure.** The file declares a project name and dependencies but no `[project.scripts]` entry point, no `[tool.setuptools.packages]` or equivalent, and no `py.typed` marker. Spec 008 requires conversus to be installable as a CLI tool (`conversus run`, `conversus lint`). The current `pyproject.toml` cannot produce a distributable package. (`pyproject.toml`, lines 1-16; `specs/008-executable-conversus/001-executable-conversus.md`, Goal section)

- **Test suite does not cover schema evolution.** The tests validate current templates against the current schema. There are no tests that verify: (a) adding a new required variable to `variables.yml` produces errors for templates missing it, (b) adding a new phase to `VALID_PHASES` is handled gracefully, (c) adding a new mode schema file is discovered automatically. These are the exact scenarios that spec 006 implementation will trigger. (`linter/test_validate.py`)

### Off-Base Assumptions

- **The spec assumes the linter is a development-time-only tool.** Section 6 states: "It does NOT run at agent runtime (unless integrated per FR-008)" and FR-008 hedges with "SHOULD validate." But SKILL.md Step 3 already integrates validation as a mandatory pre-execution step (lines 260-271). The linter is not optional infrastructure — it is a runtime dependency of the orchestrator. The spec's framing as a development-time tool understates its architectural role and may lead to insufficient investment in its programmatic API, error structures, and performance characteristics. (`specs/005-generalized-templates/spec.md`, Section 6, paragraph 1; `SKILL.md`, lines 260-271)

- **The spec assumes `MODE_PRESENCE` is derivable from the schema.** The implemented `MODE_PRESENCE` lookup table in `validate.py` (lines 108-144) is a hardcoded truth table that cannot be derived from `variables.yml` or the mode schemas. The spec's data model section shows MODE as having `phases: [review, synthesis, arbitration, cross-round-synthesis]` — but the actual schema has MODE in ALL 7 phases with a complex `condition` field. The hardcoded table is the correct implementation, but the spec does not acknowledge that MODE's conditional presence requires special handling beyond the schema's `modes` field. This means future maintainers adding a new mode will need to update the `MODE_PRESENCE` table manually — a brittle coupling the spec does not document. (`specs/005-generalized-templates/spec.md`, Section 3 data model, MODE entry; `linter/validate.py`, lines 108-144)

- **The spec treats `AGENT_DOCS` as `path-list` but the implementation types it as `extracted-content`.** The spec's data model section (line 171-175) declares `AGENT_DOCS` with `type: path-list`. The implemented `schema/variables.yml` (line 46-51) correctly types it as `extracted-content` — AGENT_DOCS is documentation content extracted and injected, not a list of paths for the agent to read. The spec's data model is outdated relative to the implementation, and this discrepancy should be resolved in favor of the implementation. (`specs/005-generalized-templates/spec.md`, line 171; `schema/variables.yml`, lines 46-51)

### Actionable Recommendations

1. **Add config-condition field to VariableDefinition** (Priority: P1)
   - **Current state**: `VariableDefinition` supports only `modes` as a conditional axis (`schema/variables.yml`, line 15; `linter/models.py`, line 49). Variables that depend on config values (e.g., `arbiter.timing`) have no representation.
   - **Proposed change**: Add `config_conditions: Optional[dict[str, str]]` to `VariableDefinition`. Example: `config_conditions: {"arbiter.timing": "inter-round"}`. The linter skips checking this variable unless the condition is met. For development-time validation (no config available), the linter treats config-conditioned variables as optional. For runtime validation (config available, spec 008), the linter enforces them when the condition is met.
   - **Rationale**: Spec 006 FR-012 requires `PRIOR_ARBITRATION_PATH` in all Phase 1-5 templates, but only when `arbiter.timing: inter-round`. Without this field, spec 006 either cannot use the schema or must make the variable universally optional, losing the enforcement value the schema exists to provide. `[specs/006-inter-round-arbitration/spec.md, FR-012]`
   - **Risk if ignored**: Spec 006 implementation will bypass the schema/linter for its new variables, creating a second validation path and fragmenting the "single source of truth" that spec 005 established.

2. **Extract a programmatic validation API from the CLI** (Priority: P1)
   - **Current state**: `validate.py` exposes only a Click CLI entry point (`main()`, line 317). Internal validation functions are usable but return unstructured strings and rely on `click.echo`/`sys.exit` for output.
   - **Proposed change**: Create a `validate_all(root: Path, mode: Optional[str] = None) -> ValidationResult` function that returns a structured `ValidationResult` Pydantic model containing `errors: list[ValidationError]`, `files_checked: int`, and `passed: bool`. Each `ValidationError` has fields: `file_path`, `error_type` (enum: `missing_variable`, `unknown_variable`, `missing_heading`, `missing_marker`), `variable_name`, `phase`, `mode`, `suggestion`. The Click CLI becomes a thin wrapper calling `validate_all`.
   - **Rationale**: Spec 008 requires the linter to be invoked programmatically from the orchestration engine, not via subprocess. SKILL.md Step 3 (line 262) already treats validation as an engine step. A structured API is needed for the engine to make decisions based on error types. `[specs/008-executable-conversus/001-executable-conversus.md, Phase 5; SKILL.md, lines 260-271]`
   - **Risk if ignored**: Spec 008 will either shell out to `validate.py` (fragile, loses type safety) or reimplement validation logic in the orchestrator (duplication, drift from schema).

3. **Add `PRIOR_ARBITRATION_PATH` to Phase 1-5 context models and `ARBITRATION_PATHS` to CrossRoundSynthesisContext** (Priority: P1)
   - **Current state**: `ReviewContext`, `CrossReviewContext`, `RevisionContext`, `DisputesContext`, and `SynthesisContext` have no `PRIOR_ARBITRATION_PATH` field (`models.py`, lines 146-232). `CrossRoundSynthesisContext` has no `ARBITRATION_PATHS` field (lines 249-258).
   - **Proposed change**: Add `PRIOR_ARBITRATION_PATH: Optional[str] = None` to all Phase 1-5 context models. Add `ARBITRATION_PATHS: Optional[str] = None` to `CrossRoundSynthesisContext`. Add corresponding entries in `schema/variables.yml` with `config_conditions: {"arbiter.timing": "inter-round"}`.
   - **Rationale**: Spec 006 FR-009 requires `{PRIOR_ARBITRATION_PATH}` as a mandatory read for Phase 1 agents when inter-round arbitration fired in the prior round. FR-013 requires `{ARBITRATION_PATHS}` in cross-round synthesis. Without these fields in the context models, the `extra: "forbid"` config on `TemplateContext` will reject them at runtime. `[specs/006-inter-round-arbitration/spec.md, FR-009, FR-012, FR-013]`
   - **Risk if ignored**: Spec 006 implementation will hit Pydantic validation errors when trying to pass inter-round arbitration paths to templates. The fix will require modifying the foundational models that spec 005 established, with no test coverage for the change.

4. **Add `ARBITRATION_RULINGS` variable for cross-round synthesis** (Priority: P1)
   - **Current state**: The cross-round synthesis template has `ROUND_SYNTHESES` but no variable carrying the content of arbiter rulings across rounds.
   - **Proposed change**: Add `ARBITRATION_RULINGS: Optional[str] = None` to `CrossRoundSynthesisContext` and `schema/variables.yml` under phase `cross-round-synthesis`. This carries the extracted content from all per-round arbitration resolutions, formatted for the cross-round synthesizer to attribute dispute resolution to agents vs. arbiter.
   - **Rationale**: Spec 006 FR-014 requires the cross-round synthesis to include a "Resolution Attribution" section tracking agent convergence vs. arbiter ruling. `ARBITRATION_PATHS` gives file paths; `ARBITRATION_RULINGS` gives extracted content. The cross-round synthesizer needs both. `[specs/006-inter-round-arbitration/spec.md, FR-014]`
   - **Risk if ignored**: The cross-round synthesis agent will need to read and parse arbitration files itself, violating Constitution Principle VIII (Templating Engines Over Inference) — the orchestrator should extract and inject, not delegate parsing to agents.

5. **Add `[project.scripts]` entry point to pyproject.toml** (Priority: P2)
   - **Current state**: `pyproject.toml` declares project metadata and dependencies but no entry points or package discovery (`pyproject.toml`, lines 1-16).
   - **Proposed change**: Add `[project.scripts]` with `conversus-lint = "conversus.linter.validate:main"` (or equivalent after establishing package structure). Add `[tool.setuptools.packages.find]` or equivalent build-system configuration. Add `packages = ["conversus"]` or equivalent to enable `pip install -e .`.
   - **Rationale**: Spec 008 envisions `conversus run` as a standalone CLI command. The current `pyproject.toml` cannot produce a distributable package or a `conversus-lint` command. The linter is the first executable component; its entry point establishes the pattern for the future `conversus run` command. `[specs/008-executable-conversus/001-executable-conversus.md, Goal section]`
   - **Risk if ignored**: Spec 008 implementation will need to retroactively restructure the package layout, potentially breaking the linter's import paths (`from models import ...` uses bare imports, not package-relative).

6. **Add schema evolution regression tests** (Priority: P2)
   - **Current state**: `test_validate.py` tests current templates against the current schema. No tests verify that the schema can be extended without breaking existing templates. (`linter/test_validate.py`)
   - **Proposed change**: Add a `TestSchemaEvolution` class with tests: (a) a test that adds a new optional variable to the schema and verifies all templates still pass, (b) a test that adds a new required variable for a specific phase and verifies it produces errors only for that phase's templates, (c) a test that adds a new mode schema file and verifies the linter discovers and validates it.
   - **Rationale**: Spec 006 will add `PRIOR_ARBITRATION_PATH` and `ARBITRATION_PATHS` to the schema. Spec 008 may add CLI-specific variables. Without evolution tests, there is no regression signal when these additions accidentally break existing validation logic. The schema is a foundation — its extensibility must be tested. `[specs/006-inter-round-arbitration/spec.md, FR-012, FR-013]`
   - **Risk if ignored**: Spec 006 implementation may introduce schema changes that cause silent validation regressions, discovered only when agents fail at runtime — exactly the problem spec 005 was designed to prevent.

7. **Document MODE_PRESENCE table maintenance in the schema** (Priority: P2)
   - **Current state**: The `MODE_PRESENCE` lookup table in `validate.py` (lines 108-144) is a hardcoded truth table derived from scanning all 28 templates. The comment on line 105 documents this but the schema files have no corresponding declaration. Adding a new mode requires manually adding entries to this table.
   - **Proposed change**: Add a `mode_presence` section to each mode schema YAML file declaring which phases use `{MODE}` in templates for that mode. Example for cooperative: `mode_presence: [review, cross-review, revision, disputes, synthesis, arbitration, cross-round-synthesis]`. The linter reads this instead of the hardcoded table.
   - **Rationale**: The hardcoded table creates a brittle coupling between the linter and template content that is invisible to schema maintainers. When spec 006 modifies templates to include `{MODE}` in new contexts, or a new mode is added, the `MODE_PRESENCE` table must be updated manually. Moving this to the schema makes the contract explicit and self-documenting. `[constitution.md, Principle II: Stable Interfaces]`
   - **Risk if ignored**: A new mode or template change silently desynchronizes the `MODE_PRESENCE` table, producing false positive or false negative validation results that undermine trust in the linter.

8. **Use structured error objects instead of string lists** (Priority: P2)
   - **Current state**: All `check_*` functions in `validate.py` return `list[str]` — formatted error messages. (`linter/validate.py`, all check functions)
   - **Proposed change**: Define a `ValidationError` Pydantic model with fields: `file_path: str`, `error_type: Literal["missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"]`, `detail: str`, `variable_name: Optional[str]`, `phase: str`, `mode: str`, `suggestion: Optional[str]`. All `check_*` functions return `list[ValidationError]`. The CLI formats them for human display; the programmatic API returns them as-is.
   - **Rationale**: Constitution Principle IX mandates Pydantic models for all data structures. Error results are data structures. Spec 008's orchestrator needs to distinguish error types programmatically (e.g., "missing marker" is a blocking error, "unknown variable that looks like a markdown artifact" might be a warning). String parsing for this is fragile. `[constitution.md, Principle IX; specs/008-executable-conversus/001-executable-conversus.md]`
   - **Risk if ignored**: Spec 008 will either parse error strings with regex (fragile, ironic for a linter) or ignore error types entirely (losing the ability to distinguish warnings from errors).

9. **Add a schema version field** (Priority: P3)
   - **Current state**: Neither `variables.yml` nor mode schema files have a version field. There is no way to determine which schema version a template was validated against.
   - **Proposed change**: Add `schema_version: "1.0.0"` to the top level of `variables.yml`. The linter reports the schema version in its output. Future schema changes increment the version following semver (minor for new variables, major for breaking changes like renaming or removing variables).
   - **Rationale**: Spec 008's executable conversus may need to support schema migration during rolling updates. Spec 006 will add variables to the schema — a version bump signals to all consumers that the contract has changed. Without versioning, there is no way to detect or communicate schema evolution. `[constitution.md, Governance section — versioning guidance]`
   - **Risk if ignored**: Schema changes are invisible to consumers. Templates validated against schema v1 may fail against schema v2 with no indication of what changed or when.

10. **Fix `AGENT_DOCS` type discrepancy between spec and implementation** (Priority: P3)
    - **Current state**: The spec's data model (Section 3, line 171) declares `AGENT_DOCS` as `type: path-list`. The implemented schema (`schema/variables.yml`, lines 46-51) correctly types it as `extracted-content`.
    - **Proposed change**: Update the spec's data model section to match the implementation: `AGENT_DOCS` has `type: extracted-content`. Add a note explaining the distinction: path-list variables are paths the agent reads; extracted-content variables are pre-extracted documentation injected into the prompt.
    - **Rationale**: The spec is the historical record of what was designed. If the spec says `path-list` but the implementation says `extracted-content`, future implementors working from the spec (e.g., spec 008's Python orchestrator) will use the wrong type. `[specs/005-generalized-templates/spec.md, Section 3; schema/variables.yml, lines 46-51]`
    - **Risk if ignored**: Spec 008's orchestrator implementor reads the spec, builds the agent context with `AGENT_DOCS` as a list of paths, and the template receives paths instead of documentation content — agents fail to see their grounding material.

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/006-inter-round-arbitration/spec.md`
- `<HOME>/code/payer-index-mono/conversus/specs/008-executable-conversus/001-executable-conversus.md`
- `<HOME>/code/payer-index-mono/conversus/SKILL.md`
- `<HOME>/code/payer-index-mono/conversus/.specify/memory/constitution.md`
- `<HOME>/code/payer-index-mono/conversus/schema/variables.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/modes/cooperative.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/modes/red-blue.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/modes/winner-take-all.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/modes/prisoners-dilemma.yml`
- `<HOME>/code/payer-index-mono/conversus/linter/models.py`
- `<HOME>/code/payer-index-mono/conversus/linter/validate.py`
- `<HOME>/code/payer-index-mono/conversus/linter/test_validate.py`
- `<HOME>/code/payer-index-mono/conversus/pyproject.toml`
- `<HOME>/code/payer-index-mono/conversus/specs/005-generalized-templates/spec.md`
