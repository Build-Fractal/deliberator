# Q05: Should the free tier collect deliberation metadata to train paid tier models?

**Status**: Decided
**Decision**: Option D — local-only aggregation, no telemetry

---

## Context

Open Question #5 from spec 007 Section 13:

> "Should the free tier anonymously collect deliberation metadata (agent count, round count, convergence rate) to train the paid tier's models? Opt-in? Opt-out?"

## Options Considered

- **A: No collection** — paid tier models trained on paid users' data only
- **B: Opt-in telemetry** — free users can enable anonymous metadata sharing
- **C: Opt-out telemetry** — free tier collects anonymously by default, users can disable
- **D: Local-only aggregation** — no data leaves the machine, per-user history improves local predictions

## Decision

**Option D: Local-only. No telemetry. No data leaves the machine.**

- Convergence predictor works on current-run data (Round 1 features → predict Round 2). No population data needed.
- Config optimizer ships with pre-trained defaults from internal stress tests and published deliberation data.
- Per-user run history (stored in scenario objects, Q07) improves local predictions over time.
- No GDPR surface, no telemetry controversy, no "free users feed paid models" optics.

Population-level training is a good problem to have if adoption reaches that scale. If it does, introduce opt-in (Option B) with a clear value exchange. Cross that bridge when it exists.

## Rejected Alternatives

- **Options A/B/C** all deferred: premature to design telemetry infrastructure before the product has users. Local-only is the simplest path that still delivers value.
