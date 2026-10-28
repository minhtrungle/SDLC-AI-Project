# Audit — Design Blueprint theo checklist IEEE 1016-2009 SDD

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/blueprint.md (v0.2), elements.yaml, data/model.md, openapi.yaml, diagrams/*.drawio |
| Checklist | docs/design/BluePrint_Design_IEEE_1016_2009_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Design Subject Scope | Done | blueprint §1.1, §1.2 (Trong: CMP-01..13; Ngoài: SSO, OCR, Anthropic). |
| 3 | Context View | In Progress | Blueprint không có context view riêng, chỉ một câu ở §1.2; không trỏ tới SAD §3 hay use_case_diagram cho bối cảnh. Thêm liên kết hoặc sơ đồ bối cảnh. |
| 4 | Stakeholder Identification | Done | §2: Dev, QA, IT/Bảo mật, UX. Thiếu PO và người vận hành (ACT-03 chạy CLI) — nên bổ sung. |
| 5 | Design Concerns | Done | §2 bảng concern→view, §2.1 trỏ SAD §10, §2.2 UQ-01..04, §2.3 ràng buộc UX. |
| 6 | Composition View | Done | §3.1 cây module ↔ CMP-xx, khớp elements.yaml (cross-view-audit PASS). |
| 7 | Logical View | In Progress | §3.3 lệch class_diagram trang "Service classes": Settings trong sơ đồ thiếu per_doc_limit, session_idle_hours, anthropic_model, answer_timeout_s, cookie_secure; sơ đồ có ChatService (lớp) trong khi §3.1 nói chat.py có hàm ask(); CurrentUser và Protocol Retriever không có trong sơ đồ. |
| 8 | Dependency View | In Progress | §3.2 nói textnorm là lá, nhưng textnorm được gán CMP-06 và component diagram vẽ CMP-05 → CMP-06 "fold()" — tạo phụ thuộc ingestion→retrieval. Router documents/chat/metrics phụ thuộc auth (current_user, require_csrf) nhưng §3.2 và component diagram không thể hiện. |
| 9 | Interaction View | Done | §3.6: sequence (Hỏi đáp, Đăng nhập), activity (Tải lên). Chưa có tương tác cho xóa tài liệu, khôi phục recover_pending, đánh giá, số liệu tuần. |
| 10 | Information View | Done | §3.4 → data/model.md + app/schema.sql; phân loại dữ liệu nhạy cảm. |
| 11 | Interface View | Done | §3.5 → openapi.yaml/openapi.md + SAD §5.3. Lỗ hổng hợp đồng lỗi xem API audit (thiếu mã `internal`, upload trả lỗi khác cấu trúc). |
| 12 | State Dynamics View | In Progress | §3.7 có máy trạng thái tài liệu và ô hỏi, nhưng: (a) tên trạng thái ô hỏi (disabled_empty, sending...) khác UIUX_Blueprint §3.7.3 (idle-empty, over-limit, busy...); (b) UIUX có trạng thái Password, Uploading, Error→Processing "Thử lại" không có trong API; (c) `ingest.interrupted` không có chuyển trạng thái; (d) thiếu trạng thái over-limit và slow/cancel (EC-06, EC-08). |
| 13 | Algorithm View | In Progress | Không có mục Algorithm view. Điểm rel/IDF chỉ ở ADR-004; thuật toán chunking (~800 ký tự, chồng lấn 100) chỉ một câu ở SAD §6.2; LocalExtractiveGenerator chỉ "chọn câu theo điểm từ"; validate_citations, công thức số liệu tuần (active_users, not_found_rate, positive_feedback_rate, theo ngày tạo lượt hay ngày đánh giá) chưa đặc tả. |
| 14 | Element Attributes | Done | elements.yaml: id, name, module, responsibility cho CMP; endpoint có operationId, component, req. |
| 15 | Resource Allocation | Pending | Không có phân bổ tài nguyên (CPU, RAM, đĩa, luồng) cho phần tử nào. |
| 16 | Decision Documentation | Done | ADR-001..008; §3.8 Patterns use view nêu lý do. |
| 17 | Alternatives Considered | Done | Mỗi ADR có bảng phương án bị loại kèm lý do. |
| 18 | Assumptions & Constraints | Done | §1.3 trỏ TC-01..04, ASM-001, PRD §3.9.4. |
| 19 | Requirements Traceability | In Progress | §4 chỉ có 4 dòng concern. elements.yaml truy vết endpoint→FR, nhưng NFR-001, 002, 005, 006, 007, 009 không có phần tử thiết kế cụ thể trong blueprint; màn hình SCR-xx không gắn FR. |
| 20 | Completeness Check | In Progress | Chưa có thiết kế cho: EC-06 (thông báo chậm + Hủy), EC-12 (trùng tên file), EC-17 (giới hạn sử dụng, `limit.reached` không có mã lỗi API), EC-09 (câu hỏi không phải tiếng Việt), sự kiện analytics PRD §5.2 (UIUX có AnalyticsClient nhưng không có endpoint/kho), "Thử lại" tài liệu lỗi; không nêu rõ US-404, US-601 bị hoãn. |

## Tóm tắt
Blueprint gọn, có composition/dependency/state/pattern views. Điểm yếu: thiếu algorithm view và resource allocation, state dynamics và logical view không nhất quán với UIUX blueprint và class diagram, độ phủ edge case PRD §4.2 chưa đủ.
