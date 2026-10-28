import logging
import sqlite3

from cwd.config import Settings
from cwd.db import connect


def test_health(client):
    """NFR-005: health endpoint for monitoring."""
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_config_defaults_to_local_ai(client):
    """AC-102.1 (part): default configuration never uses external AI."""
    body = client.get("/api/config").json()
    assert body == {"ai_mode": "local", "max_file_mb": 20, "max_docs": 50, "max_question_chars": 2000}


def test_schema_created(app, client):
    with connect(app.state.settings) as conn:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table')")}
        assert {
            "users",
            "sessions",
            "documents",
            "chunks",
            "conversations",
            "turns",
            "feedback",
            "audit_log",
            "chunks_fts",
        } <= tables
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1


def test_security_headers(client):
    """SAD §8.1 security headers on every response."""
    r = client.get("/api/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert r.headers["Referrer-Policy"] == "no-referrer"
    assert "default-src 'self'" in r.headers["Content-Security-Policy"]


def test_unknown_api_route_is_problem_json(client):
    r = client.get("/api/does-not-exist")
    assert r.status_code == 404
    assert r.headers["content-type"].startswith("application/problem+json")
    assert r.json()["code"] == "not_found"


def test_unexpected_error_hides_stack_trace(app):
    """SAD §8.2: unexpected errors return 500 problem+json without internals."""
    from fastapi.testclient import TestClient

    @app.get("/api/_boom")
    def boom():
        raise RuntimeError("secret internal detail")

    with TestClient(app, raise_server_exceptions=False) as c:
        r = c.get("/api/_boom")
    assert r.status_code == 500
    assert r.json()["code"] == "internal"
    assert "secret internal detail" not in r.text


def test_index_served(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Chat với tài liệu" in r.text


def test_access_log_has_no_body(client, caplog):
    """NFR-008: access log records metadata only."""
    with caplog.at_level(logging.INFO, logger="cwd.access"):
        client.post("/api/auth/login", json={"username": "ai-do", "password": "bi-mat-123"})
    text = " ".join(r.getMessage() for r in caplog.records)
    assert "/api/auth/login" in text
    assert "bi-mat-123" not in text


def test_settings_from_env(tmp_path):
    s = Settings.from_env(
        {
            "CWD_DATA_DIR": str(tmp_path),
            "CWD_MAX_FILE_MB": "5",
            "CWD_ALLOW_EXTERNAL_AI": "TRUE",
            "CWD_MIN_RELEVANCE": "0.5",
            "ANTHROPIC_API_KEY": "sk-test",
        }
    )
    assert s.data_dir == tmp_path
    assert s.max_file_mb == 5
    assert s.allow_external_ai is True
    assert s.min_relevance == 0.5
    assert "sk-test" not in repr(s)


def test_wal_mode(app, client):
    conn = sqlite3.connect(app.state.settings.db_path)
    assert conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
    conn.close()


def test_serves_built_frontend(tmp_path):
    """ADR-009: the backend serves frontend/dist (index.html at /, bundles under /assets)."""
    from fastapi.testclient import TestClient

    from cwd.main import create_app

    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<div id=app>Chat với tài liệu (Vue)</div>", encoding="utf-8")
    (dist / "assets" / "index-abc.js").write_text("console.log(1)", encoding="utf-8")
    with TestClient(create_app(Settings(data_dir=tmp_path / "d", frontend_dist=dist))) as c:
        assert "(Vue)" in c.get("/").text
        r = c.get("/assets/index-abc.js")
        assert r.status_code == 200 and r.headers["X-Content-Type-Options"] == "nosniff"


def test_connection_usable_across_threads(app, client):
    """E2E finding: FastAPI runs the get_conn dependency and the handler on different threads."""
    import threading

    from cwd.db import connect

    errors = []
    with connect(app.state.settings) as conn:

        def use():
            try:
                conn.execute("SELECT count(*) FROM users").fetchone()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        t = threading.Thread(target=use)
        t.start()
        t.join()
    assert errors == []
