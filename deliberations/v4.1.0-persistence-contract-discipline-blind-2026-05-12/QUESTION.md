# v4.1.0 Blind Verification — Three Questions (final stage)

This is **stage 3 of 3** in the v4.1.0 verification protocol per spec 067. The originating stage and self-consistency stage (including a rerun after DEMOTE-TO-TIER-2 disposition) both completed with PASS-variant verdicts. The spec is now at v4 (commit `8678bc7` on `spec/v4.1.0-persistence-contract-discipline`) with eight C-conditions from originating + seven Summary-of-Changes items from self-consistency + four D-conditions from rerun all applied.

**Blind verification's distinctive property** per spec 067: agents see the spec **without prior arbitration context**. No prior verdicts are loaded; no synthesis from earlier rounds is referenced. The four agents form their judgment independently of the chain-of-deliberation reasoning that produced v4.

The point of blindness is to catch what both prior stages might have missed by being too embedded in their own conversation. If the chain-of-deliberation reasoning is sound, blind verification confirms it. If the prior stages converged on a verdict because they were all looking at the problem from inside the same conversational frame, blind verification will surface the disconnect.

The agent composition is intentionally orthogonal to both prior stages:
- **None of the originating four** (pragmatist, devils-advocate, persistence-expert, ci-expert)
- **None of the self-consistency four** (strict-reader, purist, tier-coherence-auditor, precedent-auditor)
- All four agents have **no exposure to prior arbitrations** (empty `prior` in the deliberation config)

Default posture per the spec 067 methodology: agents form independent judgment. They are not asked to ratify or reject; they are asked to evaluate whether the spec, viewed fresh, holds up.

---

## Q1 — Implementability without external context

**Question:** Can a junior implementation engineer, reading ONLY spec v4 (no prior context, no governance documents beyond what the spec cites), correctly implement the persistence-contract discipline in a Build Fractal product?

This question tests whether the spec is **self-contained as prescriptive doctrine**. A constitutional principle must be implementable by readers who don't have access to its deliberation history. If the spec only makes sense to someone who watched the v1→v4 progression, it's not actually a principle — it's a record of an argument.

Examine:
- **Sub-clause 1 (declared schema with version field).** Is the requirement actionable from the spec text alone? Could an engineer determine what counts as a "schema" without further guidance? Is `schema_version` field format specified or implied?
- **Sub-clause 2 (mechanical CI enforcement, PR-required).** Is the CI gate placement unambiguous? Are the conformance-check requirements (machine-executable, binary pass/fail, etc. per C5+C6) actionable, or do they require interpretation?
- **Sub-clause 3 (versioning bump procedure).** Does "documented bump procedure" specify enough that two engineers would independently produce comparable procedures?
- **Sub-clause 4 (cross-product CONSUMER-CONTRACT.md + consumer-side fixtures).** Is the consumer-side fixture requirement (C3) implementable from the spec alone? What goes in the fixture? Where does it live?
- **Sub-clause 5 (declaration scope; display text is not stable by default).** Is the "explicit declaration" mechanism specified, or only the consequence of NOT declaring?

If sub-clauses require external context to implement, list specifically what context is missing.

Output: per-sub-clause finding with implementability assessment; verdict (IMPLEMENTABLE / IMPLEMENTABLE-WITH-CLARIFICATIONS / NOT-IMPLEMENTABLE-AS-WRITTEN).

---

## Q2 — Worst-case operational impact

**Question:** If spec v4 ratifies as drafted, what is the worst-case operational impact across the conversus suite over the next 12 months?

This question tests whether the spec's **operational reality** has been adequately considered. Constitutional principles can sound right but create disproportionate cost in practice. The risk auditor's role is to surface the worst plausible operational consequence and judge whether the spec's value justifies it.

Examine:
- **C7 universal deadline (2026-12-01).** What happens if one of the three target products misses? Does C8 ("Remediation-Blocked" status) handle this cleanly, or does it create a cascade where one product's miss triggers consumer-product failures (e.g., spec-kit-orc consuming conversus-oss surfaces)?
- **CI gate enforcement burden.** Three products × three test fixtures (per C6) × bidirectional drift detection (per C1) — what's the cumulative engineering cost? Is it plausibly delivered by 2026-12-01 given the conversus team's current capacity (deducible from CHANGELOG.md velocity)?
- **Cross-product CONSUMER-CONTRACT.md introduction.** Currently no Build Fractal product carries this file. The amendment mandates one per product. What's the migration friction? Are there products that would need to retroactively declare consumer contracts for surfaces they didn't realize were being consumed externally?
- **Forward-sibling fit (D2).** New conversus-* siblings joining post-ratification are governed by their admission process per D2. But the admission process itself probably doesn't yet specify how the persistence-discipline applies to a joining product. Is there a gap?
- **Procedural-violation rollback precedent.** D4 establishes that "agent convergence on substance cannot cure procedural violations." This applies retroactively to ANY prior amendment that invoked override-with-rationale outside blind verification. Audit history: are there other amendments that need retroactive correction now?

Output: per-axis worst-case finding; verdict (LOW-RISK / MODERATE-RISK-MANAGEABLE / HIGH-RISK-RECONSIDER).

---

## Q3 — Does the spec stand as constitutional doctrine?

**Question:** Does spec v4, read as a constitutional principle by an external scholar with knowledge of constitutional governance but no Build Fractal context, hold up?

This question tests whether the principle has **external doctrinal coherence**. A principle should make sense to a reader without insider context. If it reads as a record of internal compromises rather than a coherent prescriptive doctrine, that's a signal it ratifies an argument rather than establishing a principle.

Examine:
- **Five-point structure.** Does the principle's structure (schema declaration / mechanical enforcement / versioning / consumer contracts / declaration scope) hang together as a doctrinal unit, or does it read as a list of separate concerns clustered under one banner?
- **Universality at Tier 2.** Tier 2 = "Conversus Suite." The principle applies to all conversus-family products. Is the universality claim doctrinally coherent — does the principle actually generalize across conversus-* siblings as drafted, or does it rely on conversus-oss + spec-kit-orc specifics that would need reinterpretation for other products?
- **Override-precedent scope restriction (§ 11).** Does § 11 read as a separate procedural doctrine bolted onto the persistence-discipline principle, or as integral to it? If separate, should it be its own amendment?
- **Compound constitutional debt (§ 12).** Is the acknowledgment of compound debt doctrinally appropriate, or does it read as performative self-flagellation that future amendments would not be expected to imitate?
- **Comparison to established constitutional doctrines.** A reader familiar with software engineering constitutional patterns (e.g., the Linux Kernel's stable-ABI rules, Rust's stability guarantees, SemVer's principles) should find spec v4 recognizable as the same kind of artifact. Does it?

Output: per-axis finding; verdict (HOLDS-AS-DOCTRINE / PARTIALLY-COHERENT / READS-AS-COMPROMISE-RECORD).

---

## Arbiter ruling format

For each question:

**Q1 (Implementability):**
- IMPLEMENTABLE — junior engineer could implement from spec alone.
- IMPLEMENTABLE-WITH-CLARIFICATIONS — specify E-conditions for spec v5 (small wording fixes).
- NOT-IMPLEMENTABLE-AS-WRITTEN — substantive gaps; specify what's missing.

**Q2 (Worst-case operational impact):**
- LOW-RISK — operational impact within tolerance.
- MODERATE-RISK-MANAGEABLE — risks identified but C-conditions adequately mitigate.
- HIGH-RISK-RECONSIDER — risks exceed value; recommend further mitigation or scope reduction.

**Q3 (External doctrinal coherence):**
- HOLDS-AS-DOCTRINE — spec stands as coherent constitutional principle.
- PARTIALLY-COHERENT — specify E-conditions for tightening doctrinal framing.
- READS-AS-COMPROMISE-RECORD — spec reads as argument record; recommend doctrinal rewrite.

Combined disposition determines ratification readiness:

- **Q1+Q2+Q3 all PASS-variant: PROCEED TO RATIFICATION.** Apply any E-conditions to produce spec v5; spec v5 (or v4 if no E-conditions) is ratified via SIR + governance log + spec status entries.
- Any FAIL: spec returns to v4 review; ratification is held until the FAIL is addressed.
- Multiple PASS-WITH-EDITS: spec v5 produced; the cumulative E-conditions are applied before ratification.

For each ruling, cite specific text from spec v4 (§ section number) and from Tier 1 / Tier 2 CONSTITUTION.md where relevant.

Conclude with three ruling lines, exactly:
- "Q1 RULING: <verdict> — <one-line rationale>"
- "Q2 RULING: <verdict> — <one-line rationale>"
- "Q3 RULING: <verdict> — <one-line rationale>"

This is the final verification before ratification. If all three pass, the v4.1.0 amendment is ratified at Tier 2 of the conversus suite.
