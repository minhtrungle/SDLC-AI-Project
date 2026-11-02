# Audit — Component Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/component_diagram.drawio (trang "Components"); đối chiếu SAD §5.2, blueprint §3.2, elements.yaml, design-refine-log.md |
| Checklist | docs/checklists/Component_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Vòng 1: Independent reviewer agent · Vòng 2: artifact-auditor (agent) |
| Ngày | Vòng 1: 2026-10-28 · Vòng 2: 2026-11-02 |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d) |
| Ghi chú vòng 2 | DF-13 (đồng bộ phụ thuộc với SAD §5.2) đã áp dụng: 28 phụ thuộc nội bộ + 1 tới ACT-04 (29 cạnh). DF-20 (lollipop/socket/port) vẫn Partial, hoãn. |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | In Progress | Tên trang vẫn chỉ là "Components"; không nêu hệ thống/tầng (vd. "CWD — modular monolith app/backend + app/frontend"), không có boundary tiến trình ứng dụng. |
| 3 | Abstraction Level | Done | Nhất quán mức module (CMP-01..13, mỗi CMP một module theo elements.yaml) + một hệ thống ngoài ACT-04. textnorm không vẽ thành component riêng, đúng vai trò tiện ích ở SAD §5.2. |
| 4 | Component Nodes | Done | shape=component (biểu tượng component) cho cả 13 CMP. |
| 5 | Naming Conventions | Done | Nhãn "CMP-xx Tên" + module, khớp elements.yaml (cross_view_audit PASS sau REFINE). |
| 6 | Internal Structure (Optional) | N/A | Không thể hiện cấu trúc trong; mức chi tiết lớp nằm ở class_diagram.drawio. |
| 7 | Provided Interfaces (Lollipop) | Pending | Vẫn không có lollipop (CMP-02 REST API, CMP-06 Retriever, CMP-07 AnswerGenerator). DF-20 Partial: lollipop hoãn, owner Architect. |
| 8 | Required Interfaces (Socket) | Pending | Vẫn không có socket. DF-20 hoãn. |
| 9 | Interface Naming | In Progress | Tên interface chỉ là nhãn cạnh phụ thuộc: "HTTP/JSON", "Retriever", "AnswerGenerator", "current_user", "require_manager", "recover_pending", "textnorm.fold()"; không có phần tử interface có tên riêng. |
| 10 | Port Encapsulation | Pending | Không có port (vd. cổng HTTP của CMP-02). DF-20 hoãn. |
| 11 | Delegation Connectors | N/A | Không có cấu trúc trong nên không có delegation. |
| 12 | Usage Dependencies | Done | 29 cạnh nét đứt mũi tên mở (endArrow=open;dashed=1). Sau DF-13 đã có CMP-04/08/09 → CMP-03 (current_user, require_manager) và CMP-04/06/07 → CMP-13; khớp cột Phụ thuộc SAD §5.2. Còn Minor: cạnh CMP-05 → CMP-06 nhãn "textnorm.fold()" trong khi SAD §5.2 và blueprint §3.2 coi textnorm là module tiện ích lá (AUD-CMP-02). |
| 13 | Assembly Connectors | Pending | Không có ball-and-socket. DF-20 hoãn. |
| 14 | Realization | N/A | Interface không vẽ thành phần tử riêng nên không có realization. |
| 15 | Subsystems (<<subsystem>>) | N/A | Monolith nhỏ 13 module, không cần subsystem. |
| 16 | Artifacts (<<artifact>>) | N/A | Artifact (cwd.db, files/, app/frontend/dist) thể hiện ở deployment_diagram.drawio. |
| 17 | Loose Coupling | Done | CMP-08 dùng CMP-06/CMP-07 qua nhãn interface Retriever/AnswerGenerator; CMP-07 không phụ thuộc CMP-11 (khớp blueprint §3.2 "generation không import db"). |
| 18 | Readability | In Progress | Chưa có bản render PNG. Từ tọa độ: cạnh CMP-12 (60,620) → CMP-03 (60,300) là đường thẳng đi xuyên qua khối CMP-10 (60,460); CMP-11 nhận 8 cạnh vào (CMP-03/04/05/06/08/09/10/12), CMP-02 có 6 cạnh ra — nguy cơ cắt chéo tăng sau DF-13. |
| 19 | Orphaned Components | Done | Mọi component có quan hệ; CMP-13 nay nhận cạnh từ CMP-02/04/06/07, CMP-12 nối CMP-03/CMP-11. |

## Kiểm tra lại vòng trước

| Vấn đề vòng 1 | Trạng thái vòng 2 | Bằng chứng |
|---|---|---|
| Thiếu phụ thuộc CMP-04/08/09 → CMP-03 và CMP-04/06/07 → CMP-13 (row 12) | Đã sửa (DF-13) | COMPONENT_DEPS trong tools/gen_diagrams.py; component_diagram.drawio có nhãn current_user, require_manager |
| Cạnh CMP-05 → CMP-06 "fold()" mâu thuẫn blueprint (row 12) | Một phần — SAD §5.2 ghi textnorm là tiện ích, nhưng cạnh vẫn trỏ CMP-06 | Nhãn "textnorm.fold()" |
| Không có lollipop/socket/port/assembly (row 7, 8, 10, 13) | Chưa sửa — DF-20 Partial | design-refine-log.md DF-20 |
| Tên trang chung chung (row 2) | Chưa sửa | diagram name="Components" |
| Readability chưa kiểm chứng (row 18) | Chưa sửa; số cạnh tăng 23 → 29 | — |

## Phát hiện

| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-CMP-01 | Major | Toàn sơ đồ (row 7, 8, 10, 13) | Không dùng ký hiệu interface UML (lollipop/socket/port/assembly); sơ đồ là dependency diagram | Thực hiện phần còn lại của DF-20 hoặc ghi rõ quy ước ký hiệu được chấp nhận trong SAD |
| AUD-CMP-02 | Minor | Cạnh CMP-05 → CMP-06 "textnorm.fold()" | Lệch SAD §5.2 và blueprint §3.2 (textnorm là module lá, không thuộc CMP-06) | Bỏ cạnh hoặc chú thích textnorm là tiện ích dùng chung |
| AUD-CMP-03 | Minor | Cạnh CMP-12 → CMP-03 | Đường thẳng xuyên qua khối CMP-10 | Thêm waypoint hoặc đổi vị trí CMP-12; render PNG để review |
| AUD-CMP-04 | Minor | Tên trang | "Components" không nêu hệ thống/tầng | Đổi tên trang, thêm boundary |

## Tóm tắt

- Status: Done 6 · In Progress 3 · Pending 4 · N/A 5 (tổng 18 dòng).
- Phát hiện: Critical 0 · Major 1 · Minor 3.
- Nhận định: **Cần sửa** — nội dung phụ thuộc đã khớp SAD sau DF-13, nhưng 4 dòng ký hiệu interface vẫn Pending (DF-20 hoãn).

## Lịch sử audit

| Vòng | Ngày | Thay đổi Status | Lý do |
|---|---|---|---|
| 1 | 2026-10-28 | Bản đầu: Done 6 · In Progress 3 · Pending 4 · N/A 5 | Audit độc lập trước REFINE |
| 2 | 2026-11-02 | Không dòng nào đổi Status | DF-13 xử lý phần thiếu phụ thuộc mà row 12 (vốn đã Done) ghi chú; các dòng Pending 7, 8, 10, 13 thuộc DF-20 còn hoãn; row 2, 9, 18 không được sửa. Cập nhật Notes row 3, 9, 12, 17, 18 (phát hiện cạnh CMP-12 → CMP-03 xuyên CMP-10), 19 |
