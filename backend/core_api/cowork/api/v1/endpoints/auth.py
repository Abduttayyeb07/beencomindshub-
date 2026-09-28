"""Sign-in with the shared password.

- GET  /status — whether a sign-in is required, and whether this caller has one
- POST /login  — exchange the password for a session cookie
- POST /logout — clear it

`status` and `login` are exempt from the API gate (see cowork/server.py);
everything else on the server is not.
"""
from __future__ import annotations

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from cowork.common.auth import (
    credentials_match,
    issue_session,
    login_rate_limiter,
    session_is_valid,
)
from cowork.common.settings.app_settings import get_app_settings

router = APIRouter()

SESSION_COOKIE = "cowork_session"


class LoginRequest(BaseModel):
    password: str
    email: str = ""   # ignored when COWORK_AUTH_EMAIL is unset


def _client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@router.get("/status")
def auth_status(request: Request) -> dict:
    settings = get_app_settings()
    required = bool(settings.auth_password)
    if not required:
        return {"authRequired": False, "authenticated": True}
    return {
        "authRequired": True,
        "authenticated": session_is_valid(request.cookies.get(SESSION_COOKIE, "")),
        # Lets the sign-in page show the email field only when it is used.
        "emailRequired": bool(settings.auth_email),
    }


@router.post("/login")
def login(body: LoginRequest, request: Request) -> Response:
    settings = get_app_settings()
    if not settings.auth_password:
        # Nothing to sign in to; say so rather than minting a useless session.
        return JSONResponse({"detail": "Sign-in is not enabled."}, status_code=status.HTTP_400_BAD_REQUEST)

    client = _client_key(request)
    if login_rate_limiter.is_blocked(client):
        return JSONResponse(
            {"detail": "Too many attempts. Wait a few minutes and try again."},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    if not credentials_match(body.email, body.password):
        login_rate_limiter.record_failure(client)
        # Deliberately vague: naming the wrong field would tell a guesser which
        # half they already have.
        return JSONResponse(
            {"detail": "Incorrect email or password."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    login_rate_limiter.reset(client)
    ttl = max(1, settings.session_ttl_hours) * 3600
    response = JSONResponse({"ok": True})
    response.set_cookie(
        SESSION_COOKIE,
        issue_session(ttl),
        max_age=ttl,
        httponly=True,        # JavaScript cannot read it, so XSS cannot steal it
        samesite="lax",       # not sent on cross-site POSTs
        secure=settings.cookie_secure,
        path="/",
    )
    return response


@router.post("/logout")
def logout() -> Response:
    response = JSONResponse({"ok": True})
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response
