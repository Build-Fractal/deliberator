# Meta-Review Phase 1: Consistency Auditor — Wave 024-028

**Scope**: Specs 024, 027, 028
**Date**: 2026-04-01
**Auditor role**: Do findings in one spec contradict or affect another? Are P1 priorities consistent across specs?

---

## 1. Cross-Spec Consistency Matrix

| Finding | Spec A | Spec B | Consistency |
|---------|--------|--------|-------------|
| VALID_MODES set | 028 (adds 4 modes) | 027 (validation config hardcodes `cooperative`) | CONSISTENT — 027 uses cooperative for validation deliberations regardless of mode count; 028 adds modes to the engine's VALID_MODES tuple but does not change how validation mode is selected |
| VALID_MODES synchronization | 028 (8 modes) | 024 (scorer uses features.VALID_MODES) | CONSISTENT — features.py, objectives.py, engine/config.py all define the same 8-mode set; scorer checks `state.mode not in VALID_MODES` which reflects the expanded set |
| plugin_results lifetime | 024 (reset per hook invocation) | 027 (validation uses same engine) | CONSISTENT — validation deliberations would inherit the same hook lifecycle; no contradiction since 027 Phase 1 does not wire plugin hooks |
| equilibrium_score accumulation | 024 (P1: accumulate eq_scores across rounds) | 027 (SC-003: integrate equilibrium scorer) | TENSION — 024's P1 fix (accumulate history) must land before 027's Phase 3 (SC-003) can work correctly. If 027 ships Phase 3 without 024's P1, the scorer-in-validation will suffer the same single-element history bug |
| DecisionType classification | 028 (adds 4 new DecisionTypes) | 027 (problem_type param) | GAP — 027 defines `problem_type` as {"general", "assignment", "portfolio"} in `_AGENT_TEMPLATES`. 028 adds negotiation, resource-allocation, fair-division, mechanism-design as engine modes. 027 does not map these new modes to validation agent templates. This is a future gap, not a contradiction, since 027 Phase 1 scope is limited |
| Template completeness | 028 (7 templates per mode) | 024/027 (unrelated) | CONSISTENT — 028's templates are strictly additive and do not touch plugin or validation code |

---

## 2. P1 Priority Consistency

### Spec 024 P1 Priorities
1. Accumulate equilibrium scores across rounds
2. Fix zero-score sentinel gate

### Spec 027 P1 Priorities (Phase 1 Completions)
1. Define `ConstraintAddition` model (typed fields)
2. Define `SolverSolution` input schema model

### Spec 028 P1 Priorities
1. Populate `tests/test_mode_expansion.py`
2. Fix `ration` regex bug in construction.py
3. Update spec 028 Section 2.1 game forms text

**Assessment**: P1 priorities are non-overlapping and internally consistent. No spec's P1 action negates or complicates another spec's P1 action. The priorities target different subsystems:
- 024 targets the plugin data-flow layer (convergence.py, predictor.py)
- 027 targets the schema/validation layer (validation.py)
- 028 targets the classification/template layer (construction.py, templates/)

---

## 3. Contradictions Found

### 3.1 `ration` regex (028) vs. keyword classification accuracy (024)

028 identifies a bug where `ration` matches "rational" as a substring. This is in `construction.py` which is used for objective function construction (spec 014), not directly in the plugin layer (024). However, if a problem description containing "rational" is misclassified as RESOURCE_ALLOCATION instead of, say, NEGOTIATION, then the wrong mode is selected, which in turn affects which equilibrium scoring payoff function runs (024's scorer). The connection is indirect but real.

**Impact**: LOW — the classifier uses match count as a tiebreaker, and "rational" appearing once is unlikely to override a strong signal from the correct decision type's keywords. But it could cause edge-case misclassification.

**Recommendation**: Fix 028's P1 item 2 (regex fix) before 024's scorer is used in production with auto-classified modes.

### 3.2 Validation mode vs. engine mode scope

027's `generate_validation_config()` hardcodes `mode: "cooperative"`. This is correct — validation deliberations use cooperative mode. However, 027's synthesis notes that SC-003 (equilibrium scorer integration) is NOT MET and is blocked on spec 021. Meanwhile, 024's synthesis notes that the scorer works with all VALID_MODES. There is no contradiction, but the dependency is important: 027 Phase 3 depends on both 024's P1 fixes AND spec 021.

---

## 4. Cross-Spec Dependency Ordering

Based on the findings above, the correct implementation order is:

1. **028 P1** (regex fix, tests) — no dependencies, purely additive
2. **024 P1** (eq_score accumulation, zero-score sentinel) — no dependencies on 027/028
3. **027 Phase 1 completions** (ConstraintAddition, SolverSolution models) — no dependencies on 024/028
4. **027 Phase 2** (CLI + execution) — depends on 024 P1 being done if scorer integration is desired
5. **027 Phase 3** (equilibrium scorer integration) — hard dependency on 024 P1 + spec 021

---

## 5. Verdict

**No contradictions found.** Specs are consistent in their domains. One TENSION exists (024 P1 must precede 027 Phase 3 scorer integration) and one GAP exists (027 does not define validation agent templates for 028's new modes). Both are future-facing and do not affect current P1 priorities.
