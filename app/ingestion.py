"""CMP-05 Ingestion Pipeline — PDF text extraction, chunking, FTS indexing (ADR-008)."""

import logging
import re

from pypdf import PdfReader

from app.db import connect, now_iso
from app.textnorm import fold

log = logging.getLogger("cwd.ingestion")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
MIN_TEXT_CHARS = 20
_SENTENCE_END = re.compile(r"(?<=[.!?;:…])\s+")


def chunk_page(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split page text into chunks of at most `size` chars on sentence boundaries, carrying
    trailing sentences (up to `overlap` chars) into the next chunk."""
    text = " ".join(text.split())
    if not text:
        return []
    sentences = []
    for s in _SENTENCE_END.split(text):
        sentences.extend(s[i : i + size] for i in range(0, len(s), size))
    chunks, current = [], []
    for s in sentences:
        if current and len(" ".join([*current, s])) > size:
            chunks.append(" ".join(current))
            carry = []
            for prev in reversed(current):
                if len(" ".join([prev, *carry, s])) > min(overlap + len(prev), size) or len(prev) > overlap:
                    break
                carry.insert(0, prev)
            current = carry
        current.append(s)
    chunks.append(" ".join(current))
    return chunks


def _fail(conn, document_id: str, code: str, page_count: int | None = None) -> None:
    conn.execute(
        "UPDATE documents SET status = 'failed', error_code = ?, page_count = ?, processed_at = ? "
        "WHERE id = ?",
        (code, page_count, now_iso(), document_id),
    )


def extract_pages(path) -> tuple[str | None, list[str]]:
    """Return (error_code, page_texts)."""
    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            return "pdf.encrypted", []
        return None, [page.extract_text() or "" for page in reader.pages]
    except Exception:  # noqa: BLE001 — any parser failure means the file is unreadable
        return "pdf.corrupt", []


def ingest_document(settings, document_id: str) -> None:
    with connect(settings) as conn:
        row = conn.execute("SELECT status FROM documents WHERE id = ?", (document_id,)).fetchone()
    if row is None or row["status"] != "processing":
        return  # deleted meanwhile, or already processed
    path = settings.files_dir / f"{document_id}.pdf"
    if not path.exists():
        with connect(settings) as conn:
            _fail(conn, document_id, "ingest.interrupted")
        return

    error, pages = extract_pages(path)
    with connect(settings) as conn:
        if conn.execute("SELECT 1 FROM documents WHERE id = ?", (document_id,)).fetchone() is None:
            return
        if error:
            _fail(conn, document_id, error)
            log.info("document %s failed: %s", document_id, error)
            return
        if sum(len(p.strip()) for p in pages) < MIN_TEXT_CHARS:
            conn.execute(
                "UPDATE documents SET status = 'no_text', page_count = ?, processed_at = ? WHERE id = ?",
                (len(pages), now_iso(), document_id),
            )
            return
        ord_ = 0
        for page_no, text in enumerate(pages, start=1):
            for chunk in chunk_page(text):
                cur = conn.execute(
                    "INSERT INTO chunks (document_id, page, ord, text) VALUES (?, ?, ?, ?)",
                    (document_id, page_no, ord_, chunk),
                )
                conn.execute(
                    "INSERT INTO chunks_fts (rowid, folded) VALUES (?, ?)", (cur.lastrowid, fold(chunk))
                )
                ord_ += 1
        conn.execute(
            "UPDATE documents SET status = 'ready', page_count = ?, processed_at = ? WHERE id = ?",
            (len(pages), now_iso(), document_id),
        )
    log.info("document %s ready: %d pages, %d chunks", document_id, len(pages), ord_)


def recover_pending(settings) -> None:
    """Re-run ingestion for documents left in `processing` by a previous process."""
    with connect(settings) as conn:
        ids = [r[0] for r in conn.execute("SELECT id FROM documents WHERE status = 'processing'")]
    for document_id in ids:
        ingest_document(settings, document_id)
