# Feature Specification: Payoff Functions for New Modes

**Feature ID**: `039-new-mode-payoffs`
**Created**: 2026-04-01
**Status**: Done — 2026-04-02
**Docs Update**: Update docs/user-guide/modes.md with solver scoring for new modes; update docs/api/plugins/nashopt.md with new payoff function signatures; update docs/developer-guide/game-forms.md with Bayesian/coalitional/mechanism game form→payoff mapping
**Depends On**: `028-mode-expansion` (4 new modes), `025-game-form-expansion` (coalitional, Bayesian forms), `021-nashopt-integration` (solver wrapper)
**Origin**: Cross-spec P1 from spec 038 review — "required-elsewhere" item. EquilibriumScorer has payoff functions for 4 original modes but not for negotiation, resource-allocation, fair-division, or mechanism-design.

---

## 1. Feature Summary

Add per-mode payoff functions for the 4 new modes so the EquilibriumScorer can score deliberations in all 8 modes, not just the original 4.

## 2. New Payoff Functions

| Mode | Payoff Structure | Game Form |
|------|-----------------|-----------|
| negotiation | ZOPA coverage × party satisfaction | Bayesian |
| resource-allocation | Utilization efficiency - allocation inequality | Coalitional (Shapley) |
| fair-division | Proportionality score - envy count | Coalitional |
| mechanism-design | Social welfare - gaming vulnerability count | Mechanism design |

## 3. Functional Requirements
- FR-001: Each new mode MUST have a payoff function in `conversus/plugins/nashopt/payoffs.py`
- FR-002: Each payoff function MUST return `(payoff, best_response_payoff)` tuple (same interface as existing 4)
- FR-003: `compute_payoff()` dispatcher MUST route all 8 modes
- FR-004: Feature extraction (spec 015) MUST extract the features each payoff function needs
- FR-005: Tests MUST cover each new payoff function with representative feature data

## 4. Success Criteria
- SC-001: EquilibriumScorer produces valid scores for all 8 modes
- SC-002: Payoff functions for new modes follow the same pattern as existing 4
