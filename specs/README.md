# Specs Directory

## Lifecycle

draft/ → specs/ → done/

- `specs/draft/`: idea phase. Vision, sketches, not blocking implementation.
- `specs/`: active. Being implemented or has imminent gate (verification, deliberation, code).
- `specs/done/`: shipped, superseded, or decomposed.

## Status field is authoritative

Each spec.md has a Status field. That field is the canonical source.
Directory placement is a *derived signal* — it MUST match the Status,
but conflict resolves to the field. Renaming a directory doesn't
change a spec's status; updating the field does.

## Promotion rules

- **draft → specs**: when implementation work begins or a deliberation
  is imminent. Update Status to Active.
- **specs → done**: when implementation merges, the spec is decomposed
  into other specs, or the spec is superseded. Update Status to
  Done / Decomposed / Superseded with a Closure note.
- **specs → draft** (rare): if active work pauses. Update Status to Draft
  with a "paused" note explaining why.
- **done → anywhere**: never (history is permanent).

## Out of scope (live workspaces, not specs)

- `blog_posts.md`, `distribution-strategy.md`, `ideas.md`
- `plan-of-attack.md`, `plan-of-attack.conversus.yml`, `plan-of-attack.conversus/`
- `wave1-3-blog/`, `meta-review/`
- `archive/` (superseded vision docs — distinct purpose from done/)

## Cross-references

- `STATUS.md`: current-state index (uses this lifecycle to render the table)
- `AUDIT-YYYY-MM-DD.md`: periodic hygiene audits
- `CONTRIBUTING.md` (planned, per spec 065 G7): general contribution rules
