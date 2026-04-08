# Phase 3 Revision: game-theorist

**Spec**: 025-game-form-expansion

---

## Position Changes After Cross-Review

### Modified: Concern #1 (is_potential_game 2-player limitation) -- UPGRADED to High

The spec-compliance agent argues this should be High rather than Medium, and I concur. The spec states the diagnostic applies to "existing game forms" which include N-player games. The current implementation only handles 2-player bimatrix games. I accept the spec-compliance agent's recommendation: document the 2-player restriction rather than attempt N-player generalization (which is research-grade complexity).

**Revised recommendation**: Add a clear docstring note: "This diagnostic currently supports 2-player normal-form games only. N-player potential game detection requires payoff gradient field integrability checking, which is deferred."

### Modified: Concern #2 (BayesianGame prior key validation) -- UPGRADED to Medium

Both the schema-engineer and I flagged this independently. The schema-engineer rated it Info; I originally rated it Low. After reflection, I upgrade to Medium because invalid prior keys produce a silently valid model that would fail at solver time with confusing errors.

**Revised recommendation**: Add a validator that checks prior keys are valid type profile tuples from the Cartesian product of type_spaces values.

### Surviving: Concern #3 (MechanismDesignGame sparseness) -- MAINTAINED at Low

Both cross-reviewers agree this is acceptable for the current stage. The schema-engineer correctly notes that adding fields with no validator or solver to consume them would be speculative. I maintain Low severity.

### Withdrawn: Concern #4 (v(empty) = 0 convention)

The schema-engineer's cross-review notes that the solver handles this implicitly via `cf.get(coalition_key, 0.0)`. Since the solver code defaults missing keys to 0.0, and the empty coalition key "" would default to 0.0 if absent, the convention is effectively enforced. Withdrawing this concern.

### Surviving: Concern #5 (Congestion game missing cost_functions)

Maintained as Info. Both reviewers agree this is acceptable for schema-only validation.
