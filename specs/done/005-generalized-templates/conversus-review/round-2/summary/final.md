# Round 2 Final Synthesis: Spec 005 -- Generalized Template Schema, Variables, and Linter

**Synthesizer**: neutral
**Spec**: `005-generalized-templates`
**Deliberation mode**: cooperative
**Agents**: functional-typing, game-engine-advocate, integration-architect
**Round**: 2 of 2 (Final)
**Date**: 2026-03-21

---

## 1. Process Summary

| Metric | Round 1 | Round 2 | Cumulative |
|--------|---------|---------|------------|
| Agents | 3 | 3 | 3 |
| Phase 1 reviews | 3 | 3 | 6 |
| Phase 2 cross-reviews | 6 | 6 | 12 |
| Phase 3 revisions | 3 | 3 | 6 |
| Phase 4 dispute filings | 3 | 3 | 6 |
| Total original recommendations (Round 1) | 29 | -- | 29 |
| New recommendations (Round 2) | -- | 13 (functional-typing: 2, game-engine-advocate: 4, integration-architect: 7) | 13 |
| Recommendations withdrawn (Round 2) | -- | 4 (functional-typing: 2, integration-architect: 1, game-engine-advocate: 1) | 4 |
| Recommendations revised (Round 2) | -- | 4 (integration-architect: 2, game-engine-advocate: 2) | 4 |
| Recommendations maintained (Round 2) | -- | 5 | 5 |
| Round 1 disputes resolved in synthesis | 4 | -- | 4 |
| Round 2 disputes remaining | -- | 0 architectural, 2 prioritization | 2 |
| Convergence items (Round 2) | 14 | 20 | 20 (superseding Round 1's 14) |
| Concessions (total across both rounds) | 17 | 4 additional | 21 |

The Round 2 deliberation confirmed the stability of the Round 1 synthesis. All four Round 1 dispute resolutions were accepted by all three agents without reversal. No Round 1 concession was reversed by any agent. The Round 2 process produced genuine corrections -- functional-typing withdrew two proposals (warning-only error type validation and the separate `ValidationContext` dataclass) after convergent criticism from both cross-reviewers, game-engine-advocate conceded two documentation items (docstring field-name prescription and `extra = "ignore"` on ModeSchema) after the same convergent pattern, and integration-architect withdrew one recommendation (SKILL.md `allowed-tools` for linter invocation) as scope inflation into spec 008.

The deliberation has achieved full convergence. The two remaining items requiring synthesizer resolution are prioritization/scoping decisions (reverse template check bundling with P2-1, and P3-5 scope relative to P1-4), not architectural disagreements.

---

## 2. Recommendation Scorecard

### Round 2 Recommendations (all agents)

| ID | Agent | Description | Round 2 Review | Cross-Review Result | Revision Disposition | Final Status |
|----|-------|-------------|----------------|---------------------|---------------------|--------------|
| FT-D2-Ref | functional-typing | Warning-only `@field_validator` for unknown error types | Proposed | Both cross-reviewers flag as pattern-inconsistent with mode validation | **Withdrawn** | Converged: strict rejection, unanimous |
| FT-MO-1 | functional-typing | Frozen `ValidationContext` dataclass for internal params | P2 | Both cross-reviewers flag dual-abstraction hazard | **Withdrawn** | Converged: derive from `ValidationConfig`, no parallel object |
| FT-MO-2 | functional-typing | `itertools.product` in test case generators | P3 | game-engine-advocate: dilutes signal; integration-architect: distinct from Round 1 withdrawal | **Maintained, deprioritized** | P3, minor readability |
| FT-OBA-2 | functional-typing | Clarify `condition` field relationship to P1-4 | Editorial | game-engine-advocate sharpens: P3-5 scope must be resolved | **Strengthened** | For synthesizer resolution |
| FT-NEW-1 | functional-typing | Systematic schema-type audit alongside P1-3 | P2 | integration-architect: implementation hygiene, not spec deliverable | **Reframed** | Implementation instruction, not deliverable |
| FT-NEW-2 | functional-typing | P3-5 scope resolution relative to P1-4 | Editorial | All three agents converge | **Maintained** | For synthesizer resolution |
| GE-R1 | game-engine-advocate | `ValidationConfig` docstring with specific field name | P2 | Both cross-reviewers flag as scope inflation in prose | **Conceded** → directional hint | Converged: "plugin-aware configuration fields" |
| GE-R2 | game-engine-advocate | `PHASE_CONTEXT_MODELS` in P2-6 extension contract | P2 | Both cross-reviewers agree on substance | **Maintained** | Converged: one sentence in P2-6 |
| GE-R3 | game-engine-advocate | `ModeSchema` field extensibility with `extra = "ignore"` | P3 | Both cross-reviewers flag as withdrawn GE-2 reappearing | **Revised** → reinforce `extra = "forbid"` | Converged: typed field additions only |
| GE-R4 | game-engine-advocate | Schema version compatibility deferral note | P3 | No objections | **Maintained** | Converged: defer to version 2.0 introduction |
| GE-NR-1 | game-engine-advocate | Specify error_type validator enforcement behavior | P2 | Converges with integration-architect New Rec B | **Maintained** | Converged: reject semantics, unanimous |
| GE-NR-2 | game-engine-advocate | Reverse template check bundled with P2-1 | P2 | functional-typing prefers P3 standalone | **Maintained** | Prioritization for synthesizer |
| GE-NR-3 | game-engine-advocate | P3-5 / P1-4 scope overlap flag | Documentation | Converges with FT-NEW-2 | **Maintained** | For synthesizer resolution |
| IA-Rec1 | integration-architect | SKILL.md `allowed-tools` for linter invocation | P2 | Both cross-reviewers flag as scope inflation into spec 008 | **Withdrawn** | Closed: spec 008 concern |
| IA-Rec2 | integration-architect | Reverse template existence check | P3 | game-engine-advocate: bundle with P2-1; functional-typing: P3 standalone | **Maintained** | Prioritization for synthesizer |
| IA-Rec3 | integration-architect | Fix `ROUND_SYNTHESES` comment in models.py | P3 | No objections | **Maintained** | Converged: P3 |
| IA-Rec4 | integration-architect | Document filename-phase constraint in P2-6 | P2-6 addendum | game-engine-advocate: remove prescription, keep constraint | **Modified** → descriptive only | Converged: constraint documented, no workaround prescribed |
| IA-Rec5 | integration-architect | Document `validate_templates` evolution path | P2-6 addendum | functional-typing: weaken backward-compat commitment; game-engine-advocate: YAGNI | **Modified** → observational only | Converged: no commitment, no shape |
| IA-RecA | integration-architect | Validate mode schema `templates` against phase names | P3 | Bridges Rec2 and Rec4; functional-typing endorses | **New** | Converged: P3 bridging validation |
| IA-RecB | integration-architect | Specify error_type validator rejects unknown types | P1-2 impl detail | Converges with GE-NR-1 | **New** | Converged: reject semantics, unanimous |

---

## 3. Dangerous Contradictions Found

### 3.1 Resolved in Round 2

**R6: Warning-only error type validation vs. mode validation pattern consistency**
- functional-typing proposed that the `@field_validator` on `LintError.error_type` should issue a warning for unknown types rather than reject.
- Both game-engine-advocate and integration-architect independently identified this as breaking pattern consistency with mode validation (which rejects unknown modes) and losing typo protection for error type strings.
- functional-typing's concern (plugins cannot return custom error types without pre-registration) was addressed by the established pattern: `KNOWN_ERROR_TYPES` is a `frozenset` constructed at module load time from a base set plus plugin-registered types. Unlike `Literal` (which requires source code changes), the runtime `frozenset` can be extended programmatically without redeployment.
- **Resolution**: functional-typing withdrew the warning-only proposal. All three agents converge on strict rejection semantics, matching the mode validation pattern. Source: functional-typing/revision.md (REC-2 withdrawal); game-engine-advocate/cross-reviews/functional-typing.md (DC-1); integration-architect/cross-reviews/functional-typing.md (DC-1).

**R7: `ValidationContext` dual-abstraction pattern**
- functional-typing proposed a frozen `ValidationContext` dataclass to bundle internal parameters for `validate_template`, distinct from the public `ValidationConfig` Pydantic model.
- Both game-engine-advocate and integration-architect independently identified the dual-abstraction hazard: two configuration objects with overlapping concerns in the same call chain creates "which config do I update?" maintenance bugs and requires cross-priority-tier coordination.
- game-engine-advocate proposed deriving internal state from `ValidationConfig` via a factory function instead.
- **Resolution**: functional-typing withdrew `ValidationContext`. The parameter-count concern is real but should be addressed through derivation from `ValidationConfig`, not a parallel abstraction. Source: functional-typing/revision.md (REC-5 withdrawal); game-engine-advocate/cross-reviews/functional-typing.md (DC-2); integration-architect/cross-reviews/functional-typing.md (DC-2).

**R8: `extra = "ignore"` on ModeSchema as withdrawn GE-2 reappearing**
- game-engine-advocate's R3 originally suggested `extra = "ignore"` on `ModeSchema` as one possible extension mechanism for handling unknown fields from downstream specs.
- Both integration-architect and functional-typing identified this as the withdrawn GE-2 argument (`extra = "allow"`) reappearing through documentation -- "through a side door," as integration-architect put it.
- **Resolution**: game-engine-advocate conceded and revised R3 to explicitly reinforce `extra = "forbid"`: "Downstream specs may add typed fields to `ModeSchema` by modifying the Pydantic model definition. The `extra = 'forbid'` constraint remains in effect; unknown fields in mode schema YAML files are validation errors, not silent extensions." Source: game-engine-advocate/revision.md (R3 revision); integration-architect/cross-reviews/game-engine-advocate.md (DC-2); functional-typing/cross-reviews/game-engine-advocate.md (T-2).

**R9: `ValidationConfig` docstring specificity as scope inflation**
- game-engine-advocate's R1 originally proposed embedding `known_plugin_variables: frozenset[str]` as the anticipated extension in the `ValidationConfig` docstring.
- Both functional-typing and integration-architect independently identified this as scope inflation in prose form -- encoding spec 007's design decisions into spec 005's documentation. functional-typing called it "composing before freezing." integration-architect called it "spec 005 reaching into spec 007's design space."
- **Resolution**: game-engine-advocate conceded and narrowed to a directional hint: "downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields." No field name, no type signature. Source: game-engine-advocate/revision.md (R1 concession); functional-typing/cross-reviews/game-engine-advocate.md (DC-2); integration-architect/cross-reviews/game-engine-advocate.md (DC-1).

**R10: SKILL.md `allowed-tools` as scope inflation into spec 008**
- integration-architect's Rec 1 proposed updating SKILL.md's `allowed-tools` frontmatter to permit `uv run python linter/validate.py`.
- functional-typing identified the architectural contradiction: Rec 1 simultaneously endorses the programmatic API (P1-2) as the canonical interface and then solves the invocation problem by shelling out to the CLI, meaning the primary consumer never exercises the decoupled property P1-2 was designed to achieve.
- game-engine-advocate added that P2-8 (`[project.scripts]` entry point) would change the invocation surface, making the spec note immediately stale.
- **Resolution**: integration-architect withdrew Rec 1. All three agents agree that the SKILL.md invocation pathway is a spec 008 (executable conversus) concern. Spec 005 delivers the library API. Source: integration-architect/revision.md (Rec 1 withdrawal); functional-typing/cross-reviews/integration-architect.md (DC-1); game-engine-advocate/cross-reviews/integration-architect.md (DC-1).

**R11: Prescriptive filename-phase documentation**
- integration-architect's Rec 4 originally prescribed that "variant templates for the same phase must use conditional blocks within a single template, not separate files."
- game-engine-advocate identified this as prescribing how future specs must handle a constraint -- the same scope-inflation pattern the Round 1 deliberation corrected in game-engine-advocate's own recommendations, but applied in reverse (prescribing a constraint on extensions rather than front-loading an extension mechanism).
- **Resolution**: integration-architect revised Rec 4 to document the constraint without prescribing the workaround. Agreed formulation: "Template filenames map 1:1 to phase names (`phase = tmpl_path.stem`). This is a load-bearing assumption in the linter. Downstream specs that need per-phase variants should be aware that introducing multiple template files for a single phase would require linter changes." Source: integration-architect/revision.md (Rec 4 modified); game-engine-advocate/cross-reviews/integration-architect.md (DC-2).

### 3.2 Unresolved Contradictions

None. All dangerous contradictions identified in both rounds have been resolved through concession, revision, or convergence.

---

## 4. Systemic Contradictions

### S1: Present correctness vs. future extensibility (from Round 1, reaffirmed in Round 2)

The "freeze first, compose later" principle, identified as the governing resolution of this tension in the Round 1 synthesis, was explicitly reaffirmed by all three agents in Round 2 and applied as the corrective lens for new scope-inflation instances. game-engine-advocate's A1 calls it "the governing principle for my Round 2 positions." functional-typing and integration-architect both apply it to evaluate each other's proposals. The principle was used to correct four Round 2 proposals: game-engine-advocate's R1 (docstring prescription), game-engine-advocate's R3 (`extra = "ignore"`), integration-architect's Rec 4 (prescriptive workaround), and integration-architect's Rec 5 (backward-compatibility commitment).

### S2: Scope inflation through documentation (new in Round 2)

Round 2 surfaced a subtler variant of the scope-inflation pattern identified in Round 1 (S2): agents whose code-level scope inflation was corrected in Round 1 attempted to encode the same assumptions in documentation instead. game-engine-advocate's R1 (encoding a specific field name in a docstring) and R3 (documenting `extra = "ignore"` as a possible mechanism) were both identified as the same impulse -- encoding spec 007 assumptions into spec 005 -- expressed through prose rather than code. integration-architect's Rec 4 (prescribing conditional blocks) and Rec 5 (committing to backward compatibility) exhibited the same pattern from a different direction: encoding design constraints on future specs rather than documenting current constraints for future specs.

The cross-review mechanism caught all four instances via convergent dual-reviewer identification. The corrective principle: documentation in a spec creates normative expectations for implementers. Spec text is instruction, not commentary. The same scope discipline that applies to code applies to prose.

### S3: Self-contradiction detection via cross-review (from Round 1, confirmed in Round 2)

The cross-review mechanism's effectiveness, first demonstrated in Round 1 (catching integration-architect's MODE_PRESENCE self-contradiction and linter-composition self-contradiction), was confirmed in Round 2. Every Round 2 withdrawal was prompted by convergent, independent criticism from both cross-reviewers. The pattern is reliable: when two independent reviewers identify the same flaw using different analytical lenses, the correction is almost certainly substantive rather than positional. This held for all six resolved contradictions in Round 2.

---

## 5. Convergence Achieved

The 20 convergence items below supersede the 14 from the Round 1 synthesis. Items 1-14 carry forward from Round 1 (some with Round 2 refinements noted). Items 15-20 are new convergence achieved in Round 2.

### Unanimous -- All Three Agents, Both Rounds

1. **Purify schema-loading functions (P1-1).** Replace `sys.exit(2)` and `click.echo()` in `load_variables_schema`, `load_mode_schema`, and `find_project_root` with `SchemaLoadError` exceptions. CLI `main()` is the sole site of `sys.exit()`. All three agents independently identify this as the single highest-leverage change. Reaffirmed in Round 2 without challenge.

2. **Extract programmatic validation API (P1-2).** Create `validate_all(config: ValidationConfig) -> ValidationResult` where `ValidationConfig` is a Pydantic model with `root: Path` and `mode: Optional[str] = None`. No `known_plugin_variables` parameter. Docstring notes: "Downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields." Fix bare imports as part of this work. The `ValidationConfig` model is the sole public configuration surface -- no parallel `ValidationContext` or `**kwargs`. Round 2 refinement: docstring uses directional hint, not field-name prescription.

3. **`PathList` custom type (P1-3).** Pydantic custom type storing `list[Path]` internally with `BeforeValidator` parsing newline-separated strings and custom serializer rendering back. Export from `models.py`. Apply to all path-list fields. When implementing, the implementer should verify each field's comment and type annotation against the corresponding schema declaration (see convergence item 18 for the ROUND_SYNTHESES exclusion).

4. **`config_conditions` with typed `ConfigCondition` model (P1-4).** `ConfigCondition(BaseModel)` with `field: str` and `value: str`. Validates `field` values against known config field names at schema-load time. Enables spec 006's `PRIOR_ARBITRATION_PATH`.

5. **Spec 006 variables in context models and schema (P1-5).** `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, and `ARBITRATION_RULINGS` added with typed patterns (`Path`, `PathList`).

6. **MODE_PRESENCE migrated to mode schema YAML declarations (P2-1).** Add `mode_in_phases` field to each mode schema YAML. Derive lookup via pure function at load time. Delete the hardcoded 28-entry dict. Round 2 refinement: the reverse template existence check (convergence item 16) may be bundled with this deliverable (see synthesizer resolution below).

7. **`VALID_MODES` as dynamic registry (P2-2).** Replace hardcoded frozenset with `get_valid_modes(schema_dir: Path) -> frozenset[str]` scanning `schema/modes/*.yml`.

8. **Structured `LintError` Pydantic model (P2-3).** `LintError(BaseModel)` with `error_type: str` validated against `KNOWN_ERROR_TYPES: frozenset[str]`. Round 2 refinement: the `@field_validator` **rejects** unknown error types at construction time (raises `ValueError`), matching the mode validation pattern. Plugin-contributed `check_*` functions register their error types into `KNOWN_ERROR_TYPES` at module initialization, before producing errors. The `frozenset` is constructed at load time from a base set plus any plugin-registered types. One validation pattern for all extensible sets.

9. **Schema versioning (P2-4).** Add `schema_version: "1.0.0"` to `variables.yml`. Must be done before spec 006 adds variables. Round 2 addendum: schema version compatibility validation (linter version X supports schema versions Y-Z) is deferred to the spec that introduces schema version 2.0.

10. **`frozen=True` on `TemplateContext` hierarchy (P2-5).** Apply to core `TemplateContext` and all subclasses. Plugin extensibility via composition (`PluginContext`), not by relaxing immutability.

11. **Extension contract documentation (P2-6).** Spec Section 6 gains a subsection documenting extension points and non-extension points. Round 2 substantially expanded this deliverable's scope with several sub-items (see 12-15 below).

12. **Mandate Python in spec Implementation Notes (P2-7).** "The linter MUST be a Python script following Constitution Principle IX."

13. **`pyproject.toml` packaging and entry point (P2-8).** `[project.scripts]` with `conversus-lint`. Packaging infrastructure follows once imports are clean.

14. **Schema evolution regression tests (P2-9).** Tests covering new optional variable, new required variable, new mode schema discovery.

### Converged in Round 2

15. **`PHASE_CONTEXT_MODELS` documented as extensible registry in P2-6.** One sentence: "The `PHASE_CONTEXT_MODELS` dict maps phase names to their context model classes and is designed to be extended by downstream specs adding new phases or phase variants. It is not `Final` by deliberation consensus." Prevents future regression of the FT-8 withdrawal. Source: game-engine-advocate R2, accepted by all.

16. **Reverse template existence check.** The linter should report template files on disk not listed in the mode schema's `templates` field. All three agents endorse the check. **Synthesizer resolution on priority**: Bundle with P2-1 as bidirectional template validation. game-engine-advocate's argument is persuasive: when P2-1 makes the `templates` list authoritative, validating in only one direction creates a window where the list is authoritative for one failure mode but not its symmetric counterpart. The scope expansion to P2-1 is modest (one additional loop over filesystem entries), and the two checks are logically a single concept: the `templates` list and the filesystem must agree. integration-architect accepts bundling; functional-typing accepts either outcome.

17. **Mode schema `templates` entries validated against known phase names (P3).** Each entry in the mode schema `templates` list must correspond to a recognized phase name. This bridges the reverse template check (16) and the filename-phase constraint (19) into a coherent three-part validation chain: (1) every template on disk must be declared in the schema, (2) every declaration must correspond to a recognized phase, (3) every recognized phase must have a template on disk. Source: integration-architect New Rec A, functional-typing endorses bridging logic.

18. **`ROUND_SYNTHESES` comment fix and PathList exclusion (P3).** The `CrossRoundSynthesisContext.ROUND_SYNTHESES` field comment changes from "newline-separated paths" to "pre-formatted synthesis content per round." This field must NOT be converted to `PathList` during P1-3, as it is `type: extracted-content` in the schema, not a path list. Source: integration-architect Rec 3, unanimously accepted.

19. **P2-6 sub-items: documentation convergences.** The following items are all addenda to the P2-6 extension contract documentation, agreed by all agents after Round 2 cross-review corrections:

    - **`ModeSchema` extensibility**: "Downstream specs may add typed fields to `ModeSchema` by modifying the Pydantic model definition. The `extra = 'forbid'` constraint remains in effect; unknown fields in mode schema YAML files are validation errors, not silent extensions." (game-engine-advocate R3 revised, unanimously accepted)

    - **Filename-phase constraint**: "Template filenames map 1:1 to phase names (`phase = tmpl_path.stem`). This is a load-bearing assumption in the linter. Downstream specs that need per-phase variants should be aware that introducing multiple template files for a single phase would require linter changes." (integration-architect Rec 4 revised, unanimously accepted)

    - **`validate_templates` evolution**: "The `validate_templates` field is boolean in v1. Granular validation control (per-mode, per-check-type) is a potential future concern but is not designed here." No backward-compatibility commitment, no shape suggestion. (integration-architect Rec 5 revised, unanimously accepted)

    - **`KNOWN_ERROR_TYPES` as extensible registry**: "The `KNOWN_ERROR_TYPES` frozenset is an extensible registry with strict validation. The set is constructed at module load time from a base set plus any plugin-registered types. The `@field_validator` rejects unregistered types at construction time. Plugins register their error types at initialization before any validation calls." (game-engine-advocate NR-1, integration-architect New Rec B, functional-typing convergence)

20. **P3-5 scope resolved relative to P1-4.** **Synthesizer resolution**: P3-5 ("formalize condition syntax") should be redefined as extending P1-4's `ConfigCondition` model with additional condition types beyond the initial `field`/`value` matching -- not as a separate grammar for the prose `condition` field in `variables.yml`. The rationale: the `condition` field in `variables.yml` is currently prose documentation that `validate.py` never reads. P1-4's `ConfigCondition` is the typed, machine-readable mechanism. Formalizing the prose field into a separate grammar would create a redundant parallel system with no identified consumer. Instead, P3-5 should add condition types (e.g., `rounds > 1` as `ConfigCondition(field="rounds", operator="gt", value="1")`) to the `ConfigCondition` model, extending the existing typed mechanism rather than inventing a new one. This makes P3-5 a P1-4 extension, and its priority should be updated accordingly: P3 for adding new condition types to `ConfigCondition` when the need arises (currently, the only condition expression in the schema is `rounds > 1`, which can be handled by extending `ConfigCondition` with an `operator` field). Source: functional-typing NEW-2, game-engine-advocate NR-3, all three agents converge.

---

## 6. Remaining Disputes

<!-- CONVERSUS:DISPUTES_BEGIN -->

### No Architectural Disputes Remain

The deliberation has achieved full convergence on all architectural and design questions. The four Round 1 disputes were resolved by the Round 1 synthesis, accepted by all three agents in Round 2 without reversal, and refined through Round 2 cross-review. The Round 2 process produced no new architectural disputes.

Two minor prioritization/scoping questions were resolved by synthesizer discretion in Section 5:

1. **Reverse template check priority (P2-1 bundling vs. P3 standalone)**: Resolved in convergence item 16 -- bundled with P2-1 as bidirectional template validation.

2. **P3-5 scope relative to P1-4**: Resolved in convergence item 20 -- P3-5 is redefined as an extension of P1-4's `ConfigCondition` model with additional condition types.

Neither of these involved disagreement on whether the work should be done -- only on when and how it should be packaged.

<!-- CONVERSUS:DISPUTES_END -->

---

## 7. Actionable Spec Changes

### P1 -- Must be addressed before spec 005 can be considered complete

**P1-1: Purify schema-loading functions**
- Replace `sys.exit(2)` and `click.echo()` in `load_variables_schema`, `load_mode_schema`, and `find_project_root` with `SchemaLoadError` exceptions.
- CLI `main()` catches `SchemaLoadError` and calls `sys.exit(2)`.
- Affects: `linter/validate.py`
- Source: Round 1 FT-1 (unanimous). Reaffirmed Round 2 by all three agents as highest-leverage change.

**P1-2: Extract programmatic validation API**
- Create `validate_all(config: ValidationConfig) -> ValidationResult` where `ValidationConfig` is a Pydantic model with `root: Path` and `mode: Optional[str] = None`.
- `ValidationResult` is a Pydantic model with `errors: list[LintError]`, `files_checked: int`, `passed: bool`.
- Fix bare imports (`from models import ...` -> `from .models import ...`) as part of this work.
- Click CLI `main()` becomes a thin wrapper calling `validate_all()`.
- `ValidationConfig` docstring: "Downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields."
- `ValidationConfig` is the sole public configuration surface. No parallel `ValidationContext`, no `**kwargs`, no pre-emptive plugin parameters.
- Affects: `linter/validate.py`, `linter/__init__.py`
- Source: Round 1 IA-2, FT-1 (prerequisite), GE-N2 (import fix). Round 2 refinements: docstring phrasing (all agents converge), no parallel config object (functional-typing withdrawal).

**P1-3: Define `PathList` custom type**
- Create `PathList` custom Pydantic type: `list[Path]` internally, `BeforeValidator` for newline-separated string parsing, custom serializer for template substitution.
- Export from `models.py` as a reusable type.
- Apply to all path-list fields. Explicitly EXCLUDE `ROUND_SYNTHESES` (which is `type: extracted-content`, not `path-list`).
- Implementation instruction: when examining each field for PathList conversion, verify the field's comment and type annotation against the corresponding `variables.yml` schema declaration. The `ROUND_SYNTHESES` drift indicates broader correspondence issues may exist.
- Affects: `linter/models.py`, `schema/variables.yml` (documentation)
- Source: Round 1 FT-2 (modified), IA cross-review (serializer design). Round 2: ROUND_SYNTHESES exclusion (integration-architect Rec 3, unanimous).

**P1-4: Add `config_conditions` field with typed `ConfigCondition` model**
- `ConfigCondition(BaseModel)` with `field: str` and `value: str`.
- Add `config_conditions: Optional[list[ConfigCondition]] = None` to `VariableDefinition`.
- Validate `field` values against known config field names at schema-load time.
- Enables spec 006's `PRIOR_ARBITRATION_PATH` (conditioned on `arbiter.timing: inter-round`).
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: Round 1 IA-1 (modified per FT refinement). Round 2: P3-5 resolved as future extension of this model (convergence item 20).

**P1-5: Add spec 006 variables to context models and schema**
- Add `PRIOR_ARBITRATION_PATH: Optional[Path] = None` to `ReviewContext`, `CrossReviewContext`, `RevisionContext`, `DisputesContext`, `SynthesisContext`.
- Add `ARBITRATION_PATHS` (using `PathList` type) to `CrossRoundSynthesisContext`.
- Add `ARBITRATION_RULINGS: Optional[str] = None` to `CrossRoundSynthesisContext`.
- Add corresponding entries in `schema/variables.yml` with appropriate `config_conditions`.
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: Round 1 IA-3, IA-4.

### P2 -- Should be addressed in spec 005's scope

**P2-1: Move MODE_PRESENCE to mode schema YAML declarations with bidirectional template validation**
- Add `mode_in_phases` field to each mode schema YAML.
- Derive lookup table via pure function at load time.
- Delete the hardcoded 28-entry `MODE_PRESENCE` dict in `validate.py`.
- Add reverse template existence check: iterate `templates/{mode}/*.md` and report any template file not declared in the mode schema's `templates` list.
- Bidirectional validation as a single deliverable: templates listed but not on disk (existing check) and templates on disk but not listed (reverse check).
- Affects: `schema/modes/*.yml`, `linter/validate.py`, `linter/models.py` (ModeSchema model)
- Source: Round 1 FT-5, GE-6, IA-7 (unanimous). Round 2: reverse check bundled (game-engine-advocate NR-2, accepted by integration-architect and functional-typing).

**P2-2: Make `VALID_MODES` a dynamic registry**
- Replace `VALID_MODES = frozenset({...})` with `get_valid_modes(schema_dir: Path) -> frozenset[str]` scanning `schema/modes/*.yml`.
- Update `ModeSchema.validate_mode` to use the dynamic set.
- Affects: `linter/models.py`, `linter/validate.py`
- Source: Round 1 GE-3 (P2), IA cross-review.

**P2-3: Structured `LintError` Pydantic model with strict error type validation**
- `LintError(BaseModel)` with fields: `error_type: str`, `file_path: str`, `variable_name: Optional[str]`, `phase: str`, `mode: str`, `message: str`, `suggestion: Optional[str]`.
- `KNOWN_ERROR_TYPES: frozenset[str]` containing `{"missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"}`.
- `@field_validator` on `error_type` raises `ValueError` for types not in `KNOWN_ERROR_TYPES`. Plugins register their types before producing errors.
- `KNOWN_ERROR_TYPES` is constructed at module load time from a base set plus any plugin-registered types.
- All `check_*` functions return `list[LintError]`.
- CLI `main()` formats `LintError` objects for human display.
- Affects: `linter/validate.py`, `linter/models.py`
- Source: Round 1 IA-8, FT-A. Round 2: enforcement behavior specified as strict rejection (game-engine-advocate NR-1, integration-architect New Rec B, functional-typing concedes warning-only proposal).

**P2-4: Schema versioning**
- Add `schema_version: "1.0.0"` to `variables.yml` top level.
- Add `schema_version` field to `VariablesSchema` Pydantic model.
- The linter reports the schema version in its output.
- Must be done before spec 006 adds its variables.
- Schema version compatibility validation (linter version X supports schema versions Y-Z) is deferred to the spec that introduces schema version 2.0.
- Affects: `schema/variables.yml`, `linter/models.py`
- Source: Round 1 GE-5, IA-9. Round 2: deferral note (game-engine-advocate R4).

**P2-5: Apply `frozen=True` to `TemplateContext` hierarchy**
- Change `model_config` to include `"frozen": True` on `TemplateContext` and all subclasses.
- Add code comment: plugin-contributed data flows through a separate `PluginContext` model, designed in spec 007.
- Affects: `linter/models.py`
- Source: Round 1 FT-4.

**P2-6: Document extension contracts in spec 005**
- Add a section to spec Section 6 (Implementation Notes) titled "Extension Points for Downstream Specs" documenting:
  - **Extension points**: new variables via `schema/variables.yml` addition, new modes via `schema/modes/{mode}.yml` creation, new config conditions via `ConfigCondition`, plugin-contributed data via parallel composition (spec 007), `PHASE_CONTEXT_MODELS` as an extensible registry for new phase-to-model mappings, `ModeSchema` accepts new typed fields via model definition modification, `KNOWN_ERROR_TYPES` as an extensible registry with strict validation (register before produce).
  - **NOT extension points**: `extra = "forbid"` on all core Pydantic models (TemplateContext, ModeSchema, etc.), template syntax `{VARIABLE}`, structural marker syntax, template filename-to-phase-name 1:1 mapping (`phase = tmpl_path.stem` -- downstream specs needing per-phase variants must be aware this requires linter changes).
  - **Observations (not commitments)**: `validate_templates` is boolean in v1; granular validation control is a potential future concern but is not designed here.
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 GE-9. Round 2 sub-items: PHASE_CONTEXT_MODELS (game-engine-advocate R2), ModeSchema extensibility (game-engine-advocate R3 revised), filename-phase constraint (integration-architect Rec 4 revised), validate_templates evolution (integration-architect Rec 5 revised), KNOWN_ERROR_TYPES (game-engine-advocate NR-1, integration-architect New Rec B).

**P2-7: Mandate Python in spec Implementation Notes**
- Change spec Section 6 from "Python or shell" to "The linter MUST be a Python script following Constitution Principle IX."
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 FT-6.

**P2-8: `pyproject.toml` packaging and entry point**
- Add package discovery and `[project.scripts]` with `conversus-lint = "conversus.linter.validate:main"`.
- Affects: `pyproject.toml`
- Source: Round 1 IA-5.

**P2-9: Schema evolution regression tests**
- Tests covering: adding a new optional variable passes all existing templates, adding a new required variable for a specific phase produces errors only for that phase's templates, adding a new mode schema file is discovered and validated.
- Affects: `linter/test_validate.py`
- Source: Round 1 IA-6.

### P3 -- Should be addressed, low urgency

**P3-1: Document `required: True` default in spec**
- Add to spec Section 3: "Variables default to `required: true` when the field is omitted."
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 FT-9.

**P3-2: Fix `AGENT_DOCS` type discrepancy in spec**
- Update spec Section 3 to show `AGENT_DOCS` as `type: extracted-content` instead of `type: path-list`.
- Affects: `specs/005-generalized-templates/spec.md`
- Source: Round 1 IA-10.

**P3-3: Document core-variable vs. plugin-variable namespace rule**
- Comment in `schema/variables.yml` header: "Variables in this file carry data produced by the core orchestrator or provided by user config. Variables produced by plugins are namespaced separately (mechanism defined by spec 007)."
- Affects: `schema/variables.yml`
- Source: Round 1 IA-N3.

**P3-4: Make `VALID_PHASES` extensible**
- Derive from schema data or `PHASE_CONTEXT_MODELS` keys.
- Lower urgency than `VALID_MODES` because no spec currently adds new phases.
- Affects: `linter/models.py`
- Source: Round 1 GE-8.

**P3-5: Extend `ConfigCondition` with additional condition types**
- Redefined scope (Round 2 resolution): P3-5 extends P1-4's `ConfigCondition` model with additional condition types beyond simple `field`/`value` matching. The initial extension would add an `operator` field to `ConfigCondition` to express conditions like `rounds > 1`. This is a P1-4 extension, not a separate grammar for the prose `condition` field in `variables.yml`.
- The prose `condition` field in `variables.yml` remains documentary. It is not parsed by `validate.py`. `ConfigCondition` is the machine-readable mechanism.
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: Round 1 GE-N3. Round 2 scope resolution: functional-typing NEW-2, game-engine-advocate NR-3, unanimously converged.

**P3-6: Fix `ROUND_SYNTHESES` comment in models.py**
- Change the `CrossRoundSynthesisContext.ROUND_SYNTHESES` comment from "newline-separated paths" to "pre-formatted synthesis content per round."
- Ensure this field is NOT included in P1-3 PathList conversion batch.
- Affects: `linter/models.py`
- Source: Round 2 integration-architect Rec 3, unanimously accepted.

**P3-7: Validate mode schema `templates` entries against known phase names**
- Each entry in the mode schema `templates` list must correspond to a recognized phase name.
- Bridges the reverse template check (P2-1) and the filename-phase constraint (P2-6) into a three-part validation chain.
- Affects: `linter/validate.py`
- Source: Round 2 integration-architect New Rec A, functional-typing endorses.

**P3-8: Use `itertools.product` in test case generators**
- Where `itertools.product` improves readability over nested list comprehensions in test case generation, apply it.
- Minor readability improvement consistent with Constitution Principle IX's FP guidance.
- Affects: `linter/test_validate.py`
- Source: Round 2 functional-typing MO-2, maintained at P3, deprioritized.

### Deferred -- Explicitly out of spec 005 scope

**D1: Plugin variable namespace** -- Deferred to spec 007 Phase 1. Source: GE-1.
**D2: `PluginContext` composition architecture** -- Deferred to spec 007 Phase 1. Source: GE-2.
**D3: ModeSchema `extensions` section** -- Deferred to spec 007 Phase 1. Source: GE-7.
**D4: `float`/`number` variable type** -- Deferred to the spec that first needs it. Source: GE-4.
**D5: `__all__` exports on `models.py`** -- Deferred to post-spec-007-Phase-1. Source: FT-7.
**D6: Reserve `schema/objectives/` directory** -- Deferred to spec 007. Source: GE-10.
**D7: SKILL.md linter invocation pathway** -- Deferred to spec 008 (executable conversus). Source: Round 2 integration-architect Rec 1 (withdrawn).

---

## 8. Key Concessions (Per Agent)

### functional-typing

**Round 1 concessions (all maintained through Round 2):**
1. Withdrew `Literal` types for modes and variable types (FT-3) -- `Literal` conflicts with SC-003 extensibility.
2. Withdrew `Final` on `PHASE_CONTEXT_MODELS` (FT-8) -- it is a registry, not a constant.
3. Modified `MODE_PRESENCE` derivation approach (FT-5) -- adopted YAML approach.
4. Withdrew `itertools.chain` optimization -- structured error models make it irrelevant.
5. Deferred `__all__` exports (FT-7) -- premature before plugin interface is known.

**Round 2 concessions:**
6. Withdrew warning-only `@field_validator` on `error_type` -- both cross-reviewers identified it as breaking pattern consistency with mode validation and losing typo protection. The `frozenset` extended at load time resolves plugin extensibility without weakening validation.
7. Withdrew separate `ValidationContext` frozen dataclass -- both cross-reviewers identified the dual-abstraction maintenance hazard. Parameter-count concerns addressed by derivation from `ValidationConfig`.

### game-engine-advocate

**Round 1 concessions (all maintained through Round 2):**
1. Deferred 5 recommendations to spec 007 (GE-1, GE-2, GE-7, GE-10, GE-4) -- 7 of 10 original recommendations were scope inflation.
2. Withdrew `extra = "allow"` on TemplateContext (GE-2) -- composition pattern is architecturally superior.
3. Withdrew template-scanning for MODE_PRESENCE (GE-6) -- creates circular validation.
4. Withdrew float/number type (GE-4) -- premature abstraction.
5. Downgraded `VALID_MODES` from P1 to P2 (GE-3).

**Round 2 concessions:**
6. Conceded R1 docstring field-name prescription -- narrowed from `known_plugin_variables: frozenset[str]` to directional hint "plugin-aware configuration fields." Both cross-reviewers identified specific field-name prescription as scope inflation in prose form.
7. Revised R3 to withdraw `extra = "ignore"` suggestion on ModeSchema -- both cross-reviewers identified it as the withdrawn GE-2 argument reappearing. Revised to reinforce `extra = "forbid"`.

### integration-architect

**Round 1 concessions (all maintained through Round 2):**
1. Retracted MODE_PRESENCE Alignment endorsement (IA-N1) -- acknowledged internal contradiction.
2. Retracted characterization of schema-loading functions as "pure" (IA-N2) -- `sys.exit()` makes them impure.
3. Replaced `dict[str, str]` with typed `ConfigCondition` model (IA-1).
4. Withdrew `plugin_data: dict[str, Any]` (IA-N4) -- composition model is architecturally superior.
5. Upgraded schema versioning from P3 to P2 (IA-9).

**Round 2 concessions:**
6. Withdrew Rec 1 (SKILL.md `allowed-tools` for linter invocation) -- both cross-reviewers identified it as scope inflation into spec 008. The programmatic API's purpose is to decouple from CLI invocation; recommending CLI shell-out contradicts that purpose.
7. Modified Rec 4 to remove prescriptive workaround (conditional blocks mandate) -- game-engine-advocate identified this as prescribing future spec design, violating "freeze first, compose later."
8. Modified Rec 5 to remove backward-compatibility commitment for `validate_templates` boolean form -- functional-typing identified this as constraining spec 007's design space prematurely.

---

*This synthesis was produced by a neutral synthesizer with no agenda. Every claim traces to a specific artifact in the deliberation record. No new ideas were introduced. The deliberation achieved full convergence across two rounds. No architectural disputes remain.*
