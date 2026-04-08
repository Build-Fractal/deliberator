# Enforcement Audit Revision: The Pragmatist

**Author**: The Pragmatist
**Date**: 2026-03-19
**Inputs**: Original review, cross-reviews from The Mechanist and The Purist, my cross-reviews of both.

---

## Disposition of Original Findings

### Finding 1: Agent Counts Per Phase
**HELD.** No challenges from either reviewer. The math is correct, the spec is unambiguous. No change.

---

### Finding 2a: Iteration Loop Diagram
**HELD.** Both reviewers confirm the iteration loop and phase ordering are well-specified. Safe agreement across all three reviews.

---

### Finding 2b: Revision Filename at Iteration Boundary
**HELD.** All three reviews independently converge on the same problem and the same fix. The Purist (SA-3) and the Mechanist (SA-3) both confirm: when N=2, `revision_{N-1}.md` must resolve to `revision.md`, not `revision_1.md`. Explicit documentation is needed.

**Priority remains P2.** The system works for single-iteration runs (the common case). Multi-iteration is where this bites, and the fix is a single clarifying sentence.

---

### Finding 2c: `{ITERATION}` Dead Variable
**MODIFIED.** Originally rated P3 (cosmetic). The Purist's DC-2 argues this is functional, not cosmetic: without an iteration signal in the prompt, revision agents in iteration 3 cannot distinguish their context from iteration 1. The convergence ratchet is implicit in cross-review content rather than explicit in the prompt.

I concede the Purist's point partially. The variable is not merely "useful metadata" -- it serves a convergence-signaling purpose that becomes material when cross-reviews are vague or repetitive. However, the Mechanist did not flag this at all, and in practice most deliberations will run 1-2 iterations where the issue is moot.

**Revised verdict: Fragile, P2** (upgraded from P3). Fix: add `{ITERATION}` to the revision template header (e.g., "## Revision (Iteration {ITERATION})") so agents have an explicit signal of where they are in the convergence loop.

---

### Finding 3b: Phase 2 Missing `{AGENT_DOCS}`
**MODIFIED.** Originally rated P1 for cooperative mode only. The Purist's DC-1 correctly identifies that my fix ("add `{AGENT_DOCS}` to the Phase 2 variable list") is too narrow: the prisoners-dilemma `revision.md` and `disputes.md` templates also omit `{AGENT_DOCS}`, stripping agents of grounding documentation in Phases 3 and 4 of that mode.

I concede: the fix must be broadened. However, I maintain the cooperative-mode Phase 2 fix is the highest-priority instance because cooperative is the default and most exercised path. The prisoners-dilemma template omissions are a separate but related fix.

**Revised fix**: (1) Add `{AGENT_DOCS}` to the Phase 2 variable list in SKILL.md. (2) Add a general variable inheritance statement: "All Phase 1 variables are available in all subsequent phases unless explicitly overridden." (3) Add `{AGENT_DOCS}` placeholder to prisoners-dilemma `revision.md` and `disputes.md` templates. **Priority remains P1**, scope expanded.

---

### Finding 3e: Phase 5 Missing `{TARGET_FILES}`
**HELD.** Unanimous safe agreement across all three reviews. The synthesis template needs `{TARGET_FILES}`, not just `{TARGET_PATH}`. Priority remains P1.

---

### Finding 4: `{PRIOR_FILES}` Injection Scope
**MODIFIED.** Originally rated Fragile, P2, with the judgment that Phase 1-only injection is "likely acceptable."

The Mechanist's DC-1 argues I underrated this: the mechanism is not a placement problem but a design-level divergence (runtime string surgery vs. template placeholder substitution). The Purist raises heading mismatch (Gap 4.1) and scope ambiguity (Gap 4.2).

I concede on severity but not on the fix direction. The Mechanist's proposed fix (add `{PRIOR_FILES_SECTION}` placeholder to every template) degrades prompt quality when no prior files exist -- empty section headers in agent prompts are noise. The Purist's fix (inject everywhere literally) creates redundancy in Phases 5-6 where the full deliberation record already incorporates prior context.

**Revised position**: `{PRIOR_FILES}` injection should be explicitly scoped to Phases 1-3 only. Phases 1 agents absorb the prior context; Phases 2-3 agents benefit from it when evaluating and revising positions. Phases 4-6 agents have the complete deliberation record which already reflects prior context. The instruction should be moved to a standalone "Cross-Phase Injections" section before the per-phase instructions, eliminating the positional ambiguity.

**Revised verdict: Fragile, P1** (upgraded from P2). The injection scope must be resolved explicitly, not left to LLM interpretation.

---

### Finding 5a/5b: Phase 6 Trigger Evaluation
**MODIFIED.** Originally rated Fragile, P3 with "no critical fix needed."

The Purist's T-1 makes a fair point: unnecessary Phase 6 invocations produce phantom arbitration artifacts that downstream consumers cannot distinguish from legitimate rulings. "No fix needed" was an overstatement.

I concede this should be a low-priority fix rather than no fix. However, I maintain that the fail-safe design is correct and that investing in structured output (JSON/YAML frontmatter) is disproportionate for a system where the orchestrator is an LLM parsing LLM output.

**Revised verdict: Fragile, P3** (unchanged priority, but "no fix needed" revised to "low-priority fix"). Fix: instruct the synthesis template to include a machine-readable summary line (e.g., `<!-- disputes: N -->`) that the trigger can parse deterministically, with the markdown parsing as fallback.

---

### Finding 6b: Agent Name Validation
**HELD.** Both reviewers agree this is necessary. The Mechanist's DC-3 correctly notes that validation is "another instruction to the executor LLM" and therefore subject to the same instructional-enforcement limitation as everything else in the system. I acknowledge this but maintain the fix is still worth making: a clear regex rule (`[a-z0-9][a-z0-9-_]*`) is the kind of instruction LLMs follow reliably because it is mechanical and unambiguous.

**Priority remains P1.** The downstream corruption from bad names (every cross-review, revision, and synthesis affected) justifies the priority even with the enforcement caveat.

---

### Finding 7: Template Path Resolution
**MODIFIED.** Originally rated P1 with a three-step resolution algorithm. The Purist's DC-3 correctly identifies that my fix introduces multi-anchor ambiguity: three search strategies with two different anchors can resolve to the wrong `conversus/` directory in nested-submodule layouts.

I concede the three-step fallback chain is overengineered. The Purist's counter-proposal is better: the config file's location is the single anchor, and the template directory is a path relative to it.

The Mechanist's T-1 adds that post-resolution validation is needed: verify the resolved path contains the expected template files before proceeding.

**Revised fix**: (1) The template directory is resolved relative to the `conversus.yml` config file's parent directory -- one anchor, no fallback chain. (2) After resolution, verify `{TEMPLATE_DIR}/review.md` exists; abort with a clear error if not. **Priority remains P1.**

---

## New Findings Accepted from Cross-Reviews

### NEW-1: Red-Blue Mode Variables Are a Blocking Defect
**CONCEDED from The Purist (Gap 1.1) and The Mechanist (Claim 10, partial).**

My original audit scoped to cooperative mode only and declared the system works "for all configurations" after four fixes. This was an overstatement. The Purist identified `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` as used in all four red-blue templates but undefined anywhere in SKILL.md. This is a guaranteed rendering failure for any red-blue deliberation -- literal `{AGENT_ROLE}` strings will appear in agent prompts.

In my cross-review of the Purist (SA-3), I explicitly acknowledged this as "unambiguously correct" and "the highest-priority fix from either review." I stand by that assessment.

**Verdict: Broken. Priority: P0.** Fix: add explicit variable definitions to SKILL.md mapping `config.agents[].role` to `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` in Phase 1, 2, and 3 respectively. Add these to the red-blue mode variable tables.

---

### NEW-2: Prisoners-Dilemma Template Omissions
**CONCEDED from The Purist (DC-1).**

The prisoners-dilemma `revision.md` and `disputes.md` templates omit `{AGENT_DOCS}`. This is a separate defect from the cooperative Phase 2 `{AGENT_DOCS}` gap (Finding 3b). Agents in prisoners-dilemma Phases 3-4 lose access to their grounding documentation.

**Verdict: Broken. Priority: P1.** Fix: add `{AGENT_DOCS}` to the prisoners-dilemma revision and disputes templates.

---

### NEW-3: Audit Scope Overstatement
**CONCEDED from The Purist (T-2) and The Mechanist (DC-2).**

My original summary said "apply those four [P1 fixes] and this skill works end-to-end for all configurations." This was wrong. My audit verified cooperative mode only, and red-blue mode has independent blocking defects. The revised conclusion must be scoped to what was actually verified.

---

## Findings I Reject

### REJECTED: `{PRIOR_FILES}` Should Become a Template Placeholder (Mechanist DC-1)

The Mechanist advocates converting the runtime append to a `{PRIOR_FILES_SECTION}` template variable. I reject this for the reasons stated in my cross-review: templates would contain empty section headers when no prior files exist, producing awkward prompts. The runtime append design is intentional -- it keeps templates clean when the optional field is absent. The fix is to clarify scope and placement of the instruction, not to change the injection mechanism.

### REJECTED: Context Isolation as High Severity (Mechanist DC-2)

The Mechanist rates agent context isolation as High severity because agents can technically read any file on the filesystem. I reject this rating in the context of this system. The templates are the enforcement mechanism in a prompt-instruction architecture. Well-structured "What to Read" sections with explicit file paths provide sufficient practical isolation for LLM agents, which follow structured templates reliably. Elevating this to High severity is equivalent to rejecting the entire prompt-instruction paradigm, which the Mechanist's own conclusion accepts as valid.

### REJECTED: Exhaustive Error Message Templates (Purist DC-1)

The Purist demands all 14 validation rules have formally specified error messages. I reject this for the reasons in my cross-review: it transforms a behavioral contract into a string-literal contract, creates maintenance burden, and flattens the signal between subtle validations and obvious ones. An LLM orchestrator will produce sensible error messages from behavioral instructions. The three arbiter-specific messages exist because those validations are non-obvious; the others are self-explanatory.

---

## Revised Prioritized Fix List

### P0 -- Blocking Defects (red-blue mode broken)

| # | Finding | Location | Fix |
|---|---------|----------|-----|
| P0-1 | Red-blue role variables undefined | SKILL.md + red-blue templates | Define `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` in SKILL.md variable tables; map from `config.agents[].role` |

### P1 -- Silent Wrong Output or Execution Failure

| # | Finding | Location | Fix |
|---|---------|----------|-----|
| P1-1 | `{AGENT_DOCS}` missing from Phase 2 variable list | SKILL.md Phase 2 section | Add `{AGENT_DOCS}` to Phase 2 variables; add general inheritance statement for Phase 1 variables |
| P1-2 | `{AGENT_DOCS}` missing from prisoners-dilemma templates | `templates/prisoners-dilemma/revision.md`, `disputes.md` | Add `{AGENT_DOCS}` placeholder to both templates |
| P1-3 | `{TARGET_FILES}` missing from Phase 5 synthesis | All four `synthesis.md` templates + SKILL.md Phase 5 | Add `{TARGET_FILES}` alongside `{TARGET_PATH}` in synthesis "What to Read" section |
| P1-4 | Agent name validation absent | SKILL.md Step 1 validation | Add regex constraint: `[a-z0-9][a-z0-9-_]*`; reject invalid names at config parse |
| P1-5 | Template path resolution ambiguous | SKILL.md Step 3 | Single-anchor resolution relative to config file parent; post-resolution existence check |
| P1-6 | `{PRIOR_FILES}` injection scope ambiguous | SKILL.md (currently in Phase 1 section) | Move to standalone "Cross-Phase Injections" section; explicitly scope to Phases 1-3 |

### P2 -- Correctness Under Non-Default Conditions

| # | Finding | Location | Fix |
|---|---------|----------|-----|
| P2-1 | Revision filename boundary ambiguity | SKILL.md iteration loop section | Add note: "revision_{N-1}.md when N-1=1 resolves to revision.md (no suffix)" |
| P2-2 | `{ITERATION}` unused in revision template | Revision templates + SKILL.md Phase 3 | Add `{ITERATION}` to revision template header for convergence signaling |

### P3 -- Low-Priority Hardening

| # | Finding | Location | Fix |
|---|---------|----------|-----|
| P3-1 | Phase 6 trigger parsing fragile | Synthesis template + SKILL.md Phase 6 trigger | Add machine-readable `<!-- disputes: N -->` line; keep markdown parsing as fallback |

---

## Revised Summary Scorecard

| # | Finding | Original Verdict | Revised Verdict | Original Priority | Revised Priority | Disposition |
|---|---------|-----------------|-----------------|-------------------|-----------------|-------------|
| 1 | Agent counts per phase | Works | Works | -- | -- | Held |
| 2a | Iteration loop diagram | Works | Works | -- | -- | Held |
| 2b | Revision filename boundary | Fragile | Fragile | P2 | P2 | Held |
| 2c | `{ITERATION}` dead variable | Fragile | Fragile | P3 | P2 | Modified |
| 3b | Phase 2 `{AGENT_DOCS}` | Fragile | Fragile | P1 | P1 | Modified (scope expanded) |
| 3e | Phase 5 `{TARGET_FILES}` | Fragile | Fragile | P1 | P1 | Held |
| 4 | `{PRIOR_FILES}` injection | Fragile | Fragile | P2 | P1 | Modified (severity upgraded) |
| 5a | Trigger evaluation | Fragile | Fragile | P3 | P3 | Modified (no-fix to low-fix) |
| 6b | Agent name validation | Broken | Broken | P1 | P1 | Held |
| 7 | Template path resolution | Fragile | Fragile | P1 | P1 | Modified (algorithm simplified) |
| NEW-1 | Red-blue role variables | -- | Broken | -- | P0 | Conceded from Purist/Mechanist |
| NEW-2 | PD template `{AGENT_DOCS}` | -- | Broken | -- | P1 | Conceded from Purist |

**Revised bottom line**: The original audit verified cooperative mode thoroughly but overstated coverage. Red-blue mode has a blocking defect (P0) that my scoping missed. The revised fix list contains 1 P0, 6 P1, 2 P2, and 1 P3 item. Applying P0 + P1 fixes makes the system work end-to-end for cooperative and prisoners-dilemma modes and unblocks red-blue mode. The P2 fixes improve multi-iteration convergence quality. The P3 fix reduces phantom arbitration artifacts.
