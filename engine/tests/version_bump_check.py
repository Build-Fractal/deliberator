"""Schema version-bump detection — spec § 5.4 D15, Principle XXVIII sub-clause 3.

When a PR edits anything under ``engine/schema/v1/``, this script asserts that
at least one of the following is true:

1. The envelope's ``schema_version`` pattern/enum has bumped (visible in the
   diff between base and head of the envelope schema).
2. Any body schema's ``$id`` declares a new version path component.
3. The PR description contains the literal token ``[schema:no-bump-justified]``
   with a free-form rationale on the same line.

If none of (1), (2), or (3) hold, the schema edit is a silent format change —
a Principle XXVIII sub-clause 3 violation. Exit code 1 blocks the merge.

Invocation by CI (per spec § 5.4)::

    python -m engine.tests.version_bump_check \\
        --base-ref <base-sha> \\
        --head-ref <head-sha> \\
        --pr-body "$PR_BODY"
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

_NO_BUMP_TOKEN = "[schema:no-bump-justified]"
_SCHEMA_DIR = "engine/schema/v1"


def _git_show(ref: str, path: str, cwd: Path | None = None) -> str | None:
    """Return the contents of `path` at `ref`, or None if the path didn't exist."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def _envelope_version_signature(text: str) -> str:
    """Project the envelope schema's schema_version field down to a stable signature.

    The signature is the JSON-encoded value of the `schema_version` property's
    ``const``, ``enum``, or ``pattern`` declaration (whichever is set). A change
    in any of these is a version bump for our purposes.
    """
    try:
        schema = json.loads(text)
    except json.JSONDecodeError:
        return "<unparseable>"
    sv = schema.get("properties", {}).get("schema_version", {})
    return json.dumps(
        {
            "const": sv.get("const"),
            "enum": sv.get("enum"),
            "pattern": sv.get("pattern"),
        },
        sort_keys=True,
    )


def _changed_schema_files(base_ref: str, head_ref: str, cwd: Path | None = None) -> list[str]:
    """Return the list of files under engine/schema/v1/ that differ base..head."""
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}..{head_ref}", "--", _SCHEMA_DIR],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def _id_versions(text: str) -> set[str]:
    """Extract any '/v\\d+/' path component from a schema's `$id` field."""
    try:
        schema = json.loads(text)
    except json.JSONDecodeError:
        return set()
    schema_id = schema.get("$id")
    if not isinstance(schema_id, str):
        return set()
    return set(re.findall(r"/(v\d+)/", schema_id))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m engine.tests.version_bump_check")
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", required=True)
    parser.add_argument("--pr-body", default="", help="Full PR description body.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    repo_root: Path = args.repo_root.resolve()

    changed = _changed_schema_files(args.base_ref, args.head_ref, cwd=repo_root)
    if not changed:
        print("version-bump-check: no schema files changed; pass.")
        return 0

    # Signal 1 — envelope schema_version pattern/enum/const changed.
    envelope_path = f"{_SCHEMA_DIR}/envelope.schema.json"
    base_envelope = _git_show(args.base_ref, envelope_path, cwd=repo_root)
    head_envelope = _git_show(args.head_ref, envelope_path, cwd=repo_root)
    envelope_bumped = False
    if base_envelope is not None and head_envelope is not None:
        envelope_bumped = (
            _envelope_version_signature(base_envelope)
            != _envelope_version_signature(head_envelope)
        )

    # Signal 2 — any schema's $id version path component changed (e.g., v1 → v2).
    id_bumped = False
    for rel in changed:
        base_text = _git_show(args.base_ref, rel, cwd=repo_root)
        head_text = _git_show(args.head_ref, rel, cwd=repo_root)
        if base_text is None or head_text is None:
            # New or deleted schema file — that itself is a structural change.
            id_bumped = True
            break
        if _id_versions(base_text) != _id_versions(head_text):
            id_bumped = True
            break

    # Signal 3 — PR-body opt-out token.
    no_bump_justified = _NO_BUMP_TOKEN in args.pr_body

    if envelope_bumped or id_bumped or no_bump_justified:
        signals: list[str] = []
        if envelope_bumped:
            signals.append("envelope.schema_version changed")
        if id_bumped:
            signals.append("$id version path changed (or schema added/removed)")
        if no_bump_justified:
            signals.append(f"{_NO_BUMP_TOKEN} present in PR body")
        print(f"version-bump-check: {len(changed)} schema file(s) changed; bump signal(s): "
              f"{', '.join(signals)}.")
        return 0

    print(
        f"version-bump-check: {len(changed)} schema file(s) changed but no version-bump "
        "signal detected.",
        file=sys.stderr,
    )
    print(
        "Per Principle XXVIII sub-clause 3, schema edits MUST carry one of:\n"
        "  - envelope schema_version pattern/enum/const change\n"
        "  - $id version-path change (e.g., v1/ → v2/)\n"
        f"  - {_NO_BUMP_TOKEN} <rationale> in the PR description",
        file=sys.stderr,
    )
    print("\nChanged schema files:", file=sys.stderr)
    for rel in changed:
        print(f"  {rel}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
