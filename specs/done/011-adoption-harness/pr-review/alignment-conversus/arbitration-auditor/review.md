# Arbitration Auditor Review: Engine vs Spec 006 (Inter-Round Arbitration)

## Executive Summary

The engine implementation has a **significant structural gap** with respect to spec 006 (Inter-Round Arbitration with Influence Control). The engine was built from an older version of SKILL.md and implements a simpler arbitration model that pre-dates the `timing` and `influence` fields. Specifically:

- **`arbiter.timing` is not parsed.** The `ArbiterConfig` model has no `timing` field. The engine hard-codes arbitration to fire only after the final round (the `timing: final` behavior), with no mechanism for inter-round arbitration.
- **`arbiter.influence` is not parsed.** The `ArbiterConfig` model has no `influence` field. The engine assumes all arbitration is binding. There is no influence-aware dispatch, template variable injection, or dispute counting.
- **Phase 6 does not fire between rounds.** The `run_pipeline` function in `engine/phases.py` places Phase 6 arbitration exclusively after the outer round loop completes. There is no inter-round arbitration insertion point in `_run_single_round`.
- **No `INFLUENCE_LEVEL` template variable is passed.** The `build_arbitration_context` function in `engine/templates.py` constructs an `ArbitrationContext` but never passes `INFLUENCE_LEVEL`. The linter model defines the field (with default `BINDING`), but the engine never sets it from config.
- **No `PRIOR_ARBITRATION_SECTION` variable is assembled.** The `build_review_context` function passes `PRIOR_ARBITRATION_PATH` (from the pipeline's round-awareness code) but never constructs the influence-aware `PRIOR_ARBITRATION_SECTION` conditional block that spec 006 FR-014 requires.
- **Dispute counting is not influence-aware.** Stagnation detection in `run_pipeline` uses raw dispute counts from `check_disagreement` with no adjustment for arbiter influence level.

The schema/linter layer (outside the engine) is fully spec-006-compliant: `linter/models.py` has `InfluenceLevel` enum, `ArbitrationContext.INFLUENCE_LEVEL`, `ReviewContext.PRIOR_ARBITRATION_SECTION`, and all templates reference `{INFLUENCE_LEVEL}` and `{PRIOR_ARBITRATION_SECTION}`. The gap is exclusively in the engine's config parsing, pipeline orchestration, and context construction.

---

## Alignment

### What the engine gets right

1. **Phase 6 conditional trigger logic is correct.** The engine correctly evaluates `arbiter.trigger` ("disputes_remain" or "always") and uses `_extract_remaining_disputes` to parse synthesis text for dispute content. The two-tier extraction (marker-based primary, heading-based fallback) matches SKILL.md's Dispute-Parsing Subsystem.

2. **`PRIOR_ARBITRATION_PATH` is threaded through rounds.** The `run_pipeline` round loop checks whether a prior-round arbitration file exists (`arb_path = output_mgr.get_arbitration_path(round_base=prior_base)`) and passes it to `_run_single_round` as `prior_arbitration_path`. All Phase 1-5 context builders accept and forward this parameter. This is the plumbing for FR-013.

3. **Multi-round orchestration is structurally sound.** The round loop, retroactive directory move, stagnation detection, cross-round synthesis, and round-aware output paths are all correctly implemented per spec 004. The inter-round arbitration gap is additive, not a structural conflict.

4. **Arbitration failure handling is correct.** Phase 6 failure is isolated: partial output is cleaned up, the pipeline does not abort, and the Phase 1-5 record remains valid. This matches SKILL.md's failure handling rules.

5. **Output directory layout matches spec 006 US-4.** The `OutputManager` produces `arbiter/resolution.md` paths at both round-level and top-level, matching the expected output structure. The `get_arbitration_path(round_base=...)` method supports per-round arbitration paths.

6. **Cross-round synthesis context has arbitration fields.** `build_cross_round_synthesis_context` accepts `arbitration_paths` and `arbitration_rulings` parameters, matching the `CrossRoundSynthesisContext` model. However, the caller in `run_pipeline` does not pass these values (see Missed Opportunities).

### What the engine gets wrong

1. **`ArbiterConfig` is missing `timing` and `influence` fields.** The model (config.py L45-53) only has `name`, `prompt`, `docs`, `grounding`, and `trigger`. SKILL.md lines 109-110 specify these as optional fields with defaults.

2. **`_resolve_arbiter` does not parse `timing` or `influence`.** The function (config.py L400-471) extracts `name`, `prompt`, `docs`, `grounding`, and `trigger` from the raw YAML but silently ignores `timing` and `influence` keys. No validation is performed (FR-001 through FR-004).

3. **No FR-003 validation.** When `timing: inter-round` and `rounds: 1`, the engine should reject with "arbiter.timing: inter-round requires rounds > 1." This check does not exist.

4. **Phase 6 is positioned only after the final round.** In `run_pipeline` (phases.py L768-849), arbitration runs after the outer round loop and cross-round synthesis. For `timing: inter-round`, Phase 6 should execute inside the round loop, after each round's Phase 5 and before the termination check (FR-005). The current code structure would need to move the arbitration block inside the `for round_num` loop with a conditional on `config.arbiter.timing`.

5. **`build_arbitration_context` does not pass `INFLUENCE_LEVEL`.** The function (templates.py L566-613) constructs `ArbitrationContext` without setting `INFLUENCE_LEVEL`. Because the Pydantic model defaults to `InfluenceLevel.BINDING`, arbitration templates always receive "binding" regardless of config. This means `{INFLUENCE_LEVEL}` in templates always expands to "binding" -- correct for the default case but wrong for `recommended` or `advisory`.

6. **`build_review_context` does not construct `PRIOR_ARBITRATION_SECTION`.** The function (templates.py L208-253) passes `PRIOR_ARBITRATION_PATH` but leaves `PRIOR_ARBITRATION_SECTION` at its default empty string. Spec 006 FR-014/FR-018 require this to expand to influence-aware language when prior-round arbitration exists. The engine has the path but not the conditional block.

7. **Stagnation detection is not influence-aware.** In `run_pipeline` (phases.py L691-711), `check_disagreement` returns a raw dispute count. For `influence: binding`, arbiter-addressed disputes should be subtracted. For `influence: advisory`, arbitration should not affect the count. The engine treats all dispute counts identically regardless of arbiter activity (FR-009 through FR-012).

8. **Cross-round synthesis omits arbitration context.** In `run_pipeline` (phases.py L714-763), `build_cross_round_synthesis_context` is called without `arbitration_paths` or `arbitration_rulings`. The function signature supports these parameters, but the caller passes neither. This means cross-round synthesis has no visibility into per-round arbitration output (FR-020).

---

## Missed Opportunities

1. **The engine's `EngineConfig` model could carry `timing` and `influence` without breaking any existing code.** Since both fields have defaults (`final` and `binding`) that match the engine's current hard-coded behavior, adding them is purely additive. No existing config would fail.

2. **The `_run_single_round` function is already the right extraction boundary for inter-round arbitration.** Phase 6 could be added at the end of `_run_single_round` (after Phase 5 synthesis) with a conditional check on `config.arbiter.timing == "inter-round"`. The round loop in `run_pipeline` would then only need to handle final arbitration. The architectural split between `_run_single_round` (phases 1-5) and `run_pipeline` (round loop + arbitration) is well-suited for this change.

3. **The `PRIOR_ARBITRATION_SECTION` assembly logic could live in `build_review_context`.** The function already receives `prior_arbitration_path`. Adding a conditional that checks whether the path points to an existing file and constructing the influence-aware block would be a localized change. The influence level would come from `config.arbiter.influence`.

4. **The `arbitration_paths` and `arbitration_rulings` parameters on `build_cross_round_synthesis_context` are already defined and unused.** The caller just needs to collect per-round arbitration paths and pass them. This is low-hanging fruit.

---

## Off-Base Assumptions

1. **The engine assumes a single arbitration point.** The `arbitration_ran` boolean on `PipelineResult` is a scalar flag. For inter-round arbitration, this should track per-round arbitration runs (e.g., a list or count). The current boolean cannot distinguish "arbitration ran once after final round" from "arbitration ran three times between rounds."

2. **The engine assumes all arbitration output headings are "Binding Decisions" and "Summary of Changes Required."** The heading validation in SKILL.md (lines 673-688) specifies influence-adjusted headings. If the engine were to add output validation (currently absent from the engine, present only in SKILL.md's spec), it would need influence-aware heading checks.

3. **The engine's `_extract_remaining_disputes` is used for both trigger evaluation and stagnation detection.** This is correct for the current model but insufficient for spec 006. Stagnation detection with influence-awareness requires knowing which disputes the arbiter addressed and subtracting them based on influence level. A simple dispute count from synthesis text is not enough -- the engine would also need to parse arbitration output to determine how many disputes were addressed.

---

## Actionable Recommendations

### P1 (Must-fix: blocks spec 006 correctness)

**R1. Add `timing` and `influence` fields to `ArbiterConfig` and parse them in `_resolve_arbiter`.**
- File: `<HOME>/code/payer-index-mono/conversus/engine/config.py`
- Add `timing: Literal["final", "inter-round"] = "final"` and `influence: Literal["binding", "recommended", "advisory"] = "binding"` to `ArbiterConfig`.
- In `_resolve_arbiter`, extract `raw.get("timing", "final")` and `raw.get("influence", "binding")`, validate their values, and pass them to the model constructor.
- Implement FR-003: reject `timing: inter-round` when `config.rounds <= 1`.

**R2. Implement inter-round arbitration in `run_pipeline`.**
- File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`
- After `_run_single_round` returns and before the stagnation/termination check, if `config.arbiter.timing == "inter-round"`, evaluate the trigger condition and dispatch Phase 6.
- Write output to `round_base/arbiter/resolution.md`.
- Pass the prior-round arbitration path to the next round's `_run_single_round` call.
- Keep the existing post-loop arbitration for `timing: final` and for cumulative final arbitration when `timing: inter-round` and disputes remain.

**R3. Pass `INFLUENCE_LEVEL` from config in `build_arbitration_context`.**
- File: `<HOME>/code/payer-index-mono/conversus/engine/templates.py`
- In `build_arbitration_context`, set `INFLUENCE_LEVEL=config.arbiter.influence` (mapping the string to `InfluenceLevel` enum) in the `ArbitrationContext` constructor.

**R4. Construct `PRIOR_ARBITRATION_SECTION` in `build_review_context`.**
- File: `<HOME>/code/payer-index-mono/conversus/engine/templates.py`
- When `prior_arbitration_path` is not None and points to an existing file, construct the influence-aware text block per FR-014 using `config.arbiter.influence`.
- Pass the assembled string as `PRIOR_ARBITRATION_SECTION` to the `ReviewContext` constructor.

### P2 (Should-fix: required for full spec 006 compliance)

**R5. Implement influence-aware dispute counting for stagnation detection.**
- File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`
- After inter-round arbitration runs, parse the arbitration output to count addressed disputes.
- For `binding`: subtract addressed disputes from the count before the stagnation check.
- For `recommended`: subtract addressed disputes (provisionally).
- For `advisory`: no adjustment.
- This requires a new helper function to parse arbitration output and count addressed disputes.

**R6. Pass `arbitration_paths` and `arbitration_rulings` to `build_cross_round_synthesis_context`.**
- File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`
- Collect per-round arbitration paths as the round loop executes.
- After the loop, pass the collected paths and formatted rulings text to the cross-round synthesis builder.

**R7. Change `PipelineResult.arbitration_ran` from `bool` to a richer type.**
- File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`
- Replace `arbitration_ran: bool = False` with a structure that can express per-round arbitration (e.g., `arbitration_rounds: list[int] = []` or `arbitration_count: int = 0`). Keep backward compatibility by retaining the boolean as a computed property.

### P3 (Nice-to-have: improves robustness)

**R8. Add integration test for `timing: inter-round` + `influence: advisory` scenario.**
- This is the most complex spec 006 combination: inter-round arbitration fires but does not affect dispute counts. The stagnation detector must ignore arbitration output. A test with a mock provider would catch regressions.

**R9. Add validation for influence-adjusted arbitration output headings.**
- Currently the engine does not validate Phase 6 output headings. SKILL.md lines 673-688 specify mode-specific required headings that change based on influence level. Adding a post-Phase-6 heading check (warning, not blocking) would catch malformed arbitration output.

**R10. Log a warning when `timing` or `influence` keys appear in a config but `ArbiterConfig` ignores them.**
- Until R1 is implemented, configs specifying `timing: inter-round` or `influence: advisory` silently fall back to `final`/`binding` behavior. A deprecation-style warning would alert users that these fields are not yet effective in the engine.

---

## Referenced Documentation

- **Spec 006**: `<HOME>/code/payer-index-mono/conversus/specs/done/006-inter-round-arbitration/spec.md` -- FR-001 through FR-023, SC-001 through SC-008.
- **SKILL.md**: `<HOME>/code/payer-index-mono/conversus/SKILL.md` -- Lines 99-111 (arbiter config schema), 218-222 (timing/influence validation), 346-366 (round loop with inter-round arbitration), 430-433 (PRIOR_ARBITRATION_SECTION expansion), 519-539 (inter-round arbitration subsection), 534-538 (influence-aware dispute counting), 656 (INFLUENCE_LEVEL template variable), 673-688 (influence-adjusted heading validation).
- **engine/config.py**: `<HOME>/code/payer-index-mono/conversus/engine/config.py` -- `ArbiterConfig` (L45-53), `_resolve_arbiter` (L400-471), `parse_config` (L478-642).
- **engine/phases.py**: `<HOME>/code/payer-index-mono/conversus/engine/phases.py` -- `_run_single_round` (L191-565), `run_pipeline` (L573-860), stagnation detection (L691-711), Phase 6 block (L768-849).
- **engine/templates.py**: `<HOME>/code/payer-index-mono/conversus/engine/templates.py` -- `build_review_context` (L208-253), `build_arbitration_context` (L566-613), `build_cross_round_synthesis_context` (L620-669).
- **engine/output.py**: `<HOME>/code/payer-index-mono/conversus/engine/output.py` -- `get_arbitration_path` (L257-264), round-aware path methods.
- **linter/models.py**: `InfluenceLevel` enum, `ArbitrationContext.INFLUENCE_LEVEL` (L361), `ReviewContext.PRIOR_ARBITRATION_SECTION` (L263).
- **Templates**: All four mode arbitration templates reference `{INFLUENCE_LEVEL}` (e.g., `templates/cooperative/arbitration.md` L11, L71-73). All four mode review templates reference `{PRIOR_ARBITRATION_SECTION}`.
