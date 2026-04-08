# Phase 4 Disputes: schema-engineer

**Spec**: 030-domain-plugin-architecture

---

## Surviving Disputes

### DISPUTE 1: Scaffolds endpoint glob bug (Medium)

**Status**: Surviving -- consensus.

The API globs `*.json` but scaffolds are `*.yml`. Produces empty scaffolds endpoint for YAML-based domains.

### DISPUTE 2: scaffold_dir enforcement (Medium)

**Status**: Surviving -- architect and schema-engineer agree.

Missing scaffold_dir on a DomainPlugin subclass produces a confusing error.

### DISPUTE 3: JSON/YAML extension inconsistency (Medium)

**Status**: Surviving -- all agents acknowledge.

Base DomainPlugin.score() resolves `{scaffold}.json`, CodeReviewDomain.score() resolves `{scaffold}.yml`. Normalize to try multiple extensions or use a format-agnostic resolution.

## Withdrawn Disputes

- DomainScore.dimensions unboundedness: Non-issue (values clamped before storage)
- DomainRecord.convergence as str: Valid design choice for extensibility
