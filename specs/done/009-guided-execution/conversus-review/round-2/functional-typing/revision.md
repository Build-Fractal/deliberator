# Revision: functional-typing (Round 2)

**Reviewer**: functional-typing
**Spec**: `009-guided-execution`
**Phase**: Round 2, Phase 3 (Revision)
**Date**: 2026-03-22

---

## Recommendation Dispositions

### From Round 1 Converged Recommendations

| # | Recommendation | Disposition | Notes |
|---|---------------|-------------|-------|
| 1 | P0: Replace `/conversus arbitrate` dead reference with actionable workaround | **Maintained** | No cross-review challenges. All three Round 2 reviews reaffirm. DA confirms three-location scope (lines 1469, 1488, 1489). |
| 2 | P1: Add `--output <dir>` flag to converge handler | **Maintained** | Uncontested across both rounds. |
| 3 | P1: Fix "Problem" label to "Mode" at SKILL.md line 1377 | **Maintained** | Uncontested. The label fix ships independently of the problem-statement addition. |
| 4 | P2: Document failure recovery position | **Maintained with scope note** | DA proposes expanding scope to cover pre-execution parsing failures alongside mid-execution failures. Both IA and FT cross-reviews accept substance but flag the expansion as a modification of a converged item. Disposition: accept the scope expansion as a noted refinement, not a new item. Implementation should address both failure paths. |
| 5 | P2: Make delegation semantics explicit in Execution section | **Maintained** | DA's re-examination confirms the fix also serves an efficiency purpose (avoids config re-parsing). No challenges. |
| 6 | P2: Add "What to Expect" narrative to pre-execution summary | **Maintained** | DA flags scope ceiling ("exactly one or two sentences"). My proposed multi-round extension is a separate P3 item, not a modification of this converged wording. |
| 7 | P2: Specify dispute-parsing file target as `{output}/summary/final.md` | **Maintained** | Uncontested. |
| 8 | P2: Add spec acknowledgment for cross-tool next steps (speckit) | **Maintained** | IA defers to implementer on positive vs. negative qualification wording. DA notes the arbiter's negative qualification is the safer default. I accept negative qualification as the default framing. |

### From Round 1 Disputed Items

| # | Recommendation | Disposition | Round 2 Resolution |
|---|---------------|-------------|-------------------|
| D1 | P2: Add problem statement to pre-execution summary | **Accepted at P2** | IA concedes in Round 2 review. All three reviewers now agree on fix and priority. Full consensus at P2. The arbiter's categorical-difference argument persuaded IA. I accepted P2 sequencing (separate from the P1 label fix) per the arbiter's bridging recommendation. DA's "seven instrumentalities and zero purposes" framing is the definitive articulation. |
| D2 | P2: Add prior context disclosure to pre-execution summary | **Accepted at P2** | IA moves from P3 to P2 in Round 2 review, accepting the arbiter's analysis of prior files as uniquely invisible inputs and acknowledging Constraint 2. Full consensus at P2. |
| D3 | P3: Document mtime staleness false-positive limitation | **Formally adopted at P3** | All three reviewers explicitly adopt in Round 2. Was never substantively opposed. Procedural gap from Round 1 now closed. |
| D4 | P1: Fix Important Notes formula arithmetic | **Revised to P1** | I revised from P2 to P1 in my Round 2 review, accepting the arbiter's audience argument. DA also moves to P1. IA maintains P1. Full consensus at P1. |

### From Round 2 New Observations

| # | Recommendation | Disposition | Cross-Review Reception |
|---|---------------|-------------|----------------------|
| N1 | P2: Articulate consent-surface disclosure criterion in spec | **Maintained as P2** | IA endorses the criterion substance but prefers it be folded into the P2 problem-statement and prior-context items as rationale text rather than tracked as a separate line item. DA endorses the criterion and notes it changes FR-001 from an enumerated list to a principled framework -- an accurate characterization. I accept that the practical outcome is identical whether this is a standalone item or rationale text accompanying the field-addition fixes. I defer to the synthesis on packaging but maintain that the criterion text should appear in the spec amendment, not merely in commit messages. |
| N2 | P3: Add multi-round explanation to "What to Expect" narrative | **Maintained as P3** | IA accepts the substance but notes it extends a converged item, requesting it be treated as conditional text for `rounds > 1` only. DA accepts the specific proposal but warns against establishing precedent for unbounded extensions, suggesting an explicit note that the narrative is not further extensible without review. Both concerns are valid. The one-sentence addition is conditional (fires only for multi-round configs) and bounded (no further extensions without deliberation). I accept both constraints. |

### From Other Reviewers' Round 2 Observations

| # | Source | Observation | Disposition |
|---|--------|------------|-------------|
| O1 | DA | Failure recovery scope should cover pre-execution parsing failures | **Accepted as scope refinement** of converged P2 item. See item 4 above. |
| O2 | DA | Arbiter field terms (trigger/timing/influence) may confuse non-experts | **Noted, not elevated.** DA self-retracted. The concern connects to the consent-surface criterion but the audience is too narrow for action in this round. Future design consideration. |
| O3 | IA | Speckit qualification: defer to implementer on positive vs. negative wording | **Accepted.** The negative qualification is the safer default per the arbiter. Either achieves the goal. |
| O4 | IA | Consent-surface criterion as rationale text, not standalone item | **Partially accepted.** See N1 above. The text should appear in the spec regardless of whether it is tracked as a separate line item. |

---

## New Recommendations

### 1. (Carried from review) P2: Consent-surface disclosure criterion

Reaffirmed from my Round 2 review. The criterion -- disclose any configured input that (a) influences agent output and (b) is not visible in the results -- should be stated in the FR-001 spec amendment. All three reviewers endorse the criterion substance. The packaging question (standalone item vs. rationale text) is a bookkeeping difference with no practical impact. The important thing is that the text appears in the spec, not just in deliberation artifacts.

Suggested spec text: "The pre-execution summary should disclose any configured input that influences agent output and is not visible in the deliberation results. This includes the problem definition, prior context files, and mode. It excludes templates (visible as output structure) and constitutions (visible as synthesis process rules)."

### 2. (Carried from review) P3: Multi-round narrative extension

Reaffirmed from my Round 2 review with the constraints accepted from cross-review: conditional on `rounds > 1`, bounded (no further extensions without deliberation). One sentence covering repetition, cumulative awareness, and early termination.

### 3. None additional

The recommendation set is comprehensive. No further gaps identified.

---

## Position Summary

Round 2 has achieved full consensus on every previously disputed item:

- **Dispute 1** (problem statement): Resolved at P2. IA conceded based on the categorical-difference argument. 3-0.
- **Dispute 2** (prior context): Resolved at P2. IA moved from P3 to P2 based on Constraint 2 and the unique-invisibility of prior files. 3-0.
- **Dispute 3** (mtime documentation): Resolved at P3. All three reviewers explicitly adopt. 3-0.
- **Dispute 4** (formula priority): Resolved at P1. I revised from P2 to P1; DA moved from neutral to P1; IA maintained P1. 3-0.

Two new items from Round 2 have partial consensus:
- The consent-surface criterion is endorsed in substance by all three reviewers; packaging differs (standalone P2 vs. rationale text). This is a bookkeeping question, not a substantive dispute.
- The multi-round narrative extension is accepted by all reviewers with scope constraints. No opposition to the substance.

The deliberation has been monotonically convergent across both rounds. No concessions have been reversed. No converged items have been reopened. The spec is ready for implementation with the agreed revisions.
