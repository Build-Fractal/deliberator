# Cross-Review: spec-compliance reviewing devex-advocate

**Spec**: 027-solver-validation-flow
**Reviewer**: spec-compliance
**Subject**: devex-advocate Phase 1 review
**Round**: 1

---

## Verified Claims

### 1. End-to-end gap identification is accurate and well-structured

The devex-advocate's decomposition of the missing steps (YAML writer, deliberation runner, output parser, AMPL feedback, convergence predictor) maps precisely to the NOT MET FRs in my compliance matrix. The finding is correctly rated HIGH.

### 2. problem_type as untyped string -- CONFIRMED

This aligns with FR-002's spirit. While the function works correctly for valid inputs, the lack of a type-safe enum means developers get no IDE assistance. The ValueError for unknown types is a runtime safety net, not a design-time guide.

### 3. Missing iteration tracking and equilibrium_score -- CONFIRMED

The devex-advocate correctly identifies that `ValidationVerdict` lacks fields for FR-011 (iteration tracking) and FR-006 (equilibrium score). These are not just DX issues -- they are compliance gaps. The model is structurally incomplete against the spec.

---

## Disagreements

### 1. Agent count deviation is not undocumented -- it is intentional scope reduction

The devex-advocate notes that "the spec's table shows a 4th agent column for some types" and the implementation uses 3 agents per type. The devex-advocate frames this as an "undocumented deviation."

I disagree with the characterization. The spec's section 3 table is illustrative -- the column headers say "Agent 1", "Agent 2", etc., and the negotiation row has a dash in Agent 4. The table shows possibilities, not requirements. FR-002 requires "auto-generated based on problem type" but does not mandate a specific count. The implementation chose 3 agents per type for consistency and cost control. This is a design decision, not a deviation.

However, I note that the spec table specifically names "Robustness tester" for assignment and "Dependency checker" for scheduling. If these types are implemented, the named agents should be included to match the spec's documented expectations.

### 2. Sensitivity instructions are not "LOW" -- they are MEDIUM at minimum

The devex-advocate rates "sensitivity instructions blur quantitative/qualitative analysis boundary" as LOW. From a compliance perspective, FR-004 requires sensitivity analysis, and FR-005 requires structured findings. The instructions direct agents to perform sensitivity analysis, but the devex-advocate correctly notes that LLM agents cannot compute exact perturbation impacts from static YAML.

This creates a compliance risk: the sensitivity findings will look structured (correct field names) but contain qualitative estimates rather than quantitative results. FR-005 says findings must include "impact on solution feasibility" and "impact on objective value." If these impacts are LLM guesses rather than solver-computed values, the findings are structurally compliant but substantively unreliable.

I rate this MEDIUM because it affects the trustworthiness of FR-004 and FR-005 satisfaction.

### 3. The redundant field_validator is not INFO -- it is a code quality issue worth flagging

The devex-advocate rates the redundant `confidence_in_range` validator as INFO. While it has no behavioral impact, redundant validation logic creates maintenance risk: a future developer might change the Field constraint without realizing the validator also enforces the same rule, or vice versa. In a compliance context, redundant enforcement is better than missing enforcement, but it signals imprecise implementation. I maintain this as INFO but note it should be cleaned up.

---

## Additions

### The devex-advocate's finding #6 (feasibility_impact as free-form string) has compliance implications

FR-005 says sensitivity findings must include "impact on solution feasibility." If `feasibility_impact` is a free-form string, agents could write "somewhat feasible" or "probably ok" or "uncertain." These satisfy the structural requirement (the field is populated) but not the informational requirement (the impact is clearly characterized). A constrained vocabulary (Literal["feasible", "infeasible", "marginal", "unknown"]) would ensure the field carries decision-relevant information.

### Missing assessment of spec section 2 (The Validation Loop)

The devex-advocate focuses on the implementation but does not assess whether the implementation matches the validation loop diagram in spec section 2. The loop has 6 steps:
1. User describes problem -- out of scope
2. `/conversus define` -- separate command, not part of spec 027
3. `/conversus mode` -- separate command
4. AMPL/HiGHS solves -- external, not part of spec 027
5. `/conversus validate-solution` -- **FR-001, NOT MET**
6. Equilibrium scorer -- **FR-006, NOT MET**

Steps 5 and 6 are the spec's contribution. Both are not met. The validation loop as an integrated flow does not exist.
