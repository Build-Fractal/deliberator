# Cross-Review of The Mechanist's Enforcement Audit

**Reviewer**: The Purist
**Reviewed**: The Mechanist
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: The Mechanist Mischaracterizes `{PRIOR_FILES}` as "Broken" When the Real Defect Is the Injection Mechanism

The Mechanist's Claim 5 concludes that `{PRIOR_FILES}` is **"Broken"** because the variable "does not appear in ANY template file across ALL four modes." The Mechanist then proposes adding a `{PRIOR_FILES_SECTION}` placeholder to every template to normalize it into standard variable substitution.

This is the wrong diagnosis. The SKILL.md deliberately avoids embedding `{PRIOR_FILES}` as a static placeholder. The spec describes a conditional append operation (L191-195): if prior files exist, the executor appends a block after the "What to Read" section. This is not standard substitution; it is runtime prompt construction. The Mechanist's own review acknowledges this: "This is a design that deliberately avoids embedding `{PRIOR_FILES}` in templates."

The actual defect -- which my review identifies as Gap 1.3 and Gap 4.1 -- is that the injection point heading ("What to Read") does not match the section heading in 2 of 4 modes. Winner-take-all and prisoners-dilemma templates use "Files to Read," not "What to Read." The Mechanist notes this heading inconsistency only in passing (Claim 7, where synthesis heading variation is discussed) but never connects it to the prior-files injection failure.

**Why this is dangerous**: If the fix follows the Mechanist's recommendation (add `{PRIOR_FILES_SECTION}` to all templates), the dual-mechanism design flaw is papered over but the heading inconsistency remains latent. A future template author who follows the SKILL.md's instruction to "append after 'What to Read'" will fail on 2 of 4 modes. The Mechanist's fix addresses the symptom (no placeholder in templates) and ignores the root cause (the injection instruction references a heading that half the templates do not have).

### DC-2: The Mechanist Downgrades Context Isolation to "Medium" Implied Enforcement While Calling It "High" Severity

The Mechanist's Claim 3 rates context isolation as **"Instructional Only"** with **"High"** severity, correctly noting that subagents inherit full filesystem access and can read any file. But then in Claim 1, the Mechanist argues that templates "partially reinforce" the one-agent-per-file rule by pointing each agent at a single output path, and rates this as only **"Medium"** severity.

These two claims are in tension that the Mechanist does not resolve. If context isolation is High severity because agents CAN read anything (Claim 3), then the one-agent-per-file constraint is also High severity because the same unrestricted agent could write additional files or read other agents' outputs while constructing its own. The template pointing to a single `{OUTPUT_PATH}` does not prevent the agent from writing to other paths -- it only tells the agent where its output should go. The Mechanist applies a generous "templates partially reinforce" discount to Claim 1 that is inconsistent with the strict "agents CAN read anything" standard applied in Claim 3.

**Why this is dangerous**: This inconsistency creates a false sense of graduated risk. A reader of the Mechanist's audit could conclude that output-file discipline is a medium concern while read-access discipline is a high concern. In reality, both are governed by the same mechanism (instructional prompting to an unrestricted agent), and both have the same enforcement surface (zero). Treating them as different severities invites prioritizing one fix over the other when both require the same mitigation.

### DC-3: The Mechanist Claims `{TARGET_FILES}` in Phase 5 Is "Broken" but Accepts the SKILL.md's Own Omission as Consistent

The Mechanist's Claim 8 states that all four synthesis templates use `{TARGET_PATH}` exclusively and never `{TARGET_FILES}`, and calls this **"Broken (partially)."** But then the Mechanist writes: "The SKILL.md's Phase 5 variable list (L255) documents `{TARGET_PATH}` but NOT `{TARGET_FILES}` for Phase 5, so this omission is consistent between SKILL.md and templates."

A defect cannot be simultaneously "Broken" and "consistent between SKILL.md and templates." If the spec and the templates agree that Phase 5 uses `{TARGET_PATH}`, the system behaves as designed. The Mechanist's objection is that this design "contradicts the stated invariant that agents must read all target files" -- but that invariant (SKILL.md L183/L189) is stated in the Phase 1 context, not as a global rule for all phases. Phase 5 is a synthesis phase that reads all reviews, cross-reviews, revisions, and disputes; it is structurally different from Phases 1-4 where agents directly analyze target files.

**Why this is dangerous**: Labeling a consistent spec-template pair as "Broken" conflates design disagreement with specification defect. If a fixer acts on this, they would add `{TARGET_FILES}` to synthesis templates, changing the design of Phase 5 without acknowledging that both the spec and templates currently agree on the current behavior. The correct classification is what my review identifies: this is a design question (does the synthesizer need direct access to all target files, or is indirect access through artifacts sufficient?), not a broken contract.

---

## Tensions

### T-1: Divergent Framing of "Enforcement" in a Prompt-Driven System

The Mechanist's central thesis is that Conversus has "zero enforcement surface" and that "every rule is a wish directed at an LLM executor." My review takes a different position: the spec itself is the enforcement mechanism, and the question is whether it is complete and unambiguous enough to serve that role. The Mechanist evaluates whether the system prevents violations; I evaluate whether the system specifies behavior precisely enough that an implementer can produce a correct executor.

This is not a contradiction -- both frames are valid. But the tension matters because it leads to different remediation priorities. The Mechanist would add post-hoc validators, state machines, and sandboxed filesystems. I would add missing variable definitions, error message templates, and scope clarifications. Both are needed, but if only one set of fixes is applied, the Mechanist's infrastructure additions without spec completeness yield a validator checking against an incomplete spec, while my spec completeness without enforcement yields a complete spec that still relies on executor fidelity.

### T-2: Severity Assessment of the `{ITERATION}` Dead Variable

The Mechanist rates the `{ITERATION}` gap as **"Medium"** severity under Claim 6, describing it as "a lot of stateful logic that the SKILL.md describes in prose" and linking it to the broader iteration file-naming complexity. My review (Gap 1.2) rates it as **"Low"** severity, calling it a "dead variable, no functional impact" since no template consumes it.

The disagreement is about what the `{ITERATION}` variable represents. To the Mechanist, it is a symptom of the larger problem that iteration logic is entirely prose-based, and the Medium rating reflects the aggregate risk of the iteration system, not the variable alone. To me, it is a single unused variable definition that should either be removed or given a consumer, and the Low rating reflects its isolated impact. The Mechanist bundles; I isolate. Neither is wrong, but the bundled rating makes it harder to triage: fixing the dead variable definition is trivial, while rewriting iteration logic as a formula is a design change.

### T-3: Whether the Fail-Open Default for `disputes_remain` Is Adequate Mitigation

The Mechanist's Claim 7 rates the `disputes_remain` parsing as **"Low"** severity, largely because the fail-open default ("if parsing fails, run Phase 6 anyway") prevents silent skipping of arbitration. The Mechanist also flags that non-cooperative synthesis templates may use different heading structures, but accepts the fail-open as sufficient mitigation.

My review does not directly address `disputes_remain` parsing, but the Purist position is that a spec which works correctly only because of a fallback is still underspecified. If the parsing instruction references `### Remaining Disputes` and the prisoners-dilemma synthesis uses a different heading, the parsing silently fails and the fallback fires -- meaning Phase 6 runs even when there are no disputes. This is a false positive (unnecessary arbitration), not a false negative (missed arbitration). The Mechanist accepts this as the safe direction. The Purist position is that specifying the correct heading per mode eliminates the need for a fallback to compensate for a spec defect. A fallback should handle unexpected conditions, not compensate for a known heading mismatch.

---

## Safe Agreements

### SA-1: The Red-Blue Role Variables Are a Blocking Defect

The Mechanist's Claim 10 identifies `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` as "Broken -- used but never documented." My review (Gap 1.1) identifies the same variables as "High -- red-blue mode is broken without these" and calls Gap 1.1 "a blocking defect."

We agree completely on the facts (3 variables used in 4 red-blue templates, zero definitions in SKILL.md), the severity (high/blocking), and the required fix (add explicit variable definitions mapping `config.agents[].role` to template variables). This is the highest-priority item in both audits.

### SA-2: Template Variable Inconsistencies Are the Most Concerning Class of Defect

Both audits identify template-SKILL.md variable mismatches as the most structurally significant finding. The Mechanist's summary table (Claim 10) lists 5 variables with mismatched status. My Appendix cross-references all variables across all 24 templates and identifies the same mismatches plus additional ones (`{MODE}` usage inconsistency, prisoners-dilemma missing `{AGENT_DOCS}` in Phases 3-4).

We agree that "even if the LLM follows every instruction perfectly, the variables do not exist where the SKILL.md says they do" (Mechanist's systemic finding) and that these are not executor-reliability problems but specification-template contract failures. We agree these must be fixed before the instructional-only items.

### SA-3: The System's Nearest Approximation of Enforcement Is Template Structure

The Mechanist writes: "The templates are the closest thing to enforcement -- they structure what agents see and where they write." My review's methodology is built on the same premise: tracing every behavior to an explicit instruction, where templates serve as the concrete binding between spec intent and agent behavior.

We agree that in a prompt-driven orchestration system with no engine code, the templates are the enforcement surface. The spec defines the rules; the templates encode them into agent prompts; the executor fills and dispatches. If the templates are correct and complete, executor compliance is likely. If the templates contradict the spec, no amount of executor diligence can produce correct output. This shared understanding grounds both audits' prioritization of template-spec alignment over adding external validation infrastructure.
