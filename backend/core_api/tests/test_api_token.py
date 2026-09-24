"""COWORK_API_TOKEN gates the API, which otherwise has no authentication."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

TOKEN = "test-token-value"


@pytest.fixture()
def guarded(monkeypatch):
    monkeypatch.setenv("COWORK_API_TOKEN", TOKEN)
    import cowork.common.settings.app_settings as app_settings
    app_settings.get_app_settings.cache_clear()
    from cowork.server import create_app
    client = TestClient(create_app())
    yield client
    app_settings.get_app_settings.cache_clear()


def test_request_without_the_token_is_rejected(guarded):
    r = guarded.get("/api/v1/settings/reveal-key/anthropic")
    assert r.status_code == 401


def test_header_is_accepted(guarded):
    r = guarded.get("/api/v1/settings/", headers={"X-Cowork-Token": TOKEN})
    assert r.status_code == 200


def test_cookie_and_query_are_accepted(guarded):
    # Browser-loaded assets (<img>, <iframe>) cannot set request headers.
    assert guarded.get("/api/v1/settings/", cookies={"cowork_token": TOKEN}).status_code == 200
    assert guarded.get(f"/api/v1/settings/?cowork_token={TOKEN}").status_code == 200


def test_a_wrong_token_is_rejected(guarded):
    r = guarded.get("/api/v1/settings/", headers={"X-Cowork-Token": "wrong"})
    assert r.status_code == 401


def test_health_stays_open_for_container_healthchecks(guarded):
    assert guarded.get("/api/v1/health/").status_code == 200


def test_preflight_stays_open(guarded):
    # Browsers send preflights without custom headers; rejecting them would
    # break the UI before the real request is ever made.
    r = guarded.options(
        "/api/v1/responses/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert r.status_code < 400


def test_disabled_by_default(monkeypatch):
    monkeypatch.delenv("COWORK_API_TOKEN", raising=False)
    import cowork.common.settings.app_settings as app_settings
    app_settings.get_app_settings.cache_clear()
    from cowork.server import create_app
    try:
        assert TestClient(create_app()).get("/api/v1/settings/").status_code == 200
    finally:
        app_settings.get_app_settings.cache_clear()
