# Guided Workflow Auditor — Engine Alignment Review

**Reviewer**: guided-workflow-auditor
**Scope**: Specs 007-011 (guided workflow layer) vs engine implementation (engine/, mcp_server.py)
**Date**: 2026-03-24

---

## Executive Summary

The engine implementation (built from milestones M001-M005) is a Python-native reimplementation of SKILL.md's `/conversus run` pipeline. It handles Phases 1-6, multi-round execution, stagnation detection, cross-round synthesis, and arbitration. The guided workflow commands (`define`, `interests`, `mode`, `converge`, `arbitrate`, `gate`) specified in specs 007-011 execute entirely in the main conversation as SKILL.md handlers -- they never launch the Python engine directly.

The central finding: **the engine and the guided workflow are designed to be architecturally separate, and they currently are**. The engine handles the computational pipeline (`run_pipeline()`). The SKILL.md handlers handle conversational UX (prerequisite checks, user confirmation, plain-language reporting). The connection point is that `converge`, `arbitrate`, and `gate` eventually delegate to the same Phase 1-6 execution flow that `/conversus run` uses.

However, this delegation currently has no integration path. The engine provides `run_pipeline()`, `Deliberation.run()`, and MCP tools (`conversus_run`, `conversus_validate`, `conversus_decide`) -- but none of these accept the intermediate artifacts (`problem.md`, `interests.md`) or partial execution paths (Phase 6 only for `arbitrate`, config generation for `gate`) that the guided workflow handlers need. The engine is **UNAWARE** of the guided workflow, which is correct by design, but the delegation seam is missing.

---

## Alignment by Spec

### Spec 007 — Subcommand Dispatch & Define

**Classification: COMPATIBLE (engine is correctly uninvolved)**

Spec 007 adds the subcommand dispatch table to SKILL.md and the `/conversus define` handler. The define command produces `problem.md` entirely in the main conversation -- no engine invocation, no Python code.

The engine's entry points (`run_engine()` at `<HOME>/code/payer-index-mono/conversus/engine/run.py`, line 165; `Deliberation.run()` at `<HOME>/code/payer-index-mono/conversus/engine/sdk.py`, line 221) only handle `run` semantics. They do not interfere with other subcommands.

The dispatch table in SKILL.md (lines 22-44) lists seven subcommands. The engine has no subcommand routing at all -- it is invoked only when the SKILL.md handler for `run` (or `converge`/`arbitrate`/`gate`, which delegate to `run`) decides to call it. This is the correct separation.

**Evidence**: `run_engine()` takes a `config_path` and a `phase` parameter (`"all"` or `"review"`) at `engine/run.py:166-171`. There is no dispatch logic for `define`, `interests`, `mode`, `converge`, `arbitrate`, or `gate`.

### Spec 008 — Interests & Mode

**Classification: COMPATIBLE (engine is correctly uninvolved)**

Spec 008 adds `/conversus interests` and `/conversus mode`. Both execute in the main conversation. The interests handler reads `problem.md` and writes `interests.md`. The mode handler reads both artifacts and generates `conversus.yml`.

The engine is uninvolved. The output of `/conversus mode` is a standard `conversus.yml` that uses the exact schema the engine's `parse_config()` already validates (`engine/config.py`, line 478). The generated config contains `mode`, `target`, `output`, `agents` with `name`/`prompt`/`docs`, and optionally `role` -- all fields that `EngineConfig` at `engine/config.py:60-76` already handles.

**No conflicts.** The mode handler's YAML generation (SKILL.md lines 1256-1286) produces configs that pass `parse_config()` validation without modification.

### Spec 009 — Guided Execution (Converge)

**Classification: PARTIALLY IMPLEMENTED (delegation seam is incomplete)**

Spec 009 defines `/conversus converge` as a UX wrapper around `/conversus run`. The SKILL.md handler (lines 1329-1534) specifies:
- Pre-execution: parse config, present plain-language summary, get user confirmation
- Execution: "Proceed to Run: Execution Step 1 through Step 5 using the config already parsed" (SKILL.md line 1448)
- Post-execution: plain-language report with dispute detection and next-step routing

**The critical spec requirement** is FR-006 (spec 009): "Execution MUST delegate to the existing `/conversus run` engine. Zero new execution logic."

The engine provides this delegation capability through multiple paths:
1. `run_engine(config_path)` at `engine/run.py:165` -- takes a config path, returns written file paths
2. `Deliberation(config_path=path).run()` at `engine/sdk.py:221` -- returns a typed `Result`
3. `conversus_run(config_yaml, provider=...)` MCP tool at `mcp_server.py:493` -- in-process execution

However, the SKILL.md `converge` handler says (line 1448): "Do not re-invoke `/conversus run` as a separate skill -- continue within the current conversation." This means `converge` does not call the Python engine. It continues executing SKILL.md's own Phase 1-5 instructions (the `Run: Execution` section) within the same agent conversation. The Python engine is a parallel implementation, not the delegation target.

This creates a **dual-execution-path problem**: the SKILL.md `converge` handler runs the deliberation by orchestrating Agent tool calls per the SKILL.md instructions, while the Python engine runs the same pipeline through `run_pipeline()`. Both produce the same output structure, but they are independent code paths.

The engine's `run_pipeline()` at `engine/phases.py:573` could serve as the execution backend for `converge`, but there is no mechanism for a SKILL.md handler to invoke the Python engine. The SKILL.md handler uses `Agent` tool, `Read`, and `Write` -- not Python function calls. The MCP server (`mcp_server.py`) provides the bridge, but `conversus_run` requires a `config_yaml` string, not a pre-parsed config.

### Spec 010 — Guided Arbitration (Arbitrate)

**Classification: PARTIALLY IMPLEMENTED (Phase 6-only execution path missing)**

Spec 010 defines `/conversus arbitrate` as a guided on-ramp to Phase 6 arbitration. The SKILL.md handler (lines 1537-1878) specifies:
- Dispute detection via the Dispute-Parsing Subsystem
- Guided arbiter configuration (identity, grounding, influence)
- Config generation and `conversus.yml` modification
- Phase 6 execution delegation

**Step 5: Execution** (SKILL.md line 1819) says: "Execute Phase 6 using the existing engine defined in the Run: Execution section." This requires running ONLY Phase 6 -- not the full pipeline.

The engine's `run_pipeline()` at `engine/phases.py:573` always runs Phases 1-5 before Phase 6. There is no entry point for running Phase 6 alone. The engine provides `run_phase1()` at `engine/run.py:53` for single-phase execution, but only for the `review` phase. There is no `run_phase6()` or `run_arbitration()` function.

The `run_engine()` function at `engine/run.py:165` accepts `phase="all"` or `phase="review"` (line 238-260). Passing any other phase raises `ValueError`. Phase 6 cannot be invoked independently through the engine.

The `arbitrate` handler in SKILL.md works around this by running Phase 6 inline (same as the Run handler does) -- it loads the arbitration template, fills variables, and launches a single Agent. But this means the Python engine's Phase 6 implementation (with its error handling, event emission, output validation) is not used.

**Key gap**: The engine has complete Phase 6 logic at `engine/phases.py:769-849` (arbitration trigger evaluation, template loading, dispatch, failure handling, partial output cleanup) but no way to invoke it independently. The SKILL.md `arbitrate` handler must duplicate this logic.

**Spec 006 fields**: The `EngineConfig` model at `engine/config.py:60-76` does NOT include `timing` or `influence` fields specified by spec 006 and referenced in the SKILL.md config schema (lines 109-110). The `ArbiterConfig` at `engine/config.py:45-55` has `name`, `prompt`, `docs`, `grounding`, and `trigger` -- but no `timing` or `influence`. The `parse_config()` function at `engine/config.py:478` does not validate or parse these fields. This means the engine cannot execute inter-round arbitration or influence-aware arbitration as specified in spec 006 and used by the `arbitrate` handler.

### Spec 011 — Phase Consensus Gates

**Classification: UNAWARE (engine correctly independent, but delegation path needed)**

Spec 011 defines `/conversus gate` as a thin orchestration layer that generates a `conversus.yml` and delegates to the run engine. FR-012 (spec 011) explicitly states: "Gates MUST NOT modify the conversus engine."

The SKILL.md handler (lines 1881-2178) specifies:
- Gate configuration parsing (from `gates.yml` or `conversus.yml` `gates:` section)
- Config generation (standard `conversus.yml` from gate definition)
- Execution: "Proceed to Run: Execution Step 1 through Step 5 using the generated config" (SKILL.md line 1989)
- Post-execution: Dispute-Parsing Subsystem for pass/fail verdict, gate-result.md generation

The engine does not know about gates, which is correct per FR-012. The generated config is a standard `conversus.yml` that passes `parse_config()`.

However, the `gate` handler needs additional capabilities not exposed by the engine:
1. **Dispute count extraction**: The handler needs to parse synthesis output for dispute counts. The engine has `_extract_remaining_disputes()` at `engine/templates.py:531` and `check_disagreement()` from `linter.quality`, but neither is exposed as a public API.
2. **Exit codes**: The handler needs to communicate `0`/`1`/`2` exit codes. The engine's `PipelineResult` at `engine/phases.py:59-71` includes `termination_reason` and `arbitration_ran` but not a gate verdict.
3. **Re-run management**: The handler needs to move previous output to `attempt-N/` directories. The engine's `OutputManager` has no awareness of attempt tracking.

---

## Missed Opportunities

### 1. No SDK method for Phase 6-only execution

The `Deliberation` class at `engine/sdk.py:125` supports `config_path` mode and `question` mode, but not "run Phase 6 on existing output" mode. Adding a `Deliberation.arbitrate(output_dir=..., arbiter_config=...)` method would let the `arbitrate` SKILL.md handler delegate cleanly instead of reimplementing Phase 6 inline.

### 2. No dispute-parsing public API

The Dispute-Parsing Subsystem is described in SKILL.md (lines 750-778) and implemented in two places:
- `engine/templates.py:531-559` (`_extract_remaining_disputes()`) -- prefixed with `_` (private)
- `linter/quality.py` (`check_disagreement()`) -- imported by the engine

Neither is exposed as a stable public API for use by the `converge`, `arbitrate`, or `gate` handlers. The `gate` handler needs dispute counts, and the `converge` handler needs has-disputes boolean.

### 3. No MCP tool for gate execution

The MCP server at `mcp_server.py` exposes `conversus_validate`, `conversus_run`, and `conversus_decide`. There is no `conversus_gate` tool. CI/CD integration (spec 011, FR-008) would benefit from an MCP tool that accepts gate config and returns structured `DecideResult`-like output with exit code semantics.

### 4. Engine cost estimation not accessible to guided handlers

The `converge` handler needs to compute estimated agent launches (SKILL.md line 1420-1424). The engine has `engine.cost.estimate_cost()` used by the MCP server (`mcp_server.py:152-173`) and the SDK (`engine/sdk.py:107-117`), but the SKILL.md handlers cannot call Python functions. The cost formula is duplicated in SKILL.md (lines 318-320) rather than being available through an MCP tool.

### 5. EngineConfig missing spec 006 fields

The `EngineConfig` at `engine/config.py:60-76` and `ArbiterConfig` at `engine/config.py:45-55` do not include `timing` (default `final`, values `final`/`inter-round`) or `influence` (default `binding`, values `binding`/`recommended`/`advisory`) fields. These are specified in the SKILL.md config schema (lines 109-110) and validated in SKILL.md (lines 218-222). The engine silently ignores these fields during `parse_config()`.

---

## Off-Base Assumptions

### 1. Engine assumes it is the sole execution path

The engine's `run_pipeline()` at `engine/phases.py:573` is designed as a complete, self-contained pipeline. It creates output directories, runs all phases, writes files, and returns a result. It assumes no other code is simultaneously writing to the output directory or controlling phase execution.

But SKILL.md handlers run phases by launching Agent subagents -- they use the SKILL.md instructions directly, not the Python engine. The engine and SKILL.md are parallel implementations of the same pipeline. When SKILL.md's `converge` handler runs a deliberation, it does NOT call `run_pipeline()`. It orchestrates the same phases using Agent tool calls.

This is not a conflict today (both paths produce compatible output), but it means engine improvements (better error handling, streaming events, cost tracking) do not automatically benefit the SKILL.md execution path.

### 2. MCP server assumes YAML config as input

The MCP tools (`conversus_run`, `conversus_validate`) accept `config_yaml: str` as input. But the guided workflow handlers work with files on disk (`conversus.yml`, `problem.md`, `interests.md`). The `converge` handler reads `conversus.yml` from disk and uses it directly -- it does not serialize it to a string and pass it to an MCP tool.

This is correct for the SKILL.md execution model (SKILL.md handlers read files with the `Read` tool), but it means the MCP server cannot validate or execute a config that was just written by the `mode` handler without a separate file-read step.

### 3. Engine's ad-hoc mode assumes default presets

The `Deliberation(question=...)` ad-hoc mode at `engine/sdk.py:262-291` and `conversus_decide` MCP tool at `mcp_server.py:556-785` use `pragmatist + devils-advocate` presets hardcoded in `engine/adhoc.py`. The guided workflow has its own interest discovery (`/conversus interests`) that produces calibrated agents based on problem type. These are independent paths that could diverge.

---

## Actionable Recommendations

### P1 — Critical (blocks correct guided workflow execution)

**R1. Add `timing` and `influence` fields to `ArbiterConfig` and `EngineConfig`.**

File: `<HOME>/code/payer-index-mono/conversus/engine/config.py`, lines 45-55 and 60-76.

The SKILL.md config schema (SKILL.md lines 109-110) defines `arbiter.timing` (values: `final`/`inter-round`, default `final`) and `arbiter.influence` (values: `binding`/`recommended`/`advisory`, default `binding`). The `parse_config()` function must validate these fields and include them in `ArbiterConfig`. Without these, the engine cannot execute inter-round arbitration (spec 006) or influence-aware Phase 6 output (heading adjustments per influence level). Currently, `parse_config()` at line 478 silently drops these fields.

**R2. Add inter-round arbitration to `run_pipeline()`.**

File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`, lines 632-710 (round loop).

The round loop at line 633 runs Phases 1-5 per round, then checks termination. SKILL.md specifies (lines 519-540) that when `arbiter.timing: inter-round`, Phase 6 fires after each round's Phase 5 synthesis AND before the termination check. The engine's round loop has no inter-round arbitration insertion point. Influence-aware dispute counting (SKILL.md lines 534-538) is also missing: `binding` arbitration reduces the dispute count for termination, `advisory` does not.

**R3. Expose a Phase 6-only execution entry point.**

File: `<HOME>/code/payer-index-mono/conversus/engine/run.py`, lines 165-261.

The `run_engine()` function only supports `phase="all"` or `phase="review"`. The `/conversus arbitrate` handler needs to run Phase 6 on existing output without re-running Phases 1-5. Add `phase="arbitration"` support that loads the existing synthesis, evaluates the trigger, and dispatches the arbiter agent. This could also be exposed as `Deliberation.arbitrate()` on the SDK class.

### P2 — High (enables proper delegation from guided handlers to engine)

**R4. Expose dispute-parsing as a public API.**

File: `<HOME>/code/payer-index-mono/conversus/engine/templates.py`, line 531 (`_extract_remaining_disputes`).

Rename to `extract_remaining_disputes()` (drop the underscore prefix) and export from `engine/__init__.py`. The `converge`, `arbitrate`, and `gate` SKILL.md handlers all need dispute counting. Alternatively, expose this through an MCP tool (`conversus_disputes(synthesis_path, mode)`) so SKILL.md handlers can access it.

**R5. Add a `conversus_gate` MCP tool.**

File: `<HOME>/code/payer-index-mono/conversus/mcp_server.py`.

Spec 011 requires CI/CD integration with machine-readable exit codes. An MCP tool that accepts gate config (phase name, artifact path, pass criteria, agent preset), generates a temporary `conversus.yml`, runs the pipeline, parses disputes, and returns `{verdict, dispute_count, exit_code}` would enable programmatic gate execution. The tool should follow the same pure-function-then-MCP-wrapper pattern as `_decide()` / `conversus_decide()`.

**R6. Add `conversus_cost` MCP tool or resource.**

File: `<HOME>/code/payer-index-mono/conversus/mcp_server.py`.

The `converge` handler needs the agent launch estimate (SKILL.md line 1420-1424). The formula is currently duplicated in SKILL.md and in `engine.cost.estimate_cost()`. Exposing a `conversus_cost(agent_count, iterations, rounds, has_arbiter)` MCP tool would let SKILL.md handlers compute costs without duplicating the formula. The `conversus_validate` tool already returns cost estimates, but it requires a full YAML config string.

### P3 — Medium (correctness and consistency improvements)

**R7. Align `VALID_MODES` with SKILL.md.**

File: `<HOME>/code/payer-index-mono/conversus/engine/config.py`, line 82.

`VALID_MODES = ("cooperative", "winner-take-all", "prisoners-dilemma", "red-blue")` matches SKILL.md line 62. This is currently aligned. Maintaining this as a single source of truth (e.g., defined in a shared constants module imported by both engine and linter) would prevent drift.

**R8. Add `PRIOR_ARBITRATION_PATH` template variable support to all phase context builders.**

File: `<HOME>/code/payer-index-mono/conversus/engine/templates.py`, lines 208-253 (and other context builders).

The context builders (`build_review_context`, `build_cross_review_context`, etc.) accept `prior_arbitration_path` as a keyword argument and pass it to the context models. However, the context is only stored as a path -- the influence-aware context block expansion described in SKILL.md (lines 430-433) is not implemented in the engine. The engine stores the raw path; SKILL.md specifies expanding it into an influence-aware instruction block depending on `binding`/`recommended`/`advisory`. This requires `influence` to be available in the config (see R1).

**R9. Document the dual-execution-path architecture.**

There is no documentation explaining that SKILL.md handlers and the Python engine are parallel implementations of the same pipeline. The SKILL.md handlers orchestrate phases via Agent tool calls. The Python engine orchestrates phases via `asyncio` and `ModelProvider`. Both produce the same output structure. Future contributors need to understand that changes to the pipeline logic must be made in both places, or a unification path must be chosen.

**R10. Add `influence`-aware heading validation to engine Phase 6.**

File: `<HOME>/code/payer-index-mono/conversus/engine/phases.py`, lines 769-849.

SKILL.md (lines 682-688) specifies that Phase 6 output validation must use influence-adjusted headings: `recommended` changes "Binding Decisions" to "Recommended Resolutions", `advisory` changes it to "Advisory Opinions". The engine's Phase 6 implementation at `phases.py:769` does not perform output heading validation at all -- it writes the arbiter's response and emits events, but does not check for required section headings. This validation is specified in SKILL.md lines 671-688 and should be implemented in the engine for parity.

---

## Referenced Documentation

| Document | Path | Relevance |
|---|---|---|
| Alignment check brief | `<HOME>/code/payer-index-mono/conversus/specs/011-adoption-harness/pr-review/alignment-check.md` | Defines the review scope and key questions |
| SKILL.md | `<HOME>/code/payer-index-mono/conversus/SKILL.md` | Authoritative specification for all subcommands and execution flow |
| Engine __init__.py | `<HOME>/code/payer-index-mono/conversus/engine/__init__.py` | Public API surface: `Deliberation`, `Result`, `validate` |
| Engine config.py | `<HOME>/code/payer-index-mono/conversus/engine/config.py` | `EngineConfig`, `ArbiterConfig`, `parse_config()` -- missing `timing`/`influence` |
| Engine phases.py | `<HOME>/code/payer-index-mono/conversus/engine/phases.py` | `run_pipeline()` -- no inter-round arbitration, no Phase 6-only path |
| Engine dispatch.py | `<HOME>/code/payer-index-mono/conversus/engine/dispatch.py` | Concurrent agent dispatch -- no conflicts |
| Engine templates.py | `<HOME>/code/payer-index-mono/conversus/engine/templates.py` | Context builders, `_extract_remaining_disputes()` (private) |
| Engine events.py | `<HOME>/code/payer-index-mono/conversus/engine/events.py` | Event models -- no conflicts |
| Engine output.py | `<HOME>/code/payer-index-mono/conversus/engine/output.py` | `OutputManager` -- no gate/attempt awareness |
| Engine sdk.py | `<HOME>/code/payer-index-mono/conversus/engine/sdk.py` | `Deliberation` class -- no `arbitrate()` or gate support |
| Engine auth.py | `<HOME>/code/payer-index-mono/conversus/engine/auth.py` | OAuth/credential management -- no conflicts |
| Engine run.py | `<HOME>/code/payer-index-mono/conversus/engine/run.py` | `run_engine()` -- only `"all"` and `"review"` phases |
| MCP server | `<HOME>/code/payer-index-mono/conversus/mcp_server.py` | `conversus_validate`, `conversus_run`, `conversus_decide` -- no gate/arbitrate tools |
| Spec 007 | `<HOME>/code/payer-index-mono/conversus/specs/done/007-subcommand-dispatch-define/spec.md` | Subcommand dispatch, `/conversus define` |
| Spec 008 | `<HOME>/code/payer-index-mono/conversus/specs/done/008-interests-mode/spec.md` | `/conversus interests`, `/conversus mode` |
| Spec 009 | `<HOME>/code/payer-index-mono/conversus/specs/done/009-guided-execution/spec.md` | `/conversus converge` -- UX wrapper around run |
| Spec 010 | `<HOME>/code/payer-index-mono/conversus/specs/done/010-guided-arbitration/spec.md` | `/conversus arbitrate` -- guided Phase 6 |
| Spec 010 dispatch additions | `<HOME>/code/payer-index-mono/conversus/specs/done/010-guided-arbitration/dispatch-additions.md` | Dispatch table changes for arbitrate |
| Spec 010 handler draft | `<HOME>/code/payer-index-mono/conversus/specs/done/010-guided-arbitration/handler-draft.md` | Full arbitrate handler specification |
| Spec 011 | `<HOME>/code/payer-index-mono/conversus/specs/done/011-phase-consensus-gates/spec.md` | `/conversus gate` -- CI/CD quality gates |
