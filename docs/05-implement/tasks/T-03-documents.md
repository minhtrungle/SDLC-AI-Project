# T-03 — Tải lên, kiểm tra, ingestion, danh sách

| Mục | Giá trị |
|---|---|
| Story / FR | US-201..204 · FR-004..007 |
| Phụ thuộc | T-02 |
| Risk tier | Medium |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Planned |

## Tiêu chí hoàn thành (AC đích)
- [ ] AC-201.1..3
- [ ] AC-202.1..4
- [ ] AC-203.1..5
- [ ] AC-204.1..2
- [ ] `recover_pending()` khi khởi động (ADR-008)

## Test (viết trước)
- `tests/test_documents.py`
- `tests/test_ingestion.py`
- `tests/test_textnorm.py`

## File chạm
- `app/documents.py`
- `app/ingestion.py`
- `app/textnorm.py`
- `app/web/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
