# Conversus Review Synthesis — Spec 024: Cross-Plugin Interfaces

**Spec**: 024-cross-plugin-interfaces
**Round**: 1 (Final)
**Date**: 2026-04-01
**Reviewers**: plugin-architect, solver-engineer, spec-compliance

---

## Verdict

**PARTIAL PASS** — The plugin framework (declarations, topological sort, orchestration, graceful degradation) is correctly implemented and all functional requirements are MET. The motivating use case (3D Kalman prediction from equilibrium scores) is wired but delivers unrealized quality benefit due to data history limitations and sentinel bugs. SC-001 is PARTIAL; all other SCs are MET.

---

## Success Criteria Status

| Criterion | Verdict | Notes |
|-----------|---------|-------|
| SC-001 | **PARTIAL** | Wiring correct; quality benefit unrealized (single-element history, zero-score gate) |
| SC-002 | **MET** (caveat) | Absent-scorer fallback works; zero-score fallback validates wrong behavior |
| SC-003 | **MET** | Topological sort guarantees scorer before predictor |
| SC-004 | **MET** | Cycle detection with clear error message |
| SC-005 | **MET** | Undeclared plugins preserve declaration order |

---

## Consensus Findings (All Three Reviewers Agree)

### P1 — Critical

**1. Accumulate equilibrium scores across rounds.**
The predictor receives only the current round's score and wraps it in a single-element list. Prior rounds' scores are lost. The `_equilibrium_trend` function always returns 0.0, and the 3D Kalman filter receives the same score replicated across all historical rounds, creating a false constant-score prior that artificially shrinks covariance.
- Files: `predictor.py:255-261`, `base.py` (DeliberationState or execute_hooks)
- Fix: Persist eq_scores in a round-indexed structure across hook invocations. Options: extend `RoundState`, plugin-local accumulator, or cumulative `plugin_results` history.

**2. Fix the zero-score sentinel gate.**
`any(s != 0.0 for s in equilibrium_scores)` conflates "scorer absent" with "score equals zero." A legitimate score of 0.0 (no agents at equilibrium) is meaningful data that should trigger 3D, not fall back to 2D. The correct sentinel is `None`.
- File: `convergence.py:268-271`
- Fix: Replace with `equilibrium_scores is not None and len(equilibrium_scores) > 0`.
- Add **SC-006**: When EquilibriumScorer produces `equilibrium_score = 0.0`, ConvergencePredictor MUST use 3D observations.

### P2 — Important

**3. Add duplicate-producer detection with `DuplicateProducerError`.**
Two plugins declaring the same `produces` key silently overwrites in the `producers` dict. Raise a dedicated `DuplicateProducerError` (not `PluginDependencyCycleError`) when collisions are detected at sort time.
- File: `base.py:333-336`

**4. Harden `run_kalman_filter` default Q/R to auto-size from observation dimension.**
`default_Q()` and `default_R()` always return 2x2. The current caller (`_predict_convergence_kalman`) passes explicit 3x3, so this is not actively triggered. But the API is defective: any future caller omitting Q/R with 3D data gets silent dimension mismatch. Auto-size defaults from `len(observations[0])`.
- File: `kalman.py:372-376`

**5. Add 3D Kalman end-to-end test.**
No test feeds 3+ rounds of 3D observations through the actual Kalman filter and verifies state dimension, confidence bounds, and convergence behavior. Integration tests cover data flow plumbing but not numerical correctness.
- File: `tests/test_cross_plugin.py` (new test class)

**6. Calibrate 3D observation noise R for eq_score dimension.** *(solver-engineer recommendation)*
`R[2][2] = 0.005` trusts eq_score as much as concession_rate despite compounding multiple noise sources. Recommended: `R[2][2] = 0.05` (10x concession noise). Expose as config parameter.
- File: `convergence.py:339-343`

**7. Validate 3D superiority with innovation magnitude diagnostic.** *(plugin-architect + solver-engineer)*
The spec assumes 3D improves predictions. Eq_score may partially duplicate concession_rate signal, inflating confidence without improving accuracy. Log innovation magnitude ratio (3D/2D) to empirically validate the claim before shipping 3D as default.

**8. Add cross-hook plugin_results scoping test + docstring.** *(compromise)*
`plugin_results` is reset per hook invocation. This behavior is load-bearing but undocumented. Add a dedicated test verifying the reset and a prominent docstring note. (Compromise between plugin-architect's FR-011 and spec-compliance's docstring-only approach.)
- File: `base.py:401` (docstring), `tests/test_cross_plugin.py` (new test)

**9. Update spec section 8 text.**
Section 8 states "This spec does NOT implement the orchestration layer (#6/ORC)" but the implementation wires orchestration in `execute_hooks`. Update spec to reflect that minimal orchestration was implemented inline.
- File: `spec.md`, section 8

### P3 — Enhancement

**10. Enforce immutable types for produced values.**
`model_copy` is shallow; mutable values (lists, dicts) in `plugin_results` can leak mutations across consumers. Current values are all immutable (floats, strings). Add runtime type enforcement rejecting mutable containers in produced `result.data` values.
- File: `base.py:474-477`

**11. Log warning when a plugin declares `produces` but omits the key from `result.data`.**
Silent contract violation. A debug-level log would catch integration mistakes early.
- File: `base.py:474-477`

**12. Joseph form covariance update for numerical stability.** *(solver-engineer)*
The current `P_post = (I - K*H) * P_pred` loses symmetry/positive-definiteness over many iterations. The Joseph form is algebraically equivalent but numerically stable. More important in 3D where off-diagonal terms accumulate error.
- File: `kalman.py:337-339`

**13. Tune 3D initial covariance for eq_score dimension.** *(solver-engineer)*
Initial P variance of 1.0 for eq_score is too wide for a [0,1] range. Recommended: 0.25 (std = 0.5).
- File: `kalman.py:380`

**14. Update stale docstrings referencing "2D" in convergence.py and kalman.py.** *(solver-engineer)*
- Files: `convergence.py:703-704`, `kalman.py:1-25`

---

<!-- DISPUTES_BEGIN -->

## Resolved Disputes

All disputes from Phase 3 were resolved by Phase 4:

1. **SC-001 verdict**: All three revised to PARTIAL. Resolved.
2. **Q/R severity**: All three agreed on P2 (latent API defect). Resolved.
3. **Cross-hook lifetime mechanism**: Plugin-architect proposed FR-011; spec-compliance proposed docstring only. Compromise: test + docstring (item 8 above). Resolved.
4. **Noise calibration scope**: Solver-engineer accepts it is outside compliance scope; spec-compliance accepts it belongs in synthesis. Recorded as solver-engineer recommendation (item 6). Resolved.
5. **Masked observation approach timing**: Solver-engineer accepts accumulation first; masked approach deferred to follow-up. Resolved.
6. **Duplicate producer error type**: All agreed on dedicated `DuplicateProducerError`. Resolved.
7. **Self-nesting pattern**: Plugin-architect acknowledges P3 design preference, will not escalate. Deferred to future spec. Resolved.

**No active disputes remain.**

<!-- DISPUTES_END -->

---

## Review Termination

All disputes from Round 1 are resolved. No Round 2 is needed. The review terminates with the consensus findings above.

---

## Referenced Files

| File | Topic |
|------|-------|
| `specs/024-cross-plugin-interfaces/spec.md` | Primary spec |
| `conversus/plugins/base.py` | Plugin ABC, topological sort, execute_hooks |
| `conversus/plugins/nashopt/scorer.py` | EquilibriumScorer (produces equilibrium_score) |
| `conversus/plugins/nashopt/predictor.py` | ConvergencePredictor (consumes equilibrium_score) |
| `conversus/plugins/nashopt/convergence.py` | 2D/3D observation building, Kalman prediction |
| `conversus/plugins/nashopt/kalman.py` | Kalman filter core, matrix ops, defaults |
| `conversus/plugins/optimizer/optimizer.py` | ConfigOptimizer (produces optimal_config) |
| `conversus/plugins/scenarios/plugin.py` | ScenarioPlugin (consumes equilibrium_score, optimal_config) |
| `tests/test_cross_plugin.py` | Cross-plugin test suite |
