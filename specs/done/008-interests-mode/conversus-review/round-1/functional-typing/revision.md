# Functional-Typing Revision: Spec 008

**Reviewer**: functional-typing
**Phase**: Cooperative Revision (Phase 3)
**Date**: 2026-03-22

---

## Recommendation Dispositions

### P0-1: Add `ambiguous` fallback to heuristic detection (SKILL.md ~line 1156)

**Original recommendation**: After heuristic signal scoring, add a fallback defaulting to `cooperative` with Low confidence per the spec's decision matrix. Alternatively, update the spec to remove the `ambiguous` row.

**Cross-review challenges**:
- integration-architect (cross-review, Dangerous Contradictions #1): The P0 fix is "backwards" — blindly defaulting to `cooperative` when no signals are detected would suppress the user interaction that SKILL.md's mixed-signal handler provides. The spec should align to the SKILL.md behavior, not the other way around. Demote to P1 spec-update.
- devils-advocate (cross-review, Dangerous Contradictions #1): The P0 fix "would hardcode a fallback that enshrines bad defaults." When heuristic detection finds no signals, the honest answer is "I cannot determine the right mode" — not "default to cooperative." The current SKILL.md behavior (asking the user to choose) is a feature, not a bug. The spec should drop the `ambiguous` row.

**Disposition: MODIFIED — demote to P1, change the prescribed fix direction.**

Both cross-reviewers make the same structural argument, and it is correct. My original review acknowledged that the SKILL.md approach was "arguably more sophisticated" (my review line 101) but still prescribed adding the spec's default to the implementation. On reflection, this was internally inconsistent: I recognized the SKILL.md behavior as superior, then recommended reverting to the inferior spec behavior for compliance purposes.

The right resolution is a spec update, not an implementation change. The spec's `ambiguous` row (spec line 52: `| ambiguous | cooperative | Low — present alternatives |`) should be replaced with a reference to heuristic mode detection and the mixed-signal handler. When no signals are detected for any mode, asking the user to choose (SKILL.md lines 1158-1176) is more honest and more useful than silently assigning `cooperative`.

However, I maintain that this IS a real divergence that requires explicit resolution. integration-architect and devils-advocate both agree on this point. The two documents currently disagree, and the disagreement must be resolved in one direction. The severity remains P1 (not P2) because an unresolved disagreement between spec and implementation on a core decision path is a real shipping risk — a future implementer reading the spec would expect `cooperative` as the default for ambiguous types and would not find it in the SKILL.md.

**Revised recommendation**: Update spec 008, line 52 — replace the `ambiguous` row with: "When the problem type is ambiguous or unset, use heuristic mode detection (FR-008). If no mode has detectable signals, present the top candidates and ask the user to choose." This aligns the spec with the SKILL.md behavior that all three reviewers agree is correct.

---

### P1-2: Add `Preset` field to spec schema (spec.md ~line 87)

**Original recommendation**: Add `- **Preset**: <category/preset-name>  <!-- only if a preset was used -->` to the spec's `interests.md` schema block.

**Cross-review challenges**:
- integration-architect (cross-review, Dangerous Contradictions #2): Agrees on the action but disagrees on the framing. This is not "specification drift" — it is a necessary consequence of FR-006 and the interests-to-config data flow. Without the `Preset` field, there is no mechanism to carry a preset reference through to config generation. Calling it "drift" risks a future implementer removing the field to "align with spec."
- devils-advocate (cross-review, Dangerous Contradictions #2): Accepts FR-011 compliance at face value while questioning whether `preset:` on an agent entry in the generated `conversus.yml` is part of the established schema. Also notes (Dangerous Contradictions #3) that adding `Preset` to `interests.md` creates a new staleness vector — preset files could be updated or deleted after `interests.md` is written.

**Disposition: MODIFIED — accept reframing, address the downstream concerns.**

integration-architect is right on the framing. My original review called this "specification drift," which implies the implementation strayed from the spec. The more accurate characterization is "spec omission" — FR-006 (spec line 40) mandates preset support, but the schema block (spec lines 72-87) was not updated to include the field needed to carry that support. The SKILL.md closes a data-flow gap, not creates drift.

On devils-advocate's FR-011 concern: this challenge does not hold. The run engine schema (SKILL.md line 88) explicitly includes `preset: preset-name  # optional: reference a preset` on agent entries. The `preset:` key in generated `conversus.yml` (SKILL.md line 1260) IS part of the established schema. FR-011 compliance is genuine, not surface-level.

On devils-advocate's staleness vector concern: this is a valid observation I did not consider. Adding `Preset` to `interests.md` creates a reference that can go stale if the preset file is modified or deleted after interest discovery. However, the severity is bounded: preset staleness would be caught at run time during preset resolution (SKILL.md lines 119-130), which fails with a clear error message. The existing staleness detection (FR-013, SKILL.md lines 1117-1122) only tracks `interests.md` vs `conversus.yml` modification times, and extending it to track preset file modifications would be scope creep for this spec. The run-time validation is sufficient protection.

**Revised recommendation**: Update the spec's `interests.md` schema (spec.md ~line 87) to include the optional `Preset` field. Frame this as closing a spec omission required by FR-006's data-flow needs, not as aligning to implementation drift. integration-architect's complementary R-1 (add preset existence validation to the mode handler's post-write check) is a worthwhile addition — SKILL.md line 1269 already validates `prompt` (or `preset`) presence, and line 1271 validates `docs` paths exist on disk, so validating that a `preset:` value resolves to an existing preset file follows the same pattern.

---

### P1-3: Clarify CLARIFY-tagged Type handling (SKILL.md ~line 955)

**Original recommendation**: Add a note: "If the Type field contains a `[CLARIFY: ...]` tag, extract the best-guess type from the tag text and use it for calibration. Warn the user that the problem type is unconfirmed."

**Cross-review challenges**:
- integration-architect (cross-review, Tensions #3): Agrees the gap is valid and the recommendation reasonable, noting severity depends on frequency. The `[CLARIFY:]` path is uncommon (only fires when problem description is too vague for classification).
- devils-advocate (cross-review, Tensions #3): Argues that extracting a best-guess type from a CLARIFY tag conflicts with the define handler's intent. The define handler uses `[CLARIFY: ...]` to mean "this needs human resolution," not "use the best guess and move on." Treating CLARIFY-tagged types as equivalent to "ambiguous" and triggering heuristic detection would be safer than extracting a guess.

**Disposition: MODIFIED — accept devils-advocate's correction on the fix direction.**

Devils-advocate makes a sharp point that I missed. The define handler's `[CLARIFY: ...]` tag is an intentional ambiguity marker — a signal that the type classification was uncertain and the user should resolve it. My original recommendation to extract the best-guess type and proceed with a warning undermines that signal. It converts "this needs human resolution" into "here's my guess, moving on."

The better behavior, as devils-advocate suggests, is to treat a CLARIFY-tagged Type field as equivalent to "ambiguous" — routing it through heuristic mode detection (SKILL.md lines 1147-1156) rather than pretending the best-guess type is usable. For the interests handler specifically (which needs a type for calibration style selection), this means either: (a) using the heuristic signals from the problem description to infer a calibration style, or (b) asking the user to confirm the type before proceeding.

**Revised recommendation**: Add a note to the interests handler's Interest Generation section (SKILL.md ~line 955): "If the Type field contains a `[CLARIFY: ...]` tag, treat the problem type as unresolved. Ask the user to confirm the type before selecting a calibration style: 'The problem type is marked as uncertain: {CLARIFY text}. Which type best fits: selection, integration, scoping, or stress-test?' If the user cannot decide, use `integration` calibration style as a neutral default and note it in the interests.md output." Similarly, in the mode handler, route CLARIFY-tagged types through heuristic mode detection rather than the decision matrix.

---

### P2-4: Align staleness warning text

**Original recommendation**: Consider using identical text in spec and SKILL.md for traceability.

**Cross-review challenges**:
- integration-architect (cross-review, Safe Agreements #6): Confirms semantics are equivalent and notes the SKILL.md wording is "actually more precise."
- devils-advocate: Does not challenge this point.

**Disposition: WITHDRAWN.**

Both cross-reviewers and my own review agree the semantics are identical. The SKILL.md wording ("interests.md has changed since conversus.yml was last generated") is more precise than the spec's ("interests.md changed"). Forcing text alignment would mean either degrading the SKILL.md's more precise phrasing or updating the spec to match — and the latter is cosmetic editing with no functional value. The spec states the requirement; the implementation satisfies it with better wording. This is not worth tracking.

---

### P2-5: Document `--output` in spec

**Original recommendation**: If `--output` is to be a stable interface, add it to the spec's FR list or a "Supported Options" section.

**Cross-review challenges**:
- integration-architect (cross-review, Tensions #2): Agrees it is minor. Suggests a cross-cutting "Common Options" section rather than per-feature FR entries, since `--output` affects all handlers uniformly.
- devils-advocate (cross-review, Tensions #2): Challenges the "benign" framing — `--output` also changes the read path (SKILL.md line 949: "Also changes where `problem.md` is read from"), making it a dual read/write override. A user expecting only write-path override could get "No problem.md found" because the flag redirected the read path. Suggests splitting into `--output` (write) and `--input` (read) flags.

**Disposition: MODIFIED — escalate to P1 based on devils-advocate's analysis.**

Devils-advocate identifies a real footgun I underestimated. The `--output` flag's dual semantics (SKILL.md line 949: "Also changes where `problem.md` is read from"; line 1130: "Also changes where `problem.md` and `interests.md` are read from") are counterintuitive. A flag named `--output` should control output location, not input resolution. This is not merely "undocumented" — it is a confusing interface design that could cause user errors.

However, splitting into `--output` and `--input` flags may be premature for this spec. The simpler fix is to document the dual semantics explicitly in the spec and, if a future spec introduces a `--context` or `--input` flag, refactor at that time.

**Revised recommendation**: Escalate to P1. Add a "Common Options" section to spec 008 documenting `--output <dir>` with explicit mention that it overrides both the write path and the read path for prerequisite files (`problem.md`, `interests.md`). This prevents users from being surprised by the dual semantics and gives future specs a reference point for the behavior.

---

## New Recommendations

### N-1: Add preset existence validation to mode handler post-write check (P1)

**Source**: integration-architect's R-1, reinforced by devils-advocate's staleness concern.

The mode handler's post-write validation (SKILL.md lines 1263-1273) checks that agent names, prompts (or presets), modes, and doc paths are valid. Rule 7 (line 1271) already validates that `docs` paths exist on disk. However, when an agent entry uses `preset:` instead of an inline `prompt:` (line 1260), the post-write validation does not verify that the referenced preset file exists. This means a generated `conversus.yml` could reference a deleted or renamed preset and pass post-write validation, only to fail at run time.

**Recommendation**: Add a validation rule to the post-write check (SKILL.md ~line 1271): "If an agent uses `preset:`, resolve the preset path using the same resolution rules as Run: Execution Step 1. If the preset file does not exist, warn: 'Agent {name} references preset {preset} which cannot be resolved. The generated config may fail at run time.'" This follows the same pattern as rule 7 (docs path existence) and catches staleness between interest discovery and config execution.

### N-2: Add explicit handling for zero-signal heuristic detection outcome (P2)

**Source**: Synthesized from all three reviewers' discussion of the ambiguous row.

All three reviewers agree the spec's `ambiguous` row should be replaced with heuristic detection + user choice. However, the current SKILL.md heuristic detection section (lines 1147-1156) does not explicitly state what happens when ALL signal scores are zero — no keywords detected, no interest-name patterns matched, no structural signals found. The mixed-signal handler (lines 1158-1176) fires when "top two modes are within close signal density," but this assumes at least two modes have nonzero signal density. The edge case where no signals are detected at all is implicit but unspecified.

**Recommendation**: Add a sentence to the heuristic detection section (SKILL.md ~line 1156): "If no signals are detected for any mode, present all four modes with their plain-language descriptions and ask the user to choose. Do not default silently." This closes the edge case without enshrining a default that all three reviewers agree would be counterproductive.

---

## Position Summary

My original review identified two structural gaps (the missing `ambiguous` row and the `Preset` field schema divergence) and two operational gaps (CLARIFY-tag handling and `--output` documentation). The cross-reviews from integration-architect and devils-advocate have refined my understanding of all four.

**What I withdraw**: The P0 severity on the `ambiguous` row finding, and the specific fix direction (adding a `cooperative` fallback to SKILL.md). Both cross-reviewers convincingly argue that the SKILL.md behavior — heuristic detection plus user choice — is superior to the spec's static default. The fix should flow from spec to SKILL.md alignment, not the reverse. I also withdraw P2-4 (staleness warning text alignment) as cosmetic noise.

**What I modify**: Three recommendations change form:
1. The `ambiguous` row resolution becomes a P1 spec update rather than a P0 SKILL.md fix.
2. The CLARIFY-tag handling adopts devils-advocate's insight that extracting a best-guess type undermines the define handler's intentional ambiguity marker. The fix now routes CLARIFY-tagged types through user confirmation rather than silent extraction.
3. The `--output` documentation escalates from P2 to P1 based on devils-advocate's identification of the dual read/write semantics as a genuine footgun.

**What I defend**: The core finding that the spec and SKILL.md disagree on the ambiguous case — all three reviewers confirm this divergence exists and must be resolved. The `Preset` field spec update — all three reviewers agree the field is necessary. The CLARIFY-tag handling gap — integration-architect and devils-advocate both independently confirm it. The characterization of the implementation as "conservative and additive" — I maintain this is accurate; every SKILL.md extension beyond the spec is operationally necessary detail. Devils-advocate's challenge that `interests.md` is a "coupling artifact" does not hold against the spec's explicit two-step design (spec line 17) and the heuristic detection's dependence on interest structure as a signal source (spec lines 65-66).

**Final priority stack**:

| Priority | Item | Action |
|---|---|---|
| P1 | Ambiguous row divergence | Update spec: replace `ambiguous` row with reference to heuristic detection + user choice |
| P1 | Preset field in spec schema | Update spec: add optional `Preset` field to `interests.md` schema (spec omission) |
| P1 | CLARIFY-tag handling | Update SKILL.md: route CLARIFY-tagged types through user confirmation, not silent extraction |
| P1 | `--output` dual semantics | Update spec: document `--output` in a Common Options section, noting it overrides both read and write paths |
| P1 | Preset existence validation (NEW) | Update SKILL.md: add preset file resolution check to mode handler post-write validation |
| P2 | Zero-signal edge case (NEW) | Update SKILL.md: explicit handling when heuristic detection finds no signals for any mode |

All six items are tractable and non-conflicting. The P1 items resolve real ambiguities or gaps that could cause implementer confusion or user-facing errors. The P2 item closes an edge case that is unlikely in practice but should be specified for completeness.
