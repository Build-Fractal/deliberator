# Cross-Review: functional-typing reviews devils-advocate (Round 2)

**Reviewer**: functional-typing
**Reviewing**: devils-advocate Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

None identified.

Devils-advocate's Round 2 positions are internally consistent, maintain all Round 1 concessions without reversal, and do not contradict any converged recommendation. The new explicit alignment on Dispute 4 (P1) and the maintained positions on Disputes 1 and 2 are all coherent with the review's analytical framework. The scope refinement on failure recovery is additive rather than contradictory.

---

## Tensions

### 1. Failure recovery scope refinement: additive vs. already covered

Devils-advocate's new observation 1 proposes that the converged P2 failure recovery recommendation should cover pre-execution parsing failures in addition to mid-execution run failures. Devils-advocate frames this as "a scope refinement, not a new item." I do not object to the substance -- translating schema validation errors to plain language for non-experts is clearly aligned with SC-001. However, the converge handler already has a sentence addressing this: "If parsing fails, report the validation error and stop" (SKILL.md line 1370). The question is whether "report the validation error" is sufficient or whether it needs to be elaborated with translation guidance.

For the SC-001 non-expert persona, raw schema validation errors are likely opaque, so devils-advocate's concern has merit. But this tension is about where the fix belongs. The converged P2 failure recovery item in Round 1 was specifically about mid-execution failures -- "state that re-run is required." Expanding it to cover pre-execution parsing failures changes the scope of a converged item. If this refinement is adopted, it should be clearly flagged as an expansion rather than treated as always having been within the original scope.

This is a minor procedural tension. The substance is sound.

### 2. The "What to Expect" narrative scope warning

Devils-advocate flags a scope risk for the "What to Expect" narrative: it "must not become a process tutorial" and should be "exactly one or two sentences." This aligns with my Round 2 observation that the narrative should include a multi-round explanation for configs with `rounds > 1`. These two positions are compatible -- a one-sentence multi-round explanation fits within devils-advocate's two-sentence ceiling -- but the tension is that my proposed extension could be seen as the beginning of the scope creep devils-advocate warns against.

For the record: my proposed addition is one sentence ("In multi-round mode, the entire process repeats with awareness of prior round results. If agents stop changing their positions, the run terminates early."). This is within the scope ceiling. But the tension should be acknowledged so that implementation does not use either position as justification for further elaboration.

### 3. Arbiter field readability concern: flagged but not elevated

Devils-advocate's new observation 3 notes that arbiter disclosure terms (trigger, timing, influence) may confuse non-experts, then immediately retracts the concern as too narrow to recommend action. I agree with the retraction -- the concern is real but the audience is narrow (users inheriting hand-crafted configs with arbiters). However, this observation intersects with the consent-surface design principle I proposed in my Round 2 review. Under the (a)+(b) criterion, arbiter configuration meets both conditions: it influences agent output (the arbiter can issue rulings) and is not fully visible in results (the influence level -- advisory vs. binding -- is not obvious from the arbitration output). The readability of the disclosure is a secondary concern once you accept that the field must be disclosed; the primary question is whether the disclosure is comprehensible.

This is not actionable in the current round. I note it as a future design consideration that connects devils-advocate's observation to the consent-surface framework.

---

## Safe Agreements

### 1. All Round 1 converged recommendations are stable

Both reviews confirm all eight Round 1 converged recommendations without modification. Neither party reopens any converged item. Devils-advocate's specific re-examination of three converged items (the `/conversus arbitrate` fix scope, the delegation semantics clarification, and the "What to Expect" narrative) confirms they remain sound after a second reading.

### 2. Dispute 1: P2 problem-statement addition

Devils-advocate accepts the arbiter's P2 sequencing, consistent with my position. The label fix ships at P1; the problem-statement addition ships as immediate P2 follow-up. Devils-advocate's structural argument -- that the pre-execution summary discloses seven instrumentalities and zero purposes -- is the strongest articulation of why the problem statement is categorically different. I concur with this framing.

### 3. Dispute 2: P2 prior context disclosure

Both reviews maintain P2, aligned with the arbiter. Neither party has new arguments; the case is fully developed. Full consensus among all three reviewers.

### 4. Dispute 3: Resolved at P3

Both reviews accept P3 for the mtime false-positive documentation. Devils-advocate's emphasis that "the false-positive scenario occurs at the consent surface -- the one moment the guided flow asks the user to trust it" reinforces the rationale without changing the priority. Resolved.

### 5. Dispute 4: Resolved at P1

Devils-advocate now explicitly aligns with P1, matching my revised position and integration-architect's maintained position. The arbiter concurs. Full consensus. Devils-advocate's added observation -- that the error "actively interfered with my analysis" during Round 1 -- provides empirical evidence of demonstrated harm, strengthening the P1 case beyond the theoretical argument.

### 6. All Round 1 concessions maintained

Both reviews explicitly confirm all prior concessions: content hashing withdrawn to spec 008, mtime accepted as best-effort, formula root cause accepted as algebra error, speckit framing softened. No reversals.

### 7. The zero-new-engine-logic constraint is verified

Devils-advocate confirms the arbiter's observation that this constraint "survived through adversarial review." I concur -- this is the spec's most important architectural property and it holds under examination from all three analytical lenses.

### 8. The spec is ready for implementation

Both reviews conclude the spec and SKILL.md implementation are ready for implementation. The recommendation set is comprehensive and, after Round 2 position updates, at or near full consensus on every item.
