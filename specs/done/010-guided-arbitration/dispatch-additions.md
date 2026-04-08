# Dispatch Table Additions for Guided Arbitration

## Changes to SKILL.md Subcommand Dispatch section

### 1. New routing table row

Add to the dispatch table:

```
| `/conversus arbitrate [path] [--force]` | [Arbitrate: Guided Arbitration](#arbitrate-guided-arbitration) |
```

The full table becomes:

| Invocation | Routes to |
|---|---|
| `/conversus run [config]` | [Run: Input](#run-input) -- full deliberation engine |
| `/conversus define [description]` | [Define: Problem Definition](#define-problem-definition) |
| `/conversus interests [options]` | [Interests: Interest Discovery](#interests-interest-discovery) |
| `/conversus mode [options]` | [Mode: Mode Selection](#mode-mode-selection) |
| `/conversus converge` | [Converge: Guided Execution](#converge-guided-execution) |
| `/conversus arbitrate [path] [--force]` | [Arbitrate: Guided Arbitration](#arbitrate-guided-arbitration) |
| `/conversus` (no arguments) | Defaults to `run` (backward compatible) |

### 2. Updated "Available subcommands" line

Change:

```
Available subcommands: `run`, `define`, `interests`, `mode`, `converge`.
```

To:

```
Available subcommands: `run`, `define`, `interests`, `mode`, `converge`, `arbitrate`.
```

### 3. Updated "Future subcommands" line

Change:

```
Future subcommands (not yet implemented): `arbitrate`, `gate`.
```

To:

```
Future subcommands (not yet implemented): `gate`.
```

### 4. Updated error message

Change:

```
> Unknown subcommand: '{cmd}'. Available commands: run, define, interests, mode, converge. (Future: arbitrate, gate)
```

To:

```
> Unknown subcommand: '{cmd}'. Available commands: run, define, interests, mode, converge, arbitrate. (Future: gate)
```

### 5. Updated description frontmatter

In the YAML frontmatter `description` field, add `arbitrate` to the subcommand list:

Change:

```
  Supports subcommands: run
  (deliberation engine), define (problem definition), interests
  (interest discovery), mode (mode selection and config generation),
  converge (guided execution with pre/post UX).
```

To:

```
  Supports subcommands: run
  (deliberation engine), define (problem definition), interests
  (interest discovery), mode (mode selection and config generation),
  converge (guided execution with pre/post UX), arbitrate (guided
  arbitration for dispute resolution).
```

### 6. Updated Converge post-execution report references

In the Converge handler's Post-Execution Report, the disputes section currently says:

```
    To resolve disputes, add an `arbiter:` section to `conversus.yml` and re-run `/conversus converge`. (A dedicated `/conversus arbitrate` command is planned.)
```

Change to:

```
    To resolve disputes, run `/conversus arbitrate` to configure an arbiter and resolve disputes.
```

This appears in two places within the Converge handler:
1. The "If disputes remain" status block
2. The "If disputes remain and no arbiter was configured" next steps block
