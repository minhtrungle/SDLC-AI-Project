"""CMP-10 Audit Log — who did what and when, never content (FR-019, NFR-008)."""

from cwd.db import now_iso


def record(conn, action: str, user_id: int | None, username: str | None, target: str | None = None) -> None:
    conn.execute(
        "INSERT INTO audit_log (user_id, username, action, target, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, action, target, now_iso()),
    )
