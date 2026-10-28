"""Turn a Playwright run into test_reports/: one folder per test with its own evidence.

Usage: python tools/e2e_report.py   (after `npm test` in app/e2e)

    test_reports/
    ├── report.md          index: summary + one row per test, linking to its folder
    ├── results.json       full Playwright JSON report of the run
    └── <feature>-<NN>-<test-slug>/
        ├── screenshot.png  final screenshot of the test's page
        ├── video.mp4       whole test, H.264 (converted from Playwright's webm with imageio-ffmpeg)
        ├── report.md       criteria, result, duration, steps (the test's code), video, screenshot
        └── result.json     this test's result only

Raw artifacts in test_reports/.raw are removed afterwards. Exit code 1 if any test did not pass.
"""

import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unicodedata

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "test_reports"
RESULTS = OUT / "results.json"
E2E_TESTS = ROOT / "app" / "e2e" / "tests"
FEATURES = {  # spec file -> (folder prefix, feature name)
    "auth.spec.ts": ("dang-nhap", "Đăng nhập và phiên"),
    "documents.spec.ts": ("tai-lieu", "Quản lý tài liệu"),
    "chat.spec.ts": ("hoi-dap", "Hỏi đáp có trích dẫn"),
    "access.spec.ts": ("phan-quyen", "Cô lập dữ liệu và phân quyền"),
}
STATUS_LABEL = {
    "passed": "✅ Đạt",
    "failed": "❌ Lỗi",
    "timedOut": "⏱ Quá giờ",
    "skipped": "⏭ Bỏ qua",
    "interrupted": "⛔ Dừng",
}
ANSI = re.compile(r"\x1b\[[0-9;]*m")
KEEP = {"results.json", "results.xml", "html", ".raw"}  # outputs of the Playwright run itself


def slug(text: str, limit: int = 55) -> str:
    folded = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    ascii_text = "".join(ch for ch in folded if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")[:limit].rstrip("-")


def collect(suite: dict, spec_file: str = "", describe: str = ""):
    """Yield (spec file, describe title, spec entry, last result) for every test in the JSON report."""
    spec_file = suite.get("file", spec_file)
    title = suite.get("title", "")
    describe = describe if title.endswith(".ts") else title  # top-level suites are titled by file
    for spec in suite.get("specs", []):
        for test in spec["tests"]:
            yield spec_file, describe, spec, test["results"][-1]
    for child in suite.get("suites", []):
        yield from collect(child, spec_file, describe)


def attachment(result: dict, name: str) -> pathlib.Path | None:
    found = [
        pathlib.Path(a["path"])
        for a in result.get("attachments", [])
        if a.get("name") == name and a.get("path") and pathlib.Path(a["path"]).exists()
    ]
    # Playwright captures every page of the test: test-finished-1 is the test's own page (also the
    # recorded one); later ones are helper contexts (e.g. another user setting up data) closed earlier.
    return found[0] if found else None


def to_mp4(src: pathlib.Path, dst: pathlib.Path) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", "-i", str(src), "-c:v", "libx264", "-pix_fmt", "yuv420p"]
        + ["-preset", "veryfast", "-crf", "28", "-movflags", "+faststart", "-an", str(dst)],
        check=True,
    )


def test_source(spec_file: str, line: int) -> str:
    """The test's code from its declaration line to its closing `});` — the steps it performs."""
    path = E2E_TESTS / spec_file
    if not path.exists():
        return ""
    depth, out = 0, []
    for text in path.read_text(encoding="utf-8").splitlines()[line - 1 :]:
        out.append(text)
        depth += text.count("{") - text.count("}")
        if depth <= 0 and text.strip().startswith("});"):
            break
    indent = min((len(t) - len(t.lstrip()) for t in out if t.strip()), default=0)
    return "\n".join(t[indent:] for t in out)


def criteria(title: str) -> str:
    return ", ".join(dict.fromkeys(re.findall(r"(?:AC|EC)-[\w.-]+\d", title))) or "—"


def write_test_folder(folder: pathlib.Path, n: int, spec_file: str, describe: str, spec: dict, result: dict):
    folder.mkdir(parents=True)
    title = spec["title"]
    shot, video = attachment(result, "screenshot"), attachment(result, "video")
    if shot:
        shutil.copyfile(shot, folder / "screenshot.png")
    if video:
        to_mp4(video, folder / "video.mp4")
    status = result["status"]
    errors = [ANSI.sub("", e.get("message", "")) for e in result.get("errors", [])]
    record = {
        "id": n,
        "feature": FEATURES.get(spec_file, ("", spec_file))[1],
        "group": describe,
        "title": title,
        "criteria": criteria(title),
        "spec": f"app/e2e/tests/{spec_file}:{spec.get('line')}",
        "status": status,
        "duration_ms": result.get("duration", 0),
        "retry": result.get("retry", 0),
        "start_time": result.get("startTime"),
        "errors": errors,
        "evidence": {
            "screenshot": "screenshot.png" if shot else None,
            "video": "video.mp4" if video else None,
        },
    }
    (folder / "result.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    md = [
        f"# {n:02d}. {title}",
        "",
        "| Mục | Giá trị |",
        "|---|---|",
        f"| Chức năng | {record['feature']} |",
        f"| Nhóm | {describe} |",
        f"| Tiêu chí chấp nhận | {record['criteria']} |",
        f"| Kết quả | {STATUS_LABEL.get(status, status)} |",
        f"| Thời gian chạy | {record['duration_ms'] / 1000:.1f} s |",
        f"| Bắt đầu (UTC) | {(record['start_time'] or '')[:19].replace('T', ' ')} |",
        f"| Mã test | `{record['spec']}` |",
        "",
        "Tệp: [screenshot.png](screenshot.png) · [video.mp4](video.mp4) · [result.json](result.json) · "
        "[← Mục lục](../report.md)",
        "",
    ]
    if errors:
        md += ["## Lỗi", "", "```", *(e[:2000] for e in errors), "```", ""]
    md += [
        "## Các bước kiểm thử (mã Playwright)",
        "",
        "```ts",
        test_source(spec_file, spec.get("line", 1)),
        "```",
        "",
    ]
    if video:
        md += [
            "## Video",
            "",
            '<video src="video.mp4" controls width="960"></video>',
            "",
            "[Mở video.mp4](video.mp4)",
            "",
        ]
    if shot:
        md += ["## Ảnh chụp màn hình cuối test", "", f"![{title}](screenshot.png)", ""]
    (folder / "report.md").write_text("\n".join(md), encoding="utf-8")
    return record


def main() -> int:
    if not RESULTS.exists():
        print(f"{RESULTS} not found: run `npm test` in app/e2e first.", file=sys.stderr)
        return 1
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    for child in OUT.iterdir():  # drop folders/files of previous runs
        if child.name not in KEEP:
            shutil.rmtree(child) if child.is_dir() else child.unlink()

    records, rows = [], []
    for n, (spec_file, describe, spec, result) in enumerate(
        [t for s in data["suites"] for t in collect(s)], 1
    ):
        prefix = FEATURES.get(spec_file, (slug(spec_file.removesuffix(".spec.ts")), ""))[0]
        name = f"{prefix}-{n:02d}-{slug(spec['title'])}"
        record = write_test_folder(OUT / name, n, spec_file, describe, spec, result)
        records.append(record)
        rows.append(
            f"| {n} | {record['feature']} | [{spec['title']}]({name}/report.md) | "
            f"{STATUS_LABEL.get(record['status'], record['status'])} | {record['duration_ms'] / 1000:.1f} s | "
            f"[ảnh]({name}/screenshot.png) · [video]({name}/video.mp4) · [json]({name}/result.json) |"
        )

    stats = data.get("stats", {})
    passed = sum(1 for r in records if r["status"] == "passed")
    index = [
        "# Báo cáo kiểm thử E2E (Playwright) — Chat với tài liệu",
        "",
        "> Sinh tự động bởi `python tools/e2e_report.py` sau khi chạy `npm test` trong `app/e2e`. Không sửa tay.",
        "> Mỗi test có một thư mục riêng chứa `screenshot.png`, `video.mp4`, `report.md` và `result.json`.",
        "",
        "| Mục | Giá trị |",
        "|---|---|",
        f"| Thời điểm chạy (UTC) | {stats.get('startTime', '')[:19].replace('T', ' ')} |",
        f"| Thời lượng | {stats.get('duration', 0) / 1000:.1f} s |",
        f"| Tổng số test | {len(records)} |",
        f"| Đạt | {passed} |",
        f"| Lỗi | {stats.get('unexpected', 0)} |",
        f"| Chập chờn (flaky) | {stats.get('flaky', 0)} |",
        f"| Bỏ qua | {stats.get('skipped', 0)} |",
        "| Trình duyệt | Chromium (Google Chrome trên máy dev), 1280×800, locale vi-VN |",
        "| Môi trường | Backend FastAPI thật + bản build Vue; dữ liệu sạch mỗi lần chạy (`app/e2e/serve.py`) |",
        f"| Sinh báo cáo lúc | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} |",
        "",
        "Kết quả đầy đủ: [results.json](results.json) · JUnit: [results.xml](results.xml) · "
        "HTML của Playwright: [html/index.html](html/index.html)",
        "",
        "## Kết quả theo test",
        "",
        "| # | Chức năng | Test (tiêu chí chấp nhận) | Kết quả | Thời gian | Bằng chứng |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
    ]
    (OUT / "report.md").write_text("\n".join(index), encoding="utf-8")
    shutil.rmtree(OUT / ".raw", ignore_errors=True)  # raw webm/png/trace are not kept
    print(f"report: {OUT / 'report.md'} · {len(records)} test folders · {passed}/{len(records)} passed")
    return 0 if passed == len(records) else 1


if __name__ == "__main__":
    sys.exit(main())
