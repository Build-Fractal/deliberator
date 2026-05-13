# Arbitration Resolution — v4.2.0 Self-Consistency Verification (Manual)

**Stage:** 2 of 3 (self-consistency). Spec v2 (`edf80b4`) under review.
**Agents:** strict-reader, purist, principle-xxviii-fit-auditor, recursion-precedent-auditor.
**Synthesis:** `summary/final.md` (Phase 5 — written by neutral synthesizer).
**Arbiter:** Manual (Phase 6 did not fire — see Process Note).

---

## Process Note

Phase 6 (arbitration) did **not fire automatically** for this deliberation. This is the **THIRD consecutive deliberation in this session** to reproduce the same engine failure mode:

1. v4.1.0 blind verification — Phase 6 missed; manual arbitration produced.
2. v4.2.0 originating (`6478ac7`) — Phase 6 missed; manual arbitration produced (the verdict that authored C1-C10 + the RECURSION-EXEMPTED ruling now under review here).
3. v4.2.0 self-consistency (this deliberation) — Phase 6 missed; this manual arbitration produced.

The root cause is exactly what v4.2.0 § 12 OQ identifies and what v2 § 4.4 + § 4.6 fixes: the engine's `disputes_remain` trigger does a **regex grep against synthesis prose** for terminology like "disputes remain" or specific disputed-claim markup. The Phase 5 synthesis here uses the headings `## Dangerous Contradictions Found`, `## Systemic Contradictions`, `## Remaining Disputes`, and `## Convergence Achieved`, plus explicit per-agent disputes documents — but the grep trigger does not pattern-match the synthesis's actual disputes-terminology. The arbiter dispatch never receives the work item.

**Pedagogical observation (consistent with v4.2.0 originating's verdict):** every deliberation that purports to verify v4.2.0's structural-detection thesis is *itself reproducing the bug v4.2.0 is fixing*. This is not coincidence. It is real-time evidence — now triply replicated — that v4.2.0's core engineering claim is correct: **structural triggers grounded in a typed schema would eliminate this class of failure, and prose-based triggers cannot.** The agents' Phase 5 synthesis flagged **explicit constitutional violations and live disputes**, including a unanimously-identified Principle V violation, and the engine still did not route the work to an arbiter. The bug is the case for the spec.

Note on inputs: per protocol, self-consistency does not load the originating arbiter verdict during agent phases. The arbiter (this document) does load originating's verdict — `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` — because self-consistency is checking whether the C1-C10-applied spec v2 still holds up under fresh-perspective scrutiny, which requires knowing what originating ruled.

---

## Decision Framework

This arbiter rules under four binding constraints:

1. **Tier 2 Principle V — Observable Deliberation** (CONSTITUTION.md L70-80). Verbatim:
   > "Output validation (e.g., Phase 6 heading checks) emits **warnings** for malformed output but **does NOT block file writes**. Malformed output is better than no output."

2. **Tier 2 cross-tier weakening prohibition** (CONSTITUTION.md L649-685). Specifically L685: *"A component-tier amendment cannot grant relief from a Tier 2 principle."* And L653 criterion (i) — implicit relief without formal Relief pathway invocation is forbidden.

3. **v4.1.0 self-consistency override-precedent ruling** (`v4.1.0-...-self-consistency-rerun-2026-05-12/arbitration/resolution.md` L117-121). That ruling adopted the **temporal-vs-membership-universality** distinction over strict uniformity for product deadlines. The structural pattern: an accommodation was permitted **only because** strict reading would create *logical impossibility* (retroactive obligations on non-existent products violating Principle VII's deterministic orchestration requirement). The override required documentation in three places (SIR + governance log + spec status). It was **not** a general license to carve out exceptions from Tier 2 principles.

4. **Default posture: defend the status quo.** Ratification bias is high; the originating already approved with C1-C10 applied. The arbiter does not move spec v2 forward unless v2 actually satisfies the principles it claims to implement *without contradicting other ratified principles*.

---

## Per-Question Rulings

### Q1 (Principle XXVIII fit) — PASS-WITH-CLARIFICATIONS

**Primary input:** principle-xxviii-fit-auditor's revision_2 + the converged findings in the Phase 5 synthesis.

The principle-xxviii-fit-auditor walked through each XXVIII sub-clause. Findings:

- **Sub-clause 1 (declared schema, discoverable location):** PARTIALLY-SATISFIES. v2 § 4.1-4.7 declares schemas at `engine/schema/v1/*.schema.json` with `$id` and `schema_version`. But **the location is not declared in `conversus-oss/CONFORMANCE.md`** — and sub-clause 1 textually requires (L505-510) that "suite-convention directories be documented in the repo's CONFORMANCE.md" and linked from "**BOTH** the repo's top-level README.md AND its CLAUDE.md." This is a **literal textual gap**. **All four agents** converged on this in the synthesis (synthesis P1 row 2, unanimous). The fit-auditor, strict-reader, and recursion-precedent-auditor all cite L508-510 verbatim. The purist did not challenge.

- **Sub-clause 2 (mechanical CI enforcement, PR-required, machine-executable conformance):** PARTIALLY-SATISFIES. v2 § 5.1 specifies `engine/schema_validator.py` with `jsonschema.Draft202012Validator`, and § 5.4 adds the PR-required CI gate. Mechanical enforcement IS present. However, sub-clause 2 also requires (constitutional text per the fit-auditor's citation) bidirectional drift detection: "any change to the schema itself MUST trigger CI verification that existing producer code still emits conformant artifacts under the new schema." v2 § 5.4 only specifies forward validation (artifacts → schema). **Three agents** (fit-auditor surviving Rec 2 modified, strict-reader new Rec, recursion-precedent-auditor implicit) flagged this gap.

- **Sub-clause 3 (versioning bump procedure):** SATISFIES. § 4.8 specifies SemVer with consumer-impact rule per C8; initial `1.0.0-rc.1` per C10 with bump to `1.0.0` after 30 days clean operation. The purist disputes rc.1-vs-1.0.0 (purist surviving Rec 2), but this is a stylistic preference, not a sub-clause 3 violation — sub-clause 3 permits "SemVer or documented alternative" and rc.1 is SemVer-compliant pre-release notation. Purist's position does not survive against XXVIII text. **Minor gap:** the purist's other dispute on **schema advancement authority** (who decides the rc → 1.0.0 bump?) is a real specification hole that v3 should close.

- **Sub-clause 4 (cross-product CONSUMER-CONTRACT.md):** SATISFIES at the structural level. v2 § 7 specifies CONSUMER-CONTRACT.md authoring for conversus-oss + orchestrator integration. No agent disputed this structurally.

- **Sub-clause 5 (declaration scope — explicit declaration naming surface + stability guarantee):** PARTIALLY-SATISFIES. The fit-auditor's surviving Rec 3, **elevated to P1 by cross-review consensus**, is that v2's CONSUMER-CONTRACT.md content specification is incomplete relative to sub-clause 5's explicit text mandate ("naming the specific display-text surface... and stating the stability guarantee" — CONSTITUTION.md L572-577). v2 needs to spell out *what surfaces* are declared stable and *under what guarantee*, not just gesture at the document's existence.

**Q1 verdict: PASS-WITH-CLARIFICATIONS.** The five sub-clauses are structurally addressed, but three gaps (CONFORMANCE.md location declaration, README+CLAUDE linking, CONSUMER-CONTRACT.md content specification) are *literal textual gaps* in XXVIII satisfaction. These are remediable in v3 via D-conditions; they are not a "FAIL-INCOMPLETE-IMPLEMENTATION" because the architecture is right and the fixes are documentation-shape closing, not structural redesign.

### Q2 (Tier 3 + recursion-exempted coherence) — PASS-WITH-CLARIFICATIONS

**Primary input:** recursion-precedent-auditor's revision_2 + purist's revision_2.

#### Tier 3 stability
The originating Q3 ruled TIER-3-CONFIRMED because only conversus-oss currently produces deliberation outputs (evidence base argues for Component tier, not Suite tier). v2 § 11 implementation order does not specify a **pattern-promotion pathway** for the case where a future conversus-* sibling (e.g., a hypothetical `conversus-investigations`) begins producing deliberation-like artifacts. The purist (surviving Rec 7) flags this gap and it is real. However, this is a **forward-amendment friction concern**, not a present coherence failure. Tier 3 placement IS the lowest-tier-supported by evidence today (per the same demote-when-evidence-thin posture v4.1.0 used). D-condition for v3: add a one-paragraph forward-promotion clause (or explicit reference to GOVERNANCE.md's pattern-promotion pathway if defined) so this is captured.

#### RECURSION-EXEMPTED as precedent — **load-bearing question**

The orchestrator's prompt asks: *"Does the recursion-exempted ruling structurally resemble the v4.1.0 override-with-rationale stretch that v4.1.0 self-consistency rejected? If yes, this Q2 should likely FAIL or require precedent-narrowing."*

Three of four agents converged on **temporal-constraint framing is superior to exemption language** (recursion-precedent-auditor Rec 1 modified, purist Rec 1 modified, strict-reader Rec 4 modified). The recursion-precedent-auditor goes further and flags this as a **potential cross-tier weakening violation** in their new Rec 3 ("Eliminate performative validation in favor of mechanical enforcement"): the exemption grants relief from XXVIII's enforcement requirement on v4.2.0's own verification artifacts without invoking the formal Relief pathway documented in COMPLIANCE.md Part VI. They cite cross-tier weakening criterion (i) — implicit relief.

**Structural comparison to v4.1.0's override-with-rationale ruling:**

| Axis | v4.1.0 temporal override (ratified) | v4.2.0 RECURSION-EXEMPTED (originating Q3) |
|---|---|---|
| Logical impossibility of strict reading | YES — retroactive deadlines on non-existent products literally cannot be satisfied (violates Principle VII deterministic orchestration) | YES — JSON validation cannot exist before JSON schemas are created (bootstrap paradox; purist Rec 1 dispute makes this case) |
| Accommodation grounded in unrepeatable historical sequencing | YES — temporal-vs-membership universality distinction | YES, *if* reframed as temporal constraint ("predates JSON schema availability by construction"); NO, if framed as exemption that could be re-invoked |
| Override documented in 3+ places | YES (SIR + governance log + spec status) | PARTIAL — § 9.1 + § 12 OQ5 + § 13 in spec; no governance log entry in CONSTITUTION-history.md |
| Risk of slippery precedent | LOW — temporal scope is unrepeatable | MEDIUM-HIGH — "we're amending the meta-schema, exempt from the schema we're amending" is a *re-invocable pattern* unless explicitly contained |
| Invokes formal Relief pathway? | NOT NEEDED — distinction is not relief, it's scope clarification | NOT INVOKED — and three agents (purist new Rec, recursion-precedent-auditor new Rec, fit-auditor new Rec 2) flag this as a cross-tier weakening risk |

**Assessment:** The v4.2.0 ruling is structurally **similar but not identical** to v4.1.0's override. The key distinguishing feature in v4.1.0 was that the temporal-vs-membership distinction reframed the question so that strict reading was *logically impossible* (not merely inconvenient), which made it not really a "relief" at all — it was scope clarification. If v4.2.0 reframes via **temporal-constraint language** as the three agents recommend ("v4.2.0 verification outputs predate JSON schema availability by construction; JSON mandatory for specs ratified after v4.2.0 implementation completion"), then v4.2.0's accommodation acquires the same logical-impossibility character as v4.1.0's and the precedent stretch is contained.

If v4.2.0 keeps the **exemption language** as drafted in v2 § 9.1 ("RECURSION-EXEMPTED"), the accommodation reads as discretionary relief from XXVIII's enforcement — which IS the structural pattern of the v4.1.0 override stretch that v4.1.0 self-consistency rejected when applied uniformly. Anti-precedent language alone (purist Rec 5 modified, all four agents converged on "anti-precedent language necessity") is necessary but not sufficient; the framing itself must shift from exemption to temporal-constraint.

The recursion-precedent-auditor's strongest claim — that v2 should invoke the formal Relief pathway per COMPLIANCE.md Part VI rather than ad-hoc temporal constraint — is **rejected**. Relief pathway is for ongoing structural inability to satisfy a principle; v4.2.0's situation is a one-time bootstrap paradox at the very moment of standing up the schema infrastructure. Bootstrap paradoxes call for temporal-constraint framing with anti-precedent containment, not Relief invocation, because Relief invocation creates the audit trail of *ongoing* non-compliance that does not match the facts here.

#### Markdown deprecation cliff (2026-12-01)
Purist's surviving Rec 4 (Address Temporal Ratification Hazard) and the constitutional cliff date alignment concern: if v4.2.0 ratifies *after* 2026-12-01, the cliff has already passed. Spec v2 § 11 does not specify what happens in that case. D-condition for v3: add explicit "if ratification occurs after the universal cliff date, T4 is treated as in-effect at ratification, with T1-T3 collapsed" or equivalent fallback.

#### Schema versioning interaction with C10 (`1.0.0-rc.1`)
Interaction is clean. rc.1 is SemVer pre-release notation; sub-clause 3's "documented total ordering" requirement is satisfied by SemVer's own ordering rules (rc.N < release). The schema-advancement-authority hole (purist Rec 6) is a separate D-condition.

**Q2 verdict: PASS-WITH-CLARIFICATIONS.** No RECURSION-PRECEDENT-FAIL — *if* v3 incorporates D-conditions (temporal-constraint reframing + anti-precedent language + cross-tier weakening assessment in § 9.2). No TIER-2-PROMOTE-RECOMMENDED — Tier 3 evidence base is intact; promotion pathway addition is a clarification, not tier instability.

### Q3 (Internal contradiction check) — FAIL-CONTRADICTION

**Primary input:** strict-reader's revision_2, plus unanimous convergence in Phase 5 synthesis (all four agents independently identified the same violation).

This is the load-bearing finding of the self-consistency stage. **All four agents** (strict-reader modified Rec 1, principle-xxviii-fit-auditor new Rec 1, purist new Rec 1, recursion-precedent-auditor new Rec 1) independently identified that **v2 § 5.1 directly contradicts Tier 2 Principle V**.

The text of the contradiction:

> **Tier 2 Principle V (CONSTITUTION.md L76-78):** "Output validation (e.g., Phase 6 heading checks) emits warnings for malformed output but **does NOT block file writes. Malformed output is better than no output.**"

> **v2 § 5.1 L527:** "Failure raises `SchemaViolation` carrying an array of `ValidatorError` objects conformant to § 4.9. The engine logs the error array to the deliberation event stream and **aborts the phase (does not write the malformed file).**"

These are not in tension; they are direct negations. Principle V says "writes malformed files, emits warnings." v2 says "aborts the phase, does not write the malformed file."

**This is a Q3 contradiction in the literal sense the question asks about.** It is not a "PASS-WITH-CLARIFICATIONS where we tweak a phrase" — it is the spec under review actively violating a ratified Tier 2 principle that is one of the constitutional pillars under which the entire deliberation engine operates.

**Compounded by cross-tier weakening prohibition:** CONSTITUTION.md L685 — "A component-tier amendment cannot grant relief from a Tier 2 principle." Spec v4.2.0 is component-tier (per Q3 originating TIER-3-CONFIRMED). v2's blocking-validation language grants implicit relief from Principle V's "does NOT block file writes" guarantee, *without invoking the formal Relief pathway*. This is cross-tier weakening criterion (i): implicit relief outside the formal Relief pathway. The fit-auditor's new Rec 2 and recursion-precedent-auditor's modified Rec 4 both elevate this to P1.

**Default-defend-status-quo posture compels this verdict.** Principle V is ratified. v4.2.0 is the candidate. When a candidate spec contradicts a ratified principle, the candidate yields. The remediation is straightforward — **non-blocking warning-based validation** (write the malformed file, log the error array to the event stream, emit a prominent warning, fail the CI gate at PR-time but never at engine-write-time). This was the converged technical solution all four agents endorsed (Phase 5 synthesis "High-Confidence Agreements" item 1).

The fit-auditor also flags a secondary contradiction in v2 § 9.1: a **Principle II misattribution** in the RECURSION-EXEMPTED justification. Two agents (strict-reader new Rec, recursion-precedent-auditor modified Rec 3) converged that Principle II governs interface stability for technical contracts (dispatch tables, template variables, schema-versioned wire formats), not procedural-methodology accommodations for verification cycles. Citing Principle II to ground RECURSION-EXEMPTED is doctrinally invalid. This is a Q3 finding too — citing a principle to justify a clause without satisfying that principle's actual scope is itself a form of internal contradiction. D-condition for v3: strike the Principle II citation in § 9.1; replace with the temporal-constraint rationale.

**Q3 verdict: FAIL-CONTRADICTION.** The Principle V blocking-validation contradiction must be resolved before v3 can pass self-consistency. Re-run this stage against v3 once the fix is applied.

---

## Notable Dispute Resolutions

**Q2 — recursion-precedent-auditor vs. the three temporal-constraint agents on Relief pathway.** The recursion-precedent-auditor argued (their remaining dispute 1 + new Rec 3) that the formal Relief pathway should be invoked rather than ad-hoc temporal constraint. The other three agents accepted temporal-constraint framing with anti-precedent language as sufficient. **Arbiter sides with the three-agent majority.** Relief pathway is structurally for ongoing inability to satisfy a principle; v4.2.0's situation is a one-time bootstrap, and temporal-constraint framing with explicit anti-precedent containment is the correct shape. The recursion-precedent-auditor's contribution is preserved by requiring v3 § 9.2 to *explicitly assess the exemption against cross-tier weakening criteria* (their modified Rec 4) — assessing the criteria is required even if Relief pathway is not invoked.

**Q2 — purist vs. recursion-precedent-auditor on sequencing (eliminate-first vs. temporal-constraint-only).** purist's remaining dispute 1 argues that elimination of RECURSION-EXEMPTED is a predetermined impossibility (bootstrap paradox) and "attempt elimination first" wastes effort on a logical impossibility. recursion-precedent-auditor argues "attempt elimination first, fall back to temporal constraint." **Arbiter sides with purist on sequencing economy** — bootstrap paradox is categorical, not technical, and elimination-first is wheel-spinning. v3 goes directly to temporal-constraint framing. (This is also the cheaper path; recursion-precedent-auditor's own remaining-dispute concession in their Flexibility item 1 accepts this.)

**Q1 — fit-auditor vs. purist on performance budget constitutional status.** Both ended up converged: <100ms is an implementation choice, not a constitutional mandate. strict-reader's remaining dispute 1 wants the constitutional-language stripped from § 5.1 explicitly. **Arbiter agrees** — D-condition for v3: rephrase § 5.1's <100ms language as implementation discipline ("the engine MUST validate quickly; <100ms is the operational target, not a constitutional mandate"). This is a minor wording fix, not a Q1 fail.

**Q3 — strict-reader's remaining dispute on cross-tier weakening assessment as prerequisite vs. parallel.** strict-reader argues cross-tier weakening assessment must precede any other constitutional fix because if the exemption framework is constitutionally invalid, all temporal-constraint work is wasted. recursion-precedent-auditor agrees in their remaining dispute 2. The other two agents want parallel resolution. **Arbiter takes a middle path:** the cross-tier weakening assessment (D-condition below) IS a Q2 prerequisite for v3 ratification, but it does not block the Q3 Principle V fix from being applied in parallel — those are independent edits. Sequential gating is on *ratification*, not on *editing*.

---

## Combined Disposition

**Q3 returns FAIL-CONTRADICTION.** Per protocol ("Any FAIL: spec returns to v2 review"), the spec does NOT proceed to blind verification in its current v2 form. It returns for **v3 production** that resolves the Q3 contradiction and applies the Q1+Q2 PASS-WITH-CLARIFICATIONS D-conditions, after which **this self-consistency stage re-runs** against v3 (or, if a much-narrower fix is preferred, the FAIL is treated as a structural-blocker D-condition with v3 producing a single-issue self-consistency re-run scoped to confirming the Principle V fix). The arbiter's strong recommendation is the former — full v3 cycle, full self-consistency re-run — because the Principle V violation was unanimously missed by *both* the originating four agents AND the engineering author who wrote v2 from the originating ruling. That is a signal that the spec deserves a fresh pass, not a patch.

---

## D-Conditions for spec v3

If the agentic process produces v3, these conditions MUST be applied. They are derived from the converged findings in Phase 5 synthesis "Actionable Spec Changes," the per-agent revisions, and the arbiter's framework analysis above.

**Q3 (blocking — must fix to clear self-consistency):**

- **D1.** Rewrite § 5.1 validation architecture as **non-blocking, warning-based**. The engine writes the file unconditionally; on schema violation it logs the `ValidatorError` array to the deliberation event stream and emits a prominent warning. CI gates may block at PR-time; engine writes never block at write-time. This satisfies XXVIII sub-clause 2 (mechanical enforcement via CI visibility) AND preserves Principle V (does NOT block file writes).
- **D2.** Strike the Principle II citation in § 9.1; replace the RECURSION-EXEMPTED justification with explicit temporal-constraint framing.

**Q2 (required clarifications):**

- **D3.** Add § 9.2 cross-tier weakening assessment — explicitly evaluate the accommodation mechanism against CONSTITUTION.md L649-664 criteria (i), (ii), (iii). Document the conclusion (accommodation is temporal constraint, not implicit relief) in the spec text.
- **D4.** Replace "RECURSION-EXEMPTED" language with temporal-constraint language ("v4.2.0 verification outputs predate JSON schema availability by construction; JSON mandatory for specs ratified after v4.2.0 implementation completion") throughout § 9.1, § 12 OQ5, § 13.
- **D5.** Add explicit anti-precedent language: "This temporal-constraint accommodation applies only to specs that ratify the schema infrastructure they would otherwise be required to use. Future amendments creating new validation infrastructure are NOT exempt from using existing validation infrastructure."
- **D6.** Add temporal-ratification-hazard handling for ratification after 2026-12-01: if ratification occurs after the universal cliff date, T4 is treated as in-effect at ratification with T1-T3 collapsed.
- **D7.** Specify schema-advancement-authority — who decides the `1.0.0-rc.1` → `1.0.0` bump after 30 days clean operation, and by what criteria.
- **D8.** Add forward-promotion pathway: one paragraph referencing GOVERNANCE.md's pattern-promotion pathway (or scaffolding such a pathway) for the case where a future conversus-* sibling produces deliberation-like artifacts.

**Q1 (required clarifications):**

- **D9.** Declare `engine/schema/v1/` location in `conversus-oss/CONFORMANCE.md` per XXVIII sub-clause 1 textual requirement (CONSTITUTION.md L505-510).
- **D10.** Add README.md and CLAUDE.md links to CONSUMER-CONTRACT.md per sub-clause 1 (CONSTITUTION.md L508-510 — links required from "BOTH").
- **D11.** Complete CONSUMER-CONTRACT.md content specification per sub-clause 5 — explicitly name the schema surfaces and state the stability guarantee (CONSTITUTION.md L572-577).
- **D12.** Specify bidirectional drift-detection CI: any change to `engine/schema/v1/*.schema.json` triggers CI re-validation of all existing producer code outputs under the new schema. May be implemented as warning-only (D1 consistency) but MUST be mechanically detected.
- **D13.** Reframe § 5.1's <100ms language as implementation discipline, not constitutional mandate.
- **D14.** Document fixture validation scope coverage per XXVIII sub-clause 2 — fixtures cover field presence, types, value constraints, enum violations.
- **D15.** Specify CI detection for schema-version-not-bumped-on-schema-edit per XXVIII sub-clause 3 ("silent format changes are a violation").

---

## Ruling Lines

- **Q1 RULING: PASS-WITH-CLARIFICATIONS** — XXVIII sub-clauses 1-5 structurally addressed; literal textual gaps in CONFORMANCE.md declaration, README+CLAUDE linking, and CONSUMER-CONTRACT.md content specification (D9-D11) plus secondary cleanups (D12-D15).
- **Q2 RULING: PASS-WITH-CLARIFICATIONS** — Tier 3 placement stable; RECURSION-EXEMPTED accommodation can be precedent-safe **only if** reframed as temporal-constraint with explicit cross-tier-weakening assessment + anti-precedent language (D3-D8).
- **Q3 RULING: FAIL-CONTRADICTION** — v2 § 5.1 blocking validation directly contradicts ratified Tier 2 Principle V "does NOT block file writes" (CONSTITUTION.md L76-78), unanimously identified by all four agents; remediation via non-blocking warning architecture (D1) before re-run.
