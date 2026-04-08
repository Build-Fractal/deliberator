# Feature Specification: Guided Execution

**Feature ID**: `009-guided-execution`
**Created**: 2026-03-21
**Status**: Draft
**Depends On**: `008-interests-mode` (generates conversus.yml), existing SKILL.md `run` engine
**Origin**: Decomposed from original 003-decision-framework, Phase B

---

## 1. Feature Summary

`/conversus converge` is a guided on-ramp to `/conversus run`. It presents a human-readable summary of the config, asks the user to confirm before spending tokens, executes the deliberation via the existing engine, and provides a plain-language summary of results with suggested next steps.

This command bridges the gap between non-experts (who used `define` → `interests` → `mode` to generate a config) and the execution engine. It adds no new execution logic — it wraps `run` with pre-flight confirmation and post-flight interpretation.

**What changes**: New `/conversus converge` subcommand handler in SKILL.md. Pre-execution summary. Post-execution plain-language report.

**What does not change**: Execution engine. Phase 1-6 behavior. Output format. Template system.

---

## 2. Functional Requirements

### Pre-Execution

- **FR-001**: `/conversus converge` MUST read `conversus.yml` and present a human-readable summary: the mode (plain-language explanation, not just the YAML value), agents (names and one-line perspectives), target documents, and estimated agent launches.
- **FR-002**: The user MUST confirm before execution begins. No silent execution.
- **FR-003**: If the user declines, the system MUST route them to the appropriate prior step: `/conversus interests` to modify agents, `/conversus mode` to change the mode.

### Missing Prerequisites

- **FR-004**: If no `conversus.yml` exists, check for `problem.md` and `interests.md`. If both exist, run mode selection first. If neither exists, start from `/conversus define`.
- **FR-005**: If `conversus.yml` exists but is stale (interests.md modified more recently), warn the user and suggest re-running `/conversus mode`.

### Execution

- **FR-006**: Execution MUST delegate to the existing `/conversus run` engine. Zero new execution logic. `converge` is routing + UX, not a new engine.
- **FR-007**: Multi-round execution (spec 002), arbitration (spec 001), and inter-round arbitration (spec 006) work transparently — `converge` passes through whatever the config specifies.

### Post-Execution

- **FR-008**: The completion report MUST include: what the mode means for interpreting the results, the path to `summary/final.md`, and suggested next steps based on outcome.
- **FR-009**: If disputes remain, suggest `/conversus arbitrate`.
- **FR-010**: If all disputes converged, note that arbitration is not needed.

---

## 3. Success Criteria

- **SC-001**: A non-expert who used `define` → `interests` → `mode` can execute a deliberation without editing YAML and without understanding the engine internals.
- **SC-002**: Output from `/conversus converge` is identical to `/conversus run` with the same config — `converge` is pure UX wrapper.
- **SC-003**: Missing prerequisites route the user to the correct prior step, not an error.
- **SC-004**: The pre-execution summary is plain language: "4 agents, cooperative mode, 1 round, estimated 21 agent launches. Proceed?" — not a YAML dump.

---

## 4. Constraints

- **Must NOT add execution logic.** `converge` = guided wrapper around `run`. If it needs engine changes, those belong in a different spec.
- **Must NOT require prior guided workflow steps.** `/conversus converge` works with a hand-crafted `conversus.yml` — it's just a nicer way to review and launch.
