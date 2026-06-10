# Troubleshooting & FAQ

When something goes wrong with conversus, the failure usually falls into one of the buckets below. Each entry follows the "If you see X, do Y" pattern.

## Auth & providers

### `ProviderError: No credentials available for 'anthropic'`

You ran with `--provider anthropic` but no API key is in the environment and no stored OAuth token was found.

Fix one of these:

```bash
# Option A: env var (simplest)
export ANTHROPIC_API_KEY=sk-ant-...

# Option B: OAuth via your Claude.ai account
conversus login anthropic
```

Verify with `conversus status`.

### `ProviderError: No credentials available for 'openai'`

Same pattern as Anthropic:

```bash
export OPENAI_API_KEY=sk-...
# or
conversus login openai
```

### `OAuth token expired`

Stored OAuth tokens have a finite lifetime. Re-login:

```bash
conversus logout anthropic && conversus login anthropic
```

If `conversus status` shows "expired" even after a fresh login, your system clock may be wrong — OAuth validation checks `exp` against the local time.

### `Invalid value for '--provider': 'X' is not one of …`

You passed a provider name the CLI doesn't recognize. Run `conversus decide --help` to see the full accepted list. The CLI supports all 13 registered execution providers plus `demo` (an alias for `mock`) plus `openai` (OAuth/API-key).

If you specifically need a provider that doesn't appear (rare), check that your conversus install is current — providers are added periodically.

### `Provider not configured` from `conversus status` even though I set the env var

`conversus status` shows what's configured *for OAuth-style providers* (anthropic, openai). It doesn't probe arbitrary env vars. As long as `$ANTHROPIC_API_KEY` or `$OPENAI_API_KEY` is set in the shell where you run `conversus`, the provider will resolve at run time even if `status` says "not configured."

### `ollama` provider fails with connection refused

The Ollama server isn't running, or it's on a non-default port:

```bash
ollama serve            # start the server
ollama pull qwen3:0.6b  # pull the model your config references
```

Set `OLLAMA_BASE_URL` if your server runs on a non-default host/port.

## Config errors

### `target file not found` but the file is right there

`target:` uses a two-pass resolution: it tries the path relative to the **config file's directory** first, then falls back to your **current working directory**. So `target: README.md` from a config in `examples/` works two ways: it finds `examples/README.md` if that exists, otherwise it falls back to `<cwd>/README.md`.

If neither pass finds it, the error names both paths tried — pick the one that matches your intent and put the file there (or use an absolute path).

### `arbiter.grounding path does not exist`

Same two-pass rule as `target:` — tries config-dir-relative first, falls back to cwd-relative. The error message names both paths. If your grounding doc lives at the project root and your config is in a subdirectory, run from project root and the cwd-fallback will find it.

### Output landed at `examples/examples/output/foo/` instead of `examples/output/foo/`

`output:` is different from `target:` and `grounding:` — it's a **write target** with no fallback, because the directory doesn't have to exist yet. The engine always anchors it relative to the config file's directory. If your config is at `examples/foo.yml` and you set `output: examples/output/foo/`, the engine produces `examples/examples/output/foo/` (the config-dir prefix is added on top of your value).

Fix: use a path relative to the config file's parent dir, or use an absolute path:

```yaml
# In examples/foo.yml
output: output/foo/         # → examples/output/foo/
output: /tmp/out/foo/       # → /tmp/out/foo/ (absolute, no prefix added)
```

The resolution rules are summarized in [Config Reference → Path resolution](config-reference.md#path-resolution).

### `Unknown provider 'X'` from MCP

The MCP server's `--provider` allowlist is intentionally narrower than the CLI's — only `mock`, `demo`, `anthropic`, `openai`, and `claude-desktop` are accepted via MCP. Subprocess-based providers (ollama, claude-code, aider, etc.) would launch and then fail deep in a subprocess from the MCP context, so they're rejected up-front. Use the CLI directly for those.

## Cost & rate limits

### `Rate limit exceeded` from Anthropic / OpenAI

Each deliberation issues a burst of parallel agent calls (one per agent per phase). For 3 agents in cooperative mode, that's ~13 calls in seconds. The simplest mitigations:

1. Switch to `--provider claude-code` (uses your Claude.ai subscription, not API tokens)
2. Reduce agent count from 3 → 2 (the cost-per-agent scales as N + N(N-1) + N + N + 1 — see CLI Reference cost-estimate output)
3. Run mock-first to validate the config: `conversus run config.yml --provider mock`
4. Add a small `iterations` cap if your config sets it higher than 1

### How do I know what a deliberation will cost?

Before any LLM call:

```bash
conversus validate config.yml
```

The cost-estimate breakdown shows total launches and per-phase counts. Multiply by your provider's per-call price; the LLM model determines the price point.

### How do I cancel a running deliberation?

`Ctrl-C` in the terminal sends SIGINT. Currently-running agent dispatches will complete (you'll see the LLM call finish even after the interrupt), then the pipeline stops without writing further phases. Already-written phase outputs (`review.md`, `cross-reviews/*.md`, etc.) are kept — you can inspect them or resume planning from there.

If a dispatch is hung waiting on a network call, `Ctrl-C` may take a few seconds to take effect. A second `Ctrl-C` is harder kill.

## MCP & editor integration

### `conversus mcp` exits immediately

The MCP server uses stdio transport — it doesn't run unless something connects. To test it works at all:

```bash
conversus mcp --help  # exits 0 if the entry point is wired correctly
```

To actually use it, register it with your editor:

```bash
claude mcp add conversus -- conversus mcp     # Claude Code
```

For Cursor / Windsurf / other MCP clients, see [MCP Setup](mcp-setup.md).

### Claude Code says "MCP server not found"

The CLI entry point isn't on PATH. Either install conversus with pip (so `conversus` becomes available globally) or wire the full path into the MCP registration:

```bash
claude mcp add conversus -- /full/path/to/conversus mcp
```

### Tools missing from Claude Desktop after `.mcpb` install

Restart Claude Desktop. Extensions load at startup; a freshly-installed `.mcpb` may not take effect until the app is closed and reopened.

## Output & artifacts

### Where do deliberation outputs go?

`conversus init` creates `.conversus/deliberations/` for project-scoped runs. `conversus decide` writes to a temp directory unless you pass `--output ./somewhere/`. `conversus run` writes to the path in the config's `output:` field (see path-resolution note above).

### How do I read the output?

After a run completes:

| File | What it contains |
|---|---|
| `summary/final.md` | Synthesizer's verdict — start here |
| `<agent>/review.md` | Each agent's initial position (Phase 1) |
| `<agent>/cross-reviews/<other>.md` | Pairwise critiques (Phase 2) |
| `<agent>/revision.md` | Each agent's revised position (Phase 3) |
| `<agent>/disputes.md` | Unresolved disagreements (Phase 4) |
| `arbitration/resolution.md` | Arbiter's binding ruling (Phase 6 — only when arbiter is configured) |

### Can I re-run a deliberation against the same output dir?

Yes, but be aware: the engine **overwrites** files in the output dir. If you want to preserve a prior run, copy or rename the directory first.

## Debugging the deliberation itself

### Agents agreed too easily — no disputes surfaced

Two common causes:

1. **Agent prompts are too similar.** If two agents have overlapping incentives, they'll converge prematurely. Differentiate the *what-they-lose-if-wrong* axis, not just the job title.
2. **The mode forces convergence.** `cooperative` mode emphasizes synthesis; `red-blue` and `winner-take-all` force position-taking. For stress-tests, prefer adversarial modes.

### Agent output is generic/empty

Usually a sign the provider returned a refusal or hit a content filter. Check the per-agent file for the actual model output — refusals often look like polished but content-free prose.

### `conversus decide` always returns the same verdict

`decide` uses fixed pragmatist + devil's-advocate presets and a synthesizer. For the same question + same mode + same provider, you'll get **deterministic-ish** output (LLMs aren't fully deterministic but they're close at temperature 0). To get genuinely different results, change agents or mode — use `conversus run config.yml` with custom agents instead of `decide`.

## Still stuck?

- Open an issue: [github.com/Build-Fractal/conversus-oss/issues](https://github.com/Build-Fractal/conversus-oss/issues)
- Read the [first deliberation walkthrough](first-deliberation.md) to see what a healthy run looks like
- Check [CONTRIBUTING.md](https://github.com/Build-Fractal/conversus-oss/blob/main/CONTRIBUTING.md) for how to report a reproducible bug
