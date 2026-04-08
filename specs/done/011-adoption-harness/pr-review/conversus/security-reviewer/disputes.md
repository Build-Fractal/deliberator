# Security Reviewer — Final Disputes and Convergence

**Reviewer**: security-reviewer
**Date**: 2026-03-24
**Phase**: Cooperative Disputes — Phase 4

---

## Remaining Disputes

### Dispute 1: Rate limiting severity — P2 is correct; the consumer-advocate's and architect's P1-urgent classification is wrong

The architect's revised position (New Recommendation A) places rate limiting at P1-urgent, alongside G3 (BYOK race) and G5 (RLS mismatch). The consumer-advocate downgraded to P2 in their revision, but the architect picked up the P1 classification. I maintain P2 and reject the architect's escalation.

The argument rests on the BYOK cost model. Under BYOK, every request to `/api/deliberate` that reaches the LLM pipeline requires a valid API key that the requester paid for. An attacker without a valid key fails at provider authentication before any LLM call executes. The pre-provider pipeline work (question classification, config parsing, agent setup) is computationally lightweight. The real risk is server-side resource exhaustion (CPU, memory, async worker pool), not unbounded API cost — and that risk is bounded by uvicorn's concurrency limits on a basic-xxs instance.

This is categorically different from G3 and G5. G3 causes one user's credentials to leak to another user during normal operation — no adversarial intent required. G5 makes the entire application non-functional. Rate limiting protects against sustained adversarial attack on an unadvertised MVP endpoint. These are not the same severity class.

Placing rate limiting at P1-urgent alongside credential exposure and deployment blockers dilutes the urgency signal for the items that genuinely break the application for every user, not just under adversarial conditions. The architect's own revision (New Recommendation C) calls for a two-dimensional priority framework. Rate limiting is the test case: it is operationally important (fix before public launch) but not a correctness defect (the application works correctly without it). P2 with urgency before any consumer validation campaign is the right classification.

### Dispute 2: OAuth state validation — I revised upward to P1 in my revision, but the devex-advocate's P2 is also defensible; the dispute is about the principle, not the outcome

In my revision, I upgraded OAuth state validation from P2 to P1. The devex-advocate downgraded from P1 to P2 in their revision. The architect placed it at P1-urgent. We are split.

My revision argument was that the cost of keeping it at P1 is zero while the cost of downgrading is nonzero (deferral risk, precedent-setting). The devex-advocate's argument is that P1 should be reserved for items with "concrete, reliably-exploitable paths." Both arguments are internally consistent.

The underlying dispute is whether priority labels should reflect fix cost or exploitation probability. I argued in my revision that deferral risk and scheduled feature trajectory (FR-017 introducing redirect-based OAuth) justify P1 even when current exploitability is low. The devex-advocate argues the opposite: that P1 should signal genuine urgency, and inflating the P1 bucket with low-exploitability items degrades the signal.

I maintain P1 because the fix takes less time to implement than to triage. But I acknowledge this is a judgment call about labeling conventions, not a factual disagreement about the code. If the team implements the two-axis priority framework (P1-urgent vs P1-structural), the disagreement dissolves: OAuth state validation is P2-severity with P1-urgency-due-to-zero-cost-and-deferral-risk. The synthesis should capture this nuance rather than forcing a single label.

### Dispute 3: Consumer-advocate's error message specificity creates a key-validity oracle — the dual-layer design must enforce category-level granularity, not failure-mode-level granularity

The consumer-advocate's revised position (Recommendation #9) proposes three broad error categories: authentication issues, temporary issues, and input issues. This is a significant improvement over the original per-failure-mode messages. However, the revised categories still risk being too specific in one case. "We couldn't connect with your API key" tells an attacker that the key format was recognized but rejected — distinguishing between "invalid key" and "no key provided" is meaningful information for key-testing attacks.

The dual-layer error architecture (devex-advocate New Rec A, consumer-advocate New-2) is the correct structural solution. My dispute is about the content of the consumer-facing messages, not the architecture. The web API's `map_engine_error()` must map all authentication-category errors to a single message that does not distinguish between missing, malformed, expired, and invalid keys. The message should be: "There was an issue with your API credentials. Please verify your key and try again." This covers all authentication failure modes without revealing which one triggered. The consumer-advocate's proposed copy — "We couldn't connect with your API key. Please check that you've entered the correct key" — presupposes the key was provided and recognized, which leaks information.

This is not a major dispute. The architecture is agreed. The message copy needs one more round of refinement to close the oracle gap. I am raising it because error message wording decisions made now will be difficult to change once consumers have adapted to specific message patterns.

### Dispute 4: FRONTEND_URL does not belong in the security P1 list

The architect places G17 (FRONTEND_URL) at P1-urgent alongside G3 (BYOK race) and G5 (RLS mismatch). The consumer-advocate revised to "P1-functional (not P1-security)" and I agree with that distinction. G17 is a deployment configuration bug: share links point to localhost in production. It has zero security implications — no data is exposed, no credentials are at risk, no access control is bypassed.

The issue is not whether G17 should be fixed before consumer testing (it should) but whether it should appear in the same P1-urgent bucket as credential exposure and deployment-blocking security defects. Mixing functional deployment bugs with security defects in the same priority tier creates confusion about the nature of the risk. A team member triaging the P1-urgent list should understand that G3 and G5 are security issues requiring careful fix verification, while G17 is a one-line env var addition requiring no security review.

The architect's two-axis framework would resolve this: G17 is P1-urgent on the deployment-readiness axis and not rated on the security axis. If the synthesis uses a single priority list, G17 should be labeled "P1-deployment" or grouped separately from the security P1s.

---

## Convergence

### Convergence 1: G3 (BYOK os.environ race) and G5 (RLS/user_id mismatch) are the two highest-priority findings — universal agreement

All four reviewers independently classify G3 and G5 as P1 merge blockers. The diagnosis is identical across all reviews. The fix direction is identical: provider constructor injection for G3, service role key with documented FR-017 migration path for G5. The consumer-advocate's reframing of G3 as a "billing trust violation" and the architect's acknowledgment that the providers already accept the key parameter both strengthen the case. There is no remaining disagreement on these two items.

### Convergence 2: The two-axis priority framework resolves the P1 dilution problem

The architect proposed splitting into P1-urgent (production safety, user trust) and P1-structural (architectural readiness, fix before next spec builds on it). The devex-advocate proposed splitting urgency from severity. The consumer-advocate asked whether the merge gate should be "safe for developers" or "safe for consumers." These are three articulations of the same insight, and all four reviewers now accept some form of it.

The specific mapping I endorse: G3 and G5 are P1-urgent-security (credential exposure, deployment blocker). G4 (broken --phase) and G17 (FRONTEND_URL) are P1-urgent-functional (user trust, deployment completeness). G1 (dependency inversion) and G8 (lifecycle hooks) are P1-structural (fix before spec 016). Rate limiting, CORS, httpx timeout, and max_length are P2 (fix before consumer validation). This framework eliminates the disputes about whether items "deserve" P1 by acknowledging that different items are urgent for different reasons.

### Convergence 3: RLS fix approach — service role key now, per-user JWTs at FR-017

All four reviewers converge on the same fix: use the Supabase service role key for backend operations as an immediate unblock, with explicit documentation that RLS user-scoped policies are placeholder and will be enforced when FR-017 adds user authentication. The devex-advocate's concern about a "maintenance trap" is addressed by requiring code comments in both `web/db.py` and the migration file. The consumer-advocate's concern about data isolation is addressed by the service role key being a backend-only credential never exposed to the frontend. No remaining disagreement.

### Convergence 4: Pure function extraction is the strongest architectural pattern and must be preserved

Every reviewer independently validates the pure function extraction pattern (MCP tools, CLI commands, SDK methods all calling the same engine-layer pure functions) as the single best architectural decision in the PR. The architect frames it as the foundation for the plugin system. The devex-advocate frames it as the foundation for testability. The consumer-advocate frames it as what enables the four-surface deployment. I frame it as what enables security boundary enforcement (the engine layer is the single point where auth resolution, quality gating, and input validation happen). No disagreement.

### Convergence 5: The error architecture needs a dual-layer design — agreed on structure, minor dispute on content

All four reviewers agree that the error handling must serve both programmatic consumers (SDK/CLI needing structured `ProviderError.category`) and web consumers (needing human-readable recovery guidance). The devex-advocate's New Rec A (unified error architecture), the consumer-advocate's New-2 (dual-layer error), and the architect's acknowledgment of the gap all point to the same design: `ProviderError` retains `.category` for programmatic use; `map_engine_error()` in the web API translates categories to consumer-friendly messages; a test asserts raw error details never appear in HTTP responses. The only remaining dispute (Dispute 3 above) is about the specific wording of the consumer-facing authentication error message.

---

## Final Position Statement

### Non-Negotiables

1. **G3 (BYOK os.environ race) must be fixed before merge.** This is a credential exposure bug that is reliably exploitable under concurrent load. The fix is small (provider constructor injection), the providers already accept the key parameter, and every reviewer agrees. No compromise.

2. **G5 (RLS/user_id mismatch) must be fixed before merge.** The application is non-functional with migration 002 applied. The service role key is the correct immediate fix. The implementation must include code comments documenting that RLS is temporarily bypassed and will be enforced at FR-017. No compromise.

3. **G2 (OAuth state validation) must be fixed before merge.** The fix is one conditional and one raise statement. Even though the code-paste flow reduces exploitability, the deferral risk is nonzero and the implementation cost is zero. A one-line fix should never be deferred when it closes a spec-violation gap with a known escalation path (FR-017 redirect-based auth). No compromise on including it; the P1-vs-P2 label is a classification dispute I am willing to let the synthesis resolve.

4. **Error messages in the web API must not create a key-validity oracle.** All authentication-category errors must map to a single consumer-facing message that does not distinguish between missing, malformed, expired, or invalid keys. This is a security requirement that constrains the consumer-advocate's error message copy. The dual-layer architecture is agreed; the message content must be reviewed by security before finalizing.

5. **Any future demo/operator-key mode must undergo a dedicated security review before implementation.** The consumer-advocate correctly withdrew the demo mode proposal for this PR, but the underlying product question (BYOK viability for SC-005) remains open. BYOK is the strongest security control in the current architecture. Removing or supplementing it with operator-funded keys introduces key storage, cost exposure, and abuse amplification risks that do not exist today. This is a process gate, not an objection to demo mode.

### Flexibility

1. **Rate limiting priority.** I maintain P2, the architect proposes P1-urgent, the consumer-advocate revised to P2. I am willing to accept "P2 with a pre-consumer-validation deadline" as the synthesis position. The substance matters more than the label — rate limiting must be in place before the web form is publicly accessible, but it is not a merge blocker.

2. **OAuth state validation label.** I revised upward to P1, the devex-advocate holds P2, the architect says P1-urgent. If the two-axis framework is adopted, this resolves to "low severity, high urgency due to zero cost." I will accept any label that results in the fix shipping in this PR.

3. **CORS configuration approach.** The devex-advocate's environment-variable-driven CORS with restrictive defaults is a better implementation than my original hardcoded whitelist. I accept this approach. The security requirement is that defaults must be restrictive; the devex requirement is that they must be configurable. Both can be satisfied.

4. **Unshare endpoint timing.** I hold P3 for this PR. If the team wants to promote to P2 and include it in the PR, I have no objection. The 32-bit share_id entropy is adequate with rate limiting applied. Without rate limiting, the promotion argument is stronger — but rate limiting is independently justified regardless of unshare.

5. **Token refresh file locking.** I promoted this to a new P3 recommendation in my revision. If the team defers this to a post-merge follow-up, I accept that. The CLI-plus-MCP concurrent use case is real but edge-case for the adoption milestone. The fix (fcntl.flock) is straightforward when prioritized.
