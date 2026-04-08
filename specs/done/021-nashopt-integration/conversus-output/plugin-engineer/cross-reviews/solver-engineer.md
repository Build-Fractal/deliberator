# plugin-engineer Cross-Review of solver-engineer

**Cross-reviewer**: plugin-engineer
**Reviewing**: solver-engineer Phase 1 review of spec 021
**Date**: 2026-04-01

---

## Agreements

### 1. Cooperative heuristic formula limitation is well-identified

solver-engineer's observation that the dispute penalty is uniform across all agent pairs (rather than per-pair) is correct. The agreement matrix path handles the precise case; the heuristic is a reasonable approximation. The recommendation to document this limitation (P2-1) is appropriate.

### 2. Red-blue aggregation trade-off is real but acceptable

The severity vector summation does lose per-agent information. However, for the purpose of equilibrium analysis (are the teams collectively at equilibrium?), the aggregate is the correct unit of analysis. The red team acts as a coalition, and the equilibrium is computed for the coalition, not individual members. solver-engineer's framing of this as "information loss" is technically correct but the impact is low for the stated use case.

### 3. Distance clamping vs. normalization is the top issue

solver-engineer and spec-compliance both identify this independently. The convergence of two reviewers on the same issue increases confidence that it is a real gap. I agree it should be P1.

---

## Tensions

### 1. Timeout implementation location

solver-engineer's P1-1 recommends documenting the timeout responsibility. My view is stronger: the timeout should be implemented inside solver.py rather than delegated to callers. solver-engineer raises this as a documentation issue; I raise it as an architectural concern. The difference: documentation tells callers what to do, but code enforces it.

However, solver-engineer's argument about the scorer being the single caller is pragmatically valid today. The disagreement is about future-proofing vs. present simplicity. I maintain my position that including timeout in solver.py is better, but I acknowledge this is a design preference, not a correctness issue.

### 2. Red-blue matrix structure

solver-engineer notes the 2 x K structure "loses information." I disagree with the framing. The spec explicitly defines the red-blue matrix as "2 x K severity/mitigation matrix" -- two rows (red combined, blue combined), K severity levels. The implementation matches the spec. If per-agent information were needed, the spec would define an N x K matrix. The current design is correct for the game form: red-blue is a two-player game between coalitions.

---

## Missed Opportunities

### 1. No discussion of the scorer-solver API boundary

solver-engineer reviews the solver module thoroughly but does not discuss how the solver's API (SolverResult) maps to the scorer's needs (PluginResult). The SolverResult -> PluginResult transformation is where integration bugs typically occur: field name mismatches, missing fields, type conversions. Without this analysis, we cannot assess whether the API boundary is clean.

### 2. No assessment of the payoff matrix -> nashopt type compatibility

solver-engineer notes that `build_payoff_matrix()` returns `list[list[float]]` and the caller converts to `np.ndarray`. But nashopt's `check_equilibrium()` expects specific array shapes. solver-engineer does not verify that the matrix shapes produced by each mode builder are compatible with nashopt's expected input shape. For example, the WTA builder returns N x 1 (a column vector), not N x N. Does nashopt handle non-square payoff matrices? This is a critical integration question that solver-engineer is best positioned to answer.
