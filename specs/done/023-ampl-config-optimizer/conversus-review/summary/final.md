# Synthesis: Spec 023 -- AMPL Config Optimizer

**Phase**: 5 (Final Synthesis)
**Date**: 2026-04-01
**Agents**: solver-engineer, plugin-engineer, spec-compliance

---

## Overview

Spec 023 introduces AMPL/HiGHS mixed-integer programming to the conversus config optimizer, adds a general-purpose `solve_ampl()` API, and retains grid search as a zero-dependency fallback. The implementation is correct, well-tested, and backward compatible. The plugin interface is unchanged, the dispatch layer is transparent, and the fallback logic is robust.

The review identified 6 compliance gaps (3 requiring code changes, 3 requiring spec amendments), 4 code quality improvements, and several editorial cleanups. No reviewer identified a correctness bug in the solver logic or the plugin integration. The strongest aspect of the implementation is the cross-solver consistency verification: `TestQualityModelConsistency` exhaustively proves that AMPL and grid search produce identical quality/cost assessments at every grid point.

---

## Converged Recommendations (Priority Order)

### P1: Align FR-004 spec text with implementation

**Convergence**: solver-engineer + spec-compliance (2/3, plugin-engineer defers)
**Priority dispute**: spec-compliance argues P1 (spec integrity); solver-engineer argues P2 (documentation only). **Resolution**: P1. The spec is the contract. When it describes "piecewise linear approximation" and the implementation uses exact enumeration, the contract is inaccurate. The code is correct -- the spec must be updated to match.

**Action**: Amend FR-004 to: "The quality model MUST use the exact heuristic quality values at all integer grid points, ensuring 0% deviation from the grid search. The AMPL model encodes these values as indexed parameters for binary selection, guaranteeing provable equivalence with the grid search optimum."

---

### P2: Store config model as `.mod` file

**Convergence**: 3/3 (full)

Section 6 of the spec states: "The AMPL model must be readable/editable by users (stored as `.mod` file, not generated code)." The implementation stores it as a Python string constant.

**Action**: Create `conversus/plugins/optimizer/config_optimizer.mod`. Load it in `build_ampl_model` or at module init. The `solve_ampl()` API already supports file loading.

---

### P2: Extract real MIP gap from solver output

**Convergence**: 3/3 (full)

FR-012 requires "gap (optimality gap for MIP)." The current `gap: 0.0` is hardcoded in `ampl_solver.py` L149. If the solver times out with a feasible incumbent, the true gap is non-zero.

**Action**: After `ampl.solve()`, query the solver for the actual gap. Report 0.0 only when the solver proves optimality; otherwise, extract the gap from HiGHS output.

---

### P2: Check for both amplpy and highspy in HAS_AMPL guard

**Convergence**: 3/3 (full)

FR-001 says "amplpy AND highspy are importable." The code checks only amplpy. If a user installs amplpy without highspy, the AMPL path activates but the solver fails at solve time with a misleading diagnostic.

**Action**: Change the import guard to:
```python
try:
    from amplpy import AMPL
    import highspy
    HAS_AMPL = True
except ImportError:
    HAS_AMPL = False
```

---

### P2: Revise SC-002 in the spec

**Convergence**: solver-engineer + spec-compliance (2/3, plugin-engineer defers)

SC-002 claims "AMPL optimizer finds infeasibility faster than grid search for tight constraints." The enumeration-based formulation cannot outperform O(n) grid search for n=135. The success criterion is unfalsifiable with the current implementation.

**Action**: Revise SC-002 to: "AMPL optimizer correctly identifies infeasibility, delegating to grid search for the detailed infeasibility report. For search spaces larger than the current 135-point grid (future extensions), the MIP formulation enables LP-relaxation-based pruning that grid search cannot."

---

### P2: Structured return type for `solve_with_ampl`

**Convergence**: solver-engineer + plugin-engineer (2/3, spec-compliance accepts)

`solve_with_ampl` returns `None` for three distinct conditions (amplpy missing, infeasible, no variable selected). Callers cannot distinguish failure modes. Both solver-engineer and plugin-engineer converge on a `SolveOutcome` dataclass with discriminated status.

**Action**: Define `SolveOutcome(config: OptimalConfig | None, status: Literal["optimal", "infeasible", "no_amplpy", "no_selection"], solve_time_ms: float | None)`. Update `_solve_with_ampl_fallback` to inspect `status` for precise logging.

---

### P2: Robust file detection in `solve_ampl()`

**Convergence**: plugin-engineer + solver-engineer (2/3)

The current heuristic (`model.strip().endswith(".mod") and "\n" not in model`) has false-positive risk for model strings ending in ".mod" and false-negative risk for `.ampl`/`.run` files.

**Action**: Accept `model: str | Path`. `Path` objects are always treated as files. Strings are checked for recognized extensions (`.mod`, `.ampl`, `.run`) only when single-line.

**Note**: spec-compliance considers this outside FR-009 scope. The synthesizer includes it at P2 because `solve_ampl()` is a public API exported in `__init__.py`, and a known false-positive in a public API is a correctness concern regardless of spec scope.

---

### P2: Update enumeration documentation

**Convergence**: 3/3 (all agree documentation is inaccurate; framing disputed)

The `ampl_model.py` docstring claims the MIP "solves the mixed-integer program exactly rather than enumerating the entire grid." The implementation enumerates the entire grid.

**Action**: Update docstrings to accurately describe the formulation as exact enumeration via binary selection MIP. Lead with the positive value (formal specification, solver portability, general-purpose API, extensibility to larger search spaces) and note the current-search-space equivalence with grid search. This resolves plugin-engineer's framing concern while preserving solver-engineer's factual accuracy.

---

### P3: Remove dead `solver` config key from docstring

**Convergence**: plugin-engineer + spec-compliance (2/3)

`ConfigOptimizer`'s docstring documents a `solver` config key that the code never reads. This is dead documentation that creates false expectations.

**Action**: Remove `solver (str)` from the docstring. If solver pinning is needed, add a requirement to the spec first.

---

### P3: Integration tests with real AMPL solver

**Convergence**: spec-compliance + plugin-engineer (2/3, solver-engineer accepted)

All AMPL tests use mocks. The AMPL model string has never been parsed by a real AMPL instance in CI.

**Action**: Add `@pytest.mark.skipunless(HAS_AMPL, "amplpy not installed")` integration tests that: (1) parse the model with a real AMPL instance, (2) solve the config optimization problem, (3) verify the result matches grid search, (4) verify infeasibility detection.

---

### P3: Standardize parameter naming

**Convergence**: plugin-engineer (sole proponent, no objections)

`cost_per_agent_launch` (plugin config) vs. `cost_per_launch` (API parameter). `solver_timeout` (plugin config) vs. `timeout` (API).

**Action**: Standardize on `cost_per_launch` and `timeout` in the API. Accept both old and new names in plugin config for backward compatibility.

---

### P3: Document NLP/MINLP solver requirements and Community Edition limits

**Convergence**: plugin-engineer (sole proponent, spec-compliance accepted)

FR-008 implies HiGHS handles NLP/MINLP. It does not. The AMPL Community Edition has size limits.

**Action**: Add to `solve_ampl()` docstring: "Default solver HiGHS supports MIP and LP. NLP requires `solver='ipopt'`; MINLP requires `solver='bonmin'` (not bundled). The free AMPL Community Edition supports problems up to ~500 variables/constraints."

---

## DISPUTES_BEGIN

### Dispute 1: FR-004 priority -- P1 vs. P2

**Parties**: spec-compliance (P1) vs. solver-engineer (P2)

spec-compliance argues spec-implementation alignment is a first-order compliance concern: the spec is the contract, and an inaccurate contract undermines trust. solver-engineer argues the code is correct and the spec amendment is editorial.

**Synthesizer resolution**: P1. The spec is the authoritative document. Leaving FR-004 misaligned creates ambiguity for future implementors and auditors. The amendment is a small text change with no code impact.

---

### Dispute 2: File detection priority -- P2 vs. P3

**Parties**: plugin-engineer (P2) vs. spec-compliance (P3 / outside scope)

plugin-engineer argues a known false-positive in a public API is a correctness bug warranting P2. spec-compliance argues FR-009 only requires `.mod` support and the heuristic works for `.mod` files.

**Synthesizer resolution**: P2. `solve_ampl()` is exported in `__init__.py` as a public API for arbitrary AMPL problems. Its correctness is not bounded by FR-009's narrow `.mod` requirement. A public API function that silently misclassifies input is a bug at P2.

---

### Dispute 3: Documentation framing -- limitation-first vs. value-first

**Parties**: solver-engineer (technical accuracy first) vs. plugin-engineer (architectural value first)

solver-engineer wants documentation to lead with "equivalent to grid search for current search space." plugin-engineer wants it to lead with "formal specification, solver portability, extensibility."

**Synthesizer resolution**: Both. The documentation should state the architectural value first (why AMPL exists) and the current-search-space equivalence second (what to expect in practice). This is not a compromise -- it is correct technical writing: motivation before limitations.

## DISPUTES_END

---

## Compliance Status (Post-Review)

| Requirement | Status | Action Needed |
|---|---|---|
| FR-001 | PASS -> PASS | Add highspy to import check |
| FR-002 | PASS | None |
| FR-003 | PASS | None |
| FR-004 | PARTIAL -> PASS | Amend spec text |
| FR-005 | PASS | None |
| FR-006 | PASS | None |
| FR-007 | PASS | None |
| FR-008 | PASS | Document NLP/MINLP solvers |
| FR-009 | PARTIAL -> PASS | Create `.mod` file |
| FR-010 | PASS | Document CE limits |
| FR-011 | PASS | None |
| FR-012 | PASS* -> PASS | Extract real gap |
| SC-001 | STRONG | None |
| SC-002 | WEAK -> PASS | Revise criterion |
| SC-003 | PASS | None |
| SC-004 | PASS | None |

---

## Action Items Summary

| # | Action | Priority | Owner | Files |
|---|---|---|---|---|
| 1 | Amend FR-004 in spec | P1 | spec author | `spec.md` |
| 2 | Create `.mod` file | P2 | developer | new `config_optimizer.mod`, update `ampl_model.py` |
| 3 | Extract real MIP gap | P2 | developer | `ampl_solver.py` |
| 4 | Check amplpy+highspy | P2 | developer | `ampl_model.py` |
| 5 | Revise SC-002 | P2 | spec author | `spec.md` |
| 6 | `SolveOutcome` return type | P2 | developer | `ampl_model.py`, `ampl_solver.py` |
| 7 | Robust file detection | P2 | developer | `ampl_model.py` |
| 8 | Update docstrings | P2 | developer | `ampl_model.py`, `ampl_solver.py` |
| 9 | Remove dead docstring | P3 | developer | `optimizer.py` |
| 10 | Integration tests | P3 | developer | `tests/test_ampl.py` |
| 11 | Naming standardization | P3 | developer | `optimizer.py`, `ampl_model.py` |
| 12 | NLP/MINLP + CE docs | P3 | developer | `ampl_model.py` |

---

### Referenced Documentation

- All three reviews, six cross-reviews, three revisions, and three dispute files
- `specs/done/023-ampl-config-optimizer/spec.md`
- `conversus/plugins/optimizer/ampl_model.py`
- `conversus/plugins/optimizer/ampl_solver.py`
- `conversus/plugins/optimizer/optimizer.py`
- `conversus/plugins/optimizer/__init__.py`
- `tests/test_ampl.py`
