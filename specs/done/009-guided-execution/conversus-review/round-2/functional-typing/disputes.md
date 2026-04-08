# Disputes: functional-typing (Round 2)

**Reviewer**: functional-typing
**Spec**: `009-guided-execution`
**Phase**: Round 2, Phase 4 (Disputes)
**Date**: 2026-03-22

---

## Remaining Disputes

### None.

All four Round 1 disputes have been fully resolved in Round 2:

1. **Dispute 1** (problem-statement inclusion): Resolved at P2. Integration-architect conceded based on the arbiter's categorical-difference argument. 3-0 consensus. The P2 sequencing (separate from the P1 label fix) is accepted by all parties.

2. **Dispute 2** (prior context disclosure priority): Resolved at P2. Integration-architect moved from P3 to P2 based on Constraint 2's inherited-config scenario and the unique invisibility of prior files. 3-0 consensus.

3. **Dispute 3** (mtime false-positive documentation): Resolved at P3. All three reviewers explicitly adopted. This was never a substantive disagreement -- a procedural gap from Round 1 that has been closed. 3-0 consensus.

4. **Dispute 4** (formula correction priority): Resolved at P1. I revised from P2 to P1 based on the arbiter's audience argument (SKILL.md is an instruction document for LLM agents; internal arithmetic contradictions are functional bugs). Devils-advocate moved from neutral to P1 based on the same reasoning plus empirical evidence (the error misled their Round 1 analysis). Integration-architect maintained P1. 3-0 consensus.

### Packaging Question (Not a Dispute)

The consent-surface disclosure criterion is endorsed in substance by all three reviewers. The only open question is whether it should be a standalone P2 line item (my preference) or rationale text folded into the P2 problem-statement and prior-context items (integration-architect's preference). This is a bookkeeping difference with no impact on implementation -- the text will appear in the spec amendment either way. I defer to the synthesis on packaging. This does not constitute a dispute because:

- The substance is agreed (the (a)+(b) criterion is correct)
- The text content is agreed (my proposed paragraph)
- The placement is agreed (in the spec amendment to FR-001)
- Only the tracking granularity differs

---

## Convergence

### Convergence Record (Full Deliberation)

| Item | Round 1 Status | Round 2 Status | Final |
|------|---------------|----------------|-------|
| P0: `/conversus arbitrate` dead reference fix | Consensus | Maintained | **Consensus** |
| P1: `--output <dir>` flag | Consensus | Maintained | **Consensus** |
| P1: "Problem" label to "Mode" | Consensus | Maintained | **Consensus** |
| P1: Formula arithmetic fix | Fix consensus, P1/P2 disputed | **Resolved at P1** | **Consensus** |
| P2: Problem-statement in summary | 2-1 majority at P2 | **IA conceded, 3-0 at P2** | **Consensus** |
| P2: Prior context disclosure | 2-1 majority at P2 | **IA moved P3 to P2, 3-0** | **Consensus** |
| P2: Failure recovery documentation | Consensus | Scope expanded to cover parsing failures | **Consensus** |
| P2: Delegation semantics | Consensus | Maintained | **Consensus** |
| P2: "What to Expect" narrative | Consensus | Maintained | **Consensus** |
| P2: Dispute-parsing file target | Consensus | Maintained | **Consensus** |
| P2: Speckit acknowledgment | Consensus | Maintained; negative qualification default | **Consensus** |
| P2: Consent-surface criterion (new) | N/A | Substance agreed; packaging TBD | **Near-consensus** |
| P3: Mtime false-positive documentation | Unopposed, unresolved | **All three adopt at P3** | **Consensus** |
| P3: Multi-round narrative extension (new) | N/A | Accepted with constraints | **Consensus** |
| Deferred: `--dry-run` | Consensus | Maintained | **Consensus** |
| Withdrawn: Staleness to `problem.md` | Consensus | Maintained | **Consensus** |
| Withdrawn: Content hashing | Consensus | Maintained | **Consensus** |

### Convergence Metrics

- **Round 1**: 8 converged, 4 disputed (all on priority/scope, not diagnosis)
- **Round 2**: 4 disputes resolved (all to full 3-0 consensus), 2 new items added (1 near-consensus, 1 consensus)
- **Final**: 14 active recommendations at full or near-consensus. Zero open disputes on substance. Zero reversed concessions. Zero reopened items.
- **Convergence trajectory**: Strictly monotonic across both rounds.

---

## Final Position Statement

The Round 2 deliberation achieved the best possible outcome: every open dispute from Round 1 has been resolved to full three-reviewer consensus, with no concessions reversed and no converged items destabilized.

The analytical path to resolution was substantive, not procedural. Each dispute was resolved because the arbiter's advisory opinions identified specific analytical gaps in the minority positions, and the minority reviewer (integration-architect in Disputes 1-3, myself in Dispute 4) accepted the reasoning on its merits rather than deferring to authority. The most significant position change was integration-architect's concession on Disputes 1 and 2, which required acknowledging that the problem statement and prior files are categorically different from templates and constitutions -- a distinction the Round 1 deliberation identified but did not fully resolve.

My position update on Dispute 4 -- revising from P2 to P1 -- reflects a genuine analytical shift. The arbiter's framing that SKILL.md's audience is LLM agents changes the severity calculus for internal contradictions in the document. This was not a concession to authority but a recognition that I had underweighted the audience factor in my Round 1 analysis.

The two new items from this round (consent-surface criterion, multi-round narrative) extend the recommendation set without reopening prior agreements. Both are endorsed by all three reviewers. The consent-surface criterion is particularly valuable as a governing principle that prevents future disputes of the same class as Disputes 1, 2, and 3.

The spec and its SKILL.md implementation are ready for implementation. The converge handler is a structurally sound, architecturally constrained UX wrapper around the run engine. The recommendation set is comprehensive, prioritized, and at full consensus. The cooperative deliberation process worked as designed -- it produced findings that no single reviewer would have reached alone, resolved disagreements through analytical engagement rather than authority or exhaustion, and converged monotonically toward a complete and actionable revision plan.
