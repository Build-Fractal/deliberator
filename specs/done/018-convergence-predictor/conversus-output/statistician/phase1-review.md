# Phase 1 Review: statistician

**Spec**: 018-convergence-predictor
**Reviewer**: statistician
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Evaluate the soundness of linear trend analysis, confidence calibration, and correctness of CONVERGE/STAGNATE/UNCERTAIN classification.

---

## Linear Trend Analysis

### `_linear_slope()` Implementation

The function computes ordinary least squares (OLS) slope using the standard formula: `slope = sum((x_i - x_mean)(y_i - y_mean)) / sum((x_i - x_mean)^2)`. This is correct for equally-spaced x values (round indices 0, 1, 2, ...).

- Returns 0.0 for fewer than 2 data points: correct (undefined slope).
- Returns 0.0 for constant values (denominator == 0): correct.
- Numerical tests verify perfect slopes (+1.0, -1.0) and two-point cases.

**Assessment**: Mathematically sound. Standard OLS for univariate regression.

### `_dispute_trend()` and `_concession_trend()`

Both extract time series from RoundFeatures history and pass to `_linear_slope()`. Dispute trend uses `dispute_count`, concession trend uses average `concession_rate` across agents.

**Concern with concession_trend**: Averaging concession rates across agents may mask important heterogeneity. If one agent concedes heavily while another becomes rigid, the average could be flat (suggesting stagnation) even though the deliberation dynamics are active. A more robust approach would track per-agent trends and flag divergence.

**Assessment**: Adequate for v1. The averaging limitation should be documented.

### `_equilibrium_trend()`

Uses explicitly provided equilibrium scores (from the EquilibriumScorer) if available. Returns 0.0 otherwise. This is a clean integration point but relies on the caller passing scores. Currently, the plugin passes `equilibrium_scores=None` with a TODO comment: `# TODO: read from scorer output`. This means equilibrium trend is always 0.0 in practice.

**Assessment**: The trend function itself is correct, but the integration is incomplete. The equilibrium trend never contributes to predictions in the current implementation.

---

## Confidence Calibration

### `_compute_confidence()` Model

The calibration uses a stepped base confidence (0.30 for 1 round, 0.50 for 2, 0.65 for 3, 0.75 for 4+) with additive bonuses for signal agreement:

- Disputes decreasing + concessions increasing: +0.15
- Both signaling stagnation: +0.10
- Partial signal: +0.05
- Positive equilibrium trend: +0.05
- Negative equilibrium trend: +0.02

Maximum possible confidence: 0.75 + 0.15 + 0.05 = 0.95 (with 4+ rounds, strong agreement, improving equilibrium).

**Concern 1 -- Arbitrary step function**: The base confidence values (0.30, 0.50, 0.65, 0.75) are not derived from any statistical model. They represent the developer's intuition about how much data is needed. While reasonable, they could mislead users into thinking the confidence has a statistical interpretation (like a p-value or prediction interval). The confidence is better understood as a "data sufficiency indicator."

**Concern 2 -- Agreement bonus asymmetry**: The stagnation agreement bonus (+0.10) is lower than the convergence agreement bonus (+0.15). There is no stated justification for this asymmetry. In practice, both types of agreement should boost confidence equally since both represent consistent signals.

**Concern 3 -- Ceiling effect**: With 4+ rounds and strong agreement, confidence reaches 0.90-0.95. This leaves little room for improvement with more data. A deliberation with 10 rounds of strong convergence signals gets nearly the same confidence as one with 4 rounds. The diminishing returns of confidence should ideally continue more gradually.

**Assessment**: The calibration is a reasonable heuristic but is not statistically grounded. It should be presented as a "signal strength indicator" rather than a statistical confidence measure.

---

## CONVERGE/STAGNATE/UNCERTAIN Classification

### Single-Round Case (num_rounds <= 1)

- Zero disputes: predicts "converge" with capped confidence (0.45 max).
- Non-zero disputes: predicts "uncertain."
- Confidence always <= 0.45 for single round.

**Assessment**: Correct. Conservative handling of insufficient data. FR-003 says confidence should be in 0.3-0.5 range for single round -- the implementation caps at 0.45, within range.

### Multi-Round: Decreasing Disputes (d_trend < 0)

- Predicts "converge" if confidence >= min_confidence.
- Estimates rounds remaining via `_estimate_rounds_remaining()`.
- Falls back to "uncertain" if confidence is below threshold.

**Assessment**: Sound. The dispute trend is the primary signal, supplemented by concession and equilibrium trends.

### Multi-Round: Increasing Disputes (d_trend > 0)

- Predicts "stagnate" if confidence >= min_confidence.
- No rounds_remaining (set to None).
- Reasoning includes actionable suggestions.

**Assessment**: Correct classification. Increasing disputes are a clear stagnation signal.

### Multi-Round: Flat Disputes (d_trend == 0)

- Predicts "stagnate."

**Concern**: Flat disputes could also indicate a stable equilibrium (disputes exist but are not changing). Classifying flat as "stagnate" may be too aggressive. A stable state with some disputes could be the optimal outcome for adversarial modes (PD, red-blue) where zero disputes is unrealistic.

**Assessment**: Reasonable for cooperative mode, potentially misleading for adversarial modes. The classification is mode-agnostic, which is a limitation.

---

## Rounds Remaining Estimation

`_estimate_rounds_remaining(dispute_count, trend)`:
- Formula: `ceil(dispute_count / abs(trend))`
- Capped at 10.
- Returns 0 if trend >= 0 or disputes <= 0.

**Concern**: Linear extrapolation assumes the dispute reduction rate is constant. In practice, dispute reduction often slows as the "easy" disputes are resolved first (diminishing returns). The linear model will underestimate rounds remaining. However, the cap at 10 mitigates catastrophic underestimation.

**Assessment**: Acceptable for a first-order estimate. The linear assumption and cap are documented. Users should be warned that estimates become less reliable beyond 3-4 rounds out.

---

## Summary

| Area | Verdict |
|------|---------|
| Linear slope computation | Sound OLS implementation |
| Dispute trend | Correct |
| Concession trend | Adequate; averaging masks heterogeneity |
| Equilibrium trend | Correct but unused (TODO) |
| Confidence calibration | Reasonable heuristic, not statistically grounded |
| CONVERGE classification | Sound |
| STAGNATE classification | Flat disputes may be over-aggressive |
| UNCERTAIN classification | Correct, conservative |
| Rounds remaining | Linear extrapolation; acceptable with cap |

### Key Issues

1. **Equilibrium trend integration incomplete**: Always None in practice (TODO in predictor.py).
2. **Flat disputes classified as stagnate**: May be incorrect for adversarial modes.
3. **Confidence is not a statistical measure**: Naming may mislead users.
4. **Concession rate averaging**: Masks per-agent heterogeneity.
