# Cross-Review: functional-typing on integration-architect's Review

**Spec**: 008-interests-mode
**Reviewed document**: `conversus-review/integration-architect/review.md`
**Cross-reviewer**: functional-typing
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. The `ambiguous` row: integration-architect marks FR-007 "Satisfied" while the spec explicitly requires a fifth row

integration-architect's review states FR-007 is "**Satisfied.**" (review line 63) and maps all four SKILL.md decision matrix rows (lines 1138-1143) against the spec without noting the missing `ambiguous` row. The FR-to-Implementation Mapping section treats the four-row matrix as complete coverage of spec lines 44-52.

My review identifies this as a structural gap: the spec decision matrix (spec.md line 52) defines `| ambiguous | cooperative | Low -- present alternatives |` as a concrete fifth row. SKILL.md replaces it with heuristic detection (line 1145: "When the problem type is unset or ambiguous, use heuristic mode detection") which routes to signal-based inference (lines 1147-1156) and mixed-signal handling (lines 1158-1176). The heuristic path can recommend any mode depending on signal density -- it does NOT guarantee the spec's default of `cooperative` at Low confidence. If no signals are detected, SKILL.md asks the user to choose between two options rather than defaulting.

This is a dangerous contradiction because integration-architect's "Satisfied" verdict could be taken as clearance to ship, while the spec's `ambiguous` fallback guarantee is not preserved. A user with a genuinely ambiguous problem type and no detectable signals would hit the mixed-signal handler rather than receiving the spec's prescribed `cooperative` default. integration-architect's review acknowledges heuristic detection in the Dispatch Table section (review line 147-151) and under Missed Opportunity #3 (review lines 186-188) but never connects these observations back to the FR-007 verdict to downgrade it.

**My position**: FR-007 is partially covered, not fully satisfied. The four concrete rows are correct; the fifth row is functionally replaced, not implemented. This must be resolved before shipping -- either SKILL.md adds a fallback default after heuristic scoring yields no winner, or the spec removes the `ambiguous` row and defers to heuristic detection.

### 2. integration-architect declares "No off-base assumptions" while the `Preset` field in `interests.md` schema is a spec extension

integration-architect's review states "None identified" under Off-Base Assumptions (review line 193) and asserts the implementation "faithfully reflects the spec's scope, constraints, and design intent." However, SKILL.md line 1041 adds a `Preset` field to the `interests.md` schema (`- **Preset**: <category/preset-name>  <!-- only if a preset was used -->`) that does not appear in the spec's schema (spec.md lines 72-87). The spec schema defines: Perspective, Prompt, Docs, and Role. No Preset field.

integration-architect's review does reference the Preset field approvingly in the FR-006 mapping (review line 59: "Lines 1041 and 1052 define the `Preset` field in the interests.md schema") and in the schema alignment table (review line 169: "`agents[].preset` | `agents[].preset` | Exact match -- line 1260"), but never flags that this field is absent from the spec's interests.md schema definition. This is not a runtime-breaking issue, but it IS specification drift. The claim of zero off-base assumptions is too strong when the implementation's output schema is a strict superset of what the spec defines.

My review flags this under Missed Opportunities #2 (my review lines 176-185) and recommends updating the spec schema to include the optional Preset field, since FR-006 mandates preset integration but the schema block was not updated to reflect it. integration-architect's framing that the implementation has no off-base assumptions obscures this gap.

---

## Tensions

### 1. Preset existence validation: integration-architect raises it, my review does not

integration-architect's R-1 recommendation (review lines 206-207) identifies that preset-backed agents in generated `conversus.yml` depend on the preset file existing at run time, and the post-write validation (SKILL.md lines 1263-1273) checks for `name` and `prompt` (or `preset`) but does not resolve the preset to verify it exists on disk. integration-architect recommends adding preset existence validation to the post-write check.

My review does not raise this concern. I focused on the schema-level divergence (the Preset field existing in SKILL.md but not the spec) rather than the runtime resolution question. integration-architect's concern is valid and complementary -- it addresses a different layer of the same feature. The post-write validation at SKILL.md line 1269 ("Each agent has `name` and `prompt` (or `preset`)") treats `preset` as a valid alternative to `prompt`, but validation rule 7 at line 1271 ("If `docs` paths are specified, they exist on disk") shows the pattern of checking path existence -- the same pattern should logically extend to preset paths.

**Assessment**: integration-architect's recommendation is well-founded. This is a gap I missed. No contradiction between our reviews, but a productive tension where integration-architect's runtime focus catches what my schema-level focus does not.

### 2. `--output` flag as undocumented extension: different framing, same observation

My review notes the `--output` flag (SKILL.md lines 949, 1130) as a minor off-base assumption (my review line 209-211): "The spec does not mention an `--output` flag for either command. SKILL.md adds it as a practical convenience." I classify it as reasonable but undocumented.

integration-architect's review does not flag `--output` at all. The `--context` asymmetry is raised instead (review lines 177-179): "The interests handler reads `problem.md` from the output directory but does not support a `--context` flag to ingest additional docs during interest generation." This implies acceptance of `--output` while flagging the absence of `--context`.

The tension is minor: we agree the spec is silent on CLI flags beyond `--add` and `--mode`, but disagree on which undocumented flag deserves attention. Both observations are valid. The spec should either formalize both flags or explicitly scope the supported options.

### 3. `[CLARIFY: ...]` tag in Type field: my review raises it, integration-architect does not

My review's Missed Opportunity #4 (my review lines 196-199) notes that the Define handler (SKILL.md line 845) can mark a Type field as ambiguous via `[CLARIFY: ...]` tags, but the Interests handler's calibration table (lines 957-962) only lists four concrete types with no instruction for handling a CLARIFY-tagged Type. I recommend adding explicit behavior for this case.

integration-architect's review does not address the CLARIFY tag interaction at all. The prerequisite routing section (review lines 142-146) notes that the interests handler validates problem.md headings but does not examine what happens when values within those headings contain qualification tags.

This is a tension because the CLARIFY tag creates a real operational ambiguity: the interests handler needs a problem type to select calibration style, and a CLARIFY-tagged type does not cleanly map to any of the four rows. integration-architect's dispatch and routing analysis is thorough but stops at structural presence rather than examining value-level edge cases.

### 4. Staleness warning text alignment: different priority levels

My review flags the staleness warning text mismatch as P2 (my review line 229): the spec says "interests.md changed." while SKILL.md says "interests.md has changed since conversus.yml was last generated." integration-architect's review notes the same feature at review line 93-95 and marks it as satisfying FR-013, citing the SKILL.md text. Neither review treats this as a real problem, but we frame it differently -- I call for text alignment for traceability, while integration-architect implicitly accepts the rewording as equivalent. This is a cosmetic tension, not substantive.

### 5. draft/ready status parity: integration-architect raises it, my review does not

integration-architect's Missed Opportunity #2 (review lines 182-183) observes that the define handler annotates `problem.md` with `status: draft | ready` based on `[CLARIFY:]` tags, but the interests handler produces no equivalent status on `interests.md`, even though `[NEEDS DOCS:]` tags serve a similar "not fully ready" role. integration-architect suggests parity would enable downstream readiness checks.

My review does not raise this observation. It is a reasonable extension that would pair well with the CLARIFY tag handling I flag -- both address the question of "how does the system represent partial readiness across artifacts?" The tension is constructive: together, these observations suggest the guided workflow lacks a consistent readiness model across its artifact chain (problem.md -> interests.md -> conversus.yml).

---

## Safe Agreements

### 1. All 13 functional requirements have corresponding handler sections

Both reviews independently verify that FR-001 through FR-013 each have a traceable implementation in SKILL.md. integration-architect maps each FR to specific SKILL.md lines (review lines 19-95). My review performs the same mapping (my review lines 17-164). Neither review finds a functional requirement with zero implementation coverage. The only disagreement is on the completeness of FR-007 (the `ambiguous` row, discussed above under Dangerous Contradictions).

### 2. All five success criteria are achievable

Both reviews verify SC-001 through SC-005. integration-architect's SC analysis (review lines 100-121) and my review's alignment checks reach the same conclusions. SC-005 (missing problem.md routes to define) is confirmed at SKILL.md lines 934-939 by both reviews.

### 3. The generated conversus.yml schema is aligned with the run engine schema

integration-architect provides a detailed field-by-field alignment table (review lines 157-171) mapping generated fields to run engine fields. My review confirms the same alignment at review lines 128-134. Both reviews agree that the generated config uses no schema extensions and that intentionally omitted fields (rounds, stagnation, validate_templates, prior, arbiter) are correctly left for manual addition.

### 4. Prerequisite routing is correct and covers all permutations

Both reviews confirm the interests handler's prerequisite check (SKILL.md lines 933-941) and the mode handler's three-case prerequisite routing (SKILL.md lines 1099-1115). integration-architect maps all three mode handler cases explicitly (review lines 147-151). My review confirms the same at review lines 187-193 and notes the three-case dispatch as a positive addition beyond what the spec explicitly requires.

### 5. The three spec constraints are honored

Both reviews verify:
- No game theory terminology in user-facing conversation (SKILL.md line 1176). integration-architect cites this at review line 195; my review confirms at review lines 103-104, 113.
- No agents generated without user confirmation (SKILL.md lines 1020, 1210). integration-architect at review line 197; my review at review lines 74-76.
- No hard-coded agents or doc paths (SKILL.md line 966). integration-architect at review line 199; my review at review lines 24-25.

### 6. Post-write validation applies run engine rules to generated output

Both reviews agree that the post-write validation for conversus.yml (SKILL.md lines 1263-1273) applies the same rules as Run: Execution Step 1. integration-architect notes this at review lines 83-85 and provides the full validation rule list. My review confirms at review lines 140-143.

### 7. Existing file checks prevent silent overwrites

Both reviews verify that both handlers (interests at SKILL.md lines 996-1004, mode at lines 1214-1227) require user confirmation before overwriting existing artifacts. integration-architect at review lines 49-54 and 87-91; my review at review lines 70-76 and 148-154.

### 8. The `--add` flag supports multi-add and follows calibration rules

Both reviews confirm FR-003 implementation: `--add` can be repeated (SKILL.md line 948), and added interests follow the same calibration rules with follow-up questions for perspective and docs (SKILL.md lines 968-970). integration-architect at review lines 37-41; my review at review lines 46-54.

### 9. Agent name validation pattern is consistent across handlers

Both reviews note the `[a-z0-9][a-z0-9-_]*` pattern appears in the interests handler (line 964), mode handler post-write validation (line 1268), and run engine (line 198). integration-architect raises this as R-3 (review line 213-215) noting the maintenance risk of triple specification. My review does not flag this independently but confirms the pattern's presence in each location.
