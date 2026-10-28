# Sources — Chat với tài liệu

| ID | Nguồn | Loại | Chủ sở hữu | Ngày / phiên bản | Vị trí | Độ tin cậy |
|---|---|---|---|---|---|---|
| SRC-001 | Yêu cầu của quản lý dự án: MVP web app, upload PDF, chat với AI; cho phép BA đề xuất thêm tính năng | Sponsor brief | Quản lý dự án | 2026-10-27 / v1.0 | Prompt BRD §2.1; BRD v0.1 (commit `f30c7b7`) | Cao nhưng ngắn gọn |
| SRC-002 | Đề xuất tính năng bổ sung của BA (trích dẫn, hội thoại nhiều lượt, đánh giá, dashboard, tóm tắt) | Phân tích BA | Đội BA | 2026-10-27 | BRD v0.1 §7 | Chưa được sponsor duyệt (OQ-013) |
| SRC-003 | ISO/IEC/IEEE 29148-2018 | Tiêu chuẩn | IEEE | 2018 | — | Cao |
| SRC-004 | BRD v0.1, PRD v0.1, SAD v0.1, UI/UX blueprint, 6 sơ đồ draw.io | Artifact trước đó | Đội BA / minhtrungle | 2026-10-27 | Git history: commits `bc4d9e1`..`ca575f3` | Bản nháp, đã được tái sử dụng làm đầu vào |
| SRC-005 | Khảo sát môi trường kỹ thuật: Python 3.15.2, Node 14.19.3 (sau nâng lên 22.23.4 LTS cho frontend Vue — ADR-009), không có Docker, không có API key LLM | Quan sát | Agent | 2026-10-28 | Phiên làm việc | Cao |
| SRC-006 | Prompt và checklist chuẩn | Bộ công cụ quy trình | Repo SDLC-Prompt-Checklist | — | `docs/prompts/`, `docs/checklists/` | Cao |

## Nguồn còn thiếu (cần con người cung cấp)
- Phỏng vấn người dùng cuối (OQ-002) — chưa thực hiện; cần con người phỏng vấn theo `BRD_Elicitation_Prompt_IEEE_standard.md`.
- Số liệu baseline thời gian tìm kiếm (OQ-003).
- Bộ tài liệu mẫu và bộ câu hỏi chuẩn có đáp án (DEP-002).
- Chính sách phân loại dữ liệu của tổ chức (OQ-006).
