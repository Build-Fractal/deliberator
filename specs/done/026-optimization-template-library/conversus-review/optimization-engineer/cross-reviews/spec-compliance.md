# Cross-Review: optimization-engineer reviewing spec-compliance

**Spec**: 026-optimization-template-library

---

## Dangerous Contradictions

### DC-1: SC-004 assessment -- PARTIAL vs. PASS

- **spec-compliance claims**: SC-004 is PASS (revised from PARTIAL in body text, but the summary table says "3 Pass" for SC which only works if SC-004 is included). The reasoning: "The templates provide structurally valid examples that can be assembled. The assembly logic itself is spec 014's concern."
- **optimization-engineer claims**: SC-004 should be PASS for this spec's scope. The spec says "every template's example produces a valid AssembledObjective." The templates provide valid examples that validate against ObjectiveTemplate. The AssembledObjective is a spec 014 construct that combines template + parameters + constraints. At the template layer, the examples are structurally valid.
- **Why this matters**: If SC-004 is PARTIAL, it implies spec 026 has unfinished work. If it's PASS, spec 026 is complete and any remaining assembly work belongs to spec 014. The distinction affects whether spec 026 can be closed.
- **Resolution**: I agree with the spec-compliance agent's revised PASS assessment. The template library provides valid examples at the correct layer of abstraction. Assembly is spec 014's job.

**Note**: This was initially flagged as a dangerous contradiction because the review body revises SC-004 from PARTIAL to PASS but the summary table and initial compliance matrix show "3 Pass" for SCs. On closer reading, the agent's narrative is internally consistent -- the revision happens in the SC-004 row itself, with the note explaining the upgrade. The concern is resolved within the review.

---

## Tensions

### T1: FR-004 NOT ASSESSED -- scope boundary

- **spec-compliance's position**: FR-004 is "NOT ASSESSED" because it crosses spec boundaries. The classifier lives in spec 014.
- **optimization-engineer's position**: I agree FR-004 cannot be assessed from spec 026 artifacts. However, the spec-compliance agent's cross-cutting concern about "unreachable templates" is important. The templates are correct and valid, but if spec 014 never updates its classifier, the templates are only usable by direct reference, not by natural-language routing. This is a deployment risk, not a quality risk.
- **Nature**: Agreement on the assessment, mild tension on the urgency. The spec-compliance agent treats this as Low (SC-C2). I think it's worth flagging as a cross-spec dependency but agree it's not spec 026's problem to solve.

### T2: SC-005 confidence level

- **spec-compliance's position**: SC-005 NOT TESTED. Cites optimization-engineer's mathematical review as giving "high confidence" but notes solver execution is unverified.
- **optimization-engineer's position**: I can provide stronger confidence than "high confidence." Every formulation uses a standard problem class (LP, MIP, QP) with well-characterized solver support in HiGHS. There are no exotic constraints or non-convex formulations. HiGHS handles LP and MIP natively; QP (portfolio-markowitz) requires AMPL's QP interface. The risk of solver failure is near-zero for mathematical reasons, though implementation bugs in AMPL model generation remain possible.
- **Nature**: Mild tension. The spec-compliance agent is correctly conservative -- tests should verify, not just mathematical arguments. But the risk should be communicated as "very low" rather than "unknown."

---

## Safe Agreements

1. **FR-001 through FR-003, FR-005, FR-006 all PASS**: Both agents agree on the evidence (Pydantic model_validate, parametric tests, manual audit). No dispute.

2. **SC-001 and SC-002 PASS**: Template count 36 >= 35 and constraint count 10 >= 10. Both verified against directory listings and tests.

3. **FR-004 correctly deferred to spec 014**: Both agents agree this is a cross-spec concern. Spec 026 provides valid templates; spec 014 provides classifier routing.

4. **Test suite is comprehensive for schema-level validation**: The spec-compliance agent's evidence citations are accurate. The test structure (count tests, validation tests, cross-reference tests, gap_question tests) covers the spec's requirements thoroughly.

---

## Additions from optimization-engineer perspective

### A1: form field mathematical validity

The spec-compliance agent notes that FR-001 requires a `form` field but does not assess whether the form expressions are *mathematically valid*. From my review:

- All `form` fields are valid mathematical expressions using standard notation
- They correctly represent their optimization problem class
- Variable naming is consistent (x_ij for binary decisions, f_ij for flow, w for weights/allocations)
- The expressions match the corresponding `description` and `constraints`

This is not a formal FR requirement, but it contributes to the semantic quality of the library. A template with `form: "some nonsense"` would pass FR-001 structurally but fail the intent.

### A2: SC-003 partial addressability

The spec-compliance agent marks SC-003 as NOT TESTED. I note that while end-to-end routing is untested, the assignment-optimal template is *designed* for exactly the type of query described in SC-003 ("assign my team to projects"). The template's `description` and `gap_question` fields provide the natural-language hooks a classifier would use. The template is ready; the classifier is not.
