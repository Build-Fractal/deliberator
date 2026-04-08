# Q07: Scenario storage — git-tracked or database?

**Status**: Decided
**Decision**: File-based (Option A) until a database is needed

---

## Context

Open Question #7 from spec 007 Section 13:

> "File-based scenarios are git-friendly but don't scale for cross-team enterprise use. At what point does the transition to database storage happen?"

## Decision

**File-based. `scenarios/{id}.yml` in the project directory. Git-tracked.**

- Simple, portable, versionable
- No infrastructure dependencies
- Database when there's a concrete need, not before

## Rejected Alternatives

- **SQLite** and **export-to-DB** both premature — don't build query infrastructure before there are scenarios to query
