# The Mechanist: Revised Positions

**Agent**: The Mechanist (operational/engine perspective)
**Date**: 2026-03-19
**Inputs**: Pragmatist cross-review, Purist cross-review, my cross-reviews of both

---

## Blocker 1 -- Dispute Entry Definition

### Revised Position: HELD (Option B, content-negative)

Both cross-reviewers engage with this position from different angles. The Purist attacks it directly (selecting Option A); the Pragmatist agrees with it.

**The Purist's DC-1** argues that content-negative "undermines the Mechanist's own determinism standard" because the false-positive path requires the arbiter to behave correctly in an edge case (no real disputes present). The Purist says I trust the engine completely and the LLM not at all, then select a trigger whose failure mode requires the LLM to behave correctly. This is a well-constructed argument. It is also wrong about the stakes.

The Purist is right that I have no SC and no engine check for "endorsement-mode output." But the failure mode comparison is not "correct endorsement vs. incorrect endorsement." It is "unnecessary arbiter invocation vs. silently dropped disputes." When the arbiter fires on a false positive, the worst case is a vacuous resolution.md that a human reviewer can identify and discard. When the trigger fails to fire on a real dispute (Option A's failure mode), the worst case is that unresolved conflicts are silently accepted as resolved. The first is visible waste. The second is invisible corruption. The Purist's argument that the arbiter might misbehave on false-positive input is a valid concern, but the misbehavior is bounded and observable. The false-negative failure is unbounded and silent.

**The Purist's DC-3** says I misapply FR-012. FR-012 is about what to do when the mechanism breaks, not about what the mechanism should be. This is a sharp distinction. I accept that FR-012 is technically a fallback-failure directive, not a mechanism-design directive. But the asymmetry it encodes -- false positives are cheaper than false negatives -- is a system-level design value, not merely a fallback-failure policy. If the spec authors believed false negatives and false positives were equally costly, FR-012 would default to `false` (fail closed). They did not. The same cost asymmetry that justifies FR-012's default justifies Option B's primary mechanism. I refine my argument: FR-012 is not the authority for Option B, but the cost asymmetry that motivates FR-012 is the same cost asymmetry that motivates Option B.

**The Pragmatist** agrees fully (SA-1). The Pragmatist's framing ("which error is recoverable") is complementary to mine ("which failure mode the engine selects for"). Both framings converge on Option B.

Position held. The refinement: I no longer cite FR-012 as direct authority for Option B's mechanism design. Instead, I cite the cost asymmetry that both FR-012 and Option B share as the underlying design value.

---

## Blocker 2 -- Structured Output: Normative Weight for v1

### Revised Position: MODIFIED (Option A, headings only -- but conceding the Purist's activation-condition concept in weakened form)

Both the Pragmatist and the Purist challenge this position, from opposite directions. The Pragmatist wants SHOULD-level prose conventions in v1. The Purist agrees with headings-only for v1 but wants a formal activation condition for the deferral.

**The Pragmatist's T-2** makes the strongest case against me: "does the Mechanist's 'defer cleanly' save more v2 rework than the Pragmatist's 'shape early' saves in formatting consistency? This is an empirical question." The Pragmatist further argues that prose conventions are removable (template text, not code) while formatting entropy is permanent (inconsistent v1 output enters the corpus forever). This is a genuine concern. If v1 output is wildly inconsistent in format, v2 extraction will be harder regardless of what the spec says.

However, I am not persuaded this changes the spec-level decision. The Pragmatist's own DC-1 against me (Blocker 4) identifies the core problem: I reject prose conventions because the engine cannot validate them, then propose engine validation of citation semantics. The Pragmatist is right that there is a tension here -- but the resolution is not to add more unenforceable conventions. It is to be honest about what the engine can and cannot check. Prose conventions that the engine cannot validate are not "free" -- they create expectations that are enforced by nothing. The Pragmatist says "the SHOULD-level framing explicitly permits deviation." My cross-review response stands: SHOULD-level permissions are read by spec authors, not by developers who write parsers. The developer who sees `**Ruling:**` in 95% of output will hardcode against it.

I hold the core position: headings only for v1, advisory schema deferred.

**The modification**: I concede the Purist's point that a clean deferral without any transition criterion risks indefinite postponement. My cross-review criticized the Purist's activation condition ("when any downstream system declares a dependency") as unenforceable by the engine. I still believe this. But the Purist is identifying a real process gap, even if the proposed solution is not machine-checkable. I accept a weakened version: the deferred section SHOULD include a review trigger that is process-level, not spec-level. Something like: "The v1 implementation SHOULD collect real arbiter output samples. When 50+ samples exist, the project SHOULD evaluate whether extraction justifies formalization." This is explicitly a process recommendation, not an engine-enforced activation condition. It does not pretend to be more than it is.

Revised spec text for the deferred section's final paragraph:

> The production mechanism (arbiter-produced structured output, engine extraction from prose, or sidecar file) is deferred to v2. The v1 implementation SHOULD collect real arbiter output samples to inform the extraction strategy. When a sufficient sample corpus exists (recommended: 50+ arbitration runs), the project SHOULD evaluate whether output consistency justifies formalizing extraction conventions.

---

## Blocker 3 -- Success Criteria Priority

### Revised Position: MODIFIED (P1, with SC format concessions)

All three agents agree on P1. No one challenged the classification. The revisions are about the SCs themselves.

**The Pragmatist's DC-3** identifies that my SC-010 ("No binding decision cites a docs entry as the sole authority") requires semantic parsing that violates my own "if a machine can't check it" standard. The Pragmatist is right. My SC-010 as written describes a property that requires understanding what "sole authority" means in context, which is the same NLP problem I reject elsewhere. The Pragmatist's version ("a post-hoc review or validation check flags the citation as non-authoritative") is more honest because it acknowledges the check may require human review.

**The Purist's T-2** observes that my SCs describe engine internals rather than externally observable behaviors. "Warning channel" is an engine internal -- which channel? The Purist's version specifies stderr. This is more testable.

**The Pragmatist's T-1 (Blocker 3 tension)** notes that the Pragmatist's Given/When/Then format is stronger for test derivation, while my broader coverage (six SCs vs. four) is more complete. The Pragmatist proposes merging the Pragmatist's format with my scope.

I accept all three criticisms and revise accordingly:

1. **SC-010 revised**: Replace "No binding decision cites a docs entry as the sole authority" with a two-tier formulation: (a) engine-checkable: "At least one string matching the grounding document path appears in the Binding Decisions section," and (b) human-verifiable: "Post-hoc review confirms that no ruling relies solely on a docs entry as its authority." The engine handles (a); the SC explicitly marks (b) as requiring human or advanced tooling review.

2. **SC format revised**: Adopt Given/When/Then structure for all SCs, following the Pragmatist's lead. This is a better testing format and I have no principled objection to it.

3. **SC scope maintained**: I keep all six SCs (SC-008 through SC-013). The Pragmatist's four leave FR-025 and FR-026 without acceptance criteria. My cross-review's argument stands: if SCs are the bridge between spec language and test cases, the bridge should cross the entire river.

4. **Observable outputs**: Accept the Purist's point. SCs should specify observable outputs (stderr, exit codes, file presence/absence, report content), not internal engine state.

---

## Blocker 4 -- Citation Enforcement Surface

### Revised Position: MODIFIED (Option C, but conceding that engine citation validation is heuristic, not deterministic)

This blocker drew the sharpest fire from both cross-reviewers. Both the Pragmatist (DC-1, DC-2) and the Purist (DC-2) identify the same contradiction: I reject prose-convention validation in Blocker 2 as "brittle regex on LLM prose," then propose prose-semantic validation of citation sources in Blocker 4. This is the strongest argument against my review, and I must address it directly.

**The Pragmatist's DC-1**: "If the engine can parse citation sourcing well enough to emit warnings, it can parse labeled sub-fields well enough to check their presence. If it cannot do either reliably, then the Mechanist's own Blocker 4 proposal and SC-010 are unenforceable by the Mechanist's own standard."

**The Purist's DC-2**: "The Mechanist draws a line between section headings (machine-checkable) and prose conventions (not machine-checkable), then crosses that line when the enforcement need is compelling enough."

Both are correct that I crossed my own line. I was inconsistent. Here is how I resolve the inconsistency:

The engine check I proposed -- "at least one citation referencing the grounding document in the Binding Decisions section" -- is not deterministic semantic parsing. It is string-presence heuristic: does the Binding Decisions section contain the grounding document's filename or path? This is the same class of operation as FR-023's heading validation (string presence), not the same class as validating whether `**Ruling:**` labels are semantically correct (prose-convention parsing). My cross-review of the Pragmatist makes this argument: "Checking whether the Binding Decisions section contains at least one reference to the grounding document path (which is a known string, injected via `{GROUNDING_PATH}`) is the same class of operation -- string presence, not NLP."

However, I concede the following:

1. **String presence is a heuristic, not deterministic enforcement.** The grounding filename appearing in the section does not prove it was cited "as authority." The arbiter could mention the filename in passing while actually grounding its ruling in a docs entry. The Pragmatist's DC-2 is right that "it can detect the presence of a filename string, but it cannot determine whether that filename is being cited 'as authority' versus 'as context.'" I overstated the engine check's reliability when I called it "deterministic enforcement." It is a heuristic signal -- better than nothing, not the same as proof.

2. **The Blocker 2 / Blocker 4 asymmetry is real but justified on different grounds than I originally stated.** The difference is not "the engine can check citations but cannot check prose conventions." The difference is in the cost of getting it wrong. A false-positive on citation validation (engine warns when the citation is actually fine) wastes reviewer attention on a warning. A false-positive on prose-convention validation (engine validates `**Ruling:**` presence when the content under it is garbage) creates false confidence that the output is well-structured. The citation check's failure mode is a noisy warning. The prose-convention check's failure mode is silent acceptance of malformed content as valid. I should have argued cost-of-error asymmetry from the start, not determinism.

3. **I withdraw the claim that engine validation is "the only surface that matters for correctness."** Both cross-reviewers are right that this overstates the engine's capability for this specific check. Revised hierarchy: the template instruction is the primary prevention mechanism (it shapes the LLM's output distribution toward compliance), the engine check is a heuristic detection mechanism (it catches gross violations like zero grounding mentions), and the spec defines the normative rule. All three matter. The template is load-bearing for prevention; the engine is load-bearing for detection. Neither is sufficient alone.

Revised proposed FR-023 amendment:

> **FR-023**: After Phase 6 completes, the engine MUST validate that `resolution.md` contains the required section headings defined in FR-018. Additionally, the engine SHOULD check that the Binding Decisions section contains at least one occurrence of the grounding document identifier (filename or path). If heading validation fails, the engine MUST emit a warning to stderr. If the grounding-reference heuristic fails, the engine SHOULD emit an advisory warning: "No grounding document reference detected in Binding Decisions -- verify citation sources per FR-024." This is a heuristic check; it does not guarantee citation correctness but flags likely violations for human review.

The change from MUST to SHOULD for the citation heuristic reflects the concession that this check is not deterministic. It remains in v1 because the implementation cost is low (string search in a known section) and the signal value is high (catches the most egregious violations). But it is honestly labeled as a heuristic, not an enforcement mechanism.

---

## Final Position

| Blocker | Original | Revised | Change |
|---------|----------|---------|--------|
| 1 -- Dispute entry definition | Option B (content-negative) | Option B (content-negative) | **Held.** Refined FR-012 argument from "direct authority" to "shared cost asymmetry." |
| 2 -- Structured output | Option A (headings only) | Option A (headings only) + process-level review trigger | **Modified.** Conceded the Purist's point that clean deferral needs a transition criterion, but kept it as process recommendation, not spec-level activation condition. |
| 3 -- Success criteria | Option A (P1), 6 SCs | Option A (P1), 6 SCs in Given/When/Then format with observable outputs | **Modified.** Adopted Pragmatist's SC format, Purist's observability standard, and split SC-010 into engine-checkable and human-verifiable tiers. |
| 4 -- Citation enforcement | Option C, engine-weighted | Option C, rebalanced: template for prevention, engine heuristic for detection | **Modified.** Conceded that engine citation check is heuristic (not deterministic), downgraded from MUST to SHOULD, withdrew claim that engine is "the only surface that matters." Template and engine are co-load-bearing for different failure classes. |

### What I conceded and why

The cross-reviews exposed a genuine inconsistency in my original review: I invoked "the engine cannot validate prose" to reject Blocker 2 conventions, then proposed engine validation of prose semantics in Blocker 4. The Pragmatist and Purist both identified this from different angles, and both were right. My resolution distinguishes between string-presence heuristics (low-cost, useful signal, honestly labeled) and prose-convention validation (false confidence in output structure). The distinction is not "can the engine check it?" but "what is the cost when the check is wrong?" This is a more honest version of the mechanist position: the engine is still the most reliable actor in the system, but its reliability varies by check type, and the spec should reflect that variance rather than treating all engine checks as equally authoritative.

### What I held and why

Option B on Blocker 1 survives all challenges. The Purist's argument about false-positive input to the arbiter is valid but bounded -- the failure mode is visible and recoverable. Option A's failure mode is invisible and catastrophic (silently dropped disputes). The cost asymmetry is the same one that motivates FR-012, and no cross-reviewer offered an argument that overturns it.

Headings-only for v1 (Blocker 2) also survives. The Pragmatist's "formatting entropy" argument is real but does not justify adding unenforceable SHOULD conventions to the spec. Template authors remain free to use labeled sub-fields as instructional hints. The spec just does not bless them as conventions, because conventions the engine cannot validate become load-bearing assumptions that downstream consumers rely on without the engine guaranteeing them.
