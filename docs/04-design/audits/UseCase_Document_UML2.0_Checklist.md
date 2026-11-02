# Audit — Use Case theo checklist UML 2.0 (v2)

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/use_cases.md (đặc tả UC-01..06, 09..13, thêm theo DF-08) + docs/04-design/diagrams/use_case_diagram.drawio (UC-01..UC-13, không đổi từ e1c8a1d); đối chiếu docs/03-analysis/USER_STORIES.md, SAD §6, blueprint §3.9 |
| Checklist | docs/checklists/UseCase_Document_UML2.0_Checklist.xlsx |
| Reviewer | artifact-auditor (agent) — vòng 1: Independent reviewer agent (2026-10-28) |
| Ngày | 2026-11-02 |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d) |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Use Case ID | Done | UC-01..UC-13 trong use_case_diagram.drawio (cell c7..c19); use_cases.md dùng cùng ID ở tiêu đề mục. |
| 3 | Use Case Name | Done | Cụm động từ: "Đăng nhập / đăng xuất", "Tải lên PDF", "Đặt câu hỏi", "Đánh giá câu trả lời". Minor: UC-13 "Sinh câu trả lời bằng LLM ngoài" là hành vi hệ thống, không phải mục tiêu actor. |
| 4 | Description | In Progress | use_cases.md không có trường Mô tả 1–2 câu cho từng UC; chỉ có tiêu đề + Story/FR + luồng. Riêng mục UC-12/UC-13 có đoạn văn mô tả ngắn. |
| 5 | Version & Date | Pending | use_cases.md và sơ đồ không có phiên bản/ngày (header chỉ ghi "Bổ sung theo finding DF-08"). |
| 6 | Author & Stakeholders | Pending | Không ghi tác giả, người duyệt cho tài liệu UC hay từng UC. |
| 7 | Status | Pending | Không có trạng thái Draft/Review/Approved cho tài liệu UC hay từng UC. |
| 8 | Primary Actor | Done | Sơ đồ: ACT-01 nối UC-01..09, ACT-02 nối UC-10 (kế thừa ACT-01), ACT-03 nối UC-11; use_cases.md ghi Actor cho UC-01, UC-02, UC-10, UC-11. |
| 9 | Secondary Actors | Done | ACT-04 Anthropic API nối UC-13 (cell c35); use_cases.md UC-13 điều kiện CWD_ALLOW_EXTERNAL_AI + API key. |
| 10 | System Boundary | Done | Hình chữ nhật "Hệ thống Chat với tài liệu" (c6) bao các UC; actor nằm ngoài. |
| 11 | Trigger | In Progress | Có Trigger cho UC-01 ("Mở ứng dụng khi chưa có phiên") và UC-02 ("Bấm + Tải lên PDF hoặc kéo-thả"); UC-03..06, 09, 10 chỉ suy ra từ bước 1 của luồng chính, không có trường Trigger. |
| 12 | Pre-conditions | Done | Tiền điều kiện chung ở đầu use_cases.md (đã đăng nhập, phiên còn hạn, 401 → SCR-06); riêng UC-01 (tài khoản do UC-11 tạo), UC-05 (≥ 1 tài liệu ready trong phạm vi). Minor: UC-06/UC-09 chưa ghi "đã có câu trả lời". |
| 13 | Post-conditions (Success) | In Progress | Có cho UC-01 (phiên, cookie, auth.login_success), UC-02 (processing, file, document.upload), UC-04 (BRU-004, trích dẫn "đã bị xóa"); UC-05 chỉ ngầm qua bước 7; UC-03, 06, 09, 10 không có. |
| 14 | Post-conditions (Failure) | In Progress | Một phần: UC-05 5a "không lưu lượt; UI giữ câu hỏi", UC-02 "các file khác không bị ảnh hưởng", UC-03 3c xử lý lại khi khởi động. Chưa có trường hậu điều kiện thất bại riêng; UC-01, 04, 09 không mô tả trạng thái hệ thống khi thất bại. |
| 15 | Main Success Scenario | In Progress | Luồng chính đánh số cho UC-01..06, 09, 10; UC-11 liệt kê lệnh; UC-12/13 tham chiếu SAD §6.1, blueprint §3.9. Thiếu hoàn toàn đặc tả UC-07 (Hỏi tiếp / giới hạn phạm vi, US-401/402, P1) và UC-08 (Xem lại hội thoại, US-403, P1) dù thuộc phạm vi MVP. |
| 16 | Action/Response Format | Done | Các bước xen kẽ "Người dùng …" / "Hệ thống …" / "UI …" (UC-01 bước 2–6, UC-02, UC-04, UC-05 bước 1–8). |
| 17 | Alternate Flows | In Progress | Có luồng thay thế UC-01 6a (đăng xuất), UC-04 3a (Hủy/Esc), UC-05 4a/6a/7a (not_found, docs_processing). Chưa có luồng hỏi có phạm vi / hỏi tiếp (UC-07 không có đặc tả) và xem lại hội thoại (UC-08). |
| 18 | Exception Flows | Done | Ngoại lệ đánh số cho UC-01 (3a 429, 4a 401), UC-02 (3a–3c, 2a), UC-03 (3a–3c), UC-05 (3a 422, 3b 409, 5a 503 chat.ai_unavailable), UC-06 2a, UC-09 3a, UC-10 2a 403. |
| 19 | Flow References | Done | Luồng thay thế/ngoại lệ tham chiếu số bước của luồng chính theo dạng 3a, 4a, 6a (vd. UC-05 3a/4a/5a/6a/7a, UC-02 2a/3a). |
| 20 | Association | Done | Đường liền actor–UC (endArrow=none, c20..c31, c35). |
| 21 | Include (<<include>>) | Done | UC-05 «include» UC-12 (c32), nét đứt mũi tên mở từ base tới included; use_cases.md UC-05 bước 4 gọi UC-12. |
| 22 | Extend (<<extend>>) | In Progress | UC-07 (c33) và UC-13 (c34, điều kiện [CWD_ALLOW_EXTERNAL_AI=true]) «extend» UC-05, hướng đúng. Vẫn thiếu extension point khai báo trong UC-05 (cả sơ đồ lẫn use_cases.md); UC-07 vẫn gộp hai chức năng (hỏi tiếp và giới hạn phạm vi). |
| 23 | Generalization | Done | ACT-02 → ACT-01 bằng mũi tên tam giác rỗng (c29 endArrow=block, endFill=0). |
| 24 | Business Rules | Done | Trường Quy tắc: UC-01 (BR-019, phiên 8 giờ), UC-02 (BRU-001, BRU-002), UC-05 (BR-009..011, BRU-003); UC-04 BRU-004; giới hạn 2000 ký tự (UC-05 3a), 500 ký tự (UC-09). |
| 25 | Non-Functional Requirements | Done | Trường NFR: UC-01 NFR-010, UC-05 NFR-001/002/003, UC-11 NFR-006/007; UC liên quan hiệu năng/bảo mật đều có NFR. |
| 26 | Data Requirements | In Progress | Có nhắc thực thể/trường rải rác (sessions, documents status, page, đoạn trích, lý do ≤ 500 ký tự) nhưng không có danh sách dữ liệu vào/ra theo UC; chi tiết vẫn chỉ ở openapi.yaml. |
| 27 | No UI specifics | In Progress | Hồi quy so với vòng 1 (trước đây chỉ chấm nhãn sơ đồ): use_cases.md luồng chứa chi tiết giao diện — "Bấm 🗑" (UC-04), "SCR-01/SCR-02/SCR-04/SCR-03", "Enter" (UC-05), "Panel SCR-03", "aria-pressed" (UC-09), "biểu tượng + chữ" (UC-03). |
| 28 | No Technical Jargon | In Progress | Sơ đồ vẫn có "FR-010..013", "CWD_ALLOW_EXTERNAL_AI=true", "LLM", "CLI"; use_cases.md thêm "HttpOnly; SameSite=Strict", "getChunk", mã HTTP 401/409/422/503, câu lệnh sqlite3 (UC-11). |
| 29 | Assumptions Listed | Pending | use_cases.md không có mục giả định theo UC (ASM chỉ ở BRD/PRD). |
| 30 | Open Issues | Pending | Không có danh sách vấn đề mở theo UC; các quyết định hoãn liên quan (EC-06 nút Hủy, EC-12 trùng tên, US-404/US-601) chỉ ở blueprint §6 và USER_STORIES, không được nêu trong use_cases.md. |

## Kiểm tra lại vòng trước
- Khuyến nghị vòng 1 "thêm docs/04-design/use_cases.md": đã làm theo DF-08, cho UC-01..06, 09..13. Thiếu UC-07, UC-08 (vòng 1 đề xuất tối thiểu UC-01, 02, 04, 05, 09, 10 — đã đủ).
- Thiếu 503 chat.ai_unavailable trong luồng: đã có ở UC-05 5a.
- Extension point UC-05, UC-07 gộp chức năng, thuật ngữ kỹ thuật trên nhãn sơ đồ: chưa sửa (sơ đồ không đổi kể từ e1c8a1d).

## Phát hiện
| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-UC-01 | Major | use_cases.md | Không có đặc tả UC-07 và UC-08 dù US-401..403 là P1 trong phạm vi MVP. | Bổ sung hai mục UC-07 (tách hỏi tiếp và phạm vi nếu cần) và UC-08 theo cùng mẫu. |
| AUD-UC-02 | Minor | use_cases.md header | Không có phiên bản, ngày, tác giả, người duyệt, trạng thái. | Thêm khối metadata tài liệu. |
| AUD-UC-03 | Minor | use_cases.md UC-04, UC-05, UC-06, UC-09 | Luồng chứa chi tiết UI (SCR-xx, 🗑, Enter, aria-pressed) và thuật ngữ kỹ thuật. | Diễn đạt theo mục tiêu; chuyển chi tiết UI sang UIUX/blueprint. |
| AUD-UC-04 | Minor | use_case_diagram.drawio c11, c13; use_cases.md UC-05 | Chưa khai báo extension point; UC-07 gộp hai mục tiêu. | Thêm extension point "sau khi nhập câu hỏi" và "khi sinh câu trả lời" vào UC-05. |
| AUD-UC-05 | Minor | use_cases.md | Thiếu trường Mô tả, Trigger, Hậu điều kiện, Dữ liệu, Giả định, Vấn đề mở ở đa số UC. | Bổ sung các trường còn thiếu vào mẫu bảng mỗi UC. |

## Tóm tắt
- Status: Done 14 · In Progress 10 · Pending 5 · N/A 0 (tổng 29 dòng).
- Phát hiện: Critical 0 · Major 1 · Minor 4.
- Nhận định: Cần sửa — use_cases.md đã lấp phần lớn khoảng trống luồng/ngoại lệ/quy tắc, nhưng thiếu UC-07/UC-08 và metadata tài liệu.

## Lịch sử audit
| Vòng | Ngày | Dòng | Thay đổi | Lý do |
|---|---|---|---|---|
| 1 | 2026-10-28 | — | Audit ban đầu: Done 9 · In Progress 11 · Pending 9 | Trước REFINE e1c8a1d, chưa có use_cases.md |
| 2 | 2026-11-02 | 4 Description | Pending → In Progress | use_cases.md có tiêu đề + Story/FR + mô tả cho UC-12/13, chưa có trường Mô tả |
| 2 | 2026-11-02 | 11 Trigger | Pending → In Progress | Trigger cho UC-01, UC-02 |
| 2 | 2026-11-02 | 12 Pre-conditions | In Progress → Done | Tiền điều kiện chung + UC-01, UC-05 |
| 2 | 2026-11-02 | 16 Action/Response Format | In Progress → Done | Bước xen kẽ Người dùng / Hệ thống |
| 2 | 2026-11-02 | 17 Alternate Flows | Pending → In Progress | Có cho UC-01, 04, 05; thiếu UC-07/08 |
| 2 | 2026-11-02 | 18 Exception Flows | In Progress → Done | Ngoại lệ đánh số theo UC, có 503 |
| 2 | 2026-11-02 | 19 Flow References | Pending → Done | Tham chiếu dạng 3a, 4a |
| 2 | 2026-11-02 | 24 Business Rules | In Progress → Done | Trường Quy tắc gắn theo UC |
| 2 | 2026-11-02 | 25 Non-Functional Requirements | In Progress → Done | Trường NFR gắn theo UC |
| 2 | 2026-11-02 | 27 No UI specifics | Done → In Progress | use_cases.md mới chứa chi tiết UI (hồi quy) |
| 2 | 2026-11-02 | 13, 14, 15, 22, 26, 28 | Giữ In Progress, cập nhật Notes | Cải thiện một phần; 15 thiếu UC-07/08; 22 sơ đồ không đổi |
