# Structured review: token benchmark

**Date:** 2026-11-07. **Target:** this repo's `install.sh` (189 lines). **Model:** `haiku` through
the Claude Code CLI (`claude` 2.1.319), three reviewers (correctness, risk, clarity), one run
each. Usage is what the CLI reports per call (`total_cost_usd`, input including cache reads,
output including thinking). Raw runs are kept in `~/code/scratch/deliberator-review-bench/`.

| Run | Calls | Input tokens | Output tokens | Cost | Wall time |
|---|---|---|---|---|---|
| Existing pipeline (`run`, cooperative, 1 iteration) | 16 | 1,377,669 | 228,333 | $0.439 | 8 min 23 s |
| `deliberator review`, default CLI calls | 9 | 404,952 | 40,635 | $0.079 | 1 min 56 s |
| `deliberator review`, lean CLI calls | 10 | 43,538 | 31,288 | $0.024 | 1 min 21 s |
| `deliberator review`, lean, `--effort low` (the default) | 10 | 44,022 | 16,272 | $0.017 | about 1 min 20 s |

Against the existing pipeline, the default `review` uses **31× fewer input tokens, 14× fewer
output tokens, and costs 26× less**.

## Where the savings come from

1. **Protocol: fewer calls, each seeing less.**
   - The existing pipeline makes N reviews + N(N−1) pairwise cross-reviews + N revisions + N
     disputes + 1 synthesis, and inlines whole prior files into each call. Synthesis gets every
     review, cross-review, revision and dispute.
   - The review protocol makes N reviews + N challenges + at most N responses + at most one
     arbitration.
   - Later phases see one line per item, and only the items they act on.
   - Nothing is synthesised by a model: the verdict is computed from the argument graph.
2. **Lean CLI calls (`ClaudeCodeProvider(lean=True)`).** A default `claude -p` call carries the
   CLI's own system prompt, tool definitions, MCP servers and skills list: about 39,000 input
   tokens before the prompt. Lean calls drop all of these with `--tools "" --strict-mcp-config
   --disable-slash-commands --setting-sources ""`, a one-line system prompt and an empty working
   directory. They measured about 690 tokens of overhead. In the table, this is the gap between
   rows 2 and 3.
3. **`--effort low`.** On haiku the CLI thinks by default, and thinking is billed as output. In
   row 3 the visible replies were about 2,100 tokens out of 31,288. `--effort low` halved output
   (row 4).
4. **Terse JSON replies.**
   - One JSON object per reply, with short text fields (`text_words: 25` in
     `schema/protocols/review.yml`).
   - A cached shared prefix: every call starts with the same instructions and target.

**Separating 1 from 2.** The existing pipeline ran with default CLI calls. At about 39,000
overhead tokens × 16 calls ≈ 620,000, lean calls alone would bring it to roughly 750,000 input
tokens. That's an estimate, not a run. The protocol accounts for the remaining ~17×.

## What this does not show

- **Quality.** It's not compared. The review runs produced 10–14 distinct standing findings on
  `install.sh`, and spot checks found them real: SSH choice computed but ignored, `--extras`
  dropped for local installs, SIGPIPE under `pipefail`, `curl | bash` stdin consumption. A
  quality comparison against the existing pipeline's output still needs doing.
- **Run-to-run variance.** One run per row.
- **Agreeable reviewers.** In the first run every objection was answered with *withdraw* or
  *revise*, and none was defended. The respond prompt now says to defend when the evidence
  supports it. In the later runs arbitration was needed and ran.
- **API providers.** `anthropic` and `openai` honour `max_tokens`. The CLI does not, so the
  per-phase caps in the protocol bind only on API providers.
