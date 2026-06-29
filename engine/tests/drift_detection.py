"""Bidirectional drift detection — spec § 5.4 D12, Principle XXVIII sub-clause 2.

When a PR changes anything under ``engine/schema/v1/``, this script re-validates
the existing deliberations corpus under the **new** schema and compares against
the conformance baseline at the merge base. Any previously-conformant artifact
that becomes non-conformant under the new schema is a drift violation: the
schema edit silently broke a downstream consumer of the wire contract.

Exit codes:
    0 = no drift detected (or no deliberations corpus to compare against).
    1 = at least one previously-conformant artifact failed under the new schema.
    2 = configuration error (missing git context, malformed args).

Invocation by CI (per spec § 5.4)::

    python -m engine.tests.drift_detection --baseline-ref <merge-base-sha>

The script assumes it is run inside the repo (uses git plumbing to checkout the
baseline tree into a scratch area, validates both sides with the same
in-process validator, and diffs the conformance vectors).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from engine.schema_validator import SchemaValidator


_DELIBERATIONS_DIR = Path("deliberations")


def _run_git(*args: str, cwd: Path | None = None) -> str:
    """Run a git command and return stdout. Raises CalledProcessError on failure."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _conformance_vector(root: Path, validator: SchemaValidator) -> dict[str, bool]:
    """Validate every JSON file under `root/deliberations/`; return path → is_conformant.

    Empty/missing corpus returns an empty vector — that is the "nothing to compare"
    case and the caller treats it as no-drift.
    """
    delib_root = root / _DELIBERATIONS_DIR
    if not delib_root.is_dir():
        return {}

    vector: dict[str, bool] = {}
    for path in delib_root.rglob("*.json"):
        if path.name.endswith(".validation-warnings.json"):
            continue
        content = path.read_bytes()
        try:
            envelope = json.loads(content)
        except (json.JSONDecodeError, UnicodeDecodeError):
            vector[str(path.relative_to(root))] = False
            continue
        schema_version = (
            envelope.get("schema_version", "1.0.0-rc.1")
            if isinstance(envelope, dict)
            else "1.0.0-rc.1"
        )
        result = validator.validate(content, schema_version)
        vector[str(path.relative_to(root))] = result.is_conformant
    return vector


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m engine.tests.drift_detection")
    parser.add_argument(
        "--baseline-ref",
        required=True,
        help="git SHA or ref to compare against (typically the PR's merge base).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Path to the deliberator working tree (default: CWD).",
    )
    args = parser.parse_args(argv)

    repo_root: Path = args.repo_root.resolve()

    # HEAD-side conformance vector (current schemas, current corpus).
    schema_dir = repo_root / "engine" / "schema" / "v1"
    try:
        head_validator = SchemaValidator(schema_dir)
    except RuntimeError as exc:
        print(f"drift: HEAD validator construction failed: {exc}", file=sys.stderr)
        return 2
    head_vector = _conformance_vector(repo_root, head_validator)

    if not head_vector:
        print("drift: no deliberations corpus on HEAD — nothing to compare. (pass)")
        return 0

    # Baseline-side conformance vector. We use `git worktree add` to materialize
    # the baseline tree into a scratch directory, then run the SAME validator
    # construction path against the baseline's schemas. This catches drift in
    # both directions: removed schema constraints (file passes baseline, fails
    # HEAD) AND added constraints that retroactively break the corpus.
    with tempfile.TemporaryDirectory(prefix="drift-baseline-") as tmp:
        baseline_root = Path(tmp) / "baseline"
        try:
            _run_git("worktree", "add", "--detach", str(baseline_root), args.baseline_ref, cwd=repo_root)
        except subprocess.CalledProcessError as exc:
            print(f"drift: git worktree add failed: {exc.stderr}", file=sys.stderr)
            return 2

        try:
            try:
                baseline_validator = SchemaValidator(baseline_root / "engine" / "schema" / "v1")
            except RuntimeError as exc:
                print(f"drift: baseline validator construction failed: {exc}", file=sys.stderr)
                return 2
            baseline_vector = _conformance_vector(baseline_root, baseline_validator)
        finally:
            # Always remove the worktree so subsequent CI runs don't trip over it.
            try:
                _run_git("worktree", "remove", "--force", str(baseline_root), cwd=repo_root)
            except subprocess.CalledProcessError:
                pass

    # Drift = file conformant at baseline, non-conformant at HEAD.
    regressions: list[str] = []
    for path, baseline_ok in baseline_vector.items():
        head_ok = head_vector.get(path)
        if baseline_ok and head_ok is False:
            regressions.append(path)

    if regressions:
        print(
            f"\ndrift: {len(regressions)} previously-conformant file(s) now fail under "
            f"the HEAD schema:",
            file=sys.stderr,
        )
        for path in regressions:
            print(f"  {path}", file=sys.stderr)
        print(
            "\nThis is a Principle XXVIII sub-clause 2 violation: a schema edit "
            "silently broke previously-conformant artifacts.",
            file=sys.stderr,
        )
        return 1

    print(f"drift: {len(head_vector)} file(s) checked; no regressions detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
