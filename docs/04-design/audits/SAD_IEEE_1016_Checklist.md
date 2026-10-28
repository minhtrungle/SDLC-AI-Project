# Audit — SAD theo checklist IEEE 1016

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/SAD.md (v0.2), kèm adr/ADR-001..008, diagrams/*.drawio |
| Checklist | docs/design/SAD_IEEE_1016_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Scope & Boundary | Done | SAD §3.1 (C4 mức 1) tách rõ hệ thống với ACT-01..04; §3.2 liệt kê kênh trình duyệt, đĩa, Anthropic. |
| 3 | Context View | Done | §3.1 + §3.2 nêu dịch vụ cung cấp (hỏi đáp, số liệu, CLI) và dịch vụ cần từ môi trường (đĩa, Anthropic tùy chọn, reverse proxy TLS ở §7). |
| 4 | Architectural Drivers | Done | §1.2 Q1..Q5 có thước đo + nguồn FR/NFR; §10 QS-01..QS-07. Thiếu kịch bản cho NFR-005 (availability 99%) và NFR-009 (WCAG) — nên bổ sung vào §10. |
| 5 | System Constraints | Done | §2 TC-01..TC-04, OC-01 có nguồn. Lưu ý: TC-02 ghi Python 3.15 trong khi §7 và PRD §3.9.4 ghi Python ≥ 3.12 — cần nói rõ 3.15 là môi trường dev, 3.12 là mức tối thiểu. |
| 6 | Composition View | Done | §5.1 container, §5.2 CMP-01..CMP-13 có module, trách nhiệm, phụ thuộc, yêu cầu. |
| 7 | Logical View | In Progress | SAD không có mô hình miền; chỉ trỏ class_diagram.drawio. Không liên kết data/model.md hay blueprint.md (grep không có). Cần thêm §5.4 hoặc liên kết tới ERD/ENT-01..08. |
| 8 | Dependency View | In Progress | Cột Phụ thuộc §5.2 sai/lệch: CMP-02 phụ thuộc "CMP-03..CMP-13" gồm cả CMP-12 Admin CLI (vô lý); CMP-09 không phụ thuộc CMP-03 dù cần require_manager; CMP-06→CMP-13 có trong class diagram ("reads Settings") nhưng không có trong §5.2 và component diagram; CMP-05 phụ thuộc CMP-06 chỉ vì fold() trong khi blueprint §3.2 nói textnorm là lá. |
| 9 | Interaction View | Done | §6.1..6.4 + sequence_diagram.drawio (Hỏi đáp, Đăng nhập). Luồng xóa và khôi phục ingestion chỉ có văn xuôi. |
| 10 | State Dynamics View | In Progress | SAD không có view trạng thái; máy trạng thái tài liệu chỉ ở blueprint §3.7 và không được SAD tham chiếu. Mã lỗi `ingest.interrupted` (data/model.md §3) không xuất hiện trong bất kỳ chuyển trạng thái nào. |
| 11 | Information View | Done | §3.2, §8.1 (bảng dữ liệu, nơi lưu, có rời máy chủ không), ADR-002 (mô hình lưu trữ), §6.2 luồng ingestion. |
| 12 | Interface View | In Progress | SAD không liên kết openapi.yaml/openapi.md (grep 0 kết quả). §5.3 chỉ có 2 Protocol; chữ ký `Retriever.retrieve` ở §5.3 không có `conn` nhưng blueprint §3.3 và class diagram có `conn`. Hợp đồng với Anthropic (timeout, xử lý lỗi, định dạng prompt) chỉ mô tả ở ADR-003. |
| 13 | Resource View | Pending | Không có phân bổ CPU/RAM/đĩa: dung lượng dự kiến cwd.db + files/ (≤ 30×50×20 MB = 30 GB tối đa), RAM khi pypdf đọc PDF 300 trang, số luồng uvicorn cho ≤ 5 câu hỏi đồng thời. |
| 14 | Physical/Execution Mapping | Done | §7 + deployment_diagram.drawio. Lưu ý: backups/ nằm cùng đĩa với cwd.db (xem finding DR). |
| 15 | Architectural Decisions | Done | §9 + 8 ADR có Bối cảnh/Quyết định/Hệ quả/Khó đảo ngược. Tất cả ở trạng thái Proposed, chưa có người duyệt. |
| 16 | Rejected Alternatives | Done | Mỗi ADR có bảng "Phương án đã cân nhắc" kèm lý do (vd. ADR-002 PostgreSQL/Chroma/JSON). |
| 17 | Traceability | Done | ADR ghi FR/BR liên quan; §5.2 cột Yêu cầu; §1.2 nguồn. Thiếu: NFR-005, NFR-007, NFR-009 không gắn với quyết định kiến trúc nào trong §4. |

## Tóm tắt
SAD v0.2 có cấu trúc arc42 tốt, ADR đầy đủ phương án. Khoảng trống chính: thiếu resource view, thiếu state view/logical view trong chính SAD, không liên kết tới openapi/data model, và cột phụ thuộc §5.2 lệch với component diagram và class diagram.
