"""Cross-cutting security tests driven by the design registry (elements.yaml)."""

import logging
import pathlib

import pytest
from fastapi.testclient import TestClient
from ruamel.yaml import YAML

from tests import corpus
from tests.conftest import ask, upload_ready

ROOT = pathlib.Path(__file__).resolve().parents[3]  # repo root
ENDPOINTS = YAML(typ="safe", pure=True).load(
    (ROOT / "docs/04-design/elements.yaml").read_text(encoding="utf-8")
)["endpoints"]
PUBLIC = {"health", "getConfig", "login"}


def fill(path):
    return (
        path.replace("{document_id}", "x" * 32)
        .replace("{conversation_id}", "x" * 32)
        .replace("{turn_id}", "x" * 32)
        .replace("{chunk_id}", "1")
    )


@pytest.mark.parametrize(
    "ep", [e for e in ENDPOINTS if e["operationId"] not in PUBLIC], ids=lambda e: e["operationId"]
)
def test_every_protected_endpoint_requires_login(app, ep):
    """AC-101.4 / LG-14: every non-public endpoint rejects anonymous calls, not just the UI."""
    with TestClient(app) as c:
        r = c.request(ep["method"], fill(ep["path"]))
    assert r.status_code == 401, (ep["operationId"], r.status_code)


def test_workspace_isolation_on_every_resource(login):
    """AC-NFR-004: user B gets 404 for every resource of user A."""
    a = login("linh")
    doc = upload_ready(a, "Alpha.pdf", corpus.ALPHA)
    cid = a.post("/api/conversations").json()["id"]
    turn = ask(a, "Giá trị hợp đồng Alpha", cid).json()
    chunk_id = turn["citations"][0]["chunk_id"]

    b = login("mai")
    assert b.get(f"/api/documents/{doc['id']}").status_code == 404
    assert b.delete(f"/api/documents/{doc['id']}").status_code == 404
    assert b.get(f"/api/conversations/{cid}").status_code == 404
    assert b.post(f"/api/conversations/{cid}/questions", json={"question": "abc"}).status_code == 404
    assert b.get(f"/api/chunks/{chunk_id}").status_code == 404
    assert b.put(f"/api/turns/{turn['id']}/feedback", json={"rating": "up"}).status_code == 404
    assert b.get("/api/documents").json()["documents"] == []
    # scoping to someone else's document does not leak it either
    upload_ready(b, "Beta.pdf", corpus.BETA)
    t = ask(b, "Giá trị hợp đồng Alpha", document_ids=[doc["id"]])
    assert t.status_code == 409
    # and A's document is untouched
    assert a.get(f"/api/documents/{doc['id']}").status_code == 200


def test_logs_never_contain_content(login, caplog):
    """AC-NFR-008 / BR-027: questions, answers and document text stay out of every log record."""
    secret_text = "Mật mã kho hàng Zeta là ZX-998877."
    with caplog.at_level(logging.DEBUG):
        c = login("linh", password="mat-khau-rat-bi-mat")  # secret-scan: allow (test fixture)
        upload_ready(c, "Zeta.pdf", [secret_text])
        ask(c, "Mật mã kho hàng Zeta là gì?")
        ask(c, "Câu hỏi riêng tư về lương thưởng XYZ")
    logged = "\n".join(r.getMessage() for r in caplog.records)
    for needle in ("ZX-998877", "Mật mã kho hàng", "lương thưởng XYZ", "mat-khau-rat-bi-mat"):
        assert needle not in logged, needle
