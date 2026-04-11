---
description: Guided config builder — walks the user through creating a conversus.yml interactively. Ask one question at a time, build the config incrementally, write it to disk at the end.
---

# Conversus Design Wizard

Guide the user through building a `conversus.yml` file step by step. This is a **conversational wizard** — ask ONE question at a time, don't dump the whole form on them, and confirm each answer before moving to the next step.

## Step 0: Check installation

Before starting, verify conversus is installed:

```bash
conversus --version 2>/dev/null || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user:

> Conversus isn't installed. Install it with:
> ```
> pip install git+https://github.com/Build-Fractal/conversus-oss.git
> ```
> Then re-run `/conversus:design`.

## Step 1: The question

Ask:
> **What decision are you trying to make?** Be specific. Good examples:
> - "Should we split the auth service out of the monolith, or keep it inline?"
> - "Does spec 043 correctly handle the fallback when AMPL is unavailable?"
> - "Is our migration plan safe to run on a 50M-row table?"
>
> Vague questions like "what should we do?" won't work — the deliberation needs something concrete to argue about.

Wait for their answer. If the answer is vague (fewer than 8 words, or contains phrases like "in general", "overall", "thoughts on"), push back once:
> That's a bit vague — can you sharpen it? What specific choice or tradeoff are you deciding?

## Step 2: Target document(s)

Ask:
> **Do you have a spec, proposal, or document to deliberate on?** This is the grounded context the agents will read.
>
> - If yes: give me the path(s). Can be a single file, multiple files, or a directory.
> - If no: we'll use `conversus decide` instead of `conversus run`, which doesn't require a target.

If they have a target, verify it exists with `ls -la <path>`. If it doesn't, ask them to confirm the path.

If they have no target, skip to Step 3 but remember to output a `decide` command at the end instead of writing a `conversus.yml`.

## Step 3: Decision type → mode

Ask:
> **What kind of decision is this?** Pick the closest match:
>
> 1. **Collaborative refinement** — docs review, spec polishing, team alignment → `cooperative`
> 2. **Adversarial security/threat review** — red-team the proposal → `red-blue`
> 3. **Winner-take-all tradeoff** — pick one of N options, the rest lose → `winner-take-all`
> 4. **Incentive/game analysis** — are stakeholders rationally aligned? → `prisoners-dilemma`
> 5. **Stakeholder negotiation** — multiple parties with competing interests → `negotiation`
> 6. **Resource allocation** — budget/capacity splits, zero-sum → `resource-allocation`
> 7. **Fair division** — team assignments, workload balance → `fair-division`
> 8. **Mechanism design** — incentive structures, governance, auctions → `mechanism-design`

Map their answer to the mode. If they say "I don't know", default to `cooperative`.

## Step 4: Stakeholders → agents

Ask:
> **Who has skin in the game for this decision?** I'll turn each stakeholder into an agent. 2-4 agents is ideal.
>
> Examples:
> - "security engineer" — responsible for catching vulnerabilities
> - "product manager under quarterly revenue pressure" — needs to ship
> - "SRE who'll carry the pager" — cares about operational risk
> - "end user paying for the product" — cares about simplicity

For each stakeholder, draft an agent:

```yaml
- name: <slugified-role>
  prompt: |
    You are a <role>. <One sentence describing their incentive — what do
    they lose if they're wrong?>. Review the target and identify:
    <2-3 specific things this role would care about>.
```

Show the drafted agents and ask if they need adjustment. Iterate until the user is happy.

## Step 5: Optional arbiter

Ask:
> **Do you want an arbiter?** An arbiter is a senior agent that breaks ties when the other agents can't agree. Add one if you want a binding verdict; skip it if you want disagreement surfaced explicitly.

If yes, draft:
```yaml
arbiter:
  name: <role>
  prompt: |
    You are the <senior role>. When agents disagree, you rule. Your
    decision is final.
  trigger: disputes_remain
  influence: binding
```

## Step 6: Assemble and write

Build the full config:

```yaml
subject: "<2-6 word title>"
question: |
  <the full question>

mode: <mode>
iterations: 1

target: <target>

output: deliberations/<kebab-case-title>/output/

agents:
  - name: <agent 1>
    prompt: |
      <prompt>
  # ... more agents

# optional arbiter
```

Ask where to save it (default: `deliberations/<kebab-case-title>/conversus.yml`), then use `Write` to save it.

Show the user the validate and run commands:
```bash
conversus validate <path>
conversus run <path> --provider mock     # dry run (free)
conversus run <path> --provider claude-code  # real run
```

## No-target fallback

If the user had no target document in Step 2, skip writing a YAML file. Instead, tell them:

> Since you don't have a target document, run this directly:
> ```bash
> conversus decide "<question>" --provider claude-code --mode <mode>
> ```

## Rules

- **One question at a time.** Never dump the whole form.
- **Confirm and iterate.** Show drafts and let the user edit before writing.
- **Validate at the end.** Always suggest `conversus validate` before the first real run.
- **Start with mock.** Encourage `--provider mock` dry runs before spending credits.
