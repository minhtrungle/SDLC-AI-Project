# Audit — Planning theo checklist task DoD + traceability

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | [PLAN.md](PLAN.md), [tasks/T-01..T-10](tasks/), commit T-01..T-10, [traceability.md](../03-analysis/traceability.md), [RTM.md](../07-verification/testing/RTM.md) |
| Checklist | [Planning_Task_DoD_Traceability_Checklist.xlsx](../checklists/Planning_Task_DoD_Traceability_Checklist.xlsx) |
| Bản đã điền | [Planning_Task_DoD_Traceability_Checklist_filled.xlsx](Planning_Task_DoD_Traceability_Checklist_filled.xlsx) |
| Bằng chứng chạy | [RUN-20261102-25eb89f](../07-verification/evidence/RUN-20261102-25eb89f/README.md) |
| Reviewer | Agent (Claude). Đây là kết quả tự kiểm tra; Tech Lead phải review độc lập. |
| Ngày | 2026-11-02 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Inputs referenced | Done | Đầu PLAN dẫn SAD v0.2, USER_STORIES và elements.yaml. |
| 3 | Vertical slices | Done | PLAN §1 nêu nguyên tắc DB → API → UI → test; mỗi task T-01..T-09 là một lát dọc có test riêng. |
| 4 | Sequencing & critical path | Done | PLAN §2 có cột Phụ thuộc, sơ đồ mermaid và đường găng T-01 → T-02 → T-03 → T-04 → T-05 → T-08. |
| 5 | Estimates & owners | In Progress | Task nào cũng có ước lượng và risk tier. Owner người mới ghi chung chung là "Dev owner (người)", chưa có tên (PR-05). Owner: PO. |
| 6 | Mandatory fields | Done | Mỗi task card có bảng Story/FR, Phụ thuộc, Risk tier, Owner, Trạng thái. |
| 7 | Target acceptance criteria | Done | T-01..T-09 có mục "Tiêu chí hoàn thành (AC đích)"; T-10 có "Tiêu chí hoàn thành". |
| 8 | Tests first | Done | T-01..T-09 có mục "Test (viết trước)" kèm tên file test. Docstring của test mang ID AC (xem RTM §3). |
| 9 | Files to touch | Done | Mọi task card có mục "File chạm". |
| 10 | Task size | In Progress | PLAN §1 đặt giới hạn ≤ ~400 dòng diff. Thực tế vượt: T-01 `ad96030` +801, T-02 `bb545e5` +945, và commit `1aba0aa` (T-10 + sửa review) +10 489 / 103 file. Owner: Tech Lead. |
| 11 | DoD defined | Done | PLAN §3 có 5 điều kiện DoD đo được; task card nào cũng tham chiếu tới đó. |
| 12 | DoD met with evidence | In Progress | RTM: 57/58 AC PASS, 0 GAP; pytest 138/138 (97,73%), Vitest 49/49, Playwright 20/20. Cổng L0 chỉ đạt 16/17 vì DEF-001 (3 CVE của `pypdf 6.21.3`). DoD #2 chưa đạt cho tới khi nâng phiên bản. Owner: Tech Lead. |
| 13 | Task status current | In Progress | Trước lần audit này, T-01..T-09 còn ghi "Planned" và chưa tick AC nào dù đã có commit. Nay đã cập nhật trạng thái và tick các AC đã PASS theo RTM; trạng thái cuối "Done" vẫn chờ review L2 của con người. Owner: Dev owner. |
| 14 | Commit convention | In Progress | T-01..T-09 dùng Conventional Commits và có `Refs:`. Commit `1aba0aa` "chore: implement and testing" (gồm T-10) không theo quy ước, không có `Refs:` và gộp nhiều thay đổi. Owner: Dev owner. |
| 15 | Story → task coverage | Done | Mọi story P0/P1 nằm trong PLAN §2; NFR-001..008 thuộc T-08/T-09. P2 (US-404, US-601) hoãn có quyết định PD-05. |
| 16 | Task → requirement links | Done | Mỗi task gắn với US/FR/NFR; riêng T-10 gắn với ADR-009. |
| 17 | Traceability matrix updated | Done | `tools/trace_matrix.py` PASS trong cổng L0 (không hàng nào thiếu test); RTM liên kết thêm TC và bằng chứng. |
| 18 | Risks, unknowns, gaps | Done | PLAN §5: PR-01..05 có tác động, cách xử lý và owner. |
| 19 | Approvals | In Progress | Bảng phê duyệt PLAN §6 của PO và Tech Lead chưa ký. Agent không tự phê duyệt. Owner: PO, Tech Lead. |

**Tổng:** 12 Done · 6 In Progress · 0 Pending · 0 Fail.

## Lịch sử audit
| Ngày | Thay đổi |
|---|---|
| 2026-11-02 | Lần audit đầu theo checklist Planning mới (bổ sung theo bản đồ 8 chặng). |
