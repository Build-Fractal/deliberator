# Cross-Review: integration-architect's Review of 008-interests-mode

**Reviewer**: devils-advocate
**Reviewing**: integration-architect
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. "None identified" under Off-Base Assumptions is itself off-base

Integration-architect states: "None identified. The implementation faithfully reflects the spec's scope, constraints, and design intent." This is a dangerous consensus position because it conflates spec-faithfulness with correctness. The implementation can be a faithful realization of a spec that contains flawed assumptions, and in this case it is.

The decision matrix assigns "High" confidence to all four problem-type-to-mode mappings. Integration-architect validates this as correct because the SKILL.md mirrors the spec. But mirroring a flawed table faithfully does not make the table right. The scoping-to-prisoners-dilemma mapping at "High" confidence is the clearest example: many scoping problems are coordination exercises without defection incentives (e.g., "which team should own the shared API gateway?"). Prisoners-dilemma mode imposes dispute structures (Disputed Boundaries, responsibility maps) that assume strategic boundary-setting. A faithful implementation of a wrong default still produces wrong deliberations.

Integration-architect's review validates the wiring but never questions whether the wires connect to the right endpoints. For an integration architect, wiring correctness is the job -- but the review should have flagged that "High confidence on all four rows" is untested and asserted, not empirical.

### 2. Preset existence validation concern (R-1) understates the severity

Integration-architect's R-1 recommends validating preset existence at generation time. The recommendation is framed as "Priority: Medium" -- a nice-to-have improvement. This is too gentle.

When a preset-backed agent appears in `conversus.yml` with `preset: category/preset-name` instead of an inline `prompt`, the run engine must resolve that preset at execution time. If the preset file has been deleted, renamed, or moved between generation and execution, the run fails. But the failure does not happen at the `mode` command -- it happens at `run`, potentially after the user has already invested time in other configuration. Worse, the post-write validation (SKILL.md lines 1263-1273) checks that each agent has `name` and `prompt` (or `preset`) but does not resolve the preset. This means validation passes on a config that will deterministically fail at run time.

This is not a medium-priority enhancement. It is a validation gap that allows the guided workflow to produce configs that pass all stated validation checks yet are guaranteed to fail. Either preset existence must be validated at generation time, or the post-write validation section must be updated to explicitly state that preset resolution is deferred to run time and is not covered by generation-time validation.

### 3. The "complete but omitted fields are intentional" framing hides a usability gap

Integration-architect notes: "Fields intentionally omitted from generation: `rounds`, `stagnation`, `validate_templates`, `prior`, `arbiter`. This is correct -- these are advanced fields that users add manually."

This is presented as a clean design decision, but it contradicts the spec's stated goal of eliminating the need to understand YAML schemas (spec line 19: "Together they eliminate the need for users to understand game theory or YAML schemas"). If the generated config is intentionally incomplete and requires users to manually add advanced fields, then users DO need to understand the YAML schema -- at least the parts the generator does not cover.

The review should have flagged this tension rather than affirming the omission as "correct." The spec either needs to acknowledge that generated configs are starter templates (not complete configs) or provide a follow-up command for adding advanced fields interactively.

---

## Tensions

### 1. Schema roundtrip fidelity is validated but not stress-tested

Integration-architect correctly maps every generated field to its run-engine counterpart and confirms alignment. The table is thorough. But the review does not address the roundtrip scenario where `target` in `problem.md` contains `(none)` and the mode handler asks the user for paths interactively (SKILL.md line 1254). In that case, the user-provided paths are not validated against the same rules as paths parsed from `problem.md`. The post-write validation catches missing files (line 1266: "All `target` paths exist on disk"), but this validation happens after the user has already confirmed the config. The user experience is: confirm config, then immediately see a validation warning about missing paths. This is a minor UX tension, not a showstopper, but it deserved mention in a roundtrip-focused review.

### 2. R-3 identifies triple-duplication of name pattern but dismisses it too quickly

Integration-architect's R-3 notes that the `[a-z0-9][a-z0-9-_]*` pattern appears in three places (interests line 964, mode line 1268, run line 198) and calls it "a documentation/maintenance observation, not a bug." This is technically correct today but is a design tension that grows worse with each new handler. The interests handler, mode handler, and run engine each independently validate the same constraint. If a future spec changes the allowed character set (e.g., to support uppercase or dots in agent names), three sections must be updated. The review should have recommended either centralizing the pattern definition (a single "Agent Name Rules" section referenced by all handlers) or at minimum flagging it as a maintenance risk rather than dismissing it.

### 3. Missed opportunities are too polite

Integration-architect identifies three "missed opportunities" -- no `--context` passthrough, no draft/ready status on interests.md, and unstructured heuristic signals. All three are framed as optional enhancements. But the heuristic signals issue is not a missed opportunity -- it is an underspecification that my own review identified as a reproducibility risk. Integration-architect calls it "prose descriptions" that could be "more deterministic and testable." That framing is correct but insufficiently urgent. When two reviewers independently flag the same issue, it should be escalated from "missed opportunity" to "actionable recommendation."

### 4. R-2 on `(none)` sentinel is narrower than the actual problem

Integration-architect's R-2 asks for the `(none)` sentinel to be documented in the interests handler since interests also reads Source Documents. This is correct but does not go far enough. The `(none)` sentinel is an ad-hoc convention from the define handler (SKILL.md line 891) that has no formal definition. Both interests and mode handlers must handle it, but neither defines what it means -- they inherit it implicitly. The tension is that a sentinel value in a markdown file is fragile: a user editing `problem.md` by hand might write "none", "N/A", "TBD", or simply delete the section. Only the exact string `(none)` triggers the special handling. This is a broader design fragility than R-2 acknowledges.

---

## Safe Agreements

### 1. FR-to-implementation mapping is thorough and accurate

Integration-architect's alignment section maps all 13 functional requirements to specific SKILL.md line ranges and confirms coverage. I verified the same mappings in my own review and found no gaps. The implementation covers every FR.

### 2. Dispatch table and prerequisite routing are correctly wired

Integration-architect's verification of the dispatch table anchors (lines 23-29) and the three-case prerequisite routing in the mode handler (lines 1099-1115) is accurate. The prerequisite permutation coverage is complete: both files present, one missing, both missing. My review did not challenge these mechanics.

### 3. Success criteria are achievable

All five success criteria (SC-001 through SC-005) are achievable from the implementation as written. Integration-architect's verification is correct. SC-003 (roundtrip validity) depends on the schema alignment being correct, which the field-by-field mapping confirms. SC-005 (missing problem.md routing) is directly implemented.

### 4. User confirmation gates are correctly placed

Both reviews agree that the implementation correctly gates all writes behind user confirmation (interests: line 1020, mode: line 1210). No silent overwrites. No agents generated without approval. This satisfies the spec's constraint at line 104.

### 5. The three spec constraints are honored

Integration-architect's verification that all three constraints (no game theory knowledge required, no agents without confirmation, no hard-coded agents/paths) are honored in the implementation is accurate. My review challenged the depth of the "no game theory knowledge" constraint's implementation but did not find a violation -- only a concern about the decision matrix's authority level, which is a spec-level issue, not an implementation-level violation.

### 6. R-4 on `--dry-run` for mode handler is a sensible suggestion

Integration-architect's R-4 suggesting `--dry-run` for the mode handler is reasonable. The mode handler produces the most consequential artifact (the executable config), and previewing without writing aligns with the spec's principle of user control. This is a low-priority enhancement that both reviews can endorse without controversy.
