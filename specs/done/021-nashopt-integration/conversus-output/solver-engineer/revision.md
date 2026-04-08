# Phase 3 Revision: solver-engineer

**Agent**: solver-engineer
**Spec**: 021-nashopt-integration
**Date**: 2026-04-01
**Inputs**: plugin-engineer cross-review, spec-compliance cross-review

---

## Disposition of Original Recommendations

### P1-1. Document timeout responsibility -- MODIFIED

**Original**: Add a docstring note to `check_equilibrium_nashopt()` stating callers must wrap the call in a timeout mechanism.

**Cross-review challenge (plugin-engineer T-1)**: plugin-engineer argues the timeout should be implemented inside solver.py, not merely documented. The argument is that solver.py is the right abstraction boundary -- every caller should get timeout protection automatically.

**Revised position**: I accept plugin-engineer's stronger position. A `timeout_seconds: int = 30` parameter on `check_equilibrium_nashopt()` with an internal `concurrent.futures.ThreadPoolExecutor` wrapper is better than documentation. This moves timeout enforcement from the caller's responsibility to the module's contract. The default of 30s matches FR-007. If the solver exceeds the timeout, the function should raise `TimeoutError`, which the caller catches and falls back.

**Priority**: Remains P1.

---

### P1-2. Clarify distance normalization -- MAINTAINED

**Original**: Either implement true max-distance normalization or update the spec.

**Cross-review support**: Both plugin-engineer and spec-compliance independently identify this gap. spec-compliance provides the clearest framing: "clamping and normalization are different operations."

**Revised position**: No change. This is the top consensus finding. The implementation should either:
(a) Compute max_distance per game form (e.g., for cooperative N x N with payoffs in [0, max_surviving], the max distance is bounded) and divide, or
(b) Amend the spec to say "clamped to [0.0, 1.0]" and document that resolution is lost for high-distance games.

Option (b) is pragmatically simpler and sufficient for the current use case. I now lean toward (b) based on plugin-engineer's observation that the current consumers only use the score, not the relative distance ordering.

**Priority**: Remains P1.

---

### P2-1. Document cooperative heuristic limitation -- MAINTAINED

**Original**: Add docstring noting the uniform dispute penalty.

**Cross-review response**: spec-compliance notes that the spec says "Agreement matrix from features + dispute counts" and the heuristic is a valid interpretation. No cross-reviewer disputes the recommendation.

**Priority**: Remains P2.

---

### P2-2. Document red-blue aggregation trade-off -- WITHDRAWN

**Original**: Note that per-agent severity information is lost during aggregation.

**Cross-review challenge (plugin-engineer T-2)**: plugin-engineer correctly argues that the spec explicitly says "red_agents_combined" -- aggregation is the spec's design. spec-compliance independently confirms: "The word 'combined' explicitly calls for aggregation."

**Revised position**: I withdraw this recommendation. The aggregation matches the spec. My concern was about what the spec *should* say, not what it *does* say. If per-agent analysis is needed in the future, that is a new spec, not a change to this one.

---

### P3-1. Add to_numpy() convenience -- WITHDRAWN

**Original**: Consider adding a convenience method for numpy conversion.

**Cross-review response**: No reviewer supported this. The conversion at the call site is trivial (`np.array(matrix)`). Adding a method creates a dependency on numpy in the type signature.

---

## New Recommendations from Cross-Reviews

### N-1. Verify WTA matrix shape compatibility with nashopt (from plugin-engineer MO-2)

plugin-engineer raises a critical question: the WTA builder returns N x 1, not N x N. Does nashopt handle non-square payoff matrices? This is an integration correctness question that I should have addressed. The answer depends on nashopt's API: if `check_equilibrium()` expects square matrices, the WTA builder's output will cause a runtime error. If it accepts rectangular matrices (normal-form games with asymmetric action spaces), the output is correct.

**Recommendation**: Add a shape compatibility check in `check_equilibrium_nashopt()` before calling nashopt. If the matrix is non-square, either pad to square (with zero fill for missing actions) or raise a descriptive error explaining the incompatibility.

**Priority**: P1.

---

### N-2. Verify constraints (from spec-compliance MO-1)

spec-compliance notes that neither solver-engineer nor plugin-engineer verified the 4 constraints from spec section 6. I can verify:
- No core dependency: `pyproject.toml` does not list nashopt or jax (verified).
- No interface change: Plugin base class unchanged (verified by test imports).
- No heuristic breakage: Heuristic tests pass (verified by test results).
- Independent testability: solver.py's pure functions are tested without nashopt (verified by test structure).

All 4 constraints are met.

**Priority**: Informational (no action needed).
