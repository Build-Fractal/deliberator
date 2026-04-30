I'll read the relevant files before producing my review.

Now let me read the actual auth.py to get exact line numbers:

I now have everything I need. Here is my review:

---

### Executive Summary

SC-004 retrofits `CredentialStore` (`engine/auth.py:73–118`) to split a monolithic JSON file into per-provider files. The conservative strategy is structurally sound in its intent, but it has three categories of real failure: a token-loss race condition that exists in the current `save()` implementation and is not neutralized by the `.tmp`-rename pattern; a Windows correctness bug in the rename primitive chosen; and an information-disclosure leak from unspecified directory permissions. These are not hypothetical edge cases — they are reproducible by any user running two concurrent conversus processes, any Windows user, and any user on a shared Linux host. The strategy must address all three before shipping.

The Q1/Q2/Q3/Q4 decision points are secondary to these implementation gaps. Fix the primitives first; then the policy decisions become tractable.

**Most important recommendation**: Replace `os.rename` with `os.replace` and chmod the `.tmp` file to 600 *before* the rename, not after — this closes two independent bugs in a single change.

---

### Alignment

- **Atomic rename intent** (QUESTION.md L21): Using `.tmp` → final rename is the correct primitive for crash safety. Aligns with the existing `_write_all()` discipline at `auth.py:94–95`. The goal is right even if the implementation needs correction.

- **Legacy preservation** (QUESTION.md L20, L29): Preserving `auth.json` and never deleting it is consistent with the existing `CredentialStore.clear()` semantics — that method exists as an explicit opt-in. Not invoking it silently aligns with the principle that conversus does not delete user-owned files unilaterally.

- **Fallback-before-read** (QUESTION.md L17): Checking `credentials/{provider}.json` first, then falling back to `auth.json[provider]`, is the correct read-precedence order. It makes the new path the source of truth once populated, without invalidating old installations immediately.

- **Per-provider granularity** (QUESTION.md L34): Lazy migration's blast radius advantage is real. The existing `CredentialStore` is provider-keyed (`get(provider)`, `save(provider, ...)`), so lazy migration maps cleanly onto the existing interface without structural changes.

---

### Missed Opportunities

- **chmod race on the `.tmp` file**: The current `_write_all()` at `auth.py:94–95` writes plaintext then chmods. For `.tmp` files, `write_text()` creates the file with umask-derived permissions (typically 644). Between creation and `chmod`, the credentials are world-readable. The strategy doesn't require the `.tmp` to be created with `O_CREAT` + 600 permissions upfront. Fix: open `.tmp` with `os.open(..., flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL, mode=0o600)` before writing content. **Impact: high** — credentials exposed in a window that exists on every write.

- **`os.rename` vs `os.replace` on Windows**: On Windows, `os.rename(src, dst)` raises `FileExistsError` if `dst` already exists (e.g., from a previous migration attempt). `os.replace()` has POSIX-like atomic semantics on Windows (available since Python 3.3). The strategy names `os.rename` explicitly (QUESTION.md L21) but this fails the second time migration is attempted on Windows. Fix: mandate `os.replace()` throughout. **Impact: high** — migration silently fails for all Windows users on re-run.

- **Concurrent save() + migration race**: `CredentialStore.save()` at `auth.py:102–106` is a read-modify-write cycle with no lock. Scenario: Process A calls `get("anthropic")`, finds no per-provider file, reads `auth.json`, starts writing `anthropic.json.tmp`. Process B (token refresh) calls `save("anthropic", fresh_creds)`, writes `credentials/anthropic.json` successfully. Process A's `os.replace("anthropic.json.tmp", "anthropic.json")` now overwrites B's fresh token with the stale pre-migration token. Result: user's refreshed token is silently replaced with an expired token. **Impact: high** — this is undetectable data corruption under token refresh + concurrent access.

- **`credentials/` directory permissions not specified**: The strategy specifies `chmod 600` for JSON files but says nothing about the directory. Default umask gives new directories `0o755` (world-listable). On a shared host, any user can run `ls ~/.conversus/credentials/` to enumerate which providers the user has OAuth credentials for — even without reading the files. Fix: `mkdir(credentials_dir, mode=0o700, exist_ok=True)`. **Impact: medium** — information disclosure on multi-user systems.

- **`_read_all()` swallows `PermissionError`**: At `auth.py:88`, `OSError` is caught and returns `{}` silently. If `credentials/anthropic.json` exists but is unreadable (e.g., created with wrong permissions by a failed migration attempt), `get("anthropic")` returns `None` rather than signaling an error. Conversus then falls back to `auth.json`, silently reading stale credentials. The user sees "authentication required" with no indication that a credential file exists but is inaccessible. Fix: re-raise `PermissionError` separately from `json.JSONDecodeError`. **Impact: medium**.

- **Lazy migration + permanent fallback = invisible orphan providers** (Q2B + Q3A): If lazy, providers never explicitly invoked in conversus remain unmigrated forever. Combined with a permanent fallback, this is stable but creates an invisible split-state: `conversus status` (which now shows settings cascade per SC-003) would be inconsistent if it doesn't also reflect credential source. A user auditing their credential state cannot tell which providers came from `auth.json` vs `credentials/`. Fix: `conversus status` should report credential source per-provider. **Impact: medium**.

- **NFS/SMB rename non-atomicity** (QUESTION.md L44): NFSv3 `rename(2)` is not atomic across server crash. This is real for corporate environments where home directories are NFS-mounted. The atomic-rename pattern only protects against process crash, not filesystem failure. A transaction log is overkill, but checking for orphaned `.tmp` files on startup and logging a warning is achievable. **Impact: low** — rare but unrecoverable without manual intervention.

---

### Off-Base Assumptions

- **"Atomic-rename survives interrupt" — stated too broadly** (QUESTION.md L21–22): The strategy claims `.tmp` → rename is sufficient. It is sufficient for process crash. It is NOT sufficient for filesystem non-atomicity (NFS) or for the concurrent-save race described above. The strategy should narrow its safety claim to "protects against single-process crash on a local POSIX filesystem."

- **"Legacy auth.json read-only after cutover" — not enforced** (QUESTION.md L18): The strategy says "Legacy `auth.json` is never written after the cutover." But `CredentialStore` is initialized with `DEFAULT_AUTH_PATH` (`auth.py:80`). Nothing in the implementation prevents old code paths (or test fixtures) from instantiating `CredentialStore()` with the default path and writing to `auth.json` post-migration. The "never written" guarantee requires either removing the default path or making the new `CredentialStore` reject writes to the legacy path explicitly.

---

### Actionable Recommendations

1. **Use `os.replace()` not `os.rename()`** (Priority: P1)
   - **Current state**: QUESTION.md L21 specifies `os.rename`.
   - **Proposed change**: Replace all migration rename calls with `os.replace(tmp, final)`.
   - **Rationale**: `os.rename` raises `FileExistsError` on Windows when destination exists; `os.replace` is atomic and cross-platform.
   - **Risk if ignored**: Migration fails silently on Windows on every re-run after the first.

2. **Chmod `.tmp` to 600 before writing content** (Priority: P1)
   - **Current state**: Current `_write_all()` at `auth.py:95` chmods after write.
   - **Proposed change**: Create `.tmp` via `os.open(..., os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)`, write, then rename.
   - **Rationale**: Eliminates the world-readable window between file creation and chmod.
   - **Risk if ignored**: Credentials exposed to co-resident processes on every write.

3. **Add process lock around migration read + rename** (Priority: P1)
   - **Current state**: No concurrency guard on lazy migration or `save()` (auth.py:102–106).
   - **Proposed change**: Use `fcntl.flock` (POSIX) / `msvcrt.locking` (Windows) on the per-provider file during migration.
   - **Rationale**: Eliminates the concurrent-save race where a fresh token is overwritten by a migrating stale token.
   - **Risk if ignored**: Token refresh under concurrent access silently corrupts credentials.

4. **Create `credentials/` directory with mode 0o700** (Priority: P2)
   - **Current state**: Strategy omits directory permissions.
   - **Proposed change**: `credentials_dir.mkdir(parents=True, exist_ok=True, mode=0o700)`.
   - **Rationale**: Prevents enumeration of credential providers by co-resident users.
   - **Risk if ignored**: Information disclosure on any shared host.

5. **Re-raise `PermissionError` from `_read_all()`** (Priority: P2)
   - **Current state**: `auth.py:88` catches all `OSError` including `PermissionError`.
   - **Proposed change**: Catch `json.JSONDecodeError` and `FileNotFoundError` silently; let `PermissionError` propagate.
   - **Rationale**: Unreadable credential files should surface immediately, not silently fall through to stale legacy data.
   - **Risk if ignored**: Corrupted-permission migration leaves user silently authenticating with expired tokens.

6. **Verdict on Q1: Preserve, never delete** (Priority: P2)
   - **Current state**: Undecided (QUESTION.md L26–30).
   - **Proposed change**: Adopt Position B. Add a post-migration log line: "Legacy auth.json preserved; credentials now in ~/.conversus/credentials/. Remove legacy file manually when ready."
   - **Rationale**: Consistent with SC-001 pattern. User-visible log reduces "why does this file still exist" confusion without silent deletion.
   - **Risk if ignored**: Position A risks data loss if migration verification is incomplete.

7. **Verdict on Q2: Eager migration** (Priority: P2)
   - **Current state**: Undecided (QUESTION.md L31–35).
   - **Proposed change**: Adopt Position A (eager, on first conversus invocation). Lazy migration creates permanent split-state where untouched providers never migrate; combined with a time-bounded fallback (Q3), this silently breaks them.
   - **Rationale**: Eager migration is one-shot and deterministic. The atomic-rename pattern makes it safe to migrate all providers at once.
   - **Risk if ignored**: Lazy + time-bounded fallback = silent breakage for any provider not accessed in N releases.

8. **Verdict on Q3: Time-bounded fallback with explicit warning** (Priority: P2)
   - **Current state**: Undecided (QUESTION.md L36–39).
   - **Proposed change**: Adopt Position B. Emit a deprecation warning after 3 releases; remove fallback in the 4th. Provide `conversus migrate-credentials` as an explicit migration command.
   - **Rationale**: Permanent fallback creates permanent attack surface (even if minimal) and prevents `conversus status` from giving a clean credential-source report.
   - **Risk if ignored**: Permanent fallback means migration is never truly complete; operational state stays ambiguous indefinitely.

9. **Verify migration before returning from `get()`** (Priority: P3)
   - **Current state**: Migration copies credentials then reads from new file (implied by strategy).
   - **Proposed change**: After `os.replace()`, immediately `_read_all()` the new per-provider file and compare provider key count/token field to source. If mismatch, log error and fall back to legacy without marking migration complete.
   - **Rationale**: Surfaces filesystem-level silent failures (NFS partial write) before the user loses authentication.
   - **Risk if ignored**: NFS/SMB corruption leaves user with an empty per-provider file and no fallback.

---

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/engine/auth.py` — L64 (DEFAULT_AUTH_PATH), L73–118 (CredentialStore), L82–89 (_read_all), L91–95 (_write_all), L102–106 (save), L114–117 (clear)
- `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/057-sc4-migration-strategy-2026-04-30/QUESTION.md` — L17–22 (conservative strategy), L26–44 (decision points Q1–Q4)