# Spec Compliance Audit: Engine Implementation vs SKILL.md (Post-Merge)

**Reviewer**: spec-compliance-auditor
**Scope**: Engine implementation (engine/) and MCP server (mcp_server.py) alignment with merged SKILL.md containing specs 006-013
**Date**: 2026-03-24

---

## Executive Summary

The engine is a faithful extraction of SKILL.md as it existed before specs 006-013 landed. After the merge, SKILL.md has evolved significantly -- it now includes subcommand dispatch (spec 007), guided workflow handlers (specs 008-010), phase consensus gates (spec 011), inter-round arbitration fields (spec 006), and references to schema packages (specs 012-013). The engine handles the core run pipeline (phases 1-6, multi-round, presets, arbitration) correctly against SKILL.md's `Run: Execution` section. However, there are two categories of concrete incompatibility that would cause runtime failures:

1. **Missing `INFLUENCE_LEVEL` in `build_arbitration_context`**: The `ArbitrationContext` Pydantic model in `linter/models.py` declares `INFLUENCE_LEVEL: InfluenceLevel` as a field (defaulting to `binding`). All four arbitration templates reference `{INFLUENCE_LEVEL}`. The engine's `build_arbitration_context()` in `templates.py` never sets this field -- it relies on the Pydantic default. This is not a crash (the default works), but it means the engine cannot produce `recommended` or `advisory` arbitration output because `EngineConfig` / `ArbiterConfig` lacks `timing` and `influence` fields entirely.

2. **Missing `PRIOR_ARBITRATION_SECTION` population**: The `ReviewContext` model declares `PRIOR_ARBITRATION_SECTION: str = ""` and all four review templates include `{PRIOR_ARBITRATION_SECTION}`. The engine's `build_review_context()` never populates this field -- it always leaves it as empty string. This means inter-round arbitration context (spec 006) is never injected into review prompts for round 2+, even when prior arbitration exists.

3. **Arbiter output directory name divergence**: SKILL.md specifies `arbitration/resolution.md` as the output path. The engine uses `arbiter/resolution.md`. This is a path mismatch that would cause any SKILL.md-based workflow (including `/conversus arbitrate`) to look in the wrong directory.

---

## Alignment

### Areas of Strong Alignment

**Config parsing (config.py vs SKILL.md Step 1)**: The engine's `parse_config()` correctly implements preset resolution (single, composed up to 3, with composition templates matching SKILL.md verbatim), target/prior file resolution, agent name validation regex, mode validation, arbiter validation (name, prompt, grounding, trigger, docs), rounds/stagnation validation, and the rounds 1-5 range with the helpful message for rounds >= 6. This is a high-fidelity extraction.

**Template loading (templates.py vs SKILL.md Step 3)**: `load_template()` correctly resolves templates from `templates/{mode}/{phase}.md`, rejects draft-marked templates via the `CONVERSUS:TEMPLATE_STATUS: draft` marker, and the `find_templates_dir()` search strategy (walk up from config, then engine root, then cwd) matches SKILL.md's resolution rules.

**Template filling (templates.py vs SKILL.md variable contract)**: `fill_template()` correctly substitutes `{VARIABLE}` placeholders from Pydantic context models, serializes PathList to newline-separated bare paths (matching SKILL.md's "one bare absolute path per line" rule), and validates that no unfilled variables remain.

**Pipeline orchestration (phases.py vs SKILL.md Step 4)**: `run_pipeline()` correctly implements the outer round loop, single-round helper, iteration loop (Phase 2/3 cycling), round-aware output paths, stagnation detection, cross-round synthesis, and Phase 6 conditional arbitration. The termination conditions (converged, stagnation, max_rounds) match SKILL.md exactly.

**Dispute parsing (templates.py vs SKILL.md Dispute-Parsing Subsystem)**: `_extract_remaining_disputes()` implements the two-tier extraction (marker-based primary, heading-based fallback) with the correct mode-specific headings: cooperative `### Remaining Disputes`, winner-take-all `## Runner-Up`, red-blue `### Disputed Risks`, prisoners-dilemma `## Disputed Boundaries`. The default-to-triggered behavior (return empty string only when markers/headings are absent, then the caller treats non-empty as "has disputes") aligns with SKILL.md's safety measure.

**Output directory layout (output.py vs SKILL.md Step 2)**: The flat layout, retroactive move to `round-1/`, round directory creation, and cross-round synthesis path at root `summary/final.md` all match SKILL.md's specified structure.

**Event system (events.py vs SKILL.md reporting)**: The event models (PhaseStarted, AgentDispatched, AgentCompleted, PhaseCompleted) map to the lifecycle events SKILL.md describes. The engine's streaming capability via `AsyncQueueEmitter` supports FR-010 (streaming phase-lifecycle events).

**SDK (sdk.py vs spec 011 FR-005)**: The `Deliberation` class, `Result` model, `validate()` function, and `classify()` function implement the spec's SDK requirements. The ad-hoc question mode with auto-generated config using pragmatist + devils-advocate presets matches the "Just Ask" pipeline concept.

**MCP server (mcp_server.py vs spec 011 FR-013/014/015)**: Three tools (`conversus_validate`, `conversus_run`, `conversus_decide`) with defined input/output schemas, the quality gate in `conversus_decide` (question classifier, cost safeguard), and the hybrid execution model (validate-only, parsed-output, in-process) are well-aligned.

---

## Missed Opportunities

1. **No `timing` / `influence` fields in `ArbiterConfig`**: The engine's `ArbiterConfig` has `trigger: Literal["disputes_remain", "always"]` but lacks `timing` and `influence`. SKILL.md now specifies these fields with full validation rules (timing: final|inter-round, influence: binding|recommended|advisory). The `linter/models.py` already defines `InfluenceLevel` and `ArbiterTiming` enums, and the schema (`schema/variables.yml`) already declares `INFLUENCE_LEVEL` and `PRIOR_ARBITRATION_SECTION` as valid variables. The engine is the only component that has not adopted them.

2. **No inter-round arbitration in the pipeline**: SKILL.md's Step 4 specifies inter-round arbitration (Phase 6 fires after each round's Phase 5 when `arbiter.timing: inter-round`). The engine's `run_pipeline()` only runs arbitration after the final round. The influence-aware dispute counting for termination (binding subtracts addressed disputes, advisory does not adjust) is entirely absent.

3. **No guided workflow command awareness**: The engine only handles `run`. SKILL.md now has 7 subcommands (run, define, interests, mode, converge, arbitrate, gate). The MCP server and SDK do not expose tools for these guided workflow commands. This is by design for now (the guided workflow runs in-conversation via SKILL.md, not via the engine), but it means the engine cannot serve as a backend for the full `/conversus` command surface.

4. **No schema package integration**: Specs 012 (game form schemas) and 013 (objective function templates) define a `conversus/schemas/` package with Pydantic models. This package does not exist on disk yet. The engine has no integration points for it, which is correct since both specs are "Not started" per STATUS.md.

5. **`PRIOR_ROUND_SECTION` always empty string**: The engine's `build_review_context()` always sets `PRIOR_ROUND_SECTION=""`. SKILL.md specifies that for round 2+, this should expand to a block including the prior synthesis path and instructions about engaging with prior-round synthesis. The engine passes `PRIOR_SYNTHESIS_PATH` and `PRIOR_ROUND_DIR` as separate fields but never composes the `PRIOR_ROUND_SECTION` conditional block. The templates may reference `{PRIOR_ROUND_SECTION}` and get empty string even when prior-round context exists.

---

## Off-Base Assumptions

1. **The engine does not assume `schemas/` exists**: This is correct -- specs 012 and 013 are "Not started" and the engine has no import dependency on a schemas package. No off-base assumption here.

2. **The engine assumes `arbiter/` not `arbitration/` for output paths**: The engine's `OutputManager.get_arbitration_path()` returns `{base}/arbiter/resolution.md` and creates `arbiter/` directories. SKILL.md consistently uses `arbitration/` (e.g., `{output}/arbitration/resolution.md`). This naming mismatch would cause any tool reading SKILL.md-specified paths to miss the engine's output. The `/conversus arbitrate` handler, which reads from `{output}/arbitration/resolution.md`, would fail to find engine-produced arbitration output.

3. **STATUS.md references in engine/tests**: The engine tests do not reference `STATUS.md` or any spec paths in `done/`. The move of specs to `done/` has no impact on the engine's runtime behavior. No off-base assumption here.

4. **The engine assumes `EngineConfig` is the complete config surface**: The engine parses all fields from `conversus.yml` that it knows about and ignores unknown fields (standard YAML parsing). However, if a config includes `timing: inter-round` or `influence: advisory`, these are silently ignored -- no error, no warning. A user who writes a config with these fields (per SKILL.md documentation) will get `timing: final` and `influence: binding` behavior with no indication that their settings were discarded.

---

## Actionable Recommendations

### P1 -- Runtime Failure or Silent Incorrectness

**R01. Add `timing` and `influence` fields to `ArbiterConfig` in `engine/config.py`**

The SKILL.md config schema now includes `timing` (default: `final`, values: `final | inter-round`) and `influence` (default: `binding`, values: `binding | recommended | advisory`). Add these fields with defaults matching SKILL.md. Add the inter-round / rounds > 1 cross-validation rule: "arbiter.timing: inter-round requires rounds > 1."

File: `<HOME>/code/payer-index-mono/conversus/engine/config.py`, class `ArbiterConfig`

**R02. Pass `INFLUENCE_LEVEL` in `build_arbitration_context()`**

The `ArbitrationContext` model already has `INFLUENCE_LEVEL: InfluenceLevel` with a default of `binding`. The engine must read the influence from the parsed config and pass it explicitly. Currently, the arbitration templates receive `{INFLUENCE_LEVEL}` = `binding` regardless of config. After R01, read `config.arbiter.influence` and pass it as `INFLUENCE_LEVEL=InfluenceLevel(config.arbiter.influence)`.

File: `<HOME>/code/payer-index-mono/conversus/engine/templates.py`, function `build_arbitration_context()`

**R03. Fix arbiter output directory name: `arbiter/` to `arbitration/`**

SKILL.md uses `arbitration/` everywhere. The engine uses `arbiter/`. This causes a path mismatch for any consumer of the output (including `/conversus arbitrate` and any tests that check output paths against SKILL.md conventions). Rename `arbiter/` to `arbitration/` in `OutputManager` methods: `create_phase1_dirs()`, `get_arbitration_path()`, `_FLAT_LAYOUT_DIRS`, and the directory layout docstring.

File: `<HOME>/code/payer-index-mono/conversus/engine/output.py`

**R04. Populate `PRIOR_ARBITRATION_SECTION` in review context builders**

All four review templates include `{PRIOR_ARBITRATION_SECTION}`. The engine always leaves this empty. For round 2+ when prior arbitration exists, the engine should compose the influence-aware block per SKILL.md: binding = "arbiter has issued binding rulings... MUST treat as settled", recommended = "should adopt unless counter-evidence", advisory = "consider their reasoning... not bound". This requires R01 (influence field on config).

File: `<HOME>/code/payer-index-mono/conversus/engine/templates.py`, function `build_review_context()`

**R05. Populate `PRIOR_ROUND_SECTION` in review context builders**

The engine always sets `PRIOR_ROUND_SECTION=""`. For round 2+, SKILL.md specifies this should expand to a block including the prior synthesis path and engagement instructions. The engine passes `PRIOR_SYNTHESIS_PATH` separately, but if templates reference `{PRIOR_ROUND_SECTION}` as a composite block, they get nothing.

File: `<HOME>/code/payer-index-mono/conversus/engine/templates.py`, function `build_review_context()`

### P2 -- Functional Gaps (Not Crashes, But Missing Behavior)

**R06. Implement inter-round arbitration in `run_pipeline()`**

SKILL.md specifies that when `arbiter.timing: inter-round`, Phase 6 fires after each round's Phase 5 (before the termination check). The engine only runs arbitration after the final round. After R01 adds the timing field, add conditional inter-round arbitration dispatch inside the round loop, between the single-round result and the stagnation/convergence check. This is a significant feature addition.

File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`, function `run_pipeline()`

**R07. Implement influence-aware dispute counting for termination**

SKILL.md specifies that after inter-round arbitration: binding subtracts addressed disputes from the count, recommended subtracts provisionally, advisory does not adjust. The engine's termination check uses raw dispute count from `check_disagreement()` with no adjustment. This requires R06 first.

File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`, function `run_pipeline()`

**R08. Warn on unknown config fields (`timing`, `influence`)**

Until R01 is implemented, `parse_config()` silently ignores `timing` and `influence` fields in the arbiter section. Add a warning (not an error) when the raw YAML contains known SKILL.md fields that the engine does not yet support, so users know their config is not fully honored.

File: `<HOME>/code/payer-index-mono/conversus/engine/config.py`, function `parse_config()`

### P3 -- Documentation / Future-Proofing

**R09. Add engine integration notes for guided workflow commands**

The engine handles `run` only. Specs 007-011 added 6 new subcommands to SKILL.md. Document in the engine's module docstring or a README that these subcommands are SKILL.md-native (run in-conversation) and not yet engine-routed. This prevents future contributors from assuming the engine should handle `/conversus define` etc.

File: `<HOME>/code/payer-index-mono/conversus/engine/__init__.py`

**R10. Validate `PRIOR_ARBITRATION_SECTION` template references against engine population**

Add a test that verifies: for each template that references `{PRIOR_ARBITRATION_SECTION}`, the engine's context builder provides a non-empty value when prior arbitration exists (round 2+ with arbiter.timing: inter-round). Currently this would fail, confirming the gap. After R04, the test should pass.

File: New test in `<HOME>/code/payer-index-mono/conversus/engine/tests/`

---

## Referenced Documentation

- **SKILL.md** (merged, post-specs 006-013): `<HOME>/code/payer-index-mono/conversus/SKILL.md` -- the authoritative spec for engine behavior, including subcommand dispatch, guided workflow, inter-round arbitration, and phase consensus gates.
- **STATUS.md**: `<HOME>/code/payer-index-mono/conversus/specs/STATUS.md` -- spec 006 is "Not started" (inter-round arbitration), specs 007-011 are "Implementation-complete" (SKILL.md only), specs 012-013 are "Not started" (schema packages).
- **Engine config**: `<HOME>/code/payer-index-mono/conversus/engine/config.py` -- `ArbiterConfig` lacks `timing` and `influence` fields.
- **Engine templates**: `<HOME>/code/payer-index-mono/conversus/engine/templates.py` -- `build_arbitration_context()` does not pass `INFLUENCE_LEVEL`; `build_review_context()` does not populate `PRIOR_ARBITRATION_SECTION` or `PRIOR_ROUND_SECTION`.
- **Engine output**: `<HOME>/code/payer-index-mono/conversus/engine/output.py` -- uses `arbiter/` directory name vs SKILL.md's `arbitration/`.
- **Engine pipeline**: `<HOME>/code/payer-index-mono/conversus/engine/phases.py` -- no inter-round arbitration, no influence-aware dispute counting.
- **Linter models**: `<HOME>/code/payer-index-mono/conversus/linter/models.py` -- already declares `InfluenceLevel`, `ArbiterTiming` enums, and `INFLUENCE_LEVEL` field on `ArbitrationContext`.
- **Schema variables**: `<HOME>/code/payer-index-mono/conversus/schema/variables.yml` -- already declares `INFLUENCE_LEVEL` and `PRIOR_ARBITRATION_SECTION` as valid template variables.
- **Templates**: `<HOME>/code/payer-index-mono/conversus/templates/cooperative/arbitration.md` (and all other modes) -- reference `{INFLUENCE_LEVEL}`. Review templates reference `{PRIOR_ARBITRATION_SECTION}`.
- **Spec 011 (adoption harness)**: `<HOME>/code/payer-index-mono/conversus/specs/011-adoption-harness/spec.md` -- FR-005 (engine sub-phases), FR-027 (backward compatibility), FR-028 (power-user workflows).
- **Spec 011 alignment check**: `<HOME>/code/payer-index-mono/conversus/specs/011-adoption-harness/pr-review/alignment-check.md` -- the 7 key questions this review answers.
