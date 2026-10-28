# AGENTS.md — hướng dẫn cho agent AI và dev

Đọc file này trước khi sửa code. `docs/` là nguồn sự thật; code phải khớp thiết kế.

## Sản phẩm
"Chat với tài liệu" — MVP web hỏi đáp trên PDF, câu trả lời chỉ dựa trên tài liệu, kèm trích dẫn tên tài liệu + trang.
Yêu cầu: [docs/03-analysis/PRD.md](docs/03-analysis/PRD.md) §3.9 · Story: [USER_STORIES.md](docs/03-analysis/USER_STORIES.md) · Kiến trúc: [SAD.md](docs/04-design/SAD.md) · Kế hoạch: [PLAN.md](docs/05-implement/PLAN.md).

## Stack (ADR-001..008)
- Python ≥ 3.12 (môi trường dev: 3.15), FastAPI, Uvicorn, pypdf, SQLite + FTS5 (thư viện chuẩn `sqlite3`).
- Web UI: HTML/CSS/JS thuần trong `app/web/`, **không** có bước build, không framework (Node 14 trên máy dev).
- Test: pytest, `fastapi.testclient`, fpdf2 để sinh PDF test.
- Chỉ thêm thư viện có wheel thuần Python hoặc wheel cho Python 3.15 (PyYAML không cài được → dùng `ruamel.yaml`).

## Lệnh
```bash
python -m venv .venv && .venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m pytest                   # test + coverage (≥ 70%)
.venv/Scripts/python -m ruff check . && .venv/Scripts/python -m ruff format --check .
.venv/Scripts/python tools/ci_local.py          # toàn bộ cổng L0 như CI
.venv/Scripts/python -m app.cli seed-demo       # tạo user demo
.venv/Scripts/python -m uvicorn app.main:app    # chạy tại http://127.0.0.1:8000
```

## Cấu trúc
Mỗi module tương ứng một thành phần `CMP-xx` trong [elements.yaml](docs/04-design/elements.yaml). Thêm/xóa endpoint ⇒ cập nhật `elements.yaml` + `openapi.yaml`; `tools/cross_view_audit.py` sẽ fail nếu lệch.

## Quy ước
- Conventional Commits; dòng cuối thân commit: `Refs: US-xxx, FR-xxx`.
- TDD: viết test cho AC trước; docstring test ghi ID AC (`"""AC-201.1 ..."""`).
- Lỗi nghiệp vụ: `raise ProblemError(status, code)`; `code` thuộc enum trong `openapi.yaml`; thông điệp tiếng Việt nằm trong `app/errors.py`.
- Mọi truy vấn tài nguyên người dùng **phải** lọc `user_id` (NFR-004). Không tìm thấy hoặc không phải của mình ⇒ 404.
- SQL luôn dùng tham số `?`, không ghép chuỗi giá trị người dùng.
- Chuẩn hóa tiếng Việt chỉ qua `app/textnorm.py`.

## Điều cấm
- Không ghi nội dung câu hỏi, câu trả lời, văn bản tài liệu, mật khẩu, token vào log (NFR-008, BR-027).
- Không gọi dịch vụ AI bên ngoài trừ khi `CWD_ALLOW_EXTERNAL_AI=true` (ADR-003).
- Không để LLM tự viết tên tài liệu/số trang; trích dẫn lấy từ CSDL (ADR-005).
- Không commit secret, file `.env`, thư mục `data/`.
- Agent không approve, merge hay deploy. Không sửa file đã baseline trong `docs/` mà không ghi lịch sử phiên bản.
