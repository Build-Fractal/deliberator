# Plugin-Engineer Revision: Spec 023 -- AMPL Config Optimizer

**Reviewer**: plugin-engineer
**Revision iteration**: 1
**Date**: 2026-04-01

---

## Recommendation Dispositions

### Recommendation 1: Unify error handling (was P1)

**Disposition: MODIFIED -- adopt SolveOutcome approach, DOWNGRADED to P2**

solver-engineer's cross-review correctly challenges my initial proposal to raise exceptions for infeasibility. Infeasibility is a valid solver outcome, not an error condition. Raising `SolverInfeasibleError` would conflate normal solver results with exceptional failures, requiring the caller to catch solver outcomes alongside genuine exceptions.

spec-compliance's cross-review argues that internal API error handling is outside spec scope and suggests P2. I accept the downgrade -- no FR or SC depends on the internal function's return type convention.

I adopt solver-engineer's `SolveOutcome` approach: a structured return type that distinguishes `"optimal"`, `"infeasible"`, `"no_amplpy"`, and `"no_selection"`. The `solve_ampl` general-purpose API already returns a dict with `solve_result`, which is adequate. The asymmetry concern is resolved by the structured return type on `solve_with_ampl`, not by making `solve_ampl` match it.

**Revised recommendation**: Replace `solve_with_ampl`'s `OptimalConfig | None` return with a `SolveOutcome` dataclass containing `config`, `status`, and `solve_time_ms`. Priority: P2.

---

### Recommendation 2: Implement solver config key (was P2)

**Disposition: MODIFIED -- remove dead documentation**

spec-compliance's cross-review raises a valid point: the spec does not define a `solver` plugin config key. Implementing it would introduce an undocumented feature, creating spec drift. The two options are: (a) amend the spec, or (b) remove the docstring.

On reflection, solver pinning is a genuine user need for reproducibility, but it should be specced, not implemented ad hoc. The immediate fix is to remove the `solver` config key from the `ConfigOptimizer` docstring so it does not promise a feature that does not exist. If solver pinning is needed, a spec amendment (or a new spec) should define the feature, including edge cases (what happens when AMPL is pinned but unavailable?).

**Revised recommendation**: Remove the `solver` config key from the `ConfigOptimizer` docstring. If solver pinning is needed, amend the spec. Priority: P3 (editorial cleanup).

---

### Recommendation 3: Robust file detection in solve_ampl() (was P2)

**Disposition: MAINTAINED**

spec-compliance's cross-review argues that FR-009 only requires `.mod` file support, so the heuristic's failure on `.ampl` files is not a compliance gap. This is technically correct but misses the point: the false-positive risk (a model string ending in ".mod") is a correctness concern that affects FR-009 compliance. A model string like `"param n; maximize obj: n; # imported from foo.mod"` would be incorrectly treated as a file path.

solver-engineer's cross-review did not address this point. No cross-reviewer challenged the recommendation.

**Revised recommendation**: Accept `model: str | Path` in `solve_ampl()`. `Path` objects are always treated as files. Strings are checked for file extensions (`.mod`, `.ampl`, `.run`) only if they contain no newlines. This is a minimal change that eliminates the false-positive risk. Priority: P2.

---

### Recommendation 4: Standardize cost parameter naming (was P3)

**Disposition: MAINTAINED**

No cross-reviewer challenged or endorsed this. It is a low-priority naming cleanup. The inconsistency between `cost_per_agent_launch` (plugin config) and `cost_per_launch` (API parameter) is real but cosmetic.

**Revised recommendation**: Unchanged. Priority: P3.

---

### Recommendation 5: Document AMPL Community Edition limits (was P3)

**Disposition: MAINTAINED**

spec-compliance confirms this is not a compliance failure (FR-010 requires no licence, not unlimited size). The documentation gap is real but minor.

**Revised recommendation**: Unchanged. Priority: P3.

---

### Recommendation 6: Clarify NLP/MINLP solver requirements (was P3)

**Disposition: MAINTAINED**

spec-compliance's FR-008 analysis confirms the documentation gap. No cross-reviewer challenged the recommendation.

**Revised recommendation**: Unchanged. Priority: P3.

---

## New Recommendations

### New Recommendation A: Check for both amplpy and highspy in HAS_AMPL (Priority: P2)

Raised in my cross-review of spec-compliance's FR-001 assessment. The spec says "amplpy AND highspy are importable" but the implementation only checks for amplpy. solver-engineer's revision also adopts this as New Rec A, confirming convergence.

The fix: `try: from amplpy import AMPL; import highspy; HAS_AMPL = True except ImportError: HAS_AMPL = False`.

**Recommendation**: Both packages checked in the import guard. Priority: P2.

### New Recommendation B: Add integration tests with real AMPL solver (Priority: P3)

spec-compliance recommends `@pytest.mark.skipunless(HAS_AMPL)` integration tests. solver-engineer's cross-review of spec-compliance accepts this finding. The mock-only test suite cannot catch AMPL model syntax errors or solver option format changes.

The integration tests should: (1) parse the AMPL model string with a real AMPL instance, (2) solve the config optimization problem, (3) verify the result matches grid search (SC-001), (4) verify infeasibility detection (SC-002).

**Recommendation**: Add `@pytest.mark.skipunless(HAS_AMPL, "amplpy not installed")` integration tests. Priority: P3.

---

## Position Summary

**Modified** (2):
- Error handling unification (Rec 1) -- downgraded to P2, switched from exceptions to `SolveOutcome` per solver-engineer's cross-review.
- Solver config key (Rec 2) -- changed from "implement" to "remove dead documentation" per spec-compliance's cross-review.

**Maintained** (4):
- File detection (Rec 3) -- no challenges received.
- Cost naming (Rec 4) -- no challenges received.
- Community Edition docs (Rec 5) -- confirmed by spec-compliance.
- NLP/MINLP docs (Rec 6) -- confirmed by spec-compliance.

**New** (2):
- Both-dependency import check (New Rec A) -- convergence with solver-engineer.
- Integration tests (New Rec B) -- adopted from spec-compliance.

The deepest intellectual correction is on Rec 1 (error handling). My initial instinct to raise exceptions for infeasibility was wrong. solver-engineer correctly identified that infeasibility is a solver outcome, not an error. In optimization, the solver's job is to determine feasibility and optimality -- "infeasible" is a valid answer, not a failure. The structured return type pattern (algebraic-style result with status discrimination) is the right approach for solver APIs.

---

### Referenced Documentation

- Cross-reviews received: solver-engineer and spec-compliance cross-reviews of plugin-engineer
- Cross-reviews written: plugin-engineer cross-reviews of solver-engineer and spec-compliance
- `conversus/plugins/optimizer/optimizer.py` -- L38-39 (solver docstring)
- `conversus/plugins/optimizer/ampl_model.py` -- L29-34 (HAS_AMPL), L354 (file detection)
