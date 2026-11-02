# Audit — Intake theo checklist 7 mục intent + cổng SOP §5.1

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | [intent.md](intent.md), [sources.md](sources.md), [stakeholders.md](stakeholders.md), [glossary.md](glossary.md) |
| Checklist | [Intake_Intent_Checklist.xlsx](../checklists/Intake_Intent_Checklist.xlsx) (7 mục intent theo [agentic-sdlc-process.md](../agentic-sdlc-process.md) §2 + cổng [AI_SDLC-SOP.md](../AI_SDLC-SOP.md) §5.1) |
| Bản đã điền | [Intake_Intent_Checklist_filled.xlsx](Intake_Intent_Checklist_filled.xlsx) |
| Reviewer | Agent (Claude). Đây là kết quả tự kiểm tra; PO phải review độc lập. |
| Ngày | 2026-11-02 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Problem | Done | intent §1: nêu vấn đề, nhóm bị ảnh hưởng, nguồn SRC-001. Mức tác động chưa đo, đã ghi là OQ-003. |
| 3 | Proposed outcome | Done | intent §2 mô tả kết quả cho người dùng (chỉ dựa trên tài liệu, có trích dẫn tài liệu + trang), không áp đặt giải pháp kỹ thuật. |
| 4 | Affected users | Done | intent §3: 3 nhóm và mức ảnh hưởng của từng nhóm; chi tiết STK-001..006 ở stakeholders.md. |
| 5 | Constraints | In Progress | intent §4 đủ ràng buộc về phạm vi, dữ liệu (OQ-006, ADR-003) và môi trường. Còn lỗi: ghi "Node 14", trong khi SRC-005 và ADR-009 đã nâng lên Node 22 LTS cho frontend Vue. Cần sửa intent §4 và ghi lịch sử phiên bản. |
| 6 | Success measures | In Progress | MET-001..003 có ID và target đề xuất. Cách đo có ở BRD §4 (công thức, nguồn dữ liệu). Thiếu baseline (OQ-003) và target chưa chốt (OQ-005); MET-002 chỉ mới đo trên bộ eval tổng hợp (DEP-002). |
| 7 | Out of scope | Done | intent §6 liệt kê các loại trừ, kể cả US-404 và US-601 bị hoãn. |
| 8 | Open questions | Done | intent §7 nêu các OQ chặn baseline. BRD §12 có đủ ID, người chịu trách nhiệm, hạn và trạng thái. |
| 9 | Named owner | In Progress | Owner mới ghi vai trò "Quản lý dự án (STK-001) — [chờ xác nhận tên]". SOP §5.1 yêu cầu một người cụ thể, nên chờ OQ-001. |
| 10 | Risk tier | Done | intent §8: Medium toàn hệ thống, High cho auth/phân quyền/dữ liệu tài liệu, mỗi tier kèm lý do và control tối thiểu (L3, test grounding). |
| 11 | Acceptance criteria | Done | intent §9 có 3 AC cho work item. Đã kiểm chứng: P0 xanh trong CI (xem [RTM](../07-verification/testing/RTM.md)), coverage ≥ 70%; AC-020 (IT ký) còn chờ. |
| 12 | Source registry | Done | sources.md: SRC-001..006 có chủ sở hữu, ngày/phiên bản, vị trí, độ tin cậy; có mục "Nguồn còn thiếu". |
| 13 | Approval | In Progress | intent §10 đã có bảng phê duyệt nhưng PO chưa ký (OQ-001). Agent không tự phê duyệt. |

**Tổng:** 8 Done · 4 In Progress · 0 Pending. Cổng Intake **chưa đóng**: còn thiếu tên owner và chữ ký PO (cả hai là việc của con người), và intent §4 cần sửa lỗi Node.

## Lịch sử audit
| Ngày | Thay đổi |
|---|---|
| 2026-11-02 | Lần audit đầu theo checklist Intake mới (bổ sung theo bản đồ 8 chặng). |
