# Cross-Review of The Pragmatist's Enforcement Audit

**Reviewer**: The Mechanist
**Reviewed**: The Pragmatist
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: The Pragmatist underrates `{PRIOR_FILES}` as merely a placement problem; it is a design-level break

The Pragmatist identifies `{PRIOR_FILES}` injection scope as "Fragile" (Finding #4, P2 priority) and frames the issue as one of textual placement -- the append instruction lives inside the Phase 1 section but says "every agent prompt," so an LLM might miss it. The proposed fix is to move the instruction to a general section.

This misses the structural problem entirely. `{PRIOR_FILES}` does not appear in ANY template across ALL modes. Zero occurrences. The Pragmatist's framing implies that once the instruction is moved to a more prominent location, the executor will faithfully append the block. But the issue is not where the instruction sits in SKILL.md -- the issue is that the injection mechanism is runtime string surgery performed by an LLM, with no template slot to anchor it. Every other variable works via placeholder substitution; this one requires the executor to understand a second, undocumented injection pattern (read instruction, conditionally append block to already-filled template).

The Pragmatist even argues the impact is low because "prior files matter most for Phase 1" and "even if an LLM only injects it in Phase 1, the output will likely be acceptable." This is a dangerous conclusion. It normalizes silent data loss as acceptable degradation. If `prior:` files contain the previous iteration's final synthesis or a foundational spec, agents in Phases 2-4 operating without that context are not "likely acceptable" -- they are reasoning in a vacuum about material they were supposed to have read. The Pragmatist's own Fix 1 and Fix 2 are P1 for lesser variable mismatches; `{PRIOR_FILES}` deserves at least equal severity.

**My audit rated this Broken (Medium severity)**. The Pragmatist rated it Fragile (P2). The gap is not cosmetic -- it determines whether the fix is "reword an instruction" or "add template slots and change the injection model."

---

### DC-2: Red-blue mode variables (`{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}`) are invisible in the Pragmatist's audit

The Pragmatist audited template variables exhaustively for the cooperative mode and found two mismatches (`{AGENT_DOCS}` in Phase 2, `{TARGET_FILES}` in Phase 5). Both are real findings. But the audit scope statement says "cross-reference against every `{VARIABLE}` in every cooperative template." The word "cooperative" is doing heavy lifting: the Pragmatist explicitly scoped out the red-blue, prisoners-dilemma, and winner-take-all templates.

This is dangerous because the red-blue templates use `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` -- three variables that are never mentioned anywhere in the SKILL.md. An executor following SKILL.md's variable lists for red-blue mode would leave literal `{AGENT_ROLE}` strings in agent prompts. This is not a "fragile" outcome; it is a guaranteed rendering failure for any red-blue deliberation.

The Pragmatist's audit presents itself as a complete variable trace ("Complete variable audit" is the section header) but covers only one of four modes. A reader trusting this audit to clear the system for production use would deploy red-blue mode into a known-broken state.

**My audit identified three undocumented variables (Broken, High severity)**. The Pragmatist's audit does not mention them at all.

---

### DC-3: The Pragmatist classifies agent name validation as P1 but misdiagnoses the failure mode

The Pragmatist's Edge Case 2 and 3 correctly identify that agent names with special characters break file paths and that case-insensitive filesystem collisions can silently overwrite cross-reviews. The fix is rated P1 and the proposed validation regex (`[a-z0-9][a-z0-9-_]*`) is sound.

However, the Pragmatist frames this as an "edge case" and categorizes it under "Edge Cases That Silently Produce Wrong Output." This underestimates the blast radius. The cross-review output path is `{output}/{A}/cross-reviews/{B}.md`. If agent names collide after normalization, the damage is not limited to one file -- every cross-review involving the colliding agents is corrupted, every revision that reads those cross-reviews inherits corrupted input, and the synthesis aggregates the corruption. One bad name poisons the entire deliberation graph downstream.

More critically: the Pragmatist proposes validation but does not note that validation is impossible in a pure SKILL.md system without engine code. The "fix" is another instruction to the executor LLM: "reject configs with invalid agent names." Whether the LLM actually performs regex validation on agent names during config parsing is -- by the Pragmatist's own standard -- "hope, not enforcement." The Pragmatist applies a stricter standard to template variable mismatches than to config validation, even though both are equally instructional.

**My audit's systemic finding applies here**: every rule in Conversus is instructional. The Pragmatist treats some instructional rules as enforceable (config validation) while correctly identifying others as fragile (template resolution). The standard should be consistent.

---

## Tensions

### T-1: Template path resolution -- "fragile first step" vs. "the LLM IS the engine"

The Pragmatist rates template path resolution as P1 and proposes a detailed resolution algorithm (check config parent, check subdirectory, walk up). My audit does not cover template resolution separately because I frame the entire system as having zero enforcement surface -- the question is not "will the LLM find the templates" but "nothing validates that it found the RIGHT templates."

The tension: the Pragmatist treats this as a solvable problem (give the LLM better instructions and it will resolve paths correctly). I treat it as a symptom of the deeper architectural choice (no engine code means no deterministic path resolution). Both views have merit. The Pragmatist's fix is practical and would improve reliability. My framing is correct that even with better instructions, there is no validation that the resolved path is correct -- an LLM that resolves to a stale template directory would proceed silently.

The pragmatic resolution is to accept the Pragmatist's fix AND add post-resolution validation: "After resolving TEMPLATE_DIR, verify that `{TEMPLATE_DIR}/review.md` exists. If not, abort with an error message."

---

### T-2: Severity of context isolation failure -- "well-designed templates" vs. "agents CAN read anything"

The Pragmatist does not audit context isolation as a standalone finding. It appears implicitly in the parallel-launch discussion (Phase agent parallelism ensures agents cannot see each other's in-progress work). My audit rates context isolation as "Instructional Only, High severity" -- agents inherit full filesystem access and CAN read any file, including other agents' outputs from the current phase.

The tension: the Pragmatist's implicit position is that template design (listing explicit file paths in "What to Read") provides sufficient practical isolation. My position is that "sufficient practical isolation" is not isolation at all -- it is guidance that a sufficiently curious agent could override.

Neither of us is wrong in our domain. The Pragmatist is correct that an LLM following a well-structured template will, in practice, read only what the template lists. I am correct that this is not enforcement and that the system has no way to detect or prevent violations. The practical question is: how often does Claude Code's Agent tool produce subagents that go exploring beyond their instructions? If the answer is "rarely," the Pragmatist's position is pragmatically sound. If the answer is "sometimes, especially under ambiguous instructions," my position is the one that matters.

---

### T-3: What counts as "broken" -- template-SKILL.md contradiction vs. executor-recoverable gap

The Pragmatist uses a three-tier system: Works, Fragile, Broken. "Broken" does not appear in the Pragmatist's scorecard at all (the worst verdict is "Fragile" for five findings, plus one edge case marked as "Broken" for silent path corruption). My audit uses Broken for three claims (5, 8, 10) where the templates and SKILL.md contradict each other regardless of executor behavior.

The tension: the Pragmatist considers a gap "Fragile" if a competent executor can fill it (e.g., an LLM will probably fill `{AGENT_DOCS}` in Phase 2 even if the SKILL.md does not list it, because the variable name is self-explanatory and it appears in other phases). I consider the same gap "Broken" because the specification explicitly does not define it, so even a perfect executor following the spec exactly would fail.

This is a genuine methodological disagreement. The Pragmatist audits against "will a real LLM produce correct output?" I audit against "does the specification enforce its own invariants?" Both are valid questions. But they produce different fix priorities -- the Pragmatist deprioritizes gaps that LLMs will intuitively fill, while I treat every spec-template contradiction equally regardless of LLM recoverability.

---

## Safe Agreements

### SA-1: Phase 5 synthesis templates must include `{TARGET_FILES}` for multi-file targets

Both audits independently identify the same defect: all four synthesis templates use `{TARGET_PATH}` (single file) instead of `{TARGET_FILES}` (all files). Both audits agree this means the synthesizer in a multi-file deliberation only sees the primary target, missing context from additional files. Both propose the same fix: add `{TARGET_FILES}` to Phase 5 templates and to the SKILL.md Phase 5 variable list.

The Pragmatist rates this P1. My audit rates it Broken (Medium). The severity labels differ but the diagnosis, impact assessment, and remediation are identical.

---

### SA-2: `{AGENT_DOCS}` must be explicitly documented for Phase 2

Both audits find that the cooperative cross-review template uses `{AGENT_DOCS}` but the SKILL.md Phase 2 variable list does not include it. Both agree that a careful executor would probably fill it correctly (it is used in Phase 1, the variable name is clear), but that the omission creates unnecessary risk.

The Pragmatist proposes adding it to the Phase 2 variable list or adding a general inheritance statement. My audit flags it as part of a broader pattern of implicit variable inheritance that is never formally stated. The fix is the same: make it explicit.

---

### SA-3: The `disputes_remain` trigger is fragile but fail-safe, and that is acceptable

Both audits agree that parsing `### Remaining Disputes` and `**Dispute:` from LLM-generated markdown is inherently fragile -- the synthesizer could paraphrase the heading or format disputes differently. Both audits also agree that the fail-open default ("if parsing fails, run Phase 6") is sound engineering that converts a fragile parser into a safe one.

The Pragmatist suggests a machine-readable comment (`<!-- disputes_count: N -->`) as a hardening measure but calls it over-engineering. My audit suggests structured output (JSON/YAML frontmatter) as the enforcement-grade solution. Both agree the current design is acceptable as-is because the failure mode is "run arbitration unnecessarily" rather than "skip arbitration silently."
