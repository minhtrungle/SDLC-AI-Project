"""CMP-04 Document Service — upload validation, listing, deletion (FR-004..FR-008)."""

import sqlite3
import uuid
from pathlib import PureWindowsPath

from fastapi import APIRouter, BackgroundTasks, Depends, File, Request, Response, UploadFile

from cwd import audit
from cwd.auth import CurrentUser, current_user, require_csrf
from cwd.db import DB, now_iso
from cwd.errors import MESSAGES, ProblemError
from cwd.ingestion import ingest_document

router = APIRouter(prefix="/api/documents", tags=["documents"])

PDF_MAGIC = b"%PDF-"
MAX_FILES_PER_REQUEST = 10  # the web UI sends one file per request (CR-04)
STATUS_MESSAGES = {
    "pdf.corrupt": "Tệp PDF bị hỏng hoặc không đọc được.",
    "pdf.encrypted": "Tài liệu có mật khẩu, không thể đọc.",
    "ingest.interrupted": "Xử lý bị gián đoạn. Vui lòng xóa và tải lên lại.",
    "no_text": "Không trích xuất được văn bản (có thể là bản scan).",
}
COLUMNS = "id, filename, size_bytes, page_count, status, error_code, created_at"


def to_dict(row) -> dict:
    d = dict(row)
    key = "no_text" if d["status"] == "no_text" else d["error_code"]
    d["error_message"] = STATUS_MESSAGES.get(key) if key else None
    return d


def owned_document(conn, user_id: int, document_id: str):
    row = conn.execute(
        f"SELECT {COLUMNS} FROM documents WHERE id = ? AND user_id = ?",  # noqa: S608 — constant column list
        (document_id, user_id),
    ).fetchone()
    if row is None:
        raise ProblemError(404, "not_found")
    return row


def _display_name(name: str | None) -> str:
    # Both separators: browsers on Windows may send full paths.
    return (PureWindowsPath(name or "").name or "tai-lieu.pdf")[:255]


def _rejected(filename: str, code: str, message: str | None = None) -> dict:
    return {"filename": filename, "ok": False, "error": {"code": code, "message": message or MESSAGES[code]}}


@router.get("")
def list_documents(user: CurrentUser = Depends(current_user), conn: sqlite3.Connection = DB):
    rows = conn.execute(
        f"SELECT {COLUMNS} FROM documents WHERE user_id = ? ORDER BY created_at DESC, rowid DESC",  # noqa: S608
        (user.id,),
    ).fetchall()
    return {"documents": [to_dict(r) for r in rows]}


@router.post("")
def upload_documents(
    request: Request,
    background: BackgroundTasks,
    files: list[UploadFile] = File(...),
    user: CurrentUser = Depends(require_csrf),
    conn: sqlite3.Connection = DB,
):
    settings = request.app.state.settings
    if len(files) > MAX_FILES_PER_REQUEST:
        raise ProblemError(413, "request.too_large", f"Tối đa {MAX_FILES_PER_REQUEST} tệp mỗi lần tải lên.")
    # NR-01: take the write lock BEFORE counting, so parallel uploads (the UI sends one request per
    # file) are serialised and can never push a workspace past CWD_MAX_DOCS.
    conn.execute("BEGIN IMMEDIATE")
    count = conn.execute("SELECT count(*) FROM documents WHERE user_id = ?", (user.id,)).fetchone()[0]
    results, written = [], []
    try:
        _store_files(settings, files, user, conn, background, count, results, written)
        conn.commit()  # background ingestion opens its own connection and must see the rows
    except Exception:
        conn.rollback()
        for path in written:  # no orphan PDFs when a batch or its commit fails (CR-15, NR-11)
            path.unlink(missing_ok=True)
        raise
    return {"results": results}


def _store_files(settings, files, user, conn, background, count, results, written):
    for f in files:
        name = _display_name(f.filename)
        if count >= settings.max_docs:
            results.append(_rejected(name, "docs.limit_reached"))
            continue
        data = f.file.read(settings.max_file_bytes + 1)
        if not data.startswith(PDF_MAGIC):
            results.append(_rejected(name, "file.wrong_type"))
            continue
        if len(data) > settings.max_file_bytes:
            msg = f"Tệp vượt dung lượng cho phép (tối đa {settings.max_file_mb} MB)."
            results.append(_rejected(name, "file.too_large", msg))
            continue
        doc_id = uuid.uuid4().hex
        path = settings.files_dir / f"{doc_id}.pdf"
        path.write_bytes(data)
        written.append(path)
        conn.execute(
            "INSERT INTO documents (id, user_id, filename, size_bytes, status, created_at) "
            "VALUES (?, ?, ?, ?, 'processing', ?)",
            (doc_id, user.id, name, len(data), now_iso()),
        )
        audit.record(conn, "document.upload", user.id, user.username, doc_id)
        count += 1
        background.add_task(ingest_document, settings, doc_id)
        results.append(
            {"filename": name, "ok": True, "document": to_dict(owned_document(conn, user.id, doc_id))}
        )


@router.get("/{document_id}")
def get_document(document_id: str, user: CurrentUser = Depends(current_user), conn: sqlite3.Connection = DB):
    return to_dict(owned_document(conn, user.id, document_id))


@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: str,
    request: Request,
    user: CurrentUser = Depends(require_csrf),
    conn: sqlite3.Connection = DB,
):
    owned_document(conn, user.id, document_id)
    conn.execute("DELETE FROM documents WHERE id = ? AND user_id = ?", (document_id, user.id))
    audit.record(conn, "document.delete", user.id, user.username, document_id)
    conn.commit()
    (request.app.state.settings.files_dir / f"{document_id}.pdf").unlink(missing_ok=True)
    return Response(status_code=204)
