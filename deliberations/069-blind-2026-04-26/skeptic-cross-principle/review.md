# Skeptic Cross-Principle Review: Constitutional Inclusion Criteria Gate

## Executive Summary

The Constitutional Inclusion Criteria gate (in **Governance**) imposes three tests on amendments — *mechanical verification capability*, *falsifiable scope*, and *distinct from existing principles* — and grandfathers Principles I-XXVII. Read against the existing constitution, the gate is **structurally inconsistent with its own corpus**: at least four grandfathered principles (VI Scripts Over Markdown, X Zen of Python Output, XVI Mathematical Transparency, and arguably XX Decomposition Mechanism Precedence and XXI Extraction Ordering) would be **rejected** if proposed today. This produces a two-tier constitution — pre-gate principles permitted to be vague or judgment-dependent, post-gate amendments held to a stricter bar — which itself violates the gate's spirit (Principle II Stable Interfaces, Principle XI Single Source of Truth).

The gate's third criterion ("distinct from existing principles") is also a **redundant double-anchor with Principle XI**: XI already governs information-duplication, and the amendment process already requires rationale. The gate's first criterion ("mechanical verification capability") is genuinely new and load-bearing — it codifies the lint-or-it-doesn't-count discipline implicit across XII, XIII, XXII, XXIV, XXVI. The second criterion ("falsifiable scope") is partially redundant with the constitution's existing MUST/SHOULD discipline but adds a useful precision: it forbids principles whose violation requires interpretation.

**Net assessment**: the gate is more useful as a **single-criterion check** (mechanical verification capability) than as a three-criterion test. Criterion 3 should be merged into XI's body (or deleted). Criterion 2 should be merged into the amendment process description (or deleted). The grandfather clause should be **time-boxed** with a migration audit, not left open-ended — otherwise it becomes a permanent inconsistency the constitution explicitly tolerates, which is itself an antipattern.

## Alignment

1. **Gate criterion 1 (mechanical verification) ↔ Principles XII, XIII, XXII §1, XXIV §3, XXVI**: This alignment is the gate's strongest justification. XII (No Dead Infrastructure) requires linter checks, XIII (Enum Completeness) requires grep-for-string-literals tests, XXII §1 requires single-source version checks, XXIV §3 requires reproducer tests, XXVI requires meta-tests for parametrized capability sets. The gate codifies a property that already runs through five principles: a constitutional rule that cannot be checked is operationally indistinguishable from an aspiration. The gate makes this implicit pattern explicit and prospective.

2. **Gate criterion 2 (falsifiable scope) ↔ Principle II (Stable Interfaces)**: II already enumerates *which* interfaces are stable with concrete artifacts (markers, dispatch table names, schema paths). It is the constitution's exemplar of falsifiable scope — a reviewer can mechanically check whether a PR renames a marker. The gate's criterion 2 generalizes this precision requirement to all amendments. This is reinforcing rather than redundant: II demonstrates the standard, the gate makes it normative.

3. **Gate criterion 3 (distinct from existing) ↔ Principle XI (Single Source of Truth)**: XI explicitly states "If you find yourself writing the same fact in two places, stop. One of them is wrong, or will be soon." The gate's criterion 3 applies this to constitutional principles themselves. The principle-of-the-principle is consistent — but as analyzed in Missed Opportunities §1, this is a **redundant double-anchor** rather than productive reinforcement: the gate restates XI's content within the amendment process, creating exactly the duplication XI prohibits.

4. **Grandfathering carve-out ↔ Principle III (Backward-Compatible Extension)**: III mandates that new features extend rather than restructure. The grandfather clause applies III to the constitution itself — adding a gate without retroactively invalidating I-XXVII. This is consistent and well-founded.

5. **Gate's "operational guidance" target ↔ Principle XVII (Content Classification)**: XVII distinguishes execution logic (SKILL.md, references) from contribution guidelines (AGENTS.md). The gate adds a third tier — *constitutional invariants* vs *operational guidance* (CONTRIBUTING.md, specs, SKILL.md, reference docs). This extends XVII's classification discipline upward. Productive alignment, but the gate does not cite XVII, missing an opportunity to anchor the new tier in existing taxonomy.

6. **Gate ↔ Principle XIV (Spec-Implementation Parity)**: XIV requires specs and implementations to agree. The gate analogously requires principles and verification mechanisms to agree (mechanical check must be sketchable). Both prevent drift between *stated rule* and *enforceable rule*. This alignment should be made explicit — the gate's criterion 1 is essentially "constitutional-implementation parity."

## Missed Opportunities

1. **Gate criterion 3 vs. Principle XI overlap is unresolved.** The "distinct from existing principles" criterion is XI applied to the corpus of principles. The gate does not cite XI. A reviewer cannot tell whether this is intentional reinforcement, redundant double-anchor, or accidental duplication. Per XI's own rule ("if you find yourself writing the same fact in two places, stop"), the gate triggers an XI violation against itself. Either: (a) merge criterion 3 into XI's body as an explicit extension ("Principle XI applies recursively to the principles list"), or (b) delete criterion 3 and let XI govern transitively.

2. **Principle XVI (Mathematical Transparency) likely fails the gate.** XVI requires "plain-language explanations alongside numerical outputs." Mechanical verification: how would a CI check determine whether an explanation is *plain-language*? The path-to-check is not concrete — it requires human judgment on prose quality. Falsifiable scope: a reviewer easily reasons "well, X explanation might be plain enough if Y." If XVI were proposed today, the gate would reject it. The constitution does not address this dissonance. Either XVI needs a verification mechanism (e.g., presence-of-explanation-field check, even if quality is unverifiable), or the grandfather is doing more work than acknowledged.

3. **Principle VI (Scripts Over Markdown) and X (Zen of Python Output) are the most flagrant grandfather beneficiaries.** VI's "prefer executable scripts" is judgment-laden ("when the artifact drives behavior"). X's "if the implementation is hard to explain, it's a bad idea" is irreducibly subjective. Both fail criterion 2 (falsifiable scope) head-on. The gate's prospective-only design means VI and X persist as constitutional rules forever, despite failing the gate. This is either: (a) a permanent two-tier system, or (b) an implicit migration backlog. The constitution should pick one and say so.

4. **Principle XX (Decomposition Mechanism Precedence) and XXI (Extraction Ordering) are workflow heuristics, not invariants.** Both read as *guidance* rather than *contracts*: "prefer references/ over APM sub-skills," "extract handlers in order of independence." Mechanical verification: there is no PR-fails check for "you should have preferred references/." These belong in operational guidance per the gate's own logic. The grandfather preserves them, but their presence dilutes the constitution's invariant-only character.

5. **The "concrete enough to sketch in one paragraph" bar in criterion 1 is itself unverifiable.** Who decides whether the sketch is concrete enough? The gate requires mechanical verification of amendments but installs a human-judgment gate to evaluate amendments. This is a recursion the gate does not address. A reviewer applying the gate to the gate would find criterion 1 fails its own falsifiable-scope test. Recommend: replace "concrete enough" with a structural requirement — e.g., "amendment MUST include a `Verification:` field naming the check type (lint, parity test, structural assertion, schema validation) and the artifact it would inspect."

6. **No interaction is specified with the Antipatterns catalog.** Known Antipatterns (above Governance) is the existing channel for "rules of thumb that we keep tripping on." The gate names "operational guidance" as the destination for failing principles but does not mention the antipattern catalog as one such venue. Migrating VI, X, XVI, XX, XXI to the catalog would be a natural fit (each was learned from a recurring failure). The gate misses this.

7. **The grandfather clause has no expiry or audit trigger.** "Migrating any of them to operational guidance is a separate, intentional act" leaves the migration as latent intent forever. Compare: XXII §1 (single-source versioning) does not say "version drift is permitted on existing surfaces, fix it eventually" — it requires single-source now. The gate should either: (a) require a constitutional audit by a target version (e.g., v3.0.0 audits I-XXVII against the gate), or (b) explicitly accept permanent inconsistency.

8. **Interaction with versioning rules is unclear.** Governance says "MAJOR for principle removals or redefinitions, MINOR for new principles." The gate says principles failing the criteria belong in operational guidance. If an existing principle is migrated *out* of the constitution to CONTRIBUTING.md, is that MAJOR (removal) or PATCH (clarification of where the rule lives)? The gate is silent. This will produce inconsistent versioning when migrations begin.

9. **The gate does not address principle *expansion* via Extension blocks.** Several principles (IX v2.3.0 behavior-over-shape, XI v2.3.0 registry-first, XV v2.3.1 registry interface) carry "Extension" subsections added in later versions. Do extensions go through the gate? They add new requirements — arguably new principles in disguise. The gate's prospective scope is ambiguous about whether extensions count as "amendments landing once the gate is in force."

## Off-Base Assumptions

1. **The gate assumes constitutional principles and operational guidance are cleanly separable.** In practice, runtime-enforced contracts (per XVII) often *should* be in both — the constitution states the invariant, SKILL.md/references state the runtime check, AGENTS.md restates it for contributor visibility. The gate's "belongs in operational guidance" framing implies a single home. This conflicts with XVII's classification, where the same rule legitimately appears in multiple surfaces with derivation, not duplication.

2. **The gate assumes prospective-only application is stable.** Two-tier constitutions are unstable: as principles I-XXVII are amended, each amendment must navigate the gate, which means the gate is partially retroactive (any extension to a grandfathered principle gets gated). Eventually most principles will have at least one gated extension, creating mixed-tier principles whose old body and new body are held to different standards. This is not addressed.

3. **The gate assumes "mechanical verification capability" is a binary property.** In practice, verification is on a spectrum: schema validation (cheapest), parity tests (cheap), lint rules (moderate), structural assertions (variable), behavioral tests (expensive), human review (uncheckable). The gate treats "feasible to sketch in one paragraph" as the line. But X (Zen of Python Output) could be sketched as "lint that rejects nested directories deeper than 2 levels" — the sketch is concrete, the check is partial. The gate provides no rule for partial verifiability.

4. **The gate assumes the amendment process catches violations.** No mechanism is specified for *applying* the gate. Who runs the gate during `/speckit.constitution`? Is it self-attestation by the amendment author? A required reviewer checklist? A CI lint on `CONSTITUTION.md` diffs? Without an enforcement path, the gate is itself unverifiable — failing its own criterion 1.

## Actionable Recommendations

1. **Merge gate criterion 3 into Principle XI.** Add to XI's body: "This principle applies to the constitution itself: a new principle that restates an existing principle in different words is a duplication, not a new constraint. Refinements belong in the existing principle's body." Delete criterion 3 from the gate. (Rationale: eliminates the double-anchor flagged in Alignment §3 and Missed Opportunities §1.)

2. **Tighten criterion 1 to a structural requirement.** Replace "concrete enough to sketch in one paragraph" with: "Every amendment MUST include a `Verification:` block naming (a) the check type from {schema validation, parity test, lint rule, structural assertion, contract test}, (b) the artifact the check inspects (file, AST, output structure), (c) the failure signal (CI red, deserialization error, etc.). The check need not be implemented at amendment time, but the block MUST be sufficient for any engineer to implement it." (Rationale: removes the "concrete enough" judgment-recursion from Missed Opportunities §5.)

3. **Demote criterion 2 (falsifiable scope) into the amendment process description.** "Falsifiability" is already implicit in MUST/SHOULD discipline and exemplified by Principle II. State once in Governance: "Amendments MUST use MUST/SHOULD/MAY language and MUST be specific enough that a hypothetical PR can be flagged as violating without interpretation." This is one sentence in the amendment process, not a standalone criterion. (Rationale: removes redundancy with II while preserving the precision requirement.)

4. **Time-box the grandfather clause.** Add: "By v3.0.0, an audit MUST evaluate Principles I-XXVII against the gate. Principles that fail MUST either (a) gain a verification mechanism, (b) be migrated to operational guidance with an explicit migration spec, or (c) be retained with a documented permanent exception listing the failing criteria." Without this, the grandfather is a permanent inconsistency.

5. **Identify the migration candidates explicitly.** The audit should pre-flag VI (Scripts Over Markdown), X (Zen of Python Output), XVI (Mathematical Transparency, plain-language explanation requirement only), XX (Decomposition Mechanism Precedence), and XXI (Extraction Ordering) as known gate-failures. Calling these out now prevents litigating each one separately later.

6. **Specify the gate's enforcement path.** Add to Governance: "The Constitutional Inclusion Criteria are checked during `/speckit.constitution` execution. The amendment author MUST include the `Verification:` block (criterion 1) and an `Existing-Principle-Distinctness:` block (citing which principles were considered for extension and why a new principle is warranted). The receiving reviewer MUST confirm both blocks are present and load-bearing before approval." (Rationale: addresses Off-Base Assumption §4.)

7. **Clarify versioning for migrations.** Add to versioning rules: "Migrating an existing principle to operational guidance is MAJOR (removal from the constitutional set). Adding a verification mechanism to a grandfathered principle without changing its body is PATCH. Adding an Extension block to an existing principle is MINOR." This resolves Missed Opportunities §8.

8. **Address Extension blocks explicitly.** Add: "Extension blocks within existing principles ARE amendments and MUST satisfy the gate's verification requirement. If an extension introduces a new requirement that fails the gate, it belongs in a new principle (subject to all three criteria) or in operational guidance, not as an extension to a grandfathered principle." (Rationale: addresses Missed Opportunities §9.)

9. **Cross-reference the antipatterns catalog.** Add to "operational guidance" enumeration: "The antipatterns catalog (`antipatterns/catalog.md`) is the appropriate destination for principles that fail the gate when their content is a recurring failure pattern observed in practice." This integrates the gate with the catalog discipline already established. (Rationale: addresses Missed Opportunities §6.)

10. **Alternative: remove the gate entirely and rely on Principle XI + amendment-process discipline.** If recommendations 1-3 fully eliminate criteria 2 and 3, only criterion 1 (mechanical verification) survives — and this could be folded into Principle XII's body as an extension: "When introducing a new constitutional principle or extension, declare its verification mechanism per Principle XII (No Dead Infrastructure). A constitutional rule with no verification mechanism is dead infrastructure." This eliminates the gate as a separate construct and reuses an existing principle. **This is the strongest skeptic-position recommendation**: the gate is a redundant container for a single useful idea (mechanical verification) that already belongs to XII.

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-blind-2026-04-26/CONSTITUTION-v2.4.0-blind.md` — target constitution, lines 800-848 (Governance, Constitutional Inclusion Criteria, grandfather clause)
- Principle II (lines 18-41) — exemplar of falsifiable scope
- Principle VI (lines 85-98) — gate-failure candidate (judgment-laden)
- Principle X (lines 217-235) — gate-failure candidate (irreducibly subjective)
- Principle XI (lines 237-281) — overlaps with gate criterion 3
- Principle XII (lines 283-305) — natural home for absorbed gate criterion 1
- Principle XIV (lines 329-352) — spec-implementation parity, analogous to constitution-verification parity
- Principle XVI (lines 387-417) — gate-failure candidate (plain-language explanation requirement)
- Principle XVII (lines 419-447) — content classification taxonomy missed by gate
- Principle XX (lines 507-534) — workflow heuristic, gate-failure candidate
- Principle XXI (lines 536-564) — workflow heuristic, gate-failure candidate
- Principle XXII (lines 566-593) — exemplar of mechanically verifiable principle
- Principle XXIV (lines 626-655) — exemplar of three-layer mechanical verification
- Principle XXVI (lines 702-728) — exemplar of meta-test verification mechanism
- Known Antipatterns section (lines 785-798) — missing destination for migrated principles
