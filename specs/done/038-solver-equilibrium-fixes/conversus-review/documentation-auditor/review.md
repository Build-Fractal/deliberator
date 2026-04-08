# Solver & Equilibrium Review — Phase 1

**Agent**: documentation-auditor
**Spec**: 038-solver-equilibrium-fixes
**Date**: 2026-04-01
**Files reviewed**: scorer.py, solver.py, payoffs.py, spec docs

---

## Executive Summary

The code documentation quality is high — comprehensive docstrings, clear warnings for heuristic approximations, and well-structured module-level documentation. The spec accuracy issues (RE-2, RE-3, NEW-3) are all documentation concerns, and the code-side documentation is already ahead of the spec documents.

---

## Findings

### F-1: Spec 021 matrix shape — code documentation vs. spec [MEDIUM — RE-2]

**Code documentation**: solver.py:167-177 docstring says "N x 1 ranking payoff vector for winner-take-all mode." This accurately describes what the code does.

**Spec documentation**: Spec 021 Section 2 table says WTA is N x 1. This matches the code.

**API documentation**: nashopt's `check_equilibrium()` expects different shapes depending on the game form. The spec 021 table was written to describe the heuristic path, not the solver path.

**Gap**: The spec should clarify that the N x 1 form is the heuristic representation, and the solver path may need N x N. The code should include a comment noting the API expectation.

**Verdict**: RE-2 is a spec-vs-API documentation gap, not a code bug.

### F-2: Cooperative heuristic documentation [MEDIUM — RE-3]

**Code documentation**: solver.py:118-135 has an excellent "HEURISTIC APPROXIMATION" warning block that:
1. Labels the matrix as a heuristic
2. Explains the mixed data sources
3. References spec 038 RE-3
4. States that the Nash equilibrium is a "heuristic stability measure, not a theoretically grounded equilibrium"

This is exemplary documentation of a known limitation.

**Spec documentation**: Spec 038 asks to "document as heuristic OR use consistent data sources." The code already documents it as heuristic.

**Verdict**: RE-3 is addressed in code documentation. The spec document should be updated to match (mark this item as resolved via documentation).

### F-3: Spec 024 section 8 text staleness [LOW — NEW-3]

**Current text**: "does NOT implement orchestration"
**Reality**: `execute_hooks` in base.py:412-527 does implement minimal orchestration (topological sort, per-plugin state management).

The spec text is stale. The code has evolved past the spec's description.

**Verdict**: NEW-3 is a spec document update. The code is correct; the spec is stale.

### F-4: Module-level docstrings are comprehensive [OBSERVATION]

All reviewed files have detailed module-level docstrings:
- solver.py: Documents optional imports, pure-function design, fallback behavior
- payoffs.py: Documents payoff function contracts and return types
- scorer.py: Documents solver dispatch, timeout, hook points

**Rating**: Excellent documentation quality.

### F-5: TODO comments for deferred work [OBSERVATION]

- kalman.py:362-365: Joseph form TODO (spec 034 NEW-6)
- solver.py:118-135: Heuristic warning (spec 038 RE-3)

TODOs reference specific spec items, which makes them traceable. Good practice.

---

## Spec Accuracy Assessment

| Spec Item | Code Status | Spec Doc Status | Gap |
|---|---|---|---|
| RE-2 (matrix shape) | Code matches spec table | API expectation differs | Spec needs clarification |
| RE-3 (cooperative heuristic) | Documented in code | Spec asks for resolution | Spec should mark resolved |
| NEW-3 (spec 024 section 8) | Code evolved past spec | Spec text is stale | Spec needs update |
