# plugin-engineer Cross-Review of spec-compliance

**Cross-reviewer**: plugin-engineer
**Reviewing**: spec-compliance Phase 1 review of spec 022
**Date**: 2026-04-01

---

## Agreements

### 1. FR-001 PARTIALLY MET is the right classification

The pure Python approach is better than the spec's scipy-gated pattern, but it does diverge from the spec text. Amending the spec is the right resolution.

### 2. SC-004 trivially met analysis is correct

No scipy dependency means no fallback scenario to test. The criterion was written for a scipy-based implementation; the pure Python approach satisfies it by construction.

### 3. FR-008 is correctly classified as MET

The rounds-remaining estimate in the Kalman path uses the filtered dispute trajectory, not the OLS slope. This is a meaningful improvement over the linear estimate.

---

## Tensions

### 1. SC-003 assessment rigor

spec-compliance marks SC-003 as PARTIALLY MET and recommends a comparative test. I agree a test would help, but I think the current test is sufficient for the criterion as stated. SC-003 says: "The Kalman filter correctly handles non-linear convergence." The test verifies that the prediction is "converge" for the diminishing-returns pattern. "Correctly handles" means it produces the right answer, not that it produces a *better* answer than OLS.

The comparative advantage is a nice-to-have property, not a spec requirement. I would mark SC-003 as MET with a P3 recommendation for a comparative test.

### 2. Constraint verification completeness

spec-compliance verifies the 4 constraints but does not assess the most important one: "The Kalman filter must work with as few as 2 data points." The test suite includes `test_single_observation` (1 point) and `test_multiple_observations` (3 points), but does spec-compliance verify that 2 points produces a meaningful (even if high-uncertainty) prediction?

Looking at the code: `run_kalman_filter()` with 2 observations initializes from the first and updates from the second, producing 2 states. `detect_fixed_point()` with 2 states checks the last change. `compute_kalman_confidence()` with 2 states measures covariance shrinkage from state 1 to state 2.

This works correctly with 2 points. But the constraint says "producing high-uncertainty predictions" -- the test should verify that confidence is low (high uncertainty) with only 2 rounds.

---

## Missed Opportunities

### 1. No assessment of the prediction classification logic

spec-compliance verifies FR compliance but does not review the if/elif chain that maps Kalman state to prediction categories. This chain has 6 branches:

1. fixed_point AND dispute_est <= 1.0 AND confidence >= threshold -> "converge"
2. fixed_point AND dispute_est <= 1.0 AND confidence < threshold -> "uncertain"
3. dispute_delta < 0 AND confidence >= threshold -> "converge"
4. dispute_delta < 0 AND confidence < threshold -> "uncertain"
5. dispute_delta > 0 AND confidence >= threshold -> "stagnate"
6. dispute_delta > 0 AND confidence < threshold -> "uncertain"
7. flat AND fixed_point AND confidence >= threshold -> "stagnate"
8. flat AND confidence >= threshold -> "stagnate"
9. flat AND confidence < threshold -> "uncertain"

This logic determines the user-facing output. A compliance review should verify that each branch produces the correct prediction for its conditions. For example, branch 7 (flat + fixed point + high confidence -> stagnate) is correct: the system has stabilized but not at zero disputes.
