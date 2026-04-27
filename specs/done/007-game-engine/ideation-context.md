# Ideation Context: Game Engine Spec

**Date**: 2026-03-20
**Participants**: User + Claude Opus 4.6

This document captures the conversation that led to spec 007. It starts from the research into Bemporad's game theory libraries and traces through the business model, plugin architecture, objective function construction, and scenario storage ideas.

---

## Research: Bemporad's Game Theory Libraries

User asked to evaluate 4 repos by Alberto Bemporad (IMT Lucca):

- **nashopt** — Main library. Computes GNEs using KKT conditions solved as nonlinear least-squares with JAX autodiff. Handles GNEPs, linear-quadratic games, parametric GNEPs, game-theoretic control (LQR, MPC). Most active (commit 3 days ago, 10 stars).
- **gnep-learn** — Active learning approach. A centralized entity probes agents' best responses and builds linear surrogate models via Kalman filtering to converge on equilibria.
- **nash_mpqp** — Parametric GNE solver for quadratic objectives with coupled linear constraints. Handles variational GNEs, min-norm, welfare solutions over parameter ranges.
- **jax-gnep** — Deprecated, merged into nashopt.

### Analysis: Current Fit

> **Claude**: Conversus uses game theory as **metaphor**, not math. The modes (cooperative, winner-take-all, PD, red-blue) are prompt engineering patterns that simulate game dynamics. Stagnation detection is dispute counting. There's no J(x) to minimize — agents produce text, not numerical strategies.

Key concept mapping:

| nashopt Concept | Conversus Analog | Gap |
|----------------|-----------------|-----|
| Agent objective J(x) | Agent identity prompt + docs | No quantifiable objective |
| Best response f(x_{-i}) | Agent's revision after cross-reviews | Text, not vectors |
| Nash equilibrium | All agents stop disputing | No proof of optimality |
| Parametric game parameter p | Config values (rounds, iterations, mode) | No optimization |

> **Claude**: The most immediately useful piece is **gnep-learn's active learning of best responses**. Conversus already has a centralized orchestrator probing agents and collecting responses — that's gnep-learn's architecture. The bridge is feature extraction from deliberation text → numerical vectors → nashopt analysis.

---

## Business Model Ideation

> **User**: I was thinking that conversus, without tooling like this could be free then this would be a tool you would pay for.

> **Claude**: That's a sharp business model. Free deliberation engine, paid optimization layer.

### Free Tier (conversus core)
- Multi-agent deliberation across all modes
- Full 5-6 phase engine
- Multi-round execution with stagnation detection
- Template-driven agent behavior
- Value: structured disagreement → convergence. Free forever.

### Paid Tier (game engine plugins)
- "Was this a good outcome?" — equilibrium quality scoring
- "What config should I use?" — parametric optimization
- "Will this converge?" — predictive stagnation before burning tokens
- "What's the optimal agent count?" — game-theoretic sizing
- Value: spend less on agents, get better outcomes, prove the result is sound

> **Claude**: The economics work because the free tier is where users learn the workflow and generate deliberation data. The paid tier saves them money on the thing that actually costs — agent launches. A 69-agent stress test that could have been predicted to converge in 2 rounds instead of running 3 is real money saved.

---

## Embedding Models Discussion

> **User**: Embedding models should be able to do this, correct? Would MTEB leaderboard models do the trick?

> **Claude**: Embeddings help but they're not the whole answer.

**What nashopt needs:** Structured, interpretable vectors. Each dimension has meaning — nashopt computes gradients over these.

**What embeddings produce:** Dense, opaque vectors. Great for semantic similarity. Useless for "what's the payoff if agent A changes position on THREAT-01?"

**Where embeddings shine:**
1. Semantic stagnation — cosine similarity > 0.95 between rounds = stagnant
2. Agreement measurement — cluster tightness = convergence score
3. Cross-round drift — trajectory in embedding space

**Where embeddings fail:**
- "Is this a Nash equilibrium?" — need structured payoffs, not similarity
- "Should agent A change position?" — need explicit objective function

> **Claude**: Two plugin packages, not one. `conversus-embeddings` (semantic analysis, runs locally, cheaper) and `conversus-nashopt` (mathematical proof, premium).

---

## Objective Function Construction

> **User**: Can we use structured data and symbolic logic transformations? If the objective function takes a certain form and a person says in plain language what they want, can we use logic to parse the data into its symbolic logic representation and use that to trigger the LLM to ask questions to fill in the gaps to create an objective function from conversation?

> **Claude**: The key insight is a three-stage pipeline:

### Stage 1: Symbolic Logic Parsing (deterministic)
```
"decide between Redis and Postgres"
    → decision_type = SELECTION
    → agents = [alternative_1, alternative_2]
    → objective_template = competitive-selection
    → gaps = [weights, constraints, scoring_criteria]
```
Pattern matching against known objective function forms. No LLM needed.

### Stage 2: LLM Gap-Filling (interactive)
```
Gaps: [speed_weight, cost_weight, budget_constraint]
LLM asks: "How important is speed vs cost?"
User: "Speed is twice as important"
→ speed_weight = 2.0, cost_weight = 1.0
```
The LLM is a translator, not a mathematician. It turns gap identifiers into natural-language questions and answers into parameter values.

### Stage 3: Objective Function Assembly (deterministic)
```
J_redis(x) = -(2.0 * speed + 1.0 * cost + 3.0 * deploy)
subject to: monthly_cost ≤ 200
```
Plug parameters into the template. The math is pre-defined; the LLM just filled slots.

> **Claude**: The LLM doesn't generate the objective function. It asks questions whose answers parameterize a known mathematical form. The symbolic logic determines WHAT to ask. The LLM determines HOW to ask it. The math determines what to DO with the answers.

**Objective function template library** (~20-30 canonical forms):

| Template | Mode | Form |
|----------|------|------|
| competitive-selection | WTA | J = -w·score + penalty·overlap |
| cooperative-integration | Cooperative | J = -accepted_recs + λ·disputes |
| territory-claiming | PD | J = territory - γ·overreach |
| risk-assessment | RB | J_red = -confirmed_risks; J_blue = -mitigated |
| budget-constrained | Any | J = quality - β·agent_cost |

---

## Scenario Storage and Replay

> **User**: We could also have an objective function concept stored in a DB so folks could rerun scenarios with different data, for example using the same scenario that was used for pull request 1 for pull request 2.

> **Claude**: This is what makes it a **product** rather than a tool.

### Scenario object stores:
- Game structure (mode, objective template, parameters, agent roles) — **reusable**
- Data bindings (target docs, agent docs, grounding) — **swappable**
- Run history (outcomes, scores, rounds used) — **auditable**

### Replay workflow:
```
/conversus replay caching-decision-2026-03 --target specs/caching-v2/spec.md
```
Loads the stored game structure, swaps the target data, runs with same parameters.

### Cross-run analysis with stored history:
- Outcome consistency across different data
- Parameter drift over time
- Which scenarios produce efficient deliberations
- Feed back into convergence predictor

> **Claude**: The intellectual work of defining the game is amortized across every future decision of the same type. That's the recurring value.

---

## Long-Term Vision

> **User**: This should be pluggable. In the long run I see this becoming an engine rather than driven by templates and prompts.

The evolution path:

| Aspect | Today (Templates) | Future (Engine) |
|--------|-------------------|-----------------|
| Agent behavior | Defined by prompt template | Computed by game engine, presented via template |
| Mode selection | User picks or keyword match | Engine analyzes structure, recommends mathematically |
| Convergence | Count disputes | Engine predicts equilibrium |
| Stagnation | Compare dispute counts | Engine detects no fixed point |
| Round count | User guesses | Engine computes optimal |
| Quality assurance | None | Equilibrium score proves quality |

Templates don't disappear — they become the **presentation layer**. The engine becomes the **decision layer**.
