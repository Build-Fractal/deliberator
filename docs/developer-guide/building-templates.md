# Building Templates

Templates are the prompt layer. Each mode has 7 markdown files that define what agents are asked to do at each phase.

## Template structure

Templates live in `templates/{mode}/`:

```
templates/
├── cooperative/
│   ├── review.md
│   ├── cross-review.md
│   ├── revision.md
│   ├── disputes.md
│   ├── synthesis.md
│   ├── arbitration.md
│   └── cross-round-synthesis.md
├── winner-take-all/
│   └── (same 7 files)
├── red-blue/
│   └── (same 7 files)
└── ...
```

Every mode must have all 7 files. The linter validates their presence and variable usage.

## Template variables

Variables are wrapped in curly braces: `{VARIABLE_NAME}`. The canonical list is in `schema/variables.yml`.

### Universal variables (all phases, all modes)

| Variable | Type | Description |
|----------|------|-------------|
| `{AGENT_NAME}` | string | The agent's name from config |
| `{AGENT_PROMPT}` | string | The agent's full prompt text |
| `{MODE}` | string | Deliberation mode name |
| `{TARGET_FILES}` | path-list | Files being reviewed (formatted as bullet list) |
| `{AGENT_DOCS}` | path-list | Agent's grounding documents |
| `{OUTPUT_PATH}` | path | Where this agent should write output |

### Phase-specific variables

| Variable | Phases | Description |
|----------|--------|-------------|
| `{REVIEWED_AGENT_NAME}` | cross-review | Agent being reviewed |
| `{REVIEWED_AGENT_REVIEW_PATH}` | cross-review | Path to the reviewed agent's output |
| `{REVIEWER_REVIEW_PATH}` | cross-review | Path to the reviewer's own review |
| `{CROSS_REVIEWS_LIST}` | revision | Bullet list of cross-review file paths |
| `{AGENT_REVIEW_PATH}` | revision | Path to this agent's original review |
| `{ALL_DISPUTES_LIST}` | synthesis | Bullet list of all dispute file paths |
| `{ALL_REVISIONS_LIST}` | synthesis | Bullet list of all revision file paths |

### Conditional blocks

| Variable | Description |
|----------|-------------|
| `{PRIOR_FILES_SECTION}` | Prior iteration context (only when `prior:` is set) |
| `{PRIOR_ROUND_SECTION}` | Prior round context (multi-round only) |
| `{PRIOR_ARBITRATION_SECTION}` | Prior arbitration output (when available) |

### Dispute markers

Templates use `DISPUTES_BEGIN` / `DISPUTES_END` markers to delimit the disputes section in synthesis output. The engine extracts remaining disputes from between these markers.

## Mode-specific dispute headings

Each mode uses different headings in the synthesis disputes section:

| Mode | Disputes heading |
|------|-----------------|
| cooperative | "Remaining Disputes" or "Dangerous Contradictions Found" |
| winner-take-all | "Remaining Disputes" |
| prisoners-dilemma | "Disputed Boundaries" |
| red-blue | "Disputed Risks" |

The output contract parser handles all these variants.

## How to add a new mode

1. **Register the mode** in `deliberator/schemas/modes.py`:

```python
VALID_MODES: frozenset[str] = frozenset({
    "cooperative",
    # ...existing modes...
    "my-new-mode",
})
```

2. **Create template directory** at `templates/my-new-mode/` with all 7 files.

3. **Create feature schema** at `schema/features/my-new-mode.yml` defining mode-specific feature extraction rules.

4. **Create mode schema** at `schema/modes/my-new-mode.yml` defining mode metadata.

5. **Add game form mapping** in `schema/game-forms/mode-mapping.yml` to associate the mode with its game form.

6. **Add payoff function** in `deliberator/plugins/nashopt/payoffs.py` for equilibrium scoring.

7. **Run the linter** to validate templates:

```bash
uv run python3 -m linter.validate
```

## Template authoring guidelines

- Start every template with `# {Mode} {Phase} -- Phase N: {Phase Title}`.
- First line after the title: `You are **{AGENT_NAME}**.` followed by `{AGENT_PROMPT}`.
- Clearly separate "What to Read" (inputs) from "What to Produce" (outputs).
- In "What to Produce", always specify the output path: `Write your review to: \`{OUTPUT_PATH}\``.
- Define the exact section headings the agent must use (the output contract parser depends on them).
- End with constraints that prevent mode-inappropriate behavior (e.g., cooperative agents should not declare winners).

## Example: review.md skeleton

```markdown
# MyMode Review -- Phase 1: Initial Review

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. ...

## What to Read

1. **Target files** (the documents under review):
{TARGET_FILES}

2. **Your documentation** (your grounding material):
{AGENT_DOCS}

{PRIOR_FILES_SECTION}

{PRIOR_ROUND_SECTION}

## What to Produce

Write your review to: `{OUTPUT_PATH}`

Your review must contain the following sections:

### Executive Summary
...

### Key Findings
...

### Recommendations
...
```
