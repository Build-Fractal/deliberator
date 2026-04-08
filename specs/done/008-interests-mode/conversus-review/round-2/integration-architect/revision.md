# Round 2 Revision — integration-architect

**Spec**: `008-interests-mode`
**Target files**: `conversus/specs/008-interests-mode/spec.md`, `conversus/SKILL.md` (lines 926-1319)
**Round**: 2 of 2
**Date**: 2026-03-22

---

## Recommendation Dispositions

### AR-1 (P2): Naming-pattern-to-type mapping table for K-6 — REVISED

**Original**: Add a four-row lookup table mapping interest naming patterns to problem types as the implementation guidance for K-6.

**Cross-review feedback**: Functional-typing (DC-1) argues the table collapses multi-signal inference into a single dimension (naming patterns alone), creating a deterministic classifier where the converged K-6 deliberately specifies a heuristic warning. The concrete example is decisive: interests named "postgres," "redis," "kafka" in an integration problem would trigger a false "selection" warning under the table, because the naming pattern matches products/tools even though the problem is genuinely about making those products work together. Devils-advocate (T-3) makes a complementary point: interest names are user-defined strings matching `[a-z0-9][a-z0-9-_]*`, so many valid names are semantically opaque and cannot be classified by naming pattern alone.

**Disposition**: REVISED. Both cross-reviews are correct. The four-row table is insufficient as standalone guidance and dangerous as a deterministic classifier. Functional-typing's observation that the heuristic detection section uses multiple signal types simultaneously — linguistic phrases, structural patterns, exclusivity constraints — demonstrates that naming patterns are one input among several, not a complete mapping.

Devils-advocate's AR-3 proposes replacing "naming pattern" with "interest structure (names, perspectives, and prompts)" in K-6's description. This is the better fix. The cross-validation should examine the full interest structure, not just names. I adopt this wording change and withdraw the standalone mapping table.

However, naming patterns remain a useful starting heuristic when examined alongside perspective and prompt content. The revised recommendation: adopt devils-advocate's broader "interest structure" language for K-6, and if implementer guidance is needed, reference the full heuristic detection signal vocabulary (SKILL.md lines 1151-1154) rather than extracting a single-dimension subset of it.

### AR-2 (P2): `(none)` sentinel mismatch — MAINTAINED with resolution direction clarified

**Original**: Resolve the mismatch between the define handler's `(none — no context documents provided)` and the mode handler's `(none)` check, preferring option (a) (prefix matching) as lower risk.

**Cross-review feedback**: Functional-typing (T-2) agrees the mismatch is real and independently identified it, but argues that prefix matching on `(none` introduces its own fragility — the string `(none of the above apply)` would match. Functional-typing prefers option (b): standardize to `- (none)` in the define handler. Devils-advocate (T-1) agrees the observation is factually correct but considers the urgency overstated, noting that the mode handler's text says "contains `(none)`" which implies substring matching, and a competent implementer would handle it correctly.

**Disposition**: MAINTAINED at P2, with resolution direction changed to option (b). Functional-typing is right that prefix matching introduces a new class of fragility while option (b) eliminates the ambiguity entirely. Changing one line of output format in a handler that has no shipped backward-compatibility constraints is lower risk than introducing a matching rule that future sentinels must avoid colliding with. The define handler should write `- (none)` for all empty sentinel values, and the descriptive text `(no context documents provided)` should move to a comment or be dropped.

Devils-advocate's point about "contains" implying substring matching is reasonable as a practical observation, but the deliberation's purpose is to make specifications explicit, not to rely on implementer inference about natural-language instructions. P2 is the correct priority for a current code path with ambiguous matching semantics.

### AR-3 (P2): Cost estimate cross-review assumption — SUPERSEDED by computed count

**Original**: Change the K-5 parenthetical from "(based on {count} agents in {mode} mode)" to "(all {count} agents cross-review all others)."

**Cross-review feedback**: Functional-typing (T-3) notes the formula's assumptions go beyond cross-review uniformity — it also assumes `iterations: 1`, and both assumptions should be made explicit if the formula is displayed. Devils-advocate (T-2) proposes replacing the formula entirely with a computed count, since the mode handler knows N, rounds=1, and arbiter=absent at confirmation time and can compute an exact number. Devils-advocate argues that displaying `N^2 + N + 1` is implementer-facing information in a user-facing context.

**Disposition**: SUPERSEDED. I concede to devils-advocate's Option (b). At mode confirmation time, the handler has all the information needed to compute the exact agent launch count. Displaying a formula that the user must mentally evaluate violates the spec's constraint against requiring game theory knowledge (spec.md line 103) — not because the formula is game theory, but because it is unnecessary cognitive load when the system can do the computation.

The formula remains valuable in the Important Notes section (SKILL.md lines 1304-1308) as implementer documentation. My original AR-3 qualification — "(all {count} agents cross-review all others)" — should be applied there instead, along with functional-typing's iteration assumption note.

Revised recommendation: K-5 should display "This configuration will launch {computed number} agents" at mode confirmation, not the formula. The Important Notes section should qualify the formula with both assumptions: uniform cross-review and iterations=1.

### AR-4 (P2): Plain-language calibration style descriptions for K-2 — REVISED, parenthetical labels removed

**Original**: Present four calibration styles with plain-language descriptions and parenthetical type names: "(selection)", "(integration)", "(scoping)", "(stress-test)".

**Cross-review feedback**: Both functional-typing (DC-2) and devils-advocate (DC-1) independently identify the same contradiction: the proposed text includes parenthetical type names that leak the system's internal taxonomy to users who have not used those terms. Both reviewers note that the No Game Theory Knowledge constraint (spec.md line 103) says "Mode names appear in YAML but not in user-facing conversation unless the user uses them first," and that type names and mode names have a 1-to-1 mapping via the decision matrix (spec.md lines 48-52), making the exposure functionally equivalent. Functional-typing adds that the arbiter's Dispute 1 reasoning explicitly distinguishes the interests handler's input space from the mode handler's, so the interests handler should not reveal the type-to-mode mapping.

**Disposition**: REVISED. Both cross-reviews are correct. The parenthetical type names are an embellishment that contradicts the very constraint I cited. The fix is straightforward: present the four descriptions without labels. The user picks a behavioral description, and the system maps it internally.

Revised prompt text:

```
The problem type needs clarification. How should agents approach this deliberation?

1. Each agent advocates for its preferred option
2. Each agent advocates for its needs while finding common ground
3. Each agent honestly declares its responsibilities and boundaries
4. Attackers try to break it, defenders show it holds up
```

No parenthetical labels. No type names. The constraint is satisfied.

### AR-5 (P3): Prerequisite chain advisory for future specs — REVISED, timestamp concern separated

**Original**: Add a note to the deferred items section advising future spec authors to formalize the artifact prerequisite chain as a shared state table.

**Cross-review feedback**: Functional-typing (T-1) correctly observes that my MO-1 lumps two separable concerns: the forward-looking state-model recommendation (genuinely P3, not a spec 008 issue) and the current timestamp fragility in the staleness warning (SKILL.md lines 1117-1122). The latter is a current mechanism concern, not a future one. Devils-advocate (DC-2) makes a sharper version of the same point: proposing content hashes as a staleness mechanism would change the `interests.md` schema, which is a design change that should go through its own deliberative process. Devils-advocate also notes the current mechanism works for spec 008's scope.

**Disposition**: REVISED. I accept both critiques.

On the timestamp fragility: devils-advocate is right that proposing content hashes smuggles a design change into a deferred note. The current mtime-based staleness detection works for spec 008's temporal ordering check (does `interests.md` postdate `conversus.yml`?). The mechanism is imperfect but functional. I withdraw the content-hash suggestion. If timestamp fragility becomes a practical problem, it should be raised as a finding in a future spec, not embedded as a note in this one.

On the state-model advisory: the note itself is still valid. Functional-typing (SA-7) and devils-advocate (T-4) both agree the substance is correct. Devils-advocate raises a process concern about durability — a note in a synthesis document may not reach future spec authors. This is a fair point. The note should go in the SKILL.md's architectural section (near the subcommand dispatch table, lines 19-38) rather than in a synthesis deferred-items section, since the SKILL.md is the living document that future spec implementers will read.

Revised recommendation: Drop the timestamp criticism and the content-hash proposal. Keep the state-model advisory but place it as a brief comment in SKILL.md near the subcommand dispatch table, not in the synthesis deferred-items section.

---

## New Recommendations

### NR-1 (P2): Adopt devils-advocate's computed count for user-facing cost estimate

This recommendation consolidates AR-3 (superseded above), devils-advocate's MO-1 Option (b), and functional-typing's T-3 iteration-assumption observation into a single actionable change.

The K-5 user-facing cost estimate at mode confirmation should display a computed agent launch count, not the formula. At mode confirmation time, the handler knows: N (agent count from interests.md), iterations=1 (generated config default), rounds=1 (generated config default), arbiter=absent (not configured by mode handler). The computed count is exact.

User-facing text at mode confirmation:
> "This configuration will launch {count} agents."

Implementer-facing text in Important Notes (SKILL.md lines 1304-1308): retain the formula with two explicit qualifications: (1) assumes all N agents cross-review all others, and (2) assumes iterations=1.

**Target**: K-5 text (mode confirmation display) and SKILL.md Important Notes section.
**Source**: Devils-advocate MO-1, functional-typing T-3, my AR-3 (superseded).

### NR-2 (P2): K-6 cross-validation should examine full interest structure, not naming patterns alone

This recommendation consolidates AR-1 (revised above) and devils-advocate's AR-3 into a single actionable change.

The K-6 cross-validation description should replace "naming pattern" with "interest structure (names, perspectives, and prompts)." When the cross-validation fires, it should examine:
- Interest names for semantic signals (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles)
- Perspective sentences for type-consistent language (e.g., "advocates for its choice" vs. "seeks alignment")
- Prompt content for calibration-consistent framing

If the full interest structure is inconsistent with the stated problem type, warn. If interest names are semantically opaque (e.g., `alpha`, `beta`, `option-a`), fall back to perspective and prompt content for signals. Do not warn on opaque names alone.

For implementation guidance, reference the heuristic detection signal vocabulary (SKILL.md lines 1151-1154) as the canonical signal source. Do not extract a single-dimension subset.

**Target**: K-6 text (cross-validation warning description).
**Source**: My AR-1 (revised), devils-advocate AR-3, functional-typing DC-1.

---

## Position Summary

The deliberation has reached stable closure. All three dispute resolutions from Round 1 are accepted without reservation. All convergence points C-1 through C-10 and actionable changes S-1 through S-4, K-1 through K-8 are confirmed. All prior concessions (FR-007 downgrade, Preset field as spec omission, preset validation escalation, CLARIFY-tag extract-and-warn withdrawal) stand.

The five recommendations from my Round 2 review have been revised as follows in response to cross-review feedback:

| Original | Disposition | Key concession |
|---|---|---|
| AR-1: Naming-pattern mapping table | Revised | Withdrew standalone table; adopted devils-advocate's "interest structure" language; naming patterns are one input among several, not a complete mapping |
| AR-2: `(none)` sentinel mismatch | Maintained, direction changed | Changed from option (a) prefix matching to option (b) canonical form standardization per functional-typing's fragility argument |
| AR-3: Cost formula qualification | Superseded | Conceded to devils-advocate's computed count; formula belongs in implementer docs, not user-facing display |
| AR-4: Calibration style descriptions | Revised | Removed parenthetical type labels per both cross-reviews; present descriptions without internal taxonomy vocabulary |
| AR-5: Prerequisite chain advisory | Revised | Separated timestamp concern (withdrawn) from state-model advisory (retained, relocated to SKILL.md) |

Two new recommendations consolidate the revised positions:

| # | Description | Priority | Consolidates |
|---|---|---|---|
| NR-1 | Computed count for user-facing cost estimate | P2 | AR-3 + devils-advocate MO-1 + functional-typing T-3 |
| NR-2 | Full interest structure for K-6 cross-validation | P2 | AR-1 + devils-advocate AR-3 + functional-typing DC-1 |

No blocking defects exist. The spec and SKILL.md are substantively sound. The converged recommendation set from Round 1, refined by the Round 2 cross-review process, is ready for implementation. The remaining open items — the `(none)` sentinel standardization (AR-2) and the CLARIFY-tag third exit state (raised by devils-advocate AR-1, which I addressed in my cross-review as DC-1) — are P2 precision improvements that can be resolved in the final synthesis without further deliberation.
