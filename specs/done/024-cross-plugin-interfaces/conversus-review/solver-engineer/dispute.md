# Solver-Engineer Dispute — Spec 024: Cross-Plugin Interfaces

**Reviewer**: solver-engineer
**Round**: 1, Phase 4 (Dispute)
**Date**: 2026-04-01

**Inputs**: All three revisions (plugin-architect, solver-engineer, spec-compliance).

---

## Resolved Disputes

### RD-1. SC-001 verdict: PARTIAL

Spec-compliance revised to PARTIAL (revision R1). Plugin-architect maintained this position throughout. I concur. The data flow is wired but the numerical benefit is not delivered. Resolved.

### RD-2. Q/R dimension mismatch severity

I revised from P1-Critical to P2-Important (revision R1). Plugin-architect also revised to "latent API defect." Spec-compliance considers it P2 from a compliance standpoint. All three agree: fix the API contract defensively, but it is not currently triggered. Resolved.

### RD-3. Zero-score sentinel

All three reviewers agree the `any(s != 0.0)` gate is wrong. Spec-compliance proposes SC-006 (revision N1) to make the fix testable. I endorse this. Resolved.

### RD-4. Duplicate producer detection

Adopted from plugin-architect and spec-compliance (my revision N1). All agree on `DuplicateProducerError`. Resolved.

### RD-5. Signal double-counting diagnostic

Plugin-architect adopted this (their revision N1). I proposed the innovation magnitude ratio metric (my revision N2). No disagreement on the approach. Resolved at P2.

---

## Active Disputes

### AD-1. Noise calibration (R5) is within spec scope

**My position**: `R[2][2] = 0.005` is miscalibrated and should be `0.05`. P2-Important.

**Spec-compliance position** (revision M3): "Parameter tuning outside the spec's scope." Spec-compliance correctly notes the spec does not specify noise values and this is not a compliance concern.

**Why I maintain**: I accept that spec-compliance's review scope does not cover calibration. But the spec's goal is quality improvement from 3D. Miscalibrated noise means the 3D path trusts eq_score 10x too much, producing overconfident predictions. This directly undermines the spec's motivating purpose. I do not ask spec-compliance to change their scope -- I ask that this be recorded as a P2-Important item in the synthesis, attributed to the solver-engineer's domain expertise, even if it is outside the compliance scope.

**Path to resolution**: This is not truly a dispute -- it is a scope boundary. I accept that spec-compliance cannot validate noise values. The item should appear in the synthesis as a solver-engineer recommendation, not as a compliance finding.

### AD-2. Masked observation approach (R2) requires spec work

**My position**: When historical equilibrium scores are unavailable, use 2D observations for those rounds and 3D for rounds with data. This is the mathematically correct approach.

**Spec-compliance position** (revision N3): "The masked observation approach creates behavior not defined by any FR or SC. A spec addendum or follow-up spec should define the expected behavior."

**Plugin-architect position**: Did not directly address. Revised to accept that replicated scores cause overconfidence rather than degradation, but did not endorse or reject the masked approach.

**Why I maintain**: I agree a spec addendum is needed. But the fix should not be deferred until a spec is written -- the spec can be amended after the implementation validates the approach. The current behavior (replicate the single score) is demonstrably wrong. The masked approach, while more complex, is the only numerically sound alternative to simply disabling the 3D path until accumulation is implemented.

**Path to resolution**: Pragmatic compromise: implement score accumulation (R3, all three agree) first. Once historical scores are available, the masked approach becomes unnecessary for most cases (only the first round would lack prior data). The masked approach can be deferred to a follow-up. I accept this ordering.

---

## Consensus Summary

The following items are now fully agreed across all three reviewers:

1. **SC-001 is PARTIAL** -- data flow correct, quality benefit unrealized.
2. **Score accumulation is P1-Critical** -- all three agree, highest priority fix.
3. **Zero-score sentinel is wrong, SC-006 needed** -- all three agree.
4. **Q/R dimension mismatch is P2** -- latent API defect.
5. **Duplicate producer detection with DuplicateProducerError** -- all three agree.
6. **3D Kalman end-to-end test needed** -- P2, adopted by spec-compliance.
7. **Signal double-counting diagnostic** -- plugin-architect and solver-engineer agree.
8. **Immutable produced value types** -- plugin-architect and solver-engineer agree.
9. **Spec section 8 text is stale** -- spec-compliance and plugin-architect agree.

Remaining disputes: AD-1 (noise calibration scope) and AD-2 (masked observation approach timing). Both have proposed paths to resolution: AD-1 is a scope boundary, not a disagreement; AD-2 is resolved by implementing accumulation first.

The cross-hook lifetime dispute (plugin-architect AD-1 vs. spec-compliance M1) is not my dispute, but I note both positions are defensible. The plugin-architect's compromise (test + prominent docstring) seems reasonable.
