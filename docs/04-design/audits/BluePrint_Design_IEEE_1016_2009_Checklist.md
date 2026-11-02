# Audit — Design Blueprint theo checklist IEEE 1016-2009 SDD

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/blueprint.md (v0.2, đã REFINE: thêm §3.9, §6), elements.yaml, data/model.md, openapi.yaml, use_cases.md, diagrams/*.drawio |
| Checklist | docs/checklists/BluePrint_Design_IEEE_1016_2009_Checklist.xlsx |
| Reviewer | artifact-auditor (agent) — vòng 1: Independent reviewer agent |
| Ngày | 2026-11-02 (vòng 1: 2026-10-28) |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d), đối chiếu design-refine-log.md DF-01..DF-27 và code app/ hiện tại |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Design Subject Scope | Done | blueprint §1.1, §1.2 (Trong: CMP-01..13; Ngoài: SSO, OCR, Anthropic). |
| 3 | Context View | In Progress | Vẫn chỉ có một câu ở §1.2 và liên kết use_case_diagram ở §3.6; không có context view hay liên kết tới SAD §3.1/§3.2 (C4 mức 1, kênh kỹ thuật). Cần thêm một dòng trỏ SAD §3. |
| 4 | Stakeholder Identification | In Progress | §2 chỉ có Dev, QA, IT/Bảo mật, UX. Checklist yêu cầu nêu rõ cả operators/maintainers: thiếu người vận hành ACT-03 (chạy CLI backup/restore, SAD §7.2) và PO (SAD §1.3 có PO). Vòng 1 chấm Done kèm lưu ý này, vòng 2 chấm lại theo đúng tiêu chí. |
| 5 | Design Concerns | Done | §2 bảng concern→view, §2.1 trỏ SAD §10, §2.2 UQ-01..04, §2.3 ràng buộc UX. Minor: §2.1 ghi QS-01..QS-07 trong khi SAD §10 đã có QS-08/09. |
| 6 | Composition View | Done | §3.1 cây app/api-contract, app/backend/cwd/*, app/frontend/src ↔ CMP-xx, khớp elements.yaml (cross-view-audit PASS). |
| 7 | Logical View | In Progress | §3.3 bảng lớp đã có CurrentUser và Settings 11 trường, nhưng app/backend/cwd/config.py còn thêm max_question_chars, anthropic_api_key, frontend_dist. Ngoài ra class_diagram.drawio chưa cập nhật: Settings chỉ có 6 trường (thiếu per_doc_limit, session_idle_hours, anthropic_model, answer_timeout_s, cookie_secure), còn lớp ChatService trong khi chat.py dùng hàm, thiếu CurrentUser; FtsRetriever trong sơ đồ và §3.3 chưa có tham số cited_documents (SAD §5.3). DF-20 Partial. |
| 8 | Dependency View | In Progress | §3.2 nêu textnorm là lá, khớp SAD §5.2 sau DF-13; component diagram đã có cạnh CMP-04/08/09→CMP-03 (current_user, require_manager). Còn: component diagram vẫn có cạnh CMP-05→CMP-06 "textnorm.fold()"; quy tắc §3.2 chưa ghi documents/chat/metrics phụ thuộc auth. |
| 9 | Interaction View | Done | §3.6: sequence (Hỏi đáp, Đăng nhập, có khung alt lỗi — DF-07), activity (Tải lên); use_cases.md (DF-08) bổ sung luồng xóa tài liệu, đánh giá, số liệu tuần, quản trị. |
| 10 | Information View | Done | §3.4 → data/model.md + app/backend/cwd/schema.sql; phân loại dữ liệu nhạy cảm. |
| 11 | Interface View | Done | §3.5 → openapi.yaml/openapi.md + SAD §5.3. Hợp đồng lỗi đã bổ sung `internal`, bảng mã lỗi → HTTP (openapi.md §4.1, DF-06); phần lệch còn lại ghi ở audit API. |
| 12 | State Dynamics View | Done | §3.7 máy trạng thái tài liệu + bộ tên chuẩn duy nhất cho ô hỏi (DF-04), có `over_limit` (EC-08) và `error`/Gửi lại; UIUX_Blueprint banner dòng 4–5 tham chiếu §3.7, ánh xạ uploading/password, bỏ "Thử lại"/cancelled; slow/cancel quyết định ở §6 EC-06. Minor: nhãn processing→failed chưa ghi `ingest.interrupted`. |
| 13 | Algorithm View | Done | §3.9 (DF-09): 3.9.1 cắt chunk 800/100 theo trang, 3.9.2 truy xuất IDF + rel ≥ 0.6 + xếp hạng ngữ cảnh, 3.9.3 bộ sinh cục bộ + validate_citations, 3.9.4 công thức chỉ số tuần theo turns.created_at. |
| 14 | Element Attributes | Done | elements.yaml: id, name, module, responsibility cho CMP; endpoint có operationId, component, req. |
| 15 | Resource Allocation | In Progress | Blueprint không có mục tài nguyên và không liên kết SAD §7.1. SAD §7.1 (DF-10) có phân bổ ở mức hệ thống (CPU: 1 vCPU request, 1 ingestion; RAM theo tiến trình/PDF; threadpool) nhưng chưa gán cho từng phần tử CMP-xx. Thêm liên kết hoặc cột CMP trong SAD §7.1. |
| 16 | Decision Documentation | Done | ADR-001..009; §3.8 Patterns use view nêu lý do. |
| 17 | Alternatives Considered | Done | Mỗi ADR có bảng phương án bị loại kèm lý do. |
| 18 | Assumptions & Constraints | Done | §1.3 trỏ TC-01..04, ASM-001, PRD §3.9.4; §2.3 ràng buộc UX. |
| 19 | Requirements Traceability | In Progress | §4 vẫn chỉ 4 dòng concern. elements.yaml truy vết endpoint→FR; SAD §10 có QS cho NFR-005, NFR-009, nhưng §4 chưa có NFR-001, 002, 005, 006, 007, 009 và màn hình SCR-xx chưa gắn FR. |
| 20 | Completeness Check | In Progress | §6 (DF-12) có quyết định cho EC-06/09/12/15/17 và analytics; openapi.md §4.2 ghi US-404, US-601 hoãn. Còn mở: EC-06 nút Hủy và EC-17 hạn mức `usage.limit_reached` hoãn (owner Tech Lead, PO + IT); UIUX v0.1 chưa viết lại toàn văn (DF-03 Partial) nên còn nguồn mơ hồ; truy vết NFR chưa đủ (Row 19). |

## Kiểm tra lại vòng trước
| Row | Vấn đề vòng 1 | Kết quả vòng 2 |
|---|---|---|
| 3 | Không có context view | Chưa sửa |
| 7 | Lệch class diagram | §3.3 gần khớp code (thiếu 3 trường Settings); sơ đồ chưa cập nhật (DF-20 Partial) |
| 8 | textnorm, router→auth | Router→auth đã có trong sơ đồ; còn cạnh CMP-05→CMP-06 |
| 12 | Tên trạng thái lệch UIUX, thiếu over-limit, ingest.interrupted | Đã sửa (DF-04, DF-15, banner UIUX); còn thiếu nhãn ingest.interrupted (Minor) |
| 13 | Thiếu algorithm view | Đã sửa: §3.9 (DF-09) |
| 15 | Không có resource allocation | SAD §7.1 có mức hệ thống; blueprint chưa liên kết |
| 19 | Truy vết NFR | Chưa sửa ở §4 |
| 20 | Edge case chưa có quyết định | Đã quyết định (§6); còn mục hoãn |

## Phát hiện
| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-BP-01 | Major | diagrams/class_diagram.drawio | Logical view trong sơ đồ lệch §3.3 và code (Settings thiếu 5 trường, ChatService là lớp, thiếu CurrentUser, chữ ký retrieve thiếu cited_documents) | Cập nhật §3.3 theo config.py rồi sinh lại class diagram (tools/gen_diagrams.py) |
| AUD-BP-02 | Minor | diagrams/component_diagram.drawio; §3.2 | Cạnh CMP-05→CMP-06 "textnorm.fold()" còn tồn tại; quy tắc §3.2 thiếu phụ thuộc router→auth | Xóa cạnh; bổ sung `{documents, chat, metrics} → auth` vào §3.2 |
| AUD-BP-03 | Minor | §1.2 | Không có context view hoặc liên kết SAD §3 | Thêm liên kết SAD §3.1/§3.2 |
| AUD-BP-04 | Minor | §2 | Thiếu stakeholder PO và người vận hành (ACT-03) | Thêm hai dòng vào bảng §2 |
| AUD-BP-05 | Minor | §2.1 | Ghi QS-01..QS-07, SAD đã có QS-08/09 | Cập nhật phạm vi |
| AUD-BP-06 | Minor | §3.7 | Nhãn processing→failed thiếu `ingest.interrupted` | Bổ sung |
| AUD-BP-07 | Minor | Đầu file | Vẫn ghi Phiên bản 0.2 dù đã thêm §3.9, §6 sau REFINE; không có lịch sử phiên bản (trái quy ước AGENTS.md) | Nâng phiên bản và thêm bảng lịch sử |
| AUD-BP-08 | Minor | §4 | Ma trận truy vết thiếu NFR và SCR-xx | Mở rộng §4 |
| AUD-BP-09 | Minor | §3.9.1–3.9.4 | Đường dẫn cũ `app/ingestion`, `app/retrieval`, `app/metrics` | Đổi sang `app/backend/cwd/*` |

## Tóm tắt
- Status: Done 12 · In Progress 7 · Pending 0 · N/A 0 (tổng 19).
- Phát hiện: Critical 0 · Major 1 · Minor 8.
- Nhận định: Cần sửa — đóng AUD-BP-01 (class diagram) và các lỗ hổng tài liệu nhỏ ở Row 3, 4, 8, 15, 19; Row 20 sẽ còn In Progress chừng nào EC-06/EC-17 và DF-03 còn hoãn.

## Lịch sử audit
| Ngày | Vòng | Row | Status cũ → mới | Lý do |
|---|---|---|---|---|
| 2026-10-28 | 1 | — | — | Audit ban đầu trên blueprint v0.2: Done 11, In Progress 7, Pending 1 |
| 2026-11-02 | 2 | 4 | Done → In Progress | Chấm lại theo đúng tiêu chí: thiếu operators (ACT-03) và PO, vòng 1 đã ghi lưu ý nhưng vẫn chấm Done |
| 2026-11-02 | 2 | 12 | In Progress → Done | Bộ tên trạng thái chuẩn (DF-04), UIUX tham chiếu, over_limit, ingest.interrupted định nghĩa (DF-15) |
| 2026-11-02 | 2 | 13 | In Progress → Done | Thêm §3.9 Algorithm view (DF-09) |
| 2026-11-02 | 2 | 15 | Pending → In Progress | SAD §7.1 có phân bổ mức hệ thống (DF-10); chưa gán theo phần tử, blueprint chưa liên kết |
| 2026-11-02 | 2 | 7, 8, 19, 20 | In Progress → In Progress | Có cải thiện một phần (xem Notes), còn lỗ hổng |
| 2026-11-02 | 2 | 9, 11 | Done → Done | Cập nhật Notes: use_cases.md, bảng mã lỗi |
