# Cross-Spec Consistency Audit — Wave 034-038

**Auditor**: consistency-auditor
**Date**: 2026-04-01
**Specs reviewed**: 034, 035, 036, 037, 038
**Implementation files verified**: convergence.py, kalman.py, predictor.py, base.py, construction.py, modes.py, validation.py, solver.py, payoffs.py, scorer.py

---

## Executive Summary

Five spec syntheses were audited for internal contradictions, priority consistency, shared interface agreement, and cross-spec findings. The overall quality is high: all specs converged in Round 1, with zero unresolved disputes. The most significant cross-spec finding is the missing payoff functions for 4 new modes (identified in spec 038 but affecting specs 017, 021, 028, 036).

---

## Cross-Spec Consistency Findings

### CSI-1: VALID_MODES is consistent across all specs [CONSISTENT]

Spec 036 consolidated VALID_MODES into `modes.py`. Specs 034 (predictor), 035 (plugin base), 037 (validation), and 038 (scorer) all reference modes. All 8 modes are consistently defined across the codebase. No contradictions.

### CSI-2: Equilibrium score flow — specs 034 + 035 + 038 [CONSISTENT with gap]

The eq_score flows through three specs:
- **Spec 038/017** (scorer): Produces `equilibrium_score` via `EquilibriumScorer.produces`
- **Spec 035** (plugin framework): Routes via `execute_hooks` topological sort
- **Spec 034** (convergence): Consumes via `ConvergencePredictor.consumes`

All three specs agree on the interface. The gap: scorer silently fails for 4 new modes (spec 038 F-4), which means the predictor gets None for those modes and falls back to 2D Kalman. This is graceful degradation, not a contradiction, but it means convergence prediction is weaker for new modes.

### CSI-3: Priority scales are consistent [CONSISTENT]

All 5 specs use P1/P2/P3 or CRITICAL/HIGH/MEDIUM/LOW with consistent semantics. No priority inflation or deflation observed.

### CSI-4: "REQUIRED-ELSEWHERE" classification used correctly [CONSISTENT]

Three items were classified as REQUIRED-ELSEWHERE:
- Spec 034: Engine persistence of plugin_results (engine pipeline spec)
- Spec 036: D-5 spec 028 text amendment (spec 028 scope)
- Spec 038: Missing payoff functions for new modes (new spec needed)

All three are correctly scoped — the items ARE required for system correctness but belong in different specs. None were used to hide deferrals.

### CSI-5: Missing payoff functions affect multiple specs [CROSS-CUTTING GAP]

Spec 038's game-theorist identified that `PAYOFF_FUNCTIONS` in payoffs.py only covers 4 of 8 modes. This affects:
- **Spec 017** (equilibrium scoring): Scorer fails for 4 modes
- **Spec 021** (solver): Solver cannot compute equilibria for 4 modes
- **Spec 028** (mode expansion): New modes are incomplete without payoff functions
- **Spec 034** (convergence): eq_score dimension unavailable for 4 modes

This is the most significant cross-spec gap in the wave.

---

## Concession Audit

### Spec 034
- plugin-integration-engineer conceded F-4 (history roundtrip) from P1 to REQUIRED-ELSEWHERE: **VALID** — engine persistence is not a spec 034 responsibility.
- kalman-mathematician conceded F-9 upgrade from P2 to P1: **VALID** — crash prevention justifies P1.

### Spec 035
- safety-engineer withdrew sentinel suggestion: **VALID** — over-engineering for current scale.

### Spec 036
- No significant concessions. All findings accepted without challenge.

### Spec 037
- No concessions. Full agreement from Round 1.

### Spec 038
- documentation-auditor conceded broader framing of RE-2: **VALID** — N x 1 WTA does produce trivial equilibria.

All concessions were evidence-based. No concessions were made under social pressure.

---

## Recommendations

1. **Create a new spec** for payoff function expansion to cover negotiation, resource-allocation, fair-division, mechanism-design. This is the highest-priority cross-spec gap.
2. **Write the spec 021 amendment** for WTA matrix shape (spec 038 RE-2 deliverable).
3. **Update spec 024 section 8** text (spec 038 NEW-3 deliverable).
4. **Write the M-2 cross-hook scoping test** (spec 035 deliverable).
