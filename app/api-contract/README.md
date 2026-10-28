# API contract — Chat với tài liệu

[`openapi.yaml`](openapi.yaml) (OpenAPI 3.1) là **nguồn sự thật duy nhất** của giao tiếp giữa `app/frontend` và `app/backend` (ADR-009). Giải thích quy ước, bảng mã lỗi và ví dụ nằm ở [docs/04-design/openapi.md](../../docs/04-design/openapi.md).

## Ai dùng file này
| Bên | Cách dùng | Kiểm tra lệch |
|---|---|---|
| Frontend | `npm run gen:api` sinh `app/frontend/src/api/schema.d.ts` (openapi-typescript) | `npm run check:api` thất bại nếu file sinh ra lệch hợp đồng |
| Backend | Route FastAPI và enum mã lỗi (`cwd/errors.py`) phải khớp | `python tools/cross_view_audit.py` (so với `docs/04-design/elements.yaml`) |
| Test | `app/backend/tests/test_isolation.py` sinh test 401 cho mọi endpoint không công khai từ registry | pytest |

## Quy trình đổi hợp đồng
1. Sửa `openapi.yaml`, cập nhật `docs/04-design/elements.yaml` nếu thêm/bớt endpoint.
2. Ghi ADR nếu là thay đổi phá vỡ (breaking).
3. Backend: hiện thực + test.
4. Frontend: `npm run gen:api`, sửa code cho đến khi `npm run type-check` qua.
5. Chạy `python tools/ci_local.py`: mọi bước kiểm tra lệch phải xanh.
