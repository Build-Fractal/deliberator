# Architect Revision — Iteration 1

**Reviewer**: Systems Architect
**Date**: 2026-03-24
**Revision basis**: Original `review.md` + cross-reviews from security-reviewer, devex-advocate, consumer-advocate + my cross-reviews of those three

---

## Recommendation Dispositions

### Recommendation 1: Extract shared domain models to `conversus.models` — MODIFIED

**Original**: P1 merge blocker. Extract `Phase`, `TemplateContext` subclasses, `ModeSchema`, `VariablesSchema` from `linter/models.py` to a `conversus/models/` package.

**Modification**: Downgrade from P1 merge blocker to P1-structural (fix before spec 016 begins, not before this PR merges). Bundle with public API contract definition.

**Rationale**: Three cross-reviews independently challenged my priority assignment, and each exposed a genuine flaw in my reasoning:

- **Security-reviewer (DC-2)**: "Shipping with an inverted dependency graph is safe; shipping with the BYOK os.environ race is not." This is correct. The dependency inversion causes zero user-visible harm in the current release. My framing conflated structural severity with merge urgency.
- **Consumer-advocate (DC-2)**: "The dependency inversion causes no user-visible harm in the current release, while G5 and G17 mean no consumer can complete a deliberation or share a result in production." This is also correct. I placed an internal code organization concern above functional bugs.
- **DevEx-advocate (DC-1)**: "The refactor will break every existing import path across the codebase, affecting every test, every example, and every developer who has already started using the current package structure." This is the strongest challenge. The extraction without simultaneously defining a stable public import surface risks creating the very import churn it aims to prevent.

I maintain that the dependency inversion is real and will compound -- every future spec that imports from `engine/` transitively pulls `linter/`. But the cross-reviews are right that this is a "fix before next spec builds on it" concern, not a "fix before any user touches it" concern. The DevEx advocate's resolution -- perform the extraction and define `conversus.models` as the documented public import surface in the same PR -- is the correct approach.

**Revised recommendation**: Extract shared domain models and define the public API surface in a dedicated PR after the adoption harness merges but before spec 016 work begins. This is sequencing, not deferral.

### Recommendation 2: Add lifecycle hook call sites to run_pipeline() — MODIFIED

**Original**: P1 merge blocker. Define `PluginHook` protocol, add 4 hook call sites in `run_pipeline()`, accept `hooks: dict[HookPoint, list[PluginHook]]` parameter.

**Modification**: Downgrade from P1 merge blocker to P2. Add the hook call sites, but do not block the adoption harness merge on their absence.

**Rationale**: The DevEx advocate's challenge (DC-2) is well-targeted: "No developer adopting conversus today needs plugin hooks. The 011-adoption-harness is the adoption story; specs 016-019 are the game engine story." This is correct. My original argument -- "every game engine spec will need to modify `run_pipeline()`" -- is a valid concern about future merge conflicts, but it does not justify blocking the current PR. The EventEmitter validates the observe-only pattern under real async load (M005 SSE streaming). The hook protocol is a different mechanism serving different consumers (plugins that return results vs. observers that receive events).

I still maintain that adding empty hook call sites is zero-cost and high-value. But the DevEx advocate is right that the priority assignment was wrong for an adoption-focused PR. The consumer advocate (DC-3) reinforces this: "An unprotected public endpoint is an operational risk today; missing hook call sites are a developer inconvenience in a future PR."

**Revised recommendation**: Add hook call sites as P2 in this PR or in a fast-follow before spec 016 begins. Do not block merge.

### Recommendation 3: Wire per-phase model routing in EngineConfig and dispatch — MODIFIED

**Original**: P1 merge blocker. Add `phase_models: dict[str, str]` to `EngineConfig`, resolve per phase in `run_pipeline()`.

**Modification**: Downgrade from P1 merge blocker to P2. Additionally, fix the provider/model default mismatch first.

**Rationale**: Two cross-reviews challenged this effectively:

- **DevEx-advocate (DC-3)**: "A single `--model` flag is the correct v1 UX. New users should not need to understand the 5-phase pipeline to run their first deliberation." This is a valid point about cognitive load. More importantly, the DevEx advocate identified that `EngineConfig.provider` defaults to "anthropic" while runtime defaults to "mock" -- adding a second dimension of model configuration before resolving the existing default inconsistency will compound confusion.
- **Consumer-advocate (T-2)**: Per-phase routing is "invisible" to consumers and competes for development time with consumer-facing UX improvements.

My original argument that spec 019's config optimizer "cannot function without it" remains technically true, but spec 019 has not started. The implementation is small, but the priority was wrong.

**Revised recommendation**: Fix the provider/model default mismatch (DevEx's finding) first. Add `phase_models` to `EngineConfig` as P2 with the dict empty by default. Do not surface in CLI until spec 019 lands. Credit: DevEx-advocate DC-3 resolution path.

### Recommendation 4: Introduce StorageWriter protocol for OutputManager — MAINTAINED (P2)

**Original**: P2. Define `StorageWriter` protocol, inject into `OutputManager`.

**Disposition**: Maintained at P2, with modified sequencing per DevEx advocate's suggestion.

**Rationale**: No cross-review challenged the substance of this recommendation. The DevEx advocate (T-1) proposed extracting the `decide` service function first, then introducing `StorageWriter` as a dependency of the service function rather than of `OutputManager` directly. This is better sequencing -- the service extraction is a pure refactor with no API change, and it creates the right injection point for `StorageWriter`. The consumer advocate (T-3) correctly noted that abstracting storage before fixing the RLS mismatch is backwards. Both are right.

**Revised sequencing**: Fix G5 (RLS) first. Extract decide service function (DevEx). Then introduce StorageWriter. Same destination, better path.

### Recommendation 5: Fix BYOK key injection via constructor instead of os.environ — MAINTAINED (P1)

**Original**: P1. Pass API key directly to provider constructor.

**Disposition**: Maintained at P1. Strengthen urgency framing.

**Rationale**: All three cross-reviews reinforce this as the highest-priority fix, and the consumer advocate's reframing (DC-1) is superior to mine: "One paying consumer subsidizes another consumer's deliberation -- a billing trust violation, not merely a concurrency bug." The security reviewer (SA-1) confirms both the diagnosis and fix are identical across all reviews. The security reviewer additionally notes that the provider constructors already accept the key parameter, making the fix even simpler than I described.

I accept the consumer advocate's criticism that my framing as "constructor-injection refactor" understated the severity. This is a trust violation, not an engineering cleanup. The security reviewer's observation (DC-4) that both reviews agree the complexity is small, not medium (contradicting the synthesis), strengthens the case for fixing before merge.

**No change to recommendation substance. Framing updated: this is a consumer trust and billing defect, not just a concurrency bug.**

### Recommendation 6: Fix OAuth state validation — MODIFIED

**Original**: P1. Add `assert state_returned == state_local` before token exchange.

**Modification**: Downgrade to P2. Still fix in this PR due to near-zero cost.

**Rationale**: The security reviewer's cross-review (DC-1) provides a more rigorous threat model than mine: "The code-paste flow has no redirect URI, which means the classical OAuth CSRF attack vector (intercepting the redirect) does not apply. An attacker would need to convince a victim to paste an attacker-controlled `code#state` into their own terminal." My P1 rating was driven by fix triviality rather than exploitation probability -- that is the wrong way to assign severity.

In my cross-review of the security reviewer, I accepted this analysis: "Security-reviewer's threat model analysis is technically superior to mine." I should follow through on that concession. The fix should still land in this PR because the cost is essentially zero, but labeling it P1 alongside the BYOK race and RLS mismatch dilutes the urgency signal for those genuinely critical items.

**Revised recommendation**: P2. Fix in this PR. Add a code comment at the state generation site noting that local validation becomes critical if the flow ever migrates to redirect-based auth. Credit: security-reviewer DC-1.

### Recommendation 7: Fix RLS / user_id mismatch in Supabase migration — MAINTAINED (P1)

**Original**: P1. Use service role key, populate user_id, or replace policy.

**Disposition**: Maintained at P1 with stronger fix direction.

**Rationale**: This is the single highest-confidence agreement across all four reviews. The security reviewer (SA-2), consumer advocate (SA-1), and DevEx advocate all converge on the same diagnosis. The consumer advocate's framing -- "This is not a should-fix; it is a functional blocker" -- is the correct characterization. If migration 002 is applied, the web interface does not work. Period.

The security reviewer's cross-review (T-2) adds a nuance I should acknowledge: the service role key bypasses RLS entirely, meaning "if the web backend ever has a request injection vulnerability, RLS would not protect against data exfiltration." This is a valid long-term concern. However, for the current anonymous-user model, the service role key is pragmatically correct.

**Revised recommendation**: Use service role key for now (all reviews converge on this). Document in a code comment or ADR that FR-017 (user accounts) must switch to per-user JWTs with proper user_id population. Credit: security-reviewer T-1 for the long-term concern.

### Recommendation 8: Extend ModelProvider with optional capabilities() method — MODIFIED

**Original**: P2. Add `capabilities() -> frozenset[str]` to the protocol.

**Modification**: Downgrade to P3. Defer until spec 019 work begins.

**Rationale**: The DevEx advocate (T-3) makes a strong case: "The current text-in/text-out ModelProvider protocol is the simplest possible interface for someone implementing a custom provider. Adding a mandatory capabilities() method increases the surface area a developer must understand to write a provider." This is correct for adoption. The protocol's simplicity is a feature, not a gap, for spec 011. My recommendation was optimizing for the config optimizer (spec 019) at the expense of the current adoption surface.

The security reviewer does not mention capabilities at all, confirming it has no security surface. The consumer advocate does not mention it, confirming it has no consumer impact. When three out of three cross-reviews either challenge or ignore a recommendation, the signal is clear: this is premature.

**Revised recommendation**: P3. Add when spec 019 actually needs it. The protocol's extensibility (structural subtyping via Protocol, not ABC) means adding `capabilities()` later is non-breaking.

### Recommendation 9: Remove unsupported phase choices from CLI --phase — MODIFIED (UPGRADE)

**Original**: P2. Remove unimplemented values from `click.Choice` list.

**Modification**: Upgrade to P1-urgent.

**Rationale**: The DevEx advocate (SA-2) makes a convincing case that I underrated this: "Advertising features that crash is worse than not advertising them" was my own framing, yet I rated it P2 while the DevEx advocate rated it P1. The DevEx advocate's reasoning is sound: this is a trust-destroying first impression bug. A user who runs `conversus run --phase cross-review` and gets a `ValueError` will not investigate the dependency graph or read the roadmap -- they will conclude the tool is broken and leave.

My P2 rating was based on the trivial fix size (1-line click.Choice edit). But as I noted in my cross-review of the DevEx advocate (DC-1), urgency and severity are different axes. The fix is small (low severity in terms of blast radius) but urgent (first thing a user hits). For an adoption-focused PR, urgency should dominate.

**Revised recommendation**: P1-urgent. Fix before any user testing. The 1-line fix has outsized impact on first impressions. Credit: devex-advocate SA-2.

### Recommendation 10: Replace OutputManager.retroactive_move_to_round_1() with immutable pattern — MAINTAINED (P2)

**Original**: P2. Construct multi-round directory structure upfront.

**Disposition**: Maintained at P2, with acknowledgment that it is not urgent for adoption.

**Rationale**: The DevEx advocate (T-2) correctly notes that multi-round deliberations are a power-user feature and the retroactive move "only fires when `rounds > 1`." For adoption, single-round works fine. The security reviewer does not mention it (no security surface). The consumer advocate does not mention it (no consumer impact).

The architectural concern remains valid: stale path references are a footgun, and the pattern cannot work for non-filesystem backends. But this is exactly the kind of debt that can safely sit at P2 until either spec 020 (scenario storage) or the StorageWriter abstraction lands. No cross-review challenged the diagnosis, only the timing.

**Maintained as P2. No urgency change.**

---

## New Recommendations

### New Recommendation A: Add rate limiting to POST /api/deliberate (P1-urgent)

**Source**: Consumer-advocate DC-3 and recommendation #4. Also identified in M005 review (line 92) and global synthesis G11 (P2).

The consumer advocate is right that I omitted this entirely, and the omission is indefensible. The `/api/deliberate` endpoint is the only publicly accessible endpoint in the system. Each request spawns a full engine pipeline with multiple LLM calls. Without rate limiting, a single actor can exhaust the operator's compute budget or degrade service for all users. This is not a theoretical concern -- it is the most basic operational protection for a public-facing web endpoint.

My original review did not include rate limiting because I was focused on the dependency graph and extension point surface. The consumer advocate correctly identifies this as a prioritization inversion: "protecting the pipeline's internal extension surface is more urgent than protecting it from external abuse" is backwards for a consumer-facing product.

**Recommendation**: Add per-IP rate limiting middleware to the `/api/deliberate` POST endpoint before public launch. A simple token-bucket or sliding-window approach is sufficient. This is a well-understood infrastructure pattern with readily available FastAPI middleware (slowapi, or a simple custom implementation). P1-urgent for any deployment where the web interface is publicly accessible.

### New Recommendation B: Add FRONTEND_URL to deployment configuration (P1-urgent)

**Source**: Consumer-advocate recommendation #2, M005 review (line 72), global synthesis G17 (P2).

This was captured in the M005 review and synthesis as G17 but I did not elevate it to a standalone recommendation. The consumer advocate's framing is correct: "A consumer who shares a link that goes to localhost will not come back." Share links are the primary viral mechanism for the consumer channel. If `FRONTEND_URL` defaults to `localhost:3000` in production, every share link is broken. This is a deployment configuration bug with a trivial fix (add the env var to `.do/app.yaml`) and catastrophic consumer impact.

**Recommendation**: Add `FRONTEND_URL` to the DigitalOcean app spec and any other deployment manifests. Verify share links resolve correctly in the deployed environment. P1-urgent.

### New Recommendation C: Establish two-dimensional priority framework (Process)

**Source**: Security-reviewer DC-3 resolution; DevEx-advocate cross-review tension T-1; consumer-advocate T-1.

All three cross-reviews exposed the same meta-problem: my original review used a single P1 label for items with fundamentally different urgency profiles. The security reviewer proposes "two priority dimensions: production safety and architectural readiness." The DevEx advocate proposes splitting "urgency (user-facing, fix before release) from severity (structural, fix before next spec builds on it)." The consumer advocate asks "should the merge gate be 'safe for developers to build on' or 'safe for consumers to use'?"

These are all describing the same insight: this PR serves two audiences (adopters today, spec implementers tomorrow) and a single priority axis cannot capture both.

**Recommendation**: Adopt a two-axis priority framework for the remaining triage:
- **P1-urgent**: Fix before any user or consumer testing. Production safety and user trust. Items: G3 (BYOK race), G5 (RLS mismatch), G17 (FRONTEND_URL), G4 (broken --phase), rate limiting, OAuth state validation.
- **P1-structural**: Fix before spec 016 work begins. Architectural readiness. Items: G1 (dependency inversion + public API surface), lifecycle hooks, per-phase routing.
- P2 and P3 retain their current meanings.

---

## Position Summary

### What I Got Wrong

1. **Priority conflation.** My original review used P1 for six recommendations spanning security defects (BYOK race, RLS mismatch), user-facing bugs (broken --phase), and architectural preparation (dependency inversion, lifecycle hooks, per-phase routing). All three cross-reviews identified this as the central problem with my review. The security reviewer said it "dilutes the urgency signal." The DevEx advocate said it "confuses urgency with severity." The consumer advocate said it risks the team "resolving internal code structure issues while leaving the consumer-facing product non-functional." They are all correct.

2. **Missing consumer and operational perspective.** My original review contained zero recommendations addressing consumer UX, rate limiting, or deployment completeness. The consumer advocate (DC-3, DC-4) and DevEx advocate (DC-2) both identified this gap. Rate limiting on a public endpoint is more urgent than lifecycle hooks for a spec that has not started. FRONTEND_URL is more urgent than per-phase model routing. I was optimizing for the audience that will build on this code next quarter while neglecting the audience that will use it next week.

3. **OAuth state severity inflated.** The security reviewer's threat model analysis is more rigorous. The code-paste flow reduces the attack surface compared to redirect-based OAuth. My P1 was based on fix triviality, not exploitation probability.

### What I Got Right

1. **The linter/engine dependency inversion is real and must be resolved.** All three cross-reviews that address G1 agree the diagnosis is correct (DevEx SA-1: "I fully agree it is real technical debt"; security-reviewer DC-2: "a legitimate architectural concern"). The disagreement is only on timing, and I now accept their timing argument. But the fix must happen before spec 016 builds on the current import graph.

2. **The BYOK os.environ race is the highest-priority security fix.** Every review converges here. My diagnosis, fix direction, and P1 classification are validated by all three cross-reviews. I accept the consumer advocate's stronger framing (billing trust violation) over my original engineering framing (concurrency bug).

3. **The RLS mismatch is a deployment blocker.** Universal agreement across all reviews. No revision needed.

4. **The pure function extraction architecture is correct and must be preserved.** Every review independently validates this as the strongest architectural pattern in the PR. This is the foundation that makes the CLI, SDK, MCP, and web interface independently testable and composable.

5. **Extension points will be needed before the game engine specs.** The hook protocol, StorageWriter, and per-phase routing recommendations were over-prioritized for this PR but remain architecturally necessary. The cross-reviews challenge the timing, not the substance. I accept the timing correction while maintaining that these must land before their respective consuming specs begin work.

### Revised Priority Ordering

**Fix before merge (P1-urgent):**
1. G3 — BYOK key injection via constructor (all reviews agree)
2. G5 — RLS / user_id mismatch (all reviews agree)
3. G17 — FRONTEND_URL in deployment config (consumer-advocate, M005 review)
4. G4 — Remove broken --phase choices (devex-advocate, architect revised)
5. G11 — Rate limiting on /api/deliberate (consumer-advocate, new recommendation)
6. G2 — OAuth state validation (all reviews agree on fix; P2 severity but near-zero cost)

**Fix before spec 016 begins (P1-structural):**
7. G1 — Shared domain model extraction + public API surface definition
8. G8 — Lifecycle hook call sites in run_pipeline()
9. G6 — Per-phase model routing in EngineConfig (after fixing provider/model default mismatch)

**Fix as capacity allows (P2):**
10. StorageWriter abstraction (after decide service extraction)
11. OutputManager retroactive move elimination
12. CORS restriction to explicit methods/headers
13. httpx timeout on all calls
14. ProviderError.category preservation (requires AgentResult union type design)

**Defer to consuming spec (P3):**
15. ModelProvider capabilities() — add when spec 019 needs it
