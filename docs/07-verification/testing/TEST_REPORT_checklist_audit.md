# Audit — Test Report theo IEEE 829 + evidence log

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | [TEST_REPORT.md](TEST_REPORT.md) v1.2, [RTM.md](RTM.md), [evidence/RUN-20261102-25eb89f](../evidence/RUN-20261102-25eb89f/README.md), [test_reports/](../../../test_reports/report.md) |
| Checklist | [Test_Report_IEEE_829_Evidence_Checklist.xlsx](../../checklists/Test_Report_IEEE_829_Evidence_Checklist.xlsx) |
| Bản đã điền | [Test_Report_IEEE_829_Evidence_Checklist_filled.xlsx](Test_Report_IEEE_829_Evidence_Checklist_filled.xlsx) |
| Reviewer | Agent (Claude). Đây là kết quả tự kiểm tra; QA (STK-006) phải review độc lập. |
| Ngày | 2026-11-02 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Report Identifier | Done | TSR-CWD-001 v1.2, tham chiếu CWD-MTP-v2.0, TEST_CASES và RTM; có mục Lịch sử phiên bản. |
| 3 | Summary | Done | §1: bảng kết quả theo từng hạng mục, mỗi dòng có link bằng chứng của RUN-20261102-25eb89f; có kết luận NO-GO và lý do. |
| 4 | Variances | Done | §2: V-1..V-3 kèm lý do. |
| 5 | Comprehensiveness Assessment | Done | §3: từng mức test ghi rõ đã làm gì, chưa làm gì và vì sao. |
| 6 | Summary of Results | Done | §4: kết quả theo story và theo spec E2E; RTM chi tiết từng AC (57 PASS, 1 chờ review, 0 GAP). |
| 7 | Evaluation | Done | §7 đánh giá theo tiêu chí pass/fail; rủi ro còn lại ở §6 (R-01, R-EV, R-LLM, R-L3), mỗi rủi ro có owner. |
| 8 | Summary of Activities | Done | §8: thời lượng của từng hoạt động, cập nhật theo lần chạy 2026-11-02. |
| 9 | Approvals | In Progress | §9 đã có bảng ký cho QA và Tech Lead nhưng chưa ai ký. Agent không tự phê duyệt. Owner: QA, Tech Lead. |
| 10 | Run pinned | Done | evidence README ghi run-id, commit `25eb89f`, nhánh, OS, Python 3.15.2, Node 22.23.4 và lệnh tái lập. |
| 11 | Openable evidence | Done | Mọi kết quả trỏ tới file có trong repo: ci-log, JUnit BE/FE, eval-report.json, test_reports/<test>/ (ảnh, mp4). DEF-002: link `../eval/eval-report.json` cũ trong TEST_PLAN chưa được thay. |
| 12 | AC coverage via RTM | Done | RTM: 58/58 AC đều có case. 57 PASS có bằng chứng; AC-102.3 ghi "PENDING REVIEW", owner IT/Bảo mật. |
| 13 | NFR measured | In Progress | Đã đo NFR-001/002 (eval tổng hợp), NFR-003, -004, -006, -007, -008, -010. Chưa đo: NFR-005 (khả dụng 99%, cần môi trường prod), NFR-009 (inspection WCAG thủ công), và NFR-002 trên bộ câu hỏi thật DEP-002. Owner: QA. |
| 14 | Defects logged | Done | §5: DF-01, T05-1, CR, NR, E2E-1/2 kèm trạng thái và test chứng minh; thêm DEF-001, DEF-002 ở trạng thái Open, có owner. |
| 15 | Skips justified | Done | Lần chạy không có test bị skip (E2E 0 bỏ qua). Phần không chạy (trình duyệt khác Chrome, LLM ngoài, test tải) có lý do ở §3. |
| 16 | GO/NO-GO | Done | Khuyến nghị NO-GO, vì DEF-001 và còn chờ review L2/L3 của con người. |

**Tổng:** 14 Done · 2 In Progress · 0 Pending · 0 Fail.

## Lịch sử audit
| Ngày | Thay đổi |
|---|---|
| 2026-11-02 | Lần audit đầu theo checklist Test Report mới (bổ sung theo bản đồ 8 chặng). |
