from fastapi.testclient import TestClient

from cwd.db import connect, now_iso
from cwd.ingestion import chunk_page, ingest_document
from cwd.main import create_app
from tests.conftest import make_pdf


def test_chunk_page_respects_size_and_overlap():
    sentences = [f"Câu số {i} nói về điều khoản thứ {i} của hợp đồng." for i in range(60)]
    chunks = chunk_page(" ".join(sentences), size=300, overlap=60)
    assert len(chunks) > 1
    assert all(len(c) <= 300 for c in chunks)
    # consecutive chunks overlap by at least one sentence
    assert chunks[0].split(". ")[-1].rstrip(".") in chunks[1]


def test_chunk_page_splits_very_long_sentence():
    chunks = chunk_page("x" * 2000, size=800, overlap=100)
    assert all(len(c) <= 800 for c in chunks) and "".join(chunks).count("x") >= 2000


def test_chunk_page_blank():
    assert chunk_page("   \n ", size=800, overlap=100) == []


def test_chunks_are_indexed_folded(app, login):
    c = login()
    r = c.post(
        "/api/documents", files=[("files", ("a.pdf", make_pdf(["Đà Nẵng có cảng biển."]), "application/pdf"))]
    )
    doc_id = r.json()["results"][0]["document"]["id"]
    with connect(app.state.settings) as conn:
        (chunk_id, page, text) = conn.execute(
            "SELECT id, page, text FROM chunks WHERE document_id=?", (doc_id,)
        ).fetchone()
        folded = conn.execute("SELECT folded FROM chunks_fts WHERE rowid=?", (chunk_id,)).fetchone()[0]
    assert page == 1 and "Đà Nẵng" in text and "da nang" in folded


def test_recover_pending_on_startup(settings, make_user, client, app):
    """ADR-008: a document left in `processing` (crash) is re-ingested at startup."""
    uid = make_user()
    with connect(settings) as conn:
        conn.execute(
            "INSERT INTO documents (id, user_id, filename, size_bytes, status, created_at) "
            "VALUES (?,?,?,?,?,?)",
            ("abc123", uid, "x.pdf", 10, "processing", now_iso()),
        )
    (settings.files_dir / "abc123.pdf").write_bytes(make_pdf(["Nội dung khôi phục sau sự cố máy chủ."]))
    with TestClient(create_app(settings)):
        pass
    with connect(settings) as conn:
        assert conn.execute("SELECT status FROM documents WHERE id='abc123'").fetchone()[0] == "ready"


def test_missing_file_marks_failed(settings, make_user, client):
    uid = make_user()
    with connect(settings) as conn:
        conn.execute(
            "INSERT INTO documents (id, user_id, filename, size_bytes, status, created_at) "
            "VALUES (?,?,?,?,?,?)",
            ("gone", uid, "x.pdf", 10, "processing", now_iso()),
        )
    ingest_document(settings, "gone")
    with connect(settings) as conn:
        row = conn.execute("SELECT status, error_code FROM documents WHERE id='gone'").fetchone()
    assert tuple(row) == ("failed", "ingest.interrupted")


def test_ingest_skips_deleted_document(settings, client):
    """ADR-008: deleted while queued -> no-op."""
    ingest_document(settings, "does-not-exist")  # must not raise
