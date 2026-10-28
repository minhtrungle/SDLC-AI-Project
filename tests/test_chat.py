from app.chat import NOT_FOUND_ANSWER
from tests import corpus
from tests.conftest import ask, upload, upload_ready


def ok(r):
    assert r.status_code == 200, r.text
    return r.json()


def test_answer_with_citation(login):
    """AC-301.1, AC-305.1, AC-305.3: answer cites document name and page from the database."""
    c = login()
    upload_ready(c, "HopDong_Alpha.pdf", corpus.ALPHA)
    t = ok(ask(c, "Giá trị hợp đồng Alpha là bao nhiêu?"))
    assert t["outcome"] == "answered"
    assert "2,5 tỷ đồng" in t["answer"]
    assert t["citations"][0]["document_name"] == "HopDong_Alpha.pdf"
    assert t["citations"][0]["page"] == 2
    assert f"[{t['citations'][0]['index']}]" in t["answer"]
    assert t["citations"][0]["document_deleted"] is False
    assert t["latency_ms"] >= 0


def test_answers_are_in_vietnamese_for_unaccented_question(login):
    """AC-301.2"""
    c = login()
    upload_ready(c, "HopDong_Alpha.pdf", corpus.ALPHA)
    t = ok(ask(c, "gia tri hop dong alpha la bao nhieu"))
    assert t["outcome"] == "answered" and t["answer"].startswith("Theo tài liệu đã tải lên")


def test_multi_document_answer_cites_both(login):
    """AC-302.1"""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    upload_ready(c, "Beta.pdf", corpus.BETA)
    t = ok(ask(c, "Thời hạn hợp đồng là bao lâu?"))
    assert {x["document_name"] for x in t["citations"]} == {"Alpha.pdf", "Beta.pdf"}


def test_conflicting_documents_both_cited(login):
    """AC-302.2: different values in two documents -> both sources shown."""
    c = login()
    upload_ready(c, "BangGia2026.pdf", corpus.PRICING)
    upload_ready(c, "BangGia2025.pdf", corpus.PRICING_OLD)
    t = ok(ask(c, "Phí bảo trì hằng năm là bao nhiêu?"))
    assert "120 triệu" in t["answer"] and "100 triệu" in t["answer"]
    assert len({x["document_id"] for x in t["citations"]}) == 2


def test_general_knowledge_question_not_found(login):
    """AC-303.1, AC-304.1, AC-304.2"""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    t = ok(ask(c, "Thủ đô của nước Pháp là gì?"))
    assert t["outcome"] == "not_found"
    assert t["answer"] == NOT_FOUND_ANSWER
    assert t["answer"].startswith("Không tìm thấy thông tin trong tài liệu đã tải lên")
    assert t["citations"] == []


def test_prompt_injection_text_is_not_obeyed(login):
    """AC-303.2: instructions inside a document are data, never commands."""
    c = login()
    upload_ready(c, "QuyTrinh.pdf", corpus.INJECTION)
    t = ok(ask(c, "Quy trình nghiệm thu gồm những bước nào?"))
    assert t["outcome"] == "answered"
    assert "123456" not in t["answer"]
    t2 = ok(ask(c, "Mật khẩu quản trị là gì?"))
    # The only way the text may surface is as a cited quotation of the document itself.
    if "123456" in t2["answer"]:
        assert t2["citations"] and all(x["document_name"] == "QuyTrinh.pdf" for x in t2["citations"])


def test_empty_question_rejected(login):
    """AC-301.4"""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    r = ask(c, "   ")
    assert r.status_code == 422 and r.json()["code"] == "chat.invalid_question"
    r = ask(c, "x" * 2001)
    assert r.status_code == 422 and r.json()["code"] == "chat.invalid_question"


def test_no_ready_documents(login):
    """AC-301.5 (API part)."""
    c = login()
    r = ask(c, "Giá trị hợp đồng?")
    assert r.status_code == 409 and r.json()["code"] == "chat.no_ready_documents"


def test_processing_document_is_never_a_source(app, login):
    """AC-203.4: a document still processing is excluded and the turn carries a warning."""
    from app.db import connect

    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    beta = upload_ready(c, "Beta.pdf", corpus.BETA)
    with connect(app.state.settings) as conn:
        conn.execute("UPDATE documents SET status='processing' WHERE id=?", (beta["id"],))
    t = ok(ask(c, "Giá trị hợp đồng Beta là bao nhiêu?"))
    assert all(x["document_id"] != beta["id"] for x in t["citations"])
    assert t["warning"] == "docs_processing"


def test_citation_chunk_text(login):
    """AC-305.2: the citation opens the original passage and page."""
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    cit = ok(ask(c, "Giá trị hợp đồng Alpha"))["citations"][0]
    chunk = ok(c.get(f"/api/chunks/{cit['chunk_id']}"))
    assert chunk["page"] == cit["page"] and "2,5 tỷ đồng" in chunk["text"]


def test_unknown_conversation_404(login):
    c = login()
    r = c.post("/api/conversations/khong-co/questions", json={"question": "abc"})
    assert r.status_code == 404


def test_turn_is_persisted(login):
    c = login()
    upload_ready(c, "Alpha.pdf", corpus.ALPHA)
    conv = c.post("/api/conversations")
    assert conv.status_code == 201
    cid = conv.json()["id"]
    ok(ask(c, "Giá trị hợp đồng Alpha", cid))
    turns = ok(c.get(f"/api/conversations/{cid}"))["turns"]
    assert len(turns) == 1 and turns[0]["citations"][0]["page"] == 2


def test_upload_then_ask_end_to_end(login):
    c = login()
    r = upload(c, ("a.pdf", __import__("tests.conftest").conftest.make_pdf(corpus.BETA)))
    assert r.json()["results"][0]["ok"]
    assert ok(ask(c, "Dự án Beta triển khai ở đâu?"))["citations"][0]["page"] == 1
