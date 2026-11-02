# T-06 — Đánh giá câu trả lời, dashboard tuần

| Mục | Giá trị |
|---|---|
| Story / FR | US-501, US-502 · FR-017, FR-018 |
| Phụ thuộc | T-04 |
| Risk tier | Low |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Implemented — AC đã tick PASS theo [RTM](../../07-verification/testing/RTM.md) (RUN-20261102-25eb89f); mục chưa tick không phải AC, cần review L2 xác nhận · cập nhật 2026-11-02 |

## Tiêu chí hoàn thành (AC đích)
- [x] AC-501.1..2
- [x] AC-502.1..2
- [ ] SCR-05

## Test (viết trước)
- `app/backend/tests/test_metrics.py`

## File chạm
- `app/backend/cwd/metrics.py`
- `app/frontend/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
