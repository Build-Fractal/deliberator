# Cross-Review of The Purist's Enforcement Audit

**Reviewer**: The Mechanist
**Reviewed**: The Purist
**Date**: 2026-03-19
**Subject**: Enforcement audit of SKILL.md specification completeness

---

## Dangerous Contradictions

### DC-1: The Purist treats "Missing from SKILL.md" and "Broken" as the same category -- they are not

The Purist's entire framework classifies gaps as Specified, Implied, or Missing. Gap 1.1 (`{AGENT_ROLE}` et al. undocumented in SKILL.md but used in templates) and Gap 1.2 (`{ITERATION}` documented in SKILL.md but unused in templates) both receive the same "Missing" label. But these are opposite defects. Gap 1.1 is a template that demands something the spec never promises to supply -- a broken contract where the templates are ahead of the spec. Gap 1.2 is a spec that promises something no template consumes -- dead weight where the spec is ahead of the templates.

The Purist's recommended fix for both is "add text to SKILL.md." That is correct for 1.1 (the spec must document what the templates need) but potentially wrong for 1.2. If `{ITERATION}` is dead, the correct fix may be to remove it from the spec, not to add it to templates. Adding it to templates just to satisfy completeness creates unnecessary coupling. The Purist's methodology -- which assumes the spec is the source of truth and gaps should be closed by expanding the spec -- has no mechanism for recommending that the spec shrink. A specification that only grows is a specification that accumulates dead surface area.

This matters because an implementer following The Purist's recommendations would add `{ITERATION}` to all four revision templates. That means every revision agent would see an iteration counter in its prompt. But the current template design deliberately omits it -- agents do not need to know what iteration they are in to do their job. The orchestrator handles iteration numbering externally. Injecting iteration awareness into agents could change their behavior: an agent that knows it is on iteration 3 of 3 might behave differently than one that does not know its position in the sequence. The Purist's "completeness" fix could introduce a behavioral side effect that the current design avoids.

### DC-2: Error message specification as written would create false determinism

The Purist's Gap 2.1 demands that all 11 validation rules get specified error message templates, and provides exact examples. This sounds rigorous, but it creates a dangerous illusion: that these messages are testable outputs of a validation engine. They are not. Conversus has no validation engine. The LLM executor reads the SKILL.md, interprets the validation rules, and produces whatever error message it generates. Specifying exact error templates in the SKILL.md does not make the messages deterministic -- it makes them aspirational.

The Mechanist's review identified this: "the executor LLM will generate its own error messages for 8 of 11 failure modes. These messages will be reasonable but not deterministic or testable." The Purist's fix -- adding message templates -- does not change this reality. It adds text to the spec that cannot be enforced.

The danger: a downstream consumer (a test suite, a CI check, a monitoring system) reads The Purist's recommendation and writes assertions against exact error message strings. Those assertions will be flaky because the executor LLM may paraphrase, reorder, or embellish the message. The Purist's recommendation creates a false contract: it looks like a machine-readable interface but it is still a suggestion to an LLM.

The honest fix is what The Mechanist recommended: a JSON schema for `conversus.yml` that can be validated before the LLM starts, or structured error output. Specifying natural-language error messages for a system with no natural-language error renderer is specification theater.

### DC-3: The Purist's `{PRIOR_FILES}` injection fix misdiagnoses the root cause

The Purist identifies the `{PRIOR_FILES}` injection issue (Gaps 1.3, 4.1, 4.2) and recommends either standardizing section headings across all review templates or specifying the injection target per mode. Both fixes assume the section-appending mechanism is sound and just needs better targeting instructions.

The Mechanist's review classified this as "Broken" (Claim 5), not "Missing." The problem is not that the injection point is ambiguous -- the problem is that the injection mechanism itself is architecturally unsound. The SKILL.md asks the executor to perform runtime string surgery on filled templates: "append this section after the 'What to Read' section." This is a second variable-resolution mechanism layered on top of the first (placeholder substitution). The Purist's fix preserves this dual mechanism and tries to make it more precise. The Mechanist's fix eliminates it: add a `{PRIOR_FILES_SECTION}` placeholder to every Phase 1 template and fill it with either content or empty string. One mechanism, not two.

The Purist's fix is dangerous because it enshrines string surgery as a spec-sanctioned pattern. If future features need conditional template sections, they would follow the same precedent: "append X after heading Y." Each new conditional section makes the executor's job harder and more error-prone. The Mechanist's fix -- normalizing everything to placeholder substitution -- keeps the execution model simple and uniform.

---

## Tensions

### T-1: Completeness vs. enforcement surface

The Purist's audit is exhaustive in cataloging what the spec says and does not say. It found 13 "Missing" items and 3 "Implied" items. But the audit does not distinguish between gaps that cause incorrect behavior and gaps that cause imprecise specification. The Mechanist's audit found only 3 "Broken" items -- cases where the system produces wrong output even if the executor follows every instruction perfectly.

The tension: The Purist would close all 16 gaps by adding text to the spec. The Mechanist would fix the 3 broken items and accept the rest as tolerable imprecision in a prompt-driven system. The Purist's approach produces a more complete spec at the cost of length and maintenance burden. The Mechanist's approach produces a leaner spec that is correct where it matters and loose where looseness is harmless.

Neither is wrong. But pursuing completeness without enforcement creates a spec that is heavy but still unenforceable. The Purist's 13 fixes add approximately 200 lines to SKILL.md. Those 200 lines are still just instructions to an LLM. They do not prevent incorrect behavior; they reduce the probability of misinterpretation. Whether that probability reduction justifies the maintenance cost is a judgment call, not a technical question.

### T-2: The "dead variable" interpretation of `{ITERATION}`

The Purist calls `{ITERATION}` a "dead variable" (Gap 1.2, severity: Low) and recommends either adding it to templates or removing it from the spec. The Mechanist also identifies `{ITERATION}` as absent from templates (Claim 6) but frames the issue differently: the iteration file-naming logic is "stateful logic in prose only" and the absence of `{ITERATION}` from templates means the orchestrator carries all iteration-tracking burden.

The tension is about what `{ITERATION}` is for. The Purist assumes it is a template variable that should appear in agent prompts. The Mechanist implicitly treats it as orchestrator state that the SKILL.md documents for the executor's benefit (the executor needs to know the iteration number to compute file paths), not for the agents' benefit.

If `{ITERATION}` is orchestrator state, it belongs in the SKILL.md's phase-execution instructions but not in templates. The Purist's variable audit methodology -- which maps every defined variable to template usage -- cannot represent this distinction. It sees a defined variable with no template consumer and flags it as dead. But the consumer is the orchestrator itself, not a template.

### T-3: Scope of "enforcement" in a prompt-only system

The Purist's audit evaluates whether the spec is complete. The Mechanist's audit evaluates whether the spec is enforceable. These are different questions applied to the same document, and they produce different severity rankings.

The Purist rates Gap 1.1 (`{AGENT_ROLE}` undefined) as "High -- red-blue mode is broken without these." The Mechanist rates the same issue (Claim 10C) as part of a "High" severity cluster but frames it as "even if the LLM follows every instruction perfectly, the variables do not exist." Both agree it is severe, but for different reasons. The Purist says the spec is incomplete. The Mechanist says the system is broken.

The tension: the Purist's fix (add variable definitions to SKILL.md) makes the spec complete but still relies on the executor to read and follow the new definitions. The Mechanist's fix would also require the same SKILL.md additions but would additionally flag that no enforcement exists to validate the variables are filled. The Purist's framework stops at "the spec now says what to do." The Mechanist's framework asks "and who checks that it was done?"

For a prompt-only system, the Purist's fix is sufficient in practice -- Claude Code reliably fills documented variables. But the philosophical gap remains: completeness is not enforcement, and the two audits use the same severity labels to measure different things.

---

## Safe Agreements

### SA-1: `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` are blocking defects for red-blue mode

The Purist's Gap 1.1 and the Mechanist's Claim 10C identify the same defect from different angles. The Purist: "An implementer would have to guess the mapping." The Mechanist: "An executor that only reads the SKILL.md's variable lists would not fill them, leaving literal `{AGENT_ROLE}` strings in agent prompts."

Both agree this is the highest-priority fix. Both agree the fix is to add explicit variable definitions to the SKILL.md's Phase 1, Phase 2, Phase 3, and Phase 4 variable sections mapping `config.agents[].role` to the template variables. No disagreement on diagnosis, severity, or remediation.

### SA-2: Phase 5 synthesis templates are missing `{TARGET_FILES}`, creating a multi-target gap

The Purist's appendix note on `{TARGET_PATH}` vs `{TARGET_FILES}` and the Mechanist's Claim 8 identify the same issue: synthesis templates use only `{TARGET_PATH}`, which for multi-file targets gives the synthesizer only the primary file path.

Both agree this is a real gap. The Purist frames it as a consistency question ("creates a question: when the target is multiple files, does the synthesis agent only see the primary target path?"). The Mechanist frames it as a contract violation ("contradicts the stated invariant that agents must read all target files"). Same defect, same recommended fix: add `{TARGET_FILES}` to Phase 5 variable definitions and synthesis templates.

### SA-3: Config validation error messages are inconsistently specified

The Purist's Gap 2.1 and the Mechanist's Claim 9 both identify that 3 of 11 validation rules have specified error messages while 8 do not. Both agree this inconsistency exists and both agree the arbiter-specific rules are the only ones with formal messages.

The disagreement (covered in DC-2) is about the remedy: the Purist wants to add message templates for all 11 rules; the Mechanist wants structured validation. But both agree on the underlying finding: the current spec is inconsistent in its level of rigor between arbiter validation (formal) and everything else (informal). This inconsistency is not in dispute.
