# Phase 4 Disputes: spec-compliance

**Spec**: 026-optimization-template-library

---

## Remaining Disputes

### DISPUTE 1: Cross-reference validation gaps (Low)

**Status**: Surviving -- all three agents flag this as the primary actionable gap.

Three parallel cross-reference validation gaps exist in the test suite:

1. **game_form cross-validation**: Template `game_form` values are not checked against `schema/game-forms/*.yml`. A template with `game_form: "nonexistent"` passes all tests.
2. **mode_compatibility cross-validation**: Template `mode_compatibility` values are not checked against valid mode names. A template with `mode_compatibility: ["fake-mode"]` passes all tests.
3. **Constraint gap_question enforcement**: The `TestGapQuestions` class only tests objective templates. Constraint template parameters with gap_question fields are not enforced by tests.

These are test coverage gaps, not implementation gaps. All current values are valid. The tests do not enforce the invariants that keep them valid.

**Recommended resolution**: Three additional parametric tests, ideally bundled into a single work item:
1. `test_game_form_references_valid_game_form_file` -- cross-reference against game-forms directory
2. `test_mode_compatibility_values_are_valid_modes` -- cross-reference against mode-mapping
3. `TestConstraintGapQuestions` -- mirror of `TestGapQuestions` for constraint templates

**Agent consensus**: Unanimous across all three agents.

---

## Withdrawn Disputes

- **SC-004 PARTIAL assessment**: Revised to PASS in Phase 1, confirmed unanimously in Phase 3. Not a dispute.
- **PSD and supply-demand validation**: Correctly deferred to solver layer by all agents. Not a dispute.
- **SC-005 solver testing**: Acknowledged as deferred to spec 023. High mathematical confidence from optimization-engineer, but formal testing still required. Not a dispute between agents -- all agree it needs testing, and all agree it's spec 023's responsibility.
- **form field semantic validation**: Info. Depends on expert review. Not a dispute.

---

## Convergence

- **FR-001 through FR-006 verdict**: Unanimous. 5 pass, 1 not assessed (FR-004 deferred to spec 014). No agent disputes any FR verdict.
- **SC-001 through SC-004 verdict**: Unanimous PASS. SC-004 converged from PARTIAL to PASS during Phase 1-3.
- **SC-005 verdict**: Unanimous NOT TESTED. Correctly deferred to spec 023.
- **Overall verdict is PASS**: Unanimous across all three agents from all four phases. The template library expansion meets all assessable requirements.
- **Sole surviving dispute is Low-severity test coverage**: All three agents converge on the same set of test improvement recommendations. No agent-to-agent disagreements remain.
