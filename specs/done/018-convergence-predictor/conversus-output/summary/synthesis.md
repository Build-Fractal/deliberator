# Phase 5 Synthesis: Spec 018 -- Convergence Predictor

**Spec**: 018-convergence-predictor
**Date**: 2026-03-24
**Agents**: statistician, plugin-engineer, spec-compliance

---

## Overall Assessment

The Convergence Predictor is a well-structured plugin with sound trend analysis logic and robust error handling. The Plugin ABC conformance is complete. The primary gap is methodological: the spec requires Kalman filtering but the implementation uses OLS linear regression. A secondary gap is the cost estimation underestimate in convergence recommendations. No unresolved disputes remain.

---

## Consensus Findings

### 1. FR-004 PARTIALLY MET -- OLS Instead of Kalman Filtering (Critical)

**Unanimous**. The spec (Section 2.2) describes: "Build a linear surrogate model of each agent's best-response function using Kalman filtering (gnep-learn's approach)." The implementation uses OLS linear regression on dispute counts and concession rates. While OLS can be viewed as a degenerate case of Kalman filtering, the implementation lacks recursive state updates, noise modeling, and the fixed-point detection described in the spec. The module docstring acknowledges this: "implements a simplified version of the gnep-learn approach."

**Recommendation**: Either (a) implement Kalman-filtered surrogate models as described, or (b) update the spec to reflect the OLS approach as the v1 method with Kalman as a future enhancement. Option (b) is pragmatic since the OLS approach produces reasonable predictions.

### 2. FR-008 PARTIALLY MET -- Cost Estimation 4x Underestimate (Medium)

**Unanimous after revision**. The convergence recommendation estimates per-round cost as `num_agents + 1`, but the actual D007 formula gives ~16 for 3 agents (review + cross-review + revision + disputes + synthesis). This 4x underestimate makes "estimated additional agent launches" misleading.

**Recommendation**: Import and use `engine.cost.estimate_cost` (the same formula used by the optimizer plugin in spec 019) for accurate cost estimation.

### 3. Equilibrium Score Integration Incomplete (Medium)

**Unanimous**. The predictor passes `equilibrium_scores=None` with a TODO comment. The equilibrium trend function is implemented and tested but never receives data. The confidence calibration's equilibrium bonus (up to +0.05) is never applied.

**Recommendation**: After EquilibriumScorer runs at POST_PHASE_5, read its output JSON from the plugins directory and pass the scores to `predict_convergence()`.

### 4. FR-011 PARTIALLY MET -- auto_stop Not Consumed (Low)

**2-1 consensus** (spec-compliance and plugin-engineer for PARTIALLY MET; statistician conceded). The `auto_stop` config key is documented but never read in `execute()`. The spec says it's "reserved for future" -- the implementation correctly does not act on it, but it also does not explicitly accept and store it.

### 5. position_drift Always 0.0 (Low)

**Unanimous**. The state-to-feature bridge (`_build_feature_history()`) never populates `position_vector`, so `_compute_position_drift()` always returns 0.0. The FR-010 field is structurally present but semantically empty.

**Recommendation**: Either populate position vectors from state data or document that position_drift requires full feature extraction (from output files) to be informative.

### 6. Linear Trend Analysis Sound (Consensus)

The OLS slope implementation is mathematically correct. Dispute trend, concession trend, and equilibrium trend functions produce valid results for their inputs. The `_linear_slope()` function handles edge cases (empty, single, constant) correctly.

### 7. Confidence Calibration Reasonable (Consensus)

The stepped base confidence with additive bonuses is a reasonable heuristic. All reviewers note it is not a statistical confidence measure and should be documented as a "signal strength indicator." The calibration stays within the spec's required ranges (0.3-0.5 for single round, higher for multi-round).

### 8. CONVERGE/STAGNATE/UNCERTAIN Logic Sound (Consensus)

Classification is correct: decreasing disputes = converge, increasing = stagnate, flat = stagnate (per FR-006), insufficient data = uncertain. The `min_confidence` threshold correctly downgrades to uncertain when confidence is too low.

### 9. Recommendation Strings Match Spec (Consensus)

FR-007 (stagnation) and FR-008 (convergence) formats are correctly implemented with the required actionable suggestions and cost estimates (aside from the cost accuracy issue).

---

<!-- DISPUTES_BEGIN -->

## Unresolved Disputes

None. All disagreements were resolved during the cross-review and revision phases. Full consensus was achieved on all findings.

<!-- DISPUTES_END -->

---

## Compliance Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-001 | MET | |
| FR-002 | MET | |
| FR-003 | MET | Confidence 0.30-0.45 |
| FR-004 | **PARTIALLY MET** | OLS, not Kalman filtering |
| FR-005 | MET | |
| FR-006 | MET | |
| FR-007 | MET | |
| FR-008 | **PARTIALLY MET** | Cost 4x underestimate |
| FR-009 | MET | |
| FR-010 | MET | position_drift uninformative |
| FR-011 | PARTIALLY MET | auto_stop not consumed |
| FR-012 | MET | |
| FR-013 | MET (by design) | |
| SC-001 | MET | |
| SC-002 | MET | |
| SC-003 | MET | |
| SC-004 | NOT VERIFIED | No end-to-end accuracy test |
| SC-005 | MET | |

**MET**: 10/13 FR, 4/5 SC
**PARTIALLY MET**: 3 FR
**NOT MET**: 0
**NOT VERIFIED**: 1 SC

---

## Recommended Actions

1. Decide: Implement Kalman filtering (FR-004) or update spec to accept OLS as v1 method.
2. Fix cost estimation: Use `engine.cost.estimate_cost` for accurate agent launch counts.
3. Complete equilibrium score integration: Read EquilibriumScorer output in the predictor.
4. Fix position_drift: Populate position vectors or document the limitation.
5. Document confidence as a heuristic indicator, not a statistical measure.
