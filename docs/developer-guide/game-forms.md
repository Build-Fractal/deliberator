# Game Forms

Game forms define the mathematical structure underlying each deliberation mode. They live in `schema/game-forms/` as YAML files validated by Pydantic models in `deliberator/schemas/game_forms.py`.

## Existing game forms

| Form | YAML file | Typical mode | Description |
|------|-----------|-------------|-------------|
| `normal-form` | `normal-form.yml` | winner-take-all | Players choose simultaneously, payoffs from joint profile |
| `gnep` | `gnep.yml` | cooperative | Generalized Nash EP -- shared constraints, coupled feasibility |
| `parametric` | `parametric.yml` | cooperative | Continuous strategy spaces with parameterized payoffs |
| `stackelberg` | `stackelberg.yml` | red-blue | Leader-follower with sequential moves |
| `coalitional` | `coalitional.yml` | cooperative | Coalition formation with Shapley values |
| `congestion` | `congestion.yml` | resource-allocation | Shared resources with congestion costs |
| `bayesian` | `bayesian.yml` | negotiation | Incomplete information, type-conditional strategies |
| `repeated` | `repeated.yml` | prisoners-dilemma | Multi-round with discount factors |
| `mechanism-design` | `mechanism-design.yml` | mechanism-design | Mechanism design with incentive constraints |

The mapping from modes to game forms is in `schema/game-forms/mode-mapping.yml`.

## Game form to payoff mapping

Each mode has a corresponding payoff function in `deliberator/plugins/nashopt/payoffs.py`. The game form determines the mathematical structure; the payoff function computes the numeric score.

| Game form | Mode | Payoff function | Key features |
|-----------|------|----------------|--------------|
| `gnep` | cooperative | `cooperative_payoff` | `surviving_count` |
| `normal-form` | winner-take-all | `winner_take_all_payoff` | `ranking_position`, `score_differential` |
| `repeated` | prisoners-dilemma | `prisoners_dilemma_payoff` | `territory_held`, `overreach_penalty` |
| `stackelberg` | red-blue | `red_blue_payoff` | `severity_vector`, `role` |
| `bayesian` | negotiation | `negotiation_payoff` | `zopa_coverage`, `party_satisfaction` |
| `coalitional` | resource-allocation | `resource_allocation_payoff` | `utilization_efficiency`, `allocation_inequality`, `shapley_value` |
| `coalitional` | fair-division | `fair_division_payoff` | `proportionality_score`, `envy_count` |
| `mechanism-design` | mechanism-design | `mechanism_design_payoff` | `social_welfare_contribution`, `gaming_vulnerability_count` |

**Bayesian games** (negotiation): Agents have private types (reservation/aspiration prices). The payoff uses ZOPA coverage and satisfaction, reflecting incomplete-information equilibria where agents reveal preferences through concessions.

**Coalitional games** (resource-allocation, fair-division): Both use the coalitional form but with different solution concepts. Resource-allocation uses Shapley values for contribution measurement and penalizes inequality. Fair-division targets envy-freeness and proportionality.

**Mechanism design** (mechanism-design): Unlike other modes where agents play *within* a game, mechanism-design agents design the game itself. The payoff rewards social welfare contributions and penalizes gaming vulnerabilities -- incentive compatibility is the key constraint.

## Adding a new game form

### 1. Write the YAML schema

Create `schema/game-forms/my-form.yml`:

```yaml
form: my-form

description: >
  Description of when and why this form is used.

fields:
  - name: players
    type: list[string]
    required: true
    description: >
      Set of named players.

  - name: strategies
    type: map[string, list[string]]
    required: true
    description: >
      Per-player strategy sets.

  - name: my_custom_field
    type: float
    required: false
    description: >
      Some domain-specific parameter.

example:
  form: my-form
  players: [Alice, Bob]
  strategies:
    Alice: [cooperate, defect]
    Bob: [cooperate, defect]
  my_custom_field: 0.5
```

Valid field types (closed set): `string`, `integer`, `float`, `list[string]`, `list[float]`, `matrix`, `function`, `constraint_list`, `constraint_map`, `map[string, list[string]]`, `map[string, string]`, `map[string, function]`, `map[string, float]`.

### 2. Add the Pydantic model

In `deliberator/schemas/game_forms.py`, add a validation model:

```python
class MyFormGame(BaseModel):
    """Validates instances of the my-form game."""
    model_config = {"frozen": True}

    form: Literal["my-form"]
    players: list[str]
    strategies: dict[str, list[str]]
    my_custom_field: float = 0.5

    @model_validator(mode="after")
    def validate_structure(self) -> MyFormGame:
        if len(self.players) < 2:
            raise ValueError("Need at least 2 players")
        return self
```

### 3. Register in the validator dispatch

Add your form to the `FORM_VALIDATORS` dict (or equivalent dispatch) so the schema loading pipeline knows how to validate instances.

## Objective function templates

Objective templates live in `schema/objective-functions/`. Each defines a mathematical formulation that can be parameterized:

```yaml
name: competitive-selection
description: Select the best alternative from competing options.
game_form: normal-form
mode_compatibility: [winner-take-all]
form: "max_i sum_j(w_j * score_{i,j})"

parameters:
  - name: w
    type: float
    description: Weight vector for evaluation criteria
    default: 1.0
    range: {min: 0, max: 10}
    gap_question: "How much weight should this criterion have (0-10)?"

constraints:
  - non-negativity
  - budget
```

**Key fields:**
- `name`: Template identifier.
- `game_form`: Which game form this objective uses.
- `mode_compatibility`: Modes where this template applies.
- `form`: Symbolic mathematical expression.
- `parameters`: List of `ParameterDefinition` entries with type, range, defaults, and gap questions.
- `constraints`: References to constraint templates in `schema/objective-functions/constraints/`.

## Constraint templates

Constraint templates in `schema/objective-functions/constraints/`:

```yaml
# constraints/budget.yml
name: budget
description: Total expenditure must not exceed budget B.
symbolic: "sum_i(c_i * x_i) <= B"
parameters:
  - name: B
    type: float
    description: Budget constraint value
```

## Construction pipeline integration

The `construct_objective()` function in `deliberator/schemas/construction.py` orchestrates the 3-stage pipeline:

1. **Stage 1 (deterministic):** Classify decision type, select template, extract explicit parameters, identify gaps.
2. **Stage 2 (interactive):** Fill gaps via `GapFiller` protocol (interactive prompt, LLM, or fail-fast).
3. **Stage 3 (deterministic):** Assemble and validate the objective, substituting known values into the symbolic form.

To integrate a new game form into this pipeline, ensure your objective templates reference it and that the `DecisionType` to mode mapping in `construction.py` includes a path to your templates.
