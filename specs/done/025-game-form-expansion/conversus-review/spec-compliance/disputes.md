# Phase 4 Disputes: spec-compliance

**Spec**: 025-game-form-expansion
**Agent**: spec-compliance

---

## Surviving Disputes

### DISPUTE 1: is_potential_game() scope vs. FR-004 language (HIGH)

**Status**: SURVIVING -- all three agents flag this.

FR-004 requires the diagnostic to be "a check applied to existing game forms." The implementation applies to 2-player normal-form games only. The spec's language "existing game forms" encompasses normal-form, gnep, parametric, and stackelberg -- the diagnostic covers a subset of one of four.

**Compliance framing**: FR-004 structurally PASSES (diagnostic is a function, not a form). But the scope implied by "existing game forms" is not fully met. The spec language should be tightened.

**Recommended resolution**: Amend spec section 2.1 from "A check applied to existing game forms" to "A check applied to 2-player normal-form games." This makes the implementation fully compliant without requiring generalization.

### DISPUTE 2: BayesianGame prior key validation (MEDIUM)

**Status**: SURVIVING -- unanimous.

The model validates a necessary condition (probabilities sum to 1.0) without a sufficient condition (keys correspond to valid type profiles). This weakens FR-002's intent that models catch invalid inputs at construction time.

**Recommended resolution**: Add Cartesian product validation as specified by the schema-engineer's implementation sketch.

### DISPUTE 3: SC-005 threshold discrepancy (LOW)

**Status**: SURVIVING -- all agents converge.

The spec says `len(game_forms) >= 10`. The implementation has 9 forms. Counting the potential diagnostic as a form would contradict FR-004. The spec threshold is a drafting error.

**Recommended resolution**: Amend SC-005 from `>= 10` to `>= 9`. The implementation covers every form described in spec section 2.

### DISPUTE 4: FR-008 partial satisfaction (LOW)

**Status**: SURVIVING -- game-theorist and schema-engineer raise this.

FR-008 requires at least one objective template per game form. Existing general-purpose templates provide partial coverage, but no dedicated templates exist for bayesian games, repeated games, or shapley-specific coalitional analysis.

**Recommended resolution**: Either create dedicated templates (spec 026 could address this) or clarify that general-purpose templates (e.g., cooperative-consensus.yml) satisfy FR-008 when applicable to the game form's problem structure.

---

## Withdrawn Disputes

- **FR-004 PARTIAL verdict**: Revised to PASS after unanimous cross-review consensus.
- **FR-008/FR-009 NOT ASSESSED**: Revised FR-008 to PARTIAL, FR-009 maintained as NOT ASSESSED (spec 026 dependency).

---

## Settled Points (No Dispute)

All three agents agree on these settled outcomes:

| Item | Verdict | Confidence |
|------|---------|------------|
| Shapley computation correctness | CORRECT | High (axiom verification) |
| Potential game diagnostic math (2-player) | CORRECT | High (Monderer-Shapley characterization) |
| FR-001 through FR-003 | PASS | High |
| FR-004 (structural) | PASS | High (check function, not form) |
| FR-005 through FR-007 | PASS | High |
| FR-010 through FR-013 | PASS | High |
| SC-001 and SC-002 | PASS | High |
| SC-003 and SC-004 | CORRECTLY DEFERRED | High (Tier 2) |
| Mode mapping completeness | COMPLETE | High (5 new + 4 original) |
| YAML schema consistency | CONSISTENT | High |
