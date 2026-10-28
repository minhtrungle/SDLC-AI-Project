"""CMP-06 Retriever — FTS5 candidates, IDF-weighted relevance in [0, 1], absolute threshold (ADR-004)."""

import math
from dataclasses import dataclass
from typing import Protocol

from app.textnorm import content_terms, tokens

CANDIDATES = 50
HISTORY_TURNS = 3
HISTORY_BONUS = 0.1  # re-ranking only; never counts toward the threshold


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: int
    document_id: str
    document_name: str
    page: int
    text: str
    relevance: float


class Retriever(Protocol):
    def retrieve(
        self, conn, user_id: int, question: str, history: list[str], document_ids: list[str] | None
    ) -> list[RetrievedChunk]: ...


def _match_expr(terms: list[str]) -> str:
    # Terms are [a-z0-9]+ (see textnorm), so quoting is enough to make them literal FTS5 strings.
    return " OR ".join(f'"{t}"' for t in terms)


class FtsRetriever:
    def __init__(self, settings):
        self.min_relevance = settings.min_relevance
        self.top_k = settings.top_k
        self.per_doc_limit = settings.per_doc_limit

    def retrieve(self, conn, user_id, question, history, document_ids):
        terms = content_terms(question)
        if not terms:
            return []
        hist_terms = [t for t in content_terms(" ".join(history[-HISTORY_TURNS:])) if t not in terms]

        scope_sql, scope_args = "d.user_id = ? AND d.status = 'ready'", [user_id]
        if document_ids is not None:
            scope_sql += f" AND d.id IN ({','.join('?' * len(document_ids))})"
            scope_args += list(document_ids)
        base = f"FROM chunks c JOIN documents d ON d.id = c.document_id WHERE {scope_sql}"

        total = conn.execute(f"SELECT count(*) {base}", scope_args).fetchone()[0]  # noqa: S608 — no user text
        if total == 0:
            return []

        def df(term):
            return conn.execute(
                f"SELECT count(*) FROM chunks_fts f JOIN chunks c ON c.id = f.rowid "  # noqa: S608
                f"JOIN documents d ON d.id = c.document_id WHERE chunks_fts MATCH ? AND {scope_sql}",
                [f'"{term}"', *scope_args],
            ).fetchone()[0]

        idf = {t: math.log(1 + total / max(df(t), 1)) for t in terms}
        denom = sum(idf.values())
        rows = conn.execute(
            f"SELECT c.id, c.document_id, d.filename, c.page, c.text, f.folded, bm25(chunks_fts) AS rank "  # noqa: S608
            f"FROM chunks_fts f JOIN chunks c ON c.id = f.rowid JOIN documents d ON d.id = c.document_id "
            f"WHERE chunks_fts MATCH ? AND {scope_sql} ORDER BY rank LIMIT {CANDIDATES}",
            [_match_expr(terms + hist_terms), *scope_args],
        ).fetchall()

        scored = []
        for r in rows:
            present = set(tokens(r["folded"]))
            rel = sum(w for t, w in idf.items() if t in present) / denom
            if rel < self.min_relevance:
                continue
            bonus = (
                HISTORY_BONUS * (sum(t in present for t in hist_terms) / len(hist_terms)) if hist_terms else 0
            )
            scored.append((rel + bonus, -r["rank"], r, rel))
        scored.sort(key=lambda x: (x[0], x[1]), reverse=True)

        picked, per_doc = [], {}
        for _, _, r, rel in scored:
            if per_doc.get(r["document_id"], 0) >= self.per_doc_limit:
                continue
            per_doc[r["document_id"]] = per_doc.get(r["document_id"], 0) + 1
            picked.append(
                RetrievedChunk(r["id"], r["document_id"], r["filename"], r["page"], r["text"], round(rel, 4))
            )
            if len(picked) == self.top_k:
                break
        return picked
