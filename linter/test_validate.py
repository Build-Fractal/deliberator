"""
Data-driven test suite for the deliberator template linter.

Uses pytest.mark.parametrize to test all templates across all modes
with both positive (valid) and negative (injected defect) cases.
"""

import tempfile
from itertools import product
from pathlib import Path

import pytest

try:
    from .models import ModeSchema, VariableDefinition, VariablesSchema, VALID_PHASES, get_valid_modes
    from .validate import (
        DISPUTES_BEGIN,
        DISPUTES_END,
        extract_headings,
        extract_variables,
        find_project_root,
        has_structural_marker,
        load_mode_schema,
        load_variables_schema,
        validate_template,
    )
except ImportError:
    from models import ModeSchema, VariableDefinition, VariablesSchema, VALID_PHASES, get_valid_modes
    from validate import (
        DISPUTES_BEGIN,
        DISPUTES_END,
        extract_headings,
        extract_variables,
        find_project_root,
        has_structural_marker,
        load_mode_schema,
        load_variables_schema,
        validate_template,
    )

# ---------------------------------------------------------------------------
# Fixtures — typed per constitution Principle IX
# ---------------------------------------------------------------------------

ROOT: Path = find_project_root()

MODES: list[str] = ["cooperative", "red-blue", "winner-take-all", "prisoners-dilemma"]
PHASES: list[str] = [
    "review", "cross-review", "revision", "disputes",
    "synthesis", "arbitration", "cross-round-synthesis",
]


@pytest.fixture(scope="session")
def variables_schema() -> VariablesSchema:
    return load_variables_schema(ROOT)


@pytest.fixture(scope="session")
def all_var_names(variables_schema: VariablesSchema) -> frozenset[str]:
    return variables_schema.all_names


def mode_schema(mode: str) -> ModeSchema:
    return load_mode_schema(ROOT, mode)


def template_path(mode: str, phase: str) -> Path:
    return ROOT / "templates" / mode / f"{phase}.md"


# ---------------------------------------------------------------------------
# Content mutation helpers — pure functions for injecting defects
# ---------------------------------------------------------------------------

def remove_variable(content: str, var_name: str) -> str:
    """Remove all occurrences of {VAR_NAME} from content."""
    return content.replace(f"{{{var_name}}}", "")


def inject_typo(content: str, var_name: str, typo: str) -> str:
    """Replace first occurrence of {VAR_NAME} with {TYPO}."""
    return content.replace(f"{{{var_name}}}", f"{{{typo}}}", 1)


def remove_heading(content: str, heading_text: str) -> str:
    """Remove lines containing a heading with the given text."""
    return "\n".join(
        line for line in content.splitlines()
        if not (line.strip().startswith("#") and heading_text.lower() in line.lower())
    )


def remove_marker(content: str, marker: str) -> str:
    """Remove lines containing a structural marker."""
    return "\n".join(
        line for line in content.splitlines()
        if marker not in line
    )


def validate_mutated_template(
    original_path: Path,
    mutated_content: str,
    phase: str,
    mode: str,
    variables_schema: VariablesSchema,
    ms: ModeSchema,
    all_var_names: frozenset[str],
) -> list:
    """Write mutated content to a temp file and validate it.

    Returns the list of LintError validation errors. Cleans up the temp file.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", dir=original_path.parent, delete=False,
    ) as f:
        f.write(mutated_content)
        tmp_path: Path = Path(f.name)
    try:
        return validate_template(tmp_path, phase, mode, variables_schema, ms, all_var_names)
    finally:
        tmp_path.unlink()


# ---------------------------------------------------------------------------
# Pure function unit tests
# ---------------------------------------------------------------------------

class TestExtractVariables:
    """Tests for the variable extraction regex."""

    @pytest.mark.parametrize("text,expected", [
        ("{AGENT_NAME}", frozenset({"AGENT_NAME"})),
        ("{AGENT_NAME} and {MODE}", frozenset({"AGENT_NAME", "MODE"})),
        ("no variables here", frozenset()),
        ("{lowercase} not matched", frozenset()),
        ("{A}", frozenset()),  # single char — not matched by [A-Z][A-Z_0-9]+ pattern
        ("{VALID_123}", frozenset({"VALID_123"})),
        ("text {AGENT_NAME} more {AGENT_NAME}", frozenset({"AGENT_NAME"})),  # dedup
        ("```{OUTPUT_PATH}```", frozenset({"OUTPUT_PATH"})),  # in code blocks
    ])
    def test_extract(self, text: str, expected: frozenset[str]) -> None:
        assert extract_variables(text) == expected


class TestExtractHeadings:
    """Tests for markdown heading extraction."""

    @pytest.mark.parametrize("text,expected", [
        ("# Title", ["Title"]),
        ("## Sub\n### Deeper", ["Sub", "Deeper"]),
        ("no headings", []),
        ("## Remaining Disputes", ["Remaining Disputes"]),
        ("  ## Indented", ["Indented"]),  # strip() handles leading whitespace
    ])
    def test_extract(self, text: str, expected: list[str]) -> None:
        assert extract_headings(text) == expected


class TestStructuralMarkers:
    """Tests for structural marker detection."""

    @pytest.mark.parametrize("content,marker,expected", [
        ("<!-- DELIBERATOR:DISPUTES_BEGIN -->", DISPUTES_BEGIN, True),
        ("some text", DISPUTES_BEGIN, False),
        ("line\n<!-- DELIBERATOR:DISPUTES_END -->\nline", DISPUTES_END, True),
    ])
    def test_marker(self, content: str, marker: str, expected: bool) -> None:
        assert has_structural_marker(content, marker) == expected


# ---------------------------------------------------------------------------
# Data-driven: All templates should pass validation
# ---------------------------------------------------------------------------

def all_template_cases() -> list[tuple[str, str]]:
    """Generate (mode, phase) pairs for every existing template."""
    return [
        (mode, phase)
        for mode, phase in product(MODES, PHASES)
        if template_path(mode, phase).exists()
    ]


@pytest.mark.parametrize("mode,phase", all_template_cases(),
                         ids=[f"{m}/{p}" for m, p in all_template_cases()])
def test_all_templates_valid(
    mode: str,
    phase: str,
    variables_schema: VariablesSchema,
    all_var_names: frozenset[str],
) -> None:
    """Every existing template must pass validation with zero errors."""
    path: Path = template_path(mode, phase)
    ms: ModeSchema = mode_schema(mode)
    errors = validate_template(path, phase, mode, variables_schema, ms, all_var_names)
    assert errors == [], f"Unexpected errors in {mode}/{phase}: {[e.message for e in errors]}"


# ---------------------------------------------------------------------------
# Data-driven: Missing required variable detection
# ---------------------------------------------------------------------------

def required_variable_cases() -> list[tuple[str, str, str]]:
    """Generate (mode, phase, var_name) for each required variable per template."""
    vs: VariablesSchema = load_variables_schema(ROOT)
    cases: list[tuple[str, str, str]] = []
    for mode in MODES:
        ms: ModeSchema = mode_schema(mode)
        for phase in PHASES:
            path: Path = template_path(mode, phase)
            if not path.exists():
                continue
            found_vars: frozenset[str] = extract_variables(path.read_text())

            for var_name, var_def in vs.variables.items():
                if not var_def.required:
                    continue
                if phase not in var_def.phases:
                    continue
                if var_def.modes and mode not in var_def.modes:
                    continue
                # MODE is conditionally required based on mode_in_phases from mode schema
                if var_name == "MODE" and phase not in ms.mode_in_phases:
                    continue
                if var_name in found_vars:
                    cases.append((mode, phase, var_name))
    return cases


@pytest.mark.parametrize("mode,phase,var_name", required_variable_cases(),
                         ids=[f"{m}/{p}/missing-{v}" for m, p, v in required_variable_cases()])
def test_missing_required_variable_detected(
    mode: str,
    phase: str,
    var_name: str,
    variables_schema: VariablesSchema,
    all_var_names: frozenset[str],
) -> None:
    """Removing a required variable from a template must produce an error."""
    path: Path = template_path(mode, phase)
    ms: ModeSchema = mode_schema(mode)
    mutated: str = remove_variable(path.read_text(), var_name)

    errors = validate_mutated_template(
        path, mutated, phase, mode, variables_schema, ms, all_var_names,
    )
    matching = [
        e for e in errors
        if f"missing required variable {{{var_name}}}" in e.message
        or f"missing mode-specific variable {{{var_name}}}" in e.message
    ]
    assert len(matching) > 0, (
        f"Expected error for missing {{{var_name}}} in {mode}/{phase} but got: {[e.message for e in errors]}"
    )


# ---------------------------------------------------------------------------
# Data-driven: Unknown variable (typo) detection
# ---------------------------------------------------------------------------

TYPO_CASES: list[tuple[str, str]] = [
    ("AGENT_NMAE", "AGENT_NAME"),
    ("OUTPU_PATH", "OUTPUT_PATH"),
    ("TARET_FILES", "TARGET_FILES"),
    ("AGEN_DOCS", "AGENT_DOCS"),
]


@pytest.mark.parametrize("typo,correct", TYPO_CASES,
                         ids=[f"typo-{t}" for t, _ in TYPO_CASES])
def test_unknown_variable_with_suggestion(
    typo: str,
    correct: str,
    variables_schema: VariablesSchema,
    all_var_names: frozenset[str],
) -> None:
    """Unknown variables should be detected and suggest corrections."""
    path: Path = template_path("cooperative", "review")
    ms: ModeSchema = mode_schema("cooperative")
    mutated: str = inject_typo(path.read_text(), correct, typo)

    errors = validate_mutated_template(
        path, mutated, "review", "cooperative", variables_schema, ms, all_var_names,
    )
    unknown_errors = [e for e in errors if f"unknown variable {{{typo}}}" in e.message]
    assert len(unknown_errors) > 0, f"Typo {{{typo}}} not detected"
    suggestion_errors = [e for e in unknown_errors if e.suggestion and f"Did you mean {{{correct}}}?" in e.suggestion]
    assert len(suggestion_errors) > 0, f"No suggestion for {{{typo}}} → {{{correct}}}"


# ---------------------------------------------------------------------------
# Data-driven: Structural marker validation
# ---------------------------------------------------------------------------

def structural_marker_cases() -> list[tuple[str, str, str]]:
    """Generate (mode, phase, marker) for templates requiring structural markers."""
    cases: list[tuple[str, str, str]] = []
    for mode in MODES:
        ms: ModeSchema = mode_schema(mode)
        if ms.disputes.structural_markers:
            cases.append((mode, "synthesis", DISPUTES_BEGIN))
            cases.append((mode, "synthesis", DISPUTES_END))
        if ms.cross_round_synthesis.structural_markers:
            cases.append((mode, "cross-round-synthesis", DISPUTES_BEGIN))
            cases.append((mode, "cross-round-synthesis", DISPUTES_END))
    return cases


@pytest.mark.parametrize("mode,phase,marker", structural_marker_cases(),
                         ids=[f"{m}/{p}/{mk.split(':')[1]}" for m, p, mk in structural_marker_cases()])
def test_missing_structural_marker_detected(
    mode: str,
    phase: str,
    marker: str,
    variables_schema: VariablesSchema,
    all_var_names: frozenset[str],
) -> None:
    """Removing a structural marker must produce an error."""
    path: Path = template_path(mode, phase)
    ms: ModeSchema = mode_schema(mode)
    mutated: str = remove_marker(path.read_text(), marker)

    errors = validate_mutated_template(
        path, mutated, phase, mode, variables_schema, ms, all_var_names,
    )
    matching = [e for e in errors if f"missing required structural marker {marker}" in e.message]
    assert len(matching) > 0, f"Missing marker {marker} not detected in {mode}/{phase}"


# ---------------------------------------------------------------------------
# Data-driven: Arbitration heading validation
# ---------------------------------------------------------------------------

def arbitration_heading_cases() -> list[tuple[str, str]]:
    """Generate (mode, heading) for each required arbitration heading."""
    return [
        (mode, heading)
        for mode in MODES
        for heading in mode_schema(mode).arbitration.required_headings
    ]


@pytest.mark.parametrize("mode,heading", arbitration_heading_cases(),
                         ids=[f"{m}/arb-heading-{h.replace(' ', '_')}" for m, h in arbitration_heading_cases()])
def test_missing_arbitration_heading_detected(
    mode: str,
    heading: str,
    variables_schema: VariablesSchema,
    all_var_names: frozenset[str],
) -> None:
    """Removing a required arbitration heading must produce an error."""
    path: Path = template_path(mode, "arbitration")
    ms: ModeSchema = mode_schema(mode)
    mutated: str = remove_heading(path.read_text(), heading)

    errors = validate_mutated_template(
        path, mutated, "arbitration", mode, variables_schema, ms, all_var_names,
    )
    matching = [e for e in errors if f'missing required heading "{heading}"' in e.message]
    assert len(matching) > 0, f'Heading "{heading}" removal not detected in {mode}/arbitration'


# ---------------------------------------------------------------------------
# Data-driven: Dispute heading validation in synthesis templates
# ---------------------------------------------------------------------------

def dispute_heading_cases() -> list[tuple[str, str, str]]:
    """Generate (mode, phase, heading) for dispute heading checks."""
    cases: list[tuple[str, str, str]] = []
    for mode in MODES:
        ms: ModeSchema = mode_schema(mode)
        synth_heading: str = ms.disputes.synthesis_heading
        if synth_heading:
            cases.append((mode, "synthesis", synth_heading.lstrip("#").strip()))
        crs_heading: str = ms.cross_round_synthesis.dispute_heading
        if crs_heading:
            cases.append((mode, "cross-round-synthesis", crs_heading.lstrip("#").strip()))
    return cases


@pytest.mark.parametrize("mode,phase,heading", dispute_heading_cases(),
                         ids=[f"{m}/{p}/dispute-heading" for m, p, _ in dispute_heading_cases()])
def test_missing_dispute_heading_detected(
    mode: str,
    phase: str,
    heading: str,
    variables_schema: VariablesSchema,
    all_var_names: frozenset[str],
) -> None:
    """Removing a dispute heading must produce an error."""
    path: Path = template_path(mode, phase)
    ms: ModeSchema = mode_schema(mode)
    mutated: str = remove_heading(path.read_text(), heading)

    errors = validate_mutated_template(
        path, mutated, phase, mode, variables_schema, ms, all_var_names,
    )
    matching = [e for e in errors if "dispute heading" in e.message.lower() or f'"{heading}"' in e.message]
    assert len(matching) > 0, f'Dispute heading "{heading}" removal not detected in {mode}/{phase}'


# ---------------------------------------------------------------------------
# Mode-specific variable enforcement
# ---------------------------------------------------------------------------

def mode_specific_var_cases() -> list[tuple[str, str, str]]:
    """Generate (mode, phase, var_name) for mode-specific variables."""
    vs: VariablesSchema = load_variables_schema(ROOT)
    cases: list[tuple[str, str, str]] = []
    for mode in MODES:
        ms: ModeSchema = mode_schema(mode)
        for var_name in ms.variables:
            var_def = vs.variables.get(var_name)
            if var_def is None:
                continue
            for phase in var_def.phases:
                path: Path = template_path(mode, phase)
                if path.exists() and f"{{{var_name}}}" in path.read_text():
                    cases.append((mode, phase, var_name))
    return cases


@pytest.mark.parametrize("mode,phase,var_name", mode_specific_var_cases(),
                         ids=[f"{m}/{p}/mode-var-{v}" for m, p, v in mode_specific_var_cases()])
def test_missing_mode_specific_variable_detected(
    mode: str,
    phase: str,
    var_name: str,
    variables_schema: VariablesSchema,
    all_var_names: frozenset[str],
) -> None:
    """Removing a mode-specific variable must produce an error."""
    path: Path = template_path(mode, phase)
    ms: ModeSchema = mode_schema(mode)
    mutated: str = remove_variable(path.read_text(), var_name)

    errors = validate_mutated_template(
        path, mutated, phase, mode, variables_schema, ms, all_var_names,
    )
    matching = [e for e in errors if var_name in e.message and "missing" in e.message]
    assert len(matching) > 0, f"Mode-specific {{{var_name}}} removal not detected in {mode}/{phase}"


# ---------------------------------------------------------------------------
# Schema consistency
# ---------------------------------------------------------------------------

class TestSchemaConsistency:
    """Verify schema files are self-consistent."""

    @pytest.mark.parametrize("mode", MODES)
    def test_mode_schema_references_valid_variables(
        self, mode: str, variables_schema: VariablesSchema,
    ) -> None:
        """Mode-specific variables in mode schema must exist in variables.yml."""
        ms: ModeSchema = mode_schema(mode)
        for var_name in ms.variables:
            assert var_name in variables_schema.variables, (
                f"Mode schema {mode}.yml references {var_name} "
                f"which is not in variables.yml"
            )

    @pytest.mark.parametrize("mode", MODES)
    def test_mode_schema_templates_exist(self, mode: str) -> None:
        """All templates listed in mode schema must exist on disk."""
        ms: ModeSchema = mode_schema(mode)
        for tmpl_name in ms.templates:
            path: Path = template_path(mode, tmpl_name)
            assert path.exists(), f"Template {mode}/{tmpl_name}.md listed in schema but not found"

    @pytest.mark.parametrize("mode", MODES)
    def test_mode_field_matches_filename(self, mode: str) -> None:
        """The mode field inside the YAML must match the filename."""
        ms: ModeSchema = mode_schema(mode)
        assert ms.mode == mode, (
            f"Mode schema file {mode}.yml has mode: '{ms.mode}' "
            f"but filename says '{mode}'"
        )


# ---------------------------------------------------------------------------
# Schema evolution regression tests (P2-9)
# ---------------------------------------------------------------------------

class TestSchemaEvolution:
    """Verify that schema changes produce expected forward/backward compatibility."""

    @pytest.mark.parametrize("mode", MODES)
    def test_new_optional_variable_accepted(
        self,
        mode: str,
        variables_schema: VariablesSchema,
    ) -> None:
        """Adding an optional variable to the schema doesn't break existing templates."""
        new_var = VariableDefinition(
            type="string",
            description="Test optional variable for schema evolution",
            phases=list(VALID_PHASES),
            required=False,
        )
        extended_vars: dict[str, VariableDefinition] = {
            **variables_schema.variables,
            "TEST_NEW_OPTIONAL_VAR": new_var,
        }
        extended: VariablesSchema = variables_schema.model_copy(
            update={"variables": extended_vars},
        )
        extended_names: frozenset[str] = extended.all_names

        for phase in PHASES:
            path: Path = template_path(mode, phase)
            if not path.exists():
                continue
            ms: ModeSchema = mode_schema(mode)
            errors = validate_template(
                path, phase, mode, extended, ms, extended_names,
            )
            assert not any("TEST_NEW_OPTIONAL_VAR" in e.message for e in errors), (
                f"Optional variable TEST_NEW_OPTIONAL_VAR caused errors in "
                f"{mode}/{phase}: {[e.message for e in errors if 'TEST_NEW_OPTIONAL_VAR' in e.message]}"
            )

    @pytest.mark.parametrize("mode", MODES)
    def test_new_required_variable_produces_errors(
        self,
        mode: str,
        variables_schema: VariablesSchema,
    ) -> None:
        """Adding a required variable produces errors for templates missing it."""
        new_var = VariableDefinition(
            type="string",
            description="Test required variable for schema evolution",
            phases=["review"],
            required=True,
        )
        extended_vars: dict[str, VariableDefinition] = {
            **variables_schema.variables,
            "TEST_REQUIRED_VAR": new_var,
        }
        extended: VariablesSchema = variables_schema.model_copy(
            update={"variables": extended_vars},
        )
        extended_names: frozenset[str] = extended.all_names

        path: Path = template_path(mode, "review")
        if not path.exists():
            pytest.skip(f"No review template for mode {mode}")
        ms: ModeSchema = mode_schema(mode)
        errors = validate_template(
            path, "review", mode, extended, ms, extended_names,
        )
        missing_errors = [
            e for e in errors if "TEST_REQUIRED_VAR" in e.message and "missing" in e.message
        ]
        assert len(missing_errors) > 0, (
            f"Expected missing-variable error for TEST_REQUIRED_VAR in "
            f"{mode}/review but got: {[e.message for e in errors]}"
        )

    def test_new_mode_schema_discovered(self, tmp_path: Path) -> None:
        """A new mode schema YAML in schema/modes/ is picked up by get_valid_modes()."""
        modes_dir: Path = tmp_path / "modes"
        modes_dir.mkdir()

        # Copy existing mode files so the baseline is correct
        real_modes_dir: Path = ROOT / "schema" / "modes"
        for yml in real_modes_dir.glob("*.yml"):
            (modes_dir / yml.name).write_text(yml.read_text())

        # Add a new test mode
        test_mode_path: Path = modes_dir / "test-mode.yml"
        test_mode_path.write_text("mode: test-mode\ntemplates: []\nvariables: []\n")

        discovered: frozenset[str] = get_valid_modes(modes_dir)
        assert "test-mode" in discovered, (
            f"New mode 'test-mode' not discovered. Found: {sorted(discovered)}"
        )
        # Existing modes should still be present
        for expected_mode in MODES:
            assert expected_mode in discovered, (
                f"Existing mode '{expected_mode}' missing after adding test-mode. "
                f"Found: {sorted(discovered)}"
            )
