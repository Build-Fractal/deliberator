# Feature Specification: Generalized Template Schema, Variables, and Linter

**Feature ID**: `005-generalized-templates`
**Created**: 2026-03-20
**Status**: Draft
**Depends On**: `004-universal-rounds` (extends template system to all modes)
**Input**: Template completeness gaps discovered during spec 004's 69-agent stress test — missing variables (`{PRIOR_ROUND_SECTION}`, `{REMAINING_DISPUTES}`), missing structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`), and heading mismatches across modes. These gaps were only caught at runtime after significant agent expenditure.

---

## 1. Feature Summary

Conversus templates use `{VARIABLE}` substitution driven by SKILL.md prose instructions. The variable contract — which variables exist, which are required per phase, which are mode-specific — is scattered across SKILL.md paragraphs and learned by reading examples. There is no machine-readable schema, no automated validation, and no way to catch missing variables before a multi-agent run discovers them.

Spec 004's stress test proved this is insufficient: 3 non-cooperative review templates shipped without `{PRIOR_ROUND_SECTION}`, 3 arbitration templates shipped without `{REMAINING_DISPUTES}`, and 4 cross-round-synthesis templates shipped without `DISPUTES_BEGIN`/`DISPUTES_END` markers. All were caught by agents, not by tooling.

This spec introduces three artifacts:

1. **`schema/variables.yml`** — Machine-readable registry of all template variables with types, descriptions, and phase assignments. Single source of truth replacing SKILL.md prose.
2. **`schema/modes/{mode}.yml`** — Per-mode schema defining required output headings, dispute heading conventions, structural marker requirements, and mode-specific variables.
3. **`linter/`** — A validation tool that checks templates against the schema at development time, catching missing variables, unknown variables, heading mismatches, and missing structural markers before any agent is launched.

**What changes**: New `schema/` directory with structured YAML files. New `linter/` tool. SKILL.md gains a reference to the schema as the authoritative variable contract.

**What does not change**: Template syntax (`{VARIABLE}` substitution). Template content (prompts, sections, rules). The orchestrator's variable population logic. Runtime behavior.

---

## 2. User Stories

### US-1: Schema-Validated Template Authoring

As a template author creating or modifying a conversus template, I want the system to tell me immediately if I forgot a required variable, misspelled a variable name, or used a heading that doesn't match the mode's schema, so that I catch errors before running a multi-agent deliberation.

**Acceptance Criteria**:

1. **Given** a template author creates `templates/red-blue/review.md` without `{PRIOR_ROUND_SECTION}`, **When** they run the linter, **Then** it reports: "templates/red-blue/review.md: missing required variable {PRIOR_ROUND_SECTION} (required for phase: review, see schema/variables.yml)."

2. **Given** a template contains `{AGENT_NMAE}` (typo), **When** the linter runs, **Then** it reports: "templates/cooperative/review.md: unknown variable {AGENT_NMAE}. Did you mean {AGENT_NAME}?"

3. **Given** `schema/modes/red-blue.yml` requires the heading "Updated Risk Register" in arbitration templates, **When** `templates/red-blue/arbitration.md` uses "Risk Register Summary" instead, **Then** the linter reports the heading mismatch.

4. **Given** `schema/modes/cooperative.yml` requires `DISPUTES_BEGIN`/`DISPUTES_END` markers in cross-round-synthesis templates, **When** the markers are absent, **Then** the linter reports: "templates/cooperative/cross-round-synthesis.md: missing required structural marker CONVERSUS:DISPUTES_BEGIN."

5. **Given** all templates pass validation, **When** the linter runs, **Then** it reports: "All 28 templates valid against schema."

---

### US-2: Variable Contract as Structured Data

As a conversus maintainer, I want the variable contract defined in one YAML file instead of scattered across SKILL.md prose, so that I can see all variables, their types, which phases use them, and whether they're required or optional — without reading hundreds of lines of specification.

**Acceptance Criteria**:

1. **Given** `schema/variables.yml` exists, **When** a maintainer reads it, **Then** they can determine for any variable: its name, type, description, which phases it appears in, whether it's required or optional, and any mode-specific conditions.

2. **Given** a new variable is added to the orchestrator, **When** the maintainer adds it to `schema/variables.yml`, **Then** the linter enforces its presence in the appropriate templates. No SKILL.md prose update is needed for the linter to work.

3. **Given** `schema/variables.yml` lists all variables, **When** compared against SKILL.md's prose variable documentation, **Then** the two are consistent. The schema is authoritative; SKILL.md references it.

---

### US-3: Mode-Specific Schema Enforcement

As a conversus maintainer extending support to a new competition mode, I want a mode schema file that defines exactly what templates for that mode must contain — required headings, dispute heading conventions, structural markers, and mode-specific variables — so that I can validate completeness before the first test run.

**Acceptance Criteria**:

1. **Given** `schema/modes/red-blue.yml` exists, **When** a maintainer reads it, **Then** they know: the dispute heading for synthesis (`### Disputed Risks`), the dispute entry pattern (`**[RISK-ID]:`), the required arbitration headings, and which variables are mode-specific (`AGENT_ROLE`, `REVIEWER_ROLE`, `REVIEWED_ROLE`).

2. **Given** a new mode "auction" is proposed, **When** the maintainer creates `schema/modes/auction.yml`, **Then** the linter can validate any `templates/auction/*.md` files against it before a single agent is launched.

3. **Given** the SKILL.md Phase 6 validation heading table, **When** compared against the mode schema files, **Then** they are consistent. The mode schema is the source; SKILL.md references it.

---

### US-4: Pre-Execution Validation

As a user about to run a multi-round conversus deliberation, I want the orchestrator to validate templates against the schema before launching any agents, so that missing variables are caught at config time — not at Round 2 Phase 1 when an agent produces duplicative output.

**Acceptance Criteria**:

1. **Given** the linter is integrated into SKILL.md's Step 3 (Load Templates), **When** a template fails validation, **Then** the orchestrator reports the error and stops before Phase 1. No agents are launched.

2. **Given** all templates pass validation, **When** the orchestrator proceeds, **Then** execution is identical to the current system. Zero runtime overhead beyond the one-time check.

3. **Given** the linter is optional (can be skipped with a config flag), **When** a user sets `validate_templates: false`, **Then** the orchestrator skips validation and proceeds as today. Default is `true`.

---

## 3. Data Model

### `schema/variables.yml`

```yaml
# All template variables used by the conversus orchestrator.
# This file is the single source of truth for the variable contract.
# The linter validates templates against this schema.

variables:
  # Variables default to required: true when the required field is omitted.

  # === Universal variables (all phases, all modes) ===
  AGENT_NAME:
    type: string
    description: Agent's name from conversus.yml config
    phases: [review, cross-review, revision, disputes]

  AGENT_PROMPT:
    type: string
    description: Agent's identity prompt from config
    phases: [review, cross-review, revision, disputes]

  TARGET_PATH:
    type: path
    description: Primary target file path (first in target list)
    phases: [review, cross-review, revision, disputes, synthesis, arbitration, cross-round-synthesis]

  TARGET_FILES:
    type: path-list
    description: All resolved target file paths, one per line
    phases: [review, cross-review, revision, disputes, synthesis, arbitration, cross-round-synthesis]

  OUTPUT_PATH:
    type: path
    description: Absolute path where agent writes its output
    phases: [review, cross-review, revision, disputes, synthesis, arbitration, cross-round-synthesis]

  MODE:
    type: string
    description: Competition mode name
    phases: [review, synthesis, arbitration, cross-round-synthesis]

  # === Round-aware variables ===
  ROUND:
    type: integer
    description: Current round number (1-indexed)
    phases: [review, cross-review, revision, disputes, synthesis]
    condition: "rounds > 1"

  MAX_ROUNDS:
    type: integer
    description: Configured maximum rounds
    phases: [review, cross-review, revision, disputes, synthesis]
    condition: "rounds > 1"

  PRIOR_SYNTHESIS_PATH:
    type: path
    description: Path to prior round's synthesis (empty for Round 1)
    phases: [review, cross-review, revision, disputes, synthesis]
    condition: "rounds > 1"

  PRIOR_ROUND_DIR:
    type: path
    description: Path to prior round's output directory (empty for Round 1)
    phases: [review, cross-review, revision, disputes, synthesis]
    condition: "rounds > 1"

  # === Conditional block variables ===
  PRIOR_FILES_SECTION:
    type: conditional-block
    description: Prior iteration context block (empty if no prior config)
    phases: [review]
    required: true

  PRIOR_ROUND_SECTION:
    type: conditional-block
    description: Prior round context block (empty for Round 1, multi-line for Round 2+)
    phases: [review]
    required: true

  # === Phase-specific variables ===
  AGENT_DOCS:
    type: extracted-content
    description: Agent's documentation paths from config
    phases: [review, cross-review, revision, disputes]

  AGENT_ROLE:
    type: string
    description: Agent's role (red/blue)
    phases: [review, cross-review, revision, disputes]
    modes: [red-blue]

  REVIEWER_NAME:
    type: string
    phases: [cross-review]

  REVIEWER_PROMPT:
    type: string
    phases: [cross-review]

  REVIEWED_NAME:
    type: string
    phases: [cross-review]

  REVIEWED_REVIEW_PATH:
    type: path
    phases: [cross-review]

  REVIEWER_REVIEW_PATH:
    type: path
    phases: [cross-review]

  MY_REVIEW_PATH:
    type: path
    phases: [revision]

  CROSS_REVIEWS_OF_ME:
    type: path-list
    phases: [revision]

  MY_CROSS_REVIEWS:
    type: path-list
    phases: [revision]

  ITERATION:
    type: integer
    phases: [revision]

  ALL_REVISION_PATHS:
    type: path-list
    phases: [disputes]

  MY_REVISION_PATH:
    type: path
    phases: [disputes]

  AGENT_NAMES:
    type: string
    description: Comma-separated list of agent names
    phases: [synthesis, cross-round-synthesis]

  ALL_REVIEWS:
    type: path-list
    phases: [synthesis]

  ALL_CROSS_REVIEWS:
    type: path-list
    phases: [synthesis]

  ALL_REVISIONS:
    type: path-list
    phases: [synthesis]

  ALL_DISPUTES:
    type: path-list
    phases: [synthesis, arbitration]

  # === Arbitration variables ===
  ARBITER_NAME:
    type: string
    phases: [arbitration]

  ARBITER_PROMPT:
    type: string
    phases: [arbitration]

  ARBITER_DOCS:
    type: path-list
    phases: [arbitration]

  GROUNDING_PATH:
    type: path
    phases: [arbitration]

  SYNTHESIS_PATH:
    type: path
    phases: [arbitration]

  TRIGGER:
    type: string
    phases: [arbitration]

  REMAINING_DISPUTES:
    type: extracted-content
    description: Disputes extracted from synthesis via structural markers
    phases: [arbitration]
    required: true

  # === Cross-round synthesis variables ===
  ROUNDS_COMPLETED:
    type: integer
    phases: [cross-round-synthesis]

  ROUND_SYNTHESES:
    type: path-list
    phases: [cross-round-synthesis]

  TERMINATION_REASON:
    type: string
    phases: [cross-round-synthesis]
```

### `schema/modes/{mode}.yml`

```yaml
# schema/modes/red-blue.yml
mode: red-blue

# Mode-specific variables (required in addition to universal)
variables:
  - AGENT_ROLE
  - REVIEWER_ROLE
  - REVIEWED_ROLE

# Dispute-Parsing Subsystem interface
disputes:
  synthesis_heading: "### Disputed Risks"
  entry_pattern: "**[RISK-ID]:"
  structural_markers: true

# Phase 6 output validation
arbitration:
  required_headings:
    - Process Note
    - Decision Framework
    - Binding Decisions
    - Updated Risk Register

# Cross-round synthesis
cross_round_synthesis:
  structural_markers: true
  dispute_heading: "### Disputed Risks"
```

---

## 4. Functional Requirements

### Schema (P1)

- **FR-001**: A `schema/variables.yml` file MUST exist listing every template variable with name, type, description, and phase assignments.
- **FR-002**: A `schema/modes/{mode}.yml` file MUST exist for each competition mode, defining dispute headings, arbitration required headings, mode-specific variables, and structural marker requirements.
- **FR-003**: The schema files MUST be consistent with SKILL.md's current variable documentation. SKILL.md SHOULD reference the schema as authoritative.

### Linter (P1)

- **FR-004**: The linter MUST check every `templates/{mode}/*.md` file for: (a) all `{VARIABLE}` references exist in `schema/variables.yml`, (b) all required variables for the template's phase appear in the template, (c) required headings from the mode schema appear in the template, (d) required structural markers are present.
- **FR-005**: The linter MUST report errors with: file path, error type (missing variable, unknown variable, missing heading, missing marker), expected value, and schema reference.
- **FR-006**: The linter MUST suggest corrections for unknown variables (fuzzy match against known variables).
- **FR-007**: The linter MUST exit with code 0 on success and non-zero on failure, producing machine-readable output (one error per line) suitable for CI integration.

### Integration (P2)

- **FR-008**: SKILL.md Step 3 (Load Templates) SHOULD validate templates against the schema before Phase 1 execution. Validation failure stops execution with an error message.
- **FR-009**: A `validate_templates` config field (default: `true`) SHOULD allow users to skip validation for backward compatibility.

---

## 5. Success Criteria

- **SC-001**: The linter catches all 3 template gaps from spec 004's stress test (missing `{PRIOR_ROUND_SECTION}`, missing `{REMAINING_DISPUTES}`, missing structural markers) when run against the pre-fix template state.
- **SC-002**: Adding a new variable to the orchestrator and `schema/variables.yml` produces a linter error for every template that should contain it but doesn't — without modifying SKILL.md prose.
- **SC-003**: Adding a new mode requires creating one `schema/modes/{mode}.yml` file, and the linter validates any templates in `templates/{mode}/` against it.
- **SC-004**: The linter runs in under 5 seconds for the full template set (28 files across 4 modes).
- **SC-005**: Zero false positives — conditional variables (like `AGENT_ROLE` for red-blue only) are not flagged as missing in modes where they don't apply.

---

## 6. Implementation Notes

### Linter Technology

The linter MUST be a Python script following Constitution Principle IX (Functional Programming and Clean Code) that:
1. Reads `schema/variables.yml` and `schema/modes/*.yml`
2. Scans `templates/{mode}/*.md` for `{VARIABLE}` patterns
3. Cross-references against phase requirements
4. Reports errors

It does NOT modify templates. It does NOT run at agent runtime (unless integrated per FR-008). It is a development-time tool.

### Relationship to Constitution

- Principle VI (Scripts Over Markdown): The schema externalizes what was prose into structured YAML — directly aligned.
- Principle VIII (Templating Engines Over Inference): The linter enforces mechanical rules — no inference needed.
- Principle II (Stable Interfaces): The schema makes the variable contract explicit and enforceable.

### Backward Compatibility

All existing templates continue to work. The schema describes what already exists. The linter catches gaps that already exist. No runtime behavior changes unless FR-008 is implemented.

---

## 7. Delivery Phases

### Phase 1: Schema + Linter (M-effort)
- Create `schema/variables.yml` from SKILL.md variable documentation
- Create `schema/modes/{mode}.yml` for all 4 modes from SKILL.md heading tables
- Build linter script
- Validate against current templates (should pass after spec 004 fixes)

### Phase 2: Integration (S-effort)
- Add template validation to SKILL.md Step 3
- Add `validate_templates` config field
- Update SKILL.md to reference schema as authoritative

---

## 8. Extension Points for Downstream Specs

### Extension points (things downstream specs CAN extend)

- New variables via `schema/variables.yml`
- New modes via `schema/modes/{mode}.yml`
- New config conditions via `ConfigCondition` model
- Plugin-contributed data via parallel composition (spec 007)
- `PHASE_CONTEXT_MODELS` as an extensible registry
- `ModeSchema` accepts new typed fields via model definition modification (with `extra = "forbid"` enforced)
- `KNOWN_ERROR_TYPES` as an extensible registry with strict validation

### NOT extension points (stable interfaces that must not change)

- `extra = "forbid"` on all core Pydantic models
- Template syntax `{VARIABLE}`
- Structural marker syntax `<!-- CONVERSUS:... -->`
- Template filename-to-phase-name 1:1 mapping (`phase = tmpl_path.stem`)

### Observations (not commitments)

- `validate_templates` is boolean in v1; granular validation control is a potential future concern but is not designed here
