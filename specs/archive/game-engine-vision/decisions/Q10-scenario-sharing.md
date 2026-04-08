# Q10: Scenario replay across teams — shared scenarios?

**Status**: Decided
**Decision**: No sharing infrastructure (Option A). Scenarios are files; git handles distribution.

---

## Context

Open Question #10 from spec 007 Section 13:

> "Can team A publish their 'code review decision framework' scenario for team B to use? This implies a scenario marketplace or registry."

## Decision

**Scenarios are local YAML files (per Q07). Teams share by copying files or committing to shared repos. No marketplace, no registry.**

Git already handles distribution. A marketplace is a future product decision, not a v1 architecture decision.

## Rejected Alternatives

- **Git-based sharing infrastructure** rejected: unnecessary tooling when `cp` and `git` already work
- **Scenario marketplace** rejected: premature product-on-top-of-product before the base product has users
