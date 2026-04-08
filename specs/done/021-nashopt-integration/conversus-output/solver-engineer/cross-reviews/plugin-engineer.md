# solver-engineer Cross-Review of plugin-engineer

**Cross-reviewer**: solver-engineer
**Reviewing**: plugin-engineer Phase 1 review of spec 021
**Date**: 2026-04-01

---

## Agreements

### 1. Coupled import concern is valid but low-priority

plugin-engineer correctly identifies that the single try block couples nashopt and numpy failure modes. The suggestion to separate imports and log which is missing is a good debugging aid. However, since nashopt transitively depends on numpy (via JAX), a broken numpy always means a broken nashopt in practice. I agree this is P2, not P1.

### 2. scorer.py omission is the biggest gap in this review cycle

plugin-engineer's P1-1 (include scorer.py in artifacts) is the correct priority. I made the same observation about timeout responsibility (my P1-1). The dispatch logic, timeout wrapper, and PluginResult construction all live in scorer.py. Without it, neither of us can fully verify the integration.

### 3. SolverResult design assessment is accurate

The frozen dataclass with agent-name keys (not indices) is indeed consumer-friendly. The distance/score separation is clean. I have no disagreements with this analysis.

---

## Tensions

### 1. Scope of solver.py's responsibility

plugin-engineer frames solver.py as a "pure computation module" that should not concern itself with plugin result formatting or timeout logic. I partially disagree. While PluginResult formatting belongs in the scorer, the timeout is a solver-level concern: the spec says "Solver execution MUST be capped at a configurable timeout." The word "execution" refers to the solver call, not the plugin call. Implementing timeout at the scorer level means every caller of `check_equilibrium_nashopt()` must independently implement timeout wrapping. If solver.py grows additional callers (e.g., a CLI debug tool or a web API endpoint), each must re-implement the timeout. A `timeout_seconds` parameter on `check_equilibrium_nashopt()` with an internal `concurrent.futures` wrapper would be more robust.

This is a design disagreement, not a correctness issue. Both approaches produce correct behavior when the single caller (scorer.py) implements timeout. But the solver-level approach is more defensive.

---

## Missed Opportunities

### 1. No discussion of numerical precision

plugin-engineer's review does not address the numerical properties of the payoff matrices or the scoring formula. The cooperative heuristic computes `avg_surviving - dispute_count / n`, which can produce values close to zero for high-dispute games. These near-zero payoffs, when passed to nashopt as a numpy array, may cause numerical instability in the equilibrium solver (pivoting issues, convergence failures). This is within solver-engineer's domain, and I flagged it implicitly in my review (cooperative heuristic formula concern), but plugin-engineer should have noted the integration risk: what happens when the payoff matrix fed to nashopt contains near-zero or near-identical values that are numerically indistinguishable?

### 2. No assessment of __init__.py exports

plugin-engineer recommends adding `__all__` to solver.py (P2-2) but does not check whether the nashopt package's `__init__.py` correctly re-exports the necessary symbols. The EquilibriumScorer import path (`from conversus.plugins.nashopt import EquilibriumScorer`) suggests that `__init__.py` manages the public API. Whether `HAS_NASHOPT` is re-exported at the package level affects how callers check for nashopt availability.
