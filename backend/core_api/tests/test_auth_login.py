"""Shared-password sign-in."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

PASSWORD = "correct-horse-battery-staple"


def _client(monkeypatch, **env):
    for key in ("COWORK_AUTH_PASSWORD", "COWORK_API_TOKEN", "COWORK_COOKIE_SECURE"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    import cowork.common.settings.app_settings as app_settings
    app_settings.get_app_settings.cache_clear()
    from cowork.common.auth import login_rate_limiter
    login_rate_limiter.reset("testclient")
    from cowork.server import create_app
    return TestClient(create_app())


@pytest.fixture()
def guarded(monkeypatch):
    client = _client(monkeypatch, COWORK_AUTH_PASSWORD=PASSWORD)
    yield client
    import cowork.common.settings.app_settings as app_settings
    app_settings.get_app_settings.cache_clear()


def test_api_is_closed_until_you_sign_in(guarded):
    assert guarded.get("/api/v1/settings/").status_code == 401


def test_status_reports_that_sign_in_is_required(guarded):
    body = guarded.get("/api/v1/auth/status").json()
    assert body["authRequired"] is True
    assert body["authenticated"] is False
    # No email configured in this fixture, so the page asks for a password only.
    assert body["emailRequired"] is False


def test_email_is_checked_when_one_is_configured(monkeypatch):
    client = _client(
        monkeypatch, COWORK_AUTH_PASSWORD=PASSWORD, COWORK_AUTH_EMAIL="me@example.com"
    )
    try:
        assert client.get("/api/v1/auth/status").json()["emailRequired"] is True
        wrong = client.post(
            "/api/v1/auth/login",
            json={"email": "someone@else.com", "password": PASSWORD},
        )
        assert wrong.status_code == 401
        # Case differences in an email address are not a credential.
        ok = client.post(
            "/api/v1/auth/login",
            json={"email": "ME@Example.com", "password": PASSWORD},
        )
        assert ok.status_code == 200
    finally:
        import cowork.common.settings.app_settings as app_settings
        app_settings.get_app_settings.cache_clear()


def test_signing_in_opens_the_api(guarded):
    assert guarded.post("/api/v1/auth/login", json={"password": PASSWORD}).status_code == 200
    assert guarded.get("/api/v1/settings/").status_code == 200
    assert guarded.get("/api/v1/auth/status").json()["authenticated"] is True


def test_wrong_password_is_rejected(guarded):
    assert guarded.post("/api/v1/auth/login", json={"password": "nope"}).status_code == 401
    assert guarded.get("/api/v1/settings/").status_code == 401


def test_session_cookie_is_httponly(guarded):
    r = guarded.post("/api/v1/auth/login", json={"password": PASSWORD})
    assert "httponly" in r.headers["set-cookie"].lower()


def test_logout_closes_the_api_again(guarded):
    guarded.post("/api/v1/auth/login", json={"password": PASSWORD})
    guarded.post("/api/v1/auth/logout")
    assert guarded.get("/api/v1/settings/").status_code == 401


def test_brute_force_is_throttled(guarded):
    codes = [
        guarded.post("/api/v1/auth/login", json={"password": f"guess-{i}"}).status_code
        for i in range(12)
    ]
    assert 429 in codes, "an unthrottled shared password is one guess away from code execution"


def test_a_forged_session_cookie_is_rejected(guarded):
    guarded.cookies.set("cowork_session", "99999999999.deadbeef")
    assert guarded.get("/api/v1/settings/").status_code == 401


def test_an_expired_session_is_rejected(guarded, monkeypatch):
    from cowork.common import auth
    guarded.post("/api/v1/auth/login", json={"password": PASSWORD})
    monkeypatch.setattr(auth.time, "time", lambda: 9_999_999_999)
    assert guarded.get("/api/v1/settings/").status_code == 401


def test_health_stays_open(guarded):
    assert guarded.get("/api/v1/health/").status_code == 200


def test_api_token_still_works_for_automation(monkeypatch):
    client = _client(monkeypatch, COWORK_AUTH_PASSWORD=PASSWORD, COWORK_API_TOKEN="tok")
    try:
        assert client.get("/api/v1/settings/", headers={"X-Cowork-Token": "tok"}).status_code == 200
    finally:
        import cowork.common.settings.app_settings as app_settings
        app_settings.get_app_settings.cache_clear()


def test_open_when_nothing_is_configured(monkeypatch):
    client = _client(monkeypatch)
    try:
        assert client.get("/api/v1/settings/").status_code == 200
        assert client.get("/api/v1/auth/status").json()["authRequired"] is False
    finally:
        import cowork.common.settings.app_settings as app_settings
        app_settings.get_app_settings.cache_clear()
