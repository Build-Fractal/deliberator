# Scope-Creep Disputes — T001: Verify Draft Markers

**Agent role**: scope-creep (scope-creep detector)
**Phase**: 4 — Final Disputes and Convergence
**Iteration**: 1

---

### Remaining Disputes

#### Dispute 1: Compliance recommendations require explicit "deferred" tagging in synthesis

- **My claim**: Compliance's surviving recommendations (modified Rec 1: FR-001a for cooperative negative requirement; modified Rec 4: canonical marker location; new Rec: cross-reference appendix) must be explicitly tagged as "deferred to Phase 2 or later" in the final synthesis output. Without this tag, the synthesis implicitly expands T001 from "verify FR-001" to "verify FR-001 and propose spec amendments." (Scope-creep revision, New Recommendations: "Tag compliance recommendations as deferred observations," Priority P2.)
- **Opposing position(s)**: Compliance's revision (Position Summary, final paragraph) frames the modified Rec 1 as "the one finding that is genuinely within FR-001's scope" and states it "should survive into the final synthesis" — but does not explicitly constrain its survival to observation-only status. Compliance's new recommendation ("Cross-reference FR-002/FR-003 observations to T002") proposes a "brief appendix" as a T001 output artifact, which is a deliverable beyond verification reporting. (Compliance revision, New Recommendations and Position Summary.)
- **Why I will not concede**: T001's task description (tasks.md L24) says "Verify draft markers exist" — it does not say "verify and propose spec amendments" or "verify and produce an appendix for T002." Every compliance recommendation that survives into the synthesis without a deferred tag becomes, by default, a T001 deliverable. The distinction between "finding" and "deliverable" is precisely the boundary that scope-creep enforcement exists to maintain. If the synthesis adopts compliance's recommendations as T001 outputs rather than deferred observations, it sets a precedent where verification tasks produce spec-modification proposals, and the verification-only contract is meaningless.
- **Counter-argument to their position**: Compliance's revision (Position Summary) argues the modified Rec 1 is "genuinely within FR-001's scope" because it concerns what the functional requirements say about template markers. This is true at the observation level — the gap exists, and noting it is valid. But the recommendation as stated ("Flag the absence... as a T001 finding, and defer the creation of FR-001a to a future spec-maintenance task") is itself a two-part recommendation: the first part (flag) is verification; the second part (defer the creation of FR-001a) is a process directive that goes beyond what a verification task should prescribe. The observation is in scope; the process directive is not. The appendix recommendation has the same problem: observing that FR-002/FR-003 concerns exist is verification; creating a structured handoff appendix as a T001 artifact is deliverable creation.
- **Proposed resolution path**: The synthesizer should adopt compliance's observations (the gap exists, the redundancy exists, the FR-002/FR-003 concerns exist) but tag every recommendation that proposes creating or modifying any artifact — including an appendix, a new FR, or a canonical location refactoring — as "deferred to Phase 2+." The synthesis document itself serves as the handoff mechanism; no separate appendix artifact is needed. If compliance objects to this framing, the synthesizer must choose.

#### Dispute 2: Whether verification tasks should produce structured handoff artifacts

- **My claim**: T001 should produce a verification report (PASS/FAIL per template file, plus observations). It should not produce additional structured artifacts such as a "T002 observations appendix" or a formal FR-001a proposal document. The deliberation artifacts (reviews, cross-reviews, revisions, synthesis) are T001's natural outputs. Anything beyond that is scope expansion. (Scope-creep revision, Recommendation 1: negative-action constraint; New Recommendations: deferred tagging.)
- **Opposing position(s)**: Compliance's revision (New Recommendations: "Cross-reference FR-002/FR-003 observations to T002") proposes that "The T001 compliance review should include a brief 'Observations for T002' appendix that forwards the FR-002/FR-003 concerns." Compliance frames this as "near-zero cost" and necessary to prevent valid observations from disappearing.
- **Why I will not concede**: The argument that observations will "disappear from the deliberation record" is false. The deliberation artifacts — compliance's review, scope-creep's review, both cross-reviews, both revisions, and the final synthesis — ARE the record. They are stored in `/tasks/T001/compliance/` and `/tasks/T001/scope-creep/`. T002's agents can and should read T001's synthesis as input context. Creating a separate appendix artifact is redundant with the deliberation record and introduces a new deliverable type that is not defined in the task description, the conversus protocol, or the spec.
- **Counter-argument to their position**: Compliance argues the appendix is "near-zero cost." Cost is not the issue; precedent is. If T001 produces an appendix for T002, every future verification task is implicitly expected to produce handoff artifacts for downstream tasks. This transforms verification from a bounded checkpoint into an open-ended analysis task. The marginal cost of one appendix is low; the marginal cost of establishing that verification tasks produce handoff artifacts is high.
- **Proposed resolution path**: The synthesizer should note compliance's FR-002/FR-003 observations in the synthesis document itself (which T002's agents will read as context), and explicitly state that no separate appendix artifact is a T001 deliverable. The synthesis is the handoff.

### Convergence

#### Converged 1: T001 is verification-only — no modifications to any files

- **Shared position**: T001 verifies the current state of template files against FR-001. It does not add, modify, or fix markers. The template files are in their correct state and no changes are needed.
- **Agreeing agents**: scope-creep (revision, Recommendation 1 — surviving, negative-action constraint), compliance (revision, Position Summary — "T001 is verification-only"; Recommendation 2 withdrawal — "FR-002 is explicitly assigned to T002, not T001").
- **Strength**: Unanimous
- **Path to convergence**: Agreed from Phase 1. Both initial reviews independently confirmed that all three draft-bearing templates contain the correct marker on line 1 and the cooperative template correctly lacks it. The cross-review process reinforced this — compliance withdrew four of six recommendations specifically because they violated this boundary.

#### Converged 2: The cooperative template negative-check gap is real and must be addressed

- **Shared position**: FR-001 specifies what three templates MUST contain but no FR mandates what the cooperative template MUST NOT contain. Acceptance scenario 4 tests for this property without a backing requirement. This gap should be addressed — the only disagreement is where and when.
- **Agreeing agents**: scope-creep (revision, Recommendation 2 — modified to pair task-description fix with compliance's FR-001a), compliance (revision, Recommendation 1 — modified to flag and defer FR-001a).
- **Strength**: Unanimous
- **Path to convergence**: Both agents identified this gap independently in Phase 1. Cross-review surfaced that the two recommendations were complementary (task-description fix + FR-level fix), not competing. Both revisions explicitly acknowledged the other agent's fix as necessary. The remaining difference is purely about tagging: scope-creep wants both fixes adopted with the FR-level fix explicitly deferred; compliance wants the finding to survive into synthesis with a deferral note. These positions are substantively identical.

#### Converged 3: T001 scope is FR-001 only, not FR-001 through FR-003

- **Shared position**: T001 maps to FR-001 and US1 only. FR-002 and FR-003 are T002's scope. Recommendations targeting FR-002 or FR-003 do not belong in T001's compliance review.
- **Agreeing agents**: scope-creep (revision, Recommendation 6 — cross-reference AS1-AS4 for FR-001 only), compliance (revision, Recommendations 2, 3, 5, 6 — all withdrawn because they targeted T002 scope).
- **Strength**: Unanimous
- **Path to convergence**: This was the most significant outcome of the cross-review process. Compliance's initial review treated T001 as a general compliance audit spanning FR-001 through FR-003. Scope-creep's cross-review (Dangerous Contradictions, item 2) identified this as a scope violation. Compliance's revision explicitly accepted the criticism: "I had systematically violated T001's task boundary by issuing recommendations against FR-002 and FR-003... This overreach was consistent across four of my six recommendations and represents a structural error."

#### Converged 4: PASS/FAIL two-state model replaces PASS/FAIL/DRIFT three-state model

- **Shared position**: Verification tasks should use a two-state output: PASS (requirement confirmed) or FAIL (requirement not met, describe discrepancy). The DRIFT category is unnecessary because the negative-action constraint already prevents "helpful correction" of near-misses.
- **Agreeing agents**: scope-creep (revision, Recommendations 4 and 5 — both modified to drop DRIFT), compliance (cross-review, Tensions: "Handling 'wrong marker' vs 'missing marker'" — argued PASS/FAIL is cleaner).
- **Strength**: Unanimous
- **Path to convergence**: Scope-creep initially proposed a three-state model in Phase 1. Compliance's cross-review argued that DRIFT introduces ambiguity and that the negative-action constraint handles the same failure mode more directly. Scope-creep accepted this in revision: "I was solving the same problem twice with different mechanisms, and the simpler mechanism is the better one."

#### Converged 5: Exact marker string should appear in task description

- **Shared position**: The T001 task description should include the exact string `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` so the executing agent has a self-contained verification target without needing to cross-reference the spec.
- **Agreeing agents**: scope-creep (revision, Recommendation 3 — surviving), compliance (cross-review, Tensions: "Granularity of marker syntax verification" — acknowledged as "more immediately relevant" for T001).
- **Strength**: Unanimous
- **Path to convergence**: Scope-creep proposed this in Phase 1. Compliance's cross-review did not challenge the substance and explicitly endorsed it for Phase 1 sequencing. No disagreement at any phase.

### Final Position Statement

**Non-Negotiables** (3 items):

1. **The negative-action constraint must be added to the T001 task description.** This is the single most important process safeguard for Phase 1 verification tasks: "Report presence or absence only — do not add, modify, or fix markers." Without it, the task description permits the executing agent to interpret a FAIL result as an invitation to remediate. Both reviews confirmed this gap; no cross-review challenged it. (Scope-creep revision, Recommendation 1, surviving.)

2. **All compliance recommendations that propose creating or modifying artifacts must be tagged as deferred in the synthesis.** This includes FR-001a, the canonical marker location refactoring, and the T002 observations appendix. The observation that these gaps exist is valid and belongs in T001's record. The proposal to create new artifacts does not. (Scope-creep revision, New Recommendations: "Tag compliance recommendations as deferred observations.")

3. **T001 produces no deliverables beyond the verification report and deliberation artifacts.** The deliberation record (reviews, cross-reviews, revisions, disputes, synthesis) is the output. No appendix, no FR proposal document, no handoff artifact. The synthesis document is the handoff to downstream tasks. (Scope-creep revision, Recommendations 1 and 7; tasks.md L24: "Verify draft markers exist.")

**Flexibility** (2 items):

1. **The exact wording of the negative-action constraint is flexible; the presence is not.** I proposed "Report presence or absence only — do not add, modify, or fix markers." If the synthesizer prefers different phrasing that achieves the same prohibition, that is acceptable. What must be preserved: an explicit, unambiguous prohibition on remediation in the task description itself.

2. **The checkpoint failure protocol (Recommendation 7) can be adopted at Phase 1 level or deferred to a cross-phase convention.** I proposed adding it after the Phase 1 checkpoint in tasks.md. If the synthesizer determines this belongs in a broader process document rather than tasks.md, that is acceptable. What must be preserved: a formal statement somewhere in the spec's process artifacts that verification failures trigger new remediation tasks, not modifications to verification tasks.
