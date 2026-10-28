# ADR-008 — Xử lý tài liệu nền trong tiến trình, khôi phục khi khởi động

- **Trạng thái:** Proposed · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Thay thế:** worker + Redis queue của SAD v0.1
- **Liên quan:** FR-006, US-203

## Bối cảnh
Trích xuất một PDF 300 trang mất vài giây; không được chặn request tải lên. Không có Redis.

## Quyết định
- Sau khi lưu file và tạo bản ghi `processing`, endpoint tải lên đăng ký tác vụ nền (`BackgroundTasks` của FastAPI) cho từng tài liệu.
- Tác vụ: trích văn bản từng trang (pypdf) → cắt chunk → ghi `chunks` + FTS trong **một transaction** → đặt `ready` / `no_text` / `failed`.
- Khi khởi động, mọi tài liệu còn `processing` (do tiến trình chết giữa chừng) được xử lý lại.
- Nếu tài liệu bị xóa trong lúc xử lý, tác vụ phát hiện bản ghi không còn và bỏ kết quả.

## Hệ quả
- (+) Không cần hạ tầng hàng đợi; test tất định (TestClient chạy tác vụ nền trước khi trả kết quả).
- (−) Không chạy được nhiều instance; chuyển sang hàng đợi thật cùng lúc với ADR-002 trigger.
- **Khó đảo ngược:** Thấp.
