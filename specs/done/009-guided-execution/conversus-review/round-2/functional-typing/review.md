# Cooperative Review: functional-typing (Round 2)

**Spec**: 009-guided-execution
**Target files**: `specs/009-guided-execution/spec.md`, `SKILL.md`
**Reviewer role**: Structural correctness and specification compliance
**Round**: 2 of 2
**Date**: 2026-03-22
**Prior materials**: `round-1/summary/final.md`, `round-1/arbitration/resolution.md`, `round-1/functional-typing/disputes.md`

---

## Executive Summary

Round 1 produced a thorough, well-structured set of converged recommendations and four narrow disputes. The synthesis and arbitration are high-quality documents that correctly characterize the deliberation record. This Round 2 review engages with the arbiter's advisory opinions and the synthesis's framing of remaining disputes, affirms prior concessions, and identifies two missed opportunities that the Round 1 process did not surface.

The core finding remains unchanged: the Converge handler is a structurally sound UX wrapper around the run engine. All ten functional requirements are satisfied. The zero-new-engine-logic constraint holds. The Round 1 recommendation set -- eight fully converged items, four narrowly disputed -- constitutes the correct revision plan. Round 2 refines priority assignments for the disputed items and raises two structural observations that the Round 1 focus on individual findings did not address.

---

## Alignment

### Alignment with the Round 1 Synthesis

The synthesis (`round-1/summary/final.md`) accurately represents my positions across all four phases. Specific confirmations:

1. **Converged Recommendations 1-10**: I affirm the synthesis's characterization of all ten converged items. The fix descriptions, priority assignments, and attribution are correct. I have no factual corrections to the synthesis text.

2. **Dispute 1 (problem-statement inclusion)**: The synthesis correctly characterizes my position as 2-1 majority with devils-advocate, and correctly notes that integration-architect's scope objection is "procedurally valid." The synthesizer's recommendation to treat the problem-statement addition as "immediate P2 follow-up" is a reasonable bridge. I accept this sequencing.

3. **Dispute 2 (prior-context priority)**: The synthesis correctly identifies the analytical gap in integration-architect's position -- the slippery-slope argument does not hold because prior files are the only configured input that influences all agents and is absent from the summary. The synthesizer's assessment that "P2 is the more defensible priority" aligns with my position and devils-advocate's.

4. **Dispute 3 (mtime documentation)**: The synthesis correctly characterizes this as a procedural gap. I did not oppose the one-sentence documentation addition in Round 1; I did not adopt it because it fell outside my structural-correctness focus. I now explicitly endorse it. It should be adopted as P3.

5. **Dispute 4 (formula priority)**: The synthesis correctly represents both integration-architect's P1 argument and my P2 argument.

### Alignment with the Arbiter's Advisory Opinions

The arbiter's resolution (`round-1/arbitration/resolution.md`) is well-reasoned across all four disputes. Specific responses:

1. **Dispute 1**: The arbiter's analysis that the problem definition is "categorically different" from templates and constitutions is precisely my argument. The arbiter's conclusion -- apply label fix at P1, treat problem-statement addition as P2 -- matches the synthesis's recommendation and is acceptable to me. I concede the P2 sequencing rather than bundling it into the P1 label fix. This does not reverse my prior position that the gap is real; it accepts a two-step implementation path.

2. **Dispute 2**: The arbiter endorses P2, consistent with my position. The arbiter's observation that the inherited-config scenario (Constraint 2) undermines integration-architect's user-awareness assumption is the correct analytical frame. No change to my position.

3. **Dispute 3**: The arbiter recommends adoption as P3. I concur and formally adopt this into my recommendation set, which I did not do in Round 1. This is not a reversal -- I never opposed it -- but a correction of a procedural omission.

4. **Dispute 4**: The arbiter recommends P1, siding with integration-architect. The arbiter's tiebreaker argument -- that SKILL.md is read by LLM agents and an internal contradiction in an instruction document for automated agents is "functionally closer to a code bug than a documentation typo" -- is compelling. I accept this reframing. I revise my position from P2 to P1. The arbiter is correct that the document's audience (LLM agents, not just human readers) changes the severity calculus. This is a genuine update to my position, not a concession on substance -- I always agreed the fix was necessary; I underweighted the audience factor.

---

## Missed Opportunities

### 1. No consolidation of the consent-surface design principle

The arbiter's "Considerations for Next Round" (item 1) identifies that three of four disputes cluster around a single architectural question: what information does the pre-execution summary owe the user? The arbiter proposes a selection criterion: "disclose any configured input that (a) influences agent output and (b) is not visible in the results."

Round 1 treated each consent-surface gap (problem statement, prior files, mtime documentation) as an independent finding. This produced correct individual recommendations but missed the opportunity to establish the governing principle that would prevent future gaps of the same class. The proposed (a)+(b) criterion is sound and would have resolved Disputes 1, 2, and 3 without per-item negotiation.

**Recommendation**: The spec amendment for FR-001 should include, alongside the specific field additions, a design note articulating the disclosure criterion. Suggested text for the spec: "The pre-execution summary should disclose any configured input that influences agent output and is not visible in the deliberation results. This includes the problem definition, prior context files, and mode. It excludes templates (visible as output structure) and constitutions (visible as synthesis process rules)." This is a P2 documentation item -- it costs one paragraph and prevents a category of future disputes rather than just fixing the current instances.

### 2. No cross-round stagnation consideration for the converge handler

The `conversus.yml` for this review specifies `rounds: 2` and `stagnation: detect`. The converge handler's "What to Expect" narrative (Converged Recommendation 6) explains what agents do within a round, but does not address what happens across rounds or when stagnation is detected. For the SC-001 non-expert persona who configured `rounds: 2`, the pre-execution summary will say "Rounds: 2" but the "What to Expect" narrative describes only a single-round process.

The converge handler at SKILL.md line 1387 already displays `Rounds: {rounds} (with {iterations} iteration(s) per round)`, but the "What to Expect" narrative agreed in Recommendation 6 does not explain what "rounds" means -- why would the process repeat, what changes between rounds, and what stagnation detection does.

This is a minor extension of Recommendation 6, not a new finding. The "What to Expect" narrative should include one additional sentence for multi-round configs: "In multi-round mode, the entire process repeats with awareness of prior round results. If agents stop changing their positions, the run terminates early (stagnation detection)." This covers the three concepts a non-expert needs: repetition, cumulative awareness, and early termination.

**Recommendation**: P3. Extend the "What to Expect" narrative with a one-sentence multi-round explanation. Only relevant when `rounds > 1`, which is an advanced configuration, but the whole point of `converge` is making advanced configurations accessible.

---

## Off-Base Assumptions

### 1. The synthesis's "Process Observations" overstate the collaborative contribution model

The synthesis's "Process Observations" section claims three findings "specifically required the multi-reviewer chain": the formula error, the `/conversus arbitrate` fix, and the staleness scoping. For the formula error and the staleness scoping, the claim is well-supported -- each required multiple reviewers' analytical steps to reach the correct conclusion. For the `/conversus arbitrate` fix, the claim is weaker. Any single reviewer could have identified that suggesting an unimplemented command is problematic. The multi-reviewer contribution (severity calibration by integration-architect, dispute explanation by devils-advocate, combined fix by functional-typing) refined the solution but did not require cooperative discovery.

This is not a substantive error -- the synthesis's conclusion that the cooperative model works is correct. But the process-validation claim should be scoped more precisely. Two of the three cited examples demonstrate genuine multi-reviewer discovery. The third demonstrates multi-reviewer refinement, which is valuable but categorically different.

### 2. The arbiter's scope assessment of the speckit suggestion is underdetermined

The arbiter (Considerations, item 2) states that the negative qualification ("informational and tool-availability-dependent") is "safer because it does not create a precedent for adding arbitrary cross-tool suggestions without review." This framing assumes that cross-tool suggestions are risky by default, but does not analyze what the risk actually is. The speckit suggestion at SKILL.md lines 1504-1507 is a conditional recommendation ("if mode is cooperative"), not an unconditional insertion. It fires only for a specific mode and is appended to other next steps rather than replacing them. The risk of precedent-setting is real but overstated -- the qualifying note in the spec already bounds it. Future cross-tool suggestions would require the same spec acknowledgment, which is the correct gate.

This does not change any recommendation. The converged fix (keep the suggestion, add a spec note) is correct regardless of which framing motivates it.

---

## Actionable Recommendations

### Revised Consolidated Table (Round 2)

This table incorporates all Round 1 convergences, my revised positions on disputed items, and the two new observations from this round.

| Priority | Recommendation | Status | Round 2 Change |
|----------|---------------|--------|----------------|
| **P0** | Replace `/conversus arbitrate` dead reference with actionable workaround + planned-command note | Consensus | None |
| **P1** | Add `--output <dir>` flag to converge handler | Consensus | None |
| **P1** | Fix "Problem" label to "Mode" at SKILL.md line 1377 | Consensus | None |
| **P1** | Fix Important Notes formula arithmetic (lines 1517-1525) | **Revised to P1** | Accepted arbiter's audience argument; elevated from my prior P2 |
| **P2** | Add problem statement to pre-execution summary | 2-1 majority (FT+DA) | Accepted arbiter's sequencing as P2 follow-up to P1 label fix |
| **P2** | Add prior context disclosure to pre-execution summary | 2-1 majority (FT+DA at P2) | No change; arbiter concurs with P2 |
| **P2** | Document failure recovery position (full re-run required) | Consensus | None |
| **P2** | Make delegation semantics explicit in Execution section | Consensus | None |
| **P2** | Add "What to Expect" narrative to pre-execution summary | Consensus | None |
| **P2** | Specify dispute-parsing file target as `{output}/summary/final.md` | Consensus | None |
| **P2** | Add spec acknowledgment for cross-tool next steps (speckit) | Consensus | None |
| **P2** | Articulate consent-surface disclosure criterion in spec (new) | New | Governs future summary-field decisions; prevents dispute recurrence |
| **P3** | Document mtime staleness false-positive limitation | **Formally adopted** | Endorsed; was procedurally unadopted in Round 1 |
| **P3** | Add multi-round explanation to "What to Expect" narrative (new) | New | One-sentence extension for `rounds > 1` configs |
| **Deferred** | `--dry-run` capability for converge | Consensus | None |
| **Withdrawn** | Extend staleness check to `problem.md` (belongs in spec 008) | Consensus | None |
| **Withdrawn** | Replace mtime with content hashing (belongs in spec 008) | Consensus | None |

### Summary of Round 2 Position Changes

1. **Formula priority**: Revised from P2 to P1 (accepted arbiter's argument that SKILL.md's audience is LLM agents, making internal contradictions functionally closer to code bugs than documentation errors).

2. **Mtime documentation**: Formally adopted into my recommendation set as P3 (was never opposed, but procedurally unadopted in Round 1 due to focus scope).

3. **Problem-statement sequencing**: Accepted P2 sequencing rather than bundling into the P1 label fix (accepted arbiter's and synthesizer's bridging recommendation).

No prior concessions have been reversed. No converged recommendations have been reopened.

---

## Referenced Documentation

| Document | Lines/Section | Relevance |
|----------|---------------|-----------|
| `specs/009-guided-execution/spec.md` | 1-62 | Authoritative spec: FR-001-010, SC-001-004, constraints |
| `SKILL.md` | 1326-1508 | Converge handler (primary review target) |
| `SKILL.md` | 1511-1545 | Important Notes and baseline features |
| `SKILL.md` | 1366-1408 | Pre-execution summary template |
| `SKILL.md` | 1462-1481 | Post-execution disputes section |
| `SKILL.md` | 1504-1507 | Speckit cross-tool suggestion |
| `SKILL.md` | 747-775 | Dispute-Parsing Subsystem |
| `round-1/summary/final.md` | Full document | Phase 5 synthesis; 10 converged recommendations + 4 disputes |
| `round-1/arbitration/resolution.md` | Full document | Phase 6 arbiter advisory opinions on all 4 disputes |
| `round-1/functional-typing/disputes.md` | Full document | My Round 1 final positions and convergence record |
| `round-1/functional-typing/revision.md` | Full document | My Round 1 revised recommendations after cross-review |
| `conversus.yml` | Full document | Review configuration (rounds: 2, stagnation: detect, mode: cooperative) |
