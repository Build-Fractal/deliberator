# Consumer Advocate — Final Disputes and Convergence

**Reviewer**: Consumer Advocate
**Date**: 2026-03-24
**Phase**: 4 (Final Disputes)

---

## Remaining Disputes

### Dispute 1: Rate limiting severity — P2 is insufficient for an unprotected public endpoint

The security-reviewer maintains rate limiting at P2, arguing that under BYOK "attackers bear their own API costs." The architect adopts P1-urgent in their revised priority list (New Recommendation A) but acknowledges the security-reviewer's cost-model argument. The devex-advocate does not contest P2.

I accepted the BYOK cost-model correction in my revision and downgraded to P2. I now believe that concession went too far. The security-reviewer's analysis is correct for the LLM provider cost vector but ignores the server-side exhaustion vector entirely. Each POST to `/api/deliberate` spawns an async pipeline that consumes CPU, memory, and database connections regardless of whether the provider call succeeds. The DigitalOcean basic-xxs instance has 512 MB RAM and 1 vCPU. An attacker does not need a valid API key to exhaust the server -- they need only send requests that reach the pre-provider pipeline work (question classification, config parsing, Supabase insert, emitter setup). The provider call failing due to an invalid key does not undo the server resources already consumed.

The security-reviewer frames P1 as "the application is broken or insecure without this fix." I submit that an application which can be rendered unavailable to all consumers by a single actor sending rapid requests to an unprotected endpoint is insecure. The fact that BYOK limits the financial blast radius does not change the availability risk. For a consumer-facing product targeting non-technical users who will not understand why the form stopped responding, availability is a trust requirement.

I request P1-urgent classification with a minimal implementation: a per-IP sliding-window limiter (e.g., 5 requests per minute) applied at the FastAPI middleware layer. This is a well-understood pattern with readily available libraries (slowapi) and does not require the broader provider-layer concurrency design the devex-advocate proposes.

### Dispute 2: Consumer channel readiness is not captured in the merge/launch criteria

The architect's revised priority framework (P1-urgent vs P1-structural) is a significant improvement. However, the framework still evaluates readiness from only two perspectives: "safe for consumers to use" and "safe for developers to build on." My revision proposed a consumer launch checklist gating SC-005 testing. The architect does not address this. The security-reviewer explicitly rejects my G17 framing as having "no security implications" and places it outside their P1 list. The devex-advocate does not contest but also does not adopt it.

The gap this creates is concrete. After G3 and G5 are fixed, the architect's P1-urgent list is satisfied. But the consumer channel still lacks: (a) working share links (G17), (b) input guidance so consumers know what to type, (c) consumer-friendly error messages so failures are recoverable, and (d) a documented SC-005 recruitment plan confirming BYOK is not a blocker. None of these appear in any reviewer's "must fix before merge" list. They fall into P2, which in practice means "fix when capacity allows" -- and capacity may not allow before the validation experiment begins.

I am not asking for these items to block the PR merge. I am asking for the synthesis to include an explicit "consumer validation readiness" gate -- a short checklist that the team reviews before launching the SC-005 experiment. This is a process artifact, not a code change. The items on the checklist (G17 fix, input guidance, error copy, recruitment plan) are already agreed-upon P2 items. The checklist simply ensures they are sequenced before consumer testing begins, not after.

### Dispute 3: The 30-second latency target remains unvalidated and undiscussed

My revision accepted the architect's point that time-to-first-meaningful-content (via SSE streaming) is the consumer-relevant metric rather than wall-clock total. I revised the success criteria accordingly. No other reviewer has engaged with this concern at all. The security-reviewer does not mention latency. The devex-advocate mentions it only in the context of middleware overhead budgets (500ms for security validation). The architect acknowledges streaming decouples perceived and actual latency but does not propose measurement.

SC-001 specifies "zero to first recommendation in under 60 seconds." US-4 Scenario 1 says "within 30 seconds." The implementation includes SSE streaming, which may make the perceived experience acceptable even if the pipeline takes 90 seconds. But "may" is not a validated claim. No milestone review reports measured latency with real API providers. The test suite uses mock providers exclusively.

This matters for consumers specifically because a 90-second wait with no streaming feedback (if the SSE connection fails or the first agent takes 45 seconds) is an abandonment event. The consumer does not know the system is working. They close the tab. This is not a code defect -- it is a measurement gap that should be closed before consumer validation begins. I request that the synthesis include latency measurement as a pre-SC-005 requirement: 10 deliberations through each supported provider, reporting time-to-first-SSE-event and total wall-clock, with explicit acceptance criteria.

### Dispute 4: Error message content for consumers has no owner

My revision accepted the security-reviewer's constraint that error messages must use broad categories rather than specific failure modes (to avoid a key-validity oracle). The devex-advocate's New Rec A proposes a dual-layer error architecture: `ProviderError.category` for SDK consumers, `.user_message` for web consumers. The architect does not contest this design. All four reviewers converge on the architectural pattern.

The dispute is not about architecture. The dispute is about who writes the consumer-facing copy and when. The dual-layer design is a structural solution. But the `map_engine_error()` function currently maps categories to technical error strings, not consumer-friendly messages. Someone must write the actual copy: "We couldn't connect with your API key. Please check that you've entered the correct key." This is content work, not engineering work, and it has no owner in any reviewer's recommendation list. The devex-advocate's New Rec A focuses on the `.user_message` property design. The security-reviewer focuses on ensuring raw details never leak. Neither assigns the task of writing and testing the consumer-facing strings.

I request that the synthesis assign error message copy as a named task within the G17/consumer-readiness track, with the consumer advocate (or a designated content owner) reviewing the final strings before SC-005 testing begins. The architecture is agreed; the content is not.

---

## Convergence

### Convergence 1: G3 (BYOK race) and G5 (RLS mismatch) are unambiguous P1 merge blockers

All four reviewers agree without qualification. The diagnosis, severity, and fix direction are identical across every review and cross-review. G3 is fixed by passing the API key directly to the provider constructor. G5 is fixed by using the service role key with documented tech debt for FR-017. The consumer framing (billing trust violation, non-functional product) and the security framing (credential exposure, deployment blocker) reinforce each other. No dispute remains.

### Convergence 2: The two-axis priority framework (urgent vs. structural) resolves the P1 inflation problem

The architect proposed splitting P1 into P1-urgent (user-facing, fix before release) and P1-structural (architectural, fix before next spec builds on it). The devex-advocate adopted this framework and reclassified their recommendations accordingly. The security-reviewer's revised P1 list (G5, G3, G2) maps cleanly to P1-urgent. My own revised priorities map to the same framework: G3, G5, and G17 are P1-urgent; the dependency inversion and lifecycle hooks are P1-structural.

This framework resolves the central meta-dispute of the cross-review process: my criticism that the architect prioritized internal code structure over consumer-facing bugs, and the architect's criticism that I treated product strategy questions as code review findings. Both critiques were partially correct. The two-axis framework accommodates both perspectives without forcing one to subsume the other.

### Convergence 3: The pure function extraction architecture is the foundation that makes all fixes safe

Every reviewer independently validates this as the strongest pattern in the PR. The architect calls it "excellent architecture." The security-reviewer notes it enables testable dependency injection. The devex-advocate identifies it as the basis for the CLI-to-SDK graduation path. I note it is what makes the consumer web form independently testable and composable.

This convergence matters practically because it means the P1 fixes (G3 constructor injection, G5 service role key) can be made with confidence. The 1,318+ test suite, built on pure function extraction, provides a safety net for these changes. The architecture is not merely good design -- it is the operational prerequisite for shipping fixes quickly.

### Convergence 4: BYOK viability is a product strategy question, not a code review finding

The architect challenged my original demo-mode recommendation as "treating a product strategy decision as a code review finding." The security-reviewer identified that removing BYOK would create new security problems (key storage, cost exposure, abuse amplification). The devex-advocate noted the engineering cost of demo mode is a multi-sprint effort. I accepted all three criticisms in my revision and reframed the concern as a product strategy flag.

All four reviewers now agree: the code correctly implements BYOK as specified in FR-016. Whether BYOK is the right consumer gate for SC-005 is a question the team must answer before running the experiment, but it is not something this PR should attempt to change. The security-reviewer's process recommendation (New Rec B: require security review of any future demo/operator-key mode) is the correct gate if the team does decide to pursue it.

### Convergence 5: G17 (FRONTEND_URL) must be fixed before consumer testing, regardless of its P-label

The security-reviewer correctly notes G17 has no security implications. The architect classifies it as P1-urgent. The devex-advocate does not contest its urgency. I classified it as P1-functional in my revision. The specific priority label differs across reviewers, but the operational conclusion is identical: share links are broken in production without this fix, and share links are the primary consumer acquisition mechanism. No reviewer argues G17 can wait until after consumer testing. The disagreement is purely taxonomic (is it P1 or P2?), not substantive (should it be fixed before consumers see the product?).

---

## Final Position Statement

### Non-Negotiables

1. **G3 and G5 must be fixed before this PR merges.** This is universal consensus. No flexibility here.

2. **G17 must be fixed before any consumer testing begins.** Share links that resolve to localhost make the entire consumer validation experiment meaningless. The fix is one line in `.do/app.yaml`. This should not be deferred regardless of its priority classification.

3. **Rate limiting must exist on `/api/deliberate` before the web form is publicly accessible.** I maintain this is P1-urgent over the security-reviewer's P2 classification. A publicly accessible endpoint that spawns an expensive pipeline with no throttling is an availability risk that non-technical consumers will experience as "the product is broken" rather than "the product is under attack." Even minimal per-IP throttling is acceptable -- the implementation need not be sophisticated.

4. **Consumer-facing error messages must exist before SC-005 testing.** The dual-layer architecture is agreed. The actual consumer-friendly strings ("We couldn't connect with your API key") are not written. Non-technical users shown "ProviderError: 401" will not recover. This is a content task, not an engineering task, and it must have an owner.

### Flexibility

1. **Rate limiting implementation approach.** I accept either FastAPI middleware (my preference for speed) or the provider-layer concurrency primitive the devex-advocate proposes. The requirement is that some form of request throttling exists on the public endpoint. The architectural elegance of the solution is secondary to its existence.

2. **Latency validation timing.** I would prefer latency measurement before merge, but I accept it as a pre-SC-005 gate instead. The measurement must happen before non-technical users encounter the product, not after.

3. **Input guidance and example questions.** These are P2 items that improve SC-005 achievability but do not block the merge. I accept sequencing them after P1 fixes and before consumer testing begins. I do not insist on a specific implementation -- placeholder text, clickable examples, or a brief instructional sentence all serve the purpose.

4. **Free-text feedback field.** I accept separate storage (not in `usage_events` JSONB) per the architect's concern about heterogeneous data models. I accept P2 priority. The implementation detail is flexible as long as qualitative signal is captured before the 25-user sample is collected.

5. **Consumer readiness checklist format.** I proposed this as a section in the synthesis. I accept it as a separate document, a GitHub issue checklist, or any other artifact that makes the pre-SC-005 requirements visible and trackable. The format is unimportant; the existence of the gate is what matters.
