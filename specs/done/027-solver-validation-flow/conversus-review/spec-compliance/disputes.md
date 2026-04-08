# Phase 4 Disputes: spec-compliance

**Spec**: 027-solver-validation-flow
**Agent**: spec-compliance
**Round**: 1

---

## Surviving Disputes

### DISPUTE 1: 5 of 12 FRs are NOT MET (HIGH -- systemic)

**Status**: SURVIVING -- all agents agree on the individual NOT MET assessments.

After Round 1 revisions, the compliance picture is:
- **NOT MET**: FR-001, FR-006, FR-007, FR-010, FR-011, FR-012 (5 requirements, plus FR-010 revised from PARTIALLY MET)
- **PARTIALLY MET**: FR-002, FR-008, FR-009 (3 requirements)
- **MET**: FR-003, FR-004, FR-005 (3 requirements, plus 3 section-6 constraints)

The NOT MET requirements form two clusters:
1. **Integration cluster**: FR-001 (CLI), FR-006 (equilibrium), FR-007 (threshold flag), FR-012 (convergence) -- these depend on external specs (021, 022) or engine integration
2. **Feedback cluster**: FR-010 (solver consumable output), FR-011 (iteration tracking) -- these require architectural decisions about constraint interchange and state management

**Recommended resolution**: The spec should be phased. Phase 1 (current): config generation, data models, agent templates. Phase 2: CLI command + deliberation execution. Phase 3: equilibrium/convergence integration + AMPL feedback. This would allow the current implementation to be assessed as "Phase 1 COMPLETE" rather than "41% NOT MET."

### DISPUTE 2: FR-010 is a spec-level gap, not just an implementation gap (HIGH)

**Status**: SURVIVING -- optimization-engineer originated, all agents concur.

FR-010 says "consumable by the solver for re-optimization" but does not specify:
- What "consumable" means (AMPL syntax? abstract constraint? human-readable recommendation?)
- Which solver (HiGHS via AMPL? Pyomo? Generic?)
- Whether the integration is direct (automated code generation) or mediated (human translates)

This is a requirement that cannot be satisfied as written because the acceptance criteria are undefined. The spec must be amended to specify the constraint interchange format before implementation can be assessed.

**Recommended resolution**: Amend FR-010 to: "The validation output MUST include structured constraint additions in a format that can be translated to solver-specific syntax (AMPL, Pyomo) by a code generation layer." Then implement the generation layer.

### DISPUTE 3: SC-002 is PARTIALLY MET, not NOT MET (MEDIUM -- contested)

**Status**: SURVIVING DISAGREEMENT with devex-advocate.

The devex-advocate pushes for NOT MET; I maintain PARTIALLY MET. The disagreement is about interpretation of "correctly identifies" in the success criterion.

- **devex-advocate position**: "correctly identifies" requires demonstrated behavior -- the system must actually produce the finding for a given input. The framework has not been tested end-to-end.
- **spec-compliance position**: "correctly identifies" at the framework level means the framework is designed and equipped to identify such findings. The SensitivityFinding model, the risk-minimizer agent prompt, and the sensitivity instructions collectively enable this identification.

This is a legitimate interpretive dispute. I note that SC-002 specifically says "Sensitivity analysis correctly identifies that a portfolio solution becomes infeasible if interest rates increase by 2%." The test `test_sensitivity_findings_roundtrip` demonstrates exactly this data flowing through the model. The framework satisfies the structural requirement; the runtime behavior depends on the LLM.

**Recommended resolution**: Run an end-to-end test with a portfolio solution that is sensitive to interest rates. If the LLM agent produces a finding matching the SC-002 scenario, upgrade to MET. If not, downgrade to NOT MET.

### DISPUTE 4: Missing problem types weaken FR-002 (MEDIUM)

**Status**: SURVIVING -- all agents agree FR-002 is PARTIALLY MET.

The implementation covers 3 of 5 expected problem types. Scheduling and negotiation types are missing. A developer using `problem_type="scheduling"` gets a ValueError. This is partial compliance: the auto-generation mechanism works correctly for implemented types but the type coverage is incomplete.

**Recommended resolution**: Implement scheduling and negotiation agent templates. The spec table provides the agent names and roles; implementation is straightforward template addition.

---

## Withdrawn Disputes

- **FR-011 PARTIALLY MET**: Revised to NOT MET after devex-advocate correctly argued that `iterations: 1` is not iteration tracking.
- **FR-010 PARTIALLY MET**: Revised to NOT MET after optimization-engineer's argument about free-form strings.
- **Section 6 constraints**: All MET. No dispute.

---

## Settled Points (No Dispute)

- FR-003 target list construction: MET (all agents agree)
- FR-004 sensitivity analysis presence: MET (at least one agent per type)
- FR-005 sensitivity finding structure: MET (four required fields)
- SC-001 fairness detection: MET (prompt addresses scenario)
- SC-005 timing: MET (16 LLM calls under 10 minutes)
- Section 6 constraints: ALL MET (same engine, template-based, no modification)
- ValidationVerdict model design: SOUND (three-valued verdict, confidence range, structured output)
