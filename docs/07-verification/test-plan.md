# Chat với tài liệu — Master Test Plan (MTP)

> **Chuẩn:** IEEE 829-2008 (Software Test Documentation) · **Prompt:** [testPlan_prompt.md](../prompts/testPlan_prompt.md)
> **Checklist:** [Test_Plan_IEEE_829_Checklist.xlsx](../checklists/Test_Plan_IEEE_829_Checklist.xlsx). Kết quả audit ở [Phụ lục B](#phụ-lục-b--audit-theo-checklist-ieee-829)
> **Kết quả thực hiện:** [test-report.md](test-report.md) · bằng chứng E2E: [test_reports/report.md](../../test_reports/report.md)

---

## Phần A — Phân tích tài liệu đầu vào (prompt §2)

### A.1 Danh mục tài liệu đầu vào
| Loại | Tài liệu | Phiên bản | Nguồn | Thông tin chính dùng cho test |
|---|---|---|---|---|
| SRS/PRD | [PRD.md](../03-analysis/PRD.md) §3.9 | 0.2 | BA / Agent | FR-001..FR-019, NFR-001..NFR-010, UX-001..011, EC-01..17, launch gate LG-01..25 |
| BRD | [BRD.md](../02-requirements/BRD.md) | 0.2 | BA | BR-001..BR-028, ngưỡng mặc định §12.1 |
| SAD | [SAD.md](../04-design/SAD.md) | 0.4 | Architect / Agent | CMP-01..13, kịch bản chất lượng QS-01..09, ADR-001..009 |
| Blueprint (IEEE 1016) | [blueprint.md](../04-design/blueprint.md) | 0.2 | Architect | Máy trạng thái tài liệu / ô hỏi (§3.7), thuật toán (§3.9) |
| UI/UX | [UI_UX_design/](../04-design/UI_UX_design/README.md) | 0.2 | UX | SCR-01..06, WCAG 2.1 AA |
| API | [app/api-contract/openapi.yaml](../../app/api-contract/openapi.yaml) · [openapi.md](../04-design/openapi.md) | 0.2 | Dev | 15 endpoint, 16 mã lỗi problem+json |
| User Stories | [USER_STORIES.md](../03-analysis/USER_STORIES.md) | 0.2 | PO | 19 story trong phạm vi, AC dạng Given/When/Then |
| Development Plan | [PLAN.md](../05-implement/PLAN.md) | — | PO / Tech Lead | T-01..T-10, sprint S1–S3 |
| Data model | [data/model.md](../04-design/data/model.md) | 0.2 | Dev | 8 bảng + FTS5, ràng buộc toàn vẹn |

### A.2 Yêu cầu kiểm thử được (trích PRD §3.9)
| ID | Loại | Mô tả ngắn | Ưu tiên | Story |
|---|---|---|---|---|
| FR-001 / FR-002 | Chức năng | Đăng nhập; mọi API bảo vệ trả 401 khi không có phiên; hết hạn 8 h | High | US-101 |
| FR-003 | Chức năng / chính sách | Không gọi AI bên ngoài khi chưa cho phép | High | US-102 |
| FR-004..FR-007 | Chức năng | Tải lên nhiều PDF, từ chối file sai, xử lý nền + trạng thái, danh sách | High | US-201..204 |
| FR-008 | Chức năng | Xóa tài liệu và mọi chunk | Medium | US-205 |
| FR-009..FR-013 | Chức năng | Hỏi đáp, truy xuất đa tài liệu, grounding, not_found, trích dẫn từ CSDL | High | US-301..305 |
| FR-014..FR-016 | Chức năng | Hỏi tiếp, phạm vi tài liệu, lịch sử hội thoại | Medium | US-401..403 |
| FR-017 / FR-018 | Chức năng | Đánh giá câu trả lời; số liệu tuần (manager) | Medium | US-501/502 |
| FR-019 | Chức năng / kiểm toán | Nhật ký kiểm toán | High | US-103 |
| NFR-001 / NFR-002 | Hiệu năng / chất lượng AI | P90 ≤ 2 s (cục bộ); đúng ≥ 85%, trích dẫn ≥ 90%, not_found ≥ 9/10 | High | US-306 |
| NFR-003 | Khả dụng | Tiếng Việt, có dấu/không dấu | High | US-301 |
| NFR-004 / NFR-008 / NFR-010 | Bảo mật | Cô lập workspace; log không chứa nội dung; băm mật khẩu, cookie, CSRF, khóa sai | High | — |
| NFR-005 / NFR-006 / NFR-007 | Tin cậy | Health; sao lưu/khôi phục; lưu nhật ký ≥ 90 ngày | Medium | — |
| NFR-009 | Tiếp cận | WCAG 2.1 AA | Medium | — |
| BRU-001..004 | Quy tắc nghiệp vụ | Chỉ PDF; giới hạn; không trích dẫn giả; tài liệu đã xóa không dùng lại | High | — |

### A.3 Thành phần thiết kế cần kiểm thử (SAD / IEEE 1016)
| View | Phần tử | Loại | Interface | Trạng thái | Kiểm thử bằng |
|---|---|---|---|---|---|
| Composition | `app/backend/cwd/*` (CMP-02..13), `app/frontend/src` (CMP-01) | Module | Python / Vue | — | Unit + component |
| Component & Connector | Retriever, AnswerGenerator, Chat Service | Service | `Retriever`, `AnswerGenerator` Protocol | — | Unit + API |
| Interaction | Hỏi đáp (SAD §6.1), Đăng nhập, Tải lên (§6.2) | Sequence / activity | REST | — | API + E2E |
| Information | users, sessions, documents, chunks(+FTS), conversations, turns, feedback, audit_log | SQLite schema v2 | SQL | — | API + migration test |
| Interface | 15 endpoint REST | REST + problem+json | openapi.yaml | — | Contract (cross-view audit, `check:api`) + API |
| State dynamics | Tài liệu: processing → ready / no_text / failed; ô hỏi (blueprint §3.7) | State machine | — | 4 + 8 trạng thái | API + component + E2E |

### A.4 Thành phần UI/UX
| Màn hình | Thành phần | Tương tác | Trạng thái | Tiếp cận | Luồng |
|---|---|---|---|---|---|
| SCR-01 Đăng nhập | LoginView | Nhập, Enter, submit | lỗi, bận | label, `role=alert` | → SCR-02 |
| SCR-02 Workspace | DocumentPanel, ChatPanel, AnswerMessage | Tải lên/kéo-thả, chọn phạm vi, hỏi (Enter / Shift+Enter), đánh giá | trống, đang xử lý, sẵn sàng, lỗi, đang trả lời, gửi lại | `aria-live`, `aria-pressed`, icon + chữ | → SCR-03/04/05 |
| SCR-03 Panel nguồn | CitationDrawer | Mở từ `[n]`, Esc đóng | đang tải, lỗi, tài liệu đã xóa | `role=dialog`, trả focus | ↔ SCR-02 |
| SCR-04 Xác nhận xóa | ConfirmDialog | Xóa / Hủy / Esc | — | `<dialog>` modal, bẫy focus | ↔ SCR-02 |
| SCR-05 Số liệu | UsageDashboard | Xem | đang tải, lỗi quyền | `<caption>`, `scope=col` | ↔ SCR-02 |
| SCR-06 Phiên hết hạn | LoginView (banner) | Đăng nhập lại | giữ câu hỏi đang soạn | `role=status` | → SCR-02 |

### A.5 Thành phần API
| Endpoint | Method | Request | Response | Lỗi | Auth |
|---|---|---|---|---|---|
| /api/health, /api/config | GET | — | status / PublicConfig | — | Không |
| /api/auth/login | POST | username, password | Me + cookie | 401, 422, 429 | Không |
| /api/auth/logout, /api/auth/me | POST / GET | — | 204 / Me | 401, 403 | Có |
| /api/documents | GET / POST | multipart `files` (≤ 10) | Document[] / UploadResult[] | 401, 403, 413 | Có |
| /api/documents/{id} | GET / DELETE | — | Document / 204 | 404 | Có |
| /api/chunks/{id} | GET | — | đoạn gốc | 404 | Có |
| /api/conversations, /{id} | POST / GET | — | Conversation | 404 | Có |
| /api/conversations/{id}/questions | POST | question, document_ids? | Turn | 409, 422, 503 | Có |
| /api/turns/{id}/feedback | PUT | rating, reason? | feedback | 404, 422 | Có |
| /api/metrics/weekly | GET | weeks | WeeklyMetric[] | 403 | Có (manager) |

### A.6 User story và tiêu chí chấp nhận
19 story trong phạm vi (US-101..103, US-201..205, US-301..306, US-401..403, US-501..502), mỗi story có AC Given/When/Then trong [USER_STORIES.md](../03-analysis/USER_STORIES.md). US-404, US-601 hoãn (P2). Ánh xạ AC ↔ test tự động (backend, frontend, E2E) được sinh ra tự động ở [traceability.md](../03-analysis/traceability.md).

### A.7 Đánh giá rủi ro (định hướng mức đầu tư kiểm thử)
| ID | Rủi ro | Khả năng (1–5) | Tác động (1–5) | Điểm | Giảm thiểu bằng kiểm thử |
|---|---|---|---|---|---|
| RISK-01 | Rò dữ liệu giữa người dùng / truy cập không đăng nhập | 2 | 5 | 10 | Test 401 sinh từ registry cho mọi endpoint; cô lập mọi tài nguyên (API + E2E) |
| RISK-02 | AI trả lời sai hoặc bịa nguồn | 3 | 5 | 15 | Eval bộ câu hỏi chuẩn; trích dẫn kiểm tra với CSDL; not_found; injection |
| RISK-03 | Lỗi đồng thời / thứ tự request (commit, race) | 3 | 4 | 12 | Test đa luồng; **Playwright với trình duyệt thật** (đã bắt được E2E-2) |
| RISK-04 | Dữ liệu gửi ra ngoài khi chưa được phép | 2 | 5 | 10 | Test chọn bộ sinh theo cờ + key; client giả cho LLM |
| RISK-05 | Truy xuất bỏ sót từ đồng nghĩa | 4 | 3 | 12 | Tập diễn đạt khác (báo cáo, không chặn); chạy lại với bộ thật DEP-002 |
| RISK-06 | Hiệu năng ở quy mô tối đa | 2 | 3 | 6 | Test truy xuất với 20 000 chunk người khác; benchmark 450 000 chunk |
| RISK-07 | Mất dữ liệu khi khôi phục | 2 | 4 | 8 | Test backup/restore, backup hỏng, restore khi đang chạy, migration |
| RISK-08 | Lệch hợp đồng API giữa backend và frontend | 3 | 3 | 9 | Cross-view audit + `check:api` trong CI |

---

## Phần B — Master Test Plan theo IEEE 829

## 1.0 Test Plan Identifier
| Thuộc tính | Giá trị |
|---|---|
| Document ID | CWD-MTP-v2.0 |
| Phiên bản | 2.0 (thay TP-CWD-001 v1.0; viết lại theo testPlan_prompt) |
| Ngày ban hành | 2026-10-28 |
| Trạng thái | Review |
| Phân loại | Nội bộ |
| Người soạn | Agent (Claude) |
| Người phê duyệt | QA Lead (STK-006), PO (STK-001) — chưa ký |

## 2.0 Introduction
### 2.1 Purpose
Xác định chiến lược kiểm thử cho MVP "Chat với tài liệu": các mức và loại kiểm thử, vai trò, tiêu chí vào/ra, công cụ và môi trường, cùng khả năng truy vết từ yêu cầu tới test case.

### 2.2 Scope
**Trong phạm vi:** kiểm thử chức năng toàn bộ story P0 + P1; API và hợp đồng API; UI/UX và E2E hành trình người dùng; bảo mật ở mức ứng dụng; hiệu năng ở quy mô thiết kế (ASM-003); tiếp cận (một phần, tự động); chất lượng câu trả lời AI; hồi quy; sao lưu/khôi phục.
**Ngoài phạm vi:** xem mục 5.0.

### 2.3 Objectives
| ID | Mục tiêu | Tiêu chí thành công | Truy vết |
|---|---|---|---|
| OBJ-001 | Xác nhận yêu cầu chức năng | 100% FR có ≥ 1 test tự động đạt | FR-001..FR-019 |
| OBJ-002 | Xác nhận hợp đồng API | 15/15 endpoint có test; route = hợp đồng; type frontend khớp | openapi.yaml |
| OBJ-003 | Xác nhận UI theo thiết kế | SCR-01..06 có test component + E2E | UX-001..011 |
| OBJ-004 | Tiếp cận | Bàn phím, focus, aria, trạng thái icon + chữ có test; inspection WCAG 2.1 AA | NFR-009 |
| OBJ-005 | Hiệu năng | Hỏi đáp cục bộ P90 ≤ 2 s / 50 tài liệu; truy xuất < 0,5 s khi có 20 000 chunk người khác | NFR-001 |
| OBJ-006 | Bảo mật | 0 lỗ hổng đã biết mức cao trong phụ thuộc; 0 rò rỉ trong test cô lập | NFR-004/008/010 |
| OBJ-007 | Chất lượng AI | Đúng ≥ 85%, trích dẫn ≥ 90%, not_found ≥ 9/10 | NFR-002 |

### 2.4 References
| Tài liệu | Phiên bản |
|---|---|
| BRD, PRD, USER_STORIES | 0.2 |
| SAD (arc42), Blueprint (IEEE 1016), ADR-001..009 | 0.4 / 0.2 |
| app/api-contract/openapi.yaml | 0.2 |
| PLAN.md | T-01..T-10 |
| IEEE 829-2008, ISO/IEC/IEEE 29119 | — |

## 3.0 Test Items
### 3.1 Software items
| ID | Hạng mục | Phiên bản | Công nghệ |
|---|---|---|---|
| SI-001 | Backend `app/backend/cwd` (CMP-02..13) | HEAD nhánh `feat/chat-with-docs-sdlc` | Python ≥ 3.12, FastAPI |
| SI-002 | REST API (15 endpoint) | openapi 0.2 | REST + problem+json |
| SI-003 | Web app `app/frontend` (CMP-01) | HEAD | Vue 3.5 + TypeScript 5.9 + Vite 8 |
| SI-004 | Database schema `cwd/schema.sql` | user_version 2 | SQLite 3 + FTS5 |
| SI-005 | Cấu hình `CWD_*` | SAD §8.5 | Biến môi trường |
| SI-006 | CLI quản trị `cwd/cli.py` | HEAD | Python |

### 3.2 Test artifacts
| ID | Artifact | Định dạng | Vị trí |
|---|---|---|---|
| TA-001 | Test backend (unit, API, bảo mật, eval) | pytest | `app/backend/tests/` |
| TA-002 | Test frontend (unit, component) | Vitest + Vue Test Utils | `app/frontend/src/**/*.spec.ts` |
| TA-003 | Test E2E | Playwright | `app/e2e/tests/*.spec.ts` |
| TA-004 | Dữ liệu test | PDF sinh bằng fpdf2 từ corpus tổng hợp; bộ câu hỏi chuẩn | `tests/corpus.py`, `tests/eval/gold.py`, `app/e2e/serve.py` |
| TA-005 | Mock / giả lập | Client Anthropic giả, generator giả, mock API (Vitest) | trong các file test |
| TA-006 | Môi trường | SQLite tạm mỗi test; backend thật cho E2E | `tmp_path`, `app/e2e/.data/` |

## 4.0 Features to be Tested
### 4.1 Test priority matrix
| Ưu tiên | Tính năng | Story | Yêu cầu | Rủi ro |
|---|---|---|---|---|
| High | F-01 Xác thực, phiên, CSRF | US-101 | FR-001/002, NFR-010 | RISK-01 |
| High | F-02 Cô lập dữ liệu, kiểm toán, log sạch | US-103 | NFR-004/008, FR-019 | RISK-01 |
| High | F-04 Hỏi đáp có trích dẫn, grounding | US-301..305 | FR-009..013 | RISK-02 |
| High | F-03 Tải lên và xử lý tài liệu | US-201..204 | FR-004..007 | RISK-03 |
| High | F-08 Chính sách dữ liệu AI | US-102 | FR-003 | RISK-04 |
| Medium | F-05 Hội thoại: hỏi tiếp, phạm vi, lịch sử | US-401..403 | FR-014..016 | RISK-05 |
| Medium | F-06 Xóa tài liệu | US-205 | FR-008 | RISK-03 |
| Medium | F-09 Sao lưu, khôi phục, migration | — | NFR-006/007 | RISK-07 |
| Medium | F-10 Chất lượng & hiệu năng AI | US-306 | NFR-001/002 | RISK-02, RISK-06 |
| Low | F-07 Đánh giá & số liệu | US-501/502 | FR-017/018 | — |

### 4.2 Feature test matrix
| Tính năng | Unit | Integration (API) | System (E2E) | Acceptance | Regression | Performance | Security | Accessibility |
|---|---|---|---|---|---|---|---|---|
| F-01 | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| F-02 | – | ✓ | ✓ | ✓ | ✓ | – | ✓ | – |
| F-03 | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| F-04 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F-05 | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | ✓ |
| F-06 | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| F-07 | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| F-08 | ✓ | ✓ | – | ✓ (review IT) | ✓ | – | ✓ | – |
| F-09 | – | ✓ | – | – | ✓ | – | – | – |
| F-10 | ✓ | ✓ | – | ✓ | ✓ | ✓ | – | – |

### 4.3 Detailed feature description
| ID | Tính năng | Mô tả | Phần kiểm thử | AC |
|---|---|---|---|---|
| F-01 | Xác thực | Đăng nhập/đăng xuất, phiên máy chủ, CSRF, khóa 5 lần sai | Login, logout, me, CSRF, lockout, hết hạn | AC-101.1..6, AC-NFR-010 |
| F-02 | Cô lập & kiểm toán | Tài nguyên người khác → 404; audit; log không nội dung | Mọi endpoint, audit_log, log | AC-103.1..3, AC-NFR-004, AC-NFR-008 |
| F-03 | Tài liệu | Tải lên ≤ 10 file/lần, kiểm tra chữ ký/dung lượng/giới hạn, xử lý nền | Upload, validate, trạng thái, danh sách | AC-201.1..3, AC-202.1..4, AC-203.1..5, AC-204.1..2 |
| F-04 | Hỏi đáp | Truy xuất FTS5 tiếng Việt, bộ sinh cục bộ, kiểm tra trích dẫn | Hỏi, đa tài liệu, mâu thuẫn, not_found, injection, panel nguồn | AC-301.1..5, AC-302..305 |
| F-05 | Hội thoại | Ngữ cảnh 3 lượt + tài liệu trích dẫn trước, phạm vi, lịch sử | Hỏi tiếp, phạm vi, 5 lượt, hội thoại mới | AC-401.1, AC-402.1..2, AC-403.1..2 |
| F-06 | Xóa | Cascade chunk + FTS + file; trích dẫn cũ "đã xóa" | Xóa, không dùng lại, id không tái sử dụng | AC-205.1..4 |
| F-07 | Đánh giá & số liệu | Upsert đánh giá; số liệu tuần ISO cho manager | Feedback, weekly, 403 | AC-501.1..2, AC-502.1..2 |
| F-08 | Chính sách AI | Bộ sinh ngoài chỉ khi cờ + key; lỗi → 503 | Chọn bộ sinh, lỗi, escape prompt | AC-102.1..2 |
| F-09 | Vận hành dữ liệu | Backup/restore an toàn, migration schema, dọn nhật ký | Khứ hồi, backup hỏng, đang chạy, schema cũ | NFR-006/007 |
| F-10 | Chất lượng AI | Bộ câu hỏi chuẩn 32 câu / 50 tài liệu | Độ đúng, trích dẫn, not_found, P90 | AC-306.1..2 |

## 5.0 Features Not to be Tested
| ID | Tính năng | Lý do | Rủi ro | Kế hoạch |
|---|---|---|---|---|
| F-11 | Lịch sử các phiên trước (US-404), tóm tắt (US-601) | Hoãn P2 | Thấp | Kiểm thử khi đưa vào phạm vi |
| F-12 | Anthropic API thật | Chặn bởi OQ-006, không có key | Trung bình | Chỉ test bằng client giả; đo thật khi IT cho phép |
| F-13 | Độ chính xác trên dữ liệu thật | Chờ bộ câu hỏi DEP-002 | Cao | Chạy lại `tests/eval` với bộ thật trước khi dùng |
| F-14 | Tải lớn, khả dụng 99%, RTO 4 h thực tế | Cần môi trường prod (DEP-003) | Trung bình | Test tải + diễn tập khi có môi trường |
| F-15 | Pentest, quét DAST | Thuộc IT/Bảo mật (L3) | Trung bình | review-record §6 |
| F-16 | Trình duyệt ngoài Chrome, mobile | Mobile ngoài phạm vi MVP; chỉ có Chrome trên máy test | Thấp | Thêm project Firefox/WebKit cho Playwright khi cần |
| F-17 | Release / vận hành / ngừng (Phase 9–11) | Ngoài phạm vi dự án (PD-07) | — | — |

## 6.0 Approach
### 6.1 Test levels and types

#### 6.1.1 Unit testing
| Thuộc tính | Mô tả |
|---|---|
| Đội | Dev (Agent) |
| Công cụ | pytest (backend), Vitest (frontend) |
| Mục tiêu coverage | ≥ 70% mỗi phía (hiện tại: backend 97,7%, frontend lines 91,8%) |
| Entry | Code biên dịch được, ruff/ESLint/vue-tsc sạch |
| Exit | Mọi unit test đạt, coverage ≥ 70% |
| Trọng tâm | `textnorm`, `chunk_page`, `security`, bộ sinh, `splitAnswer`, `composerState`, API client |
| Mock | Client Anthropic giả; `api` của frontend được mock |

#### 6.1.2 Integration testing (API qua toàn stack)
| Thuộc tính | Mô tả |
|---|---|
| Công cụ | pytest + FastAPI `TestClient` + SQLite tạm + PDF sinh tự động |
| Phạm vi | 15 endpoint, CSDL, ingestion nền, CLI |
| Entry | Unit đạt |
| Exit | Mọi integration test đạt |

| Test case | Endpoint | Loại | Kiểm tra | Test tự động |
|---|---|---|---|---|
| INT-API-001 | POST /api/auth/login | Dương | 200, cookie HttpOnly + SameSite=Strict | `test_login_success_returns_user_and_sets_secure_cookie` |
| INT-API-002 | POST /api/auth/login | Âm | 401 thông báo chung; 429 sau 5 lần sai | `test_wrong_password_and_unknown_user_get_same_message`, `test_lockout_after_five_failures` |
| INT-API-003 | POST /api/documents | Dương | 3 PDF → 3 tài liệu | `test_upload_three_pdfs` |
| INT-API-004 | POST /api/documents | Âm | `file.wrong_type`, `file.too_large`, `docs.limit_reached`, 413 | `test_one_bad_file_does_not_block_others`, `test_too_large_file_rejected_with_limit`, `test_document_limit`, `test_cr04_oversized_body_rejected_with_413` |
| INT-API-005 | POST /api/documents | Đồng thời | 6 upload song song không vượt giới hạn | `test_nr01_parallel_uploads_respect_document_limit` |
| INT-API-006 | GET /api/documents/{id} | Âm | 404 khi không tồn tại / của người khác | `test_get_unknown_document_404`, `test_workspace_isolation_on_every_resource` |
| INT-API-007 | POST …/questions | Dương | Câu trả lời + trích dẫn tên/trang từ CSDL | `test_answer_with_citation`, `test_multi_document_answer_cites_both` |
| INT-API-008 | POST …/questions | Âm | 422, 409, 503, not_found | `test_empty_question_rejected`, `test_no_ready_documents`, `test_ai_failure_returns_503`, `test_general_knowledge_question_not_found` |
| INT-API-009 | DELETE /api/documents/{id} | Dương | 204, cascade, không dùng lại | `test_delete_removes_document`, `test_deleted_document_is_never_used_again` |
| INT-API-010 | PUT /api/turns/{id}/feedback | Dương / Âm | upsert; 422; 404 | `test_feedback_is_saved_and_can_change`, `test_feedback_validation`, `test_feedback_on_someone_elses_turn_404` |
| INT-API-011 | GET /api/metrics/weekly | Dương / Âm | Đúng số liệu; 403 user thường | `test_weekly_metrics`, `test_metrics_forbidden_for_regular_user` |
| INT-API-012 | Mọi endpoint bảo vệ | Âm | 401 khi không có phiên (sinh từ registry) | `test_every_protected_endpoint_requires_login` (12 case) |

#### 6.1.3 System testing (E2E — Playwright)
| Thuộc tính | Mô tả |
|---|---|
| Công cụ | Playwright 1.64, Chromium (Google Chrome trên máy dev), 1280×800, vi-VN |
| Phạm vi | Hành trình người dùng qua trình duyệt thật + backend thật + bản build Vue |
| Entry | Integration đạt, `npm run build` thành công |
| Exit | 20/20 đạt, 0 flaky |
| Bằng chứng | Mỗi test một thư mục trong `test_reports/` (ảnh chụp, video mp4, report.md, result.json) |

| Test case | Hành trình | Các bước chính | Kết quả mong đợi | Spec |
|---|---|---|---|---|
| E2E-001 | Đăng nhập → workspace → đăng xuất | Nhập tên + mật khẩu, Đăng nhập, Đăng xuất, tải lại | Vào SCR-02, thấy "Xử lý cục bộ"; sau đăng xuất về SCR-01 | auth.spec.ts |
| E2E-002 | Sai mật khẩu | Nhập sai | Thông báo chung | auth.spec.ts |
| E2E-003 | Phiên hết hạn | Đăng nhập, tải PDF, xóa cookie, hỏi | Banner hết hạn; đăng nhập lại còn câu hỏi | auth.spec.ts |
| E2E-004 | Tải song song + file sai | Chọn 2 PDF + 1 .docx | 2 tài liệu "Sẵn sàng" không tải lại trang; .docx báo lỗi | documents.spec.ts |
| E2E-005 | Xóa có xác nhận | Xóa → Hủy → Xóa → Xóa | Hủy giữ nguyên; xóa thật giảm danh sách | documents.spec.ts |
| E2E-006 | Hỏi đáp + panel nguồn | Hỏi, bấm [1], Esc | Đoạn gốc + trang; Esc đóng, focus trở về | chat.spec.ts |
| E2E-007 | Không dấu / ngoài tài liệu / hỏi tiếp / phạm vi / lịch sử / đánh giá | Theo AC tương ứng | Như AC | chat.spec.ts |
| E2E-008 | Cô lập + dashboard | A tải tài liệu; B hỏi; manager xem số liệu | B không thấy tài liệu của A; manager thấy số liệu tuần; user thường 403 | access.spec.ts |

#### 6.1.4 Acceptance testing
| Thuộc tính | Mô tả |
|---|---|
| Đội | PO, đội kinh doanh (UAT), QA |
| Công cụ | Video và report từng test trong `test_reports/` làm kịch bản demo; UAT thủ công trên môi trường test |
| Entry | System test đạt |
| Exit | Mọi AC P0 đạt, biên bản UAT ký |

| Test case | Story | Kịch bản | AC | Kết quả tự động |
|---|---|---|---|---|
| UAT-001 | US-101 | Đăng nhập bằng tài khoản được cấp | AC-101.1..6 | Đạt (API + E2E) |
| UAT-002 | US-201..204 | Tải bộ tài liệu dự án, theo dõi trạng thái | AC-201..204 | Đạt |
| UAT-003 | US-301..305 | Hỏi các câu nghiệp vụ, kiểm chứng nguồn | AC-301..305 | Đạt (bộ tổng hợp) — **cần chạy với câu hỏi thật** |
| UAT-004 | US-401..403 | Hỏi tiếp, giới hạn phạm vi | AC-401..403 | Đạt |
| UAT-005 | US-205 | Xóa tài liệu sai | AC-205.1..4 | Đạt |
| UAT-006 | US-502 | Quản lý xem số liệu tuần | AC-502.1..2 | Đạt |

#### 6.1.5 Regression testing
| Thuộc tính | Mô tả |
|---|---|
| Công cụ | Cổng L0 `tools/ci_local.py` (= GitHub Actions) |
| Kích hoạt | Mỗi commit / PR |
| Tần suất | Mỗi build |

| Suite | Phạm vi | Số test | Thời gian | Tự động |
|---|---|---|---|---|
| REG-001 | Backend unit + API + bảo mật + eval | 138 | ~80 s | ✓ |
| REG-002 | Frontend unit + component | 49 | ~35 s | ✓ |
| REG-003 | E2E Playwright | 20 | ~60–80 s | ✓ |
| REG-004 | Hợp đồng & thiết kế: cross-view audit, `check:api`, truy vết | 3 bước | ~15 s | ✓ |
| REG-005 | Static: ruff, ESLint, vue-tsc, tsc E2E, quét secret, pip-audit, npm audit | 8 bước | ~60 s | ✓ |

#### 6.1.6 Performance testing
| Thuộc tính | Mô tả |
|---|---|
| Công cụ | pytest (đo thời gian), script benchmark |
| Loại | Đo độ trễ, quy mô dữ liệu; **không** test tải nhiều người dùng (mục 5.0) |

| Kịch bản | Loại | Quy mô | Mục tiêu | Kết quả gần nhất |
|---|---|---|---|---|
| PERF-001 | Độ trễ hỏi đáp | 32 câu / 50 tài liệu | P90 ≤ 2 s | 47 ms (`test_quality_and_latency`) |
| PERF-002 | Truy xuất khi có dữ liệu người khác | 20 000 chunk | < 0,5 s | Đạt (`test_cr09_retrieval_ignores_other_workspaces_at_scale`) |
| PERF-003 | Benchmark quy mô thiết kế | 450 000 chunk / 30 người | Câu ngắn và dài < 1 s | 0,23–0,47 s / 0,07–0,09 s (benchmark CR-09) |
| PERF-004 | Không chặn khi sinh câu trả lời chậm | Generator giả 1,5 s | Request khác < 1 s | Đạt (`test_cr01_slow_answer_does_not_block_other_users`) |

#### 6.1.7 Security testing
| Thuộc tính | Mô tả |
|---|---|
| Công cụ | pytest, Playwright, quét secret, pip-audit, npm audit; L3 inspection bởi IT |
| Exit | 0 lỗ hổng phụ thuộc mức cao; mọi test bảo mật đạt; L3 ký |

| Test case | Hạng mục | Mô tả | Test tự động |
|---|---|---|---|
| SEC-001 | Xác thực | Băm PBKDF2, token lưu băm, hết hạn, khóa sai, thông báo chung | `test_password_hashing`, `test_session_token_is_stored_hashed`, `test_idle_session_expires`, `test_lockout_after_five_failures` |
| SEC-002 | Phân quyền | 401 mọi endpoint; 404 tài nguyên người khác; 403 dashboard | `test_every_protected_endpoint_requires_login`, `test_workspace_isolation_on_every_resource`, E2E access.spec |
| SEC-003 | Injection | Prompt injection qua PDF và tên file; FTS chỉ nhận token; không `v-html` (ESLint) | `test_prompt_injection_text_is_not_obeyed`, `test_document_text_cannot_forge_tags`, `test_cr07_file_name_cannot_forge_document_tag` |
| SEC-004 | CSRF | Thiếu/sai/non-ASCII header → 403 | `test_write_without_csrf_is_forbidden`, `test_cr05_non_ascii_csrf_header_is_403`, `client.spec.ts` |
| SEC-005 | Bảo vệ dữ liệu | Log không chứa nội dung; không gọi AI ngoài mặc định | `test_logs_never_contain_content`, `test_build_generator_needs_flag_and_key` |
| SEC-006 | Header bảo mật | CSP, X-Frame-Options, nosniff, Referrer-Policy (kể cả 500, 413) | `test_security_headers`, `test_cr06_unhandled_error_keeps_security_headers` |
| SEC-007 | Từ chối dịch vụ | 413 body quá lớn; tối đa 10 file | `test_cr04_oversized_body_rejected_with_413` |

#### 6.1.8 Accessibility testing
| Thuộc tính | Mô tả |
|---|---|
| Chuẩn | WCAG 2.1 AA |
| Công cụ | Playwright (truy vấn theo role/label, bàn phím), Vitest; inspection thủ công |

| Test case | Kiểm tra | Mô tả | Bằng chứng |
|---|---|---|---|
| ACC-001 | Bàn phím | Enter gửi, Shift+Enter xuống dòng, Esc đóng panel/hộp thoại | E2E chat.spec (Enter, Esc), `components.spec.ts` |
| ACC-002 | Trình đọc màn hình | `aria-live` cho câu trả lời và thông báo | Kiểm tra mã + component test; **thủ công với NVDA chưa làm** |
| ACC-003 | Độ tương phản | Token màu ≥ 4,5:1 | UI_UX_design README (tính toán); kiểm thủ công |
| ACC-004 | ARIA | Nhãn nút biểu tượng, `aria-pressed`, `role=dialog`, `<caption>` | Mọi E2E truy vấn theo role/label |
| ACC-005 | Quản lý focus | Panel nguồn trả focus; hộp thoại modal; giữ focus khi poll | E2E AC-305.2, `review-fixes.spec.ts` |
| ACC-006 | Thông báo lỗi | Lỗi đăng nhập/upload hiển thị bằng chữ, `role=alert` | E2E AC-101.3, AC-202.1 |

#### 6.1.9 UI/UX testing
| Test case | Kiểm tra | Mô tả | Bằng chứng |
|---|---|---|---|
| UI-001 | So khớp thiết kế | So với prototype SCR-01..06 | Ảnh chụp từng test trong `test_reports/` (review thủ công) |
| UI-002 | Độ rộng | 1280 px không cuộn ngang | E2E viewport 1280×800 |
| UI-003 | Trạng thái thành phần | Trống / đang xử lý / sẵn sàng / lỗi / đang trả lời / disabled | `utils.spec.ts` (composerState), E2E AC-204.2 |
| UI-004 | Tương tác | Kéo-thả, chọn phạm vi, đánh giá | E2E + component |
| UI-005 | Lỗi và trạng thái trống | Upload lỗi, not_found, gửi lại | `components.spec.ts`, E2E |
| UI-006 | Đang tải | Tiến độ upload, "Đang trả lời…" | `client.spec.ts`, `composables.spec.ts` |
| UI-007 | Thông báo | Banner hết hạn, cảnh báo docs_processing | E2E EC-15, `components.spec.ts` |
| UI-008 | Điều hướng | Workspace ↔ dashboard, về màn hình chính | E2E AC-502.1 |

#### 6.1.10 API testing
| Test case | Endpoint | Method | Loại | Kiểm tra | Trạng thái |
|---|---|---|---|---|---|
| API-001 | /api/auth/login | POST | Chức năng | Me + cookie | ✓ |
| API-002 | /api/auth/login | POST | Âm | 401 / 422 / 429 | ✓ |
| API-003 | /api/documents | POST | Chức năng | UploadResult từng file | ✓ |
| API-004 | /api/documents | POST | Đồng thời | Giới hạn khi song song | ✓ |
| API-005 | /api/conversations/{id}/questions | POST | Chức năng | Turn + citations | ✓ |
| API-006 | /api/conversations/{id}/questions | POST | Hiệu năng | P90 | ✓ |
| API-007 | /api/documents/{id} | GET / DELETE | Âm | 404 | ✓ |
| API-008 | /api/chunks/{id} | GET | Chức năng | Đoạn gốc; 404 sau xóa | ✓ |
| API-009 | /api/metrics/weekly | GET | Chức năng / quyền | Số liệu; 403 | ✓ |
| API-010 | Toàn bộ | — | Hợp đồng | Route = openapi; enum lỗi = code; type frontend khớp | ✓ |

### 6.2 Test execution strategy
1. **Thứ tự mỗi build** (cổng L0, dừng merge nếu bất kỳ bước nào lỗi): static → hợp đồng/thiết kế → backend → frontend → build → E2E → sinh `test_reports/`.
2. **TDD:** mỗi task viết test cho AC trước code. ID AC ghi trong tên/docstring test để `tools/trace_matrix.py` truy vết tự động.
3. **Dữ liệu sạch:** mỗi test backend dùng CSDL tạm; mỗi lần chạy E2E dựng CSDL và user mới; mỗi spec E2E dùng tài khoản riêng.
4. **Lỗi đồng thời/thứ tự** không lộ qua `TestClient`, nên mọi thay đổi ở auth, upload, transaction **bắt buộc** chạy Playwright.
5. **Quản lý defect:** mỗi defect có ID (DF/CR/NR/E2E-x), mức độ, test hồi quy. Test hồi quy phải được chứng minh **thất bại khi gỡ bản sửa**. Ghi nhận trong test-report §5 và review-record §3.

## 7.0 Item Pass/Fail Criteria
| Mức | Pass khi |
|---|---|
| Test case | Mọi assertion đạt |
| Build | 100% test đạt; coverage ≥ 70% mỗi phía; lint/type-check sạch; 0 secret; 0 lỗ hổng phụ thuộc mức cao; cross-view audit 0 FAIL; `check:api` đạt; mọi hàng truy vết có test; E2E 20/20, 0 flaky |
| Chất lượng AI | Đúng ≥ 85%, trích dẫn ≥ 90%, not_found ≥ 9/10, P90 ≤ 2 s (cục bộ) |
| Phát hành | Thêm: eval trên bộ thật (DEP-002), UAT ký, L2 rubric ≥ 10/14, L3 ký |

## 8.0 Suspension Criteria and Resumption Requirements
| Tạm dừng khi | Tiếp tục khi |
|---|---|
| Cổng L0 không chạy được do môi trường (thiếu Node/Python/Chrome) | Môi trường sửa xong, chạy lại toàn bộ cổng |
| Phát hiện defect Blocker hoặc lỗ hổng bảo mật | Đã sửa + test hồi quy + chạy lại toàn bộ cổng |
| > 20% E2E lỗi hoặc flaky | Tìm nguyên nhân gốc (test hay sản phẩm), sửa, chạy lại 2 lần liên tiếp đạt |

## 9.0 Test Deliverables
| Deliverable | Vị trí |
|---|---|
| Master Test Plan (tài liệu này) | `docs/07-verification/test-plan.md` |
| Test Summary Report | [test-report.md](test-report.md) |
| Bằng chứng E2E: mỗi test một thư mục (ảnh, video mp4, report.md, result.json) | [test_reports/](../../test_reports/report.md) |
| CI log | [ci-log.txt](ci-log.txt) |
| Kết quả eval chất lượng AI | [eval-report.json](eval-report.json) |
| Coverage | Artifact CI (`app/backend/coverage.xml`, `app/frontend/coverage/`); số liệu trong test-report |
| Truy vết yêu cầu ↔ test | [traceability.md](../03-analysis/traceability.md) |
| Review record (L1 vòng 1, 2; L2/L3) | [code-review-L1.md](code-review-L1.md) · [code-review-L1-round2.md](code-review-L1-round2.md) · [review-record.md](review-record.md) |

## 10.0 Testing Tasks
| Task | Đầu vào | Đầu ra | Phụ thuộc |
|---|---|---|---|
| Viết test theo AC (TDD) | USER_STORIES, PRD §3.9 | Test backend/frontend/E2E | — |
| Chuẩn bị dữ liệu test | corpus, gold set | PDF sinh, user E2E | — |
| Chạy cổng L0 | Code | ci-log, coverage | Test |
| Chạy eval | Bộ câu hỏi | eval-report.json | Backend |
| Chạy E2E + sinh báo cáo | Bản build | `test_reports/` | Build |
| L1 agent review | Diff | code-review-L1*.md | Cổng L0 xanh |
| Lập test report | Tất cả trên | test-report.md | Tất cả trên |
| UAT, L2, L3 | Báo cáo, video | Biên bản, rubric | Test report |

## 11.0 Environmental Needs
| Hạng mục | Yêu cầu |
|---|---|
| OS | Windows 10/11 (dev), Ubuntu (CI) |
| Runtime | Python ≥ 3.12 (dev 3.15.2), Node ≥ 22.12 (dev 22.23.4) |
| Trình duyệt | Google Chrome (dev); Chromium + ffmpeg của Playwright (CI) |
| Font | Unicode TTF (Arial hoặc DejaVu) để sinh PDF tiếng Việt |
| Công cụ | ffmpeg trong `imageio-ffmpeg` để chuyển video sang mp4 |
| Mạng | Không cần khi chạy test (trừ cài đặt và audit phụ thuộc) |
| Dữ liệu | Tạo tự động; không dùng dữ liệu kinh doanh thật trong CI |

## 12.0 Responsibilities
| Vai trò | Trách nhiệm |
|---|---|
| Agent (Dev + QA tự động) | Viết và chạy test tự động, sinh báo cáo, L1 tự kiểm |
| Reviewer agent độc lập | L1 review theo IEEE 1028 |
| QA Lead (STK-006) | Duyệt test plan, test report; điều phối UAT |
| Đội kinh doanh (STK-002) | Bộ câu hỏi chuẩn thật (DEP-002); UAT |
| Tech Lead (STK-004) | L2 review, rubric |
| IT/Bảo mật (STK-005) | L3 inspection, ký AC-102.3, pentest |
| PO (STK-001) | Phê duyệt phạm vi kiểm thử và kết quả UAT |

## 13.0 Staffing and Training Needs
| Đối tượng | Nhu cầu |
|---|---|
| QA | Chạy `python tools/ci_local.py`; đọc `test_reports/` và `eval-report.json` (30 phút hướng dẫn) |
| Đội kinh doanh | Cách soạn bộ câu hỏi chuẩn (câu hỏi, đáp án, tài liệu + trang) |
| Reviewer L2/L3 | Đọc review-record §5–6; chạy Playwright và xem video |

## 14.0 Schedule
| Mốc | Nội dung | Trạng thái |
|---|---|---|
| S1 (T-01..T-03) | Test nền tảng, auth, tài liệu | Hoàn tất |
| S2 (T-04..T-05) | Test hỏi đáp, hội thoại | Hoàn tất |
| S3 (T-06..T-10) | Số liệu, AI ngoài, eval, ops, Vue, E2E | Hoàn tất |
| Verify | L1 vòng 1–2, sửa, E2E, test report | Hoàn tất (2026-10-28) |
| UAT + L2/L3 | Con người | Chưa lên lịch (phụ thuộc OQ-009) |

## 15.0 Risks and Contingencies
| Rủi ro | Ảnh hưởng | Dự phòng |
|---|---|---|
| Bộ eval do agent soạn, thiên lệch | Độ chính xác báo cáo lạc quan | Chạy lại với DEP-002; báo cáo riêng tập diễn đạt khác (12,5%) |
| Không test được LLM thật | Chế độ external chưa được đo | Client giả + cờ tắt mặc định; đo khi IT cho phép |
| E2E chập chờn do thời gian | Báo đỏ giả, mất niềm tin vào CI | Một worker, dữ liệu riêng mỗi spec, helper chờ câu trả lời hoàn tất; retry 1 lần trên CI |
| Thiếu môi trường prod | Không đo tải, khả dụng | Ghi ở mục 5.0; làm khi có DEP-003 |
| Thiếu reviewer con người | Không merge được theo luật | review-record chuẩn bị sẵn, PR chia theo task |

## 16.0 Approvals
| Vai trò | Tên | Quyết định | Ngày |
|---|---|---|---|
| QA Lead | | ☐ Approve ☐ Reject | |
| Product Owner | | ☐ Approve ☐ Reject | |
| Tech Lead | | ☐ Approve ☐ Reject | |

---

## Phụ lục A — Thống kê test tự động
| Loại | Vị trí | Số lượng | Kết quả gần nhất |
|---|---|---|---|
| Backend | `app/backend/tests/` (14 file) | 138 test case | Đạt · coverage 97,73% |
| Frontend | `app/frontend/src/**/*.spec.ts` (5 file) | 49 | Đạt · lines 91,8% |
| E2E | `app/e2e/tests/` (4 file) | 20 | Đạt · 0 flaky |
| Eval AI | `app/backend/tests/eval/` | 32 câu + 8 diễn đạt khác | 100% / 12,5% (không chặn) |

## Phụ lục B — Audit theo checklist IEEE 829
Tự kiểm tra của agent (người soạn). QA Lead phải review độc lập.

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Test Plan Identifier | Done | Mục 1.0: CWD-MTP-v2.0, ngày, trạng thái, phân loại |
| 3 | Introduction | Done | Mục 2.0: mục đích, phạm vi, 7 mục tiêu có tiêu chí, tài liệu tham chiếu |
| 4 | Test Items | Done | Mục 3.0: 6 software item có phiên bản, 6 test artifact |
| 5 | Features to be Tested | Done | Mục 4.0: ma trận ưu tiên theo rủi ro, ma trận mức/loại test, mô tả F-01..F-10 |
| 6 | Features Not to be Tested | Done | Mục 5.0: F-11..F-17 kèm lý do, rủi ro, kế hoạch |
| 7 | Testing Approach | Done | Mục 6.1: 10 loại test, mỗi loại có công cụ, entry/exit, test case trỏ tới test có thật |
| 8 | Automation vs Manual | Done | Mục 6.1.5 (tự động trong cổng L0) và 6.1.4/6.1.8 (UAT, NVDA, tương phản: thủ công) |
| 9 | Item Pass/Fail Criteria | Done | Mục 7.0: ngưỡng đo được theo mức |
| 10 | Suspension Criteria | Done | Mục 8.0 |
| 11 | Resumption Requirements | Done | Mục 8.0 |
| 12 | Environmental Needs | Done | Mục 11.0 |
| 13 | Responsibilities | Done | Mục 12.0 |
| 14 | Staffing & Training Needs | Done | Mục 13.0 |
| 15 | Testing Tasks | Done | Mục 10.0 |
| 16 | Test Deliverables | Done | Mục 9.0 |
| 17 | Schedule | In Progress | Mục 14.0: UAT/L2/L3 chưa có ngày (OQ-009) |
| 18 | Risks & Contingencies | Done | Mục 15.0 và Phần A.7 |
| 19 | Approvals | Done | Mục 16.0 (chưa ký) |
