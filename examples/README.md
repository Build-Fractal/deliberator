# Examples

Four working configs you can copy-paste and run with `--provider mock` (no API key, no install beyond deliberator itself). Each demonstrates a distinct deliberation pattern.

| File | Mode | Pattern | Cost (mock) |
|---|---|---|---|
| [`doc-review-cooperative.yml`](doc-review-cooperative.yml) | `cooperative` | Three reviewers with different incentives evaluate a target document. Synthesis emphasizes convergence. | ~16 launches |
| [`architecture-red-blue.yml`](architecture-red-blue.yml) | `red-blue` | Adversarial — one agent attacks, one defends. Forces weak arguments into the open. | ~9 launches |
| [`with-arbiter.yml`](with-arbiter.yml) | `cooperative` + Phase 6 arbiter | Two reviewers with a binding arbiter that rules when disputes remain. | ~10 launches |
| [`winner-take-all-decision.yml`](winner-take-all-decision.yml) | `winner-take-all` | Three advocates compete for a single recommendation. No hedging — synthesis must pick. | ~16 launches |

## Run from project root

```bash
# Mock — synthetic responses, no API key
deliberator run examples/doc-review-cooperative.yml --provider mock

# Real LLM
export ANTHROPIC_API_KEY=sk-ant-...
deliberator run examples/doc-review-cooperative.yml --provider anthropic
```

Output lands in `examples/output/<example-name>/`. The directory is git-ignored.

## What to read in the output

After a run completes, look at:

- `summary/final.md` — the synthesizer's verdict
- `<agent>/review.md` — each agent's initial position (Phase 1)
- `<agent>/cross-reviews/<other-agent>.md` — pairwise critiques (Phase 2)
- `<agent>/revision.md` — each agent's response to cross-reviews (Phase 3)
- `<agent>/disputes.md` — unresolved disagreements (Phase 4)
- `arbitration/resolution.md` — present only when an arbiter is configured

## Modify before you ship

These are copy-paste starting points, not production configs. To adapt:

1. Change `target:` to the file(s) you want agents to read.
2. Rewrite each agent's `prompt` so each role has a genuinely different incentive — *what does this agent lose if they're wrong?* If you can't answer that for two agents, collapse them into one.
3. Pick a `mode` that matches your decision type — see [docs/user-guide/modes.md](../docs/user-guide/modes.md).
4. Validate first: `deliberator validate <your-config.yml>` prints the cost estimate before any LLM call.

## Note on `output:` and `arbiter.grounding:` paths

These paths resolve relative to the **config file's directory**, not the cwd you invoke from. The examples above use `output: output/<name>/` (which becomes `examples/output/<name>/`) and `grounding: ../CHANGELOG.md` (which resolves to the project-root `CHANGELOG.md`) for that reason. Your own configs should follow the same convention.

`target:` resolution is currently inconsistent — it appears to resolve relative to cwd. If you hit a "target file not found" error, try the path relative to where you're invoking the CLI.
