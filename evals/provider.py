"""Custom promptfoo provider that calls deliberator decide via subprocess.

Avoids shell quoting issues with exec: providers.
Promptfoo calls call_api(prompt, options, context) and expects {"output": str}.
"""

import json
import subprocess
import os


def call_api(prompt: str, options: dict, context: dict) -> dict:
    """Run deliberator decide and return JSON output."""
    config = options.get("config", {})
    mode = config.get("mode", "cooperative")
    provider = config.get("provider", "mock")

    # Run from the repo root (parent of evals/)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        result = subprocess.run(
            [
                "uv", "run", "deliberator", "decide",
                prompt,
                "--provider", provider,
                "--mode", mode,
                "--format", "json",
            ],
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=120,
        )

        if result.returncode != 0:
            stderr = result.stderr.strip()
            return {
                "output": json.dumps({
                    "error": True,
                    "message": stderr or f"Exit code {result.returncode}",
                    "returncode": result.returncode,
                }),
            }

        return {"output": result.stdout.strip()}

    except subprocess.TimeoutExpired:
        return {
            "output": json.dumps({
                "error": True,
                "message": "Timeout: deliberator decide took >120s",
            }),
        }
    except Exception as e:
        return {
            "output": json.dumps({
                "error": True,
                "message": str(e),
            }),
        }
