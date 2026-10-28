# T-04 — Truy xuất, bộ sinh cục bộ, hỏi đáp có trích dẫn

| Mục | Giá trị |
|---|---|
| Story / FR | US-301..305 · FR-009..013 |
| Phụ thuộc | T-03 |
| Risk tier | Medium |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Planned |

## Tiêu chí hoàn thành (AC đích)
- [ ] AC-301.1..5
- [ ] AC-302.1..2
- [ ] AC-303.1..2
- [ ] AC-304.1..2
- [ ] AC-305.1..3
- [ ] Ngưỡng `rel ≥ CWD_MIN_RELEVANCE`; ≤ 2 chunk/tài liệu (ADR-004)
- [ ] Trích dẫn kiểm tra với CSDL (ADR-005)

## Test (viết trước)
- `tests/test_retrieval.py`
- `tests/test_generation.py`
- `tests/test_chat.py`

## File chạm
- `app/retrieval.py`
- `app/generation.py`
- `app/chat.py`
- `app/web/*`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
