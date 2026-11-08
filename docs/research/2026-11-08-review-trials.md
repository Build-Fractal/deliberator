# Structured review: five trials on one file

**Date:** 2026-11-08. **Target:** `install.sh` (189 lines), as in the
[token benchmark](2026-11-07-review-token-benchmark.md). **Setup:** `deliberator review
--provider claude-code --model haiku --repeat 5` (lean calls, `--effort low`, three reviewers,
arbiter). **Analysis:** `deliberator trials`. Raw runs: `~/code/scratch/deliberator-review-bench/trials/`.

## Cost and spread

| | Per run (range) | Five runs |
|---|---|---|
| Calls | 9–10 | 47 |
| Input tokens | 38,936–43,335 | 203,818 |
| Output tokens | 14,606–17,556 | 80,554 |
| Cost | $0.013–$0.016 | $0.072 |
| Verdict | changes, all five | |
| Unparsed replies | 0–2.1% | |

Token use stayed within ±6% of the median, so no run was out of the token bounds.

## What the trials say about the findings

Matching findings across runs gave 30 issues:

| Stability | Issues | Meaning |
|---|---|---|
| Stable (stood in ≥ 4 of 5 runs) | 5 | the review reliably finds these |
| Unstable (2–3 of 5) | 10 | found about half the time |
| Noise (≤ 1 of 5) | 15 | one run's view |

The stable five are the real bugs the spot check found on 2026-11-07:
- `--extras` is ignored for local and from-source installs.
- `curl | bash` runs unpinned code from `main`.
- The SSH choice is computed but never used.
- A flag given without a value aborts under `set -u`.
- The Python version check is ambiguous.

The SIGPIPE bug (`--help | head -5` under `pipefail`) stood in 3 of 5 runs, so a single run
misses it 40% of the time. That is the main argument for trials: **one run's finding list is a
sample, and a single review would have reported 11–18 findings of which only 5 are reliable.**

No run was out of bounds: all verdicts agreed (residual 0), no run missed most stable issues,
and no run's serious findings were mostly its own.

## Matching had to be tuned on this data

The first matcher compared exact words and allowed one finding per run per issue. On these runs
it split the SSH bug into four issues and `--extras` into five, because reviewers word the same
bug differently and two reviewers in one run often report it twice. Every run then looked like
it alone had raised serious issues, and **all five were flagged out of bounds: a false alarm
caused by the matcher.**

What fixed it:
- **Word stems** (first five letters): "silently"/"silent" and "ignored"/"ignores" now meet.
- **Every line a location names** (`144-152`, `145,152,161`, a bare `123`), not only `name:N`.
- **Several findings per run in one issue**, with the run counted once.
- **Average-link clustering,** so a chain of loosely similar findings can't merge unrelated
  issues.
- **A line bonus of 0.3, only when at least 15% of stems overlap.** A bonus of 0.5 merged the
  SSH and `--extras` bugs, which point at the same lines.

The thresholds are tuned on one file. They should be checked on other targets before anyone
relies on `--gate`.

## The lone-finding rule

The first rule flagged any run that alone raised a serious issue. Every reviewer turns up
something the others missed, so that flags normal runs. The rule now flags a run only when at
least two of its serious standing findings, and more than half of them, appear in no other run.

## Not tested here

- **Dependency constraints** (`--link`, the isotonic fit across subjects) are covered by unit
  tests only; these trials had one subject.
- **Different configs or models** on the same subject (`SAME_TARGET` across configs).
- **Quality against the existing pipeline's output.**
