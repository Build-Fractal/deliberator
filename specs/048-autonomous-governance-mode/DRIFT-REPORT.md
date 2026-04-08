# Spec 048 Drift Report — Autonomous Governance Mode

**Analyzed**: 2026-04-05
**Spec status**: Draft (unblocked by spec 042 ruling 2026-04-05)
**Codebase ref**: `engine/cli/context.py`, `engine/cli/__init__.py`, `engine/project.py`, `engine/execution/providers/`

---

## Summary

Four drift vectors identified. Two are superseded by newer specs, one is a partial implementation with missing CLI wiring, and one is a stale provider count that no longer matches the actual registry. None are blockers to spec validity; all must be resolved before implementation begins.

---

## Drift 1 — `.conversusrc` schema superseded by spec 050

**Severity**: Design-level (implementation must follow spec 050, not spec 048 §3)

**Spec 048 §3 defines**: `.conversus/.conversusrc` as a YAML file with top-level keys `version`, `grounding`, `default_agents`, `arbiter`, `gates`, `executor`, `output`.

**Actual codebase**: `engine/project.py` manages `.conversus/settings.json` (JSON, not YAML). The `init_project()` function creates `settings.json` with keys `default_provider`, `default_model`, `output_dir`, `runtimes`. There is no `.conversusrc` loader, no YAML parser for this path, no schema enforcement for spec 048 §3 fields.

**Superseding spec**: `specs/050-cascading-settings/spec.md` (Replaces: `.conversusrc` from spec 048 §3) explicitly subsumes the `.conversusrc` design. Spec 050 §5 states governance config moves into the `"governance"` key of `.conversus/settings.json`. The governance YAML block from spec 048 §3 maps to `settings.governance` as a JSON sub-object.

**Migration path from spec 050**: `.conversusrc` is still read for backward compat if `settings.json` has no `"governance"` key. New projects use `settings.json` exclusively. Spec 048 implementation must target `settings.governance`, not a standalone `.conversusrc` file.

**Action required**: Spec 048 §3 is the design statement of intent; spec 050 is the implemented schema. The implementation of spec 048 must read from and write to `settings.json`'s `governance` key via the spec 050 `SettingsResolver`. Do not implement `.conversusrc` as a separate YAML file.

---

## Drift 2 — Provider count mismatch (spec says 4; codebase has 12)

**Severity**: Cosmetic (spec reference is stale; does not affect correctness)

**Spec 048 references**: "4 execution providers" in §0 (the 042 Integration Note) and in §14 (spec 042 dependency description). The note says the v1 set is `mock`, `anthropic`, `claude-code`, `opencode` (plus optional litellm companion).

**Actual codebase** (`engine/execution/providers/__init__.py`): 12 provider modules are registered at import time:

1. `mock`
2. `anthropic`
3. `claude_code`
4. `aider`
5. `opencode`
6. `openai_compat`
7. `codex`
8. `copilot`
9. `gemini`
10. `pi`
11. (plus `subprocess_base` as a shared base, not registered)

The `--provider` CLI option in `engine/cli/__init__.py` accepts 13 named choices including `ollama`, `llama-cpp`, `vllm`, `codex`, `copilot`, `gemini`, `pi` alongside the spec 042 original four.

**Root cause**: Spec 042's binding arbitration resolved on a 4-provider v1 plan. Implementation shipped 12. The `engine/execution/provider.py` docstring still says "4-provider v1 set" — also stale.

**Action required**: Update spec 048's dependency description to say "12+ execution providers" and remove the specific v1 set enumeration. The `.conversusrc`/`settings.governance` `executor.provider` field example (`claude-code-headless`) should be clarified — the registered name is `claude-code`, not `claude-code-headless`. Separately, the stale "4-provider v1" comment in `engine/execution/provider.py:300` is a code-level doc debt but is not a spec 048 issue.

---

## Drift 3 — `conversus governance` CLI subcommand is wired but not implemented

**Severity**: Functional gap (the spec's primary CLI surface does not exist)

**Spec 048 §5 defines**: The `conversus governance <target>` subcommand with flags `--gate`, `--post-to`, `--dry-run`, `--add-grounding`, producing structured JSON output and using governance exit codes (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE, 4=WARNING).

**Actual codebase**:

- `engine/cli/__init__.py` defines: `run`, `decide`, `validate`, `login`, `logout`, `status`, `context`, `init`. There is **no `governance` subcommand**.
- `engine/cli/context.py` **does** detect the `governance` subcommand in `_GOVERNANCE_SUBCOMMANDS = ("governance", "gate")` and selects `exit_code_scheme="governance"` when `argv[1]` matches. Tests in `engine/tests/test_cli_context.py` verify this behavior (lines 151–153, 265–274).
- The exit code scheme docstring in `context.py` lists only three codes: `0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE` — it **omits** `4=WARNING` that spec 048 FR-014/FR-015 require as a stable CI interface.

**State**: The context detection layer is forward-compatible (it will correctly detect and route `conversus governance` invocations when the subcommand is added). The subcommand itself is missing. The exit code scheme enum (`ExitCodeScheme`) only has two values (`"interactive"`, `"governance"`) — the actual exit code values (0–4) are not yet enumerated in code; that's expected for a spec that hasn't been implemented.

**Action required**: No spec text changes needed. Track as implementation gap: Phase 3 of spec 048's phasing plan is the `conversus governance` CLI subcommand. Also note that when implementing, the `ExitCodeScheme` docstring in `context.py` must be extended to include exit code 4 (WARNING).

---

## Drift 4 — `claude-agent-sdk` language in spec vs. resolved binding condition

**Severity**: Clarity (spec header accurately reflects the resolution; body reference is an artifact of the draft timeline)

**Spec 048 §0** (042 Integration Note): "claude-code-headless executor is direct `claude` CLI subprocess via spec 042's `SubprocessProvider`, **no `claude-agent-sdk` dependency**" — this is correct and reflects the spec 042 binding condition §5.1.

**Actual codebase** (`engine/execution/provider.py:300`): "direct `claude` CLI subprocess, no `claude-agent-sdk` dependency" — matches spec 048's Integration Note exactly. The `claude_code.py` provider uses `asyncio.create_subprocess_exec` calling `claude -p --bare`.

**Residual risk**: `specs/042-execution-providers/spec.md:317` still has a table row listing `@anthropic-ai/claude-agent-sdk (subprocess or Node bridge)` as the claude-code execution method — this is a pre-arbitration draft row that was explicitly corrected in the binding ruling (resolution.md §5.1: "Winner drops `claude-agent-sdk` from v1 entirely"). The spec 042 source document has not been updated to strike this row.

**Action required**: None in spec 048 itself — the §0 note is accurate. The stale `claude-agent-sdk` row in `specs/042-execution-providers/spec.md:317` is a spec 042 housekeeping item, not a spec 048 drift issue.

---

## Non-drift observation — `find_conversus_dir()` already exists

Spec 048 FR-001 requires `conversus governance` to walk upward from target/cwd to find `.conversus/.conversusrc`. The function `find_conversus_dir(start: Path) -> Path | None` in `engine/project.py` (lines 257–268) already implements this walk for the `.conversus/` directory. The governance config discovery (FR-001) can delegate to this function; it only needs to then look for `settings.json`'s `governance` key (spec 050 shape) rather than `.conversusrc`.

---

## Non-drift observation — `conversus init` vs. governance config

Spec 048 §3.2 says `.conversusrc` is checked into the repo. Under spec 050, the equivalent is `.conversus/settings.json`'s `governance` key. The existing `conversus init` command (via `engine/project.py`) creates `settings.json` but only writes `default_provider`, `default_model`, `output_dir`, `runtimes` — it does not write a `governance` stub. Spec 048 Phase 1 (config parser) will need to either extend `init` with a `--governance` flag or document that governance config is written manually.

---

## Summary table

| # | Drift vector | Severity | Spec source | Code location | Resolution |
|---|---|---|---|---|---|
| 1 | `.conversusrc` YAML superseded by `settings.json` governance key | Design | spec 048 §3 | `engine/project.py` | Implement against spec 050 `settings.governance`; do not create `.conversusrc` |
| 2 | Provider count 4 → 12 in codebase | Cosmetic | spec 048 §0, §14 | `engine/execution/providers/__init__.py` | Update spec 048 dependency description; note `claude-code` is the registered name (not `claude-code-headless`) |
| 3 | `conversus governance` subcommand missing from CLI | Functional gap | spec 048 §5 | `engine/cli/__init__.py` | Implement as Phase 3; context detection is already wired; add exit code 4 (WARNING) to `context.py` docstring |
| 4 | `claude-agent-sdk` reference stale in spec 042 body (not 048) | Clarity | spec 042 §11 table | `specs/042-execution-providers/spec.md:317` | Spec 042 housekeeping; no change to spec 048 |
