# Eval baselines (spec 061 step 8)

This directory stores **baseline snapshots** for the deepeval quality suite in
`engine/tests/test_evals.py`. Each snapshot file records per-metric scores
from a real provider run and a calibrated threshold table the test suite
loads at module import time.

## Why baselines exist

Spec 061 §3.2.1 lists five quality metrics with starter thresholds (0.7 /
0.7 / 0.6 / 0.7 / 0.8). Those numbers are guesses. Step 8 closes the loop:
run the suite once with a real provider, observe what scores the pipeline
actually produces, then calibrate each threshold to `min - 0.1` so the
recalibrated suite cannot regress on a known-good run.

Without a baseline file the suite falls back to spec defaults — a fresh
checkout still works, but the thresholds are not yet evidence-backed.

## File format

Files are named `<UTC-timestamp>.json` (`YYYYMMDDTHHMMSS.json`). Lex sort
matches chronological sort, so the test suite resolves "the latest baseline"
by sorting filenames.

```json
{
  "captured_at": "2026-05-01T20:00:00Z",
  "judge": {"provider": "anthropic", "model": "claude-sonnet-4-20250514"},
  "deliberation_provider": "claude-code",
  "snapshots": [
    {
      "question_slug": "postgres-vs-mongodb",
      "mode": "cooperative",
      "agents": ["alice", "bob"],
      "scores": {
        "review_independence": 0.85,
        "cross_review_adversarial": 0.72,
        "revision_responsiveness": 0.65,
        "dispute_specificity": 0.78,
        "synthesis_grounding": 0.91
      }
    }
  ],
  "calibrated_thresholds": {
    "review_independence": 0.75,
    "cross_review_adversarial": 0.62,
    "revision_responsiveness": 0.55,
    "dispute_specificity": 0.68,
    "synthesis_grounding": 0.81
  }
}
```

## Calibration math

For each metric:

```
calibrated_thresholds[metric] = max(0.0, min(score across snapshots) - 0.1)
```

That is: take the worst observed score for the metric across every captured
snapshot, subtract a 0.1 margin, and clamp at zero. Subtracting from the
*minimum* (not the mean) guarantees every captured deliberation would still
pass the calibrated threshold — a recalibrated suite cannot regress on a
known-good run. The 0.1 margin matches spec 061 §4.2.

A metric with no observations falls back to the spec 061 §3.2.1 default.

## Capturing a baseline

```bash
# Five-question x four-mode default matrix (~20 deliberations + judge calls;
# expect ~100+ paid LLM calls — set credentials before running).
uv run python scripts/capture-eval-baselines.py \
    --output evals/baselines/$(date -u +%Y%m%dT%H%M%S).json

# Subset run (fewer questions / modes) — cheaper smoke calibration.
uv run python scripts/capture-eval-baselines.py \
    --questions "Postgres or MongoDB?" "Build vs buy auth?" \
    --modes cooperative \
    --output evals/baselines/$(date -u +%Y%m%dT%H%M%S).json

# Dry-run — produce a stub file with empty snapshots and spec-default
# thresholds. Useful for testing the file-loading path without paying for
# LLM calls.
uv run python scripts/capture-eval-baselines.py \
    --dry-run \
    --output /tmp/baseline-stub.json
```

The capture script honours `CONVERSUS_EVAL_PROVIDER` (default `claude-code`)
and `CONVERSUS_EVAL_JUDGE_PROVIDER` (default `anthropic`); pass
`--deliberation-provider` / `--judge-provider` / `--judge-model` to override
the defaults explicitly.

## Standard question set

`standard-questions.json` ships the five spec-mandated test questions. The
shapes are intentionally varied to exercise different deliberation patterns:

| Slug | Shape |
|---|---|
| `postgres-vs-mongodb` | binary tech-stack |
| `llm-code-review-readiness` | tech-readiness |
| `formal-verification-adoption` | adoption strategy |
| `monorepo-vs-polyrepo` | organisational topology |
| `public-api-v1-timing` | product timing |

The questions overlap with the `evals/promptfooconfig.yaml` test bank to
keep the smoke and quality tiers comparable.

## When to recapture

Recapture a baseline whenever the pipeline output distribution might shift:

- After major **prompt template** changes (`templates/`).
- After **agent preset** changes (`presets/`).
- After **mode** changes that affect synthesis structure.
- After upgrading the **judge model** (the score scale can drift).
- After adding/removing **metrics** in `engine/tests/test_evals.py`.

A baseline that no longer reflects the current pipeline produces either
false-positive failures (calibrated too tight) or silent quality
regressions (calibrated too loose). When in doubt, recapture.

## File hygiene

Old baselines are not auto-deleted — keep them as a record of how thresholds
have evolved. The test suite always loads only the latest file.
