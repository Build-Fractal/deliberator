# Cross-Spec Consistency Audit — Phase 1 Meta-Review

**Auditor**: consistency-auditor
**Date**: 2026-04-01
**Specs reviewed**: 021, 022, 023, 025, 026, 029, 030
**Implementation files verified**: solver.py, kalman.py, ampl_model.py, game_forms.py, base.py, domain.py

---

## Executive Summary

Seven synthesis outputs were audited for internal contradictions, priority consistency, shared interface agreement, cross-cutting findings, and dependency chain coherence. The overall quality is high: no outright P1-vs-P1 contradictions exist between specs. However, the audit surfaced **4 cross-spec inconsistencies**, **3 missed opportunities** where a finding in one spec should have been flagged in another, and **2 off-base assumptions** that do not survive cross-spec scrutiny. The most significant finding is the scaffold file extension mismatch between specs 029 and 030, which is a confirmed code-level contradiction visible in the implementation files.

---

## Alignment

### 1. Priority scales are consistent across specs

All seven syntheses use the same priority taxonomy (P1/P2/P3 or HIGH/MEDIUM/LOW with equivalent semantics). The distinction between "compliance P1" (must-fix-before-merge) and "quality P1" (ship-in-same-PR) introduced in spec 022 is internally consistent and does not conflict with the flat P1 used in specs 021, 023, and 029. Spec 025 uses HIGH/MEDIUM/LOW which maps cleanly to P1/P2/P3.

### 2. Optional dependency pattern is consistent across solver specs (021, 022, 023)

All three solver specs follow the same pattern: try-import at module top, set a `HAS_*` flag, fallback to zero-dependency path. Verified in implementation:
- `solver.py`: `HAS_NASHOPT` with numpy/nashopt try-import (lines 27-39)
- `kalman.py`: Pure Python, no optional imports (exceeds constraint)
- `ampl_model.py`: `HAS_AMPL` with amplpy try-import (lines 29-34)

This pattern is not formalized as a shared convention anywhere. It should be.

### 3. Frozen Pydantic model convention is consistent between specs 025, 029, 030

Spec 030 establishes frozen Pydantic models as a design rule. Spec 025's game form models use `BaseModel` without `frozen=True` in `model_config`, but this is acceptable because game form schemas are data definitions, not state carriers. Spec 030's frozen rule applies to state models (`DomainScore`, `DomainRecord`, etc.), not schema validation models. No contradiction.

### 4. Pure-function service layer is followed throughout

Specs 021 (solver), 022 (kalman), and 023 (ampl) all use pure functions for computation. Spec 030's domain base uses a class hierarchy (necessary for the ABC pattern) but keeps scoring as pure functions (`_compute_weighted_score`, `_check_hard_blocks`, etc.). This is consistent with the codebase's "functional service layer" principle.

---

## Cross-Spec Inconsistencies Found

### CSI-1: Scaffold file extension — `.json` (base.py) vs. `.yml` (domain.py) [P1]

**Specs**: 030 vs. 029
**Nature**: Direct code-level contradiction

Spec 030's synthesis (Dispute 3) correctly identifies that `DomainPlugin.score()` in `base.py` hard-codes `.json` at line 447:
```python
scaffold_path = self.scaffold_dir / f"{scaffold}.json"
```

Spec 029's `CodeReviewDomain.score()` overrides this and uses `.yml` at line 375:
```python
scaffold_path = SCAFFOLD_DIR / f"{scaffold}.yml"
```

Both specs independently flag this. Spec 030 flags it as a Medium priority action item (FR-018). Spec 029 does **not** flag it because the `CodeReviewDomain` override works around it. But the contradiction means any future domain that inherits `DomainPlugin.score()` without overriding will fail on YAML scaffolds. This is a P1 because it blocks the stated goal of spec 030: "any domain can be formulated... by providing extractors and scaffolds while inheriting generic scoring."

**Spec 030 correctly identifies the fix** (search for `.yml`/`.yaml`/`.json` in order). **Spec 029 misses it** because the override masks the bug. Neither spec flags the redundancy of spec 029 re-implementing the scoring pipeline instead of using the inherited one.

### CSI-2: `DomainScore.variables` — populated (base.py) vs. missing (domain.py) [P1]

**Specs**: 030 vs. 029
**Nature**: Implementation divergence at the integration seam

Spec 030's `DomainPlugin.score()` in `base.py` at line 469 passes `variables=variables` to the `DomainScore` constructor. Spec 029's `CodeReviewDomain.score()` in `domain.py` at line 448 does **not** pass `variables`:
```python
return DomainScore(
    overall=overall,
    dimensions=clean_dimensions,
    hard_blocks=triggered_blocks,
    verdict=verdict,
    recommendations=recommendations,
)
```

Spec 029's synthesis correctly identifies this as a P1 bug (item #1 in Priority Action Items, "Bug fix: Add `variables=variables` to DomainScore constructor"). Spec 030 does **not** flag it because the base class implementation is correct -- the bug is in the subclass override. However, spec 030 should have noted that the `CodeReviewDomain` subclass duplicates the entire scoring pipeline instead of calling `super().score()`, which is why the bug exists. The root cause is architectural: spec 029 should delegate to the inherited scoring infrastructure, not reimplement it.

### CSI-3: Heuristic-solver score discontinuity — flagged in 021, relevant to 022 [P2]

**Specs**: 021 vs. 022
**Nature**: Cross-spec concern flagged in only one spec

Spec 021 (SC-SYS-2) identifies that the heuristic score (`agents_at_eq / total_agents`, discrete) and the solver score (`1.0 - distance`, continuous) are incommensurable. When the system switches between them on timeout, scores jump discontinuously.

Spec 022 introduces Kalman-filtered convergence prediction that tracks `equilibrium_score` as the third state dimension. If the equilibrium score jumps discontinuously between the heuristic and solver paths (spec 021's finding), the Kalman filter's state estimate will be corrupted by the discontinuity, producing unreliable confidence intervals and potentially false fixed-point detections.

Spec 022's synthesis notes that "equilibrium scores are not wired through" (consensus finding #5, `eq_score` is always 0.0). This masks the problem for now, but when remediation 6 ("wire equilibrium scores") is implemented, the spec 021 discontinuity will become a spec 022 correctness issue. Neither synthesis connects these dots.

### CSI-4: `solver` key provenance pattern — spec 021 establishes, spec 023 ignores [P2]

**Specs**: 021 vs. 023
**Nature**: Pattern established in one spec, not adopted in another

Spec 021 establishes a `solver` provenance key on `PluginResult` so consumers know which computation path produced the result (`"nashopt"` vs. `"heuristic"`). The synthesis dedicates significant deliberation to the error-path sentinel value.

Spec 023's `solve_with_ampl()` returns `solver_status: "optimal"` on the happy path but returns `None` for three distinct failure conditions (no amplpy, infeasible, no selection). The synthesis correctly flags this (P2: "Structured return type for `solve_with_ampl`"). However, neither spec cross-references the other's provenance pattern. Spec 023's `SolveOutcome` recommendation would benefit from aligning with spec 021's `solver` key convention, so consumers can use a uniform provenance interface across all solver-backed plugins.

---

## Missed Opportunities

### MO-1: Spec 025's game form expansion has no connection to spec 021's payoff matrix builders

Spec 025 adds 5 new game forms (coalitional, congestion, bayesian, repeated, mechanism design). Spec 021's `build_payoff_matrix()` supports 4 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue). The new game forms in spec 025 could define additional payoff matrix builders for new modes, but neither spec references the other. The mode-mapping system (spec 025, `mode-mapping.yml`) adds 5 new mode-to-form mappings, but `solver.py` will raise `ValueError` for any mode not in its hard-coded set of 4. This is not a contradiction (the new forms are Tier 2, deferred to solver integration), but it is a missed opportunity to plan the integration surface.

### MO-2: Spec 026's template library cross-validates against spec 025's game forms but not spec 021's modes

Spec 026 flags (Dispute 1) that template `game_form` values should be validated against `schema/game-forms/*.yml`. Spec 026 also flags `mode_compatibility` validation against valid modes. But the "valid modes" list is split between `mode-mapping.yml` (spec 025, 9 modes) and `solver.py` (spec 021, 4 modes). A template declaring `mode_compatibility: ["coalition-attribution"]` will pass mode-mapping validation but will fail at runtime because `solver.py` does not handle that mode. Neither spec flags this gap.

### MO-3: Spec 030's plugin discovery could use spec 023's optional import pattern

Spec 030 (Dispute 2) identifies that `importlib`-based plugin discovery is not implemented. The pattern for graceful degradation when a plugin's dependencies are missing is already established in specs 021 and 023 (`HAS_NASHOPT`, `HAS_AMPL`). Spec 030's synthesis does not reference these as precedents for the "missing packages warn and skip" behavior specified in FR-003.

---

## Off-Base Assumptions

### OBA-1: Spec 023 claims the MIP formulation "solves exactly rather than enumerating" — the implementation enumerates

Spec 023's synthesis correctly identifies this (P2: "Update enumeration documentation"), and all three agents converge on it. The AMPL model encodes all grid points as binary selection variables, which is mathematically equivalent to enumeration. The docstring at `ampl_model.py` line 8 still reads "solves the mixed-integer program exactly rather than enumerating the entire grid." This is acknowledged within spec 023's review as inaccurate documentation, so it is not a cross-spec issue, but it could mislead readers of other specs (particularly spec 026, which defers SC-005 solvability testing to spec 023 under the assumption that AMPL provides computational advantage).

### OBA-2: Spec 022's confidence calibration formula is initialization-dependent, undermining spec 021's score semantics

Spec 022's `compute_kalman_confidence()` uses `1 - trace(P_final) / trace(P_initial)`. The initial P is hard-coded in `run_kalman_filter()` at line 341 as `diag(10, 1, 1)`. This means the confidence metric is an artifact of the initialization choice, not the observation data. Spec 022's synthesis acknowledges this (consensus finding #4, remediation 4). However, the assumption that this metric can be meaningfully compared across different filter runs or used to classify convergence predictions is off-base: two runs with different `initial_P` values will produce different confidence scores from identical observation data. This undermines any cross-spec consumer that treats Kalman confidence as a calibrated probability.

---

## Actionable Recommendations

### R-1 [P1]: Fix the scaffold file extension in `DomainPlugin.score()` (base.py line 447)

Change the base class to search for `.yml`, `.yaml`, then `.json` in order. This is already recommended in spec 030's action items. Elevating to P1 because it blocks the core architectural promise of spec 030.

**Affects**: specs 029, 030
**Files**: `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/base.py` line 447

### R-2 [P1]: Fix `DomainScore.variables` omission in `CodeReviewDomain.score()` (domain.py line 448)

Add `variables=variables` to the `DomainScore` constructor call. Already identified as P1 in spec 029. Confirmed via code inspection.

**Affects**: spec 029
**Files**: `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/domain.py` line 448

### R-3 [P1]: Refactor `CodeReviewDomain.score()` to delegate to `super().score()` with dimension normalization

The current `CodeReviewDomain.score()` reimplements the entire scoring pipeline (computing weighted scores, evaluating hard blocks, determining verdicts, generating recommendations) instead of using the generic pipeline inherited from `DomainPlugin`. This is the root cause of CSI-1 and CSI-2: the override diverges from the base class. The domain-specific logic (dimension scoring via `DIMENSION_VARIABLES`, custom `_normalize_variable`, custom `_evaluate_hard_block`) should be implemented as a pre-processing step that produces a normalized variable dict, which is then passed to `super().score()`.

**Affects**: specs 029, 030
**Files**: `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/domain.py`

### R-4 [P1]: Add `highspy` to the AMPL import guard (ampl_model.py lines 29-34)

Confirmed via code inspection: only `amplpy` is checked. Spec 023's synthesis unanimously recommends adding `highspy`. The current code will activate the AMPL path without a usable solver.

**Affects**: spec 023
**Files**: `/Users/business-daddy/code/payer-index-mono/conversus/conversus/plugins/optimizer/ampl_model.py` lines 29-34

### R-5 [P2]: Establish a shared optional-import convention document

Specs 021, 022, and 023 each independently implement the same try-import / `HAS_*` / fallback pattern. Spec 030 will need it for plugin discovery (FR-002, FR-003). Codify this as a shared convention (e.g., a `conversus.utils.optional_imports` helper or a documented pattern) so future specs do not re-derive it.

**Affects**: specs 021, 022, 023, 030

### R-6 [P2]: Document the equilibrium score discontinuity as a precondition for spec 022 remediation 6

Before wiring equilibrium scores into the Kalman filter's third state dimension (spec 022, remediation 6), the heuristic-vs-solver score discontinuity identified in spec 021 (SC-SYS-2) must be resolved. Options: (a) normalize both scores to a common scale before passing to the Kalman filter, (b) only feed solver-path scores to the Kalman filter and skip heuristic-path observations, (c) add a score-source indicator to the observation vector so the filter can weight accordingly.

**Affects**: specs 021, 022

### R-7 [P2]: Align mode support between `solver.py` and `mode-mapping.yml`

`solver.py:build_payoff_matrix()` supports 4 modes. `mode-mapping.yml` defines 9 modes. Templates in spec 026 may declare `mode_compatibility` for modes that have no solver support. Add a runtime validation or a clear Tier-1/Tier-2 distinction in the mode mapping so consumers know which modes have full solver support.

**Affects**: specs 021, 025, 026

### R-8 [P2]: Standardize solver provenance keys across plugins

Spec 021 establishes `solver: "nashopt" | "heuristic"` as a provenance field. Spec 023 uses `solver_status: "optimal"` with `None` returns for failures. Define a cross-plugin provenance contract: every solver-backed plugin should include a `solver` key indicating which computation path was used and a `solver_status` key indicating the outcome. This enables uniform downstream processing.

**Affects**: specs 021, 023

### R-9 [P2]: Add BayesianGame prior key validation (spec 025 Dispute 2)

Confirmed via code inspection: `BayesianGame.validate_structure()` in `game_forms.py` (lines 403-412) validates that prior probabilities sum to 1.0 but does not validate that prior keys are valid type profile tuples from the Cartesian product of `type_spaces`. This is unanimously agreed upon in spec 025's synthesis.

**Affects**: spec 025
**Files**: `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/game_forms.py` lines 403-412

### R-10 [P3]: Cross-spec dependency map

Several specs have explicit or implicit dependencies that are tracked within individual syntheses but not in a unified view:
- Spec 026 SC-005 depends on spec 023 (AMPL solvability)
- Spec 026 FR-004 depends on spec 014 (classifier routing)
- Spec 029 FR-014/FR-016 depends on spec 011 (gate system)
- Spec 029 SC-004 depends on spec 030 (domain plugin base layer)
- Spec 022 remediation 6 depends on spec 021 (equilibrium score source)
- Spec 030 FR-015 depends on the conversus engine (gate runner injection)

A single dependency matrix would make sequencing and impact analysis tractable.

---

## Referenced Documentation

| Spec | Synthesis File | Key Implementation |
|------|---------------|-------------------|
| 021 | `specs/done/021-nashopt-integration/conversus-review/summary/final.md` | `conversus/plugins/nashopt/solver.py` |
| 022 | `specs/done/022-kalman-convergence/conversus-review/synthesis.md` | `conversus/plugins/nashopt/kalman.py` |
| 023 | `specs/done/023-ampl-config-optimizer/conversus-review/summary/final.md` | `conversus/plugins/optimizer/ampl_model.py` |
| 025 | `specs/025-game-form-expansion/conversus-review/summary/final.md` | `conversus/schemas/game_forms.py` |
| 026 | `specs/026-optimization-template-library/conversus-review/summary/final.md` | (YAML schemas, no Python) |
| 029 | `specs/029-code-review-domain/conversus-review/summary/final.md` | `conversus/domains/code_review/domain.py` |
| 030 | `specs/030-domain-plugin-architecture/conversus-review/summary/final.md` | `conversus/domains/base.py` |
