# Spec 070 Audit Context (2026-04-28)

This file is the seed for the spec 070 review deliberation. It does NOT
restate spec 070's argument — agents read `specs/070-grandfathered-audit/spec.md`
directly. This file establishes *why* the spec exists and what the deliberation
is being asked to evaluate.

## Why spec 070 exists

The v2.4.0 amendment (spec 069, ratified 2026-04-26) added the **Constitutional
Inclusion Criteria** gate to `CONSTITUTION.md` Governance. The gate is
prospective — it applies to amendments after v2.4.0 — and the v2.4.0 SIR
explicitly grandfathers existing principles I-XXVII.

Spec 069 §5 included a non-binding "worked-examples" analysis that classified
each existing principle as passing or failing the gate. Three principles were
flagged as **failing**:

- **Principle VI — Scripts Over Markdown** — judgment call about "drives
  behavior" vs "human orientation"
- **Principle X — Zen of Python Output** — aesthetic predicates, not
  falsifiable
- **Principle XVI — Mathematical Transparency** — "user understanding" cannot
  be mechanically verified (headline framing); structural sub-claims
  (parameter pinning, shape determinism) ARE verifiable

The grandfathering provision (spec 069 §4.1, last paragraph, and v2.4.0 SIR)
explicitly anticipates a follow-up:

> "Migrating any of them to operational guidance is a separate, intentional
> act governed by the same amendment process (with the receiving document
> identified explicitly in the migration spec)."

Spec 070 IS that migration spec. It performs a formal, criterion-by-criterion
audit of VI, X, and XVI against the v2.4.0 gate, and proposes per-principle
disposition (migrate to operational guidance, refactor in place, or
pass-on-review).

## What this deliberation is asked to evaluate

Spec 070 is **governance-meta**: it does not directly edit `CONSTITUTION.md`
(actual migration is a separate implementation PR). Per spec 067 §4.1, the
both-methodologies rule (self-consistency AND blind) applies to amendments
that edit the constitution. Spec 070 is an **audit / migration plan**, not an
amendment. It therefore receives **one** review deliberation, not two.

The deliberation should evaluate:

1. **Are the per-principle audit verdicts (§4) correct?** Especially §4.3's
   SPLIT verdict on Principle XVI — that is the most contestable verdict. Is
   the reasoning sound? Does it follow from the v2.4.0 gate text in
   `CONSTITUTION.md` Governance?
2. **Are the proposed migration paths (§5) feasible and well-targeted?**
   `CONTRIBUTING.md` for VI; `docs/output-conventions.md` for X; refactor-in-
   place (Option A) vs split (Option B) for XVI. Is the easiest-first ordering
   correct?
3. **Does the spec stay within its declared scope?** §3 forbids auditing the
   other 24 principles, redefining the gate, or migrating any principle in
   this spec. Does the spec body honor those non-goals?
4. **Are the open questions (§8) the right open questions?** Q2 (version-bump
   category) and Q4 (Principle X mechanically-checkable subset as a future
   new principle) are the load-bearing ones; the others are housekeeping.

## What this deliberation is NOT asked to evaluate

- Whether the v2.4.0 gate itself is correctly drafted. That is `CONSTITUTION.md`
  Governance and was settled by spec 069's verifications.
- Whether the spec 069 §5 verdicts were correct in the first place. Spec 070
  §4 re-derives each verdict from first principles (Q1 in §8 acknowledges this);
  if §4's reasoning holds, the audit stands regardless of §5's classification.
- Whether the implementation PRs that follow this spec will be well-executed.
  Each implementation PR runs its own spec 067 verification (per §6.3).

## Acceptance bar

Per spec 067 §4.1 + §4.4 (applied analogously to a non-amendment audit):
0 ACCEPT-level findings on the per-principle verdicts in §4. Findings on
ordering, tone, or scope of §5 / §8 are addressable as REVISE.
