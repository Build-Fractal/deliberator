"""
Data-driven test suite for deliberator preset YAML validation.

Validates every preset in presets/**/*.yml against the SKILL.md-defined
structural rules: name-filename match, category-directory match, required
fields, no duplicate names, and minimum preset count.
"""

from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

PRESETS_DIR: Path = Path(__file__).resolve().parent.parent / "presets"


def discover_preset_files() -> list[Path]:
    """Return all .yml preset files under presets/, excluding non-YAML files."""
    return sorted(PRESETS_DIR.rglob("*.yml"))


def load_preset(path: Path) -> dict:
    """Load and return a preset YAML file as a dict."""
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Parametrized: Per-preset structural validation
# ---------------------------------------------------------------------------

PRESET_FILES: list[Path] = discover_preset_files()
PRESET_IDS: list[str] = [
    f"{p.parent.name}/{p.stem}" for p in PRESET_FILES
]


@pytest.mark.parametrize("preset_path", PRESET_FILES, ids=PRESET_IDS)
class TestPresetStructure:
    """Validate structural rules for each individual preset."""

    def test_name_matches_filename(self, preset_path: Path) -> None:
        """The 'name' field must match the filename without .yml extension."""
        data = load_preset(preset_path)
        assert "name" in data, f"Missing 'name' field in {preset_path}"
        assert data["name"] == preset_path.stem, (
            f"name '{data['name']}' does not match filename '{preset_path.stem}' "
            f"in {preset_path}"
        )

    def test_category_matches_directory(self, preset_path: Path) -> None:
        """The 'category' field must match the parent directory name."""
        data = load_preset(preset_path)
        assert "category" in data, f"Missing 'category' field in {preset_path}"
        assert data["category"] == preset_path.parent.name, (
            f"category '{data['category']}' does not match directory "
            f"'{preset_path.parent.name}' in {preset_path}"
        )

    def test_prompt_is_nonempty_string(self, preset_path: Path) -> None:
        """The 'prompt' field must be present and a non-empty string."""
        data = load_preset(preset_path)
        assert "prompt" in data, f"Missing 'prompt' field in {preset_path}"
        assert isinstance(data["prompt"], str), (
            f"'prompt' is not a string in {preset_path}"
        )
        assert data["prompt"].strip(), (
            f"'prompt' is empty in {preset_path}"
        )

    def test_description_is_nonempty_string(self, preset_path: Path) -> None:
        """The 'description' field must be present and a non-empty string."""
        data = load_preset(preset_path)
        assert "description" in data, (
            f"Missing 'description' field in {preset_path}"
        )
        assert isinstance(data["description"], str), (
            f"'description' is not a string in {preset_path}"
        )
        assert data["description"].strip(), (
            f"'description' is empty in {preset_path}"
        )

    def test_composable_field_present_and_boolean(self, preset_path: Path) -> None:
        """The 'composable' field must be present and a boolean (M4)."""
        data = load_preset(preset_path)
        assert "composable" in data, (
            f"Missing 'composable' field in {preset_path}"
        )
        assert isinstance(data["composable"], bool), (
            f"'composable' is not a boolean in {preset_path}, "
            f"got {type(data['composable']).__name__}: {data['composable']!r}"
        )


# ---------------------------------------------------------------------------
# Standalone: No duplicate preset names
# ---------------------------------------------------------------------------

class TestPresetUniqueness:
    """Validate cross-preset constraints."""

    def test_no_duplicate_names(self) -> None:
        """All preset 'name' values must be globally unique."""
        names: list[str] = []
        for path in discover_preset_files():
            data = load_preset(path)
            names.append(data.get("name", f"<missing:{path}>"))

        seen: dict[str, list[str]] = {}
        for name in names:
            seen.setdefault(name, []).append(name)

        duplicates = [name for name, occurrences in seen.items() if len(occurrences) > 1]
        assert not duplicates, (
            f"Duplicate preset names found: {duplicates}"
        )


# ---------------------------------------------------------------------------
# Standalone: Minimum preset count (R009 floor)
# ---------------------------------------------------------------------------

class TestPresetCount:
    """Validate total preset inventory meets requirements."""

    def test_minimum_preset_count(self) -> None:
        """Total preset count must be ≥ 20 (R009 floor)."""
        preset_files = discover_preset_files()
        assert len(preset_files) >= 20, (
            f"Expected ≥ 20 presets but found {len(preset_files)}. "
            f"Presets directory: {PRESETS_DIR}"
        )
