# Template-Approach Cross-Review of Engine-Approach's Round 2 Review

**Reviewer**: template-approach
**Reviewing**: engine-approach's Round 2 review
**Round**: 2 of 3, winner-take-all deliberation on spec 004

---

## Overview

The engine-approach's Round 2 review is the strongest document they have produced in this deliberation. The rhetorical overreach of Round 1 -- the constitutional arguments, the claim to a competing architecture, the suggestion that mode behavior belongs in the engine -- is gone. What remains is a disciplined set of three concrete proposals, each framed as an enhancement to the template-first architecture. The engine-approach has fully internalized the Round 1 outcome and is now arguing within the framework they conceded is correct.

The question for this cross-review is whether the three remaining disputes can now be resolved. My assessment: yes, all three can converge. The gap between the two positions has narrowed to documentation wording and tool classification, not architecture.

---

## Dispute 1: Whether "Mode-Parameterized" Has Architectural Significance Beyond Naming

### Can This Dispute Resolve? Yes.

The engine-approach proposes a "Mode Interface Contract" section in SKILL.md listing the three mode-keyed tables with a checklist for adding new modes. My Round 2 review proposes extending the existing contract language at SKILL.md line 683 to cover all three tables. These proposals are substantively identical. The difference is organizational: the engine-approach wants a new dedicated section; I proposed extending the existing "Stable interface contract" paragraph.

I accept the engine-approach's framing of a dedicated section. A standalone "Mode Interface Contract" subsection in SKILL.md's "Important Notes" is cleaner than appending to the existing paragraph at line 683. The existing paragraph already calls out the Dispute-Parsing headings as a stable interface contract and warns that changes are breaking. Extending that pattern to Phase 6 validation headings and role enforcement rules in a single, consolidated location is better documentation. This is what both sides are asking for.

**Where I push back:** The engine-approach frames this as resolving the question of whether "mode-parameterized" has "architectural significance beyond naming." I maintain it does not. What it has is documentation significance -- the mode-keyed tables are important enough to document explicitly as an interface contract. The engine-approach's own proposal confirms this: their "Mode Interface Contract" section is a documentation change, not an architectural one. The engine-approach even says so ("This is a documentation change. It preserves the template-first architecture. It adds zero conditional branches"). We agree on the action. We disagree on whether the action vindicates the phrase "architectural significance." That disagreement is now purely semantic and has no practical consequence.

**Resolution:** Converged. Add a "Mode Interface Contract" subsection to SKILL.md documenting all three mode-keyed tables with a new-mode checklist. Both sides proposed essentially this. The terminological question ("architectural significance" vs. "documentation significance") is moot because the concrete action is identical either way.

---

## Dispute 2: Whether Role Enforcement Generalizes to "Some Mode Behavior Categorically Cannot Live in Templates"

### Can This Dispute Resolve? Yes.

The engine-approach has made two important moves in Round 2:

1. **Withdrew the generalization.** "I accept the judge's scoping and withdraw the generalization." This was the core of the dispute. The engine-approach no longer claims role enforcement proves that "mode behavior" writ large has an engine-owned category. They now claim only that configuration validation can be mode-specific -- which I already agreed to in Round 1 (Convergence point 8) and reiterated in my Round 2 review.

2. **Proposed a bounded acknowledgment.** They want a fourth item in the Mode Interface Contract: "mode-specific configuration validation rules (currently: red-blue role coverage)." This is a reasonable addition. It makes the set of engine-owned mode-specific obligations complete: three data tables plus the validation rules that depend on them.

**Where I push back on framing:** The engine-approach disputes my analogy that role enforcement is "structurally identical to validating that `rounds` is a positive integer." They argue that role enforcement is categorically different because it is mode-specific while `rounds` validation is mode-invariant. This is factually correct -- role enforcement does branch on mode. But the engine-approach concedes that "it does not carry architectural weight beyond documentation," which is exactly what my analogy was meant to demonstrate. Both are config-parse-time preconditions. Both fire before any template loads. Both are engine-owned. The mode-specificity of role enforcement makes it a more interesting specimen in the validation category, but it does not elevate it into a different architectural layer. The engine-approach now agrees with this conclusion, so the dispute over the analogy's precision is academic.

**Where the engine-approach strengthened my position:** By withdrawing the generalization and accepting the judge's scoping, the engine-approach has eliminated the wedge concern that motivated my Round 1 resistance. If role enforcement is explicitly documented as a parse-time precondition (not runtime mode behavior), and if the template-first architecture's self-description says so clearly, then future contributors cannot cite this precedent to argue for expanding engine-level mode logic. The documentation itself becomes the boundary.

**Resolution:** Converged. Add mode-specific configuration validation rules as a recognized category in the Mode Interface Contract section, scoped explicitly to parse-time preconditions. Both sides agree on the facts, the scoping, and the documentation action. The dispute over whether the `rounds`-validation analogy is structurally identical or merely structurally similar has no practical consequence.

---

## Dispute 3: Whether a Template Heading Linter Is a "Template-Layer Tool" or "Engine-Adjacent Infrastructure"

### Can This Dispute Resolve? Yes, with an explicit pragmatic agreement.

The engine-approach has made a productive move: "I propose we resolve it pragmatically rather than continuing to debate the taxonomy." They then define the linter's specification in terms of validation source (SKILL.md dispatch tables), validation target (template output sections), and change coupling (bidirectional). This is a reasonable specification regardless of classification.

My Round 2 review proposed: "Classify the linter as a 'template validation tool that enforces the stable interface contract defined in SKILL.md.'" The engine-approach proposes defining the linter by its specification rather than its category. These are compatible: my classification is a label; their specification is a definition. A tool can have both.

**Where I push back:** The engine-approach argues that calling the linter a "template tool" implies its validation rules are self-contained within the template layer, and that a maintainer working in SKILL.md would have "no reason to look for it." This concern is valid in principle but overstated in practice. The Mode Interface Contract section (which both sides now support) would explicitly state that changes to the dispatch tables require coordinated updates to templates and their validation tooling. A maintainer reading the Mode Interface Contract would find the linter referenced there. The classification of the linter does not determine its discoverability -- the documentation does.

**Where the engine-approach is correct:** Their point about the JSON Schema analogy is well-taken. A JSON Schema validator is described by what it validates against (the schema), not by what it operates on (JSON files). Similarly, a template heading linter is best described by what it validates against (the interface contract). My classification ("template validation tool") emphasizes what it operates on. The engine-approach's specification ("interface-contract enforcement") emphasizes what it validates against. Both are accurate descriptions of the same tool from different angles.

**Practical resolution:** The linter's specification should include:
1. What it validates: template output headings.
2. What it validates against: SKILL.md's mode-keyed dispatch tables.
3. When it runs: development time (CI, pre-commit).
4. Where it is referenced: the Mode Interface Contract section of SKILL.md.
5. Maintenance trigger: changes to either dispatch tables or template outputs.

Whether we call it a "template validation tool" or an "interface-contract enforcement tool" is a labeling preference. I stated in my Round 2 review (Flexibility item 4) that I can accept the "interface-contract enforcement tool" label provided it does not imply the linter belongs in the engine's runtime execution path. The engine-approach explicitly agrees it should not: "Whether this linter lives in a `tools/` directory, a `templates/lint/` directory, or a CI pipeline is a project-structure decision."

**Resolution:** Converged. Define the linter by specification (inputs, outputs, timing, dependencies) rather than fighting over a single-phrase classification. If a label is needed, "interface-contract validation tool" captures both sides' concerns: it validates templates (my emphasis) against the interface contract (their emphasis). Neither side claims it should run at engine runtime.

---

## Assessment of Engine-Approach's Competitive Position

The engine-approach closes with a competitive argument: the template-first architecture has three "documentation gaps that create silent-failure risks." They cite the heading drift caught in Round 1 (`### Remaining Contested Positions` instead of `### Remaining Disputes`) as evidence that these gaps are not hypothetical.

This is a fair point. The heading drift was a real finding from the constitutional review phase, and it demonstrates exactly the kind of failure that explicit interface-contract documentation mitigates. The engine-approach is correct that documenting these contracts reduces maintenance risk.

However, I note that the engine-approach frames these as gaps in "the template-first architecture" when they are gaps in the current documentation of that architecture. The architecture itself handled the heading drift correctly -- the Dispute-Parsing Subsystem's fallback chain (structural markers first, then headings, then default-to-true) meant that the incorrect heading would have triggered the safety default rather than silently suppressing arbitration. The architecture is robust. The documentation can be more explicit. Both sides agree on this.

The engine-approach's final paragraph asks the judge to evaluate whether any rejection from me is "substantive (the enhancements are harmful) or territorial (acknowledging engine-layer obligations feels like conceding ground)." I reject this framing as a false dichotomy. My Round 2 review accepted all three enhancements. I proposed concrete resolutions for each. I offered flexibility on the linter classification (Flexibility item 4). There is nothing to reject. The engine-approach is pre-rebutting a rejection that did not occur.

---

## Summary: All Three Disputes Can Converge

| Dispute | Engine-Approach Proposal | Template-Approach Proposal | Gap | Convergence Path |
|---------|--------------------------|----------------------------|-----|------------------|
| 1: Mode-keyed tables | Mode Interface Contract section in SKILL.md | Extend existing contract language at line 683 | Organizational (new section vs. extended paragraph) | Accept engine-approach's dedicated section format. Both sides agree on content. |
| 2: Role enforcement | Fourth item in Mode Interface Contract; mode-specific config validation as recognized category | Acknowledge mode-specific config validation; scope to parse-time preconditions | None substantive. Both sides agree on action and scoping. | Adopt the engine-approach's fourth item. Both sides already agree. |
| 3: Linter classification | Define by specification; defer categorization | "Template validation tool enforcing SKILL.md interface contract" | Labeling preference only. Both sides agree on specification, timing, and maintenance. | Define by specification. Use "interface-contract validation tool" if a single label is needed. |

All three disputes resolve to documentation and specification actions that both sides have now explicitly endorsed. No architectural changes. No engine expansion. No conditional branches. The template-first architecture is enhanced by making its implicit contracts explicit.

The deliberation should converge in Round 3.
