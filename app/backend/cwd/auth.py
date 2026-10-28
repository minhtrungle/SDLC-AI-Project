"""CMP-03 Auth & Session — login, logout, current user, CSRF, roles (ADR-007)."""

import hmac
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, Field

from cwd import audit
from cwd.db import DB, now_iso
from cwd.errors import ProblemError
from cwd.security import burn_password_check, hash_password, new_token, token_hash, verify_password

COOKIE = "cwd_session"
TOUCH_INTERVAL = timedelta(seconds=60)  # refresh last_seen_at at most once a minute
router = APIRouter(prefix="/api/auth", tags=["auth"])


@dataclass(frozen=True)
class CurrentUser:
    id: int
    username: str
    role: str
    csrf_token: str

    def as_me(self) -> dict:
        return {"id": self.id, "username": self.username, "role": self.role, "csrf_token": self.csrf_token}


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)


def create_user(conn, username: str, password: str, role: str = "user") -> int:
    if role not in {"user", "manager"}:
        raise ValueError(f"unknown role: {role}")
    cur = conn.execute(
        "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
        (username, hash_password(password), role, now_iso()),
    )
    return cur.lastrowid


def _parse(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def current_user(request: Request, conn: sqlite3.Connection = DB) -> CurrentUser:
    raw = request.cookies.get(COOKIE)
    if not raw:
        raise ProblemError(401, "auth.required")
    key = token_hash(raw)
    row = conn.execute(
        "SELECT u.id, u.username, u.role, s.csrf_token, s.last_seen_at "
        "FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ?",
        (key,),
    ).fetchone()
    if row is None:
        raise ProblemError(401, "auth.required")
    idle = timedelta(hours=request.app.state.settings.session_idle_hours)
    if datetime.now(UTC) - _parse(row["last_seen_at"]) > idle:
        conn.execute("DELETE FROM sessions WHERE token_hash = ?", (key,))
        conn.commit()
        raise ProblemError(401, "auth.required")
    if datetime.now(UTC) - _parse(row["last_seen_at"]) > TOUCH_INTERVAL:
        # Commit at once: an open write transaction would hold SQLite's write lock for the
        # whole request (retrieval, answer generation) and block every other user (CR-01).
        conn.execute("UPDATE sessions SET last_seen_at = ? WHERE token_hash = ?", (now_iso(), key))
        conn.commit()
    return CurrentUser(row["id"], row["username"], row["role"], row["csrf_token"])


def require_csrf(request: Request, user: CurrentUser = Depends(current_user)) -> CurrentUser:
    sent = request.headers.get("X-CSRF-Token", "")
    # Compare bytes: compare_digest raises TypeError on non-ASCII str (CR-05).
    if not hmac.compare_digest(sent.encode(), user.csrf_token.encode()):
        raise ProblemError(403, "csrf.invalid")
    return user


def require_manager(user: CurrentUser = Depends(current_user)) -> CurrentUser:
    if user.role != "manager":
        raise ProblemError(403, "auth.forbidden")
    return user


@router.post("/login")
def login(body: LoginIn, request: Request, response: Response, conn: sqlite3.Connection = DB):
    limiter = request.app.state.login_limiter
    key = body.username.strip().lower()
    if limiter.blocked(key):
        raise ProblemError(429, "auth.too_many_attempts")
    row = conn.execute(
        "SELECT id, username, role, password_hash FROM users WHERE username = ?", (body.username.strip(),)
    ).fetchone()
    if row is None:
        burn_password_check(body.password)
    if row is None or not verify_password(body.password, row["password_hash"]):
        limiter.fail(key)
        audit.record(conn, "auth.login_failed", row["id"] if row else None, body.username.strip())
        conn.commit()
        raise ProblemError(401, "auth.invalid_credentials")
    limiter.reset(key)
    token, csrf = new_token(), new_token()
    ts = now_iso()
    idle = timedelta(hours=request.app.state.settings.session_idle_hours)
    cutoff = (datetime.now(UTC) - idle).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute("DELETE FROM sessions WHERE last_seen_at < ?", (cutoff,))  # housekeeping (CR-14)
    conn.execute(
        "INSERT INTO sessions (token_hash, user_id, csrf_token, created_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (token_hash(token), row["id"], csrf, ts, ts),
    )
    audit.record(conn, "auth.login_success", row["id"], row["username"])
    response.set_cookie(
        COOKIE,
        token,
        httponly=True,
        samesite="strict",
        secure=request.app.state.settings.cookie_secure,
        path="/",
    )
    return CurrentUser(row["id"], row["username"], row["role"], csrf).as_me()


@router.post("/logout", status_code=204)
def logout(
    request: Request,
    user: CurrentUser = Depends(require_csrf),
    conn: sqlite3.Connection = DB,
):
    conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash(request.cookies[COOKIE]),))
    audit.record(conn, "auth.logout", user.id, user.username)
    response = Response(status_code=204)
    response.delete_cookie(COOKIE, path="/")
    return response


@router.get("/me")
def me(user: CurrentUser = Depends(current_user)):
    return user.as_me()
