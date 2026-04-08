# Phase 3 Revision: plugin-engineer

**Agent**: plugin-engineer
**Spec**: 021-nashopt-integration
**Date**: 2026-04-01
**Inputs**: solver-engineer cross-review, spec-compliance cross-review

---

## Disposition of Original Recommendations

### P1-1. Include scorer.py in review artifacts -- MAINTAINED

**Original**: Include scorer.py so FR-007, FR-008, SC-001, SC-002, SC-004 can be fully verified.

**Cross-review support**: All three reviewers converge on this. solver-engineer frames it as a timeout concern. spec-compliance marks FR-007 as NOT VERIFIED because of the omission. This is the unanimous highest-priority finding.

**Priority**: Remains P1.

---

### P2-1. Separate nashopt and numpy imports -- MAINTAINED

**Original**: Separate the try block and log which dependency is missing.

**Cross-review response**: solver-engineer agrees this is valid but low-priority. spec-compliance does not comment.

**Priority**: Remains P2.

---

### P2-2. Add __all__ export list -- MODIFIED

**Original**: Add `__all__` to solver.py.

**Cross-review addition (spec-compliance MO-1)**: spec-compliance asks whether __init__.py re-exports HAS_NASHOPT at the package level. This is a valid concern. The recommendation should be expanded: add `__all__` to solver.py AND verify that the nashopt package's `__init__.py` re-exports `HAS_NASHOPT` so callers can check it from the package root.

**Priority**: Remains P2.

---

### P3-1. TYPE_CHECKING block for nashopt/np types -- WITHDRAWN

**Original**: Use TYPE_CHECKING to provide better IDE hints for the module-level nashopt and np variables.

**Revised position**: This would require `import nashopt` inside `if TYPE_CHECKING:`, which would cause the import to run during type checking. Since nashopt is not installed in most development environments, this would cause type-checker errors. The `Any` typing is the correct approach for optional dependencies.

---

## New Recommendations from Cross-Reviews

### N-1. Timeout should be in solver.py, not scorer.py (from solver-engineer revision)

solver-engineer accepted my cross-review argument that timeout belongs in the solver module. The revised recommendation is to add a `timeout_seconds: int = 30` parameter to `check_equilibrium_nashopt()`. I now formalize this as a concrete recommendation.

**Implementation**: Use `concurrent.futures.ThreadPoolExecutor` with a single worker:

```python
def check_equilibrium_nashopt(
    features: RoundFeatures,
    mode: str,
    timeout_seconds: int = 30,
) -> SolverResult:
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_solve_inner, features, mode)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            raise TimeoutError(
                f"nashopt solver exceeded {timeout_seconds}s timeout"
            )
```

The caller catches `TimeoutError` and falls back to heuristic.

**Priority**: P1 (implements FR-007 at the right abstraction level).

---

### N-2. Verify WTA matrix shape compatibility (from solver-engineer N-1)

solver-engineer raises a critical question about non-square payoff matrices. The WTA builder returns N x 1, but nashopt may expect N x N. This needs a shape check or padding.

I support solver-engineer's recommendation. Additionally, the check should happen in `check_equilibrium_nashopt()` with a clear error message if the shape is incompatible. The scorer can then fall back to heuristic on shape error.

**Priority**: P1 (runtime error prevention).
