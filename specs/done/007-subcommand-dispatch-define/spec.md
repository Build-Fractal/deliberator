# Feature Specification: Subcommand Dispatch & Problem Definition

**Feature ID**: `007-subcommand-dispatch-define`
**Created**: 2026-03-21
**Status**: Draft
**Depends On**: None (foundational — establishes the dispatch infrastructure all guided workflow commands use)
**Origin**: Decomposed from original 003-decision-framework, Phase A (part 1)

---

## 1. Feature Summary

Today `/conversus` has a single entry point: `/conversus run`. This spec adds subcommand routing to SKILL.md so that `/conversus define`, `/conversus interests`, `/conversus mode`, etc. can each dispatch to their own handler. It then implements the first guided command: `/conversus define`, which takes a natural-language problem description and produces a structured `problem.md`.

`/conversus define` is the entry point for non-experts. A user describes a decision in plain language — the system structures it into a problem definition with type classification, constraints, and open questions. This artifact feeds subsequent commands (interests, mode) that ultimately produce a `conversus.yml`.

**What changes**: SKILL.md gains a "Subcommand Dispatch" section before Step 1. A new `/conversus define` command handler is added. The existing `/conversus run` handler is unchanged but renamespaced under `Run:` headings. The frontmatter `description` field is updated to list available subcommands.

**What does not change**: `/conversus run` behavior. Template system. Engine execution. Output format.

---

## 2. Functional Requirements

### Subcommand Dispatch

- **FR-001**: SKILL.md MUST dispatch based on the first argument after `/conversus`. Known subcommands: `run` (existing), `define` (this spec). Future specs add: `interests`, `mode`, `converge`, `arbitrate`, `gate`.
- **FR-002**: `/conversus run` MUST route to the existing Step 1-5 execution flow with zero behavioral change.
- **FR-003**: `/conversus` with no arguments MUST default to `run` (backward compatible).
- **FR-004**: Unknown subcommands MUST produce a helpful error listing available commands.

### `/conversus define`

- **FR-005**: `/conversus define` MUST accept a natural-language description of a decision, either inline or interactively.
- **FR-006**: `/conversus define --context <path>` MUST read context documents (specs, proposals, architecture docs) and incorporate domain-specific constraints into the problem definition.
- **FR-007**: Output MUST be `problem.md` in the working directory (or `--output <dir>`).
- **FR-008**: Problem type MUST be classified as one of: `selection`, `integration`, `scoping`, `stress-test`. If ambiguous, the agent marks the type as its best guess and lists alternatives.
- **FR-009**: `problem.md` MUST contain structured sections: Decision (one sentence), Type, Context (2-4 sentences), Constraints (bulleted), Success Criteria, Open Questions, Source Documents.
- **FR-010**: Ambiguities MUST be marked with `[CLARIFY: ...]` tags for the user to resolve before proceeding.
- **FR-011**: If `problem.md` already exists, the agent MUST present it and ask whether to refine or replace. Never silently overwrite.
- **FR-012**: If no description is provided and no `--context` is given, the agent MUST ask clarifying questions interactively: "What decision are you facing?", "Who or what are the competing perspectives?", "What are the constraints?"

### `problem.md` Schema

```markdown
# Problem Definition

## Decision
<one-sentence statement of the decision to be made>

## Type
<selection | integration | scoping | stress-test>

## Context
<2-4 sentences of relevant background, referencing context documents if provided>

## Constraints
- <constraint 1>
- <constraint 2>

## Success Criteria
<what does a good outcome look like?>

## Open Questions
- [CLARIFY: <question 1>]
- [CLARIFY: <question 2>]

## Source Documents
- <path to context doc 1>
- <path to context doc 2>

## Status
<draft | ready> -- <count> items need clarification
```

---

## 3. Success Criteria

- **SC-001**: `/conversus define "We need to choose between Redis and Postgres for caching"` produces a `problem.md` with type `selection`.
- **SC-002**: `/conversus define --context specs/003/spec.md` incorporates domain details from the context doc into the constraints and context sections.
- **SC-003**: `/conversus run conversus.yml` continues to work identically to current behavior — dispatch adds zero overhead to the existing path.
- **SC-004**: `/conversus` with no arguments defaults to `run` behavior (backward compatible).
- **SC-005**: A vague description ("we need to figure out the architecture") produces a `problem.md` with `[CLARIFY: ...]` tags on ambiguous fields.

---

## 4. Constraints

- **Must NOT require coding knowledge to use.** Plain-language descriptions are the input; structured markdown is the output.
- **Must NOT break `/conversus run`.** The dispatch is additive — existing behavior is untouched.
- **Must NOT couple to any specific problem domain.** Works for framework selection, architecture review, team scoping, security analysis, or any multi-perspective decision.
