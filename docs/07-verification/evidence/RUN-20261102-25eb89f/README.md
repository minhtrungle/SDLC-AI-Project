# Evidence run RUN-20261102-25eb89f

| Mục | Giá trị |
|---|---|
| Ngày | 2026-11-02 20:40–20:48 (giờ máy) |
| Commit | `25eb89fcefc22945ef8c9101f00cefc20af0b139` trên nhánh `feat/chat-with-docs-sdlc`, kèm thay đổi chưa commit chỉ nằm trong `docs/` và `tools/rtm.py`, không chạm `app/` |
| Môi trường | Windows 10 Pro 19044 · Python 3.15.2 · Node 22.23.4 · Chromium (Playwright) · không Docker |
| Người chạy | Agent (Claude). QA (STK-006) cần xác nhận lại. |

## Kết quả
| Bước | Kết quả | File |
|---|---|---|
| Cổng L0 (`tools/ci_local.py`) | **16/17 PASS**, 427 s. FAIL: `py-dependency-audit` | [ci-log.txt](ci-log.txt) · [ci-stdout.txt](ci-stdout.txt) |
| Backend pytest | 138 passed, coverage 97,73% | [backend-junit.xml](backend-junit.xml) · [backend-pytest.txt](backend-pytest.txt) |
| Frontend Vitest | 49 passed | [frontend-junit.xml](frontend-junit.xml) · [frontend-vitest.txt](frontend-vitest.txt) |
| Playwright E2E | 20/20 passed; mỗi test có ảnh, video mp4 và report.md | [test_reports/report.md](../../../../test_reports/report.md) |
| Eval AI (bộ tổng hợp 32 câu, 50 tài liệu) | Đúng 100% · trích dẫn đúng 100% · not_found 100% · P90 35,6 ms · diễn đạt khác 12,5% (không chặn) | [eval-report.json](eval-report.json) |
| RTM | 58 AC: 57 PASS, 1 chờ review (AC-102.3), 0 GAP | [RTM.md](../../testing/RTM.md) |

## Defect phát hiện trong lần chạy
| ID | Mức | Mô tả | Trạng thái |
|---|---|---|---|
| DEF-001 | Major (bảo mật, phụ thuộc) | `pip-audit` báo 3 CVE mới cho `pypdf 6.21.3` (CVE-2026-119203/119204/119205); bản sửa là 6.21.4. Lần chạy ngày 2026-10-28 chưa có các CVE này. | Open. Cần Tech Lead duyệt nâng `pypdf` trong `app/backend/requirements.txt`, rồi chạy lại toàn bộ cổng L0. |
| DEF-002 | Minor (bằng chứng) | `tests/eval/test_eval.py` ghi ra `docs/07-verification/eval-report.json`, nhưng TEST_PLAN và TEST_REPORT lại trỏ tới `docs/07-verification/eval/eval-report.json` (bản cũ, ngày 2026-10-28). Bản mới của lần chạy này đã được chuyển vào thư mục này. | Open. Cần sửa đường dẫn trong test hoặc trong tài liệu (Tech Lead). |

## Cách tái lập
```bash
# từ gốc repo, sau khi cài theo AGENTS.md
R=docs/07-verification/evidence/<run-id>
.venv/Scripts/python tools/ci_local.py --log $R/ci-log.txt
cd app/backend && ../../.venv/Scripts/python -m pytest -p no:cacheprovider -q --junitxml=../../$R/backend-junit.xml
cd ../frontend && npx vitest run --reporter=default --reporter=junit --outputFile.junit=../../$R/frontend-junit.xml
cd ../.. && .venv/Scripts/python tools/rtm.py <run-id>   # sinh lại TEST_CASES.md và RTM.md
```
