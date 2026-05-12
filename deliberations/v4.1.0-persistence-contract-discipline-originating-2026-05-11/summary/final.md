# Synthesis — v4.1.0 Persistence Contract Discipline Originating Deliberation

**Deliberation:** `v4.1.0-persistence-contract-discipline-originating-2026-05-11`
**Stage:** Phase 5 (Synthesis) — produced manually after engine crash. See Recovery Note at end.
**Agents:** pragmatist, devils-advocate, persistence-expert, ci-expert.
**Target spec:** `specs/v4.1.0-persistence-contract-discipline/spec.md` § 4 — Tier 1 Principle II sub-clause append.

---

## Recovery Note

This synthesis was produced manually on 2026-05-12 after the Phase 5 synthesizer crashed with `RateLimitError: Anthropic rate limit exceeded after 3 attempts: Error code: 429` at `01:17:35`. Phases 1-4 completed successfully. The inputs for this manual synthesis are exactly the inputs the engine would have consumed: each agent's `revision_2.md` (Phase 3 iteration 2 final position) and `disputes.md` (Phase 4 dispute consolidation). No new agent rounds were run; no positions were invented. Where an agent did not address a question explicitly, that gap is called out.

---

## Areas of agreement across all four agents

Despite the deliberation's adversarial framing (pragmatist vs. devils-advocate; expert vs. expert), the four agents converged to a strikingly high degree on the **substantive engineering content** of the amendment. The disputes that remain (see next section) are narrow and live almost entirely at the wording/policy layer, not the engineering layer.

The five convergences below are reported in every agent's `disputes.md` Convergence section:

1. **Bidirectional drift detection — unanimous.** All four agents agree that the spec's current Sub-clause 2 mandate — "CI validates that artifacts written during a run conform to the declared schema" — covers only *forward* drift (producer wrote something off-schema). It misses *reverse* drift: the schema gets edited but producer code is not updated. Persistence-expert raised this first (their Recommendation 2); ci-expert called it "a critical gap I missed in my original review" in revision_2.md and adopted it as their top new recommendation; pragmatist and devils-advocate both added it as P1 new recommendations after Phase 2 cross-review. The fix is to mandate validation in both directions in spec § 4 sub-clause 2.

2. **Pre-merge gate placement — unanimous.** All four agents converge that "mechanical enforcement" in sub-clause 2 must mean *PR-blocking* or merge-blocking CI gates — not advisory, not post-merge, not scheduled. Ci-expert held this position from Phase 1 (their surviving Recommendation 1); the others adopted it in revision_2.md once they recognized advisory enforcement defeats the mechanical-verifiability claim that justifies the amendment's Inclusion Criteria gate. Spec § 4 is silent on placement today; the agents want this nailed down.

3. **Consumer-side contract validation fixtures — unanimous.** Sub-clause 4 mandates that consumers consume the declared surface, not implementation details. Devils-advocate initially flagged this as unenforceable (you can't statically analyze every consumer's parsing code). Persistence-expert proposed the resolution: require consumers to ship test fixtures pinning the surfaces they consume, validated in *consumer* CI. Devils-advocate accepted this in revision_2.md ("moves enforcement to the consumer's CI where it can be mechanically verified"); ci-expert and pragmatist both adopted it. The bilateral enforcement model is the agreed shape.

4. **Strengthening the "deterministic conformance check" wording — unanimous on need, near-unanimous on language.** All four agents identified the prose-schema loophole (a product declares `schema: this paragraph of prose` and trivially conforms) as the single most serious threat to the amendment's effectiveness. The agreed-upon replacement language, drawn from persistence-expert's revision_2.md Recommendation 3 and explicitly accepted by ci-expert and devils-advocate, is: *"machine-executable validation with binary pass/fail result that verifies field presence, types, and value constraints, excluding prose descriptions, manual checklists, or subjective interpretation."* The pragmatist holds out for a stricter version (mandate JSON Schema / XSD / Pydantic only); see disputes.

5. **Performance budgets, not fixed timeouts — majority.** Persistence-expert (Recommendation 9), ci-expert (modified Recommendation 5), and devils-advocate (new recommendation) agree that schema validation must declare incremental or sampling-based performance budgets rather than hard timeouts, so that performance pressure cannot be used to disable enforcement on large artifact sets (e.g., spec-kit-orc's `.orchestrator/` JSONL execution logs). Pragmatist is recorded as neutral / non-opposed.

Two further convergences appear in subsets:

6. **Schema surface coverage expansion (bilateral).** Persistence-expert + ci-expert agree that the spec's implicit assumption of field-based schemas misses JSONL streaming (line semantics), positional formats (column-order), binary formats, and hybrid YAML-frontmatter-plus-markdown. Spec-kit-orc's `state-files.md` already uses two of these formats; the spec as drafted under-covers them.

7. **SemVer-compatible schema versioning (bilateral).** Persistence-expert + pragmatist agree that sub-clause 3's "documented bump procedure" should be tightened to SemVer (MAJOR/MINOR/PATCH) semantics for schemas. Devils-advocate and ci-expert did not weigh in directly.

The single **dis**agreement worth flagging in this section: devils-advocate withdrew their Phase 1 Recommendation 3 ("Split this into a separate Principle XXIX instead of attaching to Principle II"). No other agent supported it in cross-review; devils-advocate themselves concluded in revision_2.md that "the attachment to Principle II (Stable Interfaces) is conceptually coherent — persistent state is indeed a type of interface that requires stability." This forecloses the "amendment is a new principle in disguise" attack vector that QUESTION.md flagged as one of the strongest objections to Q1. All four agents now agree the sub-clause attachment is load-bearing, not cosmetic.

## Disputes that remain

After Phase 4 reconciliation, only two substantive disputes remain. Both are at the **policy** layer, not the engineering layer.

### Dispute A — Schema-format strictness: mandate technologies vs. tighten the wording

- **Pragmatist's position** (non-negotiable in their disputes.md): mandate JSON Schema, XSD, or Pydantic models *exclusively* — eliminate the "any other format" escape clause from spec § 4 sub-clause 2. Rationale: even strengthened wording like "machine-executable validation with binary pass/fail" remains vulnerable to "creative interpretation" — a product could implement a validator that returns `pass` for any artifact containing their declared field names, technically satisfying the wording while providing no real enforcement. Only mandating proven technologies with established validation semantics closes the loophole.

- **Three-against-one** — devils-advocate, persistence-expert, and ci-expert all hold the line on format flexibility. Their argument:
  - Technology lock-in contradicts the spec's explicit non-goal § 3 ("Does NOT mandate XML... Product implementations choose XSD, JSON Schema, Pydantic, AST-validator, or any other mechanical schema language").
  - The persistence-expert's strengthened language ("excluding prose descriptions, manual checklists, or subjective interpretation") closes the gaming loophole without technology constraint.
  - Mandating field-based formats (JSON Schema / Pydantic) would force suboptimal tooling for non-field surfaces — JSONL streaming validation, positional CSV, hybrid YAML-frontmatter-plus-markdown — that the Build Fractal ecosystem already uses in spec-kit-orc's `state-files.md`.
  - Ci-expert specifically notes: "a poorly written JSON Schema can still accept 'any valid JSON' just as easily as prose documentation. The enforcement gap exists in validation implementation, not format choice." Mandating formats does not actually close the gaming vector pragmatist worries about.

- **Status:** 3 of 4 against technology mandate. Pragmatist's position is reasoned but isolated.

### Dispute B — Deadline mechanism: fixed dates vs. self-declared transition plans

- **Devils-advocate's position** (non-negotiable in their disputes.md): require explicit transition plans where each product declares its compliance path and timeline, rather than accepting blanket retroactive deadlines. Rationale: fixed deadlines (even extended to 2026-12-01) create the same missed-deadline authority erosion risk for an amendment whose first contact with reality is enforcing dates against existing products.

- **Three-against-one** — pragmatist, persistence-expert (by implication), and ci-expert hold the line on fixed dates with consequences. Ci-expert is sharpest in disputes.md: "Enforcement without consequences creates compliance theater. The devils-advocate's approach allows products to declare indefinite 'transition plans' without accountability." Pragmatist proposes the differentiated compromise: 2026-12-01 for conversus (cross-product coordination complexity with spec-kit-orc adapter), 2026-09-01 for spec-kit-orc (self-contained reconciliation work).

- **Status:** 3 of 4 against self-declared timelines. Devils-advocate's position is reasoned but isolated.

A small wrinkle on Dispute B: pragmatist's own non-negotiable is the *extended* 2026-12-01 deadline for conversus, which is itself a fix to the spec-as-drafted (uniform 2026-09-01). So strictly speaking, neither pragmatist nor devils-advocate backs the spec's drafted Q3 verdict — both want changes, just in different directions.

## Per-question summary

### Q1 — Constitutional Inclusion Criteria gate

The spec § 8 claims the amendment passes universal applicability, mechanical verifiability, and non-redundance. QUESTION.md primed the four agents to attack each prong from different angles: pragmatist on cost-of-conformance, devils-advocate on whether the sub-clause is a new principle in disguise, persistence-expert on whether the schema mandate covers all surfaces, ci-expert on whether mechanical verifiability survives operational scrutiny.

- **Pragmatist:** Implicitly APPROVE-WITH-FIXES on Q1. Their revision_2.md disposition table treats the principle's adoption as a given and focuses recommendations on tightening the *mechanics* (schema format, deadlines, gate placement, drift detection). Their Recommendation 4 ("enforcement graduation" with warning periods) was withdrawn after ci-expert pointed out it defeats mechanical verifiability — that withdrawal effectively concedes the mechanical-verifiability prong of Q1. The remaining open recommendation (mandate specific formats) is a Q2 issue, not a Q1 challenge.

- **Devils-advocate:** Phase 1 attacked Q1 directly via "Split this into a separate Principle XXIX" (their original Recommendation 3). In revision_2.md they **withdrew** that recommendation, concluding "the attachment to Principle II (Stable Interfaces) is conceptually coherent — persistent state is indeed a type of interface that requires stability." This is the most consequential change in the deliberation: the strongest available Q1 BLOCK argument was withdrawn by the agent who raised it. They now hold APPROVE-WITH-FIXES on Q1, with all surviving challenges relocated to Q2 (gaming) and to deadline mechanism (Q3).

- **Persistence-expert:** APPROVE-WITH-FIXES on Q1. Their non-negotiables (bidirectional drift detection, schema coverage beyond field-based formats, consumer-side validation fixtures) are all engineering tightenings on the *mechanical-verifiability* prong. They do not challenge universal applicability or non-redundance.

- **Ci-expert:** APPROVE-WITH-FIXES on Q1 (inferred — they do not vote per-question explicitly, but their domain-expertise findings are uniformly fixes to mechanical-verifiability, not challenges to the Inclusion Criteria gate as a whole). Their three non-negotiables (pre-merge gate placement, bidirectional drift detection, binary pass/fail validation results) all sharpen mechanical verifiability rather than oppose it.

**Consensus shape for Q1:** APPROVE-WITH-FIXES, with the fixes being the engineering tightenings the four agents converged on (bidirectional drift detection, pre-merge gate placement, consumer-side validation fixtures, strengthened conformance wording, schema surface coverage). No agent argues BLOCK after Phase 4.

### Q2 — Schema-format flexibility

This is the question with the most surviving disagreement (Dispute A above).

- **Pragmatist:** REJECT-FLEXIBILITY (in disputes.md). Their non-negotiable: mandate JSON Schema, XSD, or Pydantic only. Without enforceable schema technologies, the discipline becomes "performative compliance theater rather than actual contract enforcement."

- **Devils-advocate:** APPROVE-WITH-FIXES on Q2. They reject the pragmatist's technology mandate and back the persistence-expert's wording fix: replace "deterministic conformance check" with "machine-executable validation with binary pass/fail result that verifies field presence, types, and value constraints, excluding prose descriptions, manual checklists, or subjective interpretation."

- **Persistence-expert:** APPROVE-WITH-FIXES on Q2 with the same fix language they authored. Explicitly opposes technology mandate on grounds it forces suboptimal tooling for non-field formats.

- **Ci-expert:** APPROVE-WITH-FIXES on Q2 with the same fix language. Notes pragmatist's technology mandate "conflates schema format with validation strength" — a poorly-written JSON Schema is as gameable as prose.

**Consensus shape for Q2:** 3-of-4 APPROVE-WITH-FIXES with the persistence-expert's wording fix; 1-of-4 (pragmatist) REJECT-FLEXIBILITY mandating JSON Schema / XSD / Pydantic. The numerical majority and the substantive technical argument both favor APPROVE-WITH-FIXES.

### Q3 — 2026-09-01 deadline realism

This is the question with the most movement during the deliberation, and where no agent backs the spec as drafted.

- **Pragmatist:** APPROVE-WITH-EXTENSION. Differentiated deadlines: 2026-12-01 for conversus (cross-product coordination with spec-kit-orc adapter), 2026-09-01 for spec-kit-orc (self-contained reconciliation).

- **Devils-advocate:** Reject the fixed-deadline mechanism entirely; require self-declared transition plans. Closest verdict in QUESTION.md taxonomy: REJECT-DEADLINE *as a mechanism*, while accepting that any agreed alternative would need product-specific dates.

- **Persistence-expert:** Did not address Q3 directly in revision_2.md or disputes.md as a verdict; their Recommendation 7 (cross-repository schema coordination notifications) and Recommendation 5 (SemVer versioning) imply tacit support for the pragmatist's "coordination complexity → extension" argument, but they do not vote per se. **Inferred from absence of objection:** APPROVE-WITH-EXTENSION compatible.

- **Ci-expert:** APPROVE-WITH-EXTENSION. Their modified Recommendation 4 explicitly adopts the pragmatist's differentiated timeline (2026-12-01 conversus, 2026-09-01 spec-kit-orc) and adds "missed deadlines must trigger concrete status changes, not indefinite transition plans" — explicitly rejecting devils-advocate's mechanism.

**Consensus shape for Q3:** 3-of-4 APPROVE-WITH-EXTENSION to the pragmatist's differentiated dates; 1-of-4 (devils-advocate) wants self-declared timelines as the mechanism. No agent backs the spec-as-drafted uniform 2026-09-01.

## Bottom-line synthesis

The deliberation produces a consistent picture:

- **Q1 passes** with engineering fixes. The most serious available Q1 attack (devils-advocate's "new principle in disguise") was raised, cross-reviewed, and **withdrawn by the originating agent**. This is the strongest possible signal that the Inclusion Criteria gate clears.

- **Q2 passes with fixes**, not flexibility-rejected. Three of four agents on technical grounds back wording tightening over technology mandate. The pragmatist's gaming concern is real but addressed by the persistence-expert's wording fix rather than by format restriction.

- **Q3 needs differentiated extension**. No agent backs the spec-as-drafted deadline. The pragmatist's differentiated dates (2026-12-01 conversus, 2026-09-01 spec-kit-orc) have 3-of-4 support; the devils-advocate's self-declared-timeline mechanism has 1-of-4 support and an explicit ci-expert rebuttal on accountability grounds.

The combined disposition per QUESTION.md taxonomy is: **Q1 APPROVE-WITH-FIXES + Q2 APPROVE-WITH-FIXES + Q3 APPROVE-WITH-EXTENSION** → proceed to self-consistency verification with the unanimous engineering fixes (bidirectional drift detection, pre-merge gates, consumer-side validation fixtures, strengthened conformance wording, schema surface coverage, differentiated deadlines) applied to produce spec v2.

The arbiter's ruling (`arbitration/resolution.md`) translates these synthesis findings into binding per-question verdicts and numbered conditions.
