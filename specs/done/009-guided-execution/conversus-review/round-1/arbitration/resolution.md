# Arbitration Resolution: 009-Guided-Execution

**Arbiter**: conversus-constitution (advisory)
**Spec**: `009-guided-execution`
**Phase**: 6 (Cooperative Arbitration)
**Date**: 2026-03-22
**Authority**: Advisory influence only. These opinions do not override reviewer consensus or implementer judgment.

---

## Advisory Opinions

### Dispute 1: Problem statement inclusion in the pre-execution summary

**Parties**: functional-typing + devils-advocate (include problem statement as part of P1 fix) vs. integration-architect (defer to follow-up)

**Advisory opinion**: The 2-1 majority position is the stronger reading of the spec's own intent.

The spec's Section 1 states that converge "presents a human-readable summary of the config" and Section 3's SC-004 demands plain language ("not a YAML dump"). FR-001 lists specific summary elements, but it does so under the heading "human-readable summary" -- the list is illustrative of the standard, not exhaustive of it. The problem definition is not a peripheral configuration detail comparable to template content or constitution rules. It is the input that determines what every agent writes about. Integration-architect's concern that adding it without addressing other omissions creates an inconsistency in disclosure level is procedurally valid, but the problem statement is categorically different: mode, agents, targets, and launch count are all instrumentalities in service of a problem. Disclosing the instruments without disclosing their purpose is an ordering error, not merely an omission.

Integration-architect's scope objection -- that this is a spec amendment rather than a bug fix -- is the strongest argument against inclusion at P1. The objection is correct in a narrow sense: FR-001 does not enumerate this field. But FR-001's purpose clause (informed consent for non-experts) creates an implicit completeness obligation that the field list does not satisfy on its own. The one-line conditional addition proposed by functional-typing and devils-advocate is proportionate: it reads the first sentence of `problem.md` when present, or displays a fallback for hand-crafted configs. This is less invasive than several converged recommendations (e.g., the "What to Expect" narrative, the failure recovery clause) that also extend the handler beyond what FR-001 literally requires.

**Advisory recommendation**: Apply the label fix at P1 (converged). Treat the problem-statement addition as P2 -- not deferred indefinitely, but sequenced after the label fix. This respects integration-architect's scope concern (it is not smuggled in as part of the label fix) while honoring the majority position that the gap is real and should be closed promptly. If the implementer judges the one-line addition trivial enough to bundle with the label fix, that is a reasonable implementation choice.

---

### Dispute 2: Prior context disclosure priority -- P2 vs. P3

**Parties**: functional-typing + devils-advocate (P2) vs. integration-architect (P3)

**Advisory opinion**: P2 is the more defensible priority, but the practical difference is negligible.

Integration-architect's argument rests on a user-awareness assumption: that prior-file users are sophisticated enough to know what they configured. Devils-advocate correctly identifies the gap in this reasoning -- the person who confirms execution is not necessarily the person who wrote the config. Constraint 2 (converge works with hand-crafted configs) explicitly envisions users running configs they did not create. In that scenario, prior files are the single most impactful undisclosed input: they silently shape every agent's context window.

Integration-architect's slippery-slope argument (if prior files, then templates, then constitutions, then the summary becomes a config dump) does not hold because the current summary already discloses agents, mode, targets, and launch count. Prior files are the only configured input that influences all agents and is absent from the summary. Templates and constitutions are not comparable -- templates structure output format (visible in results), constitutions are meta-rules (visible in the synthesis process description). Prior files inject substantive content that invisibly biases every agent's starting position.

**Advisory recommendation**: P2. The implementation cost is identical at either priority (one conditional line). The information gap is real for the inherited-config scenario. Integration-architect's P3 is not unreasonable, but the 2-1 majority and the stronger analytical argument favor P2.

---

### Dispute 3: Mtime staleness false-positive documentation

**Parties**: devils-advocate (document the limitation) vs. functional-typing and integration-architect (not opposed, not adopted)

**Advisory opinion**: This is a procedural gap, not a substantive disagreement. No reviewer has argued against the addition. It fell through the consolidation process because the reviewers were focused on mechanism changes (withdrawn) and scope reassignment (to spec 008), and the documentation fix was lost in the shuffle.

The proposed addition is one sentence. It addresses a real scenario (git operations updating file timestamps) that the SC-001 non-expert persona will encounter. A false-positive warning on the consent surface -- the one moment the guided flow asks for trust -- is disproportionately damaging to user confidence. The cost-benefit analysis is unambiguous: zero implementation cost, meaningful UX improvement for a known false-positive path.

**Advisory recommendation**: Adopt as P3. The fact that no reviewer opposes it is sufficient basis for inclusion. The synthesizer's final.md already characterizes it as a "procedural gap rather than a substantive disagreement" and recommends adoption. This opinion concurs.

---

### Dispute 4: Important Notes formula correction priority -- P1 vs. P2

**Parties**: integration-architect (P1) vs. functional-typing (P2)

**Advisory opinion**: Both positions are well-reasoned and the fix is identical at either priority. The question reduces to whether SKILL.md internal consistency is a functional concern (integration-architect) or a documentation concern (functional-typing).

Integration-architect's strongest argument is empirical: the arithmetic error demonstrably caused confusion during this review cycle. Devils-advocate's original analysis was led astray by the discrepancy between the Step 4 formula and the Important Notes formula, requiring functional-typing to provide the root cause correction. A document whose internal contradictions actively mislead its own reviewers has a consistency problem that affects more than "documentation users may never read."

Functional-typing's strongest argument is also empirical: no execution path is affected. The converge handler (line 1404) uses the correct formula. Users see the right number. The Important Notes section is a reference appendix, not a user-facing surface.

The tiebreaker is the document's audience. SKILL.md is read by LLM agents executing the conversus pipeline. An agent that references Important Notes during execution planning (which is exactly the use case the section exists for) will compute wrong estimates. This is not a hypothetical -- it is the intended use of the section. An internal contradiction in an instruction document for automated agents is functionally closer to a code bug than a documentation typo.

**Advisory recommendation**: P1, with the caveat that the practical difference from P2 is near-zero since all parties agree the fix will be applied regardless. Integration-architect's reasoning about SKILL.md as a single-document instruction set is the more relevant framing for a document consumed by LLM agents.

---

## Considerations for Next Round

The following observations are offered for the implementer and for future deliberation rounds on this or related specs. They do not override any converged recommendation.

### 1. The consent-surface design question is broader than spec 009

Three of the four disputes (problem-statement inclusion, prior-context disclosure, mtime false-positive documentation) cluster around the same architectural question: what information does the pre-execution summary owe the user? The spec answers this with a field list (FR-001) and a design principle (SC-004: plain language, not YAML dump). The reviewers revealed that these two constraints are in tension -- the field list is too narrow for informed consent, but expanding it risks the YAML-dump failure mode SC-004 prohibits.

A future spec (or an amendment to spec 009) should establish a principled selection criterion for summary fields. One possible criterion: disclose any configured input that (a) influences agent output and (b) is not visible in the results. This would include the problem statement (influences all agents, not directly visible in output structure) and prior files (influences all agents, invisible in results), while excluding templates (visible as output structure) and constitutions (visible as synthesis rules). This criterion would resolve the current disputes and provide a framework for future summary-field decisions as the config schema grows.

### 2. The speckit qualification language is functionally converged

Dispute 3 in integration-architect's disputes (positive authorization vs. negative qualification for speckit integration) is characterized as "closer to convergence than dispute." Both framings achieve the same goal: the speckit suggestion is no longer undocumented behavior. The implementer should choose whichever wording feels more natural. If forced to advise: the negative qualification ("informational and tool-availability-dependent") is safer because it does not create a precedent for adding arbitrary cross-tool suggestions without review. But either is acceptable.

### 3. The formula correction validates the multi-reviewer process

The Important Notes arithmetic error is the clearest demonstration that the cooperative deliberation model works as designed. One reviewer (devils-advocate) identified the symptom. A second (functional-typing) traced the root cause. A third (integration-architect) provided the line-level fix. No single reviewer would have produced the complete diagnosis. This finding should be cited in future process documentation as evidence that the three-reviewer cooperative model catches errors that individual review cannot.

### 4. Priority disputes are a sign of healthy calibration, not dysfunction

All four remaining disputes are about priority or scope, not about diagnosis or fix direction. This is the expected residual of a cooperative process: reviewers with different analytical lenses assign different weights to the same finding. The synthesizer's resolution of these disputes (in final.md) is reasonable and well-argued. Future rounds should treat P-level disagreements as calibration signals rather than failures to converge -- they indicate that the reviewers have different but legitimate perspectives on severity, not that they disagree about what is broken.

### 5. The "no new execution logic" constraint held

All three reviewers independently verified that the converge handler introduces zero new execution logic. This constraint, stated twice in the spec (Section 4, two bullet points), was the highest-risk architectural invariant. Its survival through adversarial review (devils-advocate explicitly tested it) provides strong confidence that the implementation respects the spec's most important boundary. Future specs that establish similar bright-line constraints should expect the same level of scrutiny and should welcome it.

### 6. Staleness detection is a spec-008 responsibility

The unanimous reassignment of staleness mechanism improvements to spec 008 (config generation) rather than spec 009 (config consumption) is an important architectural decision that should be recorded in spec 008's backlog. The specific items to carry forward are: (a) content hashing as a replacement for mtime-based staleness detection, (b) provenance metadata (source file tracking) embedded in the generated config, and (c) extension of staleness checking to cover `problem.md` changes. These were all identified as valuable by this review cycle but correctly scoped out of spec 009.
