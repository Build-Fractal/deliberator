# Consumer Advocate — Revised Position (Iteration 1)

**Reviewer**: Consumer Advocate
**Date**: 2026-03-24

---

## Recommendation Dispositions

### Recommendation #1 (P1): Fix G5 (RLS/user_id mismatch) before any consumer testing
**Disposition**: MAINTAIN — unchanged severity, revised fix guidance.

All three cross-reviewers agree G5 is the single highest-priority fix. The architect (SA-1), security-reviewer (SA-1), and devex-advocate (SA-1) all independently classify it as a hard blocker. No dispute on diagnosis or severity.

I accept the security-reviewer's point (DC-2) that using the service role key bypasses RLS entirely, trading a deployment blocker for a data isolation gap. My original recommendation was agnostic on the fix approach ("Use the service role key or remove the user-scoped RLS policy"). I now refine: the service role key is the correct MVP fix because there are no real user accounts yet (FR-017 defers accounts). When FR-017 ships user accounts, the RLS policies must be revisited with real `auth.uid()` values. The team should document this as explicit tech debt: "RLS user-scoped policies are placeholder; re-enable when FR-017 adds user authentication." This addresses the security-reviewer's concern without blocking the consumer channel.

### Recommendation #2 (P1): Fix G17 (FRONTEND_URL missing from DO app spec)
**Disposition**: DOWNGRADE to P1-functional (not P1-security), maintain urgency.

The security-reviewer correctly notes (DC-4) that G17 has no security implications -- it is a functionality bug, not a security bug. I accept this distinction. My original framing conflated "launch blocker" with "security issue" by listing G17 alongside G3 and G5 without distinguishing the nature of the blockage. The architect's cross-review (Tension 1) makes the same point: framing matters because it affects where the fix is applied.

However, I maintain that G17 must be fixed before any consumer testing, not just before production. Share links are the primary mechanism by which one consumer brings another to the product. If every link generated during QA testing points to localhost, the team cannot validate the share-to-acquisition funnel at all. This is a one-line fix in `.do/app.yaml` and should not be deferred. Reclassifying it as "P2 — Should Fix" (the synthesis's current rating) understates the functional impact on the consumer validation experiment.

### Recommendation #3 (P1): Fix G3 (BYOK key race condition)
**Disposition**: MAINTAIN — unchanged.

Universal agreement across all reviewers. The architect (SA-2 in cross-review of my review), security-reviewer (SA-2), and devex-advocate (SA-1) all converge on the same diagnosis, severity, and fix: pass the API key directly to the provider constructor. The security-reviewer's cross-review adds the useful framing that this is validated from two independent threat models: billing correctness (my framing) and credential exposure (their framing). Both are real. No revision needed.

### Recommendation #4 (P1): Add rate limiting to POST /api/deliberate before public launch
**Disposition**: DOWNGRADE to P2. Accept the challenger framing.

This is the recommendation where the cross-reviews changed my position most significantly.

The security-reviewer (DC-1) correctly identifies that my threat model overstated the attacker's advantage: under BYOK, every request that reaches the engine pipeline requires a valid API key the attacker paid for. An attacker without a valid key fails at provider authentication before any LLM call executes. The real concern is server-side resource exhaustion from the pre-provider pipeline work (question classification, config parsing, agent setup), which is lightweight. The architect (Tension 2) adds that prioritizing operational hardening over structural correctness when the system is not yet deployed is the wrong ordering.

I also accept the devex-advocate's point (DC-2) that rate limiting is not just a web problem -- it is a provider-layer concurrency concern that affects SDK users equally. Fixing it only at the FastAPI endpoint leaves SDK deployers exposed. The correct solution is a provider-layer concurrency primitive, not just middleware.

I downgrade to P2 with the caveat that the team must confirm whether infrastructure-level rate limiting (CDN, WAF, or reverse proxy) exists in the DO deployment. If it does not, this should be addressed before any public consumer testing -- but it is not a merge blocker.

### Recommendation #5 (P2): Add free-text feedback field alongside perceived_value
**Disposition**: MAINTAIN with revised implementation guidance.

The architect (Tension 4) raises a valid concern about storage contract ambiguity: storing free-text in the same `usage_events` JSONB column alongside structured metrics creates a heterogeneous data model that spec 015 (feature extraction) would need to handle. The devex-advocate (T-2) makes the same point about untyped blobs degrading the developer analytics surface.

I accept this and refine the implementation: the free-text feedback should be stored in a separate `feedback` column on the `deliberations` table (or a dedicated `feedback` table), not mixed into `usage_events`. This preserves the structured telemetry contract for developers while giving the validation team qualitative signal. The security-reviewer (T-2) correctly notes that any free-text field requires XSS sanitization, length validation, and the same DOMPurify pipeline the main output uses. I add these as implementation constraints.

The core argument stands: with 25 data points (SC-005), binary feedback is insufficient. Every cross-reviewer who addressed this agreed the feedback mechanism needs expansion; the disagreement was only on storage architecture.

### Recommendation #6 (P2): Add visible character limit and input guidance to the question field
**Disposition**: MAINTAIN with dual-layer implementation.

The security-reviewer (SA-3 in cross-review of my review) explicitly agrees: "Both mitigations should be implemented -- frontend guidance for UX, backend max_length for enforcement. Neither alone is sufficient." The devex-advocate (T-1) raises a valid tension about whether max_length at the service layer would constrain SDK users with legitimate long-form inputs. I accept this distinction.

Revised implementation: backend `max_length` on the Pydantic model (security enforcement, applies to all channels), plus a frontend character counter with guidance text (consumer UX, applies only to the web form). The backend limit should be generous (e.g., 10,000 characters per the security-reviewer's suggestion) to avoid constraining SDK users, while the frontend guidance should be tighter ("describe your decision in 1-3 sentences") to improve consumer input quality. These are different limits serving different purposes.

### Recommendation #7 (P2): Add example questions to the web form landing page
**Disposition**: MAINTAIN — but acknowledge competing priorities.

No cross-reviewer contested the value of example questions. The devex-advocate (DC-3) correctly notes that developer onboarding friction (no `conversus quickstart`) and consumer onboarding friction (blank form, no examples) are distinct problems requiring distinct fixes -- a `conversus quickstart` command does nothing for web consumers, and example questions do nothing for CLI developers. I agree with this separation.

The architect's cross-review does not mention this recommendation at all, which I read as implicit acceptance that it is outside the architect's scope rather than disagreement. The devex-advocate (T-3) frames this as a resource allocation question: "The team must decide whether the first-hour investment goes into developer DX or consumer UX." This is a fair tension. I maintain P2 because SC-005 (25+ non-technical users) has a hard count target and blank-page bounce directly impacts achievability. But I acknowledge this competes with developer onboarding investments and the sequencing is a product strategy decision.

### Recommendation #8 (P2): Validate the 30-second target with real API providers
**Disposition**: MAINTAIN with revised success criteria.

The architect (Tension 3) makes an important point I did not address: the streaming architecture decouples perceived latency (time-to-first-meaningful-content) from total pipeline duration. If p95 wall-clock is 90 seconds but the first meaningful content streams at 8 seconds, the consumer experience may be acceptable even though the raw number exceeds the target.

I accept this and revise the success criteria. The team should measure both metrics: (a) time-to-first-meaningful-content via SSE (the consumer-relevant metric) and (b) total pipeline duration (the resource-relevant metric). SC-001 should be evaluated against time-to-first-meaningful-content, not wall-clock total. If first meaningful content streams within 15 seconds and the full result completes within 90 seconds, that is likely acceptable for consumers given the SSE streaming UX -- but this should be explicitly validated, not assumed.

The devex-advocate's concern (DC-4) that developer-friendly middleware layers (run_sync, service extraction) add latency overhead is noted. The latency budget should be defined before those layers are added, with a 500ms non-negotiable allocation for security validation as the security-reviewer suggests (T-4).

### Recommendation #9 (P2): Design consumer-facing error messages for every failure mode
**Disposition**: MAINTAIN with revised specificity guidance. Accept the security constraint.

The security-reviewer (DC-3) makes a strong argument I underweighted: telling users exactly why their API key failed ("not accepted" vs "rate-limited" vs "expired") gives an attacker a key-validity oracle. The architect (Dangerous Contradiction 4) adds that the structured error category system is the correct abstraction and my recommendation implied the architecture was wrong when it was only missing content.

I accept both points and revise. Error messages should map to broad consumer-friendly categories, not specific failure modes:
- Authentication issues: "We couldn't connect with your API key. Please check that you've entered the correct key."
- Temporary issues: "Something went wrong. Please try again in a moment."
- Input issues: "Your question couldn't be processed. Try rephrasing it in 1-3 sentences."

This provides recovery guidance without revealing whether a key is invalid, expired, or rate-limited. The structured `ProviderError.category` taxonomy should be preserved for programmatic consumers (SDK/CLI) as the devex-advocate recommends. The web frontend's `map_engine_error()` function already provides the correct architectural boundary for this mapping -- it needs consumer-friendly copy, not a different architecture. I was wrong to prescribe specific per-failure-mode messages.

### Recommendation #10 (P3): Assess whether BYOK is viable for consumer validation
**Disposition**: MAINTAIN as a product strategy flag, not a code review finding. Accept the scope criticism.

This was the most challenged recommendation. The architect (DC-1) argues it "treats a product strategy decision as a code review finding" and that a demo mode would require "auth, provider construction, session management, cost tracking, and rate limiting -- none of which the spec authorizes." The security-reviewer (DC-2) makes the strongest counterargument: BYOK is "the single strongest security control in the current architecture" and an operator-funded key introduces key storage, cost exposure, and abuse amplification risks that do not exist today. The devex-advocate (DC-1) adds that the engineering cost is "a multi-sprint engineering effort."

I accept all of these criticisms of the implementation proposal. I was wrong to suggest a demo mode as a P3 "fix" within this PR's scope. A demo mode is a new feature requiring its own spec, security review, and engineering investment.

However, I do not withdraw the underlying concern. The question remains: can you recruit 25 non-technical users (SC-005) who already have an AI provider API key? If the answer is no, the validation experiment fails regardless of code quality. This is not something the code review should fix -- it is something the team should have a documented answer to before running the SC-005 experiment. I reframe this from "assess whether a demo mode is needed" to "document the SC-005 recruitment strategy and confirm BYOK is not a blocking assumption." If the recruitment plan relies on users who already have API keys (e.g., AI enthusiast communities, existing ChatGPT Plus subscribers who can generate API keys), that plan should be written down. If no such plan exists, the team is building toward a validation target it cannot reach.

---

## New Recommendations

### New-1 (P2): Define separate channel-readiness criteria for the consumer web form

Multiple cross-reviewers independently identified the same gap. The devex-advocate (SA-4 in cross-review of my review): "the synthesis treats CLI and SDK as separate surfaces without recognizing channel-specific readiness." The architect (Dangerous Contradiction 3): "creating a separate consumer readiness track implies the web interface can be evaluated independently of the engine architecture, but it cannot."

I accept the architect's point that the bugs themselves (G3, G5, G17) are engine-layer or infrastructure-layer defects that must be fixed at the root, not patched in the web layer. But the assessment of whether those fixes are sufficient for consumer launch is a different question than whether they are sufficient for developer use. After G3, G5, and G17 are fixed, the developer channel (CLI/SDK/MCP) is functional. The consumer channel additionally requires: working share links (G17 fix), input guidance (rec #6), error message copy (rec #9), and a testable recruitment path (rec #10 reframed). The synthesis should include a "consumer launch checklist" that gates SC-005 testing -- not as a separate architectural assessment, but as a validation readiness gate that references the same underlying fixes.

### New-2 (P2): Implement dual-layer error architecture preserving structured categories for SDK while providing consumer-friendly messages for web

The devex-advocate's cross-review (DC-3) identified that consumer-friendly error strings and preserved `ProviderError.category` are "not complementary -- they are in direct tension" and that neither my review nor the devex-advocate's review proposed the dual-layer solution. The architect (DC-4) confirmed the structured error system is correct and needs content, not architecture changes.

The resolution: `ProviderError` retains its `.category` field for programmatic consumers. The web frontend's `map_engine_error()` function maps categories to broad consumer-friendly messages (see revised rec #9 above). The SDK exposes the raw `ProviderError` with category intact. This is not a new architecture -- it is documenting the intended use of the existing `map_engine_error()` boundary and filling in the consumer-facing copy that is currently missing. The M005 review confirms this boundary already exists; the gap is content, not structure.

---

## Position Summary

After reading the cross-reviews from the architect, security-reviewer, and devex-advocate, I revise my position on two substantive points and sharpen several others:

**Downgraded**: Rate limiting (rec #4) moves from P1 to P2. The security-reviewer's correction of my threat model -- that BYOK means attackers bear provider costs -- was persuasive. The real risk is pre-provider resource exhaustion, which is lightweight. Rate limiting matters but should not leapfrog deployment blockers.

**Reframed**: The BYOK viability question (rec #10) is no longer a code review finding with a demo-mode remedy. It is a product strategy flag that the team should resolve before running the SC-005 experiment. The security-reviewer correctly identified that removing BYOK would create new security problems (key storage, cost exposure, abuse amplification) that outweigh the conversion benefits. I was wrong to propose a demo mode within this PR's scope.

**Maintained with refinement**: G5 fix guidance now explicitly calls out the RLS tech debt. Error messages are revised to use broad categories rather than specific failure modes, accepting the security-reviewer's oracle concern. The 30-second target is now measured against time-to-first-meaningful-content rather than wall-clock total. Free-text feedback is directed to a separate storage location rather than the structured telemetry table.

**Unchanged**: G3, G17, example questions, character limit guidance, and latency validation all stand. The core consumer concern remains: the implementation is architecturally sound and received genuine investment, but three P1 bugs (G3, G5, G17) make the consumer channel non-functional in production, and several P2 gaps (input guidance, error copy, feedback richness, onboarding) will determine whether SC-005 is achievable.

The strongest consensus across all four reviewers: fix G3 and G5 before merge, fix G17 before consumer testing, preserve the pure-function architecture while doing so, and rely on the 1,318+ test suite to validate fixes. The team should act on these with confidence.
