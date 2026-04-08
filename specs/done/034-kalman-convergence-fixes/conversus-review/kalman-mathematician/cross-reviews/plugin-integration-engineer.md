# Cross-Review of plugin-integration-engineer

**Reviewer**: kalman-mathematician
**Reviewing**: plugin-integration-engineer's Phase 1 review

---

## Agreements

- **F-1 (eq_score accumulation)**: Agree the wiring is correct. The accumulation pattern is sound.
- **F-2 (consumes declaration)**: Agree the `produces`/`consumes` alignment is correct.
- **F-5 (Kalman fallback)**: Agree the try/except fallback to OLS is correct defensive design.

## Challenges

### On F-4 (History roundtrip — engine responsibility)

The plugin-integration-engineer raises this as P1. I agree it is a real concern, but I would rate it **REQUIRED-ELSEWHERE** rather than P1 for spec 034. Spec 034's scope is the filter math and convergence prediction. The engine's responsibility to persist `plugin_results` into `RoundState` is an engine concern, likely belonging in a spec for the engine pipeline (phases.py). If the engine does not do this, the failure mode is silent 2D fallback — not a crash, not data corruption.

**Counter-proposal**: Rate as P2 here, and create a tracking item for the engine wiring spec.

### On F-3 (plugin_results scoping)

The risk described (separate `execute_hooks` calls for scorer and predictor) is real but unlikely given the current architecture: both are POST_PHASE_5 plugins and will be in the same `execute_hooks` invocation. Adding a test for this is reasonable but P3, not P2.

## Additions

### Missing: Kalman filter numerical stability concern

The integration engineer does not mention the Joseph form TODO (NEW-6). From a filter-correctness standpoint, the standard covariance update `P = (I - KH) @ P_pred` can cause P to lose positive semi-definiteness after many iterations. With max 5 rounds, this is unlikely to manifest, but the integration engineer should note that extending round limits would require revisiting this.

## Overall Assessment

The plugin-integration-engineer's review is thorough on wiring concerns. The F-4 finding is valid but misscoped — it belongs in the engine spec, not here. The coverage gap analysis (F-6) is actionable and agreed.
