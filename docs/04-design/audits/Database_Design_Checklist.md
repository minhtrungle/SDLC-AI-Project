# Audit — Database Design theo checklist

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/data/model.md, app/schema.sql, ADR-002, ADR-005, ADR-007 |
| Checklist | docs/design/Database_Design_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Workload Classification | In Progress | model.md không phân loại workload. Ngầm hiểu OLTP nhỏ + tìm kiếm toàn văn (FTS5) + tổng hợp tuần (metrics); nên ghi rõ trong model.md §0. |
| 3 | Data Volume & Growth | In Progress | ADR-002 có quy mô ≤ 30 người × 50 tài liệu × 300 trang và trigger > 200 000 chunk; không có ước lượng dung lượng (MB/GB) của cwd.db, files/ và tốc độ tăng turns/audit_log mỗi tháng. |
| 4 | Read/Write Ratio | Pending | Không nêu. Thực tế đọc nhiều (truy xuất) + ghi theo đợt (ingestion một transaction lớn) — cần ghi để biện minh WAL và một writer. |
| 5 | Consistency Requirements | Done | ACID của SQLite, WAL, foreign_keys=ON (model.md đầu trang); ingestion ghi chunks + FTS trong một transaction (ADR-008, activity diagram). |
| 6 | Latency SLAs | In Progress | Chỉ có NFR-001 đầu-cuối P90 ≤ 2 s; không có ngân sách cho truy vấn FTS + df(t) (model.md §4 dòng 3 chạy count(*) cho từng token — chi phí N truy vấn mỗi câu hỏi chưa đánh giá). |
| 7 | ER Modeling | Done | model.md §1 ERD mermaid với 1:N, quan hệ chunks↔chunks_fts; §2 bảng thực thể ENT-01..08. |
| 8 | Normalization | Done | Các bảng ở 3NF; các điểm phi chuẩn hóa có chủ đích được ghi (citations_json, audit_log.username). Không có lập luận 3NF tường minh. |
| 9 | Denormalization Strategy | Done | citations_json là snapshot bất biến (ADR-005, model.md §5: giữ nguyên khi xóa tài liệu); audit_log.username giữ khi user bị xóa. |
| 10 | Primary & Surrogate Keys | In Progress | Mọi bảng có PK. Nhưng chunks.id là INTEGER PRIMARY KEY không AUTOINCREMENT: SQLite có thể tái sử dụng rowid lớn nhất sau khi xóa tài liệu mới nhất → citations_json cũ trỏ chunk_id của tài liệu mới, GET /api/chunks/{id} trả sai đoạn văn. Dùng AUTOINCREMENT hoặc kiểm tra document_id khi mở trích dẫn. |
| 11 | Foreign Keys & Constraints | In Progress | FK + ON DELETE CASCADE/SET NULL, CHECK role/status/outcome/rating/reason. Thiếu so với model.md: CHECK latency_ms >= 0; CHECK action IN (5 giá trị); UNIQUE(document_id, ord) trên chunks; CHECK error_code chỉ khác NULL khi failed; CHECK json_valid(citations_json). |
| 12 | Optimal Data Types | Done | Kiểu SQLite phù hợp (INTEGER/TEXT); thời gian lưu TEXT ISO 8601. Nên ghi rõ định dạng UTC 'Z' để so sánh chuỗi theo tuần đúng. |
| 13 | Semi-Structured Data | Done | Chỉ citations_json, scope_json — dữ liệu snapshot, không thay thế bảng quan hệ. Khuyến nghị thêm CHECK json_valid. |
| 14 | High-Dimensional Data | N/A | Không dùng vector trong MVP (ADR-004); hướng chuyển đổi embedding vector(D) ghi ở model.md §6. |
| 15 | Time-Series Data | N/A | Không có kho time-series; tổng hợp tuần dùng ix_turns_created. |
| 16 | Primary/Unique Indexes | Done | Tự tạo bởi PRIMARY KEY và UNIQUE (users.username, sessions.token_hash, feedback PK kép). |
| 17 | Foreign Key Indexing | In Progress | Có: ix_sessions_user, ix_documents_user_status, ix_chunks_document, ix_conversations_user, ix_turns_conversation. Thiếu: feedback.user_id (cascade khi xóa user) và audit_log.user_id (ON DELETE SET NULL quét toàn bảng). |
| 18 | Specialized Indexes | Done | FTS5 (unicode61) cho chunks_fts; B-Tree cho truy vấn còn lại (model.md §4). |
| 19 | Covering Indexes | In Progress | ix_turns_conversation(conversation_id, created_at) phù hợp. Truy vấn số liệu tuần cần join turns→conversations theo user và feedback theo tuần nhưng feedback không có chỉ mục created_at; chưa có phân tích EXPLAIN cho truy vấn nóng. |
| 20 | Partitioning Strategy | N/A | Quy mô nhỏ (ADR-002); chỉ có dọn audit_log > 90 ngày. |
| 21 | Sharding (Horizontal Scaling) | N/A | Một file SQLite; trigger chuyển PostgreSQL ở ADR-002. |
| 22 | Replication | N/A | Không có replica; bù bằng backup (row 25). |
| 23 | Role-Based Access (RBAC) | In Progress | SQLite không có role; chỉ nhắc "quyền thư mục" ở SAD R-03. Cần đặc tả quyền file (tài khoản dịch vụ chạy uvicorn sở hữu CWD_DATA_DIR, chmod 700/ACL) và tách quyền chạy CLI restore. |
| 24 | Encryption | In Progress | Không mã hóa ở mức CSDL; dựa vào mã hóa đĩa do IT (R-03, chưa có cam kết). TLS chỉ ở reverse proxy "khuyến nghị"; CWD_COOKIE_SECURE mặc định false. |
| 25 | Disaster Recovery (DR) | In Progress | Có CLI backup/restore (model.md §5) và QS-07 RTO ≤ 4 h. Thiếu: lịch sao lưu tự động để đạt RPO ≤ 24 h (NFR-006); backups/ nằm cùng CWD_DATA_DIR trên cùng đĩa (deployment diagram) nên hỏng đĩa mất cả bản sao; sao chép files/ không nhất quán thời điểm với backup SQLite. |
| 26 | Audit Logging | In Progress | DML quan trọng ghi audit_log (login, upload, delete). Không có quản lý thay đổi schema (DDL): chỉ CREATE IF NOT EXISTS, không có PRAGMA user_version hay migration — đổi schema sau go-live sẽ không áp dụng lên CSDL cũ. |

## Tóm tắt
Schema gọn, đúng với ERD, có FK + CHECK + FTS5. Rủi ro đáng chú ý nhất là tái sử dụng chunk_id làm hỏng trích dẫn cũ; tiếp theo là DR (backup cùng đĩa, không lịch) và thiếu migration/versioning schema.
