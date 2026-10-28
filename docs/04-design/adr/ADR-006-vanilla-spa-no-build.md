# ADR-006 — Giao diện SPA bằng HTML/CSS/JavaScript thuần, không bước build

- **Trạng thái:** Proposed · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Thay thế:** AD-07 của SAD v0.1 (React 18 + TypeScript + Vite)

## Bối cảnh
- Vite và React tooling hiện tại cần Node ≥ 18; môi trường có Node 14 (SRC-005).
- Giao diện MVP nhỏ: 1 màn hình đăng nhập, 1 workspace, 1 panel trích dẫn, 1 hộp thoại, 1 dashboard.
- Prototype HTML trong `UI_UX_design/` đã viết bằng HTML/CSS thuần với design token.

## Quyết định
- Viết SPA bằng **ES2020 modules thuần** trong `app/web/` (một `index.html`, `app.js`, `api.js`, `styles.css`), FastAPI phục vụ dạng file tĩnh.
- Tái sử dụng design token và component CSS của prototype (`UI_UX_design/html_design/`).
- **Không streaming** (UX-005) trong MVP: chế độ cục bộ trả lời ≤ 2 s (NFR-001); hiển thị chỉ báo "Đang trả lời…".
- Cập nhật trạng thái tài liệu bằng polling 2 s khi còn tài liệu `processing` (AC-203.2).

## Phương án đã cân nhắc
| Phương án | Lý do không chọn |
|---|---|
| React + Vite | Không chạy trên Node 14 |
| React qua CDN, không build | Phụ thuộc mạng ngoài lúc chạy; JSX cần Babel trên trình duyệt |
| Server-side render (Jinja2) | Tương tác hội thoại, upload nhiều file cần JS nhiều; thêm một mô hình lập trình |

## Hệ quả
- (+) Không có bước build, không có `node_modules`; giao diện chạy ngay khi chạy backend.
- (−) Không có type check cho frontend; giảm thiểu bằng test E2E API và giữ JS nhỏ (< 800 dòng).
- **Khó đảo ngược:** Thấp — API tách biệt, có thể viết lại frontend bằng framework bất kỳ.
