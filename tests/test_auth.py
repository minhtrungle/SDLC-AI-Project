from fastapi.testclient import TestClient

from app.db import connect
from app.security import hash_password, verify_password


def audit_actions(app):
    with connect(app.state.settings) as conn:
        return [tuple(r) for r in conn.execute("SELECT action, username, target FROM audit_log ORDER BY id")]


def test_unauthenticated_api_is_rejected(client):
    """AC-101.1 / AC-101.4: no session -> 401 auth.required, no data."""
    r = client.get("/api/auth/me")
    assert r.status_code == 401
    assert r.json()["code"] == "auth.required"


def test_login_success_returns_user_and_sets_secure_cookie(client, make_user):
    """AC-101.2, AC-NFR-010: session cookie is HttpOnly + SameSite=Strict."""
    make_user("linh", "matkhau-123")
    r = client.post("/api/auth/login", json={"username": "linh", "password": "matkhau-123"})
    assert r.status_code == 200
    body = r.json()
    assert body["username"] == "linh" and body["role"] == "user" and body["csrf_token"]
    cookie = r.headers["set-cookie"]
    assert "cwd_session=" in cookie
    assert "HttpOnly" in cookie
    assert "SameSite=strict" in cookie or "SameSite=Strict" in cookie
    me = client.get("/api/auth/me")
    assert me.status_code == 200 and me.json()["username"] == "linh"


def test_login_is_case_insensitive_on_username(client, make_user):
    make_user("Linh", "matkhau-123")
    r = client.post("/api/auth/login", json={"username": "linh", "password": "matkhau-123"})
    assert r.status_code == 200


def test_wrong_password_and_unknown_user_get_same_message(client, make_user):
    """AC-101.3: same generic message, no account enumeration."""
    make_user("linh", "matkhau-123")
    wrong = client.post("/api/auth/login", json={"username": "linh", "password": "sai-roi"})
    unknown = client.post("/api/auth/login", json={"username": "khong-co", "password": "sai-roi"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()
    assert wrong.json()["title"] == "Tên đăng nhập hoặc mật khẩu không đúng."


def test_lockout_after_five_failures(client, make_user):
    """AC-101.5: 6th attempt within 5 minutes -> 429, even with the right password."""
    make_user("linh", "matkhau-123")
    for _ in range(5):
        assert client.post("/api/auth/login", json={"username": "linh", "password": "x"}).status_code == 401
    r = client.post("/api/auth/login", json={"username": "linh", "password": "matkhau-123"})
    assert r.status_code == 429
    assert r.json()["code"] == "auth.too_many_attempts"


def test_logout_invalidates_session(login):
    """AC-101.6"""
    c = login()
    assert c.post("/api/auth/logout").status_code == 204
    assert c.get("/api/auth/me").status_code == 401


def test_write_without_csrf_is_forbidden(login):
    """AC-NFR-010: state-changing request without the CSRF header -> 403."""
    c = login()
    del c.headers["X-CSRF-Token"]
    r = c.post("/api/auth/logout")
    assert r.status_code == 403
    assert r.json()["code"] == "csrf.invalid"
    c.headers["X-CSRF-Token"] = "wrong"
    assert c.post("/api/auth/logout").status_code == 403


def test_session_token_is_stored_hashed(app, login):
    """ADR-007: raw token only in the cookie."""
    c = login()
    raw = c.cookies.get("cwd_session")
    with connect(app.state.settings) as conn:
        stored = [r[0] for r in conn.execute("SELECT token_hash FROM sessions")]
    assert stored and raw not in stored


def test_idle_session_expires(app, login):
    """FR-002: session expires after CWD_SESSION_IDLE_HOURS without activity."""
    c = login()
    with connect(app.state.settings) as conn:
        conn.execute("UPDATE sessions SET last_seen_at = '2000-01-01T00:00:00Z'")
    assert c.get("/api/auth/me").status_code == 401


def test_password_hashing():
    """AC-NFR-010: PBKDF2-SHA256 with >= 200k iterations and random salt."""
    h1, h2 = hash_password("matkhau-123"), hash_password("matkhau-123")
    assert h1 != h2
    algo, iterations, _, _ = h1.split("$")
    assert algo == "pbkdf2_sha256" and int(iterations) >= 200_000
    assert verify_password("matkhau-123", h1)
    assert not verify_password("matkhau-124", h1)
    assert not verify_password("matkhau-123", "garbage")


def test_password_not_stored_in_plaintext(app, make_user):
    make_user("linh", "matkhau-123")
    with connect(app.state.settings) as conn:
        stored = conn.execute("SELECT password_hash FROM users").fetchone()[0]
    assert "matkhau-123" not in stored


def test_audit_log_for_login_events(app, client, make_user):
    """AC-103.1, AC-103.3: success and failure are audited, without passwords."""
    make_user("linh", "matkhau-123")
    client.post("/api/auth/login", json={"username": "linh", "password": "sai-roi"})
    client.post("/api/auth/login", json={"username": "linh", "password": "matkhau-123"})
    actions = audit_actions(app)
    assert ("auth.login_failed", "linh", None) in actions
    assert ("auth.login_success", "linh", None) in actions
    with connect(app.state.settings) as conn:
        dump = " ".join(str(tuple(r)) for r in conn.execute("SELECT * FROM audit_log"))
    assert "sai-roi" not in dump and "matkhau-123" not in dump


def test_login_validation_error(client):
    r = client.post("/api/auth/login", json={"username": "", "password": "x"})
    assert r.status_code == 422
    assert r.json()["code"] == "validation.error"


def test_cookie_secure_flag_when_configured(tmp_path, make_user):
    from app.config import Settings
    from app.main import create_app

    app = create_app(Settings(data_dir=tmp_path / "d", cookie_secure=True))
    with TestClient(app) as c:
        from app.auth import create_user

        with connect(app.state.settings) as conn:
            create_user(conn, "linh", "matkhau-123", "user")
        r = c.post("/api/auth/login", json={"username": "linh", "password": "matkhau-123"})
        assert "Secure" in r.headers["set-cookie"]
