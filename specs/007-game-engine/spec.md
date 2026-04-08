# Feature Specification: Pluggable Game Engine with Nash Equilibrium Optimization

**Feature ID**: `007-game-engine`
**Created**: 2026-03-20
**Status**: Draft
**Depends On**: `005-generalized-templates` (schema/linter foundation), `004-universal-rounds` (all-mode rounds/stagnation/arbitration)
**Input**: Business model separation (free deliberation engine vs paid optimization layer) and long-term architectural vision to evolve from template-driven prompts to a pluggable game engine.

---

## 1. Feature Summary

Conversus today is a **template-driven prompt orchestrator**. Game theory concepts (cooperative, winner-take-all, prisoners-dilemma, red-blue) are metaphors encoded as prompt templates. Convergence is detected by counting dispute headings. There is no mathematical optimization, no equilibrium verification, and no predictive capability.

This spec defines the architecture for evolving conversus into a **pluggable game engine** where:

1. The **free core** remains the template-driven deliberation engine (SKILL.md + templates)
2. A **paid plugin layer** adds mathematical game theory: equilibrium verification, convergence prediction, parametric config optimization, and deliberation quality scoring
3. The plugin interface is **pluggable** — the core engine works without any plugins, plugins can be swapped, and third-party plugins can be developed

The long-term vision: conversus transitions from "templates tell agents what to do" to "a game engine computes optimal strategies, templates format the output." The engine drives behavior; templates present it.

---

## 2. Business Model

### Free Tier: Conversus Core

Everything that exists today plus specs 004 and 005:
- Multi-agent deliberation across all 4 modes
- 5-6 phase execution (review → cross-review → revision → disputes → synthesis → arbitration)
- Multi-round execution with stagnation detection
- Template-driven agent behavior
- Cross-round synthesis
- Schema validation (spec 005)

**Value proposition**: Structured multi-agent disagreement → convergence. Free forever.

### Paid Tier: Game Engine Plugins

Mathematical game theory that saves money and proves outcomes:

| Plugin | What It Does | User Value |
|--------|-------------|------------|
| **Equilibrium Scorer** | After deliberation, scores whether the outcome is a Nash equilibrium | "Was this a good outcome?" — provable quality |
| **Convergence Predictor** | Before Round N+1, predicts whether continuing will produce convergence | "Should I spend tokens on another round?" — cost savings |
| **Config Optimizer** | Given a problem description, computes optimal rounds/agents/mode/iterations | "What config should I use?" — better outcomes, fewer wasted agents |
| **Stagnation Forecaster** | After Round 1, predicts total rounds needed | "How much will this cost?" — budget planning |
| **Quality Auditor** | Compares deliberation dynamics against game-theoretic predictions | "Did agents behave rationally?" — deliberation health check |

**Value proposition**: Spend less on agent launches, get better outcomes, prove the result is mathematically sound.

### Economics

The free tier generates deliberation data (agent positions, concessions, convergence patterns). The paid tier uses that data to optimize future runs. Users who run more deliberations get more value from optimization — natural upsell.

A 69-agent stress test that could have been predicted to converge in 2 rounds saves ~23 agent launches. At scale, this is real cost savings.

---

## 3. Architecture: Plugin System

### Design Principles

1. **Core works alone.** Removing all plugins produces exactly current conversus behavior. No degradation.
2. **Plugins are optional.** Each plugin is independently installable. No plugin depends on another plugin (they may depend on the core).
3. **Plugins are swappable.** The interface is defined; implementations can vary. nashopt today, something else tomorrow.
4. **Data flows one direction.** Core produces deliberation artifacts → plugins consume them. Plugins never modify core artifacts. Plugin output goes to a separate namespace.
5. **Plugin output is advisory.** The core engine makes the decisions (run another round? trigger arbitration?). Plugins provide recommendations. The user (or a future autonomous mode) decides whether to follow them.

### Plugin Interface

```yaml
# conversus.yml — plugin configuration
plugins:
  - name: equilibrium-scorer
    package: conversus-nashopt        # pip-installable package
    config:
      threshold: 0.85                 # minimum equilibrium quality score

  - name: convergence-predictor
    package: conversus-nashopt
    config:
      min_confidence: 0.7             # minimum prediction confidence to act on

  - name: config-optimizer
    package: conversus-nashopt
    config:
      budget: 50                      # maximum agent launches
      optimize: [rounds, agents]      # which config params to optimize
```

### Plugin Lifecycle Hooks

Plugins hook into the deliberation at defined points:

```
PRE_EXECUTION
  ├── config-optimizer: recommend config changes before launch
  └── stagnation-forecaster: predict total rounds needed

POST_PHASE_5 (after each round's synthesis)
  ├── convergence-predictor: should we run another round?
  └── equilibrium-scorer: how good is the current outcome?

POST_DELIBERATION (after all rounds complete)
  ├── equilibrium-scorer: final quality score
  └── quality-auditor: compare dynamics against predictions

POST_ARBITRATION (after Phase 6)
  └── equilibrium-scorer: re-score after arbiter rulings
```

### Plugin Output

Plugins write to a `plugins/` subdirectory in the output:

```
output/
├── summary/final.md              # core output (unchanged)
├── {agent}/                      # core output (unchanged)
├── arbitration/                  # core output (unchanged)
└── plugins/
    ├── equilibrium-score.json    # { score: 0.92, details: {...} }
    ├── convergence-prediction.json
    └── config-recommendation.json
```

### Plugin API (Python)

```python
from conversus.plugins import Plugin, HookPoint, DeliberationState

class EquilibriumScorer(Plugin):
    name = "equilibrium-scorer"
    hooks = [HookPoint.POST_PHASE_5, HookPoint.POST_DELIBERATION]

    def execute(self, state: DeliberationState, config: dict) -> PluginResult:
        """
        state contains:
          - mode: str
          - round: int
          - agents: list[AgentState]  # positions, concessions, disputes
          - synthesis: str            # current synthesis content
          - history: list[RoundState] # all prior rounds
        """
        # Extract numerical features from deliberation
        features = self.extract_features(state)

        # Compute equilibrium quality using nashopt
        score = self.compute_equilibrium_score(features)

        return PluginResult(
            recommendation=f"Equilibrium quality: {score:.2f}",
            data={"score": score, "details": features},
            advisory=True  # core engine is not required to act on this
        )
```

---

## 4. Nash Equilibrium Integration (nashopt)

### Feature Extraction: Text → Numbers

The bridge between LLM deliberation and mathematical game theory. Each round's artifacts are reduced to numerical features:

| Feature | Source | Extraction |
|---------|--------|------------|
| Position vector | Agent review/revision | Encode each recommendation as a scalar (P1=3, P2=2, P3=1, withdrawn=0) |
| Concession rate | Phase 3 revision | Count withdrawn + modified / total recommendations |
| Dispute count | Phase 4 disputes | Count `**Dispute:` entries |
| Convergence count | Phase 4 disputes | Count `**Converged:` entries |
| Severity vector | Red-blue reviews | Encode threat severities (critical=4, high=3, medium=2, low=1) |
| Territory claim vector | PD reviews | Binary: does agent claim this area? |
| Ranking vector | WTA synthesis | Position in ranking per round |

### Equilibrium Scoring

Given extracted feature vectors for all agents across all rounds:

1. **Define payoff functions per mode:**
   - Cooperative: J_i = number of agent i's recommendations accepted in synthesis
   - WTA: J_i = 1 if winner, 0 if not (binary payoff)
   - PD: J_i = territory claimed minus penalty for overreach (territory contested by others)
   - RB: J_red = severity of accepted risks; J_blue = severity of mitigated risks

2. **Compute best responses** using nashopt's `check_equilibrium()`:
   - For each agent, given other agents' final positions, could this agent improve its payoff by changing position?
   - If no agent can improve → Nash equilibrium confirmed

3. **Score**: Ratio of agents at equilibrium / total agents. Score of 1.0 = perfect Nash equilibrium.

### Convergence Prediction

Using gnep-learn's active learning approach:

1. After Round 1, extract position vectors for all agents
2. Build linear surrogate models of best-response functions (Kalman filter, exactly as gnep-learn does)
3. Check if the learned models have a fixed point
4. If yes → predict convergence, estimate rounds needed
5. If no → predict stagnation, recommend arbitration

### Config Optimization

Using nash_mpqp's parametric approach:

1. Model the deliberation as a parametric game where parameters are config values (rounds, iterations, agent count)
2. For a given problem structure, compute which parameter values produce equilibria with minimum total agent launches
3. Recommend config before execution

---

## 5. Evolution Path: Templates → Engine

### Phase 1: Plugin Infrastructure (Current Spec Scope)

- Define the plugin interface (hooks, API, output format)
- Implement plugin loading from `conversus.yml`
- Add lifecycle hooks to SKILL.md orchestration
- No mathematical plugins yet — just the scaffolding

### Phase 2: Feature Extraction Pipeline

- Build the text → numerical feature extraction
- Define feature schemas per mode
- Validate against real deliberation data (spec 004 stress test artifacts)
- Ship as `conversus-features` package

### Phase 3: nashopt Integration (First Paid Plugin)

- Implement `conversus-nashopt` package
- Equilibrium scorer (POST_DELIBERATION hook)
- Convergence predictor (POST_PHASE_5 hook)
- Requires: nashopt, jax, scipy as dependencies
- Ship as `pip install conversus-nashopt`

### Phase 4: Predictive Optimization

- Config optimizer (PRE_EXECUTION hook)
- Stagnation forecaster (PRE_EXECUTION hook)
- Requires: gnep-learn, nash_mpqp as additional dependencies
- Trained on accumulated deliberation data

### Phase 5: Engine-Driven Deliberation

The long-term destination. The game engine computes optimal agent strategies; templates format the output for LLM consumption. The shift:

| Aspect | Template-Driven (Today) | Engine-Driven (Future) |
|--------|------------------------|----------------------|
| Agent behavior | Defined by prompt template | Computed by game engine, presented via template |
| Mode selection | User picks or heuristic keyword match | Engine analyzes game structure, recommends mathematically |
| Convergence | Count disputes, hope for decrease | Engine predicts equilibrium, knows when to stop |
| Stagnation | Compare dispute counts between rounds | Engine detects no fixed point in best-response models |
| Round count | User guesses, max 5 | Engine computes optimal round count for budget |
| Agent count | User decides | Engine recommends minimum agents for equilibrium coverage |
| Arbitration trigger | "disputes_remain" heuristic | Engine identifies disputes that cannot converge mathematically |
| Quality assurance | None — user reads synthesis | Equilibrium score proves outcome quality |

Templates don't disappear — they become the presentation layer. The engine becomes the decision layer.

---

## 6. Functional Requirements

### Plugin System (P1)

- **FR-001**: A `plugins` field in `conversus.yml` MUST allow declaring plugins with name, package, and config
- **FR-002**: The orchestrator MUST load plugins at startup and call them at defined lifecycle hooks
- **FR-003**: Plugin failure MUST NOT block core deliberation. Failed plugins emit warnings; execution continues.
- **FR-004**: Plugin output MUST be written to `{output}/plugins/` — never modifying core artifacts
- **FR-005**: Core deliberation MUST produce identical output with or without plugins installed

### Plugin API (P1)

- **FR-006**: A Python plugin base class MUST define: name, hooks, execute(state, config) → PluginResult
- **FR-007**: DeliberationState MUST expose: mode, round, agents (positions/concessions), synthesis content, round history
- **FR-008**: PluginResult MUST include: recommendation (string), data (dict), advisory (bool)
- **FR-009**: Plugins MUST be installable via `pip install {package-name}`

### Feature Extraction (P2)

- **FR-010**: A feature extraction pipeline MUST convert deliberation artifacts to numerical vectors per the feature schema
- **FR-011**: Feature schemas MUST be defined per mode (cooperative, red-blue, WTA, PD)
- **FR-012**: Feature extraction MUST be deterministic — same artifacts produce same features

### nashopt Integration (P3)

- **FR-013**: An equilibrium scorer plugin MUST compute a Nash equilibrium quality score (0.0-1.0) from extracted features
- **FR-014**: A convergence predictor plugin MUST predict whether the next round will reduce disputes, with a confidence level
- **FR-015**: A config optimizer plugin MUST recommend config parameters given a problem description and agent budget

---

## 7. Success Criteria

- **SC-001**: A conversus run with `plugins: []` (empty) produces identical output to a run without the plugins field — zero behavioral change
- **SC-002**: A conversus run with a configured equilibrium scorer produces a `plugins/equilibrium-score.json` alongside the standard output
- **SC-003**: The equilibrium scorer, run against the spec 004 stress test data (69-agent, 3-mode, 2-round run), produces meaningful quality scores that differentiate between the fully-converged PD result and the severity-disputed RB Round 1 result
- **SC-004**: The convergence predictor, given Round 1 data from the spec 004 stress test, correctly predicts that all 3 modes will converge in Round 2
- **SC-005**: Plugin installation is `pip install conversus-nashopt` — no manual configuration beyond adding the plugin to `conversus.yml`

---

## 8. Dependencies

### Core (Free)

No new dependencies. Plugin loading uses Python's standard `importlib`.

### conversus-embeddings (Paid — Tier 1)

- `sentence-transformers` — embedding model runtime
- Open MTEB-ranked model (e.g., top-10 from MTEB leaderboard)
- No cloud API required — runs locally

Provides: semantic stagnation detection, convergence scoring via position clustering, cross-round drift analysis.

### conversus-nashopt (Paid — Tier 2, Premium)

- `nashopt` — GNE computation, equilibrium verification
- `jax` — automatic differentiation (nashopt dependency)
- `scipy` — optimization (nashopt dependency)
- `gnep-learn` — active learning of best-response models (convergence prediction)
- `nash-mpqp` — parametric game solving (config optimization)

Provides: mathematical equilibrium verification, best-response computation, parametric config optimization, objective function construction.

These are dependencies of the paid plugin packages, not of the free core.

---

## 9. Constraints

### Must NOT

- **Must NOT make the core depend on nashopt, jax, or any numerical library.** The free tier runs on any Python 3.12+ installation with only PyYAML.
- **Must NOT let plugins modify core deliberation artifacts.** Plugins read; they do not write to `summary/`, `{agent}/`, or `arbitration/`.
- **Must NOT make plugin output authoritative.** Plugins are advisory. The user decides whether to follow recommendations. A future "autonomous mode" may act on plugin recommendations automatically, but that's a separate spec.
- **Must NOT require plugins for any existing functionality.** Everything that works today continues to work without plugins.

### Must

- **Must be pluggable.** Third-party developers can create plugins by implementing the Plugin base class and publishing to PyPI.
- **Must degrade gracefully.** If a plugin raises an exception, the deliberation continues. If a plugin package is not installed, the orchestrator warns and proceeds.
- **Must separate concerns.** The core engine handles orchestration (phases, rounds, agents). Plugins handle analysis (scoring, prediction, optimization). Templates handle presentation (agent prompts, output format).

---

## 10. Two-Plugin Architecture

### Plugin Tier 1: conversus-embeddings (Semantic Analysis)

Lightweight, runs locally, no cloud dependencies. Uses open embedding models from the MTEB leaderboard.

**Capabilities:**

| Feature | How | Value |
|---------|-----|-------|
| Semantic stagnation | Cosine similarity of agent positions between rounds > 0.95 → stagnant | More reliable than heading counting |
| Convergence scoring | Embed all agents' final positions, measure cluster tightness | Continuous 0-1 score vs binary "disputes remain" |
| Cross-round drift | Embed each round's synthesis, plot trajectory | "Is the deliberation circling or converging?" |
| Agreement clustering | Cluster agent positions, identify factions | "Which agents agree? Where are the fault lines?" |
| Position novelty | Compare Round N position against all prior rounds | "Did this round add anything new?" |

**Hook points:** POST_PHASE_5 (per-round analysis), POST_DELIBERATION (final scoring).

### Plugin Tier 2: conversus-nashopt (Game Engine)

Heavy, requires JAX + numerical libraries. Provides mathematical proof of outcome quality.

**Capabilities:**

| Feature | How | Value |
|---------|-----|-------|
| Equilibrium verification | Compute best-responses, check if any agent can improve | "Is this outcome provably stable?" |
| Convergence prediction | gnep-learn surrogate models from Round 1 data | "Will Round 2 converge? Save tokens if not" |
| Config optimization | nash_mpqp parametric solver over config space | "Optimal rounds/agents/mode for this problem" |
| Objective function construction | Symbolic logic + LLM-guided gap-filling (see Section 11) | "Build a mathematical game from natural language" |
| Scenario replay | Stored objective functions re-parameterized with new data | "Run the same decision framework on PR #2 that you used for PR #1" |

**Hook points:** PRE_EXECUTION (config optimization, scenario loading), POST_PHASE_5 (convergence prediction, equilibrium scoring), POST_DELIBERATION (final verification, scenario storage).

---

## 11. Objective Function Construction

This is the core R&D challenge: turning natural-language problem descriptions into mathematical objective functions that nashopt can optimize. Three approaches, used in combination.

### Approach 1: Structured Extraction (Deterministic)

When deliberation artifacts follow conversus template structure, extraction is deterministic:

```
Phase 3 revision artifact:
  "Recommendation 3: [Original: Add caching]
   Disposition: Withdrawn
   Explanation: Blue's defense demonstrated..."

Extracted state:
  agent.recommendations[3].status = WITHDRAWN  → x[3] = 0
  agent.recommendations[3].original_priority = P1  → weight[3] = 3
```

The template structure IS the schema. Every conversus artifact has predictable sections, headings, and formats. Regex + structured parsing handles 80% of feature extraction with zero LLM cost.

**What this produces:** State vectors — where each agent stands on each issue.

### Approach 2: Symbolic Logic Templates (Semi-Deterministic)

Objective functions for game theory have known mathematical forms. Instead of generating J(x) from scratch, we provide **objective function templates** — parameterized symbolic forms that the user fills in.

```yaml
# Objective function template: competitive-selection
# Use when: agents are competing alternatives (WTA mode)
form: |
  J_i(x) = -w_i * score_i(x) + penalty * overlap(x_i, x_{-i})
parameters:
  w_i:
    description: "How much does winning matter to agent i?"
    type: float
    range: [0, 1]
    default: 1.0
  score_i:
    description: "Agent i's quality score as assessed by cross-review"
    type: function
    derived_from: "synthesis recommendation scorecard"
  penalty:
    description: "Cost of overlapping with other agents' positions"
    type: float
    range: [0, 10]
    default: 1.0
  overlap:
    description: "Degree to which agent i's proposal conflicts with others"
    type: function
    derived_from: "cross-review contradiction count"
```

**Library of objective function templates:**

| Template | Mode | Form | Parameters |
|----------|------|------|------------|
| `competitive-selection` | WTA | J = -w·score + penalty·overlap | score from synthesis, overlap from contradictions |
| `cooperative-integration` | Cooperative | J = -accepted_recs + λ·unresolved_disputes | recommendation acceptance rate, dispute penalty |
| `territory-claiming` | PD | J = territory_held - γ·overreach_penalty | claimed vs contested territory |
| `risk-assessment` | RB | J_red = -confirmed_risks; J_blue = -mitigated_risks | risk severity vectors |
| `budget-constrained` | Any | J = quality - β·agent_cost | quality score, per-agent token cost |

These templates are stored in `schema/objectives/` alongside the variable schema from spec 005.

### Approach 3: LLM-Guided Gap-Filling (Interactive)

When a user describes a problem in natural language, the system uses symbolic logic to parse what it can, then uses an LLM to ask targeted questions to fill gaps.

**The pipeline:**

```
User: "We need to decide between Redis and Postgres for caching.
       Redis is faster but costs more. Postgres is already deployed."

Step 1: Symbolic parsing (deterministic)
  - Decision type: selection (detected: "decide between X and Y")
  - Agents: [redis-advocate, postgres-advocate] (detected: alternatives)
  - Constraints: cost, speed, deployment (detected: "faster", "costs more", "already deployed")
  - Objective template: competitive-selection (matched: selection type)

Step 2: Identify gaps (symbolic logic)
  - w_i (winning weight): not specified → needs user input
  - score_i: can be derived from deliberation, but need scoring criteria
  - penalty: not specified → use default
  - Missing: relative importance of speed vs cost vs deployment ease

Step 3: LLM asks targeted questions (interactive)
  "I've identified this as a competitive selection between Redis and Postgres.
   To build the objective function, I need:
   1. How important is speed vs cost? (e.g., 'speed is 3x more important than cost')
   2. Is there a hard budget constraint? (e.g., 'must stay under $500/month')
   3. How much should deployment complexity factor in? (e.g., 'critical' or 'nice to have')"

Step 4: User provides answers
  "Speed is twice as important as cost. Budget must stay under $200/month.
   Deployment complexity is critical — we ship next week."

Step 5: Construct objective function (deterministic)
  J_redis(x) = -(2.0 * speed_score + 1.0 * cost_score + 3.0 * deployment_score)
             + penalty * overlap(x_redis, x_postgres)
  subject to: monthly_cost(x) ≤ 200

Step 6: Store as reusable scenario (see Section 12)
```

**Key insight:** The LLM doesn't generate the objective function. It asks questions whose answers parameterize a known mathematical form. The symbolic logic determines WHAT to ask. The LLM determines HOW to ask it (natural language). The math determines what to DO with the answers.

This keeps objective function construction deterministic and reproducible while making it accessible to non-mathematicians.

### Approach 4: Embedding-Assisted Feature Mapping

For features that can't be extracted structurally (e.g., "how strongly does this agent feel about this recommendation?"), embeddings provide a continuous signal:

1. Embed the agent's argument text for each recommendation
2. Compute semantic intensity (distance from neutral/withdrawn language)
3. Map to a scalar weight in the objective function

This bridges the gap between structured extraction (binary: withdrawn/surviving) and the continuous payoff values nashopt needs.

---

## 12. Scenario Storage and Replay

### The Problem

A team runs a conversus deliberation to decide the caching strategy for PR #1. The objective function captures: speed weight = 2.0, cost weight = 1.0, deployment weight = 3.0, budget ≤ $200/month. The deliberation produces a good outcome.

Three weeks later, PR #2 introduces a different caching decision. The team wants to use the SAME decision framework (weights, constraints, mode, agent structure) but with DIFFERENT data (new proposals, new benchmarks, new cost estimates).

Today, they'd have to reconfigure everything from scratch. With scenario storage, they load the prior scenario and just swap the data.

### Scenario Object

```yaml
# Stored in: scenarios/{scenario-id}.yml or a database
scenario:
  id: caching-decision-2026-03
  name: "Caching Strategy Selection"
  created: 2026-03-20
  last_used: 2026-03-20

  # Game structure (reusable)
  mode: winner-take-all
  objective_template: competitive-selection
  parameters:
    speed_weight: 2.0
    cost_weight: 1.0
    deployment_weight: 3.0
    budget_constraint: 200
  agent_structure:
    - role: advocate
      perspective: "speed-optimized solution"
    - role: advocate
      perspective: "cost-optimized solution"
    - role: advocate
      perspective: "deployment-optimized solution"
  rounds: 3
  stagnation: detect
  arbiter:
    grounding_type: "project requirements document"
    trigger: disputes_remain

  # Data bindings (swappable)
  data_bindings:
    target: null           # user provides at runtime
    agent_docs: null       # user provides at runtime
    grounding_doc: null    # user provides at runtime

  # History
  runs:
    - date: 2026-03-20
      target: "specs/caching-v1/spec.md"
      outcome: "Redis selected"
      equilibrium_score: 0.91
      rounds_used: 2
      agents_launched: 29
```

### Replay Workflow

```
User: /conversus replay caching-decision-2026-03 --target specs/caching-v2/spec.md

System: Loading scenario "Caching Strategy Selection" (last used 2026-03-20)
  Mode: winner-take-all
  Agents: 3 (speed-optimized, cost-optimized, deployment-optimized)
  Objective: competitive-selection (speed=2.0, cost=1.0, deployment=3.0, budget≤$200)
  Rounds: 3, stagnation: detect

  New target: specs/caching-v2/spec.md
  Previous run selected Redis with equilibrium score 0.91.

  Do you want to:
  1. Run with same parameters (recommended)
  2. Adjust parameters before running
  3. View previous run's results first

User: 1

System: [runs full deliberation with stored config + new target data]
```

### Storage Options

| Option | When | How |
|--------|------|-----|
| **File-based** (default) | Small teams, single repo | `scenarios/{id}.yml` in project directory |
| **Database** | Enterprise, cross-team | PostgreSQL/SQLite with scenario + run history tables |
| **API** | SaaS product | REST API: `POST /scenarios`, `GET /scenarios/{id}/replay` |

The file-based option ships first. Database and API are future tiers.

### Cross-Run Analysis

With multiple runs of the same scenario stored, the system can answer:

- "How consistent are outcomes across different data?" (stability analysis)
- "Did the team's weighting preferences drift over time?" (parameter evolution)
- "Which scenarios produce the most agent-efficient deliberations?" (cost optimization)
- "Do certain problem structures always stagnate?" (structural analysis)

This data feeds back into the convergence predictor and config optimizer — more scenario history = better predictions.

---

## 13. Open Questions

1. **Should plugin recommendations be surfaced in the conversus report (Step 5)?** If an equilibrium scorer says quality is 0.4, should the report include that? Or is it only in `plugins/` output?

2. **Should the convergence predictor be allowed to STOP a deliberation?** If it predicts with 95% confidence that Round 3 will stagnate, should the engine skip Round 3 automatically? Or always defer to the user?

3. **Should the config optimizer run automatically in the decision framework (spec 002/999)?** When a user runs `/conversus mode`, should the optimizer automatically recommend config if the plugin is installed?

4. **Pricing model:** Per-run credit? Monthly subscription? Per-plugin? Free for open-source projects?

5. **Data collection:** Should the free tier anonymously collect deliberation metadata (agent count, round count, convergence rate) to train the paid tier's models? Opt-in? Opt-out?

6. **Objective function template library — open or curated?** Should third parties contribute objective function templates (like presets), or should they be curated to maintain mathematical validity?

7. **Scenario storage — git-tracked or database?** File-based scenarios are git-friendly but don't scale for cross-team enterprise use. At what point does the transition to database storage happen?

8. **LLM-guided gap-filling — which model?** Should the objective function construction use the same model as the deliberation agents, or a cheaper model since it's just asking structured questions?

9. **Embedding model selection — bundled or user-configured?** Should conversus-embeddings ship with a specific MTEB model, or let users configure their own? Bundled is simpler; configurable supports domain-specific models.

10. **Scenario replay across teams — shared scenarios?** Can team A publish their "code review decision framework" scenario for team B to use? This implies a scenario marketplace or registry.

---

## Appendix A: Reference Libraries

All by Alberto Bemporad (IMT Lucca), Apache 2.0:

| Library | Purpose | Conversus Use |
|---------|---------|---------------|
| [nashopt](https://github.com/bemporad/nashopt) | GNE computation via KKT + JAX autodiff. Main/consolidated library. | Equilibrium verification, best-response computation |
| [gnep-learn](https://github.com/bemporad/gnep-learn) | Active learning of best-response models via Kalman filtering | Convergence prediction from partial deliberation data |
| [nash_mpqp](https://github.com/bemporad/nash_mpqp) | Parametric GNE solver for quadratic objectives | Config optimization over parameter ranges |
| [jax-gnep](https://github.com/bemporad/jax-gnep) | Deprecated — merged into nashopt | N/A |

### Key Concept Mapping

| nashopt Concept | Conversus Analog | Bridge |
|----------------|-----------------|--------|
| Agent objective J(x) | Agent identity prompt + docs | Feature extraction: text positions → payoff vectors |
| Best response f(x_{-i}) | Agent's revision after cross-reviews | Feature extraction: concession patterns → response functions |
| Nash equilibrium | All agents stop disputing | Equilibrium scorer: mathematical verification of convergence quality |
| Parametric game parameter p | Config values (rounds, iterations, mode) | Config optimizer: optimize parameters for minimum agent launches |
| Coupled constraints g(x) ≤ 0 | Shared target document constraints | Constraint extraction from problem definition |
| KKT stationarity | Phase 4 with 0 remaining disputes | Stationarity check: can any agent improve by changing position? |

### Data Pipeline

```
Deliberation Artifacts (markdown)
        ↓
Feature Extraction (text → vectors)
        ↓
Game Model Construction (vectors → J(x), constraints)
        ↓
nashopt Analysis (equilibrium, best-response, parametric)
        ↓
Plugin Output (scores, predictions, recommendations)
        ↓
User Decision (act on recommendations or ignore)
```
