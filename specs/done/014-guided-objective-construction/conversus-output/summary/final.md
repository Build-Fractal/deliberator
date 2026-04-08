# Conversus Final Synthesis -- Spec 014: Guided Objective Construction

**Date**: 2026-03-24
**Spec**: `specs/014-guided-objective-construction/spec.md`
**Implementation**: `conversus/schemas/construction.py`
**Tests**: `tests/test_construction.py`

---

## 1. Process Summary

Four specialist agents reviewed the three-stage guided objective construction pipeline:

| Agent | Scope | Phase 1 P1s | Final P1s |
|---|---|---|---|
| **game-theorist** | Mathematical correctness, decision-type mapping, symbolic form integrity | 4 (str.replace, source map, disambiguation, boolean) | 3 (str.replace, source map, FR-003) |
| **schema-engineer** | Pydantic models, type safety, protocol design, validation | 4 (source structure, source map, str.replace, boolean) | 4 (source structure, source map, str.replace, FR-003) |
| **functional-architect** | Pipeline architecture, composability, pattern adherence | 4 (source map, mode override, FR-003, constraints) | 4 (source map, str.replace, FR-003, source structure) |
| **spec-compliance** | FR-by-FR compliance, success criteria, coverage | 5 (FR-003, FR-020, FR-014, LLMGapFiller, gap_fill_model) | 4 (FR-003, FR-020, str.replace, source map) |

The process produced strong convergence. Initial P1 lists ranged from 4-5 items with different compositions. By the disputes phase, all four agents converged on the same four P1 items. Key shifts:

- **game-theorist**: Upgraded FR-003 from P2 to P1 (accepted MUST argument). Downgraded boolean coercion from P1 to P2 (no current trigger). Softened disambiguation from ValueError to warning.
- **schema-engineer**: Downgraded boolean coercion from P1 to P2. Withdrew `.yaml` extension support. Upgraded FR-003 from P2 to P1.
- **functional-architect**: Downgraded mode override from P1 to P2 (accepted spec-compliance's reading of FR-018). Downgraded constraint wiring from P1 to P2. Upgraded str.replace from P2 to P1.
- **spec-compliance**: Downgraded FR-014 from P1 to P2 (accepted pipeline-vs-CLI scope argument). Downgraded LLMGapFiller from P1 to P2 (acknowledged FR-016 dependency conflict). Adopted str.replace and source map as P1s.

---

## 2. Recommendation Scorecard

| ID | Recommendation | Origin | Final Priority | Unanimous? |
|---|---|---|---|---|
| **BUG-1** | Return source map from `fill_parameter_gaps` (FilledParameters dataclass) | All 4 agents | **P1** | Yes |
| **BUG-2** | Fix `_substitute_symbolic_form` with regex word-boundary replacement | game-theorist, schema-engineer, functional-architect | **P1** | Yes |
| **BUG-3** | Add boolean coercion to `_coerce_value` (bidirectional true/false/None) | game-theorist, schema-engineer | **P2** | Yes |
| **FEAT-1** | FR-003: TemplateSelector protocol + implementations + parameter | All 4 agents | **P1** | Yes (3-1 on scope: 3 want implementations, 1 wants callback only) |
| **FEAT-2** | FR-020: SourceProvenance Pydantic model with required `problem_md` | schema-engineer, spec-compliance | **P1** | Yes |
| **FEAT-3** | FR-014: `register_objective_in_config` utility function (CLI layer) | spec-compliance | **P2** | Yes |
| **FEAT-4** | FR-022/FR-009: LLMGapFiller + gap_fill_model config (bundled) | spec-compliance | **P2** | Yes (deferred pending spec amendment) |
| **FEAT-5** | FR-003 template ranking heuristics | game-theorist | **P3** | Yes |
| **POLISH-1** | GapFillRefused custom exception | schema-engineer, game-theorist | **P2** | Yes |
| **POLISH-2** | Add logging to construction pipeline | functional-architect | **P2** | Yes |
| **POLISH-3** | Provenance tag validation via Literal type | schema-engineer | **P2** | Yes |
| **POLISH-4** | Constraint parameter gap-filling | game-theorist, functional-architect | **P3** | Yes (after dispute resolution) |
| **POLISH-5** | Separate write_objective from construct_objective | functional-architect | **P3** | Yes |
| **POLISH-6** | `.yml` convention documentation | schema-engineer | **P3** | Yes (withdrawn as code change, surviving as docs) |
| **TEST-1** | Overlapping parameter name test for str.replace fix | functional-architect | **P2** | Yes |
| **TEST-2** | Retry/re-ask test (FR-007) | spec-compliance | **P2** | 3-1 (schema-engineer says P3) |
| **TEST-3** | Mode override test rewrite/rename | functional-architect | **P3** | Yes |
| **TEST-4** | Explicit importability test (SC-005) | spec-compliance | **P3** | Yes |
| **TEST-5** | GapList frozen mutation test | functional-architect | **P3** | Yes |
| **TEST-6** | YAML round-trip determinism test | spec-compliance | **P3** | Yes |

---

## 3. Dangerous Contradictions Found

### 3.1 str.replace failure mode disagreement (resolved)

Game-theorist described the danger as "value substitution introducing new matchable substrings" (multi-pass injection). Schema-engineer described it as "single-character `w` corrupting words like `score`." Functional-architect initially questioned whether regex word boundaries handle mathematical expressions. All three described *different* failure modes for the same bug.

**Resolution**: The regex word-boundary fix (`re.sub(rf'\b{re.escape(name)}\b', ...)`) addresses all three failure modes. The specific failure scenario matters less than the fix being comprehensive. Game-theorist's value-injection scenario is the most subtle (requires multi-pass analysis) but is also prevented by the single-pass-per-parameter implementation. Schema-engineer's substring scenario is the most likely trigger with current templates. All agents converge on the same fix.

### 3.2 FR-003 MUST vs P2 (resolved)

Game-theorist initially classified FR-003 as P2 ("rarely produces ambiguous results"). Spec-compliance argued MUST-level requirements are P1 by definition and that every multi-template case triggers the violation. Game-theorist accepted the upgrade in revision.

**Resolution**: FR-003 is P1. The remaining dispute is scope (callback vs callback + implementations), with 3 agents favoring full implementations and 1 favoring callback only.

### 3.3 Mode parameter: override vs fallback (resolved)

Functional-architect initially classified the shadowed `mode` parameter as a P1 correctness bug. Spec-compliance argued FR-018's "explicit and deterministic" mapping means mode is derived from decision type, not independently configurable. Functional-architect accepted the downgrade in revision.

**Resolution**: The `mode` parameter is a fallback for unmapped decision types, not a user override. The test `test_explicit_mode_override` should be renamed or rewritten. This is P3.

---

## 4. Systemic Contradictions

### 4.1 FR-016 vs FR-022: no-extra-dependencies vs LLMGapFiller

FR-016 requires the pipeline to ship in `conversus-schemas` with "no extra dependencies beyond pydantic/pyyaml." FR-022 requires an `LLMGapFiller` implementation that "accepts a model provider and generates contextual questions." An LLMGapFiller needs an LLM client library, which violates FR-016.

**Synthesizer assessment**: This is a genuine spec conflict. The resolution is a spec amendment: FR-016 applies to *import-time* dependencies; FR-022's LLMGapFiller accepts the LLM client as a *runtime-injected* callable or protocol. The class itself imports nothing beyond stdlib/pydantic/yaml. This preserves both requirements.

### 4.2 Pipeline scope vs integration scope

Multiple FR items (FR-014 `conversus.yml`, FR-009 `gap_fill_model` config, FR-005 contextualised questions) blur the line between the construction pipeline and the integration/CLI layer. The pipeline is a pure-function engine; these items require integration code that reads config files, modifies project state, and manages interactive sessions.

**Synthesizer assessment**: The pipeline's boundary should be: accept inputs, produce `AssembledObjective`, optionally serialize. All config reading, project-state modification, and interactive session management belong in a CLI/integration layer that calls the pipeline. FR-014 and FR-009 should be reframed as integration requirements, not pipeline requirements. FR-005 contextualisation belongs in GapFiller implementations.

---

## 5. Convergence Achieved

| Topic | Phase 1 | Phase 4 |
|---|---|---|
| P1 item count | 3-5 items, different compositions | 4 items, unanimous |
| str.replace priority | 3 P1 + 1 P2 | 4 P1 |
| Boolean coercion priority | 2 P1 + 0 raised | 4 P2 |
| FR-003 priority | 2 P1 + 2 P2 | 4 P1 |
| Mode override | 1 P1 + 0 raised | 4 P3 (test-only) |
| Constraint wiring | 1 P1 + 1 P3 + 2 not raised | 4 P3 |
| LLMGapFiller | 1 P1 + 3 not raised | 4 P2 (deferred) |
| FR-014 conversus.yml | 1 P1 + 3 not raised | 4 P2 (CLI layer) |
| Architecture soundness | 4 affirm | 4 affirm |
| Pipeline composability | 4 affirm | 4 affirm |

Convergence rate: 100% on P1 items. The four P1 items are locked with no remaining disputes on their inclusion. The only remaining dispute on P1 items is the *scope* of the FR-003 fix (callback vs full implementation), with 3-1 consensus favoring full implementation.

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

**Dispute A: FR-003 implementation scope**
- **3 agents** (game-theorist, functional-architect, spec-compliance): P1 must include `TemplateSelector` protocol + `InteractiveTemplateSelector` + `NonInteractiveTemplateSelector` implementations + `template_selector` parameter on `construct_objective`. ~30 lines of code.
- **1 agent** (schema-engineer): P1 is the callback parameter; implementations are P2.
- **Synthesizer assessment**: The 3-1 consensus is correct. A callback without implementations does not satisfy FR-003's "MUST present" language. The ~30 lines of additional code is trivial. Ship the full implementation as P1.

**Dispute B: SourceProvenance.problem_md value strategy**
- **3 agents** (schema-engineer, functional-architect, spec-compliance): Required with a `PROBLEM_MD_STDIN` constant default.
- **1 agent** (game-theorist): Required with caller-provided descriptive string, no magic sentinel.
- **Synthesizer assessment**: Define the constant for discoverability. Let callers override. Both approaches are compatible; the constant is better documentation.

**Dispute C: Retry test priority**
- **3 agents** (game-theorist, functional-architect, spec-compliance): P2.
- **1 agent** (schema-engineer): P3.
- **Synthesizer assessment**: P2 is correct. FR-007 is MUST. An untested MUST is a regression risk. However, it is the lowest-priority P2 item.

**Dispute D: Constraint wiring priority**
- **3 agents** (game-theorist, schema-engineer, spec-compliance): P3.
- **1 agent** (functional-architect): P2 in revision, later conceded P3 in disputes.
- **Synthesizer assessment**: P3. Constraint names in the output satisfy FR-011. Parameter resolution is an execution-stage concern. Dispute resolved by concession.
<!-- CONVERSUS:DISPUTES_END -->

---

## 6. Actionable Spec Changes

### P1 -- Bug Fixes (ship immediately)

**P1-BUG-1: Fix source map data loss in `fill_parameter_gaps`**
- File: `conversus/schemas/construction.py`
- Change: Define `FilledParameters` frozen dataclass with `values: dict[str, Any]` and `source_map: dict[str, str]`. Change `fill_parameter_gaps` return type from `dict[str, Any]` to `FilledParameters`. Remove source-map reconstruction logic from `construct_objective` (lines 760-773). Consume `FilledParameters.source_map` directly.
- Risk: Callers of `fill_parameter_gaps` must update to unpack the dataclass. All callers are internal.

**P1-BUG-2: Fix `_substitute_symbolic_form` substring collision**
- File: `conversus/schemas/construction.py`
- Change: Replace `result.replace(name, str(value))` with `result = re.sub(rf'\b{re.escape(name)}\b', str(value), result)` in `_substitute_symbolic_form`.
- Risk: None. The regex fix is a strict superset of the current behavior for well-formed templates.
- Test: Add regression test with parameters `w` and `w_fast` in the same symbolic form (TEST-1).

### P1 -- Feature Gaps (ship immediately)

**P1-FEAT-1: Implement FR-003 multi-template presentation**
- File: `conversus/schemas/construction.py`
- Change: Define `TemplateSelector` protocol with `select(candidates: list[ObjectiveTemplate], descriptions: list[str]) -> ObjectiveTemplate`. Implement `InteractiveTemplateSelector` (prints descriptions, prompts for choice) and `NonInteractiveTemplateSelector` (returns `candidates[0]`). Add `template_selector` parameter to `construct_objective`, defaulting to `NonInteractiveTemplateSelector()`.
- Risk: Changes `construct_objective` signature. Default preserves backward compatibility.

**P1-FEAT-2: Restructure `AssembledObjective.source` as `SourceProvenance` (FR-020)**
- File: `conversus/schemas/construction.py`
- Change: Define `SourceProvenance(BaseModel)` with `problem_md: str` (required, with `PROBLEM_MD_STDIN = "<stdin>"` constant) and `filled_by: dict[str, Literal["explicit", "default", "gap_filled", "deferred"]]`. Change `AssembledObjective.source` from `dict[str, str]` to `SourceProvenance`. Update model validator. Add `problem_md_path: str` parameter to `construct_objective`.
- Risk: Breaking change to `AssembledObjective.source` type. All test `source` dicts must be updated.

### P2 -- Robustness and Compliance

**P2-1: Add boolean coercion to `_coerce_value`**
- Add explicit branches for true-like (`"true"`, `"1"`, `"yes"`) and false-like (`"false"`, `"0"`, `"no"`) strings, returning `None` for unrecognized input. Add boolean-specific retry guidance in `_fill_single_gap`.

**P2-2: Define `GapFillRefused` exception**
- Define `GapFillRefused(Exception)` alongside `GapFiller` protocol. Have `NonInteractiveGapFiller` raise it instead of `RuntimeError`. Catch `GapFillRefused` specifically in `fill_parameter_gaps`.

**P2-3: Add logging**
- Add `logger = logging.getLogger(__name__)` to `construction.py`. Log: classified decision type, selected templates, extracted parameters, gap count, retry attempts.

**P2-4: Validate provenance tags via Literal type**
- Type `SourceProvenance.filled_by` values as `Literal["explicit", "default", "gap_filled", "deferred"]` (included in P1-FEAT-2).

**P2-5: FR-014 `conversus.yml` integration**
- Provide `register_objective_in_config(objective_path: Path, config_path: Path)` utility function. Call from CLI layer, not from `construct_objective`.

**P2-6: LLMGapFiller + gap_fill_model config (FR-022/FR-009)**
- Requires spec amendment resolving FR-016/FR-022 conflict. LLMGapFiller accepts LLM client as injected callable. `gap_fill_model` added as `construct_objective` parameter and `conversus.yml` config key.

**P2-7: Retry test (FR-007)**
- Use `SequentialGapFiller` with `["invalid", "999", "5.0"]` for a parameter with range 0-10. Assert third answer accepted.

**P2-8: Overlapping parameter name regression test**
- Test `_substitute_symbolic_form` with `w` and `w_fast` in the same form. Documents the fix from P1-BUG-2.

### P3 -- Polish and Completeness

**P3-1: Constraint parameter gap-filling** -- Wire `load_constraint_templates` into assembly when execution pipeline needs it.

**P3-2: Template ranking heuristics** -- Replace alphabetical sort with keyword overlap, priority field, or parameter-name matching.

**P3-3: Separate `write_objective` from `construct_objective`** -- Extract to standalone function mirroring `write_features` in `extraction.py`.

**P3-4: `.yml` convention documentation** -- Document in template authoring guide that only `.yml` is supported.

**P3-5: Mode override test rewrite** -- Rename `test_explicit_mode_override` to reflect what it actually tests, or rewrite to test the fallback path with a custom decision type.

**P3-6: Explicit importability test (SC-005)** -- Mirror `test_game_forms.py` pattern.

**P3-7: GapList frozen mutation test** -- Document or switch `gaps` to `tuple`.

**P3-8: YAML round-trip determinism test** -- Write both runs to file, assert byte-identical.

**P3-9: `problem.md` Type field parser (FR-019)** -- `parse_problem_md(path) -> (text, explicit_type)` for CLI integration.

**P3-10: Classification confidence metadata** -- When top two types have match counts within 1, log warning. Add optional `classification_confidence` to return metadata.

---

## 7. Key Concessions

| Agent | Conceded | Reason |
|---|---|---|
| **game-theorist** | FR-003 upgraded to P1 | Accepted spec-compliance's MUST argument |
| **game-theorist** | Boolean coercion downgraded to P2 | No current trigger |
| **game-theorist** | Disambiguation softened from ValueError to warning | Pipeline should never refuse to produce output |
| **schema-engineer** | Boolean coercion downgraded to P2 | No current trigger |
| **schema-engineer** | `.yaml` extension support withdrawn | Convention enforcement > permissiveness |
| **schema-engineer** | FR-003 upgraded to P1 | Accepted MUST argument |
| **functional-architect** | Mode override downgraded from P1 to P2 (test-only) | Accepted FR-018 "deterministic mapping" reading |
| **functional-architect** | Constraint wiring downgraded from P1 to P3 | Accepted grammatical analysis of FR-011 and execution-scope argument |
| **functional-architect** | str.replace upgraded from P2 to P1 | Accepted 3-1 consensus and triviality of fix |
| **spec-compliance** | FR-014 downgraded from P1 to P2 | Accepted pipeline-vs-CLI scope distinction |
| **spec-compliance** | LLMGapFiller downgraded from P1 to P2 | Acknowledged FR-016 dependency conflict |
| **spec-compliance** | SC-002 reframed as filler concern | Accepted that NLP interpretation is filler's job, not pipeline's |
