# Neutral Synthesis: Spec 008 — Round 2 (Final)

**Deliberation type**: Cooperative
**Agents**: functional-typing, integration-architect, devils-advocate
**Target**: `conversus/specs/008-interests-mode/spec.md` and `conversus/SKILL.md` (lines 926-1319)
**Round**: 2 of 2
**Date**: 2026-03-22
**Prior material**: Round 1 synthesis (`round-1/summary/final.md`), arbiter opinions (`round-1/arbitration/resolution.md`)

---

## Process Summary

Three agents completed the second and final round of cooperative review of spec 008 and its SKILL.md implementation across the standard four phases (review, cross-review, revision, disputes).

**Round 1 recap**: Eight convergence points (C-1 through C-10) were established unanimously. Three disputes were narrowed to language and framing. The synthesis produced 4 P1 spec changes, 4 P1 SKILL.md changes, 4 P2 SKILL.md changes, 1 P2 spec change, and 2 deferred items. The arbiter's advisory opinions aligned with the synthesis on all three disputes.

**Round 2 Phase 1 (Reviews)**: All three reviewers accepted the Round 1 synthesis and arbiter opinions. All three disputes from Round 1 were resolved: Dispute 1 (CLARIFY-tag handling) adopted the synthesis + arbiter position with all reviewers accepting the inline user choice and "recommend, do not require" fallback. Dispute 2 (--output framing) adopted integration-architect's workspace-override framing unanimously. Dispute 3 (generated config completeness) confirmed "complete config with extensions" framing with 3-to-0 alignment. New findings surfaced: (a) functional-typing identified a spec/SKILL.md divergence on interest count range (spec says "2-5", SKILL.md enforces only "2+"); (b) both functional-typing and integration-architect independently identified a `(none)` sentinel text mismatch between the define and mode handlers; (c) devils-advocate identified a gap in K-2's control flow for the case when the user declines both choosing a calibration style and running `/conversus define`; (d) integration-architect proposed a naming-pattern-to-type mapping table for K-6 and plain-language calibration style descriptions for K-2; (e) devils-advocate proposed replacing the cost estimate formula with a computed count in the user-facing display.

**Round 2 Phase 2 (Cross-Reviews)**: Cross-reviews produced four dangerous contradictions and sixteen tensions across six cross-review documents. The most productive exchanges were: (a) functional-typing and devils-advocate independently identifying that integration-architect's AR-4 calibration style prompt included parenthetical type names that violate the No Game Theory Knowledge constraint; (b) functional-typing identifying that integration-architect's proposed mapping table would collapse multi-signal heuristic inference into a single-dimension lookup, producing false positives; (c) integration-architect and devils-advocate independently identifying that functional-typing's preferred interest count resolution (relax to "2 or more") had no enforcement mechanism, since the cost estimate was converged as an informational display, not a validation gate; (d) functional-typing and integration-architect independently identifying that devils-advocate's proposed hard stop for the CLARIFY-tag third exit state contradicts the arbiter's "recommend, do not require" resolution and the define handler's deferred-resolution design.

**Round 2 Phase 3 (Revisions)**: All three reviewers made significant revisions. Functional-typing reversed MO-1 (interest count) from "relax the spec" to "enforce the upper bound," elevated the sentinel mismatch from P3 to P2 and withdrew the claim that the SKILL.md handles it correctly, and revised K-2 to specify a double-declination stop. Integration-architect withdrew the standalone mapping table (AR-1), changed the sentinel resolution direction from prefix matching to canonical form standardization, conceded that the cost formula should be replaced with a computed count in user-facing displays, and removed parenthetical type labels from AR-4. Devils-advocate conceded the hard stop for the CLARIFY-tag third exit state and adopted integration-architect's "user-confirmed degraded mode" approach, withdrew AR-4 (interest-count cost note at interests confirmation) and MO-2 for internal inconsistency with AR-2, and conceded OBA-1 (arbiter critique).

**Round 2 Phase 4 (Disputes)**: All Round 1 convergence points and dispute resolutions remain stable. Ten new convergence points were established in Round 2. Two narrow disputes remain, both concerning parameter choices within fully agreed mechanisms rather than architectural disagreements. No reviewer at any phase of either round identified a blocking defect.

---

## Recommendation Scorecard

| # | Item | Priority | Action Target | Status | Source |
|---|---|---|---|---|---|
| 1 | Ambiguous row divergence | P1 | Spec | Converged (R1+R2) | C-1, all rounds |
| 2 | Preset field in interests.md schema | P1 | Spec | Converged (R1+R2) | C-2, all rounds |
| 3 | `--output` workspace-override documentation | P1 | Spec | Converged (R1+R2) | Dispute 2 resolution, all rounds |
| 4 | Preset existence validation at generation time | P1 | SKILL.md | Converged (R1+R2) | C-3, all rounds |
| 5 | CLARIFY-tag handling in interests handler | P1 | SKILL.md | Converged on mechanism; third exit state disputed | K-2, synthesis + arbiter + Round 2 revisions |
| 6 | Draft status behavior for interests handler | P1 | SKILL.md | Converged (R1+R2) | C-5, all rounds |
| 7 | Confidence column rename/footnote | P2 | Spec | Converged (R1+R2) | C-11, all rounds |
| 8 | Heuristic detection advisory sentence | P2 | SKILL.md | Converged (R1+R2) | C-4, all rounds |
| 9 | Cost estimate: computed count with assumptions | P2 | SKILL.md | Converged (R2) | RC-2, all three revisions |
| 10 | Cross-validation on full interest structure | P2 | SKILL.md | Converged (R2) | RC-3, all three revisions |
| 11 | Zero-signal edge case handling | P2 | SKILL.md | Converged (R1+R2) | C-8, all rounds |
| 12 | Extension-points note in mode handler report | P2 | SKILL.md | Converged (R1+R2) | Dispute 3 resolution, all rounds |
| 13 | Interest count upper-bound warning gate | P2 | SKILL.md | Converged on mechanism; threshold disputed | NR-1, Round 2 |
| 14 | `(none)` sentinel standardization | P2 | SKILL.md (define handler) | Converged (R2) | RC-5, all three revisions |
| 15 | Calibration style descriptions without type labels | P2 | SKILL.md (folded into K-2) | Converged (R2) | RC-4, all three revisions |
| 16 | Interest-vs-type cross-validation warning | P2 | SKILL.md | Converged (R1+R2) | C-7 refined by RC-3 |
| 17 | State-model advisory near subcommand dispatch | P3 | SKILL.md | Converged (R2) | RC-7, editorial note |

---

## Dangerous Contradictions Found in Round 2

Four dangerous contradictions were identified during the Round 2 cross-review phase. All were resolved by Phase 3 revisions.

### DC-1: Integration-architect's parenthetical type labels in calibration style prompt

**Contradiction**: Integration-architect's AR-4 proposed presenting calibration styles with parenthetical type names -- `(selection)`, `(integration)`, `(scoping)`, `(stress-test)` -- while citing the No Game Theory Knowledge constraint (spec.md line 103) as the rationale for plain language. Both functional-typing (DC-2) and devils-advocate (DC-1 of integration-architect) independently identified that type names have a 1-to-1 mapping with mode names via the decision matrix (spec.md lines 48-52), making the exposure functionally equivalent to revealing mode names.

**Resolution**: Integration-architect conceded in Phase 3 revision (AR-4 revised), removing all parenthetical labels. The calibration style prompt presents plain-language behavioral descriptions only. Converged.

### DC-2: Integration-architect's naming-pattern mapping table for K-6

**Contradiction**: Integration-architect's AR-1 proposed a four-row lookup table mapping interest naming patterns to problem types as standalone implementation guidance for K-6. Functional-typing (DC-1 of integration-architect) demonstrated this would produce false positives: interests named "postgres," "redis," "kafka" in an integration problem would trigger a false "selection" warning because the naming pattern matches products/tools. The heuristic detection section uses multiple signal types simultaneously; the table collapsed this to a single dimension.

**Resolution**: Integration-architect withdrew the standalone table in Phase 3 revision (AR-1 revised), adopted devils-advocate's "interest structure (names, perspectives, and prompts)" language. Naming patterns remain one input signal among several, not a complete mapping. Converged.

### DC-3: Functional-typing's interest count relaxation path

**Contradiction**: Functional-typing's MO-1 proposed relaxing the spec's interest count from "2-5" to "2 or more" and relying on the cost estimate as the user's throttle. Both integration-architect (DC-1 of functional-typing) and devils-advocate (DC-1 of functional-typing) independently identified that the cost estimate was converged as an informational display (C-6/K-5), not as a validation gate. The relaxation path had no enforcement mechanism -- the user could add 12 interests, see the cost formula, click yes, and launch 157 agents.

**Resolution**: Functional-typing reversed their preferred resolution in Phase 3 revision (S-5 revised, NR-1), adopting resolution 1: enforce the upper bound in the SKILL.md. The warning gate with user override provides enforcement without promoting the cost estimate from display to gate. Converged on mechanism; threshold value remains in narrow dispute.

### DC-4: Devils-advocate's hard stop for K-2 third exit state

**Contradiction**: Devils-advocate's AR-1 prescribed a hard stop when the user declines both choosing a calibration style and running `/conversus define`. Both functional-typing (DC-1 of devils-advocate) and integration-architect (DC-1 of devils-advocate) identified that this contradicts the arbiter's "recommend, do not require" resolution (resolution.md, lines 60-62) and the define handler's deferred-resolution design (SKILL.md line 889). Devils-advocate's own alignment section accepted "recommend" as the right verb, but AR-1 prescribed behavior that functionally requires resolution.

**Resolution**: Devils-advocate conceded the hard stop in Phase 3 revision (AR-1 revised, NR-1), adopting integration-architect's "user-confirmed degraded mode" approach. The gap in K-2 is real but the hard stop was architecturally inconsistent with accepted principles. Converged that a hard stop as originally proposed is wrong; the specific mechanism for the third exit state remains in narrow dispute between functional-typing's double-declination stop and devils-advocate's/integration-architect's degraded mode.

---

## Systemic Observations

### SO-1: The spec consistently underspecifies what the SKILL.md correctly refines

Round 2 reinforced the pattern identified in Round 1 (Systemic Contradiction SC-1): in every case where the spec and SKILL.md disagree, all three reviewers concluded the SKILL.md was correct or the spec should be updated to match. Round 2 added two new instances: the interest count range (spec says "2-5" but SKILL.md's lower-bound-only validation is more operationally flexible with a warning gate) and the `(none)` sentinel handling (the mode handler correctly handles the edge case that the spec does not acknowledge). The spec's primary debt is precision, not architecture.

### SO-2: The cross-review mechanism in Round 2 was highly productive

Round 2 cross-reviews corrected seven significant errors across the three reviewers: (1) functional-typing's interest count resolution direction, (2) functional-typing's `(none)` sentinel priority classification, (3) functional-typing's "inconsequential" dismissal of the equal-probability assumption, (4) integration-architect's standalone mapping table, (5) integration-architect's parenthetical type labels, (6) integration-architect's prefix-matching sentinel resolution, and (7) devils-advocate's hard stop for the CLARIFY-tag third exit state. All corrections were accepted in Phase 3 revisions.

---

## Convergence Achieved

### Carried from Round 1 (reaffirmed unanimously in Round 2)

All ten Round 1 convergence points (C-1 through C-10) survived Round 2 without challenge. All three Round 1 dispute resolutions are accepted. All prior concessions from Round 1 (functional-typing: 4, integration-architect: 4, devils-advocate: 5) stand without reversal.

### C-1 through C-10: As specified in Round 1 synthesis

The converged actions from Round 1 are unchanged: S-1 (ambiguous row replacement), S-2 (Preset field in schema), S-3 (--output documentation), S-4 (Confidence column), K-1 (preset validation), K-3 (draft status behavior), K-4 (heuristic-is-advisory), K-7 (zero-signal handling), K-8 (extension-points note), and C-9 (interests.md is architecturally necessary) and C-10 (staleness warning text is adequate).

### New convergence in Round 2

#### RC-1: Interest count upper-bound enforcement direction

All three reviewers agree: the SKILL.md post-write validation must enforce an upper bound on interest count. The cost estimate (C-6/K-5) remains an informational display, not a validation gate. Functional-typing reversed their preferred resolution from "relax the spec" to "enforce the bound" after both cross-reviewers identified the enforcement-mechanism gap in the relaxation path.

**Traced agreement**: functional-typing revision NR-1 (reversed); integration-architect DC-1; devils-advocate DC-1.

#### RC-2: Computed count replaces formula in user-facing cost estimate

All three reviewers agree: the K-5 mode confirmation display should show a computed agent launch count, not the raw formula `N^2 + N + 1`. The handler knows N, rounds=1, iterations=1, and arbiter=absent at confirmation time. The formula is retained in the Important Notes section (SKILL.md lines 1304-1308) as implementer documentation with explicit qualifications: (1) assumes all N agents cross-review all others, (2) assumes iterations=1.

**Traced agreement**: devils-advocate MO-1 Option (b); integration-architect revision NR-1 (conceded); functional-typing revision K-5 (accepted).

#### RC-3: K-6 cross-validation examines full interest structure

All three reviewers agree: the K-6 cross-validation description should replace "naming pattern" with "interest structure (names, perspectives, and prompts)." Interest names alone are insufficient for reliable type inference because many valid names are semantically opaque. The cross-validation should examine interest names for semantic signals, Perspective sentences for type-consistent language, and Prompt content for calibration-consistent framing. For implementation guidance, reference the heuristic detection signal vocabulary (SKILL.md lines 1151-1154) rather than extracting a single-dimension subset.

**Traced agreement**: devils-advocate AR-3; integration-architect revision NR-2 (withdrew mapping table); functional-typing revision K-6 (adopted "interest structure" language).

#### RC-4: Calibration style descriptions use plain language without type labels

All three reviewers agree: when the interests handler presents calibration styles for a CLARIFY-tagged type, the descriptions must not include type names or mode names in parentheticals. The prompt text:

```
The problem type needs clarification. How should agents approach this deliberation?

1. Each agent advocates for its preferred option
2. Each agent advocates for its needs while finding common ground
3. Each agent honestly declares its responsibilities and boundaries
4. Attackers try to break it, defenders show it holds up
```

No parenthetical labels. No type names.

**Traced agreement**: integration-architect revision AR-4 (removed labels); functional-typing DC-2; devils-advocate DC-1 of integration-architect.

#### RC-5: `(none)` sentinel standardized to canonical form

All three reviewers agree: the mismatch between the define handler's `(none -- no context documents provided)` (SKILL.md line 891) and the mode handler's `(none)` check (SKILL.md line 1254) is a real implementation hazard that should be fixed within spec 008's scope. The resolution direction is option (b): standardize to `(none)` in the define handler's output. Prefix matching (option a) introduces its own fragility class. D-1 remains as a broader deferred item for sentinel conventions across future handlers.

**Traced agreement**: functional-typing revision NR-2; integration-architect revision AR-2 (changed from option a to option b); devils-advocate disputes convergence 3.

#### RC-6: Equal-probability assumption is consequential for K-6/K-7 design rationale

Functional-typing revised OBA-1 to withdraw the "inconsequential" characterization. The unequal prior probability of modes under heuristic detection is the architectural justification for K-6 (cross-validation when signals conflict with stated type) and K-7 (zero-signal presentation of all modes). The corrected characterization: "Off-base and consequential for the design of K-6 and K-7, but not requiring a new recommendation because K-6 and K-7 already handle the consequences correctly."

**Traced agreement**: functional-typing revision OBA-1 (revised); integration-architect DC-2 of functional-typing; devils-advocate T-2 of functional-typing.

#### RC-7: Prerequisite chain advisory relocated, timestamp concern withdrawn

All three reviewers accept the state-model advisory substance: the prerequisite chain will become complex enough to warrant a shared model as future subcommands are added. The timestamp fragility concern and the content-hash proposal are withdrawn as out of scope for spec 008. The advisory note should be placed in the SKILL.md near the subcommand dispatch table (lines 19-38), not in a synthesis deferred-items section.

**Traced agreement**: integration-architect revision AR-5 (revised); functional-typing T-1; devils-advocate DC-2 of integration-architect.

#### RC-8: D-3 (`--output` flag rename) withdrawn as formal deferred item

Functional-typing withdrew D-3 as a formal deferred item. The naming mismatch is noted as a P3 editorial observation but does not warrant a standing deferred item in a system with no shipped CLI. The deferred items list simplifies to D-1 and D-2.

**Traced agreement**: functional-typing revision D-3 (withdrawn); integration-architect T-4; devils-advocate T-4.

#### RC-9: Devils-advocate's OBA-1 (arbiter critique) conceded

Devils-advocate conceded that the arbiter's general observation 7 is a summary characterization, not a claim that no architectural implications exist. The arbiter's Dispute 1 opinion demonstrably engaged with architecture across six paragraphs. The forward-looking concern about non-interactive execution is valid but deferred.

**Traced agreement**: devils-advocate revision OBA-1 (conceded); integration-architect DC-2 of devils-advocate; functional-typing DC-2 of devils-advocate.

#### RC-10: Devils-advocate's AR-4 (interest-count cost note at interests confirmation) withdrawn

Devils-advocate withdrew AR-4 after functional-typing identified two problems: premature optimization pressure before the mode is known, and internal inconsistency with AR-2 (cannot argue the formula is too implementer-facing for mode confirmation while proposing it at an earlier step). The C-6 cost estimate at mode confirmation remains the sole placement.

**Traced agreement**: devils-advocate revision AR-4 (withdrawn); functional-typing T-2, T-4 of devils-advocate.

---

<!-- DISPUTES_BEGIN -->

## Remaining Disputes

### Dispute 1: K-2 third exit state — double-declination stop vs. user-confirmed degraded mode

**What is agreed**: All three reviewers identified the gap in K-2: the synthesis text does not specify what happens when the user declines both choosing a calibration style and running `/conversus define`. All agree it must be closed. All agree the interests handler cannot generate type-calibrated prompts without a type. All agree the define handler's deferred-resolution design (SKILL.md line 889) should be respected. All agree no silent default is acceptable. All agree the calibration style prompt should use plain-language descriptions without type labels (RC-4).

**Where they diverge**:

- **functional-typing** (revision K-2 revised): A two-attempt flow. First declination triggers a binary choice prompt: choose a calibration style or stop and run `/conversus define`. Second declination triggers a hard stop: "Cannot proceed without a calibration style." This narrows the deferred-resolution window to one additional interaction but does not eliminate it. Functional-typing explicitly accepts that this makes CLARIFY-tag resolution effectively mandatory for the interests handler after two attempts, arguing that this is an acceptable narrowing because the calibration table (SKILL.md lines 957-962) has no "uncalibrated" row -- it structurally requires a type.

- **devils-advocate** (revision NR-1) and **integration-architect** (disputes, Dispute 1): A user-confirmed degraded mode. If the user declines both choosing a calibration style and running `/conversus define`, the handler explains that prompts will use generic calibration rather than type-specific calibration, states this explicitly, and asks the user to confirm. If confirmed, generate interests with generic prompts. If declined, stop with the recommendation to run `/conversus define`. Integration-architect adds a structural reservation: "generic calibration" must be concretely defined. If undefined, functional-typing's double-declination stop is safer because it avoids generating output from an unspecified code path.

**Neutral assessment**: The dispute is genuinely narrow and well-structured. Both sides agree on 90% of the mechanism. The disagreement is about the terminal behavior after the user refuses all offered choices.

Functional-typing's position has a structural advantage: the Interest Generation table (SKILL.md lines 957-962) has exactly four rows with no generic option. Any "generic calibration" implementation would need to create prompt content not currently specified, which is a design extension. Functional-typing also correctly observes that the double-declination stop gives the user two clear opportunities before stopping, which is more generous than a single-attempt hard stop.

Devils-advocate's and integration-architect's position has a design-intent advantage: the define handler's CLARIFY tag promises deferred resolution, and the double-declination stop is quantitatively but not qualitatively different from a hard requirement. The user-confirmed degraded mode keeps the workflow unblocked and is consistent with the User Confirmation Gate (no silent default) and Domain Agnosticism (no type privileged) constraints. Integration-architect's reservation that generic calibration must be defined is crucial -- the concept needs concrete specification to be implementable.

**Synthesis recommendation**: Adopt the user-confirmed degraded mode with a concrete definition of generic calibration. The define handler's deferred-resolution design is a fundamental promise of the system, and a double-declination stop is functionally a requirement with extra steps. However, integration-architect's reservation must be satisfied: "generic calibration" means prompts that describe each interest's role and perspective without type-specific adversarial, cooperative, honesty-calibrated, or red/blue framing. Concretely:

- The Perspective field uses a neutral formulation: "This interest represents [name]'s position on the problem."
- The Prompt field uses a factual-inquiry formulation: "Articulate [name]'s position, priorities, and constraints regarding the problem statement. Ground your arguments in the problem definition and any available documentation."

This is not one of the four calibration styles under a different name -- it does not assume mutual exclusivity (selection), mutual survival (integration), boundary declaration (scoping), or asymmetric roles (stress-test). It is a minimal viable prompt that downstream consumers (the mode handler's Perspective field at SKILL.md line 1203) can process without structural issues.

The handler must also warn the user that generic prompts produce weaker deliberation because they lack type-specific framing. The user's confirmation of degraded mode is informed consent, not a hidden compromise.

### Dispute 2: Interest count upper-bound threshold value

**What is agreed**: All three reviewers agree the SKILL.md post-write validation must enforce an upper bound on interest count. All agree the mechanism should be a warning gate with user override, not a hard block. All agree the cost estimate (C-6/K-5) should remain an informational display, not a validation gate. The spec's "2-5" range establishes the principle.

**Where they diverge**:

- **functional-typing** (revision NR-1) and **devils-advocate** (disputes, Dispute 2): Set the warning threshold at 5, matching the spec's stated range. Users can override with explicit confirmation.

- **integration-architect** (disputes, Dispute 2): Prefers a warning threshold of 7 rather than 5, arguing that 5 is too restrictive for complex integration or scoping problems with 6-7 stakeholders. The cost at N=7 (57 launches) is expensive but manageable. At N=5, warning fatigue is a risk. However, integration-architect explicitly states this is a P2 calibration question, not an architectural dispute, and will not contest further if the others prefer 5.

**Neutral assessment**: This is the narrowest possible form of dispute -- a parameter choice within a fully converged mechanism. The 2-to-1 alignment favors 5. Integration-architect's concern about warning fatigue is reasonable but speculative (it depends on how often users encounter 5+ interests). The spec's "2-5" range was explicitly chosen and provides a natural Schelling point.

**Synthesis recommendation**: Set the warning threshold at 5 to match the spec's stated range. The warning gate allows user override, so the ceiling is soft. If 5 proves too restrictive in practice, the threshold can be raised in both the spec and SKILL.md together. The spec change (S-5) should acknowledge that the "2-5" range is a guideline with a soft ceiling, not a hard architectural limit. Concretely, the SKILL.md post-write validation should enforce: "At least 2 and at most 5 interests are defined. If more than 5 are present, warn with the computed agent launch cost and ask the user to confirm."

### Dispute 3: K-5 cost estimate priority — P2 vs. P3

**What is agreed**: All three reviewers agree the K-5 cost estimate at mode confirmation should display a computed count, not a raw formula. The substance and display format are converged. Only the priority classification differs.

**Where they diverge**:

- **functional-typing** (disputes, Dispute 2) and **integration-architect** (revision NR-1): P2. The cost estimate exists to inform decisions. A mechanism that requires mental polynomial evaluation is not fully serving its purpose. The No Game Theory Knowledge constraint applies in spirit -- unnecessary cognitive load on the user.

- **devils-advocate** (revision AR-2): P3. The user has already expressed intent to proceed at mode confirmation. A formula vs. a computed number is a presentation refinement.

**Neutral assessment**: The 2-to-1 alignment favors P2. The cost estimate is a decision-support mechanism; if it requires mental arithmetic to parse, it is partially undermined. However, the system can produce correct output either way -- the priority affects implementation order, not correctness.

**Synthesis recommendation**: P2. The mechanism exists to inform a user's go/no-go decision. Presenting information in a form that requires mental arithmetic when the system can trivially compute the result violates the principle of insulating users from internal abstractions. The difference between P2 and P3 is small, but the 2-to-1 alignment and the functional argument favor P2.

<!-- DISPUTES_END -->

---

## Actionable Spec Changes

Organized by target document and priority. All changes trace to converged recommendations or synthesis dispute resolutions. This section consolidates the Round 1 synthesis actionable changes with Round 2 refinements and additions.

### Changes to `specs/008-interests-mode/spec.md`

**S-1 (P1): Replace the `ambiguous` row in the decision matrix (spec line 52)**

Replace:
```
| ambiguous | cooperative | Low -- present alternatives |
```

With a note below the table:
```
When the problem type is ambiguous or unset, use heuristic mode detection (FR-008). If no mode has detectable signals, present all four modes with plain-language descriptions and ask the user to choose.
```

Source: Convergence C-1. All three reviewers, both rounds.

**S-2 (P1): Add optional Preset field to interests.md schema (spec lines 72-87)**

Add after the Docs field:
```
- **Preset**: <category/preset-name>  <!-- only if a preset was used -->
```

Source: Convergence C-2. Spec omission required by FR-006 data flow.

**S-3 (P1): Add Common Options section documenting `--output`**

Add a new section after FR-013:
```
### Common Options

Both `/conversus interests` and `/conversus mode` accept:

- `--output <dir>` -- Override the working directory for all artifact I/O. Both prerequisite files (`problem.md`, `interests.md`) and generated output will be read from and written to this directory. Default: current working directory.
```

Source: Dispute 2 resolution (Round 1); integration-architect's workspace-override framing.

**S-4 (P2): Rename or footnote the Confidence column in the decision matrix**

Either rename "Confidence" to "Default Strength" or add a footnote: "These mappings are structurally deterministic (each type maps to exactly one mode). Empirical validation of deliberation outcomes under these defaults has not been performed."

Source: C-11 (Round 1).

**S-5 (P2): Acknowledge interest count upper bound as soft ceiling**

The spec's FR-001 ("2-5 competing interests") establishes a guideline. Add a clarifying note that the upper bound is enforced as a warning gate with user override in the SKILL.md, not as a hard architectural limit.

Source: RC-1 (Round 2); Dispute 2 synthesis resolution.

### Changes to `conversus/SKILL.md`

**K-1 (P1): Add preset existence validation to mode handler post-write check (~line 1271)**

Add a validation rule: "If an agent uses `preset:`, resolve the preset path using the same resolution rules as Run: Execution Step 1. If the preset file does not exist, warn: 'Agent {name} references preset {preset} which cannot be resolved. The generated config may fail at run time.'"

Source: Convergence C-3. All three reviewers, both rounds.

**K-2 (P1): Add CLARIFY-tag handling to interests handler Interest Generation (~line 955)**

Add: "If the Type field contains a `[CLARIFY: ...]` tag, treat the problem type as unresolved. Present the CLARIFY tag's content to the user and offer the following choices using plain-language descriptions only (no type names or mode names):

```
The problem type needs clarification. How should agents approach this deliberation?

1. Each agent advocates for its preferred option
2. Each agent advocates for its needs while finding common ground
3. Each agent honestly declares its responsibilities and boundaries
4. Attackers try to break it, defenders show it holds up
```

If the user chooses an option, map it to the corresponding calibration style (selection, integration, scoping, stress-test) and proceed.

If the user declines to choose, display: 'We recommend running `/conversus define` to resolve the type before generating interests. Would you like to: (a) choose a calibration style from the list above, (b) stop and run `/conversus define` first.'

If the user chooses (a), present the calibration styles again. If the user chooses (b), stop processing.

If the user declines to choose a second time, explain that interest prompts will use generic calibration rather than type-specific calibration. Generic calibration uses neutral framing: Perspective fields describe the interest's position factually ('This interest represents [name]'s position on the problem') and Prompt fields use factual-inquiry framing ('Articulate [name]'s position, priorities, and constraints regarding the problem statement'). Warn: 'Generic prompts produce weaker deliberation because they lack type-specific framing.' Ask the user to confirm. If confirmed, proceed with generic calibration. If declined, stop processing with the recommendation to run `/conversus define`.

Do not silently extract the best-guess type from the CLARIFY tag or default to any calibration style."

In the mode handler, route CLARIFY-tagged types through heuristic mode detection (existing behavior for ambiguous/unset types).

Source: Dispute 1 synthesis resolution (Round 1), refined by Round 2 dispute resolution. Combines functional-typing's inline confirmation, integration-architect's no-silent-default principle, and devils-advocate's user-confirmed degraded mode with integration-architect's concrete definition of generic calibration.

**K-3 (P1): Add draft status behavior to interests handler prerequisite check (~line 941)**

Add: "If `problem.md` has `status: draft`, warn: 'problem.md is marked as draft with {count} unresolved [CLARIFY:] tags. Interest generation will use the current content, but results may change after clarifications are resolved.' Proceed without blocking."

Source: Convergence C-5. All three reviewers, both rounds.

**K-4 (P2): Add heuristic-is-advisory sentence (~line 1156)**

Add: "The heuristic recommendation is advisory and always subject to user confirmation before proceeding."

Source: Convergence C-4. All three reviewers, both rounds.

**K-5 (P2): Replace cost formula with computed count at mode confirmation (~line 1203)**

Change the mode confirmation display to show a computed agent launch count rather than the formula. At mode confirmation time, the handler knows N, rounds=1, iterations=1, and arbiter=absent. Display:

> "This configuration will launch {computed_count} agents (all {count} agents cross-review all others, single iteration)."

Where `computed_count` = N^2 + N + 1, computed by the handler.

In the Important Notes section (SKILL.md lines 1304-1308), retain the formula with two explicit qualifications: (1) assumes all N agents cross-review all others, (2) assumes iterations=1.

Source: RC-2 (Round 2). Devils-advocate MO-1 Option (b), integration-architect NR-1, functional-typing K-5 revision.

**K-6 (P2): Revise interest-vs-type cross-validation to examine full interest structure**

Replace the K-6 text referencing "naming pattern" with: "Check whether the interest structure (names, perspectives, and prompts) is consistent with the stated problem type. Examine interest names for semantic signals (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles), Perspective sentences for type-consistent language, and Prompt content for calibration-consistent framing. If the full interest structure is inconsistent with the stated problem type, warn: 'Your interests suggest a {inferred-type} problem, but problem.md says {stated-type}. Consider re-running /conversus define to update the type, or proceed with the current type.' If interest names are semantically opaque (e.g., `alpha`, `beta`), fall back to perspective and prompt content for signals. Do not warn on opaque names alone. For signal guidance, reference the heuristic detection signal vocabulary (SKILL.md lines 1151-1154). This is a warning, not a block."

Source: RC-3 (Round 2). Devils-advocate AR-3, integration-architect NR-2, functional-typing DC-1 of integration-architect.

**K-7 (P2): Add zero-signal edge case to heuristic detection (~line 1156)**

Add: "If no signals are detected for any mode, present all four modes with their plain-language descriptions and ask the user to choose. Do not default silently."

Source: Convergence C-8. All three reviewers, both rounds.

**K-8 (P2): Add advanced fields note to mode handler report (~line 1290)**

Add: "For multi-round deliberation, stagnation detection, prior context, or subject arbitration, add the corresponding fields to conversus.yml manually. See the Run: Execution configuration reference for available options."

Source: Dispute 3 synthesis resolution. Both rounds.

**K-9 (P2): Add interest count upper-bound validation to post-write check (~line 1059)**

Change "At least 2 interests are defined" to: "At least 2 and at most 5 interests are defined. If more than 5 are present, warn: 'You have {count} interests. This configuration will launch approximately {computed_count} agents per round. Reduce to 5 or fewer, or confirm to proceed.' If the user confirms, proceed. If the user removes interests, re-validate."

Source: Dispute 2 synthesis resolution. Functional-typing NR-1, integration-architect RC-1, devils-advocate Dispute 2.

**K-10 (P2): Standardize `(none)` sentinel in define handler output (~line 891)**

Change the define handler's Source Documents sentinel from `(none -- no context documents provided)` to `(none)`. This makes the define handler's output match the mode handler's `(none)` check (SKILL.md line 1254) exactly, eliminating the substring-vs-exact-matching ambiguity. The descriptive text adds no information the user does not already know.

Source: RC-5 (Round 2). Functional-typing NR-2, integration-architect AR-2 (revised to option b), devils-advocate implicit acceptance.

**K-11 (P3): Add state-model advisory near subcommand dispatch table (~line 38)**

Add a brief comment: "Note for future subcommand specs: as additional subcommands (converge, arbitrate, gate) are specified, consider formalizing the artifact prerequisite chain as a shared state table rather than per-handler ad-hoc conditionals. The current design works for three handlers but may not scale cleanly to six or more."

Source: RC-7 (Round 2). Integration-architect AR-5 (revised), relocated to SKILL.md per devils-advocate T-4.

### Deferred items (noted for future specs)

**D-1 (P2): Sentinel formalization across future handlers**: The broader question of sentinel conventions (canonical forms, matching rules, case sensitivity) across all handlers should be addressed when additional subcommands are specified. The specific mismatch between the define and mode handlers is resolved by K-10 above, but the general sentinel formalization question remains open.

Source: Round 1 D-1; scope narrowed by K-10.

**D-2 (P3): Interest deduplication/overlap detection**: When two interests have substantially overlapping perspectives, the interests handler could warn about correlated agents. This would reduce wasted agent launches in the N^2 cross-review phase. Uncontested but out of scope for spec 008.

Source: Round 1 D-2.

---

## Key Concessions

Each concession represents a position that an agent held, was challenged, and then explicitly abandoned. All concessions are traced to their source. This section covers Round 2 concessions only; Round 1 concessions are documented in the Round 1 synthesis and remain in force.

### functional-typing concessions (Round 2)

1. **Interest count resolution direction reversed.** Preferred "relax the spec to 2 or more" but reversed to "enforce the upper bound" after both cross-reviewers identified the cost-estimate-as-throttle dependency. (functional-typing revision S-5/NR-1: "I withdraw the preference for resolution 2. Both cross-reviewers' reasoning is sound.")

2. **`(none)` sentinel P3 classification was internally inconsistent.** Claiming the SKILL.md "handles this correctly" while noting a text mismatch is contradictory. Elevated to P2. (functional-typing revision D-1 revised: "I withdraw the claim that the SKILL.md handles this correctly.")

3. **OBA-1 "inconsequential" dismissal was wrong.** The unequal prior probability of modes is consequential for K-6 and K-7's design rationale. Revised to "consequential but not requiring a new recommendation." (functional-typing revision OBA-1 revised.)

4. **D-3 withdrawn as formal deferred item.** A flag rename in a pre-shipped system does not warrant a standing deferred item. (functional-typing revision D-3 modified.)

### integration-architect concessions (Round 2)

1. **Standalone naming-pattern mapping table withdrawn.** The four-row table collapsed multi-signal inference into single-dimension lookup, producing false positives. Adopted "interest structure" language instead. (integration-architect revision AR-1 revised.)

2. **Sentinel resolution direction changed.** Changed from prefix matching (option a) to canonical form standardization (option b) after functional-typing demonstrated that prefix matching introduces its own fragility. (integration-architect revision AR-2 maintained, direction changed.)

3. **Cost formula display superseded by computed count.** Conceded to devils-advocate's Option (b): at mode confirmation, display a computed number, not the formula. The formula belongs in implementer documentation. (integration-architect revision AR-3 superseded.)

4. **Parenthetical type labels removed from calibration prompt.** Both cross-reviewers identified the contradiction with the No Game Theory Knowledge constraint. (integration-architect revision AR-4 revised.)

5. **Timestamp concern separated and withdrawn.** Content-hash proposal would be a design change requiring its own deliberation. Current mtime-based staleness detection works for spec 008's scope. (integration-architect revision AR-5 revised.)

### devils-advocate concessions (Round 2)

1. **Hard stop for CLARIFY-tag third exit state conceded.** The hard stop contradicts the "recommend, do not require" principle and deferred-resolution design that had already been accepted. Adopted integration-architect's user-confirmed degraded mode. (devils-advocate revision AR-1 revised: "That is an internal contradiction. I concede it.")

2. **AR-4 and MO-2 withdrawn.** Internal inconsistency with AR-2 (cannot argue the formula is too implementer-facing while proposing it at an earlier step) and relitigation of Round 1 cost-placement concession. (devils-advocate revision AR-4 withdrawn.)

3. **OBA-1 arbiter critique conceded.** The arbiter's general observation 7 is a summary headline; the detailed opinion demonstrably engaged with architecture. (devils-advocate revision OBA-1 conceded.)

---

## Summary

The two-round deliberation of spec 008 has reached stable closure. No blocking defects were identified by any reviewer at any phase across two rounds. All 13 functional requirements have traceable implementations. All 5 success criteria are achievable. The three spec constraints (no game theory knowledge, no agents without confirmation, no hard-coded agents/paths) are honored.

**Round 1** established eight convergence points, resolved three disputes through synthesis, and produced a baseline set of actionable changes. **Round 2** reaffirmed all Round 1 results, resolved all three remaining disputes from Round 1, established ten additional convergence points, and surfaced three new disputes -- two of which were resolved through synthesis (with the third being a minor P2/P3 priority disagreement resolved at P2).

The final output is: **4 P1 spec changes, 1 P2 spec change, 4 P1 SKILL.md changes, 6 P2 SKILL.md changes, 1 P3 SKILL.md change, and 2 deferred items**. The most significant changes are: (a) the spec's ambiguous-type handling is updated to match the SKILL.md's superior heuristic detection, (b) the CLARIFY-tag handling now has a fully specified control flow with a user-confirmed degraded mode as the terminal fallback, (c) the cost estimate is user-legible (computed count, not formula), (d) the cross-validation examines the full interest structure rather than naming patterns alone, (e) the `(none)` sentinel mismatch is resolved before it ships, and (f) the interest count upper bound is enforced with a warning gate.

One dispute was resolved through synthesis: the K-2 third exit state adopts the user-confirmed degraded mode with a concrete definition of generic calibration, combining the deferred-resolution design intent with an actionable specification of what "generic" means in prompt-generation terms. Two remaining disputes are purely about calibration values (interest count threshold: 5, per 2-to-1 alignment; cost estimate priority: P2, per 2-to-1 alignment) and are resolved by the synthesis above.

The spec and SKILL.md are substantively sound and ready for implementation with the agreed changes.
