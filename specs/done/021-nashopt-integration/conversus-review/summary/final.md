# Neutral Synthesis — Spec 021: nashopt Solver Integration

**Synthesizer**: neutral (Phase 5)
**Date**: 2026-04-01
**Deliberation mode**: cooperative
**Agents**: solver-engineer, plugin-engineer, spec-compliance

---

## Process Summary

Three agents reviewed spec 021 (nashopt solver integration) across four phases of cooperative deliberation. The spec replaces the heuristic equilibrium scorer in `conversus-nashopt` with actual Nash equilibrium computation via the `nashopt` library (JAX-based), retaining the heuristic as a zero-dependency fallback.

**Phase 1 (Independent Review):** Each agent reviewed the spec and implementation from their domain perspective. solver-engineer focused on numerical correctness (matrix shapes, strategy dimensions, normalization). plugin-engineer focused on plugin architecture (flag patterns, dispatch, backward compatibility, import safety). spec-compliance focused on FR/SC compliance verification against spec language.

**Phase 2 (Cross-Review):** Agents identified 9 dangerous contradictions, 15 tensions, and 12 safe agreements across six cross-review documents. The most significant contradictions involved the WTA matrix shape (spec-compliant N x 1 vs. nashopt's expected N x N x actions), the ThreadPoolExecutor timeout severity, and the FR-008 compliance verdict.

**Phase 3 (Revision):** All three agents revised their positions materially. solver-engineer withdrew 3 recommendations (WTA N x N reformulation, payoff normalization, score reconciliation) and downgraded the ThreadPoolExecutor fix from P1 to P2. plugin-engineer downgraded the dead variable from P1 to P2 and adopted SC-001/SC-002 testing from spec-compliance. spec-compliance upgraded the real-timeout test from P2 to P1 and adopted the missing `solver` key finding from plugin-engineer.

**Phase 4 (Disputes):** Three disputes remain unresolved. Five convergence points achieved unanimous agreement. All agents published non-negotiables and flexibility areas.

---

## Recommendation Scorecard

| ID | Recommendation | solver-engineer | plugin-engineer | spec-compliance | Synthesis |
|----|---------------|-----------------|-----------------|-----------------|-----------|
| SC-TESTS | SC-001/SC-002 threshold tests | P1 (N-2) | P1 (N1) | P1 (P1-1, P1-2) | **P1** |
| FR005-FIX | Per-agent equilibrium from best_responses | P1 (P1-5) | P1 (accepted) | P1 (P1-3) | **P1** |
| SOLVER-KEY | `solver` key on error-path returns | P1 (agrees) | P1 (P1-1) | P1 (NEW-1) | **P1** |
| POSTPROC | Post-processing mapping for non-NxN modes | P1 (P1-2 narrowed) | P2 (N3) | P2 (accepted) | **P1** |
| STRAT-DIM | Strategy profile dimension match | P1 (P1-3) | P2 (implied) | Not raised | **P1** |
| TIMEOUT-TEST | Real-timeout integration test | P1 (implied) | P1 (P1-2 test) | P1 (upgraded) | **P1** |
| SPEC-AMEND | Spec matrix shape inconsistency | P1 (N-1) | Not blocking | Tracked, not blocking | **P1 (spec)** |
| EXEC-SHUTDOWN | ThreadPoolExecutor shutdown fix | P2 (revised) | P2 (N2) | P2 (upgraded) | **P2** |
| PAYOFF-DATA | Per-agent payoff in solver path | P2 (P2-7) | P2 (P2-1) | P2 (P2-5) | **P2** |
| SHAPE-VALID | Pre-call matrix shape validation | P2 (accepts) | P2 (upgraded) | P2 (NEW-3) | **P2** |
| RB-NORM | Red-blue dead variable + normalization | P3 (accepts P2) | P2 (merged) | P2 (NEW-2) | **P2** |
| COOP-DIAG | Cooperative diagonal from agreement matrix | P3 (flexible) | P2 (upgraded) | Not raised | **P2** |
| KEY-TYPES | Clarify best_responses key types | Not raised | P2 (P2-3 implied) | P2 (P2-6) | **P2** |
| INFO-LOG | INFO-level log on solver selection | Not raised | P2 (P2-3) | Not raised | **P2** |
| INTEG-TEST | Integration test with real nashopt | P3 (P3-10) | P2 (P2-2) | P2 (implied) | **P2** |
| ASYM-VALID | Asymmetric agreement matrix warning | P3 (P3-9) | P2 (part of COOP-DIAG) | Not raised | **P3** |
| PARAM-TESTS | Parametrize mode-specific matrix tests | Not raised | Not raised | P3 (P3-8) | **P3** |
| MODE-ERR | Unknown mode error message test | Not raised | Not raised | P3 (P3-9) | **P3** |
| ROUNDING | SolverResult rounding consistency | Not raised | Not raised | P3 (P3-10) | **P3** |

---

## Dangerous Contradictions Found

### DC-1: Spec internal inconsistency on matrix shapes

The spec's Section 2 table prescribes mode-specific shapes (N x 1 for WTA, 2 x K for red-blue) while the nashopt API signature at `spec.md:30` specifies `np.ndarray (N x N x actions)`. All three reviewers eventually agreed the inconsistency is real. solver-engineer initially treated this as an implementation bug and recommended N x N reformulation; plugin-engineer and spec-compliance correctly argued the implementation follows the spec and the inconsistency belongs at the spec level. solver-engineer withdrew the code fix in revision.

**Synthesis assessment**: This is a genuine spec defect. The implementation is compliant with the Section 2 table, but the table contradicts the API signature. This must be resolved via spec amendment before nashopt is exercised with non-NxN modes in production. The pre-call shape validation (P2) provides a runtime safety net.

### DC-2: FR-008 compliance -- error paths omit the `solver` key

solver-engineer's Phase 1 review marked FR-008 as fully passing. plugin-engineer found two error-path `PluginResult` returns that omit the key entirely. spec-compliance initially marked FR-008 as MET but upgraded to PARTIALLY MET in revision after accepting plugin-engineer's finding. This is a factual matter resolvable by code inspection: the error paths do omit the key. All three reviewers agree it must be fixed.

**Synthesis assessment**: FR-008 is PARTIALLY MET. The key is present on happy paths and absent on error paths. The fix is agreed upon; only the sentinel value is disputed (see Remaining Disputes below).

### DC-3: Post-processing loop indexes into wrong dimensions for non-NxN modes

The post-processing at `solver.py:416-424` iterates over N agent names but the red-blue mode produces a 2-row result. solver-engineer identified this in Phase 1. Initially the recommended fix (build N x N matrices) would have violated the spec. After cross-review, all three agents converged: the matrix shapes are correct per the spec, and the bug is in the result-to-agent mapping.

**Synthesis assessment**: This is a confirmed correctness bug in the post-processing layer. It will produce wrong results or crash for every red-blue mode invocation. The fix (map 2-player results back to N agents by role) is unanimously agreed upon.

---

## Systemic Contradictions

### SC-SYS-1: Spec delegates normalization to nashopt but does not verify compatibility

The spec says distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form" -- implying nashopt handles this internally. But the spec also prescribes heterogeneous matrix shapes per mode with wildly different value scales. If nashopt's normalization is shape-dependent, non-NxN matrices may not normalize correctly. solver-engineer's pre-normalization recommendation was withdrawn (correctly -- it could alter game semantics), but the underlying concern remains: the spec assumes nashopt's internal normalization handles all prescribed game forms without verification.

### SC-SYS-2: Heuristic and solver scores measure fundamentally different quantities

The heuristic computes score as `agents_at_eq / total_agents` (discrete fraction). The solver computes `1.0 - distance` (continuous metric). When the system switches between them on timeout, scores can jump discontinuously. The spec does not require cross-path score comparability, and the `solver` provenance field (FR-008) allows consumers to filter by path. However, consumers storing scores over time without filtering by `solver` will see unexplained variance. solver-engineer raised this; spec-compliance and plugin-engineer did not dispute the technical finding but correctly noted it is outside the spec's requirements.

### SC-SYS-3: Strategy profile construction is unspecified

The spec defines `strategy_profile` as an input to `check_equilibrium()` but does not specify how to construct it. The implementation uses a generic 4-element fallback vector whose dimensions do not match the mode-specific payoff matrix action spaces. All three reviewers acknowledge this will cause runtime errors. solver-engineer treats it as P1. spec-compliance frames it as a spec gap (the implementation has freedom but chose wrong dimensions). The fix is straightforward regardless of framing.

---

## Convergence Achieved

The following items achieved unanimous agreement across all three agents:

### 1. SC-001 and SC-002 threshold tests are blocking P1 items

The spec's two primary acceptance criteria have no corresponding test coverage. These are the spec author's definition of "done." spec-compliance identified this in Phase 1; solver-engineer and plugin-engineer adopted it in Phase 3. **Strength: unanimous.**

### 2. Per-agent equilibrium deviation must use `best_responses`, not the pessimistic fallback

The `hasattr(result, "agents_not_at_equilibrium")` guard checks for an API attribute the spec does not document. The blanket "all agents not at equilibrium" fallback defeats the purpose of the solver. The fix is to compare each agent's current strategy against their best response. All three reviewers independently identified this in Phase 1. **Strength: unanimous.**

### 3. ThreadPoolExecutor fix is `shutdown(wait=False, cancel_futures=True)` at P2 severity

solver-engineer originally proposed `multiprocessing`/`signal.alarm` at P1. After cross-review, all three agents agree the user-facing timeout behavior is correct (heuristic fallback fires), the resource leak is an operational concern (P2), and the targeted `shutdown(wait=False, cancel_futures=True)` fix is proportionate. **Strength: unanimous, achieved through revision.**

### 4. Matrix shapes are spec-prescribed; the bug is in post-processing

The WTA (N x 1) and red-blue (2 x K) shapes are intentional per the spec. Reformulating as N x N would violate spec semantics. The bug is the post-processing loop that maps solver results to N agents from a differently-shaped result. solver-engineer withdrew the N x N recommendation after cross-review. **Strength: unanimous, achieved through revision.**

### 5. Pre-call shape validation at the solver boundary

A shape-compatibility assertion before the nashopt call would surface incompatible dimensions with a clear message instead of opaque JAX errors. This is a defensive measure agreed upon by all three reviewers at P2 severity. **Strength: unanimous.**

### 6. Per-agent payoff data in the solver path is information loss at P2 severity

The `_score_from_solver` function hardcodes `payoff: 0.0` for all agents, losing information the heuristic path provides. All three agree this should be computed from the payoff matrix when available, sequenced after the FR-005 strategy-profile refactor. **Strength: unanimous.**

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

#### Dispute 1: Error-path `solver` key value -- `"heuristic"` vs. `"error"`

**Parties**: plugin-engineer + solver-engineer (favor `"heuristic"`) vs. spec-compliance (favors `"error"`)

**plugin-engineer/solver-engineer position**: The `solver` field is a routing tag, not a diagnostic log. The consumer contract is binary (`"nashopt"` | everything else). A third sentinel `"error"` silently expands the enum and forces every consumer to update branching logic. On error paths, no solver ran, so the result defaults to heuristic treatment. The `data["error"]` key already provides diagnostic information.

**spec-compliance position**: Error paths are semantically different from heuristic fallback. The heuristic computes a real score; error paths return 0.0 with an error message. Labeling an error as `"heuristic"` is a misrepresentation that would contaminate heuristic score aggregations. `"error"` makes the failure explicit.

**Synthesizer assessment**: Both positions have merit. The key question is the field's semantic contract: routing vs. diagnostic. The spec says the field exists "so consumers know which path ran." On error paths, neither the solver nor the heuristic ran -- labeling this as `"heuristic"` is technically inaccurate, but labeling it as `"error"` breaks binary consumer contracts.

**Recommended resolution**: Use `"heuristic"` to preserve binary routing, and add `"solver_error": true` (or equivalent) to error-path data dicts so consumers that need to distinguish error-fallback from genuine heuristic execution can do so. This preserves backward compatibility for existing consumers while providing diagnostic granularity for sophisticated consumers. The `data["error"]` key already present on these paths further serves the diagnostic purpose. This favors plugin-engineer's routing-tag interpretation while addressing spec-compliance's concern about silent error conflation.

#### Dispute 2: FR-003 and FR-007 compliance verdicts

**Parties**: solver-engineer (PARTIALLY MET for both) vs. spec-compliance (MET for both)

**solver-engineer position**: FR-003 cannot be MET when the spec is internally inconsistent (matrix table shapes vs. API signature). FR-007 cannot be MET when the timeout mechanism has a known resource leak that all reviewers agree needs fixing.

**spec-compliance position**: FR-003 asks "construct per-mode payoff matrices from FeatureSet data" -- the builders do this. The spec inconsistency is between FR-003 and FR-001 territory, not within FR-003. FR-007 asks for "configurable timeout with heuristic fallback" -- both are implemented. The resource leak is a quality-of-implementation concern, not a functional compliance failure. SC-004 (the FR-007 acceptance test) is MET.

**Synthesizer assessment**: spec-compliance's reading is more precise. FR-003 governs matrix construction, and the construction matches the spec's Section 2 table. The API shape incompatibility is a cross-FR gap, not an FR-003 deficiency. FR-007 governs timeout-with-fallback, and that mechanism works from the caller's perspective. However, solver-engineer's concern is valid: marking both as MET without qualification gives a false sense of completeness when agreed-upon follow-ups exist.

**Recommended resolution**: FR-003 is **MET with caveat** -- the construction is spec-compliant, but a spec amendment (solver-engineer's N-1) is required to reconcile the matrix shape table with the API signature. FR-007 is **MET** -- the functional requirement is satisfied. The resource leak is correctly tracked as a P2 fix recommendation, not a compliance failure. This preserves spec-compliance's reading of FR scope while acknowledging solver-engineer's valid concern about the spec inconsistency.

#### Dispute 3: Cooperative diagonal payoff source and asymmetric matrix handling

**Parties**: plugin-engineer (use agreement_matrix self-pair, validate symmetry, warn-and-proceed) vs. solver-engineer (validate symmetry, warn-and-proceed; silent on diagonal source)

**plugin-engineer position**: Mixing `surviving_count` for diagonal and agreement_matrix for off-diagonal produces a game with incoherent equilibria. The agreement matrix self-pair is semantically consistent with off-diagonal entries and should be used when present. Asymmetry should be validated with a warning, not silently repaired.

**solver-engineer position**: Agrees on asymmetry validation with warn-and-proceed. The original `max` symmetrization is withdrawn. The diagonal source question was not explicitly addressed in the revision.

**Synthesizer assessment**: plugin-engineer's argument about mixed payoff semantics is game-theoretically sound. When an agreement matrix is provided with self-pair data, using it for the diagonal maintains semantic consistency. solver-engineer does not oppose this -- the silence appears to be an oversight rather than a disagreement. spec-compliance did not engage on this topic.

**Recommended resolution**: Accept plugin-engineer's position. When `agreement_matrix` is populated and contains a self-pair entry, use it for the diagonal. Fall back to `surviving_count` only when agreement data is absent. Validate symmetry with a warning log (not a failure). This is a P2 item. solver-engineer's warn-and-proceed approach for asymmetry is adopted.
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1 -- Must Fix Before Merge

| # | Change | Source | Unanimous? |
|---|--------|--------|------------|
| 1 | Add SC-001 test: cooperative convergence score >= 0.9 with realistic feature data | spec-compliance P1-1, adopted by all | Yes |
| 2 | Add SC-002 test: 3+ disputes score < 0.5 with realistic feature data | spec-compliance P1-2, adopted by all | Yes |
| 3 | Fix FR-005: derive per-agent equilibrium deviation from `best_responses` by comparing each agent's current strategy against their best response; remove dead `hasattr(result, "agents_not_at_equilibrium")` guard; thread strategy profile into post-processing | All three reviewers | Yes |
| 4 | Add `"solver": "heuristic"` to both error-path `PluginResult` returns (unknown-mode at lines 371-378, computation-failure at lines 394-401); add `"solver_error": true` for distinguishability | plugin-engineer P1-1, spec-compliance NEW-1 | Yes (value resolved by synthesizer) |
| 5 | Fix post-processing at `solver.py:416-424`: map 2-player red-blue results back to N agents by role (red -> row 0, blue -> row 1); handle N x 1 WTA result as agent rankings | solver-engineer P1-2, plugin-engineer N3 | Yes |
| 6 | Fix strategy profile dimensions: derive strategy vector length from the payoff matrix's action dimension instead of using a generic 4-element fallback | solver-engineer P1-3 | Majority (spec-compliance did not raise but does not oppose) |
| 7 | Rewrite timeout test to exercise real `future.result(timeout=)` path with a blocking mock (e.g., `time.sleep(5)` with 0.01s timeout) instead of mock `side_effect` | plugin-engineer P1-2, spec-compliance upgraded | Yes |
| 8 | **Spec amendment**: reconcile Section 2 matrix shape table (N x 1 for WTA, 2 x K for red-blue) with the nashopt API signature (`N x N x actions`). Either define a shape adapter layer or document which modes use non-standard game forms | solver-engineer N-1 | Yes (as a spec-level action) |

### P2 -- Should Fix

| # | Change | Source | Unanimous? |
|---|--------|--------|------------|
| 9 | Replace `with ThreadPoolExecutor(...)` with explicit lifecycle: `executor.shutdown(wait=False, cancel_futures=True)` on timeout/exception | All three reviewers | Yes |
| 10 | Compute per-agent payoffs from payoff matrix in solver path instead of hardcoding 0.0; sequence after P1-3 (strategy profile refactor). Use `null` sentinel as interim if needed | All three reviewers | Yes |
| 11 | Add pre-call shape validation at solver boundary: assert payoff matrix dimensions are compatible with nashopt expectations before calling `check_equilibrium()` | plugin-engineer P3-1 upgraded, spec-compliance NEW-3 | Yes |
| 12 | Remove dead `total_surface` variable in `_build_rb_matrix` `max_k == 0` branch; normalize fallback-branch payoffs consistently with `max_k > 0` branch (severity-weighted ratios) | plugin-engineer P1-3 downgraded + P3-3, spec-compliance NEW-2 | Yes |
| 13 | Fix cooperative diagonal: use `agreement_matrix[i][i]` when agreement matrix is populated, fall back to `surviving_count` only when absent; validate symmetry with warning log | plugin-engineer P3-2 upgraded, solver-engineer P3-9 | Majority |
| 14 | Clarify `best_responses` key types: pin down whether nashopt uses int indices or string agent names; replace dual-lookup with explicit mapping | solver-engineer OBA-4, spec-compliance P2-6 | Yes |
| 15 | Add INFO-level log when solver path is selected: log timing and distance after successful solver call | plugin-engineer P2-3 | No opposition |
| 16 | Add conditional integration test with real nashopt (`pytest.importorskip`): both API contract validation and known-equilibrium numerical test (e.g., 2x2 PD with analytically known Nash solution) | solver-engineer P3-10, plugin-engineer P2-2 | Yes |

### P3 -- Nice to Have

| # | Change | Source |
|---|--------|--------|
| 17 | Parametrize mode-specific matrix tests to reduce duplication | spec-compliance P3-8 |
| 18 | Add test for unknown mode error message (verify it includes available modes list) | spec-compliance P3-9 |
| 19 | Document SolverResult rounding precision choices (score to 4dp, distance to 6dp) | spec-compliance P3-10 |
| 20 | Add asymmetric agreement matrix warning test with triangular input | solver-engineer P3-9 |

---

## Key Concessions

### solver-engineer concessions (Phase 3)

1. **Withdrew WTA N x N reformulation.** Accepted that the N x 1 shape is spec-prescribed and the bug is a spec inconsistency, not an implementation defect. Reframed as spec amendment request (N-1).
2. **Withdrew payoff normalization recommendation.** Accepted that the spec delegates normalization to nashopt and pre-normalizing could alter game semantics.
3. **Withdrew score reconciliation mechanism.** Accepted that running both paths doubles computation for incommensurable scores with no actionable threshold.
4. **Downgraded ThreadPoolExecutor from P1 to P2.** Accepted that user-facing timeout behavior is correct and the resource leak is operational, not a correctness failure. Dropped `multiprocessing`/`signal.alarm` suggestions.

### plugin-engineer concessions (Phase 3)

1. **Downgraded dead `total_surface` variable from P1 to P2.** Accepted that the dead variable alone is not a ship-blocker; merged with normalization fix.
2. **Adopted SC-001/SC-002 testing as P1.** Acknowledged as a scope gap in the original review, adopted from spec-compliance.
3. **Accepted FR-005 PARTIALLY MET verdict.** Originally marked as PASS; accepted spec-compliance's more precise assessment.
4. **Revised `solver` key fix from `"error"`/`"unavailable"` to `"heuristic"`.** Accepted solver-engineer's argument about binary enum preservation.

### spec-compliance concessions (Phase 3)

1. **Downgraded FR-008 from MET to PARTIALLY MET.** Accepted plugin-engineer's finding of missing `solver` key on error paths.
2. **Upgraded real-timeout test from P2 to P1.** Accepted that the mock tests a fundamentally different exception propagation path.
3. **Upgraded thread cancellation from P3 to P2.** Accepted that `shutdown(wait=True)` blocking under JAX workloads is a real operational concern.
4. **Adopted pre-call shape validation (NEW-3).** Synthesized from solver-engineer's shape concerns and plugin-engineer's defensive validation recommendation.

---

## Final Compliance Verdict Summary

| Requirement | Verdict | Notes |
|-------------|---------|-------|
| FR-001 | MET | Solver dispatch with optional import works correctly |
| FR-002 | MET | Heuristic fallback preserves pre-021 behavior |
| FR-003 | MET (with caveat) | Builders follow spec Section 2 table; spec inconsistency with API signature requires amendment |
| FR-004 | MET | Distance clamping and `1.0 - distance` formula correct |
| FR-005 | PARTIALLY MET | Best-response reporting uses blanket fallback; must derive from `best_responses` |
| FR-006 | MET | Degenerate cases (0, 1, zero-variance) handled correctly |
| FR-007 | MET | Configurable timeout with heuristic fallback works; executor lifecycle fix tracked as P2 |
| FR-008 | PARTIALLY MET | Missing on two error-path returns |
| SC-001 | UNVERIFIED | No threshold test exists |
| SC-002 | UNVERIFIED | No threshold test exists |
| SC-003 | MET | Heuristic behavior byte-identical without nashopt |
| SC-004 | MET | Timeout produces fallback, not error |
