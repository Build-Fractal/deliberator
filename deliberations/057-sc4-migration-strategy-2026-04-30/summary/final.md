<!-- CONVERSUS:METADATA
agents: 2
agent_names: pragmatist-reviewer, skeptical-reviewer
mode: cooperative
phases_completed: 5
iterations: 1
round: 1
-->

### Process Summary

- **Agents**: 2 — pragmatist-reviewer, skeptical-reviewer
- **Total artifacts**: 8 (2 Phase 1 reviews + 2 Phase 2 cross-reviews + 2 Phase 3 revisions + 2 Phase 4 disputes)
- **Phase 1 reviews**: 2
- **Phase 2 cross-reviews**: 2
- **Phase 3 revisions**: 2
- **Phase 4 disputes**: 2
- **Recommendations proposed** (Phase 1 total): 17 (8 from pragmatist, 9 from skeptical)
- **Recommendations withdrawn** (Phase 3): 0
- **Recommendations modified** (Phase 3): 11 (5 pragmatist, 6 skeptical)
- **Recommendations surviving** (Phase 3): 6 (3 pragmatist, 3 skeptical)
- **New recommendations added** (Phase 3): 3 (2 pragmatist, 1 skeptical; two of the three independently propose a startup sweep and converge on the same recommendation with a frequency dispute)
- **Disputes remaining** (Phase 4): 3
- **Convergence points** (Phase 4): 6

---

### Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|------------------|---------------------|---------------|-------------|--------------|
| 1 | pragmatist | Directory creation, mode 0o700, before first write | P1 | Surviving | None | Unanimous | Accepted |
| 2 | pragmatist | Credential files written via `os.open(O_TRUNC, 0o600)`; no post-rename chmod | P1 | Modified (drop "chmod after rename" alt; adopt O_TRUNC) | skeptical (O_EXCL vs. O_TRUNC) | Bilateral | Accepted-Modified |
| 3 | pragmatist | Migration failure behavior: catch + warn + fallback + `unlink(.tmp, missing_ok=True)` in `finally` | P1 | Modified (cleanup must be inside lock `finally` block) | skeptical (concurrent-save race unaddressed) | Bilateral | Accepted-Modified |
| 4 | pragmatist | Q2: Lazy migration per-provider on first read | P1 | Modified (require file lock + startup sweep) | skeptical (Q2: eager is safer) | Bilateral | Accepted-Modified |
| 5 | pragmatist | Q3: Permanent fallback with per-use INFO log line | P2 | Modified (add per-use log line to original permanent-fallback position) | skeptical (Q3: time-bounded) | Bilateral | Accepted-Modified |
| 6 | pragmatist | Atomic rename uses same-directory `.tmp`; `os.replace` mandated | P2 | Modified (`os.rename` → `os.replace`) | skeptical (Windows correctness) | Unanimous | Accepted-Modified |
| 7 | pragmatist | No transaction log; `.tmp` + `os.replace` is sufficient | P2 | Surviving | None | Unanimous | Accepted |
| 8 | pragmatist | Sanitize provider names against `[a-zA-Z0-9_-]+` | P3 | Surviving | None | None | Accepted |
| 9 | skeptical | Use `os.replace` not `os.rename` everywhere | P1 | Surviving | None | Unanimous | Accepted |
| 10 | skeptical | `.tmp` created via `os.open(O_WRONLY\|O_CREAT\|O_TRUNC, 0o600)` | P1 | Modified (O_EXCL → O_TRUNC) | pragmatist (orphan .tmp should overwrite, not error) | Bilateral | Accepted-Modified |
| 11 | skeptical | Per-provider file lock (`fcntl.flock` POSIX / `msvcrt.locking` Windows) | P1 | Modified (add non-blocking 200ms timeout; skip+fallback if contended) | pragmatist (must not block CLI) | Bilateral | Accepted-Modified |
| 12 | skeptical | `credentials/` directory created with mode 0o700 | P2 | Surviving | None | Unanimous | Accepted |
| 13 | skeptical | `PermissionError` from `_read_all()`: warn at WARNING + fallback; not hard propagate | P2 | Modified (hard propagate → warn-and-degrade-with-WARNING) | pragmatist (propagation too harsh for CLI) | Bilateral | Accepted-Modified |
| 14 | skeptical | Q1: Preserve `auth.json`, never delete | P2 | Surviving | None | Unanimous | Accepted |
| 15 | skeptical | Q2: Lazy migration (revised from original eager position) | P2 | Modified (eager → lazy; yield to pragmatist) | pragmatist (lazy: smaller per-op blast radius) | Bilateral | Accepted-Modified |
| 16 | skeptical | Q3: Permanent fallback (revised from original time-bounded position) | P2 | Modified (time-bounded → permanent; yield to pragmatist) | pragmatist (time-bounded breaks dormant users) | Bilateral | Accepted-Modified |
| 17 | skeptical | Post-write verification via read-back after `os.replace` | P3 | Modified (downgraded to P3 optional; permanent fallback makes it non-critical) | pragmatist (over-engineering for local POSIX FS) | Bilateral | Accepted-Modified |
| 18 | pragmatist | NEW: Per-provider file lock with non-blocking 200ms timeout; `finally` cleanup | P1 | New | — | Unanimous (converges with #11) | Accepted |
| 19 | pragmatist | NEW: Startup sweep — log unmigrated providers once per invocation (stateless, INFO) | P2 | New | skeptical (frequency/deduplication) | Convergent, frequency disputed | Disputed |
| 20 | skeptical | NEW: Startup sweep — log unmigrated providers, deduplicated across invocations | P2 | New | pragmatist (stateless preferred; no sentinel file) | Convergent, frequency disputed | Disputed |

**Notes on convergent duplicates**: Recommendations 1 and 12 independently propose the same `credentials/` directory creation with mode 0o700; both survive. Recommendations 6 and 9 both address `os.replace`; both arrive at the same implementation. Recommendations 11 and 18 both specify the per-provider file lock; 18 is a Phase 3 addition by pragmatist acknowledging a gap from Phase 1. Recommendations 19 and 20 describe the same startup sweep with a disputed frequency parameter.

---

### Dangerous Contradictions Found

**Resolved Contradictions**

1. **Q2: Eager vs. Lazy Migration** (identified in pragmatist/cross-reviews/skeptical-reviewer.md, Dangerous Contradictions; skeptical/cross-reviews/pragmatist-reviewer.md, Dangerous Contradictions). Pragmatist originally proposed lazy (Phase 1, Rec 4); skeptical originally proposed eager (Phase 1, Rec 7). The cross-reviews revealed that the concurrent-save race actually exists under either strategy, neutralizing the skeptical argument that eager confines the race to startup. Skeptical conceded in Phase 3 revision (Rec 7, "I yield on Q2") after accepting that a per-provider lock resolves the race regardless of migration timing, and that lazy migration provides better per-provider failure isolation. **Resolution: lazy migration adopted.**

2. **Q3: Time-Bounded vs. Permanent Fallback** (identified in pragmatist/cross-reviews/skeptical-reviewer.md, Dangerous Contradictions; skeptical/cross-reviews/pragmatist-reviewer.md, Dangerous Contradictions). Pragmatist proposed permanent (Phase 1, Rec 5); skeptical proposed time-bounded (Phase 1, Rec 8). The cross-reviews revealed that Q2 and Q3 are coupled: lazy migration + time-bounded fallback silently breaks providers that are never accessed before the fallback window expires. Skeptical's own Phase 3 revision ("I yield on the time-bounded expiry") acknowledges this coupling explicitly. **Resolution: permanent fallback adopted.**

3. **`os.rename` vs. `os.replace`** (identified in skeptical/cross-reviews/pragmatist-reviewer.md, Dangerous Contradictions; pragmatist/cross-reviews/skeptical-reviewer.md, Dangerous Contradictions). Pragmatist's Phase 1 Alignment section endorsed `os.rename` as correct for POSIX atomicity. Skeptical identified in Phase 1 (Rec 1) that `os.rename` raises `FileExistsError` on Windows when the destination already exists. Pragmatist's cross-review of skeptical stated explicitly: "Pragmatist should yield entirely here. `os.replace` is the correct primitive… this is a one-word change with no trade-off." Pragmatist incorporated `os.replace` in Phase 3 (modified Rec 6). **Resolution: `os.replace` mandated universally.**

4. **Concurrency Lock: P1 Critical vs. Not Mentioned** (identified in pragmatist/cross-reviews/skeptical-reviewer.md, Dangerous Contradictions). Skeptical had the concurrent-save race analysis and file lock (Phase 1, Rec 3); pragmatist had no mention of concurrency in Phase 1. Pragmatist acknowledged the gap in Phase 3 (New Rec 1) and added the non-blocking 200ms requirement. Skeptical accepted the non-blocking timeout as correct in Phase 3 revision (modified Rec 3). **Resolution: per-provider non-blocking lock with 200ms timeout, `finally`-block cleanup.**

5. **`O_EXCL` vs. `O_TRUNC` for `.tmp` creation** (identified in pragmatist/cross-reviews/skeptical-reviewer.md, Tensions; skeptical/cross-reviews/pragmatist-reviewer.md, Tensions). Skeptical proposed `O_EXCL` (Phase 1, Rec 2); pragmatist proposed `O_TRUNC`. Pragmatist's cross-review correctly noted that an orphaned `.tmp` from a prior crash is stale data that should be unconditionally overwritten — `O_EXCL` would require explicit orphan detection and retry on every invocation. Skeptical conceded in Phase 3 revision (modified Rec 2): "I specified `O_EXCL` as a defense against orphaned temp files, but an orphaned `.tmp` contains stale pre-migration data and should be unconditionally overwritten." **Resolution: `O_TRUNC` over `O_EXCL`.**

6. **`PermissionError` handling: hard propagate vs. warn-and-degrade** (identified in pragmatist/cross-reviews/skeptical-reviewer.md, Tensions; skeptical/cross-reviews/pragmatist-reviewer.md, Tensions). Skeptical originally proposed re-raising `PermissionError` from `_read_all()` (Phase 1, Rec 5). Pragmatist's cross-review proposed a middle path: log at WARNING level with the file path, then fall back to legacy for this session. Skeptical modified Rec 5 in Phase 3 to adopt the warn-and-fallback model, retaining the requirement that the per-provider file not be marked as migrated so the warning recurs. **Resolution: catch `PermissionError`, emit WARNING with file path and actionable message, return `{}` (allowing fallback), do not mark as migrated.**

---

**Unresolved Contradictions**

1. **`conversus status` Credential-Source Display — Scope** (pragmatist/disputes.md, Remaining Disputes; skeptical/disputes.md, Remaining Disputes). Pragmatist argues the change is out of SC-004 scope: it is a presentation-layer modification to a command's output contract, whereas the startup sweep is purely additive logging. Skeptical argues that if the startup sweep is in scope (both agents agree it is), then the status display is equally in scope — both address the same observability gap by different mechanisms. Skeptical also argues that without user-facing migration state in `conversus status`, the split-state under lazy + permanent fallback is invisible to users who rely on the status command rather than log output.

   **Synthesizer assessment**: Pragmatist's position is better supported by the evidence. The distinction between log-level observability (startup sweep: no command contract changes) and command-output changes (`conversus status`: user-visible schema modification) is real and substantive. QUESTION.md explicitly states SC-004's contract is bounded and warns against proposing new SCs. A change to `conversus status` output format is a new user-visible contract that introduces test-surface expansion and potential regression risk in a PR whose primary purpose is storage format migration. Skeptical's internal-consistency argument — "if sweep is in scope, status display is in scope" — conflates two materially different types of additions. The startup sweep runs at process startup with no command flag; `conversus status` output is a named, tested, user-documented command interface. The pragmatist's proposed compromise (TODO comment in `conversus status` code, explicit follow-on spec reference in PR description) preserves the observability intent without expanding SC-004's contract.

   **Recommended resolution**: Defer `conversus status` per-provider credential-source display to a follow-on spec. Add a single inline `# TODO(SC-005): display credential source per-provider in status output` comment at the relevant point in `conversus status` logic. The PR description must name the follow-on spec explicitly. The startup sweep covers migration observability for SC-004.

2. **Fallback Log Line Frequency — Every-Time vs. First-Time** (skeptical/disputes.md, Remaining Disputes; pragmatist/disputes.md Convergence section notes this as a flexibility area). Pragmatist proposes the log line fires every time the fallback is used (stateless, no tracking). Skeptical proposes it fires the first time per-provider (requires a one-bit state marker per-provider). Pragmatist argues statelessness is correct because "first-time" cannot be defined across machine restores. Skeptical argues that every-time firing trains users to ignore the message.

   **Synthesizer assessment**: Neither position is clearly dominant on correctness, but they are separable on implementation cost. Pragmatist's machine-restore argument does not fully hold: after a restore, `credentials/` is empty and `credentials/{provider}.json` does not exist, so the first post-restore invocation triggers a fresh first-time event regardless. However, the marker-file approach introduces persistent state that must survive upgrades and correctly invalidate if `auth.json` changes. Pragmatist's log-noise concern is real but addressable without state. The correct resolution is not a choice between the two proposals: emit the log at DEBUG level (not INFO or WARNING). DEBUG log lines appear only under verbose/debug mode, making them available for diagnosis without flooding normal operation. This preserves pragmatist's stateless requirement and addresses skeptical's noise concern without any marker file.

   **Recommended resolution**: Emit the fallback log line at DEBUG level, stateless, on every fallback trigger. This ensures visibility during migration debugging while not polluting normal CLI output. The single per-use line at DEBUG is: `"credentials/{provider}.json not found; reading from legacy auth.json. Run 'conversus migrate-credentials' to migrate."` No marker file is required.

3. **Startup Sweep Frequency — Every Invocation vs. Deduplicated** (pragmatist/disputes.md, Remaining Disputes; skeptical/disputes.md, Remaining Disputes). Pragmatist proposes the sweep fires once per invocation unconditionally (stateless, INFO level). Skeptical proposes deduplication across invocations to prevent log spam, via either a sentinel file or log-level suppression (DEBUG unless verbose).

   **Synthesizer assessment**: Skeptical's noise concern is well-founded: a developer running conversus dozens of times daily with a Gemini provider they never access will see the sweep message indefinitely, potentially hundreds of times per year until migration completes. Pragmatist correctly notes that a sentinel file introduces state that can go stale if `auth.json` changes. The resolution is the same as Dispute 2: emit the startup sweep at DEBUG level rather than INFO. DEBUG-level output is invisible in normal CLI operation, visible during debugging, and requires no sentinel file. This satisfies pragmatist (stateless) and satisfies skeptical (not visible in normal operation). If the user wants to inspect migration state, `--verbose` or `--debug` flags surface the sweep.

   **Recommended resolution**: Emit the startup sweep at DEBUG level, stateless, once per invocation. The sweep lists unmigrated providers detected at startup: `"Unmigrated credential providers found in auth.json: [gemini, ...]. These will migrate lazily on first use."` No sentinel file required. Resolves the log-noise concern without persistent state.

---

### Systemic Contradictions

- **Observability vs. Scope Discipline**
  - **Manifests in**: Dispute 1 (conversus status scope); Dispute 3 (startup sweep frequency); the per-use fallback log line frequency (Dispute 2); pragmatist's Phase 3 New Rec 2 and skeptical's Phase 3 New Rec; skeptical's "Lazy migration + permanent fallback = invisible orphan providers" missed opportunity (Phase 1 review).
  - **Root cause**: QUESTION.md is bounded to storage format migration but does not address the observability problem that lazy migration + permanent fallback creates. When users cannot tell which providers have migrated, and migrated state is invisible without log inspection, every agent independently proposed a new observability mechanism (log lines, status display, startup sweep) that then collided with the spec's scope constraint. The spec created the observability gap by not specifying any user-visible signal for migration completion.
  - **Implication for spec**: Future migration specs should include an explicit "user-visible migration state" acceptance criterion. Either the spec mandates a migration status surface (in which case it is in scope) or it explicitly excludes it and references a named follow-on spec. Leaving observability unspecified forces deliberation agents to independently propose additions that then collide with the scope constraint.

- **Security Properties Absent from Original Proposal**
  - **Manifests in**: Both Phase 1 reviews independently identifying missing directory permissions (0o700) and file permissions (0o600); skeptical's "chmod race" missed opportunity; pragmatist's "file permissions not mentioned" missed opportunity; provider name sanitization (pragmatist Rec 8).
  - **Root cause**: QUESTION.md's conservative strategy was written from a correctness-and-safety lens (crash safety via atomic rename, data preservation) without a security lens (permissions, information disclosure, path traversal). OAuth tokens are sensitive credentials; the spec did not treat them as such. The proposals in Q1–Q4 address data integrity but not data confidentiality.
  - **Implication for spec**: Credential migration specs must include an explicit security checklist: file permission requirements, directory permission requirements, and path validation for provider names used as filesystem components. The absence of this checklist caused both Phase 1 reviews to independently catch three overlapping security gaps that the spec author missed entirely.

- **Q2 and Q3 Presented as Independent When They Are Coupled**
  - **Manifests in**: The most significant Phase 3 concession (skeptical yielding on both Q2 and Q3); skeptical's Phase 3 revision explicit acknowledgment ("once I yield on Q2, Q3 followed structurally"); the dangerous contradiction flag in pragmatist's cross-review of skeptical for Q3 (pragmatist/cross-reviews/skeptical-reviewer.md, Dangerous Contradictions: "Q3 Fallback Duration: Time-Bounded vs. Permanent").
  - **Root cause**: QUESTION.md presents Q2 (eager vs. lazy) and Q3 (permanent vs. time-bounded fallback) as independent binary choices with four possible combinations. But lazy + time-bounded is degenerate: providers that are never accessed are never migrated under lazy, so the time-bounded fallback will silently break them when it expires. The spec's framing concealed this coupling, causing both agents to initially choose positions on Q2 and Q3 independently without recognizing the incompatibility.
  - **Implication for spec**: Decision trees in migration specs should explicitly identify coupled decisions and their valid combinations. When a migration trigger (Q2) determines whether migration will ever occur for a given provider, the fallback window (Q3) must be conditioned on that trigger. Presenting them as orthogonal encourages agents and implementers to compose incompatible positions.

- **Windows/Cross-Platform Correctness Absent from Spec**
  - **Manifests in**: The `os.rename` vs. `os.replace` resolved contradiction; pragmatist's Phase 1 endorsement of `os.rename` as correct without mentioning Windows; QUESTION.md's POSIX-centric framing throughout (tilde-expansion home directory paths, `os.rename` as "atomic primitive").
  - **Root cause**: The spec assumes a POSIX-only deployment context. It uses `os.rename` as the named atomic primitive, uses `~/.conversus/` notation (POSIX tilde expansion), and does not mention platform compatibility requirements. `os.rename` is a correctness bug on Windows that fails silently on every second credential save — a failure mode affecting all Windows users that a POSIX-focused review would not catch.
  - **Implication for spec**: CLI tool migration specs must specify cross-platform primitives explicitly, not POSIX-native ones. `os.replace` should be the specified primitive in any future spec that touches file-rename operations. The spec should state the target platforms (POSIX, Windows, or both) and use primitives that are correct on all stated targets.

- **Atomic Rename Addressed Single-Process Crash Safety But Not Multi-Process Concurrent Access**
  - **Manifests in**: Q4 asking about transaction logs (wrong question); the concurrent-save race identified by skeptical (Phase 1, Rec 3 missed opportunity); pragmatist's Phase 1 missing concurrency analysis entirely; the emergence of the file lock as a Phase 3 new recommendation from pragmatist; skeptical's Phase 3 modification to add non-blocking timeout.
  - **Root cause**: QUESTION.md's Q4 framed the failure-mode question as "partial migration under crash" and proposed atomic rename as the answer. This addressed single-process crash safety correctly but did not address multi-process concurrent access. For a CLI tool that may run as background token-refresh processes alongside foreground invocations, migration and concurrent saves can race. The spec's Q4 framing led both reviews to initially evaluate transaction log necessity, with the concurrent-write scenario discovered through the Phase 2 cross-review process — not from Q4's explicit question.
  - **Implication for spec**: Q4 should be split into two questions: (a) single-process crash safety (addressed by atomic rename), and (b) multi-process concurrent access safety (addressed by per-provider file lock with non-blocking semantics). A spec that conflates these under "atomic safety" will miss the locking requirement.

---

### Convergence Achieved

- **`os.replace` replaces `os.rename` everywhere** — Strength: Unanimous
  - **Agreed recommendation**: All `.tmp` → final file moves must use `os.replace(tmp, final)`, not `os.rename`. This is the correct cross-platform primitive: atomic replacement on POSIX, no `FileExistsError` on Windows when the destination already exists.
  - **Supporting agents**: Pragmatist (Phase 3 modified Rec 6: "Replace all `os.rename(tmp, final)` calls with `os.replace(tmp, final)`"); skeptical (Phase 3 surviving Rec 1; Phase 4 disputes.md Convergence: "present in both Phase 1 reviews from different angles").
  - **Evidence basis**: `os.rename` raises `FileExistsError` on Windows when the destination exists, meaning every second credential save for any provider fails silently on Windows. `os.replace` is a superset of `os.rename` behavior on POSIX and uses atomic replacement semantics on Windows (Python 3.3+). Pragmatist's cross-review of skeptical acknowledged: "this is a one-word change with no trade-off."
  - **Pre-existing or earned**: Skeptical had it from Phase 1. Pragmatist's cross-review acknowledged it and incorporated it in Phase 3. Earned through cross-review.

- **`credentials/` directory creation with mode 0o700** — Strength: Unanimous
  - **Agreed recommendation**: Any function that writes a credential file must call `os.makedirs(credentials_dir, mode=0o700, exist_ok=True)` before the first write. Without this, clean installs crash with `FileNotFoundError`; without mode 0o700, the directory is world-listable on shared hosts.
  - **Supporting agents**: Pragmatist (Phase 3 surviving Rec 1: "P1 non-negotiable"); skeptical (Phase 3 surviving Rec 4: "single strongest finding from the deliberation"); both Phase 4 dispute documents list this under Convergence.
  - **Evidence basis**: Clean installs have no `credentials/` directory; the first write crashes unconditionally without `makedirs`. Mode 0o700 prevents enumeration of which OAuth providers a user has credentials for. Both reviewers reached this independently — pragmatist from crash-path analysis, skeptical from information-disclosure analysis — using the same proposed mode. The QUESTION.md proposal does not mention directory creation anywhere.
  - **Pre-existing or earned**: Both reviews identified this independently in Phase 1 from different analytical starting points. The strongest Phase 1 finding in the deliberation.

- **Per-provider file lock, non-blocking, 200ms timeout** — Strength: Unanimous
  - **Agreed recommendation**: The read-from-auth.json → write-to-credentials/{provider}.json migration path must be wrapped in a per-provider advisory file lock (`fcntl.flock(LOCK_EX|LOCK_NB)` on POSIX, `msvcrt.locking` on Windows). If the lock cannot be acquired within 200ms, skip migration for this invocation, fall back to `auth.json[provider]`, and log a warning. The `unlink(missing_ok=True)` cleanup of any partial `.tmp` must execute in the lock's `finally` block.
  - **Supporting agents**: Skeptical (Phase 3 modified Rec 3; Phase 4 disputes.md Convergence: "per-provider file lock, non-blocking, 200ms timeout"); pragmatist (Phase 3 New Rec 1; Phase 4 disputes.md Convergence: "both revisions now describe the same lock").
  - **Evidence basis**: The concurrent-save race — process A migrating stale pre-refresh token overwrites process B's freshly saved token via `os.replace` — is not an I/O exception and is not caught by exception handling. This produces silent token corruption under concurrent access with no error surfaced. A blocking lock is unacceptable for CLI UX; the 200ms non-blocking timeout preserves responsiveness.
  - **Pre-existing or earned**: Skeptical identified the race in Phase 1. Pragmatist acknowledged the gap in Phase 3 and added the non-blocking requirement. Skeptical accepted the timeout in Phase 3. Cooperative resolution — neither agent had the complete picture in Phase 1.

- **Q1: Preserve `auth.json`, never delete** — Strength: Unanimous
  - **Agreed recommendation**: `auth.json` is never deleted or renamed by conversus after migration. The file is left in place. Users who want it removed must do so manually.
  - **Supporting agents**: Pragmatist (Phase 1 Alignment; Phase 4 disputes.md Convergence: "agreed in Phase 1, SC-001 precedent"); skeptical (Phase 3 surviving Rec 6; Phase 4 disputes.md Convergence: "both note SC-001 precedent").
  - **Evidence basis**: Pragmatist: risk asymmetry — deletion bug impact dwarfs stale-file confusion impact. Skeptical: SC-001 precedent established that conversus does not silently delete user config files. Both independently invoked the SC-001 `settings.json` preservation pattern.
  - **Pre-existing or earned**: Agreed from Phase 1. The one Q1–Q4 decision point that required no deliberation.

- **Q2 + Q3: Lazy migration per-provider + permanent fallback** — Strength: Unanimous (after Phase 3 concessions)
  - **Agreed recommendation**: Migration is per-provider on first credential read (lazy). `CredentialStore.get(provider)` permanently falls back to `auth.json[provider]` if `credentials/{provider}.json` does not exist. There is no expiry on the fallback.
  - **Supporting agents**: Pragmatist (Phase 3 modified Recs 4, 5); skeptical (Phase 3 modified Recs 7, 8: explicit concessions on both Q2 and Q3).
  - **Evidence basis**: Lazy migration provides per-provider failure isolation — if Gemini migration fails, Anthropic credentials are unaffected. The file lock resolves the concurrent-save race regardless of migration timing, eliminating skeptical's primary argument for eager. Time-bounded fallback + lazy migration is degenerate (providers never accessed are never migrated and break silently after the window expires); skeptical's Phase 3 revision acknowledges this coupling explicitly.
  - **Pre-existing or earned**: Both agents changed position. Skeptical conceded both Q2 and Q3 in Phase 3. The most significant deliberation-driven outcome.

- **Startup sweep: read-only, logs unmigrated providers per invocation** — Strength: Unanimous on existence and read-only constraint; frequency disputed
  - **Agreed recommendation**: On conversus startup, diff `auth.json` provider keys against files present in `credentials/`. For any provider key in `auth.json` with no corresponding `credentials/{provider}.json`, emit a log line listing unmigrated providers. The sweep is read-only — it never writes, never migrates, never deletes.
  - **Supporting agents**: Pragmatist (Phase 3 New Rec 2); skeptical (Phase 3 New Rec); both Phase 4 dispute documents list this under Convergence.
  - **Evidence basis**: Under lazy migration + permanent fallback, providers that are never accessed produce no migration log lines and have no observable migration state. The startup sweep closes this observability gap without requiring `conversus status` schema changes. Both agents independently proposed substantively identical sweep logic in Phase 3.
  - **Pre-existing or earned**: Emerged cooperatively from the Q2/Q3 resolution in Phase 3. Neither agent had this in Phase 1.

---

### Remaining Disputes

<!-- CONVERSUS:DISPUTES_BEGIN -->

- **Dispute: `conversus status` Credential-Source Display — SC-004 Scope**
  - **Positions**: Pragmatist (Phase 4 disputes.md, Remaining Disputes): defer to follow-on spec; the startup sweep covers the observability gap; a `conversus status` output format change is a new user-visible contract. Skeptical (Phase 4 disputes.md, Remaining Disputes): must land in SC-004; under permanent fallback, users cannot inspect migration state through `conversus status` without it; the pragmatist includes the startup sweep as in-scope while excluding the status display, which addresses the same gap at a different layer.
  - **Arguments**: Pragmatist: a `conversus status` output change modifies a named, user-documented command interface and introduces test-surface expansion. QUESTION.md is explicit that SC-004's contract is bounded. The startup sweep provides log-level observability without a command schema change. Proposed compromise: TODO comment in code plus explicit follow-on spec reference in the PR. Skeptical: if the startup sweep (which is also an addition beyond QUESTION.md's proposal) is acceptable, the status display is equally acceptable. Log-level observability requires users to inspect logs; `conversus status` is the user-facing surface for operational state. A user who runs `conversus status` to verify their setup cannot see whether Gemini is reading from the legacy file.
  - **Synthesizer assessment**: Pragmatist's position is better supported. The distinction between log-line additions and command output schema changes is substantive: the startup sweep adds no new CLI interface, no new output format, and no new command behavior; a `conversus status` change modifies an existing command's output that users, scripts, and downstream tooling may parse. QUESTION.md's explicit scope discipline ("SC-004's contract is bounded") applies more forcefully to command-output changes than to internal logging. Skeptical's internal-consistency argument conflates two materially different additions. The pragmatist's resolution path (TODO comment + follow-on spec reference) satisfies skeptical's operational-transparency requirement without expanding SC-004's surface.
  - **Recommended resolution**: Defer `conversus status` per-provider credential-source display to a follow-on spec. Add `# TODO(SC-005): display credential source per-provider in conversus status output` at the relevant point in `conversus status` logic. The PR description must reference this follow-on work explicitly. The startup sweep is the in-scope observability mechanism for SC-004.

- **Dispute: Fallback Log Line Frequency — Every-Time Stateless vs. First-Time Per-Provider**
  - **Positions**: Pragmatist (Phase 4 disputes.md, Convergence flexibility section): log line fires every time the fallback is used, stateless, no tracking of whether it has fired before. Skeptical (Phase 4 disputes.md, Remaining Disputes): log line fires the first time per-provider, requiring a one-bit marker per-provider; repeated firing trains users to ignore it.
  - **Arguments**: Pragmatist: "first-time" requires persistent state across machine restores, OS reinstalls, and backup restores, all of which reset `credentials/` to empty. Every fallback event is a meaningful event; stateless emission handles new-machine scenarios correctly. Skeptical: a WARNING that fires every invocation indefinitely for a permanent fallback is noise, not signal. The log line must be actionable the first time; repeating it is alarm fatigue. Machine-restore cases still count as "first time" because the credential file doesn't exist yet.
  - **Synthesizer assessment**: Neither position is strictly superior. Pragmatist's machine-restore argument is partially answered by skeptical (on restore, `credentials/` is empty, so any first-time marker is also absent — the "first time" fires correctly). However, pragmatist's stateless implementation argument is valid: a per-provider "already-logged" marker adds state that must survive upgrades and correctly invalidate if the migration state changes. The cleanest resolution is neither proposal: emit the fallback log at DEBUG level rather than INFO or WARNING. DEBUG lines appear only under verbose/debug mode, are invisible in normal CLI operation, and require no persistent state. This preserves the stateless property while eliminating the noise concern.
  - **Recommended resolution**: Emit the fallback log line at DEBUG level, stateless, on every fallback trigger. Line: `"credentials/{provider}.json not found; reading from legacy auth.json. Run 'conversus migrate-credentials' to migrate."` No marker file. Visible under `--debug`/`--verbose` flags, not in normal operation.

- **Dispute: Startup Sweep Frequency — Every Invocation vs. Deduplicated Across Invocations**
  - **Positions**: Pragmatist (Phase 4 disputes.md, Remaining Disputes): sweep fires once per invocation unconditionally (stateless, INFO level); deduplication via marker file adds state complexity and fails to re-notify when `auth.json` gains new providers. Skeptical (Phase 4 disputes.md, Remaining Disputes): sweep output should be deduplicated across invocations to avoid log spam; a developer using conversus daily will see the message hundreds of times per year for providers they never access.
  - **Arguments**: Pragmatist: stateless sweep handles newly added orphaned providers without invalidating a marker; the sweep is an actionable INFO-level signal, not spam; in-memory per-process deduplication (a `set()`) is an acceptable concession without persistent state. Skeptical: daily sweeps for months or years train users to ignore the output, which defeats the purpose; deduplication via sentinel file or log-level suppression is preferable; sweep output at DEBUG (visible only in verbose mode) is the minimum acceptable alternative.
  - **Synthesizer assessment**: Skeptical's noise concern is well-founded for a CLI with daily usage. Pragmatist's sentinel-file concern is also valid: a persistent marker can go stale if the user manually edits `auth.json`. The resolution that satisfies both constraints without new persistent state: emit the startup sweep at DEBUG level by default, not INFO. At DEBUG, the sweep is invisible in normal operation and surfaces only during debugging — exactly the context where migration state visibility matters. This preserves pragmatist's stateless property, addresses skeptical's noise concern, requires no sentinel file, and correctly re-notifies on any new unmigratable provider without stale-marker issues.
  - **Recommended resolution**: Emit the startup sweep at DEBUG level, stateless, once per invocation. Line: `"Unmigrated credential providers found in auth.json: [{provider_list}]. These will migrate lazily on first use."` No sentinel file. Visible under `--debug`/`--verbose` flags.

<!-- CONVERSUS:DISPUTES_END -->

---

### Actionable Spec Changes

**P1 — Must implement** (blocking issues or unanimous convergence):

1. **Directory creation before first write**: Before any write to `credentials/{provider}.json`, call `os.makedirs(Path.home() / ".conversus" / "credentials", mode=0o700, exist_ok=True)`. This must precede the `.tmp` write in every code path that writes a credential file. Source: pragmatist Rec 1 (surviving); skeptical Rec 12 (surviving); Phase 4 Convergence (unanimous, both dispute documents).

2. **`os.replace` replaces `os.rename`**: Replace every occurrence of `os.rename(tmp, final)` in the migration and credential write paths with `os.replace(tmp, final)`. The `.tmp` file must always be written to `credentials/{provider}.json.tmp` (same directory as the final destination) to preserve POSIX atomicity. Source: pragmatist modified Rec 6; skeptical surviving Rec 1 (Rec 9 in scorecard); Phase 4 Convergence (unanimous).

3. **`.tmp` file created with mode 0o600 at creation time**: Create `.tmp` files using `os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)`, write content to the returned file descriptor, close, then `os.replace`. Do not use `open()` followed by `os.chmod` — this leaves a world-readable window between creation and permission set. The `O_TRUNC` flag (not `O_EXCL`) ensures orphaned `.tmp` files from prior crashes are unconditionally overwritten. Source: pragmatist modified Rec 2; skeptical modified Rec 10 (Rec 2 in scorecard); Phase 4 Convergence (O_TRUNC over O_EXCL, bilateral).

4. **Per-provider non-blocking file lock around migration write path**: Wrap the read-from-auth.json → write-to-`credentials/{provider}.json` migration path in a per-provider advisory file lock. Use `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` on POSIX, `msvcrt.locking` on Windows. Lock file: `credentials/{provider}.lock` (same filesystem as the credential file). If the lock cannot be acquired within 200ms, skip migration for this invocation, fall back to `auth.json[provider]` for this session, and log a WARNING: `"Migration lock unavailable for {provider}; will retry on next invocation."` The `.tmp` cleanup (`unlink(missing_ok=True)`) must execute in the lock's `finally` block. Source: pragmatist New Rec 1 (Rec 18 in scorecard); skeptical modified Rec 11 (Rec 3 in scorecard); Phase 4 Convergence (unanimous).

5. **Q2: Lazy migration per-provider on first read**: Migration is triggered per-provider when `CredentialStore.get(provider)` is called and `credentials/{provider}.json` does not exist. It is not triggered at startup for all providers. Source: pragmatist modified Rec 4; skeptical modified Rec 15 (Rec 7 in scorecard, conceded from eager); Phase 4 Convergence (Q2+Q3 combined, unanimous after Phase 3 concessions).

6. **Q3: Permanent fallback in `CredentialStore.get(provider)`**: If `credentials/{provider}.json` does not exist, fall back permanently to `auth.json[provider]`. There is no expiry on the fallback. This fallback is a read-only operation; it never modifies `auth.json`. Source: pragmatist modified Rec 5; skeptical modified Rec 16 (Rec 8 in scorecard, conceded from time-bounded); Phase 4 Convergence (unanimous).

7. **Q1: Preserve `auth.json` after migration**: `auth.json` is never deleted, renamed, or modified by conversus after SC-004 lands. Users who want it removed delete it manually. Source: pragmatist Phase 1 Alignment; skeptical surviving Rec 14 (Rec 6 in scorecard); Phase 4 Convergence (unanimous, agreed from Phase 1).

8. **Migration failure behavior: catch + warn + fallback + `.tmp` cleanup**: On any exception during migration (I/O error, disk full, etc.), the handler must: (a) catch the exception, (b) emit a single-line WARNING: `"Failed to migrate credentials for {provider}: {error}. Will read from legacy auth.json this session."`, (c) fall back to reading `auth.json[provider]` directly, and (d) call `tmp_path.unlink(missing_ok=True)` in the `finally` block inside the file lock scope. Do not propagate the exception. Source: pragmatist modified Rec 3.

9. **Q4: No transaction log**: The `.tmp` + `os.replace` atomic-rename pattern is sufficient. No transaction log required. The idempotent fallback handles partial state correctly: if a crash leaves no `credentials/{provider}.json`, the next invocation falls back to `auth.json[provider]` and retries migration. Source: pragmatist surviving Rec 7; Phase 4 Convergence (unanimous, undisputed throughout all phases).

---

**P2 — Should implement** (majority convergence or strong single-agent case):

1. **`PermissionError` handling in `_read_all()`**: Modify `_read_all()` at `auth.py:88` to distinguish `PermissionError` from `FileNotFoundError` and `json.JSONDecodeError`. Catch `FileNotFoundError` and `json.JSONDecodeError` silently (return `{}`). Catch `PermissionError` separately: emit a WARNING with the file path and actionable message (`"credentials/{provider}.json exists but is not readable (permission denied); check file permissions."`), return `{}` to allow fallback, and do not mark the provider as migrated so the warning recurs on the next invocation. Source: skeptical modified Rec 13 (Rec 5 in scorecard); pragmatist cross-review middle-path (pragmatist/cross-reviews/skeptical-reviewer.md, Tensions: "PermissionError Re-Raising vs. Graceful Degradation").

2. **Startup sweep for unmigrated providers**: On conversus startup, read `auth.json` (if it exists) and compare its provider keys against the files in `credentials/`. For any provider key in `auth.json` with no corresponding `credentials/{provider}.json`, emit a log line listing all unmigrated providers. The sweep is read-only — no writes, no migration, no deletions. Log level: DEBUG (see Dispute 3 resolution). Log line: `"Unmigrated credential providers found in auth.json: [{provider_list}]. These will migrate lazily on first use."` Source: pragmatist New Rec 2 (Rec 19 in scorecard); skeptical New Rec (Rec 20 in scorecard); Phase 4 Convergence (unanimous on existence and read-only constraint; frequency resolved by synthesizer to DEBUG level).

3. **Fallback log line at DEBUG level on each trigger**: When `CredentialStore.get(provider)` falls back to `auth.json[provider]` because `credentials/{provider}.json` does not exist, emit a DEBUG-level log: `"credentials/{provider}.json not found; reading from legacy auth.json. Run 'conversus migrate-credentials' to migrate."` Stateless, fires on every fallback trigger. Source: pragmatist modified Rec 5 (log line addition); skeptical modified Rec 16; frequency dispute resolved by synthesizer to DEBUG level.

4. **Startup sweep TODO for `conversus status`**: Add `# TODO(SC-005): display credential source per-provider in conversus status output` at the point in `conversus status` logic where provider credential state is reported. The PR description must reference the follow-on spec explicitly. Source: Dispute 1 synthesizer resolution; pragmatist Phase 4 dispute Proposed Resolution.

---

**P3 — Consider implementing** (bilateral agreement or strong but disputed):

1. **Provider name sanitization**: Validate that provider names match `[a-zA-Z0-9_-]+` before using them as filename components in `credentials/{provider}.json`. Raise `ValueError` on invalid names. This closes path traversal permanently. Source: pragmatist surviving Rec 8. Note: provider names are internal constants in the current codebase, making exploitation low-probability; this is a zero-cost hardening measure.

2. **Post-write verification via read-back**: After `os.replace(tmp, final)`, call `_read_all(final_path)` and verify the provider key exists in the result. If the read-back fails or the key is absent, log a WARNING, fall back to `auth.json[provider]` for this session, and do not mark migration as complete. Targets NFS/SMB environments where `rename(2)` may not be atomic across server crash. Source: skeptical modified Rec 17 (Rec 9 in scorecard, downgraded to P3 in Phase 3). Note: with permanent fallback in place (P1 change #6), a failed verification falls back gracefully and the risk is low; this is optional defense-in-depth for NFS environments.

---

### Key Concessions

**pragmatist-reviewer**:

- **`os.rename` → `os.replace` (Phase 3, modified Rec 6)**: Pragmatist's Phase 1 Alignment section endorsed `os.rename` as "correct for POSIX filesystems" without addressing Windows. Skeptical's Phase 1 Rec 1 and cross-review identified that `os.rename` raises `FileExistsError` on Windows when the destination already exists. Pragmatist's cross-review of skeptical acknowledged: "Pragmatist should yield entirely here. `os.replace` is the correct primitive; it subsumes `os.rename` on POSIX and fixes Windows. This is a one-word change with no trade-off." This was a factual correction, not a design trade-off, and pragmatist acknowledged it cleanly.

- **Drop "chmod after rename" alternative in `.tmp` write (Phase 3, modified Rec 2)**: Pragmatist's Phase 1 Rec 2 specified `os.open(tmp_path, O_WRONLY|O_CREAT|O_TRUNC, 0o600)` but then offered "or by calling `os.chmod` immediately after the rename" as an alternative. Skeptical's cross-review correctly identified that the chmod-after-rename alternative leaves a world-readable window on the `.tmp` file from creation through the rename. Pragmatist's Phase 3 revision dropped the alternative: "the 'optionally os.chmod immediately after the rename' alternative in my original recommendation is wrong and must be dropped."

- **Acknowledging the concurrent-save race gap (Phase 3, New Rec 1)**: Pragmatist's Phase 1 review had no mention of the concurrent-save race where process A migrating stale credentials overwrites process B's freshly saved token. Skeptical's cross-review identified this as a load-bearing gap. Pragmatist's Phase 3 revision added the per-provider file lock as New Rec 1 and explicitly acknowledged: "I was wrong to frame blast-radius as the sole argument for lazy without addressing how lazy interacts with concurrent writes."

---

**skeptical-reviewer**:

- **`O_EXCL` → `O_TRUNC` (Phase 3, modified Rec 2)**: Skeptical's Phase 1 Rec 2 specified `O_EXCL` for `.tmp` file creation as defense against orphaned temp files from prior crashes. Pragmatist's cross-review correctly identified that an orphaned `.tmp` contains stale pre-migration data and should be unconditionally overwritten — `O_EXCL` would require explicit orphan detection and retry. Skeptical's Phase 3 revision acknowledged: "I specified `O_EXCL` as a defense against orphaned temp files, but an orphaned `.tmp` contains stale pre-migration data and should be unconditionally overwritten."

- **Q2: Eager → Lazy migration (Phase 3, modified Rec 7)**: Skeptical's Phase 1 position was eager migration (all providers at startup). The cross-review process surfaced that (a) the per-provider file lock resolves the concurrent-save race under either strategy, eliminating the concurrency argument for eager, and (b) eager migration has an all-or-nothing failure surface at startup before any user command executes. Skeptical's Phase 3 revision stated: "I yield on Q2. The correct position is: lazy migration, per-provider on first read, with a startup sweep that logs which providers in auth.json have not yet been migrated." This was the most significant concession in the deliberation.

- **Q3: Time-bounded → Permanent fallback (Phase 3, modified Rec 8)**: Skeptical's Phase 1 position was time-bounded fallback with deprecation warnings after 3 releases and removal in the 4th. Pragmatist's cross-review identified that if the fallback is genuinely time-bounded but `conversus migrate-credentials` is not shipped in the same PR, there is a release window where the fallback expires before users have a migration escape hatch. More critically, skeptical's own Phase 3 revision acknowledged that Q2 and Q3 are coupled: "once I yield on Q2, Q3 followed structurally." Lazy + time-bounded is degenerate for providers that are never accessed. Skeptical's Phase 3 revision adopted permanent fallback with a per-provider log line and `conversus status` display as compensating observability.

- **Added non-blocking 200ms timeout to file lock (Phase 3, modified Rec 3)**: Skeptical's Phase 1 Rec 3 proposed `fcntl.flock` without specifying behavior when the lock is contended. Pragmatist's cross-review identified that a CLI must not hang indefinitely on file contention and proposed: "the lock must be advisory and non-blocking with a short timeout (e.g., 200ms)." Skeptical's Phase 3 revision incorporated the 200ms non-blocking timeout explicitly: "If the lock cannot be acquired within 200ms, skip migration for this invocation."

- **Post-write verification downgraded to P3 optional (Phase 3, modified Rec 9)**: Skeptical's Phase 1 Rec 9 required post-write verification via read-back after every `os.replace` as protection against NFS partial writes. Pragmatist's cross-review resolved the tension by noting that permanent fallback (once Q3 was settled) provides the same protection: "If permanent fallback is adopted, a silent NFS partial-write is handled by the fallback — the user stays authenticated." Skeptical's Phase 3 revision downgraded the recommendation: "I retain this as a P3 hardening item… permanent fallback is the primary safety net, and verification is an optional secondary layer."