# Negotiation Revision — Phase 3: Revised Position After Counter-Offers

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

This is revision iteration {ITERATION}.

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you revise your opening position after reading all counter-offers. The goal is to move toward agreement: concede where their arguments are strong, hold firm where yours are stronger, and identify the emerging deal structure.

## What to Read

1. **Your original position statement**:
   `{MY_REVIEW_PATH}`

2. **Counter-offers to your position** (other parties responding to your position):
{CROSS_REVIEWS_OF_ME}

3. **Your counter-offers** (your responses to other parties):
{MY_CROSS_REVIEWS}

4. **Target document**:
   the target files:
{TARGET_FILES}

5. **Your documentation**:
{AGENT_DOCS}

Read all files before writing. Pay close attention to counter-proposals and value creation opportunities identified in the counter-offers.

## What to Produce

Write your revision to: `{OUTPUT_PATH}`

Your revision must contain the following sections in this exact order:

---

### Term Dispositions

Take each term from your opening offer and classify it. Use this exact format for every term:

#### Term N: [Original term label]

- **Original position**: [1-sentence summary of what you proposed]
- **Disposition**: Conceded | Modified | Firm
- **Explanation**:

For **Conceded** terms:
  - Which counter-offer challenged this, and what was the argument? Cite the specific counter-offer section.
  - Why you now accept the other party's position or withdraw the term.

For **Modified** terms:
  - Which counter-offer prompted the modification? Cite sections.
  - What the original term was and what it becomes. State the new version precisely.
  - Why the modification preserves your core interest while addressing their concern.

For **Firm** terms:
  - Which counter-offer challenged this (if any)? Cite sections.
  - Why their challenge does not change your position. Provide additional evidence or reasoning.

Process every term. Do not skip any.

### New Terms

Terms that emerged from the counter-offer process. 0-3 items:

- **[Term label]**
  - **Triggered by**: Which counter-offer or value creation opportunity surfaced this.
  - **Proposed term**: The specific term you now propose.
  - **Rationale**: Why this creates value for both parties.

### Revised ZOPA Assessment

Update your assessment of the zone of possible agreement:

- **Deal structure taking shape**: What the emerging agreement looks like.
- **Remaining gaps**: Where the parties are still far apart.
- **Updated BATNA assessment**: Has the negotiation changed your BATNA? Has new information changed your assessment of theirs?

---

## Rules

- **Move toward agreement.** If a counter-offer exposed a genuine weakness in your position, concede. Stubbornly holding every position signals bad faith.
- **Modifications must be concrete.** State the exact revised term, not "I am willing to be more flexible."
- **Do not concede everything.** Some counter-offers are themselves inflated. Hold firm where your evidence is stronger.
- **Credit the source.** When you change position, cite the specific counter-offer that prompted it.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate. Write the complete revision.
