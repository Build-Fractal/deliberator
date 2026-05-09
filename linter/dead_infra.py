"""Dead-infrastructure linter — Tier 2 Principle XII enforcement.

Catches the inverse direction of `linter/validate.py`:

- `validate.py` flags templates that reference variables not in the schema.
- `dead_infra.py` flags variables defined in the schema that no template
  references — the "fully defined, fully typed, fully dead" pattern from
  spec 006 (origin of Principle XII).

Per Principle XII, every provisioned capability must have at least one
consumer. A schema variable with declared `phases:` but zero matching
template references across all applicable modes is dead infrastructure.

Variables consumed only by orchestrator code (not by template text) are
exempt when they declare a `consumer:` annotation naming the consumer.
This forces explicit attribution — unattributed future-proofing fails.

Run:
    uv run python -m linter.dead_infra            # all modes
    uv run python -m linter.dead_infra --verbose  # show per-variable resolution

Exit codes:
    0 = no dead variables.
    1 = one or more dead variables found.
    2 = configuration error (missing files, malformed schema).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import click
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "variables.yml"
TEMPLATES_DIR = ROOT / "templates"

VAR_PATTERN = re.compile(r"\{([A-Z_][A-Z0-9_]*)\}")

ALL_MODES = {
    "cooperative",
    "red-blue",
    "winner-take-all",
    "prisoners-dilemma",
    "fair-division",
    "mechanism-design",
    "negotiation",
    "resource-allocation",
}

PHASE_TO_TEMPLATE = {
    "review": "review.md",
    "cross-review": "cross-review.md",
    "revision": "revision.md",
    "disputes": "disputes.md",
    "synthesis": "synthesis.md",
    "arbitration": "arbitration.md",
    "cross-round-synthesis": "cross-round-synthesis.md",
}


@dataclass(frozen=True)
class DeadVariable:
    name: str
    phases: tuple[str, ...]
    modes_searched: tuple[str, ...]
    consumer_annotation: str | None

    def reason(self) -> str:
        if self.consumer_annotation is None:
            return (
                f"variable defined for phases {list(self.phases)} but appears in "
                f"zero matching templates and has no `consumer:` annotation"
            )
        return (
            f"variable claims consumer '{self.consumer_annotation}' but no "
            f"template references it — annotation may be stale"
        )


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"schema not found at {SCHEMA_PATH}")
    return yaml.safe_load(SCHEMA_PATH.read_text())


def collect_template_variables(modes: set[str]) -> dict[tuple[str, str], frozenset[str]]:
    """Return {(mode, phase): {variable_names}} for every template under `modes`."""
    out: dict[tuple[str, str], frozenset[str]] = {}
    for mode in sorted(modes):
        mode_dir = TEMPLATES_DIR / mode
        if not mode_dir.is_dir():
            continue
        for phase, fname in PHASE_TO_TEMPLATE.items():
            tpl = mode_dir / fname
            if not tpl.is_file():
                continue
            text = tpl.read_text()
            out[(mode, phase)] = frozenset(VAR_PATTERN.findall(text))
    return out


def find_dead_variables(
    schema: dict,
    template_vars: dict[tuple[str, str], frozenset[str]],
    verbose: bool,
) -> list[DeadVariable]:
    dead: list[DeadVariable] = []
    variables = schema.get("variables", {}) or {}

    for var_name, var_def in variables.items():
        phases = tuple(var_def.get("phases", []) or [])
        modes_field = var_def.get("modes")
        consumer = var_def.get("consumer")

        if not phases:
            continue

        applicable_modes = set(modes_field) if modes_field else set(ALL_MODES)
        # Find templates we should check
        searched: list[str] = []
        found = False
        for (mode, phase), vars_in_template in template_vars.items():
            if phase not in phases or mode not in applicable_modes:
                continue
            searched.append(f"{mode}/{phase}")
            if var_name in vars_in_template:
                found = True
                if not verbose:
                    break

        if found:
            if verbose:
                click.echo(f"  ✓ {var_name}: referenced in templates")
            continue

        if consumer is not None:
            if verbose:
                click.echo(
                    f"  ~ {var_name}: no template ref, consumer='{consumer}' (orchestrator-only)"
                )
            continue

        dead.append(
            DeadVariable(
                name=var_name,
                phases=phases,
                modes_searched=tuple(sorted(set(applicable_modes))),
                consumer_annotation=consumer,
            )
        )
    return dead


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Show per-variable resolution.")
def main(verbose: bool) -> None:
    """Validate that every schema variable has at least one consumer."""
    try:
        schema = load_schema()
    except FileNotFoundError as e:
        click.echo(f"ERROR: {e}", err=True)
        sys.exit(2)

    template_vars = collect_template_variables(ALL_MODES)
    if not template_vars:
        click.echo(f"ERROR: no templates found under {TEMPLATES_DIR}", err=True)
        sys.exit(2)

    if verbose:
        click.echo(
            f"Scanning {len(schema.get('variables', {}))} variables against "
            f"{len(template_vars)} (mode, phase) template pairs..."
        )

    dead = find_dead_variables(schema, template_vars, verbose)

    if not dead:
        click.echo("✓ No dead variables — every schema variable has a consumer.")
        sys.exit(0)

    click.echo(f"\n✗ Found {len(dead)} dead variable(s):", err=True)
    for d in dead:
        click.echo(f"  - {d.name}: {d.reason()}", err=True)
    click.echo(
        "\nFix: either reference the variable in a template for its declared "
        "phases, or add a `consumer: <name>` field to the schema entry "
        "documenting which orchestrator code populates/reads it.",
        err=True,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
