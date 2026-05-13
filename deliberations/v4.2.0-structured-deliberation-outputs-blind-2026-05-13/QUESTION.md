# v4.2.0 Blind Verification — Three Questions (final stage)

This is **stage 3 of 3** in the v4.2.0 verification protocol per spec 067. The originating stage and self-consistency stage (including a rerun after Q3 FAIL-CONTRADICTION) both completed with PASS-variant verdicts. The spec is now at **v4** with C1-C10 (originating) + D1-D15 (self-consistency) + E1-E4 (self-consistency rerun) applied.

**Blind verification's distinctive property** per spec 067: agents see the spec **without prior arbitration context**. No prior verdicts are loaded; no synthesis from earlier rounds is referenced. The four agents form their judgment independently of the chain-of-deliberation reasoning that produced v4.

The point of blindness is to catch what both prior stages might have missed by being too embedded in their own conversation. If the chain-of-deliberation reasoning is sound, blind verification confirms it. If the prior stages converged on a verdict because they were all looking at the problem from inside the same conversational frame, blind verification will surface the disconnect.

The agent composition is intentionally orthogonal to both prior stages:
- **None of the originating four** (engineer, schema-design-expert, adapter-consumer, devils-advocate)
- **None of the self-consistency four** (strict-reader, purist, principle-xxviii-fit-auditor, recursion-precedent-auditor)
- All four blind agents have **no exposure to prior arbitrations** (empty `prior` in the deliberation config)

Default posture per the spec 067 methodology: agents form independent judgment. They are not asked to ratify or reject; they are asked to evaluate whether the spec, viewed fresh, holds up.

---

## Q1 — Implementability without external context

**Question:** Can an implementation engineer, reading ONLY spec v4 (no prior context, no governance documents beyond what the spec cites), correctly implement structured deliberation outputs in conversus-oss?

This question tests whether the spec is **self-contained as prescriptive doctrine**. A Tier 3 component-tier discipline must be implementable by readers who don't have access to its deliberation history. If the spec only makes sense to someone who watched the v1→v4 progression, it's not actually a Component-tier discipline — it's a record of an argument.

Examine:
- **§ 4 schema definitions.** Are the JSON Schema field requirements actionable from the spec text alone? Could an engineer determine field types, required-vs-optional, and value constraints for each of the six output types (review / cross-review / revision / disputes / synthesis / arbitration) without further guidance?
- **§ 5.1 non-blocking validator.** The validator MUST NOT raise or abort per Principle V. Is the warning-emission mechanism (event stream + sidecar `.validation-warnings.json`) specified concretely enough that two engineers would independently produce comparable implementations? Are the warning payload fields enumerated?
- **§ 5.3 fixture scope.** v3+v4 mandate four fixture types (conformant, missing-required, wrong-type, plus a fourth per D14). Is the fourth fixture type specified, or only the consequence of NOT having it? Are fixture locations declared?
- **§ 5.4 PR-time CI gate enforcement.** The CI gate prevents merging non-conformant code. Is the gate scope (which paths/files trigger it) unambiguous? Does v4's E1 authority citation (Tier 1 Principle II + Tier 2 Principle XXVIII sub-clause 2) make the gate's authority operational, or just declared?
- **§ 5.4 drift detection.** Bidirectional drift detection (D12) + schema-version-bump CI detection (D15). Are the detection rules implementable, or do they require interpretation?
- **§ 6.1 schema location.** D9 declares the schema location in CONFORMANCE.md. D10 requires both README.md AND CLAUDE.md links. Are these link conventions specified (link text, anchor format)?
- **§ 7.1 CONSUMER-CONTRACT.md content spec.** D11 mandates a six-section structure. Are the six sections enumerated with enough detail that an engineer could produce one without reference to an example?
- **§ 9.1 temporal-constraint exemption + E2 technical condition.** Is the technical condition (no JSON Schema exists AND ratification stands schema up) verifiable mechanically? Could an engineer determine, for a future amendment, whether the exemption applies?

If sub-sections require external context to implement, list specifically what context is missing.

Output: per-section finding with implementability assessment; verdict (IMPLEMENTABLE / IMPLEMENTABLE-WITH-CLARIFICATIONS / NOT-IMPLEMENTABLE-AS-WRITTEN).

---

## Q2 — Worst-case operational impact

**Question:** If spec v4 ratifies as drafted, what is the worst-case operational impact across conversus-oss and the orchestrator over the next 12 months?

This question tests whether the spec's **operational reality** has been adequately considered. Tier 3 component-tier disciplines can sound right but create disproportionate cost in practice. The risk auditor's role is to surface the worst plausible operational consequence and judge whether the spec's value justifies it.

Examine:
- **Markdown deprecation cliff (2026-12-01).** If conversus-oss misses the cliff date, what happens to consumers (orchestrator's spec-kit adapter, conversus-enhanced if applicable)? Does the spec define a graceful degradation, or does it implicitly assume the cliff is met?
- **Validator runtime budget.** § 5 mandates a <100ms validation budget. Is this budget realistic across all six output types at the sizes seen in actual deliberations (some synthesis outputs exceed 100K chars)? What happens if the budget is exceeded — does the warning still emit, or does the validator skip?
- **Schema iteration cost.** Starting at `1.0.0-rc.1` (C10) with a 30-day-clean-operation bump to 1.0.0. What's the cost of schema iteration during the rc window? Are field renames possible, or does SemVer policy lock them out immediately?
- **Adapter migration in orchestrator.** Orchestrator's spec-kit adapter currently grep-parses markdown. Spec v4 implicitly forces migration to JSON parsing. What's the worst-case adapter breakage during the transition? Is parallel-format support (markdown AND JSON) feasible in the producer (conversus-oss), or is it a hard cut?
- **Three fixture types × six modes = 18 fixtures.** The fixture-coverage cost (per D14 + XXVIII C6) is per-mode-per-fixture-type. Plus a fourth fixture type. Total fixture cost: 24+ fixtures. Is the engineering team's capacity sufficient to author 24 fixtures by the cliff date?
- **Forward-precedent risk from temporal-constraint exemption.** § 9.1 establishes a temporal-constraint exemption (bootstrap paradox). E2 tightens it to schema-substrate-standup only. E4 mandates precedent-citation in future invocations. Is this containment sufficient, or could a future amendment creatively re-frame its case as "schema-substrate-standup-adjacent"?
- **Engine bug exposure during transition.** During the markdown→JSON transition, the Phase 6 `disputes_remain` trigger grep-mismatch bug (which has hit 4× in v4.1.0+v4.2.0 deliberations) gets worse, not better — synthesis is still in markdown until v4.2.0 implements. Does v4 acknowledge this self-referential risk, or does it assume implementation begins on a clean slate?

Output: per-axis worst-case finding; verdict (LOW-RISK / MODERATE-RISK-MANAGEABLE / HIGH-RISK-RECONSIDER).

---

## Q3 — External doctrinal coherence

**Question:** Does spec v4, read as a Tier 3 component-tier discipline by an external scholar with software engineering governance context but no Build Fractal context, hold up?

This question tests whether the discipline has **external doctrinal coherence**. A component-tier discipline should make sense to a reader without insider context. If it reads as a record of internal compromises rather than a coherent prescriptive doctrine, that's a signal it ratifies an argument rather than establishing discipline.

Examine:
- **JSON Schema choice (C1).** v2 flipped from XSD to JSON Schema. Does the rationale for the choice (developer ergonomics, tooling ecosystem, lower migration friction) read as principled, or as a pragmatic concession? Compare to other governance choices in the same family (e.g., OpenAPI's JSON Schema dependency, GitHub Actions' YAML choice).
- **Non-blocking validator design (D1, § 5.1).** Principle V mandates "Malformed output is better than no output." v3 reversed v2's blocking validation per this principle. Does the resulting design — warning emission + sidecar file + PR-time CI gate — read as a coherent enforcement model, or as three separate mechanisms patched together?
- **Bootstrap-paradox temporal-constraint precedent (§ 9.1).** v4 establishes a new precedent: a spec can be temporarily exempt from a principle whose substrate it is ratifying. Is this doctrinally coherent (a logical impossibility, hence acceptable framing), or does it read as a procedural escape hatch dressed in temporal-logic clothing? Compare to Russell's paradox / set-theoretic stratification, or to constitutional law's "necessity doctrine."
- **Anti-precedent containment language (D5 + E2).** § 9.1 D5 prohibits "adjacent," "similar," and "schema-touching" framings. E2 adds a technical condition (no JSON Schema exists AND ratification stands schema up). Does the layered containment read as principled (uniform application), or as ad-hoc fence-building?
- **Cross-tier weakening assessment matrix (E3, § 9.2).** v4's E3 replaces conclusory prose with a systematic verification matrix. Does the matrix read as a doctrinal verification mechanism, or as a checkbox exercise that future amendments would not be expected to imitate?
- **Comparison to established constitutional doctrines.** A reader familiar with software governance patterns (e.g., the Linux Kernel's stable-ABI rules, Rust's RFC stability process, the Python language reference's typing PEP cascade) should find spec v4 recognizable. Does it look more disciplined, less disciplined, or equivalent?

Output: per-axis finding; verdict (HOLDS-AS-DOCTRINE / PARTIALLY-COHERENT / READS-AS-COMPROMISE-RECORD).

---

## Arbiter ruling format

For each question:

**Q1 (Implementability):**
- IMPLEMENTABLE — engineer could implement from spec alone.
- IMPLEMENTABLE-WITH-CLARIFICATIONS — specify F-conditions for spec v5 (small wording fixes).
- NOT-IMPLEMENTABLE-AS-WRITTEN — substantive gaps; specify what's missing.

**Q2 (Worst-case operational impact):**
- LOW-RISK — operational impact within tolerance.
- MODERATE-RISK-MANAGEABLE — risks identified but C/D/E-conditions adequately mitigate.
- HIGH-RISK-RECONSIDER — risks exceed value; recommend further mitigation or scope reduction.

**Q3 (External doctrinal coherence):**
- HOLDS-AS-DOCTRINE — spec stands as coherent component-tier discipline.
- PARTIALLY-COHERENT — specify F-conditions for tightening doctrinal framing.
- READS-AS-COMPROMISE-RECORD — spec reads as argument record; recommend doctrinal rewrite.

Combined disposition determines ratification readiness:

- **Q1+Q2+Q3 all PASS-variant: PROCEED TO RATIFICATION.** Apply any F-conditions to produce spec v5; spec v5 (or v4 if no F-conditions) is ratified via SIR + governance log + spec status entries.
- Any FAIL: spec returns to v4 review; ratification is held until the FAIL is addressed.
- Multiple PASS-WITH-EDITS: spec v5 produced; the cumulative F-conditions are applied before ratification.

For each ruling, cite specific text from spec v4 (§ section number) and from Tier 1 / Tier 2 CONSTITUTION.md where relevant.

Conclude with three ruling lines, exactly:
- "Q1 RULING: <verdict> — <one-line rationale>"
- "Q2 RULING: <verdict> — <one-line rationale>"
- "Q3 RULING: <verdict> — <one-line rationale>"

This is the final verification before ratification. If all three pass, the v4.2.0 amendment is ratified at Tier 3 of conversus-oss.
