# Phase 3 Revision: spec-compliance

**Spec**: 025-game-form-expansion

---

## Position Changes After Cross-Review

### Modified: FR-004 verdict -- UPGRADED from PARTIAL to PASS

Both the game-theorist and schema-engineer argue that the PotentialGame Pydantic model is a result container, not a game form. I accept this interpretation. The check functions `is_potential_game()` and `compute_potential()` are the actual diagnostic implementation. The PotentialGame model stores diagnostic results and does not participate in mode mapping or template routing.

**Revised verdict**: FR-004 PASS.

### Modified: SC-005 -- CLARIFIED as SPEC DISCREPANCY

The spec says `len(game_forms) >= 10`. The implementation has 9 YAML schemas (excluding potential, which is a diagnostic). The test threshold is >= 9, which matches the implementation. This is a discrepancy between spec text and what's achievable given the spec's own assertion that potential is not a form.

**Resolution options**:
(a) Count potential as a form in the YAML directory -> reaches 10 (but contradicts FR-004)
(b) Add one more game form (e.g., evolutionary game or mean-field game) -> reaches 10
(c) Amend spec to say >= 9

I recommend (c) -- amend the spec threshold. The implementation covers all forms described in spec section 2.

### Surviving: SC-003 and SC-004 NOT TESTED

These remain correctly deferred to Tier 2 solver integration. No position change.

### New: YAML example round-trip coverage should be credited

The game-theorist's cross-review notes that I did not credit the YAML example validation tests. Each new model has a `test_yaml_example_validates` test that loads the YAML schema's `example` field and validates it against the Pydantic model. This is valuable regression coverage and should be acknowledged.

**Revised assessment**: The test suite exceeds FR-011 requirements by also covering YAML-to-Pydantic round-trips.
