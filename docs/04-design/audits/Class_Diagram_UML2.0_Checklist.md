# Audit — Class Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/class_diagram.drawio (trang "Domain (ENT)" và "Service classes"); đối chiếu blueprint §3.3, SAD §5.3, app/backend/cwd/schema.sql, design-refine-log.md |
| Checklist | docs/checklists/Class_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Vòng 1: Independent reviewer agent · Vòng 2: artifact-auditor (agent) |
| Ngày | Vòng 1: 2026-10-28 · Vòng 2: 2026-11-02 |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d) |
| Ghi chú vòng 2 | class_diagram.drawio không thay đổi nội dung từ b6bf496 tới HEAD (tools/gen_diagrams.py chỉ định dạng lại hàm class_diagram). DF-20 (ngăn operations) ở trạng thái Partial, DF-14 sửa SAD §5.3 nhưng không sửa sơ đồ. |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | Done | Hai trang có tên "Domain (ENT)" và "Service classes", nêu rõ miền được mô hình hóa. Không có khung tiêu đề trong sơ đồ (Minor). |
| 3 | Abstraction Level | In Progress | Vẫn không ghi rõ mức. Trang Domain trộn mức vật lý («table users», -password_hash) với mức logic (+citations: Citation[], +scope: str[] trong khi schema.sql lưu citations_json/scope_json TEXT). Không đổi sau REFINE. |
| 4 | Class Notation | In Progress | Khối swimlane stackLayout chỉ có một danh sách dòng, không có ngăn phân cách thuộc tính/phương thức (Settings, AnthropicGenerator, LoginLimiter trộn cả hai). DF-20 Partial: tách ngăn operations còn hoãn, owner Architect. |
| 5 | Naming Conventions | Done | PascalCase: User, Document, FtsRetriever, LocalExtractiveGenerator, ChatService, ProblemError. |
| 6 | Abstract Classes | N/A | Không có lớp trừu tượng; trừu tượng hóa dùng Protocol (vẽ bằng «interface»). |
| 7 | Interfaces | In Progress | Có «interface» AnswerGenerator (CMP-07). Vẫn thiếu «interface» Retriever dù SAD §5.3 định nghĩa Protocol Retriever (DF-14 cập nhật chữ ký); ChatService vẫn phụ thuộc trực tiếp FtsRetriever. |
| 8 | Visibility | Done | Mọi thuộc tính có tiền tố + hoặc - (vd. -password_hash, -token_hash, -model, -timeout_s). |
| 9 | Typing & Format | In Progress | Phần lớn dạng "name: type". Còn sai: "+role: user/manager" và "+status: processing/ready/failed/no_text" dùng dấu gạch đứng thay cho enum; "+mode = 'local'", "-max_failures = 5" thiếu kiểu; datetime trong khi DDL lưu TEXT không chú thích. |
| 10 | Multiplicity (Optional) | In Progress | Dùng Citation[], str[], int[] thay vì [0..*]; "+reason: str[0..500]" dùng ký hiệu multiplicity để biểu diễn độ dài chuỗi (nên là {maxLength=500}). Không đổi. |
| 11 | Static Attributes | N/A | Không có thuộc tính cấp lớp; max_failures, window_s là cấu hình instance theo blueprint §3.3. |
| 12 | Visibility | Done | Phương thức có + / - (vd. +retrieve, -candidates, -idf, -validate_citations, +check). |
| 13 | Signatures | In Progress | Thiếu kiểu tham số/trả về: LocalExtractiveGenerator.generate(question, chunks), AnthropicGenerator.generate(question, chunks), LoginLimiter.check/fail/reset(key), -candidates(...), -validate_citations(answer, chunks). FtsRetriever.retrieve thiếu tham số cited_documents đã thêm vào SAD §5.3 theo DF-14 (lệch mới). |
| 14 | Abstract Operations | N/A | Phương thức trong «interface» AnswerGenerator mặc nhiên trừu tượng; không có lớp trừu tượng khác. |
| 15 | Static Operations | In Progress | Settings.from_env(): Settings là classmethod/factory nhưng vẫn không gạch chân (style không có fontStyle=4). |
| 16 | Association Lines | Done | Đường liền endArrow=none: User–AuditEvent, Feedback–User. |
| 17 | Navigability | N/A | Quan hệ FK ở mức miền, điều hướng hai chiều; không cần mũi tên. |
| 18 | Multiplicity | In Progress | Multiplicity vẫn là một nhãn giữa cạnh ("1 — 0..*") thay vì đặt ở hai đầu. Turn–Feedback ghi 0..* trong khi schema.sql có PRIMARY KEY (turn_id, user_id) và một lượt chỉ thuộc chủ hội thoại, nên thực tế là 0..1. |
| 19 | Roles | Pending | Không có role name ở đầu quan hệ (vd. owner, author, rater). Không được xử lý trong REFINE. |
| 20 | Aggregation (Shared) | N/A | Không có quan hệ chia sẻ trong miền. |
| 21 | Composition (Strong) | Done | Kim cương đặc (startArrow=diamondThin;startFill=1): User◆Session/Document/Conversation, Document◆Chunk, Conversation◆Turn, Turn◆Feedback — khớp ON DELETE CASCADE trong schema.sql. |
| 22 | Generalization (Inheritance) | N/A | Không có kế thừa lớp. |
| 23 | Realization (Implementation) | Done | LocalExtractiveGenerator, AnthropicGenerator → AnswerGenerator bằng nét đứt tam giác rỗng (endArrow=block;dashed=1;endFill=0). |
| 24 | Dependency | Done | Nét đứt mũi tên mở (endArrow=open;dashed=1): «creates», uses, reads, raises. |
| 25 | Cohesion & Coupling | In Progress | ChatService --uses--> FtsRetriever (lớp cụ thể) vẫn trái SAD §4 và §5.3 (Protocol Retriever). Thuộc tính khóa ngoại (Session.user_id, Turn.conversation_id, Turn.created_at, Feedback.turn_id/user_id, Document.processed_at) vẫn lược bỏ không chú thích so với schema.sql. |
| 26 | Overcrowding | Done | Tách 2 trang (miền 8 lớp, dịch vụ 11 lớp), mỗi trang ≤ 13 lớp. |

## Kiểm tra lại vòng trước

| Vấn đề vòng 1 | Trạng thái vòng 2 | Bằng chứng |
|---|---|---|
| Thiếu «interface» Retriever (row 7, 25) | Chưa sửa | class_diagram.drawio trang "Service classes" chỉ có FtsRetriever; tools/gen_diagrams.py class_diagram() không thay đổi nội dung |
| Không tách ngăn operations (row 4) | Chưa sửa — DF-20 Partial, hoãn | design-refine-log.md DF-20 |
| Multiplicity giữa cạnh (row 18) | Chưa sửa | Nhãn "1 — 0..*" trên các cạnh E_COMPOSE |
| Chữ ký thiếu kiểu (row 13) | Chưa sửa; thêm lệch cited_documents | SAD §5.3 so với dòng "+retrieve(conn, user_id, question, history, document_ids)" |
| Static operation không gạch chân (row 15) | Chưa sửa | Settings.from_env() |

## Phát hiện

| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-CLS-01 | Major | Trang "Service classes" — FtsRetriever, ChatService | Không có «interface» Retriever; ChatService phụ thuộc lớp cụ thể, trái SAD §5.3 và ADR-002/004 | Thêm «interface» Retriever, FtsRetriever realize nó, ChatService uses interface |
| AUD-CLS-02 | Minor | FtsRetriever.retrieve | Thiếu tham số cited_documents so với SAD §5.3 (DF-14) | Đồng bộ chữ ký với app/backend/cwd/retrieval.py |
| AUD-CLS-03 | Minor | Mọi lớp (DF-20) | Không có ngăn operations riêng | Sửa klass() trong tools/gen_diagrams.py thêm đường phân cách |
| AUD-CLS-04 | Minor | Cạnh miền | Multiplicity đặt giữa cạnh, không có role name | Dùng nhãn nguồn/đích của edge |
| AUD-CLS-05 | Minor | Thuộc tính, chữ ký | Kiểu dạng a/b thay cho enum, thiếu kiểu trả về, str[0..500], from_env không gạch chân | Sửa danh sách thuộc tính trong gen_diagrams.py |

## Tóm tắt

- Status: Done 9 · In Progress 9 · Pending 1 · N/A 6 (tổng 25 dòng).
- Phát hiện: Critical 0 · Major 1 · Minor 4.
- Nhận định: **Cần sửa** — REFINE không chạm class diagram; AUD-CLS-01 (thiếu interface Retriever) là lệch với SAD, còn lại là ký hiệu thuộc DF-20 (Partial, owner Architect).

## Lịch sử audit

| Vòng | Ngày | Thay đổi Status | Lý do |
|---|---|---|---|
| 1 | 2026-10-28 | Bản đầu: Done 9 · In Progress 9 · Pending 1 · N/A 6 | Audit độc lập trước REFINE |
| 2 | 2026-11-02 | Không dòng nào đổi Status | class_diagram.drawio không đổi nội dung sau REFINE (e1c8a1d) và commit 1aba0aa; DF-14 chỉ sửa SAD §5.3, DF-20 còn Partial. Cập nhật Notes row 4, 7, 9, 13 (lệch cited_documents mới), 15, 25 |
