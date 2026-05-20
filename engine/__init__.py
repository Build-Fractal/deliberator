"""Conversus multi-agent deliberation engine.

Orchestrates competitive LLM agents through structured phases (review,
cross-review, revision, disputes, synthesis) using configurable game-theory
competition modes.
"""

__version__ = "0.4.0"

from engine.sdk import Deliberation, Result, classify, validate
