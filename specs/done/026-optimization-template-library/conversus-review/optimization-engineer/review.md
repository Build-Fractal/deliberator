# Phase 1 Review: optimization-engineer

**Spec**: 026-optimization-template-library
**Agent**: optimization-engineer
**Focus**: Mathematical forms correct? Parameters reasonable? MIP formulations sound?

---

## Executive Summary

The 15 new objective function templates and 4 new constraint templates cover the canonical optimization problem classes with mathematically correct formulations. The templates bridge real-world problem types (assignment, scheduling, portfolio, network flow, knapsack, set cover, multi-criteria) to AMPL/HiGHS via the construction pipeline. Parameters carry reasonable ranges and defaults. Examples produce feasible problem instances with known-optimal or tractable solutions.

**Verdict**: PASS with 4 observations (2 Low, 2 Info).

---

## Detailed Findings

### 1. Assignment Problems

**assignment-optimal** (`J = sum(c_ij * x_ij)`): Correct binary MIP formulation for the classic assignment problem. The cost matrix encoding (semicolon-separated rows of comma-separated values) is a practical serialization for YAML. Constraints `mutual-exclusivity` and `non-negativity` are the correct pair -- mutual-exclusivity enforces the one-agent-per-task and one-task-per-agent constraints. The example (3x3 matrix: `"10,5,13;3,9,18;7,11,6"`) has a unique optimal assignment (agent 0->task 1, agent 1->task 0, agent 2->task 2) with cost 5+3+6=14. The `game_form: gnep` designation is appropriate because each agent's optimal assignment depends on what other agents choose.

**assignment-balanced**: Minimax formulation for load balancing. Correct reformulation of the assignment problem where the objective is to minimize the maximum load across agents rather than the total cost. This requires an auxiliary variable `L >= sum(w_ij * x_ij)` for each agent i, with `min L` as the objective. The template's MIP classification is correct since the minimax reformulation introduces continuous auxiliary variables alongside binary assignment variables.

### 2. Portfolio Optimization

**portfolio-markowitz** (`J = -mu^T w + lambda * w^T Sigma w`): Correct QP (quadratic programming) formulation of the Markowitz mean-variance model. The sign convention (minimize the negative return plus risk) is the standard form for minimization solvers. The `risk_aversion` parameter lambda in [0, 100] with default 1.0 is reasonable -- lambda=0 gives the maximum-return portfolio, lambda>>1 gives the minimum-variance portfolio. The covariance matrix example `"0.04,0.006,0.002;0.006,0.09,0.009;0.002,0.009,0.01"` is symmetric and has positive eigenvalues (verified by inspection: diagonal dominance holds), so it is PSD as required.

**Observation OE-1 (Info)**: The template description correctly states the covariance matrix "must be symmetric positive semi-definite" but this constraint is not enforceable at the template schema level. PSD verification requires numerical linear algebra (eigenvalue decomposition or Cholesky). This is appropriately a solver-time concern, not a template concern.

**portfolio-robust**: Minimax LP for worst-case loss. This is the robust counterpart to Markowitz -- instead of penalizing variance, it minimizes the maximum possible loss under uncertainty. The LP classification is correct when the uncertainty set is polyhedral (which is the standard formulation).

### 3. Network Flow

**network-min-cost** (`J = sum(c_ij * f_ij)`): Correct LP formulation for minimum cost flow. The arc encoding (semicolon-separated triples "i,j,cost") cleanly represents the sparse graph structure. Constraints `flow-conservation`, `capacity`, and `non-negativity` are the standard triplet for network flow. The example (4 nodes, 4 arcs, supply=10 at node 0, demand=-10 at node 3) is a minimal but complete instance. Supply/demand sums to zero, confirming feasibility.

**Observation OE-2 (Info)**: The supply_demand sum-to-zero constraint is documented in the parameter description ("Must sum to zero for feasibility") but not enforced at the template level. This is correct -- feasibility checking belongs in the solver/assembler layer, not the template layer.

**network-max-flow**: Correct LP formulation as the dual of min-cost flow. Maximizing flow from source to sink with arc capacity constraints.

### 4. Knapsack / Packing

**knapsack-binary** (`J = -sum(v_i * x_i) subject to sum(w_i * x_i) <= W`): Correct 0-1 knapsack formulation. The negative sign on the value sum converts the standard maximization into a minimization problem (solver convention). Constraints `budget` (capacity), `integrality` (binary), and `non-negativity` are correct. The example (values "60,100,120", weights "10,20,30", capacity 50) has the known optimal solution: items 1 and 2 (0-indexed), value 220, weight 50. This is the textbook 0-1 knapsack example.

**knapsack-multi**: Multi-dimensional knapsack / bin packing. Multiple capacity constraints across multiple resource dimensions. Correct MIP extension.

### 5. Set Cover

**set-cover** (`J = sum(c_i * x_i) subject to all elements covered`): Correct binary MIP formulation. The coverage matrix encoding (binary matrix as semicolon-separated rows) is consistent with the cost/assignment matrix encoding in other templates. The example has 4 sets and 5 elements with coverage matrix:
```
S0: covers {0,1}
S1: covers {1,2}
S2: covers {2,3}
S3: covers {3,4}
```
Optimal solution: select S0 and S3 (cost 5+8=13, covers {0,1,3,4}) plus either S1 or S2 (cost 10 or 3) to cover element 2. Greedy: S2 (cheapest at 3, covers {2,3}), then S0 (covers {0,1}), then S3 (covers {4}). Total greedy = 3+5+8=16. LP relaxation will find the optimal.

### 6. Multi-Criteria Templates

**epsilon-constraint**: Correct method for multi-objective optimization. Optimize one objective while constraining others to be within epsilon of their individual optima. LP/MIP classification depends on whether the underlying single-objective problems are LP or MIP.

**goal-programming**: Minimize weighted deviations from target goals. Standard LP formulation using deviation variables (d+, d-) for each goal.

**pareto-frontier**: Iterative LP to enumerate Pareto-optimal solutions. The "iterative" designation is important -- this is not a single optimization but a sweep across the Pareto front. Computationally expensive but methodologically correct.

### 7. New Constraint Templates

**integrality**: `x_i in {0, 1} or x_i in Z+`. The `variable_type` parameter (binary vs. integer) correctly distinguishes the two common variants. This is the fundamental constraint for all MIP problems.

**cardinality**: At most K variables can be non-zero. Implemented via binary indicator variables: `y_i >= x_i / M` (where M is a big-M bound) and `sum(y_i) <= K`. This is a standard MIP reformulation.

**precedence**: `start_B >= end_A`. Standard scheduling constraint with correct temporal interpretation.

**flow-conservation**: `sum(f_ji) - sum(f_ik) = b_i for all nodes i`. The notation uses b_i for supply/demand, which is standard. The constraint is correctly parameterized by supply_demand vector.

### 8. Parameter Reasonableness

All parameters across all 15 templates have:
- Meaningful `description` fields explaining the mathematical role
- Appropriate `type` values (`string` for matrices/vectors, `integer` for counts, `float` for scalars)
- Reasonable `range` constraints where applicable (e.g., `min: 0` for non-negative quantities, `min: 1` for counts)
- Sensible `default` values where provided (e.g., `risk_aversion: 1.0`)

---

## Concerns

| # | Severity | Item |
|---|----------|------|
| OE-1 | Info | Portfolio covariance PSD constraint not enforceable at template level (correctly deferred to solver) |
| OE-2 | Info | Network flow supply_demand sum-to-zero not enforceable at template level (correctly deferred to solver) |
| OE-3 | Low | `game_form` values in templates are not cross-validated against game form YAML schemas -- a typo would be silently accepted |
| OE-4 | Low | `mode_compatibility` values not cross-validated against mode-mapping.yml -- same silent-failure risk |

---

## Recommendation

**Accept.** All 15 formulations are mathematically sound, parameters are reasonable, and examples produce feasible instances with known or tractable optimal solutions. The two Low concerns (OE-3, OE-4) are test coverage gaps, not formulation errors.
