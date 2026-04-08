# Cross-Review of functional-typing (Round 2)

**Reviewer**: integration-architect
**Reviewing**: functional-typing's Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: Heading count inconsistency is asserted but not propagated to refine invariant rule (a)

Functional-typing's MO-1 correctly identifies that adopting `## Status` (Change 10) raises the required heading count from 7 to 8 and that Change 1's heading list must be updated. Functional-typing then states in Rec #1 that the validation must check for 8 headings, listing all nine headings including `## Status`. However, functional-typing's own Rec #3 proposes adding a fifth refine invariant (Status re-evaluation) without updating the text of rule (a) in the same recommendation. The Round 2 review references Change 7 rule (a) as "All 7 required headings" and says "this must become 'All 8 required headings'" (MO-1), but Rec #3 only adds invariant (e) -- it does not explicitly restate rule (a) with the updated count.

This matters because the two recommendations (Rec #1 and Rec #3) target different change items (Change 1 and Change 7 respectively) and could be adopted independently. If Rec #3 is adopted but Rec #1's heading-count fix is missed in Change 7, the refine invariants would reference 7 headings while the schema requires 8. Functional-typing identified the problem but did not close the loop in the recommendation text.

My review avoids this issue because I reference "all required headings" without hardcoding a count (R7: "four verifiable post-conditions: (a) all headings preserved"), which remains correct regardless of whether `## Status` is adopted. Functional-typing's explicit count is more precise but creates the coupling risk described above.

### DC-2: `## Status` placement between `# Problem Definition` and `## Decision` contradicts spec schema ordering

Functional-typing's RD-1 concession specifies a structural constraint: "The `## Status` section goes between `# Problem Definition` and `## Decision` in the schema" (RD-1, condition 3). This would produce the heading order: `# Problem Definition` -> `## Status` -> `## Decision` -> `## Type` -> etc.

This placement contradicts the semantic flow of the `problem.md` schema. In the spec (spec.md L45-71) and SKILL.md (L822-850), `# Problem Definition` is the document title and `## Decision` is the first substantive content section -- the one-sentence statement that anchors the entire artifact. Inserting `## Status` between the title and the decision statement breaks the reading flow: a user opening the file sees a metadata field before understanding what the decision even is.

My review does not specify placement. If `## Status` is adopted, it should go at the end of the schema (after `## Source Documents`) or as frontmatter-style metadata before `# Problem Definition`, not between the title and the anchoring section. The arbiter's framing of status as a "factual annotation" (resolution.md, RD-1) supports placement at the end or as metadata -- factual annotations describe the artifact's completeness, which is a property of the whole document, not a section that precedes the content.

This is dangerous because if adopted as functional-typing specifies, it would require reordering the canonical schema in both spec.md and SKILL.md, changing every heading-index reference in the deliberation, and degrading the user experience for the non-expert audience (spec.md L87) who needs to see the decision statement first.

---

## Tensions

### T-1: Scope of `## Status` re-evaluation during refine (MO-2 vs. my MO-1)

Functional-typing's MO-2 proposes a fifth refine invariant: "(e) Status must be re-evaluated based on `[CLARIFY:]` tag count in the refined output." My MO-1 raises a related but distinct concern: what happens when a user runs `/conversus define` against a `problem.md` that is already `status: ready` with zero `[CLARIFY:]` tags.

The tension is in the granularity of the contract. Functional-typing's invariant (e) is mechanical: recount the tags, update the status. My concern is behavioral: should a refine pass on a complete artifact re-evaluate all sections or only incorporate new input? These are not contradictory but they pull the spec in different directions. Functional-typing's formulation keeps status purely tag-driven (a computed property), which is consistent with the arbiter's factual-annotation framing. My concern asks whether the refine path might introduce new `[CLARIFY:]` tags on sections that were previously resolved, which is an agent-judgment question the spec cannot fully constrain.

I lean toward functional-typing's mechanical formulation as the right level of specification. The status field should be a pure function of tag count, not a judgment call. But the behavioral question in my MO-1 (does refine re-evaluate previously resolved sections?) remains open and is orthogonal to tag counting.

### T-2: Strictness of "no SHOULD language" condition on `## Status`

Functional-typing's RD-1 concession includes the condition: "No RFC 2119 SHOULD language prescribing downstream behavior" (RD-1, condition 2). My review takes a softer position: "Whether spec 008 treats `draft` as blocking is spec 008's decision" (RD-1 Round 2 position). Both agree that spec 007 should not prescribe consumer behavior. But functional-typing's condition explicitly bans SHOULD language, while my position simply notes the jurisdictional boundary.

The tension is that functional-typing's explicit ban could be read as constraining the synthesis's language choices beyond what is necessary. The arbiter already set aside devils-advocate's "SHOULD check" language (resolution.md, RD-1). Restating this as a formal condition on the concession creates a negative requirement ("must not contain SHOULD") rather than a positive one ("spec 007 defines what the field is; spec 008 defines what to do with it"). Negative requirements are harder to verify and can generate false positives during review -- any use of the word "should" near the `## Status` section could trigger objections even if the sentence is purely descriptive.

The arbiter's jurisdictional framing is sufficient without the explicit ban. Both positions reach the same outcome but through different enforcement mechanisms.

### T-3: FR coverage verification -- exhaustive listing vs. confirmation by reference

Functional-typing provides a complete FR-by-FR mapping (FR-001 through FR-012 with specific SKILL.md line numbers) in the "FR coverage verification" section. My review confirms FR coverage by reference to Round 1 ("I reaffirm all convergence items C-1 through C-13") without re-enumerating the mapping.

The tension is methodological. Functional-typing's exhaustive listing is more auditable -- a reader can verify each mapping independently. My approach is more concise but depends on the reader trusting the Round 1 synthesis. Neither is wrong, but they represent different review philosophies. For a Round 2 review where the convergence items are settled, my approach is appropriate (re-enumerating settled items adds length without adding signal). For a reference document that may be read independently of Round 1, functional-typing's approach is more self-contained.

This is a stylistic tension, not a substantive disagreement.

---

## Safe Agreements

### SA-1: All five dispute resolutions converge

Functional-typing and I reach identical positions on all five remaining disputes:

- **RD-1** (`## Status`): Both concede, adopting the arbiter's factual-annotation framing. Both reject RFC 2119 SHOULD language for downstream prescription. Both ground the concession in SKILL.md L865 (count already computed) and spec.md L87 (non-expert user principle).
- **RD-2** (Shared validation): Both concede to the schema-layer approach. Both adopt the arbiter's one-sentence prose contract. Both agree the dispatch section (SKILL.md L18-34) must remain minimal.
- **RD-3** (Multi-path `--context`): Both maintain deferral. Both adopt the arbiter's reframing of SKILL.md L797 directory support as the designed multi-source pattern, not a workaround. Both cite spec.md L35 (FR-006 singular `--context <path>`).
- **RD-4** (`--force`/`--dry-run`): Both maintain deferral. Both cite the arbiter's interactive-context argument and spec.md L87.
- **RD-5** (Refine semantics): Both adopt the four-rule normative contract with the diff summary as recommended practice. Both cite the arbiter's structural-invariant vs. UX-guidance distinction.

This is the strongest agreement surface across the entire deliberation. All five disputes are resolved with aligned positions and consistent grounding.

### SA-2: P1 changes are unanimous and unchanged

Both reviews reaffirm Changes 1, 2, and 3 (post-write schema validation, `--context` path validation, dispatch matching semantics) as P1 unanimous without modification. No reviewer in the entire deliberation has contested these. They are the review's most robust output.

### SA-3: All Round 1 concessions are confirmed without reversal

Functional-typing explicitly states "None identified" under Off-Base Assumptions. My review confirms all six prior concessions stand with no reversals. Neither reviewer walks back any Round 1 disposition change. The deliberation has been monotonically convergent -- positions have only moved toward agreement, never away from it.

### SA-4: Arbiter's contributions are accepted as structurally sound

Both reviews treat the arbiter's advisory opinions as well-grounded and adopt them without contestation. Functional-typing: "The arbiter's advisory opinions are well-grounded in specific SKILL.md lines and spec.md constraints" (Off-Base Assumptions). My review adopts the arbiter's framing on RD-1 (factual annotation), RD-2 (boundary validation precedent), RD-3 (directory-as-design), RD-4 (interactive context), and RD-5 (normative vs. recommended). This shared acceptance of the arbiter's contributions means the arbitration layer functioned as designed -- it provided operational grounding that moved both reviewers toward convergence.

### SA-5: Refine invariants as testable post-conditions

Both reviews agree that the four-rule refine contract defines structural invariants (testable post-conditions) while the diff summary is UX guidance (context-dependent). Functional-typing: "structural invariants are testable against output; UX guidance varies by context" (RD-5). My review: "The four rules define what the output must satisfy -- they are testable post-conditions a downstream consumer can depend on" (RD-5). The language is nearly identical, reflecting genuine convergence on the nature of the contract.

### SA-6: C-4 through C-13 are settled without further analysis

Both reviews confirm the remaining convergence items without reopening them. Functional-typing: "I reaffirm all remaining convergence points at their established priority levels without modification. None require further analysis from my perspective." My review: "C-4 through C-13: All confirmed without modification." These items consumed significant Round 1 effort and are now fully resolved.
