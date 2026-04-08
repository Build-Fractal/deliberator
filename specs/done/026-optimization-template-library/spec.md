# Feature Specification: Optimization Template Library Expansion

**Feature ID**: `026-optimization-template-library`
**Created**: 2026-03-27
**Status**: Draft
**Depends On**: `013-objective-function-templates` (existing templates), `023-ampl-config-optimizer` (AMPL solver), `025-game-form-expansion` (new game forms)
**Origin**: Research — MIP problem classes mapped to conversus deliberation modes

---

## 1. Feature Summary

Add ~15 new objective function templates covering standard optimization problem classes: assignment, scheduling, portfolio, network flow, facility location, knapsack, set cover, and multi-criteria optimization. Each template bridges a real-world problem type to the AMPL solver via the construction pipeline.

---

## 2. New Templates

### Assignment Problems
- **assignment-optimal**: Minimize total cost of assigning N agents to M tasks. Binary MIP.
- **assignment-balanced**: Minimize max load across agents (load balancing). Minimax MIP.

### Scheduling
- **scheduling-precedence**: Minimize makespan with task dependencies. MIP with precedence constraints.
- **scheduling-resource**: Schedule tasks with shared resource constraints. MIP with capacity.

### Portfolio / Selection
- **portfolio-markowitz**: Maximize return minus risk (mean-variance). QP.
- **portfolio-robust**: Minimize worst-case loss. Minimax LP.

### Network Flow
- **network-min-cost**: Minimize transport cost through a network. LP.
- **network-max-flow**: Maximize flow from source to sink. LP.

### Facility Location
- **facility-location**: Minimize total cost of opening facilities + serving demand. Binary MIP.

### Knapsack / Packing
- **knapsack-binary**: Maximize value subject to weight capacity. Binary MIP.
- **knapsack-multi**: Multiple knapsacks (bin packing). MIP.

### Set Cover
- **set-cover**: Minimize cost of covering all elements. Binary MIP.

### Multi-Criteria (completing existing set)
- **epsilon-constraint**: Optimize one objective, constrain others. LP/MIP.
- **goal-programming**: Minimize deviation from target goals. LP.
- **pareto-frontier**: Enumerate Pareto-optimal solutions. Iterative LP.

### New Constraint Templates
- **integrality**: Variable must be integer.
- **cardinality**: At most K variables can be non-zero.
- **precedence**: Task A must complete before task B starts.
- **flow-conservation**: Flow in = flow out at each node.

---

## 3. Functional Requirements

- **FR-001**: Each template MUST follow the existing YAML schema with `name`, `description`, `form`, `game_form`, `mode_compatibility`, `parameters`, `constraints`, `example`.
- **FR-002**: Each template MUST include `gap_question` fields for ALL non-derived parameters.
- **FR-003**: Templates MUST validate against the `ObjectiveTemplate` Pydantic model.
- **FR-004**: The decision type classifier (spec 014 Stage 1) MUST be updated to route new problem types to new templates.
- **FR-005**: New constraint templates MUST validate against the `ConstraintTemplate` Pydantic model.
- **FR-006**: Each template MUST have an `example` section with realistic parameter values.

---

## 4. Success Criteria

- **SC-001**: `len(objective_templates) >= 35` after implementation.
- **SC-002**: `len(constraint_templates) >= 10` after implementation.
- **SC-003**: The construction pipeline (spec 014) can route "assign my team to projects" to `assignment-optimal`.
- **SC-004**: Every template's `example` produces a valid `AssembledObjective`.
- **SC-005**: Every new template is solvable by AMPL/HiGHS (verified by model generation test).
