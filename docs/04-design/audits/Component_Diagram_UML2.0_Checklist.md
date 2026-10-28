# Audit — Component Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/component_diagram.drawio (trang "Components"); đối chiếu SAD §5.2, blueprint §3.2, elements.yaml |
| Checklist | docs/checklists/Component_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Independent reviewer agent |
| Ngày | 2026-10-28 |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | In Progress | Tên trang chỉ là "Components"; không nêu hệ thống/tầng (vd. "CWD — ứng dụng modular monolith"). Không có boundary của tiến trình ứng dụng. |
| 3 | Abstraction Level | Done | Nhất quán mức module Python (CMP-01..13) + một hệ thống ngoài. |
| 4 | Component Nodes | Done | shape=component (biểu tượng component) cho 13 CMP. |
| 5 | Naming Conventions | Done | Tên + module, khớp elements.yaml (cross-view-audit PASS). |
| 6 | Internal Structure (Optional) | N/A | Không thể hiện cấu trúc trong. |
| 7 | Provided Interfaces (Lollipop) | Pending | Không có ký hiệu lollipop (vd. CMP-02 cung cấp REST API, CMP-06 cung cấp Retriever, CMP-07 cung cấp AnswerGenerator). |
| 8 | Required Interfaces (Socket) | Pending | Không có socket. |
| 9 | Interface Naming | In Progress | Tên interface chỉ là nhãn cạnh: "Retriever", "AnswerGenerator", "HTTP/JSON", "fold()", "recover_pending". |
| 10 | Port Encapsulation | Pending | Không có port (vd. cổng HTTP của CMP-02). |
| 11 | Delegation Connectors | N/A | Không có cấu trúc trong. |
| 12 | Usage Dependencies | Done | 23 nét đứt mũi tên mở thể hiện phụ thuộc. Thiếu phụ thuộc: CMP-04/CMP-08/CMP-09 → CMP-03 (current_user, require_csrf, require_manager); CMP-06, CMP-04, CMP-07 → CMP-13 (Settings — class diagram có "FtsRetriever reads Settings"). Cạnh CMP-05 → CMP-06 "fold()" mâu thuẫn blueprint §3.2 (textnorm là lá). |
| 13 | Assembly Connectors | Pending | Không có ball-and-socket. |
| 14 | Realization | N/A | Interface không vẽ thành phần tử riêng. |
| 15 | Subsystems (<<subsystem>>) | N/A | Monolith nhỏ, không cần subsystem. |
| 16 | Artifacts (<<artifact>>) | N/A | Artifact (cwd.db, files/, schema.sql) thể hiện ở deployment diagram. |
| 17 | Loose Coupling | Done | Chat Service giao tiếp với Retriever/Generator qua interface có tên; generation không chạm Persistence. |
| 18 | Readability | In Progress | Không thể xác minh bằng render; CMP-02 có 6 cạnh ra và CMP-11 có 7 cạnh vào, nguy cơ cắt chéo. Cần xuất PNG để review. |
| 19 | Orphaned Components | Done | Mọi component có ít nhất một quan hệ; CMP-13 chỉ nối từ CMP-02. |

## Tóm tắt
Sơ đồ là "dependency diagram" dùng biểu tượng component: đúng tên và phụ thuộc chính nhưng không dùng interface lollipop/socket, port hay assembly, và thiếu một số phụ thuộc thật (auth, config). Phụ thuộc trong sơ đồ không khớp hoàn toàn với SAD §5.2.
