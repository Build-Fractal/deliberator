### Remaining Disputes

- **Dispute: `conversus status` Credential-Source Display — Scope**
  - **My claim**: The `conversus status` per-provider credential-source display (e.g., "anthropic: credentials/anthropic.json" vs "anthropic: auth.json [legacy]") belongs in a follow-on spec, not SC-004. SC-004's contract is bounded to storage migration; `conversus status` is a presentation layer change. (Pragmatist revision, modified Rec 5: "The `conversus status` credential-source display change skeptical proposes is deferred to a follow-on spec; it is not required to close SC-004.")
  - **Opposing position(s)**: Skeptical's modified Rec 8 requires `conversus status` to report per-provider credential source as part of permanent-fallback adoption: "conversus status should report credential source per-provider… The `conversus migrate-credentials` command is deferred to a follow-on spec as a user-triggered convenience; it does not gate SC-004." Skeptical treats the status display as in-scope for SC-004.
  - **Why I will not concede**: QUESTION.md explicitly states "SC-004's contract is bounded" and warns against "propos[ing] adding new SCs." A `conversus status` schema change is a new user-visible behavior, not a consequence of storage migration. Introducing it in SC-004 creates a scope creep vector: now SC-004 must also update status display logic, output formatting, and any tests that assert on `conversus status` output. The startup sweep already addresses the observability gap that motivates this change; the status display is additive, not required.
  - **Counter-argument to their position**: Skeptical's rationale is that permanent fallback without status transparency produces invisible split-state. This is correct as a concern, but the startup sweep (which both revisions now include as New Rec / P2) provides that observability. The startup sweep logs unmigrated providers once per invocation without requiring changes to a separate command's output contract. Skeptical cannot both yield on Q2 (lazy migration) and require status display changes: under lazy migration, status would show different sources for different providers across different sessions, which is information-theoretically noisy until migration is complete. The startup sweep is the right layer.
  - **Proposed resolution path**: Scope `conversus status` changes out of SC-004 explicitly. Add a TODO comment in `conversus status` output code noting the planned credential-source display. Ship the startup sweep as the observability mechanism for SC-004. This preserves skeptical's operational-transparency concern without expanding SC-004's surface.

---

- **Dispute: Startup Sweep Deduplication — Stateless vs. Marker-Based**
  - **My claim**: The startup sweep fires once per invocation, stateless: every conversus startup checks `auth.json` against `credentials/` and emits an INFO-level log line for any unmigrated providers. No marker file, no state. (Pragmatist revision, New Rec 2: "fires once per invocation, not once per provider access.")
  - **Opposing position(s)**: Skeptical's New Rec specifies "its output is deduplicated (no repeated log spam across invocations by storing a 'sweep-reported' marker or using a log level that won't surface unless verbose mode is active)." Skeptical wants across-invocation deduplication via a persistent marker or log-level suppression.
  - **Why I will not concede**: A "sweep-reported" marker file introduces state that must be managed: where does it live, what invalidates it, does it survive conversus upgrades, does it survive `auth.json` edits? For a CLI tool running in a developer's terminal, the startup sweep log line is not spam — it is an actionable prompt. A user who adds a new provider to `auth.json` between invocations needs the sweep to fire again. A stateless sweep handles this automatically; a marker-based sweep would silently suppress the warning for the new provider. The marker approach trades operational clarity for log volume, and for a CLI tool the log volume is negligible (one INFO line per startup until migration completes).
  - **Counter-argument to their position**: Skeptical's deduplication concern is grounded in "log spam across invocations," but a user who never migrates a dormant provider is precisely the user who needs to see the reminder. Suppressing it via a marker defeats the purpose of the sweep. The log-level alternative (suppress unless verbose) has the same problem: the user most likely to have orphaned providers is the least likely to run conversus in verbose mode. The sweep is an INFO-level signal, not an ERROR — any logging framework will naturally suppress it in production or quiet mode without requiring explicit deduplication logic.
  - **Proposed resolution path**: Stateless sweep as specified in my revision, with one concession: emit the log line at INFO level (not WARN), so it is filtered out by default in non-verbose conversus operation. This addresses skeptical's log-volume concern without introducing a marker file. If skeptical insists on deduplication, scope it to "within a single session" (per-process deduplicate, not cross-invocation), which adds a simple `set()` in memory without persistent state.

---

### Convergence

- **Converged: `os.replace()` replaces `os.rename()`**
  - **Shared position**: All `os.rename(tmp, final)` calls must be replaced with `os.replace(tmp, final)`. This fixes silent `FileExistsError` on Windows when the destination credential file already exists.
  - **Agreeing agents**: Pragmatist revision (modified Rec 6: "replace all `os.rename(tmp, final)` calls with `os.replace(tmp, final)`"), Skeptical revision (surviving Rec 1: "Replace all `os.rename` calls with `os.replace(tmp, final)`").
  - **Strength**: Unanimous.
  - **Path to convergence**: Pragmatist acknowledged this in the cross-review ("Pragmatist should yield entirely here"). Skeptical had it from Phase 1. No residual dispute.

- **Converged: `O_TRUNC` over `O_EXCL` in `os.open` for `.tmp` files**
  - **Shared position**: Create `.tmp` via `os.open(tmp_path, os.O_WRONLY|os.O_CREAT|os.O_TRUNC, 0o600)`. An orphaned `.tmp` from a prior crash contains stale pre-migration data and should be unconditionally overwritten, not treated as an error. `O_EXCL` would require explicit orphan detection and retry on every migration attempt.
  - **Agreeing agents**: Pragmatist revision (modified Rec 2: "`O_TRUNC` flag is correct over `O_EXCL` because orphaned `.tmp` files from prior crashes should be overwritten"), Skeptical revision (modified Rec 2: "I specified `O_EXCL` as a defense against orphaned temp files, but an orphaned `.tmp` contains stale pre-migration data and should be unconditionally overwritten").
  - **Strength**: Unanimous.
  - **Path to convergence**: Skeptical's original position used `O_EXCL`; pragmatist's cross-review identified this as an error; skeptical conceded in revision. Clean Phase 3 resolution.

- **Converged: Per-provider non-blocking file lock around migration write path**
  - **Shared position**: Wrap the read-from-auth.json → write-to-credentials/{provider}.json migration path in a per-provider advisory file lock (`fcntl.flock` on POSIX, `msvcrt.locking` on Windows). The lock must be non-blocking with a ~200ms timeout. If the lock cannot be acquired, skip migration for this invocation, fall back to `auth.json[provider]`, and log a single-line warning. The `.tmp` cleanup must occur in the lock's `finally` block.
  - **Agreeing agents**: Pragmatist revision (New Rec 1: "non-blocking with a short timeout (~200ms)… if the lock cannot be acquired, skip migration for this invocation"), Skeptical revision (modified Rec 3: "acquire `fcntl.flock(LOCK_EX|LOCK_NB)` with a 200ms retry budget. If the lock cannot be acquired within 200ms, skip migration for this invocation").
  - **Strength**: Unanimous.
  - **Path to convergence**: Neither review had this in Phase 1. Skeptical identified the concurrent-save race; pragmatist identified the non-blocking requirement in the cross-review. Both conceded toward each other in revision.

- **Converged: Directory creation with mode 0o700**
  - **Shared position**: Call `os.makedirs(credentials_dir, mode=0o700, exist_ok=True)` before any credential file write. Without this, clean installs crash with `FileNotFoundError`. Mode 0o700 prevents directory enumeration on shared hosts.
  - **Agreeing agents**: Pragmatist revision (surviving Rec 1: "P1 non-negotiable"), Skeptical revision (surviving Rec 4: "single strongest finding from the deliberation").
  - **Strength**: Unanimous.
  - **Path to convergence**: Both reviews reached this independently in Phase 1 from different analytical directions (crash path vs. information-disclosure). QUESTION.md does not mention directory creation at all, making it a mandatory addition. Highest-confidence finding of the entire deliberation.

- **Converged: Q1 preserve, Q2 lazy migration, Q3 permanent fallback, Q4 no transaction log**
  - **Shared position**: (1) Preserve `auth.json` — never delete; user removes manually. (2) Lazy migration per-provider on first read, plus a startup sweep for observability. (3) Permanent fallback: `CredentialStore.get(provider)` always falls back to `auth.json[provider]` if the per-provider file is absent, with a per-use INFO/WARNING log line. (4) `.tmp` + `os.replace` is sufficient; no transaction log required.
  - **Agreeing agents**: Pragmatist revision (modified Recs 4, 5, 7; surviving Rec 7 on transaction log), Skeptical revision (surviving Rec 6; modified Recs 7, 8; Rec 9 downgraded to P3 optional).
  - **Strength**: Unanimous across all four sub-questions.
  - **Path to convergence**: Q1 was agreed from Phase 1. Q2 and Q3 required cross-review concessions: skeptical yielded from eager to lazy; skeptical yielded from time-bounded to permanent. Pragmatist's main revision acknowledged that Q2 and Q3 are coupled — once skeptical yielded on Q2, Q3 followed structurally. Q4 was never in dispute.

---

### Final Position Statement

**Non-Negotiables**

1. **Directory creation with mode 0o700 before any credential write.**
   This is the one finding that fails every clean install unconditionally. QUESTION.md's proposed strategy does not mention it. Both reviews arrived at it independently with the same proposed mode. It requires two lines of code and has zero trade-off with any other decision in this deliberation. Without it, SC-004 is not shippable.

2. **Per-provider file lock with non-blocking 200ms timeout, `finally`-block `.tmp` cleanup.**
   The concurrent-save race — process A migrating a stale pre-refresh token overwriting process B's freshly saved token — is not an I/O exception and is not caught by any other mechanism in the proposal. This race is silent (no error, no log line, no retry) and produces "my credentials stopped working after the upgrade" reports with no obvious cause. The lock is the only defense. The non-blocking timeout is required because a CLI must not hang on file contention.

3. **`os.replace` not `os.rename`.**
   One word. Prevents `FileExistsError` on Windows for every credential save after the first. No trade-off, no design decision involved, factual correctness.

---

**Flexibility**

1. **Startup sweep behavior: stateless per-invocation vs. deduplicated across invocations.**
   I prefer stateless (every startup) because it handles newly added orphan providers without invalidating a marker. I am flexible on the deduplication mechanism if the synthesizer determines log volume is a real concern: in-memory per-process deduplication (a `set()` cleared on each startup, not persisted) preserves the stateless property while suppressing duplicate lines within a single session. I will not accept a persistent marker file.

2. **`conversus status` credential-source display.**
   I consider this out of SC-004 scope, but I am flexible on timing if skeptical's concern about permanent-fallback observability is not adequately addressed by the startup sweep. Acceptable compromise: ship the startup sweep in SC-004; add a `# TODO(SC-005): display credential source per-provider` comment in the `conversus status` code path, making the follow-on spec discoverable without expanding SC-004's surface. The core intent I require preserved: SC-004 does not change `conversus status` output format.

3. **Per-use INFO log line on fallback fires — frequency.**
   I specified this fires every time the fallback is used (stateless). Skeptical's revision says "not mark as migrated" to ensure warning recurrence. Both formulations produce the same observable behavior. I am flexible on the implementation mechanism (stateless vs. migration-state-tracking) as long as the outcome is identical: the user sees a log line every time a legacy credential is served, not just the first time.