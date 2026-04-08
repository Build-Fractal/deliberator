# Neutral Synthesis — 011-adoption-harness PR Review

**Synthesizer**: Neutral (Phase 5)
**Date**: 2026-03-24
**Target**: `global-synthesis.md` (PR #1, branch `011-adoption-harness`)
**Agents**: architect, security-reviewer, devex-advocate, consumer-advocate
**Deliberation mode**: Cooperative

---

## Process Summary

**Agents**: 4 (architect, security-reviewer, devex-advocate, consumer-advocate)

**Total artifacts produced**: 24
- Phase 1 reviews: 4 (one per agent)
- Phase 2 cross-reviews: 12 (each agent reviewed the other three)
- Phase 3 revisions: 4 (one per agent)
- Phase 4 disputes: 4 (one per agent)

**Recommendations across the process**:
- Phase 1 original recommendations: 36 (architect: 10, security-reviewer: 9, devex-advocate: 10, consumer-advocate: 10)
- Recommendations withdrawn: 0
- Recommendations modified (priority or scope): 16
- Recommendations maintained unchanged: 20
- New recommendations added in Phase 3: 10 (architect: 3, security-reviewer: 3, devex-advocate: 3, consumer-advocate: 2)
- Final recommendation count: 46

**Priority changes across the process**:
- Upgrades: 4 (G4 P2->P1-urgent by architect; G2 P2->P1 by security-reviewer; G28 P3->P2 by security-reviewer; G11 not-listed->P1-urgent by architect)
- Downgrades: 6 (architect Rec #1 P1->P1-structural; architect Rec #2 P1->P2; architect Rec #3 P1->P2; architect Rec #6 P1->P2; architect Rec #8 P2->P3; consumer-advocate Rec #4 P1->P2)
- Stable: remaining items

**Disputes remaining after Phase 4**: 4 substantive (rate limiting severity, OAuth state severity label, `quick()` convenience function, consumer readiness gate mechanism)

**Convergence points reached**: 5 major (G3/G5 as merge blockers, two-axis priority framework, pure function architecture, RLS fix approach, unified error architecture)

---

## Recommendation Scorecard

The table below tracks every recommendation from initial proposal through final disposition. Recommendations are grouped by the global synthesis issue they address where applicable.

| ID | Description | Origin | Phase 1 Priority | Phase 3 Priority | Phase 4 Status | Final Priority |
|----|-------------|--------|-------------------|-------------------|----------------|----------------|
| **G3** | BYOK os.environ race -- pass key to provider constructor | architect Rec #5, security Rec #2, consumer Rec #3 | P1 (all) | P1 (all) | Universal convergence | **P1-urgent** |
| **G5** | RLS/user_id mismatch -- use service role key, document FR-017 path | architect Rec #7, security Rec #1, consumer Rec #1 | P1 (all) | P1 (all) | Universal convergence | **P1-urgent** |
| **G4** | Remove unsupported --phase CLI choices | architect Rec #9 (P2), devex Rec #1 (P1) | P2/P1 split | P1-urgent (architect revised) | Convergence | **P1-urgent** |
| **G17** | Add FRONTEND_URL to deployment config | consumer Rec #2 (P1), architect New B | P1/absent | P1-urgent (architect New B) | Convergence (label dispute only) | **P1-urgent** |
| **G2** | OAuth state validation -- add local comparison | architect Rec #6, security Rec #3, devex Rec #2 | P1/P2 split | P1 (security revised up), P2 (architect, devex revised) | Dispute on label; all agree: fix before merge | **P2 (implement with P1 fixes)** |
| **G1** | Extract shared domain models to `conversus.models` | architect Rec #1 (P1) | P1 | P1-structural | Convergence -- fix before spec 016 | **P1-structural** |
| **G8** | Add lifecycle hook call sites to run_pipeline() | architect Rec #2 (P1) | P1 | P2 (architect revised) | Convergence -- fix before spec 016 | **P1-structural** |
| **G6** | Wire per-phase model routing in EngineConfig | architect Rec #3 (P1) | P1 | P2 (architect revised) | Convergence | **P2** |
| **G11** | Rate limiting on POST /api/deliberate | security Rec #5 (P2), consumer Rec #4 (P1) | P2/P1 split | P2 (security, consumer revised), P1-urgent (architect New A) | Dispute -- 3 say P2, architect says P1-urgent | **P2 (pre-consumer-validation)** |
| **G16** | Add max_length to web question field | security Rec #4 (P2), consumer Rec #6 (P2) | P2 (all) | P2 (all) | Convergence | **P2** |
| **G28** | Restrict CORS methods/headers (env-var-driven) | security Rec #6 (P2) | P3->P2 (security upgrade) | P2 | Convergence | **P2** |
| **G24** | Add httpx timeout to all token exchange calls | security Rec #7 (P2), devex Rec #5 (P2) | P3->P2 (both upgrade) | P2 | Convergence | **P2** |
| **G23** | Preserve ProviderError.category via AgentResult type | devex Rec #6 (P2) | P3->P2 (devex upgrade) | P2 (revised implementation) | Convergence on architecture | **P2** |
| G13 | StorageWriter protocol for OutputManager | architect Rec #4 (P2) | P2 | P2 (sequencing revised) | No dispute | **P2** |
| G12 | Replace OutputManager.retroactive_move_to_round_1() | architect Rec #10 (P2) | P2 | P2 | No dispute | **P2** |
| G15 | Consistent --provider validation between CLI commands | devex Rec #7 (P2) | P2 | P2 | No dispute | **P2** |
| G30 | Add run_sync() wrapper to SDK Deliberation | devex Rec #3 (P2) | P3->P2 (devex upgrade) | P2 | No dispute | **P2** |
| G31 | Add per_agent_outputs to SDK Result | devex Rec #4 (P2) | P3->P2 (devex upgrade) | P2 (implementation dispute) | Dispute on dependency chain | **P2** |
| G14 | ModelProvider capabilities() method | architect Rec #8 (P2) | P2 | P3 (architect revised) | Convergence | **P3** |
| G29 | Add unshare endpoint | security Rec #8 (P3) | P3 | P3 | No dispute | **P3** |
| G9 | Document stealth header ToS implications | security Rec #9 (P3) | P3 | P3 | No dispute | **P3** |
| G10 | Anthropic client_id -- verify current state | devex (P2), security (FALSE POSITIVE) | Factual dispute | Unresolved | Requires verification on branch HEAD | **Verify** |
| G18-G27 | Remaining P3 items from global synthesis | Various | P3 | P3 | Not contested | **P3** |
| **New** | Decide service extraction to engine/orchestrate.py | devex Rec #8 (P2), architect cross-review | P2 | P2 (scope expanded) | Convergence | **P2** |
| **New** | Unified dual-layer error architecture | devex New A, consumer New-2 | -- | P2 (Phase 3) | Convergence | **P2** |
| **New** | CLI-to-SDK graduation guide + quick() function | devex New B | -- | P2 (Phase 3) | Dispute on quick() vs docs-only | **P2** |
| **New** | Rate limiting at engine layer (concurrency primitive) | architect New A, devex dispute 1 | -- | P1-urgent/P2 split | Dispute on layer | **P2** |
| **New** | FRONTEND_URL in deployment config | architect New B | -- | P1-urgent (Phase 3) | Convergence | **P1-urgent** |
| **New** | Two-axis priority framework (process) | architect New C | -- | Process (Phase 3) | Universal adoption | **Process** |
| **New** | Plaintext token storage documentation | security New A, devex New C | -- | P3 (Phase 3) | Convergence | **P3** |
| **New** | Security review gate for any future demo/operator-key mode | security New B | -- | P3/process (Phase 3) | Convergence | **P3/process** |
| **New** | Token refresh file locking for CLI+MCP concurrency | security New C | -- | P3 (Phase 3) | No dispute | **P3** |
| **New** | Free-text feedback field for consumer validation | consumer Rec #5 (P2) | P2 | P2 (storage revised) | No dispute | **P2** |
| **New** | Example questions on web form landing page | consumer Rec #7 (P2) | P2 | P2 | No dispute | **P2** |
| **New** | Validate 30-second latency target with real providers | consumer Rec #8 (P2) | P2 | P2 (criteria revised) | Dispute -- no other agent engaged | **P2 (pre-SC-005)** |
| **New** | Consumer-facing error message copy | consumer Rec #9 (P2) | P2 | P2 (revised for oracle constraint) | Dispute on content ownership | **P2** |
| **New** | Consumer channel readiness checklist | consumer New-1 | -- | P2/process (Phase 3) | Dispute on mechanism | **Process** |

---

## Dangerous Contradictions Found

### Resolved Contradictions

**RC-1: OAuth state validation severity (P1 vs P2)**
- **Parties**: architect (P1) vs security-reviewer (P2) vs devex-advocate (P1 then P2)
- **Nature**: Whether the code-paste flow's narrower attack surface justifies a severity downgrade.
- **Resolution**: The security-reviewer's threat model analysis prevailed -- the code-paste flow has no redirect URI, so classical CSRF is not exploitable. The architect conceded in Phase 3: "Security-reviewer's threat model analysis is technically superior to mine." The devex-advocate conceded in Phase 3: "the security-reviewer's exploitability argument is technically sound." The security-reviewer then reversed course in Phase 3 and upgraded to P1 on cost-benefit grounds. By Phase 4, the split is 2 (architect, security-reviewer) saying P1 vs 1 (devex-advocate) saying P2, with consensus that the fix ships before merge regardless of label. **Operational resolution**: Fix before merge. Label is a classification dispute with no impact on action.

**RC-2: Linter/engine dependency inversion timing (P1 merge blocker vs P1-structural)**
- **Parties**: architect (P1 merge blocker) vs security-reviewer (not a security concern), devex-advocate (P2, fix after merge), consumer-advocate (not consumer-relevant)
- **Nature**: Whether an internal layering violation should block the adoption harness merge.
- **Resolution**: The architect conceded timing in Phase 3, accepting all three cross-reviews' argument that the dependency inversion causes "zero user-visible harm in the current release." Reclassified to P1-structural: fix before spec 016 begins, not before this PR merges. The diagnosis (inverted dependency from engine to linter in 3 locations) was never disputed -- only the timing. **Fully resolved.**

**RC-3: G10 (Anthropic client_id) -- FALSE POSITIVE vs P2**
- **Parties**: security-reviewer (FALSE POSITIVE, populated in M004 via base64) vs devex-advocate (P2, empty string placeholder per M003)
- **Nature**: Factual disagreement about the current state of the code on the PR branch HEAD.
- **Resolution**: Acknowledged as requiring verification. The security-reviewer observed base64-encoded content in a later commit; the devex-advocate referenced the M003 finding which may predate that commit. Both agreed: check `OAUTH_CONFIGS["anthropic"]["client_id"]` on branch HEAD. **Partially resolved -- requires one verification step.**

**RC-4: Rate limiting severity (P1 vs P2)**
- **Parties**: consumer-advocate (P1, then revised to P2, then re-disputed at P1-urgent), architect (P1-urgent), security-reviewer (P2), devex-advocate (P2)
- **Nature**: Whether an unprotected public endpoint is a merge blocker or a should-fix.
- **Resolution**: The security-reviewer's BYOK cost-model argument persuaded the consumer-advocate to downgrade in Phase 3. The architect elevated to P1-urgent in Phase 3. By Phase 4, the split is 2 (security-reviewer, devex-advocate) at P2 vs 1 (architect) at P1-urgent vs 1 (consumer-advocate) re-escalating to P1-urgent. All agree it must be in place before consumer validation. **Resolved as P2 with a pre-consumer-validation deadline** -- the majority position, with operational consensus on timing.

**RC-5: BYOK viability as a code review finding**
- **Parties**: consumer-advocate (P3, assess demo mode) vs architect (out of scope), security-reviewer (BYOK is the strongest security control), devex-advocate (multi-sprint engineering cost)
- **Nature**: Whether questioning the spec's access model belongs in a PR review.
- **Resolution**: The consumer-advocate conceded in Phase 3: "I was wrong to suggest a demo mode as a P3 fix within this PR's scope." Reframed from code fix to product strategy flag: document the SC-005 recruitment strategy and confirm BYOK is not a blocking assumption. The security-reviewer's process gate (New Rec B: require security review of any future demo mode) was accepted by all. **Fully resolved.**

**RC-6: Plugin lifecycle hooks timing (P1 merge blocker vs P2)**
- **Parties**: architect (P1 merge blocker) vs devex-advocate (not needed for adoption), consumer-advocate (no consumer impact)
- **Nature**: Whether preparing for spec 016 should block the adoption harness.
- **Resolution**: The architect conceded in Phase 3: "The DevEx advocate's challenge is well-targeted: No developer adopting conversus today needs plugin hooks." Downgraded to P2 in this PR / P1-structural before spec 016. **Fully resolved.**

**RC-7: Error message specificity vs information leakage**
- **Parties**: consumer-advocate (specific per-failure-mode messages) vs security-reviewer (broad categories to prevent key-validity oracle)
- **Nature**: Whether consumer error copy should distinguish auth failure modes.
- **Resolution**: The consumer-advocate conceded in Phase 3, accepting broad categories: "authentication issues, temporary issues, input issues." The security-reviewer accepted the dual-layer architecture in Phase 4 but refined the message content: all authentication errors must map to a single message. The devex-advocate proposed the `.user_message` property on ProviderError. **Resolved on architecture; minor content dispute remains (see Remaining Disputes).**

### Unresolved Contradictions

**UC-1: Rate limiting implementation layer (FastAPI middleware vs engine concurrency primitive)**
- **Parties**: devex-advocate (engine-layer in `run_pipeline()`), consumer-advocate (FastAPI middleware is sufficient), architect (engine-layer preferred)
- **Nature**: Whether rate limiting should protect only the web endpoint or all channels.
- **Status**: The devex-advocate correctly identifies that SDK and MCP callers face the same resource exhaustion risk. The consumer-advocate's FastAPI-only approach leaves these channels unprotected. No resolution reached -- both layers are likely needed. See Actionable Spec Changes for recommendation.

**UC-2: `quick()` convenience function vs documentation-only graduation path**
- **Parties**: devex-advocate (ship `quick()` as module-level function), architect (documentation-only, API surface cost)
- **Nature**: Whether a synchronous convenience function belongs in the public API.
- **Status**: The architect acknowledges the graduation cliff but prefers documentation. The devex-advocate makes the `requests.get()` analogy. The architect accepts deferral to a fast-follow. No resolution -- this is a product design decision. See Remaining Disputes.

---

## Systemic Contradictions

### Pattern 1: The P1 inflation problem

The most pervasive structural issue in this deliberation was conflation of urgency, severity, and audience into a single priority label. The architect's Phase 1 review contained 6 P1 items spanning credential exposure (security), broken CLI options (UX), and dependency inversion (architecture). The consumer-advocate's Phase 1 review contained 4 P1 items spanning deployment blockers and rate limiting. These used the same label for categorically different risk types.

This systemic contradiction was identified independently by:
- Security-reviewer (Phase 2, DC-3): "Establish two priority dimensions: production safety and architectural readiness."
- Devex-advocate (Phase 2, T-1): "Urgency (user-facing, fix before release) from severity (structural, fix before next spec builds on it)."
- Consumer-advocate (Phase 2, T-1): "Should the merge gate be safe for developers to build on or safe for consumers to use?"

**Resolution**: The two-axis priority framework (P1-urgent vs P1-structural) was proposed by the architect in Phase 3 (New Rec C) and adopted by all agents by Phase 4. This is the single most important process outcome of the deliberation.

### Pattern 2: Channel-agnostic bug classification for channel-specific impact

The global synthesis classifies bugs by technical severity without distinguishing which integration channel is affected. G3 (BYOK race) only manifests in the web channel (concurrent users sharing a process). G4 (broken --phase) only manifests in the CLI channel. G17 (FRONTEND_URL) only affects the consumer channel's share links. The synthesis's single priority list obscures these channel-specific impacts.

This was surfaced by:
- Consumer-advocate (Phase 1, Off-Base #3): "The synthesis does not distinguish consumer ready from developer ready."
- Devex-advocate (Phase 2, SA-4 with consumer): "The synthesis should include separate readiness verdicts for each integration path."
- Architect (Phase 2, DC-3 with consumer): "The bugs are channel-agnostic and the fixes must be architectural" (pushback on separate assessment).

**Resolution**: Partial. The two-axis framework helps, but no per-channel readiness matrix was adopted. The consumer-advocate's request for a consumer launch checklist was resisted by the architect as "an informal gate with no spec authority" (Phase 4, Dispute 3). The synthesis recommends channel-tagged impact notes on each P1 item. See Actionable Spec Changes.

### Pattern 3: Future-spec optimization vs present-user optimization

The architect consistently prioritized issues that protect the game engine roadmap (specs 015-020): dependency inversion, lifecycle hooks, per-phase routing, StorageWriter, ModelProvider capabilities. The devex-advocate and consumer-advocate consistently prioritized issues affecting current users: broken CLI options, OAuth state, rate limiting, error messages, input guidance. These are not incompatible goals, but they produce incompatible P1 lists when forced into a single axis.

This tension was productive. It resulted in the architect downgrading 3 of 6 original P1 merge blockers and adding 2 items from other reviewers' contributions. The cross-review process worked exactly as intended: each agent's blind spots were exposed by others' perspectives.

---

## Convergence Achieved

Ordered by strength (number of agents explicitly agreeing and phase at which agreement was reached).

### 1. G3 (BYOK race) and G5 (RLS mismatch) are P1 merge blockers (4/4 agents, Phase 1)

The strongest consensus in the entire deliberation. All four agents independently identified both bugs in Phase 1, agreed on severity in Phase 2, and never wavered through Phases 3-4. The diagnosis, fix direction, and fix approach are identical across all reviews:
- G3: Pass API key to provider constructor. Providers already accept the parameter.
- G5: Use service role key. Document RLS bypass. Add TODO for FR-017.

### 2. Pure function extraction is the defining architectural strength (4/4 agents, Phase 1)

Every agent, in every phase, validated this as the PR's strongest pattern. The architect calls it "excellent architecture." The security-reviewer notes it "enables security testing." The devex-advocate calls it "the strongest finding across all milestone reviews." The consumer-advocate notes it "makes the four channels independently testable." This is the non-negotiable architectural invariant for all future work.

### 3. Two-axis priority framework (4/4 agents, Phase 3-4)

All agents converged on splitting priority into P1-urgent (production safety, user trust, fix before merge) and P1-structural (architectural readiness, fix before next spec). Proposed by the architect in Phase 3, adopted by all agents by Phase 4. Resolves the meta-dispute that dominated Phase 2 cross-reviews.

### 4. RLS fix approach: service role key with documented FR-017 migration path (4/4 agents, Phase 3)

All agents converge on: (a) service role key now, (b) code comments in `web/db.py` and migration 002, (c) TODO referencing FR-017. The devex-advocate added the "maintenance trap" concern; the consumer-advocate added the tech debt documentation requirement. Both were incorporated.

### 5. Unified dual-layer error architecture (4/4 agents, Phase 3-4)

All agents converged on: `ProviderError` retains `.category` for programmatic consumers; `map_engine_error()` maps categories to broad consumer-friendly messages; raw provider details never appear in HTTP responses. Proposed independently by devex-advocate (New Rec A) and consumer-advocate (New-2). Architect and security-reviewer endorsed.

### 6. G4 (broken --phase) and G17 (FRONTEND_URL) are P1-urgent (3/4 agents, Phase 3)

G4: architect (revised from P2), devex-advocate (original P1), consumer-advocate (agrees). Security-reviewer does not contest.
G17: architect (New Rec B), consumer-advocate (original P1). Security-reviewer agrees on timing but disputes the P1-security label. Devex-advocate does not contest.

### 7. BYOK viability is a product strategy question, not a PR finding (4/4 agents, Phase 3)

The consumer-advocate withdrew the demo-mode recommendation. All agents agree: the code correctly implements FR-016. Whether BYOK works for SC-005 is a product decision requiring a recruitment plan, not a code change.

### 8. Decide service extraction to engine/orchestrate.py (4/4 agents, Phase 3-4)

All agents converge on the target: a `run_deliberation()` function in `engine/orchestrate.py` that CLI, SDK, MCP, and web API all call. Quality gating and auth resolution are mandatory, non-skippable steps. The CLI `decide` command becomes a thin wrapper.

### 9. Token storage plaintext is an accepted risk, not a finding (3/4 agents, Phase 2-3)

Security-reviewer classified as FALSE POSITIVE. Architect agreed. Devex-advocate converted from "concern" to "documentation task." Consumer-advocate noted different threat model for consumer users but accepted for CLI channel. Resolved as: add a code comment explaining the decision; no code change.

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

### Dispute 1: Rate limiting severity -- P2 vs P1-urgent

**Agents**: security-reviewer (P2), devex-advocate (P2), consumer-advocate (P1-urgent), architect (P1-urgent)

**Summary**: The consumer-advocate and architect argue that a publicly accessible endpoint with no throttling on a 512MB/1vCPU DO instance is an availability risk that constitutes P1. The security-reviewer and devex-advocate argue that under BYOK, the attacker bears provider costs and the pre-provider pipeline work is lightweight, making this P2 -- the application works correctly without it and only fails under sustained adversarial attack.

**Evidence**:
- Consumer-advocate Phase 4 Dispute 1: "An application which can be rendered unavailable to all consumers by a single actor sending rapid requests to an unprotected endpoint is insecure."
- Security-reviewer Phase 4 Dispute 1: "Rate limiting protects against sustained adversarial attack on an unadvertised MVP endpoint. These are not the same severity class" as G3/G5.
- Architect Phase 4 Dispute 1: "BYOK shifts the LLM cost risk; it does not eliminate the resource exhaustion risk."

**Synthesizer assessment**: The security-reviewer's distinction between "application broken for every user" (G3, G5) and "application vulnerable under adversarial conditions" (rate limiting) is the more precise severity analysis. However, the architect and consumer-advocate are correct that server-side resource exhaustion is independent of BYOK. The resolution is P2 with a hard deadline: rate limiting must be in place before the web form is publicly accessible, tracked as a pre-consumer-validation requirement. This preserves the P1 severity signal for genuine deployment blockers while ensuring rate limiting is not indefinitely deferred.

**Recommended resolution**: **P2 with pre-consumer-validation deadline.** Implement as both FastAPI middleware (per-IP, for web) and an engine-layer concurrency primitive (for all channels), per the devex-advocate's architecture recommendation. The FastAPI layer ships first as a quick win; the engine layer follows.

### Dispute 2: OAuth state validation label -- P1 vs P2

**Agents**: security-reviewer (P1, revised up), architect (P2, accepts security-reviewer's threat model but rejects label), devex-advocate (P2)

**Summary**: All agents agree the fix (one conditional + one raise) ships before merge. The dispute is whether labeling it P1 dilutes the severity signal or whether labeling it P2 creates deferral risk.

**Evidence**:
- Security-reviewer Phase 3 revision: "The cost of keeping it at P1 is zero. The cost of downgrading is nonzero (deferral risk, precedent-setting, regression if flow changes)."
- Architect Phase 4 Dispute 2: "The cost of keeping it at P1 is signal dilution. P1 means the application is broken or insecure without this fix. The code-paste flow's attack surface does not meet that bar."
- Devex-advocate Phase 4 Dispute 2: "Severity should reflect the current codebase, not a hypothetical future state."

**Synthesizer assessment**: The architect and devex-advocate's argument is more rigorous. The security-reviewer's own Phase 2 threat model analysis demonstrated that the code-paste flow materially reduces exploitability. Upgrading based on deferral risk and future-state speculation conflates severity with process discipline. However, the security-reviewer's pragmatic point -- this fix takes less time to implement than to triage -- is valid.

**Recommended resolution**: **P2, fix before merge.** Tag as FR-017 prerequisite. Add a code comment at the state generation site documenting that local validation becomes critical if the flow migrates to redirect-based auth. This captures the security-reviewer's trajectory concern without inflating the severity label.

### Dispute 3: Consumer readiness gate mechanism

**Agents**: consumer-advocate (wants a consumer launch checklist), architect (opposes a parallel gate)

**Summary**: The consumer-advocate proposes a "consumer validation readiness" checklist gating SC-005 testing. The architect argues this creates "an informal gate with no spec authority" that duplicates the P2 priority list.

**Evidence**:
- Consumer-advocate Phase 4 Dispute 2: "I am not asking for these items to block the PR merge. I am asking for the synthesis to include an explicit consumer validation readiness gate."
- Architect Phase 4 Dispute 3: "The correct mechanism already exists: the P1-urgent items are merge blockers. The P2 items should be tracked in the existing priority framework."

**Synthesizer assessment**: Both agents are partially right. The architect is correct that a separate gate risks scope creep. The consumer-advocate is correct that P2 items critical for SC-005 (input guidance, error copy, example questions) could be indefinitely deferred without a tracking mechanism. The resolution is not a formal gate but a named tracking list.

**Recommended resolution**: Include a "Pre-SC-005 Validation Checklist" in the Actionable Spec Changes section below. This is a tracking artifact, not a merge gate. It references existing P2 items that must be completed before the 25-user consumer validation experiment begins. The items are: G17 fix, consumer error message copy, input guidance/character limits, latency measurement, SC-005 recruitment plan documenting BYOK assumptions.

### Dispute 4: `quick()` convenience function

**Agents**: devex-advocate (ship it), architect (documentation-only, API surface cost)

**Summary**: The devex-advocate proposes `conversus.quick(question)` as a module-level synchronous convenience function mirroring CLI defaults. The architect prefers a CLI-to-SDK migration guide (documentation) to avoid API surface obligations.

**Evidence**:
- Devex-advocate Phase 4 Dispute 3: "This is the same pattern as `requests.get()` vs `requests.Session().get()`."
- Architect Phase 4 Dispute 4: "If `quick()` calls `run_deliberation()`, it is a one-line wrapper that adds nothing over `asyncio.run(run_deliberation(...))`."

**Synthesizer assessment**: The devex-advocate's `requests.get()` analogy is apt. Module-level convenience functions are a standard Python pattern for library adoption. The architect's concern about backwards-compatibility obligations is valid but manageable -- the function's scope is narrow and stable. However, both agents accept deferral to a fast-follow PR.

**Recommended resolution**: **Ship the CLI-to-SDK migration guide in this PR. Defer `quick()` to a fast-follow PR** where its API contract can be designed alongside `run_deliberation()` from the decide service extraction. This gives the devex-advocate the adoption ramp without rushing the API design.
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1-urgent: Fix before merge

These items are universal or near-universal consensus across all four agents. They must be resolved before the PR merges to main.

**SC-1: Fix BYOK os.environ race condition (G3)**
- Traced to: architect Rec #5, security-reviewer Rec #2, consumer-advocate Rec #3
- Action: Pass API key directly to provider constructor. Remove all `os.environ` mutation from the web request path. `AnthropicProvider(auth_token=api_key)`, `OpenAIProvider(api_key=api_key)`.
- Rationale: Cross-user credential exposure under uvicorn async concurrency. Reliably exploitable under load. Providers already accept the key parameter, making this a small change.

**SC-2: Fix RLS/user_id mismatch (G5)**
- Traced to: architect Rec #7, security-reviewer Rec #1, consumer-advocate Rec #1
- Action: Use `SUPABASE_SERVICE_ROLE_KEY` for backend operations. Add code comments in (a) `web/db.py` at client initialization, (b) `supabase/migrations/002_rls_user_scoped.sql`, and (c) a TODO referencing FR-017 for switching to per-user JWTs when user accounts are implemented.
- Rationale: Migration 002 policies reject every INSERT when user_id is NULL. Application is non-functional in production.

**SC-3: Fix broken --phase CLI choices (G4)**
- Traced to: devex-advocate Rec #1, architect Rec #9 (revised to P1-urgent)
- Action: Remove `cross-review`, `revision`, `disputes`, `synthesis` from the `click.Choice` list for `run --phase`. Keep only `all` and `review` (the implemented values). Add the others back when their execution paths are implemented.
- Rationale: A CLI that crashes on its own advertised options destroys first-impression trust. One-line fix.

**SC-4: Add FRONTEND_URL to deployment configuration (G17)**
- Traced to: consumer-advocate Rec #2, architect New Rec B
- Action: Add `FRONTEND_URL` environment variable to `.do/app.yaml` and any other deployment manifests. Verify share links resolve correctly in deployed environments.
- Rationale: Without this, every share link in production points to localhost, breaking the consumer viral mechanism entirely.

**SC-5: Fix OAuth state validation (G2)**
- Traced to: architect Rec #6, security-reviewer Rec #3, devex-advocate Rec #2
- Action: After parsing `code#state_returned` from user paste in `_login_anthropic()`, add: `if state_returned != state: raise ProviderError("OAuth state mismatch", category="auth")`. Add a code comment at the state generation site noting that local validation becomes critical if the flow migrates to redirect-based auth (FR-017).
- Rationale: One-line fix closing an OAuth spec violation. Near-zero cost, near-zero risk. All agents agree on fix timing (before merge) despite disagreeing on severity label.

### P1-structural: Fix before spec 016 begins

These items are consensus for the architectural readiness gate. They should land in a dedicated PR after the adoption harness merges but before spec 016 work starts.

**SC-6: Extract shared domain models to `conversus.models` (G1)**
- Traced to: architect Rec #1 (revised timing)
- Action: Create `conversus/models/` package. Move `Phase`, `TemplateContext` subclasses, `InfluenceLevel`, `ArbiterTiming`, `PathList`, `ModeSchema`, `VariablesSchema`, `VariableDefinition` from `linter/models.py`. Leave `LintError` and `ErrorType` in `linter/models.py`. Define `conversus.models` as the documented public import surface.
- Rationale: Eliminates the engine->linter dependency inversion in 3 locations. Every future spec importing from engine/ currently transitively pulls linter/. Bundle with public API surface definition to prevent import churn.

**SC-7: Add lifecycle hook call sites to run_pipeline() (G8)**
- Traced to: architect Rec #2 (revised timing)
- Action: Define `PluginHook` protocol with `execute(state, config) -> PluginResult`. Add 4 hook call sites in `run_pipeline()`: before Phase 1, after Phase 5 per round, after Phase 6, after all rounds. Accept optional `hooks: dict[HookPoint, list[PluginHook]]` parameter (default empty dict). Behavior is identical to current code when hooks dict is empty.
- Rationale: Spec 016 requires `PRE_EXECUTION`, `POST_PHASE_5`, `POST_DELIBERATION`, `POST_ARBITRATION` hooks. Adding empty call sites now is zero-cost; retrofitting after merge requires modifying the core orchestrator.

### P2: Should fix

Ordered by cross-agent consensus strength and dependency relationships.

**SC-8: Extract decide orchestration to engine/orchestrate.py**
- Traced to: devex-advocate Rec #8, architect cross-review expansion, security-reviewer T-5 constraint, consumer-advocate T-1
- Action: Create `engine/orchestrate.py` with `run_deliberation()` function. CLI `decide`, SDK `Deliberation.run()`, MCP `conversus_decide`, and web `/api/deliberate` all call it. Quality gating and auth resolution are mandatory, non-skippable steps.
- Dependency: None. Enables StorageWriter, per_agent_outputs, and rate limiting improvements.

**SC-9: Implement dual-layer error architecture**
- Traced to: devex-advocate New Rec A, consumer-advocate New-2, security-reviewer DC-4
- Action: (a) Design `AgentResult` type with `output: str | None` and `error: ProviderError | None` for dispatch gather results. (b) Add `.user_message` property to `ProviderError` generating consumer-friendly text from category. (c) Ensure `map_engine_error()` maps all auth-category errors to a single message (no key-validity oracle). (d) Add test asserting raw ProviderError details never appear in HTTP responses.
- Dependency: None. Enables consumer error copy (SC-18).

**SC-10: Add rate limiting (G11)**
- Traced to: security-reviewer Rec #5, consumer-advocate Rec #4, architect New Rec A, devex-advocate Dispute 1
- Action: (a) FastAPI per-IP middleware on `/api/deliberate` (5 requests/minute suggested). (b) Engine-layer concurrency primitive in `run_pipeline()` or `run_deliberation()` protecting all channels.
- Dependency: SC-8 (decide extraction) for engine-layer implementation.
- Deadline: Before web form is publicly accessible.

**SC-11: Add max_length to question field and frontend guidance (G16)**
- Traced to: security-reviewer Rec #4, consumer-advocate Rec #6
- Action: Backend: `max_length=10_000` on `DeliberateRequest.question` Pydantic field. Frontend: character counter with guidance text ("Describe your decision in 1-3 sentences").
- Dependency: None.

**SC-12: Restrict CORS configuration (G28)**
- Traced to: security-reviewer Rec #6, devex-advocate DC-3
- Action: Environment-variable-driven CORS with restrictive defaults: `CORS_METHODS=GET,POST,OPTIONS`, `CORS_HEADERS=Content-Type,Authorization`. Configurable via env vars for development flexibility.
- Dependency: None.

**SC-13: Add httpx timeout to all auth calls (G24)**
- Traced to: security-reviewer Rec #7, devex-advocate Rec #5
- Action: Add `timeout=30` to all `httpx.post()` and `httpx.get()` calls in `engine/auth.py`. Surface clear `ProviderError("Token exchange timed out after 30s")` on timeout.
- Dependency: None.

**SC-14: Add run_sync() to SDK Deliberation (G30)**
- Traced to: devex-advocate Rec #3, security-reviewer T-1 constraint
- Action: Add `def run_sync(self, **kwargs) -> Result: return asyncio.run(self.run(**kwargs))` to `Deliberation` class. Include docstring warning about blocking behavior. Must use `asyncio.run()` (new event loop), not `loop.run_until_complete()`.
- Dependency: None.

**SC-15: Add per_agent_outputs to SDK Result (G31)**
- Traced to: devex-advocate Rec #4, architect Missed Opportunity #7
- Action: Add `per_agent_outputs: dict[str, str]` to `PipelineResult`, populated from in-memory dispatch results during `run_pipeline()`. Add `exclude_agent_outputs=True` parameter to `set_deliberation_public()` per security-reviewer T-2.
- Dependency: None (devex-advocate's position: independent of StorageWriter).

**SC-16: Wire per-phase model routing (G6)**
- Traced to: architect Rec #3 (revised to P2)
- Action: Fix provider/model default mismatch first (both default to "mock" or both to "anthropic"). Then add `phase_models: dict[str, str] = {}` to `EngineConfig`. In `run_pipeline()`, resolve model per phase: `config.phase_models.get(phase_name, config.model)`. Do not surface in CLI until spec 019.
- Dependency: SC-8 (provider default mismatch fix).

**SC-17: StorageWriter protocol (G13)**
- Traced to: architect Rec #4
- Action: Define `StorageWriter` protocol with `write(rel_path, content)` and `read(rel_path)`. Inject into `run_deliberation()` (not directly into OutputManager). Default: `FilesystemWriter`. Web backend: `SupabaseWriter`.
- Dependency: SC-8 (decide extraction provides injection point).

**SC-18: Consumer-facing error message copy**
- Traced to: consumer-advocate Rec #9 (revised), security-reviewer Dispute 3
- Action: Write consumer-friendly strings for `map_engine_error()` mapping: auth category -> "There was an issue with your API credentials. Please verify your key and try again." Temporary category -> "Something went wrong. Please try again in a moment." Input category -> "Your question couldn't be processed. Try rephrasing it in 1-3 sentences." All auth errors map to a single message (no key-validity oracle).
- Dependency: SC-9 (error architecture).
- Deadline: Before SC-005 consumer validation.

**SC-19: Free-text feedback field for consumer validation**
- Traced to: consumer-advocate Rec #5
- Action: Add optional free-text `feedback` column on `deliberations` table (or separate `feedback` table). Not in `usage_events` JSONB. Apply DOMPurify sanitization and max_length. Frontend: optional text field after thumbs up/down.
- Dependency: None.
- Deadline: Before SC-005 consumer validation.

**SC-20: Example questions on web form landing page**
- Traced to: consumer-advocate Rec #7
- Action: Add 4-6 clickable example questions spanning consumer domains (career, finance, family, education) that populate the question input on click.
- Dependency: None.
- Deadline: Before SC-005 consumer validation.

**SC-21: Validate latency target with real providers**
- Traced to: consumer-advocate Rec #8
- Action: Run 10 deliberations through each supported provider. Report time-to-first-SSE-event (consumer metric) and total wall-clock (resource metric). SC-001 evaluated against time-to-first-meaningful-content, not wall-clock total.
- Dependency: None.
- Deadline: Before SC-005 consumer validation.

**SC-22: CLI-to-SDK migration guide**
- Traced to: devex-advocate New Rec B
- Action: Add "CLI to SDK" section in SDK documentation mapping every CLI flag to its SDK equivalent. Include progression: `quick()` (when available) -> `Deliberation().run_sync()` -> `Deliberation().run()`.
- Dependency: None.

**SC-23: Replace OutputManager.retroactive_move_to_round_1() (G12)**
- Traced to: architect Rec #10
- Action: Construct multi-round directory structure upfront when `config.rounds > 1`. First round writes to `{output}/round-1/` from the start. Single-round preserves flat layout.
- Dependency: SC-17 (StorageWriter) for full benefit.

**SC-24: Resolve EngineConfig.provider vs runtime default mismatch**
- Traced to: devex-advocate Rec #7
- Action: Make both defaults consistent. Default to "mock" (explicit opt-in for real providers) for security-conscious informed consent about credential usage.
- Dependency: None.

### P3: Nice to have / Defer to consuming context

**SC-25: ModelProvider capabilities() method (G14)** -- Defer to spec 019.
**SC-26: Add unshare endpoint (G29)** -- Ship in first post-merge follow-up before consumer validation.
**SC-27: Document stealth header ToS implications (G9)** -- Make version configurable via env var; add code comment.
**SC-28: Plaintext token storage documentation** -- Add code comment in `engine/auth.py` explaining threat model and industry precedent.
**SC-29: Security review gate for future demo/operator-key mode** -- Process: any operator-funded key proposal must undergo dedicated security review.
**SC-30: Token refresh file locking** -- Add `fcntl.flock()` around credential read-check-refresh-write cycle.
**SC-31: conftest.py for test import cleanup (G20)** -- 15-minute cleanup when touching test infrastructure.
**SC-32: CLI/MCP behavioral asymmetry documentation** -- Add "Behavioral Differences" section to docs.
**SC-33: Remaining P3 items from global synthesis (G18-G32 not otherwise addressed)** -- Track and address as capacity allows.

### Process Recommendations

**SC-P1: Adopt two-axis priority framework**
- Traced to: architect New Rec C, all agents Phase 4 convergence
- P1-urgent: Application broken or insecure. Gate: merge.
- P1-structural: Architectural debt compounding. Gate: next spec starting.
- P2: Important. No hard gate.
- P3: Nice to have. Defer to consuming context.

**SC-P2: Pre-SC-005 Consumer Validation Checklist**
- Traced to: consumer-advocate New-1, architect Dispute 3 compromise
- Before running the 25-user consumer validation experiment, confirm:
  - [ ] G3, G5, G17 fixes deployed
  - [ ] Consumer error message copy written and reviewed (SC-18)
  - [ ] Input guidance / character limits in place (SC-11)
  - [ ] Latency measured with real providers (SC-21)
  - [ ] SC-005 recruitment plan documented, confirming BYOK assumption
  - [ ] Rate limiting on `/api/deliberate` (SC-10)
  - [ ] Unshare endpoint available (SC-26)
- This is a tracking artifact, not a merge gate.

**SC-P3: Verify G10 (Anthropic client_id) on branch HEAD**
- Traced to: security-reviewer FALSE POSITIVE claim, devex-advocate P2 claim
- Action: Check `OAUTH_CONFIGS["anthropic"]["client_id"]` on the HEAD of `011-adoption-harness`. If non-empty after base64 decode, update synthesis to mark G10 resolved. If empty, classify as P1 functional blocker for OAuth login.

---

## Key Concessions

These are the notable moments where agents changed position based on cross-review evidence. They demonstrate the deliberation process working as designed.

### Architect concessions (Phase 3)

1. **Dependency inversion timing**: Downgraded from P1 merge blocker to P1-structural, accepting all three cross-reviews' argument that the inversion causes "zero user-visible harm in the current release." Credited security-reviewer, devex-advocate, and consumer-advocate.

2. **Lifecycle hooks timing**: Downgraded from P1 merge blocker to P2, accepting devex-advocate's argument that "no developer adopting conversus today needs plugin hooks."

3. **Per-phase routing timing**: Downgraded from P1 merge blocker to P2, accepting devex-advocate's argument about cognitive load and the need to fix the existing default mismatch first.

4. **OAuth state severity**: Downgraded from P1 to P2, accepting security-reviewer's threat model: "Security-reviewer's threat model analysis is technically superior to mine."

5. **ModelProvider capabilities**: Downgraded from P2 to P3, accepting devex-advocate's argument that protocol simplicity is a feature for adoption.

6. **Missing rate limiting and FRONTEND_URL**: Added as new P1-urgent recommendations, accepting consumer-advocate's identification of gaps in the original review.

### Security-reviewer concessions (Phase 3)

1. **OAuth state validation**: Upgraded from P2 to P1, accepting devex-advocate's deferral risk argument and consumer-advocate's FR-017 trajectory argument. (Note: this upgrade was disputed in Phase 4 by the architect and devex-advocate.)

2. **RLS fix documentation**: Accepted devex-advocate's and architect's requirement for explicit code comments documenting the service role key as a temporary bypass, preventing a "maintenance trap."

3. **Token storage**: Converted from bare FALSE POSITIVE to documented accepted risk, accepting devex-advocate's argument that every future contributor will re-litigate the decision without a code comment.

### DevEx-advocate concessions (Phase 3)

1. **OAuth state severity**: Downgraded from P1 to P2, accepting security-reviewer's exploitability analysis for the code-paste flow.

2. **ProviderError.category implementation scope**: Accepted architect's argument that the fix requires designing an `AgentResult` union type, not just "propagating the object."

3. **per_agent_outputs implementation scope**: Accepted architect's expanded scope (StorageWriter-compatible) while maintaining independence from StorageWriter dependency chain.

4. **Decide extraction scope**: Adopted architect's reframing: engine-layer orchestration function for all four channels, not just a CLI service function.

### Consumer-advocate concessions (Phase 3)

1. **Rate limiting severity**: Downgraded from P1 to P2, accepting security-reviewer's BYOK cost-model argument. (Note: partially re-escalated in Phase 4.)

2. **BYOK demo mode**: Withdrew the demo-mode proposal entirely, accepting architect's scope criticism, security-reviewer's security argument (BYOK is the strongest control), and devex-advocate's engineering cost assessment. Reframed as product strategy flag.

3. **G17 framing**: Accepted security-reviewer's distinction that G17 has no security implications. Reclassified from P1-security to P1-functional.

4. **Error message specificity**: Accepted security-reviewer's key-validity oracle constraint. Revised from per-failure-mode messages to broad categories: authentication issues, temporary issues, input issues.

5. **30-second target criteria**: Accepted architect's point that time-to-first-meaningful-content (via SSE) is the relevant consumer metric, not wall-clock total.

6. **Feedback storage**: Accepted architect's concern about heterogeneous JSONB. Directed free-text feedback to a separate storage location.
