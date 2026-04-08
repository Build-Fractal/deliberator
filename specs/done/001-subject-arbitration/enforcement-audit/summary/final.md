# Enforcement Audit Synthesis: Conversus SKILL.md

**Synthesizer**: Neutral arbiter
**Date**: 2026-03-19
**Inputs**: 15 artifacts (review, revision, disputes, 2 cross-reviews) from The Mechanist, The Pragmatist, and The Purist

---

## Process Stats

| Metric | Value |
|---|---|
| Agents | 3 (Mechanist, Pragmatist, Purist) |
| Phases completed | 4 (Review, Cross-Review, Revision, Disputes) |
| Artifacts produced | 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes) |
| Unique findings (pre-dedup) | ~35 across all three reviews |
| Unique findings (post-dedup) | 16 distinct issues |
| Unanimous convergence items | 8 |
| Resolved disputes (during process) | 3 (resolved by agents before final disputes) |
| Remaining disputes | 3 |
| Concessions made | Mechanist: 6, Pragmatist: 4, Purist: 4 |

---

## Unanimous Convergence

These items have full agreement from all three agents on diagnosis, severity category, and fix direction.

### C-1: Red-blue role variables are a blocking defect (P0)

`{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` are used in all four red-blue templates but never defined in SKILL.md. This is the single highest-priority defect. Any red-blue deliberation will produce literal `{AGENT_ROLE}` strings in agent prompts.

**Fix**: Add variable definitions to SKILL.md Phases 1-4 mapping `config.agents[].role` to the three template variables.

**Sources**: Mechanist Claim 10C, Purist Gap 1.1, Pragmatist NEW-1 (conceded from Purist)

### C-2: `{AGENT_DOCS}` must be added to Phase 2 variable list and prisoners-dilemma templates (P1)

`{AGENT_DOCS}` is used in the cooperative cross-review template but not documented in SKILL.md's Phase 2 variable list. Additionally, prisoners-dilemma `revision.md` and `disputes.md` templates omit `{AGENT_DOCS}` entirely, stripping agents of grounding documentation in Phases 3-4.

**Fix**: (1) Add `{AGENT_DOCS}` to SKILL.md Phase 2 variable list. (2) Add `{AGENT_DOCS}` to prisoners-dilemma `revision.md` and `disputes.md` templates. (3) Consider adding a general variable inheritance statement for Phase 1 variables.

**Sources**: Mechanist Claim 10E, Pragmatist Finding 3b + NEW-2, Purist appendix (promoted)

### C-3: `{TARGET_FILES}` must be added to Phase 5 synthesis (P1)

All four synthesis templates use only `{TARGET_PATH}` (single file). In multi-file target runs, the synthesis agent cannot verify claims against all original source files.

**Fix**: Add `{TARGET_FILES}` to Phase 5 variable definitions in SKILL.md and to all four synthesis templates.

**Sources**: Mechanist Claim 8, Pragmatist Finding 3e, Purist appendix (adopted)

### C-4: Template path resolution must use a single anchor (P1)

The current "walk up from CWD" instruction is fragile. The Pragmatist's original three-step algorithm introduced multi-anchor ambiguity (identified by Purist). All three converge on: resolve relative to `conversus.yml` config file's parent directory.

**Fix**: (1) Template directory resolved relative to config file parent -- one anchor, no fallback chain. (2) Post-resolution validation that expected template files exist. (3) Specified error messages for resolution failures.

**Sources**: Pragmatist Finding 7 (revised), Purist Gap 6.1 (revised), Mechanist T-1

### C-5: Agent name validation (P1)

Agent names with special characters, spaces, or slashes produce invalid filesystem paths. Case-insensitive collisions cause silent cross-review overwrites.

**Fix**: Add validation rule: agent names must match `[a-z0-9][a-z0-9-_]*`. Reject invalid names at config parse time.

**Sources**: Pragmatist Edge Cases 2-3, Purist (adopted), Mechanist (acknowledged)

### C-6: Iteration file-naming boundary must be documented (P2)

When N=2, `revision_{N-1}.md` must resolve to `revision.md`, not `revision_1.md`. All three agents identified this independently.

**Fix**: Add explicit note to SKILL.md: "When N-1 equals 1, the file path is `revision.md` (no numeric suffix), not `revision_1.md`."

**Sources**: Mechanist Claim 6, Pragmatist Finding 2b, Purist Gap 5.1/SA-3

### C-7: `{ALL_REVISIONS}` scope must be specified for multi-iteration (P2)

For iterations > 1, it is ambiguous whether `{ALL_REVISIONS}` includes all intermediate revisions or only the final ones.

**Fix**: Explicitly state that `{ALL_REVISIONS}` contains only final revision paths (from the last iteration), not intermediate revisions.

**Sources**: Purist Gap 5.2 (uncontested by either reviewer)

### C-8: Templates are the enforcement surface (systemic finding)

All three agents converge on a shared architectural understanding: Conversus enforces rules through template structure and prompt instruction to an LLM executor. Templates are the primary enforcement surface. Where templates and SKILL.md align, the system works reliably. Where they contradict, even a perfect executor produces wrong output. The priority is: fix spec-template contradictions first, then reduce ambiguity, then harden documentation.

**Sources**: Mechanist revised systemic finding, Pragmatist T-2, Purist SA-3

---

## Remaining Disputes

### Dispute 1: `{PRIOR_FILES}` injection mechanism -- placeholder vs. runtime append

All three agents agree the current state is defective (heading mismatch, scope ambiguity). They disagree on the fix mechanism.

- **Mechanist + Purist (partial convergence)**: Replace the section-append mechanism with a `{PRIOR_FILES_SECTION}` placeholder in all Phase 1 templates. The placeholder expands to either the formatted block (heading + file list) or empty string. This eliminates the heading-name dependency and normalizes to a single injection mechanism (placeholder substitution). The Purist initially conceded to this in revision, then partially retracted in disputes -- arguing that empty-string expansion is indistinguishable from a silent injection failure in a system with no validator, and proposing that if the placeholder approach is adopted, empty expansion should produce a comment line (e.g., `<!-- No prior files for this deliberation -->`) rather than nothing.

- **Pragmatist (initially dissenting, then conceded)**: The Pragmatist initially rejected the placeholder approach (empty section headers degrade prompt quality) and advocated keeping the runtime append mechanism with clearer scoping. In the final disputes, the Pragmatist withdrew this objection and conceded to the Mechanist-Purist placeholder position, with the constraint that the placeholder must expand to the complete section (heading + content) or nothing at all -- no orphaned headers.

- **Purist (final position)**: The Purist partially retracted their earlier concession and advocated retaining the append mechanism with explicit Phase-1-only scoping, heading standardization to "What to Read" across all modes, and moving the instruction to a standalone "Cross-Phase Injections" section. Alternatively, if the placeholder is adopted, empty expansion must produce a comment line, not empty string.

**Scope sub-dispute**: All three agree injection should be Phase 1 only. The Pragmatist initially proposed Phases 1-3 but conceded to Phase 1 only in final disputes.

**Net positions at close**: The mechanism choice (placeholder vs. append) remains a 2-way split. The Pragmatist conceded to the placeholder but the Purist partially retracted, creating an unstable consensus. The scope question (Phase 1 only) is resolved.

### Dispute 2: `{ITERATION}` -- remove, keep as orchestrator state, or add to templates

- **Mechanist**: Low severity. `{ITERATION}` is dead weight or orchestrator-only state. Do NOT inject into templates -- iteration awareness could change agent behavior unpredictably (agents may over-concede to reach closure or treat their position as more authoritative). The convergence ratchet should be driven by cross-review substance, not a meta-signal.

- **Pragmatist**: P2/Fragile. Add `{ITERATION}` to the revision template header (e.g., "Revision (Iteration {ITERATION})") for convergence signaling. The common case (1-2 iterations) makes this Low impact, but it is a quality improvement for edge cases.

- **Purist**: Medium severity. `{ITERATION}` is functional, not cosmetic. Without an iteration signal, revision agents in iteration 3+ cannot distinguish a refinement pass from a first pass. Convergence depends entirely on implicit cross-review content. Add to Phase 3 templates as metadata and document dual purpose (orchestrator file-path computation + agent convergence signaling).

**Split**: 2-to-1 (Pragmatist + Purist favor template inclusion; Mechanist dissents). The Mechanist acknowledges the 2-to-1 weight and does not argue the fix is harmful, only unnecessary.

### Dispute 3: `{TARGET_FILES}` Phase 5 -- severity classification

All three agents agree on the identical fix (add `{TARGET_FILES}` to Phase 5). The dispute is classification only.

- **Mechanist**: Design gap, Medium severity. The spec and templates are internally consistent (both use `{TARGET_PATH}` only). This is a design enhancement.

- **Pragmatist**: P1/Fragile. Silent wrong output in multi-target adversarial modes justifies higher priority. The synthesis agent is asked to evaluate evidence it cannot see.

- **Purist**: Initially Medium, then upgraded to P1 in final disputes after accepting the Pragmatist's adversarial-mode argument. The synthesis agent cannot verify claims against original sources in adversarial modes.

**Split**: 2-to-1 (Pragmatist + Purist favor P1; Mechanist holds Medium). The fix is identical regardless of classification; only prioritization differs.

---

## Prioritized Fix List

Consolidated, deduplicated, and ordered by priority. Items marked with agent agreement status.

### P0 -- Blocking (must fix before any red-blue deliberation)

| # | Fix | Description | Agreement |
|---|---|---|---|
| 1 | Define red-blue role variables | Add `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` definitions to SKILL.md Phases 1-4 variable sections, mapping from `config.agents[].role` | Unanimous |

### P1 -- High (produces incorrect output or silent degradation)

| # | Fix | Description | Agreement |
|---|---|---|---|
| 2 | Add `{AGENT_DOCS}` to Phase 2 and PD templates | Add to SKILL.md Phase 2 variable list; add to prisoners-dilemma `revision.md` and `disputes.md` templates; consider general inheritance statement | Unanimous |
| 3 | Add `{TARGET_FILES}` to Phase 5 synthesis | Add to SKILL.md Phase 5 variable list and all four synthesis templates alongside `{TARGET_PATH}` | Unanimous on fix; disputed severity (P1 vs Medium) |
| 4 | Single-anchor template path resolution | Resolve template directory relative to config file parent; post-resolution validation; specified error messages | Unanimous |
| 5 | Agent name validation | Add regex constraint `[a-z0-9][a-z0-9-_]*` to config validation; reject invalid names | Unanimous |
| 6 | Resolve `{PRIOR_FILES}` injection | Fix the heading mismatch and scope ambiguity; scope to Phase 1 only; mechanism disputed (placeholder vs. append) | Unanimous on need; disputed mechanism |

### P2 -- Medium (ambiguity affecting output quality)

| # | Fix | Description | Agreement |
|---|---|---|---|
| 7 | Document iteration filename boundary | Add note: "When N-1=1, the path is `revision.md` (no suffix), not `revision_1.md`" | Unanimous |
| 8 | Resolve `{ITERATION}` variable | Either add to Phase 3 revision templates for convergence signaling, or document as orchestrator-only state | Disputed (2-to-1 favor template inclusion) |
| 9 | Specify `{ALL_REVISIONS}` scope | State that `{ALL_REVISIONS}` contains only final revision paths, not intermediate | Unanimous |
| 10 | Document overwrite-without-warning behavior | State that re-runs overwrite current files without warning; stale files from removed agents are not cleaned | Unanimous (Purist finding, uncontested) |
| 11 | Validation error format rule | Add general rule: all config errors must name the field, value, and constraint. Keep existing 3 arbiter messages as examples | Unanimous (revised from Purist's original 14-template proposal) |

### P3 -- Low (documentation, hardening, non-blocking)

| # | Fix | Description | Agreement |
|---|---|---|---|
| 12 | Specify `disputes_remain` heading per mode | Document expected heading for each synthesis mode; optionally add machine-readable `<!-- disputes: N -->` line | Unanimous |
| 13 | State final-revision-path formula | Add single explicit formula with iteration-1 special case | Unanimous |
| 14 | Elevate `run_in_background` directive | Move to phase execution headers or add per-phase execution mode statement | Unanimous (Purist finding, uncontested) |
| 15 | State agent model selection | "All subagents use the orchestrator's model. Per-agent model selection is not supported." | Unanimous (Purist finding, uncontested) |
| 16 | Specify path-list variable format | State that path-list variables expand to one bare absolute path per line, no prefix characters | Unanimous (Purist finding, uncontested) |
| 17 | Note cross-review overwrite semantics | State in Phase 5 variable definitions that cross-reviews represent only the final iteration | Unanimous (Purist finding, uncontested) |
