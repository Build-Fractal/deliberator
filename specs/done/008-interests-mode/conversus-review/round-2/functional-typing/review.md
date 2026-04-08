# Round 2 Review — functional-typing

**Reviewer**: functional-typing
**Round**: 2 of 2
**Target**: `conversus/specs/008-interests-mode/spec.md` and `conversus/SKILL.md` (lines 926-1319)
**Date**: 2026-03-22
**Prior material**: Round 1 synthesis (`round-1/summary/final.md`), arbiter opinions (`round-1/arbitration/resolution.md`)

---

## Executive Summary

Round 1 produced strong convergence: eight items resolved unanimously, three disputes narrowed to language and framing, and four concessions from my own position were warranted. The synthesis and arbiter opinions are well-grounded. I accept the arbiter's reasoning on all three disputes and refine my positions accordingly.

This round focuses on: (1) closing the three remaining disputes with specific language, (2) identifying two missed opportunities that the prior round did not surface, and (3) confirming that no prior concessions should be reversed. The spec and SKILL.md remain substantively sound. No blocking defects.

---

## Alignment

### Dispute 1: CLARIFY-tag handling mechanism — RESOLVED, adopting synthesis + arbiter position

I accept the synthesis recommendation (final.md, K-2) and the arbiter's reasoning (resolution.md, lines 56-68). My Round 1 proposal of `integration` as a "neutral default" was wrong on two independent grounds:

1. **Domain Agnosticism violation** (spec.md line 105). The arbiter correctly identifies that `integration` is the cooperative calibration style, which presupposes all interests must survive. This is a domain-specific assumption, not a neutral fallback. I conceded this partially in Round 1 (Phase 3 revision P1-3) but retained the default as a last-resort path. The arbiter's grounding in the Domain Agnosticism constraint eliminates even the last-resort framing.

2. **Conflation of calibration style with mode selection**. The arbiter's observation (resolution.md, lines 124-125) that the interests handler and mode handler have different input spaces is architecturally precise. Calibration style (adversarial, cooperative, honesty-calibrated, red/blue) governs prompt generation in the interests handler. Mode selection governs deliberation structure in the mode handler. My Round 1 proposal muddled these by importing a mode-level concept (`integration` as cooperative) into a calibration-level decision.

I also accept the arbiter's nuance on integration-architect's "route back to `/conversus define`" position (resolution.md, lines 60-62): the define handler's CLARIFY tag is explicitly a deferred-resolution mechanism (SKILL.md line 889), so making it mandatory contradicts the define handler's own design. The synthesis's "recommend, do not require" language is correct.

**My position for K-2**: Present the four calibration styles inline with the CLARIFY tag's context. Let the user choose. If they decline, recommend `/conversus define` to resolve the tag. Do not default. Do not block. This is exactly the synthesis recommendation.

### Dispute 2: `--output` flag framing — RESOLVED, adopting integration-architect's framing

I withdraw "dual semantics" as the explanatory frame. The arbiter's analogy (resolution.md, lines 83-85) is decisive: calling `--output` "dual semantics" is equivalent to calling `cd` dual because it affects both reads and writes. The flag does one thing — it sets the working directory for all artifact I/O. The co-location of `problem.md`, `interests.md`, and `conversus.yml` in a single directory is not an accident or a side effect; it is the design invariant (SKILL.md lines 949, 1130).

I do note, as the arbiter also observes (resolution.md, line 87), that the flag is *named* `--output`, which creates a naming mismatch with its actual workspace-override behavior. This is a P3 naming concern for a future spec, not a P1 documentation concern for spec 008.

**My position for S-3**: Document `--output` using the workspace-override framing as specified in the synthesis (final.md, S-3). The language "Override the working directory for all artifact I/O" is accurate and sufficient.

### Dispute 3: Generated config completeness framing — RESOLVED, confirming Round 1 position

My Round 1 position aligns with the synthesis and arbiter. The generated config is complete and valid per SC-003 (spec.md line 95) and the Schema Completeness via Defaults principle (SKILL.md lines 57-60). "Starter template" framing is factually inaccurate because the config passes validation and runs successfully without modification.

The arbiter adds a forward-looking argument I had not considered (resolution.md, lines 113-114): if future specs add guided commands for `rounds`, `stagnation`, and `arbiter`, the "starter template" language would need retraction. Writing language that anticipates the system's evolution is better than writing language that will become wrong.

**My position for K-8**: Add the extension-points note as the synthesis specifies (final.md, K-8). Use "extend" or "add" language. Avoid "complete" or "fill in."

### Convergence items C-1 through C-10 — CONFIRMED

All eight convergence points from Round 1 remain settled. I have no corrections, extensions, or reversals for any of them. The actionable changes (S-1 through S-4, K-1 through K-8) as specified in the synthesis are well-grounded and ready for implementation.

### Prior concessions — NO REVERSALS

My four concessions from Round 1 (P0 severity demotion, CLARIFY-tag extract-and-warn withdrawal, staleness warning withdrawal, "specification drift" reframing) all stand. Round 2 context reinforces rather than undermines each one.

---

## Missed Opportunities

### MO-1: Interest count validation boundary — spec says 2-5, SKILL.md does not cap at 5

**Spec reference**: FR-001 (spec.md line 31) specifies "2-5 competing interests."
**SKILL.md reference**: The interests handler's Post-Write Validation (SKILL.md lines 1058-1064) validates "At least 2 interests" (line 1059) but never enforces the upper bound of 5.

This is a gap that none of the three reviewers identified in Round 1. The spec is explicit: "2-5 competing interests." The SKILL.md enforces the lower bound but not the upper. Two possible resolutions:

1. **Add upper-bound validation to SKILL.md** (line 1059): "At least 2 and at most 5 interests are defined." If validation detects more than 5, warn the user and ask whether to proceed or trim.
2. **Relax the spec to "2 or more"**: The upper bound of 5 may be unnecessarily restrictive. Some problems genuinely have more than 5 competing perspectives. If the upper bound is relaxed, the agent-launch cost formula (N^2 + N + 1) should be presented more prominently because cost scales quadratically.

The correct resolution depends on whether the upper bound is a design constraint (to prevent runaway agent costs) or a guideline (a reasonable suggestion that users can override). Given that the agent-launch cost estimate is already a converged recommendation (C-6, K-5), I lean toward resolution 2: relax to "2 or more" in the spec and let the cost estimate serve as the user's throttle. But the divergence should be acknowledged and resolved in either direction.

**Priority**: P2. Not blocking, but the spec and SKILL.md currently disagree on the valid interest count range.

### MO-2: The mode handler does not handle the `(none)` sentinel in Source Documents when mapping to `target`

**Spec reference**: FR-010 (spec.md line 56) requires the generated YAML to contain "target (from problem.md source documents)."
**SKILL.md reference**: The mode handler's Field Mapping (SKILL.md lines 1253-1254) explicitly handles this: "If Source Documents contains `(none)`, ask the user: 'No source documents in problem.md. What files should agents review?'"
**Define handler reference**: SKILL.md line 891 specifies the sentinel: "the Source Documents section should contain `- (none -- no context documents provided)`."

The SKILL.md handles this case, so there is no implementation gap. However, the spec (FR-010) does not acknowledge this edge case at all. The spec assumes Source Documents will always contain valid paths. This is a spec omission rather than an implementation gap — the SKILL.md is more thorough than the spec.

The sentinel text also differs: the define handler writes `(none -- no context documents provided)` (SKILL.md line 891) while the mode handler checks for `(none)` (SKILL.md line 1254). This is likely handled by substring matching in practice, but the inconsistency is worth noting. This connects to the deferred item D-1 (`(none)` sentinel formalization) from the Round 1 synthesis (final.md, lines 352-354).

**Priority**: P3. The SKILL.md already handles this correctly. The spec should eventually acknowledge the edge case for completeness, but this can ride with the D-1 deferred item on sentinel formalization.

---

## Off-Base Assumptions

### OBA-1: The synthesis treats all four problem types as equally likely inputs to heuristic detection

The heuristic mode detection section (SKILL.md lines 1147-1156, spec.md lines 63-68) and the Round 1 convergence on C-1 (replace the `ambiguous` row) assume that when heuristic detection fires, all four modes are equally plausible candidates. But this assumption is not grounded in the system's actual usage patterns.

The heuristic detection fires when the problem type is "ambiguous or missing" (SKILL.md line 1149). This means either: (a) the user skipped `/conversus define` and went straight to `/conversus mode`, or (b) the define handler produced a CLARIFY tag on the Type field. In case (a), the user likely has a quick, informal problem — the type distribution is genuinely unknown. In case (b), the define handler itself was unable to determine the type, which suggests the problem genuinely does not map cleanly to one of the four types.

Neither case supports the assumption that all four modes are equally probable starting positions for heuristic detection. However, this assumption is not *harmful* — presenting all four modes with plain-language descriptions (convergence C-8) is the correct behavior regardless of prior probability because the user makes the final decision. The assumption is off-base but inconsequential. I note it for completeness rather than recommending a change.

---

## Actionable Recommendations

All recommendations incorporate the synthesis and arbiter opinions. Items already converged in Round 1 are marked as confirmed rather than re-argued.

### Spec changes

| ID | Item | Priority | Action | Source |
|---|---|---|---|---|
| S-1 | Replace `ambiguous` row with heuristic detection reference | P1 | As specified in synthesis | Confirmed from C-1 |
| S-2 | Add `Preset` field to interests.md schema | P1 | As specified in synthesis | Confirmed from C-2 |
| S-3 | Add Common Options section documenting `--output` as workspace override | P1 | Use integration-architect's framing per synthesis and arbiter | Dispute 2 resolved |
| S-4 | Rename or footnote Confidence column | P2 | As specified in synthesis | Confirmed from C-11 |
| S-5 | Reconcile interest count range: spec says "2-5", SKILL.md enforces "2+" | P2 | Either add upper bound to SKILL.md or relax spec to "2 or more" | MO-1 (new) |

### SKILL.md changes

| ID | Item | Priority | Action | Source |
|---|---|---|---|---|
| K-1 | Preset existence validation in post-write check | P1 | As specified in synthesis | Confirmed from C-3 |
| K-2 | CLARIFY-tag handling: inline user choice, recommend define, no default | P1 | Per synthesis + arbiter: present four calibration styles, let user choose, recommend `/conversus define` if user declines, no silent default | Dispute 1 resolved |
| K-3 | Draft status behavior: warn and proceed | P1 | As specified in synthesis | Confirmed from C-5 |
| K-4 | Heuristic-is-advisory sentence | P2 | As specified in synthesis | Confirmed from C-4 |
| K-5 | Agent-launch cost estimate at mode confirmation | P2 | As specified in synthesis | Confirmed from C-6 |
| K-6 | Interest-vs-type cross-validation warning | P2 | As specified in synthesis | Confirmed from C-7 |
| K-7 | Zero-signal edge case: present all four modes | P2 | As specified in synthesis | Confirmed from C-8 |
| K-8 | Advanced fields extension-points note | P2 | Use "extend"/"add" language, not "complete"/"fill in" | Dispute 3 resolved |

### Deferred items

| ID | Item | Priority | Source |
|---|---|---|---|
| D-1 | `(none)` sentinel formalization | P2 | Confirmed from synthesis, extended by MO-2 |
| D-2 | Interest deduplication/overlap detection | P3 | Confirmed from synthesis |
| D-3 | `--output` flag rename to `--dir` or `--workspace` | P3 | Arbiter suggestion (resolution.md line 87), new |

---

## Referenced Documentation

- **spec.md** (`conversus/specs/008-interests-mode/spec.md`):
  - Line 31: FR-001, "2-5 competing interests"
  - Lines 44-52: FR-007 decision matrix including `ambiguous` row
  - Line 56: FR-010, generated YAML target field
  - Lines 72-87: `interests.md` schema (missing `Preset` field)
  - Line 95: SC-003, roundtrip validity
  - Lines 103-105: Constraints (no game theory, no agents without confirmation, no hard-coded paths)

- **SKILL.md** (`conversus/SKILL.md`):
  - Lines 57-60: Run engine defaults (rounds, iterations, stagnation, validate_templates)
  - Line 889: Define handler's deferred resolution design for CLARIFY tags
  - Line 891: Source Documents `(none)` sentinel text
  - Lines 949, 1130: `--output` flag read/write co-location
  - Lines 957-962: Interest Generation calibration table
  - Lines 1058-1064: Post-Write Validation for interests handler (enforces "at least 2" only)
  - Lines 1147-1156: Heuristic mode detection
  - Lines 1158-1176: Mixed-signal handling
  - Lines 1253-1254: Mode handler Source Documents `(none)` handling
  - Lines 1262-1273: Post-Write Validation for mode handler
  - Lines 1304-1307: Agent-launch cost formula

- **Round 1 synthesis** (`round-1/summary/final.md`):
  - Lines 113-175: Convergence items C-1 through C-10
  - Lines 199-245: Disputes 1-3 and synthesis recommendations
  - Lines 251-350: Actionable changes S-1 through S-4, K-1 through K-8

- **Arbiter opinions** (`round-1/arbitration/resolution.md`):
  - Lines 56-68: Dispute 1 opinion — synthesis recommendation is correct, `integration` default eliminated by Domain Agnosticism
  - Lines 60-62: Define handler's deferred resolution as design choice
  - Lines 83-85: Dispute 2 opinion — `cd` analogy for workspace-override framing
  - Line 87: `--output` naming mismatch noted for future spec
  - Lines 104-110: Dispute 3 opinion — Schema Completeness via Defaults settles the framing
  - Lines 113-114: Forward-looking argument against "starter template" language
  - Lines 124-125: Interests handler and mode handler have different input spaces
