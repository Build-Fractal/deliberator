# Cross-Review: devils-advocate reviews functional-typing (Round 2)

**Reviewer**: devils-advocate
**Reviewing**: functional-typing Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

None identified.

Functional-typing's Round 2 review is internally consistent. The revision from P2 to P1 on the formula priority is a genuine analytical update grounded in the arbiter's audience argument, not a reversal of a prior concession. The two new observations are properly scoped as extensions rather than contradictions of existing convergences. All Round 1 concessions are maintained.

---

## Tensions

### 1. Consent-surface design principle: governing principle vs. implementation guidance

Functional-typing proposes formalizing the arbiter's (a)+(b) disclosure criterion as a P2 design note in the spec amendment. The proposed text explicitly lists what is included (problem definition, prior context files, mode) and what is excluded (templates, constitutions). This is the most concrete articulation of the criterion across all three Round 2 reviews.

The tension is about the weight of the principle. If the criterion is stated as a design note in the spec, it becomes a binding constraint on future summary-field decisions. Any new configurable input would need to be evaluated against the (a)+(b) test before being excluded from the pre-execution summary. This is arguably the right outcome -- it prevents future ad-hoc disputes -- but it also creates a specification obligation that did not exist before. The current spec says "present a human-readable summary: the mode, agents, target documents, and estimated agent launches." Adding a general disclosure criterion changes FR-001 from an enumerated list to a principled framework.

I do not object to this change. The framework is correct and prevents the category of disputes we just spent two rounds resolving. But the tension is real: functional-typing is proposing to change the nature of FR-001's obligation, not just add a field. The synthesis should flag this as a deliberate architectural choice, not a minor documentation addition.

### 2. Multi-round narrative extension: P3 vs. existing converged scope

Functional-typing proposes adding a one-sentence multi-round explanation to the "What to Expect" narrative when `rounds > 1`. I flagged in my own Round 2 review that this narrative "must not become a process tutorial." Functional-typing's proposed sentence is within the scope ceiling I set ("exactly one or two sentences"), so there is no direct conflict.

The tension is about precedent. The "What to Expect" narrative was converged in Round 1 with specific agreed wording. Adding a conditional extension in Round 2 -- even a well-scoped one -- establishes that converged items can be extended by appending conditional clauses. If the multi-round sentence is adopted, a future review could propose adding conditional clauses for arbiter configurations, stagnation detection, or other advanced features. Each individual addition might be proportionate, but the cumulative effect could violate the scope ceiling.

I accept functional-typing's specific proposal -- the one-sentence multi-round explanation is genuinely useful for the `rounds > 1` scenario. But the implementation should include a note that the "What to Expect" narrative is not extensible beyond this addition without further review. Scope ceilings need explicit enforcement.

### 3. Process observations qualification: accurate but immaterial

Functional-typing challenges the synthesis's characterization of the `/conversus arbitrate` fix as requiring the "multi-reviewer chain," arguing that any single reviewer could have identified the dead reference. The distinction between discovery and refinement is analytically valid.

As the reviewer who identified the dead reference in Round 1, I can confirm: the identification was not difficult. What the multi-reviewer chain added was severity calibration (integration-architect elevated it to P0) and fix specification (the three-location scope, the planned-command note). Functional-typing's precision is correct. The synthesis overstates the collaborative requirement for the initial identification but correctly values the collaborative contribution to the fix quality.

This is immaterial to the recommendation set. The synthesis's conclusion -- that the cooperative process adds value -- stands regardless of which examples best illustrate it. I flag the precision point for completeness but do not elevate it.

---

## Safe Agreements

### 1. All four disputes resolved

Functional-typing's Round 2 positions bring the last open disputes to full consensus:

- **Dispute 1**: Functional-typing accepts P2 sequencing for the problem-statement addition, matching my position. 3-0.
- **Dispute 2**: Functional-typing maintains P2 for prior context disclosure, matching my position. 3-0.
- **Dispute 3**: Functional-typing formally adopts at P3, matching my position. 3-0.
- **Dispute 4**: Functional-typing revises from P2 to P1, matching my revised position. 3-0.

The Round 1 four-dispute residual is fully resolved. Every item in the recommendation set now has unanimous agreement on both the fix and the priority.

### 2. The arbiter's audience argument on Dispute 4 is the correct lens

Functional-typing explicitly states: "The document's audience (LLM agents, not just human readers) changes the severity calculus." This is the same reasoning that persuaded me to move from neutral to P1. The argument is now accepted by all three reviewers. The tiebreaker was not authority (the arbiter's role) but substance (the audience-specific harm analysis).

### 3. The consent-surface (a)+(b) criterion is endorsed

All three Round 2 reviews endorse the criterion in some form. Functional-typing provides the most specific articulation with explicit inclusion/exclusion lists. The principle is agreed; only the packaging differs across reviewers.

### 4. No concessions reversed, no converged items reopened

Functional-typing explicitly confirms: "No prior concessions have been reversed. No converged recommendations have been reopened." This matches my own confirmation. The deliberation has been strictly monotonic.

### 5. The synthesis and arbitration are accurate

Functional-typing confirms the synthesis's characterization of all positions and disputes, with only the minor process-observation qualification noted above. The arbiter's advisory opinions are characterized as "well-reasoned across all four disputes." This matches my assessment.

### 6. The spec is ready for implementation

Both reviews conclude the spec and SKILL.md implementation are ready. The converge handler is structurally sound and the recommendation set is comprehensive.

### 7. The formula error has demonstrated harm

Functional-typing's revised position on Dispute 4 implicitly acknowledges what I stated explicitly: the formula error interfered with this review cycle's analysis. This is empirical evidence, not hypothetical risk. Both reviews now treat the error as a bug with demonstrated harm rather than a documentation quality issue.
