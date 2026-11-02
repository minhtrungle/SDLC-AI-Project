# Audit — UI/UX Design theo checklist

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/UI_UX_design/README.md, UIUX_Blueprint_Design.md (banner "Đọc trước v0.2"), html_design/01..06 + index.html, blueprint.md §2.2–2.3, §3.7, §6; đối chiếu hiện thực app/frontend/src (styles.css, components/*.vue) |
| Checklist | docs/checklists/UI_UX_Design_IEEE-1016-2009_Checklist.xlsx |
| Reviewer | artifact-auditor (agent) — vòng 1: Independent reviewer agent (2026-10-28) |
| Ngày | 2026-11-02 |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d) và sau khi hiện thực app/frontend (1aba0aa) |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | User Personas & Scenarios | Done | README bảng persona (Linh, Hùng, Mai) + UIUX_Blueprint §2; kịch bản UQ-01..UQ-10. Không thay đổi sau REFINE. |
| 3 | Information Architecture (IA) | Done | README bản đồ SCR-01..06 ↔ story ↔ API; UQ-08 mọi chức năng P0 trong ≤ 1 lần bấm từ màn hình chính. |
| 4 | Task Flows | Done | UIUX_Blueprint §3.6.1–3.6.3 (tải lên, hỏi đáp + trích dẫn, lỗi/hồi phục); luồng nghiệp vụ chi tiết ở use_cases.md UC-02, UC-05, UC-06. |
| 5 | Grid System | Done | Token space.1..6 = 4/8/12/16/24/32 px, lưới 4 px (UIUX §3.8.1); cùng giá trị --space-1..6 trong app/frontend/src/styles.css. |
| 6 | Breakpoints | Done | DF-22: banner đầu UIUX_Blueprint chốt độ rộng tối thiểu 1280 px (PRD §3.9.4), không làm ngăn kéo 1024 px, mobile ngoài phạm vi (UX-010); banner có quyền ưu tiên khi mâu thuẫn. Hiện thực styles.css .workspace min-width 1024px nên không cuộn ngang ở ≥ 1280 px. Còn Minor: thân UIUX UQ-04/L-05 và @media (max-width:1023px) trong 02..04 html vẫn mô tả ngăn kéo <1024 px (nội dung v0.1, xem DF-03). |
| 7 | Visual Hierarchy | Done | Wireframe SCR-02 (UIUX §3.5.2), prototype 02_workspace.html và WorkspaceView.vue: 2 vùng, nút chính màu primary, composer cố định đáy. |
| 8 | Design System / Components | In Progress | Đã sửa DF-05: ID component UI đổi sang UIC-01..12 (UIUX §3.3.1, §4), không còn trùng CMP-xx; token có nguồn duy nhất ở app/frontend/src/styles.css. Còn thiếu: danh mục UIC-01..12 chưa đối chiếu với component đã hiện thực (DocumentPanel, AnswerMessage, CitationDrawer, ConfirmDialog, ChatPanel...), props còn của v0.1 (UIC-02 onRetry, UIC-04 onCancel/status streaming); prototype vẫn nhân bản CSS trong từng file. |
| 9 | Color Palette | Done | Token primary, text, text-muted, surface, bg, success, warning, danger, focus-ring (UIUX §3.8.1, index.html :root, styles.css :root cùng mã màu). |
| 10 | Typography | Done | DF-03/D-2: 7 file html_design không còn tải fonts.googleapis.com (grep = 0); banner UIUX chốt system stack; styles.css --font-family system-ui, Segoe UI, Roboto, Arial; thang 16/14 px, line-height 1.5. Minor: UIUX §3.8.1 vẫn ghi "Inter/Be Vietnam Pro" và prototype đặt "Inter" đầu stack (không tải, rơi về font hệ thống). |
| 11 | Iconography | In Progress | Biểu tượng luôn đi kèm chữ hoặc aria-label (UX-002; DocumentPanel.vue nút xóa aria-label). Chưa có bộ icon thống nhất: prototype và frontend vẫn dùng emoji/Unicode (✔ ⚠ 🔒 🗑 👍 👎 ☁ trong AnswerMessage.vue, AppHeader.vue, DocumentPanel.vue) nên hiển thị khác nhau theo hệ điều hành. Không có finding REFINE xử lý mục này. |
| 12 | Contrast Ratios | Done | README WCAG 1.4.3: text #111827 trên trắng 16:1, primary #1D4ED8 6.7:1; UIUX §2.5 yêu cầu ≥ 4.5:1 và kiểm tra axe/Lighthouse. |
| 13 | Touch Targets | Done | Vùng chạm ≥ 44 px (blueprint §2.3, UIUX §2.5); styles.css .btn min-height/min-width 44px. |
| 14 | Keyboard Navigation | Done | UX-009, README 2.1.1/2.4.7 (focus-visible 2 px, bẫy focus hộp thoại, Esc đóng), UQ-02; styles.css :focus-visible outline var(--focus-ring). |
| 15 | Error Prevention & Recovery | Done | SCR-04 ConfirmDialog trước khi xóa (ConfirmDialog.vue); giữ câu hỏi khi lỗi (UQ-06, EC-04, EC-15 qua sessionStorage, blueprint §6); trạng thái ô hỏi error "Gửi lại" ở blueprint §3.7. |
| 16 | System Status Visibility | Done | Trạng thái tài liệu + polling 2 s (D-5), "Đang trả lời…" (D-1, trạng thái sending blueprint §3.7), spinner ≤ 300 ms (UIUX §2.5). EC-06 đã có quyết định ở blueprint §6 (timeout 15 s → 503 + Gửi lại, nút Hủy hoãn tới khi bật LLM ngoài, owner Tech Lead). |
| 17 | Empty States | Done | EC-01/EC-02 với CTA (UIUX §3.8.2, chuỗi chat.empty.*); trạng thái disabled_empty/disabled_no_ready ở blueprint §3.7; dashboard có "Chưa có dữ liệu" và "chưa có quyền". |
| 18 | Micro-interactions | Done | UQ-07 hover/focus/active/disabled; prototype và styles.css có :hover, :focus-visible, [disabled], prefers-reduced-motion. |
| 19 | Chart Clarity | Done | 05_usage_dashboard.html: biểu đồ cột SVG + chuyển sang bảng (aria-pressed), chọn phạm vi tuần; UsageDashboard.vue hiện thực bảng 8 tuần + thanh .bar. |
| 20 | Data Density | Done | Dashboard ít chỉ số, có chế độ bảng thay biểu đồ; danh sách tài liệu ≤ 50 (CWD_MAX_DOCS). |
| 21 | Asset Export | Pending | Vẫn không có danh sách asset (logo, favicon, icon) hay quy định định dạng xuất SVG/PNG; icon là emoji, app/frontend không có thư mục public/ asset. Nếu nhóm quyết định MVP không dùng asset hình ảnh thì cần ghi quyết định đó để chuyển N/A. |
| 22 | Redlining & Specs | In Progress | Token giờ có một nguồn trong app/frontend/src/styles.css (radius, space, shadow, màu). Vẫn không có spec đo đạc theo từng component (khoảng cách, kích thước, trạng thái) hay Figma Dev Mode; prototype vẫn nhân bản token trong từng file HTML. |
| 23 | State Documentation | In Progress | Đã có nguồn chuẩn: blueprint §3.7 sơ đồ trạng thái tài liệu (processing/ready/no_text/failed) và bảng trạng thái ô hỏi (DF-04); banner UIUX tuyên bố bỏ streaming, cancelled, partial, Uploading/Password, nút Thử lại. Còn lại (DF-03 Partial, owner UX): thân UIUX §3.4 Message/Document và §3.7 vẫn là trạng thái v0.1; 02/03/04 html vẫn mô phỏng status streaming (dòng 417, 504); index.html tile SCR-01 vẫn ghi "Đăng nhập / SSO"; chưa có bảng trạng thái Message của v0.2 (sending/done/error, outcome answered/not_found). |

## Kiểm tra lại vòng trước
- DF-03 (Google Fonts, SSO, streaming): Google Fonts đã gỡ khỏi cả 7 file; nút SSO đã gỡ khỏi 01_login.html nhưng mô tả tile ở index.html còn "SSO"; streaming vẫn còn trong JS prototype 02..04 — Partial, khớp design-refine-log.
- DF-05 (ID CMP trùng): đã sửa, UIUX_Blueprint dùng UIC-01..12, 0 lần CMP- cho component UI.
- DF-22 (1024 vs 1280): đã chốt 1280 px qua banner; thân tài liệu chưa viết lại.
- DF-04 (tên trạng thái ô hỏi): bảng chuẩn duy nhất ở blueprint §3.7.

## Phát hiện
| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-UIUX-01 | Major | UIUX_Blueprint §3.4, §3.7; html_design/02..04 | Nội dung v0.1 (streaming, cancelled, partial, Uploading/Password) vẫn trong thân tài liệu và prototype; chỉ banner ghi đè (DF-03 Partial). | Viết lại toàn văn UIUX lên v0.2 trước baseline; bỏ mô phỏng streaming trong prototype; sửa tile SCR-01 ở index.html. |
| AUD-UIUX-02 | Minor | UIUX §3.3.1 | Danh mục UIC-01..12 không ánh xạ tới component Vue đã hiện thực, props v0.1. | Thêm cột "Hiện thực" (tên file .vue) và cập nhật props. |
| AUD-UIUX-03 | Minor | prototype, AnswerMessage.vue, AppHeader.vue, DocumentPanel.vue | Icon emoji không đồng nhất theo hệ điều hành. | Chọn bộ icon SVG nội tuyến (tương thích CSP self) hoặc ghi quyết định giữ emoji. |
| AUD-UIUX-04 | Minor | Toàn bộ UI_UX_design | Không có danh sách asset/định dạng xuất, không có redline spec. | Bổ sung mục asset (hoặc quyết định N/A) và bảng spec kích thước cho UIC chính. |

## Tóm tắt
- Status: Done 17 · In Progress 4 · Pending 1 · N/A 0 (tổng 22 dòng).
- Phát hiện: Critical 0 · Major 1 · Minor 3.
- Nhận định: Cần sửa — các quyết định v0.2 đã được chốt qua banner và hiện thực frontend đúng hướng, nhưng thân UIUX_Blueprint và prototype còn mâu thuẫn trạng thái v0.1 (DF-03 Partial) phải viết lại trước khi baseline.

## Lịch sử audit
| Vòng | Ngày | Dòng | Thay đổi | Lý do |
|---|---|---|---|---|
| 1 | 2026-10-28 | — | Audit ban đầu: Done 15 · In Progress 6 · Pending 1 | Trước REFINE e1c8a1d |
| 2 | 2026-11-02 | 6 Breakpoints | In Progress → Done | DF-22: banner chốt 1280 px, mobile ngoài phạm vi; frontend không cuộn ngang ≥ 1280 px |
| 2 | 2026-11-02 | 10 Typography | In Progress → Done | DF-03: gỡ Google Fonts khỏi 7 file prototype; system stack ở banner và styles.css |
| 2 | 2026-11-02 | 8, 11, 16, 21, 22, 23 | Giữ nguyên, cập nhật Notes | 8: DF-05 đã sửa nhưng catalog chưa khớp component thật; 11, 21, 22: chưa được xử lý; 16: thêm quyết định EC-06; 23: DF-03 Partial |
