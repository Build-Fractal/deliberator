# Phase 4 Disputes: schema-engineer

**Spec**: 026-optimization-template-library

---

## Remaining Disputes

### DISPUTE 1: Cross-reference validation for game_form and mode_compatibility (Low)

**Status**: Surviving -- consensus across all three agents.

Template `game_form` and `mode_compatibility` values are not cross-referenced against their respective source YAML files. Two additional parametric tests would close this gap:
1. `game_form` -> `schema/game-forms/*.yml` existence check
2. `mode_compatibility` entries -> valid mode names check

**Note on severity convergence**: I originally rated `mode_compatibility` validation as Info (SE-3). During Phase 3 revision, I upgraded to Low based on the spec-compliance agent's consistency argument: structurally identical gaps should carry consistent severity. All three agents now agree on Low for both sub-items.

**Agent consensus**: Unanimous.

### DISPUTE 2: Constraint template gap_question test coverage (Low)

**Status**: Surviving -- consensus across all three agents.

The `TestGapQuestions` class only covers objective templates. Constraint templates with parameterized gap_questions (e.g., `flow-conservation.supply_demand`, `integrality.variable_type`) are not tested. A `TestConstraintGapQuestions` class would enforce this invariant.

**Agent consensus**: Unanimous (identified by spec-compliance, adopted by all in Phase 3).

---

## Withdrawn Disputes

- **Constraint count fragility (SE-1)**: Info observation. The exact-threshold test is correct per SC-002. Defense-in-depth is provided by `TestTemplateConstraintReferences`. Not a dispute.
- **Constraint-template semantic alignment (SE-5)**: Info. Depends on manual mathematical review. Not automatable. Not a dispute.

---

## Convergence

- **Template schema compliance is complete**: Unanimous from Phase 1. No agent found any schema violation.
- **gap_question coverage is complete for objective templates**: Unanimous. All non-derived parameters have gap_question fields.
- **Constraint references are all valid**: Unanimous. Verified by both automated tests and manual audit.
- **SC-004 is PASS at spec 026's scope**: Unanimous after Phase 3. Templates provide valid examples; assembly is spec 014's concern.
- **Overall verdict is PASS**: Unanimous. All concerns are Low or Info.
