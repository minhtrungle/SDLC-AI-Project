"""Generate the 4+1 view diagrams (draw.io) from docs/04-design/elements.yaml.

Usage: python tools/gen_diagrams.py
Writes docs/04-design/diagrams/*.drawio. Re-run after changing elements.yaml
or this file; tools/cross_view_audit.py checks the output stays consistent.
"""

import itertools
import pathlib
import xml.etree.ElementTree as ET

from ruamel.yaml import YAML

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESIGN = ROOT / "docs" / "04-design"
OUT = DESIGN / "diagrams"

S_BOX = "rounded=0;whiteSpace=wrap;html=1;"
S_COMPONENT = "shape=component;align=left;spacingLeft=36;whiteSpace=wrap;html=1;"
S_ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
S_USECASE = "ellipse;whiteSpace=wrap;html=1;"
S_BOUNDARY = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fillColor=none;"
S_NODE = "shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;verticalAlign=top;fontStyle=1;"
S_ARTIFACT = "shape=note;whiteSpace=wrap;html=1;size=10;"
S_ACTION = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;"
S_DECISION = "rhombus;whiteSpace=wrap;html=1;"
S_START = "ellipse;html=1;fillColor=#000000;strokeColor=#000000;"
S_END = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
S_LANE = "swimlane;html=1;startSize=24;horizontal=1;"
S_LIFELINE = "shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=0;collapsible=0;size=40;"
S_CLASS = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;collapsible=0;html=1;"
S_ATTR = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;html=1;"
E_DEP = "endArrow=open;dashed=1;html=1;"
E_ASSOC = "endArrow=none;html=1;"
E_FLOW = "endArrow=block;endFill=1;html=1;"
E_MSG = "endArrow=block;endFill=1;html=1;"
E_REPLY = "endArrow=open;dashed=1;html=1;"
E_INCLUDE = "endArrow=open;dashed=1;html=1;"
E_GEN = "endArrow=block;endFill=0;html=1;"
E_COMPOSE = "endArrow=none;startArrow=diamondThin;startFill=1;html=1;"


class Page:
    def __init__(self, name):
        self.name = name
        self.cells = []
        self._ids = itertools.count(2)

    def _id(self):
        return f"c{next(self._ids)}"

    def vertex(self, label, x, y, w, h, style, parent="1"):
        cid = self._id()
        self.cells.append(("v", cid, label, style, parent, (x, y, w, h)))
        return cid

    def edge(self, src, tgt, label="", style=E_FLOW):
        cid = self._id()
        self.cells.append(("e", cid, label, style, src, tgt))
        return cid

    def free_edge(self, x1, y1, x2, y2, label="", style=E_MSG):
        cid = self._id()
        self.cells.append(("f", cid, label, style, (x1, y1), (x2, y2)))
        return cid

    def to_xml(self, parent):
        diagram = ET.SubElement(parent, "diagram", name=self.name, id=self.name.replace(" ", "_"))
        model = ET.SubElement(diagram, "mxGraphModel", grid="1", gridSize="10", page="1",
                              pageWidth="1654", pageHeight="1169")
        root = ET.SubElement(model, "root")
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")
        for kind, cid, label, style, a, b in self.cells:
            if kind == "v":
                cell = ET.SubElement(root, "mxCell", id=cid, value=label, style=style, vertex="1", parent=a)
                x, y, w, h = b
                ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})
            elif kind == "e":
                cell = ET.SubElement(root, "mxCell", id=cid, value=label, style=style, edge="1",
                                     parent="1", source=a, target=b)
                ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
            else:
                cell = ET.SubElement(root, "mxCell", id=cid, value=label, style=style, edge="1", parent="1")
                geo = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
                ET.SubElement(geo, "mxPoint", x=str(a[0]), y=str(a[1]), **{"as": "sourcePoint"})
                ET.SubElement(geo, "mxPoint", x=str(b[0]), y=str(b[1]), **{"as": "targetPoint"})


def write(filename, *pages):
    mxfile = ET.Element("mxfile", host="tools/gen_diagrams.py", version="1")
    for p in pages:
        p.to_xml(mxfile)
    ET.indent(mxfile)
    (OUT / filename).write_text(ET.tostring(mxfile, encoding="unicode") + "\n", encoding="utf-8")
    print("wrote", filename)


def load_elements():
    with open(DESIGN / "elements.yaml", encoding="utf-8") as fh:
        return YAML(typ="safe", pure=True).load(fh)


# ---------------------------------------------------------------- Scenarios
def use_case(el):
    p = Page("Use case")
    actors = {a["id"]: a for a in el["actors"]}
    act = {
        "ACT-01": p.vertex(f"{actors['ACT-01']['name']}<br>({'ACT-01'})", 40, 260, 40, 80, S_ACTOR),
        "ACT-02": p.vertex(f"{actors['ACT-02']['name']}<br>(ACT-02)", 40, 560, 40, 80, S_ACTOR),
        "ACT-03": p.vertex(f"{actors['ACT-03']['name']}<br>(ACT-03)", 40, 800, 40, 80, S_ACTOR),
        "ACT-04": p.vertex(f"{actors['ACT-04']['name']}<br>(ACT-04, tùy chọn)", 1060, 420, 40, 80, S_ACTOR),
    }
    p.vertex("Hệ thống Chat với tài liệu", 220, 20, 760, 920, S_BOUNDARY)
    ucs = [
        ("UC-01", "Đăng nhập / đăng xuất<br>US-101", 280, 60),
        ("UC-02", "Tải lên PDF<br>US-201, US-202", 280, 160),
        ("UC-03", "Xem danh sách & trạng thái<br>US-203, US-204", 280, 260),
        ("UC-04", "Xóa tài liệu<br>US-205", 280, 360),
        ("UC-05", "Đặt câu hỏi<br>US-301..304, US-306", 280, 460),
        ("UC-06", "Xem trích dẫn<br>US-305", 280, 560),
        ("UC-07", "Hỏi tiếp / giới hạn phạm vi<br>US-401, US-402", 620, 160),
        ("UC-08", "Xem lại hội thoại<br>US-403", 620, 260),
        ("UC-09", "Đánh giá câu trả lời<br>US-501", 620, 360),
        ("UC-10", "Xem số liệu sử dụng<br>US-502", 280, 680),
        ("UC-11", "Quản trị tài khoản, sao lưu, dọn nhật ký (CLI)<br>US-103, NFR-006", 280, 800),
        ("UC-12", "Truy xuất & kiểm tra trích dẫn<br>FR-010..013", 620, 460),
        ("UC-13", "Sinh câu trả lời bằng LLM ngoài<br>FR-003 (khi được phép)", 620, 580),
    ]
    uc = {k: p.vertex(f"{k}: {label}", x, y, 260, 70, S_USECASE) for k, label, x, y in ucs}
    for k in ["UC-01", "UC-02", "UC-03", "UC-04", "UC-05", "UC-06", "UC-07", "UC-08", "UC-09"]:
        p.edge(act["ACT-01"], uc[k], style=E_ASSOC)
    p.edge(act["ACT-02"], act["ACT-01"], style=E_GEN)
    p.edge(act["ACT-02"], uc["UC-10"], style=E_ASSOC)
    p.edge(act["ACT-03"], uc["UC-11"], style=E_ASSOC)
    p.edge(uc["UC-05"], uc["UC-12"], "«include»", E_INCLUDE)
    p.edge(uc["UC-07"], uc["UC-05"], "«extend»", E_INCLUDE)
    p.edge(uc["UC-13"], uc["UC-05"], "«extend»<br>[CWD_ALLOW_EXTERNAL_AI=true]", E_INCLUDE)
    p.edge(uc["UC-13"], act["ACT-04"], style=E_ASSOC)
    write("use_case_diagram.drawio", p)


# ------------------------------------------------------------------ Logical
def class_diagram(el):
    def klass(page, title, attrs, x, y, w=280):
        h = 26 + 18 * len(attrs) + 8
        cid = page.vertex(title, x, y, w, h, S_CLASS)
        for i, a in enumerate(attrs):
            page.vertex(a, 0, 26 + 18 * i, w, 18, S_ATTR, parent=cid)
        return cid

    dom = Page("Domain (ENT)")
    ent = {e["name"]: e for e in el["entities"]}

    def title(name):
        return f"{ent[name]['id']} {name}<br>«table {ent[name]['table']}»"

    u = klass(dom, title("User"), ["+id: int", "+username: str", "-password_hash: str", "+role: user|manager", "+created_at: datetime"], 40, 40)
    s = klass(dom, title("Session"), ["-token_hash: str", "+csrf_token: str", "+created_at: datetime", "+last_seen_at: datetime"], 40, 300)
    a = klass(dom, title("AuditEvent"), ["+id: int", "+username: str", "+action: str", "+target: str", "+created_at: datetime"], 40, 540)
    d = klass(dom, title("Document"), ["+id: str", "+filename: str", "+size_bytes: int", "+page_count: int", "+status: processing|ready|failed|no_text", "+error_code: str", "+created_at: datetime"], 440, 40, 320)
    c = klass(dom, title("Chunk"), ["+id: int", "+page: int", "+ord: int", "+text: str"], 440, 330, 320)
    cv = klass(dom, title("Conversation"), ["+id: str", "+created_at: datetime"], 880, 40)
    t = klass(dom, title("Turn"), ["+id: str", "+question: str", "+answer: str", "+outcome: answered|not_found", "+citations: Citation[]", "+scope: str[]", "+latency_ms: int"], 880, 220)
    f = klass(dom, title("Feedback"), ["+rating: up|down", "+reason: str[0..500]", "+created_at: datetime"], 880, 500)
    dom.edge(u, s, "1 — 0..*", E_COMPOSE)
    dom.edge(u, d, "1 — 0..*", E_COMPOSE)
    dom.edge(u, cv, "1 — 0..*", E_COMPOSE)
    dom.edge(u, a, "0..1 — 0..*", E_ASSOC)
    dom.edge(d, c, "1 — 0..*", E_COMPOSE)
    dom.edge(cv, t, "1 — 0..*", E_COMPOSE)
    dom.edge(t, f, "1 — 0..*", E_COMPOSE)
    dom.edge(f, u, "0..* — 1", E_ASSOC)

    svc = Page("Service classes")
    st = klass(svc, "Settings «dataclass» (CMP-13)", ["+data_dir: Path", "+max_file_mb: int = 20", "+max_docs: int = 50", "+min_relevance: float = 0.6", "+top_k: int = 6", "+allow_external_ai: bool = False", "+from_env(): Settings"], 40, 40)
    rc = klass(svc, "RetrievedChunk «dataclass»", ["+chunk_id: int", "+document_id: str", "+document_name: str", "+page: int", "+text: str", "+relevance: float"], 40, 330)
    rt = klass(svc, "FtsRetriever (CMP-06)", ["+retrieve(conn, user_id, question, history, document_ids): RetrievedChunk[]", "-candidates(...)", "-idf(term): float"], 400, 330, 420)
    gi = klass(svc, "«interface» AnswerGenerator (CMP-07)", ["+mode: str", "+generate(question, chunks): GeneratedAnswer"], 400, 40, 360)
    lg = klass(svc, "LocalExtractiveGenerator", ["+mode = 'local'", "+generate(question, chunks)"], 400, 190, 240)
    ag = klass(svc, "AnthropicGenerator", ["+mode = 'external'", "-model: str", "-timeout_s: float", "+generate(question, chunks)"], 680, 170, 260)
    ga = klass(svc, "GeneratedAnswer «dataclass»", ["+text: str", "+used_indices: int[]"], 1000, 40)
    ch = klass(svc, "ChatService (CMP-08)", ["+ask(conn, user, conversation_id, question, document_ids): Turn", "-validate_citations(answer, chunks)"], 1000, 330, 420)
    ll = klass(svc, "LoginLimiter (CMP-03)", ["-max_failures = 5", "-window_s = 300", "+check(key)", "+fail(key)", "+reset(key)"], 40, 560)
    pe = klass(svc, "ProblemError (CMP-02)", ["+status: int", "+code: str", "+detail: str"], 400, 560)
    svc.edge(lg, gi, "", E_GEN.replace("endArrow=block", "endArrow=block;dashed=1"))
    svc.edge(ag, gi, "", E_GEN.replace("endArrow=block", "endArrow=block;dashed=1"))
    svc.edge(gi, ga, "«creates»", E_DEP)
    svc.edge(rt, rc, "«creates»", E_DEP)
    svc.edge(ch, rt, "uses", E_DEP)
    svc.edge(ch, gi, "uses", E_DEP)
    svc.edge(rt, st, "reads", E_DEP)
    svc.edge(ch, pe, "raises", E_DEP)
    svc.edge(ll, pe, "raises", E_DEP)
    write("class_diagram.drawio", dom, svc)


# ------------------------------------------------------------------ Process
def sequence(el):
    def lifelines(page, names, height):
        xs = {}
        for i, n in enumerate(names):
            x = 40 + i * 190
            page.vertex(n, x, 40, 160, height, S_LIFELINE)
            xs[n] = x + 80
        return xs

    def msgs(page, xs, steps, y0=110, dy=44):
        y = y0
        for src, tgt, label, kind in steps:
            style = E_REPLY if kind == "r" else E_MSG
            if src == tgt:
                page.free_edge(xs[src], y, xs[src] + 60, y + 16, label, style)
            else:
                page.free_edge(xs[src], y, xs[tgt], y, label, style)
            y += dy
        return y

    ask = Page("Hỏi đáp")
    names = ["ACT-01 Người dùng", "CMP-01 Web UI", "CMP-03 Auth & Session", "CMP-08 Chat Service",
             "CMP-06 Retriever", "CMP-07 Answer Generator", "CMP-11 Persistence"]
    xs = lifelines(ask, names, 900)
    U, W, A, C, R, G, P = names
    y = msgs(ask, xs, [
        (U, W, "1: nhập câu hỏi, Enter", "m"),
        (W, C, "2: POST /api/conversations/{id}/questions + X-CSRF-Token", "m"),
        (C, A, "3: current_user() + require_csrf()", "m"),
        (A, C, "4: CurrentUser | 401 / 403", "r"),
        (C, P, "5: kiểm tra hội thoại thuộc user, có tài liệu ready", "m"),
        (P, C, "6: OK | 404 / 409", "r"),
        (C, R, "7: retrieve(question, 3 câu trước, phạm vi)", "m"),
        (R, P, "8: FTS5 MATCH + df(t) lọc user_id/status/phạm vi", "m"),
        (P, R, "9: ứng viên", "r"),
        (R, C, "10: chunk có rel ≥ 0.6 (≤ 6, ≤ 2/tài liệu)", "r"),
    ])
    ask.vertex("alt [không có chunk]", 640, y, 800, 80, S_BOUNDARY)
    ask.free_edge(xs[C], y + 40, xs[C] + 60, y + 56, "11a: outcome = not_found, không gọi bộ sinh", E_MSG)
    y += 100
    ask.vertex("alt [có chunk]", 640, y, 800, 190, S_BOUNDARY)
    y = msgs(ask, xs, [
        (C, G, "11b: generate(question, chunks)", "m"),
        (G, C, "12: text có [n]", "r"),
        (C, C, "13: validate_citations — giữ [n] hợp lệ, tên/trang từ CSDL", "m"),
    ], y0=y + 40)
    y += 10
    msgs(ask, xs, [
        (C, P, "14: INSERT turns (latency_ms, citations_json)", "m"),
        (C, W, "15: 200 Turn {answer, outcome, citations, warning}", "r"),
        (W, U, "16: hiển thị câu trả lời + trích dẫn [n]", "r"),
    ], y0=y)

    login = Page("Đăng nhập")
    names2 = ["ACT-01 Người dùng", "CMP-01 Web UI", "CMP-03 Auth & Session", "CMP-10 Audit Log", "CMP-11 Persistence"]
    xs2 = lifelines(login, names2, 640)
    U, W, A, AU, P = names2
    msgs(login, xs2, [
        (U, W, "1: tên đăng nhập + mật khẩu", "m"),
        (W, A, "2: POST /api/auth/login", "m"),
        (A, A, "3: LoginLimiter.check(username) — 429 nếu ≥ 5 lần sai / 5 phút", "m"),
        (A, P, "4: SELECT users WHERE username", "m"),
        (A, A, "5: verify_password (PBKDF2, so sánh hằng thời gian)", "m"),
        (A, AU, "6: record(auth.login_success | auth.login_failed)", "m"),
        (A, P, "7: INSERT sessions(token_hash, csrf_token)", "m"),
        (A, W, "8: 200 Me + Set-Cookie cwd_session (HttpOnly, SameSite=Strict) | 401", "r"),
        (W, U, "9: chuyển tới workspace", "r"),
    ])
    write("sequence_diagram.drawio", ask, login)


def activity(el):
    p = Page("Tải lên và xử lý tài liệu")
    req = p.vertex("CMP-04 Document Service (trong request)", 40, 20, 560, 1000, S_LANE)
    bg = p.vertex("CMP-05 Ingestion Pipeline (tác vụ nền, ADR-008)", 620, 20, 560, 1000, S_LANE)

    def a(label, x, y, parent, style=S_ACTION, w=240, h=50):
        return p.vertex(label, x, y, w, h, style, parent=parent)

    start = a("", 270, 40, req, S_START, 30, 30)
    a1 = a("Nhận danh sách file (multipart)", 165, 100, req)
    d0 = a("Workspace còn chỗ?<br>(< CWD_MAX_DOCS)", 175, 180, req, S_DECISION, 220, 90)
    e0 = a("Kết quả: docs.limit_reached", 340, 300, req, S_ACTION, 200, 50)
    d1 = a("Bắt đầu bằng %PDF-?", 175, 300, req, S_DECISION, 160, 90)
    e1 = a("Kết quả: file.wrong_type", 20, 420, req, S_ACTION, 180, 50)
    d2 = a("≤ CWD_MAX_FILE_MB?", 175, 420, req, S_DECISION, 160, 90)
    e2 = a("Kết quả: file.too_large", 20, 540, req, S_ACTION, 180, 50)
    a2 = a("Lưu files/&lt;id&gt;.pdf + documents(status=processing)", 165, 540, req)
    a3 = a("Audit document.upload; đăng ký tác vụ nền", 165, 620, req)
    d3 = a("Còn file?", 205, 700, req, S_DECISION, 100, 80)
    a4 = a("Trả 200 results[] từng file", 165, 820, req)
    end1 = a("", 270, 910, req, S_END, 30, 30)

    b1 = a("Tài liệu còn tồn tại?", 160, 60, bg, S_DECISION, 220, 90)
    bx = a("Bỏ kết quả (đã bị xóa)", 340, 180, bg, S_ACTION, 200, 50)
    b2 = a("pypdf: đọc từng trang", 160, 180, bg)
    d4 = a("Mã hóa / hỏng?", 175, 260, bg, S_DECISION, 190, 90)
    b3 = a("status = failed<br>(pdf.encrypted | pdf.corrupt)", 340, 380, bg, S_ACTION, 200, 60)
    d5 = a("Tổng văn bản ≥ 20 ký tự?", 160, 380, bg, S_DECISION, 220, 90)
    b4 = a("status = no_text", 340, 500, bg, S_ACTION, 200, 50)
    b5 = a("Cắt chunk ~800 ký tự theo câu, chồng lấn 100", 160, 500, bg)
    b6 = a("1 transaction: INSERT chunks + chunks_fts(fold(text))", 160, 580, bg)
    b7 = a("status = ready, page_count", 160, 660, bg)
    end2 = a("", 265, 760, bg, S_END, 30, 30)

    for s, t, lbl in [
        (start, a1, ""), (a1, d0, ""), (d0, e0, "không"), (d0, d1, "có"), (d1, e1, "không"),
        (d1, d2, "có"), (d2, e2, "không"), (d2, a2, "có"), (a2, a3, ""), (a3, d3, ""),
        (e1, d3, ""), (e2, d3, ""), (d3, d1, "có"), (d3, a4, "không"), (e0, a4, ""), (a4, end1, ""),
        (a3, b1, "BackgroundTasks"), (b1, bx, "không"), (b1, b2, "có"), (b2, d4, ""), (d4, b3, "có"),
        (d4, d5, "không"), (d5, b4, "không"), (d5, b5, "có"), (b5, b6, ""), (b6, b7, ""),
        (b7, end2, ""), (b3, end2, ""), (b4, end2, ""), (bx, end2, ""),
    ]:
        p.edge(s, t, lbl, E_FLOW)
    write("activity_diagram.drawio", p)


# -------------------------------------------------------------- Development
COMPONENT_DEPS = [
    ("CMP-01", "CMP-02", "HTTP/JSON"),
    ("CMP-02", "CMP-03", ""), ("CMP-02", "CMP-04", ""), ("CMP-02", "CMP-08", ""),
    ("CMP-02", "CMP-09", ""), ("CMP-02", "CMP-13", ""), ("CMP-02", "CMP-05", "recover_pending"),
    ("CMP-03", "CMP-10", ""), ("CMP-03", "CMP-11", ""),
    ("CMP-04", "CMP-05", ""), ("CMP-04", "CMP-10", ""), ("CMP-04", "CMP-11", ""),
    ("CMP-05", "CMP-06", "fold()"), ("CMP-05", "CMP-11", ""),
    ("CMP-06", "CMP-11", ""),
    ("CMP-08", "CMP-06", "Retriever"), ("CMP-08", "CMP-07", "AnswerGenerator"), ("CMP-08", "CMP-11", ""),
    ("CMP-09", "CMP-11", ""), ("CMP-10", "CMP-11", ""),
    ("CMP-12", "CMP-03", ""), ("CMP-12", "CMP-11", ""),
]

COMPONENT_POS = {
    "CMP-01": (560, 20), "CMP-02": (560, 150), "CMP-13": (960, 150),
    "CMP-03": (60, 300), "CMP-04": (360, 300), "CMP-08": (760, 300), "CMP-09": (1100, 300),
    "CMP-10": (60, 460), "CMP-05": (360, 460), "CMP-06": (660, 460), "CMP-07": (960, 460),
    "CMP-11": (560, 620), "CMP-12": (60, 620),
}


def component(el):
    p = Page("Components")
    ids = {}
    for c in el["components"]:
        x, y = COMPONENT_POS[c["id"]]
        ids[c["id"]] = p.vertex(f"<b>{c['id']} {c['name']}</b><br>{c['module']}", x, y, 260, 70, S_COMPONENT)
    ext = p.vertex("<b>ACT-04 Anthropic API</b><br>«external, tùy chọn»", 1260, 460, 220, 70, S_BOX + "dashed=1;")
    for s, t, lbl in COMPONENT_DEPS:
        p.edge(ids[s], ids[t], lbl, E_DEP)
    p.edge(ids["CMP-07"], ext, "HTTPS (chỉ khi CWD_ALLOW_EXTERNAL_AI=true)", E_DEP)
    write("component_diagram.drawio", p)


# ----------------------------------------------------------------- Physical
def deployment(el):
    p = Page("Deployment")
    ws = p.vertex("«device» Máy trạm người dùng", 40, 80, 300, 200, S_NODE)
    p.vertex("«execution env» Trình duyệt", 20, 50, 260, 130, S_BOX, parent=ws)
    p.vertex("CMP-01 Web UI<br>index.html, app.js, api.js, styles.css", 50, 110, 220, 50, S_ARTIFACT, parent=ws)
    px = p.vertex("«device» Reverse proxy (khuyến nghị)<br>IIS / Nginx / Caddy — TLS", 420, 120, 260, 120, S_NODE)
    srv = p.vertex("«device» Máy chủ ứng dụng (Windows/Linux)", 760, 40, 520, 520, S_NODE)
    env = p.vertex("«execution env» Python ≥ 3.12 — uvicorn app.main:app (1 worker)", 20, 40, 480, 250, S_BOX, parent=srv)
    p.vertex("app/ (CMP-02..CMP-10, CMP-13)", 20, 50, 220, 50, S_ARTIFACT, parent=env)
    p.vertex("app/web/ (CMP-01, tĩnh)", 250, 50, 210, 50, S_ARTIFACT, parent=env)
    p.vertex("app/cli.py (CMP-12)", 20, 120, 220, 50, S_ARTIFACT, parent=env)
    p.vertex("«config» biến môi trường CWD_*", 250, 120, 210, 50, S_ARTIFACT, parent=env)
    disk = p.vertex("«storage» CWD_DATA_DIR (CMP-11)", 20, 320, 480, 170, S_BOX, parent=srv)
    p.vertex("cwd.db (SQLite WAL)", 20, 50, 140, 50, S_ARTIFACT, parent=disk)
    p.vertex("files/&lt;id&gt;.pdf", 170, 50, 140, 50, S_ARTIFACT, parent=disk)
    p.vertex("backups/", 320, 50, 140, 50, S_ARTIFACT, parent=disk)
    ext = p.vertex("«external» ACT-04 Anthropic API<br>api.anthropic.com", 1360, 200, 240, 100, S_NODE + "dashed=1;")
    adm = p.vertex("«device» Console quản trị (ACT-03)", 420, 420, 260, 100, S_NODE)
    p.edge(ws, px, "HTTPS", E_ASSOC)
    p.edge(px, srv, "HTTP 127.0.0.1:8000", E_ASSOC)
    p.edge(srv, ext, "HTTPS — chỉ khi được phép (ADR-003)", E_ASSOC + "dashed=1;")
    p.edge(adm, srv, "SSH / RDP → python -m app.cli", E_ASSOC)
    write("deployment_diagram.drawio", p)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    el = load_elements()
    use_case(el)
    class_diagram(el)
    sequence(el)
    activity(el)
    component(el)
    deployment(el)


if __name__ == "__main__":
    main()
