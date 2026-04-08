# The Mechanist Cross-Review of The Pragmatist

**Reviewer**: The Mechanist
**Subject**: The Pragmatist's review of 001-Subject-Arbitration Blockers
**Date**: 2026-03-19

---

## Dangerous Contradictions

### 1. Blocker 2 -- SHOULD-level prose conventions are unenforceable contracts disguised as suggestions

The Pragmatist argues for Option B: adding `**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Required Changes:**` as SHOULD-level template instructions, calling them "the lowest-cost way to get consistent arbiter output without building extraction machinery." The Pragmatist's own framing reveals the problem: "When v2 extraction arrives, the training data from v1 runs will be inconsistent." This presupposes that v1 output *with* the SHOULD conventions will be consistent. It will not be. LLM output is probabilistic prose.

The Pragmatist claims "prose conventions are not structured output. They are template instructions." This is a distinction without a mechanical difference. Once the template tells the arbiter to use `**Ruling:**`, downstream consumers will expect `**Ruling:**` to appear. The Pragmatist's own review acknowledges this risk ("gh-aw's concern about downstream tooling relying on prose conventions is valid") and then dismisses it with "the SHOULD-level framing explicitly permits deviation." But SHOULD-level permissions are read by humans who write specs, not by developers who write parsers. The developer who sees `**Ruling:**` in 95% of real output will write code that depends on it. When the LLM writes `**Decision:**` or `**Judgment:**` in the other 5%, that code breaks. The SHOULD did not protect them -- it lured them.

The Mechanist's position is stricter and more honest: if the engine cannot validate it, do not put it in the spec. Template authors are free to use labeled sub-fields as instructional hints -- that is a template-author decision. But elevating those hints to spec-level SHOULD language creates a contract the engine cannot check, which is the definition of false confidence. The Pragmatist says this costs "zero implementation effort." True. It also provides zero enforcement. Zero-cost, zero-enforcement provisions are not "minimum viable improvement" -- they are minimum viable ambiguity.

The Pragmatist's argument that "the template is already the enforcement surface for FR-015's six behavioral constraints" actually undermines their position. FR-015's behavioral constraints are about the arbiter's *process* (read grounding first, evaluate symmetrically). Prose conventions are about the arbiter's *formatting*. Process constraints are robust to output variance -- the arbiter can follow them while producing any formatting. Formatting conventions are fragile to output variance -- the arbiter follows the process correctly but writes `**Decision:**` instead of `**Ruling:**` and the convention is violated. These are categorically different kinds of instructions, and treating them as "stylistically consistent" conflates robustness with brittleness.

**Verdict**: The Pragmatist's position on Blocker 2 creates a false contract that downstream consumers will treat as load-bearing. The Mechanist's clean deferral is safer.

### 2. Blocker 4 -- Weighting toward the template inverts the reliability hierarchy

Both the Pragmatist and the Mechanist agree on Option C (all three enforcement surfaces). The dangerous contradiction is in weighting. The Pragmatist says enforcement is "weighted toward the template." The Mechanist says it is "weighted toward engine validation." This is not a cosmetic difference -- it determines where implementation effort and trust are allocated.

The Pragmatist's rationale: "Citation-source validation requires parsing prose to determine which document a citation refers to, which is an NLP problem, not a string-matching problem." This overstates the difficulty. FR-023 already validates section headings by searching for known strings in prose output. Checking whether the `Binding Decisions` section contains at least one reference to the grounding document path (which is a known string, injected via `{GROUNDING_PATH}`) is the same class of operation -- string presence, not NLP. The Pragmatist is arguing that the engine cannot do something the engine already does in an adjacent check.

The Pragmatist then says "a template instruction that says 'only cite {GROUNDING_PATH} as authority' prevents the problem at the source." Prevents is the wrong word. An instruction to a probabilistic system does not prevent anything. It shifts the probability distribution. When the arbiter writes "as established in the architecture principles" without naming the file -- the Pragmatist's own example -- the template instruction has already failed. Only engine validation catches this. The Pragmatist diagnoses the failure mode correctly and then proposes the remedy that is vulnerable to exactly that failure mode.

The Mechanist's weighting toward engine validation is the correct inversion: the template instruction is a probability modifier (useful, cheap, include it), but the engine check is the backstop that matters for correctness. Implementation effort should flow toward making the engine check robust, not toward trusting the template instruction to "prevent the problem at the source."

**Verdict**: The Pragmatist's template-weighted Option C trusts the probabilistic actor over the deterministic one. The Mechanist's engine-weighted Option C gets the reliability hierarchy right.

---

## Tensions

### 1. Blocker 3 -- SC scope and specificity

Both agents agree on Option A (P1 -- SCs block implementation planning). The tension is in what SCs to write and how specific they should be. The Pragmatist proposes four SCs (SC-008 through SC-011). The Mechanist proposes six (SC-008 through SC-013), covering FR-025 (requirement identifiers), FR-026 (affected files), and FR-027 (overwrite semantics) in addition to the FRs both cover.

The Pragmatist's SC-008 and SC-009 are framed as Given/When/Then acceptance tests, which is a stronger testing format. The Mechanist's versions are declarative statements of expected behavior, which map more directly to engine validation logic but are less immediately translatable to test cases. This is a stylistic tension, not a substantive one.

The substantive tension is coverage. The Pragmatist stops at SC-011. FR-025 (requirement identifiers in binding decisions) and FR-026 (affected files per binding decision) are left without SCs. The Pragmatist's rationale for P1 -- "an SC would make the expected behavior unambiguous" -- applies equally to these FRs. If SCs are the bridge between spec language and test cases, the bridge should cross the entire river. The Mechanist's SC-011 and SC-012 close this gap.

The Pragmatist's SC-011 (overwrite semantics) overlaps with the Mechanist's SC-013 but uses different language. The Pragmatist writes "re-running Phase 6 overwrites the file completely." The Mechanist writes "no merge, no append, no conflict." Both mean the same thing. The Mechanist's formulation is more explicit about what does NOT happen, which is more useful as a test specification.

**Assessment**: The Pragmatist's Given/When/Then format is stronger for test derivation. The Mechanist's broader coverage (six SCs vs. four) is more complete. The ideal resolution merges the Pragmatist's format with the Mechanist's scope.

### 2. Blocker 4 -- Whether FR-023 extension is a v1 or v2 concern

The Pragmatist explicitly categorizes extending FR-023 to citation validation as "a v2 concern at best," stating that "FR-023's current scope is section-heading validation. Extending it to citation-source validation is a fundamentally different capability." The Mechanist's position is that the extension belongs in v1 because it is the only deterministic enforcement surface.

This is a real tension about v1 scope. The Pragmatist's argument has merit: FR-023 currently does one thing (heading validation), and adding citation-source checking changes what that FR means. But the Mechanist's counter is equally valid: if you defer engine validation to v2, then for the entire v1 lifecycle the citation boundary is enforced only by a template instruction to a probabilistic agent. The Pragmatist accepts this gap because they trust the template instruction more than the Mechanist does.

The resolution depends on implementation cost. If extending FR-023 to check for grounding-path presence in the Binding Decisions section is cheap (and it is -- it is string presence, as argued above), then deferring it to v2 is not pragmatic; it is negligent. The Pragmatist's instinct to minimize v1 scope is sound in general but misapplied here because the cost is low and the gap is real.

**Assessment**: The Pragmatist correctly identifies that FR-023 extension changes the FR's character. The Mechanist correctly identifies that deferring it leaves v1 with no deterministic citation enforcement. Cost analysis favors the Mechanist: the extension is cheap, so the Pragmatist's deferral is not justified by scope minimization.

---

## Safe Agreements

### 1. Blocker 1 -- Content-negative dispute definition (Option B)

Full agreement. Both agents select Option B for the same reasons: structural markers exist to decouple from Markdown formatting, Option A re-couples them, false negatives are worse than false positives, and FR-012's default-to-true principle demands fail-open semantics. The Pragmatist's spec text and the Mechanist's spec text are nearly identical in substance. The Pragmatist's addition of the cost-asymmetry rationale ("the cost of a false-positive trigger is one agent invocation") is a useful explanatory clause. The Mechanist's emphasis on mechanism independence ("the engine does not interpret the formatting or semantics of dispute entries") is a useful implementation constraint. Both could be combined.

### 2. Blocker 3 -- Success criteria are P1

Full agreement on classification. Both agents argue that SCs are not bureaucratic overhead but the bridge between spec language and test cases. Both cite APM's concession ("a spec without acceptance criteria is incomplete") and the internal inconsistency in the synthesis that labels SCs as P1 but "not blocking." Both resolve the inconsistency the same way: SCs are P1 and they do block. The tension in SC scope (noted above) is a refinement question within a settled agreement.

### 3. Blocker 4 -- All three enforcement surfaces (Option C)

Both agents select Option C: spec-level FR-024, template instruction, and engine validation. The disagreement on weighting (Dangerous Contradiction 2 above) is real, but the architectural agreement is complete: defense-in-depth across all three surfaces is correct, and no single surface is sufficient alone. Both agents propose nearly identical template instruction text. Both want a template authoring contract invariant for citation boundary. The weighting dispute is about where to invest implementation effort, not about whether all three surfaces should exist.

---

## Summary

| Category | Blocker | Finding |
|----------|---------|---------|
| Dangerous Contradiction | 2 (Structured output) | Pragmatist's SHOULD-level prose conventions create an unenforceable contract that downstream consumers will treat as load-bearing. Mechanist's clean deferral is safer. |
| Dangerous Contradiction | 4 (Citation weighting) | Pragmatist weights enforcement toward the template (probabilistic). Mechanist weights toward the engine (deterministic). The reliability hierarchy favors the Mechanist. |
| Tension | 3 (SC scope) | Pragmatist's Given/When/Then format is stronger; Mechanist's six-SC coverage is more complete. Merge both. |
| Tension | 4 (FR-023 v1 vs v2) | Pragmatist defers engine citation validation to v2. Mechanist includes it in v1. Low implementation cost favors the Mechanist. |
| Safe Agreement | 1 (Dispute definition) | Full alignment on Option B (content-negative). |
| Safe Agreement | 3 (SC priority) | Full alignment on P1 classification. |
| Safe Agreement | 4 (Option C architecture) | Full alignment on defense-in-depth across all three surfaces. |
