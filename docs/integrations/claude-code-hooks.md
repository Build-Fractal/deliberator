# Deliberator snap-gate for Claude Code PreToolUse hooks

**Status:** Prototype (no formal spec yet). Validate-by-use before promoting to a v4.3.0+ mode spec.

`deliberator snap` is a cheap (~3 agents, single phase, Haiku-default, sub-2s wall-clock target) multi-agent deliberation that evaluates whether Claude Code should proceed with a tool call — most commonly a Bash command. It plugs into Claude Code's [PreToolUse hook](https://code.claude.com/docs/en/hooks-guide) lifecycle, returning `allow` / `deny` / `ask` per the [hooks JSON contract](https://code.claude.com/docs/en/hooks).

## Why multi-agent deliberation for hooks?

Claude Code already supports prompt-type hooks (single LLM evaluation). `deliberator snap` adds **adversarial composition**: a pragmatist + devil's-advocate + safety-auditor each produce an independent verdict. The aggregation rule is deterministic:

1. **Any DENY → DENY** (safety-wins).
2. **Else any ASK → ASK** (escalate to user).
3. **Else (unanimous ALLOW) → allow**.

Three independent Haiku calls voting can't simultaneously miss the same edge case the way a single LLM can on an off-day. For destructive commands (`rm -rf`, `git push --force`, `DROP TABLE`), this is the property the hook wants.

## Setup

### 1. Install deliberator

```bash
pip install deliberator    # or: uv tool install deliberator
deliberator login anthropic    # one-time OAuth setup
```

### 2. Add the hook to `.claude/settings.json`

Most flexible config — narrow with both `matcher` (tool name) AND `if` (command pattern) to avoid spawning the deliberation for routine commands:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm * | git push --force* | git push -f * | DROP TABLE* | sudo *)",
            "command": "deliberator snap --hook-mode",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

The `if` condition is the cheap pre-filter: only commands matching the patterns trigger the deliberation. Routine `git status`, `ls`, `cd` calls skip the hook entirely.

### 3. Test it

In a Claude Code session, ask Claude to run a destructive command. The hook fires, deliberator snap runs three agents in parallel, and you'll see one of:

- **Silent allow** — three unanimous ALLOWs; Claude proceeds.
- **Permission prompt** — one or more ASKs; Claude Code prompts you.
- **Block + rationale** — any DENY; Claude Code refuses with the rationale shown.

## How it works

### Hook contract

When the matcher + `if` condition match, Claude Code pipes a JSON payload to the hook's stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build"
  }
}
```

`deliberator snap --hook-mode` reads this, dispatches three agents in parallel against the command, aggregates verdicts, and emits the hook's expected response shape to stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "[deliberator snap, mixed-deny-wins] safety-auditor: Recursive force-remove targeting /tmp/build; if path was intended relative, the absolute form is irrecoverable."
  }
}
```

Per the hooks contract, exit code `0` + stdout JSON tells Claude Code to apply the `permissionDecision`. Exit code `2` would block + feed stderr back to the model.

### Agent composition

| Agent | Bias | When it ALLOWs / DENYs / ASKs |
|---|---|---|
| **pragmatist** | Permissive | DENYs clearly destructive commands with no redeeming context; ALLOWs routine work freely. |
| **devils-advocate** | Skeptical | Looks for typo escalation (`rm -rf .` vs `rm -rf ./build`), dangerous defaults, exfiltration; leans ASK or DENY on ambiguity. |
| **safety-auditor** | Conservative | DENYs irrecoverable operations, uncommitted-work deletion, force-push to shared branches, state-mutation outside project. |

### Failure modes

- **LLM failure / network error**: that agent's verdict defaults to `ASK` (never silent ALLOW). If all three fail, the hook returns ASK and Claude Code prompts the user. Deliberator snap NEVER fail-opens to ALLOW.
- **Malformed stdin JSON**: exit code `2` with stderr message; the hook system surfaces the error and blocks the tool call.
- **Empty command**: same as malformed stdin — exit code `2`.

### Latency budget

Target: 1-3 seconds total wall-clock. Each Haiku call is ~500ms–1s; the three run in parallel so total is bounded by the slowest. The first call per Claude Code session pays a model spin-up cost; subsequent calls amortize.

If routine commands skip the hook (via `if` pattern narrowing), the latency only matters for the destructive-command subset where it's worth the wait.

## Direct CLI usage (no hook)

```bash
$ deliberator snap --command "git push --force origin main"
{
  "verdict": "DENY",
  "rationale": "safety-auditor: Force-push to a shared branch overwrites collaborators' commits without warning.",
  "consensus": "unanimous-deny",
  "total_latency_ms": 1840.3,
  "agent_verdicts": [
    {
      "agent": "pragmatist",
      "verdict": "DENY",
      "rationale": "Force-push to main is rarely the right move; pragmatic concerns favor safe alternatives like --force-with-lease.",
      "latency_ms": 1654.1
    },
    {
      "agent": "devils-advocate",
      "verdict": "DENY",
      "rationale": "If 'main' is shared, this silently destroys others' commits.",
      "latency_ms": 1798.4
    },
    {
      "agent": "safety-auditor",
      "verdict": "DENY",
      "rationale": "Force-push to a shared branch overwrites collaborators' commits without warning.",
      "latency_ms": 1840.3
    }
  ]
}
```

## Tuning

| Lever | Effect |
|---|---|
| Narrow `if` patterns | Fewer hook invocations → lower cost + latency overhead |
| `--model` | Trade speed for depth (e.g., `--model claude-sonnet-4-6` for higher-stakes commands) |
| `timeout` in hook config | Hard ceiling per hook; default is 10s — adjust per environment |

## Known limitations of the prototype

1. **No caching** — identical commands within a session re-run the deliberation. Future improvement.
2. **No project context** — agents see the command + cwd, but not the project's git status, recent files, or session history. For high-stakes commands, this can miss context. Future: optional context injection.
3. **Fixed 3-agent composition** — no override for different agent panels per command class. Future: configurable agent panels per hook.
4. **No persistence** — verdict history isn't saved. Future: optional logging for post-hoc audit (would dogfood v4.2.0 Principle XXIX's structured-output discipline).

## Promotion path

This prototype is intentionally informal. If validated by real use (good UX, latency in budget, false-positive rate acceptable), it promotes to a v4.3.0+ mode spec:

- `templates/snap-gate/` extracted from inline prompts
- Full four-stage verification protocol on the formalized mode
- JSON Schema for the snap-gate envelope (extends v4.2.0 Component Principle XXIX)
- Engine integration via the `composition:` config field (matches deliberator-fractal sibling-product architecture)

For now: code first, spec when warranted.

## References

- Claude Code Hooks Guide: https://code.claude.com/docs/en/hooks-guide
- Claude Code Hooks Reference: https://code.claude.com/docs/en/hooks
- Deliberator v4.2.0 (file persistence + structured outputs): `specs/v4.2.0-structured-deliberation-outputs/spec.md`
- deliberator-fractal CASE (streaming + recursive sibling product): `Build-Fractal/build-fractal-mono` → `deliberator/proposals/deliberator-fractal-CASE.md`
