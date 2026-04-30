# Spec 006 — Phase 2 SPEC (Inter-Round Arbitration completion)

**Feature ID**: `006-inter-round-arbitration` (Phase 2)
**Created**: 2026-04-29
**Status**: Draft — Phase 2 of spec 006, codifying the 7-point IMPLEMENTATION-GAP into an executable spec.
**Depends On**: `006-inter-round-arbitration/spec.md` (the original; Phase 1 partial), `006-inter-round-arbitration/IMPLEMENTATION-GAP.md` (the source checklist).
**Originating context**: 2026-04-29 burndown investigation — read-only triage of `engine/config.py`, `engine/output.py`, `engine/phases.py`, `engine/templates.py`, `linter/quality.py`, and `engine/tests/test_006_inter_round_arbitration.py` against the IMPLEMENTATION-GAP 7-point checklist found 1 of 7 shipped, 4 partial, 2 unshipped.

> **Scope discipline**: this Phase 2 SPEC operationalizes the 7-point checklist as numbered FRs. It does NOT redesign inter-round arbitration; it completes the partial work from Phase 1. Phase 1 is "shipped enough to use"; Phase 2 brings it to spec compliance.

---

## 1. Goal

Complete spec 006's Phase 1 partial work so the inter-round arbitration design ships to spec compliance. The 7 IMPLEMENTATION-GAP points become the 7 FRs of this Phase 2 spec; once all FRs are met, spec 006 (parent) closes and moves to `specs/done/`.

## 2. In-scope

The 7 FRs below correspond directly to the IMPLEMENTATION-GAP checklist. Phase 2 ships when all 7 are satisfied.

### FR-P2-1 — Config schema validation strictness

The `arbiter` config block accepts `timing` and `influence` fields (already shipped in `engine/config.py:73-77` + parser at `:546-557`). FR-003 requires that `timing: inter-round` combined with `rounds: 1` (or omitted) MUST be REJECTED — current code only WARNS at `engine/config.py:728-733`.

**Acceptance**: invalid combos raise `ConfigError` rather than logging a warning. Test added: `test_inter_round_with_single_round_rejects` asserts `ConfigError` and the existing warn path is removed.

### FR-P2-2 — Output paths: `arbiter/` → `arbitration/`

Spec FR-006 says arbitration output lives at `{base}/arbitration/resolution.md`. Current `OutputManager.get_arbitration_path` at `engine/output.py:264` writes to `{base}/arbiter/resolution.md`. Every test that asserts on the old path needs a sweep.

**Acceptance**:
- `OutputManager.get_arbitration_path` returns `{base}/arbitration/resolution.md`.
- Tests in `engine/tests/test_006_inter_round_arbitration.py`, `engine/tests/test_phases.py`, and any other path-aware tests updated.
- Backward-compatible reading: if a deliberation-run output dir contains `arbiter/resolution.md` (from a pre-FR-P2-2 run), the engine reads it fall-back style without erroring. New runs always write `arbitration/`.

### FR-P2-3 — Execution model (already SHIPPED — verify)

Round-loop dispatch is wired (`engine/phases.py:836-943`); `prior_arbitration_path` is plumbed through `_run_single_round` (`:259-299`, `:770`, `:812`, `:911`). This FR exists to **verify** — Phase 2 does not re-implement what's already shipped, but a parity test confirms the round-loop behavior matches spec 006's §4 execution model.

**Acceptance**: `test_006_round_loop_parity` asserts that for `rounds: 2 + arbiter timing: inter-round`, Round 2 receives `prior_arbitration_path` populated with Round 1's resolution path.

### FR-P2-4 — Influence-aware dispute counting

`linter/quality.py::check_disagreement` has no `influence` parameter or arbiter-addressed handling. `engine/phases.py:947` calls it without any influence-aware adjustment. Spec FR-009 through FR-012 require:
- `binding` influence: arbiter-addressed disputes are removed from the count.
- `recommended` influence: arbiter-addressed disputes are removed from the count if the addressed party in their next-round dispute does NOT re-raise the issue, OR re-raise if they do.
- `advisory` influence: disputes left counted (current behavior).

**Acceptance**:
- `check_disagreement` signature extended with `influence: InfluenceLevel | None = None` and `arbiter_addressed: list[str] | None = None`.
- Per-influence handling implemented per spec FR-009 to FR-012.
- Tests added: SC-002 (advisory leaves counted), SC-003 (recommended re-open).

### FR-P2-5 — Template language: `INFLUENCE_LEVEL` and `PRIOR_ARBITRATION_SECTION` populated

Schema variables exist (`schema/variables.yml:169,183`); `linter/models.py:263,361`); templates reference them (`templates/{mode}/arbitration.md`, `review.md`). But `build_arbitration_context` at `engine/templates.py:629-642` does NOT read `config.arbiter.influence` into `INFLUENCE_LEVEL`; `build_review_context` at `:261-277` leaves `PRIOR_ARBITRATION_SECTION` defaulted to `""`.

**Acceptance**:
- `build_arbitration_context` reads `config.arbiter.influence` and substitutes the value into `INFLUENCE_LEVEL`.
- `build_review_context` accepts a `prior_arbitration_path` kwarg and, when present, populates `PRIOR_ARBITRATION_SECTION` from the prior round's resolution.
- Equivalent edits for `build_cross_review_context`, `build_revision_context`, `build_disputes_context`, and `build_synthesis_context` if they reference these variables.
- Existing template-validation tests cover the new substitutions; no schema changes required.

### FR-P2-6 — Cross-round synthesis Resolution Attribution

`build_cross_round_synthesis_context` accepts `arbitration_paths`/`arbitration_rulings` kwargs (`engine/templates.py:656`); the call site at `engine/phases.py:987` does NOT pass them. `run_pipeline` does not accumulate per-round arbitration paths in any structure that the cross-round synthesis can consume.

**Acceptance**:
- `run_pipeline` accumulates a `list[Path]` of per-round arbitration outputs.
- `phases.py:987` call site passes `arbitration_paths=` and `arbitration_rulings=` (loaded from disk) to `build_cross_round_synthesis_context`.
- The cross-round synthesis template's "Resolution Attribution" section renders correctly with non-empty data.
- SC-007 test added: cross-round synthesis includes Resolution Attribution attribution strings derived from the per-round arbitration paths.

### FR-P2-7 — SC-002 / SC-003 / SC-007 / SC-008 test coverage

Per spec 006 §SC, scenarios:
- SC-002: advisory leaves disputes counted (Phase 2 FR-P2-4 enables; test covers).
- SC-003: recommended re-opens when addressed party re-raises (Phase 2 FR-P2-4; test covers).
- SC-007: Resolution Attribution attribution strings (Phase 2 FR-P2-6; test covers).
- SC-008: stagnation × influence interactions (covered by combining FR-P2-4 + existing stagnation detection).

**Acceptance**: 4 new tests added (one per SC). Each includes the input config, expected output behavior, and a passing assertion. Tests live in `engine/tests/test_006_inter_round_arbitration.py`.

## 3. Out-of-scope

- **Re-architecting inter-round arbitration**. The Phase 1 design holds; Phase 2 completes its implementation.
- **New influence levels beyond `binding`/`recommended`/`advisory`**. The 3-level taxonomy is settled.
- **Backward compatibility for the `arbiter/` → `arbitration/` rename beyond read-only fallback**. New runs write `arbitration/`; old runs are read-fallback only. No migration tooling.
- **Cross-mode arbitration semantics changes** (red-blue, prisoners-dilemma). Phase 2 only completes the cooperative-mode and winner-take-all-mode arbitration that Phase 1 partially shipped.

## 4. Sequencing — easiest first

1. **FR-P2-1** + **FR-P2-2** (combined PR): smallest atomic change, biggest visible signal. Validation strictness is a 1-line behavior flip; path rename touches `OutputManager` + retroactive_move + every arbitration test. The pair lands together because both are pure rename/strictness with no behavioral entanglement.
2. **FR-P2-5** (templates): wire `INFLUENCE_LEVEL` + `PRIOR_ARBITRATION_SECTION` through 5 context builders. Independent of dispute counting; lands second.
3. **FR-P2-4** (influence-aware dispute counting): introduces the `influence` parameter to `check_disagreement` + recommended-re-open logic. Largest behavioral change.
4. **FR-P2-6** (cross-round Resolution Attribution): wires the `arbitration_paths` kwarg + path accumulation; depends on FR-P2-2's path stability.
5. **FR-P2-3** (parity test) + **FR-P2-7** (SC-002/003/007/008 tests): test work, lands last and validates the prior 4 PRs.

## 5. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| FR-P2-2 path rename breaks every test that asserts on `arbiter/resolution.md` | Medium | Sweep all path-aware tests in one PR; CI catches misses; backward-read fallback prevents user-data regressions. |
| FR-P2-4 influence-aware logic introduces subtle re-open bugs | High | TDD: write SC-002/003 tests first, then implement; fail-loud on unexpected influence values. |
| FR-P2-5 template variable wiring drifts from schema | Low | Existing schema/template validation lints catch mismatches at CI time; spec 071 §6 lint also surfaces structural violations. |
| FR-P2-6 path accumulation memory growth at high `rounds` | Low | `rounds` is bounded at 5 by the engine; max 5 paths stored. |
| FR-P2-7 tests pass but mask real failure modes | High | Apply Principle XXVIII — each test must include the failure scenario it catches; `legitimate-test-bug` PR template categorization required. |

## 6. Acceptance criteria for Phase 2

Phase 2 ships when:

1. All 7 FRs are met (verified via the dedicated tests in FR-P2-7).
2. `engine/tests/test_006_inter_round_arbitration.py` has 0 skipped / 0 xfail tests covering the 4 SCs.
3. The original spec 006's IMPLEMENTATION-GAP.md is updated to reflect "all 7 points complete" or removed.
4. The original spec 006's status field flips to "Implemented 2026-04-XX (Phase 1 + Phase 2 complete)" and the spec moves to `specs/done/`.
5. `CONSTITUTIONAL_CONVERSATIONS.md` does NOT need an entry — this is implementation work, not a constitutional amendment.

## 7. References

- `specs/006-inter-round-arbitration/spec.md` (the parent spec, Phase 1)
- `specs/006-inter-round-arbitration/IMPLEMENTATION-GAP.md` (the 7-point source)
- `engine/config.py`, `engine/phases.py`, `engine/output.py`, `engine/templates.py`, `linter/quality.py` (the shipped surfaces)
- `engine/tests/test_006_inter_round_arbitration.py` (the existing test surface)
- Spec 071 — Test-Fix Boundary Preservation (governs the test discipline for FR-P2-7)
