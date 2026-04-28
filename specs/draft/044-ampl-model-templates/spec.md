# Feature Specification: AMPL Model Template Library & Self-Modeling System

**Feature ID**: `044-ampl-model-templates`
**Created**: 2026-04-03
**Status**: Draft — likely needs breakdown into sub-specs (template infra, binding system, agent skill, self-modeling are each substantial)
**Depends On**: `043-ampl-game-solvers` (game solver framework), `012-game-form-schemas` (DONE — game form definitions), `013-objective-function-templates` (DONE — objective template system)
**Docs Update**: New docs/developer-guide/ampl-models.md; new docs/api/ampl-templates/; update docs/developer-guide/game-forms.md
**Origin**: Research revealed conversus can use AMPL to model itself — its own schemas, game forms, and domains become parameterizable AMPL models. Agents can then BUILD new optimization models, not just consume pre-built ones.

---

## 1. Vision: Natural Language Game Theory Enforced with Optimization Modeling

Conversus deliberations are **natural language game theory** — agents argue positions, cross-review, and converge using game-theoretic structures (cooperative, adversarial, territorial, attack/defense). But natural language is stochastic. The same deliberation with the same prompts produces different results every time.

**Optimization models are the enforcement layer.** They translate the qualitative game theory described in prompts into formal mathematical models with deterministic parameters. The parameters become tuning knobs: adjust `gamma` → change overreach tolerance. Adjust severity weights → shift defense priorities. Same features + same parameters = same score, every run.

This spec builds the **template library and binding system** that makes this enforcement practical at scale:

1. **Templates**: A library of AMPL model files (`.mod`) indexed by game form, problem class, and solver — the more templates, the more problems agents can formally model
2. **Bindings**: Automatic mapping from conversus schemas (features, game forms, objectives) to AMPL parameters — schemas define structure, models define the math, features provide the data
3. **Agent skills**: Agents can browse templates, bind features, solve, interpret results, and generate new models — growing the library organically
4. **Self-modeling**: Conversus uses its own schemas as the data model for AMPL problems. The deliberation IS the optimization problem. The mapping is mechanical and bidirectional.

---

## 2. Paradigm Mapping: Conversus ↔ AMPL

### 2.1 Schema → AMPL Correspondence

| Conversus Concept | AMPL Concept | Example |
|-------------------|-------------|---------|
| `RoundFeatures` | `param` declarations | `param n_agents := 3;` |
| `AgentFeatures` | Indexed `param` sets | `param surviving{1..n_agents};` |
| `agreement_matrix` | 2D `param` | `param agree{1..n, 1..n};` |
| Game form (cooperative, WTA, etc.) | Model structure (objective + constraints) | Cooperative → Nash LP; WTA → Tournament MIP |
| Objective function template | AMPL `maximize`/`minimize` | `maximize welfare: sum{i} payoff[i];` |
| Feature extraction pipeline | Data binding (Python → AMPL params) | `ampl.get_parameter("agree").set_values(matrix)` |
| Mode | Template selector | `cooperative` → `templates/ampl/cooperative-nash.mod` |
| `EquilibriumScorer` output | AMPL solution extraction | `score = 1.0 - ampl.get_value("equilibrium_gap")` |

### 2.2 Engine → AMPL Correspondence

| Engine Concept | AMPL Concept |
|---------------|-------------|
| Phase sequencing | Model chaining (output of one model parameterizes the next) |
| Round loop | Iterative re-solve with updated features |
| Stagnation detection | Convergence check on objective value across iterations |
| Dispute count | Constraint violation count |
| Synthesis | Multi-objective Pareto frontier |

### 2.3 Domain → AMPL Correspondence

| Domain Concept | AMPL Concept |
|---------------|-------------|
| Domain-specific features | Problem-specific parameters |
| Scaffold | AMPL .mod template + .dat template |
| Verdict determination | Feasibility check (constraints satisfied?) |
| Score calculation | Objective function value |

---

## 3. AMPL Model Template Library

### 3.1 Template Structure

Each template lives in `ampl-templates/{category}/{name}.mod` with a companion `{name}.meta.yml`:

```
ampl-templates/
├── game-theory/
│   ├── nash-equilibrium-2player.mod     # LP: 2-player normal-form
│   ├── nash-equilibrium-nplayer.mod     # LP: N-player support enumeration
│   ├── minimax-zero-sum.mod            # LP: zero-sum minimax
│   ├── nash-bargaining.mod             # NLP: Nash bargaining solution
│   ├── correlated-equilibrium.mod      # LP: correlated equilibrium
│   └── stackelberg.mod                 # MIQP: Stackelberg leader-follower
│
├── allocation/
│   ├── envy-free-allocation.mod        # MIP: envy-free fair division
│   ├── maximin-fair-share.mod          # LP: maximin allocation
│   ├── proportional-allocation.mod     # LP: proportional fairness
│   ├── shapley-value.mod              # LP: Shapley value decomposition
│   └── vcg-auction.mod                # MIP: VCG mechanism
│
├── tournament/
│   ├── condorcet-ranking.mod           # MIP: Condorcet-consistent ranking
│   ├── kemeny-ranking.mod             # MIP: Kemeny optimal aggregation
│   └── borda-count.mod                # LP: Borda count scoring
│
├── scheduling/
│   ├── agent-scheduling.mod            # MIP: assign agents to phases
│   ├── round-budgeting.mod            # MIP: allocate budget across rounds
│   └── config-optimization.mod        # MIP: existing config optimizer (migrated)
│
├── network/
│   ├── influence-flow.mod             # LP: information flow in agent network
│   ├── coalition-formation.mod        # MIP: optimal coalition structure
│   └── consensus-convergence.mod      # QP: quadratic convergence model
│
└── domain-specific/
    ├── code-review-assignment.mod      # MIP: reviewer-to-PR matching
    ├── risk-mitigation.mod            # LP: red-blue resource allocation
    └── territory-partition.mod        # MIP: PD territory division
```

### 3.2 Template Metadata (`*.meta.yml`)

```yaml
name: nash-equilibrium-2player
category: game-theory
description: |
  Computes mixed-strategy Nash equilibrium for a 2-player normal-form game.
  Uses LP duality: Player 1's maximin strategy is optimal when Player 2
  plays their minimax strategy.

problem_class: LP
solver_requirements:
  minimum: [highs]          # Works with free bundled solver
  recommended: [gurobi]      # Better for larger instances
  capable: [cplex, mosek, cbc, xpress, copt]

compatible_modes:
  - cooperative
  - prisoners-dilemma

compatible_game_forms:
  - normal-form
  - strategic-form

input_schema:
  required:
    - n_players: integer     # Number of players (must be 2)
    - n_actions: integer     # Actions per player
    - payoff_matrix: float[n_players][n_actions][n_actions]
  optional:
    - epsilon: float         # Equilibrium tolerance (default 1e-6)

output_schema:
  - mixed_strategy: float[n_players][n_actions]   # Probability distribution
  - expected_payoff: float[n_players]              # Equilibrium payoffs
  - equilibrium_gap: float                        # Distance from exact NE
  - is_pure: boolean                              # Whether NE is pure strategy

feature_binding:
  # Maps conversus features → AMPL parameters
  n_players: len(features.agent_features)
  n_actions: 2  # cooperate/defect for cooperative; configurable
  payoff_matrix: build_from_agreement_matrix(features)

example_data:
  n_players: 2
  n_actions: 2
  payoff_matrix:
    # Classic PD payoffs
    player_1: [[3, 0], [5, 1]]
    player_2: [[3, 5], [0, 1]]

solve_time_estimate:
  n=2: "<10ms"
  n=5: "20ms"
  n=10: "50ms"
```

### 3.3 Solver Taxonomy

Full AMPL solver ecosystem mapped to problem classes:

| Problem Class | Open Source | Commercial | Best For |
|--------------|------------|-----------|----------|
| **LP** (Linear Programming) | HiGHS, CBC, SCIP | Gurobi, CPLEX, Xpress, COPT, Mosek | Nash equilibrium, minimax, maximin allocation |
| **MIP** (Mixed-Integer Programming) | HiGHS, CBC, SCIP, GCG | Gurobi, CPLEX, Xpress, COPT | Envy-free allocation, tournament ranking, VCG, scheduling |
| **QP** (Quadratic Programming) | OSQP (via SCIP) | Gurobi, CPLEX, Mosek, Knitro | Nash bargaining (log-transform), consensus convergence |
| **NLP** (Nonlinear Programming) | Ipopt, Bonmin | Knitro, CONOPT, SNOPT, MINOS | Nash bargaining (direct), mechanism design with non-linear utilities |
| **MINLP** (Mixed-Integer NLP) | Bonmin, Couenne | BARON, Knitro, LINDO Global | Fair division with non-linear valuations |
| **SOCP** (Second-Order Cone) | Mosek (open academic) | Gurobi, CPLEX, Mosek | Robust optimization, risk-aware allocation |
| **Global** | Couenne | BARON, LGO, LINDO Global | Global optimality guarantees for non-convex games |
| **GPU-Accelerated** | NVIDIA cuOpt | — | Large-scale vehicle routing, combinatorial optimization |

**Default solver chain:** HiGHS (LP/MIP) → Ipopt (NLP) → auto-detect commercial if installed.

---

## 4. Agent Skills for Model Building

### 4.1 AMPL Model Builder Skill

A skill that teaches conversus agents how to construct, parameterize, and solve AMPL models. Agents use this when they encounter optimization subproblems during deliberation.

```
.claude/skills/ampl-model-builder/SKILL.md
```

The skill provides:
1. **Template catalog** — browse available AMPL templates by problem class and game form
2. **Feature binding** — map conversus features to AMPL parameters
3. **Solver selection** — choose the right solver for the problem class
4. **Result interpretation** — extract solution concepts from AMPL output
5. **Model generation** — write NEW AMPL models for problems not covered by templates

### 4.2 Self-Modeling Capability

The key innovation: agents can use AMPL templates to model the **deliberation itself**. For example:

- "How many rounds should we run?" → `scheduling/config-optimization.mod`
- "Which agent should review which section?" → `scheduling/agent-scheduling.mod`
- "Are we at equilibrium?" → `game-theory/nash-equilibrium-nplayer.mod`
- "Is the allocation fair?" → `allocation/envy-free-allocation.mod`
- "What's the optimal defense?" → `game-theory/minimax-zero-sum.mod`

The agent reads the current `RoundFeatures`, selects a template, binds the features to AMPL parameters, solves, and interprets the result — all within a single deliberation phase.

### 4.3 Model Generation Workflow

When no template matches:

```
1. Agent identifies optimization subproblem from deliberation context
2. Agent selects closest template from catalog
3. Agent MODIFIES the template (add constraints, change objective)
4. Agent validates modified model (syntax check via amplpy)
5. Agent solves and interprets
6. If the modified model is reusable, agent saves it as a new template
```

This is the growth mechanism: the template library expands organically as agents encounter new problem types.

---

## 5. Feature Binding System

### 5.1 Automatic Binding

The `feature_binding` section in template metadata maps conversus features to AMPL parameters automatically:

```python
def bind_features_to_ampl(
    template: AMPLTemplate,
    features: RoundFeatures,
) -> dict[str, Any]:
    """Automatically map features to AMPL parameters."""
    bindings = {}
    for param_name, binding_expr in template.feature_binding.items():
        if callable(binding_expr):
            bindings[param_name] = binding_expr(features)
        elif isinstance(binding_expr, str):
            # Evaluate as Python expression with features in scope
            bindings[param_name] = eval(binding_expr, {"features": features})
        else:
            bindings[param_name] = binding_expr
    return bindings
```

### 5.2 Built-in Binding Functions

```python
# conversus/plugins/ampl/bindings.py

def build_payoff_matrix(features: RoundFeatures) -> dict:
    """Build N×N payoff matrix from agreement_matrix + surviving_count."""
    ...

def build_severity_matrix(features: RoundFeatures) -> dict:
    """Build severity matrix for red-blue from agent severity_vectors."""
    ...

def build_territory_matrix(features: RoundFeatures) -> dict:
    """Build territory overlap matrix for PD from territory claims."""
    ...

def build_valuation_matrix(features: RoundFeatures) -> dict:
    """Build agent×item valuation matrix for fair division."""
    ...

def build_score_differential(features: RoundFeatures) -> dict:
    """Build pairwise score differentials for WTA tournament."""
    ...
```

---

## 6. Functional Requirements

### Template Library
- **FR-001**: Templates MUST be stored as `.mod` files with companion `.meta.yml` metadata.
- **FR-002**: Templates MUST be indexed by `problem_class`, `compatible_modes`, and `compatible_game_forms`.
- **FR-003**: Each template MUST specify `solver_requirements.minimum` (a free solver that works).
- **FR-004**: Each template MUST include `example_data` for testing without real features.
- **FR-005**: Templates MUST be loadable via `importlib.resources` (pip-installable).

### Feature Binding
- **FR-006**: Automatic binding MUST map `RoundFeatures` → AMPL params using metadata.
- **FR-007**: Binding MUST fail gracefully when features are missing (use defaults from metadata).
- **FR-008**: Custom binding functions MUST be registrable per domain.

### Agent Skill
- **FR-009**: The AMPL model builder skill MUST be loadable by any conversus agent.
- **FR-010**: Agents MUST be able to browse templates by problem class and mode.
- **FR-011**: Agents MUST be able to generate new models from template modifications.
- **FR-012**: Generated models MUST be syntax-validated before solving.

### Self-Modeling
- **FR-013**: The system MUST support solving optimization problems DURING a deliberation phase (not just post-hoc).
- **FR-014**: Template selection MUST be automatic when mode + game form uniquely identify a template.
- **FR-015**: When multiple templates match, the agent MUST choose based on problem class and solver availability.

### Solver Management
- **FR-016**: Solver auto-detection MUST identify all installed AMPL solvers.
- **FR-017**: Solver selection MUST respect `solver_requirements.minimum` from template metadata.
- **FR-018**: If no compatible solver is installed, the system MUST report which solvers to install and fall back to heuristic.

---

## 7. Success Criteria

- **SC-001**: Template library contains at least 1 template per game form (cooperative, WTA, PD, red-blue, negotiation, resource-allocation, fair-division, mechanism-design).
- **SC-002**: An agent can select a template, bind features, solve, and interpret results within a single deliberation phase.
- **SC-003**: Self-modeling works: running `config-optimization.mod` from within a deliberation produces the same result as the standalone config optimizer.
- **SC-004**: An agent can modify an existing template to create a new model (template growth).
- **SC-005**: All templates pass solve tests with `example_data` using HiGHS (free solver).
- **SC-006**: Feature binding correctly maps `RoundFeatures` for all 8 modes.

---

## 8. Phasing

### Phase 1: Template infrastructure + 6 core templates (~2 weeks)
1. Template directory structure and metadata schema
2. Template loader with `importlib.resources` support
3. Feature binding system
4. 6 templates from spec 043 (cooperative Nash, red-blue minimax, PD dominant, WTA tournament, fair-division envy-free, resource-allocation maximin)
5. Solver auto-detection

### Phase 2: Agent skill + self-modeling (~2 weeks)
6. AMPL model builder skill (`.claude/skills/ampl-model-builder/`)
7. Template catalog browsing
8. In-deliberation solving integration
9. Model generation from template modification
10. Tests for self-modeling (config optimizer as dog food)

### Phase 3: Template expansion (~ongoing)
11. Scheduling templates (agent assignment, round budgeting)
12. Network templates (influence flow, coalition formation)
13. Domain-specific templates (code review assignment, risk mitigation)
14. Community-contributed templates (template submission process)
15. Deferred templates from spec 043 (negotiation, mechanism-design)

---

## 9. Constraints

- Templates are part of the `conversus-ampl` premium package (not free tier).
- The template metadata schema MUST be stable — templates from different versions must be forward-compatible.
- Agents MUST NOT execute arbitrary AMPL code from untrusted sources — templates are curated.
- Generated models are saved to the user's workspace, not to the template library (library growth requires review).
- The self-modeling capability is opt-in — agents only use AMPL when the user enables the optimizer plugin.

---

## 10. Open Questions

1. **Template authoring UX**: Should there be a `/conversus ampl` subcommand for browsing and testing templates?
   - **Lean**: Yes, but defer to post-spec-043. The skill is sufficient for now.

2. **Model versioning**: Templates may need updates as AMPL syntax or solver APIs evolve. How to version?
   - **Lean**: Semantic versioning in `meta.yml`. Templates are backward-compatible within a major version.

3. **Solver licensing**: Some templates work best with commercial solvers (Gurobi, CPLEX). How to handle licensing?
   - **Lean**: Document in `solver_requirements`. Auto-detect available solvers. Never require commercial.

4. **Template marketplace**: Could templates be shared via a marketplace (like conversus presets)?
   - **Lean**: Yes, long-term. The `meta.yml` format supports this. Marketplace integration is a future spec.

5. **Security**: If agents can generate AMPL models, could they produce models that consume excessive resources?
   - **Lean**: AMPL solver timeouts (default 10s) prevent runaway computation. Template metadata includes `solve_time_estimate` for budgeting.
