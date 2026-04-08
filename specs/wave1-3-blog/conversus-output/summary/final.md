# Synthesis: Wave 1-3 Blog Posts

**Synthesized by**: synthesis agent
**Date**: 2026-04-03
**Inputs**: Reviews, revisions, and disputes from technical-writer, storyteller, and docs-updater
**Target specs**: 032 (package splitting), 033 (monetization partitioning), EXECUTION-ORDER.md

---

## 1. Convergence Summary

### What all three agents agree on

1. **Post 1 structure**: The monolith-to-portable-to-monetizable arc is the correct organizing frame. Both content agents adopted this after cross-review.
2. **Build-time splitting narrative**: All agents agree that "source stays monolithic, build system produces multiple wheels" is the key insight and should be the centerpiece of Post 1.
3. **Deliberation is free, scoring is paid**: The free/paid boundary principle is correctly drawn and both posts should present it this way.
4. **Feature gating via try/except**: All agents agree the "detection, not enforcement" pattern (no license keys, no nag screens, no degraded output) is the right framing.
5. **`resolve_package_path` code**: All agents use the same code block and explanation. No disputes on accuracy.
6. **force-include mechanism**: All agents describe the Hatch `force-include` directive identically.
7. **31 split tests**: Verified as correct (14 parametrized test functions expanding to ~31 cases).
8. **Seven files with Path(__file__).parent**: Verified as correct across all three agents.
9. **Four new payoff functions**: All agents agree on the `(payoff, best_response_payoff)` interface and the four new modes.
10. **Post 1 timeline**: 12 hours across 2 calendar days. Storyteller's "two calendar days" phrasing adopted over ambiguous "48 hours."
11. **`estimate_cost` duplication**: All agents agree this was the correct fix for the cross-package coupling violation.

### What changed during cross-review and revision

- **Technical-writer** adopted the storyteller's narrative arc (monolith/portable/monetizable labels), "no nag screens" cadence, and problem-first opening.
- **Technical-writer** added "apply this to your own system" closing section to Post 2, inspired by the storyteller's four-step pattern.
- **Technical-writer** changed Post 2 category from `Architecture` to `Process` to comply with `mkdocs.yml`.
- **Technical-writer** qualified AMPL claims: infrastructure + config optimizer exist; per-mode model templates are future (specs 043-044).
- **Storyteller** corrected "41 specs" to "43 specs" and "48 hours" to "two calendar days."
- **Storyteller** dropped "60-line module" claim (module is 164 lines).
- **Storyteller** added three-tier solver fallback section to Post 2 (previously absent).
- **Storyteller** softened Kalman to "architecture supports" language.
- **Storyteller** explicitly stated gamma is "the one tunable parameter" today.
- **Docs-updater** reframed the missing `pip install` path as a deliberate earlier removal that now needs restoring (not an oversight).
- **Docs-updater** added three new gaps from cross-review: SDK import path, CLI install note, web UI install path.
- **Docs-updater** corrected Python version handling: 3.11+ for published package, 3.12+ for dev environment.

---

## 2. Dispute Resolutions

### Dispute 1: Post 2 Category

**Decision**: Use `Process` (mkdocs.yml compliant).

**Rationale**: Three agents proposed three different categories (AI, Architecture, Process). Only `Process` is in `categories_allowed` without requiring a `mkdocs.yml` change. The post describes a scoring methodology and solver selection workflow, which fits `Process`. Expanding the taxonomy can happen deliberately later -- not as a side effect of a blog post.

### Dispute 2: Two Post 2 Drafts

**Decision**: Merge the best elements from each. See Post 05 in Section 3.

- **Title and opening hook**: Use the storyteller's "Why Your AI Agents Give Different Answers Every Time (And How to Fix It)" -- this is stronger for LinkedIn discoverability and speaks to a felt problem.
- **Worked example and solver table**: Use the technical-writer's `prisoners_dilemma_payoff` code block, the 8-mode game-form table with equilibrium concepts, and the game-form-to-solver-tier mapping table. These give the post substance that justifies the title's promise.
- **Four-step closing pattern**: Use the storyteller's actionable steps, which both agents converged on.
- **Three-tier fallback**: Include the technical-writer's explicit install commands and tier descriptions, with the storyteller's graceful-fallback framing.

### Dispute 3: AMPL Claims

**Decision**: Use the technical-writer's qualified language.

- **Exists today**: AMPL infrastructure (amplpy + HiGHS binding), config optimizer module.
- **Planned (specs 043-044)**: Per-mode AMPL model templates formalizing each game form's optimization structure.
- The storyteller's phrasing ("AMPL formulations with the HiGHS solver can compute provably optimal allocations") overstates current capability and is not used.

### Dispute 4: Kalman Convergence Prediction

**Decision**: Qualify as architectural capability, not a user-documented feature.

- The Kalman filter code exists in the solvers package.
- No user-facing documentation exists.
- Blog language uses the storyteller's "the architecture supports" phrasing with the caveat "not yet documented for end users."
- The technical-writer's Post 1 mention of "convergence prediction" in the paid-tier list is retained but qualified.

### Dispute 5: Post 1 Title

**Decision**: Use a merged title: "From Heuristics to pip install -- How We Made a Monolith Portable in Three Waves". The storyteller's "Monolith Portable in Three Waves" is more descriptive of the post structure and echoes the arc labels both agents adopted.

### Dispute 6: gamma Tunability

**Decision**: Use the storyteller's explicit "one tunable parameter today" phrasing. The technical-writer's extended gamma discussion (gamma at 0.0, 0.5, 1.0, 2.0 with domain examples) is retained for illustrative value, but prefaced with the caveat that gamma in PD mode is currently the only user-tunable parameter across all eight modes. Future expansion is noted as specs 043-044.

---

## 3. Final Blog Posts

### Post 04: "From Heuristics to pip install"

```markdown
---
date: 2026-04-03
categories:
  - Engineering
  - Release
authors:
  - conversus-team
title: "From Heuristics to pip install -- How We Made a Monolith Portable in Three Waves"
description: "We started with 43 specs, a framework welded to Claude Code, and 8 modes that couldn't score themselves. Three waves later, conversus is pip-installable, the free/paid line is drawn, and the monolith never moved a single file."
---

# From Heuristics to pip install -- How We Made a Monolith Portable in Three Waves

Forty-three specs. A deliberation engine that runs 8 competition modes across a 5-phase pipeline with dispute detection, stagnation tracking, and multi-round convergence. Templates, presets, schemas, a linter, an MCP server, a web UI. All of it hardwired to a source tree that assumed it would always run inside Claude Code.

We needed to turn this into something you could `pip install`. Without breaking the development workflow. Without moving files into separate repos. Without losing the ability to `uv run pytest` and have everything pass.

Three waves of work over two calendar days took conversus from **monolith** to **portable** to **monetizable**. This post covers the technical decisions behind each wave and why the alternatives were worse.

<!-- more -->

## The Two Problems Blocking Users

**Problem 1: The scoring gap.** Four of the eight modes -- negotiation, resource-allocation, fair-division, mechanism-design -- had no payoff functions. The EquilibriumScorer could compute Nash equilibrium quality for the original four modes but returned nothing for the new ones. Half the framework was invisible to quantitative analysis.

**Problem 2: The path problem.** Every template lookup, every preset resolution, every scaffold directory call used `Path(__file__).parent` and walked up the directory tree. This works when you clone the repo. It fails catastrophically inside a pip-installed wheel, where `templates/` lives inside the package, not alongside it.

Neither problem was visible in development. Both would be fatal in production.

## Wave 1: Making the Math Work (Specs 038 + 039)

Wave 1 ran two specs in parallel -- solver equilibrium fixes (038) and new mode payoffs (039). The goal was straightforward: every mode must be scorable.

Spec 038 was documentation surgery. The matrix shape table in spec 021 said WTA payoffs are N x 1, but the nashopt API expected N x N. The code matched the table, not the API. The cooperative payoff mixed `surviving_count` on the diagonal with `agreement_matrix` off-diagonal, producing uninterpretable equilibria. Three spec amendments, zero code changes, but they cleared ambiguity that would have blocked Wave 3's package split.

Spec 039 was the real work: four new payoff functions that gave the EquilibriumScorer coverage across all eight modes. The design decision that matters: every payoff function returns `(payoff, best_response_payoff)`. When `payoff == best_response_payoff`, the agent is at Nash equilibrium. This two-value interface is what makes the scoring tier valuable -- it does not just tell you a number, it tells you whether the number could be better.

Take the negotiation payoff. It computes `zopa_coverage * party_satisfaction`. Best response is 1.0 -- full ZOPA coverage with full satisfaction. The gap between actual and best-response payoff is the quantitative measure of how far the negotiation drifted from optimal.

Or the prisoners-dilemma payoff, which computes `territory_held - gamma * overreach_penalty`. That `gamma` parameter is currently the only user-tunable knob across all eight modes -- it controls how harshly agents are penalized for overreach in PD mode. The payoff function is pure: same features, same gamma, same score every time. No randomness, no prompt sensitivity, no model variance.

After Wave 1, all eight modes had payoff functions, all returning the same `(payoff, best_response_payoff)` interface, all testable with representative feature data.

## Wave 2: Five Parallel Agents Find Eight Breaks

Wave 2 was the session that changed the project's trajectory.

We called it MIT-1 -- the minimum import test. Five agents ran in parallel, each tracing the import graph of a different future package. Their job: find every place where importing a module pulled in something it shouldn't.

They found eight path breaks.

Seven files used `Path(__file__).parent` traversal to find templates, presets, or schemas. In a source tree, this works because the directory structure is predictable. In a wheel, the traversal points to the wrong directory -- or to a directory that does not exist at all. The engine, the linter, the schema loader, the domain framework -- all broken.

### The fix: `conversus/paths.py`

The fix was `conversus/paths.py`, a single-module path resolver that finds data files using `importlib.resources` as the primary strategy and `Path(__file__)` traversal as a fallback for development:

```python
def resolve_package_path(package: str, *parts: str) -> Path:
    # Strategy 1: importlib.resources (pip-installed)
    try:
        ref = resources.files(package)
        for part in parts:
            ref = ref / part
        resolved = Path(str(ref))
        if resolved.exists():
            return resolved
    except (TypeError, FileNotFoundError, ModuleNotFoundError):
        pass

    # Strategy 2: walk up from __file__ (source tree)
    if parts:
        current = Path(__file__).resolve().parent
        for _ in range(5):
            candidate = current / Path(*parts)
            if candidate.exists():
                return candidate
            current = current.parent

    raise FileNotFoundError(...)
```

Two strategies. Try the package first. Fall back to the file system. Works in both worlds.

`importlib.resources.files()` is the standard library mechanism for locating data files inside installed packages. When you `pip install conversus`, Hatch's `force-include` directive copies `templates/`, `presets/`, and `schema/` into the wheel under `conversus/`. The `importlib.resources` call resolves them there. In development, the files live at the project root, so the fallback walks up the directory tree.

Why not just use `pkg_resources` or `__file__` with a fixed offset? `pkg_resources` is deprecated. A fixed `__file__` offset is fragile -- it breaks if the directory structure ever changes, and it is the exact pattern we were removing. `importlib.resources` is the blessed approach since Python 3.9, and it handles zip-imported packages, editable installs, and namespace packages correctly.

### force-include: getting data files into the wheel

The second half of the fix was `pyproject.toml`:

```toml
[tool.hatch.build.targets.wheel.force-include]
"schema" = "conversus/schema"
"templates" = "conversus/templates"
"presets" = "conversus/presets"
```

Without this, Hatch would build a wheel containing only Python modules. Templates and presets would be missing. `force-include` copies the project-root directories into the wheel under `conversus/`, where `importlib.resources.files("conversus")` can find them.

### One coupling violation

The eighth break was a cross-package import violation: the optimizer module imported `estimate_cost` from `engine.cost`. That single import meant `conversus-solvers` would drag in the entire engine -- defeating the point of splitting. The fix was duplicating the function into the optimizer's own module. It is a small, pure function. Duplication here is better than the coupling.

### 31 tests prove independence

`tests/test_package_split.py` verifies that each future pip package can import independently. It snapshots `sys.modules` before and after importing each module, then asserts that no forbidden cross-package modules appeared. For example, importing `conversus.schemas` must never trigger `conversus.plugins` or `conversus.domains`. Importing `conversus.plugins.nashopt` must never trigger `engine` or `linter`.

These 31 tests (14 test functions, expanded via parametrize) are the proof that physical package extraction is possible whenever the business needs it. They run in the existing `uv run pytest` suite -- the development workflow is unchanged.

## Wave 3: Build-Time Splitting (Spec 032)

Here is the decision that made everything possible: **the source code stays as a single monolith. The build system produces multiple wheels.**

### Why build-time splitting, not physical extraction

The obvious approach is to move files into separate directories, give each directory its own `pyproject.toml`, and publish independent packages. This is what most open-source projects do when they split.

We rejected it for three reasons:

1. **Moving files breaks imports.** Every `from conversus.plugins.nashopt import ...` becomes `from conversus_solvers.plugins.nashopt import ...`. Every test file, every doc example, every config reference changes.
2. **It splits the test suite.** You can no longer run `uv run pytest` to test everything. Each package needs its own test infrastructure, CI config, and fixture setup.
3. **Multi-repo coordination overhead.** A change that touches both the engine and a solver now requires coordinated PRs across repos.

Build-time splitting avoids all of this. No file moves. No import rewrites. No multi-repo coordination. One `pyproject.toml` for development (`uv run pytest` runs everything), and a `packages/` directory with per-package build configs that Hatch uses to produce separate wheels:

```
packages/
  core.toml       # conversus (free tier)
  solvers.toml    # conversus-solvers (paid tier)
  scenarios.toml  # conversus-scenarios
  swe.toml        # conversus-swe
```

Each TOML file tells Hatch which source directories to include or exclude. `core.toml` excludes `conversus/plugins/nashopt/**` and `conversus/plugins/optimizer/**`. `solvers.toml` only includes those directories. Same source tree, different slices.

The build script iterates over `packages/*.toml` and runs `hatch build` for each. Four wheels come out. Development workflow is unchanged -- `uv run pytest` still runs everything from the source tree.

Build-time splitting is also fully reversible: delete the `packages/` directory and you are back to a monolith. No code changes, no import changes, no test changes.

The `force-include` lines solve the path problem from Wave 2. Templates, presets, and schemas get bundled inside the wheel. `importlib.resources` finds them at runtime. The single-module `paths.py` resolver closes the loop.

### Why not submodules yet

Build-time splitting does not provide access control. Anyone who can see the source tree can build all packages. For monetization, the paid source code eventually needs to live in private repos -- which means extraction into git submodules.

But MIT-1 already proved zero coupling between packages. Extraction to submodules is mechanical -- just `git mv` the files and update the TOML configs. We shipped build-time splitting first because it unblocks users immediately. Submodule extraction follows when the business needs private repos.

## Wave 3b: Drawing the Line (Spec 033)

Splitting the package is a mechanical problem. Deciding where to split is a product decision.

### The principle: deliberation is free, scoring is paid

The free tier (`pip install conversus`) ships the complete deliberation engine. All 8 modes. All 5 phases (6 in multi-round deliberations with cross-round synthesis). Templates, presets, CLI, MCP server, web UI, schema validation, linter. Agents argue, cross-review, revise, and synthesize. You get the full pipeline.

The paid tier (`pip install conversus-solvers`) adds the quantitative layer. Heuristic payoff functions. Equilibrium scoring. Convergence prediction (architectural capability, not yet user-documented). Config optimization. nashopt integration.

### Why heuristics are paid

This is the decision that generates the most pushback. The payoff functions are "just math" -- weighted sums and ratios over extracted features. Why not give them away?

Four reasons:

1. **Comparability.** Without scoring, a deliberation produces reviews, cross-reviews, and a synthesis. With scoring, you know Agent A's position is 0.85 and Agent B's is 0.62. That number is what makes output comparable across runs.
2. **Consistency.** The same features always produce the same score. The deliberation itself is stochastic (LLM-generated), but the scoring is not.
3. **Tunability.** Parameters like `gamma` (the overreach penalty in prisoner's dilemma mode) give you a quantitative dial on agent behavior. Without the scoring tier, tuning means changing prompts.
4. **Value architecture.** If heuristics are free, the paid tier is "better heuristics" -- a weak value proposition. If heuristics are paid, the paid tier is the entire quantitative layer -- everything that makes agent output measurable.

### Feature gating: detection, not enforcement

The gating mechanism in v1 is trivial:

```python
try:
    from conversus.plugins.nashopt import EquilibriumScorer
    SOLVERS_AVAILABLE = True
except ImportError:
    SOLVERS_AVAILABLE = False
```

No license keys. No nag screens. No degraded output. Installed means available. Not installed means silently absent. The free tier is not a crippled version of the paid tier. It is a complete product that the paid tier extends.

`tests/test_free_tier.py` enforces this: importing `engine`, `engine.cli`, `conversus.schemas`, or `conversus.plugins.base` must never trigger imports of `nashopt`, `jax`, `amplpy`, `highspy`, or any paid plugin module. If a developer accidentally adds a paid dependency to the free path, the test fails.

## The Arc: Monolith to Portable to Monetizable

Three waves, two calendar days, and the framework went through three distinct states:

| Wave | Duration | State Change | Key Deliverable |
|------|----------|-------------|----------------|
| Wave 1 | 4 hours | Monolith (complete) | 8-mode payoff functions, 3 spec amendments |
| Wave 2 (MIT-1) | 4 hours | Portable | `conversus/paths.py`, 7 file fixes, 31 split tests |
| Wave 3 | 2 hours | Monetizable | 4 package TOMLs, build script, free/paid boundary |

**Monolith** (pre-Wave 1): Everything works, but only from a source checkout. Half the modes cannot score themselves. The engine is welded to the file system layout.

**Portable** (post-Wave 2): Every import boundary verified. Path resolution works in both source tree and wheel. 31 tests prove package independence. The engine can leave its original directory.

**Monetizable** (post-Wave 3): `pip install conversus` is a real thing. Four packages -- core, solvers, scenarios, swe -- each built from the same source tree. The free/paid boundary is drawn, tested, and enforced by the build system. The development workflow is unchanged -- same repo, same test command, same import paths. Packages are locally buildable via `scripts/build-packages.sh`; PyPI publication is a separate step that follows when the distribution channel is ready.

The critical insight was doing the split at build time, not at the source level. Physical extraction would have required rewriting imports, splitting the test suite, and coordinating multi-repo releases. Build-time splitting avoids all of this. The monolith stays monolithic where it matters (development) and splits where it matters (distribution).

One more thing. MIT-1 proved zero coupling between packages. That means extraction to separate repos is now mechanical whenever monetization requires access control for private packages. Build-time splitting ships first. Physical extraction follows when needed, not before.

The next wave is platform work: execution providers (spec 042) to decouple from Claude Code, the command center (spec 040) for a non-technical dashboard, and AMPL game-theoretic solver models (specs 043-044) to formalize what the heuristics approximate. But those are features on top of a framework that now ships as a package. The hard part is done.
```

---

### Post 05: "Why Your AI Agents Give Different Answers Every Time"

```markdown
---
date: 2026-04-03
categories:
  - Engineering
  - Process
authors:
  - conversus-team
title: "Why Your AI Agents Give Different Answers Every Time (And How to Fix It)"
description: "AI agents are non-deterministic by nature. Every run produces different output. Optimization models give you the scoring layer to make that output consistent, comparable, and reproducible -- here's the game-theoretic pattern behind it."
---

# Why Your AI Agents Give Different Answers Every Time (And How to Fix It)

You run three AI agents on the same code review. Agent A says the auth module needs a rewrite. Agent B says it's fine with minor patches. Agent C focuses entirely on test coverage.

You run it again. Agent A now agrees with Agent B. Agent C has a new concern about error handling.

Same input. Same prompts. Same model. Different answers. Every time.

This is the fundamental problem of multi-agent AI systems: **agents are non-deterministic, and without a scoring layer, you have no way to tell whether run #1 or run #2 produced the better result.**

<!-- more -->

## The Consistency Problem Is Not a Bug

LLMs are probabilistic. Temperature, sampling, context window positioning -- all of these introduce variance. When you chain multiple agents together, the variance compounds. Three agents with moderate variance each can produce wildly different collective outputs across runs.

Most teams try to solve this by tuning prompts. They add "be consistent" to the system message. They pin temperature to 0. They cache intermediate results. These help at the margins, but they do not solve the structural problem: **without a quantitative measure of output quality, you cannot compare runs.**

You can read Run A and read Run B and form an opinion about which is better. But that opinion is itself subjective and non-reproducible. You have replaced agent inconsistency with human inconsistency.

## The Optimization Model Approach

The alternative is to define a mathematical function that scores agent output. Not a vibe check. Not "this one feels more thorough." A function that takes extracted features from the output and returns a number.

This is what optimization models provide for multi-agent systems: **a deterministic scoring layer on top of non-deterministic generation.**

The concept is straightforward. After agents produce their output, you extract features from that output -- quantitative measurements of what actually happened. Then you feed those features into a payoff function that returns a score. Same features, same score. Always.

The score does not replace the output. The agents still produce their reviews, their arguments, their synthesis. The score tells you whether the dynamics that produced that output were healthy.

## How It Works in Practice

Consider a multi-agent negotiation. Three agents represent different stakeholders negotiating resource allocation. After each round, you extract two features per agent: how much of the negotiable space (the "zone of possible agreement") they covered, and how satisfied each party is with the proposed terms.

The payoff function is:

```
payoff = zopa_coverage * party_satisfaction
```

Best possible payoff is 1.0 -- full coverage, full satisfaction. The actual payoff tells you how far the negotiation drifted from optimal. And critically, the function also returns the best-response payoff -- what the agent could have achieved by playing optimally given what the other agents did.

When `payoff == best_response_payoff`, the agent is at Nash equilibrium. It could not have done better by changing its strategy unilaterally. When there is a gap, the agent left value on the table.

This gives you three things prompt engineering alone cannot:

**1. Comparability.** Run the negotiation ten times. Each run produces different text. But the payoff scores tell you which run produced the best dynamics. Run 7 scored 0.91 equilibrium quality. Run 3 scored 0.64. Run 7 was better, quantitatively.

**2. Tunability.** Some payoff functions accept parameters that change how strictly dynamics are scored. In adversarial mode (prisoners-dilemma), the function includes a `gamma` parameter that controls how harshly agents are penalized for overreach:

```
payoff = territory_held - gamma * overreach_penalty
```

Set `gamma = 0.5` and agents get away with moderate overreach. Set `gamma = 2.0` and any unjustified claim tanks their score. This is a deterministic knob that changes agent behavior without touching the prompt. Today, `gamma` in PD mode is the one tunable parameter across all eight modes; the other seven use fixed formulas. The parameter surface will expand as the framework matures (specs 043-044), but the pattern is established: pure functions with explicit coefficients, not prompt tweaks.

**3. Convergence tracking.** If you feed equilibrium scores across rounds into a filter -- even a simple exponential moving average -- you get a convergence signal. The architecture supports more sophisticated approaches (the solvers package includes a Kalman filter designed for this purpose, though it is not yet documented for end users). The goal is the same regardless of filter choice: know when to stop spending tokens. When scores stabilize, you have converged. When they diverge, cut your losses early.

## Game Forms: Why Mode Matters

Each of the 8 deliberation modes maps to a different game-theoretic structure. This is not a metaphor -- the mapping determines which payoff function computes the agent's score, which equilibrium concept defines optimality, and which optimization approach the solver uses.

| Mode | Game Form | Equilibrium Concept | What the Payoff Captures |
|------|-----------|-------------------|--------------------------|
| cooperative | Cooperative game | Pareto optimality | Recommendations surviving synthesis |
| winner-take-all | Zero-sum | Nash equilibrium | Binary win/loss |
| prisoner's dilemma | Non-cooperative | Nash equilibrium | Territory held minus overreach penalty |
| red-blue | Asymmetric | Minimax | Severity-weighted attack/mitigation |
| negotiation | Bayesian | Bayesian Nash | ZOPA coverage times party satisfaction |
| resource-allocation | Coalitional (Shapley) | Core stability | Utilization efficiency minus inequality |
| fair-division | Coalitional | Envy-freeness | Proportionality minus normalized envy |
| mechanism-design | Mechanism design | Incentive compatibility | Social welfare minus gaming vulnerability |

The mode selection is not decorative. When you choose `mode: prisoners-dilemma`, you are telling the scoring system to measure territory claims, deferral costs, and overreach penalties. When you choose `mode: cooperative`, you are telling it to measure surviving recommendations. The payoff function changes. The equilibrium concept changes. The downstream solver formulation changes.

## The Worked Example: Prisoner's Dilemma Payoff

The heuristic for prisoner's dilemma mode illustrates the full pattern:

```python
def prisoners_dilemma_payoff(
    agent_name: str,
    features: RoundFeatures,
    gamma: float = 1.0,
) -> tuple[float, float]:
    af = features.agent_features.get(agent_name)
    territory = (
        af.core_competency_count
        + af.unique_capability_count
        + af.shared_territory_count
        - af.deferral_count
    )
    overreach_penalty = max(0, af.overreach_count - af.overreach_rebutted)
    payoff = float(territory) - gamma * float(overreach_penalty)

    best_territory = (
        af.core_competency_count
        + af.unique_capability_count
        + af.shared_territory_count
    )
    best_response = float(best_territory)
    return payoff, best_response
```

`territory` counts what the agent holds. `overreach_penalty` counts unrebutted flags from cross-review. `gamma` controls how harshly overreach is punished. The best-response estimate assumes maximum territory with zero penalty -- the theoretical optimum an agent could achieve by being perfectly honest and well-evidenced.

The EquilibriumScorer uses the ratio `payoff / best_response_payoff` to compute a [0.0, 1.0] equilibrium quality score. An agent at best response scores 1.0. An agent far from best response scores lower. The aggregate across agents gives a round-level equilibrium quality metric.

The heuristic is an *approximation* of the equilibrium. It does not prove the agent is at Nash equilibrium -- it estimates the distance from it. This is sufficient for most use cases and is where the majority of users will stay.

## The Three-Tier Solver Fallback

The payoff functions are heuristic scorers -- fast, interpretable, and good enough for most use cases. But they are not the ceiling. The scoring architecture supports three tiers, each more powerful than the last:

**Tier 1: Heuristic payoffs (default).** The pure functions above. They run in microseconds, require no external dependencies, and produce the `(payoff, best_response_payoff)` pair directly from extracted features. This is what ships with `conversus-solvers`.

**Tier 2: AMPL/HiGHS (constrained optimization).** For users who need optimal configurations under budget constraints. The AMPL infrastructure and config optimizer exist today -- they solve for the optimal deliberation configuration (number of rounds, number of agents, iterations per phase) given a budget constraint. Per-mode AMPL model templates -- formalizing each game form's specific optimization structure -- are specified in specs 043 and 044 and will ship in a future wave. Install with `pip install conversus-solvers[ampl]`.

**Tier 3: nashopt/JAX (game-theoretic equilibrium).** For users who need game-theoretic proofs. Where the heuristic estimates distance from equilibrium and AMPL optimizes configuration, nashopt computes the actual Nash equilibrium of the game defined by the payoff matrix. If the agents' actual behavior matches the computed Nash equilibrium, the deliberation is provably stable -- no agent has an incentive to unilaterally deviate. Install with `pip install conversus-solvers[nashopt]`.

The fallback chain:

```
Tier 1 (heuristic) -> always available, default
Tier 2 (AMPL)      -> pip install conversus-solvers[ampl]
Tier 3 (nashopt)   -> pip install conversus-solvers[nashopt]
```

Each tier enriches the previous one. Heuristics give you scores. AMPL gives you optimal configurations. nashopt gives you equilibrium proofs. The PluginResult reports which solver was used: `"none"` (free tier), `"heuristic"`, `"ampl-highs"`, or `"nashopt"`.

How each game form connects to the solver tiers:

| Game Form | Heuristic Provides | AMPL Will Provide (specs 043-044) | nashopt Provides |
|-----------|-------------------|-----------------------------------|-----------------|
| Cooperative | Surviving count score | Budget-constrained Pareto check | Cooperative equilibrium |
| Zero-sum (WTA) | Win/loss score | Optimal agent allocation | Minimax equilibrium |
| Non-cooperative (PD) | Territory/overreach score | Config optimization | Mixed-strategy Nash |
| Bayesian (negotiation) | ZOPA/satisfaction score | Type-aware optimization | Bayesian Nash equilibrium |
| Coalitional | Efficiency/fairness score | Shapley-based allocation | Core membership proof |
| Mechanism design | Welfare/gaming score | Truthfulness verification | IC equilibrium |

## The Free/Paid Split

In conversus, we drew a specific line: the multi-agent deliberation engine is free. The scoring layer is paid.

The deliberation engine is the creative layer. Agents argue, cross-review, revise, and synthesize. The output is useful on its own. You read the synthesis and make your decision.

The scoring layer is the analytical layer. It tells you whether the deliberation dynamics were healthy, whether agents reached equilibrium, and how to compare runs quantitatively. The heuristic payoffs give you the baseline. The AMPL and nashopt tiers give you formal optimality guarantees.

Free users get the full deliberation. Paid users get the instrumentation that makes it enterprise-grade.

No license keys. No nag screens. No degraded output. Installed means available. Not installed means silently absent.

## Applying This to Your Own System

The pattern is not framework-specific. If you are building any multi-agent system and getting inconsistent results, the steps are:

**Step 1: Define what "good" means quantitatively.** For your specific task, what measurable properties of the output indicate quality? Coverage of the input space. Agreement between agents. Severity of findings. Ratio of justified to unjustified claims.

**Step 2: Write a pure scoring function.** It takes extracted features and returns a number. No LLM calls. Same features, same score. This is your ground truth for comparing runs.

**Step 3: Compute best-response.** For each agent, calculate what they could have scored if they played optimally given the other agents' strategies. The gap between actual and best-response is your equilibrium quality measure.

**Step 4: Track across rounds.** If your system runs multiple rounds, feed scores into a filter (exponential moving average works; Kalman is better). When the score stabilizes, you have converged. When it diverges, stop early and save the tokens.

The result: your multi-agent system still has the creative variance that makes LLMs useful, but you have a deterministic measurement layer that tells you when the variance produced a good outcome and when it did not.

## The Bottom Line

If you are building with AI agents and getting inconsistent results, the fix is not better prompts. Prompts control what agents say. Scoring functions control how you evaluate what they said. These are different problems with different solutions.

The pattern: generate with LLMs, score with math. Same features, same score, every time. That is the consistency your stakeholders are asking for, and no amount of prompt engineering will give it to you.

Build the scoring function. Measure equilibrium quality. Track convergence. Then decide whether run #1 or run #2 was better -- with numbers, not opinions.
```

---

## 4. Doc Fixes Required Before Publishing

Consolidated from the docs-updater's revision, prioritized. These must ship as a coordinated change before the blog posts go live.

### P0 -- Must fix before publishing (build-breaking or trust-breaking)

**P0-1: `docs/index.md` -- Restore `pip install` as primary install path**

Replace index.md Quick Install section (lines 28-31) with:

```markdown
## Quick Install

```bash
pip install conversus                    # Free: engine + 8 modes + templates + CLI
pip install conversus-solvers            # Paid: equilibrium scoring, convergence (optional)
pip install conversus[all]               # All sub-packages: solvers, scenarios, swe (optional)
```

!!! tip "Development setup"
    To work on conversus itself (Python 3.12+ required):
    ```bash
    git clone https://github.com/Build-Fractal/conversus.git && cd conversus
    uv sync
    ```
```

**P0-2: `docs/index.md` -- Three stale `clariti-care` org references + wrong license label**

- Line 10: Tests badge URL `clariti-care` -> `Build-Fractal`
- Line 11: License badge URL `clariti-care` -> `Build-Fractal`, label `proprietary` -> `MIT`
- Line 29: Clone URL `clariti-care` -> `Build-Fractal`

### P1 -- Critical path: Ship as a single coordinated update with P0

**P1-1: `docs/user-guide/quickstart.md` -- Add PyPI install as primary path**

Replace quickstart.md lines 9-20 with:

```markdown
## Install

### From PyPI (recommended)

```bash
pip install conversus              # Python 3.11+
```

This installs the free engine with all 8 deliberation modes, templates, presets, CLI, and MCP server.

For solver plugins (equilibrium scoring, convergence prediction):

```bash
pip install conversus-solvers      # Paid: nashopt, Kalman, AMPL (optional)
```

### From source (development)

```bash
git clone https://github.com/Build-Fractal/conversus.git && cd conversus
uv sync                            # Python 3.12+ required
uv sync --extra solvers            # nashopt + kalman + AMPL (optional)
```
```

Note: Two Python version numbers are intentional. `core.toml` says `>=3.11` (published package with lighter deps). Root `pyproject.toml` says `>=3.12` (dev environment with all deps).

**P1-2: `docs/user-guide/sdk.md` -- `from engine` import path is misleading**

Add a prominent warning at the top of the SDK page, before any code examples:

```markdown
!!! warning "Import path"
    The Python package is installed as `conversus` but the import namespace is currently `engine`:
    ```python
    from engine import Deliberation, Result, validate  # correct
    # from conversus import ...                        # not yet -- see roadmap
    ```
    The `engine` namespace will be renamed to `conversus` in a future release.
```

**P1-3: Entry point inconsistency between dev and published package**

`pyproject.toml` line 24 declares `engine.cli:cli`. `packages/core.toml` line 23 declares `engine.cli:main`. Verify these resolve to the same behavior. If they do, align both files to use the same entry point string. If they differ, document which is canonical. This must be verified before the doc fixes ship.

### P2 -- Should fix before publishing

**P2-1: `docs/user-guide/config-reference.md` -- No free/paid boundary callout**

Add after the plugins section (after line 175):

```markdown
!!! info "Premium Feature"
    The `equilibrium-scorer` and `scenario-runner` plugins require the paid
    `conversus-solvers` package. Install with `pip install conversus-solvers`.
    Without it, these plugins are skipped (see note above) and the deliberation
    completes normally without scoring.
```

**P2-2: `docs/user-guide/cli.md` -- Install note assumes `uv sync` as primary**

Replace CLI reference lines 5-6 with:

```markdown
If you installed via `pip install conversus` (recommended), run commands directly:
`conversus run config.yml`. If you're developing from source with `uv sync`,
prefix commands with `uv run`.
```

**P2-3: Solver install extras not documented**

Add to quickstart install section or config reference:

```markdown
For specific solver backends:
```bash
pip install conversus-solvers[nashopt]    # Nash equilibrium (jax)
pip install conversus-solvers[ampl]       # AMPL/HiGHS optimization
```
```

### P3 -- Nice to have

**P3-1: `docs/web.md` -- Web UI pip install path missing**

Add pip install option to the web docs page:

```markdown
### From PyPI
```bash
pip install conversus[web]          # Adds FastAPI + Uvicorn
```
```

**P3-2: Design system (`fractal.css`) undocumented** -- Purely internal contributor concern. Low urgency.

**P3-3: `conversus/paths.py` not in architecture docs** -- Blog Post 04 describes it as the key Wave 2 deliverable but `docs/developer-guide/architecture.md` does not mention it. Developer-facing, low urgency.

### Recommended shipping order

1. **Single coordinated commit**: P0-1 + P0-2 + P1-1 + P1-2 (closes the gap between blog promises and docs)
2. **Investigate then fix**: P1-3 (entry point consistency -- requires code inspection)
3. **Follow-up commit**: P2-1 + P2-2 + P2-3 (polish before blog promotion)
4. **Backlog**: P3-1, P3-2, P3-3

The sequence matters: a reader arrives at the index, clicks to the quickstart, then opens the SDK page. If any of those three contradict the blog's `pip install conversus` narrative, the reader's trust breaks at that point.

---

## 5. Remaining Disputes

**All disputes have been resolved by synthesis.** No disputes block publishing.

For the record, here is what was decided and why:

| # | Dispute | Resolution | Rationale |
|---|---------|------------|-----------|
| 1 | Post 2 category | `Process` | mkdocs.yml compliant, no config changes needed |
| 2 | Two Post 2 drafts | Merged | Storyteller title/hook + technical-writer depth/tables |
| 3 | AMPL claims | Technical-writer's qualified language | Config optimization exists; per-mode templates are future |
| 4 | Kalman | Architectural capability qualifier | Code exists but no user docs; use "architecture supports" |
| 5 | Post 1 title | Storyteller's phrasing | "Monolith Portable in Three Waves" echoes the arc labels |
| 6 | gamma tunability | Storyteller's explicit caveat | "One tunable parameter today" is the most accurate framing |

The one dependency that remains outside the blog posts: **P1-3 (entry point consistency)** must be verified in code before the doc fixes ship. If `engine.cli:cli` and `engine.cli:main` resolve differently, users who `pip install conversus` will get different CLI behavior than dev-installed users. This is a code investigation, not a blog-content dispute.
