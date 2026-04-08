# Feature Specification: Game Form Schema Library

**Feature ID**: `012-game-form-schemas`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `005-generalized-templates` (schema foundation: `schema/` directory, Pydantic validation patterns, YAML conventions)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 11 objective templates, Section 4 feature schemas). First spec in the game engine decomposition — establishes the mathematical vocabulary that all subsequent specs consume.

---

## 1. Feature Summary

Define standard game theory forms as YAML schemas that conversus can consume. These schemas describe the mathematical structure of games — what players exist, what strategies they have, what payoffs result — without any solver logic.

Today, conversus modes (cooperative, winner-take-all, prisoners-dilemma, red-blue) are implicit in template prompts. This spec makes the game-theoretic structure explicit and machine-readable. Each mode maps to a formal game theory form. The schemas are the shared vocabulary between the objective function library (spec 013), the feature extraction pipeline (spec 015), and the plugin system (specs 016-019).

**What changes**: New `schema/game-forms/` directory with YAML schema files. New Pydantic models for validation. Mode-to-form mapping table.

**What does not change**: SKILL.md. Template system. Execution engine. No solver, no optimizer, no plugin code.

---

## 2. Game Forms

### Normal Form

The simplest game representation. Players choose strategies simultaneously; payoffs are determined by the joint strategy profile.

- Player set: finite, named
- Strategy sets: per-player, finite
- Payoff matrix: |S_1| x |S_2| x ... x |S_N| tensor of per-player payoffs

Use case: winner-take-all mode, where agents are alternatives competing for selection.

### GNEP Form (Generalized Nash Equilibrium Problem)

Players optimize individual objectives subject to local constraints and shared (coupled) constraints. The standard form for most conversus modes.

- Player set: finite, named
- Decision variables: per-player continuous vectors x_i
- Objectives: per-player functions J_i(x_i, x_{-i})
- Local constraints: per-player g_i(x_i) <= 0
- Coupled constraints: shared h(x_1, ..., x_N) <= 0

Use case: cooperative, prisoners-dilemma, and red-blue modes. Most real deliberations have coupled constraints (shared target document, budget, timeline).

### Parametric Game Form

A GNEP where objectives and constraints depend on external parameters. Used for config optimization — the parameters are config values (rounds, agent count, mode).

- Inherits all GNEP fields
- Parameter vector: p (external, not optimized by players)
- Parametric objectives: J_i(x_i, x_{-i}; p)
- Parametric constraints: g(x; p) <= 0

Use case: config optimizer plugin (spec 019), where rounds and agent count are parameters and the optimizer finds parameter values that minimize cost subject to quality thresholds.

### Stackelberg Form

Leader-follower hierarchy. The leader commits to a strategy first; followers respond optimally. The leader anticipates follower responses when choosing.

- Leader set: typically one player
- Follower set: one or more players
- Leader objective: J_leader(x_leader, x_followers*(x_leader))
- Follower best-response: x_followers*(x_leader) = argmin J_followers subject to constraints

Use case: arbiter-as-leader scenarios where the arbiter sets binding rulings and agents respond. Also models the conversus operator (human) as leader choosing config, agents as followers.

---

## 3. Functional Requirements

### Schema Files

- **FR-001**: Each game form MUST be defined in a YAML file at `schema/game-forms/{form}.yml` where `{form}` is one of: `normal-form`, `gnep`, `parametric`, `stackelberg`.
- **FR-002**: Each schema file MUST define the following top-level fields: `form` (string identifier), `description` (plain-language), `fields` (per-field name, type, required flag, description), `example` (minimal valid instance).
- **FR-003**: Field types MUST use a closed set: `string`, `integer`, `float`, `list[string]`, `list[float]`, `matrix` (2D+ numeric), `function` (symbolic expression reference), `constraint_list` (flat list, for coupled constraints), `constraint_map` (per-player keyed, for local constraints), `map[string, list[string]]`, `map[string, string]`, `map[string, function]`.

### Mode-to-Form Mapping

- **FR-004**: A mode-to-form mapping MUST be defined in `schema/game-forms/mode-mapping.yml`:
  - `cooperative` -> `gnep`
  - `winner-take-all` -> `normal-form`
  - `prisoners-dilemma` -> `gnep`
  - `red-blue` -> `gnep`
- **FR-005**: The mapping MAY include override notes explaining why the default form is appropriate and when an alternative form might be preferred (e.g., WTA with continuous scoring could use GNEP instead of normal-form).

### Pydantic Models

- **FR-006**: Each game form MUST have a corresponding Pydantic model in `conversus/schemas/game_forms.py` that validates YAML instances against the schema.
- **FR-007**: Models MUST enforce required fields, type constraints, and structural invariants (e.g., payoff matrix dimensions match strategy set cardinalities in normal-form).
- **FR-008**: Models MUST NOT import any solver library (nashopt, jax, scipy, amplpy). Pure schema validation only.
- **FR-009**: The Pydantic models MUST be importable as `from conversus.schemas.game_forms import NormalFormGame, GNEPGame, ParametricGame, StackelbergGame`.

### Package Structure

- **FR-010**: Schema models MUST ship as part of the `conversus` package (under `conversus.schemas`) with dependencies limited to `pydantic` and `pyyaml`.
- **FR-011**: The YAML schema files MUST be included as package data, loadable at runtime for reference and validation.

---

## 4. Success Criteria

- **SC-001**: `NormalFormGame.model_validate(yaml.safe_load(open("schema/game-forms/normal-form.yml")))` succeeds — the example in the schema file validates against the Pydantic model.
- **SC-002**: A GNEP instance with mismatched player count and objective count raises `ValidationError` with a clear message.
- **SC-003**: Mode-mapping lookup: given mode `cooperative`, return form `gnep` with the corresponding schema.
- **SC-004**: All four Pydantic models import successfully in an environment with only `pydantic` and `pyyaml` installed — no solver dependency leaks.

---

## 5. Constraints

- **Must NOT include solver logic.** These are data schemas, not computation. Solvers live in plugin specs (017-019).
- **Must NOT modify SKILL.md.** The game form schemas are consumed by Python code (plugins, feature extraction), not by the template orchestrator.
- **Must NOT break without these schemas.** The core conversus engine does not depend on `conversus-schemas`. Schemas are consumed by downstream specs (013-020), not by the core.
