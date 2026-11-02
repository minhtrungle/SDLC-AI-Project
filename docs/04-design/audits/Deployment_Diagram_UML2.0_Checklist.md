# Audit — Deployment Diagram theo checklist UML 2

| Mục | Giá trị |
|---|---|
| Tài liệu được audit | docs/04-design/diagrams/deployment_diagram.drawio (trang "Deployment"); đối chiếu SAD §7, §7.1, §7.2, NFR-006, ADR-002/003/007, design-refine-log.md |
| Checklist | docs/checklists/Deployment_Diagram_UML2.0_Checklist.xlsx |
| Reviewer | Vòng 1: Independent reviewer agent · Vòng 2: artifact-auditor (agent) |
| Ngày | Vòng 1: 2026-10-28 · Vòng 2: 2026-11-02 |
| Vòng | 2 — Audit lại 2026-11-02 sau REFINE (e1c8a1d) |
| Ghi chú vòng 2 | Đã áp dụng DF-11 (node «device» Kho sao lưu ngoài máy chủ + đường «schedule» 01:00), DF-21 (bỏ nhãn CMP-11 khỏi thư mục dữ liệu, sửa nhãn proxy → "HTTP (mạng nội bộ, cổng 8000)"), DF-10 (SAD §7.1 Resource view — chỉ trong SAD, không lên sơ đồ). |

| Row | Item | Status | Notes |
|---|---|---|---|
| 2 | Diagram Name | In Progress | Tên trang vẫn là "Deployment"; không nêu kịch bản (vd. "prod — máy chủ nội bộ DEP-003" theo SAD §7). |
| 3 | Scope & Topology | In Progress | Sơ đồ nay ngầm thể hiện on-premises ("mạng nội bộ, cổng 8000", "Kho sao lưu ngoài máy chủ (NAS/share do IT quản lý)", «external» Anthropic tách riêng) nhưng không ghi chữ on-premises/prod; SAD §7 có dev/test/prod nhưng sơ đồ không chỉ môi trường nào. |
| 4 | Device Nodes (<<device>>) | Done | shape=cube «device»: Máy trạm người dùng, Reverse proxy, Máy chủ ứng dụng, Console quản trị, Kho sao lưu ngoài máy chủ (mới, DF-11); «external» ACT-04 cube nét đứt. |
| 5 | Execution Environments (<<executionEnvironment>>) | In Progress | «execution env» Trình duyệt và «execution env» Python ≥ 3.12 — uvicorn cwd.main:app (1 worker) vẫn là chữ nhật thường (S_BOX) lồng trong node, không phải cube; stereotype viết tắt. |
| 6 | Node Specifications | In Progress | Sơ đồ có OS và runtime (Máy chủ ứng dụng "Windows/Linux", "Python ≥ 3.12", "1 worker"). CPU/RAM/đĩa đã có ở SAD §7.1 (2 vCPU, 4 GB RAM, 50 GB SSD) theo DF-10 nhưng chưa ghi lên node hay tagged value trong sơ đồ. |
| 7 | Artifacts (<<artifact>>) | In Progress | Dùng shape=note (biểu tượng tài liệu) cho app/backend/cwd, app/frontend/dist, cli.py, cwd.db, files/, backups/, bản build Web UI, nhưng không có stereotype «artifact»; «config» biến môi trường CWD_* cũng dùng note. |
| 8 | Deployment Relationships | N/A | Dùng lồng (row 10) thay cho «deploy». |
| 9 | Manifestations | In Progress | DF-21 đã sửa: «storage» CWD_DATA_DIR ghi "do CMP-11 (cwd.db) và CMP-04 (files/) quản lý", khớp SAD §5.2. Vẫn chỉ manifest ngầm qua nhãn CMP-xx, không có quan hệ «manifest»; artifact "app/backend/cwd (CMP-02..CMP-10, CMP-13)" bỏ sót CMP-11 dù db.py/schema.sql nằm trong package này. |
| 10 | Nesting (Alternative) | Done | Artifact lồng trong execution env (parent=env) và trong «storage» (parent=disk) của node Máy chủ ứng dụng; Web UI lồng trong Máy trạm. |
| 11 | Node Connections | Done | 5 đường kết nối liền (endArrow=none) giữa các node; đường tới Anthropic và tới kho sao lưu nét đứt để chỉ đường có điều kiện/theo lịch. |
| 12 | Protocols & Networks | In Progress | DF-21 đã bỏ mâu thuẫn 127.0.0.1 (nay "HTTP (mạng nội bộ, cổng 8000)"). Nhãn "HTTPS", "SSH / RDP", "«schedule» 01:00" vẫn không dạng stereotype giao thức («HTTPS», «SMB»); đường sao lưu không nêu giao thức. Nhãn "python -m app.cli" (console và sao lưu) lệch SAD §7.2 và AGENTS.md "python -m cwd.cli" (AUD-DEP-03). |
| 13 | Multiplicity | Pending | Vẫn không có multiplicity trên đường kết nối (máy trạm 1..30 theo ASM-003, 1 máy chủ, 1 kho sao lưu). |
| 14 | Disaster Recovery (DR) | In Progress | DF-11: có node «device» Kho sao lưu ngoài máy chủ, "backup hằng ngày, giữ 30 bản", đường «schedule» 01:00 (NFR-006, SAD §7.2) — dữ liệu không còn chỉ nằm cùng đĩa. Chưa mô hình đường khôi phục / máy chủ thay thế và chưa ghi RPO ≤ 24 h, RTO ≤ 4 h; không có failover (đúng ADR-002 một node, nhưng nên chú thích). |
| 15 | Databases & Storage | Done | SQLite nhúng nên «storage» CWD_DATA_DIR là ngăn riêng trong node Máy chủ ứng dụng, tách khỏi «execution env» (đúng ADR-002); lưu trữ sao lưu tách thành node «device» riêng ngoài máy chủ (DF-11). |
| 16 | Scalability & Constraints | In Progress | Chỉ ghi "1 worker" (ràng buộc LoginLimiter trong bộ nhớ + SQLite một writer); không chú thích nút thắt hay trigger mở rộng ADR-002, không tham chiếu giới hạn SAD §7.1 (≤ 5 câu hỏi đồng thời). |
| 17 | Clarity | Done | 6 node (5 «device» + 1 «external»), 5 đường kết nối, bố cục ba cột + node sao lưu phía dưới; theo tọa độ không có đường cắt chéo. |

## Kiểm tra lại vòng trước

| Vấn đề vòng 1 | Trạng thái vòng 2 | Bằng chứng |
|---|---|---|
| Không có DR, backups/ cùng đĩa (row 14, 15) | Đã sửa phần sao lưu ngoài máy (DF-11); thiếu đường khôi phục, RPO/RTO | Node "Kho sao lưu ngoài máy chủ"; SAD §7.2 |
| «storage» gán CMP-11 sai (row 9) | Đã sửa (DF-21) | Nhãn "do CMP-11 (cwd.db) và CMP-04 (files/) quản lý" |
| Mâu thuẫn proxy → 127.0.0.1 (row 12) | Đã sửa (DF-21) | Nhãn "HTTP (mạng nội bộ, cổng 8000)" |
| Thiếu thông số node (row 6) | Một phần — SAD §7.1 có, sơ đồ chưa có | DF-10 |
| Stereotype «artifact», «executionEnvironment», «HTTPS», multiplicity (row 5, 7, 12, 13) | Chưa sửa — DF-20 Partial | tools/gen_diagrams.py deployment() |

## Phát hiện

| ID | Mức | Vị trí | Mô tả | Khuyến nghị |
|---|---|---|---|---|
| AUD-DEP-01 | Minor | Node Máy chủ ứng dụng | Thiếu CPU/RAM/đĩa trên node dù SAD §7.1 đã có | Ghi "2 vCPU, 4 GB RAM, 50 GB SSD" vào nhãn node |
| AUD-DEP-02 | Minor | Node Kho sao lưu | Chưa có đường khôi phục và RPO/RTO | Thêm nhãn "restore — RTO ≤ 4 h, RPO ≤ 24 h (NFR-006)" |
| AUD-DEP-03 | Minor | Đường Console → Máy chủ, Máy chủ → Kho sao lưu | Nhãn "python -m app.cli" lệch lệnh thật "python -m cwd.cli" (SAD §7.2, AGENTS.md, package cwd theo ADR-009) | Sửa nhãn trong tools/gen_diagrams.py deployment() |
| AUD-DEP-04 | Minor | Artifact app/backend/cwd | Ghi CMP-02..CMP-10, CMP-13, bỏ sót CMP-11 (db.py, schema.sql) | Thêm CMP-11 hoặc tách artifact |
| AUD-DEP-05 | Minor | Toàn sơ đồ (DF-20) | Thiếu stereotype «artifact», «executionEnvironment» dạng cube, «HTTPS», multiplicity, tên kịch bản | Hoàn thành phần còn lại của DF-20 |

## Tóm tắt

- Status: Done 5 · In Progress 9 · Pending 1 · N/A 1 (tổng 16 dòng).
- Phát hiện: Critical 0 · Major 0 · Minor 5.
- Nhận định: **Cần sửa** (không chặn) — rủi ro chính vòng 1 (backup cùng đĩa) đã được xử lý; còn lại là thông số/stereotype/multiplicity và nhãn lệnh CLI sai.

## Lịch sử audit

| Vòng | Ngày | Thay đổi Status | Lý do |
|---|---|---|---|
| 1 | 2026-10-28 | Bản đầu: Done 4 · In Progress 8 · Pending 3 · N/A 1 | Audit độc lập trước REFINE |
| 2 | 2026-11-02 | Row 6 Pending → In Progress | Sơ đồ có OS/runtime; DF-10 đưa CPU/RAM/đĩa vào SAD §7.1 nhưng chưa lên node |
| 2 | 2026-11-02 | Row 14 Pending → In Progress | DF-11 thêm node Kho sao lưu ngoài máy chủ + lịch 01:00, giữ 30 bản; còn thiếu đường khôi phục và RPO/RTO |
| 2 | 2026-11-02 | Row 15 In Progress → Done | Lý do In Progress vòng 1 (chưa tách lưu trữ sao lưu) đã được DF-11 xử lý |
| 2 | 2026-11-02 | Các dòng khác giữ nguyên Status | Row 9, 12 cập nhật Notes theo DF-21 (vẫn In Progress vì thiếu «manifest»/stereotype giao thức); row 12 thêm lệch nhãn "app.cli" |
