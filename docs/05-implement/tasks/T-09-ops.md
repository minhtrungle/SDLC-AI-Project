# T-09 — Sao lưu, khôi phục, dọn nhật ký

| Mục | Giá trị |
|---|---|
| Story / FR | NFR-006, NFR-007 |
| Phụ thuộc | T-02 |
| Risk tier | Low |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Planned |

## Tiêu chí hoàn thành (AC đích)
- [ ] `cli backup <dir>` / `cli restore <dir>` khôi phục đủ dữ liệu
- [ ] `cli prune-audit --days N` chỉ xóa bản ghi cũ hơn N ngày (mặc định 90, không cho < 90)

## Test (viết trước)
- `app/backend/tests/test_cli.py`

## File chạm
- `app/backend/cwd/cli.py`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
