# Phase 4 Disputes: schema-engineer

**Spec**: 025-game-form-expansion
**Agent**: schema-engineer

---

## Surviving Disputes

### DISPUTE 1: BayesianGame prior key validation (MEDIUM)

**Status**: SURVIVING -- unanimous across all three agents.

The BayesianGame model accepts arbitrary string keys in the `prior` dict. The only validation is that values sum to 1.0 (within 1e-6 tolerance). This allows semantically invalid games to pass construction:

```python
# This passes all validators despite meaningless keys:
BayesianGame(
    type_spaces={"p1": ["H", "L"], "p2": ["H", "L"]},
    prior={"foo": 0.5, "bar": 0.5},
)
```

**Recommended resolution**: Add Cartesian product validation in the model_validator. Implementation sketch provided in my Phase 3 revision.

### DISPUTE 2: SC-005 game form count threshold (LOW)

**Status**: SURVIVING -- schema-engineer and spec-compliance agree; game-theorist concurs.

The spec says `len(game_forms) >= 10`. Implementation has 9 YAML schemas. The 10th "form" would be the potential diagnostic, but FR-004 explicitly says potential is not a form. The spec threshold is inconsistent with its own FR-004 requirement.

**Recommended resolution**: Amend spec SC-005 from `>= 10` to `>= 9`.

### DISPUTE 3: FR-008 partial satisfaction (LOW)

**Status**: SURVIVING -- schema-engineer and game-theorist identify the gap.

FR-008 requires "each game form MUST have at least one objective template." Existing general-purpose templates cover some new forms implicitly (cooperative-consensus for coalitional, territory-claiming for congestion), but no dedicated templates exist for bayesian, repeated, or coalitional (shapley-specific) forms.

**Recommended resolution**: Create at minimum one dedicated objective template per new game form, or amend FR-008 to allow general-purpose templates to satisfy the requirement.

---

## Withdrawn Disputes

- **PotentialGame naming**: Withdrawn. Style preference, no compliance impact.
- **Discriminated union type**: Not a dispute -- deferred design recommendation.
- **Duplicate VALID_FIELD_TYPES**: Not a dispute -- cosmetic fix, all agree.

---

## Settled Points (No Dispute)

- Model architecture patterns: EXCELLENT (all agents agree)
- Validator completeness: GOOD with one known gap (BayesianGame prior keys)
- YAML schema structure: CONSISTENT
- Mode mapping: COMPLETE
- YAML-Pydantic round-trip tests: STRONG consistency guarantee
- Type safety: GOOD (appropriate Literal types, dict typing, Optional usage)
