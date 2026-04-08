# Developer Experience Advocate — Revision 1

**Revising**: `conversus/devex-advocate/review.md`
**Inputs**: Cross-reviews from architect, security-reviewer, consumer-advocate; cross-reviews I wrote of all three; global synthesis; M002-M004 reviews
**Date**: 2026-03-24

---

## Recommendation Dispositions

### Rec #1 (P1): Remove unsupported --phase choices immediately
**Disposition**: MAINTAIN at P1, accept architect's reframing of scope.

The architect's cross-review (DC-1) argues this should be P2 because "the fix is trivial, the blast radius is small," and challenges whether my definition of P1 (user-journey-first) should be unified with their definition (structural-debt-first). The consumer-advocate's cross-review (SA-1) agrees G4 is correctly P1. The security-reviewer does not contest.

I maintain P1 with this concession: the architect is right that urgency and severity are different axes. The --phase fix is P1-urgent (fix before any user touches it), not P1-structural. I accept the architect's proposed resolution of splitting into urgency and severity tracks, and place this on the urgency track. The fix remains a 1-line change to the click.Choice list. No substantive change to the recommendation itself.

### Rec #2 (P1): Add local OAuth state validation in _login_anthropic
**Disposition**: DOWNGRADE to P2, accepting security-reviewer's exploitability analysis while preserving implementation urgency.

The security-reviewer's cross-review (DC-1) argues this overstates the real CSRF risk for the code-paste flow: "For CSRF to succeed, an attacker would need to (1) convince the victim to initiate a login, (2) have the victim paste an attacker-controlled code#state value into their own terminal." The architect's cross-review (SA-1) agrees with P1. The consumer-advocate (SA-2) agrees it is a security fix regardless of audience.

After reflection, the security-reviewer's exploitability argument is technically sound -- the code-paste flow's attack surface is materially narrower than a redirect-based flow. However, two factors keep this high-priority: (a) the fix is 1 line, so the cost of doing it is negligible, and (b) as I noted in my cross-review of the security-reviewer (DC-1), if the flow ever moves to redirect-based, the missing check becomes a real CSRF vulnerability with no safety net. I downgrade to P2 rather than P1 because the security-reviewer is correct that it should not carry the same triage signal as the BYOK race (G3) or RLS mismatch (G5), which have concrete, reliably-exploitable paths. But I flag it as "P2 with zero implementation cost" -- it should be implemented in the same pass as P1 fixes regardless.

### Rec #3 (P2): Add run_sync() wrapper to Deliberation
**Disposition**: MAINTAIN at P2, accept architect's constraint on implementation.

The architect's cross-review (DC, item 3) argues that async-first is architecturally sound and that `asyncio.run()` already is the one-line sync wrapper. The security-reviewer's cross-review (T-1) supports the wrapper but requires it to use `asyncio.run()` internally, not `loop.run_until_complete()` on a shared loop. The consumer-advocate (DC-1) notes this is irrelevant to consumer adoption.

The architect's strongest point is that `run_sync()` "changes the SDK's contract" and risks thread-blocking in Django/Flask request handlers. I accept this concern -- the wrapper must include a docstring warning about blocking behavior. However, I maintain P2 because the architect's own observation that "asyncio.run() already is the one-line sync wrapper" actually proves my point: if the standard library provides the pattern, the SDK should too, because SDK users reasonably expect the SDK to handle this. The implementation should follow the security-reviewer's constraint: `def run_sync(self, **kwargs): return asyncio.run(self.run(**kwargs))` with clear documentation that this blocks the calling thread.

I also accept the architect's deeper question: the SDK's target user should be documented. My revised recommendation adds a requirement to include a "Sync vs Async" section in SDK documentation explaining when to use each method.

### Rec #4 (P2): Promote per_agent_outputs into SDK Result
**Disposition**: MAINTAIN at P2, accept architect's implementation scope.

The architect's cross-review (T, item 3) agrees on P2 but for different reasons (spec 015 needs per-agent position vectors) and warns that implementing it without a StorageWriter abstraction "creates backend-specific behavior that works for CLI/SDK but not for web." The security-reviewer (T-2) supports inclusion but recommends an `exclude_agent_outputs=True` parameter on `set_deliberation_public()` to strip per-agent outputs from share links. The consumer-advocate (DC-2) notes this competes with consumer feedback mechanisms for P2 bandwidth.

I accept the architect's expanded implementation scope: per_agent_outputs should be populated by the StorageWriter abstraction (when implemented), not by file reads. My original recommendation was too narrow -- "add a dict to Result" understates the work. The revised recommendation is: (1) add `per_agent_outputs: dict[str, str]` to Result as an initially-optional field, (2) populate it from in-memory pipeline data (which is available during execution before any file writes), and (3) ensure the StorageWriter abstraction (when built per architect Rec #4) uses the same in-memory data. This avoids the file-read dependency the architect correctly flags while delivering SDK value immediately.

I also accept the security-reviewer's recommendation to add the exclusion parameter for share links.

### Rec #5 (P2): Add 30-second timeout to all httpx.post calls
**Disposition**: MAINTAIN at P2, accept security-reviewer's expanded scope.

The security-reviewer's cross-review (DC-3) agrees on P2 but expands the concern: "a hung `refresh_token()` call permanently blocks an async worker, eventually exhausting the worker pool." My cross-review of the security-reviewer (T-4) acknowledged this as the stronger justification.

I revise the recommendation scope: the timeout must be applied to every `httpx.post()` and `httpx.get()` call in auth.py, not just the login-flow token exchange I originally focused on. The server-side async worker exhaustion risk identified by the security-reviewer is the stronger framing and should drive the implementation priority. The fix itself is identical: `timeout=30` on all httpx calls.

### Rec #6 (P2): Preserve ProviderError.category through dispatch_agent
**Disposition**: MAINTAIN at P2, revise implementation approach per architect's feedback.

The architect's cross-review (DC, item 4) argues that the fix is not "propagate the object" but "design a result type for dispatch that carries both the successful output and the error category," because `asyncio.gather(return_exceptions=True)` currently produces a homogeneous list and changing it to heterogeneous requires interface work. The security-reviewer (DC-4) raises a legitimate concern: propagating ProviderError objects must not leak structured error details through the web API. The consumer-advocate (DC-3) independently identifies the same tension -- consumer-friendly error strings and developer-friendly error categories require a dual-layer design.

I accept all three critiques. My original recommendation ("propagate the ProviderError object, not `str(e)`") was too simplistic. The revised recommendation is:

1. Design an `AgentResult` union type (or a dataclass with `output: str | None` and `error: ProviderError | None`) as the architect suggests.
2. Use this type as the return type from `dispatch_agent` in the gather results.
3. Ensure `map_engine_error()` in the web API remains the sole gateway for user-facing error responses, with a test asserting raw ProviderError details never appear in HTTP response bodies (per security-reviewer's resolution).
4. Add a `.user_message` property to ProviderError that generates consumer-friendly text from the category, so the consumer-advocate's need for plain-language errors (consumer rec #9) and the developer's need for programmatic categories are served by the same object.

This is medium-complexity design work, not a string replacement. I accept the upgraded effort estimate.

### Rec #7 (P2): Resolve EngineConfig.provider vs runtime provider default mismatch
**Disposition**: MAINTAIN at P2, no revision needed.

No cross-reviewer contested this recommendation. The architect's cross-review (DC-3) independently raises the same concern in a different context: per-phase model routing should not be added before existing defaults are consistent. This validates my recommendation. The fix: make both defaults "mock" (explicit opt-in for real providers) or both "anthropic" (implicit real usage). Given the security-reviewer's emphasis on informed consent about credential usage (T-3), defaulting to "mock" is the safer choice.

### Rec #8 (P2): Extract decide orchestration into a service function
**Disposition**: MAINTAIN at P2, accept architect's reframing and security-reviewer's constraint.

The architect's cross-review (DC, item 2) argues the extraction target should be "engine-layer orchestration function callable from CLI, SDK, and MCP" rather than my narrower "decide service function." The security-reviewer (T-5) requires the service function to enforce quality gating and auth resolution as non-optional steps. The consumer-advocate (T-1) adds that the web form's `/api/deliberate` endpoint is a fourth caller.

I accept all three expansions. The revised recommendation:
- Target: `engine/orchestrate.py` containing a `run_deliberation()` function that CLI, SDK, MCP, and web API all call.
- Quality gating and auth resolution are mandatory steps in `run_deliberation()`, not parameters the caller can skip (per security-reviewer).
- The function's interface must be designed for all four callers (per consumer-advocate), not just the three developer channels I originally scoped.
- The CLI `decide` command becomes a thin wrapper (~15 lines) over this function (per architect's framing).

The architect is correct that their framing "subsumes" mine. I adopt it.

### Rec #9 (P3): Document CLI/MCP behavioral asymmetry
**Disposition**: MAINTAIN at P3, no revision needed.

No cross-reviewer contested this recommendation. The asymmetry (CLI warns on insufficient questions, MCP rejects) is a deliberate FR-014 design choice that remains undocumented. The fix is documentation-only and low-effort.

### Rec #10 (P3): Add conftest.py to eliminate dual-import pattern in tests
**Disposition**: MAINTAIN at P3, accept architect's deprioritization rationale.

The architect's cross-review (T, item 4) agrees the fix "takes 15 minutes" but argues it "should not compete with structural recommendations for attention." The consumer-advocate (T-3) notes test contributor friction has a downstream consumer impact that is hard to quantify.

I maintain P3 and accept that this is correctly placed below structural work. The recommendation stands as-is: it is a 15-minute cleanup that should happen when someone is already in the test infrastructure, not as a standalone task.

---

## New Recommendations

### New Rec A (P2): Design a unified error architecture serving both developer and consumer audiences

**Source**: Cross-review convergence. The architect (DC, item 4), security-reviewer (DC-4), and consumer-advocate (DC-3) all independently identified that my original ProviderError.category recommendation (Rec #6) and the consumer-advocate's plain-language error messages (consumer rec #9) are in tension without a dual-layer design. My cross-review of the consumer-advocate (DC-3) flagged the same: "implementing consumer-friendly error strings without preserving the structured ProviderError taxonomy would actively break the SDK's programmatic error handling."

**Recommendation**: Design ProviderError to carry both structured category (for SDK consumers) and a human-readable `.user_message` property (for web consumers). The web API's `map_engine_error()` function maps category to user_message; SDK consumers access `.category` directly. This is a single-object, dual-interface design that serves both audiences without requiring separate error paths. Add a test asserting that raw ProviderError fields (provider name, raw API error text) never appear in HTTP responses.

This subsumes the implementation detail of Rec #6 and provides the architectural frame that all three cross-reviewers identified as missing.

### New Rec B (P2): Establish a CLI-to-SDK graduation guide as part of the adoption surface

**Source**: My original review (Off-Base #4) identified that "the gap between `conversus decide` and `Deliberation().run()` is a cliff, not a ramp." The architect's cross-review (T, item 5) validated this as "a genuine insight my review misses entirely" and proposed a middle ground: a `conversus.quick()` convenience function that mirrors CLI defaults. The consumer-advocate did not address this directly but their DC-3 independently confirmed that onboarding friction manifests differently per channel and must be addressed per-channel.

**Recommendation**: (1) Add a `conversus.quick(question, provider=None, model=None)` synchronous convenience function that mirrors the CLI `decide` command's behavior (auto-resolves provider, applies quality gating, returns Result). This is the bridge between "I used the CLI and it worked" and "I want the same thing in Python." (2) Add a "CLI to SDK" section in the SDK documentation that maps every CLI flag to its SDK equivalent. This is documentation, not code, but it is the highest-leverage documentation for adoption because it meets the developer where they already are.

The architect proposed option (b) (migration guide) as "documentation, not code" and option (a) (matching defaults) as "polluting the SDK's clean API." The `quick()` function is the compromise: it lives outside the core `Deliberation` class, provides the CLI-equivalent experience, and does not contaminate the async-first API design.

### New Rec C (P3): Add a documentation comment explaining plaintext credential storage rationale

**Source**: My cross-review of the security-reviewer (DC-2) identified that the security-reviewer's FALSE POSITIVE classification of "no at-rest encryption" is technically correct but creates a documentation gap. Every future contributor or auditor will re-litigate this decision.

**Recommendation**: Add a code comment in `engine/auth.py` near the credential write (the `chmod 600` call) explaining: (1) the threat model (local machine, single user, file-permission-based access control), (2) the industry precedent (Docker, AWS CLI, GitHub CLI, kubectl all use the same pattern), and (3) when this decision should be revisited (if conversus ever runs in a shared-user or server context). This is 5 lines of comments, not a code change.

---

## Position Summary

The cross-review process validated the core of my original review while correctly identifying three areas where I was too narrow:

1. **Priority framework**: The architect's proposal to split P1 into P1-urgent (user-facing, fix before release) and P1-structural (dependency-graph, fix before next spec builds on it) is the right resolution. I move OAuth state validation from P1 to P2 and accept that my --phase recommendation is P1-urgent rather than P1-structural. This preserves the urgency signal without diluting the structural signal.

2. **Implementation depth**: Three of my recommendations (Rec #4 per_agent_outputs, Rec #6 ProviderError.category, Rec #8 decide extraction) were correctly flagged by the architect and security-reviewer as needing more design work than I originally scoped. I revise all three to include the expanded implementation scope: AgentResult union type for error handling, StorageWriter-compatible per_agent_outputs, and engine-layer orchestrate.py with mandatory quality gating.

3. **Audience-specific design**: The convergence across all three cross-reviews on the error architecture gap (architect DC-4, security DC-4, consumer DC-3) reveals a genuine missing piece in my original review. The new Rec A addresses this with a dual-layer ProviderError design. Similarly, the architect's validation of the CLI-to-SDK graduation cliff (T, item 5) provides the basis for new Rec B.

I withdraw no recommendations. I downgrade one (Rec #2, OAuth state, P1 to P2). I expand the implementation scope of three (Recs #4, #6, #8). I add three new recommendations (A: unified error architecture at P2, B: CLI-to-SDK graduation guide at P2, C: credential storage documentation at P3).

The revised priority ordering for developer experience:

| Priority | Recommendations |
|----------|----------------|
| P1-urgent | Rec #1 (--phase choices) |
| P2 | Rec #2 (OAuth state), Rec #3 (run_sync), Rec #4 (per_agent_outputs), Rec #5 (httpx timeout), Rec #6 (ProviderError.category via AgentResult), Rec #7 (provider default mismatch), Rec #8 (decide extraction to engine/orchestrate.py), New Rec A (unified error architecture), New Rec B (CLI-to-SDK graduation) |
| P3 | Rec #9 (CLI/MCP asymmetry docs), Rec #10 (conftest.py), New Rec C (credential storage docs) |

The strongest consensus across all four reviewers: pure function extraction must be preserved, the BYOK race (G3) and RLS mismatch (G5) are unambiguous P1 launch blockers, and the test culture is a genuine strength that enables safe refactoring. The strongest remaining disagreement is whether the async-only SDK design is a feature (architect) or a barrier (devex-advocate) -- I maintain it is both, and `run_sync()` with clear documentation resolves the tension without compromising the async-first architecture.
