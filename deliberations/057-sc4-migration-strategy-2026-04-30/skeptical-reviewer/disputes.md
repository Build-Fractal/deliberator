### Remaining Disputes

- **Dispute: `conversus status` Credential Source Display — SC-004 Scope vs. Deferral**
  - **My claim**: `conversus status` must report credential source per-provider ("anthropic: credentials/anthropic.json" vs "anthropic: auth.json [legacy]") as part of SC-004, not a follow-on spec. (Skeptical revision, modified Rec 8: "conversus status should report credential source per-provider.")
  - **Opposing position(s)**: Pragmatist Rec 5 (modified) explicitly defers this: "The `conversus status` credential-source display change skeptical proposes is deferred to a follow-on spec; it is not required to close SC-004."
  - **Why I will not concede**: The QUESTION.md acceptance bar requires either zero ACCEPT findings on the conservative strategy or a clear directional verdict. The conservative strategy as written has no user-visible signal of migration state. Under lazy migration + permanent fallback — the converged Q2/Q3 position — a user with three providers who only ever uses one will never see the other two migrate. The startup sweep covers that gap at the log level, but `conversus status` is the user-facing surface that health-conscious users actually check. Without it, migration state is only observable through log inspection, which is not the same thing. The pragmatist's observability argument for the startup sweep (pragmatist new Rec 2) proves the concern is real; the conclusion that `conversus status` can be deferred while a startup sweep is required is internally inconsistent — both address the same visibility gap, but the sweep is in scope while the status command is not.
  - **Counter-argument to their position**: The pragmatist says the `conversus status` change is out of scope for SC-004 because it is not required to close the spec. This is a scope argument, not a correctness argument. The cost of adding one line to `conversus status` output is lower than the cost of adding a startup sweep, which the pragmatist treats as in-scope. If the startup sweep is in scope, the status display is in scope. The pragmatist cannot use "SC-004's contract is bounded" to exclude status display while including startup sweep — both are additions beyond the QUESTION.md proposal, and both serve the same observability goal.
  - **Proposed resolution path**: Conditional adoption — if the synthesizer determines the startup sweep is sufficient observability for SC-004, the status display can be deferred with an explicit follow-on spec reference in the PR description. If the synthesizer agrees that user-facing observability (not just log-level observability) is required to close SC-004, the status display must land in this PR. The synthesizer must choose between these two framings.

---

- **Dispute: Fallback Log Line Frequency — First-Time vs. Every-Time**
  - **My claim**: Emit the fallback log line the first time `auth.json` is used as a fallback for a given provider — not on every invocation. (Skeptical revision, modified Rec 8: "emit a single per-provider log line the first time `auth.json` is used as a fallback.")
  - **Opposing position(s)**: Pragmatist Rec 5 (modified) explicitly inverts this: "This log line is stateless (no tracking of whether it has fired before) and fires every time the fallback is used, not just once — which is the right behavior for permanent fallback, since the user may have moved machines or restored from backup."
  - **Why I will not concede**: The pragmatist's machine-restore rationale is correct in the abstract but inapplicable in practice. After a machine restore, the user starts fresh — `credentials/` is empty, `auth.json` is restored from backup, and lazy migration has not run yet. On first post-restore invocation, the fallback fires because `credentials/{provider}.json` does not yet exist. That is the correct first-time event, and the first-time log line fires as designed. There is no scenario where a user restores from backup and the credential file exists while the fallback-already-logged marker does not. The pragmatist's rationale for every-time firing does not survive examination against the actual restore scenario.
  - **Counter-argument to their position**: "Stateless" is not a design virtue when it produces log noise. A CLI tool that emits the same WARNING-level line on every invocation indefinitely trains users to ignore it, which is worse than no warning at all. First-time logging produces one actionable signal; every-time logging produces an alarm that users habituate to and stop reading. The pragmatist acknowledges the log line exists to inform users, but a message that fires on every invocation for the lifetime of a permanent fallback is not informative — it is background noise. The first-time framing requires a one-bit state marker (a `.migrated` sentinel file or checking whether the credential file exists post-migration), which is negligible implementation cost compared to the benefit of a log line users will actually read.
  - **Proposed resolution path**: Compromise — emit the log line every time the fallback fires, but at DEBUG level rather than INFO/WARNING. Reserve INFO for the startup sweep (which fires once per invocation and lists all unmigrated providers). This preserves the pragmatist's stateless property while preventing operational log spam. If the synthesizer determines a severity choice is required, INFO/WARNING first-time firing is my preferred position; stateless every-time at DEBUG is the minimum acceptable alternative.

---

- **Dispute: Startup Sweep Frequency — Every Invocation vs. Deduplicated**
  - **My claim**: The startup sweep's output should be deduplicated across invocations — no repeated log spam — by using a log level that won't surface unless verbose mode is active or by storing a lightweight marker. (Skeptical revision, new Rec: "Its output is deduplicated (no repeated log spam across invocations…)")
  - **Opposing position(s)**: Pragmatist new Rec 2 states the sweep "fires once per invocation, not once per provider access" — the contrast being with per-access logging, not with cross-invocation repetition. The pragmatist's formulation implies the sweep repeats every invocation without deduplication.
  - **Why I will not concede**: For a developer CLI used dozens of times daily, a startup sweep that logs unmigrated providers on every invocation will become the most-seen log line in the codebase within 24 hours of the migration landing. Users who never access Gemini credentials will see "Unmigrated credential providers: [gemini]" every time they run conversus, indefinitely. This is the operational definition of log spam. The purpose of the sweep is to make migration state visible; once the user has seen it, the goal is achieved. Repeating it does not advance the goal — it degrades log quality for all other messages.
  - **Counter-argument to their position**: The pragmatist's "once per invocation, not once per provider access" framing addresses a different concern — preventing the sweep from re-logging for each operation within a single invocation. That is correct and uncontested. But it does not address cross-invocation repetition. A startup sweep that fires once per invocation is still firing on every conversus run the user makes. The deduplication concern is at the session boundary (invocation-to-invocation), not within-invocation (one startup log per run). These are different axes and the pragmatist's formulation does not resolve the one I am disputing.
  - **Proposed resolution path**: Log the startup sweep at DEBUG level by default; surface it at INFO only on the first invocation where unmigrated providers are detected. Alternatively, cap sweep logging to once per calendar day using a timestamp file in `~/.conversus/` (low-cost, no sensitive content). Either approach addresses the noise concern without eliminating the observability.

---

### Convergence

- **Converged: `os.replace` replaces `os.rename` everywhere**
  - **Shared position**: All `os.rename(tmp, final)` calls in the migration path must be replaced with `os.replace(tmp, final)`. This is the correct primitive: atomic replacement on POSIX, no `FileExistsError` on Windows.
  - **Agreeing agents**: Skeptical (revision Rec 1, surviving); Pragmatist (revision Rec 6, modified to include `os.replace`).
  - **Strength**: Unanimous.
  - **Path to convergence**: Present in both Phase 1 reviews from different angles. Skeptical identified Windows correctness; Pragmatist acknowledged it in cross-review and incorporated it into the final recommendation. No concession required from either party — both arrived at `os.replace` independently.

---

- **Converged: `credentials/` directory creation with mode 0o700**
  - **Shared position**: `os.makedirs(credentials_dir, mode=0o700, exist_ok=True)` must be called before any credential file write. Without it, clean installs crash with `FileNotFoundError`. The 0o700 mode prevents directory enumeration on shared hosts.
  - **Agreeing agents**: Pragmatist (revision Rec 1, surviving); Skeptical (revision Rec 4, surviving).
  - **Strength**: Unanimous.
  - **Path to convergence**: Both Phase 1 reviews identified this independently — Pragmatist from the clean-install crash path, Skeptical from the information-disclosure path. Convergence from different analytical starting points with identical proposed mode (0o700) is the strongest signal in the deliberation.

---

- **Converged: Per-provider file lock, non-blocking, 200ms timeout**
  - **Shared position**: The read-migrate-write path must be protected by a per-provider advisory file lock (`fcntl.flock(LOCK_EX|LOCK_NB)` on POSIX, `msvcrt.locking` on Windows). If the lock cannot be acquired within 200ms, skip migration for this invocation, fall back to `auth.json[provider]`, log a warning. Lock cleanup in `finally` block.
  - **Agreeing agents**: Skeptical (revision Rec 3, modified to add 200ms non-blocking timeout); Pragmatist (new Rec 1, specifying the same mechanism and timeout).
  - **Strength**: Unanimous.
  - **Path to convergence**: Skeptical Phase 1 identified the concurrent-save race. Pragmatist cross-review accepted the lock as necessary but added the non-blocking caveat. Skeptical incorporated the non-blocking requirement in Phase 3. Both revisions now describe the same lock: per-provider, non-blocking, 200ms, `finally` cleanup. This is a cooperative resolution — neither party had the complete picture in Phase 1.

---

- **Converged: Q1 — Preserve auth.json, never delete**
  - **Shared position**: `auth.json` is never deleted or renamed by conversus after migration. Users who want the legacy file gone must remove it manually.
  - **Agreeing agents**: Skeptical (revision Rec 6, surviving); Pragmatist (original Recommendation 3's exception-handling implies preservation; explicitly confirmed in cross-review Safe Agreements).
  - **Strength**: Unanimous.
  - **Path to convergence**: Agreed in Phase 1. The SC-001 precedent (preserved orphan `settings.json`) was identified independently by both reviewers. No revision required from either party on this point.

---

- **Converged: Q2 + Q3 — Lazy migration with permanent fallback**
  - **Shared position**: Migration is per-provider on first credential read (lazy). `CredentialStore.get(provider)` permanently falls back to `auth.json[provider]` if `credentials/{provider}.json` does not exist.
  - **Agreeing agents**: Skeptical (revision Rec 7, modified from eager; revision Rec 8, modified from time-bounded); Pragmatist (revision Rec 4, surviving lazy; revision Rec 5, surviving permanent fallback).
  - **Strength**: Unanimous.
  - **Path to convergence**: The most significant shift in the deliberation. Skeptical yielded on both Q2 and Q3 in Phase 3, recognizing that the coupling between the two positions made time-bounded fallback untenable once eager migration was abandoned. The pragmatist's cross-review correctly identified this coupling as a dangerous contradiction; Skeptical's Phase 3 revision acknowledged it explicitly.

---

- **Converged: Startup sweep — read-only, logs unmigrated providers once per invocation**
  - **Shared position**: On conversus startup, diff `auth.json` provider keys against `credentials/` files and log any providers present in `auth.json` without a corresponding per-provider file. The sweep is read-only — no writes, no migration.
  - **Agreeing agents**: Skeptical (revision new Rec, "startup sweep logging unmigrated providers"); Pragmatist (revision new Rec 2, "startup sweep for unmigrated providers").
  - **Strength**: Unanimous on the existence and read-only constraint. (Frequency remains disputed above.)
  - **Path to convergence**: Emerged cooperatively from the Q2/Q3 resolution — once both parties adopted lazy migration, the observability gap for never-accessed providers required a startup-time compensating mechanism. Both parties proposed substantively identical implementations in their Phase 3 revisions.

---

### Final Position Statement

**Non-Negotiables**

1. `os.replace` + `credentials/` directory with mode 0o700 must both land in SC-004.
   These are foundational correctness issues, not hardening. `os.replace` prevents silent corruption for every Windows user on every credential save after the first. The directory creation prevents a `FileNotFoundError` crash on every clean install. Both reviewers identified these independently. The QUESTION.md proposal omits both. A PR that ships without either is broken on at least one platform or use case on day one.

2. The per-provider file lock must be non-blocking with a hard 200ms timeout ceiling.
   The concurrent-save race is not a theoretical concern for a CLI that may be invoked by background refresh daemons alongside foreground processes. A blocking lock turns that scenario into an indefinite hang. Both revisions agree on the mechanism; I am stating non-negotiability specifically on the non-blocking requirement, not the lock itself. A blocking lock is strictly worse than no lock for a CLI tool.

**Flexibility**

1. `conversus status` credential source display.
   I maintain it should land in SC-004, but will accept deferral to a follow-on spec if: (a) the follow-on spec is explicitly referenced in the PR description with a concrete issue number, and (b) the startup sweep is confirmed as in-scope for SC-004 with at minimum INFO-level output. If both conditions are met, the status display deferral does not leave users without visibility into migration state. What must be preserved: some user-visible surface (not just logs) showing whether a given provider is reading from the legacy file or the new file, in the same PR or a named follow-on.

2. Fallback log frequency and startup sweep frequency.
   My preferred position is first-time/deduplicated for the fallback line and capped (daily or by sentinel) for the sweep. What must be preserved: the log lines must not be suppressible by default and must produce at least one actionable user-visible signal per provider per machine lifetime. If every-invocation logging is adopted for both, the log level must be DEBUG-or-equivalent so users who do not run in verbose mode are not flooded. The signal cannot be pure noise.