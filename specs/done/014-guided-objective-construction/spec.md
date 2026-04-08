# Feature Specification: Guided Objective Function Construction

**Feature ID**: `014-guided-objective-construction`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `013-objective-function-templates` (template library, parameter gap definitions), `008-interests-mode` (mode selection, `conversus.yml` generation)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 11 Approach 3: LLM-Guided Gap-Filling). The three-stage pipeline that turns natural language into parameterized objective functions.

---

## 1. Feature Summary

A 3-stage pipeline that turns a natural-language problem description into a parameterized objective function. The pipeline bridges `/conversus mode` (which selects the game mode) and the plugin system (which consumes objective functions for optimization).

Stage 1 is deterministic: pattern-match the problem against known objective function forms and identify parameter gaps. Stage 2 is interactive: an LLM asks plain-language questions to fill gaps. Stage 3 is deterministic: assemble the parameterized objective function and validate it.

This extends `/conversus mode` -- when game form schemas and objective templates are available, mode selection can recommend a specific objective function alongside the mode, producing a richer config. Without the game engine packages installed, `/conversus mode` continues to work exactly as spec 008 defined it.

**What changes**: New 3-stage construction pipeline in `src/conversus_schemas/construction.py`. New `objective.yml` output artifact. Optional integration point with `/conversus mode`.

**What does not change**: Core SKILL.md behavior. `/conversus mode` without game engine packages. Execution engine.

---

## 2. Pipeline Stages

### Stage 1: Symbolic Logic Parsing (Deterministic)

Input: `problem.md` (from spec 007) + mode (from spec 008 or user override).

1. Pattern-match problem description against known decision types:
   - `SELECTION`: "choose between", "pick one", "A vs B" -> competitive templates
   - `INTEGRATION`: "work together", "integrate", "align" -> cooperative templates
   - `SCOPING`: "who owns", "responsibility", "boundary" -> territory templates
   - `STRESS_TEST`: "what could go wrong", "risks" -> adversarial templates

2. Select the best-matching objective template from the library (spec 013) based on decision type + mode.

3. Extract any parameters that can be inferred from the problem text (e.g., explicit budget numbers, named alternatives).

4. Identify remaining parameter gaps -- parameters without values or defaults that require user input.

Output: candidate template + extracted parameters + gap list.

### Stage 2: LLM Gap-Filling (Interactive)

Input: gap list from Stage 1.

For each gap, the LLM generates a plain-language question using the template's `gap_question` field as a starting point, contextualized to the specific problem.

Example:
- Gap: `speed_weight` (range: 0-10, gap_question: "How important is speed?")
- Contextualized question: "You mentioned Redis is faster. On a scale of 1-10, how important is speed compared to cost for this decision?"
- User answer: "Speed is twice as important as cost"
- Mapped value: `speed_weight = 2.0`, `cost_weight = 1.0` (relative)

The LLM's role is translation, not reasoning. It converts natural-language answers to parameter values using the template's type and range constraints.

Output: filled parameter map.

### Stage 3: Objective Function Assembly (Deterministic)

Input: template + filled parameters.

1. Plug parameter values into the template's symbolic form.
2. Attach any selected constraint templates with their parameters.
3. Produce a complete `objective.yml` file.
4. Validate against the `ObjectiveTemplate` Pydantic model (spec 013).

Output: validated `objective.yml` in the working directory.

---

## 3. Functional Requirements

### Stage 1: Parsing

- **FR-001**: The parser MUST identify the decision type from `problem.md` text using keyword/pattern matching against a defined rule set. No LLM call for classification.
- **FR-002**: The parser MUST select the top 1-3 candidate objective templates from the library based on decision type and mode.
- **FR-003**: When multiple templates are viable candidates, the parser MUST present them to the user with plain-language descriptions and ask for selection.
- **FR-004**: The parser MUST extract parameter values that are explicitly stated in the problem text (e.g., "budget is $500/month" -> `budget_constraint = 500`).

### Stage 2: Gap-Filling

- **FR-005**: For each parameter gap, the system MUST generate a plain-language question contextualized to the problem.
- **FR-006**: User answers MUST be mapped to typed parameter values. The mapping MUST respect the parameter's type and range constraints from the template.
- **FR-007**: If a user answer cannot be mapped to a valid parameter value, the system MUST explain why and re-ask with guidance (e.g., "That value is outside the range 0-10. Could you pick a number between 0 and 10?").
- **FR-008**: Parameters with defaults MAY be skipped. The system MUST present defaults and ask: "Is [default] acceptable, or would you like to adjust?"
- **FR-009**: The gap-filling model MUST be configurable via `gap_fill_model` in config (per decision Q8). Default: cheapest capable model.

### Stage 3: Assembly

- **FR-010**: The assembled `objective.yml` MUST validate against the `ObjectiveTemplate` Pydantic model.
- **FR-011**: The output file MUST include: template name, game form, mode, all parameter values (explicit + defaults + gap-filled), selected constraints with parameters, and the fully-instantiated symbolic form.
- **FR-012**: Assembly is deterministic: same template + same parameters = same `objective.yml`. No randomness.

### Integration with `/conversus mode`

- **FR-013**: When the `conversus-schemas` package is installed, `/conversus mode` MAY offer to run guided objective construction after mode selection. This is opt-in, not automatic.
- **FR-014**: When `objective.yml` exists, it MUST be referenced in `conversus.yml` under an `objective` field so plugins can locate it.
- **FR-015**: When `conversus-schemas` is NOT installed, `/conversus mode` MUST work exactly as spec 008 defined. No import errors, no degraded behavior.

### Template Discovery & Decision Type Mapping

- **FR-016**: Construction pipeline MUST ship in the `conversus-schemas` package. No additional dependencies beyond `pydantic`, `pyyaml`, and whatever model the gap-filler uses (configured at runtime, not a package dependency).
- **FR-017**: Stage 1 MUST use a `load_objective_templates(templates_dir)` function that discovers all YAML files in `schema/objective-functions/` and returns validated `ObjectiveTemplate` instances. Reuse the existing `ObjectiveTemplate` Pydantic model from spec 013.
- **FR-018**: Decision type to template mapping MUST be explicit and deterministic:
  - `SELECTION` -> templates with `mode_compatibility` containing `winner-take-all`
  - `INTEGRATION` -> templates with `mode_compatibility` containing `cooperative`
  - `SCOPING` -> templates with `mode_compatibility` containing `prisoners-dilemma`
  - `STRESS_TEST` -> templates with `mode_compatibility` containing `red-blue`
  - General templates (weighted-sum, general-linear, etc.) are candidates for all types.
- **FR-019**: The decision type MUST be derived from `problem.md`'s Type field (spec 007) when available. Fall back to keyword pattern matching only when Type is absent or `[CLARIFY:]`-tagged.

### Output Schema

- **FR-020**: The assembled output MUST be validated by an `AssembledObjective` Pydantic model with fields: `template_name`, `game_form`, `mode`, `parameters` (dict mapping parameter name to filled value), `constraints` (list of constraint names), `symbolic_form` (the template form string with values substituted where possible), and `source` (dict with `problem_md` path and `filled_by` per parameter: `"explicit"`, `"default"`, or `"gap_filled"`).
- **FR-021**: `function`-type parameters (derived_from) MUST be included in the output with their `derived_from` value as a placeholder — they cannot be filled until deliberation runs. The `source` dict MUST record these as `"deferred"`.

### Gap-Fill Interface

- **FR-022**: Stage 2 MUST accept a `GapFiller` protocol: `fill(question: str, context: str) -> str`. The default implementation is `InteractiveGapFiller` which prompts the user in the conversation. An `LLMGapFiller` implementation accepts a model provider and generates contextual questions then maps answers.
- **FR-023**: When running non-interactively (no user present), all parameters without defaults MUST be reported as errors, not silently filled. Parameters with defaults use their defaults.

---

## 4. Success Criteria

- **SC-001**: Given a problem.md describing "choose between Redis and Postgres for caching", Stage 1 identifies decision type `SELECTION` and selects `competitive-selection` template.
- **SC-002**: Stage 2 asks about speed vs cost importance and maps "speed is twice as important" to `speed_weight=2.0, cost_weight=1.0`.
- **SC-003**: Stage 3 produces a valid `objective.yml` that passes Pydantic validation.
- **SC-004**: Running the pipeline twice with the same inputs produces identical `objective.yml` output.
- **SC-005**: `/conversus mode` without `conversus-schemas` installed works identically to spec 008 behavior.

---

## 5. Constraints

- **Must NOT include solver logic.** The pipeline constructs objective functions -- it does not solve them. Solving is the domain of plugins (specs 017-019).
- **Must NOT require game engine packages for core conversus.** The pipeline is an enhancement, not a dependency. Core mode selection (spec 008) works without it.
- **Must NOT generate arbitrary objective functions.** All outputs are parameterizations of known, curated templates (spec 013). The LLM fills gaps in known forms -- it does not invent new mathematics.
- **Must NOT make LLM calls in Stages 1 or 3.** Only Stage 2 (gap-filling) uses an LLM. Parsing and assembly are deterministic.
