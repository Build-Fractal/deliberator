"""Config parser for the conversus engine.

Handles all SKILL.md Step 1 logic: YAML parsing, preset resolution
(single, composed up to 3, with composition templates), target/prior file
resolution, agent name validation, mode validation, arbiter validation,
rounds/stagnation validation.  Returns a typed ``EngineConfig`` Pydantic
model.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel

from conversus.schemas.modes import VALID_MODES as _CANONICAL_MODES


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ConfigError(Exception):
    """Raised when a conversus config fails validation."""

    pass


# ---------------------------------------------------------------------------
# Public Pydantic config models
# ---------------------------------------------------------------------------

class AgentConfig(BaseModel):
    """A fully resolved agent definition."""

    model_config = {"frozen": True}

    name: str
    prompt: str
    docs: list[Path] = []
    role: str | None = None
    provider: str | None = None
    """Per-agent execution provider override.  When set, this agent uses
    a different provider than the global ``--provider`` flag.  Enables
    heterogeneous deliberation (e.g., one agent on claude-code, another
    on ollama).  ``None`` means use the global provider."""
    agent_model: str | None = None
    """Per-agent model override.  When set, overrides the global
    ``--model`` flag for this agent only.  Named ``agent_model`` to
    avoid shadowing Pydantic's ``model`` namespace."""
    timeout: int | None = None
    """Per-agent timeout in seconds.  When set, overrides the provider's
    default timeout for this agent only.  Useful for agents with large
    doc sets that need more time (e.g., Opus reviewing 3000+ lines)."""


class ArbiterConfig(BaseModel):
    """A fully resolved arbiter definition."""

    model_config = {"frozen": True}

    name: str
    prompt: str
    docs: list[Path] = []
    grounding: Path
    trigger: Literal["disputes_remain", "always"]
    timing: Literal["final", "inter-round"] = "final"
    """When the arbiter runs.  ``final`` (default) runs once after all rounds
    complete; ``inter-round`` runs between each round.  (spec 006)"""
    influence: Literal["binding", "recommended", "advisory"] = "binding"
    """How much weight the arbiter's decision carries.  ``binding`` (default,
    spec 001 behaviour) forces adoption; ``recommended`` and ``advisory``
    allow agents to weigh the ruling.  (spec 006)"""


# Provider validation: accept any provider in the execution registry
# plus the legacy auth-only providers. Previously hardcoded to
# ("anthropic", "openai") which rejected 11+ valid providers (G12).
def _valid_providers() -> frozenset[str]:
    """Build the set of valid provider names from the execution registry."""
    from engine.execution.providers import PROVIDER_REGISTRY
    # Include legacy auth providers and all registered execution providers
    return frozenset(PROVIDER_REGISTRY.keys()) | {"anthropic", "openai"}


VALID_PROVIDERS = _valid_providers()


class EngineConfig(BaseModel):
    """The complete parsed and validated config."""

    model_config = {"frozen": True}

    mode: str
    target_files: list[Path]
    output: Path
    agents: list[AgentConfig]
    iterations: int = 1
    rounds: int = 1
    stagnation: str = "detect"
    prior_files: list[Path] = []
    arbiter: ArbiterConfig | None = None
    validate_templates: bool = True
    provider: str = "anthropic"
    plugins: list[dict] = []
    """Plugin configurations from conversus.yml ``plugins:`` key.
    Each dict has ``name``, optional ``package``, and optional ``config``."""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_MODES = tuple(sorted(_CANONICAL_MODES))
AGENT_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9\-_]*$")

# Composition templates (from SKILL.md)
TWO_PRESET_TEMPLATE = """\
You are {a_name} applied to {b_name}'s domain.

PRIMARY IDENTITY:
{a_prompt}

DOMAIN/MODIFIER:
{b_prompt}

YOUR COMBINED ROLE:
Apply the reasoning style, principles, and priorities defined in your
primary identity to the subject matter and domain expertise of your
modifier(s). When your primary identity's principles conflict with your
modifier's domain conventions, state the conflict explicitly rather than
silently resolving it."""

THREE_PRESET_TEMPLATE = """\
You are {a_name} applied to {b_name}'s domain with {c_name}'s concerns.

PRIMARY IDENTITY:
{a_prompt}

FIRST MODIFIER:
{b_prompt}

SECOND MODIFIER:
{c_prompt}

YOUR COMBINED ROLE:
Apply the reasoning style, principles, and priorities defined in your
primary identity to the subject matter of your first modifier, while
keeping your second modifier's concerns as a persistent evaluation lens.
When principles conflict across your presets, state the conflict
explicitly rather than silently resolving it."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _find_conversus_root() -> Path:
    """Locate the conversus package root (directory containing schema/ and templates/).

    Resolution order:
    1. Parent of *this file* (engine/ lives alongside schema/ and templates/).
    2. ``importlib.resources`` via ``conversus.paths`` (works when pip-installed).
    3. Current working directory.

    Raises:
        ConfigError: If the root cannot be located.
    """
    # Strategy 1: engine/ is a direct child of the conversus root (dev)
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "schema").is_dir() and (candidate / "templates").is_dir():
        return candidate

    # Strategy 2: importlib.resources (works when pip-installed)
    try:
        from conversus.paths import get_presets_dir
        # The presets dir's parent is the conversus package root in the wheel,
        # which also contains templates/ and schema/ via force-include.
        presets = get_presets_dir()
        pkg_root = presets.parent
        if (pkg_root / "templates").exists():
            return pkg_root
    except (ImportError, FileNotFoundError):
        pass

    # Strategy 3: cwd
    cwd = Path.cwd()
    if (cwd / "schema").is_dir() and (cwd / "templates").is_dir():
        return cwd

    raise ConfigError(
        "Cannot locate conversus root (schema/ + templates/). "
        "Run from the conversus directory or ensure engine/ is inside it."
    )


def _resolve_file_entries(
    raw: str | list[str],
    base: Path,
    field_name: str,
) -> list[Path]:
    """Resolve a target/prior entry into a list of existing paths.

    Resolution order for each entry:
      1. Relative to ``base`` (config file's parent directory)
      2. Relative to CWD (project root / invocation directory)
      3. Absolute path (used as-is)

    This two-pass resolution handles both conventions:
      - ``target: ./spec.md`` (relative to config dir) — resolves in pass 1
      - ``target: specs/X/spec.md`` (relative to project root) — resolves in pass 2

    Rules:
      - String ending in ``/`` → directory: find all ``.md`` files (non-recursive)
      - String ending in a file extension → single file
      - List → resolve each entry recursively

    Raises:
        ConfigError: If any resolved path does not exist on disk.
    """
    if isinstance(raw, str):
        raw = [raw]

    cwd = Path.cwd()
    resolved: list[Path] = []
    for entry in raw:
        # Try config-dir-relative first, then CWD-relative
        p_base = (base / entry).resolve()
        p_cwd = (cwd / entry).resolve()
        p = p_base if p_base.exists() or p_base.is_dir() else p_cwd

        if entry.endswith("/"):
            # Directory: non-recursive .md enumeration
            if not p.is_dir():
                raise ConfigError(
                    f"{field_name}: directory not found: {entry} "
                    f"(tried {p_base} and {p_cwd})"
                )
            md_files = sorted(p.glob("*.md"))
            if not md_files:
                raise ConfigError(
                    f"{field_name}: no .md files found in directory: {entry}"
                )
            resolved.extend(md_files)
        else:
            # Single file
            if not p.exists():
                raise ConfigError(
                    f"{field_name}: file not found: {entry} "
                    f"(tried {p_base} and {p_cwd})"
                )
            resolved.append(p)
    return resolved


# ---------------------------------------------------------------------------
# Preset resolution
# ---------------------------------------------------------------------------

_preset_cache: dict[Path, dict[str, Any]] = {}


def _load_preset_file(path: Path) -> dict[str, Any]:
    """Load and validate a single preset YAML file.  Cached per path."""
    if path in _preset_cache:
        return _preset_cache[path]

    if not path.exists():
        raise ConfigError(f"Preset file not found: {path}")

    with open(path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ConfigError(f"Preset file is not a valid YAML mapping: {path}")

    # Validate required fields
    expected_name = path.stem
    if data.get("name") != expected_name:
        raise ConfigError(
            f"Preset '{path}': 'name' field ('{data.get('name')}') must match "
            f"filename ('{expected_name}')."
        )

    expected_category = path.parent.name
    if data.get("category") != expected_category:
        raise ConfigError(
            f"Preset '{path}': 'category' field ('{data.get('category')}') must match "
            f"parent directory ('{expected_category}')."
        )

    if not data.get("prompt", "").strip():
        raise ConfigError(f"Preset '{path}': 'prompt' field must be non-empty.")

    if "description" not in data:
        raise ConfigError(f"Preset '{path}': 'description' field must be present.")

    _preset_cache[path] = data
    return data


def _resolve_single_preset(name: str, presets_root: Path) -> dict[str, Any]:
    """Resolve a single preset by name.

    - Qualified name (contains ``/``): look for ``presets/{name}.yml`` directly.
    - Unqualified: search all category dirs.
    """
    if "/" in name:
        # Qualified
        path = presets_root / f"{name}.yml"
        if not path.exists():
            raise ConfigError(
                f"Preset '{name}' not found at {presets_root / name}.yml."
            )
        return _load_preset_file(path)

    # Unqualified — search all category directories
    matches: list[Path] = []
    if presets_root.is_dir():
        for category_dir in sorted(presets_root.iterdir()):
            if category_dir.is_dir():
                candidate = category_dir / f"{name}.yml"
                if candidate.exists():
                    matches.append(candidate)

    if len(matches) == 0:
        # Collect all available preset names for the error message
        all_names: list[str] = []
        if presets_root.is_dir():
            for category_dir in sorted(presets_root.iterdir()):
                if category_dir.is_dir():
                    for p in sorted(category_dir.glob("*.yml")):
                        all_names.append(p.stem)
        available = ", ".join(all_names) if all_names else "(none)"
        raise ConfigError(
            f"Preset '{name}' not found. Available presets: {available}."
        )

    if len(matches) > 1:
        paths = ", ".join(str(m.relative_to(presets_root)) for m in matches)
        qualified = ", ".join(
            f"'{m.parent.name}/{m.stem}'" for m in matches
        )
        raise ConfigError(
            f"Ambiguous preset '{name}' found in: {paths}. "
            f"Use qualified name: {qualified}."
        )

    return _load_preset_file(matches[0])


def _resolve_presets(
    preset_value: str | list[str],
    presets_root: Path,
) -> tuple[str, list[str]]:
    """Resolve preset(s) into (prompt, docs_list).

    Returns:
        (composed_prompt, docs_list_as_strings)
    """
    if isinstance(preset_value, str):
        # Single preset
        data = _resolve_single_preset(preset_value, presets_root)
        return data["prompt"].rstrip(), data.get("docs", []) or []

    # Composed presets (list)
    if len(preset_value) > 3:
        raise ConfigError(
            "Maximum 3 presets per composition. Simplify or use an inline prompt."
        )

    resolved: list[dict[str, Any]] = []
    for name in preset_value:
        data = _resolve_single_preset(name, presets_root)
        if data.get("composable") is False:
            raise ConfigError(
                f"Preset '{data['name']}' is not composable. "
                "Use it alone or with an inline prompt override."
            )
        resolved.append(data)

    # Build composed prompt
    if len(resolved) == 2:
        composed_prompt = TWO_PRESET_TEMPLATE.format(
            a_name=resolved[0]["name"],
            a_prompt=resolved[0]["prompt"].rstrip(),
            b_name=resolved[1]["name"],
            b_prompt=resolved[1]["prompt"].rstrip(),
        )
    else:
        composed_prompt = THREE_PRESET_TEMPLATE.format(
            a_name=resolved[0]["name"],
            a_prompt=resolved[0]["prompt"].rstrip(),
            b_name=resolved[1]["name"],
            b_prompt=resolved[1]["prompt"].rstrip(),
            c_name=resolved[2]["name"],
            c_prompt=resolved[2]["prompt"].rstrip(),
        )

    # Merge docs: deduplicated union in preset order
    seen: set[str] = set()
    merged_docs: list[str] = []
    for data in resolved:
        for doc in data.get("docs", []) or []:
            if doc not in seen:
                seen.add(doc)
                merged_docs.append(doc)

    return composed_prompt, merged_docs


def _resolve_agent(
    raw: dict[str, Any],
    presets_root: Path,
    base_path: Path,
    index: int,
) -> AgentConfig:
    """Resolve a single agent entry (with optional preset) into an AgentConfig."""
    name = raw.get("name")
    if not name:
        raise ConfigError(f"agents[{index}]: 'name' is required.")

    # Start with preset values if present
    preset_prompt: str | None = None
    preset_docs: list[str] = []

    if "preset" in raw and raw["preset"] is not None:
        preset_prompt, preset_docs = _resolve_presets(raw["preset"], presets_root)

    # Apply inline overrides
    prompt = raw.get("prompt") if raw.get("prompt") is not None else preset_prompt
    if not prompt:
        raise ConfigError(
            f"agents[{index}] ('{name}'): 'prompt' is required "
            "(provide it inline or via a preset)."
        )

    # Docs: inline replaces preset entirely
    raw_docs = raw.get("docs") if raw.get("docs") is not None else preset_docs
    docs: list[Path] = []
    if raw_docs:
        for doc_entry in raw_docs:
            p = (base_path / doc_entry).resolve()
            if doc_entry.endswith("/"):
                if not p.is_dir():
                    raise ConfigError(
                        f"agents[{index}] ('{name}'): doc directory not found: "
                        f"{doc_entry} (resolved to {p})"
                    )
                docs.append(p)
            else:
                if not p.exists():
                    raise ConfigError(
                        f"agents[{index}] ('{name}'): doc file not found: "
                        f"{doc_entry} (resolved to {p})"
                    )
                docs.append(p)

    role = raw.get("role")
    agent_provider = raw.get("provider")
    agent_model = raw.get("model")
    agent_timeout = raw.get("timeout")
    return AgentConfig(
        name=name,
        prompt=prompt.strip(),
        docs=docs,
        role=role,
        provider=agent_provider,
        agent_model=agent_model,
        timeout=int(agent_timeout) if agent_timeout is not None else None,
    )


def _resolve_arbiter(
    raw: dict[str, Any],
    presets_root: Path,
    base_path: Path,
) -> ArbiterConfig:
    """Resolve the arbiter section into an ArbiterConfig."""
    name = raw.get("name")
    if not name:
        raise ConfigError("arbiter.name is required.")

    # Preset resolution for arbiter
    preset_prompt: str | None = None
    preset_docs: list[str] = []

    if "preset" in raw and raw["preset"] is not None:
        preset_prompt, preset_docs = _resolve_presets(raw["preset"], presets_root)

    # Inline overrides
    prompt = raw.get("prompt") if raw.get("prompt") is not None else preset_prompt
    if not prompt:
        raise ConfigError(
            "arbiter: 'prompt' is required (provide it inline or via a preset)."
        )

    raw_docs = raw.get("docs") if raw.get("docs") is not None else preset_docs
    docs: list[Path] = []
    if raw_docs:
        for doc_entry in raw_docs:
            p = (base_path / doc_entry).resolve()
            if doc_entry.endswith("/"):
                if not p.is_dir():
                    raise ConfigError(
                        f"arbiter: doc directory not found: {doc_entry} "
                        f"(resolved to {p})"
                    )
                docs.append(p)
            else:
                if not p.exists():
                    raise ConfigError(
                        f"arbiter: doc file not found: {doc_entry} "
                        f"(resolved to {p})"
                    )
                docs.append(p)

    # Grounding is always required inline
    grounding_raw = raw.get("grounding")
    if not grounding_raw:
        raise ConfigError(
            "arbiter.grounding is required — the arbiter must declare "
            "its decision framework."
        )
    grounding = (base_path / grounding_raw).resolve()
    if not grounding.exists():
        raise ConfigError(
            f"arbiter.grounding path does not exist: {grounding_raw} "
            f"(resolved to {grounding})"
        )

    # Trigger is always required inline
    trigger = raw.get("trigger")
    if trigger not in ("disputes_remain", "always"):
        raise ConfigError(
            "arbiter.trigger must be 'disputes_remain' or 'always'."
        )

    # Timing (spec 006) — default: "final" (single post-loop arbitration)
    timing = raw.get("timing", "final")
    if timing not in ("final", "inter-round"):
        raise ConfigError(
            f"arbiter.timing must be 'final' or 'inter-round', got {timing!r}"
        )

    # Influence (spec 006) — default: "binding" (spec 001 behavior)
    influence = raw.get("influence", "binding")
    if influence not in ("binding", "recommended", "advisory"):
        raise ConfigError(
            f"arbiter.influence must be 'binding', 'recommended', or 'advisory', "
            f"got {influence!r}"
        )

    return ArbiterConfig(
        name=name,
        prompt=prompt.strip(),
        docs=docs,
        grounding=grounding,
        trigger=trigger,
        timing=timing,
        influence=influence,
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def parse_config(config_path: Path) -> EngineConfig:
    """Parse and validate a conversus YAML config file.

    Performs all SKILL.md Step 1 validation: YAML parsing, preset resolution,
    target/prior file resolution, agent name validation, mode validation,
    arbiter validation, rounds/stagnation validation.

    Args:
        config_path: Path to the ``conversus.yml`` file.

    Returns:
        A fully validated ``EngineConfig`` model.

    Raises:
        ConfigError: On any validation failure with field name, value,
            and constraint violated.
    """
    # Clear preset cache for each parse run
    _preset_cache.clear()

    config_path = config_path.resolve()
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ConfigError(f"Config file is not a valid YAML mapping: {config_path}")

    # Base path for resolving relative paths in the config
    base_path = config_path.parent

    # Locate conversus package root for presets
    conversus_root = _find_conversus_root()
    presets_root = conversus_root / "presets"

    # --- Mode validation ---
    mode = raw.get("mode")
    if mode not in VALID_MODES:
        raise ConfigError(
            f"mode: '{mode}' is not valid. Must be one of: "
            f"{', '.join(VALID_MODES)}."
        )

    # --- Output path ---
    output_raw = raw.get("output")
    if not output_raw:
        raise ConfigError("output: is required.")
    output = (base_path / output_raw).resolve()

    # --- Target resolution ---
    target_raw = raw.get("target")
    if not target_raw:
        raise ConfigError("target: is required.")
    target_files = _resolve_file_entries(target_raw, base_path, "target")

    # --- Prior resolution ---
    prior_raw = raw.get("prior")
    prior_files: list[Path] = []
    if prior_raw:
        prior_files = _resolve_file_entries(prior_raw, base_path, "prior")

    # --- Iterations ---
    iterations = raw.get("iterations", 1)
    if not isinstance(iterations, int) or iterations < 1:
        raise ConfigError(
            f"iterations: '{iterations}' is not valid. Must be an integer >= 1."
        )

    # --- Rounds ---
    rounds = raw.get("rounds", 1)
    if not isinstance(rounds, int) or rounds < 1 or rounds > 5:
        msg = "rounds must be an integer between 1 and 5."
        if isinstance(rounds, int) and rounds >= 6:
            msg += (
                " For deliberations requiring more depth, consider adding "
                "an arbiter (see spec-001)."
            )
        raise ConfigError(msg)

    # --- Stagnation ---
    stagnation = raw.get("stagnation", "detect")
    if stagnation not in ("detect", "ignore"):
        raise ConfigError("stagnation must be 'detect' or 'ignore'.")

    # --- validate_templates ---
    validate_templates = raw.get("validate_templates", True)
    if not isinstance(validate_templates, bool):
        raise ConfigError("validate_templates must be true or false.")

    # --- Provider ---
    provider = raw.get("provider", "anthropic")
    if provider not in VALID_PROVIDERS:
        raise ConfigError(
            f"provider: '{provider}' is not valid. "
            f"Must be one of: {', '.join(VALID_PROVIDERS)}."
        )

    # --- Agents ---
    agents_raw = raw.get("agents")
    if not agents_raw or not isinstance(agents_raw, list):
        raise ConfigError("agents: at least 2 agents are required.")

    agents: list[AgentConfig] = []
    for i, agent_raw in enumerate(agents_raw):
        if not isinstance(agent_raw, dict):
            raise ConfigError(f"agents[{i}]: each agent must be a YAML mapping.")
        agents.append(_resolve_agent(agent_raw, presets_root, base_path, i))

    if len(agents) < 2:
        raise ConfigError(
            f"agents: at least 2 agents are required (found {len(agents)})."
        )

    # --- Agent name validation ---
    for agent in agents:
        if not AGENT_NAME_RE.match(agent.name):
            raise ConfigError(
                f"Invalid agent name: '{agent.name}'. "
                "Use lowercase alphanumeric with hyphens/underscores."
            )

    # Check for duplicate agent names
    seen_names: set[str] = set()
    for agent in agents:
        if agent.name in seen_names:
            raise ConfigError(
                f"Duplicate agent name: '{agent.name}'. Agent names must be unique."
            )
        seen_names.add(agent.name)

    # --- Red-blue role enforcement ---
    if mode == "red-blue":
        roles = {a.role for a in agents}
        if "red" not in roles:
            raise ConfigError(
                "red-blue mode requires at least one agent with role: red."
            )
        if "blue" not in roles:
            raise ConfigError(
                "red-blue mode requires at least one agent with role: blue."
            )

    # --- Arbiter validation ---
    arbiter: ArbiterConfig | None = None
    arbiter_raw = raw.get("arbiter")
    if arbiter_raw:
        if not isinstance(arbiter_raw, dict):
            raise ConfigError("arbiter: must be a YAML mapping.")
        arbiter = _resolve_arbiter(arbiter_raw, presets_root, base_path)

        # Cross-field validation: inter-round timing requires more than one round.
        # Inter-round arbitration runs *between* rounds, so a single-round run
        # has no gap for it to occupy.  Reject the config rather than silently
        # producing a no-op deliberation.
        if arbiter is not None and arbiter.timing == "inter-round" and rounds <= 1:
            raise ConfigError(
                f"arbiter.timing is 'inter-round' but rounds={rounds}: "
                "inter-round arbitration runs between rounds and requires "
                "rounds > 1.  Either set rounds to 2 or more, or change "
                "arbiter.timing to 'final' (or omit timing to use the default)."
            )

    # Parse plugins (optional)
    plugins_raw = raw.get("plugins", [])
    if not isinstance(plugins_raw, list):
        plugins_raw = []

    return EngineConfig(
        mode=mode,
        target_files=target_files,
        output=output,
        agents=agents,
        iterations=iterations,
        rounds=rounds,
        stagnation=stagnation,
        prior_files=prior_files,
        arbiter=arbiter,
        validate_templates=validate_templates,
        provider=provider,
        plugins=plugins_raw,
    )
