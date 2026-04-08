## Arbitrate: Guided Arbitration

`/conversus arbitrate` guides users through arbiter configuration when disputes remain after deliberation, then invokes Phase 6. It does not redefine arbitration mechanics — it provides a conversational interface to spec 001's engine.

This command adds no new arbitration logic. It detects unresolved disputes, asks who the arbiter is in plain language, explains what a grounding document is, generates the arbiter config, appends it to `conversus.yml`, and delegates execution to the Phase 6 engine.

In this version, the arbitrate command executes entirely in the main conversation. No subagents are launched for the guided UX (execution itself delegates to the Phase 6 engine, which launches agents as normal).

### Input

`/conversus arbitrate` accepts:

- **Default**: `/conversus arbitrate` — looks for a completed conversus output directory. Searches for `conversus.yml` in the current working directory to find the configured `output:` path.
- **With path**: `/conversus arbitrate <path>` — uses the provided path as the conversus output directory.
- **With force**: `/conversus arbitrate --force` — runs arbitration even if no disputes are detected (maps to `trigger: always`).

If a path is provided, use it as the output directory. If no path is provided, read `conversus.yml` from the current working directory and use the `output:` field as the output directory. If neither exists, fail with: "No conversus output found. Provide a path to a completed conversus output directory, or run from a directory containing conversus.yml."

### Missing Prerequisite Check

Before any other processing, validate that the output directory contains completed deliberation output:

1. Check that `summary/final.md` exists in the output directory.
   - If it does not exist: "No completed deliberation found at {path}. Run `/conversus converge` or `/conversus run` first to produce deliberation output."
   - Stop processing.

2. Check that `conversus.yml` exists (in the current working directory, or the parent of the provided output directory).
   - If it does not exist: "No conversus.yml found. The arbitrate command needs the original configuration to append the arbiter block."
   - Stop processing.

### Step 1: Dispute Detection

Read `{output}/summary/final.md`. Read the `mode` field from `conversus.yml` to determine which mode's parsing rules to apply. Use the Dispute-Parsing Subsystem to determine whether disputes remain and the dispute count.

**If disputes remain:**

Report:
```
{dispute_count} unresolved dispute(s) found in the deliberation output.

Arbitration can resolve these by having an authoritative voice review the disputes and issue rulings.
```

Proceed to Step 2.

**If no disputes remain and `--force` was NOT provided:**

Report:
```
No unresolved disputes. Arbitration is not needed.

All perspectives converged during deliberation. If you still want an authoritative review (for endorsement or additional scrutiny), re-run with --force.
```

Stop processing.

**If no disputes remain and `--force` WAS provided:**

Report:
```
No unresolved disputes, but --force was specified.

Running arbitration for authoritative review of the converged positions.
```

Proceed to Step 2 with `trigger: always`.

### Step 2: Check Existing Arbiter Config

Read `conversus.yml` and check whether an `arbiter:` block already exists.

**If an arbiter block already exists:**

Present the existing configuration in plain language:
```
An arbiter is already configured in conversus.yml:

  Arbiter: {arbiter.name}
  Grounding: {arbiter.grounding}
  Trigger: {trigger in plain language}
  Influence: {influence in plain language}

Run arbitration with this configuration? (yes / reconfigure / cancel)
```

- **If yes**: Skip to Step 5 (Execution).
- **If reconfigure**: Remove the existing arbiter block and proceed to Step 3.
- **If cancel**: Stop processing.

**If no arbiter block exists:**

Proceed to Step 3.

### Step 3: Guided Arbiter Configuration

Guide the user through arbiter setup using plain language. No arbitration jargon.

#### 3a: Arbiter Identity

Ask the user:
```
Who should arbitrate?

This is the voice that reviews the disputes and makes decisions. Common choices:

  - The system being reviewed — it speaks for itself, accepting or rejecting changes
    based on its own design principles.
  - A senior stakeholder — someone with authority over the domain (a tech lead,
    product owner, or architect).
  - A set of governing principles — the project's values, requirements, or
    constitution serve as the decision framework.

Who should make the final call on these disputes?
```

Based on the user's response, generate an arbiter identity prompt:

- If the user describes the system/subject being reviewed: generate a prompt that positions the arbiter AS the system. Example pattern: "You ARE {system}. You have been reviewed by {agent_count} independent perspectives. You must now respond to their disputes — accepting changes that serve your core purpose and rejecting changes that would compromise your design principles."

- If the user describes a stakeholder role: generate a prompt that positions the arbiter as that role. Example pattern: "You are {role}. You have authority over {domain}. Review the disputes raised by the deliberation and issue rulings based on your domain expertise and organizational priorities."

- If the user describes governing principles or a document: generate a prompt that positions the arbiter as an impartial judge applying those principles. Example pattern: "You are an impartial arbiter. Your rulings must be grounded in {principles/document}. For each dispute, determine which position better aligns with the stated principles and explain your reasoning."

#### 3b: Prompt Review

Present the generated prompt to the user:
```
Generated arbiter prompt:

  {generated prompt}

Use this prompt? (yes / edit)
```

- **If yes**: Proceed to 3c.
- **If edit**: Accept the user's revised prompt. Validate it is non-empty. Proceed to 3c.

#### 3c: Grounding Document

Ask the user:
```
What document grounds the arbiter's decisions?

The grounding document is what the arbiter cites when making rulings. Without
it, decisions would be arbitrary — the arbiter needs a source of truth.

Examples:
  - Design principles or architecture decision records
  - A project constitution or values document
  - Requirements specifications or acceptance criteria
  - A style guide or coding standards

Path to the grounding document:
```

**If the user provides a path:**

Validate the path exists on disk. If it does not exist, report: "File not found: {path}. Please provide a valid path." Re-ask.

**If the user has no grounding document:**

```
A grounding document is required — without one, the arbiter has no basis for
its decisions.

Would you like to create a minimal grounding document from the problem
definition? This extracts constraints and success criteria from problem.md
as a starting point. (yes / no — I'll provide my own path)
```

- **If yes**: Check that `problem.md` exists. If it does, read the Constraints and Success Criteria sections from `problem.md`. Write a minimal grounding document at `grounding.md` (in the same directory as `conversus.yml`) with this structure:

  ```markdown
  # Decision Framework

  ## Constraints
  {constraints from problem.md}

  ## Success Criteria
  {success criteria from problem.md}

  ## Principles
  - Decisions must be justified against the constraints and success criteria above.
  - When constraints conflict, prefer the constraint that most directly serves the success criteria.
  ```

  Report: "Created grounding.md from problem.md constraints and success criteria. Review and refine as needed."

  If `problem.md` does not exist: "No problem.md found. Please provide a path to an existing grounding document, or create one manually." Re-ask.

- **If no**: Re-ask for a path.

#### 3d: Influence Level

Ask the user:
```
How much authority should the arbiter's rulings carry?

  - Final authority — the arbiter's decisions are binding. Disputes are
    resolved as the arbiter decides. (This is the default and most common choice.)

  - Recommended — adopt the arbiter's decisions unless you have specific
    counter-evidence. The rulings carry weight but are not absolute.

  - Advisory — consider the arbiter's perspective, but you are not bound by it.
    Use this when you want an informed opinion, not a final decision.

Which level? (final authority / recommended / advisory)
```

Map the user's response:
- "final authority" (or similar affirmative/default) -> `influence: binding`
- "recommended" -> `influence: recommended`
- "advisory" -> `influence: advisory`

If the user does not have a preference or says something like "I don't know" or "default": use `binding`.

### Step 4: Generate and Append Config

Construct the arbiter config block:

```yaml
arbiter:
  name: {arbiter_name}
  prompt: |
    {arbiter_prompt}
  grounding: {grounding_path}
  trigger: {disputes_remain | always}
  influence: {binding | recommended | advisory}
```

The `trigger` field:
- If `--force` was used (no disputes detected): `always`
- If disputes were detected: `disputes_remain`

The `name` field: derive from the user's arbiter description. Use a lowercase, hyphenated identifier (e.g., "the system being built" -> `the-system`, "tech lead" -> `tech-lead`, "project principles" -> `project-principles`). The name must match `[a-z0-9][a-z0-9-_]*`.

Present the complete arbiter block to the user:
```
Arbiter configuration:

  Name: {name}
  Grounding: {grounding_path}
  Trigger: {trigger} — {plain-language explanation}
  Influence: {influence} — {plain-language explanation}

Append this to conversus.yml and run arbitration? (yes / edit / cancel)
```

Plain-language trigger explanations:
- `disputes_remain`: "arbitration runs only if the synthesis contains unresolved disputes"
- `always`: "arbitration runs regardless of whether disputes remain"

Plain-language influence explanations:
- `binding`: "the arbiter's rulings are final — disputes are resolved as decided"
- `recommended`: "the arbiter's rulings should be adopted unless you have counter-evidence"
- `advisory`: "the arbiter's rulings are informational — consider but not bound"

- **If yes**: Append the arbiter block to `conversus.yml`. Proceed to Step 5.
- **If edit**: Accept changes. Re-present for confirmation. Proceed to Step 5 on confirmation.
- **If cancel**: Stop processing without modifying `conversus.yml`.

### Step 5: Execution

Execute Phase 6 using the existing engine defined in the Run: Execution section.

Zero new arbitration logic. The arbitrate handler delegates entirely to the Phase 6 engine:

1. Read `conversus.yml` (now containing the arbiter block).
2. Parse and validate the config using the same Step 1 validation from Run: Execution. If validation fails, report the error in plain language and suggest what to fix.
3. Resolve the trigger condition:
   - If `trigger: disputes_remain`: use the Dispute-Parsing Subsystem on `{output}/summary/final.md` to confirm disputes still exist. If the trigger is not met (disputes resolved between detection and execution), report: "Phase 6 skipped: disputes resolved since last check." Stop processing.
   - If `trigger: always`: proceed unconditionally.
4. Create `{output}/arbitration/` directory if it does not exist.
5. Load the arbitration template from `templates/{mode}/arbitration.md`.
6. Fill template variables and launch the Phase 6 agent (foreground, not background).
7. Wait for completion.

All template variables, output validation, and failure handling follow the Phase 6 specification in Run: Execution exactly. No deviations.

### Step 6: Post-Arbitration Report

After Phase 6 completes, present a plain-language summary of the results.

Read `{output}/arbitration/resolution.md`. For each ruling in the resolution, present a one-line summary:

```
Arbitration complete.

Arbiter: {arbiter_name}
Influence: {influence in plain language}
Disputes reviewed: {count}

Rulings:
  - {dispute summary} -> {decision summary} ({one-sentence rationale})
  - {dispute summary} -> {decision summary} ({one-sentence rationale})
  ...

Full output: {output}/arbitration/resolution.md

{if influence is 'binding':}
These rulings are binding. The arbiter has resolved all reviewed disputes.

{if influence is 'recommended':}
These rulings are recommended. Adopt them unless you have specific counter-evidence.

{if influence is 'advisory':}
These rulings are advisory. Consider them alongside other evidence.

{if mode is 'cooperative':}
To apply changes: /speckit.specify --input {output}/summary/final.md
```

The ruling summaries are extracted from the resolution document by reading the dispute-specific sections. Each ruling should be condensed to: the dispute topic, the decision (accepted/rejected/modified), and the core rationale in one sentence. Do not dump the full resolution text.

If the resolution document cannot be parsed for individual rulings (malformed output), fall back to:
```
Arbitration complete. Review the full output at {output}/arbitration/resolution.md
```

---
