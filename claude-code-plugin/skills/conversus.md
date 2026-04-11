---
name: conversus
description: >-
  Run competitive multi-agent deliberation using the conversus CLI.
  Supports: design (guided config builder), run (full deliberation from config),
  decide (ad-hoc question), validate (check config + cost estimate),
  init (project setup), status (provider auth), login/logout.
allowed-tools: Bash Read Write
---

## Subcommand dispatch

`/conversus [subcommand] [args]`

| Invocation | Action |
|---|---|
| `/conversus design` | **Guided config builder** — walks you through creating a conversus.yml |
| `/conversus run <config>` | Run full deliberation from a config file |
| `/conversus decide "<question>"` | Ad-hoc deliberation on a natural-language question |
| `/conversus validate <config>` | Validate a config and show cost estimate |
| `/conversus init` | Set up runtime permissions for this project |
| `/conversus status` | Show provider authentication status |
| `/conversus login <provider>` | Authenticate with a model provider |
| `/conversus logout <provider>` | Remove stored provider credentials |
| `/conversus` (no args) | Show this help |

If the first argument doesn't match a known subcommand, say:
> Unknown subcommand: '<arg>'. Available: design, run, decide, validate, init, status, login, logout.

---

## Step 0: Check installation (always)

Before any subcommand, verify conversus is installed:

```bash
conversus --version 2>/dev/null || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, tell the user:

> Conversus isn't installed. Install it with:
> ```
> pip install git+https://github.com/Build-Fractal/conversus-oss.git
> ```
> Then re-run your command.

Stop and wait for them to install.

---

## `/conversus design` — Guided config builder

**Use this when**: the user wants to run a deliberation but doesn't want to write YAML from scratch.

This is a **conversational wizard**. Walk the user through 5 questions, build the config incrementally, and write it to disk at the end. Do NOT dump the whole form on them at once — ask one thing at a time.

### Step 1: The question

Ask:
> **What decision are you trying to make?** Be specific. Good examples:
> - "Should we split the auth service out of the monolith, or keep it inline?"
> - "Does spec 043 correctly handle the fallback when AMPL is unavailable?"
> - "Is our migration plan safe to run on a 50M-row table?"
>
> Vague questions like "what should we do?" won't work — the deliberation needs something concrete to argue about.

Wait for their answer. If the answer is vague (fewer than 8 words, or contains phrases like "in general", "overall", "thoughts on"), push back once:
> That's a bit vague — can you sharpen it? What specific choice or tradeoff are you deciding?

### Step 2: Target document(s)

Ask:
> **Do you have a spec, proposal, or document to deliberate on?** This is the grounded context the agents will read.
>
> - If yes: give me the path(s). Can be a single file, multiple files, or a directory.
> - If no: we'll use `conversus decide` instead of `conversus run`, which doesn't require a target.

If they have a target, verify it exists:
```bash
ls -la <target_path>
```

If it doesn't exist, ask them to confirm the path. If they have no target, skip to Step 3 but remember to output a `decide` command instead of writing a `conversus.yml` at the end.

### Step 3: Decision type → mode

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

Map their answer to the mode. If they say something like "I don't know", default to `cooperative` — it's the safest and most generally useful mode for first-time users.

### Step 4: Stakeholders → agents

Ask:
> **Who has skin in the game for this decision?** I'll turn each stakeholder into an agent. 2-4 agents is ideal — more than 4 gets expensive fast.
>
> Examples of good agent stakeholders:
> - "security engineer" — responsible for catching vulnerabilities
> - "product manager under quarterly revenue pressure" — needs to ship
> - "SRE who'll carry the pager" — cares about operational risk
> - "end user paying for the product" — cares about simplicity and value

Wait for their list. For each stakeholder, draft an agent prompt like:

```yaml
- name: <slugified-role>
  prompt: |
    You are a <role>. <One sentence describing their incentive — what do
    they lose if they're wrong?>. Review the target and identify:
    <2-3 specific things this role would care about>.
```

Show the drafted agents to the user and ask:
> Here are the agents I drafted from your stakeholders. Do these look right, or should I adjust any?

Iterate until they're happy.

### Step 5: Optional arbiter

Ask:
> **Do you want an arbiter?** An arbiter is a senior agent that breaks ties when the other agents can't agree. If you want a final, binding verdict when there are disputes, add one. If you want to see the disagreement surfaced explicitly, skip it.

If yes, draft an arbiter block:
```yaml
arbiter:
  name: <role>
  prompt: |
    You are the <senior role>. When agents disagree, you rule. Your
    decision is final.
  trigger: disputes_remain
  influence: binding
```

### Step 6: Assemble and write

Build the full `conversus.yml` structure. For a `run` config (has target):

```yaml
subject: "<2-6 word title for the decision>"
question: |
  <the full question from Step 1>

mode: <mode from Step 3>
iterations: 1

target: <target from Step 2>

output: deliberations/<kebab-case-title>/output/

agents:
  - name: <agent 1 name>
    prompt: |
      <agent 1 prompt>
  - name: <agent 2 name>
    prompt: |
      <agent 2 prompt>
  # ... etc

# optional arbiter block if added
```

Ask the user where to save it:
> Where should I save this? Suggested path: `deliberations/<kebab-case-title>/conversus.yml`

Use `Write` to save the file. Then show the user the validation and run commands:

```bash
# Check syntax + estimate cost (no LLM calls)
conversus validate <path>

# Dry-run with mock provider (free, synthetic responses)
conversus run <path> --provider mock

# Real run
conversus run <path> --provider claude-code
```

### Step 6 alternative: no target → decide command

If the user skipped Step 2 (no target), don't write a YAML file. Instead, tell them:

> Since you don't have a target document, run this directly:
>
> ```bash
> conversus decide "<question>" --provider claude-code --mode <mode>
> ```
>
> This uses the built-in pragmatist + devil's advocate agents. If you want to use your custom stakeholder agents, save the config anyway and run with `conversus run`.

### Design wizard — rules

- **One question at a time**. Never dump the whole form.
- **Confirm and iterate**. Show drafted agents/YAML and let the user edit before writing.
- **Validate at the end**. Always suggest `conversus validate` before the first real run.
- **Start with mock**. Encourage the user to do a `--provider mock` dry run first so they see the pipeline shape without spending credits.

---

## `/conversus run` — Run a deliberation

```bash
conversus run <config_path> [--provider <provider>] [--model <model>] [--rounds <n>] [--phase <phase>]
```

Providers: `mock` (default, no API key), `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`.

Example:
```bash
conversus run deliberations/my-review/conversus.yml --provider claude-code
```

After running, display output paths and the synthesis if present.

---

## `/conversus decide` — Ad-hoc deliberation

```bash
conversus decide "<question>" [--provider <provider>] [--mode <mode>]
```

Uses the built-in pragmatist + devil's advocate agents. No config file needed.

Modes available to `decide`: `cooperative`, `winner-take-all`, `prisoners-dilemma`, `red-blue`. (The other 4 modes require a config file with custom agents.)

Example:
```bash
conversus decide "Should we use Redis or Postgres for session storage?" --provider anthropic
```

Display the structured result output.

---

## `/conversus validate` — Check config + estimate cost

```bash
conversus validate <config_path>
```

Prints the mode, agent count, iterations, and **total LLM launches** — critical to check before a real run. A 3-agent cooperative config is ~13 launches; a 4-agent mechanism-design config is ~29.

---

## `/conversus init` — Project permissions

```bash
conversus init [--runtime <runtime>] [--provider <provider>] [--model <model>] [--force]
```

Writes a runtime settings file (`.claude/settings.json` by default) so conversus can dispatch sub-agents without interactive permission prompts. **Run this once per project** or you'll hit 29 "Approve?" dialogs during a 4-agent deliberation.

Runtimes: `claude-code` (default), `opencode`, `copilot`, `gemini`, `codex`, `aider`.

---

## `/conversus status` / `login` / `logout`

```bash
conversus status                    # show auth state for all providers
conversus login <provider>          # OAuth login (anthropic, openai, ...)
conversus logout <provider>         # remove stored credentials
```

---

## Displaying results

- Show CLI output verbatim. Preserve any Rich-formatted tables or progress bars.
- If a command exits non-zero, diagnose and suggest:
  - **Config error**: check YAML syntax, required fields (`mode`, `agents`, and `target` for `run`).
  - **Provider error**: run `conversus status`, then `conversus login <provider>` if needed.
  - **File not found**: confirm the path is correct relative to the current directory.
  - **MCP extras missing**: `pip install "conversus[mcp] @ git+https://github.com/Build-Fractal/conversus-oss.git"`.
