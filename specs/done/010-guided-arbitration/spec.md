# Feature Specification: Guided Arbitration

**Feature ID**: `010-guided-arbitration`
**Created**: 2026-03-21
**Status**: Draft
**Depends On**: `001-subject-arbitration` (hard gate — Phase 6 engine must be spec-complete before building a guided on-ramp), `006-inter-round-arbitration` (influence levels used in guided prompts), `009-guided-execution` (completed deliberation output)
**Origin**: Decomposed from original 003-decision-framework, Phase C

---

## 1. Feature Summary

`/conversus arbitrate` guides users through arbiter configuration when disputes remain after deliberation, then invokes Phase 6. It does not redefine arbitration mechanics — it provides a conversational interface to spec 001's engine.

Most users don't know what a "grounding document" is, what `trigger: disputes_remain` means, or how to write an arbiter identity prompt. This command handles all of that: it detects unresolved disputes, asks who the arbiter is in plain language, explains what a grounding document is, generates the config, and runs Phase 6.

**Implementation gate**: This spec MUST NOT be implemented until spec 001 achieves spec-complete status — all FRs implemented and verified. Phase C delegates to the Phase 6 engine; that engine must be fully correct before building a guided on-ramp to it.

**What changes**: New `/conversus arbitrate` subcommand handler in SKILL.md. Guided arbiter configuration flow. Plain-language ruling summaries.

**What does not change**: Phase 6 execution (spec 001). Arbiter schema. Template structure. Trigger evaluation.

---

## 2. Functional Requirements

### Dispute Detection

- **FR-001**: `/conversus arbitrate` MUST accept a path to a completed conversus output directory (or find one in the working directory).
- **FR-002**: MUST read `summary/final.md`, parse remaining disputes using the Dispute-Parsing Subsystem, and report the count.
- **FR-003**: If no disputes remain, report "No unresolved disputes. Arbitration is not needed." Allow override if user insists (`trigger: always` for subject endorsement).

### Guided Arbiter Configuration

- **FR-004**: If no `arbiter` block exists in `conversus.yml`, guide the user through configuration:
  - "Who should arbitrate? This is usually the subject of the review, a senior stakeholder, or the project's governing principles."
  - "What document grounds their decisions? This could be design principles, a constitution, requirements, or project values."
- **FR-005**: Generate an arbiter identity prompt from the user's natural-language description:
  - "the system being built" → prompt positions arbiter AS the system
  - A stakeholder role → prompt positions arbiter as that role
  - A governing document → prompt positions arbiter as impartial judge
- **FR-006**: The user MAY edit the generated prompt before execution.
- **FR-007**: `grounding` is required. If the user has no grounding document, explain what it is in plain language and offer to create a minimal one from `problem.md` constraints and success criteria.
- **FR-008**: Ask the user about influence level (spec 006): "Should the arbiter's rulings be binding (final authority), recommended (adopt unless you have counter-evidence), or advisory (consider but not bound)?" Default to `binding` if the user doesn't have a preference.

### Execution

- **FR-009**: Execution MUST delegate to the Phase 6 engine defined in spec 001. No new arbitration logic.
- **FR-010**: The generated `arbiter` config MUST be appended to the existing `conversus.yml`.

### Post-Arbitration

- **FR-011**: Present a plain-language summary of each ruling: the dispute, the decision, and the one-sentence rationale. Print the path to `arbitration/resolution.md` for the full output.
- **FR-012**: Works standalone — does not require the guided workflow (`define` → `interests` → `mode` → `converge`) to have been used. Any completed conversus output directory is valid input.

---

## 3. Success Criteria

- **SC-001**: Guided-workflow arbitration produces the same output structure as a hand-configured `arbiter:` block.
- **SC-002**: A user with no knowledge of Phase 6 can set up and run arbitration using only plain-language answers.
- **SC-003**: Works against any completed conversus output directory, regardless of how it was created.
- **SC-004**: The arbiter influence level prompt is clear to a non-technical user.

---

## 4. Constraints

- **Must NOT redefine arbitration mechanics.** This is a UX layer over spec 001's engine.
- **Must NOT implement before spec 001 is spec-complete.** Hard gate.
- **Must NOT generate an arbiter without grounding.** An arbiter without a decision framework produces arbitrary rulings.
