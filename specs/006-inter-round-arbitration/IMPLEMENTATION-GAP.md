# Spec 006 Implementation Gap — Inter-Round Arbitration

**Status**: Spec is marked done but the engine execution model was never wired.
**Discovered**: 2026-04-03 during spec 045 coverage push (dead code investigation
at `engine/phases.py:661`).

## What shipped

Spec 005 pre-provisioned the schema side of inter-round arbitration:

- `schema/variables.yml` defines `PRIOR_ARBITRATION_PATH`,
  `PRIOR_ARBITRATION_SECTION`, `ARBITRATION_PATHS`, `ARBITRATION_RULINGS`,
  and `INFLUENCE_LEVEL`.
- `linter/models.py` exposes `PRIOR_ARBITRATION_PATH` on the per-phase
  context models.
- `engine/templates.py` accepts `prior_arbitration_path` on
  `build_review_context` (and the rest of the Phase 1–5 builders) and
  plumbs it through to template filling.
- `engine/phases.py::_run_single_round` accepts `prior_arbitration_path`
  as a keyword argument and forwards it to the context builders.

## What did NOT ship

The **execution model** (Spec 006 §3 "Execution Model", FR-005 through
FR-008) was never implemented:

1. `ArbiterConfig` (`engine/config.py:47`) has no `timing` or `influence`
   fields. The parser in `_resolve_arbiter` does not accept either key.
2. The round loop in `run_pipeline` (`engine/phases.py` ~line 632) never
   invokes Phase 6 between rounds. Arbitration dispatch happens exactly
   once, AFTER the loop terminates, writing to either the last round's
   `round-{N}/arbiter/resolution.md` (multi-round) or
   `{root}/arbiter/resolution.md` (single-round).
3. Because Phase 6 never runs mid-loop, there is never a file at
   `round-{N-1}/arbiter/resolution.md` when Round N begins, and
   `prior_arbitration_path` is always `None` for Round N > 1. Spec 005's
   schema plumbing is load-bearing for template variable resolution but
   no caller ever populates it.
4. Influence-aware dispute counting (FR-009 through FR-012), influence-
   aware template language (FR-014), and Resolution Attribution in the
   cross-round synthesis (FR-020) are not implemented.

## Evidence of the gap

- Dead code at `engine/phases.py:659-661` (removed on 2026-04-03) tried
  to read `get_round_base(N-1) / "arbiter" / "resolution.md"`. The check
  was unreachable because (a) `retroactive_move_to_round_1()` moves the
  flat `{root}/arbiter/` directory into `{root}/round-1/arbiter/` before
  Round 2 context is built, so `get_round_base(1) / "arbiter" / ...`
  never exists during Round 2, and (b) no per-round Phase 6 ever writes
  to `{root}/round-N/arbiter/resolution.md` for N ≥ 2 because the loop
  does not run Phase 6 at all.
- `tests/test_engine_phases.py::TestRetroactiveMovePreservesArbiterDir`
  only verifies the retroactive move preserves pre-seeded content — it
  does not and cannot exercise the inter-round pickup flow.
- Spec 045 final synthesis
  (`specs/045-test-coverage-review/conversus-output/summary/final.md`
  line 168) flagged this as "documented dead code" with "Phase B
  decision: delete the branch."

## What fixing it properly requires

A follow-up spec (tentatively 047 or later) to finish spec 006's Phase 2
("Execution Model"):

1. **Config schema**: add `timing: Literal["final", "inter-round"] = "final"`
   and `influence: Literal["binding", "recommended", "advisory"] = "binding"`
   to `ArbiterConfig`. Update `_resolve_arbiter` to parse both fields.
   Add validation: `timing=inter-round` with `rounds=1` is rejected.
2. **Output paths**: change Phase 6 writes from `{base}/arbiter/resolution.md`
   to `{base}/arbitration/resolution.md` to match spec 006 §2 US-4 and
   FR-006. Update `OutputManager.get_arbitration_path`, the retroactive
   move, and every test that asserts on the current `arbiter/` path.
3. **Execution model**: factor the Phase 6 dispatch block in
   `run_pipeline` out into a helper that `_run_single_round` (or the
   round loop body) can invoke conditionally when `timing=inter-round`.
   Write the result to `{round_base}/arbitration/resolution.md`. Populate
   `prior_arbitration_path` for Round N+1 when Round N's arbitration
   fired.
4. **Influence-aware dispute counting**: extend `check_disagreement`
   (or add a wrapper) to subtract arbiter-addressed disputes from the
   active count when `influence=binding` or `recommended`, and support
   re-opening on `recommended` per FR-012.
5. **Template language**: populate `PRIOR_ARBITRATION_SECTION` and
   `INFLUENCE_LEVEL` in the context builders based on
   `config.arbiter.influence`. Add influence-aware headings to
   `templates/{mode}/arbitration.md` per FR-023.
6. **Cross-round synthesis**: add Resolution Attribution section
   per FR-020. Populate `ARBITRATION_PATHS` / `ARBITRATION_RULINGS` from
   the accumulated per-round arbitration files.
7. **Tests**: cover all four `timing × influence` combinations per
   SC-001 through SC-008.

The scope is Medium effort (estimated 2–4 days). It is NOT a bug fix —
it is the second half of an already-shipped design.

## Interim state

As of 2026-04-03 the engine behaves as spec 001 + spec 004 intended:
single final arbitration after the round loop, always "binding" in tone.
The dead `prior_arbitration_path` branch has been removed from
`engine/phases.py` and a comment explains why the variable stays `None`.
No config files in the repo use `arbiter.timing` or `arbiter.influence`
(the parser would reject unknown keys in strict mode anyway — see
`_resolve_arbiter`).
