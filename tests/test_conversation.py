from app.db import connect
from tests import corpus
from tests.conftest import ask, upload_ready


def ok(r):
    assert r.status_code == 200, r.text
    return r.json()


# ---------------------------------------------------------------- US-205 delete
def test_delete_removes_document(login):
    """AC-205.1"""
    c = login()
    doc = upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    assert c.delete(f"/api/documents/{doc['id']}").status_code == 204
    assert c.get("/api/documents").json()["documents"] == []
    assert c.get(f"/api/documents/{doc['id']}").status_code == 404


def test_deleted_document_is_never_used_again(app, login):
    """AC-205.2, AC-006: question answerable only from the deleted document -> not_found."""
    c = login()
    alpha = upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    assert ok(ask(c, "Giá trị hợp đồng Alpha là bao nhiêu?"))["outcome"] == "answered"
    c.delete(f"/api/documents/{alpha['id']}")
    t = ok(ask(c, "Giá trị hợp đồng Alpha là bao nhiêu?"))
    assert all(x["document_id"] != alpha["id"] for x in t["citations"])
    with connect(app.state.settings) as conn:
        assert (
            conn.execute("SELECT count(*) FROM chunks WHERE document_id=?", (alpha["id"],)).fetchone()[0] == 0
        )
        assert (
            conn.execute("SELECT count(*) FROM chunks_fts").fetchone()[0]
            == conn.execute("SELECT count(*) FROM chunks").fetchone()[0]
        )
    assert not (app.state.settings.files_dir / f"{alpha['id']}.pdf").exists()


def test_old_citation_marked_deleted(login):
    """AC-205.4: earlier answers show 'document deleted' instead of an error."""
    c = login()
    alpha = upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    cid = c.post("/api/conversations").json()["id"]
    t = ok(ask(c, "Giá trị hợp đồng Alpha", cid))
    c.delete(f"/api/documents/{alpha['id']}")
    (turn,) = ok(c.get(f"/api/conversations/{cid}"))["turns"]
    assert turn["citations"][0]["document_deleted"] is True
    assert c.get(f"/api/chunks/{t['citations'][0]['chunk_id']}").status_code == 404


def test_chunk_ids_not_reused_after_delete(login):
    """DF-01: a new upload never takes over the chunk id of a deleted document."""
    c = login()
    alpha = upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    old = ok(ask(c, "Giá trị hợp đồng Alpha"))["citations"][0]["chunk_id"]
    c.delete(f"/api/documents/{alpha['id']}")
    upload_ready(c, "Beta.pdf", corpus.BETA)
    assert c.get(f"/api/chunks/{old}").status_code == 404


def test_delete_is_audited(app, login):
    """AC-103.2 (delete)."""
    c = login()
    doc = upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    c.delete(f"/api/documents/{doc['id']}")
    with connect(app.state.settings) as conn:
        row = conn.execute("SELECT target FROM audit_log WHERE action='document.delete'").fetchone()
    assert row["target"] == doc["id"]


def test_delete_requires_csrf(login):
    c = login()
    doc = upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    del c.headers["X-CSRF-Token"]
    assert c.delete(f"/api/documents/{doc['id']}").status_code == 403


# ---------------------------------------------------------------- US-401..403
def test_follow_up_question_uses_previous_context(login):
    """AC-401.1: 'Thời hạn của nó?' after asking about Alpha cites Alpha's duration page."""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    cid = c.post("/api/conversations").json()["id"]
    ok(ask(c, "Giá trị hợp đồng Alpha là bao nhiêu?", cid))
    t = ok(ask(c, "Thời hạn của nó?", cid))
    assert t["citations"][0]["document_name"] == "Alpha.pdf"
    assert t["citations"][0]["page"] == 3


def test_new_conversation_has_no_history(login):
    """AC-403.2: a new conversation starts empty; the old one stays readable."""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    first = c.post("/api/conversations").json()["id"]
    ok(ask(c, "Giá trị hợp đồng Beta là bao nhiêu?", first))
    second = c.post("/api/conversations").json()["id"]
    assert ok(c.get(f"/api/conversations/{second}"))["turns"] == []
    assert len(ok(c.get(f"/api/conversations/{first}"))["turns"]) == 1


def test_scope_excludes_other_documents(login):
    """AC-402.1: answer only in B, scope = A -> not_found, B never cited."""
    c = login()
    alpha = upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    beta = upload_ready(c, "Beta.pdf", corpus.BETA)
    t = ok(ask(c, "Dự án Beta triển khai ở đâu?", document_ids=[alpha["id"]]))
    assert t["outcome"] == "not_found"
    assert all(x["document_id"] != beta["id"] for x in t["citations"])
    assert t["document_ids"] == [alpha["id"]]


def test_scope_with_no_ready_document(login):
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    r = ask(c, "Giá trị hợp đồng", document_ids=["khong-ton-tai"])
    assert r.status_code == 409


def test_five_turns_in_order(login):
    """AC-403.1"""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    cid = c.post("/api/conversations").json()["id"]
    questions = [f"Câu hỏi {i} về hợp đồng Alpha" for i in range(5)]
    for q in questions:
        ok(ask(c, q, cid))
    turns = ok(c.get(f"/api/conversations/{cid}"))["turns"]
    assert [t["question"] for t in turns] == questions
