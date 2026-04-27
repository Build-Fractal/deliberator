# Feature Specification: Phase-Completion Consensus Gates

**Feature ID**: `006-phase-consensus-gates`
**Created**: 2026-03-20
**Status**: Done — closed 2026-04-27 per spec hygiene audit. Folded into spec 011-phase-consensus-gates (now in `specs/done/`) with CI/CD-specific additions; the 998 numbering was a temporary reservation slot.
**Depends On**: `003-decision-framework` (guided workflow commands that trigger phase transitions), `004-preset-agents` (preset agents for gate deliberation)
**Input**: Automatically run a conversus deliberation at each phase boundary in a spec-driven workflow, using the phase's output as the deliberation target to validate quality and completeness before proceeding.

---

## 1. Feature Summary

Spec-driven development workflows (like speckit's specify -> plan -> tasks -> implement pipeline) proceed through discrete phases. Each phase produces an artifact: a spec, a plan, a task breakdown, an implementation. Currently, phase transitions are ungated — the output of one phase feeds directly into the next with no structured quality check. A developer might review the output manually, but there is no systematic mechanism to catch specification gaps, plan inconsistencies, or task decomposition errors before they propagate downstream.

This spec introduces **consensus gates**: automatic conversus deliberations that run at phase boundaries. When a phase completes, its output becomes the `target` of a conversus run. Multiple agents (drawn from presets or user configuration) deliberate on the output. If the deliberation converges (no remaining disputes), the gate passes and the workflow proceeds. If disputes remain, the gate blocks and the user must address them before continuing.

The key insight is that conversus already solves the hard problem — multi-agent adversarial review of a document. Phase gates are the integration point: they answer "when should conversus run?" rather than "how should it run?" The mechanism is a thin orchestration layer that connects phase transitions to conversus invocations.

**What changes**: A new `gates` section in `conversus.yml` (or a standalone `gates.yml`) defines which phases trigger deliberation, which agents review, and what the pass/fail criteria are. A new `/conversus gate` command evaluates a gate for a given phase artifact. Integration hooks allow spec-driven tools (speckit, etc.) to invoke gates automatically.

**What does not change**: Manual `/conversus run` is unaffected. The deliberation engine (Phases 1-6) is unchanged. Gate deliberations are standard conversus runs with auto-generated configs — no new engine features are needed.

---

## 2. User Stories

### US-1: Automatic Gate on Spec Completion

As a developer using a spec-driven workflow, I want the system to automatically run a multi-agent review when I complete a spec, so that specification gaps are caught before planning begins.

**Acceptance Criteria**:

1. **Given** a `gates.yml` with a `spec` phase gate configured with 3 review agents, **When** the spec artifact is marked complete (or `/conversus gate spec path/to/spec.md` is invoked), **Then** a conversus deliberation runs with the spec as target, the configured agents review it, and the gate reports pass (no disputes) or fail (disputes remain).

2. **Given** a gate that passes (no remaining disputes in synthesis), **When** the result is reported, **Then** the output includes: "Gate PASSED: spec — 0 disputes, 3 agents converged." The workflow may proceed to the next phase.

3. **Given** a gate that fails (disputes remain), **When** the result is reported, **Then** the output includes: "Gate BLOCKED: spec — 2 disputes remain. Review: {output}/summary/final.md" The disputes are listed with their synthesizer assessments. The workflow must not proceed until disputes are addressed.

4. **Given** a gate that fails, **When** the user addresses the disputes and re-runs the gate, **Then** the previous gate output is preserved (moved to `{output}/attempt-1/`) and the new deliberation runs fresh. Gate history is preserved for audit.

### US-2: Gate Configuration

As a developer, I want to define gates declaratively so that I can specify which phases get gates, which agents review them, and what the pass criteria are.

**Acceptance Criteria**:

1. **Given** this `gates.yml`:
   ```yaml
   gates:
     spec:
       agents:
         preset: review/thorough
       mode: cooperative
       rounds: 2
       pass: converged
     plan:
       agents:
         preset: review/quick
       mode: cooperative
       pass: converged
     implementation:
       agents:
         - name: security-reviewer
           prompt: |
             You are a security-focused code reviewer...
         - name: performance-reviewer
           prompt: |
             You are a performance-focused code reviewer...
       mode: cooperative
       pass: max_disputes 1
   ```
   **When** the config is parsed, **Then** three gates are registered for phases `spec`, `plan`, and `implementation`. Each gate has its own agent configuration, mode, and pass criteria.

2. **Given** a gate with `pass: converged`, **Then** the gate passes only if the synthesis has zero remaining disputes.

3. **Given** a gate with `pass: max_disputes N`, **Then** the gate passes if the synthesis has N or fewer remaining disputes. This allows "soft gates" that tolerate minor disagreements.

4. **Given** a gate with `agents.preset`, **Then** the preset is resolved using spec 004's preset engine (single preset or composition). This eliminates the need to define agents per-gate.

5. **Given** a gate without a `mode` field, **Then** it defaults to `cooperative`. Gates can use any mode but cooperative is the natural default for quality review.

### US-3: Gate as Standalone Command

As a developer, I want to run a gate manually from the command line so that I can validate any artifact at any time without waiting for a workflow phase transition.

**Acceptance Criteria**:

1. **Given** `/conversus gate spec path/to/spec.md`, **When** the command runs, **Then** it locates the `spec` gate definition in `gates.yml`, generates a `conversus.yml` with the gate's configuration and the provided path as `target`, executes the deliberation, and reports pass/fail.

2. **Given** `/conversus gate --inline path/to/artifact.md --preset review/thorough`, **When** the command runs, **Then** it creates an ad-hoc gate (no `gates.yml` required) using the specified preset and default settings. This supports one-off quality checks.

3. **Given** `/conversus gate plan path/to/plan.md --arbiter path/to/grounding.md`, **When** the command runs, **Then** the gate deliberation includes a subject arbiter. Blocked gates with an arbiter produce binding resolutions alongside the block notification.

---

## 3. Functional Requirements

### Gate Configuration

- **FR-001**: The system MUST support a `gates.yml` file (or a `gates:` section in `conversus.yml`) defining phase gates.
- **FR-002**: Each gate MUST define: a phase name (string identifier), agent configuration (inline agents, preset reference, or preset composition), and pass criteria.
- **FR-003**: Pass criteria MUST support: `converged` (zero disputes), `max_disputes N` (N or fewer disputes), and `always` (gate always passes — advisory mode, deliberation runs but never blocks).
- **FR-004**: Each gate MAY define: `mode` (default: cooperative), `rounds` (default: 1), `iterations` (default: 1), `arbiter` (optional), `output` (default: `{phase}-gate/`).
- **FR-005**: Gate agent configuration MUST support `preset:` (single preset), `presets:` (composition), or inline `agents:` list. Presets resolve via spec 004's engine.

### Gate Execution

- **FR-006**: When a gate is triggered, the system MUST generate a complete `conversus.yml` from the gate configuration and the target artifact path, then execute it as a standard conversus run.
- **FR-007**: Gate pass/fail MUST be determined by parsing the synthesis output's remaining disputes (using the Dispute-Parsing Subsystem) and comparing against the pass criteria.
- **FR-008**: When a gate passes, the system MUST report the result and allow the workflow to proceed. No blocking action.
- **FR-009**: When a gate blocks, the system MUST report the result, list the remaining disputes with synthesizer assessments, and indicate the gate output path for detailed review.
- **FR-010**: When a gate is re-run (same phase, same or updated artifact), the previous gate output MUST be preserved by moving it to `{output}/attempt-N/` where N is incremented. This provides audit history.

### Gate Command

- **FR-011**: The `/conversus gate` command MUST accept: phase name, artifact path, and optional overrides (`--preset`, `--mode`, `--rounds`, `--arbiter`).
- **FR-012**: The `/conversus gate --inline` variant MUST create an ad-hoc gate without requiring a `gates.yml` file.
- **FR-013**: Gate command output MUST include: pass/fail status, dispute count, agent count, and the path to the synthesis for review.

### Integration Hooks

- **FR-014**: The gate system MUST expose a machine-readable result (exit code or structured output) so that external tools (speckit, CI pipelines) can programmatically check gate status.
- **FR-015**: Exit code 0 for pass, exit code 1 for block, exit code 2 for gate configuration error.
- **FR-016**: When integrated with a spec-driven workflow, gates MUST run automatically at configured phase boundaries without manual invocation.

### Gate Output

- **FR-017**: Gate output MUST include a `gate-result.md` file at the top level of the gate output directory containing: phase name, artifact path, pass/fail verdict, dispute count, dispute summaries (if blocked), timestamp, and attempt number.
- **FR-018**: The full conversus output (reviews, cross-reviews, revisions, disputes, synthesis) MUST be preserved alongside `gate-result.md` for detailed review.

---

## 4. Success Criteria

- **SC-001**: A gate configured for the `spec` phase with `pass: converged` runs a conversus deliberation on a spec artifact, and correctly reports pass when no disputes remain and block when disputes remain.
- **SC-002**: A gate using `preset: review/thorough` resolves the preset via spec 004's engine and runs the deliberation with the preset's agents.
- **SC-003**: Re-running a blocked gate after addressing disputes preserves the previous attempt's output in `attempt-N/` and produces a fresh deliberation.
- **SC-004**: `/conversus gate --inline path/to/artifact.md --preset review/quick` works without a `gates.yml` file.
- **SC-005**: Gate results are machine-readable (exit codes) for CI/CD integration.
- **SC-006**: A gate with `pass: max_disputes 1` passes when 0 or 1 disputes remain and blocks when 2+ remain.
- **SC-007**: Gates do not modify the conversus engine — they are an orchestration layer that generates and executes standard `conversus.yml` configs.

---

## 5. Implementation Notes

### Thin Orchestration, Not Engine Changes

Gates are deliberately designed as orchestration around the existing engine, not modifications to it. A gate is: (1) read gate config, (2) generate conversus.yml, (3) invoke `/conversus run`, (4) parse synthesis output, (5) report result. The engine does not know it is running a gate.

This separation matters because it keeps the deliberation engine simple and testable. Gate logic (pass criteria, attempt history, integration hooks) lives in a separate layer that composes with the engine rather than extending it.

### Relationship to Spec 003 (Decision Framework)

Spec 003's guided workflow (`define -> interests -> mode -> converge -> arbitrate`) is the primary consumer of phase gates. Each command in the workflow produces an artifact; gates validate each artifact before the next command consumes it. The `/conversus gate` command can be invoked standalone or wired into spec 003's workflow automatically.

### Preset Selection for Gates

Most gates should use presets rather than inline agents. A "review/thorough" preset with 3-4 agents is appropriate for spec-level gates. A "review/quick" preset with 2 agents suits plan-level gates where speed matters more than depth. The preset system (spec 004) already handles resolution, composition, and caching.

### Advisory Mode

The `pass: always` criterion creates advisory gates that run deliberation but never block. This is useful for implementation-phase gates where you want the review record but don't want to block deployment on agent disagreements. The deliberation output still provides value as a structured review artifact.

---

## Closure note (2026-04-27)

**Why closed**: Folded into spec 011-phase-consensus-gates with CI/CD-specific additions. Per `ideas.md`: "Former spec 998 (phase consensus gates) folded into spec 011 with CI/CD-specific additions." The 998 numbering pattern was a temporary reservation slot that has been retired.

**Where the work lives**:
- `specs/done/011-phase-consensus-gates/` — the canonical, shipped spec
- `DRIFT-REPORT.md` (in this directory, moves with it) — 2026-04-05 partial-implementation drift documentation, preserved as historical record

**Reference**: `specs/AUDIT-2026-04-27.md` §D "998-phase-consensus-gates" — definitively folded, recommended close.
