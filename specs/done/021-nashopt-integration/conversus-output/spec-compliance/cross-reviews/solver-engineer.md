# spec-compliance Cross-Review of solver-engineer

**Cross-reviewer**: spec-compliance
**Reviewing**: solver-engineer Phase 1 review of spec 021
**Date**: 2026-04-01

---

## Agreements

### 1. Distance normalization vs. clamping is the highest-priority finding

solver-engineer provides the clearest articulation of this issue: "True normalization would divide by the theoretical maximum distance for the game form, preserving the relative ordering of non-equilibrium states." This exactly matches my FR-004 PARTIALLY MET finding. The two independent identifications confirm this is a genuine spec-implementation gap.

### 2. Degenerate case analysis is thorough and correct

solver-engineer's FR-006 review covers all three cases with correct mathematical justification (vacuous truth for zero agents, trivial equilibrium for single agent, any-strategy equilibrium for zero-variance). The 1e-12 threshold analysis is a useful detail I did not include in my review.

### 3. Timeout responsibility gap is correctly identified

solver-engineer's P1-1 (document timeout responsibility) and my FR-007 NOT VERIFIED converge on the same gap. The solver module does not implement or document timeout behavior.

---

## Tensions

### 1. Mathematical depth vs. spec traceability

solver-engineer provides deep mathematical analysis of each payoff matrix builder (formulas, edge cases, calibration choices). This is valuable domain expertise. However, the review does not systematically trace each formula back to the spec's table in Section 2 ("Per-Mode Payoff Matrix Construction"). The spec says:

| cooperative | N x N agreement/dispute matrix | Agreement matrix from features + dispute counts |

solver-engineer verifies the cooperative builder produces an N x N matrix and describes the formula, but does not explicitly state: "The source column says 'Agreement matrix from features + dispute counts.' The code uses `features.agreement_matrix` when available and `avg_surviving - dispute_penalty` when not. Both are faithful to the spec." This explicit traceability is what a compliance review needs.

The tension is between solver-engineer's depth (how the math works) and compliance's breadth (does the code match the spec). Both are necessary; neither is sufficient alone.

### 2. Red-blue "information loss" framing

solver-engineer calls the red-agent aggregation "information loss." From a compliance perspective, the spec says "2 x K severity/mitigation matrix" with rows "[red_agents_combined, blue_agents_combined]." The word "combined" explicitly calls for aggregation. The implementation matches the spec. solver-engineer's concern is about what the spec *should* say, not what it *does* say. From a compliance perspective, the implementation is correct.

---

## Missed Opportunities

### 1. No constraints verification

solver-engineer does not verify the spec's Section 6 constraints:
- "Must NOT add nashopt/jax to core package requirements." -- Could verify via pyproject.toml.
- "Must NOT change the Plugin interface or output format." -- Could verify via Plugin base class.
- "Must NOT break the heuristic fallback path." -- Could verify via test results.
- "solver.py must be independently testable with mock payoff matrices." -- Could verify by examining test structure.

These are important compliance items that solver-engineer is well-positioned to assess (especially the last one, since solver-engineer understands the mathematical testability requirements).

### 2. Best-response reporting edge cases

solver-engineer's FR-005 analysis describes the three-tier extraction logic but does not assess edge cases:
- What if nashopt returns `best_responses` with integer keys but `agents_not_at_equilibrium` with string keys? The code handles both via `isinstance` checks.
- What if nashopt returns `best_responses` for agents not in the input? The code uses `.get()` with a default, so unknown agents would get best_response = 0.

These edge cases are in solver-engineer's domain and would strengthen the review.
