# Developer Experience Advocate — Final Disputes and Convergence

**Agent**: devex-advocate
**Phase**: 4 (Final Disputes)
**Date**: 2026-03-24
**Inputs**: Revised positions from architect, security-reviewer, consumer-advocate, devex-advocate; global synthesis; M002-M004 reviews

---

## Remaining Disputes

### Dispute 1: Rate limiting severity — P2 is correct, but the implementation scope must cover all channels, not just the web endpoint

**With**: Architect (New Rec A, P1-urgent), Security-reviewer (Rec #5, maintained P2)

The architect upgraded rate limiting to P1-urgent in revision. The security-reviewer maintained P2. The consumer-advocate downgraded from P1 to P2, accepting the BYOK cost-model argument. I side with the security-reviewer and the revised consumer-advocate: P2 is the correct severity.

However, I dispute the architect's and consumer-advocate's shared assumption that rate limiting is primarily a web-endpoint concern solved by FastAPI middleware. The SDK and MCP channels are equally exposed. A developer embedding `Deliberation().run()` in a loop, or an MCP client issuing rapid `conversus_decide` calls, will exhaust the same provider resources and create the same server-side resource pressure the security-reviewer identified (async worker exhaustion from pre-provider pipeline work). Solving this at the FastAPI layer alone creates a false sense of protection that does not extend to the two developer channels.

**My position**: Rate limiting belongs at the engine layer as a concurrency primitive (e.g., a semaphore or token bucket in `run_pipeline()` that all callers -- CLI, SDK, MCP, and web -- pass through), not as web middleware. The FastAPI middleware is a useful additional layer for IP-based abuse prevention, but it is not the primary fix. If the team only implements the web middleware, SDK deployers are unprotected and will discover this the hard way in production.

**Resolution path**: Implement engine-layer concurrency control in `run_pipeline()` as P2, with the FastAPI per-IP middleware as a complementary P2 item. Both should ship before public consumer testing but need not block merge.

### Dispute 2: OAuth state validation does not belong at P1 — the security-reviewer's upgrade is an overcorrection

**With**: Security-reviewer (Rec #3, upgraded to P1)

In my revision, I downgraded OAuth state validation from P1 to P2, accepting the security-reviewer's original exploitability analysis that the code-paste flow materially narrows the CSRF attack surface. The security-reviewer has now reversed their own position and upgraded it to P1, citing three arguments: deferral risk, FR-017 trajectory, and triage signal.

I find all three arguments unpersuasive as justifications for a severity change:

1. **Deferral risk** ("deferred 1-line fixes stay deferred") is a process concern, not a severity assessment. The solution to deferral risk is task tracking and PR hygiene, not severity inflation. If we promote every cheap fix to P1 because we are worried about forgetting it, P1 becomes meaningless.

2. **FR-017 trajectory** ("redirect-based OAuth makes this a real CSRF vulnerability") is correct but speculative. Severity should reflect the current codebase, not a hypothetical future state. When FR-017 changes the auth flow, the security review of that change will catch the missing validation -- that is what security reviews are for.

3. **Triage signal** ("the cost of keeping it at P1 is zero") is backwards. The cost of keeping it at P1 is dilution of the P1 bucket. The architect's own New Rec C established a two-axis priority framework precisely to prevent this: P1-urgent is reserved for items where the application is broken or insecure without the fix. The code-paste flow is neither broken nor exploitably insecure per the security-reviewer's own threat model analysis from the cross-review phase.

**My position**: P2 with a note that it should be implemented in the same pass as P1 fixes due to near-zero cost. The implementation is identical regardless of the label. The label matters because it calibrates the team's severity vocabulary for future reviews.

**Resolution path**: Accept the security-reviewer's implementation recommendation (one conditional + one raise, implement before merge). Reject the P1 label. Record in the synthesis that the four reviewers disagree on severity (2 say P1, 1 says P2, 1 says P2-but-implement-with-P1s) but agree on timing (fix before merge).

### Dispute 3: The `quick()` convenience function is not "polluting the SDK's clean API" — it is the adoption ramp

**With**: Architect (who labeled option (a) from my New Rec B as "polluting the SDK's clean API")

The architect validated the CLI-to-SDK graduation cliff as "a genuine insight my review misses entirely" but then proposed only a migration guide (documentation) as the solution, characterizing the `quick()` function as API pollution. In my revision (New Rec B), I proposed `conversus.quick(question, provider=None, model=None)` as a synchronous convenience function that mirrors CLI defaults.

The architect's concern about API cleanliness is understandable but misapplied. The `quick()` function does not live on the `Deliberation` class. It is a module-level convenience function in `conversus/__init__.py` that internally constructs a `Deliberation`, applies CLI-equivalent defaults, and calls `run_sync()`. This is the same pattern as `requests.get()` (convenience) vs `requests.Session().get()` (full control), or `json.loads()` (convenience) vs `json.JSONDecoder().decode()` (full control). No one argues that `requests.get()` pollutes the Session API.

The documentation-only approach (migration guide mapping CLI flags to SDK equivalents) fails the "5-minute test." A developer who used the CLI successfully and wants the same thing in Python must: (1) read the migration guide, (2) understand async/await, (3) understand `asyncio.run()`, (4) construct a `Deliberation` object with the right parameters, (5) handle the Result type. The `quick()` function reduces this to `result = conversus.quick("Should we expand into the EU market?")` -- one line, synchronous, returns the same Result object.

**My position**: Ship `quick()` as a module-level convenience function alongside `run_sync()` on the Deliberation class. Document both in a "Getting Started" section that shows the progression: `quick()` for scripts and notebooks, `Deliberation().run_sync()` for configuration, `Deliberation().run()` for async contexts. This is not API pollution; it is API layering.

**Resolution path**: If the architect maintains the objection, I accept deferring `quick()` to a fast-follow PR after the adoption harness merges, but the migration guide alone is insufficient and should not be presented as the complete solution to the graduation cliff.

### Dispute 4: Per-agent outputs should be populated immediately from in-memory data, not deferred to StorageWriter

**With**: Architect (Rec #4, who wants per_agent_outputs populated by StorageWriter abstraction)

The architect's revision accepts per_agent_outputs at P2 but ties its population to the StorageWriter abstraction: "per_agent_outputs should be populated by the StorageWriter abstraction (when implemented), not by file reads." The revised sequencing places StorageWriter after the decide service extraction, which is itself after the RLS fix. This creates a three-dependency chain (RLS fix -> decide extraction -> StorageWriter -> per_agent_outputs) that effectively defers per_agent_outputs to a late P2 at best.

The data needed for per_agent_outputs is already available in memory during pipeline execution. Each agent's output is held in the `dispatch_phase()` return values before being written to files by `OutputManager`. Adding `per_agent_outputs: dict[str, str]` to `PipelineResult` and populating it from the in-memory dispatch results requires no file reads, no StorageWriter, and no service extraction. It is a pure data-plumbing change within `run_pipeline()`.

Tying per_agent_outputs to StorageWriter creates an artificial dependency. The StorageWriter abstraction is valuable for its own reasons (non-filesystem backends), but the SDK should not wait for it to expose data that is already computed and in memory.

**My position**: Add `per_agent_outputs` to `PipelineResult` now, populated from in-memory dispatch results. When StorageWriter lands, it uses the same in-memory data -- no migration needed. The two concerns are orthogonal and should be sequenced independently.

**Resolution path**: Implement per_agent_outputs as a standalone P2 item with no dependency on StorageWriter. If the architect objects to populating it in `run_pipeline()` directly, the compromise is to populate it in the `_decide()` service function (which all reviewers agree should be extracted), since that function already has access to the PipelineResult.

---

## Convergence

### Convergence 1: The BYOK race (G3) and RLS mismatch (G5) are unambiguous P1 launch blockers

All four reviewers agree without reservation. The architect frames G3 as a "consumer trust and billing defect." The security-reviewer frames it as "credential exposure." The consumer-advocate frames it as "one paying consumer subsidizes another consumer's deliberation." I frame it as the single most damaging bug a developer could encounter: their API key used for someone else's request. The fix -- provider constructor injection -- is simple, validated by the security-reviewer's observation that providers already accept the key parameter, and must land before merge. G5 is equally clear: if migration 002 is applied, the web interface does not work. Period. Service role key with documented FR-017 migration path is the correct interim fix.

### Convergence 2: The two-axis priority framework resolves the P1 disagreements

The architect's New Rec C (two-dimensional priority: P1-urgent vs P1-structural) was validated by all reviewers. My revision adopted it explicitly. The security-reviewer's revision implicitly uses it (distinguishing "fix before merge" from "fix before next spec"). The consumer-advocate's revision distinguishes "P1-functional" from "P1-security." These are all the same insight expressed in different vocabularies. The convergent framework:

- **P1-urgent**: Application is broken or insecure for users today. Items: G3, G5, G4, G17.
- **P1-structural**: Architecture will compound debt if not addressed before the next spec builds on it. Items: G1 (dependency inversion + public API surface).
- **P2**: Should fix for adoption quality. All other items.

This framework resolves the disputes over G2 (OAuth state), G11 (rate limiting), lifecycle hooks, and per-phase routing by placing them on the correct axis rather than forcing a single P1/P2 decision.

### Convergence 3: The unified error architecture is the right resolution for the ProviderError tension

All four reviewers independently identified that consumer-friendly error messages and developer-friendly structured error categories must coexist. My New Rec A, the consumer-advocate's New-2, and the architect's and security-reviewer's cross-review comments all converge on the same design: `ProviderError` retains `.category` for programmatic consumers; the web API's `map_engine_error()` maps categories to broad consumer-friendly messages; a test asserts raw provider details never appear in HTTP responses. The security-reviewer adds the constraint that error messages must not create a key-validity oracle. The consumer-advocate accepts broad categories over specific failure modes. This is full convergence on architecture, implementation boundary, and security constraint. No further dispute.

### Convergence 4: The decide service extraction subsumes multiple recommendations

The architect's reframing of my Rec #8 -- "engine-layer orchestration function callable from CLI, SDK, MCP, and web API" -- is the correct scope. My original "decide service function" was too narrow. The consumer-advocate added the web form's `/api/deliberate` as a fourth caller. The security-reviewer requires quality gating and auth resolution as mandatory, non-skippable steps. All four reviewers now agree on the target: `engine/orchestrate.py` containing a `run_deliberation()` function with mandatory quality gating that all four channels call. The CLI `decide` command becomes a thin wrapper. This is the single most impactful structural improvement for developer experience because it guarantees behavioral consistency across channels and enables `--dry-run`, `--budget`, and composability.

### Convergence 5: Pure function extraction is the project's defining architectural strength

Every reviewer, in every phase, has validated this pattern. The architect calls it "excellent architecture." The security-reviewer notes it enables testability. The consumer-advocate observes it makes the four channels independently testable. I note it is the reason the 1,318+ test suite provides genuine confidence for refactoring. This is not a point of dispute -- it is the shared foundation that makes all other recommendations tractable. Any fix that violates pure function extraction (e.g., adding side effects to service functions, coupling channels to specific transport) should be rejected regardless of its other merits.

---

## Final Position Statement

### Non-Negotiables

1. **G3 and G5 must be fixed before merge.** No exceptions, no deferral, no partial fixes. These are functional and trust-destroying defects that affect every user of every channel.

2. **G4 (broken --phase choices) must be fixed before merge.** A CLI that crashes on its own advertised options is a first-impression killer. The fix is one line. There is no defensible argument for shipping this.

3. **G17 (FRONTEND_URL) must be fixed before consumer testing.** Share links that point to localhost make the consumer channel non-functional. One-line deployment config fix.

4. **The decide service extraction must happen before P2 work begins.** Every P2 recommendation (StorageWriter, per_agent_outputs, error architecture, rate limiting) is easier, cleaner, and more testable when there is a single orchestration function that all channels call. Doing the P2 work without the extraction means doing it four times across four callers.

5. **`run_sync()` must ship with the SDK.** An async-only SDK excludes the majority of Python use cases (scripts, notebooks, Django/Flask handlers, CI/CD pipelines). This is a 3-line method that determines whether the SDK is usable or merely inspectable.

### Flexibility

1. **OAuth state validation timing**: I accept fixing it before merge (all reviewers agree on timing). I dispute P1 labeling but will not block on it. If the synthesis records it as P1, I will note the disagreement and move on.

2. **`quick()` convenience function**: I strongly advocate for this but accept deferral to a fast-follow PR if the architect maintains the API-pollution objection. The migration guide should ship regardless.

3. **Rate limiting scope**: I advocate for engine-layer concurrency control but accept FastAPI middleware as the initial implementation if the team needs to ship faster. The engine-layer solution can follow.

4. **Per-agent outputs sequencing**: I advocate for immediate population from in-memory data but accept population in the `_decide()` service function if the architect prefers that injection point, provided it does not wait for StorageWriter.

5. **Priority labels for G2 and G11**: I will defer to the consensus label (P1 or P2) as long as the implementation timing is "before merge" for G2 and "before consumer testing" for G11. The label is less important than the action.

6. **Dependency inversion (G1) timing**: I accept P1-structural (before spec 016) rather than P1-urgent (before merge). The extraction must define the public API surface simultaneously, as I recommended in revision. Deferring the extraction without the public API definition is unacceptable because it just recreates the churn later.

7. **ModelProvider capabilities()**: I accept P3 deferral to spec 019. The architect is right that the protocol's simplicity is a feature for adoption. Adding capabilities() now would increase the surface area a developer must understand to write a custom provider, which directly contradicts the adoption goal of spec 011.
