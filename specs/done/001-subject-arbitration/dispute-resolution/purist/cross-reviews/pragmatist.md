# The Purist Cross-Review of The Pragmatist

**Reviewer**: The Purist
**Reviewing**: The Pragmatist's dispute resolution positions
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: "The template is the enforcement surface" vs. refusing validation at the template's output boundary (Blocker 4)

The Pragmatist's central thesis -- repeated in Blockers 2 and 4 and elevated to a named principle ("The template is the enforcement surface") -- is that LLM agents see prompts, not specs, and therefore the template is where runtime enforcement happens. I agree with this thesis. The contradiction is that The Pragmatist then *stops at the template*. Option C "weighted toward the template" means: write the instruction, trust the agent, skip output validation.

This is dangerous because it treats the template as a reliable enforcement surface. It is not. The template is a *probabilistic* enforcement surface. LLMs violate prompt instructions routinely -- not out of malice but out of stochastic generation. The Pragmatist's own logic demands a validation layer: if the spec is invisible to the agent at runtime (true), and the template is probabilistic (true), then the only deterministic enforcement point is post-hoc output validation. By dismissing FR-023 citation validation as "a v2 concern at best," The Pragmatist builds a system where the only defense against citation boundary violations is a prompt instruction to a non-deterministic agent, then declares the problem solved.

The Pragmatist argues that "citation-source validation requires parsing prose to determine which document a citation refers to, which is an NLP problem." This is a straw man of my position. SC-010 does not require deep NLP. It requires checking that each binding decision contains at least one reference to the grounding document path -- a string-presence check, not semantic parsing. The hard part (detecting decisions that cite *only* docs entries) can start as a SHOULD-level heuristic. The Pragmatist conflates "perfect validation is hard" with "any validation is impossible" and uses the former to justify skipping the latter.

A system that relies on a single probabilistic enforcement point for a constraint that the entire spec identifies as critical (the grounding document is what makes arbitration authoritative, not advisory) is a system designed to fail silently. That is the opposite of the Pragmatist's own Principle 1 ("favor the recoverable error").

### DC-2: "False positives cost one agent call" misrepresents the actual cost of a false-positive trigger (Blocker 1)

The Pragmatist frames the false-positive cost of Option B as "one extra agent invocation." This framing is incomplete to the point of being misleading. The cost is not the invocation. The cost is what the invocation *produces*.

When the trigger fires on non-dispute content (a preamble line like "All disputes were resolved during deliberation"), Phase 6 runs. The arbiter reads the synthesis, finds no actionable disputes, and must produce output. The Pragmatist waves this away: "the arbiter reads the disputes, finds nothing actionable, and produces an endorsement-style output or flags 'UNRESOLVED -- no actionable disputes found.'" But the spec has no mechanism for this. FR-022's three-tier failure model covers: (1) agent process failure, (2) structurally unintelligible output (zero FR-018 headings), (3) incomplete but parseable output. A vacuous resolution -- one that contains the required section headings but resolves nothing -- falls into tier 3. The engine writes `resolution.md`. The final report says "Arbitration: 0 disputes resolved." Downstream consumers now see a `resolution.md` that exists, passed validation, and resolved nothing.

This is not a recoverable error. It is a silent semantic failure. The file exists. Validation passed. No warning was emitted. The only way to detect it is for a human to read the file and notice it is vacuous. The Pragmatist's cost model accounts for compute (one agent call) but not for the semantic integrity of the output artifact. A system that produces valid-looking but meaningless output is worse than one that produces no output, because the former creates false confidence.

The Pragmatist's own Principle 1 says to "favor the recoverable error." A vacuous `resolution.md` that passes validation is not recoverable -- it is undetectable without human review. A false negative (Phase 6 does not fire) is immediately visible: there is no `resolution.md`. The absence of an expected artifact is a signal. The presence of a meaningless artifact is camouflage.

### DC-3: Treating SHOULD-level template instructions as meaningful constraints on LLM behavior (Blocker 2)

The Pragmatist argues for SHOULD-level prose conventions in the template and explicitly distinguishes this from a contractual obligation: "SHOULD-level framing explicitly permits deviation. If an arbiter writes **Decision:** instead of **Ruling:**, that is fine." In the same breath, the Pragmatist claims this "improve[s] output consistency" and "give[s] v2 extraction a head start by establishing consistent patterns in real output."

These two claims are in tension that approaches contradiction. Either the SHOULD-level conventions produce consistent patterns (in which case they are functioning as de facto constraints and should be acknowledged as such), or they permit deviation freely (in which case they do not produce consistent patterns and the v2 benefit is illusory). The Pragmatist wants the benefit of consistency without the cost of commitment.

The deeper problem: the Pragmatist criticizes my position by saying "LLMs do not distinguish between SHOULD and MUST in their prompt" is irrelevant to Option B -- but that statement is actually *my* argument against the Pragmatist's position. If LLMs do not distinguish SHOULD from MUST, then either the convention functions as a hard constraint (in which case calling it SHOULD is dishonest) or it functions as noise (in which case adding it is pointless). The Pragmatist's "minimum viable improvement" is either an unacknowledged MUST or a documented no-op. Neither is a principled specification choice.

---

## Tensions

### T-1: "Ship v1 with minimum viable contracts, iterate from real usage" vs. specifying prose conventions and deferred schema fields before any usage exists

The Pragmatist's disposition is "ship v1 with minimum viable contracts, iterate from real usage." Yet in Blocker 2, the Pragmatist adds SHOULD-level prose conventions (six labeled sub-fields) AND a deferred structured output section with six schema fields, typing information, and future extraction targets. This is more specification than either Option A (headings only) or my Option C (headings + schema with activation condition).

The tension is not fatal but it is real. A pragmatist who ships the minimum viable contract would ship FR-018 headings and nothing else, then observe real arbiter output to determine what conventions emerge naturally. Instead, The Pragmatist pre-specifies conventions before observing a single real run. This is not iterating from real usage. This is specifying from anticipated usage. The Pragmatist is doing purist work under a pragmatist banner.

I do not object to the substance -- the conventions and schema fields are reasonable. I object to the framing. Calling pre-specified conventions "minimum viable" obscures the actual choice being made, which is to front-load design work on the theory that it will save v2 effort. That theory may be correct, but it is a purist argument, not a pragmatist one.

### T-2: SC specificity -- enough to be testable vs. enough to over-constrain implementation

The Pragmatist and I agree that SCs are P1. Our proposed SCs overlap substantially but diverge in specificity. The Pragmatist's SC-008 says "the engine does NOT write resolution.md, emits a diagnostic warning, and Phase 5 output is the terminal state." My SC-008 adds: "MUST emit a diagnostic warning to stderr" and "The final report MUST include 'Arbitration: failed ({reason})'."

The tension: my SCs constrain the output channel (stderr) and the report format (exact string pattern). The Pragmatist's SCs constrain behavior without prescribing implementation details. The Pragmatist would argue my SCs over-constrain; I would argue the Pragmatist's SCs are under-specified. Where is "diagnostic warning" emitted? How does an automated test verify it? Without a channel, the SC is not testable by a CI system. Without a format, different implementations produce different report strings that are functionally equivalent but textually incompatible.

This is a genuine tension, not a defect in either position. The right level of SC specificity depends on the consumption model: if only one implementation exists, the Pragmatist's level is sufficient. If multiple implementations or automated testing exist, my level is necessary. The spec does not yet declare its consumption model, which means this tension cannot be resolved from within the spec itself.

### T-3: The role of FR-023 -- structural validation only vs. extensible validation surface

The Pragmatist explicitly limits FR-023 to section-heading validation and argues that "extending it to citation-source validation is a fundamentally different capability that should not be conflated with structural validation." I extend FR-023 to include citation-source validation as a SHOULD-level check.

The tension concerns FR-023's identity. Is it "the section-heading validator" (a specific tool) or "the output validation framework" (an extensible surface)? The Pragmatist reads FR-023 narrowly: it validates structure, period. I read it broadly: it is the engine's post-hoc quality gate, and citation sourcing is a quality dimension.

Both readings are defensible from the current spec text. FR-023 says "the engine MUST validate that resolution.md contains the required section headings." This is clearly structural. But the validation step is the only post-hoc check point in the pipeline. If citation validation does not live in FR-023, where does it live? The Pragmatist does not answer this because the Pragmatist does not believe v1 needs citation validation. The question is deferred, not resolved.

---

## Safe Agreements

### SA-1: Success criteria are P1, and the specific FRs needing SCs are the same

Both positions classify missing SCs as P1 blockers. Both identify FR-022 (failure semantics), FR-023 (output validation), FR-024 (citation boundary), FR-026 (per-file attribution), and FR-027 (idempotency) as the requirements most in need of SCs. The Pragmatist writes four SCs (SC-008 through SC-011); I write six (SC-008 through SC-013). The Pragmatist's four are a proper subset of my six -- SC-008 and SC-009 map directly, SC-010 overlaps, SC-011 maps to my SC-013. My SC-011 (per-file attribution) and SC-012 (requirement traceability) are additions, not contradictions.

There is no dispute about whether SCs are needed, which FRs need them, or the priority of writing them. The only variance is scope (four vs. six) and specificity (see Tension T-2). This is safe to merge: write all six, negotiate specificity.

### SA-2: The template authoring contract should include a citation boundary invariant

Both positions add the citation boundary to the template authoring contract. The Pragmatist adds it as invariant 5: "The template must instruct the arbiter that only the grounding document may be cited as authority in binding decisions." I add it as an invariant with nearly identical language plus a cross-reference to FR-024. The wording differs trivially. The architectural choice -- that the template must restate this constraint -- is identical.

This is the strongest agreement in the entire cross-review. Both positions independently concluded that the template is an enforcement surface for citation boundaries and that the template authoring contract is the maintenance mechanism. The Pragmatist and I disagree about whether validation is also needed (see DC-1), but the template-layer enforcement is fully agreed.

### SA-3: FR-012's "default to true" philosophy is the correct safety posture for trigger design

Both positions cite FR-012's existing behavior -- default to `true` on parse failure -- as evidence for their Blocker 1 position. We interpret the evidence differently (the Pragmatist uses it to justify Option B's permissive trigger; I use it to argue that the defined pattern in Option A is the safer default because it avoids false positives that FR-012 cannot recover from). But both positions agree on the underlying principle: when in doubt, err toward running Phase 6 rather than skipping it. The disagreement is about what constitutes "doubt," not about the response to doubt.

This shared foundation means that any final resolution of Blocker 1 can appeal to FR-012's safety posture as common ground. The dispute is about the precision of the trigger, not the philosophy of the safety net.
