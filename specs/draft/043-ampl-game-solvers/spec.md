# Feature Specification: AMPL Game-Theoretic Solvers

**Feature ID**: `043-ampl-game-solvers`
**Created**: 2026-04-03
**Status**: Draft
**Depends On**: `023-ampl-config-optimizer` (DONE — existing AMPL integration), `039-new-mode-payoffs` (DONE — all 8 modes have payoff functions), `021-nashopt-integration` (DONE — equilibrium scorer)
**Docs Update**: New docs/developer-guide/game-solvers.md; update docs/api/plugins/nashopt.md with AMPL solver path; update docs/user-guide/modes.md with exact vs heuristic scoring
**Origin**: Honest analysis of conversus-ampl revealed the current integration is shallow. The real value is formalizing game theory as optimization models — not for "better math" but for **consistent, tunable agent behavior**.

---

## 1. Core Thesis: Natural Language Game Theory Enforced with Optimization Modeling

Conversus runs natural-language deliberations structured by game theory. Agents argue, cross-review, revise, and converge — all driven by prompts and templates. The problem: **AI agents are stochastic. The same deliberation with the same prompts produces different results every time.**

Optimization modeling solves this by creating a **formal enforcement layer** between the game theory and the agent output:

```
Natural Language          Optimization Model          Agent Behavior
─────────────────    →    ──────────────────    →    ───────────────
"cooperative mode"        maximize welfare            Consistent scoring
"find common ground"      subject to fairness         Tunable parameters
"penalize overreach"      gamma * penalty <= threshold  Reproducible across runs
```

The bidirectional flow:

1. **NL → Optimization**: Game forms (cooperative, WTA, PD, etc.) translate to formal models (LP, MIP, QP). The model parameters (`gamma`, severity weights, fairness thresholds) are the mathematical expression of what the natural-language prompts describe qualitatively.

2. **Optimization → NL**: Model parameters become tuning knobs that control agent behavior deterministically. Change `gamma` from 1.0 to 0.5 → agents tolerate more overreach. Adjust severity weights → defense priorities shift. Same features + same parameters = same score, every run.

**The heuristics are fine.** They implement the optimization model implicitly. Making the model explicit means:
- **Consistency**: Deterministic scores stabilize agent output across runs
- **Tunability**: Adjust parameters to refine behavior without editing prompts
- **Reproducibility**: Same features + same model = same result (auditable)
- **Interpretability**: Parameters have documented semantics ("gamma controls overreach tolerance")

This is the key component in getting consistent output from agents. Not better math — **stable math that humans can tune**.

---

## 2. What Changes (and What Doesn't)

The existing heuristic payoff functions (spec 039) are preserved unchanged. They are the zero-dependency fallback and they work. This spec adds a formal optimization layer that:

- Expresses each heuristic as an explicit optimization problem with named parameters
- Solves the optimization via AMPL/HiGHS when available
- Exposes parameters for user tuning
- Falls back to heuristics when AMPL is unavailable

The three-tier fallback: AMPL (formal model) → nashopt (exact equilibrium on heuristic payoffs) → heuristic (approximate). All three produce the same interface: `(payoff, best_response_payoff)`.

---

## 3. Game-Theoretic Formulations by Mode

### 3.1 Cooperative Mode — Nash Equilibrium (LP)

**Current heuristic:** `J_i = surviving_count`. Best response = max surviving across agents.

**What's wrong:** `surviving_count` measures acceptance, not equilibrium. Two agents can both have high surviving counts while being far from equilibrium (e.g., both survived because the synthesizer was permissive, not because their positions were strategically sound).

**AMPL formulation:** Mixed-strategy Nash equilibrium as a linear program.

Given the agreement/dispute matrix from features, construct a normal-form payoff matrix where:
- `u[i][j]` = payoff to agent i when agents play strategy profile j
- Strategies = "maintain position" or "concede on disputed points"

The LP finds mixed strategies `p[i][action]` such that no agent can improve their expected payoff by unilaterally changing strategy.

```ampl
param n_agents;
param n_actions;
param u{1..n_agents, 1..n_actions, 1..n_actions};

var p{i in 1..n_agents, a in 1..n_actions} >= 0;
var v{i in 1..n_agents};

maximize social_welfare: sum{i in 1..n_agents} v[i];

subject to probability{i in 1..n_agents}:
    sum{a in 1..n_actions} p[i,a] = 1;

subject to best_response{i in 1..n_agents, a in 1..n_actions}:
    sum{k in 1..n_actions} u[i,a,k] * p[-i,k] <= v[i];
```

**Payoff extraction:** `equilibrium_payoff[i] = v[i]` from the LP solution.

**Solve time:** <50ms for n<=10.

---

### 3.2 Winner-Take-All Mode — Tournament Resolution (MIP)

**Current heuristic:** `J_i = 1 if ranking_position == 1 else 0`.

**What's wrong:** The ranking comes from feature extraction, not from solving the tournament. Score differentials can be inconsistent (A beats B, B beats C, C beats A — Condorcet cycle). The heuristic can't resolve cycles.

**AMPL formulation:** Tournament ranking as a MIP that maximizes consistency with observed score differentials while enforcing transitivity.

```ampl
param n_agents;
param score_diff{i in 1..n_agents, j in 1..n_agents};

var wins{i in 1..n_agents, j in 1..n_agents: i != j} binary;
var rank{i in 1..n_agents} integer >= 1 <= n_agents;

maximize consistency:
    sum{i in 1..n_agents, j in 1..n_agents: i != j}
        wins[i,j] * score_diff[i,j];

subject to antisymmetry{i in 1..n_agents, j in 1..n_agents: i < j}:
    wins[i,j] + wins[j,i] = 1;

subject to rank_ordering{i in 1..n_agents, j in 1..n_agents: i != j}:
    rank[i] <= rank[j] - 1 + n_agents * (1 - wins[i,j]);

subject to unique_ranks{i in 1..n_agents, j in 1..n_agents: i < j}:
    rank[i] != rank[j];
```

**Payoff extraction:** `rank[i]` from the MIP. Winner = agent with rank 1.

**Solve time:** <100ms for n<=10.

---

### 3.3 Prisoners-Dilemma Mode — Dominant Strategy (LP)

**Current heuristic:** `J_i = territory_held - gamma * overreach_penalty`.

**What's wrong:** The heuristic penalizes overreach but doesn't determine whether cooperation or defection is the dominant strategy for each agent. In the real PD, the equilibrium (mutual defection) is suboptimal — the interesting question is HOW suboptimal, which requires solving the game.

**AMPL formulation:** N-player PD with territory and overreach as the payoff structure. Compute the Nash equilibrium (typically mutual defection) and the cooperative optimum (mutual cooperation). The gap between them measures the "price of anarchy."

```ampl
param n_agents;
param territory{i in 1..n_agents};
param shared{i in 1..n_agents};
param overreach_penalty{i in 1..n_agents};
param gamma;

var cooperate{i in 1..n_agents} binary;
var payoff{i in 1..n_agents};

# Payoff depends on own and others' cooperation
subject to payoff_def{i in 1..n_agents}:
    payoff[i] = territory[i]
        + shared[i] * (sum{j in 1..n_agents: j != i} cooperate[j]) / (n_agents - 1)
        - gamma * overreach_penalty[i] * (1 - cooperate[i]);
```

Solve twice: once maximizing social welfare (cooperative optimum), once finding Nash equilibrium (each agent's best response given others). Price of anarchy = cooperative welfare / equilibrium welfare.

**Solve time:** <50ms for n<=10.

---

### 3.4 Red-Blue Mode — Minimax Equilibrium (LP)

**Current heuristic:** Red: `severity * confirmed_ratio`. Blue: `severity * mitigated_ratio`.

**What's wrong:** The ratios are observed outcomes, not equilibrium strategies. The heuristic can't answer "what's the BEST red could do against OPTIMAL blue defense?" — which is the question that matters for security assessment.

**AMPL formulation:** Zero-sum game solved as a minimax LP. Red allocates attack resources across severity levels; blue allocates defense resources. The minimax value is the guaranteed outcome for each side.

```ampl
param n_levels;
param severity{k in 1..n_levels};
param red_budget;
param blue_budget;

var a_red{k in 1..n_levels} >= 0;
var a_blue{k in 1..n_levels} >= 0;
var game_value;

minimize worst_case_for_blue: game_value;

subject to red_alloc: sum{k in 1..n_levels} a_red[k] <= red_budget;
subject to blue_alloc: sum{k in 1..n_levels} a_blue[k] <= blue_budget;

subject to minimax{k in 1..n_levels}:
    game_value >= severity[k] * (a_red[k] - a_blue[k]);
```

**Payoff extraction:** `game_value` is the minimax equilibrium. Red's guaranteed payoff = game_value. Blue's guaranteed defense = -game_value.

**Solve time:** <50ms for n_levels<=20.

---

### 3.5 Fair-Division Mode — Envy-Free Allocation (MIP)

**Current heuristic:** `J_i = proportionality_score - (envy_count / (N-1))`.

**What's wrong:** The heuristic counts envy but doesn't compute the envy-free allocation. It measures a symptom (envy exists) without providing the cure (what allocation would eliminate envy).

**AMPL formulation:** Envy-free allocation as a MIP. Each recommendation is an "item" to be allocated to an agent. Each agent has a valuation for each item (derived from review scores). The MIP finds an allocation where no agent prefers another's bundle.

```ampl
param n_agents;
param n_items;
param value{i in 1..n_agents, j in 1..n_items};

var x{i in 1..n_agents, j in 1..n_items} binary;

maximize total_welfare:
    sum{i in 1..n_agents, j in 1..n_items} value[i,j] * x[i,j];

subject to each_item{j in 1..n_items}:
    sum{i in 1..n_agents} x[i,j] = 1;

subject to envy_free{i in 1..n_agents, k in 1..n_agents: i != k}:
    sum{j in 1..n_items} value[i,j] * x[i,j]
    >= sum{j in 1..n_items} value[i,j] * x[k,j];
```

**Payoff extraction:** `x[i,j]` is the allocation. `bundle_value[i]` = agent i's total value. Envy-freeness verified as a constraint satisfaction result.

**Solve time:** <500ms for n<=10, items<=50.

---

### 3.6 Resource-Allocation Mode — Maximin Fair Share (LP)

**Current heuristic:** `J_i = utilization_efficiency - allocation_inequality`.

**What's wrong:** Efficiency minus inequality is a useful metric but doesn't compute what each agent's fair share IS. The Shapley value (each agent's marginal contribution) is the game-theoretic answer.

**AMPL formulation:** Two-part:
1. **Maximin allocation** (LP): Maximize the minimum payoff across agents
2. **Shapley value** (Python enumeration): Compute each agent's fair contribution by averaging marginal contributions over all orderings

```ampl
# Part 1: Maximin LP
param n_agents;
param total_resource;
param efficiency{i in 1..n_agents};

var alloc{i in 1..n_agents} >= 0;
var min_payoff;

maximize fairness: min_payoff;

subject to budget: sum{i in 1..n_agents} alloc[i] <= total_resource;
subject to min_def{i in 1..n_agents}:
    efficiency[i] * alloc[i] >= min_payoff;
```

Shapley value is computed in Python (O(2^n) coalition evaluations, feasible for n<=10).

**Solve time:** LP <50ms. Shapley enumeration <200ms for n<=10.

---

### 3.7 Negotiation Mode — Nash Bargaining (NLP) [DEFERRED]

**Formulation:** Maximize product of utility gains (Nash bargaining solution). Requires ZOPA bounds and reservation prices from features.

**Deferred because:** Current feature extraction provides `zopa_coverage` (scalar) but not the per-agent ZOPA bounds needed to parameterize the model. Requires feature schema updates.

**When ready:** Log-transform converts the product to a sum of logs → convex optimization solvable by Ipopt or scipy.

---

### 3.8 Mechanism-Design Mode — VCG Auction (MIP) [DEFERRED]

**What VCG does:** The Vickrey-Clarke-Groves mechanism ensures truthful reporting is the dominant strategy. It works by:

1. **Allocation:** Solve a welfare-maximizing MIP (allocate recommendations to maximize total value across all agents)
2. **Pricing:** For each agent i, solve the same MIP WITHOUT agent i. Agent i's "tax" = welfare of others without i minus welfare of others with i. This makes truthful reporting optimal because your bid affects only the ALLOCATION, not your PAYMENT.

**Conversus application:**
- Agents "bid" on recommendations via review scores (higher score = higher valuation)
- VCG allocates attention/priority to maximize total welfare
- `gaming_vulnerability_count` = number of recommendations where an agent could profitably misreport
- `incentive_compatibility` = fraction of recommendations where truthful reporting is dominant

**AMPL formulation:**

```ampl
# Winner determination (solve N+1 times for VCG)
param n_agents;
param n_items;
param value{i in 1..n_agents, j in 1..n_items};
param exclude_agent default 0;  # 0 = include all; k = exclude agent k

var x{i in 1..n_agents, j in 1..n_items} binary;

maximize social_welfare:
    sum{i in 1..n_agents, j in 1..n_items: i != exclude_agent}
        value[i,j] * x[i,j];

subject to each_item{j in 1..n_items}:
    sum{i in 1..n_agents: i != exclude_agent} x[i,j] <= 1;
```

VCG payment for agent i = `welfare_without_i - (welfare_with_all - payoff_to_i)`.

**Deferred because:** Mapping review scores to valuations requires domain assumptions. Need to define what a "bid" means in the context of spec review — is it severity? priority? confidence?

**When ready:** The MIP is straightforward. The feature extraction is the hard part.

---

## 4. Architecture

### Integration with Existing Pipeline

```
RoundFeatures (from spec 015 extraction)
    │
    ├── [AMPL available?]
    │   ├── YES → ampl_game_solver.solve(mode, features)
    │   │         → exact equilibrium / allocation / minimax value
    │   │         → payoff from solution concept
    │   │
    │   └── NO → [nashopt available?]
    │            ├── YES → nashopt.check_equilibrium(payoff_matrix)
    │            │         → exact equilibrium check on heuristic payoffs
    │            │
    │            └── NO → heuristic payoff functions (current)
    │                     → approximate scores
    │
    └── EquilibriumScorer.score() → [0.0, 1.0]
```

Three-tier fallback: AMPL (exact game solver) → nashopt (exact equilibrium on heuristic payoffs) → heuristic (approximate).

### File Structure

```
conversus/plugins/
├── nashopt/
│   ├── scorer.py        (existing — dispatches to solver tiers)
│   ├── solver.py        (existing — nashopt wrapper)
│   ├── payoffs.py       (existing — heuristic payoff functions)
│   └── game_solvers/    (NEW)
│       ├── __init__.py
│       ├── base.py      (BaseSolver protocol + registry)
│       ├── cooperative.py
│       ├── winner_take_all.py
│       ├── prisoners_dilemma.py
│       ├── red_blue.py
│       ├── fair_division.py
│       └── resource_allocation.py
└── optimizer/
    ├── ampl_model.py    (existing — config optimization, stays as-is)
    └── ampl_solver.py   (existing — config dispatch)
```

### BaseSolver Protocol

```python
class GameSolver(Protocol):
    """Interface for mode-specific AMPL game solvers."""

    mode: str  # e.g., "cooperative"

    def build_game(self, features: RoundFeatures) -> dict:
        """Extract game structure from features.

        Returns AMPL parameter dict ready for solve().
        """
        ...

    def solve(
        self, features: RoundFeatures, timeout: int = 10,
    ) -> GameResult | None:
        """Solve the game and return the solution.

        Returns None if AMPL unavailable or infeasible (triggers fallback).
        """
        ...

    def extract_payoffs(
        self, result: GameResult, agent_name: str,
    ) -> tuple[float, float]:
        """Extract (payoff, best_response_payoff) from solution.

        Same interface as heuristic payoff functions.
        """
        ...
```

### GameResult

```python
@dataclass(frozen=True)
class GameResult:
    """Result from an AMPL game solver."""
    mode: str
    solution_concept: str   # "nash_equilibrium", "minimax", "envy_free", etc.
    solve_time_ms: float
    solver_status: str      # "optimal", "feasible", "infeasible"
    payoffs: dict[str, float]           # agent_name → payoff
    best_responses: dict[str, float]    # agent_name → best response payoff
    metadata: dict                      # solver-specific (strategies, allocations, etc.)
```

---

## 5. Scorer Integration

The EquilibriumScorer (`scorer.py`) currently dispatches to nashopt or heuristic. Add AMPL as the highest-priority tier:

```python
def _compute_score(self, features, mode):
    # Tier 1: AMPL game solver (exact solution concept)
    if HAS_AMPL:
        solver = GAME_SOLVER_REGISTRY.get(mode)
        if solver:
            result = solver.solve(features, timeout=self.solver_timeout)
            if result:
                return self._score_from_game_result(result)

    # Tier 2: nashopt (exact equilibrium on heuristic payoffs)
    if HAS_NASHOPT:
        return self._score_from_nashopt(features, mode)

    # Tier 3: heuristic payoffs
    return self._score_from_heuristic(features, mode)
```

The `PluginResult.data["solver"]` field reports which tier ran: `"ampl-{mode}"`, `"nashopt"`, or `"heuristic"`.

---

## 6. Functional Requirements

### Solver Framework
- **FR-001**: Each mode-specific solver MUST implement the `GameSolver` protocol.
- **FR-002**: Solvers MUST return `None` when AMPL is unavailable (triggering fallback).
- **FR-003**: Solvers MUST respect the configurable timeout (default 10s).
- **FR-004**: Solver results MUST include `solve_time_ms` for performance tracking.

### Game Formulations
- **FR-005**: Cooperative solver MUST compute mixed-strategy Nash equilibrium.
- **FR-006**: Red-blue solver MUST compute minimax equilibrium value.
- **FR-007**: Prisoners-dilemma solver MUST compute dominant strategy equilibrium AND cooperative optimum (for price-of-anarchy reporting).
- **FR-008**: Winner-take-all solver MUST resolve Condorcet cycles via consistency maximization.
- **FR-009**: Fair-division solver MUST compute envy-free allocation when one exists, or report infeasibility.
- **FR-010**: Resource-allocation solver MUST compute maximin fair share allocation.

### Fallback Chain
- **FR-011**: AMPL failure MUST fall through to nashopt, then heuristic. No exceptions.
- **FR-012**: The heuristic payoff functions (spec 039) MUST NOT be modified by this spec.
- **FR-013**: `PluginResult.data["solver"]` MUST report which tier ran.

### Validation
- **FR-014**: Each solver MUST have unit tests against known game-theoretic results (e.g., PD has known Nash equilibrium of mutual defection).
- **FR-015**: Each solver MUST validate post-solve that the solution satisfies the claimed solution concept (e.g., verify no agent can profitably deviate from Nash equilibrium).

---

## 7. Success Criteria

- **SC-001**: Cooperative mode with AMPL produces a Nash equilibrium score that differs from heuristic by >5% on at least one test case (proving it's not just replicating the heuristic).
- **SC-002**: Red-blue mode with AMPL produces a minimax value that correctly identifies which severity levels are "worth attacking" and "worth defending."
- **SC-003**: Fair-division mode with AMPL produces an envy-free allocation when one exists (verified by constraint satisfaction).
- **SC-004**: All 6 Phase 1+2 solvers pass tests against canonical game theory results.
- **SC-005**: Fallback chain works: AMPL → nashopt → heuristic with no behavioral change when AMPL is unavailable.
- **SC-006**: Solver adds <500ms per mode on average for n<=10 agents.

---

## 8. Phasing

### Phase 1: Foundation + 3 solvers (~2 weeks)
1. Create `game_solvers/` directory with `BaseSolver` protocol and registry
2. Implement cooperative solver (LP Nash equilibrium)
3. Implement red-blue solver (LP minimax)
4. Implement prisoners-dilemma solver (LP + cooperative optimum)
5. Integrate into EquilibriumScorer as Tier 1
6. Tests against canonical game theory results
7. Docs: game-solvers.md developer guide

### Phase 2: 2 more solvers (~3 weeks)
8. Implement winner-take-all solver (MIP tournament)
9. Implement fair-division solver (MIP envy-free)
10. Performance benchmarks for MIP modes
11. Optional Gurobi auto-detection for large instances

### Phase 3: Deferred solvers (post feature-extraction improvements)
12. Negotiation solver (NLP Nash bargaining) — needs ZOPA bounds in features
13. Mechanism-design solver (MIP VCG) — needs review-score-to-valuation mapping
14. Resource-allocation Shapley value computation

---

## 9. Constraints

- AMPL/HiGHS remain optional runtime dependencies — never core requirements.
- Heuristic payoff functions (spec 039) are preserved unchanged as the zero-dependency fallback.
- The existing config optimizer (spec 023) is unmodified — it's a separate concern.
- Game solver models are AMPL strings embedded in Python (not .mod files) for portability.
- All solvers use HiGHS as the default. Gurobi/Ipopt are optional upgrades documented in README.
- The `conversus-nashopt` pip package will include the game solvers (they're part of the premium solver tier).

---

## 10. Open Questions

1. **Payoff matrix construction from features:** The quality of AMPL solutions depends entirely on the payoff matrix extracted from features. Should this spec also define improved feature extraction, or rely on existing features?
   - **Lean:** Use existing features. Document assumptions. Improved extraction is a separate spec.

2. **Multi-objective for PD mode:** Computing both Nash equilibrium AND cooperative optimum requires solving the game twice. Is the "price of anarchy" metric worth the extra solve?
   - **Lean:** Yes — it's the most interesting output of PD mode. 2x solve time is still <100ms.

3. **Envy-free infeasibility:** Not all allocation problems have envy-free solutions. When infeasible, should the solver find the "least envious" allocation?
   - **Lean:** Yes — minimize total envy as a soft constraint. Report infeasibility + best-effort allocation.

4. **User control:** Should users be able to force a specific solver tier (e.g., "always use heuristic" even when AMPL is available)?
   - **Lean:** Yes — add `solver_tier: "ampl" | "nashopt" | "heuristic" | "auto"` to plugin config. Default "auto" uses the fallback chain.
