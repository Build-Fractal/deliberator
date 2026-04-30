I'll read the required files in order before producing the arbitration resolution.

Now reading the Phase 5 synthesis and Phase 4 dispute documents.

I now have all required documents. My response will be the arbitration resolution written verbatim to the output file — no tools needed.

---

### Process Note

This arbitration was triggered by the `always` condition — subject arbitration activates unconditionally for cooperative deliberations. Three disputes remain unresolved from the Phase 5 synthesis after 2 agents (pragmatist-reviewer, skeptical-reviewer) completed 4 phases across 8 total artifacts. This is a **cooperative** deliberation with subject arbitration. The subject (conversus system) holds binding decision authority per the influence level `binding` established for this run.

---

### Decision Framework

Relevant principles from CONSTITUTION.md v2.5.0 bearing on the three remaining disputes:

- **Principle I — Spec-Driven Development** (§ "I. Spec-Driven Development"): "Every behavioral change MUST start with a specification." QUESTION.md bounds SC-004's contract; additions beyond that boundary require a new spec.

- **Principle II — Stable Interfaces** (§ "II. Stable Interfaces"): "Breaking changes MUST be coordinated across all consumers." The `conversus status` subcommand name and its output are part of the dispatch-table / user-documented surface; changes to its output format must be coordinated.

- **Principle III — Backward-Compatible Extension** (§ "III. Backward-Compatible Extension"): "New features MUST extend existing behavior rather than restructuring it." A startup log sweep is additive; a `conversus status` output format change restructures an existing command's contract.

- **Principle V — Observable Deliberation** (§ "V. Observable Deliberation"): "Agents MUST NOT silently swallow errors." Migration observability must be preserved — this principle demands *some* signal exists, not that it must be at INFO level or in every output surface.

- **Principle IX — Functional Programming and Clean Code** (§ "IX. Functional Programming"): "No mutable global state. Configuration is loaded once and passed explicitly." Per-provider "already-logged" markers are mutable persistent state that must survive upgrades and `auth.json` edits; stateless log emission is the correct implementation pattern.

- **Principle X — Zen of Python Output** (§ "X. Zen of Python Output"): "Output MUST be clean, readable, and unsurprising." A log line that fires on every invocation indefinitely under a permanent fallback is neither clean nor unsurprising in normal operation.

---

### Binding Decisions

#### Dispute: `conversus status` Credential-Source Display — SC-004 Scope

**Positions:**
- **Pragmatist** (Phase 4 disputes.md, Remaining Disputes): Defer to follow-on spec; the startup sweep covers the observability gap; a `conversus status` output format change is a new user-visible contract outside SC-004's bounded scope. Proposed compromise: TODO comment in code + explicit follow-on spec reference in PR description.
- **Skeptical** (Phase 4 disputes.md, Remaining Disputes): Must land in SC-004; under permanent fallback, users cannot inspect migration state through `conversus status` without it; if the startup sweep (also an addition beyond QUESTION.md) is in scope, the status display is equally in scope.

**Synthesizer's assessment:** Pragmatist's position is better supported. The distinction between log-line additions and command output schema changes is substantive: the startup sweep adds no new CLI interface; `conversus status` output is a named command interface that users, scripts, and downstream tooling may parse. QUESTION.md's scope discipline applies more forcefully to command-output changes. The pragmatist's resolution path (TODO comment + follow-on spec reference) satisfies skeptical's operational-transparency concern without expanding SC-004's surface.

**Ruling:** Defer `conversus status` per-provider credential-source display to a follow-on spec. SC-004 ships with a startup sweep as the sole in-scope observability mechanism.

**Grounding citation:** Principle II (Stable Interfaces): "`conversus status` output is a user-documented command interface" — changing it constitutes a coordinated breaking change requiring a spec of its own. Principle III (Backward-Compatible Extension): The startup sweep is additive; a `conversus status` output format change restructures an existing command's observable contract. Principle I (Spec-Driven Development): QUESTION.md explicitly states "SC-004's contract is bounded" — new user-visible behavior must begin with a new spec, not be attached to a storage migration PR.

**Rationale:** Skeptical's internal-consistency argument — "if startup sweep is in scope, status display is equally in scope" — conflates two categorically different types of additions. A startup sweep is an internal diagnostic log that runs unconditionally and introduces no command interface. A `conversus status` output change creates a new output field that users, documentation, and downstream scripts may depend upon and that requires its own test coverage, output contract specification, and regression checking. These differ in contract weight and rollback cost. Skeptical's Phase 4 flexibility clause ("will accept deferral if startup sweep is confirmed as in-scope with at minimum INFO-level output") creates the acceptance path: the startup sweep lands in SC-004 (at DEBUG level per Dispute 3's ruling), and the follow-on spec is explicitly named in the PR description.

**Rejected position:** Skeptical's in-scope argument. Its strongest case is that log-level observability requires users to know to pass `--verbose`, while `conversus status` is the natural health-check surface. This is a valid UX concern but proves too much: any observability gap could justify scope expansion of any PR under that argument. The correct response is a named, bounded follow-on spec, not scope expansion. The Constitution provides this answer in Principles I, II, and III jointly.

**Required changes:**
1. In the `conversus status` handler (the code path that renders provider credential state): add `# TODO(SC-005): display credential source per-provider in conversus status output` at the point where per-provider credential state would be reported. File: whichever source module implements `conversus status` output rendering.
2. In the SC-004 PR description: include an explicit follow-on spec reference — "SC-005: `conversus status` credential-source display" — naming the bounded follow-on work.

---

#### Dispute: Fallback Log Line Frequency — Every-Time Stateless vs. First-Time Per-Provider

**Positions:**
- **Pragmatist** (Phase 4 disputes.md, Convergence flexibility section): Log fires every time the fallback is used, stateless, no tracking of whether it has fired before. Statelessness handles machine-restore scenarios correctly.
- **Skeptical** (Phase 4 disputes.md, Remaining Disputes): Log fires the first time per-provider, requiring a one-bit marker per-provider. Repeated firing trains users to ignore it — alarm fatigue defeats the signal's purpose.

**Synthesizer's assessment:** Neither position is strictly superior. The cleanest resolution is a third path: emit the fallback log at DEBUG level, stateless, on every fallback trigger. This preserves the stateless property while eliminating the noise concern. No marker file required.

**Ruling:** Emit the fallback log line at DEBUG level, stateless, on every fallback trigger. No marker file.

**Grounding citation:** Principle IX (Functional Programming): "No mutable global state" — a per-provider "already-logged" marker is mutable persistent state that must survive OS reinstalls, conversus upgrades, and `auth.json` edits. Stateless emission is constitutionally correct. Principle X (Zen of Python Output): "Output MUST be clean, readable, and unsurprising" — an INFO or WARNING line firing on every invocation indefinitely under a permanent fallback is neither clean nor unsurprising.

**Rationale:** Pragmatist's stateless property is directly required by Principle IX; this is not a style preference but a constitutional constraint. Skeptical's noise concern is directly addressed by Principle X. The synthesizer's DEBUG-level resolution satisfies both principles simultaneously without the marker-file state: DEBUG output is filtered in normal CLI operation and surfaces only under `--debug`/`--verbose`, precisely the diagnostic context where per-fallback migration tracing is useful. On machine restore, `credentials/` is empty and the first post-restore fallback fires correctly regardless — which means skeptical's marker adds no correctness value even under skeptical's own restore scenario.

**Rejected position:** Skeptical's first-time-per-provider marker. Its strongest argument is that once the user has seen the message, repeating it is alarm fatigue — one actionable signal is better than noise. This is answered by changing the log level rather than adding persistent state. The user who needs to act on the fallback signal can enable `--debug`; the user who has seen it and acted does not see it again in normal operation. Adding a marker file to implement "first-time" introduces mutable state that violates Principle IX without buying more than a log-level change provides.

**Required changes:**
- In `CredentialStore.get(provider)` fallback path: emit at `logging.DEBUG` level (not `logging.WARNING` or `logging.INFO`). Log line: `"credentials/{provider}.json not found; reading from legacy auth.json. Run 'conversus migrate-credentials' to migrate."` No marker file created. No migration-state tracking variable. File: the module implementing `CredentialStore.get()`.

---

#### Dispute: Startup Sweep Frequency — Every Invocation vs. Deduplicated Across Invocations

**Positions:**
- **Pragmatist** (Phase 4 disputes.md, Remaining Disputes): Sweep fires once per invocation unconditionally, stateless, INFO level. Deduplication via marker file fails when `auth.json` gains new providers between invocations.
- **Skeptical** (Phase 4 disputes.md, Remaining Disputes): Sweep output should be deduplicated across invocations; a developer using conversus daily will see the message hundreds of times per year for providers they never access, training them to ignore it.

**Synthesizer's assessment:** Skeptical's noise concern is well-founded for a CLI with daily usage. Pragmatist's sentinel-file concern is valid. The resolution satisfying both without new persistent state: emit the startup sweep at DEBUG level, not INFO. Stateless, once per invocation. No sentinel file.

**Ruling:** Emit the startup sweep at DEBUG level, stateless, once per invocation. No sentinel file.

**Grounding citation:** Principle IX (Functional Programming): "No mutable global state" — a sentinel file or timestamp tracking when the sweep last fired is mutable persistent state; stateless emission is constitutionally required. Principle X (Zen of Python Output): "Output MUST be clean, readable, and unsurprising" — an INFO-level message appearing on every conversus invocation indefinitely for a provider the user never accesses violates this principle structurally, not just aesthetically.

**Rationale:** The pragmatist's stateless-sweep property is constitutionally grounded (Principle IX) and must be preserved. Skeptical's log-noise concern is constitutionally grounded (Principle X) and must also be addressed. These are not competing values under the Constitution — both are required. A log level change resolves the tension without trading one constitutional requirement against the other. At DEBUG level, the sweep is invisible in normal operation (satisfying Principle X) and surfaces under `--debug`/`--verbose` (satisfying Principle V's observability requirement). The pragmatist's in-memory `set()` concession is unnecessary at DEBUG level since the output is already filtered; pure stateless emission is both simpler and correct.

**Rejected position:** Pragmatist's INFO-level stateless sweep. Its strongest argument is that INFO is "actionable, not spam" — a signal that should prompt user action should be visible in normal operation. This argument holds for a signal that fires rarely; under lazy migration + permanent fallback, a developer who never accesses a dormant provider will see the sweep on every conversus invocation indefinitely. An actionable signal that repeats indefinitely becomes habituation noise (Principle X). The stateless property is preserved by the ruling; only the log level changes.

**Required changes:**
- In the conversus startup sweep function (the logic that diffs `auth.json` keys against `credentials/` files): emit at `logging.DEBUG` level (not `logging.INFO`). Log line: `"Unmigrated credential providers found in auth.json: [{provider_list}]. These will migrate lazily on first use."` No sentinel file. No cross-invocation deduplication mechanism. Sweep fires once per process invocation, stateless. File: the module implementing conversus startup initialization.

---

### Summary of Changes Required

**P1 — Required for correctness:**

1. **Fallback log line at DEBUG level** (from Dispute: Fallback Log Line Frequency): In the `CredentialStore.get(provider)` fallback path, emit at `logging.DEBUG` (not INFO or WARNING). Log line: `"credentials/{provider}.json not found; reading from legacy auth.json. Run 'conversus migrate-credentials' to migrate."` No marker file. Stateless.

2. **Startup sweep at DEBUG level** (from Dispute: Startup Sweep Frequency): In the conversus startup sweep logic, emit at `logging.DEBUG` (not INFO). Log line: `"Unmigrated credential providers found in auth.json: [{provider_list}]. These will migrate lazily on first use."` Stateless, once per invocation, no sentinel file.

**P2 — Required for design integrity:**

3. **TODO comment in `conversus status` handler** (from Dispute: `conversus status` Credential-Source Display): Add `# TODO(SC-005): display credential source per-provider in conversus status output` at the point in the `conversus status` handler where per-provider credential state would be reported.

4. **PR description follow-on spec reference** (from Dispute: `conversus status` Credential-Source Display): SC-004 PR description must explicitly name the follow-on: "SC-005: `conversus status` credential-source display."

---

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| `conversus status` Credential-Source Display | Defer with TODO comment + PR description reference | High | Principles I, II, and III jointly mandate scope discipline; synthesizer convergence supports; skeptical's Phase 4 flexibility clause creates acceptance conditions for deferral |
| Fallback Log Line Frequency | DEBUG level, stateless, every trigger | High | Principle IX prohibits marker-file state; Principle X requires clean output; synthesizer's third-path resolution satisfies both; no residual tension with either agent's grounding argument |
| Startup Sweep Frequency | DEBUG level, stateless, once per invocation | High | Same constitutional grounding as Fallback Log Line Frequency; both disputes share the identical root tension (stateless vs. noise) resolved by the same mechanism (log level change rather than state addition) |

The deliberation quality was high. All three remaining disputes are editorial questions — log level and scope boundary — not correctness questions. The six convergence points (directory creation, `os.replace`, `O_TRUNC`, per-provider file lock, Q1–Q4 directional verdicts) cover every correctness-critical decision. The disputes that persisted to arbitration were precisely the ones QUESTION.md left underspecified: which log level communicates migration state without becoming noise, and which command interface falls within a storage migration PR's scope. The systemic contradictions identified by the synthesizer — observability vs. scope discipline, Q2/Q3 coupling presented as independent, Windows correctness absent from the spec — are accurate meta-observations about migration spec quality. They are not defects in the conservative strategy's architecture but lessons for future spec authoring. No architectural rework is required; the conservative strategy's framework is sound.

---

**REQUIRED CHANGES TO CONSERVATIVE STRATEGY**

From arbitration rulings (implementation corrections beyond Phase 4 convergence points):

1. **Log level for fallback signal**: The conservative strategy does not specify a log level for the per-use fallback log line. Implementation MUST use `logging.DEBUG`, not INFO or WARNING.
2. **Log level for startup sweep**: The conservative strategy does not specify a log level for the startup sweep. Implementation MUST use `logging.DEBUG`, not INFO.
3. **`conversus status` deferral**: The conservative strategy does not mention `conversus status`. Implementation MUST add the TODO comment and PR description reference deferring status display to SC-005.

All other implementation requirements (directory creation at mode 0o700, `os.replace` over `os.rename`, `O_TRUNC` over `O_EXCL`, per-provider non-blocking file lock with 200ms timeout, Q1 preserve / Q2 lazy / Q3 permanent / Q4 no-transaction-log) were settled by unanimous Phase 4 convergence and carry no arbitration ACCEPT finding — they are pre-existing convergence obligations, not corrections from this arbitration.

---

**DIRECTIONAL VERDICTS**

- **Q1 verdict**: Preserve legacy — `auth.json` is never deleted, renamed, or modified by conversus after SC-004 lands. Users remove it manually. (Unanimous Phase 4 convergence; SC-001 precedent.)
- **Q2 verdict**: Lazy migration per-provider — migration triggers on first `CredentialStore.get(provider)` call when `credentials/{provider}.json` is absent. Not triggered at startup for all providers. (Unanimous convergence after Phase 3 skeptical concession.)
- **Q3 verdict**: Permanent fallback — `CredentialStore.get(provider)` falls back to `auth.json[provider]` indefinitely when the per-provider file is absent. No expiry. (Unanimous convergence after Phase 3 skeptical concession; lazy + time-bounded is degenerate.)
- **Q4 verdict**: Atomic rename sufficient — `.tmp` + `os.replace` is the correct and complete primitive. No transaction log required. Idempotent fallback handles partial state: a crash leaving no `credentials/{provider}.json` causes the next invocation to fall back to `auth.json[provider]` and retry. (Unanimous convergence, undisputed throughout all phases.)

---

**MIGRATION STRATEGY VERDICT: SHIP WITH MODIFICATIONS**

The conservative strategy's architecture is correct. Required modifications for SC-004: (1) DEBUG level for fallback log line; (2) DEBUG level for startup sweep; (3) TODO comment + PR description reference deferring `conversus status` changes to SC-005; plus the P1 implementation additions from Phase 4 convergence (directory creation at mode 0o700, `os.replace`, `O_TRUNC` mode, per-provider non-blocking file lock with 200ms timeout and `finally`-block `.tmp` cleanup). No architectural changes. The conservative strategy as proposed in QUESTION.md is shippable after these modifications.