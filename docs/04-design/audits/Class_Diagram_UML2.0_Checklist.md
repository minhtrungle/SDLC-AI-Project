# Audit — Class Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/class_diagram.drawio (trang "Domain (ENT)" và "Service classes"); đối chiếu blueprint §3.3, SAD §5.3, app/schema.sql |
| Checklist | docs/design/Class_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | Done | Hai trang có tên "Domain (ENT)" và "Service classes". Không có khung tiêu đề trong sơ đồ. |
| 3 | Abstraction Level | In Progress | Không ghi rõ mức. Trang Domain trộn mức vật lý («table users», password_hash) với mức logic (citations: Citation[], scope: str[] trong khi bảng lưu citations_json/scope_json TEXT). |
| 4 | Class Notation | In Progress | Dùng khối stack (swimlane) nhưng không có ngăn phân cách thuộc tính/phương thức: Settings, AnthropicGenerator, LoginLimiter trộn thuộc tính và phương thức trong một danh sách; lớp Domain không có ngăn operations. |
| 5 | Naming Conventions | Done | PascalCase: User, Document, FtsRetriever, LocalExtractiveGenerator, ProblemError. |
| 6 | Abstract Classes | N/A | Không có lớp trừu tượng (dùng Protocol/interface). |
| 7 | Interfaces | In Progress | «interface» AnswerGenerator có. Thiếu «interface» Retriever dù SAD §5.3 định nghĩa Protocol Retriever và ADR-002/004 dựa vào nó; ChatService phụ thuộc trực tiếp FtsRetriever. |
| 8 | Visibility | Done | Thuộc tính có +/- (vd. -password_hash, -token_hash). |
| 9 | Typing & Format | In Progress | Phần lớn "name: type". Sai: "+role: user/manager" (trong sơ đồ dùng dấu gạch đứng) dùng ký hiệu không phải kiểu (nên là enum Role); "+mode = 'local'" thiếu kiểu; datetime trong khi DDL lưu TEXT không được chú thích. |
| 10 | Multiplicity (Optional) | In Progress | Dùng Citation[], str[], int[] thay vì [0..*]; "+reason: str[0..500]" dùng ký hiệu multiplicity để biểu diễn độ dài chuỗi — sai ngữ nghĩa (nên là ràng buộc {maxLength=500}). |
| 11 | Static Attributes | N/A | Không có thuộc tính cấp lớp (max_failures, window_s là cấu hình instance theo blueprint §3.3). |
| 12 | Visibility | Done | Phương thức có + / - (vd. -candidates, -idf, -validate_citations). |
| 13 | Signatures | In Progress | Thiếu kiểu tham số/trả về: LocalExtractiveGenerator.generate(question, chunks), AnthropicGenerator.generate(...), LoginLimiter.check(key)/fail/reset, -candidates(...), -validate_citations(answer, chunks). |
| 14 | Abstract Operations | N/A | Phương thức trong interface mặc nhiên trừu tượng. |
| 15 | Static Operations | In Progress | Settings.from_env() là classmethod/factory nhưng không gạch chân. |
| 16 | Association Lines | Done | Đường liền: User–AuditEvent, Feedback–User. |
| 17 | Navigability | N/A | Quan hệ FK hai chiều ở mức miền; không bắt buộc. |
| 18 | Multiplicity | In Progress | Multiplicity ghi thành một nhãn giữa cạnh "1 — 0..*" thay vì đặt ở hai đầu; đọc sai hướng dễ xảy ra. Turn–Feedback ghi 0..* trong khi một lượt chỉ thuộc một người (thực tế 0..1). |
| 19 | Roles | Pending | Không có role name (vd. owner, author, rater). |
| 20 | Aggregation (Shared) | N/A | Không có quan hệ chia sẻ. |
| 21 | Composition (Strong) | Done | Kim cương đặc: User◆Session/Document/Conversation, Document◆Chunk, Conversation◆Turn, Turn◆Feedback — khớp ON DELETE CASCADE trong schema.sql. |
| 22 | Generalization (Inheritance) | N/A | Không có kế thừa. |
| 23 | Realization (Implementation) | Done | LocalExtractiveGenerator, AnthropicGenerator → AnswerGenerator bằng nét đứt tam giác rỗng. |
| 24 | Dependency | Done | Nét đứt mũi tên mở «creates», uses, reads, raises. |
| 25 | Cohesion & Coupling | In Progress | ChatService phụ thuộc lớp cụ thể FtsRetriever (vi phạm SAD §4 Q4 "interface Retriever"). Thuộc tính khóa ngoại/khóa quan hệ (Session.user_id, Turn.conversation_id, Turn.created_at, Feedback.turn_id/user_id, Document.processed_at) bị lược bỏ không chú thích — lệch schema.sql. |
| 26 | Overcrowding | Done | Tách 2 trang (miền và dịch vụ), mỗi trang ≤ 13 lớp. |

## Tóm tắt
Sơ đồ đúng các ký hiệu cơ bản (composition, realization, dependency). Cần: thêm «interface» Retriever, tách ngăn operations, đặt multiplicity ở hai đầu, sửa kiểu/chữ ký, đồng bộ Settings và ChatService với blueprint §3.3.
