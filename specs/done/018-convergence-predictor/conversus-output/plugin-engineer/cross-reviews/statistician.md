# Phase 2 Cross-Review: plugin-engineer reviews statistician

**Spec**: 018-convergence-predictor
**Reviewer**: plugin-engineer
**Reviewing**: statistician's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **Linear slope implementation is correct**: statistician's OLS verification is thorough. The math is sound.

2. **Confidence is not a statistical measure**: Important finding. The stepped function with additive bonuses is a heuristic, not a probability estimate. Users should not interpret 0.80 confidence the same way they would a statistical confidence interval. This has UI implications.

3. **Flat disputes as stagnation concern**: Valid point. In PD or red-blue modes, some residual disputes may be expected at equilibrium. Classifying flat as "stagnate" could produce false alarms. This is a mode-agnostic limitation.

4. **Rounds remaining linear extrapolation**: The cap at 10 is a good safeguard, but statistician is right that the linear model will underestimate for many real deliberations where "easy" disputes resolve first.

## Points to Add

1. **`_build_feature_history()` as a bridge layer**: statistician focuses on the pure prediction functions but does not analyze the state-to-feature conversion. The `_build_feature_history()` function in predictor.py converts `RoundState` objects to `RoundFeatures`. This conversion is lossy: RoundState only has `dispute_count` and `convergence_count` at the round level, while RoundFeatures supports richer fields (position_vector, score_differential, etc.). The prediction engine gets impoverished features when operating through this bridge, compared to what it could get from full feature extraction files.

2. **position_drift always 0**: `_compute_position_drift()` sums `abs(val)` for each agent's `position_vector`. But the state-based feature construction in `_build_feature_history()` never populates `position_vector` (it defaults to `[]`). So `position_drift` is always 0.0. This is reported in the output but is uninformative.

## Disagreement

None. statistician's statistical analysis is rigorous and well-evidenced.
