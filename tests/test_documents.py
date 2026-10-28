from app.config import Settings
from app.db import connect
from app.main import create_app
from tests.conftest import make_pdf, upload


def results(r):
    assert r.status_code == 200, r.text
    return r.json()["results"]


def test_upload_three_pdfs(login):
    """AC-201.1: three valid PDFs all appear in the list."""
    c = login()
    rs = results(
        upload(c, *[(f"tai-lieu-{i}.pdf", make_pdf([f"Nội dung tài liệu số {i}."])) for i in range(3)])
    )
    assert [r["ok"] for r in rs] == [True, True, True]
    names = {d["filename"] for d in c.get("/api/documents").json()["documents"]}
    assert names == {"tai-lieu-0.pdf", "tai-lieu-1.pdf", "tai-lieu-2.pdf"}


def test_one_bad_file_does_not_block_others(login):
    """AC-201.2 / AC-202.1: wrong type rejected individually with a clear message."""
    c = login()
    rs = results(
        upload(
            c,
            ("hop-dong.pdf", make_pdf(["Hợp đồng"])),
            ("ghi-chu.docx", b"PK\x03\x04 not a pdf", "application/vnd.openxmlformats"),
        )
    )
    assert rs[0]["ok"] is True
    assert rs[1] == {
        "filename": "ghi-chu.docx",
        "ok": False,
        "error": {"code": "file.wrong_type", "message": "Sai định dạng, chỉ chấp nhận PDF."},
    }
    assert [d["filename"] for d in c.get("/api/documents").json()["documents"]] == ["hop-dong.pdf"]


def test_pdf_extension_with_non_pdf_content_is_rejected(login):
    """AC-202.3: the signature is checked, not the file name."""
    c = login()
    rs = results(upload(c, ("gia-mao.pdf", b"hello, I am text")))
    assert rs[0]["error"]["code"] == "file.wrong_type"


def test_too_large_file_rejected_with_limit(tmp_path, make_user):
    """AC-202.2: over CWD_MAX_FILE_MB -> file.too_large, message states the limit."""
    from fastapi.testclient import TestClient

    from app.auth import create_user

    app = create_app(Settings(data_dir=tmp_path / "d", max_file_mb=1))
    with TestClient(app) as c:
        with connect(app.state.settings) as conn:
            create_user(conn, "linh", "matkhau-123")
        csrf = c.post("/api/auth/login", json={"username": "linh", "password": "matkhau-123"}).json()[
            "csrf_token"
        ]
        c.headers["X-CSRF-Token"] = csrf
        big = b"%PDF-1.4\n" + b"0" * (1024 * 1024 + 1)
        rs = results(upload(c, ("lon.pdf", big)))
    assert rs[0]["error"]["code"] == "file.too_large"
    assert "1 MB" in rs[0]["error"]["message"]


def test_document_limit(tmp_path):
    """AC-202.4: workspace full -> docs.limit_reached."""
    from fastapi.testclient import TestClient

    from app.auth import create_user

    app = create_app(Settings(data_dir=tmp_path / "d", max_docs=2))
    with TestClient(app) as c:
        with connect(app.state.settings) as conn:
            create_user(conn, "linh", "matkhau-123")
        c.headers["X-CSRF-Token"] = c.post(
            "/api/auth/login", json={"username": "linh", "password": "matkhau-123"}
        ).json()["csrf_token"]
        rs = results(upload(c, *[(f"{i}.pdf", make_pdf([f"tài liệu {i}"])) for i in range(3)]))
    assert [r["ok"] for r in rs] == [True, True, False]
    assert rs[2]["error"]["code"] == "docs.limit_reached"


def test_status_lifecycle_processing_then_ready(login):
    """AC-203.1, AC-203.2: response says processing; background ingestion makes it ready."""
    c = login()
    rs = results(upload(c, ("bao-cao.pdf", make_pdf(["Trang một có nội dung.", "Trang hai có nội dung."]))))
    assert rs[0]["document"]["status"] == "processing"
    doc = c.get(f"/api/documents/{rs[0]['document']['id']}").json()
    assert doc["status"] == "ready"
    assert doc["page_count"] == 2
    assert doc["error_code"] is None


def test_corrupt_pdf_fails_with_reason(login):
    """AC-202.3 / AC-203.3: broken PDF -> failed with a readable reason."""
    c = login()
    rs = results(upload(c, ("hong.pdf", b"%PDF-1.4\nthis is not really a pdf\n%%EOF")))
    doc = c.get(f"/api/documents/{rs[0]['document']['id']}").json()
    assert doc["status"] == "failed"
    assert doc["error_code"] == "pdf.corrupt"
    assert doc["error_message"]


def test_encrypted_pdf_fails(login):
    """EC-11: password-protected PDF -> failed pdf.encrypted."""
    c = login()
    rs = results(upload(c, ("mat-khau.pdf", make_pdf(["Bí mật"], password="pw"))))
    doc = c.get(f"/api/documents/{rs[0]['document']['id']}").json()
    assert (doc["status"], doc["error_code"]) == ("failed", "pdf.encrypted")


def test_scanned_pdf_without_text_is_flagged(login):
    """AC-203.5: no text layer -> no_text, not ready."""
    c = login()
    rs = results(upload(c, ("scan.pdf", make_pdf(["", ""]))))
    doc = c.get(f"/api/documents/{rs[0]['document']['id']}").json()
    assert doc["status"] == "no_text"
    assert doc["error_message"] == "Không trích xuất được văn bản (có thể là bản scan)."


def test_list_shows_name_time_status_pages(login):
    """AC-204.1"""
    c = login()
    upload(c, ("a.pdf", make_pdf(["Nội dung của tài liệu A về hợp đồng."])))
    (doc,) = c.get("/api/documents").json()["documents"]
    assert doc["filename"] == "a.pdf"
    assert doc["created_at"].endswith("Z")
    assert doc["status"] == "ready" and doc["page_count"] == 1 and doc["size_bytes"] > 0


def test_empty_list(login):
    """AC-204.2 (API part): empty workspace returns an empty list."""
    assert login().get("/api/documents").json() == {"documents": []}


def test_upload_is_audited(app, login):
    """AC-103.2 (upload)."""
    c = login()
    doc_id = results(upload(c, ("a.pdf", make_pdf(["x y z"]))))[0]["document"]["id"]
    with connect(app.state.settings) as conn:
        row = conn.execute("SELECT username, target FROM audit_log WHERE action='document.upload'").fetchone()
    assert (row["username"], row["target"]) == ("linh", doc_id)


def test_filename_path_is_stripped(login):
    c = login()
    rs = results(upload(c, ("..\\..\\secret\\x.pdf", make_pdf(["abc"]))))
    assert rs[0]["filename"] == "x.pdf"


def test_get_unknown_document_404(login):
    assert login().get("/api/documents/khong-ton-tai").status_code == 404


def test_upload_requires_csrf(login):
    c = login()
    del c.headers["X-CSRF-Token"]
    assert upload(c, ("a.pdf", make_pdf(["abc"]))).status_code == 403
