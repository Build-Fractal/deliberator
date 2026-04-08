# Neutral Synthesis: Spec 008 — Interest Discovery & Mode Selection

**Deliberation type**: Cooperative
**Agents**: functional-typing, integration-architect, devils-advocate
**Target**: `conversus/specs/008-interests-mode/spec.md` and corresponding SKILL.md implementation (lines 926-1296)
**Date**: 2026-03-22

---

## Process Summary

Three agents reviewed spec 008 and its SKILL.md implementation across five phases:

**Phase 1 (Initial Reviews)**: All three reviewers independently confirmed that all 13 functional requirements (FR-001 through FR-013) have traceable counterparts in the SKILL.md handlers. All five success criteria (SC-001 through SC-005) were verified as achievable. No blocking defects were found. The primary findings were: (a) the spec's `ambiguous` row in the decision matrix is missing from SKILL.md (functional-typing), (b) the `Preset` field in the SKILL.md's `interests.md` schema is absent from the spec schema (functional-typing, integration-architect), (c) the decision matrix confidence labels are untested (devils-advocate), (d) heuristic mode detection is underspecified (devils-advocate, integration-architect), and (e) `interests.md` was challenged as a potentially unnecessary coupling artifact (devils-advocate).

**Phase 2 (Cross-Reviews)**: Cross-reviews produced six dangerous contradictions and sixteen tensions. The most productive exchanges were: (a) functional-typing identifying that integration-architect's "Satisfied" verdict on FR-007 was too strong given the missing `ambiguous` row, (b) integration-architect and functional-typing jointly rebutting devils-advocate's proposal to make `interests.md` optional by demonstrating prerequisite routing dependencies, user-modified interest structures, and machine-consumed fields, and (c) devils-advocate identifying the `--output` flag's dual read/write semantics as a footgun that functional-typing had classified as benign.

**Phase 3 (Revisions)**: All three reviewers revised their positions. Functional-typing demoted their P0 finding to P1 and reversed the fix direction (update the spec, not the SKILL.md). Devils-advocate withdrew the `interests.md`-as-optional recommendation and conceded that demanding formalized keyword scoring for heuristic detection was false precision. Integration-architect downgraded their FR-007 verdict from "Satisfied" to "Partially Satisfied" and escalated preset validation from Medium to High. Each reviewer adopted corrections from the others: functional-typing accepted devils-advocate's CLARIFY-tag insight; integration-architect accepted functional-typing's `ambiguous` row finding; devils-advocate accepted integration-architect's mechanism for interest-vs-type cross-validation.

**Phase 4 (Disputes)**: Eight items reached full convergence. Three genuine disputes remain, plus one minor framing disagreement. All disputes are about fix direction or language precision, not about the existence of gaps. No reviewer identified blocking defects at any phase.

---

## Recommendation Scorecard

| # | Item | Priority | Action Target | Status | Source |
|---|---|---|---|---|---|
| 1 | Ambiguous row divergence | P1 | Spec | Converged | functional-typing P0-1 (demoted), all three revisions |
| 2 | Preset field in interests.md schema | P1 | Spec | Converged | functional-typing P1-2, integration-architect revision |
| 3 | Preset existence validation at generation time | P1 | SKILL.md | Converged | integration-architect R-1, devils-advocate escalation, functional-typing N-1 |
| 4 | CLARIFY-tag handling in interests handler | P1 | SKILL.md | Disputed (mechanism) | functional-typing P1-3, devils-advocate rec 6, integration-architect N-1 |
| 5 | `--output` dual semantics documentation | P1 | Spec | Disputed (framing) | functional-typing P2-5 (escalated), devils-advocate cross-review |
| 6 | Draft status behavior for interests handler | P1 | SKILL.md | Converged | devils-advocate rec 6, integration-architect N-2 |
| 7 | Heuristic detection advisory sentence | P2 | SKILL.md | Converged | devils-advocate rec 2 (revised), functional-typing |
| 8 | Agent-launch cost estimate at mode confirmation | P2 | SKILL.md | Converged | devils-advocate rec 3 (revised), integration-architect N-3 |
| 9 | Interest-vs-type cross-validation warning | P2 | SKILL.md | Converged | devils-advocate rec 4 (revised), integration-architect mechanism |
| 10 | Zero-signal edge case handling | P2 | SKILL.md | Converged | functional-typing N-2, all three disputes |
| 11 | Confidence column rename/footnote | P2 | Spec | Converged (minor variation) | devils-advocate rec 1 (revised), integration-architect suggestion |
| 12 | Generated config completeness framing | P2 | Spec | Disputed | devils-advocate NR-3, functional-typing D-3, integration-architect D-3 |
| 13 | `(none)` sentinel formalization | P2 | SKILL.md | Partially converged | integration-architect R-2 (expanded), devils-advocate D-2 |
| 14 | Interest deduplication/overlap detection | P3 | Deferred | Noted, uncontested | devils-advocate missed opportunity 4, disputes D-3 |

---

## Dangerous Contradictions Found

Six dangerous contradictions were identified during cross-review. All were resolved or narrowed to manageable disputes by Phase 4.

### DC-1: FR-007 verdict disagreement (Phase 2)

**Contradiction**: integration-architect marked FR-007 "Satisfied" (integration-architect review, line 63). functional-typing marked it "Partially covered" (functional-typing review, lines 96-104). The spec's decision matrix (spec.md line 52) defines an `ambiguous` row defaulting to `cooperative` at Low confidence. SKILL.md replaces this with heuristic detection (line 1145) that can recommend any mode.

**Resolution**: integration-architect conceded in Phase 3 revision, downgrading to "Partially Satisfied." All three reviewers agreed the spec should be updated to match the SKILL.md's superior behavior. Converged.

### DC-2: `interests.md` as coupling artifact (Phase 2)

**Contradiction**: devils-advocate argued `interests.md` duplicates information in `conversus.yml` and proposed making it optional (devils-advocate review, lines 49-57). integration-architect and functional-typing identified concrete dependencies: prerequisite routing (SKILL.md lines 1099-1115), non-recoverable user edits (SKILL.md lines 996-1004), and machine-consumed Perspective field (SKILL.md lines 1203, 1286-1288).

**Resolution**: devils-advocate withdrew in Phase 3 revision, conceding all three architectural dependencies. Converged.

### DC-3: "No off-base assumptions" overclaim (Phase 2)

**Contradiction**: integration-architect declared "None identified" under off-base assumptions (integration-architect review, line 193). functional-typing identified the `Preset` field in `interests.md` schema (SKILL.md line 1041) as absent from the spec schema (spec.md lines 72-87), making the implementation schema a strict superset.

**Resolution**: integration-architect conceded in Phase 3 revision, acknowledging one assumption beyond the spec. All three reviewers agreed the Preset field is necessary and the spec should be updated. Converged.

### DC-4: Confidence label semantics (Phase 2)

**Contradiction**: devils-advocate called the decision matrix confidence labels "fabricated" (devils-advocate review, lines 29-37). functional-typing defended the four non-ambiguous mappings as structurally valid within the closed taxonomy (functional-typing cross-review of devils-advocate, lines 11-19). integration-architect proposed the word "confidence" is doing double duty between determinism and empirical accuracy.

**Resolution**: devils-advocate conceded the "fabricated" framing in Phase 3, accepting integration-architect's distinction. All three reviewers agreed the column should be renamed or footnoted. Converged on substance, minor variation on label choice.

### DC-5: Winner-take-all for integration problems (Phase 2)

**Contradiction**: devils-advocate suggested "some integration problems are zero-sum on specific dimensions, and winner-take-all would surface that reality better" (devils-advocate review, line 36). integration-architect demonstrated that winner-take-all's synthesis template produces `## Runner-Up` and single-verdict outcomes, which structurally violates integration problems' defining characteristic that all interests must survive (integration-architect cross-review of devils-advocate, lines 24-29).

**Resolution**: devils-advocate did not reiterate this position in Phase 3 or 4. The claim was silently dropped. integration-architect's rebuttal stands unchallenged.

### DC-6: functional-typing P0 fix direction (Phase 2)

**Contradiction**: functional-typing recommended adding a `cooperative` fallback to SKILL.md's heuristic detection (functional-typing review, lines 218-219). Both integration-architect and devils-advocate independently argued this would suppress the superior user-interactive behavior (integration-architect cross-review, Dangerous Contradictions #1; devils-advocate cross-review, Dangerous Contradictions #1).

**Resolution**: functional-typing conceded in Phase 3, demoting to P1 and reversing the fix direction (update spec, not SKILL.md). Converged.

---

## Systemic Contradictions

Two systemic contradictions emerged from the deliberation that cut across multiple findings.

### SC-1: Spec-as-authoritative vs. implementation-as-superior

The deliberation revealed a methodological tension between treating the spec as authoritative (functional-typing's approach: "Does the implementation match the spec?") and treating the spec as challengeable (devils-advocate's approach: "Should the spec require what it requires?"). This tension manifested in the `ambiguous` row finding (DC-1, DC-6), the confidence labels (DC-4), and the generated config completeness framing (Dispute 3).

**Impact**: In every case where the spec and SKILL.md disagreed, all three reviewers ultimately concluded the SKILL.md was correct. This suggests the spec was written at a higher level of abstraction than the implementation and the implementation made correct refinements. The systemic lesson: when the implementation is more sophisticated than the spec on a specific point, the spec should be updated to match, not the reverse.

**Trace**: functional-typing revision P0-1 ("The right resolution is a spec update, not an implementation change"); integration-architect revision FR-007 ("The spec should be amended to match the SKILL.md's more user-interactive behavior"); devils-advocate revision NR-1 ("The spec should catch up").

### SC-2: Machine-authored artifacts vs. human-editable files

The guided workflow assumes intermediate artifacts (`problem.md`, `interests.md`) are machine-authored by the define and interests handlers, with specific formats, sentinel values (`(none)`), and tag conventions (`[CLARIFY:]`, `[NEEDS DOCS:]`). Simultaneously, the spec encourages human editing of these artifacts (FR-005: add/remove/modify interests; define handler: review and refine problem.md). The tension between machine-readable structure and human-editable freeform text surfaces in the `(none)` sentinel fragility (integration-architect R-2, devils-advocate disputes D-2), the CLARIFY-tag handling gap (Dispute 1), and the draft status ambiguity.

**Impact**: Not a blocking issue for spec 008, but a design tension that will compound as more handlers consume these artifacts. The synthesis notes this for future spec consideration.

**Trace**: devils-advocate disputes D-2 ("the guided workflow assumes machine-authored intermediate files while also encouraging human editing"); integration-architect revision R-2 (expanded sentinel handling).

---

## Convergence Achieved

The following items reached full three-reviewer consensus by Phase 4. These are settled and require no further deliberation.

### C-1: Ambiguous row resolution — update the spec

All three reviewers unanimously agree: the spec's `ambiguous` row (spec.md line 52: `| ambiguous | cooperative | Low -- present alternatives |`) should be replaced with a reference to heuristic mode detection (SKILL.md lines 1147-1156) plus user choice via mixed-signal handling (SKILL.md lines 1158-1176). The SKILL.md behavior is superior to the spec's static default.

**Spec change**: Replace spec line 52 with: "When the problem type is ambiguous or unset, use heuristic mode detection (FR-008). If no mode has detectable signals, present the top candidates and ask the user to choose."

**Trace**: functional-typing revision P0-1; integration-architect revision FR-007; devils-advocate revision NR-1; all three disputes phase convergence sections.

### C-2: Preset field belongs in spec interests.md schema

All three reviewers agree the spec's `interests.md` schema (spec.md lines 72-87) should include the optional `Preset` field (`- **Preset**: <category/preset-name>  <!-- only if a preset was used -->`). This is a spec omission required by FR-006's data-flow from interests to config generation, not implementation drift.

**Spec change**: Add `- **Preset**: <category/preset-name>  <!-- only if a preset was used -->` to the interests.md schema block at spec.md ~line 87.

**Trace**: functional-typing revision P1-2; integration-architect revision "Original finding" section; devils-advocate implicit acceptance via withdrawal of interests.md-as-optional.

### C-3: Preset existence validation at generation time

All three reviewers agree: the mode handler's post-write validation (SKILL.md lines 1262-1273) should validate that `preset:` references resolve to existing preset files on disk. This follows the existing pattern of rule 7 (docs path existence at line 1271) and target path existence (line 1266). integration-architect escalated from Medium to High; devils-advocate endorsed the escalation.

**SKILL.md change**: Add to post-write validation (~line 1271): "If an agent uses `preset:`, resolve the preset path using the same resolution rules as Run: Execution Step 1. If the preset file does not exist, warn: 'Agent {name} references preset {preset} which cannot be resolved. The generated config may fail at run time.'"

**Trace**: integration-architect revision R-1 (escalated to High); functional-typing revision N-1; devils-advocate revision NR-2.

### C-4: Heuristic detection is advisory

All three reviewers agree the heuristic mode detection section (SKILL.md lines 1147-1156) should explicitly state that its output is advisory and subject to user confirmation. devils-advocate withdrew the demand for formalized keyword scoring, accepting that demanding precision from a classifier on freeform text is false precision. The fix is a single sentence.

**SKILL.md change**: Add to heuristic detection section (~line 1156): "The heuristic recommendation is advisory and always subject to user confirmation before proceeding."

**Trace**: devils-advocate revision rec 2 disposition; functional-typing cross-review of devils-advocate, tension 1; integration-architect cross-review of devils-advocate, tension 2.

### C-5: Draft status behavior — warn and proceed

All three reviewers independently identified this gap: spec 008 never defines behavior when `problem.md` has `status: draft` or unresolved `[CLARIFY:]` tags, despite the define handler explicitly deferring this decision to downstream specs (SKILL.md line 889). All converge on: warn the user, do not block.

**SKILL.md change**: Add to interests handler prerequisite check (~line 941): "If `problem.md` has `status: draft`, warn: 'problem.md is marked as draft with {count} unresolved [CLARIFY:] tags. Interest generation will use the current content, but results may change after clarifications are resolved.' Proceed without blocking."

**Trace**: devils-advocate review rec 6; integration-architect revision N-2; functional-typing revision P1-3 (implicitly, via CLARIFY-tag handling).

### C-6: Agent-launch cost estimate at mode confirmation

All three reviewers agree the launch cost estimate should be displayed at mode confirmation time (SKILL.md ~line 1203), not at interests confirmation time. At mode confirmation, both agent count and mode are known, making the estimate accurate. devils-advocate conceded the original placement was wrong.

**SKILL.md change**: Add to mode confirmation display (~line 1203): "Estimated agent launches per round: {N^2 + N + 1} (based on {count} agents in {mode} mode)."

**Trace**: devils-advocate revision rec 3 disposition; integration-architect revision N-3; functional-typing no objection.

### C-7: Interest-vs-type cross-validation warning

All three reviewers agree the mode handler should include a validation step comparing interest naming patterns against the stated problem type, warning if they diverge. integration-architect's mechanism (a separate validation step, not re-invocation of heuristic detection) was accepted by devils-advocate.

**SKILL.md change**: Add to mode handler (between reading inputs and running the decision matrix): "Check whether the interest structure's naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles) is consistent with the stated problem type. If inconsistent, warn: 'Your interests suggest a {inferred-type} problem, but problem.md says {stated-type}. Consider re-running /conversus define to update the type, or proceed with the current type.' This is a warning, not a block."

**Trace**: devils-advocate revision rec 4 disposition; integration-architect cross-review of devils-advocate, tension 4; devils-advocate disputes convergence 6.

### C-8: Zero-signal edge case handling

All three reviewers agree on behavior when heuristic detection finds no signals for any mode: present all four modes with their plain-language descriptions and ask the user to choose. Do not default silently. This closes the edge case created by removing the spec's `ambiguous` row.

**SKILL.md change**: Add to heuristic detection section (~line 1156): "If no signals are detected for any mode, present all four modes with their plain-language descriptions and ask the user to choose. Do not default silently."

**Trace**: functional-typing revision N-2; integration-architect disputes convergence 7; devils-advocate disputes convergence position 11.

### C-9: `interests.md` is architecturally necessary

devils-advocate withdrew the proposal to make `interests.md` optional, conceding three concrete dependencies: prerequisite routing (SKILL.md lines 1099-1115), non-recoverable user-edited interest structures (SKILL.md lines 996-1004), and machine-consumed Perspective field (SKILL.md lines 1203, 1286-1288).

**Action**: None. The current design is affirmed.

**Trace**: devils-advocate revision rec 5 disposition ("WITHDRAWN. ... I was wrong."); functional-typing cross-review of devils-advocate, dangerous contradictions 2; integration-architect cross-review of devils-advocate, dangerous contradictions 1.

### C-10: Staleness warning text is adequate

All three reviewers agree the SKILL.md wording ("interests.md has changed since conversus.yml was last generated") is semantically equivalent to the spec's ("interests.md changed") and is actually more precise. functional-typing withdrew P2-4.

**Action**: None. No text alignment needed.

**Trace**: functional-typing revision P2-4 ("WITHDRAWN"); integration-architect cross-review Safe Agreements 6.

---

<!-- DISPUTES_BEGIN -->

## Remaining Disputes

### Dispute 1: CLARIFY-tag handling mechanism

**What is agreed**: All three reviewers confirm the gap exists. The interests handler's Interest Generation table (SKILL.md lines 957-962) has four concrete type rows and no instruction for a `[CLARIFY: ...]`-tagged Type field. All agree silent best-guess extraction (functional-typing's original P1-3) is wrong -- the CLARIFY tag is an intentional ambiguity marker that should not be silently consumed.

**Where they diverge**:

- **functional-typing** (disputes D-1): Ask the user to confirm the type inline within the interests handler. Present the CLARIFY tag's context and offer the four calibration styles as explicit choices. If the user cannot decide, the interests handler should not pick a default -- but functional-typing's Phase 3 revision (P1-3 revised) proposed using `integration` as a "neutral default," which integration-architect disputes.

- **integration-architect** (disputes D-1): Route CLARIFY-tagged types through user confirmation (conceded from Phase 3 N-1 which prescribed extract-and-warn). However, explicitly rejects functional-typing's `integration` fallback default: "If the user cannot decide their problem type, the correct behavior is to route them back to `/conversus define` to resolve the CLARIFY tag, not to silently assign `integration`."

- **devils-advocate** (revision rec 6): Treat CLARIFY-tagged types as equivalent to "ambiguous" and route through heuristic detection. Allow the user to proceed if they choose, but use heuristic detection rather than the CLARIFY-tagged best-guess type for calibration. This position does not address the interests handler's specific need for a calibration style (since heuristic detection is a mode-selection mechanism, not a calibration-style selector).

**Neutral assessment**: The three-way dispute is narrower than it appears. All agree on: (a) do not silently extract the best-guess type, (b) present the ambiguity to the user, (c) allow the workflow to proceed if the user makes a choice. The genuine disagreement is over the fallback when the user cannot or will not choose: functional-typing proposes a default calibration style (`integration`); integration-architect proposes routing back to `/conversus define`; devils-advocate proposes heuristic detection (which does not directly answer the calibration-style question).

**Synthesis recommendation**: Combine functional-typing's inline confirmation (present the four calibration styles and ask the user to choose) with integration-architect's no-silent-default principle. If the user chooses a type, use it. If the user declines to choose, recommend running `/conversus define` to resolve the CLARIFY tag. Do not silently default to any calibration style. For the mode handler, route CLARIFY-tagged types through heuristic detection as all three agree.

### Dispute 2: `--output` flag framing

**What is agreed**: All three reviewers agree the `--output` flag's dual read/write semantics (SKILL.md line 949: "Also changes where `problem.md` is read from"; line 1130: "Also changes where `problem.md` and `interests.md` are read from") should be documented in the spec at P1 priority.

**Where they diverge**:

- **functional-typing** (disputes D-2): Frame `--output` as having "dual semantics" -- a write-path flag with a surprising read-path side effect. Document it but do not split the flag. The single-directory coherence principle justifies the current design.

- **integration-architect** (disputes D-2): Frame `--output` as a workspace directory override, not as a dual-semantics flag. The co-location of artifacts in a single directory is a design invariant. The documentation should explain it as `--workspace` in spirit, eliminating the "dual semantics" confusion without splitting the flag.

- **devils-advocate** (cross-review, not revised in disputes): Originally suggested considering split into `--output` (write) and `--input` (read) flags. Did not reiterate in Phase 3 or 4, implicitly accepting the document-only approach.

**Neutral assessment**: The disagreement is about explanatory framing, not about the action. All three agree: document the behavior, do not split the flag. integration-architect's "workspace override" framing is more accurate to the design intent and less likely to cause confusion than functional-typing's "dual semantics" framing.

**Synthesis recommendation**: Document `--output` in a spec Common Options section using integration-architect's workspace-override framing: "Override the working directory for all artifact I/O. Both prerequisite files (`problem.md`, `interests.md`) and generated output will be read from and written to this directory." This correctly represents the design invariant (artifact co-location) without implying a design accident.

### Dispute 3: Generated config completeness framing

**What is agreed**: The generated `conversus.yml` omits optional fields (`rounds`, `stagnation`, `validate_templates`, `prior`, `arbiter`). These fields have sensible defaults in the run engine. The generated config is valid input for `/conversus run`.

**Where they diverge**:

- **devils-advocate** (disputes D-1): The spec says the guided workflow eliminates "the need for users to understand game theory or YAML schemas" (spec line 19). If advanced features require manual YAML editing, the spec's promise has a boundary that should be stated. Recommends adding a sentence acknowledging generated configs are ready-to-run with single-round defaults, with advanced features requiring manual edits or future guided commands.

- **functional-typing** (disputes D-3): The spec's claim is accurate as stated. Generated configs ARE complete for a first run. Users who want multi-round deliberation are past the guided workflow and into advanced territory. This is a scope boundary, not a contradiction. Suggests adding a note to the mode handler's report pointing to advanced fields, but objects to "starter template" framing.

- **integration-architect** (disputes D-3): The generated config is complete, ready-to-run, and valid. Calling it a "starter template" sets incorrect expectations by implying it will not work until the user adds more fields. Advanced fields are extensions, not requirements. Proposes a mode report note: "Advanced options (rounds, stagnation, arbiter) can be added to conversus.yml manually."

**Neutral assessment**: The substance is agreed -- all three reviewers want a note about advanced fields somewhere in the mode handler's output. The dispute is purely about framing: "starter template" (devils-advocate) vs. "complete config with optional extensions" (functional-typing, integration-architect). The 2-to-1 alignment favors the "complete with extensions" framing, and it is objectively more accurate -- the config passes validation and runs successfully without modification.

**Synthesis recommendation**: Add a note to the mode handler's report (SKILL.md ~line 1290): "For multi-round deliberation, stagnation detection, prior context, or subject arbitration, add the corresponding fields to conversus.yml manually. See the Run: Execution configuration reference for available options." Do not frame the generated config as a "starter template." The config is complete and ready to run; the note surfaces extension points for power users.

<!-- DISPUTES_END -->

---

## Actionable Spec Changes

Organized by target document and priority. All changes trace to converged recommendations or synthesis dispute resolutions.

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

Source: Convergence C-1. All three reviewers.

**S-2 (P1): Add optional Preset field to interests.md schema (spec lines 72-87)**

Add after the Docs field:
```
- **Preset**: <category/preset-name>  <!-- only if a preset was used -->
```

Source: Convergence C-2. Spec omission required by FR-006 data flow.

**S-3 (P1): Add Common Options section documenting `--output`**

Add a new section (between Constraints and end of spec, or after FR-013):
```
### Common Options

Both `/conversus interests` and `/conversus mode` accept:

- `--output <dir>` -- Override the working directory for all artifact I/O. Both prerequisite files (`problem.md`, `interests.md`) and generated output will be read from and written to this directory. Default: current working directory.
```

Source: functional-typing P2-5 (escalated to P1); integration-architect workspace-override framing.

**S-4 (P2): Rename or footnote the Confidence column in the decision matrix**

Either rename "Confidence" to "Default Strength" or add a footnote: "These mappings are structurally deterministic (each type maps to exactly one mode). Empirical validation of deliberation outcomes under these defaults has not been performed."

Source: devils-advocate rec 1 (revised); integration-architect suggestion. Both agree on the substance; label choice is editorial.

### Changes to `SKILL.md`

**K-1 (P1): Add preset existence validation to mode handler post-write check (~line 1271)**

Add a validation rule: "If an agent uses `preset:`, resolve the preset path using the same resolution rules as Run: Execution Step 1. If the preset file does not exist, warn: 'Agent {name} references preset {preset} which cannot be resolved. The generated config may fail at run time.'"

Source: Convergence C-3. All three reviewers.

**K-2 (P1): Add CLARIFY-tag handling to interests handler Interest Generation (~line 955)**

Add: "If the Type field contains a `[CLARIFY: ...]` tag, treat the problem type as unresolved. Present the CLARIFY tag's content to the user and ask which calibration style to use: adversarial (selection), cooperative (integration), honesty-calibrated (scoping), or red/blue (stress-test). If the user declines to choose, recommend running `/conversus define` to resolve the CLARIFY tag before proceeding. Do not silently extract the best-guess type or default to any calibration style."

In the mode handler, route CLARIFY-tagged types through heuristic mode detection (existing behavior for ambiguous/unset types).

Source: Dispute 1 synthesis resolution. Combines functional-typing's inline confirmation with integration-architect's no-silent-default principle.

**K-3 (P1): Add draft status behavior to interests handler prerequisite check (~line 941)**

Add: "If `problem.md` has `status: draft`, warn: 'problem.md is marked as draft with {count} unresolved [CLARIFY:] tags. Interest generation will use the current content, but results may change after clarifications are resolved.' Proceed without blocking."

Source: Convergence C-5. All three reviewers.

**K-4 (P2): Add heuristic-is-advisory sentence (~line 1156)**

Add: "The heuristic recommendation is advisory and always subject to user confirmation before proceeding."

Source: Convergence C-4. All three reviewers.

**K-5 (P2): Add agent-launch cost estimate to mode confirmation (~line 1203)**

Add to confirmation display: "Estimated agent launches per round: {N^2 + N + 1} (based on {count} agents in {mode} mode)."

Source: Convergence C-6. All three reviewers.

**K-6 (P2): Add interest-vs-type cross-validation warning to mode handler**

Add between reading inputs and running the decision matrix: "Check whether the interest structure's naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles) is consistent with the stated problem type. If inconsistent, warn: 'Your interests suggest a {inferred-type} problem, but problem.md says {stated-type}. Consider re-running /conversus define to update the type, or proceed with the current type.' This is a warning, not a block."

Source: Convergence C-7. integration-architect's mechanism, accepted by devils-advocate.

**K-7 (P2): Add zero-signal edge case to heuristic detection (~line 1156)**

Add: "If no signals are detected for any mode, present all four modes with their plain-language descriptions and ask the user to choose. Do not default silently."

Source: Convergence C-8. All three reviewers.

**K-8 (P2): Add advanced fields note to mode handler report (~line 1290)**

Add: "For multi-round deliberation, stagnation detection, prior context, or subject arbitration, add the corresponding fields to conversus.yml manually. See the Run: Execution configuration reference for available options."

Source: Dispute 3 synthesis resolution. All three reviewers agree on surfacing extension points; "complete config with extensions" framing per 2-to-1 alignment.

### Deferred items (noted for future specs)

**D-1 (P2): `(none)` sentinel formalization**: integration-architect's expanded handling (`(none)`, empty list, missing section as equivalent) should be adopted for machine-authored files. The broader question of human-authored sentinel variants (case-insensitive matching, regex patterns) is deferred to a future spec addressing the machine-authored vs. human-editable artifact tension (Systemic Contradiction SC-2).

Source: integration-architect R-2 (expanded); devils-advocate disputes D-2.

**D-2 (P3): Interest deduplication/overlap detection**: When two interests have substantially overlapping perspectives, the interests handler could warn about correlated agents. This would reduce wasted agent launches in the N^2 cross-review phase. Uncontested but out of scope for spec 008.

Source: devils-advocate missed opportunity 4; devils-advocate disputes D-3.

---

## Key Concessions

Each concession listed below represents a position that an agent held, was challenged, and then explicitly abandoned. All concessions are traced to their source.

### functional-typing concessions

1. **P0 severity on ambiguous row was wrong.** Demoted to P1 and reversed the fix direction: update the spec to match the SKILL.md, not add a `cooperative` fallback to the SKILL.md. (functional-typing revision P0-1: "I was internally inconsistent: I recognized the SKILL.md behavior as superior, then recommended reverting to the inferior spec behavior for compliance purposes.")

2. **CLARIFY-tag extract-and-warn approach was wrong.** The define handler's `[CLARIFY:]` tag is an intentional ambiguity marker. Extracting the best-guess type undermines that signal. (functional-typing revision P1-3: "Devils-advocate makes a sharp point that I missed.")

3. **Staleness warning text alignment is cosmetic.** Withdrawn entirely. The SKILL.md wording is more precise. (functional-typing revision P2-4: "WITHDRAWN.")

4. **"Specification drift" framing for Preset field was wrong.** Accepted integration-architect's reframing as "spec omission." (functional-typing revision P1-2: "integration-architect is right on the framing.")

### integration-architect concessions

1. **FR-007 "Satisfied" verdict was too strong.** Downgraded to "Partially Satisfied." The spec's `ambiguous` row is not preserved in the SKILL.md. (integration-architect revision: "Downgraded to 'Partially Satisfied.' Functional-typing's challenge is valid.")

2. **"No off-base assumptions" was overconfident.** The `Preset` field in the interests.md schema IS an assumption beyond the spec text, even though it is the correct assumption. (integration-architect revision: "my original review's claim of zero off-base assumptions was itself overconfident.")

3. **Preset validation severity was understated.** Escalated from Medium to High. A config that passes validation but deterministically fails at run time is a validation gap, not an enhancement. (integration-architect revision R-1: "Escalated to High.")

4. **CLARIFY-tag extract-and-warn (N-1) was wrong.** Conceded in disputes that both other reviewers independently arrived at the treat-as-ambiguous approach. (integration-architect disputes D-1: "I concede that my N-1 recommendation is wrong.")

### devils-advocate concessions

1. **`interests.md` as optional artifact was wrong.** Three concrete architectural dependencies rebut the proposal: prerequisite routing, user-modified interest structures, machine-consumed fields. (devils-advocate revision rec 5: "WITHDRAWN. ... The separate file earns its keep. ... I was wrong.")

2. **Demanding formalized keyword scoring was false precision.** Weighted scores on freeform text would be equally arbitrary without empirical calibration. The advisory framing plus user confirmation is sufficient. (devils-advocate revision rec 2: "I concede this.")

3. **Agent-launch cost placement at interests confirmation was wrong.** Mode is not yet selected at that point; the cost formula depends on mode. (devils-advocate revision rec 3: "Both cross-reviewers correctly identify that my proposed placement is wrong.")

4. **"Fabricated" confidence labels overstated the problem.** The taxonomy is intentionally closed, and the mappings are deterministic by construction. The conflation of decision-matrix code paths with heuristic fallback code paths was a logical error. (devils-advocate revision rec 1: "I concede it.")

5. **Winner-take-all for integration problems misapplied mode semantics.** Silently dropped after integration-architect demonstrated the synthesis template incompatibility. (Not explicitly conceded, but never reiterated after Phase 2.)

---

## Summary

The spec and implementation are substantially sound. No blocking defects were identified by any reviewer at any phase. All 13 functional requirements have traceable implementations. All 5 success criteria are achievable. The three spec constraints (no game theory knowledge, no agents without confirmation, no hard-coded agents/paths) are honored.

The deliberation produced 4 P1 spec changes, 4 P1 SKILL.md changes, 4 P2 SKILL.md changes, 1 P2 spec change, and 2 deferred items. Eight convergence points were established unanimously. Three disputes were resolved through synthesis. The most significant finding is that the SKILL.md's ambiguous-type handling (heuristic detection + user choice) is superior to the spec's static `cooperative` default -- a rare case where all three reviewers independently concluded the implementation should inform the spec rather than the reverse.
