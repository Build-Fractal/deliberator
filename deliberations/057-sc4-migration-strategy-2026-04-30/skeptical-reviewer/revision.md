Reading all four files before producing the revision.

All files were provided inline in the prompt. I have everything needed to produce the revision.

### Recommendation Dispositions

#### Recommendation 1: Use `os.replace()` not `os.rename()`

- **Original position**: Replace all `os.rename` calls with `os.replace(tmp, final)` to fix a Windows correctness bug where `os.rename` raises `FileExistsError` when the destination already exists.
- **Disposition**: Surviving
- **Explanation**:
  The pragmatist cross-review ("Dangerous Contradictions: `os.rename` vs. `os.replace`") yields entirely: "Pragmatist should yield entirely here. `os.replace` is the correct primitive; it subsumes `os.rename` on POSIX and fixes Windows. This is a one-word change with no trade-off." No challenge to the substance of this recommendation exists anywhere in the cross-review corpus. The pragmatist's own Alignment section implicitly endorsed `os.rename` as correct for POSIX without addressing Windows; that gap is now acknowledged. This remains P1.

---

#### Recommendation 2: Chmod `.tmp` to 600 before writing content

- **Original position**: Create `.tmp` via `os.open(..., os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)` to eliminate the world-readable window between file creation and chmod.
- **Disposition**: Modified
- **Explanation**:
  The pragmatist cross-review ("Tensions: `O_EXCL` vs. `O_TRUNC` in `os.open`") correctly identifies that `O_EXCL` is wrong for this use case: "an orphaned `.tmp` from a previous crash is stale data that should be overwritten — it has no integrity guarantee. `O_EXCL` would require explicit orphan handling (detect, delete, retry) on each migration attempt." This is a genuine error in my original reasoning. I specified `O_EXCL` as a defense against orphaned temp files, but an orphaned `.tmp` contains stale pre-migration data and should be unconditionally overwritten, not treated as an error.

  The security goal — mode 0o600 set at file creation, not post-rename — is preserved by `O_TRUNC`. The updated recommendation: create `.tmp` via `os.open(tmp_path, os.O_WRONLY|os.O_CREAT|os.O_TRUNC, 0o600)`, write content to the returned file descriptor, close, then `os.replace(tmp, final)`. This eliminates the world-readable window while handling stale orphan `.tmp` files correctly.

---

#### Recommendation 3: Add process lock around migration read + rename

- **Original position**: Use `fcntl.flock` (POSIX) / `msvcrt.locking` (Windows) on the per-provider file during migration to prevent the concurrent-save race.
- **Disposition**: Modified
- **Explanation**:
  The pragmatist cross-review ("Dangerous Contradictions: Concurrency Lock") accepts the lock as necessary but adds a critical UX caveat: "the lock must be advisory and non-blocking with a short timeout (e.g., 200ms), not a hard block. A CLI should not hang indefinitely waiting for a file lock from another conversus process. If the lock cannot be acquired, skip migration (fall back to legacy), log a warning, and retry on next invocation."

  This modification is correct. A CLI tool that blocks on a file lock for an arbitrary duration is regressive. The concurrent-save race is real and the fix is right; the behavior when the lock is contended is what I failed to specify. The updated recommendation: acquire `fcntl.flock(LOCK_EX|LOCK_NB)` with a 200ms retry budget. If the lock cannot be acquired within 200ms, skip migration for this invocation, fall back to `auth.json[provider]` for this session, and log: "Migration lock unavailable for {provider}; will retry on next invocation." On lock acquisition, execute the read-copy-replace atomically. Release the lock in a `finally` block that also cleans up any orphaned `.tmp`.

---

#### Recommendation 4: Create `credentials/` directory with mode 0o700

- **Original position**: `credentials_dir.mkdir(parents=True, exist_ok=True, mode=0o700)` before the first write to prevent directory enumeration on shared hosts.
- **Disposition**: Surviving
- **Explanation**:
  The pragmatist cross-review ("Safe Agreements: Directory creation with 0o700 mode") treats this as the single strongest finding from the deliberation: "Both reviews reach this finding from different analytical approaches… The fact that two reviewers with different threat models independently converge on the same missing implementation detail with the same proposed mode (0o700) is strong signal." No cross-review challenges this recommendation. The pragmatist elevates it to P0 in the synthesis framing; I will retain P1 but note the consensus. The QUESTION.md proposal does not mention directory creation at all, making this a mandatory addition regardless of other decisions.

---

#### Recommendation 5: Re-raise `PermissionError` from `_read_all()`

- **Original position**: Catch `json.JSONDecodeError` and `FileNotFoundError` silently; let `PermissionError` propagate to the caller.
- **Disposition**: Modified
- **Explanation**:
  The pragmatist cross-review ("Tensions: `PermissionError` Re-Raising vs. Graceful Degradation") proposes a middle path that is better than hard propagation: "log `PermissionError` at WARNING level (not silent, not crash), skip the per-provider file, fall back to legacy for this session, and surface a user-visible message: 'credentials/{provider}.json exists but is not readable (permission denied); check file permissions.'"

  My original recommendation to propagate the exception is too harsh. A CLI user whose credential file has wrong permissions should receive a clear, actionable message — not an unhandled exception traceback. However, I reject the pragmatist's "warn-and-degrade" model as stated in their Recommendation 3, which would silently fall back without surfacing the problem at all. The correct behavior is: log at WARNING with an explicit user-visible line naming the file and the permission problem, then fall back to `auth.json[provider]` for this session only. The fallback should not mark the per-provider migration as complete so that the issue is surfaced again on next invocation until the user fixes permissions.

  Updated recommendation: in `_read_all()`, catch `FileNotFoundError` and `json.JSONDecodeError` silently and return `{}`; catch `PermissionError` separately, emit a WARNING with the file path and a "check file permissions" message, and return `{}` (allowing fallback) — but do not mark the provider as migrated, ensuring the warning recurs.

---

#### Recommendation 6: Verdict on Q1: Preserve, never delete

- **Original position**: Adopt Position B (preserve `auth.json`, never delete). Add a post-migration log line informing users of the new location.
- **Disposition**: Surviving
- **Explanation**:
  The pragmatist cross-review ("Safe Agreements: Q1 Preserve") affirms: "Both reviews endorse preserving auth.json without deletion… both note that the SC-001 PR set precedent by preserving orphan settings.json. The two rationales are complementary: one is forward-looking risk management, one is backward-looking consistency with existing user trust expectations." No cross-review challenges this. The SC-001 precedent argument is now explicitly reinforced from both directions. Position B is the correct call and survives without modification.

---

#### Recommendation 7: Verdict on Q2: Eager migration

- **Original position**: Adopt Position A (eager, all-providers on first invocation). One-shot, deterministic, and consistent.
- **Disposition**: Modified
- **Explanation**:
  The pragmatist cross-review ("Dangerous Contradictions: Q2 Migration Eagerness") offers a cooperative resolution: "adopt lazy migration (smaller failure blast radius, consistent with the read-path fallback already in place) but add a one-time startup sweep that logs which providers remain unmigrated, without acting on them. This gives skeptical-reviewer's observability concern without eager migration's all-or-nothing failure mode."

  I argued in my cross-review of the pragmatist that with a file lock in place, eager becomes strictly safer because the lock scope is cleaner at startup. The pragmatist's cross-review does not rebut this directly; it instead reframes the blast-radius argument: if provider B's migration fails during an eager all-at-once startup sweep, it shouldn't interfere with provider A's already-successful migration. This is valid regardless of locking. Eager migration's failure mode is provider-correlated: a partial I/O failure at startup could leave the migration loop in an inconsistent state across providers. Lazy migration's failure mode is provider-isolated by construction.

  I yield on Q2. The correct position is: **lazy migration, per-provider on first read, with a startup sweep that logs which providers in `auth.json` have not yet been migrated to `credentials/`.** The startup sweep is read-only (no writes, no migration) — it is observability only, not action. This satisfies my original concern about invisible split-state without the all-or-nothing failure exposure of eager migration.

---

#### Recommendation 8: Verdict on Q3: Time-bounded fallback with explicit warning

- **Original position**: Adopt Position B. Emit a deprecation warning after 3 releases; remove fallback in the 4th. Provide `conversus migrate-credentials` as an explicit migration command.
- **Disposition**: Modified
- **Explanation**:
  The pragmatist cross-review ("Dangerous Contradictions: Q3 Fallback Duration") correctly identifies the failure mode of time-bounded fallback: "if the fallback is genuinely time-bounded but the `conversus migrate-credentials` command is not shipped in the same PR, there is a release window where the fallback will expire before users have a migration escape hatch." This is a concrete regression risk I did not account for.

  My own cross-review of the pragmatist acknowledged: "adopt permanent fallback (pragmatist's position) but require conversus status to report credential source per-provider." I yield on the time-bounded expiry. A user who upgrades conversus after 7 months of inactivity should not find their credentials silently broken because the fallback window expired. The maintenance cost of a permanent fallback is one `if path.exists()` check — the pragmatist is correct that this is negligible.

  Updated position: adopt **permanent fallback (Position A)**, but address my operational-ambiguity concern through two concrete additions: (1) emit a single per-provider log line the first time `auth.json` is used as a fallback — "credentials for {provider} loaded from legacy auth.json; they will be migrated to credentials/{provider}.json on next direct access" — and (2) `conversus status` should report credential source per-provider ("anthropic: credentials/anthropic.json" vs "anthropic: auth.json [legacy]"). The `conversus migrate-credentials` command is deferred to a follow-on spec as a user-triggered convenience; it does not gate SC-004.

---

#### Recommendation 9: Verify migration before returning from `get()`

- **Original position**: After `os.replace()`, immediately `_read_all()` the new per-provider file and compare key count/token field to source. Fall back without marking migration complete if mismatch.
- **Disposition**: Modified
- **Explanation**:
  The pragmatist cross-review ("Tensions: Post-Migration Verification vs. No Over-Engineering") correctly resolves this tension: "If permanent fallback is adopted (pragmatist's Q3 position), a failed verification falls back to auth.json gracefully and the risk is low. Adopting permanent fallback resolves this tension by making verification optional rather than required."

  With permanent fallback now adopted (per my modified Rec 8), a silent NFS partial-write is handled by the fallback — the user stays authenticated, the migration simply doesn't advance for that session. The read-back verification adds a syscall on every migration event for a failure mode (NFS partial write on a developer CLI) that is rare enough that the fallback is adequate protection. I retain this as a P3 hardening item — something that should be implemented if the implementation cost is low — but I withdraw the framing that it is required for correctness. The correct framing: post-write verification is a defense-in-depth measure for NFS environments; permanent fallback is the primary safety net, and verification is an optional secondary layer.

---

### New Recommendations

- **Startup sweep logging unmigrated providers** (Priority: P2)
  - **Triggered by**: The Q2 resolution in the pragmatist cross-review ("Dangerous Contradictions: Q2 Migration Eagerness"), which proposes "a one-time startup sweep that logs which providers remain unmigrated, without acting on them." My modified Rec 7 adopts this, but the implementation detail warrants its own entry because it is a distinct code path from the lazy migration logic.
  - **Proposed change**: On conversus startup, read `auth.json` (if it exists) and diff its provider keys against the set of files present in `credentials/`. For any provider key in `auth.json` with no corresponding `credentials/{provider}.json`, emit a single INFO-level log: "Provider {provider} credentials have not been migrated to credentials/{provider}.json; migration will occur on next use." This sweep is read-only — it never writes, never migrates, never deletes. It runs once per startup and its output is deduplicated (no repeated log spam across invocations by storing a "sweep-reported" marker or using a log level that won't surface unless verbose mode is active).
  - **Rationale**: Without this sweep, lazy migration + permanent fallback produces invisible split-state. A user with three providers who only ever uses one will never see migration happen for the other two, and `conversus status` will silently serve them from `auth.json` indefinitely. The startup sweep provides the observability that prevents this from being a support mystery. It is the minimal implementation of my original "invisible orphan providers" concern without requiring `conversus status` schema changes in SC-004.

---

### Position Summary

Across nine original recommendations: two survive unchanged (Rec 1: `os.replace`, Rec 6: Q1 preserve), five are modified (Rec 2: `O_TRUNC` not `O_EXCL`; Rec 3: non-blocking lock with 200ms timeout; Rec 5: WARNING-level PermissionError with fallback; Rec 7: lazy not eager; Rec 8: permanent not time-bounded; Rec 9: downgraded to P3 optional), and zero are withdrawn. One new recommendation emerges (startup sweep).

The most significant change is the Q2/Q3 combination. My original position — eager migration plus time-bounded fallback — was internally consistent: if migration is eager and complete at startup, a time-bounded fallback is reasonable because all providers should have been migrated immediately. Once I yield on Q2 (lazy migration has better per-provider blast radius isolation), the time-bounded fallback becomes untenable: a provider that is never accessed will never be migrated under lazy, and a time-bounded fallback will eventually break it silently. The cross-review process forced me to see that my Q2 and Q3 positions were coupled, and yielding on Q2 required yielding on Q3. The pragmatist's cross-review of my work was correct to flag this as a dangerous contradiction rather than two independent tensions.

My highest-priority surviving recommendation is the combination of Rec 1 (`os.replace`) and Rec 4 (`credentials/` directory with mode 0o700). The directory creation issue is a runtime crash on first install that affects every user, QUESTION.md does not mention it anywhere, and both reviewers reached it independently from different analytical approaches. `os.replace` is a one-word change that prevents silent failure for every Windows user on every credential save after the first. These two items together are the minimal set that makes SC-004 shippable; every other recommendation in this revision is hardening on top of a working foundation.