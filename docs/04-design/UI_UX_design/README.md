# UI/UX Design — Chat với tài liệu (MVP)

> **Prompt:** [UI-UX-Design_prompt.md](../../prompts/UI-UX-Design_prompt.md) · **Checklist:** [UI_UX_Design_IEEE-1016-2009_Checklist.xlsx](../../design/UI_UX_Design_IEEE-1016-2009_Checklist.xlsx)

| Artifact | Mô tả | Nguồn |
|---|---|---|
| [UIUX_Blueprint_Design.md](UIUX_Blueprint_Design.md) | SDD UI/UX theo IEEE 1016: persona, kịch bản chất lượng UX, 8 design view, design token | Tái sử dụng v0.1 (commit `373616a`), áp dụng delta bên dưới |
| [html_design/](html_design/index.html) | 6 prototype HTML tương tác SCR-01..SCR-06 | Tái sử dụng v0.1 |
| `app/web/` | Giao diện thật, hiện thực từ prototype (ADR-006) | Phase 6 |

## Persona (tóm tắt — đầy đủ ở PRD §2.1)
| Persona | Mục tiêu | Màn hình chính |
|---|---|---|
| Linh — chuyên viên kinh doanh | Hỏi nhanh, kiểm chứng nguồn | SCR-01..04, SCR-06 |
| Hùng — quản lý dự án (`manager`) | Đo mức sử dụng | SCR-05 |
| Mai — IT/Bảo mật | Không dùng UI hằng ngày | — |

## Bản đồ màn hình ↔ story ↔ API
| Màn hình | Story | API |
|---|---|---|
| SCR-01 Đăng nhập | US-101 | login, getMe, getConfig |
| SCR-02 Workspace | US-201..204, US-301..305, US-401..403, US-501 | listDocuments, uploadDocuments, createConversation, askQuestion, setFeedback |
| SCR-03 Panel trích dẫn | US-305 | getChunk |
| SCR-04 Xác nhận xóa | US-205 | deleteDocument |
| SCR-05 Dashboard | US-502 | getWeeklyMetrics |
| SCR-06 Phiên hết hạn | EC-15 | (401 từ bất kỳ API) → về SCR-01, giữ câu hỏi đang nhập trong `sessionStorage` |

## Delta so với blueprint v0.1 (do ADR v0.2)
| # | Blueprint v0.1 | v0.2 | Lý do |
|---|---|---|---|
| D-1 | Câu trả lời hiển thị dần (streaming SSE) | Hiển thị một lần, chỉ báo "Đang trả lời…" | ADR-006, NFR-001 cục bộ ≤ 2 s |
| D-2 | Font Be Vietnam Pro tải từ Google Fonts | Dùng font hệ thống (`system-ui, Segoe UI, Roboto, Arial`) | CSP `default-src 'self'` (SAD §8.1); máy nội bộ có thể không ra Internet |
| D-3 | Workspace có thể dùng chung | Workspace riêng | OQ-007 mặc định |
| D-4 | Framework front-end để ngỏ | HTML/CSS/JS thuần | ADR-006 |
| D-5 | Trạng thái tài liệu cập nhật qua sự kiện | Polling 2 s khi còn `processing` | ADR-006 |

Giữ nguyên: design token màu/khoảng cách/bo góc, vùng chạm 44 px, bố cục hai vùng (UX-001), trạng thái bằng biểu tượng + chữ (UX-002), Enter gửi / Shift+Enter xuống dòng (UX-009).

## WCAG 2.1 AA — điểm kiểm tra cho Phase 7
| Tiêu chí | Cách đáp ứng |
|---|---|
| 1.4.3 Contrast | Token `--color-text #111827` trên `#FFFFFF` (16:1), `--color-primary #1D4ED8` trên trắng (6.7:1) |
| 2.1.1 Keyboard | Mọi điều khiển là `button`/`input`/`a`; hộp thoại bẫy focus, Esc đóng |
| 2.4.7 Focus visible | `:focus-visible` outline 2 px |
| 3.3.1 Error identification | Lỗi upload hiển thị bằng chữ cạnh tên file |
| 4.1.2 Name, role, value | `aria-label` cho nút biểu tượng; `aria-pressed` cho nút đánh giá |
| 4.1.3 Status messages | `aria-live="polite"` cho vùng hội thoại và thông báo |
