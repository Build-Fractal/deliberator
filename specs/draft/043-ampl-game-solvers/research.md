# AMPL Game-Theoretic Integration Research

**Date**: 2026-04-03
**Context**: Honest analysis found conversus-ampl is shallow — one MIP that's really a grid search in disguise. This research identifies where AMPL adds genuine value.

## TL;DR

6 of 8 modes can be formulated as real optimization problems solvable by AMPL/HiGHS in 50-500ms. The current config optimizer should be refactored into a game solver library.

## Priority Ranking

### Phase 1 — High-impact, low-risk (~2 weeks)
1. **Cooperative** (LP) — Nash equilibrium via mixed strategy LP
2. **Red-Blue** (LP minimax) — textbook minimax, fast, clear interpretation
3. **Prisoners-Dilemma** (LP complementarity) — validates the integration pattern

### Phase 2 — Medium-impact (~3 weeks)
4. **Winner-Take-All** (MIP tournament) — consistent ranking from score differentials
5. **Fair-Division** (MIP envy-free) — exact envy-free allocation

### Phase 3 — Deferred (needs feature extraction work)
6. **Resource-Allocation** (LP + Shapley) — O(2^n) coalitions for Shapley
7. **Negotiation** (NLP Nash bargaining) — needs ZOPA bounds from features
8. **Mechanism-Design** (MIP VCG) — needs review score → valuation mapping

## Solver Requirements
- **HiGHS** (bundled): covers LP/MIP for modes 1-5
- **Gurobi** (optional): better MIP for fair-division with m>100 items
- **Ipopt** (optional): NLP for negotiation Nash bargaining

## Key Insight
The current AMPL integration enumerates 135 grid points and asks HiGHS to pick the best one. Real AMPL value comes from formulating the GAME THEORY as optimization, not the config search.

See full research in agent output for: AMPL model snippets per mode, integration architecture, performance estimates, risks, and implementation checklist.
