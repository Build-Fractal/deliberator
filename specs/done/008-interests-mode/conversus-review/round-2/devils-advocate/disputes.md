# Devils-Advocate Disputes — Round 2 (Final Phase)

**Spec**: `008-interests-mode`
**Role**: devils-advocate
**Phase**: 4 — Final Disputes
**Round**: 2 of 2
**Date**: 2026-03-22

---

## Remaining Disputes

### 1. K-2 third exit state: degraded mode vs. double-declination stop

All three revisions agree the third exit state must be specified. The gap is real and closed by this round. The dispute is about the resolution mechanism.

**Functional-typing** (NR revision, K-2): Proposes a two-attempt flow. First declination triggers a binary choice prompt (choose a style or stop and run `/conversus define`). Second declination triggers a hard stop: "Cannot proceed without a calibration style." This narrows the deferred-resolution window to one additional interaction but does not eliminate it. Functional-typing explicitly accepts that this makes CLARIFY-tag resolution effectively mandatory for the interests handler after two attempts.

**Integration-architect** (DC-1 of my review, revision NR-1 implicit in cross-review): Proposes a user-confirmed degraded mode. If the user declines both choosing a calibration style and running `/conversus define`, the handler explains that prompts will use generic calibration rather than type-specific calibration, asks the user to confirm proceeding with generic calibration. If confirmed, generate interests with generic prompts. If declined, stop processing.

**My revision** (NR-1): I conceded the hard stop and adopted integration-architect's user-confirmed degraded mode. The hard stop I originally proposed contradicts the "recommend, do not require" principle and the define handler's deferred-resolution design, both of which I had already accepted. Conceded.

**The dispute**: Functional-typing's double-declination stop and integration-architect's (and my revised) degraded mode arrive at different architectures:

- **Double-declination stop** preserves the principle that calibrated prompts are structurally required. The interests handler's calibration table (SKILL.md lines 957-962) has no "uncalibrated" row, so functional-typing argues there is no legitimate generic-calibration path. After two opportunities, the handler stops because it genuinely cannot proceed without a type. This is honest about the handler's structural requirement.

- **User-confirmed degraded mode** preserves the define handler's deferred-resolution design more broadly. The handler can proceed with generic prompts, at the cost of producing lower-quality interest prompts. The user knows this and confirms. This keeps the workflow unblocked at the expense of prompt calibration quality.

Both positions are internally consistent after revision. The genuine question is whether the interests handler's calibration table creates a structural requirement for a type (functional-typing's position) or whether generic calibration is a legitimate, if degraded, operating mode (integration-architect's and my revised position).

I observe that functional-typing's position has a structural advantage: the calibration table as currently specified in the SKILL.md does not include a "generic" row. Any implementation of generic calibration would need to invent prompts not covered by the existing specification. The degraded mode I adopted requires specifying what "generic calibration" means in practice -- what prompts does the handler generate when no type is available? Neither integration-architect's cross-review nor my revision addresses this. If generic calibration is underspecified, the double-declination stop is the safer choice because it avoids generating output from an unspecified code path.

However, functional-typing's double-declination stop is functionally equivalent to a hard requirement with an extra interaction step, which is precisely what the arbiter warned against (resolution.md lines 60-62). The distinction between "require after one prompt" and "require after two prompts" is quantitative, not qualitative.

**My final position**: This dispute reduces to a design decision that the synthesizer must make. Both approaches are defensible. If the synthesizer chooses the degraded mode, the specification must define what "generic calibration" prompts look like. If the synthesizer chooses the double-declination stop, the specification should acknowledge that this makes CLARIFY-tag resolution mandatory for the interests handler, narrowing the define handler's deferred-resolution contract. I will not advocate further for either path -- both are improvements over the unspecified status quo, and both respect the concessions I made in revision. The gap is closed in either direction.

### 2. Interest count upper bound: enforcement mechanism

All three revisions agree the spec/SKILL.md divergence (spec says "2-5", SKILL.md enforces only "2+") is a genuine gap. Functional-typing reversed their preferred resolution from "relax to 2 or more" to "enforce the upper bound in the SKILL.md," adopting the reasoning from both my cross-review (DC-1) and integration-architect's cross-review (DC-1) that the cost estimate is not fit to serve as the sole throttle.

**Where convergence exists**: All three reviewers agree:
- The gap is real (P2).
- The cost estimate (C-6/K-5) should remain an informational display, not a validation gate.
- An upper-bound enforcement mechanism must exist in the SKILL.md.

**Where variation remains**: Functional-typing's NR-1 proposes a warning gate at 5 with user override: if more than 5 interests are present, warn with the computed cost count and ask the user to confirm. The user can override. This is a soft ceiling, not a hard block.

Integration-architect did not specify an exact threshold but suggested the bound could be raised to 7 or 8 if 5 is too restrictive.

My cross-review (DC-1) identified the mechanism gap but did not prescribe a specific threshold.

**My final position**: Functional-typing's NR-1 is the right resolution. The warning gate at 5 with user override is the correct design because:

1. It reconciles the spec and SKILL.md without modifying either document's contract -- the spec's "2-5" remains valid as the default range, while users who need more can explicitly opt in.
2. It preserves C-6/K-5 as an informational display by providing a separate enforcement mechanism (the warning gate) rather than relying on the cost estimate to serve as a throttle.
3. The computed cost count in the warning message ("You have {count} interests. The agent-launch cost scales quadratically (estimated {count^2 + count + 1} launches per round).") gives users the information they need to make an informed override decision.

The specific threshold (5 vs. 7 vs. 8) is an implementation detail. The design is the warning gate with override. I accept this without further dispute.

### 3. `(none)` sentinel standardization: scope and resolution

All three revisions agree:
- The mismatch between `(none -- no context documents provided)` (define handler, SKILL.md line 891) and `(none)` (mode handler, SKILL.md line 1254) is real.
- The mismatch should be fixed at P2, not deferred to D-1.
- The resolution direction should be option (b): standardize the define handler's sentinel to `(none)`, not option (a): introduce prefix matching.

**Where variation remains**: Functional-typing's NR-2 specifies the change as: "Change the define handler's sentinel from `(none -- no context documents provided)` to `(none)`." Integration-architect's AR-2 (revised) agrees with option (b) but frames the broader sentinel formalization question (D-1) as still valid for future handlers.

**My final position**: This is settled. All three reviewers converge on the same fix (standardize to `(none)` in the define handler) for the same reason (eliminates the matching ambiguity without introducing fragile prefix-matching rules). D-1 remains as a broader deferred item for sentinel conventions across future handlers, but the specific mismatch in the current code path is fixed within spec 008. No further dispute.

---

## Convergence

### Settled positions accepted without further challenge

**1. All Round 1 convergence points (C-1 through C-10) are settled.** No reviewer at any phase of Round 2 proposed reopening any of these. They are stable and ready for implementation.

**2. All Round 1 dispute resolutions are accepted.** Dispute 1 (CLARIFY-tag handling: recommend, do not require), Dispute 2 (--output as workspace override), Dispute 3 (complete config with extensions, not starter template). All three revisions reaffirm all three resolutions without reservation.

**3. All spec changes (S-1 through S-4) are confirmed.** The ambiguous row replacement, Preset field addition, --output documentation, and Confidence column rename/footnote are universally accepted at their stated priorities.

**4. All SKILL.md changes (K-1 through K-8) are confirmed.** Preset validation, CLARIFY-tag handling, draft status behavior, heuristic-is-advisory sentence, cost estimate, cross-validation warning, zero-signal handling, and extension-points note. K-2 and K-5 have revised implementation language (see below) but the substance and priority are unchanged.

**5. K-5 cost estimate: computed count, not formula.** All three revisions converge. The user-facing display at mode confirmation should show a computed agent launch count, not the raw formula. The formula belongs in the SKILL.md's Important Notes section as implementer documentation. Integration-architect explicitly conceded to my Option (b) in their revision. Functional-typing accepted the substance. The revised display text converges on: "This configuration will launch {computed_count} agents" or equivalent, with the parenthetical noting the cross-review and iteration assumptions per functional-typing's T-3 and integration-architect's AR-3.

**6. K-6 cross-validation: full interest structure, not naming patterns alone.** All three revisions converge. Replace "naming pattern" with "interest structure (names, perspectives, and prompts)" in C-7's description. Integration-architect withdrew the standalone mapping table (AR-1 revised), acknowledging that naming patterns are one input among several. For implementation guidance, reference the full heuristic detection signal vocabulary (SKILL.md lines 1151-1154) rather than extracting a single-dimension subset.

**7. Integration-architect's AR-4 calibration style prompt: type labels removed.** Both my cross-review (DC-1) and functional-typing's cross-review (DC-2) independently identified that parenthetical type names `(selection)`, `(integration)`, `(scoping)`, `(stress-test)` violate the No Game Theory Knowledge constraint. Integration-architect conceded in revision and removed the labels. The prompt text presents plain-language descriptions without internal taxonomy vocabulary. Settled.

**8. D-3 (`--output` flag rename) withdrawn as a formal deferred item.** Functional-typing withdrew this in revision, accepting integration-architect's point that creating a deferred item for a flag rename in a system with no shipped CLI is overengineering. The naming mismatch is noted as a P3 editorial observation. The deferred items list is simplified to D-1 and D-2.

**9. OBA-1 (arbiter's "all disputes are about language" characterization): conceded.** I conceded this in revision. Integration-architect's DC-2 was decisive: the arbiter's observation 7 is a summary characterization, not a claim that no architectural implications exist anywhere. The arbiter's Dispute 1 opinion spends six paragraphs on architectural analysis. My critique conflated a headline with the analysis beneath it. The non-interactive execution concern is valid as a forward-looking note but is not a spec 008 issue. Closed.

**10. OBA-1 (equal-probability assumption): consequential but already handled.** Functional-typing revised from "inconsequential" to "consequential for the design of K-6 and K-7 but not requiring a new recommendation." Integration-architect's DC-2 was correct: the unequal prior probability of modes under heuristic detection is the architectural justification for K-6 and K-7 as separate mechanisms. This observation informs the rationale for existing recommendations rather than generating a new one. Settled.

**11. D-1 sentinel formalization: scope narrowed but retained.** The specific `(none)` mismatch between define and mode handlers is fixed within spec 008 (NR-2 across all revisions). D-1 remains as a broader deferred item for sentinel conventions in future handlers, but its urgency is reduced. Settled.

**12. AR-5 (prerequisite chain advisory): relocated.** Integration-architect revised: drop the timestamp criticism and content-hash proposal. Keep the state-model advisory but place it as a comment in the SKILL.md near the subcommand dispatch table, not in the synthesis deferred-items section. This is the right location -- the SKILL.md is the living document that future implementers will read. The timestamp fragility observation is withdrawn as premature for spec 008's scope. Settled.

**13. All prior concessions from both rounds stand without reversal.** Across all three reviewers:

- Functional-typing: P0 severity demotion, CLARIFY-tag extract-and-warn withdrawal, staleness warning withdrawal, "specification drift" reframing. Plus: `integration` default fully eliminated (Round 2).
- Integration-architect: FR-007 downgrade, Preset field as spec omission, preset validation escalation, extract-and-warn withdrawal. Plus: AR-1 mapping table withdrawn, AR-4 type labels removed, AR-3 superseded by computed count, AR-5 timestamp criticism dropped (Round 2).
- Devils-advocate (me): interests.md-as-optional withdrawal, formalized keyword scoring withdrawal, cost estimate placement correction, "fabricated" confidence retraction, winner-take-all for integration dropped. Plus: AR-1 hard stop conceded, AR-4 withdrawn, MO-2 withdrawn, OBA-1 conceded (Round 2).

No reversal pressure exists from any direction. The concession set is definitive.

---

## Final Position Statement

The deliberation has reached stable closure. Two rounds of review, cross-review, and revision across three reviewers produced a converged recommendation set that is precise, well-grounded, and ready for implementation.

### What is settled

**Spec changes** (4):
- S-1 (P1): Replace `ambiguous` row with heuristic detection reference
- S-2 (P1): Add `Preset` field to interests.md schema
- S-3 (P1): Document `--output` as workspace override
- S-4 (P2): Rename or footnote Confidence column

**SKILL.md changes** (10):
- K-1 (P1): Preset existence validation in post-write check
- K-2 (P1): CLARIFY-tag handling with inline user choice, recommend define, no default (third exit state mechanism still in minor dispute -- see Remaining Dispute 1)
- K-3 (P1): Draft status behavior: warn and proceed
- K-4 (P2): Heuristic-is-advisory sentence
- K-5 (P2): Cost estimate as computed count with explicit assumptions, not formula
- K-6 (P2): Cross-validation on full interest structure (names, perspectives, and prompts)
- K-7 (P2): Zero-signal: present all four modes
- K-8 (P2): Extension-points note with "extend"/"add" language
- NR-1 (P2): Interest count upper-bound warning gate with user override
- NR-2 (P2): Standardize `(none)` sentinel to canonical form in define handler

**Deferred items** (2):
- D-1 (P2): Sentinel formalization across future handlers (scope narrowed by NR-2)
- D-2 (P3): Interest deduplication/overlap detection

### What remains in minor dispute

One item has substantive variation: the K-2 third exit state. Functional-typing proposes a double-declination stop; integration-architect and I propose a user-confirmed degraded mode. Both are improvements over the unspecified status quo. Both are internally consistent. The synthesizer should choose based on whether the interests handler's calibration table structurally requires a type (favoring the stop) or whether generic calibration is a legitimate operating mode that should be specified (favoring the degraded mode). I will not advocate further for either resolution.

### What I was wrong about

Across both rounds, I conceded eight positions. The most significant:

1. **`interests.md` as optional** (Round 1). The separate file is architecturally necessary. Three concrete dependencies rebut the proposal. I was wrong.
2. **Hard stop for CLARIFY-tag third exit state** (Round 2). The hard stop contradicts the "recommend, do not require" principle and the deferred-resolution design I had already accepted. I was wrong to prescribe a mechanism that contradicted my own stated principles.
3. **"Fabricated" confidence labels** (Round 1). The taxonomy is intentionally closed and the mappings are deterministic. Calling them fabricated was a logical error.
4. **OBA-1 critique of the arbiter** (Round 2). The arbiter engaged with the architecture in full; I conflated a summary headline with the detailed analysis.

Each concession was forced by specific, traceable reasoning from the cross-reviewers. The deliberation process worked as designed: weak positions fell, strong positions survived in refined form.

### Assessment

The spec and SKILL.md are substantively sound. No blocking defects were identified by any reviewer at any phase across two rounds. All 13 functional requirements have traceable implementations. All 5 success criteria are achievable. The three spec constraints (no game theory knowledge, no agents without confirmation, no hard-coded agents/paths) are honored.

The most significant outcome of the two-round deliberation is that the SKILL.md's behavior is consistently more sophisticated than the spec's prescriptions. In every case where the spec and SKILL.md disagreed (ambiguous-type handling, heuristic detection, interest count range, sentinel text), all three reviewers concluded the SKILL.md was correct or that the spec should be updated to match. Spec 008's primary debt is precision, not architecture -- the implementation is well-designed, and the remaining work is to make the spec and SKILL.md agree on the details of that design.

The converged recommendation set -- 4 spec changes, 10 SKILL.md changes, 2 deferred items -- is ready for synthesis and implementation.
