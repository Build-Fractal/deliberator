# Cross-Review: Spec-Compliance Reviews Plugin-Architect

**Reviewer**: spec-compliance
**Reviewed**: plugin-architect
**Round**: 1, Phase 2
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1. Plugin-architect's P1-Critical rating for equilibrium score history conflicts with SC-001 MET verdict

Plugin-architect (M5, P1-Critical) argues that the single-element equilibrium_scores list means "the Kalman filter is operating on fabricated data for all but the latest observation, which mathematically degrades the state estimate." If this is true, SC-001 ("ConvergencePredictor uses real eq_score when EquilibriumScorer is installed") cannot be MET -- the predictor uses a degraded version of the score, not the "real eq_score" the spec intends. Spec-compliance marks SC-001 as MET based on evidence that the predictor reads the score from plugin_results and passes it through. The contradiction is sharp: plugin-architect says the data path is critically broken at the mathematical level; spec-compliance says it meets the success criterion at the integration level. Both cannot be right unless the SC is ambiguous about what "uses" means.

### DC-2. Plugin-architect identifies O3 (Kalman dimension mismatch) as an active assumption error; spec-compliance identifies no off-base assumptions

Plugin-architect (O3) provides a detailed analysis showing that `_mat_add` on 2x2 + 3x3 matrices "won't crash... it will just silently use the smaller dimension and drop the third row/column," characterizing this as a "latent bug waiting to be triggered." Spec-compliance (Off-Base section) states "None identified in the core implementation." The Kalman dimension handling is part of the core implementation -- it is the mechanism through which the spec's central feature (3D prediction) is delivered. Plugin-architect's analysis of the matrix operation behavior is specific and verifiable. If it is correct, spec-compliance's clean off-base verdict missed a significant implementation assumption.

### DC-3. Plugin-architect proposes adding FR-011 to the spec; spec-compliance treats cross-hook lifetime as a documentation issue

Plugin-architect (P2-High, M2) recommends adding "FR-011: `plugin_results` is scoped to a single hook invocation" as a formal functional requirement in the spec. Spec-compliance (Missed Opportunity 1, recommendation 3) recommends "a note to the `execute_hooks` docstring or the spec clarifying that `plugin_results` is scoped to a single hook invocation." The difference is not cosmetic: a new FR requires a test, a compliance check, and becomes a binding constraint on future implementations. A docstring note is advisory. Spec-compliance's approach is consistent with the current spec's scope ("This spec adds declarations to the Plugin ABC"), while plugin-architect's approach extends the spec's scope. Both approaches solve the documentation gap, but they create different compliance obligations.

---

## Tensions

### T1. Whether the orchestration in execute_hooks is within spec scope

Spec-compliance (recommendation 10) identifies that "spec section 8 states 'This spec does NOT implement the orchestration layer (#6/ORC)' but the implementation does wire orchestration logic in `execute_hooks`." Plugin-architect (A4) praises this same orchestration as a clean architectural separation and lists it as an alignment strength. The tension is about review frame: spec-compliance evaluates against the spec's stated boundaries; plugin-architect evaluates against good architecture. Both are valid, but the implication differs -- spec-compliance implies the spec text should be updated; plugin-architect implies the implementation is correct as-is.

### T2. Error type for duplicate producers

Plugin-architect (P2) provides a code sample reusing `PluginDependencyCycleError` for duplicate producer detection. Spec-compliance (recommendation 1) suggests "PluginDependencyCycleError or a new DuplicateProducerError." From a spec-compliance perspective, error types matter because they define the API contract: a cycle and a duplicate producer are semantically different failures, and clients may catch one but not the other. Plugin-architect's reuse of the cycle error conflates two distinct failure modes.

### T3. Severity assessment of the self-nesting pattern

Plugin-architect (M4) calls the scorer's `score_data["equilibrium_score"] = score_data["score"]` pattern "boilerplate-prone and easy to forget" and recommends changing the orchestrator to store the entire `result.data` under a plugin-namespaced key. Spec-compliance (Off-Base 2, minor) calls the approach "correct" and "necessary because `execute_hooks` extracts only keys listed in `produces`." Plugin-architect views this as an architectural smell worth fixing; spec-compliance views it as a correct implementation of the specified contract. The tension is whether the contract itself should be changed.

### T4. Plugin-architect identifies nine missed opportunities; spec-compliance identifies five

Plugin-architect's missed opportunities span namespace collisions (M1), cross-hook lifetime (M2), missing validation (M3), self-nesting boilerplate (M4), history limitations (M5), untyped contracts (M6), duplicate producers (M7), sort performance (M8), and test gaps (M9). Spec-compliance covers cross-hook lifetime, history limitations, duplicate producers, `id(p)` usage, and test gaps. The additional items from plugin-architect (M1 namespace, M3 validation, M4 self-nesting, M6 typed contracts, M8 sort performance) represent architectural concerns beyond spec compliance scope. This is not a contradiction but a tension about review depth: spec-compliance evaluates what the spec requires; plugin-architect evaluates what good plugin architecture requires.

---

## Safe Agreements

### SA-1. Graceful degradation (FR-004) is correctly implemented

Plugin-architect (A2) praises the `None`-based fallback and calls it "the right default." Spec-compliance (FR-004 MET) verifies the same behavior with test evidence. Both confirm that missing consumed keys return `None` and do not crash consumers.

### SA-2. Duplicate producer keys should be detected

Plugin-architect (M1, M7, P2) and spec-compliance (Missed Opportunity 3, recommendation 1) independently identify that silent overwrite of duplicate producer keys is a problem. Both recommend raising an error. The consensus is clear despite minor differences in error type and priority.

### SA-3. The topological sort satisfies FR-005, FR-007, and FR-009

Plugin-architect (A3) validates Kahn's algorithm with declaration-order tiebreaking. Spec-compliance (FR-005, FR-007, FR-009, all MET) confirms with specific test evidence. Both agree that plugins without declarations see zero behavioral change.

### SA-4. Cross-hook plugin_results lifetime should be documented

Plugin-architect (M2) and spec-compliance (Missed Opportunity 1) both identify that the spec does not define whether plugin_results persists across hook points. Both agree the current behavior (per-hook scoping) is correct but should be explicitly stated. They differ on the mechanism (spec FR vs. docstring) but agree on the need.
