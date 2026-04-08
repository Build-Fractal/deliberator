# Cross-Review of The Mechanist's Enforcement Audit

**Cross-reviewer**: The Pragmatist
**Reviewing**: The Mechanist
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: The Mechanist mischaracterizes `{PRIOR_FILES}` as "Broken" when it is working-as-designed

The Mechanist's claim 5 rates `{PRIOR_FILES}` as **Broken** on the grounds that the variable "does not appear in ANY template file" and that the SKILL.md "asks the executor to do runtime string surgery." This framing implies a defect -- something that was supposed to work and does not.

This is wrong. The SKILL.md explicitly describes a conditional append mechanism, not a template placeholder. The instruction says: "If `{PRIOR_FILES}` is non-empty, append this section to every agent prompt after the 'What to Read' section." The absence of a `{PRIOR_FILES}` slot in the templates is not a bug -- it is the design. The SKILL.md treats prior files as an optional runtime injection, not a static template variable. You do not put a placeholder for something that should not appear when the field is empty.

The Mechanist's own text acknowledges this: "In practice, it probably works because the instruction is clear." That admission contradicts the "Broken" verdict. A system that works as instructed and whose design is intentional is not broken. It is fragile -- I rated it as such in my own review -- because the instruction is positionally ambiguous (written inside the Phase 1 section but says "every agent prompt"). But fragile and broken are different categories. Calling this broken inflates the severity count and misdirects fix priority toward redesigning a mechanism that functions correctly, away from actual gaps like missing `{AGENT_DOCS}` documentation in Phase 2.

The Mechanist's proposed fix (add a `{PRIOR_FILES_SECTION}` placeholder to every template) would actually degrade the system: templates would contain an empty section header when no prior files exist, producing awkward prompts with "## Prior Context" followed by nothing.

### DC-2: Context isolation rated "High severity" ignores the operational reality of LLM agent systems

The Mechanist rates claim 3 (context isolation between agents) as **High severity** because "agents CAN read anything" on the filesystem. The Mechanist then acknowledges that "the templates are well-designed here: they list explicit file paths in 'What to Read' sections and do not mention other agents' output paths." Yet the severity remains High.

This contradicts the Mechanist's own architectural framing. The opening section correctly identifies that Conversus is "a pure prompt-instruction system" where "the LLM IS the engine." In such a system, instructional isolation IS the enforcement mechanism. There is no other kind. Rating instructional isolation as High severity is equivalent to saying the entire system is fundamentally unacceptable -- but the Mechanist's own conclusion calls the instructional-only claims "acceptable for a prompt-driven orchestration system IF the executor is reliable."

You cannot simultaneously say instructional enforcement is acceptable AND rate instructional enforcement as High severity. The Mechanist needs to pick a lane. Either the prompt-instruction model is valid (in which case well-designed template isolation is Medium at worst) or it is not (in which case every claim is High severity and the entire audit should recommend scrapping the approach).

My review found that the templates are the strongest enforcement surface in the system -- they structure what agents see and constrain where they write. The Mechanist agrees with this assessment in prose but contradicts it in the severity rating.

### DC-3: The variable consistency table conflates severity levels that differ by an order of magnitude

The Mechanist's claim 10 groups five variable mismatches into a single "Broken -- High severity" verdict. But the individual items have wildly different impact:

- `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` missing from SKILL.md documentation: These are **red-blue mode only** variables. The Mechanist discovered them in red-blue templates, which is a non-default mode. An executor running cooperative mode (the default and most common case) will never encounter this gap. This is a documentation gap in a secondary mode, not a High severity system failure.
- `{PRIOR_FILES}` and `{ITERATION}` absent from templates: As argued in DC-1, `{PRIOR_FILES}` absence is by design. `{ITERATION}` absence is dead weight -- harmless in either direction.
- `{AGENT_DOCS}` not listed for Phase 2: This IS a real gap that could cause a literal `{AGENT_DOCS}` string to appear in agent prompts -- the one item that deserves the "Broken" label.

Rolling these into a single High-severity finding creates a false sense of crisis. One of the five is genuinely broken (undocumented `{AGENT_DOCS}` for Phase 2), one is a documentation gap in a secondary mode, and three are either by-design or harmless. The Mechanist's summary table says "5 variables mismatched" which reads as five equally severe problems. They are not.

---

## Tensions

### T-1: Disagreement on whether `{PRIOR_FILES}` should be a template variable or a runtime append

The Mechanist advocates converting `{PRIOR_FILES}` from a runtime append to a standard template variable (`{PRIOR_FILES_SECTION}`). My review accepts the runtime append design but flags its positional ambiguity (written in Phase 1 section, applies to all phases).

The tension is real: template variables are more predictable for LLM executors (simple find-and-replace), while runtime appends require the executor to remember a conditional instruction across phases. The Mechanist optimizes for predictability. I optimize for clean output (no empty sections when prior files are absent).

A middle path exists that neither review proposes: keep the runtime append design but move the instruction to a standalone section titled "Cross-Phase Injections" placed before the per-phase instructions, eliminating the positional ambiguity I flagged without introducing empty template placeholders.

### T-2: What counts as "enforcement" in a prompt-only system

The Mechanist's framing -- "That is not enforcement. That is hope." -- sets a standard where only programmatic validation counts as enforcement. My review uses a softer standard: if an instruction is clear enough that a competent LLM will follow it reliably, that is sufficient enforcement for a system whose entire execution model is LLM interpretation.

This tension runs through every finding. The Mechanist rates nine of ten claims as "Instructional Only" with an implicit negative connotation. My review uses "Works" for instructions that are clear and complete, "Fragile" for instructions that are ambiguous or have edge cases, and "Broken" only for things that will produce wrong output even with perfect instruction-following.

The disagreement matters for prioritization. Under the Mechanist's framework, the system needs a validation engine to be acceptable. Under mine, it needs four targeted fixes to the SKILL.md and templates. These are very different investment levels with very different timelines.

### T-3: Severity of the synthesis `{TARGET_FILES}` omission

Both reviews identify the missing `{TARGET_FILES}` in Phase 5 synthesis templates. The Mechanist rates it "Broken (Phase 5) -- Medium severity." I rate it "Fragile -- P1 fix priority."

The tension: the Mechanist calls it Medium because "the synthesizer reads all the reviews, cross-reviews, revisions, and disputes (which themselves reference all target files), so the information is indirectly available." I give it P1 priority because the synthesizer should be able to verify claims against original source material, not rely on second-hand references through agent outputs.

We agree on the fix (add `{TARGET_FILES}` to Phase 5). We disagree on urgency. The Mechanist's "indirectly available" argument is correct for cooperative mode where agents faithfully quote sources, but breaks down in adversarial modes where agents may selectively cite. For a system that supports four deliberation modes including red-blue and winner-take-all, the synthesizer needs direct access to source material.

---

## Safe Agreements

### SA-1: Template variable mismatches between SKILL.md and templates are the highest-priority fixes

Both reviews independently identify the same core set of template-variable problems. The Mechanist's claim 10 and my finding 3b converge on `{AGENT_DOCS}` missing from Phase 2 documentation. Both reviews identify `{TARGET_FILES}` missing from Phase 5 synthesis. Both reviews flag `{ITERATION}` as defined but unused. The specific items and the conclusion that these are the most actionable fixes are in full agreement.

### SA-2: The `disputes_remain` trigger is fragile but fail-safe, and the fail-safe direction is correct

The Mechanist (claim 7) and my review (finding 5a/5b) both conclude: the trigger parsing depends on exact markdown formatting from an LLM, which is inherently fragile; the fallback ("if unparseable, run Phase 6 anyway") is the correct engineering choice because it fails toward action rather than toward silent omission. Neither review recommends a critical fix here. The Mechanist suggests structured output (JSON/YAML) as a hardening measure; I suggest an HTML comment marker. Both are optional improvements to a design that already fails safely.

### SA-3: The iteration filename special case (revision.md vs revision_1.md) is a real ambiguity that needs explicit documentation

The Mechanist (claim 6) identifies the asymmetry: iteration 1 produces `revision.md` while iteration 2+ produces `revision_{N}.md`, creating a special case where "revision_{N-1}.md when N=2" must resolve to `revision.md` not `revision_1.md`. My review (finding 2b) reaches the identical conclusion with the identical fix: add an explicit note clarifying the resolution rule. Both reviews rate this as medium-priority. Full agreement on problem, severity, and fix.
