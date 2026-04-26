# Naming walkthrough prompt — guided one-perspective decision aid

A self-contained prompt for an agent to walk a single human (Brett or
similar) through the naming decision interactively. Companion to
`PROMPT.md` (the full multi-agent deliberation).

**When to use which:**

- **WALKTHROUGH.md (this file)** — when a human wants to form a
  reasoned position quickly via guided conversation. Output is a
  single-perspective `position.md`. ~20 minutes.
- **PROMPT.md** — when a multi-agent verdict is needed. Output is
  the full deliberation directory with arbiter ruling. ~25 LLM
  launches; longer wall time.

The two artifacts can compose: a human walks through this prompt to
form their pick, then runs `PROMPT.md` with their pick as a write-in
candidate so the status-quo-defender and skeptic agents can pressure
test it.

**Provenance**: produced 2026-04-26 in conversation. Lives at
`deliberations/fractal-naming-pending/WALKTHROUGH.md`.

---

```
You are walking [the human] through a naming decision interactively.
[The human] has not been in recent sessions; you'll surface the
context, present the two rulings the deliberation framework would
ask, and help them form a position. The output is their reasoned
answer — not a full multi-agent deliberation.

Repo: github.com/Build-Fractal/conversus-oss. You're running from the
repo root.

═══ READ FIRST ═══

1. deliberations/fractal-naming-pending/PROMPT.md
   — the full naming deliberation setup. You're walking [the human]
   through the same questions a multi-agent deliberation would ask,
   just in a single guided conversation.

2. specs/065-path-to-open-source/spec.md (specifically §G1)
   — context on why this decision matters: G1 has a default-to-
   `conversus` clause activating 2026-05-02 if no decision is filed.

═══ HOW TO RUN THE WALKTHROUGH ═══

Don't dump everything at once. Walk through this in stages, asking
for input at each. Use plain language; no game-theory jargon.

**Stage 0 — orient them**

Tell [the human], in 3-4 sentences:
- Build-Fractal is considering consolidating CLI tools under
  `fractal <verb>` (so `conversus run` becomes `fractal argue`,
  `spec-kit-orc` becomes `fractal run` or similar).
- Two tools need names: a multi-agent deliberation engine
  (currently `conversus`) and a spec-kit orchestrator
  (currently `spec-kit-orc`).
- The deliberation framework would ask TWO questions in order:
  (A) Should we consolidate at all? (B) If yes, what verbs win?
- "I'll walk you through both. Want to proceed?"

If they decline, write what they chose to a file (Stage 4) and stop.

**Stage 1 — Ruling A: should we consolidate?**

Present the case for AND against consolidation. Be honest about
both sides — don't tilt.

FOR consolidation:
- Brand coherence: a unified `fractal` CLI suite is more
  recognizable than scattered tool names.
- Discoverability: developers learn one entry point.
- Semantic accuracy: a verb tells the user what the tool does;
  proper nouns (`conversus`) require explanation.

AGAINST consolidation (status quo defended):
- Migration cost: every link in docs / README / blog posts /
  package indexes breaks. PyPI and GitHub URLs change.
- Brand equity: `conversus` is distinctive — search-engine
  identity, niche audience recognition. Generic verbs like
  `fractal run` blur into the parent brand.
- Reversibility: a rename is a one-way door. Once links die,
  they don't come back.

Then ask: "What's your gut on Ruling A — ADOPT consolidation,
REJECT (keep current names), or DEFER (need more evidence)?"

If REJECT or DEFER, jump to Stage 4. Don't push them into Stage 2
they don't want.

**Stage 2 — Ruling B (only if A is ADOPT): verbs**

Present the candidates for each tool with one-line lens hits.
DO NOT mark which candidate is currently in use — that's the
blind-judge methodology. They can ask, but make them ask.

For CONVERSUS (multi-agent deliberation engine):
Candidates: argue, deliberate, agree, debate, decide, synthesize,
converge, clash, conversus

Present each with:
- Brand-coherence read (how it sits in `fractal <verb>`)
- Semantic-accuracy read (does it tell you what the tool does?)
- Skeptic's flag (trademark / search / pronunciation risk)

Example for `argue`:
- Brand: "fractal argue" reads naturally; punchy.
- Semantic: high — "argue" precisely names the tool's adversarial
  core. Better than "deliberate" which sounds neutral.
- Skeptic: "argue" has connotation drift toward conflict; some
  audiences may read negativity where the tool means rigor.

Walk through the top 3-4 candidates this way. Don't dump all nine.
After each, ask: "Lean? Pass?" Note reactions.

Then ask for their pick + one-sentence rationale. Write-ins
permitted.

Repeat the structure for SPEC-KIT-ORC (candidates: run, runner,
do, ship, drive, execute, go, build, orc).

**Stage 3 — Pressure test their pick**

Once they have a verb for each tool, ask the strongest counter-
question for each:
- "What if `<their-pick>` shows up in your search results next
  to something embarrassing? Can you live with that?"
- "If the namespace is squatted on PyPI, are you willing to use
  `<their-pick>2` or pick again?"
- "Six months from now, when external users have linked
  `<their-pick>` in blog posts, do you still feel good about it?"

Capture answers. If they waver, offer the runner-up as fallback.

**Stage 4 — Capture their decision**

Use the **Write tool** to write the position to:
`deliberations/fractal-naming-brett-input/position.md`
(replace `brett` with the human's name if different)

Format:

```markdown
# [Name]'s Position — Fractal Naming Decision

**Date**: <today>
**Walked through by**: <model>

## Ruling A: Consolidation
**Choice**: ADOPT | REJECT | DEFER
**Rationale**: <their words, paraphrased>
**Pressure-test response**: <how they handled the counter-arguments>

## Ruling B: Verb selection (only if A = ADOPT)

### Tool 1 — CONVERSUS
**Pick**: <verb>
**Rationale**: <their sentence>
**Runner-up**: <if any>
**Pressure-test response**: <their answer to the squat / drift questions>

### Tool 2 — SPEC-KIT-ORC
**Pick**: <verb>
**Rationale**: <their sentence>
**Runner-up**: <if any>
**Pressure-test response**: <their answer>

## What this position represents
Individual judgment after a guided walkthrough — NOT a multi-agent
deliberation outcome. To validate, run the full deliberation per
`deliberations/fractal-naming-pending/PROMPT.md` with their picks as
write-in candidates so the status-quo-defender and skeptic agents
can test them.

## Next step
- File this position in spec 065 §11 (Decisions table) for G1
- OR run the full deliberation with this position's picks added as
  candidates
- OR accept this as final if confidence is high
```

Return only a one-line confirmation: "Position written to {path};
choice: <verdict>."

═══ ANTI-PATTERNS — DO NOT ═══

- Do NOT push toward consolidation. The status quo is a legitimate
  answer. Many naming deliberations correctly land on REJECT.
- Do NOT skip Stage 1 to get to verbs faster. Ruling A first is the
  methodology — verbs only matter if A is ADOPT.
- Do NOT reveal which candidate is the current name unless asked.
  Inference is allowed; revelation is not.
- Do NOT pretend this walkthrough is a multi-agent deliberation.
  It's one perspective refined through guided questions. The final-
  recommendation.md the deliberation would produce is different
  from this position document — make that distinction explicit.
- Do NOT overload Stage 2. 3-4 candidates per tool is enough; the
  full nine produces decision fatigue.
```
