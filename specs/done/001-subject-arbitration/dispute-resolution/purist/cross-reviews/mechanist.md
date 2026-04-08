# The Purist Cross-Reviews The Mechanist

**Reviewer**: The Purist
**Subject**: The Mechanist's review of 001-Subject-Arbitration dispute resolution blockers
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: "Content-negative" dispute entry definition undermines the Mechanist's own determinism standard

The Mechanist's core thesis is: "If a machine can't check it, it doesn't belong in the spec." The Mechanist then selects Option B (content-negative) for dispute entry definition on the grounds that it is "deterministic." This is true in the trivial sense that checking for non-whitespace content is a deterministic operation. But determinism is not the same as correctness. A clock that is always wrong is deterministic.

The Mechanist argues that false positives are acceptable because "the arbiter reads the synthesis, finds no disputes, and produces an endorsement-mode output or a trivial resolution." But this assumes the arbiter agent behaves correctly when given a false-positive input -- the exact kind of assumption the Mechanist rejects everywhere else. The Mechanist's entire philosophy is that LLM output is probabilistic and unreliable. An arbiter that receives a synthesis with no actual disputes but fires anyway is an LLM agent operating outside its designed input conditions. The Mechanist provides no SC, no validation rule, and no engine-level check for what "endorsement-mode output" looks like or whether it is correct. The engine has no way to distinguish a vacuous resolution from a substantive one.

This is the contradiction: the Mechanist trusts the engine completely and the LLM not at all, then selects a trigger definition whose failure mode requires the LLM to behave correctly in a scenario it was not designed for. The content-negative definition offloads the cost of imprecision from the trigger to the arbiter -- moving unreliability from one place the engine controls (the predicate) to another it does not (the LLM's response to edge-case input).

### DC-2: Rejecting all prose conventions in v1 while demanding engine validation of citation sources in v1

On Blocker 2, the Mechanist insists that no prose conventions belong in the v1 spec because the engine cannot validate them: "if a machine can't check it, it doesn't belong in the spec as a normative requirement." On Blocker 4, the Mechanist proposes extending FR-023 to validate that "at least one citation referencing the grounding document" appears in the Binding Decisions section. But what is a "citation referencing the grounding document"? The grounding document is not referenced by a machine-readable identifier in the current spec -- it is referenced by prose mention of its content, path, or principles. Validating citation sources requires the engine to parse semantic content inside a section to determine whether a reference points to the grounding document or a docs entry.

This is exactly the kind of "regex matching on LLM prose" the Mechanist calls "brittle" in Blocker 2. If the engine cannot reliably validate `**Ruling:**` labels inside a section (Blocker 2 rationale), it cannot reliably validate grounding-vs-docs citation distinctions inside a section either (Blocker 4 proposal). The Mechanist draws a line between "section headings" (machine-checkable) and "prose conventions" (not machine-checkable), then crosses that line when the enforcement need is compelling enough. The principle is not "can the engine check it?" -- it is "does the Mechanist want the engine to check it?"

### DC-3: FR-012's "default to true" does not support content-negative; it supports a different failure mode

The Mechanist cites FR-012 as evidence that the spec prefers false positives over false negatives, then extends this to justify Option B. But FR-012 is a fallback for parsing failure -- when the engine cannot determine the trigger value at all, it defaults to true. This is a statement about what to do when the mechanism breaks, not about what the mechanism should be. The Mechanist conflates "default to safe when the check fails" with "design the check to be maximally permissive." These are different strategies. A fire alarm that defaults to sounding when the sensor malfunctions (FR-012) is not improved by making the sensor trigger on any air movement (Option B). The sensor should be precise; the default should be safe. Option A gives a precise sensor with FR-012 as the safe default. Option B makes the sensor itself so broad that the default is never reached -- but only because the primary mechanism has absorbed the imprecision that the default was meant to handle.

---

## Tensions

### T-1: Both reviews demand defense-in-depth on Blocker 4 but disagree on what counts as a "surface"

We agree on Option C for citation enforcement -- all three surfaces (spec, template, engine). But the Mechanist weights engine validation as "the only one that matters for correctness" while dismissing the template instruction as "a probability modifier." I weight all three surfaces as independently necessary because they catch different failure modes. This is not a semantic disagreement; it has practical consequences for how an implementor prioritizes work. If the engine validation is the only load-bearing surface, an implementor could skip the template instruction without compromising correctness in the Mechanist's model. In my model, skipping any surface creates an undetected failure class. The tension is whether defense-in-depth means "multiple independent layers, each necessary" or "one real layer plus optional aids."

### T-2: Success criteria scope -- observable behaviors vs. engine internals

We agree that missing SCs are P1 blockers. We wrote similar SCs for overlapping FRs. But our SC drafts reveal a tension in what SCs should specify. The Mechanist's SC-008 says "no resolution.md is written, Phase 5 output is the terminal state, and a diagnostic warning is emitted to the engine's warning channel." My SC-008 specifies "the engine MUST NOT write resolution.md, MUST emit a diagnostic warning to stderr, and MUST complete the conversus with Phase 5 as the terminal output. The final report MUST include 'Arbitration: failed ({reason})' instead of dispute-resolved count."

The Mechanist specifies what happens. I specify what an external observer can verify. "Warning channel" is an engine internal -- which channel? stderr? structured log? The SC must name it. "Terminal state" is a conceptual description -- my SC specifies the observable: the final report's content. This tension matters because SCs exist to enable independent verification. If the SC describes engine internals rather than observable outputs, it is an implementation note, not an acceptance criterion.

### T-3: The role of the template authoring contract

The Mechanist treats the template authoring contract as a synchronization mechanism ("the template authoring contract already exists as the synchronization mechanism") but does not engage with what happens when it fails. I treat it as a formal invariant list that the spec can audit. The Mechanist adds one invariant (citation boundary restatement) and considers the drift risk "manageable." I add the same invariant but ground it in the existing asymmetry: FR-015 already restates six behavioral constraints as template instructions, so FR-024 is structurally identical and the omission is unprincipled. The tension is whether the template authoring contract is a loose coordination mechanism (Mechanist) or a closed set of invariants that must be complete by construction (Purist). This affects how future requirements are added -- do they get template restatement by default, or only when someone notices the gap?

---

## Safe Agreements

### SA-1: Blocker 3 is P1 -- missing success criteria block implementation

Both reviews classify missing SCs as a P1 spec-completeness defect. Both cite the same APM concession: "A spec without acceptance criteria for its requirements is incomplete by any consumption model." Both identify the same FRs as urgently needing SCs (FR-022 through FR-027). Both reject gh-aw's P2 argument that RFC 2119 language alone is sufficient. The Mechanist's framing ("a requirement without a test is dead letter") and my framing ("untestable requirements are indistinguishable from aspirations") reach the same conclusion from different axioms. The proposed SCs overlap substantially in coverage and intent. This is the strongest convergence point across both reviews.

### SA-2: Blocker 2 resolution -- headings-only for v1, advisory schema deferred

Both reviews reject prose conventions as a v1 contract. Both accept FR-018 section headings as the sole enforceable v1 output contract. Both propose a standalone "Deferred: Structured Output" section with an advisory schema table containing the same six fields (dispute_id, ruling_type, grounding_citation, required_changes, affected_target_files, confidence_level). The disagreement is marginal: I add an explicit activation condition for when the deferral expires; the Mechanist does not. But the core structural decision -- what is v1, what is deferred, and where each lives in the spec -- is identical.

### SA-3: Blocker 4 requires all three enforcement surfaces

Both reviews select Option C. Both argue that the spec (normative source), template (runtime visibility), and engine validation (post-hoc detection) address different failure modes and are therefore all necessary. Both propose the same three concrete changes: (1) add citation instruction to FR-015's template instruction list, (2) add a template authoring contract invariant, (3) extend FR-023 to validate grounding citations. The Mechanist's proposed FR-023 amendment and mine differ in MUST vs. SHOULD for citation validation, but the architectural decision -- three surfaces, defense in depth -- is shared.
