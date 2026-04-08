# Q01: Should plugin recommendations be surfaced in the conversus report?

**Status**: Decided
**Decision**: Option B — deterministic append to end of summary, structured YAML + plugin-owned templates

---

## Context

Open Question #1 from spec 007 Section 13:

> "If an equilibrium scorer says quality is 0.4, should the report include that? Or is it only in `plugins/` output?"

## Options Considered

- **A: Plugins-only** — output stays in `plugins/` subdirectory, report unchanged
- **B: Report footer** — plugin insights appended to summary as a dedicated section
- **C: Inline integration** — plugin scores appear inline next to relevant sections via template composition

Option C was initially selected but rejected after deeper analysis — template slot/fragment composition introduces unnecessary complexity (slot versioning, multi-plugin ordering, template engine changes). An LLM-driven inline approach was also considered but rejected in favor of determinism.

## Decision

**Deterministic append with structured YAML output and plugin-owned narrative templates.**

### Mechanism

1. Plugin executes at its lifecycle hook
2. Plugin writes structured YAML to `plugins/{name}.yml`
3. The YAML contains both machine-readable `data` and structured `display` fields
4. Each plugin ships its own rendering template that turns `display` into markdown
5. After deliberation, the engine reads `plugins/*.yml`, renders each through its template
6. Engine appends a `## Plugin Insights` section to `summary/final.md` with rendered output in registration order

### Plugin Output Format

```yaml
# plugins/equilibrium-score.yml
plugin: equilibrium-scorer
hook: POST_DELIBERATION
data:
  score: 0.92
  agents_at_equilibrium: 3
  total_agents: 4
  improvable_agent: "Agent C"
  improvable_delta: 0.08
  improvable_position: "THREAT-01"
display:
  headline: "Equilibrium Quality: 0.92/1.0"
  body:
    - "3 of 4 agents reached Nash equilibrium."
    - "Agent C could improve payoff by 0.08 by shifting position on THREAT-01."
  recommendation: "Outcome is stable — no agent has incentive to deviate."
  severity: info  # info | warning | critical
```

### Plugin Narrative Template

Each plugin ships a rendering template alongside its code:

```markdown
### {{headline}}
{{#each body}}
- {{this}}
{{/each}}

> **Recommendation**: {{recommendation}}
```

### Rendered Output

```markdown
## Plugin Insights

### Equilibrium Quality: 0.92/1.0
- 3 of 4 agents reached Nash equilibrium.
- Agent C could improve payoff by 0.08 by shifting position on THREAT-01.

> **Recommendation**: Outcome is stable — no agent has incentive to deviate.

### Convergence Prediction: High Confidence
- Round 2 convergence predicted with 94% confidence.
- Estimated 0 remaining disputes after next round.

> **Recommendation**: Proceed with Round 2.
```

### Why Structured YAML + Templates

| Concern | Flat display_hint string | Structured YAML + template |
|---------|------------------------|---------------------------|
| Machine readability | Data and narrative mixed | `data:` is clean, programmatic |
| Consistent narrative shape | Free-form, varies per plugin | `headline/body/recommendation/severity` is a contract |
| Cross-run analysis | Must parse narrative text | Read `data:` directly |
| Plugin authorship | Plugin writes prose | Plugin writes structured fields + ships template |
| Extensibility | New fields = new prose | New fields = new template lines |

### FR-005 Compliance

- `summary/final.md` without plugins: no `## Plugin Insights` section
- `summary/final.md` with plugins: section is appended
- The delta is clean and predictable — presence/absence of one trailing section
- No core template changes, no slot system, no composition engine

## Why This Works

- **Simple**: deterministic YAML read → template render → file append
- **Structured**: data stays machine-readable, narrative stays consistent
- **Plugin-owned**: each plugin controls both its data schema and its narrative template
- **Predictable**: same inputs → same output, same placement every time
- **No LLM cost**: no agent re-reading, no context expansion, no synthesis rewrite
- **Extensible**: new plugins add a YAML file + template, engine appends

## Open Sub-Question

**Upsell placeholders for uninstalled plugins** — deferred. When no plugins are installed, should the report mention available plugins? Requires deciding whether the core should have awareness of specific paid packages or use a generic registry. To be resolved separately.

## Rejected Alternatives

- **Option A** rejected: burying insights in `plugins/` means users rarely see them
- **Option C (template composition)** rejected: slot/fragment system introduces template versioning contracts, multi-plugin ordering complexity, and a composition engine — all before knowing which injection points plugins actually need
- **LLM-driven inline** rejected: non-deterministic placement, increased synthesis agent cost, inconsistent output across runs
- **Flat display_hint string** rejected: mixes data with narrative, no consistent structure across plugins, not machine-readable for cross-run analysis
