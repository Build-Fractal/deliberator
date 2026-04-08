# Conversus Review Synthesis -- Spec 006: Inter-Round Arbitration

**Round**: 2 (Final)
**Agents**: functional-typing, game-engine-advocate, integration-architect
**Date**: 2026-03-22
**Prior Round Synthesis**: round-1/summary/final.md
**Advisory Arbitration**: round-1/arbitration/resolution.md

---

## Process Summary

Round 2 was the final round of a 2-round cooperative deliberation. All three agents received the Round 1 synthesis (18 recommendations, 1 resolved dispute, 6 concessions) and the advisory arbitration (7 advisory opinions, 4 considerations for next round) as context.

Round 2 focused on three areas: (1) producing implementation-ready specifications for the three P1 items, (2) resolving remaining P2 design questions raised by the arbiter's advisory opinions, and (3) filling coverage gaps identified during cross-review.

The key outcomes of Round 2:
- **influence_headings field type settled**: Three-agent convergence on `dict[str, list[str]]` with string keys. YAML structure finalized with exact heading lists per influence level.
- **SC1 boundary re-applied**: functional-typing identified that integration-architect's P1 Rec 3 conflated static and runtime validation. The correction was accepted: influence_headings serves runtime heading validation (orchestrator), not static template validation (linter).
- **Provisional-resolution marker lifecycle settled**: Three-agent convergence on round-scoped markers with explicit re-opening semantics, marked as unstable per Principle II.
- **Phase enum items upgraded to unanimous**: game-engine-advocate confirmed no objection to P2 items 4, 5, and 12, upgrading from bilateral to three-agent consensus.
- **Template last-mile audit adopted**: All three agents acknowledge the systemic blind spot from Round 1 and adopt the manual audit practice.
- **P2 sub-ordering established**: P2-easy (documentation/path fixes) vs. P2-structural (type system/markers) enables incremental implementation.
- **Zero remaining disputes**: All design questions resolved through convergence.

---

## Recommendation Scorecard

| ID | Recommendation | Source | Priority | Round 1 Status | Round 2 Status | Consensus |
|----|---------------|--------|----------|----------------|----------------|-----------|
| 1 | Add influence_headings to ArbitrationConfig + cooperative.yml | All three | P1 | Unanimous | Implementation-ready (field type, YAML, static-vs-runtime boundary settled) | Unanimous |
| 2 | Wire {ARBITRATION_PATHS} into cross-round synthesis template | integration-architect | P1 | Unanimous | Implementation-ready (exact template text) | Unanimous |
| 3 | Wire {ARBITRATION_RULINGS} into cross-round synthesis template | integration-architect | P1 | Unanimous | Implementation-ready (exact template text) | Unanimous |
| 4 | Use Phase enum in validate.py | functional-typing | P2 | Bilateral (FT+IA) | Upgraded to Unanimous (GEA confirmed R2) | Unanimous |
| 5 | Type VariableDefinition.phases as list[Phase] | functional-typing | P2 | Bilateral (FT+IA) | Upgraded to Unanimous (GEA confirmed R2) | Unanimous |
| 6 | Document linter static-vs-runtime heading validation boundary | integration-architect | P2 | Unanimous | Extended with influence_headings context | Unanimous |
| 7 | Add structural markers for provisionally resolved disputes | IA + GEA | P2 | Bilateral (IA+GEA) | Lifecycle design settled; marked as unstable per Principle II | Unanimous |
| 8 | Fix conversus.yml doc paths | game-engine-advocate | P2 | Unanimous | Unchanged | Unanimous |
| 9 | Document config_conditions as metadata-only | functional-typing | P2 | Bilateral (FT+IA) | Unchanged | Bilateral (FT+IA) |
| 10 | Add PRIOR_ARBITRATION_SECTION field documentation | integration-architect | P2 | Bilateral (IA+FT) | Unchanged | Bilateral (IA+FT) |
| 11 | Verify PRIOR_ARBITRATION_PATH path computation | integration-architect | P2 | Bilateral (IA+GEA) | Explicit formula specified | Bilateral (IA+GEA) |
| 12 | Use match/case for phase-specific validation | functional-typing | P2 | Solo (FT) | Upgraded to Unanimous (GEA confirmed R2) | Unanimous |
| 13 | Normalize ConfigCondition operators | game-engine-advocate | P3 | Solo (GEA) | Unchanged | Solo (GEA) |
| 14 | Reclassify ErrorType semantic misuses | functional-typing | P3 | Solo (FT) | Unchanged | Solo (FT) |
| 15 | Create ConversusConfig Pydantic model | FT + GEA | P3 | Bilateral (FT+GEA) | Unchanged | Bilateral (FT+GEA) |
| 16 | Add stagnation-influence interaction documentation | IA + GEA | P3 | Solo (IA) | game-engine-advocate endorses | Bilateral (IA+GEA) |
| 17 | Add PRIOR_ARBITRATION_PATH model_validator | FT + IA | P3 | Bilateral (FT+IA) | Unchanged | Bilateral (FT+IA) |
| 18 | Mark ARBITRATION_RULINGS as conditionally required | integration-architect | P3 | Solo (IA) | Unchanged | Solo (IA) |

**New in Round 2:**

| ID | Recommendation | Source | Priority | Consensus |
|----|---------------|--------|----------|-----------|
| 19 | Clarify static-vs-runtime boundary for influence_headings validation | functional-typing (cross-review of IA) | P2 | Unanimous |
| 20 | Template last-mile audit practice (manual) | All three (arbiter Consideration 1) | P2 | Unanimous |
| 21 | P2 sub-ordering: P2-easy vs. P2-structural | integration-architect | P2-meta | Unanimous |
| 22 | PHASE_CONTEXT_MODELS with Phase keys | functional-typing | P3 | Solo (FT) |

**Withdrawn (Round 1, maintained in Round 2):**
- Plugin hook comments in SKILL.md (game-engine-advocate R3)
- Influence dispatch externalization to schema/influence-levels.yml (game-engine-advocate R5)

---

## Dangerous Contradictions Found

**None.** No agent proposed a recommendation in Round 2 that would break or invalidate another agent's proposals. All Round 2 refinements are additive corrections to Round 1 positions. The SC1 boundary correction (static-vs-runtime for influence_headings) was a precision fix, not a contradiction -- it corrected the location of validation logic without changing the validation behavior.

---

## Systemic Contradictions

### SC1: Static Linting vs. Runtime Configuration (Refined in Round 2)

The Round 1 identification of this boundary was confirmed by the arbiter (AO-2) and re-applied in Round 2 to the P1 implementation. The influence_headings data enables runtime heading validation in the orchestrator but does not change static linter behavior. The linter continues to validate against binding-default headings. This boundary is now explicitly documented for the P1 implementation, preventing a future implementation error where someone attempts to push influence-level-aware validation into the static linter.

### SC2: config_conditions Schema Precision vs. Enforcement Gap (Unchanged)

The gap between declared config_conditions and enforced conditions remains. The arbiter (AO-3) confirmed the Principle IV grounding. The resolution (document as metadata-only, implement evaluation in a future spec) is unchanged from Round 1.

### SC3: Typed Pipeline vs. Template Last-Mile (Addressed in Round 2)

Round 1 identified this as a systemic blind spot. The arbiter (Consideration 1) elevated it to a standing practice recommendation. Round 2 produced three-agent convergence on the remedy: document a manual template last-mile audit practice, with a future linter --audit mode as an advisory automated check. This addresses the class of errors but does not fully resolve the systemic tension -- dead infrastructure can still accumulate between audit cycles.

---

## Convergence Achieved

All three agents converged on the following positions across two rounds:

1. **The influence-aware heading data gap is the top priority.** Universal P1 across both rounds. Round 2 settled the implementation: `dict[str, list[str]]` field type with string keys, YAML structure with recommended and advisory heading lists, binding headings served by existing `required_headings`, and clear static-vs-runtime validation boundary.

2. **Dead template variables must be connected.** Universal P1. Round 2 produced exact template text for both {ARBITRATION_PATHS} (conditional reading instruction) and {ARBITRATION_RULINGS} (pre-formatted arbiter rulings in Resolution Attribution).

3. **The Phase enum should be used consistently.** Upgraded from bilateral to unanimous in Round 2 when game-engine-advocate confirmed no objection. P2 items 4, 5, and 12 are now three-agent consensus.

4. **Provisional-resolution markers need lifecycle specification.** Universal P2. Round 2 settled the lifecycle: markers are round-scoped, re-opened disputes return to DISPUTES_BEGIN/DISPUTES_END, markers are marked as unstable per Principle II until validated by one spec.

5. **The static-vs-runtime validation boundary must be documented for influence_headings.** Universal P2. Round 2 produced the boundary specification: linter validates binding default; orchestrator validates influence-specific headings at runtime.

6. **Template last-mile audit should be a standing practice.** Universal P2. Immediate action: document the manual practice. Future: advisory automated linter check.

7. **P2 items benefit from sub-ordering.** Universal. P2-easy (documentation, path fixes) vs. P2-structural (type system, markers) enables incremental implementation.

8. **Backward compatibility is preserved.** Confirmed across both rounds and by the arbiter. Omitting `timing` and `influence` produces pre-spec-006 behavior.

9. **The spec does not block future extensibility.** game-engine-advocate's core finding sustained across both rounds. String-keyed influence_headings specifically accommodates plugin-defined influence levels.

10. **config_conditions are metadata-only until evaluation is implemented.** Universal P2 documentation action. Deferred evaluation to a future spec.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

No remaining disputes. All design questions have been resolved through agent convergence across two rounds of deliberation. The single minor dispute from Round 1 (config_conditions documentation sequencing, RD1) was resolved in Round 1 through integration-architect's concession, and the resolution held in Round 2 without challenge.

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1 -- Must Address

**1. Add influence_headings to ArbitrationConfig and cooperative.yml**
- Add `influence_headings: dict[str, list[str]] = Field(default_factory=dict)` to `ArbitrationConfig` in `linter/models.py`
- Add `influence_headings` section to `schema/modes/cooperative.yml`:
  ```yaml
  influence_headings:
    recommended:
      - Process Note
      - Decision Framework
      - Recommended Resolutions
      - Suggested Changes
    advisory:
      - Process Note
      - Decision Framework
      - Advisory Opinions
      - Considerations for Next Round
  ```
- Default `required_headings` serves as the `binding` headings (no duplication)
- Runtime heading validation in SKILL.md (L640-655) uses `influence_headings[level]` when non-binding, falls back to `required_headings` for binding
- Linter (static) continues to validate against `required_headings` -- does not use influence_headings
- Files: `linter/models.py`, `schema/modes/cooperative.yml`, SKILL.md L640-655 validation logic
- Source: All three agents, arbiter AO-1. Field type settled unanimously in Round 2.

**2. Wire {ARBITRATION_PATHS} into cross-round synthesis template**
- Add conditional reading instruction in "What to Read" section of `templates/cooperative/cross-round-synthesis.md`:
  ```markdown
  3. **Per-round arbitration resolutions** (if inter-round arbitration was configured):
  {ARBITRATION_PATHS}

  These contain the arbiter's positions from each round. Read them to attribute dispute resolutions accurately in the Resolution Attribution section.
  ```
- Files: `templates/cooperative/cross-round-synthesis.md`
- Source: integration-architect. Template text endorsed by all in Round 2.

**3. Wire {ARBITRATION_RULINGS} into cross-round synthesis template**
- Add in the Resolution Attribution section of `templates/cooperative/cross-round-synthesis.md`:
  ```markdown
  **Pre-formatted arbiter rulings across rounds:**

  {ARBITRATION_RULINGS}

  Use this content to attribute dispute resolutions. When the arbiter addressed a dispute, cite the specific round and ruling rather than summarizing from the round synthesis.
  ```
- Files: `templates/cooperative/cross-round-synthesis.md`
- Source: integration-architect. Template text endorsed by all in Round 2.

### P2 -- Should Address

**P2-easy (documentation and path fixes -- implement first):**

**4. Fix conversus.yml doc paths**
- Update game-engine-advocate docs from `specs/007-game-engine/` to `specs/archive/game-engine-vision/`
- Files: `specs/006-inter-round-arbitration/conversus.yml`
- Source: game-engine-advocate. Unanimous.

**5. Add PRIOR_ARBITRATION_SECTION field documentation**
- Add inline comment on `ReviewContext.PRIOR_ARBITRATION_SECTION` distinguishing it from `PRIOR_ARBITRATION_PATH`
- Files: `linter/models.py`
- Source: integration-architect. Bilateral (IA+FT).

**6. Specify PRIOR_ARBITRATION_PATH formula explicitly**
- Add: "Set `{PRIOR_ARBITRATION_PATH}` to `{output}/round-{R-1}/arbitration/resolution.md` when `arbiter.timing: inter-round` and arbitration fired in Round R-1. If arbitration did not fire in Round R-1, set to empty string."
- Files: `SKILL.md`
- Source: integration-architect. Bilateral (IA+GEA).

**7. Document config_conditions as metadata-only**
- Add comment block in `schema/variables.yml` header and in `linter/validate.py` noting that config_conditions are schema metadata for documentation and are not evaluated by the linter
- Files: `schema/variables.yml`, `linter/validate.py`
- Source: functional-typing. Bilateral (FT+IA). Arbiter AO-3 grounding.

**8. Document linter static-vs-runtime heading validation boundary (extended)**
- Add comment in `validate.py` `check_required_headings` explaining: arbitration heading validation is influence-unaware by design; runtime validation in SKILL.md handles influence-adjusted headings. Extended: the `influence_headings` field on ArbitrationConfig provides data for runtime validation, not linter validation.
- Files: `linter/validate.py`
- Source: integration-architect (original), functional-typing (extension). Unanimous.

**9. Document template last-mile audit practice**
- Add documentation noting: after adding a variable to variables.yml, verify at least one template in the corresponding phase references it. Automated linter --audit mode is a future enhancement (advisory, not blocking).
- Files: `linter/validate.py` (or separate documentation)
- Source: All three agents, arbiter Consideration 1. Unanimous.

**P2-structural (type system and marker changes -- implement second):**

**10. Use Phase enum in validate.py**
- Import `Phase` from `models.py`. Replace string literal phase comparisons with enum members. Type `phase` parameter as `Phase`.
- Files: `linter/validate.py`
- Source: functional-typing. Unanimous.

**11. Type VariableDefinition.phases as list[Phase]**
- Change `phases: list[str]` to `phases: list[Phase]`. Remove `validate_phases` field_validator.
- Files: `linter/models.py`
- Source: functional-typing. Unanimous.

**12. Use match/case for phase-specific validation**
- Refactor `check_required_headings` and `check_structural_markers` to use `match`/`case` with `Phase` enum.
- Files: `linter/validate.py`
- Source: functional-typing. Unanimous.

**13. Add structural markers for provisionally resolved disputes**
- Define `PROVISIONALLY_RESOLVED_BEGIN`/`PROVISIONALLY_RESOLVED_END` markers in the synthesis template
- Lifecycle: markers are round-scoped; re-opened disputes return to `DISPUTES_BEGIN`/`DISPUTES_END`
- Mark as unstable per Principle II until one spec has consumed them
- Files: `templates/cooperative/synthesis.md`, `SKILL.md`
- Source: integration-architect + game-engine-advocate. Unanimous.

### P3 -- Nice to Have

**14. Normalize ConfigCondition operators** -- game-engine-advocate. Solo.
**15. Reclassify ErrorType semantic misuses** -- functional-typing. Solo.
**16. Create ConversusConfig Pydantic model** -- FT + GEA. Bilateral.
**17. Add stagnation-influence interaction documentation** -- IA + GEA. Bilateral.
**18. Add PRIOR_ARBITRATION_PATH model_validator** -- FT + IA. Bilateral.
**19. Mark ARBITRATION_RULINGS as conditionally required** -- integration-architect. Solo. Deferred.
**20. PHASE_CONTEXT_MODELS with Phase keys** -- functional-typing. Solo.

---

## Dispute Trajectory

| Dispute | Round Appeared | Round Resolved | Resolution Mechanism |
|---------|---------------|----------------|---------------------|
| config_conditions sequencing (RD1) | Round 1 | Round 1 | integration-architect conceded; documentation-first approach adopted |

No new disputes appeared in Round 2. The single Round 1 dispute resolution held without challenge.

---

## Convergence Progression

**Round 1 convergence**: 7 positions agreed unanimously, 18 total recommendations (3 P1, 9 P2, 6 P3), 2 withdrawn, 1 dispute resolved through concession.

**Round 2 convergence**: 10 positions agreed unanimously. Upgrades from Round 1:
- P2 items 4, 5, 12 (Phase enum, VariableDefinition.phases, match/case): bilateral -> unanimous
- P2 item 7 (provisional markers): lifecycle design settled, three-agent convergence
- 3 new P2 items: SC1 boundary for influence_headings, template last-mile audit, P2 sub-ordering
- 1 new P3 item: PHASE_CONTEXT_MODELS with Phase keys
- Zero new disputes

**Net change**: +3 items upgraded to unanimous, +4 new items, 0 new disputes, 0 re-opened disputes.

---

## Resolution Attribution

- **config_conditions sequencing**: Resolved by agent convergence (Round 1). integration-architect conceded to functional-typing's documentation-first approach.
- **Phase enum priority**: Resolved by agent convergence (Round 1). functional-typing downgraded from P1 to P2. Unanimity achieved in Round 2 via game-engine-advocate confirmation.
- **ErrorType reclassification priority**: Resolved by agent convergence (Round 1). functional-typing downgraded from P2 to P3.
- **Plugin hook comments**: Resolved by withdrawal (Round 1). game-engine-advocate withdrew based on integration-architect's SKILL.md executable spec argument.
- **Influence dispatch externalization**: Resolved by withdrawal (Round 1). game-engine-advocate withdrew based on YAGNI and own OBA-1 self-correction.
- **Heading validation approach (Option A vs B)**: Resolved by agent convergence (Round 1). game-engine-advocate revised from Option B to Option A.
- **influence_headings field type**: Resolved by agent convergence (Round 2). All three agents independently converged on `dict[str, list[str]]` with string keys.
- **Provisional-resolution marker lifecycle**: Resolved by agent convergence (Round 2). All three agents converged on round-scoped markers.
- **SC1 boundary for influence_headings**: Resolved by agent convergence (Round 2). functional-typing identified the precision issue; integration-architect accepted the correction.

---

## Key Concessions

**Round 1 concessions (maintained in Round 2 -- not reversed):**

1. **functional-typing**: Downgraded Phase enum from P1 to P2; downgraded ErrorType reclassification from P2 to P3.
2. **game-engine-advocate**: Withdrew plugin hook comments and influence dispatch externalization; revised from Option B to Option A for heading validation.
3. **integration-architect**: Conceded on config_conditions sequencing (documentation-first).

**Round 2 concessions:**

4. **integration-architect**: Accepted functional-typing's SC1 boundary correction on influence_headings validation. The original statement "the linter's heading validation should use influence_headings[level]" was corrected to specify that runtime orchestrator validation (not linter validation) uses influence_headings.
5. **game-engine-advocate**: Reclassified "P1-design" recommendation to a design constraint within P1 item 1 (per integration-architect's labeling feedback).
6. **functional-typing**: Adopted template last-mile audit practice (per arbiter Consideration 1 and co-reviewer feedback about the blind spot in type-system-focused reviews).

---

## Termination Assessment

**Was termination appropriate?** Yes. Round 2 produced zero new disputes and resolved all remaining design questions. The deliberation has achieved full convergence.

**Would additional rounds have been productive?** No. All P1 items are implementation-ready. All P2 design questions are settled. The remaining P3 items are correctly deferred and do not require further deliberation.

**Recommendation for future deliberations**: The template last-mile audit practice should be included in future reviews as a standard final check. The three agents identified complementary blind spots: functional-typing focused on the type system layer, game-engine-advocate on extensibility architecture, integration-architect on the integration pipeline. Each missed what the others caught. The three-perspective composition is effective; the last-mile audit closes the remaining gap.
