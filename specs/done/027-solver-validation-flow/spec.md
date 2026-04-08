# Feature Specification: Solver Validation Flow

**Feature ID**: `027-solver-validation-flow`
**Created**: 2026-03-27
**Status**: Draft
**Depends On**: `014-guided-objective-construction` (problem formulation), `016-plugin-system` (plugin hooks), `021-nashopt-integration` (equilibrium scoring), `023-ampl-config-optimizer` (AMPL solver)
**Origin**: Gap analysis — the missing loop that connects solver output back to multi-agent critique

---

## 1. Feature Summary

Close the optimization loop: after a solver produces a solution, run a conversus deliberation to validate it. Agents critique the solution from multiple perspectives, the equilibrium scorer assesses stability, and the user gets a solution + multi-perspective critique + stability score.

This is the key differentiator: **solvers give you an answer, conversus tells you if you should trust it.**

---

## 2. The Validation Loop

```
User describes problem
    ↓
/conversus define → problem.md
    ↓
/conversus mode → conversus.yml + objective.yml
    ↓
AMPL/HiGHS solves → solution.yml
    ↓
/conversus validate-solution → validation deliberation
    ↓  Agents review: Is this solution robust? Fair? Missing constraints?
    ↓  What happens if assumptions change? Who loses?
Equilibrium scorer → stability assessment
    ↓
User gets: solution + critique + stability score + sensitivity analysis
```

### New command: `/conversus validate-solution`

Input: `solution.yml` (solver output) + `problem.md` + `objective.yml`
Output: A deliberation where agents review the solution, not a proposal.

---

## 3. Agent Perspectives for Solution Validation

Auto-generated from the problem type:

| Problem Type | Agent 1 | Agent 2 | Agent 3 | Agent 4 |
|-------------|---------|---------|---------|---------|
| Assignment | Efficiency advocate | Fairness advocate | Robustness tester | Constraint auditor |
| Scheduling | Makespan optimizer | Resource utilizer | Risk assessor | Dependency checker |
| Portfolio | Return maximizer | Risk minimizer | Diversification advocate | Regulatory checker |
| Negotiation | Each party's advocate | Mediator | Legal reviewer | — |
| General | Optimality auditor | Sensitivity analyst | Constraint verifier | Stakeholder advocate |

---

## 4. Functional Requirements

### Solution Validation Command
- **FR-001**: `/conversus validate-solution <solution.yml>` MUST generate a validation conversus.yml and run a deliberation targeting the solution.
- **FR-002**: Agents MUST be auto-generated based on problem type with solution-critique prompts (not generic review prompts).
- **FR-003**: The validation deliberation MUST include the original problem.md, objective.yml, and solution.yml as target files.

### Sensitivity Analysis
- **FR-004**: At least one agent MUST perform sensitivity analysis: "What happens if parameter X changes by ±10%?"
- **FR-005**: Sensitivity findings MUST be structured: parameter name, change magnitude, impact on solution feasibility, impact on objective value.

### Equilibrium Integration
- **FR-006**: The equilibrium scorer (spec 021) MUST run POST_DELIBERATION on the validation output.
- **FR-007**: If equilibrium score < 0.7, the synthesis MUST flag the solution as potentially unstable.

### Output
- **FR-008**: The validation output MUST include a `validation-verdict.md` with: ACCEPT (solution is robust), REVISE (specific changes needed), REJECT (fundamental issues found).
- **FR-009**: Rejected or revised solutions MUST include specific constraint additions or parameter changes to improve the solution.
- **FR-010**: The validation output MUST be consumable by the solver for re-optimization (constraint feedback loop).

### Iteration
- **FR-011**: After validation, the user MAY run `/conversus validate-solution` again on a revised solution. Each iteration is tracked.
- **FR-012**: The convergence predictor (spec 022) MUST assess whether re-validation is likely to produce different results.

---

## 5. Success Criteria

- **SC-001**: Given an assignment solution that assigns the best engineer to the lowest-priority project, validation agents flag the fairness issue.
- **SC-002**: Sensitivity analysis correctly identifies that a portfolio solution becomes infeasible if interest rates increase by 2%.
- **SC-003**: A robust solution (all constraints satisfied with margin) receives ACCEPT verdict with equilibrium score > 0.8.
- **SC-004**: Validation output includes at least one specific constraint addition that, when added to the AMPL model, produces a better solution.
- **SC-005**: The full loop (define → formulate → solve → validate → revise → re-solve) completes in under 10 minutes for a 3-agent deliberation.

---

## 6. Constraints

- Validation deliberation uses the same engine as regular deliberation — no special execution path.
- Solution critique agents are auto-generated from templates, not hardcoded.
- The validation flow MUST NOT modify the original solution — it produces recommendations, not automatic changes.
