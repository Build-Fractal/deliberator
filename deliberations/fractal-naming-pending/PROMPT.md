# Naming deliberation prompt — conversus + spec-kit-orc under Fractal namespace

A self-contained prompt to hand to a fresh agent session for running a
conversus deliberation on two naming decisions.

**v2** — corrected methodology: blind judge + explicit status-quo defender.
The v1 of this prompt (no longer recorded here) framed the arbiter as a
"Fractal product owner" who knew the current names, and had no agent
defending inertia. Both created change-bias.

**Provenance**: produced 2026-04-26 in conversation; not yet executed.
Run by handing the entire codeblock below to a fresh `claude` session.
The agent will build `conversus.yml`, the brief, and run the deliberation.

**Methodology references**:
- Spec 067 §4.3.1 — use existing role presets (`devils-advocate`,
  `balanced-arbiter`)
- `feedback_constitutional_amendment_pipeline.md` — defend status quo;
  blind judge

---

```
You are starting a fresh session to run a conversus deliberation on
two naming decisions. Methodology requirements (per spec 067 §4.3 +
this session's lessons):
  - The arbiter MUST be blind: do not pre-tell the arbiter which
    candidates are the current names. Treat every candidate as a
    peer.
  - The status quo MUST be explicitly defended by a dedicated agent.
    Naming deliberations without a status-quo defender suffer
    confirmation bias toward change.
  - Use existing role presets (`presets/role/*`) where they fit.
    Do NOT hand-roll roles that already exist.

═══ CONTEXT (for the agents and you, NOT for the arbiter) ═══

Build-Fractal is considering consolidating its CLI tools under a single
namespace. The proposed pattern is:

    fractal <action> [args]

Each tool would become an action subcommand and live in a repo named
after the chosen verb (e.g., github.com/Build-Fractal/<verb>).

Two tools are in scope:

1. CONVERSUS — multi-agent deliberation engine. Game-theory modes
   (cooperative, winner-take-all, prisoners-dilemma, red-blue) drive
   structured adversarial review across LLM agents. Today the CLI is
   `conversus run config.yml`. Today the repo is conversus-oss.

2. SPEC-KIT-ORC — spec-kit orchestrator that drives
   specify→clarify→plan→tasks→implement end-to-end as one command.
   Today the repo is spec-kit-orc.

The deliberation answers TWO questions, in order:

  (A) Should we adopt the `fractal <verb>` consolidation pattern at
      all, given the migration cost from the current names?
  (B) If yes to (A), what verb wins for each tool?

═══ CANDIDATE POOLS (pass these to agents — do NOT mark which is
    incumbent) ═══

Tool 1 candidates (treat all as peers):
  argue, deliberate, agree, debate, decide, synthesize, converge,
  clash, conversus

Tool 2 candidates (treat all as peers):
  run, runner, do, ship, drive, execute, go, build, orc

Adding write-in candidates is permitted. Candidates do NOT have to be
imperative verbs IF an agent argues persuasively that breaking the
verb constraint is worth it (e.g., the status-quo defender will).

═══ DELIBERATION SETUP ═══

mode: cooperative
output: deliberations/fractal-naming-2026-04-26/
rounds: 1
stagnation: detect

agents:
  - name: status-quo-defender
    prompt: |
      Your job is to argue AGAINST changing the current names AND
      against adopting the `fractal <verb>` consolidation constraint.
      Make the strongest possible case for inertia:
      - Migration costs: every link in docs / READMEs / external
        references / blog posts / package indexes breaks.
      - Established recognition: what brand equity exists in the
        current names? Does the niche audience already know them?
      - Constraint cost: forcing every tool name to be a verb
        amputates expressive options. Distinctive proper nouns
        (`conversus`) signal "this is its own thing"; generic verbs
        (`fractal run`) blur into the parent brand.
      - Reversibility: a rename is a one-way door for index entries
        and inbound links.
      Argue for ranking the current names highest in your verdict,
      OR for rejecting the consolidation constraint entirely. Be
      willing to recommend "stay with what we have."

  - name: brand-coherence
    prompt: |
      You evaluate names assuming the consolidation constraint holds.
      Ask: do all the chosen verbs feel like one product? Does
      `fractal argue` sit naturally next to `fractal run`, or does
      the tone clash? Avoid names that are too generic, too clever,
      or that fight each other. Score each candidate 1-5 on
      within-suite coherence.

  - name: semantic-accuracy
    prompt: |
      You evaluate names for how precisely they describe what the
      tool does. Generic verbs read as placeholders; specific verbs
      tell the developer what's about to happen. For each candidate
      — INCLUDING any proper-noun candidates the status-quo
      defender raises — score 1-5 on whether someone reading just
      the verb would know what the tool does.

  - name: skeptic
    preset: devils-advocate
    prompt: |
      Argue against the strongest-looking candidate for each tool.
      Find the failure mode the other lenses are too charitable to
      surface. Specifically check: trademark / namespace collisions,
      embarrassment risk (search results), cross-language
      mistranslation, corporate-blandness risk, and — for proper-noun
      candidates — pronunciation friction in conversation.

═══ ARBITER (blind — see the special framing) ═══

arbiter:
  name: independent-arbiter
  preset: balanced-arbiter
  prompt: |
    You are an independent arbiter. You do NOT know which (if any)
    candidates are currently in use as names. Treat every candidate
    in both pools as a peer competitor. Do not assume the candidate
    that "looks Latin" or "looks technical" is more or less likely
    to be the incumbent. The agents below may reveal which is
    incumbent through their arguments — let the arguments inform
    your ruling, but do NOT default to incumbency on absence of
    evidence.

    Your job has TWO rulings, in order:

    RULING A — should the consolidation constraint (`fractal <verb>`)
    be adopted at all? The status-quo-defender will argue against;
    the other agents will argue within. Weigh:
    - Is the brand-coherence value of consolidation worth the
      migration cost?
    - Are the semantic-accuracy gains real or marginal?
    - Are there candidates strong enough to justify the change?

    Output one of: ADOPT, REJECT (keep current names + drop the
    constraint), DEFER (insufficient evidence; describe what would
    unblock).

    RULING B — applies only if Ruling A is ADOPT. Pick exactly ONE
    verb for each of Tool 1 and Tool 2. For each pick:
    - The chosen verb
    - One sentence on why it beat each runner-up
    - One sentence acknowledging the strongest argument against it
    - The full CLI form
    - The proposed repo name
    - A "what would invalidate this choice?" section (trademark,
      namespace squat, etc.)

    If Ruling A is REJECT, Ruling B is N/A — output instead a
    rationale for staying put and a list of what conditions would
    later justify reopening this question.

  grounding: deliberations/fractal-naming-2026-04-26/brief.md
  trigger: always
  timing: final
  influence: binding

═══ THE BRIEF ═══

Before launching the deliberation, create
`deliberations/fractal-naming-2026-04-26/brief.md` with:
- The two tools' purposes (one paragraph each)
- The proposed `fractal <verb>` pattern and why it was raised
- The candidate pools (mixed, no incumbent marking)
- The two rulings the arbiter must produce

Do NOT mention in the brief which candidates are currently in use.
The status-quo-defender's argument is what surfaces that information
during the deliberation — that's by design, so the arbiter sees it
as testimony, not as setup.

═══ DELIVERABLES ═══

After the deliberation, write `final-recommendation.md` at the top
of the output directory with:

  1. RULING A: ADOPT / REJECT / DEFER, with the arbiter's rationale.
  2. If ADOPT: the winners for CONVERSUS and SPEC-KIT-ORC, runners-up,
     and "what invalidates this" signals for each.
  3. If REJECT: the conditions under which to reopen.
  4. Migration cost estimate (rough order of magnitude — link count,
     repo rename, PyPI republish) so the human can decide whether
     ADOPT is operationally feasible even if logically sound.

Provider: `--provider claude-code` (host CLI subscription, no API
charge). Estimated cost: ~25 launches for 4 agents × 1 round +
arbiter.

═══ EXPLICIT ANTI-PATTERNS — DO NOT ═══

- Do NOT mark the candidate `conversus` or `spec-kit-orc` as "current"
  in any prompt or in the brief.
- Do NOT pre-tell the arbiter which option is the status quo. The
  arbiter must learn it (or fail to learn it) through agent testimony.
- Do NOT skip Ruling A. A naming deliberation that assumes change is
  desirable IS the bias this prompt corrects against.
- Do NOT hand-roll the arbiter prompt — use `preset: balanced-arbiter`
  composed with the ruling-specific prompt above.
- Do NOT propose multi-word names UNLESS the status-quo defender's
  argument carries Ruling A toward REJECT. If the constraint holds,
  one verb only.
```
