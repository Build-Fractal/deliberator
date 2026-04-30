# Spec 057 SC-004 Migration Strategy — Decision Document

## Context

Spec 057 SC-004 requires changing credential storage from monolithic `~/.conversus/auth.json` to per-provider files at `~/.conversus/credentials/{provider}.json`. The reopened spec 057's status line names the gap: "code stores monolithic `~/.conversus/auth.json`, spec requires per-provider files."

This is the **last unmet SC** for spec 057 (SC-001 + SC-003 are now in main). After SC-004 lands, spec 057 closes.

## What's at stake

The user running this deliberation (Brett) has a load-bearing `~/.conversus/auth.json` containing Anthropic OAuth credentials. The migration affects every conversus user with stored OAuth credentials. A botched migration would break authentication on next conversus invocation.

The session has shipped 18 PRs ratifying Principle XXVIII (Test-Fix Boundary Preservation) plus operational scaffolding. The discipline being tested here: do NOT make tests pass with weakened assertions; preserve real-behavior verification.

## Conservative migration strategy (proposed default)

1. **Read path**: when reading credentials for a provider, check `credentials/{provider}.json` first. Fall back to legacy `auth.json[provider]` if the per-provider file doesn't exist.
2. **Write path**: writes go to `credentials/{provider}.json` exclusively. Legacy `auth.json` is never written after the cutover.
3. **Migration trigger**: best-effort lazy migration on first read after this PR lands. If `auth.json` exists and a per-provider file is being requested, copy the relevant section to the new file before reading.
4. **Legacy preservation**: `auth.json` is preserved in place (never deleted by conversus). User can `rm` it themselves once they verify migration succeeded.
5. **Atomic safety**: write to `credentials/{provider}.json.tmp`, then `os.rename` to final path. If interrupted, the partial `.tmp` is harmless (just gets retried).
6. **No `.bak` rename**: don't rename the legacy file — leave it discoverable so users can verify content.

## Decision points the deliberation must rule on

### Q1 — Should the legacy `auth.json` be deleted after successful migration?

- **Position A (delete after migration)**: Once content is verified copied to new files, `auth.json` is dead weight. Stale credentials can be confusing if a user manually edits the legacy file expecting it to take effect.
- **Position B (preserve, never delete)**: User data is sacred. Conversus does not delete user-owned files without explicit confirmation. If a user wants the legacy file gone, they `rm` it themselves. Aligned with the SC-001 PR's pattern (preserved orphan settings.json).

### Q2 — Should migration be eager (on first conversus invocation) or lazy (on next read of a specific provider's credentials)?

- **Position A (eager)**: First conversus invocation after this PR lands triggers full migration of all providers in `auth.json`. Predictable, one-shot, easy to reason about.
- **Position B (lazy)**: Migration happens per-provider on first read of that provider. Slower migration but smaller failure blast radius — if migration fails for one provider, others are unaffected.

### Q3 — Should the legacy fallback read be permanent or time-bounded?

- **Position A (permanent fallback)**: `CredentialStore.get(provider)` always falls back to `auth.json[provider]` if the per-provider file is missing. Works forever; legacy file is read-only.
- **Position B (time-bounded fallback)**: Fallback works only for N releases (e.g., 6 months). After that, conversus emits a warning that legacy file will be ignored, and users must run `conversus migrate-credentials` explicitly.

### Q4 — What's the failure mode if migration partially succeeds (some providers migrated, others not)?

- The migration has to be safe under interrupt: if conversus crashes mid-migration, the next run must resume cleanly without corruption.
- Atomic-rename pattern (`.tmp` → final) is the proposed primitive. Is this sufficient, or do we need a transaction log?

## What deliberation agents should NOT do

- Re-litigate SC-004 itself. The spec is settled; the question is HOW to migrate, not WHETHER.
- Propose adding new SCs. SC-004's contract is bounded.
- Recommend deferring the migration. Spec 057 stays open until SC-004 lands.

## Acceptance bar

- 0 ACCEPT findings on the conservative strategy as written, OR
- A clear directional verdict on Q1/Q2/Q3/Q4 with grounded rationale.

If the deliberation finds the conservative strategy is correct as proposed, ship it as-is. If it finds a better strategy, the implementation amends before opening the PR.
