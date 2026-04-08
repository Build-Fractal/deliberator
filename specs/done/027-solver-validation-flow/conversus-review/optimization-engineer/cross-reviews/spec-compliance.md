# Cross-Review: optimization-engineer reviewing spec-compliance

**Spec**: 027-solver-validation-flow
**Reviewer**: optimization-engineer
**Subject**: spec-compliance Phase 1 review
**Round**: 1

---

## Verified Claims

### 1. FR/SC compliance matrix is methodical and accurate

The spec-compliance agent's requirement-by-requirement assessment is thorough. The MET/PARTIALLY MET/NOT MET classifications are well-supported with evidence citations. The distinction between "model exists" and "integration exists" is consistently applied.

### 2. FR-006 and FR-007 correctly identified as NOT MET

The equilibrium scorer integration (spec 021) is completely absent. The spec-compliance agent correctly identifies this as a hard dependency: FR-007 (threshold check at 0.7) cannot exist without FR-006 (scorer integration). The cascade is correctly modeled.

### 3. SC-005 timing analysis is correct

The 16 LLM calls formula (N + N(N-1) + N + N + 1 for N=3) is the standard conversus complexity. With parallelism in phases 1-4 (only synthesis is sequential), the wall-clock time is approximately max(phase_time) * 5 + synthesis_time. At ~10 seconds per call, the critical path is about 60 seconds. Well under 10 minutes.

---

## Disagreements

### 1. FR-002 should be PARTIALLY MET, not MET

The spec-compliance agent marks FR-002 as MET with a caveat about 3/5 problem types. The agent's reasoning is: "FR-002 says 'based on problem type' without enumerating which types must exist."

I disagree. FR-002 says: "Agents MUST be auto-generated based on problem type with solution-critique prompts (not generic review prompts)." The spec's section 3 table immediately following the FR-002 requirement lists five specific problem types with their agent roles. In the solver engineering domain, the problem type taxonomy is the core of the requirement -- implementing 60% of it is partial satisfaction.

More critically, a developer who runs `generate_validation_config(problem_type="scheduling")` gets a ValueError. This is not graceful degradation -- it is a hard failure for a valid problem type. PARTIALLY MET is the correct classification.

### 2. SC-002 PARTIALLY MET is correct (disagreeing with devex-advocate, agreeing with spec-compliance)

The spec-compliance agent's reasoning that SC-002 is PARTIALLY MET because "the framework supports the finding structurally" is sound from an engineering perspective. SC-002 tests whether the sensitivity analysis framework can represent and communicate interest rate sensitivity findings. The `SensitivityFinding` model can express this finding with the correct fields. The test `test_sensitivity_findings_roundtrip` demonstrates the exact scenario (interest_rate, +2%, infeasible, -15%).

SC-002 is a success criterion for the framework, not a system integration test. The question "correctly identifies" should be interpreted as "the framework directs agents to identify and structure such findings." The sensitivity instructions + the SensitivityFinding model + the portfolio risk-minimizer agent prompt collectively satisfy this at the framework design level.

Whether the LLM agent actually produces a correct finding is a runtime test, not a framework test. PARTIALLY MET is the right middle ground.

### 3. FR-010 PARTIALLY MET should be NOT MET

The spec-compliance agent marks FR-010 (output consumable by solver for re-optimization) as PARTIALLY MET because "the data structure exists." I disagree. The `constraint_additions` field is `list[str]` -- free-form strings. No solver can consume free-form English strings. There is no parser, no template system, no AMPL code generator.

FR-010 uses "MUST be consumable" -- this is a binary requirement. Either the output can be fed to a solver or it cannot. Currently it cannot. A `list[str]` field that holds English sentences is not partial solver compatibility -- it is zero solver compatibility. NOT MET.

---

## Additions

### FR-009 enforcement gap has a solver engineering implication

The spec-compliance agent notes that revise/reject verdicts don't enforce non-empty constraint_additions. From a solver perspective, this is more serious than a validation gap: it means the feedback loop can produce "revise" verdicts with no actionable feedback. A solver operator receiving "solution needs revision" with no constraint changes has nothing to implement. The model should enforce:
- `verdict == "revise"` implies `len(constraint_additions) > 0`
- `verdict == "reject"` implies `len(constraint_additions) > 0 OR len(summary) > threshold`

### The compliance matrix should distinguish "NOT MET (not implemented)" from "NOT MET (incorrectly implemented)"

All of the NOT MET findings are due to missing implementation, not incorrect implementation. The distinction matters for prioritization: missing code is an additive task (write new code), while incorrect code requires debugging and potentially redesigning existing code. A column for "Reason: missing | incorrect | insufficient" would sharpen the action items.

### FR-012 dependency chain should be explicit

FR-012 depends on spec 022 (convergence predictor). The spec-compliance agent notes this but does not assess whether spec 022 itself is implemented. If spec 022 is also unimplemented, FR-012 is blocked on an external dependency and should be classified as "NOT MET (blocked)" rather than just "NOT MET."
