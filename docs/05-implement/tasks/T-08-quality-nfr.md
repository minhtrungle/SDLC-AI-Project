# T-08 — Bộ đánh giá chất lượng/độ trễ; test bảo mật xuyên suốt

| Mục | Giá trị |
|---|---|
| Story / FR | US-306 · NFR-001..004, NFR-008 |
| Phụ thuộc | T-05 |
| Risk tier | Medium |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Implemented — AC đã tick PASS theo [RTM](../../07-verification/testing/RTM.md) (RUN-20261102-25eb89f); mục chưa tick không phải AC, cần review L2 xác nhận · cập nhật 2026-11-02 |

## Tiêu chí hoàn thành (AC đích)
- [x] AC-306.1..2 (bộ câu hỏi tổng hợp, ngưỡng 85/90/9-trên-10, P90 ≤ 2 s)
- [x] AC-NFR-004 cô lập workspace trên mọi endpoint
- [x] AC-NFR-008 log sạch
- [x] AC-303.2 injection

## Test (viết trước)
- `app/backend/tests/eval/test_eval.py`
- `app/backend/tests/test_isolation.py`
- `app/backend/tests/test_logging.py`

## File chạm
- `app/backend/tests/eval/*`
- `tests/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
