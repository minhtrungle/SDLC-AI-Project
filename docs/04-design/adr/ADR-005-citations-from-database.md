# ADR-005 — Trích dẫn lấy từ CSDL và được kiểm tra trước khi trả về

- **Trạng thái:** Proposed · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Liên quan:** FR-013, US-305, RSK-001; giữ nguyên AD-11 của SAD v0.1

## Bối cảnh
Mô hình sinh có thể bịa tên tài liệu hoặc số trang. Trích dẫn sai còn tệ hơn không có trích dẫn vì người dùng tin nó.

## Quyết định
- Bộ sinh chỉ được tham chiếu nguồn bằng chỉ số `[n]` ứng với chunk thứ *n* trong ngữ cảnh đã truy xuất.
- Sau khi sinh, `app/backend/cwd/chat.py` lọc: chỉ giữ `[n]` hợp lệ; tên tài liệu, số trang, đoạn trích lấy từ bảng `chunks`/`documents`.
- Câu trả lời `answered` không còn trích dẫn hợp lệ nào ⇒ hạ thành `not_found`.
- `chunks.id` là `AUTOINCREMENT` để `chunk_id` trong trích dẫn đã lưu không bao giờ trỏ sang đoạn của tài liệu khác sau khi xóa (finding DF-01, test `test_chunk_ids_not_reused_after_delete`); `getChunk` luôn lọc theo chủ sở hữu.
- Trích dẫn được lưu kèm lượt hỏi đáp (JSON). Khi đọc lại hội thoại, trích dẫn của tài liệu đã xóa được đánh dấu `document_deleted = true` (AC-205.4).

## Hệ quả
- (+) AC-305.3 được đảm bảo bằng cấu trúc, không dựa vào hành vi mô hình.
- (−) Đoạn trích lưu trong lượt hỏi đáp vẫn còn sau khi xóa tài liệu → đã chấp nhận: đoạn trích ≤ 300 ký tự và nằm trong workspace của chính người dùng; ghi vào SAD §11 (rủi ro R-05).
- **Khó đảo ngược:** Thấp.
