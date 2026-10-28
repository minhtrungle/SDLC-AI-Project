# Audit — Use Case theo checklist UML 2.0 (v2)

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/use_case_diagram.drawio (UC-01..UC-13); đối chiếu docs/03-analysis/USER_STORIES.md và SAD §6 |
| Checklist | docs/checklists/UseCase_Document_UML2.0_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

Lưu ý: Phase 4 **không có tài liệu đặc tả use case** (không file nào chứa UC-01..UC-13 dạng văn bản; grep "UC-0" trong docs/*.md = 0 kết quả). Chỉ có sơ đồ use case và user story Given/When/Then. Các mục về đặc tả được chấm dựa trên những gì tồn tại.

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Use Case ID | Done | UC-01..UC-13 trong use_case_diagram.drawio. |
| 3 | Use Case Name | Done | Cụm động từ: "Đăng nhập / đăng xuất", "Tải lên PDF", "Đặt câu hỏi", "Đánh giá câu trả lời". UC-13 "Sinh câu trả lời bằng LLM ngoài" là hành vi hệ thống, không phải mục tiêu actor. |
| 4 | Description | Pending | Không có mô tả 1–2 câu cho từng UC; chỉ có nhãn + US-xx. |
| 5 | Version & Date | Pending | Sơ đồ không có phiên bản/ngày; không có tài liệu UC. |
| 6 | Author & Stakeholders | Pending | Không ghi tác giả, người duyệt cho UC. |
| 7 | Status | Pending | Không có trạng thái Draft/Review/Approved cho UC. |
| 8 | Primary Actor | Done | ACT-01 nối UC-01..09, ACT-02 nối UC-10 (kế thừa ACT-01), ACT-03 nối UC-11. |
| 9 | Secondary Actors | Done | ACT-04 Anthropic API nối UC-13. |
| 10 | System Boundary | Done | Hình chữ nhật "Hệ thống Chat với tài liệu" bao các UC; actor nằm ngoài. |
| 11 | Trigger | Pending | Không có trigger cho từng UC. |
| 12 | Pre-conditions | In Progress | Chỉ ngầm qua mệnh đề Given trong USER_STORIES (vd. AC-301.1 "Có ≥ 1 tài liệu ready"); chưa gắn theo UC. |
| 13 | Post-conditions (Success) | In Progress | Ngầm qua mệnh đề Then trong AC; SAD §6.1 bước 9 cho UC-05. |
| 14 | Post-conditions (Failure) | In Progress | Chỉ có mã lỗi rời rạc (SAD §6.1 cột Quy tắc, openapi.md §3); không mô tả trạng thái hệ thống khi thất bại (vd. upload lỗi giữa chừng: file đã lưu chưa?). |
| 15 | Main Success Scenario | In Progress | Chỉ UC-05 có bước đánh số (SAD §6.1 bước 1–9) và UC-02 (SAD §6.2 văn xuôi); các UC khác không có. |
| 16 | Action/Response Format | In Progress | SAD §6.1 có cột Thành phần nhưng là component, không phải "Actor làm / Hệ thống đáp". |
| 17 | Alternate Flows | Pending | Không có luồng thay thế được đặc tả (vd. hỏi có phạm vi, đổi đánh giá). |
| 18 | Exception Flows | In Progress | Mã lỗi có trong SAD §6.1 (401/403/404/409/422) và activity diagram (file.wrong_type...), nhưng chưa thành luồng ngoại lệ theo UC; thiếu 503 chat.ai_unavailable trong luồng. |
| 19 | Flow References | Pending | Không có tham chiếu bước rẽ nhánh. |
| 20 | Association | Done | Đường liền actor–UC (endArrow=none). |
| 21 | Include (<<include>>) | Done | UC-05 «include» UC-12, nét đứt mũi tên mở từ base tới included. |
| 22 | Extend (<<extend>>) | In Progress | UC-07 và UC-13 «extend» UC-05, hướng đúng (từ extension tới base), UC-13 có điều kiện. Thiếu extension point khai báo trong UC-05. UC-07 gộp hai chức năng khác nhau (hỏi tiếp và giới hạn phạm vi). |
| 23 | Generalization | Done | ACT-02 → ACT-01 bằng mũi tên tam giác rỗng (endArrow=block, endFill=0). |
| 24 | Business Rules | In Progress | Có trong FR (giới hạn 2000 ký tự, 20 MB, 50 tài liệu, ngưỡng 0.6) và ADR nhưng không gắn vào UC. |
| 25 | Non-Functional Requirements | In Progress | NFR có trong PRD §3.9.2, chỉ UC-05 ghi US-306; không UC nào ghi NFR liên quan. |
| 26 | Data Requirements | In Progress | Trường dữ liệu có trong openapi.yaml schema, chưa gắn theo UC. |
| 27 | No UI specifics | Done | Nhãn UC mô tả mục tiêu, không mô tả giao diện. |
| 28 | No Technical Jargon | In Progress | Nhãn chứa thuật ngữ kỹ thuật: "FR-010..013", "CWD_ALLOW_EXTERNAL_AI=true", "LLM", "CLI". |
| 29 | Assumptions Listed | Pending | Không có giả định theo UC (ASM chỉ ở BRD/PRD). |
| 30 | Open Issues | Pending | Không có danh sách vấn đề mở theo UC (vd. EC-12 trùng tên, US-404, US-601 hoãn không thể hiện trên sơ đồ). |

## Tóm tắt
Sơ đồ use case đúng ký hiệu UML (association, include, extend, generalization, boundary). Tuy nhiên checklist này đánh giá **tài liệu** use case và Phase 4 không có đặc tả UC dạng văn bản — đa số mục metadata/flows ở trạng thái Pending hoặc In Progress. Đề xuất: thêm docs/04-design/use_cases.md với template UC (ID, mô tả, actor, trigger, pre/post, main/alt/exception flow tham chiếu bước, quy tắc, NFR, dữ liệu, giả định, vấn đề mở), ít nhất cho UC-01, 02, 04, 05, 09, 10.
