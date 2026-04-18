# The Pragmatist — Final Disputes and Convergence

## Perspective

Ship working software with practical tradeoffs. Perfect is the enemy of good — resolve blockers with lowest regret.

---

### Remaining Disputes

**Dispute 1: Deferral Timeline — 3-6 Months vs. Open-Ended Validation Window**

- **My claim:** The monorepo decision should be deferred 3-6 months, with the first 30 days spent instrumenting developer friction, and the schema fix validated within 60 days. This gives the team a concrete calendar boundary that forces a revisit rather than letting the question drift indefinitely.
- **Opposing position:** Devil's Advocate proposes a 6-8 week "validation window" with explicit instrumentation, after which the monorepo question is either deprioritized with evidence or reopened with data. No fixed outer bound — the timeline follows the data.
- **Why I won't concede:** A validation window without a hard deferral deadline creates the illusion of rigor while enabling indefinite avoidance. Teams under delivery pressure will instrument the first two weeks, then stop checking the dashboards. The 3-6 month boundary is a forcing function: the team *must* revisit, even if the data is ambiguous. "Deprioritized with evidence" sounds clean but in practice means "we never talked about it again." A calendar date on the team's roadmap is harder to ignore than a conditional trigger.
- **Counter-argument:** Devil's Advocate would argue that a fixed deadline is arbitrary — if the data clearly shows no coordination pain at week 8, waiting until month 6 wastes decision-making bandwidth. Conversely, if pain emerges at week 4, the fixed timeline delays response.
- **Proposed resolution:** Adopt the 6-8 week validation window as the *first* decision gate within a hard 3-month outer bound. If the validation window produces clear signal (zero schema incidents, coordination overhead below threshold), the team can formally close the monorepo question early. If the signal is ambiguous or the validation window stalls, the 3-month deadline forces the conversation regardless. The outer bound is a safety net against organizational inertia, not a replacement for data-driven checkpoints.

**Dispute 2: Migration Estimation Gap — 4-8 Weeks vs. 3-4 Months**

- **My claim:** A monorepo migration for this team, if pursued, is realistically a 4-8 week effort given the small surface area (3 services, 4 proto files, 15 engineers). The scope is bounded by the team's size and service count.
- **Opposing position:** Devil's Advocate estimates 3-4 months and insists the estimate must be decomposed into workstreams (build tooling, CI, code ownership, proto migration, developer workflow changes) to avoid underestimation. They argue aggregated estimates hide complexity.
- **Why I won't concede:** The 3-4 month estimate is calibrated for a team that has dedicated platform engineers and is migrating a larger surface area. This team has 3 services and 15 engineers. The decomposition exercise is valuable, but using it to inflate the estimate risks making the monorepo option look categorically infeasible when it's merely expensive. I'd rather the team encounter the real complexity during a time-boxed spike than be scared off by a worst-case projection that assumes every workstream hits its ceiling.
- **Counter-argument:** Devil's Advocate would point out that 4-8 weeks is itself an aggregated estimate — it doesn't account for the polyglot tooling challenges (Node + Python + Go under one build system), the fact that no platform team exists to absorb migration work, and the productivity tax on feature work during the transition.
- **Proposed resolution:** Accept the decomposition framework as the right tool, but populate it with team-specific estimates rather than generic ones. Run the merged benchmark spike (my modified Recommendation 5) to get actual numbers for the build-tooling workstream — the single largest source of estimation variance. The decomposition becomes an estimation tool, not a predetermined conclusion. If the spike reveals polyglot build times are tractable, the overall estimate compresses toward 4-8 weeks. If the spike reveals significant tooling gaps, the estimate extends toward 3-4 months. Let the data break the tie.

**Dispute 3: The Scaling Argument's Weight**

- **My claim:** The scaling argument (growing from 15 to 25-30 engineers) is speculative and should not drive the repo-structure decision today. The team should solve the problems they have now and revisit structure when scaling pain actually materializes. Premature optimization of organizational architecture is as wasteful as premature optimization of code.
- **Opposing position:** Devil's Advocate argues the scaling argument must be "stress-tested in both directions" because it is the monorepo's strongest remaining justification once the schema problem is solved independently. They treat the scaling claim as "actively misleading" without supporting evidence.
- **Why I won't concede:** "Stress-testing the scaling argument" sounds rigorous but produces no actionable output for a 15-person team today. You cannot empirically validate how 25-30 engineers will experience a repo structure that doesn't exist yet. The exercise becomes a theoretical debate that consumes decision-making energy without changing the near-term recommendation — which both reviews agree is "fix schemas first." I'd rather the team spend that energy shipping the schema fix and measuring its impact than debating hypothetical futures.
- **Counter-argument:** Devil's Advocate would argue that ignoring the scaling trajectory is how teams end up doing emergency migrations under pressure 12 months later. The question explicitly asks the team to account for growth to 25-30 engineers, so dismissing that factor entirely is non-responsive to the decision criteria.
- **Proposed resolution:** Include the scaling trajectory as a documented consideration in the 3-month revisit, not as a driver of the immediate decision. When the team revisits repo structure with real coordination data in hand, they should explicitly project whether observed friction trends would compound at 25-30 engineers. This is a future-dated analysis with real data, not a present-day debate with hypothetical data. The scaling argument gets its day in court — but only when the court has evidence to weigh.

---

### Convergence

**Convergence 1: Deploy Schema Compatibility Checks Immediately**

- **Shared position:** Both reviews independently converge on Buf-based schema breaking-change detection in CI as the highest-priority, lowest-risk action. This is a 1-3 day investment that directly addresses the two production incidents motivating the entire discussion.
- **Agreeing agents:** Pragmatist, Devil's Advocate
- **Strength:** Strong — identified as the strongest agreement across all cross-reviews. Neither review challenged the tool choice, priority, timeline, or substance of this recommendation.
- **Path to convergence:** Already converged. Both reviews list this as P1 Recommendation #1. The only refinement is the shared agreement that the fix should be treated as a hypothesis to validate (via a time-bound window) rather than assumed sufficient.

**Convergence 2: A Monorepo Without Proper Tooling Is the Worst Outcome**

- **Shared position:** Both reviews independently conclude that a partial or under-tooled monorepo migration is worse than either a well-maintained polyrepo or a fully committed monorepo. The polyglot stack (Node + Python + Go) under a single build system without platform team ownership is the highest-risk scenario.
- **Agreeing agents:** Pragmatist, Devil's Advocate
- **Strength:** Strong — both cross-reviews identify this as a safe agreement. Devil's Advocate frames it as a near-disqualifying gate; I frame it as a high-weight factor. The directional agreement is complete even if the severity framing differs.
- **Path to convergence:** Already converged on the principle. The remaining gap is whether "no platform team" is a disqualifier or a high-weight negative. Both agree the team must evaluate platform capacity before any monorepo commitment — the disagreement is intensity, not direction.

**Convergence 3: Shared Repo Scope Must Be Narrow at Launch**

- **Shared position:** The shared contracts repo should contain proto schema files and Buf validation configuration at launch — nothing else. Shared libraries stay in current locations. Integration tests stay in CI pipelines. Scope expansion requires explicit team agreement.
- **Agreeing agents:** Pragmatist, Devil's Advocate
- **Strength:** Strong — this convergence emerged directly from the cross-review process. Devil's Advocate conceded their original broader scope (proto + shared libs + integration tests) and adopted the narrow formulation. I conceded that integration tests should not live in the shared repo but in cross-repo CI pipelines.
- **Path to convergence:** Fully converged. Both revised positions now specify the same scope boundary. The Pragmatist's "shared-contracts repo" and Devil's Advocate's revised "shared repo" are the same thing.

**Convergence 4: Rollback Criteria Must Be Quantitative and Unified**

- **Shared position:** Whichever path the team pursues, rollback criteria should include quantitative triggers (CI time thresholds, merge conflict frequency, tooling maintenance time) paired with a structured qualitative survey at defined intervals. The criteria apply to any migration, not just the monorepo.
- **Agreeing agents:** Pragmatist, Devil's Advocate
- **Strength:** Moderate — the revised positions align on the framework (quantitative primary, qualitative secondary), but specific threshold values haven't been jointly calibrated. Devil's Advocate proposed concrete numbers (CI >20 min, >5 merge conflicts/week, >10% engineer time on build tooling) which I adopted; the survey cadence (4 and 8 weeks) is Devil's Advocate's proposal.
- **Path to convergence:** Largely converged. The remaining work is team-specific calibration of threshold values, which neither agent can do without baseline measurements from the team.

**Convergence 5: Deferral Without Instrumentation Is Procrastination**

- **Shared position:** Both reviews agree that deferring the monorepo decision is correct, but deferral without structured measurement of developer friction produces no new information. The team must instrument coordination costs during the deferral period to ensure the eventual decision is data-informed.
- **Agreeing agents:** Pragmatist, Devil's Advocate
- **Strength:** Strong — Devil's Advocate's cross-review landed the sharpest challenge of the process on this point ("deferral without active measurement means the team will arrive at the 3-month mark with the same anecdotal evidence"), and my revised position directly incorporated it by binding the developer friction survey to the first 30 days of the deferral.
- **Path to convergence:** Converged on principle. The remaining dispute (Dispute 1 above) is about the shape of the deferral — fixed timeline with checkpoints vs. data-triggered gates — not about whether instrumentation is required.

---

### Final Position Statement

**Non-Negotiables:**

1. **Fix the schema problem this week.** Deploy Buf-based breaking-change detection in CI within 1-3 days. This is the only recommendation with near-zero downside risk and direct impact on the two production incidents that started this conversation. Every other recommendation is downstream of whether this works. Validate over 60 days before declaring the acute problem resolved.

2. **Do not attempt a monorepo migration without first establishing platform ownership.** Whether that's a dedicated platform team, a distributed platform rotation, or an explicit agreement on who maintains the build system — someone must own the monorepo tooling before the migration begins. An unowned monorepo is the worst possible outcome, and both reviews independently concluded this. This is a precondition, not a recommendation to be prioritized against feature work.

3. **Measure before you decide.** The deferral period must produce quantitative data on coordination costs — not opinions, not anecdotes, not "it feels better." Developer friction surveys within 30 days, cross-repo coordination time tracked per cross-cutting change, schema incident count over the validation window. The 3-month revisit happens with a dashboard, not a debate.

**Flexibility:**

1. **Deferral timeline shape.** I prefer a hard 3-month outer bound with a 6-8 week early checkpoint, but I can accept a purely data-triggered approach if the team commits to the instrumentation and defines specific thresholds that force the conversation. The mechanism matters less than the guarantee that the question gets revisited with data.

2. **Migration estimation approach.** I believe 4-8 weeks is realistic for this team's scale, but I'll accept the decomposition framework as the estimation tool and let the benchmark spike produce actual numbers. If the spike shows polyglot build tooling is harder than I expect, I'll update toward Devil's Advocate's longer timeline without resistance.

3. **Shared repo scope expansion.** Starting narrow is non-negotiable, but I'm open to expanding the shared contracts repo to include integration smoke tests if the team finds that cross-repo CI pipelines create their own coordination overhead. The expansion should be a deliberate decision at the 3-month mark, informed by the same instrumentation data that drives the monorepo revisit.
