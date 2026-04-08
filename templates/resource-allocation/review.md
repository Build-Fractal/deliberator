# Resource Allocation Review — Phase 1: Demand Statement

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you state your demand for resources from a shared pool. Your goal is to justify your allocation needs with evidence and demonstrate why your demand should be prioritized.

## What to Read

1. **Target files** (the resource pool definition and constraints — read ALL of these):
{TARGET_FILES}

2. **Your documentation** (your grounding material — read all of these thoroughly):
{AGENT_DOCS}

{PRIOR_FILES_SECTION}

{PRIOR_ROUND_SECTION}

{PRIOR_ARBITRATION_SECTION}

Read every file listed above before writing your demand statement. Your claims must be grounded in your actual documentation. Cite exact file paths and line numbers when referencing your docs.

## What to Produce

Write your demand statement to: `{OUTPUT_PATH}`

Your demand statement must contain the following sections in this exact order:

---

### Resource Demand

State your resource requirements. For each resource type in the pool:

- **[Resource type]**: Quantity requested, with justification.
  - **Minimum viable**: The absolute minimum you need to function.
  - **Optimal**: What you would use if unconstrained.
  - **Marginal value**: What each additional unit beyond minimum delivers, with evidence from `[doc-file, L##-##]`.

### Impact Case

Why your demand should be prioritized. 4-6 items:

- **[Impact label]**: What outcome your allocation enables, quantified where possible. Reference your documentation: `[doc-file, L##-##]`. Classify impact as: critical (system fails without this) | high (significant degradation) | medium (noticeable but manageable).

### Efficiency Analysis

How efficiently you use allocated resources:

- **Utilization rate**: How much of your current allocation you actually use, with evidence.
- **Output per unit**: What each unit of resource produces, benchmarked against alternatives if possible.
- **Waste reduction**: How you minimize waste in your current allocation.

### Dependencies

Resources that other demand sources need to deliver for your allocation to have maximum impact:

- **[Dependency label]**: What you need from [other agent], why, and what happens if it is not available.

### Fairness Argument

Why your proposed allocation is fair relative to others:

- **Shapley contribution**: Your contribution to the overall outcome — what value would be lost if you received zero allocation.
- **Proportionality**: Why your share is proportional to your contribution or need.

---

## Rules

- **Justify every unit.** Do not request resources you cannot justify with evidence. Inflated demands will be challenged in cross-review.
- **Evidence over assertion.** Every claim must reference either the target document or your documentation.
- **Acknowledge the constraint.** The pool is finite. Show that you understand the trade-offs your demand creates for others.
- **Be specific.** "We need more resources" is not a demand. State exact quantities and what each unit delivers.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate.
