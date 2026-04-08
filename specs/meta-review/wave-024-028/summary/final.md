# Meta-Review Synthesis — Wave 024-028

**Specs**: 024 (Cross-Plugin Interfaces), 027 (Solver Validation Flow), 028 (Mode Expansion)
**Date**: 2026-04-01
**Auditors**: consistency-auditor, implementation-verifier, dependency-auditor, test-coverage-auditor
**Phases executed**: P1 (independent reviews), P2 (cross-review), P3 (consolidation), P4 (dispute resolution), P5 (synthesis)

---

## Executive Summary

The three specs target distinct subsystems (plugin data flow, validation config, mode/template expansion) with clean import boundaries and no contradictions. Implementation quality is high across all three — 8 of 9 spot-checked claims verified against code. The primary risks are:

1. **028 has zero test coverage** (empty test file) — the single most urgent remediation.
2. **024's P1 bugs are real and untested** — eq_score history loss and zero-score sentinel gate are confirmed in code but no test guards the correct behavior.
3. **027 is the healthiest** — Phase 1 is well-tested and correctly scoped; remaining gaps are additive.

No inter-spec contradictions found. Dependency chains hold. Import boundaries are clean.

---

## P2: Cross-Auditor Agreement Matrix

| Finding | Consistency | Implementation | Dependency | Test Coverage | Agreement |
|---------|------------|---------------|------------|---------------|-----------|
| 028 empty test file is critical | Noted as gap | Verified empty | N/A | CRITICAL BLIND SPOT | 4/4 UNANIMOUS |
| 024 eq_score history loss (P1-1) | Noted as tension with 027 | VERIFIED in predictor.py | N/A | NO TEST | 4/4 UNANIMOUS |
| 024 zero-score sentinel (P1-2) | No cross-spec impact | VERIFIED in convergence.py | N/A | TESTS WRONG BEHAVIOR | 4/4 UNANIMOUS |
| ration regex bug (028 P1-2) | Indirect impact on 024 scorer | VERIFIED in construction.py | N/A | NO TEST | 4/4 UNANIMOUS |
| VALID_MODES triple definition | N/A | N/A | DRY risk identified | NO SYNC TEST | 3/4 (dep + test + consistency) |
| DuplicateProducerError missing | N/A | N/A | NOT IMPLEMENTED | NO TEST | 2/4 (dep + impl) |
| 027 Phase 3 depends on 024 P1 | TENSION identified | N/A | Correctly blocked | N/A | 2/4 (consistency + dep) |
| 027 missing new-mode templates | GAP identified | N/A | No dependency | N/A | 2/4 (consistency + test) |

---

## P3: Consolidated Findings

### CRITICAL (must fix before next release)

**C-1. Populate `tests/test_mode_expansion.py`.**
All four auditors converge on this as the highest-priority item. The file is empty. No mode expansion functionality — classification, template completeness, keyword routing, VALID_MODES consistency, backward compatibility — is verified by any test. Blocks empirical confirmation of 028 SC-005.
- Source: 028 synthesis P1-1, all 4 auditors
- Files: `tests/test_mode_expansion.py`

**C-2. Fix eq_score history accumulation (024 P1-1).**
The predictor wraps the current round's score in a single-element list, discarding all prior rounds. The `_equilibrium_trend` function always returns 0.0 with a single data point. The 3D Kalman filter receives replicated scores that create a false constant-score prior. No test exists for the correct behavior.
- Source: 024 synthesis P1-1, implementation-verifier claim 1, test-coverage-auditor gap
- Files: `conversus/plugins/nashopt/predictor.py:255-261`, `conversus/plugins/base.py` (or RoundState)

**C-3. Fix zero-score sentinel gate (024 P1-2).**
`any(s != 0.0 for s in equilibrium_scores)` treats a legitimate score of 0.0 (no agents at equilibrium) as "scorer absent," falling back to 2D. The existing test `test_2d_with_all_zero_eq_scores` asserts the buggy behavior and must be inverted after the fix.
- Source: 024 synthesis P1-2, implementation-verifier claim 2, test-coverage-auditor
- Files: `conversus/plugins/nashopt/convergence.py:268-271`

### HIGH (should fix in this wave)

**H-1. Fix `ration` regex in construction.py (028 P1-2).**
The pattern `ration` matches "rational", "rationale", "irrational" as substrings. Fix: `\bration(?:ing|ed)?\b`. Indirect impact on 024 scorer via mode misclassification.
- Source: 028 synthesis P1-2, implementation-verifier claim 7, consistency-auditor 3.1
- File: `conversus/schemas/construction.py:107`

**H-2. Add VALID_MODES consistency test.**
Three files define VALID_MODES independently. No test catches drift. A single assertion comparing all three sets would prevent future mode-addition bugs.
- Source: dependency-auditor section 3, test-coverage-auditor gap 3
- Files: `engine/config.py`, `conversus/schemas/features.py`, `conversus/schemas/objectives.py`

**H-3. Add DuplicateProducerError (024 P2-3).**
Two plugins declaring the same `produces` key silently shadow each other. The sort function's `producers` dict overwrites without warning. Raise a dedicated `DuplicateProducerError`.
- Source: 024 synthesis P2-3, dependency-auditor section 6
- File: `conversus/plugins/base.py:333-336`

**H-4. Define `ConstraintAddition` typed model (027 Phase 1).**
`constraint_additions: list[str]` is not solver-consumable. Replace with a structured model carrying fields like `constraint_type`, `expression`, `parameters`.
- Source: 027 synthesis Phase 1 completions, implementation-verifier claim 5
- File: `conversus/schemas/validation.py:61-64`

### MEDIUM (track for next wave)

**M-1. Add 3D Kalman end-to-end test (024 P2-5).**
No test feeds multi-round 3D observations through the Kalman filter and verifies state dimension, confidence bounds, and convergence behavior.
- Source: 024 synthesis P2-5, test-coverage-auditor

**M-2. Add cross-hook plugin_results scoping test (024 P2-8).**
`plugin_results` is reset per hook invocation. This is load-bearing but undocumented and untested.
- Source: 024 synthesis P2-8, test-coverage-auditor

**M-3. Add scheduling/negotiation validation templates (027 Phase 1).**
`_AGENT_TEMPLATES` has 3 problem types (general, assignment, portfolio). 028 adds 4 new modes that lack corresponding validation agent templates.
- Source: 027 synthesis Phase 1 completions, consistency-auditor gap

**M-4. Consolidate VALID_MODES to single definition (DRY).**
Three independent definitions of the same set is a maintenance hazard. Consolidate to one canonical source.
- Source: dependency-auditor section 3

**M-5. Calibrate 3D observation noise R for eq_score dimension (024 P2-6).**
`R[2][2] = 0.005` trusts eq_score as much as concession_rate. Recommended: `R[2][2] = 0.05`.
- Source: 024 synthesis P2-6

---

## P4: Dispute Resolution

No disputes among auditors. All four converge on the same priority ordering:
1. C-1 (028 tests) is unanimously the top priority
2. C-2 and C-3 (024 P1 bugs) are unanimously critical
3. H-1 through H-4 are unanimously HIGH but non-blocking

The only area of partial disagreement is the severity of M-4 (VALID_MODES consolidation). The dependency-auditor rates it MEDIUM (maintenance hazard), while the consistency-auditor did not flag it. Resolved as MEDIUM — the current 3-way sync is correct today and the risk is future-facing.

---

## P5: Implementation Priority Matrix

### Wave 024-028 Action Plan

| Priority | Item | Spec | Effort | Dependency |
|----------|------|------|--------|------------|
| CRITICAL | C-1: Populate test_mode_expansion.py | 028 | Medium | None |
| CRITICAL | C-2: Accumulate eq_scores across rounds | 024 | Medium | None |
| CRITICAL | C-3: Fix zero-score sentinel gate | 024 | Small | None |
| HIGH | H-1: Fix ration regex | 028 | Trivial | None |
| HIGH | H-2: Add VALID_MODES consistency test | Cross | Trivial | None |
| HIGH | H-3: Add DuplicateProducerError | 024 | Small | None |
| HIGH | H-4: Define ConstraintAddition model | 027 | Medium | None |
| MEDIUM | M-1: 3D Kalman e2e test | 024 | Medium | C-2, C-3 |
| MEDIUM | M-2: Cross-hook scoping test | 024 | Small | None |
| MEDIUM | M-3: New mode validation templates | 027 | Small | None |
| MEDIUM | M-4: Consolidate VALID_MODES | Cross | Small | None |
| MEDIUM | M-5: Calibrate R[2][2] for eq_score | 024 | Trivial | C-2 |

### Recommended Implementation Order

1. **Batch 1** (no dependencies, parallel-safe):
   - C-3: Fix zero-score sentinel (convergence.py, 1 line)
   - H-1: Fix ration regex (construction.py, 1 line)
   - H-2: Add VALID_MODES consistency test (new test)
   - H-3: Add DuplicateProducerError (base.py)

2. **Batch 2** (depends on nothing, but more effort):
   - C-2: Accumulate eq_scores across rounds (predictor.py + base.py/RoundState)
   - C-1: Populate test_mode_expansion.py (new tests)
   - H-4: Define ConstraintAddition model (validation.py)

3. **Batch 3** (depends on Batch 1/2):
   - M-1: 3D Kalman e2e test (depends on C-2, C-3)
   - M-2: Cross-hook scoping test
   - M-5: Calibrate R[2][2] (depends on C-2)

4. **Batch 4** (maintenance, any time):
   - M-3: New mode validation templates
   - M-4: Consolidate VALID_MODES

---

## Compliance Summary

| Spec | Synthesis Verdict | Meta-Review Verdict | Change? |
|------|-------------------|---------------------|---------|
| 024 | PARTIAL PASS | CONFIRMED — P1 bugs verified in code, tests confirm wiring but not numerical correctness | No change |
| 027 | REVISE (Phase 1 complete) | CONFIRMED — Phase 1 is solid; remaining work is correctly identified as additive | No change |
| 028 | MET with defects | CONFIRMED with emphasis — empty test file is more critical than synthesis suggests; "MET BY DESIGN, pending empirical confirmation" for SC-005 is effectively UNVERIFIED until tests exist | Recommend downgrade SC-005 to UNVERIFIED |

---

## Cross-Spec Health Dashboard

```
Spec 024 (Cross-Plugin Interfaces)
  Implementation: ████████░░  80%  (wiring correct, 2 P1 bugs)
  Tests:          ██████░░░░  60%  (good structure, numerical gaps)
  Synthesis:      ██████████  100% (all claims verified)

Spec 027 (Solver Validation Flow)
  Implementation: ██████░░░░  60%  (Phase 1 only, correctly scoped)
  Tests:          █████████░  90%  (thorough for Phase 1)
  Synthesis:      ██████████  100% (all claims verified)

Spec 028 (Mode Expansion)
  Implementation: █████████░  90%  (1 regex bug, otherwise complete)
  Tests:          ░░░░░░░░░░   0%  (empty file)
  Synthesis:      █████████░  90%  (1 claim partially verified)
```

---

## Referenced Files

| File | Relevance |
|------|-----------|
| `conversus/plugins/base.py` | 024: Plugin ABC, topo sort, execute_hooks, DuplicateProducerError gap |
| `conversus/plugins/nashopt/predictor.py` | 024: eq_score history loss (lines 255-261) |
| `conversus/plugins/nashopt/convergence.py` | 024: zero-score sentinel (lines 268-271), R calibration (lines 339-343) |
| `conversus/plugins/nashopt/scorer.py` | 024: produces equilibrium_score |
| `conversus/plugins/nashopt/kalman.py` | 024: Kalman filter, default Q/R sizing |
| `conversus/schemas/validation.py` | 027: config generation, ValidationVerdict, ConstraintAddition gap |
| `conversus/schemas/construction.py` | 028: DecisionType, ration regex bug (line 107) |
| `engine/config.py` | 028: VALID_MODES tuple |
| `conversus/schemas/features.py` | Cross: VALID_MODES frozenset |
| `conversus/schemas/objectives.py` | Cross: VALID_MODES frozenset |
| `tests/test_cross_plugin.py` | 024: structural tests, numerical gaps |
| `tests/test_validation.py` | 027: thorough Phase 1 tests |
| `tests/test_mode_expansion.py` | 028: EMPTY — critical gap |
| `templates/` | 028: 8 modes x 7 templates = 56 files (complete) |
| `schema/modes/` | 028: 8 mode YAML files (complete) |
