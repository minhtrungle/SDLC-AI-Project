# Bộ câu hỏi elicitation (AI-as-client)

Sinh theo [BRD_Elicitation_Prompt_IEEE_standard.md](../../prompts/BRD_Elicitation_Prompt_IEEE_standard.md). Thứ tự ưu tiên: câu chặn baseline trước. Mỗi câu ghi OQ/BR mà câu trả lời sẽ đóng.

## Buổi 1 — Quản lý dự án (STK-001), 45 phút

| # | Topic | Câu hỏi | Đóng | Câu hỏi đào sâu nếu trả lời mơ hồ |
|---|---|---|---|---|
| 1 | Governance | Ai ký duyệt BRD, PRD và quyết định go-live? | OQ-001 | "Nếu anh/chị vắng, ai ký thay?" |
| 2 | Drivers | Vì sao làm MVP này bây giờ? Có hạn chót nào gắn với sự kiện kinh doanh không? | OQ-009 | "Nếu trễ 1 tháng thì mất gì?" |
| 3 | Objectives | Đạt kết quả nào sau 4 tuần thì anh/chị coi MVP thành công? | OQ-005 | "Con số tối thiểu là bao nhiêu? 70%? 85%?" |
| 4 | Constraints | Ngân sách MVP, gồm chi phí dịch vụ AI hàng tháng, là bao nhiêu? | OQ-008 | "Trần chi phí mỗi tháng?" |
| 5 | Scope | Tài liệu nên riêng từng người hay dùng chung cả đội? | OQ-007 | "Có tài liệu nào chỉ một số người được xem không?" |
| 6 | Scope | Đồng ý giữ BR-016, BR-021, BR-022 trong MVP và hoãn BR-018, BR-023? | OQ-013 | — |

## Buổi 2 — Đội phát triển kinh doanh (STK-002), 2–3 người, 60 phút

| # | Topic | Câu hỏi | Đóng |
|---|---|---|---|
| 1 | Problem | Kể lần gần nhất anh/chị phải tìm một thông tin trong tài liệu dự án: tìm gì, mở bao nhiêu file, mất bao lâu? | OQ-002, OQ-003 |
| 2 | Problem | Năm loại câu hỏi anh/chị hỏi tài liệu nhiều nhất là gì? | OQ-002, DEP-002 |
| 3 | Context | Có khoảng bao nhiêu file PDF, mỗi file bao nhiêu trang, bao nhiêu file là bản scan? | OQ-004, ASM-001 |
| 4 | Language | Tài liệu viết bằng tiếng gì? Anh/chị có cần hỏi tiếng Việt trên tài liệu tiếng Anh không? | OQ-010 |
| 5 | NFR | Chờ một câu trả lời tối đa bao lâu thì vẫn chấp nhận? | OQ-012 |
| 6 | Limits | File lớn nhất anh/chị từng có là bao nhiêu MB? | OQ-011 |
| 7 | Acceptance | Anh/chị có thể soạn 30 câu hỏi kèm đáp án và vị trí trang để nghiệm thu không? | DEP-002 |

## Buổi 3 — IT / Bảo mật (STK-005), 30 phút

| # | Câu hỏi | Đóng |
|---|---|---|
| 1 | Tài liệu dự án thuộc mức phân loại nào? | OQ-006 |
| 2 | Có được gửi nội dung tài liệu tới dịch vụ AI bên ngoài không? Nếu có, nhà cung cấp nào được phê duyệt, cần điều khoản gì? | OQ-006, DEP-001 |
| 3 | Yêu cầu xác thực: tài khoản riêng hay SSO nội bộ? | BR-019 |
| 4 | Thời gian lưu nhật ký kiểm toán tối thiểu? | BR-026 |
| 5 | Môi trường triển khai nội bộ có sẵn không? | DEP-003 |
