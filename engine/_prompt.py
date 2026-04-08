"""Shared prompt assembly helpers.

Extracted from ``engine.run`` to break circular imports between
``engine.run`` and ``engine.phases``.
"""

from __future__ import annotations

import warnings
from pathlib import Path

# ---------------------------------------------------------------------------
# Prompt content size limit (characters)
# ---------------------------------------------------------------------------

INLINE_CONTENT_WARN_LIMIT = 150_000


# ---------------------------------------------------------------------------
# File inlining
# ---------------------------------------------------------------------------


def _read_file_safe(path: Path) -> str | None:
    """Read a file, returning None if it doesn't exist or can't be read."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        warnings.warn(f"Cannot read file {path}: {exc}", stacklevel=2)
        return None


def _collect_files_from_path(path: Path) -> list[Path]:
    """Collect readable files from a path (file or directory).

    If path is a directory, returns all .md files sorted.
    If path is a file, returns it in a single-element list.
    """
    if path.is_dir():
        return sorted(path.glob("*.md"))
    elif path.is_file():
        return [path]
    return []


def _inline_files(files: list[Path], base_dir: Path | None = None) -> str:
    """Inline file contents in a delimited format for prompt assembly.

    Args:
        files: List of file or directory paths to inline.
        base_dir: Optional base directory for relative path display.

    Returns:
        Concatenated file sections, each wrapped in delimiters.
    """
    sections: list[str] = []
    for entry in files:
        actual_files = _collect_files_from_path(entry)
        for file_path in actual_files:
            content = _read_file_safe(file_path)
            if content is None:
                continue
            if base_dir:
                try:
                    display_path = file_path.relative_to(base_dir)
                except ValueError:
                    display_path = file_path
            else:
                display_path = file_path
            sections.append(
                f"--- FILE: {display_path} ---\n{content}\n--- END FILE ---\n"
            )
    return "\n".join(sections)


def _assemble_prompt(
    filled_template: str,
    target_files: list[Path],
    agent_docs: list[Path],
    base_dir: Path | None = None,
) -> str:
    """Assemble a complete prompt with inlined file contents.

    Per D011 (prompt-only dispatch), all file contents are inlined in the
    prompt rather than relying on agents reading files themselves.

    Format:
        1. Target file contents (delimited)
        2. Agent doc contents (delimited)
        3. Filled template

    Args:
        filled_template: The template with all {VARIABLE} placeholders filled.
        target_files: Target files to inline.
        agent_docs: Agent-specific documentation files to inline.
        base_dir: Base directory for computing relative display paths.

    Returns:
        The complete assembled prompt string.
    """
    parts: list[str] = []

    # Inline target files
    target_section = _inline_files(target_files, base_dir)
    if target_section:
        parts.append(target_section)

    # Inline agent doc files
    doc_section = _inline_files(agent_docs, base_dir)
    if doc_section:
        parts.append(doc_section)

    # Append the filled template
    parts.append(filled_template)

    prompt = "\n\n".join(parts)

    # Warn if the prompt exceeds the size limit
    if len(prompt) > INLINE_CONTENT_WARN_LIMIT:
        warnings.warn(
            f"Assembled prompt is {len(prompt):,} characters "
            f"(exceeds {INLINE_CONTENT_WARN_LIMIT:,} limit). "
            "Large prompts may approach context window limits.",
            stacklevel=2,
        )

    return prompt
