# Cross-Review of functional-typing's Review

**Cross-reviewer**: integration-architect
**Reviewing**: functional-typing's review of spec 008 implementation in SKILL.md
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. The `ambiguous` row omission is flagged as a gap, but the SKILL.md behavior is intentionally more correct than a static default

functional-typing's Finding (FR-007, lines 96-104 of their review) identifies that SKILL.md's decision matrix omits the spec's `ambiguous` row and replaces it with heuristic detection + mixed-signal handling. They call this "Partially covered" and escalate to P0: "Add `ambiguous` fallback to heuristic detection."

I disagree with the P0 severity. The spec's `ambiguous` row prescribes `cooperative` at `Low` confidence. But SKILL.md line 1145 explicitly states: "When the problem type is unset or ambiguous, use heuristic mode detection." This is a deliberate routing decision, not an accidental omission. The heuristic detection (SKILL.md lines 1147-1156) scores all four modes by signal density, then either recommends the winner or triggers mixed-signal handling (lines 1158-1176), which presents two options and asks the user to choose.

The danger in functional-typing's P0 recommendation is that blindly defaulting to `cooperative` when no signals are detected would suppress the user interaction that SKILL.md's mixed-signal handler provides. Consider: a genuinely ambiguous problem with zero detectable signals benefits more from "Which approach fits your situation better?" than from silently assigning `cooperative` at Low confidence. The spec's intent (line 103: "Must NOT require game theory knowledge") is better served by asking than by defaulting.

That said, functional-typing is correct that the two documents disagree and this disagreement should be resolved. The resolution should be to update the spec to replace the `ambiguous` row with a reference to heuristic detection and mixed-signal handling, not to add a silent fallback to SKILL.md. This is a spec-update issue, not a SKILL.md fix.

**Verdict**: The finding is valid but the prescribed fix is backwards. The spec should align to the SKILL.md behavior, not the other way around. Demote from P0 to P1 spec-update.

### 2. Characterizing the `Preset` field as "specification drift" understates its necessity

functional-typing's Finding (Missed Opportunities, item 2, lines 176-185) correctly identifies that SKILL.md's `interests.md` schema includes a `Preset` field (SKILL.md line 1041) that the spec's schema block (spec lines 72-87) omits. functional-typing calls this "specification drift" and recommends updating the spec.

I agree with the recommendation but disagree with the framing. This is not drift -- it is a necessary consequence of FR-006 (spec line 40: "Interests MAY reference presets") and the generated conversus.yml behavior (SKILL.md line 1260: "If an interest referenced a preset, include `preset: <category/preset-name>` on the agent entry instead of inlining the prompt"). Without the `Preset` field in `interests.md`, there is no mechanism to carry a preset reference from interest discovery through to config generation. The SKILL.md is closing a data-flow gap that the spec left open.

The danger of calling this "drift" is that a future implementer might remove the field to "align with spec," breaking the preset-to-config pipeline. This should be documented as a spec omission, not as implementation overreach.

**Verdict**: Agree on the action (update spec schema). Disagree on the framing (this is a spec omission, not implementation drift). My review's R-1 (preset existence validation at post-write time) is the complementary concern: the Preset field must exist for data flow, but the generated config must also validate that the referenced preset file still exists.

---

## Tensions

### 1. Severity of the `ambiguous` fallback: P0 (functional-typing) vs. not flagged (integration-architect)

functional-typing rates the missing `ambiguous` row as P0 must-fix. My review did not flag it at all because the SKILL.md behavior (heuristic detection + mixed-signal + user choice) is strictly more capable than the spec's static fallback. We agree the documents disagree; we disagree on which document is wrong and how urgently it matters.

The tension resolves by acknowledging that both reviewers are protecting different properties. functional-typing protects spec compliance (the spec says `cooperative`, the implementation does not guarantee `cooperative`). I protect user experience (asking is better than silently defaulting). The right resolution is a spec amendment that removes the `ambiguous` row and adds: "When the problem type is ambiguous or unset, use heuristic mode detection (section X). If no mode has detectable signals, present the top candidates and ask the user to choose."

### 2. Whether `--output` is worth documenting in the spec

functional-typing notes (Off-Base Assumptions, item 2, line 211) that `--output` is an implementation addition not in the spec and calls it "worth noting as an undocumented extension," rating it P2. My review did not flag it. The tension is minor: `--output` is a practical interface detail that affects every handler uniformly (define, interests, mode all accept it in SKILL.md). It belongs in a cross-cutting "Common Options" section of either the spec or SKILL.md, not in per-feature FR lists.

### 3. Handling of `[CLARIFY: ...]` tags in the Type field

functional-typing raises (Missed Opportunities, item 4, lines 196-199) that the interests handler has no explicit instruction for what to do when the Type field contains a `[CLARIFY: ...]` tag from the define handler. This is a valid gap I did not flag. The define handler (SKILL.md line 845 area) can produce `[CLARIFY: best-guess-type — reason]` in the Type field. The interests handler's calibration table (lines 957-962) only lists four concrete types. The heuristic mode detection (line 1149) covers the mode handler's path, but the interests handler's calibration is left unspecified for this case.

However, the severity depends on frequency. The define handler's primary path produces a clean type; `[CLARIFY:]` tags only appear when the problem description is too vague for classification. In practice, the interests handler would likely extract the best-guess type from the tag, but "likely" is not "specified." functional-typing's P1 recommendation to add a note is reasonable.

### 4. Structured vs. prose heuristic signals

My review (Missed Opportunities, item 3) noted that the heuristic detection signals (SKILL.md lines 1149-1155) are prose descriptions and would benefit from a structured signal-to-mode mapping table. functional-typing does not raise this point. This is a stylistic tension: functional-typing's review focuses on spec-to-implementation fidelity (and the signals match the spec's prose at lines 63-68), while my review focuses on operational determinism (prose signals are harder to implement consistently). Both perspectives have merit; neither represents an error.

---

## Safe Agreements

### 1. All 13 functional requirements are substantively covered

Both reviews independently confirm that FR-001 through FR-013 are implemented in SKILL.md with direct, traceable mappings. functional-typing provides line-by-line verdicts for each FR; my review provides an FR-to-implementation mapping table. No FR is missing coverage. The implementation is faithful and additive.

### 2. The implementation is conservative and does not make off-base assumptions

functional-typing explicitly states (Off-Base Assumptions, item 1, line 206): "The SKILL.md implementation is conservative and additive." My review states (Off-Base Assumptions section): "None identified. The implementation faithfully reflects the spec's scope, constraints, and design intent." Both reviews confirm the three spec constraints (no game theory knowledge required, no agents without confirmation, no hard-coded agents/paths) are honored.

### 3. All five success criteria are achievable

Both reviews independently verify SC-001 through SC-005. functional-typing does not explicitly list SC verification but confirms the underlying mechanisms (decision matrix mapping, problem-grounded prompts, schema alignment, override handling, prerequisite routing). My review provides explicit SC-by-SC verification.

### 4. The `Preset` field should be added to the spec schema

functional-typing recommends (P1, item 2): "Add `Preset` field to spec schema." My review's R-1 addresses the downstream concern (preset existence validation). Both reviews agree the Preset field is necessary for the interests-to-config pipeline and that the spec should be updated to include it. The spec's FR-006 already mandates preset support; the schema block is simply missing the corresponding field.

### 5. Prerequisite routing is correct and thorough

functional-typing confirms (Missed Opportunities, item 3, lines 189-193) that SC-005 prerequisite routing is "correctly implemented" and notes the mode handler's three-case dispatch as "a positive addition." My review (Dispatch Table and Routing Verification section) independently confirms all prerequisite routing paths, including the three-case mode handler dispatch. Both reviews agree this exceeds spec requirements in a beneficial way.

### 6. Staleness warning semantics are correct despite minor wording differences

functional-typing rates the wording difference between spec ("interests.md changed") and SKILL.md ("interests.md has changed since conversus.yml was last generated") as P2. My review confirms the implementation is correct (FR-013 satisfied). Both agree the semantics are equivalent and the SKILL.md wording is actually more precise.

### 7. Generated conversus.yml schema aligns with the run engine

functional-typing confirms (FR-010, FR-011) that the generated YAML uses the same schema as hand-crafted configs. My review provides a field-by-field alignment table (Generated Field vs. Run Engine Field) confirming exact matches across all nine fields. Both reviews agree on schema correctness, with my review adding the observation that intentionally omitted advanced fields (rounds, stagnation, validate_templates, prior, arbiter) are correct omissions for a generated minimal config.

### 8. Post-write validation is well-implemented

Both reviews confirm that SKILL.md applies the same validation rules from the run engine to the generated config (SKILL.md lines 1263-1273). functional-typing references this in FR-011; my review notes it in SC-003 verification. Neither review identifies validation gaps in the post-write check itself.

---

## Summary of Recommended Actions

| Item | functional-typing | integration-architect | Agreed Action |
|---|---|---|---|
| `ambiguous` row | P0: add `cooperative` fallback to SKILL.md | Not flagged | P1: update spec to remove `ambiguous` row and reference heuristic detection |
| `Preset` field in spec schema | P1: add to spec | R-1: validate preset existence at post-write | Both: update spec schema + add preset existence check |
| `[CLARIFY:]` tag handling | P1: add note to SKILL.md | Not flagged | P1: add explicit handling note for CLARIFY-tagged Type fields |
| Staleness warning wording | P2: align text | Confirmed correct | P2: optional alignment, SKILL.md wording is more precise |
| `--output` in spec | P2: document | Not flagged | P2: add cross-cutting "Common Options" section |

---

## Referenced Documentation

| Document | Location | Lines Referenced |
|---|---|---|
| functional-typing review | `conversus/specs/008-interests-mode/conversus-review/functional-typing/review.md` | Full document |
| integration-architect review | `conversus/specs/008-interests-mode/conversus-review/integration-architect/review.md` | Full document |
| Spec 008 | `conversus/specs/008-interests-mode/spec.md` | 31-59 (FRs), 44-52 (decision matrix), 63-68 (heuristic signals), 72-87 (schema), 101-105 (constraints) |
| SKILL.md | `conversus/SKILL.md` | 926-1090 (interests handler), 1093-1296 (mode handler), 1041 (Preset field), 1138-1145 (decision matrix + ambiguous routing), 1147-1176 (heuristic + mixed-signal), 1231-1260 (generated YAML) |
