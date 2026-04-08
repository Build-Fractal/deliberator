# Final Disputes: The Purist

**Author**: The Purist
**Date**: 2026-03-19
**Phase**: Disputes (final position)

---

## Remaining Disputes

### Dispute 1: `{PRIOR_FILES}` injection mechanism — placeholder vs. section-append

**Contested with**: The Mechanist (who proposed `{PRIOR_FILES_SECTION}` placeholder) and, after my own revision, with my prior self.

In my revision I conceded the Mechanist's position: replace the dual mechanism (section-appending + placeholder substitution) with a single `{PRIOR_FILES_SECTION}` placeholder that expands to a formatted block or empty string. I now partially retract that concession.

The Mechanist's placeholder design is cleaner in the abstract. But it introduces a problem neither the Mechanist nor the Pragmatist addresses: **what constitutes "empty string" expansion in a template consumed by an LLM?** A placeholder that silently vanishes leaves no trace in the rendered prompt -- the agent has no way to know whether prior context was absent or whether the orchestrator failed to inject it. In a system with no fallback validator, silent omission is indistinguishable from silent failure.

The Pragmatist's position (keep the append mechanism, clarify scope and placement) preserves an important property: the append is an additive operation that either visibly succeeds or visibly does not occur, and the base template remains a complete, valid prompt without it.

**My final position**: The append mechanism should be retained, but (a) scoped explicitly to Phase 1 only, (b) moved to a standalone "Cross-Phase Injections" section in SKILL.md, and (c) the heading inconsistency ("What to Read" vs. "Files to Read") should be resolved by standardizing all modes to "What to Read." If the placeholder approach is adopted instead, the spec must mandate that an empty `{PRIOR_FILES_SECTION}` expands to a comment line (e.g., `<!-- No prior files for this deliberation -->`) rather than to the empty string, so the absence is explicit and auditable.

**Why this matters**: This is not a cosmetic disagreement. In a system without programmatic validation, the difference between "nothing was injected because nothing existed" and "nothing was injected because of a bug" must be observable in the rendered prompt. Silent expansion to empty string violates that requirement.

---

### Dispute 2: `{ITERATION}` — convergence signaling is functional, not optional

**Contested with**: The Mechanist, who classifies `{ITERATION}` as Low-severity "dead weight" to be removed or re-scoped as orchestrator-only state.

The Mechanist's revision unbundles `{ITERATION}` from iteration logic and rates the variable itself as Low. The Pragmatist upgrades it to P2/Fragile and agrees it should be added to revision templates. The disagreement is between the Mechanist (who sees it as dead weight) and the Purist-Pragmatist alignment (who see it as functional).

The Mechanist's concern -- that injecting iteration awareness "could change agent behavior" -- is precisely the point. Agents in iteration 3 who do not know they are in iteration 3 will treat their task as a first-pass revision rather than a convergence-seeking refinement. The behavioral change is not a side effect; it is the purpose. Convergence quality in multi-iteration runs depends on agents understanding where they are in the sequence.

**My final position**: `{ITERATION}` is a Medium-severity functional variable, not Low-severity dead weight. It must be (a) retained in SKILL.md, (b) added to Phase 3 revision templates with a metadata line (e.g., "This is revision iteration {ITERATION}"), and (c) documented as serving both orchestrator file-path computation and agent convergence signaling. The Mechanist's alternative -- removing it from the spec or labeling it orchestrator-only -- degrades multi-iteration convergence quality for the sake of template minimalism.

---

### Dispute 3: `{TARGET_FILES}` Phase 5 severity — design gap vs. design enhancement

**Contested with**: The Mechanist (who labels this "Design gap, Medium") and to a lesser extent myself (who labels it "Medium" as consistent-but-insufficient).

All three reviewers agree on the fix: add `{TARGET_FILES}` to Phase 5 synthesis templates and SKILL.md. The dispute is over characterization. The Mechanist initially called it "Broken," then conceded to "Design gap." I called it "Medium" as a design enhancement. The Pragmatist calls it P1/Fragile.

The Pragmatist's severity is correct and mine was too conservative. In adversarial modes (red-blue, winner-take-all), agents may selectively cite or misrepresent source material. A synthesis agent that cannot verify claims against original target files is not merely "insufficient" -- it is structurally unable to perform its stated function in adversarial contexts. The synthesis template for red-blue mode instructs the agent to "weigh the strength of arguments" and "identify which positions are best supported by evidence" -- but the agent cannot access the evidence directly.

**My final position**: This should be rated P1, not P2. The Pragmatist had it right. For cooperative mode the current design is tolerable (agents are collaborative, selective citation is unlikely). For adversarial modes it is a correctness defect: the synthesis agent is asked to evaluate evidence it cannot see. The fix is identical regardless of severity classification, but the priority determines whether it ships in the initial fix batch or gets deferred.

---

## Convergence

### Convergence 1: Red-blue role variables are the highest-priority blocking defect (P0)

All three reviewers independently identify `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` as undefined in SKILL.md despite being used in all four red-blue templates. All three rate this as the single highest-priority fix. The Mechanist, Pragmatist, and Purist agree on diagnosis, severity, and remediation without qualification. This is the strongest consensus item in the entire audit.

**Fix**: Add variable definitions to SKILL.md Phases 1-4 mapping `config.agents[].role` to the three role template variables.

---

### Convergence 2: `{AGENT_DOCS}` must be added to Phase 2 variable list and prisoners-dilemma templates

All three reviewers identify the `{AGENT_DOCS}` omission, though they arrive at it from different directions. The Mechanist finds it through template variable analysis (Claim 10E). The Pragmatist finds it through cooperative mode audit (Finding 3b). I find the prisoners-dilemma instance through template-by-template comparison (appendix, later promoted). The Pragmatist concedes the prisoners-dilemma scope expansion in revision (NEW-2).

**Fix**: (1) Add `{AGENT_DOCS}` to SKILL.md Phase 2 variable list. (2) Add `{AGENT_DOCS}` to prisoners-dilemma `revision.md` and `disputes.md` templates. (3) Consider adding a general variable inheritance statement for Phase 1 variables in subsequent phases.

---

### Convergence 3: Template path resolution must use a single anchor

All three reviewers agree that template path resolution is underspecified. The Pragmatist originally proposed a three-step resolution algorithm; I identified the multi-anchor ambiguity in that proposal; the Pragmatist conceded and simplified to a single-anchor approach in revision. The Mechanist supports post-resolution validation. All three agree on the final design.

**Fix**: Resolve template directory relative to the `conversus.yml` config file's parent directory. Verify the resolved path contains expected template files before proceeding. Specify error behavior for missing template directory and missing individual template files.

---

### Convergence 4: Iteration file-naming boundary needs explicit documentation

All three reviewers independently identify that `revision_{N-1}.md` when N-1=1 must resolve to `revision.md`, not `revision_1.md`. No reviewer disputes the finding, the severity, or the fix. This is a one-sentence clarification.

**Fix**: Add explicit note to SKILL.md: "When N-1 equals 1, the file path is `revision.md` (no numeric suffix), not `revision_1.md`."

---

### Convergence 5: The enforcement model is template-centric, and spec-template alignment is the primary quality metric

All three reviewers converge on a shared understanding of the system's enforcement architecture, despite arriving from different starting assumptions. The Mechanist initially declared "zero enforcement surface" and revised to "enforcement through template structure with no fallback." The Pragmatist maintained from the start that templates are the enforcement mechanism. I maintained that spec-template alignment is the meaningful metric.

The revised systemic finding is shared: Conversus enforces rules through template structure and prompt instruction. Templates are the primary enforcement surface. Where spec and templates align, the system is reliable. Where they contradict, even a perfect executor produces wrong output. The audit priority is therefore: eliminate contradictions (Broken items), then reduce ambiguity (Fragile items), then improve documentation (Low items).

---

## Final Position

The three-reviewer enforcement audit has been productive. The deliberation process surfaced one blocking defect (red-blue role variables) that two of three original audits missed entirely, and produced a prioritized fix list with genuine consensus on the top items.

**What is settled**: P0 (role variables) and the structural P1 items (`{AGENT_DOCS}` additions, `{TARGET_FILES}` in Phase 5, template path resolution, agent name validation) have unanimous or near-unanimous agreement on both diagnosis and remedy. These should be implemented without further deliberation.

**What remains disputed**: Three items lack full convergence:

1. The `{PRIOR_FILES}` injection mechanism (placeholder vs. append) is a genuine architectural choice with trade-offs on both sides. My position favors the append mechanism with explicit scoping; the Mechanist favors the placeholder mechanism. Either is workable if the chosen approach addresses observability of absent prior files.

2. The `{ITERATION}` variable's role and severity is disputed between the Mechanist (Low/dead weight) and the Purist-Pragmatist alignment (Medium/functional). The functional argument for convergence signaling is stronger, but the Mechanist's caution about changing agent behavior is not without merit for single-iteration runs where the signal is noise.

3. The severity of `{TARGET_FILES}` in Phase 5 is disputed between my original Medium and the Pragmatist's P1. On reflection I align with the Pragmatist: adversarial modes make this a correctness issue, not merely a design enhancement.

**Recommendation to the arbiter**: The disputed items are all P1-P2 range disagreements about severity and mechanism, not disagreements about whether fixes are needed. All three reviewers agree every disputed item needs a fix. The arbiter should rule on mechanism choice for `{PRIOR_FILES}` and severity classification for `{ITERATION}` and `{TARGET_FILES}` Phase 5, then close the audit.
