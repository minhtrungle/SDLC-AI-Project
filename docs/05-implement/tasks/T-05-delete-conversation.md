# T-05 — Xóa tài liệu; hội thoại nhiều lượt, phạm vi, xem lại

| Mục | Giá trị |
|---|---|
| Story / FR | US-205, US-401..403 · FR-008, FR-014..016 |
| Phụ thuộc | T-04 |
| Risk tier | Medium |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Implemented — AC đã tick PASS theo [RTM](../../07-verification/testing/RTM.md) (RUN-20261102-25eb89f); mục chưa tick không phải AC, cần review L2 xác nhận · cập nhật 2026-11-02 |

## Tiêu chí hoàn thành (AC đích)
- [x] AC-205.1..4
- [x] AC-401.1
- [x] AC-402.1..2
- [x] AC-403.1..2

## Test (viết trước)
- `app/backend/tests/test_documents.py`
- `app/backend/tests/test_conversation.py`

## File chạm
- `app/backend/cwd/documents.py`
- `app/backend/cwd/chat.py`
- `app/backend/cwd/retrieval.py`
- `app/frontend/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
