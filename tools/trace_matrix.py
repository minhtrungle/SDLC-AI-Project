"""Regenerate docs/03-analysis/traceability.md: BR -> FR/NFR -> US -> AC -> design -> code -> tests.

Sources of truth:
- rows (BR, FR/NFR, story, AC range): ROWS below, copied from PRD §3.9 / USER_STORIES.md
- design: components whose endpoints list the FR (elements.yaml) or SAD §5.2 rows mentioning it
- code: module paths of those components
- tests: test functions whose docstring mentions an AC id of the row

Usage: python tools/trace_matrix.py   (exit 1 if an in-scope row has no test)
"""

import ast
import pathlib
import re
import sys

from ruamel.yaml import YAML

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "03-analysis" / "traceability.md"

# (BR, FR/NFR ids, story, AC prefixes)
ROWS = [
    ("BR-019", ["FR-001", "FR-002", "NFR-010"], "US-101", ["AC-101.", "AC-NFR-010"]),
    ("BR-020", ["FR-003"], "US-102", ["AC-102."]),
    ("BR-026", ["FR-019", "NFR-007"], "US-103", ["AC-103."]),
    ("BR-001", ["FR-004"], "US-201", ["AC-201."]),
    ("BR-002", ["FR-005"], "US-202", ["AC-202."]),
    ("BR-003", ["FR-006"], "US-203", ["AC-203."]),
    ("BR-004", ["FR-007"], "US-204", ["AC-204."]),
    ("BR-005, BR-006", ["FR-008"], "US-205", ["AC-205.", "AC-006"]),
    ("BR-007, BR-014", ["FR-009", "NFR-003"], "US-301", ["AC-301."]),
    ("BR-008", ["FR-010"], "US-302", ["AC-302."]),
    ("BR-009", ["FR-011"], "US-303", ["AC-303."]),
    ("BR-010", ["FR-012"], "US-304", ["AC-304."]),
    ("BR-011", ["FR-013"], "US-305", ["AC-305."]),
    ("BR-012, BR-013", ["NFR-001", "NFR-002"], "US-306", ["AC-306."]),
    ("BR-015", ["FR-014"], "US-401", ["AC-401."]),
    ("BR-016", ["FR-015"], "US-402", ["AC-402."]),
    ("BR-017", ["FR-016"], "US-403", ["AC-403."]),
    ("BR-021", ["FR-017"], "US-501", ["AC-501."]),
    ("BR-022", ["FR-018"], "US-502", ["AC-502."]),
    ("BR-024", ["NFR-005"], "—", ["NFR-005"]),
    ("BR-025", ["NFR-006"], "—", ["NFR-006", "AC-025"]),
    ("BR-027", ["NFR-008"], "—", ["AC-NFR-008", "NFR-008"]),
    ("BR-028", ["NFR-004"], "—", ["AC-NFR-004", "NFR-004"]),
]
# Non-functional rows whose design lives in a cross-cutting module rather than an endpoint.
EXTRA_MODULES = {
    "NFR-001": ["app/retrieval.py"],
    "NFR-002": ["app/retrieval.py", "app/generation.py"],
    "NFR-003": ["app/textnorm.py"],
    "NFR-004": ["app/auth.py"],
    "NFR-006": ["app/cli.py"],
    "NFR-007": ["app/audit.py", "app/cli.py"],
    "NFR-008": ["app/main.py"],
    "NFR-010": ["app/security.py"],
}
DEFERRED = [("BR-018", "US-404"), ("BR-023", "US-601")]


def collect_tests():
    found = []  # (test id, docstring)
    for path in sorted((ROOT / "tests").rglob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                doc = ast.get_docstring(node) or ""
                found.append((f"{path.relative_to(ROOT).as_posix()}::{node.name}", doc))
    return found


def main():
    el = YAML(typ="safe", pure=True).load((ROOT / "docs/04-design/elements.yaml").read_text(encoding="utf-8"))
    modules = {c["id"]: c["module"] for c in el["components"]}
    sad = (ROOT / "docs/04-design/SAD.md").read_text(encoding="utf-8")
    sad_rows = [line for line in sad.splitlines() if re.match(r"\| CMP-\d\d \|", line)]
    tests = collect_tests()

    lines = [
        "# Ma trận truy vết — BR → FR/NFR → US → AC → Thiết kế → Code → Test",
        "",
        "> Sinh tự động bởi `python tools/trace_matrix.py` (Phase 6 ↻). Không sửa tay.",
        "> Test được gắn với AC qua ID trong docstring. Thiết kế lấy từ `elements.yaml` + SAD §5.2.",
        "",
        "| BR | FR/NFR | Story | AC | Thiết kế (CMP) | Code | Test |",
        "|---|---|---|---|---|---|---|",
    ]
    missing = []
    for br, reqs, story, prefixes in ROWS:
        cmps = sorted(
            {e["component"] for e in el["endpoints"] if set(e["req"]) & set(reqs)}
            | {row.split("|")[1].strip() for row in sad_rows if any(r in row for r in reqs)}
        )
        code = sorted({modules[c] for c in cmps} | {m for r in reqs for m in EXTRA_MODULES.get(r, [])})
        hits = [tid for tid, doc in tests if any(p in doc for p in prefixes)]
        if not hits:
            missing.append(story if story != "—" else br)
        acs = (
            ", ".join(
                sorted(
                    {
                        m
                        for _, doc in tests
                        for m in re.findall(r"AC-[\w.-]+\d", doc)
                        if any(m.startswith(p.rstrip(".")) for p in prefixes)
                    }
                )
            )
            or "—"
        )
        test_cell = "<br>".join(f"`{h.split('::')[1]}`" for h in hits) or "**THIẾU**"
        lines.append(
            f"| {br} | {', '.join(reqs)} | {story} | {acs} | {', '.join(cmps) or '—'} | "
            f"{'<br>'.join(f'`{m}`' for m in code) or '—'} | {test_cell} |"
        )
    for br, story in DEFERRED:
        lines.append(f"| {br} | — | {story} | — | Hoãn (P2, BRD §12.1) | — | — |")
    lines += [
        "",
        "## Độ phủ",
        f"- Hàng trong phạm vi: {len(ROWS)}; thiếu test: {', '.join(missing) if missing else 'không có'}.",
        f"- Tổng số test function: {len(tests)}; có ID AC/NFR trong docstring: "
        f"{sum(1 for _, d in tests if re.search(r'AC-|NFR-', d))}.",
        "- AC chỉ kiểm chứng bằng review (không tự động hóa): AC-102.3 (IT ký luồng dữ liệu), "
        "AC-201.3 / AC-204.2 / AC-305.2 / AC-402.2 phần giao diện (kiểm chứng bằng UI E2E thủ công, "
        "xem test-report §4), NFR-009 (inspection WCAG).",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}; rows without tests: {missing or 'none'}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
