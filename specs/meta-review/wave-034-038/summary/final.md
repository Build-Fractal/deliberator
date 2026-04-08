# Meta-Review Final Synthesis — Specs 034-038

**Date**: 2026-04-01
**Deliberation**: 4 auditors, single-pass meta-review
**Specs reviewed**: 034, 035, 036, 037, 038
**Per-spec files read**: All rounds (Round 1 only — all specs converged in Round 1)

---

## 1. Process Summary

Four auditors reviewed five spec synthesis documents from specs 034-038:

| Auditor | Scope | Key Method |
|---|---|---|
| **consistency-auditor** | Cross-spec contradictions, shared interfaces, REQUIRED-ELSEWHERE validity | Side-by-side synthesis comparison + code inspection |
| **implementation-verifier** | Synthesis claim accuracy against actual code (3 claims/spec) | Line-by-line code verification of 15 claims |
| **dependency-auditor** | Import boundaries, architectural layering, data flow chains | Import graph analysis across all reviewed files |
| **test-coverage-auditor** | Test coverage of P1 findings, SC test presence | Test file analysis against synthesis claims |

---

## 2. Recommendation Scorecard

### P1 — Must Address

| ID | Spec | Recommendation | Auditor Agreement |
|---|---|---|---|
| RE-1 | 034 | Add Q/R dimension assertion at `run_kalman_filter` entry | 4/4 (crash prevention) |
| PAYOFF-NEW | 038 | Create spec for payoff functions for 4 new modes | 4/4 (scorer silently fails) |

### P2 — Should Address

| ID | Spec | Recommendation | Auditor Agreement |
|---|---|---|---|
| M-2 | 035 | Write cross-hook scoping test (plugin_results isolation) | 4/4 |
| RE-2 | 038 | Write spec 021 amendment for WTA matrix shape (N x 1 -> N x N) | 4/4 |
| M-1 | 034 | Verify/write 3D e2e test with mathematical property checks | 3/4 |
| C-3-TEST | 034 | Verify test_2d_with_all_zero_eq_scores was inverted | 3/4 |
| ENGINE-1 | 034 | Verify engine persists plugin_results into RoundState | 3/4 |

### P3 — Nice to Have

| ID | Spec | Recommendation |
|---|---|---|
| NEW-3 | 038 | Update spec 024 section 8 text |
| D-5 | 036 | Amend spec 028 Section 2.1 text |
| NEW-6 | 034 | Joseph form covariance update (acceptable for max-5-round) |
| TIE-BREAK | 036 | Document classification tie-breaking bias |
| SOLVER-STATUS | 037 | Constrain solver_status to Literal (Phase 3) |

---

## 3. Cross-Spec Impact Check

### Impact 1: Missing payoff functions (P1)

**Source**: Spec 038 game-theorist F-4
**Affects**: Specs 017, 021, 028, 034

The `PAYOFF_FUNCTIONS` dict in payoffs.py covers only 4 modes. The EquilibriumScorer (spec 017/021) calls `compute_payoff()` which raises `ValueError` for new modes. The outer exception handler in scorer.py catches this and returns a partial error result.

**Chain effect**: When the scorer fails, it does not emit `equilibrium_score`. The ConvergencePredictor (spec 034) receives None for the current round's eq_score and falls back to 2D Kalman. This is graceful degradation but means convergence prediction is weaker for 4 of 8 modes.

**Not caught by any per-spec review**: Each spec review examined its own files and found no issues. The gap exists at the intersection of spec 028 (added modes) and spec 017/021 (scoring). Only the meta-review's cross-spec analysis identified this.

### Impact 2: WTA matrix shape (P2)

**Source**: Spec 038 RE-2
**Affects**: Specs 017, 021

The N x 1 WTA matrix produces trivial equilibria. The equilibrium scorer always reports 1.0 for WTA mode. This means the ConvergencePredictor's eq_score dimension is always 1.0 for WTA mode, which provides no useful signal to the Kalman filter.

**Not blocking**: WTA mode's primary convergence signal is the dispute count and concession rate (2D path), not equilibrium quality. The eq_score dimension adds minimal value for WTA.

### Impact 3: Engine persistence assumption (P2)

**Source**: Spec 034 integration-engineer F-4
**Affects**: Spec 034 SC-001

The ConvergencePredictor's eq_score accumulation depends on the engine persisting `plugin_results` into `RoundState.plugin_results` after each round. If the engine does not do this, historical eq_scores are all None, and the predictor falls back to 2D Kalman for all modes. This is a spec 034 -> engine dependency.

---

## 4. Dropped Items Table

| Per-Spec Finding | Original Priority | Meta-Review Status | Reason |
|---|---|---|---|
| Spec 034 F-6 (Joseph form) | P3 | DEFERRED | Acceptable for max-5-round constraint |
| Spec 034 Q/R passthrough from plugin config | P3 | DEFERRED | Auto-sizing handles all real-world usage |
| Spec 034 None carry-forward documentation | P3 | DEFERRED | Modeling decision, not a bug |
| Spec 035 sentinel for missing produces | WITHDRAWN | DROPPED | Over-engineering (safety-engineer conceded) |
| Spec 035 required vs. optional plugins flag | P3 | DEFERRED | Belongs in spec 016 scope |
| Spec 035 _find_plugin_class first-match risk | P3 | DEFERRED | Document in spec 016 |
| Spec 036 RE-5 empirical template testing | P3 | TRACKED | Operational task |
| Spec 037 solver_status Literal | P3 | DEFERRED | Phase 3 solver integration |

**No P1 findings were dropped.** All P1 items appear in the recommendation scorecard.

---

## 5. Deferred Items Table

| Item | Original Spec | Reason for Deferral | Tracking Target |
|---|---|---|---|
| NEW-6 (Joseph form) | 034 | Max-5-round constraint makes it non-urgent | Revisit if rounds limit increases |
| D-3 (typed contracts) | 035 | Tracked for spec 032 (package splitting) | Spec 032 |
| NEW-4 (immutable types) | 035 | No current bug — all values are immutable | Monitor |
| D-5 (spec 028 amendment) | 036 | Documentation task for spec 028 | Spec 028 |
| RE-5 (empirical testing) | 036 | Operational verification, not code | Ops checklist |
| NEW-10/11 (Phase 2/3) | 037 | Future phases, tracked in docstrings | Phase 2/3 specs |
| SOLVER-STATUS (Literal) | 037 | Phase 3 solver integration | Phase 3 spec |
| RE-2 spec amendment | 038 | Documentation deliverable pending | **ACTION REQUIRED** |
| NEW-3 spec 024 update | 038 | Documentation deliverable pending | **ACTION REQUIRED** |

Items marked **ACTION REQUIRED** are not true deferrals — they are pending deliverables within spec 038's scope.

---

## 6. Concession Audit

| Spec | Agent | Concession | Verified Against Code | Valid? |
|---|---|---|---|---|
| 034 | plugin-integration-engineer | F-4 downgraded from P1 to REQUIRED-ELSEWHERE | N/A (engine scope) | **YES** — engine persistence is not spec 034's responsibility |
| 034 | kalman-mathematician | F-9 upgraded from P2 to P1 | kalman.py _mat_mul would crash on dim mismatch | **YES** — crash risk confirmed |
| 034 | All agents | test inversion accepted as P2 gap | test_kalman.py/test_convergence.py | **YES** — spec explicitly says "invert test" |
| 035 | safety-engineer | Sentinel suggestion withdrawn | base.py:491-499 | **YES** — None behavior is sufficient |
| 038 | documentation-auditor | Broader framing of RE-2 accepted | solver.py:167-195 | **YES** — N x 1 produces trivial equilibria |
| 038 | game-theorist | F-4 scoped as REQUIRED-ELSEWHERE | payoffs.py:225-230 | **YES** — only 4 modes in PAYOFF_FUNCTIONS |

**All 6 concessions verified.** No concessions were made under social pressure. All were evidence-based.

---

## 7. Overall Wave Assessment

### Implementation Completeness

| Spec | Items | Implemented | Rate |
|---|---|---|---|
| 034 | 9 | 7 (+ 1 partial, 1 deferred) | 78% |
| 035 | 5 | 4 (+ 1 needs test) | 80% |
| 036 | 6 | 4 code items (+ 2 non-code) | 100% code |
| 037 | 7 | 7 | 100% |
| 038 | 3 | 1 (+ 2 documentation pending) | 33% |

### Synthesis Accuracy

15/15 claims verified as ACCURATE by implementation-verifier. 100% accuracy rate.

### Dependency Health

All import boundaries clean. No circular dependencies. Single cross-spec data flow (eq_score pipeline) correctly implemented.

### Priority Recommendations

1. **Immediate**: Fix RE-1 (dimension assertion), create payoff expansion spec (PAYOFF-NEW)
2. **Before merge**: Write M-2 test, verify M-1 test, verify C-3 test inversion
3. **Documentation**: Write RE-2 spec amendment, update NEW-3 spec text
4. **Track**: Engine persistence verification (ENGINE-1)
