# Q08: LLM-guided gap-filling — which model?

**Status**: Decided
**Decision**: User-configurable, default to cheapest capable model (Option C)

---

## Context

Open Question #8 from spec 007 Section 13:

> "Should the objective function construction use the same model as the deliberation agents, or a cheaper model since it's just asking structured questions?"

## Decision

**User-configurable via `gap_fill_model` in plugin config. Default to cheapest capable model.**

Gap-filling is structured translation (parse gaps → ask questions → map answers to parameters), not reasoning. A smaller model handles it. Users override for complex domains where question quality matters.

```yaml
plugins:
  - name: config-optimizer
    package: conversus-nashopt
    config:
      gap_fill_model: haiku  # default: cheapest capable
```

## Rejected Alternatives

- **Same model as agents** rejected: overpowered for structured Q&A, unnecessary cost
- **Hardcoded cheaper model** rejected: doesn't account for complex domains where question quality matters
