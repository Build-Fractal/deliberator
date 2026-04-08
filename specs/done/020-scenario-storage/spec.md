# Feature Specification: Scenario Storage & Replay

**Feature ID**: `020-scenario-storage`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `016-plugin-system` (plugin hooks for scenario save/load triggers)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 12: Scenario Storage and Replay, decisions Q7: file-based storage, Q10: no sharing infrastructure).

---

## 1. Feature Summary

Store game configurations as reusable scenarios for replay across deliberations. A scenario captures the decision framework -- mode, objective template, parameters, agent roles -- separately from the data it operates on. The same scenario can be replayed with different target documents, enabling consistent decision-making across recurring problem types.

Per decision Q7, storage is file-based: `scenarios/{id}.yml` in the project directory, git-tracked. Per decision Q10, no sharing infrastructure; git handles distribution. Database storage (Memgraph, PostgreSQL + pgvector) is a future evolution when cross-run analysis justifies the complexity.

**What changes**: New `scenarios/` directory. New `/conversus save`, `/conversus replay`, `/conversus scenarios` commands. Scenario YAML schema and Pydantic model.

**What does not change**: Core deliberation engine. Template system. Plugin behavior.

---

## 2. Scenario Object

A scenario has three sections: game structure (reusable), data bindings (swappable), and run history (auditable).

### Game Structure (Reusable)

The decision framework itself, independent of specific documents:

- `mode`: deliberation mode
- `objective_template`: reference to an objective function template (spec 013), if used
- `parameters`: objective function parameter values (spec 014), if used
- `agent_roles`: role descriptions (perspective, prompt skeleton) without specific document bindings
- `rounds`: number of rounds
- `stagnation`: detection config
- `arbiter`: arbiter config (grounding type, trigger, influence)

### Data Bindings (Swappable)

The run-specific data that changes between replays:

- `target`: path to the target document(s) under deliberation
- `agent_docs`: per-agent documentation paths
- `grounding_doc`: arbiter grounding document path

Data bindings are null in the stored scenario and provided at replay time.

### Run History (Auditable)

A log of every time this scenario was executed:

- `date`: timestamp
- `target`: what was deliberated
- `outcome`: brief description of the result
- `equilibrium_score`: float (if equilibrium scorer was active)
- `rounds_used`: integer
- `agents_launched`: integer

---

## 3. Functional Requirements

### Scenario Schema

- **FR-001**: Scenarios MUST be stored as YAML files at `scenarios/{id}.yml` where `{id}` is a user-provided or auto-generated slug.
- **FR-002**: A `Scenario` Pydantic model MUST validate scenario files, enforcing required fields and type constraints.
- **FR-003**: The scenario schema MUST cleanly separate game structure (reusable) from data bindings (swappable) from run history (append-only).

### Save Command

- **FR-004**: `/conversus save <name>` MUST extract the current game structure from `conversus.yml` (and `objective.yml` if present) and save it as `scenarios/<name>.yml`.
- **FR-005**: If a scenario with the same name exists, the user MUST be asked whether to overwrite, rename, or cancel.
- **FR-006**: Data bindings in the saved scenario MUST be set to null. The scenario captures the framework, not the data.
- **FR-007**: The current run's outcome MUST be appended to the scenario's run history.

### Replay Command

- **FR-008**: `/conversus replay <name> --target <path>` MUST load the scenario's game structure, bind the new target path, and generate a `conversus.yml` ready for execution.
- **FR-009**: Replay MUST present the scenario summary (mode, agents, parameters, prior run history) and ask for confirmation before generating config.
- **FR-010**: The user MUST be able to adjust parameters before execution: `/conversus replay <name> --target <path> --adjust`. This re-runs the gap-filling stage (spec 014) with the stored template.
- **FR-011**: After a replayed run completes, the outcome MUST be appended to the scenario's run history.

### List Command

- **FR-012**: `/conversus scenarios` MUST list all saved scenarios with: name, mode, last used date, number of runs, most recent outcome.
- **FR-013**: `/conversus scenarios <name>` MUST display full scenario details including run history.

### Storage

- **FR-014**: Scenario files MUST be human-readable YAML, suitable for git tracking and code review.
- **FR-015**: Scenario files MUST be self-contained -- no external references except to objective function templates (by name, not path).
- **FR-016**: Run history MUST be append-only. Modifying historical entries requires manual YAML editing (intentional friction).

### Cross-Run Analysis

- **FR-017**: With 3+ runs of the same scenario, `/conversus scenarios <name> --analysis` MUST report:
  - Outcome consistency: how often the same type of outcome recurs
  - Average rounds used and agent launches
  - Equilibrium score trend (if scorer was active)
- **FR-018**: Cross-run analysis is computed from run history at display time, not stored separately.

### Future Storage Options

- **FR-019**: The scenario storage interface MUST be abstracted behind a `ScenarioStore` protocol (Python Protocol class) with `save`, `load`, `list`, `append_run` methods. This enables future implementations (Memgraph, PostgreSQL + pgvector) without changing the command layer.

---

## 4. Success Criteria

- **SC-001**: `/conversus save caching-decision` after a WTA deliberation creates `scenarios/caching-decision.yml` with mode `winner-take-all` and null data bindings.
- **SC-002**: `/conversus replay caching-decision --target new-spec.md` generates a valid `conversus.yml` using the stored game structure with the new target.
- **SC-003**: After 3 replays, `/conversus scenarios caching-decision --analysis` reports outcome consistency and average metrics.
- **SC-004**: Scenario files are clean, human-readable YAML that passes Pydantic validation.
- **SC-005**: A scenario saved from a run with the equilibrium scorer includes the score in run history; a scenario saved without the scorer omits it gracefully.

---

## 5. Constraints

- **Must NOT require a database.** File-based storage (decision Q7) is the only mandatory backend. Database implementations are future optional backends behind the `ScenarioStore` protocol.
- **Must NOT build sharing infrastructure.** Scenarios are YAML files; git handles distribution (decision Q10). Marketplace is a future product decision.
- **Must NOT couple to plugins.** Scenarios work with or without plugins. Plugin-produced data (equilibrium scores) is stored in run history when available, omitted when not.
- **Must NOT modify historical run entries.** Run history is append-only. This provides an audit trail of how the same decision framework performed across different data.
