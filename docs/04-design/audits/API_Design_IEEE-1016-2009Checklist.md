# Audit — API Design theo checklist

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | app/api-contract/openapi.yaml (OpenAPI 3.1, v0.2.0, sau REFINE), docs/04-design/openapi.md; đối chiếu app/backend/cwd/*.py |
| Checklist | docs/checklists/API_Design_IEEE-1016-2009Checklist.xlsx |
| Reviewer | artifact-auditor (agent) — vòng 1: Independent reviewer agent |
| Ngày | 2026-11-02 (vòng 1: 2026-10-28) |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d), đối chiếu design-refine-log.md DF-01..DF-27 và code app/ hiện tại |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Protocol Selection | Done | REST/JSON + multipart cho upload (openapi.md §2). Không dùng SSE; lý do ở ADR-009 (thay ADR-006), SAD TD-01 và blueprint §6 EC-06. |
| 3 | Idempotency | In Progress | GET an toàn, PUT feedback idempotent (upsert, model.md ENT-07), DELETE 204 rồi 404. POST .../questions vẫn không có Idempotency-Key: openapi.md §4.2 ghi rõ Gửi lại có thể tạo lượt trùng, hoãn (DF-16 Partial, owner Tech Lead). |
| 4 | Statelessness | In Progress | Cố ý dùng phiên phía máy chủ (cookie cwd_session + bảng sessions, ADR-007) và LoginLimiter trong bộ nhớ tiến trình (SAD R-06). Đánh đổi có ghi lại và chấp nhận cho MVP nhưng không đạt tiêu chí stateless. |
| 5 | Resource Naming | Done | Danh từ: /documents, /conversations, /chunks, /turns. Lưu ý vẫn còn: POST /conversations/{id}/questions trả Turn, Turn truy cập qua /turns/{id}. |
| 6 | Pluralization & Case | Done | Tập hợp số nhiều, đường dẫn chữ thường; /metrics/weekly là tài nguyên báo cáo. |
| 7 | Nesting Depth | Done | Tối đa 2 cấp (/conversations/{id}/questions). |
| 8 | JSON Standards | Done | snake_case nhất quán (document_id, latency_ms, size_bytes, error_code); thời gian ISO 8601 UTC có Z (openapi.md §2). |
| 9 | Pagination | In Progress | Không endpoint nào phân trang. listDocuments bị chặn bởi CWD_MAX_DOCS=50 (chấp nhận được); US-404 hoãn đã ghi ở openapi.md §4.2 (DF-25). getConversation vẫn trả toàn bộ turns không giới hạn (chat.py dòng 117 không LIMIT). |
| 10 | Filtering & Sorting | Pending | Hợp đồng không có tham số lọc/sắp xếp và không đặc tả thứ tự mặc định của listDocuments. Code sắp created_at DESC (documents.py dòng 57) nhưng openapi.yaml/openapi.md chưa ghi. |
| 11 | Partial Updates | N/A | Không có tài nguyên cần cập nhật một phần; feedback dùng PUT thay thế toàn bộ, phù hợp. |
| 12 | HTTP Status Codes | In Progress | Đã sửa (DF-06): `internal` 500 ở openapi.md §4.1 (mọi endpoint) và AQ-04; `validation.error` = 422; ví dụ upload đúng 200 + results[]. Còn lệch: code trả 413 `request.too_large` (main.py BodyLimitMiddleware, documents.py dòng 73) nhưng openapi.yaml không khai báo 413/500 ở endpoint nào và §4.1 không có dòng request.too_large. |
| 13 | Standard Error Envelope | In Progress | problem+json (RFC 9457) với enum code có `internal`; Document.error_code có enum (pdf.corrupt, pdf.encrypted, ingest.interrupted). Còn: UploadResult.error vẫn là cấu trúc riêng {code, message}, `code` không có enum (openapi.yaml dòng 405–409) dù §4.1 liệt kê 3 giá trị. |
| 14 | Correlation IDs | Pending | Problem không có request_id/instance, không có header X-Request-ID; middleware log (main.py) không sinh request_id. DF-17 Deferred tới sau go-live (owner Tech Lead). |
| 15 | API Versioning | Pending | Chưa có version trong URL/header (openapi.md §2 Phiên bản: chưa đánh phiên bản URL; thay đổi phá vỡ cập nhật openapi + ADR). Không thay đổi sau REFINE. |
| 16 | Deprecation Strategy | Pending | Không có quy trình deprecation (Sunset/Deprecation header). Không thay đổi sau REFINE. |
| 17 | Authentication | Done | securitySchemes sessionCookie toàn cục; endpoint công khai security: [] (health, config, login); 401 khai báo ở endpoint bảo vệ; AQ-01 kiểm chứng. |
| 18 | Authorization (RBAC/ABAC) | Done | 404 cho tài nguyên ngoài workspace (NFR-004), 403 auth.forbidden cho metrics. Rủi ro tái sử dụng chunk_id đã đóng: chunks.id AUTOINCREMENT (DF-01, test_chunk_ids_not_reused_after_delete). |
| 19 | Rate Limiting | In Progress | Chỉ giới hạn đăng nhập 5/5 phút theo username (429). Không giới hạn tần suất upload hay câu hỏi (chỉ giới hạn kích thước 413 và 10 file/lần); EC-17 hoãn (blueprint §6). Khóa theo username có thể bị lạm dụng: DF-18 Deferred → L3 (owner IT/Bảo mật). |
| 20 | Input Validation | In Progress | Đã thêm (DF-16): question maxLength 4000 + kiểm tra 1–2000 ở máy chủ; document_ids maxItems 50, pattern hex 32; reason maxLength 5000 + kiểm tra 500. Còn: path id (document_id, conversation_id, turn_id) không có pattern; files không có maxItems trong hợp đồng dù code giới hạn MAX_FILES_PER_REQUEST = 10 (documents.py dòng 18). |
| 21 | Documentation | Done | OpenAPI 3.1 + openapi.md (quy ước, danh mục, ví dụ, bảng mã lỗi §4.1, ngoài phạm vi §4.2, AQ-01..04). Minor: AQ-03 nhắc test_contract.py nhưng app/backend/tests không có file này; đồng bộ thực tế dựa vào npm run check:api và tools/cross_view_audit.py. |
| 22 | HATEOAS (Optional) | N/A | Tùy chọn; API chỉ phục vụ Web UI nội bộ (openapi.md §1). |

## Kiểm tra lại vòng trước
| Row | Vấn đề vòng 1 | Kết quả vòng 2 |
|---|---|---|
| 3 | Không có idempotency key | Hoãn có ghi nhận (DF-16) |
| 9 | Không ghi rõ US-404 hoãn | Đã ghi (DF-25); getConversation vẫn không giới hạn |
| 10 | Không ghi thứ tự mặc định | Chưa sửa |
| 12 | Thiếu 500, 413, status validation.error, ví dụ upload mâu thuẫn | 500, 422, ví dụ đã sửa; 413 còn lệch |
| 13 | UploadResult.error riêng, thiếu internal, error_code không enum | internal + error_code đã sửa; UploadResult.error chưa |
| 14 | Không có correlation id | Hoãn (DF-17) |
| 19 | Không giới hạn upload/câu hỏi; DoS khóa tài khoản | Hoãn (DF-18 → L3) |
| 20 | Thiếu maxLength/maxItems/pattern | Phần lớn đã sửa; còn path id và số file |

## Phát hiện
| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-API-01 | Major | openapi.yaml uploadDocuments; openapi.md §4.1 | Code trả 413 request.too_large (BodyLimitMiddleware, > 10 file) nhưng hợp đồng contract-first không khai báo 413 và bảng mã lỗi không có dòng này | Thêm response 413 cho POST/PUT và dòng request.too_large vào §4.1 |
| AUD-API-02 | Minor | openapi.yaml dòng 405–409 | UploadResult.error.code không có enum | Thêm enum file.wrong_type, file.too_large, docs.limit_reached |
| AUD-API-03 | Minor | openapi.yaml path parameters | document_id, conversation_id, turn_id không có pattern ^[0-9a-f]{32}$ (openapi.md §2 đã định nghĩa định dạng) | Thêm pattern |
| AUD-API-04 | Minor | openapi.yaml/openapi.md listDocuments | Không ghi thứ tự mặc định (code: created_at DESC) | Ghi vào description |
| AUD-API-05 | Minor | getConversation | Trả toàn bộ turns không giới hạn | Ghi giới hạn hoặc thêm limit |
| AUD-API-06 | Minor | SAD §8.2 so với main.py | SAD nói log có request_id, code không có | Đồng bộ với DF-17 |
| AUD-API-07 | Minor | openapi.md §5 AQ-03 | Tham chiếu test_contract.py không tồn tại trong app/backend/tests | Sửa tham chiếu sang check:api / cross_view_audit.py hoặc thêm test |

## Tóm tắt
- Status: Done 8 · In Progress 7 · Pending 4 · N/A 2 (tổng 21).
- Phát hiện: Critical 0 · Major 1 · Minor 6.
- Nhận định: Cần sửa — AUD-API-01 (413 lệch hợp đồng) nên sửa trước baseline; các Pending (14, 15, 16) và In Progress 3, 4, 19 là quyết định hoãn/đánh đổi có owner, cần người duyệt chấp nhận rủi ro.

## Lịch sử audit
| Ngày | Vòng | Row | Status cũ → mới | Lý do |
|---|---|---|---|---|
| 2026-10-28 | 1 | — | — | Audit ban đầu: Done 8, In Progress 7, Pending 4, N/A 2 |
| 2026-11-02 | 2 | — | Không có dòng đổi Status | REFINE sửa một phần Row 9, 12, 13, 20 nhưng mỗi dòng còn lỗ hổng (413 lệch hợp đồng, UploadResult.error, path pattern); Row 3, 14, 19 là Deferred có owner nên giữ nguyên |
| 2026-11-02 | 2 | 2, 8, 18, 21 | Done → Done | Cập nhật Notes: ADR-009, error_code, DF-01 đóng rủi ro chunk_id, §4.1/§4.2 |
