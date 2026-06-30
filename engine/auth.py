"""Credential storage, OAuth PKCE flows, and provider resolution.

Provides:
- ``CredentialStore``: per-provider token persistence in ``~/.deliberator/credentials/{provider}.json``
- ``login`` / ``logout`` / ``get_credentials`` / ``refresh_token``: OAuth lifecycle
- ``resolve_provider``: factory that maps provider name + credentials → ``ModelProvider``

Spec 057 SC-004: each provider's credentials live in their own file under
``~/.deliberator/credentials/`` rather than the legacy monolithic
``~/.deliberator/auth.json``. ``CredentialStore`` lazily migrates from the legacy
file on first read so existing OAuth users keep working with no manual action.
The legacy file is preserved on disk after migration (users can ``rm`` it
themselves); writes never touch it.
"""

from __future__ import annotations

import base64
import errno
import hashlib
import json
import logging
import os
import secrets
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import click
import httpx

from engine.providers import MockProvider, ModelProvider, ProviderError

# fcntl is POSIX-only — wrap import for Windows support.
# TODO: cross-platform locking (msvcrt.locking or portalocker) when Windows is
# supported as a first-class target. For now, Windows skips locking — atomic
# replace still guarantees the final file is consistent, only concurrent writers
# may race on the *.tmp filename.
try:
    import fcntl  # type: ignore[import-not-found]

    _HAS_FCNTL = True
except ImportError:  # pragma: no cover — Windows
    fcntl = None  # type: ignore[assignment]
    _HAS_FCNTL = False

logger = logging.getLogger("deliberator.auth")

# ---------------------------------------------------------------------------
# OAuth provider constants
# ---------------------------------------------------------------------------

# Default OAuth client ID for the Deliberator public app.
# Override via DELIBERATOR_ANTHROPIC_CLIENT_ID env var for custom deployments.
_DEFAULT_ANTHROPIC_CLIENT_ID = base64.b64decode(
    "OWQxYzI1MGEtZTYxYi00NGQ5LTg4ZWQtNTk0NGQxOTYyZjVl"
).decode()

OAUTH_CONFIGS: dict[str, dict[str, str]] = {
    "anthropic": {
        "client_id": os.environ.get(
            "DELIBERATOR_ANTHROPIC_CLIENT_ID",
            _DEFAULT_ANTHROPIC_CLIENT_ID,
        ),
        "authorize_url": "https://claude.ai/oauth/authorize",
        "token_url": "https://platform.claude.com/v1/oauth/token",
        "redirect_uri": "https://platform.claude.com/oauth/code/callback",
        "scopes": "org:create_api_key user:profile user:inference",
        "flow_type": "code_paste",
        "env_var": "ANTHROPIC_API_KEY",
    },
    "openai": {
        "client_id": "app_EMoamEEZ73f0CkXaXp7hrann",
        "authorize_url": "https://auth.openai.com/authorize",
        "token_url": "https://auth.openai.com/oauth/token",
        "env_var": "OPENAI_API_KEY",
    },
}

DEFAULT_AUTH_PATH = Path.home() / ".deliberator" / "auth.json"
DEFAULT_CREDENTIALS_DIR = Path.home() / ".deliberator" / "credentials"
CALLBACK_TIMEOUT = 120  # seconds


# ---------------------------------------------------------------------------
# Atomic write helper
# ---------------------------------------------------------------------------


def _flock_with_timeout(fd: int, timeout_ms: int = 200) -> None:
    """Acquire ``LOCK_EX`` non-blocking on *fd*, retrying up to *timeout_ms*.

    Per the spec 057 SC-004 deliberation verdict
    (``deliberations/057-sc4-migration-strategy-2026-04-30/arbitration/resolution.md``)
    writes to a per-provider credential file must use a non-blocking, bounded
    file lock. Two ``deliberator`` invocations writing the same provider at the
    same time should serialize, not interleave; the bounded timeout prevents a
    crashed/hung writer from indefinitely blocking the second writer.

    No-op on platforms without ``fcntl`` (Windows). The atomic ``os.replace``
    still guarantees the final file is consistent — concurrent writers there
    may race only on the ``.tmp`` filename.
    """
    if not _HAS_FCNTL:
        return
    deadline = time.monotonic() + (timeout_ms / 1000.0)
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except BlockingIOError:
            if time.monotonic() >= deadline:
                raise BlockingIOError(
                    errno.EWOULDBLOCK,
                    f"Could not acquire credential file lock within {timeout_ms}ms",
                )
            time.sleep(0.01)


def _atomic_write_json(path: Path, data: dict[str, Any], mode: int = 0o600) -> None:
    """Write *data* to *path* atomically with restrictive permissions.

    Writes to ``{path}.tmp`` first (opened with ``O_TRUNC`` semantics via
    Python's ``"w"`` mode — see verdict §"O_TRUNC over O_EXCL"), acquires a
    bounded ``fcntl.LOCK_EX`` lock for concurrency safety, sets ``mode`` on
    the tmp file *before* the rename (so the file is never world-readable in
    plaintext, even briefly), then ``os.replace`` to swap into place. Survives
    a crash mid-write — the final path either holds the previous contents or
    the new ones, never a partial JSON document. If any error occurs between
    open and replace, the ``.tmp`` file is removed in ``finally``.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.parent.chmod(0o700)
    except OSError:
        # Some filesystems / mocks may reject chmod on the parent; the
        # per-file mode below is the load-bearing protection.
        pass
    tmp = path.with_suffix(path.suffix + ".tmp")
    payload = json.dumps(data, indent=2)
    try:
        # ``"w"`` opens with O_TRUNC (Python's default for text-write) — per
        # verdict, preferred over O_EXCL because the .tmp slot may legitimately
        # exist from a prior crashed write and overwriting it is safe.
        with open(tmp, "w", encoding="utf-8") as f:
            _flock_with_timeout(f.fileno(), timeout_ms=200)
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
            # chmod must happen before replace so the swapped-in file is never
            # world-readable in plaintext, even briefly.
            os.chmod(tmp, mode)
        # Lock released implicitly when the file descriptor closed above.
        os.replace(tmp, path)
    except Exception:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        raise


# ---------------------------------------------------------------------------
# Credential store
# ---------------------------------------------------------------------------


class CredentialStore:
    """Read/write per-provider OAuth tokens in ``~/.deliberator/credentials/``.

    Each provider lives in its own file at ``{credentials_dir}/{provider}.json``
    holding only that provider's credential dict (not a nested
    ``{provider: dict}`` mapping). Files are written atomically and ``chmod
    600``-ed before the rename to keep secrets unreadable to other users.

    The legacy monolithic ``~/.deliberator/auth.json`` is read on a fallback path:
    if a per-provider file is missing on first ``get()``, the credentials are
    lazily migrated from the legacy file (if present) to the per-provider
    location. The legacy file is preserved on disk afterward.

    ``path`` parameter is preserved for backwards compatibility with code that
    used to override the legacy auth file path. It still controls where the
    legacy file is read from for migration purposes.
    """

    def __init__(
        self,
        path: Path | None = None,
        *,
        credentials_dir: Path | None = None,
    ) -> None:
        # ``path`` keeps the legacy keyword argument name some callers
        # (CLI tests, integration tests, older docs) still use. It now refers
        # solely to the legacy auth.json read path used during lazy migration.
        self.path = path or DEFAULT_AUTH_PATH
        self._credentials_dir_override = credentials_dir

    @property
    def credentials_dir(self) -> Path:
        """Directory holding per-provider credential files.

        Resolved lazily so monkeypatching ``DEFAULT_CREDENTIALS_DIR`` (mirrors
        how existing tests monkeypatch ``DEFAULT_AUTH_PATH``) works without
        re-instantiating the store.
        """
        if self._credentials_dir_override is not None:
            return self._credentials_dir_override
        return DEFAULT_CREDENTIALS_DIR

    def _credential_path(self, provider: str) -> Path:
        """Return ``{credentials_dir}/{provider}.json``."""
        return self.credentials_dir / f"{provider}.json"

    def _read_legacy_all(self) -> dict[str, Any]:
        """Read the legacy ``auth.json``, returning ``{}`` if missing or invalid."""
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _read_provider_file(self, provider: str) -> dict[str, Any] | None:
        """Read a per-provider file, returning ``None`` if missing or invalid."""
        cred_path = self._credential_path(provider)
        if not cred_path.exists():
            return None
        try:
            return json.loads(cred_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def get(self, provider: str) -> dict[str, Any] | None:
        """Return stored credentials for *provider*, or ``None``.

        Reads the per-provider file first. If the per-provider file is missing
        but the legacy ``auth.json`` contains the provider, lazily migrates the
        credentials to the new location before returning. The legacy file is
        not touched.
        """
        per_provider = self._read_provider_file(provider)
        if per_provider is not None:
            return per_provider

        # Per-provider file missing — fall back to legacy auth.json and migrate.
        # DEBUG-level so quiet by default but visible to anyone investigating
        # an unexpected migration. Stateless — fires every fallback (verdict
        # §"DEBUG fallback log").
        logger.debug(
            "credentials/%s.json not found; reading from legacy auth.json. "
            "Run 'deliberator migrate-credentials' to migrate.",
            provider,
        )
        legacy = self._read_legacy_all()
        legacy_creds = legacy.get(provider)
        if legacy_creds is None:
            return None

        # Lazy-migrate: write to per-provider file but leave auth.json alone.
        try:
            _atomic_write_json(self._credential_path(provider), legacy_creds)
        except OSError as exc:
            # If migration write fails (read-only fs, etc.) we still want the
            # caller to receive the credentials — degrade gracefully.
            logger.warning(
                "Lazy migration for %s failed (%s); returning legacy creds without persisting.",
                provider,
                exc,
            )
        return legacy_creds

    def set(self, provider: str, credentials: dict[str, Any]) -> None:
        """Persist *credentials* to the per-provider file.

        Writes are atomic (tmp + ``os.replace``) and the resulting file is
        ``chmod 600``. The legacy ``auth.json`` is never touched.
        """
        _atomic_write_json(self._credential_path(provider), credentials)

    # ``save`` is preserved as an alias so internal callers (login flows,
    # refresh_token, OAuth provider implementations) and existing tests keep
    # working without churn. ``set`` is the spec-mandated name.
    save = set

    def delete(self, provider: str) -> None:
        """Remove the per-provider file for *provider*.

        Does not touch the legacy ``auth.json`` — users can ``rm`` it manually
        once they're confident the migration succeeded.
        """
        cred_path = self._credential_path(provider)
        if cred_path.exists():
            cred_path.unlink()

    def clear(self) -> None:
        """Delete every per-provider file and the legacy ``auth.json``.

        Used by ``logout --all``-style operations. ``clear`` is the only
        method that touches the legacy file, because the user has explicitly
        asked to remove all credentials.
        """
        if self.credentials_dir.exists():
            for entry in self.credentials_dir.iterdir():
                if entry.is_file() and entry.suffix == ".json":
                    try:
                        entry.unlink()
                    except OSError:
                        pass
        if self.path.exists():
            try:
                self.path.unlink()
            except OSError:
                pass

    def list_providers(self) -> list[str]:
        """Return the union of providers with a per-provider file or a legacy entry."""
        providers: set[str] = set()
        if self.credentials_dir.exists():
            for entry in self.credentials_dir.iterdir():
                if entry.is_file() and entry.suffix == ".json":
                    providers.add(entry.stem)
        legacy = self._read_legacy_all()
        providers.update(legacy.keys())
        return sorted(providers)


# ---------------------------------------------------------------------------
# Source attribution (spec 072 SC-005)
# ---------------------------------------------------------------------------


def inspect_credential_source(
    provider: str,
    store: CredentialStore | None = None,
) -> tuple[str, Path | None]:
    """Return ``(source_label, source_path)`` for *provider*'s effective credentials.

    Source labels:

    - ``"per-provider-file"`` — ``credentials/{provider}.json`` exists and
      contains an ``access_token``. ``source_path`` is the per-provider file.
    - ``"legacy-fallback"`` — per-provider file is missing/empty and the
      legacy ``auth.json`` contains a provider entry with ``access_token``.
      ``source_path`` is the legacy auth file.
    - ``"env-var"`` — neither file path supplies credentials and
      ``OAUTH_CONFIGS[provider]["env_var"]`` is set in ``os.environ``.
      ``source_path`` is ``None`` (env vars have no on-disk location).
    - ``"none"`` — no credentials are available from any source.

    Resolution order for files mirrors ``CredentialStore.get()``: per-provider
    beats legacy. Env-var detection uses the OAuth config map only — a provider
    not registered in ``OAUTH_CONFIGS`` simply cannot resolve to ``env-var``.

    This is an inspection helper for ``deliberator status`` (spec 072 SC-005);
    it is intentionally read-only and **does not** trigger the lazy-migration
    write that ``CredentialStore.get()`` performs.
    """
    store = store or CredentialStore()

    # 1. Per-provider file with an access_token wins.
    per_provider = store._read_provider_file(provider)
    if per_provider is not None and per_provider.get("access_token"):
        return "per-provider-file", store._credential_path(provider)

    # 2. Legacy auth.json fallback.
    legacy = store._read_legacy_all()
    legacy_creds = legacy.get(provider) if isinstance(legacy, dict) else None
    if isinstance(legacy_creds, dict) and legacy_creds.get("access_token"):
        return "legacy-fallback", store.path

    # 3. Environment variable.
    config = OAUTH_CONFIGS.get(provider)
    if config is not None:
        env_var = config.get("env_var")
        if env_var and os.environ.get(env_var):
            return "env-var", None

    # 4. Nothing configured.
    return "none", None


# ---------------------------------------------------------------------------
# Startup migration sweep (spec 057 SC-004 verdict)
# ---------------------------------------------------------------------------


def log_unmigrated_credentials_sweep() -> None:
    """Diff legacy ``auth.json`` against ``credentials/`` files; log if any unmigrated.

    Stateless. Fires once per CLI invocation (wired into the ``cli`` group
    callback). No sentinel file, no in-memory dedup — re-running the CLI is
    the only way to re-emit, so the sweep can't drift out of sync with disk
    state. Per spec 057 SC-004 deliberation verdict 2026-04-30
    (``deliberations/057-sc4-migration-strategy-2026-04-30/arbitration/resolution.md``).

    Best-effort: any I/O error (auth.json unreadable, credentials dir missing)
    fails silent. The sweep is observability, not a precondition.
    """
    try:
        legacy_path = DEFAULT_AUTH_PATH
        if not legacy_path.exists():
            return
        try:
            legacy_data = json.loads(legacy_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        if not isinstance(legacy_data, dict) or not legacy_data:
            return
        legacy_providers = set(legacy_data.keys())

        migrated: set[str] = set()
        cred_dir = DEFAULT_CREDENTIALS_DIR
        if cred_dir.exists():
            for entry in cred_dir.iterdir():
                if entry.is_file() and entry.suffix == ".json":
                    migrated.add(entry.stem)

        unmigrated = sorted(legacy_providers - migrated)
        if unmigrated:
            logger.debug(
                "Unmigrated credential providers found in auth.json: %s. "
                "These will migrate lazily on first use.",
                unmigrated,
            )
    except Exception:  # pragma: no cover — defensive, sweep must never raise
        return


# ---------------------------------------------------------------------------
# PKCE helpers
# ---------------------------------------------------------------------------


def _generate_pkce() -> tuple[str, str]:
    """Generate a PKCE code verifier and S256 code challenge.

    Returns:
        ``(code_verifier, code_challenge)``
    """
    verifier = secrets.token_urlsafe(64)  # ≥43 chars per RFC 7636
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


# ---------------------------------------------------------------------------
# Local callback server
# ---------------------------------------------------------------------------


class _CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler that captures the ``code`` query parameter."""

    authorization_code: str | None = None

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        codes = params.get("code")
        if codes:
            _CallbackHandler.authorization_code = codes[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authorization successful</h1>"
                b"<p>You can close this tab.</p></body></html>"
            )
        else:
            error = params.get("error", ["unknown"])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<html><body><h1>Authorization failed: {error}</h1></body></html>".encode()
            )

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """Suppress default stderr logging from the HTTP server."""


def _run_callback_server(port: int = 0) -> tuple[str, int]:
    """Start a local HTTP server, wait for the OAuth callback, return the authorization code.

    Args:
        port: Port to listen on (0 = auto-assign).

    Returns:
        ``(authorization_code, port_used)``

    Raises:
        ProviderError: If the callback times out or no code is received.
    """
    _CallbackHandler.authorization_code = None
    server = HTTPServer(("localhost", port), _CallbackHandler)
    actual_port = server.server_address[1]

    def serve() -> None:
        server.handle_request()

    thread = Thread(target=serve, daemon=True)
    thread.start()
    thread.join(timeout=CALLBACK_TIMEOUT)

    server.server_close()

    code = _CallbackHandler.authorization_code
    if code is None:
        raise ProviderError(
            "OAuth callback timed out — no authorization code received.",
            category="auth",
        )
    return code, actual_port


# ---------------------------------------------------------------------------
# Token helpers
# ---------------------------------------------------------------------------


def _redact(token: str) -> str:
    """Redact a token to first/last 4 characters for safe logging."""
    if len(token) <= 8:
        return "***"
    return f"{token[:4]}...{token[-4:]}"


# ---------------------------------------------------------------------------
# Anthropic code-paste OAuth flow
# ---------------------------------------------------------------------------


def _exchange_code_json(
    token_url: str,
    *,
    code: str,
    redirect_uri: str,
    code_verifier: str,
    client_id: str,
    state: str,
) -> dict[str, Any]:
    """Exchange an authorization code for tokens via JSON POST (Anthropic).

    Anthropic requires ``json={...}`` (not form-encoded ``data={...}``) and
    includes the ``state`` parameter in the body.
    """
    response = httpx.post(
        token_url,
        json={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
            "client_id": client_id,
            "state": state,
        },
    )
    if response.status_code != 200:
        raise ProviderError(
            f"Anthropic token exchange failed (HTTP {response.status_code}): {response.text}",
            category="auth",
        )
    return response.json()


def _login_anthropic(
    store: CredentialStore | None = None,
    *,
    _open_browser: Any = None,
    _prompt_code: Any = None,
    _exchange_token: Any = None,
) -> dict[str, Any]:
    """Perform Anthropic OAuth login via the code-paste flow.

    Unlike OpenAI (which uses a localhost callback server), Anthropic shows the
    authorization code on ``platform.claude.com/oauth/code/callback`` and the
    user pastes it into the terminal.  The pasted value has the format
    ``code#state``.

    Parameters ``_open_browser``, ``_prompt_code``, and ``_exchange_token`` are
    injectable for testing.
    """
    store = store or CredentialStore()
    config = OAUTH_CONFIGS["anthropic"]
    verifier, challenge = _generate_pkce()
    state = secrets.token_urlsafe(32)

    # Build authorization URL
    params = {
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "scope": config["scopes"],
        "code": "true",
        "state": state,
    }
    auth_url = f"{config['authorize_url']}?{urlencode(params)}"

    # Open browser
    open_fn = _open_browser or webbrowser.open
    open_fn(auth_url)

    # Prompt user to paste code#state
    prompt_fn = _prompt_code or (lambda: click.prompt("Paste the authorization code"))
    raw_code = prompt_fn()

    # Parse code#state
    if "#" not in raw_code:
        raise ProviderError(
            "Invalid authorization code format — expected 'code#state' but no '#' found.",
            category="auth",
        )
    code, state_returned = raw_code.split("#", 1)

    # Validate state to prevent CSRF. This is critical if the flow ever
    # migrates to redirect-based auth (FR-017). See PR #2 deliberation SC-5.
    if state_returned != state:
        raise ProviderError(
            "OAuth state mismatch — the returned state does not match the "
            "locally generated value. This may indicate a CSRF attempt.",
            category="auth",
        )

    # Exchange code for tokens
    if _exchange_token:
        token_data = _exchange_token(
            config["token_url"],
            code=code,
            redirect_uri=config["redirect_uri"],
            code_verifier=verifier,
            client_id=config["client_id"],
            state=state_returned,
        )
    else:
        token_data = _exchange_code_json(
            config["token_url"],
            code=code,
            redirect_uri=config["redirect_uri"],
            code_verifier=verifier,
            client_id=config["client_id"],
            state=state_returned,
        )

    # Build credentials with 5-minute safety buffer on expiry
    expires_in = token_data.get("expires_in", 3600)
    credentials = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token", ""),
        "expires_at": int(time.time()) + expires_in - 300,
        "token_type": token_data.get("token_type", "bearer"),
    }

    store.save("anthropic", credentials)
    logger.info(
        "Login successful for anthropic (token: %s)",
        _redact(credentials["access_token"]),
    )
    return credentials


# ---------------------------------------------------------------------------
# OAuth lifecycle
# ---------------------------------------------------------------------------


def login(
    provider: str,
    store: CredentialStore | None = None,
    *,
    _open_browser: Any = None,
    _run_server: Any = None,
    _exchange_token: Any = None,
    _prompt_code: Any = None,
) -> dict[str, Any]:
    """Perform an OAuth PKCE login for *provider*.

    Opens the browser to the provider's authorization URL, waits for the
    local callback (OpenAI) or prompts for a pasted code (Anthropic),
    exchanges the code for tokens, and stores them.

    The ``_open_browser``, ``_run_server``, ``_exchange_token``, and
    ``_prompt_code`` parameters exist solely for testing.

    Returns:
        The stored credentials dict.

    Raises:
        ProviderError: If the provider is unknown or the flow fails.
    """
    if provider not in OAUTH_CONFIGS:
        raise ProviderError(
            f"Unknown provider: '{provider}'. Must be one of: {', '.join(OAUTH_CONFIGS)}.",
            category="auth",
        )

    # Anthropic uses a code-paste flow, not localhost callback
    if provider == "anthropic":
        return _login_anthropic(
            store=store,
            _open_browser=_open_browser,
            _prompt_code=_prompt_code,
            _exchange_token=_exchange_token,
        )

    store = store or CredentialStore()
    config = OAUTH_CONFIGS[provider]
    verifier, challenge = _generate_pkce()

    # Start callback server
    run_server = _run_server or _run_callback_server
    code, port = run_server(0) if _run_server else (None, 0)

    # If using the real server, we need to start it in background first
    if _run_server is None:
        # Start server in background thread, then open browser
        _CallbackHandler.authorization_code = None
        server = HTTPServer(("localhost", 0), _CallbackHandler)
        port = server.server_address[1]

        def serve() -> None:
            server.handle_request()

        thread = Thread(target=serve, daemon=True)
        thread.start()

        # Build auth URL and open browser
        redirect_uri = f"http://localhost:{port}/callback"
        params = {
            "response_type": "code",
            "client_id": config["client_id"],
            "redirect_uri": redirect_uri,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "scope": "openid",
        }
        auth_url = f"{config['authorize_url']}?{urlencode(params)}"
        open_fn = _open_browser or webbrowser.open
        open_fn(auth_url)

        thread.join(timeout=CALLBACK_TIMEOUT)
        server.server_close()

        code = _CallbackHandler.authorization_code
        if code is None:
            raise ProviderError(
                "OAuth callback timed out — no authorization code received.",
                category="auth",
            )
    else:
        # Test path: server mock returned code directly
        redirect_uri = f"http://localhost:{port}/callback"
        params = {
            "response_type": "code",
            "client_id": config["client_id"],
            "redirect_uri": redirect_uri,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "scope": "openid",
        }
        auth_url = f"{config['authorize_url']}?{urlencode(params)}"
        open_fn = _open_browser or webbrowser.open
        open_fn(auth_url)

    # Exchange code for tokens
    if _exchange_token:
        token_data = _exchange_token(
            config["token_url"],
            code=code,
            redirect_uri=redirect_uri,
            code_verifier=verifier,
            client_id=config["client_id"],
        )
    else:
        token_data = _exchange_code(
            config["token_url"],
            code=code,
            redirect_uri=redirect_uri,
            code_verifier=verifier,
            client_id=config["client_id"],
        )

    credentials = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token", ""),
        "expires_at": int(time.time()) + token_data.get("expires_in", 3600),
        "token_type": token_data.get("token_type", "bearer"),
    }

    store.save(provider, credentials)
    logger.info("Login successful for %s (token: %s)", provider, _redact(credentials["access_token"]))
    return credentials


def _exchange_code(
    token_url: str,
    *,
    code: str,
    redirect_uri: str,
    code_verifier: str,
    client_id: str,
) -> dict[str, Any]:
    """Exchange an authorization code for tokens via HTTP POST."""
    response = httpx.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
            "client_id": client_id,
        },
    )
    if response.status_code != 200:
        raise ProviderError(
            f"Token exchange failed (HTTP {response.status_code}): {response.text}",
            category="auth",
        )
    return response.json()


def logout(provider: str, store: CredentialStore | None = None) -> None:
    """Remove stored credentials for *provider*."""
    store = store or CredentialStore()
    store.delete(provider)
    logger.info("Logged out of %s", provider)


def get_credentials(provider: str, store: CredentialStore | None = None) -> dict[str, Any] | None:
    """Retrieve stored credentials for *provider*, or ``None``."""
    store = store or CredentialStore()
    return store.get(provider)


def refresh_token(
    provider: str,
    store: CredentialStore | None = None,
    *,
    _post: Any = None,
) -> dict[str, Any] | None:
    """Refresh the access token for *provider* if expired.

    Returns:
        Updated credentials if refresh succeeded, or ``None`` if no refresh
        token is available.

    Raises:
        ProviderError: If the refresh request fails.
    """
    if provider not in OAUTH_CONFIGS:
        raise ProviderError(
            f"Unknown provider: '{provider}'.",
            category="auth",
        )

    store = store or CredentialStore()
    creds = store.get(provider)
    if not creds or not creds.get("refresh_token"):
        return None

    # Only refresh if expired (or within 60s of expiry)
    expires_at = creds.get("expires_at", 0)
    if time.time() < expires_at - 60:
        return creds  # Still valid

    config = OAUTH_CONFIGS[provider]
    post_fn = _post or httpx.post

    # Anthropic requires JSON POST for token refresh; others use form-encoded
    if provider == "anthropic":
        payload_kwargs = {
            "json": {
                "grant_type": "refresh_token",
                "refresh_token": creds["refresh_token"],
                "client_id": config["client_id"],
            }
        }
    else:
        payload_kwargs = {
            "data": {
                "grant_type": "refresh_token",
                "refresh_token": creds["refresh_token"],
                "client_id": config["client_id"],
            }
        }

    try:
        response = post_fn(config["token_url"], **payload_kwargs)
    except Exception as exc:
        logger.error("Token refresh failed for %s: %s", provider, exc)
        raise ProviderError(
            f"Token refresh failed for {provider}: {exc}",
            category="auth",
            original=exc,
        ) from exc

    if hasattr(response, "status_code") and response.status_code != 200:
        logger.error("Token refresh HTTP error for %s: %s", provider, response.status_code)
        raise ProviderError(
            f"Token refresh failed for {provider} (HTTP {response.status_code})",
            category="auth",
        )

    token_data = response.json() if hasattr(response, "json") else response

    updated = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token", creds["refresh_token"]),
        "expires_at": int(time.time()) + token_data.get("expires_in", 3600),
        "token_type": token_data.get("token_type", "bearer"),
    }

    store.save(provider, updated)
    logger.info("Token refreshed for %s (token: %s)", provider, _redact(updated["access_token"]))
    return updated


# ---------------------------------------------------------------------------
# Provider resolution
# ---------------------------------------------------------------------------


def resolve_provider(
    provider_name: str,
    credential_store: CredentialStore | None = None,
) -> ModelProvider:
    """Instantiate the correct ``ModelProvider`` for *provider_name*.

    Resolution order:
    1. Environment variable (``ANTHROPIC_API_KEY`` / ``OPENAI_API_KEY``)
    2. Stored OAuth credentials from ``CredentialStore``
    3. Raise ``ProviderError(category="auth")`` with a helpful message

    The ``"mock"`` provider is always available without credentials.

    Raises:
        ProviderError: If no credentials are available for *provider_name*.
    """
    if provider_name in ("mock", "demo"):
        return MockProvider()

    if provider_name not in OAUTH_CONFIGS:
        raise ProviderError(
            f"Unknown provider: '{provider_name}'. "
            f"Must be one of: {', '.join(OAUTH_CONFIGS)}, mock.",
            category="auth",
        )

    config = OAUTH_CONFIGS[provider_name]
    env_key = os.environ.get(config["env_var"])

    # Path 1: env var
    if env_key:
        if provider_name == "anthropic":
            from engine.providers.anthropic import AnthropicProvider
            return AnthropicProvider()
        else:
            from engine.providers.openai import OpenAIProvider
            return OpenAIProvider()

    # Path 2: stored OAuth credentials
    store = credential_store or CredentialStore()
    creds = store.get(provider_name)
    if creds and creds.get("access_token"):
        token = creds["access_token"]
        if provider_name == "anthropic":
            from engine.providers.anthropic import AnthropicProvider
            return AnthropicProvider(auth_token=token)
        else:
            from engine.providers.openai import OpenAIProvider
            return OpenAIProvider(api_key=token)

    # Path 3: no credentials
    raise ProviderError(
        f"No credentials available for '{provider_name}'. "
        f"Set the {config['env_var']} environment variable or run "
        f"`deliberator login {provider_name}` to authenticate via OAuth.",
        category="auth",
    )
