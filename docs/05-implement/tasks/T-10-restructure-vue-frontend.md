# T-10 — Tái cấu trúc thư mục và frontend Vue 3 + TypeScript

| Mục | Giá trị |
|---|---|
| Story / FR | Mọi story có giao diện (US-101..US-502) · ADR-009 |
| Phụ thuộc | T-01..T-09 |
| Risk tier | Medium |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Done (chờ review) |

## Tiêu chí hoàn thành
- [x] `app/backend` (package `cwd`), `app/frontend`, `app/api-contract/openapi.yaml`; backend test giữ nguyên kết quả
- [x] Frontend Vue 3 + TypeScript strict hiện thực SCR-01..06, cùng hành vi UI cũ (US-101..502, EC-01/02/04/15)
- [x] `src/api/schema.d.ts` sinh từ hợp đồng; `npm run check:api` chặn lệch
- [x] Test Vitest cho AC giao diện (AC-201.2, AC-204.2, AC-301.3..5, AC-305.1..2, AC-402.1, AC-403.2, AC-501.1, AC-502.2), coverage ≥ 70%
- [x] Backend phục vụ `app/frontend/dist`; E2E Chrome: đăng nhập → tải song song 2 PDF → hỏi → trích dẫn → Esc
- [x] Cổng L0 gồm cả bước frontend; CI cài Node 22

## Test
- `app/frontend/src/**/*.spec.ts`
- `app/backend/tests/test_app_basics.py::test_serves_built_frontend`, `::test_connection_usable_across_threads`

## Phát hiện trong quá trình làm
- E2E với frontend mới (upload song song + polling) làm lộ lỗi `sqlite3.ProgrammingError` do FastAPI dùng connection ở thread khác thread tạo ra nó → đã sửa (`check_same_thread=False`) và thêm test hồi quy.

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
