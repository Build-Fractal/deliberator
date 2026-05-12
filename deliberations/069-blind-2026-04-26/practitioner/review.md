# Practitioner Review — Constitutional Inclusion Criteria Gate

Audited from the perspective of an amendment author who must apply this gate when proposing a new principle. The lens is operational: does the gate help me, does it block me unfairly, can it be enforced, and would I know how to use it without consulting a maintainer?

---

### Executive Summary

The Constitutional Inclusion Criteria gate is a well-intentioned attempt to bound the constitution's growth and push judgment-call rules into operational guidance. It defines three criteria — mechanical verification capability, falsifiable scope, distinct-from-existing — and applies them prospectively to new principles only.

The gate is **operationally usable in roughly three of its four moving parts** but **substantially overengineered in the fourth (Criterion 1)** and **structurally unenforceable as a self-assessment**. The strongest single critique: the gate describes itself as a check that an amendment "qualifies for inclusion only if it satisfies all three" — yet there is no specified actor, hook, or PR template field that mechanizes the check. It is a self-assessment that the amendment author performs while writing the amendment, with no second pair of eyes mandated by the gate itself. That makes it a rubber stamp absent additional process scaffolding.

A separate problem: Criterion 1 ("mechanical verification capability") collides head-on with several grandfathered principles (X "Zen of Python Output", IX "Functional Programming and Clean Code", XVI "Mathematical Transparency") whose mechanical-check feasibility is dubious at best. A future author looking at those neighbors will reasonably conclude the criterion is honored more in the breach than the observance, weakening the gate's normative force.

The boundary between "constitution" and "operational guidance" is the gate's most useful contribution and is reasonably clear. The prospective-only carve-out is correctly handled. The friction cost on legitimate amendments is modest — a paragraph of justification — but the bug-prevention value is **conditional on the gate being actually applied**, which the current text does not ensure.

Net recommendation: **keep the gate but simplify Criterion 1, mechanize the application via PR template, and either drop the "feasible in one paragraph" sketch requirement or move it to a CONTRIBUTING.md checklist where it can be enforced procedurally.**

---

### Alignment

Places where the gate is operationally usable and earns its keep:

1. **Criterion 3 (distinct-from-existing) is genuinely useful.** An amendment author proposing, say, "Principle XXVIII: All Pydantic models must have explicit type annotations" can be mechanically rejected by pointing at IX's "Explicit Typing (non-negotiable)" subsection. The criterion gives a maintainer a textual lever to push refinements into the body of an existing principle rather than spawning a new Roman numeral. This is high-value and the wording is concrete enough to apply.

2. **The constitution-vs-operational-guidance distinction is the right boundary.** Pushing "judgment calls and rules of thumb" into `CONTRIBUTING.md`, specs, `SKILL.md`, or domain reference documents is exactly the right home for them. The gate names the receiving documents explicitly, which is an unusually concrete piece of governance.

3. **Prospective application carve-out is correctly drafted.** "Existing principles I-XXVII are grandfathered. Migrating any of them to operational guidance is a separate, intentional act governed by the same amendment process (with the receiving document identified explicitly in the migration spec)." This forecloses the most obvious bad-faith reading ("Principle X fails Criterion 1, therefore X is invalid") and provides a documented migration path.

4. **Criterion 2 (falsifiable scope) gives reviewers a clean rejection lever.** "If a reviewer must reason 'well, X might be okay if Y,' the principle is too vague" is a usable bright-line test. An amendment author writing "Principle XXVIII: Code should be elegant" gets a one-sentence rejection.

5. **The gate names the right alternative venues.** `CONTRIBUTING.md`, the relevant spec, `SKILL.md` instructions, domain-specific reference documents — these are the actual surfaces the project uses. The gate doesn't invent a new home for rejected principles, it routes them to homes that exist.

6. **Linkage to MAJOR/MINOR/PATCH versioning is consistent.** A principle that fails the gate would never become a MINOR bump (because it never gets added); a principle migrated out under the prospective carve-out is the kind of "principle removal" that justifies a MAJOR bump. The versioning and inclusion machinery cohere.

---

### Missed Opportunities

Places where friction is high, enforcement is weak, or the gate over-promises:

1. **Criterion 1 is internally inconsistent with the existing grandfathered set.** "Mechanical verification capability" would arguably reject Principle X (Zen of Python Output — "If the implementation is hard to explain, it's a bad idea"), Principle IX's clean-code prose ("Code should be self-documenting through clear naming and structure"), and Principle XVI (Mathematical Transparency — "the user MUST understand what is being optimized"). These cannot be linted. A future author proposing a similarly-styled principle will point at them as precedent. The gate then either applies inconsistently (rejecting new prose-principles while keeping old ones) or has its bite removed entirely. The grandfathering clause covers the legal question but does not solve the precedent question.

2. **The gate has no specified enforcer.** The text says "a principle qualifies for constitutional inclusion only if it satisfies all three" but does not say *who decides* it satisfies them. Self-assessment by the amendment author is the only reading. There is no PR template field, no CI check, no required maintainer sign-off, no sentence of the form "the reviewer of `/speckit.constitution` PRs MUST evaluate each criterion and document their conclusion in the PR description." This is the largest single gap. A gate that is not enforced becomes a rubber stamp the moment an author writes "I assert this satisfies all three" — which is exactly what the gate prohibits ("if a reviewer must reason 'well, X might be okay if Y'").

3. **Criterion 1's "concrete enough to sketch the check in one paragraph" subclause is itself unfalsifiable.** What counts as "concrete enough"? If I write "the linter could grep for `assert isinstance(...)` calls without a value assertion" — is that one paragraph? Two? Does it have to compile? The criterion meant to demand rigor introduces a meta-judgment-call. A reviewer who wants to wave a principle through can call any sketch "concrete"; a reviewer who wants to block can call any sketch "vague." This is the same problem Criterion 2 is supposed to prevent, recurring inside Criterion 1.

4. **"At least one form of automated check ... MUST be feasible" reads as a much higher bar than the project actually meets.** Many existing principles (XII Dead Infrastructure, XIII Enum Completeness, XXVI Meta-Testing) explicitly say "the linter SHOULD eventually check for X" — i.e., the check does not exist and may never. The gate accepts this ("does not have to exist at amendment time") but does not say what happens if the check is never built. Without a follow-through requirement, the criterion collapses to "the author must write a paragraph asserting feasibility," which is a documentation exercise, not a verification capability.

5. **No CI hook is specified to enforce the gate itself.** A trivially-buildable lint would parse `CONSTITUTION.md` for new principle headings (### II / ### III / etc.) added in the diff and require the PR description to contain three labeled subsections (Criterion 1 / Criterion 2 / Criterion 3) with non-empty content. That would convert self-assessment into a procedural artifact that reviewers can audit. The constitution does not specify this lint, does not require it, and does not name the PR template field that would carry the assessment. Without procedural scaffolding, the gate floats.

6. **The gate slows down legitimate amendments by an asymmetric amount.** A trivial amendment (refining IX's typing rules) costs maybe 10 minutes of authoring. A novel principle proposal now costs an additional 30-60 minutes of "justify Criteria 1-3" prose, and the rejection mode is "your sketch isn't concrete enough" — which has no clear path to remediation. The slowdown is acceptable for the value-add **only if** the gate is actually applied; absent an enforcer, the slowdown lands on conscientious authors and bypasses the rest. This selection effect is bad governance.

7. **The boundary between "constitutional" and "operational" is clearer in theory than in the actual existing principles.** Principle XXV ("Live Test Cost Discipline") is largely operational (CI configuration, marker taxonomy, gating job structure); Principle XVIII ("Progressive Disclosure Contract") includes a specific token budget (8-12k) that is operational tuning, not invariant. The gate would have rejected pieces of these had it existed earlier. An amendment author looking at the existing constitution will conclude that "operational guidance" is whatever the amendment author can credibly call "operational" — which is most things. The boundary leaks in practice.

8. **Criterion 3's "compose existing principles" test has no example.** The gate says "the principle MUST cover concerns not already addressable by composing existing principles" but provides zero examples of a hypothetical rejected principle and the composition that subsumes it. Without an example, an author cannot tell whether their proposal is a refinement (acceptable, goes in the body of an existing principle) or genuinely novel. A single worked example in the gate text would dramatically improve usability.

9. **The "principle's body, not as a new principle" subclause creates a body-bloat incentive.** If refinements go in the parent principle's body, large principles (IX, XV) become magnets for accretion. Principle IX already has a "v2.3.0 Extension" subsection. Over time, this approach produces a small number of giant principles rather than many small ones. That may be fine — but the constitution does not document this trade-off, and an amendment author cannot tell whether adding a five-paragraph "v2.5.0 Extension" to Principle IX is a feature or an antipattern.

---

### Off-Base Assumptions

1. **The gate assumes amendment authors are also adversarial reviewers of their own work.** This is the central enforceability problem. Self-assessment criteria assume good-faith authors who will reject their own pet amendments when the criteria fail. This is not how governance works in practice. Mature constitutional gates are applied by someone *other than* the proposer.

2. **The gate assumes "mechanical verification" is a uniform concept across the existing principle set.** It is not. Principle XIII (Enum Completeness) is grep-able. Principle X (Zen of Python Output) is not. The gate treats them as if a single criterion applies; in practice, different principles have radically different verification profiles, and the criterion does not acknowledge this.

3. **The gate assumes "operational guidance" documents are stable enough to be a credible alternative venue.** `CONTRIBUTING.md`, `SKILL.md`, and domain reference documents have their own version histories, ownership, and review processes. Migrating a principle to "operational guidance" without specifying *which* operational document and *who owns it* risks the principle landing in a less-stable home than the constitution. The gate names the categories but does not require the migration spec to identify the specific receiving file with its current owner.

4. **The gate assumes amendment frequency is low enough that the friction cost doesn't matter.** If conversus enters a phase of rapid principle accretion (which the v2.3.x and 2.4.0 series suggest), the gate's friction compounds. The cost of writing three justification paragraphs for every amendment is not zero, and the project has demonstrated willingness to accumulate principles quickly.

---

### Actionable Recommendations

In priority order. "Remove or simplify" is permitted by the brief and is invoked where warranted.

1. **Mechanize the gate via PR template, not prose.** Add a required section to the `/speckit.constitution` PR template: three labeled subsections (Criterion 1: Mechanical Verification / Criterion 2: Falsifiable Scope / Criterion 3: Distinct From Existing) with a CI lint that fails the PR if any subsection is empty when a new `### N. Principle Name` heading is added in the diff. This converts self-assessment into a procedural artifact and is the single highest-leverage change.

2. **Simplify Criterion 1 by dropping the "concrete enough to sketch in one paragraph" subclause.** Replace with: "The principle's wording MUST permit a future automated check (linter, parity test, structural assertion, or schema validation) that flags violations. The check need not exist at amendment time but the principle MUST name the artifact (file path, test pattern, or schema constraint) where the check would live." Naming a concrete location is a tighter, more falsifiable bar than "sketch in one paragraph."

3. **Remove Criterion 1 entirely and rely on Criteria 2 and 3.** Alternative to recommendation 2. If a principle has falsifiable scope (Criterion 2), an automated check is implicitly buildable; the explicit verification-capability criterion is redundant and conflicts with grandfathered principles like X and XVI. This is the most aggressive simplification and is defensible.

4. **Add a worked example to Criterion 3.** One paragraph showing a hypothetical proposed principle ("Principle XXVIII: All template variables must be lowercase") that is rejected because it composes from IX (Explicit Typing) + XI (Single Source of Truth) — and the refinement should land in the body of IX or XI. Without an example the criterion is harder to apply than it needs to be.

5. **Specify the enforcer.** Add one sentence: "Constitutional amendments MUST be reviewed by at least one project maintainer who is not the amendment author. The reviewer's evaluation against the three criteria MUST be documented in the PR." This closes the rubber-stamp gap.

6. **Reconcile the gate with grandfathered principles that fail Criterion 1.** Add a footnote: "Principles X, XVI, and the prose subsections of IX would not satisfy Criterion 1 under strict reading. They are retained under the prospective-only clause but should not be cited as precedent for new prose-principles." Without this, future authors will use these principles as a wedge against the gate.

7. **Require migration specs to identify the specific receiving file and owner.** The current text says "with the receiving document identified explicitly in the migration spec" but does not require the *current owner* of that document to sign off. Add: "and the maintainer of the receiving document MUST acknowledge the addition in the migration PR."

8. **Add a sunset clause for "linter SHOULD eventually check" provisions.** Across the constitution there are many "the linter SHOULD eventually check X" hedges. Add to the gate: "If a principle relies on a future linter for enforcement, the principle MUST cite a tracking spec or issue where the linter is being built, OR the principle's enforcement MUST be acceptable as code review only. Indefinite 'eventually' is rejected." This forces the project to either commit to building the check or admit the principle is review-only.

9. **Document the body-vs-new-principle trade-off explicitly.** Add a sentence: "Refinements that significantly extend an existing principle's scope (more than one paragraph of new normative text) MAY be proposed as new principles even when Criterion 3 is borderline; the constitution prefers many focused principles over few sprawling ones, when the alternative is a 'v2.X Extension' subsection larger than the original principle body." This addresses the body-bloat incentive without contradicting Criterion 3.

10. **Simplify the gate header from "Constitutional Inclusion Criteria" to "Amendment Inclusion Gate" and lead with the enforcement procedure, not the criteria.** A reader's first question is "how is this applied" not "what does it say." Reordering the section to lead with the PR template requirement and enforcer identity makes the gate read as governance machinery, not a manifesto.

---

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/069-blind-2026-04-26/CONSTITUTION-v2.4.0-blind.md` (target document, full read)
  - Governance section, Constitutional Inclusion Criteria subsection (lines 800-846)
  - Principle X (Zen of Python Output, lines 216-235) — cited as Criterion 1 conflict
  - Principle IX (Functional Programming and Clean Code, lines 136-214) — cited for prose-principle precedent and v2.3.0 Extension pattern
  - Principle XVI (Mathematical Transparency, lines 388-417) — cited as Criterion 1 conflict
  - Principle XIII (Enum Completeness, lines 308-327) — cited as grep-able example
  - Principle XII (Dead Infrastructure, lines 283-305) — cited for "linter SHOULD eventually check" pattern
  - Principle XXV (Live Test Cost Discipline, lines 658-700) — cited as boundary-leak example
  - Principle XVIII (Progressive Disclosure Contract, lines 449-475) — cited for operational tuning embedded in constitution
  - Principle XXVI (Meta-Testing for Parametrized Capabilities, lines 702-728) — cited for "linter SHOULD eventually" pattern
- `pyproject.toml` `[project] version` — referenced by Principle XXII as the single-source versioning anchor (not directly relevant to the gate but cited as an example of a mechanically-verifiable invariant the gate would accept cleanly).
- No external standards (PEP-8, agentskills.io, Keep a Changelog) needed for this audit; the gate is self-contained governance.

