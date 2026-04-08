# Plugin-Integration-Engineer — Phase 3 Revision

**Incorporating cross-review feedback from**: kalman-mathematician, spec-compliance

---

## Revisions

### F-4 (History roundtrip): Downgrade to P2 / REQUIRED-ELSEWHERE

Both reviewers argue that this belongs in the engine pipeline spec, not spec 034. I accept this classification. The failure mode (silent 2D fallback instead of 3D Kalman) is a degradation, not a crash. The system remains correct, just suboptimal.

**Revised priority**: P2 / REQUIRED-ELSEWHERE (engine pipeline spec).
**Action**: Create a tracking item for the engine spec to verify plugin_results persistence into RoundState.

### F-3 (plugin_results scoping): Downgrade to P3

Both reviewers agree this is mitigated by current architecture. Relabel as documentation item.

**Revised priority**: P3 (documentation).

### New: Q/R passthrough gap confirmed

The kalman-mathematician did not initially catch this, but it is a real gap. The `predict_convergence` function accepts Q/R, but the `ConvergencePredictor.execute()` method does not read Q/R from plugin_config.

**Priority**: P3 — the auto-sizing defaults work for all current use cases. This only matters for expert tuning.

### New: None-to-last-known carry-forward (from kalman-mathematician cross-review)

I accept the mathematician's observation that carrying forward the last known eq_score for absent rounds (convergence.py:298-301) introduces correlation in the observation sequence. This is a modeling decision, not a bug. For 2-5 round sequences, the impact is negligible.

**Priority**: P3 — document the modeling assumption.

## Concessions

- F-4 downgraded from P1 to P2 / REQUIRED-ELSEWHERE.
- F-3 downgraded from P2 to P3.

## Maintained Positions

- F-6 (test coverage gaps) remains P2 — multi-round integration tests are needed for confidence.
