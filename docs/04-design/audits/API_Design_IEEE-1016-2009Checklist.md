# Audit — API Design theo checklist

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | app/api-contract/openapi.yaml (OpenAPI 3.1, v0.2.0), docs/04-design/openapi.md |
| Checklist | docs/checklists/API_Design_IEEE-1016-2009Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Protocol Selection | Done | REST/JSON + multipart cho upload (openapi.md §2). Không dùng SSE; lý do ở ADR-006 và SAD TD-01. |
| 3 | Idempotency | In Progress | GET an toàn, PUT feedback idempotent, DELETE 204 rồi 404. Nhưng POST .../questions không có Idempotency-Key: nút "Gửi lại" (EC-04) sau khi mất kết nối có thể tạo lượt trùng trong turns. Cần khóa idempotency hoặc client_request_id. |
| 4 | Statelessness | In Progress | Cố ý dùng phiên phía máy chủ (cookie cwd_session + bảng sessions, ADR-007); LoginLimiter giữ trạng thái trong bộ nhớ tiến trình. Đánh đổi đã ghi lại nhưng không stateless theo nghĩa checklist. |
| 5 | Resource Naming | Done | Danh từ: /documents, /conversations, /chunks, /turns. Lưu ý: POST /conversations/{id}/questions trả về Turn và Turn lại được truy cập qua /turns/{id} — tên tài nguyên không nhất quán (questions và turns). |
| 6 | Pluralization & Case | Done | Tập hợp số nhiều, đường dẫn chữ thường; /metrics/weekly là tài nguyên báo cáo. |
| 7 | Nesting Depth | Done | Tối đa 2 cấp (/conversations/{id}/questions). |
| 8 | JSON Standards | Done | snake_case nhất quán (document_id, latency_ms, size_bytes); thời gian ISO 8601 UTC (openapi.md §2). |
| 9 | Pagination | In Progress | Không endpoint nào phân trang. listDocuments bị chặn bởi CWD_MAX_DOCS=50 (chấp nhận được), nhưng getConversation trả toàn bộ turns không giới hạn và không có GET danh sách hội thoại (US-404 hoãn, chưa ghi rõ). |
| 10 | Filtering & Sorting | Pending | Không có tham số lọc/sắp xếp; thứ tự trả về của listDocuments không được đặc tả (theo created_at?). Ít nhất phải ghi rõ thứ tự mặc định. |
| 11 | Partial Updates | N/A | Không có tài nguyên cần cập nhật một phần; feedback dùng PUT thay thế toàn bộ, phù hợp. |
| 12 | HTTP Status Codes | In Progress | Dùng 200/201/204/401/403/404/409/422/429/503. Thiếu: 500 (SAD §8.2 có `internal`) không khai báo ở endpoint nào; 413 khi request vượt giới hạn proxy; status của `validation.error` (400 hay 422) không định nghĩa. Ví dụ lỗi openapi.md §4 ghi status 422 cho `file.wrong_type` nhưng uploadDocuments trả 200 với lỗi trong results[] — mâu thuẫn. |
| 13 | Standard Error Envelope | In Progress | problem+json (RFC 9457) với code ổn định. Nhưng UploadResult.error dùng cấu trúc riêng {code, message} không theo Problem và `code` không có enum; enum Problem.code thiếu `internal`; `pdf.encrypted`, `pdf.corrupt`, `ingest.interrupted` (Document.error_code) không có enum/mô tả. |
| 14 | Correlation IDs | Pending | SAD §8.2 nói log có request_id nhưng Problem không có trường request_id/instance và không có header X-Request-ID. |
| 15 | API Versioning | Pending | Chưa có version trong URL/header (openapi.md §2 ghi "chưa đánh phiên bản"). Có quy tắc cập nhật openapi + ADR khi phá vỡ, chấp nhận cho MVP nội bộ nhưng chưa đạt mục. |
| 16 | Deprecation Strategy | Pending | Không có quy trình deprecation (Sunset/Deprecation header). |
| 17 | Authentication | Done | securitySchemes sessionCookie áp dụng toàn cục; endpoint công khai đặt security: [] (health, config, login); 401 khai báo ở endpoint bảo vệ. |
| 18 | Authorization (RBAC/ABAC) | Done | 404 cho tài nguyên ngoài workspace (NFR-004), 403 `auth.forbidden` cho metrics. Lưu ý rủi ro chunk_id là số nguyên tuần tự có thể bị tái sử dụng (xem Database audit row 10). |
| 19 | Rate Limiting | In Progress | Chỉ giới hạn đăng nhập (5/5 phút theo username, trả 429). Không giới hạn upload hay câu hỏi; EC-17 / copy `limit.reached` không có mã lỗi API. Giới hạn theo username cho phép khóa tài khoản người khác (DoS) và không chặn password spraying. |
| 20 | Input Validation | In Progress | login có min/maxLength; weeks có min/max; rating enum; reason maxLength 500. Thiếu: question chỉ ghi "1–2000 ký tự" trong description, không có maxLength; document_ids không có maxItems/pattern; path id không có pattern (hex 32); không giới hạn số file mỗi lần upload. |
| 21 | Documentation | Done | OpenAPI 3.1 máy đọc được + openapi.md (quy ước, danh mục, ví dụ, kịch bản AQ-01..04). |
| 22 | HATEOAS (Optional) | N/A | Tùy chọn; API chỉ phục vụ Web UI nội bộ (openapi.md §1). |

## Tóm tắt
Hợp đồng rõ ràng, snake_case nhất quán, bảo mật cookie + CSRF + 404 cô lập. Cần sửa: mâu thuẫn ví dụ lỗi upload, hợp nhất cấu trúc lỗi, thêm `internal`/500, correlation id, idempotency cho câu hỏi, ràng buộc maxLength/maxItems.
