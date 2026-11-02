# T-03 — Tải lên, kiểm tra, ingestion, danh sách

| Mục | Giá trị |
|---|---|
| Story / FR | US-201..204 · FR-004..007 |
| Phụ thuộc | T-02 |
| Risk tier | Medium |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Implemented — AC đã tick PASS theo [RTM](../../07-verification/testing/RTM.md) (RUN-20261102-25eb89f); mục chưa tick không phải AC, cần review L2 xác nhận · cập nhật 2026-11-02 |

## Tiêu chí hoàn thành (AC đích)
- [x] AC-201.1..3
- [x] AC-202.1..4
- [x] AC-203.1..5
- [x] AC-204.1..2
- [ ] `recover_pending()` khi khởi động (ADR-008)

## Test (viết trước)
- `app/backend/tests/test_documents.py`
- `app/backend/tests/test_ingestion.py`
- `app/backend/tests/test_textnorm.py`

## File chạm
- `app/backend/cwd/documents.py`
- `app/backend/cwd/ingestion.py`
- `app/backend/cwd/textnorm.py`
- `app/frontend/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
