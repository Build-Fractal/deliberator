I'll read the QUESTION.md file before writing my review.

### Executive Summary

SC-004 closes spec 057 by migrating credential storage from a monolithic `~/.conversus/auth.json` to per-provider files under `~/.conversus/credentials/{provider}.json`. The migration is a one-time data reshaping problem with a permanently load-bearing constraint: any user with existing OAuth credentials must not lose authentication on the first invocation after the PR lands. The conservative strategy described in the proposal is structurally sound and its instincts are correct in all four decision areas, but it has two concrete implementation gaps — directory creation and file permissions — that are not mentioned anywhere in the proposal and will cause failures in clean environments and on security-conscious systems respectively.

The proposal correctly reaches for atomic rename, permanent fallback, and legacy preservation. These are the right defaults for a CLI tool with a small but real user base and no central update coordination. The eagerness debate (Q2) is the one place where the proposal leaves the decision genuinely open; lazy is the right answer for reasons that become clear when you trace the three-provider scenario. The time-bounded fallback (Q3, Position B) is appealing in theory but is the single item most likely to generate a future breaking bug report six months from now.

**Most important recommendation: add explicit `os.makedirs(credentials_dir, mode=0o700, exist_ok=True)` before the first write, and set `0o600` permissions on every newly written credential file — these are not addressed anywhere in the proposal and will be the most likely failure mode in practice.**

### Alignment

- **Atomic-rename primitive** (spec L21): Using `.tmp` + `os.rename` is the correct primitive for crash-safe single-file writes. `os.rename` is atomic on POSIX filesystems within the same directory, which is exactly the case here since `.tmp` and the final file share the `credentials/` directory. This approach handles interruption correctly and is idiomatic.

- **Read-path fallback precedence** (spec L17): Checking `credentials/{provider}.json` first and falling back to `auth.json[provider]` is the correct ordering. New writes always go to the new location; reads degrade gracefully. This pattern allows incremental migration without a flag day and is well-established in config migration practice.

- **Legacy preservation over deletion** (spec L20, Position B of Q1): Preserving `auth.json` is the right call for a local-only CLI tool. The blast radius of a deletion bug (user loses all credentials) dwarfs the blast radius of stale-file confusion (user edits a file that has no effect). SC-001 set the precedent with `settings.json` — consistency with that decision also matters for user trust.

- **No `.bak` rename** (spec L22): Renaming to `.bak` would create a confusing artifact (users would wonder why there are two files, whether `.bak` is active). Leaving the original in place is simpler and more transparent.

- **Per-provider isolation at the file level** (spec L3-5): Storing credentials in `{provider}.json` rather than a single multi-provider JSON means a corrupted write for one provider cannot corrupt credentials for another. This is a structural safety property the monolithic approach does not offer.

### Missed Opportunities

- **Directory creation is not addressed**: The proposal writes to `~/.conversus/credentials/{provider}.json` but never mentions creating `~/.conversus/credentials/`. On a clean install or when a user has only set environment-variable credentials, this directory will not exist. The first write will fail with `FileNotFoundError`. Every code path that writes a credential file must call `os.makedirs(credentials_dir, mode=0o700, exist_ok=True)` before the write. Impact: **high** — this is a runtime crash in a common scenario.

- **File permissions are not mentioned**: OAuth tokens stored in `{provider}.json` are sensitive credentials. The proposal says nothing about what permissions are set on newly created files. On most systems, a file created with `open()` defaults to `0o644` (world-readable). Credential files should be written with `0o600`. This can be done by opening with `os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)` or by calling `os.chmod` immediately after the rename. The `.tmp` file should also be created with `0o600`. Impact: **high** — world-readable credential files violate standard security practice for token storage.

- **Provider name sanitization is not mentioned**: The proposal uses the provider name directly as a filename component (`{provider}.json`). If a provider name ever contains `/`, `..`, or other path characters, this becomes a path traversal issue. A one-line sanitization — reject or strip any provider name that does not match `[a-zA-Z0-9_-]+` — closes this permanently. In practice, provider names are controlled by the codebase, so this is low probability but zero-cost to fix. Impact: **medium** — low probability, trivial to close.

- **Empty or malformed `auth.json` handling**: The proposal does not specify what `migrate_provider` does if `auth.json` exists but contains malformed JSON, or if the provider key is present but its value is `null` or an empty dict. The lazy migration path must handle `json.JSONDecodeError` and skip migration (log a warning, fall through to returning no credentials) rather than crashing. Impact: **medium** — corrupted state in the old file should not break first invocation.

- **One-time deprecation warning on fallback trigger**: The proposal specifies a permanent fallback (correct) but does not suggest any user-visible signal when the fallback fires. A single-line log message — "Note: credentials for {provider} loaded from legacy auth.json; they will be migrated to credentials/{provider}.json" — emitted once per provider per migration event would give users visibility without nagging them. This costs two lines of code and substantially improves debuggability. Impact: **low** — nice-to-have observability.

### Off-Base Assumptions

- **"Atomic rename within same directory" is assumed without verifying `.tmp` placement**: The atomic guarantee of `os.rename` holds only when source and destination are on the same filesystem. The proposal says "write to `credentials/{provider}.json.tmp`" but does not explicitly state the `.tmp` file is written inside the `credentials/` directory. If any implementation writes the `.tmp` to a different location (e.g., the system temp directory), the rename crosses filesystem boundaries and atomicity breaks. The implementation must write `.tmp` to `credentials/{provider}.json.tmp` — same directory as the final destination.

- **"Best-effort lazy migration" implies silent failure is acceptable** (spec L19): The phrase "best-effort" is load-bearing here and the proposal does not define what happens when migration fails. If the file copy fails (permissions error, disk full), does conversus fall back to reading the legacy file directly? Does it surface an error? Does it leave a partial `.tmp` file? The conservative strategy is incomplete without specifying the failure behavior. The correct answer is: on migration failure, log a warning, fall back to reading from `auth.json[provider]` directly (no new file written), and retry on the next invocation. This is safe because the write-path guarantee (new files only) is separate from the migration trigger.

### Actionable Recommendations

1. **Add directory creation with secure permissions** (Priority: P1)
   - **Current state**: Proposal mentions writing to `credentials/{provider}.json` but does not address directory existence (spec L21).
   - **Proposed change**: Any function that writes a credential file must begin with `os.makedirs(Path.home() / ".conversus" / "credentials", mode=0o700, exist_ok=True)`. This must precede the `.tmp` write.
   - **Rationale**: Without directory creation, the first write on a clean install or credentials-less system will raise `FileNotFoundError` and crash conversus. `mode=0o700` ensures the directory itself is not world-accessible.
   - **Risk if ignored**: First-run crash on clean systems; any system where the user has never stored credentials via conversus before SC-004 lands.

2. **Enforce 0o600 permissions on credential files** (Priority: P1)
   - **Current state**: No mention of file permissions anywhere in the proposal.
   - **Proposed change**: Write `.tmp` using `os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)`, write content, close, then `os.rename(tmp_path, final_path)`. This ensures the file is never visible at `final_path` with wrong permissions.
   - **Rationale**: OAuth tokens are sensitive. Default `open()` permissions are world-readable on most systems. Token exposure violates standard security practice.
   - **Risk if ignored**: Credential files are world-readable on multi-user systems or systems with permissive umask defaults.

3. **Define migration failure behavior explicitly** (Priority: P1)
   - **Current state**: "best-effort lazy migration" (spec L19) leaves failure behavior unspecified.
   - **Proposed change**: On migration failure (any exception during the copy or rename): catch, log a single-line warning ("Failed to migrate credentials for {provider}: {error}. Will read from legacy auth.json this session."), and fall back to reading from `auth.json[provider]` directly. Do not propagate the exception. Do not leave a partial `.tmp` file (clean it up in the except block with `unlink(missing_ok=True)`).
   - **Rationale**: Migration failure must not break authentication. The fallback path already exists; the question is just whether failure is handled or crashes.
   - **Risk if ignored**: Any transient I/O error during migration crashes conversus on the invocation that should be transparent.

4. **Choose lazy migration** (Q2 verdict, Priority: P1)
   - **Current state**: Q2 is left open between eager and lazy (spec L31-34).
   - **Proposed change**: Adopt lazy (Position B). Migration triggers per-provider on first read of that provider's credentials.
   - **Rationale**: In the three-provider scenario (Anthropic OAuth + OpenAI env + Gemini OAuth): eager migration on first invocation runs all migrations at startup, before the user has done anything. If Anthropic migrates but Gemini fails, the next invocation reads Gemini from legacy (correct via fallback). But with lazy, each provider migrates only when needed — a `conversus status` that touches only Anthropic credentials never even attempts to migrate Gemini. The failure blast radius per operation is smaller, and the test surface is narrower. OpenAI in env never touches the file layer at all. Lazy also means migration code only runs on the hot path where it would need to fail gracefully anyway (credential reads), so the exception handler is already in context.
   - **Risk if ignored**: Eager migration at startup creates a multi-step operation with multiple failure points before the user has issued any command, which is the worst time to fail.

5. **Adopt permanent fallback** (Q3 verdict, Priority: P2)
   - **Current state**: Q3 is left open between permanent (Position A) and time-bounded (Position B) (spec L37-39).
   - **Proposed change**: Adopt permanent fallback (Position A). The fallback is a read-only JSON lookup. Its maintenance burden is a single `if path.exists()` check plus a dict key access. Time-bounded fallback requires version tracking, a deprecation warning system, and a hard-removal PR that will inevitably land when a long-dormant user upgrades.
   - **Rationale**: The cost of the permanent fallback is essentially zero. The cost of a time-bounded fallback breaking a user who upgraded after six months and never ran a migration command is high. This is a local CLI tool, not a service with forced upgrades.
   - **Risk if ignored**: Time-bounded fallback will eventually produce "my credentials disappeared after an upgrade" bug reports from users who did not run `conversus migrate-credentials` before the cutover.

6. **Confirm atomic rename uses same-directory `.tmp`** (Q4, Priority: P2)
   - **Current state**: Proposal specifies `.tmp` + `os.rename` but does not specify where `.tmp` is written (spec L21).
   - **Proposed change**: Explicitly document and enforce in code that the `.tmp` file is always written as `credentials/{provider}.json.tmp` — same directory as the final destination, never in `/tmp` or any other location.
   - **Rationale**: `os.rename` is atomic only within the same filesystem/directory. Cross-filesystem rename silently falls back to copy+delete, losing atomicity.
   - **Risk if ignored**: If any implementation variant writes to a different directory, the atomicity guarantee silently disappears.

7. **No transaction log** (Q4 verdict, Priority: P2)
   - **Current state**: Q4 asks whether `.tmp` + `os.rename` is sufficient or whether a transaction log is needed (spec L44).
   - **Proposed change**: Confirm the proposal: no transaction log. The atomic-rename pattern is sufficient.
   - **Rationale**: The invariant after a crash is clean: either `{provider}.json` exists and is valid (migration succeeded), or it does not exist (migration never completed or `.tmp` was written but rename didn't happen). In both cases, the next invocation correctly falls back to `auth.json`. A `.tmp` left behind is harmless and gets overwritten on retry. A transaction log would need to track which providers were migrated successfully, handle its own crash during write, and add complexity to the read path. The cost is not justified when the idempotent fallback already handles partial state correctly.
   - **Risk if ignored**: Over-engineering that adds failure surface without improving the actual safety guarantee.

8. **Sanitize provider names before use as filenames** (Priority: P3)
   - **Current state**: Provider names are used directly as filename components (spec L3, implied by `{provider}.json`).
   - **Proposed change**: Add a one-line validation: assert provider names match `[a-zA-Z0-9_-]+` and raise `ValueError` on invalid names. This can be in the `CredentialStore` constructor or in the path-construction helper.
   - **Rationale**: Provider names are internal constants today, but adding a one-line guard permanently closes path traversal as a concern with no maintenance cost.
   - **Risk if ignored**: Low-probability path traversal if provider name handling ever becomes more dynamic.

**Verdict: Modify the conservative strategy as follows:**
1. Add `os.makedirs` with `mode=0o700` before first write.
2. Write credential files with `0o600` permissions.
3. Specify explicit failure behavior for failed migration (warn + fall back + clean `.tmp`).
4. Choose lazy migration (Q2: Position B).
5. Choose permanent fallback (Q3: Position A).
6. Confirm `.tmp` is same-directory (Q4: no transaction log needed).

The conservative strategy as written would ship successfully on any system where the `credentials/` directory already exists and the user does not care about file permissions. On a clean system or a security-conscious one, it fails at first write. These are not hypothetical failure modes — they are the most likely first-run scenario.

### Referenced Documentation

- `QUESTION.md` — all sections: L1-57 (full document reviewed)