# Output Conventions (formerly Constitutional Principle X)

*Authoring guidance for clean, readable output across CLI, MCP, and
plugin surfaces.*

This document is operational guidance, not a constitutional invariant.
Departures SHOULD be justified in the PR description; the constitution
([`../CONSTITUTION.md`](../CONSTITUTION.md)) governs invariant behavior.

## Conventions

Output SHOULD be clean, readable, and unsurprising. Follow the spirit
of the Zen of Python: explicit is better than implicit, simple is
better than complex, readability counts.

- There SHOULD be one obvious way to find the result. The output
  tree follows a predictable structure: `summary/final.md` is
  always the starting point.
- Flat is better than nested — avoid deep directory hierarchies
  when shallow ones suffice. Agent output is one level deep
  (`{agent}/review.md`), not arbitrarily nested.
- Sparse is better than dense — output files SHOULD contain focused
  content, not kitchen-sink aggregations. Each file SHOULD have one
  clear purpose.
- If the implementation is hard to explain, it's a bad idea. If
  SKILL.md instructions require paragraphs of caveats, the design
  needs simplification.

## Recommended implementation patterns

The mechanically checkable parts of these conventions are RECOMMENDED
implementation patterns rather than constitutional requirements:

- **Warnings for malformed output**: code that processes output
  artifacts SHOULD emit a warning when expected fields are missing,
  documents are malformed, or edge cases are encountered. Silent
  failure is worse than warned-and-continued behavior.
  *Recommended check*: surface validation warnings via the standard
  warning channel; keep the behavior warn-and-continue rather than
  halt-on-malformed unless the artifact is safety-critical (in which
  case Principle XXIV in the constitution governs).
- **Predictable output tree**: output emitters SHOULD write to
  paths derivable from the config. A reviewer SHOULD be able to
  predict the output tree from `deliberator.yml` alone.
- **Shallow hierarchies**: prefer `{agent}/review.md` to deeper
  structures unless the depth is justified by the underlying data.

## Why operational guidance, not constitutional

The core sentence "readability counts" is irreducibly subjective —
two reviewers can read the same output and disagree on whether it
satisfies the convention, with no mechanical resolution. Under the
v2.4.0 Constitutional Inclusion Criteria, that subjectivity makes
the discipline a poor constitutional invariant but a perfectly
useful authoring guide. The substantive content survives here with
its judgment-laden parts framed as SHOULDs and the
mechanically-checkable parts framed as RECOMMENDED patterns.

The constitution retains all of the load-bearing structural
properties output emitters depend on (Principle V on observability,
Principle VII on reproducibility, Principle XV on plugin isolation,
Principle XXIV on safety-critical defense-in-depth). The
"readability" overlay is the operational layer that those
constitutional invariants do not address.

---

*Migrated from CONSTITUTION.md Principle X in v2.6.0 → v3.0.0 per
spec 070 cycle 2 (2026-05-01).*
