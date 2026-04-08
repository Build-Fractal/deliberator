# Feature Specification: Equilibrium Scorer Plugin (nashopt)

**Feature ID**: `017-equilibrium-scorer`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `015-feature-extraction` (extracted feature vectors), `016-plugin-system` (Plugin base class, lifecycle hooks, output namespace)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 4: Equilibrium Scoring, FR-013). First paid plugin in the conversus-nashopt package.

---

## 1. Feature Summary

The equilibrium scorer computes a Nash equilibrium quality score for a completed (or in-progress) deliberation. It answers the question: "Is this outcome stable? Could any agent have done better by changing position?"

For each agent, given all other agents' final positions, the scorer checks whether that agent could improve its payoff by changing its own position. If no agent can improve, the outcome is a Nash equilibrium. The score is the ratio of agents at equilibrium to total agents.

This is the first paid plugin. It hooks into POST_DELIBERATION (final score) and POST_PHASE_5 (per-round score), consuming extracted features (spec 015) and computing equilibrium quality via nashopt's `check_equilibrium()`.

**What changes**: New `conversus-nashopt` package with `EquilibriumScorer` plugin class. New `plugins/equilibrium-score.json` output.

**What does not change**: Core deliberation. Template system. All changes are in the plugin namespace.

---

## 2. Payoff Functions Per Mode

The scorer needs a payoff function for each agent to check equilibrium. These are derived from the objective function templates (spec 013), instantiated with extracted features (spec 015).

### Cooperative

`J_i = recommendations_accepted_in_synthesis`

Agent i's payoff is the count of their recommendations that survived to the final synthesis. An agent at equilibrium cannot get more recommendations accepted by changing position.

### Winner-Take-All

`J_i = 1 if winner, 0 otherwise`

Binary payoff. The winner has no incentive to change; losers cannot improve by unilateral deviation (the synthesis already ranked them). Score is typically 1.0 or 0.0 (all at equilibrium or the loser could have won by changing strategy).

### Prisoners Dilemma

`J_i = territory_held - gamma * overreach_penalty`

Agent i's payoff is claimed territory minus penalty for overreach (claiming territory another agent also claims and defends). Gamma is configurable (default: 1.0).

### Red-Blue

`J_red = sum(severity * confirmed_findings)`
`J_blue = sum(severity * mitigated_findings)`

Red's payoff is total severity of confirmed risks. Blue's payoff is total severity of mitigated risks. Adversarial: red wants to maximize unmitigated risk, blue wants to maximize mitigation.

---

## 3. Functional Requirements

### Plugin Registration

- **FR-001**: The plugin MUST register as `equilibrium-scorer` with hooks `[POST_PHASE_5, POST_DELIBERATION]`.
- **FR-002**: The plugin MUST be part of the `conversus-nashopt` package, installable via `pip install conversus-nashopt`.

### Equilibrium Computation

- **FR-003**: The scorer MUST extract features from the deliberation state using the `conversus-features` API (`extract_features()` or pre-computed `features.json`).
- **FR-004**: The scorer MUST construct per-agent payoff functions based on the deliberation mode, using the payoff definitions in Section 2.
- **FR-005**: The scorer MUST use nashopt's `check_equilibrium()` to verify whether each agent is at a best response given others' positions.
- **FR-006**: The equilibrium quality score MUST be computed as: `agents_at_equilibrium / total_agents`, producing a float in [0.0, 1.0].

### Output

- **FR-007**: The plugin MUST produce `plugins/equilibrium-score.json` containing:
  - `score`: float 0.0-1.0
  - `agents_at_equilibrium`: integer count
  - `total_agents`: integer count
  - `per_agent`: dict mapping agent name to `{at_equilibrium: bool, payoff: float, best_response_payoff: float}`
  - `mode`: string
  - `round`: integer (for POST_PHASE_5)
  - `hook`: string identifying which hook produced this result
- **FR-008**: At POST_PHASE_5, the output filename MUST include the round number: `equilibrium-score-round-{N}.json`.
- **FR-009**: The `recommendation` field of `PluginResult` MUST include a plain-language interpretation: "Equilibrium quality: 0.85 -- 5 of 6 agents are at best response. Agent 'cost-advocate' could improve by conceding on recommendation #3."

### Configuration

- **FR-010**: Plugin config MUST support a `threshold` field (float, default 0.85) indicating the minimum acceptable equilibrium quality score.
- **FR-011**: When the score is below threshold, the recommendation MUST note this and suggest actions (e.g., "Consider another round or arbitration to improve equilibrium quality").

### Error Handling

- **FR-012**: If feature extraction fails (no `features.json`, malformed output), the plugin MUST return a PluginResult with `data: {error: "..."}` and `advisory: True`. No crash.
- **FR-013**: If nashopt computation fails (numerical issues, singular matrices), the plugin MUST catch the exception and report a partial result with available information.

---

## 4. Success Criteria

- **SC-001**: Given a cooperative deliberation where all agents' recommendations are accepted in synthesis, the equilibrium score is 1.0 (all at best response).
- **SC-002**: Given a cooperative deliberation where one agent could have gotten more recommendations accepted, the score is less than 1.0, and that agent is identified in `per_agent`.
- **SC-003**: The scorer produces meaningful score differentiation between a fully-converged outcome and a disputed outcome from the same deliberation.
- **SC-004**: `pip install conversus-nashopt` installs nashopt, jax, scipy, and conversus-features as dependencies. No manual dependency management.
- **SC-005**: A conversus run with the equilibrium scorer configured produces identical core output plus `plugins/equilibrium-score.json`.

---

## 5. Constraints

- **Must NOT modify core deliberation output.** The scorer writes to `plugins/` only.
- **Must NOT block deliberation on computation failure.** Equilibrium computation can fail (numerical issues, incomplete features). The plugin degrades gracefully.
- **Must NOT make scoring authoritative.** The score is advisory. The user decides whether to act on it. No automatic round termination or config changes based on the score.
- **Must NOT bundle nashopt in the free core.** nashopt, jax, and scipy are dependencies of `conversus-nashopt` (paid), not of the core engine or `conversus-plugins`.
