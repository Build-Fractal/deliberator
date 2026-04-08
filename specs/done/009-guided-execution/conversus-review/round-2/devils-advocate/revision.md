# Revision: devils-advocate (Round 2)

**Reviewer**: devils-advocate
**Spec**: `009-guided-execution`
**Phase**: Round 2, Phase 3 (Revision)
**Date**: 2026-03-22

---

## Recommendation Dispositions

### From Round 1 Converged Recommendations

| # | Recommendation | Disposition | Notes |
|---|---------------|-------------|-------|
| 1 | P0: Replace `/conversus arbitrate` dead reference with actionable workaround | **Maintained** | Re-examined in my Round 2 review. Confirmed three-location scope (lines 1469, 1488, 1489). The fix must hit all three plus the spec's FR-009 text. |
| 2 | P1: Add `--output <dir>` flag to converge handler | **Maintained** | Uncontested. |
| 3 | P1: Fix "Problem" label to "Mode" at SKILL.md line 1377 | **Maintained** | Uncontested. |
| 4 | P2: Document failure recovery position | **Maintained with scope expansion** | I proposed in my Round 2 review that this should cover both pre-execution parsing failures and mid-execution run failures. Both IA and FT cross-reviews accept the substance but flag it as an expansion of a converged item. I accept this characterization -- the scope refinement should be tracked as a Round 2 addition so implementers address both failure paths. The underlying principle is the same: translate errors to plain language for the SC-001 persona. |
| 5 | P2: Make delegation semantics explicit in Execution section | **Maintained** | Re-examined in Round 2 review. The fix also serves efficiency (avoids config re-parsing in the agent's context window). |
| 6 | P2: Add "What to Expect" narrative to pre-execution summary | **Maintained with scope ceiling** | I flagged in my Round 2 review that this must not become a process tutorial. "Exactly one or two sentences." FT's multi-round extension is a separate P3 item and fits within this ceiling. I accept FT's proposed one-sentence multi-round extension with two constraints: (1) conditional on `rounds > 1`, (2) no further extensions without review. |
| 7 | P2: Specify dispute-parsing file target as `{output}/summary/final.md` | **Maintained** | Uncontested. |
| 8 | P2: Add spec acknowledgment for cross-tool next steps (speckit) | **Maintained** | IA defers to implementer on wording. I recommend the negative qualification ("informational and tool-availability-dependent") as the safer default, per the arbiter's reasoning. This avoids creating precedent for arbitrary cross-tool additions. |

### From Round 1 Disputed Items

| # | Recommendation | Disposition | Round 2 Resolution |
|---|---------------|-------------|-------------------|
| D1 | P2: Add problem statement to pre-execution summary | **Maintained at P2** | IA concedes in Round 2, accepting the arbiter's categorical-difference argument. Full consensus at P2. My structural argument -- the summary discloses seven instrumentalities and zero purposes -- is the definitive articulation of why the problem statement is categorically different. The arbiter's P2 sequencing (separate from the P1 label fix) is the correct landing point. |
| D2 | P2: Add prior context disclosure to pre-execution summary | **Maintained at P2** | IA moves from P3 to P2. Full consensus. The arguments are fully developed. Prior files are the only configured input that is both invisible in results and influential over every agent. |
| D3 | P3: Document mtime staleness false-positive limitation | **Resolved at P3** | All three reviewers explicitly adopt. I accepted P3 in my Round 2 review and stated I would not raise the issue again. This is the least consequential dispute and P3 is appropriate for a one-sentence addition. |
| D4 | P1: Fix Important Notes formula arithmetic | **Revised to P1** | I explicitly aligned with P1 in my Round 2 review, joining IA's position. FT also revised to P1. The arbiter's audience argument is correct: SKILL.md is an executable instruction set for LLM agents, not traditional documentation. The error demonstrably misled my Round 1 analysis -- this is empirical evidence of harm, not hypothetical risk. Full consensus at P1. |

### From Round 2 New Observations

| # | Source | Observation | Disposition |
|---|--------|------------|-------------|
| N1 | FT | P2: Consent-surface disclosure criterion in spec | **Endorsed in substance.** The (a)+(b) criterion validates the 2-1 majority positions on Disputes 1 and 2. FT's proposed text is the most concrete articulation. I note (per my cross-review of FT) that this changes FR-001 from an enumerated list to a principled framework -- a deliberate architectural choice, not a minor documentation addition. I support this change. Whether it is tracked as a standalone P2 item or as rationale text accompanying the field additions is a bookkeeping question. |
| N2 | FT | P3: Multi-round narrative extension | **Accepted with constraints.** See item 6 above. The one-sentence addition is within the scope ceiling. Constraints: conditional on `rounds > 1`, not further extensible without review. |
| N3 | Self | Failure recovery scope expansion | See item 4 above. Accepted as a scope refinement by both cross-reviewers. |
| N4 | Self | Arbiter field readability concern | **Self-retracted.** The audience (users inheriting hand-crafted configs with arbiters) is too narrow for action. Noted as a future design consideration connected to the consent-surface criterion. Both cross-reviewers concur with the retraction. |
| N5 | Self | Post-execution speckit suggestion review | **Self-retracted.** I noted on second reading that the no-disputes case is well-structured. No gap. |

---

## New Recommendations

None additional beyond what was proposed in my Round 2 review. The failure recovery scope expansion (N3) is a refinement of an existing item, not a new recommendation. I endorse FT's two new items (consent-surface criterion and multi-round narrative) as described in the dispositions above.

---

## Position Summary

Round 2 achieved full convergence on every previously disputed item. My position changes:

1. **Dispute 4** (formula priority): Moved from neutral/unstated to P1. The arbiter's audience argument and the empirical evidence from this review cycle (the error misled my own analysis) are dispositive. This is a bug in an executable instruction set, not a documentation quality issue.

2. **Dispute 3** (mtime documentation): Accepted P3. This was the least consequential dispute. One sentence, zero cost, no opposition.

All concessions from Round 1 remain in place:
- Content hashing belongs in spec 008. Withdrawn.
- Mtime is acceptable as best-effort for spec 009. Accepted.
- Formula root cause is an algebra error (dropped Phase 4 term). Accepted.
- Speckit integration is spec-underauthorized, not spec-drifted. Softened framing accepted.
- FR-004 sub-case expansion is scoped to the guided-workflow path. Accepted.

The deliberation has been monotonically convergent. The recommendation set is comprehensive, prioritized, and at full consensus on every item. The spec is ready for implementation.

No new substantive disputes remain. The only open question is the packaging of the consent-surface criterion (standalone P2 item vs. rationale text), which is a bookkeeping difference that does not affect implementation.
