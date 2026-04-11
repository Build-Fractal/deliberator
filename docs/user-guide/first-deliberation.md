# Your First Deliberation

A 5-minute walkthrough that installs conversus, runs a real deliberation, and explains what you just saw.

## Step 1: Install

```bash
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

**What this does**: installs the `conversus` Python package and its dependencies directly from GitHub. No PyPI account needed, no separate sdist download. Pip fetches the current `main` branch, builds a wheel, and installs it into your active Python environment.

**What you get**: a `conversus` binary on your PATH, the engine code as an importable Python module, and all 8 game theory modes wired up.

Verify the install:

```bash
conversus --version
```

## Step 2: Grant permissions

```bash
conversus init
```

**What this does**: writes a runtime settings file in your project so conversus can dispatch sub-agents **without** stopping for interactive permission prompts.

By default it writes `.claude/settings.json` (for Claude Code) with grants for the tools conversus needs:

- **`Agent`** — dispatch parallel sub-agents (one per deliberation phase × role)
- **`Read`** — read the target document being deliberated on
- **`Write`** — write per-agent outputs to the `conversus-output/` directory
- **`Bash`** — invoke the `conversus` CLI from within dispatched agents

**Why you need it**: a `decide` run dispatches 5-10 sub-agents. A full 4-agent deliberation in mechanism-design mode dispatches 29. Without `init`, every single dispatch stops and waits for you to click Approve. `init` grants those permissions once so the pipeline runs unattended.

**Other runtimes**: `conversus init --runtime opencode` (or `copilot`, `gemini`, `codex`, `aider`) writes the equivalent settings file for that runtime instead. Each runtime has its own permission format.

## Step 3: Ask a real question

```bash
conversus decide "Should we write unit tests or integration tests first for a new service?" --provider claude-code
```

**What this does**: runs an ad-hoc deliberation on a natural-language question, bypassing the config file. Under the hood, `decide` generates a temporary `conversus.yml` using two preset agents (pragmatist + devil's advocate), runs the full 5-phase pipeline, and prints structured results.

**The flags**:

- **Your question** in quotes — any decision you care about. Works best for questions where the right answer isn't obvious, where multiple perspectives matter, or where you'd otherwise be debating with yourself.
- **`--provider claude-code`** — use your installed Claude Code CLI as the LLM runtime. No API key needed — it uses your existing Claude Code subscription. Alternatives: `anthropic` (requires `ANTHROPIC_API_KEY`), `openai`, `ollama` (local models, free), `gemini`, `claude-code`, `mock` (fake responses, no credentials).

**No credentials or free preview?** Use `--provider mock` to see the full pipeline with synthetic agent responses — perfect for learning the mechanics before spending anything:

```bash
conversus decide "Should we write unit tests or integration tests first?" --provider mock
```

## What you'll see

A progress table prints as the pipeline runs:

```text
[14:21:03] ⏳ Phase: review (2 agents)
             → pragmatist dispatched to claude-sonnet-4-20250514
             → devils-advocate dispatched to claude-sonnet-4-20250514
[14:22:41]   ✓ pragmatist (98s)
[14:22:58]   ✓ devils-advocate (115s)
           ✓ Phase: review — 2/2 succeeded (115s)
           ⏳ Phase: cross-review (2 agents)
             → pragmatist→devils-advocate dispatched
             → devils-advocate→pragmatist dispatched
[14:24:39]   ✓ pragmatist→devils-advocate (101s)
[14:24:51]   ✓ devils-advocate→pragmatist (113s)
           ⏳ Phase: revision (2 agents)
           ...
           ⏳ Phase: synthesis (1 agent)
           ✓ Deliberation complete
```

The default `decide` command runs a **5-phase pipeline** with two agents: a **pragmatist** (evaluates practical feasibility and real-world tradeoffs) and a **devil's advocate** (challenges assumptions and surfaces risks).

### What each phase does

#### 1. Review

Each agent is dispatched in parallel with your question and their role prompt. They have **no knowledge of the other agent** — they write their initial position in isolation. This is deliberate: you don't want groupthink before the first opinion is on paper.

Output: `pragmatist/review.md`, `devils-advocate/review.md`

Each review contains the agent's answer to your question, their reasoning, and any caveats they think are important.

#### 2. Cross-review

Each agent now reads *the other agent's* review and writes a critique. The pragmatist reviews the devil's advocate's position, and vice versa. They're told to look for: unsupported claims, missing context, internal contradictions, blind spots.

Output: `pragmatist/cross-reviews/devils-advocate.md`, `devils-advocate/cross-reviews/pragmatist.md`

This is the phase where adversarial pressure starts. Single-LLM answers skip this entirely — which is why they sound confident even when they're wrong.

#### 3. Revision

Each agent reads the critique against their own position and writes a revision. They can:
- **Concede** points where the critique was correct
- **Defend** positions that survived scrutiny
- **Modify** arguments to address valid concerns
- **Add** new considerations surfaced during cross-review

Output: `pragmatist/revision.md`, `devils-advocate/revision.md`

The revision isn't a compromise — it's what each agent *still believes* after being challenged. Sometimes positions converge. Sometimes they don't.

#### 4. Disputes

Each agent writes a formal statement of what they still disagree on with the other agent after revision. This phase makes unresolved tension **explicit** rather than papering over it. If the two agents genuinely can't agree, that's important signal — you should know before trusting the synthesis.

Output: `pragmatist/disputes.md`, `devils-advocate/disputes.md`

#### 5. Synthesis

A final synthesizer agent reads **everything**: both reviews, both cross-reviews, both revisions, both dispute statements. It produces the verdict — grounded in the full adversarial record, with unresolved disputes called out explicitly.

Output: `summary/final.md`

This is the file you read. But the rest of the tree is preserved so you can audit *how* the answer was produced.

## Where the output lands

```text
your-project/
└── conversus-output/
    └── 2026-04-10_142103/
        ├── pragmatist/
        │   ├── review.md
        │   ├── cross-reviews/devils-advocate.md
        │   ├── revision.md
        │   └── disputes.md
        ├── devils-advocate/
        │   └── ... (same structure)
        └── summary/
            └── final.md       ← the verdict
```

Open `summary/final.md` in your editor. That's the synthesized answer, grounded in the full adversarial record. If you want to see *how* the agents got there, every phase file is preserved — real, auditable reasoning trails.

## Why this is different from asking one LLM

Ask ChatGPT "Should I write unit tests or integration tests first?" and you get one answer from one perspective, confidently stated.

Conversus gives you:

1. **Two initial positions** written in isolation (no groupthink)
2. **Cross-reviews** where each agent has to defend against the other's critique
3. **Revisions** where agents update their positions when challenged
4. **Formal disputes** — what remains unresolved is explicit, not buried
5. **A synthesis** that accounts for the adversarial record

The important part is the **cross-review phase**. Single-LLM answers sound confident because they're never challenged. Conversus makes the LLM challenge itself — and the weak arguments get exposed.

## A real example

The decisions behind conversus itself were made by running conversus. See the [packaging strategy deliberation](https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations/packaging-strategy): 4 agents (APM maximizer, non-technical user advocate, technical power user, fact-based arbiter), 29 LLM launches, mechanism-design mode. It produced the three-layer PyPI + MCP + Claude Code plugin architecture.

Browse the per-agent reviews, the cross-reviews, and the final synthesis. That's what a full conversus run looks like.

## Next steps

- **[Modes](modes.md)** — 8 deliberation modes: cooperative, winner-take-all, red-blue, prisoner's dilemma, negotiation, resource-allocation, fair-division, mechanism-design. Pick the one that matches your decision type.
- **[Config files](config-reference.md)** — for reproducible deliberations with custom agents, targets, and modes.
- **[CLI reference](cli.md)** — every command and flag.
- **[MCP setup](mcp-setup.md)** — use conversus directly from Claude Code, Cursor, or Windsurf without leaving your editor.
- **[Specs & Deliberations](../developer-guide/specs-and-deliberations.md)** — real case studies of conversus in action.
