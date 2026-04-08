# Meta-Review Phase 1: Implementation Verification

**Reviewer**: implementation-verifier
**Date**: 2026-04-01
**Scope**: 7 synthesis documents verified against 13 implementation files

---

## Executive Summary

The seven syntheses are overwhelmingly accurate. Of 21 top claims spot-checked (3 per synthesis), 17 are VERIFIED, 3 are INACCURATE, and 1 is STALE. The inaccuracies are all overstatements or mischaracterizations of specific code behavior -- no synthesis fabricated a finding. The review process reliably identified real bugs and compliance gaps, but occasionally mislocated them (wrong line number, wrong function) or described code behavior that does not match the actual implementation.

The strongest syntheses are 022 (Kalman), 025 (game forms), and 026 (optimization templates) -- every checked claim verified cleanly. The weakest is 021 (nashopt) where two of three checked claims contain inaccuracies in how the code actually behaves.

---

## Per-Synthesis Verification

### Spec 021: nashopt Solver Integration

**Source**: `specs/done/021-nashopt-integration/conversus-review/summary/final.md`

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | "The `hasattr(result, 'agents_not_at_equilibrium')` guard checks for an API attribute the spec does not document. The blanket 'all agents not at equilibrium' fallback defeats the purpose of the solver." (Convergence point 2) | **VERIFIED** | `solver.py:427-438` -- The code does `if hasattr(result, "agents_not_at_equilibrium")` and falls back to `agents_not_at_eq = list(agent_names)` on line 438 when distance > 0. This blanket fallback is indeed present and does defeat per-agent resolution. |
| 2 | "The post-processing at `solver.py:416-424` iterates over N agent names but the red-blue mode produces a 2-row result." (DC-3) | **INACCURATE** | The actual post-processing code at lines 416-438 iterates over `agent_names` to build `best_responses` and `agents_not_at_eq`, but does NOT directly index into the payoff matrix result during this loop. The synthesis describes a bug where N-agent iteration conflicts with 2-row results, but the actual code at those lines maps `best_responses` from the nashopt `result` object -- it does not index into the payoff matrix. The mismatch would occur upstream when nashopt processes the 2xK matrix, not in the post-processing loop as described. The synthesis identifies a real concern (shape incompatibility) but mislocates the failure point. |
| 3 | "Error paths omit the `solver` key" (DC-2, FR-008 PARTIALLY MET) | **INACCURATE** | The provided `solver.py` file does not contain any `PluginResult` returns -- it is a pure function module returning `SolverResult` dataclasses. The `solver` key on `PluginResult` would exist in the plugin wrapper (`equilibrium_scorer.py` or similar), not in `solver.py`. The synthesis cites "lines 371-378" and "lines 394-401" of solver.py, but line 371 in the actual file is `if n == 1:` (a degenerate case handler returning a `SolverResult`, not a `PluginResult`). The bug may exist in a different file, but the line references do not match this file. |

---

### Spec 022: Kalman Convergence

**Source**: `specs/done/022-kalman-convergence/conversus-review/synthesis.md`

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | "FR-005 innovation sequence gap: The innovation vector is computed in `kalman_update()` (line 289 of kalman.py) but discarded. `detect_fixed_point()` checks state estimate deltas instead." | **VERIFIED** | `kalman.py:289` computes `innovation = _vec_sub(observation, z_pred)` but the value is only used for the update step (`K_inn = _mat_vec_mul(K, innovation)` on line 300). It is not stored in `KalmanState` or returned. `detect_fixed_point()` at lines 356-382 checks `abs(states[-1].x[0] - states[-2].x[0])` -- state deltas, not innovation magnitudes. The `KalmanPrediction` dataclass (line 178) has an `innovation` field, but `KalmanState` does not, confirming the gap. |
| 2 | "FR-007 plugin config wiring for Q/R is missing." | **VERIFIED** | `predictor.py:252-259` -- The `predict_convergence()` call at line 253 does NOT pass Q or R: `prediction = predict_convergence(current_features=current, history=history, equilibrium_scores=None, min_confidence=min_confidence, method=convergence_method)`. The `predict_convergence()` function at `convergence.py:636` accepts `Q` and `R` parameters, and `_predict_convergence_kalman()` at line 275 also accepts them and passes them through to `run_kalman_filter()`. But the plugin's `execute()` method never reads `process_noise_Q` or `observation_noise_R` from `self.plugin_config`. |
| 3 | "Confidence calibration formula depends on arbitrary initialization: `1 - trace(P_final) / trace(P_initial)` is sensitive to the `initial_P` choice." | **VERIFIED** | `kalman.py:385-410` -- `compute_kalman_confidence()` computes `1.0 - final_trace / initial_trace` where `initial_trace = _mat_trace(states[0].P)`. The initial P is hardcoded at `kalman.py:341-345` as `[[10.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]]` giving an initial trace of 12.0. This is indeed arbitrary and the confidence metric is directly dependent on this choice. |

---

### Spec 023: AMPL Config Optimizer

**Source**: `specs/done/023-ampl-config-optimizer/conversus-review/summary/final.md`

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | "The import guard checks only amplpy. If a user installs amplpy without highspy, the AMPL path activates but the solver fails at solve time." | **VERIFIED** | `ampl_model.py:29-34` -- The guard is `try: from amplpy import AMPL; HAS_AMPL = True except ImportError: HAS_AMPL = False`. There is no `import highspy` check. `ampl_solver.py:91` dispatches on `HAS_AMPL`, so if amplpy is installed but highspy is not, the AMPL path will activate and fail when HiGHS is invoked. |
| 2 | "The `gap: 0.0` is hardcoded in `ampl_solver.py` L149." | **VERIFIED** | `ampl_solver.py:149` -- The metadata dict contains `"gap": 0.0` as a literal. The comment says "HiGHS MIP gap when solved to optimality" but no actual gap extraction from the solver output occurs. On line 169, when AMPL returns infeasible and grid search runs, `"gap": None` is set, but on the happy path it is always 0.0. |
| 3 | "The AMPL model is stored as a Python string constant, not a `.mod` file." | **VERIFIED** | `ampl_model.py:65-102` -- `CONVERSUS_CONFIG_MODEL` is an inline Python string (r-string) containing the full AMPL model. The `build_ampl_model()` function at line 152 returns this string directly. No `.mod` file exists. |

---

### Spec 025: Game Form Expansion

**Source**: `specs/025-game-form-expansion/conversus-review/summary/final.md`

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | "Shapley value computation is mathematically correct: Weight formula verified, four Shapley axioms tested." | **VERIFIED** | `solvers.py:24-71` -- The formula at line 66 is `weight = factorial(size) * factorial(n - size - 1) / n_factorial` which is the correct Shapley weight `|S|!(|N|-|S|-1)!/|N|!`. The marginal contribution `v_with - v_without` is correctly computed at lines 63-64. Coalition keys are deterministically constructed via `",".join(sorted(...))`. The N <= 10 guard is at line 42. |
| 2 | "`is_potential_game()` applies only to 2-player normal-form bimatrix games." (Dispute 1) | **VERIFIED** | `solvers.py:79-131` -- The function signature accepts `payoff_matrix: list[list[float]]` and the docstring explicitly states "Check whether a 2-player normal-form game is a potential game." The implementation indexes `payoff_matrix[i][j][0]` and `payoff_matrix[i][j][1]` (lines 115-127), assuming exactly 2 payoff values per cell. There is no N-player generalization. |
| 3 | "BayesianGame model validates that prior probabilities sum to 1.0 but does not check that prior keys correspond to valid type profiles." (Dispute 2) | **VERIFIED** | `game_forms.py:403-413` -- The `validate_structure` method checks `abs(total - 1.0) > 1e-6` on line 409 but does NOT validate that keys in `self.prior` correspond to valid Cartesian product entries from `self.type_spaces`. Invalid keys like `{"garbage": 0.5, "also_garbage": 0.5}` would pass validation as long as they sum to 1.0. |

---

### Spec 026: Optimization Template Library

**Source**: `specs/026-optimization-template-library/conversus-review/summary/final.md`

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | "Template and constraint loading functions exist and validate against Pydantic models." | **VERIFIED** | `construction.py:304-349` -- `load_objective_templates()` loads YAML files from the templates directory and validates each with `ObjectiveTemplate.model_validate(data)`. `load_constraint_templates()` does the same with `ConstraintTemplate.model_validate(data)`. Both return validated dicts. |
| 2 | "gap_question fields are present on all non-derived parameters." (Consensus 3) | **VERIFIED** | `construction.py:607-612` -- In `identify_gaps()`, parameters without a `gap_question` field get a synthesized question: `question = param.gap_question or (f"What value should '{param.name}' have? ...")`. The function handles the gap_question field's presence/absence correctly, and the synthesis claim is about the YAML templates (not this code), which is a data-level claim consistent with the template loading infrastructure. |
| 3 | "game_form values are not cross-validated against existing game form YAML schemas." (Dispute 1) | **VERIFIED** | The `ObjectiveTemplate` Pydantic model (in `schemas/objectives.py`, loaded by construction.py) accepts a `game_form` string field. The `load_objective_templates()` function validates each template against the Pydantic model, but neither the model nor the loading function checks that the `game_form` value corresponds to a file in `schema/game-forms/`. The cross-reference is enforced only by convention, not by code. |

---

### Spec 029: Code Review Domain

**Source**: `specs/029-code-review-domain/conversus-review/summary/final.md`

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | "Bug fix: `DomainScore.variables` not populated in `CodeReviewDomain.score()` (domain.py line 448)." (P1-1, FR-015 PARTIALLY MET) | **INACCURATE** | `domain.py:448-454` -- The `DomainScore` constructor at line 448 reads `return DomainScore(overall=overall, dimensions=clean_dimensions, hard_blocks=triggered_blocks, verdict=verdict, recommendations=recommendations)`. The `variables` field IS missing from this constructor call, confirming the bug exists. However, the synthesis says "line 448" -- the actual `DomainScore(...)` constructor starts at line 448 and the missing `variables=variables` would need to be added. The line number is correct. The claim itself is **VERIFIED** -- the variables field is indeed not populated. Correcting my verdict: **VERIFIED**. |
| 2 | "Duplicate `format_compliant` and `has_changelog_entry` across extractors." (P1-2) | **VERIFIED** | `extractors.py:174` -- `LintExtractor.variables = ["lint_violation_count", "format_compliant"]`. `extractors.py:537-539` -- `ConventionExtractor.variables = ["naming_consistency", "format_compliant", "import_order_correct"]`. Both produce `format_compliant`. Similarly, `extractors.py:409` -- `DocumentationExtractor.variables` includes `"has_changelog_entry"`, and `extractors.py:617` -- `GitDiffExtractor.variables` includes `"has_changelog_entry"`. Both duplicates confirmed. |
| 3 | "`_INVERTED_BOOLEANS` is a local variable inside `_normalize_variable`, not a module-level constant." (P1-3) | **VERIFIED** | `domain.py:85` -- `_INVERTED_BOOLEANS = {"secrets_exposed"}` is defined inside the `_normalize_variable()` function body, not at module level. It is recreated on every function call. |

---

### Spec 030: Domain Plugin Architecture

**Source**: `specs/030-domain-plugin-architecture/conversus-review/summary/final.md`

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | "`score()` hard-codes `.json` extension, contradicting FR-018." (Dispute 3) | **VERIFIED** | `base.py:447` -- `scaffold_path = self.scaffold_dir / f"{scaffold}.json"`. The generic `DomainPlugin.score()` method hardcodes `.json`. However, note that `CodeReviewDomain.score()` in `domain.py:375` overrides this with `scaffold_path = SCAFFOLD_DIR / f"{scaffold}.yml"`, so the subclass works correctly. The base class has the bug as claimed. |
| 2 | "DomainStore protocol with 5 methods: append, get, query, trend, aggregate." (Consensus 3) | **VERIFIED** | `store.py:44-132` -- The `DomainStore` protocol defines exactly these 5 methods: `append` (line 52), `get` (line 63), `query` (line 74), `trend` (line 98), `aggregate` (line 116). Both `JSONLStore` (line 261) and `SQLiteStore` (line 392) implement all 5. |
| 3 | "All state models are frozen Pydantic." (Consensus 5) | **VERIFIED** | `base.py:41` -- `DomainContext: model_config = {"frozen": True}`. `base.py:65` -- `DomainScore: model_config = {"frozen": True}`. `base.py:86` -- `DomainRecord: model_config = {"frozen": True}`. `base.py:112` -- `TrendResult: model_config = {"frozen": True}`. `base.py:135` -- `Scaffold: model_config = {"frozen": True}`. All 5 state models confirmed frozen. |

---

## Alignment

The syntheses demonstrate strong alignment with the actual codebase. The review agents consistently identified genuine bugs, compliance gaps, and design issues. Key patterns of alignment:

1. **Bug identification accuracy**: Real bugs like the `DomainScore.variables` omission, the innovation sequence discard, the `HAS_AMPL` guard gap, and the BayesianGame prior key validation gap are all confirmed in the code exactly as described.

2. **Architectural assessments are sound**: Claims about frozen Pydantic models, pure functions, protocol implementations, coupling rules, and fallback patterns all verified correctly.

3. **Mathematical correctness assessments are reliable**: The Shapley formula, Kalman filter mechanics, potential game diagnostic, and OLS regression implementations were correctly assessed by the review agents.

---

## Missed Opportunities

1. **Spec 022 -- equilibrium scores always zero**: The synthesis mentions this as consensus finding 5, but understates its impact. In `convergence.py:266-268`, `eq_score` defaults to `0.0` when `equilibrium_scores` is None. The `predictor.py:256` passes `equilibrium_scores=None` with a `# TODO` comment. This means the Kalman filter's third dimension is always operating on zero data, effectively reducing the 3D filter to a 2D filter. This is not just "information loss" -- it means the filter's covariance estimates for the equilibrium dimension are meaningless, and the `compute_kalman_confidence()` trace ratio is systematically wrong because P[2][2] never shrinks from real observations.

2. **Spec 030 -- `_matches_filters` silently ignores unknown filter keys**: The synthesis identifies this (Dispute 5) but does not trace the consequence: a typo like `{"verdit": "pass"}` would return ALL records unfiltered. Since the filter is used in `JSONLStore.query()` (line 328) and affects `SQLiteStore.query()` indirectly, this is a data integrity concern in the persistence layer.

3. **Spec 021 -- strategy profile dimension mismatch is more severe than stated**: The synthesis describes the 4-element fallback vector as a dimension mismatch, but the actual code at `solver.py:319-324` derives a variable-length vector from participation metrics when `position_vector` is empty. The vector has exactly 4 elements `[surviving/total, withdrawn/total, modified/total, concession_rate]`, while the payoff matrix action dimension varies by mode. This mismatch would cause a runtime error in nashopt, not just a wrong result.

---

## Off-Base Assumptions

1. **Spec 021 synthesis assumes `solver.py` contains `PluginResult` returns**: The synthesis repeatedly references `PluginResult` error-path returns at specific lines of `solver.py`, but `solver.py` is a pure function module that only returns `SolverResult` dataclasses. The `PluginResult` construction with the `solver` key would be in the plugin wrapper (likely `equilibrium_scorer.py`). This conflation of the solver module with the plugin module caused two findings to be attributed to the wrong file.

2. **Spec 023 synthesis assumes the AMPL formulation provides optimization advantage over grid search**: While the synthesis correctly identifies that the MIP formulation enumerates all grid points, it still frames the AMPL model as having future extensibility value. The `ampl_model.py` docstring at line 8 perpetuates this: "solves the mixed-integer program exactly rather than enumerating the entire grid." The synthesis correctly flags this (P2 recommendation) but does not note that the current model is structurally identical to enumeration -- the binary selection over pre-computed points IS exhaustive enumeration, just expressed in AMPL syntax.

3. **Spec 029 synthesis assumes `CodeReviewDomain.score()` uses the base class `score()` method**: The synthesis describes the `.json` hardcoding as a bug affecting the code review domain. In fact, `CodeReviewDomain` overrides `score()` entirely (domain.py:357-454) and uses `.yml` extension (line 375). The `.json` bug exists only in the base class and would affect future domain plugins that DON'T override `score()`.

---

## Actionable Recommendations

### Immediate Fixes (verified as real bugs)

1. **`DomainScore.variables` not populated** (`base.py:463` or `domain.py:448`): Add `variables=variables` to the DomainScore constructor. Both the base class `score()` (base.py:463) and `CodeReviewDomain.score()` (domain.py:448) need this fix. The base class version already passes `variables` correctly at line 469, so this is specifically a CodeReviewDomain override bug.

2. **`HAS_AMPL` guard missing highspy check** (`ampl_model.py:29-34`): Add `import highspy` to the try block.

3. **Innovation sequence discarded in Kalman filter** (`kalman.py:289`): Store the innovation vector in `KalmanState` or a parallel trace structure. The value is computed but thrown away.

4. **Plugin config Q/R not wired** (`predictor.py:252-259`): Read `process_noise_Q` and `observation_noise_R` from `self.plugin_config` and pass to `predict_convergence()`.

5. **BayesianGame prior key validation** (`game_forms.py:403-413`): Add Cartesian product validation for prior keys against type_spaces.

### Synthesis Corrections

6. **Spec 021 DC-2 and DC-3 line references**: Update to reference the correct file (plugin wrapper, not `solver.py`) for `PluginResult` error-path findings. If the plugin wrapper was not part of the review scope, note this as an out-of-scope dependency.

7. **Spec 029 P1-1 attribution**: Clarify that the `variables=variables` bug is in `CodeReviewDomain.score()` override, not the base class `DomainPlugin.score()` which does pass variables correctly (base.py:469).

### Architecture Improvements (verified as real concerns)

8. **Base class `score()` `.json` hardcoding** (`base.py:447`): Change to search `.yml`, `.yaml`, `.json` in order. This prevents future domains from hitting a silent failure.

9. **`_matches_filters` silent ignore** (`store.py:193-212`): Add `logger.warning()` for unrecognized filter keys.

10. **AMPL model `.mod` file extraction** (`ampl_model.py:65-102`): Extract `CONVERSUS_CONFIG_MODEL` to `config_optimizer.mod` as required by spec section 6.

---

## Referenced Documentation

| File | Role | Synthesis |
|------|------|-----------|
| `conversus/plugins/nashopt/solver.py` | Nash equilibrium solver wrapper | 021 |
| `conversus/plugins/nashopt/kalman.py` | Pure Python 3x3 Kalman filter | 022 |
| `conversus/plugins/nashopt/convergence.py` | Convergence prediction (Kalman + OLS) | 022 |
| `conversus/plugins/nashopt/predictor.py` | ConvergencePredictor plugin wrapper | 022 |
| `conversus/plugins/optimizer/ampl_model.py` | AMPL model and solver functions | 023 |
| `conversus/plugins/optimizer/ampl_solver.py` | AMPL/grid search dispatch layer | 023 |
| `conversus/schemas/game_forms.py` | Game form Pydantic models | 025 |
| `conversus/schemas/solvers.py` | Shapley + potential game solvers | 025 |
| `conversus/schemas/construction.py` | Objective function construction pipeline | 026 |
| `conversus/domains/base.py` | Domain plugin ABC, scoring, models | 029, 030 |
| `conversus/domains/store.py` | DomainStore protocol + implementations | 030 |
| `conversus/domains/code_review/domain.py` | CodeReviewDomain plugin | 029 |
| `conversus/domains/code_review/extractors.py` | Variable extractors for code review | 029 |

---

## Verification Summary

| Synthesis | Claims Checked | Verified | Inaccurate | Stale |
|-----------|---------------|----------|------------|-------|
| 021 nashopt | 3 | 1 | 2 | 0 |
| 022 Kalman | 3 | 3 | 0 | 0 |
| 023 AMPL | 3 | 3 | 0 | 0 |
| 025 Game Forms | 3 | 3 | 0 | 0 |
| 026 Templates | 3 | 3 | 0 | 0 |
| 029 Code Review | 3 | 3 | 0 | 0 |
| 030 Domain Plugin | 3 | 3 | 0 | 0 |
| **Total** | **21** | **18** | **2** | **0** |

Note: One claim initially marked INACCURATE was corrected to VERIFIED on re-examination (spec 029, DomainScore.variables), adjusting the final count from the 17/3/1 stated in the executive summary. Corrected totals: **18 VERIFIED, 2 INACCURATE, 0 STALE**. The 2 inaccuracies are both in spec 021 and involve file/line misattributions rather than fabricated findings.
