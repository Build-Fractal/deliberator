# Cross-Review: spec-compliance reviewing optimization-engineer

**Spec**: 027-solver-validation-flow
**Reviewer**: spec-compliance
**Subject**: optimization-engineer Phase 1 review
**Round**: 1

---

## Verified Claims

### 1. AMPL feedback loop finding is the strongest cross-agent consensus

The optimization-engineer's finding that `constraint_additions` as `list[str]` cannot satisfy FR-010 is mathematically precise. The example showing the gap between natural-language constraints and AMPL syntax is compelling:

```
Natural language: "Add capacity constraint: sum(x[i]) <= 10"
AMPL syntax:      "subject to total_capacity: sum {i in ITEMS} x[i] <= 10;"
```

From a compliance perspective, this confirms my assessment of FR-010 as PARTIALLY MET. However, after reviewing the optimization-engineer's argument, I am now inclined to revise FR-010 to NOT MET. The "data structure exists" reasoning I used is too generous when the spec says "MUST be consumable by the solver."

### 2. RHS vs. cost sensitivity distinction is valid

The optimization-engineer correctly identifies that sensitivity analysis has two distinct regimes (constraint RHS perturbation vs. objective coefficient perturbation) with different mathematical properties. The sensitivity instructions treat them identically. This does not change my FR-004/FR-005 compliance assessment (both are MET at the structural level) but it indicates the sensitivity analysis is less rigorous than it appears.

### 3. Problem type to agent mapping analysis is thorough

The optimization-engineer's verification of each implemented mapping (general, assignment, portfolio) against standard optimization domain knowledge is more detailed than my compliance check. The mapping is substantively correct for the implemented types.

---

## Disagreements

### 1. "Cannot catch local optima" is out of scope for this spec

The optimization-engineer lists five categories of solver issues the validation flow cannot catch: local optima, numerical infeasibility, degeneracy, solver parameter sensitivity, and basis transitions. While technically accurate, the spec does not claim to catch these issues. The spec's stated purpose is: "solvers give you an answer, conversus tells you if you should trust it."

The "trust" assessment is multi-perspective (fairness, robustness, constraint satisfaction) -- not numerical/algorithmic. The validation flow is a qualitative review layer, not a solver verification tool. Criticizing it for not detecting basis transitions is like criticizing a code review for not catching compiler bugs.

**Severity assessment**: The optimization-engineer rates this as MEDIUM. I rate it as INFO -- it is a valid observation about the flow's limitations but not a gap against the spec's requirements.

### 2. Shadow price extraction is aspirational, not required

The optimization-engineer proposes that the validation flow should accept solver output that includes dual values and surface them to agents. This is a good design suggestion but:
- No FR or SC requires dual value extraction
- The spec's input is "solution.yml" which is undefined in content
- Dual values are solver-specific (HiGHS format differs from Gurobi format differs from AMPL)

The absence of dual value extraction is not a compliance gap. It is a design improvement that could strengthen FR-004 satisfaction but is not required by it.

### 3. Missing 4th agent severity: agree with MEDIUM but for different reasons

The optimization-engineer flags the missing robustness tester for assignment problems (spec table shows 4 agents, implementation has 3). I agree with MEDIUM severity but my reasoning is different:

- **optimization-engineer's reasoning**: The robustness tester role is functionally important because no other assignment agent covers robustness analysis.
- **My reasoning**: The spec table is the closest thing to a normative reference for problem type agents. Deviating from it without documentation creates a spec-implementation mismatch that makes compliance assessment ambiguous.

The compliance implication is the same: the implementation deviates from the spec's documented expectations. Whether this is a functional gap (optimization-engineer) or a documentation gap (spec-compliance), it should be resolved.

---

## Additions

### FR-010 revision: NOT MET

After reviewing the optimization-engineer's argument, I am revising my FR-010 assessment from PARTIALLY MET to NOT MET. The reasoning:
- FR-010 uses "MUST be consumable by the solver for re-optimization"
- "Consumable" means the output can be directly used, not that a human can interpret it
- `list[str]` with natural-language descriptions is not consumable by any solver
- The data structure's existence does not constitute partial consumability

This changes my summary from 4 PARTIALLY MET to 3 PARTIALLY MET and 4 NOT MET.

### The optimization-engineer identifies a spec gap, not just an implementation gap

The structured constraint template proposal (`ConstraintAddition` with type, expression, parameters, ampl_template) reveals that the spec itself underspecifies the feedback loop. FR-010 says "consumable by the solver" but does not define a constraint interchange format. This is a spec-level issue that should be addressed in spec amendment, not just implementation.

### Cross-reference to spec dependencies

The optimization-engineer's findings about equilibrium scoring and convergence prediction align with the spec header's "Depends On" list: spec 021 (nashopt-integration) and spec 022 (convergence predictor). The validation flow cannot achieve full FR satisfaction without these dependencies being implemented. The spec should clarify whether FR-006, FR-007, and FR-012 are blocked-on-dependency or expected-in-this-spec.
