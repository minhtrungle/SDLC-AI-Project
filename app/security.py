"""CMP-03 security primitives — password hashing, tokens, login throttling (ADR-007)."""

import hashlib
import hmac
import secrets
import threading
import time

PBKDF2_ITERATIONS = 210_000
_DUMMY_HASH = None


def hash_password(password: str, iterations: int = PBKDF2_ITERATIONS) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iterations, salt_hex, digest_hex = stored.split("$")
        if algo != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations))
    except ValueError:
        return False
    return hmac.compare_digest(digest.hex(), digest_hex)


def burn_password_check(password: str) -> None:
    """Spend the same time as a real verification so unknown users are not distinguishable."""
    global _DUMMY_HASH  # noqa: PLW0603 — lazily computed constant
    if _DUMMY_HASH is None:
        _DUMMY_HASH = hash_password("not-a-real-password")
    verify_password(password, _DUMMY_HASH)


def new_token() -> str:
    return secrets.token_urlsafe(32)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class LoginLimiter:
    """At most `max_failures` failed logins per key within `window_s` seconds (in-process)."""

    def __init__(self, max_failures: int = 5, window_s: float = 300, clock=time.monotonic):
        self.max_failures = max_failures
        self.window_s = window_s
        self.clock = clock
        self._failures: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def _recent(self, key: str) -> list[float]:
        cutoff = self.clock() - self.window_s
        recent = [t for t in self._failures.get(key, []) if t > cutoff]
        self._failures[key] = recent
        return recent

    def blocked(self, key: str) -> bool:
        with self._lock:
            return len(self._recent(key)) >= self.max_failures

    def fail(self, key: str) -> None:
        with self._lock:
            self._recent(key).append(self.clock())

    def reset(self, key: str) -> None:
        with self._lock:
            self._failures.pop(key, None)
