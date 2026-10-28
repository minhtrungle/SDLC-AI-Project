# T-07 — AnthropicGenerator sau cờ chính sách dữ liệu

| Mục | Giá trị |
|---|---|
| Story / FR | US-102 · FR-003, FR-011 |
| Phụ thuộc | T-04 |
| Risk tier | High — review L3 bắt buộc |
| Owner | Agent (sinh) · Dev owner (review, merge) |
| Trạng thái | Planned |

## Tiêu chí hoàn thành (AC đích)
- [ ] AC-102.1, AC-102.2 (chọn bộ sinh)
- [ ] Chunk bọc `<document>`, hệ thống nhắc không làm theo chỉ dẫn trong tài liệu
- [ ] Lỗi/timeout → 503 `chat.ai_unavailable`, không trả câu trả lời suy đoán
- [ ] Test bằng client giả, không gọi mạng

## Test (viết trước)
- `tests/test_generation.py`

## File chạm
- `app/generation.py`

## Definition of Done
Theo [PLAN.md §3](../PLAN.md#3-definition-of-done-mọi-task).
