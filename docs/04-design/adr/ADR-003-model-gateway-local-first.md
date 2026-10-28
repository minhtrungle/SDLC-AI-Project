# ADR-003 — ModelGateway, mặc định sinh câu trả lời cục bộ

- **Trạng thái:** Proposed — **cần IT/Bảo mật xác nhận** (OQ-006) · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Liên quan:** BR-020, FR-003, US-102; AD-04 của SAD v0.1

## Bối cảnh
- Chưa biết tổ chức có cho phép gửi nội dung tài liệu ra dịch vụ AI bên ngoài không (OQ-006). Gửi sai là sự cố rò rỉ dữ liệu (RSK-002), không thể thu hồi.
- Không có API key nào trong môi trường hiện tại; CI phải chạy không cần mạng.

## Quyết định
1. Mọi lời gọi sinh câu trả lời đi qua interface `AnswerGenerator` trong `app/generation.py`.
2. Hai cài đặt:
   - `LocalExtractiveGenerator` (**mặc định**): chọn các câu liên quan nhất trong chunk đã truy xuất và ghép thành câu trả lời có đánh số trích dẫn. Không gửi dữ liệu ra ngoài, tất định, không thể bị prompt injection điều khiển vì không diễn giải chỉ thị.
   - `AnthropicGenerator`: gọi Anthropic Messages API (mô hình mặc định `claude-opus-5-5`, effort `low`, bật `fallbacks: "default"` cho trường hợp bị từ chối; đổi bằng `CWD_ANTHROPIC_MODEL`), chunk được bọc trong thẻ `<document>` và đánh dấu là dữ liệu; mô hình không có công cụ.
3. `AnthropicGenerator` **chỉ** được chọn khi đồng thời `CWD_ALLOW_EXTERNAL_AI=true` **và** có `ANTHROPIC_API_KEY`. Mọi trường hợp khác dùng chế độ cục bộ. Chế độ đang dùng được công bố tại `GET /api/config` (`ai_mode`).
4. Nếu dịch vụ ngoài lỗi hoặc quá `CWD_ANSWER_TIMEOUT_S`, hệ thống trả lỗi `chat.ai_unavailable`, không tự rơi về câu trả lời suy đoán.

## Phương án đã cân nhắc
| Phương án | Lý do không chọn |
|---|---|
| Gọi LLM ngoài mặc định | Vi phạm nguyên tắc an toàn khi OQ-006 chưa có |
| Mô hình tự lưu trữ (Ollama, vLLM) | Không có GPU/hạ tầng; có thể thêm sau như một cài đặt `AnswerGenerator` mới |

## Hệ quả
- (+) Mặc định an toàn; IT/Bảo mật kiểm chứng được bằng cấu hình (AC-102.1, AC-102.2).
- (−) Chế độ cục bộ trả lời dạng trích đoạn, kém tự nhiên hơn LLM; không diễn giải hay suy luận. NFR-002 phải được đo lại khi bật LLM.
- **Khó đảo ngược:** Thấp — đổi cấu hình.
