#!/usr/bin/env python3
"""Validate desktop-extension/manifest.json against the official MCPB schema."""
import json, sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("pip install jsonschema", file=sys.stderr)
    sys.exit(1)

repo = Path(__file__).parent.parent
schema = json.loads((repo / "desktop-extension/mcpb-manifest.schema.json").read_text())
manifest = json.loads((repo / "desktop-extension/manifest.json").read_text())

try:
    validate(instance=manifest, schema=schema)
    print("✓ manifest.json is valid")
except ValidationError as e:
    print(f"✗ {e.message}", file=sys.stderr)
    print(f"  path: {'.'.join(str(p) for p in e.absolute_path)}", file=sys.stderr)
    sys.exit(1)
