# APM v2 Final Disputes: Subject Arbitration (Phase 6)

**Agent**: APM (Agent Package Manager)
**Date**: 2026-03-19
**Phase**: Disputes (post-v2 revision)
**Inputs**: APM v2 revision, spec-kit v2 revision, gh-aw v2 revision

---

## Remaining Disputes

### Dispute 1: "Dispute entry" definition — pattern-match vs. non-comment non-whitespace

**Disputed with**: gh-aw (modified P1-2)

All three agents agree that "dispute entry" must be defined before SKILL.md is synced. The disagreement is over the definition itself.

- **APM (modified P1-1)**: A dispute entry is any line between the markers that matches the `**Dispute:**` pattern, or at minimum any line beginning with a Markdown bold marker (`**`). This keeps the primary trigger mechanism structurally aligned with the heading-based fallback, where `**Dispute:**` entries are the recognized unit.
- **gh-aw (modified P1-2)**: A dispute entry is any line containing non-whitespace content that is not an HTML comment (`<!-- ... -->`). This excludes stray comments and pure whitespace but does not couple the trigger to a specific Markdown formatting convention.
- **spec-kit (modified P1-3)**: Adopts gh-aw's positive-definition framing for `trigger: disputes_remain` but does not take a position on the line-level definition. Defers to the pattern that emerges between APM and gh-aw.

gh-aw's revised definition is better than its original "any non-whitespace" proposal -- excluding HTML comments closes the most obvious false-positive vector. But it remains too permissive. Consider: a Phase 5 template that leaves a stray paragraph of explanatory text between the markers (e.g., "The following disputes were identified during synthesis:") would trigger Phase 6 under gh-aw's definition because the line contains non-whitespace, non-comment content. This is a context-setting preamble, not a dispute entry. The engine would dispatch an expensive LLM arbitration call on content that contains zero actionable disputes.

gh-aw argues that coupling the trigger to the `**Dispute:**` pattern would make the primary mechanism no more capable than the fallback. This conflates two concerns. The primary mechanism's advantage over the fallback is its use of machine-parseable delimiters (HTML markers) rather than fragile heading detection -- that advantage is about *where* to look, not *what* to look for. What constitutes a dispute entry can and should be consistent across both mechanisms. Consistency means that switching from fallback to primary mode does not change the set of documents that trigger Phase 6 -- only the reliability of detection changes.

**APM's position**: Define "dispute entry" as any line between the markers that begins with `**Dispute:**` or `**Dispute` (allowing for minor formatting variations like bold text without the colon). This is strict enough to prevent false positives from preamble text, template artifacts, and non-dispute content, while loose enough to tolerate minor formatting variation from the Phase 5 agent. If the Phase 5 template is correctly authored, every dispute entry will begin with this pattern. If it does not, the fallback mechanism (heading-based parsing) provides the safety net.

---

### Dispute 2: Structured output schema — normative-advisory hybrid vs. prose conventions as v1 contract

**Disputed with**: spec-kit (modified P2-4)

This is the sharpest three-way evolution across both rounds. The positions have converged significantly but a real disagreement remains on the v1 contract.

- **APM (N-1)**: Endorse spec-kit's normative schema fields with the `affected_target_files` pluralization fix. The schema fields are normatively committed via an FR. The prose template remains free-form. The schema is the v2 commitment; the mechanism is deferred.
- **spec-kit (modified P2-4)**: Withdraws the normative FR. Adopts a hybrid: prose conventions (`**Dispute:**`, `**Ruling:**`, etc.) as the v1 contract in FR-015, and advisory schema fields in a dedicated "Deferred: Structured Output" section. Two separate sources of truth, one per version.
- **gh-aw (modified P3-8)**: Standalone "Deferred: Structured Output" section with SHOULD-level language. No normative commitment. No prose conventions.

Spec-kit's revised position is a surprise reversal. In v1 disputes, spec-kit held firm that the schema must be normatively specified regardless of mechanism. In v2, spec-kit withdraws the normative FR and instead adopts APM's prose conventions (the very approach spec-kit's own cross-review DC-1 called "the more dangerous of the two positions because it looks like compliance while reducing the commitment"). APM conceded P1-3 (prose conventions) in its revision because both cross-reviewers identified it as premature commitment conflicting with deferred structured output. Now spec-kit adopts that same withdrawn recommendation as its v1 contract.

The contradiction is procedural: APM withdrew prose conventions because the cross-reviews were persuasive. Spec-kit adopts prose conventions after its own cross-review argued against them. These two moves cannot both be correct.

**APM's position**: The v1 contract should be *neither* normative schema fields *nor* prose conventions. The v1 contract is FR-018's section headings, validated by FR-023's heading-presence check. That is the structural commitment the spec already makes. Adding prose conventions (spec-kit's position) or advisory schema fields (gh-aw's position) on top of that are both forward-looking commitments that should live in a clearly deferred section with no normative weight in v1. For v2 planning, APM endorses a dedicated "Deferred: Structured Output" section using SHOULD-level language (gh-aw's organizational recommendation) with the corrected field list including `affected_target_files`. The prose conventions and the schema fields should converge in v2 design, informed by real arbiter output, not diverge into separate v1 and v2 contracts that may conflict. gh-aw's "design after observing real output" principle is the right sequencing for extraction; APM's cardinality fix (`affected_target_files`) ensures the advisory schema does not bake in a known-wrong assumption while it waits.

---

### Dispute 3: Citation boundary enforcement — spec-level FR vs. template-level instruction

**Disputed with**: gh-aw (surviving P2-4)

- **APM (implicit in Alignment 2, explicit in revision)**: FR-024 is normatively sufficient. The engine validates output per FR-023. The template inherits the constraint from the FR without needing to restate it.
- **gh-aw (surviving P2-4)**: FR-024 in the spec is not FR-024 in the template. The arbiter only sees its prompt. If the citation boundary is not in the template instructions, the arbiter cannot follow a rule it does not know about. FR-023 only validates section heading presence, not citation sourcing, so there is no post-hoc enforcement either.

gh-aw's argument has a true premise and a false conclusion. The true premise: the arbiter only sees its prompt, so any rule it must follow should appear in its instructions. The false conclusion: therefore the template must restate every relevant FR. If this logic holds, the template must also restate FR-015.5 (no new recommendations), FR-026 (per-file attribution), FR-025 (grounding singularity), and every other FR that constrains the arbiter's output. The template would become a restatement of the spec, which defeats the purpose of separating normative requirements from template instructions.

The correct architecture is: the template instructs the arbiter on *what to produce* (sections, structure, reasoning approach). The FRs constrain *what is acceptable* (output validation, citation rules, scope limits). The engine enforces the FRs against the output. The template does not need to enumerate every constraint the engine will check.

gh-aw's specific concern -- that FR-023 does not validate citation sourcing -- is valid but misdiagnosed. The fix is to extend FR-023's validation scope (or add a new validation FR for citation-source checking), not to push enforcement into the template. Template-level instructions are unenforceable: the arbiter can be told "do not cite docs as sole authority" and still do it, with no automated detection. An engine-level check that flags `docs`-only citations in Binding Decisions is both enforceable and auditable.

**APM's position**: Do not add citation boundary instructions to the template. Instead, note in FR-024 that future versions SHOULD add engine-level validation for citation-source compliance. This keeps the enforcement architecture clean (engine validates, template instructs) while acknowledging the current gap. The current gap is acceptable for v1 because the arbiter's grounding document is the primary input and the template already instructs the arbiter to derive rulings from it -- the risk of `docs`-only citations is low when the grounding document is the dominant context.

---

## Convergence

### 1. Three-tier failure model for FR-022/FR-023

All three agents converge on APM's three-tier disambiguation. APM proposed it (N-3). gh-aw adopted it explicitly in its revision (modified P1-1), including APM's "garbage in 200 OK" framing. Spec-kit endorsed gh-aw's original disambiguation (N-1) and the three-tier extension is compatible with spec-kit's endorsed sentence. The bright-line test is unanimous: does the output contain at least one FR-018 section heading? If yes, tier 3 (write with warning). If no, tier 2 (no file written, diagnostic). Process failure (no output at all) is tier 1. This is settled.

### 2. SKILL.md sync sequenced after dispute-entry definition

All three agents agree on the sequencing constraint. APM identified the drift (P1-1). gh-aw identified the sequencing dependency (N-2): define "dispute entry" first, then sync SKILL.md. Spec-kit's revision treats the SKILL.md fix as the highest-priority convergence point. The definition of "dispute entry" remains disputed (Dispute 1 above), but the sequencing -- define first, then sync -- is unanimous.

### 3. Content-presence guard scoped to `trigger: disputes_remain` only

All three agents converge on scoping the whitespace guard. APM proposed it (N-5). Spec-kit adopted the scoping in its modified P1-3. gh-aw's diagnostic-warning approach for `trigger: always` with empty content is compatible. The consensus: for `trigger: disputes_remain`, empty markers mean the trigger evaluates to `false`. For `trigger: always`, the trigger fires regardless, with a diagnostic if `{REMAINING_DISPUTES}` extraction is empty. The endorsement path (US1-AS3) is preserved.

### 4. Draft template filtering as a normative FR

All three agents agree. APM endorsed it (N-4). gh-aw proposed it (P2-3). Spec-kit endorsed it (N-2). The engine MUST NOT dispatch templates containing the draft marker. The only question is FR numbering (avoiding collision with other proposed FRs), which is an editorial concern, not a design disagreement. gh-aw's withdrawn directory-separation preference (OB-1) removes the last obstacle: the marker mechanism is the agreed approach, and it now has a testable FR behind it.

### 5. Template authoring contract scoped to cooperative mode with per-file attribution

APM and spec-kit converge on the combined fix: scope the contract to cooperative mode (spec-kit P2-6), then add per-file attribution as an invariant within that scope (APM P1-2, spec-kit N-3). gh-aw's revision does not contest either change. The sequencing concern APM raised (DC-3 in its cross-review of spec-kit) dissolves when both changes land simultaneously, as spec-kit's revision notes. The contract becomes: "For cooperative-mode templates, authors MUST preserve these invariants: [existing four] + per-file attribution per FR-026."

---

## Final Position Statement

### Positions Held

1. **Dispute-entry definition must be pattern-based, not permissive.** The `**Dispute:**` pattern (or `**Dispute` with formatting tolerance) is the right definition because it prevents false-positive triggers from preamble text, template artifacts, and non-dispute content between markers. gh-aw's HTML-comment exclusion is a necessary but insufficient filter. The primary trigger mechanism's advantage is *where* it looks (machine-parseable markers), not *what* it accepts (any non-comment text). The *what* should be consistent across primary and fallback mechanisms. APM will advocate for pattern-based matching but will accept gh-aw's non-comment definition if the arbiter (synthesis phase) determines that template artifact risk is adequately mitigated by Phase 5 template quality.

2. **The v1 structured output contract is FR-018 section headings, nothing more.** Neither prose conventions nor advisory schema fields should carry normative weight in v1. Both belong in a "Deferred: Structured Output" section for v2 planning. Spec-kit's reversal -- withdrawing the normative schema FR and adopting the prose conventions APM itself withdrew -- creates an internally inconsistent position. The clean answer is: v1 validates headings (FR-023), v2 designs extraction informed by real output. APM will accept gh-aw's SHOULD-level advisory schema in the deferred section with the `affected_target_files` pluralization fix.

3. **Citation boundary enforcement belongs in the engine, not the template.** Adding FR-024's citation rule to template instructions creates a precedent where every FR that constrains arbiter output must be restated in the template. The correct architecture separates instructional content (template) from validation rules (engine). The current gap (no citation-source validation in FR-023) should be noted as a future enhancement, not patched by template duplication.

### Positions Yielded

1. **Three-tier failure model**: APM proposed it; both agents adopted it. No further advocacy needed.

2. **Success criteria for post-conversus FRs**: APM conceded this was a material gap. Spec-kit's identification was correct. The SCs should be added as specified in APM's N-2.

3. **Grounding document stability**: APM accepts this belongs in engine implementation, not in spec normative text. Withdrawn entirely.

4. **Observation carve-out rationale**: APM concedes FR-015.5's audit trail is incomplete and endorses narrowed rationale documentation (spec-kit's modified P2-5, scoped to the observation carve-out only).

5. **Prose structure conventions**: APM's original P1-3 was correctly identified as premature commitment by both cross-reviewers. Withdrawn and not re-adopted despite spec-kit's N-4 attempting to resurrect it. The withdrawal stands.

### Areas of Flexibility

1. **Endorsement path specification**: APM supports spec-kit's modified P3-8 (explicit endorsement-mode behavior in FR-015) and gh-aw's modified P2-5 (contract annotation). Either approach is acceptable -- the key requirement is that `trigger: always` with empty disputes is documented as a legitimate path producing endorsement output, not treated as a degenerate edge case.

2. **Success criteria priority**: APM classified this as P1 (N-2). gh-aw classifies it as P2 (N-1). APM is flexible on priority classification -- the SCs should be added regardless.

3. **Hybrid enforcement model acknowledgment**: gh-aw's N-3 (acknowledge the engine-level vs. author-level enforcement split in the template authoring contract) is a sensible documentation improvement. APM supports it without strong feelings on priority.

4. **Validation-error on unknown trigger values**: APM narrowed this from extensibility framing to validation hardening (modified P2-5, downgraded to P3). If the synthesis deems it too minor for v1, APM will not contest deferral.
