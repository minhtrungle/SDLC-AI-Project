from datetime import UTC, datetime

from app.db import connect
from app.metrics import iso_week
from tests import corpus
from tests.conftest import ask, upload_ready


def ok(r):
    assert r.status_code == 200, r.text
    return r.json()


def test_feedback_is_saved_and_can_change(login):
    """AC-501.1: one rating per answer per user; changing overwrites."""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    cid = c.post("/api/conversations").json()["id"]
    turn = ok(ask(c, "Giá trị hợp đồng Alpha", cid))
    assert ok(c.put(f"/api/turns/{turn['id']}/feedback", json={"rating": "up"}))["rating"] == "up"
    ok(c.put(f"/api/turns/{turn['id']}/feedback", json={"rating": "down", "reason": "Thiếu thông tin đợt 3"}))
    (saved,) = ok(c.get(f"/api/conversations/{cid}"))["turns"]
    assert saved["feedback"] == "down"


def test_feedback_validation(login):
    """AC-501.2: reason over 500 chars or unknown rating -> 422 feedback.invalid."""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    turn = ok(ask(c, "Giá trị hợp đồng Alpha"))
    r = c.put(f"/api/turns/{turn['id']}/feedback", json={"rating": "down", "reason": "x" * 501})
    assert r.status_code == 422 and r.json()["code"] == "feedback.invalid"
    r = c.put(f"/api/turns/{turn['id']}/feedback", json={"rating": "meh"})
    assert r.status_code == 422 and r.json()["code"] == "feedback.invalid"


def test_feedback_on_someone_elses_turn_404(login):
    a = login("linh")
    upload_ready(a, "Alpha.pdf", corpus.ALPHA)
    turn = ok(ask(a, "Giá trị hợp đồng Alpha"))
    b = login("mai")
    assert b.put(f"/api/turns/{turn['id']}/feedback", json={"rating": "up"}).status_code == 404


def test_weekly_metrics(login):
    """AC-502.1: 2 users asking 3 questions this week -> 2 active users, 3 questions."""
    a = login("linh")
    b = login("mai")
    upload_ready(a, "Alpha.pdf", corpus.ALPHA)
    upload_ready(b, "Beta.pdf", corpus.BETA)
    t1 = ok(ask(a, "Giá trị hợp đồng Alpha"))
    ok(ask(a, "Lương giám đốc là bao nhiêu?"))
    ok(ask(b, "Giá trị hợp đồng Beta"))
    a.put(f"/api/turns/{t1['id']}/feedback", json={"rating": "up"})
    hung = login("hung", role="manager")
    weeks = ok(hung.get("/api/metrics/weekly?weeks=4"))["weeks"]
    assert len(weeks) == 4
    current = weeks[-1]
    assert current["week"] == iso_week(datetime.now(UTC))
    assert current["active_users"] == 2
    assert current["questions"] == 3
    assert current["not_found_rate"] == round(1 / 3, 4)
    assert current["positive_feedback_rate"] == 1.0
    assert weeks[0]["questions"] == 0 and weeks[0]["positive_feedback_rate"] is None


def test_metrics_counts_old_turns_in_their_week(app, login):
    a = login("linh")
    upload_ready(a, "Alpha.pdf", corpus.ALPHA)
    ok(ask(a, "Giá trị hợp đồng Alpha"))
    with connect(app.state.settings) as conn:
        conn.execute("UPDATE turns SET created_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now', '-7 days')")
    weeks = ok(login("hung", role="manager").get("/api/metrics/weekly?weeks=2"))["weeks"]
    assert [w["questions"] for w in weeks] == [1, 0]


def test_metrics_forbidden_for_regular_user(login):
    """AC-502.2"""
    r = login().get("/api/metrics/weekly")
    assert r.status_code == 403 and r.json()["code"] == "auth.forbidden"


def test_iso_week_format():
    assert iso_week(datetime(2026, 10, 28, tzinfo=UTC)) == "2026-W44"
    assert iso_week(datetime(2027, 1, 1, tzinfo=UTC)) == "2026-W53"
