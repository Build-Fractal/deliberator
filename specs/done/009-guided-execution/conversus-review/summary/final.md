# Cross-Round Synthesis: 009-Guided-Execution

**Spec**: `009-guided-execution`
**Mode**: cooperative
**Agents**: functional-typing, integration-architect, devils-advocate
**Synthesizer**: cross-round (final)
**Rounds completed**: 2 of 2 (terminated: max_rounds)
**Date**: 2026-03-22

---

## Process Summary

Two rounds of cooperative deliberation were conducted by three specialized reviewers against spec 009-guided-execution and its SKILL.md implementation (the Converge handler, lines 1326-1508). The spec defines `/conversus converge` as a guided UX wrapper around the existing `/conversus run` engine -- pre-flight confirmation, delegation to the run engine, and post-flight interpretation -- with zero new execution logic.

**Round 1** produced twelve substantive recommendations. Eight reached full three-reviewer consensus. Four remained narrowly disputed -- all on priority calibration or scope boundaries, not on diagnosis or fix direction. An arbiter issued advisory opinions on all four disputes, providing analytical frameworks (categorical-difference, unique-invisibility, audience-specific severity) without exercising decision authority.

**Round 2** was charged with engaging the arbiter's advisory opinions and identifying any new issues. It achieved total convergence: all four Round 1 disputes resolved to full three-reviewer consensus, two new items were added with unanimous support, and one existing item's scope was expanded. Zero Round 1 concessions were reversed.

The core architectural finding is unanimous across both rounds: the converge handler is a structurally sound, zero-new-engine-logic UX wrapper. All ten functional requirements (FR-001 through FR-010) are satisfied. Both spec constraints hold (no new engine logic; no walled garden requiring prior guided workflow). All four success criteria (SC-001 through SC-004) are met.

---

## Dispute Trajectory

Four disputes emerged from Round 1. All four followed the same pattern: substantive agreement on diagnosis and fix direction, with narrow disagreement on priority or scope. The arbiter's advisory opinions provided dispositive analytical frameworks in each case. All four resolved to 3-0 consensus in Round 2.

### Dispute 1: Problem statement inclusion in the pre-execution summary

| Round | State |
|-------|-------|
| Round 1 | 2-1 majority at P2 (functional-typing + devils-advocate). Integration-architect deferred to follow-up, citing spec-amendment scope concern. |
| Arbitration | Advisory: P2. The problem statement is categorically different from templates/constitutions -- it is the purpose of the deliberation, not an instrumentality. The slippery-slope argument fails because the problem statement is the only undisclosed item in the "purpose" category. |
| Round 2 | 3-0 at P2. Integration-architect conceded, accepting the categorical-difference argument. Devils-advocate's framing -- "seven instrumentalities and zero purposes" -- was the definitive articulation. |

### Dispute 2: Prior context disclosure priority (P2 vs. P3)

| Round | State |
|-------|-------|
| Round 1 | 2-1 at P2 (functional-typing + devils-advocate) vs. P3 (integration-architect). |
| Arbitration | Advisory: P2. Prior files are uniquely invisible -- they influence every agent's context window with no trace in summary or results. The user-awareness assumption is undermined by Constraint 2's inherited-config scenario. |
| Round 2 | 3-0 at P2. Integration-architect acknowledged underweighting Constraint 2 and moved from P3 to P2. |

### Dispute 3: Mtime staleness false-positive documentation

| Round | State |
|-------|-------|
| Round 1 | 1-0-0 (procedural gap). Devils-advocate proposed; functional-typing and integration-architect did not oppose but did not adopt into their consolidated lists. |
| Arbitration | Advisory: Adopt at P3. No reviewer opposes. The false-positive occurs at the consent surface, the one moment the guided flow asks for trust. |
| Round 2 | 3-0 at P3. All three explicitly adopted. The arbiter's characterization as a "procedural gap" was accepted by all reviewers. |

### Dispute 4: Important Notes formula correction priority (P1 vs. P2)

| Round | State |
|-------|-------|
| Round 1 | 1-1-neutral. Integration-architect at P1, functional-typing at P2, devils-advocate unstated. |
| Arbitration | Advisory: P1. SKILL.md is an instruction document for LLM agents. An internal arithmetic contradiction consumed by automated agents during execution planning is functionally a code bug, not a documentation typo. |
| Round 2 | 3-0 at P1. Functional-typing revised from P2 to P1 (accepted audience argument). Devils-advocate moved from neutral to P1 (cited empirical evidence: the error misled their own Round 1 analysis). |

---

## Convergence Progression

| Metric | Round 1 | After Arbitration | Round 2 Final |
|--------|---------|-------------------|---------------|
| Items with full consensus | 8 | 8 (advisory only, no binding changes) | 15 |
| Items with majority (2-1) | 2 | 2 | 0 |
| Items with split (1-1) | 1 | 1 | 0 |
| Procedural gaps (1-0-0) | 1 | 1 | 0 |
| Open disputes | 4 | 4 | 0 |
| New items added | -- | -- | 2 |
| Items with expanded scope | -- | -- | 1 |
| Concessions reversed | -- | -- | 0 |

Convergence was strictly monotonic across both rounds. Positions moved exclusively toward agreement with no oscillation or backsliding. No converged item was destabilized or reopened. This is the strongest possible convergence outcome for a two-round cooperative review.

---

## Final Recommendation Set

### P0

**1. Replace `/conversus arbitrate` dead reference with actionable workaround**

Status: Full consensus (Round 1, reaffirmed Round 2).

The post-execution report at SKILL.md lines 1469, 1488-1489 suggests `/conversus arbitrate` as a next step. The dispatch table (line 34) lists `arbitrate` as "not yet implemented." A non-expert following the guided flow hits an error at the moment they most need guidance.

Fix: Replace the `/conversus arbitrate` suggestion with: "To resolve disputes, add an `arbiter:` section to `conversus.yml` and re-run `/conversus converge`. (A dedicated `/conversus arbitrate` subcommand is planned.)" Update spec FR-009 to say "suggest how to resolve disputes" rather than naming a specific unimplemented subcommand.

### P1

**2. Add `--output <dir>` flag to the converge handler**

Status: Full consensus (Round 1, uncontested at every phase).

Upstream handlers (`define`, `interests`, `mode`) all accept `--output <dir>`. The converge handler reads only from the working directory (line 1336). A user who ran the guided workflow with `--output my-delib/` cannot use `converge` without changing directories or moving files.

Fix: Add `--output <dir>` to the converge handler, using it as the working directory for config lookup, execution delegation, and report output.

**3. Fix "Problem" label to "Mode" at SKILL.md line 1377**

Status: Full consensus on label fix (Round 1). Problem-statement inclusion resolved to full consensus at P2 (Round 2); see item 6.

The pre-execution summary template at line 1377 labels its first field `Problem:` but fills it with the mode description. The post-execution report correctly uses `Mode:` at line 1439.

Fix (minimum): Change line 1377 from `Problem: {mode in plain language}` to `Mode: {mode in plain language}`.

**4. Fix Important Notes formula arithmetic (lines 1517-1525)**

Status: Full consensus at P1 (resolved in Round 2; was 1-1-neutral in Round 1).

The Important Notes simplified formula disagrees with the Step 4 formula for N=3, iterations=1 (Step 4 yields 16; Important Notes claims 13). Root cause: the Important Notes section drops the Phase 4 (Disputes) term of N agents. The expanded form `N + N*(N-1) + N + N + 1` simplifies to `N^2 + 2N + 1`, but the text claims `N^2 + N + 1`.

Fix:
- Line 1517: `N^2 + N + 1` becomes `N^2 + 2N + 1`
- Line 1518: `N^2 + N + 2` becomes `N^2 + 2N + 2`
- Line 1519: "13 total agent launches" becomes "16 total agent launches"
- Line 1520: "14 total agent launches" becomes "17 total agent launches"
- Line 1524: "3 * 13 + 1 = 40" becomes "3 * 16 + 1 = 49"

The converge handler (line 1404) already uses the correct formula.

### P2

**5. Add prior context disclosure to the pre-execution summary**

Status: Full consensus at P2 (resolved in Round 2; was 2-1 in Round 1).

Prior files silently influence every agent's context window. They have no trace in either the pre-execution summary or the deliberation results. The user who confirms execution is not necessarily the user who configured the prior files (Constraint 2 explicitly envisions inherited configs).

Fix: Add a conditional line to the pre-execution summary disclosing prior context files when configured.

**6. Add problem statement to the pre-execution summary**

Status: Full consensus at P2 (resolved in Round 2; was 2-1 in Round 1).

The pre-execution summary discloses seven instrumentalities (mode, agents, targets, output directory, rounds, iterations, launch count, arbiter) but not the purpose of the deliberation. A user who confirms execution without seeing what problem is being deliberated is consenting to something they cannot evaluate.

Fix: Add a `Problem:` field sourced from the first sentence or heading of `problem.md` when present; display "(hand-crafted config -- no problem.md)" when absent. Sequenced after the P1 label fix (item 3).

**7. Document failure recovery position (parsing + mid-execution failures)**

Status: Full consensus (Round 1, scope expanded in Round 2).

The spec does not address what happens when the delegated `/conversus run` fails. A non-expert who burns dozens of successful agent calls before a failure has no recovery path.

Fix: Add a failure-handling clause covering both paths: (1) for parsing failures, translate validation errors to plain language and suggest what to fix; (2) for mid-execution failures, translate engine errors, state that re-run is required, and defer resume capability to future work.

**8. Make delegation semantics explicit in the Execution section**

Status: Full consensus (Round 1, reaffirmed Round 2).

"Delegate to `/conversus run`" (line 1426) is ambiguous in a SKILL.md context. SKILL.md is an instruction set for an LLM agent, not code with function calls.

Fix: Revise line 1426 to: "Proceed to Run: Execution Step 1 through Step 5 using the config already parsed in the pre-execution summary. Do not re-invoke `/conversus run` as a separate skill invocation -- continue within the current conversation."

**9. Add a "What to Expect" narrative to the pre-execution summary**

Status: Full consensus (Round 1, extended in Round 2 with conditional multi-round text).

The bare agent launch count (e.g., "226 agent launches") is opaque to the SC-001 non-expert persona.

Fix: After the launch estimate line, add: "Each agent reads the target documents and writes a review. Agents then cross-review each other's work, revise, and a synthesis is produced." When `rounds > 1`, append: "In multi-round mode, the entire process repeats with awareness of prior round results. If agents stop changing their positions, the run terminates early (stagnation detection)."

**10. Specify dispute-parsing file target as `{output}/summary/final.md`**

Status: Full consensus (Round 1, reaffirmed Round 2).

Line 1464 says "Check the run engine's output" without specifying which file. In multi-round runs, multiple synthesis files exist.

Fix: At line 1464, specify: "Read `{output}/summary/final.md` (the cross-round synthesis for multi-round runs, or the Phase 5 synthesis for single-round runs)."

**11. Add spec acknowledgment for cross-tool next steps (speckit integration)**

Status: Full consensus (Round 1, refined in Round 2 with negative qualification framing).

The `/speckit.specify --input {output}/summary/final.md` next step at lines 1504-1507 appears only in the implementation, not in the spec. This is spec drift, not a bug.

Fix: Keep the speckit suggestion in SKILL.md. Add a qualifying note to the spec that cross-tool next steps under FR-008 are informational and tool-availability-dependent.

**12. Consent-surface disclosure criterion as rationale text in FR-001 amendment**

Status: New in Round 2, substance 3-0.

The deliberation surfaced a principled criterion for deciding what belongs in the pre-execution summary: disclose any configured input that (a) influences agent output and (b) is not visible in the deliberation results. This criterion correctly includes the problem definition and prior context files while excluding templates (visible as output structure) and constitutions (visible as synthesis process rules).

Fix: Record as rationale text in the FR-001 spec amendment. Suggested text: "The pre-execution summary should disclose any configured input that influences agent output and is not visible in the deliberation results. This includes the problem definition, prior context files, and mode. It excludes templates (visible as output structure) and constitutions (visible as synthesis process rules)."

### P3

**13. Document mtime staleness false-positive limitation**

Status: Full consensus at P3 (resolved in Round 2; was a procedural gap in Round 1).

The mtime staleness warning may fire after git operations that update file timestamps, producing a false positive at the consent surface.

Fix: Add one sentence to the staleness warning section: "This warning may appear after git operations that update file timestamps. It is safe to proceed if you have not changed your interests."

**14. Multi-round narrative extension in "What to Expect"**

Status: New in Round 2, all three accepted with constraints.

Fix: Conditional text appended to the "What to Expect" narrative only when `rounds > 1` (already incorporated in item 9 above). Scope ceiling is binding -- no further extensions to this narrative without a deliberation round.

### Deferred

**15. `--dry-run` capability for converge**

Status: Full consensus (out of scope for spec 009). All three reviewers identify it as a reasonable future enhancement. None consider it blocking.

### Withdrawn

**16. Extend staleness check to `problem.md`** -- belongs in spec 008, not spec 009. Unanimous.

**17. Replace mtime with content hashing** -- belongs in spec 008, not spec 009. Unanimous. Staleness mechanism improvements (content hashing, provenance metadata, source file tracking) should be embedded by the config generator, not verified by the config consumer.

---

## Resolution Attribution

Every dispute resolution and position change is traceable to specific analytical arguments, not authority or exhaustion.

| Resolution | Attributed To |
|------------|--------------|
| Problem-statement inclusion (P2) | Arbiter's categorical-difference argument (purpose vs. instrumentality); devils-advocate's "seven instrumentalities and zero purposes" framing |
| Prior context priority (P2) | Arbiter's unique-invisibility analysis; Constraint 2's inherited-config scenario |
| Mtime false-positive docs (P3) | Arbiter's procedural-gap characterization; devils-advocate's consent-surface observation |
| Formula priority (P1) | Arbiter's audience argument (SKILL.md as LLM instruction document); devils-advocate's empirical evidence (error misled their own Round 1 analysis) |

### Multi-reviewer discovery contributions

Three findings specifically required the multi-reviewer chain:

1. **Formula error**: Symptom identified by devils-advocate, root cause traced by functional-typing (dropped Phase 4 term), line-level fix specified by integration-architect. No single reviewer would have produced the complete diagnosis.

2. **Staleness scope reassignment**: Mechanism challenged by devils-advocate, scope extension proposed by integration-architect, both withdrawn through mutual challenge, unanimously reassigned to spec 008. The final position was one that no reviewer started with.

3. **`/conversus arbitrate` fix**: Dead reference identified by multiple reviewers, but the comprehensive fix (three-location scope, P0 severity calibration, combined workaround + planned-command note framing) emerged through multi-reviewer refinement.

---

<!-- DISPUTES_BEGIN -->

## Remaining Disputes

None. All four Round 1 disputes were resolved to full three-reviewer consensus in Round 2. The deliberation has no open disputes.

| Dispute | Round 1 Status | Round 2 Resolution | Final |
|---------|---------------|-------------------|-------|
| Problem-statement inclusion | 2-1 majority at P2 | IA conceded; 3-0 at P2 | **Resolved** |
| Prior context priority | 2-1 at P2 vs. P3 | IA moved to P2; 3-0 | **Resolved** |
| Mtime false-positive docs | 1-0-0 (procedural gap) | All three adopted at P3; 3-0 | **Resolved** |
| Formula priority | 1-1-neutral (P1 vs. P2) | FT and DA moved to P1; 3-0 | **Resolved** |

<!-- DISPUTES_END -->

---

## Termination Assessment

**Termination reason**: max_rounds (2 of 2 completed).

**Assessment**: Termination at max_rounds is clean. The deliberation achieved total convergence before the round limit -- all disputes were resolved in Round 2, two new items were added with full consensus, and no open disagreements remain. A hypothetical Round 3 would have no disputes to resolve and no position updates to process. The marginal value of additional rounds is zero.

**Convergence quality**: The strongest possible outcome for a two-round cooperative review. Monotonic convergence across both rounds with no oscillation, backsliding, or exhaustion-based concessions. Every position change is attributable to a specific analytical argument, not authority or fatigue.

**Implementation readiness**: The spec and SKILL.md are ready for implementation with the 14 actionable recommendations applied (3 at P0/P1, 8 at P2, 2 at P3, plus 1 deferred). The changes required are enumerated in both the Final Recommendation Set above and the Round 2 synthesis's "Spec Changes Required" section, which provides line-level implementation guidance.

**Architectural confidence**: The spec's most important invariant -- zero new execution logic -- survived adversarial review by all three agents across both rounds. Devils-advocate explicitly tested it (checking for phase orchestration, agent management, output file creation, and schema extension). The converge handler is confirmed as a pure UX wrapper.

---

## Consolidated Recommendation Table

| # | Priority | Recommendation | Status |
|---|----------|---------------|--------|
| 1 | **P0** | Replace `/conversus arbitrate` dead reference with actionable workaround + planned-command note | Consensus |
| 2 | **P1** | Add `--output <dir>` flag to converge handler | Consensus |
| 3 | **P1** | Fix "Problem" label to "Mode" at SKILL.md line 1377 | Consensus |
| 4 | **P1** | Fix Important Notes formula arithmetic (lines 1517-1525) | Consensus (resolved R2) |
| 5 | **P2** | Add prior context disclosure to pre-execution summary | Consensus (resolved R2) |
| 6 | **P2** | Add problem statement to pre-execution summary | Consensus (resolved R2) |
| 7 | **P2** | Document failure recovery position (parsing + mid-execution) | Consensus (scope expanded R2) |
| 8 | **P2** | Make delegation semantics explicit in Execution section | Consensus |
| 9 | **P2** | Add "What to Expect" narrative to pre-execution summary | Consensus (extended R2) |
| 10 | **P2** | Specify dispute-parsing file target as `{output}/summary/final.md` | Consensus |
| 11 | **P2** | Add spec acknowledgment for cross-tool next steps (speckit) | Consensus |
| 12 | **P2** | Consent-surface disclosure criterion as FR-001 rationale text | New R2, consensus |
| 13 | **P3** | Document mtime staleness false-positive limitation | Consensus (resolved R2) |
| 14 | **P3** | Multi-round narrative extension in "What to Expect" | New R2, consensus |
| 15 | **Deferred** | `--dry-run` capability for converge | Consensus (out of scope) |
| 16 | **Withdrawn** | Extend staleness check to `problem.md` (belongs in spec 008) | Consensus |
| 17 | **Withdrawn** | Replace mtime with content hashing (belongs in spec 008) | Consensus |
