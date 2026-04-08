# Cross-Review: integration-architect reviews devils-advocate (Round 2)

**Reviewer**: integration-architect
**Reviewing**: devils-advocate Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

None identified.

Devils-advocate's Round 2 positions are internally consistent, maintain all Round 1 concessions, and do not contradict any converged recommendation. The explicit alignment on Dispute 4 (P1) is a new position that is consistent with the arbiter's advisory and the analytical framework devils-advocate used throughout. The scope refinement on failure recovery is additive and does not undermine the existing convergence on that item.

---

## Tensions

### 1. Failure recovery scope refinement: expansion of a converged item

Devils-advocate proposes expanding the converged P2 failure recovery recommendation to cover pre-execution parsing failures alongside mid-execution run failures. Devils-advocate frames this as "a scope refinement, not a new item." I understand the framing -- both scenarios are instances of "translate errors for non-experts" -- but modifying the scope of a converged item in Round 2 requires careful handling.

The Round 1 convergence on failure recovery was specifically about mid-execution failures: "document that re-running is required, not manual recovery." Pre-execution parsing failures are a different failure category with different remediation (fix the YAML and retry, not re-run the entire deliberation). The user experience is related but the fix guidance is distinct.

I do not object to the substance. The pre-execution parsing failure path at SKILL.md line 1370 does need more specific guidance for SC-001 non-experts. But I prefer this be tracked as a scope note on the existing P2 item rather than treated as if it were always part of the original convergence. The distinction matters for implementation: someone implementing the P2 failure recovery item should know that the scope was expanded in Round 2 so they address both failure paths.

### 2. Dispute 1 argumentation: resolved but still advocating

Devils-advocate accepts the arbiter's P2 sequencing on the problem-statement addition but devotes significant space to re-arguing why integration-architect's slippery-slope objection fails. The structural argument -- "seven instrumentalities and zero purposes" -- is the strongest version of the case. I conceded this dispute in my own Round 2 review, so the argumentation is directed at a position I no longer hold.

This is not a contradiction -- devils-advocate could not have known I would concede when writing the Round 2 review. But it creates a tension in the record: the dispute is fully resolved (3-0 at P2) yet the most detailed advocacy for one side appears in Round 2 rather than Round 1. The next synthesis should note the resolution and can reference devils-advocate's structural argument as the definitive articulation of the rationale, rather than treating it as ongoing advocacy for a contested position.

### 3. Arbiter field readability: flagged, retracted, but potentially relevant

Devils-advocate's new observation 3 flags that arbiter disclosure terms (trigger, timing, influence) may confuse non-experts, then immediately retracts it as too narrow to act on. I agree with the retraction -- the audience for this concern (users inheriting hand-crafted configs with arbiters) is small. But the observation connects to the consent-surface design question I raised in my Residual Concerns section. If we adopt the (a)+(b) disclosure criterion, the arbiter field satisfies it. The question then becomes not whether to disclose (yes) but whether the disclosure is comprehensible.

This is a future design consideration, not a current tension. I note it because devils-advocate identified the right concern -- arbiter terms are engine-internal jargon -- even if the current retraction is the correct Round 2 disposition. If the consent-surface criterion is formalized in a spec amendment, the comprehensibility of arbiter disclosure should be addressed at that time.

---

## Safe Agreements

### 1. All four disputes resolved or nearly resolved

Devils-advocate's Round 2 positions align with the emerging consensus on all four disputes:

- **Dispute 1**: P2 problem-statement addition. Devils-advocate accepts the arbiter's sequencing. I conceded in my own review. 3-0.
- **Dispute 2**: P2 prior context disclosure. Devils-advocate maintains P2. I moved to P2. 3-0.
- **Dispute 3**: P3 mtime documentation. Devils-advocate accepts P3. I explicitly adopted. 3-0.
- **Dispute 4**: P1 formula correction. Devils-advocate moves to P1. I maintained P1. 3-0 (pending functional-typing's confirmation).

Every disputed item from Round 1 now has at least 2-0 agreement with the third reviewer's concurrence expected. The deliberation achieved full convergence.

### 2. All Round 1 concessions maintained

Devils-advocate explicitly lists all Round 1 concessions (content hashing, mtime heuristic, formula root cause, speckit framing, FR-004 scoping) and confirms they all stand. No reversals. This matches my own confirmation. The deliberation has been monotonically convergent.

### 3. The zero-new-engine-logic constraint is verified

Devils-advocate confirms testing this constraint explicitly in Round 1 and the arbiter's observation that it "survived through adversarial review." I concur. This is the spec's most important architectural property.

### 4. The "What to Expect" narrative scope ceiling

Devils-advocate flags that the narrative "must not become a process tutorial" and should be "exactly one or two sentences." I agree with this scope ceiling. The converged wording from Round 1 is the right length. This aligns with SC-004's prohibition on YAML dumps -- the same principle applies to process dumps.

### 5. The `/conversus arbitrate` dead reference fix is correctly scoped

Devils-advocate re-examined the three locations where the dead reference appears (lines 1469, 1488, 1489) and confirmed the converged fix must hit all three. This matches the synthesis's identification. Comprehensive and correct.

### 6. The delegation semantics fix serves both clarity and efficiency

Devils-advocate observes that the phrase "config already parsed in the pre-execution summary" tells the agent not to re-parse `conversus.yml`, avoiding redundant work in the context window. This is a good practical observation that reinforces the value of the converged fix beyond its primary purpose of eliminating ambiguity.

### 7. The spec is ready for implementation

Both reviews conclude the spec is ready. The recommendation set is comprehensive, prioritized, and at or near full consensus on every item after Round 2 concessions.

### 8. Priority disputes are calibration signals, not failures

Devils-advocate endorses the arbiter's framing that P-level disagreements are "calibration signals rather than failures to converge." I agree. The fact that all three reviewers reached the same diagnosis and fix direction for every item -- differing only on severity weighting -- validates the cooperative process.
