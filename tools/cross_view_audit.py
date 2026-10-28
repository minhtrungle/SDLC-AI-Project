"""Deterministic cross-view consistency audit for the design (Phase 4).

Checks every view against docs/04-design/elements.yaml:
SAD, blueprint, openapi.yaml/.md, data model, schema.sql, diagrams, ADRs,
UI prototypes, and (once Phase 6 exists) module paths and FastAPI routes.

Usage:
    python tools/cross_view_audit.py            # print report, exit 1 on failure
    python tools/cross_view_audit.py --write    # also write docs/04-design/cross-view-audit.md
"""

import pathlib
import re
import sys

from ruamel.yaml import YAML

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESIGN = ROOT / "docs" / "04-design"
sys.path.insert(0, str(ROOT))
yaml = YAML(typ="safe", pure=True)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class Report:
    def __init__(self):
        self.rows = []

    def check(self, view, rule, ok, detail=""):
        self.rows.append((view, rule, "PASS" if ok else "FAIL", detail))

    def note(self, view, rule, detail):
        self.rows.append((view, rule, "SKIP", detail))

    @property
    def failed(self):
        return [r for r in self.rows if r[2] == "FAIL"]

    def markdown(self):
        lines = [
            "# Cross-view audit — Phase 4 Design",
            "",
            "> Sinh tự động bởi `python tools/cross_view_audit.py --write`. Không sửa tay.",
            "> Nguồn sự thật: [elements.yaml](elements.yaml).",
            "",
            "| View | Quy tắc | Kết quả | Chi tiết |",
            "|---|---|---|---|",
        ]
        lines += [f"| {v} | {r} | {s} | {d or '—'} |" for v, r, s, d in self.rows]
        passed = sum(1 for r in self.rows if r[2] == "PASS")
        lines += [
            "",
            f"**Tổng:** {passed} PASS · {len(self.failed)} FAIL · "
            f"{sum(1 for r in self.rows if r[2] == 'SKIP')} SKIP",
            "",
        ]
        return "\n".join(lines)


def missing(ids, text):
    return [i for i in ids if i not in text]


def openapi_operations(spec):
    ops = set()
    for path, item in spec["paths"].items():
        for method, op in item.items():
            if method in {"get", "post", "put", "delete", "patch"}:
                ops.add((method.upper(), path, op["operationId"]))
    return ops


def app_routes():
    from app.main import create_app  # noqa: PLC0415 — optional until Phase 6

    routes = set()

    def walk(items, prefix=""):
        for r in items:
            if hasattr(r, "original_router"):  # FastAPI >= 0.16x wraps included routers
                walk(r.original_router.routes, prefix + r.include_context.prefix)
                continue
            path = prefix + getattr(r, "path", "")
            if path.startswith("/api"):
                for m in (getattr(r, "methods", None) or set()) - {"HEAD", "OPTIONS"}:
                    routes.add((m, path))

    walk(create_app().routes)
    return routes


def main(write=False):
    el = yaml.load((DESIGN / "elements.yaml").read_text(encoding="utf-8"))
    rep = Report()
    cmp_ids = [c["id"] for c in el["components"]]
    act_ids = [a["id"] for a in el["actors"]]

    sad = read("docs/04-design/SAD.md")
    blueprint = read("docs/04-design/blueprint.md")
    comp_dia = read("docs/04-design/diagrams/component_diagram.drawio")
    rep.check("SAD", "mọi CMP có trong SAD §5.2", not missing(cmp_ids, sad), ", ".join(missing(cmp_ids, sad)))
    rep.check(
        "Blueprint",
        "mọi CMP có trong composition view",
        not missing(cmp_ids, blueprint),
        ", ".join(missing(cmp_ids, blueprint)),
    )
    rep.check(
        "Component diagram",
        "mọi CMP có trong sơ đồ",
        not missing(cmp_ids, comp_dia),
        ", ".join(missing(cmp_ids, comp_dia)),
    )
    for c in el["components"]:
        if c["module"] not in sad:
            rep.check("SAD", f"{c['id']} module `{c['module']}` khớp", False, "module không có trong SAD")

    spec = yaml.load((DESIGN / "openapi.yaml").read_text(encoding="utf-8"))
    spec_ops = openapi_operations(spec)
    reg_ops = {(e["method"], e["path"], e["operationId"]) for e in el["endpoints"]}
    rep.check(
        "openapi.yaml",
        "endpoint trong registry ⊆ openapi",
        reg_ops <= spec_ops,
        ", ".join(f"{m} {p}" for m, p, _ in sorted(reg_ops - spec_ops)),
    )
    rep.check(
        "openapi.yaml",
        "không có endpoint ngoài registry",
        spec_ops <= reg_ops,
        ", ".join(f"{m} {p}" for m, p, _ in sorted(spec_ops - reg_ops)),
    )
    api_md = read("docs/04-design/openapi.md")
    op_missing = [e["operationId"] for e in el["endpoints"] if e["operationId"] not in api_md]
    rep.check("openapi.md", "mọi operationId được mô tả", not op_missing, ", ".join(op_missing))
    bad_cmp = [e["operationId"] for e in el["endpoints"] if e["component"] not in cmp_ids]
    rep.check("Registry", "endpoint gán cho CMP tồn tại", not bad_cmp, ", ".join(bad_cmp))

    schema = read("app/schema.sql")
    model = read("docs/04-design/data/model.md")
    class_dia = read("docs/04-design/diagrams/class_diagram.drawio")
    tables_sql = set(re.findall(r"CREATE TABLE IF NOT EXISTS (\w+)", schema))
    reg_tables = {e["table"] for e in el["entities"]}
    rep.check(
        "schema.sql",
        "bảng trong registry = bảng trong DDL",
        reg_tables == tables_sql,
        f"thiếu {sorted(reg_tables - tables_sql)}, thừa {sorted(tables_sql - reg_tables)}",
    )
    for e in el["entities"]:
        rep.check(
            "data/model.md", f"{e['id']} `{e['table']}` được mô tả", e["id"] in model and e["table"] in model
        )
        rep.check(
            "Class diagram",
            f"{e['id']} {e['name']} có trong sơ đồ",
            e["id"] in class_dia and e["name"] in class_dia,
        )

    uc = read("docs/04-design/diagrams/use_case_diagram.drawio")
    rep.check(
        "Use case diagram",
        "mọi actor có trong sơ đồ",
        not missing(act_ids, uc),
        ", ".join(missing(act_ids, uc)),
    )
    seq = read("docs/04-design/diagrams/sequence_diagram.drawio")
    for cid in ["CMP-03", "CMP-06", "CMP-07", "CMP-08", "CMP-11"]:
        rep.check("Sequence diagram", f"{cid} tham gia luồng hỏi đáp", cid in seq)
    dep = read("docs/04-design/diagrams/deployment_diagram.drawio")
    rep.check(
        "Deployment diagram",
        "CMP-01, CMP-11, CMP-12 và ACT-04 được triển khai",
        not missing(["CMP-01", "CMP-11", "CMP-12", "ACT-04"], dep),
    )

    prd = read("docs/03-analysis/PRD.md")
    frs = sorted(set(re.findall(r"\| (FR-\d{3}) \|", prd)))
    covered_text = sad + " ".join(r for e in el["endpoints"] for r in e["req"])
    fr_missing = [f for f in frs if f not in covered_text]
    rep.check(
        "PRD → Design",
        f"{len(frs)} FR đều có CMP/endpoint",
        bool(frs) and not fr_missing,
        ", ".join(fr_missing),
    )

    adrs = sorted(p.name for p in (DESIGN / "adr").glob("ADR-*.md"))
    adr_missing = [a for a in adrs if a not in sad]
    rep.check(
        "ADR",
        f"{len(adrs)} ADR (≥ 3) đều được SAD §9 tham chiếu",
        len(adrs) >= 3 and not adr_missing,
        ", ".join(adr_missing),
    )

    proto_missing = [s["prototype"] for s in el["screens"] if not (DESIGN / s["prototype"]).exists()]
    rep.check("UI/UX", "mọi màn hình có prototype", not proto_missing, ", ".join(proto_missing))

    if (ROOT / "app" / "main.py").exists():
        mod_missing = [c["module"] for c in el["components"] if not (ROOT / c["module"]).exists()]
        rep.check("Code", "mọi module của CMP tồn tại", not mod_missing, ", ".join(mod_missing))
        from app.errors import MESSAGES  # noqa: PLC0415

        enum = set(spec["components"]["schemas"]["Problem"]["properties"]["code"]["enum"])
        rep.check(
            "Code ↔ openapi.yaml",
            "enum Problem.code = mã lỗi trong app/errors.py",
            enum == set(MESSAGES),
            f"chỉ ở openapi {sorted(enum - set(MESSAGES))}, chỉ ở code {sorted(set(MESSAGES) - enum)}",
        )
        routes = app_routes()
        reg_routes = {(m, p) for m, p, _ in reg_ops}
        rep.check(
            "Code",
            "route FastAPI = endpoint registry",
            routes == reg_routes,
            f"thiếu {sorted(reg_routes - routes)}, thừa {sorted(routes - reg_routes)}",
        )
    else:
        rep.note("Code", "module và route khớp registry", "chưa có app/main.py (trước Phase 6)")

    report = rep.markdown()
    print(report)
    if write:
        (DESIGN / "cross-view-audit.md").write_text(report, encoding="utf-8")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main(write="--write" in sys.argv))
