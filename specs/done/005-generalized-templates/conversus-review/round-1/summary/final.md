# Neutral Synthesis: Spec 005 -- Generalized Template Schema, Variables, and Linter

**Synthesizer**: neutral
**Spec**: `005-generalized-templates`
**Deliberation mode**: cooperative
**Agents**: functional-typing, game-engine-advocate, integration-architect
**Date**: 2026-03-21

---

## 1. Process Summary

| Metric | Count |
|--------|-------|
| Agents | 3 |
| Phase 1 reviews | 3 |
| Phase 2 cross-reviews | 6 |
| Phase 3 revisions | 3 |
| Phase 4 dispute filings | 3 |
| Total original recommendations | 29 (functional-typing: 9, game-engine-advocate: 10, integration-architect: 10) |
| Recommendations maintained | 12 |
| Recommendations modified | 8 |
| Recommendations withdrawn | 5 |
| Recommendations deferred to downstream specs | 4 |
| New recommendations (arising from cross-review) | 8 (functional-typing: 3, game-engine-advocate: 3, integration-architect: 4) |
| Final disputes (Phase 4) | 4 active disputes (across 3 agents) |
| Full convergence items | 14 |
| Two-of-three convergence items | 4 |

The deliberation exhibited substantial intellectual movement. game-engine-advocate made the largest positional shift, conceding 7 of 10 original recommendations as scope inflation (spec 007 concerns dressed as spec 005 feedback). functional-typing withdrew 2 recommendations and modified 3 after persuasive cross-review arguments. integration-architect retracted 2 self-contradictions identified by cross-reviewers (MODE_PRESENCE endorsement/critique, impure functions labeled as pure).

---

## 2. Recommendation Scorecard

Each row traces a recommendation from its origin through all four phases.

### functional-typing Recommendations

| ID | Description | P1 Priority | P2 Cross-Review Response | P3 Disposition | P4 Final Status |
|----|-------------|-------------|--------------------------|----------------|-----------------|
| FT-1 | Purify schema-loading functions (replace `sys.exit()` with `SchemaLoadError`) | P1 | Unanimous agreement; integration-architect adopts as prerequisite for own Rec 2 | MAINTAINED at P1 | **Converged (unanimous P1)** |
| FT-2 | Replace raw `str` path-list fields with `list[Path]` / `PathList` type | P1 | integration-architect proposes `PathList` with serializer; game-engine-advocate agrees, requests export | MAINTAINED with `PathList` serializer modification | **Converged (P1)** |
| FT-3 | Use `Literal` types for mode and variable type enums | P2 | game-engine-advocate: conflicts with SC-003 extensibility; integration-architect: Literal for modes only | WITHDRAWN (both modes and types) | **Converged (unanimous withdrawal)** |
| FT-4 | Make `TemplateContext` models `frozen=True` | P2 | game-engine-advocate: conflicts with plugin extensibility; integration-architect: accept, enforces construction discipline | MAINTAINED with scope qualification (core models only) | **Converged (functional-typing + integration-architect; game-engine-advocate concedes for core)** |
| FT-5 | Derive `MODE_PRESENCE` from schema data | P2 | integration-architect: condition field not machine-parseable; game-engine-advocate: mode schemas preferred location | MODIFIED to mode schema YAML approach | **Converged (unanimous P2)** |
| FT-6 | Mandate Python in spec Implementation Notes | P2 | Unanimous implicit agreement | MAINTAINED | **Converged (unanimous P2)** |
| FT-7 | Add `__all__` exports to `models.py` | P3 | game-engine-advocate: premature API lockdown before spec 007 | DEFERRED | **Deferred to post-spec-007-Phase-1** |
| FT-8 | Type `PHASE_CONTEXT_MODELS` as `Final` | P3 | game-engine-advocate: this is a registry, not a constant | WITHDRAWN | **Converged (unanimous withdrawal)** |
| FT-9 | Document `required: True` default in spec | P3 | Unanimous agreement | MAINTAINED | **Converged (unanimous P3)** |
| FT-A | Structured `LintError` Pydantic model for error returns | -- | New in P3 (adopted from integration-architect Rec 8) | NEW at P2 | **Converged (unanimous P2, minor dispute on `error_type` typing)** |
| FT-B | Ensure spec 006 fields use typed patterns | -- | New in P3 (coordination recommendation) | NEW at P2 | **Converged (functional-typing + integration-architect)** |
| FT-C | Fix `AGENT_DOCS` type discrepancy in spec | -- | New in P3 (adopted from integration-architect Rec 10) | NEW at P3 | **Converged (unanimous P3)** |

### game-engine-advocate Recommendations

| ID | Description | P1 Priority | P2 Cross-Review Response | P3 Disposition | P4 Final Status |
|----|-------------|-------------|--------------------------|----------------|-----------------|
| GE-1 | Add plugin variable namespace to schema | P1 | integration-architect: competes with config_condition; functional-typing: speculative | DEFERRED to spec 007 | **Deferred** |
| GE-2 | Create extensible TemplateContext variant (`extra = "allow"`) | P1 | functional-typing: violates Principle IX; integration-architect: explicit fields instead | MODIFIED: narrow to documentation; defer impl to spec 007 | **Converged (unanimous: no `extra = "allow"` on core models)** |
| GE-3 | Make VALID_MODES a registry, not frozen set | P1 | integration-architect: downgrade to P2, spec 005 self-consistency fix | MODIFIED to P2, file-scanning approach | **Converged (P2)** |
| GE-4 | Add float/number variable type | P2 | integration-architect: premature abstraction; no current need | WITHDRAWN | **Withdrawn** |
| GE-5 | Add schema version field | P2 | integration-architect: P3; functional-typing: defer | MAINTAINED at P2, re-justified by spec 006 evolution | **Converged (integration-architect + game-engine-advocate at P2; functional-typing accepts P2-P3)** |
| GE-6 | Derive MODE_PRESENCE from schema | P2 | integration-architect: template scanning harmful; functional-typing: YAML approach | MODIFIED: adopt YAML declaration, reject template scanning | **Converged (unanimous P2)** |
| GE-7 | Add extensions section to ModeSchema | P2 | integration-architect: no use case before spec 007 | DEFERRED to spec 007 | **Deferred** |
| GE-8 | Make VALID_PHASES extensible | P3 | No direct challenge | MAINTAINED at P3 | **Retained at P3** |
| GE-9 | Document extension contract in spec 005 | P3 | integration-architect: supports; functional-typing: no objection | ELEVATED to P2 | **Converged (P2)** |
| GE-10 | Reserve `schema/objectives/` directory | P3 | Not addressed by cross-reviewers | WITHDRAWN | **Withdrawn** |
| GE-N1 | Programmatic API with `known_plugin_variables` parameter | -- | New in P3 | NEW at P1 | **Disputed (game-engine-advocate vs. integration-architect + functional-typing)** |
| GE-N2 | Fix bare imports for package importability | -- | New in P3 | NEW at P2 | **Converged (P2; game-engine-advocate argues P1 as prerequisite)** |
| GE-N3 | Formalize condition field syntax | -- | New in P3 | NEW at P3 | **Retained at P3** |

### integration-architect Recommendations

| ID | Description | P1 Priority | P2 Cross-Review Response | P3 Disposition | P4 Final Status |
|----|-------------|-------------|--------------------------|----------------|-----------------|
| IA-1 | Add `config_conditions` field to VariableDefinition | P1 | functional-typing: refine typing from `dict[str,str]` to `ConfigCondition` model; game-engine-advocate: also need `provided_by` axis | MODIFIED: typed `ConfigCondition` model; defer plugin axis to spec 007 | **Converged (P1, functional-typing + integration-architect; game-engine-advocate defers)** |
| IA-2 | Extract programmatic validation API from CLI | P1 | functional-typing: prerequisite is purifying loaders; game-engine-advocate: needs plugin-variables param | MODIFIED: expand scope to include loader purification | **Converged on existence (P1); disputed on parameter design** |
| IA-3 | Add `PRIOR_ARBITRATION_PATH` to Phase 1-5 models, `ARBITRATION_PATHS` to CrossRoundSynthesis | P1 | functional-typing: use typed patterns, not `Optional[str]` | MODIFIED: use `Path`/`PathList` types | **Converged (P1)** |
| IA-4 | Add `ARBITRATION_RULINGS` variable | P1 | game-engine-advocate: valid but establish core/plugin namespace rule | RETAINED at P1 | **Converged (P1, with namespace documentation)** |
| IA-5 | Add `[project.scripts]` entry point to pyproject.toml | P2 | functional-typing: bare imports are latent bug; game-engine-advocate: needs package-relative imports | MODIFIED: expand to include import path fixes | **Converged (P2)** |
| IA-6 | Add schema evolution regression tests | P2 | No challenges | RETAINED at P2 | **Converged (P2)** |
| IA-7 | Document MODE_PRESENCE in mode schema YAML | P2 | functional-typing: agrees after retracting own approach; game-engine-advocate: agrees after retracting template scanning | MODIFIED: retract contradictory Alignment endorsement | **Converged (unanimous P2)** |
| IA-8 | Structured error objects instead of `list[str]` | P2 | functional-typing: adopts as New Rec A; game-engine-advocate: error_type should be `str` not `Literal` | MODIFIED: retain `Literal` for error_type | **Converged on model (unanimous); disputed on `error_type` field type** |
| IA-9 | Add schema version field | P3 | game-engine-advocate: P2 justified by spec 006 timing | UPGRADED to P2 | **Converged (P2)** |
| IA-10 | Fix `AGENT_DOCS` type discrepancy | P3 | No challenges | RETAINED at P3 | **Converged (unanimous P3)** |
| IA-N1 | Retract MODE_PRESENCE Alignment endorsement | -- | New in P3 (editorial self-correction) | Editorial | **Resolved** |
| IA-N2 | Retract Alignment characterization of loaders as "pure" | -- | New in P3 (editorial self-correction) | Editorial | **Resolved** |
| IA-N3 | Document core-variable vs. plugin-variable namespace rule | -- | New in P3 | NEW at P3 | **Retained at P3** |
| IA-N4 | Add `plugin_data: dict[str, Any]` to TemplateContext | -- | New in P3 | NEW at P2 | **integration-architect concedes in Phase 4; withdrawn** |

---

## 3. Dangerous Contradictions Found

### 3.1 Resolved Contradictions

**R1: `Literal` types vs. registry extensibility**
- functional-typing (FT-3) proposed `Literal` for mode and variable type enums for static type checking.
- game-engine-advocate (GE-3) proposed dynamic registry scanning `schema/modes/*.yml`.
- These are mutually exclusive: `Literal` is a compile-time closed set; dynamic scanning is runtime-open.
- **Resolution**: functional-typing withdrew FT-3 entirely in Phase 3, accepting that spec 005's own SC-003 (adding "auction" mode via YAML alone) requires runtime-open validation. The `@field_validator` pattern with dynamically constructed sets is the unanimous approach.
- Source: functional-typing/revision.md (Rec 3 disposition); game-engine-advocate/cross-reviews/functional-typing.md (Dangerous Contradiction #2).

**R2: `extra = "forbid"` as safety net vs. extensibility blocker**
- integration-architect defended `extra = "forbid"` as essential safety for typo catching.
- game-engine-advocate proposed `extra = "allow"` on a plugin-aware variant.
- functional-typing proposed adding `frozen=True` (further tightening).
- **Resolution**: game-engine-advocate withdrew `extra = "allow"` in Phase 3. All three converge on: `extra = "forbid"` and `frozen=True` on core models; plugin data flows through a separate `PluginContext` composition mechanism designed in spec 007. integration-architect also withdrew `plugin_data: dict[str, Any]` in Phase 4 after functional-typing and game-engine-advocate both identified it as a Principle IX violation.
- Source: game-engine-advocate/revision.md (Rec 2 disposition); integration-architect/disputes.md (Dispute 1 concession).

**R3: MODE_PRESENCE -- three conflicting derivation proposals**
- functional-typing: derive from `variables.yml` condition field via pure function.
- game-engine-advocate: scan templates at linter initialization.
- integration-architect: self-contradicted (endorsed hardcoded table in Alignment, criticized it in Rec 7).
- **Resolution**: All three converge on mode schema YAML declarations. functional-typing conceded the condition field is not machine-parseable. game-engine-advocate conceded template scanning creates circular validation. integration-architect retracted the Alignment endorsement.
- Source: functional-typing/revision.md (Rec 5 disposition); game-engine-advocate/revision.md (Rec 6 disposition); integration-architect/revision.md (N1 retraction).

**R4: `list[str]` praised as composable vs. criticized as untyped**
- integration-architect praised `list[str]` returns as "well-structured" (Alignment) but then proposed replacing them with Pydantic models (Rec 8).
- functional-typing proposed `itertools.chain.from_iterable` optimization of `list[str]`.
- **Resolution**: All three agree `list[str]` is the wrong error representation. functional-typing withdrew the `itertools.chain` suggestion and adopted integration-architect's structured error model recommendation. The Alignment characterization was an overstatement that integration-architect acknowledged in Phase 3 (N2).
- Source: functional-typing/revision.md (New Rec A); integration-architect/revision.md (N2).

**R5: `plugin_data: dict[str, Any]` vs. typed composition**
- integration-architect (N4) proposed `plugin_data: dict[str, Any]` on TemplateContext.
- functional-typing rejected it as a Principle IX violation (`Any` prohibition).
- game-engine-advocate rejected it, endorsing functional-typing's composition pattern.
- **Resolution**: integration-architect conceded in Phase 4 disputes, withdrawing the proposal. Composition model (separate `PluginContext`) is the unanimous approach.
- Source: integration-architect/disputes.md (Dispute 1 concession).

### 3.2 Unresolved Contradictions

**U1: Programmatic API parameter design**
See Remaining Disputes, Dispute 1.

**U2: `ValidationError.error_type` -- `Literal` vs. `str`**
See Remaining Disputes, Dispute 2.

---

## 4. Systemic Contradictions

### S1: Present correctness vs. future extensibility

The deepest structural pattern in this deliberation is the tension between making the current system maximally correct (functional-typing's immutability and type safety mandates) and making it extensible for downstream specs (game-engine-advocate's plugin architecture needs). This manifested in every major dispute: `Literal` vs. dynamic validation, `frozen=True` vs. mutable extension points, `Final` vs. extensible registry, `extra = "forbid"` vs. `extra = "allow"`.

The deliberation resolved this systematically: spec 005 optimizes for correctness of the current system; spec 007 designs extension mechanisms with full knowledge of the frozen foundation. The principle is: freeze first, compose later. This was not the starting position of any agent -- it emerged through the cross-review process.

### S2: Scope discipline for foundation specs

game-engine-advocate's admission that 7 of 10 original recommendations were scope inflation reveals a systemic risk in multi-spec review: agents reviewing a foundation spec through the lens of their downstream dependency are biased toward front-loading extension points. The deliberation process itself corrected this, but the initial recommendation set was 70% out of scope for game-engine-advocate. integration-architect's recommendations were better scoped (8 of 10 addressed spec 005 or the immediate downstream spec 006), and functional-typing's were entirely in scope.

### S3: Self-contradiction in single reviews

integration-architect's review contained two internal contradictions (MODE_PRESENCE endorsed in Alignment, criticized in Rec 7; linter composition praised as "well-structured" while error returns criticized as untyped). Both were identified by functional-typing's cross-review and retracted by integration-architect in Phase 3. This suggests a pattern: Alignment sections, written to identify strengths, can inadvertently endorse patterns that the same reviewer's recommendations section proposes to change.

---

## 5. Convergence Achieved

Items are ordered by convergence strength (unanimous first, then two-of-three) and within that by priority.

### Unanimous Convergence (all three agents)

1. **Purify schema-loading functions**: Replace `sys.exit(2)` and `click.echo()` in `load_variables_schema`, `load_mode_schema`, and `find_project_root` with `SchemaLoadError` exceptions. CLI `main()` is the sole site of `sys.exit()`. Priority: P1. Source: FT-1 (identified), IA-2 (consequence for API), GE cross-review (downstream need).

2. **Extract programmatic validation API**: Create `validate_all()` returning structured `ValidationResult`, decoupled from Click CLI. Priority: P1. Source: IA-2, all three revisions. (Parameter design disputed; existence unanimous.)

3. **Structured error model**: Replace `list[str]` returns from `check_*` functions with a Pydantic `LintError`/`ValidationError` model. Priority: P2. Source: IA-8, FT-A, GE convergence 6. (The `error_type` field's type is disputed; the model itself is unanimous.)

4. **MODE_PRESENCE as mode schema YAML declarations**: Delete the hardcoded 28-entry dict in `validate.py` L108-144. Add `mode_in_phases` field to each mode schema YAML. Derive lookup via pure function at load time. Priority: P2. Source: FT-5 (modified), GE-6 (modified), IA-7 (modified).

5. **No `Literal` types for modes or variable types**: The `@field_validator` pattern with dynamically constructed valid sets is correct. `Literal` conflicts with SC-003's YAML-only mode addition story. Priority: N/A (withdrawal). Source: FT-3 (withdrawn), GE-3 (confirmed), IA cross-review (agreed).

6. **No `PHASE_CONTEXT_MODELS` as `Final`**: This is a registry that spec 007 needs to extend, not an immutable constant. Priority: N/A (withdrawal). Source: FT-8 (withdrawn), GE (confirmed), IA (implicit agreement).

7. **Mandate Python in spec Implementation Notes**: Spec Section 6 should say "Python script following Constitution Principle IX," not "Python or shell." Priority: P2. Source: FT-6, all three agents in agreement.

8. **Document `required: True` default in spec**: Add to spec Section 3: "Variables default to `required: true` when omitted." Priority: P3. Source: FT-9, unanimous.

### Two-of-Three Convergence

9. **`PathList` custom type**: Pydantic custom type storing `list[Path]` internally with serializer rendering newline-separated strings for template substitution. Export from `models.py` as reusable type. Apply to existing and new path-list fields. Priority: P1. Source: FT-2 (modified), IA cross-review (proposed serializer), GE (accepted without dispute).

10. **`frozen=True` on `TemplateContext`**: Apply `frozen=True` to core `TemplateContext` and all subclasses. Plugin extensibility addressed by composition (separate `PluginContext`), not by relaxing immutability. Priority: P2. Source: FT-4, IA (endorsed), GE (conceded for core models in Phase 4).

11. **New spec 006 fields use typed patterns**: Any new path or path-list fields added by downstream specs must use `Path` and `PathList` types, not `Optional[str]`. Priority: P2. Source: FT-B, IA-3 (modified to use typed patterns).

12. **`config_conditions` with typed `ConfigCondition` model**: Add `config_conditions: Optional[list[ConfigCondition]]` to `VariableDefinition`, where `ConfigCondition` is a Pydantic model with `field: str` and `value: str`. Validates against known config fields at load time. Priority: P1. Source: IA-1 (modified per FT cross-review), FT (endorsed refinement), GE (deferred plugin axis to spec 007 but did not dispute the typed approach).

---

## 6. Remaining Disputes

DISPUTES_BEGIN

### Dispute 1: Programmatic API parameter design -- plugin-variables parameter

**Parties**: game-engine-advocate vs. integration-architect vs. functional-typing

**game-engine-advocate position** (disputes.md, Dispute 1): The `validate_all()` API must accept `known_plugin_variables: frozenset[str] = frozenset()` from day one. Omitting it means spec 007 must either make a breaking API change or hack around the validation. The parameter costs nothing (default is empty frozenset). This is "non-negotiable."

**integration-architect position** (disputes.md, Dispute 2): Ship `validate_all(config: ValidationConfig) -> ValidationResult` with `ValidationConfig` containing only `root` and `mode`. Document that spec 007 will extend `ValidationConfig`. Do not add `known_plugin_variables` until there is a caller. Accepts `ValidationConfig` model approach, rejects `**kwargs`.

**functional-typing position** (disputes.md, Dispute 2): The initial API should be `validate_all(root: Path, mode: Optional[str] = None) -> ValidationResult` -- minimal and correct. No speculative forward-compatibility. Will defer to synthesizer if majority disagrees.

**Analysis**: The three positions form a spectrum. functional-typing wants bare parameters. integration-architect wants a config model without plugin fields. game-engine-advocate wants a config model (or bare parameter) with an explicit plugin-variables field. The substantive question is whether a zero-cost, default-empty parameter that no current caller uses should be included to prevent a future API change. game-engine-advocate's argument rests on the assumption that adding a parameter to `validate_all` is a breaking change; however, since the API has no external consumers until spec 008 ships, any parameter addition before that point is non-breaking. functional-typing notes this explicitly.

**Synthesizer resolution**: Use a `ValidationConfig` Pydantic model (integration-architect's approach) for the API boundary, containing `root: Path` and `mode: Optional[str] = None`. Do NOT include `known_plugin_variables` in the initial model. Document in the `ValidationConfig` docstring that spec 007 may extend this model with plugin-aware fields. Rationale: the `ValidationConfig` model provides a stable extension surface (adding a field with a default to a Pydantic model is non-breaking), which satisfies game-engine-advocate's concern about future extensibility without including a parameter that has no caller, no tests, and no defined semantics today. This is a minor disagreement; all three agents agree on the API's existence and structured return type.

---

### Dispute 2: `ValidationError.error_type` -- `Literal` vs. `str`

**Parties**: game-engine-advocate vs. integration-architect

**game-engine-advocate position** (disputes.md, Dispute 3): `error_type` must be `str` with runtime validation, not `Literal`. The argument that defeated `Literal` for modes applies identically: plugins will produce custom error types, and `Literal` requires source code modification to accommodate them. "Non-negotiable."

**integration-architect position** (disputes.md, Dispute 3): `Literal` is correct for error types because they are program-internal classifications (the linter defines them, the orchestrator consumes them), not user-facing schema extensions. Adding a new error type requires modifying linter code regardless, unlike adding a new mode (which SC-003 promises via YAML alone).

**functional-typing position** (disputes.md, Flexibility #4): Agrees with integration-architect that `Literal` is correct for spec 005's scope. Will accept `str` if synthesizer prefers, acknowledging the open-set argument has merit.

**Analysis**: integration-architect draws a meaningful distinction: modes are schema-external (users add them via YAML files), but error types are code-internal (only the linter implementation defines them). Adding a new error type inherently requires a code change to the validation logic that produces it. This is different from the mode case, where the entire point of SC-003 is YAML-only addition. However, game-engine-advocate's concern about plugin-contributed validation rules is architecturally coherent: if plugins can compose their own `check_*` functions (which all three agents agree the architecture supports), those functions need to return errors with plugin-defined types.

**Synthesizer resolution**: Use `str` for `error_type`, but validate at construction time against a known registry (mirroring the mode resolution). Define a `KNOWN_ERROR_TYPES: frozenset[str]` in the linter module containing the five core types. The `@field_validator` checks against this set but can be extended at load time. This gives autocompletion and typo-catching for core error types (integration-architect's concern) while remaining open to plugin-contributed types (game-engine-advocate's concern). This is consistent with the resolution adopted unanimously for modes, and applying the same pattern to error types produces a coherent, predictable system.

---

### Dispute 3: Schema version field priority -- P2 vs. P3

**Parties**: functional-typing vs. integration-architect + game-engine-advocate

**functional-typing position** (disputes.md, Dispute 3): Accepts the recommendation but disputes P2 elevation. The version field has no consumer today, no validation logic, and can be added alongside spec 006's changes in the same commit. P3 is correct for a single line of YAML with no enforcement.

**integration-architect + game-engine-advocate position** (both disputes.md): P2. The version field should precede spec 006's schema evolution so the first change is already versioned.

**Analysis**: This is a minor priority dispute, not a substantive disagreement. All three agents agree the field should be added. The question is whether a single-line YAML addition with no validation code merits P2 or P3. functional-typing's argument is technically correct (it is one line with no consumer), but the majority's argument about establishing the versioning practice before the first evolution event is pragmatically sound.

**Synthesizer resolution**: P2. The version field should exist before spec 006's variables are added, establishing the convention that schema changes are accompanied by version bumps. The implementation cost is trivial (one line of YAML), so the priority question is about signaling importance, not about resource allocation. Two of three agents support P2, and the argument that the first schema evolution should be versioned from the start is reasonable.

---

### Dispute 4: Bare import fix sequencing -- P1 prerequisite vs. P2 separate item

**Parties**: game-engine-advocate vs. integration-architect

**game-engine-advocate position** (disputes.md, Dispute 4): The bare import fix (`from models import ...` -> `from .models import ...`) is a prerequisite for the programmatic API, not a separate P2 item. The API is useless if the package cannot be imported from outside `linter/`.

**integration-architect position** (revision.md, Rec 5): Treats the import fix as P2, bundled with `pyproject.toml` entry point work.

**functional-typing position**: Acknowledged the import issue in cross-review of integration-architect (Safe Agreement #4, noting bare imports are a "latent bug"), but did not assign an explicit priority.

**Analysis**: game-engine-advocate is correct that the programmatic API (`validate_all()`) cannot be invoked from outside the `linter/` directory if imports are bare. However, the import fix and the API extraction are the same unit of work -- you cannot create a callable library function without fixing the imports. Treating them as separate priority items is an artificial distinction. The question is not P1 vs. P2 but whether they are one task or two.

**Synthesizer resolution**: The import fix is part of the P1 programmatic API work item, not a separate P2 deliverable. When implementing `validate_all()` as a library function (P1), the imports must be made package-relative as part of that work. The `pyproject.toml` entry point and package discovery configuration remain P2 as packaging infrastructure that can follow once the imports are clean.

DISPUTES_END

---

## 7. Actionable Spec Changes

### P1 -- Must be addressed before spec 005 can be considered complete

**P1-1: Purify schema-loading functions**
- Replace `sys.exit(2)` and `click.echo()` in `load_variables_schema` (`validate.py` L48-56), `load_mode_schema` (L59-67), and `find_project_root` (L35-45) with `SchemaLoadError` exceptions.
- CLI `main()` catches `SchemaLoadError` and calls `sys.exit(2)`.
- Affects: `linter/validate.py`
- Source: FT-1 (unanimous)

**P1-2: Extract programmatic validation API**
- Create `validate_all(config: ValidationConfig) -> ValidationResult` where `ValidationConfig` is a Pydantic model with `root: Path` and `mode: Optional[str] = None`.
- `ValidationResult` is a Pydantic model with `errors: list[LintError]`, `files_checked: int`, `passed: bool`.
- Fix bare imports (`from models import ...` -> `from .models import ...`) as part of this work.
- Click CLI `main()` becomes a thin wrapper calling `validate_all()`.
- Document in `ValidationConfig` docstring that spec 007 may extend the model.
- Affects: `linter/validate.py`, `linter/__init__.py`
- Source: IA-2, FT-1 (prerequisite), GE-N2 (import fix)
- Dispute resolution: No `known_plugin_variables` parameter in initial API. `ValidationConfig` model provides non-breaking extension path.

**P1-3: Define `PathList` custom type**
- Create a `PathList` custom Pydantic type that stores `list[Path]` internally with a `BeforeValidator` that parses newline-separated strings and a custom serializer that renders back to newline-separated strings for template substitution.
- Export from `models.py` as a reusable type.
- Apply to all existing path-list fields: `TARGET_FILES`, `AGENT_DOCS` (if applicable), `CROSS_REVIEWS_OF_ME`, `MY_CROSS_REVIEWS`, `ALL_REVISION_PATHS`, `ALL_REVIEWS`, `ALL_CROSS_REVIEWS`, `ALL_REVISIONS`, `ALL_DISPUTES`, `ROUND_SYNTHESES`.
- Require use for any new path-list fields from downstream specs.
- Affects: `linter/models.py`, `schema/variables.yml` (documentation)
- Source: FT-2 (modified), IA cross-review (serializer design)

**P1-4: Add `config_conditions` field with typed `ConfigCondition` model**
- Add `ConfigCondition(BaseModel)` with `field: str` and `value: str`.
- Add `config_conditions: Optional[list[ConfigCondition]] = None` to `VariableDefinition`.
- Validate `field` values against known config field names at schema-load time.
- Enables spec 006's `PRIOR_ARBITRATION_PATH` (conditioned on `arbiter.timing: inter-round`).
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: IA-1 (modified per FT refinement)

**P1-5: Add spec 006 variables to context models and schema**
- Add `PRIOR_ARBITRATION_PATH: Optional[Path] = None` to `ReviewContext`, `CrossReviewContext`, `RevisionContext`, `DisputesContext`, `SynthesisContext`.
- Add `ARBITRATION_PATHS` (using `PathList` type or `Optional[str]` with upgrade comment) to `CrossRoundSynthesisContext`.
- Add `ARBITRATION_RULINGS: Optional[str] = None` to `CrossRoundSynthesisContext`.
- Add corresponding entries in `schema/variables.yml` with appropriate `config_conditions`.
- Document the rule: core variables carry orchestrator-produced data; plugin variables carry plugin-produced data.
- Affects: `linter/models.py`, `schema/variables.yml`
- Source: IA-3, IA-4

### P2 -- Should be addressed in spec 005's scope

**P2-1: Move MODE_PRESENCE to mode schema YAML declarations**
- Add `mode_in_phases` field to each mode schema YAML listing phases where `{MODE}` is expected (e.g., `mode_in_phases: [review, synthesis, arbitration, cross-round-synthesis]`).
- Derive lookup table via pure function at load time.
- Delete the hardcoded 28-entry `MODE_PRESENCE` dict in `validate.py` L108-144.
- Affects: `schema/modes/*.yml`, `linter/validate.py`, `linter/models.py` (ModeSchema model)
- Source: FT-5, GE-6, IA-7 (unanimous convergence)

**P2-2: Make `VALID_MODES` a dynamic registry**
- Replace `VALID_MODES = frozenset({...})` with a function `get_valid_modes(schema_dir: Path) -> frozenset[str]` that scans `schema/modes/*.yml`.
- Update `ModeSchema.validate_mode` to use the dynamic set instead of the hardcoded frozenset.
- This fixes the contradiction between SC-003 (adding modes via YAML) and the implementation (hard-rejecting unknown modes).
- Affects: `linter/models.py`, `linter/validate.py`
- Source: GE-3 (P2), IA cross-review (endorsed)

**P2-3: Structured `LintError` Pydantic model**
- Define `LintError(BaseModel)` with fields: `error_type: str` (validated against known set), `file_path: str`, `variable_name: Optional[str]`, `phase: str`, `mode: str`, `message: str`, `suggestion: Optional[str]`.
- Define `KNOWN_ERROR_TYPES: frozenset[str]` containing `{"missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"}`.
- All `check_*` functions return `list[LintError]`.
- CLI `main()` formats `LintError` objects for human display.
- Affects: `linter/validate.py`, `linter/models.py`
- Source: IA-8, FT-A (unanimous on model; `str` with validated set resolves `Literal` dispute)

**P2-4: Schema versioning**
- Add `schema_version: "1.0.0"` to `variables.yml` top level.
- Add `schema_version` field to `VariablesSchema` Pydantic model.
- The linter reports the schema version in its output.
- Must be done before spec 006 adds its variables.
- Affects: `schema/variables.yml`, `linter/models.py`
- Source: GE-5, IA-9 (both upgraded to P2)

**P2-5: Apply `frozen=True` to `TemplateContext` hierarchy**
- Change `model_config = {"extra": "forbid"}` to `model_config = {"extra": "forbid", "frozen": True}` on `TemplateContext` and all subclasses.
- Add code comment: plugin-contributed data flows through a separate `PluginContext` model, designed in spec 007.
- Affects: `linter/models.py`
- Source: FT-4 (functional-typing + integration-architect convergence; game-engine-advocate concedes for core)

**P2-6: Document extension contracts in spec 005**
- Add a section to spec Section 6 (Implementation Notes) titled "Extension Points for Downstream Specs" documenting:
  - Extension points: new variables via `schema/variables.yml` addition, new modes via `schema/modes/{mode}.yml` creation, new config conditions via `ConfigCondition`, plugin-contributed data via parallel composition (spec 007).
  - NOT extension points: `extra = "forbid"` on TemplateContext, template syntax `{VARIABLE}`, structural marker syntax.
- Affects: `specs/005-generalized-templates/spec.md`
- Source: GE-9 (elevated to P2)

**P2-7: Mandate Python in spec Implementation Notes**
- Change spec Section 6 from "The linter should be a script (Python or shell)" to "The linter MUST be a Python script following Constitution Principle IX (functional programming, explicit typing, Pydantic models)."
- Affects: `specs/005-generalized-templates/spec.md` L362
- Source: FT-6 (unanimous)

**P2-8: `pyproject.toml` packaging and entry point**
- Add `[tool.setuptools.packages.find]` or equivalent package discovery.
- Add `[project.scripts]` with `conversus-lint = "conversus.linter.validate:main"`.
- Affects: `pyproject.toml`
- Source: IA-5

**P2-9: Schema evolution regression tests**
- Add tests covering: (a) adding a new optional variable passes all existing templates, (b) adding a new required variable for a specific phase produces errors only for that phase's templates, (c) adding a new mode schema file is discovered and validated.
- Affects: `linter/test_validate.py`
- Source: IA-6

### P3 -- Should be addressed, low urgency

**P3-1: Document `required: True` default in spec**
- Add to spec Section 3: "Variables default to `required: true` when the field is omitted. Set `required: false` explicitly for optional variables."
- Affects: `specs/005-generalized-templates/spec.md`
- Source: FT-9 (unanimous)

**P3-2: Fix `AGENT_DOCS` type discrepancy in spec**
- Update spec Section 3 data model to show `AGENT_DOCS` as `type: extracted-content` instead of `type: path-list`, matching the implementation.
- Affects: `specs/005-generalized-templates/spec.md` L171
- Source: IA-10 (unanimous)

**P3-3: Document core-variable vs. plugin-variable namespace rule**
- Add a comment to `schema/variables.yml` header: "Variables in this file carry data produced by the core orchestrator or provided by user config. Variables produced by plugins are namespaced separately (mechanism defined by spec 007)."
- Affects: `schema/variables.yml`
- Source: IA-N3

**P3-4: Make `VALID_PHASES` extensible**
- Apply the same pattern as `VALID_MODES`: derive from schema data or `PHASE_CONTEXT_MODELS` keys.
- Lower urgency than `VALID_MODES` because no spec currently adds new phases.
- Affects: `linter/models.py`
- Source: GE-8

**P3-5: Formalize condition field syntax**
- Define a minimal grammar for the `condition` field in `variables.yml` (currently free-text like `"rounds > 1"`) so the linter can interpret it.
- Affects: `schema/variables.yml`, `linter/validate.py`
- Source: GE-N3

### Deferred -- Explicitly out of spec 005 scope, to be addressed by named downstream specs

**D1: Plugin variable namespace** -- Deferred to spec 007 Phase 1. Source: GE-1.
**D2: `PluginContext` composition architecture** -- Deferred to spec 007 Phase 1. Source: GE-2.
**D3: ModeSchema `extensions` section** -- Deferred to spec 007 Phase 1. Source: GE-7.
**D4: `float`/`number` variable type** -- Deferred to the spec that first needs it. Source: GE-4.
**D5: `__all__` exports on `models.py`** -- Deferred to post-spec-007-Phase-1 when extension contract is defined. Source: FT-7.
**D6: Reserve `schema/objectives/` directory** -- Deferred to spec 007. Source: GE-10.

---

## 8. Key Concessions (Per Agent)

### functional-typing

1. **Withdrew `Literal` types for modes and variable types (FT-3)**. game-engine-advocate demonstrated that `Literal` conflicts with spec 005's own SC-003 extensibility story. functional-typing acknowledged this as "the deepest intellectual correction" -- the constitution's `Literal` guidance applies to program-defined enumerations, not schema-defined ones. (revision.md, Rec 3 disposition)

2. **Withdrew `Final` on `PHASE_CONTEXT_MODELS` (FT-8)**. game-engine-advocate identified this as a registry spec 007 needs to extend. functional-typing accepted that it is a registry, not a constant. (revision.md, Rec 8 disposition)

3. **Modified `MODE_PRESENCE` derivation approach (FT-5)**. Conceded that the `condition` field is not machine-parseable and adopted the mode schema YAML approach proposed by integration-architect and game-engine-advocate. (revision.md, Rec 5 disposition)

4. **Withdrew `itertools.chain` optimization (original Missed Opportunity #5)**. Accepted integration-architect's argument that this optimized concatenation of the wrong abstraction; structured error models make the aggregation question irrelevant. (revision.md, New Rec A)

5. **Deferred `__all__` exports (FT-7)**. Accepted game-engine-advocate's argument that defining the public API surface before the plugin interface is known is premature. (revision.md, Rec 7 disposition)

### game-engine-advocate

1. **Deferred 5 recommendations to spec 007 (GE-1, GE-2, GE-7, GE-10, GE-4)**. Acknowledged that 7 of 10 original recommendations were "spec 007 concerns dressed as spec 005 feedback." The fundamental correction: "Spec 005's job is to be a correct, well-structured foundation. Making it extensible is spec 007's job." (revision.md, Position Summary)

2. **Withdrew `extra = "allow"` on TemplateContext (GE-2)**. functional-typing demonstrated that `dict[str, Any]` violates Principle IX, and the composition pattern is architecturally superior. Withdrew "without reservation." (revision.md, Rec 2 disposition)

3. **Withdrew template-scanning for MODE_PRESENCE (GE-6)**. integration-architect demonstrated this creates circular validation: the linter's rules would depend on the content it validates. (revision.md, Rec 6 disposition)

4. **Withdrew float/number type (GE-4)**. Accepted integration-architect's "premature abstraction" argument and recognized that plugin output uses JSON, not template variables. (revision.md, Rec 4 disposition)

5. **Downgraded `VALID_MODES` from P1 to P2 (GE-3)**. Accepted integration-architect's observation that this is a spec 005 internal consistency fix, not a spec 007 dependency. (revision.md, Rec 3 disposition)

### integration-architect

1. **Retracted MODE_PRESENCE Alignment endorsement (IA-N1)**. functional-typing's cross-review identified the internal contradiction between endorsing the hardcoded table in Alignment and criticizing it in Rec 7. Acknowledged: "The hardcoded table is not the right approach." (revision.md, Rec 7 disposition)

2. **Retracted characterization of schema-loading functions as "pure" (IA-N2)**. functional-typing identified that `load_variables_schema` and `load_mode_schema` call `sys.exit()` and `click.echo()`, making them impure. Acknowledged: "I failed to catch this contradiction." (revision.md, Rec 2 disposition)

3. **Replaced `dict[str, str]` with typed `ConfigCondition` model (IA-1)**. functional-typing correctly identified the weakly-typed interface as violating the spirit of Principle IX. (revision.md, Rec 1 disposition)

4. **Withdrew `plugin_data: dict[str, Any]` (IA-N4)**. Conceded in Phase 4 after both functional-typing and game-engine-advocate rejected it as a Principle IX violation. Adopted the composition model. (disputes.md, Dispute 1 concession)

5. **Upgraded schema versioning from P3 to P2 (IA-9)**. game-engine-advocate's argument that versioning should precede the first schema evolution event was persuasive. (revision.md, Rec 9 disposition)

---

*This synthesis was produced by a neutral synthesizer with no agenda. Every claim traces to a specific artifact in the deliberation record. No new ideas were introduced.*