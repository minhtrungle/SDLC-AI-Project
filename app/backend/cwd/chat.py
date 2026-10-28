"""CMP-08 Chat Service — conversations, RAG orchestration, citation validation (FR-009..FR-016)."""

import json
import re
import sqlite3
import time
import uuid

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from cwd.auth import CurrentUser, current_user, require_csrf
from cwd.db import DB, now_iso
from cwd.errors import ProblemError
from cwd.generation import GeneratorUnavailable
from cwd.retrieval import HISTORY_TURNS, FtsRetriever, RetrievedChunk

router = APIRouter(prefix="/api", tags=["chat"])

NOT_FOUND_ANSWER = (
    "Không tìm thấy thông tin trong tài liệu đã tải lên. "
    "Bạn có thể thử diễn đạt khác hoặc kiểm tra tài liệu đã đủ chưa."
)
SNIPPET_CHARS = 300
_MARKER = re.compile(r"\[(\d+)\]")


class QuestionIn(BaseModel):
    question: str = Field(max_length=4000)  # = app/api-contract/openapi.yaml (NR-07)
    document_ids: list[str] | None = Field(default=None, max_length=50)


def owned_conversation(conn, user_id: int, conversation_id: str):
    row = conn.execute(
        "SELECT id, created_at FROM conversations WHERE id = ? AND user_id = ?", (conversation_id, user_id)
    ).fetchone()
    if row is None:
        raise ProblemError(404, "not_found")
    return row


def validate_citations(text: str, chunks: list[RetrievedChunk]) -> tuple[str, list[dict]]:
    """Keep only [n] markers that point at a retrieved chunk; build citations from the database rows
    (never from generated text) in order of first appearance (ADR-005)."""
    citations, seen = [], set()

    def keep(m):
        n = int(m.group(1))
        if not 1 <= n <= len(chunks):
            return ""
        if n not in seen:
            seen.add(n)
            c = chunks[n - 1]
            citations.append(
                {
                    "index": n,
                    "chunk_id": c.chunk_id,
                    "document_id": c.document_id,
                    "document_name": c.document_name,
                    "page": c.page,
                    "snippet": c.text[:SNIPPET_CHARS],
                }
            )
        return m.group(0)

    cleaned = _MARKER.sub(keep, text)
    return re.sub(r"[ \t]+\n", "\n", cleaned).strip(), citations


def turn_to_dict(conn, row, user_id: int) -> dict:
    citations = json.loads(row["citations_json"])
    doc_ids = {c["document_id"] for c in citations}
    alive = set()
    if doc_ids:
        marks = ",".join("?" * len(doc_ids))
        alive = {
            r[0]
            for r in conn.execute(
                f"SELECT id FROM documents WHERE user_id = ? AND id IN ({marks})",  # noqa: S608 — placeholders only
                [user_id, *doc_ids],
            )
        }
    for c in citations:
        c["document_deleted"] = c["document_id"] not in alive
    fb = conn.execute(
        "SELECT rating FROM feedback WHERE turn_id = ? AND user_id = ?", (row["id"], user_id)
    ).fetchone()
    return {
        "id": row["id"],
        "question": row["question"],
        "answer": row["answer"],
        "outcome": row["outcome"],
        "citations": citations,
        "document_ids": json.loads(row["scope_json"]) if row["scope_json"] else None,
        "warning": None,
        "latency_ms": row["latency_ms"],
        "feedback": fb["rating"] if fb else None,
        "created_at": row["created_at"],
    }


@router.post("/conversations", status_code=201)
def create_conversation(user: CurrentUser = Depends(require_csrf), conn: sqlite3.Connection = DB):
    cid, ts = uuid.uuid4().hex, now_iso()
    conn.execute("INSERT INTO conversations (id, user_id, created_at) VALUES (?, ?, ?)", (cid, user.id, ts))
    return {"id": cid, "created_at": ts, "turns": []}


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: str,
    user: CurrentUser = Depends(current_user),
    conn: sqlite3.Connection = DB,
):
    conv = owned_conversation(conn, user.id, conversation_id)
    rows = conn.execute(
        "SELECT * FROM turns WHERE conversation_id = ? ORDER BY created_at, rowid", (conversation_id,)
    ).fetchall()
    return {
        "id": conv["id"],
        "created_at": conv["created_at"],
        "turns": [turn_to_dict(conn, r, user.id) for r in rows],
    }


@router.post("/conversations/{conversation_id}/questions")
def ask_question(
    conversation_id: str,
    body: QuestionIn,
    request: Request,
    user: CurrentUser = Depends(require_csrf),
    conn: sqlite3.Connection = DB,
):
    started = time.perf_counter()
    settings = request.app.state.settings
    owned_conversation(conn, user.id, conversation_id)
    question = body.question.strip()
    if not 1 <= len(question) <= settings.max_question_chars:
        raise ProblemError(
            422, "chat.invalid_question", f"Câu hỏi phải có từ 1 đến {settings.max_question_chars} ký tự."
        )

    scope_sql, scope_args = "user_id = ?", [user.id]
    if body.document_ids is not None:
        scope_sql += f" AND id IN ({','.join('?' * len(body.document_ids))})"
        scope_args += body.document_ids
    statuses = [
        r[0]
        for r in conn.execute(f"SELECT status FROM documents WHERE {scope_sql}", scope_args)  # noqa: S608
    ]
    if "ready" not in statuses:
        raise ProblemError(409, "chat.no_ready_documents")

    previous = conn.execute(
        "SELECT question, citations_json FROM turns WHERE conversation_id = ? "
        "ORDER BY created_at DESC, rowid DESC LIMIT ?",
        (conversation_id, HISTORY_TURNS),
    ).fetchall()[::-1]
    history = [r["question"] for r in previous]
    # The top-ranked source of the previous answer is the best referent for "nó" (FR-014, ADR-004 §6).
    last_citations = json.loads(previous[-1]["citations_json"]) if previous else []
    cited = {last_citations[0]["document_id"]} if last_citations else set()
    chunks = FtsRetriever(settings).retrieve(conn, user.id, question, history, body.document_ids, cited)

    answer, citations, outcome = NOT_FOUND_ANSWER, [], "not_found"
    if chunks:  # FR-012: no relevant chunk -> the generator is not called at all
        try:
            generated = request.app.state.generator.generate(question, chunks)
        except GeneratorUnavailable:
            raise ProblemError(503, "chat.ai_unavailable") from None
        text, citations = validate_citations(generated.text, chunks)
        if citations:
            answer, outcome = text, "answered"
        else:
            citations = []

    turn_id, ts = uuid.uuid4().hex, now_iso()
    latency_ms = round((time.perf_counter() - started) * 1000)
    conn.execute(
        "INSERT INTO turns (id, conversation_id, question, answer, outcome, citations_json, scope_json, "
        "latency_ms, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            turn_id,
            conversation_id,
            question,
            answer,
            outcome,
            json.dumps(citations, ensure_ascii=False),
            json.dumps(body.document_ids) if body.document_ids is not None else None,
            latency_ms,
            ts,
        ),
    )
    row = conn.execute("SELECT * FROM turns WHERE id = ?", (turn_id,)).fetchone()
    result = turn_to_dict(conn, row, user.id)
    if "processing" in statuses:
        result["warning"] = "docs_processing"  # AC-203.4
    return result


@router.get("/chunks/{chunk_id}")
def get_chunk(chunk_id: int, user: CurrentUser = Depends(current_user), conn: sqlite3.Connection = DB):
    row = conn.execute(
        "SELECT c.id, c.document_id, d.filename, c.page, c.text FROM chunks c "
        "JOIN documents d ON d.id = c.document_id WHERE c.id = ? AND d.user_id = ?",
        (chunk_id, user.id),
    ).fetchone()
    if row is None:
        raise ProblemError(404, "not_found")
    return {
        "chunk_id": row["id"],
        "document_id": row["document_id"],
        "document_name": row["filename"],
        "page": row["page"],
        "text": row["text"],
    }
