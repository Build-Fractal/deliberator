# Drift Report: 998-phase-consensus-gates

**Spec**: `specs/998-phase-consensus-gates/spec.md` (internally ID'd `006-phase-consensus-gates`)
**Date**: 2026-04-05
**Scope**: `engine/phases.py`, `engine/dispatch.py`, `engine/events.py`, `engine/cli/`, `engine/config.py`, `linter/`

---

## DONE (spec foundations satisfied by existing code)

**SC-007 / Implementation Notes §1 — Engine unchanged**: The spec requires gates to be an orchestration layer that does not modify the deliberation engine. The engine (`engine/phases.py:615–928`) has no gate logic. This separation precondition is satisfied.

**FR-007 partial — Dispute-parsing subsystem exists**: `linter/quality.py` exports `check_disagreement(text, mode) → DisagreementResult` (line 429) with a `.dispute_count` field (line 58). `engine/templates.py:546` provides `_extract_remaining_disputes()`. Both are already used by `engine/phases.py:758–761` for stagnation detection. The parsing substrate that FR-007 depends on is in place.

**FR-014/FR-015 partial — Exit-code infrastructure exists**: `engine/cli/context.py:56–95` defines a `"governance"` exit-code scheme (0=PASS, 1=BLOCK, 2=ERROR). The module already lists `"gate"` as a subcommand that selects this scheme (line 95), and the test at `engine/tests/test_cli_context.py:155–157` explicitly asserts `conversus gate review spec.md` activates governance exit codes. The exit-code mapping matches FR-015.

---

## MISSING (spec requirements with no code at all)

**FR-001 — `gates.yml` config format**: No `GateConfig`, `GatesConfig`, or schema for a `gates:` section anywhere in `engine/config.py` or the repo root. `parse_config()` (`engine/config.py:519`) does not parse a `gates:` key. No `gates.yml` example file exists.

**FR-002/FR-003/FR-004/FR-005 — Gate model fields**: No Pydantic model for a gate definition (phase name, agent config, pass criteria, mode, rounds, iterations, arbiter, output). The `EngineConfig` at `engine/config.py:75–90` has no `gates` field. Pass-criteria variants `converged`, `max_disputes N`, and `always` (FR-003) are undefined.

**FR-006 — Gate execution / `conversus.yml` generation**: No function that reads a gate config, synthesizes a `conversus.yml`, and invokes `run_pipeline`. The spec's "thin orchestration" step (Implementation Notes §1) does not exist.

**FR-007 partial — Gate pass/fail evaluation**: Although dispute parsing exists, there is no function that compares `dispute_count` against a gate's pass criterion and returns a structured pass/block result.

**FR-008/FR-009/FR-013 — Gate result reporting**: No `gate-result.md` writer. No formatted pass/block output (e.g., "Gate PASSED: spec — 0 disputes, 3 agents converged." from US-1 AC-2). No `FR-017` output file.

**FR-010 — Attempt history (`attempt-N/` directories)**: No logic that detects a prior gate output and renames it to `attempt-N/` before re-running. `OutputManager` (`engine/output.py`) has no `preserve_gate_attempt()` or equivalent.

**FR-011/FR-012 — `/conversus gate` CLI command**: The CLI (`engine/cli/__init__.py`) has subcommands `run`, `validate`, `decide`, `login`, `logout`, `status`, `context`, `init`. There is no `gate` subcommand registered with `@cli.command()`. Context detection anticipates `argv[1] == "gate"` (line 95) but the command itself does not exist.

**FR-016 — Automatic phase-boundary hooks for spec-driven workflows**: No integration hook, callback, or event that fires at a spec-kit/speckit phase boundary to auto-invoke a gate. The event system (`engine/events.py`) only defines `PhaseStarted`, `AgentDispatched`, `AgentCompleted`, `PhaseCompleted` — no `PhaseGatePassed` or `PhaseGateBlocked` events.

**SC-003/FR-010 — `attempt-N/` audit history**: Confirmed missing (same as FR-010 above).

**SC-004/FR-012 — `--inline` flag / ad-hoc gate without `gates.yml`**: No implementation.

---

## UNDOCUMENTED (codebase behaviour not mentioned in spec)

**Exit-code scheme pre-wired**: `engine/cli/context.py:94–96` lists `"gate"` in `_GOVERNANCE_SUBCOMMANDS` and the test at `test_cli_context.py:155–157` covers `conversus gate review spec.md`. This was implemented ahead of the `gate` command itself. The spec does not mention that this infrastructure was partially pre-built.

**`check_disagreement` used for multi-round stagnation, not gating**: `engine/phases.py:758` calls `check_disagreement(synthesis_text, config.mode)` inside the round loop to count disputes for stagnation detection. This repurposes the same linter function the spec says gates will use (FR-007). The spec treats dispute parsing as a gate concern; the codebase also uses it internally for round termination. No conflict, but worth noting for gate implementers.

**`linter/quality.py` CLI has exit code 2 for file-not-found**: `linter/quality.py:728` exits with code 2 on `FileNotFoundError`. The spec defines exit code 2 as "gate configuration error" (FR-015). These are different semantics for the same exit code — the linter's `__main__` is not the gate command, but if callers confuse them there is a semantic mismatch.

---

## DIVERGED (spec claims vs. actual design)

**`presets:` composition key vs. actual config key**: The spec (US-2 AC-4, FR-005) says gates support `agents.presets:` (plural) for preset composition. The existing `parse_config` resolves `preset:` as either a string (single) or a list (composed) under the same key — there is no separate `presets:` key (`engine/config.py:394–396`). A gate implementation that literally follows FR-005's `presets:` YAML key would diverge from the current preset resolution contract. **Spec line 81 vs. `engine/config.py:394`.**

**`pass: max_disputes N` as a YAML value**: FR-003 specifies the string `max_disputes N` (with N embedded) as a YAML scalar value. The existing config system has no parser for mixed-type scalars of this form. Implementing this literally would require a custom string parser, whereas the natural fit is `pass: {criterion: max_disputes, n: 1}`. The spec doesn't mention this parsing challenge.

**`output` default in spec vs. existing `OutputManager` layout**: FR-004 says gate output defaults to `{phase}-gate/`. The existing `OutputManager` (`engine/output.py`) uses `summary/final.md`, `round-N/`, `arbiter/resolution.md` path conventions. A gate writing to `{phase}-gate/` would introduce a new top-level layout not currently managed by `OutputManager`. The `attempt-N/` sub-path scheme (FR-010) has no parallel in the existing output manager.

---

## CONTRADICTIONS

**SC-007 says "no new engine features needed" vs. FR-016 requires phase-boundary hooks**: SC-007 (Implementation Notes §1) states "The engine does not know it is running a gate." FR-016 requires gates to "run automatically at configured phase boundaries without manual invocation." Automatic triggering at a phase boundary requires either: (a) changes to the pipeline (engine knows about gates), or (b) an external orchestrator that wraps pipeline invocations. The spec does not resolve which approach to use, creating an architectural ambiguity. The current event system emits `PhaseCompleted` events but no external consumer can intercept them to inject a gate call mid-workflow.

**`conversus gate --arbiter` (US-3 AC-3) vs. arbiter requiring `grounding`**: The spec's `--arbiter path/to/grounding.md` CLI flag (US-3 AC-3, FR-011) implies passing just the grounding path. But `ArbiterConfig` (`engine/config.py:60–70`) requires `name`, `prompt`, and `trigger` in addition to `grounding`. The gate command cannot construct a valid `ArbiterConfig` from only a grounding path, so either the arbiter for gates needs a separate, lighter model or the spec's CLI surface is incomplete.
