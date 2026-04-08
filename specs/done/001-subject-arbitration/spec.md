# Feature Specification: Subject Arbitration (Phase 6)

**Feature Branch**: `001-subject-arbitration`
**Created**: 2026-03-19
**Status**: Draft
**Input**: Add an optional Phase 6 to the conversus framework where the subject of the review acts as a binding arbiter for unresolved disputes.

## Motivation

### The Problem

In cooperative mode, Phase 5 (synthesis) identifies remaining disputes but does not resolve them. The synthesizer is explicitly neutral — it documents convergence, assesses which positions the evidence better supports, and recommends resolution paths, but it does not make binding decisions. When disputes survive the full 5-phase process (review → cross-review → revision → disputes → synthesis), there is no mechanism to break deadlocks.

The Prisoner's Dilemma and Red-Blue modes already have binding decisions in Phase 5 — trust-scored responsibility maps and risk verdicts respectively. Cooperative mode is the only mode where Phase 5 abstains from binding rulings.

### The Observed Gap

In a real-world case (speckit-orchestrator), two cooperative-mode conversus runs (spec-level and plan-level, 30 total artifacts, 3 agents) left 9 disputes unresolved. The three agents (APM, spec-kit, gh-aw) represented external tool perspectives — packaging, extension system, CI. None represented the orchestrator's own operational needs. A 4th agent — the orchestrator itself — was introduced ad hoc as a post-conversus arbiter, grounding all rulings in its 7 constitution principles. It resolved all 5 remaining plan-level disputes with clear, actionable decisions.

### The Insight

The subject of a review has information and interests that external reviewers lack. In classical game theory, this maps to **interested-party arbitration** (a variant of the principal-agent problem viewed from the principal's side). The 5-phase process is a mechanism that forces honest preference revelation through cross-review pressure. Subject arbitration is the mechanism designer evaluating those revealed preferences against the system's actual requirements.

This interest is a **strength**, not a weakness, when properly constrained. The constraint mechanism: a required grounding document (constitution, design principles, requirements) that makes the arbiter's decision framework legible and forces citation in every ruling.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Cooperative Mode Dispute Resolution (Priority: P1)

As a developer running a cooperative-mode conversus, I want unresolved disputes from Phase 4 to be resolved by the subject of the review, so that the deliberation produces binding decisions instead of open questions.

**Acceptance Scenarios**:

1. **Given** a `conversus.yml` with `mode: cooperative` and an `arbiter` field, **When** Phase 5 synthesis identifies remaining disputes (the "Remaining Disputes" section contains at least one dispute entry), **Then** Phase 6 runs: the arbiter agent reads all Phase 4 disputes and the Phase 5 synthesis, issues binding decisions for each unresolved dispute grounded in the declared `grounding` document, and writes the resolution to `{output}/arbitration/resolution.md`.

2. **Given** a cooperative-mode conversus where Phase 5 synthesis has no remaining disputes (all positions converged), **When** `trigger: disputes_remain` is configured, **Then** Phase 6 does NOT run. The conversus completes after Phase 5. The output directory does not contain an `arbitration/` subdirectory.

3. **Given** a `conversus.yml` with `trigger: always`, **When** Phase 5 completes regardless of dispute count, **Then** Phase 6 runs. If no disputes remain, the arbiter produces a "subject endorsement" document confirming the synthesis positions.

4. **Given** a `conversus.yml` without an `arbiter` field, **When** the conversus runs, **Then** the process completes after Phase 5 exactly as it does today. No Phase 6, no behavioral change. Full backward compatibility.

5. **Given** a Phase 6 arbitration, **When** the arbiter issues a binding decision, **Then** every decision MUST cite at least one specific principle, requirement, or constraint from the `grounding` document. Decisions without grounding citations are invalid.

6. **Given** a Phase 6 arbitration, **When** the arbiter considers a dispute, **Then** it MUST NOT introduce new recommendations that no agent proposed. It resolves existing disputes only — it does not add to the deliberation record.

7. **Given** a completed Phase 6, **When** the final report is printed, **Then** it includes the arbitration output path in the directory listing and notes "Arbitration: {N} disputes resolved" in the summary.

---

### User Story 2 — Arbiter Configuration (Priority: P1)

As a developer configuring a conversus run, I want to define the subject arbiter in the `conversus.yml`, so that the system knows who the arbiter is, what it's grounded in, and when it should run.

**Acceptance Scenarios**:

1. **Given** this `conversus.yml` configuration:
   ```yaml
   arbiter:
     name: my-system
     prompt: |
       You ARE the system being reviewed...
     docs:
       - .specify/memory/constitution.md
     grounding: .specify/memory/constitution.md
     trigger: disputes_remain
   ```
   **When** the config is parsed, **Then** validation succeeds and the arbiter is registered for conditional Phase 6 execution.

2. **Given** an `arbiter` field without a `grounding` field, **When** validation runs, **Then** it fails with error: "arbiter.grounding is required — the arbiter must declare its decision framework."

3. **Given** an `arbiter` field with a `grounding` path that does not exist on disk, **When** validation runs, **Then** it fails with error: "arbiter.grounding path does not exist: {path}".

4. **Given** an `arbiter.trigger` value that is not `disputes_remain` or `always`, **When** validation runs, **Then** it fails with error: "arbiter.trigger must be 'disputes_remain' or 'always'".

5. **Given** an `arbiter` field on a non-cooperative mode (`winner-take-all`, `prisoners-dilemma`, `red-blue`), **When** validation runs, **Then** it fails with error: "arbiter is only supported in cooperative mode (current mode: {mode})."

---

### User Story 3 — Arbitration Template (Priority: P2)

As a developer creating a custom conversus mode, I want the arbitration template to follow the same conventions as Phase 1-5 templates, so that mode extensibility is preserved.

**Acceptance Scenarios**:

1. **Given** the conversus templates directory, **When** a developer looks for the arbitration template, **Then** it exists at `templates/cooperative/arbitration.md` following the same naming convention as other phase templates.

2. **Given** the arbitration template, **When** variables are substituted, **Then** it uses the same `{VARIABLE}` syntax as all other templates, plus arbitration-specific variables (`{ARBITER_NAME}`, `{ARBITER_PROMPT}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`).

3. **Given** a future mode that wants arbitration, **When** a developer creates `templates/{new-mode}/arbitration.md`, **Then** the engine picks it up automatically — no code changes needed beyond the template.

---

### Edge Cases

- What happens when the grounding document is very large (>50K tokens)? The arbiter prompt should instruct the agent to read the grounding document, not inline it. The template uses `{GROUNDING_PATH}` as a file reference, not as inlined content.
- What happens when the arbiter's ruling contradicts a unanimous convergence point from Phase 4? The arbiter SHOULD NOT override unanimous convergence — it resolves disputes (contested positions), not re-litigate agreements. The template must instruct: "Do not overturn positions where all agents converged. Your scope is the Remaining Disputes section only."
- What happens when one of the Phase 4 dispute documents is missing or empty? Phase 6 should still run — it reads whatever dispute documents exist. An empty disputes document means that agent has no remaining disputes (a valid outcome).
- What happens when the arbiter declares it cannot resolve a dispute? The arbiter should write: "UNRESOLVED — insufficient information to make a grounded decision. Requires: [specific information needed]." This is a valid outcome — not every dispute must be resolved.

## Requirements *(mandatory)*

### Functional Requirements

#### Schema Extension

- **FR-001**: The `conversus.yml` schema MUST support an optional top-level `arbiter` field at the same level as `mode`, `target`, `output`, and `agents`.
- **FR-002**: The `arbiter` field MUST accept the following sub-fields:
  - `name` (required, string): Identifier for the arbiter agent
  - `prompt` (required, string): Identity/role prompt for the arbiter
  - `docs` (optional, list of strings): Documentation paths for grounding the arbiter's perspective
  - `grounding` (required, string): Path to the decision framework document (constitution, principles, requirements)
  - `trigger` (required, enum): `disputes_remain` or `always`
- **FR-003**: Validation MUST reject `arbiter` configurations that are missing `grounding` or `trigger` fields.
- **FR-004**: Validation MUST reject `arbiter` on non-cooperative modes with a clear error message.
- **FR-005**: The `arbiter` field MUST be fully optional. Omitting it preserves exact Phase 1-5 behavior with no changes.

#### Phase 6 Execution

- **FR-006**: When `trigger: disputes_remain`, Phase 6 MUST run only if the Phase 5 synthesis contains at least one entry in its "Remaining Disputes" section.
- **FR-007**: When `trigger: always`, Phase 6 MUST run after Phase 5 regardless of dispute count.
- **FR-008**: Phase 6 MUST execute as a single foreground agent (same as Phase 5), not in background.
- **FR-009**: Phase 6 MUST run after Phase 5 completes. It reads the synthesis output as input.
- **FR-010**: The Phase 6 agent MUST be dispatched with the arbitration template from `templates/{mode}/arbitration.md`, with all variables substituted.

#### Trigger Evaluation

- **FR-011**: The `disputes_remain` trigger MUST be evaluated by parsing the Phase 5 synthesis output file. The primary mechanism is structural HTML markers: the engine looks for content between `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->` markers and checks whether at least one dispute entry exists within that range. If markers are not present, the engine MUST fall back to heading-based parsing (checking whether the `### Remaining Disputes` heading contains at least one `**Dispute:` entry).
- **FR-012**: If the synthesis file cannot be parsed or the heading is not found, the trigger MUST default to `true` (run Phase 6) as a safety measure — better to run the arbiter unnecessarily than to skip it when disputes exist.

#### Arbitration Template

- **FR-013**: The arbitration template MUST be located at `templates/cooperative/arbitration.md` following the existing template naming convention.
- **FR-014**: The template MUST use the standard `{VARIABLE}` substitution syntax, supporting all standard variables plus:
  - `{ARBITER_NAME}` — from config `arbiter.name`
  - `{ARBITER_PROMPT}` — from config `arbiter.prompt`
  - `{ARBITER_DOCS}` — newline-separated list of doc paths from `arbiter.docs`
  - `{GROUNDING_PATH}` — from config `arbiter.grounding`
  - `{SYNTHESIS_PATH}` — absolute path to Phase 5 output (`{output}/summary/final.md`)
  - `{ALL_DISPUTES}` — existing variable (Phase 4 dispute paths)
  - `{REMAINING_DISPUTES}` — content extracted from between the `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->` markers in the Phase 5 synthesis, making the arbiter's dispute scope machine-defined
  - `{TARGET_FILES}` — existing variable (all target file paths)
  - `{AGENT_NAMES}` — existing variable (comma-separated participant names)
  - `{OUTPUT_PATH}` — `{output}/arbitration/resolution.md`
- **FR-015**: The template MUST instruct the arbiter to:
  1. Read the grounding document first (decision framework)
  2. Read the Phase 5 synthesis (neutral assessment of disputes)
  3. Read all Phase 4 dispute documents (each agent's final position)
  4. For each unresolved dispute: issue a binding decision with grounding citation, explain rejected positions, and list concrete changes required
  5. NOT introduce new recommendations. Observations noted in the Confidence Assessment section, explicitly labeled as non-binding, are not new recommendations — they are permitted as long as they are confined to that section and do not prescribe specific changes
  6. NOT overturn unanimous convergence points

#### Output

- **FR-016**: Phase 6 output MUST be written to `{output}/arbitration/resolution.md`.
- **FR-017**: The output directory `{output}/arbitration/` MUST be created by the engine before dispatching the arbiter.
- **FR-018**: The output MUST contain these sections: Process Note (what triggered arbitration), Decision Framework (grounding document summary), Binding Decisions (per dispute), Summary of Changes Required.
- **FR-019**: Every binding decision MUST include: the dispute (with citations to Phase 4), the ruling, the rationale (citing the grounding document), and rejected positions with reasons.
- **FR-024**: The `docs` field provides read-only context only. Only the `grounding` document MAY be cited as authority in binding decisions. Citations to `docs` entries are permitted for factual context but MUST NOT serve as the sole basis for a ruling.
- **FR-025**: When target documents contain numbered requirements (e.g., FR-xxx, SC-xxx), the arbiter's Required Changes MUST cite specific identifiers rather than making vague references. The template MUST instruct the arbiter to reference target-document identifiers in binding decisions.
- **FR-026**: When multiple target files exist, each binding decision's Required Changes MUST specify which file is affected. The template MUST instruct the arbiter to attribute changes to specific files.

#### Reporting

- **FR-020**: The final conversus report (Step 5 in SKILL.md) MUST include the arbitration output in the directory listing when Phase 6 ran.
- **FR-021**: The report MUST include "Arbitration: {N} disputes resolved" when Phase 6 ran, or indicate "Arbitration: skipped (no disputes)" when the trigger was not met.

#### Failure Semantics

- **FR-022**: If the arbiter agent fails (timeout, crash, or malformed output), Phase 5 output MUST be the terminal state. A diagnostic warning MUST be emitted. No partial `resolution.md` MUST be written. The Phase 1-5 record MUST NOT be invalidated by a Phase 6 failure.

#### Output Validation

- **FR-023**: After Phase 6 completes, the engine MUST validate that `resolution.md` contains the required section headings defined in FR-018. If validation fails, the engine MUST emit a warning flagging the malformed output. Malformed output MUST NOT be silently accepted, but the file MUST still be written (the warning is informational, not blocking).
- **FR-027**: Re-running Phase 6 MUST overwrite any existing `resolution.md`. The engine MUST NOT preserve previous arbitration output. Each Phase 6 execution produces a complete, self-contained resolution. Prior resolutions should be committed to version control before re-running if preservation is desired.

### Key Entities

- **Arbiter**: The subject of the review, configured in `conversus.yml`. Has a name, prompt, docs, grounding document, and trigger condition. Not a regular participant — does not participate in Phases 1-4. Runs only in Phase 6, conditionally.
- **Grounding Document**: The arbiter's declared decision framework (constitution, design principles, requirements). Every ruling must cite it. This is the transparency mechanism that makes interested-party arbitration legitimate.
- **Binding Decision**: A ruling on an unresolved dispute. Contains: the dispute reference, the decision, the grounding citation, rejected positions with reasons, and required changes. Binding means no further deliberation — the decision is final for this conversus run.
- **Trigger**: The condition under which Phase 6 executes. `disputes_remain` checks the synthesis output. `always` runs unconditionally.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A cooperative-mode conversus with an `arbiter` field and unresolved disputes produces a `{output}/arbitration/resolution.md` file with binding decisions for every dispute in the synthesis's "Remaining Disputes" section.
- **SC-002**: Every binding decision in the resolution file contains at least one explicit citation to the grounding document. Zero unsupported rulings.
- **SC-003**: A cooperative-mode conversus with an `arbiter` field and zero remaining disputes does NOT produce an `arbitration/` directory when `trigger: disputes_remain`.
- **SC-004**: A conversus configuration without an `arbiter` field produces identical output to the current system — full backward compatibility.
- **SC-005**: Validation rejects `arbiter` on non-cooperative modes, missing `grounding`, and missing `trigger` with clear error messages.
- **SC-006**: The arbitration template follows the same `{VARIABLE}` substitution pattern as all 20 existing templates — no special-case parsing.
- **SC-007**: Phase 6 reads all Phase 4 disputes AND the Phase 5 synthesis before producing output — verified by the template requiring citations to both.

## Assumptions

- The conversus framework is running in an environment with the Agent tool available (Claude Code or equivalent).
- Phase 5 synthesis templates MUST include `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` structural markers around the remaining disputes section. The `### Remaining Disputes` heading convention is retained as a backward-compatible fallback.
- The grounding document exists on disk at the configured path before the conversus run starts.
- The grounding document is assumed stable for the duration of the conversus run. Concurrent modifications to the grounding document during a run may produce inconsistent rulings and should be avoided.
- Subject arbitration is meaningful when the arbiter has decision authority over the target artifact, constrained by a grounding document. The common case is that the subject has integration knowledge that individual reviewers lack, but decision authority — not information asymmetry — is the necessary condition. If the arbiter lacks decision authority over the target, arbitration has no binding force regardless of information advantage.

## Constraints

- Cooperative mode only for initial release. Prisoner's Dilemma and Red-Blue extensions change game dynamics fundamentally and need separate analysis.
- The arbiter is NOT a participant in Phases 1-4. It does not produce a review, is not cross-reviewed, does not revise, and does not file disputes. It is a post-synthesis decision-maker.
- The arbiter MUST NOT introduce new recommendations. It resolves existing disputes — it does not add to the deliberation record.
- The arbiter MUST NOT overturn unanimous convergence points. Its scope is the "Remaining Disputes" section only.
- The `grounding` field is required, not optional. An arbiter without a declared decision framework is unconstrained and produces arbitrary rulings. The grounding document is the key integrity mechanism.
- The arbitration template lives in the mode's template directory (`templates/cooperative/arbitration.md`), not in a global location. If other modes adopt arbitration in the future, they get their own templates.
- Total agent launches increases from N² + N + 1 to N² + N + 2 (one additional foreground agent for Phase 6).
- Non-cooperative mode arbitration templates (Prisoner's Dilemma, Red-Blue) are draft/experimental. They MUST NOT be activatable in v1. Activation requires a separate game-dynamics analysis spec per mode. Templates MAY exist in `templates/{mode}/arbitration.md` with a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker but MUST be filtered out by the engine at runtime.

## Implementation Guidance

This section is non-normative. It provides recommendations for implementors and template authors.

### Spec-Kit Project Convention

When the target of a conversus is a spec-kit project, `arbiter.grounding` SHOULD be the constitution path (e.g., `.specify/memory/constitution.md`). The constitution serves as the natural decision framework since it defines the project's foundational principles and constraints.

### Grounding Document Requirements

Grounding documents should meet the following minimum content expectations:
- Contain numbered or otherwise identifiable principles, requirements, or constraints that can be cited in rulings
- Be self-contained enough that a reader can evaluate whether a citation supports the ruling
- Avoid vague aspirational language that could justify any decision

Recommended structure: a numbered list of principles or requirements, each with a clear scope statement. Anti-patterns include: grounding documents that are purely procedural (how to contribute), documents that contain no citable constraints, and documents that are too broad to constrain any decision.

### Template Authoring Contract

Phase 6 templates consume the following Phase 5 output elements:
- The synthesis file at `{SYNTHESIS_PATH}` (the full Phase 5 output)
- The remaining disputes content extracted via `{REMAINING_DISPUTES}` (between structural markers)
- All Phase 4 dispute files via `{ALL_DISPUTES}`
- Target files via `{TARGET_FILES}`

Template authors MUST preserve these invariants:
- The arbiter prompt must instruct the agent to read the grounding document before making decisions
- The output must be directed to `{OUTPUT_PATH}`
- The template must not instruct the arbiter to produce output that contradicts FR-015 (the six behavioral constraints)
- The engine validates output against FR-018 section headings after Phase 6 completes

### Structured Output Schema (Deferred)

The following fields are defined for future structured extraction from arbitration output. The production mechanism (arbiter-produced YAML, engine extraction from prose, or sidecar file) is deferred to a future version. The schema is defined now to guide template design:
- `dispute_id`: Identifier for the dispute being resolved
- `ruling_type`: One of `accept`, `reject`, `modify`, `unresolved`
- `grounding_citation`: Specific principle/requirement cited from the grounding document
- `required_changes`: List of concrete changes required
- `affected_target_file`: Which target file the changes apply to (per FR-026)
- `confidence_level`: Arbiter's confidence in the ruling

### Trigger Quorum (Future)

A future iteration MAY introduce a `trigger: quorum` option that runs Phase 6 only when N or more disputes remain. This is explicitly deferred from v1. The `trigger` enum is limited to `disputes_remain` and `always` for the initial release.

## Deliberation History

This spec has been through 4 conversus cycles spanning 100+ independent agent dispatches. Each cycle produced improvements that were integrated into the spec and SKILL.md.

### Cycle 1: Cooperative Review (v1)

**Mode**: cooperative | **Agents**: apm, spec-kit, gh-aw | **Artifacts**: 16
**Record**: [`conversus/summary/final.md`](conversus/summary/final.md)

- 30 recommendations → 8 withdrawn, 11 modified, 11 surviving, 9 new
- 8 convergence points achieved (singular grounding, failure semantics, cooperative-only, backward compat, structural markers, decision-authority reframe, schema versioning deferred, template extensibility)
- 4 remaining disputes → 17 spec changes applied

### Cycle 2: Cooperative Review (v2)

**Mode**: cooperative | **Agents**: apm, spec-kit, gh-aw | **Artifacts**: 16
**Record**: [`conversus-v2/summary/final.md`](conversus-v2/summary/final.md)

- Reviewed the spec after v1 changes were integrated
- 15/17 v1 changes correctly integrated; 7 new convergence points
- 4 new disputes (dispute-entry definition, structured output weight, SC priority, citation enforcement)
- Assessment: spec ready for implementation with 2 text-level blockers

### Cycle 3: Dispute Resolution

**Mode**: winner-take-all | **Agents**: mechanist, pragmatist, purist | **Arbiter**: balanced | **Artifacts**: 18
**Record**: [`dispute-resolution/summary/final.md`](dispute-resolution/summary/final.md)

- 3 philosophically distinct agents debated the 4 v2 blockers
- All 4 blockers resolved unanimously or by 2:1 majority
- 3 micro-disputes arbitrated with binding rulings
- Produced exact spec text for each resolution

### Cycle 4: Enforcement Audit

**Mode**: cooperative | **Agents**: mechanist, pragmatist, purist | **Arbiter**: balanced | **Artifacts**: 18
**Record**: [`enforcement-audit/summary/final.md`](enforcement-audit/summary/final.md)

- Audited whether SKILL.md enforces what it claims
- Found P0 blocker: red-blue role variables undefined
- 17 consolidated fixes (1 P0, 6 P1, 5 P2, 6 P3)
- 3 disputes arbitrated; all fixes applied to SKILL.md and templates
- **All 17 fixes applied** — SKILL.md and 20 templates updated

### Convergence Points (cumulative)

1. Singular grounding document as sole citation authority
2. Phase 6 failure falls back to Phase 5 output
3. Cooperative-only restriction retained for v1
4. Backward compatibility via optional arbiter field
5. Structural HTML markers for trigger evaluation
6. Information-asymmetry reframed as decision authority
7. Schema versioning deferred (YAGNI)
8. Template extensibility preserved
9. Three-tier failure model (FR-022/FR-023)
10. Content-presence guard scoped to `disputes_remain`
11. Draft template filtering requires testable FR
12. Template authoring contract scoped to cooperative mode
13. Red-blue role variables as blocking defect (fixed)
14. Templates are the enforcement surface
15. Single-anchor template path resolution