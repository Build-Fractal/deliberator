# Cross-Round Synthesis: Spec 005 -- Generalized Template Schema, Variables, and Linter

**Synthesizer**: neutral (cross-round)
**Spec**: `005-generalized-templates`
**Deliberation mode**: cooperative
**Agents**: functional-typing, game-engine-advocate, integration-architect
**Rounds completed**: 2 of 2
**Termination reason**: Converged -- no disputes remain after Round 2
**Date**: 2026-03-21

---

## Process Summary

| Metric | Round 1 | Round 2 | Cumulative |
|--------|---------|---------|------------|
| Agents | 3 | 3 | 3 |
| Phase 1 reviews | 3 | 3 | 6 |
| Phase 2 cross-reviews | 6 | 6 | 12 |
| Phase 3 revisions | 3 | 3 | 6 |
| Phase 4 dispute filings | 3 | 3 | 6 |
| Original recommendations | 29 | 13 new | 42 |
| Recommendations withdrawn | 5 | 4 additional | 9 |
| Concessions (total) | 17 | 4 additional | 21 |
| Dangerous contradictions identified | 5 | 6 | 11 |
| Dangerous contradictions resolved | 5 | 6 | 11 |
| Disputes remaining after round | 4 | 0 architectural, 2 prioritization (synthesizer-resolved) | 0 |
| Convergence items | 14 | 20 (superseding) | 20 |

The deliberation terminated via convergence: all four Round 1 disputes were resolved by the Round 1 synthesis and accepted by all three agents in Round 2 without reversal. Round 2 produced no new architectural disputes. The two remaining prioritization questions after Round 2 were resolved by synthesizer discretion (reverse template check bundling with P2-1, and P3-5 scope relative to P1-4), neither of which involved disagreement on whether the work should be done.

---

## Dispute Trajectory

### Round 1: 4 Active Disputes

1. **Programmatic API parameter design** (game-engine-advocate vs. integration-architect vs. functional-typing). Whether `validate_all()` should accept `known_plugin_variables` from day one, use a `ValidationConfig` model without plugin fields, or use bare parameters.
2. **`LintError.error_type` -- `Literal` vs. `str`** (game-engine-advocate vs. integration-architect, functional-typing leaning integration-architect). Whether error types are a closed code-internal set or an open plugin-extensible set.
3. **Schema version field priority -- P2 vs. P3** (functional-typing vs. integration-architect + game-engine-advocate). Whether versioning a single YAML line merits P2 or P3.
4. **Bare import fix sequencing -- P1 prerequisite vs. P2 separate item** (game-engine-advocate vs. integration-architect). Whether fixing bare imports is part of the P1 API work or a separate P2 deliverable.

**Resolution mechanism**: All four were resolved by the Round 1 synthesizer using analysis of the arguments and consistency with the deliberation's governing principles. The synthesizer selected `ValidationConfig` model without plugin fields (Dispute 1), `str` with runtime validation against `KNOWN_ERROR_TYPES` frozenset (Dispute 2), P2 priority (Dispute 3), and import fix bundled with P1 API extraction (Dispute 4).

### Round 2: 0 Disputes (Convergence Achieved)

All four Round 1 synthesizer resolutions were accepted by all three agents without reversal. Round 2's cross-review process produced six new dangerous contradictions (R6-R11), all resolved through concession during the same round. Two minor prioritization/scoping questions were resolved by synthesizer discretion in the Round 2 synthesis.

**Key resolution mechanisms in Round 2**:
- Convergent dual-reviewer identification: every Round 2 withdrawal was prompted by both cross-reviewers independently identifying the same flaw using different analytical lenses (R6, R7, R8, R9, R10, R11).
- Application of the Round 1 governing principle ("freeze first, compose later") as a corrective lens for new scope-inflation instances (R8, R9, R10, R11).

---

## Proposal Evolution

### functional-typing

**Round 1 thesis**: Maximize type safety and functional purity in the linter implementation. Original recommendations focused on `Literal` types for enums, `frozen=True` immutability, `Final` for constants, pure function extraction, and `PathList` typed patterns.

**Round 1 adaptations**: Withdrew `Literal` types (FT-3) after game-engine-advocate demonstrated conflict with SC-003 extensibility -- functional-typing called this "the deepest intellectual correction." Withdrew `Final` on `PHASE_CONTEXT_MODELS` (FT-8) after accepting it is a registry. Modified `MODE_PRESENCE` derivation (FT-5) from condition-field parsing to YAML approach. Withdrew `itertools.chain` optimization after structured error models made it irrelevant. Deferred `__all__` exports (FT-7) as premature.

**Round 2 adaptations**: Withdrew warning-only `@field_validator` on `error_type` (FT-D2-Ref) after both cross-reviewers identified pattern inconsistency with mode validation. Withdrew separate `ValidationContext` frozen dataclass (FT-MO-1) after both cross-reviewers identified dual-abstraction maintenance hazard.

**Feedback incorporated**: game-engine-advocate's extensibility arguments (Literal withdrawal, PHASE_CONTEXT_MODELS withdrawal, __all__ deferral); integration-architect's structured error model approach (adopted as FT-A); both reviewers' pattern consistency critique (error_type warning withdrawal); both reviewers' dual-abstraction critique (ValidationContext withdrawal).

**Feedback ignored**: None. functional-typing incorporated all substantive feedback across both rounds.

**Net trajectory**: Started as the strictest type-safety advocate. Ended with a refined position: type safety is paramount within each spec's scope, but types that close extension surfaces belonging to downstream specs are counterproductive. The "freeze first, compose later" principle became functional-typing's own lens for evaluating extensibility proposals in Round 2. Total concessions: 7 (5 in Round 1, 2 in Round 2).

### game-engine-advocate

**Round 1 thesis**: Front-load plugin extensibility into the foundation spec. Original recommendations focused on plugin variable namespaces, extensible TemplateContext, dynamic mode registry, float types, schema versioning, ModeSchema extensions, and extensibility documentation.

**Round 1 adaptations**: The largest positional shift of any agent -- conceded 7 of 10 original recommendations as scope inflation ("spec 007 concerns dressed as spec 005 feedback"). Deferred 5 recommendations to spec 007. Withdrew `extra = "allow"` (GE-2), template-scanning for MODE_PRESENCE (GE-6), float/number type (GE-4). Downgraded `VALID_MODES` from P1 to P2 (GE-3). Acknowledged the fundamental principle: "Spec 005's job is to be a correct, well-structured foundation. Making it extensible is spec 007's job."

**Round 2 adaptations**: Conceded R1 docstring field-name prescription after both cross-reviewers identified specific field-name encoding as scope inflation in prose form. Revised R3 to withdraw `extra = "ignore"` on ModeSchema after both cross-reviewers identified it as the withdrawn GE-2 argument reappearing through documentation.

**Feedback incorporated**: functional-typing's Principle IX arguments (extra = "allow" withdrawal); integration-architect's scope discipline arguments (5 deferrals, P1-to-P2 downgrade); integration-architect's circular validation critique (template scanning withdrawal); both reviewers' prose-level scope inflation critique (docstring prescription, extra = "ignore").

**Feedback ignored**: None. game-engine-advocate incorporated all substantive feedback, though the programmatic API parameter dispute (GE-N1) required synthesizer resolution in Round 1 rather than voluntary concession.

**Net trajectory**: Started as the broadest extensibility advocate. Ended as a disciplined contributor who internalized scope boundaries and actively applied the "freeze first, compose later" principle to evaluate others' proposals in Round 2. The Round 2 synthesis confirmed that game-engine-advocate used this principle as a self-check ("the governing principle for my Round 2 positions"). Total concessions: 9 (7 in Round 1, 2 in Round 2).

### integration-architect

**Round 1 thesis**: Strengthen the schema with operational concerns -- config conditions, programmatic API extraction, spec 006 variable additions, structured errors, and packaging infrastructure.

**Round 1 adaptations**: Retracted two internal contradictions identified by cross-reviewers: MODE_PRESENCE endorsed in Alignment but criticized in Rec 7 (IA-N1), and schema-loading functions characterized as "pure" while containing `sys.exit()` (IA-N2). Replaced weakly-typed `dict[str, str]` with typed `ConfigCondition` model (IA-1) per functional-typing's refinement. Withdrew `plugin_data: dict[str, Any]` (IA-N4) in Phase 4 after both other agents identified it as a Principle IX violation. Upgraded schema versioning from P3 to P2 (IA-9).

**Round 2 adaptations**: Withdrew SKILL.md `allowed-tools` for linter invocation (IA-Rec1) after both cross-reviewers identified it as scope inflation into spec 008. Modified Rec 4 to remove prescriptive workaround for filename-phase constraint. Modified Rec 5 to remove backward-compatibility commitment for `validate_templates`.

**Feedback incorporated**: functional-typing's type refinement demands (ConfigCondition model, import purity); game-engine-advocate's scope discipline feedback (SKILL.md withdrawal, prescriptive workaround removal); functional-typing's premature commitment critique (validate_templates backward-compat removal).

**Feedback ignored**: None. integration-architect incorporated all substantive feedback across both rounds.

**Net trajectory**: Started with the most operationally grounded recommendations but with two internal contradictions and one Principle IX violation. Through cross-review, achieved internal consistency and refined all proposals to match the deliberation's governing principles. Round 2 showed that integration-architect's scope inflation instincts -- when present -- took a subtler form than game-engine-advocate's (prescribing workarounds and committing to backward compatibility rather than front-loading extension mechanisms), but the cross-review mechanism caught all instances. Total concessions: 8 (5 in Round 1, 3 in Round 2).

---

## Final Convergence Record

The definitive list of all agreed-upon spec changes from the complete 2-round process. Items are organized by priority. Each item represents the final, post-Round-2 formulation with all refinements applied.

### P1 -- Must be addressed before spec 005 can be considered complete

**P1-1: Purify schema-loading functions**
- Replace `sys.exit(2)` and `click.echo()` in `load_variables_schema`, `load_mode_schema`, and `find_project_root` with `SchemaLoadError` exceptions. CLI `main()` is the sole site of `sys.exit()`.
- Affects: `linter/validate.py`
- Source: Round 1 FT-1 (unanimous). Reaffirmed Round 2 by all three agents as highest-leverage change. Zero positional movement across both rounds -- this was unanimous from the start.

**P1-2: Extract programmatic validation API**
- Create `validate_all(config: ValidationConfig) -> ValidationResult` where `ValidationConfig` is a Pydantic model with `root: Path` and `mode: Optional[str] = None`.
- `ValidationResult` is a Pydantic model with `errors: list[LintError]`, `files_checked: int`, `passed: bool`.
- Fix bare imports (`from models import ...` -> `from .models import ...`) as part of this work.
- Click CLI `main()` becomes a thin wrapper calling `validate_all()`.
- `ValidationConfig` docstring: "Downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields."
- `ValidationConfig` is the sole public configuration surface. No parallel `ValidationContext`, no `**kwargs`, no pre-emptive plugin parameters.
- Affects: `linter/validate.py`, `linter/__init__.py`
- Source: Round 1 IA-2, FT-1 (prerequisite), GE-N2 (import fix). Round 1 dispute resolved by synthesizer (ValidationConfig model without plugin fields). Round 2 refinements: docstring phrasing narrowed to directional hint (all agents converge), ValidationContext withdrawn (functional-typing concession).

**P1-3: Define `PathList` custom type**
- Pydantic custom type storing `list[Path]` internally with `BeforeValidator` for newline-separated string parsing and custom serializer for template substitution.
- Export from `models.py` as a reusable type. Apply to all path-list fields.
- Explicitly EXCLUDE `ROUND_SYNTHESES` (which is `type: extracted-content`, not `path-list`).
- Implementation instruction: verify each field's comment and type annotation against the corresponding `variables.yml` schema declaration during conversion.
- Affects: `linter/models.py`, `schema/variables.yml` (documentation)
- Source: Round 1 FT-2 (modified per IA serializer design). Round 2: ROUND_SYNTHESES exclusion added (integration-architect Rec 3, unanimous).

**P1-4: Add `config_conditions` field with typed `ConfigCondition` model**
- `ConfigCondition(BaseModel)` with `field: str` and `value: str`.
- `config_conditions: Optional[list[ConfigCondition]] = None` on `VariableDefinition`.
- Validate `field` values against known config field names at schema-load time.
- Enables spec 006's `PRIOR_ARBITRATION_PATH` (conditioned on `arbiter.timing: inter-round`).
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: Round 1 IA-1 (modified per FT refinement). Round 2: P3-5 resolved as future extension of this model (convergence item 20).

**P1-5: Add spec 006 variables to context models and schema**
- `PRIOR_ARBITRATION_PATH: Optional[Path] = None` added to `ReviewContext`, `CrossReviewContext`, `RevisionContext`, `DisputesContext`, `SynthesisContext`.
- `ARBITRATION_PATHS` (using `PathList` type) added to `CrossRoundSynthesisContext`.
- `ARBITRATION_RULINGS: Optional[str] = None` added to `CrossRoundSynthesisContext`.
- Corresponding entries in `schema/variables.yml` with appropriate `config_conditions`.
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: Round 1 IA-3, IA-4. Stable across both rounds.

### P2 -- Should be addressed in spec 005's scope

**P2-1: Move MODE_PRESENCE to mode schema YAML declarations with bidirectional template validation**
- Add `mode_in_phases` field to each mode schema YAML.
- Derive lookup table via pure function at load time. Delete the hardcoded 28-entry `MODE_PRESENCE` dict.
- Add reverse template existence check: report template files on disk not declared in the mode schema's `templates` list.
- Bidirectional validation as a single deliverable.
- Affects: `schema/modes/*.yml`, `linter/validate.py`, `linter/models.py` (ModeSchema model)
- Source: Round 1 FT-5, GE-6, IA-7 (unanimous). Round 2: reverse check bundled (game-engine-advocate NR-2, synthesizer resolution).

**P2-2: Make `VALID_MODES` a dynamic registry**
- Replace `VALID_MODES = frozenset({...})` with `get_valid_modes(schema_dir: Path) -> frozenset[str]` scanning `schema/modes/*.yml`.
- Affects: `linter/models.py`, `linter/validate.py`
- Source: Round 1 GE-3 (P2). Stable across both rounds.

**P2-3: Structured `LintError` Pydantic model with strict error type validation**
- `LintError(BaseModel)` with `error_type: str` validated against `KNOWN_ERROR_TYPES: frozenset[str]`.
- `KNOWN_ERROR_TYPES` contains `{"missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"}`.
- `@field_validator` on `error_type` raises `ValueError` for types not in `KNOWN_ERROR_TYPES`. Plugins register their types at module initialization before producing errors.
- `KNOWN_ERROR_TYPES` constructed at module load time from a base set plus plugin-registered types.
- All `check_*` functions return `list[LintError]`. CLI `main()` formats for human display.
- Affects: `linter/validate.py`, `linter/models.py`
- Source: Round 1 IA-8, FT-A. Round 1 dispute resolved by synthesizer (`str` with `frozenset` validation). Round 2: strict rejection semantics confirmed (game-engine-advocate NR-1, integration-architect New Rec B, functional-typing concedes warning-only proposal).

**P2-4: Schema versioning**
- Add `schema_version: "1.0.0"` to `variables.yml` top level.
- Add `schema_version` field to `VariablesSchema` Pydantic model.
- Must be done before spec 006 adds variables.
- Schema version compatibility validation deferred to the spec that introduces schema version 2.0.
- Affects: `schema/variables.yml`, `linter/models.py`
- Source: Round 1 GE-5, IA-9 (both upgraded to P2). Round 2: deferral note added (game-engine-advocate R4).

**P2-5: Apply `frozen=True` to `TemplateContext` hierarchy**
- `model_config = {"extra": "forbid", "frozen": True}` on `TemplateContext` and all subclasses.
- Plugin-contributed data flows through separate `PluginContext` model, designed in spec 007.
- Affects: `linter/models.py`
- Source: Round 1 FT-4. Stable across both rounds.

**P2-6: Document extension contracts in spec 005**
- Add a section to spec Section 6 titled "Extension Points for Downstream Specs" documenting:
  - **Extension points**: new variables via `schema/variables.yml`, new modes via `schema/modes/{mode}.yml`, new config conditions via `ConfigCondition`, plugin-contributed data via parallel composition (spec 007), `PHASE_CONTEXT_MODELS` as an extensible registry, `ModeSchema` accepts new typed fields via model definition modification (with `extra = "forbid"` enforced), `KNOWN_ERROR_TYPES` as an extensible registry with strict validation.
  - **NOT extension points**: `extra = "forbid"` on all core Pydantic models, template syntax `{VARIABLE}`, structural marker syntax, template filename-to-phase-name 1:1 mapping (`phase = tmpl_path.stem`).
  - **Observations (not commitments)**: `validate_templates` is boolean in v1; granular validation control is a potential future concern but is not designed here.
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 GE-9. Round 2 substantially expanded: PHASE_CONTEXT_MODELS (game-engine-advocate R2), ModeSchema extensibility (game-engine-advocate R3 revised), filename-phase constraint (integration-architect Rec 4 revised), validate_templates evolution (integration-architect Rec 5 revised), KNOWN_ERROR_TYPES (game-engine-advocate NR-1, integration-architect New Rec B).

**P2-7: Mandate Python in spec Implementation Notes**
- "The linter MUST be a Python script following Constitution Principle IX."
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 FT-6 (unanimous). Stable across both rounds.

**P2-8: `pyproject.toml` packaging and entry point**
- `[project.scripts]` with `conversus-lint = "conversus.linter.validate:main"`.
- Affects: `pyproject.toml`
- Source: Round 1 IA-5. Stable across both rounds.

**P2-9: Schema evolution regression tests**
- Tests covering: new optional variable passes existing templates, new required variable produces phase-specific errors, new mode schema file is discovered and validated.
- Affects: `linter/test_validate.py`
- Source: Round 1 IA-6. Stable across both rounds.

### P3 -- Should be addressed, low urgency

**P3-1: Document `required: True` default in spec**
- Add to spec Section 3: "Variables default to `required: true` when the field is omitted."
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 FT-9 (unanimous). Stable across both rounds.

**P3-2: Fix `AGENT_DOCS` type discrepancy in spec**
- Update spec Section 3 to show `AGENT_DOCS` as `type: extracted-content` instead of `type: path-list`.
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 IA-10 (unanimous). Stable across both rounds.

**P3-3: Document core-variable vs. plugin-variable namespace rule**
- Comment in `schema/variables.yml` header establishing that core variables carry orchestrator/config data, plugin variables are namespaced separately (mechanism defined by spec 007).
- Affects: `schema/variables.yml`
- Source: Round 1 IA-N3. Stable across both rounds.

**P3-4: Make `VALID_PHASES` extensible**
- Derive from schema data or `PHASE_CONTEXT_MODELS` keys. Lower urgency than `VALID_MODES` because no spec currently adds new phases.
- Affects: `linter/models.py`
- Source: Round 1 GE-8. Stable across both rounds.

**P3-5: Extend `ConfigCondition` with additional condition types**
- Scope redefined in Round 2: extends P1-4's `ConfigCondition` model with an `operator` field to express conditions like `rounds > 1`. This is a P1-4 extension, not a separate grammar for the prose `condition` field.
- The prose `condition` field in `variables.yml` remains documentary, not parsed by `validate.py`.
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: Round 1 GE-N3. Round 2 scope resolution: functional-typing NEW-2, game-engine-advocate NR-3, unanimously converged.

**P3-6: Fix `ROUND_SYNTHESES` comment in models.py**
- Change comment from "newline-separated paths" to "pre-formatted synthesis content per round."
- Ensure this field is NOT included in P1-3 PathList conversion batch.
- Affects: `linter/models.py`
- Source: Round 2 integration-architect Rec 3 (unanimous).

**P3-7: Validate mode schema `templates` entries against known phase names**
- Each entry in the mode schema `templates` list must correspond to a recognized phase name. Bridges P2-1 and P2-6 into a three-part validation chain.
- Affects: `linter/validate.py`
- Source: Round 2 integration-architect New Rec A, functional-typing endorses.

**P3-8: Use `itertools.product` in test case generators**
- Minor readability improvement where applicable.
- Affects: `linter/test_validate.py`
- Source: Round 2 functional-typing MO-2, maintained at P3 and deprioritized.

### Deferred -- Explicitly out of spec 005 scope

**D1: Plugin variable namespace** -- spec 007 Phase 1. Source: GE-1.
**D2: `PluginContext` composition architecture** -- spec 007 Phase 1. Source: GE-2.
**D3: ModeSchema `extensions` section** -- spec 007 Phase 1. Source: GE-7.
**D4: `float`/`number` variable type** -- deferred to the spec that first needs it. Source: GE-4.
**D5: `__all__` exports on `models.py`** -- post-spec-007-Phase-1. Source: FT-7.
**D6: Reserve `schema/objectives/` directory** -- spec 007. Source: GE-10.
**D7: SKILL.md linter invocation pathway** -- spec 008 (executable conversus). Source: Round 2 integration-architect Rec 1 (withdrawn).

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

No remaining disputed positions -- the final convergence is decisive across all evaluated criteria.

All four Round 1 disputes were resolved by the Round 1 synthesizer and accepted by all three agents in Round 2 without reversal. Round 2 produced no new architectural disputes. The two prioritization questions remaining after Round 2 (reverse template check bundling and P3-5 scope) were resolved by synthesizer discretion and accepted by all parties. The eleven dangerous contradictions identified across both rounds were all resolved through concession, revision, or convergence.
<!-- CONVERSUS:DISPUTES_END -->

---

## Termination Assessment

**Was termination appropriate?** Yes. The deliberation met all convergence criteria: zero architectural disputes, zero reversed concessions, and all dangerous contradictions resolved. Continuing to a third round would have produced diminishing returns.

**Did the second round add value?** Yes, substantially. Round 2 accomplished four categories of work that Round 1 could not:

1. **Validated Round 1 stability.** All four Round 1 dispute resolutions and all 17 concessions were tested against a fresh review cycle. None were reversed. This confirmation is itself valuable -- it distinguishes genuine convergence from premature agreement.

2. **Caught subtler scope inflation.** Round 2 identified a new pattern: agents whose code-level scope inflation was corrected in Round 1 attempted the same assumptions through documentation (game-engine-advocate's docstring field-name prescription and `extra = "ignore"` suggestion; integration-architect's prescriptive workarounds and backward-compatibility commitments). The cross-review mechanism caught all four instances. This pattern -- scope inflation migrating from code to prose -- would not have been detected without a second round.

3. **Produced genuine corrections.** functional-typing's warning-only error type validation and separate `ValidationContext` dataclass were both new proposals that survived initial review but were correctly identified and withdrawn after convergent dual-reviewer criticism. These were real architectural hazards (pattern inconsistency and dual-abstraction maintenance burden) that would have entered the convergence record unchallenged had the deliberation stopped at Round 1.

4. **Expanded the convergence record.** Round 2 grew the convergence set from 14 to 20 items. The six new items (PHASE_CONTEXT_MODELS documentation, reverse template check, mode schema templates validation, ROUND_SYNTHESES exclusion, P2-6 sub-items, and P3-5 scope resolution) are all substantive contributions that improve the spec's completeness.

**Would additional rounds have been productive?** No. The Round 2 synthesis shows zero architectural disputes, zero pending contradictions, and all agents applying the same governing principles to evaluate proposals. The marginal value of a third round -- given the pattern of decreasing dispute counts (4 -> 0) and increasing convergence stability -- would not justify the agent expenditure. The deliberation reached its natural conclusion.

---

*This cross-round synthesis was produced by a neutral synthesizer with no agenda. Every claim traces to a specific per-round synthesis. No new ideas were introduced. The trajectory -- from 4 disputes to full convergence -- demonstrates that the cooperative deliberation process achieved its purpose: a thoroughly vetted, unanimously endorsed set of spec changes.*
