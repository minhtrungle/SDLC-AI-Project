# ADR-001 — Backend Python + FastAPI

- **Trạng thái:** Proposed (chờ Tech Lead duyệt) · **Ngày:** 2026-10-28 · **Tác giả:** Agent (Claude)
- **Liên quan:** SAD §4, §9; thay thế quyết định AD-02 của SAD v0.1 (giữ nguyên lựa chọn, bổ sung bối cảnh môi trường)

## Bối cảnh
- Cần đọc PDF, xử lý văn bản tiếng Việt, gọi mô hình AI, sinh hợp đồng API tự động.
- Môi trường thực tế của đội (SRC-005): Python 3.15.2; Node 14.19.3; không có Docker.
- Đã kiểm tra: `fastapi 0.162`, `pydantic 2.14`, `pypdf 6.21` cài và chạy được trên Python 3.15.

## Quyết định
Dùng **Python ≥ 3.12 + FastAPI + Uvicorn** cho toàn bộ backend, một tiến trình duy nhất (modular monolith).

## Phương án đã cân nhắc
| Phương án | Lý do không chọn |
|---|---|
| Node.js / NestJS | Node 14 đã hết hỗ trợ; hệ sinh thái PDF/NLP yếu hơn |
| Java / Spring | Nặng cho MVP, đội không có JDK sẵn |
| Tách microservice (API, worker) | Thêm vận hành, hàng đợi; quy mô ≤ 30 người dùng không cần |

## Hệ quả
- (+) Tự sinh OpenAPI; test bằng `TestClient` không cần mạng.
- (+) Một tiến trình: triển khai bằng một lệnh, phù hợp môi trường không Docker.
- (−) Mở rộng ngang cần tách ingestion (ADR-008) và đổi kho dữ liệu (ADR-002).
- **Khó đảo ngược:** Trung bình — đổi ngôn ngữ là viết lại backend, nhưng hợp đồng API (openapi.yaml) giữ nguyên.
