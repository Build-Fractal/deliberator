# Q03: Should the config optimizer run automatically in the decision framework?

**Status**: Decided
**Decision**: Mode-dependent — inline recommendation in interactive mode (C), silent apply in auto mode (A)

---

## Context

Open Question #3 from spec 007 Section 13:

> "Should the config optimizer run automatically in the decision framework (spec 002/999)? When a user runs `/conversus mode`, should the optimizer automatically recommend config if the plugin is installed?"

## Options Considered

- **A: Transparent enhancement** — optimizer silently improves the generated YAML
- **B: Separate step** — new `/conversus optimize` command
- **C: Inline recommendation** — show optimization with explanation, user confirms

## Decision

**Both A and C, depending on execution mode.**

### Interactive Mode (Decision Framework)

When the user is going through the guided workflow (`/conversus mode`), the optimizer presents its recommendations with reasoning. The user confirms or overrides.

```
/conversus mode

Recommended mode: cooperative
  Your interests represent perspectives that must coexist.

Config optimizer recommendations (conversus-nashopt):
  Rounds: 3  — convergence predicted by Round 2, Round 3 as safety margin
  Agents: 4  — minimum for equilibrium coverage in cooperative mode
  Iterations: 1  — single iteration sufficient for this problem complexity

  Apply optimizer recommendations? [Y/n]

  (Default config without optimizer: rounds=1, iterations=1)
```

The value is visible. The user sees what they're paying for. They can override any parameter.

### Auto Mode (Direct Run / Batch / CI)

When the user runs `/conversus run` directly or in a non-interactive context, the optimizer silently applies its recommendations to the config before execution — if `auto_optimize: true` is set.

```yaml
# conversus.yml
plugins:
  - name: config-optimizer
    package: conversus-nashopt
    config:
      auto_optimize: true   # silently apply in non-interactive mode
      budget: 50             # maximum agent launches
      optimize: [rounds, agents]
```

- `auto_optimize: true` — optimizer applies recommendations without prompting
- `auto_optimize: false` (default) — optimizer writes recommendations to `plugins/config-recommendation.yml` but does not modify config
- User must explicitly opt in to silent optimization

### Why Not a Separate Command (Option B)

If you pay for the optimizer, it should run where it adds value — at the point where config decisions are made. A separate `/conversus optimize` command:
- Adds friction to the workflow (6 commands instead of 5)
- Most users won't know to run it
- The optimization is only useful BEFORE execution, not as a standalone step

The optimizer's natural home is `/conversus mode` (interactive) and PRE_EXECUTION hook (auto).

## Behavior Matrix

| Context | Plugin installed | auto_optimize | Behavior |
|---------|-----------------|---------------|----------|
| `/conversus mode` | Yes | N/A | Show recommendations, ask to confirm |
| `/conversus mode` | No | N/A | Normal mode selection, no optimization |
| `/conversus run` | Yes | true | Silently apply recommendations |
| `/conversus run` | Yes | false | Write to `plugins/config-recommendation.yml` only |
| `/conversus run` | No | N/A | Normal execution |
| Batch/CI | Yes | true | Silently apply, log what changed |
| Batch/CI | Yes | false | Write recommendation file only |

## Pattern Alignment

This follows the same interactive/non-interactive split established in Q02:

| Question | Interactive | Non-interactive |
|----------|------------|-----------------|
| Q02 (stop on stagnation) | Pause and prompt | Log warning, continue (v1) / auto-cancel (v2) |
| Q03 (config optimization) | Show recommendations, confirm | Advisory only (default) / auto-apply (opt-in) |

Both respect the principle: **show the value when the user is watching, apply it silently when they've opted in.**

## Implications

- `/conversus mode` needs plugin awareness — check if config optimizer is installed, call it
- The PRE_EXECUTION hook (already defined in spec 007) is where auto-mode optimization runs
- Plugin output for auto mode should log what it changed: "Config optimizer applied: rounds 1→3, agents 3→4"
- `auto_optimize` is a per-plugin config field, not a global setting

## Rejected Alternatives

- **Option A alone** rejected: hiding the value means users don't see what they're paying for. The optimizer's reasoning (WHY 3 rounds) is valuable context for the decision.
- **Option B** rejected: separate command adds friction. Users who pay for optimization shouldn't need to remember an extra step.
- **Option C alone** rejected: doesn't cover batch/CI where no one is watching. Auto-apply with opt-in handles unattended execution.
