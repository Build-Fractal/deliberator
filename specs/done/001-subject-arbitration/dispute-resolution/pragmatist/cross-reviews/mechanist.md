# The Pragmatist Cross-Review of The Mechanist

**Reviewer**: The Pragmatist
**Reviewing**: The Mechanist's review of 001-Subject-Arbitration blockers
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Blocker 2 -- Engine validation as gatekeeper vs. the reality that no engine can validate prose semantics

The Mechanist's central axiom -- "if a machine can't check it, it doesn't belong in the spec" -- leads to a self-defeating position on Blocker 2. The Mechanist rejects SHOULD-level prose conventions because "the engine cannot validate them." But the Mechanist simultaneously proposes SC-010 ("No binding decision in resolution.md cites a docs entry as the sole authority for a ruling") and extends FR-023 to detect "rulings without grounding citations." These are prose-semantic validations. The engine would need to parse natural language to determine whether a citation is a "sole authority" or a "contextual reference," and whether a passage constitutes a "ruling." This is the same NLP problem the Mechanist invokes to reject prose conventions -- yet the Mechanist builds enforcement mechanisms that depend on solving it.

The contradiction: the Mechanist says the engine cannot validate prose conventions (Blocker 2) but proposes engine validation of citation semantics (Blocker 4 and SC-010), which is a harder version of the same problem. If the engine can parse citation sourcing well enough to emit warnings, it can parse labeled sub-fields well enough to check their presence. If it cannot do either reliably, then the Mechanist's own Blocker 4 proposal and SC-010 are unenforceable by the Mechanist's own standard.

The Pragmatist's position -- template-level SHOULD conventions plus deferred engine extraction -- is internally consistent because it places the enforcement surface where it belongs (the prompt) and defers the machine-validation question to v2 when structured output makes it tractable.

### DC-2: Blocker 4 -- "Engine validation is the only thing that matters" vs. the Mechanist's own admission that citation validation is an NLP problem

The Mechanist states: "Engine validation is the only surface that is deterministic, machine-verifiable, and cannot be bypassed by LLM non-compliance." The Mechanist then proposes extending FR-023 so that the engine checks for "at least one citation referencing the grounding document in the Binding Decisions section." But determining whether a passage "references the grounding document" requires understanding the semantic content of prose. The arbiter might write "per the architectural constraints established in the project's foundational specification" -- is that a grounding citation? The engine cannot answer this deterministically.

The Mechanist dismisses template instructions as "probability modifiers" and elevates engine validation as the "load-bearing" surface. But for citation enforcement specifically, the engine check is also probabilistic -- it can detect the presence of a filename string, but it cannot determine whether that filename is being cited "as authority" versus "as context." The Mechanist's own enforcement mechanism has the same reliability problem the Mechanist attributes to template instructions, just relocated from the input side (prompt) to the output side (validation regex). The Pragmatist's position -- weighted toward the template -- is more honest about this limitation: prevent the problem at the source rather than pretend the engine can detect it after the fact.

### DC-3: Blocker 3 -- "Without SCs the engine has no specification for its own validation behavior" vs. proposing SCs that themselves require semantic parsing

The Mechanist frames SC need as a correctness gap: "A requirement without a test is a requirement the engine cannot verify." This is sound. But SC-010 as proposed ("No binding decision in resolution.md cites a docs entry as the sole authority for a ruling. At least one grounding citation appears in every ruling's rationale") defines acceptance criteria that are not machine-testable by the Mechanist's own standard. How does the engine identify "every ruling's rationale"? How does it determine that a citation is the "sole authority"? These require semantic parsing of LLM prose.

The Mechanist insists SCs must exist so the engine knows what correct behavior looks like -- but then writes SCs that describe correct behavior in terms the engine cannot evaluate deterministically. The Pragmatist's SC-010 is more honest: "Given a binding decision that cites only a docs entry, a post-hoc review or validation check flags the citation as non-authoritative." The phrase "post-hoc review or validation check" acknowledges that this may require human review, not just engine automation. The Mechanist's version implies pure engine enforcement of a criterion the engine cannot reliably check.

---

## Tensions

### T-1: Blocker 1 -- Agreement on Option B, disagreement on why it is correct (and what that implies for the rest of the spec)

Both reviews select Option B (content-negative). The reasoning overlaps substantially: both cite FR-012's "err toward running" principle, both identify the false-negative asymmetry, both reference the 2:1 deliberation split. But the Mechanist frames the choice as "which failure mode the engine selects for," while the Pragmatist frames it as "which error is recoverable."

This is not a semantic quibble. The Mechanist's framing implies the engine should be designed to select failure modes as a policy choice -- the engine is the decision-maker. The Pragmatist's framing implies the system should be designed so that when failures happen (regardless of cause), recovery is cheap. These framings diverge when applied to Blocker 4: the Mechanist says the engine should catch citation violations (engine as active enforcer); the Pragmatist says the template should prevent them (system designed for cheap recovery at the source).

The tension is productive but real: the same principle (prefer false positives) leads to different architectural postures depending on whether you center the engine or the system.

### T-2: Blocker 2 -- The real disagreement about what "contract" means

The Mechanist says SHOULD-level prose conventions are "a suggestion wearing a contract's clothes" and that "unenforceable SHOULDs create false confidence." The Pragmatist says SHOULD-level conventions are "template instructions" that "cost nothing to add" and "do not create contractual obligations."

Both are right about different things. The Mechanist is right that downstream tooling will treat consistent patterns as load-bearing, regardless of the SHOULD qualifier. The Pragmatist is right that template instructions are the correct enforcement surface for LLM output shaping, and that withholding guidance produces formatting entropy that costs more to fix in v2 than the conventions cost to add in v1.

The tension reduces to a risk-timing question: does the Mechanist's "defer cleanly" save more v2 rework than the Pragmatist's "shape early" saves in formatting consistency? This is an empirical question that neither review can resolve from first principles. The Pragmatist's position is lower-risk because the conventions are removable (they are template text, not code), while the Mechanist's formatting entropy is not -- once v1 produces inconsistent output, that output exists in the training/evaluation corpus permanently.

### T-3: Blocker 4 -- Template-weighted vs. engine-weighted Option C

Both reviews choose Option C (spec + template + engine). Both agree all three surfaces should exist. The disagreement is which surface is "load-bearing." The Mechanist says engine validation. The Pragmatist says the template.

The tension is genuine because the two weightings produce different implementation priorities. If the engine is load-bearing, v1 must ship citation validation in the engine -- a nontrivial feature that requires parsing prose for citation sources. If the template is load-bearing, v1 ships with a one-sentence template instruction and defers engine citation validation to v2. The Mechanist's approach is more thorough but requires solving the NLP problem now. The Pragmatist's approach is less thorough but shippable today with text-only changes.

This tension connects directly to DC-1 and DC-2: the Mechanist's engine-weighted position depends on the engine being able to perform citation-source validation deterministically, which the Pragmatist argues it cannot.

---

## Safe Agreements

### SA-1: Blocker 1 -- Option B (content-negative) with the whitespace/comment guard

Both reviews select Option B. Both cite FR-012. Both identify the false-negative asymmetry as decisive. Both reference the 2:1 deliberation split. Both propose nearly identical spec text: non-whitespace, non-HTML-comment content constitutes a dispute entry. The proposed FR-011 amendments are substantively identical -- the Mechanist's is slightly more formal ("The engine does not interpret the formatting or semantics"), the Pragmatist's is slightly more operational ("the cost of a false-positive trigger is one agent invocation"), but both produce the same engine behavior.

This is a genuine safe agreement. No further deliberation needed on Blocker 1.

### SA-2: Blocker 3 -- P1 priority, SCs required before implementation

Both reviews select Option A (P1). Both reject gh-aw's P2 argument. Both cite the same evidence: APM's concession, spec-kit's framing, the v2 synthesis classification. Both argue that implementability without SCs is not the same as verifiability without SCs. Both propose concrete SCs covering FR-022 (failure semantics), FR-023 (partial output), FR-024 (citation boundary), and FR-027 (idempotent overwrite).

The SC formulations differ in detail (the Mechanist proposes SC-008 through SC-013; the Pragmatist proposes SC-008 through SC-011), but the coverage is compatible. The Mechanist's set is more granular (separate SCs for FR-025 target-document identifiers and FR-026 affected files); the Pragmatist folds those into the Blocker 2 prose conventions. These can be reconciled during spec drafting without further deliberation.

### SA-3: Blocker 4 -- Option C (all three enforcement surfaces)

Both reviews select Option C. Both agree that FR-024 defines the normative rule, the template makes it visible to the arbiter, and the engine validates output. Both propose adding a citation-boundary invariant to the template authoring contract. Both propose adding a one-sentence instruction to FR-015 item 1. The proposed spec text is nearly identical.

The weighting disagreement (engine-weighted vs. template-weighted) is a real tension (T-3 above), but the surface-level agreement on "all three surfaces" is safe. The spec can adopt Option C as stated by either review; the weighting question affects implementation priority, not spec text.
