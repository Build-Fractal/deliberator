# Feature Specification: Phase Consensus Gates

**Feature ID**: `011-phase-consensus-gates`
**Created**: 2026-03-21
**Status**: Draft
**Depends On**: `007-subcommand-dispatch-define` (subcommand dispatch), `004-preset-agents` (preset resolution for gate agents)
**Origin**: Extracted from 998-phase-consensus-gates. Unique CI/CD integration and declarative gate config preserved. Deliberation mechanics removed (already handled by the engine).

---

## 1. Feature Summary

Phase consensus gates are automatic conversus deliberations that run at workflow phase boundaries. When a phase completes (a spec is written, a plan is produced, code is implemented), its output becomes the target of a conversus run. If the deliberation converges, the gate passes. If disputes remain, the gate blocks.

The key value is twofold:
1. **Quality checks at phase boundaries** — catch spec gaps, plan inconsistencies, or implementation issues before they propagate downstream.
2. **CI/CD integration** — machine-readable exit codes and structured gate results that pipelines can act on.

Gates are a thin orchestration layer. A gate reads its config, generates a `conversus.yml`, invokes `/conversus run`, parses the synthesis, and reports pass/fail. The deliberation engine does not know it is running a gate.

**What changes**: New `/conversus gate` subcommand. New `gates` config section. Machine-readable `gate-result.md` output. Exit codes for CI/CD.

**What does not change**: Deliberation engine. Template system. Output format (gate output IS standard conversus output plus a gate-result summary).

---

## 2. Functional Requirements

### Gate Configuration

- **FR-001**: A `gates` section in `conversus.yml` (or standalone `gates.yml`) MUST define phase gates.
- **FR-002**: Each gate MUST define: phase name (string identifier), agent configuration (inline agents, preset reference, or preset composition), and pass criteria.
- **FR-003**: Pass criteria MUST support:
  - `converged` — zero remaining disputes (strict gate)
  - `max_disputes N` — N or fewer disputes (soft gate)
  - `always` — gate always passes, deliberation is advisory only
- **FR-004**: Each gate MAY define: `mode` (default: `cooperative`), `rounds` (default: 1), `arbiter` (optional), `output` (default: `{phase}-gate/`).

### Gate Execution

- **FR-005**: `/conversus gate <phase> <artifact-path>` MUST: locate the gate definition, generate a `conversus.yml` from gate config + artifact path, execute via `/conversus run`, parse synthesis for disputes, report pass/fail.
- **FR-006**: `/conversus gate --inline <path> --preset <preset>` MUST create an ad-hoc gate without requiring a `gates.yml`. Supports one-off quality checks.
- **FR-007**: Gate pass/fail MUST use the Dispute-Parsing Subsystem to count remaining disputes and compare against pass criteria.

### Machine-Readable Output

- **FR-008**: Exit codes: `0` = pass, `1` = block, `2` = gate configuration error.
- **FR-009**: `gate-result.md` MUST be produced at the top level of gate output containing: phase name, artifact path, pass/fail verdict, dispute count, dispute summaries (if blocked), timestamp, attempt number.
- **FR-010**: Full conversus output (reviews, cross-reviews, revisions, disputes, synthesis) MUST be preserved alongside `gate-result.md`.

### Re-Run Behavior

- **FR-011**: When a gate is re-run (same phase, same or updated artifact), previous output MUST be preserved by moving it to `{output}/attempt-N/`. Gate history is preserved for audit.

### Engine Independence

- **FR-012**: Gates MUST NOT modify the conversus engine. A gate is orchestration that generates and executes standard configs. The engine does not know it is running a gate.

### Example Configuration

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

---

## 3. Success Criteria

- **SC-001**: Gate with `pass: converged` correctly reports pass (0 disputes) or block (1+ disputes) with appropriate exit code.
- **SC-002**: Gate using `preset: review/thorough` resolves via spec 004's preset engine.
- **SC-003**: `/conversus gate --inline path/to/spec.md --preset review/quick` works without a `gates.yml`.
- **SC-004**: Exit codes are machine-readable — a CI pipeline can gate on conversus gate exit status.
- **SC-005**: Re-running a blocked gate preserves previous attempt output.
- **SC-006**: Gate with `pass: max_disputes 1` passes on 0-1 disputes and blocks on 2+.

---

## 4. Constraints

- **Must NOT modify the engine.** Gates compose with the engine, not extend it.
- **Must NOT require the guided workflow.** Gates work with presets, inline agents, or any valid agent config. The `define` → `interests` → `mode` pipeline is not required.
- **Must be CI/CD-friendly.** Exit codes, structured output, no interactive prompts during execution (configuration is declarative).
