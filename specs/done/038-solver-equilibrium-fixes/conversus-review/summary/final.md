# Spec 038 — Solver & Equilibrium Fixes: Final Synthesis

**Date**: 2026-04-01
**Deliberation**: 3 agents, 5 phases, 1 round
**Spec**: 038-solver-equilibrium-fixes
**Files**: scorer.py, solver.py, payoffs.py

---

## 1. Process Summary

| Agent | Role | Key Findings |
|---|---|---|
| **game-theorist** | Mathematical correctness | WTA N x 1 produces trivial equilibria; 4 new modes lack payoff functions |
| **documentation-auditor** | Spec accuracy | Code documentation is exemplary; spec documents are stale |
| **spec-compliance** | Compliance audit | 1/3 items MET; 2/3 are documentation tasks not yet done |

---

## 2. Recommendation Scorecard

### Unanimous

| ID | Priority | Recommendation | Status |
|---|---|---|---|
| RE-3 | IMPLEMENTED | Cooperative payoff matrix documented as heuristic | solver.py:118-135 |
| RE-2 | **P2** | Write spec 021 amendment: recommend N x N for WTA, not N x 1 | Spec document task |
| NEW-3 | **P3** | Update spec 024 section 8 to reflect execute_hooks orchestration | Spec document task |

### Required Elsewhere

| ID | Priority | Recommendation | Target |
|---|---|---|---|
| PAYOFF-NEW | **P1** | Add payoff functions for negotiation, resource-allocation, fair-division, mechanism-design | New spec (payoff expansion) |
| WTA-NxN | **P2** | Change WTA matrix from N x 1 to N x N (code change) | Spec 021 amendment |

---

## 3. Success Criteria

| SC | Verdict |
|---|---|
| SC-001 | **NOT MET** — spec 021 table not yet amended |
| SC-002 | **MET** — cooperative documented as heuristic |
| SC-003 | **NOT MET** — spec 024 section 8 not updated |

---

## 4. Convergence

All agents converged in Round 1. Key concession: documentation-auditor accepted broader framing of RE-2 (not just documentation, also code design issue).

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
## 5. Remaining Disputes

**None.** All disputes resolved.

The most significant finding is out-of-scope: payoff functions are missing for 4 new modes (negotiation, resource-allocation, fair-division, mechanism-design), causing the equilibrium scorer to silently fail for these modes. This is classified as REQUIRED-ELSEWHERE.
<!-- CONVERSUS:DISPUTES_END -->

---

## 6. Implementation Completeness

**1 of 3 spec items is implemented** (RE-3 via documentation). RE-2 and NEW-3 are documentation deliverables that have not been written. The code is correct — the gap is in the spec documents.

**Recommended**: Write the RE-2 spec amendment (including N x N recommendation) and update spec 024 section 8.

## 7. Cross-Spec Impact

The game-theorist identified that the equilibrium scorer silently fails for 4 new modes because `PAYOFF_FUNCTIONS` in payoffs.py only covers the original 4 modes. This is a **P1 cross-spec gap** that affects specs 017, 021, and 028. A new spec should be created to add payoff functions for the new modes.
