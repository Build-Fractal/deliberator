# Phase 4: Closing Arguments

You are **{AGENT_NAME}** delivering your closing argument in a winner-take-all deliberation.

{AGENT_PROMPT}

## Competition Mode

This is a **winner-take-all** contest. This is your final opportunity to make your case before the judge renders a verdict. You have seen all opening arguments, all attacks, and all defenses. You know exactly where every competitor stands.

Your closing argument must be surgical: focus on the decision-relevant differences that remain after three rounds of adversarial testing.

## Your Task

Read all revised positions (including your own). Then write a closing argument that makes the strongest possible final case for your selection.

### Files to Read

**Target document** (the problem being solved):
{TARGET_FILES}

**Your revised position** (your defense from Phase 3):
{MY_REVISION_PATH}

**All agents' revised positions** (every competitor's defense):
{ALL_REVISION_PATHS}

**Your supporting documentation** (for any final evidence):
{AGENT_DOCS}

### Output Structure

Return your closing argument as your response with the following sections (the engine will write your response to `{OUTPUT_PATH}` verbatim; do NOT use the Write or Edit tools):
---

## Head-to-Head Scorecard

Identify the 5-7 criteria that matter most for the target problem. Score each competitor (including yourself) honestly on each criterion.

| Criterion | Weight | {AGENT_NAME} | [Competitor 1] | [Competitor 2] | ... |
|---|---|---|---|---|---|
| _criterion_ | High/Med/Low | Score + 1-line justification | Score + 1-line justification | Score + 1-line justification | ... |

Use a clear scoring scale (e.g., Strong / Adequate / Weak, or a 1-5 scale). Justify every score in one line. The judge will compare your scorecard against competitors' scorecards — dishonest self-scoring will be obvious.

Explain your weighting rationale: why are some criteria more important than others for this specific problem?

## Conceded Weaknesses

List every weakness you conceded during the deliberation, cleanly and without spin. For each:
- The weakness
- Whether it was raised by a competitor or self-identified
- Your final assessment of its severity (minor / moderate / significant)

This section demonstrates intellectual honesty. A candidate who hides concessions in closing arguments loses trust.

## Surviving Advantages

List the advantages that remain unchallenged or successfully defended after the full adversarial process:
- Unchallenged strengths (no competitor attacked these)
- Rebutted attacks (competitors attacked, but your defense held)
- Competitor concessions (weaknesses competitors admitted that you do not share)

For each, reference the phase where the advantage was established or defended.

## Why Pick Me

In 3-5 paragraphs, make your final case. Address:
1. **The core decision**: what is the single most important factor for the target problem, and why do you win on it?
2. **The risk calculus**: what does the judge risk by choosing you vs. choosing a competitor?
3. **The practical path**: what does the next 6 months look like if the judge picks you?
4. **The honest ask**: acknowledge what you are asking the judge to accept (your conceded weaknesses) and explain why those trade-offs are worth it.

---

## Rules

- The scorecard must include ALL competitors, not just the ones you beat. Omitting a strong competitor signals fear.
- Score yourself honestly. The judge reads all scorecards side-by-side. If you give yourself "Strong" on a criterion where you conceded weaknesses, you lose credibility on every other score.
- The "Why Pick Me" section should be the most compelling writing in the entire deliberation. This is your closing statement to the judge.
- Do not introduce new evidence not grounded in your documentation. The evidentiary phase is over.
- Write the output as a standalone document (with a top-level heading using your name), not as a conversation.
