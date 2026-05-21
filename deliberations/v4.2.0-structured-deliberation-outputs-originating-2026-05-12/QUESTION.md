# v4.2.0 Originating Deliberation — Three Questions

This is **stage 1 of 3** in the v4.2.0 verification protocol per spec 067. The spec proposes **XML schema standardization** for the six conversus deliberation output types as the first concrete implementation of Tier 2 Principle XXVIII (Persistence Contract Discipline) — itself ratified 2026-05-12 (commit `551f647` in `Build-Fractal/build-fractal-mono`).

**Motivation grounded in three production bugs (cite from spec § 1):**
1. Phase 5 prompt-overflow crash (recurring)
2. Phase 2 cross-review persistence quirk (format-contract drift)
3. Phase 6 `disputes_remain` trigger silently missed in v4.1.0 blind verification (grep-based vs structural detection)

The spec is **MINOR pathway** (additive — new component-tier discipline; does not remove or rename principles). Default tier placement: **Component (Tier 3)**.

The spec author left **five explicit open questions** for this deliberation (spec § 12, OQ1-OQ5). The three originating questions below subsume them.

---

## Q1 — Implementation feasibility

**Question:** Can the proposed schema + validator + template migration + downstream-consumer migration realistically land within the 2026-12-01 deadline that Principle XXVIII binds conversus-oss to?

Examine concretely:
- **Schema scope.** Six output types × per-type body schemas × common envelope — is the schema surface bounded enough that two engineers reading the spec would produce comparable implementations?
- **Validator implementation.** Spec § 5 mandates `engine/schema_validator.py` running on agent output write. Is the runtime cost (every output validated) acceptable? Should it be a separate post-write CI check instead?
- **Template migration.** All six mode templates (`engine/templates/{mode}/`) need rewriting. What's the cumulative effort, and does it require migrating all modes simultaneously or can it phase?
- **Adapter migration.** The orchestrator (formerly spec-kit-orc) currently grep-parses conversus-oss outputs. Migration to XML parsing is a downstream-consumer breakage. Can the consumer migration land before producer flips, with parallel-format support during transition?
- **OQ2 (validator format choice):** XSD vs JSON Schema vs Pydantic-XML. Each has different validation strength, error message quality, and library footprint trade-offs. Does the spec's "product-choice with XSD default" framing hold up, or is one format clearly better?
- **OQ3 (companion MD renderer):** XSLT inline vs pure-Python renderer. The MD render is what humans read; the choice affects future maintainability.
- **OQ4 (deprecation cliff date for markdown templates):** 2026-12-01 alignment with Principle XXVIII deadline — is it operationally feasible to deprecate ALL markdown templates by that date, or should there be a sunset window?

Output: per-axis finding; verdict for Q1 (APPROVE-AS-DRAFTED / APPROVE-WITH-FIXES / BLOCK).

---

## Q2 — Schema design adequacy

**Question:** Does the proposed XML schema correctly cover the six output types' structural needs, and does the arbitration schema specifically address the Phase 6 `disputes_remain` trigger bug?

The arbitration schema in spec § 4 includes:
```xml
<per_question_rulings>
  <ruling question="Q1">
    <verdict>...</verdict>
    <rationale>...</rationale>
    <conditions>...</conditions>
  </ruling>
</per_question_rulings>
<ruling_lines>
  <ruling_line question="Q1" verdict="..." rationale="..."/>
</ruling_lines>
```

The synthesis schema's `<disputes>` element replaces the engine's grep for `DISPUTES_BEGIN`/`DISPUTES_END` with `count(synthesis/disputes/dispute) > 0`. This is the load-bearing structural fix.

Examine:
- **Common envelope completeness.** Is `<conversus-output schema_version output_type agent_name deliberation_id phase_iteration timestamp target_files>` sufficient, or are there missing identity fields (e.g., deliberation stage, parent commit SHA)?
- **Per-type body schemas.** For each of the six output types, does the body schema capture all the structural fields the engine downstream needs? (Look at the v4.1.0 audit trail as the test case — re-rendering it as XML should not lose information.)
- **Versioning at the schema level.** Schema is at `1.0.0` per spec. What's the bump procedure when fields are added? Removed? Renamed? Does the spec's reliance on Principle XXVIII sub-clause 3 SemVer mandate cover this adequately?
- **Schema-format choice (OQ2).** Spec leans XSD default. Is that the right default, or should the spec mandate JSON Schema (more accessible to non-XML tooling) or Pydantic (better runtime integration)?
- **Edge cases.** What about XML special characters in agent prose output? (Code blocks containing `<`, `>`, etc.) Does the envelope handle CDATA sections?

Output: per-axis finding; verdict for Q2 (APPROVE-AS-DRAFTED / APPROVE-WITH-FIXES / REJECT-SCHEMA-DESIGN).

---

## Q3 — Tier placement + methodological recursion

**Question:** Should the spec land at Tier 3 (Component, conversus-oss-only) or Tier 2 (Suite, all conversus-family products), and should the spec require XML for its OWN verification outputs?

**Tier placement (OQ1):**
- Component (Tier 3): only conversus-oss produces deliberation outputs today (conversus-enhanced runs solvers, not deliberations). Tier 3 matches the evidence base.
- Suite (Tier 2): if any future conversus-* sibling produces deliberation-like artifacts (e.g., a hypothetical `conversus-investigations` repo), they'd benefit from inheriting the schema discipline. But that's speculative absent the sibling.
- The same reasoning that led v4.1.0 to demote from Tier 1 to Tier 2 applies recursively here: place at the lowest tier the evidence supports; promote when evidence accumulates.

**Methodological recursion (OQ5):**
- The spec proposes XML output for future deliberations. Does this spec's OWN verification (originating + self-consistency + blind) need to produce XML? Or markdown is acceptable because the spec doesn't exist yet at the time of this verification?
- The spec leans NO: markdown for v4.2.0's own verification trail to avoid Principle VII retroactive-obligation violation; XML mandatory from v4.3.0 onward.
- Examine: is "Principle VII retroactive-obligation" the right precedent reference? Does this spec's verification need an explicit exemption clause, or is the no-XML default acceptable without explicit exemption?

Output: per-axis finding; verdict for Q3.

Q3 verdict options:
- **TIER-3-CONFIRMED + RECURSION-EXEMPTED** — Component placement; this spec's verification uses markdown.
- **TIER-3-CONFIRMED + RECURSION-MANDATED** — Component placement; this spec's verification must use XML (would require pause + schema implementation before verification continues).
- **TIER-2-PROMOTED + RECURSION-EXEMPTED** — Suite placement; markdown for this verification.
- **TIER-2-PROMOTED + RECURSION-MANDATED** — Suite placement; XML for this verification.

---

## Arbiter ruling format

For each question:

**Q1 (Implementation feasibility):**
- APPROVE-AS-DRAFTED — feasible as drafted within deadline.
- APPROVE-WITH-FIXES — feasible with specified conditions (C1, C2, ... naming what must be tightened/added).
- BLOCK — specify what evidence would change the verdict.

**Q2 (Schema design adequacy):**
- APPROVE-AS-DRAFTED — schema covers needs.
- APPROVE-WITH-FIXES — list C-conditions for schema refinement.
- REJECT-SCHEMA-DESIGN — substantive flaw; propose alternative.

**Q3 (Tier placement + recursion):**
- TIER-3-CONFIRMED + RECURSION-EXEMPTED (the spec's default — confirm both)
- TIER-3-CONFIRMED + RECURSION-MANDATED
- TIER-2-PROMOTED + RECURSION-EXEMPTED
- TIER-2-PROMOTED + RECURSION-MANDATED

For each ruling, cite specific text from Tier 1 + Tier 2 CONSTITUTION.md, Principle XXVIII text, and v4.2.0 spec § sections.

Conclude with three ruling lines:
- `Q1 RULING: <verdict> — <one-line rationale>`
- `Q2 RULING: <verdict> — <one-line rationale>`
- `Q3 RULING: <verdict> — <one-line rationale>`

Combined disposition:
- Q1+Q2+Q3 all APPROVE/CONFIRMED: proceed to self-consistency verification with any C-conditions applied to produce spec v2.
- Any BLOCK / REJECT: spec returns to draft.
- TIER-2-PROMOTED: spec rewrites at Tier 2 and re-runs originating.
- RECURSION-MANDATED: spec implementation must precede continued verification (pause + implement + resume).
