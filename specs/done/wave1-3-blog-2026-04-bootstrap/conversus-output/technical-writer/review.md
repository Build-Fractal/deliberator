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
title: "From Heuristics to pip install — How We Got Conversus Ready for Users"
description: "Wave 1 added 8-mode payoffs, Wave 2 fixed every path resolution bug blocking pip install, and Wave 3 split a monolith into free and paid tiers at build time — without moving a single file. Here's how and why."
---

# From Heuristics to pip install — How We Got Conversus Ready for Users

Three waves of work over two days turned conversus from a monolith that only ran from a git checkout into something you can `pip install`. Wave 1 completed the 8-mode payoff functions. Wave 2 killed every `Path(__file__).parent` traversal that assumed a source tree layout. Wave 3 split one source tree into multiple wheels with a free/paid boundary — at build time, without moving files.

This post covers the technical decisions behind each wave and why the alternatives were worse.

<!-- more -->

## Wave 1: Completing the Payoff Functions (specs 038, 039)

Conversus shipped with payoff functions for four modes: cooperative, winner-take-all, prisoner's dilemma, and red-blue. Spec 028 had added four new modes — negotiation, resource-allocation, fair-division, and mechanism-design — but the EquilibriumScorer had no payoff logic for them. Scoring a deliberation in any new mode would fail.

Spec 039 added four new payoff functions, each returning the same `(payoff, best_response_payoff)` tuple as the original four:

| Mode | Payoff Formula | Game Form |
|------|---------------|-----------|
| negotiation | `zopa_coverage * party_satisfaction` | Bayesian |
| resource-allocation | `utilization_efficiency - allocation_inequality` | Coalitional (Shapley) |
| fair-division | `proportionality_score - (envy_count / (N-1))` | Coalitional |
| mechanism-design | `social_welfare_contribution - (gaming_vulns / total_vulns)` | Mechanism design |

The `compute_payoff()` dispatcher now routes all 8 modes. This was a prerequisite for everything downstream — the solvers package has no value if it can only score half the modes.

Spec 038 ran in parallel, resolving three spec-level inconsistencies in the solver documentation. The WTA matrix shape discrepancy between the spec table and the nashopt API was resolved. The cooperative diagonal semantics issue — mixing `surviving_count` with `agreement_matrix` — was documented as heuristic-only rather than papered over with a bad fix. These were spec amendments, not code changes, but they cleared ambiguity that would have blocked Wave 3's package split.

## Wave 2: Killing Path(__file__).parent (MIT-1)

Before you can ship a pip package, every file access in the codebase must work when the code is installed into a `site-packages` directory — not just when it runs from a source checkout. We called this prerequisite "MIT-1" (Minimum Independent Test, iteration 1).

The problem was widespread. Seven files across the engine, linter, schemas, and domains used `Path(__file__).parent` traversal to find templates, presets, and scaffolds at the project root. This works in development because `engine/phases.py` and `templates/cooperative/review.md` are siblings in the directory tree. It breaks completely when pip installs `engine/` into `site-packages/engine/` — the templates aren't there.

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
        target_name = parts[0]
        current = Path(__file__).resolve().parent
        for _ in range(5):
            candidate = current / Path(*parts)
            if candidate.exists():
                return candidate
            current = current.parent

    raise FileNotFoundError(...)
```

`importlib.resources.files()` is the standard library mechanism for locating data files inside installed packages. When you `pip install conversus`, Hatch's `force-include` directive copies `templates/`, `presets/`, and `schema/` into the wheel under `conversus/`. The `importlib.resources` call resolves them there. In development, the files live at the project root, so the fallback walks up the directory tree.

Why not just use `pkg_resources` or `__file__` with a fixed offset? `pkg_resources` is deprecated. A fixed `__file__` offset is fragile — it breaks if the directory structure ever changes, and it's the exact pattern we were removing. `importlib.resources` is the blessed approach since Python 3.9, and it handles zip-imported packages, editable installs, and namespace packages correctly.

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

MIT-1 also discovered that the optimizer plugin imported `estimate_cost` from `engine.cost`. That's a cross-package dependency — the paid solvers package would require the free engine package at the Python import level, which is fine, but the engine would also need to be importable without the optimizer, which means the optimizer can't reach back into engine internals.

The fix was to duplicate `estimate_cost` into the optimizer module. It's a small, pure function. Duplication here is better than the coupling.

### 31 tests prove independence

`tests/test_package_split.py` verifies that each future pip package can import independently. It snapshots `sys.modules` before and after importing each module, then asserts that no forbidden cross-package modules appeared. For example, importing `conversus.schemas` must never trigger `conversus.plugins` or `conversus.domains`. Importing `conversus.plugins.nashopt` must never trigger `engine` or `linter`.

These 31 tests are the proof that physical package extraction is possible whenever the business needs it. They run in the existing `uv run pytest` suite — the development workflow is unchanged.

## Wave 3: Build-Time Package Splitting (spec 032)

The goal was `pip install conversus`. The question was how to get there.

### Why build-time splitting, not physical extraction

The obvious approach is to move files into separate directories, give each directory its own `pyproject.toml`, and publish independent packages. This is what most open-source projects do when they split.

We rejected it for three reasons:

1. **Moving files breaks imports.** Every `from conversus.plugins.nashopt import ...` becomes `from conversus_solvers.plugins.nashopt import ...` or whatever the new package name is. Every test file, every doc example, every config reference changes.
2. **It splits the test suite.** You can no longer run `uv run pytest` to test everything. Each package needs its own test infrastructure, CI config, and fixture setup.
3. **Multi-repo coordination overhead.** A change that touches both the engine and a solver now requires coordinated PRs across repos.

Build-time splitting avoids all of this. The source code stays as a single monolith. The build system produces multiple wheels from the same tree. A `packages/` directory contains one TOML config per wheel:

```
packages/
  core.toml       # pip install conversus
  solvers.toml    # pip install conversus-solvers
  scenarios.toml  # pip install conversus-scenarios
  swe.toml        # pip install conversus-swe
```

Each TOML file tells Hatch which source directories to include or exclude. `core.toml` excludes `conversus/plugins/nashopt/**` and `conversus/plugins/optimizer/**`. `solvers.toml` only includes those directories. Same source tree, different slices.

The build script iterates over `packages/*.toml` and runs `hatch build` for each. Four wheels come out. Development workflow is unchanged — `uv run pytest` still runs everything from the source tree.

### Why not submodules yet

Build-time splitting does not provide access control. Anyone who can see the source tree can build all packages. For monetization, the paid source code needs to live in private repos — which means eventual extraction into git submodules.

But MIT-1 already proved zero coupling between packages. Extraction to submodules is mechanical — just `git mv` the files and update the TOML configs. We shipped build-time splitting first because it unblocks users immediately. Submodule extraction follows when the business needs private repos.

Build-time splitting is also fully reversible: delete the `packages/` directory and you're back to a monolith.

## Wave 3b: The Free/Paid Boundary (spec 033)

With packages split, the question becomes: what goes where?

### The principle: deliberation is free, scoring is paid

The free tier (`pip install conversus`) ships the complete deliberation engine. All 8 modes. All 5-6 phases. Templates, presets, CLI, MCP server, web UI, schema validation, linter. Agents argue, cross-review, revise, and synthesize. You get the full pipeline.

The paid tier (`pip install conversus-solvers`) adds the quantitative layer. Heuristic payoff functions. Equilibrium scoring. Kalman convergence prediction. Config optimization. nashopt integration. AMPL integration.

### Why heuristics are paid

This is the decision that generates the most pushback. The payoff functions are "just math" — weighted sums and ratios over extracted features. Why not give them away?

Four reasons:

1. **Comparability.** Without scoring, a deliberation produces reviews, cross-reviews, and a synthesis. With scoring, you know Agent A's position is 0.85 and Agent B's is 0.62. That number is what makes output comparable across runs.
2. **Consistency.** The same features always produce the same score. This is what makes conversus output deterministic — the deliberation itself is stochastic (LLM-generated), but the scoring is not.
3. **Tunability.** Parameters like `gamma` (the overreach penalty in prisoner's dilemma mode) give you a quantitative dial on agent behavior. Without the scoring tier, tuning means changing prompts.
4. **Value architecture.** If heuristics are free, the paid tier is "better heuristics" — a weak value proposition. If heuristics are paid, the paid tier is the entire quantitative layer — everything that makes agent output measurable. nashopt, AMPL, and Kalman build on the same foundation.

### Feature gating: detection, not enforcement

The gating mechanism in v1 is trivial:

```python
try:
    from conversus.plugins.nashopt import EquilibriumScorer
    SOLVERS_AVAILABLE = True
except ImportError:
    SOLVERS_AVAILABLE = False
```

No license keys. No nag screens. No degraded output. If `conversus-solvers` is installed, its plugins load. If not, deliberation completes normally without scoring. The paid tier is additive — the free tier is never a crippled version of the full product.

`tests/test_free_tier.py` enforces this: importing `engine`, `engine.cli`, `conversus.schemas`, or `conversus.plugins.base` must never trigger imports of `nashopt`, `jax`, `amplpy`, `highspy`, or any paid plugin module.

## What Shipped

| Wave | Duration | Key Deliverable |
|------|----------|----------------|
| Wave 1 | 4 hours | 8-mode payoff functions, 3 spec amendments |
| Wave 2 (MIT-1) | 4 hours | `conversus/paths.py`, 7 file fixes, 31 split tests |
| Wave 3 | 2 hours | 4 package TOMLs, build script, `core.toml` + `solvers.toml` |
| Wave 3b | 2 hours | Free/paid feature matrix, gating logic, `test_free_tier.py` |

The critical path was 12 hours across 2 days. `pip install conversus` now works. The development workflow is unchanged. Package extraction to private repos is mechanical whenever monetization requires it.

Next up: execution provider abstraction (spec 042) to decouple the engine from Claude Code, and the AMPL game-theoretic solvers (spec 043) to formalize what the heuristics approximate.
```

---

# Blog Post 2

---

```markdown
---
date: 2026-04-03
categories:
  - Engineering
  - Architecture
authors:
  - conversus-team
title: "Natural Language Game Theory Enforced with Optimization Modeling"
description: "AI agents are stochastic. The same prompt produces different outputs each run. Conversus stabilizes multi-agent deliberation output using game-theoretic payoff functions, equilibrium scoring, and a three-tier solver fallback from heuristics to AMPL to nashopt."
---

# Natural Language Game Theory Enforced with Optimization Modeling

Multi-agent deliberation has an output stability problem. Ask three LLM agents to review a spec today, you get one synthesis. Ask the same three agents with the same prompts tomorrow, you get a different synthesis. The deliberation content changes because language models are stochastic — but the *quality* of the deliberation should be measurable, consistent, and tunable regardless of the specific words the agents chose.

That is the thesis behind the conversus scoring tier: formal game theory applied to natural language deliberation to produce deterministic quality metrics over stochastic output.

<!-- more -->

## The Problem: Stochastic Agents, Deterministic Decisions

When you run a conversus deliberation, each agent independently reviews a target document, cross-reviews the other agents' work, revises its position, and flags disputes. A synthesizer then produces a final verdict. This 5-phase pipeline is powerful — it surfaces contradictions that a single reviewer would suppress — but it produces *text*, not *numbers*.

Text is hard to compare across runs. Did this deliberation converge more than the last one? Is Agent A consistently contributing more than Agent B? Should you add a fourth agent or run an extra round? Without quantitative instrumentation, these questions reduce to "read both outputs and decide."

The scoring tier exists to answer them with math.

## Game Forms: Why Mode Matters

Each of conversus's 8 deliberation modes maps to a different game-theoretic structure. This isn't a metaphor — the mapping determines which payoff function computes the agent's score, which equilibrium concept defines optimality, and which optimization problem the solver formulates.

| Mode | Game Form | Equilibrium Concept | Payoff Captures |
|------|-----------|-------------------|-----------------|
| cooperative | Cooperative game | Pareto optimality | How many recommendations survived synthesis |
| winner-take-all | Zero-sum | Nash equilibrium | Binary: did you win? |
| prisoner's dilemma | Non-cooperative | Nash equilibrium | Territory held minus overreach penalty |
| red-blue | Asymmetric | Minimax | Severity-weighted attack success or mitigation |
| negotiation | Bayesian | Bayesian Nash | ZOPA coverage times party satisfaction |
| resource-allocation | Coalitional (Shapley) | Core stability | Utilization efficiency minus allocation inequality |
| fair-division | Coalitional | Envy-freeness | Proportionality minus normalized envy count |
| mechanism-design | Mechanism design | Incentive compatibility | Social welfare contribution minus gaming vulnerability |

The mode selection is not decorative. When you choose `mode: prisoners-dilemma`, you're telling the scoring system to measure territory claims, deferral costs, and overreach penalties. When you choose `mode: cooperative`, you're telling it to measure surviving recommendations. The payoff function changes. The equilibrium concept changes. The optimization model changes.

## The Three-Tier Solver Fallback

Conversus implements three solver backends that form a fallback chain. Each tier provides a different tradeoff between speed, precision, and infrastructure requirements.

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

`territory` counts what the agent holds. `overreach_penalty` counts unrebutted flags from cross-review. `gamma` controls how harshly overreach is punished. The best-response estimate assumes maximum territory with zero penalty — the theoretical optimum an agent could achieve by being perfectly honest and well-evidenced.

The EquilibriumScorer uses the ratio `payoff / best_response_payoff` to compute a [0.0, 1.0] equilibrium quality score. An agent at best response scores 1.0. An agent far from best response scores lower. The aggregate across agents gives a round-level equilibrium quality metric.

The heuristic is an *approximation* of the equilibrium. It doesn't prove the agent is at Nash equilibrium — it estimates the distance from it. This is sufficient for most use cases and is where 90% of users will stay.

### Tier 2: AMPL/HiGHS (exact optimization)

For users who need provably optimal configurations, conversus integrates with AMPL through the amplpy binding and HiGHS as the open-source LP/MIP solver.

The AMPL tier formalizes the heuristic as an optimization problem. Instead of computing a point estimate of the payoff, it solves for the optimal agent configuration given budget constraints:

- **Decision variables**: number of rounds, number of agents, iterations per cross-review phase
- **Objective**: maximize aggregate equilibrium quality
- **Constraints**: total LLM calls <= budget, minimum mode-specific thresholds

The heuristic payoff function defines *what* to optimize. AMPL defines *how* to optimize it. The heuristic is the objective function; AMPL is the solver.

This matters because the heuristic alone can't answer "given a $50 API budget, should I run 3 agents for 2 rounds or 5 agents for 1 round?" That's a constrained optimization problem, and AMPL solves it exactly.

### Tier 3: nashopt/JAX (game-theoretic equilibrium)

For users who need game-theoretic proofs, conversus integrates with nashopt — a JAX-based Nash equilibrium solver.

Where the heuristic estimates distance from equilibrium and AMPL optimizes configuration, nashopt computes the actual Nash equilibrium of the game defined by the payoff matrix. It answers: "given these agents with these payoff functions, what is the equilibrium strategy profile?"

The payoff matrix is constructed from the per-agent payoff functions. For an N-agent game, the matrix is N-dimensional — each agent's payoff depends on all other agents' strategies. nashopt finds the mixed-strategy Nash equilibrium using support enumeration and verified through JAX automatic differentiation.

The practical value: if the agents' actual behavior matches the computed Nash equilibrium, the deliberation is provably stable. No agent has an incentive to unilaterally deviate. The output is as good as it can be given the mode and feature structure.

### The Fallback Chain

```
Tier 1 (heuristic) -> always available, default
Tier 2 (AMPL)      -> pip install conversus-solvers[ampl]
Tier 3 (nashopt)   -> pip install conversus-solvers[nashopt]
```

Each tier enriches the previous one. Heuristics give you scores. AMPL gives you optimal configurations. nashopt gives you equilibrium proofs. A user at Tier 1 still gets useful output — the scoring is deterministic and comparable across runs. A user at Tier 3 gets formal guarantees.

The PluginResult reports which solver was used: `"none"` (free tier), `"heuristic"`, `"ampl-highs"`, or `"nashopt"`. Downstream consumers — including the Kalman convergence predictor — adapt their confidence bounds based on solver fidelity.

## Tunability: Parameters as the Interface

The key design decision in the payoff functions is that they expose parameters rather than hard-coded weights. This is what makes the scoring tier useful beyond its defaults.

### gamma: the overreach penalty

In prisoner's dilemma mode, `gamma` controls the cost of unrebutted overreach flags:

```
payoff = territory - gamma * overreach_penalty
```

At `gamma=0.0`, overreach is free — agents can claim anything without penalty. This produces aggressive, expansive reviews where every agent claims maximum territory.

At `gamma=2.0`, overreach is expensive — a single unrebutted overreach flag costs twice as much as a territory claim is worth. This produces conservative, well-evidenced reviews where agents only claim what they can defend.

The default `gamma=1.0` balances expansion against accountability. But the right value depends on the domain. For a security review (red-blue mode), you might want aggressive red-team agents (`gamma=0.5`). For a compliance review, you want conservative, evidence-heavy agents (`gamma=2.0`).

### Mode-specific parameters

Each payoff function can accept mode-specific keyword arguments via the `compute_payoff()` dispatcher:

```python
def compute_payoff(mode, agent_name, features, **kwargs):
    fn = PAYOFF_FUNCTIONS.get(mode)
    if mode == "prisoners-dilemma":
        gamma = kwargs.get("gamma", 1.0)
        return fn(agent_name, features, gamma=gamma)
    return fn(agent_name, features)
```

Future specs (043, 044) will expand the parameter surface — adding threshold controls for fair-division envy tolerance, weighting for cooperative surviving-count valuation, and severity scaling for red-blue attack scoring. The pattern is established: each parameter is a dial that controls agent incentives without changing prompts.

This is the fundamental advantage of the optimization modeling approach. Prompt engineering is qualitative — you describe what you want in natural language and hope the model interprets it correctly. Parameter tuning is quantitative — you set `gamma=1.5` and the scoring system mechanically adjusts what behavior is rewarded. Both are useful. But only the quantitative approach is reproducible.

## How Game Forms Map to Optimization Problems

The mapping from game form to optimization problem is not arbitrary. Each game form has a natural optimization formulation, and the payoff function is the bridge.

**Cooperative games** map to Pareto optimization. The objective is to maximize the aggregate payoff without making any agent worse off. The cooperative payoff function (`surviving_count`) measures how many of each agent's recommendations survive synthesis. A Pareto-optimal outcome is one where you can't increase any agent's surviving count without decreasing another's.

**Zero-sum games** (WTA) map to minimax problems. The objective is to find the strategy profile where the winning agent's advantage is maximized. The WTA payoff function returns 1 for the winner and 0 for everyone else — the optimization problem is to determine whether the winner's victory is stable.

**Non-cooperative games** (PD) map to Nash equilibrium computation. The objective is to find the strategy profile where no agent can unilaterally improve their payoff. The PD payoff function — territory minus penalized overreach — defines the utility surface. The Nash equilibrium is the point on that surface where all agents are simultaneously at best response.

**Bayesian games** (negotiation) map to Bayesian Nash equilibrium. Agents have private information (their reservation prices and satisfaction thresholds), and the equilibrium must hold in expectation over the type distribution. The negotiation payoff function factors in ZOPA coverage and per-party satisfaction — both of which depend on information the other agents don't have.

**Coalitional games** (resource-allocation, fair-division) map to core stability and envy-freeness checks. The optimization problem is to find allocations in the core — where no coalition of agents can do better by breaking away. The Shapley value provides the reference allocation.

**Mechanism design** maps to incentive compatibility verification. The optimization problem is to check whether agents can improve their payoff by misreporting their true preferences. The mechanism-design payoff function penalizes gaming vulnerabilities — points where truthful reporting is not optimal.

Each mode's payoff function encodes the game form's utility structure. The solver tiers compute progressively stronger solution concepts over that structure. The user selects a mode based on their deliberation's dynamics, and the entire optimization stack follows from that selection.

## What This Means for Users

If you're using the free tier, none of this matters. Your deliberations run the full 5-phase pipeline and produce a synthesis. The output is useful on its own.

If you install `conversus-solvers`, you get a number next to each agent name: their equilibrium score. You get a convergence prediction: how many more rounds until positions stabilize. You get a configuration recommendation: whether to add agents, increase iterations, or extend rounds.

If you install the AMPL or nashopt extras, you get formal optimization and equilibrium proofs. The same heuristic payoff functions that produce a quick score also define the objective functions that the solvers optimize exactly.

The three tiers share one interface: the payoff function. Everything else is solver selection. This is why the architecture works — you can start with heuristics, validate your workflow, and upgrade to exact solvers when the stakes justify it.

The free tier is the deliberation engine. The paid tier is the instrumentation. The optimization models are what make the instrumentation trustworthy.
```
