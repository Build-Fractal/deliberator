# Cross-Review of integration-architect — Round 2

**Reviewer**: devils-advocate
**Reviewing**: integration-architect's Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: The K-2 plain-language calibration style descriptions reintroduce mode names through the back door

Integration-architect's AR-4 proposes presenting calibration style choices with parenthetical mode names:

> 1. Each agent advocates for its preferred option (selection)
> 2. Each agent advocates for its needs while finding common ground (integration)
> 3. Each agent honestly declares its responsibilities and boundaries (scoping)
> 4. Attackers try to break it, defenders show it holds up (stress-test)

Integration-architect grounds this in the No Game Theory Knowledge Required constraint (spec.md line 103), arguing that plain-language descriptions should be used "not just at the mode selection point." But the proposed text places the type names — `selection`, `integration`, `scoping`, `stress-test` — directly in the user prompt as parentheticals. These are the spec's internal taxonomy labels. The No Game Theory Knowledge constraint says: "Mode names appear in YAML but not in user-facing conversation unless the user uses them first."

The constraint's language says "mode names," but the spec uses these same labels across both the type taxonomy and the mode decision matrix (spec.md lines 46-52). The type name `selection` and the mode recommendation `winner-take-all` are coupled by the decision matrix — presenting type names to a user who has not used them is functionally equivalent to presenting mode names.

The safe approach: present only the plain-language descriptions without the parenthetical labels. The user picks a description, and the system maps it to the internal type. If the user needs to refer to their choice later, the system can echo the label after selection — but the initial prompt should not front-load taxonomy vocabulary that the user has not introduced.

This contradicts integration-architect's own stated principle. AR-4 opens by citing the constraint, then proposes text that violates it. The contradiction is not about intent (we agree on plain language) but about execution.

### DC-2: The state-machine formalization (MO-1) contradicts the "no reopening" commitment

Integration-architect's MO-1 proposes formalizing the prerequisite chain as a shared state model, noting that "per-handler ad-hoc conditionals" will not scale to six or more handlers. This is framed as a future concern (AR-5 is P3, advisory for future spec authors).

But MO-1 also criticizes the current staleness warning mechanism (SKILL.md lines 1117-1122) as "fragile" because it uses filesystem modification times, and proposes "a content hash or generation marker in the artifact itself." This is not a future concern — it is a recommendation to change the current mode handler's staleness detection mechanism. Content hashes in artifacts would change the `interests.md` schema (adding a hash field), which is a schema extension that spec 008 explicitly prohibits for `conversus.yml` (FR-011: "No schema extensions") and which the deliberation has not considered for `interests.md`.

Integration-architect classifies MO-1 as "not a spec 008 fix" but then identifies a concrete current-handler deficiency (timestamp fragility) and proposes a concrete fix (content hashes) that would affect spec 008 artifacts. Either the staleness detection criticism is a spec 008 concern (in which case it should be a recommendation, not a deferred note) or it is genuinely a future concern (in which case the criticism of the current mechanism is premature). It cannot be both deferred and actionable.

I do not dispute that filesystem timestamps are imperfect. But the current mechanism works for the spec 008 scope (SKILL.md lines 1117-1122 detect a specific temporal ordering), and introducing content hashes is a design change that should go through the same deliberative process, not be smuggled in as a "note for future specs."

---

## Tensions

### T-1: The `(none)` sentinel mismatch (MO-3/AR-2) is correctly identified but the urgency claim is overstated

Integration-architect elevates the `(none)` sentinel mismatch from the synthesis's "deferred future spec" (D-1) to a P2 SKILL.md clarification in spec 008, arguing it is "more urgent than its P2 deferral suggests" because "the mode handler already consumes `(none)` at a critical juncture."

The observation is factually correct: the define handler writes `(none -- no context documents provided)` (SKILL.md line 891) and the mode handler checks for `(none)` (SKILL.md line 1254). These do not string-match on exact equality.

However, the mode handler's text says "If Source Documents contains `(none)`" — the word "contains" already implies substring matching, not exact equality. An implementer reading "contains `(none)`" would naturally check whether the value contains the substring `(none)`, which matches both the short and long forms. The mismatch is real in a pedantic reading, but the natural-language instruction is unambiguous enough that a competent implementer would handle it correctly.

I agree with AR-2 option (a) — prefix matching — as a low-risk precision improvement. But the claim that this "should be elevated from deferred future spec" overstates the risk. The synthesis's D-1 deferral is about the broader `(none)` sentinel formalization across all handlers, which is genuinely a larger question. The specific string-matching behavior in the mode handler is a narrow implementation detail, not a sentinel formalization issue.

Priority agreement: P2 is right, but the urgency framing is a tension with the synthesis's deliberate deferral decision.

### T-2: The cost estimate qualification (AR-3/OBA-1) is correct but addresses a scenario that does not exist

Integration-architect's OBA-1 identifies that the N^2 + N + 1 formula assumes "all N agents participate in all phases uniformly" and that red-blue mode could theoretically have role-scoped cross-review. AR-3 proposes qualifying the formula with "(all {count} agents cross-review all others)."

This is technically valid — the qualification makes an implicit assumption explicit. But the qualification addresses a scenario that integration-architect acknowledges does not exist: "The current engine does not implement role-scoped cross-review." The proposed parenthetical "(all {count} agents cross-review all others)" adds information that is only useful to someone who is wondering whether the engine might not cross-review all agents — a question that no user of the guided workflow would ask, and that no current or specified behavior would prompt.

My own AR-2 also addresses the K-5 cost estimate, but with a different concern: the formula itself is implementer-facing, and the user should see a computed count, not N^2 + N + 1. If we adopt my AR-2 (display the computed number, not the formula), integration-architect's AR-3 becomes moot — you do not need to qualify a formula that is not displayed.

These two recommendations are not contradictory but they are in tension: AR-3 refines the formula display, AR-2 removes the formula display. If Round 2 synthesis accepts my AR-2, integration-architect's AR-3 is superseded. If it accepts AR-3 instead, the formula is still being shown to users who should not need to mentally evaluate algebraic expressions.

### T-3: The naming-pattern-to-type mapping table (MO-2/AR-1) partially addresses my OBA-2 but does not resolve it

Integration-architect's MO-2 and AR-1 propose adding an explicit mapping table from interest naming patterns to problem types, making K-6 more implementable. The table maps:

- Products/tools/approaches -> selection
- Teams/roles/systems -> integration
- Overlapping capability claims -> scoping
- Asymmetric attacker/defender roles -> stress-test

My OBA-2 identifies a deeper problem: interest names are user-defined strings matching `[a-z0-9][a-z0-9-_]*`, and many valid names (`alpha`, `beta`, `gamma`, `option-a`, `option-b`) cannot be classified by naming pattern alone. Integration-architect's table assumes interest names are semantically transparent (e.g., `team-backend`, `product-redis`), but the spec places no such constraint on naming.

Integration-architect's AR-1 makes K-6 more implementable for the happy path (semantically meaningful names), but it does not address the failure path (opaque names). My AR-3 proposes that the cross-validation should operate on "interest structure (names, perspectives, and prompts)" rather than "naming pattern" alone. Integration-architect's table is a subset of that broader approach — it covers names but not perspectives and prompts.

The tension: integration-architect's table could lead an implementer to build a name-only classifier that generates false warnings on opaque names, while my recommendation pushes toward a fuller structural analysis. These are not contradictory — the table could be one input among several — but AR-1 as written presents the table as the complete implementation guidance for K-6, without noting that names alone are insufficient.

### T-4: The prerequisite chain advisory (AR-5) is sound but arrives too late

Integration-architect's AR-5 proposes adding a note to the deferred items section: "As future subcommands are specified, consider formalizing the artifact prerequisite chain as a shared state table." This is P3 and advisory.

I agree with the substance — per-handler conditionals will become unwieldy. But deferred items in a synthesis document are not requirements, they are notes. There is no mechanism to ensure future spec authors read the deferred items from spec 008's synthesis before writing spec 009 or 010. If the concern is real (and it is), the note should go somewhere with more durability — the conversus SKILL.md's top-level architecture section, or a design decision record — not in a synthesis document that is read once during this deliberation and then archived.

This is a tension about the appropriate vehicle for the advice, not about the advice itself.

---

## Safe Agreements

### SA-1: All dispute resolutions are correctly affirmed

Integration-architect reaffirms the synthesis recommendations on all three disputes without reopening settled positions. The alignment on Dispute 1 (CLARIFY-tag handling with "recommend, do not require"), Dispute 2 (workspace-override framing for `--output`), and Dispute 3 (rejection of "starter template" framing) is complete. I affirm the same positions in my review. No daylight between us on any resolved dispute.

### SA-2: All convergence points C-1 through C-10 are settled

Integration-architect affirms all convergence points without modification. I do the same. These are settled and should be implemented.

### SA-3: Prior concessions are respected

Integration-architect explicitly lists prior concessions (FR-007 downgrade, Preset field as spec omission, preset validation escalation, withdrawal of extract-and-warn) and declares none should be revisited. I respect all my own prior concessions (interests.md-as-optional withdrawal, formalized keyword scoring withdrawal, cost estimate placement correction, "fabricated" confidence retraction). Neither review attempts to relitigate Round 1 positions.

### SA-4: The `(none)` sentinel observation is factually correct

Integration-architect's MO-3 correctly identifies that the define handler writes `(none -- no context documents provided)` while the mode handler checks for `(none)`. The string mismatch is real. My only disagreement is with the urgency of elevating this from deferred to spec 008 scope (see Tension T-1), not with the observation itself. The fix (prefix matching or sentinel standardization) is sound either way.

### SA-5: The K-2 calibration style descriptions should use plain language

Integration-architect and I agree that the K-2 fix should present calibration styles in plain language, not mode names or type labels. The disagreement (DC-1) is about whether integration-architect's proposed text actually achieves this goal, not about the goal itself.

### SA-6: The cost estimate should be more precise than the current K-5 text

Both reviews identify the K-5 cost estimate text as insufficiently precise. Integration-architect proposes qualifying the formula's assumption (AR-3). I propose replacing the formula with a computed count (AR-2). We agree the current text needs improvement; we differ on the direction. The synthesis can choose either approach — both are improvements over the status quo.

### SA-7: No blocking defects exist

Both reviews confirm that the spec and SKILL.md are substantively sound. No new blocking defects are identified. All Round 2 recommendations are P2 or P3 refinements to converged positions, not challenges to the fundamental design.

---

## Summary

Integration-architect's Round 2 review is careful and well-grounded. The five recommendations (AR-1 through AR-5) all operate within the converged framework and none attempt to reopen settled disputes. Two dangerous contradictions emerge: the AR-4 calibration prompt text violates the constraint it cites (fixable by dropping the parenthetical type labels), and MO-1 conflates a future architectural concern with a current mechanism criticism without committing to either scope. Four tensions exist, mostly about precision and urgency rather than direction. Seven safe agreements confirm that the two reviews are substantially aligned on all settled positions and dispute resolutions.
