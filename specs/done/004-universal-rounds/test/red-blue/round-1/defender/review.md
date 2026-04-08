# Defense Brief: Spec 004 — Universal Rounds, Stagnation Detection, and Arbitration

**Role**: Blue Team Defender
**Date**: 2026-03-20
**Spec Under Review**: `/Users/business-daddy/code/payer-index-mono/conversus/specs/004-universal-rounds/spec.md`
**Implementation Record**: `/Users/business-daddy/code/payer-index-mono/conversus/specs/004-universal-rounds/work_done.md`

---

## Executive Summary

Spec 004 extends three features -- multi-round execution (`rounds > 1`), stagnation detection (`stagnation: detect`), and subject arbitration (`arbiter`) -- from cooperative-only to all four competition modes. The implementation is conservative by design: it removes two validation guards, un-drafts three existing templates, creates three new templates, and updates one validation table. No engine logic was added or modified. The spec's thesis is that the orchestrator was already mode-agnostic -- the mode restrictions were training wheels, not structural requirements. The evidence supports this thesis.

The changes are correct, complete, and safe because:

1. **All mode-specific behavior lives in templates, not the engine.** The round loop, stagnation check, and Phase 6 trigger evaluation are mode-agnostic code paths that delegate mode semantics to template content. Removing the validation guards exposed this delegation, it did not create it.
2. **Stagnation detection reuses the existing Dispute-Parsing Subsystem**, which was already mode-aware before this spec. No new parsing logic was introduced.
3. **The arbitration templates for non-cooperative modes already existed** -- they were gated by a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker. Un-drafting them was a promotion decision, not a creation decision.
4. **Cross-round synthesis templates follow the cooperative template's structural contract** (same variables, same section flow, same rules) while adapting content to each mode's game dynamics.
5. **Backward compatibility is fully preserved.** No existing behavior, path, validation rule, or template was modified for cooperative mode.

---

## Architecture Rationale

### Why Validation Removal Is Safe

The two removed validation rules were:

- `"rounds > 1 is only supported in cooperative mode (current mode: {mode})."`
- `"arbiter is only supported in cooperative mode (current mode: {mode})."`

These rules existed in SKILL.md's Step 1 validation section. They were added during spec 001 and 002 development as a scope limitation -- cooperative mode was the first mode to receive rounds and arbitration, and the validation gates prevented premature use in other modes before templates existed.

The safety argument rests on the engine's architecture: **the round loop, stagnation detection, and Phase 6 dispatch are mode-unaware code paths.** Evidence:

1. **Round loop** (SKILL.md L294-313): The outer round loop wraps Phases 1-5 and checks termination conditions. None of the four termination conditions (`no disputes remain`, `stagnation detected`, `max rounds reached`, `continue`) reference the mode. The loop dispatches phases using `templates/{mode}/` paths, but the loop itself is mode-agnostic.

2. **Stagnation detection** (SKILL.md L474-478): Compares dispute counts between rounds using the Dispute-Parsing Subsystem. The subsystem (SKILL.md L656-683) already has mode-specific fallback headings for all four modes: `### Remaining Disputes` (cooperative), `### Disputed Risks` (red-blue), `## Runner-Up` (winner-take-all), `## Disputed Boundaries` (prisoners-dilemma). These headings were defined before spec 004 -- the subsystem was designed for future mode support.

3. **Phase 6 trigger evaluation** (SKILL.md L539-542): Uses the Dispute-Parsing Subsystem to determine whether disputes remain. The same mode-aware parsing that works for cooperative mode works for all modes, because the subsystem dispatches on mode internally.

4. **Template loading** (SKILL.md L244-251): All template paths use `templates/{mode}/`. The engine loads whatever template exists at the mode-specific path. When the mode was cooperative-only, only cooperative templates were exercised. With the validation gates removed, the engine will now load red-blue, winner-take-all, and prisoners-dilemma templates through the same path.

The validation rules were not protecting against an engine deficiency -- they were protecting against missing templates. Now that the templates exist, the guards are unnecessary.

### Why the Engine Needed No Changes

The spec identifies three engine changes (spec.md L200-204):

1. Remove two validation `if` statements (done -- FR-001)
2. Add mode-specific required headings to Phase 6 validation (done -- FR-009)
3. Verify round-aware variables populate for all modes (verified -- FR-010)

Item 3 is the critical verification. The round-aware template variables (`{ROUND}`, `{MAX_ROUNDS}`, `{PRIOR_SYNTHESIS_PATH}`, `{PRIOR_ROUND_DIR}`, `{PRIOR_ROUND_SECTION}`) are populated by the orchestrator in Step 4 (SKILL.md L336-342) with no mode gate. The variable population code is:

- `{ROUND}` -- current round number, set by the round loop counter
- `{MAX_ROUNDS}` -- from config `rounds` field
- `{PRIOR_SYNTHESIS_PATH}` -- computed from the prior round's output directory
- `{PRIOR_ROUND_DIR}` -- computed from the prior round's output directory

None of these computations reference the mode. They are structural properties of the round loop, not properties of any particular mode's semantics. This was verified (work_done.md L50: "Round-aware variables are populated generically by the orchestrator -- no mode gate exists").

### Why Template-First Design Is Correct

Conversus's architecture places all mode-specific prompt engineering in templates, not in the orchestrator. This is stated explicitly at SKILL.md L701: "Templates contain the mode-specific prompt engineering. The skill just fills variables and orchestrates."

This design decision means that extending to new modes (or extending existing modes with new features like rounds) is primarily a template authoring task. The orchestrator is a variable-substituting dispatcher. This is a deliberate and well-justified architecture:

- Templates are self-contained prompt documents that can be reviewed independently.
- Template changes do not risk regressions in the orchestrator.
- New mode support does not require engine patches.

Spec 004 is the first real validation of this architecture. It proves that the "add templates, remove guards" pattern works for feature extension.

---

## Safeguards in Place

### Safeguard 1: Draft-Gate Mechanism

The three non-cooperative arbitration templates (`templates/red-blue/arbitration.md`, `templates/winner-take-all/arbitration.md`, `templates/prisoners-dilemma/arbitration.md`) already existed in the codebase. They were gated by a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker on their first line.

SKILL.md L257 enforces this gate: "If the loaded template's first line contains `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`, fail with: 'Template {path} is marked as draft and cannot be used in production runs.'"

This means even if the validation rules had been removed prematurely (before templates were ready), the draft-gate would have prevented execution. The system had a defense-in-depth safeguard. Spec 004 removed the outer guard (validation rules) and the inner guard (draft markers) simultaneously, which is correct -- both guards served the same purpose (preventing use of incomplete features) and both are now obsolete.

Verification that no draft markers remain:

A grep for `TEMPLATE_STATUS.*draft` across all templates under `/Users/business-daddy/code/payer-index-mono/conversus/templates/` returns zero matches. All templates are production-ready.

### Safeguard 2: Dispute-Parsing Subsystem Fail-Safe

The Dispute-Parsing Subsystem (SKILL.md L666-679) has a three-tier fallback:

1. **Primary**: Structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`)
2. **Fallback**: Mode-specific heading-based parsing
3. **Default**: Return `true` (has disputes) as safety measure

The default-to-true behavior (SKILL.md L679) means that if a synthesis output for a new mode produces an unexpected format, the system errs on the side of running Phase 6 arbitration rather than silently skipping it. This is the correct failure mode: an unnecessary arbitration is a minor cost, while a skipped arbitration on disputed content is a correctness failure.

### Safeguard 3: Phase 6 Output Validation

SKILL.md L583-594 defines mode-specific required headings for Phase 6 output validation. The implementation (work_done.md L19) updated this validation table to include headings for all four modes:

| Mode | Required Headings (SKILL.md L587-592) |
|------|---------------------------------------|
| cooperative | Process Note, Decision Framework, Binding Decisions, Summary of Changes Required |
| red-blue | Process Note, Decision Framework, Binding Decisions, Updated Risk Register |
| winner-take-all | Process Note, Decision Framework, Verdict Review, Binding Decision |
| prisoners-dilemma | Process Note, Decision Framework, Binding Decisions, Revised Responsibility Map |

These headings were verified to match the actual `###` headings in each mode's arbitration template:

- Red-blue template headings: Process Note (L42), Decision Framework (L50), Binding Decisions (L56), Updated Risk Register (L92) -- match.
- Winner-take-all template headings: Process Note (L42), Decision Framework (L50), Verdict Review (L56), Binding Decision (L68) -- match.
- Prisoners-dilemma template headings: Process Note (L42), Decision Framework (L50), Binding Decisions (L56), Revised Responsibility Map (L89) -- match.

The validation is informational (warning, not blocking) per SKILL.md L583, which is appropriate -- malformed output is better than no output, but the warning ensures the user reviews it.

### Safeguard 4: Phase 6 Failure Handling

SKILL.md L577-581 defines failure handling for Phase 6: if the arbiter agent fails, partial output is cleaned up, a warning is emitted, and the Phase 1-5 record remains valid. This safeguard applies to all modes equally and was not modified by spec 004.

### Safeguard 5: Cooperative Mode Isolation

No cooperative-mode artifact was modified. Evidence from work_done.md L52-58:

- Cooperative mode behavior -- untouched
- Single-round execution -- untouched
- Round loop mechanics -- unchanged
- `iterations` field -- continues to work orthogonally
- Phase 1-5 templates for any mode -- unchanged
- Dispute-Parsing Subsystem -- unchanged (already mode-aware)

The cooperative `cross-round-synthesis.md` and `arbitration.md` templates were not modified. The SKILL.md validation rules that were removed only affected non-cooperative mode configs -- cooperative configs never triggered those rules. The Phase 6 validation heading table change was additive (new rows for new modes; the cooperative row is unchanged at SKILL.md L589).

---

## Resilience Evidence

### Evidence 1: Structural Consistency Across Templates

All three new cross-round synthesis templates follow the cooperative template's structural contract:

| Structural Element | Cooperative | Red-Blue | Winner-Take-All | Prisoners-Dilemma |
|-------------------|-------------|----------|-----------------|-------------------|
| Same template variables | Yes | Yes (FR-003) | Yes (FR-004) | Yes (FR-005) |
| Process Summary section | Yes | Yes | Yes | Yes |
| Trajectory tracking section | Dispute Trajectory | Risk Trajectory | Ranking Trajectory | Boundary Trajectory |
| Progression section | Convergence Progression | Defense Effectiveness Progression | Proposal Evolution | Cooperation Dynamics |
| Final state section | Final Recommendation Set | Final Risk Register | Final Ranking and Selection | Final Boundary Map |
| Remaining disputes section | Remaining Disputes | Disputed Risks | Remaining Disputes | Disputed Boundaries |
| Termination Assessment | Yes | Yes | Yes | Yes |
| Neutrality rule | Yes | Yes | Yes | Yes |
| Trace-everything rule | Yes | Yes | Yes | Yes |
| No-new-ideas rule | Yes | Yes | Yes | Yes |
| Write-the-file rule | Yes | Yes | Yes | Yes |

The mode-specific sections adapt the content framing (risks vs. rankings vs. boundaries) while preserving the structural invariants (process summary, trajectory, final state, disputes, termination assessment). This is the correct adaptation strategy -- different games produce different artifacts, but the meta-structure of "track evolution across rounds" is universal.

### Evidence 2: Arbitration Templates Follow the Cooperative Pattern

All three un-drafted arbitration templates follow the cooperative template's structure:

| Element | Cooperative | Red-Blue | Winner-Take-All | Prisoners-Dilemma |
|---------|-------------|----------|-----------------|-------------------|
| Subject-as-arbiter framing | Yes | Yes | Yes | Yes |
| Grounding citation required | Yes | Yes | Yes | Yes |
| Scope limited to disputes | Yes | Yes | Yes | Yes |
| No new recommendations | Yes | Yes | Yes | Yes |
| Same template variables | Yes | Yes | Yes | Yes |
| Write-the-file constraint | Yes | Yes | Yes | Yes |
| Confidence Assessment | Yes | Yes | Yes | Yes |

The domain-specific adaptations are appropriate:

- Red-blue: "Binding Risk Decisions" instead of "Binding Decisions"; risk-specific ruling options (Accept Red's assessment, Accept Blue's defense, Reclassify, Accept with monitoring); Updated Risk Register output.
- Winner-take-all: "Verdict Review" section assessing the Phase 5 judge's decision; override-requires-strong-grounding constraint; ADR update requirement.
- Prisoners-dilemma: Boundary-specific ruling format (owner, scope, handoff); trust scores as tiebreaker input; Revised Responsibility Map output.

### Evidence 3: Game Theory Grounding

Each mode's multi-round behavior maps to established game theory:

- **Red-blue rounds** = iterated attack-defense games (standard in penetration testing). The spec cites this at L63-68.
- **Winner-take-all rounds** = iterated elimination tournaments. The spec cites this at L69-76.
- **Prisoners-dilemma rounds** = iterated prisoner's dilemma, one of the most studied structures in game theory. The spec cites this at L77-83, noting that the iterated version is "fundamentally different from the single-shot version because agents can build reputation and retaliate."

The stagnation detection criteria are mode-appropriate:

- Red-blue stagnation = no new risks identified (attack surface exhausted). This is meaningful -- a red team that cannot find new vulnerabilities has completed its assessment.
- Winner-take-all stagnation = rankings stabilize. This is meaningful -- when the same proposal wins in consecutive rounds with no movement, further rounds are unproductive.
- Prisoners-dilemma stagnation = boundary disputes stop moving. This is meaningful -- when the same disputed boundaries persist unchanged across rounds, positions have calcified.

### Evidence 4: No New Parsing Logic Required

The Dispute-Parsing Subsystem (SKILL.md L656-683) already defined mode-specific fallback headings for all four modes before spec 004. The subsystem was designed with forward compatibility -- the heading entries for `red-blue`, `winner-take-all`, and `prisoners-dilemma` were present but dormant (never exercised because the validation rules prevented non-cooperative multi-round runs).

This means stagnation detection and Phase 6 trigger evaluation for the new modes use the same parsing code path that has been tested with cooperative mode. The only difference is which heading string is matched, and those strings were already defined.

### Evidence 5: Template Variable Completeness

The cross-round synthesis templates use the same variable set as the cooperative template: `{ROUND_SYNTHESES}`, `{ROUNDS_COMPLETED}`, `{MAX_ROUNDS}`, `{TERMINATION_REASON}`, `{MODE}`, `{TARGET_FILES}`, `{TARGET_PATH}`, `{AGENT_NAMES}`, `{OUTPUT_PATH}` (spec.md L113). These variables are populated by the cross-round synthesis dispatch code at SKILL.md L510-519, which is mode-agnostic. No new variables are needed.

The arbitration templates use the same variable set as the cooperative template: `{ARBITER_NAME}`, `{ARBITER_PROMPT}`, `{ARBITER_DOCS}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`, `{ALL_DISPUTES}`, `{TARGET_FILES}`, `{TARGET_PATH}`, `{AGENT_NAMES}`, `{MODE}`, `{OUTPUT_PATH}`, `{TRIGGER}`, `{REMAINING_DISPUTES}` (spec.md L144). These variables are populated by the Phase 6 dispatch code at SKILL.md L557-569, which is mode-agnostic. No new variables are needed.

---

## Acknowledged Limitations

### Limitation 1: Spec FR-009 Heading Mismatch

The spec's FR-009 (spec.md L173-178) specifies different Phase 6 required headings than what was implemented in SKILL.md (L587-592). For example:

- Spec FR-009 red-blue: "Process Note, Risk Framework, Binding Risk Decisions, Residual Risk Summary"
- SKILL.md implementation: "Process Note, Decision Framework, Binding Decisions, Updated Risk Register"

The implementation chose to align the validation headings with the actual template headings rather than the spec's theoretical headings. This is the correct decision -- the validation must match what the templates instruct agents to produce. However, it means the spec document itself is now out of sync with the implementation. The spec should be updated to reflect the actual headings, or the discrepancy should be documented.

### Limitation 2: No Integration Tests for Non-Cooperative Rounds

The success criteria (spec.md L188-193) define what a passing run looks like for each mode, but no automated test harness exists. Conversus is an LLM-orchestrated system, and its "tests" are actual multi-agent runs. The success criteria are verifiable by running the described configurations and inspecting outputs, but this is a manual process.

This is a known limitation of the conversus architecture, not specific to spec 004. The cooperative mode's rounds and arbitration features also lack automated tests. Addressing this limitation is a cross-cutting concern for the entire conversus project.

### Limitation 3: Template Quality Is Untested at Scale

The new cross-round synthesis templates are prompt engineering artifacts. Their effectiveness depends on LLM interpretation at runtime. The templates follow the cooperative template's structure and rules, which provides structural confidence, but the mode-specific content (risk trajectory tracking for red-blue, ranking trajectory for winner-take-all, cooperation dynamics for prisoners-dilemma) has not been validated through actual multi-round runs.

This is an inherent risk of prompt-based systems: the templates are instructions to an LLM, not deterministic code. However, the structural safeguards (required sections, neutrality rules, trace-everything rules, write-the-file rules) constrain the output space significantly, reducing the risk of completely off-target outputs.

### Limitation 4: Cross-Round Synthesis Heading Conventions Vary

The dispute headings in the cross-round synthesis templates are not perfectly uniform:

- Red-blue uses `### Disputed Risks` (L114 of the template)
- Winner-take-all uses `### Remaining Disputes` (L95 of the template)
- Prisoners-dilemma uses `## Disputed Boundaries` (L101 of the template -- different heading level)

The Dispute-Parsing Subsystem handles this variation through its mode-specific heading lookups (SKILL.md L674-677), and heading matching is level-insensitive (SKILL.md L681). However, the heading-level inconsistency (prisoners-dilemma uses `##` while others use `###`) could be a source of confusion for template maintainers. This is a minor cosmetic issue, not a functional one.

### Limitation 5: Winner-Take-All Stagnation Detection Is Indirect

The spec (L74) defines winner-take-all stagnation as "Rankings stabilize -- the same proposal wins in consecutive rounds with no movement." The Dispute-Parsing Subsystem detects this by checking `## Runner-Up` presence (SKILL.md L675), which is an indirect proxy. The presence of a runner-up heading indicates a contested decision, but it does not directly measure ranking stability across rounds.

This is a pragmatic design choice. The subsystem counts disputes using headings in the synthesis output, and it cannot perform cross-round comparison of rankings. The stagnation detection in winner-take-all mode is therefore less precise than in other modes. A more sophisticated approach would track the winner identity across rounds, but this would require engine changes that spec 004 deliberately avoids. The current approach is conservative -- it may miss stagnation in some cases (leading to extra rounds) but will not falsely declare stagnation.

---

## Conclusion

Spec 004 is a clean, minimal extension that validates conversus's template-first architecture. The engine was already mode-agnostic; the mode restrictions were scope gates, not architectural boundaries. Removing them and providing mode-specific templates is the correct and complete change.

The acknowledged limitations are real but proportionate: heading mismatches between spec and implementation should be reconciled, integration testing remains a project-wide gap, and template quality is inherently difficult to validate before runtime. None of these limitations represent correctness or safety risks -- they are documentation and testing debts that apply equally to the existing cooperative-mode features.

The strongest evidence for spec 004's correctness is what it did NOT change: the round loop, the stagnation detection algorithm, the Phase 6 trigger evaluation, the template variable population, and the entire cooperative mode pathway. The changes are additive (new templates, new validation table rows) and subtractive (removed guards, removed draft markers). There are no modifications to existing logic paths.
