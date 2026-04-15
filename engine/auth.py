"""Credential storage, OAuth PKCE flows, and provider resolution.

Provides:
- ``CredentialStore``: per-provider token persistence in ``~/.conversus/auth.json``
- ``login`` / ``logout`` / ``get_credentials`` / ``refresh_token``: OAuth lifecycle
- ``resolve_provider``: factory that maps provider name + credentials → ``ModelProvider``
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import secrets
import stat
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

logger = logging.getLogger("conversus.auth")

# ---------------------------------------------------------------------------
# OAuth provider constants
# ---------------------------------------------------------------------------

# Default OAuth client ID for the Conversus public app.
# Override via CONVERSUS_ANTHROPIC_CLIENT_ID env var for custom deployments.
_DEFAULT_ANTHROPIC_CLIENT_ID = base64.b64decode(
    "OWQxYzI1MGEtZTYxYi00NGQ5LTg4ZWQtNTk0NGQxOTYyZjVl"
).decode()

OAUTH_CONFIGS: dict[str, dict[str, str]] = {
    "anthropic": {
        "client_id": os.environ.get(
            "CONVERSUS_ANTHROPIC_CLIENT_ID",
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

DEFAULT_AUTH_PATH = Path.home() / ".conversus" / "auth.json"
CALLBACK_TIMEOUT = 120  # seconds


# ---------------------------------------------------------------------------
# Credential store
# ---------------------------------------------------------------------------


class CredentialStore:
    """Read/write per-provider OAuth tokens in ``~/.conversus/auth.json``.

    The JSON file is ``chmod 600`` after every write to protect secrets.
    """

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DEFAULT_AUTH_PATH

    def _read_all(self) -> dict[str, Any]:
        """Read the entire auth file, returning {} if missing or invalid."""
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_all(self, data: dict[str, Any]) -> None:
        """Write the full data dict and set restrictive permissions."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.path.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 600

    def get(self, provider: str) -> dict[str, Any] | None:
        """Return stored credentials for *provider*, or ``None``."""
        data = self._read_all()
        return data.get(provider)

    def save(self, provider: str, credentials: dict[str, Any]) -> None:
        """Persist *credentials* under *provider*, merging with existing data."""
        data = self._read_all()
        data[provider] = credentials
        self._write_all(data)

    def delete(self, provider: str) -> None:
        """Remove credentials for a single *provider*."""
        data = self._read_all()
        data.pop(provider, None)
        self._write_all(data)

    def clear(self) -> None:
        """Delete the entire auth file."""
        if self.path.exists():
            self.path.unlink()


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
        f"`conversus login {provider_name}` to authenticate via OAuth.",
        category="auth",
    )
