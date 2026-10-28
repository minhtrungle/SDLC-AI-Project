import pathlib

import pytest
from fastapi.testclient import TestClient
from fpdf import FPDF

from cwd.config import Settings
from cwd.main import create_app

FONT_CANDIDATES = [
    pathlib.Path("C:/Windows/Fonts/arial.ttf"),
    pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    pathlib.Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
    pathlib.Path("/Library/Fonts/Arial Unicode.ttf"),
]


def _font():
    for p in FONT_CANDIDATES:
        if p.exists():
            return p
    pytest.skip("no Unicode TTF font available to build Vietnamese test PDFs")


def make_pdf(pages, password=None):
    """Build a text PDF; `pages` is a list of page texts. Empty string = blank page."""
    pdf = FPDF()
    pdf.add_font("U", fname=str(_font()))
    pdf.set_font("U", size=12)
    for text in pages:
        pdf.add_page()
        if text:
            pdf.multi_cell(0, 8, text)
    if password:
        pdf.set_encryption(owner_password=password, user_password=password)
    return bytes(pdf.output())


@pytest.fixture
def settings(tmp_path):
    return Settings(data_dir=tmp_path / "data")


@pytest.fixture
def app(settings):
    return create_app(settings)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def make_user(app, client):
    """Create a user directly in the database. `client` ensures the schema exists."""
    from cwd.auth import create_user
    from cwd.db import connect

    def _make(username="linh", password="matkhau-123", role="user"):
        with connect(app.state.settings) as conn:
            return create_user(conn, username, password, role)

    return _make


@pytest.fixture
def login(app, make_user):
    """Return a logged-in TestClient (own cookie jar) with the CSRF header preset."""
    clients = []

    def _login(username="linh", password="matkhau-123", role="user", create=True):
        if create:
            make_user(username, password, role)
        c = TestClient(app)
        r = c.post("/api/auth/login", json={"username": username, "password": password})
        assert r.status_code == 200, r.text
        c.headers["X-CSRF-Token"] = r.json()["csrf_token"]
        clients.append(c)
        return c

    yield _login
    for c in clients:
        c.close()


def upload(client, *files):
    """files: (name, bytes[, content_type]) tuples. Returns the response."""
    parts = [("files", (f[0], f[1], f[2] if len(f) > 2 else "application/pdf")) for f in files]
    return client.post("/api/documents", files=parts)


def upload_ready(client, name, pages):
    r = upload(client, (name, make_pdf(pages)))
    assert r.status_code == 200, r.text
    result = r.json()["results"][0]
    assert result["ok"], result
    doc = client.get(f"/api/documents/{result['document']['id']}").json()
    assert doc["status"] == "ready", doc
    return doc


def ask(client, question, conversation_id=None, document_ids=None):
    if conversation_id is None:
        conversation_id = client.post("/api/conversations").json()["id"]
    body = {"question": question}
    if document_ids is not None:
        body["document_ids"] = document_ids
    return client.post(f"/api/conversations/{conversation_id}/questions", json=body)
