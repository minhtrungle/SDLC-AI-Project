# ADR-004 — Truy xuất từ vựng (FTS5) có chuẩn hóa tiếng Việt và ngưỡng liên quan theo IDF

- **Trạng thái:** Proposed · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Liên quan:** FR-010, FR-012, FR-014, FR-015, NFR-003; AD-03/AD-05 của SAD v0.1 (tìm kiếm lai vector + từ khóa)

## Bối cảnh
- Tìm kiếm vector cần mô hình embedding: dịch vụ ngoài bị chặn bởi OQ-006, mô hình cục bộ cần tải trọng số lớn và không chắc chạy trên Python 3.15.
- Câu hỏi nghiệp vụ thường chứa tên riêng, mã hợp đồng, con số — tìm kiếm từ khóa xử lý tốt.
- Người dùng có thể gõ không dấu.
- FR-012 cần một ngưỡng **tuyệt đối** để quyết định `not_found`; điểm BM25 chỉ có ý nghĩa tương đối.

## Quyết định
1. **Chuẩn hóa:** NFD → bỏ dấu kết hợp → `đ→d` → chữ thường; tách token theo ký tự chữ/số. Áp dụng cho cả văn bản chunk (cột FTS) và câu hỏi.
2. **Ứng viên:** truy vấn FTS5 `OR` các token nội dung (đã bỏ stopword tiếng Việt/Anh), giới hạn trong tài liệu `ready` của người dùng và phạm vi đã chọn, lấy 50 ứng viên theo `bm25()`.
3. **Điểm liên quan** của chunk *c* với tập token câu hỏi *T*: `rel(c) = Σ idf(t), t ∈ T ∩ c  /  Σ idf(t), t ∈ T`, với `idf(t) = ln(1 + N / df(t))` tính trong phạm vi workspace. Giá trị trong [0, 1].
4. **Ngưỡng:** chunk có `rel ≥ CWD_MIN_RELEVANCE` (mặc định 0.6) mới được dùng. Không chunk nào đạt ⇒ `not_found` (không gọi bộ sinh).
5. **Đa dạng nguồn:** giữ tối đa `CWD_TOP_K` (mặc định 6) chunk, tối đa 2 chunk mỗi tài liệu.
6. **Hội thoại (FR-014):** token của tối đa 3 câu hỏi trước được dùng để **xếp hạng phụ** (cộng điểm nhỏ), không dùng để tính ngưỡng — tránh câu hỏi tiếp theo bị trả lời bằng ngữ cảnh cũ khi tài liệu không có thông tin mới.

## Phương án đã cân nhắc
| Phương án | Lý do không chọn |
|---|---|
| Vector + từ khóa (SAD v0.1) | Chặn bởi OQ-006 / thiếu mô hình embedding |
| Chỉ dùng `bm25()` + ngưỡng cố định | Điểm BM25 phụ thuộc độ dài và kho; không có ý nghĩa tuyệt đối |

## Hệ quả
- (+) Tất định, giải thích được (vì sao chunk được chọn), test được không cần mạng.
- (−) Không hiểu đồng nghĩa ("giá trị" vs "tổng tiền"). Giảm thiểu: bộ đánh giá `tests/eval` đo tỷ lệ bỏ sót; thêm embedding sau như một `Retriever` thứ hai khi OQ-006 cho phép.
- (−) Ngưỡng 0.6 phải hiệu chỉnh lại bằng bộ câu hỏi chuẩn thật (DEP-002).
- **Khó đảo ngược:** Thấp — nằm sau interface `Retriever`.
