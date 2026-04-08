# Phase 1 Review: optimization-engineer

**Spec**: 019-config-optimizer
**Reviewer**: optimization-engineer
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Evaluate the quality model, grid search coverage, diminishing returns curves, and infeasibility detection.

---

## Quality Model (`_quality_score`)

### Diminishing Returns Curves

The quality model uses three exponential saturation curves:
- **Rounds**: `1 - exp(-0.8 * rounds)` -- steeper curve, rounds matter most early.
- **Agents**: `1 - exp(-0.5 * (agent_count - 1))` -- gentler curve, 1 agent = no debate (offset by 1).
- **Iterations**: `1 - exp(-0.7 * iterations)` -- moderate curve.

These are combined via weighted geometric mean: `round^0.40 * agent^0.35 * iter^0.25`.

**Analysis**:

1. **Curve shape**: Exponential saturation `1 - exp(-k*x)` is a standard diminishing-returns model. It starts at 0 (x=0) and asymptotically approaches 1. The rate parameter `k` controls how quickly it saturates. For rounds (k=0.8): 1 round = 0.55, 2 rounds = 0.80, 3 rounds = 0.91, 5 rounds = 0.98. This means most quality gain is in the first 2-3 rounds, which aligns with typical deliberation behavior.

2. **Agent offset**: `agent_count - 1` is correct because 1 agent contributes zero diversity. With 2 agents: 0.39, 3 agents: 0.63, 5 agents: 0.86, 10 agents: 0.99. The curve saturates more slowly than rounds, reflecting that agent diversity has longer-tail benefits.

3. **Weighted geometric mean**: This penalizes weakness in any dimension while rewarding balance. A config with 5 rounds but 2 agents and 1 iteration will score lower than 3 rounds, 3 agents, 2 iterations. This is a desirable property -- balanced configs are preferred.

**Assessment**: Well-designed quality model. The curves are reasonable for a heuristic, the weighting reflects domain knowledge (rounds > agents > iterations), and the geometric mean prevents degenerate configs.

### Quality Range

Tests verify quality is always in [0.0, 1.0] for the full search space. The minimal config (1 round, 2 agents, 1 iter) gives ~0.19. The maximal config (5 rounds, 10 agents, 3 iters) gives ~0.93. Quality never reaches 1.0, which is intentional -- perfect quality is asymptotic.

**Concern**: The quality threshold of 1.0 is unreachable, which the test `test_very_high_quality_threshold_infeasible` verifies. However, the infeasibility message says "quality threshold {threshold} is unreachable" without explaining why. A user asking for quality=0.99 would get infeasible even with unlimited budget, which may be confusing.

---

## Grid Search Coverage

### Search Space

```
rounds:      1..5         (5 values)
iterations:  1..3         (3 values)
agent_count: 2..max_agents (up to 9 values with max_agents=10)
```

Total grid points: 5 * 3 * 9 = 135 at max. This is small enough for exhaustive enumeration. No heuristic pruning needed.

### Search Strategy

Exhaustive enumeration with:
1. Skip configs exceeding budget.
2. Skip configs below quality threshold.
3. Among feasible configs, maximize quality.
4. Break ties by minimizing cost.

**Assessment**: The strategy is correct for a small grid. It guarantees optimality within the discrete search space. The time complexity is O(5 * 3 * max_agents) which is negligible.

### Missing Dimension: Mode

The spec's Section 2 lists `mode` as a decision variable with values {cooperative, wta, pd, rb}. The implementation does NOT search over modes. It uses the state's current mode as context but does not recommend a mode. FR-009 requires `recommended_mode` in the output, but the implementation omits this field.

**Assessment**: Significant omission. The spec envisions the optimizer recommending which mode to use, but the implementation only optimizes rounds, iterations, and agent count within a fixed mode.

---

## Cost Model (`_total_launches`)

Delegates to `engine.cost.estimate_cost(agent_count, iterations, has_arbiter)` for per-round cost, then multiplies by rounds.

```python
per_round = estimate_cost(agent_count, iterations, has_arbiter)
launches_per_round = sum(per_round.values())
return launches_per_round * rounds
```

This is correct: total cost scales linearly with rounds, each round having the same phase pipeline cost. The test `test_known_value` verifies: 3 agents, 1 iteration, 1 round = 16 (3 + 6 + 3 + 3 + 1). The arbiter test verifies +1 per round.

**Assessment**: Correct and well-tested. Using the canonical engine cost formula ensures consistency.

---

## Infeasibility Detection

Two infeasibility cases:
1. **Budget too low for quality**: The grid search tracks `min_budget_for_quality` (cheapest config meeting quality threshold). If no config fits both budget and quality, reports the minimum budget needed.
2. **Quality unreachable**: If no config in the search space meets the quality threshold regardless of budget, reports that the threshold is unreachable.

Both cases produce clear reasoning strings with actionable information.

**Assessment**: Well-implemented. The dual-path infeasibility (budget-constrained vs. quality-unreachable) is a good design.

---

## Missing Features

### AMPL Integration (FR-006, FR-007)

The spec envisions MIP formulation using AMPL with HiGHS solver. The implementation uses grid search. The code has comments marking AMPL integration points but no AMPL code exists. FR-017 allows heuristic fallback when AMPL is unavailable, so the grid search serves as the fallback.

### Solver Configuration (FR-007, FR-018)

No solver configuration (HiGHS, Gurobi, timeout). The grid search has no solver concept.

### General-Purpose Optimization (FR-014, FR-015)

No general-purpose `solve()` API or custom model support. The implementation is config-specific.

---

## Summary

| Area | Verdict |
|------|---------|
| Quality model curves | Well-designed diminishing returns |
| Weighted geometric mean | Correct, rewards balance |
| Grid search coverage | Complete for 3 dimensions |
| Mode as decision variable | Missing from search |
| Cost model | Correct, uses canonical formula |
| Infeasibility detection | Well-implemented, dual-path |
| AMPL integration | Not implemented |
| General-purpose optimization | Not implemented |

### Key Issues

1. **Mode not searched**: Spec requires `recommended_mode` but implementation does not search modes.
2. **AMPL not implemented**: Grid search is the fallback, but the primary method is absent.
3. **FR-009 missing `recommended_mode`**: Output lacks this required field.
4. **General-purpose solve() API missing**: FR-014/FR-015 not implemented.
