# Solver & Equilibrium Review — Phase 1

**Agent**: game-theorist
**Spec**: 038-solver-equilibrium-fixes
**Date**: 2026-04-01
**Files reviewed**: scorer.py, solver.py, payoffs.py, spec docs

---

## Executive Summary

The equilibrium scoring system has solid fundamentals but contains a documented heuristic approximation in cooperative mode that limits the game-theoretic validity of the Nash equilibrium check. The spec correctly identifies this and the two matrix shape issues.

---

## Findings

### F-1: Spec 021 matrix shape inconsistency [MEDIUM — RE-2]

**Location**: solver.py:167-195 (`_build_wta_matrix`)
**Status**: DOCUMENTED in code

The WTA matrix builder returns an N x 1 matrix (each agent gets a single payoff based on ranking position). The spec 021 Section 2 table says WTA is N x 1, which matches the code. However, the nashopt API `check_equilibrium()` expects an N x N matrix for proper equilibrium analysis (each agent's payoff must depend on OTHER agents' strategies, not just their own).

The current N x 1 form treats WTA as a single-column game where agents have only one "action" each. This trivially makes every agent at equilibrium (with one action, you can't deviate). The equilibrium check becomes meaningless.

**Spec 038 asks**: Write a spec amendment resolving the inconsistency.
**My assessment**: The code should be amended to produce an N x N matrix where entry (i, j) represents agent i's payoff when agent j wins. This gives agents a meaningful strategy space.

**Priority**: P2 — the current form produces trivial results.

### F-2: Cooperative diagonal semantics [MEDIUM — RE-3]

**Location**: solver.py:107-164, docstring warning at lines 118-135
**Status**: DOCUMENTED with warning

The cooperative payoff matrix mixes two data sources:
- **Diagonal**: `surviving_count` (how many of the agent's recommendations survived)
- **Off-diagonal**: `agreement_matrix` (pairwise agreement scores)

This produces a valid matrix but the Nash equilibrium computed on it is a heuristic stability measure, not a game-theoretic equilibrium. The issue is that the diagonal (self-payoff) uses a different metric than the off-diagonal (interaction), so the payoff structure does not represent a consistent game.

The code already includes a comprehensive docstring warning (lines 118-135) that says "HEURISTIC APPROXIMATION" and explains the issue.

**Spec 038 asks**: Either use agreement_matrix for both, or document as heuristic-only.
**My assessment**: The documentation approach is taken (docstring warning). The alternative (using agreement_matrix for diagonal) would require the agreement_matrix to have self-agreement entries, which it currently may not.

**Priority**: P2 — the heuristic label is correct. The documentation is already present. The remaining work is to ensure the spec document matches the code's heuristic label.

### F-3: Spec 024 section 8 text [LOW — NEW-3]

**Location**: Not visible in implementation files (spec document issue)
**Status**: DOCUMENTATION TASK

Spec 024 section 8 says "does NOT implement orchestration" but `execute_hooks` in base.py now does minimal orchestration (topological sort, per-plugin state management, result accumulation). The spec text is stale.

**Verdict**: NEW-3 is a documentation task, not a code change.

### F-4: Payoff function coverage for new modes [OBSERVATION]

**Location**: payoffs.py:225-230 (`PAYOFF_FUNCTIONS`)
**Status**: LIMITED

`PAYOFF_FUNCTIONS` only has entries for the original 4 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue). The new 4 modes (negotiation, resource-allocation, fair-division, mechanism-design) have no payoff functions.

The heuristic scorer (`_compute_equilibrium_score_heuristic` in scorer.py) calls `compute_payoff` which dispatches to `PAYOFF_FUNCTIONS`. If the mode is one of the new 4, `compute_payoff` raises `ValueError`.

The scorer handles this via the mode validation check at scorer.py:371: `if state.mode not in VALID_MODES` returns an error. But `VALID_MODES` includes the new modes. The scorer's VALID_MODES check passes, then the payoff function raises.

This is caught by the outer exception handler (scorer.py:391-402) and returns a partial error result. Not a crash, but the equilibrium scorer silently fails for 4 of 8 modes.

**Priority**: P1 — this is a functional gap. The scorer claims to support modes it cannot score.

**Spec 038 scope**: This item is NOT in spec 038. It belongs in a separate spec or as a spec 038 addition.

---

## Game-Theoretic Assessment

| Mode | Payoff Quality | Equilibrium Validity |
|---|---|---|
| cooperative | Heuristic (mixed data sources) | Low — heuristic stability, not Nash |
| winner-take-all | Trivial (N x 1) | None — single action = trivial equilibrium |
| prisoners-dilemma | Good (territory + penalty) | Moderate — captures overreach dynamics |
| red-blue | Good (severity-weighted) | Moderate — zero-sum structure is correct |
| negotiation | MISSING | N/A |
| resource-allocation | MISSING | N/A |
| fair-division | MISSING | N/A |
| mechanism-design | MISSING | N/A |
