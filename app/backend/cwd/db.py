"""CMP-11 Persistence — SQLite connection and schema (ADR-002)."""

import contextlib
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from fastapi import Depends, Request

SCHEMA = Path(__file__).with_name("schema.sql")


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@contextlib.contextmanager
def connect(settings):
    """Open a connection; commits on success, rolls back on error, always closes."""
    # FastAPI may open the connection (dependency) and use it (handler) on different threadpool
    # threads; each connection still serves one request at a time, so cross-thread use is safe.
    conn = sqlite3.connect(settings.db_path, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_schema(settings) -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.files_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.db_path)
    try:
        conn.execute("PRAGMA journal_mode = WAL")
        migrate(conn)
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
    finally:
        conn.close()


SCHEMA_VERSION = 2  # 1 = initial; 2 = chunks_fts gained the `owner` column (CR-09)


def migrate(conn: sqlite3.Connection) -> None:
    """Bring a database (live or restored from an older backup) up to SCHEMA_VERSION (NR-02)."""
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    fts_columns = [r[1] for r in conn.execute("PRAGMA table_info(chunks_fts)")]
    if version < 2 and fts_columns and "owner" not in fts_columns:
        # Rebuild the full-text index with the owner partition from the authoritative chunks table.
        with conn:
            conn.execute("DROP TABLE chunks_fts")
            conn.execute(
                "CREATE VIRTUAL TABLE chunks_fts USING fts5(folded, owner, "
                "tokenize = 'unicode61 remove_diacritics 0')"
            )
            from cwd.textnorm import fold  # noqa: PLC0415 — avoid a module cycle at import time

            rows = conn.execute(
                "SELECT c.id, c.text, d.user_id FROM chunks c JOIN documents d ON d.id = c.document_id"
            ).fetchall()
            conn.executemany(
                "INSERT INTO chunks_fts (rowid, folded, owner) VALUES (?, ?, ?)",
                [(cid, fold(text), f"u{uid}") for cid, text, uid in rows],
            )


def get_conn(request: Request):
    """FastAPI dependency: one connection per request."""
    with connect(request.app.state.settings) as conn:
        yield conn


# scope="function": commit/close run BEFORE the response is sent. With the default ("request")
# FastAPI finishes the generator after the response, so a browser's next request could arrive
# before the login session (or any other write) was committed and get a 401 (Playwright E2E finding).
DB = Depends(get_conn, scope="function")
