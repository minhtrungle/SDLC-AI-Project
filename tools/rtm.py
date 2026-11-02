"""Generate docs/07-verification/testing/TEST_CASES.md and RTM.md (IEEE 829) from acceptance criteria.

One test case TC-<ac> per acceptance criterion in USER_STORIES.md (Given → preconditions, When → steps,
Then → expected result). A case is proven by the automated tests that carry the AC id (same convention
as trace_matrix.py). Results come from one evidence run:

    docs/07-verification/evidence/<run-id>/backend-junit.xml   pytest --junitxml
    docs/07-verification/evidence/<run-id>/frontend-junit.xml  vitest --reporter=junit
    test_reports/<test>/result.json                            Playwright via tools/e2e_report.py

An AC with no case is recorded as GAP, never left blank.

Usage: python tools/rtm.py <run-id>   (exit 1 if an AC has a GAP or a linked test did not pass)
"""

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from trace_matrix import collect_tests  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
STORIES = ROOT / "docs" / "03-analysis" / "USER_STORIES.md"
OUT_DIR = ROOT / "docs" / "07-verification" / "testing"
E2E_DIR = ROOT / "test_reports"

# ACs verified by review/inspection instead of an automated test: (method, owner).
REVIEW_ONLY = {
    "AC-102.3": ("Review: IT/Bảo mật ký luồng dữ liệu SAD §8", "IT/Bảo mật (STK-005)"),
}
LEVEL = {"backend": "BE", "frontend": "FE", "e2e": "E2E"}
# Cross-cutting NFR acceptance criteria have no story row; their BR comes from PRD §3.9.
NFR_BR = {"NFR-004": "BR-028", "NFR-008": "BR-027", "NFR-010": "BR-019"}


def parse_stories():
    text = STORIES.read_text(encoding="utf-8")
    overview = {}
    for m in re.finditer(r"^\| (US-\d+) \| ([^|]+) \| (P\d) \| ([^|]+) \| ([^|]+) \|", text, re.M):
        overview[m.group(1)] = (m.group(2).strip(), m.group(3), m.group(4).strip(), m.group(5).strip())
    acs, story = [], "—"
    for line in text.splitlines():
        h = re.match(r"### (US-\d+)", line)
        if h:
            story = h.group(1)
        elif line.startswith("## Yêu cầu xuyên suốt"):
            story = "—"
        a = re.match(r"- \*\*(AC-[\w.-]+?)\*\* (.*)", line)
        if a:
            title, prio, reqs, br = overview.get(story, ("Cô lập workspace, log sạch, bảo mật", "P0", "", ""))
            if story == "—":
                reqs = a.group(1).removeprefix("AC-")
                br = NFR_BR.get(reqs, "—")
            acs.append(
                {
                    "ac": a.group(1),
                    "text": a.group(2),
                    "story": story,
                    "title": title,
                    "prio": prio,
                    "reqs": reqs,
                    "br": br,
                }
            )
    return acs


def split_gwt(text):
    """Given/When/Then, or 'condition → result'; returns (pre, steps, expected)."""
    m = re.match(r"Given (.*?)(?:, When (.*?))?, Then (.*)", text)
    if m:
        return m.group(1), m.group(2) or "—", m.group(3)
    if "→" in text:
        cond, _, exp = text.partition("→")
        return "—", cond.strip(), exp.strip()
    return "—", "—", text


def load_results(run_dir):
    res = {}  # (level, key) -> status
    be = run_dir / "backend-junit.xml"
    if be.exists():
        for tc in ET.parse(be).iter("testcase"):
            # Parametrized cases (test_x[param]) count as one test that passes only if every variant passes.
            key = ("backend", tc.get("name").split("[")[0])
            if res.get(key) in (None, "passed"):
                res[key] = _status(tc)
    fe = run_dir / "frontend-junit.xml"
    if fe.exists():
        for tc in ET.parse(fe).iter("testcase"):
            res[("frontend", tc.get("name").split(" > ")[-1])] = _status(tc)
    e2e = {}
    for p in sorted(E2E_DIR.glob("*/result.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        res[("e2e", r["title"])] = "passed" if r["status"] in ("passed", "expected") else r["status"]
        e2e[r["title"]] = p.parent.name
    return res, e2e


def _status(tc):
    if tc.find("failure") is not None or tc.find("error") is not None:
        return "failed"
    return "skipped" if tc.find("skipped") is not None else "passed"


def level_of(test_id):
    return "e2e" if test_id.startswith("app/e2e/") else "frontend" if "/frontend/" in test_id else "backend"


def main(run_id):
    run_dir = ROOT / "docs" / "07-verification" / "evidence" / run_id
    if not run_dir.is_dir():
        raise SystemExit(f"evidence run not found: {run_dir.relative_to(ROOT)}")
    acs = parse_stories()
    tests = collect_tests()
    results, e2e_dirs = load_results(run_dir)
    ev = f"../evidence/{run_id}"

    rows, gaps, failed = [], [], []
    for a in acs:
        pat = re.compile(re.escape(a["ac"]) + r"(?![\d.])")
        linked = []
        for tid, doc in tests:
            if pat.search(doc):
                lv = level_of(tid)
                name = tid.split("::")[1]
                linked.append((lv, tid, name, results.get((lv, name), "not run")))
        a["tc"] = "TC-" + a["ac"].removeprefix("AC-")
        a["tests"] = linked
        if not linked and a["ac"] not in REVIEW_ONLY:
            gaps.append(a["ac"])
        failed += [f"{a['ac']}: {n} ({s})" for _, _, n, s in linked if s != "passed"]
        rows.append(a)

    write_cases(rows, run_id)
    write_rtm(rows, tests, gaps, failed, run_id, ev, e2e_dirs, results)
    print(f"{len(rows)} AC -> TEST_CASES.md, RTM.md; GAP: {gaps or 'none'}; not passed: {len(failed)}")
    return 1 if gaps or failed else 0


def write_cases(rows, run_id):
    lines = [
        "# Test Cases (IEEE 829) — Chat với tài liệu (MVP)",
        "",
        "| Mục | Giá trị |",
        "|---|---|",
        "| Mã | TCS-CWD-001 v1.0 · thuộc [Test Plan TP-CWD-001](TEST_PLAN.md) |",
        "| Nguồn | Acceptance Criteria trong [USER_STORIES.md](../../03-analysis/USER_STORIES.md) |",
        f"| Sinh bởi | `python tools/rtm.py {run_id}` — không sửa tay |",
        "",
        "Mỗi AC có một test case `TC-<AC>`: **Tiền điều kiện** = mệnh đề Given, **Bước** = When, "
        "**Kết quả mong đợi** = Then. Dữ liệu cụ thể (PDF sinh bằng fpdf2, tài khoản, câu hỏi) nằm trong "
        "fixture của test tự động ở cột *Chứng minh bởi*. BE = pytest, FE = Vitest, E2E = Playwright.",
        "",
    ]
    for story in dict.fromkeys(r["story"] for r in rows):
        group = [r for r in rows if r["story"] == story]
        head = f"{story} — {group[0]['title']}" if story != "—" else "Yêu cầu xuyên suốt (NFR)"
        lines += [
            f"## {head} ({group[0]['prio']})",
            "",
            "| TC | AC | Tiền điều kiện | Bước | Kết quả mong đợi | Mức | Chứng minh bởi |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in group:
            pre, steps, exp = (c.replace("|", "\\|") for c in split_gwt(r["text"]))
            levels = "/".join(LEVEL[lv] for lv in LEVEL if any(t[0] == lv for t in r["tests"]))
            proof = "<br>".join(f"`{n}` ({LEVEL[lv]})" for lv, _, n, _ in r["tests"])
            if r["ac"] in REVIEW_ONLY:
                levels, proof = "Review", REVIEW_ONLY[r["ac"]][0]
            lines.append(
                f"| {r['tc']} | {r['ac']} | {pre} | {steps} | {exp} | {levels or '—'} | "
                f"{proof or '**GAP**'} |"
            )
        lines.append("")
    (OUT_DIR / "TEST_CASES.md").write_text("\n".join(lines), encoding="utf-8")


def write_rtm(rows, tests, gaps, failed, run_id, ev, e2e_dirs, results):
    def evidence(lv, name):
        if lv == "e2e" and name in e2e_dirs:
            return f"[E2E](../../../test_reports/{e2e_dirs[name]}/report.md)"
        return f"[{LEVEL[lv]}]({ev}/{lv}-junit.xml)"

    passed_ac = 0
    body = []
    for r in rows:
        if r["ac"] in REVIEW_ONLY:
            method, owner = REVIEW_ONLY[r["ac"]]
            body.append(
                f"| {r['br']} | {r['reqs']} | {r['story']} | {r['ac']} | {r['tc']} | {r['prio']} | — | "
                f"**PENDING REVIEW** | {method}; owner {owner} |"
            )
            continue
        if not r["tests"]:
            body.append(
                f"| {r['br']} | {r['reqs']} | {r['story']} | {r['ac']} | {r['tc']} | {r['prio']} | — | **GAP** | — |"
            )
            continue
        n_ok = sum(1 for t in r["tests"] if t[3] == "passed")
        counts = " · ".join(
            f"{LEVEL[lv]} {sum(1 for t in r['tests'] if t[0] == lv)}"
            for lv in LEVEL
            if any(t[0] == lv for t in r["tests"])
        )
        verdict = "PASS" if n_ok == len(r["tests"]) else "FAIL"
        passed_ac += verdict == "PASS"
        links = " ".join(dict.fromkeys(evidence(lv, n) for lv, _, n, _ in r["tests"]))
        body.append(
            f"| {r['br']} | {r['reqs']} | {r['story']} | {r['ac']} | {r['tc']} | {r['prio']} | {counts} | "
            f"**{verdict}** ({n_ok}/{len(r['tests'])}) | {links} |"
        )

    linked_ids = {t[1] for r in rows for t in r["tests"]}
    orphans = [tid for tid, _ in tests if tid not in linked_ids]
    executed = {lv: [v for (l2, _), v in results.items() if l2 == lv] for lv in LEVEL}
    lines = [
        "# Requirements Traceability Matrix (RTM) — Chat với tài liệu (MVP)",
        "",
        "| Mục | Giá trị |",
        "|---|---|",
        "| Mã | RTM-CWD-001 v1.0 · thuộc [Test Plan TP-CWD-001](TEST_PLAN.md) · "
        "case: [TEST_CASES.md](TEST_CASES.md) |",
        f"| Lần chạy | `{run_id}` — bằng chứng: [{ev}/]({ev}/) và [test_reports/](../../../test_reports/report.md) |",
        f"| Sinh bởi | `python tools/rtm.py {run_id}` — không sửa tay |",
        "",
        "## 1. Tóm tắt",
        "| Chỉ số | Giá trị |",
        "|---|---|",
        f"| Tổng AC | {len(rows)} |",
        f"| AC có test case tự động | {sum(1 for r in rows if r['tests'])} |",
        f"| AC PASS (mọi test liên kết đạt) | {passed_ac} |",
        f"| AC chờ review thủ công | {len(REVIEW_ONLY)} ({', '.join(REVIEW_ONLY)}) |",
        f"| GAP (AC không có case) | {len(gaps)}{' — ' + ', '.join(gaps) if gaps else ''} |",
        f"| Test liên kết không đạt / chưa chạy | {len(failed)} |",
        "| Test đã chạy trong lần này (BE: test có tham số tính là 1) | "
        + " · ".join(
            f"{LEVEL[lv]} {sum(v == 'passed' for v in executed[lv])}/{len(executed[lv])} pass" for lv in LEVEL
        )
        + " |",
        "",
        "## 2. Chiều xuôi: BR → FR/NFR → US → AC → TC → kết quả → bằng chứng",
        "| BR | FR/NFR | Story | AC | TC | Ưu tiên | Số test | Kết quả | Bằng chứng |",
        "|---|---|---|---|---|---|---|---|---|",
        *body,
        "",
        "## 3. Chiều ngược: test → AC",
        f"{len(linked_ids)}/{len(tests)} test tự động có ID AC và đã gắn vào ít nhất một dòng ở §2. "
        f"Test không mang ID AC ({len(orphans)}) là test hồi quy kỹ thuật (lỗi CR/NR/E2E, migration, "
        "đồng thời, tiện ích) và không chứng minh AC nào:",
        "",
        *(f"- `{t}`" for t in orphans),
        "",
    ]
    if failed:
        lines += ["## 4. Test liên kết không đạt", "", *(f"- {f}" for f in failed), ""]
    (OUT_DIR / "RTM.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(main(sys.argv[1]))
