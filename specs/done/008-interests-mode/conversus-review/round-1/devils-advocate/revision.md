# Devil's Advocate — Revised Review (Phase 3)

**Spec**: `008-interests-mode`
**Role**: devils-advocate
**Date**: 2026-03-22

---

## Recommendation Dispositions

### Recommendation 1: Downgrade confidence labels from "High" to "Default"

**Original**: Downgrade all four decision matrix confidence labels from "High" to "Default," reserving "High" for empirically validated mappings.

**Disposition**: REVISED — concede the framing, retain the substance.

Both cross-reviewers challenged this recommendation on the same grounds: the taxonomy is intentionally closed (SKILL.md line 850), and the four mappings are deterministic by construction — one type maps to exactly one mode. Functional-typing correctly distinguishes between the decision matrix (fires when type IS set) and heuristic detection (fires when type is unset or ambiguous). These are disjoint code paths, not fallbacks for the same condition. My original argument — "if the mapping is truly high-confidence, why does the spec need heuristic detection at all?" — conflated these two paths. That was a logical error and I concede it.

However, integration-architect concedes my underlying point: the word "confidence" is doing double duty. The mapping is deterministic (given a type, the mode is unambiguous), but whether that deterministic mapping produces good deliberations is untested. Integration-architect's proposed resolution — rename the column to "Determinism" or split into two columns — is better than either my "Default" or the current "High."

**Revised recommendation**: Rename the column from "Confidence" to "Default Strength" or, per integration-architect's suggestion, add a footnote clarifying that the determinism is structural (each type maps to exactly one mode) while empirical validation of these defaults has not been performed. Drop my demand for "Default" labels, which was less informative than what it would replace.

---

### Recommendation 2: Formalize or demote heuristic detection

**Original**: Either define a concrete scoring mechanism (weighted keywords, thresholds, tie-breaking) or rename from "Heuristic Mode Detection" to "Mode Suggestion Signals" and state the recommendation is always soft.

**Disposition**: REVISED — concede the formalization demand, retain the demote-to-advisory position.

Both cross-reviewers rightly point out that the heuristic detection operates on freeform natural language, not structured machine output. Integration-architect's observation is precise: the Dispute-Parsing Subsystem (SKILL.md lines 743-770) that I held up as a positive contrast parses structured text with known heading markers. Demanding the same formalism from a classifier operating on user-written problem descriptions is, as integration-architect puts it, "false precision." Weighted keyword scores would look formal but would be equally arbitrary without empirical calibration. I concede this.

What survives: the heuristic section (SKILL.md lines 1147-1156) does not reference the user confirmation gate (SKILL.md line 1210). Functional-typing identifies this exact gap and proposes the right fix: add a sentence in the heuristic section stating "The heuristic recommendation is always presented to the user for confirmation before proceeding." This is sufficient. No scoring function needed — just an explicit acknowledgment that the heuristic output is advisory, not authoritative.

**Revised recommendation**: Add a sentence to the Heuristic Mode Detection section (SKILL.md line 1156) stating that the recommendation is advisory and always subject to user confirmation. Drop the demand for weighted keyword scoring.

---

### Recommendation 3: Add agent-launch cost estimate to the interests confirmation step

**Original**: After presenting suggested interests, include an agent-launch cost estimate using the formula from SKILL.md lines 1304-1306.

**Disposition**: REVISED — concede the placement, retain the recommendation.

Both cross-reviewers agree this is a real gap but correctly identify that my proposed placement is wrong. At interest confirmation time, the mode is not yet selected, and the mode affects the launch formula (red-blue has asymmetric counts). The cost can only be accurately calculated after mode selection. Integration-architect and functional-typing converge on the same fix: place the launch estimate in the mode handler's confirmation display (SKILL.md lines 1197-1208), where both agent count and mode are known.

**Revised recommendation**: Add an agent-launch cost estimate to the mode confirmation step (not the interests confirmation step). The mode handler's confirmation display already shows agent count, mode, and target — adding "Estimated agent launches per round: {N^2 + N + 1}" completes the picture. This is the only point where all variables are known.

---

### Recommendation 4: Add interest-vs-type cross-validation to the mode command

**Original**: When interest structure signals a different mode than the problem type, warn the user and suggest re-evaluating the problem type.

**Disposition**: REVISED — accept integration-architect's refinement of the mechanism.

Integration-architect agrees this is a real gap but correctly objects to my proposed mechanism of re-invoking heuristic detection when interests contradict the problem type. The heuristic detection section is explicitly scoped to "when the problem type from problem.md is ambiguous or missing" (SKILL.md line 1149). Expanding its trigger to include "present but contradicted" changes it from a fallback to a validator, which is a different role.

Integration-architect's alternative — a separate validation step in the mode handler that compares interest naming patterns against the problem type and emits a warning — is cleaner. It preserves the heuristic section's scoping while still catching the case where `define` and `interests` were run at different times with evolving understanding.

**Revised recommendation**: Add a validation step in the mode handler (between reading inputs and running the decision matrix) that checks whether the interest structure's naming pattern (products/tools vs. teams/roles vs. overlapping claims vs. asymmetric roles) is consistent with the stated problem type. If inconsistent, warn: "Your interests suggest a {inferred-type} problem, but problem.md says {stated-type}. Consider re-running /conversus define to update the type, or proceed with the current type." This is a warning, not a block.

---

### Recommendation 5: Evaluate whether `interests.md` should be optional

**Original**: Consider making `interests.md` optional or providing a `/conversus mode --from-problem` shortcut that skips it.

**Disposition**: WITHDRAWN.

I concede this recommendation. Both cross-reviewers identified concrete architectural reasons why `interests.md` must be a persisted file, and I cannot rebut them:

1. **Prerequisite routing depends on it.** The mode handler's three-case prerequisite check (SKILL.md lines 1099-1115) uses `interests.md` existence as a routing signal. Making it optional would require two code paths — one with the file, one without — doubling prerequisite logic. Integration-architect is right that this is a regression, not a simplification.

2. **Interest structure is not recoverable from problem.md.** My claim that "interest structure could be extracted at mode-selection time by reading problem.md directly" was wrong about the data source. Users may rename, add, or remove interests during the interactive confirmation flow (SKILL.md lines 996-1004). The edited interest structure after user modifications is stored in `interests.md`, not derivable from `problem.md`.

3. **The Perspective field IS machine-consumed.** I dismissed it as "human-readable metadata, not machine-consumed input." Integration-architect points out that the mode handler reads it for the confirmation display (SKILL.md line 1203) and the report (SKILL.md lines 1286-1288). It is consumed by the mode handler.

4. **Functional-typing's observation is the clincher.** My own proposed `--from-problem` shortcut would still need to present interests for confirmation, display them in structured format, and allow modification — which recreates the `interests.md` workflow inside the mode command without eliminating the coupling. The complexity moves from inter-file to intra-command, with no net reduction.

The separate file earns its keep as an editable, versionable intermediate artifact that the user can modify between commands. I was wrong.

---

### Recommendation 6: Specify behavior when `problem.md` has status: draft

**Original**: Define whether `/conversus interests` should warn, block, or proceed when `problem.md` has unresolved `[CLARIFY:]` tags.

**Disposition**: RETAINED — strengthened by cross-reviewer agreement.

All three reviews independently identify this gap. Integration-architect frames it as "the status lifecycle is underspecified across the guided workflow." Functional-typing identifies the specific implementation gap: the Interest Generation table (SKILL.md lines 957-962) has no row for a `[CLARIFY: ...]`-tagged Type field.

Functional-typing recommends extracting the best-guess type from the CLARIFY tag and using it for calibration with a warning. In my cross-review of functional-typing, I argued this undermines the define handler's intentional ambiguity marker — `[CLARIFY:]` means "this needs human resolution," not "use the best guess and move on." I maintain that position. The safer behavior is to treat CLARIFY-tagged types as equivalent to "ambiguous" and trigger heuristic detection, which already handles the unset/ambiguous case and routes to user choice via mixed-signal handling.

**Retained recommendation**: When `problem.md` has `status: draft` or the Type field contains a `[CLARIFY: ...]` tag, the interests handler should warn: "problem.md has unresolved questions ({count} CLARIFY tags). Consider running /conversus define to resolve them before proceeding." Allow the user to proceed if they choose, using heuristic detection rather than the CLARIFY-tagged best-guess type for calibration. This treats the define handler's ambiguity markers with the seriousness they deserve without blocking the workflow.

---

## New Recommendations

### New Recommendation 1: Resolve the `ambiguous` row divergence between spec and SKILL.md

Functional-typing's P0 finding is the sharpest structural issue in this review cycle: the spec's decision matrix (spec line 52) includes an `ambiguous` row defaulting to `cooperative` at Low confidence, but SKILL.md replaces this with heuristic detection that could recommend ANY mode. This is an unresolved divergence.

In my cross-review of functional-typing, I argued that functional-typing's proposed fix (add a `cooperative` fallback when no heuristic signals are detected) would enshrine a bad default. The SKILL.md's current behavior — asking the user to choose when signals are mixed — is better than silently defaulting to cooperative. Many ambiguous problems turn out to be selection problems where cooperative mode produces mushy consensus instead of a clear winner.

The correct resolution is to update the spec, not the SKILL.md. The spec should drop the `ambiguous` row and replace it with an explicit reference to heuristic detection with user choice as the terminal fallback when no clear signal emerges. The SKILL.md already does this correctly. The spec should catch up.

### New Recommendation 2: Validate preset existence at generation time or document the gap

Integration-architect's R-1 (validate preset existence) is underrated as a Medium priority in their review. I escalated this in my cross-review and maintain it here. When a preset-backed agent appears in `conversus.yml` with `preset: category/preset-name` instead of an inline `prompt`, the run engine must resolve that preset at execution time. The post-write validation (SKILL.md lines 1262-1273) checks that each agent has `name` and `prompt` (or `preset`) but does not resolve the preset. This means validation passes on a config that will deterministically fail at run time if the preset has been deleted or renamed.

Either validate preset existence at generation time (when the preset file is known to exist because the interests handler just matched it), or update the post-write validation section to explicitly state that preset resolution is deferred to run time and is not covered by generation-time validation. Do not leave this as an implicit gap.

### New Recommendation 3: Document that generated configs are starter templates, not complete configs

Integration-architect notes that fields like `rounds`, `stagnation`, `validate_templates`, `prior`, and `arbiter` are "intentionally omitted from generation" and calls this "correct — these are advanced fields that users add manually." But this contradicts the spec's stated goal of eliminating the need to understand YAML schemas (spec line 19). If the generated config is intentionally incomplete and requires users to manually add advanced fields, then users DO need to understand the YAML schema — at least the parts the generator does not cover.

The spec should acknowledge this boundary explicitly: generated configs are ready-to-run starter templates with sensible defaults, but users who want multi-round deliberation, stagnation detection, or arbitration must add those fields manually (or a future guided command could handle them). This is an honest framing that sets correct expectations without expanding scope.

---

## Position Summary

This revision concedes three positions, revises three others, and retains one. The major concession is on `interests.md` as an optional artifact — both cross-reviewers demonstrated concrete architectural dependencies that I failed to account for. The file earns its keep. I was wrong.

The major revision is on confidence labels and heuristic formalization. Integration-architect's reframing — "confidence" is doing double duty between determinism and empirical accuracy — is more precise than my original "fabricated" label. And both cross-reviewers correctly argue that demanding weighted keyword scoring for a classifier operating on freeform text is false precision. The advisory nature of the heuristic output is the real issue, and a single sentence in the spec resolves it.

What survives intact: the `problem.md` draft status gap (universally agreed across all three reviews), the need for agent-launch cost transparency (with corrected placement at mode confirmation, not interests confirmation), and the interest-vs-type cross-validation gap (with integration-architect's cleaner mechanism replacing my original proposal).

Three new recommendations emerge from synthesizing the cross-reviews: resolving the `ambiguous` row spec/SKILL.md divergence (update the spec to match the SKILL.md's superior behavior), validating preset existence at generation time (or documenting the gap), and honestly framing generated configs as starter templates rather than complete configurations.

The spec is sound. The implementation is faithful and in some cases superior to the spec (notably the ambiguous-case handling). The gaps that remain are documentation and expectation-setting issues, not architectural flaws.
