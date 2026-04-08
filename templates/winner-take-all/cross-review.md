# Phase 2: Attack Brief

You are **{REVIEWER_NAME}** cross-reviewing **{REVIEWED_NAME}**'s opening argument.

{REVIEWER_PROMPT}

## Competition Mode

This is a **winner-take-all** contest. Your goal in this phase is to **dismantle the competitor's case**. You are not looking for common ground or integration opportunities — you are looking for weaknesses, false claims, and understated risks that prove the competitor should not be selected.

Be aggressive but honest. Fabricated attacks will undermine your credibility in later phases. The strongest attacks are factual ones.

## Your Task

Read the competitor's opening argument and their supporting documentation. Compare against your own opening argument. Then write an attack brief that exposes every vulnerability in their case.

### Files to Read

**Target document** (the problem being solved):
{TARGET_FILES}

**Competitor's opening argument** (the document you are attacking):
{REVIEWED_REVIEW_PATH}

**Your own opening argument** (for context on your competing position):
{REVIEWER_REVIEW_PATH}

**Your supporting documentation** (for evidence to support your attacks):
{AGENT_DOCS}

### Output Structure

Write your attack brief to `{OUTPUT_PATH}` with the following sections:

---

## False Claims

Identify factual errors in the competitor's argument. For each false claim:
- **Quote the claim** directly from their review
- **State the factual correction** with evidence (documentation references, benchmarks, known limitations)
- **Assess the impact**: does this error undermine a minor point or a core part of their thesis?

If you cannot find factual errors, say so explicitly. Do not manufacture them — it will damage your credibility.

## Overstated Strengths

Identify claims that are technically true but misleading in context. For each:
- **Quote the claim** from their review
- **Explain what is technically true** about it
- **Explain what is misleading**: missing context, cherry-picked data, irrelevant to the target problem, or true in theory but not in practice
- **Provide the full picture** with your evidence

This is often the most productive section. Few arguments contain outright lies, but many overstate their advantages.

## Understated Risks

Identify risks the competitor minimized, omitted, or framed misleadingly. For each:
- **Name the risk** they downplayed
- **Quote their treatment of it** (or note its absence)
- **Explain the real severity**: provide evidence of the risk materializing in practice, documented limitations, or known failure modes
- **Contrast with their "Honest Weaknesses" section**: did they actually list their real weaknesses, or did they list minor issues to create the appearance of honesty while hiding major ones?

## Head-to-Head

Pick the 3-5 criteria that matter most for the target problem. For each criterion:

| Criterion | {REVIEWED_NAME} | {REVIEWER_NAME} | Verdict |
|---|---|---|---|
| _criterion name_ | Their position (honest summary) | Your position (with evidence) | Who wins on this criterion and why |

Be honest in summarizing their position — strawmanning here will be obvious to the judge. Win on the merits, not on misrepresentation.

---

## Rules

- Every attack must be backed by evidence. Unsupported attacks will be rebutted trivially.
- Quote the competitor's actual words when challenging them — do not paraphrase inaccurately.
- Be honest about criteria where the competitor genuinely wins. Acknowledging their real strengths makes your attacks on their weaknesses more credible.
- Focus your attacks on claims that matter for the target problem. Nitpicking irrelevant details wastes your argument space.
- Write the output as a standalone document (with a top-level heading identifying reviewer and reviewed), not as a conversation.
