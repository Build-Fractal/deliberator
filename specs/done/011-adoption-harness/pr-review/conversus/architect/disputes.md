# Architect — Final Disputes and Convergence

**Reviewer**: Systems Architect
**Date**: 2026-03-24
**Phase**: 4 (Final Disputes)
**Inputs**: All four revised positions (architect, security-reviewer, devex-advocate, consumer-advocate)

---

## Remaining Disputes

### Dispute 1: Rate limiting severity — P2 is correct, but the security-reviewer's rationale is incomplete

The security-reviewer and I converge on P2 for rate limiting. The consumer-advocate has downgraded to P2. But the security-reviewer's rationale -- "under BYOK, attackers bear their own API costs" -- is only half the story, and I want to prevent this reasoning from becoming doctrine.

The BYOK cost-shifting argument applies to LLM provider costs. It does not apply to server-side compute costs. Each `/api/deliberate` request executes question classification, config parsing, preset loading, agent construction, quality gating, and output formatting before any provider call. On the DO basic-xxs instance, an unauthenticated request flood that provides invalid API keys would still saturate CPU and memory with pre-provider pipeline work. The requests would fail at the provider, but only after consuming server resources.

P2 is the right severity because the system is not yet deployed and fixing G3/G5/G17 is more urgent. But the team should not defer rate limiting based on the belief that BYOK makes it unnecessary. BYOK shifts the LLM cost risk; it does not eliminate the resource exhaustion risk. The rate limiting implementation should protect the server, not just the provider budget.

I flag this because the devex-advocate's revised position correctly identifies that rate limiting is a provider-layer concurrency concern, not just a FastAPI middleware concern. The implementation should throttle at the engine entry point (the future `run_deliberation()` function in `engine/orchestrate.py`), not only at the HTTP layer. This ensures SDK deployers, MCP servers, and the web API all benefit from the same protection.

### Dispute 2: OAuth state validation — the security-reviewer's P1 upgrade is wrong, and the devex-advocate's P2 is correct

The security-reviewer revised upward to P1. The devex-advocate revised downward to P2. I revised to P2 in my own revision. The consumer-advocate did not take a strong position.

The security-reviewer's three justifications for upgrading are: (a) deferred 1-line fixes tend to stay deferred, (b) FR-017 will add redirect-based OAuth making this a real CSRF vulnerability, and (c) the cost of keeping it at P1 is zero.

I reject argument (c) as the reasoning is exactly backwards. The cost of keeping it at P1 is signal dilution. If the P1 list contains three items (G3, G5, RLS mismatch) that cause the application to malfunction for every user, plus one item (OAuth state) that requires an attacker to convince a victim to paste an attacker-controlled value into their own terminal, then "P1" stops meaning "the application is broken without this fix." It starts meaning "we should probably do this." That weakens every P1 on the list.

Arguments (a) and (b) are valid but prove the wrong conclusion. The correct response to "this will be needed when FR-017 lands" is to tag it as a prerequisite for FR-017, not to inflate its severity in the current PR. The correct response to "deferred fixes stay deferred" is process discipline, not severity inflation.

The devex-advocate's position is the most precise: P2 with zero implementation cost, implemented in the same pass as P1 fixes. This preserves the severity signal while ensuring the fix actually ships. I align with the devex-advocate here.

### Dispute 3: The consumer-advocate's "consumer launch checklist" risks creating a parallel gate that does not exist in the spec

The consumer-advocate's New-1 recommendation proposes "separate channel-readiness criteria for the consumer web form" with a "consumer launch checklist" that gates SC-005 testing. While the underlying concern is legitimate -- G17 affects consumers more than developers -- the proposed mechanism is problematic.

The spec defines success criteria (SC-001 through SC-006) and functional requirements (FR-001 through FR-021). A "consumer launch checklist" that is distinct from these creates an informal gate with no spec authority. Who decides when the checklist is satisfied? What happens when a checklist item contradicts a spec priority? The consumer-advocate's own revision acknowledges that "the sequencing is a product strategy decision," yet the checklist would encode product strategy decisions as engineering gates.

The correct mechanism already exists: the P1-urgent items (G3, G5, G17) are merge blockers that affect all channels including consumer. Once those are fixed, the consumer channel is functional. The P2 items the consumer-advocate identifies (input guidance, error copy, feedback richness) are genuinely important for SC-005 achievability, but they should be tracked as P2 items in the existing priority framework, not elevated through a separate gating mechanism.

I do not dispute the consumer-advocate's assessment that these items matter for SC-005. I dispute the proposed mechanism for tracking them.

### Dispute 4: The `quick()` convenience function proposed by the devex-advocate conflates two distinct API layers

The devex-advocate's New Rec B proposes a `conversus.quick(question, provider=None, model=None)` synchronous convenience function that "mirrors the CLI `decide` command's behavior." This was partially my suggestion (I proposed a migration guide and matching defaults), but the `quick()` function as specified has an architectural problem.

The function would need to internally perform: auth resolution, provider construction, EngineConfig assembly, quality gating, pipeline execution, output formatting, and result construction. This is the same scope as the `run_deliberation()` orchestration function the devex-advocate proposes in Rec #8. If `quick()` calls `run_deliberation()`, it is a one-line wrapper that adds nothing over `asyncio.run(run_deliberation(...))`. If it reimplements any of these steps, it creates a second orchestration path that must be kept in sync.

The devex-advocate frames this as "the bridge between CLI and SDK." The actual bridge is documentation: a "CLI to SDK" section that maps every CLI flag to its SDK equivalent (which the devex-advocate also proposes). The `quick()` function is either redundant with `run_deliberation()` or a maintenance burden. I prefer the documentation-only approach.

This is not a strong dispute -- if the team wants `quick()`, the implementation cost is near-zero as a wrapper around `run_deliberation()`. But I want to flag that adding convenience functions to the public API surface creates backwards-compatibility obligations. Once `quick()` exists, removing it is a breaking change.

---

## Convergence

### Convergence 1: P1-urgent list — G3, G5, G17, G4

All four reviewers converge on G3 (BYOK key race) and G5 (RLS/user_id mismatch) as unambiguous P1 merge blockers. The consumer-advocate and I converge on G17 (FRONTEND_URL) as P1-urgent for any consumer testing. The devex-advocate and I converge on G4 (broken --phase choices) as P1-urgent for any user testing. The security-reviewer does not contest G4 or G17.

The final P1-urgent list across all four reviewers is: G3, G5, G17, G4. These must be fixed before merge.

### Convergence 2: Two-axis priority framework

All four reviewers either proposed or accepted the split between P1-urgent (fix before users touch it) and P1-structural (fix before the next spec builds on it). The security-reviewer proposed "production safety vs. architectural readiness." The devex-advocate proposed "urgency vs. severity." The consumer-advocate proposed "functional blocker vs. product strategy." These are all describing the same insight with different vocabulary.

The consensus framework:
- **P1-urgent**: Production safety, user trust, functional correctness. Gate: merge or consumer testing.
- **P1-structural**: Dependency hygiene, API surface stability, extension point readiness. Gate: next spec beginning work.
- **P2**: Important improvements without a hard gate.
- **P3**: Nice-to-have, defer to consuming context.

### Convergence 3: The pure function extraction architecture is the PR's strongest pattern

Every reviewer independently validates this as the correct foundation. The security-reviewer notes it enables testable auth resolution. The devex-advocate notes it enables the `run_deliberation()` extraction. The consumer-advocate notes it makes the web interface independently testable. I note it makes the engine composable across four consumer channels (CLI, SDK, MCP, web).

This is the non-negotiable architectural invariant. Any fix, refactor, or extension must preserve the property that the engine's core functions are pure, stateless, and callable without framework dependencies.

### Convergence 4: RLS fix approach — service role key with documented FR-017 migration path

All four reviewers converge on: (a) use the service role key now, (b) document that RLS user-scoped policies are placeholder, (c) enforce real RLS when FR-017 adds user authentication. The security-reviewer adds the requirement for explicit code comments in `web/db.py` and `supabase/migrations/002_rls_user_scoped.sql`. The devex-advocate adds the concern about the migration being dead code. The consumer-advocate adds the tech debt documentation requirement.

The implementation is: service role key, three code comments (client init, migration file, TODO referencing FR-017), and a line in the tech debt tracker. No disagreement remains on this item.

### Convergence 5: Unified error architecture with dual-layer design

The devex-advocate (New Rec A), consumer-advocate (New-2), security-reviewer (Rec 5 revision), and I all converge on the same design: `ProviderError` retains `.category` for programmatic consumers (SDK/CLI), `map_engine_error()` maps categories to broad consumer-friendly messages for the web API, and raw error details never appear in HTTP responses. The consumer-advocate's revised error message categories (authentication issues, temporary issues, input issues) are the right granularity. The security-reviewer's constraint against key-validity oracles is the right security boundary.

This was the most productive multi-reviewer convergence in the process. Four independent reviews identified the same gap from different angles and arrived at the same architectural resolution.

---

## Final Position Statement

### Non-Negotiables

1. **G3 (BYOK race) and G5 (RLS mismatch) are merge blockers.** No amount of reframing changes this. One causes credential cross-contamination between concurrent users. The other makes the web interface non-functional when migration 002 is applied. Both must be fixed before the PR merges.

2. **G17 (FRONTEND_URL) and G4 (broken --phase) must be fixed before any user or consumer testing.** G17 breaks every share link in production. G4 crashes on advertised CLI options. These are trust-destroying first impressions that cannot be deferred to a follow-up PR if testing begins.

3. **The pure function extraction architecture must be preserved through all fixes.** The engine's core functions are pure, stateless, and composable across four consumer channels. Any fix that introduces framework dependencies, global state, or side effects into the engine layer is a regression regardless of what it fixes. This is the PR's most valuable architectural contribution and the foundation that makes specs 012-020 viable.

4. **G1 (linter/engine dependency inversion) must be resolved before spec 016 work begins.** This is not a merge blocker, but it is a structural prerequisite. The shared domain model extraction and public API surface definition must happen in a dedicated PR after merge. Every reviewer agrees the diagnosis is correct; the disagreement was only on timing, and timing is now resolved.

5. **OAuth state validation is P2, not P1.** The fix should ship in the same pass as P1 fixes (near-zero cost), but the severity label must not be inflated. P1 means "the application is broken or insecure for every user." The code-paste flow's attack surface does not meet that bar. Preserving the meaning of P1 is itself a non-negotiable process commitment.

### Flexibility

1. **Rate limiting implementation approach.** I prefer engine-layer throttling in `run_deliberation()` over HTTP-only middleware, but I accept either approach as long as it protects server resources, not just provider budgets. The implementation details are P2 and can be designed when the work is prioritized.

2. **Lifecycle hooks and per-phase routing timing.** I originally wanted these before merge. I now accept they can land in a fast-follow before spec 016 begins. The devex-advocate correctly identified that adoption-focused users do not need these today.

3. **`quick()` convenience function.** I prefer documentation-only over a new public API entry point, but if the team judges the conversion benefit worth the API surface cost, I will not block it. The implementation is trivial as a wrapper around `run_deliberation()`.

4. **Consumer launch checklist mechanism.** I oppose a formal separate gate, but I support the consumer-advocate's underlying concern being tracked as P2 items in the unified priority framework. The items themselves (input guidance, error copy, feedback richness) are legitimate and should be addressed before SC-005 testing.

5. **StorageWriter, OutputManager refactor, capabilities() method, conftest.py cleanup.** These are all correctly classified as P2 or P3. I have no strong position on sequencing within those tiers. The team should prioritize based on which specs are next in the pipeline.

### Summary of Moves

| Item | Original Position | Final Position | Reason |
|------|------------------|----------------|--------|
| G1 (dependency inversion) | P1 merge blocker | P1-structural (pre-016) | Cross-reviews correct on timing |
| G2 (OAuth state) | P1 merge blocker | P2 (ship with P1 fixes) | Security-reviewer threat model; signal preservation |
| G3 (BYOK race) | P1 merge blocker | P1-urgent merge blocker | Unchanged; universal agreement |
| G4 (broken --phase) | P2 | P1-urgent | DevEx-advocate correct on first-impression trust |
| G5 (RLS mismatch) | P1 merge blocker | P1-urgent merge blocker | Unchanged; universal agreement |
| G17 (FRONTEND_URL) | Not in original review | P1-urgent | Consumer-advocate correctly identified the gap |
| Lifecycle hooks | P1 merge blocker | P1-structural (pre-016) | DevEx-advocate correct on adoption timing |
| Per-phase routing | P1 merge blocker | P2 | DevEx-advocate correct on cognitive load |
| ModelProvider capabilities | P2 | P3 | Three cross-reviews confirmed premature |
| Rate limiting | Not in original review | P2 | Consumer-advocate identified; security-reviewer sized correctly |

Three of my original six P1 merge blockers survived as P1-urgent. Three were correctly downgraded. Two items I missed (G17, rate limiting) were added from other reviewers' contributions. The cross-review process worked: the final priority list is more defensible than any individual reviewer's original list.
