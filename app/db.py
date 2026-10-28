"""CMP-11 Persistence — SQLite connection and schema (ADR-002)."""

import contextlib
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from fastapi import Request

SCHEMA = Path(__file__).with_name("schema.sql")


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@contextlib.contextmanager
def connect(settings):
    """Open a connection; commits on success, rolls back on error, always closes."""
    conn = sqlite3.connect(settings.db_path, timeout=10)
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
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    finally:
        conn.close()


def get_conn(request: Request):
    """FastAPI dependency: one connection per request."""
    with connect(request.app.state.settings) as conn:
        yield conn
