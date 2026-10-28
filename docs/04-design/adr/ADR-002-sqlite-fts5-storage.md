# ADR-002 — SQLite + FTS5 làm kho dữ liệu duy nhất cho MVP

- **Trạng thái:** Proposed · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Thay thế:** AD-03 của SAD v0.1 (PostgreSQL 16 + pgvector + Redis + object storage)

## Bối cảnh
- SAD v0.1 đề xuất PostgreSQL + pgvector + Redis + object storage. Môi trường hiện tại không có Docker, không có PostgreSQL hay Redis (SRC-005); DEP-003 (hạ tầng) chưa có hạn.
- Quy mô thiết kế (PRD §3.9.4): ≤ 30 người dùng × 50 tài liệu × 300 trang ⇒ tối đa ~450 000 trang, thực tế MVP vài nghìn trang.
- Python 3.15 có sẵn SQLite 3.53 với FTS5 (đã kiểm tra).

## Quyết định
- Dùng **một file SQLite** (chế độ WAL, `foreign_keys=ON`) cho người dùng, phiên, tài liệu, chunk, hội thoại, phản hồi, nhật ký kiểm toán.
- Tìm kiếm toàn văn bằng **FTS5** trên văn bản đã chuẩn hóa (bỏ dấu tiếng Việt, `đ→d`, chữ thường).
- File PDF gốc lưu trên đĩa tại `CWD_DATA_DIR/files/<document_id>.pdf`.
- Mọi truy cập dữ liệu đi qua module `app/backend/cwd/db.py` + các hàm repository; bộ truy xuất đi qua interface `Retriever` (ADR-004).

## Phương án đã cân nhắc
| Phương án | Lý do không chọn cho MVP |
|---|---|
| PostgreSQL + pgvector (SAD v0.1) | Không có hạ tầng; chặn toàn bộ Phase 6 chờ DEP-003 |
| CSDL vector chuyên dụng (Chroma, Qdrant) | Cần mô hình embedding (ADR-004) và thêm một hệ thống |
| Lưu file JSON | Không có transaction, không có tìm kiếm toàn văn |

## Điều kiện xem lại (trigger)
Chuyển sang PostgreSQL + pgvector khi một trong các điều kiện sau xảy ra: > 5 câu hỏi đồng thời kéo dài; > 200 000 chunk; cần nhiều instance ứng dụng; IT yêu cầu CSDL được quản lý tập trung.

## Hệ quả
- (+) Không phụ thuộc hạ tầng; sao lưu bằng một lệnh (`python -m cwd.cli backup`), đáp ứng NFR-006.
- (+) Test chạy trên CSDL tạm, tất định.
- (−) Một writer tại một thời điểm; đủ cho quy mô ASM-003.
- (−) Không mã hóa khi lưu ở mức CSDL; dựa vào mã hóa đĩa của máy chủ (ghi vào rủi ro R-03 của SAD).
- **Khó đảo ngược:** Trung bình — schema SQL chuẩn, chỉ FTS5 là đặc thù SQLite.
