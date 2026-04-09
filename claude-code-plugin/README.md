# Conversus — Claude Code Plugin

A Claude Code plugin that gives you a `/conversus` slash command for running competitive multi-agent deliberation directly from your editor.

## Install

```
/plugin install https://github.com/build-fractal/conversus-oss
```

Or install the CLI first:

```bash
pip install git+https://github.com/Build-Fractal/conversus.git
```

## Usage

```
/conversus run conversus.yml --provider anthropic
/conversus decide "Should we use Postgres or MongoDB?" --provider anthropic
/conversus validate conversus.yml
/conversus init
/conversus status
```

## Subcommands

| Command | Description |
|---|---|
| `run <config>` | Full deliberation from a `conversus.yml` config file |
| `decide "<question>"` | Ad-hoc deliberation on a natural-language question |
| `validate <config>` | Check config validity and print cost estimate |
| `init` | Initialize project runtime permissions |
| `status` | Show provider authentication status |
| `login <provider>` | Authenticate with a model provider |
| `logout <provider>` | Remove stored credentials |

## Providers

`anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, and more. Default is `mock` (no API key needed, for testing).

## Example config

```yaml
mode: cooperative
target: spec.md
output: deliberations/

agents:
  - name: pragmatist
    prompt: |
      You evaluate proposals for practical feasibility and real-world tradeoffs.
  - name: devils-advocate
    prompt: |
      You challenge assumptions and surface risks the team may have missed.
```

Run it:

```
/conversus run conversus.yml --provider anthropic
```

## Links

- [Full documentation](https://github.com/build-fractal/conversus-oss)
- [Config reference](https://github.com/build-fractal/conversus-oss/blob/main/conversus.example.yml)
