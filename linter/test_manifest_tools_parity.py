"""Parity test — manifest.json tools[] matches projector output.

Constitution Principle XXII (Distribution Surface Integrity, v2.3.0)
requires single-source declaration of distribution artifacts. The MCPB
bundle's manifest.json carries a `tools[]` array that mirrors the four
hand-coded `@mcp.tool()` decorations + capability-registry-discovered
tools.

This test is the **drift guard**: if a developer adds a `Capability`
with `Surface.MCPB` but forgets to regenerate the manifest, this test
trips. If a developer hand-edits the manifest's `tools[]` (which the
constitution prohibits), this test trips.

The fix-it message is the regeneration command — see test failure
output.
"""

from __future__ import annotations

import json
from pathlib import Path

from capabilities import CAPABILITIES
from conversus.registry.projector import project_to_mcpb_manifest_tools


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "desktop-extension" / "manifest.json"


def test_manifest_tools_matches_projector() -> None:
    """The committed manifest's tools[] must equal the projector output.

    On failure, regenerate the manifest with::

        python -c "
        import json
        from pathlib import Path
        from capabilities import CAPABILITIES
        from conversus.registry.projector import project_to_mcpb_manifest_tools
        m = json.loads(Path('desktop-extension/manifest.json').read_text())
        m['tools'] = [dict(e) for e in project_to_mcpb_manifest_tools(CAPABILITIES)]
        Path('desktop-extension/manifest.json').write_text(json.dumps(m, indent=2) + '\n')
        "

    Or run ``./desktop-extension/build.sh`` which performs the same sync
    in-place (idempotent — only writes on drift).
    """
    projected = [dict(entry) for entry in project_to_mcpb_manifest_tools(CAPABILITIES)]
    committed = json.loads(MANIFEST.read_text())["tools"]

    assert committed == projected, (
        f"manifest.json tools[] is out of sync with the capability registry.\n"
        f"  committed: {len(committed)} tools — {[t['name'] for t in committed]}\n"
        f"  projector: {len(projected)} tools — {[t['name'] for t in projected]}\n"
        f"Regenerate via ./desktop-extension/build.sh (or see this test's "
        f"docstring for an inline regeneration command)."
    )


def test_every_mcpb_capability_appears_in_manifest() -> None:
    """Every Surface.MCPB capability in the registry has a manifest entry.

    Belt-and-suspenders check: the parity test above already covers this
    via equality, but a separate test reports a more readable failure
    message when a single capability is missing (vs reporting "lists
    not equal" which forces a manual diff).
    """
    from conversus.registry import Surface

    expected_names = {
        "conversus_" + cap.name.replace("-", "_")
        for cap in CAPABILITIES
        if Surface.MCPB in cap.surfaces
    }
    committed_names = {
        tool["name"] for tool in json.loads(MANIFEST.read_text())["tools"]
    }

    missing = expected_names - committed_names
    extra = committed_names - expected_names

    assert not missing, (
        f"manifest.json missing {len(missing)} MCPB capability(ies): "
        f"{sorted(missing)}. Regenerate via ./desktop-extension/build.sh."
    )
    assert not extra, (
        f"manifest.json has {len(extra)} hand-edited tool(s) not in the "
        f"capability registry: {sorted(extra)}. Hand-editing manifest.json "
        f"tools[] is prohibited by Principle XXII (Distribution Surface "
        f"Integrity). Add the corresponding Capability to capabilities.py "
        f"or remove the tool entry."
    )
