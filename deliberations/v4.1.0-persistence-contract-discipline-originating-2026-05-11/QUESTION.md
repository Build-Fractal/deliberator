# v4.1.0 Originating Deliberation — Persistence Contract Discipline

**Pathway:** MINOR (Tier 1 sub-clause appended to Principle II; no principle removed or renamed). Per GOVERNANCE.md, MINOR amendments follow the same verification protocol as MAJOR: originating + self-consistency + blind.
**Date:** 2026-05-11
**Stage:** Originating (per GOVERNANCE.md Part VIII step 3 — produces the verdict that gates self-consistency verification).
**Spec under deliberation:** [`specs/v4.1.0-persistence-contract-discipline/spec.md`](../../specs/v4.1.0-persistence-contract-discipline/spec.md)

---

## What this deliberation decides

Three bundled questions. The arbiter rules on each separately; combined disposition gates whether the spec advances to self-consistency verification.

### Question 1 — Constitutional Inclusion Criteria gate

Per spec 070, principle additions and extensions must pass three Inclusion Criteria:

1. **Universal applicability** — does it apply to every Build Fractal product?
2. **Mechanical verifiability** — can conformance be checked deterministically?
3. **Non-redundance** — does it cover something not already addressed by an existing principle?

The spec § 8 argues the amendment passes all three:

- Universal: persistent on-disk state is a feature of every Build Fractal product.
- Mechanical: the discipline literally MANDATES mechanical CI enforcement.
- Non-redundant: existing Principle II (Stable Interfaces) treats stability abstractly; the sub-clause is the operational definition for the persistence interface specifically.

**Decide:** Does the amendment meet all three criteria? The pragmatist evaluates cost-of-conformance vs. stability gain. The devils-advocate challenges whether attaching the sub-doctrine to Principle II is load-bearing or cosmetic (i.e., whether this is really a NEW principle in disguise that would face a higher bar). The persistence-expert audits whether the schema-declaration mandate covers all realistic persistence surfaces. The ci-expert audits whether the mechanical-verifiability claim survives operational scrutiny.

### Question 2 — Schema-format flexibility

The spec § 3 non-goals explicitly states: "Does NOT mandate XML. Product implementations choose XSD, JSON Schema, Pydantic, AST-validator, or any other mechanical schema language. The amendment mandates that SOME mechanical enforcement exists."

The amendment text in spec § 4 sub-clause 2 reads: *"Mechanical enforcement. A CI gate validates that artifacts written during a run conform to the declared schema. Schema format is product-choice — XSD, JSON Schema, Pydantic model, AST validator, or any other format with a deterministic conformance check. Schemas declared without enforcement do not satisfy this discipline."*

The risk surfaced as condition **C1** in spec § 10: a product could declare "schema: this paragraph of prose" and trivially conform. The spec text attempts to close this with the "deterministic conformance check" clause.

**Decide:** Is product-choice the right flexibility, or should the amendment mandate a specific format? If product-choice is correct, is the "deterministic conformance check" wording tight enough to close the prose-loophole?

### Question 3 — 2026-09-01 remediation deadline realism

The spec assigns 2026-09-01 (roughly four months out from 2026-05-11) as the remediation deadline for three affected products:

- **conversus-oss**: structured-output migration (XML or equivalent), XSD CI gate active, V's 6 xfail tests un-xfail.
- **conversus-enhanced**: schema enforcement on whatever stateful artifacts the paid layer writes (or N/A with rationale).
- **spec-kit-orc**: reconcile `state-files.md` declared schemas with production JSONL data; add `bin/validate-state.sh`.

The spec § 10 names this as condition **C3**: confirm deadlines are operationally feasible.

**Decide:** Is 2026-09-01 lowest-regret? Or does the deadline set up a missed-deadline failure mode that erodes the principle's authority on first contact?

---

## Verdict format

The arbiter rules on each question:

- **Question 1:** APPROVE-AS-DRAFTED / APPROVE-WITH-FIXES (specify conditions) / BLOCK (specify failing criterion).
- **Question 2:** APPROVE-AS-DRAFTED / APPROVE-WITH-FIXES (specify wording tightenings) / REJECT-FLEXIBILITY (mandate a specific format).
- **Question 3:** APPROVE-AS-DRAFTED / APPROVE-WITH-EXTENSION (specify revised deadlines) / REJECT-DEADLINE (specify per-product feasibility).

### Combined disposition

- **All three APPROVE** (any variant): proceed to self-consistency verification with any specified fixes applied to produce spec v2.
- **Q1 or Q2 BLOCK/REJECT**: spec returns to draft; no self-consistency verification runs until the BLOCK is addressed.
- **Q3 REJECT-DEADLINE alone**: spec proceeds with revised deadlines; Q1+Q2 verdicts still gate ratification.

The conditions (C1, C2, C3, ...) emerging from the arbiter's ruling populate spec § 10 ("Conditions from originating") which the self-consistency verification stage must address.

---

## Files this deliberation reads

The agents read:

- `specs/v4.1.0-persistence-contract-discipline/spec.md` — the amendment spec itself (canonical text under deliberation).
- `build-fractal/CONSTITUTION.md` — Tier 1 Principle II current text (the principle being amended; preservation contract per spec § 5).
- `build-fractal/spec-kit-orc/specs/001-orchestrator/contracts/state-files.md` — the canonical positive example of a declared state-files contract, plus the documented drift (spec § 1 motivating evidence).
- `QUESTION.md` — this document.

The cross-product audit report from 2026-05-11 referenced in spec § 1 is summarized inline in the spec itself; agents do not need a separate audit-report file.

## Out of scope

This originating deliberation does NOT:

- Run self-consistency verification (separate deliberation per spec 067 + GOVERNANCE.md Part IV).
- Run blind verification (separate deliberation per spec 067).
- Decide the structured-output migration format (conversus-oss XML vs JSON vs other). That decision lives in the follow-on component-tier spec `v4.1.1-conversus-structured-output`.
- Decide spec-kit-orc's state-files reconciliation approach. That decision lives in the follow-on component-tier spec `v4.1.2-spec-kit-orc-state-files-reconciliation`.
- Amend any existing Tier 1 or Tier 2 principle other than Principle II.

If the originating deliberation passes, the next step is self-consistency verification (re-deliberate with a different agent composition against the same spec text, then apply any fixes to produce spec v2), then blind verification (strip version/date markers, run with agents not exposed to originating verdict), then ratification per spec § 9.4.

## Sequencing note

Per spec § 13 recommendation, this deliberation is staged but **NOT FIRED** in the same change that creates it. The amendment is intended to fire after Batch 2 (XXII × 2) PRs merge — the empirical evidence from those merges (vendoring discipline as applied to cross-product surfaces) informs the deliberation. Firing prematurely would miss that evidence.
