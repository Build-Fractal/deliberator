# Principle X Path-(c) Restoration Candidate

**Prepared 2026-05-04 for spec 070 cycle 3A deliberation per issue #119.**

This document is the candidate path-(c) refactor for Principle X
(Zen of Python Output). It is the artifact under deliberation: agents
evaluate whether the proposed restoration satisfies the three
conditions named by the supplemental blind verdict 2026-05-04
(SUSTAINED WITH FINDINGS, P1 finding #1).

---

## Background

Principle X was removed from the constitution in v3.0.0 (PR #98, spec
070 cycle 2A) on the grounds that its headline ("Zen of Python Output")
was rhetorical scaffolding rather than a falsifiable claim. The
substrate (four sub-bullets describing predictable output structure)
was migrated to `docs/output-conventions.md` at SHOULD strength.

The supplemental blind 2026-05-04 ruled that the cycle 2A removal was
**procedurally premature**: cycle 2A removed X without first
conducting a path-(c) feasibility assessment of whether the headline
could be refactored to express ONE structural invariant (parallel to
XVI's parameter-pinning headline rewrite in v2.6.0).

Per spec 070's path-(c) Governance subsection (added v2.6.0): a
headline rewrite of a grandfathered principle that restructures
existing body content into a new headline without introducing new
normative requirements is PATCH-class for the restructuring component.

This document is the path-(c) feasibility candidate for X.

---

## Three conditions to evaluate (from supplemental blind verdict)

The deliberation MUST evaluate the candidate against each of the three
conditions. The condition outcomes determine the verdict per spec 073
§4.3:

**Condition (i) Mechanical headline adequacy**: can a refactored
headline express ONE structural invariant that is mechanically
verifiable (analogous to XVI's "parameter pinning" headline)?

**Condition (ii) Sub-bullet specialization verification**: does X's
third sub-bullet ("errors should never pass silently") specialize
Principle V's "every phase MUST report progress" with output-format
requirements that V does not cover? (If V already covers it, the
sub-bullet composes from V and Criterion 3 fails.)

**Condition (iii) Verification block concreteness**: can a path-(c)
Verification block be written that an engineer could sketch in one
paragraph (as the v2.4.0 gate's Criterion 1 requires)?

If ALL THREE conditions are satisfied: VERDICT PASS — X is restored
under the proposed path-(c) refactor; the v3.0.0 X migration is
superseded.

If ANY condition fails: VERDICT FAIL — the v3.0.0 migration is
confirmed and X stays migrated to operational guidance.

PARTIALLY PASS may be a valid verdict if specific sub-bullets pass
their condition but the headline does not (or vice versa) — in which
case the verdict names which sub-bullets are eligible for restoration
under a narrower path-(c) and which remain in operational guidance.

---

## Proposed restoration (the candidate under evaluation)

### Restored X — Predictable Output Tree

> Every conversus run produces a deterministic output tree such that
> an implementor can predict the full set of artifacts from the
> `conversus.yml` config alone. Specifically: the canonical synthesis
> location is `summary/final.md` for cooperative mode (and the
> mode-specific equivalent at the documented path for other modes
> per `templates/<mode>/synthesis.md`).
>
> Concrete invariants enumerated below; each is independently
> mechanically checkable.
>
> - **Synthesis canonical path**: `summary/final.md` exists with
>   non-empty content after every successful cooperative-mode run.
>   The absence of this file is a synthesis failure that MUST be
>   surfaced rather than silently swallowed.
> - **Output depth bound**: agent-produced content is at most ONE
>   directory level below the agent's own directory under the
>   configured `output:` root. Deeper nesting is a structural
>   violation.
> - **Malformed-output emission**: code that processes phase output
>   MUST emit a warning when documents are malformed, missing, or
>   out-of-spec. Silent halt-on-malformed is prohibited unless the
>   artifact is safety-critical (Principle XXIV applies).
> - **Per-file focus**: a single output file does not bundle multiple
>   unrelated artifacts. Each file has one obvious purpose
>   discoverable from its filename.
>
> **Verification**: parity test in `engine/tests/test_phases.py`
> asserts that `summary/final.md` exists with non-empty content after
> every mock-provider cooperative run (analogous to existing tests
> covering Phase 5 synthesis output). The depth-bound is enforceable
> via a path-depth lint walking `output:` after each run. The
> malformed-output emission is enforceable via warning-emission
> assertions in the artifacts test surface. Per-file focus has a
> filename-purpose lint via a per-mode whitelist.
>
> *Origin: Zen of Python Output. Retired in v3.0.0 cycle 2A as the
> headline "Zen of Python Output" was deemed rhetorical scaffolding;
> re-ratified under path (c) in v3.X.X cycle 3A on the basis that
> the substrate sub-bullets are independently mechanically checkable
> and the new headline ("Predictable Output Tree") names a single
> structural invariant. The migrated `docs/output-conventions.md` is
> retained as elaboration; the constitutional principle is the
> normative anchor.*

### Why the headline change works

The original headline ("Zen of Python Output") was a pun referencing
PEP 20. It read as rhetorical guidance rather than a falsifiable
claim — a reviewer applying the v2.4.0 gate would conclude "this is
a vibes principle" without engaging the body.

The proposed new headline ("Predictable Output Tree") names a single
structural invariant: the output tree is deterministic given the
config. A CI lint can walk the output directory after a run and
assert structural properties (file existence, depth bound, content
shape). This is parallel to XVI's path-(c) rewrite from "Mathematical
Transparency" to "Parameter pinning" — both replace a thematic
headline with a concrete structural anchor.

### How condition (i) is satisfied

Mechanical headline adequacy: "Predictable output tree" is a
structural property that a CI parity test checks directly. The
candidate Verification block names the test surface
(`engine/tests/test_phases.py`) and the assertion shape
(`summary/final.md` exists with non-empty content after every
cooperative-mode run). The check is sketchable in one paragraph.

### How condition (ii) is satisfied

Sub-bullet specialization verification: the malformed-output
sub-bullet ("warnings emitted for malformed output") specializes
V's "every phase MUST report progress" by adding output-format
requirements V does not cover. V mandates progress reporting (the
mechanism: events emitted at phase boundaries). X's malformed-output
sub-bullet mandates a different signal: warnings emitted when
artifacts violate structural expectations. The two principles
compose without redundancy.

The other sub-bullets (depth bound, per-file focus) similarly extend
V+VII (Reproducibility) with structure-specific concrete invariants.

### How condition (iii) is satisfied

Verification block concreteness: the candidate's Verification block
names exactly what a CI lint would check, where (which test files /
which path lints), and how (assertion shape). An engineer reading
the block can implement the verification in a single afternoon. This
matches the bar set by Principles XI, XII, XIII whose Verification
blocks are equally concrete.

---

## Cross-references

- Original X body: see `deliberations/070-supplemental-blind-2026-05-04/CONSTITUTION-v2.5.0-pre-migration.md` lines ~610-660 (X. Zen of Python Output, four sub-bullets)
- v3.0.0 migration: PR #98, `CONSTITUTION.md` v3.0.0 SIR
- Path-(c) precedent: v2.6.0 XVI rewrite (PR #95)
- Migrated content: `docs/output-conventions.md`
- Spec 070 cycle 3A tracking: issue #119
- Supplemental blind verdict: `deliberations/070-supplemental-blind-2026-05-04/arbitration/resolution.md`
