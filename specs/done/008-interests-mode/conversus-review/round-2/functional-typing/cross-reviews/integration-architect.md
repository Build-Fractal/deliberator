# Cross-Review of integration-architect — Round 2

**Reviewer**: functional-typing
**Reviewing**: integration-architect's Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: MO-2's naming-pattern-to-type mapping table presupposes a classification boundary that the system deliberately avoids

Integration-architect proposes (AR-1, MO-2) adding an explicit mapping table to K-6 that maps interest naming patterns to problem types:

> | Interest naming pattern | Suggests problem type |
> |---|---|
> | Named after products, tools, approaches | `selection` |
> | Named after teams, roles, systems | `integration` |
> | Overlapping capability claims | `scoping` |
> | Asymmetric roles (attacker/defender) | `stress-test` |

The stated rationale is that this table "already exists implicitly" in the heuristic detection signals and the Interest Generation table (SKILL.md lines 957-962). This is wrong. The heuristic detection signals (SKILL.md lines 1151-1154) operate on the problem description text and interest structure simultaneously, using multiple signal types (linguistic phrases, structural patterns, exclusivity constraints). The proposed table collapses this multi-signal inference into a single dimension: naming patterns alone.

The danger is that codifying this table in K-6 creates a deterministic classifier where the converged recommendation deliberately specifies a heuristic warning. K-6 as converged says: "Check whether the interest structure's naming pattern ... is consistent with the stated problem type. If inconsistent, warn." This leaves the implementer to apply judgment about what "consistent" means in context. The proposed table eliminates that judgment space and replaces it with a four-row lookup that will produce false positives.

Concrete example: a problem of type `integration` might have interests named after products (e.g., "postgres," "redis," "kafka") because the integration question is about making those products work together. Under the proposed table, an implementer would fire a warning ("Your interests suggest a selection problem") because the naming pattern matches the `selection` row. But the problem is genuinely about integration. The naming pattern alone is insufficient to distinguish "choose among these products" from "integrate these products."

The heuristic detection section avoids this exact failure mode by using multiple signal types: it checks for phrases like "work together" and "integrate" alongside the naming patterns, and it evaluates whether "all interests must survive in the outcome" (SKILL.md line 1152). The proposed table strips away this multi-signal context.

The K-6 recommendation as converged is correct precisely because it is abstract. Adding the table would reduce it from a thoughtful heuristic warning to a brittle pattern match. If implementers need more guidance, the guidance should reference the full heuristic detection signal vocabulary (SKILL.md lines 1151-1154), not a single-dimension extract of it.

### DC-2: AR-4's calibration style descriptions import mode-level semantics into the interests handler

Integration-architect proposes (AR-4) that K-2's inline calibration style prompt should use specific text:

> 1. Each agent advocates for its preferred option (selection)
> 2. Each agent advocates for its needs while finding common ground (integration)
> 3. Each agent honestly declares its responsibilities and boundaries (scoping)
> 4. Attackers try to break it, defenders show it holds up (stress-test)

Integration-architect explicitly cites the constraint against requiring game theory knowledge (spec.md line 103) and the Interest Generation table (SKILL.md lines 957-962) as sources. But the proposed text includes the problem type names in parentheses: `(selection)`, `(integration)`, `(scoping)`, `(stress-test)`. The constraint says mode names should not appear "in user-facing conversation unless the user uses them first." While the parentheticals are labeled as type names rather than mode names, in this system types and modes have a 1-to-1 mapping (the decision matrix, spec.md lines 48-52), so exposing type names is functionally equivalent to exposing mode names.

This contradicts the arbiter's own reasoning on Dispute 1 (resolution.md, lines 124-125): "The interests handler and mode handler have different input spaces." If the input spaces are different, the interests handler should not reveal the type-to-mode mapping to the user at the calibration style selection point. The user should choose based on the plain-language descriptions alone, not based on parenthetical type labels that leak the system's internal taxonomy.

The fix is straightforward: remove the parenthetical type names from the proposed prompt text. Present the four descriptions without labels. The K-2 synthesis recommendation does not specify that type names should be shown -- it says "present the four calibration styles." Integration-architect's proposed text adds the labels as an embellishment that conflicts with the constraint it cites.

---

## Tensions

### T-1: MO-1's prerequisite chain formalization is forward-looking advice dressed as a Round 2 finding

Integration-architect's MO-1 proposes formalizing the prerequisite chain (define -> interests -> mode) as a shared state model, motivated by the observation that future subcommands (converge, arbitrate, gate) will need similar checks. The analysis is sound -- the current ad-hoc conditionals will not scale to six or more handlers.

However, integration-architect also acknowledges "This is not a spec 008 fix" and classifies it as AR-5 at P3 priority with the target being the deferred items section. This is consistent with the Round 1 principle that spec 008 recommendations should address spec 008 gaps. But the filesystem-timestamp fragility observation embedded within MO-1 (modification times as staleness signals) is a current concern, not a future one. The staleness warning (SKILL.md lines 1117-1122) is active code in the mode handler. If timestamps are unreliable, the warning is unreliable now, not in a hypothetical future.

My concern: lumping the current staleness-signal reliability issue with the forward-looking state-model recommendation may cause the former to be deferred along with the latter. The timestamp fragility should be noted as a standalone P2 observation tied to the existing staleness warning (SKILL.md line 1119), separate from the P3 advisory about prerequisite chain formalization.

That said, I withdrew my own staleness warning concern in Round 1 (functional-typing revision P2-4: "WITHDRAWN") based on the text alignment being adequate. The timestamp fragility is a different issue from the text alignment I withdrew -- it concerns the mechanism (mtime comparison) rather than the wording. I do not want to reopen a withdrawn position, but I note the tension: integration-architect identifies a real problem in a domain I explicitly left, and the problem deserves evaluation on its own merits.

### T-2: MO-3's `(none)` sentinel mismatch is well-identified but the proposed resolution is incomplete

Integration-architect's MO-3 correctly identifies that the define handler writes `(none -- no context documents provided)` (SKILL.md line 891) while the mode handler checks for `(none)` (SKILL.md line 1254), and that these do not string-match on exact equality. The two proposed resolutions -- prefix matching on `(none` or standardizing to `- (none)` -- are both reasonable.

My own MO-2 independently identified the same mismatch (functional-typing review, lines 75-85). We converge on the gap. However, integration-architect's analysis is more precise than mine: they correctly note this is a current code path, not a deferred concern, and argue it should be elevated from the D-1 deferred item to a P2 SKILL.md clarification.

The tension is that the proposed prefix match `(none` introduces its own fragility: any field content that happens to begin with `(none` would trigger the sentinel check. The string `(none of the above apply)` would match. The probability of this in practice is low, but the sentinel formalization question (D-1) exists precisely because ad-hoc pattern matching on sentinels is brittle. Proposing a new ad-hoc pattern (prefix match) while acknowledging that D-1 exists for exactly this class of problem is internally inconsistent.

The cleaner resolution is option (b): standardize to `- (none)` in the define handler. This eliminates the matching problem entirely and reduces the sentinel vocabulary to a single canonical form. Integration-architect notes that option (a) is "lower risk" because it does not change the define handler's output format, but changing one line of output format in a pre-spec handler is lower risk than introducing an ambiguous matching rule that future sentinels will need to avoid colliding with.

### T-3: OBA-1's cost formula qualification is correct but underestimates the scope of the assumption

Integration-architect observes that the N^2 + N + 1 formula assumes all N agents participate uniformly in cross-review, and proposes qualifying the K-5 text from "(based on {count} agents in {mode} mode)" to "(all {count} agents cross-review all others)." This is a good improvement.

However, the formula's assumptions go beyond just cross-review uniformity. The formula also assumes `iterations: 1` (the default). With `iterations: 2`, the cross-review and revision phases run twice, changing the formula. The Important Notes section (SKILL.md lines 1310-1313) documents the multi-iteration formula: `Per-round agents = N + iterations * (N*(N-1) + N) + N + 1`. At `iterations: 1` this simplifies to N^2 + N + 1, but K-5 presents the simplified form without noting that it assumes the default iteration count.

Since the generated config always sets `iterations: 1` (SKILL.md line 1256), and the cost estimate fires at mode confirmation (before the user has edited the config to increase iterations), the simplification is valid at the moment it is displayed. But the parenthetical should arguably note both assumptions: uniform cross-review AND single iteration. Integration-architect's proposed change addresses one assumption and leaves the other implicit.

This is a minor tension, not a dangerous contradiction. The simplified formula is correct for the generated config. I note it for completeness because the recommendation is specifically about making assumptions explicit, and it would be inconsistent to make one assumption explicit while leaving another implicit.

---

## Safe Agreements

### SA-1: All three dispute resolutions are fully aligned

Integration-architect's alignment with the synthesis and arbiter on Disputes 1, 2, and 3 matches my own positions exactly. On Dispute 1: the "recommend, do not require" formulation for CLARIFY-tag handling is accepted without reservation by both of us. On Dispute 2: the workspace-override framing is adopted. On Dispute 3: the "complete config with extensions" language is confirmed. No further discussion is needed on any settled dispute.

### SA-2: Convergence points C-1 through C-10 and recommendations S-1 through S-4, K-1 through K-8 are affirmed

Both reviews confirm all convergence points and actionable recommendations from Round 1 without modification. Neither review proposes reopening or reversing any prior concession. The converged recommendation set is stable.

### SA-3: The `(none)` sentinel mismatch is independently confirmed

Both reviews independently identified the mismatch between the define handler's `(none -- no context documents provided)` and the mode handler's `(none)` check. Integration-architect's MO-3 and my MO-2 arrive at the same conclusion: this is a real gap that the Round 1 synthesis deferred too aggressively. We agree this should be addressed sooner than D-1's general sentinel formalization. The only disagreement is on the resolution approach (prefix matching vs. canonical form standardization), which is a T-2 tension above, not a blocking disagreement.

### SA-4: Prior concessions are stable across both reviews

Integration-architect explicitly reaffirms all prior concessions (FR-007 downgrade, Preset field as spec omission, preset validation escalation, CLARIFY-tag extract-and-warn withdrawal). I explicitly reaffirm all of mine (P0 severity demotion, CLARIFY-tag extract-and-warn withdrawal, staleness warning withdrawal, "specification drift" reframing). No reversal pressure from either side.

### SA-5: The spec and SKILL.md are substantively sound

Both reviews conclude that no blocking defects exist and the converged recommendation set from Round 1 is the right set of changes. All new observations from both reviews are P2 or P3 precision improvements within the converged framework, not challenges to the framework itself. The deliberation has reached productive closure.

### SA-6: Integration-architect's AR-3 on cost estimate parenthetical wording is a clean improvement

Changing the K-5 parenthetical from "(based on {count} agents in {mode} mode)" to "(all {count} agents cross-review all others)" is strictly more informative and does not introduce any new concerns. The T-3 tension about iteration assumptions is an extension of this improvement, not a challenge to it. The proposed wording should be adopted.

### SA-7: Integration-architect's AR-5 on prerequisite chain advisory is well-scoped

The recommendation to add a forward-looking note about prerequisite chain formalization for future specs is correctly scoped as P3 advisory. It does not create spec 008 obligations and it correctly identifies a real scaling concern. The timestamp fragility concern I raised in T-1 is separable from this advisory and does not undermine it.
