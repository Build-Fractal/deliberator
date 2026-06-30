# The Pragmatist — Review of Monorepo vs Polyrepo Decision

## Perspective

Ship working software with practical tradeoffs. Template instructions are the real enforcement surface. Perfect is the enemy of good — resolve blockers with lowest regret.

---

### Executive Summary

This question asks whether a 15-engineer startup with three services in three languages should consolidate into a monorepo or invest in better cross-repo coordination tooling. The real problem isn't repository structure — it's that protobuf schema changes break production because CI validates each repo in isolation. Two incidents last quarter is the forcing function, and the team is right to act on it. The question frames this as a binary architectural choice, but the pragmatic lens sees it as a risk-mitigation problem with a concrete blast radius.

From a pragmatist standpoint, the question is well-grounded in operational reality — actual incidents, actual CI times, actual team size. But it underweights the migration cost of a monorepo for a polyglot stack (Node, Python, Go) with no platform team, and it overweights the long-term elegance of either approach relative to the immediate pain. The 12-month growth projection to 25-30 engineers is relevant but speculative; making a high-disruption architectural bet on a hiring plan is risky when the near-term problem (schema mismatches) has surgical fixes.

My primary recommendation: **fix the schema coordination problem directly before committing to either structural change.** A shared protobuf registry with CI-enforced compatibility checks solves the two incidents, takes days not months, and leaves the monorepo option open for later. If the team still wants a monorepo after the bleeding stops, they can migrate deliberately instead of under pressure.

---

### Alignment

- **Incident-driven framing.** The question leads with real production failures (two schema mismatch incidents), not theoretical architecture preferences. This is exactly the right forcing function for a decision.
- **Concrete operational details.** CI times (8-12 min), team size (15), service count (3), communication protocol (gRPC), and infrastructure (EKS) are all specified. This grounds the discussion in what's actually true rather than what's aspirational.
- **Growth trajectory acknowledged.** Noting the 12-month plan to scale to 25-30 engineers is honest about the decision's shelf life. A choice that works for 15 may not work for 30.
- **Tooling options named.** Listing Nx, Turborepo, and Bazel as monorepo candidates — and schema registry, contract testing, and release bot as polyrepo investments — shows the team has done initial research rather than asking a blank-slate question.
- **Decision criteria are measurable.** Migration cost, developer velocity, CI reliability, and ownership clarity are all observable outcomes, not vibes.

---

### Missed Opportunities

- **No cost estimate for the monorepo migration itself.** Moving three repos in three languages into a unified build system is a multi-week project minimum, likely 4-8 weeks of disrupted velocity for a 15-person team with no platform engineers. The question treats migration as a line item but doesn't size it. **Impact: the team could commit to a 2-month migration when a 2-day fix solves the acute problem.**

- **Polyglot build orchestration complexity is unaddressed.** Nx is JavaScript-native. Turborepo is JavaScript-native. Bazel handles polyglot but has a steep learning curve and significant maintenance burden. None of these are plug-and-play for a Node + Python + Go stack. The question doesn't surface how hard the "just use a monorepo tool" path actually is. **Impact: the team picks Nx because it's popular, discovers it doesn't orchestrate Python/Go builds well, and spends weeks on custom tooling.**

- **No mention of the protobuf-specific fix.** Buf (buf.build) or a proto registry with breaking-change detection would directly solve the stated problem — schema version mismatches — without any repo restructuring. This is the surgical option and it's absent from the question. **Impact: the team debates repo structure for weeks while a focused schema-compatibility CI check could ship in days.**

- **Developer experience during transition is listed but not scoped.** "Impact on developer velocity" during migration is a criterion, but there's no discussion of what that impact looks like: IDE performance with a monorepo, git clone times, branch management for 15 people in one repo, or the learning curve for whichever build tool is chosen. **Impact: migration surprises erode trust in the decision.**

- **Deployment coupling risk isn't discussed.** A monorepo creates pressure toward coupled deployments unless the team invests in path-based CI triggers and independent deployment pipelines. With no platform team, who builds and maintains that? **Impact: the monorepo ships, and now a Python change triggers a Go rebuild, or worse, a Go deploy.**

- **"No dedicated platform team" is mentioned but not weighted.** This is the single most important constraint. Every monorepo benefit (atomic cross-service changes, unified CI, shared tooling) requires platform-level investment to realize. Without a platform team, the monorepo becomes a shared liability that no squad owns. **Impact: the monorepo degrades into a "big ball of mud" repo that's worse than the polyrepo it replaced.**

---

### Off-Base Assumptions

- **The assumption that this is a binary choice.** The question frames it as monorepo OR polyrepo + better tooling. In practice, the highest-value move is a hybrid: keep separate repos but extract the shared protobuf schemas into a dedicated repo with compatibility CI, versioned releases, and a generated-code distribution mechanism. This is neither monorepo nor "stay with polyrepo and hope." It's a targeted structural fix for the actual failure mode.

- **The assumption that scaling to 25-30 engineers makes monorepo more attractive.** The opposite is more likely true at this team size. Monorepos shine at scale (100+ engineers) where the investment in build tooling, CODEOWNERS enforcement, and CI infrastructure pays for itself. At 25-30 engineers with no platform team, a monorepo is overhead without the economies of scale to justify it. The growth plan actually favors keeping repos separate and investing in integration contracts.

- **The assumption that CI/CD reliability improves with a monorepo.** It can — but only with significant CI engineering. Naive monorepo CI (run everything on every change) will turn 8-12 minute builds into 20-30 minute builds. Selective/affected-target CI requires Bazel-level tooling or custom scripting. The question treats CI improvement as a monorepo benefit without accounting for the CI engineering cost to realize it.

---

### Actionable Recommendations

1. **Deploy schema compatibility checks.**
   - **Priority:** P1
   - **Current state:** Protobuf schema changes are validated per-repo; version mismatches cause production incidents.
   - **Proposed change:** Introduce Buf or a custom proto lint/breaking-change CI step that runs against all 4 shared proto files on every PR in any repo. Use a dedicated `shared-protos` repo as the source of truth, with generated code published as versioned packages (npm, PyPI, Go module).
   - **Rationale:** This directly fixes the two incidents that motivated the decision. It's deployable in 1-3 days, not weeks.
   - **Risk if ignored:** The team spends 6-8 weeks on a monorepo migration while the same class of incident keeps happening.

2. **Add cross-repo integration CI.**
   - **Priority:** P1
   - **Current state:** Each repo's CI validates in isolation.
   - **Proposed change:** Create a lightweight integration test pipeline (triggered by merges to any service repo) that spins up all three services and runs a gRPC smoke test against the shared protos. Keep it under 5 minutes.
   - **Rationale:** This catches the exact failure mode (works alone, breaks together) regardless of repo structure.
   - **Risk if ignored:** A monorepo only helps if atomic commits are enforced; without integration tests, the same class of bug can still ship.

3. **Defer the monorepo decision 3-6 months.**
   - **Priority:** P1
   - **Current state:** The team is evaluating monorepo under incident pressure.
   - **Proposed change:** Fix the schema problem (recommendations 1-2), then revisit the repo structure question when the acute pain is resolved and the team can evaluate clearly.
   - **Rationale:** Decisions made under incident pressure optimize for the last failure, not the next one. The monorepo question deserves evaluation when the team isn't bleeding.
   - **Risk if ignored:** The team commits to a high-disruption migration that solves the wrong problem.

4. **Evaluate platform team need before monorepo.**
   - **Priority:** P2
   - **Current state:** No platform/infra team; each squad owns its own CI and deploy.
   - **Proposed change:** If the team still wants a monorepo after stabilizing, first allocate 1-2 engineers to a platform role responsible for build tooling, CI infrastructure, and CODEOWNERS enforcement.
   - **Rationale:** A monorepo without a platform team is a shared commons with no steward. It will degrade.
   - **Risk if ignored:** Three squads each "own" parts of the monorepo build config, leading to conflicting CI changes and broken trunk.

5. **Benchmark monorepo build tooling for polyglot.**
   - **Priority:** P2
   - **Current state:** Nx, Turborepo, and Bazel are listed as candidates without polyglot evaluation.
   - **Proposed change:** Before any migration commitment, spike each tool for 2-3 days with the actual stack (Node + Python + Go + protobuf). Measure: setup time, build correctness, selective CI accuracy, and developer onboarding friction.
   - **Rationale:** Nx and Turborepo are JavaScript-ecosystem tools. Their Python and Go support ranges from limited to nonexistent. Bazel works but has a 2-4 week learning curve. The team needs data, not assumptions.
   - **Risk if ignored:** The team picks a tool based on blog posts, discovers it doesn't work for their stack, and either migrates again or builds custom glue.

6. **Define rollback criteria for any migration.**
   - **Priority:** P2
   - **Current state:** No discussion of what happens if the chosen approach fails.
   - **Proposed change:** Before committing to either path, define explicit "this isn't working" signals (e.g., CI times exceed 20 min, migration takes longer than 6 weeks, developer satisfaction drops below threshold) and a rollback plan.
   - **Rationale:** Irreversible decisions deserve exit criteria. A monorepo migration without a rollback plan is a one-way door disguised as a two-way door.
   - **Risk if ignored:** Sunk cost fallacy keeps the team on a failing path.

7. **Instrument the actual developer pain.**
   - **Priority:** P3
   - **Current state:** The question references incidents and CI times but not developer workflow friction.
   - **Proposed change:** Before deciding, survey the 15 engineers: how often do cross-repo changes cause friction? How much time per week is spent on coordination? What's the actual pain beyond the two incidents?
   - **Rationale:** If the two incidents are the only pain, a schema fix is sufficient. If developers are losing hours daily to cross-repo coordination, the case for a monorepo is stronger. The decision should be data-driven, not incident-driven.
   - **Risk if ignored:** The team over-indexes on two dramatic incidents when the day-to-day experience might be fine — or discovers post-migration that the real friction was elsewhere.
