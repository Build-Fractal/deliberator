# Conversus Review Synthesis -- Spec 006: Inter-Round Arbitration

**Round**: 1
**Agents**: functional-typing, game-engine-advocate, integration-architect
**Date**: 2026-03-21

---

## Process Summary

Three agents reviewed spec 006 from complementary perspectives: type-system correctness (functional-typing), game engine extensibility (game-engine-advocate), and integration pipeline completeness (integration-architect). The original reviews produced 8, 5, and 9 recommendations respectively, with significant overlap on the top gap (influence-aware heading validation) and complementary findings on other issues.

The cross-review phase produced genuine engagement: functional-typing downgraded two recommendations (Phase enum P1->P2, ErrorType reclassification P2->P3) based on integration-architect's pragmatic prioritization framework. game-engine-advocate withdrew two recommendations (plugin hook comments, influence dispatch externalization) based on integration-architect's YAGNI arguments. All three agents adopted integration-architect's template wiring findings ({ARBITRATION_PATHS}, {ARBITRATION_RULINGS} dead infrastructure) as P1 items they had independently missed.

The revision phase produced 3 new recommendations adopted from cross-reviews and 2 priority adjustments. The dispute phase resolved all major disagreements, with one minor sequencing tension (config_conditions documentation vs. required status) resolved through concession.

---

## Recommendation Scorecard

| ID | Recommendation | Source | Priority | Consensus |
|----|---------------|--------|----------|-----------|
| 1 | Add influence-aware heading data to ArbitrationConfig + cooperative.yml | All three | P1 | Unanimous |
| 2 | Wire {ARBITRATION_PATHS} into cross-round synthesis template | integration-architect | P1 | Unanimous |
| 3 | Wire {ARBITRATION_RULINGS} into cross-round synthesis template | integration-architect | P1 | Unanimous |
| 4 | Use Phase enum in validate.py | functional-typing | P2 | functional-typing + integration-architect |
| 5 | Type VariableDefinition.phases as list[Phase] | functional-typing | P2 | functional-typing + integration-architect |
| 6 | Document linter static-vs-runtime heading validation boundary | integration-architect | P2 | Unanimous |
| 7 | Add structural markers for provisionally resolved disputes | integration-architect + game-engine-advocate | P2 | integration-architect + game-engine-advocate |
| 8 | Fix conversus.yml doc paths for game-engine-advocate | game-engine-advocate | P2 | Unanimous |
| 9 | Document config_conditions as metadata-only (not linter-enforced) | functional-typing | P2 | functional-typing + integration-architect |
| 10 | Add PRIOR_ARBITRATION_SECTION field documentation on ReviewContext | integration-architect | P2 | integration-architect + functional-typing |
| 11 | Verify PRIOR_ARBITRATION_PATH set during inter-round dispatch | integration-architect | P2 | integration-architect + game-engine-advocate |
| 12 | Use match/case for phase-specific validation logic | functional-typing | P2 | functional-typing |
| 13 | Normalize ConfigCondition operators in variables.yml | game-engine-advocate | P3 | game-engine-advocate |
| 14 | Reclassify semantic misuses of ErrorType | functional-typing | P3 | functional-typing |
| 15 | Create ConversusConfig Pydantic model | functional-typing | P3 | functional-typing + game-engine-advocate |
| 16 | Add stagnation-influence interaction documentation | integration-architect | P3 | integration-architect |
| 17 | Add PRIOR_ARBITRATION_PATH model_validator on ReviewContext | functional-typing | P3 | functional-typing + integration-architect |
| 18 | Mark ARBITRATION_RULINGS as required:true (after config_conditions evaluation exists) | integration-architect | P3 | integration-architect |

**Withdrawn:**
- Plugin hook comments in SKILL.md (game-engine-advocate R3) -- SKILL.md is executable spec; archived spec references would mislead
- Influence dispatch externalization to schema/influence-levels.yml (game-engine-advocate R5) -- premature abstraction; own OBA-1 undermined the use case

---

## Dangerous Contradictions Found

**None.** No agent proposed a recommendation that would break or invalidate another agent's proposals. All recommendations are additive or complementary. The three perspectives (type system, extensibility, integration pipeline) produced orthogonal findings that compose without conflict.

---

## Systemic Contradictions

### SC1: Static Linting vs. Runtime Configuration

The linter validates templates statically before runtime configuration is known. Influence level is a runtime config value. This creates a fundamental architectural boundary: the linter can validate template structure and variable presence, but cannot validate influence-dependent content (headings, dispute categorization). All three agents identified this boundary and agree it is intentional, not a bug. The resolution is:
- The mode schema stores all heading variants (P1 recommendation #1)
- The linter validates against the schema's default headings
- The orchestrator validates against influence-adjusted headings at runtime
- A code comment documents the boundary to prevent future misguided "fixes"

### SC2: config_conditions Schema Precision vs. Enforcement Gap

The `variables.yml` schema declares `config_conditions` on 7+ variables with precise field/operator/value conditions. The linter does not evaluate these conditions -- variables are either always required or never required, regardless of declared conditions. This creates false precision: the schema suggests conditional enforcement that does not exist. All agents agree the gap should be documented; full evaluation is deferred to a future spec.

### SC3: Typed Pipeline vs. Template Last-Mile

The schema-to-model-to-SKILL.md pipeline is fully typed and validated. But the template -- the only artifact that actually reaches the agent -- can omit variables without the linter flagging it (when `required: false` or when the variable has unimplemented config_conditions). This means perfectly typed infrastructure can be dead. The cross-round synthesis template's missing references to {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} exemplify this gap.

---

## Convergence Achieved

All three agents converged on the following positions:

1. **The influence-aware heading gap is the top priority.** Universal P1. All agents propose the same solution: structured heading data in both the YAML schema and Pydantic model, keyed by influence level.

2. **Dead template variables must be connected.** {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} are fully provisioned but never consumed by the cross-round synthesis template. Universal P1 after the cross-review cycle.

3. **The StrEnum implementation is correct.** All agents validate the InfluenceLevel and ArbiterTiming StrEnums as properly implemented per Constitution Principle IX, with correct factory extension documentation.

4. **Backward compatibility is preserved.** Omitting `timing` and `influence` produces pre-spec-006 behavior. The default values (`final`, `binding`) are correctly implemented.

5. **The spec does not block future extensibility.** game-engine-advocate's core finding ("no decisions that would require rework when the game engine ships") is independently confirmed by both co-reviewers.

6. **The linter's static-vs-runtime boundary is intentional.** Influence-adjusted heading validation belongs at the orchestrator level. The linter validates template structure, not runtime content.

7. **config_conditions are metadata-only.** The schema declares conditions that the linter does not evaluate. This should be documented to prevent false expectations.

---

## Remaining Disputes

<!-- CONVERSUS:DISPUTES_BEGIN -->

### RD1: config_conditions Documentation Sequencing (Minor)

**Parties**: functional-typing vs. integration-architect
**Issue**: Should spec 006 changes include documenting config_conditions as metadata-only (functional-typing) or should the required status be fixed first (integration-architect)?
**Resolution**: integration-architect conceded during the dispute phase. Documentation-first is safer because changing required status without evaluation creates unconditional enforcement, which is wrong for conditionally-required variables. Both agree documentation should happen in this spec cycle; evaluation mechanism deferred.
**Severity**: Low. Both agents agree on the end state; disagreement was only on sequencing and has been resolved through concession.

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1 -- Must Address

**1. Add influence-aware heading data to ArbitrationConfig and cooperative.yml**
- Add `influence_headings: dict[str, list[str]]` field to `ArbitrationConfig` in `linter/models.py`
- Add `influence_headings` section to `schema/modes/cooperative.yml` with heading lists for `recommended` and `advisory` influence levels
- Default `required_headings` serves as the `binding` headings (no duplication needed)
- Files: `linter/models.py`, `schema/modes/cooperative.yml`
- Source: functional-typing Rec 2, game-engine-advocate R2, integration-architect Rec 1 + Rec 7

**2. Wire {ARBITRATION_PATHS} into cross-round synthesis template**
- Add a conditional reading instruction in the "What to Read" section of `templates/cooperative/cross-round-synthesis.md` referencing `{ARBITRATION_PATHS}` for inter-round arbitration scenarios
- Files: `templates/cooperative/cross-round-synthesis.md`
- Source: integration-architect Rec 2

**3. Wire {ARBITRATION_RULINGS} into cross-round synthesis template**
- Add `{ARBITRATION_RULINGS}` reference in the Resolution Attribution section of `templates/cooperative/cross-round-synthesis.md` as pre-formatted arbiter ruling content
- Files: `templates/cooperative/cross-round-synthesis.md`
- Source: integration-architect Rec 3

### P2 -- Should Address

**4. Use Phase enum in validate.py**
- Import `Phase` from `models.py` and replace all string literal phase comparisons (`"arbitration"`, `"synthesis"`, `"cross-round-synthesis"`) with enum members
- Type the `phase` parameter in `check_required_headings` and `check_structural_markers` as `Phase`
- Files: `linter/validate.py`
- Source: functional-typing Rec 1

**5. Type VariableDefinition.phases as list[Phase]**
- Change `phases: list[str]` to `phases: list[Phase]` in `linter/models.py`
- Remove the `validate_phases` field_validator (Pydantic handles validation through the type)
- Files: `linter/models.py`
- Source: functional-typing Rec 4

**6. Document linter static-vs-runtime heading validation boundary**
- Add a comment in `validate.py` `check_required_headings` function explaining that arbitration heading validation is influence-unaware by design; runtime validation in SKILL.md handles influence-adjusted headings
- Files: `linter/validate.py`
- Source: integration-architect Rec 4

**7. Add structural markers for provisionally resolved disputes**
- Define `PROVISIONALLY_RESOLVED_BEGIN`/`PROVISIONALLY_RESOLVED_END` markers in the synthesis template for disputes resolved with `recommended` influence
- Update the dispute-parsing subsystem documentation in SKILL.md to reference these markers
- Files: `templates/cooperative/synthesis.md`, `SKILL.md`
- Source: integration-architect Missed Opportunity 6, game-engine-advocate NEW-2

**8. Fix conversus.yml doc paths**
- Update game-engine-advocate docs from `specs/007-game-engine/` to `specs/archive/game-engine-vision/`
- Files: `specs/006-inter-round-arbitration/conversus.yml`
- Source: game-engine-advocate R4

**9. Document config_conditions as metadata-only**
- Add documentation (inline comments or schema header) noting that `config_conditions` are schema metadata for documentation purposes and are not evaluated by the linter at runtime
- Files: `schema/variables.yml`, `linter/validate.py`
- Source: functional-typing Rec 5

**10. Add PRIOR_ARBITRATION_SECTION field documentation**
- Add inline comment on `ReviewContext.PRIOR_ARBITRATION_SECTION` distinguishing it from `PRIOR_ARBITRATION_PATH`
- Files: `linter/models.py`
- Source: integration-architect Rec 5

**11. Verify PRIOR_ARBITRATION_PATH path computation is explicit**
- Add explicit path formula in SKILL.md for setting `{PRIOR_ARBITRATION_PATH}` during Round R > 1 dispatch
- Files: `SKILL.md`
- Source: integration-architect Rec 6

**12. Use match/case for phase-specific validation**
- Refactor `check_required_headings` and `check_structural_markers` to use `match`/`case` with `Phase` enum
- Files: `linter/validate.py`
- Source: functional-typing Rec 6

### P3 -- Nice to Have

**13. Normalize ConfigCondition operators in variables.yml**
- Add explicit `operator: "=="` to all config_conditions entries that omit it
- Files: `schema/variables.yml`
- Source: game-engine-advocate R1

**14. Reclassify ErrorType semantic misuses**
- Add `MISSING_TEMPLATE` and `INVALID_SCHEMA_ENTRY` to `ErrorType` enum; update `validate_all` usage
- Files: `linter/models.py`, `linter/validate.py`
- Source: functional-typing Rec 3

**15. Create ConversusConfig Pydantic model**
- Define `ArbiterConfig` with typed `ArbiterTiming` and `InfluenceLevel` fields; wrap in top-level `ConversusConfig`
- Use `extra: "allow"` or `plugins: dict[str, Any]` for extensibility
- Files: `linter/models.py` (or new `linter/config.py`)
- Source: functional-typing Rec 7

**16. Add stagnation-influence interaction documentation**
- Explicitly connect influence-adjusted dispute counts to stagnation detection in SKILL.md
- Files: `SKILL.md`
- Source: integration-architect Rec 8

**17. Add PRIOR_ARBITRATION_PATH model_validator**
- Add cross-field validator on ReviewContext: when PRIOR_ARBITRATION_SECTION is non-empty, PRIOR_ARBITRATION_PATH must be non-None
- Files: `linter/models.py`
- Source: functional-typing Rec 8

**18. Mark ARBITRATION_RULINGS as conditionally required**
- Defer until config_conditions evaluation is implemented; then set `required: true` with config_conditions gate
- Files: `schema/variables.yml`
- Source: integration-architect Rec 9

---

## Key Concessions

1. **functional-typing conceded P1 for Phase enum usage** -- downgraded to P2 based on integration-architect's argument that P1 should be reserved for correctness gaps, not constitution compliance issues in working code.

2. **functional-typing conceded P2 for ErrorType reclassification** -- downgraded to P3 based on integration-architect's observation that the misclassification is linter-internal with no downstream behavioral impact.

3. **game-engine-advocate withdrew plugin hook comments** -- based on integration-architect's argument that SKILL.md is an executable spec where comments referencing archived specs would mislead implementers.

4. **game-engine-advocate withdrew influence dispatch externalization** -- based on integration-architect's premature abstraction argument and the game-engine-advocate's own self-correction (OBA-1) that game engine plugins are unlikely to need new influence levels.

5. **game-engine-advocate revised from Option B to Option A for heading validation** -- originally favored skipping heading validation for dynamic templates; revised to structured data approach based on cross-review arguments that abandoning static validation removes a safety net.

6. **integration-architect conceded on config_conditions sequencing** -- accepted functional-typing's documentation-first approach over the fix-required-status-first approach, because changing required status without evaluation creates unconditional enforcement.

7. **All three agents adopted integration-architect's template wiring findings** -- {ARBITRATION_PATHS} and {ARBITRATION_RULINGS} dead infrastructure was missed by functional-typing and game-engine-advocate in their original reviews; both acknowledged the blind spot and adopted the findings as P1.
