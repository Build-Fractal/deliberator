### Remaining Disputes

- **Dispute: OAuth Verification Epistemic Authority**
  - **My claim**: The OAuth preflight regex runs against `auth.json`, not against HTTP responses. My revision quoted the actual bash code verbatim: `grep -qE '"(access_token|oauth|subscription)"' "$HOME/.conversus/auth.json"`. The factual question is resolved. The `"subscription"` key is the specific false-positive surface. The appropriate action is to file a P2 issue scoped to that key. (Skeptical revision, Rec 1.)
  - **Opposing position(s)**: Pragmatist's New Rec 1 declares "Verify OAuth preflight code path before synthesis proceeds" as a blocking prerequisite: "Synthesis that incorporates both without resolving the factual question will give contradictory instructions." Pragmatist modified Rec 2a structures the filing decision as a conditional still pending verification. (Pragmatist revision, Modified Rec 2a and New Rec 1.)
  - **Why I will not concede**: I read the code and quoted it. The bash snippet is complete, locatable (SKILL.md in decide and run skills), and unambiguous about what is being scanned. A deliberation rule that treats in-revision code reads as insufficient while calling for the identical read in synthesis is circular — it asks the synthesizer to redo work already done. The pragmatist's conditional ("if auth.json preflight: file issue per skeptical-reviewer's Rec 1 scope") resolves deterministically once the factual question is answered. The answer is auth.json. The conditional fires.
  - **Counter-argument to their position**: Pragmatist's "verify first" prerequisite would be sound if both reviewers disagreed about what the code said or if my claim were an inference rather than a quote. Neither is true. Pragmatist's verification request is a process norm — don't act on one reviewer's unilateral claim — but that norm is satisfied by a direct code quote, not only by the synthesizer independently reading the file. If the synthesizer doubts the quote's accuracy, it can read the file; but the prerequisite framing in New Rec 1 suggests the synthesizer must re-read before considering any recommendation, which is not how in-revision evidentiary claims work in other parts of this deliberation.
  - **Proposed resolution path**: The synthesizer should treat the quoted code snippet as the closing evidence for the factual dispute, accept that `auth.json` is the regex target, and apply pragmatist's own conditional logic: file an issue scoped to the `"subscription"` key at P2. Pragmatist's New Rec 1 is satisfied by this path — the code path has been verified; the verification is in the skeptical revision. If the synthesizer independently wants to confirm, one file read suffices and does not require deferring the recommendation.

---

- **Dispute: Spec Amendment Wording — Scope and Mandatory vs. Conditional Framing**
  - **My claim**: The spec change for override-with-rationale should be scoped specifically to uniformity override claims and should use mandatory language: "A uniformity override claim must quote the specific text from the affected existing principle that would be narrowed under uniform application." (Skeptical revision, modified Rec 4.)
  - **Opposing position(s)**: Pragmatist's modified Rec 4 proposes broader scope and validity-conditional framing: "Override with rationale is valid when the rationale quotes the specific text of the existing principle that would be narrowed under uniform application." This covers all override-with-rationale invocations and is permissive ("valid when") rather than mandatory ("must"). (Pragmatist revision, modified Rec 4.)
  - **Why I will not concede**: The original precedent was established on a uniformity argument specifically. Broadening the quoted-text requirement to "override with rationale" generally is a scope expansion not requested by SESSION-REVIEW.md Q3 and not discussed in either Phase 2 cross-review. The substantive difference matters: "valid when" allows an override without quoted text that still claims other validity criteria. "Must quote" prohibits non-quoting uniformity overrides categorically. The falsifiability requirement I argued for is only satisfied by the mandatory framing — if quoted text is one of multiple criteria for validity, a future author can omit it and argue validity on other grounds. That is exactly the loophole the requirement is meant to close.
  - **Counter-argument to their position**: Pragmatist's wording was likely intended to merge our two requirements (discoverability anchor + falsifiability). But "valid when" does not forbid overrides that lack quoted text — it only characterizes what makes one valid. A future override author can cite other grounds for validity and bypass the quoted-text standard entirely under this wording. Pragmatist's framing is correct about the intent but incorrect about the enforcement: a validity condition and a mandatory requirement produce different behavior when the condition is not met.
  - **Proposed resolution path**: Accept the spec change in my wording (mandatory, uniformity-scoped) as the default. If the synthesizer prefers broader coverage, extend scope to all override-with-rationale invocations while preserving the mandatory "must quote" framing: "Any override-with-rationale claim must quote the specific text of the existing principle that would be narrowed under the override; the quoted passage and rationale are logged in SIR, governance log, and spec status." This preserves the falsifiability requirement pragmatist and I agree on, regardless of scope decision.

---

### Convergence

- **Converged: 1KB Adversarial Test Is Standalone P1**
  - **Shared position**: File a new issue — "test(engine): add adversarial long-response test for `_detect_provider_passthrough_error` — error string past 1KB boundary." One parametrized test, no implementation change. P1 priority.
  - **Agreeing agents**: Skeptical (New Rec 1), pragmatist (Rec 1, surviving).
  - **Strength**: Unanimous
  - **Path to convergence**: Both reviews identified this independently in Phase 1 from different analytical approaches — pragmatist from internal coherence (fix intent vs. test coverage), skeptical from external threat modeling (adversarial provider response). Both Phase 3 revisions preserved it without modification. Strongest consensus signal in this deliberation.

- **Converged: Bug 3b Future-Alias Regression Test**
  - **Shared position**: Add `test_decide_unknown_model_does_not_trigger_blocklist_fallback` — a test confirming an unknown model alias reaches `run_engine` unchanged without triggering blocklist substitution. P2 priority.
  - **Agreeing agents**: Skeptical (Rec 3, surviving), pragmatist (New Rec 2, added in revision).
  - **Strength**: Unanimous
  - **Path to convergence**: Skeptical carried this recommendation through all phases. Pragmatist was silent on Bug 3b in Phase 1 and Phase 2; in Phase 3 revision explicitly acknowledged the gap and added the recommendation. Pragmatist noted: "My original silence on Bug 3b was not a principled omission — I simply failed to convert an implicit concern into an explicit recommendation."

- **Converged: Concurrent Re-Raise Requires Positive Architectural Characterization**
  - **Shared position**: The `_gated_dispatch` concurrent re-raise question must not be closed with a burden-shift to the claimant. Before closing, a positive characterization must be written: "Cooperative dispatch is sequential in context X" or equivalent. If the dispatch model cannot be characterized, file a bounded issue rather than leaving it open.
  - **Agreeing agents**: Skeptical (modified Rec 2), pragmatist (modified Rec 2b).
  - **Strength**: Unanimous
  - **Path to convergence**: Skeptical pushed for explicit characterization in Phase 1; pragmatist pushed back with "burden on claimant" in Phase 1. Cross-review revealed that burden-shift is insufficient for a concern on the exact dispatch path that PR #52 was written to make fail-safe. Both revisions now require the positive characterization. The residual difference (where the characterization appears) is not a dispute — both require it be written.

- **Converged: #53 Deferral Was Correct**
  - **Shared position**: Not executing #53 in this session was the right call. The trigger condition (4th copy of OAuth preflight) is a legitimate technical criterion, not procrastination. 3 existing sites do not meet the threshold given cross-repo installation path complexity.
  - **Agreeing agents**: Skeptical (Rec 5 withdrawn in revision with explicit concession), pragmatist (Rec 3, surviving).
  - **Strength**: Unanimous
  - **Path to convergence**: Skeptical challenged the deferral in Phase 1. Pragmatist defended it. Cross-review revealed skeptical's "no prior policy weight" claim was ungrounded in governance text. Skeptical withdrew Rec 5 "without reservation" in Phase 3 revision and endorsed pragmatist's primary verdict: "Both reviews agree that executing #53 in this session would have been the wrong call."

- **Converged: Quoted-Text Citation Standard for Uniformity Override Falsifiability**
  - **Shared position**: Any uniformity override claim must quote the specific text from the affected existing principle that would be narrowed under uniform application, making the argument verifiable without independent research.
  - **Agreeing agents**: Skeptical (modified Rec 4), pragmatist (modified Rec 4).
  - **Strength**: Unanimous
  - **Path to convergence**: Phase 1 pragmatist proposed a single-line spec anchor without quoted-text requirement. Phase 1 skeptical proposed quoted-text without a spec anchor. Phase 2 cross-reviews identified these as complementary. Both Phase 3 revisions merged the requirements: quoted-text citation incorporated into a spec-level change. The residual dispute is scope and mandatory vs. conditional framing, not the quoted-text requirement itself.

---

### Final Position Statement

**Non-Negotiables**

1. **The 1KB adversarial test must be filed as a standalone P1 issue before this deliberation closes.** `_detect_provider_passthrough_error` is the primary mechanism preventing Bug 3a recurrence. An untested detection boundary is structurally inconsistent with the fix's purpose. Both reviews arrived at this finding independently, with no opposition at any phase. Non-negotiable because it is the unanimous convergence finding of this deliberation and costs one test to close a concrete, predictable regression path.

2. **The OAuth `"subscription"` key false-positive concern must be filed as a P2 issue, not closed as accepted risk.** The false-positive mechanism is real (any auth.json containing `"subscription"` as a key/value in a non-OAuth context routes silently to claude-code provider without valid credentials, producing 401 errors with no obvious cause). Pragmatist's modified Rec 2a states: "if auth.json preflight: file issue per skeptical-reviewer's Rec 1 scope." The code confirms auth.json is the target. The conditional fires. Closing this as accepted risk requires pragmatist to concede the factual premise; their revision does not concede it, but their own conditional logic requires the issue once the premise is resolved.

**Flexibility**

1. **The spec amendment wording can accommodate broader scope (all override-with-rationale, not only uniformity overrides) if the mandatory "must quote" framing is preserved.** What must be preserved: an override author cannot skip the quoted-text requirement and argue validity on other grounds. What I am flexible on: whether the requirement applies only to uniformity overrides or to all override-with-rationale invocations.

2. **The OAuth P2 priority could be elevated to P1 if the synthesizer determines the `"subscription"` false-positive path is more common than my current assessment.** My P2 reflects the narrowed scope (only `"subscription"` not `"access_token"` or `"oauth"`) and the specific failure condition (a non-OAuth provider that persists tier metadata in auth.json). If the synthesizer finds evidence that this path is common among the providers conversus targets, P1 is defensible. What must be preserved: the issue is filed; it is not closed as accepted risk.