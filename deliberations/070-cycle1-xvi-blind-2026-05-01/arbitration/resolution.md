I'll read the synthesis and dispute documents before producing my arbitration resolution.

Now I have all the documents needed to produce my ruling. I'll compose the arbitration resolution as required.

### Process Note

This arbitration was triggered by the `always` condition — subject arbitration activates unconditionally in this deliberation configuration regardless of dispute count or severity. Two disputes remain from the Phase 5 synthesis. Two agents participated: **skeptic-mathematical** and **skeptic-cross-principle**. This is a **cooperative** deliberation with subject arbitration: I am the subject of the review (the conversus constitution) and hold binding decision authority over unresolved disputes.

---

### Decision Framework

The following principles and governance requirements from the grounding document (`CONSTITUTION-v2.6.0-blind.md`) bear directly on the two remaining disputes:

- **Governance: Constitutional Inclusion Criteria — Criterion 3 (Distinctness)**: "The principle MUST cover concerns not already addressable by composing existing principles. Restating an existing principle in different words is rejected by this gate." (Governance section, Constitutional Inclusion Criteria, criterion 3.) This criterion determines whether stage-3's bit-identical assembly guarantee constitutes an independent normative contribution or a composition of existing principles.

- **Governance: Constitutional Inclusion Criteria — Criterion 1 (Mechanical verification capability)**: "at least one form of automated check... MUST be feasible such that a future PR violating the principle would fail the check. The check does NOT have to exist at amendment time, but the path to building it MUST be concrete enough that an engineer reading the principle can sketch the check in one paragraph." (Governance section, Constitutional Inclusion Criteria, criterion 1.) This criterion shapes how the stage-3 verification artifact is labeled and what work it is required to perform.

- **Principle IX — Behavior-over-shape extension (explicit "shape test" prohibition)**: "A test that verifies `result.foo == 9` without verifying that the 9 actually represents the right behavior is a shape test... Shape tests are permitted only as preconditions inside a test that ALSO asserts behavior." (Principle IX, behavior-over-shape extension.) The explicit prohibition on "shape tests" establishes the terminological context that makes SCP's rename recommendation non-aesthetic.

- **Principle X — Zen of Python Output**: "Errors should never pass silently — warnings are emitted for malformed output, missing documents, and edge cases." (Principle X, fourth bullet.) Applied to specification text: terminological collision that requires a reader to perform implicit disambiguation is the specification-level analogue of a silent error.

- **Principle XI — Single Source of Truth**: "Every piece of information MUST have exactly one authoritative source. All other representations MUST be derived from that source, not maintained independently. When two sources disagree, it is always a bug." (Principle XI, opening paragraph.) If stage-3's content is fully subsumed by VII+VIII, naming it as a headline invariant in XVI introduces a secondary, potentially diverging source for the same normative content — the class of bug XI was designed to eliminate.

- **Principle VII — Reproducibility Over Inconsistency**: "Given the same inputs, conversus MUST produce structurally identical output." (Principle VII, opening.) Stage-3's assembly-form guarantee is grounded in VII's same-inputs/same-output requirement; the dispute about independence turns on whether VII (plus VIII) is already sufficient.

- **Principle VIII — Templating Engines Over Inference**: "Prefer mechanical template-driven behavior over LLM inference and improvisation." (Principle VIII, opening.) The bit-identical assembly claim follows directly from VIII's mechanical template-driven guarantee; this is the second leg of the composition argument both reviews identified.

---

### Binding Decisions

#### Dispute: Stage-3 Headline Invariant Status and Criterion 3 Analysis Formality

**Positions:**

- **skeptic-mathematical**: The bilateral negative finding — that neither of two adversarially-positioned agents, arriving via different analytical paths, identified any stage-3-specific normative claim not already implied by Principles VII and VIII — constitutes the effective Criterion 3 analysis outcome. This finding should immediately determine headline structure: one named invariant (parameter pinning). The stage-3 verification artifact, if added, is a completeness test for the VII+VIII composition, not evidence of stage-3 independence. The formal Criterion 3 record must be documented (as a structured SIR entry) before the headline restructuring is applied, but this documentation is not a blocking process gate — it is a co-requisite of the same amendment. (skeptic-mathematical/disputes.md, Disputes 1 and 2.)

- **skeptic-cross-principle**: The stage-3 verification artifact should be added now (modified Rec 2, option a) without gatekeeping the headline determination on the artifact's outcome. The Criterion 3 question — "can we name a contract test that tests something VII+VIII leave underspecified?" — cannot be answered in the abstract; the artifact is what generates the evidence the analysis needs. SCP proposed a conditional exit: if the artifact, when implemented, reproduces a failure VII and VIII individually would not catch, stage-3 retains headline status; otherwise, the SIR documentation provides the complete disposition. (skeptic-cross-principle/disputes.md, Dispute 2.)

**Synthesizer's assessment:** SM's position is better supported on the headline question. The bilateral negative finding is the relevant evidence for Criterion 3, not the artifact's implementation. SCP's conditional exit presupposes a stage-3-specific claim that could be named; neither review has identified what that claim would be. In the absence of a candidate, the burden of proof for headline invariant status is not met. The artifact should be added as a completeness test, and the headline determination should follow the Criterion 3 conclusion now, not await the artifact. (synthesis/final.md, Remaining Disputes, first dispute, Synthesizer assessment.)

**Ruling:** Reduce XVI's headline to one named invariant (parameter pinning) now, add the stage-3 verification artifact to the enforcement block labeled explicitly as a VII+VIII composition completeness test, and document the Criterion 3 analysis as a formal SIR entry — all as co-requisites of the same amendment, with no blocking gate separating them.

**Grounding citation:** Governance — Constitutional Inclusion Criteria, Criterion 3: "The principle MUST cover concerns not already addressable by composing existing principles." The bilateral negative finding from two independently-positioned adversarial reviews is precisely the evidence Criterion 3 requires: neither review identified a verifiable assertion about stage-3 (bit-identical assembly given a fully-pinned parameter set within a deliberation run) that is not already a consequence of composing Principle VII ("same config produces same prompts; no ambient state or hidden context") with Principle VIII ("mechanical template-driven behavior... same config produces same prompts"). The composition is not merely an informal impression — VII's reproducibility guarantee and VIII's determinism-by-construction are individually sufficient to entail stage-3's property, and both reviews confirmed this through independent analytical paths. Under Criterion 3, this is the finding; the burden of proof is on independence, not composition.

**Rationale:** SM and SCP agree on more than they disagree. Both accept: (1) the safe agreement is real; (2) the artifact should be added; (3) the SIR should document the Criterion 3 analysis. The dispute is sequencing and whether the artifact's eventual implementation could reverse the headline decision. On sequencing: the SIR documentation entry — which SM explicitly says need not be elaborate ("a three-sentence entry stating the question, the evidence, and the conclusion satisfies the requirement") — can be written simultaneously with the headline restructuring as part of the same amendment. SM's non-negotiable is not a blocking gate; it is a co-requisite documentation requirement. On reversibility: SCP's conditional exit ("if the artifact reveals independence, reconsider") is a valid future-amendment path, but it is not a reason to defer the current decision. Constitutional amendments are the mechanism for reconsideration when new evidence emerges; SCP's conditionality is already handled by the existing amendment process without encoding it into XVI's text.

**Rejected position:** SCP's conditional exit — deferring headline reduction until the artifact's implementation reveals whether stage-3 is independent — is not adopted. SCP's strongest argument is epistemological: the analysis question cannot be answered in the abstract without naming a candidate artifact. This is correct as a matter of first principles, but it mischaracterizes the state of this deliberation. Both reviews *did* attempt to name stage-3-specific claims — that is how they arrived at the bilateral negative finding. The analysis was performed; the finding is that no distinguishing claim was identified. The conditional exit treats the bilateral negative as an absence of analysis rather than as an analysis outcome. Under Criterion 3's Governance gate, the standard is whether "an engineer reading the principle can sketch the verification check in one paragraph" — not whether the check has been implemented. Both reviews demonstrated this is achievable for stage-3-as-VII+VIII-composition. The artifact will verify the composition's coverage, which is valuable regardless of the Criterion 3 outcome; but "the artifact hasn't been implemented yet" is not a reason to leave the headline ambiguous in the meantime.

**Required changes** (applying to `CONSTITUTION-v2.6.0-blind.md`):

1. **Headline reduction**: Amend Principle XVI's opening paragraph from a three-requirement enumeration to one named structural invariant. The amended headline reads: "When optimization drives decisions, conversus MUST satisfy one structural invariant: **parameter pinning** — resolved values are persisted once and re-loaded, never re-resolved within a deliberation run." Remove requirements (1) and (2) from the headline enumeration (plain-language pairing was already converged as excised; assembly-form determinism moves to body as per below).

2. **Stage-3 body relocation**: In XVI's three-stage pipeline body description, replace the existing stage-3 text with: "3. **Deterministic assembly**: applies Principles VII and VIII to the optimization domain — given a template and a fully-pinned parameter set (every gap identifier from stage 1 has a pinned value from stage 2), the assembled objective function is assembly-form-identical on every assembly within a deliberation run. No additional normative requirement beyond Principles VII and VIII is introduced at this stage."

3. **Stage-3 verification artifact in enforcement block**: In XVI's Clarification v2.3.2 Enforcement sub-bullet, after the stage-2 enforcement text, add: "Stage-3 assembly-form determinism MUST have a corresponding completeness test: a CI check that invokes the assembly path twice within the same run artifact, using the same fully-pinned parameter set and the same template registry state, and asserts assembly-form-identical output. This test verifies the VII+VIII composition applied to the optimization domain. It is a pipeline completeness test — not a Criterion 3 demonstration of stage-3 independence from those principles. If a future implementation of this test reveals a failure mode that Principles VII and VIII individually would not catch, that finding constitutes grounds for a new amendment reconsidering stage-3's constitutional status."

4. **SIR Criterion 3 formal record**: Add to XVI's SIR comment block the following structured entry: "Criterion 3 assessment for stage-3 deterministic assembly (deliberation 070, 2026-05-01): (a) Question: does stage-3's assembly-form-identity claim produce a verifiable assertion not already implied by composing Principle VII ('same config produces same prompts; no ambient state') with Principle VIII ('mechanical template-driven behavior')? (b) Evidence: bilateral negative finding from two adversarially-positioned reviewing agents (skeptic-mathematical, skeptic-cross-principle), each arriving at the composition conclusion through different analytical paths; neither agent identified a stage-3-specific verifiable claim that VII+VIII do not subsume. (c) Conclusion: stage-3 is a VII+VIII composition applied to the optimization domain; no independent normative requirement beyond those principles is introduced. (d) Headline consequence: one named invariant (parameter pinning). (e) Artifact disposition: stage-3 verification artifact added to enforcement block as a VII+VIII composition completeness test. A future amendment may reopen this assessment if a stage-3-specific claim is identified that the completeness test demonstrates to be independent of VII+VIII."

---

#### Dispute: Shape Determinism Rename

**Positions:**

- **skeptic-cross-principle**: Replace "shape determinism" throughout XVI with "assembly-form determinism" to eliminate terminological collision with Principle IX's explicit "shape test" prohibition. In a document consumed by agents as execution truth, encountering "shape determinism MUST be satisfied" (XVI) alongside "shape tests are prohibited on their own" (IX) creates interpretive work that fails silently. The rename is zero-normative-cost. (skeptic-cross-principle/disputes.md, Dispute 1.)

- **skeptic-mathematical**: SM used "shape determinism" in its modified Rec 4 restructured headline without engaging the rename question at any phase. SM's non-engagement is a gap, not an opposition. (skeptic-mathematical/disputes.md, no counter-argument recorded.)

**Synthesizer's assessment:** SCP's position is uncontested on the merits. No counter-argument exists in the deliberation record. The collision is genuine. The cost of the rename is zero. Given the headline reduction to one invariant, the term "shape determinism" will no longer appear in the headline; the rename's primary impact is on body text and the Clarification v2.3.2 block. SM's failure to engage does not create a dispute — it leaves SCP's position unopposed. (synthesis/final.md, Remaining Disputes, second dispute, Synthesizer assessment.)

**Ruling:** Adopt the rename. Replace "shape determinism" with "assembly-form determinism" in all XVI body text and in the Clarification v2.3.2 block wherever the term refers to the assembled objective function's structural guarantee.

**Grounding citation:** Principle X — "Errors should never pass silently." In a specification consumed by agents as execution truth, terminological collision between a prohibition ("shape tests are prohibited on their own" — Principle IX) and a structural requirement using the same root word ("shape determinism" — Principle XVI) is exactly the class of silent error Principle X cautions against. An agent that has correctly internalized IX's prohibition — "shape tests are prohibited" — encounters XVI's requirement — "shape determinism is required" — and must perform implicit disambiguation. The constitution provides no disambiguation signal. This is a silent interpretive failure, not an aesthetic concern. Additionally, Principle XI (Single Source of Truth) applies to vocabulary: a term that means "prohibited" in one principle and "required" in another has two sources for its normative valence. The rename eliminates this precisely, at zero normative cost.

**Rationale:** SM's non-engagement is not a position. The reform does not touch any of SM's substantive recommendations; "assembly-form determinism" as the replacement for "shape determinism" in body text is compatible with all of SM's surviving recommendations (Recs 2, 3, 6, 7, New Rec 1, New Rec 2, modified Recs 1, 4, 5). With the headline now reduced to one invariant (parameter pinning), the term "shape determinism" no longer appears in the headline, so the rename's scope is entirely within body text where SM had no competing formulation. There is no substantive conflict to adjudicate; only a gap in SM's review coverage.

**Rejected position:** No position explicitly opposing the rename exists. The alternative — retaining "shape determinism" unchanged — is rejected because it preserves a genuine terminological collision that Principles IX and X together prohibit. The absence of SM counter-argument is not grounds for inaction when SCP's argument is uncontested on the merits.

**Required changes** (applying to `CONSTITUTION-v2.6.0-blind.md`):

1. **Body text rename in Principle XVI**: In the three-stage pipeline body description, in the stage-3 text (as relocated per Dispute 1 required change 2 above), the phrase "assembly-form-identical" should be used consistently (this follows naturally from the relocation text above which already incorporates the new term).

2. **Clarification v2.3.2 rename**: In the Clarification v2.3.2 block, locate all instances of "shape determinism" and replace with "assembly-form determinism." Specifically: the sub-bullet "(2) **shape determinism**" in the existing headline enumeration (which will be removed by Dispute 1's headline reduction, so this applies to any remaining references in the Clarification text); and the Clarification's own references to the term within its cross-run/within-run determinism scope discussion. The phrase "cross-run variance in the assembled objective function's *shape*" in Clarification v2.3.2 should be assessed in context: if "shape" here refers to the structural guarantee (parameter names, template selection, gap-identifier set), rename to "assembly form" or "assembled form" for consistency. The existing Clarification text stating "cross-run variance in the assembled objective function's *shape* (parameter names, template selection, gap-identifier set) is prohibited" should read "cross-run variance in the assembled objective function's *assembly form* (parameter names, template selection, gap-identifier set) is prohibited."

3. **Headline removal**: The headline enumeration item "(2) **shape determinism**" is removed as part of the headline reduction to one invariant (Dispute 1, required change 1). No separate rename action is needed for the headline position; it ceases to exist.

---

### Summary of Changes Required

**P1 — Required for correctness**

1. **Headline reduction to one invariant** (from Dispute: Stage-3 Headline Invariant Status): Remove requirements (2) and (3) from XVI's headline enumeration; retain only parameter pinning. Applies to: `CONSTITUTION-v2.6.0-blind.md`, Principle XVI opening paragraph. Priority: P1.

2. **Stage-3 body relocation with VII+VIII attribution** (from Dispute: Stage-3 Headline Invariant Status): Replace existing stage-3 body text with language explicitly attributing stage-3's guarantee to Principles VII and VIII and stating no additional normative requirement is introduced. Applies to: `CONSTITUTION-v2.6.0-blind.md`, Principle XVI three-stage pipeline body. Priority: P1.

3. **SIR Criterion 3 formal record** (from Dispute: Stage-3 Headline Invariant Status): Add structured five-part Criterion 3 analysis entry to XVI's SIR comment block. Applies to: `CONSTITUTION-v2.6.0-blind.md`, Principle XVI SIR comment. Priority: P1 (SM's non-negotiable: the formal record must accompany the headline restructuring as a co-requisite of the same amendment).

**P2 — Required for design integrity**

4. **Stage-3 verification artifact in enforcement block** (from Dispute: Stage-3 Headline Invariant Status): Add named CI completeness test to XVI's Clarification v2.3.2 Enforcement sub-bullet, explicitly labeled as a VII+VIII composition completeness test with future-amendment reconsideration clause. Applies to: `CONSTITUTION-v2.6.0-blind.md`, Principle XVI Clarification v2.3.2 Enforcement. Priority: P2.

5. **Assembly-form determinism rename in Clarification v2.3.2 block** (from Dispute: Shape Determinism Rename): Replace "shape determinism" with "assembly-form determinism" in all XVI Clarification v2.3.2 body text referring to the assembled objective function's structural guarantee, including the cross-run variance prohibition sentence. Applies to: `CONSTITUTION-v2.6.0-blind.md`, Principle XVI Clarification v2.3.2. Priority: P2.

6. **Assembly-form determinism rename in XVI body pipeline description** (from Dispute: Shape Determinism Rename): Ensure stage-3 pipeline description uses "assembly-form-identical" (as incorporated in required change 2 above). Applies to: `CONSTITUTION-v2.6.0-blind.md`, Principle XVI three-stage pipeline body. Priority: P2.

---

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| Stage-3 Headline Invariant Status and Criterion 3 Analysis Formality | Reduce headline to one invariant now; add artifact as completeness test; document Criterion 3 formally in SIR — all as co-requisites of the same amendment | High | Grounded in Governance Criterion 3 (distinctness) and the bilateral negative finding as the analysis outcome; synthesizer's assessment aligns; SM's non-negotiable on formality is satisfied by SIR co-requisite without creating a blocking gate; SCP's practical concern about artifact value is satisfied by adopting artifact addition now |
| Shape Determinism Rename | Adopt rename throughout XVI body and Clarification v2.3.2 | High | Grounded in Principles IX (explicit "shape test" prohibition) and X (silent failures prohibited); uncontested by any agent; zero normative cost; headline reduction removes the headline instance naturally |

This deliberation is of high quality. The two disputes that survive to arbitration are not fundamental disagreements about substance — both agents agree that stage-3 is a VII+VIII composition, that the artifact should be added, and that the SIR should document the analysis. The dispute is sequencing and formality, which the co-requisite structure resolves. The rename dispute exists only because SM's review had a gap in coverage, not because of substantive conflict. Five unanimous convergence points — each earned through genuine Phase 2 cross-review exposure of real contradictions — represent the deliberation process working correctly. The most consequential outcome, the excision of the plain-language requirement, emerged from diametrically opposed Phase 1 positions converging after the adequacy-vs-presence distinction was established. That convergence is the mark of a deliberation that generated knowledge rather than merely documenting initial positions.

The remaining disputes do not indicate a systemic issue in the spec. They reflect the inherent difficulty of making compositional arguments about normative content (is stage-3 independent or derivative?) and the routine challenge of consistent terminology across a long document. Both are addressable within the same amendment without reopening converged questions.

**BLIND VERIFICATION VERDICT: PASS WITH FIXES**