# T-02 — Đăng nhập, phiên, CSRF, nhật ký kiểm toán

| Mục | Giá trị |
|---|---|
| Story / FR | US-101, US-103 · FR-001, FR-002, FR-019, NFR-010 |
| Phụ thuộc | T-01 |
| Risk tier | High — review L3 bắt buộc |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Implemented — AC đã tick PASS theo [RTM](../../07-verification/testing/RTM.md) (RUN-20261102-25eb89f); mục chưa tick không phải AC, cần review L2 xác nhận · cập nhật 2026-11-02 |

## Tiêu chí hoàn thành (AC đích)
- [x] AC-101.1..6
- [x] AC-103.1..3
- [x] AC-NFR-010 (băm PBKDF2, cookie HttpOnly+SameSite=Strict, CSRF)
- [ ] CLI `create-user`, `seed-demo`
- [ ] SCR-01, SCR-06 trên Web UI

## Test (viết trước)
- `app/backend/tests/test_auth.py`
- `app/backend/tests/test_cli.py`

## File chạm
- `app/backend/cwd/security.py`
- `app/backend/cwd/auth.py`
- `app/backend/cwd/audit.py`
- `app/backend/cwd/cli.py`
- `app/frontend/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
