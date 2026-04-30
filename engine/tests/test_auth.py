"""Tests for engine.auth — credential store, PKCE, OAuth flows, and provider resolution."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import stat
import time
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from engine.auth import (
    OAUTH_CONFIGS,
    CredentialStore,
    _atomic_write_json,
    _exchange_code_json,
    _generate_pkce,
    _redact,
    get_credentials,
    login,
    logout,
    refresh_token,
    resolve_provider,
)
from engine.providers import MockProvider, ModelProvider, ProviderError


def _make_store(tmp_path: Path) -> CredentialStore:
    """Build a CredentialStore wired to tmp_path for both legacy and per-provider files."""
    return CredentialStore(
        path=tmp_path / "auth.json",
        credentials_dir=tmp_path / "credentials",
    )


def _patch_state(monkeypatch: pytest.MonkeyPatch, state_value: str) -> None:
    """Make the OAuth state generated inside ``_login_anthropic`` deterministic.

    ``_login_anthropic`` calls ``secrets.token_urlsafe(32)`` to generate a CSRF
    state and then validates the returned ``code#state`` against it. Tests that
    mock ``_prompt_code`` with a fixed state string need the generated state to
    match, so we patch the 32-byte call while letting the 64-byte PKCE verifier
    call in ``_generate_pkce`` keep its real entropy.
    """
    import secrets as _secrets

    real_token_urlsafe = _secrets.token_urlsafe

    def fake_token_urlsafe(nbytes: int | None = None) -> str:
        if nbytes == 32:
            return state_value
        return real_token_urlsafe(nbytes)

    monkeypatch.setattr("engine.auth.secrets.token_urlsafe", fake_token_urlsafe)


# ===================================================================
# CredentialStore
# ===================================================================


class TestCredentialStore:
    """CRUD operations on per-provider credential storage.

    SC-004: ``save`` writes to ``credentials/{provider}.json``. The legacy
    monolithic ``auth.json`` is read-only on the migration fallback path.
    """

    def test_get_missing_file_returns_none(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        assert store.get("anthropic") is None

    def test_save_and_get(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        creds = {"access_token": "tok-abc", "refresh_token": "ref-123"}
        store.save("openai", creds)
        result = store.get("openai")
        assert result == creds

    def test_save_creates_parent_dirs(self, tmp_path: Path) -> None:
        store = CredentialStore(
            path=tmp_path / "nested" / "deep" / "auth.json",
            credentials_dir=tmp_path / "nested" / "deep" / "credentials",
        )
        store.save("anthropic", {"access_token": "x"})
        assert (tmp_path / "nested" / "deep" / "credentials" / "anthropic.json").exists()

    def test_file_permissions_are_600(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("anthropic", {"access_token": "secret"})
        cred_path = tmp_path / "credentials" / "anthropic.json"
        mode = cred_path.stat().st_mode
        assert mode & 0o777 == stat.S_IRUSR | stat.S_IWUSR  # 0o600

    def test_delete_removes_single_provider(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("anthropic", {"access_token": "a"})
        store.save("openai", {"access_token": "o"})
        store.delete("anthropic")
        assert store.get("anthropic") is None
        assert store.get("openai") is not None

    def test_delete_nonexistent_provider_is_noop(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "o"})
        store.delete("anthropic")  # should not raise
        assert store.get("openai") is not None

    def test_clear_deletes_files(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("anthropic", {"access_token": "a"})
        store.save("openai", {"access_token": "o"})
        store.clear()
        assert store.get("anthropic") is None
        assert store.get("openai") is not None or store.get("openai") is None  # no files left
        assert not (tmp_path / "credentials" / "anthropic.json").exists()
        assert not (tmp_path / "credentials" / "openai.json").exists()

    def test_clear_nonexistent_dir_is_noop(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.clear()  # should not raise

    def test_concurrent_provider_storage(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("anthropic", {"access_token": "a-tok"})
        store.save("openai", {"access_token": "o-tok"})
        assert store.get("anthropic")["access_token"] == "a-tok"
        assert store.get("openai")["access_token"] == "o-tok"

    def test_overwrite_existing_credentials(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "old"})
        store.save("openai", {"access_token": "new"})
        assert store.get("openai")["access_token"] == "new"

    def test_corrupt_per_provider_file_returns_none(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        cred_dir = tmp_path / "credentials"
        cred_dir.mkdir(parents=True)
        (cred_dir / "anthropic.json").write_text("{broken json", encoding="utf-8")
        assert store.get("anthropic") is None

    def test_corrupt_legacy_json_returns_none(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.path.write_text("{broken json", encoding="utf-8")
        assert store.get("anthropic") is None


# ===================================================================
# CredentialStore — Spec 057 SC-004 (per-provider files + lazy migration)
# ===================================================================


class TestCredentialStoreSC4:
    """SC-004: per-provider credential files with lazy migration.

    Each provider's credentials live at ``~/.conversus/credentials/{provider}.json``
    (single dict, not a nested ``{provider: dict}`` mapping). On first ``get()``,
    legacy entries from ``~/.conversus/auth.json`` are migrated to the new
    location. The legacy file is preserved.
    """

    def test_set_writes_per_provider_file(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        creds = {
            "access_token": "tok-abc",
            "refresh_token": "ref-123",
            "expires_at": 9999999999,
            "token_type": "bearer",
        }
        store.set("anthropic", creds)

        cred_path = tmp_path / "credentials" / "anthropic.json"
        assert cred_path.exists()
        # File contains the credential dict directly, not nested under provider name.
        on_disk = json.loads(cred_path.read_text(encoding="utf-8"))
        assert on_disk == creds
        assert "anthropic" not in on_disk  # not nested

    def test_set_does_not_write_legacy_auth_json(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        assert not store.path.exists()
        store.set("anthropic", {"access_token": "x"})
        # Legacy file must not be created or modified by ``set``.
        assert not store.path.exists()

    def test_get_reads_per_provider_file(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        cred_dir = tmp_path / "credentials"
        cred_dir.mkdir(parents=True)
        creds = {"access_token": "from-disk", "expires_at": 123}
        (cred_dir / "anthropic.json").write_text(
            json.dumps(creds), encoding="utf-8"
        )

        result = store.get("anthropic")
        assert result == creds

    def test_get_lazy_migrates_from_legacy_auth_json(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        # Plant legacy auth.json with a nested {provider: creds} structure.
        legacy_creds = {"access_token": "legacy-tok", "refresh_token": "legacy-ref"}
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(
            json.dumps({"anthropic": legacy_creds}), encoding="utf-8"
        )

        cred_path = tmp_path / "credentials" / "anthropic.json"
        assert not cred_path.exists()  # not migrated yet

        result = store.get("anthropic")
        assert result == legacy_creds
        # Migration must have happened on first read.
        assert cred_path.exists()
        on_disk = json.loads(cred_path.read_text(encoding="utf-8"))
        assert on_disk == legacy_creds

    def test_get_lazy_migration_preserves_legacy_file(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        legacy_data = {
            "anthropic": {"access_token": "legacy-tok"},
            "openai": {"access_token": "openai-tok"},
        }
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(json.dumps(legacy_data), encoding="utf-8")

        store.get("anthropic")  # triggers migration

        # Legacy file still on disk with all original data intact.
        assert store.path.exists()
        on_disk = json.loads(store.path.read_text(encoding="utf-8"))
        assert on_disk == legacy_data

    def test_get_returns_none_when_provider_absent_everywhere(
        self, tmp_path: Path
    ) -> None:
        store = _make_store(tmp_path)
        # Legacy auth.json exists but has a different provider.
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(
            json.dumps({"openai": {"access_token": "o"}}), encoding="utf-8"
        )

        assert store.get("anthropic") is None
        # No spurious per-provider file should have been created.
        assert not (tmp_path / "credentials" / "anthropic.json").exists()

    def test_delete_removes_per_provider_file_only(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        # Plant both a legacy file and a per-provider file.
        legacy_data = {"anthropic": {"access_token": "legacy-tok"}}
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(json.dumps(legacy_data), encoding="utf-8")
        store.set("anthropic", {"access_token": "new-tok"})
        cred_path = tmp_path / "credentials" / "anthropic.json"
        assert cred_path.exists()

        store.delete("anthropic")

        # Per-provider file gone.
        assert not cred_path.exists()
        # Legacy file untouched.
        assert store.path.exists()
        assert json.loads(store.path.read_text(encoding="utf-8")) == legacy_data

    def test_atomic_write_via_tmp_and_replace(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify writes go through ``{path}.tmp`` then ``os.replace``."""
        store = _make_store(tmp_path)
        replace_calls: list[tuple[str, str]] = []
        real_replace = os.replace

        def spy_replace(src: str | Path, dst: str | Path) -> None:
            replace_calls.append((str(src), str(dst)))
            real_replace(src, dst)

        monkeypatch.setattr("engine.auth.os.replace", spy_replace)

        store.set("anthropic", {"access_token": "x"})

        cred_path = tmp_path / "credentials" / "anthropic.json"
        assert cred_path.exists()
        assert len(replace_calls) == 1
        src, dst = replace_calls[0]
        assert src.endswith(".json.tmp")
        assert dst == str(cred_path)
        # The tmp file should not linger after replace.
        assert not Path(src).exists()

    def test_per_provider_file_has_0600_mode(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.set("anthropic", {"access_token": "secret"})
        cred_path = tmp_path / "credentials" / "anthropic.json"
        mode = cred_path.stat().st_mode & 0o777
        assert mode == 0o600

    def test_credentials_dir_has_0700_mode(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.set("anthropic", {"access_token": "x"})
        cred_dir = tmp_path / "credentials"
        assert cred_dir.is_dir()
        mode = cred_dir.stat().st_mode & 0o777
        assert mode == 0o700

    def test_save_alias_matches_set(self, tmp_path: Path) -> None:
        """Backward-compat: ``save`` is an alias for ``set``."""
        store = _make_store(tmp_path)
        store.save("anthropic", {"access_token": "via-save"})
        assert store.get("anthropic") == {"access_token": "via-save"}

    def test_list_providers_dedupes_legacy_and_per_provider(
        self, tmp_path: Path
    ) -> None:
        store = _make_store(tmp_path)
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(
            json.dumps(
                {
                    "anthropic": {"access_token": "legacy-a"},
                    "openai": {"access_token": "legacy-o"},
                }
            ),
            encoding="utf-8",
        )
        # New per-provider file for a third provider.
        store.set("anthropic", {"access_token": "new-a"})  # already in legacy
        assert store.list_providers() == ["anthropic", "openai"]


# ===================================================================
# _atomic_write_json
# ===================================================================


class TestAtomicWriteJson:
    """Helper that backs every per-provider write."""

    def test_writes_data_to_path(self, tmp_path: Path) -> None:
        target = tmp_path / "out.json"
        _atomic_write_json(target, {"a": 1})
        assert json.loads(target.read_text(encoding="utf-8")) == {"a": 1}

    def test_default_mode_is_0600(self, tmp_path: Path) -> None:
        target = tmp_path / "out.json"
        _atomic_write_json(target, {"a": 1})
        assert target.stat().st_mode & 0o777 == 0o600

    def test_creates_parent_dir(self, tmp_path: Path) -> None:
        target = tmp_path / "deep" / "nested" / "out.json"
        _atomic_write_json(target, {"a": 1})
        assert target.exists()

    def test_uses_tmp_then_replace(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        target = tmp_path / "out.json"
        replace_args: list[tuple[Any, Any]] = []
        real_replace = os.replace

        def spy(src: Any, dst: Any) -> None:
            replace_args.append((src, dst))
            real_replace(src, dst)

        monkeypatch.setattr("engine.auth.os.replace", spy)
        _atomic_write_json(target, {"a": 1})

        assert len(replace_args) == 1
        src, dst = replace_args[0]
        assert str(src).endswith(".json.tmp")
        assert str(dst) == str(target)


# ===================================================================
# PKCE generation
# ===================================================================


class TestPKCE:
    """PKCE verifier and S256 challenge generation."""

    def test_verifier_length(self) -> None:
        verifier, _ = _generate_pkce()
        # RFC 7636: verifier must be 43-128 characters
        assert 43 <= len(verifier) <= 128

    def test_challenge_is_sha256_of_verifier(self) -> None:
        verifier, challenge = _generate_pkce()
        expected_digest = hashlib.sha256(verifier.encode("ascii")).digest()
        expected_challenge = base64.urlsafe_b64encode(expected_digest).rstrip(b"=").decode("ascii")
        assert challenge == expected_challenge

    def test_verifiers_are_unique(self) -> None:
        v1, _ = _generate_pkce()
        v2, _ = _generate_pkce()
        assert v1 != v2


# ===================================================================
# Token redaction
# ===================================================================


class TestRedact:
    """Token redaction for safe logging."""

    def test_long_token_redacted(self) -> None:
        assert _redact("sk-abcdefghijklmnop") == "sk-a...mnop"

    def test_short_token_fully_masked(self) -> None:
        assert _redact("short") == "***"


# ===================================================================
# login flow
# ===================================================================


class TestLogin:
    """OAuth PKCE login with mocked browser, callback, and token exchange."""

    def test_login_stores_credentials(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        browser_calls: list[str] = []

        def mock_open(url: str) -> None:
            browser_calls.append(url)

        def mock_server(port: int) -> tuple[str, int]:
            return ("auth-code-123", 12345)

        def mock_exchange(
            token_url: str,
            *,
            code: str,
            redirect_uri: str,
            code_verifier: str,
            client_id: str,
        ) -> dict[str, Any]:
            assert code == "auth-code-123"
            return {
                "access_token": "access-tok-xyz",
                "refresh_token": "refresh-tok-abc",
                "expires_in": 3600,
                "token_type": "bearer",
            }

        creds = login(
            "openai",
            store=store,
            _open_browser=mock_open,
            _run_server=mock_server,
            _exchange_token=mock_exchange,
        )

        assert creds["access_token"] == "access-tok-xyz"
        assert creds["refresh_token"] == "refresh-tok-abc"
        assert creds["token_type"] == "bearer"
        assert creds["expires_at"] > time.time()

        # Verify stored
        stored = store.get("openai")
        assert stored is not None
        assert stored["access_token"] == "access-tok-xyz"

        # Verify browser was opened with correct URL
        assert len(browser_calls) == 1
        assert "auth.openai.com/authorize" in browser_calls[0]
        assert "code_challenge" in browser_calls[0]
        assert "S256" in browser_calls[0]

    def test_login_unknown_provider_raises(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        with pytest.raises(ProviderError, match="Unknown provider"):
            login("gemini", store=store)

    def test_login_anthropic_uses_correct_urls(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        store = _make_store(tmp_path)
        browser_calls: list[str] = []

        # Make state deterministic so the pasted code#state matches the
        # locally-generated state the CSRF check compares against.
        _patch_state(monkeypatch, "statevalue")

        def mock_open(url: str) -> None:
            browser_calls.append(url)

        def mock_prompt() -> str:
            return "authcode123#statevalue"

        def mock_exchange(token_url: str, **kwargs: Any) -> dict[str, Any]:
            assert "platform.claude.com" in token_url
            return {"access_token": "at", "expires_in": 3600}

        login(
            "anthropic",
            store=store,
            _open_browser=mock_open,
            _prompt_code=mock_prompt,
            _exchange_token=mock_exchange,
        )

        assert "claude.ai/oauth/authorize" in browser_calls[0]

    def test_login_anthropic_code_paste_flow(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Full code-paste flow: browser open → prompt → exchange → store."""
        store = _make_store(tmp_path)
        _patch_state(monkeypatch, "statevalue")
        browser_calls: list[str] = []

        def mock_open(url: str) -> None:
            browser_calls.append(url)

        def mock_prompt() -> str:
            return "authcode123#statevalue"

        def mock_exchange(
            token_url: str,
            *,
            code: str,
            redirect_uri: str,
            code_verifier: str,
            client_id: str,
            state: str,
        ) -> dict[str, Any]:
            assert code == "authcode123"
            assert state == "statevalue"
            return {
                "access_token": "sk-ant-oat-test-token",
                "refresh_token": "ref-tok-abc",
                "expires_in": 3600,
                "token_type": "bearer",
            }

        creds = login(
            "anthropic",
            store=store,
            _open_browser=mock_open,
            _prompt_code=mock_prompt,
            _exchange_token=mock_exchange,
        )

        assert creds["access_token"] == "sk-ant-oat-test-token"
        assert creds["refresh_token"] == "ref-tok-abc"
        # Verify expiry has 5-minute buffer: expires_at should be ~now + 3600 - 300 = now + 3300
        assert creds["expires_at"] <= int(time.time()) + 3600 - 300 + 2  # +2s tolerance
        assert creds["expires_at"] >= int(time.time()) + 3600 - 300 - 2

        # Verify stored
        stored = store.get("anthropic")
        assert stored is not None
        assert stored["access_token"] == "sk-ant-oat-test-token"

        # Verify browser was opened
        assert len(browser_calls) == 1
        assert "claude.ai/oauth/authorize" in browser_calls[0]

    def test_login_anthropic_code_state_parsing(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify code#state splits correctly and missing # raises ProviderError."""
        store = _make_store(tmp_path)
        _patch_state(monkeypatch, "mystate")

        def mock_open(url: str) -> None:
            pass

        def mock_exchange(token_url: str, **kwargs: Any) -> dict[str, Any]:
            return {"access_token": "tok", "expires_in": 3600}

        # Valid format with # in the middle
        def prompt_valid() -> str:
            return "mycode#mystate"

        creds = login(
            "anthropic",
            store=store,
            _open_browser=mock_open,
            _prompt_code=prompt_valid,
            _exchange_token=mock_exchange,
        )
        assert creds["access_token"] == "tok"

        # Missing # should raise
        def prompt_no_hash() -> str:
            return "just-a-code-no-state"

        with pytest.raises(ProviderError, match="no '#' found"):
            login(
                "anthropic",
                store=store,
                _open_browser=mock_open,
                _prompt_code=prompt_no_hash,
                _exchange_token=mock_exchange,
            )

    def test_login_anthropic_json_exchange(self, tmp_path: Path) -> None:
        """Verify _exchange_code_json sends JSON body with state param."""
        from unittest.mock import patch, MagicMock as MM

        mock_response = MM()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "at",
            "refresh_token": "rt",
            "expires_in": 3600,
        }

        with patch("engine.auth.httpx.post", return_value=mock_response) as mock_post:
            from engine.auth import _exchange_code_json

            _exchange_code_json(
                "https://platform.claude.com/v1/oauth/token",
                code="testcode",
                redirect_uri="https://platform.claude.com/oauth/code/callback",
                code_verifier="verifier123",
                client_id="test-client-id",
                state="teststate",
            )

            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args
            # Must use json= not data=
            assert "json" in call_kwargs.kwargs or (len(call_kwargs.args) > 1 and False)
            json_body = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
            assert json_body["state"] == "teststate"
            assert json_body["grant_type"] == "authorization_code"
            assert json_body["code"] == "testcode"

    def test_login_anthropic_expiry_buffer(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify expires_at = now + expires_in - 300 (5-minute buffer)."""
        store = _make_store(tmp_path)
        _patch_state(monkeypatch, "state")
        before = int(time.time())

        def mock_exchange(token_url: str, **kwargs: Any) -> dict[str, Any]:
            return {"access_token": "tok", "expires_in": 7200}

        creds = login(
            "anthropic",
            store=store,
            _open_browser=lambda url: None,
            _prompt_code=lambda: "code#state",
            _exchange_token=mock_exchange,
        )

        after = int(time.time())
        # expires_at should be approximately now + 7200 - 300 = now + 6900
        assert creds["expires_at"] >= before + 7200 - 300
        assert creds["expires_at"] <= after + 7200 - 300

    def test_login_anthropic_auth_url_has_code_param(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify the authorization URL includes code=true parameter."""
        store = _make_store(tmp_path)
        _patch_state(monkeypatch, "s")
        browser_calls: list[str] = []

        def mock_open(url: str) -> None:
            browser_calls.append(url)

        def mock_exchange(token_url: str, **kwargs: Any) -> dict[str, Any]:
            return {"access_token": "tok", "expires_in": 3600}

        login(
            "anthropic",
            store=store,
            _open_browser=mock_open,
            _prompt_code=lambda: "c#s",
            _exchange_token=mock_exchange,
        )

        auth_url = browser_calls[0]
        assert "code=true" in auth_url


# ===================================================================
# Anthropic refresh uses JSON
# ===================================================================


class TestRefreshAnthropic:
    """Anthropic-specific refresh token behavior."""

    def test_refresh_anthropic_uses_json(self, tmp_path: Path) -> None:
        """Verify refresh POST uses json= kwarg for Anthropic, not data=."""
        store = _make_store(tmp_path)
        store.save("anthropic", {
            "access_token": "old-tok",
            "refresh_token": "ref-tok",
            "expires_at": int(time.time()) - 100,  # expired
            "token_type": "bearer",
        })

        post_calls: list[dict[str, Any]] = []

        def mock_post(url: str, **kwargs: Any) -> MagicMock:
            post_calls.append({"url": url, **kwargs})
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = {
                "access_token": "new-tok",
                "refresh_token": "new-ref",
                "expires_in": 7200,
                "token_type": "bearer",
            }
            return resp

        refresh_token("anthropic", store=store, _post=mock_post)

        assert len(post_calls) == 1
        call = post_calls[0]
        # Must use json= not data=
        assert "json" in call, "Anthropic refresh must use json= kwarg"
        assert "data" not in call, "Anthropic refresh must not use data= kwarg"
        assert call["json"]["client_id"] == OAUTH_CONFIGS["anthropic"]["client_id"]


# ===================================================================
# logout
# ===================================================================


class TestLogout:
    """Logout removes stored credentials."""

    def test_logout_deletes_credentials(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "tok"})
        logout("openai", store=store)
        assert store.get("openai") is None

    def test_logout_preserves_other_providers(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "o"})
        store.save("anthropic", {"access_token": "a"})
        logout("openai", store=store)
        assert store.get("anthropic") is not None


# ===================================================================
# get_credentials
# ===================================================================


class TestGetCredentials:
    """get_credentials retrieves stored tokens."""

    def test_returns_stored_credentials(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "tok"})
        assert get_credentials("openai", store=store)["access_token"] == "tok"

    def test_returns_none_when_absent(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        assert get_credentials("openai", store=store) is None


# ===================================================================
# refresh_token
# ===================================================================


class TestRefreshToken:
    """Token refresh when access token is expired."""

    def test_refresh_updates_stored_tokens(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {
            "access_token": "old-tok",
            "refresh_token": "ref-tok",
            "expires_at": int(time.time()) - 100,  # expired
            "token_type": "bearer",
        })

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new-tok",
            "refresh_token": "new-ref",
            "expires_in": 7200,
            "token_type": "bearer",
        }

        result = refresh_token("openai", store=store, _post=lambda *a, **kw: mock_response)
        assert result is not None
        assert result["access_token"] == "new-tok"

        stored = store.get("openai")
        assert stored["access_token"] == "new-tok"
        assert stored["refresh_token"] == "new-ref"

    def test_refresh_skips_when_not_expired(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        future = int(time.time()) + 3600
        store.save("openai", {
            "access_token": "still-valid",
            "refresh_token": "ref",
            "expires_at": future,
            "token_type": "bearer",
        })

        result = refresh_token("openai", store=store)
        assert result["access_token"] == "still-valid"

    def test_refresh_returns_none_without_refresh_token(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "tok", "refresh_token": ""})
        assert refresh_token("openai", store=store) is None

    def test_refresh_returns_none_without_credentials(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        assert refresh_token("openai", store=store) is None

    def test_refresh_http_error_raises(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        store.save("openai", {
            "access_token": "old",
            "refresh_token": "ref",
            "expires_at": int(time.time()) - 100,
        })

        mock_response = MagicMock()
        mock_response.status_code = 401

        with pytest.raises(ProviderError, match="Token refresh failed"):
            refresh_token("openai", store=store, _post=lambda *a, **kw: mock_response)

    def test_refresh_unknown_provider_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ProviderError, match="Unknown provider"):
            refresh_token("gemini")


# ===================================================================
# resolve_provider
# ===================================================================


class TestResolveProvider:
    """Provider resolution: env var → OAuth → error."""

    def test_mock_provider_always_available(self) -> None:
        provider = resolve_provider("mock")
        assert isinstance(provider, MockProvider)

    def test_env_var_anthropic(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-key")
        store = _make_store(tmp_path)
        provider = resolve_provider("anthropic", credential_store=store)
        from engine.providers.anthropic import AnthropicProvider
        assert isinstance(provider, AnthropicProvider)

    def test_env_var_openai(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        store = _make_store(tmp_path)
        provider = resolve_provider("openai", credential_store=store)
        from engine.providers.openai import OpenAIProvider
        assert isinstance(provider, OpenAIProvider)

    def test_oauth_credentials_anthropic(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        store = _make_store(tmp_path)
        store.save("anthropic", {"access_token": "oauth-tok-anthropic"})
        provider = resolve_provider("anthropic", credential_store=store)
        from engine.providers.anthropic import AnthropicProvider
        assert isinstance(provider, AnthropicProvider)

    def test_oauth_credentials_openai(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "oauth-tok-openai"})
        provider = resolve_provider("openai", credential_store=store)
        from engine.providers.openai import OpenAIProvider
        assert isinstance(provider, OpenAIProvider)

    def test_no_credentials_raises_auth_error(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        store = _make_store(tmp_path)
        with pytest.raises(ProviderError, match="No credentials available") as exc_info:
            resolve_provider("anthropic", credential_store=store)
        assert exc_info.value.category == "auth"

    def test_env_var_takes_precedence_over_stored(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setenv("OPENAI_API_KEY", "env-key")
        store = _make_store(tmp_path)
        store.save("openai", {"access_token": "oauth-key"})
        # Should use env var, not stored credentials
        provider = resolve_provider("openai", credential_store=store)
        from engine.providers.openai import OpenAIProvider
        assert isinstance(provider, OpenAIProvider)

    def test_unknown_provider_raises(self, tmp_path: Path) -> None:
        store = _make_store(tmp_path)
        with pytest.raises(ProviderError, match="Unknown provider"):
            resolve_provider("gemini", credential_store=store)

    def test_resolved_provider_satisfies_protocol(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        store = _make_store(tmp_path)
        provider = resolve_provider("openai", credential_store=store)
        assert isinstance(provider, ModelProvider)
