# POST 1

---
date: 2026-04-03
categories:
  - Engineering
  - Release
authors:
  - conversus-team
title: "From Heuristics to pip install: How We Made a Monolith Portable in Three Waves"
description: "We started with 41 specs, a framework welded to Claude Code, and 8 modes that couldn't score themselves. Three waves later, conversus is pip-installable, the free/paid line is drawn, and the monolith never moved a single file."
---

# From Heuristics to pip install: How We Made a Monolith Portable in Three Waves

Forty-one specs. A deliberation engine that runs 8 competition modes across a 5-phase pipeline with dispute detection, stagnation tracking, and multi-round convergence. Templates, presets, schemas, a linter, an MCP server, a web UI. All of it hardwired to a source tree that assumed it would always run inside Claude Code.

We needed to turn this into something you could `pip install`. And we needed to do it without breaking the development workflow, without moving files into separate repos, and without losing the ability to `uv run pytest` and have everything pass.

This is the story of how three waves of work -- executed over 48 hours -- took conversus from monolith to portable to monetizable.

<!-- more -->

## The Starting Point: What 41 Specs Built

By spec 031, conversus was a complete deliberation framework. Eight modes spanning cooperative consensus to winner-take-all elimination to red-blue adversarial review. A 55-agent documentation review had just shipped 3 code bug fixes and 28 documentation improvements. The engine worked.

But it had two problems that blocked every user who didn't already have the source tree on their machine.

**Problem 1: The scoring gap.** Four of the eight modes -- negotiation, resource-allocation, fair-division, mechanism-design -- had no payoff functions. The EquilibriumScorer could compute Nash equilibrium quality for the original four modes but returned nothing for the new ones. Half the framework was invisible to quantitative analysis.

**Problem 2: The path problem.** Every template lookup, every preset resolution, every scaffold directory call used `Path(__file__).parent` and walked up the directory tree. This works when you clone the repo. It fails catastrophically inside a pip-installed wheel, where `templates/` lives inside the package, not alongside it.

Neither problem was visible in development. Both would be fatal in production.

## Wave 1: Making the Math Work (Specs 038 + 039)

Wave 1 ran two specs in parallel -- solver equilibrium fixes (038) and new mode payoffs (039). The goal was straightforward: every mode must be scorable.

Spec 038 was documentation surgery. The matrix shape table in spec 021 said WTA payoffs are N x 1, but the nashopt API expected N x N. The code matched the table, not the API. The cooperative payoff mixed `surviving_count` on the diagonal with `agreement_matrix` off-diagonal, producing uninterpretable equilibria. Three spec amendments, zero code changes.

Spec 039 was the real work: four new payoff functions that gave the EquilibriumScorer coverage across all eight modes.

The design decision that matters: every payoff function returns `(payoff, best_response_payoff)`. When `payoff == best_response_payoff`, the agent is at Nash equilibrium. This two-value interface is what makes the scoring tier valuable -- it doesn't just tell you a number, it tells you whether the number could be better.

Take the negotiation payoff. It computes `zopa_coverage * party_satisfaction`. Best response is 1.0 -- full ZOPA coverage with full satisfaction. The gap between actual and best-response payoff is the quantitative measure of how far the negotiation drifted from optimal.

Or the prisoners-dilemma payoff, which computes `territory_held - gamma * overreach_penalty`. That `gamma` parameter is a tuning knob. Set it high and agents are punished harshly for overreach. Set it low and they get away with more. This is what we mean by "deterministic tuning" -- same features, same gamma, same score every time. The payoff function is pure. No randomness, no prompt sensitivity, no model variance.

After Wave 1, all eight modes had payoff functions, all returning the same `(payoff, best_response_payoff)` interface, all testable with representative feature data.

## Wave 2: Five Parallel Agents Find Eight Breaks

Wave 2 was the session that changed the project's trajectory.

We called it MIT-1 -- the minimum import test. Five agents ran in parallel, each tracing the import graph of a different future package. Their job: find every place where importing a module pulled in something it shouldn't.

They found eight path breaks.

Seven files used `Path(__file__).parent` traversal to find templates, presets, or schemas. In a source tree, this works because the directory structure is predictable. In a wheel, the traversal points to the wrong directory -- or to a directory that doesn't exist at all. The engine, the linter, the schema loader, the domain framework -- all broken.

The fix was `conversus/paths.py`, a 60-line module that resolves data file paths using `importlib.resources` as the primary strategy and `Path(__file__)` traversal as a fallback for development. The key function is `resolve_package_path`:

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

The eighth break was a cross-package import violation: the optimizer module imported `estimate_cost` from `engine.cost`. That single import meant `conversus-solvers` would drag in the entire engine -- defeating the point of splitting. The fix was duplicating the function into the optimizer's own module. Not elegant, but it eliminated the coupling.

By the end of Wave 2, we had 31 package-split tests verifying that each future package's import boundary held. Schemas import nothing. The plugin framework imports only schemas. Premium packages don't import the engine or each other. Every test passed.

## Wave 3: Build-Time Splitting (Spec 032)

Here is the decision that made everything possible: **the source code stays as a single monolith. The build system produces multiple wheels.**

No file moves. No import rewrites. No multi-repo coordination. One `pyproject.toml` for development (`uv run pytest` runs everything), and a `packages/` directory with per-package build configs that hatch uses to produce separate wheels.

The core package excludes premium code:

```toml
# packages/core.toml
[tool.hatch.build.targets.wheel]
packages = ["engine", "linter", "web", "conversus"]
exclude = [
    "conversus/plugins/nashopt/**",
    "conversus/plugins/optimizer/**",
    "conversus/plugins/scenarios/**",
    "conversus/domains/implementations/**",
]

[tool.hatch.build.targets.wheel.force-include]
"schema" = "conversus/schema"
"templates" = "conversus/templates"
"presets" = "conversus/presets"
```

The solvers package includes only premium code:

```toml
# packages/solvers.toml
[tool.hatch.build.targets.wheel]
packages = ["conversus"]
only-include = [
    "conversus/plugins/nashopt",
    "conversus/plugins/optimizer",
]
```

Build-time splitting is reversible. Delete the `packages/` directory and you're back to a monolith. No code changes, no import changes, no test changes.

The `force-include` lines solve the path problem from Wave 2. Templates, presets, and schemas get bundled inside the wheel. `importlib.resources` finds them at runtime. The 60-line `paths.py` module closes the loop.

## Wave 3b: Drawing the Line (Spec 033)

Splitting the package is a mechanical problem. Deciding where to split is a product decision.

The principle we landed on: **deliberation is free. Scoring is paid.**

`pip install conversus` gives you the complete engine. Eight modes, five-phase pipeline, multi-round deliberation, templates, presets, CLI, MCP server, web UI. Agents argue, cross-review, revise, and synthesize. You get the full output.

`pip install conversus-solvers` adds the quantitative layer. Equilibrium scoring, convergence prediction, config optimization, and all eight payoff functions. These are the features that make agent output consistent, tunable, and reproducible.

The gating mechanism is deliberately simple: try/except on import.

```python
try:
    from conversus.plugins.nashopt import EquilibriumScorer
    SOLVERS_AVAILABLE = True
except ImportError:
    SOLVERS_AVAILABLE = False
```

No license keys. No nag screens. No degraded output. Installed means available. Not installed means silently absent. The free tier is not a crippled version of the paid tier. It is a complete product that the paid tier extends.

The test suite enforces this boundary. `test_free_tier.py` verifies that importing the engine, CLI, schemas, and plugin framework never triggers imports of nashopt, jax, amplpy, or highspy. If a developer accidentally adds a paid dependency to the free path, the test fails.

## The Arc: Monolith to Portable to Monetizable

Three waves, 48 hours, and the framework went through three distinct states:

**Monolith** (pre-Wave 1): Everything works, but only if you have the source tree. Half the modes can't score themselves. The engine is welded to the file system layout.

**Portable** (post-Wave 2): Every import boundary verified. Path resolution works in both source tree and wheel. 31 tests prove package independence. The engine can leave its original directory.

**Monetizable** (post-Wave 3): `pip install conversus` is a real thing. The free/paid boundary is drawn, tested, and enforced by the build system. The development workflow is unchanged -- same repo, same test command, same import paths.

The critical insight was doing the split at build time, not at the source level. Physical extraction -- moving files into separate repos -- would have required rewriting imports, splitting the test suite, and coordinating multi-repo releases. Build-time splitting avoids all of this. The monolith stays monolithic where it matters (development) and splits where it matters (distribution).

One more thing. MIT-1 proved zero coupling between packages. That means extraction to separate repos is now mechanical whenever monetization requires access control for private packages. Build-time splitting ships first. Physical extraction follows when needed, not before.

The next wave is platform work: execution providers (decouple from Claude Code), the command center (non-technical dashboard), and AMPL game-theoretic solvers (formal optimization models). But those are features on top of a framework that now ships as a package. The hard part is done.

---

# POST 2

---
date: 2026-04-03
categories:
  - Engineering
  - AI
authors:
  - conversus-team
title: "Why Your AI Agents Give Different Answers Every Time (And How to Fix It)"
description: "AI agents are non-deterministic by nature. Every run produces different output. Optimization models give you the tuning knobs to make that output consistent, comparable, and reproducible."
---

# Why Your AI Agents Give Different Answers Every Time (And How to Fix It)

You run three AI agents on the same code review. Agent A says the auth module needs a rewrite. Agent B says it's fine with minor patches. Agent C focuses entirely on test coverage.

You run it again. Agent A now agrees with Agent B. Agent C has a new concern about error handling.

Same input. Same prompts. Same model. Different answers. Every time.

This is the fundamental problem of multi-agent AI systems: **agents are non-deterministic, and without a scoring layer, you have no way to tell whether run #1 or run #2 produced the better result.**

<!-- more -->

## The Consistency Problem Is Not a Bug

LLMs are probabilistic. Temperature, sampling, context window positioning -- all of these introduce variance. When you chain multiple agents together, the variance compounds. Three agents with moderate variance each can produce wildly different collective outputs across runs.

Most teams try to solve this by tuning prompts. They add "be consistent" to the system message. They pin temperature to 0. They cache intermediate results. These help at the margins, but they don't solve the structural problem: **without a quantitative measure of output quality, you cannot compare runs.**

You can read Run A and read Run B and form an opinion about which is better. But that opinion is itself subjective and non-reproducible. You've replaced agent inconsistency with human inconsistency.

## The Optimization Model Approach

The alternative is to define a mathematical function that scores agent output. Not a vibe check. Not "this one feels more thorough." A function that takes extracted features from the output and returns a number.

This is what optimization models provide for multi-agent systems: **a deterministic scoring layer on top of non-deterministic generation.**

The concept is straightforward. After agents produce their output, you extract features from that output -- quantitative measurements of what actually happened. Then you feed those features into a payoff function that returns a score. Same features, same score. Always.

The score doesn't replace the output. The agents still produce their reviews, their arguments, their synthesis. The score tells you whether the dynamics that produced that output were healthy.

## How It Works in Practice

Consider a multi-agent negotiation. Three agents represent different stakeholders negotiating resource allocation. After each round, you extract two features per agent: how much of the negotiable space (the "zone of possible agreement") they covered, and how satisfied each party is with the proposed terms.

The payoff function is:

```
payoff = zopa_coverage * party_satisfaction
```

Best possible payoff is 1.0 -- full coverage, full satisfaction. The actual payoff tells you how far the negotiation drifted from optimal. And critically, the function also returns the best-response payoff -- what the agent could have achieved by playing optimally given what the other agents did.

When `payoff == best_response_payoff`, the agent is at Nash equilibrium. It couldn't have done better by changing its strategy unilaterally. When there's a gap, the agent left value on the table.

This gives you three things prompt engineering alone cannot:

**1. Comparability.** Run the negotiation ten times. Each run produces different text. But the payoff scores tell you which run produced the best dynamics. Run 7 scored 0.91 equilibrium quality. Run 3 scored 0.64. Run 7 was better, quantitatively.

**2. Tunability.** The payoff function has parameters. In a territorial mode (think responsibility assignment between agents), the function includes a `gamma` parameter that controls how harshly agents are penalized for overreach:

```
payoff = territory_held - gamma * overreach_penalty
```

Set `gamma = 0.5` and agents get away with moderate overreach. Set `gamma = 2.0` and any unjustified claim tanks their score. This is a deterministic knob that changes agent behavior without touching the prompt.

**3. Convergence prediction.** If you feed equilibrium scores into a Kalman filter across rounds, you get a convergence estimate with confidence bounds. "This deliberation will converge in 2 more rounds with 85% confidence." Or: "This deliberation is diverging -- stop spending tokens." Budget control through math, not intuition.

## The Eight-Mode Pattern

Different agent dynamics require different scoring functions. A cooperative review where agents seek alignment needs a different payoff than a competitive evaluation where only one option wins.

The pattern we've found useful maps each interaction mode to a game-theoretic form:

| Mode | What's Scored | Key Features |
|---|---|---|
| Cooperative | Alignment quality | Recommendations surviving into synthesis |
| Winner-take-all | Decision clarity | Win/loss plus score differential |
| Adversarial (PD) | Honest advocacy | Territory held minus overreach penalty |
| Red-blue | Attack/defense balance | Severity-weighted confirmed vs. mitigated findings |
| Negotiation | Deal quality | ZOPA coverage times party satisfaction |
| Resource allocation | Efficiency | Utilization minus inequality |
| Fair division | Fairness | Proportionality minus envy |
| Mechanism design | Social welfare | Welfare contribution minus gaming vulnerabilities |

The important thing is not these specific modes. It's that each one has a payoff function that returns `(payoff, best_response_payoff)`. The interface is uniform. The math varies by mode. And every function is pure -- no randomness, no model calls, no side effects.

## Why This Matters for Your System

You don't need a game theory PhD to apply this pattern. The steps are:

**Step 1: Define what "good" means quantitatively.** For your specific multi-agent task, what features of the output indicate quality? Not "it sounds right" -- actual measurable properties. Coverage of the input space. Agreement between agents. Severity of findings. Ratio of justified to unjustified claims.

**Step 2: Write a scoring function.** It takes extracted features and returns a number. Pure function. No LLM calls. This is your ground truth for comparing runs.

**Step 3: Compute best-response.** For each agent, calculate what they could have scored if they played optimally given the other agents' strategies. The gap between actual and best-response is your measure of equilibrium quality.

**Step 4: Track across rounds.** If your system runs multiple rounds, feed scores into a simple filter (exponential moving average works; Kalman is better). When the score stabilizes, you've converged. When it diverges, stop early and save the tokens.

The result: your multi-agent system still has the creative variance that makes LLMs useful, but you have a deterministic measurement layer that tells you when the variance produced a good outcome and when it didn't.

## The Free/Paid Split

In our framework (conversus), we drew a specific line: the multi-agent deliberation engine is free. The scoring layer is paid. This isn't arbitrary -- it maps to a real difference in value.

The deliberation engine is the creative layer. Agents argue, cross-review, revise, and synthesize. The output is useful on its own. You read the synthesis and make your decision.

The scoring layer is the analytical layer. It tells you whether the deliberation dynamics were healthy, whether agents reached equilibrium, whether convergence happened, and how to tune parameters for next time. This is what makes the output consistent and reproducible across runs.

Free users get the full deliberation. Paid users get the instrumentation that makes it enterprise-grade.

## The Bottom Line

If you're building with AI agents and getting inconsistent results, the fix is not better prompts. Prompts control what agents say. Scoring functions control how you evaluate what they said. These are different problems with different solutions.

The pattern: generate with LLMs, score with math. Same features, same score, every time. That's the consistency your stakeholders are asking for, and no amount of prompt engineering will give it to you.

Build the scoring function. Measure equilibrium quality. Track convergence. Then decide whether run #1 or run #2 was better -- with numbers, not opinions.
