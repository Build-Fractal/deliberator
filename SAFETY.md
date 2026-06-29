# SAFETY.md — Named Safety Perimeters & Their Independent Guards

**Status:** Active
**Satisfies:** Tier 2 (Suite) Principle XXIV — Safety-Critical Defense-in-Depth
**Companion file:** `CONFORMANCE.md` (declaration), `CONSTITUTION.md` (principle text)
**Updated:** On any change that adds, removes, or modifies a guard at a perimeter listed here, or that introduces a new perimeter. Each PR that touches a guard cited below must update the corresponding section's `file:line` reference and, if a guard is removed, the defense-in-depth assessment.

---

## Purpose

Principle XXIV requires that safety-critical paths implement
*multiple independent guards*. Until 2026-05-11 the suite-level conformance
declaration listed XXIV as Provisional because the perimeters and their
guards were never enumerated — "multiple guards" without a list of *what*
they defend and *where the guards live* is unfalsifiable. This document
closes that gap.

**Perimeter** is defined here as: any place in the engine where data
crossing a trust boundary, if accepted unchanged, could produce a silent
failure, code execution, data exfiltration, or a downstream gate
mis-decision. A perimeter is *guarded* when at least one explicit
mechanism (schema, validator, allowlist, escape function, sandbox path
check, retry-with-cap, etc.) sits between the untrusted input and the
sensitive sink. A perimeter is *defense-in-depth-compliant* when **two
or more independent guards** would each, on their own, stop a
representative attack.

The audit below is grounded in actual code, not aspirational design.
Every guard cites `file:line`. If a citation falls out of sync with the
code, the audit has decayed and this file MUST be regenerated as part
of the change that moved the line.

---

## P1 — User config YAML → Engine

**What crosses:** A `deliberator.yml` document supplied by a human operator
or by the `deliberator_run` MCP tool. The file declares the mode, the
agents, file paths to read as `target`/`prior`, the provider, and the
output directory. Any of these fields is attacker-supplied in the MCP
case.

**Threat model:** Malformed mode coerces the engine into an invalid
dispatch table cell; unbounded `rounds` or `iterations` produces an
LLM-spend DoS; provider name slips a non-allowlisted backend past
validation; relative paths in `target:` escape the project root.

**Guards:**

1. **YAML safe loader.** `yaml.safe_load` (never `yaml.load`) is used at
   every entry point that reads operator YAML:
   `engine/config.py:275`, `engine/config.py:597`, `engine/handlers.py:230`,
   `engine/handlers.py:516`. Prevents arbitrary Python instantiation via
   YAML tags.
2. **Mode allowlist.** `engine/config.py:611` rejects any `mode` not in
   `VALID_MODES`, which is itself derived from
   `deliberator.schemas.modes.VALID_MODES` (`engine/config.py:19`) — the
   single source of truth for the dispatch enum.
3. **Provider allowlist.** `engine/config.py:665` rejects any `provider`
   not in `VALID_PROVIDERS`.
4. **Stagnation enum.** `engine/config.py:655` rejects values other than
   `detect`/`ignore`.
5. **Rounds ceiling.** `engine/config.py:644` rejects `rounds` outside
   `[1, 5]`; the upper bound is a deliberate spend ceiling.
6. **Iterations floor.** `engine/config.py:637` rejects non-integer or
   `< 1` values.
7. **Agent name regex.** `engine/config.py:689` rejects agent names that
   do not match `AGENT_NAME_RE = ^[a-z0-9][a-z0-9\-_]*$`
   (`engine/config.py:118`).
8. **Duplicate-name check.** `engine/config.py:697` rejects YAML where
   two agents share a name.
9. **Two-agent minimum.** `engine/config.py:682` rejects configs with
   fewer than two agents (the deliberation contract assumes
   adversarial-pair minimum).
10. **Existence-on-disk check.** `engine/config.py:250` (in
    `_resolve_file_entries`) rejects `target:` / `prior:` entries that
    resolve to non-existent paths — the resolved path must exist before
    the engine accepts the config.

**Defense-in-depth status:** Compliant. Each field has its own
typed validator; the YAML safe loader is itself an independent layer
that would block tag-based injection even if every field check were
bypassed.

---

## P2 — MCP tool surface → Engine entry

**What crosses:** Arguments passed to `mcp_server.deliberator_validate`,
`mcp_server.deliberator_run`, `mcp_server.deliberator_decide`,
`mcp_server.list_deliberations`, `mcp_server.read_deliberation_file`.
These are caller-supplied across the MCP protocol; the MCP host is
trusted, the *content* of its tool-call arguments is not.

**Threat model:** A malicious tool call submits a provider name the
engine registry would resolve but the MCP contract does not document
(silent fall-through into a subprocess that fails opaquely); a
deliberation-cost-DoS via a config that estimates to thousands of
launches; an MCP caller asks for a file path outside the deliberations
sandbox.

**Guards:**

1. **MCP-supported provider allowlist.** Distinct from and stricter
   than the engine's `VALID_PROVIDERS`. Defined at
   `engine/handlers.py:94` as `_MCP_SUPPORTED_PROVIDERS = frozenset({"mock",
   "demo", "anthropic", "openai", "claude-desktop"})`. Enforced by
   `_validate_mcp_provider` (`engine/handlers.py:99`), called *before*
   the pipeline runs at `engine/handlers.py:198` and `engine/handlers.py:562`.
   Spec 045 documents the silent-fallback bug this guard fixes.
2. **Empty-question rejection.** `engine/handlers.py:163` returns a
   structured error rather than dispatching agents on whitespace input.
3. **Question classifier.** `engine/handlers.py:172` calls
   `classify_question` to reject questions that are too vague to
   deliberate over; the classifier itself is a guard against
   meaningless-LLM-spend.
4. **Cost gate (`max_launches`).** `engine/handlers.py:234` rejects any
   resolved config whose estimated launches exceeds `max_launches`
   (default 20, configurable via the cascade). Settings cascade is
   `engine/settings.py:184`.
5. **Disabled-tools env knob.** Operator can hide any MCP tool by name
   via `DELIBERATOR_DISABLED_TOOLS`. Implemented in `mcp_server.py:97`
   (parser) and `mcp_server.py:120` (`_optional_tool` decorator).
   Independent of the engine guards above; the tool simply never
   registers if disabled.

**Defense-in-depth status:** Compliant. The provider allowlist and the
cost gate would each individually block a tool-call abuse;
the question classifier and empty-question check independently filter
upstream of dispatch.

---

## P3 — File IO at the deliberation sandbox

**What crosses:** A `deliberation_path` plus `file_path` argument pair
into `read_deliberation_file` (called from the MCP surface and from
the CLI's deliberation-history viewer). The caller supplies these as
strings; both can be relative, both can contain `..`, both can be
absolute, both can contain null bytes, and either can be a symlink
target.

**Threat model:** Classic path traversal — read `/etc/passwd` or any
file on the host. The deliberation history is meant to be a read-only
view onto `<project_root>/.deliberator/deliberations/` and nothing else.

**Guards:**

1. **Resolved-path containment check.** `engine/persistence.py:353`
   computes `target.resolve()` and rejects anything not
   `is_relative_to(delib_root)`. This resolves symlinks before
   comparison, so a symlink whose target is outside the sandbox is
   rejected on the *resolved* path, not the *literal* path.
2. **Existence-as-file check.** `engine/persistence.py:358` rejects
   any resolved path that is not a regular file (directory or special
   file access is denied even if the resolved path is inside the
   sandbox).
3. **Contract test suite reproducing each known attack.**
   `engine/tests/test_security.py` covers `..` traversal
   (`test_path_traversal_dot_dot`), URL-encoded `..`
   (`test_path_traversal_encoded`), absolute paths
   (`test_path_traversal_absolute`), null-byte injection
   (`test_path_traversal_null_byte`), and symlink escape
   (`test_path_traversal_symlink`). These tests are the third defense
   layer required by Principle XXIV's clause 3 (contract test
   reproducing the failure scenario).

**Defense-in-depth status:** Compliant. Containment check and
is-file check are independent (the second still rejects directory
traversal that lands inside the sandbox); the test suite enforces
the contract under CI.

---

## P4 — Capability metadata → Generated CLI/MCP source

**What crosses:** Capability metadata (summary, param help, default
values, handler strings) registered via `deliberator.registry.Capability`
flows through `project_to_cli` / `project_to_mcp` in
`deliberator/registry/projector.py`, which *emits Python source code*
that is then `exec`'d by the surface adapter. If any metadata string
appears unescaped in the emitted source, it executes as Python.

**Threat model:** A plugin author (intentional or accidental) ships a
capability whose `summary` is `"); import os; os.system("rm -rf /")"`,
which — if interpolated raw into a `help=...` argument — escapes the
string literal and executes the payload at adapter import time.

**Guards:**

1. **`literal()` rendering helper.** `deliberator/registry/adapters/_helpers.py:15`
   wraps every emitted string in `json.dumps`, which produces a
   correctly-escaped double-quoted Python literal. Bool and None are
   handled separately because `json.dumps` would emit `true`/`null`,
   which are not valid Python literals.
2. **Handler-string shape check.** `deliberator/registry/adapters/_helpers.py:53`
   (`split_handler`) rejects handler strings that do not match the
   `module.path:func_name` shape with exactly one colon. A malformed
   handler is caught at registration time rather than leaking into
   generated source as a `NameError` at import time — or worse, as
   call to an unintended symbol.
3. **Compile-clean contract tests.** `engine/tests/test_security.py:121`
   (`test_projector_escapes_malicious_summary`) and
   `engine/tests/test_security.py:145`
   (`test_projector_escapes_malicious_param_help`) compile the emitted
   source and assert it parses; if a future regression let injection
   break out of the string literal, `compile()` would raise. These
   tests are the contract-test layer required by Principle XXIV.

**Defense-in-depth status:** Compliant. `literal()` and the
shape-check guard independent injection vectors (string-literal escape
vs. handler-name leakage); the compile-clean tests would catch a
regression in either.

---

## P5 — Synthesis text → Downstream gates

**What crosses:** The final synthesis markdown produced by an LLM
agent flows into `parse_synthesis` (`linter/output_contract.py`),
which extracts a `QualityIndicators` struct that downstream CI gates
and dashboards then read. The LLM output is untrusted — it can omit
fields, lie about the agent count, or return a chat-message receipt
instead of a real synthesis.

**Threat model:** A misbehaving tool-use-capable agent writes the real
synthesis to disk via the Write tool and returns only a conversational
receipt as its response — the engine then clobbers the real file with
the receipt. The receipt looks like prose, every regex extractor
returns the schema default of `0`, and the downstream gate reads
"zero disputes, clean convergence" as a PASS. This is the spec 027
postmortem class of bug.

**Guards:**

1. **`UnparseableSynthesisError` on no-structural-markers.**
   `linter/output_contract.py:543` raises rather than silently returning
   defaults when every structural probe misses (no agent count, no
   disputes, no convergence section, no scorecard). The error is a
   distinct type from `ValueError` so callers can catch
   parse-failure-as-PASS specifically.
2. **Engine-injected authoritative metadata block.** When the engine
   itself writes the metadata block (`<!-- DELIBERATOR:METADATA ... -->`
   pattern at `linter/output_contract.py:120`), the parser prefers it
   over LLM prose extraction (`linter/output_contract.py:246`,
   `linter/output_contract.py:284`). The engine's own count is
   authoritative; LLM prose is a fallback for older fixtures.
3. **Frozen Pydantic schema.** `QualityIndicators`
   (`linter/output_contract.py:63`) is `model_config = {"frozen": True}`
   with every field non-optional. A parser that fails to populate
   any field raises at construction, not at downstream consumption.
4. **Disagreement-count cross-check.** `check_disagreement`
   (`linter/quality.py`) is called independently of the regex
   extraction path and feeds its result into the same
   `QualityIndicators` struct, providing a second extraction of
   dispute counts that would disagree with a confabulated synthesis.

**Defense-in-depth status:** Compliant. The structural-markers check,
the engine-metadata override, and the frozen Pydantic schema each
independently block a defaulted-zero false-PASS.

---

## P6 — Arbiter `resolution.md` → Next-round disagreement check

**What crosses:** The arbiter writes `resolution.md` at the end of an
arbitration phase. `extract_addressed_disputes`
(`linter/arbitration_parser.py:51`) reads the file and returns the
addressed dispute titles; those titles feed into the next round's
`check_disagreement` via the `arbiter_addressed` kwarg
(`engine/phases.py:1022`). If the parser produces a wrong list, the
next round's stagnation/convergence detection silently miscounts
disputes.

**Threat model:** Malformed arbiter output (heading-level drift,
trailing whitespace anomalies, missing titles) makes the parser
return either a spurious title (suppressing a real dispute as
"already addressed") or miss a real title (failing to suppress an
addressed dispute, producing fake stagnation).

**Guards:**

1. **Strict heading regex.** `linter/arbitration_parser.py:43`
   accepts only heading levels 2–4 with the literal `Dispute:` keyword
   and a non-empty title; `[^\S\n]` whitespace class prevents greedy
   consumption of the next heading line.
2. **Best-effort parsing contract.** `linter/arbitration_parser.py:68`
   returns `[]` rather than raising on missing/unreadable files —
   the downstream `check_disagreement` has its own dispute-count path
   (`engine/phases.py:1029`) that does not depend on arbiter input.
   This is *defense by independent path*: if the arbiter parser
   returns empty, the dispute count still works.
3. **Defensive `strip()` on captured title.**
   `linter/arbitration_parser.py:84` strips the captured group
   defensively even though the regex already trims; the second
   strip is the second layer.

**Defense-in-depth status:** Compliant. Strict regex + independent
disagreement path means a parser regression cannot, on its own,
corrupt the stagnation termination decision.

---

## P7 — Subprocess execution provider → External CLI

**What crosses:** Prompts, file paths, model IDs, and API keys flow
into `SubprocessProvider.execute` (`engine/execution/providers/subprocess_base.py:198`)
and from there into `asyncio.create_subprocess_exec` for the
claude-code, gemini, aider, opencode, codex, copilot, and pi
providers.

**Threat model:** Prompt content containing `---` markers misinterpreted
as CLI flags; secrets leaking into argv (visible via `ps`); subprocess
that hangs indefinitely; binary-not-found surfacing as an opaque
crash deep in dispatch.

**Guards:**

1. **`create_subprocess_exec` (not shell).**
   `engine/execution/providers/subprocess_base.py:217` — `argv` is
   passed positionally; no shell interpolation. A prompt cannot
   smuggle shell metacharacters.
2. **Prompt-via-stdin convention.**
   `engine/execution/providers/claude_code.py:175` (`_build_stdin`)
   pipes the prompt via stdin rather than argv, sidestepping
   `--`-marker misinterpretation entirely.
3. **Env-only secrets contract.** Documented at
   `engine/execution/providers/subprocess_base.py:117` (`_build_argv`
   docstring): *"Secrets MUST NOT appear in argv — use `_build_env`
   instead."* `_build_env` is enforced at the abstract-method level
   (`engine/execution/providers/subprocess_base.py:137`); the
   claude-code implementation puts `ANTHROPIC_API_KEY` exclusively in
   env (`engine/execution/providers/claude_code.py:184`).
4. **Subprocess timeout with SIGTERM → SIGKILL escalation.**
   Documented at `engine/execution/providers/subprocess_base.py:204`;
   default 300s, per-task overridable via `task.metadata["timeout"]`.
5. **`FileNotFoundError` / `OSError` capture.**
   `engine/execution/providers/subprocess_base.py:225` and `241`
   convert "binary not installed" and "spawn failed" into structured
   `ProviderError` with `category="subprocess"` — the dispatch layer
   sees a typed error, not an unhandled exception cascade.

**Defense-in-depth status:** Compliant. The no-shell + stdin-piping +
env-only-secrets stack ensures three independent vectors (shell
injection, flag injection, argv-leaked-secret) are each blocked
without relying on the other.

---

## P8 — Provider rate-limit response → Dispatch loop

**What crosses:** HTTP `429` responses from the Anthropic or OpenAI
providers. The dispatch layer fans agents out concurrently; without
guards, a 429 cascade aborts the whole deliberation.

**Threat model:** Subscription OAuth tokens collide under modest
concurrency producing transient 429s that look indistinguishable
from sustained quota exhaustion; an unbounded retry loop looks like
an abuse pattern to the upstream provider; a missing `Retry-After`
hint defaults to overly-aggressive client-side backoff.

**Guards:**

1. **Bounded retry budget.** `engine/providers/anthropic.py:28`
   (`_RETRY_MAX_ATTEMPTS = 3`); `engine/providers/anthropic.py:174`
   loops over `range(_RETRY_MAX_ATTEMPTS)`, never beyond.
2. **Server-honored `Retry-After`.**
   `engine/providers/anthropic.py:33` (`_retry_after_seconds`) prefers
   the server's hint over client-side backoff; falls back to jittered
   exponential only when absent or malformed.
3. **Capped jittered exponential backoff.**
   `engine/providers/anthropic.py:62` — `uniform(0, min(base*2^attempt,
   cap))` with `_RETRY_BACKOFF_CAP_SECONDS = 30.0` upper bound.
4. **Per-provider concurrency semaphore.**
   `engine/dispatch.py:498` (`provider_sems`) gates concurrent calls
   by `effective_concurrency` declared on the provider — limits 429s
   at the source rather than relying on retries to absorb them.
5. **Typed `ProviderError(category="rate_limit", status_code=429)`.**
   `engine/errors.py:73` produces the typed error so the dispatch
   layer can pattern-match rate-limit vs. other failures.

**Defense-in-depth status:** Compliant. The concurrency semaphore
prevents 429s at the source; the bounded retry with server-honored
backoff absorbs the ones that slip through; the typed error means
dispatch failures are categorizable rather than opaque.

---

## P9 — Environment variable settings cascade → Engine

**What crosses:** Operator-supplied environment variables
(`DELIBERATOR_DEFAULT_PROVIDER`, `DELIBERATOR_MAX_LAUNCHES`, etc.) flow
through `engine.settings.load_settings`.

**Threat model:** Malicious env var like
`DELIBERATOR_DEFAULT_PROVIDER="'; DROP TABLE users; --"` or
`DELIBERATOR_MAX_LAUNCHES="not_a_number"`; injection into downstream
code that treats settings as raw strings.

**Guards:**

1. **Type-coerce-or-warn on numeric fields.**
   `engine/settings.py:186` calls `int()` inside a try/except;
   `engine/settings.py:188` logs a warning and falls back to default
   rather than crashing.
2. **Provider name validated downstream by resolve_provider.**
   The settings layer stores the string as-is, but `resolve_provider`
   (`engine/auth.py`) only resolves names in the known-providers map;
   unknown names raise `ProviderError`. Tested at
   `engine/tests/test_security.py:193` (`test_settings_cascade_sanitizes_provider`).
3. **Contract tests on malicious env input.**
   `engine/tests/test_security.py:207`
   (`test_settings_cascade_invalid_max_launches`) verifies the
   non-numeric fallback path.

**Defense-in-depth status:** Compliant. Type-coercion and downstream
provider-allowlist resolution are independent; either alone would
block the represented attack class.

---

## P10 — Ad-hoc agent display name → Generated config

**What crosses:** A caller-supplied display name (`"UX Reviewer"`) is
slug-converted by `_sanitize_agent_name` (`engine/adhoc.py:19`) into
a config name (`"ux-reviewer"`), which is then written into a
generated `deliberator.yml` document.

**Threat model:** Display names containing YAML-special characters
(colons, brackets, newlines) corrupt the generated config; collisions
between sanitized names silently merge two agents into one.

**Guards:**

1. **Slug regex.** `engine/adhoc.py:27`:
   `re.sub(r"[^a-z0-9]+", "-", slug)` strips any character not
   alnum-lowercase to a hyphen; `engine/adhoc.py:30` falls back to
   `"agent"` for empty input.
2. **Downstream `AGENT_NAME_RE` validation.** The generated config is
   parsed by the same `parse_config` path as a hand-written YAML,
   so the agent-name regex at `engine/config.py:689` is a second
   independent check.
3. **Collision deduplication.** `engine/adhoc.py:164` appends a
   numeric suffix when two display names sanitize to the same slug.

**Defense-in-depth status:** Compliant. Slug regex at construction
and `AGENT_NAME_RE` at parse are independent.

---

## Follow-on candidates (single-guard or unguarded perimeters)

These are not violations of Principle XXIV today — most of them are
defended by *contract* (e.g., "only the engine writes here") rather
than by a code guard. They are listed here so future audits know
where the next defense-in-depth investment should land.

1. **JSONL streaming output parsing in subprocess providers.**
   `engine/execution/providers/codex.py:186`,
   `engine/execution/providers/opencode.py:159`,
   `engine/execution/providers/gemini.py:114`,
   `engine/execution/providers/claude_code.py:203` each call
   `json.loads` on a line of subprocess output. There is no schema
   validation layer between the JSON and the `ExecutionResult` struct.
   The contract today is "we trust the CLI tool" — a future PR could
   add a Pydantic envelope check as a second layer (cheap; small).
2. **Settings cascade env-var-name allowlist.** Today
   `engine/settings.py:239` maps known config fields to known env vars;
   the inverse — rejecting unrecognized `DELIBERATOR_*` env vars — is
   not enforced. An unknown `DELIBERATOR_X` is silently ignored. This is
   a usability gap more than a safety gap, but a typo'd
   `DELIBERATOR_MAX_LAUNCHE` (note the missing `S`) would silently keep
   the default rather than warn.
3. **`literal()` `repr()` fallback for non-stringable values.**
   `deliberator/registry/adapters/_helpers.py:41` returns `repr(value)`
   for types it doesn't explicitly handle. `repr()` of a malicious
   `__repr__` method on a third-party type could in principle emit
   invalid Python. Today the registry only accepts a small fixed set
   of param types so this is a defense-by-typing-contract; a follow-on
   could explicitly reject unsupported types at registration time.

---

## Auditing

This file is hand-maintained. The audit cadence is:

- **On every PR that adds, removes, or modifies a guard at a listed
  perimeter:** the PR MUST update the relevant section's `file:line`
  citation. If a guard is removed, the PR MUST update the
  defense-in-depth-status line and either justify removal (e.g., the
  perimeter was eliminated) or add a follow-on entry.
- **On every PR that introduces a new perimeter** (new untrusted-input
  entry point, new external-process invocation, new file-IO surface
  taking user-supplied paths): the PR MUST add a new section to this
  file enumerating its guards.
- **Annually as part of the suite-level re-audit** (next: 2027-05-06):
  spot-check that every cited `file:line` still points to the guard it
  claims to. A `linter` extension that mechanically verifies this is
  tracked as a follow-on under Principle XII's dead-infrastructure
  linter family.

---

## Provenance

Created 2026-05-11 to close out the Principle XXIV Provisional
remediation tracked in `CONFORMANCE.md`. The remediation was opened
2026-05-07 against the 2026-05-06 originating tier-extraction
deliberation, with a 2026-09-01 deadline; closed early.

Future amendments to this file are governed by `GOVERNANCE.md` and
require a constitutional-pathway deliberation only when they would
modify Principle XXIV itself; updates to perimeter citations or
guard inventories are routine engineering changes.
