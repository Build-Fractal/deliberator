# Feature Specification: Preset Agents

**Feature ID**: `004-preset-agents`
**Created**: 2026-03-19
**Status**: Draft
**Depends On**: None (enhances existing agent definition; orthogonal to 001/002/003)

---

## 1. Feature Summary

Every `conversus.yml` written so far duplicates agent definitions. The Mechanist, Pragmatist, and Purist appear identically in `001-subject-arbitration/dispute-resolution/conversus.yml`. The APM, spec-kit, and gh-aw agents appear identically in `conversus.example.yml` and the self-review config. The agents-md, agentskills, and apm auditor agents exist only in `self-review/conversus.yml` but would be reusable for any agent-package self-review.

This spec introduces **preset agents** -- pre-defined agent personalities stored as YAML files in a `presets/` directory that can be referenced by name in any `conversus.yml`. Presets eliminate prompt duplication, establish a reusable vocabulary of deliberation perspectives, and enable composition (combining a philosophy preset with a tool preset).

**What changes**: A new `presets/` directory with categorized agent definitions. A `preset:` field on agent entries in `conversus.yml` that resolves to a stored definition. A composition mechanism for layering presets. Preset-bundled `docs` paths with override capability.

**What does not change**: Inline agent definitions (`name` + `prompt` + `docs`) continue to work exactly as today. The execution engine (SKILL.md Phases 1-6) is untouched. Templates, modes, iterations, rounds, and arbitration are unaffected.

---

## 2. Motivation

### The Problem

Agent definitions in conversus are verbose and repetitive. A typical agent entry is 5-15 lines of YAML containing an identity prompt, documentation paths, and optionally a role. When the same conceptual agent (e.g., "The Mechanist" or "APM") participates in multiple deliberations, its definition is copy-pasted across `conversus.yml` files. This creates three problems:

1. **Drift**: Copy-pasted prompts diverge over time. The Mechanist prompt in one spec may emphasize different aspects than in another, not because the user intended a different personality, but because edits accumulated independently.

2. **Barrier to entry**: Spec-003 (Decision Framework) introduces guided workflow commands that generate `conversus.yml` files. The `/conversus interests` command must generate agent identity prompts from scratch every time. With presets, the system can suggest existing personalities ("Would you like to use the Mechanist, Pragmatist, and Purist for this spec review?") instead of generating new ones.

3. **No institutional knowledge**: The project has developed effective agent archetypes through real deliberation runs -- the three philosophers (Mechanist/Pragmatist/Purist), the three tool advocates (APM/spec-kit/gh-aw), the three standards auditors (agents-md/agentskills/apm). These archetypes exist only as inline YAML. There is no way to share, version, or discover them.

### The Insight

Agent presets are analogous to character sheets in tabletop RPGs. A character sheet defines identity, capabilities, and equipment. The game master (the `conversus.yml`) assigns characters to a scenario and sets the rules (mode, target, iterations). The character's personality is stable across scenarios; the scenario changes.

The critical design decision: presets must be **composable**. A "Mechanist + APM" agent is not just a Mechanist who happens to know about APM -- it is a Mechanist whose verification-first philosophy is grounded in APM's packaging and distribution domain. Composition produces emergent identity, not concatenation.

---

## 3. User Stories

### US-1: Reference a Preset by Name (Priority: P1)

As a user configuring a `conversus.yml`, I want to reference a pre-defined agent by name instead of writing an inline prompt, so that I can reuse established agent personalities without duplication.

**Acceptance Criteria**:

1. **Given** a preset file exists at `presets/philosophy/mechanist.yml`, **When** a `conversus.yml` contains `preset: mechanist`, **Then** the engine resolves the preset by searching the `presets/` directory tree for a file named `mechanist.yml`, loads its `prompt` and `docs` fields, and uses them as the agent definition.

2. **Given** `preset: mechanist` is specified and the preset file defines `docs: [path/to/docs]`, **When** the agent is resolved, **Then** the preset's docs paths are used. If the `conversus.yml` agent entry also specifies `docs:`, the inline docs REPLACE the preset docs (explicit override, not merge).

3. **Given** `preset: nonexistent` is specified, **When** validation runs, **Then** it fails with error: "Preset 'nonexistent' not found. Available presets: mechanist, pragmatist, purist, ..."

4. **Given** an agent entry has BOTH `preset: mechanist` AND an inline `prompt:`, **When** the config is parsed, **Then** the inline `prompt` OVERRIDES the preset prompt. The preset serves as a base; inline fields take precedence. This allows surgical customization: "Use the Mechanist but with this specific tweak."

5. **Given** an agent entry has ONLY `preset: mechanist` with no other fields except `name:`, **When** the config is parsed, **Then** the agent is fully defined by the preset. The `name` field is required on the agent entry (it is the agent's identity in this specific run, which may differ from the preset name).

6. **Given** a preset file at `presets/philosophy/mechanist.yml`, **When** another preset exists at `presets/tool/mechanist.yml`, **Then** validation fails with error: "Ambiguous preset 'mechanist' found in multiple categories: philosophy/mechanist.yml, tool/mechanist.yml. Use the qualified name: 'philosophy/mechanist' or 'tool/mechanist'."

7. **Given** the user specifies `preset: philosophy/mechanist`, **When** the preset is resolved, **Then** the engine looks for `presets/philosophy/mechanist.yml` directly (qualified path, no search).

---

### US-2: Compose Multiple Presets (Priority: P1)

As a user configuring a deliberation, I want to combine a philosophy preset with a domain preset so that the agent has both a reasoning style and domain expertise.

**Acceptance Criteria**:

1. **Given** an agent entry with `preset: [mechanist, apm]`, **When** the config is parsed, **Then** the engine loads both presets and composes them. The composed prompt is constructed by the engine using both presets' prompts (see Section 5 for composition rules). The composed docs are the union of both presets' docs lists.

2. **Given** `preset: [mechanist, apm]`, **When** the composed agent is used in a deliberation, **Then** the agent's identity reflects BOTH presets: it applies mechanist reasoning (deterministic, machine-verifiable) to APM's domain (packaging, distribution, compilation). The composed prompt is not a naive concatenation -- it instructs the agent to apply the philosophy preset's reasoning style to the domain preset's subject matter.

3. **Given** `preset: [mechanist, apm]` and an inline `prompt:` override, **When** the config is parsed, **Then** the inline prompt replaces the composed prompt entirely. Composition happens first; inline override happens second.

4. **Given** `preset: [mechanist, apm]` where both presets define `docs`, **When** docs are resolved, **Then** the docs lists are merged (union, preserving order: first preset's docs, then second preset's docs, deduplicated).

5. **Given** `preset: [apm, mechanist]` (reversed order), **When** composition runs, **Then** the result is semantically different from `[mechanist, apm]`. The first preset in the list is the **primary identity** (what the agent IS), and subsequent presets are **modifiers** (how the agent reasons or what domain it applies to). `[apm, mechanist]` means "an APM advocate who reasons like a Mechanist." `[mechanist, apm]` means "a Mechanist philosopher applied to the APM domain." The distinction matters for prompt construction.

6. **Given** `preset: [red-team, security, apm]` (three presets), **When** composition runs, **Then** all three are composed. The first is primary identity, subsequent are modifiers applied in order. Maximum composition depth is 3 presets. Validation rejects lists longer than 3 with error: "Maximum 3 presets per composition. Simplify or use an inline prompt."

---

### US-3: Discover Available Presets (Priority: P2)

As a user setting up a deliberation, I want to see what presets are available so that I can choose the right agents without reading source files.

**Acceptance Criteria**:

1. **Given** the user runs `/conversus presets`, **When** the command executes, **Then** it lists all available presets grouped by category, showing each preset's name, category, and one-line description.

2. **Given** the user runs `/conversus presets --category philosophy`, **When** the command executes, **Then** it shows only philosophy presets with their full descriptions and example usage.

3. **Given** the user runs `/conversus presets --show mechanist`, **When** the command executes, **Then** it displays the full preset definition: name, description, category, prompt, docs, and tags. It also shows an example `conversus.yml` snippet using that preset.

4. **Given** a preset file lacks a `description` field, **When** the preset is listed, **Then** the listing shows "(no description)" and emits a warning: "Preset 'name' is missing a description field."

---

### US-4: Create Custom Presets (Priority: P2)

As a user who has developed effective agent prompts through deliberation, I want to save them as reusable presets so that future deliberations can use them without re-engineering the prompt.

**Acceptance Criteria**:

1. **Given** the user runs `/conversus presets --save my-architect --from conversus-output/mechanist/review.md`, **When** the command processes, **Then** it extracts the agent's identity from the specified run, generates a preset file at `presets/custom/my-architect.yml`, and asks the user to confirm the description and tags.

2. **Given** the user creates a preset file manually at `presets/custom/my-preset.yml`, **When** the file follows the preset schema (Section 4), **Then** it is discoverable by name and usable via `preset: my-preset`.

3. **Given** a custom preset file has invalid YAML or missing required fields, **When** validation runs (at discovery time or config parse time), **Then** it fails with a specific error: "Preset 'name' at path/to/file.yml is invalid: missing required field 'prompt'."

---

### US-5: Preset-Aware Guided Workflow (Priority: P2)

As a user of the `/conversus interests` command (spec-003), I want the system to suggest relevant presets instead of generating prompts from scratch, so that deliberations use battle-tested agent personalities.

**Acceptance Criteria**:

1. **Given** the user runs `/conversus interests` and the problem type is "integration" with interests that map to known tools (APM, spec-kit, gh-aw), **When** the system suggests agents, **Then** it offers the matching tool presets: "I found presets matching your interests: `apm`, `spec-kit`, `gh-aw`. Use these?" The generated `interests.md` references the presets.

2. **Given** the user runs `/conversus interests` for a spec review, **When** the system suggests agents, **Then** it offers the philosophy presets: "For spec review, the Mechanist/Pragmatist/Purist trio covers verification, practicality, and completeness perspectives. Use these?"

3. **Given** the system suggests presets but the user declines, **When** the user provides custom descriptions, **Then** the system generates inline prompts as today (spec-003 behavior). Presets are suggestions, never requirements.

4. **Given** the generated `interests.md` references presets, **When** `/conversus mode` generates the `conversus.yml`, **Then** the agent entries use `preset:` references instead of inline prompts.

---

### US-6: Preset Interaction with Arbiter (Priority: P2)

As a user configuring a subject arbiter, I want to use a preset for the arbiter so that standard arbitration philosophies are reusable.

**Acceptance Criteria**:

1. **Given** a preset file at `presets/role/balanced-arbiter.yml`, **When** the `conversus.yml` arbiter section specifies `preset: balanced-arbiter`, **Then** the arbiter's prompt is loaded from the preset. The `grounding` and `trigger` fields must still be specified inline (they are run-specific, not personality-specific).

2. **Given** an arbiter with `preset: balanced-arbiter` and inline `prompt:`, **When** the config is parsed, **Then** the inline prompt overrides the preset prompt (same override semantics as regular agents).

3. **Given** an arbiter preset, **When** the preset defines `docs`, **Then** the preset docs are used as the arbiter's default docs. Inline `docs` on the arbiter entry overrides (replaces) the preset docs.

---

## 4. Data Model

### 4.1 Preset File Format

Each preset is a YAML file with the following schema:

```yaml
# presets/{category}/{name}.yml
name: mechanist                        # required: identifier (must match filename)
description: >-                        # required: one-line description for discovery
  Deterministic, machine-verifiable, minimal-commitment reasoning.
  If a machine can't check it, it doesn't belong.
category: philosophy                   # required: must match parent directory name
tags:                                  # optional: for search and filtering
  - verification
  - formal
  - minimal

prompt: |                              # required: the agent identity prompt
  You are The Mechanist. You believe in deterministic, machine-verifiable,
  minimal-commitment specifications. If a machine can't check it, it doesn't
  belong in the spec. Engine validation is the only reliable enforcement surface.

docs:                                  # optional: default documentation paths
  - conversus/references/mechanist-principles.md

composable: true                       # optional: whether this preset can be
                                       # combined with others (default: true)
```

**Required fields**: `name`, `description`, `category`, `prompt`.

**Optional fields**: `tags`, `docs`, `composable`.

**Filename convention**: The filename (without extension) MUST match the `name` field. The file MUST be placed in the directory matching its `category` field. `presets/philosophy/mechanist.yml` has `name: mechanist` and `category: philosophy`.

### 4.2 Directory Structure

```
conversus/
├── presets/
│   ├── philosophy/           # Reasoning style presets
│   │   ├── mechanist.yml
│   │   ├── pragmatist.yml
│   │   └── purist.yml
│   ├── tool/                 # Tool/ecosystem advocate presets
│   │   ├── apm.yml
│   │   ├── spec-kit.yml
│   │   └── gh-aw.yml
│   ├── standard/             # Standards auditor presets
│   │   ├── agents-md.yml
│   │   ├── agentskills.yml
│   │   └── apm-auditor.yml
│   ├── role/                 # Structural role presets
│   │   ├── red-team.yml
│   │   ├── blue-team.yml
│   │   ├── balanced-arbiter.yml
│   │   └── devils-advocate.yml
│   ├── domain/               # Domain expertise presets
│   │   ├── security.yml
│   │   ├── performance.yml
│   │   ├── ux.yml
│   │   ├── accessibility.yml
│   │   └── cost.yml
│   └── custom/               # User-created presets (gitignored by default)
│       └── .gitkeep
├── templates/
├── specs/
├── ...
```

### 4.3 Preset Categories

| Category | Purpose | Example Presets | Typical Use |
|---|---|---|---|
| `philosophy` | Reasoning style -- HOW the agent thinks | mechanist, pragmatist, purist | Spec review, architecture decisions |
| `tool` | Tool/ecosystem advocacy -- WHAT the agent represents | apm, spec-kit, gh-aw | Ecosystem integration, tool selection |
| `standard` | Standards compliance audit -- WHAT the agent checks against | agents-md, agentskills, apm-auditor | Self-review, compliance checking |
| `role` | Structural deliberation role -- WHERE the agent sits | red-team, blue-team, balanced-arbiter, devils-advocate | Red-blue mode, arbitration, stress tests |
| `domain` | Domain expertise -- WHAT concerns the agent prioritizes | security, performance, ux, accessibility, cost | Architecture review, cross-cutting concerns |
| `custom` | User-created project-specific presets | (user-defined) | Project-specific recurring agents |

**Category is closed for built-in presets.** The five built-in categories (philosophy, tool, standard, role, domain) are the canonical set. New categories require a spec amendment. The `custom/` directory is the escape hatch for project-specific presets that do not fit existing categories.

### 4.4 Schema Changes to `conversus.yml`

The agent entry schema is extended with an optional `preset` field:

```yaml
agents:
  # Option 1: Inline definition (existing, unchanged)
  - name: my-agent
    prompt: |
      You are a custom agent...
    docs:
      - path/to/docs/

  # Option 2: Preset reference (new)
  - name: the-mechanist
    preset: mechanist

  # Option 3: Preset with overrides (new)
  - name: strict-mechanist
    preset: mechanist
    prompt: |
      You are The Mechanist, but with extra emphasis on formal verification.
      Every claim must be backed by a proof or a test.
    docs:
      - path/to/custom-docs/

  # Option 4: Composed presets (new)
  - name: mechanist-apm
    preset: [mechanist, apm]

  # Option 5: Composed presets with overrides (new)
  - name: mechanist-apm-strict
    preset: [mechanist, apm]
    docs:
      - path/to/additional-docs/

  # Option 6: Preset with role (for red-blue mode)
  - name: red-security
    preset: [red-team, security]
    role: red
```

**Arbiter preset support:**

```yaml
arbiter:
  name: my-arbiter
  preset: balanced-arbiter        # loads prompt (and docs if defined)
  grounding: path/to/constitution.md   # always required inline
  trigger: disputes_remain             # always required inline
```

### 4.5 Resolution Rules

When an agent entry is parsed, fields are resolved in this order:

1. **Load preset(s)**: If `preset` is specified, load the preset file(s). If a list, compose them (Section 5).
2. **Apply inline overrides**: Any field specified inline on the agent entry overrides the corresponding preset field.
3. **Validate**: The resolved agent must have a `name` and a `prompt`. `docs` is optional.

**Field-level override semantics:**

| Field | Preset provides | Inline provides | Result |
|---|---|---|---|
| `prompt` | Yes | No | Preset prompt |
| `prompt` | Yes | Yes | Inline prompt (override) |
| `prompt` | No | Yes | Inline prompt |
| `prompt` | No | No | Validation error |
| `docs` | Yes | No | Preset docs |
| `docs` | Yes | Yes | Inline docs (override, not merge) |
| `docs` | No | Yes | Inline docs |
| `docs` | No | No | No docs (valid) |
| `role` | N/A | Yes/No | Always inline (presets do not define role) |

**Why override, not merge, for `docs`**: Merging creates hidden dependencies. If the preset's docs change, every run that uses the preset silently picks up new documentation. Override semantics give the user explicit control: use the preset's docs (omit inline docs) or bring your own (specify inline docs). This matches the principle of least surprise.

---

## 5. Composition Model

### 5.1 Composition Semantics

When `preset: [A, B]` is specified:

- **A** is the **primary identity**: what the agent IS.
- **B** is the **modifier**: how the agent reasons or what domain it applies to.

For `preset: [A, B, C]`:
- **A** is the primary identity.
- **B** is the first modifier.
- **C** is the second modifier.

### 5.2 Prompt Composition

The engine constructs a composed prompt using a fixed template:

```
You are {A.name} applied to {B.name}'s domain.

PRIMARY IDENTITY:
{A.prompt}

DOMAIN/MODIFIER:
{B.prompt}

YOUR COMBINED ROLE:
Apply the reasoning style, principles, and priorities defined in your
primary identity to the subject matter and domain expertise of your
modifier(s). When your primary identity's principles conflict with your
modifier's domain conventions, state the conflict explicitly rather than
silently resolving it.
```

For three presets (`[A, B, C]`):

```
You are {A.name} applied to {B.name}'s domain with {C.name}'s concerns.

PRIMARY IDENTITY:
{A.prompt}

FIRST MODIFIER:
{B.prompt}

SECOND MODIFIER:
{C.prompt}

YOUR COMBINED ROLE:
Apply the reasoning style, principles, and priorities defined in your
primary identity to the subject matter of your first modifier, while
keeping your second modifier's concerns as a persistent evaluation lens.
When principles conflict across your presets, state the conflict
explicitly rather than silently resolving it.
```

### 5.3 Docs Composition

Docs lists are concatenated in preset order and deduplicated:

```
composed_docs = deduplicate(A.docs + B.docs + C.docs)
```

Deduplication preserves first occurrence. If A and B both list `path/to/shared.md`, it appears once (from A's position).

### 5.4 Composition Constraints

- **Maximum 3 presets per composition.** More than 3 produces prompt bloat and diluted identity. Validation rejects lists longer than 3.
- **`composable: false` blocks composition.** A preset may declare `composable: false` to prevent use in multi-preset lists. Attempting to compose a non-composable preset produces: "Preset 'X' is not composable. Use it alone or with an inline prompt override."
- **Role presets should be primary.** Presets in the `role` category (red-team, blue-team, balanced-arbiter) have structural significance and should typically be the primary identity in a composition (first in the list). The engine does not enforce this -- it is guidance.
- **Philosophy + domain is the canonical composition.** The most common composition pattern is `[philosophy, domain]` or `[philosophy, tool]`. Example: `[mechanist, security]` produces a security reviewer who demands machine-verifiable evidence for every claim.

### 5.5 Composition Examples

| Preset List | Meaning | Use Case |
|---|---|---|
| `[mechanist, apm]` | Mechanist reasoning applied to APM's domain | Reviewing APM-related specs with verification focus |
| `[pragmatist, security]` | Pragmatist approach to security concerns | Security review that balances ideal vs. practical |
| `[red-team, performance]` | Red team attacker focused on performance | Performance stress-testing in red-blue mode |
| `[blue-team, security]` | Blue team defender with security expertise | Defending architecture against security attacks |
| `[purist, agents-md]` | Purist completeness applied to AGENTS.md standard | Rigorous standards compliance audit |
| `[devils-advocate, cost]` | Contrarian focused on cost implications | Challenging expensive architectural decisions |

---

## 6. Built-in Presets

### 6.1 Philosophy Presets

**mechanist.yml**
```yaml
name: mechanist
description: >-
  Deterministic, machine-verifiable, minimal-commitment reasoning.
  If a machine can't check it, it doesn't belong.
category: philosophy
tags: [verification, formal, minimal]
prompt: |
  You are The Mechanist. You believe in deterministic, machine-verifiable,
  minimal-commitment specifications. If a machine can't check it, it doesn't
  belong in the spec. Engine validation is the only reliable enforcement surface.
```

**pragmatist.yml**
```yaml
name: pragmatist
description: >-
  Ship working software with practical tradeoffs. Perfect is the enemy of good.
category: philosophy
tags: [practical, shipping, tradeoffs]
prompt: |
  You are The Pragmatist. You believe in shipping working software with
  practical tradeoffs. Template instructions are the real enforcement surface.
  Perfect is the enemy of good -- resolve blockers with lowest regret.
```

**purist.yml**
```yaml
name: purist
description: >-
  Specification completeness, formal correctness, and explicit contracts.
category: philosophy
tags: [completeness, correctness, contracts]
prompt: |
  You are The Purist. You believe in specification completeness, formal
  correctness, and explicit contracts. A spec without success criteria for
  every FR is incomplete. Every enforcement surface should be covered.
```

### 6.2 Tool Presets

**apm.yml**
```yaml
name: apm
description: >-
  Agent Package Manager advocate. Packaging, distribution, context compilation,
  and agent primitives.
category: tool
tags: [packaging, distribution, compilation, agents]
prompt: |
  You are APM (Agent Package Manager). You represent the perspective
  of packaging, distribution, context compilation, and agent primitives.
docs:
  - apm/docs/
  - apm/README.md
```

**spec-kit.yml**
```yaml
name: spec-kit
description: >-
  Spec-kit SDD framework advocate. Extension system, commands, hooks,
  templates, and configuration.
category: tool
tags: [specification, sdd, extensions, templates]
prompt: |
  You are spec-kit (the SDD framework). You represent the extension system,
  commands, hooks, templates, and configuration.
docs:
  - spec-kit/README.md
  - spec-kit/templates/
  - spec-kit/extensions/
```

**gh-aw.yml**
```yaml
name: gh-aw
description: >-
  GitHub Agentic Workflows advocate. CI dispatch, workflow automation,
  repo-memory, and concurrency.
category: tool
tags: [ci, workflows, automation, github]
prompt: |
  You are gh-aw (GitHub Agentic Workflows). You represent CI dispatch,
  workflow automation, repo-memory, and concurrency.
docs:
  - gh-aw/docs/
  - gh-aw/README.md
```

### 6.3 Standard Presets

**agents-md.yml**
```yaml
name: agents-md
description: >-
  AGENTS.md standard auditor. Checks package discoverability and
  structure for AGENTS.md-compatible agents.
category: standard
tags: [agents-md, discoverability, structure]
prompt: |
  You are an expert in the AGENTS.md standard. Is this package structured
  so that any AGENTS.md-compatible agent can discover and use it?
docs:
  - conversus/references/agents-md.md
```

**agentskills.yml**
```yaml
name: agentskills
description: >-
  Agent Skills specification auditor. Checks SKILL.md conformance
  and description optimization for discovery.
category: standard
tags: [agentskills, skills, discovery]
prompt: |
  You are an expert in the Agent Skills specification. Does the SKILL.md
  conform to the spec? Are descriptions optimized for discovery?
docs:
  - conversus/references/agentskills-spec.md
  - conversus/references/agentskills-best-practices.md
```

**apm-auditor.yml**
```yaml
name: apm-auditor
description: >-
  APM package auditor. Checks apm.yml correctness and compatibility
  with apm install/compile.
category: standard
tags: [apm, manifest, packaging, audit]
prompt: |
  You are APM (Agent Package Manager). Is the apm.yml correct? Does the
  package structure work with apm install/compile?
docs:
  - apm/docs/src/content/docs/reference/manifest-schema.md
  - apm/docs/src/content/docs/guides/skills.md
```

### 6.4 Role Presets

**red-team.yml**
```yaml
name: red-team
description: >-
  Adversarial attacker. Finds every flaw, risk, failure mode, and edge case.
  Assumes the worst. Proves it.
category: role
tags: [adversarial, attack, risk, security]
prompt: |
  You are a Red Team attacker. Your job is to find every flaw, risk, failure
  mode, and edge case in the proposal. Assume the worst-case scenario for
  every design decision. Do not suggest fixes -- only expose vulnerabilities.
  Every claim must be backed by a concrete attack scenario or failure path.
```

**blue-team.yml**
```yaml
name: blue-team
description: >-
  Architecture defender. Justifies design decisions with evidence, not
  dismissal. Concedes genuine vulnerabilities.
category: role
tags: [defense, architecture, justification]
prompt: |
  You are a Blue Team defender. Your job is to justify the design decisions
  in the proposal with evidence, not dismissal. When an attack is valid,
  concede it and propose a mitigation. When an attack is based on a
  misunderstanding, correct it with specific references to the design.
  Never dismiss a concern without evidence.
```

**balanced-arbiter.yml**
```yaml
name: balanced-arbiter
description: >-
  Impartial arbiter who weighs all perspectives equally.
  Issues binding decisions grounded in declared principles.
category: role
tags: [arbiter, impartial, binding, decisions]
composable: false
prompt: |
  You are a balanced arbiter who considers all perspectives equally.
  Issue binding decisions on remaining disputes grounded in the
  declared decision framework. Every ruling must cite a specific
  principle from the grounding document. Do not favor any single
  agent's perspective -- evaluate arguments on evidence and alignment
  with the grounding principles.
```

**devils-advocate.yml**
```yaml
name: devils-advocate
description: >-
  Contrarian who challenges the strongest consensus positions.
  Forces teams to defend their assumptions.
category: role
tags: [contrarian, challenge, assumptions]
prompt: |
  You are the Devil's Advocate. Your job is to challenge the positions
  that appear most agreed-upon. When everyone converges on an approach,
  find the strongest argument against it. You are not opposed to the
  proposal -- you are opposed to unchallenged assumptions. If a position
  survives your challenge, it is stronger. If it does not, it was not
  ready.
```

### 6.5 Domain Presets

**security.yml**
```yaml
name: security
description: >-
  Security-focused reviewer. Authentication, authorization, data protection,
  threat modeling, and compliance.
category: domain
tags: [security, auth, threats, compliance, data-protection]
prompt: |
  You evaluate proposals through a security lens. Your concerns are:
  authentication and authorization correctness, data protection and
  privacy (especially PII/PHI in healthcare), threat modeling for
  the described architecture, injection and input validation, secrets
  management, and compliance with relevant standards. Every security
  concern must include a concrete threat scenario, not abstract warnings.
```

**performance.yml**
```yaml
name: performance
description: >-
  Performance-focused reviewer. Latency, throughput, resource efficiency,
  scalability, and bottleneck analysis.
category: domain
tags: [performance, latency, scalability, throughput]
prompt: |
  You evaluate proposals through a performance lens. Your concerns are:
  latency at the 50th, 95th, and 99th percentiles; throughput under
  expected and peak load; resource efficiency (CPU, memory, I/O, network);
  scalability characteristics (linear, sublinear, superlinear); and
  identification of bottlenecks. Every performance concern must include
  an estimated impact magnitude, not just "this could be slow."
```

**ux.yml**
```yaml
name: ux
description: >-
  User experience reviewer. Usability, cognitive load, error recovery,
  information architecture, and workflow efficiency.
category: domain
tags: [ux, usability, cognitive-load, workflows]
prompt: |
  You evaluate proposals through a user experience lens. Your concerns are:
  cognitive load on the user (how many concepts must they hold simultaneously),
  error recovery paths (what happens when users make mistakes), information
  architecture (can users find what they need), workflow efficiency (how many
  steps to accomplish a task), and consistency with existing patterns the user
  already knows. Every UX concern must reference a concrete user scenario.
```

**accessibility.yml**
```yaml
name: accessibility
description: >-
  Accessibility reviewer. WCAG compliance, assistive technology support,
  inclusive design, and cognitive accessibility.
category: domain
tags: [accessibility, wcag, assistive-tech, inclusive-design]
prompt: |
  You evaluate proposals through an accessibility lens. Your concerns are:
  WCAG 2.1 AA compliance, screen reader and assistive technology compatibility,
  keyboard navigation, color contrast and visual design for low vision,
  cognitive accessibility (clear language, predictable navigation), and
  internationalization. Every accessibility concern must cite a specific
  WCAG criterion or assistive technology interaction pattern.
```

**cost.yml**
```yaml
name: cost
description: >-
  Cost-focused reviewer. Infrastructure spend, operational overhead,
  build-vs-buy economics, and total cost of ownership.
category: domain
tags: [cost, infrastructure, economics, tco]
prompt: |
  You evaluate proposals through a cost lens. Your concerns are:
  infrastructure spend (compute, storage, network, managed services),
  operational overhead (maintenance hours, on-call burden, monitoring),
  build-vs-buy economics (development cost vs. vendor pricing over 1-3 years),
  and total cost of ownership including hidden costs (migration, training,
  lock-in). Every cost concern must include an order-of-magnitude estimate
  or a comparison to a known baseline.
```

---

## 7. Preset Resolution Algorithm

### 7.1 Search Path

When `preset: name` is specified, the engine resolves it as follows:

1. **Qualified path**: If `name` contains a `/` (e.g., `philosophy/mechanist`), look for `presets/{name}.yml` directly. If not found, fail.

2. **Unqualified search**: If `name` has no `/`, search all category directories under `presets/` for a file named `{name}.yml`.
   - If exactly one match: use it.
   - If zero matches: fail with "Preset '{name}' not found."
   - If multiple matches: fail with "Ambiguous preset '{name}' found in: {paths}. Use a qualified name."

3. **Preset root**: The `presets/` directory is located relative to the conversus package root (the directory containing `SKILL.md`). The engine finds this root using the same walk-up mechanism it uses to find `templates/`.

### 7.2 Validation

After resolution, validate:

- `name` field matches the filename.
- `category` field matches the parent directory name.
- `prompt` field is non-empty.
- `description` field is present.
- If `docs` are specified, each path exists on disk (same validation as inline docs).
- If `composable: false` and the preset appears in a multi-preset list, fail.

### 7.3 Caching

Preset files are read once per conversus run and cached in memory. A preset referenced by multiple agents (e.g., two agents both compose with `security`) reads the file once.

---

## 8. Interaction with Existing Features

### 8.1 Modes

Presets are mode-agnostic. Any preset can be used in any mode. The mode's templates control how the agent's prompt is framed within the deliberation context. A `security` preset used in `cooperative` mode advocates for security integration; the same preset in `red-blue` mode acts as a domain-specific attacker or defender (depending on the `role` field on the agent entry).

### 8.2 Prior Context

Preset-defined `docs` paths are resolved and validated alongside inline `docs` paths during config parsing. Prior context (`prior:` field) is separate from agent docs and is not affected by presets.

### 8.3 Iterations and Rounds

Presets define agent identity. Iterations (spec-002 `iterations` field) and rounds (spec-002 `rounds` field) control execution depth. These are orthogonal -- a preset agent participates in as many iterations and rounds as configured.

### 8.4 Arbiter

Presets can be used for the arbiter's prompt and docs (US-6). The `grounding` and `trigger` fields remain required inline because they are run-specific, not personality-specific. A balanced-arbiter preset provides a reusable arbitration philosophy; the grounding document anchors it to a specific decision framework.

### 8.5 Decision Framework (Spec-003)

The `/conversus interests` command benefits directly from presets (US-5). Instead of generating prompts from scratch, the guided workflow can suggest matching presets. The `/conversus mode` command generates `conversus.yml` entries with `preset:` references when presets were selected during the interests phase.

### 8.6 Templates

Templates are unaffected. The template system sees a resolved agent with a `name`, `prompt`, and `docs` -- it does not know or care whether those came from a preset, inline definition, or composition. Resolution happens at config parse time (Step 1 in SKILL.md), before template loading (Step 3).

---

## 9. Example Configurations

### 9.1 Spec Review with Philosophy Presets

```yaml
mode: cooperative
target: specs/005-new-feature/spec.md
output: specs/005-new-feature/conversus/
iterations: 1

agents:
  - name: the-mechanist
    preset: mechanist

  - name: the-pragmatist
    preset: pragmatist

  - name: the-purist
    preset: purist

arbiter:
  name: the-spec
  preset: balanced-arbiter
  grounding: specs/005-new-feature/constitution.md
  trigger: disputes_remain
```

### 9.2 Ecosystem Integration with Tool Presets

```yaml
mode: cooperative
target: specs/001-speckit-orchestrator/spec.md
output: specs/001-speckit-orchestrator/conversus/

agents:
  - name: apm
    preset: apm

  - name: spec-kit
    preset: spec-kit

  - name: gh-aw
    preset: gh-aw
```

### 9.3 Composed Presets for Security Review

```yaml
mode: red-blue
target: docs/architecture/api-gateway.md
output: docs/architecture/api-gateway-conversus/

agents:
  - name: security-attacker
    preset: [red-team, security]
    role: red

  - name: performance-attacker
    preset: [red-team, performance]
    role: red

  - name: architecture-defender
    preset: blue-team
    role: blue
    docs:
      - aws/cdk/
      - infra-cloudformation/
```

### 9.4 Self-Review with Standard Presets (replaces current self-review/conversus.yml)

```yaml
mode: prisoners-dilemma
target: conversus/SKILL.md
output: conversus/self-review/
iterations: 1

agents:
  - name: agents-md
    preset: agents-md
    docs:
      - conversus/AGENTS.md

  - name: agentskills
    preset: agentskills
    docs:
      - conversus/SKILL.md

  - name: apm
    preset: apm-auditor
    docs:
      - conversus/apm.yml
```

### 9.5 Mixed Inline and Preset Agents

```yaml
mode: cooperative
target: specs/006-caching/spec.md
output: specs/006-caching/conversus/

agents:
  - name: mechanist-security
    preset: [mechanist, security]

  - name: pragmatist-cost
    preset: [pragmatist, cost]

  - name: domain-expert
    prompt: |
      You are the Clariti platform's caching architect. You have deep knowledge
      of the existing Django ORM query patterns, the multi-tenant schema isolation,
      and the Aurora PostgreSQL read replica topology.
    docs:
      - clariti-snf-be/docs/caching-strategy.md
      - clariti-snf-be/docs/query-patterns.md
```

---

## 10. Requirements

### Functional Requirements

#### Preset Storage and Discovery

- **FR-001**: Presets MUST be stored as YAML files in `conversus/presets/{category}/{name}.yml`.
- **FR-002**: Each preset file MUST contain at minimum: `name`, `description`, `category`, `prompt`.
- **FR-003**: The `name` field MUST match the filename (without `.yml` extension).
- **FR-004**: The `category` field MUST match the parent directory name.
- **FR-005**: The engine MUST support five built-in categories: `philosophy`, `tool`, `standard`, `role`, `domain`, plus a `custom` category for user-created presets.
- **FR-006**: The engine MUST resolve unqualified preset names by searching all category directories. Ambiguous names (found in multiple categories) MUST produce a clear error listing all matches and suggesting qualified names.
- **FR-007**: Qualified preset names (containing `/`) MUST resolve directly to `presets/{qualified-name}.yml`.

#### Schema Extension

- **FR-008**: The `conversus.yml` agent entry schema MUST support an optional `preset` field accepting either a string (single preset) or a list of strings (composition).
- **FR-009**: The `preset` field MUST be usable on the `arbiter` configuration in addition to regular agents.
- **FR-010**: When both `preset` and inline fields are present, inline fields MUST override the resolved preset fields. Override is per-field, not all-or-nothing.
- **FR-011**: An agent entry with `preset` MUST still require a `name` field. The `name` is the agent's identity in this specific run and may differ from the preset name.
- **FR-012**: An agent entry without `preset` MUST work identically to today (backward compatibility). Inline `prompt` + `docs` definition is the existing path.

#### Composition

- **FR-013**: When `preset` is a list, the engine MUST compose the presets. The first preset is the primary identity; subsequent presets are modifiers.
- **FR-014**: Composed prompts MUST be constructed using the composition template defined in Section 5.2. The engine MUST NOT naively concatenate prompts.
- **FR-015**: Composed docs MUST be the deduplicated union of all presets' docs lists, in preset order.
- **FR-016**: Maximum composition depth MUST be 3 presets. Validation MUST reject lists longer than 3.
- **FR-017**: Presets with `composable: false` MUST NOT appear in multi-preset lists. Validation MUST reject this with a clear error.

#### Validation

- **FR-018**: Preset files MUST be validated at discovery time (when first loaded). Invalid presets (missing required fields, name/category mismatch) MUST produce clear errors.
- **FR-019**: Preset `docs` paths MUST be validated at config parse time (same as inline docs). Missing docs paths MUST produce the same error as missing inline docs.
- **FR-020**: After preset resolution and inline override, the resolved agent MUST have a non-empty `prompt`. If neither the preset nor inline provides a prompt, validation MUST fail.
- **FR-021**: The `preset` field MUST be fully optional. Omitting it preserves exact current behavior.

#### Discovery Command

- **FR-022**: A `/conversus presets` command MUST list all available presets grouped by category, showing name, category, and description.
- **FR-023**: `/conversus presets --category {cat}` MUST filter to a single category.
- **FR-024**: `/conversus presets --show {name}` MUST display the full preset definition including prompt text, docs, tags, and an example usage snippet.

---

## 11. Success Criteria

- **SC-001**: A `conversus.yml` using `preset: mechanist` produces identical deliberation behavior to one with the mechanist prompt inlined. The execution engine cannot distinguish preset-resolved agents from inline agents.

- **SC-002**: A `conversus.yml` using `preset: [mechanist, security]` produces an agent whose review output demonstrates both mechanist reasoning (machine-verifiable claims, minimal commitment) AND security domain concerns (threat scenarios, authentication, data protection).

- **SC-003**: The current `self-review/conversus.yml` can be rewritten to use presets with no change in deliberation output structure. The inline agent definitions in the existing file match the preset definitions exactly.

- **SC-004**: The current `specs/001-subject-arbitration/dispute-resolution/conversus.yml` can be rewritten to use `preset: mechanist`, `preset: pragmatist`, `preset: purist` with no change in deliberation behavior.

- **SC-005**: A `conversus.yml` without any `preset` fields works identically to today. Zero regressions.

- **SC-006**: `/conversus presets` lists all built-in presets across all categories. Adding a new `.yml` file to `presets/custom/` makes it immediately discoverable.

- **SC-007**: Inline field overrides on a preset agent work correctly: specifying `docs:` replaces preset docs, specifying `prompt:` replaces preset prompt.

- **SC-008**: Ambiguous preset names produce clear errors that list all matches and suggest qualified names.

---

## 12. Assumptions

- Preset files are small (under 1KB each) and do not create meaningful I/O overhead.
- The `conversus/presets/` directory is co-located with `conversus/templates/` and `conversus/SKILL.md`. The engine's root-finding mechanism (walk up from cwd looking for `conversus/templates/`) also finds `conversus/presets/`.
- Preset prompts are stable across runs. A user who references `preset: mechanist` expects the same personality in every deliberation. Preset file changes between runs are the user's responsibility.
- The composition template (Section 5.2) produces effective combined prompts for LLM agents. This is an empirical assumption that should be validated by running composed-preset deliberations and comparing output quality to hand-crafted combined prompts.
- The `custom/` category directory is gitignored by default in the conversus package distribution but NOT gitignored in project-level `.gitignore`. Projects that want to share custom presets commit them; the conversus package itself does not ship user customizations.

---

## 13. Constraints

- **No runtime preset generation.** Presets are static YAML files on disk. The engine reads them; it does not create or modify them at runtime. The `/conversus presets --save` command (US-4) is a convenience for users; the engine itself only reads.

- **No remote presets.** Presets are local files. No HTTP fetching, no package registry, no git submodule resolution. If a future version wants remote presets, it should use APM's package mechanism (install a preset package, which copies files to `presets/`).

- **No preset inheritance.** Presets do not extend other presets. Composition (`preset: [A, B]`) is the combination mechanism. There is no `extends: mechanist` field. This keeps the resolution model flat and predictable.

- **No preset versioning.** Presets are not versioned. The file on disk is the current version. Version control (git) provides history. If preset versioning becomes necessary, it should be handled through APM's package versioning.

- **Presets do not define `role`.** The `role` field (red/blue for red-blue mode) is always specified on the agent entry in `conversus.yml`, not in the preset. A `red-team` preset defines the attacker personality but does not hardcode `role: red` -- the same preset could theoretically be used in cooperative mode as a constructive critic without a role assignment.

- **Built-in categories are closed.** New categories require a spec amendment. The `custom/` escape hatch handles project-specific needs. This prevents category proliferation.

- **Composition order matters.** `[A, B]` is not the same as `[B, A]`. This is intentional (Section 5.1) and documented, but it is a usability risk. The `/conversus presets` discovery command should include composition guidance.

---

## 14. Implementation Guidance

This section is non-normative.

### 14.1 Migration Path

Existing `conversus.yml` files do not need to change. Presets are additive. The recommended migration is:

1. Ship the `presets/` directory with built-in presets matching the prompts already used in `conversus.example.yml`, `self-review/conversus.yml`, and `specs/001-subject-arbitration/dispute-resolution/conversus.yml`.
2. Update examples and documentation to show preset usage alongside inline usage.
3. Do NOT rewrite existing `conversus.yml` files to use presets -- let users migrate at their own pace.

### 14.2 Preset Quality Bar

A built-in preset should meet these criteria before inclusion:

- Has been used in at least one real conversus deliberation.
- The prompt produces meaningfully different output from other presets in the same category.
- The description accurately predicts the agent's behavior to a user who has never seen the prompt.
- If `docs` are included, the docs are available in the conversus package distribution (not project-specific paths).

### 14.3 APM Package Distribution

When conversus is distributed as an APM package, the `presets/` directory is included in the package. The `custom/` subdirectory is empty (contains only `.gitkeep`). Users add custom presets after installation. APM's `apm.yml` manifest does not need schema changes -- presets are just files in the package.

### 14.4 Future: Preset Packs

A natural extension is preset packs -- APM packages that contain only presets. A `healthcare-presets` pack could provide `hipaa-auditor`, `phi-reviewer`, `clinical-workflow` presets. This is explicitly deferred. The current spec provides the file format and resolution mechanism that makes packs possible without additional engine changes.

---

## Appendix A: Preset Quick Reference

| Preset | Category | One-liner |
|---|---|---|
| `mechanist` | philosophy | Deterministic, machine-verifiable, minimal-commitment |
| `pragmatist` | philosophy | Ship working software, practical tradeoffs |
| `purist` | philosophy | Specification completeness, formal correctness |
| `apm` | tool | APM: packaging, distribution, compilation |
| `spec-kit` | tool | Spec-kit: extensions, commands, templates |
| `gh-aw` | tool | GH-AW: CI dispatch, workflows, repo-memory |
| `agents-md` | standard | AGENTS.md discoverability audit |
| `agentskills` | standard | Agent Skills spec conformance |
| `apm-auditor` | standard | APM manifest and structure audit |
| `red-team` | role | Adversarial attacker |
| `blue-team` | role | Architecture defender |
| `balanced-arbiter` | role | Impartial arbiter (not composable) |
| `devils-advocate` | role | Contrarian challenger |
| `security` | domain | AuthN/AuthZ, threats, compliance |
| `performance` | domain | Latency, throughput, scalability |
| `ux` | domain | Usability, cognitive load, workflows |
| `accessibility` | domain | WCAG, assistive tech, inclusive design |
| `cost` | domain | Infrastructure spend, TCO, build-vs-buy |

## Appendix B: Relationship to Existing Specs

```
004-preset-agents (this spec)
 |
 |  Defines reusable agent personalities referenced by name
 |
 |--- Used by 003-decision-framework
 |     /conversus interests suggests matching presets
 |     /conversus mode generates preset references in YAML
 |
 |--- Used by 001-subject-arbitration
 |     Arbiter config supports preset: for personality
 |     grounding + trigger remain inline (run-specific)
 |
 |--- Used by 002-recursive-rounds
 |     No direct interaction. Preset agents participate
 |     in rounds like inline agents. Orthogonal.
 |
 |--- Used by SKILL.md (existing)
 |     Resolution happens at Step 1 (Parse Config).
 |     Steps 2-5 see resolved agents, not presets.
```

## Appendix C: Composition Template (Normative Reference)

The composition templates referenced in Section 5.2 are the normative specification for how composed prompts are constructed. Implementors MUST use these exact templates (with variable substitution) to ensure consistent composed agent behavior across engine versions.

**Two-preset composition:**

```
You are {A.name} applied to {B.name}'s domain.

PRIMARY IDENTITY:
{A.prompt}

DOMAIN/MODIFIER:
{B.prompt}

YOUR COMBINED ROLE:
Apply the reasoning style, principles, and priorities defined in your
primary identity to the subject matter and domain expertise of your
modifier(s). When your primary identity's principles conflict with your
modifier's domain conventions, state the conflict explicitly rather than
silently resolving it.
```

**Three-preset composition:**

```
You are {A.name} applied to {B.name}'s domain with {C.name}'s concerns.

PRIMARY IDENTITY:
{A.prompt}

FIRST MODIFIER:
{B.prompt}

SECOND MODIFIER:
{C.prompt}

YOUR COMBINED ROLE:
Apply the reasoning style, principles, and priorities defined in your
primary identity to the subject matter of your first modifier, while
keeping your second modifier's concerns as a persistent evaluation lens.
When principles conflict across your presets, state the conflict
explicitly rather than silently resolving it.
```
