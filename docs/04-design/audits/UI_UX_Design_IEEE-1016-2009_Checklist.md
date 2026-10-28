# Audit — UI/UX Design theo checklist

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/UI_UX_design/README.md, UIUX_Blueprint_Design.md, html_design/01..06 + index.html, blueprint.md §2.2–2.3, §3.7 |
| Checklist | docs/design/UI_UX_Design_IEEE-1016-2009_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | User Personas & Scenarios | Done | README bảng persona (Linh, Hùng, Mai) + UIUX_Blueprint §2; kịch bản UQ-01..UQ-10. |
| 3 | Information Architecture (IA) | Done | Bản đồ SCR-01..06 ↔ story ↔ API (README); UQ-08 mọi chức năng P0 trong ≤ 1 lần bấm từ màn hình chính. |
| 4 | Task Flows | Done | UIUX_Blueprint §3.6.1–3.6.3 (tải lên, hỏi đáp + trích dẫn, lỗi/hồi phục). |
| 5 | Grid System | Done | Token space.1..6 = 4/8/12/16/24/32 px, lưới 4 px (UIUX §3.8.1); CSS variables trong prototype. |
| 6 | Breakpoints | In Progress | Chỉ desktop (mobile ngoài phạm vi, UX-010). Mâu thuẫn: UIUX UQ-04 "từ 1024 px, dưới 1024 px thu ngăn kéo" và blueprint §2.3 / PRD §3.9.4 "tối thiểu 1280 px". Prototype không có @media theo độ rộng (chỉ prefers-reduced-motion). |
| 7 | Visual Hierarchy | Done | Wireframe SCR-02 (UIUX §3.5.2) và prototype 02_workspace.html: 2 vùng, nút chính màu primary, composer cố định đáy. |
| 8 | Design System / Components | In Progress | Có danh mục component + token, nhưng ID component UIUX §3.3.1 (CMP-01 UploadZone ... CMP-12 Banner) trùng không gian ID với thành phần backend trong elements.yaml (CMP-01 Web UI ... CMP-12 Admin CLI) — gây nhầm truy vết. Component chỉ tồn tại dạng CSS nhân bản trong từng file HTML, chưa có thư viện dùng chung. |
| 9 | Color Palette | Done | Token primary, text, text-muted, surface, bg, success, warning, danger, focus-ring (UIUX §3.8.1, index.html :root). |
| 10 | Typography | In Progress | Thang 16/14 px, line-height 1.5. Mâu thuẫn font: README D-2 chọn font hệ thống vì CSP, nhưng UIUX §3.8.1 vẫn ghi "Inter/Be Vietnam Pro" và cả 7 file html_design vẫn tải fonts.googleapis.com. |
| 11 | Iconography | In Progress | Biểu tượng luôn đi kèm chữ (UX-002), nhưng dùng emoji/Unicode (✔ ⚠ 🔒 ⬆ 👍) — hiển thị khác nhau theo hệ điều hành, không có bộ icon thống nhất nét/kích thước. |
| 12 | Contrast Ratios | Done | README WCAG 1.4.3: text #111827 trên trắng 16:1, primary #1D4ED8 6.7:1; UIUX §2.5 yêu cầu ≥ 4.5:1 và kiểm tra axe/Lighthouse. |
| 13 | Touch Targets | Done | Vùng chạm ≥ 44 px (blueprint §2.3, UIUX §2.5) dù mobile ngoài phạm vi. |
| 14 | Keyboard Navigation | Done | UX-009, README 2.1.1/2.4.7 (focus-visible 2 px, bẫy focus hộp thoại, Esc đóng), UQ-02 blueprint. |
| 15 | Error Prevention & Recovery | Done | SCR-04 ConfirmDialog trước khi xóa; giữ câu hỏi khi lỗi (UQ-06, EC-04, EC-15 qua sessionStorage). |
| 16 | System Status Visibility | Done | Trạng thái tài liệu + polling 2 s (D-5), "Đang trả lời…" (D-1), spinner ≤ 300 ms (UIUX §2.5). Thiếu EC-06 (thông báo chậm + Hủy) trong thiết kế v0.2 vì không có API hủy. |
| 17 | Empty States | Done | EC-01/EC-02 với CTA (UIUX §3.8.2, chuỗi chat.empty.*); dashboard có trạng thái "Chưa có dữ liệu" và "chưa có quyền". |
| 18 | Micro-interactions | Done | UQ-07 hover/focus/active/disabled; prototype có :hover, :active, :focus-visible, thuộc tính disabled. |
| 19 | Chart Clarity | Done | 05_usage_dashboard.html: biểu đồ cột SVG + chuyển sang bảng (aria-pressed), chọn phạm vi tuần. |
| 20 | Data Density | Done | Dashboard ít chỉ số, có chế độ bảng thay biểu đồ; danh sách tài liệu ≤ 50. |
| 21 | Asset Export | Pending | Không có danh sách asset (logo, icon) hay định dạng xuất SVG/PNG; icon là emoji. |
| 22 | Redlining & Specs | In Progress | Token dưới dạng CSS variables trong prototype; không có spec đo đạc (khoảng cách, kích thước từng component) hay Figma Dev Mode; token bị nhân bản trong từng file HTML. |
| 23 | State Documentation | In Progress | Có bảng trạng thái tài liệu, message, composer (UIUX §3.7). Nhưng trạng thái v0.1 chưa cập nhật theo v0.2: Message còn Streaming/Cancelled và outcome partial (API không có), tài liệu còn Uploading/Password/Error→Thử lại (API chỉ có processing/ready/failed/no_text và không có endpoint thử lại); prototype 02_workspace.html vẫn mô phỏng streaming; 01_login.html còn nút SSO. |

## Tóm tắt
Thiết kế UI/UX phong phú (persona, token, WCAG, empty/error state). Vấn đề lớn: tài liệu UIUX_Blueprint và prototype được tái sử dụng từ v0.1 nhưng chỉ có "bảng delta" trong README; nội dung gốc và prototype vẫn mâu thuẫn với v0.2 (streaming, SSO, Google Fonts, trạng thái Password/Uploading, nút Thử lại, partial). ID component trùng với CMP backend.
