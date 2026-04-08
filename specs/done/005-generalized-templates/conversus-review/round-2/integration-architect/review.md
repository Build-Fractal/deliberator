# Integration Architect Review -- Round 2

**Reviewer**: integration-architect
**Spec**: `005-generalized-templates`
**Round**: 2 of 2
**Date**: 2026-03-21
**Prior Round Synthesis**: `round-1/summary/final.md`

---

## Executive Summary

Round 1 produced a high-quality synthesis with 14 fully converged items and only 4 remaining disputes. The synthesizer's resolutions on all 4 disputes are sound. I accept them. My Round 2 review shifts focus from convergence mechanics to integration readiness: whether the converged recommendations, as synthesized, will actually work when spec 006 (inter-round arbitration), spec 008 (executable conversus), and SKILL.md meet the implementation artifacts. I surface 3 integration gaps the Round 1 deliberation did not reach and refine 2 converged items where the synthesized form has latent issues that will manifest during implementation.

No Round 1 concessions are reversed. My 5 concessions from Round 1 (MODE_PRESENCE endorsement retraction, loader purity retraction, ConfigCondition typing upgrade, plugin_data withdrawal, schema version upgrade) all stand.

---

## Alignment with Round 1 Synthesis

### Accepted Dispute Resolutions

**Dispute 1 (Programmatic API parameter design)**: I accept the synthesizer's resolution -- `ValidationConfig` Pydantic model with `root: Path` and `mode: Optional[str] = None`, no `known_plugin_variables`. The synthesizer correctly identified that adding a field with a default to a Pydantic model is non-breaking, which neutralizes game-engine-advocate's concern without front-loading speculative parameters. This is the right call.

**Dispute 2 (`error_type` -- `Literal` vs. `str`)**: I accept the synthesizer's resolution -- `str` with `@field_validator` checking against `KNOWN_ERROR_TYPES: frozenset[str]`. The synthesizer applied the mode-resolution precedent consistently. I concede that my distinction between "schema-external" and "code-internal" enumerations, while intellectually defensible, is not worth maintaining a different validation pattern for a different kind of extensible set. One pattern for all extensible sets is simpler to reason about.

**Dispute 3 (Schema version field priority)**: I already held the P2 position. Accepted.

**Dispute 4 (Bare import fix sequencing)**: I accept the synthesizer's resolution that the import fix is part of P1-2 (programmatic API), not a separate P2 deliverable. game-engine-advocate was correct that you cannot ship a library function with broken imports. The synthesizer's framing -- "they are one task, not two" -- is cleaner than my original P2 bundling.

### Convergence Items I Endorse Without Reservation

All 14 convergence items from Section 5 are well-formulated. I particularly want to reinforce:

- **P1-1 (Purify schema-loading functions)**: This is the single highest-leverage change. Every downstream integration -- spec 006 validation of `arbiter.timing`, spec 008 pre-execution validation, CI pipeline linting -- depends on the linter being callable without side effects. The current `sys.exit(2)` in `load_variables_schema` and `load_mode_schema` makes it impossible to use these functions in any context other than the CLI. This must ship first.

- **P1-4 (ConfigCondition model)**: This directly enables spec 006's `PRIOR_ARBITRATION_PATH`, which is conditioned on `arbiter.timing: inter-round`. Without typed config conditions, the linter cannot express "this variable is required only when arbiter.timing is inter-round" -- it would have to hardcode the condition or skip validation entirely.

- **P2-1 (MODE_PRESENCE as YAML declarations)**: The current 28-entry hardcoded dict in `validate.py` L108-144 is the single largest maintenance burden in the linter. It has no derivation trail, no documentation of why specific (phase, mode) pairs are True or False, and must be manually updated whenever a template changes. Moving this to mode schema YAML makes the data self-documenting and auditable.

---

## Missed Opportunities

### MO-1: Linter invocation pathway from SKILL.md Step 3 is underspecified

The Round 1 synthesis converged on P1-2 (programmatic API) and the spec's FR-008 (validation in Step 3), but the actual invocation pathway is ambiguous. SKILL.md Step 3 currently says:

> Run validation: `uv run python linter/validate.py` (or `--mode {mode}` for a single mode).

This is a CLI invocation inside an orchestrator step that is itself a Claude Code skill. The skill engine does not shell out to run Python scripts -- it dispatches agents. The synthesized `validate_all(config: ValidationConfig) -> ValidationResult` API solves the library-call problem, but no one in Round 1 addressed how the skill engine actually calls it. There are two options:

1. **Agent-based validation**: The orchestrator spawns a sub-agent that runs `uv run python linter/validate.py` via the Bash tool. This works but is heavyweight -- an entire agent context for a sub-second validation.
2. **SKILL.md inline validation**: The SKILL.md step instructs the orchestrating agent to call the linter's API directly (via Python eval or Bash). This is more natural but means the orchestrating agent needs Python execution capability.

The spec should take a position. My recommendation: option 2 (Bash tool invocation by the orchestrating agent, not a sub-agent). This aligns with the `allowed-tools` in SKILL.md's frontmatter, which includes `Bash(ls:*)` -- but this glob does not currently permit `uv run python`. The `allowed-tools` field needs to be updated to `Bash(ls:*,uv run python linter/validate.py)` or the validation invocation needs to use a different mechanism.

**Priority**: P2. This does not block the schema or linter implementation, but it blocks FR-008 (pre-execution validation in SKILL.md).

### MO-2: Mode schema `templates` list is not validated against the filesystem

The mode schema files (e.g., `cooperative.yml`) include a `templates` list declaring which template files should exist:

```yaml
templates:
  - review
  - cross-review
  - revision
  - disputes
  - synthesis
  - arbitration
  - cross-round-synthesis
```

The linter's `main()` function (validate.py L339-345) already checks this:

```python
for tmpl_name in ms.templates:
    tmpl_path: Path = templates_dir / f"{tmpl_name}.md"
    if not tmpl_path.exists():
        all_errors.append(...)
```

This is good. But the reverse check is missing: templates that exist in `templates/{mode}/` but are NOT listed in the mode schema's `templates` field are silently ignored. This means a template could exist, pass the linter (because the linter skips unknown templates), but fail at runtime because the orchestrator does not load it. Or worse, a renamed template (e.g., `disputes.md` -> `dispute-filing.md`) would be silently orphaned.

The linter should report: "templates/{mode}/{name}.md: template file exists but is not listed in schema/modes/{mode}.yml. Either add it to the templates list or remove the file."

**Priority**: P3. Defensive check. No current templates are orphaned, but this is a "pit of success" improvement that prevents silent drift.

### MO-3: `ROUND_SYNTHESES` type mismatch between schema and models

In `schema/variables.yml`, `ROUND_SYNTHESES` is declared as `type: extracted-content`:

```yaml
ROUND_SYNTHESES:
    type: extracted-content
    description: >
      Extracted content from each round's synthesis output, formatted by
      the orchestrator for cross-round comparison.
```

But in `linter/models.py`, the corresponding field in `CrossRoundSynthesisContext` is:

```python
ROUND_SYNTHESES: str  # newline-separated paths
```

The comment says "newline-separated paths" (which is a path-list pattern), but the schema says `extracted-content` (which is pre-formatted content, not paths). These are semantically different: a path-list tells the agent "read these files," while extracted-content says "here is the content, already extracted." The linter models and the schema need to agree. Based on how cross-round synthesis actually works in SKILL.md -- the orchestrator pre-formats content from each round's synthesis -- `extracted-content` is correct and the models.py comment is wrong.

When P1-3 (PathList custom type) is implemented, this field should NOT be converted to `PathList` because it is not a path list. The comment should be corrected to `# pre-formatted synthesis content per round`.

**Priority**: P3. Cosmetic, but becomes a real bug if someone applies PathList blindly to all `str` fields with "path" in the comment.

---

## Off-Base Assumptions

### OBA-1: The spec assumes a 1:1 mapping between template filenames and phase names

Throughout the spec (FR-004), the linter (validate.py L348: `phase: str = tmpl_path.stem`), and the mode schemas, there is a rigid assumption that the template filename IS the phase name. `review.md` is the review phase template. `cross-round-synthesis.md` is the cross-round-synthesis phase template.

This works today. But spec 006's inter-round arbitration (FR-006) places arbitration output at `{output}/round-N/arbitration/resolution.md`, and the arbitration template is reused per-round. The template filename (`arbitration.md`) still maps to the phase name (`arbitration`). No issue yet.

However, if any future spec introduces variant templates for the same phase (e.g., `review-round-1.md` vs. `review-round-2+.md` for first-round vs. subsequent-round review prompts), the `phase = tmpl_path.stem` assumption breaks entirely. The linter cannot validate a template whose filename does not match a known phase name.

This is not an immediate problem -- no current spec introduces variant templates. But it is worth noting in the spec's "Extension Points" section (P2-6) that the filename-phase mapping is a constraint, not an accident. If downstream specs need per-round template variants, they should use conditional blocks within a single template (which is the current pattern with `PRIOR_ROUND_SECTION`), not separate template files.

**Priority**: Documentation only (include in P2-6). No code change needed.

### OBA-2: `validate_templates: false` bypass is too coarse

The spec (FR-009) and SKILL.md Step 3 both describe a binary toggle: validate or skip. There is no middle ground. In practice, during active template development, a user may want to:

- Skip heading validation but keep variable validation (because they are editing the heading structure but want to ensure variables are correct).
- Skip validation for a single mode while validating others (because they are adding a new mode's templates incrementally).

The binary toggle is fine for v1. But the spec should note in Section 6 (Implementation Notes) that `validate_templates` may evolve from boolean to a structured config (e.g., `validate_templates: {variables: true, headings: false}` or `validate_templates: {skip_modes: [auction]}`). This is not a P1/P2 change -- it is forward-looking documentation.

**Priority**: Documentation only (include in P2-6). No code change needed.

---

## Actionable Recommendations

### Rec 1: Update SKILL.md `allowed-tools` for linter invocation (P2)

**Context**: MO-1. The linter's programmatic API (P1-2) enables library-level validation, but the SKILL.md orchestration pathway still needs a concrete invocation mechanism.

**Action**: Add a note to spec Section 6 (Implementation Notes) specifying that SKILL.md Step 3's validation invocation should use `Bash` tool with `uv run python linter/validate.py --mode {mode}`, and that `allowed-tools` in SKILL.md frontmatter should be updated to permit this. Alternatively, if the programmatic API is exposed as a `[project.scripts]` entry point (P2-8), the invocation becomes `conversus-lint --mode {mode}`.

**Rationale**: Without this, P1-2 and FR-008 are implemented but never connected. The linter exists as a library function and a CLI tool, but the orchestrator has no authorized way to call either.

### Rec 2: Add reverse template existence check to the linter (P3)

**Context**: MO-2. Templates on disk but not in the mode schema are silently ignored.

**Action**: After the existing check (mode schema lists a template that does not exist on disk), add the reverse: iterate `templates/{mode}/*.md` and check each against the mode schema's `templates` list. Report any template file that exists but is not declared.

**Rationale**: This catches orphaned templates after renames or refactors. It is a "pit of success" design -- the linter already validates in one direction, and adding the reverse direction is trivial.

### Rec 3: Fix `ROUND_SYNTHESES` comment in models.py (P3)

**Context**: MO-3. The field comment says "newline-separated paths" but the schema says `extracted-content`.

**Action**: Change the `CrossRoundSynthesisContext.ROUND_SYNTHESES` comment from `# newline-separated paths` to `# pre-formatted synthesis content per round`. Ensure this field is NOT included in the P1-3 PathList conversion batch.

**Rationale**: Prevents a real bug when PathList is applied systematically. The comment is the only documentation of this field's semantics at the code level.

### Rec 4: Document filename-phase constraint in Extension Points (P2-6 addendum)

**Context**: OBA-1. The `phase = tmpl_path.stem` pattern is load-bearing but undocumented as a constraint.

**Action**: In the P2-6 "Extension Points" spec section, add under "NOT extension points": "Template filenames must match phase names exactly (e.g., `review.md` for the review phase). Variant templates for the same phase must use conditional blocks within a single template, not separate files."

**Rationale**: Prevents future specs from introducing multi-file-per-phase patterns that would break the linter without this being recognized as a breaking change.

### Rec 5: Note `validate_templates` evolution path in Extension Points (P2-6 addendum)

**Context**: OBA-2. The boolean toggle is correct for v1 but may need granularity.

**Action**: In the P2-6 "Extension Points" spec section, add: "The `validate_templates` field is boolean in v1. If granular control is needed (per-mode, per-check-type), the field may evolve to accept a structured config object. The boolean form must remain valid for backward compatibility."

**Rationale**: Establishes the evolution path without implementing it prematurely. Prevents a future spec from treating the boolean field as permanent and designing around it.

---

## Referenced Documentation

| Document | Relevance |
|---|---|
| `conversus/specs/006-inter-round-arbitration/spec.md` | FR-009 introduces `PRIOR_ARBITRATION_PATH` variable requiring `config_conditions` in spec 005. FR-012 adds variables to Phase 1-5 templates. The Round 1 P1-5 convergence correctly addresses this. |
| `conversus/specs/008-executable-conversus/001-executable-conversus.md` | Spec 008's Phase 5 (Config Validation) overlaps with spec 005's FR-008/FR-009 pre-execution validation. The linter's programmatic API (P1-2) is the mechanism spec 008 should use for template validation. MO-1 identifies the invocation gap. |
| `conversus/SKILL.md` | Step 3 (Load Templates) is the integration point for FR-008. The `allowed-tools` frontmatter field and `validate_templates` config field are the two configuration surfaces. MO-1 identifies the authorization gap. |
| `conversus/schema/variables.yml` | Single source of truth for variable definitions. MO-3 identifies the `ROUND_SYNTHESES` type discrepancy. |
| `conversus/linter/models.py` | Implementation of Pydantic models. MO-3 identifies the comment inaccuracy on `ROUND_SYNTHESES`. |
| `conversus/linter/validate.py` | Linter implementation. MO-2 identifies the missing reverse template existence check (L339-357). |
| `conversus/schema/modes/*.yml` | Mode schema files. All 4 modes declare identical `templates` lists (7 entries each), which is correct for current scope but means the `templates` field adds no mode-specific information today -- its value is in future modes that may have different template sets. |

---

## Summary of Positions

| Item | Position | Priority |
|---|---|---|
| Dispute 1 (API parameter design) | Accept synthesizer resolution (ValidationConfig, no plugin params) | -- |
| Dispute 2 (error_type Literal vs str) | Accept synthesizer resolution (str with validated set) | -- |
| Dispute 3 (Schema version priority) | Accept P2 (already held this position) | -- |
| Dispute 4 (Import fix sequencing) | Accept synthesizer resolution (part of P1-2) | -- |
| Rec 1: SKILL.md linter invocation pathway | New | P2 |
| Rec 2: Reverse template existence check | New | P3 |
| Rec 3: Fix ROUND_SYNTHESES comment | New | P3 |
| Rec 4: Document filename-phase constraint | Addendum to P2-6 | Documentation |
| Rec 5: Document validate_templates evolution | Addendum to P2-6 | Documentation |

All 5 concessions from Round 1 are maintained. No reversals.
