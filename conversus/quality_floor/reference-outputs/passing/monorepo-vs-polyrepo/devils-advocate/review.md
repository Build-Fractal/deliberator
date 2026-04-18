# Devil's Advocate Review: Monorepo vs Polyrepo Decision

## Perspective

Devil's Advocate — challenging unchallenged assumptions so the surviving decision is stronger, not weaker.

---

### Executive Summary

This question asks whether a 15-engineer startup running three services in three languages should consolidate into a monorepo or double down on polyrepo with better tooling. The framing presents this as a binary architectural choice, but the strongest consensus trap here is the unstated assumption that the repository structure is the root cause of the team's integration failures. Two production incidents from schema mismatches are cited as motivation — but those incidents are symptoms of a missing contract verification step, not of repository topology. A monorepo would make atomic cross-service commits *possible*, but it would not make them *automatic*, and it would introduce an entirely new category of problems the team has zero operational experience with.

The question also converges too quickly on the tooling dimension (Nx/Turborepo/Bazel vs. schema registries and release bots) without interrogating whether the team's actual bottleneck is coordination overhead or simply the absence of a single CI gate that validates protobuf compatibility across services. If you can solve the schema mismatch problem with a 20-line CI job that pulls all four `.proto` files and runs `buf breaking` against each consumer, you have eliminated the stated pain point without touching repository structure at all. The monorepo discussion then needs to stand on its own merits — and those merits are weaker than they first appear for a polyglot team with no platform engineering capacity.

My most important recommendation: **Before choosing a repository strategy, isolate the schema compatibility problem and solve it independently.** If the team solves cross-service schema validation in the polyrepo setup and *still* finds coordination painful, the monorepo case becomes genuine. If the pain disappears, the monorepo migration is a costly solution to a problem that no longer exists, and the team should spend that engineering budget on scaling challenges they will actually face at 25-30 engineers.

---

### Alignment

- **The question correctly identifies schema version mismatches as the proximate trigger.** Naming the specific failure mode (two production incidents from proto mismatches passing isolated CI) gives evaluators something concrete to solve rather than debating abstractions.

- **Growth trajectory is included as a decision criterion.** Most monorepo-vs-polyrepo framings treat the decision as static. Acknowledging the 15→30 engineer scaling window forces respondents to reason about the future state, not just the current pain.

- **The polyglot nature of the stack is stated explicitly.** Node.js, Python, and Go in the same monorepo is a materially different problem than three Node.js services, and the question doesn't hide this complexity.

- **CI timing is quantified.** Providing the 8-12 minute baseline gives respondents a concrete number to reason about rather than hand-waving about "fast builds."

- **The absence of a platform team is disclosed.** This is the single most important constraint in the entire question and the question does not bury it.

---

### Missed Opportunities

- **The question never asks whether the problem is the repository or the CI pipeline.** The two production incidents were caused by schema changes that "passed CI in isolation but broke at integration." This is a CI design gap, not a repository topology problem. A cross-repo integration test triggered on any proto file change would have caught both incidents regardless of repo structure. By skipping this diagnosis, the question channels respondents toward a structural migration when a pipeline fix might suffice. **Impact: The entire decision may be solving the wrong problem, risking 2-4 months of migration effort for a fix achievable in days.**

- **The question assumes the monorepo tooling options (Nx, Turborepo, Bazel) are interchangeable.** They are radically different. Nx and Turborepo are JavaScript-ecosystem tools with bolted-on polyglot support. Bazel is a polyglot build system with a brutal learning curve and no team on staff to maintain it. For a Node/Python/Go stack with no platform team, the realistic monorepo tooling options are far narrower than the question implies — possibly none of the three named tools are a good fit. **Impact: Respondents may recommend "use a monorepo with Bazel" without accounting for the 3-6 month Bazel adoption curve and ongoing maintenance tax that a 15-person team cannot absorb.**

- **Developer experience during transition is listed as a criterion but not decomposed.** "Developer experience" during a monorepo migration means: learning a new build system, rewriting all CI pipelines, changing git workflows (sparse checkout? virtual filesystem?), losing per-repo git history or accepting a grafted history, updating every developer's local tooling. The question treats this as a single line item when it is actually 5-6 distinct workstreams, each with its own risk profile. **Impact: Migration cost estimates will be systematically underestimated by 2-3x because the work is not disaggregated.**

- **No mention of the monorepo's impact on CI duration at scale.** The current 8-12 minute CI runs are *per repo*. In a monorepo, the question becomes: does every PR run all three services' test suites, or do you invest in affected-target analysis? If the former, CI goes from 8-12 minutes to 24-36 minutes (or worse, serial). If the latter, you need Bazel-level build graph analysis — which circles back to the tooling problem the team cannot staff. **Impact: CI speed, listed as a decision criterion, could actually *degrade* under the monorepo option, directly contradicting the expected benefit.**

- **The question does not address code review and merge contention.** In a monorepo with 15 engineers (growing to 30), the `main` branch becomes a shared resource. Merge conflicts increase quadratically with contributor count. CODEOWNERS files help but do not eliminate the coordination cost of a busy trunk. In polyrepo, each squad merges independently. **Impact: The monorepo may trade one coordination problem (cross-repo schema PRs) for another (merge contention on a shared trunk), and the second problem scales worse.**

- **No consideration of the "monorepo without monorepo tooling" failure mode.** Teams that move to a monorepo without investing in proper build orchestration end up with something worse than either option: a single repo where every change triggers full CI, where there is no affected-target analysis, and where the build system is duct-taped shell scripts. This is the most common monorepo failure mode in practice, and the question's constraint (no platform team) makes it the likely outcome. **Impact: The monorepo option may be evaluated against its ideal state while the polyrepo option is evaluated against its current flawed state — an asymmetric comparison that biases the decision.**

---

### Off-Base Assumptions

1. **"Cross-service changes require coordinating PRs across repos" is treated as inherently bad.** Coordinated PRs are a forcing function for explicit cross-team communication. In a monorepo, a single engineer can make an atomic commit that changes the proto schema *and* all three consumers — which sounds efficient until you realize it means one person is modifying code owned by three different squads without the natural review gate that separate PRs provide. The coordination overhead of polyrepo PRs is also a coordination *benefit*: it makes cross-service changes visible, reviewable, and reversible per-service. The question assumes this friction is pure cost. It is also a safety mechanism.

2. **The question assumes the team will successfully adopt monorepo build tooling.** For a polyglot stack (Node/Python/Go) with no platform team, the probability of successfully adopting and maintaining Bazel, Nx, or Turborepo as a monorepo build system is significantly lower than the probability of successfully adding a schema registry and contract tests to the existing polyrepo setup. The question presents both options as equally feasible when they have very different implementation risk profiles. The monorepo option requires the team to become experts in a build system domain that is orthogonal to their product work; the polyrepo option extends patterns (CI jobs, test suites) they already understand.

3. **The 12-month growth projection (15→30 engineers) is presented as favoring the monorepo, but the opposite case is at least as strong.** Monorepos become harder to manage as teams grow: slower clones, larger CI graphs, more merge contention, more pressure on build tooling. Google and Meta make monorepos work at scale because they have dedicated teams of 50+ engineers building custom VCS and build infrastructure. A 30-person startup will not have this. The polyrepo model, with proper cross-repo tooling, may actually *scale better* for a team that will never have dedicated platform engineers — because each squad retains full autonomy over their build, test, and deploy pipeline. The question should force respondents to argue the scaling case in both directions, not assume monorepo scales better by default.

---

### Actionable Recommendations

1. **Isolate the Schema Problem**
   - **Priority:** P1
   - **Current state:** Schema mismatches are the stated motivation for the entire decision, but no targeted solution has been attempted.
   - **Proposed change:** Before evaluating repository topology, implement a cross-repo CI gate: a dedicated job that triggers on any `.proto` file change, pulls all proto files from all repos, and runs `buf breaking` and `buf lint` against every consumer's generated code. This can be a GitHub Actions workflow in a small `schema-ci` repo that triggers via repository dispatch.
   - **Rationale:** If this solves the production incident pattern, the monorepo's primary justification evaporates and the decision can be made on its actual merits rather than on pain that no longer exists.
   - **Risk if ignored:** The team migrates to a monorepo to solve a problem that a 50-line CI workflow would have fixed, consuming 2-4 months of engineering time during a critical growth phase.

2. **Require Asymmetric Risk Assessment**
   - **Priority:** P1
   - **Current state:** The question presents monorepo and polyrepo as two options with equal implementation risk.
   - **Proposed change:** Require respondents to explicitly estimate the probability of successful implementation for each option, including the probability of a partial or failed monorepo migration (which leaves the team in a worse state than either pure option).
   - **Rationale:** A monorepo migration that stalls at 60% completion — some services moved, some not, tooling half-built — is worse than the current polyrepo setup. This failure mode needs to be priced into the decision.
   - **Risk if ignored:** The team selects the monorepo based on its ideal-state benefits without accounting for the realistic probability of reaching that state given their constraints.

3. **Decompose Migration Cost Into Workstreams**
   - **Priority:** P1
   - **Current state:** "Migration cost and timeline" is a single decision criterion.
   - **Proposed change:** Break migration cost into: (a) repository consolidation and history preservation, (b) build system adoption and configuration, (c) CI/CD pipeline rewrite, (d) developer tooling updates (IDE config, git workflows, sparse checkout), (e) CODEOWNERS and review process redesign, (f) deployment pipeline changes. Estimate each independently.
   - **Rationale:** Aggregated estimates for complex migrations are systematically optimistic. Disaggregation forces honest accounting.
   - **Risk if ignored:** The team commits to a monorepo migration expecting 4-6 weeks of work and discovers 3-4 months of work after the point of no return.

4. **Benchmark CI Duration Under Monorepo**
   - **Priority:** P2
   - **Current state:** CI runs are 8-12 minutes per repo. No estimate is provided for monorepo CI.
   - **Proposed change:** Before deciding, prototype the monorepo CI pipeline. Run all three services' test suites in sequence and in parallel to establish baseline monorepo CI time. Then estimate the effort required to implement affected-target analysis to bring it back to per-service timing.
   - **Rationale:** If monorepo CI is 30+ minutes without affected-target analysis, and affected-target analysis requires Bazel-level tooling, the CI speed criterion may actually *favor* polyrepo — the opposite of the expected outcome.
   - **Risk if ignored:** The team migrates to a monorepo expecting faster CI and gets slower CI, degrading developer velocity — the primary metric they are trying to improve.

5. **Evaluate the "Thin Shared Repo" Middle Path**
   - **Priority:** P2
   - **Current state:** The question frames the decision as binary: monorepo or polyrepo.
   - **Proposed change:** Evaluate a third option: keep three service repos but create a fourth shared repo for proto schemas, shared libraries, and cross-service integration tests. This repo becomes the integration point with its own CI that validates all consumers. Services pin to tagged releases of the shared repo.
   - **Rationale:** This captures the atomic-schema-change benefit of a monorepo without the build system complexity, merge contention, or migration cost. It is the minimum viable version of "shared code in one place."
   - **Risk if ignored:** The team debates a false binary and misses the option that best fits their constraints (polyglot, no platform team, growing fast).

6. **Stress-Test the Scaling Argument**
   - **Priority:** P2
   - **Current state:** Growth to 25-30 engineers is cited as a factor but not analyzed directionally.
   - **Proposed change:** Require respondents to argue the scaling case for *both* options. Specifically: at 30 engineers with 5-6 services (reasonable 12-month projection), what does merge contention look like in a monorepo? What does CI time look like? What platform engineering investment is required to keep the monorepo healthy? Compare against polyrepo with a schema registry and contract testing.
   - **Rationale:** The implicit assumption that monorepos scale better is true only with significant infrastructure investment. Without a platform team, the polyrepo model may scale more gracefully because each squad retains full pipeline autonomy.
   - **Risk if ignored:** The team makes a decision optimized for 15 engineers that becomes a drag at 30, in either direction.

7. **Define Rollback Criteria**
   - **Priority:** P2
   - **Current state:** No rollback plan or failure criteria are mentioned.
   - **Proposed change:** If the monorepo path is chosen, define explicit failure criteria (e.g., CI time exceeds 20 minutes after 8 weeks, more than 5 merge conflicts per week on main, build tooling requires more than 10% of one engineer's time to maintain) and a concrete rollback plan.
   - **Rationale:** Monorepo migrations are notoriously difficult to reverse. Defining failure criteria upfront prevents the sunk-cost fallacy from keeping the team on a failing path.
   - **Risk if ignored:** The team ends up in the worst-case scenario — a half-migrated monorepo with inadequate tooling that is too expensive to complete and too expensive to undo.

8. **Name the Opportunity Cost**
   - **Priority:** P3
   - **Current state:** Migration cost is discussed in terms of effort but not in terms of what the team will *not* build during migration.
   - **Proposed change:** Require the decision to explicitly name 2-3 product features or infrastructure improvements that will be delayed by the migration timeline. Frame the monorepo decision as "we are choosing to build repository infrastructure instead of [X, Y, Z] for the next N months."
   - **Rationale:** For a mid-stage startup, engineering time is the scarcest resource. Abstract "migration cost" does not create the same urgency as "we will delay the billing system rewrite and the EU data residency requirement by 6 weeks."
   - **Risk if ignored:** The migration is approved in a vacuum without competing against the product roadmap, leading to regret when product deadlines slip.
