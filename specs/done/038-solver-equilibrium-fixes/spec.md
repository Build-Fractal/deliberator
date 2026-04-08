# Feature Specification: Solver & Equilibrium Fixes

**Feature ID**: `038-solver-equilibrium-fixes`
**Created**: 2026-04-01
**Status**: Done — 2026-04-02 — spec amendments only, no code changes
**Docs Update**: Update docs/developer-guide/architecture.md solver section; update docs/api/plugins/nashopt.md if payoff matrix docs change
**Files**: `conversus/plugins/nashopt/scorer.py`, `solver.py`, `payoffs.py`, spec docs

---

## Items (3)

### MEDIUM
- **RE-2**: Spec 021 matrix shape inconsistency. Spec Section 2 table says WTA is N×1, but the nashopt API expects N×N. The code matches the table, not the API. Write a spec amendment resolving the inconsistency.
- **RE-3**: Cooperative diagonal semantics. Mixing `surviving_count` (diagonal) with `agreement_matrix` (off-diagonal) produces uninterpretable equilibria. Either use agreement_matrix for both, or document as heuristic-only.

### LOW
- **NEW-3**: Update spec 024 section 8 text. Says "does NOT implement orchestration" but `execute_hooks` now does minimal orchestration.

## Success Criteria
- SC-001: Spec 021 matrix shape table matches the code AND the API.
- SC-002: Cooperative payoff matrix is documented as heuristic OR uses consistent data sources.
- SC-003: Spec 024 section 8 accurately describes what was implemented.
