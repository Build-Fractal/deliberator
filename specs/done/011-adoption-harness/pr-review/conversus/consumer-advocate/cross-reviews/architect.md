# Cross-Review of Architect's Review — Consumer Advocate Perspective

**Cross-reviewer**: Consumer Advocate
**Reviewing**: Architect's review (`conversus/architect/review.md`)
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: BYOK key injection framed as engineering hygiene vs. consumer trust violation

The architect identifies the `os.environ` race condition (Recommendation #5) as a P1 and prescribes passing the API key directly to the provider constructor. The rationale is "key leakage between concurrent requests" and "thread-safe" construction. This is technically correct but dangerously understated. From the consumer perspective, a BYOK key race means one paying consumer subsidizes another consumer's deliberation -- a billing trust violation, not merely a concurrency bug. The architect's framing as a constructor-injection refactor risks it being treated as a clean-up item rather than the launch blocker it is. My review (Recommendation #3) frames the same bug as a consumer trust and billing issue. If the team internalizes the architect's framing, they may deprioritize this behind the dependency inversion work (Recommendation #1), which has zero consumer impact but is positioned as the architect's top priority. The consumer channel is the only channel where this bug is exploitable -- CLI, SDK, and MCP users run single-process, single-user. The fix priority should reflect who is harmed, not which layer is violated.

**Architect**: "Key leakage between concurrent requests. A user's API key is used for another user's deliberation." (Rec #5)
**Consumer Advocate**: "Consumers could be billed for other users' requests." (Rec #3)

### DC-2: Domain model extraction prioritized over functional production bugs

The architect's top recommendation (P1, Rec #1) is extracting shared domain models from `linter/models.py` to a `conversus.models` package. The rationale is that the inverted dependency will "become a hard blocker when specs 015 and 016 need to import from the engine." This is a forward-looking architectural concern about developer ergonomics for future spec authors. Meanwhile, the RLS/user_id mismatch (architect's Rec #7) and the FRONTEND_URL gap (not in the architect's recommendations at all) are bugs that make the consumer web interface non-functional today. The architect's prioritization inverts the urgency: the dependency inversion causes no user-visible harm in the current release, while G5 and G17 mean no consumer can complete a deliberation or share a result in production. My review places G5 as Recommendation #1 and G17 as Recommendation #2, both ahead of any architectural refactoring. The danger is that the team addresses the architect's priorities first and ships a consumer interface that literally does not work.

**Architect**: "Extract shared domain models to `conversus.models`" as P1 Rec #1; RLS fix as Rec #7.
**Consumer Advocate**: "Fix G5 before any consumer testing" as P1 Rec #1; "Fix G17 before share link testing" as P1 Rec #2.

### DC-3: Plugin hooks rated P1 while rate limiting is absent from architect's recommendations

The architect elevates lifecycle hook call sites to P1 (Rec #2), arguing that without them "every game engine spec will need to modify `run_pipeline()`." This is a maintainability concern for future spec PRs authored by developers. Meanwhile, rate limiting on the public `/api/deliberate` endpoint -- the only publicly accessible endpoint in the entire system -- does not appear in the architect's 10 recommendations at all (G11 is mentioned only in the global synthesis as P2). My review places rate limiting as P1 Rec #4 because the consumer web form can be hit by anyone on the internet and each request spawns a full engine pipeline. The architect's omission implies that protecting the pipeline's internal extension surface is more urgent than protecting it from external abuse. For a consumer-facing product, this ordering is backwards. An unprotected public endpoint is an operational risk today; missing hook call sites are a developer inconvenience in a future PR.

**Architect**: Lifecycle hooks as P1 Rec #2; rate limiting absent from recommendations.
**Consumer Advocate**: Rate limiting as P1 Rec #4; lifecycle hooks not mentioned (correctly -- they have no consumer impact).

### DC-4: The architect never questions whether BYOK is viable for consumers

The architect's entire review evaluates whether the architecture supports the game engine vision (specs 012-020). Every recommendation is about enabling future developer-facing specs: model extraction for clean imports, hook protocols for plugins, per-phase routing for the optimizer, StorageWriter for scenario storage, provider capabilities for the optimizer. None of these affect whether a non-technical consumer can actually use the product. My review (Recommendation #10) flags that BYOK may structurally prevent consumer validation: SC-005 requires 25+ non-technical users, and requiring an API key from a developer console is a multi-step funnel with catastrophic drop-off for non-technical users. The architect's silence on this question is not a neutral omission -- it implicitly validates BYOK as sufficient for the consumer channel by focusing exclusively on the developer channel's needs. If the team follows only the architect's recommendations, they will have a beautifully layered dependency graph that no consumer can reach.

**Architect**: No mention of BYOK viability, SC-005 achievability, or consumer access barriers.
**Consumer Advocate**: "Assess whether BYOK is viable for consumer validation or if a trial/demo mode is needed." (Rec #10)

---

## Tensions

### T-1: "Before merge" vs. "before consumer testing" -- different merge gates

The architect frames recommendations as "must fix before merge" (matching the global synthesis P1 framing). My review frames them as "before consumer testing" or "before public launch." These are different gates. The architect's gate protects code quality for downstream spec authors. My gate protects consumer experience for SC-005 validation. If the team merges with the architect's fixes (dependency inversion, hooks, per-phase routing) but without mine (rate limiting, example questions, error message copy), the code is architecturally clean but the consumer product is incomplete. The tension is real: should the merge gate be "safe for developers to build on" or "safe for consumers to use"? Both are legitimate, but conflating them risks satisfying one while ignoring the other.

**Architect**: "Must Fix Before Merge" framing (Rec #1-3, #5-7).
**Consumer Advocate**: "Before any consumer testing" (Rec #1), "before public launch" (Rec #4).

### T-2: Per-phase model routing as architectural necessity vs. consumer irrelevance

The architect argues per-phase model routing (Rec #3) is P1 because "the config optimizer cannot recommend per-phase model assignments if the engine cannot execute them." This is correct for spec 019's developer-facing optimization surface. From the consumer perspective, per-phase routing is invisible -- consumers provide one API key for one provider, and the engine uses that provider's model for all phases. Consumers do not configure models. The tension is that the architect wants to build the routing infrastructure now to avoid a breaking refactor later, while the consumer channel does not benefit from this work at all. If development capacity is constrained, every hour spent on per-phase routing is an hour not spent on example questions, error messages, or input guidance -- all of which directly impact whether SC-005 is achievable.

**Architect**: Per-phase routing as P1 Rec #3 for spec 019 optimizer.
**Consumer Advocate**: Not mentioned; consumer-facing UX items (Recs #5-7) compete for the same development time.

### T-3: StorageWriter abstraction vs. making the existing storage work

The architect recommends a StorageWriter protocol (Rec #4, P2) to unify filesystem, Supabase, and future scenario storage backends. This is sound forward-looking architecture. But the existing Supabase storage does not work because of the RLS/user_id mismatch (G5). The tension: should the team abstract storage before fixing it, or fix the concrete implementation first? The architect's review treats these as independent items (Rec #4 and Rec #7). From the consumer perspective, they are sequentially dependent -- there is no point abstracting a storage layer that cannot write a single row to the database. Fix G5 first, then abstract.

**Architect**: StorageWriter protocol as P2 Rec #4; RLS fix as P1 Rec #7.
**Consumer Advocate**: RLS fix as P1 Rec #1 (top priority); storage abstraction not mentioned.

### T-4: debate_transcript separation for feature extraction vs. consumer output clarity

The architect flags that `debate_transcript == full_analysis` (Missed Opportunity #6) blocks spec 015 feature extraction, which needs per-phase artifacts separately. From the consumer perspective, the single-blob output is also a readability problem: consumers receive one large markdown document with no structural separation between phases. But the motivations differ. The architect wants machine-parseable per-phase sections for automated feature extraction. Consumers want human-scannable sections with clear visual hierarchy. These goals are compatible but could diverge -- a JSON-structured per-phase breakdown optimized for machine parsing may be less readable for consumers than a well-formatted markdown document with clear headings. The implementation should serve both audiences.

**Architect**: Separate debate_transcript for "deterministic and fast" feature extraction (Missed Opportunity #6).
**Consumer Advocate**: Not explicitly flagged, but progressive disclosure (Alignment section) implies structured output matters for consumer scanning.

### T-5: OAuth state validation urgency

The architect rates OAuth state validation as P1 (Rec #6) with the rationale that it is "a one-line fix for a real security vulnerability." I agree it should be fixed, but it did not appear in my recommendations because the consumer web channel does not use OAuth -- it uses BYOK key paste. The OAuth flow is in the CLI (M004), which targets developers. The tension is minor but illustrative: the architect's P1 list includes items that affect only the developer channel, while my P1 list includes items that affect only the consumer channel. Neither review explicitly separates "P1 for which audience."

**Architect**: OAuth state validation as P1 Rec #6.
**Consumer Advocate**: Not mentioned (OAuth is CLI-only, not consumer-facing).

---

## Safe Agreements

### SA-1: G5 (RLS/user_id mismatch) is a functional blocker that must be fixed before any deployment

The architect (Rec #7) and I (Rec #1) both identify this as a P1 that makes the web interface non-functional. The architect frames it as "all backend inserts and reads fail" and proposes three fix options (service role key, populate user_id, or backend-specific policy). I frame it as "no consumer can complete a deliberation if the database rejects the insert." The diagnosis and proposed fixes are identical. This is the single highest-confidence agreement across both reviews.

**Architect**: "This is a functional bug. If migration 002 is applied, all backend inserts and reads fail." (Rec #7)
**Consumer Advocate**: "This is not a should-fix; it is a functional blocker." (Rec #1)

### SA-2: BYOK key injection must move from os.environ to constructor parameter

The architect (Rec #5) and I (Rec #3) agree on both the diagnosis (race condition under concurrent requests) and the fix (pass key directly to provider constructor). The architect additionally notes that `ModelProvider` protocol already abstracts provider construction, making the fix natural. I additionally note this is the only channel where multiple untrusted users share a server process. The fix is identical; the urgency framing differs (architect: thread safety; consumer advocate: billing trust) but both rate it P1.

**Architect**: "Pass the API key directly to the provider constructor." (Rec #5)
**Consumer Advocate**: "Pass the key directly to the provider constructor." (Rec #3)

### SA-3: The architecture is fundamentally sound and the test culture is exceptional

The architect's executive summary praises "pure function extraction, frozen Pydantic models, protocol-based typing, and event-driven dispatch" with 1,318 tests running 3x spec requirements. My review's alignment section confirms that progressive disclosure, share links, dual-primary paths, and quality indicators all work as specified. Neither review questions the fundamental technical approach. The disagreements are about prioritization and completeness, not about whether the implementation is well-built. This is important context: the cross-review tensions above are about what to do next, not about whether what exists is wrong.

**Architect**: "The architecture is fundamentally sound." (Executive Summary)
**Consumer Advocate**: "The implementation made significant progress on every recommendation I raised." (Executive Summary)

### SA-4: Share links and the self-contained share page are correctly implemented

The architect notes "JSON-serializable pipeline results" support the share/storage path (Alignment section). My review confirms "share links are genuinely self-contained" with SSR and OG metadata (Alignment section). Both reviews implicitly agree this is the primary consumer viral mechanism. The only gap is G17 (FRONTEND_URL), which the architect identifies as a production bug in G5's vicinity but does not elevate to a standalone recommendation, while I place it as P1 Rec #2. The implementation quality is agreed upon; the deployment configuration gap is where we diverge on urgency.

**Architect**: "PipelineResult and ConversusOutput both support model_dump_json()." (Alignment section)
**Consumer Advocate**: "The share page uses SSR with OG metadata and 60-second ISR." (Alignment section)

---

## Summary

The architect's review is thorough, technically precise, and correctly identifies the structural issues that will compound across specs 012-020. However, it is written almost entirely for a developer audience building on the engine, not for the consumer audience using the product. Of the architect's 10 recommendations, zero address consumer UX (example questions, error messages, input guidance, onboarding), and only 3 address bugs that affect consumers (Recs #5, #6, #7 -- and #6 is CLI-only). The most dangerous pattern is the prioritization inversion: dependency extraction and lifecycle hooks are rated P1 ahead of rate limiting, FRONTEND_URL, and the BYOK viability question. If the team has limited capacity and follows the architect's priority ordering, they will resolve internal code structure issues while leaving the consumer-facing product non-functional in production and unreachable for validation.
