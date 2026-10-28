# Stakeholders — Chat với tài liệu

| ID | Bên liên quan | Vai trò trong dự án | Concern chính | Ảnh hưởng | Vai trò phê duyệt |
|---|---|---|---|---|---|
| STK-001 | Quản lý dự án | Sponsor, Product Owner (tạm thời) | MVP chứng minh được giá trị, đúng tiến độ, đo được hiệu quả | Cao | Duyệt intent, BRD, PRD, PLAN |
| STK-002 | Đội phát triển kinh doanh | Người dùng cuối | Tìm thông tin nhanh, chính xác, kiểm chứng được nguồn | Cao | UAT, bộ câu hỏi chuẩn |
| STK-003 | Đội BA | Quản lý yêu cầu | Yêu cầu rõ ràng, truy vết được | Trung bình | Review BRD/PRD |
| STK-004 | Đội kỹ thuật (Tech Lead, Dev) | Xây dựng, vận hành | Phạm vi khả thi, stack phù hợp năng lực | Trung bình | Duyệt SAD, ADR, PLAN, code review |
| STK-005 | IT / Bảo mật | Bảo vệ dữ liệu, **có thể chặn go-live** | Tài liệu không bị lộ; dữ liệu không gửi ra ngoài khi chưa được phép | Cao | Ký AC-020, review L3 |
| STK-006 | QA | Kiểm thử, nghiệm thu | Test plan, bộ câu hỏi chuẩn, launch gate | Trung bình | Ký test report |
| STK-007 | Agent AI (Claude) | Sinh bản nháp tài liệu, code, test; audit theo checklist | — | — | **Không có quyền phê duyệt, merge hay deploy** |

## Ma trận RACI theo phase

| Phase | Agent | PO (STK-001) | Tech Lead (STK-004) | IT/Bảo mật (STK-005) | QA (STK-006) |
|---|---|---|---|---|---|
| 1 Intake | R | A | C | C | I |
| 2 Requirements | R | A | C | C | I |
| 3 Analysis | R | A | A | C | C |
| 4 Design | R | I | A | C | C |
| 5 Planning | R | A | A | I | C |
| 6 Build | R | I | A | I | C |
| 7 Verify | R (L0, L1) | I | C | C | A |
| 8 Review | — | I | A (L2) | A (L3 cho auth/data) | C |
| 9 Release | R (chuẩn bị) | A | C | C | C |

R = thực hiện, A = phê duyệt/chịu trách nhiệm, C = tham vấn, I = được thông báo.
