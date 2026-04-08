# Cross-Review: devex-advocate reviewing spec-compliance

**Spec**: 027-solver-validation-flow
**Reviewer**: devex-advocate
**Subject**: spec-compliance Phase 1 review
**Round**: 1

---

## Verified Claims

### 1. FR-001 NOT MET is correct

The spec-compliance agent correctly identifies that no CLI command exists. From a DX perspective, this is the single most important gap: the entry point for the entire validation flow does not exist. A developer reading the spec would expect to run `/conversus validate-solution solution.yml` and get results. They cannot.

### 2. FR-008 PARTIALLY MET is accurate

The three-valued verdict model exists but no code writes it to a file. The spec-compliance agent correctly distinguishes between "the data model satisfies the structural requirement" and "the file generation does not exist." This is a precise and useful distinction.

### 3. FR-009 PARTIALLY MET -- with an important nuance

The spec-compliance agent notes that revise/reject verdicts do not enforce non-empty constraint_additions. This is a good catch that I missed in my review. From a DX perspective, a developer receiving a "revise" verdict with zero constraint additions would be confused -- they're told to change something but not told what to change.

### 4. SC-005 MET assessment is reasonable

The 16 LLM calls calculation is correct (N=3: 3 + 6 + 3 + 3 + 1 = 16). With parallel execution and ~10 second latency per call, the deliberation portion is well under 10 minutes. The caveat about the full loop is important but SC-005 specifically says "3-agent deliberation," which scopes the criterion to the validation deliberation itself.

---

## Disagreements

### 1. SC-002 should be NOT MET, not PARTIALLY MET

The spec-compliance agent rates SC-002 (sensitivity analysis identifies portfolio infeasibility under interest rate increase) as PARTIALLY MET because "the framework supports the finding structurally." I disagree. SC-002 says "correctly identifies," which requires the system to actually produce this finding for a given input. The SensitivityFinding model can represent the finding, but so can a plain dict. The existence of a data model that could hold the answer is not the same as having a system that produces the answer.

By this logic, any Pydantic model that matches an expected output schema would satisfy any success criterion. The criterion requires demonstrated behavior, not structural possibility. SC-002 should be NOT MET until the flow actually runs and produces the finding.

### 2. FR-002 MET should note the 3-of-5 gap more prominently

The spec-compliance agent marks FR-002 as MET with a caveat about missing scheduling and negotiation types. The caveat reads: "This does not prevent MET status because FR-002 says 'based on problem type' without enumerating which types must exist." This is technically correct but misleading. The spec's section 3 table is immediately adjacent to the FR-002 requirement and clearly establishes the expected set of problem types. A PARTIALLY MET with the note "3 of 5 expected types implemented" would better reflect reality.

### 3. FR-011 PARTIALLY MET is generous

FR-011 says iterations are tracked. The only evidence of iteration awareness is `iterations: 1` in the generated config, which is a static default value. There is no tracking, no counter, no history. The config field is not iteration tracking -- it is a deliberation engine parameter that says "run 1 iteration." PARTIALLY MET implies partial implementation; this is closer to NOT MET with incidental config overlap.

---

## Additions

### Missing assessment: spec section 6 (Constraints)

The spec-compliance agent assessed all FRs and SCs but did not assess the three constraints in section 6:
1. "Validation deliberation uses the same engine as regular deliberation -- no special execution path." The config generation function produces a standard conversus.yml dict, which would use the standard engine. MET by design.
2. "Solution critique agents are auto-generated from templates, not hardcoded." MET -- the `_AGENT_TEMPLATES` dict is a template system.
3. "The validation flow MUST NOT modify the original solution." MET by design -- the flow produces recommendations, not modifications.

These are all MET, but should be documented for completeness.

### FR-009 enforcement gap is a real DX problem

The spec-compliance agent's observation about non-enforced constraint_additions on revise/reject is worth amplifying. A Pydantic `model_validator` should enforce:
```python
if self.verdict in ("revise", "reject") and not self.constraint_additions:
    raise ValueError("Revise/reject verdicts must include constraint additions")
```

This would make the data model self-documenting: a developer constructing a ValidationVerdict would be guided by the validation error to provide the required information.
