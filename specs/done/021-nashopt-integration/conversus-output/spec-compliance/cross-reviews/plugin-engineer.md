# spec-compliance Cross-Review of plugin-engineer

**Cross-reviewer**: spec-compliance
**Reviewing**: plugin-engineer Phase 1 review of spec 021
**Date**: 2026-04-01

---

## Agreements

### 1. scorer.py omission is the most impactful gap

plugin-engineer's P1-1 (include scorer.py) is the highest-priority recommendation across all three reviews. Without scorer.py, FR-007, FR-008, SC-001, SC-002, and SC-004 cannot be fully verified. All three reviewers converge on this point.

### 2. Coupled import concern is correctly scoped

plugin-engineer's analysis of the single try block is technically sound. The suggestion to separate imports and log which dependency is missing is a reasonable debugging improvement. I agree with the P2 classification -- it does not affect correctness.

### 3. SolverResult and Plugin dispatch pattern assessment is accurate

The frozen dataclass analysis and the dispatch pattern comparison with other plugins (HAS_AMPL, Kalman vs OLS) correctly identifies consistency across the plugin system. This pattern conformity is a compliance strength.

---

## Tensions

### 1. FR-008 verification approach

plugin-engineer verifies FR-008 (solver field in PluginResult.data) by referencing test code:

```python
assert result.data["solver"] == "heuristic"
```

From a strict compliance perspective, tests are necessary but not sufficient evidence. The test could be testing incorrect behavior that happens to match the assertion. Full verification requires seeing the production code that sets the field. Since the production code (scorer.py) is not in the artifacts, FR-008 is verified only at the test level, not the implementation level.

plugin-engineer correctly notes that solver.py does not set this field (separation of concerns), but does not flag that this means FR-008 is unverifiable from the provided artifacts alone. I mark FR-008 as MET based on the test evidence plus the architectural argument, but the epistemological gap should be acknowledged.

### 2. Backward compatibility assessment depth

plugin-engineer states "The existing heuristic path in scorer.py is completely untouched." This is asserted without evidence from the review artifacts. If scorer.py is not reviewed, how does plugin-engineer know it is untouched? The claim is likely correct (the spec explicitly requires no behavioral change), but it is an assumption, not a verified finding.

---

## Missed Opportunities

### 1. No analysis of the nashopt package __init__.py

plugin-engineer mentions __init__.py exports in passing but does not review the actual file. The `from conversus.plugins.nashopt import EquilibriumScorer` import path in the tests implies that __init__.py re-exports EquilibriumScorer. Does it also re-export HAS_NASHOPT? If callers must check `HAS_NASHOPT` before using the scorer, the flag should be accessible from the package root, not just from `conversus.plugins.nashopt.solver`.

### 2. No discussion of plugin configuration

The EquilibriumScorer plugin presumably accepts configuration (e.g., timeout_seconds). plugin-engineer does not discuss how the solver's configuration is passed through the plugin system. This is relevant to FR-007 (configurable timeout) -- the "configurable" part means the timeout must be settable via plugin_config, which is a plugin-layer concern.
