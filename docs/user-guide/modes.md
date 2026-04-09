# Deliberation Modes

Conversus has 8 modes. Each mode changes agent incentives, how cross-review works, and what the synthesis produces.

## cooperative

**Find common ground.** Agents represent complementary perspectives that must coexist. Cross-reviews find contradictions and tensions. Synthesis produces converged positions with remaining disputes documented.

**When to use:** Architecture reviews, spec refinement, integration decisions -- any situation where all perspectives will coexist in the final system.

**Example:** Three tool teams (APM, spec-kit, gh-aw) review a shared orchestrator spec. Each advocates for their tool's capabilities while finding integration points with the others.

```yaml
mode: cooperative
agents:
  - name: backend
    prompt: "You represent the Django backend team."
  - name: frontend
    prompt: "You represent the React frontend team."
```

**What you'll see:** A synthesis listing convergence points (areas of agreement) and surviving disputes, with each dispute attributed to the originating agents.

## winner-take-all

**Pick the best option.** Agents represent competing alternatives -- only one will be chosen. Cross-reviews become attack surfaces. Synthesis declares a winner with rationale and conditions where the runner-up wins.

**When to use:** Framework selection, vendor evaluation, any "pick one" decision with strong trade-offs.

**Example:** Zustand vs Redux Toolkit for state management. Each agent defends its library with evidence from docs, and attacks the other's weaknesses.

```yaml
mode: winner-take-all
agents:
  - name: zustand
    prompt: "You advocate for Zustand as the state management solution."
    docs: [docs/zustand-evaluation.md]
  - name: redux-toolkit
    prompt: "You advocate for Redux Toolkit."
    docs: [docs/redux-evaluation.md]
```

**What you'll see:** A synthesis declaring a winner with rationale, runner-up strengths, and conditions under which the runner-up would be the better choice.

## prisoners-dilemma

**Figure out who owns what.** Agents are incentivized to overstate their importance, but cross-reviews punish false claims. The Nash equilibrium is honest, well-evidenced advocacy. Scored on accuracy times value.

**When to use:** Responsibility assignment, scoping exercises, evaluating how much of each tool or team should own.

**Example:** Backend, frontend, and infra teams each claim ownership of auth logic. The mode surfaces honest boundaries by penalizing overreach.

```yaml
mode: prisoners-dilemma
agents:
  - name: backend
    prompt: "You represent the Django backend team."
  - name: frontend
    prompt: "You represent the React frontend team."
  - name: infra
    prompt: "You represent the infrastructure team."
```

**What you'll see:** A synthesis with ownership boundaries per agent, scored claims (accuracy x value), and a matrix showing where responsibilities overlap or were over-claimed.

## red-blue

**Stress-test the plan.** Asymmetric roles. Red team agents attack (find flaws, risks, failure modes). Blue team agents defend (with evidence, not dismissal). Synthesis produces a risk register.

**When to use:** Security review, stress-testing migration plans, pre-mortems, devil's advocate on high-stakes decisions.

**Example:** Reviewing an API gateway design. The attacker finds vulnerabilities; the defender explains mitigations.

```yaml
mode: red-blue
agents:
  - name: attacker
    role: red
    prompt: "You are a security researcher finding vulnerabilities."
  - name: defender
    role: blue
    prompt: "You are the architecture team defending the design."
    docs: [docs/api-gateway-spec.md]
```

**Note:** Red-blue mode requires at least one `role: red` agent and one `role: blue` agent.

**What you'll see:** A risk register listing each identified vulnerability, severity, the red team's attack, the blue team's defense, and a final risk rating.

## negotiation

**Reach a deal.** Agents have different interests and must find mutually acceptable terms. Cross-reviews identify ZOPAs (zones of possible agreement) and BATNAs (best alternatives). Synthesis produces a deal structure.

**When to use:** Contract terms, API boundaries between teams, SLA negotiations, resource sharing agreements.

**Example:** Two teams negotiating the API contract between a data pipeline and a reporting service.

```yaml
mode: negotiation
agents:
  - name: data-pipeline
    prompt: "You represent the data pipeline team. You need flexibility on schema changes."
  - name: reporting
    prompt: "You represent the reporting team. You need stable, versioned APIs."
```

**What you'll see:** A deal structure with agreed terms, concessions made by each side, ZOPA boundaries, and fallback BATNAs if no deal is reached.

**Solver scoring:** `J_i = zopa_coverage * party_satisfaction`. An agent scores highest when it covers the full Zone of Possible Agreement with high satisfaction. Best response is `1.0` (full coverage, full satisfaction).

## resource-allocation

**Distribute fairly.** Agents compete for a limited resource pool. Cross-reviews challenge overestimates and highlight dependencies. Synthesis produces an allocation plan with justification.

**When to use:** Budget allocation, headcount distribution, capacity planning, sprint planning across teams.

**Example:** Three teams share 100 compute hours per month.

```yaml
mode: resource-allocation
agents:
  - name: ml-team
    prompt: "You represent the ML training team. You need GPU compute for model training."
  - name: analytics
    prompt: "You represent the analytics team. You need compute for batch processing."
  - name: dev-team
    prompt: "You represent the dev team. You need compute for CI/CD and testing."
```

**What you'll see:** An allocation plan showing each agent's share of the resource pool, justification per allocation, and dependency notes where one team's allocation affects another.

**Solver scoring:** `J_i = utilization_efficiency - allocation_inequality`. Agents are rewarded for efficient resource use and penalized for inequality in the allocation. Best response is `1.0` (perfect utilization, zero inequality). Uses Shapley values to measure each agent's marginal contribution.

## fair-division

**Split with no envy.** Agents have subjective valuations of the items being divided. Cross-reviews challenge valuations. Synthesis produces an envy-free allocation where no agent prefers another's share.

**When to use:** Dividing shared codebases, splitting ownership of microservices, partitioning a monolith.

**Example:** Two teams splitting ownership of a monolith's modules.

```yaml
mode: fair-division
agents:
  - name: team-alpha
    prompt: "You value the user-facing modules most highly."
  - name: team-beta
    prompt: "You value the data processing modules most highly."
```

**What you'll see:** An envy-free allocation where each agent's bundle is listed, along with a proof that no agent prefers another's share given their stated valuations.

**Solver scoring:** `J_i = proportionality_score - envy_count / max(1, N-1)` where N is the number of agents. Agents are rewarded for proportional allocations and penalized for envying others. Best response is `1.0` (perfect proportionality, zero envy).

## mechanism-design

**Design the rules.** Instead of playing a game, agents design the game itself. Cross-reviews check for incentive compatibility and strategic manipulation. Synthesis produces a rule set that is strategyproof.

**When to use:** Designing review processes, voting systems, resource allocation rules, auction mechanisms.

**Example:** Designing the code review assignment process for a large team.

```yaml
mode: mechanism-design
agents:
  - name: fairness-advocate
    prompt: "You prioritize equitable review load distribution."
  - name: quality-advocate
    prompt: "You prioritize matching reviewers to their areas of expertise."
```

**What you'll see:** A proposed rule set (mechanism) with incentive-compatibility analysis, showing that truthful reporting is each agent's dominant strategy, plus examples of manipulation attempts the rules prevent.

**Solver scoring:** `J_i = social_welfare_contribution - gaming_vulnerability_count / max(1, total_vulnerabilities)`. Agents are rewarded for contributing to social welfare and penalized for introducing gaming vulnerabilities. Best response removes all vulnerabilities while maintaining welfare contribution.
