# Feature Specification: Credential Source Display in `conversus status`

**Feature ID**: `072-credential-source-display`
**Created**: 2026-04-28
**Status**: Active 2026-04-30 — implementation PR (this branch).
**Depends On**: `057-settings-architecture` (SC-004 — per-provider credential files)
**Motivated by**: SC-004 deliberation verdict deferred per-provider source attribution to a follow-on spec because adding a column to a user-documented command interface requires its own contract.

---

## 1. Problem

After SC-004, each provider's OAuth credentials live in their own file at `~/.conversus/credentials/{provider}.json`, with a lazy-migration fallback to the legacy `~/.conversus/auth.json`. Environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) take precedence over both file-based stores when wiring a `ModelProvider`.

The `conversus status` command renders an auth-status table but does **not** tell the user *where* the effective credentials came from. When a user sees `logged in` for `anthropic`, they cannot distinguish between:

- a per-provider file (`credentials/anthropic.json`) that they deliberately wrote,
- a legacy `auth.json` entry that has not yet been migrated,
- an environment variable shadowing both files,
- or no credentials at all.

This is a debuggability gap: SC-003 already surfaces the settings cascade source per-key; SC-005 closes the same gap for credentials.

---

## 2. Goal

Add per-provider source attribution to the auth-status table rendered by `conversus status`. The column tells the user which of the four possible sources (per-provider file, legacy fallback, env var, none) supplied the effective credentials, and where on disk the source lives when applicable.

---

## 3. Source labels

| Label | Condition | `source_path` |
|---|---|---|
| `per-provider-file` | `credentials/{provider}.json` exists *and* contains `access_token` | `Path` to the per-provider file |
| `legacy-fallback` | per-provider file missing/empty *and* `auth.json` has the provider with `access_token` | `Path` to `auth.json` |
| `env-var` | both file paths absent *and* `OAUTH_CONFIGS[provider]["env_var"]` is set in `os.environ` | `None` |
| `none` | none of the above | `None` |

Resolution order matches `CredentialStore.get()` for files (per-provider beats legacy), then env var, then none. Note: this **inspection** order is the inverse of `resolve_provider`'s **runtime** order (which checks env var first); inspection reflects "where credentials are stored", not "what would be used at runtime". A future enhancement may add a "runtime-precedence" view; this spec is scoped to source-of-credentials.

---

## 4. Display

The existing 3-column auth-status table gains a 4th column:

| Provider | Status | Details | Source |

The Source column is colored to mirror the cascade table convention:

- `per-provider-file` → green
- `legacy-fallback` → yellow
- `env-var` → cyan
- `none` → dim

The 3 existing columns retain their current rendering exactly. The new column is purely additive — no existing test of the 3 original columns should require modification.

---

## 5. Implementation surface

- `engine/auth.py`: new pure helper `inspect_credential_source(provider, store=None) -> tuple[str, Path | None]`. No state, no I/O beyond reading the per-provider and legacy files (both already done by `CredentialStore`).
- `engine/handlers.py::status_cli`: remove the `# TODO(SC-005)` block, add the 4th column, call `inspect_credential_source` per provider.

---

## 6. Tests

Five unit tests for `inspect_credential_source` (in `engine/tests/test_auth.py`):

1. `test_inspect_credential_source_per_provider_file`
2. `test_inspect_credential_source_legacy_fallback`
3. `test_inspect_credential_source_env_var`
4. `test_inspect_credential_source_none`
5. `test_inspect_credential_source_per_provider_takes_precedence_over_legacy`

Three CLI integration tests for the column (in `engine/tests/test_cli.py::TestStatusCommand`):

1. `test_status_shows_credential_source_column` — header present.
2. `test_status_credential_source_per_provider_file` — label rendered for that provider.
3. `test_status_credential_source_env_var` — label rendered when env var is the only source.

All existing `TestStatusCommand` tests (8+) and cascade tests (5) continue to pass without modification.

---

## 7. Out of scope

- Migration prompts ("you have an unmigrated provider — run `conversus migrate-credentials`"). Spec 057 SC-004 already logs this at DEBUG.
- Runtime-precedence view (which credentials `resolve_provider` would actually pick).
- Source attribution in JSON output of `conversus status` (status_cli is the Rich-table surface; JSON variants would land in a separate spec when needed).
