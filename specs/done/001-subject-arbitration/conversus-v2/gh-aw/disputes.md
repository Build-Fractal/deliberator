# gh-aw Final Disputes: Subject Arbitration (Phase 6) -- v2

**Agent**: gh-aw (GitHub Agentic Workflows)
**Date**: 2026-03-19
**Phase**: Final disputes after v2 revision round
**Inputs**: All three v2 revised positions (APM, spec-kit, gh-aw)

---

## Remaining Disputes

### Dispute 1: "Dispute entry" definition -- pattern-matching vs. content-negative

**Disputed with**: APM (modified P1-1)

All three agents agree that "dispute entry" must be defined before SKILL.md is synced (gh-aw N-2, APM P1-1, spec-kit P1-3). The disagreement is over what constitutes a dispute entry between the structural markers.

- **gh-aw (modified P1-2)**: Any line containing non-whitespace content that is not an HTML comment. This is a content-negative definition: it excludes two specific categories (whitespace, HTML comments) and treats everything else as a dispute signal.
- **APM (modified P1-1)**: Any line matching the `**Dispute:**` pattern, or at minimum any line beginning with a Markdown bold marker (`**`). This is a pattern-positive definition: it requires a specific formatting convention.
- **spec-kit (modified P1-3)**: Adopted gh-aw's positive framing ("any non-whitespace content between the markers constitutes at least one dispute entry") for the `disputes_remain` trigger.

APM's concern about false positives from stray template artifacts is valid, which is why gh-aw revised to exclude HTML comments. But APM's proposed remedy -- coupling the primary trigger to the `**Dispute:**` pattern -- collapses the distinction between the primary and fallback mechanisms. If the primary mechanism requires `**Dispute:**` formatting, it is functionally identical to the heading-based fallback that all three agents agree is the inferior path. The entire point of structural markers was to decouple trigger evaluation from Markdown formatting conventions. APM's pattern requirement re-couples them.

The practical consequence: a Phase 5 agent that writes disputes in any format other than `**Dispute:** ...` between the markers would fail to trigger Phase 6 under APM's definition, even though the content is clearly dispute material. This makes the trigger mechanism fragile to Phase 5 template changes -- the exact problem the markers were designed to solve.

gh-aw maintains that the content-negative definition (exclude whitespace and HTML comments, everything else triggers) is correct. If a Phase 5 template produces non-comment, non-whitespace content between dispute markers that is not actually a dispute, the Phase 5 template is buggy, and triggering Phase 6 with a diagnostic is the correct behavior -- it surfaces the bug rather than silently swallowing it.

### Dispute 2: Structured output schema -- advisory fields vs. prose conventions as the v1 contract

**Disputed with**: spec-kit (modified P2-4)

The v1 disputes saw a three-way disagreement on structured output. The v2 revisions collapsed this into a two-position split with a novel hybrid from spec-kit:

- **gh-aw (modified P3-8)**: Extract schema fields to a standalone "Deferred: Structured Output" section with SHOULD-level language. The fields are advisory, subject to revision after implementation experience. No v1 prose-level structural requirements on the arbiter beyond FR-018 section headings.
- **spec-kit (modified P2-4)**: Withdraw the normative FR. Adopt gh-aw's organizational recommendation (standalone section) AND adopt APM's prose conventions (`**Dispute:**`, `**Ruling:**`, `**Grounding:**` labels) as a v1 template instruction in FR-015. The prose conventions are "the v1 contract"; the schema fields are "the v2 aspiration."
- **APM (N-1)**: Endorse spec-kit's normative schema FR with a cardinality fix (`affected_target_files` as list). The schema is normatively important for future versions.

Spec-kit's hybrid sounds reasonable but creates the dual-binding problem APM's own cross-review warned about. If FR-015 requires labeled sub-fields in Binding Decisions entries (`**Dispute:**`, `**Ruling:**`, etc.) AND a deferred section declares advisory schema fields (`dispute_id`, `ruling_type`, etc.), the spec contains two parallel representations of the same semantic contract at different normative levels. When v2 arrives and the schema fields are elevated, they must either align perfectly with the prose labels (in which case the prose labels were an unnecessary intermediate step) or diverge (in which case the v1 template instructions become a migration burden).

gh-aw's position is unchanged from the v1 disputes: the arbiter is an LLM agent whose output is probabilistic prose. Adding labeled sub-field requirements to FR-015 (spec-kit's hybrid) is a softer version of the same mistake as requiring YAML (spec-kit's v1 position) -- it asks the arbiter to produce structurally regular output that downstream tooling will depend on, and then provides a degradation path (FR-023 warnings) for when the arbiter inevitably varies. The correct v1 contract is FR-018 section headings only. The correct v2 preparation is SHOULD-level advisory fields in a standalone section, giving future implementors a starting point without binding the current template.

The cardinality fix (`affected_target_files` as list) is correct regardless of normative status. gh-aw accepts the pluralization.

### Dispute 3: FR-022/FR-023 boundary test -- section-heading presence vs. prose parseability

**Disputed with**: APM (N-3, three-tier model)

All three agents now agree on a three-tier failure model. The dispute is over the bright-line test that separates tier 2 (structurally unintelligible, no file written) from tier 3 (incomplete but parseable prose, file written with warning).

- **gh-aw (modified P1-1)**: The boundary is: does the output contain at least one FR-018 section heading? If yes, tier 3. If no, tier 2. This is a heading-presence test -- a single regex check against the FR-018 heading list.
- **APM (N-3)**: The boundary is: can the output be "parsed as prose"? Prose parseability is the criterion, with section headings as a downstream validation within tier 3. Structurally unintelligible output is "output that cannot be parsed as prose (e.g., raw YAML dump, refusal message, output in wrong language)."

APM's "parsed as prose" criterion is not a bright-line test. It requires the engine to determine whether arbitrary text constitutes "prose" -- a judgment that is trivial for humans but undefined for machines. What parser determines prose-ness? A language detector? A sentence-structure analyzer? The examples APM provides (raw YAML, refusal message, wrong language) are recognizable by humans but each requires a different detection mechanism. An engine that must distinguish "prose in English" from "prose in French" or "a polite refusal formatted as prose" from "a legitimate resolution that happens to decline a ruling" is performing semantic classification, not structural validation.

gh-aw's heading-presence test is a mechanical check: scan the output for any string matching an FR-018 section heading (`## Process Note`, `## Binding Decisions`, `## Summary of Changes Required`, `## Confidence Assessment`). If at least one is found, the output is recognizably an attempt at resolution -- write it with a warning listing the missing headings. If zero are found, the output is not an attempt at resolution -- discard it with a diagnostic. This is implementable in any language with a regex engine, produces deterministic results, and requires no semantic judgment.

gh-aw maintains that the heading-presence test is the correct boundary. APM's "prose parseability" criterion is the right intuition but the wrong specification -- it describes what the test should feel like, not what it should do.

---

## Convergence

### Convergence 1: Three-tier failure model for FR-022/FR-023

The v1 disputes contained a two-way disagreement (gh-aw's two-tier model vs. the implicit single-tier in the spec). The v2 revisions produced full convergence on the three-tier structure:

1. Agent-process failure (FR-022): no output produced. No file. Diagnostic.
2. Structural unintelligibility (FR-022 sub-case): agent completed, output is not a resolution attempt. No file. Diagnostic.
3. Incomplete but parseable (FR-023): agent completed, output is a recognizable resolution attempt with missing sections. File written. Warning.

APM proposed the three-tier model (N-3). gh-aw accepted it (modified P1-1). spec-kit endorsed the disambiguation (N-1). The remaining dispute (Dispute 3 above) is about the tier 2/3 boundary test, not the tier structure itself. The three-tier model is settled.

### Convergence 2: Content-presence guard scoped to `trigger: disputes_remain` only

The v1 disputes left the interaction between empty markers and `trigger: always` unresolved. The v2 revisions produced convergence:

- The whitespace/empty-content guard applies only to `trigger: disputes_remain`. Empty markers cause the trigger to evaluate to `false`.
- For `trigger: always`, the trigger fires regardless of content. The engine SHOULD log a diagnostic if `{REMAINING_DISPUTES}` extraction produces empty content.

APM (N-5), spec-kit (modified P1-3), and gh-aw (P3-6 + modified P2-5) all converge on this scoping. The endorsement path under `trigger: always` is preserved. This resolves the v1 tension where spec-kit's harder gate would have broken `trigger: always` semantics.

### Convergence 3: Draft template filtering requires a normative FR

The v1 disputes contained a disagreement about directory separation vs. markers for draft templates. The v2 revisions resolved the mechanism question (markers won; gh-aw withdrew the directory preference) and surfaced a new consensus: the Constraints-section MUST for draft template filtering has no testable FR, and one must be added.

APM (N-4), spec-kit (N-2), and gh-aw (surviving P2-3) all recommend adding an FR (proposed FR-028 or equivalent) requiring the engine to skip templates with the draft marker and emit a diagnostic. gh-aw additionally recommends documenting the layered defense relationship between FR-004 (config-time gate) and the new FR (dispatch-time gate) (surviving P3-7, unchallenged). This is settled.

### Convergence 4: SKILL.md sync must follow dispute-entry definition

The v1 disputes did not address SKILL.md sync sequencing because the "dispute entry" definition gap had not yet been identified. The v2 revisions produced a new consensus:

1. Define "dispute entry" in FR-011 first.
2. Then sync SKILL.md to the updated FR-011.

APM (modified P1-1) accepts the sequencing constraint. gh-aw (N-2) originated it. spec-kit (surviving P1-1) treats the sync as the top priority without contesting the sequencing. All three agents agree that propagating an undefined term into the executable skill definition would compound the ambiguity. The ordering is settled; the dispute-entry definition itself remains contested (Dispute 1 above).

### Convergence 5: Template authoring contract must be scoped to cooperative mode

The v1 disputes did not explicitly address contract scoping. The v2 revisions produced convergence:

- The template authoring contract's variables and invariants are specific to cooperative-mode Phase 5 output.
- Non-cooperative modes produce fundamentally different Phase 5 outputs and would need their own contracts.
- Scoping the contract to cooperative mode is a prerequisite for adding new invariants (per-file attribution, Phase 5 cross-references).

spec-kit (surviving P2-6) originated the recommendation. APM (modified P1-2) accepts it as a prerequisite. gh-aw does not contest it. Applying the scope narrowing and invariant additions simultaneously (spec-kit's resolution of the sequencing concern) is the correct approach. This is settled.

---

## Final Position Statement

gh-aw entered the v2 deliberation with the largest concession count from v1: directory separation withdrawn, template branching withdrawn, three-tier failure model accepted from APM. The v2 round confirmed that these concessions were correct -- no agent relitigated them, and the revised positions built productively on the conceded ground.

The v2 revisions resolved more disputes than they created. The five convergence points above represent genuine progress: the three-tier failure model, content-presence scoping, draft template FR, SKILL.md sequencing, and contract scoping were all open or ambiguous after v1 and are now settled. The remaining three disputes are narrower than the v1 disputes -- they concern specific mechanism choices within agreed-upon frameworks, not the frameworks themselves.

### Positions held

1. **Content-negative dispute-entry definition** (Dispute 1). The trigger mechanism was designed to decouple evaluation from Markdown formatting. APM's `**Dispute:**` pattern requirement re-couples them. Excluding whitespace and HTML comments is sufficient; requiring a specific Markdown pattern defeats the purpose of the structural markers. gh-aw will not support a definition that makes the primary mechanism functionally identical to the fallback.

2. **FR-018 section headings as the only v1 structural requirement on the arbiter** (Dispute 2). Adding labeled sub-field conventions to FR-015 is a softer version of requiring structured output from the LLM. It creates a dependency that downstream tooling will rely on, a degradation path for when the arbiter varies, and a migration burden when the v2 schema inevitably diverges from the v1 prose labels. The correct v1 contract is section headings only. The correct v2 preparation is advisory schema fields in a standalone section.

3. **Heading-presence as the tier 2/3 boundary test** (Dispute 3). APM's "prose parseability" criterion is the right intuition but not a machine-implementable specification. The heading-presence test is a single regex check that any engine can implement deterministically. It correctly classifies the examples all three agents cite (raw YAML: zero headings, tier 2; refusal message: zero headings, tier 2; resolution with missing Confidence Assessment: three headings present, tier 3). gh-aw will not support a boundary definition that requires semantic prose classification.

### Areas of flexibility

1. **Schema field cardinality** (Dispute 2, sub-point). The `affected_target_files` pluralization is correct. gh-aw accepts this regardless of the normative status of the fields.

2. **Success criteria priority** (N-1). gh-aw classified the missing SCs as P2; spec-kit classifies them as P1. gh-aw will not block on priority classification. The SCs should be added; the priority affects sequencing, not substance.

3. **Endorsement-mode specification detail** (modified P2-5). gh-aw's revised position and spec-kit's revised P3-8 are functionally identical -- both specify what the FR-018 sections contain when no disputes exist. The exact wording is negotiable as long as the endorsement path is explicitly documented rather than left as an implicit edge case.

4. **Hybrid enforcement model acknowledgment** (N-3). This is a P3 documentation improvement that no agent contested. gh-aw will accept any wording that makes the engine/author enforcement division explicit in the template authoring contract.

### Net assessment

The v2 deliberation narrowed the dispute surface from architectural disagreements to mechanism-selection disagreements. The three remaining disputes share a common theme: gh-aw favors mechanical, deterministic, minimal-commitment specifications; APM and spec-kit favor richer semantic contracts that provide more guidance at the cost of more assumptions about agent behavior. This is a legitimate design-philosophy tension, not a misunderstanding. The synthesis should resolve each dispute by choosing the mechanism that best serves the spec's stated goal of being implementable across diverse engine architectures, and record the rationale for the chosen approach.
