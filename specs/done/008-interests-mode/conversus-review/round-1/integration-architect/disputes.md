# Integration Architect — Cooperative Disputes (Phase 4)

**Spec**: `008-interests-mode`
**Role**: integration-architect
**Date**: 2026-03-22

---

## Remaining Disputes

### 1. CLARIFY-tag handling: extract-and-warn vs. treat-as-ambiguous

Functional-typing's revision (P1-3, revised recommendation) and devils-advocate's revision (Recommendation 6, retained) converge on routing CLARIFY-tagged types through heuristic detection rather than extracting the best-guess type. Functional-typing's revised recommendation goes further: ask the user to confirm the type before selecting a calibration style.

My revision (N-1) prescribes the opposite direction: "extract the best-guess type from the tag text and use it for prompt calibration" with a warning and a pointer back to `/conversus define`.

I concede that my N-1 recommendation is wrong. Both other reviewers independently arrived at the same correction, and the structural argument is sound. The define handler produces `[CLARIFY: best-guess-type -- reason]` as an intentional ambiguity marker (SKILL.md ~line 845). Extracting the best-guess and proceeding, even with a warning, converts "this needs human resolution" into "here is my guess, moving on." That undermines the define handler's signal. The interests handler should treat a CLARIFY-tagged Type the same way the mode handler treats an ambiguous type: present the options and let the user decide.

However, I dispute one detail in functional-typing's revised recommendation. They propose a fallback default: "If the user cannot decide, use `integration` calibration style as a neutral default and note it in the interests.md output." This enshrines a silent default in the same way the spec's `ambiguous -> cooperative` row does. If the user cannot decide their problem type, the correct behavior is to route them back to `/conversus define` to resolve the CLARIFY tag, not to silently assign `integration`. The interests handler should not absorb ambiguity that the define handler explicitly flagged for resolution.

**My position**: Route CLARIFY-tagged types through user confirmation (agreed). Do NOT provide a silent `integration` fallback. If the user cannot decide, recommend they run `/conversus define` to resolve the CLARIFY tag first, then re-run `/conversus interests`.

---

### 2. `--output` dual semantics: document vs. split

Functional-typing's revision (P2-5, revised to P1) correctly identifies the `--output` flag's dual read/write semantics as a footgun (SKILL.md line 949: "Also changes where `problem.md` is read from"; line 1130: "Also changes where `problem.md` and `interests.md` are read from"). Their revised recommendation is to document the dual semantics in a "Common Options" section of the spec and defer flag splitting to a future spec.

I agree on the escalation to P1 and agree on documenting the dual semantics. However, I dispute the framing that calls the dual semantics "confusing interface design." The `--output` flag functions as a workspace directory override. In the conversus workflow, all artifacts (`problem.md`, `interests.md`, `conversus.yml`) co-locate in a single directory. The flag's semantics are: "use this directory as the workspace instead of the current working directory." Reading prerequisite files from the same workspace directory where output will be written is the only consistent behavior -- anything else would mean the mode handler reads `interests.md` from one directory and writes `conversus.yml` to another, which breaks the co-location invariant and creates exactly the confusion that functional-typing wants to prevent.

The documentation should frame `--output` as `--workspace` in spirit: "Override the working directory for all artifact I/O. Both prerequisite files and generated output will use this directory." This framing eliminates the "dual semantics" confusion without splitting the flag. If a future spec adds a genuine need to read from directory A and write to directory B, THAT spec should introduce the split, with the understanding that it breaks co-location.

Devils-advocate's revision does not raise the `--output` flag, implicitly accepting functional-typing's framing. I dispute the implicit acceptance -- the workspace-override framing is architecturally correct and should be the language used in the spec documentation.

**My position**: Document `--output` as a workspace directory override, not as a write-path flag with a surprising read-path side effect. The co-location of artifacts in a single directory is a design invariant, not a confusing accident.

---

### 3. Generated configs as "starter templates" vs. ready-to-run configs

Devils-advocate's revision (New Recommendation 3) argues the spec should acknowledge that generated configs are "starter templates, not complete configs" because advanced fields (`rounds`, `stagnation`, `validate_templates`, `prior`, `arbiter`) require manual YAML editing. Devils-advocate frames this as contradicting the spec's stated goal of eliminating the need to understand YAML schemas (spec line 19).

I dispute this characterization. The spec says the commands "eliminate the need for users to understand game theory or YAML schemas" (spec line 19). A generated config IS a complete, valid, ready-to-run config. It passes post-write validation (SKILL.md lines 1263-1273) using the same validation rules as `/conversus run`. Running `/conversus run` on a generated config works. The user does not need to touch YAML to get a working deliberation.

The advanced fields that devils-advocate lists are OPTIONAL fields for POWER USERS who want to customize deliberation behavior. Their omission does not make the generated config incomplete -- it makes it a valid minimal config with sensible defaults. The run engine applies defaults for all omitted optional fields: `rounds` defaults to 1, `iterations` defaults to 1, `stagnation` is disabled by default, `validate_templates` is disabled by default, `prior` is empty by default, `arbiter` is omitted by default (SKILL.md lines 1316-1319: "The `arbiter` field is fully optional. Omitting it preserves exact Phase 1-5 behavior" and "The `rounds` field is fully optional. Omitting it (or setting to 1) preserves exact current behavior").

Calling the generated config a "starter template" sets incorrect expectations -- it implies the config will not work until the user adds more fields. This is false. The config works immediately. Advanced fields are extensions, not requirements.

**My position**: The generated config is a complete, ready-to-run config with sensible defaults. Do NOT frame it as a "starter template" in the spec. If documentation is needed, add a note to the mode handler's report: "Advanced options (`rounds`, `stagnation`, `arbiter`) can be added to conversus.yml manually. See `/conversus run` documentation for available fields." This surfaces the extension points without undermining the validity of the generated config.

---

### 4. Preset existence validation: generation-time check vs. run-time deferral

All three reviewers agree preset existence should be validated. Devils-advocate's revision (New Recommendation 2) offers an alternative: "Either validate preset existence at generation time, or update the post-write validation section to explicitly state that preset resolution is deferred to run time." My revision (R-1, escalated to High) and functional-typing's revision (N-1) both prescribe generation-time validation.

I dispute the "or document the gap" alternative. The pattern is already established: SKILL.md line 1271 validates that `docs` paths exist on disk at generation time. Target paths are validated at generation time (SKILL.md line 1266). The principle is clear -- if the mode handler can verify a path at generation time, it should. Preset files are known to exist at interest discovery time (SKILL.md lines 985-992: the interests handler matches presets from `presets/` directory). If the file existed when interests were generated but is missing when mode generates the config, that is exactly the kind of staleness the post-write validation should catch.

Documenting the gap instead of fixing it means a user gets a green "Configuration generated" report from the mode handler, then a red resolution error from the run engine. The whole point of post-write validation is to prevent this category of delayed failure.

**My position**: Validate preset existence at generation time. Do not offer "document the gap" as an acceptable alternative. The validation pattern is established, the implementation is trivial (same existence check as `docs` paths), and the failure mode without it is user-hostile.

---

## Convergence

The following items have reached full agreement across all three reviewers. No further debate is needed.

### 1. Ambiguous row resolution: update the spec (unanimous)

All three reviewers agree: the spec's `ambiguous` row (spec line 52) should be replaced with a reference to heuristic mode detection plus user choice. The SKILL.md behavior (heuristic detection at lines 1147-1156 plus mixed-signal handling at lines 1158-1176) is superior to the spec's static `cooperative` default. The spec should be amended, not the SKILL.md.

- Functional-typing revision: "Update spec 008, line 52 -- replace the `ambiguous` row with: 'When the problem type is ambiguous or unset, use heuristic mode detection (FR-008). If no mode has detectable signals, present the top candidates and ask the user to choose.'"
- Integration-architect revision: "The resolution should be a spec amendment that replaces the `ambiguous` row."
- Devils-advocate revision: "The correct resolution is to update the spec, not the SKILL.md."

### 2. Preset field in spec schema: spec omission, not implementation drift (unanimous)

All three reviewers agree the `Preset` field must be added to the spec's `interests.md` schema (spec lines 72-87). All three agree this is a spec omission required by FR-006's data-flow needs, not implementation overreach.

- Functional-typing revision: "Frame this as closing a spec omission required by FR-006's data-flow needs."
- Integration-architect revision: "The implementation makes one assumption beyond the spec: that the interests.md schema should include a Preset field. That assumption is correct and necessary."
- Devils-advocate revision: Does not challenge the field, only adds a staleness concern which functional-typing addresses via run-time validation at preset resolution.

### 3. Heuristic detection is advisory, not authoritative (unanimous)

All three reviewers agree that the heuristic mode detection output should be explicitly marked as advisory and subject to user confirmation. Devils-advocate withdrew the demand for weighted keyword scoring. Functional-typing and integration-architect concur that formalization beyond a single advisory-nature sentence is false precision for a classifier operating on freeform natural language.

### 4. Problem.md draft status behavior: warn and proceed (unanimous)

All three reviewers independently identified the gap: spec 008 never defines behavior when `problem.md` has `status: draft` or unresolved `[CLARIFY:]` tags. All three converge on the same resolution: warn the user about the draft state, do not block the workflow.

### 5. Agent-launch cost estimate at mode confirmation (unanimous)

All three reviewers agree the cost estimate belongs in the mode handler's confirmation display (SKILL.md ~line 1203), not at interest confirmation time. At mode confirmation, both agent count and mode are known, making the estimate accurate.

### 6. Interest-vs-type cross-validation as a warning (unanimous)

Devils-advocate's recommendation (revised with integration-architect's mechanism) is accepted: a separate validation step in the mode handler that compares interest naming patterns against the stated problem type and warns if they diverge. This is a warning, not a block. The heuristic detection section retains its original scope (fires only when type is unset or ambiguous).

### 7. Zero-signal edge case: ask, do not default (unanimous)

Functional-typing's N-2 explicitly addresses the edge case where heuristic detection finds no signals for any mode. All three reviewers agree the correct behavior is to present all modes and ask the user to choose, not to default silently. This closes the gap left by removing the spec's `ambiguous` row.

### 8. `interests.md` is a necessary persisted artifact (unanimous)

Devils-advocate withdrew the recommendation to make `interests.md` optional, conceding three concrete architectural dependencies: prerequisite routing, non-recoverable user edits, and machine-consumed fields. The file earns its keep as an editable, versionable intermediate artifact.

---

## Final Position Statement

The three-reviewer process has been effective. Starting from six original recommendations across my review, I revised three, added three new ones, and now after the disputes phase I concede one more (CLARIFY-tag handling direction in N-1, where I adopt functional-typing and devils-advocate's treat-as-ambiguous approach with one refinement: no silent `integration` fallback).

Four genuine disputes remain. Two are about framing rather than action: whether `--output` dual semantics represent "confusing design" or "correct workspace behavior" (dispute 2), and whether generated configs are "starter templates" or "complete configs" (dispute 3). These framing disputes matter because they determine the language that goes into the spec, and language shapes implementer expectations. The other two disputes are about fix direction: whether CLARIFY-tag handling should include a fallback default (dispute 1), and whether documenting a validation gap is an acceptable alternative to fixing it (dispute 4).

Eight items have reached full convergence. These can proceed directly to the synthesis phase without further deliberation: the ambiguous row spec amendment, the Preset field spec addition, the advisory nature of heuristic detection, the draft status warning behavior, the launch cost estimate placement, the interest-vs-type cross-validation warning, the zero-signal edge case handling, and the architectural necessity of `interests.md`.

The implementation remains substantially correct and faithful to the spec. No blocking defects have been identified by any reviewer at any phase. All findings are resolvable within the current architecture through spec amendments (3 items), SKILL.md additions (5 items), or documentation updates (2 items). The disputes that remain are about precision of language and placement of validation boundaries -- the kind of refinements that improve a solid design rather than rescue a broken one.
