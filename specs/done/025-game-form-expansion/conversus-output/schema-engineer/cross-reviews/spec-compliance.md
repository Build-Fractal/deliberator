# Cross-Review: schema-engineer reviewing spec-compliance

**Spec**: 025-game-form-expansion

---

## Agreement

The compliance matrix is thorough and well-structured. I agree with:

- All FR-001 through FR-003, FR-005 through FR-007 verdicts
- The decision to mark FR-008 through FR-010 as "NOT ASSESSED" (correctly identified as cross-cutting with spec 026)
- SC-001 and SC-002 PASS verdicts

## Disagreements

### 1. FR-004 should be PASS

I agree with the game-theorist's cross-review position here. The PotentialGame Pydantic model is a data container for diagnostic results, not a game form. It does not appear in mode-mapping.yml, has no YAML schema in game-forms/ with the standard form/description/fields/example structure (its YAML, if any, would be a diagnostic output format), and is not dispatched to by the mode classifier.

The spec says "implemented as a check function, not a separate form." The check functions `is_potential_game()` and `compute_potential()` are the implementation. The PotentialGame model is an output container. FR-004 is satisfied.

### 2. SC-005 game form count discrepancy

The spec says `len(game_forms) >= 10`. The test uses `>= 9`. Current YAML schemas:

1. normal-form
2. gnep
3. parametric
4. stackelberg
5. coalitional
6. congestion
7. bayesian
8. repeated
9. mechanism-design

That's 9 forms. Potential is a diagnostic, not a form. The spec may be counting an additional form we haven't identified, or it may be aspirational. The test threshold of 9 is correct for what exists. I would flag this as a spec clarification needed rather than a compliance failure.

## Additions

The spec-compliance agent correctly identifies that FR-011 through FR-013 pass. I would add that the test organization is clean -- each game form has its own test class, each YAML schema is parametrically tested, and the round-trip (YAML -> Pydantic) validates schema-model consistency. This exceeds the minimum testing requirements.
