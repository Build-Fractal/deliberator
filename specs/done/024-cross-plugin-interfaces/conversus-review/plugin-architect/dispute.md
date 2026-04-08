# Plugin-Architect Dispute — Spec 024: Cross-Plugin Interfaces

**Reviewer**: plugin-architect
**Round**: 1, Phase 4 (Dispute)
**Date**: 2026-04-01

**Inputs**: All three revisions (plugin-architect, solver-engineer, spec-compliance).

---

## Resolved Disputes

### RD-1. SC-001 verdict: PARTIAL

All three reviewers now agree SC-001 should be PARTIAL rather than MET. Spec-compliance revised from MET to PARTIAL (revision R1), acknowledging the quality benefit is unrealized. The solver-engineer explicitly aligned with this position (revision M1). This dispute is fully resolved.

### RD-2. Q/R dimension mismatch severity

The solver-engineer revised from P1-Critical to P2-Important (revision R1), accepting my revised framing of "latent API defect." I had already revised from "active corruption bug" to "latent API defect." We now agree on P2-Important for defensive hardening. Spec-compliance's cross-review also noted this should be P2 from a compliance standpoint. Resolved.

### RD-3. Duplicate producer detection

All three reviewers agree this should be detected with a dedicated `DuplicateProducerError`. The solver-engineer adopted this (revision N1). Spec-compliance refined the error type (revision R4). I adopt `DuplicateProducerError` over my original reuse of `PluginDependencyCycleError`. Resolved.

### RD-4. Signal double-counting diagnostic

Both the solver-engineer (revision N2) and I (revision N1) agree that the 3D path's superiority should be empirically validated with an innovation magnitude diagnostic before shipping as default. Spec-compliance does not dispute this. Resolved at P2.

---

## Active Disputes

### AD-1. Cross-hook lifetime: formal FR vs. docstring (MAINTAINED)

**My position**: Add FR-011 to the spec defining cross-hook `plugin_results` scoping.

**Spec-compliance position** (revision M1): A docstring note is sufficient. Three arguments given: (1) scope expansion, (2) implicit test coverage, (3) flexibility for future designs.

**Why I maintain**: Spec-compliance's argument (3) about flexibility is backwards. If a future spec needs cross-hook data, it should explicitly override FR-011 rather than silently depending on an undocumented implementation detail. The FR makes the change intentional and traceable. Spec-compliance's argument (2) about implicit test coverage is weak -- implicit coverage is not the same as explicit coverage, and there is no test that specifically verifies plugin_results is reset between hooks. Spec-compliance's argument (1) about scope is valid but is a cost I accept: the orchestrator's behavior is part of the plugin contract, and contracts should be specified.

**Path to resolution**: If spec-compliance agrees that the current behavior should be tested (even without a formal FR), we can compromise: add a test in `test_cross_plugin.py` that verifies plugin_results scoping, and add a prominent docstring note. This achieves the testing and documentation goals without a formal FR.

### AD-2. Self-nesting pattern: architectural smell vs. correct contract

**My position** (M4): The orchestrator should not force producers to manually copy values into key-named fields in `result.data`. The extraction design should be changed.

**Spec-compliance position** (revision, not directly addressed): Calls the pattern "correct" and "necessary."

**Solver-engineer position**: No opinion.

**Why I maintain**: This is a P3 recommendation that does not block the spec. But every new producer will need to repeat this pattern, and forgetting the manual copy means the produced key silently disappears from `plugin_results`. The orchestrator already knows the plugin's `produces` list and the plugin's `result.data` -- it could extract the entire `data` dict or use a convention where the plugin returns `{key: value}` directly. I acknowledge this is a design preference, not a correctness issue, and I will not escalate further. This dispute can be deferred to a future spec.

---

## Consensus Summary

The following items are now fully agreed across all three reviewers:

1. **SC-001 is PARTIAL** -- wiring correct, numerical quality benefit unrealized.
2. **SC-002 is MET with caveat** -- zero-score case validates wrong behavior.
3. **Equilibrium score accumulation is P1-Critical** -- all three agree.
4. **Zero-score sentinel is wrong** -- all three agree, spec-compliance proposes SC-006.
5. **Q/R dimension mismatch is P2** -- latent API defect, not active bug.
6. **Duplicate producer detection needs DuplicateProducerError** -- all three agree.
7. **3D Kalman end-to-end test is needed** -- solver-engineer P2, adopted by spec-compliance.
8. **Signal double-counting needs empirical validation** -- plugin-architect and solver-engineer agree.
9. **Produced values should be immutable types** -- plugin-architect and solver-engineer agree.

Remaining disputes: AD-1 (FR vs. docstring for cross-hook lifetime) and AD-2 (self-nesting pattern).
