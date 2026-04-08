# Cross-Review: game-theorist reviewing spec-compliance

**Spec**: 025-game-form-expansion

---

## Agreement

The spec-compliance agent's FR-by-FR assessment is thorough and accurate. I agree with the PASS verdicts on FR-001 through FR-003, FR-005 through FR-007, and FR-011 through FR-013. The observation that SC-003 and SC-004 are correctly deferred to Tier 2 is consistent with the spec's phased approach.

## Disagreements

### 1. FR-004 should be PASS, not PARTIAL

The spec-compliance agent marks FR-004 as PARTIAL because `PotentialGame` exists as a Pydantic model alongside game forms. However, the spec says "diagnostic MUST be implemented as a check function, not a separate form." The implementation satisfies this:

- `is_potential_game()` and `compute_potential()` are pure functions (the diagnostic)
- `PotentialGame` is a result model that stores diagnostic output

The PotentialGame model does not participate in mode mapping, does not have a YAML schema in the game-forms directory with the same structure as game forms, and is not routed to by the mode classifier. Its existence as a data model does not violate the "not a separate form" requirement. FR-004 should be **PASS**.

### 2. SC-005 assessment is too conservative

The spec-compliance agent says SC-005 is "PARTIAL" because the test threshold is >= 9 instead of >= 10. But the spec says "len(game_forms) >= 10" and the existing forms (normal-form, gnep, parametric, stackelberg) plus new forms (coalitional, congestion, bayesian, repeated, mechanism-design) = 9. The potential diagnostic is explicitly not a form, so the count is 9, not 10. Either the spec overcounts (including potential as a form) or there's one more form expected. This is a genuine discrepancy between spec and implementation that should be documented.

## Additions

The spec-compliance agent did not assess whether the YAML schemas include the `example` field that validates against the corresponding Pydantic model. The test suite does check this (`test_yaml_example_validates` in each test class), so this is covered but not credited in the compliance matrix.
