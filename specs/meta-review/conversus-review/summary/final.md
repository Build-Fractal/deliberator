# Meta-Review Final Synthesis — Specs 021-030

**Date**: 2026-04-01
**Deliberation**: 4 agents, 5 phases, 21 files
**Specs reviewed**: 021, 022, 023, 025, 026, 029, 030

---

## 1. Process Summary

Four auditors reviewed seven spec synthesis documents across specs 021-030:

| Auditor | Scope | Key Method |
|---|---|---|
| **consistency-auditor** | Cross-spec behavioral contracts, shared interfaces, contradictions | Side-by-side synthesis comparison + code inspection |
| **dependency-auditor** | Import boundaries, architectural layering, coupling rules | Exhaustive grep of all imports across the codebase |
| **implementation-verifier** | Synthesis claim accuracy against actual code (3 claims/spec) | Line-by-line code verification of 21 claims |
| **test-coverage-auditor** | Test coverage of P1 findings, SC test presence | Test file analysis against synthesis claims |

The deliberation progressed through:
- **Phase 1**: Independent reviews (4 files)
- **Phase 2**: Cross-reviews — each auditor reviewed the other 3 (12 files)
- **Phase 3**: Revisions incorporating cross-review feedback (4 files)
- **Phase 4**: Final disputes and convergence (4 files)
- **Phase 5**: This synthesis (1 file)

---

## 2. Recommendation Scorecard

### Unanimous (all 4 auditors agree)

| ID | Priority | Recommendation | Specs Affected | Status |
|---|---|---|---|---|
| R-1 | **P1** | Fix scaffold file extension in `base.py:447` — search `.yml`, `.yaml`, `.json` in order | 029, 030 | Confirmed in code |
| R-2 | **P1** | Fix `DomainScore.variables` omission in `CodeReviewDomain.score()` at `domain.py:448` | 029 | **Most validated finding** — confirmed by all 4 auditors independently |
| R-4 | **P1** | Add `highspy` to the AMPL import guard at `ampl_model.py:29-34` | 023 | Confirmed in code |
| R-11 | **P1** | Write failing tests for CSI-1, CSI-2, CSI-3, CSI-4 BEFORE fixing code | 021-030 | New (from deliberation) |
| R-3 | **P1** | Refactor `CodeReviewDomain.score()` to delegate to `super().score()` | 029, 030 | **Sequenced**: R-1 -> R-11 tests -> R-3 |
| T-1 | **CRITICAL** | Add SC-001/SC-002 threshold tests for spec 021 | 021 | Zero test coverage for spec's own acceptance criteria |
| T-7 | **CRITICAL** | Add YAML scaffold loading test for spec 030 `score()` | 030 | Surfaces CSI-1 bug immediately |

### Majority (3 of 4 agree)

| ID | Priority | Recommendation | Dissent |
|---|---|---|---|
| R-8 | **P2** | Standardize solver provenance keys across plugin wrappers (`equilibrium_scorer.py`, `config_optimizer.py`) | None explicit; adjusted file targets after Phase 2 |
| R-9 | **P2** | Add BayesianGame prior key validation (`game_forms.py:403-412`) | None |
| R-5 | **P2** | Shared optional-import convention (`HAS_*` pattern) | None |
| D-1 | **P1** | Rewrite `domains/__init__.py` docstring as coupling RULE (not dependency claim) | test-coverage-auditor rates P2 unless bundled with import-linter |
| ORC | **P1** | Investigate orchestration layer — how plugins/domains wire into engine | Scope disputed: dependency-auditor wants full architecture review; consistency-auditor wants dependency matrix only |

### Split or deferred

| ID | Priority | Recommendation | Status |
|---|---|---|---|
| R-6 | **P3** | Document eq_score discontinuity as precondition for spec 022 Remediation 6 | Downgraded from P2; implementation-verifier prefers design note |
| R-7 | **P2** | Annotate `mode-mapping.yml` modes with solver type | Narrowed: only congestion games map to payoff matrices |

---

## 3. Dangerous Contradictions Found

The deliberation surfaced contradictions *between auditors* that required resolution:

### Resolved

| Contradiction | Resolution |
|---|---|
| Dependency-auditor's "all clean" vs. consistency-auditor's cross-spec bugs | **Both correct at different scopes.** Import boundaries are clean; behavioral contracts are broken within those boundaries. Consensus: import verification is necessary but insufficient. |
| Implementation-verifier's "INACCURATE" label vs. consistency-auditor's "bugs are real" | **Reclassified to "MISLOCATED."** The 2 spec 021 findings describe real bugs attributed to the wrong file (`solver.py` vs. plugin wrapper). Not fabricated, just misplaced. |
| Test-coverage-auditor's 41% finding vs. implementation-verifier's 86% accuracy | **Both correct, measuring different things.** 86% = synthesis-to-code accuracy. 41% = code-to-test coverage for P1 items. Combined pipeline: synthesis -> code (86%) -> test (41%). |

### Unresolved (minor)

| Contradiction | Status |
|---|---|
| `domains/__init__.py` docstring priority: P1 (dependency-auditor) vs. P2 (test-coverage-auditor) | **Split.** Consensus on the fix content (coupling RULE). Priority depends on whether import-linter lands simultaneously. |
| CSI-3 tracking: P3 item (consistency-auditor) vs. design note (implementation-verifier) | **Deferred.** Both agree the finding is real and dormant. Format is editorial, not substantive. |

---

## 4. Systemic Contradictions

Patterns that emerged across multiple specs, not just individual bugs:

### SC-SYS-1: The Override Antipattern (specs 029/030)

`CodeReviewDomain.score()` reimplements the entire scoring pipeline from `DomainPlugin.score()` — weighted scores, hard blocks, verdicts, recommendations — instead of delegating to the inherited pipeline. This reimplementation is the root cause of both CSI-1 (scaffold extension mismatch) and CSI-2 (`DomainScore.variables` omission). Any future domain that copies this pattern will inherit the same class of bugs. **The base class scoring pipeline must be the single path, with subclasses providing only dimension-specific logic (extractors, normalizers, scaffolds).**

### SC-SYS-2: Untested P1 Findings (specs 021, 022, 023)

The three solver-layer specs have the lowest test coverage for their most critical findings. Spec 021 has 6+ untested P1 items including its own acceptance criteria (SC-001/SC-002). Spec 022 has 3 compliance remediations with no test coverage. Spec 023 has an import guard gap with no test. **The pattern: the riskiest code is the least tested.** This is the inverse of the expected relationship.

### SC-SYS-3: Aspirational Cross-Spec Dependencies (specs 021-030)

Of 6 identified cross-spec dependencies, only 1 is verified in code (spec 029 -> spec 030 domain base). The remaining 5 are described in syntheses but not implemented. This means cross-spec planning is ahead of cross-spec implementation. **Risk: specs are designed against interfaces that do not yet exist and may not materialize as designed.**

### SC-SYS-4: Missing Orchestration Layer (specs 021, 022, 030)

The engine (`engine/`) imports nothing from plugins, domains, or schemas. Plugin execution, domain lifecycle, and inter-plugin data flow all require a wiring layer that no spec has defined, no synthesis has verified, and no test exercises. **This is the single largest shared blind spot across all 4 reviews.**

---

## 5. Convergence Achieved

The following findings have **unanimous agreement** across all 4 auditors after the full deliberation:

1. The dependency architecture (import boundaries, layer hierarchy, package isolation) is **correct and clean**. No boundary violations exist.
2. Plugin-to-plugin isolation is the **strongest architectural property** in the codebase.
3. `schemas/` is a **true leaf package** with zero upstream dependencies.
4. Specs 025 (Game Form Expansion) and 026 (Optimization Template Library) are the **healthiest specs** — all claims verified, all SC tests pass, clean dependencies, no cross-spec issues.
5. Spec 021 (nashopt Solver Integration) is the **weakest spec** — mislocated findings, most untested P1s, missing acceptance criteria tests, source of 2 cross-spec inconsistencies.
6. The `DomainScore.variables` omission (R-2) is the **single most validated bug** — confirmed independently by all 4 auditors from code verification, cross-spec impact, dependency safety, and test gap perspectives.
7. **Test-first development** should be adopted for all P1 code fixes: write a failing test, then fix the code, then verify the test passes.
8. Import-level verification is **necessary but insufficient** for dependency health. Behavioral contracts and test verification are also required.
9. The mathematical implementations (Shapley values, Kalman filter mechanics, potential game diagnostic) are **correct and well-tested**.
10. The frozen Pydantic model convention is **consistently applied** across all domain state models.

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

1. **`domains/__init__.py` docstring priority**: P1 (dependency-auditor) vs. P2 (test-coverage-auditor). Content agreed (coupling RULE rewrite). Priority depends on whether automated enforcement via import-linter is bundled.

2. **CSI-3 tracking format**: P3 recommendation (consistency-auditor) vs. design note on spec 022 Remediation 6 (implementation-verifier). Both agree the finding is real, dormant, and contingent on future work. Disagreement is editorial.

3. **Orchestration layer investigation scope**: Full architecture review including sequence diagrams and DI feasibility assessment (dependency-auditor) vs. structured dependency matrix + import-linter config (consistency-auditor). Both agree on P1 urgency for investigation.
<!-- CONVERSUS:DISPUTES_END -->

---

## 6. Actionable Spec Changes

### Cross-spec bugs (affect multiple specs)

| ID | Bug | Files | Fix | Sequence | Test Needed |
|---|---|---|---|---|---|
| **CSI-1** | `DomainPlugin.score()` hard-codes `.json`; `CodeReviewDomain.score()` uses `.yml` — base class will break future YAML-using domains | `domains/base.py:447` | Search `.yml`, `.yaml`, `.json` in order | **First** (blocks R-3) | `test_domains.py`: load `.yml` scaffold through `score()` |
| **CSI-2** | `CodeReviewDomain.score()` does not pass `variables=variables` to `DomainScore` constructor — divergence from base class contract | `domains/code_review/domain.py:448` | Add `variables=variables` to constructor | After CSI-1 test | `test_code_review.py`: assert `score.variables` is populated |
| **CSI-4** | Solver provenance keys inconsistent: spec 021 uses `solver` on `PluginResult`; spec 023 returns `None` for failures | Plugin wrappers (`equilibrium_scorer.py`, `config_optimizer.py`) | Standardize `solver` + `solver_status` keys on all `PluginResult` error/success paths | Independent | Assert `"solver" in result.data` on error paths |

### Per-spec P1s (aggregated from all 7 spec reviews)

**Spec 021 — nashopt Solver Integration** (weakest spec)
| Finding | Source | Test Status |
|---|---|---|
| SC-001/SC-002 acceptance criteria unverified | test-coverage-auditor | **NO TEST** — CRITICAL gap |
| Per-agent equilibrium from `best_responses` not implemented | 021 synthesis P1-3 | NO TEST |
| `solver` key missing on error-path `PluginResult` returns | 021 synthesis P1-4 | PARTIAL (happy path only) |
| Post-processing mapping for non-NxN modes (red-blue 2-row) | 021 synthesis P1-5 | NO TEST |
| Strategy profile dimension mismatch — 4-element vector vs. variable matrix dimension | 021 synthesis P1-6 | PARTIAL |
| Real-timeout integration test needed (current test uses mock `side_effect`) | 021 synthesis P1-7 | NO TEST |

**Spec 022 — Kalman Convergence**
| Finding | Source | Test Status |
|---|---|---|
| Innovation sequence computed but discarded (`kalman.py:289`) — FR-005 compliance gap | 022 synthesis Remediation 1 | NO TEST |
| Plugin config Q/R not wired (`predictor.py:252-259`) — FR-007 compliance gap | 022 synthesis Remediation 2 | NO TEST |
| Confidence calibration initialization-dependent (`kalman.py:385-410`) | 022 synthesis Remediation 4 | NO TEST |
| SC-002 test assertion relaxed (uses `0.5x` instead of `1.0x` threshold) | test-coverage-auditor | Exists but non-compliant |

**Spec 023 — AMPL Config Optimizer**
| Finding | Source | Test Status |
|---|---|---|
| `HAS_AMPL` guard checks only `amplpy`, not `highspy` (`ampl_model.py:29-34`) | 023 synthesis (unanimous) | NO TEST |
| `gap: 0.0` hardcoded, not extracted from solver output (`ampl_solver.py:149`) | 023 synthesis P2 | NO TEST (mock) |
| `solve_with_ampl()` returns `None` for 3 distinct failure modes — no structured error | 023 synthesis P2 | NO TEST |

**Spec 025 — Game Form Expansion** (healthy)
| Finding | Source | Test Status |
|---|---|---|
| `BayesianGame.validate_structure()` does not validate prior keys against type profile Cartesian product | 025 synthesis Dispute 2 | NO TEST |
| `is_potential_game()` limited to 2-player — no N-player generalization | 025 synthesis Dispute 1 | NO TEST (Low) |

**Spec 026 — Optimization Template Library** (healthy)
| Finding | Source | Test Status |
|---|---|---|
| Template `game_form` values not cross-validated against `game-forms/*.yml` | 026 synthesis Dispute 1 | NO TEST (Low) |
| Constraint `gap_question` test coverage missing | 026 synthesis Dispute 2 | NO TEST (Low) |

**Spec 029 — Code Review Domain**
| Finding | Source | Test Status |
|---|---|---|
| `DomainScore.variables` not populated (P1-1) | 029 synthesis | NO TEST |
| Duplicate `format_compliant` and `has_changelog_entry` across extractors (P1-2) | 029 synthesis | NO TEST |
| `_INVERTED_BOOLEANS` is local to function, not module-level constant (P1-3) | 029 synthesis | N/A (code organization) |
| Scoring pipeline reimplements base class instead of delegating (architectural) | consistency-auditor CSI-2/R-3 | NO TEST |

**Spec 030 — Domain Plugin Architecture**
| Finding | Source | Test Status |
|---|---|---|
| `score()` hard-codes `.json` scaffold extension (FR-018) | 030 synthesis | NO TEST |
| Gate lifecycle absent (Dispute 1) — NOT MET | 030 synthesis | NO TEST |
| Plugin discovery not implemented (Dispute 2) — NOT MET | 030 synthesis | NO TEST |
| `_matches_filters` silently ignores unknown filter keys (Dispute 5) | 030 synthesis | NO TEST |
| Hard block string validation missing (Dispute 4) | 030 synthesis | NO TEST |

### Test gaps (untested P1 findings requiring new tests)

| Priority | Test | Target File | Expected Result |
|---|---|---|---|
| **CRITICAL** | Spec 021 SC-001: cooperative convergence score >= 0.9 | `test_solver.py` or `test_nashopt.py` | Should pass if solver works correctly |
| **CRITICAL** | Spec 021 SC-002: 3+ disputes score < 0.5 | `test_solver.py` or `test_nashopt.py` | Should pass if solver works correctly |
| **CRITICAL** | CSI-1: Load `.yml` scaffold through `DomainPlugin.score()` | `test_domains.py` | **Expected FAIL** (`.json` hardcoded) |
| **CRITICAL** | CSI-2: Assert `DomainScore.variables` populated after `CodeReviewDomain.score()` | `test_code_review.py` | **Expected FAIL** (variables not passed) |
| **HIGH** | CSI-4: Assert `"solver"` key on error-path `PluginResult` | `test_equilibrium_scorer.py` | **Expected FAIL** on at least one path |
| **HIGH** | Spec 021: Real-timeout test (replace mock `side_effect` with `time.sleep`) | `test_solver.py` | Validates heuristic fallback path |
| **HIGH** | Spec 022 SC-002: Tighten assertion from `0.5x` to `1.0x` | `test_kalman.py` | May fail — investigate parameters |
| **HIGH** | 029/030 scoring pipeline integration test (base vs. override comparison) | `test_code_review.py` | Documents behavioral divergence |
| **MEDIUM** | Spec 022: Innovation sequence stored in `KalmanState` | `test_kalman.py` | Blocked until `KalmanState` field added |
| **MEDIUM** | Spec 023: `highspy` presence check in import guard | `test_ampl.py` | **Expected FAIL** (only `amplpy` checked) |
| **MEDIUM** | Spec 025: BayesianGame garbage prior keys rejected | `test_game_forms_expanded.py` | **Expected FAIL** (keys not validated) |
| **MEDIUM** | Spec 026: Constraint `gap_question` tests | `test_templates_expanded.py` | Should pass |
| **MEDIUM** | Spec 030: Two-domain store isolation | `test_domains.py` | Should pass |
| **MEDIUM** | Spec 021: Red-blue 2-row result mapped to N agents | `test_solver.py` | **Expected FAIL** (dimension mismatch) |

### Architecture issues (coupling, interfaces, missing layers)

| ID | Issue | Impact | Recommendation |
|---|---|---|---|
| **ARC-1** | `CodeReviewDomain.score()` reimplements base class scoring pipeline | Root cause of CSI-1 and CSI-2; future domains will copy the antipattern | Refactor to `super().score()` delegation (after CSI-1 fix) |
| **ARC-2** | No orchestration layer connects plugins/domains to the engine | Blocks gate lifecycle (030), inter-plugin data flow (022), plugin hooks (021) | P1 investigation: identify entry points, assess DI feasibility |
| **ARC-3** | `domains/__init__.py` docstring claims false dependencies (`plugins.base`, `schemas`) | Misleads contributors about coupling rules | Rewrite as coupling RULE: "MUST NOT import from engine, linter, web, mcp_server" |
| **ARC-4** | `VariableExtractor` protocol not verified at runtime | Extractors implement protocol via duck typing without importing it | Add `@runtime_checkable` to protocol; add `isinstance` assertions in tests |
| **ARC-5** | 5 of 6 cross-spec dependencies are aspirational, not implemented | Specs designed against interfaces that do not exist | Track verified vs. aspirational status per dependency |
| **ARC-6** | No cross-spec integration tests exist | Each spec tested in isolation; cross-boundary bugs invisible to test suite | Start with 029/030 scoring pipeline integration test |
| **ARC-7** | `mode-mapping.yml` (9 modes) and `solver.py` (4 modes) are misaligned | Templates may declare modes with no solver support | Annotate each mode with its solver type in `mode-mapping.yml` |
| **ARC-8** | Optional-import pattern (`HAS_*` flag) reimplemented 3 times | No shared convention; spec 030 will need it for plugin discovery | Formalize as `conversus.utils.optional_imports` helper or documented pattern |

---

## 7. Key Concessions

Positions abandoned or significantly modified during deliberation:

| Auditor | Original Position | Conceded To | Reason |
|---|---|---|---|
| **consistency-auditor** | CSI-3 is P2 | P3 / design note | Bug is dormant (eq_score=0.0), integration path does not exist, orchestration layer unverified |
| **consistency-auditor** | Scaffold test outranks SC-001/SC-002 | Both are CRITICAL (parallel) | Test-coverage-auditor's two-category system accepted |
| **dependency-auditor** | Import cleanliness = dependency health | Import cleanliness is necessary but insufficient | Consistency-auditor's behavioral contract bugs exist within clean boundaries |
| **dependency-auditor** | Docstring fix is simple correction | Docstring should be coupling RULE, not dependency claim | Implementation-verifier's reframing is more durable |
| **implementation-verifier** | "INACCURATE" for spec 021 findings | "MISLOCATED" — bugs are real, file attribution wrong | Consistency-auditor correctly noted the findings exist in a different file |
| **implementation-verifier** | Fix list does not need sequencing | R-1 must precede R-3 | Consistency-auditor identified scaffold fix as prerequisite for delegation refactor |
| **test-coverage-auditor** | Several test recommendations are "blocked" | Tests can be written against current buggy behavior | Implementation-verifier noted characterization tests are valuable for bug documentation |
| **test-coverage-auditor** | Single CRITICAL category | Two CRITICAL categories (acceptance + cross-spec regression) | Consistency-auditor's argument that both types deserve top priority |

---

## Appendix: Verification Metrics

### Implementation Verification (21 claims spot-checked)

| Spec | Verified | Mislocated | Stale | Accuracy |
|---|---|---|---|---|
| 021 nashopt | 1 | 2 | 0 | 33% |
| 022 Kalman | 3 | 0 | 0 | 100% |
| 023 AMPL | 3 | 0 | 0 | 100% |
| 025 Game Forms | 3 | 0 | 0 | 100% |
| 026 Templates | 3 | 0 | 0 | 100% |
| 029 Code Review | 3 | 0 | 0 | 100% |
| 030 Domain Plugin | 3 | 0 | 0 | 100% |
| **Total** | **19** | **2** | **0** | **90%** |

### Test Coverage of P1 Findings

| Metric | Value |
|---|---|
| Total P1 findings (single-spec) | 22 |
| P1 findings with test coverage | 9 (41%) |
| P1 findings without test coverage | 13 (59%) |
| Cross-spec P1 findings (meta-review) | 4 (CSI-1 through CSI-4) |
| Cross-spec P1 findings with test coverage | 0 (0%) |
| **Combined P1 findings without test coverage** | **17 of 26 (65%)** |

### Dependency Architecture

| Property | Status |
|---|---|
| Import boundary violations | **0** |
| Cycles in dependency DAG | **0** |
| Plugin-to-plugin imports | **0** |
| schemas/ upstream dependencies | **0** |
| Docstring-reality mismatches | **1** (`domains/__init__.py`) |
| Cross-spec dependencies verified in code | **1 of 6** |

### Spec Health Ranking

| Rank | Spec | Rationale |
|---|---|---|
| 1 | **025 Game Form Expansion** | All claims verified, all SC tests pass, clean dependencies, 2 Low-priority items |
| 2 | **026 Optimization Template Library** | All claims verified, all SC tests pass, clean dependencies, 2 Low-priority items |
| 3 | **030 Domain Plugin Architecture** | All claims verified, strong base layer tests, 5 NOT MET items (Phase 2 scope) |
| 4 | **022 Kalman Convergence** | All claims verified, 3 compliance gaps identified and tracked, SC tests present |
| 5 | **029 Code Review Domain** | All claims verified, 2 P1 bugs confirmed, override antipattern identified |
| 6 | **023 AMPL Config Optimizer** | All claims verified, import guard bug confirmed, strong quality model tests |
| 7 | **021 nashopt Solver Integration** | 2 mislocated findings, 6+ untested P1s, missing acceptance criteria tests, 2 cross-spec issues |
