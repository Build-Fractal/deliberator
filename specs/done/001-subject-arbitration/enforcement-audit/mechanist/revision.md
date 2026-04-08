# Revised Enforcement Audit: Conversus SKILL.md

**Auditor**: The Mechanist
**Date**: 2026-03-19
**Revision basis**: Original review + cross-reviews from The Pragmatist and The Purist + my cross-reviews of both

---

## Disposition of Original Findings

### Claim 1: "One agent per output file" — HELD (Medium, Instructional Only)

No cross-reviewer challenged this finding. Templates point each agent at a single `{OUTPUT_PATH}`, which structurally reinforces the rule but does not enforce it. Held as stated.

---

### Claim 2: "All agents launch in single message" — HELD (Low, Instructional Only)

No cross-reviewer challenged this finding. The concern (sequential launch allowing later agents to read earlier agents' in-progress outputs) is valid but mitigated by the Agent tool's parallel dispatch. Held as stated.

---

### Claim 3: Context isolation between agents — MODIFIED (Instructional Only, Medium severity; was High)

**Pragmatist DC-2** argues that rating instructional isolation as High severity contradicts my own conclusion that instructional-only claims are "acceptable for a prompt-driven orchestration system." The Pragmatist is correct: I cannot simultaneously validate the prompt-instruction model and rate its primary isolation mechanism as High severity. The Purist DC-2 makes a related point — that I inconsistently apply a generous "templates partially reinforce" discount to Claim 1 (output discipline, Medium) while applying a strict standard to Claim 3 (read discipline, High), even though both are governed by the same mechanism.

I concede the inconsistency. Both read and write discipline operate on the same enforcement surface (instructional prompting to an unrestricted agent). Templates are well-designed here: they list explicit file paths in "What to Read" sections and do not reference other agents' same-phase outputs. This is the strongest practical isolation available in a prompt-only system.

**Revised verdict**: Instructional Only, **Medium** severity. The templates provide meaningful practical isolation. The risk is real but consistent with the system's architectural constraints, not an outlier requiring special treatment.

---

### Claim 4: Phase boundaries are hard barriers — HELD (Low, Instructional Only)

No substantive challenge. The implicit file-dependency reinforcement (Phase 3 templates reference Phase 2 output files) remains the strongest structural guard. Held as stated.

---

### Claim 5: `{PRIOR_FILES}` injection — MODIFIED (Fragile, Medium severity; was Broken)

Both cross-reviewers challenged the "Broken" verdict:

- **Pragmatist DC-1**: The absence of `{PRIOR_FILES}` from templates is by design — the SKILL.md describes a conditional append, not placeholder substitution. Adding a `{PRIOR_FILES_SECTION}` placeholder would produce empty section headers when no prior files exist.
- **Purist DC-1**: The real defect is not the absence of a placeholder but the heading mismatch — the injection instruction says "append after 'What to Read'" but 2 of 4 modes use "Files to Read" instead.

I concede that "Broken" was the wrong label. The SKILL.md deliberately uses a runtime append mechanism, and my review acknowledged this ("This is a design that deliberately avoids embedding `{PRIOR_FILES}` in templates"). Calling a deliberately chosen design "Broken" conflates design disagreement with specification defect.

However, I do not concede entirely to the Pragmatist's position that this is merely a placement problem. The Purist identifies the deeper issue: the injection instruction references a heading ("What to Read") that does not exist in half the templates. This is not placement ambiguity — it is a targeting defect in the append mechanism.

**Revised verdict**: **Fragile**, Medium severity. The design is intentional but the injection target is underspecified. The fix should address the heading inconsistency (standardize section headings across modes, or specify the injection target per mode) rather than replacing the append mechanism with a placeholder.

**Revised fix**: Adopt the Purist's recommendation — standardize the "What to Read" heading across all four modes, or specify the injection target per mode in SKILL.md. Additionally, adopt the Pragmatist's suggestion to move the injection instruction out of the Phase 1 section into a standalone "Cross-Phase Injections" section to eliminate positional ambiguity.

---

### Claim 6: Iteration file naming / `{ITERATION}` variable — MODIFIED (Low for `{ITERATION}` variable; Medium held for iteration logic)

**Purist T-2** challenges my bundling: `{ITERATION}` the variable is dead weight (Low), while the iteration file-naming logic being prose-only is a separate, higher concern. The Purist correctly notes that `{ITERATION}` may be orchestrator state (the executor needs it to compute file paths) rather than a template variable (agents need it in their prompts).

I accept the unbundling. The `{ITERATION}` variable should either be removed from SKILL.md or explicitly documented as orchestrator-only state, not a template variable. This is a Low-severity cleanup. The iteration file-naming logic (the `revision.md` vs `revision_{N}.md` asymmetry, the stateful path computation) remains Medium severity as originally stated.

**Revised verdict**: `{ITERATION}` variable: Low (dead weight — remove from spec or document as orchestrator-only). Iteration file-naming logic: Medium (held).

---

### Claim 7: `disputes_remain` parsing — HELD (Low, Instructional Only)

The Purist (T-3) argues that a spec which works only because of a fallback is underspecified, and that the correct fix is to specify the heading per mode rather than relying on fail-open. This is technically correct but does not change the severity. The fail-open default converts a fragile parser into a safe one. The failure mode is "unnecessary arbitration" not "missed arbitration."

I hold the Low severity rating. The Purist's fix (specify heading per mode) is sound and belongs in the fix list as a low-priority hardening item.

---

### Claim 8: Multi-file `{TARGET_FILES}` in Phase 5 — MODIFIED (Design Question, Medium severity; was Broken)

**Purist DC-3** argues this cannot be simultaneously "Broken" and "consistent between SKILL.md and templates." The Purist is correct: the SKILL.md Phase 5 variable list documents `{TARGET_PATH}` only, the templates use `{TARGET_PATH}` only, and the system behaves as designed. My objection was that this design contradicts a stated invariant ("agents MUST read all target files") — but as the Purist notes, that invariant is stated in the Phase 1 context, not as a global rule.

I concede the "Broken" label. The spec and templates agree. This is a design question: should the synthesizer have direct access to all target files, or is indirect access through reviewed artifacts sufficient?

The Pragmatist's argument tips the balance on the design question: in adversarial modes (red-blue, winner-take-all), agents may selectively cite sources, so the synthesizer needs direct access to verify claims against originals. I agree with this reasoning.

**Revised verdict**: **Design gap**, Medium severity. The spec and templates are internally consistent, but the design should be revised to include `{TARGET_FILES}` in Phase 5 for multi-file targets — especially given adversarial modes where indirect access is unreliable.

---

### Claim 9: Config validation error messages — HELD (Low, Instructional Only)

The Purist (DC-2 in my cross-review of the Purist) wants to add message templates for all 11 rules. I maintain this creates false determinism — specifying natural-language error messages for a system with no deterministic error renderer is specification theater. The 3/11 inconsistency is real but Low severity.

Held as stated. If error messages are formalized, they should be paired with structured validation (JSON schema for `conversus.yml`), not added as more LLM instructions.

---

### Claim 10: Template variable consistency — MODIFIED (disaggregated; was single High)

**Pragmatist DC-3** correctly argues that grouping five variable mismatches into a single "Broken, High severity" verdict creates a false sense of crisis. The individual items have different impacts and different fixes. I concede the bundling was a mistake.

Disaggregated verdicts:

| Variable | Revised Verdict | Severity | Rationale |
|---|---|---|---|
| `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` | **Broken** | **High** | Red-blue mode is non-functional without these. All three reviewers agree this is the highest-priority fix. Literal `{AGENT_ROLE}` strings will appear in agent prompts. |
| `{PRIOR_FILES}` | **Fragile** | **Medium** | Reclassified per Claim 5 revision above. Design is intentional; injection target is underspecified. |
| `{ITERATION}` | **Dead weight** | **Low** | Orchestrator state, not a template variable. Remove from spec or document as orchestrator-only. |
| `{AGENT_DOCS}` (Phase 2, Phase 4) | **Broken** | **Medium** | Not listed in SKILL.md variable sections for these phases. An executor strictly following the variable lists would not fill it. The Pragmatist and Purist both identify this independently. |
| `{TARGET_FILES}` (Phase 5) | **Design gap** | **Medium** | Reclassified per Claim 8 revision above. Spec and templates agree, but design should be revised for multi-file targets. |

---

## Systemic Finding — MODIFIED

My original systemic finding stated: "Conversus has zero enforcement surface. Every rule exists as an instruction to an LLM executor."

Both cross-reviewers push back on the framing. The Pragmatist argues that in a system where "the LLM IS the engine," well-structured instructions to a reliable executor ARE the enforcement mechanism — the only one available. The Purist agrees that templates are the enforcement surface and that spec-template alignment is the meaningful metric.

I partially concede. The phrase "zero enforcement surface" sets a standard (programmatic validation) that is foreign to the system's architecture. A more accurate framing:

**Revised systemic finding**: Conversus enforces its rules through template structure and prompt instruction to an LLM executor. This enforcement model has no fallback — if the executor misinterprets an instruction, no validator catches the error. The templates are the primary enforcement surface: they constrain what agents see and where they write. Where templates and SKILL.md are aligned, the system works reliably. Where they contradict each other, even a perfect executor cannot produce correct output. The priority is therefore to eliminate spec-template contradictions (the "Broken" items), then to reduce ambiguity in the remaining instructions (the "Fragile" items).

---

## Prioritized Fix List

### P0 — Blocking (must fix before any red-blue deliberation)

**Fix 1: Add `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` definitions to SKILL.md**

- Add explicit variable definitions to the Phase 1, Phase 2, Phase 3, and Phase 4 variable sections
- Specify mapping: `config.agents[].role` maps to `{AGENT_ROLE}` for the authoring agent, `{REVIEWER_ROLE}` for the cross-reviewing agent, `{REVIEWED_ROLE}` for the agent being cross-reviewed
- Source: Mechanist Claim 10C, Purist Gap 1.1, Pragmatist (absent — scoped only to cooperative mode)
- Consensus: All three reviewers who examined red-blue templates agree this is the highest-priority fix

### P1 — High (spec-template contract failures)

**Fix 2: Add `{AGENT_DOCS}` to SKILL.md Phase 2 and Phase 4 variable lists**

- The variable is used in cooperative cross-review and disputes templates but not documented in SKILL.md for those phases
- An executor strictly following the variable lists would not fill it
- Source: Mechanist Claim 10E, Pragmatist Finding 3b, Purist appendix
- Consensus: All three reviewers agree

**Fix 3: Add `{TARGET_FILES}` to Phase 5 synthesis templates and SKILL.md Phase 5 variable list**

- All four synthesis templates use `{TARGET_PATH}` only — the synthesizer in a multi-file target run cannot verify claims against all original sources
- Especially critical for adversarial modes where agents may selectively cite
- Source: Mechanist Claim 8, Pragmatist Finding 3a, Purist appendix
- Consensus: All three reviewers agree on the fix; severity labels differ but remediation is identical

### P2 — Medium (ambiguity that increases misinterpretation risk)

**Fix 4: Standardize `{PRIOR_FILES}` injection targeting**

- Standardize the "What to Read" section heading across all four modes (currently "Files to Read" in winner-take-all and prisoners-dilemma), OR specify the injection target per mode in SKILL.md
- Move the injection instruction from Phase 1 section to a standalone "Cross-Phase Injections" section
- Source: Mechanist Claim 5, Purist Gaps 1.3/4.1, Pragmatist Finding 4

**Fix 5: Document the iteration file-naming resolution rule**

- Add explicit note: iteration 1 produces `revision.md` (no suffix); iteration 2+ produces `revision_{N}.md`; cross-reviews in iteration 2 therefore read `revision.md`, not `revision_1.md`
- Source: Mechanist Claim 6, Pragmatist Finding 2b, Purist (implicit)
- Consensus: All three reviewers agree

**Fix 6: Resolve `{ITERATION}` — remove or re-scope**

- Either remove `{ITERATION}` from SKILL.md's Phase 3 variable list (it is not consumed by any template) or explicitly document it as orchestrator-only state used for file-path computation, not a template variable
- Source: Mechanist Claim 6/10B, Purist Gap 1.2

### P3 — Low (hardening, non-blocking)

**Fix 7: Specify `disputes_remain` heading per mode**

- Document the expected heading for each synthesis mode so the trigger parsing does not rely on the fail-open default to compensate for heading mismatches
- Source: Mechanist Claim 7, Purist T-3

**Fix 8: Standardize config validation error messages (if structured validation is added)**

- If a JSON schema or validation engine is ever introduced for `conversus.yml`, formalize error messages at that time
- Without structured validation, adding natural-language error message templates to SKILL.md creates false determinism
- Source: Mechanist Claim 9, Purist Gap 2.1

---

## Concession Summary

| Item | Original Position | Challenge From | Disposition |
|---|---|---|---|
| `{PRIOR_FILES}` = Broken | Broken, Medium | Pragmatist DC-1, Purist DC-1 | **Conceded** to Fragile. Design is intentional; injection target heading is the real defect. |
| Context isolation = High severity | High | Pragmatist DC-2 | **Conceded** to Medium. Cannot rate the enforcement model as acceptable AND its primary mechanism as High severity. |
| `{TARGET_FILES}` Phase 5 = Broken | Broken, Medium | Purist DC-3 | **Conceded** to Design gap. Spec and templates agree; this is a design question, not a contract failure. |
| Claim 10 = single High verdict | 5 vars bundled at High | Pragmatist DC-3 | **Conceded**. Disaggregated into individual verdicts ranging from High to Low. |
| `{ITERATION}` = Medium | Part of Claim 6 bundle | Purist T-2 | **Modified**. Variable itself is Low (dead weight); iteration logic remains Medium. |
| "Zero enforcement surface" | Systemic finding | Pragmatist T-2, Purist T-1 | **Modified**. Templates are the enforcement surface. Reframed from "no enforcement" to "enforcement through template structure with no fallback." |

| Item | Original Position | Challenge From | Disposition |
|---|---|---|---|
| One agent per output file | Instructional Only, Medium | (unchallenged) | **Held** |
| All agents launch in single message | Instructional Only, Low | (unchallenged) | **Held** |
| Phase boundaries | Instructional Only, Low | (unchallenged) | **Held** |
| Red-blue role variables = Broken | High (within Claim 10) | (universally agreed) | **Held** |
| `{AGENT_DOCS}` undocumented | Broken (within Claim 10) | (universally agreed) | **Held** |
| Iteration file-naming asymmetry | Medium | (universally agreed) | **Held** |
| `disputes_remain` fail-open | Low | Purist T-3 | **Held** on severity; accepted fix recommendation |
| Config validation messages | Low | Purist DC-2 (in my cross-review) | **Held** |
