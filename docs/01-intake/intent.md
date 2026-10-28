# Intent — Công cụ "Chat với tài liệu" (MVP)

| Mục | Giá trị |
|---|---|
| Work item | WI-001 |
| Owner (đề xuất) | Quản lý dự án (STK-001) — [chờ xác nhận tên] |
| Tác giả | Agent (Claude) — bản nháp |
| Risk tier | **Medium** cho toàn hệ thống; **High** cho các đường xác thực, phân quyền và dữ liệu tài liệu (xem §8) |
| Trạng thái | Draft — chờ PO phê duyệt |
| Ngày | 2026-10-28 |
| Nguồn | SRC-001, SRC-002 (xem [sources.md](sources.md)) |

## 1. Problem
Đội phát triển kinh doanh làm việc với nhiều tài liệu PDF của dự án. Muốn có một thông tin, họ phải mở từng file, tìm thủ công rồi tự tổng hợp. Việc này tốn thời gian và dễ bỏ sót (SRC-001). Mức độ tác động chưa được đo (OQ-003).

## 2. Proposed outcome
Một ứng dụng web MVP cho phép người dùng tải lên PDF và hỏi đáp bằng tiếng Việt. Câu trả lời **chỉ dựa trên nội dung tài liệu** và **kèm trích dẫn tên tài liệu + số trang** để người dùng kiểm chứng.

## 3. Affected users
| Nhóm | Ảnh hưởng |
|---|---|
| Đội phát triển kinh doanh (người dùng chính) | Tìm thông tin nhanh hơn, có nguồn kiểm chứng |
| Quản lý dự án (sponsor) | Đo được giá trị MVP qua số liệu sử dụng và phản hồi |
| IT / Bảo mật | Phải review luồng dữ liệu trước go-live |

## 4. Constraints
- Ứng dụng web; đầu vào chỉ PDF; phạm vi MVP (SRC-001).
- Dữ liệu kinh doanh nội bộ: mặc định **không gửi nội dung ra dịch vụ AI bên ngoài** cho tới khi IT/Bảo mật cho phép (OQ-006, xem ADR-003).
- Môi trường đội kỹ thuật hiện tại: Python 3.15, Node 14, không có Docker (ADR-001, ADR-002).

## 5. Success measures
| ID | Thước đo | Target đề xuất (chờ PO chốt, OQ-005) |
|---|---|---|
| MET-001 | Thời gian tìm một thông tin trên bộ câu hỏi chuẩn | Giảm ≥ 50% so với baseline |
| MET-002 | Tỷ lệ câu trả lời đúng + trích dẫn đúng | ≥ 85% đúng; ≥ 90% trích dẫn đúng tài liệu và trang |
| MET-003 | Người dùng hoạt động hàng tuần | ≥ 70% thành viên đội kinh doanh sau 4 tuần |

## 6. Out of scope
Định dạng khác PDF, OCR cho PDF scan, ứng dụng mobile, tích hợp Drive/SharePoint, sinh tài liệu mới, phân quyền chi tiết theo nhóm, lịch sử hội thoại giữa các phiên (US-404), tóm tắt tài liệu (US-601).

## 7. Open questions
Danh sách đầy đủ ở BRD §12. Các câu chặn baseline: OQ-001 (người phê duyệt), OQ-003/005 (baseline và target), OQ-006 (chính sách dữ liệu), OQ-011/012 (giới hạn file, độ trễ). Bảng **giá trị mặc định đề xuất** để đội có thể tiếp tục làm việc nằm ở [BRD §12.1](../02-requirements/BRD.md#121-giá-trị-mặc-định-đề-xuất-để-không-chặn-tiến-độ).

## 8. Risk tier và lý do
| Khu vực | Tier | Lý do | Hệ quả về quy trình |
|---|---|---|---|
| Xác thực, phiên, phân quyền workspace | High | Lộ tài liệu kinh doanh (RSK-002) | Inspection L3 bắt buộc khi review |
| Pipeline hỏi đáp (grounding, trích dẫn) | Medium | Trả lời sai (RSK-001) | Bộ test grounding/injection chạy trong CI |
| UI, dashboard | Low | Không chạm dữ liệu nhạy cảm | Review L2 thông thường |

## 9. Acceptance criteria cho work item
1. Mọi user story P0 đạt toàn bộ AC tự động trong CI.
2. Coverage ≥ 70%, lint sạch, không phát hiện secret.
3. IT/Bảo mật ký xác nhận luồng dữ liệu (AC-020) trước go-live.

## 10. Phê duyệt
| Vai trò | Tên | Quyết định | Ngày |
|---|---|---|---|
| Product Owner | [chờ OQ-001] | ☐ Approve ☐ Reject | |

> Agent không tự phê duyệt. Mục này để con người ký.
