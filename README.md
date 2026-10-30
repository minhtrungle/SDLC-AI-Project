# SDLC-AI-Project
Software Development Life Cycle with AI

Dự án thực hành [Agentic SDLC](docs/agentic-sdlc-process.md): sản phẩm **"Chat với tài liệu"** (MVP) đi qua Phase 1–8, từ Intake đến Verify & Review. Mỗi phase để lại artifact riêng.

**Sản phẩm:** ứng dụng web để tải lên PDF và hỏi đáp bằng tiếng Việt. Câu trả lời chỉ lấy từ tài liệu và kèm trích dẫn tên tài liệu + số trang. Mặc định xử lý hoàn toàn cục bộ, không gửi dữ liệu ra ngoài.

## Cấu trúc
```
app/
├── api-contract/   openapi.yaml — hợp đồng API dùng chung
├── backend/        Python (FastAPI, SQLite + FTS5) — package cwd, tests/
├── frontend/       Vue 3 + TypeScript + Vite
└── e2e/            Playwright E2E (backend thật + bản build Vue)
docs/               artifact Phase 1–8, prompts/, checklists/
test_reports/       kết quả E2E Playwright: report.md, results.json, screenshots/*.png, videos/*.mp4, html/
tools/              cổng chất lượng L0, cross-view audit, truy vết, sinh sơ đồ
```

## Chạy nhanh
Yêu cầu: Python ≥ 3.12 và Node.js ≥ 22.12. Không cần Docker, cơ sở dữ liệu ngoài hay API key.
```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r app/backend/requirements-dev.txt     # Linux/macOS: .venv/bin/python
npm ci --prefix app/frontend && npm run build --prefix app/frontend        # build giao diện vào app/frontend/dist

cd app/backend
../../.venv/Scripts/python -m cwd.cli seed-demo        # in ra mật khẩu của linh (user) và hung (manager)
../../.venv/Scripts/python -m uvicorn cwd.main:app     # mở http://127.0.0.1:8000
```
Khi phát triển giao diện: chạy uvicorn như trên, rồi `npm run dev` trong `app/frontend` (http://localhost:5173, tự proxy `/api`).

E2E: `npm ci --prefix app/e2e`, rồi `npm test` trong `app/e2e` (tự khởi động backend với dữ liệu sạch), rồi `python tools/e2e_report.py` ở gốc repo để sinh `test_reports/` (ảnh chụp, video mp4, report.md, results.json).

## Artifact theo phase
| Phase | Artifact |
|---|---|
| 1 Intake | [intent](docs/01-intake/intent.md) · [glossary](docs/01-intake/glossary.md) · [stakeholders](docs/01-intake/stakeholders.md) · [sources](docs/01-intake/sources.md) |
| 2 Requirements | [BRD v0.2](docs/02-requirements/BRD.md) · [audit IEEE 29148](docs/02-requirements/BRD_checklist_audit.md) |
| 3 Analysis | [PRD v0.2 (FR/NFR)](docs/03-analysis/PRD.md) · [USER_STORIES](docs/03-analysis/USER_STORIES.md) · [traceability](docs/03-analysis/traceability.md) |
| 4 Design | [SAD v0.4](docs/04-design/SAD.md) · [ADR-001..009](docs/04-design/adr/) · [blueprint](docs/04-design/blueprint.md) · [API contract](app/api-contract/openapi.yaml) · [data model](docs/04-design/data/model.md) · [use cases](docs/04-design/use_cases.md) · [diagrams](docs/04-design/diagrams/) · [UI/UX](docs/04-design/UI_UX_design/README.md) · [audits](docs/04-design/design_checklist_audit.md) · [refine log](docs/04-design/design-refine-log.md) |
| 5 Planning | [PLAN](docs/05-implement/PLAN.md) · [tasks/](docs/05-implement/tasks/) |
| 6 Build | [AGENTS.md](AGENTS.md) · [app/backend](app/backend/) · [app/frontend](app/frontend/) · [app/api-contract](app/api-contract/) |
| 7–8 Verify & Review | [test plan](docs/07-verification/testing/test-plan.md) · [test report](docs/07-verification/testing/test-report.md) · [E2E report (ảnh + video)](test_reports/report.md) · [CI log](docs/07-verification/ci/ci-log.txt) · [L1 review vòng 1](docs/07-verification/code-review/code-review-L1.md) · [vòng 2](docs/07-verification/code-review/code-review-L1-round2.md) · [review record](docs/07-verification/code-review/review-record.md) · [eval report](docs/07-verification/eval/eval-report.json) |

## Công cụ của quy trình
| Lệnh (từ gốc repo) | Việc |
|---|---|
| `python tools/ci_local.py` | Cổng L0: format/lint Python, quét secret, quét lỗ hổng phụ thuộc (pip + npm), cross-view audit, truy vết, test + coverage backend, kiểm tra lệch hợp đồng API, lint/type-check/test/build frontend, Playwright E2E |
| `python tools/cross_view_audit.py --write` | Kiểm tra nhất quán giữa các view thiết kế, hợp đồng API và code |
| `python tools/trace_matrix.py` | Sinh lại ma trận truy vết BR → FR → US → AC → CMP → code → test (backend + frontend) |
| `python tools/gen_diagrams.py` | Sinh lại 6 sơ đồ draw.io từ `elements.yaml` |
| `python tools/checklist_fill.py <xlsx> <audit.md> <out.xlsx>` | Ghi kết quả audit markdown vào checklist Excel |

## Phê duyệt
Agent sinh nội dung nhưng không tự phê duyệt, merge hay deploy. Mọi bảng phê duyệt trong tài liệu đang chờ người có trách nhiệm ký.
