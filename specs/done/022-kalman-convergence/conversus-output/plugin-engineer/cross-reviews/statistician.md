# plugin-engineer Cross-Review of statistician

**Cross-reviewer**: plugin-engineer
**Reviewing**: statistician Phase 1 review of spec 022
**Date**: 2026-04-01

---

## Agreements

### 1. Matrix operations are correct

statistician's verification table for all 12 helper functions is thorough. The analytic verification methods (roundtrip, invariant, direct computation) are appropriate for 3x3 matrices. No disagreements on correctness.

### 2. Pure Python choice is sound

The argument that numpy overhead dominates for 3x3 matrices is correct. The constant-size matrices make the complexity analysis trivial. The zero-dependency benefit is significant for the plugin system.

### 3. Initial covariance bias is worth documenting

The `diag(10, 1, 1)` initial P makes confidence 83% dispute-driven. This is a reasonable default (disputes ARE the primary signal), but documenting it as a design choice helps users who might expect equal weighting.

---

## Tensions

### 1. Joseph form necessity

statistician recommends the Joseph form for covariance update (P2-1) as a numerical stability improvement. I have a different perspective: for 3x3 diagonal-dominant matrices with well-behaved noise parameters, the simple form is adequate. The Joseph form adds code complexity:

```python
# Simple form (current):
P = (I - KH) @ P_pred

# Joseph form:
P = (I - KH) @ P_pred @ (I - KH)^T + K @ R @ K^T
```

For 3x3 matrices, this is 2 additional matrix multiplications and 2 additions. The computational cost is negligible, but the code readability cost is real. The simple form is easier to audit and understand.

My position: keep the simple form with a comment noting the Joseph form as an option if numerical issues are observed. This follows the principle of least complexity.

### 2. Default noise validation scope

statistician recommends validating Q and R defaults across a range of deliberation patterns (P2-2). I agree with the intent but question the scope: what constitutes "a range of deliberation patterns"? Without real-world data, we would be validating against synthetic scenarios. The defaults were chosen based on domain reasoning (disputes are more volatile than rates/scores), and they produce reasonable results in the test suite.

I suggest a lighter approach: add test cases that verify the filter does not diverge or produce nonsensical results for extreme inputs (e.g., disputes jumping from 0 to 100, or negative concession rates). This is more practical than comprehensive validation.

---

## Missed Opportunities

### 1. No assessment of the convergence.py integration

statistician focuses on kalman.py (the mathematical core) but does not review convergence.py (the integration layer that uses the Kalman filter to produce predictions). The classification logic in `_predict_convergence_kalman()` is where mathematical output becomes user-facing advice. Bugs here would not be caught by kalman.py tests alone.

For example, the observation construction in `_build_observation_sequence()` averages concession rates across agents. statistician notes the bimodality concern in their cross-review of me, but the original review does not mention it.

### 2. No discussion of the run_kalman_filter() initialization

The initial state is set from the first observation with P = diag(10, 1, 1). This means the Kalman filter uses the first round's raw observation as its initial state estimate. If the first round has an unusually high or low dispute count (outlier), this biases the entire filter. A more robust initialization would use the mean of the first two observations. statistician's domain expertise would be valuable here.
