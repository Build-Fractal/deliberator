# Cross-Review: spec-compliance reviewing optimization-engineer

**Spec**: 026-optimization-template-library

---

## Agreement

The optimization-engineer's mathematical review provides the domain expertise needed to validate formulation correctness. I agree that:

- All formulations are mathematically valid for their problem class
- Parameters are reasonable with appropriate ranges
- Examples are feasible instances
- PSD validation is correctly identified as a solver-time concern

## Disagreements

### Concern #1 (PSD validation) should not even be Low

The optimization-engineer rates the covariance PSD concern as Low. I think it should be **Info only**. The template schema is a declarative specification, not a solver input validator. PSD checking requires numerical linear algebra (eigenvalue decomposition or Cholesky factorization), which is firmly in solver territory. The template description correctly documents the PSD requirement as a note, which is sufficient at this layer.

### Concern #2 (supply_demand sum-to-zero) -- same argument

Network flow feasibility (supply equals demand) is a constraint that the solver should enforce, not the template schema. The template correctly declares `flow-conservation` as a constraint reference.

## Additions

I note that the optimization-engineer did not assess whether the templates are mutually consistent -- i.e., whether two templates could produce conflicting constraint sets for the same problem type. This is unlikely given the clean separation of problem classes, but would be worth checking in an integration review with the construction pipeline.
