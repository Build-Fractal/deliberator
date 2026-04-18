# Conversus Spec Status

## Taxonomy

Status uses two tiers measuring different dimensions.

### Implementation Tier

Tracks whether a spec's functional requirements (FRs) are represented in SKILL.md.

- **Implementation-complete**: All FRs from this spec are represented in SKILL.md.
- **Partially-complete**: Some FRs are implemented, others remain. Specific gaps listed.
- **Not started**: No SKILL.md representation exists for this spec's features.

Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., "Implementation-complete (core) / Not started (discovery)"). Each component must use a defined implementation-tier label.

### Acceptance Tier

Tracks whether a spec's own acceptance criteria are met.

- **Feature-complete**: All major capabilities are present, but acceptance criteria gaps remain (e.g., missing template instructions, incomplete edge case documentation).
- **Spec-complete**: All acceptance criteria are met. The spec is fully satisfied.
- **Not assessed**: No acceptance criteria have been evaluated.

Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability.

### Interpreting the Two Tiers

The tiers are orthogonal. A spec can be implementation-complete (all FRs in SKILL.md) but only feature-complete (some acceptance criteria gaps remain). Conversely, a spec can be partially-complete in implementation but spec-complete for the subset it covers. Dependencies are also orthogonal — a spec can be implementation-complete while depending on another spec's correctness for composed behavior.

---

## Status

### 001 — Subject Arbitration
**Implementation**: Partially-complete | **Acceptance**: Feature-complete
**Gaps**: FR-023 (output validation — SKILL.md validation logic exists but template-level heading instructions pending), FR-025 (per-FR citation instructions), FR-026 (per-file attribution instructions)
**Notes**: Core Phase 6 execution, config validation, trigger evaluation, failure handling, and structural markers are all implemented. Remaining gaps are template-level behavioral instructions.
**Risk-of-Gap**: Disputes remain unresolved after deliberation; manual post-processing needed to extract actionable decisions from raw synthesis output.
**Effort**: Small — 2 FRs remain (template-level instructions for FR-025 per-FR citation and FR-026 per-file attribution). FR-023 engine logic exists; template instructions pending.

### 002 — Recursive Rounds
**Implementation**: Implementation-complete | **Acceptance**: Spec-complete
**Depends On**: `001-subject-arbitration` (shared dispute-parsing subsystem — stagnation detection FR-021 reuses spec 001's structural markers and heading-based parsing per FR-011)
**Notes**: All 36 FRs represented in SKILL.md. Cross-round synthesis template exists. Runtime correctness of stagnation detection depends on spec 001's parsing subsystem.
**Risk-of-Gap**: Single-pass deliberation only; no iterative convergence improvement. Complex multi-perspective topics may not reach consensus in one round.
**Effort**: None — complete. All 36 FRs implemented. No remaining work.

### 003 — Decision Framework
**Implementation**: Not started | **Acceptance**: Not assessed
**Depends On**: `001-subject-arbitration` (hard dependency for `/conversus arbitrate`), `002-recursive-rounds` (for rounds > 1 in `/conversus converge`), `004-preset-agents` (soft dependency for `/conversus interests` preset suggestions)
**Delivery**: Three phases — Phase A (define/interests/mode, M-effort), Phase B (converge, S-effort), Phase C (arbitrate, M-effort). See spec for details.
**Risk-of-Gap**: Users must manually configure conversus.yml for every deliberation; no guided workflow, interest discovery, or mode selection assistance.
**Effort**: Large — 5 new subcommands (`define`, `interests`, `mode`, `converge`, `arbitrate`), Phase A/B/C incremental delivery, new SKILL.md Subcommand Dispatch section.

### 004 — Preset Agents
**Implementation**: Implementation-complete (core) / Not started (discovery) | **Acceptance**: Feature-complete
**Core (FR-001–021)**: Engine-level preset resolution, composition, validation, caching, arbiter support — all implemented. 18 preset files across 6 categories.
**Discovery (FR-022–024)**: `/conversus presets` list, filter, detail commands — not started. Becomes prerequisite when spec 003 Phase A enters development.
**Gaps**: FR-022 (preset list command), FR-023 (preset filter command), FR-024 (preset detail command) — discovery features not started; acceptance scenarios US-3 through US-6 not testable.
**Risk-of-Gap**: Agent definitions copy-pasted across conversus configs; no reuse mechanism for common agent archetypes. Discovery of available presets requires filesystem browsing.
**Effort**: Small (discovery only) — 3 FRs for `/conversus presets` list, filter, and detail commands. Core engine already complete.

### 005 — P2/P3 Backlog Hardening
**Implementation**: Partially-complete | **Acceptance**: Feature-complete
**Gaps**: FR-007 (heading match semantics — engine validation exists but explicit matching rules pending), FR-011 (dispute-parsing cross-reference — Round Termination Check and Trigger Evaluation still use inline parsing), FR-014 (Phase 4 missing document edge case), FR-015 (Phase 6 overwrite semantics)
**Depends On**: `001-subject-arbitration` (documents spec 001 implementation state), `002-recursive-rounds` (documents spec 002 implementation state), `004-preset-agents` (documents spec 004 implementation state)
**Notes**: 10 of 19 FRs fully implemented, 1 partial (FR-011). Remaining 8 FRs are targeted documentation edits to STATUS.md and SKILL.md. All changes are specification-level — no code, no new files.
**Risk-of-Gap**: Documentation gaps persist in SKILL.md Phase 6 section (heading match semantics, missing document handling, overwrite behavior) and STATUS.md lacks complete cross-spec reference information.
**Effort**: Small — 9 FRs remaining, all documentation edits to 2 existing files (specs/STATUS.md and SKILL.md).

## SKILL.md Structure Plan

Documents how SKILL.md accommodates future spec implementations.

### 002 — Recursive Rounds
**Status**: Already integrated
**Sections**: Rounds configuration (Step 1 config parsing), round termination check, cross-round synthesis template, stagnation detection, multi-round completion report. Dispute-parsing subsystem section handles round-level dispute counting.

### 003 — Decision Framework
**Status**: Needs new sections
**Changes required**:
- New "Subcommand Dispatch" section before Step 1 — routes `/conversus define`, `/conversus interests`, `/conversus mode`, `/conversus converge`, `/conversus arbitrate` to their respective execution flows
- Entry point routing logic to distinguish subcommand invocations from `/conversus run`
- Phase A/B/C orchestration within the `converge` subcommand
- Integration with preset resolution (spec 004) for `/conversus interests` preset suggestions

### 004 — Preset Agents
**Status**: Already integrated
**Sections**: Preset resolution in Step 1 config parsing (single preset, composition, qualified/unqualified names), preset validation, caching, arbiter preset support. 18 preset files across 6 categories in `presets/` directory.

## Shared Subsystems

### Dispute-Parsing Subsystem
**Location**: SKILL.md section "Dispute-Parsing Subsystem"
**Stability**: Stable
**Consumers**: spec 001 (trigger evaluation), spec 002 (stagnation detection)
**Interface**: Input — synthesis file path; Output — boolean (has disputes) for trigger evaluation, integer (dispute count) for stagnation detection. Parsing rules: structural markers primary (`DISPUTES_BEGIN`/`DISPUTES_END`), heading-based fallback per mode.
**Notes**: Stagnation detection (spec 002) does not support structural-marker parsing — it uses only heading-based parsing. Heading-match semantics for the dispute-parsing fallback are not explicitly specified in the subsystem documentation.

### Structural Markers
**Stability**: Stable

- `DISPUTES_BEGIN` / `DISPUTES_END`: Delimit dispute sections in synthesis output. Consumers: spec 001, spec 002, synthesis templates.
- `TEMPLATE_STATUS`: Marks non-production templates as draft. Consumers: spec 005, all arbitration templates.

### Template Conventions
**Stability**: Stable
**Consumers**: All specs
**Interface**: `{VARIABLE}` substitution syntax, mode-specific template selection (`templates/{mode}/`), standardized output sections per mode.

## Cross-Spec Dependencies

### Dependency Graph

```
001 Subject Arbitration ──→ (none — foundational)
002 Recursive Rounds ────→ 001 (shared dispute-parsing subsystem)
003 Decision Framework ──→ 001 (hard: /conversus arbitrate)
                           002 (rounds > 1 in /conversus converge)
                           004 (soft: /conversus interests preset suggestions)
004 Preset Agents ───────→ (none — self-contained engine)
005 P2/P3 Hardening ────→ 001, 002, 004 (documents existing implementations)
```

### Recommended Implementation Order

**001 → 004 → 002 → 003**

- **001 first**: Foundational — dispute parsing, structural markers, and Phase 6 execution are consumed by specs 002 and 003.
- **004 next**: Self-contained engine with no upstream dependencies. Completing 004 before 003 enables preset suggestions in spec 003's `/conversus interests` command.
- **002 after 001**: Rounds and stagnation detection depend on spec 001's dispute-parsing subsystem.
- **003 last**: Depends on all three preceding specs. Three-phase delivery (A/B/C) allows incremental progress.

**Note**: This section summarizes the per-spec "Depends On" fields in the Status section above. Per-spec entries are authoritative; this section provides the cross-cutting view.


---

*Updated: 2026-03-20*

---

*Maintenance obligation: This document MUST be updated when any spec's implementation or acceptance status changes (FR-008a).*
