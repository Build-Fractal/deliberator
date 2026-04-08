# Feature Specification: Decision-Making Framework

**Feature ID**: `003-decision-framework`
**Created**: 2026-03-19
**Status**: Draft
**Depends On**: `001-subject-arbitration` (optional Phase 6), `002-recursive-rounds` (optional multi-round)

---

## 1. Feature Summary

Conversus today is a competitive multi-agent deliberation tool for engineers. It works, but it requires hand-crafting a `conversus.yml` with agent identity prompts, documentation paths, competition modes, and output directories. The person configuring it must understand game theory modes, agent prompt engineering, and the YAML schema. This limits Conversus to power users who already know what they want.

This spec transforms Conversus from a deliberation tool into a **decision-making framework** with a guided workflow. Five new commands walk a user from a natural-language problem statement to a fully executed deliberation with optional binding arbitration. The competition modes, agent orchestration, prompt engineering, and YAML configuration become implementation details hidden behind a conversational interface.

The analogy: spec-kit turned specification into a guided workflow (`/speckit.specify` -> `/speckit.plan` -> `/speckit.tasks` -> `/speckit.implement`). This spec does the same for decisions. A user describes a problem, identifies the competing interests, and the system handles the rest.

**What changes**: Five new slash commands (`/conversus define`, `/conversus interests`, `/conversus mode`, `/conversus converge`, `/conversus arbitrate`) that chain into a guided workflow. Each command produces a concrete artifact. The final command generates and executes a `conversus.yml` automatically.

**What does not change**: `/conversus run` continues to work exactly as today for users who prefer hand-crafted YAML. The new commands are an on-ramp, not a replacement.

---

## 2. User Stories

### US-1: Define the Decision (`/conversus define`)

As a user facing a decision, I want to describe my problem in natural language so that the system creates a structured problem definition I can refine before deliberation.

**Input**: Natural-language description of the decision point, trade-off, or problem. Optionally, a path to existing documents that provide context (specs, proposals, architecture docs).

**Output**: `problem.md` in the working directory (or a specified output path).

**Acceptance Criteria**:

1. **Given** a user runs `/conversus define` and provides a natural-language description ("We need to decide whether to use server-side rendering or client-side rendering for the patient dashboard"), **When** the command completes, **Then** a `problem.md` file is written containing: a structured problem statement, the decision type (selection, integration, scoping, stress-test), key constraints identified from the description, and open questions the user should consider.

2. **Given** a user provides context documents (`/conversus define --context specs/003-dashboard/spec.md`), **When** the command processes, **Then** the agent reads the context documents and incorporates domain-specific constraints, stakeholders, and trade-offs into the problem definition. The problem statement references concrete details from the context, not generic platitudes.

3. **Given** a user provides no description and no context, **When** the command runs, **Then** the agent asks clarifying questions interactively: "What decision are you facing?", "Who or what are the competing perspectives?", "What are the constraints?"

4. **Given** the output `problem.md` already exists, **When** the command runs, **Then** the agent reads the existing file, presents it to the user, and asks whether to refine or replace it.

5. **Given** the problem description is vague ("we need to figure out the architecture"), **When** the command runs, **Then** the agent produces the best problem definition it can and explicitly marks ambiguities with `[CLARIFY: ...]` tags for the user to resolve before proceeding.

**`problem.md` structure**:

```markdown
# Problem Definition

## Decision
<one-sentence statement of the decision to be made>

## Type
<selection | integration | scoping | stress-test>

## Context
<2-4 sentences of relevant background, referencing context documents if provided>

## Constraints
- <constraint 1>
- <constraint 2>
- ...

## Success Criteria
<what does a good outcome look like?>

## Open Questions
- [CLARIFY: <question 1>]
- [CLARIFY: <question 2>]

## Source Documents
- <path to context doc 1>
- <path to context doc 2>
```

---

### US-2: Identify Competing Interests (`/conversus interests`)

As a user with a defined problem, I want to identify (or have the system suggest) the competing interests, perspectives, or stakeholders so that each becomes a grounded agent in the deliberation.

**Input**: The `problem.md` from US-1. Optionally, explicit interest names or perspectives provided by the user. Optionally, documentation paths for grounding each interest.

**Output**: `interests.md` in the same directory as `problem.md`.

**Acceptance Criteria**:

1. **Given** a `problem.md` exists and the user runs `/conversus interests`, **When** the command completes, **Then** the agent reads the problem definition and suggests 2-5 competing interests with: a name, a one-sentence perspective statement, a draft identity prompt, and suggested documentation paths for grounding. The user is asked to confirm, modify, or add interests.

2. **Given** a user provides explicit interests (`/conversus interests --add "backend-team" --add "frontend-team" --add "devops"`), **When** the command runs, **Then** the agent creates entries for each named interest, generates identity prompts based on the name and the problem context, and asks the user for documentation paths to ground each.

3. **Given** the problem type is "selection" (from `problem.md`), **When** interests are suggested, **Then** each interest represents a competing alternative (e.g., "React", "Svelte", "Vue" for a framework selection). The identity prompts are adversarial — each agent advocates for its alternative.

4. **Given** the problem type is "integration", **When** interests are suggested, **Then** each interest represents a stakeholder or component that must coexist. The identity prompts are cooperative — each agent advocates for its needs while seeking integration.

5. **Given** the problem type is "scoping", **When** interests are suggested, **Then** each interest represents a party that could own the responsibility. The identity prompts are calibrated for honesty — each agent declares capabilities and deferrals.

6. **Given** the problem type is "stress-test", **When** interests are suggested, **Then** interests are split into attackers and defenders. The identity prompts assign red or blue roles.

7. **Given** an interest has no documentation paths, **When** the agent generates the entry, **Then** it marks the docs field as `[NEEDS DOCS: suggest what to provide]` and warns the user that ungrounded agents produce weaker arguments.

8. **Given** `interests.md` already exists, **When** the command runs, **Then** the agent reads the existing file, presents the current interests, and asks whether to add, remove, or modify entries.

**`interests.md` structure**:

```markdown
# Competing Interests

## Problem Reference
<path to problem.md>

## Interests

### <interest-name>
- **Perspective**: <one-sentence what this interest cares about>
- **Prompt**: |
    <full identity prompt for the agent>
- **Docs**:
    - <path/to/doc1>
    - <path/to/doc2>
- **Role**: <red | blue>  <!-- only for stress-test type -->

### <interest-name-2>
...
```

---

### US-3: Select Competition Mode (`/conversus mode`)

As a user with a defined problem and identified interests, I want the system to recommend the right competition mode so that I do not need to understand game theory to get a good deliberation.

**Input**: `problem.md` and `interests.md` from prior steps.

**Output**: A `conversus.yml` in the same directory, fully configured and ready to execute.

**Acceptance Criteria**:

1. **Given** a `problem.md` with type "selection" and an `interests.md` with competing alternatives, **When** the user runs `/conversus mode`, **Then** the system recommends `winner-take-all` mode with a plain-language explanation: "Your interests represent competing alternatives where one will be chosen. Winner-take-all mode has each agent make its best case, attack competitors' weaknesses, and defend against attacks. The synthesis declares a winner with rationale."

2. **Given** a `problem.md` with type "integration" and an `interests.md` with complementary stakeholders, **When** the user runs `/conversus mode`, **Then** the system recommends `cooperative` mode with explanation: "Your interests represent perspectives that must coexist. Cooperative mode finds integration points and documents where perspectives conflict. All participants survive; the output is a unified recommendation."

3. **Given** a `problem.md` with type "scoping" and an `interests.md` with parties claiming overlapping territory, **When** the user runs `/conversus mode`, **Then** the system recommends `prisoners-dilemma` mode with explanation: "Your interests overlap in responsibility. Prisoner's Dilemma mode rewards honest capability declaration and punishes overreach. The output is a responsibility map showing who owns what."

4. **Given** a `problem.md` with type "stress-test" and an `interests.md` with red/blue roles, **When** the user runs `/conversus mode`, **Then** the system recommends `red-blue` mode with explanation: "You want to stress-test a proposal. Red-Blue mode has attackers find every flaw while defenders justify with evidence. The output is a risk register."

5. **Given** any recommendation, **When** the user disagrees, **Then** they can override: "Use cooperative instead." The system regenerates the `conversus.yml` with the overridden mode and explains the trade-off: "Cooperative mode will seek integration rather than declaring a winner. Agents will not have adversarial incentives."

6. **Given** the mode is selected (recommended or overridden), **When** the `conversus.yml` is generated, **Then** it includes: the selected mode, the target (from `problem.md` source documents, or `problem.md` itself if no source docs), the output directory (defaults to `conversus-output/` in the same directory), all agents from `interests.md` with their prompts and docs, iterations defaulting to 1, and a comment header explaining the config was auto-generated.

7. **Given** `problem.md` has an ambiguous type or the interests do not cleanly map to a single mode, **When** the system recommends, **Then** it presents the top two candidates with trade-off analysis and asks the user to choose.

8. **Given** a `conversus.yml` already exists in the directory, **When** the command runs, **Then** the agent presents the existing config, shows what would change, and asks for confirmation before overwriting.

**Mode selection logic** (see Section 5 for full details):

| Problem Type | Default Mode | Signal |
|---|---|---|
| selection | winner-take-all | Interests are alternatives solving the same problem |
| integration | cooperative | Interests must coexist, seeking alignment |
| scoping | prisoners-dilemma | Interests claim overlapping territory |
| stress-test | red-blue | Interests are split into attackers and defenders |

---

### US-4: Execute Deliberation (`/conversus converge`)

As a user with a generated `conversus.yml`, I want to review the configuration and kick off the full multi-agent deliberation so that I get a structured outcome without needing to understand the orchestration internals.

**Input**: The `conversus.yml` from US-3 (or a hand-crafted one — this command is the bridge).

**Output**: The full conversus output directory with all phase artifacts and the final synthesis.

**Acceptance Criteria**:

1. **Given** a `conversus.yml` exists in the working directory, **When** the user runs `/conversus converge`, **Then** the system presents a human-readable summary of the config: the problem (from `problem.md` if it exists), the mode (with a plain-language explanation), the agents (names and one-line perspectives), the target documents, and the estimated agent launches. The user is asked to confirm before execution begins.

2. **Given** the user confirms, **When** execution begins, **Then** the system delegates to the existing `/conversus run` execution engine. The 5-phase process runs exactly as defined in `SKILL.md`. No new execution logic is introduced — `converge` is a guided on-ramp to `run`.

3. **Given** the user declines ("the agents are wrong" or "change the mode"), **When** they provide feedback, **Then** the system routes them back to the appropriate prior step: `/conversus interests` to modify agents, `/conversus mode` to change the mode.

4. **Given** no `conversus.yml` exists, **When** the user runs `/conversus converge`, **Then** the system checks for `problem.md` and `interests.md`. If both exist, it runs the mode selection step first. If neither exists, it starts from `/conversus define`.

5. **Given** the deliberation completes, **When** the final report is printed, **Then** it includes the standard conversus report (from `SKILL.md` Step 5) plus a plain-language summary: what the mode means for interpreting the results, where to find the key output (always `summary/final.md`), and suggested next steps based on the mode.

6. **Given** `rounds > 1` is configured (spec-002), **When** the deliberation runs, **Then** multi-round execution proceeds as defined in spec-002. The `converge` command does not add behavior beyond what `run` provides — it is the same engine.

7. **Given** an `arbiter` is configured (spec-001), **When** Phase 5 completes and the trigger condition is met, **Then** Phase 6 runs as defined in spec-001.

---

### US-5: Resolve Remaining Disputes (`/conversus arbitrate`)

As a user whose deliberation produced unresolved disputes, I want an arbiter to make binding decisions so that the deliberation produces actionable outcomes even when agents cannot agree.

**Input**: A completed conversus run (the output directory with `summary/final.md` containing unresolved disputes). Optionally, an arbiter already configured in `conversus.yml`.

**Output**: `arbitration/resolution.md` in the output directory.

**Acceptance Criteria**:

1. **Given** a completed conversus run with unresolved disputes in `summary/final.md` and no `arbiter` in the `conversus.yml`, **When** the user runs `/conversus arbitrate`, **Then** the system guides the user through arbiter configuration: "The deliberation has N unresolved disputes. To arbitrate, I need: (1) Who is the arbiter? (2) What document grounds their decisions?" The system generates the `arbiter` config and appends it to the `conversus.yml`.

2. **Given** a completed conversus run with an `arbiter` already configured, **When** the user runs `/conversus arbitrate`, **Then** the system presents the arbiter config, confirms with the user, and executes Phase 6 as defined in spec-001.

3. **Given** a completed conversus run with NO unresolved disputes, **When** the user runs `/conversus arbitrate`, **Then** the system reports: "No unresolved disputes found in the synthesis. Arbitration is not needed." If the user insists, the system allows `trigger: always` to run a subject endorsement.

4. **Given** the user does not have a grounding document, **When** the system asks for one, **Then** it explains what a grounding document is in plain language: "A grounding document is the arbiter's decision framework — design principles, requirements, a constitution, or project values. Every ruling must cite it. This prevents arbitrary decisions." If the user has no such document, the system offers to help create a minimal one from the problem definition and constraints.

5. **Given** the arbitration completes, **When** the output is produced, **Then** the system presents a plain-language summary of each binding decision: the dispute, the ruling, and the one-sentence rationale. It also prints the path to the full `resolution.md`.

6. **Given** the user has not run any prior `/conversus` commands and directly invokes `/conversus arbitrate` against an existing output directory, **When** the command runs, **Then** it works — it reads the output directory, finds the synthesis, and proceeds. The command does not require the guided workflow to have been used.

---

## 3. Workflow

The five commands form a sequential pipeline. Each command produces an artifact consumed by the next. All commands are independently invocable — a user can enter at any point.

```
/conversus define          /conversus interests        /conversus mode
     │                          │                           │
     ▼                          ▼                           ▼
 problem.md ──────────────► interests.md ──────────────► conversus.yml
                                                            │
                                                            ▼
                                                   /conversus converge
                                                            │
                                                            ▼
                                                     output/summary/
                                                       final.md
                                                            │
                                                  (disputes remain?)
                                                            │
                                                            ▼
                                                  /conversus arbitrate
                                                            │
                                                            ▼
                                                   output/arbitration/
                                                     resolution.md
```

**Entry points**:

| User knows... | Start at | Skips |
|---|---|---|
| Nothing — just has a problem | `/conversus define` | Nothing |
| The interests but not the mode | `/conversus interests` | `define` |
| Everything — has a YAML | `/conversus converge` | `define`, `interests`, `mode` |
| Everything — hand-crafted expert | `/conversus run` | All new commands |

**Automatic chaining**: Each command can suggest the next step. After `define` completes: "Next: `/conversus interests` to identify the competing perspectives." After `interests` completes: "Next: `/conversus mode` to select how they compete." After `mode` completes: "Next: `/conversus converge` to run the deliberation." After `converge` completes with disputes: "Disputes remain. Run `/conversus arbitrate` to resolve them."

**No forced linearity**: A user can re-run any command at any time. Running `/conversus interests` after `/conversus mode` regenerates the interests and invalidates the `conversus.yml` (the system warns: "interests.md changed. Your conversus.yml may be out of date. Run `/conversus mode` to regenerate.").

---

## 4. Data Model

Each command produces a file. The files form a dependency chain.

### Artifacts by Phase

| Command | Artifact | Format | Consumed By |
|---|---|---|---|
| `define` | `problem.md` | Markdown with structured sections | `interests`, `mode` |
| `interests` | `interests.md` | Markdown with agent definitions | `mode` |
| `mode` | `conversus.yml` | YAML (existing schema) | `converge`, `run` |
| `converge` | `output/` directory | Full conversus output tree | `arbitrate`, user |
| `arbitrate` | `output/arbitration/resolution.md` | Markdown with binding decisions | User |

### File Placement

All artifacts are created in the working directory by default. The user can override with `--output <dir>`.

```
working-directory/
├── problem.md              # from /conversus define
├── interests.md            # from /conversus interests
├── conversus.yml           # from /conversus mode (or hand-crafted)
└── conversus-output/       # from /conversus converge
    ├── {agent}/
    │   ├── review.md
    │   ├── revision.md
    │   ├── disputes.md
    │   └── cross-reviews/
    │       └── {other-agent}.md
    ├── summary/
    │   └── final.md
    └── arbitration/        # from /conversus arbitrate (optional)
        └── resolution.md
```

### Artifact Ownership

- `problem.md`, `interests.md`: User-editable. The system generates them; the user refines them. The system must never overwrite without confirmation.
- `conversus.yml`: Generated from the prior artifacts. The system may regenerate it when upstream artifacts change.
- `output/`: System-generated. Read-only from the user's perspective during execution. The user reads results after completion.
- `arbitration/resolution.md`: System-generated. Final and binding for the scope of this deliberation.

---

## 5. Mode Selection Logic

The system recommends a competition mode based on the problem type (from `problem.md`) and the structure of the interests (from `interests.md`). The user always has final say.

### Decision Matrix

| Problem Type | Interest Pattern | Recommended Mode | Confidence |
|---|---|---|---|
| selection | Alternatives solving the same problem | winner-take-all | High |
| integration | Stakeholders/components that must coexist | cooperative | High |
| scoping | Parties with overlapping responsibilities | prisoners-dilemma | High |
| stress-test | Proposal with risk concerns | red-blue | High |
| selection | Alternatives that could be combined | cooperative | Medium — explain both options |
| integration | Stakeholders with hard either/or constraints | winner-take-all | Medium — explain trade-off |
| scoping | Two parties, one clearly subordinate | cooperative | Medium — PD may be overkill |
| unclear | Any | cooperative | Low — safest default, explain alternatives |

### Heuristics for Automatic Detection

When the user does not explicitly set a problem type, the system infers it from signals in the problem description and interest structure:

**Winner-take-all signals**:
- Language: "choose between", "pick one", "which is better", "A vs B", "evaluate alternatives"
- Interest structure: interests named after products, tools, frameworks, or approaches
- Constraint: mutual exclusivity stated or implied

**Cooperative signals**:
- Language: "how should these work together", "integrate", "align", "coordinate"
- Interest structure: interests named after teams, roles, systems, or components
- Constraint: all interests must be preserved in the outcome

**Prisoner's Dilemma signals**:
- Language: "who owns", "responsibility", "boundary", "scope", "divide"
- Interest structure: interests with overlapping capability claims
- Constraint: need clear ownership assignment

**Red-Blue signals**:
- Language: "what could go wrong", "risks", "vulnerabilities", "stress-test", "pre-mortem"
- Interest structure: asymmetric roles (attacker/defender, critic/advocate)
- Constraint: a specific proposal or plan exists to be tested

### Ambiguity Resolution

When signals are mixed, the system presents the top two candidates with a comparison:

```
I see two possible modes for this deliberation:

1. **Cooperative** — Your interests must coexist, so I'd normally recommend
   cooperative mode. But your problem has a "pick one" constraint on the
   authentication approach, which suggests...

2. **Winner-take-all** — ...that you need a clear winner for the auth
   approach, even though the teams implementing it must cooperate.

Recommendation: Run winner-take-all for the auth approach decision, then
a separate cooperative run for the integration plan. Or: use cooperative
mode with the understanding that the synthesis may recommend one approach
over another without the adversarial pressure of winner-take-all.

Which would you prefer?
```

---

## 6. Arbitration Design

Arbitration is the optional final phase that resolves disputes the deliberation could not. This section describes how the guided workflow integrates with the arbitration mechanism specified in `001-subject-arbitration`.

### When Arbitration Applies

Arbitration is relevant when:
- A deliberation completes with unresolved disputes in the synthesis
- The user wants binding decisions rather than open questions
- A natural arbiter exists (the subject of the review, a senior stakeholder, a governing document)

Arbitration is NOT relevant when:
- All disputes converged during deliberation
- The user prefers to make the decision themselves using the synthesis as input
- No natural arbiter or grounding document exists

### The `/conversus arbitrate` Flow

1. **Detect disputes**: Read `summary/final.md`, parse the `### Remaining Disputes` section. Count `**Dispute:` entries.

2. **If no arbiter configured**: Guide the user through configuration.
   - "Who should arbitrate? This is usually the subject of the review — the system being built, the team lead, or the project's governing principles."
   - "What document grounds the arbiter's decisions? This could be design principles, a constitution, requirements, or project values."
   - Generate the `arbiter:` block and append to `conversus.yml`.

3. **If arbiter configured**: Present the config, confirm, execute Phase 6 per spec-001.

4. **Present results**: Plain-language summary of each ruling.

### Arbiter Configuration (schema extension from spec-001)

```yaml
arbiter:
  name: <identifier>
  prompt: |
    <identity prompt — who the arbiter is and why they have authority>
  docs:
    - <path/to/relevant/docs>
  grounding: <path/to/decision-framework-document>
  trigger: disputes_remain | always
```

- `grounding` is required. An arbiter without a decision framework produces arbitrary rulings.
- `trigger: disputes_remain` is the default recommendation for guided workflow users.
- `trigger: always` runs the arbiter even when no disputes remain (produces a subject endorsement).

### Guided Arbiter Prompt Generation

When the user describes the arbiter in natural language ("the system being built" or "our CTO's priorities"), the `/conversus arbitrate` command generates an appropriate identity prompt:

- For "the subject of the review": the prompt positions the arbiter AS the system, evaluating from operational needs.
- For a stakeholder role: the prompt positions the arbiter as that role, evaluating from their priorities.
- For a governing document: the prompt positions the arbiter as an impartial judge applying the document's principles.

The user can edit the generated prompt before execution.

### Relationship to Spec-001

This spec does not redefine arbitration mechanics. It defines the guided workflow for configuring and invoking arbitration. The execution is entirely delegated to the Phase 6 engine defined in spec-001. Specifically:

- Spec-001 defines: the `arbiter` schema, Phase 6 execution, template variables, trigger evaluation, output format.
- This spec defines: the `/conversus arbitrate` command that guides users to configure and invoke spec-001's mechanism.

**Implementation gate**: `/conversus arbitrate` (Phase C) MUST NOT be implemented until spec 001 (Subject Arbitration) achieves spec-complete status — all FRs implemented and verified. Phase C delegates to the Phase 6 engine; that engine must be fully correct before building a guided on-ramp to it.

---

## 7. Integration

### Backward Compatibility

The existing `/conversus run` command is unchanged. Users who hand-craft `conversus.yml` files continue to use `run` exactly as today. The new commands are an alternative path to the same engine.

| Path | User | Effort | Control |
|---|---|---|---|
| `/conversus define` -> `interests` -> `mode` -> `converge` -> `arbitrate` | Non-expert | Low | Guided, constrained |
| Hand-craft `conversus.yml` -> `/conversus run` | Expert | Higher | Full control |
| `/conversus define` -> `interests` -> edit YAML manually -> `/conversus run` | Hybrid | Medium | Guided start, manual finish |

### Skill Registration

Each new command is a separate skill trigger registered in `SKILL.md`. The skill file must be updated to handle:

```
/conversus define [--context <path>] [--output <dir>]
/conversus interests [--add <name>] [--output <dir>]
/conversus mode [--override <mode>] [--output <dir>]
/conversus converge [<path-to-yml>]
/conversus arbitrate [<path-to-output-dir>]
/conversus run [<path-to-yml>]     # existing, unchanged
```

The skill parser dispatches to the appropriate subcommand handler based on the first argument.

### Relationship to Spec-001 and Spec-002

- **Spec-001 (Subject Arbitration)**: Provides the Phase 6 engine. This spec provides the guided `/conversus arbitrate` command that configures and invokes it. Can be implemented independently — `arbitrate` is optional and the guided workflow works without it (it just ends at `converge`).

- **Spec-002 (Recursive Rounds)**: Provides multi-round execution. The `converge` command transparently supports `rounds > 1` when configured. The mode selection step may recommend `rounds: 2` for complex integration problems. Can be implemented independently — single-round is the default.

### Template Requirements

No new prompt templates are needed for the `define`, `interests`, or `mode` commands. These commands use direct agent interaction (conversational), not the phase-based template system. The templates are only used by `converge` (which delegates to `run`) and `arbitrate` (which delegates to Phase 6).

### APM Package Updates

The `apm.yml` manifest must be updated to register the new skill triggers. The `allowed-tools` field remains the same (Agent, Read, Write, Bash). No new tool dependencies are introduced.

---

## 8. Success Criteria

### SC-1: Non-Expert Usability

A user with no knowledge of game theory, agent prompting, or YAML can go from "I have a decision to make" to a completed deliberation with actionable output using only the five guided commands. Verified by: a user describes a problem in plain English, the system produces a `conversus.yml`, and the deliberation runs to completion without the user editing any YAML.

### SC-2: Mode Recommendation Accuracy

For problems with clear type signals (selection, integration, scoping, stress-test), the system recommends the correct mode at least 4 out of 5 times without user override. Verified by: testing against 10 problem descriptions with known correct modes.

### SC-3: Artifact Chain Integrity

Each command's output is a valid input to the next command. The chain `define` -> `interests` -> `mode` -> `converge` produces identical results to a hand-crafted `conversus.yml` with the same configuration. Verified by: running both paths with equivalent inputs and comparing the generated YAML.

### SC-4: Full Backward Compatibility

`/conversus run` with a hand-crafted `conversus.yml` produces identical behavior and output to the current system. Zero regressions. Verified by: running the existing `conversus.example.yml` and the `conversus.yml` in the conversus root (the self-review config) and comparing output structure.

### SC-5: Entry-Point Flexibility

A user can enter the workflow at any command. `/conversus converge` works with a hand-crafted YAML. `/conversus interests` works without a `problem.md` (the user provides context interactively). `/conversus arbitrate` works against any completed conversus output directory. Verified by: invoking each command in isolation with appropriate inputs.

### SC-6: Guided Recovery

When a user is missing prerequisites (no `problem.md` when running `interests`, no `conversus.yml` when running `converge`), the system either routes them to the appropriate prior step or gathers the missing information interactively. No command fails silently due to missing artifacts. Verified by: invoking each command without its prerequisites and confirming guided recovery.

### SC-7: Arbitration Integration

`/conversus arbitrate` correctly configures and invokes the Phase 6 engine from spec-001. A guided-workflow arbitration produces the same output structure as a hand-configured `arbiter:` block in the YAML. Verified by: comparing arbitration output from both paths.

### SC-8: Plain-Language Output

Every command's output includes plain-language explanations suitable for a non-technical audience. Mode recommendations explain WHY, not just WHAT. Deliberation results include interpretation guidance. Verified by: reviewing output for jargon-free explanations at every decision point.

---

## 9. Constraints

### Must NOT

- **Must NOT require coding knowledge to use.** The guided workflow is designed for product managers, architects, and team leads who face decisions — not just engineers. All prompts, explanations, and outputs use plain language. Technical details (agent count, token estimates, YAML syntax) are presented only when the user asks or when they are needed for informed consent (e.g., estimated agent launches before execution).

- **Must NOT require game theory knowledge.** The mode names (cooperative, winner-take-all, prisoners-dilemma, red-blue) are implementation labels. The guided workflow uses plain-language descriptions: "find the best option", "make these work together", "figure out who owns what", "stress-test this plan." Mode names appear in the generated YAML but not in the user-facing conversation unless the user uses them first.

- **Must NOT break existing `/conversus run` behavior.** The `run` command is the power-user path. It accepts a `conversus.yml` and executes. The new commands generate a `conversus.yml` and then delegate to the same engine. No changes to the execution engine, template system, or output format.

- **Must NOT require a linear workflow.** Users can enter at any command, skip commands, re-run commands, or mix guided and manual configuration. The system adapts to what artifacts exist on disk.

- **Must NOT generate agents without user confirmation.** The system suggests interests, prompts, and documentation paths. The user confirms, modifies, or rejects. The system never executes a deliberation without the user reviewing and approving the configuration.

- **Must NOT hard-code agents or documentation paths.** The system suggests based on problem context, but all agent definitions are user-configurable. The framework is domain-agnostic — it works for framework selection, architecture review, team scoping, security analysis, or any multi-perspective decision.

- **Must NOT couple to a specific agent runtime.** The guided workflow uses the same tools as `/conversus run` (Agent, Read, Write). It works in any environment that supports these tools. The `SKILL.md` compatibility note ("Requires an agent runtime that supports background Agent tool dispatch") applies to `converge` (which delegates to `run`), not to `define`, `interests`, or `mode` (which are conversational).

### Must

- **Must work incrementally.** Each command produces a durable artifact on disk. The user can stop after any command and resume later. The system reads existing artifacts to determine current state.

- **Must preserve the existing YAML schema.** The `conversus.yml` generated by `/conversus mode` uses the exact same schema as hand-crafted configs. No schema extensions are introduced by this spec (schema extensions for arbitration and rounds are in spec-001 and spec-002 respectively).

- **Must generate high-quality agent prompts.** The identity prompts generated for each interest must be specific to the problem context, grounded in the declared documentation, and calibrated for the selected competition mode. Generic prompts ("You are an expert in X") are insufficient — the prompts must include: the agent's role in this specific decision, what it is grounding its arguments in, and how its incentives align with the competition mode.

- **Must handle multi-file targets.** When the problem references multiple source documents (spec + plan + data model), the generated `conversus.yml` must use the list target format. The system must correctly resolve file and directory paths.

---

## Delivery Phases

Spec 003 is decomposed into three independently shippable phases:

### Phase A: Define / Interests / Mode (M-effort)
**Commands**: `/conversus define`, `/conversus interests`, `/conversus mode`
**Dependencies**: None (these are conversational commands that produce markdown artifacts)
**Soft dependency**: Spec 004 presets improve `/conversus interests` suggestions (US-5) but are not required
**Sequencing**: After all P1 runtime fixes (spec 001 gaps). Phase A introduces a new execution model (interactive, stateful, multi-turn) that requires M-effort infrastructure: command dispatcher, interactive agent model, artifact state management, cross-command dependency validation. The P1 fixes change the behavior of the engine that `/conversus converge` delegates to — correct the engine first, then build the on-ramp.
**Output artifacts**: `problem.md`, `interests.md`, `conversus.yml`

### Phase B: Converge (S-effort)
**Commands**: `/conversus converge`
**Dependencies**: Phase A (needs generated `conversus.yml`), existing SKILL.md `run` engine
**Sequencing**: After Phase A. This is primarily a guided wrapper around `/conversus run` with pre-execution confirmation and post-execution plain-language summary.
**Output artifacts**: Full conversus output directory

### Phase C: Arbitrate (M-effort)
**Commands**: `/conversus arbitrate`
**Dependencies**: Spec 001 completion (all gaps closed — Phase 6 must be fully correct before building a guided on-ramp to it)
**Sequencing**: After Phase B and spec 001 completion. Hard gate: do not implement `/conversus arbitrate` until spec 001 is spec-complete.
**Output artifacts**: `arbitration/resolution.md`

## Appendix A: Command Quick Reference

| Command | Purpose | Input | Output | Interactive? |
|---|---|---|---|---|
| `/conversus define` | Structure the problem | Natural language, optional context docs | `problem.md` | Yes — asks clarifying questions |
| `/conversus interests` | Identify competing perspectives | `problem.md`, optional explicit names | `interests.md` | Yes — user confirms/modifies |
| `/conversus mode` | Select competition mode | `problem.md` + `interests.md` | `conversus.yml` | Yes — user confirms/overrides |
| `/conversus converge` | Execute deliberation | `conversus.yml` | `output/` directory | Yes — user confirms before execution |
| `/conversus arbitrate` | Resolve remaining disputes | Completed `output/`, optional arbiter config | `arbitration/resolution.md` | Yes — guides arbiter setup if needed |
| `/conversus run` | Execute from YAML (existing) | `conversus.yml` | `output/` directory | No — direct execution |

## Appendix B: Worked Example

A product manager needs to decide the caching strategy for a healthcare platform.

**Step 1** — `/conversus define`:
> "We need to decide how to cache expensive database queries in our Django backend. Options include Redis query-level caching, Django's built-in cache framework, or replacing the queries entirely with materialized views. The system handles multi-tenant healthcare data with strict latency requirements."

The system produces `problem.md` with type "selection", constraints around multi-tenancy and healthcare compliance, and open questions about cache invalidation strategy.

**Step 2** — `/conversus interests`:

The system suggests three interests:
- **redis-caching**: Advocates for Redis query-level caching. Docs: Redis documentation, existing caching strategy doc.
- **django-cache**: Advocates for Django's built-in cache framework. Docs: Django cache framework docs.
- **materialized-views**: Advocates for PostgreSQL materialized views. Docs: PostgreSQL materialized views docs, Aurora PostgreSQL features.

The PM adds a fourth: **hybrid** — advocates for combining approaches. The system generates a prompt and asks for docs.

**Step 3** — `/conversus mode`:

The system recommends `winner-take-all`: "Your interests are competing approaches to the same problem — only one primary caching strategy should be chosen. Winner-take-all mode will have each approach make its strongest case and attack the others' weaknesses."

The PM overrides to `cooperative`: "Actually, we might combine approaches. Use cooperative." The system explains the trade-off and regenerates the YAML.

**Step 4** — `/conversus converge`:

The system presents: "4 agents, cooperative mode, 1 iteration, estimated 21 agent launches. Proceed?" The PM confirms. The deliberation runs.

**Step 5** — `/conversus arbitrate`:

Two disputes remain: cache invalidation ownership and materialized view refresh timing. The PM sets the arbiter as "the system's latency requirements" grounded in the SLA document. Phase 6 resolves both disputes with binding decisions citing the SLA.

## Appendix C: Relationship to Existing Specs

```
003-decision-framework (this spec)
 │
 │  Guided workflow commands that generate configs and invoke engines
 │
 ├──► 001-subject-arbitration
 │     Phase 6 engine: arbiter schema, execution, templates
 │     /conversus arbitrate delegates to this
 │
 ├──► 002-recursive-rounds
 │     Multi-round engine: rounds field, stagnation, cross-round synthesis
 │     /conversus converge transparently supports this
 │
 └──► SKILL.md (existing)
       Phase 1-5 engine: /conversus run execution
       /conversus converge delegates to this
```

The decision framework is the user-facing layer. The three specs below it are the engine layer. The framework generates configurations; the engines execute them.
