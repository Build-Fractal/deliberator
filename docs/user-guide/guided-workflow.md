# Guided Workflow

The guided workflow is a series of Claude Code skill subcommands that walk you through a complete deliberation. Each step produces an artifact that the next step consumes.

## Overview

| Step | Command | Produces |
|------|---------|----------|
| 1 | `/deliberator define` | `problem.md` |
| 2 | `/deliberator interests` | Interest map |
| 3 | `/deliberator mode` | `deliberator.yml` |
| 4 | `/deliberator converge` | Full deliberation output |
| 5 | `/deliberator arbitrate` | Arbitration ruling (optional) |
| 6 | `/deliberator gate` | CI/CD quality verdict (optional) |

## Step 1: Define your problem

```
/deliberator define "We need to decide between Redis and Postgres for our metadata cache"
```

This produces a `problem.md` that captures:
- The decision to be made
- Known constraints and requirements
- Stakeholders affected
- Success criteria

You can also provide a path to an existing problem description:

```
/deliberator define path/to/existing-problem.md
```

The classifier identifies the decision type (SELECTION, INTEGRATION, SCOPING, STRESS_TEST, NEGOTIATION, RESOURCE_ALLOCATION, FAIR_DIVISION, or MECHANISM_DESIGN) which influences mode selection in the next step.

## Step 2: Discover interests

```
/deliberator interests
```

Reads `problem.md` and identifies the relevant perspectives that should participate in the deliberation. For a caching decision, this might surface:
- Performance engineer (latency, throughput)
- Operations (complexity, failure modes)
- Developer experience (API ergonomics, learning curve)
- Cost analyst (licensing, infrastructure)

The output is an interest map with suggested agent configurations.

## Step 3: Select mode and generate config

```
/deliberator mode
```

Based on the decision type from `problem.md`, recommends a deliberation mode:

| Decision Type | Recommended Mode |
|---------------|-----------------|
| Pick one option | `winner-take-all` |
| Find common ground | `cooperative` |
| Assign ownership | `prisoners-dilemma` |
| Stress-test a plan | `red-blue` |
| Reach a deal | `negotiation` |
| Distribute resources | `resource-allocation` |
| Split fairly | `fair-division` |
| Design rules | `mechanism-design` |

Generates a `deliberator.yml` config file with the selected mode, agents from the interest map, and appropriate presets.

## Step 4: Execute with confirmation

```
/deliberator converge
```

Before running, shows:
- Config summary (mode, agents, iterations)
- Cost estimate (total LLM launches)
- Confirmation prompt

After confirmation, runs the full 5-phase pipeline with Rich progress output showing each phase as it completes.

## Step 5: Resolve disputes (optional)

```
/deliberator arbitrate path/to/output/
/deliberator arbitrate path/to/output/ --force   # Run even if no disputes
```

If the synthesis has surviving disputes, the arbiter (configured in `deliberator.yml`) resolves them using a grounding document (constitution, architecture doc, etc.). Each ruling must cite the grounding source.

Arbitration only runs when:
- An `arbiter` section is defined in the config
- `trigger: disputes_remain` and the synthesis has unresolved disputes, OR
- `trigger: always` (runs unconditionally)

## Step 6: Quality gates (optional)

```
/deliberator gate <phase> <artifact>
```

Runs a consensus check on a specific phase artifact. Useful in CI/CD pipelines to enforce quality thresholds:

```bash
# Check that synthesis meets quality bar
/deliberator gate synthesis output/summary/final.md

# Check phase 3 revisions
/deliberator gate revision output/pragmatist/revision-1.md
```

## Complete example: Redis vs Postgres

```
# 1. Define the problem
/deliberator define "Should we use Redis or Postgres for our session cache? \
  We have 50k DAU, need sub-10ms reads, and our team knows Postgres well."

# 2. Discover perspectives
/deliberator interests

# 3. Pick mode and generate config
/deliberator mode

# 4. Review the generated deliberator.yml, then run
/deliberator converge

# 5. If disputes remain, arbitrate
/deliberator arbitrate
```

Each step checks for the artifacts from previous steps and will prompt you if something is missing.
