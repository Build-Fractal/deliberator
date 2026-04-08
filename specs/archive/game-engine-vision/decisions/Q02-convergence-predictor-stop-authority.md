# Q02: Should the convergence predictor be allowed to STOP a deliberation?

**Status**: Decided
**Decision**: Recommend-then-confirm — prompt user to cancel on stagnation prediction, evolve toward auto-cancel

---

## Context

Open Question #2 from spec 007 Section 13:

> "If it predicts with 95% confidence that Round 3 will stagnate, should the engine skip Round 3 automatically? Or always defer to the user?"

## Options Considered

- **A: Always defer** — predictor writes advisory output, user decides, engine never acts
- **B: Auto-stop with override** — engine stops automatically above confidence threshold
- **C: Recommend-then-confirm** — engine pauses, presents prediction, asks user

An arbiter-aware routing variant of C was considered (offer to add arbiter mid-deliberation if not configured) but rejected — too complex for the pause point, violates KISS.

## Decision

**Option C, simple: pause and prompt user to cancel or continue.**

### Mechanism

```
Convergence predictor fires (POST_PHASE_5)
  │
  ├── Prediction: CONVERGENCE LIKELY
  │   └── Proceed to next round (no pause)
  │
  └── Prediction: STAGNATION LIKELY
      │
      └── Pause and present:
          "Stagnation predicted with 93% confidence.
           Continuing to Round 2 is unlikely to reduce disputes.
           1. Stop deliberation here (recommended)
           2. Continue to Round 2"
```

That's it. No config suggestions, no arbiter routing, no workflow branching. The predictor says stop or go, the user decides.

### Evolution Path: Prompt → Auto-Cancel

| Phase | Behavior | Trigger |
|-------|----------|---------|
| **v1** | Always pause, always ask | Launch — predictions unproven |
| **v2** | Auto-cancel on by default, opt-out via `auto_stop: false` | Prediction accuracy exceeds threshold over N runs |

Auto-cancel becomes **opt-out** once predictions prove reliable. Users who installed the predictor want automation — once the tool earns trust, deliver it.

### Prediction Quality Tracking

Each prediction is stored with its actual outcome:

```yaml
# plugins/convergence-prediction.yml
plugin: convergence-predictor
hook: POST_PHASE_5
data:
  round: 1
  prediction: stagnation
  confidence: 0.93
  actual_outcome: null  # filled after deliberation completes: converged | stagnated
  prediction_correct: null
display:
  headline: "Stagnation Predicted (93% confidence)"
  body:
    - "Based on Round 1 position vectors, agents are unlikely to converge in Round 2."
  recommendation: "Stop deliberation here."
  severity: warning
```

### Non-Interactive Degradation

In batch/CI mode (no TTY or `--non-interactive` flag):
- v1: log warning, continue (advisory only)
- v2: log warning, auto-cancel (opt-out with `auto_stop: false`)

## Open Sub-Questions

- **What accuracy threshold triggers auto-cancel graduation?** Needs empirical data. Strawman: 85% accuracy over 20+ predictions.
- **Mode-awareness**: In red-blue mode, "stagnation" may mean confirmed risks rather than wasted tokens. Should the predictor adjust its recommendation language per mode? Deferred to implementation.

## Rejected Alternatives

- **Option A** rejected: users who install a convergence predictor want actionable guidance at decision time, not a post-hoc JSON file
- **Option B** rejected for v1: predictions are unproven, auto-stopping could frustrate users who would have converged. Accepted as v2 evolution target.
- **Arbiter-aware routing** rejected: adding arbiter mid-deliberation creates a mini-workflow at the pause point, crosses plugin→core config boundary, violates KISS
