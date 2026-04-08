# Round 2 Review — integration-architect

**Spec**: `008-interests-mode`
**Target files**: `conversus/specs/008-interests-mode/spec.md`, `conversus/SKILL.md` (lines 926-1319)
**Round**: 2 of 2
**Date**: 2026-03-22

---

## Executive Summary

The Round 1 deliberation was thorough and productive. Eight convergence points were established unanimously, three disputes were resolved through synthesis, and no blocking defects were identified at any phase. I reaffirm all my prior concessions (FR-007 downgrade to "Partially Satisfied," the Preset field as a spec omission not implementation drift, preset validation escalation to High, and withdrawal of the extract-and-warn approach for CLARIFY tags). None of those positions should be revisited.

Round 2 is the final round. My focus here is threefold: (1) confirm alignment with the synthesis recommendations and arbiter opinions on the three resolved disputes, (2) surface integration-level concerns that the dispute-centric Phase 4 discussion may have underweighted, and (3) identify actionable gaps in the converged recommendations themselves — places where the *agreed-upon fixes* need tightening before implementation.

The spec and SKILL.md remain substantively sound. The 4 P1 spec changes and 4 P1 SKILL.md changes from the synthesis are the right set. My new observations are about implementation precision within the converged recommendations, not about reopening settled questions.

---

## Alignment

### Dispute 1 Resolution: CLARIFY-tag handling — Aligned

The synthesis recommendation (final.md, Dispute 1 synthesis) correctly combines inline user confirmation with the no-silent-default principle. The arbiter's opinion (resolution.md, lines 56-68) strengthens this by grounding it in two constitutional principles: the User Confirmation Gate (spec.md line 104) and Domain Agnosticism (spec.md line 105). I agree with both.

The arbiter's observation that "recommend" is load-bearing language (resolution.md, line 62) is precisely right. My Round 1 position was too strict — routing the user *back* to `/conversus define` as the only path effectively nullifies deferred resolution, which the define handler explicitly supports (SKILL.md line 889: "whether downstream commands treat `draft` as blocking is defined by those commands' specs"). The synthesis's "recommend, do not require" formulation respects this design intent. I accept it without reservation.

The recommended SKILL.md change K-2 (final.md, lines 307-313) is implementable as written. One precision note: the four calibration styles presented to the user should use the plain-language descriptions from the Interest Generation table (SKILL.md lines 957-962), not the mode names. The spec's constraint against requiring game theory knowledge (spec.md line 103) applies to calibration style selection as well as mode selection.

### Dispute 2 Resolution: `--output` framing — Aligned

The synthesis adopted my workspace-override framing (final.md, Dispute 2 synthesis, lines 228-229). The arbiter independently arrived at the same conclusion through a different argument — the `cd` analogy (resolution.md, line 85) — which reinforces that this is the natural characterization, not a preference. I have no further comment on this dispute.

### Dispute 3 Resolution: Generated config completeness — Aligned

The synthesis and arbiter both reject the "starter template" framing. The arbiter's grounding in Schema Completeness via Defaults (SKILL.md lines 57-60) is definitive: a config that omits optional fields is functionally identical to one that sets them to defaults. The recommended SKILL.md change K-8 (final.md, lines 345-349) correctly surfaces extension points without undermining validity. Aligned.

### Convergence Points C-1 through C-10 — Affirmed

All eight convergence points from the synthesis (final.md, lines 109-191) are settled. I reaffirm them. The recommended spec changes S-1 through S-4 and SKILL.md changes K-1 through K-8 are the right set with the right priorities. No reopening.

---

## Missed Opportunities

### MO-1: The prerequisite chain lacks a state-machine formalization (P2)

The three handlers (define, interests, mode) form a linear prerequisite chain: define produces `problem.md`, interests consumes `problem.md` and produces `interests.md`, mode consumes both and produces `conversus.yml`. Each handler has its own prerequisite check (SKILL.md lines 932-941, 1099-1115), and the checks are correct. But the checks are expressed as ad-hoc conditionals rather than as a shared state model.

This matters for two reasons. First, the convergence on draft-status behavior (C-5, final.md lines 146-151) and CLARIFY-tag handling (K-2) both add conditional warnings based on artifact state. As more handlers are added (the SKILL.md header lists future subcommands: `converge`, `arbitrate`, `gate` at line 32), each will need its own prerequisite checks, draft-status warnings, and CLARIFY-tag handling. Without a shared model, each new handler will re-derive the artifact state independently, inviting inconsistency.

Second, the staleness warning (SKILL.md lines 1117-1122) uses filesystem modification times to detect drift between `interests.md` and `conversus.yml`. This is fragile — file timestamps can be misleading (e.g., `touch` without content changes, editor autosave). A content hash or generation marker in the artifact itself would be more reliable.

This is not a spec 008 fix — the current checks work. But it should be noted for the future subcommand specs: the prerequisite chain is becoming complex enough to warrant a shared state model (even just a documented state table) rather than per-handler ad-hoc conditionals.

### MO-2: Cross-validation warning (K-6) needs a concrete signal vocabulary (P2)

The converged recommendation K-6 (final.md, lines 333-337) specifies that the mode handler should check whether "the interest structure's naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles) is consistent with the stated problem type." This is the right check, but the implementation guidance is abstract.

The heuristic detection section (SKILL.md lines 1149-1154) has a concrete signal vocabulary for mode detection — specific phrases and structural patterns. The cross-validation warning has no equivalent. An implementer reading K-6 would need to invent the mapping from interest naming patterns to problem types. The synthesis should have specified the mapping explicitly:

| Interest naming pattern | Suggests problem type |
|---|---|
| Named after products, tools, approaches | `selection` |
| Named after teams, roles, systems | `integration` |
| Overlapping capability claims | `scoping` |
| Asymmetric roles (attacker/defender) | `stress-test` |

This table already exists implicitly in the heuristic detection signals and in the Interest Generation table (SKILL.md lines 957-962). Making it explicit in K-6 would reduce implementer ambiguity. This is a precision improvement to a converged recommendation, not a new requirement.

### MO-3: The `(none)` sentinel question is more urgent than its P2 deferral suggests (P2)

The synthesis defers `(none)` sentinel formalization to a future spec (D-1, final.md lines 352-354). But the mode handler already consumes `(none)` at a critical juncture: the Source Documents field mapping (SKILL.md line 1254: "If Source Documents contains `(none)`, ask the user..."). This is not a future concern — it is a current code path.

The define handler writes three different `(none)` variants:
- `- (none — no context documents provided)` for Source Documents (SKILL.md line 891)
- `- (none)` for Open Questions (SKILL.md line 891)
- The bare concept of emptiness for other sections (SKILL.md line 891, handled via `[CLARIFY:]` tags)

The mode handler checks for `(none)` (SKILL.md line 1254) but the define handler writes `(none — no context documents provided)`. These do not string-match. An implementer doing a literal substring check on `(none)` would match both forms, but one doing an exact-equality check would miss the longer form. The converged recommendations do not address this mismatch.

This should be elevated from "deferred future spec" to a P2 SKILL.md clarification in spec 008: the mode handler's Source Documents check should explicitly specify that it matches any value beginning with `(none` — or the define handler's sentinel should be simplified to a single canonical form.

---

## Off-Base Assumptions

### OBA-1: The cost estimate formula may mislead for modes with structural agent-count variation

The converged recommendation K-5 (final.md, lines 327-329) adds an agent-launch cost estimate at mode confirmation: "Estimated agent launches per round: {N^2 + N + 1}." This formula comes from the Important Notes section (SKILL.md lines 1304-1307) and is correct for the standard cooperative/winner-take-all/prisoners-dilemma modes.

However, the formula assumes all N agents participate in all phases uniformly. The red-blue mode has asymmetric roles — red agents and blue agents may have different participation patterns in cross-review (a red agent cross-reviewing another red agent is qualitatively different from a red agent cross-reviewing a blue agent). If a future spec introduces role-scoped cross-review (where red agents only cross-review blue agents and vice versa), the formula changes from N^2 to N_red * N_blue * 2.

The current engine does not implement role-scoped cross-review — all N agents cross-review all other N-1 agents regardless of role (SKILL.md Important Notes confirm this). So the formula is currently correct. But presenting it as "Estimated agent launches" without noting that it assumes uniform cross-review could set incorrect expectations if the red-blue mode later gains role-scoped behavior.

This is not a blocking issue. The fix is minor: the K-5 text should say "Estimated agent launches per round: {N^2 + N + 1} (all agents cross-review all others)" rather than just "{N^2 + N + 1} (based on {count} agents in {mode} mode)." The parenthetical explains the assumption.

---

## Actionable Recommendations

All recommendations below operate within the converged framework from Round 1. None reopen settled disputes or reverse concessions.

### AR-1 (P2): Tighten K-6 with an explicit naming-pattern-to-type mapping table

Add the following table to the K-6 recommendation text:

```
When checking interest naming patterns against stated problem type, use these correspondences:
- Interests named after products, tools, or approaches → suggests selection
- Interests named after teams, roles, or systems → suggests integration
- Interests with overlapping capability claims → suggests scoping
- Interests with asymmetric attacker/defender roles → suggests stress-test
```

This makes K-6 implementable without requiring the implementer to reverse-engineer the mapping from the heuristic detection signals.

**Target**: SKILL.md K-6 text (final.md, lines 333-337).
**Source**: Interest Generation table (SKILL.md lines 957-962), Heuristic Mode Detection (SKILL.md lines 1149-1154).

### AR-2 (P2): Resolve the `(none)` sentinel mismatch between define and mode handlers

The mode handler's Source Documents check (SKILL.md line 1254) should explicitly handle the define handler's long-form sentinel. Either:

(a) Change the mode handler text to: "If Source Documents contains a value beginning with `(none`, ask the user..." — prefix matching.

Or:

(b) Standardize the define handler to write `- (none)` for all empty sentinel values, and update the comment text to a separate line or parenthetical.

Option (a) is lower risk — it does not change the define handler's output format.

**Target**: SKILL.md line 1254 (mode handler field mapping) or SKILL.md line 891 (define handler empty sections).
**Source**: MO-3 above.

### AR-3 (P2): Qualify the K-5 cost estimate with its cross-review assumption

Change the K-5 recommended text from:

> "Estimated agent launches per round: {N^2 + N + 1} (based on {count} agents in {mode} mode)."

To:

> "Estimated agent launches per round: {N^2 + N + 1} (all {count} agents cross-review all others)."

This makes the formula's assumption explicit and prevents confusion if role-scoped cross-review is introduced in a future spec.

**Target**: SKILL.md K-5 text (final.md, lines 327-329).
**Source**: OBA-1 above; SKILL.md lines 1304-1307.

### AR-4 (P2): Add the plain-language calibration style descriptions to K-2

The K-2 recommendation (final.md, lines 307-313) specifies that the interests handler should present four calibration styles when a CLARIFY tag is found on the Type field. The presentation should use the plain-language descriptions from the Interest Generation table, not the type names or mode names. Suggested text for the user prompt:

```
The problem type needs clarification. How should agents approach this deliberation?

1. Each agent advocates for its preferred option (selection)
2. Each agent advocates for its needs while finding common ground (integration)
3. Each agent honestly declares its responsibilities and boundaries (scoping)
4. Attackers try to break it, defenders show it holds up (stress-test)
```

This respects the constraint against requiring game theory knowledge (spec.md line 103) at the calibration-style selection point, not just at the mode selection point.

**Target**: SKILL.md K-2 text (final.md, lines 307-313).
**Source**: No Game Theory Knowledge Required constraint (spec.md line 103); Interest Generation table (SKILL.md lines 957-962).

### AR-5 (P3): Note the prerequisite chain complexity for future specs

Add a note to the deferred items section of the synthesis: "As future subcommands (converge, arbitrate, gate) are specified, consider formalizing the artifact prerequisite chain as a shared state table rather than per-handler ad-hoc conditionals. The current design works for three handlers but will not scale cleanly to six or more."

This is advisory for future spec authors, not an action item for spec 008.

**Target**: Deferred items section (final.md, lines 351-358).
**Source**: MO-1 above; SKILL.md line 32 (future subcommands list).

---

## Referenced Documentation

| Reference | Location | Relevance |
|---|---|---|
| Spec 008 feature specification | `conversus/specs/008-interests-mode/spec.md` | Primary spec under review |
| SKILL.md interests handler | `conversus/SKILL.md` lines 926-1090 | Implementation of `/conversus interests` |
| SKILL.md mode handler | `conversus/SKILL.md` lines 1093-1296 | Implementation of `/conversus mode` |
| SKILL.md define handler | `conversus/SKILL.md` lines 800-924 | Upstream handler producing `problem.md`; CLARIFY-tag and sentinel semantics |
| SKILL.md subcommand dispatch | `conversus/SKILL.md` lines 19-38 | Future subcommands list, prerequisite chain |
| SKILL.md run configuration schema | `conversus/SKILL.md` lines 50-60 | Schema defaults (rounds, iterations, stagnation, validate_templates) |
| SKILL.md agent count formulas | `conversus/SKILL.md` lines 1304-1314 | Cost estimate formula and its assumptions |
| Round 1 synthesis | `conversus/specs/008-interests-mode/conversus-review/round-1/summary/final.md` | Converged recommendations, disputes, concessions |
| Arbiter resolution | `conversus/specs/008-interests-mode/conversus-review/round-1/arbitration/resolution.md` | Advisory opinions on three disputes |
| User Confirmation Gate | `spec.md` line 104 | Constraint: no generation without user confirmation |
| No Game Theory Knowledge Required | `spec.md` line 103 | Constraint: plain language in user-facing interactions |
| Domain Agnosticism | `spec.md` line 105 | Constraint: no hard-coded agents or domain assumptions |
| Deferred resolution design | `SKILL.md` line 889 | Define handler's `status` field is factual annotation; downstream commands decide blocking behavior |
