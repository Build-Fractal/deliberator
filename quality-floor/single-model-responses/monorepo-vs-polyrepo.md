# Monorepo vs Polyrepo: Analysis and Recommendation

## Summary

You should consolidate into a monorepo. The two production incidents from protobuf schema mismatches are the clearest signal: your services aren't as independent as your repository structure pretends they are. When shared schemas are the integration surface and cross-service changes are frequent enough to cause outages, separate repositories create coordination overhead that compounds as the team grows. A monorepo won't solve every problem, but it directly addresses the ones that are currently hurting you.

---

## Analysis of Key Tradeoffs

### The Core Problem

Your three services share a gRPC contract defined by 4 protobuf files. This is a tight coupling point — any schema change is inherently a cross-service change. In a polyrepo setup, this means synchronized PRs, version pinning, and hoping that each repo's CI catches incompatibilities that only manifest at integration. You've already seen this fail twice in one quarter. That's not a tooling gap you can paper over; it's a structural mismatch between your dependency graph and your repository topology.

### What Polyrepo With Better Tooling Would Require

Staying polyrepo and solving the schema problem means building or adopting:

- **A shared schema registry** with versioning, backward-compatibility checks, and automated publishing. Buf is the most mature option here.
- **Contract testing** (e.g., Pact for gRPC) across all three services, with a centralized test suite that runs on every schema change.
- **A release coordination bot** that can detect when a schema change needs corresponding updates in consumer repos, open PRs, and block deployments until all are green.
- **Unified CI visibility** so developers can see the integration state across all three repos, not just their own.

This is a real platform engineering effort. You'd be building internal tooling to compensate for the fact that your repos don't reflect your dependency structure. With no dedicated platform team and 15 engineers, this work falls on squads that are already managing their own CI and deployments. The opportunity cost is high, and the tooling itself becomes a maintenance burden.

It's not impossible — large organizations with hundreds of services and dedicated platform teams do this well. But those organizations have the staffing to build and maintain cross-repo infrastructure as a product. You don't, and you won't at 25-30 engineers either.

### What a Monorepo Gives You

A monorepo puts your protobuf schemas, all three services, and shared infrastructure (Kubernetes manifests, CI config, linting rules) in one place. The direct benefits:

- **Atomic cross-service changes.** A schema update and all consuming service changes land in a single PR. CI validates the full integration surface before merge. The class of bug that caused your two production incidents becomes structurally impossible.
- **Unified CI/CD.** One pipeline configuration instead of three. Build orchestration tools (more on this below) handle caching, affected-service detection, and parallel execution. You stop maintaining three separate CI setups.
- **Shared tooling without extraction.** Linting, formatting, testing conventions, deployment scripts — these live once and apply everywhere. No need to publish internal packages or coordinate version bumps across repos.
- **Discoverability.** New engineers (and you'll be onboarding many as you grow to 30) can see the full system in one checkout. They can trace a gRPC call from gateway to pipeline to notification service without switching repos.

### What a Monorepo Costs You

- **Migration effort.** Consolidating three repos with history preservation is a multi-day project. It's disruptive but bounded — this is a one-time cost.
- **Build orchestration complexity.** You need a tool that understands your dependency graph and only builds/tests what changed. Without it, CI times will balloon as the repo grows.
- **Ownership boundaries become conventions.** In polyrepo, ownership is structural — you own your repo. In a monorepo, ownership is defined by CODEOWNERS files and team conventions. This works fine at 30 engineers but requires intentionality.
- **Tooling learning curve.** Whichever build orchestrator you choose, the team needs to learn it. This is real but manageable — these tools exist specifically because monorepos at your scale are common.

---

## Evaluation Given Your Context

Several factors in your situation tilt strongly toward monorepo:

**Team size.** 15 engineers growing to 30 is well within the range where monorepos work smoothly. The coordination overhead of polyrepo scales worse than the tooling overhead of monorepo at this size. Google, Meta, and Stripe run monorepos at thousands of engineers — you're orders of magnitude smaller. The "monorepos don't scale" argument doesn't apply until you're well past 100 engineers, and even then it's debatable.

**Three services, not thirty.** You have a small, tightly coupled service graph. The monorepo won't be unwieldy. A polyrepo strategy makes more sense when you have dozens of genuinely independent services with separate release cadences and no shared schemas. That's not your situation.

**No platform team.** Cross-repo tooling (schema registries, contract testing, coordination bots) needs someone to build and maintain it. A monorepo with a build orchestrator is a more self-service model — the tool handles dependency detection, caching, and selective builds. You configure it once and it scales with you.

**Mixed language stack.** Node.js, Python, and Go in one repo is fine with the right build tool. Bazel handles polyglot natively. Nx and Turborepo are more JavaScript-centric but can shell out to language-specific build commands. This is a factor in tool selection, not a reason to avoid monorepo.

**Growth trajectory.** As you onboard engineers, a monorepo with clear ownership conventions (CODEOWNERS, directory structure, CI checks) is easier to ramp into than navigating three repos with implicit knowledge about which schema versions are compatible and how to coordinate releases.

---

## Recommendation

**Consolidate into a monorepo. Use Bazel as your build orchestrator.**

Here's why Bazel over the alternatives:

- **Polyglot support.** You have Node.js, Python, and Go. Bazel has mature rulesets for all three (`rules_nodejs`, `rules_python`, `rules_go`) plus first-class protobuf support (`rules_proto`). Nx and Turborepo would require you to wrap Python and Go builds in npm scripts, which is a leaky abstraction.
- **Hermetic builds.** Bazel sandboxes builds and enforces declared dependencies. This prevents the "works on my machine" class of issues and makes CI results trustworthy.
- **Remote caching.** Bazel's remote cache (via Bazel Remote or a cloud service) means CI doesn't rebuild what hasn't changed, even across branches and developers. Your 8-12 minute per-repo CI times should stay flat or improve as the repo grows.
- **Protobuf integration.** Bazel can compile your protobuf schemas and generate language-specific stubs as build targets. Changing a `.proto` file automatically triggers rebuilds of all dependent services. This is exactly the integration guarantee you're missing.

The learning curve is the main downside. Bazel's BUILD file syntax and dependency model take a week or two to internalize. But the investment pays off immediately in CI reliability and scales with your growth.

**If Bazel's learning curve feels too steep for your current velocity pressure**, Turborepo is a reasonable second choice. It's simpler to adopt, handles task orchestration and caching well, and your team likely already has JavaScript/TypeScript familiarity. You'd need to set up language-specific build scripts for Python and Go services and handle protobuf compilation separately, but it's workable at your scale. Nx is a similar alternative with more built-in structure but heavier configuration.

---

## Implementation Plan

### Phase 1: Preparation (1 week)

- Choose your build orchestrator and spike a proof-of-concept with one service and the protobuf schemas.
- Define the directory structure:
  ```
  /
  ├── proto/                  # Shared protobuf schemas
  ├── services/
  │   ├── api-gateway/        # Node.js/Express
  │   ├── data-pipeline/      # Python/FastAPI
  │   └── notifications/      # Go
  ├── infra/
  │   ├── k8s/                # Kubernetes manifests
  │   └── ci/                 # Shared CI configuration
  ├── tools/                  # Shared scripts and utilities
  ├── CODEOWNERS
  └── BUILD / workspace config
  ```
- Set up CODEOWNERS mapping each directory to its squad. Configure branch protection to require CODEOWNERS approval.
- Write the CI pipeline that runs affected-service detection and parallel builds.

### Phase 2: Migration (1-2 weeks)

- Use `git subtree` or a tool like `tomono` to merge the three repos with full history into the new structure. Preserving git history matters — `git blame` and `git log` remain useful for debugging and onboarding.
- Migrate CI/CD. Start with a simple "build everything" pipeline and add selective builds once it's stable.
- Run the old and new pipelines in parallel for one sprint. Deploy from the monorepo only after the team confirms parity.

### Phase 3: Stabilization (1-2 weeks)

- Archive the old repositories (read-only, not deleted — links in docs and issues still resolve).
- Tune build caching and selective test execution.
- Write a short internal guide: how to create a PR, how to run tests locally for one service, how to update protobuf schemas.
- Set up remote caching if using Bazel.

**Total timeline: 3-5 weeks**, with the team fully productive on the monorepo by the end. The migration itself (Phase 2) is the most disruptive — plan it during a lighter sprint.

---

## Risk Factors to Monitor

### During Migration

- **CI parity gaps.** The most dangerous moment is when you switch deployment from old repos to the monorepo. Run both in parallel and diff the outputs before cutting over. Don't rush this.
- **Developer friction.** Engineers will hit unfamiliar build tool errors in the first two weeks. Designate one person per squad as the monorepo point-of-contact who can unblock others. This investment in knowledge distribution pays for itself quickly.
- **Large repo clone times.** At three services, this won't be a real problem. If it becomes one later, Git's sparse checkout and partial clone features handle it. Don't optimize prematurely.

### Post-Migration

- **Ownership erosion.** In a monorepo, it's easy for "quick fixes" to cross ownership boundaries without review. CODEOWNERS enforcement is essential — make it a blocking check, not advisory. Review CODEOWNERS quarterly as teams shift.
- **CI time creep.** Without proper affected-target detection, CI will slow down as code accumulates. Monitor P50 and P95 CI times monthly. If they drift past 15 minutes, invest in build graph optimization.
- **Dependency coupling.** A monorepo makes it easy to import across service boundaries — too easy. Establish a rule: services communicate only via defined APIs (gRPC contracts), not by importing each other's internal modules. Enforce this with build-level visibility rules (Bazel makes this trivial; other tools need linting).
- **Merge contention.** At 30 engineers with one repo, you'll see more merge conflicts on shared files (protobuf schemas, CI config, shared tooling). This is actually a feature — it surfaces coordination that was previously invisible. But it means your trunk-based development practices need to be solid: short-lived branches, frequent rebases, fast CI feedback.

### The "What If We're Wrong" Escape Hatch

If the monorepo doesn't work out — unlikely at your scale, but worth acknowledging — extracting a service back to its own repo is straightforward with `git subtree split`. You'd preserve history and the service would be independently deployable again. The migration is not a one-way door.

---

## Final Note

The schema mismatch incidents are the strongest argument here. Every hour your team spends coordinating PRs across repos, debugging version mismatches, or maintaining parallel CI pipelines is an hour not spent on product work. A monorepo doesn't eliminate coordination — it makes coordination visible and enforceable at the tooling level instead of relying on human process. At 15 engineers growing to 30, with tightly coupled services and no platform team, that's the right tradeoff.
