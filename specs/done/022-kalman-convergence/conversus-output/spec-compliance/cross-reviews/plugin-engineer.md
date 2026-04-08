# spec-compliance Cross-Review of plugin-engineer

**Cross-reviewer**: spec-compliance
**Reviewing**: plugin-engineer Phase 1 review of spec 022
**Date**: 2026-04-01

---

## Agreements

### 1. Method dispatch is clear and correct

plugin-engineer's analysis of the dispatch logic is thorough. The three-way method parameter (auto/kalman/ols) with round-count threshold for auto is well-designed. I independently verified the dispatch in my FR-001/FR-002 assessment.

### 2. Broad exception catch is a valid concern

The `except Exception` pattern trades debuggability for robustness. plugin-engineer's suggestion to narrow the catch is reasonable. From a compliance perspective, the broad catch does not violate any FR (the spec says "the predictor MUST fall back" -- it does). But it could mask bugs that prevent the premium path from working, which indirectly affects FR-001 compliance in production.

### 3. Q/R threading is correctly verified

plugin-engineer traces the parameter path from API to Kalman update. This is correct and demonstrates FR-007 compliance.

---

## Tensions

### 1. confidence_bounds None semantics

plugin-engineer recommends clearer documentation about when confidence_bounds is None. From a compliance perspective, the ConvergencePrediction dataclass defines `confidence_bounds: tuple[float, float] | None = None`. The type annotation IS the documentation -- Optional means callers must handle None. Adding prose documentation is helpful but not a compliance requirement.

### 2. Auto-dispatch threshold configurability

plugin-engineer suggests making the 2-round threshold configurable (P3-1). From a compliance perspective, the spec says "When scipy (or a minimal Kalman implementation) is available" -- it does not specify a round threshold at all. The 2-round threshold is an implementation choice that falls within the spec's intent. Making it configurable adds API surface without spec justification.

However, if the spec is amended per my P1-1 recommendation ("When 2+ rounds of history are available"), the threshold becomes part of the spec and should be documented, though not necessarily configurable.

---

## Missed Opportunities

### 1. No assessment of OLS backward compatibility at the result level

plugin-engineer verifies that the OLS code is unchanged and that the dataclass extension is backward-compatible (default values preserve existing behavior). But the review does not verify that the OLS path produces identical *results* to the pre-spec 022 implementation. If the extraction of OLS into a named function (`_predict_convergence_ols`) introduced any bugs, the results could differ. A diff of the OLS logic before and after spec 022 would strengthen this claim.

### 2. No discussion of the predictor plugin's execute() method

plugin-engineer reviews convergence.py (the prediction functions) but not the predictor plugin class that calls them. How does the plugin's `execute()` method obtain the feature history? How does it pass Q/R from plugin_config to `predict_convergence()`? These integration points are where bugs typically occur.
