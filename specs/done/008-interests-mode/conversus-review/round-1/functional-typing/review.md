# Functional-Typing Review: Spec 008 Implementation in SKILL.md

**Reviewer**: functional-typing (structural correctness & specification compliance)
**Target**: `conversus/SKILL.md` (Interests and Mode handlers) vs `conversus/specs/008-interests-mode/spec.md`
**Date**: 2026-03-22

---

## Executive Summary

The SKILL.md implementation is a faithful and substantially expanded translation of spec 008. All 13 functional requirements (FR-001 through FR-013) have corresponding handler sections, and the implementation adds operational detail the spec intentionally leaves abstract (input forms, prerequisite checks, post-write validation, reporting). Two structural gaps exist: (1) the decision matrix in SKILL.md omits the spec's `ambiguous` row, and (2) the `interests.md` schema in SKILL.md adds a `Preset` field not present in the spec schema. Neither gap causes runtime incompatibility, but both represent specification drift that should be resolved in one direction or the other.

---

## Alignment

### FR-001: Read problem.md and suggest 2-5 interests with name, perspective, prompt, docs

**Spec** (line 31): "MUST read `problem.md` and suggest 2-5 competing interests with: name, perspective (one sentence), identity prompt, and suggested documentation paths."

**SKILL.md** (line 955): "Read the Type field from `problem.md` and generate 2-5 interests calibrated to the problem type"

**SKILL.md** (lines 1034-1040): Schema shows `### <interest-name>`, `**Perspective**`, `**Prompt**`, and `**Docs**` fields.

**Verdict**: Fully covered. The four required fields (name, perspective, prompt, docs) are present in both the Interest Generation section and the output schema.

---

### FR-002: Prompts calibrated to problem type

**Spec** (lines 32-36): Four calibration styles — selection/adversarial, integration/cooperative, scoping/honesty-calibrated, stress-test/red-blue.

**SKILL.md** (lines 957-962): Interest Generation table provides all four rows with matching calibration styles and example prompt text.

| Spec Calibration | SKILL.md Table Row |
|---|---|
| `selection`: adversarial (line 33) | `selection`: "Adversarial — each interest advocates for its alternative" (line 959) |
| `integration`: cooperative (line 34) | `integration`: "Cooperative — each interest advocates for its needs while seeking alignment" (line 960) |
| `scoping`: honesty-calibrated (line 35) | `scoping`: "Honesty-calibrated — each interest declares capabilities and deferrals" (line 961) |
| `stress-test`: red/blue (line 36) | `stress-test`: "Red/blue roles — attackers and defenders" (line 962) |

**Verdict**: Fully covered. One-to-one mapping with concrete prompt templates.

---

### FR-003: User MAY add explicit interests via --add

**Spec** (line 37): "User MAY add explicit interests via `--add <name>`. The agent generates a prompt and asks for docs."

**SKILL.md** (line 948): "`--add <name>` — adds a named interest to the suggestions. The agent generates a prompt for it and asks the user for documentation paths. May be repeated: `--add security --add performance`."

**SKILL.md** (lines 968-970): "For `--add <name>` interests, generate a prompt following the same calibration rules and ask the user: 'What perspective does '{name}' represent?' / 'What documentation should this interest have access to?'"

**Verdict**: Fully covered. Implementation adds multi-add support (`--add security --add performance`) which is a reasonable extension.

---

### FR-004: Ungrounded agents marked with [NEEDS DOCS]

**Spec** (line 38): "Ungrounded agents (no docs) MUST be marked with `[NEEDS DOCS: suggest what to provide]` and a warning that ungrounded agents produce weaker arguments."

**SKILL.md** (lines 974-981): Ungrounded Agent Warning section specifies the exact marker format `[NEEDS DOCS: <suggestion>]` and the warning text: "Interest '{name}' has no grounding documents. Ungrounded agents produce weaker arguments..."

**SKILL.md** (line 1050): Schema rules specify: "If empty, use `- (none)` and include the `[NEEDS DOCS: ...]` tag after it."

**Verdict**: Fully covered.

---

### FR-005: Existing interests.md — present and ask to add/remove/modify

**Spec** (line 39): "If `interests.md` already exists, the agent MUST present current interests and ask to add, remove, or modify."

**SKILL.md** (lines 996-1004): Existing File Check section implements all three operations (Add, Remove, Modify) with specific interaction patterns for each.

**Verdict**: Fully covered.

---

### FR-006: Preset matching

**Spec** (line 40): "Interests MAY reference presets from spec 004's preset engine. When a preset matches a suggested interest, the agent notes it."

**SKILL.md** (lines 983-992): Preset Matching section implements preset search with user-facing note: "Interest '{name}' matches the `{category/preset-name}` preset. Use the preset?"

**Verdict**: Fully covered. Implementation adds merge semantics for documentation paths (line 990: "merge documentation paths") which is a reasonable detail.

---

### FR-007: Decision matrix — mode recommendation

**Spec** (lines 44-52): Decision matrix with 5 rows (selection, integration, scoping, stress-test, ambiguous).

**SKILL.md** (lines 1138-1144): Decision matrix with 4 rows (selection, integration, scoping, stress-test). Adds a "Plain-Language Description" column.

**FINDING — Missing `ambiguous` row**: The spec's decision matrix (line 52) includes:

> | ambiguous | cooperative | Low — present alternatives |

The SKILL.md decision matrix (lines 1138-1144) does NOT include an `ambiguous` row. Instead, SKILL.md handles the ambiguous case through a separate mechanism: line 1145 states "When the problem type is unset or ambiguous, use heuristic mode detection" which routes to the Heuristic Mode Detection section (lines 1147-1156).

This is a structural divergence. The spec prescribes a default fallback (cooperative, Low confidence), while SKILL.md replaces that default with signal-based inference. The SKILL.md approach is arguably more sophisticated, but it does NOT guarantee the spec's stated default of `cooperative` for ambiguous types. The heuristic detection could recommend any mode depending on signal density.

**Verdict**: Partially covered. The ambiguous case is handled, but the guaranteed default of `cooperative` from the spec is not preserved. If heuristic detection produces no clear winner, the mixed-signal handling (line 1160) asks the user to choose rather than defaulting to `cooperative`.

---

### FR-008: Mixed signals — present top 2 candidates

**Spec** (line 54): "When signals are mixed, MUST present the top 2 candidates with a plain-language trade-off comparison and ask the user to choose."

**SKILL.md** (lines 1158-1176): Mixed-Signal Handling section presents "Option A" and "Option B" with descriptions, signal explanations, and user choice prompt.

**Verdict**: Fully covered.

---

### FR-009: User MAY override recommendation

**Spec** (line 55): "User MAY override the recommendation. The system explains the trade-off and regenerates."

**SKILL.md** (lines 1178-1191): User Override section handles `--mode <mode-name>` and interactive override, with trade-off explanation and validation.

**Verdict**: Fully covered.

---

### FR-010: Output valid conversus.yml with required fields

**Spec** (line 56): "Output MUST be a valid `conversus.yml` containing: mode, target (from problem.md source documents), output directory, all agents from interests.md with prompts and docs, iterations (default 1)."

**SKILL.md** (lines 1233-1260): Generated YAML structure includes all required fields: `mode`, `target` (from problem.md Source Documents), `output` (default `conversus-output/`), `iterations: 1`, and `agents` mapped from interests.md.

**Verdict**: Fully covered.

---

### FR-011: Generated YAML uses same schema as hand-crafted configs

**Spec** (line 57): "Generated YAML MUST use the exact same schema as hand-crafted configs. No schema extensions."

**SKILL.md** (line 1231): "The file MUST use the exact same schema as hand-crafted configs (as defined in the Run: Execution Step 1 section). No schema extensions."

**Verdict**: Fully covered, verbatim match.

---

### FR-012: Existing conversus.yml — show diff and ask

**Spec** (line 58): "If `conversus.yml` already exists, show what would change and ask before overwriting."

**SKILL.md** (lines 1212-1227): Existing File Check section reads the existing config, shows a change summary (mode, agent count, target), and asks "Overwrite with the new configuration?" with "Never silently overwrite" guarantee.

**Verdict**: Fully covered.

---

### FR-013: Staleness warning for interests.md changes

**Spec** (line 59): "If `interests.md` has changed since the last `conversus.yml` was generated, warn."

**SKILL.md** (lines 1117-1122): Staleness Warning section uses modification time comparison and emits: "interests.md has changed since conversus.yml was last generated. Your config may be out of date."

**Verdict**: Fully covered. The spec's example message says "interests.md changed. Your conversus.yml may be out of date." while SKILL.md says "interests.md has changed since conversus.yml was last generated. Your config may be out of date." Minor wording difference, same semantics.

---

## Missed Opportunities

### 1. The `ambiguous` row is silently replaced, not explicitly superseded

The spec's decision matrix (line 52) defines a concrete default for the ambiguous case: `cooperative` at `Low` confidence. The SKILL.md replaces this with heuristic detection (lines 1147-1156) and mixed-signal handling (lines 1158-1176), which is more capable but does not preserve the spec's guaranteed fallback.

**Recommendation**: Either (a) add a fallback in SKILL.md's heuristic detection: "If no signals are detected for any mode, default to `cooperative` with Low confidence (per spec 008 FR-007)," or (b) explicitly update the spec to remove the `ambiguous` row and replace it with a reference to heuristic detection. The current state is implicit disagreement.

### 2. `interests.md` schema diverges: `Preset` field

The spec's `interests.md` schema (lines 72-87) defines these fields per interest: Perspective, Prompt, Docs, and Role (stress-test only).

The SKILL.md schema (lines 1026-1046) adds a field not in the spec:
- Line 1041: `- **Preset**: <category/preset-name>  <!-- only if a preset was used -->`

The spec's FR-006 (line 40) says interests "MAY reference presets" but the schema block (lines 72-87) does not include a `Preset` field. This means the SKILL.md schema is a superset of the spec schema.

**Recommendation**: Update the spec's `interests.md` schema to include the optional `Preset` field, since FR-006 clearly intends preset integration. This is a spec omission, not an implementation error.

### 3. SC-005 prerequisite routing is implemented but placed differently

**Spec SC-005** (line 97): "When `problem.md` is missing and user runs `/conversus interests`, the agent routes them to `/conversus define` first."

**SKILL.md** (lines 932-939): The Missing Prerequisite Check section handles this: "No problem.md found. Run `/conversus define` first to create a problem definition." and "Stop processing."

This is correctly implemented. However, the SKILL.md adds an additional prerequisite check in the mode handler (lines 1101-1113) with a three-case dispatch (no interests.md + no problem.md, no interests.md + yes problem.md, no problem.md + yes interests.md) that the spec only mentions implicitly. This is a positive addition.

### 4. No explicit handling of the `ambiguous` problem type value in type field

The Define handler (line 845) can mark a type as ambiguous via `[CLARIFY: ...]` tags. However, the Interests handler's Interest Generation table (lines 957-962) only lists four concrete types. There is no explicit instruction for what happens when the Type field in `problem.md` contains a `[CLARIFY: ...]` tag. The handler would need to either use the "best guess" type mentioned in the tag or fall back to a default calibration style.

**Recommendation**: Add a note in the Interest Generation section specifying behavior when the Type field contains a `[CLARIFY: ...]` tag — likely use the best-guess type from within the tag, or ask the user to resolve it before proceeding.

---

## Off-Base Assumptions

### 1. The implementation does NOT make off-base assumptions about the spec

The SKILL.md implementation is conservative and additive. Every extension beyond the spec (prerequisite checks, post-write validation, reporting format, input forms) is operationally necessary detail that the spec intentionally leaves to the implementation. The implementation does not contradict any spec requirement.

### 2. Minor: `--output` flag is an implementation addition, not a spec requirement

The spec does not mention an `--output` flag for either command. SKILL.md adds it (lines 949, 1130) as a practical convenience. This is reasonable and does not conflict with the spec, but it is worth noting as an undocumented extension.

---

## Actionable Recommendations

### P0 — Must fix before shipping

1. **Add `ambiguous` fallback to heuristic detection (SKILL.md ~line 1156)**: After the heuristic signal scoring, add: "If no mode has detectable signals, default to `cooperative` with Low confidence, per the spec 008 decision matrix." This preserves the spec's guaranteed fallback while keeping the more sophisticated signal detection. Alternatively, update the spec (line 52) to remove the `ambiguous` row and replace it with a reference to heuristic detection — but the two documents must agree.

### P1 — Should fix

2. **Add `Preset` field to spec schema (spec.md ~line 87)**: Add `- **Preset**: <category/preset-name>  <!-- only if a preset was used -->` to the spec's `interests.md` schema block. FR-006 already mandates preset support; the schema should reflect it.

3. **Clarify CLARIFY-tagged Type handling (SKILL.md ~line 955)**: Add a note: "If the Type field contains a `[CLARIFY: ...]` tag, extract the best-guess type from the tag text and use it for calibration. Warn the user that the problem type is unconfirmed."

### P2 — Nice to have

4. **Align staleness warning text**: The spec (line 59) says "interests.md changed." while SKILL.md (line 1120) says "interests.md has changed since conversus.yml was last generated." Consider using identical text in both documents for traceability.

5. **Document `--output` in spec**: If `--output` is to be a stable interface, add it to the spec's FR list or at minimum to a "Supported Options" section.

---

## Referenced Documentation

| Document | Location | Lines Referenced |
|---|---|---|
| Spec 008 | `conversus/specs/008-interests-mode/spec.md` | 31-59 (FRs), 44-52 (decision matrix), 63-68 (heuristic signals), 72-87 (interests.md schema), 92-97 (success criteria) |
| SKILL.md | `conversus/SKILL.md` | 926-1090 (Interests handler), 1093-1296 (Mode handler), 1138-1144 (decision matrix), 1026-1046 (interests.md schema), 1147-1156 (heuristic detection), 1233-1260 (YAML output) |
| SKILL.md Define handler | `conversus/SKILL.md` | 834-850 (problem type classification), 854-901 (problem.md schema and validation) |
