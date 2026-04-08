# Final Disputes: The Pragmatist

**Author**: The Pragmatist
**Date**: 2026-03-19
**Phase**: Disputes (final)
**Inputs**: Revised positions from The Mechanist, The Pragmatist, and The Purist.

---

## Remaining Disputes

### Dispute 1: `{PRIOR_FILES}` Injection Mechanism — Placeholder vs. Runtime Append

**The split**: The Purist now concedes to the Mechanist that a single `{PRIOR_FILES_SECTION}` placeholder replacing the section-append mechanism is the correct fix. The Mechanist's revision proposes standardizing section headings OR specifying the injection target per mode, but does not adopt the placeholder. My revision explicitly rejects the placeholder approach.

Two positions remain:

- **Mechanist + Purist (converged)**: Replace the append mechanism with a `{PRIOR_FILES_SECTION}` placeholder in all Phase 1 templates. The placeholder expands to either the formatted block or empty string. This eliminates heading-name dependency entirely.
- **Pragmatist (dissenting)**: Keep the runtime append mechanism. Move the injection instruction to a standalone "Cross-Phase Injections" section, explicitly scope to Phases 1-3, and standardize the heading names for reliability.

**My final position**: I withdraw my objection. The Purist's concession to the Mechanist is well-reasoned: one injection mechanism is simpler than two, and a placeholder that expands to empty string avoids the "awkward empty section header" problem I raised if implemented correctly (the placeholder replaces the entire section including its heading, not just its body). The heading standardization becomes a cosmetic item rather than a functional one. I concede to the Mechanist-Purist position, with one constraint: the placeholder must expand to either the complete section (heading + file list) or nothing at all. It must not produce an orphaned "## Prior Context" header with no content beneath it.

**Disposition**: Resolved. Placeholder mechanism with whole-section-or-nothing expansion. The injection scope question (Phases 1-3 vs. Phase 1 only) is a separate, minor item addressed in Dispute 2.

---

### Dispute 2: `{PRIOR_FILES}` Injection Scope — Phase 1 Only vs. Phases 1-3

**The split**: The Purist holds that injection should apply to Phase 1 only, arguing that prior context propagates naturally through Phase 1 agents' outputs. My revision scoped injection to Phases 1-3, arguing that cross-review and revision agents also benefit from direct access. The Mechanist's revision does not take a firm position on scope.

- **Purist**: Phase 1 only. Prior context propagates through agent outputs.
- **Pragmatist**: Phases 1-3. Agents evaluating and revising positions benefit from direct access to what came before.

**My final position**: I concede to the Purist. The propagation argument is sound: Phase 1 agents absorb prior context into their reviews, and every Phase 2 cross-reviewer reads those reviews. Phase 3 revision agents read both the original reviews and the cross-reviews. Injecting prior files into Phases 2-3 adds prompt bulk without adding information the agents cannot already access through the deliberation artifacts. Phase 1 only is sufficient.

**Disposition**: Resolved. Phase 1 only.

---

### Dispute 3: `{ITERATION}` — Remove, Keep as Orchestrator State, or Add to Templates

**The split**: Three distinct positions remain after revision.

- **Mechanist**: `{ITERATION}` is Low-severity dead weight. Either remove from SKILL.md or document as orchestrator-only state. Do NOT inject into templates (could change agent behavior).
- **Purist**: `{ITERATION}` should be added to Phase 3 revision templates as convergence context. Agents need an explicit signal of where they are in the loop. Medium severity.
- **Pragmatist**: Upgraded to Fragile/P2. Should be added to revision template header for convergence signaling.

In practice, the Pragmatist and Purist converge against the Mechanist. The question: should agents know what iteration they are on?

**My final position**: I hold that agents benefit from knowing their iteration number. The Mechanist's concern that this "could change their behavior" is precisely the point: a revision-3 agent should behave differently from a revision-1 agent because it is expected to converge, not re-argue. The Mechanist's own revision acknowledges that the iteration file-naming logic is Medium severity and that the orchestrator needs `{ITERATION}` for path computation. Documenting it as orchestrator-only while agents operate in ignorance of their position in the convergence loop is an artificial restriction.

However, the severity is Low, not Medium. The common case is 1-2 iterations where the cross-review content carries sufficient convergence signal. The explicit iteration number is a quality improvement for edge cases (iteration 3+), not a correctness requirement.

**Disposition**: Unresolved. 2-to-1 split (Pragmatist + Purist vs. Mechanist). Add `{ITERATION}` to revision templates. Severity: Low (Pragmatist compromise between Purist's Medium and Mechanist's Low).

---

## Convergence

### Convergence 1: Red-Blue Role Variables Are the P0 Fix

All three reviewers independently confirmed that `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` being undefined in SKILL.md is the single highest-priority defect. The Mechanist held this from original findings. The Purist identified it as Gap 1.1. I adopted it as NEW-1 after the Purist's cross-review exposed my cooperative-mode-only audit scope.

**Consensus**: P0. Add variable definitions to SKILL.md Phase 1-4 variable sections mapping from `config.agents[].role`. No reviewer disputes any aspect of the diagnosis, severity, or fix.

---

### Convergence 2: `{AGENT_DOCS}` Must Be Added to Phase 2 and Prisoners-Dilemma Templates

All three reviewers agree that `{AGENT_DOCS}` is missing from the Phase 2 variable list in SKILL.md. The Purist further identified the prisoners-dilemma template omissions in Phases 3-4. I conceded this broader scope in my revision (NEW-2). The Mechanist's disaggregated Claim 10 lists `{AGENT_DOCS}` as Broken/Medium.

**Consensus**: P1. Two fixes: (1) add `{AGENT_DOCS}` to SKILL.md Phase 2 variable list, (2) add `{AGENT_DOCS}` to prisoners-dilemma `revision.md` and `disputes.md` templates. No remaining disagreement.

---

### Convergence 3: `{TARGET_FILES}` Must Be Added to Phase 5 Synthesis

All three reviewers independently identified that Phase 5 synthesis templates need `{TARGET_FILES}` in addition to `{TARGET_PATH}` for multi-file targets. The Mechanist reclassified this from "Broken" to "Design gap." The Purist calls it Medium (consistent-but-insufficient). I held it at P1.

**Consensus**: P1. Add `{TARGET_FILES}` to Phase 5 variable definitions and all four synthesis templates. The severity label varies (Mechanist: Medium design gap; Purist: Medium; Pragmatist: P1) but the fix is identical across all three revisions.

---

### Convergence 4: Template Path Resolution — Single Anchor, Config-Relative

All three reviewers converge on the same resolution algorithm: template directory is resolved relative to the `conversus.yml` config file's parent directory. My original three-step fallback was overengineered (the Purist correctly identified multi-anchor ambiguity). The Purist added the requirement for specified error messages on resolution failure. The Mechanist's revision does not directly address this but does not contest the approach.

**Consensus**: P1. Single-anchor resolution relative to config file parent. Post-resolution validation that expected template files exist. Specified error messages for failure cases. My original multi-step algorithm is withdrawn.

---

### Convergence 5: The Systemic Finding — Templates Are the Enforcement Surface

All three reviewers converged on the reframing. The Mechanist withdrew "zero enforcement surface" and revised to: "Conversus enforces its rules through template structure and prompt instruction. Templates are the primary enforcement surface." The Purist held from the start that spec-template alignment is the meaningful metric. I held from the start that in a system where the LLM is the engine, well-structured instructions are the enforcement mechanism.

**Consensus**: The priority is to eliminate spec-template contradictions (Broken items), then reduce ambiguity (Fragile items). Template alignment is the testable quality metric. No reviewer disputes this framing.

---

## Final Position

The three-reviewer audit has produced a remarkably tight consensus. Of the original 20+ findings across three reviews, only one dispute remains genuinely unresolved (the `{ITERATION}` template injection question, which splits 2-to-1 and concerns a Low-severity item). Every Broken and P0/P1 item has unanimous agreement on both diagnosis and fix.

**Consolidated fix list from the Pragmatist's perspective:**

| Priority | Fix | Status |
|---|---|---|
| P0 | Define `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` in SKILL.md | Unanimous |
| P1 | Add `{AGENT_DOCS}` to Phase 2 variable list and PD templates | Unanimous |
| P1 | Add `{TARGET_FILES}` to Phase 5 synthesis | Unanimous |
| P1 | Single-anchor template path resolution with error behavior | Unanimous |
| P1 | `{PRIOR_FILES_SECTION}` placeholder mechanism, Phase 1 only, whole-section-or-nothing | Resolved (Pragmatist conceded to Mechanist-Purist) |
| P1 | Agent name validation (`[a-z0-9][a-z0-9-_]*`) | Unanimous |
| P2 | Document revision filename boundary (iteration 1 = no suffix) | Unanimous |
| P2 | Add `{ITERATION}` to revision templates | 2-to-1 (Pragmatist + Purist) |
| P2 | Specify `{ALL_REVISIONS}` scope (final revisions only) | Unanimous (Purist finding, uncontested) |
| P3 | Machine-readable disputes line in synthesis output | Unanimous |
| P3 | Document overwrite-without-warning behavior on re-run | Unanimous (Purist finding, Pragmatist remedy) |
| P3 | Validation error format rule (name field, value, constraint) | Unanimous (revised from Purist's original 14-template proposal) |

**disputes_remain: false**

The single unresolved item (`{ITERATION}` template injection) is a Low-to-Medium severity quality improvement where the majority position is clear and the dissenting position (Mechanist) does not argue the fix is harmful, only that it is unnecessary. This does not warrant arbitration. The 2-to-1 majority should stand.

The audit is complete. Apply the P0 and P1 fixes, and the Conversus SKILL.md works end-to-end for all four deliberation modes.
