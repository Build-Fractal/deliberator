# Cooperative Synthesis: 009-Guided-Execution

**Spec**: `009-guided-execution`
**Mode**: cooperative
**Agents**: functional-typing, integration-architect, devils-advocate
**Synthesizer**: neutral (Phase 5)
**Date**: 2026-03-22

---

## Deliberation Summary

Three reviewers examined spec 009-guided-execution and its SKILL.md implementation (the Converge handler, lines 1326-1508) across four phases: independent review, cross-review, revision, and disputes. The spec defines `/conversus converge` as a guided UX wrapper around the existing `/conversus run` engine -- pre-flight confirmation, delegation, and post-flight interpretation -- with zero new execution logic.

All three reviewers independently verified that the implementation satisfies all ten functional requirements (FR-001 through FR-010), upholds both spec constraints (no new engine logic, no walled garden), and meets all four success criteria (SC-001 through SC-004). The converge handler is confirmed as a pure UX wrapper: it reads configuration, presents a summary, obtains confirmation, delegates to the run engine, and reports results. It creates no new artifacts, extends no schema, and introduces no phase orchestration.

The deliberation produced twelve substantive recommendations, of which eight reached full consensus and four remain narrowly disputed on priority or scope -- not on the underlying diagnosis or fix direction.

---

## Converged Recommendations

The following recommendations achieved full three-reviewer consensus on problem, fix, and priority. These constitute the actionable revision plan.

### 1. P0: Replace `/conversus arbitrate` dead reference with actionable workaround

**Status**: Full consensus (all three reviewers).

The post-execution report at SKILL.md lines 1469 and 1488-1489 suggests `/conversus arbitrate` as a next step when disputes remain. The dispatch table (line 34) lists `arbitrate` as "not yet implemented." A non-expert following the guided flow will hit an "Unknown subcommand" error at the moment they most need guidance.

**Agreed fix**: Replace the `/conversus arbitrate` suggestion with: "To resolve disputes, add an `arbiter:` section to `conversus.yml` and re-run `/conversus converge`. (A dedicated `/conversus arbitrate` subcommand is planned.)" Update the spec's FR-009 text to say "suggest how to resolve disputes" rather than naming a specific subcommand. This provides an actionable path today and sets expectations for future capability.

Integration-architect established P0 severity; functional-typing elevated from P1 to P0 in revision; devils-advocate endorsed the combined fix (plain-language dispute explanation + workaround + planned-command note).

### 2. P1: Add `--output <dir>` flag to the converge handler

**Status**: Full consensus, uncontested at every phase.

The upstream handlers (`define`, `interests`, `mode`) all accept `--output <dir>`. The converge handler reads only from the working directory (line 1336). A user who ran the guided workflow with `--output my-delib/` cannot use `converge` without changing directories or moving files.

**Agreed fix**: Add `--output <dir>` to the converge handler, using it as the working directory for config lookup, execution delegation, and report output.

### 3. P1: Fix "Problem" label to "Mode" at SKILL.md line 1377

**Status**: Full consensus on the label fix. Problem-statement inclusion remains disputed (see Dispute 1).

The pre-execution summary template at line 1377 labels its first field `Problem:` but fills it with the mode and its plain-language explanation. The post-execution report correctly uses `Mode:` at line 1439. This internal inconsistency misleads users into believing the field shows the problem definition from `problem.md`.

**Agreed fix (minimum)**: Change line 1377 from `Problem: {mode in plain language}` to `Mode: {mode in plain language}`.

### 4. P2: Document the failure recovery position

**Status**: Full consensus (all three reviewers converged independently).

The spec does not address what happens when the delegated `/conversus run` fails mid-execution. A non-expert who burns dozens of successful agent calls before a Phase 5 failure has no recovery path and no guidance.

**Agreed fix**: Add a failure-handling clause to the spec and SKILL.md handler that: (1) translates engine errors to plain language, (2) states explicitly that failures require a full re-run, and (3) defers resume capability to future work. This costs one paragraph and sets correct expectations within the zero-new-engine-logic constraint.

### 5. P2: Make delegation semantics explicit in the Execution section

**Status**: Full consensus.

"Delegate to `/conversus run`" (line 1426) is ambiguous in a SKILL.md context. The SKILL.md is an instruction set for an LLM agent, not code with function calls. The agent must correctly interpret "delegate" as "proceed to the Run handler sections," but this is implicit.

**Agreed fix**: Revise line 1426 to: "Proceed to Run: Execution Step 1 through Step 5 using the config already parsed in the pre-execution summary. Do not re-invoke `/conversus run` as a separate skill invocation -- continue within the current conversation."

### 6. P2: Add a "What to Expect" narrative to the pre-execution summary

**Status**: Full consensus.

All three reviewers agree that the bare agent launch count (e.g., "226 agent launches") is opaque to the SC-001 non-expert persona. Token/time estimates are impractical without engine instrumentation that does not exist.

**Agreed fix**: After the launch estimate line, add a brief process explanation: "Each agent reads the target documents and writes a review. Agents then cross-review each other's work, revise, and a synthesis is produced." This transforms an opaque number into a comprehensible process at zero implementation cost.

### 7. P2: Specify dispute-parsing file target as `{output}/summary/final.md`

**Status**: Full consensus.

Line 1464 says "Check the run engine's output" without specifying which file to parse. In multi-round runs, multiple synthesis files exist in the output tree. An LLM agent executing this instruction could parse a per-round synthesis rather than `final.md`.

**Agreed fix**: At line 1464, specify: "Read `{output}/summary/final.md` (the cross-round synthesis for multi-round runs, or the Phase 5 synthesis for single-round runs)."

### 8. P2: Add spec acknowledgment for cross-tool next steps (speckit integration)

**Status**: Full consensus on the approach; minor drafting-preference tension on wording (see Dispute 4 in integration-architect's disputes, characterized as nearly converged).

The `/speckit.specify --input {output}/summary/final.md` next step at SKILL.md lines 1504-1507 appears only in the implementation, not in spec 009. Devils-advocate identified this as spec drift. Functional-typing and integration-architect reframed it as a reasonable implementation choice under FR-008's open-ended "suggested next steps based on outcome."

**Agreed fix**: Keep the speckit suggestion. Add a qualifying note to the spec that cross-tool next steps under FR-008 are informational and tool-availability-dependent. This explicitly authorizes the existing behavior without removing a useful UX affordance.

### 9. Staleness mechanism improvements belong in spec 008, not spec 009

**Status**: Full consensus (structural agreement).

Devils-advocate proposed content hashing; integration-architect proposed extending mtime checks to `problem.md`. Through mutual challenge, all three converged on a conclusion none started with: provenance metadata (content hashes, source file tracking) should be embedded by the config generator (spec 008), not verified by the config consumer (spec 009). The converge handler's mtime heuristic is acceptable as a best-effort mechanism for spec 009.

Devils-advocate retains one documentation request: the SKILL.md should note that the mtime warning may fire after git operations that update file timestamps. This request was not explicitly opposed but was not adopted into any reviewer's consolidated list. See Dispute 3 in the Remaining Disputes section.

### 10. `--dry-run` is deferred

**Status**: Full consensus (out of scope for spec 009).

All three reviewers identify `--dry-run` as a reasonable future enhancement. None consider it blocking.

---

## Important Notes Formula Correction

**Status**: Full consensus on the diagnosis and fix direction. Priority disputed (P1 vs. P2; see Dispute 4).

Devils-advocate identified that the Step 4 formula and the Important Notes simplified formula disagree for N=3, iterations=1 (Step 4 yields 16; Important Notes claims 13). Functional-typing traced the root cause: the Important Notes section has an internal arithmetic error. The expanded form `N + N*(N-1) + N + N + 1` simplifies to `N^2 + 2N + 1`, but the text claims `N^2 + N + 1`, dropping the Phase 4 (Disputes) term of N agents.

**Agreed fix** (direction unanimous): Correct the Important Notes section to match Step 4. Do not modify the Step 4 formula or the converge handler. Specific corrections:
- Line 1517: `N^2 + N + 1` becomes `N^2 + 2N + 1`
- Line 1518: `N^2 + N + 2` becomes `N^2 + 2N + 2`
- Line 1519: "13 total agent launches" becomes "16 total agent launches"
- Line 1520: "14 total agent launches" becomes "17 total agent launches"
- Line 1524: "3 * 13 + 1 = 40" becomes "3 * 16 + 1 = 49"

The converge handler (line 1404) already uses the correct Step 4 formula. The fix prevents cross-document confusion within SKILL.md.

---

<!-- DISPUTES_BEGIN -->

## Remaining Disputes

Four disputes remain after Phase 4. All four are narrow -- they concern scope boundaries and priority calibration, not fundamental disagreements about what is broken or the direction of the fix. None block implementation.

### Dispute 1: Problem statement inclusion in the pre-execution summary

**Parties**: functional-typing + devils-advocate (include problem statement) vs. integration-architect (defer to follow-up)

**functional-typing position**: The P1 label fix should be expanded: (1) relabel `Problem:` to `Mode:`, and (2) add a `Problem:` field displaying the first sentence or heading from `problem.md` (or "(hand-crafted config -- no problem.md)" when absent). The problem definition is the most fundamental input to any deliberation; a consent surface that omits it is structurally incomplete.

**devils-advocate position**: Aligns with functional-typing. "A user who confirms execution without seeing what problem is being deliberated is consenting to something they cannot evaluate." The label fix alone is a half-measure -- the summary will say `Mode: Find common ground` but the user still does not know the problem. The one-line conditional addition is the same category of "reasonable extension" accepted for FR-004's sub-case expansion.

**integration-architect position**: Accepts the label fix as P1 but defers problem-statement inclusion. FR-001 lists "mode (plain-language explanation)" as a required summary element and does not list the problem definition. Adding it is a spec amendment, not a bug fix. The pre-execution summary is lossy by design -- it also omits template content, constitution rules, and prior file content. Adding one omitted dimension without addressing the others creates an inconsistency in the level of detail.

**Synthesizer assessment**: The label fix (`Problem:` to `Mode:`) is fully converged and should be applied immediately. On the expansion: functional-typing and devils-advocate make a strong informed-consent argument -- the problem definition is qualitatively different from templates or constitution rules because it is the anchor of the entire deliberation. Integration-architect's concern about spec-amendment scope is procedurally valid but may be overly cautious for a one-line conditional addition. The implementer should apply the label fix as P1 and treat the problem-statement addition as an immediate P2 follow-up, which bridges the gap between the two-reviewer majority position and integration-architect's scope concern.

### Dispute 2: Prior context disclosure priority -- P2 vs. P3

**Parties**: functional-typing + devils-advocate (P2) vs. integration-architect (P3)

**functional-typing position**: P2. Prior files silently influence every agent. The informed-consent principle of FR-001/FR-002 does not carve out advanced features. The fix is a single conditional line in the summary template.

**devils-advocate position**: Aligns with functional-typing at P2. A user who inherits a `conversus.yml` from a colleague may not know that `prior:` files are configured. "The person who configured it probably knows" is insufficient -- the person who confirms execution needs to know.

**integration-architect position**: P3. Prior files are an advanced configuration dimension, and users who set them are more likely to be aware of their influence. If prior files must be disclosed, then templates, constitutions, and iteration counts also deserve expanded disclosure -- the summary becomes a config dump, which SC-004 rejects.

**Synthesizer assessment**: All three agree the fix should be implemented; only the priority differs. The implementation cost is identical at P2 or P3 (one conditional line). Integration-architect's slippery-slope argument (if prior files, then templates, then constitutions) has merit as a design principle, but prior files are unique in that they influence every agent's context window without being visible in the config summary -- templates and iteration counts are already surfaced. P2 is the more defensible priority given a two-reviewer majority and the low implementation cost, but the practical difference is negligible.

### Dispute 3: Mtime staleness false-positive documentation

**Parties**: devils-advocate (explicitly document the limitation) vs. functional-typing and integration-architect (not opposed, but did not adopt)

**devils-advocate position**: The spec or SKILL.md should include one sentence: "This warning may appear after git operations that update file timestamps. It is safe to proceed if you have not changed your interests." No reviewer opposes this, but it was not adopted into any consolidated recommendation list.

**functional-typing position**: Accepted mtime as a reasonable best-effort heuristic; did not comment on documenting its limitations.

**integration-architect position**: Withdrew the staleness-check extension to spec 008; did not comment on the documentation request.

**Synthesizer assessment**: This is a procedural gap rather than a substantive disagreement. No reviewer opposes the one-sentence documentation addition. It should be adopted as a minor addendum (P3) to the staleness warning section. The cost is negligible and the benefit is real: a non-expert who sees a false-positive warning after `git stash pop` will lose trust in the guided flow without this context.

### Dispute 4: Important Notes formula correction priority -- P1 vs. P2

**Parties**: integration-architect (P1) vs. functional-typing (P2)

**integration-architect position**: P1. The SKILL.md is a single document and internal contradictions degrade trust in the document as a whole. A non-expert reading Important Notes alongside the converge output will see contradictory numbers, eroding trust in the exact feature designed to build trust.

**functional-typing position**: P2. The converge handler uses the correct formula (Step 4), so users see the right number. The Important Notes section is documentation that users may never read. The primary harm -- confusion during review -- has already been surfaced and documented by this review cycle.

**devils-advocate position**: Aligned with the fix direction; did not take a strong position on P1 vs. P2.

**Synthesizer assessment**: The fix is identical at either priority -- the same lines change. Integration-architect's argument that SKILL.md internal consistency matters is sound, but functional-typing is correct that no execution path is affected. P1 is justified if the SKILL.md is expected to be read by agents or reviewers who may reference Important Notes during future deliberations (which this review cycle demonstrates does happen). P2 is justified if the converge handler's correct output is the user-facing surface that matters. Given that the error demonstrably caused confusion in this very review cycle, P1 is the pragmatically safer choice.

<!-- DISPUTES_END -->

---

## Consolidated Recommendation Table

| Priority | Recommendation | Status |
|----------|---------------|--------|
| **P0** | Replace `/conversus arbitrate` dead reference with actionable workaround + planned-command note | Consensus |
| **P1** | Add `--output <dir>` flag to converge handler | Consensus |
| **P1** | Fix "Problem" label to "Mode" at SKILL.md line 1377 | Consensus (label fix); problem-statement expansion disputed |
| **P1/P2** | Fix Important Notes formula arithmetic (lines 1517-1525) | Consensus on fix; priority disputed |
| **P2** | Document failure recovery position (full re-run required) | Consensus |
| **P2** | Make delegation semantics explicit in Execution section | Consensus |
| **P2** | Add "What to Expect" narrative to pre-execution summary | Consensus |
| **P2** | Specify dispute-parsing file target as `{output}/summary/final.md` | Consensus |
| **P2** | Add spec acknowledgment for cross-tool next steps (speckit) | Consensus |
| **P2/P3** | Add prior context disclosure to pre-execution summary | Consensus on fix; priority disputed |
| **P2** | Add problem statement to pre-execution summary | 2-1 majority (FT+DA); IA defers to follow-up |
| **P3** | Document mtime staleness false-positive limitation | Unopposed; procedurally unresolved |
| **Deferred** | `--dry-run` capability for converge | Consensus (out of scope) |
| **Withdrawn** | Extend staleness check to `problem.md` (belongs in spec 008) | Consensus |
| **Withdrawn** | Replace mtime with content hashing (belongs in spec 008) | Consensus |

---

## Process Observations

The cooperative deliberation was productive. Each reviewer's analytical lens caught issues the others missed:

- **functional-typing** (structural correctness): Caught the "Problem" label mislabeling, the prior-context omission, and the dispute-parsing file ambiguity. Provided the root-cause analysis for the Important Notes formula error that devils-advocate identified symptomatically.

- **integration-architect** (integration architecture): Identified the `--output` flag gap, elevated the `/conversus arbitrate` dead reference to P0, and provided the line-level corrections for the formula fix. Correctly scoped the staleness mechanism to spec 008 during cross-review.

- **devils-advocate** (adversarial challenge): Identified the formula discrepancy, challenged the staleness mechanism (forcing a correct reassignment to spec 008), raised the delegation-semantics fragility, and flagged the speckit integration as unspec'd behavior.

Three findings specifically required the multi-reviewer chain: (1) the formula error (symptom by DA, root cause by FT, line-level fix by IA); (2) the `/conversus arbitrate` fix (severity by IA, dispute explanation by DA, combined fix framing by FT); and (3) the staleness scoping (mechanism challenge by DA, scope extension by IA, both withdrawn through mutual challenge, reassigned to spec 008 by consensus).

The spec is ready for implementation with the converged recommendations applied. The four remaining disputes are narrow refinements that do not affect the core implementation plan.
