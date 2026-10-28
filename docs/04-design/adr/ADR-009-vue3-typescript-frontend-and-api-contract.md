# ADR-009 — Frontend Vue 3 + TypeScript tách riêng, hợp đồng API là thư mục riêng

- **Trạng thái:** Proposed (chờ Tech Lead duyệt) · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Thay thế:** [ADR-006](ADR-006-vanilla-spa-no-build.md) (SPA JavaScript thuần, không bước build)
- **Yêu cầu từ:** chủ dự án (2026-10-28): "tạo folder frontend riêng code bằng Vue 3, TypeScript, backend riêng code bằng Python, folder api contract"

## Bối cảnh
- ADR-006 chọn JavaScript thuần vì máy dev chỉ có Node 14. Node 22.23.4 LTS nay đã được cài.
- JavaScript thuần không có kiểm tra kiểu. Mỗi lần đổi hợp đồng API, frontend có thể lệch mà không ai biết (ADR-006 đã ghi đây là hệ quả tiêu cực).
- Review L1 (CR-11) chỉ ra việc dựng lại DOM thủ công làm mất focus bàn phím. Framework có reactive rendering giải quyết vấn đề này một cách tự nhiên.

## Quyết định
1. **Cấu trúc thư mục**, toàn bộ implement nằm trong `app/`:
   ```
   app/
   ├── api-contract/openapi.yaml   nguồn sự thật duy nhất của API (OpenAPI 3.1)
   ├── backend/                    Python ≥ 3.12, FastAPI; package `cwd`, tests/
   └── frontend/                   Vue 3 + TypeScript + Vite; src/, *.spec.ts
   ```
2. **Frontend:** Vue 3.5 (Composition API, `<script setup lang="ts">`), TypeScript 5.9 strict, Vite 8, Vitest 5 + Vue Test Utils, ESLint 10 (typescript-eslint, eslint-plugin-vue; cấm `v-html`). Node ≥ 22.12. Không dùng router hay store bên ngoài: trạng thái nằm trong composable (`useSession`, `useDocuments`, `useChat`), quá ít màn hình để cần thêm thư viện.
3. **Hợp đồng là nguồn sinh code:** `npm run gen:api` sinh `src/api/schema.d.ts` từ `app/api-contract/openapi.yaml` bằng openapi-typescript. `npm run check:api` (trong CI) thất bại khi file sinh ra lệch hợp đồng. Phía backend, `tools/cross_view_audit.py` đối chiếu route FastAPI và enum mã lỗi với cùng file đó.
4. **Triển khai:** `npm run build` tạo `app/frontend/dist/`; FastAPI phục vụ `index.html` tại `/` và bundle tại `/assets` (một tiến trình, giữ ADR-001/008). Khi phát triển, `npm run dev` (Vite, cổng 5173) proxy `/api` sang uvicorn cổng 8000.
5. **Phiên bản phụ thuộc:** pin chính xác. Mỗi gói chọn bản ổn định mới nhất đã phát hành ít nhất 14 ngày (giảm rủi ro chuỗi cung ứng). Riêng TypeScript giữ 5.9.3 vì typescript-eslint yêu cầu < 6.1 và openapi-typescript yêu cầu 5.x. `.npmrc` bật `legacy-peer-deps` để tránh lỗi arborist khi giải optional peer của vitest; các peer bắt buộc được khai báo tường minh.

## Phương án đã cân nhắc
| Phương án | Lý do không chọn |
|---|---|
| Giữ JavaScript thuần (ADR-006) | Không đáp ứng yêu cầu chủ dự án; không có kiểm tra kiểu với hợp đồng |
| Vite 2 + Vue 3 trên Node 14 | Toolchain đã hết hỗ trợ, có lỗ hổng đã biết |
| React | Chủ dự án chỉ định Vue 3 |
| Nuxt / SSR | Ứng dụng sau đăng nhập, không cần SEO; thêm máy chủ Node |
| Tách repo frontend/backend | Một đội nhỏ, một sản phẩm; monorepo giữ hợp đồng và hai phía đồng bộ trong một commit |

## Hệ quả
- (+) Kiểm tra kiểu từ hợp đồng tới component; lệch hợp đồng làm CI thất bại.
- (+) Test component (43 test, coverage > 75%), lint, type-check nằm trong cổng L0.
- (+) CSP `default-src 'self'` vẫn giữ được: bản build không có script inline; style động đặt qua CSSOM (`:style`).
- (−) Cần Node ≥ 22.12 để build. Máy chạy production chỉ cần Python nếu dùng `dist/` đã build sẵn.
- (−) Thêm khoảng 250 gói npm (devDependencies; `npm audit` = 0 lỗ hổng tại thời điểm chọn).
- **Khó đảo ngược:** Trung bình. Hợp đồng API độc lập nên có thể viết lại frontend mà không đổi backend.
