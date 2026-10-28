# Glossary — Chat với tài liệu

| Thuật ngữ | Định nghĩa | Dùng trong |
|---|---|---|
| MVP | Sản phẩm khả dụng tối thiểu để kiểm chứng giá trị | Toàn bộ |
| Tài liệu | Một file PDF người dùng đã tải lên workspace của mình | BRD §7.1 |
| Workspace | Không gian riêng của một người dùng, chứa tài liệu và hội thoại của người đó (quyết định mặc định cho OQ-007) | BRD, SAD |
| Trạng thái tài liệu | `processing` (Đang xử lý), `ready` (Sẵn sàng), `failed` (Lỗi), `no_text` (Không trích xuất được văn bản) | US-203 |
| Chunk | Đoạn văn bản trích từ một trang PDF, là đơn vị tìm kiếm và trích dẫn | SAD, data model |
| Truy xuất (retrieval) | Bước tìm các chunk liên quan tới câu hỏi | SAD §6 |
| RAG | Retrieval-Augmented Generation: truy xuất chunk rồi sinh câu trả lời chỉ từ các chunk đó | ADR-004 |
| Grounding | Câu trả lời chỉ dựa trên nội dung tài liệu (BR-009) | US-303 |
| Trích dẫn (citation) | Tên tài liệu + số trang + đoạn trích gốc. Luôn lấy từ CSDL, không do mô hình tự viết | US-305, ADR-005 |
| `not_found` | Kết quả hỏi đáp khi tài liệu không chứa thông tin; không kèm trích dẫn | US-304 |
| ModelGateway | Lớp trừu tượng che giấu nhà cung cấp mô hình AI | ADR-003 |
| Extractive provider | Bộ sinh câu trả lời chạy cục bộ, ghép các câu liên quan nhất từ chunk; không gửi dữ liệu ra ngoài | ADR-003 |
| Phạm vi (scope) | Tập tài liệu được chọn để hỏi; mặc định là tất cả tài liệu sẵn sàng | US-402 |
| Phiên hội thoại | Chuỗi câu hỏi/câu trả lời từ lúc bấm "Cuộc hội thoại mới" | US-401, US-403 |
| Bộ câu hỏi chuẩn | Bộ câu hỏi có đáp án và vị trí nguồn, do đội kinh doanh soạn, dùng để nghiệm thu (DEP-002) | US-306 |
| Người dùng hoạt động | Người dùng đặt ít nhất 1 câu hỏi trong tuần | US-502 |
| Prompt injection | Văn bản trong tài liệu cố ra lệnh cho mô hình AI | US-303, AC-303.2 |
| phải / nên / có thể | *shall* / *should* / *may* theo IEEE 29148 | BRD, PRD |
| P0 / P1 / P2 | Must / Should / Could | PRD |
| L0–L4 | Các tầng đảm bảo chất lượng: CI, agent review, human review, inspection, demo | Phase 7–8 |
