from app.db import connect
from app.retrieval import FtsRetriever
from tests import corpus
from tests.conftest import upload_ready


def retrieve(app, user_id, question, history=(), document_ids=None):
    s = app.state.settings
    with connect(s) as conn:
        return FtsRetriever(s).retrieve(conn, user_id, question, list(history), document_ids)


def me(c):
    return c.get("/api/auth/me").json()["id"]


def test_finds_relevant_chunk_with_page(app, login):
    c = login()
    upload_ready(c, "HopDong_Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    hits = retrieve(app, me(c), "Giá trị hợp đồng Alpha là bao nhiêu?")
    assert hits[0].document_name == "HopDong_Alpha.pdf" and hits[0].page == 2
    assert all(0 <= h.relevance <= 1 for h in hits)


def test_unaccented_query_matches_accented_text(app, login):
    """AC-301.2: 'gia tri hop dong alpha' finds 'Giá trị hợp đồng Alpha'."""
    c = login()
    upload_ready(c, "HopDong_Alpha.pdf", corpus.ALPHA)
    hits = retrieve(app, me(c), "gia tri hop dong alpha")
    assert hits and hits[0].page == 2


def test_unrelated_question_returns_nothing(app, login):
    """FR-012: below the relevance threshold -> no chunks."""
    c = login()
    upload_ready(c, "HopDong_Alpha.pdf", corpus.ALPHA)
    assert retrieve(app, me(c), "Thủ đô của nước Pháp là gì?") == []
    assert retrieve(app, me(c), "là gì?") == []


def test_scope_limits_documents(app, login):
    """FR-015"""
    c = login()
    a = upload_ready(c, "HopDong_Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    hits = retrieve(app, me(c), "Giá trị hợp đồng Beta", document_ids=[a["id"]])
    assert all(h.document_id == a["id"] for h in hits)


def test_per_document_limit_keeps_sources_diverse(app, login):
    """FR-010: at most per_doc_limit chunks per document."""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    hits = retrieve(app, me(c), "thời hạn hợp đồng")
    per_doc = {}
    for h in hits:
        per_doc[h.document_id] = per_doc.get(h.document_id, 0) + 1
    assert len(per_doc) == 2 and max(per_doc.values()) <= 2


def test_history_breaks_ties_but_does_not_create_matches(app, login):
    """FR-014 / ADR-004 §6: history only re-ranks."""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    hits = retrieve(app, me(c), "Thời hạn của nó?", history=["Giá trị hợp đồng Beta là bao nhiêu?"])
    assert hits[0].document_name == "Beta.pdf"
    assert retrieve(app, me(c), "Thủ đô nước Pháp?", history=["hợp đồng Alpha"]) == []


def test_other_users_documents_are_invisible(app, login):
    """NFR-004 at the retrieval layer."""
    a = login("linh")
    upload_ready(a, "Alpha.pdf", corpus.ALPHA)
    b = login("mai")
    assert retrieve(app, me(b), "Giá trị hợp đồng Alpha") == []
