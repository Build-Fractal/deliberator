# Integration Architect — Cooperative Disputes (Phase 4, Round 2)

**Spec**: `008-interests-mode`
**Role**: integration-architect
**Round**: 2 of 2 (Final)
**Date**: 2026-03-22

---

## Remaining Disputes

### 1. K-2 third exit state: double-declination stop vs. user-confirmed degraded mode

All three reviewers agree in Round 2 that the K-2 CLARIFY-tag handling needs a specified third exit state -- the scenario where the user declines both choosing a calibration style and returning to `/conversus define`. The convergence on the first two exits is complete: (1) user chooses a calibration style, proceed; (2) user declines to choose and is presented with the recommendation to run `/conversus define`. The dispute is about what happens when the user declines _again_.

**Functional-typing's revised position (K-2 revised)**: A two-attempt loop. First declination triggers a recommendation to run `/conversus define`. Second declination triggers a hard stop: "Cannot proceed without a calibration style." This narrows the deferred-resolution window but does not eliminate it -- the user gets one round of deferred resolution before the handler stops.

**Devils-advocate's revised position (NR-1)**: A user-confirmed degraded mode. If the user declines both options, the handler explains that interest prompts will use generic calibration rather than type-specific calibration, states this explicitly, and asks the user to confirm proceeding with generic calibration. If confirmed, generate interests with generic prompts. If declined, stop with the recommendation to run `/conversus define`.

**My position**: I favor devils-advocate's user-confirmed degraded mode over functional-typing's double-declination hard stop, but with a structural reservation that narrows the gap.

Devils-advocate's resolution is more consistent with the deferred-resolution design. The define handler's CLARIFY tag promises "this needs resolution, but not necessarily right now" (SKILL.md line 889). Functional-typing's double-declination stop converts this to "this needs resolution within two prompts." While functional-typing correctly observes that the interests handler's calibration table (SKILL.md lines 957-962) has no "uncalibrated" row -- it structurally requires a type -- devils-advocate's "generic calibration" path addresses this by providing a degraded but functional calibration that the user explicitly confirms. The user remains in control (satisfying the User Confirmation Gate at spec.md line 104), no type is silently defaulted (satisfying Domain Agnosticism at spec.md line 105), and the workflow is not hard-blocked.

The structural reservation: "generic calibration" must be defined. The Interest Generation table (SKILL.md lines 957-962) has four calibration styles and no generic row. Devils-advocate's NR-1 proposes generating interests with "generic prompts" but does not specify what those prompts contain. If "generic" means "cooperative without saying so," it is the `integration` default under a different name -- which all three reviewers rejected in Round 1. If "generic" means "no perspective or prompt content," the resulting interests.md would be missing the fields that downstream consumers (the mode handler's Perspective field mapping at SKILL.md line 1203) depend on.

For the user-confirmed degraded mode to be implementable, "generic calibration" must mean: prompts that describe each interest's role and perspective without type-specific adversarial, cooperative, honesty-calibrated, or red/blue framing. Concretely, the Perspective field would use a neutral formulation ("This interest represents [name]'s position on the problem") and the Prompt field would use a factual-inquiry formulation ("Articulate [name]'s position, priorities, and constraints regarding the problem statement") rather than the type-calibrated formulations in the Interest Generation table.

If the generic calibration is defined in this way, I accept devils-advocate's resolution. If it remains undefined, functional-typing's double-declination stop is safer because it avoids generating structurally incomplete interests.

**Status**: Narrow dispute. Resolvable by defining the generic calibration content. Not a blocking issue -- either resolution is acceptable and both are superior to leaving the third exit state unspecified.

---

### 2. Interest count upper-bound: threshold value

All three reviewers now agree on the resolution _direction_ for S-5/NR-1: the SKILL.md post-write validation should enforce an upper-bound on interest count, and the cost estimate (C-6/K-5) should remain an informational display rather than being promoted to a validation gate. This was the most significant cross-review correction of Round 2 -- functional-typing reversed their preferred resolution (from "relax the spec" to "enforce the bound") after both my DC-1 and devils-advocate's DC-1 independently identified that the relaxation path had no enforcement mechanism.

The remaining dispute is about the _threshold value_ and the _enforcement mechanism_.

**Functional-typing's NR-1**: Set the ceiling at 5 (matching the spec's "2-5" range). Enforce it as a warning gate with user override -- warn above 5 with a computed cost estimate, but allow the user to confirm and proceed.

**My position**: The warning-gate-with-override mechanism is correct. The threshold of 5 is reasonable as the default but may be too restrictive for some problem domains. At N=5 the cost is 31 launches per round, which is manageable. At N=7 the cost is 57, which is expensive but not unreasonable for a complex integration problem with seven stakeholders. At N=10 the cost is 111, which is clearly in "are you sure?" territory.

I would prefer a threshold of 7 rather than 5 as the warning trigger. The spec's "2-5" range was written as guidance for the typical case, not as a hard architectural limit. A threshold of 7 accommodates the most common exceptions (6-7 stakeholders in complex integration or scoping problems) while still triggering a warning before quadratic scaling becomes punitive. The threshold of 5 would produce a warning for every problem with more than 5 interests, which risks warning fatigue.

However, this is a P2 calibration question, not an architectural dispute. Both 5 and 7 are defensible thresholds. The important convergence is on the mechanism (warning gate with override) and the principle (the cost estimate remains informational, the upper-bound provides the enforcement). If functional-typing and devils-advocate prefer 5, I will not dispute it further.

**Status**: Narrow dispute on threshold value. The mechanism is converged. Not blocking.

---

## Convergence

The following items have reached full three-reviewer agreement in Round 2. Combined with the Round 1 convergence set (C-1 through C-10), these represent the complete set of settled items ready for final synthesis and implementation.

### Round 1 Convergence (reaffirmed)

All ten convergence points from Round 1 (C-1 through C-10) are reaffirmed without modification by all three Round 2 revisions. All prior concessions stand. All three dispute resolutions from the Round 1 synthesis are adopted without reservation.

### Round 2 Convergence

#### RC-1: Resolution direction for interest count upper-bound (was S-5)

All three reviewers now agree: the SKILL.md post-write validation must enforce an upper-bound on interest count. The cost estimate (C-6/K-5) remains an informational display, not a validation gate. The spec's "2-5" range establishes the principle; the SKILL.md must implement it. Only the threshold value remains in narrow dispute (see Dispute 2 above).

- **Functional-typing**: Reversed from resolution 2 (relax) to resolution 1 (enforce) per both cross-review DCs.
- **Integration-architect**: DC-1 identified the enforcement-mechanism gap in the relaxation path.
- **Devils-advocate**: DC-1 independently confirmed the formula-as-throttle is insufficiently legible.

#### RC-2: Computed count replaces formula in user-facing cost estimate (was K-5)

All three reviewers agree: the K-5 user-facing cost estimate at mode confirmation should display a computed agent launch count, not the raw formula `N^2 + N + 1`. The handler knows N, rounds=1, iterations=1, and arbiter=absent at confirmation time and can compute an exact number. The formula remains in the Important Notes section (SKILL.md lines 1304-1308) as implementer documentation with explicit qualifications: (1) assumes all N agents cross-review all others, (2) assumes iterations=1.

User-facing text at mode confirmation:
> "This configuration will launch {computed_count} agents."

Or, per functional-typing's revision:
> "Estimated agent launches per round: {computed_count} (all {count} agents cross-review all others, single iteration)."

The exact wording is editorial; the substance (computed count, not formula) is settled.

- **Devils-advocate**: Originally proposed Option (b) in MO-1; accepted by both cross-reviewers.
- **Integration-architect**: Conceded in revision that AR-3 is superseded; formula belongs in implementer docs.
- **Functional-typing**: Accepted with the addition of the iteration assumption qualifier.

#### RC-3: K-6 cross-validation examines full interest structure, not naming patterns alone

All three reviewers agree: the K-6 cross-validation description should replace "naming pattern" with "interest structure (names, perspectives, and prompts)." Interest names alone are insufficient for reliable type inference because many valid names are semantically opaque (`alpha`, `beta`, `option-a`). When the cross-validation fires, it should examine interest names for semantic signals, perspective sentences for type-consistent language, and prompt content for calibration-consistent framing.

My original AR-1 (standalone naming-pattern-to-type mapping table) is withdrawn as a deterministic classifier. Functional-typing's DC-1 was decisive: the table collapses multi-signal inference into single-dimension lookup, producing false positives (e.g., interests named "postgres," "redis," "kafka" in an integration problem triggering a false "selection" warning). Naming patterns remain one useful signal among several, not a complete mapping.

For implementation guidance, reference the heuristic detection signal vocabulary (SKILL.md lines 1151-1154) as the canonical signal source rather than extracting a single-dimension subset.

- **Devils-advocate**: Originally proposed AR-3; accepted by both other reviewers.
- **Integration-architect**: Withdrew standalone table; adopted "interest structure" language.
- **Functional-typing**: DC-1 provided the decisive counterexample.

#### RC-4: K-2 calibration styles use plain-language descriptions without type labels

All three reviewers agree: when the interests handler presents calibration styles for a CLARIFY-tagged type, the descriptions must not include type names or mode names in parentheticals. The No Game Theory Knowledge constraint (spec.md line 103) applies to calibration-style selection, not just mode selection.

Revised prompt text (per my revision, AR-4 revised):
```
The problem type needs clarification. How should agents approach this deliberation?

1. Each agent advocates for its preferred option
2. Each agent advocates for its needs while finding common ground
3. Each agent honestly declares its responsibilities and boundaries
4. Attackers try to break it, defenders show it holds up
```

No parenthetical labels. No type names. Both cross-reviewers (functional-typing DC-2, devils-advocate DC-1) independently identified the contradiction in my original AR-4 which included parenthetical type names. I concede the parentheticals and accept the clean descriptions.

- **Functional-typing**: DC-2 identified the type-name exposure as violating spec.md line 103.
- **Devils-advocate**: DC-1 made the same point via the 1-to-1 mapping between types and modes.
- **Integration-architect**: Revised AR-4 to remove parentheticals.

#### RC-5: `(none)` sentinel standardized to canonical form (was AR-2 / D-1 / MO-2 / NR-2)

All three reviewers agree: the mismatch between the define handler's `(none -- no context documents provided)` (SKILL.md line 891) and the mode handler's `(none)` check (SKILL.md line 1254) is a real implementation hazard, not a theoretical concern. All three agree the fix should be within spec 008's scope rather than fully deferred to D-1.

The resolution direction is converged: standardize to `(none)` in the define handler's output (option b). Functional-typing's argument that prefix matching on `(none` introduces its own fragility class (e.g., `(none of the above apply)` would match) is correct, and I concede my original preference for option (a). Changing one line of sentinel text in the define handler is lower risk than introducing a matching rule that future sentinels must avoid colliding with.

- **Integration-architect**: Originally preferred option (a); revised to option (b) per functional-typing T-2.
- **Functional-typing**: NR-2 specifies the change; P2 priority, within spec 008 scope.
- **Devils-advocate**: Did not contest; the mismatch stands as accepted by all.

D-1 remains as a broader deferred item for sentinel formalization across future handlers, but the specific mismatch in the current code path is resolved.

#### RC-6: OBA-1 (equal-probability assumption) is consequential, not inconsequential

Functional-typing revised OBA-1 to withdraw the "inconsequential" characterization, accepting my DC-2 reasoning: the unequal prior probability of modes under heuristic detection is the architectural justification for both K-6 (cross-validation when signals conflict with stated type) and K-7 (zero-signal presentation of all modes). These are distinct mechanisms because the modes are not equally likely, and both depend on this being the case.

The revised characterization: "Off-base and consequential for the design of K-6 and K-7, but not requiring a new recommendation because K-6 and K-7 already handle the consequences correctly." This is the right landing -- the observation informs the rationale for existing recommendations rather than generating a new one.

- **Functional-typing**: Withdrew "inconsequential" per integration-architect DC-2.
- **Integration-architect**: DC-2 traced the dependency to K-6 and K-7.
- **Devils-advocate**: T-2 (via cross-review of functional-typing) supported the non-dismissal.

#### RC-7: AR-5 (prerequisite chain advisory) separated from timestamp concern

All three reviewers accept the substance of the state-model advisory -- the prerequisite chain will become complex enough to warrant a shared model as future subcommands are added. The timestamp fragility concern and the content-hash proposal are withdrawn as out of scope for spec 008 (functional-typing T-1, devils-advocate DC-2 correctly separated these). The state-model advisory note should be placed in the SKILL.md near the subcommand dispatch table (lines 19-38) rather than in a synthesis deferred-items section, since the SKILL.md is the document future spec implementers will read.

- **Integration-architect**: Withdrew timestamp criticism and content-hash proposal; retained advisory.
- **Functional-typing**: T-1 separated the two concerns.
- **Devils-advocate**: DC-2 noted content hashes would be a design change requiring its own deliberation.

#### RC-8: D-3 (`--output` flag rename) withdrawn as a formal deferred item

Functional-typing withdrew D-3, accepting that a deferred item for a flag rename in a system with no shipped CLI is overengineered. The naming observation stands as a P3 editorial note but does not warrant a standing deferred item. The deferred items list simplifies to D-1 (sentinel formalization, broader scope) and D-2 (interest deduplication/overlap detection).

- **Functional-typing**: Withdrew per integration-architect T-4 and devils-advocate T-4.
- **Integration-architect**: T-4 identified the premature deferral process.
- **Devils-advocate**: T-4 noted the weaker support base compared to D-1 and D-2.

#### RC-9: Devils-advocate's OBA-1 (arbiter underweights architecture) conceded

Devils-advocate conceded that the arbiter's general observation 7 is a summary characterization, not a claim that no architectural implications exist. The arbiter's Dispute 1 opinion demonstrably engaged with architecture across six paragraphs. The critique conflated a headline with the analysis beneath it. The forward-looking concern about non-interactive execution is valid but deferred.

- **Devils-advocate**: Conceded per integration-architect DC-2 and functional-typing DC-2.

#### RC-10: Devils-advocate's AR-4 (interest-count cost note at interests confirmation) withdrawn

Devils-advocate withdrew AR-4 after functional-typing identified two problems: (1) premature optimization pressure before the mode is known, and (2) internal inconsistency with AR-2 (cannot argue the formula is too implementer-facing for mode confirmation while proposing it at an earlier step). The C-6 cost estimate at mode confirmation remains the right and only placement.

- **Devils-advocate**: Withdrew, acknowledging the internal inconsistency with AR-2.

---

## Final Position Statement

The two-round deliberation has reached stable closure. The cross-review process in Round 2 was the most productive phase of the entire deliberation -- it corrected three significant errors (the interest count resolution direction, the `(none)` sentinel handling, and the OBA-1 consequentiality assessment), withdrew two overengineered proposals (D-3 deferred item, AR-1 mapping table), and tightened four converged recommendations (K-5 computed count, K-6 interest structure language, K-2 plain-language calibration styles, AR-5 separation of concerns).

Two narrow disputes remain. Neither is blocking. Both concern calibration within an agreed mechanism rather than disagreement about the mechanism itself:

1. **K-2 third exit state**: Whether the user who declines twice should hit a hard stop (functional-typing) or be offered a user-confirmed degraded mode (devils-advocate, supported by integration-architect with the reservation that "generic calibration" must be concretely defined). Both resolutions close the gap; the choice is between strictness and flexibility.

2. **Interest count threshold**: Whether the warning gate triggers at 5 (functional-typing) or 7 (integration-architect preference). Both values are defensible; the mechanism (warning gate with user override) is settled.

### Complete Recommendation Table

#### Spec changes

| ID | Item | Priority | Status |
|---|---|---|---|
| S-1 | Replace `ambiguous` row with heuristic detection reference | P1 | Converged (C-1, all rounds) |
| S-2 | Add `Preset` field to interests.md schema | P1 | Converged (C-2, all rounds) |
| S-3 | Document `--output` as workspace override | P1 | Converged (Dispute 2 resolution, all rounds) |
| S-4 | Rename or footnote Confidence column | P2 | Converged (C-11, all rounds) |

#### SKILL.md changes

| ID | Item | Priority | Status |
|---|---|---|---|
| K-1 | Preset existence validation in post-write check | P1 | Converged (C-3, all rounds) |
| K-2 | CLARIFY-tag handling with specified third exit state | P1 | Narrow dispute on third exit (stop vs. degraded mode) |
| K-3 | Draft status behavior: warn and proceed | P1 | Converged (C-5, all rounds) |
| K-4 | Heuristic-is-advisory sentence | P2 | Converged (C-4, all rounds) |
| K-5 | Cost estimate: computed count with assumptions | P2 | Converged (RC-2, Round 2) |
| K-6 | Cross-validation on full interest structure | P2 | Converged (RC-3, Round 2) |
| K-7 | Zero-signal: present all four modes | P2 | Converged (C-8, all rounds) |
| K-8 | Extension-points note with "extend"/"add" language | P2 | Converged (Dispute 3 resolution, all rounds) |
| NR-1 | Interest count upper-bound warning gate | P2 | Mechanism converged; threshold in narrow dispute (5 vs. 7) |
| NR-2 | Standardize `(none)` sentinel to canonical form | P2 | Converged (RC-5, Round 2) |
| -- | State-model advisory near subcommand dispatch table | P3 | Converged (RC-7, Round 2); editorial note |
| -- | Calibration style descriptions without type labels | P2 | Converged (RC-4, Round 2); folded into K-2 |

#### Deferred items

| ID | Item | Priority |
|---|---|---|
| D-1 | Sentinel formalization (broader, future handlers) | P2 |
| D-2 | Interest deduplication/overlap detection | P3 |

### Assessment

The spec and SKILL.md are substantively sound. No blocking defects have been identified by any reviewer at any phase across two rounds. All 13 functional requirements have traceable implementations. All 5 success criteria are achievable. All three spec constraints are honored. The deliberation produced genuine improvements: the SKILL.md's heuristic detection was recognized as superior to the spec's static default (a rare spec-updates-from-implementation direction), the CLARIFY-tag handling now has a specified control flow, the cost estimate is user-legible, the cross-validation examines the right signals, and the sentinel mismatch is resolved before it ships.

The two remaining disputes are the narrowest possible form of disagreement -- both are about parameter values within fully converged mechanisms. A final synthesis can resolve both by choosing either side without architectural consequence. The deliberation is ready for final synthesis and implementation.
