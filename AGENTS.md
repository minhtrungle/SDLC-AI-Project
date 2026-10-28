# AGENTS.md — hướng dẫn cho agent AI và dev

Đọc file này trước khi sửa code. `docs/` là nguồn sự thật; code phải khớp thiết kế.

## Sản phẩm
"Chat với tài liệu" — MVP web hỏi đáp trên PDF, câu trả lời chỉ dựa trên tài liệu, kèm trích dẫn tên tài liệu + trang.
Yêu cầu: [PRD.md](docs/03-analysis/PRD.md) §3.9 · Story: [USER_STORIES.md](docs/03-analysis/USER_STORIES.md) · Kiến trúc: [SAD.md](docs/04-design/SAD.md) · Kế hoạch: [PLAN.md](docs/05-implement/PLAN.md).

## Cấu trúc (ADR-009)
```
app/
├── api-contract/openapi.yaml   hợp đồng API — nguồn sự thật cho cả hai phía
├── backend/                    Python ≥ 3.12, FastAPI, SQLite + FTS5 · package `cwd`, tests/
├── frontend/                   Vue 3 + TypeScript + Vite · Node ≥ 22.12
└── e2e/                        Playwright E2E — serve.py khởi động backend thật + dữ liệu sạch
tools/                          công cụ quy trình (cổng L0, audit, truy vết, sơ đồ)
docs/                           artifact theo phase 1–8
```
Mỗi module backend và thư mục `app/frontend/src` ứng với một thành phần `CMP-xx` trong [elements.yaml](docs/04-design/elements.yaml).

## Lệnh
```bash
# Backend (từ gốc repo)
python -m venv .venv && .venv/Scripts/python -m pip install -r app/backend/requirements-dev.txt
cd app/backend && ../../.venv/Scripts/python -m pytest          # test + coverage (≥ 70%)
cd app/backend && ../../.venv/Scripts/python -m cwd.cli seed-demo
cd app/backend && ../../.venv/Scripts/python -m uvicorn cwd.main:app   # http://127.0.0.1:8000

# Frontend
cd app/frontend && npm ci
npm run dev            # Vite :5173, proxy /api → :8000
npm run gen:api        # sinh src/api/schema.d.ts từ app/api-contract/openapi.yaml
npm run lint && npm run type-check && npm test && npm run build   # build → app/frontend/dist (backend phục vụ tại /)

# E2E (cần bản build frontend)
cd app/e2e && npm ci && npm test   # rồi: python tools/e2e_report.py → test_reports/ (ảnh, mp4, report.md)

# Toàn bộ cổng L0 như CI (từ gốc repo)
.venv/Scripts/python tools/ci_local.py
```

## Quy ước
- Conventional Commits; dòng cuối thân commit: `Refs: US-xxx, FR-xxx`.
- TDD: viết test cho AC trước. Backend: docstring test ghi ID AC (`"""AC-201.1 ..."""`). Frontend: ghi ID AC trong `describe`/`it`. E2E: ghi ID AC trong `test("AC-xxx …")`. `tools/trace_matrix.py` dựa vào quy ước này.
- **Đổi API** ⇒ sửa `app/api-contract/openapi.yaml` trước, cập nhật `elements.yaml`, chạy `npm run gen:api`. `check:api` và `cross_view_audit.py` sẽ fail nếu lệch.
- Backend: lỗi nghiệp vụ dùng `raise ProblemError(status, code)`; `code` thuộc enum trong hợp đồng; thông điệp tiếng Việt nằm ở `app/backend/cwd/errors.py`. Mọi truy vấn tài nguyên người dùng **phải** lọc `user_id` (NFR-004), nếu không tìm thấy hoặc không phải của mình thì trả 404. SQL luôn dùng tham số `?`. Chuẩn hóa tiếng Việt chỉ qua `cwd/textnorm.py`.
- Lỗi đồng thời/thứ tự (commit, race giữa request) không lộ qua `TestClient`; mọi thay đổi ở auth, upload, transaction phải chạy Playwright.
- Frontend: `<script setup lang="ts">`, TypeScript strict; type API lấy từ `src/api/types.ts` (alias của type sinh tự động), không tự định nghĩa lại. Trạng thái nằm trong composable `src/composables/`.
- Python: chỉ thêm thư viện có wheel thuần Python hoặc cho Python 3.15 (PyYAML không cài được → dùng `ruamel.yaml`). npm: pin chính xác phiên bản đã phát hành ≥ 14 ngày; `.npmrc` bật `legacy-peer-deps`.

## Điều cấm
- Không ghi nội dung câu hỏi, câu trả lời, văn bản tài liệu, mật khẩu, token vào log (NFR-008, BR-027).
- Không dùng `v-html` hay `innerHTML` với dữ liệu từ API (ESLint chặn `vue/no-v-html`).
- Không gọi dịch vụ AI bên ngoài trừ khi `CWD_ALLOW_EXTERNAL_AI=true` (ADR-003).
- Không để LLM tự viết tên tài liệu/số trang; trích dẫn lấy từ CSDL (ADR-005).
- Không commit secret, `.env`, `data/`, `node_modules/`, `dist/`.
- Agent không approve, merge hay deploy. Không sửa file đã baseline trong `docs/` mà không ghi lịch sử phiên bản.
