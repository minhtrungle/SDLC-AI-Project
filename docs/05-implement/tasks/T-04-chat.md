# T-04 — Truy xuất, bộ sinh cục bộ, hỏi đáp có trích dẫn

| Mục | Giá trị |
|---|---|
| Story / FR | US-301..305 · FR-009..013 |
| Phụ thuộc | T-03 |
| Risk tier | Medium |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Implemented — AC đã tick PASS theo [RTM](../../07-verification/testing/RTM.md) (RUN-20261102-25eb89f); mục chưa tick không phải AC, cần review L2 xác nhận · cập nhật 2026-11-02 |

## Tiêu chí hoàn thành (AC đích)
- [x] AC-301.1..5
- [x] AC-302.1..2
- [x] AC-303.1..2
- [x] AC-304.1..2
- [x] AC-305.1..3
- [ ] Ngưỡng `rel ≥ CWD_MIN_RELEVANCE`; ≤ 2 chunk/tài liệu (ADR-004)
- [ ] Trích dẫn kiểm tra với CSDL (ADR-005)

## Test (viết trước)
- `app/backend/tests/test_retrieval.py`
- `app/backend/tests/test_generation.py`
- `app/backend/tests/test_chat.py`

## File chạm
- `app/backend/cwd/retrieval.py`
- `app/backend/cwd/generation.py`
- `app/backend/cwd/chat.py`
- `app/frontend/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
