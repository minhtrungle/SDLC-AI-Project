# Design REFINE log — xử lý finding của reviewer độc lập

> Đầu vào: [design_checklist_audit.md](design_checklist_audit.md) (27 finding: 1 Blocker, 11 Major, 15 Minor; reviewer agent độc lập, 2026-10-28).
> Đây là bản ghi change control cho thay đổi thiết kế sau audit. Người duyệt: Architect + Tech Lead.
> Trạng thái: **Fixed** = đã sửa và kiểm chứng · **Partial** = đã sửa phần chặn, phần còn lại ghi rõ · **Deferred** = hoãn có owner và lý do.

| ID | Mức | Trạng thái | Xử lý | Bằng chứng |
|---|---|---|---|---|
| DF-01 | Blocker | Fixed | `chunks.id` → `AUTOINCREMENT`; quy tắc ghi vào model.md, ADR-005 | `app/schema.sql`; test `test_chunk_ids_not_reused_after_delete` |
| DF-02 | Major | Fixed | Kiểm tra giới hạn trong vòng lặp từng file, đếm cả file đã nhận trong lô (code đã đúng từ T-03); sửa activity diagram | `app/documents.py`; test `test_document_limit`; `activity_diagram.drawio` |
| DF-03 | Major | Partial | Gỡ Google Fonts và nút SSO khỏi prototype; banner "đọc trước" trong UIUX_Blueprint chỉ rõ các mục v0.1 bị thay thế. **Còn lại:** viết lại toàn văn UIUX lên v0.2 — owner UX, trước khi baseline | `UI_UX_design/html_design/*`, `UIUX_Blueprint_Design.md` |
| DF-04 | Major | Fixed | Một bộ tên trạng thái ô hỏi chuẩn ở blueprint §3.7, UIUX tham chiếu | blueprint §3.7 |
| DF-05 | Major | Fixed | ID component UI đổi `CMP-xx` → `UIC-xx` | `UIUX_Blueprint_Design.md` (0 lần `CMP-`) |
| DF-06 | Major | Fixed | Thêm `internal` vào enum; sửa ví dụ upload; bảng mã lỗi → HTTP → thông điệp; enum `Document.error_code` | openapi.yaml, openapi.md §4.1 |
| DF-07 | Major | Fixed | Sequence: khung alt lỗi trả về Web UI (401/403/404/409/422), nhánh 503 khi bộ sinh lỗi; trang Đăng nhập có alt khóa / sai / đúng với fail/reset | `sequence_diagram.drawio` |
| DF-08 | Major | Fixed | Thêm đặc tả use case UC-01..06, 09..13 | [use_cases.md](use_cases.md) |
| DF-09 | Major | Fixed | Blueprint §3.9 Algorithm view: chunking, truy xuất, bộ sinh cục bộ, kiểm tra trích dẫn, công thức chỉ số tuần | blueprint §3.9; `app/metrics.py` docstring |
| DF-10 | Major | Fixed | SAD §7.1 Resource view + cấu hình tối thiểu | SAD §7.1 |
| DF-11 | Major | Fixed | Sao lưu hằng ngày ra ngoài máy chủ, giữ 30 bản, thứ tự CSDL trước file; node sao lưu trong deployment diagram; diễn tập quý | SAD §7.2, runbook, `deployment_diagram.drawio` |
| DF-12 | Major | Fixed | Quyết định cho EC-06/09/12/15/17 và analytics (thiết kế hoặc hoãn + owner) | blueprint §6 |
| DF-13 | Minor | Fixed | SAD §5.2 và component diagram đồng bộ phụ thuộc (CMP-03, CMP-13); textnorm là module tiện ích | SAD §5.2, `component_diagram.drawio` |
| DF-14 | Minor | Fixed | Chữ ký `Retriever` thống nhất SAD = code (thêm `conn`, `cited_documents`) | SAD §5.3, `app/retrieval.py` |
| DF-15 | Minor | Fixed | `ingest.interrupted` được định nghĩa (file gốc mất khi xử lý) | model.md, `app/ingestion.py`, test `test_missing_file_marks_failed` |
| DF-16 | Minor | Partial | openapi: `maxItems: 50`, pattern id; code kiểm tra 2000 ký tự và 50 id. **Hoãn:** idempotency key cho câu hỏi — owner Tech Lead | openapi.yaml, openapi.md §4.2 |
| DF-17 | Minor | Deferred | Header `X-Request-ID` — thêm cùng giám sát tập trung sau go-live | owner Tech Lead |
| DF-18 | Minor | Deferred → L3 | Khóa đăng nhập theo username (có thể bị lợi dụng để khóa người khác); thiếu thời hạn phiên tuyệt đối. Đưa vào inspection L3 (review-record) | owner IT/Bảo mật |
| DF-19 | Minor | Deferred | Ràng buộc/chỉ mục/migration bổ sung | model.md §7 |
| DF-20 | Minor | Partial | Guard đặt trong `[ ]` ở activity diagram. **Còn lại:** activation, lollipop, ngăn operations — cải tiến ký hiệu, không đổi nội dung; owner Architect | `tools/gen_diagrams.py` |
| DF-21 | Minor | Fixed | Bỏ nhãn CMP-11 khỏi thư mục dữ liệu; trách nhiệm lưu file = CMP-04 (SAD §5.2); sửa nhãn kết nối proxy | `deployment_diagram.drawio` |
| DF-22 | Minor | Fixed | Chốt 1280 px | UIUX banner |
| DF-23 | Minor | Fixed | Nguồn thông điệp duy nhất `app/errors.py`; FR-012 và AC-202.1 khớp code (đã có test) | openapi.md §4.1; `test_general_knowledge_question_not_found`, `test_one_bad_file_does_not_block_others` |
| DF-24 | Minor | Fixed | Liên kết view trong SAD; QS-08, QS-09; ghi rõ 3.15 = dev, ≥ 3.12 = tối thiểu | SAD header, §7, §10 |
| DF-25 | Minor | Fixed | Ghi rõ mục hoãn và cách lưu `conversation_id`; cách đọc audit_log bằng sqlite3 | openapi.md §4.2, use_cases.md UC-11 |
| DF-26 | Minor | Open (con người) | ADR vẫn `Proposed` — chỉ người duyệt mới đổi thành `Accepted`. Agent không tự phê duyệt | Architect, Tech Lead, IT |
| DF-27 | Minor | Fixed | TLS + `CWD_COOKIE_SECURE=true` + mã hóa đĩa là mục bắt buộc trong checklist go-live | SAD §7, release-plan.md |

**Tổng:** 21 Fixed · 3 Partial · 3 Deferred · 1 Open (cần con người; DF-18 tính trong Deferred).

Sau REFINE: `tools/cross_view_audit.py` → 36 PASS / 0 FAIL; toàn bộ test xanh.

## Cải tiến công cụ rút ra
Reviewer chỉ ra cross-view audit chỉ kiểm tra **ID có xuất hiện**. Đã thêm kiểm tra enum `Problem.code` trong openapi = khóa `MESSAGES` trong `app/errors.py` (PASS). Backlog: kiểm tra ID trùng tiền tố giữa các tài liệu và tên trạng thái UI.
