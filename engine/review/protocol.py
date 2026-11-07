"""The structured review protocol: roles, phases, vocabulary and token caps, loaded from data.

The protocol file (``schema/protocols/review.yml``) is the "game file" of spec 074 § 7.4. The
engine reads words, caps and roles from it; nothing about what a move is called lives in code.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from engine._root import find_project_root

Severity = Literal["block", "major", "minor"]
Verdict = Literal["pass", "changes", "block"]

_FROZEN = ConfigDict(frozen=True, extra="forbid")


class PhaseSpec(BaseModel):
    model_config = _FROZEN

    role: str
    max_tokens: int = Field(gt=0)
    max_items: int | None = Field(default=None, gt=0)


class RoleSpec(BaseModel):
    model_config = _FROZEN

    phases: tuple[str, ...]


class VocabularySpec(BaseModel):
    model_config = _FROZEN

    labels: dict[str, str]
    edges: dict[str, str]


class Protocol(BaseModel):
    model_config = _FROZEN

    protocol: str
    schema_version: str
    vocabulary: VocabularySpec
    roles: dict[str, RoleSpec]
    phases: dict[str, PhaseSpec]
    text_words: int = Field(gt=0)
    severities: tuple[Severity, ...]
    verdict: dict[Severity, Verdict]

    def word(self, schema_name: str, *, edge: bool = False) -> str:
        """The protocol's word for a schema type (the first alias that maps to it)."""
        table = self.vocabulary.edges if edge else self.vocabulary.labels
        for word, target in table.items():
            if target == schema_name:
                return word
        raise KeyError(f"protocol {self.protocol!r} has no word for {schema_name!r}")


def protocol_path(name: str = "review") -> Path:
    root = find_project_root(marker="schema")
    return root / "schema" / "protocols" / f"{name}.yml"


@lru_cache(maxsize=8)
def load_protocol(path: Path | None = None) -> Protocol:
    """Load and validate a protocol file. Unknown fields are refused."""
    source = path or protocol_path()
    with source.open(encoding="utf-8") as f:
        return Protocol.model_validate(yaml.safe_load(f))
