"""CMP-09 Feedback & Metrics — answer ratings and weekly usage (FR-017, FR-018).

Metric definitions (blueprint §3.9):
- week: ISO week (UTC) of the turn's created_at
- active_users: distinct users who asked at least one question in the week
- questions: turns created in the week
- not_found_rate: not_found turns / questions (0 when there are no questions)
- positive_feedback_rate: 'up' / all ratings on turns created in the week (null without ratings)
"""

import sqlite3
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.auth import CurrentUser, require_csrf, require_manager
from app.db import get_conn, now_iso
from app.errors import ProblemError

router = APIRouter(prefix="/api", tags=["metrics"])
MAX_REASON = 500


class FeedbackIn(BaseModel):
    rating: str
    reason: str | None = None


def iso_week(dt: datetime) -> str:
    year, week, _ = dt.isocalendar()
    return f"{year}-W{week:02d}"


@router.put("/turns/{turn_id}/feedback")
def set_feedback(
    turn_id: str,
    body: FeedbackIn,
    user: CurrentUser = Depends(require_csrf),
    conn: sqlite3.Connection = Depends(get_conn),
):
    owned = conn.execute(
        "SELECT 1 FROM turns t JOIN conversations c ON c.id = t.conversation_id "
        "WHERE t.id = ? AND c.user_id = ?",
        (turn_id, user.id),
    ).fetchone()
    if owned is None:
        raise ProblemError(404, "not_found")
    reason = (body.reason or "").strip() or None
    if body.rating not in {"up", "down"} or (reason and len(reason) > MAX_REASON):
        raise ProblemError(422, "feedback.invalid")
    conn.execute(
        "INSERT INTO feedback (turn_id, user_id, rating, reason, created_at) VALUES (?, ?, ?, ?, ?) "
        "ON CONFLICT (turn_id, user_id) DO UPDATE SET rating = excluded.rating, reason = excluded.reason, "
        "created_at = excluded.created_at",
        (turn_id, user.id, body.rating, reason, now_iso()),
    )
    return {"turn_id": turn_id, "rating": body.rating, "reason": reason}


@router.get("/metrics/weekly")
def weekly_metrics(
    weeks: int = Query(default=8, ge=1, le=26),
    _: CurrentUser = Depends(require_manager),
    conn: sqlite3.Connection = Depends(get_conn),
):
    today = datetime.now(UTC)
    monday = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    starts = [monday - timedelta(weeks=i) for i in reversed(range(weeks))]
    buckets = {
        iso_week(s): {"users": set(), "questions": 0, "not_found": 0, "up": 0, "rated": 0} for s in starts
    }
    since = starts[0].strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = conn.execute(
        "SELECT t.created_at, t.outcome, c.user_id, "
        "(SELECT count(*) FROM feedback f WHERE f.turn_id = t.id AND f.rating = 'up') AS ups, "
        "(SELECT count(*) FROM feedback f WHERE f.turn_id = t.id) AS rated "
        "FROM turns t JOIN conversations c ON c.id = t.conversation_id WHERE t.created_at >= ?",
        (since,),
    )
    for r in rows:
        week = iso_week(datetime.strptime(r["created_at"], "%Y-%m-%dT%H:%M:%SZ"))
        b = buckets.get(week)
        if b is None:
            continue
        b["users"].add(r["user_id"])
        b["questions"] += 1
        b["not_found"] += r["outcome"] == "not_found"
        b["up"] += r["ups"]
        b["rated"] += r["rated"]
    return {
        "weeks": [
            {
                "week": week,
                "active_users": len(b["users"]),
                "questions": b["questions"],
                "not_found_rate": round(b["not_found"] / b["questions"], 4) if b["questions"] else 0.0,
                "positive_feedback_rate": round(b["up"] / b["rated"], 4) if b["rated"] else None,
            }
            for week, b in buckets.items()
        ]
    }
