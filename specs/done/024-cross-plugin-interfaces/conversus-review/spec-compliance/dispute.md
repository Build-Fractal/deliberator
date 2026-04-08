# Spec-Compliance Dispute — Spec 024: Cross-Plugin Interfaces

**Reviewer**: spec-compliance
**Round**: 1, Phase 4 (Dispute)
**Date**: 2026-04-01

**Inputs**: All three revisions (plugin-architect, solver-engineer, spec-compliance).

---

## Resolved Disputes

### RD-1. SC-001 verdict: PARTIAL

I revised to PARTIAL in Phase 3 (revision R1). Both plugin-architect and solver-engineer maintained this position and acknowledge my revision. Fully resolved.

### RD-2. Q/R dimension mismatch severity

All three agree: P2-Important, latent API defect. Resolved.

### RD-3. Zero-score sentinel and SC-006

All three agree the `any(s != 0.0)` gate is wrong. My proposed SC-006 (revision N1) is endorsed by the solver-engineer (dispute RD-3) and not contested by the plugin-architect. Resolved.

### RD-4. Duplicate producer detection

All three agree on `DuplicateProducerError`. Resolved.

### RD-5. Score accumulation is P1-Critical

All three agree. Resolved.

---

## Active Disputes

### AD-1. Cross-hook lifetime: FR-011 vs. docstring + test (NARROWED)

**My position** (revision M1): A docstring note is sufficient. A formal FR expands scope and constrains future designs.

**Plugin-architect position** (dispute AD-1): Proposes a compromise: add a test that verifies plugin_results scoping + a prominent docstring note, without a formal FR.

**Resolution**: I accept the compromise. A dedicated test in `test_cross_plugin.py` that verifies `plugin_results` is reset between hook invocations, combined with a prominent docstring note, achieves the plugin-architect's goals (explicit coverage, documentation) without my concern (scope expansion, rigidity). This dispute is resolved by the plugin-architect's compromise proposal.

### AD-2. Noise calibration scope boundary

**Solver-engineer position** (dispute AD-1): R5 should be recorded in the synthesis as a P2 solver-engineer recommendation even though it is outside compliance scope.

**My position**: I accept this framing. I do not contest the solver-engineer's domain expertise on noise calibration. The synthesis should attribute it correctly: this is a numerical engineering recommendation, not a compliance finding. I cannot validate whether `0.05` is the right value, but I do not dispute that the solver-engineer's analysis is sound.

**Resolution**: Effectively resolved. The solver-engineer accepts it is outside compliance scope; I accept it should be in the synthesis. No remaining disagreement.

---

## Consensus Summary

The following items are now fully agreed across all three reviewers:

1. **SC-001 is PARTIAL** -- wiring correct, quality benefit unrealized.
2. **SC-002 is MET with caveat** -- zero-score edge case validates wrong behavior.
3. **SC-003 through SC-005 are MET** -- unchanged.
4. **FR-001 through FR-010 are all MET** -- unchanged.
5. **Score accumulation is P1-Critical** -- all agree.
6. **Zero-score sentinel fix + SC-006** -- all agree.
7. **Q/R dimension mismatch is P2** -- latent API defect.
8. **Duplicate producer detection with DuplicateProducerError** -- all agree.
9. **3D Kalman end-to-end test** -- P2, all agree.
10. **Cross-hook lifetime: test + docstring** -- compromise accepted by plugin-architect and spec-compliance.
11. **Signal double-counting diagnostic** -- P2, plugin-architect and solver-engineer agree.
12. **Noise calibration** -- P2, solver-engineer recommendation (outside compliance scope).
13. **Produced values should be immutable types** -- P3, plugin-architect and solver-engineer agree.
14. **Spec section 8 text is stale** -- should be updated to reflect that orchestration was implemented.

All disputes from Phase 3 are either resolved or narrowed to scope-boundary clarifications that have agreed-upon framings. No remaining genuine disagreements. I recommend termination after Phase 5 synthesis -- no Round 2 is needed.
