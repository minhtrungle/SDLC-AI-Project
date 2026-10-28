# Design Blueprint (IEEE 1016-2009) — Chat với tài liệu (MVP)

> **Prompt:** [bluePrint_design_prompt.md](../prompts/bluePrint_design_prompt.md) · **Checklist:** [BluePrint_Design_IEEE_1016_2009_Checklist.xlsx](../design/BluePrint_Design_IEEE_1016_2009_Checklist.xlsx)
> **Quan hệ với SAD:** SAD mô tả kiến trúc (arc42). Blueprint mô tả thiết kế chi tiết theo các *design view* IEEE 1016 để dev hiện thực trực tiếp. ID phần tử theo [elements.yaml](elements.yaml).
> **Phiên bản:** 0.2 · 2026-10-28 · Agent (Claude) · chờ Tech Lead duyệt

## 1. Bối cảnh và đối tượng thiết kế

### 1.1 Nhận diện hệ thống
CWD — ứng dụng web hỏi đáp trên PDF có trích dẫn. Đơn vị triển khai: một tiến trình Python + một thư mục dữ liệu.

### 1.2 Phạm vi và ranh giới
Trong: CMP-01..CMP-13. Ngoài: IdP/SSO, OCR, kho tài liệu khác, Anthropic API (hệ thống ngoài tùy chọn).

### 1.3 Giả định và ràng buộc
TC-01..TC-04 (SAD §2); ASM-001 (PDF có lớp văn bản); quy mô PRD §3.9.4.

## 2. Stakeholder và mối quan tâm

| Stakeholder | Mối quan tâm thiết kế | View trả lời |
|---|---|---|
| Dev | Module nào làm gì, gọi nhau thế nào | Composition, Dependency, Interface |
| QA | Trạng thái, luồng, điểm kiểm thử | State dynamics, Interaction |
| IT/Bảo mật | Dữ liệu nào lưu ở đâu | Information, SAD §8.1 |
| UX | Trạng thái giao diện | State dynamics, UI_UX_design |

### 2.1 Kịch bản chất lượng
Xem SAD §10 (QS-01..QS-07).

### 2.2 Kịch bản chất lượng UX/UI
| ID | Kịch bản | Thước đo |
|---|---|---|
| UQ-01 | Người dùng mới đăng nhập lần đầu, workspace trống → thấy hướng dẫn tải tài liệu, ô hỏi bị khóa có lý do | 100% (EC-01) |
| UQ-02 | Chỉ dùng bàn phím: tải lên, hỏi, mở trích dẫn, đóng panel | Hoàn thành không cần chuột |
| UQ-03 | Trình đọc màn hình đọc câu trả lời mới | Vùng `aria-live="polite"` |
| UQ-04 | Tài liệu chuyển `processing → ready` | UI cập nhật ≤ 4 s, không tải lại trang |

### 2.3 Ma trận ràng buộc UX/UI
| Ràng buộc | Giá trị | Nguồn |
|---|---|---|
| Ngôn ngữ | 100% tiếng Việt | NFR-003 |
| Tương phản | ≥ 4.5:1 | NFR-009 |
| Vùng chạm | ≥ 44 px | Design token prototype |
| Độ rộng tối thiểu | 1280 px | PRD §3.9.4 |
| Trạng thái | Biểu tượng + chữ, không chỉ màu | UX-002 |

## 3. Design views

### 3.1 Composition view
```
app/
├── main.py         CMP-02  create_app(settings) → FastAPI
├── config.py       CMP-13  Settings (dataclass, đọc env)
├── db.py           CMP-11  connect(), init_schema(), transaction()
├── schema.sql      CMP-11
├── errors.py       CMP-02  ProblemError, handlers, thông điệp tiếng Việt
├── security.py     CMP-03  hash_password, verify_password, new_token, LoginLimiter
├── auth.py         CMP-03  router /api/auth/*, current_user, require_csrf, require_manager
├── audit.py        CMP-10  record(conn, action, user, target)
├── documents.py    CMP-04  router /api/documents*, validate_upload
├── ingestion.py    CMP-05  ingest_document(), extract_pages(), chunk_page(), recover_pending()
├── textnorm.py     CMP-06  fold(), tokens(), content_terms()
├── retrieval.py    CMP-06  FtsRetriever, RetrievedChunk
├── generation.py   CMP-07  LocalExtractiveGenerator, AnthropicGenerator, build_generator()
├── chat.py         CMP-08  router /api/conversations*, /api/chunks/*, ask()
├── metrics.py      CMP-09  router /api/turns/*/feedback, /api/metrics/weekly
├── cli.py          CMP-12  create-user, seed-demo, backup, restore, prune-audit
└── web/            CMP-01  index.html, styles.css, api.js, app.js
```

### 3.2 Dependency view
Quy tắc phụ thuộc (kiểm tra trong review): `web → (HTTP) → main → {auth, documents, chat, metrics} → {retrieval, generation, ingestion, audit} → db`. `textnorm`, `config`, `errors` là lá. Không module nghiệp vụ nào import `main`. `generation` không import `db` (chỉ nhận chunk).

### 3.3 Logical view (lớp chính) — [diagrams/class_diagram.drawio](diagrams/class_diagram.drawio)
| Lớp / kiểu | Thuộc tính / phương thức | Ghi chú |
|---|---|---|
| `Settings` | `data_dir, max_file_mb, max_docs, min_relevance, top_k, per_doc_limit, session_idle_hours, allow_external_ai, anthropic_model, answer_timeout_s, cookie_secure`; `from_env()` | frozen dataclass |
| `CurrentUser` | `id, username, role, csrf_token` | |
| `RetrievedChunk` | `chunk_id, document_id, document_name, page, text, relevance` | |
| `FtsRetriever` | `retrieve(conn, user_id, question, history, document_ids)` | ADR-004 |
| `GeneratedAnswer` | `text, used_indices: list[int]` | chỉ số 1-based |
| `AnswerGenerator` (Protocol) | `mode`, `generate(question, chunks)` | |
| `LocalExtractiveGenerator` | chọn câu theo điểm từ, ≤ 1 câu tốt nhất mỗi chunk, ≤ 4 câu | ADR-003 |
| `AnthropicGenerator` | `client, model, timeout`; `generate()` | ADR-003 |
| `LoginLimiter` | `max_failures=5, window_s=300`; `check(key)`, `fail(key)`, `reset(key)` | ADR-007 |
| `ProblemError` | `status, code, detail` | |

### 3.4 Information view
Xem [data/model.md](data/model.md). Thông tin nhạy cảm: `documents/chunks/turns` (nội dung kinh doanh), `users.password_hash`, `sessions`. Không bảng nào lưu token thô.

### 3.5 Interface view
- API ngoài: [openapi.yaml](openapi.yaml), giải thích ở [openapi.md](openapi.md).
- Interface nội bộ: SAD §5.3.
- Hợp đồng lỗi: problem+json, `code` cố định (enum trong openapi).

### 3.6 Interaction view
| Tương tác | Sơ đồ |
|---|---|
| Hỏi đáp | [sequence_diagram.drawio](diagrams/sequence_diagram.drawio) (trang "Hỏi đáp") |
| Đăng nhập | [sequence_diagram.drawio](diagrams/sequence_diagram.drawio) (trang "Đăng nhập") |
| Tải lên + xử lý | [activity_diagram.drawio](diagrams/activity_diagram.drawio) |
| Use case | [use_case_diagram.drawio](diagrams/use_case_diagram.drawio) |

### 3.7 State dynamics view

**Tài liệu (ENT-03)**
```mermaid
stateDiagram-v2
    [*] --> processing : tải lên hợp lệ
    processing --> ready : có văn bản
    processing --> no_text : văn bản < 20 ký tự
    processing --> failed : pdf.corrupt / pdf.encrypted
    processing --> processing : khởi động lại (recover_pending)
    ready --> [*] : xóa
    no_text --> [*] : xóa
    failed --> [*] : xóa
    processing --> [*] : xóa (tác vụ nền bỏ kết quả)
```

**Ô hỏi trên UI (SCR-02)**
| Trạng thái | Điều kiện | Hiển thị |
|---|---|---|
| `disabled_empty` | 0 tài liệu | "Hãy tải tài liệu để bắt đầu hỏi" |
| `disabled_processing` | 0 `ready`, ≥ 1 `processing` | "Đang xử lý n tài liệu…" |
| `ready` | ≥ 1 `ready` | Cho nhập |
| `sending` | Đã gửi, chờ phản hồi | "Đang trả lời…", khóa nút gửi |
| `error` | Lỗi mạng/AI | Giữ câu hỏi, nút "Gửi lại" |

### 3.8 Patterns use view
| Mẫu | Nơi dùng | Lý do |
|---|---|---|
| RAG | CMP-06/07/08 | Grounding + trích dẫn |
| Strategy | `AnswerGenerator` | Đổi mô hình bằng cấu hình |
| Repository (hàm truy vấn tập trung) | `db.py` + từng service | Cô lập SQL |
| App factory | `create_app(settings)` | Test với cấu hình riêng |
| Double-submit CSRF token | CMP-03 | Cookie SameSite + header |

## 4. Truy vết Stakeholder → Concern → Thiết kế → Yêu cầu
| Concern | Thiết kế | Yêu cầu |
|---|---|---|
| Tin được câu trả lời | ADR-004 ngưỡng, ADR-005 trích dẫn | FR-011..013 |
| Không lộ dữ liệu | ADR-003, ADR-007, SAD §8.1 | FR-003, NFR-004, NFR-008 |
| Dễ dùng tiếng Việt | textnorm, UI tiếng Việt | NFR-003 |
| Đo được giá trị | CMP-09 | FR-017, FR-018 |

## 5. Chiến lược xác minh thiết kế
1. Cross-view audit tự động: [cross-view-audit.md](cross-view-audit.md) (`tools/cross_view_audit.py`).
2. Audit theo checklist IEEE 1016 / UML 2.0 bởi reviewer độc lập: [design_checklist_audit.md](design_checklist_audit.md).
3. Test hợp đồng: test kiểm tra route FastAPI khớp `elements.yaml`/`openapi.yaml`.

## 6. Rủi ro thiết kế
Xem SAD §11.
