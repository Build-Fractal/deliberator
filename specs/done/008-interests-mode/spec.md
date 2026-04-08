# Feature Specification: Interest Discovery & Mode Selection

**Feature ID**: `008-interests-mode`
**Created**: 2026-03-21
**Status**: Draft
**Depends On**: `007-subcommand-dispatch-define` (subcommand routing, problem.md schema), `004-preset-agents` (soft — preset suggestions for interests)
**Origin**: Decomposed from original 003-decision-framework, Phase A (part 2)

---

## 1. Feature Summary

Two commands that bridge the gap between a natural-language problem definition and a ready-to-execute `conversus.yml`.

`/conversus interests` reads `problem.md` and identifies the competing perspectives — the agents who will deliberate. Each interest gets a name, a one-sentence perspective, a calibrated identity prompt, and suggested documentation paths. The output is `interests.md`.

`/conversus mode` reads both `problem.md` and `interests.md`, recommends a competition mode based on the problem type and interest structure, and generates a complete `conversus.yml`. The user always has final say — they can override the recommendation.

These two commands pair naturally: interests determine mode, and mode generates the config. Together they eliminate the need for users to understand game theory or YAML schemas.

**What changes**: Two new subcommand handlers in SKILL.md. Two new artifact schemas (`interests.md`, auto-generated `conversus.yml`).

**What does not change**: `/conversus run` behavior. Engine execution. Template system.

---

## 2. Functional Requirements

### Common Options

- `--output <dir>`: Override the working directory for all artifact I/O. Both prerequisite files (`problem.md`, `interests.md`) and generated output will be read from and written to this directory. Default: current working directory.

### `/conversus interests`

- **FR-001**: MUST read `problem.md` and suggest 2-5 competing interests (the 2-5 range is enforced as a warning gate with user override, not a hard limit) with: name, perspective (one sentence), identity prompt, and suggested documentation paths.
- **FR-002**: Interest prompts MUST be calibrated to the problem type from `problem.md`:
  - `selection`: adversarial — each agent advocates for its alternative
  - `integration`: cooperative — each agent advocates for its needs while seeking alignment
  - `scoping`: honesty-calibrated — each agent declares capabilities and deferrals
  - `stress-test`: red/blue roles — attackers and defenders
- **FR-003**: User MAY add explicit interests via `--add <name>`. The agent generates a prompt and asks for docs.
- **FR-004**: Ungrounded agents (no docs) MUST be marked with `[NEEDS DOCS: suggest what to provide]` and a warning that ungrounded agents produce weaker arguments.
- **FR-005**: If `interests.md` already exists, the agent MUST present current interests and ask to add, remove, or modify.
- **FR-006**: Interests MAY reference presets from spec 004's preset engine. When a preset matches a suggested interest, the agent notes it: "This matches the `review/security` preset — use it?"

### `/conversus mode`

- **FR-007**: MUST recommend a competition mode based on problem type + interest structure using this decision matrix:

  | Problem Type | Default Mode | Default Strength |
  |---|---|---|
  | selection | winner-take-all | High |
  | integration | cooperative | High |
  | scoping | prisoners-dilemma | High |
  | stress-test | red-blue | High |
  | ambiguous / unset | (heuristic detection) | — present alternatives based on interest structure and problem signals |

- **FR-008**: When signals are mixed, MUST present the top 2 candidates with a plain-language trade-off comparison and ask the user to choose.
- **FR-009**: User MAY override the recommendation. The system explains the trade-off and regenerates.
- **FR-010**: Output MUST be a valid `conversus.yml` containing: mode, target (from problem.md source documents), output directory, all agents from interests.md with prompts and docs, iterations (default 1).
- **FR-011**: Generated YAML MUST use the exact same schema as hand-crafted configs. No schema extensions.
- **FR-012**: If `conversus.yml` already exists, show what would change and ask before overwriting.
- **FR-013**: If `interests.md` has changed since the last `conversus.yml` was generated, warn: "interests.md changed. Your conversus.yml may be out of date."

### Heuristic Mode Detection

When the user does not explicitly set a problem type in `problem.md`, the mode command infers from signals:

- **WTA signals**: "choose between", "pick one", "A vs B"; interests named after products/tools/approaches; mutual exclusivity
- **Cooperative signals**: "work together", "integrate", "align"; interests named after teams/roles/systems; all interests must survive
- **PD signals**: "who owns", "responsibility", "scope", "boundary"; overlapping capability claims
- **Red-Blue signals**: "what could go wrong", "risks", "stress-test"; asymmetric roles

### `interests.md` Schema

```markdown
# Competing Interests

## Problem Reference
<path to problem.md>

## Interests

### <interest-name>
- **Perspective**: <one sentence>
- **Prompt**: |
    <full identity prompt>
- **Docs**:
    - <path/to/doc1>
- **Preset**: <preset-name>  <!-- optional: matched from presets/ -->
- **Role**: <red | blue>  <!-- only for stress-test type -->
```

---

## 3. Success Criteria

- **SC-001**: After running `interests` + `mode` on a "selection" problem, the output `conversus.yml` has `mode: winner-take-all`.
- **SC-002**: Agent identity prompts reference the specific problem context and constraints, not generic "You are an expert in X" placeholders.
- **SC-003**: Generated `conversus.yml` is valid input for `/conversus run` — the roundtrip works.
- **SC-004**: Overriding mode to `cooperative` on a selection problem produces a `conversus.yml` with `mode: cooperative` and an explanation of the trade-off.
- **SC-005**: When `problem.md` is missing and user runs `/conversus interests`, the agent routes them to `/conversus define` first.

---

## 4. Constraints

- **Must NOT require game theory knowledge.** Mode names appear in YAML but not in user-facing conversation unless the user uses them first. Use plain language: "find the best option", "make these work together", "figure out who owns what", "stress-test this plan."
- **Must NOT generate agents without user confirmation.** Always present suggestions and get approval before writing.
- **Must NOT hard-code agents or documentation paths.** The framework is domain-agnostic.
