# Plugin-Architect Revision — Spec 024: Cross-Plugin Interfaces

**Reviewer**: plugin-architect
**Round**: 1, Phase 3 (Revision)
**Date**: 2026-04-01

**Inputs**: Own review, cross-reviews received (solver-engineer, spec-compliance), cross-reviews written (about solver-engineer, spec-compliance).

---

## Positions Revised

### R1. Downgrade Q/R dimension mismatch from "active corruption bug" to "latent API defect"

**Original position** (O3): Stated that calling `run_kalman_filter(observations_3d)` without explicit Q/R produces "a corrupted matrix" and framed this as a currently triggered bug.

**Revision**: The solver-engineer (Alignment 5, cross-review DC-2 from solver-engineer) correctly points out that `_predict_convergence_kalman` always passes explicit 3x3 Q/R, so the `default_Q()` path is never triggered for 3D data in the current codebase. My original framing overstated the immediacy. The bug is real in the `run_kalman_filter` API -- any future caller that omits Q/R with 3D data will get silent corruption -- but it is not currently triggered. I maintain P1 severity because API contracts should be self-defending, but I retract the claim that this is an active data corruption path.

### R2. Refine "fabricated data" characterization of replicated scores

**Original position** (M5): Stated the Kalman filter "is operating on fabricated data for all but the latest observation, which mathematically degrades the state estimate rather than improving it."

**Revision**: The solver-engineer's cross-review (DC-3) provides a more precise mathematical characterization: replicated scores create "a false prior that biases the filter toward the most recent value" and "artificially shrinks covariance." This is overconfidence, not necessarily degradation of point estimates. I was imprecise. The correct statement is: the 3D path with replicated scores produces overconfident predictions whose point estimates may be reasonable but whose uncertainty bounds are poorly calibrated. This still justifies P1 for the accumulation fix but does not support my implied recommendation to disable the 3D path with limited data.

### R3. Accept that the hardcoded Q/R values in my fix proposal need calibration

**Original position** (P1): Proposed `Q = [[1.0, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.01]]` with `0.01` for the eq_score dimension.

**Revision**: The solver-engineer (R5) argues that eq_score compounds multiple noise sources and should have `R[2][2] = 0.05` (10x concession noise). My hardcoded values underestimate eq_score uncertainty. I withdraw the specific matrix values and defer to the solver-engineer's calibration analysis. The structural fix (auto-size from observation dimension) remains valid; the specific noise values should be determined by the solver-engineer.

### R4. Narrow the scope of the deep-copy recommendation

**Original position** (O2, P3): Recommended `copy.deepcopy(result.data[key])` for all produced values.

**Revision**: The solver-engineer's silence on this issue (noted in my cross-review DC-4 of solver-engineer → plugin-architect) and spec-compliance's non-mention both suggest the practical risk is currently low since all produced values are floats and strings. I revise to: document that produced values MUST be immutable types (primitives, frozen dataclasses), and add a runtime check that rejects mutable containers in `result.data` values. This is cheaper than deepcopy and catches the problem at the source rather than the consumption point.

---

## Positions Maintained

### M1. SC-001 MET verdict is misleading (DISPUTE)

Spec-compliance marks SC-001 as MET. I maintain that SC-001's intent is not merely "the predictor syntactically reads the score" but "the predictor gains quality from the score." The single-element replicated list, the zero-score conflation, and (per the solver-engineer) the potential signal double-counting all mean the 3D path's quality benefit is unrealized. SC-001 should be PARTIAL: the wiring is correct, the numerical benefit is not yet delivered.

**Why maintained**: Spec-compliance's cross-review (DC-1 from spec-compliance → plugin-architect) acknowledges the tension but frames it as ambiguity in what "uses" means. I argue the spec's motivation section (lines 7-8, 16-19) makes the intent clear: the quality regression should be fixed. A syntactic pass-through that delivers fabricated data does not fix the quality regression.

### M2. Cross-hook lifetime should be a formal FR, not just a docstring

Spec-compliance recommends a docstring note (recommendation 3). I maintain that a formal FR is necessary because the behavior is load-bearing: if the engine changes cross-hook semantics, plugins that rely on re-production at multiple hooks (like the scorer) would silently break. A docstring does not create a test obligation; an FR does.

**Why maintained**: Spec-compliance's cross-review (DC-3) correctly notes that an FR extends the spec's scope. I accept this cost. The alternative -- undocumented behavior that works by coincidence -- is worse for long-term maintenance.

### M3. Namespace collision prevention is important even though only one producer exists today

The solver-engineer does not mention this at all. Spec-compliance agrees it matters. I maintain P2-High for duplicate producer detection and add that a namespace convention should be recommended in the spec (even if not enforced at runtime initially).

**Why maintained**: The plugin ecosystem will grow. Catching collisions after they cause silent data corruption is far more expensive than preventing them.

### M4. The self-nesting pattern is an architectural smell

Spec-compliance calls it "correct" and "necessary." I maintain it is an architectural smell. The orchestrator should not force every producer to know its own key name and manually copy values. The convention could be changed so that `execute_hooks` stores the entire `result.data` under `f"{plugin.name}.{key}"` or extracts keys from a declarative mapping. I accept spec-compliance's point that this is a design preference, not a bug, but I maintain it as a P3 recommendation.

---

## New Positions

### N1. The solver-engineer's signal double-counting concern (Off-Base 1) deserves investigation

The solver-engineer argues that eq_score may partially duplicate concession_rate signal, meaning 3D could inflate confidence without improving accuracy. This was not in my original review. I now consider this a P2 concern: before the 3D path ships as the default, a diagnostic comparing 2D vs 3D innovation magnitudes should be implemented to validate the spec's central claim.

### N2. Accept the solver-engineer's R6 initial covariance recommendation

The solver-engineer's argument that initial P variance of 1.0 for eq_score is too wide relative to the [0,1] range is sound. I did not address initial covariance in my review. I now endorse `0.25` (std = 0.5) as more appropriate.

---

## Summary of Priority Changes

| Item | Original Priority | Revised Priority | Reason |
|------|------------------|-----------------|--------|
| Q/R dimension mismatch | P1-Critical (active bug) | P1-Critical (latent API defect) | Not currently triggered but must be fixed |
| Zero-score sentinel | P1-Critical | P1-Critical | Unchanged |
| Score accumulation | P1-Critical | P1-Critical | Unchanged, but characterization refined |
| Duplicate producer detection | P2-High | P2-High | Unchanged |
| Cross-hook lifetime FR | P2-High | P2-High | Unchanged, dispute with spec-compliance |
| Deep copy / immutability | P3-Medium | P3-Medium (narrowed to type enforcement) | Practical risk currently low |
| Signal double-counting diagnostic | (new) | P2-High | Adopted from solver-engineer |
