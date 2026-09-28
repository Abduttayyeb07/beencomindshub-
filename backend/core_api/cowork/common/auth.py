"""Shared-password login: session tokens and brute-force limiting.

The API has no user accounts. When COWORK_AUTH_PASSWORD is set, the UI asks for
that password once and receives a signed, expiring session cookie; the API-token
header remains available for automation.

The session token is signed rather than stored: there is no session table to
grow or clean up, and a server restart with a new signing key invalidates every
outstanding session. The signing key lives beside the database so sessions do
survive an ordinary restart.
"""
from __future__ import annotations

import base64
import hmac
import time
from collections import defaultdict, deque
from hashlib import sha256
from pathlib import Path

from cowork.common.settings.app_settings import get_app_settings

_SESSION_KEY_FILENAME = ".session_key"


def _signing_key() -> bytes:
    """Load (or create) the key used to sign session tokens."""
    import secrets

    key_path = Path(get_app_settings().master_key_path).parent / _SESSION_KEY_FILENAME
    key_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing = key_path.read_bytes().strip()
        if existing:
            return existing
    except FileNotFoundError:
        pass
    key = secrets.token_bytes(32).hex().encode()
    try:
        with open(key_path, "xb") as fh:
            fh.write(key)
        key_path.chmod(0o600)
    except FileExistsError:
        return key_path.read_bytes().strip()
    except OSError:
        pass
    return key


def issue_session(ttl_seconds: int) -> str:
    """Mint a session token valid for ttl_seconds."""
    expires_at = int(time.time()) + ttl_seconds
    payload = str(expires_at).encode()
    signature = hmac.new(_signing_key(), payload, sha256).hexdigest()
    return base64.urlsafe_b64encode(payload).decode().rstrip("=") + "." + signature


def session_is_valid(token: str) -> bool:
    """True when the token carries a valid signature and has not expired."""
    if not token or "." not in token:
        return False
    encoded, _, signature = token.partition(".")
    try:
        payload = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
        expires_at = int(payload)
    except (ValueError, TypeError):
        return False
    expected = hmac.new(_signing_key(), payload, sha256).hexdigest()
    # Check the signature before the expiry so an attacker learns nothing from
    # the timing about which half failed.
    if not hmac.compare_digest(signature, expected):
        return False
    return expires_at > int(time.time())


def credentials_match(email: str, password: str) -> bool:
    """Check the sign-in pair against the configured values.

    Both comparisons run every time, and neither short-circuits, so the time
    taken does not reveal whether the email was the part that was wrong.
    """
    settings = get_app_settings()
    if not settings.auth_password:
        return False

    password_ok = hmac.compare_digest(password or "", settings.auth_password)
    if settings.auth_email:
        email_ok = hmac.compare_digest(
            (email or "").strip().casefold(), settings.auth_email.strip().casefold()
        )
    else:
        # No email configured: the password alone is the credential.
        email_ok = True
    return password_ok and email_ok


class LoginRateLimiter:
    """Cap login attempts per client.

    A shared password is one guess away from full access — which includes code
    execution — so an unthrottled login endpoint on a reachable host is a
    standing invitation. In-memory on purpose: this is a single process, and a
    restart clearing the counters is an acceptable trade for having no
    dependency.
    """

    def __init__(self, max_attempts: int = 10, window_seconds: int = 900) -> None:
        self._max = max_attempts
        self._window = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def _prune(self, key: str, now: float) -> deque[float]:
        hits = self._hits[key]
        while hits and now - hits[0] > self._window:
            hits.popleft()
        return hits

    def is_blocked(self, key: str) -> bool:
        return len(self._prune(key, time.monotonic())) >= self._max

    def record_failure(self, key: str) -> None:
        now = time.monotonic()
        self._prune(key, now).append(now)

    def reset(self, key: str) -> None:
        self._hits.pop(key, None)


login_rate_limiter = LoginRateLimiter()
