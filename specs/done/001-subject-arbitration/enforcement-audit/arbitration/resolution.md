# Arbitration Resolution: Enforcement Audit Disputes

**Arbiter**: Synthesis arbiter
**Date**: 2026-03-19
**Grounding document**: `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md`
**Inputs**: Synthesis at `summary/final.md`, all 15 deliberation artifacts

---

## Ruling 1: `{PRIOR_FILES}` Injection Mechanism

### The Dispute

All three agents agree the current `{PRIOR_FILES}` injection is defective (heading mismatch between "What to Read" and "Files to Read" across modes, scope ambiguity, dual injection mechanism). They disagree on the fix.

### Each Agent's Position

- **Mechanist + Purist (partial)**: Replace section-append with a `{PRIOR_FILES_SECTION}` placeholder in Phase 1 review templates. Expands to formatted block or empty string. Single mechanism.
- **Pragmatist**: Conceded to the placeholder approach in final disputes, with constraint that expansion must be whole-section-or-nothing.
- **Purist (final retraction)**: Partially retracted concession. If placeholder is adopted, empty expansion must produce a comment line (`<!-- No prior files for this deliberation -->`), not empty string, to distinguish "no prior files" from "injection failure."

### Ruling

**Adopt the placeholder mechanism (`{PRIOR_FILES_SECTION}`), scoped to Phase 1 only, with empty-string expansion (not comment line).**

Reasoning:

1. The SKILL.md currently uses placeholder substitution for every other variable. Introducing a second mechanism (runtime section-append) is an unnecessary architectural divergence. One mechanism is simpler for the executor to implement correctly.

2. The Purist's concern about distinguishing "no prior files" from "injection failure" is valid in principle but not in practice for this system. The orchestrator fills template variables in a single pass. If `{PRIOR_FILES_SECTION}` is defined in the template, the orchestrator will either fill it or leave the literal string `{PRIOR_FILES_SECTION}` -- which is a visible failure, not a silent one. Empty-string expansion when `prior:` is absent is the correct behavior because the template should render as a clean prompt with no vestigial markers.

3. The comment-line proposal (`<!-- No prior files -->`) adds noise to prompts that LLM agents will either ignore or be confused by. HTML comments are not a standard convention in the existing templates.

4. Phase 1 only scope is unanimously agreed. Prior context propagates naturally through Phase 1 agent outputs into all subsequent phases.

### Exact Text Changes

**In SKILL.md, replace the current `{PRIOR_FILES}` section (lines 187-195):**

Replace:
```
- `{PRIOR_FILES}` — newline-separated list of prior iteration context files. Empty string if no `prior:` configured.

When filling templates, ALWAYS include `{TARGET_FILES}` so agents know to read all files. If only one target file exists, `{TARGET_FILES}` and `{TARGET_PATH}` will be the same value.

If `{PRIOR_FILES}` is non-empty, append this section to every agent prompt after the "What to Read" section:
```
**Prior iteration context** (read for background — this run builds on previous deliberation):
{PRIOR_FILES}
```
```

With:
```
- `{PRIOR_FILES_SECTION}` — if `prior:` is configured and resolves to non-empty file list, this variable expands to the following block (with actual paths substituted). If `prior:` is absent or empty, this variable expands to empty string.
  ```
  **Prior iteration context** (read for background — this run builds on previous deliberation):
  {resolved prior file paths, one per line}
  ```

When filling templates, ALWAYS include `{TARGET_FILES}` so agents know to read all files. If only one target file exists, `{TARGET_FILES}` and `{TARGET_PATH}` will be the same value.
```

**In each of the four Phase 1 review templates** (`cooperative/review.md`, `red-blue/review.md`, `winner-take-all/review.md`, `prisoners-dilemma/review.md`):

Add `{PRIOR_FILES_SECTION}` on its own line after the last file-list item in the "What to Read" / "Files to Read" section. The placeholder will either expand to the prior context block or to nothing.

---

## Ruling 2: `{ITERATION}` Variable

### The Dispute

Should `{ITERATION}` be removed from the spec, kept as orchestrator-only state, or added to Phase 3 revision templates for convergence signaling?

### Each Agent's Position

- **Mechanist**: Low severity. Remove from SKILL.md or document as orchestrator-only. Do NOT inject into templates -- could change agent behavior unpredictably.
- **Pragmatist**: P2. Add to revision template header for convergence signaling. Low impact for common case (1-2 iterations), quality improvement for edge cases.
- **Purist**: Medium severity. Functional, not cosmetic. Agents need iteration awareness for convergence quality in multi-iteration runs.

### Ruling

**Add `{ITERATION}` to Phase 3 revision templates as neutral metadata. Keep the variable defined in SKILL.md. Document its dual purpose.**

Reasoning:

1. The 2-to-1 majority (Pragmatist + Purist) presents the stronger functional argument. The convergence ratchet in multi-iteration runs benefits from agents knowing where they are in the sequence. The Mechanist's concern that agents might "over-concede" is speculative and not supported by evidence of actual agent misbehavior from iteration awareness.

2. The SKILL.md already defines `{ITERATION}` at line 230. It is used by the orchestrator for file-path computation. Removing it creates a gap -- the orchestrator needs this value, and documenting it as "orchestrator-only" while hiding it from agents is an artificial distinction in a system where the orchestrator fills templates.

3. The Mechanist's own disputes document acknowledges the 2-to-1 weight and concedes the fix is "not harmful, only unnecessary." This is sufficient for the majority position to stand.

4. The phrasing must be neutral metadata, not a convergence directive. "This is revision iteration {ITERATION}" is appropriate. "This is a late-stage revision -- prioritize convergence" is not.

### Exact Text Changes

**In SKILL.md Phase 3 section, add clarifying note after line 230:**

After:
```
- `{ITERATION}` — current iteration number (1-indexed)
```

Add:
```
  Used by the orchestrator for file-path computation and included in agent prompts as convergence context.
```

**In all four revision templates** (`cooperative/revision.md`, `red-blue/revision.md`, `winner-take-all/revision.md`, `prisoners-dilemma/revision.md`):

Add a metadata line near the top of the template (after the agent identity preamble), e.g.:
```
This is revision iteration {ITERATION}.
```

The exact placement should be after the agent identity/role section and before the "What to Read" / "Files to Read" section, so it serves as context without dominating the prompt.

---

## Ruling 3: `{TARGET_FILES}` Phase 5 Severity Classification

### The Dispute

All three agents agree on the identical fix. The dispute is whether this is P1 (high priority) or P2/Medium (medium priority).

### Each Agent's Position

- **Mechanist**: Design gap, Medium severity. Spec and templates are consistent. This is a design enhancement.
- **Pragmatist**: P1. Silent wrong output in adversarial modes. Synthesis agent asked to evaluate evidence it cannot see.
- **Purist**: Initially Medium, upgraded to P1 in final disputes after accepting the adversarial-mode argument.

### Ruling

**P1. The fix ships in the initial batch alongside the other P1 items.**

Reasoning:

1. The SKILL.md supports four deliberation modes, two of which are explicitly adversarial (red-blue, winner-take-all). In adversarial modes, agents may selectively cite or misrepresent source material. A synthesis agent that cannot access the original target files cannot verify claims against evidence. The synthesis template for several modes instructs the agent to evaluate which positions are "best supported by evidence" -- but without `{TARGET_FILES}`, the agent cannot access that evidence directly.

2. The Mechanist's argument that the information is "indirectly available" through reviews and cross-reviews holds for cooperative mode where agents faithfully quote sources. It does not hold for adversarial modes where selective citation is an expected behavior, not an edge case.

3. The cost of the fix is negligible (add one variable to four templates and one line to SKILL.md). The cost of deferring is that every multi-file adversarial deliberation produces a synthesis with unverifiable claims. The risk-to-effort ratio strongly favors P1.

4. The Mechanist's own revision concedes: "I agree with [the Pragmatist's] reasoning" regarding the adversarial-mode argument.

### Exact Text Changes

**In SKILL.md Phase 5 section, add after line 255:**

After:
```
- `{TARGET_PATH}` — target spec path
```

Add:
```
- `{TARGET_FILES}` — newline-separated list of all target file paths (same as other phases)
```

**In all four synthesis templates** (`cooperative/synthesis.md`, `red-blue/synthesis.md`, `winner-take-all/synthesis.md`, `prisoners-dilemma/synthesis.md`):

In the "What to Read" / "Files to Read" section, add `{TARGET_FILES}` alongside or replacing the single `{TARGET_PATH}` reference for the file-reading instruction. Keep `{TARGET_PATH}` in any context header that identifies the "primary" spec.

---

## Summary of Rulings

| # | Dispute | Ruling | Rationale |
|---|---|---|---|
| 1 | `{PRIOR_FILES}` mechanism | Placeholder (`{PRIOR_FILES_SECTION}`), Phase 1 only, empty-string expansion | One mechanism is simpler; heading mismatch eliminated; scope unanimously agreed |
| 2 | `{ITERATION}` variable | Add to Phase 3 revision templates as neutral metadata; document dual purpose | 2-to-1 majority; functional convergence argument is stronger; phrasing must be neutral |
| 3 | `{TARGET_FILES}` Phase 5 severity | P1 | Adversarial modes require direct evidence access; fix cost is negligible; 2-to-1 majority |

---

## Final Consolidated Fix List (Post-Arbitration)

All disputes resolved. This is the authoritative, actionable fix list.

### P0

1. **Define red-blue role variables**: Add `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` to SKILL.md Phases 1-4.

### P1

2. **Add `{AGENT_DOCS}` to Phase 2 and PD templates**: SKILL.md Phase 2 variable list + prisoners-dilemma `revision.md` and `disputes.md`.
3. **Add `{TARGET_FILES}` to Phase 5 synthesis**: SKILL.md Phase 5 variable list + all four synthesis templates.
4. **Single-anchor template path resolution**: Resolve relative to config file parent; validate post-resolution; specify error messages.
5. **Agent name validation**: Add regex `[a-z0-9][a-z0-9-_]*` to config validation.
6. **`{PRIOR_FILES_SECTION}` placeholder**: Replace section-append with placeholder in Phase 1 review templates; empty-string expansion when no prior files.

### P2

7. **Document iteration filename boundary**: Add "revision_{N-1}.md when N-1=1 resolves to revision.md" note.
8. **Add `{ITERATION}` to revision templates**: Neutral metadata line in all four revision templates; document dual purpose in SKILL.md.
9. **Specify `{ALL_REVISIONS}` scope**: Final revision paths only, not intermediate.
10. **Document overwrite-without-warning behavior**: Re-runs overwrite; stale files not cleaned.
11. **Validation error format rule**: All errors must name field, value, constraint. Keep 3 arbiter examples.

### P3

12. **Specify `disputes_remain` heading per mode**: Document expected heading; optionally add machine-readable line.
13. **State final-revision-path formula**: Explicit formula with iteration-1 special case.
14. **Elevate `run_in_background` directive**: Per-phase execution mode statements.
15. **State agent model selection**: All subagents use orchestrator's model.
16. **Specify path-list variable format**: One bare absolute path per line, no prefix.
17. **Note cross-review overwrite semantics**: Cross-reviews represent final iteration only.
