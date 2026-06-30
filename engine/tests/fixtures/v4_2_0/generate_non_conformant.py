"""Generator for the 18 non-conformant v4.2.0 fixtures (6 output types × 3 modes).

Per spec § 5.3 + Principle XXVIII sub-clause 2, each output type ships:
  - a known-conformant fixture (already present: `{type}.conformant.json`)
  - missing-required (REQUIRED_FIELD_MISSING)
  - wrong-type (TYPE_MISMATCH)
  - enum-violation (ENUM_VIOLATION)

The three non-conformant modes cover XXVIII sub-clause 2's enforcement surface:
field presence, type checking, value-constraint membership.

This generator is the single source of truth for the fixture derivations. Run
it whenever the conformant fixtures change; the non-conformant fixtures are
mechanical derivatives. Each fixture is written with `sort_keys=True, indent=2`
so diffs stay stable across regenerations.

Usage:
    cd deliberator
    uv run python engine/tests/fixtures/v4_2_0/generate_non_conformant.py
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
NON_CONFORMANT_DIR = HERE / "non-conformant"


def _load_conformant(output_type: str) -> dict[str, Any]:
    return json.loads((HERE / f"{output_type}.conformant.json").read_text())


def _write(output_type: str, mode: str, envelope: dict[str, Any]) -> Path:
    NON_CONFORMANT_DIR.mkdir(exist_ok=True)
    out = NON_CONFORMANT_DIR / f"{output_type}.{mode}.json"
    out.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


# ────────────────────────────────────────────────────────────────────────────
# Per-output-type defect injectors
# ────────────────────────────────────────────────────────────────────────────


def _review_missing_required(env: dict[str, Any]) -> dict[str, Any]:
    """REQUIRED_FIELD_MISSING at /body/recommendation."""
    del env["body"]["recommendation"]
    return env


def _review_wrong_type(env: dict[str, Any]) -> dict[str, Any]:
    """TYPE_MISMATCH at /body/strengths — array → string."""
    env["body"]["strengths"] = "not an array of strengths"
    return env


def _review_enum_violation(env: dict[str, Any]) -> dict[str, Any]:
    """ENUM_VIOLATION at /body/recommendation."""
    env["body"]["recommendation"] = "MAYBE"
    return env


def _cross_review_missing_required(env: dict[str, Any]) -> dict[str, Any]:
    """REQUIRED_FIELD_MISSING at /body/reviewing_agent."""
    del env["body"]["reviewing_agent"]
    return env


def _cross_review_wrong_type(env: dict[str, Any]) -> dict[str, Any]:
    """TYPE_MISMATCH at /body/disagreement_points — array → string."""
    env["body"]["disagreement_points"] = "should be array"
    return env


def _cross_review_enum_violation(env: dict[str, Any]) -> dict[str, Any]:
    """ENUM_VIOLATION at /body/disagreement_points/0/stance.

    The disagreement_point items declare `stance: enum [disagree, partial-disagree]`.
    Substitute a value outside the enum.
    """
    if env["body"].get("disagreement_points"):
        env["body"]["disagreement_points"][0]["stance"] = "catastrophic-disagree"
    return env


def _revision_missing_required(env: dict[str, Any]) -> dict[str, Any]:
    """REQUIRED_FIELD_MISSING at /body/iteration."""
    del env["body"]["iteration"]
    return env


def _revision_wrong_type(env: dict[str, Any]) -> dict[str, Any]:
    """TYPE_MISMATCH at /body/iteration — integer → string."""
    env["body"]["iteration"] = "two"
    return env


def _revision_enum_violation(env: dict[str, Any]) -> dict[str, Any]:
    """ENUM_VIOLATION at /body/updated_recommendation."""
    env["body"]["updated_recommendation"] = "MAYBE"
    return env


def _disputes_missing_required(env: dict[str, Any]) -> dict[str, Any]:
    """REQUIRED_FIELD_MISSING at /body/disputes."""
    del env["body"]["disputes"]
    return env


def _disputes_wrong_type(env: dict[str, Any]) -> dict[str, Any]:
    """TYPE_MISMATCH at /body/disputes — array → string."""
    env["body"]["disputes"] = "should be array"
    return env


def _disputes_enum_violation(env: dict[str, Any]) -> dict[str, Any]:
    """ENUM_VIOLATION at /body/disputes/0/severity."""
    if env["body"].get("disputes"):
        env["body"]["disputes"][0]["severity"] = "nit"
    return env


def _synthesis_missing_required(env: dict[str, Any]) -> dict[str, Any]:
    """REQUIRED_FIELD_MISSING at /body/recommendation_to_arbiter."""
    del env["body"]["recommendation_to_arbiter"]
    return env


def _synthesis_wrong_type(env: dict[str, Any]) -> dict[str, Any]:
    """TYPE_MISMATCH at /body/disputes — array → string."""
    env["body"]["disputes"] = "should be array"
    return env


def _synthesis_enum_violation(env: dict[str, Any]) -> dict[str, Any]:
    """ENUM_VIOLATION at /body/disputes/0/severity."""
    if env["body"].get("disputes"):
        env["body"]["disputes"][0]["severity"] = "trivial"
    return env


def _arbitration_missing_required(env: dict[str, Any]) -> dict[str, Any]:
    """REQUIRED_FIELD_MISSING at /body/per_question_rulings."""
    del env["body"]["per_question_rulings"]
    return env


def _arbitration_wrong_type(env: dict[str, Any]) -> dict[str, Any]:
    """TYPE_MISMATCH at /body/per_question_rulings — array → string."""
    env["body"]["per_question_rulings"] = "should be array"
    return env


def _arbitration_enum_violation(env: dict[str, Any]) -> dict[str, Any]:
    """ENUM_VIOLATION at /body/combined_disposition."""
    env["body"]["combined_disposition"] = "YOLO"
    return env


# ────────────────────────────────────────────────────────────────────────────
# Registry
# ────────────────────────────────────────────────────────────────────────────

Mutator = Callable[[dict[str, Any]], dict[str, Any]]

DEFECTS: dict[str, dict[str, Mutator]] = {
    "review": {
        "missing-required": _review_missing_required,
        "wrong-type": _review_wrong_type,
        "enum-violation": _review_enum_violation,
    },
    "cross-review": {
        "missing-required": _cross_review_missing_required,
        "wrong-type": _cross_review_wrong_type,
        "enum-violation": _cross_review_enum_violation,
    },
    "revision": {
        "missing-required": _revision_missing_required,
        "wrong-type": _revision_wrong_type,
        "enum-violation": _revision_enum_violation,
    },
    "disputes": {
        "missing-required": _disputes_missing_required,
        "wrong-type": _disputes_wrong_type,
        "enum-violation": _disputes_enum_violation,
    },
    "synthesis": {
        "missing-required": _synthesis_missing_required,
        "wrong-type": _synthesis_wrong_type,
        "enum-violation": _synthesis_enum_violation,
    },
    "arbitration": {
        "missing-required": _arbitration_missing_required,
        "wrong-type": _arbitration_wrong_type,
        "enum-violation": _arbitration_enum_violation,
    },
}


def regenerate_all() -> list[Path]:
    """Regenerate every non-conformant fixture. Returns the list of written paths."""
    written: list[Path] = []
    for output_type, modes in DEFECTS.items():
        baseline = _load_conformant(output_type)
        for mode, mutator in modes.items():
            mutated = mutator(copy.deepcopy(baseline))
            written.append(_write(output_type, mode, mutated))
    return written


if __name__ == "__main__":
    paths = regenerate_all()
    for p in paths:
        print(f"wrote {p.relative_to(HERE.parents[2])}")
    print(f"\n{len(paths)} non-conformant fixtures generated")
