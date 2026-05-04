### Recommendation Dispositions

#### Recommendation 1: Annotate XVI's grandfathering entry with partial-upgrade status

- **Original position**: Insert a "Partial upgrade (v2.3.2)" annotation into the grandfathering disclosure recording that XVI's determinism-scope content satisfies Criterion 1 by the same standard as Principle XXIV; the plain-language clause remains a Criterion 2 failure.
- **Disposition**: Modified
- **Explanation**: Two cross-reviews challenged the framing without undermining the core need.

  CVXD's dangerous contradiction analysis ("XVI pre-refactor gate compliance," CVXD cross-review of CPC) established that the pre-cycle-1 XVI body contained three numbered falsifiable rules — parameter pinning on `fill()` return, `objective.yml` persistence with no re-resolution within a run, cross-run shape invariance — that individually satisfied Criterion 2 before the cycle-1 refactor. This means the annotation cannot simply say "v2.3.2 upgraded XVI"; it must also record that XVI's compliance history predates v2.3.2. My original annotation text was chronologically incomplete.

  GF's tension analysis ("Locus of XVI's mixed-status documentation," GF cross-review of CPC) correctly identified that the grandfathering disclosure and the migration SIR serve different audiences and neither alone is sufficient. The disclosure annotation is discovery-time context; the SIR clause map is amendment-time audit trail. My recommendation addressed only the disclosure side.

  **Modified recommendation**: The grandfathering disclosure entry for XVI should carry a composite annotation reading: "*Compliance history:* (a) The pre-cycle-1 body's three numbered rules (parameter pinning on fill() return, no re-resolution within a run, cross-run shape invariance) satisfied Criterion 2 independently — the cycle-1 headline refactor was a defensive improvement, not a gate-required correction. (b) The v2.3.2 extension further strengthened Criterion 1 via SourceProvenance.filled_by, the XXIV enforcement cross-reference, and the explicit falsification clause. (c) Current mixed status: the determinism-scope content (items a + b) passes Criterion 1 by the same standard as Principle XXIV's contract test requirement; the plain-language explanation clause (third bullet, first paragraph) fails Criterion 2. Migration, if any, MUST target only the plain-language clause." The v3.0.0 SIR must additionally carry a clause-by-clause retention/migration map cross-referenced from the disclosure entry.

#### Recommendation 2: Apply Principle XVII taxonomy to VI migration routing

- **Original position**: Split VI's content along the XVII taxonomy before migration — execution-logic sub-bullets to SKILL.md, contribution-guideline sub-bullets to CONTRIBUTING.md.
- **Disposition**: Modified
- **Explanation**: CVXD's dangerous contradiction analysis ("VI disposition: Constitutional retention versus XVII-routed migration," CVXD cross-review of CPC) correctly identified that my recommendation presupposes migration as having occurred and focuses on routing quality, while CVXD's primary claim is that migration was incorrectly decided. These are different questions and I conflated them by operating entirely within the migration frame.

  My role is cross-principle coherence, not migration adjudication. The XVII routing finding is valid and important independent of whether migration was correctly decided — it establishes that IF VI is migrated, routing execution-logic sub-bullets to CONTRIBUTING.md is an XVII violation that silently removes runtime-enforced constraints from the document agents actually read.

  GF's cross-review endorsed this finding and explicitly stated "gate-faithfulness should yield on destination: the load-trigger lint belongs in SKILL.md references or a runtime-consumed reference file, not CONTRIBUTING.md" (GF cross-review of CPC, Dangerous Contradiction 2).

  However, CVXD's primary disposition argument (retention on Criterion 2 parity grounds) remains contested. My cross-review of CVXD noted this as a dangerous contradiction requiring primary-frame selection, and I should not resolve that from within my audit role.

  **Modified recommendation**: The XVII-taxonomy routing split is a mandatory constraint on any VI migration, conditional on migration being confirmed: IF VI migration is confirmed by the synthesis, the v3.0.0 SIR MUST include a XVII-classification table for each VI sub-bullet and MUST route execution-logic sub-bullets (SKILL.md-directed orchestration logic, YAML configuration requirements) to a runtime-consumed reference file, NOT CONTRIBUTING.md. CONTRIBUTING.md is the correct destination only for the format-choice guidance ("when markdown is appropriate") that does not constitute runtime enforcement. The unconditional form of this recommendation overreaches my audit mandate; the conditional form is the correct scope.

#### Recommendation 3: Delete X's error-handling sub-bullet rather than migrate it

- **Original position**: X's third bullet ("Errors should never pass silently — warnings are emitted for malformed output, missing documents, and edge cases") is substantively identical to V's third bullet; deleting it from X's migration payload prevents an XI violation.
- **Disposition**: Modified
- **Explanation**: CVXD's tensions section ("X's sub-bullet 3 and Principle V," CVXD cross-review of CPC) identified that X's bullet 3 is not simply identical to V's — X adds "missing documents" and "edge cases" as categories V does not enumerate. V says "emits warnings for malformed output but does NOT block file writes." X says "warnings are emitted for malformed output, missing documents, and edge cases." X's third bullet is a specialization of V, not a duplicate. The XI violation I identified dissolves once the scope difference is recognized.

  This was a genuine error in my original analysis. I read "substantively identical" where the texts are substantively distinct.

  However, the XVII routing concern is independent and remains valid: X's third bullet is a runtime enforcement rule ("errors should never pass silently" governs what the agent runtime emits, not what contributors should write). Routing it to docs/output-conventions.md routes execution logic to a contribution-guideline document, an XVII violation regardless of whether it duplicates V.

  **Modified recommendation**: Do NOT delete X's error-handling sub-bullet — the bullet has distinct scope (adding "missing documents" and "edge cases" beyond V) and deletion would lose that coverage. If X is migrated, this sub-bullet MUST go to a runtime-consumed document (SKILL.md/references or equivalent execution-logic destination), NOT docs/output-conventions.md. The XI deletion rationale was wrong; the XVII routing concern stands and now applies with greater force because the specialization means the content cannot be retrieved from V if it is stranded in the wrong document.

#### Recommendation 4: Add a passing borderline worked example to the gate text

- **Original position**: Add a third worked example to the gate text — one that illustrates a principle that narrowly passes, citing Principle XXVIII's SIR as the positive anchor.
- **Disposition**: Surviving
- **Explanation**: Neither GF's nor CVXD's cross-reviews challenged this recommendation. GF's tension analysis ("Gate's worked examples: calibration sufficiency vs. asymmetry risk," GF cross-review of CPC) noted that GF "accepts the existing calibration as adequate" while acknowledging the cross-principle-coherence concern about asymmetric calibration, without arguing against adding the example.

  The safe agreement between GF and my review ("Gate calibration is incomplete," GF/CPC cross-reviews of each other) confirms the shared diagnosis: two failure examples without a passing-borderline anchor creates asymmetric calibration that risks over-migration of borderline-compliant principles. The XXVIII SIR's "acknowledged residual = override-with-rationale" precedent is exactly the kind of borderline-pass case the gate currently cannot calibrate against.

  CVXD's independent calibration-gap finding ("Criterion 2 evaluation scope," CVXD Rec 8) identified a related structural gap — the gate's Criterion 2 language could be misread as headline-only evaluation. Both gaps trace to the same root: the gate's calibration instruments are failure-anchored, which makes borderline cases drift toward over-migration. Adding a passing example addresses the vertical gap; clarifying headline-plus-body evaluation addresses the structural gap. The two fixes are complementary, not competing.

#### Recommendation 5: Clarify that XVI is substantively distinct from VII and VIII

- **Original position**: Add to the XVI grandfathering entry that XVI passes Criterion 3 and must not be merged into VII or VIII's body during migration — the VII bilateral carve-out is structural evidence of complementary-but-distinct relationship.
- **Disposition**: Surviving
- **Explanation**: GF's tension analysis ("Asymmetry documentation focus," GF cross-review of CPC) confirmed this recommendation but identified it as addressing a different asymmetry problem than GF's own focus (VI/IX/XV/XXIV comparison). GF said: "These surface orthogonal asymmetry problems... Both are load-bearing for different failure modes." This is convergence, not challenge.

  CVXD did not directly address this recommendation in their cross-review of my work.

  The XVI/VII/VIII distinctness finding is structurally grounded: the bilateral carve-out language in Principle VII first bullet ("narrowed by Principle XVI for LLM gap-filling output") is evidence of two principles that scope each other rather than composing — composable principles reduce to one authoritative source, complementary principles maintain bilateral cross-references. A merged XVI/VII principle would require VII's first bullet to reference its own body, which is incoherent. This reasoning holds regardless of what happens to VI or X, and regardless of whether XVI's plain-language clause migrates.

  One additive finding from GF's cross-review: the synthesis requires TWO separate asymmetry sections in the v3.0.0 SIR — XVI/VII/VIII distinctness (this recommendation) and VI/IX/XV/XXIV comparison (GF's Rec 5). I am recording the second as a new recommendation below because my original review did not propose it.

#### Recommendation 6: Distinguish VI's Criterion 1 and Criterion 2 failure modes

- **Original position**: Update VI's grandfathering entry to reflect that Criterion 1 status is borderline (bounded check feasible for known consumer list) and Criterion 2 status is the definitive failure (judgment required for novel artifact types not in the bounded list).
- **Disposition**: Modified
- **Explanation**: GF's tension analysis ("VI Criterion failure degree," GF cross-review of CPC) agreed on the core distinction but provided a more precise framing for the SIR: "Criterion 2 is the definitive failure (scope-qualifier failure, not tightenable without restructuring the principle); Criterion 1 is borderline (a bounded check is feasible for the known consumer list but not for the principle's stated scope of 'any artifact consumed by automation')." This framing is more actionable than my original because it specifies why Criterion 2 is decisive (tightening would require restructuring, not just narrowing) and why Criterion 1 is borderline but not decisive (the principle's stated scope exceeds the bounded-list check even if the bounded-list check works within its limits).

  CVXD's dangerous contradiction analysis (#2 in CVXD cross-review of CPC) challenged the failure-mode characterization differently — CVXD argues VI's "'drives behavior' qualifier resolves to directory membership" and therefore clearly passes Criterion 1. I do not concede this. Directory-membership is a valid partial check for the known consumer list, but VI's stated predicate — "consumed by automation or agents to make decisions" — applies to any artifact, not just those in the known directories. A novel artifact type not in the enumerated list cannot be evaluated by the directory check. The bounded check is a Criterion 1 partial-pass, not a full pass. CVXD's Criterion 1 argument proves too much: a principle whose predicate is "any X in directory D or directory E" passes Criterion 1; VI's predicate is "any artifact that drives behavior," which is wider than that.

  **Modified recommendation**: Update VI's grandfathering entry to: "Criterion 2 status: FAIL (decisive). The scope-qualifier 'when the artifact drives behavior' requires judgment for artifact types outside the known consumer list; tightening the wording to remove this judgment requirement would require restructuring the principle rather than narrowing it. Criterion 1 status: BORDERLINE. A bounded check against the known consumer list (SKILL.md, conversus.yml, preset files, reference files, templates) is feasible and valid for those cases; the principle's stated scope extends beyond this list, making Criterion 1 borderline rather than a clear pass. This distinguishes VI from X: X's Criterion 1 failure is categorical (no check is feasible for readability); VI's Criterion 1 failure is borderline (a bounded check is feasible within the known-consumer-list subset). Future rehabilitation of VI targets Criterion 2 exclusively by restructuring around the bounded consumer list."

#### Recommendation 7: Add a CI lint for grandfathering-disclosure completeness

- **Original position**: Add to the Governance section a requirement that every principle listed as grandfathered has an entry in the disclosure, with a CI lint asserting completeness as principles are added or migrated.
- **Disposition**: Surviving
- **Explanation**: Neither GF nor CVXD challenged this recommendation. It is a P3 process improvement applying the XXVI meta-test pattern to the gate's own grandfathering list — a straightforward extension of an established pattern that both reviews implicitly endorse when they agree the grandfathering disclosure's clause-level granularity is a design strength worth preserving.

  The risk if ignored remains: future amendments add grandfathered principles informally without disclosure entries, eroding the gate's authority over time. The XXVI meta-test pattern exists precisely because silent coverage gaps in enumerated lists are the dominant failure mode as systems grow. The grandfathering disclosure is exactly such a list.

#### Recommendation 8: Record the migration SIR stream-crossing findings explicitly

- **Original position**: Require that every migration SIR include a XVII-classification table for each migrated sub-bullet: `| Sub-bullet text | XVII classification | Migration destination | Validation |`.
- **Disposition**: Modified
- **Explanation**: Two modifications are warranted based on cross-review convergence.

  First, GF's tensions analysis ("Audit trail record types," GF cross-review of CPC) identified that CVXD's parallel requirement (contrarian-argument entries in CONSTITUTIONAL_CONVERSATIONS.md) and my XVII-classification table requirement address different audiences — migration SIRs are read by implementation engineers; governance logs are read by constitutional reviewers. GF's coordination: "Make the XVII-classification table a required appendix in CONSTITUTIONAL_CONVERSATIONS.md deliberation entries, not just in migration SIRs." This consolidates both requirements into a single document both audiences consult.

  Second, CVXD's tensions section ("Normative-strength preservation," CVXD cross-review of CPC) identified that MUST-to-SHOULD downgrade during migration is a validity test my XVII-taxonomy table does not capture. A migration can correctly classify sub-bullets per XVII but still downgrade their normative force at the destination document. GF's coordination confirms this should be a jointly necessary condition: "correct routing per XVII taxonomy AND preserved normative strength at the destination."

  **Modified recommendation**: Require that every migration SIR include a XVII-classification table for each migrated sub-bullet expanded to: `| Sub-bullet text | XVII classification | Migration destination | Normative strength (original) | Normative strength (destination) | Validation |`. This table MUST also appear as a required appendix in the corresponding CONSTITUTIONAL_CONVERSATIONS.md deliberation entry, not only in the SIR. A migration that correctly classifies sub-bullets but downgrades MUST to SHOULD at the destination is invalid; the normative-strength columns make this detectable without requiring downstream readers to compare across documents.

---

### New Recommendations

- **Document VI/IX/XV/XXIV asymmetry in the v3.0.0 SIR** (Priority: P2)
  - **Triggered by**: GF cross-review of CPC, "Asymmetry documentation focus" tension section. GF identified that the v3.0.0 SIR needs two separate asymmetry sections — one for XVI/VII/VIII distinctness (my Rec 5) and one for VI/IX/XV/XXIV comparison (GF's Rec 5). My original review did not propose the VI/IX asymmetry documentation because I treated it as GF's domain. My cross-review of GF acknowledged both are needed and are orthogonal; this belongs in my revised recommendations.
  - **Proposed change**: The v3.0.0 SIR MUST include an explicit "asymmetry response" section addressing: (a) why VI's "when the artifact drives behavior" qualifier fails Criterion 2 while IX's "when framework or domain modeling requires them" qualifier does not — the structural distinction is that IX's qualifier is subordinate to a large block of MUST requirements that independently satisfy Criterion 1 (explicit typing, StrEnum for closed behavioral choices, no mutable global state), whereas VI's judgment-laden conditional IS the only trigger for VI's sole prescription with no supporting mechanical MUST block; (b) why XV's plugin isolation satisfies Criterion 1 via the `PluginResult` typed interface test (architectural invariant, not just stated) while VI's analogous isolation aspiration lacks a named enforcement mechanism. If this section cannot be drafted — if the asymmetry cannot be articulated without also condemning IX, XV, or XXIV — the migration basis for VI is not established and the SIR must record this gap rather than assert the migration was correct.
  - **Rationale**: Both my cross-review of CVXD and GF's cross-review of CPC converged on this as a settled finding: "the principled-distinction gap is a structural defect in the migration record, not a disputed interpretation." CVXD's Recommendation 4 and GF's Recommendation 5 both demand this documentation. My original review treated the gap as a "missed opportunity" finding belonging to the migration quality analysis but did not formulate it as a recommendation in its own right. Given the convergence across all three reviews, it warrants explicit recommendation status.

- **Adopt headline-plus-body convention for Criterion 2 evaluation in the gate text** (Priority: P2)
  - **Triggered by**: CVXD Recommendation 8 ("Clarify Criterion 2 evaluation scope as headline-plus-body") and the corresponding tension identified in my cross-review of CVXD ("Constitutional gate clarification: Criterion 2 scope versus migration SIR process requirement"). My original review proposed adding a passing worked example (Rec 4) but did not address the structural calibration gap CVXD identified — that the gate's Criterion 2 language could be read as applying to the headline alone.
  - **Proposed change**: Add one sentence to the Criterion 2 paragraph in the gate text: "Criterion 2 applies to the principle as a whole — the combination of headline and body. A principle whose headline is ambiguous but whose body specifies falsifiable rules satisfies Criterion 2 if the body rules, taken together, are specific enough to flag a violating PR without interpretation." This is consistent with the retained corpus: IX, XII, XIII, XVII all have headlines that are not independently falsifiable but bodies that are, and all pass Criterion 2.
  - **Rationale**: The safe agreement between my review and CVXD identified this calibration gap as credible and well-grounded. Without the headline-plus-body clarification, the gate can be read as applying only to the headline — which would make IX ("Functional Programming and Clean Code") a gate-failure despite its extensive falsifiable body. The calibration gaps identified by my original Rec 4 (vertical: no passing example) and by CVXD (structural: headline-only misreading) are both real and both should be closed. My Rec 4 addresses the vertical gap; this new recommendation addresses the structural gap.

---

### Position Summary

Of my original eight recommendations, I withdrew none, modified four (Recommendations 1, 2, 3, 8), and maintained four unchanged (Recommendations 4, 5, 6, 7). Two new recommendations emerged from the cross-review process.

The most significant change in my thinking was on Recommendation 3. My claim that X's error-handling sub-bullet was "substantively identical" to V's third bullet was wrong — X adds "missing documents" and "edge cases" as categories V does not enumerate. CVXD's cross-review identified this textual distinction, and it dissolves the XI violation I claimed. The deletion rationale was therefore incorrect. The routing concern survives because the sub-bullet is execution logic under XVII's taxonomy and docs/output-conventions.md is the wrong destination regardless, but the content should be preserved and routed correctly rather than deleted. I credit CVXD's cross-review of CPC's tension section ("X's sub-bullet 3 and Principle V") for surfacing this.

The modification to Recommendation 2 reflects a discipline boundary I should have maintained from the start: my audit role is cross-principle coherence, not migration adjudication. The XVII routing finding (execution-logic sub-bullets of VI cannot go to CONTRIBUTING.md) is valid and important whether or not VI's migration was correctly decided. Framing it as conditional on migration confirmation rather than as a standalone migration-improvement recommendation preserves the finding's value without my overreaching into the retention-versus-migration dispute that properly belongs to the synthesis arbiter.

My remaining highest-priority recommendation is the modified Recommendation 1 — the composite XVI annotation covering the full compliance history from the pre-cycle-1 body through v2.3.2. This should survive into the final synthesis because the grandfathering disclosure is the point of first contact for future amendment authors assessing XVI, and an annotation that understates XVI's compliance history will lead to over-migration of the principle's mechanically-verifiable content. Both GF and CVXD independently confirmed that XVI's determinism-scope content has more gate compliance than the disclosure acknowledges; the composite annotation is the governance mechanism for recording that finding with the precision required to prevent a future migration from treating the failing plain-language clause as a license to migrate the entire principle.