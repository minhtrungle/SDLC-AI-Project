# Audit — Database Design theo checklist

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/data/model.md (sau REFINE, có §7), app/backend/cwd/schema.sql, ADR-002, ADR-005, ADR-007, SAD §7, §7.1, §7.2 |
| Checklist | docs/checklists/Database_Design_Checklist.xlsx |
| Reviewer | artifact-auditor (agent) — vòng 1: Independent reviewer agent |
| Ngày | 2026-11-02 (vòng 1: 2026-10-28) |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d), đối chiếu design-refine-log.md DF-01..DF-27 và code app/ hiện tại |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Workload Classification | In Progress | model.md vẫn không phân loại workload (đầu file chỉ ghi Loại CSDL: quan hệ). Ngầm hiểu OLTP nhỏ + tìm kiếm toàn văn FTS5 + tổng hợp tuần; cần ghi tường minh. |
| 3 | Data Volume & Growth | In Progress | Đã có kích thước ban đầu ở SAD §7.1 (DF-10): PDF ≈ 4,5 GB (trần 30 GB), cwd.db 1–2 GB; ADR-002 trigger > 200 000 chunk. Còn thiếu tốc độ tăng theo tháng/năm của turns, audit_log, feedback. |
| 4 | Read/Write Ratio | Pending | Không có trong model.md, ADR-002 hay SAD. Thực tế đọc nhiều (truy xuất) + ghi theo đợt (ingestion một transaction) — cần ghi để biện minh WAL và một writer. |
| 5 | Consistency Requirements | Done | ACID của SQLite, WAL, foreign_keys=ON (model.md đầu trang); ingestion ghi chunks + FTS trong một transaction (ADR-008, activity diagram). |
| 6 | Latency SLAs | In Progress | Có NFR-001 đầu-cuối P90 ≤ 2 s và số đo P90 = 37,6 ms ở chế độ cục bộ (SAD §7.1, eval-report.json); chunks_fts có cột owner phân vùng theo workspace giảm chi phí df(t) (schema.sql, CR-09). Chưa có ngân sách đọc/ghi ở mức CSDL (truy vấn FTS, ghi ingestion). |
| 7 | ER Modeling | Done | model.md §1 ERD mermaid với 1:N, chunks↔chunks_fts; §2 ENT-01..08. |
| 8 | Normalization | Done | Các bảng ở 3NF; điểm phi chuẩn hóa có chủ đích được ghi (citations_json, audit_log.username). Không có lập luận 3NF tường minh. |
| 9 | Denormalization Strategy | Done | citations_json là snapshot bất biến (ADR-005, model.md §5); audit_log.username giữ khi user bị xóa. |
| 10 | Primary & Surrogate Keys | Done | Mọi bảng có PK; chunks.id INTEGER PRIMARY KEY AUTOINCREMENT, không tái sử dụng (schema.sql, model.md ENT-04, ADR-005 dòng 13 — DF-01); kiểm chứng bằng test_chunk_ids_not_reused_after_delete (tests/test_conversation.py). |
| 11 | Foreign Keys & Constraints | In Progress | FK + ON DELETE CASCADE/SET NULL, CHECK role/status/outcome/rating/reason/page/size_bytes. Các ràng buộc còn thiếu (CHECK audit_log.action, latency_ms >= 0, json_valid(citations_json), UNIQUE(document_id, ord)) được hoãn có chủ đích ở model.md §7 (DF-19, owner Tech Lead) — chưa có trong schema. |
| 12 | Optimal Data Types | Done | Kiểu SQLite phù hợp (INTEGER/TEXT); thời gian TEXT ISO 8601 UTC dạng Z (openapi.md §2) nên so sánh chuỗi theo tuần đúng. |
| 13 | Semi-Structured Data | Done | Chỉ citations_json, scope_json — snapshot, không thay thế bảng quan hệ. CHECK json_valid hoãn (model.md §7). |
| 14 | High-Dimensional Data | N/A | Không dùng vector trong MVP (ADR-004); hướng embedding vector(D) ở model.md §6. |
| 15 | Time-Series Data | N/A | Không có kho time-series; tổng hợp tuần dùng ix_turns_created. |
| 16 | Primary/Unique Indexes | Done | Tự tạo bởi PRIMARY KEY và UNIQUE (users.username, sessions.token_hash, feedback PK kép). |
| 17 | Foreign Key Indexing | In Progress | Có ix_sessions_user, ix_documents_user_status, ix_chunks_document, ix_conversations_user, ix_turns_conversation. feedback(user_id) và audit_log(user_id) vẫn chưa có chỉ mục — hoãn ở model.md §7 (DF-19); khi xóa user, cascade/SET NULL vẫn quét toàn bảng. |
| 18 | Specialized Indexes | Done | FTS5 (unicode61) cho chunks_fts, có cột owner phân vùng workspace; B-Tree cho truy vấn còn lại (model.md §4). |
| 19 | Covering Indexes | In Progress | ix_turns_conversation(conversation_id, created_at) phù hợp. Truy vấn số liệu tuần join turns→conversations và feedback theo lượt trong tuần chưa có phân tích EXPLAIN; feedback không có chỉ mục hỗ trợ. Không thay đổi sau REFINE. |
| 20 | Partitioning Strategy | N/A | Quy mô nhỏ (ADR-002); chỉ có dọn audit_log > 90 ngày. |
| 21 | Sharding (Horizontal Scaling) | N/A | Một file SQLite; trigger chuyển PostgreSQL ở ADR-002. |
| 22 | Replication | N/A | Không có replica; bù bằng sao lưu hằng ngày ngoài máy (Row 25). |
| 23 | Role-Based Access (RBAC) | In Progress | SQLite không có role; chỉ có "quyền thư mục" ở SAD R-03. Chưa đặc tả tài khoản dịch vụ sở hữu CWD_DATA_DIR, quyền file (chmod 700/ACL) và tách quyền chạy CLI restore. Không thay đổi sau REFINE. |
| 24 | Encryption | Done | SAD §7 Bắt buộc ở prod (DF-27): TLS tại reverse proxy + CWD_COOKIE_SECURE=true (in transit), mã hóa đĩa chứa CWD_DATA_DIR (at rest, IT); là điều kiện go-live cần IT xác nhận. Mặc định cookie_secure=false chỉ cho dev. |
| 25 | Disaster Recovery (DR) | Done | SAD §7.2 (DF-11): backup hằng ngày 01:00 bằng Task Scheduler/cron ra kho ngoài máy chủ, giữ 30 bản, CSDL trước files/, diễn tập quý (QS-07 RTO ≤ 4 h); deployment diagram có node sao lưu ngoài; restore được test (test_backup_and_restore_roundtrip, test_cr10_bad_backup_leaves_live_data_untouched, test_nr10_restore_refuses_while_database_is_in_use). Minor: model.md §5 chưa nêu lịch/đích sao lưu. |
| 26 | Audit Logging | In Progress | DML quan trọng ghi audit_log (login, logout, upload, delete). Quản lý thay đổi schema (DDL) vẫn chưa có: schema.sql chỉ CREATE IF NOT EXISTS, không PRAGMA user_version; model.md §7 hoãn tới trước thay đổi schema đầu tiên sau go-live (DF-19). |

## Kiểm tra lại vòng trước
| Row | Vấn đề vòng 1 | Kết quả vòng 2 |
|---|---|---|
| 3 | Không có ước lượng dung lượng | Có ở SAD §7.1; thiếu tốc độ tăng |
| 10 | chunk_id có thể tái sử dụng (Blocker) | Đã sửa: AUTOINCREMENT + test (DF-01) |
| 11, 17, 26 | Thiếu CHECK/UNIQUE, chỉ mục FK, migration | Hoãn có owner (model.md §7, DF-19) |
| 24 | TLS khuyến nghị, mã hóa đĩa chưa cam kết | Đã thành yêu cầu bắt buộc ở prod (DF-27) |
| 25 | Không lịch sao lưu, backup cùng đĩa | Đã sửa (DF-11) |

## Phát hiện
| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-DB-01 | Major | schema.sql, model.md §7 | Không có versioning schema (PRAGMA user_version, migrate) — thay đổi schema sau go-live sẽ không áp lên CSDL cũ; đang hoãn | Thêm user_version = 1 và hàm migrate trước baseline phát hành |
| AUD-DB-02 | Minor | model.md | Thiếu phân loại workload, tỷ lệ đọc/ghi, tốc độ tăng dữ liệu | Thêm mục §0 Đặc tính tải |
| AUD-DB-03 | Minor | schema.sql | Ràng buộc và chỉ mục hoãn (DF-19) | Thêm cùng migration đầu tiên |
| AUD-DB-04 | Minor | SAD R-03 / §7 | Chưa đặc tả quyền tối thiểu trên CWD_DATA_DIR và CLI restore | Thêm vào checklist go-live |
| AUD-DB-05 | Minor | model.md §5 | Dòng Sao lưu chưa nêu lịch, đích ngoài máy, thứ tự — chỉ có ở SAD §7.2 | Liên kết SAD §7.2 |

## Tóm tắt
- Status: Done 11 · In Progress 8 · Pending 1 · N/A 5 (tổng 25).
- Phát hiện: Critical 0 · Major 1 · Minor 4.
- Nhận định: Blocker vòng 1 (tái sử dụng chunk_id) đã đóng; DR và mã hóa đạt. Cần sửa trước baseline phát hành: AUD-DB-01 (migration). Các In Progress còn lại là tài liệu hóa đặc tính tải và hạng mục hoãn có owner.

## Lịch sử audit
| Ngày | Vòng | Row | Status cũ → mới | Lý do |
|---|---|---|---|---|
| 2026-10-28 | 1 | — | — | Audit ban đầu: Done 8, In Progress 11, Pending 1, N/A 5 |
| 2026-11-02 | 2 | 10 | In Progress → Done | chunks.id AUTOINCREMENT + test_chunk_ids_not_reused_after_delete (DF-01) |
| 2026-11-02 | 2 | 24 | In Progress → Done | TLS, cookie secure, mã hóa đĩa thành yêu cầu bắt buộc ở prod (SAD §7, DF-27) |
| 2026-11-02 | 2 | 25 | In Progress → Done | Lịch hằng ngày, kho ngoài máy, giữ 30 bản, diễn tập quý (SAD §7.2, DF-11); restore có test |
| 2026-11-02 | 2 | 3, 6, 11, 17, 26 | In Progress → In Progress | Cải thiện một phần hoặc hoãn có owner (DF-10, DF-19); Notes đã cập nhật |
