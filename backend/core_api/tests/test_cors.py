"""The API is unauthenticated, so an arbitrary website must not be able to call it."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from cowork.server import create_app
    return TestClient(create_app())


def test_arbitrary_origin_is_not_allowed(client):
    # Previously allow_origins=["*"] + allow_credentials=True made Starlette
    # echo the request's Origin, so any page could read every response.
    r = client.get("/api/v1/health/", headers={"Origin": "https://evil.example"})
    assert r.headers.get("access-control-allow-origin") != "https://evil.example"
    assert r.headers.get("access-control-allow-origin") != "*"


def test_arbitrary_origin_preflight_is_not_allowed(client):
    r = client.options(
        "/api/v1/responses/",
        headers={
            "Origin": "https://evil.example",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert r.headers.get("access-control-allow-origin") != "https://evil.example"


def test_local_ui_origin_is_allowed(client):
    r = client.get("/api/v1/health/", headers={"Origin": "http://localhost:5173"})
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_same_origin_requests_are_unaffected(client):
    # Both supported setups proxy the API under the UI's origin, so no Origin
    # header is sent and CORS never applies.
    assert client.get("/api/v1/health/").status_code == 200
