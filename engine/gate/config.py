"""Gate configuration: `.deliberator/gate.yml` in the project, defaults otherwise."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

Provider = Literal["bedrock", "anthropic", "claude-code", "mock"]
Effort = Literal["low", "medium", "high", "xhigh", "max"]

CONFIG_PATH = Path(".deliberator") / "gate.yml"
# Used when the project has no gate.yml: one config for every project.
USER_CONFIG_PATH = Path.home() / ".config" / "deliberator" / "gate.yml"

DEFAULT_RULES: tuple[str, ...] = (
    "Deny anything that deletes or overwrites uncommitted or unpushed work.",
    "Deny force-pushes, history rewrites or deletes on main, master or shared branches.",
    "Deny commands that send secrets, keys or credentials anywhere, or print them.",
    (
        "Ask before changing anything outside the current project: other repos, the home "
        "directory, machine-wide packages, cloud resources, databases."
    ),
    "Ask before anything that publishes: git push, package publish, deploys, messages.",
    (
        "Allow routine development: reading, searching, building, testing, editing files in "
        "the project, committing on a feature branch."
    ),
)


class GateConfig(BaseModel):
    """What the gate asks, of which model, and where decisions are kept."""

    model_config = ConfigDict(extra="forbid")

    provider: Provider = "bedrock"
    model: str | None = None  # default per provider: see `resolved_model`
    effort: Effort = "low"
    aws_profile: str | None = None
    aws_region: str = "us-east-1"
    timeout_s: float = 45.0
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
    # Edits (Write, Edit, MultiEdit, NotebookEdit) to files inside the working folder are
    # allowed without a model call. Paths in .git, and paths outside the folder, still go
    # to the judge.
    allow_edits_in_project: bool = True
    # Keep the log in this folder instead of the project's .deliberator/gate/. Set it in the
    # user config so every project shares one log, and precedent carries across projects.
    log_dir: str | None = None

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


def config_path(project_root: Path) -> Path | None:
    """The project's gate.yml, else the user's, else None (defaults)."""
    for path in (project_root / CONFIG_PATH, USER_CONFIG_PATH):
        if path.is_file():
            return path
    return None


def load_config(project_root: Path) -> GateConfig:
    path = config_path(project_root)
    if path is None:
        return GateConfig()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return GateConfig.model_validate(data)


EXAMPLE_CONFIG = """\
# deliberator gate: yes/no decisions for Claude Code tool calls.
provider: bedrock            # bedrock | anthropic | claude-code | mock
# model: anthropic.claude-opus-5-5
effort: low                  # thinking effort; low keeps hooks fast
aws_profile: null            # the AWS profile with Bedrock access
aws_region: us-east-1
rules:
  - Deny anything that deletes or overwrites uncommitted or unpushed work.
  - Deny force-pushes, history rewrites or deletes on main, master or shared branches.
  - Deny commands that send secrets, keys or credentials anywhere, or print them.
  - Ask before changing anything outside the current project.
  - Ask before anything that publishes (git push, publish, deploy, messages).
  - Allow routine development inside the project.
allow_without_asking:
  - '^(ls|pwd|cat|head|tail|wc|grep|rg|find)\\b'
  - '^git (status|diff|log|show|branch)\\b'
precedents: 6
reuse_identical: true
learn_from_approvals: true
graph_uri: null              # e.g. bolt://localhost:7687 (Memgraph)
allow_edits_in_project: true # edits inside the working folder skip the model
log_dir: null                # e.g. ~/.local/share/deliberator: one log for every project
"""
