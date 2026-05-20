# Revision Notes

**Revision by**: technical-writer
**Date**: 2026-04-03
**Addressing feedback from**: storyteller cross-review, docs-updater cross-review, own cross-reviews of storyteller and docs-updater

## Changes Made

### P0: Post 2 category fix
- Changed `Architecture` to `Process` in Post 2 frontmatter. mkdocs.yml `categories_allowed` only permits Engineering, Process, Release. The post's focus on design methodology and solver selection workflow fits Process better than duplicating Engineering.

### Storyteller feedback: Post 2 game-form mapping section too dense
- Replaced the six dense paragraphs in "How Game Forms Map to Optimization Problems" with a table-driven structure and a single worked example (cooperative mode). Removed the sequential Pareto/minimax/Nash/Bayesian-Nash/core-stability/incentive-compatibility wall. Readers who need the full mapping can follow a reference to the developer guide.

### Docs-updater feedback: Tone down AMPL claims
- Added explicit qualifier that AMPL per-mode model templates are specified in specs 043-044 but not yet implemented. The AMPL infrastructure (amplpy + HiGHS integration) exists; the per-mode optimization formulations are forward-looking.
- Changed "AMPL defines *how* to optimize it" language to future-oriented phrasing.
- Qualified the Tier 2 description to distinguish what exists (infrastructure, config optimization) from what is planned (per-mode AMPL model templates).

### Adopted storyteller's "monolith -> portable -> monetizable" framing
- Restructured Post 1 opening to establish context and stakes before diving into waves, adopting the storyteller's approach of starting with the scale of the system and the two blocking problems.
- Added the three-state arc labels (Monolith, Portable, Monetizable) as a summary frame.
- Adopted "No license keys. No nag screens. No degraded output." cadence from storyteller.

### Factual corrections
- Tightened "5-6 phases" to "5 phases (6 in multi-round deliberations with cross-round synthesis)."
- Verified 31-test count remains accurate (parametrized expansion of 14 test functions).
- Kept "seven files" claim (verified correct by docs-updater).
- Added qualifier about pip install: packages are locally buildable; PyPI publication is a separate step not yet completed.
- Removed the full payoff formula table from Post 1 Wave 1 section per storyteller feedback that formulas belong in API docs. Replaced with prose summary.

### Additional improvements from cross-review insights
- Added "Why not" justification framing that storyteller praised.
- Compressed the `compute_payoff` dispatcher code block in Post 2 (storyteller noted information fatigue by that point).
- Added an outward-facing "apply this to your own system" note at the end of Post 2, inspired by storyteller's four-step pattern.

---

# Blog Post 1

---

```markdown
---
date: 2026-04-03
categories:
  - Engineering
  - Release
authors:
  - conversus-team
title: "From Heuristics to pip install -- How We Got Conversus Ready for Users"
description: "Wave 1 added 8-mode payoffs, Wave 2 fixed every path resolution bug blocking pip install, and Wave 3 split a monolith into free and paid tiers at build time -- without moving a single file."
---

# From Heuristics to pip install -- How We Got Conversus Ready for Users

By spec 039, conversus was a complete multi-agent deliberation framework. Eight competition modes. A 5-phase pipeline with dispute detection, stagnation tracking, and multi-round convergence. Templates, presets, schemas, a linter, an MCP server, a web UI. All of it hardwired to a source tree that assumed it would always run from a git checkout.

We needed to turn this into something you could `pip install`. Without breaking the development workflow. Without moving files into separate repos. Without losing the ability to `uv run pytest` and have everything pass.

Three waves of work over two days took conversus from **monolith** to **portable** to **monetizable**. This post covers the technical decisions behind each wave and why the alternatives were worse.

<!-- more -->

## The Two Problems Blocking Users

**Problem 1: The scoring gap.** Four of the eight modes -- negotiation, resource-allocation, fair-division, mechanism-design -- had no payoff functions. The EquilibriumScorer could compute Nash equilibrium quality for the original four modes but returned nothing for the new ones. Half the framework was invisible to quantitative analysis.

**Problem 2: The path problem.** Every template lookup, every preset resolution, every scaffold directory call used `Path(__file__).parent` and walked up the directory tree. This works when you clone the repo. It fails inside a pip-installed wheel, where `templates/` lives inside the package, not alongside it.

Neither problem was visible in development. Both would be fatal in production.

## Wave 1: Completing the Payoff Functions (specs 038, 039)

Wave 1 ran two specs in parallel. The goal was straightforward: every mode must be scorable.

Spec 038 was documentation surgery. The WTA matrix shape discrepancy between the spec table and the nashopt API was resolved. The cooperative diagonal semantics issue -- mixing `surviving_count` with `agreement_matrix` -- was documented as heuristic-only rather than papered over with a bad fix. Three spec amendments, zero code changes, but they cleared ambiguity that would have blocked Wave 3's package split.

Spec 039 added four new payoff functions -- negotiation, resource-allocation, fair-division, and mechanism-design -- each returning the same `(payoff, best_response_payoff)` tuple as the original four. This two-value interface is what makes the scoring tier valuable: it does not just tell you a number, it tells you whether the number could be better. When `payoff == best_response_payoff`, the agent is at Nash equilibrium.

The `compute_payoff()` dispatcher now routes all 8 modes. This was a prerequisite for everything downstream -- the solvers package has no value if it can only score half the modes.

## Wave 2: Killing Path(__file__).parent (MIT-1)

Before you can ship a pip package, every file access in the codebase must work when the code is installed into a `site-packages` directory -- not just when it runs from a source checkout. We called this prerequisite "MIT-1" (Minimum Independent Test, iteration 1).

Five agents ran in parallel, each tracing the import graph of a different future package. They found eight breaks. Seven files across the engine, linter, schemas, and domains used `Path(__file__).parent` traversal to find templates, presets, and scaffolds at the project root. This works in development because `engine/phases.py` and `templates/cooperative/review.md` are siblings in the directory tree. It breaks completely when pip installs `engine/` into `site-packages/engine/` -- the templates are not there.

### The fix: `conversus/paths.py`

We created a single module with a two-strategy resolver:

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

    # Strategy 2: walk up from this file (development)
    if parts:
        current = Path(__file__).resolve().parent
        for _ in range(5):
            candidate = current / Path(*parts)
            if candidate.exists():
                return candidate
            current = current.parent

    raise FileNotFoundError(...)
```

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

MIT-1 also discovered that the optimizer plugin imported `estimate_cost` from `engine.cost`. That is a cross-package dependency -- the paid solvers package would drag in the entire engine at the Python import level. Duplication here is better than the coupling. The function is small and pure, so we copied it into the optimizer module and cut the import.

### 31 tests prove independence

`tests/test_package_split.py` verifies that each future pip package can import independently. It snapshots `sys.modules` before and after importing each module, then asserts that no forbidden cross-package modules appeared. For example, importing `conversus.schemas` must never trigger `conversus.plugins` or `conversus.domains`. Importing `conversus.plugins.nashopt` must never trigger `engine` or `linter`.

These 31 tests (14 test functions, expanded via parametrize) are the proof that physical package extraction is possible whenever the business needs it. They run in the existing `uv run pytest` suite -- the development workflow is unchanged.

## Wave 3: Build-Time Package Splitting (spec 032)

The goal was `pip install conversus`. The question was how to get there.

### Why build-time splitting, not physical extraction

The obvious approach is to move files into separate directories, give each directory its own `pyproject.toml`, and publish independent packages. This is what most open-source projects do when they split.

We rejected it for three reasons:

1. **Moving files breaks imports.** Every `from conversus.plugins.nashopt import ...` becomes `from conversus_solvers.plugins.nashopt import ...`. Every test file, every doc example, every config reference changes.
2. **It splits the test suite.** You can no longer run `uv run pytest` to test everything. Each package needs its own test infrastructure, CI config, and fixture setup.
3. **Multi-repo coordination overhead.** A change that touches both the engine and a solver now requires coordinated PRs across repos.

Build-time splitting avoids all of this. The source code stays as a single monolith. The build system produces multiple wheels from the same tree. A `packages/` directory contains one TOML config per wheel:

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

### Why not submodules yet

Build-time splitting does not provide access control. Anyone who can see the source tree can build all packages. For monetization, the paid source code eventually needs to live in private repos -- which means extraction into git submodules.

But MIT-1 already proved zero coupling between packages. Extraction to submodules is mechanical -- just `git mv` the files and update the TOML configs. We shipped build-time splitting first because it unblocks users immediately. Submodule extraction follows when the business needs private repos.

## Wave 3b: The Free/Paid Boundary (spec 033)

With packages split, the question becomes: what goes where?

### The principle: deliberation is free, scoring is paid

The free tier (`pip install conversus`) ships the complete deliberation engine. All 8 modes. All 5 phases (6 in multi-round deliberations with cross-round synthesis). Templates, presets, CLI, MCP server, web UI, schema validation, linter. Agents argue, cross-review, revise, and synthesize. You get the full pipeline.

The paid tier (`pip install conversus-solvers`) adds the quantitative layer. Heuristic payoff functions. Equilibrium scoring. Kalman convergence prediction. Config optimization. nashopt integration.

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

No license keys. No nag screens. No degraded output. If `conversus-solvers` is installed, its plugins load. If not, deliberation completes normally without scoring. The paid tier is additive -- the free tier is never a crippled version of the full product.

`tests/test_free_tier.py` enforces this: importing `engine`, `engine.cli`, `conversus.schemas`, or `conversus.plugins.base` must never trigger imports of `nashopt`, `jax`, `amplpy`, `highspy`, or any paid plugin module.

## The Arc: Monolith to Portable to Monetizable

| Wave | Duration | State Change | Key Deliverable |
|------|----------|-------------|----------------|
| Wave 1 | 4 hours | Monolith (complete) | 8-mode payoff functions, 3 spec amendments |
| Wave 2 (MIT-1) | 4 hours | Portable | `conversus/paths.py`, 7 file fixes, 31 split tests |
| Wave 3 | 2 hours | Monetizable | 4 package TOMLs, build script, free/paid boundary |

**Monolith** (pre-Wave 1): Everything works, but only from a source checkout. Half the modes cannot score themselves.

**Portable** (post-Wave 2): Every import boundary verified. Path resolution works in both source tree and wheel. 31 tests prove package independence. The engine can leave its original directory.

**Monetizable** (post-Wave 3): The free/paid boundary is drawn, tested, and enforced by the build system. The development workflow is unchanged -- same repo, same test command, same import paths. Packages are locally buildable via `scripts/build-packages.sh`; PyPI publication is a separate step that follows when the distribution channel is ready.

The critical insight was doing the split at build time, not at the source level. Physical extraction would have required rewriting imports, splitting the test suite, and coordinating multi-repo releases. Build-time splitting avoids all of this. The monolith stays monolithic where it matters (development) and splits where it matters (distribution).

Next up: execution provider abstraction (spec 042) to decouple the engine from Claude Code, the command center (spec 040) for a non-technical dashboard, and AMPL game-theoretic solver models (specs 043-044) to formalize what the heuristics approximate.
```

---

# Blog Post 2

---

```markdown
---
date: 2026-04-03
categories:
  - Engineering
  - Process
authors:
  - conversus-team
title: "Natural Language Game Theory Enforced with Optimization Modeling"
description: "AI agents are stochastic. The same prompt produces different outputs each run. Conversus stabilizes multi-agent deliberation output using game-theoretic payoff functions, equilibrium scoring, and a solver fallback from heuristics to formal optimization."
---

# Natural Language Game Theory Enforced with Optimization Modeling

Multi-agent deliberation has an output stability problem. Ask three LLM agents to review a spec today, you get one synthesis. Ask the same three agents with the same prompts tomorrow, you get a different synthesis. The deliberation content changes because language models are stochastic -- but the *quality* of the deliberation should be measurable, consistent, and tunable regardless of the specific words the agents chose.

That is the thesis behind the conversus scoring tier: formal game theory applied to natural language deliberation to produce deterministic quality metrics over stochastic output.

<!-- more -->

## The Problem: Stochastic Agents, Deterministic Decisions

When you run a conversus deliberation, each agent independently reviews a target document, cross-reviews the other agents' work, revises its position, and flags disputes. A synthesizer then produces a final verdict. This 5-phase pipeline is powerful -- it surfaces contradictions that a single reviewer would suppress -- but it produces *text*, not *numbers*.

Text is hard to compare across runs. Did this deliberation converge more than the last one? Is Agent A consistently contributing more than Agent B? Should you add a fourth agent or run an extra round? Without quantitative instrumentation, these questions reduce to "read both outputs and decide."

The scoring tier exists to answer them with math.

## Game Forms: Why Mode Matters

Each of conversus's 8 deliberation modes maps to a different game-theoretic structure. This is not a metaphor -- the mapping determines which payoff function computes the agent's score, which equilibrium concept defines optimality, and which optimization approach the solver uses.

| Mode | Game Form | Equilibrium Concept | What the Payoff Captures |
|------|-----------|-------------------|-----------------|
| cooperative | Cooperative game | Pareto optimality | Recommendations surviving synthesis |
| winner-take-all | Zero-sum | Nash equilibrium | Binary win/loss |
| prisoner's dilemma | Non-cooperative | Nash equilibrium | Territory held minus overreach penalty |
| red-blue | Asymmetric | Minimax | Severity-weighted attack/mitigation |
| negotiation | Bayesian | Bayesian Nash | ZOPA coverage times party satisfaction |
| resource-allocation | Coalitional (Shapley) | Core stability | Utilization efficiency minus inequality |
| fair-division | Coalitional | Envy-freeness | Proportionality minus normalized envy |
| mechanism-design | Mechanism design | Incentive compatibility | Social welfare minus gaming vulnerability |

The mode selection is not decorative. When you choose `mode: prisoners-dilemma`, you are telling the scoring system to measure territory claims, deferral costs, and overreach penalties. When you choose `mode: cooperative`, you are telling it to measure surviving recommendations. The payoff function changes. The equilibrium concept changes. The downstream solver formulation changes.

## The Solver Tiers

Conversus provides three solver tiers that form a fallback chain. Each tier provides a different tradeoff between speed, precision, and infrastructure requirements.

### Tier 1: Heuristic Payoffs (default)

Every mode has a hand-written payoff function that takes extracted feature vectors and returns a `(payoff, best_response_payoff)` tuple. These are deterministic, fast (microseconds), and require no external dependencies.

The heuristic for prisoner's dilemma mode illustrates the pattern:

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

### Tier 2: AMPL/HiGHS (constrained optimization)

For users who need optimal configurations under budget constraints, conversus integrates with AMPL through the amplpy binding and HiGHS as the open-source LP/MIP solver.

The AMPL tier uses the heuristic payoff functions as objective functions within a constrained optimization framework. Instead of computing a point estimate, it solves for the optimal deliberation configuration:

- **Decision variables**: number of rounds, number of agents, iterations per cross-review phase
- **Objective**: maximize aggregate equilibrium quality
- **Constraints**: total LLM calls <= budget, minimum mode-specific thresholds

This matters because the heuristic alone cannot answer "given a $50 API budget, should I run 3 agents for 2 rounds or 5 agents for 1 round?" That is a constrained optimization problem.

The AMPL infrastructure and config optimizer exist today. Per-mode AMPL model templates -- formalizing each game form's specific optimization structure -- are specified in specs 043 and 044 and will ship in a future wave. The current AMPL tier handles configuration optimization; the upcoming templates will add mode-aware objective functions.

### Tier 3: nashopt/JAX (game-theoretic equilibrium)

For users who need game-theoretic proofs, conversus integrates with nashopt -- a JAX-based Nash equilibrium solver.

Where the heuristic estimates distance from equilibrium and AMPL optimizes configuration, nashopt computes the actual Nash equilibrium of the game defined by the payoff matrix. It answers: "given these agents with these payoff functions, what is the equilibrium strategy profile?"

The practical value: if the agents' actual behavior matches the computed Nash equilibrium, the deliberation is provably stable. No agent has an incentive to unilaterally deviate.

### The Fallback Chain

```
Tier 1 (heuristic) -> always available, default
Tier 2 (AMPL)      -> pip install conversus-solvers[ampl]
Tier 3 (nashopt)   -> pip install conversus-solvers[nashopt]
```

Each tier enriches the previous one. Heuristics give you scores. AMPL gives you optimal configurations. nashopt gives you equilibrium proofs. A user at Tier 1 still gets useful output -- the scoring is deterministic and comparable across runs.

The PluginResult reports which solver was used: `"none"` (free tier), `"heuristic"`, `"ampl-highs"`, or `"nashopt"`. Downstream consumers -- including the Kalman convergence predictor -- adapt their confidence bounds based on solver fidelity.

## Tunability: Parameters as the Interface

The key design decision in the payoff functions is that they expose parameters rather than hard-coded weights.

### gamma: the overreach penalty

In prisoner's dilemma mode, `gamma` controls the cost of unrebutted overreach flags:

```
payoff = territory - gamma * overreach_penalty
```

At `gamma=0.0`, overreach is free -- agents can claim anything without penalty. This produces aggressive, expansive reviews.

At `gamma=2.0`, overreach is expensive -- a single unrebutted overreach flag costs twice as much as a territory claim is worth. This produces conservative, well-evidenced reviews.

The default `gamma=1.0` balances expansion against accountability. But the right value depends on the domain. For a security review (red-blue mode), you might want aggressive red-team agents (`gamma=0.5`). For a compliance review, you want conservative, evidence-heavy agents (`gamma=2.0`).

Future specs (043, 044) will expand the parameter surface -- adding threshold controls for fair-division envy tolerance, weighting for cooperative surviving-count valuation, and severity scaling for red-blue attack scoring. The pattern is established: each parameter is a dial that controls agent incentives without changing prompts.

This is the fundamental advantage of the optimization modeling approach. Prompt engineering is qualitative -- you describe what you want in natural language and hope the model interprets it correctly. Parameter tuning is quantitative -- you set `gamma=1.5` and the scoring system mechanically adjusts what behavior is rewarded. Both are useful. But only the quantitative approach is reproducible.

## How Game Forms Connect to Solvers

Each game form has a natural optimization formulation, and the payoff function is the bridge. Rather than exhaustively mapping all eight, here is the pattern through one example.

**Cooperative games** map to Pareto optimization. The cooperative payoff function measures how many of each agent's recommendations survived synthesis. A Pareto-optimal outcome is one where you cannot increase any agent's surviving count without decreasing another's. At the heuristic tier, you get the surviving-count score. At the AMPL tier (once per-mode templates ship in specs 043-044), the solver will verify Pareto optimality under budget constraints. At the nashopt tier, you get the full cooperative equilibrium.

The same pattern holds across all modes:

| Game Form | Optimization Formulation | Heuristic Provides | AMPL Will Provide | nashopt Provides |
|-----------|-------------------------|-------------------|-------------------|-----------------|
| Cooperative | Pareto optimization | Surviving count score | Budget-constrained Pareto check | Cooperative equilibrium |
| Zero-sum (WTA) | Minimax | Win/loss score | Optimal agent allocation | Minimax equilibrium |
| Non-cooperative (PD) | Nash equilibrium | Territory/overreach score | Config optimization | Mixed-strategy Nash |
| Bayesian (negotiation) | Bayesian Nash | ZOPA/satisfaction score | Type-aware optimization | Bayesian Nash equilibrium |
| Coalitional | Core stability | Efficiency/fairness score | Shapley-based allocation | Core membership proof |
| Mechanism design | Incentive compatibility | Welfare/gaming score | Truthfulness verification | IC equilibrium |

Each mode's payoff function encodes the game form's utility structure. The solver tiers compute progressively stronger solution concepts over that structure. The user selects a mode based on their deliberation's dynamics, and the solver stack follows from that selection.

## What This Means for Users

If you are using the free tier, none of this matters. Your deliberations run the full 5-phase pipeline and produce a synthesis. The output is useful on its own.

If you install `conversus-solvers`, you get a number next to each agent name: their equilibrium score. You get a convergence prediction: how many more rounds until positions stabilize. You get a configuration recommendation: whether to add agents, increase iterations, or extend rounds.

If you install the AMPL or nashopt extras, you get constrained optimization and equilibrium proofs. The same heuristic payoff functions that produce a quick score also serve as the objective functions that the solvers optimize.

The three tiers share one interface: the payoff function. Everything else is solver selection.

## Applying This to Your Own System

The pattern behind conversus's scoring tier is not conversus-specific. If you are building any multi-agent system and getting inconsistent results, the steps are:

1. **Define what "good" means quantitatively.** For your specific task, what measurable properties of the output indicate quality? Coverage, agreement, severity of findings, ratio of justified to unjustified claims.
2. **Write a pure scoring function.** It takes extracted features and returns a number. No LLM calls. Same features, same score. This is your ground truth for comparing runs.
3. **Compute best-response.** For each agent, calculate what they could have scored if they played optimally given the other agents' strategies. The gap between actual and best-response is your equilibrium quality measure.
4. **Track across rounds.** Feed scores into a filter (exponential moving average works; Kalman is better). When the score stabilizes, you have converged. When it diverges, stop early and save the tokens.

The free tier is the deliberation engine. The paid tier is the instrumentation. The optimization models are what make the instrumentation trustworthy. Build the scoring function first -- everything else follows.
```
