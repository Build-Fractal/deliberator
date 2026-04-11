# Building a Config

`conversus decide` is great for quick ad-hoc questions, but the real power of the tool comes from **custom configs** — your own agents, your own target documents, your own modes. This page walks you through building a `conversus.yml` from scratch.

!!! tip "Using Claude Code?"
    Install the conversus plugin (`/plugin install https://github.com/Build-Fractal/conversus-oss`) and run `/conversus design`. It walks you through this entire flow interactively and writes the config for you.

## The 6-step process

### Step 1: Write the question

Frame your decision as a **specific** question. Vague questions produce vague deliberations.

| Vague | Specific |
|---|---|
| "What about our architecture?" | "Should we split the auth service out of the monolith, or keep it inline?" |
| "Is this spec good?" | "Does spec 043 correctly handle the AMPL-unavailable fallback path?" |
| "Review this" | "Evaluate the packaging-strategy proposal for PyPI-first vs APM meta-packaging." |

The question goes into two fields:

```yaml
subject: "Auth service extraction"
question: |
  Should we split the auth service out of the monolith, or keep it inline?
  Consider operational complexity, team ownership, and the cost of the
  extraction effort versus the risk of maintaining the status quo.
```

### Step 2: Pick a mode

The 8 modes map to decision types:

| Decision type | Mode | When to use |
|---|---|---|
| Collaborative refinement | `cooperative` | Docs review, spec polishing, team alignment — agents work together |
| Adversarial review | `red-blue` | Security threat modeling, red-team exercises — one side attacks, one defends |
| Winner-take-all | `winner-take-all` | Technology selection, vendor choice — pick one, the rest lose |
| Incentive analysis | `prisoners-dilemma` | Team dynamics, multi-party agreements — are stakeholders rationally aligned? |
| Negotiation | `negotiation` | Contract terms, feature scoping — multiple parties with competing interests |
| Zero-sum allocation | `resource-allocation` | Budget splits, capacity planning — limited pool, fixed total |
| Fair division | `fair-division` | Team assignments, workload balancing — minimize envy |
| Mechanism design | `mechanism-design` | Auction design, governance rules — design incentive structures |

```yaml
mode: cooperative
```

Unsure? Start with `cooperative`. It's the most generally useful and surfaces both agreement and disagreement without forcing adversarial framing.

### Step 3: Identify the target

What document(s) should agents read? This is the grounded context — the concrete thing they're evaluating.

```yaml
# Single file
target: specs/042-execution-providers/spec.md

# Multiple files
target:
  - specs/042-execution-providers/spec.md
  - specs/042-execution-providers/plan.md
  - engine/execution/providers/anthropic.py

# Whole directory (reads all .md files)
target: specs/042-execution-providers/
```

If you have **no target document**, you're in `decide` territory, not `run` territory — skip the config and use `conversus decide "<question>"` directly.

### Step 4: Define agents

Each agent is a role with a prompt. The secret to good agent definitions: **give each agent a genuinely different incentive**, not just a different job title. Ask yourself: *what does this agent lose if they're wrong?*

```yaml
agents:
  - name: security-engineer
    prompt: |
      You are a security engineer. Your reputation depends on catching
      vulnerabilities before they reach production. Review the target and
      identify: attack vectors, data exposure paths, auth boundary issues.
      Flag anything that would page you at 2am.

  - name: product-manager
    prompt: |
      You are a product manager under quarterly revenue pressure. You need
      this feature to ship by end of month. Evaluate the target from the
      perspective of: what's the minimum viable version, what can we defer,
      what blocks us from shipping?

  - name: site-reliability-engineer
    prompt: |
      You are an SRE. You'll carry the pager for this feature. Evaluate
      the target for: failure modes, rollback strategy, observability
      coverage, blast radius if things go wrong.
```

**2-4 agents is the sweet spot.** More agents = more phases = more cost. A 4-agent mechanism-design run is ~29 LLM launches; 3 agents cooperative is ~13.

### Step 5: Optional arbiter

An arbiter is a senior agent that **breaks ties** when the regular agents can't agree. Add one if you want a final, binding verdict when disputes remain.

```yaml
arbiter:
  name: senior-architect
  prompt: |
    You are the senior architect. When agents disagree, you rule. Your
    decision is final.
  trigger: disputes_remain   # only invoked if disputes phase leaves gaps
  influence: binding         # binding = final word, advisory = input only
```

Skip the arbiter if you want disputes **surfaced explicitly** rather than resolved. Unresolved disagreement is often more valuable than a forced consensus.

### Step 6: Configure output + mechanics

```yaml
output: deliberations/auth-service-extraction/output/
iterations: 1                # 1 = single pipeline pass (default). 2+ = repeat revision loop.
rounds: 1                    # agent dispatch rounds per phase. usually 1.
```

## Complete example

Putting it all together:

```yaml
subject: "Auth service extraction"
question: |
  Should we split the auth service out of the monolith, or keep it inline?
  Consider operational complexity, team ownership, and the cost of the
  extraction effort versus the risk of maintaining the status quo.

mode: cooperative
iterations: 1

target:
  - specs/auth-service-extraction/spec.md
  - specs/auth-service-extraction/plan.md

output: deliberations/auth-service-extraction/output/

agents:
  - name: security-engineer
    prompt: |
      You are a security engineer. Your reputation depends on catching
      vulnerabilities before they reach production. Identify attack vectors,
      data exposure paths, and auth boundary issues introduced or resolved
      by this split.

  - name: site-reliability-engineer
    prompt: |
      You are an SRE carrying the pager. Evaluate failure modes, rollback
      strategy, observability coverage, and blast radius for both options.
      Which one is easier to operate?

  - name: product-manager
    prompt: |
      You are a product manager under quarterly revenue pressure. Evaluate
      the cost of extraction (engineering weeks) against the risk of the
      status quo. What's the minimum viable split that unblocks the roadmap?

arbiter:
  name: senior-architect
  prompt: |
    You are the senior architect. When agents disagree, you rule. Weigh
    security + operational concerns against delivery timeline and give
    a binding recommendation.
  trigger: disputes_remain
  influence: binding
```

## Validate, dry-run, ship

Before committing to a real run:

```bash
# 1. Check syntax + estimate cost (no LLM calls)
conversus validate deliberations/auth-service-extraction/conversus.yml

# 2. Dry-run with mock provider (free, synthetic responses)
conversus run deliberations/auth-service-extraction/conversus.yml --provider mock

# 3. Real run with Claude Code
conversus run deliberations/auth-service-extraction/conversus.yml --provider claude-code
```

`validate` prints the total LLM launch count before you commit. A 3-agent cooperative run with an arbiter is ~17 launches. Know your cost before you spend it.

## The feedback loop

Your first config is almost always wrong. That's fine — treat it as a draft, run it, read the outputs, iterate.

Common failure modes and fixes:

| Symptom | Likely cause | Fix |
|---|---|---|
| Agents agreed too quickly | Prompts are too similar | Differentiate their incentives — what does each agent **lose** if wrong? |
| Synthesis missed a key concern | No agent was positioned to catch it | Add an agent with that specific stakeholder perspective |
| Agent kept asking for more context | Target is too thin | Add more files to `target`, or include supporting docs |
| "Vague question" error | Question fails the sufficiency classifier | Rewrite the question to be more specific (see Step 1) |
| Cross-reviews were shallow | Prompts didn't emphasize critique | Add "look for weaknesses in the other agent's position" to each prompt |
| Wrong mode | Using `cooperative` for an adversarial decision | Re-read the mode table in Step 2 and switch |

## Real examples

The best way to learn is to read configs that already work. These are all real deliberations shipped in this repo:

- [packaging-strategy/conversus.yml](https://github.com/Build-Fractal/conversus-oss/blob/main/deliberations/packaging-strategy/conversus.yml) — 4 agents, mechanism-design mode, 29 launches
- [docs-review/conversus.yml](https://github.com/Build-Fractal/conversus-oss/blob/main/deliberations/docs-review/conversus.yml) — 3 agents + arbiter, cooperative mode, 17 launches
- [docs-specs-integration/conversus.yml](https://github.com/Build-Fractal/conversus-oss/blob/main/deliberations/docs-specs-integration/conversus.yml) — 4 agents + arbiter, cooperative, 26 launches

Read them side-by-side to see how agent prompts and modes vary by decision type.

## Next steps

- **[Modes](modes.md)** — deep dive on all 8 deliberation modes with examples
- **[Config reference](config-reference.md)** — full YAML schema reference
- **[CLI reference](cli.md)** — every command and flag
- **[Specs & Deliberations](../developer-guide/specs-and-deliberations.md)** — real case studies from this repo
