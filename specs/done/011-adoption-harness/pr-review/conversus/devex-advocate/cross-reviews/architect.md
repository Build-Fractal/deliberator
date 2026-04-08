# Cross-Review of Architect's Review — DevEx Advocate Perspective

**Cross-reviewer**: Developer Experience Advocate
**Reviewing**: Architect review (`conversus/architect/review.md`)
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: Shared domain model extraction vs. first-hour developer experience

The architect's top recommendation (P1, Rec #1) is extracting shared domain models to `conversus.models` — a new package that both linter and engine depend on. This is architecturally correct but creates a tension the architect does not address: **the refactor will break every existing import path** across the codebase, affecting every test, every example, and every developer who has already started using the current package structure. My review (Missed Opportunity #1) identifies that no "getting started" friction analysis exists — we do not know whether developers can reach a working deliberation in under 5 minutes. Performing a large-scale internal refactor before establishing and documenting the stable import surface risks shipping a v1 where the imports developers learn from early examples become stale within one release cycle. The architect frames this as "exponentially harder as more code depends on current import paths" (Rec #1 risk), which is true for internal consumers but equally true for external ones. **The contradiction**: the architect wants to fix the dependency graph before merge to protect future spec authors, but doing so without simultaneously publishing a stable public API contract means the fix itself becomes the source of future import churn for SDK users.

**Resolution path**: Perform the extraction *and* define `conversus.models` as the documented public import surface in the same PR. My review's recommendation #4 (promote per_agent_outputs into SDK Result) and the architect's Rec #1 should be bundled — the model extraction is the moment to get the public API right, not just the internal dependency graph.

### DC-2: Plugin lifecycle hooks as P1 merge blocker vs. adoption-first scope

The architect elevates plugin lifecycle hooks to P1 (Rec #2), arguing that "every game engine spec will need to modify `run_pipeline()` to inject its hook calls, creating merge conflicts." My review does not mention plugin hooks at all — because from a DevEx perspective, **no developer adopting conversus today needs plugin hooks**. The 011-adoption-harness is the adoption story; specs 016-019 are the game engine story. The architect's own executive summary acknowledges the EventEmitter is "observe-only" and works well for its current purpose (SSE streaming in M005 validates this). Making empty hook call sites a P1 merge blocker on the adoption harness PR means delaying the feature that developers *can* use today (CLI, SDK, web) to protect an internal surface that developers *might* use in a future spec. My review prioritizes removing broken --phase choices (P1), OAuth state validation (P1), and run_sync() (P2) because those gate the developer's first session. **The contradiction**: the architect treats internal extensibility debt as equally urgent to user-facing functionality debt. For adoption, they are not. A developer who cannot run `conversus decide` without hitting a ValueError (my Rec #1) will never reach the point where they care about plugin hooks.

**Resolution path**: Ship the adoption harness with empty hook call sites as a P2 (not P1) — add them, but do not block merge on their absence. The architect's Rec #2 is sound engineering; the priority assignment is wrong for an adoption-focused PR.

### DC-3: Per-phase model routing as P1 vs. single-model simplicity for onboarding

The architect's Rec #3 promotes per-phase model routing to P1, arguing the config optimizer (spec 019) cannot function without it. My review does not mention per-phase routing because from the developer's perspective, **a single `--model` flag is the correct v1 UX**. New users should not need to understand the 5-phase pipeline to run their first deliberation. The architect acknowledges the implementation is small ("No changes to dispatch_phase's signature needed") but still rates it P1. My review's Missed Opportunity #7 flags the *opposite* problem: EngineConfig.provider defaults to "anthropic" while runtime defaults to "mock," which is confusing precisely because the current single-model path is already inconsistent. Adding a second dimension of model configuration (per-phase) before resolving the existing default mismatch will compound the confusion. **The contradiction**: the architect wants richer configuration surface area; my review wants the existing surface area to be consistent first.

**Resolution path**: Fix the provider/model default mismatch (my Rec #7) first, then add per-phase routing as P2 with it disabled by default (empty `phase_models` dict). The feature should exist in the engine but not be surfaced in the CLI until spec 019 lands.

---

## Tensions

### T-1: StorageWriter abstraction (architect P2) vs. decide service extraction (devex P2)

The architect's Rec #4 proposes a StorageWriter protocol to abstract OutputManager's filesystem writes, motivated by three storage backends (filesystem, Supabase, scenario YAML). My review's Rec #8 proposes extracting the `decide` orchestration into a service function, motivated by the command accumulating too many responsibilities. Both are P2, both touch OutputManager's consumers, and both should happen before the codebase grows further — but they pull in different directions. The StorageWriter abstraction pushes OutputManager to become more generic and protocol-based; the service extraction pushes the decide command to become thinner and delegate to a function that *uses* OutputManager. If done in the wrong order, the service extraction hard-codes a filesystem-coupled OutputManager, and the StorageWriter refactor then requires touching the service function too. **Tension**: the architect is working bottom-up (abstract the storage layer), while I am working top-down (thin the command surface). Both are right; sequencing matters.

**Suggested sequencing**: Extract the decide service function first (it is a pure refactor with no API change), then introduce StorageWriter as a dependency of the service function rather than of OutputManager directly.

### T-2: Retroactive move elimination (architect P2) vs. getting multi-round output working at all

The architect's Rec #10 proposes replacing `retroactive_move_to_round_1()` with an upfront directory structure. My M002 review (Issue #6, P2) flags the same mutation concern. However, my DevEx review does not prioritize this because multi-round deliberations are a power-user feature. The tension is between architectural cleanliness (the architect's concern — stale path references, non-filesystem incompatibility) and pragmatic adoption (my concern — single-round is the onboarding path, and it works fine). The retroactive move is ugly but only fires when `rounds > 1`, which is an advanced config option. **Tension**: the architect sees a footgun that will hurt future spec implementers; I see a rarely-triggered edge case that does not affect first-hour experience. Both evaluations are valid for their respective audiences.

### T-3: Provider capability negotiation (architect P2) vs. simpler provider onboarding

The architect's Rec #8 proposes adding `capabilities()` to ModelProvider, returning a frozenset of capability tokens. My review does not address this because from a DevEx perspective, the current text-in/text-out ModelProvider protocol is the *simplest possible interface* for someone implementing a custom provider. Adding a mandatory `capabilities()` method (even with a default return) increases the surface area a developer must understand to write a provider. The architect frames this as enabling the config optimizer (spec 019); I frame the current simplicity as enabling adoption (spec 011). **Tension**: richness for framework consumers vs. simplicity for framework contributors.

### T-4: StructuredDeliberation per-phase separation (architect MO-6) vs. simpler output for SDK consumers

The architect identifies that `debate_transcript == full_analysis` (G32) and proposes emitting per-phase sections in a StructuredDeliberation, arguing spec 015 needs phase-level artifacts. My review's Rec #4 asks for per_agent_outputs in the SDK Result — a related but different slicing of the same data. The architect wants output split by *phase*; I want it split by *agent*. Both are valid decompositions and both serve different consumers (feature extraction vs. training data). **Tension**: these two asks could result in the SDK Result carrying both `per_phase_outputs` and `per_agent_outputs`, which is a combinatorial explosion that adds weight to a model the architect's own review praises for being frozen and clean.

### T-5: Security fix prioritization — agreement on issues, disagreement on urgency

The architect rates BYOK key injection (Rec #5, P1), OAuth state (Rec #6, P1), and RLS mismatch (Rec #7, P1) as three separate P1 items. My review rates OAuth state as P1 (Rec #2) but does not separately call out BYOK or RLS — instead I elevate developer-facing issues like run_sync() (Rec #3, P2) and ProviderError.category preservation (Rec #6, P2). We agree these security issues exist; we disagree on whether they all must block merge. The BYOK race condition only manifests under concurrent web requests (M005's web interface is the newest, least-adopted surface), and the RLS mismatch is a migration that may not yet be deployed. **Tension**: the architect treats all security issues as equally urgent; I triage based on the likelihood a developer actually hits them during adoption.

---

## Safe Agreements

### SA-1: The linter-to-engine dependency inversion must be resolved

The architect's entire review centers on this as the "critical architectural issue" (executive summary). My M002 review (Coupling Analysis) independently identified the same three dependency sites: `engine/templates.py -> linter/models.py`, `engine/phases.py -> linter/quality.py`, `engine/sdk.py -> linter/output_contract.py`. My DevEx review does not explicitly list this because it is not a developer-facing issue, but I fully agree it is real technical debt. The disagreement is only on timing and bundling (see DC-1), not on the diagnosis. Both reviews cite the same evidence.

### SA-2: Broken --phase choices is the highest-priority user-facing bug

The architect's Rec #9 (P2) and my Rec #1 (P1) both identify the same issue: `run --phase` advertises choices that crash at runtime. We disagree slightly on priority (the architect rates it P2 because it is a small fix; I rate it P1 because it is a trust-destroying first impression), but we agree it must be fixed before merge. The architect's framing — "Advertising features that crash is worse than not advertising them" — is exactly my position. This is the safest agreement in both reviews: the fix is a 1-line change to the click.Choice list.

### SA-3: OAuth state validation is a P1 security fix

The architect's Rec #6 and my Rec #2 identify the identical vulnerability with the identical fix: compare `state_returned` to `state_local` before token exchange. Both reviews cite the M004 review (Security Assessment, L46-48). Both agree the fix is trivial (one comparison) and the risk is real (CSRF in the auth flow). No disagreement on diagnosis, priority, or resolution.

### SA-4: Pure function extraction is the correct architecture and must be preserved

The architect's Alignment section leads with pure function extraction as "the correct architecture for a system that will be extended by plugins." My review's executive summary independently identifies the same: "The strongest finding across all milestone reviews is the pure-function extraction pattern." Both reviews agree this pattern is what makes the CLI, SDK, and MCP tools independently testable and composable. The architect frames this through the lens of plugin composability; I frame it through the lens of contributor experience. Same conclusion, different motivations.

---

## Summary

The architect's review is thorough, well-evidenced, and architecturally rigorous. The three dangerous contradictions all follow the same pattern: the architect optimizes for the *next* set of consumers (spec 016-020 implementers) while I optimize for the *first* set of consumers (developers adopting conversus today). These are not incompatible goals, but they produce different priority orderings. The key resolution is sequencing: ship the adoption surface clean (fix crashes, add run_sync, resolve defaults), then perform the structural refactors (model extraction, hook sites, per-phase routing) in a fast-follow PR before spec 016 begins. This avoids blocking the adoption launch on game-engine preparation while still honoring the architect's valid concern that the dependency graph must be clean before specs 015-020 build on it.
