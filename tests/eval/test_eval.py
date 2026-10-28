"""US-306 quality and latency evaluation (AC-306.1, AC-306.2).

Writes docs/07-verification/eval-report.json.
"""

import json
import math
import pathlib
import time

from tests.conftest import ask, make_pdf, upload
from tests.eval import gold

REPORT = pathlib.Path(__file__).resolve().parents[2] / "docs" / "07-verification" / "eval-report.json"
FILLER_DOCS = 44  # 6 gold documents + 44 filler = 50 documents (PRD §3.9.4 scale)


def p90(values):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(0.9 * len(ordered)) - 1)]


def filler_pages(i):
    return [
        f"Biên bản họp nội bộ số {i}: thảo luận kế hoạch tuần, phân công nhân sự phòng {i % 7} và lịch trực.",
        f"Ghi chú số {i}: cập nhật tiến độ chung, không có quyết định mới, lần họp sau vào thứ {2 + i % 5}.",
    ]


def test_quality_and_latency(login):
    c = login()
    files = [(name, make_pdf(pages)) for name, pages in gold.DOCUMENTS.items()]
    files += [(f"BienBan_{i:02d}.pdf", make_pdf(filler_pages(i))) for i in range(FILLER_DOCS)]
    for start in range(0, len(files), 10):
        r = upload(c, *files[start : start + 10])
        assert all(x["ok"] for x in r.json()["results"])
    docs = c.get("/api/documents").json()["documents"]
    assert len(docs) == 50 and all(d["status"] == "ready" for d in docs)

    rows, latencies = [], []
    for question, expect in gold.QUESTIONS:
        started = time.perf_counter()
        turn = ask(c, question).json()  # new conversation each time: no history effects
        latencies.append((time.perf_counter() - started) * 1000)
        cited = {(x["document_name"], x["page"]) for x in turn["citations"]}
        if expect is None:
            correct = turn["outcome"] == "not_found"
            citation_ok = not turn["citations"]
        else:
            name, page, needle = expect
            citation_ok = (name, page) in cited
            correct = turn["outcome"] == "answered" and needle in turn["answer"] and citation_ok
        rows.append(
            {
                "question": question,
                "expected": expect,
                "outcome": turn["outcome"],
                "correct": correct,
                "citation_ok": citation_ok,
                "cited": sorted(cited),
            }
        )

    paraphrase_hits = []
    for question, (name, page, needle) in gold.PARAPHRASES:
        turn = ask(c, question).json()
        cited = {(x["document_name"], x["page"]) for x in turn["citations"]}
        paraphrase_hits.append(
            turn["outcome"] == "answered" and needle in turn["answer"] and (name, page) in cited
        )

    answerable = [r for r in rows if r["expected"] is not None]
    unanswerable = [r for r in rows if r["expected"] is None]
    summary = {
        "questions": len(rows),
        "accuracy": round(sum(r["correct"] for r in rows) / len(rows), 4),
        "citation_accuracy": round(sum(r["citation_ok"] for r in answerable) / len(answerable), 4),
        "not_found_correct": round(sum(r["correct"] for r in unanswerable) / len(unanswerable), 4),
        "p90_latency_ms": round(p90(latencies), 1),
        "paraphrase_accuracy_ungated": round(sum(paraphrase_hits) / len(paraphrase_hits), 4),
        "documents": len(docs),
        "thresholds": {
            "accuracy": gold.MIN_ACCURACY,
            "citation_accuracy": gold.MIN_CITATION_ACCURACY,
            "not_found_correct": gold.MIN_NOT_FOUND_CORRECT,
            "p90_latency_ms": gold.MAX_P90_LATENCY_MS_LOCAL,
        },
        "ai_mode": "local",
        "note": "Synthetic gold set (PD-04); re-run with DEP-002 before go-live.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    failures = [r["question"] for r in rows if not r["correct"]]
    assert summary["accuracy"] >= gold.MIN_ACCURACY, failures
    assert summary["citation_accuracy"] >= gold.MIN_CITATION_ACCURACY, failures
    assert summary["not_found_correct"] >= gold.MIN_NOT_FOUND_CORRECT, failures
    assert summary["p90_latency_ms"] <= gold.MAX_P90_LATENCY_MS_LOCAL
