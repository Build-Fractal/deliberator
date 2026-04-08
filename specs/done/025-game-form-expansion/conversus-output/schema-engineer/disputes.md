# Phase 4 Disputes: schema-engineer

**Spec**: 025-game-form-expansion

---

## Surviving Disputes

### DISPUTE 1: BayesianGame prior key validation (Medium)

**Status**: Surviving -- consensus across agents that this is a real gap.

The BayesianGame model accepts any string keys in the `prior` dict as long as probabilities sum to 1.0. This allows semantically invalid games to pass validation. The fix is straightforward: compute the Cartesian product of type_spaces values and verify all prior keys are valid type profile tuples.

### DISPUTE 2: SC-005 game form count threshold (Low)

**Status**: Surviving -- spec says >= 10, implementation has 9.

This is a spec clarification issue. The potential game diagnostic is not a form (per FR-004), so counting it would contradict the spec's own requirement. Either the spec threshold should be amended to >= 9, or one additional game form should be added.

## Withdrawn Disputes

- Duplicate VALID_FIELD_TYPES entry: Not a dispute -- cosmetic fix, all agree
- PotentialGame naming: Withdrawn
- Discriminated union type: Deferred to future work, not a dispute
