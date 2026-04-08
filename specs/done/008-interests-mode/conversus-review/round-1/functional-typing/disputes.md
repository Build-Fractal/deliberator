# Functional-Typing Disputes: Spec 008

**Reviewer**: functional-typing
**Phase**: Cooperative Disputes (Phase 4)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: CLARIFY-tag handling — extract-and-warn vs. treat-as-ambiguous

**With**: devils-advocate (revision, Recommendation 6 disposition)
**Regarding**: SKILL.md ~line 955, Interest Generation table behavior when Type contains `[CLARIFY: ...]`

All three reviewers agree the gap exists: the Interest Generation table (SKILL.md lines 957-962) has four concrete rows and no instruction for a CLARIFY-tagged Type field. The dispute is on what to do when the gap is closed.

**Devils-advocate's position** (revision, Recommendation 6 disposition): Treat CLARIFY-tagged types as equivalent to "ambiguous" and trigger heuristic detection. The `[CLARIFY:]` tag means "this needs human resolution," and using the best-guess type undermines the define handler's intentional ambiguity marker.

**Integration-architect's position** (revision, New Recommendation N-1): Extract the best-guess type from the CLARIFY tag text, use it for prompt calibration, and warn the user to confirm via `/conversus define`. This is the opposite of devils-advocate's position.

**My revised position** (revision, P1-3 disposition): I conceded devils-advocate's correction in Phase 3 and adopted the treat-as-ambiguous approach. However, I now observe a tension between my Phase 3 concession and the practical problem it creates.

The interests handler is NOT the mode handler. The mode handler can fall back to heuristic detection because mode selection only needs a single categorical output (which mode to use). The interests handler needs a calibration STYLE to generate prompt text — adversarial, cooperative, honesty-calibrated, or red/blue (SKILL.md lines 957-962). "Ambiguous" is not a calibration style. If we treat the type as ambiguous, the interests handler cannot generate prompts without either (a) asking the user to confirm the type first, or (b) picking a default calibration style anyway.

Option (a) — asking the user — is what my revised recommendation in Phase 3 prescribes. But this creates a workflow interruption that the define handler explicitly deferred: the define handler's `[CLARIFY:]` tag says "downstream commands decide how to handle this" (SKILL.md line 889). If the interests handler always blocks on CLARIFY-tagged types and sends the user back to `/conversus define`, it effectively makes the define handler's deferred resolution mandatory rather than optional.

Option (b) — picking a default — is what integration-architect recommends (use the best-guess type) and what devils-advocate rejects.

**My final position**: The interests handler should ask the user to confirm the type inline, NOT send them back to `/conversus define`. Present the CLARIFY tag's best-guess type and the alternative: "The problem type is marked as uncertain: {CLARIFY text}. Which calibration style should I use for interest prompts: adversarial (selection), cooperative (integration), honesty-calibrated (scoping), or red/blue (stress-test)?" This respects the ambiguity marker (devils-advocate's point) without blocking the workflow (integration-architect's concern) and without silently using an unconfirmed type (my original mistake). The mode handler should independently handle the same CLARIFY tag through heuristic detection, since it operates on a different input space.

This is a genuine dispute because integration-architect's revision (N-1) still recommends extract-and-warn with no user choice, and devils-advocate's revision still recommends routing through heuristic detection which does not apply to the interests handler's calibration table.

---

### Dispute 2: `--output` flag — dual semantics documentation vs. split flags

**With**: devils-advocate (revision — implicit, not explicitly revised but original position stands)
**Regarding**: SKILL.md lines 949 and 1130, `--output` flag behavior

In Phase 3, I escalated this from P2 to P1 based on devils-advocate's cross-review identifying the dual read/write semantics as a footgun. Devils-advocate's original position (cross-review, Tensions #2) was to consider splitting `--output` into `--output` (write) and `--input` (read) flags.

**My position**: Document the dual semantics in the spec, do not split the flag. The `--output` flag's dual semantics — overriding both write path and read path for prerequisite files (SKILL.md line 949: "Also changes where `problem.md` is read from"; line 1130: "Also changes where `problem.md` and `interests.md` are read from") — follow a coherent design principle: all conversus artifacts live in the same directory. Splitting into `--output` and `--input` would create a new class of user error where artifacts are scattered across directories, breaking the prerequisite chain (`problem.md` in one directory, `interests.md` in another, `conversus.yml` in a third).

Devils-advocate did not revise this position in Phase 3 (it does not appear in their revision's recommendation dispositions), so I cannot confirm whether they still advocate for split flags. If they do, this remains a dispute on interface design philosophy: single-directory coherence (my position) vs. explicit read/write separation (their position).

**Resolution path**: If devils-advocate has withdrawn the split-flag suggestion, this dispute is resolved — document the dual semantics in the spec's Common Options section. If they maintain it, we should defer the split to a future spec that introduces multi-directory workflows, since spec 008 assumes a single working directory.

---

### Dispute 3: Generated config completeness framing

**With**: devils-advocate (revision, New Recommendation 3)
**Regarding**: Spec line 19, spec line 57, and SKILL.md lines 1233-1260

Devils-advocate argues that the spec's goal of eliminating the need to understand YAML schemas (spec line 19: "eliminate the need for users to understand game theory or YAML schemas") contradicts the reality that generated configs are intentionally incomplete — fields like `rounds`, `stagnation`, `validate_templates`, `prior`, and `arbiter` are omitted. Devils-advocate recommends the spec "acknowledge this boundary explicitly."

**My position**: The spec's claim is accurate as stated, and the generated config IS complete for a first run. The omitted fields are all optional with sensible defaults defined in the run engine schema (SKILL.md lines 57-60): `iterations: 1`, `rounds: 1`, `stagnation: detect`, `validate_templates: true`. A generated config without these fields is valid input for `/conversus run` — this is verified by SC-003 (spec line 95: "Generated `conversus.yml` is valid input for `/conversus run` — the roundtrip works").

The spec does not claim that users will NEVER need to understand the schema — it says the two commands "eliminate the need" for the initial generation workflow. Users who want multi-round deliberation or arbitration are, by definition, past the initial guided workflow and into advanced configuration territory. This is not a contradiction; it is a scope boundary.

However, devils-advocate's underlying concern — that users may not know what advanced fields exist — is worth addressing. The mode handler's report section (SKILL.md lines 1277-1295) could include a brief note: "For multi-round deliberation, stagnation detection, or subject arbitration, see the conversus.yml schema reference." This acknowledges the boundary without framing the generated config as incomplete.

**This dispute is low-severity.** If devils-advocate insists on explicit "starter template" framing in the spec, the impact is cosmetic. I disagree with the framing but not strongly enough to block it.

---

## Convergence

The following points have reached full convergence across all three reviewers. These are settled.

### C-1: The `ambiguous` row must be resolved by updating the spec, not the SKILL.md

All three reviewers independently conclude that the SKILL.md's heuristic detection + user choice behavior (SKILL.md lines 1145-1176) is superior to the spec's static `cooperative` default (spec line 52). The spec should be amended to replace the `ambiguous` row with a reference to heuristic mode detection and user choice as the terminal fallback. No reviewer advocates for adding a `cooperative` default to the SKILL.md.

**Cited agreement**:
- functional-typing revision, P0-1 disposition: "The right resolution is a spec update, not an implementation change."
- integration-architect revision, FR-007 status: "The resolution should be a spec amendment that replaces the `ambiguous` row."
- devils-advocate revision, New Recommendation 1: "The correct resolution is to update the spec, not the SKILL.md."

### C-2: The `Preset` field belongs in the spec's `interests.md` schema

All three reviewers agree the spec's schema (spec lines 72-87) should include the optional `Preset` field. This is a spec omission required by FR-006's data-flow needs, not implementation drift.

**Cited agreement**:
- functional-typing revision, P1-2 disposition: "Frame this as closing a spec omission required by FR-006's data-flow needs."
- integration-architect revision, Original finding: "No off-base assumptions" status: "The spec schema should be updated to include it."
- devils-advocate: Does not dispute the field's inclusion (revision, Recommendation 5 withdrawal implicitly accepts the interests.md schema as necessary).

### C-3: Preset existence validation should be added to post-write checks

All three reviewers agree that the mode handler's post-write validation (SKILL.md lines 1262-1273) should verify that `preset:` references resolve to existing preset files, following the same pattern as rule 7's docs path validation (SKILL.md line 1271).

**Cited agreement**:
- functional-typing revision, N-1: "Add a validation rule to the post-write check."
- integration-architect revision, R-1: "Validate that referenced preset files exist on disk at generation time."
- devils-advocate revision, New Recommendation 2: "Validate preset existence at generation time."

### C-4: The CLARIFY-tag handling gap exists and must be addressed

All three reviewers confirm that the interests handler has no explicit instruction for Type fields containing `[CLARIFY: ...]` tags (SKILL.md lines 957-962). The gap is real. The precise fix is disputed (see Dispute 1 above), but the existence of the gap is settled.

**Cited agreement**:
- functional-typing revision, P1-3.
- integration-architect revision, N-1.
- devils-advocate revision, Recommendation 6 disposition.

### C-5: `problem.md` draft status behavior should be specified

All three reviewers agree that spec 008 should define what happens when `/conversus interests` is run against a `problem.md` with `status: draft`. The define handler explicitly defers this to downstream specs (SKILL.md line 889), and spec 008 never exercises that option.

**Cited agreement**:
- integration-architect revision, N-2: "Warn and proceed without blocking."
- devils-advocate revision, Recommendation 6 disposition: "Allow the user to proceed if they choose."
- functional-typing revision, P1-3 disposition (implicitly — the CLARIFY-tag handling recommendation addresses the same underlying gap).

### C-6: Heuristic detection is advisory, not authoritative

All three reviewers agree that the heuristic mode detection output (SKILL.md lines 1147-1156) should be explicitly marked as advisory and subject to user confirmation. The user confirmation gate at SKILL.md line 1210 provides the mechanism, but the heuristic section does not reference it.

**Cited agreement**:
- devils-advocate revision, Recommendation 2 disposition: "Add a sentence to the Heuristic Mode Detection section stating that the recommendation is advisory."
- functional-typing revision, P0-1 disposition (implicitly — the spec update recommendation includes "present the top candidates and ask the user to choose").
- integration-architect revision, FR-007 status: "If no mode has detectable signals, present the top candidates and ask the user to choose."

### C-7: Agent-launch cost estimate belongs at mode confirmation, not interests confirmation

All three reviewers agree the launch cost estimate should be surfaced, and all three agree it belongs in the mode handler's confirmation display (SKILL.md lines 1197-1208) rather than at interest confirmation time.

**Cited agreement**:
- devils-advocate revision, Recommendation 3 disposition: "Add an agent-launch cost estimate to the mode confirmation step."
- integration-architect revision, N-3: "Add the agent-launch estimate to the mode handler's confirmation display."
- functional-typing: No objection raised in any phase.

### C-8: Staleness warning text alignment is cosmetic and not worth tracking

All three reviewers agree the spec's wording ("interests.md changed") and SKILL.md's wording ("interests.md has changed since conversus.yml was last generated") are semantically equivalent, with the SKILL.md version being more precise.

**Cited agreement**:
- functional-typing revision, P2-4 disposition: "WITHDRAWN."
- integration-architect original review, Safe Agreements #6.
- devils-advocate: No challenge raised.

---

## Final Position Statement

### What I defend without modification

**The spec and SKILL.md must explicitly agree on the ambiguous case.** This was the central finding of my original review, and four phases of deliberation have only strengthened it. Every reviewer, from every angle, confirms the divergence exists and must be resolved. The direction is now settled (update the spec), but I defend the finding's importance: an unresolved disagreement between a specification and its implementation on a core decision path is not cosmetic. A future implementer reading spec line 52 would expect `cooperative` as the default for ambiguous types and would build accordingly. The spec must be updated to prevent that.

**The `Preset` field is a spec omission, not implementation drift.** My original review used the term "specification drift," which integration-architect correctly challenged. I accept the reframing. But I defend the substance: the two documents disagree on the schema, and the disagreement must be resolved. The resolution is a spec update adding the optional `Preset` field.

**The `--output` dual semantics are a P1 documentation gap.** Devils-advocate identified the footgun; I escalated the severity. A flag named `--output` that also controls input resolution is counterintuitive and must be documented. Whether or not the flag is eventually split, users need to know what it does today.

### What I concede

**My original P0 severity was wrong.** The ambiguous row divergence is P1 (spec update needed), not P0 (implementation defect). Both cross-reviewers demonstrated that the SKILL.md behavior is intentionally superior. I was wrong to prescribe adding the spec's inferior default to the implementation.

**My original CLARIFY-tag fix direction was wrong.** Extracting the best-guess type and proceeding with a warning undermines the define handler's intentional ambiguity marker. Devils-advocate's correction was sharp and I accepted it in Phase 3. I now refine the fix further (see Dispute 1) but the original direction was incorrect.

**Staleness warning text alignment is not worth tracking.** I withdraw P2-4 entirely. The SKILL.md wording is better. Forcing alignment would degrade it.

### Non-negotiables

1. **The spec's `ambiguous` row (spec line 52) must be updated.** The current text prescribes behavior that all three reviewers agree is inferior to the implementation. Shipping with this divergence intact means the spec actively misleads future implementers.

2. **The spec's `interests.md` schema (spec lines 72-87) must include the optional `Preset` field.** FR-006 mandates preset support. The schema that carries preset references must reflect that mandate. Omitting it breaks the data-flow traceability from spec requirement to implementation.

3. **Post-write validation must check preset file existence (SKILL.md ~line 1269).** A generated `conversus.yml` that passes all validation checks but deterministically fails at run time due to a missing preset is a validation gap that contradicts the purpose of post-write validation. The pattern already exists for docs paths (SKILL.md line 1271); extending it to presets is consistent and necessary.

4. **The CLARIFY-tag gap in the interests handler must be closed.** The specific fix is disputed (Dispute 1), but leaving the interests handler silent on CLARIFY-tagged types is not acceptable. The Interest Generation table (SKILL.md lines 957-962) must have explicit instruction for this case.

5. **The `--output` dual semantics must be documented in the spec.** Whether in a Common Options section or per-FR entries, users must be told that `--output` overrides both write and read paths. This is a stable interface behavior that the spec does not mention at all.

### Priority stack entering synthesis

| Priority | Item | Status | Action |
|---|---|---|---|
| P1 | Ambiguous row divergence | Converged (C-1) | Update spec: replace `ambiguous` row with heuristic detection + user choice reference |
| P1 | Preset field in spec schema | Converged (C-2) | Update spec: add optional `Preset` field to `interests.md` schema |
| P1 | CLARIFY-tag handling | Disputed (D-1) | Update SKILL.md: add explicit CLARIFY-tag instruction to Interest Generation; exact mechanism to be resolved in synthesis |
| P1 | `--output` dual semantics | Minor dispute (D-2) | Update spec: document `--output` in Common Options, noting dual read/write behavior |
| P1 | Preset existence validation | Converged (C-3) | Update SKILL.md: add preset file resolution check to post-write validation |
| P1 | Draft status behavior | Converged (C-5) | Update SKILL.md: warn and proceed when `problem.md` has `status: draft` |
| P2 | Heuristic advisory note | Converged (C-6) | Update SKILL.md: add sentence stating heuristic output is advisory and subject to user confirmation |
| P2 | Agent-launch cost estimate | Converged (C-7) | Update SKILL.md: add launch estimate to mode confirmation display |
| P2 | Zero-signal edge case | Converged (C-1, implicit) | Update SKILL.md: explicit handling when all heuristic signal scores are zero |
| P2 | Generated config framing | Disputed (D-3) | Possibly update spec or mode handler report; low severity either way |
