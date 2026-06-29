# The Pragmatist — Revision 1

## Perspective

Ship working software with practical tradeoffs. Template instructions are the real enforcement surface. Perfect is the enemy of good — resolve blockers with lowest regret.

---

### Recommendation Dispositions

**1. Deploy schema compatibility checks (P1) — SURVIVING**

Both reviews converge here with near-identical specificity: Buf-based breaking-change detection, CI enforcement, days-not-weeks timeline. Devil's Advocate's cross-review lists this as Safe Agreement #1, calling it "the strongest agreement between the two reviews." No challenge was raised to the tool choice, the priority, or the timeline estimate. This remains my highest-conviction recommendation.

One refinement warranted by Devil's Advocate's broader framing: the cross-review (Tension #5) correctly notes I present this as a near-certain fix while Devil's Advocate treats it as a hypothesis to validate. Fair. I'm adding an explicit validation gate: if schema incidents recur within 60 days of deployment, the team should escalate to the deeper structural evaluation rather than assuming the fix was sufficient. Confidence is fine; blind spots about confidence are not.

**2. Add cross-repo integration CI (P1) — MODIFIED**

Surviving in intent, modified in scope. Devil's Advocate's cross-review (Dangerous Contradiction #2) identifies a real conflict: my shared-protos repo and their broader "thin shared repo" (protos + shared libs + integration tests) overlap in scope but diverge in ownership model. Adopting both creates a fourth repo that "either does too much or not enough."

I'm conceding that integration tests should live alongside the proto schemas in the shared repo rather than as a standalone pipeline. This consolidates the validation surface: proto compatibility checks and gRPC smoke tests run from the same repo, owned by the same on-call rotation, triggered by the same events. The shared-protos repo becomes a shared-contracts repo — still narrow (no "shared libraries" beyond generated proto code), but inclusive of the integration test suite. Devil's Advocate's maximalist scope (shared libraries, etc.) still risks recreating mini-monorepo problems, so I hold the line on keeping the repo's scope to contracts and their verification.

**3. Defer the monorepo decision 3-6 months (P1) — MODIFIED**

The deferral survives, but Devil's Advocate's cross-review (Dangerous Contradiction #1) lands a clean hit: "deferral without active measurement means the team will arrive at the 3-month mark with the same anecdotal evidence they have now." My own Recommendation 7 (instrument developer pain) was supposed to fill that gap, but the cross-review correctly identifies that I didn't bind them together — deferral and instrumentation are presented as independent recommendations when they must be coupled.

Modified: the 3-6 month deferral is now explicitly conditional on running the developer friction survey (original Recommendation 7) within the first 30 days and establishing a lightweight coordination-cost metric (hours per week spent on cross-repo work per engineer). At the 3-month mark, the team revisits with actual data — not just "the bleeding stopped." If the survey reveals significant daily friction beyond the schema incidents, the deferral window shortens.

**4. Evaluate platform team need before monorepo (P2) — SURVIVING**

Devil's Advocate's cross-review (Safe Agreement #3) reinforces this from a different angle: "both reviews treat a partial or under-tooled monorepo as the worst possible outcome." The cross-review (Tension #2) notes disagreement on whether the no-platform-team constraint is a strong signal (my position) or a near-disqualifying gate (Devil's Advocate's position). I maintain the weighting framing over the gating framing — "near-disqualifying" is overconfident given that some teams do successfully adopt monorepos without dedicated platform engineers, usually by distributing platform ownership. But the cross-review strengthens my conviction that this recommendation must precede any monorepo commitment. Surviving unchanged.

**5. Benchmark monorepo build tooling for polyglot (P2) — MODIFIED**

Devil's Advocate's cross-review (Tension #4) identifies a real scheduling conflict: their CI-prototype recommendation and my tooling-benchmark recommendation compete for the same scarce engineer time. Both are pre-commitment spikes, but they answer different questions ("which tool works?" vs. "what does CI look like?").

Modified: merge these into a single spike. The 2-3 day benchmark per tool should include CI pipeline measurement as a core evaluation criterion — not just "does this tool build our stack" but "what are end-to-end CI times with this tool on a representative changeset." This eliminates the sequencing conflict and produces a richer dataset from the same time investment.

**6. Define rollback criteria for any migration (P2) — MODIFIED**

Devil's Advocate's cross-review (Dangerous Contradiction #4) correctly identifies that my rollback criteria are "broader but vaguer" — specifically, "developer satisfaction drops below threshold" is undefined. Their quantitative thresholds (CI >20 min after 8 weeks, >5 merge conflicts/week, >10% engineer time on build tooling) are better operationalized.

Modified: adopt Devil's Advocate's quantitative triggers as the primary rollback criteria, and add a qualitative escape valve (team retro vote) as a secondary mechanism. The unified criteria apply to whichever path is chosen, not just the monorepo — though in practice the schema-fix path is low-enough-stakes that rollback criteria are mostly relevant if the team eventually pursues monorepo.

**7. Instrument the actual developer pain (P3) — MODIFIED (merged into Recommendation 3)**

As noted in Recommendation 3's disposition, this is no longer a standalone P3 recommendation — it's a binding precondition of the deferral. Promoting it from P3 to a required component of P1 deferral is a direct response to Devil's Advocate's Dangerous Contradiction #1. The survey and metric collection happen in the first 30 days, not "before deciding" in some unspecified future.

---

### New Recommendations

**N1. Validate the schema fix explicitly before declaring the acute problem solved.**
- **Priority:** P1 (coupled with Recommendation 1)
- Devil's Advocate's cross-review (Tension #5) flags that I present the schema fix with high confidence while they treat it as a hypothesis. They're right to hedge. The fix should include a 60-day validation window: if zero schema-mismatch incidents occur, the team can confirm the root cause was CI isolation and proceed with the deferral timeline. If incidents recur or new coordination failures emerge, the team should accelerate the structural evaluation rather than extending the deferral. This converts confidence into a testable claim.

**N2. Unify the shared repo scope before implementation.**
- **Priority:** P1
- Devil's Advocate's cross-review (Dangerous Contradiction #2) and my own cross-review of their "thin shared repo" proposal surface a real risk: two reviews recommending overlapping-but-different shared repos could produce a confused implementation. Before writing any code, the team should explicitly decide the scope boundary: proto schemas + generated code + integration smoke tests (my revised position) vs. proto schemas + shared libraries + integration tests (Devil's Advocate's position). I recommend the narrower scope, but the critical point is that the team picks one and commits. An ambiguously scoped shared repo is worse than no shared repo.

---

### Position Summary

The cross-review process sharpened my position without fundamentally redirecting it. The core thesis — fix the schema problem surgically before committing to structural changes — survived intact and was reinforced as the strongest convergence point between both reviews. What changed is the rigor around that thesis. Devil's Advocate correctly identified that my deferral recommendation was disconnected from my instrumentation recommendation, creating a path where the team defers into a data vacuum. Binding the developer survey to the first 30 days of the deferral window fixes this and ensures the eventual structural decision is data-informed rather than inertia-driven.

The most productive challenge was around shared-repo scope. My original review proposed a narrow shared-protos repo; Devil's Advocate proposed a broader shared-contracts repo. The cross-review process revealed these would collide if both were adopted. I've landed on a middle position — proto schemas plus integration tests, but not general shared libraries — that concentrates the validation surface without recreating the mini-monorepo risk. The rollback criteria also improved through synthesis: Devil's Advocate's quantitative thresholds replaced my vague qualitative criteria, producing exit ramps that actually trigger.

My strongest remaining recommendation is unchanged: **deploy Buf-based schema compatibility checks this week, with a 60-day validation window.** This is a 1-3 day investment that directly addresses the two incidents that motivated this entire discussion. Every other recommendation — deferral, benchmarking, platform team evaluation, rollback criteria — is downstream of whether this fix resolves the acute pain. If it does, the team has months of runway to evaluate monorepo vs. polyrepo with clear heads and real data. If it doesn't, that failure itself is the most valuable signal for what to do next.
