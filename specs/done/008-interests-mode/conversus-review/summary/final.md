# Cross-Round Synthesis: Spec 008 — Interest Discovery & Mode Selection

**Deliberation type**: Cooperative
**Agents**: functional-typing, integration-architect, devils-advocate
**Target**: `conversus/specs/008-interests-mode/spec.md` and `conversus/SKILL.md` (interest and mode handlers)
**Rounds completed**: 2 of 2
**Termination reason**: max_rounds
**Date**: 2026-03-22

---

## Process Summary

Three agents conducted a two-round cooperative review of spec 008 (Interest Discovery & Mode Selection) and its SKILL.md implementation, covering the `/conversus interests` and `/conversus mode` subcommand handlers. Each round comprised four phases: initial review, cross-review, revision, and disputes. An advisory arbitration by the conversus-constitution arbiter occurred between rounds.

**Round 1** produced independent reviews that confirmed all 13 functional requirements (FR-001 through FR-013) have traceable counterparts in the SKILL.md handlers and all 5 success criteria (SC-001 through SC-005) are achievable. No blocking defects were found at any phase. Six dangerous contradictions were identified during cross-review — all resolved by Phase 3 revisions. Eight convergence points (C-1 through C-8, plus C-9 and C-10) were established unanimously. Three disputes remained, all concerning language, framing, or mechanism choice rather than architecture: (1) CLARIFY-tag handling mechanism in the interests handler, (2) `--output` flag documentation framing, and (3) generated config completeness framing. The Round 1 synthesis proposed resolutions for all three disputes.

**Arbitration** (between rounds): The conversus-constitution arbiter issued advisory opinions on all three disputes. All three opinions aligned with the Round 1 synthesis recommendations, grounding each in explicit spec constraints: the User Confirmation Gate and Domain Agnosticism constraints eliminate the `integration` default for CLARIFY-tagged types; the Artifact Co-location invariant makes "dual semantics" a mischaracterization of `--output`; and Schema Completeness via Defaults proves the generated config is complete, not a "starter template." The arbiter's considerations for Round 2 emphasized that the interests handler and mode handler have different input spaces (calibration style vs. mode selection), that the define handler's deferred-resolution design is intentional, and that all three disputes concern language rather than architecture.

**Round 2** resolved all three Round 1 disputes and established ten additional convergence points (RC-1 through RC-10). Four new dangerous contradictions were identified and resolved: (1) integration-architect's parenthetical type labels violated the No Game Theory Knowledge constraint, (2) integration-architect's standalone naming-pattern mapping table collapsed multi-signal inference into single-dimension lookup, (3) functional-typing's interest count relaxation had no enforcement mechanism, and (4) devils-advocate's hard stop for the CLARIFY-tag third exit state contradicted the arbiter's "recommend, do not require" resolution. Three new narrow disputes emerged in Round 2 — two were resolved by the synthesis through 2-to-1 alignment (interest count threshold at 5; cost estimate priority at P2), and the third (K-2 third exit state mechanism) was resolved through synthesis combining the deferred-resolution design intent with a concrete definition of generic calibration.

Across both rounds, twelve concessions were made by the three reviewers in Round 1 (functional-typing: 4, integration-architect: 4, devils-advocate: 4-5) and twelve in Round 2 (functional-typing: 4, integration-architect: 5, devils-advocate: 3). No concession from Round 1 was reversed in Round 2.

---

## Dispute Trajectory

### Dispute 1: CLARIFY-tag handling mechanism

**Round 1 state**: Three-way split. Functional-typing: inline user confirmation with `integration` as neutral default. Integration-architect: user confirmation but route back to `/conversus define` if user cannot choose; no silent default. Devils-advocate: treat as ambiguous and route through heuristic detection (does not address calibration-style selection). All agreed: do not silently extract the best-guess type; present ambiguity to user; allow workflow to proceed on user choice.

**Arbitration input**: Arbiter eliminated functional-typing's `integration` default on Domain Agnosticism grounds (privileging one type violates the constraint). Arbiter supported "recommend, do not require" over hard routing back to `/conversus define`, citing the define handler's deferred-resolution design (SKILL.md line 889). Recommended inline user confirmation with recommend-not-require fallback.

**Round 2 state**: All three reviewers accepted the synthesis + arbiter resolution. Dispute narrowed to the terminal fallback (third exit state): functional-typing proposed a double-declination stop; devils-advocate and integration-architect proposed user-confirmed degraded mode. Integration-architect added the crucial reservation that "generic calibration" must be concretely defined to be implementable.

**Final resolution**: Adopted user-confirmed degraded mode with a concrete definition of generic calibration. Generic calibration uses neutral Perspective formulations ("This interest represents [name]'s position on the problem") and factual-inquiry Prompt formulations ("Articulate [name]'s position, priorities, and constraints regarding the problem statement"). The handler warns that generic prompts produce weaker deliberation. The user's confirmation is informed consent. This resolves the tension between the define handler's deferred-resolution promise and the interests handler's structural need for a calibration style.

### Dispute 2: `--output` flag framing

**Round 1 state**: Functional-typing: "dual semantics" framing (write-path flag with read-path side effect). Integration-architect: "workspace override" framing (single directory invariant, not an accident). Devils-advocate: initially suggested flag split, then implicitly accepted document-only approach. All agreed: document the behavior, do not split the flag.

**Arbitration input**: Arbiter endorsed workspace-override framing. "Dual semantics" is a mischaracterization analogous to calling `cd` a command with dual semantics. The Artifact Co-location invariant means the behavior is unified, not dual.

**Round 2 state**: Resolved unanimously. All three reviewers adopted the workspace-override framing. Functional-typing withdrew D-3 (flag rename) as a formal deferred item since the system has no shipped CLI.

### Dispute 3: Generated config completeness framing

**Round 1 state**: Devils-advocate: "starter template" framing (acknowledging advanced features require manual YAML). Functional-typing and integration-architect: "complete config with extensions" framing (config is valid and runs without modification). All agreed a note about advanced fields should appear in the mode handler's output.

**Arbitration input**: Arbiter ruled "starter template" factually inaccurate. Schema Completeness via Defaults means a config with omitted optional fields is functionally identical to one with all defaults set. The Guided Workflow Promise is fulfilled: the generated config runs without YAML knowledge.

**Round 2 state**: Resolved with 3-to-0 alignment. "Complete config with extensions" framing adopted. Extension-points note specifies: "For multi-round deliberation, stagnation detection, prior context, or subject arbitration, add the corresponding fields to conversus.yml manually."

### New Round 2 disputes (all resolved)

**Interest count threshold**: 2-to-1 alignment at 5, matching the spec's stated "2-5" range. Warning gate allows user override. Integration-architect preferred 7 but explicitly declined to contest further.

**Cost estimate priority**: 2-to-1 alignment at P2. The mechanism exists to inform decisions; presenting a formula when the system can compute the result violates the principle of insulating users from internal abstractions.

**K-2 third exit state**: Resolved through synthesis combining the deferred-resolution design intent with concrete generic calibration, as described above.

---

## Convergence Progression

### Round 1 convergence (10 items, all reaffirmed in Round 2)

| ID | Item | Action |
|---|---|---|
| C-1 | Ambiguous row -- update spec to reference heuristic detection | Replace spec line 52 with heuristic detection reference |
| C-2 | Preset field belongs in spec interests.md schema | Add optional Preset field to schema |
| C-3 | Preset existence validation at generation time | Add validation rule to mode handler post-write check |
| C-4 | Heuristic detection is advisory | Add advisory sentence to SKILL.md |
| C-5 | Draft status behavior -- warn and proceed | Add warning to interests handler prerequisite check |
| C-6 | Agent-launch cost estimate at mode confirmation | Display at mode confirmation, not interests confirmation |
| C-7 | Interest-vs-type cross-validation warning | Add validation step to mode handler |
| C-8 | Zero-signal edge case -- present all modes | Add explicit behavior to heuristic detection |
| C-9 | `interests.md` is architecturally necessary | No change; current design affirmed |
| C-10 | Staleness warning text is adequate | No change; SKILL.md wording is more precise |

### Round 2 convergence (10 items)

| ID | Item | Action |
|---|---|---|
| RC-1 | Interest count upper-bound enforcement direction | SKILL.md must enforce upper bound; cost estimate remains informational |
| RC-2 | Computed count replaces formula in user-facing display | Mode confirmation shows computed number, not N^2+N+1 |
| RC-3 | Cross-validation examines full interest structure | Replace "naming pattern" with "interest structure (names, perspectives, and prompts)" |
| RC-4 | Calibration style descriptions use plain language | No type names or mode names in parentheticals |
| RC-5 | `(none)` sentinel standardized to canonical form | Define handler output changed to `(none)` |
| RC-6 | Equal-probability assumption is consequential for K-6/K-7 | Corrected characterization; no new recommendation needed |
| RC-7 | State-model advisory relocated | Brief comment near subcommand dispatch table |
| RC-8 | D-3 (flag rename) withdrawn as formal deferred item | Deferred items list simplified to D-1 and D-2 |
| RC-9 | Devils-advocate's OBA-1 (arbiter critique) conceded | Arbiter's general observation was summary, not architectural omission |
| RC-10 | Devils-advocate's AR-4 (early cost note) withdrawn | C-6 cost estimate at mode confirmation remains sole placement |

### Convergence rate

- Round 1: 10 convergence points from 14 substantive items (71%). Three disputes carried forward.
- Round 2: 10 additional convergence points. All three Round 1 disputes resolved. Three new disputes emerged and were resolved by synthesis. Zero disputes carried forward.
- Total: 20 convergence points. Zero unresolved disputes at termination.

---

## Final Recommendation Set

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

Source: C-1. Unanimous across both rounds.

**S-2 (P1): Add optional Preset field to interests.md schema (spec lines 72-87)**

Add after the Docs field:
```
- **Preset**: <category/preset-name>  <!-- only if a preset was used -->
```

Source: C-2. Required by FR-006 data flow.

**S-3 (P1): Add Common Options section documenting `--output`**

Add a new section after FR-013:
```
### Common Options

Both `/conversus interests` and `/conversus mode` accept:

- `--output <dir>` -- Override the working directory for all artifact I/O. Both prerequisite files (`problem.md`, `interests.md`) and generated output will be read from and written to this directory. Default: current working directory.
```

Source: Round 1 Dispute 2 resolution. Integration-architect's workspace-override framing, adopted unanimously in Round 2.

**S-4 (P2): Rename or footnote the Confidence column in the decision matrix**

Either rename "Confidence" to "Default Strength" or add a footnote: "These mappings are structurally deterministic (each type maps to exactly one mode). Empirical validation of deliberation outcomes under these defaults has not been performed."

Source: C-11. Editorial choice between label and footnote.

**S-5 (P2): Acknowledge interest count upper bound as soft ceiling**

Add a clarifying note to FR-001 that the "2-5" range is enforced as a warning gate with user override, not as a hard architectural limit.

Source: RC-1; Dispute 2 synthesis resolution (Round 2).

### Changes to `conversus/SKILL.md`

**K-1 (P1): Add preset existence validation to mode handler post-write check (~line 1271)**

Add a validation rule: "If an agent uses `preset:`, resolve the preset path using the same resolution rules as Run: Execution Step 1. If the preset file does not exist, warn: 'Agent {name} references preset {preset} which cannot be resolved. The generated config may fail at run time.'"

Source: C-3. Unanimous across both rounds.

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

Source: Round 1 Dispute 1 synthesis + arbiter opinion, refined by Round 2 convergence (RC-4) and dispute resolution. Combines functional-typing's inline confirmation, integration-architect's no-silent-default principle, the arbiter's "recommend, do not require" grounding, and the user-confirmed degraded mode with integration-architect's concrete definition of generic calibration.

**K-3 (P1): Add draft status behavior to interests handler prerequisite check (~line 941)**

Add: "If `problem.md` has `status: draft`, warn: 'problem.md is marked as draft with {count} unresolved [CLARIFY:] tags. Interest generation will use the current content, but results may change after clarifications are resolved.' Proceed without blocking."

Source: C-5. Unanimous across both rounds.

**K-4 (P2): Add heuristic-is-advisory sentence (~line 1156)**

Add: "The heuristic recommendation is advisory and always subject to user confirmation before proceeding."

Source: C-4. Unanimous across both rounds.

**K-5 (P2): Replace cost formula with computed count at mode confirmation (~line 1203)**

Change the mode confirmation display to show a computed agent launch count rather than the formula. At mode confirmation time, the handler knows N, rounds=1, iterations=1, and arbiter=absent. Display:

> "This configuration will launch {computed_count} agents (all {count} agents cross-review all others, single iteration)."

Where `computed_count` = N^2 + N + 1, computed by the handler.

In the Important Notes section (SKILL.md lines 1304-1308), retain the formula with two explicit qualifications: (1) assumes all N agents cross-review all others, (2) assumes iterations=1.

Source: RC-2. Unanimous in Round 2.

**K-6 (P2): Revise interest-vs-type cross-validation to examine full interest structure**

Replace the K-6 text referencing "naming pattern" with: "Check whether the interest structure (names, perspectives, and prompts) is consistent with the stated problem type. Examine interest names for semantic signals (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles), Perspective sentences for type-consistent language, and Prompt content for calibration-consistent framing. If the full interest structure is inconsistent with the stated problem type, warn: 'Your interests suggest a {inferred-type} problem, but problem.md says {stated-type}. Consider re-running /conversus define to update the type, or proceed with the current type.' If interest names are semantically opaque (e.g., `alpha`, `beta`), fall back to perspective and prompt content for signals. Do not warn on opaque names alone. For signal guidance, reference the heuristic detection signal vocabulary (SKILL.md lines 1151-1154). This is a warning, not a block."

Source: C-7 refined by RC-3. Unanimous in Round 2.

**K-7 (P2): Add zero-signal edge case to heuristic detection (~line 1156)**

Add: "If no signals are detected for any mode, present all four modes with their plain-language descriptions and ask the user to choose. Do not default silently."

Source: C-8. Unanimous across both rounds.

**K-8 (P2): Add advanced fields note to mode handler report (~line 1290)**

Add: "For multi-round deliberation, stagnation detection, prior context, or subject arbitration, add the corresponding fields to conversus.yml manually. See the Run: Execution configuration reference for available options."

Source: Round 1 Dispute 3 resolution. Unanimous across both rounds.

**K-9 (P2): Add interest count upper-bound validation to post-write check (~line 1059)**

Change "At least 2 interests are defined" to: "At least 2 and at most 5 interests are defined. If more than 5 are present, warn: 'You have {count} interests. This configuration will launch approximately {computed_count} agents per round. Reduce to 5 or fewer, or confirm to proceed.' If the user confirms, proceed. If the user removes interests, re-validate."

Source: RC-1; Dispute 2 synthesis resolution (Round 2). Threshold of 5 per 2-to-1 alignment.

**K-10 (P2): Standardize `(none)` sentinel in define handler output (~line 891)**

Change the define handler's Source Documents sentinel from `(none -- no context documents provided)` to `(none)`. This makes the define handler's output match the mode handler's `(none)` check (SKILL.md line 1254) exactly, eliminating the substring-vs-exact-matching ambiguity.

Source: RC-5. Unanimous in Round 2.

**K-11 (P3): Add state-model advisory near subcommand dispatch table (~line 38)**

Add a brief comment: "Note for future subcommand specs: as additional subcommands (converge, arbitrate, gate) are specified, consider formalizing the artifact prerequisite chain as a shared state table rather than per-handler ad-hoc conditionals. The current design works for three handlers but may not scale cleanly to six or more."

Source: RC-7. Editorial note.

### Deferred items

**D-1 (P2): Sentinel formalization across future handlers**: The broader question of sentinel conventions (canonical forms, matching rules, case sensitivity) across all handlers should be addressed when additional subcommands are specified. The specific mismatch between the define and mode handlers is resolved by K-10, but the general question remains open.

**D-2 (P3): Interest deduplication/overlap detection**: When two interests have substantially overlapping perspectives, the interests handler could warn about correlated agents. This would reduce wasted agent launches in the N^2 cross-review phase. Uncontested but out of scope for spec 008.

---

## Resolution Attribution

Every recommendation traces to at least one of: unanimous convergence, synthesis dispute resolution, or 2-to-1 alignment.

| Recommendation | Resolution Mechanism | Key Contributors |
|---|---|---|
| S-1 (ambiguous row) | Unanimous convergence (C-1) | functional-typing identified gap; all three agreed spec should match SKILL.md |
| S-2 (Preset field) | Unanimous convergence (C-2) | functional-typing and integration-architect identified omission |
| S-3 (--output documentation) | Dispute 2 synthesis + Round 2 unanimity | integration-architect's workspace-override framing; arbiter grounding |
| S-4 (Confidence column) | Unanimous convergence (C-11) | devils-advocate identified issue; integration-architect proposed rename |
| S-5 (interest count soft ceiling) | Round 2 convergence (RC-1) + synthesis | functional-typing reversed after cross-review; 2-to-1 on threshold |
| K-1 (preset validation) | Unanimous convergence (C-3) | integration-architect escalated to High; all endorsed |
| K-2 (CLARIFY-tag handling) | Dispute 1 synthesis + arbiter + Round 2 resolution | All three contributed mechanism elements; arbiter eliminated defaults |
| K-3 (draft status) | Unanimous convergence (C-5) | devils-advocate identified gap; all endorsed warn-and-proceed |
| K-4 (heuristic-is-advisory) | Unanimous convergence (C-4) | devils-advocate proposed; all accepted after devil withdrew precision demand |
| K-5 (computed count) | Round 2 convergence (RC-2) | devils-advocate proposed; 2-to-1 on P2 priority |
| K-6 (full interest structure) | C-7 refined by RC-3 | devils-advocate proposed broader signal base; integration-architect withdrew table |
| K-7 (zero-signal handling) | Unanimous convergence (C-8) | functional-typing proposed; all endorsed |
| K-8 (extension-points note) | Dispute 3 synthesis + Round 2 unanimity | All agreed on note; 2-to-1 rejected "starter template" framing |
| K-9 (interest count gate) | RC-1 + synthesis | functional-typing reversed to enforcement; 2-to-1 on threshold of 5 |
| K-10 (sentinel standardization) | Round 2 convergence (RC-5) | functional-typing and integration-architect identified mismatch; all agreed on canonical form |
| K-11 (state-model advisory) | Round 2 convergence (RC-7) | integration-architect proposed; relocated per devils-advocate |

---

<!-- DISPUTES_BEGIN -->

## Remaining Disputes

No disputes remain. All disputes from both rounds have been resolved.

**Round 1 disputes resolved**:

1. **CLARIFY-tag handling mechanism** (Dispute 1): Resolved through synthesis combining functional-typing's inline confirmation, integration-architect's no-silent-default principle, and the arbiter's "recommend, do not require" grounding. The user-confirmed degraded mode with concrete generic calibration closes the Round 2 third-exit-state gap. See K-2 for the final specification.

2. **`--output` flag framing** (Dispute 2): Resolved unanimously in Round 2. Integration-architect's workspace-override framing adopted. See S-3 for the final specification.

3. **Generated config completeness framing** (Dispute 3): Resolved with 3-to-0 alignment in Round 2. "Complete config with extensions" framing adopted; "starter template" rejected as factually inaccurate. See K-8 for the final specification.

**Round 2 disputes resolved**:

4. **K-2 third exit state** (Dispute 1, Round 2): Resolved through synthesis. User-confirmed degraded mode with concrete generic calibration definition adopted. Functional-typing's double-declination stop rejected as quantitatively but not qualitatively different from a hard requirement. See K-2 for the final specification.

5. **Interest count upper-bound threshold** (Dispute 2, Round 2): Resolved at 5 per 2-to-1 alignment (functional-typing + devils-advocate). Integration-architect's preference for 7 noted but not contested. See K-9 for the final specification.

6. **Cost estimate priority** (Dispute 3, Round 2): Resolved at P2 per 2-to-1 alignment (functional-typing + integration-architect). Devils-advocate's P3 position noted. See K-5 for the final specification.

<!-- DISPUTES_END -->

---

## Termination Assessment

**Termination reason**: max_rounds (2 of 2 completed).

**Convergence quality**: Excellent. All 20 convergence points are unanimous. All 6 disputes (3 from Round 1, 3 from Round 2) are resolved — three through synthesis, two through 2-to-1 alignment, one through unanimous Round 2 adoption. Zero disputes remain at termination. The deliberation achieved full closure naturally; additional rounds would not have produced meaningful refinement.

**Systemic findings**: Two cross-cutting patterns emerged that inform future spec development:

1. **Spec-as-draft, implementation-as-refinement**: In every case where the spec and SKILL.md disagreed (ambiguous row, interest count range, `(none)` sentinel, Preset field), all three reviewers concluded the SKILL.md was correct or the spec should be updated to match. The spec's primary debt is precision, not architecture. This pattern suggests spec authors should expect implementation to refine their abstractions and should welcome spec-update recommendations as a healthy sign, not as drift.

2. **Machine-authored artifacts vs. human-editable files**: The guided workflow assumes intermediate artifacts (`problem.md`, `interests.md`) are machine-authored with specific formats, sentinel values, and tag conventions, while simultaneously encouraging human editing. This tension surfaces in sentinel fragility, CLARIFY-tag handling, and draft status ambiguity. It is not blocking for spec 008 but will compound as more handlers consume these artifacts. D-1 (sentinel formalization) is the first step toward addressing this.

**Deliberation health indicators**:

- No blocking defects identified by any reviewer at any phase across two rounds.
- All 13 functional requirements have traceable implementations.
- All 5 success criteria are achievable.
- All 3 spec constraints (no game theory knowledge, no agents without confirmation, no hard-coded agents/paths) are honored.
- 24 concessions across both rounds (functional-typing: 8, integration-architect: 9, devils-advocate: 7-8), indicating genuine position evolution rather than entrenchment.
- Seven significant errors corrected during Round 2 cross-reviews alone, demonstrating the cross-review phase's value.
- The most significant finding — that the SKILL.md's heuristic detection is superior to the spec's static `cooperative` default — was reached independently by all three reviewers, a strong consensus signal.

**Final assessment**: The spec and SKILL.md are substantively sound and ready for implementation with the agreed changes. The deliverable is 5 spec changes (3 P1, 2 P2), 11 SKILL.md changes (3 P1, 7 P2, 1 P3), and 2 deferred items for future specs.
