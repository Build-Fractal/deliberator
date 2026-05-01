# Spec Execution Order — DEPRECATED

**Status**: DEPRECATED 2026-05-01.

This file was last meaningfully updated 2026-04-02 with a Wave-1/Wave-2 sequencing focused on getting to spec 032 (package splitting). All Wave-1/Wave-2 specs have shipped; subsequent work has not been tracked here.

## Source of truth — use these instead

- **`specs/STATUS.md`** — canonical index of active / closed / draft / archived specs with current status lines. Refreshed 2026-05-01.
- **`specs/README.md`** — spec lifecycle conventions (`draft/ → active → done/`).
- **`git log specs/done/`** — chronological closure history.
- **`CONSTITUTIONAL_CONVERSATIONS.md`** — governance/amendment history with deliberation cross-references.

## Why deprecated, not deleted

This file is preserved as a historical artifact:
- The Wave-1/Wave-2 sequencing (Apr 1-3 sprint to spec 032) was a real strategic decision that shaped the early plugin/package architecture.
- Future archaeology may benefit from reading the original wave plans alongside their actual closure dates.
- The pattern of "execution-order documents going stale within weeks" is itself a methodology lesson worth preserving for future contributors.

If a future maintainer wants to revive an active execution-order document:
- Use `STATUS.md`'s "Most actionable next moves" section as the new home.
- Or auto-generate sequencing from spec dependency graphs at build time.
- Manually-maintained ordering documents accumulate drift — see Principle XI (single source of truth) and the 2026-04-27 audit's notes on STATUS.md staleness for the case study.
