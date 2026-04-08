# Feature Specification: Convergence Predictor Plugin (nashopt)

**Feature ID**: `018-convergence-predictor`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `015-feature-extraction` (extracted feature vectors), `016-plugin-system` (Plugin base class, lifecycle hooks), `017-equilibrium-scorer` (ships in same `conversus-nashopt` package, shares payoff function definitions)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 4: Convergence Prediction, FR-014, decision Q2: recommend-then-confirm stop authority).

---

## 1. Feature Summary

The convergence predictor answers the question: "Should I spend tokens on another round?" After each round's synthesis, it predicts whether the next round will reduce disputes, estimates how many rounds remain until convergence, and provides a confidence level.

The method uses gnep-learn's active learning approach: build linear surrogate models of each agent's best-response function via Kalman filtering, then check whether those models have a fixed point. If a fixed point exists, convergence is predicted. If not, stagnation is predicted and the system recommends arbitration or stopping.

This is decision support, not automation. Per decision Q2, the predictor recommends then confirms: on stagnation prediction, the engine pauses and prompts the user to cancel or continue. Future evolution: auto-cancel (opt-out via `auto_stop: false`) once prediction accuracy is proven.

**What changes**: New `ConvergencePredictor` plugin class in `conversus-nashopt`. New `plugins/convergence-prediction-round-{N}.json` output.

**What does not change**: Core deliberation. Round termination logic. Template system.

---

## 2. Prediction Method

### Input

Feature vectors from the current round and all prior rounds (spec 015). Minimum input: Round 1 features. More rounds improve prediction accuracy.

### Process

1. For each agent, collect position vectors across rounds: `x_i^{(1)}, x_i^{(2)}, ..., x_i^{(r)}`
2. Build a linear surrogate model of each agent's best-response function using Kalman filtering (gnep-learn's approach): `x_i^{(r+1)} = A_i * x_{-i}^{(r)} + b_i + noise`
3. The surrogate models form a system of linear equations. Check for a fixed point: a state where all agents' best responses map to the current state.
4. If a fixed point exists within the feasible region, predict convergence and estimate rounds remaining based on the distance from current state to fixed point.
5. If no fixed point exists (or the fixed point is outside feasible bounds), predict stagnation.

### Output

- `prediction`: one of `converge`, `stagnate`, `uncertain`
- `confidence`: float 0.0-1.0 (higher with more rounds of data)
- `estimated_rounds_remaining`: integer (when prediction is `converge`), null otherwise
- `reasoning`: plain-language explanation

---

## 3. Functional Requirements

### Plugin Registration

- **FR-001**: The plugin MUST register as `convergence-predictor` with hook `[POST_PHASE_5]`.
- **FR-002**: The plugin MUST ship as part of the `conversus-nashopt` package alongside the equilibrium scorer (spec 017).

### Prediction Logic

- **FR-003**: After Round 1, the predictor MUST produce a prediction based on single-round features. Confidence is low (0.3-0.5 range) with only one data point.
- **FR-004**: After Round 2+, the predictor MUST use cross-round feature trajectories to build surrogate models via Kalman filtering.
- **FR-005**: The predictor MUST report `uncertain` when confidence is below a configurable threshold (default: 0.5). No false certainty.
- **FR-006**: Estimated rounds remaining MUST be computed from the convergence rate (distance reduction per round to the fixed point). If the rate is zero or negative, report stagnation.

### Decision Support

- **FR-007**: When prediction is `stagnate` with confidence above threshold, the `recommendation` MUST suggest concrete actions: "Stagnation predicted (confidence: 0.78). Consider: (1) triggering arbitration, (2) adjusting agent configuration, (3) stopping and using current synthesis."
- **FR-008**: When prediction is `converge`, the recommendation MUST include estimated cost: "Convergence predicted in ~2 rounds (confidence: 0.82). Estimated additional agent launches: 14."
- **FR-009**: The predictor MUST NOT automatically stop rounds or trigger arbitration. It is advisory only (per decision Q2 and Constitution Principle XV).

### Output

- **FR-010**: The plugin MUST produce `plugins/convergence-prediction-round-{N}.json` containing:
  - `prediction`: string (`converge`, `stagnate`, `uncertain`)
  - `confidence`: float 0.0-1.0
  - `estimated_rounds_remaining`: integer or null
  - `current_round`: integer
  - `dispute_trajectory`: list of dispute counts per round
  - `position_drift`: float measuring total position movement this round
  - `fixed_point_exists`: boolean
  - `reasoning`: string

### Configuration

- **FR-011**: Plugin config MUST support:
  - `min_confidence`: float (default 0.5) -- minimum confidence to report a definitive prediction
  - `auto_stop`: boolean (default false) -- reserved for future autonomous mode; when true, stagnation prediction above confidence threshold triggers automatic stop recommendation

### Error Handling

- **FR-012**: If feature extraction provides insufficient data (e.g., only one agent), the predictor MUST return `uncertain` with an explanatory message.
- **FR-013**: If gnep-learn's Kalman filter fails to converge, the predictor MUST fall back to simple heuristics (dispute count trajectory: increasing = stagnate, decreasing = converge).

---

## 4. Success Criteria

- **SC-001**: Given a 2-round deliberation where disputes decreased from 5 to 2, the predictor predicts `converge` with reasonable confidence.
- **SC-002**: Given a 2-round deliberation where disputes increased from 3 to 5, the predictor predicts `stagnate`.
- **SC-003**: After Round 1 only, the predictor returns a prediction with confidence below 0.6 (acknowledging limited data).
- **SC-004**: The predictor's `estimated_rounds_remaining` is within +/-1 of actual rounds needed on test data.
- **SC-005**: A stagnation prediction includes actionable suggestions (arbitration, config change, stop).

---

## 5. Constraints

- **Must NOT automatically stop deliberation.** The predictor advises; the user decides. `auto_stop` is reserved for future autonomous mode and defaults to false.
- **Must NOT modify core round logic.** The predictor reads deliberation state and produces advisory output. Round termination remains in the core engine.
- **Must NOT require more than Round 1 data.** The predictor works with any number of rounds, though accuracy improves with more data.
- **Must NOT depend on libraries beyond nashopt/gnep-learn ecosystem.** Uses gnep-learn for Kalman-filtered surrogate models, which is already a nashopt ecosystem dependency.
