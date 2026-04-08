#!/usr/bin/env python3
"""
Conversus Template Linter

Validates templates/{mode}/*.md against schema/variables.yml and schema/modes/{mode}.yml.
Catches missing variables, unknown variables, heading mismatches, and missing structural
markers at development time — before any agent is launched.

Usage:
    uv run python linter/validate.py                    # validate all templates
    uv run python linter/validate.py --mode red-blue    # validate one mode only
    uv run python linter/validate.py --verbose          # show per-file details
"""

import re
import sys
from difflib import get_close_matches
from pathlib import Path
from typing import Optional

import click
import yaml

try:
    from .models import (
        VALID_PHASES,
        ErrorType,
        LintError,
        ModeSchema,
        Phase,
        VariableDefinition,
        VariablesSchema,
    )
except ImportError:
    from models import (
        VALID_PHASES,
        ErrorType,
        LintError,
        ModeSchema,
        Phase,
        VariableDefinition,
        VariablesSchema,
    )

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class SchemaLoadError(Exception):
    """Raised when a schema file cannot be found or loaded."""
    pass


# ---------------------------------------------------------------------------
# Programmatic API models
# ---------------------------------------------------------------------------

class ValidationConfig(BaseModel):
    """Configuration for programmatic template validation.

    Downstream specs (particularly spec 007) may extend this model
    with plugin-aware configuration fields.
    """
    root: Path
    mode: Optional[str] = None


class ValidationResult(BaseModel):
    """Result of template validation."""
    errors: list[LintError]
    files_checked: int

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


# ---------------------------------------------------------------------------
# Schema loading — pure functions returning typed models
# ---------------------------------------------------------------------------

def find_project_root() -> Path:
    """Locate the conversus root (contains schema/ and templates/).

    Strategy:
      1. ``importlib.resources`` — when pip-installed, schema/ and templates/
         are bundled inside the ``conversus`` package.
      2. Walk up from this script (dev source tree).
      3. Fall back to cwd.

    Raises:
        SchemaLoadError: If the conversus root cannot be located.
    """
    # Strategy 1: importlib.resources (pip-installed)
    try:
        from conversus.paths import resolve_package_path

        schema_dir = resolve_package_path("conversus", "schema")
        templates_dir = resolve_package_path("conversus", "templates")
        if schema_dir.is_dir() and templates_dir.is_dir():
            # Both resolved — return their common parent
            return schema_dir.parent
    except (ImportError, FileNotFoundError):
        pass

    # Strategy 2: walk up from this file (dev source tree)
    candidate: Path = Path(__file__).resolve().parent.parent
    if (candidate / "schema").is_dir() and (candidate / "templates").is_dir():
        return candidate

    # Strategy 3: cwd fallback
    cwd: Path = Path.cwd()
    if (cwd / "schema").is_dir() and (cwd / "templates").is_dir():
        return cwd

    raise SchemaLoadError(
        "Error: cannot locate conversus root (schema/ + templates/). "
        "Run from the conversus directory or ensure linter/ is inside it."
    )


def load_variables_schema(root: Path) -> VariablesSchema:
    """Load schema/variables.yml into a typed VariablesSchema model.

    Raises:
        SchemaLoadError: If the schema file is not found.
    """
    path: Path = root / "schema" / "variables.yml"
    if not path.exists():
        raise SchemaLoadError(f"Error: schema file not found: {path}")
    with open(path) as f:
        raw: dict = yaml.safe_load(f)
    return VariablesSchema.model_validate(raw)


def load_mode_schema(root: Path, mode: str) -> ModeSchema:
    """Load schema/modes/{mode}.yml into a typed ModeSchema model.

    Raises:
        SchemaLoadError: If the mode schema file is not found.
    """
    path: Path = root / "schema" / "modes" / f"{mode}.yml"
    if not path.exists():
        raise SchemaLoadError(f"Error: mode schema not found: {path}")
    with open(path) as f:
        raw: dict = yaml.safe_load(f)
    return ModeSchema.model_validate(raw)


# ---------------------------------------------------------------------------
# Template scanning — pure functions
# ---------------------------------------------------------------------------

# Matches {UPPER_CASE_VARS} but not markdown headings or other brace uses
VAR_PATTERN: re.Pattern[str] = re.compile(r"\{([A-Z][A-Z_0-9]+)\}")

# Structural markers
DISPUTES_BEGIN: str = "CONVERSUS:DISPUTES_BEGIN"
DISPUTES_END: str = "CONVERSUS:DISPUTES_END"


def extract_variables(content: str) -> frozenset[str]:
    """Extract all {VARIABLE} references from template content."""
    return frozenset(VAR_PATTERN.findall(content))


def extract_headings(content: str) -> list[str]:
    """Extract markdown heading text (strip # prefix and whitespace)."""
    return [
        line.strip().lstrip("#").strip()
        for line in content.splitlines()
        if line.strip().startswith("#")
    ]


def has_structural_marker(content: str, marker: str) -> bool:
    """Check if content contains a structural marker comment."""
    return marker in content


# ---------------------------------------------------------------------------
# Validation logic — pure functions operating on typed models
# ---------------------------------------------------------------------------

def check_unknown_variables(
    found_vars: frozenset[str],
    known_vars: frozenset[str],
    rel_path: str,
) -> list[LintError]:
    """Check for variables in template that aren't in the schema."""
    errors: list[LintError] = []
    for var in sorted(found_vars - known_vars):
        suggestions: list[str] = get_close_matches(var, list(known_vars), n=1, cutoff=0.6)
        suggestion: Optional[str] = suggestions[0] if suggestions else None
        errors.append(LintError(
            file_path=rel_path,
            error_type=ErrorType.UNKNOWN_VARIABLE,
            message=f"unknown variable {{{var}}}",
            suggestion=f"Did you mean {{{suggestion}}}?" if suggestion else None,
        ))
    return errors


def check_missing_required_variables(
    found_vars: frozenset[str],
    variables_schema: VariablesSchema,
    phase: str,
    mode: str,
    rel_path: str,
    mode_schema: ModeSchema,
) -> list[LintError]:
    """Check that all required variables for this phase+mode are present."""
    errors: list[LintError] = []
    for var_name, var_def in variables_schema.variables.items():
        if not var_def.required:
            continue
        if phase not in var_def.phases:
            continue
        if var_def.modes and mode not in var_def.modes:
            continue
        if var_name == "MODE":
            if phase not in mode_schema.mode_in_phases:
                continue
        if var_name not in found_vars:
            errors.append(LintError(
                file_path=rel_path,
                error_type=ErrorType.MISSING_VARIABLE,
                message=f"missing required variable {{{var_name}}} (required for phase: {phase})",
                schema_ref="schema/variables.yml",
            ))
    return errors


def check_mode_specific_variables(
    found_vars: frozenset[str],
    variables_schema: VariablesSchema,
    mode_schema: ModeSchema,
    phase: str,
    rel_path: str,
) -> list[LintError]:
    """Check that mode-specific variables are present where required."""
    errors: list[LintError] = []
    for var_name in mode_schema.variables:
        var_def: Optional[VariableDefinition] = variables_schema.variables.get(var_name)
        if var_def is None:
            continue
        if phase not in var_def.phases:
            continue
        if var_name not in found_vars:
            errors.append(LintError(
                file_path=rel_path,
                error_type=ErrorType.MISSING_MODE_VARIABLE,
                message=f"missing mode-specific variable {{{var_name}}} (required for {mode_schema.mode} mode in phase: {phase})",
                schema_ref=f"schema/modes/{mode_schema.mode}.yml",
            ))
    return errors


def check_required_headings(
    found_headings_lower: list[str],
    mode_schema: ModeSchema,
    phase: str,
    rel_path: str,
) -> list[LintError]:
    """Check required headings for arbitration, synthesis, and cross-round-synthesis."""
    errors: list[LintError] = []
    schema_ref: str = f"schema/modes/{mode_schema.mode}.yml"

    if phase == Phase.ARBITRATION:
        for heading in mode_schema.arbitration.required_headings:
            if heading.lower() not in found_headings_lower:
                errors.append(LintError(
                    file_path=rel_path,
                    error_type=ErrorType.MISSING_HEADING,
                    message=f'missing required heading "{heading}" (required for {mode_schema.mode} arbitration)',
                    schema_ref=schema_ref,
                ))

    if phase == Phase.SYNTHESIS:
        dispute_heading: str = mode_schema.disputes.synthesis_heading
        if dispute_heading:
            heading_text: str = dispute_heading.lstrip("#").strip()
            if heading_text.lower() not in found_headings_lower:
                errors.append(LintError(
                    file_path=rel_path,
                    error_type=ErrorType.MISSING_HEADING,
                    message=f'missing dispute heading "{dispute_heading}" (required by dispute-parsing subsystem)',
                    schema_ref=schema_ref,
                ))

    if phase == Phase.CROSS_ROUND_SYNTHESIS:
        crs_heading: str = mode_schema.cross_round_synthesis.dispute_heading
        if crs_heading:
            heading_text = crs_heading.lstrip("#").strip()
            if heading_text.lower() not in found_headings_lower:
                errors.append(LintError(
                    file_path=rel_path,
                    error_type=ErrorType.MISSING_HEADING,
                    message=f'missing dispute heading "{crs_heading}" (required for cross-round synthesis)',
                    schema_ref=schema_ref,
                ))

    return errors


def check_structural_markers(
    content: str,
    mode_schema: ModeSchema,
    phase: str,
    rel_path: str,
) -> list[LintError]:
    """Check for required DISPUTES_BEGIN/END structural markers."""
    needs_markers: bool = (
        (phase == Phase.SYNTHESIS and mode_schema.disputes.structural_markers)
        or (phase == Phase.CROSS_ROUND_SYNTHESIS and mode_schema.cross_round_synthesis.structural_markers)
    )
    if not needs_markers:
        return []

    errors: list[LintError] = []
    if not has_structural_marker(content, DISPUTES_BEGIN):
        errors.append(LintError(
            file_path=rel_path,
            error_type=ErrorType.MISSING_MARKER,
            message=f"missing required structural marker {DISPUTES_BEGIN}",
        ))
    if not has_structural_marker(content, DISPUTES_END):
        errors.append(LintError(
            file_path=rel_path,
            error_type=ErrorType.MISSING_MARKER,
            message=f"missing required structural marker {DISPUTES_END}",
        ))
    return errors


def validate_template(
    template_path: Path,
    phase: str,
    mode: str,
    variables_schema: VariablesSchema,
    mode_schema: ModeSchema,
    all_var_names: frozenset[str],
) -> list[LintError]:
    """Validate a single template file. Returns list of typed LintError objects.

    Composes all check functions — each is a pure function that takes
    extracted data and returns errors without side effects.
    """
    rel_path: str = str(template_path.relative_to(template_path.parent.parent.parent))
    content: str = template_path.read_text()
    found_vars: frozenset[str] = extract_variables(content)
    found_headings_lower: list[str] = [h.lower() for h in extract_headings(content)]

    return (
        check_unknown_variables(found_vars, all_var_names, rel_path)
        + check_missing_required_variables(found_vars, variables_schema, phase, mode, rel_path, mode_schema)
        + check_mode_specific_variables(found_vars, variables_schema, mode_schema, phase, rel_path)
        + check_required_headings(found_headings_lower, mode_schema, phase, rel_path)
        + check_structural_markers(content, mode_schema, phase, rel_path)
    )


# ---------------------------------------------------------------------------
# Programmatic validation API
# ---------------------------------------------------------------------------

def validate_all(config: ValidationConfig) -> ValidationResult:
    """Validate all templates against the schema. Programmatic entry point.

    Raises:
        SchemaLoadError: If a schema file cannot be loaded.
    """
    schema: VariablesSchema = load_variables_schema(config.root)
    all_var_names: frozenset[str] = schema.all_names

    modes: list[str] = (
        [config.mode] if config.mode
        else sorted(p.stem for p in (config.root / "schema" / "modes").glob("*.yml"))
    )

    all_errors: list[LintError] = []
    total_files: int = 0

    for mode in modes:
        ms: ModeSchema = load_mode_schema(config.root, mode)
        templates_dir: Path = config.root / "templates" / mode

        if not templates_dir.is_dir():
            all_errors.append(LintError(
                file_path=f"templates/{mode}/",
                error_type=ErrorType.MISSING_VARIABLE,
                message="directory not found",
            ))
            continue

        # P3-7: Validate mode schema template entries against known phase names
        for tmpl_name in ms.templates:
            if tmpl_name not in VALID_PHASES:
                all_errors.append(LintError(
                    file_path=f"schema/modes/{mode}.yml",
                    error_type=ErrorType.UNKNOWN_VARIABLE,
                    message=f"template '{tmpl_name}' is not a recognized phase name",
                ))

        for tmpl_name in ms.templates:
            tmpl_path: Path = templates_dir / f"{tmpl_name}.md"
            if not tmpl_path.exists():
                all_errors.append(LintError(
                    file_path=f"templates/{mode}/{tmpl_name}.md",
                    error_type=ErrorType.MISSING_VARIABLE,
                    message=f"expected template file missing (listed in schema/modes/{mode}.yml)",
                    schema_ref=f"schema/modes/{mode}.yml",
                ))

        for tmpl_path in sorted(templates_dir.glob("*.md")):
            phase: str = tmpl_path.stem
            total_files += 1
            errors: list[LintError] = validate_template(
                tmpl_path, phase, mode, schema, ms, all_var_names,
            )
            all_errors.extend(errors)

    return ValidationResult(errors=all_errors, files_checked=total_files)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.command()
@click.option("--mode", "target_mode", default=None,
              type=click.Choice(["cooperative", "red-blue", "winner-take-all", "prisoners-dilemma"]),
              help="Validate only this mode's templates (default: all modes)")
@click.option("--verbose", is_flag=True, help="Show per-file validation details")
def main(target_mode: Optional[str], verbose: bool) -> None:
    """Validate conversus templates against the schema."""
    try:
        root: Path = find_project_root()
    except SchemaLoadError as e:
        click.echo(str(e), err=True)
        sys.exit(2)

    config = ValidationConfig(root=root, mode=target_mode)
    try:
        result = validate_all(config)
    except SchemaLoadError as e:
        click.echo(str(e), err=True)
        sys.exit(2)

    if verbose:
        click.echo(f"Checked {result.files_checked} template files.")

    if not result.passed:
        click.echo(f"\n{len(result.errors)} error(s) found across {result.files_checked} templates:\n")
        for err in result.errors:
            msg: str = f"{err.file_path}: {err.message}"
            if err.suggestion:
                msg += f" {err.suggestion}"
            if err.schema_ref:
                msg += f" (see {err.schema_ref})"
            click.echo(f"  ✗ {msg}")
        click.echo()
        sys.exit(1)
    else:
        click.echo(f"All {result.files_checked} templates valid against schema.")
        sys.exit(0)


if __name__ == "__main__":
    main()
