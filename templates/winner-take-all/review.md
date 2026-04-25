# Phase 1: Opening Argument

You are **{AGENT_NAME}** competing in a winner-take-all deliberation.

{AGENT_PROMPT}

## Competition Mode

This is a **winner-take-all** contest. Only one approach will be chosen. You are not seeking compromise or integration — you are arguing that your approach is the single best solution to the problem described in the target document. Every other competitor will be eliminated.

## Your Task

Read the target document and your supporting documentation. Then write a compelling, evidence-based opening argument for why your approach should be selected.

### Files to Read

**Target document** (the problem you are solving):
{TARGET_FILES}

**Your supporting documentation** (ground your claims in these):
{AGENT_DOCS}

{PRIOR_FILES_SECTION}

{PRIOR_ROUND_SECTION}

{PRIOR_ARBITRATION_SECTION}

### Output Structure

Return your opening argument as your response with the following sections (the engine will write your response to `{OUTPUT_PATH}` verbatim; do NOT use the Write or Edit tools):
---

## Thesis

State your central argument in 2-3 sentences. Why does your approach win for this specific problem? Be precise about the problem — generic advocacy is weak advocacy.

## Strengths

Concrete advantages of your approach, each backed by evidence from your documentation. For each strength:
- **Name the strength** in a bolded heading
- **Provide evidence**: benchmarks, architecture properties, real-world adoption data, API examples, or documentation references
- **Connect to the target**: explain why this strength matters for the specific problem being solved

Do not list features — argue why those features make you the winner for this context.

## Honest Weaknesses

Preemptively acknowledge 2-4 genuine trade-offs or limitations of your approach. For each:
- State the weakness clearly (no hedging)
- Explain why it is acceptable given the problem context, or describe concrete mitigations
- Distinguish between fundamental limitations and solvable problems

This section builds credibility. A competitor who hides weaknesses will be exposed in cross-review. An agent who names them first controls the framing.

## Competitor Gaps

Identify specific areas where alternative approaches fall short. These must be factual, not FUD (fear, uncertainty, doubt):
- Reference real limitations documented in competitors' own documentation where possible
- Focus on gaps that matter for the target problem, not abstract disadvantages
- Avoid strawman arguments — attack the strongest version of each competitor

## Migration/Adoption Path

Describe the practical cost of choosing your approach:
- What does adoption look like? (learning curve, setup time, migration effort)
- What ecosystem, tooling, and community support exists?
- What is the path from current state to full adoption?
- Are there incremental adoption options, or is it all-or-nothing?

## Risk Profile

What could go wrong if your approach is selected?
- Identify 2-4 risks with honest severity assessments
- For each risk, provide a concrete mitigation strategy
- Distinguish between risks you control and risks you don't

---

## Rules

- Ground every claim in your documentation. Unsubstantiated claims will be dismantled in cross-review.
- Write for a skeptical judge, not a friendly audience.
- Acknowledge the target problem precisely — generic advocacy loses to specific advocacy.
- Do not reference or respond to other agents' arguments (you have not seen them yet).
- Write the output as a standalone document (with a top-level heading using your name), not as a conversation.
