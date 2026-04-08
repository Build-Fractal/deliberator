# Cooperative Synthesis: 009-Guided-Execution (Round 2)

**Spec**: `009-guided-execution`
**Mode**: cooperative
**Agents**: functional-typing, integration-architect, devils-advocate
**Synthesizer**: neutral (Phase 5)
**Round**: 2 of 2
**Date**: 2026-03-22
**Prior artifacts**: Round 1 synthesis (`round-1/summary/final.md`), Round 1 arbitration (`round-1/arbitration/resolution.md`)

---

## Deliberation Summary

Round 2 was charged with engaging the arbiter's advisory opinions on four narrow Round 1 disputes and determining whether any new issues emerged from a second reading of the target files. The round achieved total convergence: all four Round 1 disputes were resolved to full three-reviewer consensus, two new items were added with unanimous or near-unanimous support, and zero concessions from Round 1 were reversed.

The Round 1 synthesis identified twelve substantive recommendations, eight of which had full consensus and four of which were narrowly disputed on priority or scope. The arbiter issued advisory opinions on each dispute, providing analytical frameworks that proved dispositive in Round 2. Every disputed item is now resolved. The deliberation trajectory across both rounds has been strictly monotonic -- positions moved exclusively toward agreement, with no oscillation or backsliding.

The core architectural finding is reaffirmed: the converge handler is a structurally sound, zero-new-engine-logic UX wrapper around the existing run engine. All ten functional requirements are satisfied. Both constraints hold. All four success criteria are met. The recommendation set constitutes a targeted refinement plan, not structural changes.

---

## Resolution of Round 1 Disputes

### Dispute 1: Problem statement inclusion in the pre-execution summary

**Round 1 status**: 2-1 majority (functional-typing + devils-advocate at P2, integration-architect deferred to follow-up).

**Round 2 resolution**: Full consensus at P2. Integration-architect conceded.

Integration-architect accepted the arbiter's categorical-difference argument: the problem statement is the purpose of the entire deliberation, not an instrumentality comparable to templates or constitutions. The pre-execution summary already discloses mode, agents, targets, rounds, iterations, launch count, and arbiter configuration -- all of which are instrumentalities describing how the deliberation will run. The problem statement is the only input that describes what the deliberation is about. Devils-advocate's structural articulation -- "seven instrumentalities and zero purposes" -- was the definitive framing. Integration-architect's slippery-slope argument (adding one omitted dimension without addressing others creates inconsistency) failed because the problem statement is the only undisclosed item in the "purpose" category; there is no slope.

**Final recommendation**: Apply the P1 "Problem"-to-"Mode" label fix (converged in Round 1). Add the problem-statement field to the pre-execution summary as P2, sequenced after the label fix. Implementation: read the first sentence or heading from `problem.md` when present; display "(hand-crafted config -- no problem.md)" when absent.

### Dispute 2: Prior context disclosure priority -- P2 vs. P3

**Round 1 status**: 2-1 at P2 (functional-typing + devils-advocate) vs. P3 (integration-architect).

**Round 2 resolution**: Full consensus at P2. Integration-architect moved from P3 to P2.

Integration-architect accepted two arguments: (1) the arbiter's analysis that prior files are uniquely invisible -- they influence every agent's context window and have no trace in either the pre-execution summary or the deliberation results; and (2) Constraint 2's inherited-config scenario, which explicitly envisions users running configs they did not create. The user-awareness assumption (that the person who configured prior files knows they exist) is directly undermined by this constraint. Integration-architect acknowledged underweighting Constraint 2 in the Round 1 analysis.

**Final recommendation**: P2. Add a conditional line to the pre-execution summary disclosing prior context files when configured.

### Dispute 3: Mtime staleness false-positive documentation

**Round 1 status**: 1-0-0. Devils-advocate proposed; functional-typing and integration-architect did not oppose but did not adopt.

**Round 2 resolution**: Full consensus at P3. All three reviewers explicitly adopted.

This was a procedural gap, not a substantive disagreement. No reviewer ever opposed the one-sentence documentation addition. The arbiter's characterization -- that it "fell through the consolidation process" -- was accepted by all three reviewers. Devils-advocate's observation that the false-positive occurs at the consent surface (the one moment the guided flow asks for trust) reinforces the value of the addition. The proposed text: "This warning may appear after git operations that update file timestamps. It is safe to proceed if you have not changed your interests."

**Final recommendation**: P3. One sentence added to the staleness warning section.

### Dispute 4: Important Notes formula correction priority -- P1 vs. P2

**Round 1 status**: 1-1-neutral. Integration-architect at P1, functional-typing at P2, devils-advocate unstated.

**Round 2 resolution**: Full consensus at P1. Functional-typing revised from P2 to P1. Devils-advocate moved from neutral to P1.

The arbiter's audience argument was dispositive: SKILL.md is an instruction document for LLM agents, not traditional documentation. An internal arithmetic contradiction in an instruction document consumed by automated agents during execution planning is functionally closer to a code bug than a documentation typo. Both functional-typing and devils-advocate accepted this reframing. Devils-advocate added empirical evidence: the error demonstrably misled their Round 1 analysis, causing incorrect speculation about iteration handling when the real cause was a dropped Phase 4 term. Functional-typing acknowledged underweighting the audience factor.

**Final recommendation**: P1. Correct the Important Notes formula:
- Line 1517: `N^2 + N + 1` becomes `N^2 + 2N + 1`
- Line 1518: `N^2 + N + 2` becomes `N^2 + 2N + 2`
- Line 1519: "13 total agent launches" becomes "16 total agent launches"
- Line 1520: "14 total agent launches" becomes "17 total agent launches"
- Line 1524: "3 * 13 + 1 = 40" becomes "3 * 16 + 1 = 49"

---

## Round 2 New Items

### 1. P2: Consent-surface disclosure criterion (functional-typing proposal)

All three reviewers endorse the arbiter's disclosure criterion in substance: the pre-execution summary should disclose any configured input that (a) influences agent output and (b) is not visible in the deliberation results. This criterion correctly includes the problem definition and prior context files while excluding templates (visible as output structure) and constitutions (visible as synthesis process rules).

Functional-typing proposed formalizing this as a design note in the FR-001 spec amendment. Integration-architect endorsed the criterion but preferred it as rationale text accompanying the P2 problem-statement and prior-context fixes rather than a standalone tracked item. Devils-advocate endorsed the criterion and noted it changes FR-001 from an enumerated list to a principled framework -- a deliberate architectural choice.

**Synthesizer resolution**: The substance is 3-0 agreed. The packaging question (standalone item vs. rationale text) is a bookkeeping difference with no impact on implementation. Record as P2 rationale text accompanying the problem-statement and prior-context fixes. The text should appear in the spec amendment to FR-001 regardless of tracking granularity. This resolves the packaging question by choosing integration-architect's simpler framing while ensuring the text is written (which is functional-typing's substantive goal).

Suggested text for the spec amendment: "The pre-execution summary should disclose any configured input that influences agent output and is not visible in the deliberation results. This includes the problem definition, prior context files, and mode. It excludes templates (visible as output structure) and constitutions (visible as synthesis process rules)."

### 2. P3: Multi-round narrative extension (functional-typing proposal)

All three reviewers accept this in substance with two constraints:

1. The addition is conditional -- fires only when `rounds > 1`.
2. The "What to Expect" narrative is not further extensible without review.

Functional-typing's proposed text: "In multi-round mode, the entire process repeats with awareness of prior round results. If agents stop changing their positions, the run terminates early (stagnation detection)."

This is a one-sentence conditional extension of the converged P2 "What to Expect" narrative. Devils-advocate's scope ceiling ("one or two sentences, not a process tutorial") is respected. Integration-architect accepts the substance and the constraints.

**Synthesizer resolution**: P3. Conditional text appended to the "What to Expect" narrative only when `rounds > 1`. The scope ceiling is binding -- no further extensions to this narrative without a deliberation round.

### 3. Failure recovery scope expansion (devils-advocate refinement)

Devils-advocate proposed that the converged P2 failure recovery recommendation should cover both pre-execution parsing failures (translate schema validation errors to plain language for non-experts) and mid-execution run failures (translate engine errors, state that re-run is required). Both cross-reviewers accepted the substance but flagged it as a modification of a converged item from Round 1.

**Synthesizer resolution**: Accepted as a scope note on the existing P2 item. The original Round 1 convergence was specifically about mid-execution failures. The Round 2 expansion to cover pre-execution parsing failures is tracked as a scope addition. Implementation should address both failure paths: (1) for parsing failures, translate validation errors and suggest what to fix; (2) for mid-execution failures, translate engine errors and state that re-run is required.

---

## Converged Recommendations from Round 1 (Unchanged)

The following eight items from Round 1 remain unchanged. All were reaffirmed without modification in Round 2.

1. **P0**: Replace `/conversus arbitrate` dead reference with actionable workaround + planned-command note. Three locations (lines 1469, 1488, 1489) plus FR-009 spec text.

2. **P1**: Add `--output <dir>` flag to the converge handler.

3. **P1**: Fix "Problem" label to "Mode" at SKILL.md line 1377.

4. **P2**: Document the failure recovery position. (Scope expanded in Round 2 to cover parsing failures; see above.)

5. **P2**: Make delegation semantics explicit in the Execution section. Revise line 1426 to clarify "proceed to Run: Execution Step 1 through Step 5" within the current conversation.

6. **P2**: Add a "What to Expect" narrative to the pre-execution summary. (Extended in Round 2 with conditional multi-round text; see above.)

7. **P2**: Specify dispute-parsing file target as `{output}/summary/final.md`.

8. **P2**: Add spec acknowledgment for cross-tool next steps (speckit). Use negative qualification ("informational and tool-availability-dependent") as the default framing.

---

## Structural Findings (Unchanged from Round 1)

- **Staleness mechanism improvements belong in spec 008**, not spec 009. Content hashing, provenance metadata, and `problem.md` staleness checking are all spec 008 responsibilities. The converge handler's mtime heuristic is acceptable as best-effort for spec 009.

- **`--dry-run` is deferred**. All three reviewers identify it as a reasonable future enhancement. None consider it blocking for spec 009.

---

<!-- DISPUTES_BEGIN -->

## Remaining Disputes

None. All four Round 1 disputes have been resolved to full three-reviewer consensus in Round 2. The deliberation has no open disputes.

For the record, the resolution of each dispute:

| Dispute | Round 1 Status | Round 2 Resolution | Final |
|---------|---------------|-------------------|-------|
| Problem-statement inclusion | 2-1 majority at P2 | IA conceded; 3-0 at P2 | **Resolved** |
| Prior context priority | 2-1 at P2 vs. P3 | IA moved to P2; 3-0 | **Resolved** |
| Mtime false-positive docs | 1-0-0 (procedural gap) | All three adopted at P3; 3-0 | **Resolved** |
| Formula priority | 1-1-neutral (P1 vs. P2) | FT and DA moved to P1; 3-0 | **Resolved** |

<!-- DISPUTES_END -->

---

## Final Recommendation Table (Complete, Round 2)

| Priority | Recommendation | Status | Round 2 Change |
|----------|---------------|--------|----------------|
| **P0** | Replace `/conversus arbitrate` dead reference with actionable workaround + planned-command note (lines 1469, 1488, 1489 + FR-009 spec text) | Consensus | None |
| **P1** | Add `--output <dir>` flag to converge handler | Consensus | None |
| **P1** | Fix "Problem" label to "Mode" at SKILL.md line 1377 | Consensus | None |
| **P1** | Fix Important Notes formula arithmetic (lines 1517-1525) | **Consensus (resolved)** | FT revised P2 to P1; DA moved neutral to P1; now 3-0 at P1 |
| **P2** | Add problem statement to pre-execution summary | **Consensus (resolved)** | IA conceded; now 3-0 at P2 |
| **P2** | Add prior context disclosure to pre-execution summary | **Consensus (resolved)** | IA moved P3 to P2; now 3-0 |
| **P2** | Document failure recovery position (parsing + mid-execution failures) | Consensus | Scope expanded in Round 2 to cover parsing failures |
| **P2** | Make delegation semantics explicit in Execution section | Consensus | None |
| **P2** | Add "What to Expect" narrative to pre-execution summary | Consensus | None |
| **P2** | Specify dispute-parsing file target as `{output}/summary/final.md` | Consensus | None |
| **P2** | Add spec acknowledgment for cross-tool next steps (speckit) | Consensus | Negative qualification as default framing |
| **P2** | Consent-surface disclosure criterion as rationale text in FR-001 amendment | **New (Round 2)** | Substance 3-0; recorded as rationale text per synthesizer resolution |
| **P3** | Document mtime staleness false-positive limitation | **Consensus (resolved)** | All three explicitly adopted; procedural gap closed |
| **P3** | Multi-round explanation in "What to Expect" narrative | **New (Round 2)** | Conditional on `rounds > 1`; scope ceiling binding |
| **Deferred** | `--dry-run` capability for converge | Consensus | None |
| **Withdrawn** | Extend staleness check to `problem.md` (belongs in spec 008) | Consensus | None |
| **Withdrawn** | Replace mtime with content hashing (belongs in spec 008) | Consensus | None |

---

## Spec Changes Required

### Changes to `specs/009-guided-execution/spec.md`

1. **FR-001 amendment**: Add the problem definition and prior context files to the summary field list. Include the consent-surface disclosure criterion as a rationale note.

2. **FR-009 amendment**: Replace "suggest `/conversus arbitrate`" with "suggest how to resolve disputes" (avoid naming a specific unimplemented subcommand).

3. **Failure recovery clause**: Add language addressing both pre-execution parsing failures and mid-execution run failures, stating that failures require a full re-run.

4. **Cross-tool next steps acknowledgment**: Add a note that FR-008's "suggested next steps based on outcome" may include cross-tool suggestions that are informational and tool-availability-dependent.

### Changes to `SKILL.md` (Converge Handler, lines 1326-1545)

1. **Line 1377**: Change `Problem:` to `Mode:` in the pre-execution summary template.

2. **Lines 1374-1393**: Add `Problem:` field (sourced from `problem.md` first sentence/heading, with fallback for hand-crafted configs). Add `Prior context:` field (conditional, when `prior:` is configured). Add "What to Expect" narrative after the launch estimate. Add multi-round explanation (conditional, when `rounds > 1`).

3. **Line 1362-1364**: Add one sentence to the staleness warning noting that git operations may trigger false positives.

4. **Line 1370**: Expand parsing-failure guidance for non-experts (translate validation errors, suggest what to fix).

5. **Line 1426**: Revise delegation instruction: "Proceed to Run: Execution Step 1 through Step 5 using the config already parsed in the pre-execution summary. Do not re-invoke `/conversus run` as a separate skill invocation -- continue within the current conversation."

6. **Line 1464**: Specify file target: "Read `{output}/summary/final.md`."

7. **Lines 1469, 1488, 1489**: Replace `/conversus arbitrate` with workaround text + planned-command note.

8. **Lines 1504-1507**: Keep the speckit suggestion. (No SKILL.md change needed; the spec amendment provides the authorization.)

9. **Lines 1517-1525**: Correct the Important Notes formula arithmetic.

10. **Add `--output <dir>` flag**: Add flag handling before the prerequisite check (line 1336), using the specified directory as the working directory for config lookup, execution delegation, and report output.

---

## Process Observations (Round 2)

### The arbiter's advisory opinions were dispositive

All four Round 1 disputes were resolved in Round 2 after reviewers engaged with the arbiter's reasoning. The arbiter did not resolve disputes by authority -- the resolution document explicitly states advisory-only influence. Instead, the arbiter provided analytical frameworks (categorical-difference, unique-invisibility, audience-specific severity) that identified specific gaps in minority positions. Each conceding reviewer cited the arbiter's reasoning as the basis for their position update, not the arbiter's authority. This validates the advisory-influence model: the arbiter's value is analytical clarity, not decision-making power.

### Monotonic convergence held across both rounds

The deliberation trajectory was strictly monotonic: 8 consensus items in Round 1, 12 after Round 1 dispute resolution attempts, and 15 at full or near-full consensus after Round 2. No concession was reversed across either round. No converged item was destabilized or reopened. This is the strongest possible convergence outcome for a two-round cooperative review. The monotonicity indicates that the reviewers' position changes were genuine analytical updates rather than strategic moves or exhaustion-based concessions.

### Multi-reviewer discovery validated

Round 1's synthesis identified three findings that specifically required the multi-reviewer chain. Functional-typing's Round 2 review offered a precision correction: one of the three (the `/conversus arbitrate` fix) demonstrates multi-reviewer refinement rather than multi-reviewer discovery. The distinction is valid -- any single reviewer could have identified the dead reference, but the multi-reviewer chain produced the comprehensive fix (three-location scope, severity calibration, planned-command note). Two of three cited examples remain as genuine multi-reviewer discoveries (the formula error chain and the staleness scope reassignment). The cooperative process adds value through both discovery and refinement, which are different but complementary contributions.

### The zero-new-engine-logic constraint survived

All three reviewers independently verified this constraint across both rounds. Devils-advocate explicitly tested it in Round 1 (checking for phase orchestration, agent management, output file creation, and schema extension). The arbiter noted it "survived through adversarial review." This is the spec's most important architectural invariant and it is confirmed with high confidence.

---

## Conclusion

The spec 009 guided execution deliberation is complete. Two rounds of cooperative review by three specialized agents produced a comprehensive, fully-converged revision plan with 15 actionable items (3 at P0/P1, 8 at P2, 2 at P3, plus 2 withdrawn and 1 deferred). Zero disputes remain. The converge handler is architecturally sound and ready for implementation with the targeted refinements described above.
