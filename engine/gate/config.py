"""Gate configuration: `~/.config/deliberator/gate.yml`, defaults otherwise.

A project's `.deliberator/gate.yml` is read only when the user config opts in with
`allow_project_config: true` (a cloned repo must not be able to switch the gate to the mock
judge). Even then it cannot change where the log goes, the graph connection, or the opt-in.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

Provider = Literal["bedrock", "anthropic", "claude-code", "mock"]
Effort = Literal["low", "medium", "high", "xhigh", "max"]

CONFIG_PATH = Path(".deliberator") / "gate.yml"
# The config for every project; a project gate.yml is read only if this file opts in.
USER_CONFIG_PATH = Path.home() / ".config" / "deliberator" / "gate.yml"

DEFAULT_RULES: tuple[str, ...] = (
    (
        "Never lose work: deny deleting or overwriting uncommitted or unpushed work, or "
        "someone else's files, without a backup."
    ),
    "Deny force-pushes, history rewrites or branch deletes on main, master or shared branches.",
    "Deny sending secrets, keys or credentials anywhere, or printing their values.",
    (
        "Ask before actions that are costly or hard to undo outside the project: deleting "
        "other repos or data, machine-wide package changes, changing cloud resources, "
        "writing to shared databases, spending money."
    ),
    (
        "Ask before publishing to other people: package releases, deploys, messages, emails, "
        "merging to main. Pushing a feature branch or opening a PR is routine."
    ),
    (
        "Allow ordinary work wherever it happens: reading and searching anywhere, building, "
        "testing, editing, committing, and writing the agent's own notes, memory, scratch "
        "and temporary files."
    ),
)


MAX_TIMEOUT_S = 50.0
# Keys only the user config may set: a project file can't move the log or the graph.
USER_ONLY_KEYS = frozenset({"allow_project_config", "log_dir", "graph_uri", "graph_user",
                            "graph_password_env"})


class GateConfig(BaseModel):
    """What the gate asks, of which model, and where decisions are kept."""

    model_config = ConfigDict(extra="forbid")

    provider: Provider = "bedrock"
    model: str | None = None  # default per provider: see `resolved_model`
    effort: Effort = "low"
    aws_profile: str | None = None
    aws_region: str = "us-east-1"
    # Seconds the judge may take. Kept under the 60 s hook timeout (clamped to 50), so a slow
    # judge becomes an ask instead of the hook being killed and the tool running unlogged.
    timeout_s: float = 40.0
    # Plain-language rules the judge applies, numbered in the prompt and cited in reasons.
    rules: list[str] = Field(default_factory=lambda: list(DEFAULT_RULES))
    # Regexes (matched against the command or path) that are allowed without a model call.
    allow_without_asking: list[str] = Field(default_factory=list)
    # How many earlier decisions to show the judge as precedent.
    precedents: int = 6
    # Reuse an earlier decision for an identical call (same tool, input, folder and rules).
    reuse_identical: bool = True
    # When you approved something the gate asked about, an identical call is then allowed.
    learn_from_approvals: bool = True
    # Where decisions are written as a graph: a bolt URI such as bolt://localhost:7687.
    # None keeps them in the local log and graph.json only.
    graph_uri: str | None = None
    graph_user: str | None = None
    graph_password_env: str | None = None  # name of the env var that holds the password
    # Edits (Write, Edit, MultiEdit, NotebookEdit) to files inside the git repository that
    # holds the working folder are allowed without a model call. Protected paths (.git,
    # .claude, .deliberator, ...), files outside the repo, and sessions in ~, / or ~/code
    # (or outside any repo) still go to the judge.
    allow_edits_in_project: bool = True
    # Keep the log in this folder instead of the project's .deliberator/gate/. Set it in the
    # user config so every project shares one log, and precedent carries across projects.
    log_dir: str | None = None
    # Read a project's .deliberator/gate.yml on top of this one (user config only).
    allow_project_config: bool = False

    @field_validator("timeout_s")
    @classmethod
    def _clamp_timeout(cls, v: float) -> float:
        return min(max(float(v), 0.01), MAX_TIMEOUT_S)

    def store_root(self, project_root: Path) -> Path:
        """The folder whose .deliberator/gate/ holds the log."""
        return Path(self.log_dir).expanduser() if self.log_dir else project_root

    def resolved_model(self) -> str:
        if self.model:
            return self.model
        return {
            "bedrock": "anthropic.claude-opus-5-5",
            "anthropic": "claude-opus-5-5",
            "claude-code": "opus",
            "mock": "mock",
        }[self.provider]

    def rules_hash(self) -> str:
        return hashlib.sha256("\n".join(self.rules).encode()).hexdigest()[:12]


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise TypeError(f"{path}: expected a mapping")
    return data


def config_path(project_root: Path) -> Path | None:
    """The user's gate.yml if it exists (the project's is only an overlay, see load_config)."""
    return USER_CONFIG_PATH if USER_CONFIG_PATH.is_file() else None


def load_config(project_root: Path) -> GateConfig:
    """User config (or defaults); the project's gate.yml on top only if the user opted in."""
    data = _load_yaml(USER_CONFIG_PATH) if USER_CONFIG_PATH.is_file() else {}
    user = GateConfig.model_validate(data)
    project = project_root / CONFIG_PATH
    if not user.allow_project_config or not project.is_file():
        return user
    overlay = {k: v for k, v in _load_yaml(project).items() if k not in USER_ONLY_KEYS}
    return GateConfig.model_validate({**data, **overlay})


EXAMPLE_CONFIG = """\
# deliberator gate: yes/no decisions for Claude Code tool calls.
provider: bedrock            # bedrock | anthropic | claude-code | mock
# model: anthropic.claude-opus-5-5
effort: low                  # thinking effort; low keeps hooks fast
aws_profile: null            # the AWS profile with Bedrock access
aws_region: us-east-1
# rules: plain-language intent the judge weighs (defaults in engine/gate/config.py)
allow_without_asking:        # simple commands only: no chains, redirects or risky flags
  - '^(ls|pwd|wc|which|date|du|df)\\b'
  - '^git (status|diff|log|show)\\b'
precedents: 6
reuse_identical: true
learn_from_approvals: true
graph_uri: null              # e.g. bolt://localhost:7687 (Memgraph)
allow_edits_in_project: true # edits inside the working folder skip the model
log_dir: null                # e.g. ~/.local/share/deliberator: one log for every project
timeout_s: 40                # judge time limit (max 50; the hook's own limit is 60)
allow_project_config: false  # user config only: also read a project's .deliberator/gate.yml
"""
