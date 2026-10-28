# Release Plan & Release Notes — Chat với tài liệu v0.1.0 (MVP)

> **Trạng thái: CHƯA ĐƯỢC PHÉP PHÁT HÀNH.** Agent chuẩn bị tài liệu; **chỉ con người** (Release owner = PO) được authorize deploy (Process §9, luật bất biến). Các mục ☐ dưới đây phải được người có trách nhiệm đánh dấu.

## 1. Release notes (v0.1.0)

**Tính năng**
- Đăng nhập bằng tài khoản do quản trị tạo; phiên an toàn (cookie HttpOnly/SameSite=Strict, CSRF, khóa tạm sau 5 lần sai).
- Tải lên nhiều PDF (≤ 20 MB/file, ≤ 50 tài liệu/người), kiểm tra định dạng, xử lý nền, trạng thái Đang xử lý / Sẵn sàng / Lỗi / Không có văn bản.
- Hỏi đáp tiếng Việt (có dấu hoặc không dấu) trên toàn bộ hoặc một phần tài liệu; câu trả lời chỉ từ tài liệu, kèm trích dẫn tên tài liệu + trang; bấm trích dẫn xem đoạn gốc.
- Hỏi tiếp theo ngữ cảnh, xem lại hội thoại, cuộc hội thoại mới.
- Xóa tài liệu (tài liệu đã xóa không bao giờ được dùng lại).
- Đánh giá câu trả lời; dashboard số liệu tuần cho quản lý.
- Nhật ký kiểm toán; CLI quản trị: tạo người dùng, sao lưu, khôi phục, dọn nhật ký.

**Chế độ xử lý:** mặc định **cục bộ** — không gửi dữ liệu ra ngoài. Chế độ LLM ngoài có sẵn nhưng tắt, chỉ bật khi IT/Bảo mật cho phép (ADR-003).

**Giới hạn đã biết** (phải đưa vào hướng dẫn người dùng — LG-24)
1. Câu trả lời ở chế độ cục bộ là **trích nguyên câu** từ tài liệu, không diễn giải.
2. **Câu hỏi dùng từ đồng nghĩa không có trong tài liệu thường không tìm thấy** (đo: 12,5% trên tập diễn đạt khác — test-report §3). Hãy dùng đúng thuật ngữ trong tài liệu.
3. PDF bản scan (không có lớp văn bản) không đọc được; bảng biểu nhiều cột có thể trích xuất sai thứ tự.
4. Không có lịch sử các phiên trước (US-404) và tóm tắt tài liệu (US-601).

## 2. Artifact = reviewed commit
| Mục | Giá trị |
|---|---|
| Nhánh | `feat/chat-with-docs-sdlc` |
| Commit phát hành | ☐ ghi SHA sau khi PR được approve và merge vào `main` |
| Kiểm chứng | `git rev-parse HEAD` trên máy chủ = SHA trên; `python tools/ci_local.py` xanh tại SHA đó |

## 3. Go-live checklist (launch gate PRD §5.1 + DF-27)
| # | Mục | Owner | Trạng thái |
|---|---|---|---|
| 1 | PR được approve bởi reviewer ≠ author, rubric ≥ 10/14 (review-record.md) | Tech Lead | ☐ |
| 2 | Inspection L3 cho auth/session/workspace isolation đã ký | IT/Bảo mật | ☐ |
| 3 | IT ký luồng dữ liệu SAD §8.1 (AC-102.3, LG-13) | IT/Bảo mật | ☐ |
| 4 | Chạy lại `tests/eval` với **bộ câu hỏi thật** (DEP-002); đạt ≥ 85% / 90% / 9 trên 10 | QA + Đội kinh doanh | ☐ |
| 5 | Quyết định về hạn chế từ đồng nghĩa (R-01): chấp nhận cho pilot, hoặc bật LLM/embedding trước go-live | PO + IT | ☐ |
| 6 | UAT với đại diện đội kinh doanh, có biên bản (LG-21) | QA | ☐ |
| 7 | TLS tại reverse proxy; `CWD_COOKIE_SECURE=true` | IT | ☐ |
| 8 | Mã hóa đĩa chứa `CWD_DATA_DIR`; quyền thư mục chỉ cho tài khoản dịch vụ | IT | ☐ |
| 9 | Lịch sao lưu hằng ngày ra ngoài máy chủ + diễn tập khôi phục 1 lần (QS-07) | IT | ☐ |
| 10 | Giám sát `/api/health` mỗi phút (QS-08) | IT | ☐ |
| 11 | Tài khoản người dùng pilot đã tạo; không dùng `seed-demo` ở prod | IT | ☐ |
| 12 | Hướng dẫn sử dụng ngắn nêu giới hạn §1 (LG-24) | PO | ☐ |
| 13 | Các OQ chặn baseline (OQ-001, 003, 005, 006, 011, 012) đã chốt (LG-25) | PO | ☐ |

## 4. Kế hoạch triển khai theo giai đoạn
| Giai đoạn | Phạm vi | Thời gian | Tiêu chí đi tiếp | Chỉ số theo dõi |
|---|---|---|---|---|
| Canary | 3 người dùng pilot của đội kinh doanh | 1 tuần | 0 sự cố Sev1/Sev2; `not_found_rate` < 40%; đánh giá tích cực ≥ 60% | Dashboard tuần, log lỗi 5xx |
| Mở rộng | Toàn đội kinh doanh | 3 tuần | MET-003 ≥ 70% người dùng hoạt động | Dashboard tuần |
| Đánh giá MVP | — | Tuần 4 | Đo MET-001/002 theo BRD §4 | Bài đo bấm giờ, bộ câu hỏi chuẩn |

Feature flag: `CWD_ALLOW_EXTERNAL_AI` (mặc định tắt) — bật/tắt bằng cấu hình + khởi động lại, không cần deploy.

## 5. Rollback plan
| Tình huống | Hành động | Thời gian |
|---|---|---|
| Lỗi ứng dụng sau deploy | Dừng dịch vụ → checkout SHA trước → khởi động lại (schema chỉ dùng `CREATE IF NOT EXISTS`, tương thích lùi trong v0.1) | < 15 phút |
| Hỏng dữ liệu | `python -m app.cli restore <bản sao lưu gần nhất>` (runbook §5) | < 4 giờ (RTO) |
| Sự cố bảo mật | Dừng dịch vụ ngay; giữ nguyên dữ liệu và log để điều tra; báo IT/Bảo mật (runbook §6) | Ngay lập tức |

## 6. Release record (điền khi phát hành)
| Mục | Giá trị |
|---|---|
| Ngày giờ deploy | |
| Commit SHA | |
| Người authorize | |
| Người thực hiện | |
| Kết quả smoke test (`/api/health`, đăng nhập, hỏi 1 câu) | |
| Giai đoạn | Canary / Mở rộng |
