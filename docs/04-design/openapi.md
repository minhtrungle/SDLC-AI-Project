# API Design — Chat với tài liệu (MVP)

> **Prompt:** [apiDesign_prompt.md](../prompts/apiDesign_prompt.md) · **Hợp đồng máy đọc được:** [openapi.yaml](../../app/api-contract/openapi.yaml) (OpenAPI 3.1) · **Checklist:** [API_Design_IEEE-1016-2009Checklist.xlsx](../checklists/API_Design_IEEE-1016-2009Checklist.xlsx)

## 1. Người dùng API
| Persona | Dùng API qua | Nhu cầu |
|---|---|---|
| Web UI (CMP-01) | Trình duyệt, cookie | Toàn bộ endpoint |
| QA / test tự động | `TestClient`, httpx | Hợp đồng ổn định, mã lỗi cố định |
| Tích hợp sau này | — | Không cam kết trong MVP; API chỉ dành cho Web UI |

## 2. Quy ước
| Chủ đề | Quy ước |
|---|---|
| Base path | `/api` |
| Định dạng | JSON UTF-8; upload `multipart/form-data` field `files` (lặp lại) |
| Xác thực | Cookie `cwd_session`; thiếu/hết hạn → 401 `auth.required` |
| CSRF | Header `X-CSRF-Token` cho `POST/PUT/DELETE` trừ `/api/auth/login`; sai → 403 `csrf.invalid` |
| Phân quyền | Tài nguyên ngoài workspace → 404 `not_found`; thiếu vai trò → 403 `auth.forbidden` |
| Lỗi | `application/problem+json`: `{type, title, status, code, detail}`; `title` là câu tiếng Việt hiển thị được; không có stack trace |
| Thời gian | ISO 8601 UTC (`2026-10-28T09:15:00Z`) |
| ID | Tài liệu/hội thoại/lượt: chuỗi hex 32 ký tự; chunk: số nguyên |
| Phiên bản | Chưa đánh phiên bản URL trong MVP; thay đổi phá vỡ phải cập nhật openapi + ADR |

## 3. Danh mục endpoint
| Method | Path | operationId | CMP | Yêu cầu | Mã lỗi chính |
|---|---|---|---|---|---|
| GET | /api/health | health | CMP-02 | NFR-005 | — |
| GET | /api/config | getConfig | CMP-02 | FR-003 | — |
| POST | /api/auth/login | login | CMP-03 | FR-001 | 401 `auth.invalid_credentials`, 429 `auth.too_many_attempts` |
| POST | /api/auth/logout | logout | CMP-03 | FR-002 | 401, 403 |
| GET | /api/auth/me | getMe | CMP-03 | FR-002 | 401 |
| GET | /api/documents | listDocuments | CMP-04 | FR-007 | 401 |
| POST | /api/documents | uploadDocuments | CMP-04 | FR-004..006 | lỗi theo từng file trong `results[]` |
| GET | /api/documents/{document_id} | getDocument | CMP-04 | FR-006 | 404 |
| DELETE | /api/documents/{document_id} | deleteDocument | CMP-04 | FR-008 | 404 |
| GET | /api/chunks/{chunk_id} | getChunk | CMP-08 | FR-013 | 404 |
| POST | /api/conversations | createConversation | CMP-08 | FR-016 | — |
| GET | /api/conversations/{conversation_id} | getConversation | CMP-08 | FR-016 | 404 |
| POST | /api/conversations/{conversation_id}/questions | askQuestion | CMP-08 | FR-009..015 | 422 `chat.invalid_question`, 409 `chat.no_ready_documents`, 503 `chat.ai_unavailable` |
| PUT | /api/turns/{turn_id}/feedback | setFeedback | CMP-09 | FR-017 | 422 `feedback.invalid`, 404 |
| GET | /api/metrics/weekly | getWeeklyMetrics | CMP-09 | FR-018 | 403 `auth.forbidden` |

## 4. Ví dụ

**Hỏi đáp có trích dẫn**
```http
POST /api/conversations/3f9c.../questions
X-CSRF-Token: 6b1e...
Content-Type: application/json

{"question": "Giá trị hợp đồng Alpha là bao nhiêu?"}
```
```json
{
  "id": "a81d...", "question": "Giá trị hợp đồng Alpha là bao nhiêu?",
  "answer": "Theo tài liệu đã tải lên:\n- Giá trị hợp đồng Alpha là 2,5 tỷ đồng, thanh toán làm 3 đợt. [1]",
  "outcome": "answered",
  "citations": [{"index": 1, "chunk_id": 42, "document_id": "c0de...", "document_name": "HopDong_Alpha.pdf",
                 "page": 2, "snippet": "Giá trị hợp đồng Alpha là 2,5 tỷ đồng, thanh toán làm 3 đợt.", "document_deleted": false}],
  "document_ids": null, "warning": null, "latency_ms": 38, "feedback": null,
  "created_at": "2026-10-28T09:15:00Z"
}
```

**Không tìm thấy**
```json
{"outcome": "not_found", "answer": "Không tìm thấy thông tin trong tài liệu đã tải lên. Bạn có thể thử diễn đạt khác hoặc kiểm tra tài liệu đã đủ chưa.", "citations": []}
```

**Lỗi của một file khi tải lên** (HTTP 200, lỗi nằm trong `results[]` — DF-06)
```json
{"results": [{"filename": "ghi-chu.docx", "ok": false,
              "error": {"code": "file.wrong_type", "message": "Sai định dạng, chỉ chấp nhận PDF."}}]}
```

**Lỗi problem+json**
```json
{"type": "about:blank", "title": "Câu hỏi phải có từ 1 đến 2000 ký tự.", "status": 422, "code": "chat.invalid_question"}
```

## 4.1 Bảng mã lỗi (nguồn duy nhất của thông điệp: `app/backend/cwd/errors.py`, `app/backend/cwd/documents.py`)
| Mã | HTTP | Nơi xuất hiện | Thông điệp tiếng Việt |
|---|---|---|---|
| auth.required | 401 | Mọi endpoint bảo vệ | Bạn cần đăng nhập để tiếp tục. |
| auth.invalid_credentials | 401 | login | Tên đăng nhập hoặc mật khẩu không đúng. |
| auth.too_many_attempts | 429 | login | Bạn đã nhập sai quá nhiều lần. Vui lòng thử lại sau 5 phút. |
| auth.forbidden | 403 | getWeeklyMetrics | Bạn không có quyền thực hiện thao tác này. |
| csrf.invalid | 403 | Mọi POST/PUT/DELETE trừ login | Phiên làm việc không hợp lệ. Vui lòng tải lại trang. |
| not_found | 404 | Tài nguyên không tồn tại hoặc của người khác | Không tìm thấy dữ liệu yêu cầu. |
| file.wrong_type | 200 (trong results[]) | uploadDocuments | Sai định dạng, chỉ chấp nhận PDF. |
| file.too_large | 200 (trong results[]) | uploadDocuments | Tệp vượt dung lượng cho phép (tối đa N MB). |
| docs.limit_reached | 200 (trong results[]) | uploadDocuments | Đã đạt số lượng tài liệu tối đa của workspace. |
| chat.invalid_question | 422 | askQuestion | Câu hỏi phải có từ 1 đến 2000 ký tự. |
| chat.no_ready_documents | 409 | askQuestion | Chưa có tài liệu nào sẵn sàng để hỏi. |
| chat.ai_unavailable | 503 | askQuestion (chế độ external) | Dịch vụ trả lời đang gặp sự cố. Vui lòng thử lại. |
| feedback.invalid | 422 | setFeedback | Đánh giá không hợp lệ. |
| validation.error | 422 | Body/query sai kiểu | Dữ liệu gửi lên không hợp lệ. |
| internal | 500 | Lỗi không lường trước (mọi endpoint) | Đã có lỗi xảy ra. Vui lòng thử lại sau. |

Mã trạng thái tài liệu (`Document.error_code`): `pdf.corrupt` (PDF hỏng), `pdf.encrypted` (có mật khẩu), `ingest.interrupted` (file gốc mất khi xử lý lại sau khởi động — DF-15).

## 4.2 Ngoài phạm vi API MVP (DF-25)
- Không có endpoint liệt kê hội thoại (US-404 hoãn). Web UI giữ `conversation_id` hiện tại trong `sessionStorage`.
- Không có endpoint tóm tắt (US-601 hoãn), không có endpoint retry tài liệu (xóa và tải lại).
- Không có idempotency key cho câu hỏi; "Gửi lại" sau lỗi mạng có thể tạo lượt trùng — chấp nhận ở MVP (DF-16).

## 5. Kịch bản chất lượng API
| ID | Kịch bản | Thước đo |
|---|---|---|
| AQ-01 | Gọi API không có cookie | 100% endpoint bảo vệ trả 401 |
| AQ-02 | Gọi API ghi không có CSRF | 100% trả 403 |
| AQ-03 | Hợp đồng lệch code | Test `test_contract.py` thất bại trong CI |
| AQ-04 | Lỗi bất ngờ | 500 problem+json, không lộ stack trace |

## 6. Bảo mật API
Xem SAD §8.1 và ADR-007. Giới hạn kích thước upload ở mức ứng dụng (`CWD_MAX_FILE_MB`) và nên giới hạn thêm ở reverse proxy.
